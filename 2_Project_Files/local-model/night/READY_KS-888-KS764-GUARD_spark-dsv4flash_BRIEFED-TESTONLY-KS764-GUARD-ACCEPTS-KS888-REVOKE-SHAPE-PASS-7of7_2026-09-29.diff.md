# READY — KS-764 GUARD vs the KS-888 revoke shape (spark-dsv4flash, briefed, test-only, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-764-GUARD-KS888-SHAPE/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape/KS-888.golden.diff` (`cmp` rc 0; a mutated-golden control rc 1), measured by Wednesday.

**Held BY HAND at 00:42 2026-09-29 by Wednesday overnight seat 24014037** (hold_ready.py cannot hold a test-only run on this input; the owed defect). Source develop **3d706c21f65e** (#1331, docs only; the Dev tree is identical to db8d85dcd).

- **Why:** #1327 (KS-888 revoke, Kam-ruled default a, merged on gate37) put a comment block and a `try {` between `apiKey.isActive = false;` and `await dbSaveApiKey(`, so the packages/shared KS-764 guard's 80-character window stopped matching. Develop has carried 1 failed / 945 since then (Seat B 40th bisected it; Wednesday confirmed it with a python regex over four revisions). The product is correct; only the guard changes.
- **The fix:** both copies of the pattern (`:77` CALL_SITES, `:97` REVOKE_WRITES) admit only whitespace, whole `//` lines and one optional `try {`, so a statement in between, a moved, deleted or commented-out save, or an early return still reds the guard (the brief-writer's five arms). A loose `{0,2000}` window was measured green even with the save deleted, so it was rejected.
- **Ticket:** the files are named KS-888 because KS-764 is archived (build_input refused it). The PR Refs KS-888 (the change that caused the red) and names KS-764 in its body. No closing keyword.
- **For the gate:** `startup-migrations.ts` is on this guard's allowlist, so run the guard on any branch that touches it (Seat B 40th's KS-1054).
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 (test-only) touched-file set == { Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts } — the product file is untouched, as the ticket requires`
  - `PASS A3c every '+' line the brief adds is in the product hunk (9 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks764-key-revoke-call-site-guard.test.ts fails at the untouched tip (2 failed / 15 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks764-key-revoke-call-site-guard.test.ts passes with the product hunk (15 passed / 15 run)`
  - `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=1 +9/-2 test=src/__tests__/ks764-key-revoke-call-site-guard.test.ts red_first=yes apply_mode=strict`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts
@@ -76,3 +76,10 @@
     // enough to mean nothing, so each site names its own write.
-    revokeWrite: /isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(/,
+    // KS-888 (#1327) put a comment block and a try between the flip and the
+    // save, which an 80-character window could not span. Between the two this
+    // admits ONLY whitespace, whole // comment lines and one try {, so a
+    // statement in between, or a save that is moved, deleted or commented out,
+    // turns the guard red. [^!-~] is any character that is not visible ASCII,
+    // which here means whitespace; [/] [{] [(] are those literal characters;
+    // ^ under the m flag is the start of a line.
+    revokeWrite: /isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m,
   },
@@ -96,3 +103,3 @@
   /UPDATE\s+svc_api_keys\s+SET\s+is_active\s*=\s*false/i,
-  /isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(/,
+  /isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m,
 ];
```
