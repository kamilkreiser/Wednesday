#!/bin/bash
# g2_allow_seats_arms.sh — red-proof for night_run.sh's G2 SEATS ALLOWANCE (2026-09-16).
# Kam 20:40: keep the local model working WHILE Claude seats run. G2 refused whenever a foreign
# fleet pane was live; the allowance is a FILE (line 1 expiry epoch, line 2 reason). Arms, all on a
# SCRATCH tmux socket holding a 'fleet' session with ONE foreign pane, an EMPTY scratch queue (nothing
# runs), and a scratch NIGHT_LOG_DIR (own lock, own log):
#   ARM 1  no allowance file              -> G2 REFUSE   (the defect-free old behaviour, kept)
#   ARM 2  allowance, expiry in the future -> G2 ALLOWED ... pass
#   ARM 3  allowance, expiry in the past   -> G2 REFUSE   (a scoped override expires on its own)
#   ARM 4  allowance, garbage line 1       -> G2 REFUSE
#   ARM 5  CONTROL: no foreign pane        -> G2 "none foreign — pass" (the allowance is not consulted)
# Usage: bash local-model/tests/g2_allow_seats_arms.sh [night_run.sh path]  (default: the live one)
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="${1:-$HERE/../night/night_run.sh}"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
W="$(mktemp -d "${TMPDIR:-/tmp}/g2allow.XXXXXX")"
SOCK="g2arms$$"
PASS=0; FAIL=0
: > "$W/queue.md"

run_gates() { # $1 = label ; prints the G2 line
  rm -rf "$W/log_$1"; mkdir -p "$W/log_$1"
  NIGHT_TMUX_SOCKET="$SOCK" NIGHT_QUEUE="$W/queue.md" NIGHT_LOG_DIR="$W/log_$1" \
  NIGHT_ALLOW_SEATS_FILE="$W/ALLOW_SEATS" NIGHT_DRY_RUN=1 bash "$RUNNER" > "$W/out_$1.txt" 2>&1
  /usr/bin/grep 'GATE G2' "$W/out_$1.txt" | tail -1
}
check() { # $1 name  $2 line  $3 pattern
  case "$2" in *"$3"*) echo "PASS: $1"; PASS=$((PASS+1));; *) echo "FAIL: $1 — got: $2"; FAIL=$((FAIL+1));; esac
}

"$TMUX_BIN" -L "$SOCK" new-session -d -s fleet -x 80 -y 20 'sleep 600'
"$TMUX_BIN" -L "$SOCK" set-option -p -t fleet:0.0 @cockpit_name wednesday
"$TMUX_BIN" -L "$SOCK" split-window -t fleet:0 'sleep 600'
"$TMUX_BIN" -L "$SOCK" set-option -p -t fleet:0.1 @cockpit_name "Secuura/Blockchain-A"

L=$(run_gates a1); check "ARM1 no allowance file -> REFUSE" "$L" "REFUSE (other agents run)"
printf '%s\n%s\n' "$(( $(date +%s) + 3600 ))" "arms: Kam 20:40 seats + local model" > "$W/ALLOW_SEATS"
L=$(run_gates a2); check "ARM2 future expiry -> ALLOWED pass" "$L" "ALLOWED by"
printf '%s\n%s\n' "$(( $(date +%s) - 60 ))" "arms: expired" > "$W/ALLOW_SEATS"
L=$(run_gates a3); check "ARM3 past expiry -> REFUSE" "$L" "REFUSE (other agents run)"
printf 'tomorrow\nbad\n' > "$W/ALLOW_SEATS"
L=$(run_gates a4); check "ARM4 unparseable -> REFUSE" "$L" "REFUSE (other agents run)"
"$TMUX_BIN" -L "$SOCK" kill-pane -t fleet:0.1
L=$(run_gates a5); check "ARM5 CONTROL no foreign pane -> none foreign pass" "$L" "none foreign — pass"

"$TMUX_BIN" -L "$SOCK" kill-server 2>/dev/null
echo "RESULT: $PASS passed, $FAIL failed (work dir kept: $W)"
[ "$FAIL" -eq 0 ]
