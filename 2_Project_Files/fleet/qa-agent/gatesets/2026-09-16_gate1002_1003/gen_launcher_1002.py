#!/usr/bin/env python3
"""gen_launcher_1002.py — derive launch_qa_secuura_ks1123_1002.sh from tonight's #999/#1000 tier-2 launcher
(launch_qa_secuura_ks1130_999_ks960_1000.sh) by ASSERTED substitutions (every anchor must occur exactly as often as
stated, or the generator refuses), collapsing its two heads to ONE and adding a develop arm (exit 18) because develop
had already moved past the PR's base when this gate was drafted. Then a RESIDUAL GUARD (any token of the source gate
left anywhere is a refusal), POSITIVE CONTROLS on the output, a heredoc apostrophe/paren check (macOS /bin/bash 3.2
scans quote state through a heredoc inside $( )), and `bash -n` on the candidate. Nothing is written on refusal.

Usage: gen_launcher_1002.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n or heredoc check failed
"""
import datetime
import hashlib
import re
import subprocess
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()
TEMPLATE_EXITS = sorted({int(x) for x in re.findall(r"exit (\d+)", s)})

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks1123_1002.sh — cross-project QA agent, ONE TIER 2 (through code) gate, ROUND 1, over Secuura/Blockchain
# PR #1002 (KS-1123, Seat A) @ a376756aba1e1ae32c49ed47ba057fd80c7ed136, branch feature/ks-1123-ornith-verify-status-pins —
# ONE commit on develop 80686962, 3 files under services/api-gateway: two new test files (F3 empty-string status, F2
# stale confidence) plus comment-only edits in routes/verification.ts (F1 reword, P1, P2). "Part of KS-1123".
#
# THE SHAPE, as read 22:36-22:40 AEST 2026-09-16 (git + the compare API agree): the head's parent is 80686962 = its
# merge-base with develop. Develop had ALREADY moved to 5b4f38a48 (#1001: csrf.ts + one api-gateway test, disjoint from
# #1002's files). The compare develop...head is asserted as merge_base + ahead + files (exit 10); `behind` is
# deliberately NOT asserted, so develop moving on does not trip it. A landed PR reads ahead=0 and refuses there.
#
# exit 18 (the develop arm): develop MAY move — the brief tells the gate to merge the then-current develop onto the head
# in its clone and re-derive — but a move that touches one of #1002's 3 files, the api-gateway vitest/tsconfig/package
# files or the Dev lockfile re-anchors the tampers or changes the substrate, so it refuses (as does an unjudgeable move).
#
# Adapted from launch_qa_secuura_ks1130_999_ks960_1000.sh by gen_launcher_1002.py (asserted substitutions, residual
# guard, positive controls, heredoc check, bash -n): the same guards and exit codes collapsed to ONE head — exit 6 (the
# head moved), exits 13/10 (compare unreadable / changed), exit 20 (brief or prompt does not name the head SHA),
# exit 21 (the LAUNCH path refuses a non-TTY stdin), exit 12 (the prompt must name wednesday-agent@agentmail.to) —
# plus exit 18 above.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1123_1002.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18, 20, 21 a guard refused
"""

marker = "set -u\n"
if s.count(marker) != 1:
    print("REFUSING: header marker count != 1", file=sys.stderr); sys.exit(1)
s = NEW_HEADER + s[s.index(marker):]

OLD_PINS = """BRANCH='refs/heads/feature/ks-1130-ornith-tier2-twin-cells'
HEAD_SHA="${QA999_HEAD:-91793e5d4f4d4b70eec93662c45555472e2bb8a6}"
BRANCH_1000='refs/heads/feature/ks-960-ornith-createuser-conflict-target-pin'
HEAD_1000="${QA1000_HEAD:-ab4a35d75d9b7611b4588ce88a792a489a124324}"
MERGE_BASE='0b25f823f6660ac52b665f14055799ff0c3b616d'   # the merge-base of BOTH heads with develop
"""
NEW_PINS = """BRANCH='refs/heads/feature/ks-1123-ornith-verify-status-pins'
HEAD_SHA="${QA1002_HEAD:-a376756aba1e1ae32c49ed47ba057fd80c7ed136}"
MERGE_BASE='80686962828197acf305e4010a2ed5b401285743'   # the head's parent = its merge-base with develop
DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'   # develop at draft time, #1001 merged (read 22:36:56 and 22:40:06 AEST)
"""

OLD_LSR = """# TWO heads, each pinned at its own branch on origin; a moved head names its PR (exit 6).
for pair in "999|$HEAD_SHA|$BRANCH" "1000|$HEAD_1000|$BRANCH_1000"; do
  PR_N="${pair%%|*}"; REST="${pair#*|}"; PR_HEAD="${REST%%|*}"; PR_BRANCH="${REST#*|}"
  if ! git -C "$REPO" ls-remote origin "$PR_BRANCH" | grep -q "^${PR_HEAD}[[:space:]]"; then
    echo "REFUSING: #$PR_N head $PR_HEAD is not at $PR_BRANCH on origin — the head moved; the brief is about a different SHA" >&2
    git -C "$REPO" ls-remote origin "$PR_BRANCH" >&2
    exit 6
  fi
done
"""
NEW_LSR = """# The head, pinned at its branch on origin (one ls-remote; exit 6).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\\$"; then
  echo "REFUSING: #1002 head $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\\n' "$LSR" >&2
  exit 6
fi
"""

OLD_MB = """# The merge-base, read once PER PR from the GitHub compare API (exit 13 unreadable, exit 10 changed).
for pair in "999|$HEAD_SHA" "1000|$HEAD_1000"; do
PR_N="${pair%%|*}"; PR_HEAD="${pair#*|}"
ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$PR_HEAD" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read #$PR_N's merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: #$PR_N merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }
done
"""
NEW_MB = """# The compare develop...head (GitHub compare API), asserted as merge_base + ahead + files; NOT behind (see the header).
# exit 13 unreadable, exit 10 changed.
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...#1002 from the GitHub compare API" >&2; exit 13; }
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=3" ] || { echo "REFUSING: #1002 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=3'" >&2; exit 10; }

# The develop arm (exit 18). Develop MAY move; a move touching a GUARDED path, or one that cannot be judged, refuses.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (the draft reading: #1001 merged, file-disjoint from #1002; the gate runs the merged tree)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__)
    raise SystemExit(0)
files = [f["filename"] for f in (c.get("files") or [])]
if c.get("status") != "ahead" or len(files) >= 300:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files)))
    raise SystemExit(0)
D = "Blockchain/Dev/"
GUARDED = [D + "services/api-gateway/src/routes/verification.ts",
           D + "services/api-gateway/src/__tests__/ks1123-f2-anchor-failed-stale-confidence.test.ts",
           D + "services/api-gateway/src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts",
           D + "services/api-gateway/vitest.config.ts",
           D + "services/api-gateway/vitest.setup.ts",
           D + "services/api-gateway/tsconfig.json",
           D + "services/api-gateway/package.json",
           D + "package-lock.json"]
hits = sorted(f for f in files if f in GUARDED)
if hits:
    print("GUARDED " + " ".join(hits))
    raise SystemExit(0)
print("OK origin develop MOVED %s -> %s: commits=%d files=%d, none on the GUARDED list; the gate merges the then-current develop onto the head in its clone and re-derives, brief D1 and item 3" % (os.environ["DEVELOP_SHA"][:9], os.environ["CUR_DEV"][:9], c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably clear of #1002: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief D1 + prompt)" >&2
       exit 18 ;;
  esac
fi
"""

OLD_SHAS = """for sha in "$HEAD_SHA" "$HEAD_1000"; do
  grep -qF "$sha" "$PROMPT_FILE" && grep -qF "$sha" "$BRIEF" \\
    || { echo "REFUSING: brief or prompt does not name the head SHA $sha — a gate about another SHA is another gate" >&2; exit 20; }
done
"""
NEW_SHAS = """grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
"""

OLD_CHK1 = """  echo "  #999 head $HEAD_SHA present at $BRANCH on origin"
  echo "  #1000 head $HEAD_1000 present at $BRANCH_1000 on origin"
  echo "  merge-base of both heads still $MERGE_BASE (GitHub compare API, one read per PR)"
"""
NEW_CHK1 = """  echo "  #1002 head $HEAD_SHA present at $BRANCH on origin"
  echo "  compare (GitHub API): develop...#1002 = $COMPARE"
  echo "  $DEV_NOTE"
"""
OLD_CHK2 = """  echo "  brief and prompt both name both head SHAs"
"""
NEW_CHK2 = """  echo "  brief and prompt both name the head SHA"
"""

OLD_OVR = """[ -z "${QA9991000_BRIEF:-}${QA9991000_PROMPT:-}${QA999_HEAD:-}${QA1000_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
"""
NEW_OVR = """[ -z "${QA1002_BRIEF:-}${QA1002_PROMPT:-}${QA1002_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
"""

subs = [
    (OLD_PINS, NEW_PINS, 1),
    (OLD_LSR, NEW_LSR, 1),
    (OLD_MB, NEW_MB, 1),
    (OLD_SHAS, NEW_SHAS, 1),
    (OLD_CHK1, NEW_CHK1, 1),
    (OLD_CHK2, NEW_CHK2, 1),
    (OLD_OVR, NEW_OVR, 1),
    ("QA9991000_BRIEF", "QA1002_BRIEF", 1),
    ("QA9991000_PROMPT", "QA1002_PROMPT", 1),
    ("2026-09-16_secuura-999-1000-ks1130-ks960-tier2", "2026-09-16_secuura-1002-ks1123-tier2", 3),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# Residual guard: tokens of the SOURCE gate. The header's one mention of the template file name is permitted.
body = s.replace("launch_qa_secuura_ks1130_999_ks960_1000.sh", "")
hits = []
for tok in ["91793e5d4", "ab4a35d75", "0b25f823f", "HEAD_1000", "BRANCH_1000", "QA999", "QA1000", "QA9991000",
            "1130", "twin", "createuser", "conflict-target", "PR_N", "PR_HEAD", "pair", "both head", "one read per PR",
            "999", "1000", "960"]:
    for m in re.finditer(re.escape(tok), body):
        hits.append((tok, body.count("\n", 0, m.start()) + 1))
if hits:
    for tok, line in hits:
        print(f"REFUSING: residual token {tok!r} at line {line}", file=sys.stderr)
    sys.exit(2)

# Positive controls on the output.
controls = [
    ("HEAD_SHA=\"${QA1002_HEAD:-a376756aba1e1ae32c49ed47ba057fd80c7ed136}\"", 1),
    ("MERGE_BASE='80686962828197acf305e4010a2ed5b401285743'", 1),
    ("DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'", 1),
    ("BRANCH='refs/heads/feature/ks-1123-ornith-verify-status-pins'", 1),
    ("\"$MERGE_BASE ahead=1 files=3\"", 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2),
    ("/briefs/2026-09-16_secuura-1002-ks1123-tier2.md", 2),
    ("/briefs/2026-09-16_secuura-1002-ks1123-tier2.prompt.txt", 1),
    ("grep -qF 'wednesday-agent@agentmail.to' \"$PROMPT_FILE\"", 1),
    ("[ -t 0 ] ||", 1),
    ("\nPY\n", 1), ("\nPYJ\n", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1),
    ("if [ \"${1:-}\" = \"--check\" ]; then", 1),
]
for needle, n in controls:
    c = s.count(needle)
    if c != n:
        print(f"REFUSING: output control {needle!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
# the --check branch must come AFTER every guard and BEFORE the TTY guard and the exec
i_check = s.index("if [ \"${1:-}\" = \"--check\" ]; then")
if not (s.rindex("exit 17") < i_check < s.index("[ -t 0 ] ||") < s.index("exec claude")):
    print("REFUSING: --check branch is not between the last guard and the TTY guard / exec", file=sys.stderr); sys.exit(1)
out_exits = sorted({int(x) for x in re.findall(r"exit (\d+)", s)})
if out_exits != sorted(set(TEMPLATE_EXITS) | {18}):
    print(f"REFUSING: exit codes {out_exits} != template {TEMPLATE_EXITS} + [18]", file=sys.stderr)
    sys.exit(1)

# Heredoc bodies inside $( ): no apostrophes, balanced parentheses (macOS /bin/bash 3.2).
for tag in ("PY", "PYJ"):
    m = re.search(r"<<'" + tag + r"'\n(.*?)\n" + tag + r"\n", s, re.S)
    if not m:
        print(f"REFUSING: heredoc {tag} not found", file=sys.stderr); sys.exit(3)
    hb = m.group(1)
    if "'" in hb or hb.count("(") != hb.count(")") or hb.count("[") != hb.count("]"):
        print(f"REFUSING: heredoc {tag}: apostrophes={hb.count(chr(39))} parens {hb.count('(')}/{hb.count(')')} brackets {hb.count('[')}/{hb.count(']')}", file=sys.stderr)
        sys.exit(3)

bn = subprocess.run(["/bin/bash", "-n"], input=s, text=True, capture_output=True)
if bn.returncode != 0:
    print(f"REFUSING: bash -n rc {bn.returncode}: {bn.stderr.strip()}", file=sys.stderr); sys.exit(3)

open(out_path, "w", encoding="utf-8").write(s)
now = datetime.datetime.now().astimezone().strftime("%H:%M:%S %Z")
print(f"{now} wrote {out_path} lines {s.count(chr(10))} sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]} "
      f"subs {len(subs)} controls {len(controls)} residual guard clean heredocs clean bash -n rc 0 exits {out_exits}")
