#!/usr/bin/env python3
"""receiptguard.py — two Bash-command refusals that were OWED as enforcement by Tuesday's ledger.

Called by pretooluse_no_cd.sh with the Bash tool's command on stdin. Prints ONE line
"<clause>|<detail>" when the command must be refused, and nothing otherwise. Exit 0 always;
the caller decides. Kept OUT of the hook's single-quoted python string on purpose (an
apostrophe there bricks every Bash call — the hook's own comments record it twice).

CLAUSE 1 — RECEIPT CHAIN (Tuesday ledger, REGRESSION w=4, 2026-10-06 06:13; earlier rows
2026-09-30, 10-02, 10-03, 10-05). Four times a seat composed a send (send_brief / chat_reply /
cockpit say / decision_queue / brief_and_launch) AND the note line reporting it in ONE command,
so the receipt ("sent", "tap verified", "HTTP 201") was written before the send's output was
read — and twice the send had REFUSED. The rule was known and quoted at every boot; it failed
under the speed of routine relays. Refused here when ALL hold, outside heredoc bodies:
  - the command invokes a refusable sender, AND
  - the command invokes note_entry.sh, AND
  - the note_entry heredoc body carries a receipt word.
Fix: three separate tool calls (send, tap, note) and the note quotes the send's output line.

CLAUSE 2 — DOT-DOT WRITE TARGET (Tuesday ledger, REGRESSION w=3, 2026-10-05 12:25; w=2 rows
2026-09-30 and 10-04). Three times a scratch redirect was written as `$R/../file`, which lands
at the drive root, outside the seat tree (hard rule 1). Refused: a `>`/`>>`/`tee` target, or any
`mv`/`cp` argument, containing a `/..` path segment. Fix: write scratch to the session
scratchpad by its absolute path.

Heredoc BODIES are stripped before matching (prose about these tools is not an invocation —
the lesson pretooluse_no_cd.sh learned three times), except that clause 1 reads the body of the
note_entry heredoc, because that body IS the receipt.
"""
import re
import sys

SENDER = re.compile(
    r"(?:send_brief\.sh|chat_reply\.sh|brief_and_launch\.sh|cockpit\.sh\s+say\b|decision_queue\.sh\s+(?:add|rule)\b)")
NOTE = re.compile(r"note_entry\.sh\b")
RECEIPT = re.compile(
    r"\b(?:sent|posted|delivered|tapped|tap\s+verified|verified\s+at|HTTP\s*201)\b", re.I)
HEREDOC_OPEN = re.compile(r"<<-?\s*([\x27\x22]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def split_heredocs(text):
    """Return (outside_text, [(opener_line, body), ...])."""
    lines = text.split("\n")
    out, bodies, i = [], [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        m = HEREDOC_OPEN.search(line)
        if not m:
            continue
        delim, body = m.group(2), []
        while i < len(lines) and lines[i].strip() != delim:
            body.append(lines[i])
            i += 1
        bodies.append((line, "\n".join(body)))
        if i < len(lines):
            out.append(lines[i])
            i += 1
    return "\n".join(out), bodies


def receipt_chain(outside, bodies):
    if not (SENDER.search(outside) and NOTE.search(outside)):
        return None
    for opener, body in bodies:
        if NOTE.search(opener):
            m = RECEIPT.search(body)
            if m:
                return "receipt-chain|the note body says %r in the same command as a send" % m.group(0)
    return None


REDIR = re.compile(r"(?:>>?|\btee\s+(?:-a\s+)?)\s*([\x22\x27]?)([^\s;|&<>]+)\1")
MVCP = re.compile(r"(?:^|[;&|(\n]|\bthen\s|\bdo\s)\s*(?:mv|cp)\s+([^;&|\n]+)")
DOTDOT = re.compile(r"(?:^|/)\.\.(?:/|$)")


def dotdot_target(outside):
    for m in REDIR.finditer(outside):
        tgt = m.group(2)
        if tgt.startswith("&"):          # 2>&1 and friends
            continue
        if DOTDOT.search(tgt) and "/" in tgt:
            return "dotdot-write|redirect target %s" % tgt
    for m in MVCP.finditer(outside):
        for arg in m.group(1).split():
            arg = arg.strip("\x22\x27")
            if arg.startswith("-"):
                continue
            if DOTDOT.search(arg) and "/" in arg:
                return "dotdot-write|mv/cp argument %s" % arg
    return None


def main():
    cmd = sys.stdin.read()
    outside, bodies = split_heredocs(cmd)
    hit = receipt_chain(outside, bodies) or dotdot_target(outside)
    if hit:
        print(hit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
