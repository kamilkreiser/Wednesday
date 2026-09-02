#!/bin/bash
# doctor.sh — machine preflight for the portable T9 drive (Kam, 2026-08-04:
# "what happens when I plug the portable drive into my laptop").
# Checks every machine-local dependency the project needs, maps each miss to
# its PORTABILITY.md item + one-line fix. Never prints secret VALUES — only
# presence of keys. Exit 0 = all hard requirements met (warns allowed).
#
# Usage: doctor.sh [--quiet]   (quiet: only problems + summary line)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
QUIET="${1:-}"
HARD_FAIL=0; WARNS=0

ok()   { [ "$QUIET" = "--quiet" ] || printf "  ✓ %s\n" "$1"; }
warn() { printf "  ⚠ %-38s %s\n" "$1" "${2:-}"; WARNS=$((WARNS+1)); }
fail() { printf "  ✗ %-38s %s\n" "$1" "${2:-}"; HARD_FAIL=1; }

echo "Wednesday preflight — $(hostname -s), $(date '+%Y-%m-%d %H:%M')"

# --- Hard requirements (Wednesday cannot run properly without) ---
if command -v claude >/dev/null; then
  V=$(claude --version 2>/dev/null | grep -oE '^[0-9]+\.[0-9]+\.[0-9]+' || echo "0")
  ok "claude CLI $V"
  # Feature floor: teams/agent-view era (see delegation-v2 design)
  [ "$(printf '%s\n2.1.178\n' "$V" | sort -V | head -1)" = "2.1.178" ] || warn "claude version < 2.1.178" "npm update -g or install current — Agent Teams era features missing"
else
  fail "claude CLI missing" "install Claude Code (machine-local by nature)"
fi
command -v git    >/dev/null && ok "git"    || fail "git missing" "xcode-select --install"
command -v python3 >/dev/null && ok "python3" || fail "python3 missing" "brew install python"
command -v curl   >/dev/null && ok "curl"   || fail "curl missing" "part of macOS — PATH problem?"

[ -f "$PROJECT_DIR/4_Credentials/.env" ] && ok ".env present" || fail "4_Credentials/.env missing" "restore from password manager — never in git"
# Key/credential MODES (2026-08-25, the DevMASTER relocation): Kam's unison sync engine
# runs perms=0 (SMB-safe), so a synced copy lands the deploy key as 0644 and ssh REFUSES
# it ("UNPROTECTED PRIVATE KEY FILE") — git push dies with "Permission denied (publickey)"
# on a tree that looks complete. Same family as the stripped-exec-bit check below.
if [ -f "$PROJECT_DIR/3_Access_Keys/github_deploy_rw" ]; then
  KM="$(stat -f '%Lp' "$PROJECT_DIR/3_Access_Keys/github_deploy_rw" 2>/dev/null)"
  [ "$KM" = "600" ] && ok "deploy key mode 0600" || fail "deploy key mode $KM (ssh will refuse it)" "chmod 600 3_Access_Keys/* — a drive sync reset it"
fi
EM="$(stat -f '%Lp' "$PROJECT_DIR/4_Credentials/.env" 2>/dev/null)"
case "$EM" in 600|400) ok ".env mode $EM" ;; *) warn ".env mode ${EM:-?} (world/group readable)" "chmod 600 4_Credentials/.env" ;; esac
if [ -f "$PROJECT_DIR/4_Credentials/.env" ]; then
  for key in LINEAR_API_KEY AGENTMAIL_API_KEY; do
    grep -qE "^${key}=." "$PROJECT_DIR/4_Credentials/.env" && ok "$key set" || warn "$key unset in .env" "Linear/Agent Mail features degrade"
  done
fi

# --- Voice (PORTABILITY item 2) ---
if [ -x "$PROJECT_DIR/2_Project_Files/voice/speak.sh" ]; then
  if say -v '?' 2>/dev/null | grep -q "Matilda (Premium)"; then ok "voice: Matilda (Premium)"
  elif say -v '?' 2>/dev/null | grep -qE "Matilda|Moira"; then warn "Matilda Premium not downloaded" "System Settings → Spoken Content → add Matilda Premium (fallback chain active)"
  else warn "no preferred voices" "speak.sh will use default voice"; fi
else
  fail "voice/speak.sh missing or not executable" "chmod +x 2_Project_Files/voice/speak.sh"
fi

# --- Cockpit engine (PORTABILITY items 13-14) ---
command -v tmux >/dev/null && ok "tmux $(tmux -V | awk '{print $2}')" || warn "tmux missing" "brew install tmux — fleet cockpit disabled without it (PORTABILITY 13)"
[ -d /Applications/iTerm.app ] && ok "iTerm2" || warn "iTerm2 missing" "brew install --cask iterm2 — cockpit glass (PORTABILITY 14); plain 'tmux attach' still works"
command -v brew >/dev/null && ok "homebrew" || warn "homebrew missing" "needed to install tmux/iTerm2 — https://brew.sh"

# --- Scheduler (PORTABILITY item 12, machine-local launchd) ---
if launchctl list 2>/dev/null | grep -q com.wednesday.wake; then ok "scheduler launchd jobs loaded"
else warn "scheduler jobs not loaded" "run 2_Project_Files/scheduler/install.sh on this machine (PORTABILITY 12)"; fi

# --- Optional seats / mounts ---
[ -x "$PROJECT_DIR/2_Project_Files/tools/codex-cli/node_modules/.bin/codex" ] || [ -d "$PROJECT_DIR/2_Project_Files/tools/codex-cli" ] && ok "codex CLI (drive-local)" || warn "codex CLI dir missing" "gpt seat unavailable (PORTABILITY 7-9)"
[ -d "/Volumes/DevMASTER" ] && ok "DevMASTER mounted" || warn "DevMASTER not mounted" "cross-project context read-only unavailable — fine on the laptop"

# --- Repo hooks (ledger w=3 enforcement travels per-clone) ---
[ -x "$PROJECT_DIR/.git/hooks/pre-commit" ] && ok "pre-commit artifact gate" || warn "pre-commit hook missing" "re-create per learnings/2026-08-04_gitignore-artifacts-at-creation (fresh clone?)"

# --- Calendar probe (added 2026-08-05: dashboard EventKit feed; PORTABILITY 18) ---
# On an ungranted machine the macOS calendar prompt appears HERE at launch —
# the 25s window is for clicking "Allow Full Access" (Kam's ask: surface the
# Studio re-grant at boot). perl alarm = portable timeout (macOS has no GNU timeout).
if [ -x "$PROJECT_DIR/2_Project_Files/tools/calendar_probe" ]; then
  cp_out=$(perl -e 'alarm 25; exec @ARGV' "$PROJECT_DIR/2_Project_Files/tools/calendar_probe" 2>/dev/null || echo BLOCKED)
  case "$cp_out" in
    '{"calendars"'*) ok "calendar probe (EventKit access granted)";;
    *) warn "calendar access not granted" "click Allow on the calendar prompt, or System Settings > Privacy & Security > Calendars (PORTABILITY 18)";;
  esac
else
  warn "calendar_probe missing/not executable" "swiftc 2_Project_Files/tools/calendar_probe.swift (exec bit: PORTABILITY 16)"
fi

# --- Statusline dependency (added 2026-08-05: tools/statusline.sh needs jq) ---
command -v jq >/dev/null 2>&1 && ok "jq (statusline)" || warn "jq missing" "statusline degrades to bare label — brew install jq"

# --- Machine dev toolset (added 2026-09-02, new-laptop bring-up): the workspace
# CLAUDE.md requires az/docker/node/npm; the fleet uses gh + unison (sync engine).
# Warn-level: Wednesday boots without them, the fleet/sync legs do not.
for t in node npm gh az unison docker; do
  command -v "$t" >/dev/null 2>&1 && ok "$t" || warn "$t missing" "brew install $( [ "$t" = az ] && echo azure-cli || { [ "$t" = docker ] && echo '--cask docker (then launch Docker.app once for the CLI symlink)' || echo "$t"; } )"
done

# WED-16 scheduler TCC health (added 2026-08-05; relocated same day — was
# unreachable below the exit): launchd jobs must execute from this drive.
# Exit code 126 on kickstart = TCC ungranted (PORTABILITY 15: Full Disk
# Access for /bin/bash, GUI-only, per machine).
for job in com.wednesday.shiftchange com.wednesday.wake com.wednesday.close; do
  if launchctl print "gui/$(id -u)/$job" >/dev/null 2>&1; then
    lec=$(launchctl print "gui/$(id -u)/$job" 2>/dev/null | awk '/last exit code/{print $NF}')
    case "$lec" in
      126|78:*|78) warn "scheduler $job last exit $lec" "TCC/stdio blocked (PORTABILITY 15)";;
      *) ok "scheduler $job loaded (last exit ${lec:-never})";;
    esac
  else
    warn "scheduler $job not loaded" "run scheduler/install_scheduler.command"
  fi
done

# --- Executable bits on on-drive scripts (added 2026-08-06) ---
# Drive syncs move CONTENT but not always MODES. This bit twice in one day:
# wake_watch.sh failed to arm ("Permission denied") and serve.sh could not
# restart, taking the dashboard down until it was diagnosed. Cheap to check,
# expensive to debug when a launcher silently fails instead.
NOEXEC="$(find "$SCRIPT_DIR" \( -name '*.sh' -o -name '*.command' \) ! -perm -u+x 2>/dev/null)"
if [ -n "$NOEXEC" ]; then
  warn "scripts have lost their executable bit (drive sync drops modes)" \
       "chmod +x on: $(echo "$NOEXEC" | tr '\n' ' ')"
else
  ok "all on-drive scripts are executable"
fi

# --- Fleet send queue not draining (added 2026-08-08) ---
# AgentMail enforces a daily send cap. Mail that could not go out is parked in
# fleet/state/send_queue and drained by send_queue.sh. The failure mode worth
# catching is the SILENT one: an item that sits there because nothing ever
# retried it looks exactly like an empty queue from the outside. Anything older
# than 6 hours means the trigger did not fire, or the provenance gate refused it
# and it needs a human. (learnings/2026-08-07_a-promise-is-not-a-mechanism)
QDIR="$PROJECT_DIR/2_Project_Files/fleet/state/send_queue"
if [ -d "$QDIR" ]; then
  STALE="$(find "$QDIR" -maxdepth 1 -name '*.item' -mmin +360 2>/dev/null)"
  PENDING_N="$(find "$QDIR" -maxdepth 1 -name '*.item' 2>/dev/null | wc -l | tr -d ' ')"
  if [ -n "$STALE" ]; then
    warn "fleet mail queued >6h and still unsent ($PENDING_N pending)" \
         "run 2_Project_Files/fleet/send_queue.sh drain — and read the log; a provenance REFUSAL never self-resolves"
  elif [ "$PENDING_N" -gt 0 ]; then
    ok "fleet send queue: $PENDING_N pending (recent — drain armed)"
  else
    ok "fleet send queue empty"
  fi
fi

# --- Fleet wake watcher armed (added 2026-08-09) ---
# w=4 ledger row 2026-08-09: wake_watch.sh existed, would have caught two
# unanswered agent QUESTIONs, and was NOT running — nothing armed it, nothing
# checked it was armed. A safeguard that runs beside the work needs both
# (learnings/2026-08-09_an-enforcement-you-must-arm-is-not-one). Rule: any
# live agent pane in the fleet tmux session ⇒ the watcher must be running.
TMUX_CHK="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
AGENT_PANES="$("$TMUX_CHK" list-panes -t fleet:0 -F '#{@cockpit_name}' 2>/dev/null | grep -vE '^(wednesday|fleet-monitor)$' | grep -c . || true)"
if [ "${AGENT_PANES:-0}" -gt 0 ] 2>/dev/null; then
  if pgrep -f 'wake_watch\.sh' >/dev/null 2>&1; then
    ok "wake_watch armed ($AGENT_PANES agent pane(s) live)"
  else
    fail "wake_watch NOT running — $AGENT_PANES agent pane(s) live unwatched" \
         "arm: fleet/cockpit/wake_watch.sh '<latest-inbound-mail-ts>' as a background task"
  fi
else
  ok "no agent panes live — wake_watch not required"
fi

# --- Boot digest current (WED-139, 2026-09-02): the seat boots on a digest GENERATED
# from the lesson files. The launcher regenerates it in-path; this is the backstop —
# a digest older than any lesson file, or missing a headline/rule line, means a seat
# would boot on stale rules. --check exits 1 on either.
BD="$PROJECT_DIR/2_Project_Files/tools/boot_digest.py"
if [ -f "$BD" ]; then
  BD_OUT="$(python3 "$BD" --check 2>&1)"; BD_RC=$?
  if [ "$BD_RC" -eq 0 ]; then
    ok "boot digest current ($(printf '%s' "$BD_OUT" | tail -1 | sed 's/^check: //'))"
  else
    warn "boot digest STALE or incomplete" "regenerate: python3 2_Project_Files/tools/boot_digest.py — $(printf '%s' "$BD_OUT" | head -1)"
  fi
else
  warn "boot_digest.py missing" "the seat will read every lesson file (34% boot) — restore 2_Project_Files/tools/boot_digest.py"
fi

# --- Dead-coordinator rotation (2026-09-02): the 06:39 seat hit the hard context
# limit at 09:49 and sat unreachable for six hours while the watcher tapped it 94
# times. The fix has three parts and each must be present or the others are decor:
# the watcher leg that sees "Context limit reached", the runner case that respawns
# instead of tapping, and the respawn script itself.
RT="$PROJECT_DIR/2_Project_Files/fleet/cockpit/wednesday_rotate.sh"
if [ -x "$RT" ] \
   && grep -q "Context limit reached" "$PROJECT_DIR/2_Project_Files/fleet/cockpit/wake_watch.sh" \
   && grep -q 'wednesday_rotate.sh --dead' "$PROJECT_DIR/2_Project_Files/fleet/cockpit/arm_wake_watch.sh" \
   && grep -q 'ROTATE NOW' "$PROJECT_DIR/2_Project_Files/fleet/cockpit/wake_watch.sh"; then
  ok "dead-coordinator rotation wired (watcher leg + runner case + wednesday_rotate.sh)"
else
  fail "dead-coordinator rotation NOT wired" "a seat at its context limit would sit dead until a human notices (2026-09-02); check wake_watch.sh / arm_wake_watch.sh / wednesday_rotate.sh"
fi

# --- Fleet model pins (Kam ruling 2026-08-12: all projects Opus 5; only Wednesday
# stays on Fable 5 while the usage limit is tight). Launchers pin --model on the
# exec line, which OVERRIDES the global default — a stale fable pin silently
# reverts a project at its next launch. Wednesday never edits other projects'
# launchers (hard rule 1): a warning here routes the fix to that project's own
# agent or to Kam. Read-only check; remove when Kam lifts the ruling.
LCONF="$PROJECT_DIR/2_Project_Files/fleet/cockpit/launchers.conf"
if [ -f "$LCONF" ]; then
  STALE_PINS=""
  while IFS='|' read -r LNAME LPATH; do
    case "$LNAME" in \#*|"") continue ;; esac
    [ -f "$LPATH" ] || continue
    # Comments excluded: Secuura's launcher keeps "Was `--model claude-fable-5`"
    # as a history note, which made this check warn on an already-fixed pin
    # (false alarm, 2026-08-13). Only a live (non-#) line counts.
    if grep -vE '^\s*#' "$LPATH" 2>/dev/null | grep -qE -- '--model claude-fable-5'; then
      STALE_PINS="$STALE_PINS $LNAME"
    fi
  done < "$LCONF"
  if [ -n "$STALE_PINS" ]; then
    warn "fable-5 pin still in launcher(s):$STALE_PINS" "next launch reverts to Fable — route the pin edit to that project's agent (or Kam)"
  else
    ok "fleet launchers carry no fable-5 pins"
  fi
fi

# --- Wednesday's OWN model pin must be the `fable` ALIAS, never a dated ID (Kam,
# 2026-09-02: "always choose the latest fable model"). A dated pin went stale the day
# Fable 5.1 shipped and nothing noticed until Kam did — this check is the mechanism.
WLAUNCH="$PROJECT_DIR/Launch_Wednesday.command"
if [ -f "$WLAUNCH" ]; then
  if grep -vE '^\s*#' "$WLAUNCH" | grep -qE -- '--model claude-fable-[0-9]'; then
    warn "Launch_Wednesday.command pins a DATED Fable ID" "use '--model fable' (alias = latest Fable) — Kam's 2026-09-02 ruling"
  elif grep -vE '^\s*#' "$WLAUNCH" | grep -qE -- '--model fable(\[1m\])?( |$)'; then
    ok "Wednesday launcher uses the 'fable' alias (latest Fable at every launch)"
  else
    warn "Launch_Wednesday.command has no recognisable --model fable line" "read the exec line — the alias rule may have been edited away"
  fi
fi

# ── Tailscale remote-access leg (added 2026-08-20; DORMANT-BY-DEFAULT per Kam
# 2026-08-20 ruling 17: "case by case. I will ask or turn it on when I need.
# Keep it dormant in the meantime."). Down is the EXPECTED state — report it
# as ok/informational, never as a warning. Warn only on the half-states
# (up without serve, or serve without 47787) which mean an activation was
# started and not finished. To activate on Kam's ask:
#   $TS_BIN up && $TS_BIN serve --bg --http=80 --set-path=/ http://127.0.0.1:47787
TS_BIN="/Applications/Tailscale.app/Contents/MacOS/Tailscale"
if [ -x "$TS_BIN" ]; then
  # Bounded call (2026-09-02, new laptop): before the user approves the VPN
  # configuration the CLI BLOCKS forever waiting for the backend, and doctor
  # hung with it. macOS has no `timeout`; background + kill after 4 s.
  TS_TMP=$(mktemp); ( "$TS_BIN" status --json > "$TS_TMP" 2>/dev/null & TS_PID=$!; sleep 4; kill "$TS_PID" 2>/dev/null; wait "$TS_PID" 2>/dev/null )
  TS_STATE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("BackendState",""))' "$TS_TMP" 2>/dev/null); rm -f "$TS_TMP"
  [ -z "$TS_STATE" ] && warn "tailscale backend not answering" "first run: approve the VPN configuration + log in via the menu-bar icon (PORTABILITY Tailscale section)"
  if [ "$TS_STATE" = "Running" ]; then
    if "$TS_BIN" serve status 2>/dev/null | grep -q "proxy http://127.0.0.1:47787"; then
      ok "tailscale ACTIVE + dashboard served (Kam asked for it — make dormant again when he is done)"
    else
      warn "tailscale up but NO serve config for 47787 — half-activated" "finish: $TS_BIN serve --bg --http=80 --set-path=/ http://127.0.0.1:47787   (or make dormant: $TS_BIN down)"
    fi
  else
    ok "tailscale dormant (expected state per Kam 2026-08-20; activate on his ask only)"
  fi
else
  warn "Tailscale.app missing" "remote access unavailable on this machine — see PORTABILITY.md"
fi

# --- Travel pointers (PORTABILITY 18, 2026-08-25): a drive sync copies files but
# freezes stored ABSOLUTE PATHS. Sweep every project repo's core.sshCommand and warn
# on pointers to paths that do not exist on THIS machine. Read-only: warnings are
# routed to the projects' own launchers/agents — Wednesday never edits their repos.
DRIVE_ROOT="${PROJECT_DIR%/WEDNESDAY}"
STALE_PTRS=0
for cfg in "$DRIVE_ROOT"/!CODING/*/*/2_Project_Files/.git/config; do
  [ -f "$cfg" ] || continue
  SSHCMD=$(git config -f "$cfg" core.sshCommand 2>/dev/null) || continue
  [ -n "$SSHCMD" ] || continue
  KEYPATH=$(printf '%s' "$SSHCMD" | sed -n 's/.*-i "\{0,1\}\([^" ]*\)"\{0,1\}.*/\1/p')
  if [ -n "$KEYPATH" ] && [ ! -f "$KEYPATH" ]; then
    PROJ=$(printf '%s' "$cfg" | sed "s|$DRIVE_ROOT/!CODING/||; s|/2_Project_Files/.git/config||")
    warn "stale ssh pointer: $PROJ" "core.sshCommand -> $KEYPATH (missing here) — heals at that project's next launch, or its agent repoints"
    STALE_PTRS=$((STALE_PTRS+1))
  fi
done
[ "$STALE_PTRS" = "0" ] && ok "travel pointers: no project repo points at a missing key path"

# md2pdf house-style renderer deps (Kam 2026-08-28: "keep this style going forward"; PORTABILITY 21)
if command -v pandoc >/dev/null && [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] && command -v pdftoppm >/dev/null; then
  ok "md2pdf deps (pandoc + Google Chrome + pdftoppm)"
else
  warn "md2pdf deps missing" "pandoc/Google Chrome/pdftoppm — report PDFs will not render (brew install pandoc poppler; Chrome from google.com/chrome)"
fi

echo
if [ "$HARD_FAIL" = "1" ]; then

  echo "PREFLIGHT: HARD FAILURES above — fix before relying on this machine."
  exit 1
elif [ "$WARNS" -gt 0 ]; then
  echo "PREFLIGHT: OK with $WARNS warning(s) — degraded features listed above."
else
  echo "PREFLIGHT: all clear."
fi
exit 0
