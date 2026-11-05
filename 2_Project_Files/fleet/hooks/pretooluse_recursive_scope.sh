#!/bin/bash
# pretooluse_recursive_scope.sh — PreToolUse hook (matcher: Bash): REFUSE an UNSCOPED recursive
# grep/find over the big trees: 0_Brain/reference, any 5_Project_History, local-model/ (spark/runs,
# night/). Scoped = grep carries --include=..., find carries -maxdepth N. Override: put the literal
# comment `# scope-ok: <reason>` in the command.
#
# WHY (ledger 2026-11-05 13:3x, w=3 = REGRESSION of the 11-02/11-03 rows): three times a recursive
# search over one of these trees ran for 30 min to 2.5 h (the harness backgrounds it at the 120 s
# timeout and it leaves the seat's view), holding load1 high while seats were building. The rule
# lived in ledger rows only and lost to a reflex each time. The pickup asked for an "advisory";
# an exit-0 hook's stderr never reaches the model, so an advisory would be invisible: this REFUSES
# (exit 2) with the fix, and the override keeps a deliberate wide search one comment away.
#
# Parse failure PASSES (fail-open on the instrument, stated) so a hook bug cannot brick Bash.
# Built 2026-11-05 by the 16:1x Wednesday seat (claim published first). Arms: tests/recursive_scope_arms.sh
INPUT=$(cat)
printf '%s' "$INPUT" | python3 -I -c '
import json, re, sys
try:
    cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
except Exception as e:
    print("pretooluse_recursive_scope: could not parse hook input: %s" % e, file=sys.stderr)
    sys.exit(0)
if "# scope-ok:" in cmd:
    sys.exit(0)
TREE = re.compile(r"(0_Brain/reference|5_Project_History|local-model(/|\b)|/night(/|\b)|spark/runs)")
hits = []
# split into simple commands on ; && || | and newlines
for seg in re.split(r"\|\||&&|;|\||\n", cmd):
    toks = seg.strip().split()
    if not toks:
        continue
    # skip leading env assignments
    i = 0
    while i < len(toks) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[i]):
        i += 1
    if i >= len(toks):
        continue
    prog = toks[i].rsplit("/", 1)[-1]
    rest = " ".join(toks[i+1:])
    if not TREE.search(rest):
        continue
    if prog in ("grep", "egrep", "rg", "ggrep"):
        flags = [t for t in toks[i+1:] if t.startswith("-")]
        recursive = prog == "rg" or any(
            t in ("--recursive", "--dereference-recursive") or
            (not t.startswith("--") and re.search(r"[rR]", t[1:])) for t in flags)
        if recursive and "--include" not in rest and "-g" not in flags and "--glob" not in rest:
            hits.append(seg.strip())
    elif prog in ("find", "bfs"):
        if "-maxdepth" not in rest:
            hits.append(seg.strip())
if hits:
    print("REFUSED by pretooluse_recursive_scope.sh: an UNSCOPED recursive search over a big tree "
          "(0_Brain/reference, 5_Project_History, local-model runs/night). Ledger 2026-11-05 w=3: these "
          "ran 30 min to 2.5 h in the background, unwatched.\n"
          "Fix: grep -> add --include=<glob> and name a small dir; find -> add -maxdepth N. "
          "A deliberate wide search: add the comment  # scope-ok: <reason>  and, if the harness "
          "backgrounds it, decide in the SAME turn to stop it by pid or say why it runs.\n"
          "Offending: " + " || ".join(h[:160] for h in hits), file=sys.stderr)
    sys.exit(2)
sys.exit(0)
'
exit $?
