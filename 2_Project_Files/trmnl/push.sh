#!/bin/bash
# push.sh — build the TRMNL "Kam view" payload and POST it to the private plugin's webhook.
#
# NOT RUN by the design task (2026-10-09). Kam supplies the URL first (README, step 6).
#
#   push.sh            build + POST
#   push.sh --dry-run  build + measure + print the payload; NO network, URL not needed
#
# Reads from 4_Credentials/.env (parsed, never sourced, never echoed):
#   TRMNL_WEBHOOK_URL    required for a real push — https://trmnl.com/api/custom_plugins/<uuid>
#   TRMNL_REDACT         optional, e.g. "datasec,secuura" -> titles replaced by "Datasec event"
#   TRMNL_PAYLOAD_LIMIT  optional, bytes; 5120 standard, 10240 with TRMNL+
#
# Guarantees:
#   * the URL is never printed, logged, or put on a command line (curl reads it from stdin
#     config, so it is not visible in `ps`);
#   * refuses (exit 2) when the variable is unset or not an https://trmnl.com/api/custom_plugins/ URL;
#   * refuses (exit 4) a push within MIN_GAP_S of the last successful one: TRMNL allows 12
#     webhook posts/hour on the standard plan (docs.trmnl.com/go/private-plugins/webhooks),
#     and a 429 is a wasted cycle;
#   * stderr is never discarded: build_payload's and curl's both go to the log AND the terminal.
set -u
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$DIR/../.." && pwd)"
ENV_FILE="$ROOT/4_Credentials/.env"
STATE="$DIR/state"; LOG="$DIR/logs/push.log"
MIN_GAP_S="${TRMNL_MIN_GAP_S:-300}"
mkdir -p "$STATE" "$DIR/logs"
log() { printf '%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$*" | tee -a "$LOG" >&2; }

envval() {   # envval NAME -> value of NAME= in .env, without sourcing the file
  [ -f "$ENV_FILE" ] || return 0
  /usr/bin/awk -v k="$1" 'index($0, k"=")==1 { sub(/^[^=]*=/, ""); v=$0 } END { if (v != "") print v }' "$ENV_FILE" \
    | /usr/bin/sed -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'\$/\1/"
}

DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
REDACT="$(envval TRMNL_REDACT)"
LIMIT="$(envval TRMNL_PAYLOAD_LIMIT)"; LIMIT="${LIMIT:-5120}"

PAYLOAD="$(python3 -I "$DIR/build_payload.py" --measure --limit "$LIMIT" ${REDACT:+--redact "$REDACT"} 2> >(tee -a "$LOG" >&2))"
rc=$?
if [ $rc -ne 0 ] || [ -z "$PAYLOAD" ]; then
  log "REFUSED: build_payload exit $rc — nothing sent"
  exit 3
fi

if [ $DRY -eq 1 ]; then
  printf '%s\n' "$PAYLOAD"
  log "dry-run: payload built (${#PAYLOAD} chars), nothing sent"
  exit 0
fi

URL="$(envval TRMNL_WEBHOOK_URL)"
if [ -z "$URL" ]; then
  log "REFUSED: TRMNL_WEBHOOK_URL is not set in 4_Credentials/.env — nothing sent"
  exit 2
fi
case "$URL" in
  https://trmnl.com/api/custom_plugins/?*) ;;
  *) log "REFUSED: TRMNL_WEBHOOK_URL is not an https://trmnl.com/api/custom_plugins/<uuid> URL (value not shown)"; exit 2 ;;
esac
case "$URL" in *[[:space:]\"\\]*) log "REFUSED: TRMNL_WEBHOOK_URL contains whitespace/quotes (value not shown)"; exit 2 ;; esac

last="$(cat "$STATE/last_ok_epoch" 2>/dev/null || echo 0)"
now="$(date +%s)"
if [ $((now - last)) -lt "$MIN_GAP_S" ]; then
  log "SKIPPED: last successful push $((now - last))s ago (< ${MIN_GAP_S}s rate guard)"
  exit 4
fi

RESP="$STATE/last_response.json"
# The URL reaches curl through a process-substitution config fd (-K /dev/fd/N): it is never
# an argv element (so not visible in `ps`), never written to disk, never echoed.
code="$(/usr/bin/curl -sS -K <(printf 'url = "%s"\n' "$URL") -X POST \
          -H 'Content-Type: application/json' --data-binary @- \
          -o "$RESP" -w '%{http_code}' --max-time 30 \
          2> >(tee -a "$LOG" >&2) <<<"$PAYLOAD")"
crc=$?
if [ $crc -ne 0 ]; then
  log "FAILED: curl exit $crc — see stderr above (URL not shown)"
  exit 5
fi
case "$code" in
  200) echo "$now" > "$STATE/last_ok_epoch"; log "OK: HTTP 200, payload ${#PAYLOAD} chars" ;;
  429) log "FAILED: HTTP 429 rate-limited (12/h standard) — response in $RESP"; exit 6 ;;
  422) log "FAILED: HTTP 422 (oversize or malformed) — response in $RESP"; exit 6 ;;
  403) log "FAILED: HTTP 403 — device lacks Developer edition, or plugin strategy is not Webhook"; exit 6 ;;
  *)   log "FAILED: HTTP $code — response in $RESP"; exit 6 ;;
esac
