#!/bin/bash
# g7_busy_leg_arms.sh — red-proof for night_run.sh's G7 BUSY leg (2026-09-17).
# Ledger w=3 (2026-09-16 21:2x, "idle on a worked day" — REGRESSION): Ornith sat idle 20:50 -> 21:20 while
# the coordinator was busy with Claude seats; G7's 2 h panel alert woke nobody in time and never reached the
# coordinator's pane. The BUSY leg: while night/ALLOW_SEATS is live, an EMPTY default queue for
# NIGHT_IDLE_BUSY_MIN minutes taps the coordinator pane with a bare pointer (rate-limited).
# Every arm runs on a SCRATCH tmux socket (one pane named 'wednesday' so G2 passes), a scratch queue, a
# scratch marker dir and log dir, a STUB cockpit that records its arguments, and NIGHT_IDLE_ALERT_H=999 so
# the 2 h leg can never post to Kam's real panel. G3 is pointed at a pattern nothing matches; G4's load cap
# is lifted; G5 reads the real ollama /api/tags with the self-heal OFF (an arm that stops at G5 says so).
#   ARM 1  FIRE: allowance live, drought 25 min            -> stub tapped 'wednesday' with the pointer
#   ARM 2  QUIET: allowance live, drought 5 min            -> no tap
#   ARM 3  QUIET: no allowance file, drought 60 min        -> no tap (the 2 h panel leg governs)
#   ARM 4  QUIET: allowance EXPIRED, drought 60 min        -> no tap
#   ARM 5  RATE LIMIT: allowance live, last tap 5 min ago  -> no tap
#   ARM 6  RE-FIRE: allowance live, last tap 25 min ago    -> tap
#   ARM 7  NEGATIVE: the OLD runner on ARM 1's state       -> no tap (proves the arms discriminate)
#   ARM 8  the pointer the runner builds passes cockpit.sh say's OWN no-mail guards (length + the
#          authorising-verb pattern read out of cockpit.sh, not re-implemented)
# Usage: bash g7_busy_leg_arms.sh <new night_run.sh> <old night_run.sh>
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEW="${1:?new runner}"; OLD="${2:?old runner}"
COCKPIT="$HERE/../../fleet/cockpit/cockpit.sh"
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
W="$(mktemp -d "${TMPDIR:-/tmp}/g7busy.XXXXXX")"
SOCK="g7arms$$"
PASS=0; FAIL=0
: > "$W/queue.md"
cat > "$W/stub_cockpit.sh" <<'STUB'
#!/bin/bash
printf '%s\n' "$*" >> "$G7_TAP_REC"
STUB
chmod +x "$W/stub_cockpit.sh"
now() { date +%s; }

run_arm() { # $1 label  $2 runner  $3 allow(live|none|expired)  $4 drought_min  $5 last_tap_min_ago(or -)
  local d="$W/$1"; mkdir -p "$d/mk" "$d/log"
  case "$3" in
    live)    printf '%s\n%s\n' "$(( $(now) + 3600 ))" "arms: live" > "$d/ALLOW_SEATS";;
    expired) printf '%s\n%s\n' "$(( $(now) - 60 ))" "arms: expired" > "$d/ALLOW_SEATS";;
    none)    : ;;
  esac
  echo "$(( $(now) - $4 * 60 ))" > "$d/mk/.queue_empty_since"
  [ "$5" = "-" ] || echo "$(( $(now) - $5 * 60 ))" > "$d/mk/.queue_empty_tapped"
  G7_TAP_REC="$d/tap.txt" NIGHT_TMUX_SOCKET="$SOCK" NIGHT_QUEUE="$W/queue.md" NIGHT_IDLE_DEFAULT_QUEUE="$W/queue.md" \
  NIGHT_IDLE_MARKER_DIR="$d/mk" NIGHT_LOG_DIR="$d/log" NIGHT_ALLOW_SEATS_FILE="$d/ALLOW_SEATS" \
  NIGHT_COCKPIT="$W/stub_cockpit.sh" NIGHT_IDLE_ALERT_H=999 NIGHT_IDLE_ALERT_DRY=0 NIGHT_DRY_RUN=1 \
  NIGHT_QA_PGREP='__g7_arms_matches_nothing__' NIGHT_MAX_LOAD=999 NIGHT_G5_SELFHEAL=0 NIGHT_DERIVE_DRY=1 \
    bash "$2" > "$d/out.txt" 2>&1
  echo "rc=$?" >> "$d/out.txt"
}
reached_queue() { /usr/bin/grep -q 'has no pending ticket' "$W/$1/out.txt"; }
tapped() { [ -s "$W/$1/tap.txt" ]; }
ok()  { echo "PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
expect_tap() { # $1 arm  $2 name
  if ! reached_queue "$1"; then bad "$2 — never reached the empty-queue branch: $(/usr/bin/grep -E 'REFUSE|GATE G5' "$W/$1/out.txt" | tail -1)"; return; fi
  if tapped "$1" && /usr/bin/grep -q '^say wednesday Ornith queue empty since' "$W/$1/tap.txt"; then ok "$2 ($(head -1 "$W/$1/tap.txt" | cut -c1-90))"; else bad "$2 — no tap recorded"; fi
}
expect_quiet() {
  if ! reached_queue "$1"; then bad "$2 — never reached the empty-queue branch: $(/usr/bin/grep -E 'REFUSE|GATE G5' "$W/$1/out.txt" | tail -1)"; return; fi
  if tapped "$1"; then bad "$2 — tapped: $(head -1 "$W/$1/tap.txt")"; else ok "$2"; fi
}

"$TMUX_BIN" -L "$SOCK" new-session -d -s fleet -x 80 -y 20 'sleep 600'
"$TMUX_BIN" -L "$SOCK" set-option -p -t fleet:0.0 @cockpit_name wednesday

run_arm a1 "$NEW" live 25 -;     expect_tap   a1 "ARM1 FIRE live allowance, 25-min drought"
run_arm a2 "$NEW" live 5 -;      expect_quiet a2 "ARM2 QUIET 5-min drought"
run_arm a3 "$NEW" none 60 -;     expect_quiet a3 "ARM3 QUIET no allowance"
run_arm a4 "$NEW" expired 60 -;  expect_quiet a4 "ARM4 QUIET expired allowance"
run_arm a5 "$NEW" live 60 5;     expect_quiet a5 "ARM5 RATE LIMIT last tap 5 min ago"
run_arm a6 "$NEW" live 60 25;    expect_tap   a6 "ARM6 RE-FIRE last tap 25 min ago"
run_arm a7 "$OLD" live 25 -;     expect_quiet a7 "ARM7 NEGATIVE old runner"

# ARM 8 — the real pointer text from ARM 1 against cockpit.sh's own guards
PTR="$(head -1 "$W/a1/tap.txt" 2>/dev/null | sed 's/^say wednesday //')"
PAT="$(/usr/bin/grep -o "grep -qiE '[^']*'" "$COCKPIT" | head -1 | sed "s/^grep -qiE '//; s/'\$//")"
MAXP="$(/usr/bin/grep -o 'SAY_MAX_PTR:-[0-9]*' "$COCKPIT" | head -1 | tr -dc '0-9')"
if [ -z "$PTR" ] || [ -z "$PAT" ] || [ -z "$MAXP" ]; then
  bad "ARM8 instrument incomplete (ptr=${#PTR} pat=${#PAT} max=$MAXP)"
elif [ "${#PTR}" -gt "$MAXP" ]; then
  bad "ARM8 pointer ${#PTR} chars > $MAXP"
elif printf '%s' "$PTR" | /usr/bin/grep -qiE "$PAT"; then
  bad "ARM8 pointer carries an authorising verb: $PTR"
elif ! printf '%s' "Wednesday says proceed" | /usr/bin/grep -qiE "$PAT"; then
  bad "ARM8 CONTROL: the extracted pattern did not fire on a known authorising line (pattern extraction broken)"
else
  ok "ARM8 pointer ${#PTR}/$MAXP chars, no authorising verb (control fired on 'proceed')"
fi

"$TMUX_BIN" -L "$SOCK" kill-server 2>/dev/null
echo "RESULT: $PASS passed, $FAIL failed (work dir kept: $W)"
[ "$FAIL" -eq 0 ]
