# READY — KS-1260-N62 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1260-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` of that dir, 15:50).

**Held 15:50 2026-09-19 by the 10:2x Wednesday seat after a source read.** Tip `51dbedd39` (develop has since moved to f9c28a8b8 with #1070-#1076; the raising seat re-measures that its target blob is unchanged). `run_legs` gains two optional args (legs failing for want of an install; the last leg driven) plus three cells pinning OLDFORMULA (:705), ALSOLINENOOP (:707) and NONEDECLAREDEXIT0 (:746; its `From` `exit 1` occurs 4× in preflight.sh and is pinned by Line, so rebuild if the file moves). 0 of 742 red without, each tamper exactly 1 FAIL with it. Source: the #1061-#1069 gate's N62-1/N62-2 rows. Source read: 10/10 + and 2/2 - = the brief; crossed 10/10 absent. **Refs KS-1260** (In Progress). Test files only. Tier 2.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T8[NONEDECLAREDEXIT0] Blockchain/Dev/scripts/preflight/preflight.sh restored by bytes: sha256 148d59338fde == tip blob, git diff --quiet rc 0
PASS T6[NONEDECLAREDEXIT0] red set == declared exactly: {RED KS-1260 N62-2b: a clean run with the last leg never driv}, every red an assertion failure
PASS T7[NONEDECLAREDEXIT0] every control green under the tamper
T6 summary: 3/3 tamper(s) red exactly their declared set
T7 summary: controls green under all 3 tamper(s)
T8 summary: all 3 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh mode=modify runner=bash cells=8 tampers=3 apply=strict
RESULT: PASS (8/8)
