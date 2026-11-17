# my three anchor guards (gate_r5 r5_guard_*) under the surviving mutants R17 R18 R23 R26, in copy mut1
source /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/env_atk.sh
S=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5
M=$S/mut/mut1
for id in R17 R18 R23 R26; do
  echo "=== $id"
  python3 -c "
import sys; sys.path.insert(0, '$S/out'); import mutate_r5 as m, os
mm=[x for x in m.MUTANTS if x[0]=='$id'][0]; m.apply(os.path.join('$M', mm[2]), mm[3], mm[4])"
  CARGO_TARGET_DIR=$S/mut/target_mut1 cargo test -j 4 --offline --locked --manifest-path $M/Cargo.toml -p coagent-audit --test gate_r5 r5_guard -- --nocapture 2>&1 | grep -E "^r5|^test |panicked|^  left|^ right|failed:" | cut -c1-300
  git -C $M checkout -- crates/coagent-audit/src
done
git -C $M status --short
