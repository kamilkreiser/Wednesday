# READY — KS-1273-TRIVYYAMLEXITCODE-1 (Ornith, briefed, test_only, modify · bash) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 16:13 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1119rows-drafter-precheck/TRIVYYAMLEXITCODE/out.md.checker/patch.diff` rc 0, Wednesday 13:5x seat, 2026-09-21).

**Held 16:13 2026-09-21 by Wednesday 13:5x seat, 2026-09-21 after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night2/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh` (modify). `+` lines 8 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 1 == `must_remove`. Green at the tip: 6/6 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `EXITCODEFLAGGONE` → red exactly ["RED KS-1273 a trivy.yaml exit-code: 1 in the job's cwd keeps", '🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 ima', '🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keep']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1273-TRIVYYAMLEXITCODE-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1273-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
@@ -63,4 +63,5 @@
   case " $* " in *" --exit-code 0 "*) exit 0 ;; esac
-  exit "${TRIVY_EXIT_CODE:-0}"
+  cfg="$(awk '$1 == "exit-code:" { print $2 }' "$PWD/trivy.yaml" 2>/dev/null)"
+  exit "${TRIVY_EXIT_CODE:-${cfg:-0}}"
 fi
 echo '{}'
@@ -112,3 +112,9 @@
+# RED - KS-1273, the ticket's second arm: a trivy.yaml with exit-code: 1 in the job's cwd (the job runs from $SELF) and NO env var; the ONLY image HAS findings.
+build_fixture "$WORK/yamlcode" 'dev-auth:latest' 'dev-auth:latest findings'
+echo 'exit-code: 1' > "$WORK/yamlcode/Testing/trivy.yaml"
+rc="$(run_job "$WORK/yamlcode")"
+got="$rc $(row "$WORK/yamlcode")"
+if [ "$got" = "0 none 1 1" ]; then ok "RED KS-1273 a trivy.yaml exit-code: 1 in the job's cwd keeps findings: rc 0, no error, CRITICAL=1 HIGH=1"; else bad "RED KS-1273 a trivy.yaml exit-code: 1 in the job's cwd keeps findings: rc 0, no error, CRITICAL=1 HIGH=1" "want 0 none 1 1, got $got (trivy argv: $(cat "$WORK/yamlcode/trivy_calls.txt" 2>/dev/null))"; fi
 printf '\n  %d passed, %d failed\n' "$pass" "$fail"
 [ "$fail" -eq 0 ] || exit 1
 exit 0
```
