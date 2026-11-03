# READY — KS-1868-KS-1868-O94-P11 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/out.md.checker/patch.diff`** (from `ls` at 12:54 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:54 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/cardano/provider.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/cardano/provider.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
20	3	Blockchain/Dev/services/anchoring/src/cardano/provider.ts
68	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (20 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: provider.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/cardano/provider.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/cardano/provider.ts 20 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts 68 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/cardano/provider.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 the chain-health record reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value is recorded as failing with no status and a constant message', 'KS-1868 the chain-health record reads the thrown value safely RED ks1868 R2 an Error with a 503 status whose message getter throws keeps its status and gets a constant message']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=817 failed=2 | after: total=821 failed=1` · `NEW reds: []` [baseline_suite.json total=817 failed=2; after_suite.json total=821 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/cardano/provider.ts` (+20/-3 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts` (+68/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/cardano/provider.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `32921f7921c2cdeb87e4361a2976a9e8cfd6beac` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p11_anchoring_provider_chain_health_record_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/cardano/provider.ts b/Blockchain/Dev/services/anchoring/src/cardano/provider.ts
--- a/Blockchain/Dev/services/anchoring/src/cardano/provider.ts
+++ b/Blockchain/Dev/services/anchoring/src/cardano/provider.ts
@@ -126,7 +126,12 @@
  * Answered:    every other 4xx.
  */
 export function isChainReachableError(err: any): boolean {
-  const status = typeof err?.status_code === 'number' ? err.status_code : null;
+  let status: number | null;
+  try {
+    status = typeof err?.status_code === 'number' ? err.status_code : null;
+  } catch {
+    return false;
+  }
   if (status === null) return false;
   if (status === 402 || status === 408 || status === 429) return false;
   if (status >= 500) return false;
@@ -142,7 +147,19 @@
 function recordChainFailure(err: any): void {
   chainHealth.reachability = 'failing';
   chainHealth.lastFailureAt = new Date().toISOString();
-  chainHealth.lastFailureStatus = typeof err?.status_code === 'number' ? err.status_code : null;
-  chainHealth.lastFailureMessage = String(err?.message ?? 'unknown error').slice(0, 200);
+  let status: number | null;
+  let message: string;
+  try {
+    status = typeof err?.status_code === 'number' ? err.status_code : null;
+  } catch {
+    status = null;
+  }
+  try {
+    message = String(err?.message ?? 'unknown error').slice(0, 200);
+  } catch {
+    message = 'unreadable thrown value';
+  }
+  chainHealth.lastFailureStatus = status;
+  chainHealth.lastFailureMessage = message;
   chainHealth.consecutiveFailures += 1;
 }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts
@@ -0,0 +1,68 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+// KS-1868: the chain-health record of src/cardano/provider.ts. `recordChainOutcome(err)` is called for every failed Blockfrost call (the
+// instrumentation wrapper of the provider handle calls it before the call's own catch runs). It classifies the error with
+// `isChainReachableError` (reads `err?.status_code`) and, for an unreachable chain, `recordChainFailure` (reads `err?.status_code` and
+// `String(err?.message ?? ...)`). All unguarded: when the thrown value cannot be read (a revoked Proxy throws on every read; an Error whose
+// `message` getter throws, throws on the message read) recordChainOutcome THROWS, so the wrapper rejects with a TypeError in place of the provider's
+// error and the record is left half-written. An unreadable value is an unreachable chain with no status and a constant message.
+vi.mock('../utils/logger', () => ({ logger: { debug: () => undefined, info: () => undefined, warn: () => undefined, error: () => undefined } }));
+
+import { recordChainOutcome, getChainHealth, __resetChainHealth } from '../cardano/provider';
+
+/** Record the outcome; the string 'rejected' when recordChainOutcome throws (an assertion can then fail on it). */
+function record(value: unknown): string {
+  try {
+    recordChainOutcome(value);
+    return 'recorded';
+  } catch {
+    return 'rejected';
+  }
+}
+
+describe('KS-1868 the chain-health record reads the thrown value safely', () => {
+  beforeEach(() => {
+    __resetChainHealth();
+  });
+
+  it('control ks1868 C1 a 402 quota error is recorded as failing with its status and message', () => {
+    expect(record(Object.assign(new Error('quota'), { status_code: 402 }))).toBe('recorded');
+    const h = getChainHealth();
+    expect(h.reachability).toBe('failing');
+    expect(h.lastFailureStatus).toBe(402);
+    expect(h.lastFailureMessage).toBe('quota');
+    expect(h.consecutiveFailures).toBe(1);
+  });
+
+  it('control ks1868 C2 a 404 answer is recorded as the chain being reachable', () => {
+    expect(record(Object.assign(new Error('Not found'), { status_code: 404 }))).toBe('recorded');
+    expect(getChainHealth().reachability).toBe('ok');
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value is recorded as failing with no status and a constant message', () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    expect(record(proxy)).toBe('recorded');
+    const h = getChainHealth();
+    expect(h.reachability).toBe('failing');
+    expect(h.lastFailureStatus).toBeNull();
+    expect(h.lastFailureMessage).toBe('unreadable thrown value');
+    expect(h.consecutiveFailures).toBe(1);
+  });
+
+  it('RED ks1868 R2 an Error with a 503 status whose message getter throws keeps its status and gets a constant message', () => {
+    const hostile = Object.create(Error.prototype, {
+      status_code: { value: 503 },
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(record(hostile)).toBe('recorded');
+    const h = getChainHealth();
+    expect(h.reachability).toBe('failing');
+    expect(h.lastFailureStatus).toBe(503);
+    expect(h.lastFailureMessage).toBe('unreadable thrown value');
+  });
+});
```
