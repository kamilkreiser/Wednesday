#!/bin/bash
# pane_close_typed_arms.sh — red-proof for pane_close.sh's TYPED-UNSENT gate (ledger row 2026-09-17:
# `pane_prompt_check.sh %25` printed `⚠ TYPED, UNSENT ... :: do` and a chained `pane_close.sh %25` closed the
# pane anyway, losing a line Kam had typed). The NEW script runs the detector itself and refuses rc 7 on a typed
# line (unless --typed-ok) and rc 8 when the detector cannot give a verdict.
#
# Runs ONLY in the scratch tmux session `pctest` (refuses to start if it already exists — then it is not ours).
# Every pane id is checked against ^%[0-9]+$ AND session_name==pctest before any close; the real `fleet` session's
# pane list + @cockpit_name values are snapshotted before and after and must be identical. Never touches `fleet`.
# The detector-failure arms run a COPY of the new pane_close.sh beside a STUB pane_prompt_check.sh in a temp dir
# (no bypass env var exists in the real script). Temp dir is left in place (never-delete rule).
#
# Fixtures (read from pane_prompt_check.sh): it greps capture-pane -e lines holding '❯', strips through the glyph
# and the U+00A0 after it; non-empty text WITHOUT SGR 2 (ESC[2m) = TYPED, WITH it = SUGGESTION, nothing = empty.
#   typed      — interactive bash whose PS1 is '❯ ', text sent with send-keys -l and NO Enter
#   empty      — the same shell, nothing typed
#   suggestion — a pane that printf's '❯ ' + ESC[2m ghost text ESC[0m, then sleeps
#
# Arms:
#   a  typed           NEW -> rc 7, typed line + instruction printed, pane survives; OLD on the same pane -> rc 0, closed (negative control)
#   b  typed+override  NEW --typed-ok -> rc 0, closed, "OVERRIDE USED" printed
#   c  empty           NEW -> rc 0 closed; OLD on a twin empty pane -> rc 0 closed (same as old)
#   c2 suggestion      NEW -> rc 0 closed
#   d  %99999          NEW -> refuses non-zero, nothing killed (pctest pane set unchanged)
#   d2 stub rc 3       copy of NEW + stub detector exiting 3            -> rc 8, pane survives
#   d3 stub garbage    stub prints an unrecognised line, rc 0           -> rc 8, pane survives
#   d4 stub silent     stub prints nothing, rc 0                        -> rc 8, pane survives
#   d5 stub pane-gone  stub kills the (scratch) pane, prints "prompt empty" -> rc 8 (vacuous empty refused)
#   e  fleet snapshot  identical before/after
# Usage: pane_close_typed_arms.sh [path-to-new-pane_close.sh]   (default: cockpit/pane_close.sh)
set -u
FLEET=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet
NEW="${1:-$FLEET/cockpit/pane_close.sh}"
OLD=$FLEET/cockpit/pane_close.sh.pre-0917-typedok
DET=$FLEET/cockpit/pane_prompt_check.sh
TMUX_BIN=$(command -v tmux || echo /opt/homebrew/bin/tmux)
S=pctest
W=$(mktemp -d "${TMPDIR:-/tmp}/pane_close_typed_arms.XXXXXX")
P=$'\xe2\x9d\xaf\xc2\xa0'   # ❯ + NO-BREAK SPACE, exactly what the detector matches
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "ARM PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "ARM FAIL $1"; }
die() { echo "ABORT: $1"; exit 99; }

[ -f "$NEW" ] && [ -f "$OLD" ] && [ -f "$DET" ] || die "missing NEW=$NEW or OLD=$OLD or DET=$DET"
if "$TMUX_BIN" has-session -t "=$S" > /dev/null 2>&1; then die "session $S already exists — not ours, refusing to run"; fi

fleet_snap() { "$TMUX_BIN" list-panes -a -F '#{session_name}|#{pane_id}|#{@cockpit_name}' 2>/dev/null | awk -F'|' '$1=="fleet"'; }
pct_snap()   { "$TMUX_BIN" list-panes -s -t "=$S" -F '#{pane_id}' 2>/dev/null | sort; }
exists()     { [ "$("$TMUX_BIN" display -p -t "$1" '#{pane_id}' 2>/dev/null)" = "$1" ]; }
guard() { # $1 pane id: must be %N AND in session pctest, else ABORT the whole run
  [[ "$1" =~ ^%[0-9]+$ ]] || die "target guard: '$1' is not a %N pane id"
  [ "$("$TMUX_BIN" display -p -t "$1" '#{session_name}' 2>/dev/null)" = "$S" ] || die "target guard: $1 is not in session $S"
}

FLEET_BEFORE="$(fleet_snap)"
[ -n "$FLEET_BEFORE" ] || echo "note: no fleet session panes visible (snapshot empty) — arm e still compares"
echo "fleet snapshot before: $(printf '%s\n' "$FLEET_BEFORE" | wc -l | tr -d ' ') panes"

"$TMUX_BIN" new-session -d -s "$S" -x 200 -y 30 'sleep 3600' || die "could not create scratch session"
echo "scratch session $S created"

shell_pane() { # → id of a new interactive bash pane at a '❯ ' prompt
  local id i
  id=$("$TMUX_BIN" new-window -d -t "=$S:" -P -F '#{pane_id}' "env BASH_SILENCE_DEPRECATION_WARNING=1 PS1='$P' /bin/bash --norc --noprofile -i")
  guard "$id"
  for i in $(seq 1 25); do "$TMUX_BIN" capture-pane -p -t "$id" | LC_ALL=C grep -aq '❯' && break; sleep 0.2; done
  echo "$id"
}
typed_pane() { # → shell pane with $1 typed at the prompt, NOT sent
  local id i; id=$(shell_pane); guard "$id"
  "$TMUX_BIN" send-keys -t "$id" -l "$1"
  for i in $(seq 1 25); do "$TMUX_BIN" capture-pane -p -t "$id" | LC_ALL=C grep -aqF "$1" && break; sleep 0.2; done
  echo "$id"
}
sugg_pane() {
  local id i
  id=$("$TMUX_BIN" new-window -d -t "=$S:" -P -F '#{pane_id}' "printf '\\342\\235\\257\\302\\240\\033[2mghost suggestion text\\033[0m\\n'; exec sleep 3600")
  guard "$id"
  for i in $(seq 1 25); do "$TMUX_BIN" capture-pane -p -t "$id" | LC_ALL=C grep -aq 'ghost suggestion' && break; sleep 0.2; done
  echo "$id"
}
verdict() { /bin/bash "$DET" "$1" 2>&1; }
run() { # $1 script, $2 target pane (GUARDED), rest = the full argv passed to the script; output → $W/out; echoes rc
  local script=$1 target=$2; shift 2
  guard "$target"
  /bin/bash "$script" "$@" > "$W/out" 2>&1; echo $?
}
show() { sed 's/^/      | /' "$W/out"; }

# ---- fixture validity: the detector MUST print each verdict, or stop (no faking) ----
T1=$(typed_pane 'hello from a human'); guard "$T1"; V=$(verdict "$T1"); echo "fixture typed      $T1 :: $V"
case "$V" in *"⚠ TYPED, UNSENT"*"hello from a human") ;; *) "$TMUX_BIN" kill-session -t "=$S"; die "detector did not print TYPED-UNSENT for the typed fixture — cannot test honestly";; esac
E1=$(shell_pane); guard "$E1"; V=$(verdict "$E1"); echo "fixture empty      $E1 :: $V"
case "$V" in *": prompt empty") ;; *) "$TMUX_BIN" kill-session -t "=$S"; die "detector did not print 'prompt empty' for the empty fixture";; esac
S1=$(sugg_pane); guard "$S1"; V=$(verdict "$S1"); echo "fixture suggestion $S1 :: $V"
case "$V" in *"SUGGESTION (Claude ghost text"*"ghost suggestion text") ;; *) "$TMUX_BIN" kill-session -t "=$S"; die "detector did not print SUGGESTION for the suggestion fixture";; esac

# ---- a: typed → NEW refuses rc 7, pane survives; OLD closes it (negative control) ----
rc=$(run "$NEW" "$T1" "$T1"); echo "  a NEW $T1 rc=$rc"; show
if [ "$rc" = 7 ] && exists "$T1" && /usr/bin/grep -qi 'typed line :: hello from a human' "$W/out" && /usr/bin/grep -qi 're-run with --typed-ok' "$W/out"; then
  ok "a  typed: NEW REFUSED rc 7, line + instruction printed, pane $T1 still exists"
else bad "a  typed: NEW rc=$rc exists=$(exists "$T1" && echo yes || echo no)"; fi
guard "$T1"; rc=$(run "$OLD" "$T1" "$T1"); echo "  a OLD $T1 rc=$rc"; show
if [ "$rc" = 0 ] && ! exists "$T1"; then ok "a  negative control: OLD closed the same typed pane (rc 0) — the bug the gate fixes"
else bad "a  negative control: OLD rc=$rc exists=$(exists "$T1" && echo yes || echo no)"; fi

# ---- b: --typed-ok (placed BEFORE the pane id, to exercise arg parsing) → closes ----
T2=$(typed_pane 'second human line'); echo "fixture typed      $T2 :: $(verdict "$T2")"
guard "$T2"; rc=$(run "$NEW" "$T2" --typed-ok "$T2"); echo "  b NEW --typed-ok $T2 rc=$rc"; show
if [ "$rc" = 0 ] && ! exists "$T2" && /usr/bin/grep -qi 'OVERRIDE USED' "$W/out"; then ok "b  --typed-ok: closed (rc 0), override announced"
else bad "b  --typed-ok: rc=$rc exists=$(exists "$T2" && echo yes || echo no)"; fi

# ---- c: empty → NEW closes; OLD closes a twin (same as old) ----
guard "$E1"; rc=$(run "$NEW" "$E1" "$E1"); echo "  c NEW $E1 rc=$rc"; show
if [ "$rc" = 0 ] && ! exists "$E1"; then ok "c  empty: NEW closed (rc 0)"; else bad "c  empty: NEW rc=$rc exists=$(exists "$E1" && echo yes || echo no)"; fi
E2=$(shell_pane); echo "fixture empty      $E2 :: $(verdict "$E2")"
guard "$E2"; rc=$(run "$OLD" "$E2" "$E2"); echo "  c OLD $E2 rc=$rc"
if [ "$rc" = 0 ] && ! exists "$E2"; then ok "c  empty: OLD closed its twin (rc 0) — same outcome"; else bad "c  empty: OLD rc=$rc"; fi

# ---- c2: suggestion → NEW closes ----
guard "$S1"; rc=$(run "$NEW" "$S1" "$S1"); echo "  c2 NEW $S1 rc=$rc"; show
if [ "$rc" = 0 ] && ! exists "$S1"; then ok "c2 suggestion: NEW closed (rc 0)"; else bad "c2 suggestion: rc=$rc exists=$(exists "$S1" && echo yes || echo no)"; fi

# ---- d: %99999 → refuses, nothing killed ----
exists %99999 && die "%99999 unexpectedly exists"
PCT_BEFORE="$(pct_snap)"; FLEET_MID="$(fleet_snap)"
/bin/bash "$NEW" %99999 > "$W/out" 2>&1; rc=$?; echo "  d NEW %99999 rc=$rc"; show
if [ "$rc" != 0 ] && [ "$(pct_snap)" = "$PCT_BEFORE" ] && [ "$(fleet_snap)" = "$FLEET_MID" ] && /usr/bin/grep -qi 'REFUSED' "$W/out"; then
  ok "d  %99999: REFUSED rc $rc, no scratch or fleet pane killed"
else bad "d  %99999: rc=$rc"; fi

# ---- d2-d5: detector failures, via a COPY of NEW beside a stub detector ----
stub_run() { # $1 arm label, $2 stub body, $3 expect-pane-survives (yes|no) → asserts rc 8
  local label=$1 body=$2 survive=$3 dir id rc
  dir="$W/$label"; mkdir -p "$dir"; cp "$NEW" "$dir/pane_close.sh"
  printf '#!/bin/bash\n%s\n' "$body" > "$dir/pane_prompt_check.sh"
  id=$(shell_pane); guard "$id"
  rc=$(run "$dir/pane_close.sh" "$id" "$id"); echo "  $label stub-copy $id rc=$rc"; show
  if [ "$rc" = 8 ] && /usr/bin/grep -qi 'detector could not give a verdict' "$W/out" \
     && { [ "$survive" = no ] || exists "$id"; }; then ok "$label: REFUSED rc 8 (fail closed)$([ "$survive" = yes ] && echo ", pane $id survives")"
  else bad "$label: rc=$rc exists=$(exists "$id" && echo yes || echo no)"; fi
}
stub_run d2-stub-rc3     'echo "detector blew up" >&2; exit 3' yes
stub_run d3-stub-garbage 'echo "  $1: something this parser has never seen"; exit 0' yes
stub_run d4-stub-silent  'exit 0' yes
stub_run d5-stub-panegone '[[ "$1" =~ ^%[0-9]+$ ]] && [ "$(tmux display -p -t "$1" "#{session_name}")" = pctest ] && tmux kill-pane -t "$1"; echo "  $1: prompt empty"; exit 0' no

# ---- e: the real fleet is unchanged ----
FLEET_AFTER="$(fleet_snap)"
if [ "$FLEET_AFTER" = "$FLEET_BEFORE" ]; then ok "e  fleet snapshot unchanged ($(printf '%s\n' "$FLEET_AFTER" | awk 'NF' | wc -l | tr -d ' ') panes, ids + @cockpit_name)"
else bad "e  fleet snapshot CHANGED"; diff <(printf '%s\n' "$FLEET_BEFORE") <(printf '%s\n' "$FLEET_AFTER") | sed 's/^/      /'; fi

"$TMUX_BIN" kill-session -t "=$S"
echo "pane_close_typed_arms: $PASS passed, $FAIL failed (work dir kept: $W)"
[ "$FAIL" -eq 0 ] || exit 1
exit 0
