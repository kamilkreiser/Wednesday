# READY — KS-1868-KS-1868-O87-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 01:37 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 01:37 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts
103	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: confirmation.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts 103 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1868 waitForConfirmation counts a failed attempt and reports text for a hostile thrown value RED ks1868 R1: a revoked Proxy counts one failed attempt and is reported as text, as for an ordinary Error', 'KS-1868 waitForConfirmation counts a failed attempt and reports text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws counts one failed attempt and is reported as text, as for an ordinary Error', 'KS-1868 waitForConfirmation counts a failed attempt and reports text for a hostile thrown value RED ks1868 R3: an Error whose message is a Symbol counts one failed attempt and is reported as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=760 failed=1 | after: total=767 failed=1` · `NEW reds: []` [baseline_suite.json total=760 failed=1; after_suite.json total=767 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts` (+103/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p5_anchoring_confirmation_wait_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts b/Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts
--- a/Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts
+++ b/Blockchain/Dev/services/anchoring/src/cardano/confirmation.ts
@@ -104,6 +104,13 @@
     } catch (err: any) {
       errored += 1;
       if (onStatusUpdate) {
-        onStatusUpdate(attempt, `error: ${err?.message}`);
+        let reason: string | null | undefined;
+        try {
+          const m = err?.message;
+          reason = m === undefined || m === null ? m : String(m);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
+        onStatusUpdate(attempt, `error: ${reason}`);
       }
     }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts
@@ -0,0 +1,103 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+// KS-1868 (operator 87 screen, anchoring cardano confirmation module): the catch of waitForConfirmation (line 107 of
+// services/anchoring/src/cardano/confirmation.ts) builds the status text with the thrown value's message read INSIDE a
+// template literal, unguarded: `error: ${err?.message}`. A thrown value whose read throws (a revoked Proxy, an Error whose
+// message getter throws) or whose message is a Symbol (a template literal cannot convert a Symbol) makes the catch itself
+// throw, so the whole poll REJECTS on the first such attempt instead of counting the failed attempt and carrying on, as it
+// does for an ordinary Error. The cells make the (stand-in) getTransaction reject with such a value, with a single attempt
+// and a 1 ms delay, and assert the call resolves, counts the failed attempt and reports a status line of text (the constant
+// when the value cannot be turned into text). Harness: the real module with ./provider replaced by a plain stand-in.
+const h = vi.hoisted(() => ({
+  failure: undefined as undefined | { value: unknown },
+}));
+
+vi.mock('../cardano/provider', () => ({
+  getTransaction: async () => {
+    if (h.failure) throw h.failure.value;
+    return { block: 'block-1', block_height: 7, slot: 9 };
+  },
+}));
+
+import { waitForConfirmation } from '../cardano/confirmation';
+
+beforeEach(() => {
+  h.failure = undefined;
+});
+
+type Outcome = { ok: boolean; result: Awaited<ReturnType<typeof waitForConfirmation>> | undefined; statuses: string[] };
+async function poll(failure: { value: unknown } | undefined): Promise<Outcome> {
+  h.failure = failure;
+  const statuses: string[] = [];
+  try {
+    const result = await waitForConfirmation('tx-1', 1, 1, 1, (_attempt, status) => {
+      statuses.push(status);
+    });
+    return { ok: true, result, statuses };
+  } catch {
+    return { ok: false, result: undefined, statuses };
+  }
+}
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 waitForConfirmation counts a failed attempt and reports text for a hostile thrown value', () => {
+  it('control ks1868 C1: a transaction the chain answers is confirmed and no error status is reported', async () => {
+    const r = await poll(undefined);
+    expect(r.ok).toBe(true);
+    expect(r.result?.confirmed).toBe(true);
+    expect(r.result?.errored).toBe(0);
+    expect(r.statuses).toEqual([]);
+  });
+  it('control ks1868 C2: an ordinary Error counts one failed attempt and is reported with its message', async () => {
+    const r = await poll({ value: new Error('net boom') });
+    expect(r.ok).toBe(true);
+    expect(r.result?.confirmed).toBe(false);
+    expect(r.result?.errored).toBe(1);
+    expect(r.statuses).toEqual(['error: net boom']);
+  });
+  it('control ks1868 C3: a thrown plain string counts one failed attempt and is reported without a message', async () => {
+    const r = await poll({ value: 'plain boom' });
+    expect(r.ok).toBe(true);
+    expect(r.result?.errored).toBe(1);
+    expect(r.statuses).toEqual(['error: undefined']);
+  });
+  it('control ks1868 C4: a thrown number counts one failed attempt and is reported without a message', async () => {
+    const r = await poll({ value: 42 });
+    expect(r.ok).toBe(true);
+    expect(r.result?.errored).toBe(1);
+    expect(r.statuses).toEqual(['error: undefined']);
+  });
+  it('RED ks1868 R1: a revoked Proxy counts one failed attempt and is reported as text, as for an ordinary Error', async () => {
+    const r = await poll({ value: revokedProxy() });
+    expect(r.ok).toBe(true);
+    expect(r.result?.errored).toBe(1);
+    expect(r.statuses).toEqual(['error: unreadable thrown value']);
+  });
+  it('RED ks1868 R2: an Error whose message getter throws counts one failed attempt and is reported as text, as for an ordinary Error', async () => {
+    const r = await poll({ value: getterThrows() });
+    expect(r.ok).toBe(true);
+    expect(r.result?.errored).toBe(1);
+    expect(r.statuses).toEqual(['error: unreadable thrown value']);
+  });
+  it('RED ks1868 R3: an Error whose message is a Symbol counts one failed attempt and is reported as text, as for an ordinary Error', async () => {
+    const r = await poll({ value: withMessage(Symbol('ks1868')) });
+    expect(r.ok).toBe(true);
+    expect(r.result?.errored).toBe(1);
+    expect(r.statuses).toEqual(['error: Symbol(ks1868)']);
+  });
+});
```
