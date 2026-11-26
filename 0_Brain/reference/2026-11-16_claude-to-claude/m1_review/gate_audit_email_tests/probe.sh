#!/bin/bash
# usage: probe.sh <copy dir> <target dir> <corpus.hex> <out>   (extra env passed through)
Q=/private/tmp/claude-501/qae
QAE_IN="$3" QAE_OUT="$4" bash $Q/r.sh $Q/$1 $Q/$2 cargo test --locked -p coagent-audit --test qae_probe -- --exact qae_dump --nocapture
