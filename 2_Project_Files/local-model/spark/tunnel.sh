#!/bin/bash
# tunnel.sh — check, or re-open, the Studio's LOCAL ssh forward to the Spark (127.0.0.1:47788 -> Spark:8888).
#
# WHY (2026-10-16, Wednesday): the forward died silently on two mornings running (10-15, 10-16). Nothing
# re-opened it and nothing told the seat: round.sh refused rc 4 ENDPOINT DOWN only when a round was attempted,
# and on 10-16 no round was attempted for 3.5 h, so the Spark sat unreachable with nobody knowing. The fix is
# to make the drop cost nothing: round.sh calls `tunnel.sh up` once before refusing, and doctor.sh calls
# `tunnel.sh check` at every Wednesday boot.
#
# SCOPE, exactly: this re-opens the LOCAL ssh forward only. It NEVER touches the box, the container or vLLM
# (a stopped model is restarted with the box's own run-a2.sh / RELOAD notes, by a human or Friday — see
# 0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/). It never kills a process: if something already
# LISTENS on the port while the endpoint is down, that is reported (rc 4), not "fixed".
#
# Usage:
#   tunnel.sh check   -> rc 0 "UP" when GET $SPARK_URL/v1/models answers 200; rc 1 "DOWN ..." otherwise
#   tunnel.sh up      -> rc 0 when up (already, or after re-opening the forward); rc 4 when it cannot be made up
# Env seams: SPARK_TUNNEL_PORT (47788, PORTS.md) · SPARK_SSH_HOST (Spark, the NVIDIA Sync alias) ·
#            SPARK_REMOTE (127.0.0.1:8888) · SPARK_URL (default http://127.0.0.1:$SPARK_TUNNEL_PORT)
# bash 3.2; stderr never discarded (ssh's goes to state/tunnel.log and is printed on failure); no cd.

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${SPARK_TUNNEL_PORT:-47788}"
HOST="${SPARK_SSH_HOST:-Spark}"
# Laptop fallback (2026-10-26): NVIDIA Sync names the box "ZGX-Nano-G1n" on the laptop, "Spark" on the Studio.
# If the default alias does not resolve to a configured host, use the laptop's alias when it exists.
if [ -z "${SPARK_SSH_HOST:-}" ] && [ "$(ssh -G Spark 2>/dev/null | awk '/^hostname /{print $2}')" = "spark" ] \
   && [ "$(ssh -G ZGX-Nano-G1n 2>/dev/null | awk '/^hostname /{print $2}')" != "zgx-nano-g1n" ]; then
  HOST="ZGX-Nano-G1n"
fi
REMOTE="${SPARK_REMOTE:-127.0.0.1:8888}"
URL="${SPARK_URL:-http://127.0.0.1:$PORT}"
LOG_DIR="$SELF_DIR/state"
LOG="$LOG_DIR/tunnel.log"
mkdir -p "$LOG_DIR"

ts() { date '+%Y-%m-%d %H:%M:%S'; }
probe() { curl -s -m 10 -o /dev/null -w '%{http_code}' "$URL/v1/models" 2>&1; }
listener() { lsof -nP -iTCP:"$PORT" -sTCP:LISTEN 2>&1 | awk 'NR>1 {print $1" pid "$2}' | sort -u | tr '\n' ' '; }

do_check() {
  local code; code="$(probe)"
  if [ "$code" = "200" ]; then
    echo "UP — $URL/v1/models 200 (listener: $(listener))"
    return 0
  fi
  local lis; lis="$(listener)"
  echo "DOWN — $URL/v1/models http=$code; listener on $PORT: ${lis:-none}"
  [ -z "$lis" ] && echo "  no listener: the local forward is gone — re-open with: bash $SELF_DIR/tunnel.sh up"
  return 1
}

do_up() {
  if [ "$(probe)" = "200" ]; then
    echo "UP — already: $URL/v1/models 200 (listener: $(listener))"
    return 0
  fi
  local lis; lis="$(listener)"
  if [ -n "$lis" ]; then
    echo "REFUSED rc 4 — endpoint DOWN but something already listens on $PORT ($lis)."
    echo "  Not killed (this script never kills). Most likely the box or its container is down, not the forward:"
    echo "  check the Spark per 0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/ (run-a2.sh / RELOAD)."
    return 4
  fi
  echo "$(ts) re-opening: ssh -f -N -L $PORT:$REMOTE $HOST (keepalives)" >> "$LOG"
  ssh -f -N -o ServerAliveInterval=30 -o ServerAliveCountMax=6 -o ExitOnForwardFailure=yes \
      -o ConnectTimeout=15 -L "$PORT:$REMOTE" "$HOST" >> "$LOG" 2>&1
  local src=$?
  if [ $src -ne 0 ]; then
    echo "REFUSED rc 4 — ssh exited $src opening the forward; its stderr (tail of $LOG):"
    tail -5 "$LOG"
    return 4
  fi
  local i code
  for i in 1 2 3 4 5 6 7 8 9 10; do
    code="$(probe)"
    [ "$code" = "200" ] && break
    sleep 1
  done
  if [ "$code" = "200" ]; then
    echo "$(ts) re-opened OK (listener: $(listener))" >> "$LOG"
    echo "UP — re-opened the forward: $URL/v1/models 200 (listener: $(listener))"
    return 0
  fi
  echo "$(ts) forward open but endpoint http=$code" >> "$LOG"
  echo "REFUSED rc 4 — the forward is open (listener: $(listener)) but $URL/v1/models answers http=$code:"
  echo "  the box or its container is down; this script never touches the box (see the Spark kit's RELOAD notes)."
  return 4
}

case "${1:-}" in
  check) do_check ;;
  up)    do_up ;;
  *)     echo "usage: tunnel.sh check|up" >&2; exit 2 ;;
esac
