#!/usr/bin/env python3
# grepcase.py — the checker behind pretooluse_grep_case.sh (same split as pathguard.py, and for
# the same reason: macOS bash 3.2 cannot parse a heredoc holding backticks inside `$( ... )`,
# which the first draft found on its first exercise — 23/23 fixtures failed with a bash syntax
# error before a single grep was inspected). Reads the hook JSON on stdin; prints ONE JSON line
# (additionalContext) when a warning is due, nothing otherwise; the warning also goes to stderr.
# Never exits non-zero on the instrument: a parse failure is a silent pass, stated.
import json, re, sys

try:
    d = json.loads(sys.stdin.read() or "{}")
    cmd = d.get("tool_input", {}).get("command", "") or ""
except Exception as e:
    print("pretooluse_grep_case: could not parse hook input: %s" % e, file=sys.stderr)
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

# Tokenise ONE grep invocation starting at index i (just after the word `grep`): returns a
# list of (raw_text, value, quoted) tokens up to an unquoted shell operator / newline.
def tokens_after(s, i):
    toks, cur, raw, quoted, inword = [], [], [], False, False
    n = len(s)
    def flush():
        nonlocal cur, raw, quoted, inword
        if inword:
            toks.append(("".join(raw), "".join(cur), quoted))
        cur, raw, quoted, inword = [], [], False, False
    while i < n:
        c = s[i]
        if c in " \t":
            flush(); i += 1; continue
        if c == "\n" or c in ";|&<>()`":
            break
        if c == "\\" and i + 1 < n:
            cur.append(s[i+1]); raw.append(s[i:i+2]); inword = True; i += 2; continue
        if c == "'":
            j = s.find("'", i + 1)
            if j < 0: j = n
            cur.append(s[i+1:j]); raw.append(s[i:j+1]); quoted = True; inword = True; i = j + 1; continue
        if c == '"':
            j = i + 1; buf = []
            while j < n and s[j] != '"':
                if s[j] == "\\" and j + 1 < n and s[j+1] in '"\\$`':
                    buf.append(s[j+1]); j += 2; continue
                buf.append(s[j]); j += 1
            cur.append("".join(buf)); raw.append(s[i:j+1]); quoted = True; inword = True; i = j + 1; continue
        cur.append(c); raw.append(c); inword = True; i += 1
    flush()
    return toks

# Command-position grep, bare or /usr/bin/grep (the Bash tool is zsh where `grep` is a shell
# function, so seats type both). `git grep` is deliberately NOT covered (different tool).
inv = re.compile(r"(?:^|[;&|(`\n]|\$\(|\bthen\s|\bdo\s|\bxargs\s)\s*(?:/usr/bin/)?grep(?=\s|$)", re.M)
warnings = []
for m in inv.finditer(cmd):
    toks = tokens_after(cmd, m.end())
    flags = set(); pattern = None; pat_quoted = False; pat_raw = ""
    k = 0
    while k < len(toks):
        raw, val, quoted = toks[k]
        if pattern is None and not quoted and val == "--":
            k += 1
            if k < len(toks):
                pat_raw, pattern, pat_quoted = toks[k]
            break
        if pattern is None and not quoted and val.startswith("--"):
            name = val[2:].split("=")[0]
            if name == "regexp" and "=" in val:
                pattern = val.split("=", 1)[1]; pat_raw = raw
            elif name == "regexp" and k + 1 < len(toks):
                k += 1; pat_raw, pattern, pat_quoted = toks[k]
            else:
                flags.add({"count": "c", "quiet": "q", "silent": "q", "line-number": "n",
                           "ignore-case": "i", "no-ignore-case": "I"}.get(name, name))
            k += 1; continue
        if pattern is None and not quoted and val.startswith("-") and len(val) > 1:
            letters = val[1:]
            # short flags that TAKE an argument: e (pattern) f (file) m A B C d D
            j = 0
            while j < len(letters):
                ch = letters[j]
                if ch == "e":
                    rest = letters[j+1:]
                    if rest:
                        pattern = rest; pat_raw = raw
                    elif k + 1 < len(toks):
                        k += 1; pat_raw, pattern, pat_quoted = toks[k]
                    break
                if ch in "fmABCdD":
                    if not letters[j+1:] and k + 1 < len(toks):
                        k += 1
                    break
                flags.add(ch); j += 1
            k += 1; continue
        if pattern is None:
            pat_raw, pattern, pat_quoted = raw, val, quoted
        k += 1
    if pattern is None:
        continue
    snippet = (pat_raw or pattern)[:60]
    if "$(" in pattern or "$(" in pat_raw:
        warnings.append("grep pattern contains `$(` (%s) — a composed command inside the pattern; build the phrase in a variable first and check what it holds" % snippet)
        continue
    if flags & {"c", "q", "n"} and "i" not in flags and pat_quoted and " " in pattern.strip():
        warnings.append("`grep -%s %s` is a CASE-SENSITIVE multi-word phrase grep — its zero would be a false zero on any capitalisation drift (ledger w=3, 2026-09-11 REGRESSION). Use /usr/bin/grep -i and pair the count with a positive control from the same file"
                        % ("".join(sorted(flags & {"c", "q", "n"})), snippet))

if not warnings:
    sys.exit(0)
text = "ADVISORY from pretooluse_grep_case.sh (not blocked): " + " | ".join(warnings)
print(text, file=sys.stderr)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}}))
