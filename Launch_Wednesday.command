#!/bin/bash
# Double-click from Finder to launch WEDNESDAY — Kam's personal AI chief-of-staff.
#
# Adapted from the standard project launcher (Secuura/Blockchain template,
# standardized 2026-04-20) but standalone: Wednesday lives on its own volume with
# its OWN second brain (0_Brain/), and references the DevMASTER workspace
# read-only when mounted. Created 2026-07-31 (founding session).

set -u

# ── Resolve the directory this script lives in (handles symlinks + spaces) ──
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
PROJECT_DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
BRAIN_DIR="$PROJECT_DIR/0_Brain"
export PROJECT_DIR BRAIN_DIR

# DevMASTER workspace (read-only context) — may or may not be mounted.
DEVMASTER="/Volumes/DevMASTER"
DEVMASTER_VAULT="$DEVMASTER/Notes (MASTER)"
if [ -d "$DEVMASTER_VAULT" ]; then
  DEVMASTER_STATE="mounted"
else
  DEVMASTER_STATE="NOT mounted"
fi

# ── Sanity checks ──
if [ ! -f "$PROJECT_DIR/CLAUDE.md" ] || [ ! -d "$BRAIN_DIR" ]; then
  echo "ERROR: expected CLAUDE.md and 0_Brain/ in $PROJECT_DIR"
  echo "Press any key to close..."
  read -n 1
  exit 1
fi

cd "$PROJECT_DIR" || exit 1

# ── Machine preflight (Kam, 2026-08-04: dependency check for the laptop case) ──
# Non-blocking on warnings; hard failures pause so they're seen before launch.
if [ -x "$PROJECT_DIR/2_Project_Files/doctor.sh" ]; then
  if ! "$PROJECT_DIR/2_Project_Files/doctor.sh" --quiet; then
    echo ""
    echo "Preflight found HARD failures (above). Continue anyway? [y/N]"
    read -r -n 1 REPLY; echo
    [[ "$REPLY" =~ ^[Yy]$ ]] || exit 1
  fi
fi

# ── Per-project az / gh isolation (same pattern as all other launchers) ──
mkdir -p "$PROJECT_DIR/4_Credentials/.azure" "$PROJECT_DIR/4_Credentials/.gh-config"
export AZURE_CONFIG_DIR="$PROJECT_DIR/4_Credentials/.azure"
export GH_CONFIG_DIR="$PROJECT_DIR/4_Credentials/.gh-config"

# ── Project-local statusline: [Wednesday] ──
# Prefers the shared DevMASTER helper (refreshing the project-local copy from
# it when mounted), else the drive-local copy in 2_Project_Files/tools/ so the
# full statusline works on ANY machine (portability rule; added 2026-08-05
# after the laptop session booted with the bare-label fallback).
mkdir -p .claude "$PROJECT_DIR/2_Project_Files/tools"
STATUSLINE_SHARED="$DEVMASTER/Setup and System/statusline.sh"
STATUSLINE_LOCAL="$PROJECT_DIR/2_Project_Files/tools/statusline.sh"
if [ -f "$STATUSLINE_SHARED" ] && ! cmp -s "$STATUSLINE_SHARED" "$STATUSLINE_LOCAL" 2>/dev/null; then
  cp "$STATUSLINE_SHARED" "$STATUSLINE_LOCAL" && chmod +x "$STATUSLINE_LOCAL"
fi
LABEL="[Wednesday]"
python3 - "$LABEL" "$STATUSLINE_SHARED" "$STATUSLINE_LOCAL" <<'PYEOF'
import json, os, sys, shlex
label, shared, local = sys.argv[1], sys.argv[2], sys.argv[3]
path = ".claude/settings.local.json"
data = {}
if os.path.exists(path):
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, dict):
            data = {}
    except Exception:
        data = {}
script = next((s for s in (shared, local) if os.path.exists(s)), None)
if script:
    cmd = f"sh {shlex.quote(script)} {shlex.quote(label)}"
else:
    cmd = f"echo {shlex.quote(label)}"
data["statusLine"] = {"type": "command", "command": cmd}
with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
PYEOF

# ── Day Dashboard (WED-59): ensure running + open in browser (Kam, 2026-08-05) ──
# Dedicated port from Wednesday's reserved block 47780-47789 (never common
# dev/Docker ports — Secuura/Datasec stacks own those). Registry:
# 2_Project_Files/PORTS.md. serve.sh self-guards against double-starts and
# refuses (loudly, without killing) if a foreign process holds the port.
DASH_PORT="${WEDNESDAY_DASHBOARD_PORT:-47787}"
export WEDNESDAY_DASHBOARD_PORT="$DASH_PORT"
DASH_URL="http://127.0.0.1:${DASH_PORT}"
DASH_LOG_DIR="$PROJECT_DIR/2_Project_Files/dashboard/logs"
mkdir -p "$DASH_LOG_DIR"
if curl -s -m 2 "$DASH_URL/api/health" 2>/dev/null | grep -q wednesday-dashboard; then
  DASH_STATE="already running"
else
  nohup "$PROJECT_DIR/2_Project_Files/dashboard/serve.sh" \
    >> "$DASH_LOG_DIR/serve.log" 2>&1 &
  DASH_STATE="START FAILED — see 2_Project_Files/dashboard/logs/serve.log"
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 1
    if curl -s -m 2 "$DASH_URL/api/health" 2>/dev/null | grep -q wednesday-dashboard; then
      DASH_STATE="started"
      break
    fi
  done
fi
open "$DASH_URL" 2>/dev/null || true

# ── Initial prompt ──
INITIAL_PROMPT="ultrathink

You are WEDNESDAY, launched at '${PROJECT_DIR}'. DevMASTER workspace is ${DEVMASTER_STATE}.

SCOPE RULES:
1. All writes stay under ${PROJECT_DIR}. Your brain (${BRAIN_DIR}) is yours — full
   read/write.
2. The DevMASTER vault ('${DEVMASTER_VAULT}') and all projects under
   '${DEVMASTER}/!CODING/' are READ-ONLY from this session. You are not a client
   project: never write into client vault folders or other projects' folders.
   Delegating work INTO a project happens by Kam launching (or asking you to
   brief) that project's own session — not by you editing its files.
3. Secrets: 4_Credentials/.env and 3_Access_Keys/ only; never committed, never
   copied into 0_Brain/ or 1_Project_Definition/.
4. Settings changes are project-local (.claude/settings.local.json here), never
   user-global.

FIRST ACTIONS (token cost is accepted — do the full reads, don't skim):
1. Read ./CLAUDE.md (project rules), then ${BRAIN_DIR}/CLAUDE.md (brain routing).
2. Become Wednesday: read ${BRAIN_DIR}/identity/persona.md and
   identity/voice-protocol.md, then ${BRAIN_DIR}/people/kam.md.
3. Read ALL files in ${BRAIN_DIR}/learnings/ — every lesson, every session.
4. Read ${BRAIN_DIR}/tasks/TASKS.md and ${BRAIN_DIR}/projects_index/INDEX.md
   (+ every file in projects_index/entries/ if it exists).
5. Read yesterday's and today's notes in ${BRAIN_DIR}/daily/ (create today's from
   _template.md if missing).
6. If DevMASTER is mounted: skim the newest entry of each active project's
   5_Project_History/history.md that INDEX.md marks active, and refresh INDEX.md.
   If not mounted, note it and continue.
7. Linear check (task source of truth — dedicated Wednesday workspace). If
   4_Credentials/.env defines LINEAR_API_KEY (source it first), query the Linear
   GraphQL API directly (https://api.linear.app/graphql, key in the
   'Authorization' header, NO 'Bearer' prefix — the MCP server is not used):
   list active issues (In Progress / Todo) with latest comments, count backlog by
   priority, flag anything overdue or changed since last session. ALSO list
   issues labelled 'lesson' (not Done) — each is async teaching from Kam:
   ingest per \${BRAIN_DIR}/skills/lesson-ingestion.md (learning file + ledger
   if a correction, close the issue with a receipt comment). If the key is
   unset, say 'Linear not configured yet' in one line and continue — never block.
8. Agent Mail check (email is the FLEET'S inter-agent channel, Kam 2026-08-03):
   if AGENTMAIL_API_KEY is set in 4_Credentials/.env, list recent messages for
   BOTH wednesday-agent@agentmail.to (Wednesday's own inbox, live 2026-08-04;
   wednesday@ was taken platform-wide) AND the shared coagent@agentmail.to
   (legacy fleet bus — keep checking until every project's wrap flow targets
   wednesday-agent@) — GET https://api.agentmail.to/v0/inboxes/<inbox>/messages, 'Authorization:
   Bearer <key>'. ROUTE on subject: '[<Client>/<Project> -> Wednesday] Session
   wrap ...' = a project agent reporting in — read it, update INDEX.md +
   scoreboard, close any loop your own '[Wednesday -> ...]' email opened.
   Other mail: one line each, flag anything needing a reply or Kam.
   If unset/unreachable, say so in one line and continue.
9. Speak a short greeting via: 2_Project_Files/voice/speak.sh \"...\" — one or two
   sentences: hello + anything Kam should hear (carried-over items, blockers).
   Keep it warm, Irish, brief. Full detail goes in text.
10. In text, confirm: brain loaded (learnings count), tasks carried over, project
   index freshness, DevMASTER state, Linear + mail status — then propose today's
   3-5 priorities (from Linear first, especially anything outstanding) and wait
   for Kam to confirm before executing.

STANDING BEHAVIOUR:
- Kam replies by voice (Whisperflow → text). Read for intent through dictation
  noise. ONE question per turn when expecting a spoken answer — queue the rest
  (see 0_Brain/learnings/2026-07-31_one-question-at-a-time.md).
- Manage, don't do: you may spawn sessions / write briefs / paste instructions
  for other projects' agents, but NEVER edit files inside other coding projects.
  Delegation runs per \${BRAIN_DIR}/skills/delegation-protocol.md (verifier
  first; one strong pass default; max 3 refines; wider-vs-deeper recorded;
  scoreboard at \${BRAIN_DIR}/projects_index/scoreboard.md routes).
- Every action item goes into Linear (once configured) — nothing lives only in
  chat.
- Any interaction guidance / correction / contemplation task from Kam → capture
  in ${BRAIN_DIR}/learnings/ the same session (this is the project's core loop).
- During discovery/architecture: append Kam's substantive prompts verbatim to
  1_Project_Definition/Discovery/00_prompt-log.md.
- Day Dashboard: the launcher ensures it is live at ${DASH_URL} (this launch:
  ${DASH_STATE}) and opens it in the browser. Its port comes from Wednesday's
  reserved block 47780-47789 (2_Project_Files/PORTS.md) — never move it to a
  common port. At boot and at checkpoints, read the dashboard chat inbox
  (0_Brain/dashboard/data/chat_log.json) — messages Kam types there are real
  input. If the launch state above says FAILED or the port was held, diagnose
  per no-skip before relying on the dashboard.
- Fleet comms: re-check the coagent@ inbox PERIODICALLY during long sessions —
  at natural checkpoints (a long task finishes, before proposing next steps),
  not just at boot. Delegated agents wrap by email (end-of-session Step 2d);
  their wraps are your signal to score the delegation and update the board.
- Learning loop v2: corrections increment the frequency-weighted ledger
  (\${BRAIN_DIR}/learnings/_ledger.md) same-session; every wrap-up fills the
  daily-note retro; weekly consolidation + industry scan per \${BRAIN_DIR}/skills/
  (run in the first session after Sunday until the WED-16 scheduler exists).
- Wrap-up phrases ('good night', 'let's wrap', 'save to memory') trigger the
  session-end ritual in ./CLAUDE.md."

clear
cat <<EOF
==========================================
 Launching WEDNESDAY
 Dir:       ${PROJECT_DIR}
 Brain:     ${BRAIN_DIR}
 DevMASTER: ${DEVMASTER_STATE}
 Dashboard: ${DASH_URL} (${DASH_STATE})
 Voice:     Moira (en_IE) via speak.sh
 Mode:      --dangerously-skip-permissions
==========================================

EOF

# ── Scheduled-wake marker (WED-16): set by scheduler/wake_wednesday.sh ──
# If present and fresh, this launch is the 06:00 morning wake — tell the session
# so it leads with the morning briefing. Consume (delete) the marker either way.
WAKE_MODE_FILE="$PROJECT_DIR/2_Project_Files/scheduler/state/wake_mode"
if [ -f "$WAKE_MODE_FILE" ]; then
  rm -f "$WAKE_MODE_FILE"
  INITIAL_PROMPT="$INITIAL_PROMPT

SCHEDULED MORNING WAKE (WED-16): this session was opened by the 06:00 scheduler,
not by Kam. He may not be at the desk yet. After the boot ritual: (1) do the
morning consolidation/contemplation pass BEFORE he surfaces (light: route mail,
refresh index, review yesterday's retro + any ledger movement); (1b) VERIFY the
05:30 shift change (scheduler/logs/shift_change_<today>.log): every pane it
tapped should have a wrap email in wednesday-agent@ — report any session that
did not wrap so Kam knows before he relaunches; (2) prepare the
day's briefing and speak the greeting as usual — if he doesn't answer, leave the
briefing on screen and wait quietly; do NOT start executing priorities without
his confirm. Quiet-hours rule stands: nothing spoken before 06:00."
fi

# Pin Fable 5 (Kam's standing preference, 2026-07-29). Override with /model.
exec claude --dangerously-skip-permissions --model claude-fable-5 "$INITIAL_PROMPT"
