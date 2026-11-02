// KS-1868 (originate routes/certifications.ts, POST /api/certifications/:id/recertify): each route catch logged
// `error instanceof Error ? error.message : String(error)` itself and then answered a constant 500. When the thrown value cannot be read (a revoked Proxy makes
// `instanceof` throw; an Error whose `message` getter throws), that read threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Each catch
// now reads the value inside its own try and logs the constant reason `unreadable thrown value`. getCertification rejects with the thrown value on a real loopback
// listener, before the route has written or anchored anything; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
const mockGetCertification = jest.fn();
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
  listCertifications: jest.fn(),
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
  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = { userId: '11111111-2222-4333-8444-555555555555', email: 'ks1868@example.test' }; next(); },
}));
jest.mock('../utils/logger', () => ({ logger: mockLog }));

import express from 'express';
import { certificationsRouter } from '../routes/certifications';

const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
const CERT_ID = 'aaaaaaaa-1111-4111-8111-111111111111';
const UNREADABLE = 'unreadable thrown value';

const ROUTES = [
  { route: 'POST /:id/recertify', path: `/${CERT_ID}/recertify`, context: 'Failed to issue verification certificate', constant: { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to issue verification certificate' } }, payload: { note: 'ks1868' } },
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
  mockGetCertification.mockRejectedValueOnce(thrown);
  try {
    const res = await fetch(`${baseUrl}/api/certifications${c.path}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(c.payload),
      signal: AbortSignal.timeout(1500),
    });
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
  it(`RED ks1868 R1 ${c.route}: a revoked Proxy from getCertification is logged as a constant reason and answered with the constant 500`, async () => {
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

// G105-F1, after the write: recertify has built the verification certificate and saveCertification has APPLIED it when the failure arrives. `stored` models what the repository
// kept (the new certificate id); the hostile cells must leave it exactly as the ordinary-Error control does, and answer the constant 500 instead of nothing. The route's anchoring
// call is intercepted at the global fetch (the cell's own client passes through) and rejects with an ordinary Error, which the route swallows outside production, as in the gate's probe.
// The cell never names the anchoring base variable and never leaves this process, so the KS-1293 hermeticity pin has nothing to flag.
describe('KS-1868 G105-F1 POST /:id/recertify: the failure arrives after saveCertification applied the write', () => {
  const issuerId = '11111111-2222-4333-8444-555555555555';
  async function recertifyThenFail(thrown: unknown): Promise<{ status: number | string; body?: unknown; storedType: string | null }> {
    const stored: { type: string | null } = { type: null };
    const clientFetch = globalThis.fetch;
    const fetchSpy = jest.spyOn(globalThis, 'fetch').mockImplementation(((url: unknown, init?: unknown) =>
      String(url).startsWith(baseUrl) ? clientFetch(url as string, init as RequestInit) : Promise.reject(new Error('ks1868 anchoring stand-in: unreachable'))) as typeof fetch);
    mockGetCertification.mockResolvedValueOnce({ id: CERT_ID, type: 'professional_certification', status: 'certified', issuer: { id: issuerId }, holder: { id: 'ks1868-holder' }, data: { title: 'ks1868' } });
    mockSaveCertification.mockImplementationOnce(async (cert: any) => {
      stored.type = cert.type;
      throw thrown;
    });
    try {
      const res = await fetch(`${baseUrl}/api/certifications/${CERT_ID}/recertify`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ note: 'ks1868' }),
        signal: AbortSignal.timeout(2500),
      });
      return { status: res.status, body: await res.json(), storedType: stored.type };
    } catch {
      return { status: 'NO ANSWER', storedType: stored.type };
    } finally {
      fetchSpy.mockRestore();
    }
  }
  const r = ROUTES[0];

  it(`control ks1868 C4 ${r.route} after the write: an ordinary Error answers the constant 500 and the verification certificate is stored`, async () => {
    useRealLogger();
    expect(await recertifyThenFail(new Error('ks1868 ordinary'))).toEqual({ status: 500, body: r.constant, storedType: 'verification_certificate' });
    expect(mockLog.error.mock.calls).toEqual([[r.context, { error: 'ks1868 ordinary' }]]);
  });

  it(`RED ks1868 R5 ${r.route} after the write: a message getter returning a revoked Proxy answers the constant 500 and the stored state is the ordinary one`, async () => {
    useRealLogger();
    expect(await recertifyThenFail(messageGetterReturningRevokedProxy())).toEqual({ status: 500, body: r.constant, storedType: 'verification_certificate' });
    expect(mockLog.error.mock.calls).toEqual([[r.context, { error: UNREADABLE }]]);
  });

  it(`RED ks1868 R6 ${r.route} after the write: a message getter returning an object with a throwing toJSON answers the constant 500 and the stored state is the ordinary one`, async () => {
    useRealLogger();
    expect(await recertifyThenFail(messageGetterReturningThrowingToJson())).toEqual({ status: 500, body: r.constant, storedType: 'verification_certificate' });
    expect(mockLog.error.mock.calls).toEqual([[r.context, { error: '[object Object]' }]]);
  });
});
