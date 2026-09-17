#!/usr/bin/env python3
"""gen_launcher_1029.py — derive launchers/launch_qa_secuura_ks1180p1_1029.sh from launchers/launch_qa_secuura_ks1050_1018.sh (the #1018 ROUND 2 TIER 2
launcher: launched, verdicted GO WITH FINDINGS, merged tonight) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the
generator refuses and writes nothing. Two blocks are replaced whole (the authored header, and the develop judgement) because #1029 changes the guard's
KIND, not its values:
  * #1018 judged develop by thirteen blobs + a users.ts REGION + a GUARDED-prefix compare that refuses ANY develop move under services/auth/src/.
  * #1029 judges develop by PATH BLOBS ONLY, never by develop's SHA and never by a prefix: the one PR test file (develop-OK 4ad1cdcd1 / LANDED d9c98320e,
    exit 19) + the api-gateway files that test reads (its import closure: routes/verification.ts, services/redis.ts, utils/logger.ts — measured by
    import_closure_1029.py) + the api-gateway suite configuration (package.json, vitest.config.ts, vitest.setup.ts, tsconfig.json) + the packages/shared/src
    TREE (the in-tree @secuura/shared dist the gateway imports is built from it). Any other develop move — auth, other services, other api-gateway files,
    lockfiles — does not refuse; it is REPORTED (api-gateway files in the merge-base...develop delta are listed, so a denominator change is visible).
Every pinned blob is re-read from the repo (READ verb) at the head AND the current develop and asserted before anything is written.
Re-points: #1029 (KS-1180 part 1) ROUND 1 TIER 2; head cd3580e1f; compare develop...head = merge_base 20ab16f9a ahead 3 files 1 (behind NOT asserted);
brief/prompt/report dir/subject; overrides QA1029_*; fixture QA1029_TEST_FILE (a local file stands in for develop's ks1072 test blob); new exit 26
(the prompt must carry the probe-location rule: probe files OUTSIDE services/*, the #1018 F-3 lesson). Residual guard, output controls, heredoc parity,
no git write verb against $REPO, bash -n on a tmp file, then os.replace; a .pre-* copy if the output exists.
Usage: gen_launcher_1029.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1029', now(), '| template', os.path.basename(TPL), 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = 'cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc'; MB = '20ab16f9a80c5c3c75e613d8c670efefd8f5cafb'; CUR = '75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'
HT = '5138ce74287a7743f2b9fd652e7b9e58475f804f'; MT = '1227ecc82935c6e527c12abc6ff8e628c948e83b'
D = 'Blockchain/Dev/'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', '--quiet', x], capture_output=True, text=True).stdout.strip()
TEST = 'services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts'
T_DEV = '4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780'; T_OWN = 'd9c98320ea64638c3ab5ef2f35c102aba6d1207a'
PIN = {  # path relative to Blockchain/Dev -> blob (= head = merge-base = current develop)
 'services/api-gateway/src/routes/verification.ts': '28fb5834308a502f5f7b806e3b49a77627601eff',
 'services/api-gateway/src/services/redis.ts': '47659ee9c9f06acf9ac64e09b2dc207113ba92ea',
 'services/api-gateway/src/utils/logger.ts': '77200ea9c44109bb9e8d63734575fc8e3fa8b083',
 'services/api-gateway/package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 'services/api-gateway/vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 'services/api-gateway/vitest.setup.ts': '22c1107683b8192df3bfd3e929aa94aff3dc7d45',
 'services/api-gateway/tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
}
SHARED_SRC = '960758bcb07a2c5c42a0da4b1b1f742b258601da'
bad = [(p, b) for p, b in PIN.items() for ref in (H, MB, CUR) if rp(ref + ':' + D + p) != b]
bad += [('test @' + r[:9], rp(r + ':' + D + TEST)) for r, want in ((H, T_OWN), (MB, T_DEV), (CUR, T_DEV)) if rp(r + ':' + D + TEST) != want]
bad += [('shared/src @' + r[:9], rp(r + ':' + D + 'packages/shared/src')) for r in (H, MB, CUR) if rp(r + ':' + D + 'packages/shared/src') != SHARED_SRC]
bad += [x for x in [('head tree', rp(H + '^{tree}'))] if x[1] != HT]
print('pinned blobs re-read from the repo at head / merge-base / current develop:', 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); assert s.count(s[i:j]) == 1; return s[i:j]
HEADER_OLD = cut('#!/bin/bash\n', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """#!/bin/bash
# launch_qa_secuura_ks1180p1_1029.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1029 (KS-1180 part 1, Seat A)
# @ cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc — TEST-ONLY: services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts
# 4ad1cdcd1 -> d9c98320e (+16 -3). postTier2 now witnesses tier 2 by the stub anchor store's requests (exactly one read of this document) instead of
# blockchain.source (which reads 'persisted' on BOTH tiers: P-1016-1), plus a new control (an absent document: 404 after exactly one anchor-store request).
# Three commits: a4dc0d8ee (the change, parent d7e95cd9f) -> 7553821fc (merge of develop 81ee4b729) -> cd3580e1f (merge of develop 20ab16f9a). TIER 2.
#
# THE SHAPE, as read 21:03-21:14 AEST 2026-09-17 (git ls-remote + the PR and compare APIs agree): compare develop...head = merge_base 20ab16f9a, ahead 3,
# files 1 (asserted, exit 10; behind NOT asserted: develop was 75ad0e55c = #1026, auth only, at draft). The drafter re-derived IN ITS CLONE: merge-tree
# a4dc0d8ee x 81ee4b729 = tree(7553821fc) = 02f3ab417 and merge-tree 7553821fc x 20ab16f9a = tree(cd3580e1f) = 5138ce742; each merge's first-parent diff
# = develop's own delta (name set AND patch-id equal); merged over 75ad0e55c = tree 1227ecc82 (api-gateway + shared subtrees = the head's).
#
# The develop arm judges PATH BLOBS at the CURRENT develop, never develop's SHA and never a path prefix. GUARDED PATHS (Blockchain/Dev/...):
#   services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts   develop-OK 4ad1cdcd1 · LANDED d9c98320e (exit 19)
#   services/api-gateway/src/routes/verification.ts 28fb58343 · services/api-gateway/src/services/redis.ts 47659ee9c · services/api-gateway/src/utils/logger.ts
#   77200ea9c (the test's import closure inside api-gateway) · services/api-gateway/package.json 841d8c6ad · vitest.config.ts 5888e0b32 · vitest.setup.ts
#   22c110768 · tsconfig.json c981e6a92 (the suite's configuration) · packages/shared/src TREE 960758bcb (the in-tree @secuura/shared dist is built from it)
# Any of those at a blob nobody pinned -> exit 18. A develop move anywhere else clears, and the api-gateway files it touches are LISTED in the --check
# output (the gate re-measures the whole-suite denominator on its merged tree). WHY: develop moves often tonight; what the gate measures is the one test
# file running the real verification router, so only those bytes can make this brief about different code.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY, and the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM (the merge seat equality targets and the In Progress hold ride on it).
# exit 26: the prompt must carry the probe-location rule — probe files OUTSIDE services/* (the #1018 F-3 lesson: src/qa_probe/ sat inside tsc -p . and
#          vitest's default include).
# QA1029_CUR_DEV (test override, --check only): stands in for origin develop so the GUARDED / LANDED refusals can be proven.
# QA1029_TEST_FILE (test fixture, --check only): a local file stands in for develop's ks1072 test (its git blob) so the LANDED and GUARDED arms can be
# proven without a real develop commit.
# A launch with any QA1029_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1029/gen_launcher_1029.py from launch_qa_secuura_ks1050_1018.sh (asserted substitutions + two whole-block
# replacements + pins re-read from the repo + residual guard + output controls + bash -n): exit codes 2..26 (19 = LANDED), path-blob develop judgement.
#
# Usage: launch_qa_secuura_ks1180p1_1029.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..26 a guard refused
"""
JUDGE_OLD = cut('# The develop pin, judged by CONTENT (see the header):', '  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2\n     exit 18 ;;\nesac\n')
JUDGE_NEW = """# The develop judgement, by PATH BLOBS at the CURRENT develop (see the header) — never develop's SHA, never a prefix. Other moves are listed, not refused.
CUR_DEV="${QA1029_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  MERGE_BASE="$MERGE_BASE" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import hashlib, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; mb = os.environ["MERGE_BASE"]
D = "Blockchain/Dev/"
G = D + "services/api-gateway/"
TEST = G + "src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts"
DV = "develop"
# path -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  TEST:                                    ({"4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780": DV}, {"d9c98320ea64638c3ab5ef2f35c102aba6d1207a": "#1029 own"}),
  G + "src/routes/verification.ts":        ({"28fb5834308a502f5f7b806e3b49a77627601eff": DV}, {}),
  G + "src/services/redis.ts":             ({"47659ee9c9f06acf9ac64e09b2dc207113ba92ea": DV}, {}),
  G + "src/utils/logger.ts":               ({"77200ea9c44109bb9e8d63734575fc8e3fa8b083": DV}, {}),
  G + "package.json":                      ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  G + "vitest.config.ts":                  ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  G + "vitest.setup.ts":                   ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": DV}, {}),
  G + "tsconfig.json":                     ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
}
SHARED_SRC_OK = "960758bcb07a2c5c42a0da4b1b1f742b258601da"
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QA1029_TEST_FILE", "") if f == TEST else ""
    try:
        if fixture:
            data = open(fixture, "rb").read()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()
        else:
            blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": HTTP " + str(e.code)); sys.exit(0)
        blob = "ABSENT"
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1029 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9])
try:
    src = [x for x in get("/contents/" + D + "packages/shared?ref=" + cur) if x.get("name") == "src"]
except Exception as e:
    print("UNJUDGEABLE packages/shared listing unreadable: " + type(e).__name__); sys.exit(0)
if not src or src[0].get("sha") != SHARED_SRC_OK:
    print("GUARDED develop packages/shared/src tree " + (src[0].get("sha", "?")[:9] if src else "ABSENT") + " — a version nobody pinned"); sys.exit(0)
state.append("packages/shared/src tree " + SHARED_SRC_OK[:9])
state = "; ".join(state) + " (all = develop-OK)"
if cur == mb:
    print("OK " + state + " | origin develop = the head merge-base " + mb[:9] + " (merged tree = the head tree 5138ce742)"); sys.exit(0)
try:
    c = get("/compare/" + mb + "..." + cur)
    files = c.get("files") or []
    gwf = sorted(x["filename"].replace(D, "") for x in files if x["filename"].startswith(G))
    moved = "compare status %s, ahead %d behind %d, files %d, api-gateway files %d%s" % (c.get("status"), c.get("ahead_by", -1), c.get("behind_by", -1), len(files), len(gwf), (": " + " ".join(gwf[:6])) if gwf else "")
except Exception as e:
    moved = "delta unread (" + type(e).__name__ + "), not a guard"
tail = "the gate merges the then-current develop onto cd3580e1f in its own clone, names the merged-tree OID, and re-measures the api-gateway denominator and the tamper table there (brief items 1, 3)"
print("OK " + state + " | origin develop is " + cur + ", not the head merge-base " + mb[:9] + " (" + moved + ") — no guarded path moved; " + tail); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV and a GUARDED path moved or could not be judged: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
"""
REPORT_OLD = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1050-1018-efd677e98-tier2-r2/'
REPORT_NEW = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1180-1029-cd3580e1f-tier2-r1/'
SUBJ_OLD = '[QA -> Wednesday] TIER 2 GATE #1018 ROUND 2 (KS-1050) efd677e98'; SUBJ_NEW = '[QA -> Wednesday] TIER 2 GATE #1029 (KS-1180) cd3580e1f'
BRIEF_NEW = 'briefs/2026-09-17_secuura-1029-ks1180p1-tier2.md'; PROMPT_NEW = 'briefs/2026-09-17_secuura-1029-ks1180p1-tier2.prompt.txt'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('judgement block', JUDGE_OLD, JUDGE_NEW, 1),
 ('brief var', 'BRIEF="${QA1018_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.md}"', 'BRIEF="${QA1029_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/' + BRIEF_NEW + '}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1018_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.prompt.txt}"', 'PROMPT_FILE="${QA1029_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/' + PROMPT_NEW + '}"', 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/' + BRIEF_NEW + '"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1050-usersts933-answers-success-true-over-a-0-row-profile-update'", "BRANCH='refs/heads/feature/ks-1180-ks1073-verify-cells-the-tier-guard-is-not-a-tier-witness-the'", 1),
 ('head var', 'HEAD_SHA="${QA1018_HEAD:-efd677e98c917a52f8af442c9fcfde756166070e}"', 'HEAD_SHA="${QA1029_HEAD:-' + H + '}"', 1),
 ('merge-base', "MERGE_BASE='19f1e54750ce2b65312a687add2db4f5628edb7d'   # the merge-base of the head with develop = develop itself (#1025s squash), merged in by efd677e98",
  "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop = the head's second parent (#1027s squash), merged in by cd3580e1f", 1),
 ('develop var', "DEVELOP_SHA='19f1e54750ce2b65312a687add2db4f5628edb7d'   # develop at round-2 draft = #1025s squash, an ancestor of the head (git ls-remote 20:04:35, branches API 20:04:45 AEST)\n",
  "# NO develop SHA pin: develop is judged by PATH BLOBS (header). At draft develop was " + CUR + " (#1026s squash; git ls-remote 21:09:56, branches API 21:13:04 AEST).\n", 1),
 ('report dir', "REPORT_DIR='" + REPORT_OLD + "'", "REPORT_DIR='" + REPORT_NEW + "'", 1),
 ('head refuse msg', 'echo "REFUSING: #1018 — $HEAD_SHA is not at $BRANCH', 'echo "REFUSING: #1029 — $HEAD_SHA is not at $BRANCH', 1),
 ('compare comment', '# develop...#1018 = 19f1e5475 ahead 4 files 2 (behind 0 at round-2 draft; behind deliberately not asserted).', '# develop...#1029 = 20ab16f9a ahead 3 files 1 (behind 1 at draft; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=4 files=2" ] || { echo "REFUSING: #1018 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=4 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=1" ] || { echo "REFUSING: #1029 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=1'" >&2; exit 10; }''', 1),
 ('round guard', "grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round (ROUND 2)\" >&2; exit 15; }",
  "grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round (ROUND 1)\" >&2; exit 15; }", 1),
 ('subject', "grep -qF '" + SUBJ_OLD + "' \"$PROMPT_FILE\"", "grep -qF '" + SUBJ_NEW + "' \"$PROMPT_FILE\" && grep -qF '" + SUBJ_NEW + "' \"$BRIEF\"", 1),
 ('addendum guard + exit 26', '''  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM — the merge seat's equality targets and the In Progress hold ride on it" >&2; exit 25; }\n''',
  '''  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM — the merge seat's equality targets and the In Progress hold ride on it" >&2; exit 25; }\ngrep -qF 'probe files OUTSIDE services/' "$PROMPT_FILE" && grep -qF 'probe files OUTSIDE services/' "$BRIEF" \\\n  || { echo "REFUSING: brief or prompt does not carry the probe-location rule (probe files OUTSIDE services/*: the #1018 F-3 lesson)" >&2; exit 26; }\n''', 1),
 ('check head line', 'echo "  head on origin: #1018 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1029 $HEAD_SHA at $BRANCH"', 1),
 ('check compare line', 'echo "  compare (GitHub API): develop...#1018 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1029 = $COMPARE"', 1),
 ('check round', 'echo "  brief and prompt agree on TIER 2 and ROUND 2"', 'echo "  brief and prompt agree on TIER 2 and ROUND 1"', 1),
 ('check subject line', 'echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient"', 'echo "  brief and prompt carry the exact #1029 verdict subject; prompt names coagent@ sender, wednesday-agent@ recipient"', 1),
 ('subject refusal text', 'echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23;', 'echo "REFUSING: brief or prompt does not carry the exact verdict subject, or the prompt lacks the coagent@ sender or the wednesday-agent@ recipient" >&2; exit 23;', 1),
 ('check addendum line', 'echo "  brief and prompt carry the MERGE ADDENDUM"\n', 'echo "  brief and prompt carry the MERGE ADDENDUM"\n  echo "  brief and prompt carry the probe-location rule (probe files OUTSIDE services/*)"\n', 1),
 ('check override notes', '''  [ -n "${QA1018_CUR_DEV:-}" ] && echo "  (develop read from the QA1018_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1018_USERS_FILE:-}" ] && echo "  (develop auth routes/users.ts read from the QA1018_USERS_FILE fixture, not the contents API)"\n''',
  '''  [ -n "${QA1029_CUR_DEV:-}" ] && echo "  (develop read from the QA1029_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1029_TEST_FILE:-}" ] && echo "  (develop ks1072 test read from the QA1029_TEST_FILE fixture, not the contents API)"\n''', 1),
 ('launch override guard', '[ -z "${QA1018_BRIEF:-}${QA1018_PROMPT:-}${QA1018_HEAD:-}${QA1018_CUR_DEV:-}${QA1018_USERS_FILE:-}" ]', '[ -z "${QA1029_BRIEF:-}${QA1029_PROMPT:-}${QA1029_HEAD:-}${QA1029_CUR_DEV:-}${QA1029_TEST_FILE:-}" ]', 1),
]
for name, old, new, n in REPL:
    c = s.count(old)
    if c != n: print('REFUSE anchor', name, 'count', c, 'want', n); sys.exit(1)
    s = s.replace(old, new); print('  ok', name, c)
RES = s.replace(HEADER_NEW, '').replace('the #1018 F-3 lesson', '')  # the exit-26 message names its origin on purpose
for tok in ('efd677e98', '19f1e5475', 'ks1050', 'KS-1050', '#1018', 'QA1018', 'users.ts', 'USERS', 'ROUND 2', 'tier2-r2', 'DEVELOP_SHA', 'DEV_CONTENT_ALLOWED', 'services/auth', 'ahead=4', 'files=2', 'region'):
    if tok in RES: print('REFUSE residual token', tok, [l[:110] for l in s.splitlines() if tok in l][:4]); sys.exit(2)
# counts include the authored header: H (header + HEAD_SHA); QA1029_TEST_FILE (header, judgement, check note x2, launch guard); QA1029_CUR_DEV (header,
# CUR_DEV=, check note x2, launch guard); probe rule (header, 2 greps, refusal text, check echo); exit 26/19 (header + code); exit 18 (header + 2 code)
want = {H: 2, MB: 1, REPORT_NEW: 1, 'ahead=3 files=1': 2, "grep -q 'ROUND 1'": 2, "grep -q 'TIER 2'": 2, SUBJ_NEW: 2, T_DEV: 1, T_OWN: 1, SHARED_SRC: 1, ': DV}': 8,
        '[ -t 0 ]': 1, 'exec claude --dangerously-skip-permissions --model opus': 1, 'QA1029_TEST_FILE': 5, 'QA1029_CUR_DEV': 5, 'MERGE ADDENDUM': 5, 'NOT-TESTED.written-first.md': 4,
        BRIEF_NEW: 2, PROMPT_NEW: 1, 'probe files OUTSIDE services/': 5, 'exit 26': 2, 'exit 19': 2, 'exit 18': 3}
want.update({v: 1 for v in PIN.values()})
ctl = {k: s.count(k) for k in want}
print('output controls', {k[:28] + ('…' if len(k) > 28 else ''): v for k, v in ctl.items()})
bad = [(k[:50], ctl[k], v) for k, v in want.items() if ctl[k] != v]
if bad: print('REFUSE controls', bad); sys.exit(1)
for tag in ("<<'PY'", "<<'PYJ'"):
    i = s.index(tag); j = s.index('\n' + tag[3:-1] + '\n', i); blk = s[i:j]
    ap, op, cl = blk.count("'") - 2, blk.count('('), blk.count(')'); print('heredoc', tag, 'apostrophes', ap, 'parens (', op, ')', cl)
    if ap % 2 or op != cl: print('REFUSE heredoc parity', tag); sys.exit(1)
for verb in (' fetch ', ' merge ', ' reset ', ' worktree ', ' checkout ', ' push', ' commit '):
    if re.search(r'git -C "\$REPO"' + re.escape(verb), s): print('REFUSE git write verb', verb); sys.exit(1)
if any(ord(ch) < 32 and ch not in '\n\t' for ch in s): print('REFUSE control bytes'); sys.exit(1)
if os.path.exists(OUT):
    bak = OUT + '.pre-' + now('+%H%M%S'); shutil.copyfile(OUT, bak); print('existing launcher copied aside to', bak)
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip())
if p.returncode: sys.exit(3)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
