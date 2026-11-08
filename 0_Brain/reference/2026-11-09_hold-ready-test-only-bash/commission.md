# Commission: teach hold_ready.py the new `test_only_bash` tier (Wednesday's own tree; Sonnet tooling subagent). 2026-11-09.

## Why (measured)
The Spark's new `test_only_bash` tier (commit f804b8eb95, local-model/spark/tiers/) produced two PASSes, and hold_ready.py REFUSES both, with and without --model-tag: "--model-tag is supported on the code_patch and bash_patch paths only (2026-10-08); this run is neither". Runs:
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2129_o112_p1_ks1728_scanner_misses_five_spellings_of_the_closed_pipe_fault
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2130_o112_p1_ks1547_abort_sentence_pinned_whole
Wednesday has read both diffs at source and wants them held.

## Build
Read /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py whole and its arms in local-model/tests/hold_ready_*. Add a `test_only_bash` path mirroring the test_only_input path: STRICT-APPLY leg, touched set == the declared suite(s) only, product files unchanged (re-measured blobs before/after a strict `git apply --cached`), red evidence quoted from checker.out (A4/A5 or the expect-shape A4b/A7 legs), legs quoted verbatim, golden comparison from round.json; and --model-tag accepted on it (default spark-dsv4flash for runs under spark_*). Edit by COPY then mv, with a `.pre-1109-bashhold` backup; check `pgrep -fl hold_ready` first. Arms in local-model/tests/hold_ready_test_only_bash_arms.sh: the two real runs above HOLD (in a scratch NIGHT dir via whatever override the script supports, or by a dry mode; do NOT write the real READY files: Wednesday runs the real holds), a run whose touched set includes a product file REFUSES, a run with no red evidence REFUSES, the existing hold_ready arms still pass (run them).

## Limits
Never cd; zsh Bash tool; never discard stderr; quote heredocs; no rm; no git commit (Wednesday commits); no ticket, PR or mail.

## Output
Final message: BLUF, files changed with backups, arms table with rc per arm, the exact command Wednesday runs to hold each of the two real runs, what is NOT covered.
