W=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4
R=/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review
T=$W/clone/crates/coagent-audit/tests
for p in "gate_audit_tests/gate_attacks.rs gate_attacks.rs" "gate_audit_tests_r2/gate_r2.rs gate_r2.rs" "gate_audit_tests_r3/gate_r3.rs gate_r3.rs"; do
  set -- $p
  echo "== $2: ref $(shasum -a256 $R/$1|cut -c1-16) branch $(shasum -a256 $T/$2|cut -c1-16) at882e094 $(git -C $W/clone show 882e094:crates/coagent-audit/tests/$2 2>/dev/null | shasum -a256 | cut -c1-16) at4bc3d36 $(git -C $W/clone show 4bc3d36:crates/coagent-audit/tests/$2 2>/dev/null | shasum -a256 | cut -c1-16) origin/main $(git -C $W/clone show origin/main:crates/coagent-audit/tests/$2 2>/dev/null | shasum -a256 | cut -c1-16)"
  echo "diff lines vs ref: $(diff $R/$1 $T/$2 | grep -c '^[<>]')"
  echo "RULING markers in branch: $(grep -c 'RULING' $T/$2)"
done
echo "empty sha: $(printf '' | shasum -a256 | cut -c1-16)"
