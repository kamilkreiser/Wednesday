# READY — KS-1134 — (Ornith, briefed, TEST_ONLY bash suite) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = the fenced diff in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1134-ornith35b-night/out.md` (one test file; STRICT apply, headers consistent).**

**Held 2026-09-18 19:38 by the 14:4x Wednesday seat after a source read.** Tip `52df64f84`. Search round 7; the brief was graded PASS 8/8 by the real checker before queuing.

## Source read
- `orchestrate_jobs.test.sh`: one ok/bad cell: with zero Stage-1 jobs the run REACHES 'Stage 1 JOIN complete'; tamper Tg (the bare bash-4 "${stage1_pids[@]}" at orchestrate.sh:119, which crashes bash 3.2) reds exactly it while CELL 14 stays green.
- 6 '+' lines IDENTICAL to the brief, 0 '-'. T1-T8 PASS; T6 red set exact (assertion); controls green; product restored.
- **No product change.** Refs KS-1134. Test-only (bash), tier 2.
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh
@@ -433,3 +433,9 @@
 build_fixture "$WORK/s1absent" stage1-absent
 rc_s1absent="$(run_orchestrator "$WORK/s1absent")"
+# KS-1134: CELL 14 below asserts an ABSENCE, so a run that DIES before the Stage-1 JOIN passes it too (the gate's Tg).
+if grep -q 'Stage 1 JOIN complete' "$WORK/s1absent/out.txt"; then
+  ok "KS-1134 - with ZERO Stage-1 jobs started the run REACHES the Stage-1 JOIN instead of dying before it (rc=$rc_s1absent)"
+else
+  bad "KS-1134 - with ZERO Stage-1 jobs started the run REACHES the Stage-1 JOIN instead of dying before it" "rc=$rc_s1absent, the Stage 1 JOIN complete line is absent"
+fi
 out_s1absent="$(cat "$WORK/s1absent/out.txt")"
```
