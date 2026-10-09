// KS-1028 (KS-754 gate F-1, MAJOR): a step-12 throw in executeErasureImpl must NOT skip
// the step-13 USER_ERASED fan-out that runs AFTER the crypto-shred (step 11). Before the
// fix a rejected updateDSRStatus jumped straight to the outer catch, so the DEK was gone
// and no downstream service ever heard about it. The mocks are the erasure driver's
// (gdprService.erasure.test.ts) copied whole; only the step-12 UPDATE is made to throw,
// matched with indexOf on the lower-cased SQL text (no regex).

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: mockExecuteRaw,
  },
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

jest.mock('@secuura/shared', () => require('./helpers/sharedModuleMock').makeSharedMock({
  publishEvent: jest.fn().mockResolvedValue(undefined),
  EventTypes: { USER_ERASED: 'user.erased' },
  encryptField: jest.fn((v: string) => v),
  decryptField: jest.fn((v: string) => v),
  encryptFieldWithDek: jest.fn((v: string) => v),
  decryptFieldWithDek: jest.fn((v: string) => v),
  isSubjectDekCiphertext: jest.fn(() => false),
  isEncryptedPii: jest.fn(() => false),
  runWithPlatformScope: jest.fn(<T,>(fn: () => T): T => fn()),
  SubjectDekProvider: class { getOrCreateDek = async () => Buffer.alloc(32); getDek = async () => null; destroyDek = async () => 'destroyed'; evict = () => undefined; },
}));

const mockDestroyDek = jest.fn().mockResolvedValue('destroyed');
jest.mock('../services/subjectDeks', () => ({
  subjectDeks: {
    getOrCreateDek: jest.fn(async () => Buffer.alloc(32)),
    getDek: jest.fn(async () => null),
    destroyDek: mockDestroyDek,
    evict: jest.fn(),
  },
}));

const mockLocalPublish = jest.fn().mockResolvedValue(undefined);
jest.mock('../events', () => ({
  publishEvent: mockLocalPublish,
  EventTypes: { USER_ERASED: 'user.erased' },
}));

import { executeErasure } from '../services/gdprService';

/** Every executeRaw succeeds except the step-12 UPDATE of data_subject_requests, which throws. */
function failStep12(): void {
  mockExecuteRaw.mockImplementation(async (strings: readonly string[]) => {
    const sql = strings.join(' ? ').toLowerCase();
    if (sql.indexOf('update data_subject_requests') >= 0) throw new Error('step-12 boom (KS-1028)');
    return 1;
  });
}

const USER_ID = '11111111-1111-1111-1111-111111111111';
const DSR_ID = '22222222-2222-2222-2222-222222222222';
const ADMIN_ID = '33333333-3333-3333-3333-333333333333';

describe('KS-1028: a step-12 throw does not skip the USER_ERASED fan-out', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockExecuteRaw.mockResolvedValue(1);
    mockQueryRaw.mockResolvedValue([{ id: 'log-row', records_affected: 1 }]);
  });

  it('RED KS-1028 A: when the DSR status write throws after the shred, user.erased is STILL published', async () => {
    failStep12();
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(mockDestroyDek).toHaveBeenCalledWith(USER_ID);
    expect(mockLocalPublish).toHaveBeenCalledWith('user.erased', expect.objectContaining({ userId: USER_ID, dsrId: DSR_ID }));
  });

  it('RED KS-1028 B: the fan-out fires AFTER the shred, and the shred is not repeated', async () => {
    failStep12();
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(mockDestroyDek).toHaveBeenCalledTimes(1);
    expect(mockLocalPublish).toHaveBeenCalledTimes(1);
    expect(mockDestroyDek.mock.invocationCallOrder[0]).toBeLessThan(mockLocalPublish.mock.invocationCallOrder[0]);
  });

  it('control: the step-12 failure still fails the erasure (success false), before and after', async () => {
    failStep12();
    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(result.success).toBe(false);
  });

  it('control: with no failure the erasure succeeds and publishes once', async () => {
    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(result.success).toBe(true);
    expect(mockLocalPublish).toHaveBeenCalledTimes(1);
  });
});
