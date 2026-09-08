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

# ── WHICH AGENT IS THIS SEAT (Kam, 2026-09-08 11:56: the Datasec agent is TUESDAY)
# The LAUNCHER FILE decides: Launch_Tuesday.command exports WED_AGENT=tuesday and
# execs this script. The hostname map below is only the DEFAULT, kept so the
# laptop's existing behaviour is byte-identical to before this change. It is
# deliberately not the authority — once the headless Datasec Mac exists its
# hostname is unknown, and a seat that guesses its own client is the failure this
# whole two-agent split is built to prevent.
AGENT="${WED_AGENT:-}"
if [ -z "$AGENT" ]; then
  case "$(hostname -s 2>/dev/null || hostname 2>/dev/null)" in
    Kamils-MBP*) AGENT="tuesday" ;;
    *)           AGENT="wednesday" ;;
  esac
fi
case "$AGENT" in
  wednesday) AGENT_NAME="Wednesday"; AGENT_UPPER="WEDNESDAY" ;;
  tuesday)   AGENT_NAME="Tuesday";   AGENT_UPPER="TUESDAY"   ;;
  *) echo "Launch: WED_AGENT must be wednesday or tuesday, got '$AGENT'" >&2; exit 2 ;;
esac
export WED_AGENT="$AGENT"          # chat_reply.sh reads this to pick its stream

# Tuesday gets her OWN Claude auth namespace (TESTED 2026-09-08: an empty
# CLAUDE_CONFIG_DIR answers "Not logged in · Please run /login" and builds its own
# .claude.json/projects/sessions). Wednesday is deliberately left on the global
# config: pointing her at a fresh one would log Kam's own seat out at its next
# launch, and that is his move to make, not this script's.
if [ "$AGENT" = "tuesday" ]; then
  export CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$PROJECT_DIR/4_Credentials/.claude}"
  mkdir -p "$CLAUDE_CONFIG_DIR"
fi

# DevMASTER workspace (read-only context) — may or may not be mounted.
DEVMASTER="/Volumes/DevMASTER"
DEVMASTER_VAULT="$DEVMASTER/Notes (MASTER)"
if [ -d "$DEVMASTER_VAULT" ]; then
  DEVMASTER_STATE="mounted"
else
  DEVMASTER_STATE="NOT mounted"
fi

# ── VAULT SSH POINTER HEAL (Kam ruling 2026-09-07 18:58, card `vault-ssh-pointer-heal`
# => `clauseandlauncher`) ────────────────────────────────────────────────────────────
# Every project launcher rewrites its OWN repo's core.sshCommand at each launch, so a
# drive rename self-heals there. THE SHARED VAULT HAS NO LAUNCHER, so its pointer froze
# at the old volume name and stayed broken. On 2026-09-07 a NexusAI agent hit it mid-wrap
# ("Permission denied (publickey)", which reads as "repository does not exist") and had to
# diagnose and repair it by hand; any session that ran the wrap ritual since the rename
# either hit it or silently skipped its vault push. The vault is the ONE repo every agent
# on the drive writes to, so a stale pointer there fails every project at once.
#
# This heals it on THIS drive, for every agent, at every Wednesday launch. It is
# deliberately narrow: it only rewrites when the configured key path does NOT exist and a
# key IS present at the drive-local path — so a correct pointer is never touched, and a
# genuinely missing key is left alone to be reported rather than papered over.
DRIVE_ROOT="$(cd -P "$PROJECT_DIR/.." && pwd)"
VAULT_LOCAL="$DRIVE_ROOT/Notes (MASTER)"
VAULT_KEY="$DRIVE_ROOT/Setup and System/keys/claude_obsidian_brain_deploy"
if [ -d "$VAULT_LOCAL/.git" ]; then
  VAULT_SSH="$(git -C "$VAULT_LOCAL" config --get core.sshCommand 2>/dev/null || true)"
  # quoted form first: the key path contains spaces ("Setup and System")
  VAULT_KEYPATH="$(printf '%s' "$VAULT_SSH" | sed -n 's/.*-i "\([^"]*\)".*/\1/p')"
  [ -n "$VAULT_KEYPATH" ] || VAULT_KEYPATH="$(printf '%s' "$VAULT_SSH" | sed -n 's/.*-i \([^ ]*\).*/\1/p')"
  if [ -n "$VAULT_KEYPATH" ] && [ ! -f "$VAULT_KEYPATH" ]; then
    if [ -f "$VAULT_KEY" ]; then
      git -C "$VAULT_LOCAL" config core.sshCommand \
        "ssh -i \"$VAULT_KEY\" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
      echo "  [vault] HEALED core.sshCommand: was -> $VAULT_KEYPATH (missing); now -> $VAULT_KEY"
    else
      echo "  [vault] WARNING: core.sshCommand points at $VAULT_KEYPATH (missing) and no key at $VAULT_KEY — vault pushes WILL fail; repair by hand." >&2
    fi
  fi
fi

# ── OWN-REPO SSH POINTER HEAL (2026-09-08, found while provisioning Tuesday) ─────────
# The comment above says "every project launcher rewrites its OWN repo's core.sshCommand
# at each launch". THIS launcher did not — it healed the vault and left itself alone, and
# nobody noticed because on the Studio the pointer has always been correct.
#
# It stops being harmless the moment the tree is CLONED or COPIED: Tuesday's tree on the
# T9 inherited `-i /Volumes/DevMASTER/WEDNESDAY/3_Access_Keys/github_deploy_rw`, a path
# that will not exist on her machine. Git reports that as "Permission denied (publickey)",
# which reads as "repository does not exist" — the exact 2026-09-07 diagnosis a NexusAI
# agent lost time to, and the 2026-08-25 travel-drive stale-pointer class pointed at
# Wednesday's own repo instead of someone else's.
#
# Same narrow shape as the vault heal: rewrite ONLY when the configured key path is
# missing AND a key exists in this tree. A correct pointer is never touched; a genuinely
# absent key is reported, never papered over.
OWN_KEY="$PROJECT_DIR/3_Access_Keys/github_deploy_rw"
if [ -d "$PROJECT_DIR/.git" ]; then
  OWN_SSH="$(git -C "$PROJECT_DIR" config --get core.sshCommand 2>/dev/null || true)"
  OWN_KEYPATH="$(printf '%s' "$OWN_SSH" | sed -n 's/.*-i "\([^"]*\)".*/\1/p')"
  [ -n "$OWN_KEYPATH" ] || OWN_KEYPATH="$(printf '%s' "$OWN_SSH" | sed -n 's/.*-i \([^ ]*\).*/\1/p')"
  if [ -n "$OWN_KEYPATH" ] && [ ! -f "$OWN_KEYPATH" ]; then
    if [ -f "$OWN_KEY" ]; then
      git -C "$PROJECT_DIR" config core.sshCommand \
        "ssh -i \"$OWN_KEY\" -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
      echo "  [repo] HEALED core.sshCommand: was -> $OWN_KEYPATH (missing); now -> $OWN_KEY"
    else
      echo "  [repo] WARNING: core.sshCommand points at $OWN_KEYPATH (missing) and no key at $OWN_KEY — pushes WILL fail; Kam must place the deploy key." >&2
    fi
  fi
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
# --- Boot digest (WED-139, Kam 2026-09-02 20:47 "go with a boot as you recommend"):
# regenerate 0_Brain/learnings/_boot_digest.md FROM the lesson files at every launch,
# so the seat never boots on a stale digest (in-path enforcement; doctor.sh is the
# backstop). Non-fatal: a generator failure falls back to the full lesson read.
python3 "$PROJECT_DIR/2_Project_Files/tools/boot_digest.py" --by-tier >/dev/null 2>/tmp/wednesday_boot_digest_bytier.$$ || echo "⚠ boot_digest.py --by-tier FAILED — the seat reads _boot_digest.md this boot: $(cat /tmp/wednesday_boot_digest_bytier.$$)"; rm -f /tmp/wednesday_boot_digest_bytier.$$
if python3 "$PROJECT_DIR/2_Project_Files/tools/boot_digest.py" >/tmp/wednesday_boot_digest.$$ 2>&1; then
  tail -1 /tmp/wednesday_boot_digest.$$
else
  echo "⚠ boot_digest.py FAILED (rc=$?) — read the lesson files in full this boot:"; cat /tmp/wednesday_boot_digest.$$
fi
rm -f /tmp/wednesday_boot_digest.$$

if [ -x "$PROJECT_DIR/2_Project_Files/doctor.sh" ]; then
  if ! "$PROJECT_DIR/2_Project_Files/doctor.sh" --quiet; then
    echo ""
    echo "Preflight found HARD failures (above). Continue anyway? [y/N]"
    read -r -n 1 REPLY; echo
    [[ "$REPLY" =~ ^[Yy]$ ]] || exit 1
  fi
fi

# ── Arm the fleet wake watcher (2026-08-10, ledger w=5) ──
# Hand-arming died within a day, three times. The launcher is in the path of
# every session, so it arms; doctor.sh checks. Non-fatal on failure — the
# doctor hard-fail is the gate when agent panes are live.
if [ -x "$PROJECT_DIR/2_Project_Files/fleet/cockpit/arm_wake_watch.sh" ]; then
  "$PROJECT_DIR/2_Project_Files/fleet/cockpit/arm_wake_watch.sh" || \
    echo "WARNING: wake_watch failed to arm — report this in the session (no-skip)."
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
LABEL="[$AGENT_NAME]"
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
# ONE WEBSITE, served from the Studio (Kam, 2026-09-08 11:41: "can both agents read
# the same pane so that I'm interacting with one website rather than two"). Tuesday
# does NOT stand up a second dashboard: two servers would be two sites, and on the
# headless box nobody is looking at the second one. She writes her stream; Kam's
# panel renders it through the TUESDAY toggle. Override with WED_DASHBOARD=1 if a
# Tuesday seat ever genuinely needs its own (a lone laptop with no Studio).
if [ "$AGENT" = "tuesday" ] && [ "${WED_DASHBOARD:-0}" != "1" ]; then
  DASH_STATE="not started — one panel, served from the Wednesday seat"
elif curl -s -m 2 "$DASH_URL/api/health" 2>/dev/null | grep -q wednesday-dashboard; then
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
# NO LONGER OPENS THE BROWSER (Kam, 2026-09-08 14:05, verbatim): "There is no longer a need
# to bring up the dashboard page as I have this saved and can refresh myself." The SERVER is
# still started above — he refreshes his own saved tab; what stopped is this launcher stealing
# focus with a new one at every boot, several times a day across two agents.
# WED_OPEN_DASH=1 restores it for the one case that still needs it: a machine where the page
# has never been opened and he has no saved tab yet (Tuesday's, when it is built).
[ "${WED_OPEN_DASH:-0}" = "1" ] && open "$DASH_URL" 2>/dev/null; true

# ── Initial prompt ──
# ── PER-SEAT LEDGER SCOPE (Kam ruled `scope` on card `wed-boot-names-one-ledger-there-are-two`,
# panel 2026-09-08 09:57) ───────────────────────────────────────────────────────────────────
# Since his 2026-09-07 11:01 split there are TWO coordinator ledgers, and this prompt named
# only one. Measured at the 2026-09-08 laptop boot: `_ledger.md` 345,743 B (the Studio/Secuura
# seat's) vs `_ledger_laptop_datasec.md` 81,167 B / 36 rows (the laptop's own). A laptop seat
# obeying the old line read ~86K tokens of ANOTHER CLIENT'S corrections and never opened its
# own. `doctor.sh` already swept both by name (lines ~419-420) — the two mechanisms disagreed
# and the boot prompt was the one being obeyed.
# THE MAPPING IS HIS SPLIT AND HE CALLED IT TEMPORARY. It lives here, in one place. An
# unknown host falls back to `_ledger.md`, which is the pre-ruling behaviour — never a guess.
SEAT_HOST="$(hostname -s 2>/dev/null || hostname 2>/dev/null)"
case "$SEAT_HOST" in
  # Keyed on the AGENT now, not the host — a seat's corrections belong to the
  # agent, and Tuesday will move machines. The Datasec file keeps its historical
  # name (_ledger_laptop_datasec.md) on purpose: renaming it would orphan 86K of
  # that seat's own corrections and every link pointing at it.
  *) case "$AGENT" in
       tuesday) SEAT_LEDGER="_ledger_laptop_datasec.md"; OTHER_LEDGER="_ledger.md" ;;
       *)       SEAT_LEDGER="_ledger.md";                OTHER_LEDGER="_ledger_laptop_datasec.md" ;;
     esac ;;
esac

# ── CLIENT SCOPE, per agent (Kam, 2026-09-08 11:50 + 11:56) ────────────────────
# Wednesday: Secuura and everything general. Tuesday: every Datasec project,
# "as defined by living inside the Datasec folder" — his own words, and the
# reason the boundary is a PATH test rather than a judgement call.
if [ "$AGENT" = "tuesday" ]; then
  AGENT_SCOPE="YOUR CLIENT SCOPE: every DATASEC project — anything under
'/Volumes/DevMASTER/!CODING/Datasec/'. Secuura and general work belong to WEDNESDAY on
the Studio; you do not brief, launch, or answer for them. You are her sister seat, not a
different person: same persona, same voice, same W and M lessons, your own ledger, daily
notes, pickup, claims file and inbox. Cross-seat mail to her carries COORDINATION ONLY —
never Datasec code, findings, tickets or credentials. If a message needs client material
to make sense, it is not cross-seat mail.

🔴 ON YOUR VERY FIRST BOOT, before anything else, read
${BRAIN_DIR}/tasks/FIRST-BOOT-TUESDAY.md — it is who you are, what was built for you on
2026-09-08 so you do not re-derive it, and what is deliberately NOT done. Then read
${BRAIN_DIR}/tasks/NEXT-PICKUP-DATASEC-LAPTOP.md for the actual state of your projects.
Replace the first-boot brief with your own NEXT-PICKUP-TUESDAY.md at your first wrap; a
first-boot brief still being read on the tenth boot is a stale representation."
else
  AGENT_SCOPE="YOUR CLIENT SCOPE: SECUURA and all general/generic work. Every DATASEC
project belongs to TUESDAY (Kam ruled the name 2026-09-08 11:56); read Datasec mail by
SUBJECT only, and never brief or answer for a Datasec project. Cross-seat mail to her
carries COORDINATION ONLY — never Secuura code, findings, tickets or credentials."
fi

case "$AGENT" in
  tuesday) SELF_INBOX="tuesday-agent@agentmail.to" ;;
  *)       SELF_INBOX="wednesday-agent@agentmail.to" ;;
esac

INITIAL_PROMPT="ultrathink

You are ${AGENT_UPPER}, launched at '${PROJECT_DIR}'. DevMASTER workspace is ${DEVMASTER_STATE}.

${AGENT_SCOPE}

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
3. Read ${BRAIN_DIR}/learnings/_boot_digest_by_tier.md WHOLE (WED-145 Phase 0, Kam 2026-09-05 20:28: the by-tier digest — W whole, M rules-only, P cases as one-line handles; if it is missing, read _boot_digest.md instead) — it was GENERATED at this
   launch from every lesson file (headline = the retrieval handle, frontmatter,
   the operative paragraph, the section index, and every rules section verbatim;
   6 short files included whole) — then YOUR OWN SEAT'S LEDGER,
   ${BRAIN_DIR}/learnings/${SEAT_LEDGER}, WHOLE. (Kam ruled \"scope\" on 2026-09-08 09:57:
   each seat reads the ledger for ITS OWN scope. There are TWO since his 09-07 split —
   this seat's is ${SEAT_LEDGER}; the other coordinator's is ${OTHER_LEDGER}, which you read
   as ROW HEADLINES ONLY for cross-seat awareness, never whole. Reading the other seat's
   ledger whole is ~86K tokens of another client's corrections.) Do NOT read the individual lesson files at boot: open
   a lesson file the moment its rule FIRES, or when a diagnosis or a ledger row
   needs its cases — the digest names the file beside every headline. This is
   WED-139 (Kam 2026-09-02 20:47 \"go with a boot as you recommend\"): the full
   lesson load cost 34% of the window by statusline; report your statusline
   after the brain load in the boot note so the digest is measured, not assumed.
   _ledger_archive.md (rows dated 2026-08-29 and earlier, Kam's 2026-08-31 ruling
   + his 2026-09-02 \"we need to prune a little\") is read only on demand.
   The scoreboard (projects_index/scoreboard.md) is read HEAD-ONLY at boot (the
   newest ~15 rows), and INDEX.md's dated 'Refreshed' history only back to the
   newest two blocks. Two seats on 2026-09-01 booted at 51–57% ctx by reading
   all three whole — a seat that boots past 50% has ~20 minutes of useful life.
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
   **ANY COUNT you report from ANY board — yours or a project's — comes from
   2_Project_Files/fleet/board_count.sh, never from a hand-written query with a
   'first:'/'maxResults' you chose.** It refuses to print a total when the
   result equals its own limit or another page exists. Built at ledger w=5,
   2026-08-14, after I reported a row cap as a board total three times in one
   day (Secuura twelve-vs-fourteen, NexusAI 30-vs-46, and my own boot saying 60
   WED issues when there were 71). A cap quoted as a count is a silent
   truncation, and the two agents caught it before I did.
8. Agent Mail check (email is the FLEET'S inter-agent channel, Kam 2026-08-03):
   if AGENTMAIL_API_KEY is set in 4_Credentials/.env, list recent messages for
   BOTH ${SELF_INBOX} (this seat's OWN inbox — never the other agent's; the
   2026-08-13 cross-client capture is exactly that shape) AND the shared coagent@agentmail.to
   (legacy fleet bus — keep checking until every project's wrap flow targets
   the seat's own inbox) — GET https://api.agentmail.to/v0/inboxes/<inbox>/messages, 'Authorization:
   Bearer <key>'. ROUTE on subject: '[<Client>/<Project> -> Wednesday] Session
   wrap ...' = a project agent reporting in — read it, update INDEX.md +
   scoreboard, close any loop your own '[Wednesday -> ...]' email opened.
   Other mail: one line each, flag anything needing a reply or Kam.
   If unset/unreachable, say so in one line and continue.
9. Speak a short greeting via: 2_Project_Files/voice/speak.sh \"...\" — one or two
   sentences: hello + anything Kam should hear (carried-over items, blockers).
   Keep it warm, Irish, brief. Full detail goes in text.
10. MORNING TICKET SWEEP + AUTOSTART (Kam's standing grant, 2026-08-12 —
   learnings/2026-08-12_morning-ticket-sweep-autostart.md): in the MORNING
   session, sweep each active project's board read-only (Secuura/Blockchain ·
   Datasec/NexusAI · Datasec/Vision — SKIP myPKI, CypherKey, Lead_Bot for
   now) for outstanding agent-actionable tickets. If a project has any,
   launch its agent (cockpit.sh launch) and brief it to start — no
   per-morning Kam confirmation needed. Boundaries unchanged: v1.3 signature
   classes (prod, money, external comms, irreversible) still pause for Kam;
   briefs still go through send_brief.sh with provenance; sweep the board
   BEFORE briefing (2026-08-11 ledger). Check for client-human responses
   (e.g. Stuart on Secuura) as part of the sweep.
11. In text, confirm: brain loaded (learnings count), tasks carried over, project
   index freshness, DevMASTER state, Linear + mail status — then report what the
   sweep found + which agents were started, and propose today's remaining
   3-5 priorities (from Linear first) for anything OUTSIDE the standing grant;
   wait for Kam only on those.

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
  KAM'S RULINGS FIRST (2026-09-05, after the fourth raise of a subject he had
  ruled in hand): run 2_Project_Files/tools/kam_rulings_today.sh right after the
  brain load and at every checkpoint, and read EVERY line — his panel messages
  for the day, verbatim. A handover note summarises; his words on a card or in
  passing reach it as an episode, not a rule. No card, brief or ruling is written
  before this read. decision_queue.sh add now REFUSES a card whose subject he has
  already written on (--override-prior-rulings, with the reason in the BLUF).
  **STABLE CONVERSATION SURFACE (Kam, 2026-08-17 — learnings/2026-08-17_conversation-needs-a-stable-panel.md):**
  the chat tile is where Kam READS; the terminal buries conversation under
  fleet mechanics. MIRROR every substantive conversational reply to Kam via
  2_Project_Files/tools/chat_reply.sh — short form, pointers to documents for
  anything long (the 2026-08-17 HPSM sitting-pack PDF is the template; long
  content becomes a file, never scrollback-only). Fleet mechanics NEVER go
  into the chat mirror.
- Fleet comms: re-check the coagent@ inbox PERIODICALLY during long sessions —
  at natural checkpoints (a long task finishes, before proposing next steps),
  not just at boot. Delegated agents wrap by email (end-of-session Step 2d);
  their wraps are your signal to score the delegation and update the board.
- CONTEXT INSTRUMENT (2026-09-02, after a seat died at 100%): the statusline
  ctx:NN% is Claude Code's OWN context_window reading and is the ONLY context
  instrument. The <total_tokens> harness counter is a session token BUDGET, not
  the window — the 06:39 seat dismissed its 50% and 65% wakes as a \"statusline
  misparse\" on that counter and hit \"Prompt is too long\" at 09:49, unreachable
  for six hours with two agents idle. Read the pane statusline (tmux
  capture-pane) when a ctx wake lands; never argue with it. ROTATION BAND =
  80-90%, Kam 2026-09-07 10:49 verbatim: 'don't forget the Wednesday window is
  between 80 and 90% context. Use this as your rotation window.' This supersedes
  the 80-85 band (2026-09-05) and the bare 70% that stood in this line until
  2026-09-07 — that line was TWO rulings stale and is why seats kept rotating
  early. 70% is a CHECKPOINT only: refresh the handover block, start nothing
  heavy, do NOT rotate. Rotate at the first SAFE boundary inside 80-90, 90 the
  ceiling: finish the step, write + push the handover block, then run
  2_Project_Files/fleet/cockpit/wednesday_rotate.sh --self DETACHED (nohup, &).
  A dead seat is respawned by the watcher automatically (--dead); nothing on
  disk is lost, but everything not yet in the note is.
- Learning loop v2: corrections increment the frequency-weighted ledger
  (\${BRAIN_DIR}/learnings/${SEAT_LEDGER}) same-session; every wrap-up fills the
  daily-note retro; weekly consolidation + industry scan per \${BRAIN_DIR}/skills/
  (run in the first session after Sunday until the WED-16 scheduler exists).
- Wrap-up phrases ('good night', 'let's wrap', 'save to memory') trigger the
  session-end ritual in ./CLAUDE.md."

clear
cat <<EOF
==========================================
 Launching ${AGENT_UPPER}
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
tapped should have a wrap email in ${SELF_INBOX} — report any session that
did not wrap so Kam knows before he relaunches; (2) prepare the
day's briefing and speak the greeting as usual — if he doesn't answer, leave the
briefing on screen and wait quietly; do NOT start executing priorities without
his confirm. Quiet-hours rule stands: nothing spoken before 06:00."
fi

# Model (Kam, 2026-09-05 13:1x, verbatim: "you should load in latest fable model
# (now 5.1) unless credits are out in which case you should load in latest opus
# model"). PRIMARY = the `fable` ALIAS (tracks the newest Fable — 5.1 today — at
# every launch; a dated pin went stale the day 5.1 shipped, Kam 2026-09-02).
# FALLBACK = the `opus` alias via `--fallback-model`, which `claude --help`
# describes as "automatic fallback … when the default model is overloaded or not
# available". This replaces the hand-pin `--model opus` of 2026-09-04 21:15 (Fable
# credits out that evening) — a pin that silently kept every later seat on Opus
# after the credits came back.
#   EXERCISED 2026-09-05 13:2x before arming (exercise-mechanisms-before-arming):
#   - `claude --model fable -p '…'` answered FABLE-OK → Fable reachable, credits live.
#   - `claude --model <bogus> --fallback-model opus -p '…'` answered FALLBACK-OK on
#     Opus → the fallback leg FIRES when the primary is unavailable.
#   UNVERIFIED, stated honestly: whether a Fable CREDIT EXHAUSTION presents to the
#   CLI as "not available" and trips the same leg. It cannot be exercised without
#   spending the credits. The observation that settles it: a seat boots with Fable
#   credits believed live and its statusline reads Opus (or vice-versa: credits out
#   and the seat fails to start). Record either in the boot note the day it happens.
#   Manual override at any time: /model in the session, or edit the exec line.
# The boot block records the RESOLVED model from the pane statusline — the model
# can change between seats without a code change. (`fable[1m]` is the 1M-context
# variant if Kam ever wants that as the default — not chosen here.)
# Safety-classifier routing target (Kam, 2026-08-11). Claude Code reruns
# security-flagged turns on a higher-assurance Opus model — content-triggered,
# NOT an availability fallback, and unaffected by the --model pin below. Left
# unset it lands on Opus 4.8; Kam wants Opus 5. Verified before adopting:
# ANTHROPIC_DEFAULT_OPUS_MODEL appears 40x in the claude binary (strings on
# /Users/.../claude/versions/2.1.227), i.e. the CLI genuinely reads it — the
# documentation for this is third-party, so the binary is the source of truth.
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5

# WEEK-SCOPED OVERRIDE (Kam, 2026-09-06 20:2x, verbatim into Wednesday's own
# session: "please change your boot script for the rest of the week to boot in
# opus 5 rather than fable. we are burning through credits a little too
# quickly"). Every Wednesday seat boots on the `opus` ALIAS (newest Opus = Opus 5
# today; ANTHROPIC_DEFAULT_OPUS_MODEL above pins the classifier target the same
# way) until the week is out. "The week" is read as through Sunday 2026-09-13 —
# the 7-day usage window renews ~2026-09-13 (statusline "renews:6d 15h" at
# 20:14 on 09-06) — stated as an assumption to Kam; his one word moves it.
# REVERT = restore the line below (fable primary, opus fallback — the 09-05
# ruling, exercised then). doctor.sh WARNS from 2026-09-14 while this pin is
# live, so the override cannot outlive its week silently (the 09-04 hand-pin did
# exactly that; a promise is not a mechanism). Backup beside this file:
# Launch_Wednesday.command.pre-0906-opus.
# exec claude --dangerously-skip-permissions --model fable --fallback-model opus "$INITIAL_PROMPT"
exec claude --dangerously-skip-permissions --model opus "$INITIAL_PROMPT"
