#!/bin/bash
# Gate probes (G1-G5) then the release property at 1,024 cases: committed seed and the gate's own seed.
export COAGENT_TOOLS=<work>/mc/tools CARGO_TARGET_DIR=<work>/mc/target
W=<work>
pushd "$W/atk" >/dev/null || exit 9
. scripts/env.sh
cargo test --locked -p coagent-roster --test qa_deputy_gate -- --nocapture > "$W/qa_gate.log" 2>&1; echo "QA exit $?" >> "$W/qa_gate.log"
for seed in 0xD3B07E5EED000001 0x6A7E00DE9D7A1120; do
  /usr/bin/time -p env COAGENT_DEPUTY_PROP_SEED=$seed COAGENT_DEPUTY_PROP_CASES=1024 cargo test --locked --release -p coagent-roster --test deputy_props -- --nocapture > "$W/prop_$seed.log" 2>&1
  echo "PROP exit $?" >> "$W/prop_$seed.log"
done
echo DONE > "$W/run_qa.done"
