#!/usr/bin/env python3
"""gen_launcher_1024.py — derive launch_qa_secuura_ks1202_1024.sh from launchers/launch_qa_secuura_ks1187_1019.sh (the #1019 ROUND 1 launcher) by ASSERTED
substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing. Re-points at #1024 (KS-1202) ROUND 1: head d1a328088,
merge-base 581c9db0d, develop pinned 81ee4b729 (#1021's squash landed during drafting; NOT an ancestor of the head): compare develop...head = merge_base 581c9db0d
ahead 3 files 2 (behind NOT asserted). The develop arm judges SIXTEEN files by blob (originate documents.ts LANDED = #1024's blob) and originate documents.ts by
REGION content (the create resolution + guard site, the list and GET served readers, the /:id/version writer) with the WANT sha computed here from develop's blob
c3a818ac8 read with `git show` (a read verb) from the checkout. GUARDED move paths: originate src/ + its config files, the api-gateway create/verify/auth/index files,
docs/openapi/, eslint.config.mjs, the Dev lockfile. Exits unchanged 2..25 (24 report dir + NOT-TESTED, 25 MERGE ADDENDUM). Test hooks QA1024_*. Then a RESIDUAL GUARD,
output controls, heredoc parity, no git write verb, bash -n. Never overwrites an existing output (writes a .pre-* copy first).
Usage: gen_launcher_1024.py <template launcher> <output launcher>"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1024', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DOCS = 'Blockchain/Dev/services/originate/src/routes/documents.ts'
dev_doc = subprocess.run(['git', '-C', REPO, 'show', '581c9db0db4201c42cbbf702f339b750989acdb1:' + DOCS], capture_output=True).stdout
assert hashlib.sha1(b'blob %d\0' % len(dev_doc) + dev_doc).hexdigest().startswith('c3a818ac8')
head_doc = subprocess.run(['git', '-C', REPO, 'show', 'd1a3280880d85ff31fd409aa1b5a16c428c4bb9a:' + DOCS], capture_output=True).stdout
assert hashlib.sha1(b'blob %d\0' % len(head_doc) + head_doc).hexdigest().startswith('de9b5ae25')
Q = chr(39)
SEGS = [["      const docType: string = documentType || rawType || @@Q@@DOCUMENT@@Q@@;", "      if (documentType && !data.documentType) data.documentType = documentType;"],
        ["          documentType: (d.data?.documentType as string) || d.type,", "          documentType: (d.data?.documentType as string) || d.type,"],
        ["        documentType: (document.data as Record<string, unknown>)?.documentType || document.type,", "        documentType: (document.data as Record<string, unknown>)?.documentType || document.type,"],
        ["const ALLOWED_VERSION_ACTIONS = [", "      await saveDocument(derivedDoc, tenantId, (req as any).db);"]]
def region_sha(text, segs):
    parts = []
    for a, b in segs:
        a = a.replace('@@Q@@', Q); b = b.replace('@@Q@@', Q)
        if text.count(a) != 1: return 'anchor-count-' + str(text.count(a))
        i = text.index(a); j = text.find(b, i)
        if j < 0: return 'end-anchor-missing'
        parts.append(text[i:j + len(b)])
    return hashlib.sha256('\n@@SEG@@\n'.join(parts).encode()).hexdigest()
WANT = region_sha(dev_doc.decode(), SEGS); HEADR = region_sha(head_doc.decode(), SEGS)
print('region WANT (develop documents.ts)', WANT, '| head region', HEADR, '| differ (the guard is inside region 1):', WANT != HEADR)
assert re.fullmatch(r'[0-9a-f]{64}', WANT) and WANT != HEADR
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/'
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
HEADER_OLD = cut('#!/bin/bash\n', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """#!/bin/bash
# launch_qa_secuura_ks1202_1024.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate (round 1 of 2 under the cap) over Secuura/Blockchain PR #1024
# (KS-1202, Seat A) @ d1a3280880d85ff31fd409aa1b5a16c428c4bb9a — originate POST /api/documents: a create whose data.documentType is present and differs from the
# resolved type (documentType || type || DOCUMENT, routes/documents.ts:565) is refused 400, so a document stored as one type is no longer SERVED as another
# (GET /:id and the list serve data.documentType || type). Fix commit 86b11045c (documents.ts +12, a 19-cell jest test); the head merges develop f8c7aaa39 then
# 581c9db0d (#1019s squash); tree 10a71b876. TIER 1: the served type decides the gateway verify gate level and bypassed the connector allow-list. Kam ruled
# build-and-merge (KS-1202 comment fa50d21e): Wednesday merges on this gate GO.
#
# THE SHAPE, as read 18:13-18:25 AEST 2026-09-17 (git ls-remote x2 + the PR, compare and contents APIs agree): develop MOVED during drafting 581c9db0d -> 81ee4b729
# (#1021s squash: scripts/audit/audit-baseline.json + two systemTest locks, nothing under services/), so develop is NOT an ancestor of the head: compare
# develop...head = merge_base 581c9db0d, diverged, ahead 3, behind 1, files 2 (asserted as merge_base + ahead + files, exit 10; behind NOT asserted).
# Merged tree over 81ee4b729 = ccd3f281977eb0ddda4af2e555c074d30fddd3db (merge-tree --write-tree in the drafter clone; originate + api-gateway subtrees = the head).
#
# The develop pin is judged by CONTENT, not bare: (a) SIXTEEN files by blob at the CURRENT develop — the PR two (originate documents.ts c3a818ac8, the ks1202
# test ABSENT; at their #1024 blobs -> exit 19 LANDED), originate documentRepo.ts / certifications.ts / index.ts / middleware auth.ts + rbac.ts / originate.openapi.ts /
# package.json / jest.config.js / tsconfig.json, api-gateway routes/verification.ts / services/enforcement.ts / src/index.ts, docs/openapi/secuura-api.yaml, Dev
# eslint.config.mjs — any blob nobody pinned -> exit 18; documents.ts at ANY OTHER blob is judged by REGION content (the create type resolution through the data
# fill, the list and GET served readers, the /:id/version writer): a move into a region refuses (exit 18), a move outside clears; (b) if develop moved past
# 81ee4b729, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — services/originate/src/ and its config files, the
# api-gateway create/verify/auth/index files, docs/openapi/, eslint.config.mjs, the Dev lockfile — unless documents.ts cleared by its region judgement
# (DEV_CONTENT_ALLOWED is EMPTY), or the move cannot be judged.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY, and the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM (the merge seat equality targets and the In Progress hold ride on it).
# QA1024_CUR_DEV (test override, --check only): stands in for origin develop so the GUARDED refusals can be proven.
# QA1024_DOCS_FILE (test fixture, --check only): a local file stands in for develop routes/documents.ts (content AND git blob) so the region judgement
# clear and refuse arms, and the LANDED arm, can be proven without a real develop commit.
# A launch with any QA1024_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1024/gen_launcher_1024.py from launch_qa_secuura_ks1187_1019.sh (asserted substitutions + residual guard + output
# controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1024 ROUND 1.
#
# Usage: launch_qa_secuura_ks1202_1024.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
BODY_OLD = cut('cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]\n', 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/api-gateway/src/ + its config files, originate gdpr routes + index, eslint.config.mjs, the Dev lockfile) or cleared by the proxy.ts region judgement or #1017s exact blobs; %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)\n')
BODY_NEW = '''cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
O = D + "services/originate/"
G = D + "services/api-gateway/"
DOCS = O + "src/routes/documents.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  DOCS:                                                                ({"c3a818ac8ac8de1b385540d15e3fbb23200cea30": DV}, {"de9b5ae25984ea29eff01d6c4e73f9bc0dc6573a": "#1024 own"}),
  O + "src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts": ({"ABSENT": DV}, {"ada07f0536ad003754cb2a08f514fc04f8996b27": "#1024 own"}),
  O + "src/repositories/documentRepo.ts":                              ({"6e059d36c50a82016faca14111c28ec35bc4f237": DV}, {}),
  O + "src/routes/certifications.ts":                                  ({"59bfe1c62cad4d324505344582d374f4c6035a6d": DV}, {}),
  O + "src/index.ts":                                                  ({"44d4e4f341f5d314f5b95405b209a9450cde1d3e": DV}, {}),
  O + "src/middleware/auth.ts":                                        ({"f08ee1a895bc878bc2656f649833706f665686e7": DV}, {}),
  O + "src/middleware/rbac.ts":                                        ({"@@RBAC@@": DV}, {}),
  O + "src/originate.openapi.ts":                                      ({"2d1b48a0c7ea93521d553cc28ccb53b4fe3fd19c": DV}, {}),
  O + "package.json":                                                  ({"749912c592e8630fff348cc60e1bf49677c18ab1": DV}, {}),
  O + "jest.config.js":                                                ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  O + "tsconfig.json":                                                 ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  G + "src/routes/verification.ts":                                    ({"28fb5834308a502f5f7b806e3b49a77627601eff": DV}, {}),
  G + "src/services/enforcement.ts":                                   ({"be466fbf444178bbb41293fb1d811957e55e1d2d": DV}, {}),
  G + "src/index.ts":                                                  ({"db127dbfa5dd899b0a8e0d844690890d91e27f10": DV}, {}),
  D + "docs/openapi/secuura-api.yaml":                                 ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": DV}, {}),
  D + "eslint.config.mjs":                                             ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
}
# REGION judgement for originate routes/documents.ts (brief items 1-3 stand on it): four segments of develop c3a818ac8; the SHA was computed by gen_launcher_1024.py.
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
    fixture = os.environ.get("QA1024_DOCS_FILE", "") if f == DOCS else ""
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1024 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok and f == DOCS:
        try:
            text = open(fixture).read() if fixture else raw(f, cur)
        except Exception as e:
            print("UNJUDGEABLE develop " + short + " content unreadable: " + type(e).__name__); sys.exit(0)
        rs = region_sha(text)
        if rs != WANT:
            print("GUARDED develop " + short + " blob " + blob[:9] + " — a #1024 region changed: region " + rs[:16] + " vs pinned " + WANT[:16]); sys.exit(0)
        content_cleared.add(f)
        state.append(f.split("/")[-1] + " " + blob[:9] + " = moved OUTSIDE the #1024 regions, judged by content: region " + rs[:12])
        continue
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= #1021s squash on 581c9db0d, NOT an ancestor of the head: the gate merges it; drafter merged tree ccd3f281977eb0ddda4af2e555c074d30fddd3db; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [O + "src/",
           O + "package.json",
           O + "jest.config.js",
           O + "tsconfig.json",
           G + "src/routes/verification.ts",
           G + "src/services/enforcement.ts",
           G + "src/middleware/auth.ts",
           G + "src/index.ts",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. documents.ts is judged by its REGIONS above; every other guarded hit falls through to exit 18. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if (h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h]) or h in content_cleared)
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto d1a328088 in its own clone, rebuilds the shared dist there, runs the originate suite and the carrier and writer censuses on the MERGED tree beside the develop and head trees, names the merged-tree OID and re-derives every count, above all the originate denominator (brief items 1, 2, 5)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/originate/src/ + its config files, the api-gateway create/verify/auth/index files, docs/openapi/, eslint.config.mjs, the Dev lockfile) or documents.ts cleared by its region judgement; %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
'''
rbac = subprocess.run(['git', '-C', REPO, 'rev-parse', '81ee4b729e86a645fc9098aafa1aaf39035a9950:Blockchain/Dev/services/originate/src/middleware/rbac.ts'], capture_output=True, text=True)
if rbac.returncode != 0:
    rbac = subprocess.run(['git', '-C', REPO, 'rev-parse', '581c9db0db4201c42cbbf702f339b750989acdb1:Blockchain/Dev/services/originate/src/middleware/rbac.ts'], capture_output=True, text=True)
RB = rbac.stdout.strip(); assert re.fullmatch(r'[0-9a-f]{40}', RB), rbac.stderr; print('rbac.ts blob at develop', RB)
segs_lit = '[' + ', '.join('[' + ', '.join('"' + x.replace('"', '\\"') + '"' for x in pair) + ']' for pair in SEGS) + ']'
BODY_NEW = BODY_NEW.replace('@@SEGS@@', segs_lit).replace('@@WANT@@', WANT).replace('@@RBAC@@', RB)
T = '[QA -> Wednesday] TIER 1 GATE #1024 (KS-1202) d1a328088'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1019_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019-ks1187-tier1.md}"', 'BRIEF="${QA1024_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1019_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019-ks1187-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1024_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1187-security-an-absolute-form-request-target-bypasses-the-ks-843'", "BRANCH='refs/heads/feature/ks-1202-the-served-document-type-comes-from-datadocumenttype-which'", 1),
 ('head var', 'HEAD_SHA="${QA1019_HEAD:-8b8996f8b290ef55c35721c30f8671f982fa5a91}"', 'HEAD_SHA="${QA1024_HEAD:-d1a3280880d85ff31fd409aa1b5a16c428c4bb9a}"', 1),
 ('merge-base', "MERGE_BASE='fa887f382b212b8da4a0a4a556bacb05ea34daaa'   # the merge-base of the head with develop = the PR parent of 50a4b749a (#1014s squash)",
  "MERGE_BASE='581c9db0db4201c42cbbf702f339b750989acdb1'   # the merge-base of the head with develop = #1019s squash, the second parent of the head merge d1a328088", 1),
 ('develop', "DEVELOP_SHA='fa887f382b212b8da4a0a4a556bacb05ea34daaa'   # develop at draft close = the PR parent (branches API 09:35:53, git ls-remote 09:18:55 and 09:37:10 AEST)",
  "DEVELOP_SHA='81ee4b729e86a645fc9098aafa1aaf39035a9950'   # develop at draft close = #1021s squash on 581c9db0d, NOT an ancestor of the head (git ls-remote 18:24:04, branches API 18:24:23 AEST)", 1),
 ('report dir', "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019-8b8996f8b-tier1-r1/'", "REPORT_DIR='" + REPORT_DIR + "'", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019-ks1187-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1019 — $HEAD_SHA', 'REFUSING: #1024 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1019 = fa887f382 ahead 2 files 3 (behind 0 at draft close; behind deliberately not asserted).', '# develop...#1024 = 581c9db0d ahead 3 files 2 (behind 1 at draft close = #1021; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=3" ] || { echo "REFUSING: #1019 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=3'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1024 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''', 1),
 ('develop comment', '# The develop pin, judged by CONTENT (see the header): twenty files by blob at the CURRENT develop (proxy.ts also by region), then — if develop',
                     '# The develop pin, judged by CONTENT (see the header): sixteen files by blob at the CURRENT develop (documents.ts also by region), then — if develop', 1),
 ('cur dev', 'CUR_DEV="${QA1019_CUR_DEV:-', 'CUR_DEV="${QA1024_CUR_DEV:-', 1),
 ('body', BODY_OLD, BODY_NEW, 1),
 ('refuse repin msg', '(launcher DEVELOP_SHA / JUDGED blobs / DEV_CONTENT_ALLOWED + brief TARGET + prompt)', '(launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)', 1),
 ('subject', "grep -qF '[QA -> Wednesday] TIER 1 GATE #1019 (KS-1187) 8b8996f8b' \"$PROMPT_FILE\"", "grep -qF '" + T + "' \"$PROMPT_FILE\"", 1),
 ('check head', 'echo "  head on origin: #1019 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1024 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1019 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1024 = $COMPARE"', 1),
 ('check cur dev', '[ -n "${QA1019_CUR_DEV:-}" ] && echo "  (develop read from the QA1019_CUR_DEV test override, not ls-remote)"', '[ -n "${QA1024_CUR_DEV:-}" ] && echo "  (develop read from the QA1024_CUR_DEV test override, not ls-remote)"', 1),
 ('check fixture', '[ -n "${QA1019_PROXY_FILE:-}" ] && echo "  (develop routes/proxy.ts read from the QA1019_PROXY_FILE fixture, not the contents API)"', '[ -n "${QA1024_DOCS_FILE:-}" ] && echo "  (develop originate routes/documents.ts read from the QA1024_DOCS_FILE fixture, not the contents API)"', 1),
 ('exit16', '[ -z "${QA1019_BRIEF:-}${QA1019_PROMPT:-}${QA1019_HEAD:-}${QA1019_CUR_DEV:-}${QA1019_PROXY_FILE:-}" ]', '[ -z "${QA1024_BRIEF:-}${QA1024_PROMPT:-}${QA1024_HEAD:-}${QA1024_CUR_DEV:-}${QA1024_DOCS_FILE:-}" ]', 1),
]
for name, old, new, n in REPL:
    c = s.count(old)
    if c != n: print('REFUSE anchor', name, 'count', c, 'want', n); sys.exit(1)
    s = s.replace(old, new); print('  ok', name, c)
RES = s.replace('#1019s squash', '').replace('launch_qa_secuura_ks1187_1019.sh', '')  # the two legitimate mentions: the develop commit name and the template name
for tok in ('QA1019', '1019', 'KS-1187', '8b8996f8b', 'fa887f382', 'proxy.ts', 'PROXY', 'erasure', 'gdpr', 'S17', '#1017'):
    if tok in RES: print('REFUSE residual token', tok, [l[:100] for l in s.splitlines() if tok in l][:4]); sys.exit(2)
ctl = {k: s.count(k) for k in ('d1a3280880d85ff31fd409aa1b5a16c428c4bb9a', '81ee4b729e86a645fc9098aafa1aaf39035a9950', '581c9db0db4201c42cbbf702f339b750989acdb1', 'ccd3f281977eb0ddda4af2e555c074d30fddd3db', WANT, REPORT_DIR, 'ahead=3 files=2', 'QA1024_DOCS_FILE', 'QA1024_CUR_DEV', 'de9b5ae25984ea29eff01d6c4e73f9bc0dc6573a', 'ada07f0536ad003754cb2a08f514fc04f8996b27', 'DEV_CONTENT_ALLOWED = {}', ': DV}', "grep -q 'ROUND 1'", 'MERGE ADDENDUM', 'NOT-TESTED.written-first.md', 'exit 19', 'exit 21', 'exit 22', 'exit 23', 'exit 24', 'exit 25', 'exit 16', T)}
print('output controls', {k[:24] + ('…' if len(k) > 24 else ''): v for k, v in ctl.items()})
want = {'ahead=3 files=2': 2, ': DV}': 16, 'DEV_CONTENT_ALLOWED = {}': 1, T: 1, 'QA1024_DOCS_FILE': 5, 'QA1024_CUR_DEV': 5}
for k, v in want.items():
    if ctl[k] != v: print('REFUSE control', k, ctl[k], 'want', v); sys.exit(1)
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
