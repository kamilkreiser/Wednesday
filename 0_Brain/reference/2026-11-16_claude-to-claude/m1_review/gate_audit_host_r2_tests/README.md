# QA-AUDIT-HOST-R2 probes (head 680d333) — how they were run
Copied into a worktree of the head (never the project folder), beside the first check's probes (gate_audit_host_tests/):
- src_tests_qa2.rs -> crates/coagent-audit-host/src/tests/qa2.rs, with `mod qa2;` in src/tests/mod.rs (uses the crate's fault injector, incl. the round's Rule::FailEvery)
- qa2_triggers.rs -> crates/coagent-audit-host/tests/ (release: cargo test --release --locked -p coagent-audit-host --test qa2_triggers -- --nocapture --test-threads=1)
- src_tests_qa2b_at_35f7e89.rs -> src/tests/qa2b.rs in a worktree of 35f7e89 with the round's fsio.rs diff applied (FailEvery only): shows P-r2-1 is pre-existing
- redctl.py: qa2_triggers under COAGENT_AUDIT_HOST_RED=own_seat_counts_requests (positive control; debug)
- mutate2.py: the round's mutants + first check's M7 (adapted) / M9, each in its own worktree and target dir; --long re-runs survivors against stop_anywhere + property
- launch.py: runs a command with cwd set (no shell cd), scripts/env.sh sourced, own CARGO_TARGET_DIR
Lib: cargo test --locked -p coagent-audit-host --lib -- tests::qa2:: --nocapture --test-threads=1
