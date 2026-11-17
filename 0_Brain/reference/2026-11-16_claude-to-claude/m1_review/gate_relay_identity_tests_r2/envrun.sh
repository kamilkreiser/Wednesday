#!/bin/bash
# usage: envrun.sh <target-dir> <log> <cwd> cmd...
export COAGENT_TOOLS="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
export RUSTUP_HOME="$COAGENT_TOOLS/rustup" CARGO_HOME="$COAGENT_TOOLS/cargo" PATH="$COAGENT_TOOLS/cargo/bin:$PATH" CARGO_NET_OFFLINE=true
export CARGO_TARGET_DIR="$1"; LOG="$2"; WD="$3"; shift 3
start=$(date +%s)
( cd "$WD" && "$@" ) > "$LOG" 2>&1
echo "exit=$? secs=$(( $(date +%s) - start ))" >> "$LOG"
