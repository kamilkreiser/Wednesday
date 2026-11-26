#!/bin/bash
# wrapper: from the head copy's root (git archive 5aa56e1, pristine), the audit red runner with my own folders
export COAGENT_TOOLS=/private/tmp/claude-501/qae2/tools COAGENT_AUDIT_RED_TARGET=/private/tmp/claude-501/qae2/red-t COAGENT_AUDIT_RED_LOGS=/private/tmp/claude-501/qae2/red-logs
cd /private/tmp/claude-501/qae2/ph || exit 99
echo "start $(date +%T) redact.rs $(shasum -a 256 crates/coagent-audit/src/redact.rs | cut -c1-64)"
bash scripts/red-controls-audit.sh; echo "exit=$? end $(date +%T)"
