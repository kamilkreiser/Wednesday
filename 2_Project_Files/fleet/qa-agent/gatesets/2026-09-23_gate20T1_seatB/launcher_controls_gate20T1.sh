#!/bin/bash
# launcher_controls_gate20T1.sh <launcher> <prompt> <scratch dir> — the negative controls, each on a COPY of the prompt / the launcher or an override
# (never the real files). Works on the REAL launcher (seven rows) and on the CONTROL COPY (six rows, PR 11 not yet raised; CONTROL_COPY=1):
# C STALE HEAD (the last row's head with its last hex digit changed) -> 6 · D develop at BASE 2bc5ccf63 (a stale develop; content-judged 17 disjoint) ->
# 17/18/19 · E develop at #1204's head (a tier-1 blob LANDED) -> 19 · S PARTIAL (PENDING-PR- planted in the prompt) -> 34 · P11a a launcher COPY whose
# last row's head is PENDING (not 40-hex) -> 34 · P11b a launcher COPY with the last row REMOVED -> 34 · X (real launcher only) the prompt carrying the
# control marker PR11-NOT-YET-RAISED -> 34 · G no thinking directive -> 8 · O RULE WHETHER IT BLOCKS reworded -> 30 · L a by-name keyword reworded -> 33 ·
# I #1204 demoted to T2 -> 7 · U the PR 11 self-testing phrase reworded -> 35 · V the #1208 generator phrase reworded -> 36 · B the base-move phrase
# reworded -> 38 · Y the #1210 FINDING phrase reworded -> 39 · T a BOTH token altered (verify_pr21.py) -> 30 · N non-TTY launch -> 21 · K (CONTROL COPY
# only) a launch under a pseudo-TTY (python pty.fork) -> 37 — never run against a real launcher, which would start the gate · POSITIVE --check -> 0.
set -u
L="$1"; P="$2"; SP="$3"
case "$SP" in /private/tmp/claude-501/*/scratchpad*) ;; *) echo "REFUSING: $SP is not a scratchpad"; exit 9;; esac
CC="$(sed -n 's/^CONTROL_COPY=\([01]\)$/\1/p' "$L")"
D="$(mktemp -d "$SP/controls_gate20T1.XXXXXX")"
LASTROW="$(sed -n '/^PRS=($/,/^)$/p' "$L" | /usr/bin/grep '^  "' | tail -1)"
LASTN="$(printf '%s' "$LASTROW" | sed 's/^  "\([0-9]*\)|.*/\1/')"; LASTH="$(printf '%s' "$LASTROW" | sed -E 's/.*\|([0-9a-f]{40})\|[0-9]+"$/\1/')"
STALE="${LASTH%?}$( [ "${LASTH: -1}" = 0 ] && echo 1 || echo 0 )"
echo "controls start $(date -u +%Y-%m-%dT%H:%M:%SZ) dir $D | launcher $L (CONTROL_COPY=$CC) | last row #$LASTN head $LASTH | stale stand-in $STALE"
ok=0; bad=0
run() { name="$1"; want="$2"; shift 2; "$@" > "$D/$name.out" 2>&1; rc=$?; case " $want " in *" $rc "*) echo "OK   $name rc $rc (want $want)"; ok=$((ok+1));; *) echo "MISMATCH $name rc $rc (want $want) — $D/$name.out"; bad=$((bad+1));; esac; }
env | /usr/bin/grep -c '^QAB1204_' > "$D/env_overrides.count" 2>&1; echo "  (QAB1204_* variables already in the environment: $(cat "$D/env_overrides.count") — must be 0)"
run C_stale_head_last 6 env "QAB1204_HEAD_${LASTN}=${STALE}" bash "$L" --check
run D_curdev_stale_BASE "17 18 19" env QAB1204_CUR_DEV=2bc5ccf63b8c40911afb568b03cace066238ffcf bash "$L" --check
run E_curdev_is_1204_head_LANDED 19 env QAB1204_CUR_DEV=6edffa3a96d08a96b4fd016b65bf12c10cd67869 bash "$L" --check
sed '3s/^/PENDING-PR-11 /' "$P" > "$D/S.txt"; run S_partial_prompt 34 env QAB1204_PROMPT="$D/S.txt" bash "$L" --check
sed -E "s/^(  \"${LASTN}\|KS-[0-9]+\|[^|]*\|)[0-9a-f]{40}(\|[0-9]+\")$/  \"PENDING|KS-1143|refs\/heads\/feature\/ks-1143-pending|PENDING-PR-11|1\"/" "$L" > "$D/L_p11a.sh"
echo "  (P11a copy: PENDING rows $(/usr/bin/grep -c 'PENDING-PR-11|1"' "$D/L_p11a.sh") — must be 1 for the control to mean anything)"
run P11a_last_row_pending 34 bash "$D/L_p11a.sh" --check
/usr/bin/grep -v -E "^  \"${LASTN}\|" "$L" > "$D/L_p11b.sh"
echo "  (P11b copy: rows naming #$LASTN left $(/usr/bin/grep -c -E "^  \"${LASTN}\|" "$D/L_p11b.sh") — must be 0; the launcher under test: $(/usr/bin/grep -c -E "^  \"${LASTN}\|" "$L") — must be 1)"
run P11b_last_row_removed 34 bash "$D/L_p11b.sh" --check
if [ "$CC" = 0 ]; then sed '3s/$/ PR11-NOT-YET-RAISED/' "$P" > "$D/X.txt"; run X_control_prompt_on_real_launcher 34 env QAB1204_PROMPT="$D/X.txt" bash "$L" --check; fi
sed 's/^ultrathink$/think/' "$P" > "$D/G.txt"; run G_no_thinking_directive 8 env QAB1204_PROMPT="$D/G.txt" bash "$L" --check
sed 's/RULE WHETHER IT BLOCKS/decide if it blocks/g' "$P" > "$D/O.txt"; run O_both_rule_reworded 30 env QAB1204_PROMPT="$D/O.txt" bash "$L" --check
sed 's/READ THE WHOLE TEST FILE/read the test file/g' "$P" > "$D/Lx.txt"; run L_byname_reworded 33 env QAB1204_PROMPT="$D/Lx.txt" bash "$L" --check
sed 's/#1204 T1/#1204 T2/' "$P" > "$D/I.txt"; run I_1204_regraded 7 env QAB1204_PROMPT="$D/I.txt" bash "$L" --check
sed 's/THE GATE PROVES RED-FIRST BY HUNK/the gate checks red-first/g' "$P" > "$D/U.txt"; run U_selftest_rule_reworded 35 env QAB1204_PROMPT="$D/U.txt" bash "$L" --check
sed 's/THE GATE VERIFIES THE YAML IS EXACTLY WHAT/the gate looks at whether the YAML matches what/g' "$P" > "$D/V.txt"; run V_specregen_rule_reworded 36 env QAB1204_PROMPT="$D/V.txt" bash "$L" --check
sed 's/grade over the develop read at launch/grade over develop/g' "$P" > "$D/B.txt"; run B_basemove_rule_reworded 38 env QAB1204_PROMPT="$D/B.txt" bash "$L" --check
sed 's/THE RULED DANGLING-COMMENT FINDING MUST BE IN THE BODY AS STATED/the finding should be mentioned/g' "$P" > "$D/Y.txt"; run Y_bodyclaims_rule_reworded 39 env QAB1204_PROMPT="$D/Y.txt" bash "$L" --check
sed 's/verify_pr21\.py/verify_pr22.py/g' "$P" > "$D/T.txt"; run T_both_token_altered 30 env QAB1204_PROMPT="$D/T.txt" bash "$L" --check
run N_nontty_launch 21 bash "$L" < /dev/null
PTYRUN='import os, pty, sys
pid, fd = pty.fork()
if pid == 0: os.execvp("bash", ["bash", sys.argv[1]])
out = b""
while True:
    try: d = os.read(fd, 4096)
    except OSError: break
    if not d: break
    out += d
sys.stdout.write(out.decode("utf-8", "replace")); _, st = os.waitpid(pid, 0); sys.exit(os.waitstatus_to_exitcode(st))'
if [ "$CC" = 1 ] && /usr/bin/grep -qx 'CONTROL_COPY=1' "$L"; then run K_control_copy_pty_launch 37 python3 -c "$PTYRUN" "$L"; fi
run POSITIVE_check 0 bash "$L" --check
echo "controls end $(date -u +%Y-%m-%dT%H:%M:%SZ): $ok OK / $bad MISMATCH (dir $D)"
[ "$bad" -eq 0 ]
