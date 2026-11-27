#!/bin/bash
# usage: probe.sh <copy dir> <target dir> <corpus name> <out tag>   (COAGENT_AUDIT_RED passed through if set)
Q=/private/tmp/claude-501/qae3
echo "probe $1 target $2 corpus $3 tag $4 red=${COAGENT_AUDIT_RED:-none} redact.rs $(shasum -a 256 $Q/$1/crates/coagent-audit/src/redact.rs | cut -c1-64) $(date +%T)"
QAE_IN=$Q/corp/$3.hex QAE_OUT=$Q/corp/$3.$4.out bash $Q/r.sh $Q/$1 $Q/$2 cargo test --locked -p coagent-audit --test qae3_probe -- --exact qae_dump --nocapture 2>&1
echo "exit=$? $(date +%T)"
