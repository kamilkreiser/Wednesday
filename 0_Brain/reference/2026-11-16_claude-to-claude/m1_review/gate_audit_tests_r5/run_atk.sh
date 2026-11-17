source /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/env_atk.sh
cargo test -j 4 --locked --manifest-path $C/Cargo.toml -p coagent-audit --test gate_r5 "$@" 2>&1
