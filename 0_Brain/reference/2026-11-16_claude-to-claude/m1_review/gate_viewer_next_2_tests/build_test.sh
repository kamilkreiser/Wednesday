#!/bin/bash
# usage: build_test.sh <name> [runs]  : build workspace bins, touch .rs, run la_fields_narrow --exact <runs> times. Logs in $W/<name>/
set -u
W=/private/tmp/claude-501/qvx2; N="$1"; R="${2:-1}"
. /Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_viewer_next_2_tests/env.sh
export CARGO_TARGET_DIR="$W/$N/target"
M="$W/$N/src/Cargo.toml"
find "$W/$N/src" -name '*.rs' -exec touch {} +
cargo build --workspace --bins --locked --manifest-path "$M" > "$W/$N/build.log" 2>&1; echo "build exit $?" >> "$W/$N/build.log"
for i in $(seq 1 "$R"); do
  cargo test -p coagent-daemon --locked --manifest-path "$M" --test la_wrap -- --exact la_fields_narrow > "$W/$N/run$i.log" 2>&1; echo "test exit $?" >> "$W/$N/run$i.log"
done
