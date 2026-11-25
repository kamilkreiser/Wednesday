# QA-POLICY-AT-R2: toolchain linked (as coagent_merge_check.sh), own cargo home under the work dir
export COAGENT_TOOLS=/private/tmp/claude-501/qpa2/tools
export RUSTUP_HOME=$COAGENT_TOOLS/rustup CARGO_HOME=$COAGENT_TOOLS/cargo
export PATH="$CARGO_HOME/bin:$PATH"
