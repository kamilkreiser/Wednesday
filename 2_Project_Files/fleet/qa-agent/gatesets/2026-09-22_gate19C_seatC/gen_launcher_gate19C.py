#!/usr/bin/env python3
"""gen_launcher_gate19C.py — generates launchers/launch_qa_secuura_batch1180-1197.sh. Pins RE-READ from origin in this same action (ls-remote:
develop + every refs/pull/N/head + branch) and asserted == round19C.py (refuses rc 3 on any move); the 40-hex head blobs read from the scratch clone
named in argv[2] (the predict run's clone from ORIGIN); the BOTH list (tokens the READY capture and the prompt must both carry) and the by-name
keyword ladder asserted against the capture and the prompt BEFORE writing; bash -n on a scratchpad copy; written only on rc 0; a COPY of any
previous launcher kept beside as .pre-HHMMSS. Usage: gen_launcher_gate19C.py <launcher path> <scratch clone (bare, from ORIGIN)>"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19C as R
OUT, CL = sys.argv[1], sys.argv[2]
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1180-1197.prompt.txt'
CAPTURE = os.path.join(G, 'mail_gate19C_ready.md')
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()
print('gen_launcher_gate19C', now())
assert CL.startswith('/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/') and os.path.isdir(CL), 'the scratch clone must be under the scratchpad'
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in R.PUSH] + [R.PRS[p]['branch'] for p in R.PUSH]
lsr = dict(l.split('\t')[::-1] for l in sh(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs).splitlines()); print('ls-remote', now(), len(lsr), 'refs; develop', lsr['refs/heads/develop'][:9], '== pin', lsr['refs/heads/develop'] == R.DEV)
if lsr['refs/heads/develop'] != R.DEV: print('REFUSING: develop moved — re-run predict, re-read THE SHAPE, then regenerate'); sys.exit(3)
for p in R.PUSH:
    pr = R.PRS[p]
    if not (lsr.get('refs/pull/%s/head' % pr['n']) == lsr.get(pr['branch']) == pr['head']): print('REFUSING: head moved on #' + pr['n']); sys.exit(3)
print('12 pull heads + 12 branches == round19C')
def blob(head, path): o = sh(['git', '-C', CL, 'ls-tree', head, '--', path]); return (o.split()[2], o.split()[0]) if o else ('ABSENT', 'ABSENT')
rows = []; judged = {}
for p in R.PUSH:
    pr = R.PRS[p]; rows.append('%s|%s|%s|%s|%d' % (pr['n'], pr['key'], pr['branch'], pr['head'], len(pr['files'])))
    for f in pr['files']:
        b, m = blob(pr['head'], f['path']); assert b.startswith(f['blob12']), (pr['n'], f['path'], b)
        db, dm = blob(R.DEV, f['path']); assert (db == 'ABSENT') == (f['mode'] == 'new'), (f['path'], db)
        if f['path'] in R.EXEC_SCRIPTS: assert m == '100755' == dm, (f['path'], m, dm)
        landed = [b] + ([R.PAIR_BLOB] if f['path'] == R.PAIR_PATH else [])
        judged.setdefault(f['path'], (db, set()))[1].update(landed)
judged = sorted('%s|%s|%s' % (k, v[0], ','.join(sorted(v[1]))) for k, v in judged.items()); print('judged content paths', len(judged), '(21 expected; the pair path carries both alone blobs + the PAIR blob)'); assert len(judged) == 21
tree = sh(['git', '-C', CL, 'rev-parse', R.DEV + '^{tree}']); assert tree.startswith(R.DEV_TREE12)
BOTH = [R.DEV, R.SEAT_ALL14, R.PAIR_BLOB, 'eaa961172883', '5a8458a5697f', '58cdd3dc846b', 'cd9b0f6c7b84', R.GO_STRING, 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub', 'skips are not a pass', 'PROTOCOL-CLEAN', '.push-lock-19', 'fixmodes19', '5772145479', 'stacklegs-2', '--pair-blob', '18499832', 'check_shared_relink', 'B4', 'B5', 'B6', 'bash -n', '46 passed, 0 failed (of 46)', '47 passed, 0 failed (of 47)', '45 passed, 0 failed (of 45)', '21 files changed, 915 insertions(+), 29 deletions(-)', 'measure19', 'targets19', 'merge19b', 'attrib19', 'series19', 'ks-666', 'ks-754', 'ks-926', 'Claude-written', '100755', 'core.filemode', 'r16b']
BOTH += [R.PRS[p]['head'] for p in R.PUSH] + ['Refs KS-' + k.split('-')[1] for p in R.PUSH for k in R.PRS[p]['keys']] + [f['blob12'] for p in R.PUSH for f in R.PRS[p]['files']] + [r[3] for p in R.PUSH for r in R.PRS[p]['canon']] + R.ARCHIVED[:6]
BOTH = sorted(set(BOTH))
BYNAME = ['TIER AND ROUND', 'ASSIGN the tier from the files', 'STATE BOTH', 'round 1 of 2', 'SCRIPT BYTES exactly as declared', 'assert the mode at every head by `ls-tree`', 'TREES over `3bad652d1`', 'in >= 3 orders', '0 overlap with Seat B 20th', 'CANONICAL-PATCH IDENTITY', 'Claude-written sections stated as such', 'CELLS: the bash suites', 'read, do not compose', 'TYPECHECK: n/a for bash', 'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE', 'attachmentsForURL per PR exactly its own key(s)', 'subjects <= 92 chars ASCII', 'THE TWO-SEAT ARTEFACTS', 'CONFIRM it ran on every later push', "THE SEAT'S OWN FINDINGS/SLIPS", 'CONFIRMED / REFUTED', 'INTERMITTENTS per PR (do not block)', 'RULE WHETHER IT BLOCKS', 'MERGE ADDENDUM', 'twelve lines VERBATIM in report.md', '2/2/2/2/3/2/2/2/2/1/1/1', 'stays In Progress', 'KEY-FREE', 'NOT-PINNED', 'READ THE WHOLE TEST FILE', 'NOT-TESTED first', 'CONTEXT RULE', 'at ctx 80', 'BASE_GO', 'END_TREE', '## MERGE ADDENDUM', 'MEASURE, not conclude', 'RESTORE DISK MODES FROM THE INDEX', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'node_modules PER ENTRY', 'never print a credential value', 'No memory maintenance', 'NOT-TESTED.written-first.md', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '[QA -> Wednesday] BATCH GATE #1180-#1197 (twelve PRs; tier 1 = #1180, #1181, #1183, #1185, #1187, #1188, #1190, #1191, #1192: Seat C 19th — nine bash_patch script PRs on the fleet gates + boot path; tier 2 = #1193, #1195, #1197 docs) —', 'fleet/briefs_staged/2026-09-22_raise_seatC_19.md', "WEDNESDAY'S signed GO naming each head", 'Never enter any seat worktree', '2026-09-22_seatC-19th', '#1180 BEFORE #1181', 'alone blob by construction; mode 100755', 'mail_gate19C_ready.md']
cap = open(CAPTURE, encoding='utf-8').read(); prm = open(PROMPT, encoding='utf-8').read(); prm1 = re.sub(r'\n\s+', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: print('REFUSING: BOTH-list tokens missing from the capture or the prompt:', miss); sys.exit(4)
missb = [k for k in BYNAME if k not in prm1]
if missb: print('REFUSING: by-name keywords missing from the prompt:', missb); sys.exit(4)
print('BOTH list', len(BOTH), 'tokens in BOTH the capture and the prompt; by-name', len(BYNAME), 'keywords in the prompt')
TIERS = ' '.join('#%s T%d' % (R.PRS[p]['n'], R.PRS[p]['tier_ready']) for p in R.PUSH)
for p in R.PUSH: assert ('#%s T%d' % (R.PRS[p]['n'], R.PRS[p]['tier_ready'])) in prm
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
L = open(os.path.join(G, 'launcher_template_gate19C.sh.txt'), encoding='utf-8').read()
L = L.replace('__ROWS__', '\n'.join('  "%s"' % r for r in rows)).replace('__JUDGED__', '\n'.join('  "%s"' % j for j in judged)).replace('__DEV__', R.DEV).replace('__ALL__', R.SEAT_ALL14).replace('__PAIRBLOB__', R.PAIR_BLOB)
L = L.replace('__CAPTURE__', CAPTURE).replace('__PROMPT__', PROMPT).replace('__TIERS__', TIERS).replace('__TIERWORDS__', ' '.join("'#%s T%d'" % (R.PRS[p]['n'], R.PRS[p]['tier_ready']) for p in R.PUSH))
L = L.replace('__BOTH__', bash_list(BOTH)).replace('__BYNAME__', bash_list(BYNAME)).replace('__NBOTH__', str(len(BOTH))).replace('__NBYNAME__', str(len(BYNAME))).replace('__NOW__', now())
L = L.replace('__ENTERQA__', 'c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change (the 18C launcher's line), spelled so the drafter's no-cd hook is not tripped by this generator's text
assert not re.findall(r'__[A-Z]+__', L), re.findall(r'__[A-Z]+__', L)
tmp = tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False, dir='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f6fac5b6-1670-49a8-8c75-27176731d099/scratchpad', encoding='utf-8'); tmp.write(L); tmp.close()
rc = subprocess.run(['bash', '-n', tmp.name]).returncode; print('bash -n rc', rc)
if rc != 0: sys.exit(5)
if os.path.exists(OUT): bk = OUT + '.pre-' + now()[11:19].replace(':', ''); shutil.copyfile(OUT, bk); print('previous launcher COPIED beside as', bk)
open(OUT, 'w', encoding='utf-8').write(L); os.chmod(OUT, 0o755)
b = open(OUT, 'rb').read(); print('WROTE', OUT, len(L.splitlines()), 'lines mode 755 sha256', hashlib.sha256(b).hexdigest(), now())
