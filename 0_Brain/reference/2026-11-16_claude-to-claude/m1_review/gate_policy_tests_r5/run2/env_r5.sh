# Source me. Read-only use of the drive-local toolchain: real toolchain binaries (not rustup proxies), a
# private CARGO_HOME (copy of the registry) and a private target dir, all in the gate's scratchpad.
S=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r5
T="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
export COAGENT_TOOLS="$S/tools"
export RUSTUP_HOME="$T/rustup"
export CARGO_HOME="$S/tools/cargo"
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$S/target}"
export PATH="$T/rustup/toolchains/1.100.0-aarch64-apple-darwin/bin:$S/tools/cargo/bin:$PATH"
export CARGO_NET_OFFLINE=true
O=/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_policy_tests_r5/run2
