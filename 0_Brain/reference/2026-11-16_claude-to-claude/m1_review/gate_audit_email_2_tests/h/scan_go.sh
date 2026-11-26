#!/bin/bash
Q=/private/tmp/claude-501/qae2; P=$Q/ph
FILES=($Q/scan/added.txt $Q/scan/commit_msg.txt $P/BACKLOG.md $P/crates/coagent-audit/Cargo.toml $P/crates/coagent-audit/build.rs $P/crates/coagent-audit/src/redact.rs $P/crates/coagent-audit/tests/ae2_email.rs $P/crates/coagent-audit/tests/ae_email.rs $P/docs/AUDIT.md $P/docs/M0-OUTCOMES.md $P/scripts/red-controls-audit.sh $Q/scan/ctl_ae2.rs $Q/scan/ctl.bin)
. $Q/h/run_scan.sh "$@"
