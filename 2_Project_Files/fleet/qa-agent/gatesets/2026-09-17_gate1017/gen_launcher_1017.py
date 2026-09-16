#!/usr/bin/env python3
"""gen_launcher_1017.py — derive launch_qa_secuura_ks1195_1017.sh from launchers/launch_qa_secuura_ks1176_1014r2.sh (the #1014 ROUND 2 launcher, itself generated
by gen_launcher_1014r2.py) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.
Re-points at #1017 (KS-1195) ROUND 1: head cbe29597d / merge-base 7e89318bc / develop fa887f382 (#1014's squash, which LANDED during drafting; develop is not
an ancestor of the head: compare develop...head = merge_base 7e89318bc ahead 2 behind 1 files 5 — behind NOT asserted). The develop arm is judged by CONTENT:
TWENTY-ONE files by blob at the current develop (the PR's five at their head blobs -> exit 19 LANDED); middleware/auth.ts, middleware/rateLimitEnforce.ts and
src/index.ts at ANY OTHER blob are judged by REGION content (auth.ts and rateLimitEnforce.ts from their first import to EOF; index.ts from the global limiter to
the platform mount) and index.ts additionally by its three ks781 PIN LINES (846/859/892 must still hold their body-parser sites — the KS-953 class): a move
into a region or a pin shift refuses exit 18, a move outside clears; --check-only fixtures QA1017_AUTH_FILE / QA1017_RLE_FILE / QA1017_INDEX_FILE prove both
arms. Past fa887f382 the compare refuses (exit 18) on a delta touching a GUARDED path unless the hit is one of the three files cleared by its region judgement.
Round-1 rules replace the template's round-N exits: exit 15 ROUND 1; exit 24 brief AND prompt name the REPORT DIRECTORY and prompt names
NOT-TESTED.written-first.md; exit 25 brief AND prompt carry the MERGE ADDENDUM. Then a RESIDUAL GUARD (no #1014-round-2-only token survives outside the
permitted mentions), output controls, heredoc apostrophe/paren parity, no git write verb, no control bytes, bash -n. Region SHAs are computed HERE from the base
blobs saved in src/ (git blob asserted), not typed in. Never overwrites an existing output (writes a .pre-* copy first if one exists).
Usage: gen_launcher_1017.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017'
s = open(TPL).read()
print('gen_launcher_1017', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:50], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]

# ---- region SHAs from the base blobs (asserted) ----
def gitblob(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
REG = {}
for key, fname, blob, a, b in (('AUTH', 'B.middleware_auth.ts', '20311010db0eb8ba097644ce105cf8df966ce456', 'import { Request, Response, NextFunction, RequestHandler } from', None),
                               ('RLE', 'B.middleware_rateLimitEnforce.ts', 'fc5c5a4d934384745565e730cd12c0a0fcfcaa70', 'import { Request, Response, NextFunction } from', None),
                               ('IDX', 'B.index.ts', '6f38c819e48162e3179aaf557085766f91beecc1', '// Global rate limiter', 'PLATFORM / MULTI-TENANCY ROUTES')):
    raw = open(GS + '/src/' + fname, 'rb').read(); assert gitblob(raw) == blob, (fname, gitblob(raw)); t = raw.decode()
    assert t.count(a) == 1 and (b is None or t.count(b) == 1), (fname, 'anchor counts')
    i = t.index(a); seg = t[i:] if b is None else t[i:t.index(b) + len(b)]
    REG[key] = hashlib.sha256(seg.encode()).hexdigest(); print('  region', key, 'from base blob', blob[:9], 'sha', REG[key][:16], 'chars', len(seg))
    if key == 'IDX':
        L = t.split('\n')
        for n, sub in ((846, '/api/auth/wallet/challenge'), (859, '/api/auth/wallet/authenticate'), (892, 'authenticateToken, mockBodyParser, query, isDbAvailable')):
            assert sub in L[n - 1], ('pin line', n)
        print('  pins 846/859/892 hold their sites in the base index.ts')

REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'

HEADER_OLD = cut('# launch_qa_secuura_ks1176_1014r2.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1195_1017.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate (round 1 of 2 under the cap) over Secuura/Blockchain
# PR #1017 (KS-1195, Seat A) @ cbe29597d11e59f2e1a14519e9ba3dbf6de9a756 — the per-key rate limiter (enforceClientRateLimit) now runs as the continuation of each
# req.user-setting branch of authenticateToken (middleware/auth.ts +11 -3), inside that branch's runWithTenantId, with a once-per-request WeakSet guard
# (middleware/rateLimitEnforce.ts +12); the dead app-level mount at index.ts:522-524 is removed (+2 -3); a new 8-cell ks1195 test; a second, test-only commit
# re-pins the packages/shared ks781 body-parser line numbers by -1. TIER 1: auth middleware on every authenticated route.
#
# THE SHAPE, as read 08:30-08:55 AEST 2026-09-17 (git ls-remote + the PR, compare and commits APIs agree): merge-base = the PR parent 7e89318bc (#1016s squash);
# develop moved DURING drafting to fa887f382 = #1014s squash (KS-1176, merged 08:44:35 AEST: routes/verification.ts -> 28fb58343, services/enforcement.ts ->
# be466fbf4, a ks1176 test 43cebf8d7; tree 5748a1d68 = the drafter local squash), so develop is NOT an ancestor of the head: compare develop...head =
# merge_base 7e89318bc, diverged, ahead 2, behind 1, files 5. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT
# asserted — the develop arm judges every move by CONTENT. Drafter merged tree (head x fa887f382): 135b07468.
#
# The develop pin is judged by CONTENT, not bare: (a) TWENTY-ONE files by blob at the CURRENT develop — the PR's five (auth.ts 20311010d, rateLimitEnforce.ts
# fc5c5a4d9, index.ts 6f38c819e, the ks1195 test ABSENT, the packages/shared ks781 test ca1fe34a7; at their head blobs -> exit 19 LANDED), #1014s three at their
# squash blobs, services/redis.ts, routes/proxy.ts, middleware/audit.ts, rateLimitEnforce.test.ts, api-gateway package.json / vitest.config.ts / vitest.setup.ts /
# tsconfig.json, Dev eslint.config.mjs, packages/shared db/tenant-guc.ts, services/security/src/index.ts (the validate producer) and docs/openapi/secuura-api.yaml
# — any blob nobody pinned -> exit 18; auth.ts, rateLimitEnforce.ts and index.ts at ANY OTHER blob are judged by REGION content (auth.ts and rateLimitEnforce.ts
# from their first import to EOF; index.ts from the global limiter to the platform mount, PLUS its ks781 pin lines 846/859/892 must still hold their sites):
# a move into a region or a pin shift refuses (exit 18), a move outside clears; (b) if develop moved past fa887f382, the compare pinned...develop REFUSES
# (exit 18) when the delta touches a GUARDED path — services/api-gateway/src/ and its config files, packages/shared/src/, services/security/src/index.ts, the
# auth JWT mint + internal route, eslint.config.mjs, the Dev lockfile, docs/openapi/ — unless the hit is one of the three region-judged files and its
# judgement cleared it (DEV_CONTENT_ALLOWED is EMPTY), or the move cannot be judged.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY, and the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM template (the merge seat's equality targets and the deploy precondition ride on it).
# QA1017_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1017_AUTH_FILE / QA1017_RLE_FILE / QA1017_INDEX_FILE (test fixtures, --check only): a local file stands in for develop's copy of that file (content AND git
# blob) so each region judgement's clear and refuse arms can be proven without a real develop commit.
# A launch with any QA1017_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1017/gen_launcher_1017.py from launch_qa_secuura_ks1176_1014r2.sh (asserted substitutions + residual
# guard + output controls + bash -n): same guard set and exit codes 2..23, re-pointed at #1017 round 1, with round-1 exits 24/25. Exit codes 2..25 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks1195_1017.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""

VARS_OLD = cut('BRIEF="${QA1014R2_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1014r2-ks1176-tier1.md"\n')
VARS_NEW = '''BRIEF="${QA1017_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017-ks1195-tier1.md}"
PROMPT_FILE="${QA1017_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017-ks1195-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1195-api-gateway-per-key-rate-limiter-never-fires'
HEAD_SHA="${QA1017_HEAD:-cbe29597d11e59f2e1a14519e9ba3dbf6de9a756}"
MERGE_BASE='7e89318bcedbc9a35757d4298ace54a6a23020bd'   # the merge-base of the head with develop = the PR parent of 973eb49ef (#1016s squash)
DEVELOP_SHA='fa887f382b212b8da4a0a4a556bacb05ea34daaa'   # develop at draft close = #1014s squash on 7e89318bc, NOT an ancestor of the head (branches API 08:49:54 + 08:51:46, git ls-remote 08:52:38 AEST; #1014 merged 08:44:35)
REPORT_DIR=\'''' + REPORT_DIR + '''\'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017-ks1195-tier1.md"
'''

PYJ_OLD = cut('import hashlib, json, os, sys, urllib.request, urllib.error\n', '% (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)\n')
PYJ_NEW = r'''import hashlib, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
def raw(path, ref):
    return urllib.request.urlopen(urllib.request.Request(api + "/contents/" + path + "?ref=" + ref, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github.raw"}), timeout=60).read().decode("utf-8")
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
G = D + "services/api-gateway/"
AUTH = G + "src/middleware/auth.ts"
RLE = G + "src/middleware/rateLimitEnforce.ts"
IDX = G + "src/index.ts"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  AUTH:                                                                ({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {"8fbe102eb58cc1cb7c39c242c88fad1f2d489841": "#1017 own"}),
  RLE:                                                                 ({"fc5c5a4d934384745565e730cd12c0a0fcfcaa70": "base"}, {"f4b66aa1abb8b337e3fa00aaf6ebba97ffb5745d": "#1017 own"}),
  IDX:                                                                 ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {"db127dbfa5dd899b0a8e0d844690890d91e27f10": "#1017 own"}),
  G + "src/__tests__/ks1195-per-key-rate-limiter-runs-after-authentication.test.ts": ({"ABSENT": "base"}, {"ade08ac1ebd2a7305a7e253a79a78c63099bf5c0": "#1017 own"}),
  D + "packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts": ({"ca1fe34a74880305cebf87e034d9d9ffa9c94f3c": "base"}, {"bc4815c4ec9cae2f065e29dec6b938cdf49f2d23": "#1017 own"}),
  G + "src/routes/verification.ts":                                    ({"28fb5834308a502f5f7b806e3b49a77627601eff": "develop = #1014 squash fa887f382"}, {}),
  G + "src/services/enforcement.ts":                                   ({"be466fbf444178bbb41293fb1d811957e55e1d2d": "develop = #1014 squash fa887f382"}, {}),
  G + "src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts": ({"43cebf8d75376f5a40252c5096fd02747c4f0a9e": "develop = #1014 squash fa887f382"}, {}),
  G + "src/services/redis.ts":                                         ({"47659ee9c9f06acf9ac64e09b2dc207113ba92ea": "base"}, {}),
  G + "src/routes/proxy.ts":                                           ({"b99f45a4c9c89088a7809de5f26c4f56fc94819c": "base"}, {}),
  G + "src/middleware/audit.ts":                                       ({"052131de06c3f510e4bcaadc9b6831d0cca617c2": "base"}, {}),
  G + "src/__tests__/rateLimitEnforce.test.ts":                        ({"b5fa8a17b981d8bd0470c74ad880f45f48551de4": "base"}, {}),
  G + "package.json":                                                  ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),
  G + "vitest.config.ts":                                              ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),
  G + "vitest.setup.ts":                                               ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),
  G + "tsconfig.json":                                                 ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),
  D + "eslint.config.mjs":                                             ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
  D + "packages/shared/src/db/tenant-guc.ts":                          ({"86953b978062eb1d124abf3154fa1da324c6e110": "base"}, {}),
  D + "services/security/src/index.ts":                                ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                                 ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
}
# REGION judgement for the three product files (brief items 1-9 stand on them); the SHAs were computed by the generator from the base blobs.
REGION = {
  AUTH: ["import { Request, Response, NextFunction, RequestHandler } from", "", "@@AUTH_SHA@@", "QA1017_AUTH_FILE"],
  RLE:  ["import { Request, Response, NextFunction } from", "", "@@RLE_SHA@@", "QA1017_RLE_FILE"],
  IDX:  ["// Global rate limiter", "PLATFORM / MULTI-TENANCY ROUTES", "@@IDX_SHA@@", "QA1017_INDEX_FILE"],
}
# the ks781 body-parser line pins (packages/shared) read index.ts BY LINE: at develop they must still hold their sites, or the merged shared suite goes red
PINS = [[846, "/api/auth/wallet/challenge"], [859, "/api/auth/wallet/authenticate"], [892, "authenticateToken, mockBodyParser, query, isDbAvailable"]]
def region_sha(text, a, b):
    if text.count(a) != 1:
        return "anchor-count-" + str(text.count(a))
    i = text.index(a)
    if not b:
        return hashlib.sha256(text[i:].encode()).hexdigest()
    if text.count(b) != 1:
        return "end-anchor-count-" + str(text.count(b))
    j = text.index(b)
    if j < i:
        return "end-before-start"
    return hashlib.sha256(text[i:j + len(b)].encode()).hexdigest()
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get(REGION[f][3], "") if f in REGION else ""
    try:
        if fixture:
            data = open(fixture, "rb").read()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1017 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok and f in REGION:
        try:
            text = open(fixture).read() if fixture else raw(f, cur)
        except Exception as e:
            print("UNJUDGEABLE develop " + short + " content unreadable: " + type(e).__name__); sys.exit(0)
        a, b, want, _ = REGION[f]
        rs = region_sha(text, a, b)
        if rs != want:
            print("GUARDED develop " + short + " blob " + blob[:9] + " — the #1017 region changed: region " + rs[:16] + " vs pinned " + want[:16]); sys.exit(0)
        if f == IDX:
            lines = text.split("\n")
            moved = [str(n) for n, sub in PINS if len(lines) < n or sub not in lines[n - 1]]
            if moved:
                print("GUARDED develop " + short + " blob " + blob[:9] + " — the ks781 body-parser pin lines moved: line " + ",".join(moved) + " no longer holds its site, so the merged packages/shared suite would go red — the KS-953 class"); sys.exit(0)
        content_cleared.add(f)
        state.append(f.split("/")[-1] + " " + blob[:9] + " = moved OUTSIDE the #1017 region, judged by content: region " + rs[:12] + ("; pins 846/859/892 hold" if f == IDX else ""))
        continue
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= #1014 squash on #1016 squash, NOT an ancestor of the head: the gate merges it; drafter merged tree 135b07468c0f12279836c43051e16d5ff1053398; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [G + "src/",
           G + "package.json",
           G + "vitest.config.ts",
           G + "vitest.setup.ts",
           G + "tsconfig.json",
           D + "packages/shared/src/",
           D + "services/security/src/index.ts",
           D + "services/auth/src/services/jwt.ts",
           D + "services/auth/src/routes/internal.ts",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: auth.ts / rateLimitEnforce.ts / index.ts are judged by their REGION content above, not by a blob here; every other
# guarded hit falls through to exit 18 — dependabot #649 / #575, the lockfile PRs, #922 docs/openapi and #923 / #995 api-gateway included. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if (h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h]) or h in content_cleared)
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto cbe29597d in its own clone, rebuilds the shared dist there, runs the api-gateway suite, packages/shared and the route-family, double-count and principal censuses on the MERGED tree beside the base and head trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 2, 3, 11)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/api-gateway/src/ + its config files, packages/shared/src/, services/security/src/index.ts, the auth JWT mint + internal route, docs/openapi/, eslint.config.mjs, the Dev lockfile) or auth.ts / rateLimitEnforce.ts / index.ts cleared by their region judgement; %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
'''
PYJ_NEW = PYJ_NEW.replace('@@AUTH_SHA@@', REG['AUTH']).replace('@@RLE_SHA@@', REG['RLE']).replace('@@IDX_SHA@@', REG['IDX'])
assert '@@' not in PYJ_NEW

REPL = [
  # (label, old, new, expected count)
  ('header', HEADER_OLD, HEADER_NEW, 1),
  ('vars', VARS_OLD, VARS_NEW, 1),
  ('head refuse', 'REFUSING: #1014 ROUND 2 — $HEAD_SHA', 'REFUSING: #1017 — $HEAD_SHA', 1),
  ('compare comment', '# develop...#1014 = e0f41a8fa ahead 2 files 3 (behind 3 at draft close; behind deliberately not asserted).', '# develop...#1017 = 7e89318bc ahead 2 files 5 (behind 1 at draft close; behind deliberately not asserted).', 1),
  ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=3" ] || { echo "REFUSING: #1014 ROUND 2 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=3'" >&2; exit 10; }''',
                     '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=5" ] || { echo "REFUSING: #1017 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=5'" >&2; exit 10; }''', 1),
  ('count comment', '# The develop pin, judged by CONTENT (see the header): eighteen files by blob at the CURRENT develop, then — if develop',
                    '# The develop pin, judged by CONTENT (see the header): twenty-one files by blob at the CURRENT develop (three of them also by region), then — if develop', 1),
  ('cur dev', 'CUR_DEV="${QA1014R2_CUR_DEV:-', 'CUR_DEV="${QA1017_CUR_DEV:-', 1),
  ('pyj', PYJ_OLD, PYJ_NEW, 1),
  ('landed msg', 'LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;',
                 'LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;', 1),
  ('round grep', '''grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 2)" >&2; exit 15; }''',
                 '''grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }''', 1),
  ('subject + round-1 rules',
   '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1014 ROUND 2 (KS-1176) 9ba0caf78' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not carry the exact ROUND 2 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$R1_REPORT" "$PROMPT_FILE" && grep -qF "$R1_REPORT" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the prior round REPORT path $R1_REPORT — the QA agent has no inbox; a carry-forward with no pointer can only be answered with I could not" >&2; exit 24; }
grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not require the per-finding CLOSED / STILL OPEN / NEW disposition — round 2 of 2: closed instances ship and residue is ticketed" >&2; exit 25; }
''',
   '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1017 (KS-1195) cbe29597d' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" \\
  || { echo "REFUSING: brief or prompt does not name the report directory $REPORT_DIR, or the prompt does not name NOT-TESTED.written-first.md — the report must land where Wednesday reads it, NOT-TESTED first" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MERGE ADDENDUM' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM — the merge seat's equality targets and the deploy precondition ride on it" >&2; exit 25; }
''', 1),
  ('check round', 'echo "  brief and prompt agree on TIER 1 and ROUND 2"', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 1),
  ('check subject', 'echo "  prompt carries the exact ROUND 2 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the prior round REPORT path"\n  echo "  brief and prompt require CLOSED / STILL OPEN / NEW per finding"\n',
                    'echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory; prompt names NOT-TESTED.written-first.md"\n  echo "  brief and prompt carry the MERGE ADDENDUM"\n', 1),
  ('check head', 'echo "  head on origin: #1014 ROUND 2 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1017 $HEAD_SHA at $BRANCH"', 1),
  ('check compare', 'echo "  compare (GitHub API): develop...#1014 ROUND 2 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1017 = $COMPARE"', 1),
  ('check fixture echo', '  [ -n "${QA1014R2_CUR_DEV:-}" ] && echo "  (develop read from the QA1014R2_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1014R2_VERIF_FILE:-}" ] && echo "  (develop verification.ts read from the QA1014R2_VERIF_FILE fixture, not the contents API)"\n',
   '  [ -n "${QA1017_CUR_DEV:-}" ] && echo "  (develop read from the QA1017_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1017_AUTH_FILE:-}${QA1017_RLE_FILE:-}${QA1017_INDEX_FILE:-}" ] && echo "  (a develop product file read from a QA1017_*_FILE fixture, not the contents API)"\n', 1),
  ('exit16 fixture', '[ -z "${QA1014R2_BRIEF:-}${QA1014R2_PROMPT:-}${QA1014R2_HEAD:-}${QA1014R2_CUR_DEV:-}${QA1014R2_VERIF_FILE:-}" ]',
                     '[ -z "${QA1017_BRIEF:-}${QA1017_PROMPT:-}${QA1017_HEAD:-}${QA1017_CUR_DEV:-}${QA1017_AUTH_FILE:-}${QA1017_RLE_FILE:-}${QA1017_INDEX_FILE:-}" ]', 1),
]
bad = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want:
        print('ANCHOR COUNT', label, n, '!=', want); bad += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if bad: print('REFUSING: %d anchors disagreed; nothing written' % bad); sys.exit(1)
RESID = ['QA1014R2_', 'ROUND 2', 'eighteen', '9ba0caf78b8ddb737541df38303b776c982521d2', 'e0f41a8fa', 'R1_REPORT', 'CLOSED / STILL OPEN / NEW', '70426094413b', 'spelling census',
         '5748a1d68318ed2e310a360fb79e7a1ebc63c785x', 'VERIF_FILE', 'a7a6d46057a18b3460e7d08bbec5df12ab763a81', 'ks1176-1014-616c766a5', 'originate/src/routes/documents.ts', 'KS-1176)', 'allow-list', 'DocumentUpload']
PERMITTED = {'from launch_qa_secuura_ks1176_1014r2.sh': 1}  # the template-name provenance mention
stripped = s
for k, v in PERMITTED.items():
    if stripped.count(k) != v: print('PERMITTED count', repr(k), stripped.count(k), '!=', v); sys.exit(1)
    stripped = stripped.replace(k, '')
res = {t: stripped.count(t) for t in RESID if t in stripped}
if res: print('REFUSING: residual tokens', res); sys.exit(2)
CTL = {'#1017': None, 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756': 2, '7e89318bcedbc9a35757d4298ace54a6a23020bd': 1, 'fa887f382b212b8da4a0a4a556bacb05ea34daaa': 1,
       REG['AUTH']: 1, REG['RLE']: 1, REG['IDX']: 1, 'content_cleared': 3, '135b07468c0f12279836c43051e16d5ff1053398': 1, REPORT_DIR: 1,
       'QA1017_': None, 'QA1017_AUTH_FILE': 4, 'QA1017_RLE_FILE': 4, 'QA1017_INDEX_FILE': 4, '"ABSENT"': None, 'exit 19': None, 'exit 22': None, 'exit 23': None, 'exit 24': None,
       'exit 25': None, 'exit 21': None, 'exit 16': None, 'KS-1195': None, 'ROUND 1': None, 'MERGE ADDENDUM': None, 'NOT-TESTED.written-first.md': None, 'PINS': 2,
       '8fbe102eb58cc1cb7c39c242c88fad1f2d489841': 1, 'f4b66aa1abb8b337e3fa00aaf6ebba97ffb5745d': 1, 'db127dbfa5dd899b0a8e0d844690890d91e27f10': 1,
       'ade08ac1ebd2a7305a7e253a79a78c63099bf5c0': 1, 'bc4815c4ec9cae2f065e29dec6b938cdf49f2d23': 1, '28fb5834308a502f5f7b806e3b49a77627601eff': 1}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); j = s.index('\nPY' + ('J' if 'PYJ' in tag else '') + '\n', i); blk = s[i:j]
    print('heredoc', tag.strip(), "apostrophes", blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
if os.path.exists(OUT):
    pre = OUT + '.pre-' + datetime.datetime.now().strftime('%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
open(OUT, 'w').write(s); os.chmod(OUT, 0o755)
p = subprocess.run(['bash', '-n', OUT], capture_output=True, text=True)
print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: sys.exit(3)
print('written', OUT, 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
