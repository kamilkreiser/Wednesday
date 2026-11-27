# QA-POLICY-B: toolchain linked (as coagent_merge_check.sh), own cargo home; caller sets CARGO_TARGET_DIR, COAGENT_TEST_TMP, RED_CONTROLS_LOG
export COAGENT_TOOLS=/private/tmp/claude-501/qpb/tools
export RUSTUP_HOME=$COAGENT_TOOLS/rustup CARGO_HOME=$COAGENT_TOOLS/cargo
export PATH="$CARGO_HOME/bin:$PATH"
