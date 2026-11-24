#!/bin/bash
# pretooluse_clock_guard.sh — PreToolUse hook (matcher: Edit|Write|MultiEdit), Tuesday seat only: REFUSE a NEW typed
# clock estimate such as "12:5x" or "13:1X" written into the seat's own memory files.
#
# WHY (ledger _ledger_laptop_datasec.md 2026-11-18, s290, the typed-clock family, w=3 IN ONE SESSION): note_alone.sh and
# stamp_brief.py already refuse an "HH:Mx" clock, but the pickup, the ledger and the daily notes are also written through
# the Edit and Write tools, which had no such check. s290 wrote "12:2x" into a note, then "12:5x" and "13:5x" into the
# pickup, minutes after writing the stamp checklist whose item 7 forbids exactly that. A rule I must remember at the
# moment I am writing fastest is not a rule; this puts it in the path.
#
# REFUSES (exit 2): an Edit/MultiEdit/Write whose NEW text holds a token matching \b[0-2]?[0-9]:[0-5][xX]\b that the OLD
# text does not already hold (multiset difference), when the target is one of:
#   0_Brain/tasks/*.md · 0_Brain/learnings/_ledger*.md · 0_Brain/daily*/*.md
# ALLOWS: every other file; old history lines that already carry such a token (they are not new); a token on a line that
# also holds the literal "[quoted clock]" (a clock copied from someone else's artefact, as stamp_brief.py allows).
# SEAT-SCOPED: active only when the project tree's folder is TUESDAY (the same folder-name rule as
# pretooluse_inbox_scope.sh); on any other seat's tree it passes at once, so registering it in the shared
# settings.template.json changes nothing for Wednesday or Friday.
# FAIL-OPEN, stated: unparseable hook input -> pass, with a line on stderr saying the check did not run.
# Arms: 2_Project_Files/tuesday/tests/clock_guard_arms.sh
_TREE="${CLAUDE_PROJECT_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd -P)}"
case "$(basename "$_TREE")" in
  TUESDAY|Tuesday|tuesday) ;;
  *) exit 0 ;;
esac
exec python3 -I -c '
import json, re, sys, os
CLOCK = re.compile(r"\b[0-2]?[0-9]:[0-5][xX]\b")
TARGET = re.compile(r"/0_Brain/(tasks/[^/]+\.md|learnings/_ledger[^/]*\.md|daily[^/]*/[^/]+\.md)$")
try:
    data = json.load(sys.stdin)
except Exception:
    print("clock_guard: hook input unparseable; the check did NOT run", file=sys.stderr); sys.exit(0)
tool = data.get("tool_name", ""); ti = data.get("tool_input") or {}
fp = ti.get("file_path") or ""
if tool not in ("Edit", "Write", "MultiEdit") or not TARGET.search(fp):
    sys.exit(0)
def toks(s):
    out = []
    for line in (s or "").splitlines():
        if "[quoted clock]" in line:
            continue
        out += CLOCK.findall(line)
    return out
pairs = []
if tool == "Edit":
    pairs.append((ti.get("old_string", ""), ti.get("new_string", "")))
elif tool == "MultiEdit":
    for e in ti.get("edits") or []:
        pairs.append((e.get("old_string", ""), e.get("new_string", "")))
else:
    try:
        old = open(fp, encoding="utf-8", errors="replace").read() if os.path.exists(fp) else ""
    except Exception:
        old = ""
    pairs.append((old, ti.get("content", "")))
new_tokens = []
for old, new in pairs:
    pool = toks(old)
    for t in toks(new):
        if t in pool:
            pool.remove(t)
        else:
            new_tokens.append(t)
if new_tokens:
    print("REFUSED by pretooluse_clock_guard.sh: the new text holds a typed clock estimate " + repr(new_tokens) +
          " (ledger w=3, 2026-11-18). A clock for a done act is copied from `date` output or the artefact own stamp, or "
          "written as a bracket of known times (\"between 12:29:02 and 12:29:50\"). A clock quoted from another artefact: "
          "put [quoted clock] on that line. Nothing was written.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
'
