W=/private/tmp/claude-501/qsn; C=$W/clone
export COAGENT_TOOLS=$W/tools RUSTUP_HOME=$W/tools/rustup CARGO_HOME=$W/tools/cargo CARGO_TARGET_DIR=$W/target RUSTUP_TOOLCHAIN=1.100.0
export PATH=$W/tools/cargo/bin:$PATH
unset COAGENT_RED COAGENT_RED_ROSTER COAGENT_AUDIT_RED COAGENT_AUDIT_HOST_RED COAGENT_SCANNER_RED COAGENT_SCANNER_SRC_DIR
M="--manifest-path $C/Cargo.toml"
