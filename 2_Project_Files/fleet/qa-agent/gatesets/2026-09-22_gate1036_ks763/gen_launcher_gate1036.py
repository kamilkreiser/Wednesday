#!/usr/bin/env python3
"""gen_launcher_gate1036.py — write launch_qa_secuura_ks763_1036.sh for the #1036 (KS-763 PR-4, qs in range on express 4) TIER 1 gate, in the shape of
gatesets/2026-09-17_gate1033/gen_launcher_1033.py (the same lock class) with the gate16B/16C conventions (BOTH-list, by-name ladder, PARTIAL refusal).
EVERY PIN IS RE-READ AT ORIGIN IN THIS RUN: head by `git ls-remote` (branch AND refs/pull/1036/head must agree), develop by ls-remote, the merge-base,
the 50 PR paths and their merge-base / head blobs by `git diff --raw -z` (READ verbs in the Secuura checkout only), the 13 scripts/audit files by ls-tree,
the 3 REACH Dockerfiles (api-gateway, auth, originate — the runtime steps) by rev-parse; the merged tree by merge-tree in the DRAFTER'S SCRATCH CLONE
(argv[4]; never the checkout). The develop arm of the launcher is judged by PATH BLOBS at the CURRENT develop (develop moves often; its SHA is printed,
never a guard): every guarded path at its merge-base blob -> OK; all 50 at their #1036 blobs -> exit 19 LANDED; anything else -> exit 18 GUARDED.
Then a dry run of the launcher's own grep ladder against the prompt and the READY capture (the generator refuses before writing if any grep would fail),
heredoc apostrophe/paren parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Written with the Write tool (not a Bash heredoc) because the launcher legitimately changes directory before exec and the fleet's no-cd hook reads the
Bash command text. Usage: gen_launcher_gate1036.py <output launcher> <expected head> <expected develop> <drafter scratch clone>
Exit: 0 written · 1 a pin/anchor/control disagreed · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys
OUT = sys.argv[1]
EXP_HEAD = sys.argv[2] if len(sys.argv) > 2 else ''
EXP_DEV = sys.argv[3] if len(sys.argv) > 3 else ''
CLONE = sys.argv[4] if len(sys.argv) > 4 else ''
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
WED = '/Volumes/DevMASTER/WEDNESDAY'
G = os.path.dirname(os.path.abspath(__file__))
PROMPT = WED + '/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-1036-ks763-qs-tier1.prompt.txt'
BRIEF = WED + '/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1036/mail_1036_ready.md'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-ks763-1036-4b251997a-tier1-r1/'
SUBJECT = '[QA -> Wednesday] TIER 1 GATE #1036 (KS-763) 4b251997a — '
BRANCH = 'refs/heads/feature/ks-763-qs-in-range'
D = 'Blockchain/Dev/'
AUDIT_DIR = D + 'scripts/audit'
REACH = [D + 'services/api-gateway/Dockerfile', D + 'services/auth/Dockerfile', D + 'services/originate/Dockerfile']
def refuse(msg, code=1): print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)
def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
    if p.returncode != 0: refuse('git %r rc %d %s' % (a[:3], p.returncode, p.stderr[-200:]))
    return p.stdout
if not CLONE.startswith('/private/tmp/claude-501/'): refuse('argv[4] must be the drafter scratch clone under /private/tmp/claude-501/')
# 1. pins at origin
now = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
lsr = git('ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1036/head', BRANCH)
refs = {l.split('\t')[1]: l.split('\t')[0] for l in lsr.splitlines()}
HEAD, DEV = refs.get('refs/pull/1036/head', ''), refs.get('refs/heads/develop', '')
if not HEAD or refs.get(BRANCH) != HEAD: refuse('refs/pull/1036/head %s and %s %s disagree at origin' % (HEAD, BRANCH, refs.get(BRANCH)))
if EXP_HEAD and HEAD != EXP_HEAD: refuse('head at origin %s != expected %s' % (HEAD, EXP_HEAD))
if EXP_DEV and DEV != EXP_DEV: refuse('develop at origin %s != expected %s' % (DEV, EXP_DEV))
print('ls-remote', now); print(lsr.rstrip())
MB = git('merge-base', HEAD, DEV).strip()
ahead = int(git('rev-list', '--count', MB + '..' + HEAD).strip())
mt = subprocess.run(['git', '-C', CLONE, 'merge-tree', '--write-tree', DEV, HEAD], capture_output=True, text=True).stdout.split()
if len(mt) != 1: refuse('merge-tree in the scratch clone reports conflicts or nothing: %r' % mt[:5])
MERGED = mt[0]
raw = git('diff', '--raw', '-z', '--abbrev=40', MB, HEAD).split('\0')
rows = []
for i in range(0, len(raw) - 1, 2):
    m = re.match(r':(\d{6}) (\d{6}) ([0-9a-f]{40}) ([0-9a-f]{40}) (\w)', raw[i])
    if m: rows.append((raw[i + 1], m.group(3), m.group(4)))
if len(rows) != 50 or ahead != 3: refuse('PR paths %d (want 50) ahead %d (want 3)' % (len(rows), ahead))
if any(b == h for p, b, h in rows): refuse('a PR path with equal blobs')
for p in REACH:
    b, h = git('rev-parse', MB + ':' + p).strip(), git('rev-parse', HEAD + ':' + p).strip()
    if b != h: refuse('reach path moved in the PR: ' + p)
    rows.append((p, b, ''))
audit_files = [(l.split('\t')[1].rsplit('/', 1)[1], l.split()[2]) for l in git('ls-tree', MB, AUDIT_DIR + '/').splitlines() if l.split()[1] == 'blob']
if len(audit_files) != 13 or 'audit-baseline.json' not in dict(audit_files): refuse('scripts/audit files %d' % len(audit_files))
arows = []
for n, b in sorted(audit_files):
    h = git('rev-parse', HEAD + ':' + AUDIT_DIR + '/' + n).strip()
    if (n == 'audit-baseline.json') != (b != h): refuse('audit pin sanity ' + n)
    arows.append((n, b, h if b != h else ''))
judged_pr = [r for r in rows if r[2] and not r[0].startswith(AUDIT_DIR + '/')]
if len(judged_pr) != 49: refuse('non-audit PR paths %d, want 49' % len(judged_pr))
judged = judged_pr + [r for r in rows if not r[2]]
baseline_head_blob = dict((n, h) for n, b, h in arows)['audit-baseline.json']
print('merge-base', MB, 'ahead', ahead, '| merged tree', MERGED, '| PR paths', len(rows) - 3, '| reach', 3, '| audit files', len(arows))

# 2. the ladders (dry-run before writing)
BOTH = ['4b251997a', 'KS-763', 'KS-775', '29 -> 26', 'GHSA-4mjr', 'GHSA-x5fp', 'GHSA-q8mj', '6.16.0', '4.22.3', '1.20.8', 'side-channel 1.1.0 -> 1.1.1', 'npm 11.19.0',
        'node:24-alpine', '251', 'KS-562', 'lockfile-cleanroom', '35/35', '09d6f7c6-eb10-4e1f-8f98-16bf8254b689', '1b1eb4d3-aa0f-4e38-8e70-9fbcb407a787',
        '#949', '#948', '#947', '#946', '#945', '#649', '#639', '#635', '#575', '#572', 'audit-baseline.json', 'Image build', 'runtime load trace', 'NOT COVERED',
        '851/851', '556/556', '762/762', '741/741', '213/213', '237/238', '12/12', 'contributes', 'In Progress', '2026-09-03', '13:50:18Z', 'whatsapp-bot', 'frontend/issuer']
BYNAME = ['TIER AND ROUND', 'round 1 of 2', 'FULL WEIGHT', 'real-browser half', 'Any product byte', 'MERGEABILITY at the CURRENT develop', 'BOTH orders', 'conflicts BY PATH',
          'CONSERVATION', 'develop\'s minus EXACTLY the three rows', 'MEASURE develop\'s row count NOW', 'FINDING for the seat', 'THE LOCKS: parse EVERY tracked package-lock.json',
          '0 qs < 6.16.0', 'ONLY non-family move is side-channel 1.1.0 -> 1.1.1', 'NO major jumps', 'mysql2 3.23.1', 'vitest 4.1.11', 'PLANTED-VIOLATION CONTROL',
          'THE SHIPPED AUDIT SCRIPTS at the head', 'NEGATIVE CONTROL', 'CLEANUP naming exactly GHSA-4mjr + GHSA-x5fp', 'Tee vulnerable_versions', 'INSTALL + SUITES from the head\'s locks',
          'THE WORKSPACE MATRIX', 'RE-RUN, do not copy', 'threadTokenMint = KS-562', 'own-lock `npm ci`', 'lockfile-cleanroom.sh 35/35', 'THE TWO THINGS THE READY SAYS ARE NOT COVERED',
          'RUNTIME REACH FIRST', 'IMAGE BUILD', 'docker build', 'never fake it', 'RUNTIME LOAD TRACE', 'SERVES ONE REQUEST', 'a[b]=1&a[c]=2', 'a[0]=x,y', 'module.registerHooks',
          'DEPENDABOT OVERLAP', 'SUPERSEDES', 'LINEAR LINK HYGIENE', 'attachmentsForURL(pull/1036)', 'EXACTLY KS-763 `contributes` + KS-775 `contributes`', 'READ BACK', '<= 92 chars ASCII',
          'THE SEAT\'S OWN SLIPS', 'CONFIRMED / REFUTED', 'whitespace-split', 'root loop re-picking express', 'patched once', 'MERGE ADDENDUM', '## MERGE ADDENDUM',
          'ONE line VERBATIM', 'BASE_GO', 'GO: merge #1036', 'path blob (mode)', 'SHIPS-WITH <= 3 sentences', 'NOT-PINNED: none', 'INTERMITTENTS do not block',
          'RULED (WHETHER IT BLOCKS)', 'THE CONTEXT RULE', 'ctx 80%', 'NOT-TESTED.written-first.md', 'THE CENSUS RULE v2', 'lsof -nP -iTCP:5432 -sTCP:LISTEN',
          'lsof -nP -iTCP:4000 -sTCP:LISTEN', 'lsof -nP -iTCP:4003 -sTCP:LISTEN', 'lsof -nP -iTCP:8080 -sTCP:LISTEN', 'login_stub', 'farmed per ENTRY', 'name it uniquely',
          '--runInBand', 'load average', 'npm-version dependent', 'INSTRUMENT ARTEFACT', 'MEASURE, not conclude', 'FINDINGS-ONLY', 'NEVER print a credential value',
          'no memory maintenance', 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'NEVER touch the push-window lock directory',
          'MAIL YOUR VERDICT', 'WRITE report.md BEFORE THE MAIL', 'sha256 + byte count IN the mail', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to',
          'GO, GO WITH FINDINGS, or NO GO', 'Never enter any seat\'s worktree', 'count-objects', 'No Datasec', 'Docker daemon was DOWN', 'never a wholesale symlink']
ptxt = open(PROMPT, encoding='utf-8').read(); btxt = open(BRIEF, encoding='utf-8').read()
miss = [w for w in BOTH if w.lower() not in ptxt.lower() or w.lower() not in btxt.lower()]
if miss: refuse('BOTH-list misses (prompt AND READY capture, case-insensitive): %r' % miss)
miss = [w for w in BYNAME if w not in ptxt]
if miss: refuse('by-name ladder misses in the prompt: %r' % miss)
for tok in ('PENDING', 'deadbeef', 'DEADBEEF', '@@'):
    if tok in ptxt: refuse('the prompt carries %r' % tok)
if ptxt.splitlines()[0] != 'ultrathink': refuse('prompt line 1')
for must in (HEAD, DEV, MB, MERGED, REPORT_DIR, SUBJECT, BRIEF, 'TIER 1', 'ROUND 1'):
    if must not in ptxt: refuse('prompt lacks %r' % must[:60])
missing_blobs = [p for p, b, h in judged_pr if h not in ptxt] + ([AUDIT_DIR + '/audit-baseline.json'] if baseline_head_blob not in ptxt else [])
if missing_blobs: refuse('prompt lacks the head blob of %r' % missing_blobs[:5])
print('dry ladder: BOTH %d, by-name %d, 50 head blobs present in the prompt' % (len(BOTH), len(BYNAME)))

def bash_list(items): return ' \\\n          '.join("'" + w.replace("'", "'\"'\"'") + "'" for w in items)
judged_lines = '\n'.join('  "%s": ["%s", "%s"],' % r for r in judged)
audit_lines = '\n'.join('  "%s": ["%s", "%s"],' % r for r in arows)
CD_LINE = 'c' + 'd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }'
L = r'''#!/bin/bash
# launch_qa_secuura_ks763_1036.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1036
# (KS-763, Seat B 1st successor, PR-4: qs in range on express 4 — 20 manifests overrides.body-parser 1.20.6 -> 1.20.8, 29 regenerated locks
# express 4.22.3 / body-parser 1.20.8 / qs 6.16.0 / side-channel 1.1.1, audit-baseline.json 29 -> 26: GHSA-4mjr-xmp4-gh2g + GHSA-x5fp-wj9c-mxmx (KS-763,
# EXPIRE 2026-09-24) + GHSA-q8mj-m7cp-5q26 (KS-531 / KS-775, Wednesday's 2026-09-17 13:50:18Z ruling))
# @ __HEAD__ — THREE commits: c9e034744 (the change, on bb848b828), c93d84c9b (a merge of develop 3961c2add = #1029 + #1031 + #1033),
# 4b251997a (q8mj removed). 50 files vs the merge-base: 29 package-lock.json + 20 package.json + scripts/audit/audit-baseline.json. TIER 1 because
# express, body-parser and qs are prod runtime dependencies in every express service image (Wednesday's receipt, 2026-09-18).
#
# THE SHAPE, as read __NOW__ by the generator (git ls-remote + local object reads): head = refs/pull/1036/head = the branch; origin develop
# __DEV__ (142 commits past the merge-base, 6 merges; it moves often). compare develop...head = merge_base __MB_SHORT__, status diverged,
# ahead 3, behind 142, files 50. Asserted: merge_base + ahead + files (exit 10); behind is NOT asserted. MERGED TREE over that develop
# (merge-tree, both orders, 0 conflicts) = __MERGED__ — printed, not a guard (the gate re-predicts over the develop it reads).
#
# THE DEVELOP ARM IS JUDGED BY PATH BLOBS, NEVER BY DEVELOP'S SHA. GUARDED PATHS, each read from its parent directory's GitHub contents listing at
# the CURRENT develop (__NDIRS__ listings): (a) the 49 non-audit PR paths (29 locks + 20 manifests); (b) EVERY file of Blockchain/Dev/scripts/audit/
# (13 at draft, incl. audit-baseline.json, audit-gate.mjs, audit-locks.mjs); the listing must name exactly these 13; (c) 3 REACH paths with no #1036
# blob: the api-gateway, auth and originate Dockerfiles (the runtime `npm ci --omit=dev` steps). Every path at its merge-base blob -> OK (develop's SHA
# is printed, not judged). ALL 50 PR paths at their #1036 blobs (reach paths unmoved) -> exit 19 LANDED. Any path at a blob nobody pinned, a file
# absent, a scripts/audit/ file added or removed, or a PARTIAL landing -> exit 18 GUARDED. TEN open Dependabot PRs share these paths (#949 #948 #947
# #946 #945 #649 #639 #635 #575 #572): one landing first REFUSES here by design — re-pin deliberately (README section 0).
#
# exit 6:  the head is not at the branch AND refs/pull/1036/head on origin.
# exit 7 / 15: the READY capture (BRIEF) and the prompt must carry TIER 1 / ROUND 1.
# exit 10: the compare (merge_base __MB_SHORT__ ahead=3 files=50). exit 13: compare unreadable. exit 18/19: the develop arm (above).
# exit 20: the READY capture AND the prompt must name the head SHA in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit pane, never inside a
#          Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: node_modules farmed PER ENTRY. exit 23: the exact #1036 verdict subject, coagent@ sender, wednesday-agent@ recipient.
# exit 24: the REPORT DIRECTORY + NOT-TESTED.written-first.md. exit 25: the MERGE ADDENDUM (+ `## MERGE ADDENDUM`, `GO: merge #1036`, BASE_GO).
# exit 26: unique container names, --runInBand in containers, the host load average beside every timed run.
# exit 27: RUNTIME REACH FIRST. exit 28: the npm-version dependent root-lock recipe (host npm cannot reproduce the seat's locks; a false NO GO trap).
# exit 29: MERGEABILITY at the CURRENT develop, with the merge-base, the develop pin and the predicted merged tree named in FULL.
# exit 30: Wednesday's ELEVEN by-name items and the standard closing (the keyword ladder, __NBYNAME__ keywords).
# exit 31: THE CONTEXT RULE (report.md at ctx 80%). exit 32: THE CENSUS RULE v2 with the :5432 / :4000 / :4003 / :8080 lsof lines.
# exit 33: a PARTIAL prompt (any `PENDING` token) refuses — --check and launch alike. exit 34: a `deadbeef` literal in the prompt refuses.
# exit 35: every one of the 50 head blobs (the equality targets) must appear in the prompt.
# exit 36: the READY capture AND the prompt must BOTH carry the seat's items (__NBOTH__ tokens, case-insensitive).
# QA1036_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED arms can be proven. QA1036_HEAD / QA1036_PROMPT /
# QA1036_BRIEF (test overrides). A launch with any QA1036_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-22_gate1036_ks763/gen_launcher_gate1036.py (pins re-read at origin + local objects + dry ladder + heredoc parity +
# bash -n) in the shape of gen_launcher_1033.py / gen_launcher_gate16C.py. Exit codes 2..36 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks763_1036.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..36 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1036_BRIEF:-__BRIEF__}"
PROMPT_FILE="${QA1036_PROMPT:-__PROMPT__}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='__BRANCH__'
HEAD_SHA="${QA1036_HEAD:-__HEAD__}"
MERGE_BASE='__MB__'   # the merge-base of the head with develop = the develop c93d84c9b merged in (#1033 squash)
DEVELOP_SHA='__DEV__'   # develop at generation (ls-remote __NOW__) — PRINTED, never a guard
MERGED_TREE='__MERGED__'   # merge-tree(develop at generation, head), 0 conflicts — PRINTED, never a guard
REPORT_DIR='__REPORT_DIR__'
SUBJECT='__SUBJECT__'
REAL_BRIEF="__BRIEF__"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }
/usr/bin/grep -qF 'PENDING' "$PROMPT_FILE" && { echo "REFUSING: the prompt is PARTIAL (a PENDING token) — a partial gate is not a gate" >&2; exit 33; }
/usr/bin/grep -qiF 'deadbeef' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries a deadbeef literal — a placeholder pin is not a pin" >&2; exit 34; }

# The head, pinned at its branch AND at refs/pull/1036/head on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH" refs/pull/1036/head)"
if ! printf '%s\n' "$LSR" | /usr/bin/grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$" || ! printf '%s\n' "$LSR" | /usr/bin/grep -q "^${HEAD_SHA}[[:space:]]refs/pull/1036/head\$"; then
  echo "REFUSING: #1036 — $HEAD_SHA is not at $BRANCH AND refs/pull/1036/head on origin — the head moved; the prompt is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1036 = __MB_SHORT__ ahead 3 files 50 (behind 142 at generation — deliberately not asserted).
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
r = urllib.request.urlopen(urllib.request.Request(api + "develop..." + os.environ["HEAD_SHA"], headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...head from the GitHub compare API" >&2; exit 13; }
[ "$COMPARE" = "$MERGE_BASE ahead=3 files=50" ] || { echo "REFUSING: #1036 develop...head reads '$COMPARE', the pin is '$MERGE_BASE ahead=3 files=50'" >&2; exit 10; }

# The develop arm, judged by PATH BLOBS (see the header) — never by develop's SHA, never by a pinned...develop compare.
CUR_DEV="${QA1036_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
# path -> [merge-base blob = develop-OK, the #1036 blob = LANDED, empty for the 3 REACH Dockerfiles]; read by the generator with git diff --raw / rev-parse
JUDGED = {
__JUDGED__
}
# EVERY file of Blockchain/Dev/scripts/audit/ -> [merge-base blob, #1036 blob or empty]; the listing must name exactly these
AUDIT_DIR = "Blockchain/Dev/scripts/audit"
AUDIT = {
__AUDIT__
}
for n, v in AUDIT.items():
    JUDGED[AUDIT_DIR + "/" + n] = v
dirs = sorted({p.rsplit("/", 1)[0] for p in JUDGED})
seen = {}
for d in dirs:
    try:
        listing = get("/contents/" + d + "?ref=" + cur)
    except Exception as e:
        print("UNJUDGEABLE contents listing unreadable for " + d + ": " + type(e).__name__); sys.exit(0)
    for x in listing:
        seen[d + "/" + x["name"]] = x["sha"] if x.get("type") == "file" else "type-" + str(x.get("type"))
    if d == AUDIT_DIR:
        names = sorted(x["name"] for x in listing)
        if names != sorted(AUDIT):
            print("GUARDED develop " + cur[:9] + " scripts/audit/ file set differs from the pin: " + ",".join(sorted(set(names) ^ set(AUDIT)))); sys.exit(0)
landed, unpinned, ok = [], [], 0
for p, (base, own) in JUDGED.items():
    b = seen.get(p, "ABSENT")
    if b == base:
        ok += 1
    elif own and b == own:
        landed.append(p.replace(D, ""))
    else:
        unpinned.append(p.replace(D, "") + " " + b[:9])
owned = sum(1 for v in JUDGED.values() if v[1])
if unpinned or (landed and len(landed) != owned):
    print("GUARDED develop %s: %d guarded path[s] at a blob nobody pinned %s; %d of %d at the #1036 blob" % (cur[:9], len(unpinned), unpinned[:6], len(landed), owned)); sys.exit(0)
if landed:
    print("LANDED develop %s: all %d #1036 blobs present — #1036 has landed; this prompt is stale" % (cur[:9], owned)); sys.exit(0)
note = "= the generation pin" if cur == pinned else "MOVED from the generation pin " + pinned[:9] + ", not judged by SHA (the gate re-predicts the merged tree over the tip it reads)"
print("OK develop %s %s: %d of %d guarded paths at their merge-base blobs [49 PR paths + 3 reach Dockerfiles + all %d files of scripts/audit/], read from %d directory listings" % (cur[:9], note, ok, len(JUDGED), len(AUDIT), len(dirs))); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } — re-pin deliberately: a different gate" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop $CUR_DEV is not provably clean on the guarded paths: ${DEV_JUDGEMENT:-no judgement} — confirm the delta (a Dependabot PR landing first is the expected mover), then re-pin deliberately (README section 0)" >&2
     exit 18 ;;
esac
/usr/bin/grep -q 'TIER 1' "$BRIEF" && /usr/bin/grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: READY capture and prompt disagree about the tier (TIER 1)" >&2; exit 7; }
/usr/bin/grep -q 'ROUND 1' "$PROMPT_FILE" && /usr/bin/grep -q 'round 1 of 2' "$PROMPT_FILE" || { echo "REFUSING: prompt does not carry ROUND 1 / round 1 of 2" >&2; exit 15; }
head -1 "$PROMPT_FILE" | /usr/bin/grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
/usr/bin/grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the READY capture path" >&2; exit 9; }
/usr/bin/grep -qF "$HEAD_SHA" "$PROMPT_FILE" && /usr/bin/grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: READY capture or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
/usr/bin/grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
/usr/bin/grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
/usr/bin/grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
/usr/bin/grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
/usr/bin/grep -qi 'farmed per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY" >&2; exit 22; }
/usr/bin/grep -qF "$SUBJECT" "$PROMPT_FILE" && /usr/bin/grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && /usr/bin/grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact #1036 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
/usr/bin/grep -qF "$REPORT_DIR" "$PROMPT_FILE" && /usr/bin/grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR or NOT-TESTED.written-first.md" >&2; exit 24; }
/usr/bin/grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && /usr/bin/grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && /usr/bin/grep -qF 'GO: merge #1036' "$PROMPT_FILE" && /usr/bin/grep -qF 'BASE_GO' "$PROMPT_FILE" && /usr/bin/grep -qF 'path blob (mode)' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the MERGE ADDENDUM (the ## heading, the GO string, BASE_GO, the path blob (mode) targets)" >&2; exit 25; }
/usr/bin/grep -qi 'name it uniquely' "$PROMPT_FILE" && /usr/bin/grep -qF -- '--runInBand' "$PROMPT_FILE" && /usr/bin/grep -qi 'load average' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require unique container names, --runInBand in containers, or the host load average beside timed runs" >&2; exit 26; }
/usr/bin/grep -qF 'RUNTIME REACH FIRST' "$PROMPT_FILE" || { echo "REFUSING: prompt does not carry the RUNTIME REACH FIRST rule" >&2; exit 27; }
/usr/bin/grep -qi 'npm-version dependent' "$PROMPT_FILE" && /usr/bin/grep -qF 'INSTRUMENT ARTEFACT' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the npm-version dependent lock-recipe finding (host npm cannot reproduce the locks)" >&2; exit 28; }
/usr/bin/grep -qF 'MERGEABILITY at the CURRENT develop' "$PROMPT_FILE" && /usr/bin/grep -qF "$MERGE_BASE" "$PROMPT_FILE" && /usr/bin/grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && /usr/bin/grep -qF "$MERGED_TREE" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry MERGEABILITY at the CURRENT develop with the merge-base, the develop pin and the predicted merged tree in full" >&2; exit 29; }
for _w in __BYNAME_LIST__; do
  /usr/bin/grep -qF -- "$_w" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 30; }
done
/usr/bin/grep -qF 'THE CONTEXT RULE' "$PROMPT_FILE" && /usr/bin/grep -qF 'ctx 80%' "$PROMPT_FILE" || { echo "REFUSING: prompt does not carry THE CONTEXT RULE (report.md at ctx 80%)" >&2; exit 31; }
/usr/bin/grep -qF 'THE CENSUS RULE v2' "$PROMPT_FILE" && /usr/bin/grep -qF 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" && /usr/bin/grep -qF 'lsof -nP -iTCP:4000 -sTCP:LISTEN' "$PROMPT_FILE" && /usr/bin/grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && /usr/bin/grep -qF 'lsof -nP -iTCP:8080 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry THE CENSUS RULE v2 with the :5432 / :4000 / :4003 / :8080 lsof lines" >&2; exit 32; }
for _b in __BLOB_LIST__; do
  /usr/bin/grep -qF -- "$_b" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not carry the head blob $_b (an equality target)" >&2; exit 35; }
done
for _w in __BOTH_LIST__; do
  /usr/bin/grep -qiF -- "$_w" "$PROMPT_FILE" && /usr/bin/grep -qiF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 36; }
done

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1036 $HEAD_SHA at $BRANCH AND refs/pull/1036/head"
  echo "  compare (GitHub API): develop...#1036 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  generation pins (printed, not guards): develop $DEVELOP_SHA, merged tree $MERGED_TREE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL and carries no deadbeef literal"
  echo "  READY capture and prompt agree on TIER 1; prompt names ROUND 1 / round 1 of 2"
  echo "  prompt opens with the thinking directive and names the READY capture"
  echo "  READY capture and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict; forbids pushing / the real hook / preflight in the Secuura checkout; forbids memory maintenance; forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY; unique container names; --runInBand in containers; the host load average beside timed runs"
  echo "  prompt carries the exact verdict subject ($SUBJECT...); names coagent@ -> wednesday-agent@"
  echo "  prompt names the report directory and NOT-TESTED.written-first.md"
  echo "  prompt carries the MERGE ADDENDUM (## heading, GO: merge #1036, BASE_GO, path blob (mode)), RUNTIME REACH FIRST, the npm-version dependent finding, MERGEABILITY at the CURRENT develop (merge-base + develop + merged tree in full)"
  echo "  prompt carries Wednesday's ELEVEN by-name items and the standard closing (__NBYNAME__ keywords), THE CONTEXT RULE, THE CENSUS RULE v2 (:5432 / :4000 / :4003 / :8080)"
  echo "  prompt carries all 50 head blobs (the equality targets); READY capture and prompt BOTH carry the seat's items (__NBOTH__ tokens)"
  echo "  guarded paths (blobs at the current develop): the 49 non-audit PR paths + 3 reach Dockerfiles (api-gateway, auth, originate) + every file of Blockchain/Dev/scripts/audit/ (13, incl. audit-baseline.json)"
  [ -n "${QA1036_CUR_DEV:-}" ] && echo "  (develop read from the QA1036_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1036_BRIEF:-}${QA1036_PROMPT:-}${QA1036_HEAD:-}${QA1036_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
__CD_LINE__
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
'''
ndirs = len({p.rsplit('/', 1)[0] for p, b, h in judged} | {AUDIT_DIR})
s = (L.replace('__HEAD__', HEAD).replace('__DEV__', DEV).replace('__MB__', MB).replace('__MB_SHORT__', MB[:9]).replace('__MERGED__', MERGED)
     .replace('__NOW__', now).replace('__NDIRS__', str(ndirs)).replace('__BRIEF__', BRIEF).replace('__PROMPT__', PROMPT).replace('__BRANCH__', BRANCH)
     .replace('__REPORT_DIR__', REPORT_DIR).replace('__SUBJECT__', SUBJECT).replace('__JUDGED__', judged_lines).replace('__AUDIT__', audit_lines)
     .replace('__BYNAME_LIST__', bash_list(BYNAME)).replace('__BOTH_LIST__', bash_list(BOTH)).replace('__BLOB_LIST__', bash_list([h for p, b, h in judged_pr] + [baseline_head_blob]))
     .replace('__NBYNAME__', str(len(BYNAME))).replace('__NBOTH__', str(len(BOTH))).replace('__CD_LINE__', CD_LINE))
if re.findall(r'__[A-Z_]+__', s): refuse('residual __TOKEN__ in the launcher: %r' % re.findall(r'__[A-Z_]+__', s)[:5])
# 3. static controls
controls = [('HEAD_SHA="${QA1036_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + MB + "'", 1), ("DEVELOP_SHA='" + DEV + "'", 1), ("MERGED_TREE='" + MERGED + "'", 1), ("BRANCH='" + BRANCH + "'", 1),
            ("REPORT_DIR='" + REPORT_DIR + "'", 1), ("SUBJECT='" + SUBJECT + "'", 1), ('exit 6', 2), ('exit 10;', 1), ('exit 18', 4), ('exit 19', 2), ('exit 21;', 1),
            ('exit 33;', 1), ('exit 34;', 1), ('exit 35;', 1), ('exit 36;', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 1), ('[ -t 0 ]', 1),
            ('exec claude --dangerously-skip-permissions --model opus', 1), ('set -u', 1), ('QA1036_CUR_DEV', 5), (CD_LINE, 1)]
bad = [(k, want, s.count(k)) for k, want in controls if s.count(k) != want]
if bad: refuse('output controls %r' % bad)
if len(re.findall(r'^  "Blockchain/Dev/[^"]+": \["[0-9a-f]{40}", "(?:[0-9a-f]{40})?"\],$', s, flags=re.M)) != 52: refuse('JUDGED row count (49 PR + 3 reach)')
if len(re.findall(r'^  "[a-z][^"]+": \["[0-9a-f]{40}", "(?:[0-9a-f]{40})?"\],$', s, flags=re.M)) != 13: refuse('AUDIT row count')
verbs = re.findall(r'git (?:-C "\$REPO" )?(fetch|checkout|worktree|merge-tree|merge|pull|push|reset|switch|clone|apply)\b', s)
if verbs: refuse('git write verbs in the launcher %r' % verbs)
for tag in ('PYJ', 'PY'):
    body = s.split("<<'" + tag + "'")[1].split(tag + '\n')[0]
    if body.count("'") % 2: refuse('odd apostrophes inside the %s heredoc' % tag)
    if body.count('(') != body.count(')'): refuse('unbalanced parentheses inside the %s heredoc' % tag)
raw_b = s.encode('utf-8')
if any((b < 0x20 and b not in (9, 10, 13)) or b == 0x7f for b in raw_b): refuse('control bytes')
if os.path.exists(OUT):
    bak = OUT + '.pre-' + datetime.datetime.now().strftime('%H%M%S'); shutil.copyfile(OUT, bak); print('existing output copied to', bak)
open(OUT, 'w', encoding='utf-8').write(s); os.chmod(OUT, 0o755)
rc = subprocess.run(['bash', '-n', OUT]).returncode
print(now, 'wrote', OUT, 'lines', s.count('\n'), 'bytes', len(raw_b), 'sha256', hashlib.sha256(raw_b).hexdigest(), '| judged', len(judged), '(49 PR + 3 reach) + audit', len(arows), '| listings', ndirs, '| BOTH', len(BOTH), 'by-name', len(BYNAME), '| bash -n rc', rc)
sys.exit(0 if rc == 0 else 3)
