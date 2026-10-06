# READY — KS-1355-STACK-GUARD-ONE-LINE-PER-PROJECT-1 (Spark DeepSeek V4 Flash, briefed; label corrected by Wednesday 2026-10-06, hold_ready.py has no --model-tag for bash_patch, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project/out.md.checker/patch.diff`** (from `ls` at 12:58 2026-10-06; sha256[:16] 7096be5d6c878887, 3338 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project-control/out.md.checker/patch.diff` rc 0, Spark review sub-agent for Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 12:58 2026-10-06 by Spark review sub-agent for Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe, Blockchain/Dev/scripts/stack_guard.sh and Blockchain/Dev/scripts/__tests__/stop_secuura.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/__tests__/stack_guard.test.sh', 'Blockchain/Dev/scripts/stack_guard.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/stack_guard.sh , Blockchain/Dev/scripts/__tests__/stack_guard.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/stack_guard.sh` (script) and `Blockchain/Dev/scripts/__tests__/stack_guard.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/stop_secuura.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_2.diff` + input.json defect_line: every one of the 18 brief `+` line(s) present; script `+` lines 18 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/__tests__/stack_guard.test.sh` (+35/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/stack_guard.sh` (+18/-1 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/stack_guard.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=25 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 25 pass line(s); FAIL lines: ['FAIL KS-1355: a stack with an owner=unknown container is listed ONCE', 'FAIL KS-1355: ...under its real owner, with the owner=unknown count']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/stack_guard.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 27 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=27 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 27 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive stack_guard.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/stack_guard.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/stack_guard.sh` (+18/-1 counted from `section_2.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/stack_guard.test.sh` (+35/-1); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-stack-guard-one-line-per-project/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/stack_guard.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/stack_guard.test.sh
@@ -316,3 +316,37 @@ expect_val "three distinct foreign stacks are listed three times" "3" \
 mine|alice|feature/mine|abc1234|2026-08-19T10:00:00Z")"
-
+
+# --- KS-1355 spot 1: one line per PROJECT under mixed owner labels --------------
+# A stack with one container started outside start-secuura.sh carries
+# owner=unknown beside its real owner's labels (the KS-1011 case), and `sort -u`
+# on the label tuple listed that project twice - seen 2026-09-28 bringing up
+# slot 4 beside slot 3. The guard lists the project ONCE, under its real owner,
+# and counts the owner=unknown containers onto that line.
+other_stacks_out() {
+  local labels="$1"
+  local tmp; tmp="$(mktemp -d)"
+  make_repo "$tmp/repo"
+  make_docker_stub "$tmp/bin" "$labels" 33
+  PATH="$tmp/bin:$PATH" REPO_ROOT="$tmp/repo" USER=alice SUDO_USER=alice \
+    STACK_PROJECT=mine bash "$GUARD" 2>&1
+  rm -rf "$tmp"
+}
+
+KS1355_MIXED="theirs|bob|feature/theirs|dead1234|2026-08-19T11:00:00Z
+theirs|bob|feature/theirs|dead1234|2026-08-19T11:00:00Z
+theirs|unknown|unknown|unknown|unknown
+mine|alice|feature/mine|abc1234|2026-08-19T10:00:00Z"
+
+expect_val "KS-1355: a stack with an owner=unknown container is listed ONCE" "1" \
+  "$(count_other_lines "$KS1355_MIXED")"
+
+expect_val "KS-1355: ...under its real owner, with the owner=unknown count" "1" \
+  "$(other_stacks_out "$KS1355_MIXED" | grep -cF 'owner bob, branch feature/theirs (+1 container(s) with owner unknown)')"
+
+# Control: a stack whose containers ALL read owner=unknown has no real owner to
+# name, so it is still listed, once, as owner unknown.
+expect_val "KS-1355 CONTROL: an all-unknown stack is still listed once, as owner unknown" "1" \
+  "$(other_stacks_out "theirs|unknown|unknown|unknown|unknown
+theirs|unknown|unknown|unknown|unknown
+mine|alice|feature/mine|abc1234|2026-08-19T10:00:00Z" | grep -cF 'owner unknown, branch unknown')"
+
 echo ""
--- a/Blockchain/Dev/scripts/stack_guard.sh
+++ b/Blockchain/Dev/scripts/stack_guard.sh
@@ -103,2 +103,6 @@ read_stack_labels() {
 # but the operator should still know the host is shared before they act.
+# KS-1355: ONE line per PROJECT. A stack with one container started outside
+# start-secuura.sh carries owner=unknown beside its real owner's labels, and
+# `sort -u` on the label tuple listed that project twice. The first labelled
+# tuple names the stack; its owner=unknown containers are counted onto it.
 list_other_stacks() {
@@ -108,3 +112,16 @@ list_other_stacks() {
     --format '{{.Label "com.docker.compose.project"}}|{{.Label "com.secuura.stack.owner"}}|{{.Label "com.secuura.stack.branch"}}' \
-    2>/dev/null | grep -v "^${project}|" | sort -u || true
+    2>/dev/null | grep -v "^${project}|" \
+    | awk -F'|' '
+        $1 == "" { next }
+        !($1 in seen) { seen[$1] = 1; order[++n] = $1 }
+        $2 == "unknown" { unk[$1]++; next }
+        !($1 in tuple) { tuple[$1] = $2 "|" $3 }
+        END {
+          for (i = 1; i <= n; i++) {
+            p = order[i]
+            if (!(p in tuple)) { print p "|unknown|unknown"; continue }
+            print p "|" tuple[p] (unk[p] ? " (+" unk[p] " container(s) with owner unknown)" : "")
+          }
+        }' \
+    | sort || true
 }
```
