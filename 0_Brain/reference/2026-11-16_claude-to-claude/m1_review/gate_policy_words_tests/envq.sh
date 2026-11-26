# QA-POLICY-WORDS: toolchain LINKED as coagent_merge_check.sh does; own cargo home (registry cache) under the work dir
export COAGENT_TOOLS=/private/tmp/claude-501/qpw/tools
export RUSTUP_HOME=$COAGENT_TOOLS/rustup CARGO_HOME=$COAGENT_TOOLS/cargo
export PATH="$CARGO_HOME/bin:$PATH"
