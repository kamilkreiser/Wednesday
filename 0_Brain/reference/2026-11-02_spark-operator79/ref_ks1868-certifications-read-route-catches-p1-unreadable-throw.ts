// KS-1868 (originate routes/certifications.ts, GET /api/certifications, GET /:id/lineage, GET /:id/evidence-bundle): each route catch logged
// `error instanceof Error ? error.message : String(error)` itself and then answered a constant 500. When the thrown value cannot be read (a revoked Proxy makes
// `instanceof` throw; an Error whose `message` getter throws), that read threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Each catch
// now reads the value inside its own try and logs the constant reason `unreadable thrown value`. The repository stand-in rejects with the thrown value on a real loopback
// listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
const mockGetCertification = jest.fn();
const mockListCertifications = jest.fn();
const mockSaveCertification = jest.fn(async (..._a: unknown[]) => undefined);
const mockGetShares = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
const mockGetLineageEvents = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
const mockCreateChargeEvent = jest.fn(async (..._a: unknown[]) => ({ id: 'charge-new', eventType: 'evidence_export' }));
const mockGetChargeEvents = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };

jest.mock('../repositories/certificationRepo', () => ({
  initRepo: jest.fn(async () => undefined),
  getCertification: (...a: unknown[]) => mockGetCertification(...a),
  saveCertification: (...a: unknown[]) => mockSaveCertification(...a),
  listCertifications: (...a: unknown[]) => mockListCertifications(...a),
  saveShare: jest.fn(),
  getSharesByCertification: (...a: unknown[]) => mockGetShares(...a),
  getLineageEvents: (...a: unknown[]) => mockGetLineageEvents(...a),
  deleteCertification: jest.fn(),
  reserveCertificationRow: jest.fn(),
}));
jest.mock('../db', () => ({
  prisma: { $queryRaw: jest.fn(async () => []), $executeRaw: jest.fn(async () => 1), $executeRawUnsafe: jest.fn() },
}));
jest.mock('../services/chargeEvents', () => ({
  createChargeEvent: (...a: unknown[]) => mockCreateChargeEvent(...a),
  getChargeEventsByCertification: (...a: unknown[]) => mockGetChargeEvents(...a),
}));
jest.mock('../utils/notificationClient', () => ({
  notifyDocumentCertified: jest.fn(async () => undefined),
  notifyDocumentRevoked: jest.fn(async () => undefined),
  notifyDocumentShared: jest.fn(async () => undefined),
}));
jest.mock('../events', () => ({
  publishEvent: jest.fn(async () => undefined),
  EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' },
}));
jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(),
  saveDocument: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
  generateContentHash: jest.fn(() => 'hash'),
}));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = null; next(); },
}));
jest.mock('../utils/logger', () => ({ logger: mockLog }));

import express from 'express';
import { certificationsRouter } from '../routes/certifications';

const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
const CERT_ID = 'aaaaaaaa-1111-4111-8111-111111111111';
const UNREADABLE = 'unreadable thrown value';

const ROUTES = [
  { route: 'GET /', path: '', context: 'Failed to list certifications', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list certifications' } }, rejecter: mockListCertifications },
  { route: 'GET /:id/lineage', path: `/${CERT_ID}/lineage`, context: 'Failed to get lineage', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get lineage data' } }, rejecter: mockGetCertification },
  { route: 'GET /:id/evidence-bundle', path: `/${CERT_ID}/evidence-bundle`, context: 'Failed to generate evidence bundle', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to generate evidence bundle' } }, rejecter: mockGetCertification },
];

const app = express();
app.use((req: any, _res: unknown, next: () => void) => { req.tenantId = TENANT; next(); });
app.use('/api/certifications', express.json(), certificationsRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;
beforeAll(async () => {
  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});
afterAll(() => { server?.close(); });

beforeEach(() => {
  jest.clearAllMocks();
});

async function callWithThrow(c: (typeof ROUTES)[number], thrown: unknown): Promise<{ status: number | string; body?: unknown }> {
  c.rejecter.mockRejectedValueOnce(thrown);
  try {
    const res = await fetch(`${baseUrl}/api/certifications${c.path}`, { signal: AbortSignal.timeout(1500) });
    return { status: res.status, body: await res.json() };
  } catch {
    return { status: 'NO ANSWER' };
  }
}

const revokedProxy = (): object => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};
const throwingMessageError = (): Error =>
  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
    get(): string {
      throw new Error('ks1868 message getter threw');
    },
  });

// G105-F1 (gate 105): an Error whose `message` getter RETURNS a hostile non-string. The guard's expression returned that object unchanged, so `reason` was the object, and the
// REAL winston logger (KS-1348 redaction and the dev format) throws on it inside logger.error, outside the guard's try: the request got no answer. The gate measured two such values:
// a getter returning a revoked Proxy and a getter returning an object whose toJSON throws. The cells below send logger.error through the real logger (its transports' output
// swallowed, its formats still run) so that the failure is the real one, and the ordinary-Error control C3 shows the same harness answers normally.
const messageGetterReturningRevokedProxy = (): Error =>
  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
    get(): unknown {
      return revokedProxy();
    },
  });
const messageGetterReturningThrowingToJson = (): Error =>
  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
    get(): unknown {
      return {
        toJSON(): never {
          throw new Error('ks1868 toJSON threw');
        },
      };
    },
  });
function useRealLogger(): void {
  const real = jest.requireActual('../utils/logger').logger;
  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
    t.log = (_info: unknown, next: () => void) => next();
  });
  mockLog.error.mockImplementation((...a: unknown[]) => (real.error as (...x: unknown[]) => unknown)(...a));
}
afterEach(() => {
  mockLog.error.mockReset();
});

describe.each(ROUTES)('KS-1868 $route catch reads the thrown value safely', (c) => {
  it(`RED ks1868 R1 ${c.route}: a revoked Proxy from the repository is logged as a constant reason and answered with the constant 500`, async () => {
    expect(await callWithThrow(c, revokedProxy())).toEqual({ status: 500, body: c.constant });
    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
  });

  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and answered with the constant 500`, async () => {
    expect(await callWithThrow(c, throwingMessageError())).toEqual({ status: 500, body: c.constant });
    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
  });

  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its own message and the answer is the constant 500`, async () => {
    expect(await callWithThrow(c, new Error('ks1868 ordinary'))).toEqual({ status: 500, body: c.constant });
    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
  });

  it(`control ks1868 C2 ${c.route}: a thrown string is logged as itself, as before`, async () => {
    expect(await callWithThrow(c, 'ks1868 plain string')).toEqual({ status: 500, body: c.constant });
    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: 'ks1868 plain string' }]]);
  });

  it(`RED ks1868 R3 ${c.route}: an Error whose message getter returns a revoked Proxy gets the constant 500 through the real logger`, async () => {
    useRealLogger();
    expect(await callWithThrow(c, messageGetterReturningRevokedProxy())).toEqual({ status: 500, body: c.constant });
    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
  });

  it(`RED ks1868 R4 ${c.route}: an Error whose message getter returns an object with a throwing toJSON gets the constant 500 through the real logger`, async () => {
    useRealLogger();
    expect(await callWithThrow(c, messageGetterReturningThrowingToJson())).toEqual({ status: 500, body: c.constant });
    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: '[object Object]' }]]);
  });

  it(`control ks1868 C3 ${c.route}: an ordinary Error through the real logger gets the constant 500 and its own message is logged`, async () => {
    useRealLogger();
    expect(await callWithThrow(c, new Error('ks1868 ordinary'))).toEqual({ status: 500, body: c.constant });
    expect(mockLog.error.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
  });
});
