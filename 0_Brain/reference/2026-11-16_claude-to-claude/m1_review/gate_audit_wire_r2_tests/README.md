# QA-AUDIT-WIRE-R2 harnesses and logs
- `qa_alpha2.rs`: the first check's `qa_alpha.rs` adapted to `drive_seal(Option<u64>, ..)` plus three R2 tests (segment unknown/known, record placeholder, status vs member segment). Run as a test file of a scratch copy of the head (`crates/coagent-daemon/tests/`), never in a tree whose whole suite is run.
- `qa_lib.py`, `qa_causes.py`, `qa_causes2.py`, `qa_diff.py`, `qa_cmp.py`, `qa_scan.py`: the first check's, byte-identical, reused unchanged.
- `run_diff.sh` (task 4), `red_r2.sh` (task 5 RED_ONLY), `build1.sh` (clean builds), `r.sh` (the wrapper that does the cd).
- `logs/`: every run's output; `logs/red/` the red script's own logs (12 rows + final_green.log); `logs/diff/` the 8 differential sessions and the two comparisons. The scan's word list was never written to a file (the scan outputs name words only as #n).
