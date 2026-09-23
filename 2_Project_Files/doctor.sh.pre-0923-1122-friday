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

# --- chat_sync: Kam's ONE page, kept current on BOTH machines (Kam, 2026-09-09 17:53/17:54) ---
# Before this job, Tuesday's replies reached his page only when a Wednesday seat happened to
# pull — a person standing in for a mechanism. Agent-derived label so a seat can never run the
# other seat's job from the wrong tree. `launchctl print` deliberately, NOT `list | grep`:
# the grep form gives a false negative here (2026-09-09, and the comment above says why).
if launchctl print "gui/$(id -u)/com.${_DOC_AGENT}.chatsync" >/dev/null 2>&1; then
  # LOADED IS NOT RUNNING, and a fresh log is NOT proof either: a seat running the script by
  # hand keeps the log fresh while launchd fails every cycle. That exact check passed while the
  # job was dead with EX_CONFIG on 2026-09-09. Key on launchd's OWN exit code, which nothing a
  # seat does by hand can move.
  _cs_rc=$(launchctl print "gui/$(id -u)/com.${_DOC_AGENT}.chatsync" 2>/dev/null | awk -F'= ' '/last exit code/{print $2}')
  case "${_cs_rc:-unknown}" in
    0|"(never exited)") ok "chat_sync loaded, last launchd exit clean (agent: $_DOC_AGENT)" ;;
    # 126 and 78 are DIFFERENT failures with DIFFERENT fixes (Tuesday, 2026-09-16 STATUS,
    # disagreement 4: this line used to print the 78 hint for a 126). 126 = the script could not
    # be executed — on these Macs that is TCC: /bin/bash lacks Full Disk Access, so launchd gets
    # EPERM on a file that runs fine from Terminal. 78 = EX_CONFIG — launchd refused the plist
    # before running a line, usually an out/err path it cannot open.
    126) warn "chat_sync loaded but launchd's last exit was: 126 (not permitted)" "TCC: /bin/bash needs Full Disk Access on THIS machine — Kam's hands, System Settings → Privacy & Security → Full Disk Access → add /bin/bash (PORTABILITY 15). Kam's page will not show the other agent until then." ;;
    78)  warn "chat_sync loaded but launchd's last exit was: 78 (EX_CONFIG)" "the plist points its out/err somewhere launchd cannot open (/Volumes, or a home that does not exist) — they must live in ~/Library/Logs (PORTABILITY 22). Kam's page will not show the other agent." ;;
    *) warn "chat_sync loaded but launchd's last exit was: ${_cs_rc}" "read ~/Library/Logs/${_DOC_AGENT}_chatsync.err for the cause (126 = TCC/Full Disk Access, 78 = plist out/err path, 127 = script not found). Kam's page will not show the other agent." ;;
  esac
else
  warn "chat_sync not loaded (agent: $_DOC_AGENT)" "launchctl load ~/Library/LaunchAgents/com.${_DOC_AGENT}.chatsync.plist (PORTABILITY 22) — without it Kam's page will not show the other agent"
fi

# --- Optional seats / mounts ---
[ -x "$PROJECT_DIR/2_Project_Files/tools/codex-cli/node_modules/.bin/codex" ] || [ -d "$PROJECT_DIR/2_Project_Files/tools/codex-cli" ] && ok "codex CLI (drive-local)" || warn "codex CLI dir missing" "gpt seat unavailable (PORTABILITY 7-9)"
[ -d "/Volumes/DevMASTER" ] && ok "DevMASTER mounted" || warn "DevMASTER not mounted" "cross-project context read-only unavailable — fine on the laptop"

# --- Local model harness (Kam, panel 2026-09-14 11:26: "download and implement
# Qwen 3 30b ... use it within the workflow"). Machine-local (Homebrew ollama)
# + weights on the drive (PORTABILITY item added same day). Warn-level only —
# the fleet runs fine without the local model, this just says the seat is dark.
LM_MODELS_DIR="$PROJECT_DIR/2_Project_Files/local-model/models"
LM_MODEL_TAG="qwen3/30b-a3b"
LM_MANIFEST="$LM_MODELS_DIR/manifests/registry.ollama.ai/library/$LM_MODEL_TAG"
# PARKED 2026-09-14 14:2x — Kam, panel 14:25: "Please remove Quen from the system as we won't use
# it going forward." The model was removed (ollama rm), the server stopped; the harness + checkers
# stay for a future trial. This check is a one-line INFO, never a warning, until Kam un-parks it.
if [ "${LM_UNPARK:-0}" != "1" ]; then
  ok "local-model: PARKED 2026-09-14 (Kam) — model removed, server stopped; harness kept (LM_UNPARK=1 re-enables this check)"
elif ! command -v ollama >/dev/null 2>&1; then
  warn "ollama not on PATH" "brew install ollama — local-model harness unavailable (PORTABILITY: local-model)"
elif [ ! -f "$LM_MANIFEST" ]; then
  warn "qwen3:30b-a3b manifest missing under local-model/models" "OLLAMA_MODELS=$LM_MODELS_DIR ollama pull qwen3:30b-a3b (~18 GB; PORTABILITY: local-model)"
else
  LM_TAGS=$(curl -sS -m 4 http://127.0.0.1:11434/api/tags 2>&1)
  LM_TAGS_RC=$?
  if [ "$LM_TAGS_RC" -ne 0 ] || ! echo "$LM_TAGS" | grep -q '"qwen3:30b-a3b"'; then
    warn "ollama serve not answering /api/tags with qwen3:30b-a3b loaded" "OLLAMA_MODELS=$LM_MODELS_DIR ollama serve (PORTABILITY: local-model) — local-model harness tasks will refuse (rc 2)"
  else
    ok "local-model harness: ollama serving qwen3:30b-a3b"
  fi
fi

# --- Ornith night job (Kam, panel 2026-09-14 18:15:36: "lets use Ornith at night in the
# downtime (when no other agents run) … Set this up as a rule and get it working on the
# backlog"). Rule: 0_Brain/learnings/2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md.
# Mechanism: 2_Project_Files/local-model/night/ (night_run.sh + queue.md + install_night.command).
# Four facts, warn-level (the fleet runs without it; this says whether the NIGHT will):
#   job armed? · model present on the drive-local Ollama? · queue non-empty? · last run's exit + age.
# Wednesday's seat only — on another agent's Mac the job is expected absent, so only an INFO line.
NIGHT_DIR="$PROJECT_DIR/2_Project_Files/local-model/night"
NIGHT_MODEL_TAG="ornith/35b"
NIGHT_MANIFEST="$PROJECT_DIR/2_Project_Files/local-model/models/manifests/registry.ollama.ai/library/$NIGHT_MODEL_TAG"
if [ "${WED_AGENT:-wednesday}" != "wednesday" ]; then
  ok "ornith night job: not this seat's (Wednesday only) — skipped"
elif [ ! -f "$NIGHT_DIR/night_run.sh" ]; then
  warn "ornith night runner missing" "2_Project_Files/local-model/night/night_run.sh is gone — the 2026-09-14 rule has no mechanism (PORTABILITY 15)"
else
  if launchctl print "gui/$(id -u)/com.wednesday.ornith-night" >/dev/null 2>&1; then
    ok "ornith night job armed (com.wednesday.ornith-night, 23:30)"
  else
    warn "ornith night job NOT armed" "bash 2_Project_Files/local-model/night/install_night.command (PORTABILITY 15) — nothing runs the backlog at night until it is"
  fi
  # 2026-09-15 23:1x (Kam 18:19 "know progress continues through the week"): the 06:45 daily RECEIPT job posts one
  # counted panel line from the runner's own records (night/daily_receipt.sh --post). Monday-loop piece (e).
  if [ -f "$PROJECT_DIR/2_Project_Files/local-model/night/daily_receipt.sh" ]; then
    if launchctl print "gui/$(id -u)/com.wednesday.ornith-receipt" >/dev/null 2>&1; then
      ok "ornith daily receipt armed (com.wednesday.ornith-receipt, 06:45 → the panel)"
    else
      warn "ornith daily receipt NOT armed" "bash 2_Project_Files/local-model/night/install_receipt.command (PORTABILITY 15) — Kam gets no morning line from the night's work until it is"
    fi
  else
    warn "ornith daily receipt script missing" "2_Project_Files/local-model/night/daily_receipt.sh is gone — the 18:19 rule's receipt has no mechanism"
  fi
  # 2026-09-15 (Kam 2026-09-14 21:57: Ornith 24/7 when no other agents run): the 15-minute loop job.
  # night_run.sh's own G2 pane census is the gate; a run lock stops overlap with the 23:30 job.
  if launchctl print "gui/$(id -u)/com.wednesday.ornith-loop" >/dev/null 2>&1; then
    ok "ornith 24/7 loop armed (com.wednesday.ornith-loop, every 900 s; G2 refuses while any agent pane is live)"
  else
    warn "ornith 24/7 loop NOT armed" "render 2_Project_Files/local-model/night/com.wednesday.ornith-loop.plist to ~/Library/LaunchAgents and launchctl bootstrap it (PORTABILITY 15b) — Ornith then runs only at 23:30"
  fi
  if [ -f "$NIGHT_MANIFEST" ]; then
    NIGHT_TAGS=$(curl -sS -m 4 http://127.0.0.1:11434/api/tags 2>&1)
    if [ $? -eq 0 ] && echo "$NIGHT_TAGS" | grep -q '"ornith:35b"'; then
      ok "ornith:35b on the drive and served (/api/tags)"
    else
      warn "ornith:35b on the drive but Ollama not serving it" "bash 2_Project_Files/local-model/start_ollama.sh (PORTABILITY 14/15) — it uses the drive-local binary + OLLAMA_MODELS, the two things a hand-start gets wrong; night_run's G5 also calls it itself now (2026-09-16)"
    fi
  else
    warn "ornith:35b manifest missing under local-model/models" "OLLAMA_MODELS=<local-model>/models ollama pull ornith:35b (~20 GB; PORTABILITY 15)"
  fi
  NIGHT_Q=$(grep -v -E '^[[:space:]]*(#|$)' "$NIGHT_DIR/queue.md" 2>/dev/null | wc -l | tr -d ' ')
  if [ "${NIGHT_Q:-0}" -gt 0 ]; then
    ok "ornith night queue: $NIGHT_Q ticket(s) pending in night/queue.md"
  else
    warn "ornith night queue EMPTY" "re-derive night/queue.md from the KS board (Backlog/Todo, one file, fix shape, in-process test; see the queue header) — the job exits 4 until then"
  fi
  if [ -f "$NIGHT_DIR/log/last_run.json" ]; then
    NIGHT_LAST=$(python3 - "$NIGHT_DIR/log/last_run.json" <<'PYEOF' 2>/dev/null
import json, sys, datetime
j = json.load(open(sys.argv[1])); end = j.get("ended", "")
age_h = "?"
try:
    t = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S"); age_h = round((datetime.datetime.now() - t).total_seconds() / 3600, 1)
except Exception:
    pass
print(f"{j.get('exit')}|{j.get('reason','')}|{age_h}|{j.get('tickets_run',0)}|{','.join(j.get('verdicts',[]))}")
PYEOF
)
    NIGHT_RC="${NIGHT_LAST%%|*}"; NIGHT_REST="${NIGHT_LAST#*|}"; NIGHT_REASON="${NIGHT_REST%%|*}"; NIGHT_REST="${NIGHT_REST#*|}"; NIGHT_AGE="${NIGHT_REST%%|*}"; NIGHT_REST="${NIGHT_REST#*|}"; NIGHT_N="${NIGHT_REST%%|*}"; NIGHT_V="${NIGHT_REST#*|}"
    case "$NIGHT_RC" in
      0) ok "ornith night last run: rc 0 ($NIGHT_N ticket(s): ${NIGHT_V:-none}) ${NIGHT_AGE}h ago" ;;
      4) ok "ornith night last run: rc 4 queue empty, ${NIGHT_AGE}h ago" ;;
      3) ok "ornith night last run: rc 3 $NIGHT_REASON, ${NIGHT_AGE}h ago (a refusal is the gate working — read night/log/)" ;;
      *) warn "ornith night last run rc ${NIGHT_RC:-?} ${NIGHT_AGE}h ago" "$NIGHT_REASON — read 2_Project_Files/local-model/night/log/" ;;
    esac
  else
    ok "ornith night: no run recorded yet (night/log/last_run.json absent)"
  fi
fi

# --- Weekly-usage launch gate (Kam, panel 2026-09-14 19:14:25: "Once it reaches 90%, let's stop
# using other agents and we'll move to a model of you working with the local model"; confirmed
# 19:15:46). Mechanism: fleet/usage_gate.sh in BOTH launch paths (brief_and_launch.sh STEP 0,
# cockpit.sh add). Each part alone is decoration — a missing wiring is a hard FAIL.
UG="$PROJECT_DIR/2_Project_Files/fleet/usage_gate.sh"
if [ ! -x "$UG" ]; then
  fail "usage gate script missing/not executable" "2_Project_Files/fleet/usage_gate.sh — the 2026-09-14 90% rule has no mechanism"
else
  UG_W=0
  grep -q 'usage_gate.sh' "$PROJECT_DIR/2_Project_Files/fleet/brief_and_launch.sh" 2>/dev/null && UG_W=$((UG_W+1))
  grep -q 'usage_gate.sh' "$PROJECT_DIR/2_Project_Files/fleet/cockpit/cockpit.sh" 2>/dev/null && UG_W=$((UG_W+1))
  if [ "$UG_W" -eq 2 ]; then
    UG_OUT=$(bash "$UG" --check 2>&1); UG_RC=$?
    case "$UG_RC" in
      0) ok "usage gate wired ×2; $(printf '%s' "$UG_OUT" | sed 's/^usage_gate: OK — //')" ;;
      3) warn "USAGE GATE CLOSED — no new agents" "$(printf '%s' "$UG_OUT" | tail -1 | cut -c1-120)" ;;
      *) warn "usage gate gauge unreadable/stale" "$(printf '%s' "$UG_OUT" | tail -1 | cut -c1-120)" ;;
    esac
  else
    fail "usage gate wired in $UG_W of 2 launch paths" "brief_and_launch.sh + cockpit.sh add must both call fleet/usage_gate.sh"
  fi
fi

# --- Live-board usage gauge publisher (Kam, live board 2026-09-22 08:57:36: "I was able to see the weekly
# usage count on both Wednesday and Tuesday. Is this possible for the live version?"). Mechanism:
# dashboard-cloud/seat/publish_usage.sh (a detached loop, --arm) hands this seat's usage_<seat>.json to
# seat/post_usage.py every 2 min -> POST /api/seat/usage (token-attributed). Not armed = the live chips
# read "no reading" within 30 min. WARN, never FAIL: a gauge is a degraded feature, not a broken seat.
UPUB="$PROJECT_DIR/2_Project_Files/dashboard-cloud/seat/publish_usage.sh"
UHEALTH="$PROJECT_DIR/2_Project_Files/fleet/cockpit/state/usage_publish.health"
if [ ! -x "$UPUB" ]; then
  warn "live usage publisher missing/not executable" "2_Project_Files/dashboard-cloud/seat/publish_usage.sh — the live chips will show 'no reading'"
elif bash "$UPUB" --status >/dev/null 2>&1; then
  UH="$(head -1 "$UHEALTH" 2>/dev/null)"
  case "$UH" in
    OK*)      ok "live usage publisher running; $(printf '%s' "$UH" | cut -c1-100)" ;;
    FAILING*) warn "live usage publisher FAILING" "$(printf '%s' "$UH" | cut -c1-110) — read fleet/cockpit/logs/usage_publish.log" ;;
    *)        warn "live usage publisher running, no health line yet" "first tick pending — fleet/cockpit/logs/usage_publish.log" ;;
  esac
else
  warn "live usage publisher NOT armed on this seat" "bash 2_Project_Files/dashboard-cloud/seat/publish_usage.sh --arm  (live chips show 'no reading' otherwise)"
fi

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
        126) warn "scheduler $job last exit 126" "TCC: /bin/bash lacks Full Disk Access on this machine — Kam's hands (PORTABILITY 15)";;
        78:*|78) warn "scheduler $job last exit $lec" "EX_CONFIG: launchd refused the plist — usually an out/err path it cannot open; logs must live in ~/Library/Logs (PORTABILITY 22)";;
        127) warn "scheduler $job last exit 127" "its script was not found at fire time — re-run scheduler/install_scheduler.command";;
        *) ok "scheduler $job loaded (last exit ${lec:-never})";;
      esac
    fi
  else
    warn "scheduler $job not loaded" "run scheduler/install_scheduler.command"
  fi
done

# --- NAS replica staleness (added 2026-09-21, Kam 09:48 "build it today") ---
# The nassync job above being LOADED with a last exit of 2 was true for six nights while the
# files that change every night — history.md, the ledger, NEXT-PICKUP.md, the daily note —
# sat on the NAS days old: unison aborts a transfer when the source changes under it, and the
# fleet writes those files all night. A green job line is not a landed file
# (2026-08-05_verify-the-chain-not-the-legs). nas_staleness.sh compares the key files on both
# sides by sha256 (read-only). Not mounted is a stated SKIP, not a pass and not a warning: a
# laptop without the NAS in reach has nothing to measure. The 36 h threshold is one missed
# night plus a working day — a single bad night self-heals at the next 03:30; two do not.
NS="$PROJECT_DIR/2_Project_Files/scheduler/nas_staleness.sh"
if [ -f "$NS" ]; then
  NS_OUT="$(bash "$NS" --warn-hours 36 2>&1)"; NS_RC=$?
  NS_SUM="$(printf '%s\n' "$NS_OUT" | /usr/bin/grep -i '^staleness:' | tail -1)"
  if printf '%s\n' "$NS_OUT" | /usr/bin/grep -qi '^SKIP'; then
    ok "NAS staleness not measured — $(printf '%s\n' "$NS_OUT" | /usr/bin/grep -i '^SKIP' | head -1 | cut -c1-90)"
  elif [ "$NS_RC" -eq 0 ] && [ -n "$NS_SUM" ]; then
    ok "NAS replica key files current ($NS_SUM)"
  elif [ -n "$NS_SUM" ]; then
    warn "NAS replica STALE >36h or MISSING ($NS_SUM)" \
         "$(printf '%s\n' "$NS_OUT" | /usr/bin/grep -iE '^(STALE|MISSING)' | awk '{print $NF}' | xargs | cut -c1-160) — read scheduler/state/nas_sync_last_${_DOC_AGENT}.txt: its 'retry: A → B' says whether the retry pass carried them"
  else
    warn "nas_staleness.sh produced no summary line" "bash 2_Project_Files/scheduler/nas_staleness.sh — $(printf '%s\n' "$NS_OUT" | head -1 | cut -c1-120)"
  fi
else
  warn "scheduler/nas_staleness.sh missing" "restore it from git — without it a stale NAS replica is invisible until someone diffs a file by hand"
fi

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

# --- Rotation LIVENESS check (2026-09-13): at 16:04:29 on 09-12 a `respawn-pane -k`
# on the coordinator's pane was followed 36 ms later by the death of the WHOLE fleet
# session — three agents, the QA gate, the monitor — and the rotate script reported
# "respawned OK; agents are untouched" without looking (1 loss in 63 rotations, trigger
# never established: reference/2026-09-13_fleet-loss-1604/). The guard is a detached
# checker, rotate_liveness.sh, that the rotate script spawns BEFORE the respawn. Three
# parts, each a FAIL if missing: the checker exists + is executable, parses
# (`bash -n`), and wednesday_rotate.sh actually references it — a checker nothing
# spawns is decoration.
RL="$PROJECT_DIR/2_Project_Files/fleet/cockpit/rotate_liveness.sh"
if [ ! -x "$RL" ]; then
  fail "rotate_liveness.sh missing or not executable" "a rotation would run UNGUARDED: the 16:04 loss class (whole fleet gone at respawn) goes unnoticed — restore 2_Project_Files/fleet/cockpit/rotate_liveness.sh (+x)"
elif ! bash -n "$RL" 2>/dev/null; then
  fail "rotate_liveness.sh does not parse (bash -n)" "the rotate script would spawn a checker that dies at once — fix the syntax error"
elif ! grep -q 'rotate_liveness.sh' "$RT" 2>/dev/null; then
  fail "wednesday_rotate.sh does not spawn rotate_liveness.sh" "the post-respawn liveness check is NOT wired — restore the spawn block in wednesday_rotate.sh"
else
  ok "rotation liveness check wired (rotate_liveness.sh +x, parses, spawned by wednesday_rotate.sh)"
fi
# The checker's FIRE path leaves state/ROTATE_LOSS_<ts>.txt (before + after pane lists).
# LOUD until a seat reads it: never deleted here — the seat quarantines it (move, never
# rm; learnings/2026-08-26_never-delete-cleanup-means-quarantine) once the loss is handled.
# 2026-09-16 — the alarm now distinguishes a REAL loss from a TEST one. rotate_liveness.sh is
# deliberately runnable against a scratch session (the rotate arms use `rtest` / `wedtest_*`), and
# its FIRE path writes the same alarm file when that scratch session ends — which is the expected
# end of a test, not an incident. One such file from 06:58 on 09-14 had been warning at EVERY
# launch for two days. A warning that cannot be acted on is how a real one gets ignored, so a file
# whose own first line names a session other than `fleet` is counted and reported, never warned on.
ROTATE_LOSS_ALL="$(find "$PROJECT_DIR/2_Project_Files/fleet/cockpit/state" -maxdepth 1 -name 'ROTATE_LOSS_*.txt' 2>/dev/null | sort)"
ROTATE_LOSS_FILES=""; ROTATE_LOSS_TEST=0
for _rl in $ROTATE_LOSS_ALL; do
  if head -1 "$_rl" 2>/dev/null | /usr/bin/grep -q -i -- "session 'fleet'"; then
    ROTATE_LOSS_FILES="$ROTATE_LOSS_FILES $_rl"
  else
    ROTATE_LOSS_TEST=$((ROTATE_LOSS_TEST + 1))
  fi
done
if [ -n "${ROTATE_LOSS_FILES// /}" ]; then
  warn "!!! FLEET LOSS ALARM from a rotation: $(printf '%s\n' $ROTATE_LOSS_FILES | xargs -n1 basename | tr '\n' ' ')" \
       "a rotation lost the fleet session or an agent pane — READ the file(s) (before/after pane lists), relaunch what is missing, then QUARANTINE the file (move it under 0_Brain/reference/<date>_fleet-loss/; never rm)"
else
  # `${VAR:+...}` expands on the STRING "0", which is non-empty — so the suffix needs a numeric test,
  # not a set-test, or a clean floor reports "(0 ... ignored)".
  if [ "$ROTATE_LOSS_TEST" -gt 0 ]; then
    ok "no ROTATE_LOSS alarm files for the fleet session ($ROTATE_LOSS_TEST from a scratch/test session, ignored)"
  else
    ok "no ROTATE_LOSS alarm files in cockpit/state"
  fi
fi

# ── ROTATE_PENDING: a rotation armed a liveness checker that never reported ──
# 2026-09-20. The checker armed 40 times against the real fleet and logged a verdict
# 15 times; from 09-18 00:54 it was nine armings and zero verdicts. NOTHING said so —
# the rotate log recorded "respawned OK — liveness verdict follows in ~25 s" and the
# verdict simply never came, and no file, warning or tap existed to notice. Two days.
# wednesday_rotate.sh now writes state/rotate_pending_<ts>.txt BEFORE the respawn and
# rotate_liveness.sh is the ONLY thing that clears it (by rename to consumed_*), on
# every path that logs a verdict. So a marker still here = a rotation that went
# UNVERIFIED, and this leg is where the successor lands on it at its next boot.
# -mmin +5 is the grace window: a rotation in flight has a marker ~25 s old and must
# not warn. Real-fleet vs scratch is the same first-line read the ROTATE_LOSS leg uses.
ROTATE_PENDING_ALL="$(find "$PROJECT_DIR/2_Project_Files/fleet/cockpit/state" -maxdepth 1 -name 'rotate_pending_*.txt' -mmin +5 2>/dev/null | sort)"
ROTATE_PENDING_FILES=""; ROTATE_PENDING_TEST=0
for _rp in $ROTATE_PENDING_ALL; do
  if head -1 "$_rp" 2>/dev/null | /usr/bin/grep -q -i -- "session 'fleet'"; then
    ROTATE_PENDING_FILES="$ROTATE_PENDING_FILES $_rp"
  else
    ROTATE_PENDING_TEST=$((ROTATE_PENDING_TEST + 1))
  fi
done
if [ -n "${ROTATE_PENDING_FILES// /}" ]; then
  warn "!!! ROTATION WENT UNVERIFIED: liveness checker armed and never reported: $(printf '%s\n' $ROTATE_PENDING_FILES | xargs -n1 basename | tr '\n' ' ')" \
       "the rotation's liveness check produced NO verdict, so nothing confirmed the fleet session or its agent panes survived that respawn — check the fleet session and every agent pane BY HAND now, then QUARANTINE the file(s) (move under 0_Brain/reference/<date>_rotation-unverified/; never rm)"
else
  if [ "$ROTATE_PENDING_TEST" -gt 0 ]; then
    ok "no unverified rotations ($ROTATE_PENDING_TEST pending marker(s) from a scratch/test session, ignored)"
  else
    ok "no unverified rotations (every armed liveness checker logged a verdict)"
  fi
fi

# ── PAUSE_QUEUE EXPIRED: a deliberate Ornith pause whose expiry nothing observed ──
# 2026-09-20: a pause written with an expiry (20:05) ran out and Ornith sat idle 70 min,
# then 83 min again at the next boot — the G7 busy leg lives INSIDE night_run.sh, which
# does not run while the queue is empty, so the alarm could not fire in exactly the state
# it guards (learnings/2026-09-20_a-guard-inside-the-thing-it-guards.md). The observer
# must live OUTSIDE the paused system: this check, on doctor's own clock.
# Overrides for the arms: NIGHT_PAUSE_FILE (the file), DOCTOR_NOW_EPOCH (the clock).
_PQ="${NIGHT_PAUSE_FILE:-$PROJECT_DIR/2_Project_Files/local-model/night/PAUSE_QUEUE}"
if [ -f "$_PQ" ]; then
  _pq_epoch="$(head -1 "$_PQ" | tr -dc 0-9)"
  _pq_now="${DOCTOR_NOW_EPOCH:-$(date +%s)}"
  # a 10-digit epoch only: a date string's digits (202609202331) would read as an epoch
  # that never expires — the 2026-09-17 ALLOW_SEATS defect, caught here by arm A3
  if [ -z "$_pq_epoch" ] || [ "${#_pq_epoch}" -ne 10 ]; then
    warn "PAUSE_QUEUE has NO 10-digit epoch on line 1 (read: '${_pq_epoch:-empty}')" "night_run.sh reads line 1's digits as an expiry; a pause without one never expires — rewrite it as \$(date -j ... +%s) or move it aside (never rm)"
  elif [ "$_pq_epoch" -lt "$_pq_now" ]; then
    warn "!!! PAUSE_QUEUE EXPIRED $(( (_pq_now - _pq_epoch) / 60 )) min ago and Ornith may be idle" \
         "expired $(date -r "$_pq_epoch" '+%F %H:%M' 2>/dev/null): $(sed -n 2p "$_PQ" | cut -c1-120) — run fleet/ornith_status.py, queue the next brief, and move the pause file aside (never rm)"
  else
    ok "Ornith pause live until $(date -r "$_pq_epoch" '+%F %H:%M' 2>/dev/null) (deliberate, unexpired)"
  fi
else
  ok "no Ornith pause file (queue not deliberately paused)"
fi

# --- panel_sync loop alive (2026-09-13): Kam's ONE chat page is kept current by
# `panel_sync.sh loop` (60 s cycles, detached, outside tmux). It died with the 09-12
# 16:27 reboot and nothing noticed until a seat read the log at 08:45 the next morning
# — his page was 16 hours stale and no check said so. The log is written by the loop
# itself (every cycle), so the log's mtime IS the newest line's time. Not running with a
# log present = FAIL (the machine has run it before, so it is expected here); running but
# the log older than 5 min = WARN with the age (the loop is wedged or sleeping past its
# cycle). No log at all = never run on this machine (fresh clone): ok, the launcher arms it.
# EXERCISE OVERRIDES (never set in production; both documented here so the check can be
# fired without stopping the live loop): DOCTOR_PANEL_SYNC_LOG=<path> points the check at
# another log (a scratch copy with an old mtime exercises the WARN);
# DOCTOR_PANEL_SYNC_PGREP_PATTERN=<pattern> replaces the pgrep pattern (one that matches
# nothing exercises the FAIL).
PS_LOG="${DOCTOR_PANEL_SYNC_LOG:-$PROJECT_DIR/2_Project_Files/tools/logs/panel_sync.log}"
PS_PAT="${DOCTOR_PANEL_SYNC_PGREP_PATTERN:-panel_sync\.sh loop}"
if [ -f "$PS_LOG" ]; then
  if ! pgrep -f "$PS_PAT" >/dev/null 2>&1; then
    fail "panel_sync loop NOT running (log exists: $(basename "$PS_LOG"))" "Kam's chat page goes stale — the launcher arms it at boot; by hand: python3 -c 'import os,sys; os.setsid(); os.execvp(sys.argv[1], sys.argv[1:])' nohup bash 2_Project_Files/tools/panel_sync.sh loop </dev/null >> 2_Project_Files/tools/logs/panel_sync.log 2>&1 &"
  else
    PS_AGE=$(( $(date +%s) - $(stat -f %m "$PS_LOG" 2>/dev/null || echo 0) ))
    if [ "$PS_AGE" -gt 300 ]; then
      warn "panel_sync loop running but its log is ${PS_AGE}s old (>300 s)" "the loop should write every 60 s — read $(basename "$PS_LOG") tail; a wedged loop looks alive to pgrep"
    else
      ok "panel_sync loop running, log ${PS_AGE}s fresh"
    fi
  fi
else
  ok "panel_sync: no log yet on this machine (never run) — the launcher arms it"
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

# ── WEEK INSTRUCTION — Kam's away-week standing instruction expires itself (added 2026-09-16) ──
# 1_Project_Definition/Architecture/2026-09-16_unattended-week-loop.md piece (a): a fresh seat boots on
# 0_Brain/tasks/WEEK-INSTRUCTION.md instead of Kam while he is away (Monday night 2026-09-21 →). The file
# carries `status:` and `valid_until:`; a live file past its date is the 09-06 scoped-override failure
# (a permanent instruction nobody decided to make), so this leg WARNS on it at every launch.
WI="$PROJECT_DIR/0_Brain/tasks/WEEK-INSTRUCTION.md"
if [ -f "$WI" ]; then
  WI_STATUS=$(/usr/bin/grep -m1 -i '^status:' "$WI" | sed 's/^[Ss]tatus:[[:space:]]*//' | tr -d '[:space:]')
  WI_UNTIL=$(/usr/bin/grep -m1 -i '^valid_until:' "$WI" | sed 's/^[Vv]alid_until:[[:space:]]*//' | tr -d '[:space:]')
  if [ "$WI_STATUS" = "live" ] && [ -n "$WI_UNTIL" ] && [ "$(date +%Y-%m-%d)" \> "$WI_UNTIL" ]; then
    warn "WEEK-INSTRUCTION.md is LIVE but LAPSED (valid_until $WI_UNTIL)" "Kam's away-week instruction outlived its date: STOP briefing on its authority; set status: lapsed and card Kam (learnings/2026-09-06_a-scoped-override-carries-its-own-expiry.md)"
  elif [ "$WI_STATUS" = "live" ]; then
    ok "WEEK-INSTRUCTION.md LIVE until $WI_UNTIL — Kam away; the boot's first act is to brief the next candidates"
  else
    ok "WEEK-INSTRUCTION.md status: ${WI_STATUS:-none} — no away-week instruction in force (normal boot)"
  fi
else
  warn "WEEK-INSTRUCTION.md missing" "the launcher's boot step 4 names it; restore it from git"
fi

# ── NEXT-PICKUP stays ONE live block (added 2026-09-18, ledger w=2 "I regressed my own fix") ──
# The 10:0x seat split NEXT-PICKUP 220 KB → 8 KB under its own `replace wholesale; do not append`
# rule, then re-appended 14 UPDATE blocks by 13:4x (40 KB). The rule lives in the file's frontmatter,
# which nobody re-reads while appending, so it is checked here instead. WED_PICKUP_FILE is a test seam.
NP="${WED_PICKUP_FILE:-$PROJECT_DIR/0_Brain/tasks/NEXT-PICKUP.md}"
if [ -f "$NP" ]; then
  NP_BLOCKS=$(/usr/bin/grep -c '^## ' "$NP")
  NP_BYTES=$(stat -f%z "$NP")
  if [ "$NP_BLOCKS" -gt 1 ] || [ "$NP_BYTES" -gt 15360 ]; then
    warn "NEXT-PICKUP.md has regrown ($NP_BLOCKS live ## blocks, $NP_BYTES B)" "its own rule is 'replace wholesale; do not append': consolidate to ONE block, archive the rest verbatim to NEXT-PICKUP-archive.md (conservation asserted)"
  else
    ok "NEXT-PICKUP.md is one live block ($NP_BYTES B)"
  fi
else
  warn "NEXT-PICKUP.md missing" "boot step 4 names it; restore it from git"
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
# 2026-09-20 21:4x — TWO holes found by measurement while this check printed OK:
#  (1) `Launch_*.command` in the allow-list MATCHED a unison conflict copy,
#      `Launch_Wednesday (conflict_on_2026-09-18).command` — a stale duplicate of
#      the launcher sitting unflagged in the root. A conflict copy is a NEW file
#      that matches the same glob as the real one (learnings/2026-09-10_a-sync-
#      conflict-copy-is-an-input-to-every-glob). So conflict copies are tested
#      FIRST, before any allow-list can swallow them.
#  (2) `[ -f "$f" ] || continue` skipped DIRECTORIES outright, so a stray `logs/`
#      in the root was invisible to the one check whose job is stray root entries.
#      Directories are now checked against their own allow-list.
ROOT_STRAYS=""
for f in "$PROJECT_DIR"/* "$PROJECT_DIR"/.[!.]*; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  case "$b" in *conflict_on*) ROOT_STRAYS="$ROOT_STRAYS $b"; continue ;; esac
  if [ -d "$f" ]; then
    case "$b" in
      0_Brain|1_Project_Definition|2_Project_Files|3_Access_Keys|4_Credentials|5_Project_History|.git|.claude) ;;
      *)
        # A directory someone deliberately GITIGNORED is a state drawer by a recorded
        # decision (logs/, .playwright-mcp/ — .gitignore:161 and :49), not a filing
        # miss. Keying on that decision instead of on a name list means a new tool
        # drawer needs no edit here, and a guard that fires every launch on something
        # legitimate is a guard nobody reads (2026-09-10 rule 4). Conflict copies are
        # tested ABOVE this, so a gitignored one is still caught.
        if git -C "$PROJECT_DIR" check-ignore -q "$b" 2>/dev/null; then :
        else ROOT_STRAYS="$ROOT_STRAYS $b/"; fi
        ;;
    esac
    continue
  fi
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


# --- Claude Code hooks + permission guards (2026-09-16) -----------------------
# FAILS, not warns. .claude/settings.local.json is gitignored, so on 2026-09-16 Tuesday's
# copy was 169 bytes of statusline against Wednesday's 1775: she had been running with NO
# PreCompact block and NO PreToolUse guards, and no check anywhere said so. A guard that one
# seat silently lacks is the shape this whole file exists to prevent, so a missing hook is a
# hard failure rather than a line in the scroll.
RENDER_TOOL="$PROJECT_DIR/2_Project_Files/tools/render_claude_settings.py"
SETTINGS_LOCAL="$PROJECT_DIR/.claude/settings.local.json"
if [ ! -f "$PROJECT_DIR/.claude/settings.template.json" ]; then
  fail "no .claude/settings.template.json — this seat's hooks cannot be rendered" \
       "restore it from git; it is the tracked source of every seat's hooks and permission rules"
elif [ ! -f "$SETTINGS_LOCAL" ]; then
  fail ".claude/settings.local.json is ABSENT — this seat is running with no hooks" \
       "python3 2_Project_Files/tools/render_claude_settings.py"
else
  HOOK_N="$(python3 -c '
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception: print(-1); raise SystemExit
n=0
for blocks in (d.get("hooks") or {}).values():
    for b in blocks: n += len(b.get("hooks",[]))
print(n)' "$SETTINGS_LOCAL" 2>/dev/null || echo -1)"
  if [ "${HOOK_N:--1}" -lt 6 ]; then
    fail "this seat has only ${HOOK_N} Claude Code hook(s) wired, expected 6" \
         "python3 2_Project_Files/tools/render_claude_settings.py — WITHOUT them there is no PreCompact block and no Bash guards (no cd / no rm / seat-scoped chat / grep-case)"
  elif [ -x "$RENDER_TOOL" ] && ! python3 "$RENDER_TOOL" --check >/dev/null 2>&1; then
    warn "the rendered settings differ from the tracked template" \
         "python3 2_Project_Files/tools/render_claude_settings.py (the launcher does this at every boot; a drift here means someone edited the rendered file)"
  else
    ok "Claude Code hooks wired ($HOOK_N) and matching the tracked template"
  fi
fi

# --- every scheduled job this seat needs (2026-09-16) -------------------------
# install_scheduler.command armed THREE of the nine launchd jobs that keep a coordinator
# alive; the other six existed only as loaded jobs on Wednesday's Mac with no plist on the
# drive, so a new machine got three of nine and Tuesday's got none — the job that puts her
# replies on Kam's page had never run there. The plists are now tracked templates under
# scheduler/jobs/ and scheduler/install_all_jobs.sh renders them for whichever seat runs it.
JOBS_INSTALLER="$PROJECT_DIR/2_Project_Files/scheduler/install_all_jobs.sh"
if [ ! -x "$JOBS_INSTALLER" ]; then
  warn "scheduler/install_all_jobs.sh missing or not executable" \
       "restore it from git — without it only three of this seat's nine launchd jobs are armed by any installer"
elif JOBS_OUT="$(env -u WED_AGENT bash "$JOBS_INSTALLER" --check 2>&1)"; then
  ok "scheduled jobs: $(printf '%s' "$JOBS_OUT" | tail -1)"
else
  warn "scheduled jobs MISSING for this seat: $(printf '%s' "$JOBS_OUT" | tail -1)" \
       "bash 2_Project_Files/scheduler/install_all_jobs.sh (from this seat's own tree, WED_AGENT unset) — a missing job is a mechanism that silently never fires"
fi

# ── PYTHON TOOLS REFERENCE ONLY NAMES THEY BIND (2026-09-20, Tuesday) ─────────
# Patching reconcile_rulings.py I added os.environ to a module whose imports read
# "import json, re, subprocess, sys", and verified it with ast.parse — which
# printed "syntax OK" on a module that could not load. Measured the same night:
# `python3 -m py_compile` PASSES on that exact defect too. A syntax check cannot
# fail on a missing name, so both were checks that could not catch what they were
# pointed at. Running the tool caught it; this makes the catch a mechanism.
# WARNS rather than FAILS: it reads module scope only (stated limit in the
# checker), so it is a real signal, not a proof, and a false positive must not
# stop a boot. Armed both ways before wiring: a fixture using os without
# importing it is flagged; the same file with the import passes; all 9 tools pass.
UNDEF="$PROJECT_DIR/2_Project_Files/tools/check_undefined_names.py"
if [ ! -f "$UNDEF" ]; then
  warn "tools/check_undefined_names.py missing" \
       "restore it from git — without it a tool can reference an unimported name and every syntax check still passes"
else
  UNDEF_OUT="$(python3 "$UNDEF" "$PROJECT_DIR"/2_Project_Files/tools/*.py 2>&1)"
  if [ $? -eq 0 ]; then
    ok "python tools: $(printf '%s' "$UNDEF_OUT" | tail -1)"
  else
    warn "python tool references an unbound name: $(printf '%s' "$UNDEF_OUT" | head -1)" \
         "python3 2_Project_Files/tools/check_undefined_names.py 2_Project_Files/tools/*.py — a syntax check will NOT show this"
  fi
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
