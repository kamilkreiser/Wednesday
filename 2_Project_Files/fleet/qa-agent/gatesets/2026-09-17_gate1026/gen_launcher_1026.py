#!/usr/bin/env python3
"""gen_launcher_1026.py — derive launch_qa_secuura_ks839_1026.sh from launchers/launch_qa_secuura_ks1202_1024.sh (the #1024 ROUND 1 launcher) by ASSERTED
substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing. Re-points at #1026 (KS-839) ROUND 1: head 8ab493354,
merge-base = develop efaaa6034 (an ANCESTOR of the head): compare develop...head = merge_base efaaa6034 ahead 3 files 2 (behind NOT asserted). The develop arm
judges THIRTEEN files by blob (auth services/oauth.ts LANDED = #1026s blob; the ks839 test LANDED = #1026s blob), with NO region judgement (a one-line fix: any other
oauth.ts blob refuses). GUARDED move paths: services/auth/, packages/shared/, the Dev lockfile, plus api-gateway src/middleware/scopes.ts (the gate probe judge).
Exits unchanged 2..25 (19 LANDED, 24 report dir + NOT-TESTED, 25 MERGE ADDENDUM). Test hooks QA1026_*. Then a RESIDUAL GUARD, output controls, heredoc parity,
no git write verb, bash -n. Never overwrites an existing output (writes a .pre-* copy first).
Usage: gen_launcher_1026.py <template launcher> <output launcher>"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1026', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = '8ab493354bbdb3fa52d2eb14654492db1a891e4a'; DEVSHA = 'efaaa6034f036dd9538ee35b189217b1d08b90a9'
BLOBS = {}
for f in ('services/auth/src/services/oauth.ts', 'services/auth/src/routes/oauth.ts', 'services/auth/src/services/jwt.ts', 'services/auth/src/auth.openapi.ts', 'services/auth/package.json',
          'services/auth/vitest.config.ts', 'services/auth/vitest.setup.ts', 'services/auth/tsconfig.json', 'packages/shared/src/security/scopes.ts', 'packages/shared/src/validation/index.ts',
          'services/api-gateway/src/middleware/scopes.ts', 'package-lock.json'):
    r = subprocess.run(['git', '-C', REPO, 'rev-parse', DEVSHA + ':Blockchain/Dev/' + f], capture_output=True, text=True); assert r.returncode == 0, r.stderr
    BLOBS[f] = r.stdout.strip()
HB = {f: subprocess.run(['git', '-C', REPO, 'rev-parse', H + ':Blockchain/Dev/' + f], capture_output=True, text=True).stdout.strip() for f in ('services/auth/src/services/oauth.ts', 'services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts')}
assert BLOBS['services/auth/src/services/oauth.ts'].startswith('e9953d376') and HB['services/auth/src/services/oauth.ts'].startswith('b10182890') and HB['services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts'].startswith('4e847a4f0')
print('develop blobs read with git rev-parse (a read verb):', {k.split('/')[-1]: v[:9] for k, v in BLOBS.items()})
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks839-1026-8ab493354-tier1-r1/'
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
HEADER_OLD = cut('#!/bin/bash\n', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """#!/bin/bash
# launch_qa_secuura_ks839_1026.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate (round 1 of 2 under the cap) over Secuura/Blockchain PR #1026
# (KS-839, Seat A) @ 8ab493354bbdb3fa52d2eb14654492db1a891e4a — services/auth validateScopes (services/oauth.ts:353): an OAuth app allow-list holding the
# wildcard * now grants NOTHING (return requested -> return []), plus a 52-line vitest test. Fix commit cb2ed18d9 (parent f8c7aaa39); the head merges develop
# 581c9db0d then efaaa6034; tree 8158ff5da. TIER 1: an OAuth scope grant on the authorize path. Kam ruled grants-nothing = option E (card
# secuura-ks839-oauth-wildcard-scope-grants-everything, 15:09:35 AEST) and said: yes, merge KS-839 on your go. Wednesday merges on this gate GO.
#
# THE SHAPE, as read 19:28-19:35 AEST 2026-09-17 (git ls-remote + the PR, compare, branches and contents APIs agree): develop efaaa6034 is an ANCESTOR of the
# head: compare develop...head = merge_base efaaa6034, ahead 3, behind 0, files 2 (asserted as merge_base + ahead + files, exit 10; behind NOT asserted).
# Drafter merged tree over efaaa6034 = 8158ff5dafad138c52359d2525e2cc72ff15486b (the head tree); over #1025s head 9954a7069 = 2455003d0 (disjoint).
#
# The develop pin is judged by CONTENT, not bare: (a) THIRTEEN files by blob at the CURRENT develop — the PR two (auth services/oauth.ts e9953d376, the ks839
# test ABSENT; at their #1026 blobs -> exit 19 LANDED), auth routes/oauth.ts / services/jwt.ts / auth.openapi.ts / package.json / vitest.config.ts /
# vitest.setup.ts / tsconfig.json, shared security/scopes.ts + validation/index.ts, api-gateway middleware/scopes.ts, the Dev lockfile — any blob nobody
# pinned -> exit 18 (NO partial-content judgement: a one-line fix); (b) if develop moved past efaaa6034, the compare pinned...develop REFUSES (exit 18) when the delta
# touches a GUARDED path — services/auth/, packages/shared/, the Dev lockfile, api-gateway src/middleware/scopes.ts (DEV_CONTENT_ALLOWED is EMPTY), or the
# move cannot be judged. #1025 (scripts/audit/audit-baseline.json) landing first is disjoint and clears.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY, and the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM (the merge seat equality targets and the In Progress hold ride on it).
# QA1026_CUR_DEV (test override, --check only): stands in for origin develop so the GUARDED refusals can be proven.
# QA1026_OAUTH_FILE (test fixture, --check only): a local file stands in for develop services/auth/src/services/oauth.ts (its git blob) so the clear,
# refuse and LANDED arms can be proven without a real develop commit.
# A launch with any QA1026_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1026/gen_launcher_1026.py from the #1024 ROUND 1 launcher (asserted substitutions + residual guard + output
# controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1026 ROUND 1.
#
# Usage: launch_qa_secuura_ks839_1026.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
BODY_OLD = cut('cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]\n', 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/originate/src/ + its config files, the api-gateway create/verify/auth/index files, docs/openapi/, eslint.config.mjs, the Dev lockfile) or documents.ts cleared by its region judgement; %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)\n')
A = 'services/auth/'
BODY_NEW = '''cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
AU = D + "services/auth/"
SH = D + "packages/shared/"
OAUTH = AU + "src/services/oauth.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  OAUTH:                                                            ({"@@B:services/auth/src/services/oauth.ts@@": DV}, {"@@HB:services/auth/src/services/oauth.ts@@": "#1026 own"}),
  AU + "src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts": ({"ABSENT": DV}, {"@@HB:services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts@@": "#1026 own"}),
  AU + "src/routes/oauth.ts":                                       ({"@@B:services/auth/src/routes/oauth.ts@@": DV}, {}),
  AU + "src/services/jwt.ts":                                       ({"@@B:services/auth/src/services/jwt.ts@@": DV}, {}),
  AU + "src/auth.openapi.ts":                                       ({"@@B:services/auth/src/auth.openapi.ts@@": DV}, {}),
  AU + "package.json":                                              ({"@@B:services/auth/package.json@@": DV}, {}),
  AU + "vitest.config.ts":                                          ({"@@B:services/auth/vitest.config.ts@@": DV}, {}),
  AU + "vitest.setup.ts":                                           ({"@@B:services/auth/vitest.setup.ts@@": DV}, {}),
  AU + "tsconfig.json":                                             ({"@@B:services/auth/tsconfig.json@@": DV}, {}),
  SH + "src/security/scopes.ts":                                    ({"@@B:packages/shared/src/security/scopes.ts@@": DV}, {}),
  SH + "src/validation/index.ts":                                   ({"@@B:packages/shared/src/validation/index.ts@@": DV}, {}),
  D + "services/api-gateway/src/middleware/scopes.ts":               ({"@@B:services/api-gateway/src/middleware/scopes.ts@@": DV}, {}),
  D + "package-lock.json":                                          ({"@@B:package-lock.json@@": DV}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QA1026_OAUTH_FILE", "") if f == OAUTH else ""
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1026 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= the head second parent, an ANCESTOR of the head: drafter merged tree 8158ff5dafad138c52359d2525e2cc72ff15486b = the head tree; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [AU,
           SH,
           D + "package-lock.json",
           D + "services/api-gateway/src/middleware/scopes.ts"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. Every guarded hit falls through to exit 18. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 8ab493354 in its own clone, rebuilds the shared dist there, runs the services/auth suite and the authorize, padded-carrier and seeded-app censuses on the MERGED tree beside the develop and head trees, names the merged-tree OID and re-derives every count, above all the services/auth denominator (brief items 1, 4, 5)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/auth/, packages/shared/, the Dev lockfile, api-gateway src/middleware/scopes.ts); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
'''
for f, b in BLOBS.items():
    BODY_NEW = BODY_NEW.replace('@@B:' + f + '@@', b)
for f, b in HB.items():
    BODY_NEW = BODY_NEW.replace('@@HB:' + f + '@@', b)
assert '@@' not in BODY_NEW, [l for l in BODY_NEW.splitlines() if '@@' in l][:3]
T = '[QA -> Wednesday] TIER 1 GATE #1026 (KS-839) 8ab493354'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1024_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.md}"', 'BRIEF="${QA1026_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1026-ks839-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1024_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1026_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1026-ks839-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1202-the-served-document-type-comes-from-datadocumenttype-which'", "BRANCH='refs/heads/feature/ks-839-security-an-allowedscopes-of-bypasses-the-invalid_scope'", 1),
 ('head var', 'HEAD_SHA="${QA1024_HEAD:-d1a3280880d85ff31fd409aa1b5a16c428c4bb9a}"', 'HEAD_SHA="${QA1026_HEAD:-8ab493354bbdb3fa52d2eb14654492db1a891e4a}"', 1),
 ('merge-base', "MERGE_BASE='581c9db0db4201c42cbbf702f339b750989acdb1'   # the merge-base of the head with develop = #1019s squash, the second parent of the head merge d1a328088",
  "MERGE_BASE='efaaa6034f036dd9538ee35b189217b1d08b90a9'   # the merge-base of the head with develop = develop itself, the second parent of the head merge 8ab493354", 1),
 ('develop', "DEVELOP_SHA='81ee4b729e86a645fc9098aafa1aaf39035a9950'   # develop at draft close = #1021s squash on 581c9db0d, NOT an ancestor of the head (git ls-remote 18:24:04, branches API 18:24:23 AEST)",
  "DEVELOP_SHA='efaaa6034f036dd9538ee35b189217b1d08b90a9'   # develop at draft close, an ANCESTOR of the head (git ls-remote 19:28:15, branches API 19:34:10 AEST)", 1),
 ('report dir', "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/'", "REPORT_DIR='" + REPORT_DIR + "'", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1024-ks1202-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1026-ks839-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1024 — $HEAD_SHA', 'REFUSING: #1026 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1024 = 581c9db0d ahead 3 files 2 (behind 1 at draft close = #1021; behind deliberately not asserted).', '# develop...#1026 = efaaa6034 ahead 3 files 2 (behind 0 at draft close; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1024 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1026 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''', 1),
 ('develop comment', '# The develop pin, judged by CONTENT (see the header): sixteen files by blob at the CURRENT develop (documents.ts also by region), then — if develop',
                     '# The develop pin, judged by CONTENT (see the header): thirteen files by blob at the CURRENT develop, then — if develop', 1),
 ('cur dev', 'CUR_DEV="${QA1024_CUR_DEV:-', 'CUR_DEV="${QA1026_CUR_DEV:-', 1),
 ('body', BODY_OLD, BODY_NEW, 1),
 ('subject', "grep -qF '[QA -> Wednesday] TIER 1 GATE #1024 (KS-1202) d1a328088' \"$PROMPT_FILE\"", "grep -qF '" + T + "' \"$PROMPT_FILE\"", 1),
 ('check head', 'echo "  head on origin: #1024 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1026 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1024 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1026 = $COMPARE"', 1),
 ('check cur dev', '[ -n "${QA1024_CUR_DEV:-}" ] && echo "  (develop read from the QA1024_CUR_DEV test override, not ls-remote)"', '[ -n "${QA1026_CUR_DEV:-}" ] && echo "  (develop read from the QA1026_CUR_DEV test override, not ls-remote)"', 1),
 ('check fixture', '[ -n "${QA1024_DOCS_FILE:-}" ] && echo "  (develop originate routes/documents.ts read from the QA1024_DOCS_FILE fixture, not the contents API)"', '[ -n "${QA1026_OAUTH_FILE:-}" ] && echo "  (develop services/auth/src/services/oauth.ts read from the QA1026_OAUTH_FILE fixture, not the contents API)"', 1),
 ('exit16', '[ -z "${QA1024_BRIEF:-}${QA1024_PROMPT:-}${QA1024_HEAD:-}${QA1024_CUR_DEV:-}${QA1024_DOCS_FILE:-}" ]', '[ -z "${QA1026_BRIEF:-}${QA1026_PROMPT:-}${QA1026_HEAD:-}${QA1026_CUR_DEV:-}${QA1026_OAUTH_FILE:-}" ]', 1),
]
for name, old, new, n in REPL:
    c = s.count(old)
    if c != n: print('REFUSE anchor', name, 'count', c, 'want', n); sys.exit(1)
    s = s.replace(old, new); print('  ok', name, c)
RES = s.replace('#1024 ROUND 1 launcher', '')  # the one legitimate mention: the template it was generated from
for tok in ('QA1024', '1024', 'KS-1202', 'd1a328088', '81ee4b729', '581c9db0db4201c', 'documents.ts', 'DOCS', 'originate', 'ccd3f2819', 'SEGS', 'region', '#1021', '#1019'):
    if tok in RES: print('REFUSE residual token', tok, [l[:110] for l in s.splitlines() if tok in l][:4]); sys.exit(2)
ctl = {k: s.count(k) for k in (H, DEVSHA, '8158ff5dafad138c52359d2525e2cc72ff15486b', REPORT_DIR, 'ahead=3 files=2', 'QA1026_OAUTH_FILE', 'QA1026_CUR_DEV', HB['services/auth/src/services/oauth.ts'], HB['services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts'], 'DEV_CONTENT_ALLOWED = {}', ': DV}', "grep -q 'ROUND 1'", 'MERGE ADDENDUM', 'NOT-TESTED.written-first.md', 'exit 19', 'exit 21', 'exit 22', 'exit 23', 'exit 24', 'exit 25', 'exit 16', T)}
print('output controls', {k[:24] + ('…' if len(k) > 24 else ''): v for k, v in ctl.items()})
want = {'ahead=3 files=2': 2, ': DV}': 13, 'DEV_CONTENT_ALLOWED = {}': 1, T: 1, 'QA1026_OAUTH_FILE': 5, 'QA1026_CUR_DEV': 5, HB['services/auth/src/services/oauth.ts']: 1, 'exit 19': 2, 'exit 21': 3}
for k, v in want.items():
    if ctl[k] != v: print('REFUSE control', k[:40], ctl[k], 'want', v); sys.exit(1)
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
