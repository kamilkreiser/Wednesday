# READY — KS-1868-KS-1868-O87-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 01:34 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 01:34 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	2	Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts
145	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (9 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: threadTokenIndex.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts 9 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts 145 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=5 of total=9; red cell(s): ['KS-1868 loadActiveRegistry degrades or rethrows the original value and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy in non-strict mode resolves [] and is logged as text, as for an ordinary Error', 'KS-1868 loadActiveRegistry degrades or rethrows the original value and logs text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws in non-strict mode resolves [] and is logged as text, as for an ordinary Error', 'KS-1868 loadActiveRegistry degrades or rethrows the original value and logs text for a hostile thrown value RED ks1868 R3: an Error whose message is a Symbol in non-strict mode resolves [] and is logged as text, as for an ordinary Error', 'KS-1868 loadActiveRegistry degrades or rethrows the original value and logs text for a hostile thrown value RED ks1868 R4: a revoked Proxy in strict mode is logged as text and rethrown as the same object, as for an ordinary Error', 'KS-1868 loadActiveRegistry degrades or rethrows the original value and logs text for a hostile thrown value RED ks1868 R5: an Error whose message getter throws in strict mode is logged as text and rethrown as the same object, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=760 failed=1 | after: total=769 failed=1` · `NEW reds: []` [baseline_suite.json total=760 failed=1; after_suite.json total=769 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts` (+9/-2 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts` (+145/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8150eeb3802bd9cfe5242ffbc49278c1a3739a84` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o87_p4_anchoring_thread_token_index_load_registry_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts b/Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts
--- a/Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts
+++ b/Blockchain/Dev/services/anchoring/src/cardano/threadTokenIndex.ts
@@ -73,14 +73,21 @@
     // The migration may not have run in older environments. Silently degrade
     // to the metadata-label path — STRICT_THREAD_TOKEN_INDEX flips this to a
     // hard error when the migration is mandatory.
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     if (STRICT_MODE) {
       logger.error('state_thread_registry unavailable in STRICT mode', {
-        error: err?.message,
+        error: reason,
       });
       throw err;
     }
     logger.debug('state_thread_registry not available — falling back to metadata-only', {
-      error: err?.message,
+      error: reason,
     });
     return [];
   }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts
@@ -0,0 +1,145 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 87 screen, anchoring thread-token index): the catch of loadActiveRegistry (lines 78 and 83 of
+// services/anchoring/src/cardano/threadTokenIndex.ts) pass `err?.message` straight into the logger's meta object in BOTH
+// branches (STRICT_THREAD_TOKEN_INDEX true: log and rethrow; false: log at debug and answer the empty registry),
+// unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch itself
+// throw: the call rejects with that read error instead of resolving [] (non-strict) or rethrowing the ORIGINAL value
+// (strict); an Error whose message is not a string (a Symbol) is passed to the logger uncoerced. The cells make the registry
+// query reject with such a value and assert the non-strict call resolves [] and the strict call rejects with the original
+// value, with the logged value text (the constant when the value cannot be turned into text). Harness: the real module with
+// the db module, the logger and @secuura/shared replaced by plain stand-ins (no database); STRICT_MODE is read when the
+// module loads, so each cell loads a fresh copy under the environment it needs.
+const h = vi.hoisted(() => ({
+  failure: undefined as undefined | { value: unknown },
+  lines: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  query: async () => {
+    if (h.failure) throw h.failure.value;
+    return { rows: [{ document_id: 'doc-1', policy_id: 'pol-1', network: 'preprod', status: 'active' }] };
+  },
+}));
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.lines.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+vi.mock('@secuura/shared', () => ({
+  utxoCarriesThreadToken: () => false,
+  selectThreadTokenUtxos: () => [],
+}));
+
+type Idx = typeof import('../cardano/threadTokenIndex');
+const realStrict = process.env.STRICT_THREAD_TOKEN_INDEX;
+afterAll(() => {
+  if (realStrict === undefined) delete process.env.STRICT_THREAD_TOKEN_INDEX;
+  else process.env.STRICT_THREAD_TOKEN_INDEX = realStrict;
+});
+beforeEach(() => {
+  h.failure = undefined;
+  h.lines.length = 0;
+});
+
+async function load(strict: boolean): Promise<Idx> {
+  process.env.STRICT_THREAD_TOKEN_INDEX = strict ? 'true' : 'false';
+  vi.resetModules();
+  return import('../cardano/threadTokenIndex');
+}
+type Outcome = { settled: 'resolved' | 'rejected'; value: unknown };
+async function call(strict: boolean, failure: { value: unknown } | undefined): Promise<Outcome> {
+  h.failure = failure;
+  const idx = await load(strict);
+  try {
+    return { settled: 'resolved', value: await idx.loadActiveRegistry('preprod' as never) };
+  } catch (e) {
+    return { settled: 'rejected', value: e };
+  }
+}
+const DEBUG_MSG = 'state_thread_registry not available — falling back to metadata-only';
+const STRICT_MSG = 'state_thread_registry unavailable in STRICT mode';
+const lineOf = (message: string): { level: string; message: string; meta: Record<string, unknown> | undefined }[] =>
+  h.lines.filter((l) => l.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string =>
+  typeof l?.meta?.error === 'string' ? (l.meta.error as string) : '<' + typeof l?.meta?.error + '>';
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
+describe('KS-1868 loadActiveRegistry degrades or rethrows the original value and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: a registry that reads resolves its entries and logs no failure', async () => {
+    const r = await call(false, undefined);
+    expect(r).toEqual({ settled: 'resolved', value: [{ documentId: 'doc-1', policyId: 'pol-1' }] });
+    expect(lineOf(DEBUG_MSG)).toHaveLength(0);
+  });
+  it('control ks1868 C2: an ordinary Error in non-strict mode resolves [] and is logged at debug with its message', async () => {
+    const r = await call(false, { value: new Error('registry boom') });
+    expect(r).toEqual({ settled: 'resolved', value: [] });
+    expect(lineOf(DEBUG_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(DEBUG_MSG)[0])).toBe('registry boom');
+  });
+  it('control ks1868 C3: a thrown plain string in non-strict mode resolves [] and is logged without a message', async () => {
+    const r = await call(false, { value: 'plain boom' });
+    expect(r).toEqual({ settled: 'resolved', value: [] });
+    expect(lineOf(DEBUG_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(DEBUG_MSG)[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C4: an ordinary Error in strict mode is logged with its message and rethrown as the same object', async () => {
+    const err = new Error('registry boom');
+    const r = await call(true, { value: err });
+    expect(r.settled).toBe('rejected');
+    expect(r.value).toBe(err);
+    expect(lineOf(STRICT_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(STRICT_MSG)[0])).toBe('registry boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy in non-strict mode resolves [] and is logged as text, as for an ordinary Error', async () => {
+    const r = await call(false, { value: revokedProxy() });
+    expect(r).toEqual({ settled: 'resolved', value: [] });
+    expect(lineOf(DEBUG_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(DEBUG_MSG)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws in non-strict mode resolves [] and is logged as text, as for an ordinary Error', async () => {
+    const r = await call(false, { value: getterThrows() });
+    expect(r).toEqual({ settled: 'resolved', value: [] });
+    expect(lineOf(DEBUG_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(DEBUG_MSG)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an Error whose message is a Symbol in non-strict mode resolves [] and is logged as text, as for an ordinary Error', async () => {
+    const r = await call(false, { value: withMessage(Symbol('ks1868')) });
+    expect(r).toEqual({ settled: 'resolved', value: [] });
+    expect(lineOf(DEBUG_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(DEBUG_MSG)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R4: a revoked Proxy in strict mode is logged as text and rethrown as the same object, as for an ordinary Error', async () => {
+    const value = revokedProxy();
+    const r = await call(true, { value });
+    expect(r.settled).toBe('rejected');
+    expect(r.value === value).toBe(true);
+    expect(lineOf(STRICT_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(STRICT_MSG)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an Error whose message getter throws in strict mode is logged as text and rethrown as the same object, as for an ordinary Error', async () => {
+    const value = getterThrows();
+    const r = await call(true, { value });
+    expect(r.settled).toBe('rejected');
+    expect(r.value === value).toBe(true);
+    expect(lineOf(STRICT_MSG)).toHaveLength(1);
+    expect(reasonOf(lineOf(STRICT_MSG)[0])).toBe('unreadable thrown value');
+  });
+});
```
