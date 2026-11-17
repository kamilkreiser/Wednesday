source /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/env.sh
cargo fetch --locked --manifest-path $C/Cargo.toml; echo fetch_rc=$?
cargo build --tests -p coagent-audit --manifest-path $C/Cargo.toml -j 4 2>&1 | tail -3; echo build_rc=$?
