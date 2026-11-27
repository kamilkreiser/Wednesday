#!/bin/bash
# wrapper: from the pristine head copy's root (git archive 6274318), the audit red runner with my own folders
export COAGENT_TOOLS=/private/tmp/claude-501/qae3/tools COAGENT_AUDIT_RED_TARGET=/private/tmp/claude-501/qae3/red-t COAGENT_AUDIT_RED_LOGS=/private/tmp/claude-501/qae3/red-logs
cd /private/tmp/claude-501/qae3/ph || exit 99
export RUSTUP_TOOLCHAIN="$(sed -n 's/^channel *= *"\(.*\)"/\1/p' rust-toolchain.toml)"
echo "start $(date +%T) redact.rs $(shasum -a 256 crates/coagent-audit/src/redact.rs | cut -c1-64) toolchain $RUSTUP_TOOLCHAIN"
bash scripts/red-controls-audit.sh; echo "exit=$? end $(date +%T)"
