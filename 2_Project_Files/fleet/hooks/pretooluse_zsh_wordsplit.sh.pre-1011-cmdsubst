#!/bin/bash
# pretooluse_zsh_wordsplit.sh — PreToolUse hook (matcher: Bash): REFUSE a command that relies on
# bash word-splitting of an unquoted $VAR while running under zsh (the Bash tool's shell).
#
# WHY (Friday ledger w=3, 2026-10-10): zsh does NOT word-split an unquoted parameter. So
#   G="git -C /x"; $G status            runs a command literally named "git -C /x" and fails, and
#   for p in "a b" "c d"; do set -- $p   leaves $1 as the whole string.
# Three checks built that way could not pass. The fix is to run the snippet under bash.
#
# REFUSES (exit 2) when ALL hold:
#   - the command is not bash-wrapped (first word is not `bash`, so `bash -c '…'`, `bash script`
#     and `bash <<EOF` all pass); `bash -c '…'` / `sh -c '…'` strings elsewhere are ignored too;
#   - a variable is assigned a quoted value containing whitespace (NAME="a b", NAME='a b'), or a
#     `for x in` list has a quoted item containing whitespace;
#   - that variable is then used UNQUOTED in a splitting position: command position
#     ($NAME args / ${NAME} args), `set [--] … $NAME`, or `for y in … $NAME`.
# PASSES: "$NAME" quoted uses; values without whitespace; heredoc bodies; bash-wrapped snippets.
# NOT COVERED, stated: variables assigned in an earlier call or the environment; unquoted uses as
# plain arguments (echo $G — zsh passes one word, usually what was meant); ${=NAME} (zsh's own
# explicit split — not refused, it is the correct zsh spelling). Fail-open on a parse error.
HOOK_INPUT="$(cat)"; export HOOK_INPUT
python3 -I - <<'PY'
import json, os, re, sys
try:
    cmd = json.loads(os.environ.get("HOOK_INPUT", "")).get("tool_input", {}).get("command", "")
    if not isinstance(cmd, str): sys.exit(0)
except Exception as e:
    print(f"pretooluse_zsh_wordsplit: parse error, passing: {e}", file=sys.stderr); sys.exit(0)

def strip_heredocs(t):
    out, end = [], None
    for ln in t.split("\n"):
        if end is not None:
            if ln.strip() == end: end = None
            continue
        out.append(ln)
        m = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", ln)
        if m: end = m.group(1)
    return "\n".join(out)

try:
    text = strip_heredocs(cmd)
    if re.match(r"\s*(?:env\s+(?:[A-Za-z_]\w*=\S*\s+)*)?bash(?:\s|$)", text):
        sys.exit(0)                                         # bash is the command: bash splits
    DQ = r'"(?:[^"\\]|\\.)*"'
    SQ = r"'[^']*'"
    text = re.sub(r"\b(?:bash|sh)\s+-c\s+(?:%s|%s)" % (SQ, DQ), " ", text)

    ws = set()
    for m in re.finditer(r"(?:^|(?<=[\s;&|(`]))([A-Za-z_]\w*)=(?:\"((?:[^\"\\]|\\.)*)\"|'([^']*)')", text):
        val = m.group(2) if m.group(2) is not None else m.group(3)
        if re.search(r"\s", val): ws.add(m.group(1))
    for m in re.finditer(r"\bfor\s+([A-Za-z_]\w*)\s+in\s+([^;\n]*)", text):
        if re.search(r"\"[^\"]*\s[^\"]*\"|'[^']*\s[^']*'", m.group(2)): ws.add(m.group(1))
    if not ws: sys.exit(0)

    names = "|".join(sorted(map(re.escape, ws)))
    REF = r"\$(?:\{(%s)\}|(%s)(?![A-Za-z0-9_]))" % (names, names)
    bare = re.sub(r"%s|%s" % (DQ, SQ), '""', text)          # quoted uses are not splitting uses
    hit = None
    for seg in re.split(r"(?:\n|;|&&|\|\||\||\$\(|`|\(|\bthen\b|\bdo\b|\belse\b)", bare):
        s = seg.strip()
        m = re.match(REF + r"(?:\s|$)", s)
        if m: hit = (m.group(1) or m.group(2), "in command position"); break
        if re.match(r"set(?:\s|$)", s):
            m = re.search(REF, s)
            if m: hit = (m.group(1) or m.group(2), "in `set -- $NAME`"); break
        mf = re.match(r"for\s+[A-Za-z_]\w*\s+in\s+(.*)", s)
        if mf:
            m = re.search(REF, mf.group(1))
            if m: hit = (m.group(1) or m.group(2), "in a `for … in $NAME` list"); break
except SystemExit:
    raise
except Exception as e:
    print(f"pretooluse_zsh_wordsplit: internal error, passing: {e}", file=sys.stderr); sys.exit(0)

if hit:
    name, where = hit
    print(f"REFUSED by pretooluse_zsh_wordsplit.sh: ${name} holds a value with spaces and is used "
          f"unquoted {where}, which relies on word-splitting — but the Bash tool runs zsh, which does "
          f"NOT split an unquoted $VAR, so the command would run one literal word (e.g. a program "
          f"named \"git -C /x\") or leave $1 as the whole string (Friday ledger w=3, 2026-10-10). "
          f"Fix: wrap the whole call in bash, i.e.  bash -c '<the same command>'  (or bash <<'EOF' … EOF), "
          f"or use an array / write the command out in full.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
exit $?
