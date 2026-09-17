#!/usr/bin/env python3
"""gen_launcher_1018_r2.py — re-pin launchers/launch_qa_secuura_ks1050_1018.sh (the ROUND 1 launcher, pinned head 267bd8624 / develop ee40d3099) to the
ROUND 2 delta gate IN PLACE (same name; the round-1 file is copied to a .pre-* backup before anything is written) by ASSERTED substitutions: head
efd677e98, compare develop...head = merge_base 19f1e5475 ahead 4 files 2 (develop is now an ANCESTOR of the head: the seat merged it in), develop pinned
19f1e5475 (#1025), LANDED blobs = the round-2 users.ts c723a68af / ks1050 test ffb3e801a (round-1 blobs kept as LANDED too), the round-2 brief/prompt,
report dir -r2, ROUND 1 -> ROUND 2 in the round guard, the round-2 verdict subject. The users.ts REGION judgement is unchanged (develop users.ts is still
8ef9065e2, re-asserted here). Then a RESIDUAL GUARD, output controls, heredoc parity, no git write verb, bash -n.
Usage: gen_launcher_1018_r2.py <round-1 launcher> <output launcher (the same path)>"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1018_r2', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H1 = '267bd8624ce276ca62160216d042b8477bac52f1'; H2 = 'efd677e98c917a52f8af442c9fcfde756166070e'
D1 = 'ee40d3099599fa2db23a37049da8e00ac953eacd'; D2 = '19f1e54750ce2b65312a687add2db4f5628edb7d'
B1 = '7e89318bcedbc9a35757d4298ace54a6a23020bd'
U = 'Blockchain/Dev/services/auth/src/routes/users.ts'; TF = 'Blockchain/Dev/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', x], capture_output=True, text=True).stdout.strip()
assert rp(D2 + ':' + U) == '8ef9065e2fb24308daeb41820a227a4ee1d6ecc9', 'develop users.ts moved: the region WANT must be recomputed'
assert rp(H2 + ':' + U).startswith('c723a68af') and rp(H2 + ':' + TF).startswith('ffb3e801a')
U2, T2 = rp(H2 + ':' + U), rp(H2 + ':' + TF)
REPORT1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1050-1018-267bd8624-tier2-r1/'
REPORT2 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1050-1018-efd677e98-tier2-r2/'
T1 = '[QA -> Wednesday] TIER 2 GATE #1018 (KS-1050) 267bd8624'
TS2 = '[QA -> Wednesday] TIER 2 GATE #1018 ROUND 2 (KS-1050) efd677e98'
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
HEADER_OLD = cut('#!/bin/bash\n', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """#!/bin/bash
# launch_qa_secuura_ks1050_1018.sh — cross-project QA agent, ONE TIER 2 ROUND 2 DELTA gate over Secuura/Blockchain PR #1018 (KS-1050, Seat A)
# @ efd677e98c917a52f8af442c9fcfde756166070e — auth PATCH /api/users/me now calls userRepo.updateUserOrThrow(user.id, updates, 'Profile update'), the house
# helper (KS-1052): a 0-row UPDATE answers 503 SERVICE_UNAVAILABLE "Profile update could not be confirmed. Please retry ..." instead of success: true.
# Round 2 replaced round 1's 500 PROFILE_UPDATE_NOT_PERSISTED shape per Wednesday's contract-fix ruling (gatesets/2026-09-17_gate1018/answer_1018_contract_fix.md).
# Four commits: 267bd8624 (round 1) -> 9c66589bb (merge of develop efaaa6034) -> c08cec102 (the round-2 change: users.ts +4 -6, the ks1050 test rebuilt on the
# REAL userRepo over a stateful db stub, 3 red cells + 1 control) -> efd677e98 (merge of develop 19f1e5475 = #1025). Net over develop: TWO files,
# users.ts 8ef9065e2 -> c723a68af and the ks1050 test ABSENT -> ffb3e801a. TIER 2 (Wednesday's receipt). The ROUND 1 launcher is the .pre-* copy beside this.
#
# THE SHAPE, as read 20:04-20:10 AEST 2026-09-17 (git ls-remote + the PR, compare and contents APIs agree): develop 19f1e5475 is an ANCESTOR of the head;
# compare develop...head = merge_base 19f1e5475, ahead 4, behind 0, files 2 (asserted as merge_base + ahead + files, exit 10; behind NOT asserted). PR API
# mergeable true (state unstable). Drafter re-derived both merge-ins IN ITS CLONE: merge-tree 267bd8624 x efaaa6034 = tree(9c66589bb) = 0d351b735 and
# merge-tree c08cec102 x 19f1e5475 = tree(efd677e98) = ce49c7bfd, each = the seat's prediction; each merge brought exactly develop's own delta.
#
# The develop pin is judged by CONTENT, not bare: (a) THIRTEEN files by blob at the CURRENT develop — the PR two (auth routes/users.ts 8ef9065e2, the
# ks1050 test ABSENT; at a #1018 blob, round 2 or round 1 -> exit 19 LANDED), auth repositories/userRepo.ts (updateUser + updateUserOrThrow, the helper the
# round-2 contract IS) / middleware/errorHandler.ts / middleware/authenticate.ts / routes/wallet.ts / auth.openapi.ts / package.json / vitest.config.ts /
# vitest.setup.ts / tsconfig.json, docs/openapi/secuura-api.yaml, Dev eslint.config.mjs — any blob nobody pinned -> exit 18; users.ts at ANY OTHER
# blob is judged by REGION content (the errorHandler import line and the PATCH /me handler body through the change-password banner): a move into a
# region refuses (exit 18), a move outside clears; (b) if develop moved past 19f1e5475, the compare pinned...develop REFUSES (exit 18) when the delta
# touches a GUARDED path — services/auth/src/ and its package.json / vitest config + setup / tsconfig, packages/shared/src/ and its package.json,
# docs/openapi/, eslint.config.mjs, the Dev lockfile — unless users.ts cleared by its region judgement (DEV_CONTENT_ALLOWED is EMPTY), or the move
# cannot be judged. Open PR #1026 (KS-839) edits services/auth/src/services/oauth.ts: if it lands first this REFUSES by design — re-pin deliberately.
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
# Re-pinned by gatesets/2026-09-17_gate1018/gen_launcher_1018_r2.py from the ROUND 1 launcher (itself gen_launcher_1018.py from launch_qa_secuura_ks1202_1024.sh):
# same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1018 TIER 2 ROUND 2.
#
# Usage: launch_qa_secuura_ks1050_1018.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'briefs/2026-09-17_secuura-1018-ks1050-tier2.md}"', 'briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.md}"', 1),
 ('prompt var', 'briefs/2026-09-17_secuura-1018-ks1050-tier2.prompt.txt}"', 'briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.prompt.txt}"', 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.md"', 1),
 ('head var', 'HEAD_SHA="${QA1018_HEAD:-' + H1 + '}"', 'HEAD_SHA="${QA1018_HEAD:-' + H2 + '}"', 1),
 ('merge-base', "MERGE_BASE='" + B1 + "'   # the merge-base of the head with develop = the PR parent (#1016s squash; #1015 KS-1018 already under it)",
  "MERGE_BASE='" + D2 + "'   # the merge-base of the head with develop = develop itself (#1025s squash), merged in by efd677e98", 1),
 ('develop', "DEVELOP_SHA='" + D1 + "'   # develop at draft close = #1022s squash, 7 commits past the PR parent, 0 auth files (moved from 81ee4b729 mid-draft; branches API 19:11:02 AEST)",
  "DEVELOP_SHA='" + D2 + "'   # develop at round-2 draft = #1025s squash, an ancestor of the head (git ls-remote 20:04:35, branches API 20:04:45 AEST)", 1),
 ('report dir', "REPORT_DIR='" + REPORT1 + "'", "REPORT_DIR='" + REPORT2 + "'", 1),
 ('compare comment', '# develop...#1018 = 7e89318bc ahead 1 files 2 (behind 7 at draft close; behind deliberately not asserted).', '# develop...#1018 = 19f1e5475 ahead 4 files 2 (behind 0 at round-2 draft; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1018 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=4 files=2" ] || { echo "REFUSING: #1018 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=4 files=2'" >&2; exit 10; }''', 1),
 ('landed users', '{"84d4b75e1aca7a5100f51401e394648b26557643": "#1018 own"}', '{"' + U2 + '": "#1018 round-2 own", "84d4b75e1aca7a5100f51401e394648b26557643": "#1018 round-1 blob"}', 1),
 ('landed test', '{"7beff88572395d7a11eb1f1086ddae2b986a5774": "#1018 own"}', '{"' + T2 + '": "#1018 round-2 own", "7beff88572395d7a11eb1f1086ddae2b986a5774": "#1018 round-1 blob"}', 1),
 ('ok still', '(= #1022s squash, 7 commits past the PR parent 7e89318bc, 0 auth files: the gate merges it; drafter merged tree a133db3e77328dded88a8f982122248c3e8486c4; git ls-remote)',
  '(= #1025s squash, an ANCESTOR of the head: merged tree = head tree ce49c7bfd; the drafter re-derived both merge-ins; git ls-remote)', 1),
 ('tail', 'the gate merges the then-current develop onto 267bd8624 in its own clone,', 'the gate merges the then-current develop onto efd677e98 in its own clone,', 1),
 ('round guard', "grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round (ROUND 1)\" >&2; exit 15; }",
  "grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round (ROUND 2)\" >&2; exit 15; }", 1),
 ('subject', "grep -qF '" + T1 + "' \"$PROMPT_FILE\"", "grep -qF '" + TS2 + "' \"$PROMPT_FILE\"", 1),
 ('check round', 'echo "  brief and prompt agree on TIER 2 and ROUND 1"', 'echo "  brief and prompt agree on TIER 2 and ROUND 2"', 1),
]
for name, old, new, n in REPL:
    c = s.count(old)
    if c != n: print('REFUSE anchor', name, 'count', c, 'want', n); sys.exit(1)
    s = s.replace(old, new); print('  ok', name, c)
# the authored header legitimately names the round-1 commit and the old pins as history; the residual guard judges the BODY
RES = s.replace(HEADER_NEW, '').replace('84d4b75e1aca7a5100f51401e394648b26557643": "#1018 round-1 blob', '').replace('7beff88572395d7a11eb1f1086ddae2b986a5774": "#1018 round-1 blob', '').replace('267bd8624 (round 1)', '').replace('ROUND 1 launcher', '')
for tok in (H1, '267bd8624', 'ee40d3099', 'a133db3e7', '7e89318bc', '#1022s', 'ROUND 1', "'ROUND 1'", 'tier2-r1', 'seven commits', 'PROFILE_UPDATE_NOT_PERSISTED', 'ahead=1'):
    if tok in RES: print('REFUSE residual token', tok, [l[:100] for l in s.splitlines() if tok in l][:4]); sys.exit(2)
# D2 full SHA: MERGE_BASE + DEVELOP_SHA (the header uses the short form); brief path: BRIEF var + REAL_BRIEF
want = {H2: 2, D2: 2, REPORT2: 1, 'ahead=4 files=2': 2, "grep -q 'ROUND 2'": 2, "grep -q 'TIER 2'": 2, TS2: 1, U2: 1, T2: 1, ': DV}': 13, 'DEV_CONTENT_ALLOWED = {}': 1,
        '[ -t 0 ]': 1, 'exec claude --dangerously-skip-permissions --model opus': 1, 'QA1018_USERS_FILE': 5, 'QA1018_CUR_DEV': 5, 'MERGE ADDENDUM': 5, 'NOT-TESTED.written-first.md': 4,
        'briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.md': 2, 'briefs/2026-09-17_secuura-1018-ks1050-tier2-r2.prompt.txt': 1}
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
if os.path.exists(OUT):
    bak = OUT + '.pre-r2-' + now('+%H%M%S'); shutil.copyfile(OUT, bak); print('round-1 launcher copied aside to', bak, 'sha256', hashlib.sha256(open(bak, 'rb').read()).hexdigest()[:16])
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip())
if p.returncode: sys.exit(3)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
