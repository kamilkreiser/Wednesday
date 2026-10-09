/**
 * KS-445 — Postgres SQLSTATE classification.
 *
 * Covers the two halves of the classification chain:
 *  - utils/pgErrors.extractPgCode: normalises the three error shapes originate
 *    sees (bare pg `code`, Prisma-wrapped `meta.code`, message-embedded text).
 *  - gdprService.recordConsent / createDSR: re-throw their sanitised wrapper
 *    Error WITH the SQLSTATE preserved as `pgCode`, so the route can map
 *    unknown-user / bad-value failures to 404/400 instead of a raw 500.
 *
 * Service mocks mirror gdprService.erasure.test.ts (prisma + shared crypto).
 */

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

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    encryptField: jest.fn((v: string) => v),
    decryptField: jest.fn((v: string) => v),
    // KS-291 subject-DEK surface used by gdprService's PII helpers.
    encryptFieldWithDek: jest.fn((v: string) => v),
    decryptFieldWithDek: jest.fn((v: string) => v),
    isSubjectDekCiphertext: jest.fn(() => false),
    isEncryptedPii: jest.fn(() => false),
    SubjectDekProvider: class {
      getOrCreateDek = async () => Buffer.alloc(32);
      getDek = async () => null;
      destroyDek = async () => 'destroyed' as const;
      evict = () => undefined;
    },
  }),
);

jest.mock('../services/subjectDeks', () => ({
  subjectDeks: {
    getOrCreateDek: jest.fn(async () => Buffer.alloc(32)),
    getDek: jest.fn(async () => null),
    destroyDek: jest.fn(async () => 'destroyed'),
    evict: jest.fn(),
  },
}));

jest.mock('../events', () => ({
  publishEvent: jest.fn().mockResolvedValue(undefined),
  EventTypes: { USER_ERASED: 'user.erased' },
}));

import { extractPgCode } from '../utils/pgErrors';
import { recordConsent, createDSR } from '../services/gdprService';

beforeEach(() => jest.clearAllMocks());

describe('KS-445 extractPgCode', () => {
  it('reads a bare pg driver error (SQLSTATE on err.code)', () => {
    expect(extractPgCode({ code: '23503', message: 'violates foreign key constraint' })).toBe('23503');
  });

  it('reads a Prisma-wrapped error (P2010 on code, SQLSTATE on meta.code)', () => {
    expect(
      extractPgCode({ code: 'P2010', meta: { code: '42804' }, message: 'Raw query failed.' }),
    ).toBe('42804');
  });

  it('never returns Prisma’s own P-code as if it were a SQLSTATE', () => {
    expect(extractPgCode({ code: 'P2010', message: 'Raw query failed.' })).toBeUndefined();
  });

  it('falls back to a known code embedded in the message text', () => {
    expect(extractPgCode(new Error('Raw query failed. Code: `22P02`. Message: invalid input'))).toBe('22P02');
  });

  it('does not false-match arbitrary 5-char tokens in the message', () => {
    // "ABC12" is 5 chars but not one of the known SQLSTATEs the routes map.
    expect(extractPgCode(new Error('failure token ABC12 occurred'))).toBeUndefined();
  });

  it('recognises 22P05 (untranslatable character — the jsonb NUL-escape rejection)', () => {
    // Postgres refuses \u0000 inside a jsonb value with SQLSTATE 22P05; the
    // certifications/issue fuzz-500 rode exactly this class.
    expect(extractPgCode({ code: '22P05', message: 'unsupported Unicode escape sequence' })).toBe('22P05');
    expect(extractPgCode(new Error('Raw query failed. Code: `22P05`. unsupported Unicode escape sequence'))).toBe('22P05');
  });

  it('is safe on non-object inputs', () => {
    expect(extractPgCode(undefined)).toBeUndefined();
    expect(extractPgCode(null)).toBeUndefined();
    expect(extractPgCode('boom')).toBeUndefined();
  });
});

describe('KS-445 gdprService SQLSTATE tagging', () => {
  it('recordConsent re-throws its sanitised error WITH pgCode preserved (FK 23503)', async () => {
    // Prisma-wrapped FK violation: valid UUID, but no such row in users.
    mockQueryRaw.mockRejectedValueOnce(
      Object.assign(new Error('Raw query failed. Code: `23503`.'), { code: 'P2010', meta: { code: '23503' } }),
    );
    await expect(
      recordConsent('11111111-2222-4333-8444-555555555555', 'marketing'),
    ).rejects.toMatchObject({ message: 'Failed to record consent', pgCode: '23503' });
  });

  it('createDSR re-throws its sanitised error WITH pgCode preserved (22001 truncation)', async () => {
    // Message-only shape: the SQLSTATE survives via the text fallback.
    mockQueryRaw.mockRejectedValueOnce(new Error('Raw query failed. Code: `22001`. value too long'));
    await expect(
      createDSR('access', '11111111-2222-4333-8444-555555555555', 'subject@example.com'),
    ).rejects.toMatchObject({ message: 'Failed to create data subject request', pgCode: '22001' });
  });

  it('leaves pgCode undefined for unclassifiable failures (route keeps its 500)', async () => {
    mockQueryRaw.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
    await expect(
      recordConsent('11111111-2222-4333-8444-555555555555', 'marketing'),
    ).rejects.toMatchObject({ message: 'Failed to record consent', pgCode: undefined });
  });
});
