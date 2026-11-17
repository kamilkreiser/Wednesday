#!/bin/bash
# Gate driver: the builder's red-control runner, unchanged, on a scratch worktree with its own target dir.
W="$1"; OUT="$2"
export COAGENT_TOOLS="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
export RUSTUP_HOME="$COAGENT_TOOLS/rustup" CARGO_HOME="$COAGENT_TOOLS/cargo" PATH="$COAGENT_TOOLS/cargo/bin:$PATH"
export CARGO_TARGET_DIR="$3"
export CARGO_NET_OFFLINE=true
start=$(date +%s)
python3 "$W/crates/coagent-relay/red-controls/run.py" --with-dep > "$OUT" 2>&1
echo "exit=$? secs=$(( $(date +%s) - start ))" >> "$OUT"
