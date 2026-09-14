#!/usr/bin/env python3
# norm.py — the parser behind pretooluse_no_rm.sh (kept in a file: `python3 - <<HEREDOC` swallows the
# hook JSON that arrives on stdin — the first red-proof of this hook passed ALL 14 arms because of exactly that).
import json, re, sys, shlex
try:
    d = json.load(sys.stdin)
    cmd = d.get("tool_input", {}).get("command", "") or ""
except Exception as e:
    print("pretooluse_no_rm: could not parse hook input: %s" % e, file=sys.stderr); sys.exit(0)

SCRATCH = ("/private/tmp/", "/tmp/")
def under_scratch(p):
    return p.startswith(SCRATCH)

# split into command segments at shell command positions; keep it lexical, not a full parser.
# Command positions: line start, `;`, `&&`, `||`, `|`, `$(`, `then`, `do`. NOT the backtick —
# the first live fire (2026-09-14 15:4x, minutes after wiring) refused Wednesday's own daily-note
# heredoc because markdown code spans like `git rm` and `find -delete` became "commands". Backtick
# command substitution is not used in this fleet's commands; markdown backticks are in every note.
# A gate with false positives gets routed around, so the splitter loses the backtick (a backtick-
# substituted rm is the one shape this hook now does not see — stated, accepted).
segments = re.split(r'(?:^|\n|;|&&|\|\||\||\$\(|\bthen\b|\bdo\b)', cmd)
problems = []
for seg in segments:
    s = seg.strip()
    if not s:
        continue
    try:
        toks = shlex.split(s, posix=True)
    except ValueError:
        toks = s.split()
    if not toks:
        continue
    # strip leading env assignments (FOO=bar rm x) and sudo
    i = 0
    while i < len(toks) and (re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', toks[i]) or toks[i] == "sudo"):
        i += 1
    if i >= len(toks):
        continue
    head = toks[i]; rest = toks[i+1:]
    if head in ("rm", "unlink", "/bin/rm", "/usr/bin/unlink"):
        args = [a for a in rest if not a.startswith("-")]
        if not args:
            continue
        bad = [a for a in args if not under_scratch(a)]
        if bad:
            problems.append("%s %s → target(s) outside the scratchpad or non-literal: %s" % (head, " ".join(rest), ", ".join(bad)))
    elif head == "git":
        j = 0
        while j < len(rest) and rest[j].startswith("-"):
            j += 2 if rest[j] in ("-C", "-c") else 1
        if j < len(rest) and rest[j] == "rm":
            sub = rest[j+1:]
            if "--cached" not in sub:
                problems.append("git rm %s → deletes from the working tree (use `git rm --cached` to untrack, or `git mv` into a quarantine folder)" % " ".join(sub))
    elif head == "find" and "-delete" in rest:
        roots = [a for a in rest if not a.startswith("-") and a not in ("(", ")", "!")]
        root = roots[0] if roots else ""
        if not under_scratch(root):
            problems.append("find %s -delete → deletes under '%s', outside the scratchpad" % (root, root))
if problems:
    print("REFUSED by pretooluse_no_rm.sh: this Bash call DELETES outside the session scratchpad.", file=sys.stderr)
    for p in problems:
        print("  - " + p, file=sys.stderr)
    print("Kam 2026-08-26: never delete — quarantine instead: `mkdir -p <dir>/_quarantine_$(date +%F)` then `mv <file> <that dir>/`, and say where it went.", file=sys.stderr)
    print("Deleting your OWN scratch files is fine: write the literal /private/tmp/... path (a $VAR is refused because the hook cannot see it).", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
