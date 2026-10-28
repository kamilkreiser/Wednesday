P1='Blockchain/Dev/services/api-gateway/src/routes/proxy.ts'
P2='Blockchain/Dev/services/api-gateway/src/routes/admin.ts'
TP='Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts'
def sig(c): return "SIGLINE"
A="signal: AbortSignal.timeout(UPSTREAM_PROXY_FETCH_TIMEOUT_MS),"
def site(old_first_line, ind, const='UPSTREAM_PROXY_FETCH_TIMEOUT_MS'):
    return (old_first_line, old_first_line + ind + "signal: AbortSignal.timeout(" + const + "),\n")
IMP1=("import { vouchHeaderFor } from '../utils/originateForward';\n",
"""import { vouchHeaderFor } from '../utils/originateForward';

// KS-1240: every hand-built upstream fetch in this file carries a timeout signal. Without one an upstream that accepts the connection and never answers holds the caller's request open for as long
// as the socket lives. On expiry the fetch rejects and the handler's existing catch answers 502 BAD_GATEWAY, as it already does for an unreachable upstream. The package-generation call gets a longer bound.
const UPSTREAM_PROXY_FETCH_TIMEOUT_MS = 30_000;
const UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS = 120_000;
""")
S1=site("      const upstream = await fetch(`${authUrl}/api/users/admin/create`, {\n","        ")
S2=site("      const upstream = await fetch(`${authUrl}/api/users/admin/${req.params.id}`, {\n","        ")
S3=site("        const upstream = await fetch(`${originateUrl}/api/signatories${qs}`, {\n","          ")
S4=site("        const upstream = await fetch(`${originateUrl}/api/third-party-verifiers`, {\n","          ")
S5=site("        const r = await fetch(`${MCP_SERVER_URL}/generate-package`, {\n","          ","UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS")
IMP2=("import { runWithPlatformScope } from '@secuura/shared';\n",
"""import { runWithPlatformScope } from '@secuura/shared';

// KS-1240: the two hand-built auth-service fetches below carry a timeout signal; without one an auth service that never answers holds the admin's request open. On expiry the handler's existing catch answers 502.
const UPSTREAM_ADMIN_FETCH_TIMEOUT_MS = 30_000;
""")
A1=site("      const upstream = await fetch(`${authUrl}/api/users/admin/create`, {\n","        ","UPSTREAM_ADMIN_FETCH_TIMEOUT_MS")
A2=site("      const upstream = await fetch(`${authUrl}/api/users/admin/${encodeURIComponent(id)}`, {\n","        ","UPSTREAM_ADMIN_FETCH_TIMEOUT_MS")
TEST='''// KS-1240 (api-gateway routes/proxy.ts and routes/admin.ts): the hand-built upstream fetches in these two files carried no timeout, so an upstream that accepted the connection and never answered held the
// caller's request open with no bound (the key-exchange half of the same ticket is in middleware/auth.ts). This file reads the two sources and pins, per fetch call, that the call carries an
// AbortSignal.timeout signal, and that the timeout constants exist and are bounded. The extractor balances the call's own parentheses, so a signal in a NEIGHBOUR call cannot satisfy a fetch that has none.
// C3 and C4 prove the extractor can return both answers (a bounded call that already existed at admin.ts, and a synthetic unbounded one), so the red cells are not vacuous.
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const PROXY_SRC = readFileSync(join(__dirname, '..', 'routes', 'proxy.ts'), 'utf8');
const ADMIN_SRC = readFileSync(join(__dirname, '..', 'routes', 'admin.ts'), 'utf8');

/** Every `fetch(` call in the source, each as the text from `fetch(` to its balancing `)`. */
function fetchCalls(src: string): string[] {
  const calls: string[] = [];
  const re = /\\bfetch\\(/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(src)) !== null) {
    const open = match.index + match[0].length - 1;
    let depth = 0;
    let end = -1;
    for (let i = open; i < src.length; i++) {
      const ch = src[i];
      if (ch === '(') depth++;
      else if (ch === ')') {
        depth--;
        if (depth === 0) {
          end = i;
          break;
        }
      }
    }
    expect(end, 'unbalanced fetch call at offset ' + match.index).toBeGreaterThan(-1);
    calls.push(src.slice(match.index, end + 1));
  }
  return calls;
}

function isBounded(call: string): boolean {
  return call.includes('AbortSignal.timeout(');
}

/** The first line of each unbounded call, so a failure names the call. */
function unbounded(src: string): string[] {
  return fetchCalls(src)
    .filter((call) => !isBounded(call))
    .map((call) => call.split('\\n')[0].trim());
}

function constantMs(src: string, name: string): number {
  const found = new RegExp('const ' + name + ' = ([0-9_]+);').exec(src);
  return found ? Number(found[1].replace(/_/g, '')) : Number.NaN;
}

describe('KS-1240: every hand-built gateway fetch in proxy.ts and admin.ts is bounded', () => {
  it('RED KS-1240 R1 every fetch call in proxy.ts carries an AbortSignal.timeout', () => {
    expect(unbounded(PROXY_SRC)).toEqual([]);
  });

  it('RED KS-1240 R2 every fetch call in admin.ts carries an AbortSignal.timeout', () => {
    expect(unbounded(ADMIN_SRC)).toEqual([]);
  });

  it('RED KS-1240 R3 proxy.ts declares its two timeout constants, each positive and at most 120000 ms', () => {
    const proxyMs = constantMs(PROXY_SRC, 'UPSTREAM_PROXY_FETCH_TIMEOUT_MS');
    const packageMs = constantMs(PROXY_SRC, 'UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS');
    expect(proxyMs).toBeGreaterThan(0);
    expect(proxyMs).toBeLessThanOrEqual(120000);
    expect(packageMs).toBeGreaterThanOrEqual(proxyMs);
    expect(packageMs).toBeLessThanOrEqual(120000);
  });

  it('RED KS-1240 R4 admin.ts declares its timeout constant, positive and at most 120000 ms', () => {
    const adminMs = constantMs(ADMIN_SRC, 'UPSTREAM_ADMIN_FETCH_TIMEOUT_MS');
    expect(adminMs).toBeGreaterThan(0);
    expect(adminMs).toBeLessThanOrEqual(120000);
  });

  it('control KS-1240 C1 proxy.ts has exactly five hand-built fetch calls', () => {
    expect(fetchCalls(PROXY_SRC)).toHaveLength(5);
  });

  it('control KS-1240 C2 admin.ts has exactly three hand-built fetch calls', () => {
    expect(fetchCalls(ADMIN_SRC)).toHaveLength(3);
  });

  it('control KS-1240 C3 the extractor reads the fetch that was already bounded in admin.ts as bounded', () => {
    const calls = fetchCalls(ADMIN_SRC).filter((call) => call.includes('bfUrl'));
    expect(calls).toHaveLength(1);
    expect(isBounded(calls[0])).toBe(true);
  });

  it('control KS-1240 C4 the extractor reads a synthetic call with no signal as unbounded', () => {
    const synthetic = "const r = await fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) });\\n";
    expect(unbounded(synthetic)).toEqual(["fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) })"]);
  });
});
'''
S=dict(dir='ks_1240_p2_proxy_admin',ticket='KS-1240',
 title='api-gateway: the hand-built upstream fetches in routes/proxy.ts (5) and routes/admin.ts (2) carry no timeout; add AbortSignal.timeout to each (RUNG 3, code_patch2: TWO product files, 9 hunks + one NEW source-text vitest)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 3 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. This is the wider half of KS-1240 (the connector-token / key-validate half is `ks_1240_p1`, in middleware/auth.ts). Seven near-identical edits across two files; the bound values (30 s, and 120 s for MCP package generation) are the drafter's, the raise seat confirms them with the owner. tokenisation.ts is left out ON PURPOSE: its catch degrades to an empty map, so a timeout there changes what PII reaches storage and needs a ruling. The Spark may fail this one (capability data).",
 products=[(P1,[IMP1,S1,S2,S3,S4,S5]),(P2,[IMP2,A1,A2])],
 prodnote=['product 1 of 2, modified in place: SIX hunks - an added constant block, then one added `signal:` line in each of the five fetches','product 2 of 2, modified in place: THREE hunks - an added constant block, then one added `signal:` line in each of the two fetches that had none'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 8 cells (source-text pins, balanced-parenthesis extractor)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts` from `Blockchain/Dev/services/api-gateway',
 tier='code_patch2', rung='3 (two product files in one service, nine hunks given byte-exact; the new test given whole)',
 pins='''# code_patch2: 2 products in services/api-gateway (proxy.ts six hunks; admin.ts three hunks) + 1 NEW source-text vitest file; ref = ks689 (shape only: the same mountArgs-style source reader); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks689-users-admin-create-auth-mount.test.ts
line=29
ctx=65536
''',
 wrong="Five hand-built `fetch(...)` calls in `routes/proxy.ts` (POST and PATCH `/api/users/admin/...` to auth, GET `/api/signatories` and GET `/api/third-party-verifiers` to originate, POST `/api/mcp/generate-package` to the MCP server) and two in `routes/admin.ts` (POST `/api/users/admin/create` and PATCH `/api/users/admin/:id` to auth) pass no `signal`. An upstream that accepts the connection and never answers holds the caller's request open for as long as the socket lives. Each call sits inside a `try` whose `catch` already answers `502 BAD_GATEWAY`. The change adds, per file, a module constant for the bound and, in each of the seven fetches, `signal: AbortSignal.timeout(<constant>),` as the FIRST property of the init object. When the signal fires the fetch rejects and the existing catch answers 502, exactly as for an unreachable upstream. Nothing else changes for a healthy upstream.",
 where="- `routes/proxy.ts:25` - **must change** (insertion): after the import `import { vouchHeaderFor } from '../utils/originateForward';` a blank line, three comment lines and the two constants `UPSTREAM_PROXY_FETCH_TIMEOUT_MS = 30_000` and `UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS = 120_000` (hunk 1 of proxy.ts).\n- `routes/proxy.ts:471`, `:502`, `:665`, `:693`, `:1261` - **must change** (insertion, one hunk each): one added line right after the line that opens each `fetch(... , {`. The first four use `UPSTREAM_PROXY_FETCH_TIMEOUT_MS`; the `/generate-package` call uses `UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS`. Line numbers are at the tip BEFORE the constant block is added.\n- `routes/admin.ts:13` - **must change** (insertion): after `import { runWithPlatformScope } from '@secuura/shared';` a blank line, one comment line and the constant `UPSTREAM_ADMIN_FETCH_TIMEOUT_MS = 30_000`.\n- `routes/admin.ts:1375`, `:1440` - **must change** (insertion, one hunk each): one added line right after the line that opens each of the two auth fetches. The already-bounded fetch at `:967` (`AbortSignal.timeout(8000)`) is NOT touched.\n- Every `catch` block and every other line of both files are NOT touched.",
 exactnote="Nine hunks (six in proxy.ts, three in admin.ts): each a pure insertion with context.\n",
 donot="**Do NOT touch** any other line of `proxy.ts` or `admin.ts`, the `catch` blocks, `services/tokenisation.ts`, `middleware/auth.ts` (another brief), or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It reads `routes/proxy.ts` and `routes/admin.ts` with `readFileSync` (the same technique as ks689).",
 red=['RED KS-1240 R1','RED KS-1240 R2','RED KS-1240 R3','RED KS-1240 R4'],
 cells="- RED `R1`, `R2`: at the tip five (proxy.ts) and two (admin.ts) fetch calls carry no `AbortSignal.timeout`, so `unbounded(...)` returns their first lines and `toEqual([])` fails; after the edit both lists are empty.\n- RED `R3`, `R4`: at the tip the constants do not exist, so `constantMs` is NaN and `toBeGreaterThan(0)` fails; after the edit they read 30000, 120000 and 30000.\n- CONTROL `C1` to `C4`: green at the tip AND after (proxy.ts has five fetch calls, admin.ts has three, the extractor reads admin.ts's already-bounded `bfUrl` fetch as bounded, and a synthetic unsignalled call as unbounded).",
 premises="- The seven unbounded fetches are at `proxy.ts:471, :502, :665, :693, :1261` and `admin.ts:1375, :1440`; `admin.ts:967` is already `fetch(bfUrl, { ..., signal: AbortSignal.timeout(8000) })`; no other `fetch(` occurs in either file (read with a case-insensitive grep at the tip).\n- Each of the seven sits inside a `try` whose `catch` answers 502 BAD_GATEWAY (proxy.ts :478-481, :509-512, :672-675, :700-703, :1274-1276; admin.ts :1383-1385 and :1450-1452).\n- `ks689-users-admin-create-auth-mount.test.ts` reads `routes/proxy.ts` with `readFileSync` from `__dirname/..`, so the same read works here.\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether 30 s / 120 s are the right bounds: not established (the drafter's values; the raise seat confirms with the owner). Whether MCP package generation can legitimately take longer than 120 s: not measured.\n- The cells are source-text pins; no request is sent, so the 502 on expiry is read from the existing catch blocks, not driven.\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the proxy.ts and admin.ts hand-built fetch half of KS-1240.** `services/tokenisation.ts`, `routes/batch.ts`, `routes/audit-export.ts` and the health fetches stay open. Link the PR as Refs KS-1240, never a close-word.",
)
