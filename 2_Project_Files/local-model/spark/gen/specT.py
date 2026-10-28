P='Blockchain/Dev/services/auth/src/routes/internal.ts'
TP='Blockchain/Dev/services/auth/src/__tests__/ks1240-connector-token-security-validate-fetch-is-bounded.test.ts'
E1=("const SECURITY_SERVICE_URL = process.env.SECURITY_SERVICE_URL || 'http://security:4008';\n",
"""const SECURITY_SERVICE_URL = process.env.SECURITY_SERVICE_URL || 'http://security:4008';

// KS-1240 (class): the longest the connector-token exchange waits for the security service's key validation. The fetch carried no timeout, so a security service that accepted the connection and never
// answered held the gateway's exchange for as long as the socket lived. On expiry the fetch rejects into the route's existing catch, which answers the 502 it already gives an unreachable service.
const SECURITY_VALIDATE_FETCH_TIMEOUT_MS = 10_000;
""")
E2=("      body: JSON.stringify({ key: parsed.data.apiKey }),\n    });","      body: JSON.stringify({ key: parsed.data.apiKey }),\n      signal: AbortSignal.timeout(SECURITY_VALIDATE_FETCH_TIMEOUT_MS),\n    });")
TEST='''// KS-1240 (class: hand-built outbound fetches with no timeout), services/auth routes/internal.ts, POST /internal/connector-token: the route validates the presented sk_ key with a fetch to the security
// service and carried no `signal`, so a security service that accepted the connection and never answered held the gateway's token exchange open for as long as the socket lived. The real router runs on a
// loopback listener; the global fetch is wrapped so calls to the listener go through and calls to the security service are stubbed (and honour `init.signal`; with no signal they never answer). R1 pins that
// the security call carries an AbortSignal, R2 that the bound is sane, R3 that a silent security service ends in the route's existing 502 and not a hang; C1 to C4 pin the unchanged answers.
import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
import type { Server } from 'node:http';
import express from 'express';

const silent = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() }));
vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));
vi.mock('../services/jwt', () => ({ generateConnectorToken: vi.fn(() => ({ token: 'connector-jwt', expiresIn: 300 })) }));

import { internalRoutes } from '../routes/internal';

const realFetch = globalThis.fetch;
const API_KEY = 'sk_' + 'a'.repeat(24);

let server: Server;
let base = '';

beforeAll(async () => {
  const app = express();
  app.use(express.json());
  app.use('/internal', internalRoutes);
  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });
  const addr = server.address();
  base = 'http://127.0.0.1:' + (typeof addr === 'object' && addr ? addr.port : 0);
});
afterAll(() => { (server as Server & { closeAllConnections?: () => void })?.closeAllConnections?.(); server?.close(); });
afterEach(() => { vi.restoreAllMocks(); globalThis.fetch = realFetch; });

function jsonReply(status: number, body: unknown): Response {
  return { ok: status >= 200 && status < 300, status, json: async () => body, text: async () => JSON.stringify(body) } as unknown as Response;
}

/** Wraps fetch: the loopback listener is called for real, the security service is answered by `security`. */
function stubSecurity(security: (init?: { signal?: AbortSignal }) => Promise<Response>, seen: unknown[] = []): void {
  globalThis.fetch = ((url: unknown, init?: { signal?: AbortSignal }) => {
    if (String(url).startsWith(base)) return realFetch(url as string, init as RequestInit);
    seen.push(init?.signal);
    return security(init);
  }) as typeof fetch;
}

const VALID = { data: { valid: true, organizationId: 'org-1', tenantId: 'tenant-1', scopes: ['documents:read'], connectorId: 'conn-1' } };

/** Honours the signal; with NO signal it never answers (the hang the fix removes). */
function neverAnswers(init?: { signal?: AbortSignal }): Promise<Response> {
  return new Promise<Response>((_resolve, reject) => {
    const signal = init?.signal;
    if (!signal) return;
    if (signal.aborted) reject(new Error('aborted'));
    else signal.addEventListener('abort', () => reject(new Error('aborted')));
  });
}

/** The route's status, or 'HUNG' when nothing has answered after 300 ms, so a hang is a red assertion and not a stuck run. */
async function exchange(body: unknown = { apiKey: API_KEY }): Promise<number | 'HUNG'> {
  return Promise.race([
    realFetch(base + '/internal/connector-token', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then((r) => r.status),
    new Promise<'HUNG'>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
  ]);
}

describe('KS-1240: the connector-token exchange bounds its security-service fetch', () => {
  it('RED KS-1240 R1 the key-validation fetch carries an AbortSignal', async () => {
    const seen: unknown[] = [];
    stubSecurity(async () => jsonReply(200, VALID), seen);
    expect(await exchange()).toBe(200);
    expect(seen).toHaveLength(1);
    expect(seen[0]).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R2 the bound handed to AbortSignal.timeout is positive and at most 30000 ms', async () => {
    const timeout = vi.spyOn(AbortSignal, 'timeout');
    stubSecurity(async () => jsonReply(200, VALID));
    expect(await exchange()).toBe(200);
    const bounds = timeout.mock.calls.map((c) => c[0] as number);
    expect(bounds).toHaveLength(1);
    expect(bounds[0]).toBeGreaterThan(0);
    expect(bounds[0]).toBeLessThanOrEqual(30000);
  });

  it('RED KS-1240 R3 a security service that never answers ends in the 502, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubSecurity(neverAnswers);
    expect(await exchange()).toBe(502);
  });

  it('control KS-1240 C1 a valid key still gets its connector token', async () => {
    stubSecurity(async () => jsonReply(200, VALID));
    const res = await realFetch(base + '/internal/connector-token', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ apiKey: API_KEY }) });
    expect(res.status).toBe(200);
    expect(((await res.json()) as { data: { token: string } }).data.token).toBe('connector-jwt');
  });

  it('control KS-1240 C2 an invalid key is still refused with 401', async () => {
    stubSecurity(async () => jsonReply(200, { data: { valid: false } }));
    expect(await exchange()).toBe(401);
  });

  it('control KS-1240 C3 a non-2xx answer from security is still a 502', async () => {
    stubSecurity(async () => jsonReply(500, {}));
    expect(await exchange()).toBe(502);
  });

  it('control KS-1240 C4 an unreachable security service is still a 502, and a malformed key is still a 400', async () => {
    stubSecurity(async () => { throw new Error('connect ECONNREFUSED'); });
    expect(await exchange()).toBe(502);
    expect(await exchange({ apiKey: 'not-a-key' })).toBe(400);
  });
});
'''
S=dict(dir='ks_1240_p9_internal_loose',ticket='KS-1240',
 title='(class, slice 9, LOOSE) auth routes/internal.ts: the connector-token route fetches the security service with no timeout; the product edit is described by behaviour only, the test is given whole (RUNG 4, code_patch: the model writes the product lines)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 4 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Slice 9 of the KS-1240 class (hand-built fetch with no timeout), and the LOOSE one: the first looser brief of today. KS-1240 is the gateway ticket and applying it to services/auth is the drafter's extension, stated: the raise seat confirms the scope with the owner. The product edit is NOT dictated line by line (no diff, no `+` lines): the brief states the shape and the contract and the model writes the lines; the new test is given whole and the verdict is the checker's A4-A7 (the golden is ONE correct answer for Wednesday's source read: expect `golden DIFFERS` on a correct, differently worded patch). The question this brief asks: with the shape stated and the lines not dictated, does the Spark produce a minimal edit that the tests accept? This is the counterpart, in services/auth, of the gateway's getConnectorBearer (slice 1). The Spark may fail this one (capability data).",
 products=[(P,[E1,E2])],
 prodnote=['product, modified in place: you write the lines (a constant near `SECURITY_SERVICE_URL`, and a `signal` on the one fetch)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 7 cells (3 red, 4 control; real router on a loopback listener, security service stubbed)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-connector-token-security-validate-fetch-is-bounded.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch', rung='4', rung_raw="**4** (a LOOSER brief: one product file and one site, but the product `+` lines are NOT given - the brief states the fix shape and the contract, and the model writes the code. The test is given whole.)",
 pins='''# code_patch (auth vitest), RUNG 4 (looser brief: no product fence; the model writes the product lines).
# ref = the ks728 loopback spec (shape only); line = the fetch site (internal.ts:43). golden.diff is ONE correct answer: expect `golden DIFFERS` on a correct differently-worded patch; the verdict is A4-A7.
tier=code_patch
ref=Blockchain/Dev/services/auth/src/__tests__/ks728-social-link-responds.test.ts
line=43
ctx=65536
''',
 wrong="`POST /internal/connector-token` in `services/auth/src/routes/internal.ts` validates the presented `sk_` key by `await fetch(`${SECURITY_SERVICE_URL}/api/keys/validate`, {...})` (one fetch, `:43`) with no `signal`. A security service that accepts the connection and never answers holds the gateway's token exchange open for as long as the socket lives. The route's body is already in a `try` whose `catch` logs `connector-token exchange failed` and answers `502 BAD_GATEWAY` with the constant body `Key validation unavailable`, so a timeout needs no new handling.",
 where="- `routes/internal.ts:43` - **must change**: the `fetch(` call to `${SECURITY_SERVICE_URL}/api/keys/validate` inside the `try` of the connector-token handler gains a timeout signal.\n- The `SECURITY_SERVICE_URL` const (line 21) is the place for the new named constant.\n- Every other line of the file, including the catch, the 401 and 502 bodies, and the token minting, is NOT touched.",
 exactnote="",
 loose="The required shape, all of it:\n\n1. Add ONE module-level named constant for the bound, directly below the `SECURITY_SERVICE_URL` const (with a short comment saying what it bounds and what happens on expiry), equal to ten seconds written as `10_000`.\n2. Add ONE property `signal: AbortSignal.timeout(<that constant>),` as the LAST property of the init object of the `fetch(` to `${SECURITY_SERVICE_URL}/api/keys/validate` (after the `body: JSON.stringify({ key: parsed.data.apiKey }),` line).\n3. Change nothing else: not the catch, not the status codes or bodies, not the imports (no new import is needed: `AbortSignal` is a global).",
 donot="**Do NOT touch** the catch block, the 401 / 502 / 400 bodies, `generateConnectorToken`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It mocks the logger (hoisted) and `../services/jwt`, runs the real router on a loopback listener, wraps the global `fetch` so calls to the listener are real and calls to the security service are stubbed, and spies on `AbortSignal.timeout`.",
 red=['RED KS-1240 R1','RED KS-1240 R2','RED KS-1240 R3'],
 cells="- RED `R1`: at the tip the security fetch carries no `init.signal`, so `toBeInstanceOf(AbortSignal)` fails; after the edit it does.\n- RED `R2`: at the tip `AbortSignal.timeout` is never called (0 bounds, not 1); after the edit one bound, positive and at most 30000.\n- RED `R3`: `AbortSignal.timeout` returns an already-aborted signal and the stub honours it; at the tip no signal is passed, the stub never answers and the exchange reads `HUNG` after 300 ms; after the edit the existing catch answers 502.\n- CONTROL `C1` to `C4`: green at the tip AND after (valid key gets its token; invalid key 401; non-2xx 502; unreachable 502 and a malformed key 400).",
 premises="- `routes/internal.ts` line 21 is the `SECURITY_SERVICE_URL` const; the one `fetch(` is at :43 and its init object ends with `body: JSON.stringify({ key: parsed.data.apiKey }),` then `    });` (read from the cache clone at the tip); the handler's `catch` is at the end of the route and answers 502 `Key validation unavailable`.\n- `generateConnectorToken` is imported from `../services/jwt` (mocked by the test).\n- The service's test runner is vitest. The golden is generated by script and is one correct answer, not the only one.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 10000 ms is the right bound: the value is the drafter's; the raise seat confirms with the owner. A signal also bounds reading the response body.\n- Because the product lines are not dictated, byte-identity to the golden is NOT expected; the checker's red-to-green and whole-suite checks are the verdict.\n- Open PRs touching this file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Slice 9 of the KS-1240 class (auth connector-token route), loose.** Link the PR as Refs KS-1240, never a close-word.",
)
