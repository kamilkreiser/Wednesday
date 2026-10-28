D='Blockchain/Dev/services/tenant-provisioning/src/'
PM,PI=D+'meteringKey.ts',D+'index.ts'
TP=D+'__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts'
M1=("/**\n * Mint a read-only, single-tenant `metering:read` connector key for Platform-S.",
"""// KS-1240 (class): the longest provisioning waits for the security service to mint the metering key. The fetch carried no timeout, so a security service that accepted the connection and never answered
// held the tenant-creation request for as long as the socket lived. On expiry the fetch rejects, requestMeteringKey throws, and the provisioning handler fails soft as it already does for a non-2xx.
const METERING_KEY_FETCH_TIMEOUT_MS = 10_000;

/**
 * Mint a read-only, single-tenant `metering:read` connector key for Platform-S.""")
M2=("      connectorId: 'platform-s',\n    }),\n  });","      connectorId: 'platform-s',\n    }),\n    signal: AbortSignal.timeout(METERING_KEY_FETCH_TIMEOUT_MS),\n  });")
I1=("const TOKENISATION_URL = process.env.TOKENISATION_URL || 'http://tokenisation:4021';\n",
"""const TOKENISATION_URL = process.env.TOKENISATION_URL || 'http://tokenisation:4021';

// KS-1240 (class): the longest provisioning waits for the tokenisation service to generate a tenant key. The fetch carried no timeout, so a tokenisation service that accepted the connection and never
// answered held the tenant-creation request for as long as the socket lived. On expiry the fetch rejects out of requestKeyGeneration to the handler's existing error path.
const KEY_GENERATION_FETCH_TIMEOUT_MS = 10_000;
""")
I2=("    body: JSON.stringify({ tenantId, tenantSlug }),\n  });","    body: JSON.stringify({ tenantId, tenantSlug }),\n    signal: AbortSignal.timeout(KEY_GENERATION_FETCH_TIMEOUT_MS),\n  });")
TEST='''// KS-1240 (class: hand-built outbound fetches with no timeout), tenant-provisioning meteringKey.ts and index.ts: the metering-key mint (requestMeteringKey, exported) and the tenant key generation
// (requestKeyGeneration, private to index.ts, which boots a server and so is read as TEXT here) fetched the security and tokenisation services with no `signal`, so a service that accepted the connection
// and never answered held the tenant-creation request for as long as the socket lived. requestMeteringKey is driven directly with a stubbed global fetch that honours `init.signal` (and never answers when there
// is none). R1 pins that its fetch carries an AbortSignal, R2 that the bound is sane, R3 that a silent security service ends in a rejection and not a hang, R4 and R5 that index.ts bounds its fetch;
// C1 to C3 pin the unchanged answers.
import { describe, it, expect, vi, afterEach } from 'vitest';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { requestMeteringKey } from '../meteringKey.js';

const SEC = 'http://security:4004';
const INDEX_SRC = readFileSync(fileURLToPath(new URL('../index.ts', import.meta.url)), 'utf8');

afterEach(() => { vi.restoreAllMocks(); vi.unstubAllGlobals(); });

/** The key the security service mints, as a Response-like object. */
function mintedKey(): Response {
  return { ok: true, status: 201, json: async () => ({ success: true, data: { id: 'key_abc', key: 'sk_deadbeef', prefix: 'sk_deadbeef0' } }) } as unknown as Response;
}

/** Answers the mint and records the signal the call carried. */
function stubAnswering(seen: unknown[]): void {
  vi.stubGlobal('fetch', vi.fn(async (_url: unknown, init?: { signal?: unknown }) => { seen.push(init?.signal); return mintedKey(); }));
}

/** Every call honours its signal; a call with NO signal never answers (the hang the fix removes). */
function stubNeverAnswering(): void {
  vi.stubGlobal('fetch', vi.fn((_url: unknown, init?: { signal?: AbortSignal }) =>
    new Promise<Response>((_resolve, reject) => {
      const signal = init?.signal;
      if (!signal) return;
      if (signal.aborted) reject(new Error('aborted'));
      else signal.addEventListener('abort', () => reject(new Error('aborted')));
    })));
}

/** 'REJECTED' when the call rejects, 'RESOLVED' when it resolves, 'HUNG' when it is still pending after 300 ms, so a hang is a red assertion and not a stuck run. */
async function outcome(run: () => Promise<unknown>): Promise<string> {
  return Promise.race([
    run().then(() => 'RESOLVED', () => 'REJECTED'),
    new Promise<string>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
  ]);
}

describe('KS-1240: tenant provisioning bounds its outbound fetches', () => {
  it('RED KS-1240 R1 the metering-key fetch carries an AbortSignal', async () => {
    const seen: unknown[] = [];
    stubAnswering(seen);
    await requestMeteringKey(SEC, 'tenant-123', 'acme', 'Bearer admintoken');
    expect(seen).toHaveLength(1);
    expect(seen[0]).toBeInstanceOf(AbortSignal);
  });

  it('RED KS-1240 R2 the bound handed to AbortSignal.timeout is positive and at most 30000 ms', async () => {
    const timeout = vi.spyOn(AbortSignal, 'timeout');
    stubAnswering([]);
    await requestMeteringKey(SEC, 'tenant-123', 'acme');
    const bounds = timeout.mock.calls.map((c) => c[0] as number);
    expect(bounds).toHaveLength(1);
    expect(bounds[0]).toBeGreaterThan(0);
    expect(bounds[0]).toBeLessThanOrEqual(30000);
  });

  it('RED KS-1240 R3 a security service that never answers ends in a rejection, not a hang', async () => {
    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
    stubNeverAnswering();
    expect(await outcome(() => requestMeteringKey(SEC, 'tenant-123', 'acme'))).toBe('REJECTED');
  });

  it('RED KS-1240 R4 the generate-key fetch in index.ts carries a timeout signal', () => {
    expect(INDEX_SRC).toContain('signal: AbortSignal.timeout(KEY_GENERATION_FETCH_TIMEOUT_MS),');
  });

  it('RED KS-1240 R5 index.ts declares the generate-key bound as a positive number of at most 30000 ms', () => {
    const match = /const KEY_GENERATION_FETCH_TIMEOUT_MS = ([0-9_]+);/.exec(INDEX_SRC);
    const ms = match ? Number(match[1].replace(/_/g, '')) : NaN;
    expect(ms).toBeGreaterThan(0);
    expect(ms).toBeLessThanOrEqual(30000);
  });

  it('control KS-1240 C1 a healthy mint still returns the key material', async () => {
    stubAnswering([]);
    expect(await requestMeteringKey(SEC, 'tenant-123', 'acme')).toEqual({ key: 'sk_deadbeef', prefix: 'sk_deadbeef0', id: 'key_abc' });
  });

  it('control KS-1240 C2 a non-2xx answer still throws with the status in the message', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 403, json: async () => ({}) })));
    await expect(requestMeteringKey(SEC, 't', 's')).rejects.toThrow('403');
  });

  it('control KS-1240 C3 index.ts still sends the generate-key request to the tokenisation service', () => {
    expect(INDEX_SRC).toContain('${TOKENISATION_URL}/api/generate-key');
  });
});
'''
S=dict(dir='ks_1240_p8_provisioning',ticket='KS-1240',
 title='(class, slice 8) tenant-provisioning: the metering-key mint in meteringKey.ts and the tenant key generation in index.ts fetch the security and tokenisation services with no timeout; add AbortSignal.timeout (RUNG 3, code_patch2: 2 products, 4 hunks + one NEW behavioural and source-text vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 4 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Slice 8 of the KS-1240 class (hand-built fetch with no timeout): KS-1240 is the gateway ticket and applying it to tenant-provisioning is the drafter's extension, stated: the raise seat confirms the scope with the owner. TWO products in one service: an exported function tested by behaviour (meteringKey.ts) and a private one in a file that boots a server (index.ts) tested by source text, in ONE new test file. On expiry the fetch rejects: requestMeteringKey throws as it already does for a non-2xx (its caller fails soft), and requestKeyGeneration's rejection reaches the handler's existing error path (not read here). The Spark may fail this one (capability data).",
 products=[(PM,[M1,M2]),(PI,[I1,I2])],
 prodnote=['product 1 (meteringKey.ts), modified in place: TWO hunks - a constant block before the function doc comment, then one `signal:` line in the fetch','product 2 (index.ts), modified in place: TWO hunks - a constant block after `TOKENISATION_URL`, then one `signal:` line in the fetch'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 8 cells (5 red, 3 control; stubbed fetch for the exported function, source text for index.ts)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts` from `Blockchain/Dev/services/tenant-provisioning',
 tier='code_patch2', rung='3 (four hunks in two products given byte-exact; the new test given whole)',
 pins='''# code_patch2: 2 products in services/tenant-provisioning (meteringKey.ts 2 hunks; index.ts 2) + 1 NEW vitest file; ref = meteringKey.test.ts (fetch-stub spec of the exported function, shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/tenant-provisioning/src/__tests__/meteringKey.test.ts
line=20
ctx=65536
''',
 wrong="Two fetches in `services/tenant-provisioning` carry no `signal`: `requestMeteringKey` in `meteringKey.ts` (POST to the security service's `/api/keys`, exported) and `requestKeyGeneration` in `index.ts` (POST to the tokenisation service's `/api/generate-key`, private to the file). A service that accepts the connection and never answers holds the tenant-creation request open for as long as the socket lives. The change adds, per file, one module constant (`METERING_KEY_FETCH_TIMEOUT_MS = 10_000` in meteringKey.ts, `KEY_GENERATION_FETCH_TIMEOUT_MS = 10_000` in index.ts, each with a comment) and `signal: AbortSignal.timeout(<constant>),` as the last property of the fetch's init object. When the signal fires the fetch rejects: `requestMeteringKey` throws exactly as it already does for a non-2xx (its doc says the caller fails soft), and `requestKeyGeneration`'s rejection propagates to its caller. For a healthy service nothing changes.",
 where="- `meteringKey.ts:20` - **must change** (insertion): before the `/**` doc comment of `requestMeteringKey`, three comment/constant lines and one blank line (hunk 1).\n- `meteringKey.ts:57` - **must change** (insertion): after the `    }),` that closes `body: JSON.stringify({...})` inside the fetch, one added line `    signal: AbortSignal.timeout(METERING_KEY_FETCH_TIMEOUT_MS),` (hunk 2).\n- `index.ts:37` - **must change** (insertion): after the `const TOKENISATION_URL = ...;` line, one blank line, three comment lines and the constant line (hunk 3).\n- `index.ts:137` - **must change** (insertion): after `    body: JSON.stringify({ tenantId, tenantSlug }),`, one added line `    signal: AbortSignal.timeout(KEY_GENERATION_FETCH_TIMEOUT_MS),` (hunk 4).\n- Every other line of both files is NOT touched.",
 exactnote="FOUR hunks in two files, all pure insertions with context.\n",
 donot="**Do NOT touch** any other line of either file, the handler that calls `requestKeyGeneration`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports (ESM; `.js` import suffix as the sibling spec), no top-level await. It stubs the global `fetch` for `requestMeteringKey`, spies on `AbortSignal.timeout`, and reads `index.ts` as text with `readFileSync(fileURLToPath(new URL('../index.ts', import.meta.url)))` because importing it boots the service.",
 red=['RED KS-1240 R1','RED KS-1240 R2','RED KS-1240 R3','RED KS-1240 R4','RED KS-1240 R5'],
 cells="- RED `R1`: at the tip the fetch carries no `init.signal`; after the edit it does.\n- RED `R2`: at the tip `AbortSignal.timeout` is never called (0 bounds, not 1); after the edit one bound, positive and at most 30000.\n- RED `R3`: `AbortSignal.timeout` returns an already-aborted signal and the stub honours it; at the tip no signal is passed, the stub never answers and the cell reads `HUNG`; after the edit the call rejects (`REJECTED`).\n- RED `R4`, `R5`: at the tip index.ts holds neither the `signal:` line nor the constant; after the edit both, the bound within 1..30000.\n- CONTROL `C1` to `C3`: green at the tip AND after (healthy mint returns the key material; a 403 still throws with the status; index.ts still targets `/api/generate-key`).",
 premises="- `meteringKey.ts` :20 is the `/**` that opens the doc comment of `requestMeteringKey`; the fetch closes at :57-:58 with `    }),` then `  });` (read from the cache clone at the tip).\n- `index.ts` :37 is the `TOKENISATION_URL` const and the generate-key fetch ends at :137-:138 with `body: JSON.stringify({ tenantId, tenantSlug }),` then `  });`.\n- The sibling spec `meteringKey.test.ts` stubs `fetch` with `vi.stubGlobal` and asserts on `opts.method`, `opts.headers` and `opts.body` only, so an extra `signal` property does not disturb it.\n- The package uses ESM (`.js` import suffixes); the test reads `index.ts` with `import.meta.url`.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 10000 ms is the right bound: the value is the drafter's; the raise seat confirms with the owner. A signal also bounds reading the response body.\n- How the tenant-creation handler presents a rejection from `requestKeyGeneration` (not read or pinned here; the metering mint's caller is documented to fail soft).\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Slice 8 of the KS-1240 class (tenant-provisioning).** Link the PR as Refs KS-1240, never a close-word.",
)
