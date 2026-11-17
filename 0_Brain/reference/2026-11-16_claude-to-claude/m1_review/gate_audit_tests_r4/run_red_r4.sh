. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4/env.sh
export CARGO_TARGET_DIR=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4/target_redr4 R4_CASES=48
OUT=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4/red_r4_results.txt; : > $OUT
mkdir -p /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4/redr4_logs
while IFS='|' read -r red test; do
  log=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4/redr4_logs/$red.$test.log
  COAGENT_AUDIT_RED=$red cargo test --offline --locked --manifest-path /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4/redr4/Cargo.toml -p coagent-audit --test gate_r4 -- --exact $test --nocapture > $log 2>&1
  rc=$?
  marker=$(grep -c 'RED CONTROL BUILD' $log)
  verdict=GREEN; grep -q "test $test ... FAILED" $log && verdict=RED
  msg=$(grep -A2 -m1 "panicked at" $log | sed -n 2p | cut -c1-220)
  echo "$red | $test | $verdict | rc=$rc marker=$marker | $msg" >> $OUT
done <<ROWS
hs_headers_to_nothing|r4_fixed_a_b1_a_nothing_member_holds_no_header_of_that_author
hs_current_roster|r4_fixed_a_m1_cross_check_catches_equivocation_after_a_removal
cs_rule_current_only|r4_fixed_a_m2_a_joiner_cannot_countersign_before_its_anchor_and_the_export_verifies
audit_under_binding|r4_fixed_a_m3_no_audit_domain_signature_is_a_device_binding
head_no_cap|r4_fixed_a_m4_checkpoints_are_bounded_and_the_export_verifies
hs_accept_removed_reporter|r4_fixed_r2_m1_heads_seen_replays_and_removed_reporters_store_nothing
receipt_on_receive|r4_fixed_r3_m1_traffic_to_one_member_cannot_spend_its_seat_at_another_and_rosters_apply
roster_on_seat|r4_fixed_r3_m1_traffic_to_one_member_cannot_spend_its_seat_at_another_and_rosters_apply
space_before_fork|r4_fixed_r3_n2_fork_from_an_author_with_a_full_seat_is_a_fork_with_evidence
shared_peer_pool|r4_prop_storage_accounting
uncharged_slot|r4_prop_storage_accounting
release_keeps_charge|r4_prop_storage_accounting
resume_all_own|r4_prop_storage_accounting
roster_on_seat|r4_prop_storage_accounting
head_no_max_seq|r4_extreme_numbers_on_the_new_paths_never_panic_and_store_within_bounds
ROWS
echo done >> $OUT
