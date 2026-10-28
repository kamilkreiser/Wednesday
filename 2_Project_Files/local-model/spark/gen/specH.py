P='Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
TP='Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts'
E1=("export const connectorBearerCache = new Map<string, { token: string; expiresAt: number }>();\n",
"""export const connectorBearerCache = new Map<string, { token: string; expiresAt: number }>();

// KS-1240: the longest the gateway waits for auth's connector-token exchange or security's key-validate answer. Neither fetch carried a timeout, so an upstream that never answered held the
// caller's request for as long as the socket lived. On expiry the fetch rejects and the existing catch in each function answers exactly as it already did for an unreachable upstream (null).
const UPSTREAM_AUTH_FETCH_TIMEOUT_MS = 5_000;
""")
E2=("      body: JSON.stringify({ apiKey: key }),\n","      body: JSON.stringify({ apiKey: key }),\n      signal: AbortSignal.timeout(UPSTREAM_AUTH_FETCH_TIMEOUT_MS),\n")
E3=("      body: JSON.stringify({ key }),\n","      body: JSON.stringify({ key }),\n      signal: AbortSignal.timeout(UPSTREAM_AUTH_FETCH_TIMEOUT_MS),\n")
TEST='''// KS-1240 (api-gateway middleware/auth.ts getConnectorBearer and validateApiKey): both fetches carried no timeout, so an upstream (auth's connector-token exchange, security's key-validate) that never
// answered held the caller's request open with no bound. T1/T2 pin that each fetch is given an abort signal built from AbortSignal.timeout with a bounded value; T3/T4 drive an upstream that never
// answers and fire that signal: the call must settle with null (the existing unreachable-upstream answer) instead of hanging. A call still pending after 300 ms is reported as the string HUNG, so a
// hang is a red assertion, not a stuck run. C1 to C3 keep the answers for a healthy upstream exactly as they were.
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getConnectorBearer, validateApiKey, apiKeyCache, connectorBearerCache } from '../middleware/auth';

const fetchMock = vi.fn();
vi.stubGlobal('fetch', fetchMock);

let timeoutSpy: ReturnType<typeof vi.spyOn>;
let controller: AbortController;

beforeEach(() => {
  fetchMock.mockReset();
  apiKeyCache.clear();
  connectorBearerCache.clear();
  controller = new AbortController();
  timeoutSpy = vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => controller.signal);
});

afterEach(() => {
  timeoutSpy.mockRestore();
});

function neverAnswering(): void {
  fetchMock.mockImplementation(
    (_url: string, init?: { signal?: AbortSignal }) =>
      new Promise((_resolve, reject) => {
        init?.signal?.addEventListener('abort', () => reject(new Error('aborted by signal')));
      }),
  );
}

async function settled<T>(pending: Promise<T>): Promise<T | 'HUNG'> {
  return Promise.race([pending, new Promise<'HUNG'>((resolve) => setTimeout(() => resolve('HUNG'), 300))]);
}

describe('KS-1240: the gateway key-exchange and key-validate fetches are bounded', () => {
  it('RED KS-1240 T1 the connector-token exchange fetch is given a timeout signal', async () => {
    fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { token: 't1', expiresIn: 600 } }) });
    await getConnectorBearer('sk_ks1240_t1');
    const init = fetchMock.mock.calls[0][1] as { signal?: unknown };
    expect(init.signal).toBeInstanceOf(AbortSignal);
    expect(timeoutSpy).toHaveBeenCalledTimes(1);
    const ms = timeoutSpy.mock.calls[0][0] as number;
    expect(ms).toBeGreaterThan(0);
    expect(ms).toBeLessThanOrEqual(30000);
  });

  it('RED KS-1240 T2 the key-validate fetch is given a timeout signal', async () => {
    fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { valid: false } }) });
    await validateApiKey('sk_ks1240_t2');
    const init = fetchMock.mock.calls[0][1] as { signal?: unknown };
    expect(init.signal).toBeInstanceOf(AbortSignal);
    expect(timeoutSpy).toHaveBeenCalledTimes(1);
    const ms = timeoutSpy.mock.calls[0][0] as number;
    expect(ms).toBeGreaterThan(0);
    expect(ms).toBeLessThanOrEqual(30000);
  });

  it('RED KS-1240 T3 an exchange that never answers settles with null once the signal fires', async () => {
    neverAnswering();
    const pending = getConnectorBearer('sk_ks1240_t3');
    controller.abort();
    expect(await settled(pending)).toBeNull();
  });

  it('RED KS-1240 T4 a validate that never answers settles with null once the signal fires and caches nothing', async () => {
    neverAnswering();
    const pending = validateApiKey('sk_ks1240_t4');
    controller.abort();
    expect(await settled(pending)).toBeNull();
    expect(apiKeyCache.has('sk_ks1240_t4')).toBe(false);
  });

  it('control KS-1240 C1 a healthy exchange still returns the connector token and caches it', async () => {
    fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { token: 'jwt-c1', expiresIn: 600 } }) });
    expect(await getConnectorBearer('sk_ks1240_c1')).toBe('jwt-c1');
    expect(connectorBearerCache.get('sk_ks1240_c1')?.token).toBe('jwt-c1');
  });

  it('control KS-1240 C2 a healthy validate still returns the key metadata', async () => {
    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({ data: { valid: true, connectorId: 'platform-s:c2', scopes: ['documents:write'], organizationId: 'org-c2', tenantId: 'ten-c2' } }),
    });
    const meta = await validateApiKey('sk_ks1240_c2');
    expect(meta?.connectorId).toBe('platform-s:c2');
    expect(meta?.tenantId).toBe('ten-c2');
  });

  it('control KS-1240 C3 a refused exchange (HTTP 502) still returns null', async () => {
    fetchMock.mockResolvedValue({ ok: false, status: 502, json: async () => ({}) });
    expect(await getConnectorBearer('sk_ks1240_c3')).toBeNull();
  });
});
'''
S=dict(dir='ks_1240_p1',ticket='KS-1240',
 title='api-gateway: the connector-token exchange and key-validate fetches in middleware/auth.ts carry no timeout, so an upstream that never answers hangs the request; add AbortSignal.timeout (RUNG 2, code_patch: 3 hunks in one file + one NEW vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 3 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. The ticket leaves the refusal shape to the board ('a 503 on timeout is consistent with...'); this brief does NOT decide a new shape: on timeout the fetch rejects and the EXISTING catch in each function answers as it already does for an unreachable upstream (`null`, which the callers already turn into their failure answer). The raise seat must put that choice to the owner. The Spark may fail this one (capability data).",
 products=[(P,[E1,E2,E3])],
 prodnote=['product, modified in place: THREE hunks - one added constant, then one added `signal:` line in each of the two fetches'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 7 cells'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts` from `Blockchain/Dev/services/api-gateway',
 tier='code_patch', rung='2 (three hunks given byte-exact; the new test given whole)',
 pins='''# code_patch, 3 hunks in api-gateway middleware/auth.ts + a NEW vitest file; ref = ks480 (shape only: same function family, fetch stub); line = the first changed line.
tier=code_patch
ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks480-connector-auth.test.ts
line=185
ctx=65536
''',
 wrong="`getConnectorBearer` (`middleware/auth.ts:194`) and `validateApiKey` (`:222`) each `await fetch(...)` an internal upstream (auth's `/internal/connector-token`, security's `/api/keys/validate`) with NO `signal`. An upstream that accepts the connection and never answers, or answers its body seconds late, holds the gateway request open for as long as the socket lives (the gate measured 'never answers: hangs' and 'body 2.5 s late: hangs 2.5 s' on both develop and head). The change adds one module constant `UPSTREAM_AUTH_FETCH_TIMEOUT_MS = 5_000` and passes `signal: AbortSignal.timeout(UPSTREAM_AUTH_FETCH_TIMEOUT_MS)` in both fetches. When the signal fires the fetch rejects, and each function's EXISTING `catch` answers `null` exactly as for an unreachable upstream. Nothing else changes for a healthy upstream.",
 where="- `middleware/auth.ts:185` - **must change** (insertion): between the blank line that follows the `connectorBearerCache` declaration and the `/**` doc comment of `getConnectorBearer`, insert two comment lines, the constant line and one blank line (hunk 1; see \"The exact change\").\n- `middleware/auth.ts:200` - **must change** (insertion): after `      body: JSON.stringify({ apiKey: key }),` inside `getConnectorBearer`'s fetch, one added line `      signal: AbortSignal.timeout(UPSTREAM_AUTH_FETCH_TIMEOUT_MS),` (hunk 2).\n- `middleware/auth.ts:230` - **must change** (insertion): after `      body: JSON.stringify({ key }),` inside `validateApiKey`'s fetch, the same added line (hunk 3).\n- Both `catch` blocks, every other line of the file and every other fetch in the gateway are (correct for this brief) NOT touched.",
 exactnote="THREE hunks, all pure insertions with context: the constant block, then one `signal:` line in each fetch.\n",
 donot="**Do NOT touch** any other line of `middleware/auth.ts`, the two `catch` blocks, any other gateway fetch (proxy.ts, admin.ts, tokenisation.ts and others stay unbounded for now), or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII. Imports from `'../middleware/auth'` and stubs the global `fetch`, as ks480 does. It spies on `AbortSignal.timeout` so the test controls when the signal fires and reads the millisecond value passed.",
 red=['RED KS-1240 T1','RED KS-1240 T2','RED KS-1240 T3','RED KS-1240 T4'],
 cells="- RED `T1`, `T2`: at the tip neither fetch receives an `init.signal`, so `toBeInstanceOf(AbortSignal)` fails; after the edit each fetch gets the signal built by `AbortSignal.timeout(5000)` (the spy sees one call, with 5000).\n- RED `T3`, `T4`: at the tip the stubbed upstream never answers and nothing aborts it, so the call is still pending after 300 ms and the cell reads `HUNG` (a failed `toBeNull`); after the edit the fired signal rejects the fetch and the call settles with `null`.\n- CONTROL `C1` to `C3`: green at the tip AND after (healthy exchange returns and caches the token; healthy validate returns the metadata; a 502 exchange returns null).",
 premises="- `middleware/auth.ts:185` is the `connectorBearerCache` declaration; `:197-201` is `getConnectorBearer`'s fetch ending `body: JSON.stringify({ apiKey: key }),`; `:227-231` is `validateApiKey`'s fetch ending `body: JSON.stringify({ key }),`; both functions already wrap the fetch in a `try` whose `catch` returns `null` (read from the cache clone at the tip).\n- `AbortSignal.timeout(ms)` exists on the Node versions the gateway runs (admin.ts:967 already uses `AbortSignal.timeout(8000)` in the same service).\n- The service's test runner is vitest; ks480 stubs the global `fetch` the same way.\n- The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 5000 ms is the right bound: not established (the value is the drafter's; the raise seat confirms with the owner). The cells assert only that it is positive and at most 30000.\n- The 503-on-timeout shape the ticket suggests is NOT built: the callers keep their present failure answer for a null.\n- Open PRs touching this file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the connector-token / key-validate half of KS-1240** (the ticket's T-2). Other unbounded gateway fetches stay open. Link the PR as Refs KS-1240, never a close-word.",
)
