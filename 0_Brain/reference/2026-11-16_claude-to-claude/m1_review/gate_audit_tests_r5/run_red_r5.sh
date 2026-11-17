# my gate_r5 tests under the builder's red controls (debug)
source /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/env_atk.sh
S=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5
for red in requested_cp_on_free requested_no_holdback commit_before_write own_seat_overfill anchor_not_checked own_cp_unchecked; do
  echo "=== $red"
  R5_CASES=64 COAGENT_AUDIT_RED=$red cargo test -j 4 --locked --manifest-path $C/Cargo.toml -p coagent-audit --test gate_r5 -- --test-threads 4 2>&1 | grep -E "^test |panicked|^  left|^ right|Test failed|r5 property|changed although|not shown|answered|accepted the older|removing|test result" | cut -c1-400
done
