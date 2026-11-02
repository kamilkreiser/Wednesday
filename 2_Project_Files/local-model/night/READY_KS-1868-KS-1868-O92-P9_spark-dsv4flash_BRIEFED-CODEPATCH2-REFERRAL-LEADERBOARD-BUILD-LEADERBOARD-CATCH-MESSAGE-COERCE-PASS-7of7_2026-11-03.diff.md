# READY — KS-1868-KS-1868-O92-P9 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 09:00 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:00 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/referral/src/routes/leaderboard.ts } + { Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/referral/src/routes/leaderboard.ts` (product) and `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/referral/src/routes/leaderboard.ts
109	0	Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: leaderboard.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/referral/src/routes/leaderboard.ts`; test(s): `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/referral/src/routes/leaderboard.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts 109 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/referral/src/routes/leaderboard.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the referral leaderboard query catch answers empty and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the query is logged as text and the leaderboard is answered empty, as for an ordinary Error', 'KS-1868 the referral leaderboard query catch answers empty and logs text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol from the query is logged as text and the leaderboard is answered empty, as for an ordinary Error', 'KS-1868 the referral leaderboard query catch answers empty and logs text for a hostile thrown value RED ks1868 R3: an Error whose message getter throws from the query is logged as text and the leaderboard is answered empty, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=36 failed=0 | after: total=41 failed=0` · `NEW reds: []` [baseline_suite.json total=36 failed=0; after_suite.json total=41 failed=0]
- A6 [verbatim]: `PASS A6 whole services/referral suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/referral: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/referral/src/routes/leaderboard.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts` (+109/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/referral/src/routes/leaderboard.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p9_referral_leaderboard_build_leaderboard_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/referral/src/routes/leaderboard.ts b/Blockchain/Dev/services/referral/src/routes/leaderboard.ts
--- a/Blockchain/Dev/services/referral/src/routes/leaderboard.ts
+++ b/Blockchain/Dev/services/referral/src/routes/leaderboard.ts
@@ -283,7 +283,14 @@
       badge: getTierBadge((row.current_tier || 'starter').toUpperCase()),
     }));
   } catch (err: any) {
-    logger.error('Leaderboard DB query failed', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Leaderboard DB query failed', { error: reason });
     return [];
   }
 }
diff --git a/Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts
@@ -0,0 +1,109 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+import http from 'http';
+import type { AddressInfo } from 'net';
+import express from 'express';
+
+// KS-1868 (operator 92 screen, referral leaderboard): the catch of buildLeaderboard (line 285) of services/referral/src/routes/leaderboard.ts passes
+// `err?.message` straight into the logger's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy,
+// an Error whose message getter throws) makes the catch throw, so GET /api/leaderboard (the router mounted here at '/') answers the error path (a 500 from the
+// default handler) where an ordinary Error is logged and the leaderboard is answered empty (200, no entries); an Error whose message is readable but not a
+// string (a Symbol) is handed to the logger uncoerced. The cells make the leaderboard query reject with such a value and assert the empty 200 answer and a
+// logged line that carries text (the constant when the value cannot be turned into text). Harness: the real router mounted on a real express app on 127.0.0.1,
+// a fresh copy of the module per cell (the all-time cache is module state); `../db` and `../utils/logger` are plain stand-ins (no database, no network).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+}));
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { createLogger: () => ({ debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') }) };
+});
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logs.length = 0;
+});
+
+const FAILED = 'Leaderboard DB query failed';
+const LINES = () => h.logs.filter((l) => l.message === FAILED);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string => {
+  const v = l?.meta?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+async function board(value: unknown): Promise<{ status: number; entries: number | undefined } | null> {
+  h.toThrow = value;
+  vi.resetModules();
+  const { leaderboardRoutes } = await import('../routes/leaderboard');
+  const app = express();
+  app.use('/', leaderboardRoutes);
+  const server = http.createServer(app);
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  try {
+    const r = await fetch('http://127.0.0.1:' + (server.address() as AddressInfo).port + '/', { signal: AbortSignal.timeout(1500) });
+    let entries: number | undefined;
+    try {
+      const body = (await r.json()) as { data?: { entries?: unknown[] } };
+      entries = body.data?.entries?.length;
+    } catch {
+      entries = undefined;
+    }
+    return { status: r.status, entries };
+  } catch {
+    return null;
+  } finally {
+    await new Promise<void>((resolve) => server.close(() => resolve()));
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
+describe('KS-1868 the referral leaderboard query catch answers empty and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the leaderboard query is logged with its message and the leaderboard is answered empty', async () => {
+    expect(await board(new Error('db boom'))).toEqual({ status: 200, entries: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('db boom');
+  });
+  it('control ks1868 C2: a thrown plain string is logged without a message and the leaderboard is answered empty', async () => {
+    expect(await board('plain boom')).toEqual({ status: 200, entries: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the query is logged as text and the leaderboard is answered empty, as for an ordinary Error', async () => {
+    expect(await board(revokedProxy())).toEqual({ status: 200, entries: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol from the query is logged as text and the leaderboard is answered empty, as for an ordinary Error', async () => {
+    expect(await board(withMessage(Symbol('ks1868')))).toEqual({ status: 200, entries: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an Error whose message getter throws from the query is logged as text and the leaderboard is answered empty, as for an ordinary Error', async () => {
+    expect(await board(getterThrows())).toEqual({ status: 200, entries: 0 });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+});
```
