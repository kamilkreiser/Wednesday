# READY — KS-1209 N41-3 (Ornith, briefed, TEST_ONLY bash suite) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = the fenced diff in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1209-ornith35b-night2/out.md` (one test file; STRICT apply, headers consistent).**

**Held 2026-09-18 19:38 by the 14:4x Wednesday seat after a source read.** Tip `52df64f84`. Search round 7; the brief was graded PASS 8/8 by the real checker before queuing.

## Source read
- `preflight_verdict_names_real_failures.test.sh`: one cell before the tally: a REAL leg-1 failure in an installed tree is named, exits 1, no env excuse; tamper T7 (leg 1 always excluded, preflight.sh:696) reds exactly it.
- 3 '+' lines IDENTICAL to the brief, 0 '-'. T1-T8 PASS; T6 red set exact (assertion); controls green; product restored.
- **No product change.** Refs KS-1209. Test-only (bash), tier 2.
- **Collision note:** held KS-1261 edits preflight.sh:96-98; this pins behaviour at :696 and edits only the suite. File-disjoint; if KS-1261 merges first nothing here changes (the tamper is a gate artefact, not part of the PR).
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/scripts/__tests__/preflight_verdict_names_real_failures.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/preflight_verdict_names_real_failures.test.sh
@@ -72,3 +72,6 @@
 echo ""
+# KS-1209 N41-3: a REAL leg-1 failure (the tree IS installed, env_fail=0) is a finding, so it is named like any other leg.
+run_legs "1" 0
+expect "a REAL leg-1 failure with an install (env_fail=0) is named as leg 1 and does not blame the environment" "1 yes no" "$RC $(has 'leg(s) 1 ') $(has 'environment condition')"
 echo "preflight_verdict_names_real_failures: $PASS passed, $FAIL failed"
 [ "$FAIL" -eq 0 ]
```
