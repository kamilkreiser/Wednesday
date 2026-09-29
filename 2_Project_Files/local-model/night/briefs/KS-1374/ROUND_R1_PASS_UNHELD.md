# KS-1374 R1: Spark PASS, but NOT HELD (hold_ready.py refused)

Written 16:34 AEST 2026-09-29 (shell `date`) by the KS-1374 brief-writer (Wednesday subagent, session 35f90900).

- Run: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-29_KS-1374-R1`, the first round (original brief). The model was spark (LM_BACKEND=spark, think=0). Wall time 57.8 s, prompt 32,799 tokens, eval 1,618 tokens, done_reason=stop.
- Checker (`checker.out`, verbatim): `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/index.ts:474)`. PASS on A1, A2 (strict), A3 (test-only, one file), A4 (1 failed / 7 under the tamper, W1 declared), A5 (7/7), A6 and A7. INFO: A3i skipped. `RESULT: PASS (7/7)`, `PASS A2a ANCHOR`, `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`.
- Golden comparison: `cmp out.md.checker/patch.diff KS-1374.golden.diff` gives **IDENTICAL**. The out.md fence also matches the golden byte for byte (5,235 B).
- Develop was `2cb858335472fafcce535ca4ad328c897ed87bfb` by `ls-remote` at 16:20, 16:27 and 16:34 AEST. It did not move.

## Why there is no READY
```
python3 night/hold_ready.py <run> <scratch>/ks1374/chk_k1374_spark_163055 DEMO-LIMITER BRIEFED-TESTONLY-KS1374-GLOBAL-LIMITER-AT-DEMO-LIMIT-PIN --model-tag spark-dsv4flash --seat '...' --dry-run
hold_ready: REFUSE — checker.out has no 'mode: code_patch' line — the input says code_patch but the checker did not run it as one
```
This is the known gap. A code_patch input that carries a brief `## Tamper` runs as `mode: test_only`, and hold_ready's code_patch path has no branch for it. KS-888-VALIDATE-LOGONLY hit the same refusal and was held BY HAND by the Wednesday overnight seat (00:07 2026-09-29). This writer's scope allows a READY only through the tool, so the hold is left for Wednesday to do by hand. The golden precheck dir is `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/35f90900-da39-4310-a097-bf496fc89a5b/scratchpad/ks1374/chk_k1374_spark_163055`.
