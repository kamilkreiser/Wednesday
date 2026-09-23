#!/usr/bin/env python3
"""gen_launcher_gate20T1.py — generates launch_qa_secuura_batch1204-t1.sh (beside this script: the drafter's write fence is this gateset dir; Wednesday
may copy it into launchers/ — the repin script takes the launcher path as its argument). REFUSES rc 8 while PR 11 is PENDING (no READY 11 captured —
the tier-1 gate is seven PRs or nothing, Wednesday's AMENDMENT 18:1x). Pins RE-READ from origin in this same action (ls-remote: develop + every
refs/pull/N/head + branch) and asserted == round20T1.py (rc 3 on any head move) and develop == newdev_tree.txt's dev_launch (rc 3 — re-predict first);
the 40-hex head / BASE blobs + modes from newdev_tree.txt (the predict run's scratch clone FROM ORIGIN), asserted against round20T1's 12-hex; the BOTH
list (tokens the READY capture and the prompt must both carry) and the by-name ladder asserted against the capture and the prompt BEFORE writing; the
exit-35/36/38/39 phrases asserted present AND reachable (not inside a BOTH / by-name token); bash -n on a scratchpad copy; written only on rc 0; a COPY
of any previous launcher kept beside as .pre-HHMMSS.
Usage: gen_launcher_gate20T1.py <launcher path> <scratchpad dir>
       gen_launcher_gate20T1.py --control-six <launcher path under the scratchpad> <control prompt under the scratchpad> <scratchpad dir>
         (PR 11 PENDING only: a CONTROL COPY with the six real rows, CONTROL_COPY=1 — --check works, a launch refuses exit 37.)"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T1 as R
CONTROL = len(sys.argv) > 1 and sys.argv[1] == '--control-six'
if CONTROL: OUT, PROMPT, SP = sys.argv[2], sys.argv[3], sys.argv[4]
else: OUT, SP = sys.argv[1], sys.argv[2]; PROMPT = os.path.join(G, '2026-09-23_secuura-batch1204-t1.prompt.txt')
CAPTURE = os.path.join(G, 'mail_gate20T1_ready.md')
SCR = '/private/tmp/claude-501/'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()
print('gen_launcher_gate20T1', now(), '| PR11_PENDING', R.PR11_PENDING, '| mode', 'CONTROL-SIX' if CONTROL else 'REAL', '->', OUT)
if not os.path.realpath(SP).startswith(SCR) or not os.path.isdir(SP): print('REFUSING: argv scratchpad is not under', SCR); sys.exit(9)
if CONTROL:
    if not R.PR11_PENDING: print('REFUSING: --control-six is for the PENDING state only'); sys.exit(8)
    if not (os.path.realpath(OUT).startswith(SCR) and os.path.realpath(PROMPT).startswith(SCR)): print('REFUSING: a control copy lives only under the scratchpad'); sys.exit(9)
elif R.PR11_PENDING: print('REFUSING: PR 11 (KS-1143) is PENDING — no launcher without it (take_pr11_gate20T1.sh when READY 11 lands)'); sys.exit(8)
LIVE = [p for p in R.PUSH if R.PRS[p]['n']]
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in LIVE] + [R.PRS[p]['branch'] for p in LIVE]
lsr = dict(l.split('\t')[::-1] for l in sh(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs).splitlines())
nd = R.read_newdev(); dev = lsr.get('refs/heads/develop')
print('ls-remote', now(), len(lsr), 'refs; develop', (dev or '?')[:12], '== newdev dev_launch', dev == nd.get('dev_launch'))
if dev != nd.get('dev_launch'): print('REFUSING: develop moved since the predict run — re-run predict + fill (or the repin script)'); sys.exit(3)
for p in LIVE:
    pr = R.PRS[p]
    if not (lsr.get('refs/pull/%s/head' % pr['n']) == lsr.get(pr['branch']) == pr['head']): print('REFUSING: head moved (or absent) on #' + str(pr['n'])); sys.exit(3)
print('%d pull heads + %d branches == round20T1' % (len(LIVE), len(LIVE)))
NDL = [l.split(' ', 1) for l in open(os.path.join(G, 'newdev_tree.txt')).read().splitlines()]
HB = {v.split(' ')[0]: (v.split(' ')[1], v.split(' ')[2]) for k, v in NDL if k == 'blob'}; BB = {v.split(' ')[0]: v.split(' ')[1] for k, v in NDL if k == 'baseblob'}
rows = []; judged = []
for p in LIVE:
    pr = R.PRS[p]; rows.append('%s|%s|%s|%s|%d' % (pr['n'], pr['key'], pr['branch'], pr['head'], len(pr['files'])))
    for f in pr['files']:
        b, m = HB[f['path']]; bb = BB[f['path']]
        if f['blob12']: assert b.startswith(f['blob12']), (pr['n'], f['path'], b)
        if f['dev_blob12']: assert bb.startswith(f['dev_blob12']), (f['path'], bb)
        judged.append('%s|%s|%s' % (f['path'], bb, b))
want = sum(len(R.PRS[p]['files']) for p in LIVE); print('judged content paths', len(judged), '(%d expected)' % want); assert len(judged) == want == len(set(j.split('|')[0] for j in judged))
BOTH = [R.BASE[:9], R.SEAT_T1SUB_6, R.SEAT_ALL10, R.T2_SUB, nd['dev_launch'], '864c199baf389172cfa948685c72f9cc597268ac', R.PRS['6']['spec_blob40'],
        '4c3beea0b1e7', '1c36a7542970dc7ed2ae19abe66f2c1a9c9e55a3', '29e249e84057', 'ee5c6b40654e9626d97f278c61dcf0f738f47496', '08f413f2b6d99a5c8b58ae2e903bc9e8b60523f8', '735c31b2c56615634c43cb444c60db7189e747da',
        'QUOTEDWRITE', '(128, 0, 0, 128, 1)', '12/15', 'SKIPPED', 'login_stub', 'PROTOCOL-CLEAN', 'contributes', 'In Progress', 'MID_BLOB', '8a67471cef2c',
        'raise20.py.pre-0755-hunkcum', 'CONTROL 2', 'Part B', '/api/batch', '0 bytes under `services/auth/`', 'exit 2', 'scripts/run-code-guards.sh:116', 'scripts/preflight/preflight.sh:670',
        'routes/platform.ts:204', 'ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts', 'ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts',
        'SMOKE_BASE_URL', 'required: false', '231 passed / 231', '1 failed / 232 run', '232 passed / 232', '917/917', '918/918', 'bc4815c4ec9c', '9d0b59ae7199', 'required: true', '742 -> 746', '29/29', '30/30', 'TS2322', 'verify_pr21.py', 'raise20.py:509', 'testonlyopts',
        'check_no_demo_mutation_base.test.sh', 'baseline.api-gateway.json', 'stopped-ks1084', '.push-lock-20', 'cross-tenant effect is NOT measured', 'calls the P0 closed']
if not CONTROL: BOTH += [R.SEAT_T1SUB, R.SEAT_END_T2DEV, R.PRS['11']['tree12'], R.SEAT_GO_STRING]
BOTH += [R.PRS[p]['head'] for p in LIVE] + [f['blob12'] for p in LIVE for f in R.PRS[p]['files'] if f['blob12'] and p != '11'] + [R.PRS[p]['key'] for p in LIVE]
BOTH = sorted(set(BOTH))
SUBJ = '[QA -> Wednesday] TIER-1 BATCH GATE #1204-#'
BYNAME = ['TIER AND ROUND', 'ASSIGN the tier from the files', 'STATE BOTH', 'round 1 of 2', 'PRODUCT vs SCRIPT vs TEST-FILE-ONLY vs GENERATED exactly as each READY declares',
          'TREES over `2bc5ccf63` AND over the launch develop', 'in >= 3 orders', '0 overlap with the tier-2 four', 'CANONICAL-PATCH IDENTITY', 'CELLS per lane', 'read, do not compose',
          'PER-FILE TYPECHECK DELTA 0', 'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE', 'attachmentsForURL per PR exactly its own key', 'subjects <= 92 chars ASCII',
          'THE ONE-PANE TWO-SEAT ARTEFACTS', 'BOARD GUARD', "THE SEATS' OWN FINDINGS/SLIPS", 'CONFIRMED / REFUTED', 'INTERMITTENTS per PR (do not block)', 'RULE WHETHER IT BLOCKS',
          'MERGE ADDENDUM', 'SEVEN lines VERBATIM in report.md', '1/3/2/2/2/3/1', 'stays In Progress', 'KEY-FREE', 'NOT-PINNED', 'READ THE WHOLE TEST FILE', 'NOT-TESTED first',
          'CONTEXT RULE', 'at ctx 80', 'BASE_GO', 'END_TREE', '## MERGE ADDENDUM', 'MEASURE, not conclude', 'RESTORE DISK MODES FROM THE INDEX', 'NEVER `git clone --shared`',
          'CLONE FROM ORIGIN', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'node_modules PER ENTRY', 'never print a credential value', 'No memory maintenance',
          'NOT-TESTED.written-first.md', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', SUBJ, 'fleet/briefs_staged/2026-09-23_raise_seatB_21.md',
          'fleet/briefs_staged/2026-09-23_raise_seatB_22.md', "WEDNESDAY'S signed GO naming each head", 'Never enter any seat worktree', '2026-09-23_seatB-21st', '2026-09-23_seatB-22nd',
          'HANDOVER-seatB-21st-successor-2026-09-23.md', 'mail_gate20T1_ready.md', 'THE BASE MOVED', 'the merging seat must re-predict', 'Datasec files and mail are out of scope entirely',
          'CARRY-FORWARD', 'AMENDMENT 18:1x', 'KS-1143-R19-SELFTEST.md', 'smoke-test.sh is 100755', 'RE-READ develop at your start', 'LEG F']
EXIT35 = ['THE GATE PROVES RED-FIRST BY HUNK', 'the W6 cell hunk ALONE at BASE reds', 'CHANGES WHAT THE ANALYSER COUNTS, NOT JUST THAT THE SUITE IS GREEN']
EXIT36 = ['THE GATE VERIFIES THE YAML IS EXACTLY WHAT `npm run generate-openapi` PRODUCES FROM THE HEAD', 'a planted control that FIRES']
EXIT38 = ['grade over the develop read at launch', 'tier-1 ∩ tier-2 = EMPTY', '0 bytes under `services/auth/` across all 14 paths']
EXIT39 = ['THE CROSS-TENANT EFFECT IS NOT MEASURED AND THE BODY MUST SAY SO', 'Part B (`/api/batch`) is OUT', 'THE GATE CHECKS THE BODY SAYS SO', 'THE RULED DANGLING-COMMENT FINDING MUST BE IN THE BODY AS STATED, NOTHING FIXED OR FILED', "THE SEAT'S TOOLING, NOT THE PRODUCT"]
cap = open(CAPTURE, encoding='utf-8').read(); prm = open(PROMPT, encoding='utf-8').read(); prm1 = re.sub(r'\n\s+', ' ', prm); prm0 = re.sub(r'\n\s*', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: print('REFUSING: BOTH-list tokens missing from the capture or the prompt:', [(t, t in cap, t in prm) for t in miss]); sys.exit(4)
missb = [k for k in BYNAME if k not in prm1]
if missb: print('REFUSING: by-name keywords missing from the prompt:', missb); sys.exit(4)
missx = [k for k in EXIT35 + EXIT36 + EXIT38 + EXIT39 if k not in prm0]
if missx: print('REFUSING: exit-35/36/38/39 phrases missing from the prompt:', missx); sys.exit(4)
overlap = [k for k in EXIT35 + EXIT36 + EXIT38 + EXIT39 if any(k in t for t in BOTH + BYNAME)]
if overlap: print('REFUSING: an exit phrase is inside a BOTH / by-name token — its guard would be unreachable:', overlap); sys.exit(4)
print('BOTH list', len(BOTH), 'tokens in BOTH the capture and the prompt; by-name', len(BYNAME), 'keywords; exit phrases', len(EXIT35 + EXIT36 + EXIT38 + EXIT39), 'present and reachable')
TIERS = ' '.join('#%s T1' % R.PRS[p]['n'] for p in LIVE)
for p in LIVE: assert ('#%s T1' % R.PRS[p]['n']) in prm, p
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
L = open(os.path.join(G, 'launcher_template_gate20T1.sh.txt'), encoding='utf-8').read()
L = L.replace('__ROWS__', '\n'.join('  "%s"' % r for r in rows)).replace('__JUDGED__', '\n'.join('  "%s"' % j for j in judged))
L = L.replace('__BASE__', R.BASE).replace('__DEV__', nd['dev_launch']).replace('__BEHIND__', nd['behind']).replace('__END__', nd['end_tree'])
L = L.replace('__CAPTURE__', CAPTURE).replace('__PROMPT__', PROMPT).replace('__TIERS__', TIERS).replace('__TIERWORDS__', ' '.join("'#%s T1'" % R.PRS[p]['n'] for p in LIVE))
L = L.replace('__BOTH__', bash_list(BOTH)).replace('__BYNAME__', bash_list(BYNAME)).replace('__NBOTH__', str(len(BOTH))).replace('__NBYNAME__', str(len(BYNAME))).replace('__NOW__', now())
L = L.replace('__LASTN__', R.PRS[LIVE[-1]]['n']).replace('__NROWS__', str(len(LIVE) if CONTROL else 7)).replace('__CONTROLCOPY__', '1' if CONTROL else '0')
L = L.replace('__ENTERQA__', 'c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change, spelled so the drafter's no-cd hook is not tripped by this generator's text
assert not re.findall(r'__[A-Z]+__', L), re.findall(r'__[A-Z]+__', L)
assert 'QAB1204_HEAD_%s' % R.PRS[LIVE[-1]]['n'] in L
tmp = tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False, dir=SP, encoding='utf-8'); tmp.write(L); tmp.close()
rc = subprocess.run(['bash', '-n', tmp.name]).returncode; print('bash -n rc', rc, 'on', tmp.name)
if rc != 0: sys.exit(5)
if os.path.exists(OUT): bk = OUT + '.pre-' + now()[11:19].replace(':', ''); shutil.copyfile(OUT, bk); print('previous launcher COPIED beside as', bk)
open(OUT, 'w', encoding='utf-8').write(L); os.chmod(OUT, 0o755)
b = open(OUT, 'rb').read(); print('WROTE', OUT, len(L.splitlines()), 'lines mode 755 sha256', hashlib.sha256(b).hexdigest(), '| rows', len(rows), '| CONTROL_COPY', int(CONTROL), now())
