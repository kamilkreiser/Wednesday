# Spark standing filler queue (routine (c)) — builder report (saved by Wednesday 2026-11-12 ~16:5x; the builder's Write was refused)

## BLUF
Built `2_Project_Files/local-model/filler/` (queue.tsv, tasks/<id>.json, filler_lib.py with gates + prompts + deterministic checkers `check_mutant` / `check_numstat`, run_filler.py (ONE task per call), status.py, tests/test_filler.py, inputs/ read-only snapshots). Ran all 5 seed tasks on Nemotron after the nemo1112b A/B ended: F01 mutants of isPasswordBreached (PR 2209) ACCEPTED 5/5 (`>0`->`>=0`, `&&`->`||`, `line.trim()`->`line`, `>0`->`>1`, `return true`->`return false` = the gate-331 class); F02 mutants of the KS-2055 cancel-reason validator (PR 2182) ACCEPTED 2/4 (2 duplicates refused); F03 numstat PR 2209 MATCH; F04 PR 2208 MATCH; F05 PR 2182 MATCH (after a checker fix). Red-proofs 19/19 + an end-to-end runner exercise (planted ungrounded claim REJECTED, non-applying mutant REJECTED 0/5, clean MATCH). `fleet/spark_status.py` gains a `FILLER:` line (one try-block; existing lines unchanged).

## Gates (run_filler.py exits rc 3, row untouched, unless all open)
No spark-ab/ab.py running; spark/state/round.lock and queue.lock not held by a live pid; tunnel GET /v1/models 200. Secuura tasks only in v1.

## Fixed during the build
F01 first run kept 1/5 (model dropped a comment context line) -> zero-context diffs + `--unidiff-zero` in the checker; 5/5 after. F05 first flagged MISMATCH wrongly (mail labels vs API paths) -> path-token then count fallback; MATCH. KS-2169 has no validator: the target is KS-2055 half 2 (PR 2182).

## Does NOT do
No automatic drain (nothing loops/schedules run_filler.py yet); does not take round.lock (outside its write scope); no judgement (mutants not run against tests, compile not checked); a crashed row stays `running` (hand reset); numstat = PR line counts only; Secuura only. No doctor/PORTABILITY change (stdlib + git + pgrep).
