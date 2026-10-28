import re
P='Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts'
HELPERS='''/**
 * KS-1780: a catch that tests `err?.message?.includes(...)` or `err?.code` BEFORE it reaches fail500 reads the thrown value itself. A revoked Proxy, or an object whose `message` getter throws,
 * makes THAT read throw from inside the catch, so the handler's promise rejects and the request gets no response at all (the KS-1772 shape, one step earlier). These two readers answer false
 * when the value cannot be inspected: such a value is not a "table missing" or "unique constraint" error, so it falls through to fail500 and gets the constant 500.
 */
function errorMessageIncludes(err: any, needle: string): boolean {
  try {
    return err?.message?.includes(needle) === true;
  } catch {
    return false;
  }
}

function isMissingTableError(err: any): boolean {
  try {
    return err?.message?.includes('does not exist') === true || err?.code === '42P01';
  } catch {
    return false;
  }
}

'''
def ins(c):
    a="adminConfigRouter.post('/refresh-tenants', async"
    assert c.count(a)==1
    return c.replace(a,HELPERS+a)
def sites(c):
    old="    if (err?.message?.includes('does not exist') || err?.code === '42P01') {"
    assert c.count(old)==13
    c=c.replace(old,"    if (isMissingTableError(err)) {")
    o2="    if (err?.message?.includes('unique constraint')) {"; assert c.count(o2)==1
    c=c.replace(o2,"    if (errorMessageIncludes(err, 'unique constraint')) {")
    o3="    if (err?.message?.includes('does not exist')) {"; assert c.count(o3)==1
    c=c.replace(o3,"    if (errorMessageIncludes(err, 'does not exist')) {")
    return c
TEST='''// KS-1780 (originate routes/adminConfig.ts): fifteen catch blocks tested `err?.message?.includes(...)` and/or `err?.code` BEFORE they reached fail500. That read touches the thrown value
// itself, so a revoked Proxy, or an object whose `message` getter throws, made the read throw inside the catch: the handler's promise rejected and the request got NO answer. fail500
// already survives such a value (KS-1772); this file pins that the catches' own reads do too. Four GET routes are driven over a real loopback listener by making their prisma.$queryRaw
// reject, as the KS-1346 part C cells do; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.
// S1 pins the source: no `if (err?.message` / `if (err?.code` condition may remain in the file.
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: jest.fn() },
  refreshTenantConfigs: jest.fn(),
  withTenant: (_t: unknown, fn: () => unknown) => fn(),
  getTenantManager: () => null,
}));

jest.mock('../middleware/auth', () => {
  const actual = jest.requireActual('../middleware/auth');
  return {
    ...actual,
    authenticate: () => (req: any, _res: unknown, next: () => void) => {
      const principal = { id: 'u-ks1780', role: 'SYSTEM_ADMIN', tenantId: 't-ks1780' };
      req._secuuraUser = principal; req.user = principal; req.tenantId = principal.tenantId;
      next();
    },
    requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  };
});

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
    runWithPlatformScope: (fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import { readFileSync } from 'fs';
import { join } from 'path';
import express from 'express';
import type { AddressInfo } from 'net';
import { adminConfigRouter } from '../routes/adminConfig';

const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ROUTES = [
  { label: 'GET /settings', path: '/settings', empty: { success: true, settings: {} } },
  { label: 'GET /document-types', path: '/document-types', empty: { success: true, documentTypes: [] } },
  { label: 'GET /workflows', path: '/workflows', empty: { success: true, workflows: [] } },
  { label: 'GET /organizations', path: '/organizations', empty: { success: true, organizations: [], total: 0 } },
] as const;

const app = express();
app.use('/api/admin', express.json(), adminConfigRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  (server as unknown as { closeAllConnections?: () => void })?.closeAllConnections?.();
  server?.close();
});
beforeEach(() => mockQueryRaw.mockReset());

async function callWithThrow(path: string, thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
  mockQueryRaw.mockRejectedValueOnce(thrown);
  try {
    const res = await fetch(baseUrl + '/api/admin' + path, { signal: AbortSignal.timeout(1500) });
    return { status: res.status, body: await res.json() };
  } catch {
    return { status: 'NO ANSWER', body: null };
  }
}

function revokedProxy(): object {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
}

function throwingMessageGetter(): object {
  return {
    get message(): string {
      throw new Error('ks1780 getter');
    },
  };
}

describe('KS-1780: adminConfig catches answer a hostile thrown value', () => {
  it.each(ROUTES)('RED KS-1780 A1 $label: a revoked Proxy thrown by the query is answered with the constant 500', async (route) => {
    expect(await callWithThrow(route.path, revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
  });

  it.each(ROUTES)('RED KS-1780 A2 $label: an object whose message getter throws is answered with the constant 500', async (route) => {
    expect(await callWithThrow(route.path, throwingMessageGetter())).toEqual({ status: 500, body: CONSTANT_BODY });
  });

  it.each(ROUTES)('control KS-1780 C1 $label: an Error saying "does not exist" is still answered with the empty list', async (route) => {
    expect(await callWithThrow(route.path, new Error('relation "x" does not exist'))).toEqual({ status: 200, body: route.empty });
  });

  it.each(ROUTES)('control KS-1780 C2 $label: a thrown object with code 42P01 is still answered with the empty list', async (route) => {
    expect(await callWithThrow(route.path, { code: '42P01' })).toEqual({ status: 200, body: route.empty });
  });

  it.each(ROUTES)('control KS-1780 C3 $label: an ordinary Error is still answered with the constant 500', async (route) => {
    expect(await callWithThrow(route.path, new Error('ks1780 ordinary'))).toEqual({ status: 500, body: CONSTANT_BODY });
  });

  it('RED KS-1780 S1: no catch condition in adminConfig.ts reads err?.message or err?.code directly', () => {
    const source = readFileSync(join(__dirname, '..', 'routes', 'adminConfig.ts'), 'utf8');
    const direct = source.split('\\n').filter((line) => /^\\s*if \\(err\\?\\.(message|code)/.test(line));
    expect(direct).toEqual([]);
  });
});
'''
S=dict(dir='ks_1780_p2_admin',ticket='KS-1780',
 title='(adminConfig.ts sites) originate: 15 catches read the thrown value before fail500, so a revoked Proxy or a throwing message getter gets no response; read it inside a try (RUNG 3, code_patch: ONE product file with 16 hunks - 2 helpers + 15 replaced condition lines - and one NEW jest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 2 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. This brief takes the 15 `adminConfig.ts` sites of KS-1780 (batch 1 took `systemErrors.ts:196`; `webhooks.ts:320` is a separate brief). It is a MULTI-SITE brief: the Spark may fail it (it is a capability measurement).",
 products=[(P,[ins,sites])],
 prodnote=['product, modified in place: 16 hunks - two helper functions INSERTED before the first route, then 15 single-line replacements'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, 124 lines, given in full below; 21 cells (9 red at the tip)'],
 runner='jest` (`npx jest src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch',
 rung='3 in effect (one file but 16 hunks given byte-exact: does the Spark replace 15 near-identical lines without dropping or mutating one?)',
 pins='''# code_patch, ONE product file, 16 hunks (helpers + 15 call sites) + a NEW loopback jest (test_file NOT pinned: it would mean MODIFY); ref = the ks1346c loopback spec (shape only); line = the first changed line at the tip.
tier=code_patch
ref=Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts
line=127
ctx=65536
''',
 wrong="In `routes/adminConfig.ts` fifteen `catch (err: any)` blocks read the thrown value before they reach `fail500`: thirteen open with `if (err?.message?.includes('does not exist') || err?.code === '42P01') {` (an empty-list answer when a table is missing), one reads `err?.message?.includes('unique constraint')` (`:227`, a 409), one reads `err?.message?.includes('does not exist')` (`:1568`, no code test). If the thrown value is a revoked Proxy, or an object whose `message` getter throws, THAT read throws from inside the catch, before `fail500` is reached; the async handler's promise rejects and the request gets NO response (the shape KS-1772 closed for the describer, one step earlier; Gate B measured it on `systemErrors.ts:196`, not on these sites). The change adds two small helpers that do the read inside their own `try` and answer false when it throws, and the fifteen conditions call them. A value that cannot be inspected is not a missing-table or unique-constraint error, so it falls through to `fail500` and gets the constant 500. Every value that could be read before gives the same answer as before.",
 where="- Directly above `adminConfigRouter.post('/refresh-tenants', async (_req: Request, res: Response) => {` (`:128`), after `fail500`'s closing `}` and one blank line - **must change**: the doc comment and the two functions `errorMessageIncludes` and `isMissingTableError` are INSERTED (followed by one blank line); nothing else moves.\n- The thirteen lines `    if (err?.message?.includes('does not exist') || err?.code === '42P01') {` (at the tip `:191 :291 :380 :435 :523 :704 :820 :935 :1228 :1391 :1660 :1697 :1725`) - **must change**: each becomes `    if (isMissingTableError(err)) {`.\n- `:227` `    if (err?.message?.includes('unique constraint')) {` becomes `    if (errorMessageIncludes(err, 'unique constraint')) {`; `:1568` `    if (err?.message?.includes('does not exist')) {` becomes `    if (errorMessageIncludes(err, 'does not exist')) {` - **must change**.\n- Every other line, including `fail500` (`:110`), the other catches that go straight to `fail500`, and the log read at `:2091` (`error: err?.message`), is (correct) and is NOT touched. The line numbers above are the tip's; the hunks below carry them.",
 exactnote="Sixteen hunks in one file, in file order. `err` is `any` in every catch, so the helper arguments type-check.\n",
 donot="**Do NOT touch** `fail500`, any other catch, any other file, or the `:2091` log line.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. It mirrors the loopback pattern of the neighbouring `ks1346c` spec (mocks of the db, the auth middleware, shared and the logger; an express app on port 0; `fetch`). A request that gets no answer in 1500 ms is reported as the string `NO ANSWER`, so the red state is an assertion, not a stuck run. Pure ASCII. Jest globals without import.",
 red=['RED KS-1780 A1','RED KS-1780 A2','RED KS-1780 S1'],
 cells="- RED `A1` (4 rows, one per route) revoked Proxy; RED `A2` (4 rows) throwing message getter: at the tip the catch's read throws, the request gets no answer, the cell reads `{ status: 'NO ANSWER', body: null }`; after the edit both give the constant 500.\n- RED `S1`: at the tip fifteen lines match `/^\\s*if \\(err\\?\\.(message|code)/`; after, none.\n- CONTROL `C1` (an Error saying 'does not exist' still gets the empty list), `C2` (`{ code: '42P01' }` likewise), `C3` (a plain Error still gets the constant 500): 12 rows, green at the tip AND after.",
 premises="- The thirteen identical lines, `:227` and `:1568` were read with `git show 8894c7486f82:Blockchain/Dev/services/originate/src/routes/adminConfig.ts`; `err?.message?.includes('does not exist') || err?.code === '42P01'` occurs 13 times, `unique constraint` once, `err?.message?.includes('does not exist')` without the code test once.\n- The four routes the test drives (`GET /settings`, `/document-types`, `/workflows`, `/organizations`) are the ones the existing ks1346c spec drives by making `prisma.$queryRaw` reject; their missing-table answers are `{ success: true, settings: {} }`, `documentTypes: []`, `workflows: []`, `organizations: [], total: 0`.\n- The package test runner is jest; the golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether a revoked Proxy or a throwing getter can reach these catches from a real prisma call: not established (the ticket says the values are Gate B's choosing; only the systemErrors site was driven).\n- Only four of the fifteen sites are driven by a loopback cell; the other eleven are pinned by S1's source text only.\n- Open PRs touching the product or test file: none by the file lists of every open PR read on 2026-10-28 (#1772 originate `routes/anchors.ts`; #1773 api-gateway openapi; #1756 api-gateway and bootstrap files; dependency bumps; docs). The batch-1 brief `ks_1779_p1` edits the same product file at `:2181`/`:2221`: different hunks, far apart; the raise seat merges them separately.",
 scope="**Closes the adminConfig.ts sites of KS-1780** (15 of the ticket's 17; `systemErrors.ts:196` is batch 1's `ks_1780_p1`, `webhooks.ts:320` is `ks_1780_p3`). Link the PR as Refs KS-1780, never a close-word.",
)
