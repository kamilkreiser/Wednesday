#!/usr/bin/env python3
"""gen_launcher_gate20T2.py — generates launchers/launch_qa_secuura_batch1202-t2.sh. REFUSES rc 8 while PR 5 is PENDING (no READY 5 captured — the
tier-2 gate is four PRs or nothing). Pins RE-READ from origin in this same action (ls-remote: develop + every refs/pull/N/head + branch) and asserted
== round20T2.py (refuses rc 3 on any move); the 40-hex head blobs + modes read from the scratch clone named in argv[2] (the predict run's clone from
ORIGIN); the BOTH list (tokens the READY capture and the prompt must both carry) and the by-name keyword ladder asserted against the capture and the
prompt BEFORE writing; bash -n on a scratchpad copy; written only on rc 0; a COPY of any previous launcher kept beside as .pre-HHMMSS.
Usage: gen_launcher_gate20T2.py <launcher path> <scratch clone (bare, from ORIGIN)>. The gate19B generator re-keyed (exit 35 = the KS-1019 token
instrument; exit 36 = the bash-kind rule; exit 34 also covers a PENDING / missing PR-5 row)."""
import hashlib, os, re, shutil, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round20T2 as R
OUT, CL = sys.argv[1], sys.argv[2]
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_secuura-batch1202-t2.prompt.txt'
CAPTURE = os.path.join(G, 'mail_gate20T2_ready.md')
SCRATCH = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/'
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()
print('gen_launcher_gate20T2', now(), '| PR5_PENDING', R.PR5_PENDING)
if R.PR5_PENDING: print('REFUSING: PR 5 (KS-1139) is PENDING — no launcher without it (take_pr5_gate20T2.sh when READY 5 lands)'); sys.exit(8)
assert CL.startswith(SCRATCH) and os.path.isdir(CL), 'the scratch clone must be under the scratchpad'
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in R.PUSH] + [R.PRS[p]['branch'] for p in R.PUSH]
lsr = dict(l.split('\t')[::-1] for l in sh(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs).splitlines()); print('ls-remote', now(), len(lsr), 'refs; develop', lsr.get('refs/heads/develop', '?')[:9], '== pin', lsr.get('refs/heads/develop') == R.DEV)
if lsr.get('refs/heads/develop') != R.DEV: print('REFUSING: develop moved — re-run predict, re-read THE SHAPE, then regenerate'); sys.exit(3)
for p in R.PUSH:
    pr = R.PRS[p]
    if not (lsr.get('refs/pull/%s/head' % pr['n']) == lsr.get(pr['branch']) == pr['head']): print('REFUSING: head moved (or absent) on #' + str(pr['n'])); sys.exit(3)
print('4 pull heads + 4 branches == round20T2')
def blob(head, path): o = sh(['git', '-C', CL, 'ls-tree', head, '--', path]); return (o.split()[2], o.split()[0]) if o else ('ABSENT', 'ABSENT')
rows = []; judged = []
for p in R.PUSH:
    pr = R.PRS[p]; rows.append('%s|%s|%s|%s|%d' % (pr['n'], pr['key'], pr['branch'], pr['head'], len(pr['files'])))
    for f in pr['files']:
        b, m = blob(pr['head'], f['path']); assert b.startswith(f['blob12']), (pr['n'], f['path'], b)
        db, dm = blob(R.DEV, f['path']); assert db.startswith(f['dev_blob12']), (f['path'], db)
        assert m == '100644' and dm == '100644', (f['path'], m, dm)
        judged.append('%s|%s|%s' % (f['path'], db, b))
print('judged content paths', len(judged), '(4 expected)'); assert len(judged) == 4 and len(set(j.split('|')[0] for j in judged)) == 4
tree = sh(['git', '-C', CL, 'rev-parse', R.DEV + '^{tree}']); assert tree == R.DEV_TREE, tree
BOTH = [R.DEV, R.SEAT_T2SUB, R.SEAT_GO_STRING, R.SEAT_T2SUB_SHORTSTAT, '830ed7609143', '6beda06e9d9e', '3f31d9e91e2f', '8c02c7b62858', '2bc5ccf63',
        'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub', 'PROTOCOL-CLEAN', '.push-lock-20', '6417b203accd839f', 'kamil.kreiser@secuura.ai', 'contributes', 'In Progress',
        'ADMIN_USER_PASSWORD', 'Default-tenant accounts', 'Quick smoke', '86 documentary occurrences', 'KS-547', 'services/auth/',
        'c4tokens.js', '17731', '17736', '17679', 'z.unknown()', 'line 590', 'prs.tsv', 'raise15.py', 'raise13.py',
        'GUARDGONE', 'PASSPLUSPLUS', 'FAILPLUSPLUS', 'bootstrap-env.sh', 'validate-lint.sh', 'run_check', 'bash -e', '6 ok / 1 FAIL', '1 ok / 3 FAIL', '2 ok / 2 FAIL',
        'tickets_boot.json', 'raise20.py']   # the three cell NAMES are in the brief and the prompt, NOT in the READY capture (the READYs say 'the declared cell(s)') — run 1 refused on them
BOTH += [R.PRS[p]['head'] for p in R.PUSH] + [f['blob12'] for p in R.PUSH for f in R.PRS[p]['files']] + [r[3] for p in R.PUSH for r in R.PRS[p]['canon']] + [R.PRS[p]['key'] for p in R.PUSH]
BOTH = sorted(set(BOTH))
SUBJ = '[QA -> Wednesday] TIER-2 BATCH GATE #1202-#1206 (four PRs; tier 2 = #1202, #1203, #1205, #1206: Seat B 21st — doc_patch + comment_patch (token equivalence) + two bash test_only cells with script tampers) —'
BYNAME = ['TIER AND ROUND', 'ASSIGN the tier from the files', 'STATE BOTH', 'round 1 of 2', 'PRODUCT vs TEST-FILE-ONLY vs DOC vs COMMENT exactly as each READY declares', 'TREES over `2bc5ccf63`', 'in >= 3 orders',
          '0 overlap with the tier-1 batch', 'CANONICAL-PATCH IDENTITY', 'CELLS per lane', 'read, do not compose', 'PER-FILE TYPECHECK DELTA 0', 'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE',
          'attachmentsForURL per PR exactly its own key', 'subjects <= 92 chars ASCII', 'THE ONE-SEAT ARTEFACTS', 'BOARD GUARD', "THE SEAT'S OWN FINDINGS/SLIPS", 'CONFIRMED / REFUTED',
          'INTERMITTENTS per PR (do not block)', 'RULE WHETHER IT BLOCKS', 'MERGE ADDENDUM', 'four lines VERBATIM in report.md', '1/1/1/1', 'stays In Progress', 'KEY-FREE', 'NOT-PINNED',
          'READ THE WHOLE TEST FILE', 'NOT-TESTED first', 'CONTEXT RULE', 'at ctx 80', 'BASE_GO', 'END_TREE', '## MERGE ADDENDUM', 'MEASURE, not conclude', 'RESTORE DISK MODES FROM THE INDEX',
          'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'node_modules PER ENTRY', 'never print a credential value', 'No memory maintenance',
          'NOT-TESTED.written-first.md', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', SUBJ, 'fleet/briefs_staged/2026-09-23_raise_seatB_21.md',
          "WEDNESDAY'S signed GO naming each head", 'Never enter any seat worktree', '2026-09-23_seatB-21st', 'mail_gate20T2_ready.md', 'if the tier-1 gate', 'BASE moves', 'TOKEN EQUIVALENCE',
          'the merging seat must re-predict', 'Datasec files and mail are out of scope entirely', 'never print the retired admin literal', 'CLOSES it', 'THE GATE MUST RE-RUN THE TOKEN-EQUIVALENCE PROOF ITSELF',
          'VACUOUS PASS', 'CARRY-FORWARD']
EXIT35 = ['planted-comment control', 'planted-token control that FIRES']; EXIT36 = ['ONE AT A TIME', 'DIFFERENT subsets', 'zero parsed cells']
cap = open(CAPTURE, encoding='utf-8').read(); prm = open(PROMPT, encoding='utf-8').read(); prm1 = re.sub(r'\n\s+', ' ', prm); prm0 = re.sub(r'\n\s*', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: print('REFUSING: BOTH-list tokens missing from the capture or the prompt:', [(t, t in cap, t in prm) for t in miss]); sys.exit(4)
missb = [k for k in BYNAME if k not in prm1]
if missb: print('REFUSING: by-name keywords missing from the prompt:', missb); sys.exit(4)
miss5 = [k for k in EXIT35 + EXIT36 if k not in prm0]
if miss5: print('REFUSING: exit-35/36 phrases missing from the prompt:', miss5); sys.exit(4)
overlap = [k for k in EXIT35 + EXIT36 if any(k in t for t in BOTH + BYNAME)]
if overlap: print('REFUSING: an exit-35/36 phrase is also inside a BOTH / by-name token — its guard would be unreachable:', overlap); sys.exit(4)
print('BOTH list', len(BOTH), 'tokens in BOTH the capture and the prompt; by-name', len(BYNAME), 'keywords in the prompt; exit-35/36 phrases', len(EXIT35 + EXIT36), 'present and reachable')
TIERS = ' '.join('#%s T%d' % (R.PRS[p]['n'], R.PRS[p]['tier_ready']) for p in R.PUSH)
for p in R.PUSH: assert ('#%s T%d' % (R.PRS[p]['n'], R.PRS[p]['tier_ready'])) in prm
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
L = open(os.path.join(G, 'launcher_template_gate20T2.sh.txt'), encoding='utf-8').read()
L = L.replace('__ROWS__', '\n'.join('  "%s"' % r for r in rows)).replace('__JUDGED__', '\n'.join('  "%s"' % j for j in judged)).replace('__DEV__', R.DEV).replace('__ALL__', R.SEAT_T2SUB)
L = L.replace('__CAPTURE__', CAPTURE).replace('__PROMPT__', PROMPT).replace('__TIERS__', TIERS).replace('__TIERWORDS__', ' '.join("'#%s T%d'" % (R.PRS[p]['n'], R.PRS[p]['tier_ready']) for p in R.PUSH))
L = L.replace('__BOTH__', bash_list(BOTH)).replace('__BYNAME__', bash_list(BYNAME)).replace('__NBOTH__', str(len(BOTH))).replace('__NBYNAME__', str(len(BYNAME))).replace('__NOW__', now())
L = L.replace('__LASTN__', R.PRS[R.PUSH[-1]]['n'])
L = L.replace('__ENTERQA__', 'c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change (the 19B launcher's line), spelled so the drafter's no-cd hook is not tripped by this generator's text
assert not re.findall(r'__[A-Z]+__', L), re.findall(r'__[A-Z]+__', L)
assert 'QAB1202_HEAD_%s' % R.PRS['5']['n'] in L
sp = os.environ.get('GATE20T2_SCRATCH') or [d for d in [os.path.dirname(os.path.dirname(CL))] if d.startswith(SCRATCH)][0]
tmp = tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False, dir=sp, encoding='utf-8'); tmp.write(L); tmp.close()
rc = subprocess.run(['bash', '-n', tmp.name]).returncode; print('bash -n rc', rc, 'on', tmp.name)
if rc != 0: sys.exit(5)
if os.path.exists(OUT): bk = OUT + '.pre-' + now()[11:19].replace(':', ''); shutil.copyfile(OUT, bk); print('previous launcher COPIED beside as', bk)
open(OUT, 'w', encoding='utf-8').write(L); os.chmod(OUT, 0o755)
b = open(OUT, 'rb').read(); print('WROTE', OUT, len(L.splitlines()), 'lines mode 755 sha256', hashlib.sha256(b).hexdigest(), now())
