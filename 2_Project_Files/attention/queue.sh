#!/bin/bash
# queue.sh — Wednesday's unified attention queue CLI.
#
#   queue.sh list                fresh view: runs ingest first, then prints
#                                unread (newest first), then recent read
#   queue.sh mark <id>           mark ONE item read (explicit acknowledgment)
#   queue.sh mark all-listed     mark everything the last `list` showed as unread
#   queue.sh count               "<n> unread / <m> total"
#
# Marking is NEVER automatic — not on ingest, not on list (2026-08-04
# lesson: acknowledgment covers exactly what was explicitly marked).
# Queue is Wednesday's and Kam's only; no project agent reads it.
# bash 3.2-safe.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CMD="${1:-}"
case "$CMD" in
  list)
    # list = fresh view: ingest first. On ingest failure, still list what we
    # have, but say loudly that the view is stale (never discard stderr).
    if ! "$SCRIPT_DIR/ingest.sh"; then
      echo "WARN: ingest failed — listing possibly-stale queue" >&2
    fi
    python3 "$SCRIPT_DIR/queue_cli.py" list
    ;;
  mark)
    shift
    python3 "$SCRIPT_DIR/queue_cli.py" mark "$@"
    ;;
  count)
    python3 "$SCRIPT_DIR/queue_cli.py" count
    ;;
  *)
    echo "usage: queue.sh list | mark <id|all-listed> | count" >&2
    exit 2
    ;;
esac
