# READY — KS-1258-N68-2 (Ornith, briefed, test_only) — PASS 8/8 first sample (graded by a harness RE-CHECK) — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1258-ornith35b-night3/out.md.checker/patch.diff`** (from `ls` of that dir, 14:57).

**Held 14:57 2026-09-19 by the 10:2x Wednesday seat after a source read.** Tip `51dbedd39`. One allow-list cell in `ks1258-degraded-optional-service-advice.test.ts`: the degraded-optional advice is EXACTLY the comment line + the curl line, so DOCKERRUN / BUNRUN / MAKEUP / NODEDIST / PNPMDEV / TSXWATCH each red exactly the new cell by assertion. Source: the #1061-#1069 gate's N68-2 (the regex form false-reds, per its N68-3; this is the allow-list form). **Grading history, stated:** the night run's checker returned CHECKER_NO_RESULT (a harness fault: N68-1's modify-mode test file had been left in the shared KS-1258 clone). The checker was fixed (it now saves-and-restores a previous run's modified file in the test dir) and RE-RUN on the SAME model output `out.md`: PASS 8/8 (`checker.rerun.out`). The model was not re-run; this is not a rebrief. Source read: 6/6 + lines = the brief; crossed controls 5/6 absent. **Refs KS-1258.** Test files only. Tier 2. Rides the batch after Seat B 4th's, WITH READY_KS-1258-N68-1 (different files: ks1248 vs ks1258).

**HELD. Not raised.**

---
## Checker verdict (the re-run, verbatim tail)
PASS T7[TSXWATCH] every control green under the tamper
T6 summary: 6/6 tamper(s) red exactly their declared set
T7 summary: controls green under all 6 tamper(s)
T8 summary: all 6 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1258-degraded-optional-service-advice.test.ts mode=modify runner=vitest cells=5 tampers=6 apply=strict
RESULT: PASS (8/8)
