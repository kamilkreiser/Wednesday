#!/bin/bash
# c2_regen_gate55.sh — gate55 C2: the YAML is REGENERATED, not hand-patched; `check:openapi` rc 0. bash 3.2 / zsh safe; no rc via a pipe.
#   plan [REPO]             READ ONLY (git cat-file / rev-parse / show / grep on the shared checkout or your clone): the YAML blob at base and
#                           head == kit base_blobs / drafted_head_blobs (and they differ); the generator script + both npm scripts exist; the
#                           transfer.openapi.ts module is imported by the test and by NO non-test transfer source (so it is not runtime code).
#   regen WS OUT            head WS (installed): sha256 of the committed YAML (== kit spec_yaml_sha256_head) -> `npm run generate-openapi` at
#                           Blockchain/Dev -> sha256 AFTER == before and `git status --porcelain` empty (a byte-identical regeneration);
#                           POSITIVE ARM: `npm run generate-openapi -- --check` rc 0 with `CHECK PASS`. A different YAML is a FINDING: the
#                           regenerated file is kept in OUT, the committed blob restored, sha256 proven.
#   control WS OUT          head WS: the YAML set to its BASE blob -> `npm run generate-openapi -- --check` MUST be rc 1 with `CHECK FAIL:
#                           generated YAML differs`, and the file's sha256 UNCHANGED by the check (it wrote nothing); restored from the head
#                           blob, sha256 proven, worktree clean. (The control that proves the drift check can fail on THIS change.)
#   checkopenapi WS OUT     head WS: `npm run check:openapi` rc 0 (its two legs: generate --check + check:spec-examples; the example count
#                           printed); CONTROL: one planted YAML line -> rc != 0; restored, sha256 proven, worktree clean.
# REFUSES (rc 2, before writing) a WS inside /Volumes/DevMASTER/!CODING/, a dirty WS, a WS whose HEAD^{tree} is not kit expected_tree, an
# OUT inside !CODING/ other than the QA reports root (guards_gate55.sh). rc 0 PASS / 1 FAIL / 2 refusal / 3 a tool step failed.
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
. "$GS/guards_gate55.sh"
Y="$(KJ spec_yaml)"; YB0="$(KB base_blobs "$(KJ spec_yaml)")"; YB1="$(KB drafted_head_blobs "$(KJ spec_yaml)")"; YSHA="$(KJ spec_yaml_sha256_head)"
usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; }
npmrun() {  # npmrun <name> <args...> in Blockchain/Dev (subshell cd)
  _n="$1"; shift
  ( cd "$DEV" && npm run "$@" ) > "$OUTR/$_n.out" 2> "$OUTR/$_n.err"; _rc=$?; echo "$_rc" > "$OUTR/$_n.rc"; echo "  npm run $* rc=$_rc ($(date -u +%H:%M:%SZ))"
  return $_rc
}
CMD="${1:-}"
case "$CMD" in
  ''|-h|--help) usage; [ -n "$CMD" ] && exit 0; exit 2;;
  plan)
    REPO="${2:-$(KJ checkout)}"; B="$(KJ base)"; H="$(KJ expected_head)"; F=0
    echo "C2 PLAN $(date -u +%Y-%m-%dT%H:%M:%SZ) | repo $REPO (READ ONLY) | base ${B:0:12} | head ${H:0:12}"
    git -C "$REPO" cat-file -e "$H:$Y.g55-absent-control" 2> /dev/null; crc=$?
    yb="$(git -C "$REPO" rev-parse "$B:$Y" 2> /dev/null)"; yh="$(git -C "$REPO" rev-parse "$H:$Y" 2> /dev/null)"
    if [ "$yb" = "$YB0" ] && [ "$yh" = "$YB1" ] && [ "$yb" != "$yh" ] && [ "$crc" != 0 ]; then echo "PASS R1 yaml blob base $yb == kit, head $yh == kit, they differ (absent-path control rc $crc: rev-parse cannot echo a fake)"; else echo "FAIL R1 yaml base '$yb' head '$yh' kit $YB0 / $YB1 (control rc $crc)"; F=1; fi
    P="$(git -C "$REPO" show "$H:Blockchain/Dev/package.json" 2> /dev/null | python3 -c 'import json,sys; s=json.load(sys.stdin)["scripts"]; print(s.get("generate-openapi","ABSENT")); print(s.get("check:openapi","ABSENT"))')"
    git -C "$REPO" cat-file -e "$H:Blockchain/Dev/scripts/generate-openapi.ts" 2> /dev/null; grc=$?
    echo "  scripts at head: generate-openapi = '$(printf '%s' "$P" | sed -n 1p)' | check:openapi = '$(printf '%s' "$P" | sed -n 2p)' | scripts/generate-openapi.ts present rc $grc"
    case "$P" in *ABSENT*) F=1; echo "FAIL R2 an npm script is absent";; *) [ "$grc" = 0 ] && echo "PASS R2 both scripts and the generator exist" || { F=1; echo "FAIL R2 generator absent"; };; esac
    imp="$(git -C "$REPO" grep -l -F 'transfer.openapi' "$H" -- 'Blockchain/Dev/services/transfer/src' 2> /dev/null | sed "s#^$H:##")"
    nt="$(printf '%s\n' "$imp" | grep -c '/__tests__/')"; nr="$(printf '%s\n' "$imp" | grep -v '^$' | grep -v '/__tests__/' | grep -v 'transfer.openapi.ts$' | grep -c .)"
    echo "  importers of transfer.openapi under services/transfer/src at head: tests $nt (MUST-HIT, want >= 1: the ks1015 test) | non-test runtime files $nr (want 0)"
    [ "$nt" -ge 1 ] && [ "$nr" = 0 ] && echo "PASS R3 transfer.openapi.ts is spec-registration only (no runtime importer)" || { echo "FAIL R3"; F=1; }
    echo "  RUN PLAN: c3 install WS_HEAD OUT; regen WS_HEAD OUT; control WS_HEAD OUT; checkopenapi WS_HEAD OUT"
    [ "$F" = 0 ] && { echo "C2 PLAN OK"; exit 0; }; echo "C2 PLAN FAIL"; exit 1;;
  regen)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_ws "$WS" head; guard_out "$O"; echo "C2 REGEN $(date -u +%Y-%m-%dT%H:%M:%SZ) | OUT $OUTR"
    s0="$(sha "$WSR/$Y")"; l0="$(wc -l < "$WSR/$Y" | tr -d ' ')"; q0="$(grep -c 'required: true' "$WSR/$Y")"
    echo "  committed YAML sha256 $s0 (kit $YSHA: $([ "$s0" = "$YSHA" ] && echo equal || echo DIFFERS)) | $l0 lines | 'required: true' $q0"
    npmrun regen generate-openapi; r1=$?
    s1="$(sha "$WSR/$Y")"; l1="$(wc -l < "$WSR/$Y" | tr -d ' ')"; q1="$(grep -c 'required: true' "$WSR/$Y")"
    echo "  AFTER regeneration sha256 $s1 | $l1 lines | 'required: true' $q1 | byte-identical to the committed blob: $([ "$s0" = "$s1" ] && echo YES || echo NO)"
    clean_or_fail regen_after; r2=$?
    if [ "$s0" != "$s1" ]; then
      mkdir -p "$OUTR/quarantine" && cp "$WSR/$Y" "$OUTR/quarantine/regenerated.secuura-api.yaml" && git -C "$WSR" diff --stat > "$OUTR/regen_diffstat.out" 2>&1
      put_blob "$YB1" "$Y"; echo "  FINDING: the generator does NOT reproduce the committed YAML; regenerated copy kept in OUT/quarantine; restored sha256 $(sha "$WSR/$Y" | cut -c1-16)"
    fi
    npmrun regen_check generate-openapi -- --check; r3=$?; pl="$(grep -c 'CHECK PASS' "$OUTR/regen_check.out")"
    echo "  POSITIVE ARM --check rc $r3, 'CHECK PASS' lines $pl"
    [ "$r1" = 0 ] && [ "$s0" = "$YSHA" ] && [ "$s0" = "$s1" ] && [ "$r2" = 0 ] && [ "$r3" = 0 ] && [ "$pl" -ge 1 ] && { echo "C2 REGEN PASS (generate-openapi reproduces the committed YAML byte-identically; --check rc 0)"; exit 0; }
    echo "C2 REGEN FAIL"; exit 1;;
  control)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_ws "$WS" head; guard_out "$O"; echo "C2 CONTROL $(date -u +%Y-%m-%dT%H:%M:%SZ) | OUT $OUTR"
    put_blob "$YB0" "$Y"; rc=$?; s0="$(sha "$WSR/$Y")"
    echo "  YAML set to its BASE blob ${YB0:0:12}: rc $rc, sha256 $s0"
    npmrun control_check generate-openapi -- --check; r1=$?; fl="$(grep -c 'CHECK FAIL: generated YAML differs' "$OUTR/control_check.err" "$OUTR/control_check.out" | awk -F: '{s+=$NF} END {print s+0}')"
    s1="$(sha "$WSR/$Y")"
    echo "  reverted-YAML --check rc $r1 (want 1) | 'CHECK FAIL: generated YAML differs' lines $fl (want >= 1) | sha256 after the check $s1: unchanged $([ "$s0" = "$s1" ] && echo YES || echo NO)"
    put_blob "$YB1" "$Y"; s2="$(sha "$WSR/$Y")"
    echo "  restored from the head blob ${YB1:0:12}: sha256 $s2 == kit $([ "$s2" = "$YSHA" ] && echo YES || echo NO)"
    clean_or_fail control_after; r2=$?
    [ "$rc" = 0 ] && [ "$r1" = 1 ] && [ "$fl" -ge 1 ] && [ "$s0" = "$s1" ] && [ "$s2" = "$YSHA" ] && [ "$r2" = 0 ] && { echo "C2 CONTROL PASS (the drift check refuses the pre-change YAML and writes nothing)"; exit 0; }
    echo "C2 CONTROL FAIL"; exit 1;;
  checkopenapi)
    WS="${2:-}"; O="${3:-}"; [ -n "$WS" ] && [ -n "$O" ] || { usage; exit 2; }
    guard_ws "$WS" head; guard_out "$O"; echo "C2 CHECK:OPENAPI $(date -u +%Y-%m-%dT%H:%M:%SZ) | OUT $OUTR"
    npmrun checkopenapi check:openapi; r1=$?
    echo "  example-block line: $(grep -h -i -o '[0-9,]* example block[^|]*' "$OUTR/checkopenapi.out" "$OUTR/checkopenapi.err" | head -1)"
    s0="$(sha "$WSR/$Y")"; printf '\n# g55 drift-control plant\n' >> "$WSR/$Y"
    npmrun checkopenapi_planted check:openapi; r2=$?
    put_blob "$YB1" "$Y"; s1="$(sha "$WSR/$Y")"
    echo "  CONTROL planted line rc $r2 (want non-zero) | restored sha256 equal $([ "$s0" = "$s1" ] && echo YES || echo NO)"
    clean_or_fail checkopenapi_after; r3=$?
    [ "$r1" = 0 ] && [ "$r2" != 0 ] && [ "$s0" = "$s1" ] && [ "$r3" = 0 ] && { echo "C2 CHECK:OPENAPI PASS"; exit 0; }
    echo "C2 CHECK:OPENAPI FAIL"; exit 1;;
  *) usage; exit 2;;
esac
