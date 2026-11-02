# READY — KS-1868-KS-1868-O85-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 23:39 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 23:39 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1584c0f0ff808fddf35245bee41b6b5f9231054c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/reconciler.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/reconciler.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/anchoring/src/reconciler.ts
182	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: reconciler.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/reconciler.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/reconciler.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts 182 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/reconciler.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (8 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=8 of total=12; red cell(s): ['KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R1 chain check: a rejection that is a revoked Proxy is logged as text, as for an ordinary Error, and row 2 is still confirmed', 'KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R2 chain check: a rejection that is an Error whose message getter throws is logged as text, as for an ordinary Error, and row 2 is still confirmed', 'KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R3 chain check: a rejection that is an Error whose message is a null-prototype object is logged as text, as for an ordinary Error, and row 2 is still confirmed', 'KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R4 chain check: a rejection that is an Error whose message is a Symbol is logged as text, as for an ordinary Error, and row 2 is still confirmed', 'KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R5 the SELECT: a rejection that is a revoked Proxy is logged as text and the pass resolves, as for an ordinary Error', 'KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R6 the SELECT: a rejection that is an Error whose message is a Symbol is logged as text and the pass resolves, as for an ordinary Error', 'KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R7 the SELECT: a rejection that is an Error whose message getter throws is logged as text and the pass resolves, as for an ordinary Error', 'KS-1868 the reconciler catches carry on and log text for a hostile thrown value RED ks1868 R8 the SELECT: a rejection that is an Error whose message is a null-prototype object is logged as text and the pass resolves, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=760 failed=1 | after: total=772 failed=1` · `NEW reds: []` [baseline_suite.json total=760 failed=1; after_suite.json total=772 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/reconciler.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts` (+182/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/reconciler.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1584c0f0ff808fddf35245bee41b6b5f9231054c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p2_anchoring_reconciler_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/reconciler.ts b/Blockchain/Dev/services/anchoring/src/reconciler.ts
--- a/Blockchain/Dev/services/anchoring/src/reconciler.ts
+++ b/Blockchain/Dev/services/anchoring/src/reconciler.ts
@@ -403,7 +403,14 @@
           // the "could not ask" branch above decides it (never failed, KS-1810). A rejection
           // here leaves the row for the next pass and is not counted. Never guess.
           answeredMisses.delete(key);
-          deps.log('warn', 'Reconciler: chain check errored; leaving row as-is', { anchorId: row.id, error: err?.message });
+          let reason: string | null | undefined;
+          try {
+            const m = err?.message;
+            reason = m === undefined || m === null ? m : String(m);
+          } catch {
+            reason = 'unreadable thrown value';
+          }
+          deps.log('warn', 'Reconciler: chain check errored; leaving row as-is', { anchorId: row.id, error: reason });
         }
       }
       if (now() - startedAt >= SWEEP_BOOT_GRACE_MS) await sweepNullHashRows(out);
@@ -411,7 +418,14 @@
         deps.log('info', 'Reconciler pass complete (KS-584)', { ...out });
       }
     } catch (err: any) {
-      deps.log('warn', 'Reconciler pass failed', { error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      deps.log('warn', 'Reconciler pass failed', { error: reason });
     } finally {
       running = false;
     }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts
@@ -0,0 +1,182 @@
+import { describe, it, expect, vi } from 'vitest';
+import { createStuckAnchorReconciler, type ReconcilerDeps } from '../reconciler';
+
+// KS-1868 (operator 85 screen, anchoring reconciler): the per-row chain-check catch (line 406) and the whole-pass catch
+// (line 414) of services/anchoring/src/reconciler.ts log `{ error: err?.message }` with the read INSIDE the log call's
+// arguments, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the
+// catch itself throw: the row loop is abandoned, the outer catch throws again, and reconcileStuckAnchors REJECTS although a
+// pass is meant never to throw; the rows after the failing one are skipped. An Error whose message is readable but not a
+// string is handed to the log as is. The cells make the chain check (row 1) or the row SELECT reject with such a value and
+// assert the pass resolves, the line is logged as text (the constant when the value cannot be turned into text) and, for the
+// chain check, row 2 is still confirmed exactly as after an ordinary Error. Harness: the real reconciler with plain-function
+// dependencies (no database, no chain, no module mocks).
+const TX1 = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
+const TX2 = '94fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c4';
+const HOUR = 3_600_000;
+const CONFIG = { minAgeMs: 10 * 60_000, giveUpMs: 24 * HOUR, batch: 25 };
+
+const row = (id: string, tx: string) => ({
+  id,
+  transaction_hash: tx,
+  created_at: '2026-08-11T09:00:00Z',
+  updated_at: '2026-08-11T09:00:00Z',
+});
+
+type Setup = { rows?: unknown[]; selectThrows?: unknown; checkThrows?: unknown };
+function build(s: Setup) {
+  const logged: unknown[][] = [];
+  const updates: Array<{ id: string; updates: Record<string, unknown> }> = [];
+  const deps: ReconcilerDeps = {
+    isDbAvailable: () => true,
+    isCardanoReady: () => true,
+    query: async () => {
+      if ('selectThrows' in s) return Promise.reject(s.selectThrows);
+      return { rows: s.rows ?? [] };
+    },
+    checkTx: async (tx: string) => {
+      if (tx === TX1 && 'checkThrows' in s) return Promise.reject(s.checkThrows);
+      return { confirmed: true, blockNumber: 4547897, blockHash: 'bh', slot: 123, confirmations: 1 };
+    },
+    updateStatus: async (id: string, u: Record<string, unknown>) => {
+      updates.push({ id, updates: u });
+      return 1;
+    },
+    log: (...args: unknown[]) => {
+      logged.push(args);
+    },
+    now: () => new Date('2026-08-11T12:00:00Z').getTime(),
+    isDriven: () => false,
+    scanWallet: async () => ({ outcome: 'complete' as const, scanned: 0, matches: [] }),
+  } as unknown as ReconcilerDeps;
+  return { deps, logged, updates };
+}
+
+async function runPass(s: Setup): Promise<{ ok: boolean; logged: unknown[][]; updates: Array<{ id: string; updates: Record<string, unknown> }> }> {
+  const { deps, logged, updates } = build(s);
+  try {
+    await createStuckAnchorReconciler(deps, CONFIG)();
+    return { ok: true, logged, updates };
+  } catch {
+    return { ok: false, logged, updates };
+  }
+}
+
+const CHECK = 'Reconciler: chain check errored; leaving row as-is';
+const PASS = 'Reconciler pass failed';
+const LINES = (logged: unknown[][], msg: string) => logged.filter((c) => c[1] === msg);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[2] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+const confirmedIds = (u: Array<{ id: string; updates: Record<string, unknown> }>) =>
+  u.filter((x) => x.updates.status === 'confirmed').map((x) => x.id);
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
+const SHAPES: Array<[string, () => unknown, string]> = [
+  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
+  ['an Error whose message getter throws', getterThrows, 'unreadable thrown value'],
+  ['an Error whose message is a null-prototype object', () => withMessage(Object.create(null)), 'unreadable thrown value'],
+  ['an Error whose message is a Symbol', () => withMessage(Symbol('ks1868')), 'Symbol(ks1868)'],
+];
+const TWO = () => [row('anchor-1', TX1), row('anchor-2', TX2)];
+
+describe('KS-1868 the reconciler catches carry on and log text for a hostile thrown value', () => {
+  it('control ks1868 C1 chain check: an ordinary Error on row 1 is logged with its message and row 2 is still confirmed', async () => {
+    const r = await runPass({ rows: TWO(), checkThrows: new Error('blockfrost 429') });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, CHECK)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, CHECK)[0])).toBe('blockfrost 429');
+    expect(confirmedIds(r.updates)).toEqual(['anchor-2']);
+  });
+  it('control ks1868 C2 the SELECT: an ordinary Error is logged with its message and the pass resolves', async () => {
+    const r = await runPass({ selectThrows: new Error('connection terminated') });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, PASS)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, PASS)[0])).toBe('connection terminated');
+    expect(r.updates).toHaveLength(0);
+  });
+  it('control ks1868 C3 chain check: a thrown plain string has no message, is logged with no error, as before, and row 2 is confirmed', async () => {
+    const r = await runPass({ rows: TWO(), checkThrows: 'plain boom' });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, CHECK)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, CHECK)[0])).toBe('<undefined>');
+    expect(confirmedIds(r.updates)).toEqual(['anchor-2']);
+  });
+  it('control ks1868 C4 no failure: both rows are confirmed and nothing is logged as an error line', async () => {
+    const r = await runPass({ rows: TWO() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, CHECK)).toHaveLength(0);
+    expect(confirmedIds(r.updates)).toEqual(['anchor-1', 'anchor-2']);
+  });
+  it('RED ks1868 R1 chain check: a rejection that is a revoked Proxy is logged as text, as for an ordinary Error, and row 2 is still confirmed', async () => {
+    const r = await runPass({ rows: TWO(), checkThrows: SHAPES[0][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, CHECK)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, CHECK)[0])).toBe(SHAPES[0][2]);
+    expect(confirmedIds(r.updates)).toEqual(['anchor-2']);
+  });
+  it('RED ks1868 R2 chain check: a rejection that is an Error whose message getter throws is logged as text, as for an ordinary Error, and row 2 is still confirmed', async () => {
+    const r = await runPass({ rows: TWO(), checkThrows: SHAPES[1][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, CHECK)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, CHECK)[0])).toBe(SHAPES[1][2]);
+    expect(confirmedIds(r.updates)).toEqual(['anchor-2']);
+  });
+  it('RED ks1868 R3 chain check: a rejection that is an Error whose message is a null-prototype object is logged as text, as for an ordinary Error, and row 2 is still confirmed', async () => {
+    const r = await runPass({ rows: TWO(), checkThrows: SHAPES[2][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, CHECK)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, CHECK)[0])).toBe(SHAPES[2][2]);
+    expect(confirmedIds(r.updates)).toEqual(['anchor-2']);
+  });
+  it('RED ks1868 R4 chain check: a rejection that is an Error whose message is a Symbol is logged as text, as for an ordinary Error, and row 2 is still confirmed', async () => {
+    const r = await runPass({ rows: TWO(), checkThrows: SHAPES[3][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, CHECK)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, CHECK)[0])).toBe(SHAPES[3][2]);
+    expect(confirmedIds(r.updates)).toEqual(['anchor-2']);
+  });
+  it('RED ks1868 R5 the SELECT: a rejection that is a revoked Proxy is logged as text and the pass resolves, as for an ordinary Error', async () => {
+    const r = await runPass({ selectThrows: SHAPES[0][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, PASS)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, PASS)[0])).toBe(SHAPES[0][2]);
+    expect(r.updates).toHaveLength(0);
+  });
+  it('RED ks1868 R6 the SELECT: a rejection that is an Error whose message is a Symbol is logged as text and the pass resolves, as for an ordinary Error', async () => {
+    const r = await runPass({ selectThrows: SHAPES[3][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, PASS)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, PASS)[0])).toBe(SHAPES[3][2]);
+    expect(r.updates).toHaveLength(0);
+  });
+  it('RED ks1868 R7 the SELECT: a rejection that is an Error whose message getter throws is logged as text and the pass resolves, as for an ordinary Error', async () => {
+    const r = await runPass({ selectThrows: SHAPES[1][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, PASS)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, PASS)[0])).toBe(SHAPES[1][2]);
+    expect(r.updates).toHaveLength(0);
+  });
+  it('RED ks1868 R8 the SELECT: a rejection that is an Error whose message is a null-prototype object is logged as text and the pass resolves, as for an ordinary Error', async () => {
+    const r = await runPass({ selectThrows: SHAPES[2][1]() });
+    expect(r.ok).toBe(true);
+    expect(LINES(r.logged, PASS)).toHaveLength(1);
+    expect(reasonOf(LINES(r.logged, PASS)[0])).toBe(SHAPES[2][2]);
+    expect(r.updates).toHaveLength(0);
+  });
+});
```
