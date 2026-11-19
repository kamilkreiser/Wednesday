#!/usr/bin/env python3
"""Checker for pretooluse_cockpit_verb.sh. stdin = the Bash command; argv[1] = cockpit.sh verbs 'a|b|c'.
Prints one line per problem (empty output = allow). See the hook's header for WHY.
Run with --selftest to exercise the fire and quiet paths."""
import re
import sys

COCKPIT_RE = re.compile(r"/cockpit/cockpit\.sh[\"']?(?:\s+(\S+))?")
FLEET_RE = re.compile(r"(?:2_Project_Files/(?:fleet|tools)/\S*\.sh|/(?:fleet|tools|cockpit)/[A-Za-z0-9_.-]+\.sh)")
# A tool counts only in COMMAND POSITION of a segment: optional ( { , VAR=x assignments, nohup/time/exec/command,
# then bash/sh/zsh or the path itself. A path that is an ARGUMENT (grep, sed, cat, ls, true reading the file) is
# not a run (2026-11-20 00:0x: the first version refused a grep over cockpit.sh's own source).
PREFIX = r"^\s*[({]*\s*(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*(?:(?:nohup|time|exec|command)\s+)*(?:(?:bash|sh|zsh)\s+)?[\"']?"
CMDPOS_COCKPIT_RE = re.compile(PREFIX + r"\S*/cockpit/cockpit\.sh[\"']?(?:\s+(\S+))?")
CMDPOS_FLEET_RE = re.compile(PREFIX + r"\S*/(?:fleet|tools|cockpit)/[A-Za-z0-9_.-]+\.sh")
SEG_SPLIT = re.compile(r"\|\||&&|;|\||\n|\$\(|`")
HEREDOC_RE = re.compile(r"<<-?\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]")


def strip_quoted_heredocs(text):
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        out.append(lines[i])
        m = HEREDOC_RE.search(lines[i])
        if m:
            tag = m.group(1)
            i += 1
            while i < len(lines) and lines[i].strip() != tag:
                i += 1
        i += 1
    return "\n".join(out)


def stdout_null(seg):
    return bool(re.search(r"&>\s*/dev/null", seg) or re.search(r"(?:^|[^0-9&])1?>\s*/dev/null", seg))


def stderr_gone(seg):
    return bool(re.search(r"&>\s*/dev/null", seg) or re.search(r"2>\s*/dev/null", seg)
                or re.search(r">\s*/dev/null\s+2>&1", seg))


def check(cmd, verbs):
    t = strip_quoted_heredocs(cmd)
    probs = []
    for seg in SEG_SPLIT.split(t):
        m = CMDPOS_COCKPIT_RE.match(seg)
        if not m:
            continue
        w = m.group(1)
        if w is None or not re.match(r"[A-Za-z_]", w):
            probs.append("cockpit.sh with NO verb (next word: %s)" % (w or "end of command"))
        else:
            v = re.match(r"[A-Za-z_][A-Za-z0-9_-]*", w).group(0)
            if v not in verbs:
                probs.append("cockpit.sh invented verb: %s" % v)
    for seg in SEG_SPLIT.split(t):
        if CMDPOS_FLEET_RE.match(seg) and stdout_null(seg) and stderr_gone(seg):
            probs.append("fleet tool with stdout AND stderr discarded: %s" % seg.strip()[:160])
    return probs


def selftest():
    V = set("up|launch|resolve|add|layout|status|say|rotate|down".split("|"))
    C = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/cockpit.sh"
    T = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/wake_ack.sh"
    fire = [
        C + " 2>/dev/null >/dev/null",
        C + " --help",
        C,
        "bash " + C + " list 2>/dev/null | head -0",
        T + " %0 >/dev/null 2>&1",
        "bash " + T + " %0 &>/dev/null",
        "x=1; bash " + C + " ; echo done",
        "FOO=1 nohup bash " + C + " 2>/dev/null",
        "(" + T + " %0 >/dev/null 2>&1)",
        "echo $(" + C + " --help)",
    ]
    quiet = [
        "bash " + C + " say --mail 'subj' 2>&1 | tail -3",
        "bash " + C + " launch Secuura/Blockchain-K > /tmp/x.txt 2>&1",
        T + " %0 2>&1",
        "pgrep -f foo >/dev/null 2>&1",
        "cat > /tmp/f <<'EOF'\n" + C + " 2>/dev/null >/dev/null\n" + T + " >/dev/null 2>&1\nEOF\necho ok",
        "bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/note_entry.sh --stdin <<'EOF'\nran cockpit.sh --help by mistake\nEOF",
        "bash " + T + " %0 > /tmp/out.txt",
        "/usr/bin/grep -n -i -E 'say\\)|--mail' " + C + " | head -8",
        "sed -n '1,40p' " + C,
        "true " + C + " --help",
        "ls -l " + T + " >/dev/null 2>&1",
    ]
    bad = 0
    for c in fire:
        if not check(c, V):
            print("SELFTEST FAIL (should fire):", repr(c)); bad += 1
    for c in quiet:
        p = check(c, V)
        if p:
            print("SELFTEST FAIL (should be quiet):", repr(c), p); bad += 1
    print("selftest: %d fire, %d quiet, %d failures" % (len(fire), len(quiet), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    verbs = set(sys.argv[1].split("|")) if len(sys.argv) > 1 else set()
    print("\n".join(check(sys.stdin.read(), verbs)))
