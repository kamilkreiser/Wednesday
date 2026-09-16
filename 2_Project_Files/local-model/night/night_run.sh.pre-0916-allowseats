#!/bin/bash
# night_run.sh — Ornith (ornith:35b, drive-local Ollama) works the Secuura KS backlog
# AT NIGHT, in the downtime, only when no other agent runs. Kam, panel 2026-09-14
# 18:15:36: "lets use Ornith at night in the downtime (when no other agents run). clear
# system memory before it runs so that's not a problem. Set this up as a rule and get it
# working on the backlog. Prepare a list of tickets for it to work on."
# Rule: 0_Brain/learnings/2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md
#
# WHAT ONE RUN DOES
#   GATES  (each printed with its measurement; the first failure refuses, rc 3):
#     G1 clock inside 23:00–06:00 local        (NIGHT_HOUR_OVERRIDE=<0-23> for tests)
#     G2 fleet pane census: no live pane other than `wednesday` / `fleet-monitor`
#        (`tmux list-panes -t fleet -F '#{@cockpit_name}'`; NIGHT_TMUX_SOCKET=<name>
#        points tests at a scratch server; no fleet session at all = empty floor = pass;
#        an UNNAMED live pane counts as foreign)
#     G3 no QA gate / drafter process: `pgrep -f launch_qa_` = 0
#        (NIGHT_QA_PGREP=<pattern> is a TEST-ONLY override of the pattern — the FIRE test
#        needs it when another seat is launching gates on the same Mac; never set it in
#        the plist)
#     G4 1-min load < NIGHT_MAX_LOAD (8)
#     G5 Ollama answers /api/tags and lists the model
#   MEMORY (before EVERY ticket): unload every loaded model except ours
#     (`POST /api/generate {"model":m,"keep_alive":0}` for each /api/ps entry), then
#     measure `memory_pressure` + `vm_stat` and assert >= NIGHT_MIN_FREE_GB (30) available,
#     else skip the ticket with the reason. `sudo purge` is NOT attempted (needs admin —
#     see the rule's honest-limit line).
#   QUEUE  night/queue.md: one ticket per line, `# comments`, optional `k=v` pins after
#     the id (product= ref= line= ctx= test_file= input= task= nocheck=1 out=). The first not-done line
#     is taken; when its run ends the line MOVES to night/done.md with the verdict and the
#     run dir. At most NIGHT_MAX_TICKETS (4) model runs per night; gates re-checked after
#     each ticket (a seat may have launched) — stop on the first failure.
#   PER TICKET: build_input.sh → input.json (rc 2 = BUILD_REFUSED, line moved, next);
#     local_model_task.sh with LM_MODEL=$NIGHT_MODEL LM_THINK=$NIGHT_THINK
#     LM_NUM_CTX=$NIGHT_NUM_CTX (or the line's ctx=) → out.md; a `--shared --no-checkout`
#     clone at the pinned tip under NIGHT_SCRATCH (/private/tmp/claude-501/night/),
#     prepare_clone.sh, checker.sh → checker.out; everything into
#     runs/<date>_<ticket>-ornith-night/ (run.log, input.json, out.md + .meta.json +
#     .raw.json, checker.out, out.md.checker/, night_meta.json).
#   NEVER pushes, never writes Linear, never touches the source checkout (git READ verbs
#     only there; every write verb runs inside the scratch clone). A PASS becomes a PR only
#     through a Secuura seat in the morning; a FAIL is evidence.
#   NIGHT_DRY_RUN=1 does everything but the model call and the checker (verdict DRY_RUN).
#
# Exit codes: 0 ran (>= 1 ticket attempted; a mid-run gate stop is recorded, not an
# error) · 2 usage/environment · 3 gate refused before any ticket (the gate is named on
# stdout and in the log) · 4 queue empty.
# Logs: night/log/night_<date>.log (one line per decision) + night/log/last_run.json
# (what doctor.sh reads). bash 3.2, no `timeout`, no `cd` outside subshells, no `rm`
# (leftovers are quarantined by mv). stderr never discarded.
set -uo pipefail

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM_DIR="$(cd -P "$SELF_DIR/.." && pwd)"                 # 2_Project_Files/local-model
PF_DIR="$(cd -P "$LM_DIR/.." && pwd)"                   # 2_Project_Files
TASK_DIR="$LM_DIR/tasks/code_patch"

NIGHT_MODEL="${NIGHT_MODEL:-ornith:35b}"
NIGHT_THINK="${NIGHT_THINK:-0}"   # 2026-09-15 10:4x: think=0 again — WITH a Wednesday brief the brief is the reasoning (KS-1087 round 3 produced the correct fix at think=0); think=1 + brief over-thought into the context wall twice (47K and 78K chars). Set NIGHT_THINK=1 only for a ticket with no brief.
NIGHT_NUM_CTX="${NIGHT_NUM_CTX:-32768}"
NIGHT_MAX_TICKETS="${NIGHT_MAX_TICKETS:-4}"
# 2026-09-15 20:2x: macOS mediaanalysisd (560% CPU, days) keeps the 1-min load ~9 with NO seat live; G2 (the pane census)
# is the seat gate, G4 only protects the checker from a busy box — 14 lets the loop run under that daemon.
NIGHT_MAX_LOAD="${NIGHT_MAX_LOAD:-14}"
NIGHT_MIN_FREE_GB="${NIGHT_MIN_FREE_GB:-30}"
NIGHT_QUEUE="${NIGHT_QUEUE:-$SELF_DIR/queue.md}"
NIGHT_DONE="${NIGHT_DONE:-$(dirname "$NIGHT_QUEUE")/done.md}"
NIGHT_RUNS_DIR="${NIGHT_RUNS_DIR:-$LM_DIR/runs}"
NIGHT_LOG_DIR="${NIGHT_LOG_DIR:-$SELF_DIR/log}"
NIGHT_SCRATCH="${NIGHT_SCRATCH:-/private/tmp/claude-501/night}"
NIGHT_DRY_RUN="${NIGHT_DRY_RUN:-0}"
NIGHT_TMUX_SOCKET="${NIGHT_TMUX_SOCKET:-}"
NIGHT_HOUR_OVERRIDE="${NIGHT_HOUR_OVERRIDE:-}"
NIGHT_QA_PGREP="${NIGHT_QA_PGREP:-launch_qa_}"
OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
# 2026-09-16 13:5x — PINNED, not defaulted. Kam is moving his personal 141 GB ollama store to
# /Volumes/DevMASTER/SYSTEM/ollama and a global OLLAMA_MODELS is about to exist. With the old
# `${OLLAMA_MODELS:-...}` form this runner would INHERIT it and look for ornith:35b in Kam's
# personal store, where it is not — G5 would refuse forever, and now self-heal into the wrong
# store. A global env var is a floating pointer (2026-08-05_identities-float-verify-always);
# the fleet's model path is a property of this tree, so it is set here unconditionally.
# NIGHT_OLLAMA_MODELS is the deliberate override, named so it cannot be set by accident.
export OLLAMA_MODELS="${NIGHT_OLLAMA_MODELS:-$LM_DIR/models}"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"   # launchd hands a minimal env
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
export NIGHT_SOURCE_CHECKOUT="$SRC"

mkdir -p "$NIGHT_LOG_DIR" "$NIGHT_SCRATCH" "$NIGHT_RUNS_DIR"
DATE="$(date +%F)"
LOG="$NIGHT_LOG_DIR/night_$DATE.log"
STATE="$NIGHT_LOG_DIR/last_run.json"
RUN_START="$(date '+%F %T')"
log() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
tmuxc() { if [ -n "$NIGHT_TMUX_SOCKET" ]; then "$TMUX_BIN" -L "$NIGHT_TMUX_SOCKET" "$@"; else "$TMUX_BIN" "$@"; fi; }

TICKETS_RUN=0; TICKETS_ATTEMPTED=0; VERDICTS=""
write_state() {
  # write_state <exit> <reason>
  python3 - "$STATE" "$1" "$2" "$RUN_START" "$TICKETS_ATTEMPTED" "$TICKETS_RUN" "$VERDICTS" "$NIGHT_MODEL" "$NIGHT_DRY_RUN" <<'PYEOF'
import json, sys, time
p, rc, reason, start, att, ran, verdicts, model, dry = sys.argv[1:10]
json.dump({"exit": int(rc), "reason": reason, "started": start, "ended": time.strftime("%Y-%m-%d %H:%M:%S"),
           "tickets_attempted": int(att), "tickets_run": int(ran), "verdicts": [v for v in verdicts.split(";") if v],
           "model": model, "dry_run": dry == "1"}, open(p, "w"), indent=1)
PYEOF
}
finish() { write_state "$1" "$2"; log "END rc=$1 $2 (attempted=$TICKETS_ATTEMPTED run=$TICKETS_RUN)"; exit "$1"; }

# RUN LOCK (2026-09-15): with Kam's 24/7 ruling the runner is also fired every 15 min by
# com.wednesday.ornith-loop; two runs must never overlap (one model, one queue). mkdir is the
# portable atomic lock; a stale lock (owner pid dead) is taken over, and the lock is released
# on every exit path. A refused start is logged, quietly, at rc 0 — the loop is not an error.
LOCKDIR="$NIGHT_LOG_DIR/.night_run.lock"
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  OWNER="$(cat "$LOCKDIR/pid" 2>/dev/null || echo)"
  if [ -n "$OWNER" ] && kill -0 "$OWNER" 2>/dev/null; then
    echo "$(date '+%F %T') LOCK: another night_run is live (pid $OWNER) — this start exits 0" | tee -a "$LOG"; exit 0
  fi
  echo "$(date '+%F %T') LOCK: stale lock (owner ${OWNER:-unknown} dead) — taking it over" | tee -a "$LOG"
fi
echo $$ > "$LOCKDIR/pid"
trap 'rmdir "$LOCKDIR" 2>/dev/null || { rm -f "$LOCKDIR/pid" 2>/dev/null; rmdir "$LOCKDIR" 2>/dev/null; }' EXIT
log "START night_run model=$NIGHT_MODEL think=$NIGHT_THINK num_ctx=$NIGHT_NUM_CTX max=$NIGHT_MAX_TICKETS dry=$NIGHT_DRY_RUN queue=$NIGHT_QUEUE socket=${NIGHT_TMUX_SOCKET:-default}"

# ---------------------------------------------------------------- gates
GATE_FAIL=""
gates() {
  GATE_FAIL=""
  # G1 clock
  local hour
  if [ -n "$NIGHT_HOUR_OVERRIDE" ]; then hour="$((10#$NIGHT_HOUR_OVERRIDE))"; else hour="$((10#$(date +%H)))"; fi
  # Kam, panel 2026-09-14 21:57:43 (verbatim): "no need to gate it to the nighttime, as this machine is
  # only used by you. And if you're not pulling up any agents, then you can do the work 24/7." — so the
  # clock is INFORMATIONAL and G2 (the pane census) is the gate. NIGHT_CLOCK_GATE=1 restores the window.
  if [ "${NIGHT_CLOCK_GATE:-0}" != "1" ]; then
    log "GATE G1 clock: hour=$hour — informational only (Kam 2026-09-14 21:57: 24/7 when no other agents run; NIGHT_CLOCK_GATE=1 restores 23:00-06:00) — pass"
  elif [ "$hour" -ge 23 ] || [ "$hour" -lt 6 ]; then
    log "GATE G1 clock: hour=$hour inside 23:00-06:00${NIGHT_HOUR_OVERRIDE:+ (OVERRIDE)} — pass"
  else
    log "GATE G1 clock: hour=$hour outside 23:00-06:00${NIGHT_HOUR_OVERRIDE:+ (OVERRIDE)} — REFUSE"; GATE_FAIL="G1-clock"; return 1
  fi
  # G2 pane census
  local census foreign n
  if tmuxc has-session -t fleet 2>/dev/null; then
    census="$(tmuxc list-panes -s -t fleet -F '#{@cockpit_name}|#{pane_dead}' 2>/dev/null)"
    foreign="$(echo "$census" | awk -F'|' '$2!="1" && $1!="wednesday" && $1!="fleet-monitor" {print ($1==""?"<unnamed>":$1)}' | tr '\n' ' ')"
    n="$(echo "$census" | /usr/bin/grep -c . )"
    if [ -z "$foreign" ]; then
      log "GATE G2 panes: $n live pane(s) [$(echo "$census" | cut -d'|' -f1 | tr '\n' ' ')] none foreign — pass"
    else
      log "GATE G2 panes: foreign live pane(s): $foreign — REFUSE (other agents run)"; GATE_FAIL="G2-panes"; return 1
    fi
  else
    log "GATE G2 panes: no 'fleet' tmux session on ${NIGHT_TMUX_SOCKET:-default} socket — empty floor — pass"
  fi
  # G3 QA gate / drafter processes
  local nqa nclaude
  nqa="$(pgrep -f "$NIGHT_QA_PGREP" | wc -l | tr -d ' ')"
  nclaude="$(pgrep -x claude | wc -l | tr -d ' ')"
  local qanote=""; [ "$NIGHT_QA_PGREP" != "launch_qa_" ] && qanote=" (TEST OVERRIDE pattern)"
  if [ "$nqa" -eq 0 ]; then
    log "GATE G3 qa-procs: pgrep -f $NIGHT_QA_PGREP = 0$qanote (claude processes: $nclaude, informational) — pass"
  else
    log "GATE G3 qa-procs: pgrep -f $NIGHT_QA_PGREP = $nqa$qanote — REFUSE"; GATE_FAIL="G3-qa-procs"; return 1
  fi
  # G4 load
  local load1
  load1="$(sysctl -n vm.loadavg | awk '{gsub(/[{}]/,""); print $1}')"
  if python3 -c "import sys; sys.exit(0 if float('$load1') < float('$NIGHT_MAX_LOAD') else 1)"; then
    log "GATE G4 load: 1-min $load1 < $NIGHT_MAX_LOAD — pass"
  else
    log "GATE G4 load: 1-min $load1 >= $NIGHT_MAX_LOAD — REFUSE"; GATE_FAIL="G4-load"; return 1
  fi
  # G5 ollama
  #
  # SELF-HEAL, added 2026-09-16 13:4x: on 2026-09-16 the server died before 12:24 and this gate
  # refused SIX consecutive cycles (12:24 -> 13:24) into this log, which nobody reads — Ornith sat
  # idle 09:58 -> 13:32 on the day Kam twice said never to idle. A dead LOCAL server is not a safety
  # boundary, so detecting it and refusing was the wrong response: removing the failure mode beats
  # detecting it (2026-09-08_a-false-absence-is-usually-my-own-instrument rule 9). start_ollama.sh is
  # idempotent, uses the drive-local binary + OLLAMA_MODELS, and REFUSES (rc 3) rather than fighting a
  # server already holding the port — so a foreign listener still reaches the refusal below, which is
  # the case that genuinely needs a human.
  local tags rc
  tags="$(curl -sS -m 10 "$OLLAMA_URL/api/tags" 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ] && echo "$tags" | /usr/bin/grep -q "\"$NIGHT_MODEL\""; then
    log "GATE G5 ollama: $OLLAMA_URL/api/tags lists $NIGHT_MODEL — pass"
  elif [ "${NIGHT_G5_SELFHEAL:-1}" = "1" ] && [ -f "$SELF_DIR/../start_ollama.sh" ] \
       && NIGHT_MODEL="$NIGHT_MODEL" OLLAMA_URL="$OLLAMA_URL" bash "$SELF_DIR/../start_ollama.sh" >> "$LOG" 2>&1; then
    log "GATE G5 ollama: was down — start_ollama.sh brought it back serving $NIGHT_MODEL — pass (SELF-HEALED)"
  else
    log "GATE G5 ollama: curl rc=$rc or $NIGHT_MODEL absent, and the self-heal did not recover it: $(echo "$tags" | head -c 200) — REFUSE"; GATE_FAIL="G5-ollama"; return 1
  fi
  return 0
}

# ---------------------------------------------------------------- memory
FREE_GB=""; MEM_NOTE=""
clear_memory() {
  # unload every loaded model except ours, then measure
  local ps loaded m
  ps="$(curl -sS -m 10 "$OLLAMA_URL/api/ps" 2>/dev/null)"
  loaded="$(echo "$ps" | python3 -c 'import json,sys
try:
    for x in json.load(sys.stdin).get("models",[]): print(x["name"], round(x.get("size",0)/2**30,1))
except Exception as e: pass')"
  if [ -z "$loaded" ]; then log "MEMORY: /api/ps lists no loaded model"; fi
  echo "$loaded" | while read -r m sz; do
    [ -z "$m" ] && continue
    if [ "$m" = "$NIGHT_MODEL" ]; then log "MEMORY: $m (${sz} GB) is ours — kept"; continue; fi
    local r; r="$(curl -sS -m 60 -X POST "$OLLAMA_URL/api/generate" -d "{\"model\":\"$m\",\"keep_alive\":0}" 2>&1 | head -c 200)"
    log "MEMORY: unloaded $m (${sz} GB) keep_alive=0 → $r"
  done
  sleep 2
  local mp
  mp="$(memory_pressure 2>/dev/null | /usr/bin/grep -o 'free percentage: [0-9]*%' | /usr/bin/grep -o '[0-9]*')"
  FREE_GB="$(vm_stat | python3 -c '
import re,sys
t=sys.stdin.read(); ps=int(re.search(r"page size of (\d+)",t).group(1))
def g(k):
    m=re.search(k+r":\s+(\d+)",t); return int(m.group(1)) if m else 0
free=g("Pages free"); spec=g("Pages speculative"); inact=g("Pages inactive")
print(f"{(free+spec)*ps/2**30:.1f} {inact*ps/2**30:.1f} {(free+spec+inact)*ps/2**30:.1f}")')"
  set -- $FREE_GB
  MEM_NOTE="memory_pressure free=${mp:-?}% · vm_stat free+speculative=${1} GB, inactive(reclaimable)=${2} GB, available=${3} GB"
  # 2026-09-15 11:0x: the vm_stat sum (free+speculative+inactive) UNDERCOUNTS on macOS after a model unloads —
  # q8 round 8 read 27.8 GB by vm_stat while memory_pressure said 55% free of 96 GB (~53 GB); the kernel's own
  # figure is the instrument, vm_stat stays in the note. available = free% x hw.memsize (falls back to vm_stat
  # only when memory_pressure printed nothing).
  RAM_GB="$(sysctl -n hw.memsize 2>/dev/null | awk '{printf "%.1f", $1/1073741824}')"
  if [ -n "${mp:-}" ] && [ -n "$RAM_GB" ]; then
    FREE_GB="$(python3 -c "print(f'{float('$mp')/100*float('$RAM_GB'):.1f}')")"
    MEM_NOTE="$MEM_NOTE · available by memory_pressure = ${FREE_GB} GB (${mp}% of ${RAM_GB} GB) — the gate's figure"
  else
    FREE_GB="$3"
  fi
  log "MEMORY: $MEM_NOTE · sudo purge NOT attempted (needs admin; sudoers line if Kam wants it: \`$(id -un) ALL=(root) NOPASSWD: /usr/sbin/purge\`)"
  if python3 -c "import sys; sys.exit(0 if float('$FREE_GB') >= float('$NIGHT_MIN_FREE_GB') else 1)"; then
    log "MEMORY: available $FREE_GB GB >= $NIGHT_MIN_FREE_GB GB — ok"; return 0
  fi
  log "MEMORY: available $FREE_GB GB < $NIGHT_MIN_FREE_GB GB — skip"; return 1
}

# ---------------------------------------------------------------- queue
next_ticket() {
  # prints the first non-comment, non-empty line of the queue (or nothing)
  [ -f "$NIGHT_QUEUE" ] || return 0
  /usr/bin/grep -v -E '^[[:space:]]*(#|$)' "$NIGHT_QUEUE" | head -1
}
move_done() {
  # move_done <queue line> <verdict> <run dir>  — the line leaves queue.md and lands in done.md
  python3 - "$NIGHT_QUEUE" "$NIGHT_DONE" "$1" "$2" "$3" <<'PYEOF'
import sys, time, os
q, d, line, verdict, run = sys.argv[1:6]
lines = open(q, encoding="utf-8").read().split("\n")
try:
    i = lines.index(line)
except ValueError:
    sys.stderr.write("move_done: queue line not found verbatim; appended to done.md anyway\n"); i = None
if i is not None:
    del lines[i]
    open(q, "w", encoding="utf-8").write("\n".join(lines))
hdr = not os.path.exists(d) or os.path.getsize(d) == 0
with open(d, "a", encoding="utf-8") as f:
    if hdr:
        f.write("# night/done.md — queue lines moved here by night_run.sh (newest at the bottom)\n# <queue line> | done <when> | verdict <verdict> | run <dir>\n")
    f.write(f"{line} | done {time.strftime('%Y-%m-%d %H:%M')} | verdict {verdict} | run {run}\n")
PYEOF
  log "QUEUE: moved '$1' → done.md (verdict $2)"
}
pin() { # pin <line> <key>  → value or ""
  echo "$1" | tr ' ' '\n' | /usr/bin/grep "^$2=" | head -1 | cut -d= -f2-
}

# ---------------------------------------------------------------- run
#
# G8 (2026-09-16 13:4x) — A REFUSAL NOBODY READS IS INDISTINGUISHABLE FROM WORKING.
# G7 alerts when the QUEUE is empty. Nothing alerted when a GATE refused, so six G5 refusals in an
# hour reached no surface a human or a seat lands on, and the only reason anyone noticed was a boot.
# So: the first refusal of a gate stamps a marker; once the SAME gate has been refusing for
# NIGHT_GATE_ALERT_MIN minutes (default 30), ONE panel line goes out, rate-limited exactly like G7,
# and the markers are cleared the moment the gates pass. The alert DEGRADES rather than blocks — a
# failed post is logged and the refusal still happens (2026-09-10_a-refusal-nobody-reads...).
_gate_marker="$NIGHT_LOG_DIR/.gate_refused_since"; _gate_alerted="$NIGHT_LOG_DIR/.gate_refused_alerted"
# Clearing a marker is a MOVE, never a delete (Kam 2026-08-26; G7 above does the same with its own
# two markers) — the quarantined copies are the record of how long each outage actually ran.
_gate_clear() {
  mkdir -p "$NIGHT_LOG_DIR/_quarantine_g8" 2>/dev/null
  for _m in "$_gate_marker" "$_gate_alerted"; do
    [ -f "$_m" ] && mv "$_m" "$NIGHT_LOG_DIR/_quarantine_g8/$(basename "$_m").$(date +%s)"
  done
  :
}
if ! gates; then
  _now="$(date +%s)"
  if [ -f "$_gate_marker" ] && [ "$(cut -d' ' -f2- "$_gate_marker" 2>/dev/null)" = "$GATE_FAIL" ]; then
    _since="$(cut -d' ' -f1 "$_gate_marker" 2>/dev/null)"
  else
    _gate_clear; _since="$_now"; printf '%s %s\n' "$_now" "$GATE_FAIL" > "$_gate_marker"
  fi
  _mins=$(( (_now - ${_since:-$_now}) / 60 ))
  if [ "$_mins" -ge "${NIGHT_GATE_ALERT_MIN:-30}" ] && [ ! -f "$_gate_alerted" ]; then
    : > "$_gate_alerted"
    _remedy="read night/log/$(basename "$LOG") for the refusal line"
    [ "$GATE_FAIL" = "G5-ollama" ] && _remedy="bash 2_Project_Files/local-model/start_ollama.sh (the self-heal already failed — something else holds port 11434)"
    log "G8 GATE ALERT: $GATE_FAIL has refused for ${_mins} min — posting to the panel"
    [ "${NIGHT_GATE_ALERT_DRY:-0}" = 1 ] || bash "$SELF_DIR/../../tools/chat_reply.sh" \
      "Ornith has been gate-refused for ${_mins} minutes on ${GATE_FAIL} — nothing has run since it started. Remedy: ${_remedy}." > /dev/null 2>&1 || log "G8 GATE ALERT: post FAILED"
  fi
  finish 3 "gate refused: $GATE_FAIL"
fi
_gate_clear
if [ -z "$(next_ticket)" ]; then
  log "QUEUE: $NIGHT_QUEUE has no pending ticket"
  # (b) of the 2026-09-16 unattended-week design: an empty DEFAULT queue re-derives the candidate pool when
  # night/candidates.md is older than NIGHT_DERIVE_H hours (default 6) — a ticket closed/archived/taken during the
  # day must drop out and a new one must appear without a seat. Read-only board query under the 2026-08-03 grant
  # (the Secuura .env is sourced transiently for the query, never copied); the file's own header says what it read.
  if [ "$NIGHT_QUEUE" = "$SELF_DIR/queue.md" ] && [ -f "$SELF_DIR/derive_candidates.py" ]; then
    _cand="$SELF_DIR/candidates.md"; _age_h="${NIGHT_DERIVE_H:-6}"; _env="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
    if [ ! -f "$_cand" ] || [ "$(( ( $(date +%s) - $(stat -f %m "$_cand") ) / 3600 ))" -ge "$_age_h" ]; then
      if [ "${NIGHT_DERIVE_DRY:-0}" = 1 ]; then log "DERIVE: candidates.md older than ${_age_h}h — would re-derive (DRY)"
      elif [ -f "$_env" ]; then
        log "DERIVE: candidates.md older than ${_age_h}h — re-deriving from the board (read-only)"
        ( set -a; . "$_env"; set +a; python3 "$SELF_DIR/derive_candidates.py" ) > "$SELF_DIR/log/derive_$(date +%F_%H%M).out" 2>&1 && log "DERIVE: ok — $(tail -1 "$SELF_DIR/log/derive_$(date +%F_%H%M).out" | cut -c1-160)" || log "DERIVE: FAILED — see $SELF_DIR/log/derive_$(date +%F_%H%M).out"
      else log "DERIVE: candidates.md older than ${_age_h}h but the Secuura .env is not at $_env — not re-derived"; fi
    fi
  fi
  # G7 (2026-09-16, unattended-week design piece d): an EMPTY queue during 06-23 is the never-idle failure
  # (Kam 2026-09-15 18:19) and nothing woke anyone for it. Record when the drought began; after
  # NIGHT_IDLE_ALERT_H hours (default 2) post ONE panel line, then at most one more per NIGHT_IDLE_ALERT_H.
  # Only the DEFAULT queue counts (a split queue going empty is normal). A non-empty run resets the marker.
  if [ "$NIGHT_QUEUE" = "$SELF_DIR/queue.md" ]; then
    _idle_marker="$SELF_DIR/log/.queue_empty_since"; _idle_alert="$SELF_DIR/log/.queue_empty_alerted"
    _now=$(date +%s); _hour=$(date +%H | sed 's/^0//'); _alert_h="${NIGHT_IDLE_ALERT_H:-2}"
    [ -f "$_idle_marker" ] || echo "$_now" > "$_idle_marker"
    _since=$(cat "$_idle_marker" 2>/dev/null || echo "$_now"); _last=$(cat "$_idle_alert" 2>/dev/null || echo 0)
    if [ "$_hour" -ge 6 ] && [ "$_hour" -lt 23 ] && [ $((_now - _since)) -ge $((_alert_h * 3600)) ] && [ $((_now - _last)) -ge $((_alert_h * 3600)) ]; then
      _since_hm=$(date -r "$_since" +%H:%M 2>/dev/null || echo "?")
      log "G7 IDLE ALERT: queue empty since $_since_hm — posting to the panel"
      echo "$_now" > "$_idle_alert"
      [ "${NIGHT_IDLE_ALERT_DRY:-0}" = 1 ] || bash "$SELF_DIR/../../tools/chat_reply.sh" "Ornith has had nothing queued since $_since_hm — the coordinator owes it a brief or a reason (never-idle, 2026-09-15 18:19)." > /dev/null 2>&1 || log "G7 IDLE ALERT: post FAILED"
    fi
  fi
  finish 4 "queue empty"
fi

ITER=0
while [ "$TICKETS_RUN" -lt "$NIGHT_MAX_TICKETS" ] && [ "$ITER" -lt $((NIGHT_MAX_TICKETS + 8)) ]; do
  ITER=$((ITER + 1))
  LINE="$(next_ticket)"
  [ -z "$LINE" ] && { log "QUEUE: empty — nothing more to take"; break; }
  TICKET="$(echo "$LINE" | awk '{print $1}')"
  TICKETS_ATTEMPTED=$((TICKETS_ATTEMPTED + 1))
  RUN="$NIGHT_RUNS_DIR/${DATE}_$(echo "$TICKET" | tr 'A-Z' 'a-z' | tr -d '-')-$(echo "$NIGHT_MODEL" | tr -d ':')-night"
  k=1; while [ -d "$RUN" ]; do k=$((k+1)); RUN="${RUN%-night*}-night$k"; done
  mkdir -p "$RUN"
  RLOG="$RUN/run.log"
  log "TICKET $TICKET take: '$LINE' → $RUN"
  # G7: a taken ticket ends the drought — clear the empty-queue markers (default queue only).
  [ "$NIGHT_QUEUE" = "$SELF_DIR/queue.md" ] && { mkdir -p "$SELF_DIR/log/_quarantine_g7" 2>/dev/null; for _m in "$SELF_DIR/log/.queue_empty_since" "$SELF_DIR/log/.queue_empty_alerted"; do [ -f "$_m" ] && mv "$_m" "$SELF_DIR/log/_quarantine_g7/$(basename "$_m").$(date +%s)"; done; :; }
  echo "== $(date '+%F %T') night_run $TICKET line='$LINE' model=$NIGHT_MODEL think=$NIGHT_THINK" >> "$RLOG"

  # build input (or take a pre-built one — the FIRE test uses a hand-made tiny input)
  INPUT="$RUN/input.json"
  PRE="$(pin "$LINE" input)"
  if [ -n "$PRE" ]; then
    cp "$PRE" "$INPUT"; echo "input: pre-built $PRE" >> "$RLOG"; log "TICKET $TICKET input pre-built: $PRE"
  else
    # 2026-09-15 18:5x: test_file= forwarded (KS-1172 — a widened pin needs the EXISTING test file in the input;
    # the allow-list silently dropped it on the first relaunch, files stayed 2, the model invented context again).
    PINS=""; for kk in product ref line ctx test_file tool test_dir vitest_config; do v="$(pin "$LINE" $kk)"; [ -n "$v" ] && PINS="$PINS $kk=$v"; done
    bash "$SELF_DIR/build_input.sh" "$TICKET" "$INPUT" $PINS > "$RUN/build_input.out" 2>&1
    brc=$?
    cat "$RUN/build_input.out" >> "$RLOG"
    if [ "$brc" -ne 0 ]; then
      REASON="$(/usr/bin/grep -m1 'REFUSED\|build_input:' "$RUN/build_input.out" | head -c 300)"
      log "TICKET $TICKET build_input rc=$brc — $REASON"
      VERDICTS="$VERDICTS;$TICKET=BUILD_REFUSED"
      move_done "$LINE" "BUILD_REFUSED rc=$brc ($REASON)" "$RUN"
      continue
    fi
    log "TICKET $TICKET input built: $(tail -1 "$RUN/build_input.out" | head -c 200)"
  fi
  CTX="$(pin "$LINE" ctx)"; CTX="${CTX:-$(python3 -c "import json;print(json.load(open('$INPUT')).get('_night_num_ctx',$NIGHT_NUM_CTX))")}"
  TASK="$(pin "$LINE" task)"; TASK="${TASK:-$TASK_DIR/task.md}"
  # 2026-09-15 20:0x (Kam 19:55 "see how the local agents perform on the docs"): a pinned task= selects its own
  # task TYPE — prepare_clone.sh (if the type has one) and checker.sh come from the task's directory.
  TDIR="$(cd "$(dirname "$TASK")" && pwd)"
  NOCHECK="$(pin "$LINE" nocheck)"

  # memory — 2026-09-15 10:55 (q8 round 7): right after a 37 GB model unloads, vm_stat still shows ~3 GB
  # free + ~3 GB inactive for a minute while the kernel reclaims; one read skipped two of three tickets.
  # So: up to 4 reads, 30 s apart, before a skip — and a memory skip goes BACK TO THE QUEUE (the front),
  # never to done.md as a verdict: it is a timing fact about the machine, not a result about the ticket.
  MEM_TRY=0; MEM_OK=0
  while [ "$MEM_TRY" -lt 4 ]; do
    if clear_memory; then MEM_OK=1; break; fi
    MEM_TRY=$((MEM_TRY + 1)); log "MEMORY: not yet reclaimed (try $MEM_TRY/4) — waiting 30 s"; sleep 30
  done
  if [ "$MEM_OK" -ne 1 ]; then
    echo "memory: $MEM_NOTE — skipped after 4 reads; line returned to the queue" >> "$RLOG"
    VERDICTS="$VERDICTS;$TICKET=SKIP_MEMORY"
    log "SKIP_MEMORY $TICKET after 4 reads ($MEM_NOTE) — the line STAYS in the queue (next_ticket only reads; move_done is what removes), the runner stops here"
    break
  fi
  echo "memory: $MEM_NOTE" >> "$RLOG"

  if [ "$NIGHT_DRY_RUN" = "1" ]; then
    log "TICKET $TICKET DRY_RUN — model call and checker skipped (would run: LM_MODEL=$NIGHT_MODEL LM_THINK=$NIGHT_THINK LM_NUM_CTX=$CTX task=$TASK)"
    echo "DRY_RUN: no model call, no checker" >> "$RLOG"
    VERDICTS="$VERDICTS;$TICKET=DRY_RUN"
    TICKETS_RUN=$((TICKETS_RUN + 1))
    move_done "$LINE" "DRY_RUN" "$RUN"
    python3 - "$RUN/night_meta.json" "$TICKET" "$NIGHT_MODEL" "$CTX" "$MEM_NOTE" "DRY_RUN" <<'PYEOF'
import json,sys,time; p,t,m,c,mem,v=sys.argv[1:7]
json.dump({"ticket":t,"model":m,"num_ctx":int(c),"memory":mem,"verdict":v,"when":time.strftime("%F %T")},open(p,"w"),indent=1)
PYEOF
    if ! gates; then log "STOP after $TICKET: gate $GATE_FAIL failed (a seat may have launched)"; finish 0 "ran; stopped by gate $GATE_FAIL"; fi
    continue
  fi

  # model (or a pre-made answer via out= — TEST ONLY, to drive the checker path without a model call)
  T0="$(date +%s)"
  PREOUT="$(pin "$LINE" out)"
  if [ -n "$PREOUT" ]; then
    cp "$PREOUT" "$RUN/out.md"; hrc=$?; echo "out.md: PRE-MADE from $PREOUT (test only, no model call)" >> "$RLOG"
    log "TICKET $TICKET out.md pre-made (TEST): $PREOUT"
  else
    LM_MODEL="$NIGHT_MODEL" LM_THINK="$NIGHT_THINK" LM_NUM_CTX="$CTX" LM_MAX_LOAD="$NIGHT_MAX_LOAD" OLLAMA_URL="$OLLAMA_URL" \
      bash "$LM_DIR/local_model_task.sh" "$TASK" "$INPUT" "$RUN/out.md" >> "$RLOG" 2>&1
    hrc=$?
  fi
  T1="$(date +%s)"
  echo "harness rc=$hrc wall=$((T1 - T0))s" >> "$RLOG"
  TICKETS_RUN=$((TICKETS_RUN + 1))
  if [ "$hrc" -ne 0 ]; then
    log "TICKET $TICKET harness rc=$hrc after $((T1 - T0))s — $(tail -1 "$RLOG" | head -c 200)"
    VERDICTS="$VERDICTS;$TICKET=HARNESS_FAIL"
    move_done "$LINE" "HARNESS_FAIL rc=$hrc" "$RUN"
    if ! gates; then log "STOP after $TICKET: gate $GATE_FAIL failed"; finish 0 "ran; stopped by gate $GATE_FAIL"; fi
    continue
  fi
  log "TICKET $TICKET model done in $((T1 - T0))s: $(/usr/bin/grep -m1 'lm_call: ok' "$RLOG" | head -c 220)"

  # checker in a --shared clone at the pinned tip (night scratch only)
  VERDICT="HARNESS_ONLY"
  if [ "$NOCHECK" != "1" ]; then
    TIP="$(python3 -c "import json;print(json.load(open('$INPUT'))['tip'])")"
    CLONE="$NIGHT_SCRATCH/clone_$(echo "$TICKET" | tr 'A-Z' 'a-z' | tr -d '-')"
    if [ -d "$CLONE/.git" ]; then
      HAVE="$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)"
      if [ "$HAVE" != "$TIP" ]; then
        Q="$NIGHT_SCRATCH/quarantine/$(date +%Y%m%d-%H%M%S)_$(basename "$CLONE")"; mkdir -p "$(dirname "$Q")"
        mv "$CLONE" "$Q"; echo "clone at $HAVE != tip $TIP — quarantined to $Q" >> "$RLOG"
      fi
    fi
    if [ ! -d "$CLONE/.git" ]; then
      git clone --shared --no-checkout "$SRC" "$CLONE" >> "$RLOG" 2>&1; echo "clone rc=$?" >> "$RLOG"
      git -C "$CLONE" checkout --detach "$TIP" >> "$RLOG" 2>&1; echo "checkout rc=$?" >> "$RLOG"
    fi
    SRC_DIRTY_BEFORE="$(git -C "$SRC" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
    if [ -f "$TDIR/prepare_clone.sh" ]; then bash "$TDIR/prepare_clone.sh" "$INPUT" "$CLONE" >> "$RLOG" 2>&1; prc=$?; else prc=0; echo "prepare_clone: none for $TDIR (doc task)" >> "$RLOG"; fi; echo "prepare_clone rc=$prc" >> "$RLOG"
    if [ "$prc" -ne 0 ]; then
      VERDICT="PREPARE_FAIL rc=$prc"
    else
      T2="$(date +%s)"
      bash "$TDIR/checker.sh" "$INPUT" "$RUN/out.md" "$CLONE" > "$RUN/checker.out" 2>&1
      crc=$?
      echo "checker rc=$crc wall=$(( $(date +%s) - T2 ))s" >> "$RLOG"
      VERDICT="$(/usr/bin/grep -m1 '^RESULT:' "$RUN/checker.out" | head -c 120)"; VERDICT="${VERDICT:-CHECKER_NO_RESULT rc=$crc}"
      /usr/bin/grep -E '^(PASS|FAIL|SUMMARY|RESULT)' "$RUN/checker.out" >> "$RLOG"
    fi
    SRC_DIRTY_AFTER="$(git -C "$SRC" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
    echo "source checkout tracked-modified: before=$SRC_DIRTY_BEFORE after=$SRC_DIRTY_AFTER (must be equal)" >> "$RLOG"
    [ "$SRC_DIRTY_BEFORE" = "$SRC_DIRTY_AFTER" ] || log "WARNING $TICKET: source checkout modified count changed $SRC_DIRTY_BEFORE → $SRC_DIRTY_AFTER — read the run.log"
  fi
  # ---------------------------------------------------------------- RETRY-ONCE (2026-09-15 15:5x)
  # A3b PARTIAL (a named site left untouched — four times on audit.ts it was the NEIGHBOUR that changed) and
  # A2b PLACEHOLDER (a one-line test file) are SAMPLE failures, not model verdicts: the same brief on a fresh
  # sample with the checker's own words in front of the model is the cheapest next step (row 33 of
  # IMPROVEMENTS.md). One retry, same model, input + `retry_feedback` (verdict, missed sites from the A3b
  # line, an instruction); the retry's out.md/checker.out live under $RUN/retry/; the FIRST attempt's files
  # are untouched. NIGHT_RETRY_ON_PARTIAL=0 disables. The done.md row carries both verdicts.
  # 2026-09-16 13:5x — TWO fixes on this one line, both found by KS-1011 r1 failing with no retry:
  #  (1) the trigger listed only the VITEST tier's stop points (A3b/A2b/A3d/A3c). The BASH tier's
  #      repairable stops are B3b (a context line marked '+' — the same A3d dialect, different gate)
  #      and B3c (a "stays" line marked '-'), and neither was here, so the bash tier had no retry at
  #      all. A trigger keyed on one tier's NAMES is a census over the wrong frame.
  #  (2) `A && B && C || D` binds so that D is evaluated whenever the left side is false — so the
  #      checker.out grep could fire a retry even with NIGHT_RETRY_ON_PARTIAL=0. Grouped so the
  #      disable flag actually disables.
  if [ "${NIGHT_RETRY_ON_PARTIAL:-1}" = "1" ] && [ -z "${RETRY_DONE:-}" ] && \
     { echo "$VERDICT" | /usr/bin/grep -q -i -E 'stopped at A3b|stopped at A2b|A2b PLACEHOLDER|stopped at A3d|stopped at A3c|stopped at B3b|stopped at B3c' || \
       /usr/bin/grep -q -i 'FAIL A4 RED-FIRST: the test file did not run any test' "$RUN/checker.out"; }; then
    RETRY_DONE=1; FIRST_VERDICT="$VERDICT"
    mkdir -p "$RUN/retry"
    python3 - "$INPUT" "$RUN/checker.out" "$RUN/retry/input.json" <<'PYR'
import json, re, sys
inp, chk, out = sys.argv[1:4]
d = json.load(open(inp, encoding="utf-8")); c = open(chk, encoding="utf-8").read()
m = re.search(r"^(FAIL A3b PARTIAL FIX.*|FAIL A2b PLACEHOLDER.*|FAIL A3d CONTEXT MARKED AS ADDITION.*|FAIL A4 RED-FIRST: the test file did not run any test.*)$", c, re.M)
verdict = m.group(1).strip() if m else "the checker refused the first attempt (see verdict)"
# 2026-09-15 18:3x: a LOAD/COMPILE error (ts-jest TS6133, a vitest idiom under jest, a missing import) carries the
# compiler's own lines so the retry can act on them — the first 25 error lines of red_first.out, ANSI stripped.
if "did not run any test" in verdict:
    import os
    rf = os.path.join(os.path.dirname(chk), "out.md.checker", "red_first.out")
    if os.path.exists(rf):
        txt = re.sub(r"\x1b\[[0-9;]*m", "", open(rf, encoding="utf-8", errors="replace").read())
        errs = [l.rstrip() for l in txt.split("\n") if re.search(r"error TS\d+|Cannot find|is not defined|SyntaxError|ReferenceError|TypeError", l)]
        verdict = verdict[:300] + " | COMPILER/LOADER SAID: " + " ⏎ ".join(errs[:25])[:1500]
missed = []
for ln in re.findall(r":(\d+) `", verdict):
    for s_ in d.get("defect_line", {}).get("sites", []):
        if str(s_.get("line")) == ln:
            missed.append({"line": s_["line"], "text_at_tip": s_.get("text_at_tip", s_.get("text", ""))})
# 2026-09-15 23:5x (KS-1133 A r2): the retry FIXED the product hunk and replaced its attempt-1 test file (54 lines, 5
# cells, A2b clean) with a 2-line stub patch to the REFERENCE file — the feedback said "emit the COMPLETE diff again" and
# nothing told the model its test was already right. When attempt 1's TEST section was accepted (A2b did not fire and
# the section carries an it()/test() cell), it travels into the retry VERBATIM with the instruction to reproduce it.
keep_test = ""
try:
    import os as _os
    _sj = _os.path.join(_os.path.dirname(chk), "out.md.checker", "sections.json")
    if "A2b PLACEHOLDER" not in c and _os.path.exists(_sj):
        for _o in json.load(open(_sj, encoding="utf-8")):
            if "__tests__" in _o.get("path", "") and _os.path.exists(_o.get("file", "")):
                _t = open(_o["file"], encoding="utf-8", errors="replace").read()
                if re.search(r"^\+\s*(it|test)\(", _t, re.M) and len(_t) <= 24000:
                    keep_test = _t
                break
except Exception as _e:  # never let the feedback builder kill the retry — the retry runs without the section
    print(f"retry input: keep_test skipped ({_e})")
d["retry_feedback"] = {
    "attempt": 2,
    "verdict": verdict[:600],
    "missed_sites": missed,
    "accepted_test_section": keep_test,
    "instruction": ("Your first diff was REFUSED: " + verdict[:600] + ". Emit the COMPLETE diff again. If the verdict carries COMPILER/LOADER lines, fix exactly what they name (remove an unused declaration/import, add a missing import, replace a vitest idiom with the jest one) and change nothing else. For every "
        "missed site the `-` line is `text_at_tip` copied character for character (do NOT edit the comment or the "
        "line beside it); keep the test exactly as specified. If the verdict names a PLACEHOLDER test file, write "
        "the full test file this time. If the verdict names CONTEXT MARKED AS ADDITION, the lines it lists ALREADY EXIST in the file: "
        "emit them with a leading SPACE as context (or leave them out), never as `+` — the ONLY `+` lines in the product hunk are the "
        "new lines the task spells out; an insert-only edit adds exactly those lines and removes nothing. "
        "If `accepted_test_section` is non-empty, your attempt-1 TEST FILE section was ACCEPTED: reproduce that section "
        "BYTE FOR BYTE as the test file part of your diff (same path, same `--- /dev/null` header, every cell) and change "
        "ONLY the product section as the verdict says — never replace the test with a stub or a patch to the reference file."),
}
json.dump(d, open(out, "w", encoding="utf-8"), indent=1)
print(f"retry input: {len(missed)} missed site(s) carried; verdict={verdict[:120]!r}")
PYR
    log "TICKET $TICKET RETRY-ONCE on '$FIRST_VERDICT' — $(tail -1 "$RLOG" 2>/dev/null | head -c 0)same model, input + retry_feedback → $RUN/retry/"
    TR0="$(date +%s)"
    LM_MODEL="$NIGHT_MODEL" LM_THINK="$NIGHT_THINK" LM_NUM_CTX="$CTX" LM_MAX_LOAD="$NIGHT_MAX_LOAD" OLLAMA_URL="$OLLAMA_URL" \
      bash "$LM_DIR/local_model_task.sh" "$TASK" "$RUN/retry/input.json" "$RUN/retry/out.md" >> "$RLOG" 2>&1
    rrc=$?; TR1="$(date +%s)"
    echo "retry harness rc=$rrc wall=$((TR1 - TR0))s" >> "$RLOG"
    if [ "$rrc" -eq 0 ]; then
      [ -f "$TDIR/prepare_clone.sh" ] && bash "$TDIR/prepare_clone.sh" "$INPUT" "$CLONE" >> "$RLOG" 2>&1
      bash "$TDIR/checker.sh" "$RUN/retry/input.json" "$RUN/retry/out.md" "$CLONE" > "$RUN/retry/checker.out" 2>&1
      RV="$(/usr/bin/grep -m1 '^RESULT:' "$RUN/retry/checker.out" | head -c 120)"; RV="${RV:-CHECKER_NO_RESULT}"
      /usr/bin/grep -E '^(PASS|FAIL|SUMMARY|RESULT)' "$RUN/retry/checker.out" | sed 's/^/retry: /' >> "$RLOG"
      VERDICT="$RV — RETRY of [$FIRST_VERDICT] (retry/out.md, $((TR1 - TR0))s)"
      log "TICKET $TICKET retry verdict: $RV (first: $FIRST_VERDICT)"
    else
      log "TICKET $TICKET retry harness rc=$rrc — first verdict stands"
      VERDICT="$FIRST_VERDICT — retry harness rc=$rrc"
    fi
  fi
  RETRY_DONE=""
  log "TICKET $TICKET verdict: $VERDICT"
  VERDICTS="$VERDICTS;$TICKET=$(echo "$VERDICT" | tr ' ;' '_,')"
  python3 - "$RUN/night_meta.json" "$TICKET" "$NIGHT_MODEL" "$CTX" "$MEM_NOTE" "$VERDICT" "$((T1 - T0))" "$LINE" <<'PYEOF'
import json,sys,time; p,t,m,c,mem,v,w,line=sys.argv[1:9]
json.dump({"ticket":t,"queue_line":line,"model":m,"num_ctx":int(c),"memory_before":mem,"verdict":v,"model_wall_s":int(w),"when":time.strftime("%F %T")},open(p,"w"),indent=1)
PYEOF
  move_done "$LINE" "$VERDICT" "$RUN"
  echo "== $(date '+%F %T') end $TICKET verdict=$VERDICT" >> "$RLOG"

  # re-check the gates before the next ticket (a seat may have launched).
  # 2026-09-15: the checker's OWN vitest/tsc leaves the 1-min load above 8 for a minute or two after a
  # ticket (rounds 3 and 4 both STOPPED at G4 on their own load, not on a seat). So: settle 60 s first,
  # and the between-ticket G4 bar is NIGHT_MAX_LOAD_BETWEEN (12) — G2 (the pane census) is still the
  # gate that detects a launched seat, and it is re-checked here unchanged.
  log "settle 60 s before the between-ticket gate re-check (the checker's own load)"; sleep 60
  NIGHT_MAX_LOAD="${NIGHT_MAX_LOAD_BETWEEN:-14}"
  if ! gates; then log "STOP after $TICKET: gate $GATE_FAIL failed (a seat may have launched)"; break; fi
done

# leave the memory clean for the morning
curl -sS -m 60 -X POST "$OLLAMA_URL/api/generate" -d "{\"model\":\"$NIGHT_MODEL\",\"keep_alive\":0}" > /dev/null 2>&1 && log "MEMORY: $NIGHT_MODEL unloaded at end"
if [ "$TICKETS_ATTEMPTED" -eq 0 ]; then finish 4 "queue empty"; fi
finish 0 "ran${GATE_FAIL:+; stopped by gate $GATE_FAIL}"
