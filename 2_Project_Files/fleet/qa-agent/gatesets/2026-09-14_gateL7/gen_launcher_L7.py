#!/usr/bin/env python3
"""gen_launcher_L7.py — generate launch_qa_secuura_L7_918r2_924_925.sh from the INSTALLED #903 round-2 launcher (the newest
tier-2 exemplar; sha256 asserted) by ASSERTED substitutions and ASSERTED block replacements. Every anchor must occur exactly
once in the template; every replaced block is named; the residual (the files-present guards, the brief/prompt agreement guards,
the prompt-clause guards, the TTY guard, the override guard, the cd and the exec) is asserted byte-identical to the template
after generation; output controls are counted. Prints the post-header diff to gen_postheader.diff.
What changes vs the template: THREE heads on THREE branches (exit 6 each); FIVE stack compares (exit 10: #918 and #925 vs M18,
#924 vs its own base d4cf7e3cf, #918 -> #925 and #903 -> #925 by ancestry); the develop pin = M20 a53343502 (#903's SQUASH)
judged by CONTENT on SEVEN files + a GUARDED list for the rest of the move (exit 18; exit 22 when #925 has LANDED — the whole
stack is in and there is nothing left to gate but #924); TWO round-1 records (exit 19: Peter's saved #918 review AND the s161
report); the head-SHA-in-both guard over all three heads (exit 20); the same TTY guard (exit 21).
Usage: gen_launcher_L7.py <OUTPUT DIR>
"""
import hashlib, sys, os, subprocess, difflib
G = sys.argv[1]
TEMPLATE = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate903r2/launch_qa_secuura_ks991_903_r2.sh'
INSTALLED = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks991_903_r2.sh'
OUT = f"{G}/launch_qa_secuura_L7_918r2_924_925.sh"
t = open(TEMPLATE, encoding='utf-8').read()
h = hashlib.sha256(t.encode()).hexdigest()[:16]
assert h == 'ccf1864168e7831a', f"template sha {h} != ccf1864168e7831a (the gate903r2 launcher as built)"
if os.path.exists(INSTALLED):
    hi = hashlib.sha256(open(INSTALLED, 'rb').read()).hexdigest()[:16]
    print(f"installed #903 r2 launcher sha {hi} ({'= template' if hi == h else 'DIFFERS from the template — the set copy is the exemplar'})")
subs = 0
def sub(old, new, count=1):
    global t, subs
    n = t.count(old); assert n == count, f"anchor occurs {n} times, expected {count}: {old[:70]!r}"
    t = t.replace(old, new); subs += 1
def block(start, end, new, name):
    """replace the region from the line containing `start` through the line containing `end` (inclusive) with `new`."""
    global t, subs
    assert t.count(start) == 1 and t.count(end) == 1, f"block anchors not unique: {name}"
    i = t.index(start); i = t.rfind('\n', 0, i) + 1
    j = t.index(end) + len(end); j = t.index('\n', j) + 1     # through the END of a multi-line anchor, then its newline
    assert i < j, name
    t = t[:i] + new + t[j:]; subs += 1
    print(f"block replaced: {name}")

# ---- 1. the header (everything above `set -u`) ------------------------------------------------------------------------------
hdr_end = t.index('set -u\n')
header = '''#!/bin/bash
# launch_qa_secuura_L7_918r2_924_925.sh — cross-project QA agent, ONE TIER 2 (through code: shell scripts under
# Blockchain/Dev/scripts/ + the pre-push hook and its test that #925 carries from #903 — no service, route, spec, schema or UI)
# pass over THREE Secuura PRs of LANE L7, three verdicts, one report, one mail:
#   #918 (KS-926) ROUND 2 @ b54487216 — Peter's one ask answered: check-environment.sh out of WIRED into DEFERRED in
#        run-code-guards.sh (a reason string with no backtick / $ / inner quote — the s213 docker-info incident), the 21st guard
#        homed, the develop merge 21368d250 resolved to 15 legs (carries no fix), ruling 4(a)'s ONE fixture line. 3 commits, 4 files.
#   #924 (KS-773) RE-GATE @ b85f1db24 — UNCHANGED since 2026-09-09 (no code this round): lockfile-cleanroom.sh 35/35 on bash 3.2.57
#        at the head AND on the merged tree; F-924-1 red-first from s214's BEFORE/AFTER/CONTROL lines. 3 commits, 1 file.
#   #925 (KS-1046) RE-GATE @ 5341b1dae, STACKED on #918 b54487216 AND #903 a4f71cde6 by merge commit — the honest INCOMPLETE
#        verdict; rulings 4(b) (the leg-14 oracle widened at preflight_deps.test.sh:427) / 4(c) (PREFLIGHT_STRICT_LEGS=0 pinned on
#        the nested run at :409) / 2 (F-925-3: step() checks each header's denominator against TOTAL_LEGS). 14 commits, 6 files.
#
# DEVELOP = M20 a5334350221c819f54d4a20a3308daeb9ca09617 = #903's SQUASH (23:18:09Z 2026-09-13; read 10:35 and 10:46 AEST
# 2026-09-14). A squash: a4f71cde6 is NOT an ancestor of M20, but M20's three #903 files are BYTE-IDENTICAL to #903's head
# (pre-push 1b22d4e14 · pre_push_hook_base.test.sh affdf027b · preflight.sh 0727300f7). The merge-base of #918 and #925 with M20
# is STILL M18 8861e6216, so #925's merge onto develop is a 3-way from M18 with #903's hunk on BOTH sides: the drafter's
# merge-tree (gateL7/mt_*.out) reads #918 onto M20 CLEAN (tree f089eaffe, 4 files), #924 onto M20 CLEAN (tree 4641202fd), and
# #925 onto M20 or onto M20+#918 CONFLICTING in preflight.sh ONLY (1 block / 3 blocks), every block resolved by taking #925's
# side — the resolved file is byte-identical to #925's head blob 28d3636c1 and the resolved tree is 364e44ca1 in EITHER order.
# GitHub agrees: #925 reads mergeable false / dirty since M20 (it was true / unstable at the READY); #918 true / unstable;
# #924 true / clean. The brief carries this for the merge seat; the gate re-derives it.
#
# The develop pin is judged by CONTENT (the #984 pattern), not bare: SEVEN files are read at origin develop through the contents
# API — preflight.sh (0727300f7 = M20 ok · 8840ac661 = #918 landed, ok, noted · 28d3636c1 = #925 landed -> exit 22),
# preflight_deps.test.sh (a713a94e7 · 343f24a6e #918 landed · 5ad054131 #925 landed -> 22), run-code-guards.sh (absent ·
# 2f06e19d3 #918 landed), run_code_guards.test.sh (absent · 55a376f76), lockfile-cleanroom.sh (26e7feb2b · 518bffeea = #924
# landed, ok, noted), .githooks/pre-push (1b22d4e14), pre_push_hook_base.test.sh (affdf027b) — any OTHER blob -> exit 18. Then
# the M20..current compare: any file under Blockchain/Dev/scripts/__tests__/ (the leg-14 count), scripts/preflight/, scripts/check-*
# (the census 21), .githooks/, deps-present.sh or run-shell-suites.sh -> exit 18; otherwise the move is printed and the gate
# re-states it (brief TARGET + each section's item 6). A refusal means: confirm the delta, then re-pin DEVELOP_SHA here AND in the
# brief's TARGET AND the prompt — a different brief, a deliberate edit.
#
# Round 1 (exit 19, TWO records, both on disk): Peter's #918 review 5151452193 saved at
# 5_Project_History/2026-09-13_s213/boot/peter_918_review_5151452193.md, and the s161 batch report of 2026-09-09 (#924 @ 1497b39de,
# #925 @ 0956c3dbe) at Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md.
#
# Exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit pane,
# never inside a Bash tool — a gate launched there runs headless, invisible to Kam, and dies with the caller's shell (2026-09-13
# ledger). `--check` still runs headless (it launches nothing).
#
# Adapted from the #903 round-2 launcher (sha ccf1864168e7831a) by gen_launcher_L7.py (asserted substitutions and block
# replacements, residual guard): the same guard family and exit codes 2..21 plus 22 (a PR of the stack has LANDED).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_L7_918r2_924_925.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
'''
t = header + t[hdr_end:]; subs += 1
print("block replaced: header")

# ---- 2. the variable block ------------------------------------------------------------------------------------------------
block("BRIEF=\"${QA903R2_BRIEF:-", "REAL_BRIEF=\"$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.md\"", '''MODE="${1:-}"                                            # captured FIRST: the head-guard loop below uses `set --` (the first --check read 21 — check.first-run-*.out)
BRIEF="${QAL7_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.md}"
PROMPT_FILE="${QAL7_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH_918='refs/heads/feature/ks-926-wire-unreachable-guards'
BRANCH_924='refs/heads/kamilkreiser/ks-773-cleanroom-skip-mcp-server'
BRANCH_925='refs/heads/feature/ks-1046-preflight-passed-is-printed-identically-whether-13-legs-ran'
HEAD_918="${QAL7_HEAD918:-b54487216ebb49f1de7ed9349f089d92a3e5bfc1}"
HEAD_924="${QAL7_HEAD924:-b85f1db24596a5e0ce98fe2b1343d9f515a1a995}"
HEAD_925="${QAL7_HEAD925:-5341b1daed8afe4254e05ef66ef4350fd8220d4f}"
HEAD_903='a4f71cde660c1442d98317e26d93845340b20098'     # merged as M20 — pinned only as #925's stack parent (ancestry)
M18='8861e62161466c40f08d2b10a30edeb203123993'          # the merge-base of #918 / #925 / #903 with develop (unchanged by the squash)
BASE_924='d4cf7e3cf73e91422a229b7d0767cf6c3a04fe57'     # #924's own merge-base with develop
DEVELOP_SHA='a5334350221c819f54d4a20a3308daeb9ca09617'  # M20 = #903's squash
# the SEVEN content-judged files at develop: ok blobs (M20's, or a stack member landed in order) · the blob that means #925 LANDED
JUDGED='Blockchain/Dev/scripts/preflight/preflight.sh=0727300f79938fd26b578ed77fca281e49662c6f:M20,8840ac6619a9e4d967373c338a7bd03f768b7b41:#918-landed,28d3636c13a4259bbdade8b15ac527cbe93742c3:LANDED925
Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh=a713a94e7cffd22fc6429f8c877bb9c98736a32c:M20,343f24a6ef1d68f56edafe68e177fe1296fb020f:#918-landed,5ad0541313589635c6c100677cf14fb02d00be78:LANDED925
Blockchain/Dev/scripts/run-code-guards.sh=ABSENT:M20,2f06e19d3d33d649d7229e44ade8a35c0df3a0db:#918-landed
Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh=ABSENT:M20,55a376f769e078ceeeadc25d026364c0e06961b1:#918-landed
Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh=26e7feb2b9764256beb8171fb10a734e1af326e7:M20,518bffeeaf4a3c47a4660f594f822f34e26c2d15:#924-landed
.githooks/pre-push=1b22d4e146487aa25698310b353152a7d09986b5:M20
Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh=affdf027bff11e3690d374e902e3e93274788c62:M20'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.md"
''', "variables")

# ---- 3. the head guard: three heads on three branches (exit 6) ----------------------------------------------------------------
block('if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then', '  exit 6\nfi', '''for pair in "$HEAD_918 $BRANCH_918 918" "$HEAD_924 $BRANCH_924 924" "$HEAD_925 $BRANCH_925 925"; do
  set -- $pair
  if ! git -C "$REPO" ls-remote origin "$2" | grep -q "^${1}[[:space:]]"; then
    echo "REFUSING: $1 is not at $2 on origin — #$3's head moved; the brief is about a different SHA" >&2
    git -C "$REPO" ls-remote origin "$2" >&2
    exit 6
  fi
done
''', "head guard x3")

# ---- 4. the merge-base guard -> five stack compares (exit 10 / 13) ------------------------------------------------------------
block('ACTUAL_MB="$(', '[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now \'$ACTUAL_MB\', brief says \'$MERGE_BASE\'" >&2; exit 10; }', '''# The stack, pinned through the GitHub compare API: each line is "<base>...<head> merge_base ahead files" as the brief states it.
STACK_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_918="$HEAD_918" HEAD_924="$HEAD_924" HEAD_925="$HEAD_925" HEAD_903="$HEAD_903" M18="$M18" BASE_924="$BASE_924" python3 - <<'PY'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
E = os.environ
for a, b in [(E["M18"], E["HEAD_918"]), (E["M18"], E["HEAD_925"]), (E["BASE_924"], E["HEAD_924"]), (E["HEAD_918"], E["HEAD_925"]), (E["HEAD_903"], E["HEAD_925"])]:
    try:
        c = json.load(urllib.request.urlopen(urllib.request.Request(api + a + "..." + b, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    except Exception as e:
        print("UNREADABLE " + type(e).__name__); sys.exit(0)
    print("%s %s %d %d" % (b[:9], c["merge_base_commit"]["sha"][:9], c["ahead_by"], len(c.get("files") or [])))
PY
)"
case "$STACK_READ" in UNREADABLE*|"") echo "REFUSING: could not read the stack compares from the GitHub compare API: ${STACK_READ:-empty}" >&2; exit 13 ;; esac
STACK_WANT="$(printf '%s\\n' "${HEAD_918:0:9} ${M18:0:9} 3 4" "${HEAD_925:0:9} ${M18:0:9} 14 6" "${HEAD_924:0:9} ${BASE_924:0:9} 3 1" "${HEAD_925:0:9} ${HEAD_918:0:9} 11 4" "${HEAD_925:0:9} ${HEAD_903:0:9} 10 4")"
[ "$STACK_READ" = "$STACK_WANT" ] || { printf 'REFUSING: the stack is not what the brief pins (head merge_base ahead files):\\n--- read\\n%s\\n--- brief\\n%s\\n' "$STACK_READ" "$STACK_WANT" >&2; exit 10; }
''', "stack compares x5")

# ---- 5. the develop guard -> content-judged on seven files + the GUARDED list (exit 18 / 22) ---------------------------------------
block('# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.', '''       exit 18 ;;
  esac
fi''', '''# The develop pin, judged by CONTENT on the seven L7 files (see the header), then by the GUARDED list over the rest of the move.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" JUDGED="$JUDGED" python3 - <<'PYJ'
import json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
judged = {}
for line in os.environ["JUDGED"].splitlines():
    path, spec = line.split("=", 1)
    judged[path] = [tuple(x.split(":", 1)) for x in spec.split(",")]
state = []; landed925 = []; other = []
for path, okl in judged.items():
    try:
        blob = get("/contents/" + path + "?ref=" + cur)["sha"]
    except urllib.error.HTTPError as e:
        if e.code == 404: blob = "ABSENT"
        else: print("UNJUDGEABLE develop blob unreadable: HTTP %d on %s" % (e.code, path)); sys.exit(0)
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable: " + type(e).__name__); sys.exit(0)
    label = dict(okl).get(blob)
    short = path.split("/")[-1] + " " + blob[:9]
    if label is None: other.append(short)
    elif label == "LANDED925": landed925.append(short)
    else: state.append(short + " (" + label + ")")
if landed925:
    print("LANDED925 " + ", ".join(landed925) + " — #925 (and with it #918) has landed on develop; nothing left to gate but #924 — re-issue a #924-only gate"); sys.exit(0)
if other:
    print("GUARDED develop carries a version nobody pinned: " + ", ".join(other)); sys.exit(0)
st = "; ".join(state)
if cur == pinned:
    print("OK origin develop still " + pinned + " (M20 = #903's squash; git ls-remote) | judged files: " + st); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/scripts/preflight/deps-present.sh",
           "Blockchain/Dev/scripts/run-shell-suites.sh",
           "Blockchain/Dev/scripts/__tests__/",
           "Blockchain/Dev/scripts/preflight/",
           "Blockchain/Dev/scripts/check-",
           ".githooks/"]
hits = sorted({f["filename"] for f in files if f["filename"] not in judged for g in GUARDED if f["filename"] == g or (not g.endswith(".sh") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("OK origin develop MOVED %s -> %s: commits=%d files=%d — the seven judged files are at pinned versions (%s) and the rest of the move is disjoint from the guard's six paths (deps-present.sh, run-shell-suites.sh, scripts/__tests__/, scripts/preflight/, scripts/check-*, .githooks/); the gate reads develop at start and end and re-derives the merged shapes onto it (brief TARGET + items 6)" % (pinned, cur, c["ahead_by"], len(files), st)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED925*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED925 } (develop $CUR_DEV)" >&2; exit 22 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA/JUDGED + brief TARGET + prompt)" >&2
     exit 18 ;;
esac''', "develop guard (content-judged)")

# ---- 6. the round guard: ROUND 2 AND RE-GATE both named ------------------------------------------------------------------------
sub("grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round\" >&2; exit 15; }",
    "grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\" && grep -q 'RE-GATE' \"$BRIEF\" && grep -q 'RE-GATE' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the rounds (#918 ROUND 2; #924/#925 RE-GATE)\" >&2; exit 15; }")
# ---- 7. the head-SHA-in-both guard over three heads (exit 20) -------------------------------------------------------------------
sub('''grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }''',
    '''for h in "$HEAD_918" "$HEAD_924" "$HEAD_925"; do
  grep -qF "$h" "$PROMPT_FILE" && grep -qF "$h" "$BRIEF" \\
    || { echo "REFUSING: brief or prompt does not name the head SHA $h — a gate about another SHA is another gate" >&2; exit 20; }
done''')
# ---- 8. the round-1 records (exit 19), two of them ---------------------------------------------------------------------------------
block("R1_REPORT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_903_comment_5585854866.md'",
      '[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 record named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }',
      '''R1_918='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_918_review_5151452193.md'
R1_S161='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md'
for r in "$R1_918" "$R1_S161"; do
  grep -qF "$r" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 record path $r (a gate cannot ask)" >&2; exit 19; }
  [ -s "$r" ] || { echo "REFUSING: the round-1 record named by the brief is missing or empty: $r" >&2; exit 19; }
done
''', "round-1 records x2")
# ---- 9. the --check block ---------------------------------------------------------------------------------------------------------
block('  echo "  head $HEAD_SHA present at $BRANCH on origin"', "  echo \"  brief names the round-1 record (Peter's review) and it is present on disk\"", '''  echo "  head #918 $HEAD_918 present at $BRANCH_918 on origin"
  echo "  head #924 $HEAD_924 present at $BRANCH_924 on origin"
  echo "  head #925 $HEAD_925 present at $BRANCH_925 on origin"
  echo "  the stack holds (GitHub compare API): #918 and #925 on M18 (3 commits / 4 files; 14 / 6), #924 on d4cf7e3cf (3 / 1), #925 contains #918 (ahead 11 / 4 files) and #903 (ahead 10 / 4 files)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2, ROUND 2 (#918) and RE-GATE (#924, #925)"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the three head SHAs"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  brief names both round-1 records (Peter's #918 review; the s161 report) and both are present on disk"
''', "--check block")
# ---- 9b. the --check test reads the captured MODE (the head loop's `set --` consumed $1) ------------------------------------------
sub('if [ "${1:-}" = "--check" ]; then', 'if [ "$MODE" = "--check" ]; then')
# ---- 10. the override guard names the L7 overrides -----------------------------------------------------------------------------------
sub('[ -z "${QA903R2_BRIEF:-}${QA903R2_PROMPT:-}${QA903R2_HEAD:-}" ]', '[ -z "${QAL7_BRIEF:-}${QAL7_PROMPT:-}${QAL7_HEAD918:-}${QAL7_HEAD924:-}${QAL7_HEAD925:-}" ]')

# ---- residual guard: the untouched lines of the template must survive byte-for-byte ------------------------------------------------
RESIDUAL = ['[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }',
            '[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }',
            '[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }',
            '[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }',
            "grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the tier\" >&2; exit 7; }",
            "head -1 \"$PROMPT_FILE\" | grep -q 'ultrathink' || { echo \"REFUSING: prompt does not open with the thinking directive\" >&2; exit 8; }",
            'grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }',
            "grep -qi 'MAIL YOUR VERDICT' \"$PROMPT_FILE\" || { echo \"REFUSING: prompt does not tell the agent to MAIL its verdict\" >&2; exit 12; }",
            "grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' \"$PROMPT_FILE\" \\\n  || { echo \"REFUSING: prompt does not forbid pushing / running the hook in the real checkout\" >&2; exit 11; }",
            "grep -qi 'no memory maintenance' \"$PROMPT_FILE\" \\\n  || { echo \"REFUSING: prompt does not forbid memory maintenance inside the gate session\" >&2; exit 14; }",
            "grep -qi 'NEVER print a credential value' \"$PROMPT_FILE\" \\\n  || { echo \"REFUSING: prompt does not forbid printing a credential value\" >&2; exit 17; }",
            '[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller\'s shell)" >&2; exit 21; }',
            '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n  exit 0\nfi',
            'echo "$DEV_NOTE" >&2\ncd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }\nexec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"',
            'set -u\n\nQA_DIR=\'/Volumes/DevMASTER/!CODING/Testing Agent MAIN\'\nWED=\'/Volumes/DevMASTER/WEDNESDAY\'']
tmpl = open(TEMPLATE, encoding='utf-8').read()
for r in RESIDUAL:
    assert tmpl.count(r) == 1, f"residual token not unique in the TEMPLATE: {r[:60]!r}"
    assert t.count(r) == 1, f"residual token not unique in the OUTPUT: {r[:60]!r}"
print(f"residual guard: {len(RESIDUAL)} tokens byte-identical in template and output")
# ---- output controls ------------------------------------------------------------------------------------------------------------------
CONTROLS = {'b54487216ebb49f1de7ed9349f089d92a3e5bfc1': 1, 'b85f1db24596a5e0ce98fe2b1343d9f515a1a995': 1, '5341b1daed8afe4254e05ef66ef4350fd8220d4f': 1,
            'a5334350221c819f54d4a20a3308daeb9ca09617': 2, 'a4f71cde660c1442d98317e26d93845340b20098': 1, '8861e62161466c40f08d2b10a30edeb203123993': 1,
            'd4cf7e3cf73e91422a229b7d0767cf6c3a04fe57': 1, 'exit 22': 2, 'exit 19': 3, 'exit 20': 1, 'exit 21': 2, 'exit 18': 4, 'exit 10': 1, 'exit 13': 1, 'exit 6': 1,   # counted on the output (first run's guesses kept in gen_launcher.first-run-7-count-guesses.out)
            'QA903R2': 0, 'HEAD_SHA': 0, 'MERGE_BASE': 0, 'ks-991-stale-local-develop': 0, 'peter_903_comment': 0, 'QAL7_': 10,
            'LANDED925': 6, 'peter_918_review_5151452193.md': 2, '2026-09-09-s161-batch-six-prs/report.md': 2, 'RE-GATE': 6, 'TIER 2': 4}
bad = [(k, t.count(k), v) for k, v in CONTROLS.items() if t.count(k) != v]
for k, got, want in bad: print(f"output control {k!r} occurs {got} times, expected {want}")
assert not bad, "output controls failed"
# no raw control byte
assert not [b for b in t.encode() if b < 32 and b not in (9, 10)], "raw control byte in the output"
open(OUT, 'w', encoding='utf-8').write(t); os.chmod(OUT, 0o755)
print(f"wrote {OUT} ({len(t)} B, sha256 {hashlib.sha256(t.encode()).hexdigest()[:16]}); substitutions/blocks: {subs}; output controls: {len(CONTROLS)}")
rc = subprocess.run(['/bin/bash', '-n', OUT]).returncode; print(f"/bin/bash -n rc={rc}"); assert rc == 0
# the post-header diff
a = tmpl[tmpl.index('set -u\n'):].splitlines(); b = t[t.index('set -u\n'):].splitlines()
d = list(difflib.unified_diff(a, b, 'template(post-header)', 'L7(post-header)', lineterm='', n=1))
open(f"{G}/gen_postheader.diff", 'w', encoding='utf-8').write('\n'.join(d) + '\n'); print(f"gen_postheader.diff: {len(d)} lines")
