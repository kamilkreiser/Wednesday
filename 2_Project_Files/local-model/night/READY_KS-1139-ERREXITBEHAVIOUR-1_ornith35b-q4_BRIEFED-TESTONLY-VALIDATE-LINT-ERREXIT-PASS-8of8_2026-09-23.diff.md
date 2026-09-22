# READY — KS-1139-ERREXITBEHAVIOUR-1 (Ornith, briefed, test_only, modify · bash) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 06:06 2026-09-23). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed17-drafter-precheck/ERREXITBEHAVIOUR/out.md.checker/patch.diff` rc 0, Wednesday 06:0x seat 2026-09-23).

**Held 06:06 2026-09-23 by Wednesday 06:0x seat 2026-09-23 after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night2/out.md.checker`, not typed).** Tip `2bc5ccf63b8c40911afb568b03cace066238ffcf`. Touches ONE file: `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` (modify). `+` lines 13 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `FAILPLUSPLUS` → red exactly ['both counters advance by assignment', 'validate-lint.sh has NO bare arithmetic-command post-increme']
- `PASSPLUSPLUS` → red exactly ['both counters advance by assignment', 'run_check survives bash -e from PASS_COUNT=0 to the second c', 'validate-lint.sh has NO bare arithmetic-command post-increme']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1139-ERREXITBEHAVIOUR-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh
@@ -63,2 +63,15 @@
 # ---------------------------------------------------------------------------
+# CELL 4 - KS-1139 (gate 19C ERREXIT-ZEROCOUNT, #1192): cells 1-2 pin the fix
+# STATICALLY. This one RUNS it: run_check is extracted from the subject and run
+# under bash -e with both counters at 0; a bare ((PASS_COUNT++)) at 0 exits 1
+# and errexit kills the shell before the second check (measured on /bin/bash
+# 3.2.57 at the pre-#1192 script: rc 1, no survived line). Fixed: survived=2.
+TOTAL_CELLS=$((TOTAL_CELLS + 1))
+survived="$(bash -e -c 'eval "$(sed -n "/^run_check()/,/^}/p" "$1")"; PASS_COUNT=0; FAIL_COUNT=0; run_check a true >/dev/null; run_check b true >/dev/null; echo "survived=$PASS_COUNT"' _ "$SUBJ" 2>/dev/null | tail -1 || true)"
+if [ "$survived" = "survived=2" ]; then
+  ok "run_check survives bash -e from PASS_COUNT=0 to the second check (survived=2)"
+else
+  bad "run_check survives bash -e from PASS_COUNT=0 to the second check (survived=2)" "got '${survived:-<nothing>}' - errexit killed the extracted run_check at the first counter"
+fi
+# ---------------------------------------------------------------------------
 # CONTROL CELL 3 - The subject parses cleanly under any bash version we run this
```
