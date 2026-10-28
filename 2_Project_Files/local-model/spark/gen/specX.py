P='Blockchain/Dev/services/demo-service/src/services/authClient.ts'
TP='Blockchain/Dev/services/demo-service/src/__tests__/ks1240-demo-auth-client-login-fetch-is-bounded.test.ts'
SIG="signal: AbortSignal.timeout(AUTH_FETCH_TIMEOUT_MS),"
E1=("const AUTH_PORT = process.env.AUTH_PORT || '4003';\n",
"""const AUTH_PORT = process.env.AUTH_PORT || '4003';

// KS-1240: the longest the demo service waits for the auth service's login endpoint. The fetch carried no timeout, so an auth service that accepted the connection and never answered held the
// caller for as long as the socket lived. On expiry the fetch rejects and the existing catch answers { success: false, error } exactly as it already does for an unreachable service.
const AUTH_FETCH_TIMEOUT_MS = 10_000;
""")
E2=("      body: JSON.stringify({ email, password }),\n    });","      body: JSON.stringify({ email, password }),\n      "+SIG+"\n    });")
TEST='''// KS-1240 (class: hand-built outbound fetches with no timeout), demo-service services/authClient.ts: authenticatePersona fetched the auth service's login endpoint with no `signal`, so an auth service that
// accepted the connection and never answered held the caller for as long as the socket lived. The function already catches a failed fetch and answers { success: false, error }. It is driven directly with a
// stubbed global fetch that honours `init.signal` (and never answers when there is none); nothing touches the network. R1 pins that the fetch carries an AbortSignal, R2 that the bound is a sane positive
// number, R3 that a service that never answers ends in { success: false } and not a hang; C1 to C3 pin the unchanged answers.
import { describe, it, expect, afterEach, vi } from 'vitest';

const silent = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }));
vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent }));

import { authenticatePersona } from '../services/authClient';

function okReply(): Response {
  return {
    ok: true,
    status: 200,
    headers: { get: (name: string) => (name === 'set-cookie' ? 'refresh_token=abc; Path=/api/auth; HttpOnly' : null) },
    json: async () => ({ data: { accessToken: 'jwt-1', user: { id: 'u1' } } }),
  } as unknown as Response;
}

afterEach(() => { vi.restoreAllMocks(); });

/** The call's outcome, or 'HUNG' when it is still pending after 300 ms, so a hang is a red assertion and not a stuck run. */
async function outcome(): Promise<unknown> {
  return Promise.race([
    authenticatePersona('a@x.test', 'pw').then((r) => r, () => 'REJECTED'),
    new Promise<string>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
  ]);
}

describe('KS-1240: the demo-service auth client bounds its login fetch', () => {
  it('RED KS-1240 R1 the login fetch carries an AbortSignal', async () => {
    const seen: unknown[] = [];
    vi.spyOn(globalThis, 'fetch').mockImplementation((async (_url: unknown, init?: { signal?: unknown }) => { seen.push(init?.signal); return okReply(); }) as never);
    await authenticatePersona('a@x.test', 'pw');
    expect(seen).toHaveLength(1);
    expect(seen[0]).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R2 the bound handed to AbortSignal.timeout is positive and at most 30000 ms', async () => {
    const timeout = vi.spyOn(AbortSignal, 'timeout');
    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => okReply()) as never);
    await authenticatePersona('a@x.test', 'pw');
    const bounds = timeout.mock.calls.map((c) => c[0] as number);
    expect(bounds).toHaveLength(1);
    expect(bounds[0]).toBeGreaterThan(0);
    expect(bounds[0]).toBeLessThanOrEqual(30000);
  });

  it('RED KS-1240 R3 an auth service that never answers ends in { success: false }, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    vi.spyOn(globalThis, 'fetch').mockImplementation(((_url: unknown, init?: { signal?: AbortSignal }) =>
      new Promise<Response>((_resolve, reject) => {
        const signal = init?.signal;
        if (!signal) return;
        if (signal.aborted) reject(new Error('aborted'));
        else signal.addEventListener('abort', () => reject(new Error('aborted')));
      })) as never);
    const r = (await outcome()) as { success?: boolean };
    expect(r).not.toBe('HUNG');
    expect(r.success).toBe(false);
  });

  it('control KS-1240 C1 a healthy login still answers the token, the user and the cookie header', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => okReply()) as never);
    const r = await authenticatePersona('a@x.test', 'pw');
    expect([r.success, r.accessToken, r.setCookieHeader]).toEqual([true, 'jwt-1', 'refresh_token=abc; Path=/api/auth; HttpOnly']);
  });

  it('control KS-1240 C2 a refused login still answers { success: false, error: "Auth service returned 401" }', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => ({ ok: false, status: 401, headers: { get: () => null }, json: async () => ({}) })) as never);
    const r = await authenticatePersona('a@x.test', 'pw');
    expect([r.success, r.error]).toEqual([false, 'Auth service returned 401']);
  });

  it('control KS-1240 C3 an unreachable auth service still answers { success: false } with the error text', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => { throw new Error('connect ECONNREFUSED'); }) as never);
    const r = await authenticatePersona('a@x.test', 'pw');
    expect([r.success, r.error]).toEqual([false, 'connect ECONNREFUSED']);
  });
});
'''
S=dict(dir='ks_1240_p10_demo_auth',ticket='KS-1240',
 title='(class, slice 10) demo-service: authenticatePersona fetches the auth service login with no timeout; bound it with AbortSignal.timeout (RUNG 2, code_patch: two hunks in one product + one NEW behavioural vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 5 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Same class as the KS-1240 slices 1-8 (the gateway ticket); this is another service of the same shape. The 10 s bound is the drafter's, to be confirmed by the owner.",
 products=[(P,[E1,E2])],
 prodnote=['product, modified in place: TWO hunks (a constant block after the AUTH_PORT line, the signal line in the login fetch)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 6 cells (3 red, 3 control; behavioural, stubbed fetch)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-demo-auth-client-login-fetch-is-bounded.test.ts` from `Blockchain/Dev/services/demo-service',
 tier='code_patch', rung='2 (two hunks, byte-exact; the new test given whole)',
 pins='''# code_patch, 2 hunks in demo-service authClient.ts + a NEW vitest file; ref = authClient.test.ts (stubbed fetch, shape only); line = the first changed line (AUTH_PORT).
tier=code_patch
ref=Blockchain/Dev/services/demo-service/src/__tests__/authClient.test.ts
line=18
ctx=65536
''',
 wrong="`authenticatePersona` in `services/demo-service/src/services/authClient.ts` calls `fetch(url, { method: 'POST', headers, body })` against the auth service's login endpoint with no `signal`. An auth service that accepts the connection and never answers holds the caller for as long as the socket lives. The function already has a try/catch that logs and answers `{ success: false, error: message }`. The change adds a constant `AUTH_FETCH_TIMEOUT_MS = 10_000` (with a comment) after the `AUTH_PORT` line and `signal: AbortSignal.timeout(AUTH_FETCH_TIMEOUT_MS),` as the last property of the fetch init. On expiry the fetch rejects and the existing catch answers as it does for an unreachable service.",
 where="- `src/services/authClient.ts:18` - **must change**: directly after `const AUTH_PORT = process.env.AUTH_PORT || '4003';` a blank line, a two-line `// KS-1240:` comment and `const AUTH_FETCH_TIMEOUT_MS = 10_000;` are inserted.\n- `src/services/authClient.ts:38` - **must change**: after the `body: JSON.stringify({ email, password }),` line inside the `fetch(url, {` init, one line is added: `signal: AbortSignal.timeout(AUTH_FETCH_TIMEOUT_MS),`.\n- Every other line of the file is NOT touched.",
 exactnote="Two hunks in one file, in file order.\n",
 donot="**Do NOT touch** any other line of `authClient.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It stubs the global `fetch` and the logger; nothing touches the network.",
 red=['RED KS-1240 R1','RED KS-1240 R2','RED KS-1240 R3'],
 cells="- RED `R1`: at the tip the fetch init has no `signal`, so the recorded signal is `undefined`.\n- RED `R2`: at the tip `AbortSignal.timeout` is never called, so the bounds list is empty.\n- RED `R3`: at the tip the stubbed never-answering fetch has no signal to honour, so the call is still pending after 300 ms and the outcome is 'HUNG'.\n- CONTROL `C1` to `C3`: green at the tip AND after (healthy login, a 401 answer, an unreachable service).",
 premises="- `authClient.ts:18` (AUTH_PORT) and the login fetch at `:35-39` are as quoted (read at the tip); the file has exactly one `fetch(`.\n- `authenticatePersona` is exported and does not throw on failure (its docblock and catch), so the cells call it directly.\n- The service's test runner is vitest (`vitest run`). The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 10000 ms is the right bound for a demo login: the value is the drafter's; the raise seat confirms with the owner.\n- Open PRs touching this file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Slice 10 of the KS-1240 class (demo-service).** Link the PR as Refs KS-1240, never a close-word.",
)
