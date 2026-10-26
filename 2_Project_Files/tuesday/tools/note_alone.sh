#!/bin/bash
# note_alone.sh — the Tuesday seat's ONLY way to write a daily-note line: a wrapper around tools/note_entry.sh that
# REFUSES (rc 2, writes nothing) when the assistant message that invoked it holds any other tool call.
#
# WHY (ledger _ledger_laptop_datasec.md, the parallel-call family, REGRESSION w=18 on 2026-10-25): a note issued in
# parallel with a send, a launch, a watcher or a read is composed before that call's output exists, and eighteen times
# it claimed a result that was false or invented. tuesday/hooks/pretooluse_note_alone.sh (2026-10-24) catches a note
# issued BEFORE another call, but not one issued LAST: at PreToolUse time the last tool_use of a message is not yet in
# the transcript. This wrapper checks at EXECUTION time instead, when it is.
# MEASURED 2026-10-25 19:48 (s174, scratchpad probe_msgcount.py): a probe issued LAST beside a Write and a Bash call
# read calls_in_message=3 at execution; the same probe issued alone read 1.
#
# Usage (same forms as note_entry.sh; the body MUST come by --stdin so it appears verbatim in the transcript):
#   note_alone.sh --stdin <<'EOF'        -> "- HH:MM — text"
#   note_alone.sh --h3 --stdin <<'EOF'   -> "### HH:MM — title"
# How it finds its own message: the NEWEST assistant tool_use whose command contains "note_alone.sh" AND the body's
# first non-empty line (up to 80 chars); it then counts every tool_use block sharing that message id.
# FAIL-CLOSED since 2026-10-26 20:1x (ledger w=24 and w=29 of the parallel-note family): no transcript, a read error,
# or its own call not found after 12 reads (~3 s) -> REFUSED rc 3, nothing written. Both fail-open writes on record
# (10:21 and 18:10, 26 Oct) were notes that DID share their message with another call, so the open path let through
# exactly the case it exists to stop. A refused note is not lost: its body is in the transcript, re-issue it alone.
# Override, for a seat with no transcript at all: NOTE_ALONE_ALLOW_UNCHECKED=1 (writes, and says so on stderr).
# Arms: tests/note_alone_arms.sh
set -u
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTE_ENTRY="${NOTE_ALONE_NOTE_ENTRY:-$DIR/../../tools/note_entry.sh}"
STDIN=0; for a in "$@"; do [ "$a" = "--stdin" ] && STDIN=1; done
[ "$STDIN" = 1 ] || { echo "note_alone.sh: REFUSED: pass the body with --stdin <<'EOF' (it must be in the transcript verbatim)" >&2; exit 2; }
BODY="$(cat)"
[ -n "$BODY" ] || { echo "note_alone.sh: REFUSED: empty body" >&2; exit 2; }
TPDIR="${NOTE_ALONE_TRANSCRIPT_DIR:-${CLAUDE_CONFIG_DIR:-$DIR/../../../4_Credentials/.claude}/projects/-Volumes-Laptop-DEV-TUESDAY}"
ALLOW="${NOTE_ALONE_ALLOW_UNCHECKED:-0}"
export BODY TPDIR ALLOW
python3 -I - <<'PY'
import glob, json, os, sys, time
body, d = os.environ["BODY"], os.environ["TPDIR"]
allow = os.environ.get("ALLOW") == "1"
first = next((l.strip() for l in body.splitlines() if l.strip()), "")[:80]
def not_run(why):
    if allow:
        print(f"note_alone.sh: check NOT run ({why}); NOTE_ALONE_ALLOW_UNCHECKED=1 given, writing the note", file=sys.stderr); sys.exit(0)
    print(f"note_alone.sh: REFUSED (rc 3), nothing written: check NOT run ({why}).\n"
          "Re-issue the note ALONE in its own message (no other call, no text beside it).", file=sys.stderr); sys.exit(3)
files = glob.glob(os.path.join(d, "*.jsonl"))
if not files:
    not_run(f"no transcript in {d}")
tp = max(files, key=os.path.getmtime)
for attempt in range(12):
    count, mid = {}, None
    try:
        for line in open(tp, encoding="utf-8", errors="replace"):
            if '"tool_use"' not in line: continue
            try: e = json.loads(line)
            except Exception: continue
            if e.get("type") != "assistant": continue
            m = e.get("message") or {}
            k = m.get("id") or e.get("uuid")
            for b in m.get("content") or []:
                if not isinstance(b, dict) or b.get("type") != "tool_use": continue
                count[k] = count.get(k, 0) + 1
                c = (b.get("input") or {}).get("command", "") or ""
                if "note_alone.sh" in c and first in c: mid = k
    except Exception as ex:
        not_run(f"transcript read error: {ex}")
    if mid is not None: break
    time.sleep(0.25)
if mid is None:
    not_run("own call not found in the transcript after 12 reads")
n = count[mid]
if n > 1:
    print(f"note_alone.sh: REFUSED, nothing written: this note shares its message with {n - 1} other tool call(s).\n"
          "A note written in parallel is composed before the other output exists (ledger w=18, 2026-10-25).\n"
          "Read the other output, then re-issue the note ALONE in a later message.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
RC=$?
[ "$RC" = 2 ] && exit 2
[ "$RC" = 3 ] && exit 3
[ "$RC" = 0 ] || { echo "note_alone.sh: REFUSED, nothing written: the check exited rc $RC" >&2; exit 3; }
printf '%s\n' "$BODY" | bash "$NOTE_ENTRY" "$@"
