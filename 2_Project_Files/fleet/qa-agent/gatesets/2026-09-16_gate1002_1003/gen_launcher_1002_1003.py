#!/usr/bin/env python3
"""gen_launcher_1002_1003.py — derive launch_qa_secuura_ks1123_1002_ks1165_1003.sh from tonight's #999/#1000 tier-2
launcher (launch_qa_secuura_ks1130_999_ks960_1000.sh) by ASSERTED substitutions (every anchor must occur exactly as
often as stated, or the generator refuses). The two-head shape is kept; what changes: the two PRs have DIFFERENT bases,
so the compare is asserted PER PR as merge_base + ahead + files (not behind); and a develop arm (exit 18) is added,
because develop had already moved past #1002's base when this gate was drafted. Then a RESIDUAL GUARD (any token of the
source gate left anywhere is a refusal), POSITIVE CONTROLS on the output, a heredoc apostrophe/paren check (macOS
/bin/bash 3.2 scans quote state through a heredoc inside $( )), and `bash -n` on the candidate. Nothing is written on
refusal. Supersedes gen_launcher_1002.py (the single-PR generator, kept in gatesets/2026-09-16_gate1002/).

Usage: gen_launcher_1002_1003.py <template launcher> <output launcher>
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
# launch_qa_secuura_ks1123_1002_ks1165_1003.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on TWO
# test-only Secuura PRs in ONE pass, one verdict per PR (both Seat A, both services/api-gateway, no shared file):
#   PR #1002 (KS-1123) @ a376756ab, branch feature/ks-1123-ornith-verify-status-pins — two new test files (F3, F2) plus
#            comment-only edits in routes/verification.ts; one commit on develop 80686962; "Part of KS-1123";
#   PR #1003 (KS-1165) @ c5488a689, branch feature/ks-1165-f1-real-app-mount-cell — a real-app CSRF mount-order test
#            file plus a header fix in the merged composed ks1165 test; one commit on develop 5b4f38a48; "Closes KS-1165".
#
# THE SHAPE, as read 22:36-22:51 AEST 2026-09-16 (git + the compare API agree): the PRs have DIFFERENT bases. Each head's
# parent is its merge-base with develop (80686962 and 5b4f38a48). Develop is 5b4f38a48 (#1001 merged). The compare
# develop...head is asserted PER PR as merge_base + ahead + files (exits 13/10); `behind` is deliberately NOT asserted,
# so develop moving on does not trip it. A landed PR reads ahead=0 and refuses there.
#
# exit 18 (the develop arm): develop MAY move — the brief tells the gate to merge the then-current develop onto each
# head in its clone and re-derive — but a move that touches either PR's files, the files their tampers anchor in
# (routes/verification.ts, src/index.ts, middleware/csrf.ts, middleware/contentType.ts), the api-gateway
# vitest/tsconfig/package files or the Dev lockfile refuses, as does an unjudgeable move.
#
# Adapted from launch_qa_secuura_ks1130_999_ks960_1000.sh by gen_launcher_1002_1003.py (asserted substitutions, residual
# guard, positive controls, heredoc check, bash -n): the same guards and exit codes — exit 6 per head, exits 13/10 per
# PR, exit 20 (brief or prompt does not name a pinned head SHA), exit 21 (the LAUNCH path refuses a non-TTY stdin),
# exit 12 (the prompt must name wednesday-agent@agentmail.to) — plus exit 18 above.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1123_1002_ks1165_1003.sh [--check]
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
MERGE_BASE='80686962828197acf305e4010a2ed5b401285743'        # #1002: the head's parent = its merge-base with develop
BRANCH_1003='refs/heads/feature/ks-1165-f1-real-app-mount-cell'
HEAD_1003="${QA1003_HEAD:-c5488a6891e6ac6fe950c101196d8c33ab8e173f}"
MERGE_BASE_1003='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'   # #1003: the head's parent = its merge-base with develop
DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'       # develop at draft time, #1001 merged (read 22:36:56, 22:49:03, 22:51:05 AEST)
"""

OLD_LSR_HEAD = """# TWO heads, each pinned at its own branch on origin; a moved head names its PR (exit 6).
for pair in "999|$HEAD_SHA|$BRANCH" "1000|$HEAD_1000|$BRANCH_1000"; do
"""
NEW_LSR_HEAD = """# TWO heads, each pinned at its own branch on origin; a moved head names its PR (exit 6).
for pair in "1002|$HEAD_SHA|$BRANCH" "1003|$HEAD_1003|$BRANCH_1003"; do
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
NEW_MB = """# The compare develop...head, read PER PR from the GitHub compare API and asserted as merge_base + ahead + files
# (NOT behind; see the header). The two PRs have DIFFERENT bases. exit 13 unreadable, exit 10 changed.
COMPARES=""
for pair in "1002|$HEAD_SHA|$MERGE_BASE|3" "1003|$HEAD_1003|$MERGE_BASE_1003|2"; do
PR_N="${pair%%|*}"; REST="${pair#*|}"; PR_HEAD="${REST%%|*}"; REST="${REST#*|}"; PR_MB="${REST%%|*}"; PR_FILES="${REST#*|}"
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$PR_HEAD" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...#$PR_N from the GitHub compare API" >&2; exit 13; }
[ "$COMPARE" = "$PR_MB ahead=1 files=$PR_FILES" ] || { echo "REFUSING: #$PR_N develop...head reads '$COMPARE', brief pins '$PR_MB ahead=1 files=$PR_FILES'" >&2; exit 10; }
COMPARES="$COMPARES #$PR_N $COMPARE;"
done

# The develop arm (exit 18). Develop MAY move; a move touching a GUARDED path, or one that cannot be judged, refuses.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (the draft reading: #1001 merged; #1003 sits on it, #1002 is one merge behind and file-disjoint)"
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
A = "Blockchain/Dev/services/api-gateway/"
GUARDED = [A + "src/routes/verification.ts",
           A + "src/index.ts",
           A + "src/middleware/csrf.ts",
           A + "src/middleware/contentType.ts",
           A + "src/__tests__/ks1123-f2-anchor-failed-stale-confidence.test.ts",
           A + "src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts",
           A + "src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts",
           A + "src/__tests__/ks1165-real-app-csrf-mount-order.test.ts",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           A + "package.json",
           "Blockchain/Dev/package-lock.json"]
hits = sorted(f for f in files if f in GUARDED)
if hits:
    print("GUARDED " + " ".join(hits))
    raise SystemExit(0)
print("OK origin develop MOVED %s -> %s: commits=%d files=%d, none on the GUARDED list; the gate merges the then-current develop onto each head in its clone and re-derives, brief D1 and item 4" % (os.environ["DEVELOP_SHA"][:9], os.environ["CUR_DEV"][:9], c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably clear of #1002/#1003: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief D1 + prompt)" >&2
       exit 18 ;;
  esac
fi
"""

OLD_SHAS = """for sha in "$HEAD_SHA" "$HEAD_1000"; do
"""
NEW_SHAS = """for sha in "$HEAD_SHA" "$HEAD_1003"; do
"""

OLD_CHK1 = """  echo "  #999 head $HEAD_SHA present at $BRANCH on origin"
  echo "  #1000 head $HEAD_1000 present at $BRANCH_1000 on origin"
  echo "  merge-base of both heads still $MERGE_BASE (GitHub compare API, one read per PR)"
"""
NEW_CHK1 = """  echo "  #1002 head $HEAD_SHA present at $BRANCH on origin"
  echo "  #1003 head $HEAD_1003 present at $BRANCH_1003 on origin"
  echo "  compare develop...head (GitHub API, per PR):$COMPARES"
  echo "  $DEV_NOTE"
"""

OLD_OVR = """[ -z "${QA9991000_BRIEF:-}${QA9991000_PROMPT:-}${QA999_HEAD:-}${QA1000_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
"""
NEW_OVR = """[ -z "${QA10021003_BRIEF:-}${QA10021003_PROMPT:-}${QA1002_HEAD:-}${QA1003_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
"""

subs = [
    (OLD_PINS, NEW_PINS, 1),
    (OLD_LSR_HEAD, NEW_LSR_HEAD, 1),
    (OLD_MB, NEW_MB, 1),
    (OLD_SHAS, NEW_SHAS, 1),
    (OLD_CHK1, NEW_CHK1, 1),
    (OLD_OVR, NEW_OVR, 1),
    ("QA9991000_BRIEF", "QA10021003_BRIEF", 1),
    ("QA9991000_PROMPT", "QA10021003_PROMPT", 1),
    ("2026-09-16_secuura-999-1000-ks1130-ks960-tier2", "2026-09-16_secuura-1002-1003-ks1123-ks1165-tier2", 3),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# Residual guard: tokens of the SOURCE gate. The header's one mention of the template file name is permitted.
RESIDUAL = ["91793e5d4", "ab4a35d75", "0b25f823f", "HEAD_1000", "BRANCH_1000", "QA999", "QA1000", "QA9991000", "1130",
            "twin", "createuser", "conflict-target", "one read per PR", "ACTUAL_MB", "999", "1000", "960"]
body = s.replace("launch_qa_secuura_ks1130_999_ks960_1000.sh", "")
hits = []
for tok in RESIDUAL:
    for m in re.finditer(re.escape(tok), body):
        hits.append((tok, body.count("\n", 0, m.start()) + 1))
if hits:
    for tok, line in hits:
        print(f"REFUSING: residual token {tok!r} at line {line}", file=sys.stderr)
    sys.exit(2)

controls = [
    ("HEAD_SHA=\"${QA1002_HEAD:-a376756aba1e1ae32c49ed47ba057fd80c7ed136}\"", 1),
    ("HEAD_1003=\"${QA1003_HEAD:-c5488a6891e6ac6fe950c101196d8c33ab8e173f}\"", 1),
    ("MERGE_BASE='80686962828197acf305e4010a2ed5b401285743'", 1),
    ("MERGE_BASE_1003='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'", 1),
    ("DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'", 1),
    ("BRANCH='refs/heads/feature/ks-1123-ornith-verify-status-pins'", 1),
    ("BRANCH_1003='refs/heads/feature/ks-1165-f1-real-app-mount-cell'", 1),
    ("for pair in \"1002|$HEAD_SHA|$BRANCH\" \"1003|$HEAD_1003|$BRANCH_1003\"; do", 1),
    ("for pair in \"1002|$HEAD_SHA|$MERGE_BASE|3\" \"1003|$HEAD_1003|$MERGE_BASE_1003|2\"; do", 1),
    ("for sha in \"$HEAD_SHA\" \"$HEAD_1003\"; do", 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2),
    ("/briefs/2026-09-16_secuura-1002-1003-ks1123-ks1165-tier2.md", 2),
    ("/briefs/2026-09-16_secuura-1002-1003-ks1123-ks1165-tier2.prompt.txt", 1),
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
i_check = s.index("if [ \"${1:-}\" = \"--check\" ]; then")
if not (s.rindex("exit 17") < i_check < s.index("[ -t 0 ] ||") < s.index("exec claude")):
    print("REFUSING: --check branch is not between the last guard and the TTY guard / exec", file=sys.stderr); sys.exit(1)
out_exits = sorted({int(x) for x in re.findall(r"exit (\d+)", s)})
if out_exits != sorted(set(TEMPLATE_EXITS) | {18}):
    print(f"REFUSING: exit codes {out_exits} != template {TEMPLATE_EXITS} + [18]", file=sys.stderr)
    sys.exit(1)

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
      f"subs {len(subs)} controls {len(controls)} residual guard clean ({len(RESIDUAL)} tokens) heredocs clean bash -n rc 0 exits {out_exits}")
