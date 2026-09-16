#!/usr/bin/env python3
"""gen_launcher_999_1000.py — derive launch_qa_secuura_ks1130_999_ks960_1000.sh from the #960 (KS-1099) tier-2
launcher by ASSERTED substitutions (every anchor must occur exactly as often as stated, or the generator refuses),
then a RESIDUAL GUARD (any token of the source gate left anywhere is a refusal) and POSITIVE CONTROLS on the output.
Nothing is written on refusal.

Usage: gen_launcher_999_1000.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived
"""
import re
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()
TEMPLATE_EXITS = sorted({int(x) for x in re.findall(r"exit (\d+)", s)})

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks1130_999_ks960_1000.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# TWO test-only Secuura PRs in ONE pass, one verdict per PR:
#   PR #999  (KS-1130) @ 91793e5d4, branch feature/ks-1130-ornith-tier2-twin-cells — three tier-2 twin cells
#            plus comment-only edits, 5 files under services/api-gateway;
#   PR #1000 (KS-960)  @ ab4a35d75, branch feature/ks-960-ornith-createuser-conflict-target-pin — one new auth
#            test file, does NOT close its ticket.
# Both are one commit on develop 0b25f823f (develop's tip when drafted); they share no file.
#
# Adapted from launch_qa_secuura_ks1099_960.sh by gen_launcher_999_1000.py (asserted substitutions, residual
# guard, positive controls): the same guards and exit codes 2..17, widened to TWO heads — exit 6 (a head moved)
# and exits 13/10 (merge-base unreadable / changed) run once per PR and name the PR. Two guards are ADDED from
# the one-launcher-many-heads family (launch_qa_secuura_AUTH4_983_984_986_987.sh / launch_qa_secuura_ks1061_931.sh):
# exit 20 (brief or prompt does not name a pinned head SHA) and exit 21 (the LAUNCH path refuses a non-TTY stdin).
# Exit 12 is strengthened: the prompt must also name wednesday-agent@agentmail.to.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1130_999_ks960_1000.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..17, 20, 21 a guard refused
"""

marker = "set -u\n"
if s.count(marker) != 1:
    print("REFUSING: header marker count != 1", file=sys.stderr); sys.exit(1)
s = NEW_HEADER + s[s.index(marker):]

OLD_PINS = """BRANCH='refs/heads/feature/ks-1099-a-malformed-k6-yaml-config-prints-secrets-file-lines-to'
HEAD_SHA="${QA960_HEAD:-0e70ed1c77e1f832a4ab165152e024926be509a0}"
MERGE_BASE='4554b25e21dfd01113bf40e8f6d34573345a5f37'
"""
NEW_PINS = """BRANCH='refs/heads/feature/ks-1130-ornith-tier2-twin-cells'
HEAD_SHA="${QA999_HEAD:-91793e5d4f4d4b70eec93662c45555472e2bb8a6}"
BRANCH_1000='refs/heads/feature/ks-960-ornith-createuser-conflict-target-pin'
HEAD_1000="${QA1000_HEAD:-ab4a35d75d9b7611b4588ce88a792a489a124324}"
MERGE_BASE='0b25f823f6660ac52b665f14055799ff0c3b616d'   # the merge-base of BOTH heads with develop
"""

OLD_LSR = """if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi
"""
NEW_LSR = """# TWO heads, each pinned at its own branch on origin; a moved head names its PR (exit 6).
for pair in "999|$HEAD_SHA|$BRANCH" "1000|$HEAD_1000|$BRANCH_1000"; do
  PR_N="${pair%%|*}"; REST="${pair#*|}"; PR_HEAD="${REST%%|*}"; PR_BRANCH="${REST#*|}"
  if ! git -C "$REPO" ls-remote origin "$PR_BRANCH" | grep -q "^${PR_HEAD}[[:space:]]"; then
    echo "REFUSING: #$PR_N head $PR_HEAD is not at $PR_BRANCH on origin — the head moved; the brief is about a different SHA" >&2
    git -C "$REPO" ls-remote origin "$PR_BRANCH" >&2
    exit 6
  fi
done
"""

OLD_MB = """ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
"""
NEW_MB = """# The merge-base, read once PER PR from the GitHub compare API (exit 13 unreadable, exit 10 changed).
for pair in "999|$HEAD_SHA" "1000|$HEAD_1000"; do
PR_N="${pair%%|*}"; PR_HEAD="${pair#*|}"
ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$PR_HEAD" python3 - <<'PY'
"""
OLD_MB_TAIL = """[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read the merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }
"""
NEW_MB_TAIL = """[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read #$PR_N's merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: #$PR_N merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }
done
"""

OLD_BRIEFNAME = """grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
"""
NEW_BRIEFNAME = OLD_BRIEFNAME + """for sha in "$HEAD_SHA" "$HEAD_1000"; do
  grep -qF "$sha" "$PROMPT_FILE" && grep -qF "$sha" "$BRIEF" \\
    || { echo "REFUSING: brief or prompt does not name the head SHA $sha — a gate about another SHA is another gate" >&2; exit 20; }
done
"""

OLD_MAIL = """grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
"""
NEW_MAIL = """grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict to wednesday-agent@agentmail.to" >&2; exit 12; }
"""

OLD_CHK1 = """  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
"""
NEW_CHK1 = """  echo "  #999 head $HEAD_SHA present at $BRANCH on origin"
  echo "  #1000 head $HEAD_1000 present at $BRANCH_1000 on origin"
  echo "  merge-base of both heads still $MERGE_BASE (GitHub compare API, one read per PR)"
"""
OLD_CHK2 = """  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
"""
NEW_CHK2 = """  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name both head SHAs"
  echo "  prompt tells the agent to MAIL its verdict to wednesday-agent@agentmail.to"
"""
OLD_CHK3 = """  echo "  prompt forbids printing a credential value"
  exit 0
"""
NEW_CHK3 = """  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
"""

OLD_OVR = """[ -z "${QA960_BRIEF:-}${QA960_PROMPT:-}${QA960_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
"""
NEW_OVR = """[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ -z "${QA9991000_BRIEF:-}${QA9991000_PROMPT:-}${QA999_HEAD:-}${QA1000_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
"""

subs = [
    (OLD_PINS, NEW_PINS, 1),
    (OLD_LSR, NEW_LSR, 1),
    (OLD_MB, NEW_MB, 1),
    (OLD_MB_TAIL, NEW_MB_TAIL, 1),
    (OLD_BRIEFNAME, NEW_BRIEFNAME, 1),
    (OLD_MAIL, NEW_MAIL, 1),
    (OLD_CHK1, NEW_CHK1, 1),
    (OLD_CHK2, NEW_CHK2, 1),
    (OLD_CHK3, NEW_CHK3, 1),
    (OLD_OVR, NEW_OVR, 1),
    ("QA960_BRIEF", "QA9991000_BRIEF", 1),
    ("QA960_PROMPT", "QA9991000_PROMPT", 1),
    ("2026-09-12_secuura-960-ks1099-tier2", "2026-09-16_secuura-999-1000-ks1130-ks960-tier2", 3),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# Residual guard: tokens of the SOURCE gate. The header's one mention of the template file name is permitted.
body = s.replace("launch_qa_secuura_ks1099_960.sh", "")
hits = []
for tok in ["0e70ed1c7", "4554b25e2", "1099", "QA960", "yaml", "YAML", "k6", "secrets-file", "malformed"]:
    for m in re.finditer(re.escape(tok), body):
        hits.append((tok, body.count("\n", 0, m.start()) + 1))
# A bare 960 is the source PR; KS-960 / ks-960 / ks960 are this gate's ticket and are allowed.
for m in re.finditer(r"(?<![Kk][Ss]-)(?<![Kk][Ss])960", body):
    hits.append(("960", body.count("\n", 0, m.start()) + 1))
if hits:
    for tok, line in hits:
        print(f"REFUSING: residual token {tok!r} at line {line}", file=sys.stderr)
    sys.exit(2)

# Positive controls on the output.
controls = [
    ("HEAD_SHA=\"${QA999_HEAD:-91793e5d4f4d4b70eec93662c45555472e2bb8a6}\"", 1),
    ("HEAD_1000=\"${QA1000_HEAD:-ab4a35d75d9b7611b4588ce88a792a489a124324}\"", 1),
    ("MERGE_BASE='0b25f823f6660ac52b665f14055799ff0c3b616d'", 1),
    ("BRANCH='refs/heads/feature/ks-1130-ornith-tier2-twin-cells'", 1),
    ("BRANCH_1000='refs/heads/feature/ks-960-ornith-createuser-conflict-target-pin'", 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2),
    ("/briefs/2026-09-16_secuura-999-1000-ks1130-ks960-tier2.md", 2),
    ("/briefs/2026-09-16_secuura-999-1000-ks1130-ks960-tier2.prompt.txt", 1),
    ("\nPY\n", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1),
]
for needle, n in controls:
    c = s.count(needle)
    if c != n:
        print(f"REFUSING: output control {needle!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
out_exits = sorted({int(x) for x in re.findall(r"exit (\d+)", s)})
if out_exits != sorted(set(TEMPLATE_EXITS) | {20, 21}):
    print(f"REFUSING: exit codes {out_exits} != template {TEMPLATE_EXITS} + [20, 21]", file=sys.stderr)
    sys.exit(1)

open(out_path, "w", encoding="utf-8").write(s)
print(f"written {out_path} ({len(s)} bytes); {len(subs)} substitutions asserted; residual guard clean; "
      f"{len(controls)} output controls pass; exits {out_exits}")
