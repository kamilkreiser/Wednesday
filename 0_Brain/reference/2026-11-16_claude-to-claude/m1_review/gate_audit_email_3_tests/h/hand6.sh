#!/bin/bash
# the six new red names by hand, in the red script's own form, on the pristine head copy qae3/ph (one target qae3/tr, warm after the first)
Q=/private/tmp/claude-501/qae3
while IFS='|' read -r N T; do
  L=$Q/logs/hand_$N.log
  echo "hand $N $T redact.rs $(shasum -a 256 $Q/ph/crates/coagent-audit/src/redact.rs | cut -c1-64) start $(date +%T)" > $L
  COAGENT_AUDIT_RED=$N bash $Q/r.sh $Q/ph $Q/tr cargo test --locked -p coagent-audit --test ae3_email -- --exact $T >> $L 2>&1
  echo "exit=$? end $(date +%T)" >> $L
  echo "$N: RED CONTROL BUILD $(grep -c 'RED CONTROL BUILD' $L); $(grep -E '^test result' $L)"
done <<'R'
email_userinfo_slash_only|ae3_address_joined_to_a_link_is_masked
email_colon_later_slash|ae3_address_before_a_colon_is_masked
email_stop_whitespace_only|ae3_stop_bytes_end_the_colon_token
email_stop_keeps_non_ascii|ae3_non_ascii_ends_the_colon_token
email_tilde_not_kept|ae3_tilde_alone_is_kept
email_prefix_takes_dash|ae3_prefix_does_not_take_a_dash
R
