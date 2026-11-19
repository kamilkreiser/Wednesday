#!/bin/bash
# Gate's own mutation probes on the m3-deputy tree (attack clone). One mutant at a time, file restored after each.
set -u
T=<work>/atk
OUT=<work>/mut
mkdir -p "$OUT"
export COAGENT_TOOLS=<work>/mc/tools CARGO_TARGET_DIR=<work>/mc/target
cd "$T" && . scripts/env.sh
TESTS="--test deputy_admission --test deputy_grant --test deputy_intake --test deputy_start --test deputy_roles --test deputy_props --test api_stability --test pinned_proposed"
# name | file | perl -0pe expression
MUTS=(
"M01_withdraw_no_void|src/deputy.rs|s/\(Some\(_\), None\) => true,/(Some(_), None) => false,/"
"M02_no_proposal_before_epoch|src/deputy.rs|s/if p\.at_version < grant\.epoch && !epoch_unchecked/if false \&\& p.at_version < grant.epoch/"
"M03_no_key_in_use|src/deputy.rs|s/if in_use \{\n        return Err\(AdmissionError::CandidateKeyInUse\)/if false \&\& in_use {\n        return Err(AdmissionError::CandidateKeyInUse)/"
"M05_no_rebuild_after_roster|src/deputy.rs|s/self\.rebuild\(\);\n        Ok\(SessionReport/Ok(SessionReport/"
"M07_unsigned_no_seq|src/deputy.rs|s/if b\.seq != n \{/if false \&\& b.seq != n {/"
"M09_no_slot_taken|src/deputy.rs|s/if view\.taken\.contains\(&e\.slot\) \{/if false \&\& view.taken.contains(\&e.slot) {/"
"M13_evidence_same_ok|src/deputy.rs|s/if a == b \{/if false \&\& a == b {/"
"M15_cap_change_keeps_epoch|src/deputy.rs|s/ && cur\.cap == next\.cap;/;/"
"M16_holder_change_keeps_epoch|src/deputy.rs|s/is_some_and\(\|\(oh, og\)\| oh == h && og\.slots == g\.slots\)/is_some_and(|(_oh, og)| og.slots == g.slots)/"
"M17_deputy_intake_no_stale|src/deputy_intake.rs|s/return Err\(DeputyIntakeError::Stale\);/{}/"
"M18_provisional_may_send_admission_kind|src/deputy.rs|s/    \"deputy.admission\",\n\];/];/; s/\[&str; 5\]/[&str; 4]/"
"M20_start_local_not_last_ok|src/deputy.rs|s/Some\(p\) if Some\(p\) != last =>/Some(p) if false \&\& Some(p) != last =>/"
"M21_no_prev_check|src/deputy.rs|s/if b\.prev\.0 != self\.hashes\.last\(\)/if false \&\& b.prev.0 != self.hashes.last()/"
"M23_evidence_any_epoch|src/deputy.rs|s/if a\.epoch != g\.epoch \|\| b\.epoch != g\.epoch \{/if false {/"
"M25_former_holder_any_epoch_member|src/deputy.rs|s/roster\.deputy\(\)\.is_some_and\(\|\(h, _\)\| &h == key\)\n\}/roster.deputy().is_some_and(|(h, _)| \&h == key) || roster.role_of(key) == Some(Role::Guest)\n}/"
"M26_no_proposer_is_starter|src/deputy.rs|s/if r\.is_convener\(&p\.proposer\) \{/if false \&\& r.is_convener(\&p.proposer) {/"
"M27_no_proposal_held_check|src/deputy.rs|s/if held\(p\.at_version\) != Some\(p\.at_hash\.0\) \{/if false {/"
)
for row in "${MUTS[@]}"; do
  IFS='|' read -r name file expr <<<"$row"
  f="crates/coagent-roster/$file"
  cp "$f" "$OUT/orig.rs"
  perl -0pi -e "$expr" "$f"
  if cmp -s "$f" "$OUT/orig.rs"; then echo "$name NOT-APPLIED"; continue; fi
  cargo test --locked --no-fail-fast -p coagent-roster $TESTS > "$OUT/$name.log" 2>&1; rc=$?
  cp "$OUT/orig.rs" "$f"
  fails=$(grep -E "^test .* FAILED$" "$OUT/$name.log" | sed 's/^test //; s/ \.\.\. FAILED//' | tr '\n' ' ')
  if grep -q "error\[E" "$OUT/$name.log"; then echo "$name COMPILE-ERROR"; continue; fi
  if [ "$rc" -ne 0 ]; then echo "$name KILLED by: $fails"; else echo "$name SURVIVED"; fi
done
git -C "$T" status --short
