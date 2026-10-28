# READY — KS-1240-KS-1240-ks_1240_p3_batch_audit (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/out.md.checker/patch.diff`** (from `ls` at 14:15 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit-control/out.md.checker/patch.diff` rc 0, Spark operator for Wednesday).

**Held 14:15 2026-10-28 by Spark operator for Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/batch.ts , Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	0	Blockchain/Dev/services/api-gateway/src/routes/batch.ts
5	1	Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
92	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: batch.ts audit-export.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/batch.ts`, `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/batch.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts 92 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1240: the batch and audit-export upstream fetches are bounded RED KS-1240 R1 every fetch call in batch.ts carries an AbortSignal.timeout', 'KS-1240: the batch and audit-export upstream fetches are bounded RED KS-1240 R2 every fetch call in audit-export.ts carries an AbortSignal.timeout', 'KS-1240: the batch and audit-export upstream fetches are bounded RED KS-1240 R3 batch.ts declares its timeout constant, positive and at most 120000 ms', 'KS-1240: the batch and audit-export upstream fetches are bounded RED KS-1240 R4 audit-export.ts declares its timeout constant, positive and at most 120000 ms']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1255 failed=0 | after: total=1263 failed=0` · `NEW reds: []` [baseline_suite.json total=1255 failed=0; after_suite.json total=1263 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` (+5/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts` (+92/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/batch.ts, Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p3_batch_audit/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/batch.ts b/Blockchain/Dev/services/api-gateway/src/routes/batch.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/batch.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/batch.ts
@@ -122,3 +122,7 @@
+// KS-1240: the batch fan-out fetch carries a timeout signal. Without one an originate or transfer service that never answers holds the whole batch request open. On expiry the fetch rejects and the existing
+// catch in proxyRequest returns `{ ok: false, error }` for that item, as it already does for an unreachable service.
+const UPSTREAM_BATCH_FETCH_TIMEOUT_MS = 30_000;
+
 async function proxyRequest(
   baseUrl: string,
   path: string,
@@ -132,4 +136,5 @@
     const response = await fetch(`${baseUrl}${path}`, {
+      signal: AbortSignal.timeout(UPSTREAM_BATCH_FETCH_TIMEOUT_MS),
       method: 'POST',
       headers,
       body: JSON.stringify(body),
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts
@@ -73,3 +73,7 @@
+// KS-1240: the audit-log fetch carries a timeout signal. Without one a security service that never answers holds the export request open. On expiry the fetch rejects and the existing catch answers the
+// constant 502 BAD_GATEWAY, as it already does for an unreachable service.
+const UPSTREAM_AUDIT_FETCH_TIMEOUT_MS = 30_000;
+
 function escapeCSVField(value: string | undefined | null): string {
   if (value == null) return '';
   const str = String(value);
@@ -172,5 +176,5 @@
       const response = await fetch(
         // KS-745: the security service lists at /api/audit (no /logs route — that hit /api/audit/:id with id "logs" → 404)
         `${SECURITY_SERVICE_URL}/api/audit?${queryParams.toString()}`,
-        { method: 'GET', headers },
+        { method: 'GET', headers, signal: AbortSignal.timeout(UPSTREAM_AUDIT_FETCH_TIMEOUT_MS) },
       );
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts
@@ -0,0 +1,92 @@
+// KS-1240 (api-gateway routes/batch.ts and routes/audit-export.ts): the upstream fetch in each of these two files carried no timeout, so an upstream that accepted the connection and never answered held the
+// caller's request open with no bound (the key-exchange half of the same ticket is in middleware/auth.ts, the proxy.ts and admin.ts half is another file). This file reads the two sources and pins, per fetch call, that the call carries an
+// AbortSignal.timeout signal, and that the timeout constants exist and are bounded. The extractor balances the call's own parentheses, so a signal in a NEIGHBOUR call cannot satisfy a fetch that has none.
+// C3 and C4 prove the extractor can return both answers (a bounded call that already existed at admin.ts, and a synthetic unbounded one), so the red cells are not vacuous.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const BATCH_SRC = readFileSync(join(__dirname, '..', 'routes', 'batch.ts'), 'utf8');
+const AUDIT_SRC = readFileSync(join(__dirname, '..', 'routes', 'audit-export.ts'), 'utf8');
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
+describe('KS-1240: the batch and audit-export upstream fetches are bounded', () => {
+  it('RED KS-1240 R1 every fetch call in batch.ts carries an AbortSignal.timeout', () => {
+    expect(unbounded(BATCH_SRC)).toEqual([]);
+  });
+
+  it('RED KS-1240 R2 every fetch call in audit-export.ts carries an AbortSignal.timeout', () => {
+    expect(unbounded(AUDIT_SRC)).toEqual([]);
+  });
+
+  it('RED KS-1240 R3 batch.ts declares its timeout constant, positive and at most 120000 ms', () => {
+    const ms = constantMs(BATCH_SRC, 'UPSTREAM_BATCH_FETCH_TIMEOUT_MS');
+    expect(ms).toBeGreaterThan(0);
+    expect(ms).toBeLessThanOrEqual(120000);
+  });
+
+  it('RED KS-1240 R4 audit-export.ts declares its timeout constant, positive and at most 120000 ms', () => {
+    const ms = constantMs(AUDIT_SRC, 'UPSTREAM_AUDIT_FETCH_TIMEOUT_MS');
+    expect(ms).toBeGreaterThan(0);
+    expect(ms).toBeLessThanOrEqual(120000);
+  });
+
+  it('control KS-1240 C1 batch.ts has exactly one fetch call', () => {
+    expect(fetchCalls(BATCH_SRC)).toHaveLength(1);
+  });
+
+  it('control KS-1240 C2 audit-export.ts has exactly one fetch call', () => {
+    expect(fetchCalls(AUDIT_SRC)).toHaveLength(1);
+  });
+
+  it('control KS-1240 C3 the extractor reads a call whose init object holds a signal as bounded', () => {
+    const synthetic = "const r = await fetch(url, { method: 'GET', signal: AbortSignal.timeout(5000) });\n";
+    expect(unbounded(synthetic)).toEqual([]);
+  });
+
+  it('control KS-1240 C4 the extractor reads a synthetic call with no signal as unbounded', () => {
+    const synthetic = "const r = await fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) });\n";
+    expect(unbounded(synthetic)).toEqual(["fetch('http://x', { method: 'POST', body: JSON.stringify({ a: (1) }) })"]);
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: batch.ts constant 30_000 + `signal:` in the single fan-out fetch of `proxyRequest` (an expired signal lands in its existing catch, which returns `{ ok: false, error }` for that item); audit-export.ts constant 30_000 and the init object becomes `{ method: 'GET', headers, signal: AbortSignal.timeout(...) }` (the one `-` line is that init line); its catch answers the constant 502. Test: 8 source-text cells.
- DECISIONS for the owner: the 30 s values are the drafter's. The audit-export fetch reads the whole security answer with `response.json()` inside the same signal, so a very large audit page that takes more than 30 s to arrive now ends in 502; the batch item reports an error text instead of waiting.
- SEQUENCE: shares NO file with `ks_1240_p1` or `ks_1240_p2_proxy_admin`; any order. Refs KS-1240, no close-word.
- Verdict: HOLD-WITH-DECISION.
