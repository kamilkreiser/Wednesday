#!/usr/bin/env python3
"""gen_launcher_1017r2.py — derive launch_qa_secuura_ks1195_1017r2.sh from launchers/launch_qa_secuura_ks1195_1017.sh (the #1017 ROUND 1 launcher, itself generated
by gen_launcher_1017.py) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.
Re-points at #1017 (KS-1195) ROUND 2 (a delta): head a067d4e3e (parent cbe29597d) / merge-base 7e89318bc / develop fa887f382 (#1014's squash; unmoved since round 1):
compare develop...head = merge_base 7e89318bc ahead 3 files 5 (behind NOT asserted). The develop arm keeps round 1's CONTENT judgement (21 files by blob, three
product files by REGION + the ks781 pins) with the LANDED arm extended to the ROUND-2 blobs (auth.ts 7c985bdce, rateLimitEnforce.ts 90bd29378, ks1195 test
4b1fc017d) beside the round-1 blobs. Round-2 rules replace the round-1 exits: exit 15 ROUND 2; exit 24 brief AND prompt name the round-2 REPORT DIRECTORY and the
ROUND-1 REPORT path, and the prompt names NOT-TESTED.written-first.md; exit 25 brief AND prompt carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN /
NEW disposition. Test hooks renamed QA1017R2_*. Then a RESIDUAL GUARD, output controls, heredoc parity, no git write verb, no control bytes, bash -n.
Never overwrites an existing output (writes a .pre-* copy first if one exists).
Usage: gen_launcher_1017r2.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1017r2', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:50], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017r2-a067d4e3e-tier1-r2/'
R1_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'
HEADER_OLD = cut('# launch_qa_secuura_ks1195_1017.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1195_1017r2.sh — cross-project QA agent, ONE TIER 1 ROUND 2 DELTA gate (round 2 of 2 under the cap) over Secuura/Blockchain
# PR #1017 (KS-1195, Seat A) @ a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66 — round 1 (head cbe29597d) was NO GO on F-1: the per-key limiter bucketed by
# connectorId || userId, so every key with no connectorId shared ONE bucket (connector:api-key) across all tenants. The ONE new commit (parent cbe29597d):
# middleware/auth.ts +9 (API-key branch sets req.user.rateLimitBucket = api_key: + a domain-separated SHA-256 of the key), middleware/rateLimitEnforce.ts +5 -1
# (clientId = rateLimitBucket || connectorId || userId), the ks1195 test +48 (cells a/b/c + F-2's real double-auth erasure cell). TIER 1: auth middleware on
# every authenticated route. ROUND 2 of 2 is the CAP: a NO GO ships the closed instances and tickets the residue.
#
# THE SHAPE, as read 09:49-10:05 AEST 2026-09-17 (git ls-remote x2 + the PR, compare and commits APIs agree): merge-base = 7e89318bc (#1016s squash); develop =
# fa887f382 = #1014s squash (unmoved since round 1), NOT an ancestor of the head: compare develop...head = merge_base 7e89318bc, diverged, ahead 3, behind 1,
# files 5. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted. Drafter merged tree (head x fa887f382): 35974a2ff.
#
# The develop pin is judged by CONTENT exactly as in round 1: (a) TWENTY-ONE files by blob at the CURRENT develop — the PR's five at their round-1 OR round-2
# head blobs -> exit 19 LANDED; auth.ts, rateLimitEnforce.ts and index.ts at ANY OTHER unpinned blob judged by REGION content (auth.ts and rateLimitEnforce.ts
# from their base first import to EOF; index.ts from the global limiter to the platform mount, PLUS its ks781 pin lines 846/859/892): a move into a region or a
# pin shift refuses (exit 18), a move outside clears; (b) past fa887f382 the compare pinned...develop REFUSES (exit 18) on a GUARDED path unless cleared by the
# region judgement (DEV_CONTENT_ALLOWED is EMPTY), or the move cannot be judged.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact ROUND 2 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the round-2 REPORT DIRECTORY and the ROUND-1 REPORT path (the QA agent has no inbox), and the prompt must name
#          NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition (round 2 of 2: closed instances ship,
#          residue is ticketed).
# QA1017R2_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1017R2_AUTH_FILE / QA1017R2_RLE_FILE / QA1017R2_INDEX_FILE (test fixtures, --check only): a local file stands in for develop's copy of that file (content
# AND git blob) so each region judgement's clear and refuse arms, and the LANDED arm, can be proven without a real develop commit.
# A launch with any QA1017R2_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1017r2/gen_launcher_1017r2.py from launch_qa_secuura_ks1195_1017.sh (asserted substitutions + residual
# guard + output controls + bash -n): same guard set and exit codes 2..23, re-pointed at #1017 ROUND 2, with round-2 exits 24/25. Exit codes 2..25 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks1195_1017r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1017_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017-ks1195-tier1.md}"', 'BRIEF="${QA1017R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017r2-ks1195-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1017_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017-ks1195-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1017R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017r2-ks1195-tier1.prompt.txt}"', 1),
 ('head var', 'HEAD_SHA="${QA1017_HEAD:-cbe29597d11e59f2e1a14519e9ba3dbf6de9a756}"', 'HEAD_SHA="${QA1017R2_HEAD:-a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66}"', 1),
 ('merge-base comment', "MERGE_BASE='7e89318bcedbc9a35757d4298ace54a6a23020bd'   # the merge-base of the head with develop = the PR parent of 973eb49ef (#1016s squash)", "MERGE_BASE='7e89318bcedbc9a35757d4298ace54a6a23020bd'   # the merge-base of the head with develop = the parent of 973eb49ef, the PR's first commit (#1016s squash)", 1),
 ('develop comment', "DEVELOP_SHA='fa887f382b212b8da4a0a4a556bacb05ea34daaa'   # develop at draft close = #1014s squash on 7e89318bc, NOT an ancestor of the head (branches API 08:49:54 + 08:51:46, git ls-remote 08:52:38 AEST; #1014 merged 08:44:35)",
  "DEVELOP_SHA='fa887f382b212b8da4a0a4a556bacb05ea34daaa'   # develop at round-2 drafting = #1014s squash on 7e89318bc, unmoved since round 1, NOT an ancestor of the head (git ls-remote 09:49:57 + 10:01:16, branches API 10:05 AEST)", 1),
 ('report dir', "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'\n", "REPORT_DIR='" + REPORT_DIR + "'\nR1_REPORT='" + R1_REPORT + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017-ks1195-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1017r2-ks1195-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1017 — $HEAD_SHA', 'REFUSING: #1017 ROUND 2 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1017 = 7e89318bc ahead 2 files 5 (behind 1 at draft close; behind deliberately not asserted).', '# develop...#1017 ROUND 2 = 7e89318bc ahead 3 files 5 (behind 1 at draft close; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=5" ] || { echo "REFUSING: #1017 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=5'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=5" ] || { echo "REFUSING: #1017 ROUND 2 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=5'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1017_CUR_DEV:-', 'CUR_DEV="${QA1017R2_CUR_DEV:-', 1),
 ('landed auth', '({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {"8fbe102eb58cc1cb7c39c242c88fad1f2d489841": "#1017 own"}),',
                 '({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {"8fbe102eb58cc1cb7c39c242c88fad1f2d489841": "#1017 round-1 own", "7c985bdcefc26293815bfbe0cbf315f929b48835": "#1017 round-2 own"}),', 1),
 ('landed rle', '({"fc5c5a4d934384745565e730cd12c0a0fcfcaa70": "base"}, {"f4b66aa1abb8b337e3fa00aaf6ebba97ffb5745d": "#1017 own"}),',
                '({"fc5c5a4d934384745565e730cd12c0a0fcfcaa70": "base"}, {"f4b66aa1abb8b337e3fa00aaf6ebba97ffb5745d": "#1017 round-1 own", "90bd29378508c8fee54e010b54cdc72ff992aafa": "#1017 round-2 own"}),', 1),
 ('landed idx', '{"db127dbfa5dd899b0a8e0d844690890d91e27f10": "#1017 own"}', '{"db127dbfa5dd899b0a8e0d844690890d91e27f10": "#1017 own, rounds 1 and 2"}', 1),
 ('landed test', '({"ABSENT": "base"}, {"ade08ac1ebd2a7305a7e253a79a78c63099bf5c0": "#1017 own"}),', '({"ABSENT": "base"}, {"ade08ac1ebd2a7305a7e253a79a78c63099bf5c0": "#1017 round-1 own", "4b1fc017da158de4e7a3a47565b7dbccc1ea3872": "#1017 round-2 own"}),', 1),
 ('landed ks781', '{"bc4815c4ec9cae2f065e29dec6b938cdf49f2d23": "#1017 own"}', '{"bc4815c4ec9cae2f065e29dec6b938cdf49f2d23": "#1017 own, rounds 1 and 2"}', 1),
 ('region comment', '# REGION judgement for the three product files (brief items 1-9 stand on them); the SHAs were computed by the generator from the base blobs.',
                    '# REGION judgement for the three product files (brief items 1-5 stand on them); the SHAs were computed by gen_launcher_1017.py from the base blobs and carried verbatim.', 1),
 ('region env auth', '"QA1017_AUTH_FILE"]', '"QA1017R2_AUTH_FILE"]', 1),
 ('region env rle', '"QA1017_RLE_FILE"]', '"QA1017R2_RLE_FILE"]', 1),
 ('region env idx', '"QA1017_INDEX_FILE"]', '"QA1017R2_INDEX_FILE"]', 1),
 ('ok merged tree', 'drafter merged tree 135b07468c0f12279836c43051e16d5ff1053398', 'drafter merged tree 35974a2ffce620fe37c956daf5fde1a2e4e7a738', 1),
 ('tail', 'tail = "the gate merges the then-current develop onto cbe29597d in its own clone, rebuilds the shared dist there, runs the api-gateway suite, packages/shared and the route-family, double-count and principal censuses on the MERGED tree beside the base and head trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 2, 3, 11)"',
          'tail = "the gate merges the then-current develop onto a067d4e3e in its own clone, rebuilds the shared dist there, re-runs the round-1 census and the A5 bucket probe on the MERGED tree beside the base, round-1 and head trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 2, 4, 6)"', 1),
 ('round grep', '''grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }''',
                '''grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 2)" >&2; exit 15; }''', 1),
 ('subject + round-2 rules',
  '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1017 (KS-1195) cbe29597d' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" \\
  || { echo "REFUSING: brief or prompt does not name the report directory $REPORT_DIR, or the prompt does not name NOT-TESTED.written-first.md — the report must land where Wednesday reads it, NOT-TESTED first" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MERGE ADDENDUM' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM — the merge seat's equality targets and the deploy precondition ride on it" >&2; exit 25; }
''',
  '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1017 ROUND 2 (KS-1195) a067d4e3e' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not carry the exact ROUND 2 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$R1_REPORT" "$PROMPT_FILE" && grep -qF "$R1_REPORT" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the report directory $REPORT_DIR and the ROUND-1 REPORT $R1_REPORT, or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox; a carry-forward with no pointer can only be answered with I could not" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MERGE ADDENDUM' "$BRIEF" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition — round 2 of 2: closed instances ship and residue is ticketed" >&2; exit 25; }
''', 1),
 ('check head', 'echo "  head on origin: #1017 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1017 ROUND 2 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1017 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1017 ROUND 2 = $COMPARE"', 1),
 ('check round', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 'echo "  brief and prompt agree on TIER 1 and ROUND 2"', 1),
 ('check subject', 'echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory; prompt names NOT-TESTED.written-first.md"\n  echo "  brief and prompt carry the MERGE ADDENDUM"\n',
                   'echo "  prompt carries the exact ROUND 2 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the round-2 report directory and the ROUND-1 REPORT; prompt names NOT-TESTED.written-first.md"\n  echo "  brief and prompt carry the MERGE ADDENDUM and require CLOSED / STILL OPEN / NEW per finding"\n', 1),
 ('check fixture echo', '  [ -n "${QA1017_CUR_DEV:-}" ] && echo "  (develop read from the QA1017_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1017_AUTH_FILE:-}${QA1017_RLE_FILE:-}${QA1017_INDEX_FILE:-}" ] && echo "  (a develop product file read from a QA1017_*_FILE fixture, not the contents API)"\n',
  '  [ -n "${QA1017R2_CUR_DEV:-}" ] && echo "  (develop read from the QA1017R2_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1017R2_AUTH_FILE:-}${QA1017R2_RLE_FILE:-}${QA1017R2_INDEX_FILE:-}" ] && echo "  (a develop product file read from a QA1017R2_*_FILE fixture, not the contents API)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1017_BRIEF:-}${QA1017_PROMPT:-}${QA1017_HEAD:-}${QA1017_CUR_DEV:-}${QA1017_AUTH_FILE:-}${QA1017_RLE_FILE:-}${QA1017_INDEX_FILE:-}" ]',
                    '[ -z "${QA1017R2_BRIEF:-}${QA1017R2_PROMPT:-}${QA1017R2_HEAD:-}${QA1017R2_CUR_DEV:-}${QA1017R2_AUTH_FILE:-}${QA1017R2_RLE_FILE:-}${QA1017R2_INDEX_FILE:-}" ]', 1),
]
bad = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); bad += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if bad: print('REFUSING: %d anchors disagreed; nothing written' % bad); sys.exit(1)
RESID = ['QA1017_', 'ROUND 1', 'ahead=2', 'cbe29597d11e59f2e1a14519e9ba3dbf6de9a756', '135b07468', "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'", '"#1017 own"', 'launch_qa_secuura_ks1195_1017.sh —', 'brief items 1, 2, 3, 11', 'onto cbe29597d']
PERMITTED = {'from launch_qa_secuura_ks1195_1017.sh': 1}
stripped = s
for k, v in PERMITTED.items():
    if stripped.count(k) != v: print('PERMITTED count', repr(k), stripped.count(k), '!=', v); sys.exit(1)
    stripped = stripped.replace(k, '')
res = {t: stripped.count(t) for t in RESID if t in stripped}
if res: print('REFUSING: residual tokens', res); sys.exit(2)
CTL = {'a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66': 2, '7e89318bcedbc9a35757d4298ace54a6a23020bd': 1, 'fa887f382b212b8da4a0a4a556bacb05ea34daaa': 1, '35974a2ffce620fe37c956daf5fde1a2e4e7a738': 1,
       REPORT_DIR: 1, R1_REPORT: 1, '"$R1_REPORT"': 2, 'ahead=3 files=5': 2, 'QA1017R2_AUTH_FILE': 4, 'QA1017R2_RLE_FILE': 4, 'QA1017R2_INDEX_FILE': 4, 'QA1017R2_CUR_DEV': 5,
       '2f397badf55601f74137365eae1a50999fe97af2ba7aeb38292440d62fdcbac7': 1, 'a8b72dd55b760aee0435e4632adc358bc2966da7f5219cb2397b0fa28c947d4c': 1, '451630676f0ea13518f6723ee4e395a2472f3ff00aadd0d665b78b85e7bf5bdf': 1,
       '7c985bdcefc26293815bfbe0cbf315f929b48835': 1, '90bd29378508c8fee54e010b54cdc72ff992aafa': 1, '4b1fc017da158de4e7a3a47565b7dbccc1ea3872': 1, '8fbe102eb58cc1cb7c39c242c88fad1f2d489841': 1,
       "grep -q 'ROUND 2'": 2, 'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None, 'NOT-TESTED.written-first.md': None, 'content_cleared': 3, 'PINS': 2,
       'exit 19': None, 'exit 21': None, 'exit 22': None, 'exit 23': None, 'exit 24': None, 'exit 25': None, 'exit 16': None, '[QA -> Wednesday] TIER 1 GATE #1017 ROUND 2 (KS-1195) a067d4e3e': 1}
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
    pre = OUT + '.pre-' + now('+%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
open(OUT, 'w').write(s); os.chmod(OUT, 0o755)
p = subprocess.run(['bash', '-n', OUT], capture_output=True, text=True)
print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: sys.exit(3)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
