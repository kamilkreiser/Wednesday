#!/bin/bash
# pretooluse_note_alone.sh — PreToolUse hook (matcher: Bash), Tuesday seat only: REFUSE a note_entry.sh call that is
# not the ONLY tool call in its assistant message.
#
# WHY (ledger _ledger_laptop_datasec.md, the parallel-call family: w=15 on 2026-10-24, three times in s157 alone): a
# note issued as a PARALLEL call beside a send, a launch, a commit or a read is composed before that call's output
# exists, and fifteen times it claimed a result that was false or invented ("delivered" for a refused tap, an artifact
# name and size that did not exist). The behavioural rule ("a note_entry call is ALWAYS the only call in its message")
# failed under flow every time; receiptguard.py only catches the same-COMMAND form. The w=8 row (2026-10-12) asked for
# a turn-marker hook; this reads the turn itself instead: the transcript groups every tool_use block of one assistant
# message under one message.id, so the hook counts them.
#
# REFUSES (exit 2): a Bash command that runs note_entry.sh (outside a heredoc body) whose assistant message in the
# transcript holds MORE THAN ONE tool_use block, of any tool.
# FINDS the message by the hook input's tool_use_id; if that is absent, by the newest tool_use whose command equals
# this command exactly.
# FAIL-OPEN, stated: no transcript, no matching tool_use found, or a parse error -> pass, with a line on stderr that
# says the check did not run (never silent), and a line in logs/note_alone.log.
# MEASURED LIMIT (2026-10-24 11:40-11:41, live arms, s158): the LAST tool_use block of a message is not yet in the
# transcript when its PreToolUse hook runs (a solo call never is; re-reading for 1 s does not help). So this CATCHES
# a note issued BEFORE another call in the same message (live red arm refused, rc 2) and does NOT catch a note issued
# LAST (live arm passed as NOT RUN). The hook input carries tool_use_id and prompt_id but no message id, so the
# transcript cannot close that case. The behavioural rule still covers it: note_entry alone, always.
HOOK_INPUT="$(cat)"; HOOK_SELF="${BASH_SOURCE[0]}"; export HOOK_INPUT HOOK_SELF
python3 -I - <<'PY'
import json, os, re, sys
def log(line):
    try:  # one line per checked call, so a hook that never fires (or never finds its call) is measurable
        import datetime
        lg = os.path.join(os.path.dirname(os.path.abspath(os.environ.get("HOOK_SELF", "."))), "logs")
        os.makedirs(lg, exist_ok=True)
        with open(os.path.join(lg, "note_alone.log"), "a") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {line}\n")
    except Exception:
        pass
def warn(msg):
    log(f"NOT RUN: {msg}")
    print(f"pretooluse_note_alone: check NOT run ({msg}); passing", file=sys.stderr); sys.exit(0)
try:
    inp = json.loads(os.environ.get("HOOK_INPUT", ""))
except Exception as e:
    warn(f"input parse error: {e}")
cmd = (inp.get("tool_input") or {}).get("command", "") or ""
if os.environ.get("WED_AGENT") != "tuesday":
    sys.exit(0)  # 2026-10-25: this hook is wired through the SHARED settings template; it acts on the Tuesday seat only

# drop heredoc bodies: a brief or note text may quote note_entry.sh without running it
out, end = [], None
for ln in cmd.split("\n"):
    if end is not None:
        if ln.strip() == end: end = None
        continue
    out.append(ln)
    m = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", ln)
    if m: end = m.group(1)
if not re.search(r"note_entry\.sh\b", "\n".join(out)):
    sys.exit(0)
# 2026-10-25 19:5x (s174, ledger w=18): a direct note_entry.sh write is refused outright on this seat; the wrapper
# tuesday/tools/note_alone.sh checks the message at EXECUTION time, which closes this hook's note-issued-LAST hole.
if not re.search(r"note_entry\.sh\s+--where\b", "\n".join(out)):
    log("REFUSED: direct note_entry.sh (use note_alone.sh)")
    print("REFUSED by pretooluse_note_alone.sh: on the Tuesday seat a note is written ONLY through\n"
          "  bash 2_Project_Files/tuesday/tools/note_alone.sh [--h3] --stdin <<'EOF' ... EOF\n"
          "which refuses when its message holds any other tool call (ledger w=18, 2026-10-25).", file=sys.stderr)
    sys.exit(2)

tp, tuid = inp.get("transcript_path") or "", inp.get("tool_use_id") or ""
if not tp or not os.path.isfile(tp):
    warn("no transcript_path")
def scan():
    count, by_cmd, mid = {}, None, None
    with open(tp, encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"tool_use"' not in line: continue
            try: e = json.loads(line)
            except Exception: continue
            if e.get("type") != "assistant": continue
            msg = e.get("message") or {}
            k = msg.get("id") or e.get("uuid")
            for b in msg.get("content") or []:
                if not isinstance(b, dict) or b.get("type") != "tool_use": continue
                count[k] = count.get(k, 0) + 1
                if tuid and b.get("id") == tuid: mid = k
                if (b.get("input") or {}).get("command") == cmd: by_cmd = k
    # the by-command match is used ONLY when the input carries no tool_use_id: with an id, an older identical
    # command would otherwise be found and a solo note refused for another message's parallel calls
    return count, (mid if tuid else by_cmd)
# 2026-10-24 measured: a SOLO call's entry may not be in the transcript yet when the hook runs (a parallel message's
# was). Re-read a few times before failing open.
import time
for attempt in range(4):
    try:
        count, mid = scan()
    except Exception as e:
        warn(f"transcript read error: {e}")
    if mid is not None: break
    time.sleep(0.25)
if mid is None:
    warn("this call's tool_use not found in the transcript after 4 reads")
n = count.get(mid, 0)
log(f"id={tuid or '-'} calls_in_message={n}")
if n > 1:
    print(f"REFUSED by pretooluse_note_alone.sh: this note_entry.sh call shares its message with {n - 1} other tool "
          "call(s).\nA note written in parallel is composed before the other call's output exists (ledger parallel-call "
          "family, w=15 on 2026-10-24).\nRe-issue the note ALONE, in a later message, after reading the other output.",
          file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
exit $?
