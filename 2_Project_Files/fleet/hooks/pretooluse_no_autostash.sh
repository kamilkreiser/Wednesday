#!/bin/bash
# pretooluse_no_autostash.sh — PreToolUse hook (matcher: Bash): REFUSE a hand-typed autostash pull or
# rebase, or a wholesale stash of 0_Brain/dashboard/data/, against THIS repo. Use tools/safe_pull.sh.
#
# WHY (ledger w=3, 2026-10-06 — "dashboard state swept by a stash"): three times in one day the
# coordinator's own hand pull swept STATE (decisions.json, the chat streams, the Spark done.md) into an
# autostash or a wholesale stash: the KS-1402 card vanished locally, two finished Spark tasks would
# have re-run, 12 panel posts sat in a stash. Inspecting afterwards caught all three; the rule
# "inspect the autostash" is a catch, not a prevention. safe_pull.sh is the prevention, and this hook
# is what makes it the only path (an-enforcement-you-must-arm-is-not-one; its 09-10 sibling: an
# optional mechanism is a rule with a script attached).
#
# REFUSES (exit 2), only at a git command aimed at this repo:
#   git … pull … --autostash | -c rebase.autoStash=true      git … rebase … --autostash
#   git … stash (push|save)? … 0_Brain/dashboard/data[/]   (the whole folder; named files are fine)
# "This repo" = no -C; or -C naming the hook's own project root ($CLAUDE_PROJECT_DIR, else three
# levels above this hooks/ folder) or a path inside it; or -C with WEDNESDAY/FRIDAY/TUESDAY as a
# path segment; or an unresolved $VAR target.
# IGNORES: text inside heredoc bodies (briefs may quote the command), `--no-autostash`.
#
# 2026-10-10 (Friday, two holes measured that day):
#  (a) only segments whose first word was literally `git` were inspected, so
#      bash -c 'G="git -C <root>"; $G pull --rebase --autostash' performed an autostash pull.
#      Now: simple assignments in the same command text (NAME="…", NAME='…', NAME=word, including
#      inside a bash -c string) are collected and $NAME / ${NAME} are substituted before matching;
#      a leading `bash|sh|zsh -c '` is peeled off a segment.
#  (b) -C counted as this repo only when the path contained WEDNESDAY, so on the FRIDAY and
#      TUESDAY trees `git -C <own root> pull --autostash` passed. Now root-relative (see above).
#  The refusal names safe_pull.sh under the resolved root, not a hard-coded DevMASTER path.
# NOT COVERED, stated: tools that pull internally (safe_push.sh, wed_claim.sh); a variable assigned
# in an earlier Bash call or exported in the environment (not visible in this command text).
# Fail-open on a parse error. The Python is fed by a QUOTED heredoc so an apostrophe in it is safe.
HOOK_OWN_ROOT="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../.." 2>/dev/null && pwd)"
HOOK_INPUT="$(cat)"; export HOOK_INPUT HOOK_OWN_ROOT
python3 -I - <<'PY'
import json, os, re, sys
try:
    cmd = json.loads(os.environ.get("HOOK_INPUT", "")).get("tool_input", {}).get("command", "")
except Exception as e:
    print(f"pretooluse_no_autostash: parse error, passing: {e}", file=sys.stderr); sys.exit(0)
root = (os.environ.get("CLAUDE_PROJECT_DIR") or os.environ.get("HOOK_OWN_ROOT") or "").rstrip("/")
root = os.path.normpath(root) if root else ""

# drop heredoc bodies
lines, out, end = cmd.split("\n"), [], None
for ln in lines:
    if end is not None:
        if ln.strip() == end: end = None
        continue
    m = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", ln)
    out.append(ln)
    if m: end = m.group(1)
text = "\n".join(out)

# simple assignments anywhere in the text (also inside a bash -c '...' string)
VARS = {}
for m in re.finditer(r"""(?:^|(?<=[\s;&|(`'"]))([A-Za-z_][A-Za-z0-9_]*)=(?:"([^"]*)"|'([^']*)'|([^\s;&|()`'"]+))""", text):
    val = next(g for g in (m.group(2), m.group(3), m.group(4)) if g is not None)
    VARS[m.group(1)] = val
def expand(s):
    return re.sub(r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))",
                  lambda m: VARS.get(m.group(1) or m.group(2), m.group(0)), s)

def ours(target):
    t = target.strip("'\"")
    if "$" in t: return True                       # unresolved variable: fail closed, as before
    if re.search(r"(?:^|/)(?:WEDNESDAY|FRIDAY|TUESDAY)(?:/|$)", t): return True
    if root and t.startswith("/"):
        n = os.path.normpath(t)
        return n == root or n.startswith(root + "/")
    return False

for seg in re.split(r"(?:\n|;|&&|\|\||\||\$\(|\bthen\b|\bdo\b)", text):
    s = expand(seg.strip())
    s = re.sub(r"^(?:bash|sh|zsh)\s+-c\s+['\"]?", "", s).lstrip("'\" ")
    if not re.match(r"^(?:env\s+[^g]*\s+)?git\b", s): continue
    mC = re.search(r"\s-C\s+(\"[^\"]*\"|'[^']*'|\S+)", s)
    if mC and not ours(mC.group(1)): continue
    autostash = re.search(r"(?<!no-)--autostash\b", s) or re.search(r"rebase\.autoStash=true", s, re.I)
    if re.search(r"\b(pull|rebase)\b", s) and autostash:
        why = "an autostash pull/rebase"
    elif re.search(r"\bstash\b", s) and re.search(r"0_Brain/dashboard/data/?(\s|$|'|\")", s):
        why = "a wholesale stash of 0_Brain/dashboard/data/"
    else:
        continue
    sp = f"{root}/2_Project_Files/tools/safe_pull.sh" if root else "2_Project_Files/tools/safe_pull.sh"
    print(f"REFUSED by pretooluse_no_autostash.sh: {why} on this seat's own repo ({root or 'cwd'}).\n"
          "It sweeps STATE (decisions.json, chat streams, Spark done.md) in with generated feeds — "
          f"ledger w=3, 2026-10-06.\nUse:  bash {sp} "
          "[--dry-run]   (commit your own files by pathspec first).", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
exit $?
