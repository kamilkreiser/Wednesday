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
#     the id (product= ref= line= ctx= input= task= nocheck=1 out=). The first not-done line
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
NIGHT_THINK="${NIGHT_THINK:-0}"
NIGHT_NUM_CTX="${NIGHT_NUM_CTX:-32768}"
NIGHT_MAX_TICKETS="${NIGHT_MAX_TICKETS:-4}"
NIGHT_MAX_LOAD="${NIGHT_MAX_LOAD:-8}"
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
export OLLAMA_MODELS="${OLLAMA_MODELS:-$LM_DIR/models}"
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

log "START night_run model=$NIGHT_MODEL think=$NIGHT_THINK num_ctx=$NIGHT_NUM_CTX max=$NIGHT_MAX_TICKETS dry=$NIGHT_DRY_RUN queue=$NIGHT_QUEUE socket=${NIGHT_TMUX_SOCKET:-default}"

# ---------------------------------------------------------------- gates
GATE_FAIL=""
gates() {
  GATE_FAIL=""
  # G1 clock
  local hour
  if [ -n "$NIGHT_HOUR_OVERRIDE" ]; then hour="$((10#$NIGHT_HOUR_OVERRIDE))"; else hour="$((10#$(date +%H)))"; fi
  if [ "$hour" -ge 23 ] || [ "$hour" -lt 6 ]; then
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
  local tags
  tags="$(curl -sS -m 10 "$OLLAMA_URL/api/tags" 2>&1)"
  if [ $? -eq 0 ] && echo "$tags" | /usr/bin/grep -q "\"$NIGHT_MODEL\""; then
    log "GATE G5 ollama: $OLLAMA_URL/api/tags lists $NIGHT_MODEL — pass"
  else
    log "GATE G5 ollama: $OLLAMA_URL/api/tags rc=$? or $NIGHT_MODEL absent: $(echo "$tags" | head -c 200) — REFUSE"; GATE_FAIL="G5-ollama"; return 1
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
  FREE_GB="$3"
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
if ! gates; then finish 3 "gate refused: $GATE_FAIL"; fi
if [ -z "$(next_ticket)" ]; then log "QUEUE: $NIGHT_QUEUE has no pending ticket"; finish 4 "queue empty"; fi

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
  echo "== $(date '+%F %T') night_run $TICKET line='$LINE' model=$NIGHT_MODEL think=$NIGHT_THINK" >> "$RLOG"

  # build input (or take a pre-built one — the FIRE test uses a hand-made tiny input)
  INPUT="$RUN/input.json"
  PRE="$(pin "$LINE" input)"
  if [ -n "$PRE" ]; then
    cp "$PRE" "$INPUT"; echo "input: pre-built $PRE" >> "$RLOG"; log "TICKET $TICKET input pre-built: $PRE"
  else
    PINS=""; for kk in product ref line ctx; do v="$(pin "$LINE" $kk)"; [ -n "$v" ] && PINS="$PINS $kk=$v"; done
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
  NOCHECK="$(pin "$LINE" nocheck)"

  # memory
  if ! clear_memory; then
    echo "memory: $MEM_NOTE — skipped" >> "$RLOG"
    VERDICTS="$VERDICTS;$TICKET=SKIP_MEMORY"
    move_done "$LINE" "SKIP_MEMORY ($MEM_NOTE)" "$RUN"
    continue
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
    bash "$TASK_DIR/prepare_clone.sh" "$INPUT" "$CLONE" >> "$RLOG" 2>&1; prc=$?; echo "prepare_clone rc=$prc" >> "$RLOG"
    if [ "$prc" -ne 0 ]; then
      VERDICT="PREPARE_FAIL rc=$prc"
    else
      T2="$(date +%s)"
      bash "$TASK_DIR/checker.sh" "$INPUT" "$RUN/out.md" "$CLONE" > "$RUN/checker.out" 2>&1
      crc=$?
      echo "checker rc=$crc wall=$(( $(date +%s) - T2 ))s" >> "$RLOG"
      VERDICT="$(/usr/bin/grep -m1 '^RESULT:' "$RUN/checker.out" | head -c 120)"; VERDICT="${VERDICT:-CHECKER_NO_RESULT rc=$crc}"
      /usr/bin/grep -E '^(PASS|FAIL|SUMMARY|RESULT)' "$RUN/checker.out" >> "$RLOG"
    fi
    SRC_DIRTY_AFTER="$(git -C "$SRC" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
    echo "source checkout tracked-modified: before=$SRC_DIRTY_BEFORE after=$SRC_DIRTY_AFTER (must be equal)" >> "$RLOG"
    [ "$SRC_DIRTY_BEFORE" = "$SRC_DIRTY_AFTER" ] || log "WARNING $TICKET: source checkout modified count changed $SRC_DIRTY_BEFORE → $SRC_DIRTY_AFTER — read the run.log"
  fi
  log "TICKET $TICKET verdict: $VERDICT"
  VERDICTS="$VERDICTS;$TICKET=$(echo "$VERDICT" | tr ' ;' '_,')"
  python3 - "$RUN/night_meta.json" "$TICKET" "$NIGHT_MODEL" "$CTX" "$MEM_NOTE" "$VERDICT" "$((T1 - T0))" "$LINE" <<'PYEOF'
import json,sys,time; p,t,m,c,mem,v,w,line=sys.argv[1:9]
json.dump({"ticket":t,"queue_line":line,"model":m,"num_ctx":int(c),"memory_before":mem,"verdict":v,"model_wall_s":int(w),"when":time.strftime("%F %T")},open(p,"w"),indent=1)
PYEOF
  move_done "$LINE" "$VERDICT" "$RUN"
  echo "== $(date '+%F %T') end $TICKET verdict=$VERDICT" >> "$RLOG"

  # re-check the gates before the next ticket (a seat may have launched)
  if ! gates; then log "STOP after $TICKET: gate $GATE_FAIL failed (a seat may have launched)"; break; fi
done

# leave the memory clean for the morning
curl -sS -m 60 -X POST "$OLLAMA_URL/api/generate" -d "{\"model\":\"$NIGHT_MODEL\",\"keep_alive\":0}" > /dev/null 2>&1 && log "MEMORY: $NIGHT_MODEL unloaded at end"
if [ "$TICKETS_ATTEMPTED" -eq 0 ]; then finish 4 "queue empty"; fi
finish 0 "ran${GATE_FAIL:+; stopped by gate $GATE_FAIL}"
