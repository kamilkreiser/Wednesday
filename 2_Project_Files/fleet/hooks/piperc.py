#!/usr/bin/env python3
# piperc.py — checker for pretooluse_pipe_rc.sh (ADVISORY ONLY; the wrapper always exits 0).
#
# WHY (Tuesday ledger _ledger_laptop_datasec.md 2026-11-01, w=3 REGRESSION): an exit code read
# with `echo $?` straight after a PIPELINE is the exit code of the pipeline's LAST command
# (`cut`, `head`, `tail`), not of the command being checked. zsh has no PIPESTATUS
# (learnings/2026-08-26_zsh-has-no-pipestatus.md). Three times a `pgrep ... | cut; echo rc=$?`
# printed rc=0 over an empty result, once as the guard before a destructive pane close.
#
# What it flags: a `$?` read in a command segment whose IMMEDIATELY PRECEDING segment (split on
# `;`, `&&`, `||`, newline) contains a pipe `|` (not `||`). Heredoc bodies are stripped first
# (prose that quotes the pattern is not the pattern). Reads the hook JSON on stdin; prints ONE
# JSON line (additionalContext) when a warning is due, nothing otherwise; the warning also goes to
# stderr. A parse failure passes silently (fail-open on the instrument, stated).
import json, re, sys

try:
    d = json.loads(sys.stdin.read() or "{}")
    cmd = d.get("tool_input", {}).get("command", "") or ""
except Exception as e:
    print("pretooluse_pipe_rc: could not parse hook input: %s" % e, file=sys.stderr)
    sys.exit(0)

def strip_heredocs(t):
    out, i = [], 0
    lines = t.split("\n")
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.search(r"<<-?\s*([\x27\x22]?)([A-Za-z_][A-Za-z0-9_]*)\1", line)
        i += 1
        if not m:
            continue
        delim = m.group(2)
        while i < len(lines) and lines[i].strip() != delim:
            i += 1
        if i < len(lines):
            out.append(lines[i]); i += 1
    return "\n".join(out)

cmd = strip_heredocs(cmd)
# Drop single-quoted strings: a `|` or `$?` inside '...' is data (a regex, an awk program), not shell.
cmd_nq = re.sub(r"'[^']*'", "''", cmd)
segs = re.split(r";|&&|\|\||\n", cmd_nq)
hits = []
for k in range(1, len(segs)):
    if "$?" in segs[k] and re.search(r"(?<!\|)\|(?!\|)", segs[k - 1]):
        hits.append((segs[k - 1].strip()[-70:], segs[k].strip()[:50]))
if not hits:
    sys.exit(0)
a, b = hits[0]
text = ("ADVISORY from pretooluse_pipe_rc.sh (not blocked): `%s` reads $? right after a PIPELINE (`...%s`): "
        "that is the exit code of the pipeline's LAST command, not of the one you mean (zsh has no PIPESTATUS; "
        "Tuesday ledger 2026-11-01 w=3 REGRESSION). Run the checked command alone, e.g. `cmd >/dev/null; echo rc=$?`, "
        "and read its output in a separate step." % (b, a))
print(text, file=sys.stderr)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}}))
