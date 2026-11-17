source /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/env_atk.sh
for g in gate gate_r2 gate_r3 gate_r4; do
  echo "=== $g"
  cargo test -j 4 --release --locked --manifest-path $C/Cargo.toml -p coagent-audit --test $g -- --ignored --nocapture 2>&1 | grep -E "^test |test result|panicked|R4-M1|requested events" | cut -c1-400
done
