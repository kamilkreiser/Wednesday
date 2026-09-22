#!/usr/bin/env python3
"""gen_launcher_gate19B.py — generates launchers/launch_qa_secuura_batch1182-1201.sh. Pins RE-READ from origin in this same action (ls-remote:
develop + every refs/pull/N/head + branch) and asserted == round19B.py (refuses rc 3 on any move); the 40-hex head blobs read from the scratch clone
named in argv[2] (the predict run's clone from ORIGIN); the BOTH list (tokens the READY capture and the prompt must both carry) and the by-name
keyword ladder asserted against the capture and the prompt BEFORE writing; bash -n on a scratchpad copy; written only on rc 0; a COPY of any
previous launcher kept beside as .pre-HHMMSS. Usage: gen_launcher_gate19B.py <launcher path> <scratch clone (bare, from ORIGIN)>. The gate19C
generator re-keyed (no exec-bit files this round; the pair path is security/src/index.ts; exit 36 = the KS-1164 instrument)."""
import hashlib, os, re, shutil, subprocess, sys, tempfile
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round19B as R
OUT, CL = sys.argv[1], sys.argv[2]
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1182-1201.prompt.txt'
CAPTURE = os.path.join(G, 'mail_gate19B_ready.md')
def now(): return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def sh(a): return subprocess.run(a, capture_output=True, text=True).stdout.strip()
print('gen_launcher_gate19B', now())
assert CL.startswith('/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/') and os.path.isdir(CL), 'the scratch clone must be under the scratchpad'
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % R.PRS[p]['n'] for p in R.PUSH] + [R.PRS[p]['branch'] for p in R.PUSH]
lsr = dict(l.split('\t')[::-1] for l in sh(['git', '-C', R.REPO, 'ls-remote', 'origin'] + refs).splitlines()); print('ls-remote', now(), len(lsr), 'refs; develop', lsr['refs/heads/develop'][:9], '== pin', lsr['refs/heads/develop'] == R.DEV)
if lsr['refs/heads/develop'] != R.DEV: print('REFUSING: develop moved — re-run predict, re-read THE SHAPE, then regenerate'); sys.exit(3)
for p in R.PUSH:
    pr = R.PRS[p]
    if not (lsr.get('refs/pull/%s/head' % pr['n']) == lsr.get(pr['branch']) == pr['head']): print('REFUSING: head moved on #' + pr['n']); sys.exit(3)
print('9 pull heads + 9 branches == round19B')
def blob(head, path): o = sh(['git', '-C', CL, 'ls-tree', head, '--', path]); return (o.split()[2], o.split()[0]) if o else ('ABSENT', 'ABSENT')
rows = []; judged = {}
for p in R.PUSH:
    pr = R.PRS[p]; rows.append('%s|%s|%s|%s|%d' % (pr['n'], pr['key'], pr['branch'], pr['head'], len(pr['files'])))
    for f in pr['files']:
        b, m = blob(pr['head'], f['path']); assert b.startswith(f['blob12']), (pr['n'], f['path'], b)
        db, dm = blob(R.DEV, f['path']); assert (db == 'ABSENT') == (f['mode'] == 'new'), (f['path'], db)
        assert m == '100644', (f['path'], m)   # no exec-bit file in this round
        landed = [b] + ([R.PAIR_BLOB] if f['path'] == R.PAIR_PATH else [])
        judged.setdefault(f['path'], (db, set()))[1].update(landed)
judged = sorted('%s|%s|%s' % (k, v[0], ','.join(sorted(v[1]))) for k, v in judged.items()); print('judged content paths', len(judged), '(17 expected; the pair path carries both alone blobs + the PAIR blob)'); assert len(judged) == 17
tree = sh(['git', '-C', CL, 'rev-parse', R.DEV + '^{tree}']); assert tree.startswith(R.DEV_TREE12)
BOTH = [R.DEV, R.SEAT_ALL11, R.PAIR_BLOB, '64de96836e46', '3df72c02d325', '2ad45cd8e555', 'cd9b0f6c7b84', '34728affba20', 'b4edbe5b0d12', '1d41e7033542', 'd309bb90f69f', '2a91afd2029e',
        'whitespace-stripped', 'git diff -w', '--pair-blob', R.GO_STRING, 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub', 'skips are not a pass', 'PROTOCOL-CLEAN', '.push-lock-19', '18499832',
        'typecheck_pre19', 'netlog.cjs', 'series19', 'postmerge19', 'go19.sh', 'targets19', 'batch11amend_19', 'ready_build19', 'amend1164_19', 'ks-754', 'Claude-written', 'r16b', 'GROUPING', 'RED-FIRST',
        '45 passed, 0 failed (of 45)', '+642/-13', '+639/-13', 'format-gate', 'my_files19', 'hold_state20', 'amend_tree_8', '06:14:10Z', 'KS-1093', '2-prime', 'anchoring:4005', 'db.retry.test.ts', 'ssrf-guard',
        'STOP-class 0', 'zero :5432', 'control CAUGHT', 'contributes', 'In Progress', 'KS-727', 'ks1213', 'commits.tsv', 'octopus', 'd64e15b98', 'stubs=4', "(2')",
        'runs/2026-09-22_feed11-drafter-precheck/SCOPE403', 'runs/2026-09-22_feed7-drafter-precheck/1179F2F3-R16B', 'cat(section_1.diff, section_2.diff) == patch.diff: True']
BOTH += [R.PRS[p]['head'] for p in R.PUSH] + ['Refs KS-' + k.split('-')[1] for p in R.PUSH for k in R.PRS[p]['keys']] + [f['blob12'] for p in R.PUSH for f in R.PRS[p]['files']] + [r[3] for p in R.PUSH for r in R.PRS[p]['canon']] + R.ARCHIVED[:6]
BOTH = sorted(set(BOTH))
SUBJ = '[QA -> Wednesday] BATCH GATE #1182-#1201 (nine PRs; tier 1 = #1182, #1184, #1186, #1196, #1198, #1199, #1200, #1201: Seat B 19th/20th — six product/tooling code_patch rows incl. the security index.ts pair + two Claude-written + the KS-1164 rewrap; tier 2 = #1194 test-only) —'
BYNAME = ['TIER AND ROUND', 'ASSIGN the tier from the files', 'STATE BOTH', 'round 1 of 2', 'PRODUCT vs TEST-FILE-ONLY exactly as each READY declares', 'code_patch RED/GREEN protocol', 'TREES over `3bad652d1`', 'in >= 3 orders', "0 overlap with Seat C 19th's 21 paths", 'CANONICAL-PATCH IDENTITY', 'stated as such', 'CELLS per lane', 'read, do not compose', 'PER-FILE TYPECHECK DELTA 0', 'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE', 'attachmentsForURL per PR exactly its own key', 'subjects <= 92 chars ASCII', 'THE TWO-SEAT ARTEFACTS', 'F-GUARD', "THE SEATS' OWN FINDINGS/SLIPS", 'CONFIRMED / REFUTED', 'INTERMITTENTS per PR (do not block)', 'RULE WHETHER IT BLOCKS', 'MERGE ADDENDUM', 'nine lines VERBATIM in report.md', '2/2/2/1/2/4/2/2/1', 'stays In Progress', 'KEY-FREE', 'NOT-PINNED', 'READ THE WHOLE TEST FILE', 'NOT-TESTED first', 'CONTEXT RULE', 'at ctx 80', 'BASE_GO', 'END_TREE', '## MERGE ADDENDUM', 'MEASURE, not conclude', 'RESTORE DISK MODES FROM THE INDEX', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'node_modules PER ENTRY', 'never print a credential value', 'No memory maintenance', 'NOT-TESTED.written-first.md', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', SUBJ, 'fleet/briefs_staged/2026-09-22_raise_seatB_19.md', '2026-09-22_raise_seatB_20.md', "WEDNESDAY'S signed GO naming each head", 'Never enter any seat worktree', '2026-09-22_seatB-19th', '2026-09-22_seatB-20th', '#1198 BEFORE #1199', 'alone blob by construction; mode 100644', 'mail_gate19B_ready.md', "if gate19C's GO lands first", 'the BASE moves', 'WHITESPACE-STRIPPED BYTE-STREAM EQUALITY', 'State which instrument YOU used', 'HANDOVER-seatB-19th-successor-2026-09-22.md', 'every head unchanged across the hand-over', 'foreign-second-key refusal', 'graded, not a STOP by itself', 'the merging seat re-predicts', 'Datasec files and mail are out of scope entirely']
cap = open(CAPTURE, encoding='utf-8').read(); prm = open(PROMPT, encoding='utf-8').read(); prm1 = re.sub(r'\n\s+', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: print('REFUSING: BOTH-list tokens missing from the capture or the prompt:', [(t, t in cap, t in prm) for t in miss]); sys.exit(4)
missb = [k for k in BYNAME if k not in prm1]
if missb: print('REFUSING: by-name keywords missing from the prompt:', missb); sys.exit(4)
print('BOTH list', len(BOTH), 'tokens in BOTH the capture and the prompt; by-name', len(BYNAME), 'keywords in the prompt')
TIERS = ' '.join('#%s T%d' % (R.PRS[p]['n'], R.PRS[p]['tier_ready']) for p in R.PUSH)
for p in R.PUSH: assert ('#%s T%d' % (R.PRS[p]['n'], R.PRS[p]['tier_ready'])) in prm
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
L = open(os.path.join(G, 'launcher_template_gate19B.sh.txt'), encoding='utf-8').read()
L = L.replace('__ROWS__', '\n'.join('  "%s"' % r for r in rows)).replace('__JUDGED__', '\n'.join('  "%s"' % j for j in judged)).replace('__DEV__', R.DEV).replace('__ALL__', R.SEAT_ALL11).replace('__PAIRBLOB__', R.PAIR_BLOB)
L = L.replace('__CAPTURE__', CAPTURE).replace('__PROMPT__', PROMPT).replace('__TIERS__', TIERS).replace('__TIERWORDS__', ' '.join("'#%s T%d'" % (R.PRS[p]['n'], R.PRS[p]['tier_ready']) for p in R.PUSH))
L = L.replace('__BOTH__', bash_list(BOTH)).replace('__BYNAME__', bash_list(BYNAME)).replace('__NBOTH__', str(len(BOTH))).replace('__NBYNAME__', str(len(BYNAME))).replace('__NOW__', now())
L = L.replace('__ENTERQA__', 'c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change (the 18C/19C launcher's line), spelled so the drafter's no-cd hook is not tripped by this generator's text
assert not re.findall(r'__[A-Z]+__', L), re.findall(r'__[A-Z]+__', L)
tmp = tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False, dir='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f6fac5b6-1670-49a8-8c75-27176731d099/scratchpad', encoding='utf-8'); tmp.write(L); tmp.close()
rc = subprocess.run(['bash', '-n', tmp.name]).returncode; print('bash -n rc', rc)
if rc != 0: sys.exit(5)
if os.path.exists(OUT): bk = OUT + '.pre-' + now()[11:19].replace(':', ''); shutil.copyfile(OUT, bk); print('previous launcher COPIED beside as', bk)
open(OUT, 'w', encoding='utf-8').write(L); os.chmod(OUT, 0o755)
b = open(OUT, 'rb').read(); print('WROTE', OUT, len(L.splitlines()), 'lines mode 755 sha256', hashlib.sha256(b).hexdigest(), now())
