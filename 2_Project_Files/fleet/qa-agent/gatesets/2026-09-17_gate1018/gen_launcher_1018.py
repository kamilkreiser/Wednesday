#!/usr/bin/env python3
"""gen_launcher_1018.py — derive launch_qa_secuura_ks1050_1018.sh from launchers/launch_qa_secuura_ks1202_1024.sh (the #1024 ROUND 1 launcher, the newest
auth-adjacent guard family: head on origin 6, compare 10/13, develop judged BY CONTENT 18/19 with a REGION judgement, brief/prompt guards 7-17 + 20 + 22-25,
TTY 21, overrides 16) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.
Re-points at #1018 (KS-1050) TIER 2 ROUND 1: head 267bd8624, merge-base 7e89318bc (the PR parent), develop pinned ee40d3099 (re-pinned 19:1x after 79933c798 + #1022 landed mid-draft; 7 commits past
the PR parent, 0 files under services/auth): compare develop...head = merge_base 7e89318bc ahead 1 files 2 (behind NOT asserted). The develop arm judges
THIRTEEN files by blob (auth users.ts LANDED = #1018's blob, the ks1050 test ABSENT / LANDED) and auth routes/users.ts by REGION content (the errorHandler
import line and the PATCH /me handler body) with the WANT sha computed here from develop's blob 8ef9065e2 read with `git show` (a read verb) from the
checkout. GUARDED move paths: services/auth/src/ + its package.json / vitest config + setup / tsconfig, packages/shared/src/ + package.json,
docs/openapi/, eslint.config.mjs, the Dev lockfile. TIER 1 -> TIER 2 in the tier guard. Test hooks QA1018_*. Then a RESIDUAL GUARD, output controls,
heredoc parity, no git write verb, bash -n. Never overwrites an existing output (writes a .pre-* copy first).
Usage: gen_launcher_1018.py <template launcher> <output launcher>"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1018', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
HEAD = '267bd8624ce276ca62160216d042b8477bac52f1'; BASE = '7e89318bcedbc9a35757d4298ace54a6a23020bd'; DEVSHA = 'ee40d3099599fa2db23a37049da8e00ac953eacd'
USERS = 'Blockchain/Dev/services/auth/src/routes/users.ts'
dev_u = subprocess.run(['git', '-C', REPO, 'show', DEVSHA + ':' + USERS], capture_output=True).stdout
assert hashlib.sha1(b'blob %d\0' % len(dev_u) + dev_u).hexdigest().startswith('8ef9065e2')
head_u = subprocess.run(['git', '-C', REPO, 'show', HEAD + ':' + USERS], capture_output=True).stdout
assert hashlib.sha1(b'blob %d\0' % len(head_u) + head_u).hexdigest().startswith('84d4b75e1')
Q = chr(39)
SEGS = [["import { BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from @@Q@@../middleware/errorHandler@@Q@@;",
         "import { BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from @@Q@@../middleware/errorHandler@@Q@@;"],
        ["    const data = updateProfileSchema.parse(req.body);", "// POST /api/users/me/change-password"]]
def region_sha(text, segs):
    parts = []
    for a, b in segs:
        a = a.replace('@@Q@@', Q); b = b.replace('@@Q@@', Q)
        if text.count(a) != 1: return 'anchor-count-' + str(text.count(a))
        i = text.index(a); j = text.find(b, i)
        if j < 0: return 'end-anchor-missing'
        parts.append(text[i:j + len(b)])
    return hashlib.sha256('\n@@SEG@@\n'.join(parts).encode()).hexdigest()
WANT = region_sha(dev_u.decode(), SEGS); HEADR = region_sha(head_u.decode(), SEGS)
print('region WANT (develop users.ts)', WANT, '| head region', HEADR, '| differ (the import and the guard are inside the regions):', WANT != HEADR)
assert re.fullmatch(r'[0-9a-f]{64}', WANT) and WANT != HEADR
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1050-1018-267bd8624-tier2-r1/'
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
HEADER_OLD = cut('#!/bin/bash\n', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """#!/bin/bash
# launch_qa_secuura_ks1050_1018.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1018 (KS-1050, Seat A)
# @ 267bd8624ce276ca62160216d042b8477bac52f1 — auth PATCH /api/users/me: when userRepo.updateUser returns null (a 0-row UPDATE since KS-943) the
# handler throws AppError 500 PROFILE_UPDATE_NOT_PERSISTED instead of answering success: true with undefined fields. ONE commit on 7e89318bc, TWO
# files: services/auth/src/routes/users.ts 8ef9065e2 -> 84d4b75e1 (+5 -1: AppError added to the errorHandler import, a 4-line guard) and a new
# vitest file ks1050-profile-update-zero-rows-is-not-success.test.ts 7beff8857 (3 cells). TIER 2 (Wednesday's receipt, not the seat's proposed tier 1):
# a correctness guard on a response contract, not an authorisation, data-destruction or handover surface; 500 is already in the spec.
#
# THE SHAPE, as read 18:49-19:12 AEST 2026-09-17 (git ls-remote + the PR, compare and contents APIs agree): develop MOVED mid-draft 81ee4b729 -> ee40d3099
# (79933c798 then #1022s squash: the hono lock bump in the Dev, mcp-server and one other service lock + audit rows + one other service route/test;
# NOTHING under services/auth or packages/shared). develop is seven commits past the PR parent 7e89318bc (the earlier five: gateway, scripts/audit,
# systemTest locks, one packages/shared TEST file). compare develop...head = merge_base 7e89318bc, diverged, ahead 1, behind 7, files 2 (asserted as
# merge_base + ahead + files, exit 10; behind NOT asserted). PR API mergeable true (state unstable). Merged tree over ee40d3099 =
# a133db3e77328dded88a8f982122248c3e8486c4 (merge-tree --write-tree in the drafter clone, clean; the auth subtree = the head's; develop -> merged =
# exactly the 2 PR files at the PR's own blobs).
#
# The develop pin is judged by CONTENT, not bare: (a) THIRTEEN files by blob at the CURRENT develop — the PR two (auth routes/users.ts 8ef9065e2, the
# ks1050 test ABSENT; at their #1018 blobs -> exit 19 LANDED), auth repositories/userRepo.ts (updateUser + the house helper updateUserOrThrow) /
# middleware/errorHandler.ts / middleware/authenticate.ts / routes/wallet.ts (the precedent) / auth.openapi.ts / package.json / vitest.config.ts /
# vitest.setup.ts / tsconfig.json, docs/openapi/secuura-api.yaml, Dev eslint.config.mjs — any blob nobody pinned -> exit 18; users.ts at ANY OTHER
# blob is judged by REGION content (the errorHandler import line and the PATCH /me handler body through the change-password banner): a move into a
# region refuses (exit 18), a move outside clears; (b) if develop moved past ee40d3099, the compare pinned...develop REFUSES (exit 18) when the delta
# touches a GUARDED path — services/auth/src/ and its package.json / vitest config + setup / tsconfig, packages/shared/src/ and its package.json,
# docs/openapi/, eslint.config.mjs, the Dev lockfile — unless users.ts cleared by its region judgement (DEV_CONTENT_ALLOWED is EMPTY), or the move
# cannot be judged. A packages/shared TEST-only move refuses too, by design: re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY, and the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM (the merge seat equality targets and the In Progress hold ride on it).
# QA1018_CUR_DEV (test override, --check only): stands in for origin develop so the GUARDED / UNJUDGEABLE refusals can be proven.
# QA1018_USERS_FILE (test fixture, --check only): a local file stands in for develop auth routes/users.ts (content AND git blob) so the region
# judgement clear and refuse arms, and the LANDED arm, can be proven without a real develop commit.
# A launch with any QA1018_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1018/gen_launcher_1018.py from launch_qa_secuura_ks1202_1024.sh (asserted substitutions + residual guard + output
# controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1018 TIER 2 ROUND 1.
#
# Usage: launch_qa_secuura_ks1050_1018.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
BODY_OLD = cut('D = "Blockchain/Dev/"\nO = D + "services/originate/"\n', 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/originate/src/ + its config files, the api-gateway create/verify/auth/index files, docs/openapi/, eslint.config.mjs, the Dev lockfile) or documents.ts cleared by its region judgement; %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)\n')
BODY_NEW = '''D = "Blockchain/Dev/"
A = D + "services/auth/"
USERS = A + "src/routes/users.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  USERS:                                                                ({"8ef9065e2fb24308daeb41820a227a4ee1d6ecc9": DV}, {"84d4b75e1aca7a5100f51401e394648b26557643": "#1018 own"}),
  A + "src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts": ({"ABSENT": DV}, {"7beff88572395d7a11eb1f1086ddae2b986a5774": "#1018 own"}),
  A + "src/repositories/userRepo.ts":                                   ({"9060b308e6d6a82c8a79be7387032d2a18c4ac22": DV}, {}),
  A + "src/middleware/errorHandler.ts":                                 ({"1cf66e74cd2bbe1d56f53c6f7ef5200e1835ee3c": DV}, {}),
  A + "src/middleware/authenticate.ts":                                 ({"be7102929b44f7567b0cab4ec1c82f84d04bc58e": DV}, {}),
  A + "src/routes/wallet.ts":                                           ({"3134e9525fcf972f81a5c74a8fc77fe3df15c367": DV}, {}),
  A + "src/auth.openapi.ts":                                            ({"2c356c3c7877add99f5e1a3c437d04ac8be3dc76": DV}, {}),
  A + "package.json":                                                   ({"814e88419470b811f26f1593984071bb317608d8": DV}, {}),
  A + "vitest.config.ts":                                               ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": DV}, {}),
  A + "vitest.setup.ts":                                                ({"bc18c18755cb00f96e3e228ca34d99fd1266c20f": DV}, {}),
  A + "tsconfig.json":                                                  ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": DV}, {}),
  D + "docs/openapi/secuura-api.yaml":                                  ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": DV}, {}),
  D + "eslint.config.mjs":                                              ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
}
# REGION judgement for auth routes/users.ts (brief items 1-4 stand on it): two segments of develop 8ef9065e2; the SHA was computed by gen_launcher_1018.py.
SEGS = @@SEGS@@
SEGS = [[x.replace("@@Q@@", chr(39)) for x in pair] for pair in SEGS]
WANT = "@@WANT@@"
def region_sha(text):
    parts = []
    for a, b in SEGS:
        if text.count(a) != 1:
            return "anchor-count-" + str(text.count(a))
        i = text.index(a); j = text.find(b, i)
        if j < 0:
            return "end-anchor-missing"
        parts.append(text[i:j + len(b)])
    return hashlib.sha256("\\n@@SEG@@\\n".join(parts).encode()).hexdigest()
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QA1018_USERS_FILE", "") if f == USERS else ""
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1018 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok and f == USERS:
        try:
            text = open(fixture).read() if fixture else raw(f, cur)
        except Exception as e:
            print("UNJUDGEABLE develop " + short + " content unreadable: " + type(e).__name__); sys.exit(0)
        rs = region_sha(text)
        if rs != WANT:
            print("GUARDED develop " + short + " blob " + blob[:9] + " — a #1018 region changed: region " + rs[:16] + " vs pinned " + WANT[:16]); sys.exit(0)
        content_cleared.add(f)
        state.append(f.split("/")[-1] + " " + blob[:9] + " = moved OUTSIDE the #1018 regions, judged by content: region " + rs[:12])
        continue
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= #1022s squash, 7 commits past the PR parent 7e89318bc, 0 auth files: the gate merges it; drafter merged tree a133db3e77328dded88a8f982122248c3e8486c4; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           D + "packages/shared/src/",
           D + "packages/shared/package.json",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. users.ts is judged by its REGIONS above; every other guarded hit falls through to exit 18. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if (h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h]) or h in content_cleared)
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 267bd8624 in its own clone, rebuilds the shared dist there, runs the whole auth vitest suite and the ks1050 cells on the MERGED tree beside the base and head trees, names the merged-tree OID and re-derives every count, above all the auth denominator (brief items 1, 4, 6)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/auth/src/ + its config files, packages/shared/src/ + package.json, docs/openapi/, eslint.config.mjs, the Dev lockfile) or users.ts cleared by its region judgement; %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
'''
segs_lit = '[' + ', '.join('[' + ', '.join('"' + x.replace('"', '\\"') + '"' for x in pair) + ']' for pair in SEGS) + ']'
BODY_NEW = BODY_NEW.replace('@@SEGS@@', segs_lit).replace('@@WANT@@', WANT)
T = '[QA -> Wednesday] TIER 2 GATE #1018 (KS-1050) 267bd8624'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1024_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.md}"', 'BRIEF="${QA1018_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1024_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1018_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1202-the-served-document-type-comes-from-datadocumenttype-which'", "BRANCH='refs/heads/feature/ks-1050-usersts933-answers-success-true-over-a-0-row-profile-update'", 1),
 ('head var', 'HEAD_SHA="${QA1024_HEAD:-d1a3280880d85ff31fd409aa1b5a16c428c4bb9a}"', 'HEAD_SHA="${QA1018_HEAD:-' + HEAD + '}"', 1),
 ('merge-base', "MERGE_BASE='581c9db0db4201c42cbbf702f339b750989acdb1'   # the merge-base of the head with develop = #1019s squash, the second parent of the head merge d1a328088",
  "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR parent (#1016s squash; #1015 KS-1018 already under it)", 1),
 ('develop', "DEVELOP_SHA='81ee4b729e86a645fc9098aafa1aaf39035a9950'   # develop at draft close = #1021s squash on 581c9db0d, NOT an ancestor of the head (git ls-remote 18:24:04, branches API 18:24:23 AEST)",
  "DEVELOP_SHA='" + DEVSHA + "'   # develop at draft close = #1022s squash, 7 commits past the PR parent, 0 auth files (moved from 81ee4b729 mid-draft; branches API 19:11:02 AEST)", 1),
 ('report dir', "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/'", "REPORT_DIR='" + REPORT_DIR + "'", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2.md"', 1),
 ('head refuse', 'REFUSING: #1024 — $HEAD_SHA', 'REFUSING: #1018 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1024 = 581c9db0d ahead 3 files 2 (behind 1 at draft close = #1021; behind deliberately not asserted).', '# develop...#1018 = 7e89318bc ahead 1 files 2 (behind 7 at draft close; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1024 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1018 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
 ('develop comment', '# The develop pin, judged by CONTENT (see the header): sixteen files by blob at the CURRENT develop (documents.ts also by region), then — if develop',
                     '# The develop pin, judged by CONTENT (see the header): thirteen files by blob at the CURRENT develop (users.ts also by region), then — if develop', 1),
 ('cur dev', 'CUR_DEV="${QA1024_CUR_DEV:-', 'CUR_DEV="${QA1018_CUR_DEV:-', 1),
 ('body', BODY_OLD, BODY_NEW, 1),
 ('tier brief', "grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", "grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\"", 1),
 ('subject', "grep -qF '[QA -> Wednesday] TIER 1 GATE #1024 (KS-1202) d1a328088' \"$PROMPT_FILE\"", "grep -qF '" + T + "' \"$PROMPT_FILE\"", 1),
 ('check head', 'echo "  head on origin: #1024 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1018 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1024 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1018 = $COMPARE"', 1),
 ('check tier', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 'echo "  brief and prompt agree on TIER 2 and ROUND 1"', 1),
 ('check cur dev', '[ -n "${QA1024_CUR_DEV:-}" ] && echo "  (develop read from the QA1024_CUR_DEV test override, not ls-remote)"', '[ -n "${QA1018_CUR_DEV:-}" ] && echo "  (develop read from the QA1018_CUR_DEV test override, not ls-remote)"', 1),
 ('check fixture', '[ -n "${QA1024_DOCS_FILE:-}" ] && echo "  (develop originate routes/documents.ts read from the QA1024_DOCS_FILE fixture, not the contents API)"', '[ -n "${QA1018_USERS_FILE:-}" ] && echo "  (develop auth routes/users.ts read from the QA1018_USERS_FILE fixture, not the contents API)"', 1),
 ('exit16', '[ -z "${QA1024_BRIEF:-}${QA1024_PROMPT:-}${QA1024_HEAD:-}${QA1024_CUR_DEV:-}${QA1024_DOCS_FILE:-}" ]', '[ -z "${QA1018_BRIEF:-}${QA1018_PROMPT:-}${QA1018_HEAD:-}${QA1018_CUR_DEV:-}${QA1018_USERS_FILE:-}" ]', 1),
]
for name, old, new, n in REPL:
    c = s.count(old)
    if c != n: print('REFUSE anchor', name, 'count', c, 'want', n); sys.exit(1)
    s = s.replace(old, new); print('  ok', name, c)
RES = s.replace('launch_qa_secuura_ks1202_1024.sh', '').replace('#1022s squash', '')  # the legitimate mentions: the template name, the develop commit name, the develop delta in the header
for tok in ('QA1024', '1024', 'KS-1202', 'd1a328088', '581c9db0d', 'ccd3f2819', 'originate', 'documents.ts', 'DOCS', 'TIER 1', 'sixteen', 'api-gateway', 'jest'):
    if tok in RES: print('REFUSE residual token', tok, [l[:100] for l in s.splitlines() if tok in l][:4]); sys.exit(2)
ctl = {k: s.count(k) for k in (HEAD, DEVSHA, BASE, 'a133db3e77328dded88a8f982122248c3e8486c4', WANT, REPORT_DIR, 'ahead=1 files=2', 'QA1018_USERS_FILE', 'QA1018_CUR_DEV', '84d4b75e1aca7a5100f51401e394648b26557643', '7beff88572395d7a11eb1f1086ddae2b986a5774', 'DEV_CONTENT_ALLOWED = {}', ': DV}', "grep -q 'ROUND 1'", "grep -q 'TIER 2'", 'MERGE ADDENDUM', 'NOT-TESTED.written-first.md', 'exit 19', 'exit 21', 'exit 22', 'exit 23', 'exit 24', 'exit 25', 'exit 16', '[ -t 0 ]', 'exec claude --dangerously-skip-permissions --model opus', T)}
print('output controls', {k[:24] + ('…' if len(k) > 24 else ''): v for k, v in ctl.items()})
want = {'ahead=1 files=2': 2, ': DV}': 13, 'DEV_CONTENT_ALLOWED = {}': 1, T: 1, 'QA1018_USERS_FILE': 5, 'QA1018_CUR_DEV': 5, HEAD: 2, "grep -q 'TIER 2'": 2, "grep -q 'ROUND 1'": 2, WANT: 1, '[ -t 0 ]': 1,
        '84d4b75e1aca7a5100f51401e394648b26557643': 1, '7beff88572395d7a11eb1f1086ddae2b986a5774': 1, 'exec claude --dangerously-skip-permissions --model opus': 1}
for k, v in want.items():
    if ctl[k] != v: print('REFUSE control', k[:60], ctl[k], 'want', v); sys.exit(1)
for tag in ("<<'PY'", "<<'PYJ'"):
    i = s.index(tag); j = s.index('\n' + tag[3:-1] + '\n', i); blk = s[i:j]
    ap, op, cl = blk.count("'") - 2, blk.count('('), blk.count(')'); print('heredoc', tag, 'apostrophes', ap, 'parens (', op, ')', cl)
    if ap % 2 or op != cl: print('REFUSE heredoc parity', tag); sys.exit(1)
for verb in (' fetch ', ' merge ', ' reset ', ' worktree ', ' checkout ', ' push', ' commit '):
    if re.search(r'git -C "\$REPO"' + re.escape(verb), s): print('REFUSE git write verb', verb); sys.exit(1)
if os.path.exists(OUT): shutil.copyfile(OUT, OUT + '.pre-' + now('+%H%M%S')); print('existing output copied aside')
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip())
if p.returncode: sys.exit(3)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
