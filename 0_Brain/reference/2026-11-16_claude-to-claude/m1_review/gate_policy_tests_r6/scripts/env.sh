G=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_policy_r6
C=$G/clone
export COAGENT_TOOLS=$G/tools
export CARGO_HOME=$G/tools/cargo RUSTUP_HOME=$G/tools/rustup CARGO_TARGET_DIR=$G/target
export PATH=$CARGO_HOME/bin:$PATH
export COAGENT_TEST_TMP=${COAGENT_TEST_TMP:-$G/fix_ci}
export CARGO_BUILD_JOBS=4
O=/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_policy_tests_r6
