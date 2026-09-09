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
# AGENT-AWARE 2026-09-09 (Kam ruled `parameterise` 08:21): this grepped a hardcoded
# com.wednesday.wake, so on Tuesday's machine it reported "not loaded" for a job that
# SHOULD NOT exist there, and would have reported "loaded" for one that must not.
_DOC_AGENT="${WED_AGENT:-wednesday}"
# INSTRUMENT CHANGED 2026-09-09, and the reason is measured rather than assumed. This check
# used `launchctl list | grep -q <label>`. On 2026-09-09 that pipeline returned FALSE inside
# doctor while `launchctl print gui/$(id -u)/<label>` — the call the per-job sweep below uses,
# forty lines further down, in the SAME RUN — returned true for all four jobs. Two checks in
# one run disagreed about the same fact. The same `list|grep` line run standalone matched, so
# the fault is contextual and not worth more of anyone's evening: the fix is to stop using the
# instrument that disagrees with its neighbour and use the one that is already proven here.
# (Rule: when two instruments disagree, re-measure and keep the one whose answer is checkable —
# never the one whose answer creates work you were expecting to do.)
if launchctl print "gui/$(id -u)/com.${_DOC_AGENT}.wake" >/dev/null 2>&1; then ok "scheduler launchd jobs loaded (agent: $_DOC_AGENT)"
else warn "scheduler jobs not loaded (agent: $_DOC_AGENT)" "run 2_Project_Files/scheduler/install_scheduler.command on this machine (PORTABILITY 12)"; fi

# --- Optional seats / mounts ---
[ -x "$PROJECT_DIR/2_Project_Files/tools/codex-cli/node_modules/.bin/codex" ] || [ -d "$PROJECT_DIR/2_Project_Files/tools/codex-cli" ] && ok "codex CLI (drive-local)" || warn "codex CLI dir missing" "gpt seat unavailable (PORTABILITY 7-9)"
[ -d "/Volumes/DevMASTER" ] && ok "DevMASTER mounted" || warn "DevMASTER not mounted" "cross-project context read-only unavailable — fine on the laptop"

# --- Repo hooks (ledger w=3 enforcement travels per-clone) ---
# A TRACKED master copy now lives beside the other hooks, so a stranded seat installs it
# with one command instead of reconstructing it from a 2026-08-04 commit message. The
# check also compares the two: an installed hook that has DRIFTED from the master is worse
# than a missing one, because it looks armed. Proof the gap is real — the clone made on
# 2026-09-08 had no hook at all, and its whole job is refusing the conflict markers that
# reached origin twice that same morning.
PCM="$PROJECT_DIR/2_Project_Files/fleet/hooks/pre-commit"
PCI="$PROJECT_DIR/.git/hooks/pre-commit"
if [ ! -x "$PCI" ]; then
  if [ -f "$PCM" ]; then
    warn "pre-commit hook NOT installed" "one command: cp 2_Project_Files/fleet/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit"
  else
    fail "pre-commit hook missing AND no tracked master" "the artifact/marker gate is gone entirely — restore 2_Project_Files/fleet/hooks/pre-commit"
  fi
elif [ -f "$PCM" ] && ! diff -q "$PCM" "$PCI" >/dev/null 2>&1; then
  warn "pre-commit hook has DRIFTED from the tracked master" "diff 2_Project_Files/fleet/hooks/pre-commit .git/hooks/pre-commit — an armed-looking hook may not be"
else
  ok "pre-commit artifact + marker gate" "installed and matching the tracked master"
fi

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
# DOCKER CHECK CORRECTED 2026-09-09: `command -v docker` was reporting "docker missing"
# on a machine where Docker Desktop was installed, RUNNING and serving (daemon 29.7.2,
# socket at ~/.docker/run/docker.sock). Docker Desktop no longer creates the
# /usr/local/bin symlink unless the optional admin prompt is accepted, and its CLI lives
# inside the app bundle — which is on PATH only for LOGIN shells (~/.zprofile). doctor runs
# in a non-login shell, so it measured PATH and called it Docker. Ask the thing itself.
DOCKER_BUNDLED="/Applications/Docker.app/Contents/Resources/bin/docker"
for t in node npm gh az unison docker; do
  if [ "$t" = docker ]; then
    DBIN="$(command -v docker 2>/dev/null || { [ -x "$DOCKER_BUNDLED" ] && echo "$DOCKER_BUNDLED"; })"
    if [ -n "$DBIN" ]; then
      if "$DBIN" info --format '{{.ServerVersion}}' >/dev/null 2>&1; then ok "docker ($("$DBIN" --version 2>/dev/null | awk '{print $3}' | tr -d ,), daemon up)"
      else warn "docker CLI present, daemon not responding" "open -a Docker and accept its prompts"; fi
      [ -x /usr/local/bin/docker ] || ok "docker CLI is bundle-only (no /usr/local/bin symlink) — ~/.zprofile puts it on PATH for login shells"
    else warn "docker missing" "brew install --cask docker (then launch Docker.app once)"; fi
    continue
  fi
  command -v "$t" >/dev/null 2>&1 && ok "$t" || warn "$t missing" "brew install $( [ "$t" = az ] && echo azure-cli || echo "$t" )"
done

# WED-16 scheduler TCC health (added 2026-08-05; relocated same day — was
# unreachable below the exit): launchd jobs must execute from this drive.
# Exit code 126 on kickstart = TCC ungranted (PORTABILITY 15: Full Disk
# Access for /bin/bash, GUI-only, per machine).
# 2026-09-08 (s152): this check said "must execute from this drive" and never
# checked it. All three jobs had failed EVERY fire since 2026-09-07 with exit
# 127 — the plists were generated on 2026-09-02 hardcoding /Volumes/KK_DEV_Local
# and the drive is now mounted elsewhere — and this loop printed a green tick for
# each, because 127 fell through to the catch-all. Loaded is not runnable: the
# plist's script path is now READ and stat'd, and 127 is named rather than
# decorated. install_scheduler.command self-locates, so re-running it from the
# current drive is the whole fix.
# The nightly NAS sync (Kam 2026-09-08 14:57) joins the sweep. The LABEL carries the
# agent — com.wednesday.nassync on this seat, com.tuesday.nassync on hers — so the two
# machines cannot collide, and so this check follows whichever seat is booting.
# AGENT-AWARE 2026-09-09: all four labels now follow the booting seat, not just nassync.
for job in "com.${_DOC_AGENT}.shiftchange" "com.${_DOC_AGENT}.wake" "com.${_DOC_AGENT}.close" "com.${_DOC_AGENT}.nassync"; do
  if launchctl print "gui/$(id -u)/$job" >/dev/null 2>&1; then
    lec=$(launchctl print "gui/$(id -u)/$job" 2>/dev/null | awk '/last exit code/{print $NF}')
    prog=$(launchctl list "$job" 2>/dev/null | awk -F'"' '/scheduler\/.*\.sh/{print $2; exit}')
    if [ -n "$prog" ] && [ ! -f "$prog" ]; then
      warn "scheduler $job points off-drive" "$prog missing — re-run scheduler/install_scheduler.command from this drive"
    else
      case "$lec" in
        126|78:*|78) warn "scheduler $job last exit $lec" "TCC/stdio blocked (PORTABILITY 15)";;
        127) warn "scheduler $job last exit 127" "its script was not found at fire time — re-run scheduler/install_scheduler.command";;
        *) ok "scheduler $job loaded (last exit ${lec:-never})";;
      esac
    fi
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
    warn "boot digest STALE or incomplete" "regenerate BOTH: python3 2_Project_Files/tools/boot_digest.py --by-tier && python3 2_Project_Files/tools/boot_digest.py — $(printf '%s' "$BD_OUT" | head -1)"
  fi
else
  warn "boot_digest.py missing" "the seat will read every lesson file (34% boot) — restore 2_Project_Files/tools/boot_digest.py"
fi

# --- Two-agent path guard armed (Phase 2, Kam 2026-09-08: "a strong gate between
# agents acting between the two"). A guard that can go MISSING is not a guard — the
# file could be lost to a bad merge, a clone, or a tidy-up, and nothing else would say
# so. This does not just check the file exists: it FIRES it on a known-bad command and
# on a known-good one, so a pathguard that is present but inert fails the check too
# (a-check-that-cannot-fail, 2026-08-07). Both probes are strings here, never run.
PG="$PROJECT_DIR/2_Project_Files/fleet/hooks/pathguard.py"
if [ -f "$PG" ]; then
  PG_BAD="$(printf 'cp a /Volumes/DevMASTER/TUESDAY/b' | HOOK_OWN_ROOT="$PROJECT_DIR" python3 "$PG" 2>/dev/null)"
  PG_GOOD="$(printf 'cp a %s/b' "$PROJECT_DIR" | HOOK_OWN_ROOT="$PROJECT_DIR" python3 "$PG" 2>/dev/null)"
  if [ -n "$PG_BAD" ] && [ -z "$PG_GOOD" ]; then
    ok "two-agent path guard armed" "refuses the sister tree, passes its own"
  elif [ -z "$PG_BAD" ]; then
    fail "path guard is INERT" "it did not refuse a write to the other agent's tree — the gate is decoration"
  else
    fail "path guard refuses its OWN tree" "it would block every write this seat makes — check HOOK_OWN_ROOT resolution"
  fi
else
  fail "pathguard.py missing" "the file-write half of the two-agent gate is gone; only git verbs are guarded"
fi

# --- Chat streams (Phase 0, Kam's 2026-09-08 11:50 two-agent commission) ---------
# chat_log.json is DERIVED from chat_legacy.json + one stream per writer, and it is
# gitignored: a generated file that two seats both regenerate is what corrupted Kam's
# reading surface three times on 2026-09-08. So a fresh clone HAS NO chat_log.json
# until something builds it, and every reader of it — kam_rulings_today.sh,
# wake_watch.sh, attention/ingest.py, generate.py — would report an empty day.
# This does not warn about staleness, it REBUILDS: the file is derived, so the fix
# and the check are the same command, and a boot is exactly when it must be right.
CS="$PROJECT_DIR/2_Project_Files/tools/chat_streams.py"
if [ -f "$CS" ]; then
  # --harvest, not a bare run: a writer that bypassed the streams (an old server
  # still up across a cutover — measured 2026-09-08) leaves an entry only the
  # derived file holds, and a bare rebuild DELETES it. --harvest routes it back by
  # its own fields and still fails (rc 4) on anything it cannot attribute.
  if CS_OUT="$(python3 "$CS" --harvest 2>&1)"; then
    ok "chat streams merged" "$(printf '%s' "$CS_OUT" | tail -1 | sed 's/^chat_streams: //')"
  else
    fail "chat_log.json NOT rebuilt from the streams" "$(printf '%s' "$CS_OUT" | head -2 | tr '\n' ' ')"
  fi
else
  fail "chat_streams.py missing" "chat_log.json is derived and gitignored — without this tool Kam's panel is empty on a fresh clone"
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
    if grep -vE '^\s*#' "$LPATH" 2>/dev/null | grep -qE -- '--model (claude-)?fable'; then
      STALE_PINS="$STALE_PINS $LNAME"
    fi
  done < "$LCONF"
  # Wednesday's OWN launcher is not in launchers.conf, so it was never in this
  # check's corpus — an alias pin (`--model fable`) sat there unseen until Kam's
  # Fable credits ran out on 2026-09-03 and he had to switch the model by hand.
  # A check whose corpus excludes the checker's own file is a check that cannot
  # see (ledger, a-check-that-cannot-fail family).
  # AMENDED 2026-09-05 (Kam: "latest fable … unless credits are out, in which case
  # latest opus"): Wednesday's launcher now pins `--model fable --fallback-model
  # opus`. The hazard this check guards is "credits out → seat cannot start"; the
  # fallback flag is the remedy, so a fable pin WITH the fallback is the wanted
  # state and only a fable pin WITHOUT it warns. (A dated `claude-fable-N` pin
  # still warns — the alias is what tracks the newest Fable.)
  WEXEC=$(grep -vE '^\s*#' "$PROJECT_DIR/Launch_Wednesday.command" 2>/dev/null | grep -E -- '--model (claude-)?fable' || true)
  if [ -n "$WEXEC" ]; then
    if printf '%s\n' "$WEXEC" | grep -qE -- '--model claude-fable'; then
      STALE_PINS="$STALE_PINS WEDNESDAY(own:dated-pin)"
    elif ! printf '%s\n' "$WEXEC" | grep -qE -- '--fallback-model'; then
      STALE_PINS="$STALE_PINS WEDNESDAY(own:fable-without-fallback)"
    fi
  fi
  if [ -n "$STALE_PINS" ]; then
    warn "fable-5 pin still in launcher(s):$STALE_PINS" "next launch reverts to Fable — route the pin edit to that project's agent (or Kam)"
  else
    ok "fleet launchers carry no fable-5 pins"
  fi
fi

# --- Wednesday's OWN model pin (Kam, 2026-09-05 13:1x, verbatim: "you should load in
# latest fable model (now 5.1) unless credits are out in which case you should load
# in latest opus model"). The wanted exec line is `--model fable --fallback-model
# opus`: the `fable` ALIAS tracks the newest Fable (a dated pin went stale the day
# 5.1 shipped, 2026-09-02), and `--fallback-model opus` is the CLI's own leg for an
# unavailable primary — exercised 2026-09-05 with a bogus primary (FALLBACK-OK).
# History this supersedes: 09-02 fable alias → 09-03/09-04 hand-pin `opus` when the
# Fable credits ran out (a pin that silently kept every later seat on Opus after the
# credits came back — the 09-05 13:09 seat booted on Opus with Fable reachable).
# Honest limit, also written in the launcher: whether a CREDIT exhaustion trips the
# fallback leg is unverified — it cannot be exercised without spending the credits.
WLAUNCH="$PROJECT_DIR/Launch_Wednesday.command"
if [ -f "$WLAUNCH" ]; then
  WEXECLINE=$(grep -vE '^\s*#' "$WLAUNCH" | grep -E -- '^exec claude|--model ' | tail -1)
  if printf '%s\n' "$WEXECLINE" | grep -qE -- '--model (claude-fable-[0-9]|claude-opus-[0-9])'; then
    warn "Launch_Wednesday.command pins a DATED model ID" "use the aliases: '--model fable --fallback-model opus' (Kam 2026-09-05)"
  elif printf '%s\n' "$WEXECLINE" | grep -qE -- '--model fable(\[1m\])? ' && printf '%s\n' "$WEXECLINE" | grep -qE -- '--fallback-model opus'; then
    ok "Wednesday launcher: fable alias with opus fallback (Kam 2026-09-05)"
  elif printf '%s\n' "$WEXECLINE" | grep -qE -- '--model fable'; then
    warn "Launch_Wednesday.command pins Fable with NO fallback" "credits out = the seat cannot start; add '--fallback-model opus' (Kam 2026-09-05)"
  elif printf '%s\n' "$WEXECLINE" | grep -qE -- '--model opus'; then
    # WEEK-SCOPED OVERRIDE (Kam, 2026-09-06 20:2x, verbatim: "please change your boot
    # script for the rest of the week to boot in opus 5 rather than fable. we are
    # burning through credits a little too quickly"). An opus-only pin is the WANTED
    # state until the week is out; after that it is the 09-04 hazard again (a hand-pin
    # that silently outlived its reason), so this leg EXPIRES itself rather than
    # relying on anyone remembering. Kam's word moves the date; the revert is the
    # commented fable line in Launch_Wednesday.command.
    WED_OPUS_UNTIL="2026-09-13"
    if [ "$(date +%Y-%m-%d)" \> "$WED_OPUS_UNTIL" ]; then
      warn "Launch_Wednesday.command still pins opus ONLY after $WED_OPUS_UNTIL" "Kam's 2026-09-06 override was for one week — restore the commented '--model fable --fallback-model opus' line or ask him to extend it"
    else
      ok "Wednesday launcher: opus pin, Kam's week-scoped credit override (expires after $WED_OPUS_UNTIL)"
    fi
  else
    warn "Launch_Wednesday.command has no recognisable --model line" "read the exec line — the alias rule may have been edited away"
  fi
fi

# ── WEEK-SCOPED AUTONOMY GRANTS — they expire themselves (added 2026-09-07) ──────
# Kam gave TWO week-scoped grants on 2026-09-07, in his own words, hours apart:
#   09:40  "you can give the go ahead to merge as it becomes relevant so that I'm not
#           slowing things down"                                    -> MERGE authority
#   11:09  "Go ahead with the deploy, and you've got permission to deploy for the rest
#           of the week."                                           -> DEPLOY authority
#   12:07  "Lift the production ban. This week we are allowed to make production
#           changes, but flag these when relevant or when making changes."
#                                                              -> PRODUCTION changes
# The third is the largest boundary he has moved (never-touch-prod is a hard rule with
# its own skill). SCOPE CONFIRMED BY KAM 12:10:40 — "Only secure" = SECUURA ONLY.
# Datasec production is NOT covered and the laptop seat has no such grant. A credential live systems authenticate with is a
# ROTATION and still comes to him; external comms are untouched.
# Both are read as THROUGH SUNDAY 2026-09-13, stated to him as a reading he can move.
# WHY THIS IS A CHECK AND NOT A NOTE (2026-09-06_a-scoped-override-carries-its-own-expiry):
# a scoped instruction applied without an expiry becomes a standing one the moment the
# seat that heard it rotates — and this pair grants MERGE and DEPLOY, which is exactly
# the category where a silently-permanent grant is worst. After the date the honest
# state is the v1.3 standing grant, which already covers merges and dev/staging/demo
# deploys; what lapses is the extra latitude, not the baseline. Kam's word moves it.
WED_WEEK_GRANTS_UNTIL="2026-09-13"
if [ "$(date +%Y-%m-%d)" \> "$WED_WEEK_GRANTS_UNTIL" ]; then
  warn "Kam's week-scoped MERGE + DEPLOY + PRODUCTION grants lapsed after $WED_WEEK_GRANTS_UNTIL" "2026-09-07 09:40, 11:09 and 12:07 were 'for the rest of the week' — fall back to protocol v1.3 scope, or ask him to extend. Do not carry the extra latitude forward silently."
else
  ok "Kam's week-scoped merge + deploy + PRODUCTION grants (2026-09-07) live until $WED_WEEK_GRANTS_UNTIL (production: SECUURA ONLY, confirmed by Kam 12:10)"
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
# 2026-09-07: the sweep used to cover ONLY !CODING project repos. The SHARED VAULT was
# never swept — and it is the one repo EVERY agent on the drive pushes to at wrap, so a
# stale pointer there fails every project at once rather than one. Found when the NexusAI
# agent hit exactly that mid-wrap on the T9 (its pointer still named /Volumes/DevMASTER)
# and had to diagnose it itself. Wednesday's own repo is swept for the same reason.
# Read-only either way: warnings are ROUTED, never worked around — Wednesday does not
# edit another project's .git (hard rule 1).
for cfg in "$DRIVE_ROOT"/!CODING/*/*/2_Project_Files/.git/config \
           "$DRIVE_ROOT"/Notes\ \(MASTER\)/.git/config \
           "$PROJECT_DIR"/.git/config; do
  [ -f "$cfg" ] || continue
  SSHCMD=$(git config -f "$cfg" core.sshCommand 2>/dev/null) || continue
  [ -n "$SSHCMD" ] || continue
  # Extract the -i argument. QUOTED FORM FIRST: a key path may contain spaces (the vault's
  # does — ".../Setup and System/keys/..."), and the unquoted character class below stops
  # at the first space, which would truncate the path and warn on a healthy repo. Latent
  # until a spaced path entered the sweep; adding the vault is what makes it reachable.
  KEYPATH=$(printf '%s' "$SSHCMD" | sed -n 's/.*-i "\([^"]*\)".*/\1/p')
  [ -n "$KEYPATH" ] || KEYPATH=$(printf '%s' "$SSHCMD" | sed -n 's/.*-i \([^ ]*\).*/\1/p')
  if [ -n "$KEYPATH" ] && [ ! -f "$KEYPATH" ]; then
    case "$cfg" in
      "$PROJECT_DIR"/.git/config)          PROJ="WEDNESDAY (this repo)" ;;
      "$DRIVE_ROOT"/Notes\ \(MASTER\)/*)   PROJ="Notes (MASTER) — THE SHARED VAULT: every agent's wrap pushes here" ;;
      *) PROJ=$(printf '%s' "$cfg" | sed "s|$DRIVE_ROOT/!CODING/||; s|/2_Project_Files/.git/config||") ;;
    esac
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

# --- Root-folder hygiene (Kam 2026-09-05 08:1x: "the images in the root folder do
# not belong there … create a rule"). The project root holds the rules file, the
# portability checklist and the launchers — nothing else. Screenshots go to
# 0_Brain/reference/<date>_<topic>/, session artefacts to 5_Project_History/,
# scratch to the session scratchpad. A backup of a root script may sit beside it
# (the cockpit precedent: cockpit.sh.pre-0902-*). Anything else is a filing miss.
ROOT_STRAYS=""
for f in "$PROJECT_DIR"/* "$PROJECT_DIR"/.[!.]*; do
  [ -f "$f" ] || continue
  b=$(basename "$f")
  case "$b" in
    CLAUDE.md|PORTABILITY.md|.gitignore|.DS_Store|Launch_*.command|Launch_*.command.pre-*|Launch_*.command.bak*) ;;
    *) ROOT_STRAYS="$ROOT_STRAYS $b" ;;
  esac
done
if [ -z "$ROOT_STRAYS" ]; then
  ok "root folder: only rules, portability and launchers"
else
  warn "root folder holds stray file(s):$ROOT_STRAYS" "file them (screenshots -> 0_Brain/reference/<date>_<topic>/; artefacts -> 5_Project_History/) — never delete"
fi

# --- Ledger archive has a TRIGGER (Kam ruling 2026-09-08 07:07, card
# `wed-ledger-archive-has-no-trigger` => `trigger`: "Add the doctor.sh trigger,
# leave your cadence alone"). CLAUDE.md rule 3c says move `_ledger.md` rows older
# than ~3 days into `_ledger_archive.md`. It was written as a SESSION-END step —
# and a seat that ROTATES never runs the session-end ritual, so with 3-5 rotations
# a day it fired approximately never. Measured 2026-09-08: `_ledger.md` had reached
# 398,606 B / 206 rows, LARGER than the boot digest beside it, while rule 3c was
# perfectly correct and simply unexecuted. His cadence is untouched; this only
# makes it fire.
# The sibling per-seat ledgers are covered too: they grow by the same mechanism and
# leaving a known sibling out is the frame error this project keeps catching.
LEDGER_CUTOFF=$(date -v-3d +%Y-%m-%d 2>/dev/null || date -d '3 days ago' +%Y-%m-%d 2>/dev/null)
LEDGER_STALE=""
if [ -n "$LEDGER_CUTOFF" ]; then
  for LF in "$PROJECT_DIR"/0_Brain/learnings/_ledger.md \
            "$PROJECT_DIR"/0_Brain/learnings/_ledger_laptop_datasec.md; do
    [ -f "$LF" ] || continue
    # Row dates are the first cell of a table row: `| YYYY-MM-DD | ...`
    OLD=$(grep -oE '^\| 2[0-9]{3}-[0-9]{2}-[0-9]{2} \|' "$LF" 2>/dev/null \
          | tr -d '| ' | awk -v c="$LEDGER_CUTOFF" '$0 < c' | wc -l | tr -d ' ')
    if [ "${OLD:-0}" -gt 0 ]; then
      SZ=$(( $(wc -c < "$LF" | tr -d ' ') / 1024 ))
      LEDGER_STALE="$LEDGER_STALE $(basename "$LF"):${OLD}rows/${SZ}KB"
    fi
  done
fi
if [ -z "$LEDGER_CUTOFF" ]; then
  warn "ledger archive: could not compute a 3-day cutoff" "neither \`date -v-3d\` nor \`date -d\` worked — rule 3c is UNCHECKED on this machine, not satisfied"
elif [ -z "$LEDGER_STALE" ]; then
  ok "ledger archive: no rows older than $LEDGER_CUTOFF"
else
  warn "ledger rows past rule 3c's cadence:$LEDGER_STALE" "move them to _ledger_archive.md VERBATIM, newest-first, and ASSERT CONSERVATION (rows before == rows after). Never edit, never delete — 3c is a move."
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
