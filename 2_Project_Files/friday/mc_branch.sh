#!/bin/bash
# Friday's merge check for one branch: clean clone, cargo fetch, scripts/check.sh, optional extra runner.
# usage: mc_branch.sh <work dir> <project repo> <project tools dir> <shared cargo home> <branch> [runner script relative to the clone]
W="$1"; R="$2"; T="$3"; CH="$4"; B="$5"; RUN="$6"
mkdir -p "$W"
git clone -q --branch "$B" "$R" "$W/clone" > "$W/clone.log" 2>&1
echo "clone_rc=$?" >> "$W/clone.log"
git -C "$W/clone" rev-parse HEAD > "$W/head.txt"
export CARGO_HOME="$CH" RUSTUP_HOME="$T/rustup" CARGO_TARGET_DIR="$W/target" PATH="$CH/bin:$PATH"
cargo fetch --locked --manifest-path "$W/clone/Cargo.toml" > "$W/fetch.log" 2>&1
echo "fetch_rc=$?" >> "$W/fetch.log"
( builtin pushd "$W/clone" > /dev/null && bash scripts/check.sh ) > "$W/check.log" 2>&1
echo "check_rc=$?" >> "$W/check.log"
if [ -n "$RUN" ]; then
  ( builtin pushd "$W/clone" > /dev/null && bash "$RUN" ) > "$W/red.log" 2>&1
  echo "red_rc=$?" >> "$W/red.log"
fi
git -C "$W/clone" status --short > "$W/status_after.txt"
cat "$W/head.txt"; tail -1 "$W/fetch.log"; tail -2 "$W/check.log"; [ -n "$RUN" ] && tail -3 "$W/red.log"; wc -l < "$W/status_after.txt"
