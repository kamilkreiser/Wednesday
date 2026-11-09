# READY - KS-2091-KS-2091-O129-P2 (Spark (DeepSeek V4 Flash), briefed, test_only_bash/plant) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2091_o129_p2_pre_push_red_preflight_refuses_the_push_cell/out.md.checker/patch.diff` (from `ls` at 07:47 2026-11-10; sha256[:16] 27d7c1cfccf0dbd2, 4573 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 07:47 2026-11-10 by Wednesday after a source read (hold_ready.py, test_only_bash path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2091_o129_p2_pre_push_red_preflight_refuses_the_push_cell/out.md.checker`; product and plant-file bytes were RE-MEASURED here.** Tip `0d286210f98b1bd549ff67cec20746648654d501`. Brief: not given (--brief) and not located
- Touched set [patch.diff `+++` headers == sections.json == `git apply --numstat` == input.json test_files; no product or plant file named]: ['Blockchain/Dev/scripts/__tests__/pre_push_red_preflight_refuses_the_push.test.sh']; `+` lines 80 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `.githooks/pre-push` blob 0c53e79ea5d5; plant file(s) also unchanged.
- Red cells [input.json]:
  - `a red preflight refuses the push`
- Red evidence under the plant [red_with_plant__*.out, the suite's own FAIL line per red cell, verbatim]:
  - `FAIL a red preflight refuses the push`
- Plant file(s) [input.json plant_diff / plant; applied in the checker's clone only]: ['.githooks/pre-push']
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=0 ok=0 bad=0 skipped_newfile=1)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/scripts/__tests__/pre_push_red_preflight_refuses_the_push.test.sh)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A3s every patched suite parses (bash -n)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 named cell(s) exist and pass on the unmodified product; declared suites 4 cells, 0 red, rc [0]`
  - `PASS A6 WHOLE SUITE no worse: declared cells 0 -> 4 (none lost); 0 sibling suite(s) 0 -> 0 cells, FAIL lines 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 named cell(s) print the suite's own FAIL line under the plant (.githooks/pre-push) and pass without it; rc [1]; e.g. pre_push_red_preflight_refuses_the_push.test.sh: FAIL a red preflight refuses the push`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- Checker INFO lines [checker.out, verbatim]:
  - `INFO baseline at the tip: declared suites 0 cell(s), 0 FAIL line(s), rc {}; 0 sibling suite(s) 0 cell(s), 0 FAIL line(s)`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_bash)`

**PR NOTES for the raise seat:** TEST_ONLY_BASH (plant shape) - bash suite bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief plant (checker clone only), not a change in the PR. DOES NOT PROVE the plant is the regression that matters, or that a cell catches a different fault; an INFO line above is the checker's own note and is not a leg. Wednesday read the cells against the brief before this hold.

```diff
diff --git a/Blockchain/Dev/scripts/__tests__/pre_push_red_preflight_refuses_the_push.test.sh b/Blockchain/Dev/scripts/__tests__/pre_push_red_preflight_refuses_the_push.test.sh
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/pre_push_red_preflight_refuses_the_push.test.sh
@@ -0,0 +1,80 @@
+#!/usr/bin/env bash
+# TESTS for .githooks/pre-push - a RED preflight must make the hook refuse the push (KS-2091)
+# The last step of the hook runs the preflight and ends in `|| { ...; exit 1; }`. If that exit 1 became exit 0 every leg of the
+# preflight would be advisory, and no other hook suite would notice. Fixture: a local bare remote; the preflight is a stub that
+# exits with PREFLIGHT_RC (default 0) after printing a marker line; the systemTest formatting gate is a stub that exits 0.
+# Cells: a green preflight lets a Blockchain/Dev push land (control); a red preflight refuses it, the push does not land,
+# and the hook says why.
+# Usage: bash Blockchain/Dev/scripts/__tests__/pre_push_red_preflight_refuses_the_push.test.sh
+#        HOOK_SH=/path/to/other/pre-push bash ...   (to test a different copy)
+set -uo pipefail
+export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+HOOK="${HOOK_SH:-$REPO_ROOT/.githooks/pre-push}"
+[ -f "$HOOK" ] || { echo "FATAL: pre-push hook not found at $HOOK" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks2091.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+pass=0
+fail=0
+ok()   { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad()  { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+(
+  git init -q --bare -b main "$WORK/origin.git"
+  git init -q -b main "$WORK/seed"
+  cd "$WORK/seed"
+  git config user.email t@t.t; git config user.name t
+  mkdir -p Blockchain/Dev/scripts/preflight systemTest/scripts docs
+  echo base > Blockchain/Dev/file.txt
+  printf '#!/usr/bin/env bash\necho "[preflight] ran"\n[ "${PREFLIGHT_RC:-0}" = 0 ] || echo "[preflight] LEG FAILED"\nexit "${PREFLIGHT_RC:-0}"\n' > Blockchain/Dev/scripts/preflight/preflight.sh
+  : > systemTest/slot-target.sh
+  printf '#!/usr/bin/env bash\n[ "${1:-}" = "--all" ] || cat >/dev/null\nexit 0\n' > systemTest/scripts/check-package-format.sh
+  chmod +x systemTest/scripts/check-package-format.sh
+  git add -A; git commit -qm init
+  git branch develop
+  git remote add origin "$WORK/origin.git"
+  git push -q origin main develop
+  cd "$WORK"
+  git clone -q "$WORK/origin.git" fresh
+  cd fresh
+  git config user.email t@t.t; git config user.name t
+  mkdir -p "$WORK/hooks"
+  cp "$HOOK" "$WORK/hooks/pre-push"
+  chmod +x "$WORK/hooks/pre-push"
+  git config core.hooksPath "$WORK/hooks"
+) >/dev/null 2>&1
+push_branch() { # push_branch <branch> <preflight rc>: a Blockchain/Dev change pushed with the stub preflight exiting <rc>
+  (
+    cd "$WORK/fresh" || exit 1
+    git checkout -q -b "$1" --no-track origin/develop
+    echo "$1" >> Blockchain/Dev/file.txt
+    git add -A; git commit -qm "dev change on $1"
+    PREFLIGHT_RC="$2" git push origin "$1" 2>&1
+    git ls-remote origin "refs/heads/$1" | grep -q . && echo "PUSH-LANDED"
+  )
+}
+green_out="$(push_branch feat/green 0)"
+red_out="$(push_branch feat/red 1)"
+if [[ "$green_out" == *'[preflight] ran'* && "$green_out" == *'PUSH-LANDED'* ]]; then
+  ok "CONTROL a green preflight: the Blockchain/Dev push runs the preflight and lands"
+else
+  bad "CONTROL a green preflight: the Blockchain/Dev push runs the preflight and lands" "the preflight did not run, or the push did not land"
+fi
+if [[ "$red_out" == *'[preflight] LEG FAILED'* ]]; then
+  ok "CONTROL the red preflight stub ran: its failure marker is in the push output"
+else
+  bad "CONTROL the red preflight stub ran: its failure marker is in the push output" "the preflight stub did not run, so the red cells below prove nothing"
+fi
+if [[ "$red_out" == *'PUSH-LANDED'* ]]; then
+  bad "a red preflight refuses the push" "the push landed on the remote although the preflight exited 1"
+else
+  ok "a red preflight refuses the push - nothing landed on the remote"
+fi
+if [[ "$red_out" == *'[pre-push] preflight failed'* ]]; then
+  ok "a red preflight is announced - the hook prints its preflight failed line"
+else
+  bad "a red preflight is announced - the hook prints its preflight failed line" "no [pre-push] preflight failed line in the push output"
+fi
+echo ""
+echo "pre_push_red_preflight_refuses_the_push: ${pass} passed, ${fail} failed"
+(( fail == 0 ))
```
