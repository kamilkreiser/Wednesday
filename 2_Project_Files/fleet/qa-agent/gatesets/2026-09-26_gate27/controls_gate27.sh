#!/bin/bash
# controls_<kit>.sh — every guard of ONE gate27 kit (the directory this script lives in; kit.json beside it), run BOTH WAYS. Each control has a DOCTORED
# arm (one planted defect; the guard must refuse with its own exit code) and, where the mechanism is an override or a copied file, a PRISTINE twin
# through the SAME mechanism (defect not planted; must pass) — so a refusal is attributable to the defect, not to the harness. `--invert` flips every
# expectation: every control must then report MISMATCH (proves each control can fail and the harness can report it). Launches nothing: launcher
# controls use `--check` (headless) or stop at the non-TTY guard; repin controls use `--dry-run`, a bad argv, a routing-file override that stops at
# step 0, or G27_STOP_AFTER_3B in a MOVED COPY of the kit (the real re-pin runs there and nothing after it). Doctored arms are PINNED to the
# launcher's own develop (pchk) so a develop move mid-run cannot mask them as exit 17.
# EVERY MUTATION IS INDEPENDENT OF THE ORIGINAL (gate24T2d's H20 lesson: it appended an X to a real head, the doctored text still CONTAINED the real
# head, and the control could not fail): doctor() REFUSES (rc 98) a replacement that contains the text it replaces, and every wrong head here is the
# real head with ONE hex digit CHANGED (same length, never a superset); a removed phrase is SPLIT by ' ~ ' at a space so the original no longer occurs.
# Writes only under <scratchpad>/g27_controls_<kit>_*. Starts no container and binds no port.
# gate27 re-key: PS2 is `--simulate moved` (develop + an unrelated synthetic commit; no OLDER develop can host #1287), PF1 fills from its SIM pins.
# Usage: controls_<kit>.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_<kit>.sh <scratchpad> [--invert]"; exit 9;; esac
kj() { python3 -c 'import json,sys; k=json.load(open(sys.argv[1])); print(eval(sys.argv[2]))' "$GS/kit.json" "$1"; }
KIT="$(kj 'k["kit"]')"; OVR="QAB27_"
L="$GS/$(kj 'k["launcher"]')"; PR="$GS/$(kj 'k["prompt"]')"; CAP="$GS/mail_${KIT}_ready.md"; REPIN="$GS/repin_and_launch_${KIT}.sh"
NS="$(kj '" ".join(sorted(k["prs"]))')"; N1="${NS%% *}"; N2="$(echo $NS | cut -d' ' -f2)"
CW="$SP/g27_controls_${KIT}_$(date -u +%H%M%S)$([ "$INV" = 1 ] && echo _inv)"; mkdir -p "$CW"
OK=0; BAD=0; N=0
say() { printf '%s\n' "$*"; }
judge() { # $1 id, $2 want rc, $3 got rc, $4 label
  local want="$2"; N=$((N+1))
  if [ "$INV" = 1 ]; then
    if [ "$3" != "$want" ]; then OK=$((OK+1)); say "  OK       $1 (inverted: want != $want, got $3) — $4"; else BAD=$((BAD+1)); say "  MISMATCH $1 (inverted: want != $want, got $3) — $4"; fi
  else
    if [ "$3" = "$want" ]; then OK=$((OK+1)); say "  OK       $1 want $want got $3 — $4"; else BAD=$((BAD+1)); say "  MISMATCH $1 want $want got $3 — $4"; fi
  fi
}
# doctor <src> <dst> <old> <new|SPLIT>: a copy with ONE planted defect, every occurrence; refuses (99) if <old> is absent and (98) if the new text still
# CONTAINS the old one (a mutation that cannot make the guard fail)
doctor() { python3 - "$1" "$2" "$3" "$4" <<'PY'
import re, sys
s, d, o, n = sys.argv[1:5]
if n == 'SPLIT':
    i = o.find(' ', len(o) // 2); i = i if i > 0 else o.rfind(' ')
    n = o[:i] + ' ~' + o[i:] if i > 0 else o[:len(o) // 2] + '~' + o[len(o) // 2:]
if o in n: print('DOCTOR: the replacement %r CONTAINS the original — a control that cannot fail' % n[:80]); sys.exit(98)
t = open(s, encoding='utf-8').read()
rx = re.compile(r'\s+'.join(re.escape(w) for w in o.split(' ')))
t2, k = rx.subn(lambda m: n, t)
if k == 0: print('DOCTOR: anchor absent: %r' % o[:80]); sys.exit(99)
if o in re.sub(r'\n\s*', ' ', t2): print('DOCTOR: the original still occurs after the plant'); sys.exit(97)
open(d, 'w', encoding='utf-8').write(t2)
PY
}
chk() { "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pchk() { env "${OVR}CUR_DEV=${CUR_OVR:-$PDEV}" "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" > "$CW/$id.doctor" 2>&1 || { judge "$id" "$want" "D$?" "DOCTOR FAILED ($(cat "$CW/$id.doctor")): $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(env "${OVR}PROMPT=$CW/$id.prompt" "${OVR}CUR_DEV=$PDEV" "$L" --check > "$CW/$id.out" 2>&1; echo $?)" "$5"
  judge "$id/twin" 0 "$(env "${OVR}PROMPT=$CW/$id.pristine.prompt" "${OVR}CUR_DEV=$PDEV" "$L" --check > "$CW/$id.twin.out" 2>&1; echo $?)" "$5 — pristine copy through the same override"
}
ovr() { # id want label VAR=VAL... : a --check with test overrides (pinned develop)
  local id="$1" want="$2" lab="$3"; shift 3
  judge "$id" "$want" "$(env "$@" "${OVR}CUR_DEV=$PDEV" "$L" --check > "$CW/${id//\//.}.out" 2>&1; echo $?)" "$lab"
}
hd() { sed -n "s/^  \"$1|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|.*$/\1/p" "$L"; }
paths() { sed -n "s/^  \"$1|[^|]*|[^|]*|[0-9a-f]\{40\}|[0-9]*|[0-9]*|[0-9a-f]*|[0-9]*|\([^|]*\)|T[0-9]\"$/\1/p" "$L"; }
flip() { python3 -c 'import sys; h=sys.argv[1]; c=h[-1]; print(h[:-1] + ("0" if c != "0" else "1"))' "$1"; }
PDEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")"
for n in $NS; do [ -n "$(hd $n)" ] && [ -n "$(paths $n)" ] || { echo "REFUSING: could not read #$n's row from $L"; exit 9; }; done
[ -n "$PDEV" ] || { echo "REFUSING: no DEVELOP_SHA in $L"; exit 9; }
M1BASE="$(kj 'k["predev"]')"   # gate27: develop BEFORE gate26's eleven squashes (kit.json predev, 00de57baeb40) plays the moved-develop role
say "controls_${KIT}.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW | rows $NS | pinned develop $PDEV"

say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled"
H1="$(hd $N1)"; H2="$(hd $N2)"; F1="$(flip "$H1")"
case "$F1" in *"$H1"*) echo "REFUSING: the flipped head contains the real one"; exit 9;; esac
ovr C 6 "stale #$N1 head (all zeros)" "${OVR}HEAD_$N1=0000000000000000000000000000000000000000"
ovr C2 6 "#$N2's head pinned as #$N1's" "${OVR}HEAD_$N1=$H2"
ovr C3 6 "#$N1's head with ONE hex digit changed ($F1: same length, never a superset of the real head)" "${OVR}HEAD_$N1=$F1"
TW=(); for n in $NS; do TW+=("${OVR}HEAD_$n=$(hd $n)"); done
ovr C/twin 0 "every real head through the same overrides" "${TW[@]}"
judge D 17 "$(env "${OVR}CUR_DEV=$M1BASE" "$L" --check > "$CW/D.out" 2>&1; echo $?)" "develop moved (predev ${M1BASE:0:12} as the current develop)"
judge D/twin 0 "$(env "${OVR}CUR_DEV=$PDEV" "$L" --check > "$CW/D.twin.out" 2>&1; echo $?)" "the pinned develop through the same override"
VT=()
for n in $NS; do
  P0="$(paths $n)"; PW="$(python3 -c 'import sys; p=sys.argv[1].split(","); f=p[0]; i=f.rfind(".")-1; p[0]=f[:i]+("x" if f[i]!="x" else "y")+f[i+1:]; print(",".join(p))' "$P0")"
  ovr "V$n" 10 "base-invariant compare: #$n with ONE path's name changed by one character (same count)" "${OVR}PATHS_$n=$PW"
  VT+=("${OVR}PATHS_$n=$P0")
done
ovr V/twin 0 "the right paths through the same overrides" "${VT[@]}"
# the launcher's two `for _w in` lists: block 1 = the seat items, block 2 = the by-name keywords (bash single-quote escapes undone)
wlist() { python3 - "$L" "$1" <<'PY2'
import re, sys
blocks, cur = [], None
for l in open(sys.argv[1], encoding='utf-8'):
    l = l.rstrip('\n')
    if l == 'for _w in \\': cur = []; continue
    if cur is not None:
        m = re.match(r"^  '(.*)'( \\|; do)$", l)
        if m: cur.append(m.group(1).replace("'\\''", "'"))
        if not m or m.group(2) == '; do': blocks.append(cur); cur = None
for w in blocks[int(sys.argv[2]) - 1]: print(w)
PY2
}
SEAT1="$(wlist 1 | sed -n 2p)"
doctor "$CAP" "$CW/O.cap" "$SEAT1" SPLIT > "$CW/O.doctor" 2>&1 && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(env "${OVR}BRIEF=$CW/O.cap" "${OVR}CUR_DEV=$PDEV" "$L" --check > "$CW/O.out" 2>&1; echo $?)" "capture missing a seat item ('$SEAT1')"
judge O/twin 0 "$(env "${OVR}BRIEF=$CW/O.pristine.cap" "${OVR}CUR_DEV=$PDEV" "$L" --check > "$CW/O.twin.out" 2>&1; echo $?)" "pristine capture through the same override"
doctor "$CAP" "$CW/O2.cap" "$H1" "$F1" > "$CW/O2.doctor" 2>&1
judge O2 20 "$(env "${OVR}BRIEF=$CW/O2.cap" "${OVR}CUR_DEV=$PDEV" "$L" --check > "$CW/O2.out" 2>&1; echo $?)" "the capture names a WRONG #$N1 head (one digit changed, every occurrence)"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'THE PRS (read from origin' 'THE PRS {{UNFILLED}} (read from origin' "an unfilled fill token"
for n in $NS; do pctl "H$n" 20 "$(hd $n)" "$(flip "$(hd $n)")" "the prompt names a WRONG #$n head (one digit changed, every occurrence — never a superset)"; done
for n in $NS; do
  T0="$(sed -n "s/^  \"$n|\([^|]*\)|.*/\1/p" "$L")"; TK="$(python3 -c 'import re,sys; t=sys.argv[1]; m=list(re.finditer(r"\d+",t))[-1]; print(t[:m.start()]+str(int(m.group())+1)+t[m.end():])' "$T0")"
  pctl "T$n" 32 "PR #$n is $T0." "PR #$n is $TK." "ticket statement for #$n"
  TI="$(sed -n "s/^  \"$n|.*|\(T[0-9]\)\"$/\1/p" "$L")"; TJ="T$(( ${TI#T} == 1 ? 2 : 1 ))"
  pctl "I$n" 7 "#$n $TI" "#$n $TJ" "tier line for #$n ($TI)"
done
FZ="$(sed -n "s/^has 'The batch is FROZEN at \([a-z]*\)' .*/\1/p" "$L")"; FZ2="$([ "$FZ" = seven ] && echo eight || echo seven)"
pctl I0 7 "The batch is FROZEN at $FZ" "The batch is FROZEN at $FZ2" "the batch frozen at $FZ"
TD="$(sed -n "s/^has 'The batch is FROZEN at [a-z]*' \&\& has '\(.*\)' ||.*/\1/p" "$L")"
pctl I1 7 "$TD" SPLIT "the tier definition ('$TD')"
KW1="$(wlist 2 | sed -n 1p)"; KW2="$(wlist 2 | tail -n 1)"
pctl K 33 "$KW1" "${KW1:0:3}~${KW1:3}" "a by-name keyword ($KW1, every occurrence)"
pctl K2 33 "$KW2" "${KW2:0:3}~${KW2:3}" "a by-name keyword ($KW2, every occurrence)"
pctl B 34 'A sibling batch merging is not a difference' 'A sibling batch merging is a difference' "base-invariant rule"
pctl B2 34 'declare any overlap you find with its merged-blob target' 'ignore any overlap you find' "pairwise: declare any overlap with its merged-blob target"
pctl X 36 'restore by bytes' 'restore somehow' "red-proof rule: restore by bytes"
pctl X2 36 'in YOUR OWN clone' 'in the shared checkout' "red proof in the tester's own clone"
pctl F 37 'the count after this merge stays 28/0 · 6/0 · 49/0 · 60 of 60' 'the count after this merge stays 28/0 · 6/0 · 50/0 · 60 of 60' "fleet STOP after the merge (49/0, not 50/0)"
pctl F2 37 'NO STANDALONE RUN of' 'A STANDALONE RUN of' "fleet STOP: no standalone run of the hook suites"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl H2 39 'NO ticket filed' 'tickets may be filed' "holds: no ticket filed"
pctl L8 45 'They are NOT RUN in this gate' 'They are run as convenient in this gate' "legs 3/4/8 NOT run"
# the kit's own rules: the FIRST phrase of each, split (every occurrence), must refuse with that rule's exit
while IFS='|' read -r ex ph lab; do [ -n "$ex" ] && pctl "R$ex" "$ex" "$ph" SPLIT "kit rule: $lab"; done < <(python3 - "$L" <<'PY'
import re, sys
for l in open(sys.argv[1], encoding='utf-8'):
    m = re.match(r"^has '(.*?)' (?:&&.*)?\|\| \{ echo \"REFUSING: (.*?)\" >&2; exit (\d+); \}$", l.rstrip('\n'))
    if m and int(m.group(3)) >= 40 or (m and m.group(3) in ('35',) ) or (m and m.group(3) == '37' and 'NOT APPLICABLE' in l):
        print('%s|%s|%s' % (m.group(3), m.group(1).replace("'\\''", "'"), m.group(2)))
PY
)
GOS="$(sed -n "s/^has \"WEDNESDAY'S signed GO naming the head\" \&\& has '\([^']*\)' .*/\1/p" "$L")"
MA="$(sed -n "s/^has \"WEDNESDAY'S signed GO naming the head\" \&\& has '[^']*' \&\& has '\([^']*\)' .*/\1/p" "$L")"
pctl A 26 "$GOS" "\`GO: merge #$N1 batch\`" "the GO string"
pctl A2 26 "$MA" SPLIT "merge authority ('$MA')"
AC="$(sed -n "s/^has '## MERGE ADDENDUM' \&\& has '\([^']*\)' .*/\1/p" "$L")"
pctl E 25 "$AC" 'PER PR FILE' "addendum count ('$AC')"
pctl E2 25 'MG-11 each subject <= 92' 'MG-11 each subject <= 120' "addendum: MG-11 <= 92"
SUBJ="$(sed -n "s/^grep -qF -- '\(\[QA -> Wednesday\][^']*\)' .*/\1/p" "$L")"
pctl J 23 "$SUBJ" "${SUBJ% (*}" "the verdict subject"
say "--- moved kit and the launch path"
mkdir -p "$CW/moved"; cp "$L" "$CW/moved/"
judge M 2 "$("$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; echo $?)" "a MOVED launcher (copied out of its home) refuses"
judge TTY 21 "$("$L" < /dev/null > "$CW/TTY.out" 2>&1; echo $?)" "the LAUNCH path (no --check) with stdin not a TTY refuses before exec"

say "--- repin_and_launch (dry-run / argv / routing override / a MOVED COPY for the real re-pin)"
judge RA 9 "$("$REPIN" "$L" /tmp > "$CW/RA.out" 2>&1; echo $?)" "argv[2] not a session scratchpad"
printf 'QA/Some-other-pane|coagent@agentmail.to|yes\n' > "$CW/routing.absent"; printf '%s|coagent@agentmail.to|yes\n' "$(kj 'k["pane"]')" > "$CW/routing.present"
judge RB 1 "$(G27_ROUTING="$CW/routing.absent" "$REPIN" "$L" "$SP" > "$CW/RB.out" 2>&1; echo $?)" "the pane is not routed: a REAL run refuses at step 0 (nothing after it runs)"
judge RB/twin 0 "$(G27_ROUTING="$CW/routing.present" "$REPIN" "$L" "$SP" --dry-run > "$CW/RB.twin.out" 2>&1; echo $?)" "routed + --dry-run: every read agrees with the pins"
# a MOVED COPY at its own home: re-fill there (fill only — the pins are current), then plant the PRE-M1 develop as the launcher's pin
KC="$CW/kitcopy"; mkdir -p "$KC"; for f in kit.json pins_$KIT.json stopcounts_$KIT.json mail_${KIT}_ready.md prompt_$KIT.TEMPLATE.txt launcher_$KIT.TEMPLATE.sh.txt predict_gate27.py fill_gate27.py repin_and_launch_$KIT.sh $(basename "$(ls "$GS"/predict_[0-9]*.out | tail -1)") $(ls "$GS" | /usr/bin/grep '^gh_body_[0-9]*\.md$'); do cp "$GS/$f" "$KC/"; done
python3 "$KC/fill_gate27.py" > "$CW/KC.fill.out" 2>&1; judge KC 0 "$?" "fill in a MOVED copy (the copy becomes its own home)"
KL="$KC/$(basename "$L")"; KR="$KC/repin_and_launch_$KIT.sh"
judge KC/check 0 "$("$KL" --check > "$CW/KC.check.out" 2>&1; echo $?)" "the moved copy's launcher passes --check at its new home"
sed -i '' "s/^DEVELOP_SHA='$PDEV'$/DEVELOP_SHA='$M1BASE'/" "$KL"
judge RC 10 "$(G27_ROUTING="$CW/routing.present" "$KR" "$KL" "$SP" --dry-run > "$CW/RC.out" 2>&1; echo $?)" "a launcher pinned to predev ${M1BASE:0:12}: --dry-run REPORTS the move and exits 10"
judge RD 0 "$(G27_ROUTING="$CW/routing.present" G27_STOP_AFTER_3B=1 "$KR" "$KL" "$SP" > "$CW/RD.out" 2>&1; echo $?)" "the REAL re-pin across the move (step 3b: predict -> fill -> develop re-read), stopped right after 3b"
judge RD/pin 0 "$([ "$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$KL")" = "$PDEV" ]; echo $?)" "after the re-pin the copy's launcher pins the current develop again"
judge RD/check 0 "$("$KL" --check > "$CW/RD.check.out" 2>&1; echo $?)" "the re-pinned copy passes --check"
# the re-pin must REFUSE when the move cannot be proven base-invariant: an overlap predict cannot accept
sed -i '' "s/^DEVELOP_SHA='$PDEV'$/DEVELOP_SHA='$M1BASE'/" "$KL"
python3 - "$KC/kit.json" <<'PY'
import json, sys
k = json.load(open(sys.argv[1]))
assert not k['declared_overlap']                                       # gate27: no in-kit overlap declared (measured)
k['sibling_batch'] = k['sibling_batch'] + [sorted(k['prs'])[0]]        # a kit PR listed in the sibling kit too = a pairwise overlap
json.dump(k, open(sys.argv[1], 'w'), indent=1)
PY
judge RE 10 "$(G27_ROUTING="$CW/routing.present" G27_STOP_AFTER_3B=1 "$KR" "$KL" "$SP" > "$CW/RE.out" 2>&1; echo $?)" "the re-pin over a move predict cannot accept (a kit PR also listed in the sibling kit = a pairwise overlap) REFUSES rc 10"

say "--- predict / fill"
judge PS1 1 "$(python3 "$GS/predict_gate27.py" "$SP" --simulate "foreign$N2" > "$CW/PS1.out" 2>&1; echo $?)" "predict over develop + a FOREIGN edit of #$N2's first own file REFUSES"
judge PS2 0 "$(python3 "$GS/predict_gate27.py" "$SP" --simulate moved > "$CW/PS2.out" 2>&1; echo $?)" "predict over develop + an UNRELATED synthetic commit (a develop move no PR touches) PASSES"
KF="$CW/fillcopy"; mkdir -p "$KF"; for f in kit.json stopcounts_$KIT.json mail_${KIT}_ready.md prompt_$KIT.TEMPLATE.txt launcher_$KIT.TEMPLATE.sh.txt fill_gate27.py $(basename "$(ls "$GS"/predict_[0-9]*.out | tail -1)") $(ls "$GS" | /usr/bin/grep '^gh_body_[0-9]*\.md$'); do cp "$GS/$f" "$KF/"; done
cp "$GS/pins_$KIT.SIM-moved.json" "$KF/pins_$KIT.json"
judge PF1 1 "$(python3 "$KF/fill_gate27.py" > "$CW/PF1.out" 2>&1; echo $?)" "fill from SIMULATED pins refuses"
python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); p["fail"]=1; json.dump(p, open(sys.argv[2],"w"))' "$GS/pins_$KIT.json" "$KF/pins_$KIT.json"
judge PF2 1 "$(python3 "$KF/fill_gate27.py" > "$CW/PF2.out" 2>&1; echo $?)" "fill from pins carrying fail=1 refuses"
cp "$GS/pins_$KIT.json" "$KF/pins_$KIT.json"
judge PF/twin 0 "$(python3 "$KF/fill_gate27.py" > "$CW/PF.twin.out" 2>&1; echo $?)" "fill from the real pins in the same copy passes"

say "SUMMARY $KIT: $N controls, OK $OK, MISMATCH $BAD$([ "$INV" = 1 ] && echo ' (inverted: every control must MISMATCH-then-flip to OK; a MISMATCH here is a control that could not fail)')"
[ "$BAD" = 0 ]
