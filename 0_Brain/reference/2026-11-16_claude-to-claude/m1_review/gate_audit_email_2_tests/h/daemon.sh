#!/bin/bash
Q=/private/tmp/claude-501/qae2; A=()
for t in an_after an_create an_nothing an_texts aw_answers aw_disk aw_lifecycle aw_off aw_peer aw_record aw_round2 aw_seal aw_util; do A+=(--test "$t"); done
echo "start $(date +%T)"; bash $Q/r.sh $Q/ph $Q/td cargo test --locked -p coagent-daemon --no-fail-fast "${A[@]}"; echo "exit=$? end $(date +%T)"
