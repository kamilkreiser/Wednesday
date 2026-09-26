// KS-730 part B (originate routes/gdpr.ts): fifteen inline handlers returned `err.message` verbatim
// unless NODE_ENV === 'production', so development, demo, test and an UNSET NODE_ENV all answered a
// GDPR route — consent, DSRs, exports, erasure, retention, the deletion log — with raw internal text.
// The KS-727 doctrine, applied to the per-route remainder KS-727 enumerated rather than folded in.
//
// TWO KINDS OF CELL, and the difference is stated rather than blurred:
//   * BEHAVIOURAL cells drive four routes end to end over a loopback listener and read the real 500
//     body and the real log call. They are the strong evidence, and they cover four of fifteen.
//   * A SOURCE cell pins all fifteen by construction: zero live ternary sites, fifteen fail500 call
//     sites. It is weaker — it reads the file rather than the behaviour — and it exists because
//     driving fifteen routes would need fifteen service mocks for no additional discrimination.
const mockGetPendingDSRs = jest.fn();
const mockGetRetentionPolicies = jest.fn();
const mockGetDeletionLog = jest.fn();
const mockHasValidConsent = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../services/gdprService', () => ({
  getPendingDSRs: mockGetPendingDSRs,
  getRetentionPolicies: mockGetRetentionPolicies,
  getDeletionLog: mockGetDeletionLog,
  hasValidConsent: mockHasValidConsent,
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  hasAnyRole: () => true,
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { gdprRouter } from '../routes/gdpr';
import { readFileSync } from 'fs';
import path from 'path';

const LEAK = 'relation gdpr_consent does not exist ks730b-private-detail';
const NODE_ENVS = ['development', 'demo', 'test', undefined];
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;

const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  if (ORIGINAL_NODE_ENV === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = ORIGINAL_NODE_ENV;
  server?.close();
});
beforeEach(() => jest.clearAllMocks());

function setNodeEnv(v: string | undefined): void {
  if (v === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = v;
}

// FOUR ROUTES CHOSEN SO THE THROW IS WHAT THE CELL MEASURES. My first set used POST /consent and
// PATCH /dsr/:dsrId, whose bodies must satisfy a zod schema and a UUID check BEFORE the service is
// called — my fixtures did not, so each was refused 400 and the service never threw. The cells were
// measuring my own fixtures rather than the handler. These four reach their service with nothing to
// satisfy first (verified at source), and each is driven by making ITS OWN service call throw, so a
// cell cannot pass because a different handler answered.
const ROUTES = [
  { label: 'GET /dsr/pending', method: 'GET', path: '/dsr/pending', body: undefined, mock: mockGetPendingDSRs, context: 'GDPR pending DSR list failed (GET /api/gdpr/dsr/pending)' },
  { label: 'GET /retention', method: 'GET', path: '/retention', body: undefined, mock: mockGetRetentionPolicies, context: 'GDPR retention policy read failed (GET /api/gdpr/retention)' },
  { label: 'GET /deletion-log', method: 'GET', path: '/deletion-log', body: undefined, mock: mockGetDeletionLog, context: 'GDPR deletion log read failed (GET /api/gdpr/deletion-log)' },
  { label: 'GET /consent/check', method: 'GET', path: '/consent/check?userId=u-ks730b&purpose=MARKETING', body: undefined, mock: mockHasValidConsent, context: 'GDPR consent check failed (GET /api/gdpr/consent/check)' },
] as const;

async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined, throwInService: boolean): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  if (throwInService) route.mock.mockRejectedValueOnce(new Error(LEAK));
  else route.mock.mockResolvedValueOnce([]);
  const res = await fetch(baseUrl + '/api/gdpr' + route.path, {
    method: route.method,
    headers: { 'content-type': 'application/json' },
    ...(route.body === undefined ? {} : { body: JSON.stringify(route.body) }),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-730 part B: the GDPR routes never answer a 500 with err.message', () => {
  it.each(ROUTES)('RED KS-730 B1 $label: the thrown message is not in the 500 body under development, demo, test or unset', async (route) => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await call(route, nodeEnv, true);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
    }
  });

  it.each(ROUTES)('RED KS-730 B2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await call(route, 'development', true);
    expect(reply.status).toBe(500);
    // The context is asserted as a VALUE: a helper logging one constant string would satisfy a looser
    // check and make every route's log indistinguishable from every other's.
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('KS-730 B3 SOURCE: all fifteen sites are routed through the helper — zero ternaries left', () => {
    // Weaker than the behavioural cells above, and deliberately so: it reads the file rather than the
    // behaviour, and it is what covers the eleven routes not driven here. Stated as a source pin.
    const src = readFileSync(path.join(__dirname, '..', 'routes', 'gdpr.ts'), 'utf8');
    const lines = src.split('\n');
    const liveTernaries = lines.filter(
      (l) => l.includes("NODE_ENV === 'production'") && !l.trim().startsWith('*') && !l.trim().startsWith('//') && !l.includes('logger.'),
    );
    const helperCalls = lines.filter((l) => l.includes('fail500(res,'));
    expect({ liveTernaries: liveTernaries.length, helperCalls: helperCalls.length })
      .toEqual({ liveTernaries: 0, helperCalls: 15 });
    // and every helper call carries a DISTINCT context, so no two routes log the same line
    const contexts = helperCalls.map((l) => (l.match(/fail500\(res, '([^']+)'/) ?? [])[1]);
    expect(new Set(contexts).size).toBe(15);
  });

  it('control KS-730 B: under production these routes already answered the constant text', async () => {
    for (const route of ROUTES) {
      const reply = await call(route, 'production', true);
      expect({ label: route.label, status: reply.status, body: JSON.parse(reply.text) })
        .toEqual({ label: route.label, status: 500, body: CONSTANT_BODY });
    }
  });

  it('control KS-730 B: a typed CLIENT error keeps its own authored text and logs nothing', async () => {
    // The risk of a blanket helper is that it swallows messages a route MEANT to return.
    setNodeEnv('development');
    // GET /consent/check without its required query params: a 400 the route authors itself.
    const res = await fetch(baseUrl + '/api/gdpr/consent/check');
    const text = await res.text();
    expect(res.status).toBeGreaterThanOrEqual(400);
    expect(res.status).toBeLessThan(500);
    expect(text).not.toContain('Internal server error');
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-730 B: the LEAK string really is the thrown text, so "not leaked" is not vacuous', () => {
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
  });
});
