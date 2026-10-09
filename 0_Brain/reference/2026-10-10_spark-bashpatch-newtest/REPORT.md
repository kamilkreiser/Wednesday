# Spark bash_patch: KS-1456 control failed at B5 (2026-10-10)

## FOUND
Neither hypothesis as stated. The cause is a third thing: the checker's SECTION SPLITTER (checker.sh lines 85-101).
It cuts sections at `--- ` lines only, so the git preamble of the NEXT file (`diff --git`, `new file mode 100644`,
`index 0000000..0ef305a`) lands at the TAIL of the previous section. In the KS-1456 golden the product hunk comes first, so
section_1.diff (lines 15-17) ended with a header-only "create the test file" fragment, and section_2.diff began at
`--- /dev/null`. B2 passed (both apply at the tip); B4 applied section_2 (wrote the test); B5 applied section_1 (the
product), and its tail fragment tried to create the test file again: "already exists in working directory".
- H1 (B5 re-applies the whole patch / test again): NOT as stated. B5 (line 443 after the fix) applies PROD_SEC only, as
  intended; the defect is that PROD_SEC carried the test file's creation header. code_patch needs no mirroring.
- H2 (mode header 100644 vs 100755): REFUTED. The same warning is printed in the PASSING run (apply_product.out of
  control-r2): `warning: ...run-migrations.sh has type 100755, expected 100644`, and the apply succeeds. Golden left unchanged.
Why no earlier bash_patch control hit it: the other passing bash_patch goldens (KS-1355, KS-1139, KS-1136, KS-1274) have no
`diff --git` lines; KS-1456 is the first git-form golden with a modify-then-new-file order.

## FIX
Peel trailing preamble lines (and blanks) off every section except the last into section_N.diff.peeled (kept, not lost).
The `--- /dev/null` header still implies the add. Diff: checker.diff beside this file (reproduced below).
Files changed:
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/bash_patch/checker.sh  3ffbb77e72d9 -> 7e5634d0ce13 (backup: checker.sh.pre-1010-bashnewtest)
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tests/bash_patch_newtest_arms.sh  new, 0558c3816ae6
Not running when edited (pgrep checker.sh/round.sh: none). Nothing committed or deleted.

## TESTED (arms; verbatim verdicts, from tests/bash_patch_newtest_arms.sh)
```
ARM1 (new-file test, product hunk FIRST (the fix)): SPARK ROUND KS-1456-run-migrations-failed-run-message: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 613070f29112 · 26s round, no model (control) · /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/lo
ARM2a (test_mode=modify, no regression): SPARK ROUND KS-1355-stack-guard-one-line-per-project: REFUSED — STALE BRIEF: written at 4eaf7741a6a4, and by develop 613070f29112 these changed: Blockchain/Dev/scripts/__tests__/stack_guard.test.sh Blockchain/Dev/scripts/stack_gua
ARM2b (new-file test, no git preamble, no regression): SPARK ROUND KS-1139-smoke-test-counters-errexit: REFUSED — STALE BRIEF: written at 2c27ddfeef51, and by develop 613070f29112 these changed: Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh Blockchain/De
ARM2c PASS (earlier bash_patch control, test_mode=modify (an existing test MODIFIED), new checker; rc=0): RESULT: PASS (7/7) at tip 147ae442074c
ARM2d PASS (earlier bash_patch control, new-file test, no git preamble, new checker; rc=0): RESULT: PASS (7/7) at tip 2c27ddfeef51
ARM3 PASS (product hunk leaves the counts-skips text: new test stays red; rc=1): FAIL B5 GREEN-AFTER: still red after the script hunk (rc=1, 1 FAIL line(s), load_error=0): FAIL: the failed-run output still names the closed defect: the remaining applied=N-counts-skips defect·
ARM4a PASS (malformed test hunk header refused; rc=1): FAIL B2 section_2.diff does NOT apply at the tip: strict: error: No valid patches in input (allow with "--allow-empty")  | reanchored:  
ARM4b PASS (test with a syntax error refused at B4; rc=1): FAIL B4 the new test does not parse (bash -n): /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-10_KS-1456-run-migrations-failed-run-message-control-r4_061804/clone/Blockchain/Dev/scr
scratch (kept): /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/45262932-2aa6-4254-821d-057e81431f6a/scratchpad/arms2
```
Pre-fix control (the red side): run spark_secuura_2026-10-10_KS-1456-...-control checker.out: `FAIL B5 the script hunk did not apply ... already exists`.
Post-fix: run ...-control-r2: `RESULT: PASS (7/7)`, `SPARK RESULT: PASS`, golden byte-identical.

## HOW (with controls)
- Arm 1: round.sh --control on the KS-1456 brief (no model). Control for the arm: the same golden FAILED before the fix.
- Arm 2: briefs KS-1355 (test_mode=modify) and KS-1139 (new file) are STALE at today's develop (2a/2b REFUSED at the
  stale-brief gate; allow_drift=1 then refuses in the builder), so no-regression is shown by 2c/2d: the SAVED 10-07 golden
  outputs replayed through the new checker in a scratch shared clone at each run's own tip, both 7/7.
- Arm 3: golden plus one extra `+` line re-adding "the remaining applied=N-counts-skips defect" (header count bumped):
  passes B3b (must_change `-` line and brief `+` line present), then B5 correctly stays red.
- Arm 4: 4a test hunk header `@@ garbage @@` refused at B2; 4b test with a syntax error refused at B4.

## NOT TESTED
- Peeling when the new-file test comes first and a git-form product section follows (its preamble stays at the head of
  that section, as before; not exercised).
- Pure rename/mode-change sections (preamble-only sections) are not a bash_patch shape; not exercised.
- bash_patch2 (different checker.sh under tasks/bash_patch2) shares this splitter pattern? NOT inspected; check it if
  a git-form modify-then-new-file golden is used there.
- A live model round.

## DESIGN LIMIT (not fixed, for Wednesday)
The bash_patch builder REFUSES prose-only (loose, rung 6) briefs ("no fenced '+' lines"), so rung 6 cannot run on bash tickets.
(Observed while preparing: KS-1456-run-migrations-failed-run-message-loose is in night/briefs.)

## EXACT DIFF
```diff
--- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/bash_patch/checker.sh.pre-1010-bashnewtest	2026-10-10 06:14:43
+++ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/bash_patch/checker.sh	2026-10-10 06:14:47
@@ -96,8 +96,20 @@
     cur["lines"].append(ln)
     if ln.startswith("+++ ") and cur["path"] is None:
         cur["path"]=re.sub(r"^\+\+\+ (b/)?","",ln).strip()
+# 2026-10-10 (bashnewtest, KS-1456 control): the split is at `--- ` lines, so the git PREAMBLE of the NEXT file
+# (`diff --git` / `new file mode` / `index` ...) lands at the TAIL of the previous section. For a modify-then-new-file
+# patch that tail is a header-only "create this file" fragment: B5 applying the product section re-created the test
+# file B4 had already written ("already exists"). Peel the trailing preamble off every section but the last-opened
+# one's own head (kept beside as section_N.diff.peeled, never lost); the `--- /dev/null` header still implies the add.
+PRE=re.compile(r"^(diff --git |index [0-9a-f]+\.\.[0-9a-f]+|new file mode |deleted file mode |old mode |new mode |similarity index |rename (from|to) |copy (from|to) )")
+for k in range(len(secs)-1):
+    L=secs[k]["lines"]; moved=[]
+    while L and (L[-1].strip()=="" or PRE.match(L[-1])):
+        moved.append(L.pop())
+    secs[k]["peeled"]=[m for m in reversed(moved) if m.strip()]
 out=[]
 for i,s in enumerate(secs,1):
+    if s.get("peeled"): open(f"{rep}/section_{i}.diff.peeled","w",encoding="utf-8").write("\n".join(s["peeled"])+"\n")
     p=f"{rep}/section_{i}.diff"; open(p,"w",encoding="utf-8").write("\n".join(s["lines"]).rstrip("\n")+"\n"); out.append({"path":s["path"],"file":p})
 json.dump(out,open(f"{rep}/sections.json","w"))
 print("sections:",[o["path"] for o in out])
```
