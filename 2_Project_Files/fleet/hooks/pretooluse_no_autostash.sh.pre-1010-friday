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
# REFUSES (exit 2), only at a git command aimed at this repo (no -C, or -C naming WEDNESDAY or a $VAR):
#   git … pull … --autostash | -c rebase.autoStash=true      git … rebase … --autostash
#   git … stash (push|save)? … 0_Brain/dashboard/data[/]   (the whole folder; named files are fine)
# IGNORES: text inside heredoc bodies (briefs may quote the command), `--no-autostash`.
# NOT COVERED, stated: tools that pull internally (safe_push.sh:108, wed_claim.sh:54 still use
# `rebase --autostash`; shared with Tuesday/Friday — owed in NEXT-PICKUP). Fail-open on a parse error.
INPUT=$(cat)
printf '%s' "$INPUT" | python3 -I -c '
import json, re, sys
try:
    cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
except Exception as e:
    print(f"pretooluse_no_autostash: parse error, passing: {e}", file=sys.stderr); sys.exit(0)
# drop heredoc bodies
lines, out, end = cmd.split("\n"), [], None
for ln in lines:
    if end is not None:
        if ln.strip() == end: end = None
        continue
    m = re.search(r"<<-?\s*[\x27\"]?([A-Za-z_][A-Za-z0-9_]*)[\x27\"]?", ln)
    out.append(ln)
    if m: end = m.group(1)
text = "\n".join(out)
for seg in re.split(r"(?:\n|;|&&|\|\||\||\$\(|\bthen\b|\bdo\b)", text):
    s = seg.strip()
    if not re.match(r"^(?:env\s+[^g]*\s+)?git\b", s): continue
    mC = re.search(r"\s-C\s+(\"[^\"]*\"|\x27[^\x27]*\x27|\S+)", s)
    target = mC.group(1) if mC else ""
    if mC and "WEDNESDAY" not in target and "$" not in target: continue
    autostash = re.search(r"(?<!no-)--autostash\b", s) or re.search(r"rebase\.autoStash=true", s, re.I)
    if re.search(r"\b(pull|rebase)\b", s) and autostash:
        why = "an autostash pull/rebase"
    elif re.search(r"\bstash\b", s) and re.search(r"0_Brain/dashboard/data/?(\s|$|\x27|\")", s):
        why = "a wholesale stash of 0_Brain/dashboard/data/"
    else:
        continue
    print(f"REFUSED by pretooluse_no_autostash.sh: {why} on the WEDNESDAY repo.\n"
          "It sweeps STATE (decisions.json, chat streams, Spark done.md) in with generated feeds — "
          "ledger w=3, 2026-10-06.\nUse:  bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/safe_pull.sh "
          "[--dry-run]   (commit your own files by pathspec first).", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
'
exit $?
