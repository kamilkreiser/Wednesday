# source: toolchain linked (as coagent_merge_check.sh), own cargo home; caller sets CARGO_TARGET_DIR
export COAGENT_TOOLS=/private/tmp/claude-501/qpn/tools
export RUSTUP_HOME=$COAGENT_TOOLS/rustup CARGO_HOME=$COAGENT_TOOLS/cargo
export PATH="$CARGO_HOME/bin:$PATH"
export COAGENT_TEST_TMP=/private/tmp/claude-501/qpn/testtmp
mkdir -p $COAGENT_TEST_TMP
