# READY — KS-1818-KS-1818-LOGGERGUARD (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1818_p1_logger_guard/out.md.checker/patch.diff`** (from `ls` at 01:45 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1818_p1_logger_guard/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1818_p1_logger_guard/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 01:45 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1818_p1_logger_guard/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/adminConfig.ts , Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	1	Blockchain/Dev/services/originate/src/routes/adminConfig.ts
18	0	Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/adminConfig.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts fails at the untouched tip (2 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=2 of total=8; red cell(s): ['KS-1802: seed-demo-users keeps going when a user insert throws a hostile value RED KS-1818 R4: a logger that throws on every failed insert is reported as 14 failed, not as the constant 500', 'KS-1802: seed-demo-users keeps going when a user insert throws a hostile value RED KS-1818 R5: one failed insert whose log line throws does not stop the other 13 from being seeded']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1818 failed=0 | after: total=1820 failed=0` · `NEW reds: []` [baseline_suite.json total=1818 failed=0; after_suite.json total=1820 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +23/-1 test=src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+5/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (+18/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1818_p1_logger_guard/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1818_p1_logger_guard/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -2118,6 +2118,10 @@
         // DO NOTHING a conflict is no longer an exception, so anything reaching
         // here is a real failure and was being swallowed silently.
         failed++;
-        logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) });
+        // KS-1818: readableErrorMessage guards the message READ; the logger call after it sat directly in this catch, so a logger (or a serialiser) that throws left the catch, ended the loop
+        // at this user and reached the route's outer catch (the KS-1802 hang class). Log in a try of its own, as fail500 and migrate-tenant-data do; the loop goes on with the next user.
+        try { logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) }); } catch {
+          // Nothing more can be said if the logger itself fails; the failure is already counted and the next user is still attempted.
+        }
       }
     }
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
@@ -112,3 +112,21 @@
+  // KS-1818: R1-R3 make the thrown VALUE hostile; these two make the LOGGER throw. The logger call after readableErrorMessage sat outside any guard.
+  it('RED KS-1818 R4: a logger that throws on every failed insert is reported as 14 failed, not as the constant 500', async () => {
+    mockLogError.mockImplementation(() => {
+      throw new Error('ks1818 logger down');
+    });
+    mockExecuteRaw.mockRejectedValue(new Error('ks1818 insert'));
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
+    expect(mockLogError).toHaveBeenCalledTimes(USERS);
+  });
+
+  it('RED KS-1818 R5: one failed insert whose log line throws does not stop the other 13 from being seeded', async () => {
+    mockLogError.mockImplementation(() => {
+      throw new Error('ks1818 logger down');
+    });
+    mockExecuteRaw.mockRejectedValueOnce(new Error('ks1818 insert')).mockResolvedValue(1);
+    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 13, created: 13, alreadyPresent: 0, failed: 1 } });
+  });
+
   it('control KS-1802 C1: an ordinary Error on every insert is reported as 14 failed and its message is logged', async () => {
     mockExecuteRaw.mockRejectedValue(new Error('ks1802 ordinary'));
     expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
```
