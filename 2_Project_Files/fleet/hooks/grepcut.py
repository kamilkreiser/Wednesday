#!/usr/bin/env python3
# grepcut.py — checker behind pretooluse_grep_cut.sh. ADVISORY ONLY (never a refusal).
# WARNS when a grep's output is piped (in the same pipeline) into `cut -c`: a long line (a mail
# body, a one-line paragraph) can carry the matched token PAST the cut, so a HIT displays as a
# MISS. Ledger 2026-11-03 (B 83rd, 'controls ABSENT', cut -c1-300) and 2026-11-10 (B 129th,
# 'scope block NOT IN THE MAIL', cut -c1-330): the same false absence twice, the second after the
# written rule; promoted to this hook. Reads hook JSON on stdin; prints ONE JSON line
# (additionalContext) when due, nothing otherwise. A parse failure is a silent pass, stated.
import json, re, sys
try:
    d = json.loads(sys.stdin.read() or "{}")
    cmd = d.get("tool_input", {}).get("command", "") or ""
except Exception as e:
    print("pretooluse_grep_cut: could not parse hook input: %s" % e, file=sys.stderr)
    sys.exit(0)

def strip_heredocs(t):
    out, i, lines = [], 0, t.split("\n")
    while i < len(lines):
        line = lines[i]; out.append(line); i += 1
        m = re.search(r"<<-?\s*([\x27\x22]?)([A-Za-z_][A-Za-z0-9_]*)\1", line)
        if not m:
            continue
        while i < len(lines) and lines[i].strip() != m.group(2):
            i += 1
        if i < len(lines):
            out.append(lines[i]); i += 1
    return "\n".join(out)

cmd = strip_heredocs(cmd)
hit = False
# A pipeline = text between newlines, ';', '&&', '||'. Inside it, segments split on a single '|'.
for pipeline in re.split(r"\n|;|&&|\|\|", cmd):
    segs = [s.strip() for s in pipeline.split("|")]
    saw_grep = False
    for s in segs:
        if re.match(r"^(\S*/)?grep\b", s):
            saw_grep = True; continue
        if saw_grep and re.match(r"^cut\b.*\s-c", s):
            hit = True; break
    if hit:
        break
if hit:
    msg = ("ADVISORY from pretooluse_grep_cut.sh (not blocked): a grep piped into `cut -c` can hide the matched "
           "token past the cut, so a HIT reads as a MISS (ledger 2026-11-03 and 2026-11-10, false absence twice). "
           "A returned line IS presence. Never write an absence from this view: count with `/usr/bin/grep -o -i -c` "
           "on the untruncated text, with a positive control.")
    print(msg, file=sys.stderr)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": msg}}))
sys.exit(0)
