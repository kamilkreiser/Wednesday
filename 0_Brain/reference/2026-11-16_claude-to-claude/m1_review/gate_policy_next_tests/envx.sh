# QA-POLICY-NEXT: toolchain linked (as coagent_merge_check.sh), own cargo home; caller sets CARGO_TARGET_DIR, COAGENT_TEST_TMP
export COAGENT_TOOLS=/private/tmp/claude-501/qpx/tools
export RUSTUP_HOME=$COAGENT_TOOLS/rustup CARGO_HOME=$COAGENT_TOOLS/cargo
export PATH="$CARGO_HOME/bin:$PATH"
