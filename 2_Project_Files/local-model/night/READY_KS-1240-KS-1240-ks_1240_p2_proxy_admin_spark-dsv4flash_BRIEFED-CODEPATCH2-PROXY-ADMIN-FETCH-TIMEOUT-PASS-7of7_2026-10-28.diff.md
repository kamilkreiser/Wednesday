# READY — KS-1240-KS-1240-ks_1240_p2_proxy_admin (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/out.md.checker/patch.diff`** (from `ls` at 14:15 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts b/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts' vs '+++ --- a/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/api-gateway/src/routes/proxy.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts' vs '+++ --- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/api-gateway/src/routes/admin.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 3: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/api-gateway/src/routes/proxy.ts): `error: patch failed: Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:21`; section 2 (Blockchain/Dev/services/api-gateway/src/routes/admin.ts): `error: patch failed: Blockchain/Dev/services/api-gateway/src/routes/admin.ts:11` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin-control/out.md.checker/patch.diff` rc 0, Spark operator for Wednesday).

**Held 14:15 2026-10-28 by Spark operator for Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/proxy.ts , Blockchain/Dev/services/api-gateway/src/routes/admin.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
10	0	Blockchain/Dev/services/api-gateway/src/routes/proxy.ts
5	0	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
96	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (13 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: proxy.ts admin.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts`, `Blockchain/Dev/services/api-gateway/src/routes/admin.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/proxy.ts 10 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/routes/admin.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts 96 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` (hunks=6, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:21`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=3, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_2.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/api-gateway/src/routes/admin.ts:11`)
- section 3 `section_3.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1240: every hand-built gateway fetch in proxy.ts and admin.ts is bounded RED KS-1240 R1 every fetch call in proxy.ts carries an AbortSignal.timeout', 'KS-1240: every hand-built gateway fetch in proxy.ts and admin.ts is bounded RED KS-1240 R2 every fetch call in admin.ts carries an AbortSignal.timeout', 'KS-1240: every hand-built gateway fetch in proxy.ts and admin.ts is bounded RED KS-1240 R3 proxy.ts declares its two timeout constants, each positive and at most 120000 ms', 'KS-1240: every hand-built gateway fetch in proxy.ts and admin.ts is bounded RED KS-1240 R4 admin.ts declares its timeout constant, positive and at most 120000 ms']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1255 failed=0 | after: total=1263 failed=0` · `NEW reds: []` [baseline_suite.json total=1255 failed=0; after_suite.json total=1263 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` (+10/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts` (+96/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/proxy.ts, Blockchain/Dev/services/api-gateway/src/routes/admin.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p2_proxy_admin/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts b/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/proxy.ts
@@ -21,3 +21,8 @@
 // list live in utils/originateForward.ts — the one reader, shared by onProxyReq
 // below and by the hand-built originate forwards in this file and verification.ts.
 import { vouchHeaderFor } from '../utils/originateForward';
+
+// KS-1240: every hand-built upstream fetch in this file carries a timeout signal. Without one an upstream that accepts the connection and never answers holds the caller's request open for as long
+// as the socket lives. On expiry the fetch rejects and the handler's existing catch answers 502 BAD_GATEWAY, as it already does for an unreachable upstream. The package-generation call gets a longer bound.
+const UPSTREAM_PROXY_FETCH_TIMEOUT_MS = 30_000;
+const UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS = 120_000;
@@ -469,6 +474,7 @@
         });
       }
       const upstream = await fetch(`${authUrl}/api/users/admin/create`, {
+        signal: AbortSignal.timeout(UPSTREAM_PROXY_FETCH_TIMEOUT_MS),
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
@@ -500,6 +506,7 @@
         });
       }
       const upstream = await fetch(`${authUrl}/api/users/admin/${req.params.id}`, {
+        signal: AbortSignal.timeout(UPSTREAM_PROXY_FETCH_TIMEOUT_MS),
         method: 'PATCH',
         headers: {
           'Content-Type': 'application/json',
@@ -663,6 +670,7 @@
         const originateUrl = services.originate?.url || 'http://originate:4000';
         const qs = req.url.includes('?') ? req.url.slice(req.url.indexOf('?')) : '';
         const upstream = await fetch(`${originateUrl}/api/signatories${qs}`, {
+          signal: AbortSignal.timeout(UPSTREAM_PROXY_FETCH_TIMEOUT_MS),
           // KS-1084: forward the tenant authenticateToken verified (it writes x-tenant-id onto req.headers,
           // middleware/auth.ts) so single-tenant originate does not scope this read to DEFAULT_TENANT_ID.
           // KS-955 P2a: and vouch, or a provisioned originate drops that x-tenant-id as unvouched.
@@ -691,6 +699,7 @@
       try {
         const originateUrl = services.originate?.url || 'http://originate:4000';
         const upstream = await fetch(`${originateUrl}/api/third-party-verifiers`, {
+          signal: AbortSignal.timeout(UPSTREAM_PROXY_FETCH_TIMEOUT_MS),
           // KS-1084: forward the tenant authenticateToken verified (it writes x-tenant-id onto req.headers,
           // middleware/auth.ts) so single-tenant originate does not scope this read to DEFAULT_TENANT_ID.
           // KS-955 P2a: and vouch, or a provisioned originate drops that x-tenant-id as unvouched.
@@ -1259,6 +1268,7 @@
     async (req: Request, res: Response) => {
       try {
         const r = await fetch(`${MCP_SERVER_URL}/generate-package`, {
+          signal: AbortSignal.timeout(UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS),
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify(req.body),
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -11,3 +11,6 @@
 import crypto from 'crypto';
 import express from 'express';
 import { runWithPlatformScope } from '@secuura/shared';
+
+// KS-1240: the two hand-built auth-service fetches below carry a timeout signal; without one an auth service that never answers holds the admin's request open. On expiry the handler's existing catch answers 502.
+const UPSTREAM_ADMIN_FETCH_TIMEOUT_MS = 30_000;
@@ -1373,6 +1376,7 @@
       const authUrl = services.auth?.url || 'http://auth:4003';
       const token = req.headers.authorization;
       const upstream = await fetch(`${authUrl}/api/users/admin/create`, {
+        signal: AbortSignal.timeout(UPSTREAM_ADMIN_FETCH_TIMEOUT_MS),
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
@@ -1440,4 +1444,5 @@
       const upstream = await fetch(`${authUrl}/api/users/admin/${encodeURIComponent(id)}`, {
+        signal: AbortSignal.timeout(UPSTREAM_ADMIN_FETCH_TIMEOUT_MS),
         method: 'PATCH',
         headers: {
           'Content-Type': 'application/json',
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts
@@ -0,0 +1,96 @@
+// KS-1240 (api-gateway routes/proxy.ts and routes/admin.ts): the hand-built upstream fetches in these two files carried no timeout, so an upstream that accepted the connection and never answered held the
+// caller's request open with no bound (the key-exchange half of the same ticket is in middleware/auth.ts). This file reads the two sources and pins, per fetch call, that the call carries an
+// AbortSignal.timeout signal, and that the timeout constants exist and are bounded. The extractor balances the call's own parentheses, so a signal in a NEIGHBOUR call cannot satisfy a fetch that has none.
+// C3 and C4 prove the extractor can return both answers (a bounded call that already existed at admin.ts, and a synthetic unbounded one), so the red cells are not vacuous.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const PROXY_SRC = readFileSync(join(__dirname, '..', 'routes', 'proxy.ts'), 'utf8');
+const ADMIN_SRC = readFileSync(join(__dirname, '..', 'routes', 'admin.ts'), 'utf8');
+
+/** Every `fetch(` call in the source, each as the text from `fetch(` to its balancing `)`. */
+function fetchCalls(src: string): string[] {
+  const calls: string[] = [];
+  const re = /\bfetch\(/g;
+  let match: RegExpExecArray | null;
+  while ((match = re.exec(src)) !== null) {
+    const open = match.index + match[0].length - 1;
+    let depth = 0;
+    let end = -1;
+    for (let i = open; i < src.length; i++) {
+      const ch = src[i];
+      if (ch === '(') depth++;
+      else if (ch === ')') {
+        depth--;
+        if (depth === 0) {
+          end = i;
+          break;
+        }
+      }
+    }
+    expect(end, 'unbalanced fetch call at offset ' + match.index).toBeGreaterThan(-1);
+    calls.push(src.slice(match.index, end + 1));
+  }
+  return calls;
+}
+
+function isBounded(call: string): boolean {
+  return call.includes('AbortSignal.timeout(');
+}
+
+/** The first line of each unbounded call, so a failure names the call. */
+function unbounded(src: string): string[] {
+  return fetchCalls(src)
+    .filter((call) => !isBounded(call))
+    .map((call) => call.split('\n')[0].trim());
+}
+
+function constantMs(src: string, name: string): number {
+  const found = new RegExp('const ' + name + ' = ([0-9_]+);').exec(src);
+  return found ? Number(found[1].replace(/_/g, '')) : Number.NaN;
+}
+
+describe('KS-1240: every hand-built gateway fetch in proxy.ts and admin.ts is bounded', () => {
+  it('RED KS-1240 R1 every fetch call in proxy.ts carries an AbortSignal.timeout', () => {
+    expect(unbounded(PROXY_SRC)).toEqual([]);
+  });
+
+  it('RED KS-1240 R2 every fetch call in admin.ts carries an AbortSignal.timeout', () => {
+    expect(unbounded(ADMIN_SRC)).toEqual([]);
+  });
+
+  it('RED KS-1240 R3 proxy.ts declares its two timeout constants, each positive and at most 120000 ms', () => {
+    const proxyMs = constantMs(PROXY_SRC, 'UPSTREAM_PROXY_FETCH_TIMEOUT_MS');
+    const packageMs = constantMs(PROXY_SRC, 'UPSTREAM_PACKAGE_FETCH_TIMEOUT_MS');
+    expect(proxyMs).toBeGreaterThan(0);
+    expect(proxyMs).toBeLessThanOrEqual(120000);
+    expect(packageMs).toBeGreaterThanOrEqual(proxyMs);
+    expect(packageMs).toBeLessThanOrEqual(120000);
+  });
+
+  it('RED KS-1240 R4 admin.ts declares its timeout constant, positive and at most 120000 ms', () => {
+    const adminMs = constantMs(ADMIN_SRC, 'UPSTREAM_ADMIN_FETCH_TIMEOUT_MS');
+    expect(adminMs).toBeGreaterThan(0);
+    expect(adminMs).toBeLessThanOrEqual(120000);
+  });
+
+  it('control KS-1240 C1 proxy.ts has exactly five hand-built fetch calls', () => {
+    expect(fetchCalls(PROXY_SRC)).toHaveLength(5);
+  });
+
+  it('control KS-1240 C2 admin.ts has exactly three hand-built fetch calls', () => {
+    expect(fetchCalls(ADMIN_SRC)).toHaveLength(3);
+  });
+
+  it('control KS-1240 C3 the extractor reads the fetch that was already bounded in admin.ts as bounded', () => {
+    const calls = fetchCalls(ADMIN_SRC).filter((call) => call.includes('bfUrl'));
+    expect(calls).toHaveLength(1);
+    expect(isBounded(calls[0])).toBe(true);
+  });
+
+  it('control KS-1240 C4 the extractor reads a synthetic call with no signal as unbounded', () => {
+    const synthetic = "const r = await fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) });\n";
+    expect(unbounded(synthetic)).toEqual(["fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) })"]);
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: proxy.ts gets two constants (30_000 and 120_000 for the MCP generate-package call) and 5 `signal:` lines; admin.ts gets one constant and 2 `signal:` lines; every signal is the FIRST property of its init object; each fetch already sits in a try whose catch answers 502 BAD_GATEWAY. Test: 8 cells, source-text (pins the count of fetches and a bound on each).
- STRICT APPLY IS NOT CLAIMED: proxy.ts and admin.ts sections applied only with `--recount --ignore-whitespace -C1` (strict apply --check errors at proxy.ts:21 and admin.ts:11; see the Sections lines above). Apply per section with the checker's mode, and have the raise seat re-derive the hunks from the tip rather than trust a strict apply.
- DECISIONS for the owner: the 30 s / 120 s values are the drafter's; a legitimately slow admin-create or signatory list now ends in 502 after 30 s; the bound also covers reading the response body.
- SEQUENCE: shares NO file with `ks_1240_p1` or `ks_1240_p3_batch_audit`; the three KS-1240 READYs may be raised in any order. Refs KS-1240, no close-word.
- Verdict: HOLD-WITH-DECISION.
