# How these were run
Copied into a worktree of the head 35f7e89 (never the project folder):
- qa_store.rs, qa_triggers.rs, qa_hostile.rs -> crates/coagent-audit-host/tests/
- src_tests_qa.rs -> crates/coagent-audit-host/src/tests/qa.rs, src_tests_qa_stop.rs -> src/tests/qa_stop.rs, with `mod qa; mod qa_stop;` added to src/tests/mod.rs (they use the crate-internal fault injector)
- mutate.py applies 14 source mutations one at a time to a separate worktree and runs the crate tests
Run: cargo test --locked -p coagent-audit-host --test <name> -- --nocapture --test-threads=1 ; lib: --lib tests::qa:: / tests::qa_stop:: (release for qa_stop)
