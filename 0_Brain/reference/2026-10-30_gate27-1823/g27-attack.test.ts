/**
 * QA gate 27 attack cells (not part of the PR). Copied into a worktree's originate/src/__tests__ only.
 * Every cell records { status, code, calls, bodySuccess } into a table written to G27_OUT, so the same
 * file run at base, head and develop gives a comparable table; assertions encode the HEAD expectation.
 */
import * as fs from 'fs';

const mockRecordConsent = jest.fn();
const mockCreateDSR = jest.fn();

jest.mock('../services/gdprService', () => ({
  recordConsent: mockRecordConsent,
  createDSR: mockCreateDSR,
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  hasAnyRole: () => true,
}));

import express from 'express';
import { gdprRouter } from '../routes/gdpr';

const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);
let baseUrl = '';
let server: ReturnType<typeof app.listen>;
const table: Record<string, unknown> = {};

beforeAll(async () => {
  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
  const a = server.address();
  baseUrl = `http://127.0.0.1:${typeof a === 'object' && a ? a.port : 0}`;
});
afterAll(() => {
  server?.close();
  if (process.env.G27_OUT) fs.writeFileSync(process.env.G27_OUT, JSON.stringify(table, null, 1));
});
beforeEach(() => jest.clearAllMocks());

const USER_ID = '11111111-2222-4333-8444-555555555555';
const bodies: Record<string, unknown> = {
  dsr: { type: 'erasure', userId: USER_ID, email: 'subject@example.com' },
  consent: { userId: USER_ID, purpose: 'marketing' },
};
const mocks: Record<string, jest.Mock> = { dsr: mockCreateDSR, consent: mockRecordConsent };

type Row = { status: number | string; code?: string; bodySuccess?: unknown; calls: number };
async function hit(route: 'dsr' | 'consent', outcome: { reject?: unknown; resolve?: unknown }): Promise<Row> {
  const m = mocks[route];
  if ('resolve' in outcome) m.mockResolvedValueOnce(outcome.resolve);
  else m.mockRejectedValueOnce(outcome.reject);
  try {
    const res = await fetch(`${baseUrl}/api/gdpr/${route}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(bodies[route]),
      signal: AbortSignal.timeout(1500),
    });
    let j: any = undefined;
    try { j = await res.json(); } catch { j = 'unparsable'; }
    return { status: res.status, code: j?.error?.code, bodySuccess: j?.success, calls: m.mock.calls.length };
  } catch {
    return { status: 'NO ANSWER', calls: m.mock.calls.length };
  }
}

const throwAllProxy = () => new Proxy({}, { get() { throw new Error('g27 get trap'); }, getPrototypeOf() { throw new Error('g27 proto trap'); }, ownKeys() { throw new Error('g27 keys trap'); } });
const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const pgCodeGetterThrows = (extra: Record<string, unknown> = {}) =>
  Object.defineProperty(Object.assign(new Error('g27 pgCode getter'), extra), 'pgCode', { get() { throw new Error('g27 pgCode threw'); } });
const proxyThrowsOnlyPgCode = (code: string) =>
  new Proxy(Object.assign(new Error('g27 selective'), { code }), { get(t, k, r) { if (k === 'pgCode') throw new Error('g27 pgCode trap'); return Reflect.get(t, k, r); } });
const tagged = (pgCode: string) => Object.assign(new Error('Failed to create data subject request'), { pgCode });
const barePg = (code: string) => Object.assign(new Error(`duplicate key value violates unique constraint (${code})`), { code, severity: 'ERROR', detail: 'Key exists' });
const prismaWrapped = (code: string) => Object.assign(new Error('Raw query failed.'), { code: 'P2010', meta: { code } });
let pgCodeReads = 0;
const countingPgCode = (v: string | undefined) => Object.defineProperty(new Error('g27 counting'), 'pgCode', { get() { pgCodeReads += 1; return v; } });

// name -> [factory, expected HEAD status, expected error.code]
const cases: Array<[string, () => { reject?: unknown; resolve?: unknown }, number, string | undefined]> = [
  ['success resolve', () => ({ resolve: { id: 'x-1' } }), 201, undefined],
  ['throw-all Proxy', () => ({ reject: throwAllProxy() }), 500, 'INTERNAL_ERROR'],
  ['revoked Proxy', () => ({ reject: revoked() }), 500, 'INTERNAL_ERROR'],
  ['pgCode getter throws', () => ({ reject: pgCodeGetterThrows() }), 500, 'INTERNAL_ERROR'],
  ['pgCode getter throws + code 23503', () => ({ reject: pgCodeGetterThrows({ code: '23503' }) }), 404, 'NOT_FOUND'],
  ['pgCode getter throws + code 23505', () => ({ reject: pgCodeGetterThrows({ code: '23505' }) }), 500, 'INTERNAL_ERROR'],
  ['Proxy throws only on pgCode, code 22001', () => ({ reject: proxyThrowsOnlyPgCode('22001') }), 400, 'VALIDATION_ERROR'],
  ['plain Error', () => ({ reject: new Error('plain') }), 500, 'INTERNAL_ERROR'],
  ['thrown null', () => ({ reject: null }), 500, 'INTERNAL_ERROR'],
  ['thrown undefined', () => ({ reject: undefined }), 500, 'INTERNAL_ERROR'],
  ['thrown string 23503', () => ({ reject: 'boom 23503' }), 500, 'INTERNAL_ERROR'],
  ['bare pg 23505 unique', () => ({ reject: barePg('23505') }), 500, 'INTERNAL_ERROR'],
  ['bare pg 23503 FK', () => ({ reject: barePg('23503') }), 404, 'NOT_FOUND'],
  ['bare pg 23502 not-null', () => ({ reject: barePg('23502') }), 500, 'INTERNAL_ERROR'],
  ['tagged 23505', () => ({ reject: tagged('23505') }), 500, 'INTERNAL_ERROR'],
  ['tagged 23503', () => ({ reject: tagged('23503') }), 404, 'NOT_FOUND'],
  ['tagged 23502', () => ({ reject: tagged('23502') }), 500, 'INTERNAL_ERROR'],
  ['tagged 22001', () => ({ reject: tagged('22001') }), 400, 'VALIDATION_ERROR'],
  ['tagged 23514', () => ({ reject: tagged('23514') }), 400, 'VALIDATION_ERROR'],
  ['prisma 23503', () => ({ reject: prismaWrapped('23503') }), 404, 'NOT_FOUND'],
  ['prisma 23505', () => ({ reject: prismaWrapped('23505') }), 500, 'INTERNAL_ERROR'],
  ['tagged pgCode wins over code (pg 23505, code 23503)', () => ({ reject: Object.assign(tagged('23505'), { code: '23503' }) }), 500, 'INTERNAL_ERROR'],
];

for (const route of ['dsr', 'consent'] as const) {
  describe(`g27 ${route}`, () => {
    for (const [name, mk, st, code] of cases) {
      it(`${route}: ${name}`, async () => {
        const row = await hit(route, mk());
        table[`${route}: ${name}`] = row;
        expect(row.calls).toBe(1); // service invoked exactly once: no retry, no skip
        expect(row.status).toBe(st);
        if (code) { expect(row.code).toBe(code); expect(row.bodySuccess).toBe(false); }
        else expect(row.bodySuccess).toBe(true);
      });
    }
    it(`${route}: pgCode getter read exactly once`, async () => {
      pgCodeReads = 0;
      const row = await hit(route, { reject: countingPgCode('23503') });
      table[`${route}: counting getter 23503`] = { ...row, pgCodeReads };
      expect(row.status).toBe(404);
      expect(pgCodeReads).toBe(1);
    });
  });
}
