#!/bin/bash
# omlx_serve.sh — start | stop | status | clear-trip the oMLX server that serves Ornith 1.5 to the night runner.
#
# Why (Kam, 2026-10-08 18:12, verbatim): "go with Ornith 1.5 and deploy it. use this instead of the old model.
# Keep pushing it and see how far it can go." The A/B that preceded it (0_Brain/reference/2026-10-08_omlx-flash-next/
# ORNITH15_AB.md) served Ornith-1.5-35B-A3B-MLX-8bit from a gitignored scratch run dir; this script is that recipe made
# TRACKED and self-locating, so night/night_run.sh can depend on it.
#
# WHAT IT SERVES (and only that):
#   - port 47780 on 127.0.0.1 (Wednesday's reserved block, 2_Project_Files/PORTS.md), never another port;
#   - its OWN --base-path (omlx/state/base/), rendered at each start from the tracked omlx/settings.template.json —
#     tools/omlx/base (the Flash test's settings) is never read or written;
#   - a model_dir (omlx/state/models/) holding ONE symlink, to tools/omlx/models/Ornith-1.5-35B-A3B-MLX-8bit,
#     so the 104 GB Flash model beside it is NOT discoverable;
#   - memory tier `balanced` (the template is refused if it says anything else), max context 65536 (via
#     sampling.max_context_window_policy — max_context_window alone does not cap it; refused if not 65536),
#     max_concurrent_requests 1, SSD KV cache under omlx/state/cache (10 GB cap). All of omlx/state/ is gitignored.
#
# THE GUARD (from the A/B's guard.sh): while the server runs, a detached loop samples every 2 s and KILLS the server
# when swap used grows more than OMLX_GUARD_SWAP_MB (256) above the baseline taken at start, or when memory_pressure's
# free percentage drops below OMLX_GUARD_MIN_FREE (10). A trip writes omlx/state/GUARD_TRIPPED; `start` then REFUSES
# until a human runs `clear-trip` (otherwise the night runner's auto-start would re-load into the same pressure, over
# and over). `stop` writes omlx/state/GUARD_STOP; the guard consumes it (moves it to GUARD_STOP.last) and exits.
# The guard also exits on its own when the server pid is gone.
#
# Usage: omlx_serve.sh start [--no-load] | stop | status | clear-trip
#   start   idempotent. Already listening on 47780 with OUR pid -> rc 0 (re-arms a missing guard, loads the model
#           unless --no-load). Refuses (rc 3) if: a guard trip is recorded; something ELSE holds 47780; available memory
#           < OMLX_MIN_FREE_GB_TO_LOAD (40 = the model's ~35 GB + margin); the model folder / venv is missing (rc 2).
#           Then POSTs /v1/models/<id>/load (blocks until loaded) so the first night ticket does not pay the load.
#   stop    SIGINT to our pid (oMLX shuts down cleanly on it), SIGTERM after 20 s, stops the guard. rc 0.
#   status  prints listening / pid / loaded / guard / memory. rc 0 = listening AND model loaded,
#           1 = listening but model not loaded, 2 = not listening.
#   clear-trip  moves GUARD_TRIPPED to GUARD_TRIPPED.last (a human decision; never automatic).
#
# Env: OMLX_PORT (47780 — anything else refuses), OMLX_MODEL (Ornith-1.5-35B-A3B-MLX-8bit = the model id AND the symlink
#      name), OMLX_MODEL_SRC (the model folder; default tools/omlx/models/$OMLX_MODEL — point it at another MLX model for
#      another test; render() then quarantines the previous symlink so model_dir still holds exactly one model; raise
#      OMLX_MIN_FREE_GB_TO_LOAD to that model's size + margin),
#      OMLX_MIN_FREE_GB_TO_LOAD (40), OMLX_GUARD_SWAP_MB (256), OMLX_GUARD_MIN_FREE (10).
# Side effect outside the drive, recorded in PORTABILITY.md: oMLX publishes ~/.omlx/bin/omlx-cluster-python
# (a 4-line sh shim that execs the drive venv's python) at start.
# bash 3.2; no `cd`; no `rm`; stderr never discarded.
set -uo pipefail

LM_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # 2_Project_Files/local-model
PF_DIR="$(cd -P "$LM_DIR/.." && pwd)"                          # 2_Project_Files
OMLX_TOOL="$PF_DIR/tools/omlx"
VENV_BIN="$OMLX_TOOL/venv/bin"
OMLX_MODEL="${OMLX_MODEL:-Ornith-1.5-35B-A3B-MLX-8bit}"
MODEL_SRC="${OMLX_MODEL_SRC:-$OMLX_TOOL/models/$OMLX_MODEL}"   # GENERIC (2026-10-08 18:3x, Wednesday: the Qwen3.5-122B test reuses this script) — any one MLX model folder
TEMPLATE="$LM_DIR/omlx/settings.template.json"
STATE="$LM_DIR/omlx/state"
BASE="$STATE/base"; MODELS="$STATE/models"; CACHE="$STATE/cache"; LOGS="$STATE/logs"
PIDF="$STATE/omlx.pid"; GPIDF="$STATE/guard.pid"
TRIP="$STATE/GUARD_TRIPPED"; GSTOP="$STATE/GUARD_STOP"
PORT="${OMLX_PORT:-47780}"
URL="http://127.0.0.1:$PORT"
MIN_LOAD_GB="${OMLX_MIN_FREE_GB_TO_LOAD:-40}"
GUARD_SWAP_MB="${OMLX_GUARD_SWAP_MB:-256}"
GUARD_MIN_FREE="${OMLX_GUARD_MIN_FREE:-10}"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

[ "$PORT" = "47780" ] || { echo "omlx_serve: REFUSED — port $PORT is not Wednesday's oMLX port 47780 (PORTS.md)" >&2; exit 2; }
mkdir -p "$STATE" "$LOGS"
say() { echo "$(date '+%F %T') omlx_serve: $*" | tee -a "$LOGS/omlx_serve.log"; }

listener_pid() { lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -1; }
our_pid() { local p; p="$(cat "$PIDF" 2>/dev/null)"; [ -n "$p" ] && kill -0 "$p" 2>/dev/null && echo "$p"; }
guard_pid() { local p; p="$(cat "$GPIDF" 2>/dev/null)"; [ -n "$p" ] && kill -0 "$p" 2>/dev/null && ps -p "$p" -o command= 2>/dev/null | /usr/bin/grep -q "omlx_serve.sh _guard" && echo "$p"; }
swap_mb() { sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/'; }
free_pct() { memory_pressure 2>/dev/null | sed -n 's/.*free percentage: \([0-9]*\)%.*/\1/p'; }
avail_gb() { local p r; p="$(free_pct)"; r="$(sysctl -n hw.memsize)"; python3 -c "print(f'{float(\"${p:-0}\")/100*$r/2**30:.1f}')"; }
loaded_json() { curl -sS -m 10 "$URL/v1/models/status" 2>&1; }
is_loaded() {
  loaded_json | python3 -c '
import json,sys
try: d=json.load(sys.stdin)
except Exception: sys.exit(2)
m=[x for x in d.get("models",[]) if x.get("id")==sys.argv[1]]
sys.exit(0 if m and m[0].get("loaded") else 1)' "$OMLX_MODEL"
}
mem_line() {
  local vs; vs="$(vm_stat | awk '/page size of/ {ps=$8} /Pages free/ {gsub(/\./,"",$3); f=$3} /Pages wired down/ {gsub(/\./,"",$4); w=$4} END {printf "%d pages (%.1f GiB), wired %.1f GiB", f, f*ps/1073741824, w*ps/1073741824}')"
  echo "vm_stat free=$vs · swap used=$(swap_mb)M · memory_pressure free=$(free_pct)% · load=$(sysctl -n vm.loadavg | tr -d '{}' | awk '{print $1}')"
}

render() {
  [ -f "$TEMPLATE" ] || { echo "omlx_serve: REFUSED — settings template missing: $TEMPLATE" >&2; return 2; }
  mkdir -p "$BASE" "$MODELS" "$CACHE"
  # the model_dir holds exactly ONE entry: the 1.5 symlink. Anything else there is quarantined (moved), never deleted.
  local e
  for e in "$MODELS"/* "$MODELS"/.[!.]*; do
    [ -e "$e" ] || [ -L "$e" ] || continue
    [ "$(basename "$e")" = "$OMLX_MODEL" ] && [ "$(readlink "$e")" = "$MODEL_SRC" ] && continue
    mkdir -p "$STATE/_quarantine"; mv "$e" "$STATE/_quarantine/$(basename "$e").$(date +%s)"
    say "quarantined unexpected model_dir entry $(basename "$e")"
  done
  [ -L "$MODELS/$OMLX_MODEL" ] || ln -s "$MODEL_SRC" "$MODELS/$OMLX_MODEL"
  python3 - "$TEMPLATE" "$BASE/settings.json" "$MODELS" "$CACHE" "$PORT" <<'PYEOF' || return 2
import json, os, sys
t, out, mdir, cdir, port = sys.argv[1:6]
d = json.load(open(t))
d.pop("_comment", None)
if d.get("memory", {}).get("memory_guard_tier") != "balanced":
    sys.stderr.write(f"omlx_serve: REFUSED — template memory_guard_tier={d.get('memory',{}).get('memory_guard_tier')!r}, must be 'balanced'\n"); sys.exit(2)
if d.get("sampling", {}).get("max_context_window_policy") != 65536:
    sys.stderr.write("omlx_serve: REFUSED — template sampling.max_context_window_policy must be 65536 (the field that caps context in oMLX 0.7.0)\n"); sys.exit(2)
if d["server"].get("host") != "127.0.0.1" or str(d["server"].get("port")) != port:
    sys.stderr.write("omlx_serve: REFUSED — template server host/port is not 127.0.0.1:47780\n"); sys.exit(2)
d["model"]["model_dirs"] = [mdir]; d["model"]["model_dir"] = mdir
d["cache"]["ssd_cache_dir"] = cdir
# keep a secret_key oMLX itself generated into an earlier rendered copy (never tracked); else null
if os.path.exists(out):
    try:
        old = json.load(open(out)).get("auth", {}).get("secret_key")
        if old: d["auth"]["secret_key"] = old
    except Exception:
        pass
json.dump(d, open(out, "w"), indent=2)
os.chmod(out, 0o600)
PYEOF
}

guard_loop() { # _guard <baseline swap MB> <server pid>
  local base="$1" spid="$2" n=0 maxswap=0 minfree=100 sw sw_i fr grow
  echo $$ > "$GPIDF"
  echo "$(date '+%F %T') guard start pid=$$ server=$spid baseline_swap_used=${base}M limit=+${GUARD_SWAP_MB}M min_free=${GUARD_MIN_FREE}%" >> "$LOGS/guard.log"
  while :; do
    if [ -f "$GSTOP" ]; then
      mv "$GSTOP" "$GSTOP.last"
      echo "$(date '+%F %T') guard stop requested (max_swap=${maxswap}M min_free=${minfree}%)" >> "$LOGS/guard.log"; exit 0
    fi
    if ! kill -0 "$spid" 2>/dev/null; then
      echo "$(date '+%F %T') guard exit: server pid $spid gone (max_swap=${maxswap}M min_free=${minfree}%)" >> "$LOGS/guard.log"; exit 0
    fi
    sw="$(swap_mb)"; fr="$(free_pct)"; sw_i="${sw%.*}"; fr="${fr:-100}"
    [ "$sw_i" -gt "$maxswap" ] && maxswap="$sw_i"
    [ "$fr" -lt "$minfree" ] && minfree="$fr"
    grow=$(( sw_i - ${base%.*} ))
    if [ "$grow" -gt "$GUARD_SWAP_MB" ] || [ "$fr" -lt "$GUARD_MIN_FREE" ]; then
      echo "$(date '+%F %T') TRIP swap_used=${sw}M (grow ${grow}M) free=${fr}% — killing omlx pid=$spid" >> "$LOGS/guard.log"
      kill -INT "$spid" 2>/dev/null; sleep 5; kill -0 "$spid" 2>/dev/null && kill -9 "$spid" 2>/dev/null
      echo "$(date '+%F %T') TRIP swap_used=${sw}M grow=${grow}M free=${fr}% killed pid=$spid" > "$TRIP"
      echo "$(date '+%F %T') guard exit after trip (max_swap=${maxswap}M min_free=${minfree}%)" >> "$LOGS/guard.log"
      exit 1
    fi
    n=$((n + 1))
    [ $((n % 150)) -eq 0 ] && echo "$(date '+%F %T') ok swap_used=${sw}M grow=${grow}M free=${fr}% (max_swap=${maxswap}M min_free=${minfree}%)" >> "$LOGS/guard.log"
    sleep 2
  done
}

arm_guard() { # arm_guard <server pid>
  local g; g="$(guard_pid)"
  if [ -n "$g" ]; then say "guard already armed (pid $g)"; return 0; fi
  [ -f "$GSTOP" ] && mv "$GSTOP" "$GSTOP.last"
  nohup bash "$LM_DIR/omlx_serve.sh" _guard "$(swap_mb)" "$1" >> "$LOGS/guard.log" 2>&1 &
  sleep 1
  g="$(guard_pid)"; [ -n "$g" ] && say "guard armed (pid $g, baseline swap $(swap_mb)M, trips at +${GUARD_SWAP_MB}M or free < ${GUARD_MIN_FREE}%)" \
    || { say "FAILED to arm the guard — stopping the server rather than serve unguarded"; do_stop; return 3; }
}

load_model() {
  local t0 r; t0="$(date +%s)"
  r="$(curl -sS -m 600 -X POST "$URL/v1/models/$OMLX_MODEL/load" 2>&1)"
  if is_loaded; then say "model $OMLX_MODEL loaded in $(( $(date +%s) - t0 ))s ($(echo "$r" | head -c 160))"; return 0; fi
  say "model load FAILED after $(( $(date +%s) - t0 ))s: $(echo "$r" | head -c 300)"; return 4
}

do_stop() {
  local p; p="$(our_pid)"
  : > "$GSTOP"
  if [ -z "$p" ]; then
    local lp; lp="$(listener_pid)"
    [ -n "$lp" ] && { say "stop: 47780 is held by pid $lp which is NOT ours ($PIDF) — not touching it"; return 3; }
    say "stop: no server of ours running"; return 0
  fi
  kill -INT "$p" 2>/dev/null
  local i=0; while kill -0 "$p" 2>/dev/null && [ "$i" -lt 20 ]; do sleep 1; i=$((i + 1)); done
  if kill -0 "$p" 2>/dev/null; then kill -TERM "$p" 2>/dev/null; sleep 3; say "stop: SIGINT did not finish in 20 s — SIGTERM sent"; fi
  kill -0 "$p" 2>/dev/null && { say "stop: pid $p STILL alive"; return 4; }
  say "stopped pid $p ($(mem_line))"
  return 0
}

do_start() {
  local noload="${1:-}"
  [ -f "$TRIP" ] && { echo "omlx_serve: REFUSED — the memory guard TRIPPED: $(cat "$TRIP"). Read $LOGS/guard.log, then 'omlx_serve.sh clear-trip' (a human decision)." >&2; return 3; }
  [ -x "$VENV_BIN/omlx" ] || { echo "omlx_serve: REFUSED — oMLX venv missing: $VENV_BIN/omlx (PORTABILITY: oMLX night backend)" >&2; return 2; }
  [ -f "$MODEL_SRC/config.json" ] || { echo "omlx_serve: REFUSED — model folder missing or incomplete: $MODEL_SRC" >&2; return 2; }
  local p lp; p="$(our_pid)"; lp="$(listener_pid)"
  if [ -n "$lp" ] && [ "$lp" != "$p" ]; then
    echo "omlx_serve: REFUSED — 127.0.0.1:$PORT is held by pid $lp, not ours ($(ps -p "$lp" -o command= 2>/dev/null | head -c 160)). Not touching it." >&2; return 3
  fi
  if [ -n "$p" ] && [ -n "$lp" ]; then
    say "already running (pid $p, listening on $PORT)"
    arm_guard "$p" || return $?
    [ "$noload" = "--no-load" ] || is_loaded || load_model || return $?
    return 0
  fi
  local av; av="$(avail_gb)"
  if ! python3 -c "import sys; sys.exit(0 if float('$av') >= float('$MIN_LOAD_GB') else 1)"; then
    echo "omlx_serve: REFUSED — available memory ${av} GB < ${MIN_LOAD_GB} GB needed to load $OMLX_MODEL (~35 GB) with margin ($(mem_line))" >&2; return 3
  fi
  render || return 2
  say "starting oMLX on $URL (base $BASE, model_dir $MODELS, before: $(mem_line))"
  nohup "$VENV_BIN/omlx" serve --base-path "$BASE" --model-dir "$MODELS" --host 127.0.0.1 --port "$PORT" \
    --memory-guard balanced --max-concurrent-requests 1 \
    --paged-ssd-cache-dir "$CACHE" --paged-ssd-cache-max-size 10GB >> "$LOGS/serve.out" 2>&1 &
  p=$!; echo "$p" > "$PIDF"
  local i=0
  while [ "$i" -lt 60 ]; do
    kill -0 "$p" 2>/dev/null || { say "server pid $p DIED during start — tail of $LOGS/serve.out:"; tail -20 "$LOGS/serve.out" >&2; return 4; }
    curl -sS -m 3 "$URL/health" > /dev/null 2>&1 && break
    sleep 2; i=$((i + 1))
  done
  curl -sS -m 3 "$URL/health" > /dev/null 2>&1 || { say "server did not answer /health within 120 s — stopping it"; do_stop; return 4; }
  say "listening (pid $p) after $((i * 2))s"
  arm_guard "$p" || return $?
  [ "$noload" = "--no-load" ] && return 0
  load_model || return $?
  say "ready ($(mem_line))"
}

do_status() {
  local p lp g; p="$(our_pid)"; lp="$(listener_pid)"; g="$(guard_pid)"
  if [ -z "$lp" ]; then
    echo "oMLX: NOT LISTENING on $URL (pid file: ${p:-none alive}; guard: $( [ -n "$g" ] && echo "pid $g" || echo "not running" ))$( [ -f "$TRIP" ] && echo " · GUARD TRIPPED: $(cat "$TRIP")")"
    echo "memory: $(mem_line)"; return 2
  fi
  local owner="ours"; [ "$lp" = "$p" ] || owner="NOT OURS (pid file says ${p:-none})"
  local ld="not loaded"; is_loaded && ld="LOADED"
  local rss; rss="$(ps -p "$lp" -o rss= 2>/dev/null | awk '{printf "%.1f GiB", $1/1048576}')"
  echo "oMLX: LISTENING on $URL · pid $lp ($owner, rss $rss) · $OMLX_MODEL $ld · guard: $( [ -n "$g" ] && echo "armed pid $g" || echo "NOT RUNNING" )$( [ -f "$TRIP" ] && echo " · GUARD TRIPPED: $(cat "$TRIP")")"
  echo "memory: $(mem_line)"
  [ "$ld" = "LOADED" ] && return 0 || return 1
}

case "${1:-}" in
  start) do_start "${2:-}"; exit $? ;;
  stop) do_stop; exit $? ;;
  status) do_status; exit $? ;;
  clear-trip) if [ -f "$TRIP" ]; then mv "$TRIP" "$TRIP.last"; say "guard trip cleared by hand (was: $(cat "$TRIP.last"))"; else echo "no guard trip recorded"; fi ;;
  _guard) guard_loop "$2" "$3" ;;
  *) echo "usage: omlx_serve.sh start [--no-load] | stop | status | clear-trip" >&2; exit 2 ;;
esac
