# source: own toolchain links + own cargo home (registry), as coagent_merge_check.sh does
export COAGENT_TOOLS=/private/tmp/claude-501/qvx2/tools
export RUSTUP_HOME="$COAGENT_TOOLS/rustup" CARGO_HOME="$COAGENT_TOOLS/cargo"
export PATH="$CARGO_HOME/bin:$PATH"
