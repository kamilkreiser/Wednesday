# READY — KS-1868-KS-1868-O96-P8 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/out.md.checker/patch.diff`** (from `ls` at 16:08 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:08 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
72	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: event-indexer.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts 72 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 ContractEventIndexer.handleError reads a thrown value safely RED ks1868 R1 a revoked Proxy is handed to onError as an Error with a constant reason', 'KS-1868 ContractEventIndexer.handleError reads a thrown value safely RED ks1868 R2 an object whose toString throws is handed to onError as an Error with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1447 failed=1 | after: total=1451 failed=1` · `NEW reds: []` [baseline_suite.json total=1447 failed=1; after_suite.json total=1451 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts` (+72/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p8_shared_event_indexer_handle_error_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts b/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
--- a/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
+++ b/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
@@ -343,5 +343,10 @@
   private handleError(err: any): void {
-    const error = err instanceof Error ? err : new Error(String(err));
+    let error: Error;
+    try {
+      error = err instanceof Error ? err : new Error(String(err));
+    } catch {
+      error = new Error('unreadable thrown value');
+    }
     if (this.options.onError) {
       this.options.onError(error);
     } else {
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-event-indexer-handle-error-unreadable-throw.test.ts
@@ -0,0 +1,72 @@
+import { describe, it, expect } from 'vitest';
+
+// KS-1868: ContractEventIndexer.handleError (src/blockchain/event-indexer.ts) turns every non-fatal polling failure into an
+// Error and hands it to the `onError` callback. It reads the value as `err instanceof Error ? err : new Error(String(err))`,
+// unguarded. When the value cannot be read (a revoked Proxy throws on `instanceof`; an object whose toString throws, throws
+// in String()) handleError itself throws, so the polling loop's catch sites throw and `onError` is never called. The
+// callback is a plain function that records what it is given; handleError is private and is reached through a type cast;
+// no network.
+import { ContractEventIndexer } from '../blockchain/event-indexer';
+
+type Outcome = { threw: boolean; received: unknown[] };
+
+function run(value: unknown): Outcome {
+  const received: unknown[] = [];
+  const indexer = new ContractEventIndexer({
+    onError: (e: Error) => {
+      received.push(e);
+    },
+  } as never);
+  let threw = false;
+  try {
+    (indexer as unknown as { handleError(v: unknown): void }).handleError(value);
+  } catch {
+    threw = true;
+  }
+  return { threw, received };
+}
+
+const messageOf = (o: Outcome): unknown => (o.received[0] as { message?: unknown } | undefined)?.message;
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const toStringThrows = (): unknown => ({
+  toString() {
+    throw new Error('toString boom');
+  },
+});
+
+describe('KS-1868 ContractEventIndexer.handleError reads a thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error is handed to onError as is', () => {
+    const err = new Error('rpc down');
+    const out = run(err);
+    expect(out.threw).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(out.received[0] === err).toBe(true);
+  });
+
+  it('control ks1868 C2 a thrown plain string is handed to onError as an Error with that text', () => {
+    const out = run('plain text failure');
+    expect(out.threw).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(messageOf(out)).toBe('plain text failure');
+  });
+
+  it('RED ks1868 R1 a revoked Proxy is handed to onError as an Error with a constant reason', () => {
+    const out = run(revokedProxy());
+    expect(out.threw).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(messageOf(out)).toBe('unreadable thrown value');
+  });
+
+  it('RED ks1868 R2 an object whose toString throws is handed to onError as an Error with a constant reason', () => {
+    const out = run(toStringThrows());
+    expect(out.threw).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(messageOf(out)).toBe('unreadable thrown value');
+  });
+});
```
