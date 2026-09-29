#!/bin/bash
# run_fuseproof_gate42b.sh — the drafter's OFFLINE fuse predicate, five arms, printed as `ARM <name> rc <n>: <result>`. Extracts (git show, from the
# scratch clone, at the pinned develop and head) audit-baseline.json and the repo's OWN baseline-contract.mjs into <scratchpad>/g42b_sp/fuse/{base,head},
# then runs fuseproof_gate42b.mjs under clockfreeze_gate42b.mjs. NOT legs 6/7 (no advisory fetched): the rows that CAN lapse; the gate owes the real legs.
# Writes only under <scratchpad>/g42b_sp/fuse. rc 0 iff every arm matched its expectation. Usage: run_fuseproof_gate42b.sh <scratchpad>
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; CL="$SP/g42b_sp/clone"; F="$SP/g42b_sp/fuse"; PATH_='Blockchain/Dev/scripts/audit'
P() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/pins_gate42b.json" "$1"; }
mkdir -p "$F/base" "$F/head"
for s in "base:$(P develop)" "head:$(P head)"; do d="${s%%:*}"; c="${s#*:}"
  git -C "$CL" show "$c:$PATH_/audit-baseline.json" > "$F/$d/audit-baseline.json" || exit 2
  git -C "$CL" show "$c:$PATH_/baseline-contract.mjs" > "$F/$d/baseline-contract.mjs" || exit 2
done
PL="$GS/clockfreeze_gate42b.mjs"; FP="$GS/fuseproof_gate42b.mjs"; C="$F/head/baseline-contract.mjs"
FOUR='GHSA-337j-9hxr-rhxg,GHSA-frvp-7c67-39w9,GHSA-mwp4-54f8-5fhr,GHSA-wrjc-x8rr-h8h6'
bad=0
arm() { local name="$1" at="$2" side="$3" exp="$4" out rc
  out="$(G42B_FROZEN_NOW="$at" node --import "$PL" "$FP" "$C" "$F/$side/audit-baseline.json" "$exp" 2>/dev/null)"; rc=$?
  echo "ARM $name rc $rc: $side baseline @ $at -> $(printf '%s' "$out" | tr '\n' ' ')"; [ "$rc" = 0 ] || bad=1; }
arm base-0930 2026-09-30T00:01:00Z base 'GHSA-frvp-7c67-39w9,GHSA-mwp4-54f8-5fhr'
arm head-0930 2026-09-30T00:01:00Z head ''
arm head-1008 2026-10-08T23:59:00Z head ''
arm head-1009 2026-10-09T00:01:00Z head "$FOUR"
arm head-1010 2026-10-10T00:01:00Z head "$FOUR"
echo "FUSEPROOF $([ $bad = 0 ] && echo PASS || echo FAIL) at $(date -u +%Y-%m-%dT%H:%M:%SZ) (contract blob sha256 $(shasum -a 256 "$C" | cut -c1-16))"
exit $bad
