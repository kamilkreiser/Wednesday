#!/bin/bash
# Arms for fleet/gate_stray_check.sh — run against a scratch git tree, never the real one.
set -u
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHK="$SELF_DIR/../gate_stray_check.sh"
T="$(mktemp -d)"
git -C "$T" init -q && git -C "$T" -c user.name=a -c user.email=a@b commit -q --allow-empty -m init
PASS=0; FAIL=0
arm() { # name expected_rc [env...]
  local name="$1" want="$2"; shift 2
  env GATE_STRAY_TREE="$T" "$@" bash "$CHK" > "$T.out" 2>&1; local rc=$?
  if [ "$rc" = "$want" ]; then PASS=$((PASS+1)); echo "PASS $name (rc $rc)"; else FAIL=$((FAIL+1)); echo "FAIL $name (rc $rc, want $want)"; sed 's/^/    /' "$T.out"; fi
}
arm "clean tree" 0
mkdir -p "$T/0_Brain/reference/x" && echo v > "$T/0_Brain/reference/x/verdict.md"
arm "verdict in 0_Brain/reference is allowed" 0
mkdir -p "$T/2_Project_Files/local-model/night/briefs/ks_1" && echo b > "$T/2_Project_Files/local-model/night/briefs/ks_1/b.md"
arm "screen brief dir is allowed" 0
mkdir -p "$T/node_modules/.vite" && echo r > "$T/node_modules/.vite/results.json"
arm "root node_modules is a stray (the AJ1/AQ1 shape)" 1
arm "stray with a stated override passes" 0 GATE_STRAY_OK='arms test'
mv "$T/node_modules" "$T.nm_moved"
echo x > "$T/r2"
arm "root file r2 is a stray (the AL1 shape)" 1
mv "$T/r2" "$T.r2_moved"
mkdir -p "$T/2_Project_Files/tools" && echo t > "$T/2_Project_Files/tools/new.sh"
arm "a new file in 2_Project_Files/tools is a stray" 1
mv "$T/2_Project_Files/tools/new.sh" "$T.tool_moved"
arm "back to clean after moves" 0
env GATE_STRAY_TREE="$T/does-not-exist" bash "$CHK" > "$T.out" 2>&1; rc=$?
if [ "$rc" = 2 ]; then PASS=$((PASS+1)); echo "PASS not-a-tree refuses (rc 2)"; else FAIL=$((FAIL+1)); echo "FAIL not-a-tree (rc $rc, want 2)"; fi
echo "ARMS: $PASS pass, $FAIL fail (scratch tree $T left in place, not deleted)"
[ "$FAIL" = 0 ]
