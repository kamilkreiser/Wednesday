# READY — KS-1568-ROTATEWAITPARSE-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1568_p1/out.md.checker/patch.diff`** (from `ls` at 19:25 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1568_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1568_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1568_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in index.ts (run 6 vs golden 7 body lines — context, since the change lines are equal) (identical in ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 19:25 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1568_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `80868551e67934cb951d28eec44ce3bdf835944c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/index.ts , Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/security/src/index.ts
64	0	Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1568 o6 - ROTATE_CHAIN_WAIT_MS must be a plain number of milliseconds RED KS-1568 W1: "10s" does not shorten the wait to 10 ms - the second caller is still held at 5 s', 'KS-1568 o6 - ROTATE_CHAIN_WAIT_MS must be a plain number of milliseconds RED KS-1568 W2: "1500ms" does not shorten the wait to 1500 ms - the second caller is still held at 5 s']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=347 failed=0 | after: total=352 failed=0` · `NEW reds: []` [baseline_suite.json total=347 failed=0; after_suite.json total=352 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +65/-1 test=src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts` (+64/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `80868551e67934cb951d28eec44ce3bdf835944c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1568_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1568_p1/KS-1568.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1568_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/index.ts b/Blockchain/Dev/services/security/src/index.ts
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -311,3 +311,3 @@
 function rotateChainWaitMs(): number {
-  const raw = Number.parseInt(process.env.ROTATE_CHAIN_WAIT_MS ?? '', 10);
+  const raw = /^\s*\d+\s*$/.test(process.env.ROTATE_CHAIN_WAIT_MS ?? '') ? Number(process.env.ROTATE_CHAIN_WAIT_MS) : Number.NaN;
   return Number.isFinite(raw) && raw > 0 ? raw : 10_000;
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1568-rotate-chain-wait-ms-ignores-a-unit-suffixed-value.test.ts
@@ -0,0 +1,64 @@
+/**
+ * KS-1568 (the folded-in o6 only) - a unit-suffixed ROTATE_CHAIN_WAIT_MS must not shorten the rotate chain's bounded wait.
+ *
+ * `withConnectorChain` makes the next rotate of one connector wait for the previous one, bounded by
+ * ROTATE_CHAIN_WAIT_MS (default 10 s). The value was read with `Number.parseInt`, which stops at the first non-digit:
+ * `10s` read as 10 ms and `1500ms` as 1500 ms, so a unit suffix silently shrank the bound (to "effectively no chain",
+ * which brings back the pool pressure the chain exists to prevent). A value that is not a plain number of milliseconds
+ * is now ignored and the 10 s default applies. No database: the chain is pure in-process code, driven on fake timers.
+ */
+import { describe, it, expect, beforeAll, afterEach, vi } from 'vitest';
+
+process.env.SECURITY_DISABLE_BOOT = '1';
+delete process.env.DATABASE_URL;
+
+let withConnectorChain: <T>(key: string, fn: () => Promise<T>) => Promise<T>;
+
+beforeAll(async () => {
+  const mod = await import('../index');
+  withConnectorChain = mod.withConnectorChain;
+});
+
+afterEach(() => {
+  delete process.env.ROTATE_CHAIN_WAIT_MS;
+  vi.useRealTimers();
+});
+
+/** Hang a predecessor on `key`, queue a second caller behind it, and report when the second one is let through. */
+async function probe(key: string, env: string | undefined, checkpointsMs: number[]): Promise<boolean[]> {
+  vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout'] });
+  if (env !== undefined) process.env.ROTATE_CHAIN_WAIT_MS = env;
+  void withConnectorChain(key, () => new Promise<never>(() => { /* never settles */ }));
+  let proceeded = false;
+  void withConnectorChain(key, async () => { proceeded = true; });
+  const seen: boolean[] = [];
+  let at = 0;
+  for (const cp of checkpointsMs) {
+    await vi.advanceTimersByTimeAsync(cp - at);
+    at = cp;
+    seen.push(proceeded);
+  }
+  return seen;
+}
+
+describe('KS-1568 o6 - ROTATE_CHAIN_WAIT_MS must be a plain number of milliseconds', () => {
+  it('RED KS-1568 W1: "10s" does not shorten the wait to 10 ms - the second caller is still held at 5 s', async () => {
+    expect(await probe('t:w1', '10s', [5_000])).toEqual([false]);
+  });
+
+  it('RED KS-1568 W2: "1500ms" does not shorten the wait to 1500 ms - the second caller is still held at 5 s', async () => {
+    expect(await probe('t:w2', '1500ms', [5_000])).toEqual([false]);
+  });
+
+  it('CONTROL KS-1568 W3: with the variable unset the wait is the 10 s default (held at 5 s, let through by 10 s)', async () => {
+    expect(await probe('t:w3', undefined, [5_000, 10_001])).toEqual([false, true]);
+  });
+
+  it('CONTROL KS-1568 W4: a plain number is honoured (250 holds at 100 ms and lets through by 250 ms)', async () => {
+    expect(await probe('t:w4', '250', [100, 251])).toEqual([false, true]);
+  });
+
+  it('CONTROL KS-1568 W5: a bad value falls back to the 10 s default (held at 5 s, let through by 10 s)', async () => {
+    expect(await probe('t:w5', 'abc', [5_000, 10_001])).toEqual([false, true]);
+  });
+});
```
