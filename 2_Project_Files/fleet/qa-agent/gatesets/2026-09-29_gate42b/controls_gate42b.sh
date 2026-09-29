#!/bin/bash
# controls_gate42b.sh — every guard in the gate42b kit driven on the REAL subject and on PLANTED defects, each with the rc it must give (and, where it
# refuses, a WHY pattern its refusing line must carry — a refusal for the wrong reason is a MISMATCH).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants are written ONLY under <scratchpad>/g42b_sp/controls_<HHMMSS>/. The kit's own files are never edited. The launcher runs with --check
# (headless) except L10, which runs the real launch path with stdin NOT a TTY (it must refuse rc 21 before exec; skipped as MISMATCH if stdin is a TTY).
# The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) — both stop long before the usage gate / cockpit.
# Usage: controls_gate42b.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g42b_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g42b_sp/clone"; L="$GS/launch_qa_secuura_batch1340.sh"; PROMPT="$GS/2026-09-29_secuura-batch1340.prompt.txt"; CAP="$GS/mail_gate42b_ready.md"
P() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/pins_gate42b.json" "$1"; }
HEAD="$(P head)"; DEV="$(P develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"
BP='Blockchain/Dev/scripts/audit/audit-baseline.json'
git -C "$CL" show "$DEV:$BP" > "$W/base.json"; git -C "$CL" show "$HEAD:$BP" > "$W/head.json"
TOT=0; OK=0; MM=0
ctl() { # ctl <id> <expected rc> <why regex or ''> -- <command...>
  local id="$1" exp="$2" why="$3"; shift 4
  local out rc good; out="$("$@" 2>&1)"; rc=$?
  good=0; [ "$rc" = "$exp" ] && { [ -z "$why" ] || printf '%s' "$out" | grep -qE -- "$why"; } && good=1
  [ "$INV" = 1 ] && good=$((1 - good))
  TOT=$((TOT + 1)); if [ "$good" = 1 ]; then OK=$((OK + 1)); v=OK; else MM=$((MM + 1)); v=MISMATCH; fi
  printf 'CONTROL %-5s expect rc %s%s | got rc %s -> %s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|MATCH|all guards|DRY RUN COMPLETE|utcToday' | tail -1 | cut -c1-170)"
}
plant() { # plant <name> <python expression over h (head dict) or b (base dict)>; writes $W/<name>.json from head.json
  python3 - "$W/head.json" "$W/$1.json" "$2" <<'PY'
import json, sys
h = json.load(open(sys.argv[1])); a = h['accepted']
exec(sys.argv[3])
json.dump(h, open(sys.argv[2], 'w'), indent=2)
PY
}
FC="$GS/fieldcheck_gate42b.py"
echo "=== controls_gate42b $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | head $HEAD | develop $DEV | plants $W"
echo "--- fieldcheck (requirements 1 + 2)"
ctl FC0 0 'FIELDCHECK PASS' -- python3 "$FC" "$SP"
plant p1 "a['GHSA-ggr8-5vv4-36mx']['expires']='2026-11-30'";               ctl FC1 1 'FAIL F5' -- python3 "$FC" "$SP" --head-file "$W/p1.json"
plant p2 "a['GHSA-frvp-7c67-39w9']['ticket']='KS-729'";                    ctl FC2 1 'FAIL F6 GHSA-frvp' -- python3 "$FC" "$SP" --head-file "$W/p2.json"
plant p3 "a['GHSA-wrjc-x8rr-h8h6']['expires']='2026-10-10'";               ctl FC3 1 'FAIL F7 GHSA-wrjc' -- python3 "$FC" "$SP" --head-file "$W/p3.json"
plant p4 "del a['GHSA-w5hq-g745-h8pq']";                                   ctl FC4 1 'FAIL F3' -- python3 "$FC" "$SP" --head-file "$W/p4.json"
plant p5 "h['extra']=1";                                                   ctl FC5 1 'FAIL F2' -- python3 "$FC" "$SP" --head-file "$W/p5.json"
ctl FC6 1 'FAIL F1' -- python3 "$FC" "$SP" --files "$BP,Blockchain/Dev/package.json"
plant p7 "import json as j; b=j.load(open(sys.argv[1].replace('head.json','base.json')))['accepted']; a['GHSA-337j-9hxr-rhxg']=b['GHSA-337j-9hxr-rhxg']"
ctl FC7 1 'FAIL F5' -- python3 "$FC" "$SP" --head-file "$W/p7.json"
sed 's/GHSA-mwp4-54f8-5fhr/GHSA-v2v4-37r5-5v8g/' <<< "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["authority"]["text"])' "$GS/kit.json")" > "$W/auth_swapped.txt"
ctl FC8 1 'FAIL F5' -- python3 "$FC" "$SP" --authority "$W/auth_swapped.txt"
plant p9 "a['GHSA-frvp-7c67-39w9']['reason']='X'+a['GHSA-frvp-7c67-39w9']['reason']"; ctl FC9 1 'FAIL F9 GHSA-frvp' -- python3 "$FC" "$SP" --head-file "$W/p9.json"
plant p10 "h['\$comment']=h['\$comment']+' '";                             ctl FC10 1 'FAIL F2' -- python3 "$FC" "$SP" --head-file "$W/p10.json"
plant p11 "a['GHSA-frvp-7c67-39w9']['expires']='2026-09-30'; a['GHSA-frvp-7c67-39w9']['reason']=a['GHSA-frvp-7c67-39w9']['reason']"; ctl FC11 1 'FAIL F10' -- python3 "$FC" "$SP" --head-file "$W/p11.json"
echo "--- keyscan (requirement 5)"
KS="$GS/keyscan_gate42b.py"; SUBJ="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["subject"])' "$GS/kit.json")"
python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["mandated_body"])' "$GS/kit.json" > "$W/body.txt"
ctl KS0 0 'KEYSCAN PASS' -- python3 "$KS" "$SP"
ctl KS1 1 'FAIL S2' -- python3 "$KS" "$SP" --subject "$SUBJ (#1340)"
ctl KS2 1 'FAIL S1' -- python3 "$KS" "$SP" --subject "KS-530: re-date the four rows (KS-493 wave) to 2026-10-09"
ctl KS3 1 'FAIL S3' -- python3 "$KS" "$SP" --subject "$SUBJ and a tail that pushes it past the ninety-two limit"
grep -v '^Refs KS-528$' "$W/body.txt" > "$W/body_norefs.txt";            ctl KS4 1 'FAIL B1 KS-528' -- python3 "$KS" "$SP" --body-file "$W/body_norefs.txt"
{ cat "$W/body.txt"; echo "Closes KS-530"; } > "$W/body_close.txt";      ctl KS5 1 'FAIL B2' -- python3 "$KS" "$SP" --body-file "$W/body_close.txt"
{ cat "$W/body.txt"; echo "  - GHSA-v2v4-37r5-5v8g (ip-address, KS-470)"; } > "$W/body_foreign.txt"; ctl KS6 1 'FAIL B3' -- python3 "$KS" "$SP" --body-file "$W/body_foreign.txt"
echo "--- the clock-freeze preload (requirement 4: positive arm + refusal), through the REPO's OWN baseline-contract.mjs"
"$GS/run_fuseproof_gate42b.sh" "$SP" > "$W/fuseproof.out" 2>&1
PL="$GS/clockfreeze_gate42b.mjs"; FP="$GS/fuseproof_gate42b.mjs"; C="$SP/g42b_sp/fuse/head/baseline-contract.mjs"; HB="$SP/g42b_sp/fuse/head/audit-baseline.json"; BB="$SP/g42b_sp/fuse/base/audit-baseline.json"
ctl CK0 0 'utcToday 2026-09-30 ' -- env G42B_FROZEN_NOW=2026-09-30T00:01:00Z node --import "$PL" "$FP" "$C" "$HB"
ctl CK1 97 'REFUSING — G42B_FROZEN_NOW is unset' -- env -u G42B_FROZEN_NOW node --import "$PL" "$FP" "$C" "$HB"
ctl CK2 97 'is not an ISO-8601' -- env G42B_FROZEN_NOW=notadate node --import "$PL" "$FP" "$C" "$HB"
ctl CK3 0 "utcToday $(date -u +%Y-%m-%d) " -- node "$FP" "$C" "$HB"
ctl CK4 0 'FROZEN CLOCK 2026-10-10T00:01:00.000Z' -- env G42B_FROZEN_NOW=2026-10-10T00:01:00Z node --import "$PL" -e 'console.log(new Date().toISOString(), Date.now())'
echo "--- the fuse predicate (requirement 4, offline: rows that CAN lapse)"
FOUR='GHSA-337j-9hxr-rhxg,GHSA-frvp-7c67-39w9,GHSA-mwp4-54f8-5fhr,GHSA-wrjc-x8rr-h8h6'
ctl FU0 0 '^MATCH' -- env G42B_FROZEN_NOW=2026-09-30T00:01:00Z node --import "$PL" "$FP" "$C" "$BB" 'GHSA-frvp-7c67-39w9,GHSA-mwp4-54f8-5fhr'
ctl FU1 0 '^MATCH' -- env G42B_FROZEN_NOW=2026-09-30T00:01:00Z node --import "$PL" "$FP" "$C" "$HB" ''
ctl FU2 0 '^MATCH' -- env G42B_FROZEN_NOW=2026-10-10T00:01:00Z node --import "$PL" "$FP" "$C" "$HB" "$FOUR"
ctl FU3 0 '^MATCH' -- env G42B_FROZEN_NOW=2026-10-08T23:59:00Z node --import "$PL" "$FP" "$C" "$HB" ''
ctl FU4 1 'NO MATCH' -- env G42B_FROZEN_NOW=2026-09-30T00:01:00Z node --import "$PL" "$FP" "$C" "$BB" ''
ctl FU5 1 'NO MATCH' -- env G42B_FROZEN_NOW=2026-09-30T00:01:00Z node --import "$PL" "$FP" "$C" "$HB" 'GHSA-frvp-7c67-39w9'
ctl FU6 0 'FUSEPROOF PASS' -- cat "$W/fuseproof.out"
echo "--- the launcher (--check; L10 the real launch path, non-TTY)"
ctl L0 0 'all guards pass' -- "$L" --check
ctl L1 6 'is not at .* AND refs/pull/1340/head' -- env G42B_HEAD="$DEV" "$L" --check
ctl L2 17 'origin develop .* != the pinned develop' -- env G42B_CUR_DEV="$OLDDEV" "$L" --check
ctl L3 10 'the compare is not the pinned' -- env G42B_PATHS="Blockchain/Dev/package.json" "$L" --check
sed "s/GO (Seat B 44th): merge 1340 on gate42b/GO (Seat B 43rd): merge 1340 on gate42b/g" "$PROMPT" > "$W/prompt_go.txt";       ctl L4 26 'merge authority / the GO string' -- env G42B_PROMPT="$W/prompt_go.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/prompt_tok.txt";                                                                   ctl L5 8 'unfilled double-brace' -- env G42B_PROMPT="$W/prompt_tok.txt" "$L" --check
sed "s/FUSE-HEAD-GREEN/FUSE-HEAD-GRN/g" "$PROMPT" > "$W/prompt_kw.txt";                                                          ctl L6 33 "by-name keyword 'FUSE-HEAD-GREEN'" -- env G42B_PROMPT="$W/prompt_kw.txt" "$L" --check
sed "s/(KS-528) to 2026-10-09. The real/(KS-528) to 2026-10-10. The real/g" "$PROMPT" > "$W/prompt_kam.txt";                     ctl L7 34 "Kam's instruction verbatim" -- env G42B_PROMPT="$W/prompt_kam.txt" "$L" --check
sed "s/$HEAD/${HEAD:0:39}x/g" "$CAP" > "$W/cap_nohead.md";                                                                       ctl L8 20 'do not both name' -- env G42B_BRIEF="$W/cap_nohead.md" "$L" --check
sed "s/NO baseline edit/NO baseline change/g" "$PROMPT" > "$W/prompt_hold.txt";                                                   ctl L9 39 'the HOLDS' -- env G42B_PROMPT="$W/prompt_hold.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L10  SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L10 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/prompt_dev.txt";                                                                     ctl L11 31 'launch develop / the END_TREE' -- env G42B_PROMPT="$W/prompt_dev.txt" "$L" --check
echo "--- the launch action (repin: --dry-run; R1 a real run refusing at step 0)"
R="$GS/repin_and_launch_gate42b.sh"
ctl R0 0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
: > "$W/routing_empty.conf";                                               ctl R1 1 'is not registered in inbox_routing.conf' -- env G42B_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2 15 'another open PR touches the path' -- env G42B_OVERLAP_PATH="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
sed "s/|$HEAD|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh"; ctl R3 11 'the head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R4 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R5 9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "--- the pin script (refuses a head it was not given; writes nothing on refusal)"
PS="$(shasum -a 256 "$GS/pins_gate42b.json" | cut -c1-64)"
ctl PN0 1 'P1 head .* != the expected' -- python3 "$GS/pin_gate42b.py" "$SP" --expect-head "$DEV"
ctl PN1 0 '' -- test "$(shasum -a 256 "$GS/pins_gate42b.json" | cut -c1-64)" = "$PS"
echo "SUMMARY gate42b: $TOT controls, OK $OK, MISMATCH $MM$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
