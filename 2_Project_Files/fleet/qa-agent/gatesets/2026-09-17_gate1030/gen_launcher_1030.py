#!/usr/bin/env python3
"""gen_launcher_1030.py — derive launch_qa_secuura_ks1211_1030.sh from the sibling TIER 2 launcher launchers/launch_qa_secuura_ks1211_1027.sh
(same lane, same class, verdicted GO WITH FINDINGS tonight) by ASSERTED substitutions and asserted SEGMENT replacement: every anchor must occur
exactly as often as stated, or the generator refuses and writes nothing.
CHANGED ON PURPOSE vs #1027: the develop arm is judged by PATH BLOBS ONLY, never by develop's SHA and never by a pinned...develop compare:
the 42 non-audit PR paths each read from their parent directory's contents listing at the CURRENT develop, plus EVERY file of
Blockchain/Dev/scripts/audit/ (13 at draft; the listing must name exactly these — an added or removed file is GUARDED). Pins are re-read from
the Secuura checkout with read-only `git rev-parse` at generation time. Added guards 22-27 (prompt/brief content) and a --check-only
QA1030_CUR_DEV test override (so LANDED / GUARDED / an older develop can be proven without a real develop commit).
Then a RESIDUAL GUARD (tokens of the #1027 gate), output controls, PYJ/PY heredoc apostrophe/paren parity, no git write verbs, no control
bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1030.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
HEAD = 'e43af493418a1f13cfb60c994380fb74d79ad07e'
BASE = '20ab16f9a80c5c3c75e613d8c670efefd8f5cafb'      # merge-base of head with develop = the develop 566107f01 merged in (#1027)
DEVELOP = '75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'   # origin develop at draft (#1026, services/auth only) — informational, NOT a guard
OLD_HEAD = 'd7fc6cc5582b918c0773ec6f25f86407de6f86ab'
OLD_BASE = '19f1e54750ce2b65312a687add2db4f5628edb7d'
BRANCH = 'refs/heads/feature/ks-1211-bump-vitest'
STEM = '2026-09-17_secuura-1030-ks1211-vitest-tier2'
OLD_STEM = '2026-09-17_secuura-1027-ks1211-jsyaml-bbm-tier2'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1030-e43af4934-tier2-r1/'
SUBJECT = '[QA -> Wednesday] TIER 2 GATE #1030 (KS-1211) e43af4934 — '
AUDIT_DIR = 'Blockchain/Dev/scripts/audit'

def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
    if p.returncode != 0: refuse('git %r rc %d %s' % (a, p.returncode, p.stderr[-200:]), 1)
    return p.stdout.strip()
pr_paths = git('diff', '--name-only', BASE + '...' + HEAD).splitlines()
if len(pr_paths) != 43: refuse('PR paths %d, want 43' % len(pr_paths), 1)
nonaudit = [p for p in pr_paths if not p.startswith(AUDIT_DIR + '/')]
if len(nonaudit) != 42: refuse('non-audit PR paths %d, want 42' % len(nonaudit), 1)
audit_files = [l.split('\t')[1].rsplit('/', 1)[1] for l in git('ls-tree', BASE, AUDIT_DIR + '/').splitlines() if l.split()[1] == 'blob']
if len(audit_files) != 13 or 'audit-baseline.json' not in audit_files: refuse('scripts/audit files %d' % len(audit_files), 1)
if git('rev-parse', DEVELOP + ':' + AUDIT_DIR) != git('rev-parse', BASE + ':' + AUDIT_DIR): refuse('scripts/audit tree differs base vs draft develop', 1)
rows = []
for p in nonaudit:
    b, h, c = git('rev-parse', BASE + ':' + p), git('rev-parse', HEAD + ':' + p), git('rev-parse', DEVELOP + ':' + p)
    if b == h or b != c: refuse('pin sanity %s base %s head %s develop %s' % (p, b[:9], h[:9], c[:9]), 1)
    rows.append((p, b, h))
arows = []
for n in sorted(audit_files):
    p = AUDIT_DIR + '/' + n
    b, h = git('rev-parse', BASE + ':' + p), git('rev-parse', HEAD + ':' + p)
    if (n == 'audit-baseline.json') != (b != h): refuse('audit pin sanity %s' % n, 1)
    arows.append((n, b, h if b != h else ''))
if sum(1 for r in arows if r[2]) != 1: refuse('audit own blobs', 1)
OWNED = 42 + 1

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks1211_1030.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1030
# (KS-1211, Seat B, PR-3b: GHSA-82fw-gwwq-j7x9, vitest / @vitest/mocker < 4.1.11, moderate) @ e43af493418a1f13cfb60c994380fb74d79ad07e —
# THREE commits: 17cbb1091 (26 standalone locks + 15 manifests, on 19f1e5475), 566107f01 (a merge of develop 20ab16f9a = #1018 + #1027) and
# e43af4934 (the Blockchain/Dev root lock + the audit-baseline row removed, 32 -> 31). 43 files vs develop: 27 package-lock.json (frontend/issuer,
# the Dev root, 23 services/*, systemTest/api-explorer, systemTest/performance), 15 services/*/package.json, scripts/audit/audit-baseline.json.
#
# THE SHAPE, as read 21:06-21:14 AEST 2026-09-17 (git ls-remote + the PR and compare APIs): head parent 566107f01; merge parents 17cbb1091 +
# 20ab16f9a; origin develop 75ad0e55c (#1026, services/auth oauth.ts + one test — 0 of the 43). compare develop...head = merge_base 20ab16f9a,
# status diverged, ahead 3, behind 1, files 43. Asserted: merge_base + ahead + files (exit 10); behind is NOT asserted.
#
# THE DEVELOP ARM IS JUDGED BY PATH BLOBS, NEVER BY DEVELOP'S SHA (develop moves often). GUARDED PATHS, each read from its parent directory's
# GitHub contents listing at the CURRENT develop (28 listings):
#   (a) the 42 non-audit PR paths: frontend/issuer/package-lock.json; Blockchain/Dev/package-lock.json; services/{analytics, anchoring,
#       api-gateway, auth, billing, demo-service, guardian, kyc, m365-integration, mcp-server, nft-certificate, prism, queue, referral, security,
#       shared, staking, tenant-provisioning, timestamping, tokenisation, transfer, vc-issuer, wallet-connector}/package-lock.json;
#       services/{analytics, guardian, kyc, m365-integration, mcp-server, nft-certificate, prism, queue, referral, security, tenant-provisioning,
#       timestamping, tokenisation, vc-issuer, wallet-connector}/package.json; systemTest/{api-explorer, performance}/package-lock.json;
#   (b) EVERY file of Blockchain/Dev/scripts/audit/ (13 at draft, incl. audit-baseline.json, audit-gate.mjs, audit-locks.mjs, lock-discovery.mjs,
#       baseline-contract.mjs, package.json, package-lock.json); the listing must name exactly these 13.
# Every path at its merge-base blob -> OK (develop's SHA is printed, not judged). ALL 43 PR paths at their #1030 blobs -> exit 19 LANDED.
# Any path at a blob nobody pinned, a file absent, a scripts/audit/ file added or removed, or a PARTIAL landing -> exit 18 GUARDED.
# TEN open Dependabot PRs (#949 #948 #947 #946 #945 #649 #639 #635 #575 #572) touch the root lock (#948, #649, #575 also service manifests):
# one of them landing first REFUSES here by design — re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit pane, never inside a
# Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: brief AND prompt must carry the exact #1030 verdict subject; the prompt must name coagent@ as sender and wednesday-agent@ as recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY; the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM.
# exit 26: the prompt must say Docker is NOT available and require the host load average beside every timed run.
# exit 27: brief AND prompt must carry the TIER 1 TRIGGERED rule (a moved runtime byte is stated, the gate does not silently continue as tier 2).
# QA1030_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED arms and an older develop can be proven.
# A launch with any QA1030_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1030/gen_launcher_1030.py from launch_qa_secuura_ks1211_1027.sh (asserted substitutions + segment
# replacement + pins re-read from the repo + residual guard + output controls + bash -n). Exit codes 2..27 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1211_1030.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..27 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

def segment(start, end):
    if s.count(start) != 1: refuse('segment start %r count %d' % (start[:60], s.count(start)), 1)
    i = s.index(start); j = s.find(end, i)
    if j < 0: refuse('segment end %r not found' % end[:40], 1)
    return s[i:j + len(end)]

jl = []
for p, b, h in rows:
    jl.append('  "%s": ["%s", "%s"],' % (p, b, h))
al = []
for n, b, h in arows:
    al.append('  "%s": ["%s", "%s"],' % (n, b, h))
NEW_DEV = '''# The develop arm, judged by PATH BLOBS (see the header) — never by develop's SHA, never by a pinned...develop compare.
CUR_DEV="${QA1030_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
# path -> [merge-base blob = develop-OK, the #1030 blob = LANDED]; read by generator from the Secuura checkout with git rev-parse
JUDGED = {
''' + '\n'.join(jl) + '''
}
# EVERY file of Blockchain/Dev/scripts/audit/ -> [merge-base blob, #1030 blob or empty]; the listing must name exactly these
AUDIT_DIR = "Blockchain/Dev/scripts/audit"
AUDIT = {
''' + '\n'.join(al) + '''
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
    print("GUARDED develop %s: %d guarded path[s] at a blob nobody pinned %s; %d of %d at the #1030 blob" % (cur[:9], len(unpinned), unpinned[:6], len(landed), owned)); sys.exit(0)
if landed:
    print("LANDED develop %s: all %d #1030 blobs present — #1030 has landed; this brief is stale" % (cur[:9], owned)); sys.exit(0)
note = "= the draft pin" if cur == pinned else "MOVED from the draft pin " + pinned[:9] + ", not judged by SHA"
print("OK develop %s %s: %d of %d guarded paths at their merge-base blobs [42 PR paths + all %d files of scripts/audit/], read from %d directory listings" % (cur[:9], note, ok, len(JUDGED), len(AUDIT), len(dirs))); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop $CUR_DEV is not provably clean on the guarded paths: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher JUDGED/AUDIT blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
'''
old_dev = segment('# The develop pin, judged by CONTENT (see the header): twenty-five files', 'exit 18 ;;\nesac\n')
s = s.replace(old_dev, NEW_DEV)

GREPS_ADD = '''grep -qi 'farmed per ENTRY' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY" >&2; exit 22; }
grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: brief or prompt does not carry the exact #1030 verdict subject, or the prompt does not name the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" \\
  || { echo "REFUSING: brief or prompt does not name the report directory $REPORT_DIR, or the prompt does not name NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MERGE ADDENDUM' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM" >&2; exit 25; }
grep -qi 'Docker is NOT available' "$PROMPT_FILE" && grep -qi 'load average' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not say Docker is NOT available or does not require the host load average beside timed runs" >&2; exit 26; }
grep -qF 'TIER 1 TRIGGERED' "$PROMPT_FILE" && grep -qF 'TIER 1 TRIGGERED' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the TIER 1 TRIGGERED rule" >&2; exit 27; }
'''
anchor17 = '''  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }\n'''
if s.count(anchor17) != 1: refuse('exit 17 anchor count %d' % s.count(anchor17), 1)
s = s.replace(anchor17, anchor17 + GREPS_ADD)

subs = [
    ('QA1027_BRIEF', 'QA1030_BRIEF', 2),
    ('QA1027_PROMPT', 'QA1030_PROMPT', 2),
    ('QA1027_HEAD', 'QA1030_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ("BRANCH='refs/heads/feature/ks-1211-bump-jsyaml-bbm'", "BRANCH='" + BRANCH + "'", 1),
    (OLD_HEAD, HEAD, 1),
    ("MERGE_BASE='" + OLD_BASE + "'   # the merge-base of the head with develop = the develop the seat merged in (#1025, KS-528)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the develop 566107f01 merged in (#1027 squash, on #1018)", 1),
    ("DEVELOP_SHA='" + OLD_BASE + "'   # develop at draft time = the merge-base itself, #1025 squash (ls-remote 20:05:22 and 20:07:07 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft = #1026 squash (ls-remote 21:06:26 and 21:08:32 AEST) — PRINTED, never a guard\n"
     "REPORT_DIR='" + REPORT_DIR + "'\nSUBJECT='" + SUBJECT + "'", 1),
    ('echo "REFUSING: #1027 — $HEAD_SHA is not at', 'echo "REFUSING: #1030 — $HEAD_SHA is not at', 1),
    ('# develop...#1027 = 19f1e5475 ahead 2 files 10 (behind 0 at draft time — deliberately not asserted).',
     '# develop...#1030 = 20ab16f9a ahead 3 files 43 (behind 1 at draft time: #1026 — deliberately not asserted).', 1),
    ('ahead=2 files=10', 'ahead=3 files=43', 2),
    ('''{ echo "REFUSING: #1027 develop...head reads''', '''{ echo "REFUSING: #1030 develop...head reads''', 1),
    ('echo "  head on origin: #1027 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1030 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1027 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1030 = $COMPARE"', 1),
    ('echo "  prompt forbids printing a credential value"\n',
     'echo "  prompt forbids printing a credential value"\n'
     '  echo "  prompt requires node_modules farmed per ENTRY; says Docker is NOT available; requires the host load average beside timed runs"\n'
     '  echo "  brief and prompt carry the exact verdict subject ($SUBJECT...); prompt names coagent@ -> wednesday-agent@"\n'
     '  echo "  brief and prompt name the report directory; prompt names NOT-TESTED.written-first.md"\n'
     '  echo "  brief and prompt carry the MERGE ADDENDUM and the TIER 1 TRIGGERED rule"\n'
     '  echo "  guarded paths (blobs at the current develop): the 42 non-audit PR paths + every file of Blockchain/Dev/scripts/audit/ (13, incl. audit-baseline.json)"\n'
     '  [ -n "${QA1030_CUR_DEV:-}" ] && echo "  (develop read from the QA1030_CUR_DEV test override, not ls-remote)"\n', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)
fin = '[ -z "${QA1030_BRIEF:-}${QA1030_PROMPT:-}${QA1030_HEAD:-}" ]'
if s.count(fin) != 1: refuse('final override line count %d' % s.count(fin), 1)
s = s.replace(fin, '[ -z "${QA1030_BRIEF:-}${QA1030_PROMPT:-}${QA1030_HEAD:-}${QA1030_CUR_DEV:-}" ]')

residual = ['1027', 'd7fc6cc5', '19f1e547', 'jsyaml', 'js-yaml', 'bbm', 'baseline-browser', 'governance', 'originate', 'twenty-five', 'TWENTY-FIVE',
            'e6f2184d2', '#1025', 'KS-528', 'DEV_CONTENT_ALLOWED', 'GUARDED = [', '/compare/" + pinned', 'ahead=2', 'files=10', '20:0', '20:1']
# PERMITTED history mentions (exact phrase, exact count), masked before the residual scan
permitted = [('from launch_qa_secuura_ks1211_1027.sh (asserted', 1), ('merge of develop 20ab16f9a = #1018 + #1027)', 1), ('on 19f1e5475)', 1),
             ('(#1027 squash, on #1018)', 1)]
body = s
for ph, n in permitted:
    if body.count(ph) != n: refuse('permitted phrase %r count %d, want %d' % (ph, body.count(ph), n), 1)
    body = body.replace(ph, '<permitted>')
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body): hits.append((tok, body.count('\n', 0, m.start()) + 1))
lines = body.split('\n')
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d: %s' % (tok, line, lines[line - 1][:120]), file=sys.stderr)
    sys.exit(2)

controls = [
    ('HEAD_SHA="${QA1030_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1), ("REPORT_DIR='" + REPORT_DIR + "'", 1), ("SUBJECT='" + SUBJECT + "'", 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('     exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1), ('exit 22;', 1), ('exit 23;', 1), ('exit 24;', 1),
    ('exit 25;', 1), ('exit 26;', 1), ('exit 27;', 1),
    ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 1), ('LANDED*)', 1), ('OK*)', 1),
    ('ahead=3 files=43', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2), ('QA1030_CUR_DEV', 5),   # header 1, the CUR_DEV read 1, the --check note 2 (test + text), the launch refusal 1
] + [('  "%s": ["%s", "%s"],' % r, 1) for r in rows] + [('  "%s": ["%s", "%s"],' % r, 1) for r in arows]
bad = [(k, want, s.count(k)) for k, want in controls if s.count(k) != want]
if bad: refuse('output controls %r' % bad, 1)
if 'git -C $' in s: refuse('git -C $VAR form', 1)
verbs = re.findall(r'git (?:-C "\$REPO" )?(fetch|checkout|worktree|merge-tree|merge|pull|push|reset|switch|clone)\b', s)
if verbs: refuse('git write verbs in the launcher %r' % verbs, 1)
pyj = s.split("<<'PYJ'")[1].split('PYJ\n')[0]
if pyj.count("'") % 2: refuse('odd apostrophes inside the PYJ heredoc (%d)' % pyj.count("'"), 1)
if pyj.count('(') != pyj.count(')'): refuse('unbalanced parentheses inside the PYJ heredoc (%d/%d)' % (pyj.count('('), pyj.count(')')), 1)
py = s.split("<<'PY'")[1].split('PY\n')[0]
if py.count("'") % 2: refuse('odd apostrophes inside the PY heredoc (%d)' % py.count("'"), 1)
raw = s.encode('utf-8')
if sum(1 for b in raw if (b < 0x20 and b not in (9, 10, 13)) or b == 0x7f): refuse('control bytes', 1)
if os.path.exists(out_path):
    bak = out_path + '.pre-' + datetime.datetime.now().strftime('%m%d%H%M%S')
    shutil.copyfile(out_path, bak); print('existing output copied to', bak)
open(out_path, 'w', encoding='utf-8').write(s)
os.chmod(out_path, 0o755)
rc = subprocess.run(['bash', '-n', out_path]).returncode
print(datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'), 'wrote', out_path, 'lines', s.count('\n'), 'sha256', hashlib.sha256(raw).hexdigest()[:16],
      'subs', len(subs), 'controls', len(controls), 'judged', len(rows), '+ audit', len(arows), 'residual guard clean', 'bash -n rc', rc, 'pyj apostrophes', pyj.count("'"), 'pyj parens', pyj.count('('))
sys.exit(0 if rc == 0 else 3)
