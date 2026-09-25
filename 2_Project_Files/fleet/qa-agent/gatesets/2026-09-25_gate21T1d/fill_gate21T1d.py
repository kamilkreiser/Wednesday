#!/usr/bin/env python3
"""fill_gate21T1d.py — fill the prompt + launcher templates from pins_gate21T1d.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop and the head by `git ls-remote` (READ verb, from the Secuura checkout) and REFUSES
(rc 1) if they disagree with the pins — a stale pin is re-measured with predict_gate21T1d.py first, never filled. Pre-checks every seat item (raw
grep in BOTH the capture and the filled prompt) and every by-name keyword (in the whitespace-joined prompt) exactly as the launcher will, and runs
`bash -n` on the launcher. Keeps any previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
Usage: fill_gate21T1d.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-25_secuura-batch1239-t1r2.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_batch1239-t1r2.sh')
CAPTURE = os.path.join(GS, 'mail_gate21T1d_ready.md')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate21T1d.json'), encoding='utf-8'))
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1239/head'], capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate21T1d.py first' % (L.get('refs/heads/develop'), P['develop']))
if L.get('refs/pull/1239/head') != P['head']: die('#1239 head moved: %s != %s' % (L.get('refs/pull/1239/head'), P['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, head %s)' % (P['develop'][:9], P['head'][:9]))

def subj_len(sha):
    r = subprocess.run(['git', '-C', CHECKOUT, 'log', '-1', '--format=%s', sha], capture_output=True, text=True)
    if r.returncode != 0: die('git log %s rc %d' % (sha[:9], r.returncode))
    return str(len(r.stdout.rstrip('\n')))

SEAT_ITEMS = [
    'c8e1875c21e994a746e36c8b8efec8de1d9dbc98', '42c20e998a1a', 'e68e2f0e8', '5 passed / 5', '1 failed / 4 passed', 'Expected: 0, Received: 1',
    '29 passed / 29', '1 failed / 28 passed', '865 passed / 865', '5 failed / 5', "Cannot find module '.prisma/client/default'", 'KS1305', '22021',
    's-b27-pg-ks1263', '55437', 'ROUTE-ROLLBACK', '4 failed, 1 passed', '57 passed, 0 failed (of 57)', 'check_no_latest_tags.test.sh',
    'pre_push_hook_base_fixture_guard.test.sh', 'audit-contract 59/59', 'HANDOVER-NOTES-tools.md', 'KS-1263',
]
KEYWORDS = [
    'TIER 1: a FULL gate', 'THROUGH-CODE REVIEW', "RED-PROOF CHECK OF THE PR'S OWN PROOF", 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY',
    'A red proof must NAME WHY it went red', 'FINDINGS ONLY', 'A VERDICT IS VALID ONLY AT ITS HEAD', 'PRIOR ROUND: round 1 gated',
    '2026-09-25-batch1234-t1-r1', 'a FAST-FORWARD of round 1', 'TEST-ONLY', 'RE-READ develop at your start', "WEDNESDAY'S ROUND-2 RULING (b)",
    'KS-1305', 'KS-1304', 'F5 POOL-BRANCH-WITNESS', 'F7 Polish', 'C-CUSTODY', 'g21T1d_flip', 'THE DISPOSABLE POSTGRES', 'P0 CENSUS BEFORE',
    'P1 THE ENGINE IS NOT YOURS', 'P2 PORT', 'P3 CREDENTIALS', 'P4 CREATE', 'P5 MIGRATIONS, INSIDE YOUR CONTAINER', 'P6 R0 PRECONDITIONS',
    'P9 TEAR DOWN, ALWAYS', 'qa-g21d-pg-ks980', 'log_statement=all', 'init-platform', 'Platform schema initialized.', 'THE MATRIX', 'M-HEAD',
    'M-DEVT', 'M-BASE0', 'M-MERGED', 'T-TRAP', 'T-POOL', 'T-ROUTE', 'MODE-F', 'W1 the log lines', 'W2 YOUR container', 'Loaded N tenant configs',
    'falling back to single-tenant mode', 'Failed to load tenant configs', 'turns a COMMIT of an ABORTED transaction', 'G-S2 AND THE STRUCTURAL CELLS',
    '__txClient', 'INSTRUMENT FAULT', 'SPLIT tamper', 'PER-FILE TYPECHECK DELTA 0', 'legs 3/4/8: not applicable, no surface', 'LEADS for you to grade',
    'SUPERUSER-DSN / RLS INERT', "THE SEAT'S PLATFORM DB", "THE WITNESS'S STRENGTH", 'THE BASE SEAM', 'SWALLOWED SEEDS', 'ORDER DEPENDENCE',
    "MODE F's SWALLOW", "THE SEAT'S DISCLOSURES", 'THE DEVELOP DRIFT', 'LOGIN_STUB REAPER — YOUR OWN ONLY', 'BY-NAME ITEMS', 'CENSUS v2',
    'LINEAR LINK HYGIENE', 'KS-1155 (x2) and KS-1228', 'MG-1', 'MG-3', 'MG-11', 'STAYS In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD',
    'READ THE WHOLE TEST FILES', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree',
    '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value',
    'No memory maintenance', 'Datasec files and mail are out of scope entirely', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE',
    'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '2026-09-25-batch1239-t1-r2', 'RESIDUE TICKET SHAPES',
    'mail_gate21T1d_ready.md', 'COMMISSION.md', 'EVIDENCE CLASS', '2026-09-25-batch1241-t2d', 'NO STANDALONE run',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

rows = []
for f in P['files']:
    extra = (' | MERGED %s over %s (OVERLAP: the move touched it; patch-id %s equal)' % (f['merged_blob'], P['develop'][:9], f['patch_id'][:12])
             if f['overlap'] else '')
    rows.append('  %s %s (%s; BASE %s)%s' % (f['path'], f['head_blob'], f['mode'], f['base_blob'] if f['base_blob'] == 'ABSENT' else f['base_blob'][:12], extra))
reg = []
for h, r in sorted(P['region'].items()):
    reg.append('  %s handler: BASE lines %d-%d | develop %d-%d | head %d-%d | merged %d-%d | move hunks inside: none' % (
        h.strip("',"), r['base_span'][0], r['base_span'][1], r['develop_span'][0], r['develop_span'][1], r['head_span'][0], r['head_span'][1],
        r['merged_span'][0], r['merged_span'][1]))
ks1263 = [f for f in P['files'] if f['path'].endswith('ks1263-multi-write-rolls-back.integration.test.ts')][0]
subst = '; '.join('%s (by %s)' % (k, ', '.join(v)) for k, v in sorted(P['substrate_touched'].items())) or 'none'
r2ns = '; '.join('%s +%s/-%s' % (l.split('\t')[2].rsplit('/', 1)[-1], l.split('\t')[0], l.split('\t')[1]) for l in P['r2_numstat'].splitlines())
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_SHORT': P['base'][:9], 'BASE_TREE': P['base_tree'],
    'R1': P['r1'], 'R1_SHORT': P['r1'][:9], 'HEAD': P['head'], 'HEAD_SHORT': P['head'][:9], 'DEVELOP': P['develop'], 'DEVELOP_SHORT': P['develop'][:9],
    'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']), 'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']),
    'MT': P['merged_tree'], 'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'].strip(), 'SHORTSTAT': P['shortstat'].strip(),
    'FILES_TABLE': '\n'.join(rows), 'PATHS': ','.join(sorted(f['path'] for f in P['files'])), 'REGION_TABLE': '\n'.join(reg),
    'DOCS_HUNKS': ', '.join('%d-%d' % (a, b) for a, b in P['docs_move_hunks']), 'SUBSTRATE': subst, 'R2_NUMSTAT': r2ns,
    'KS1263_BLOB': ks1263['head_blob'], 'R1_SUBJ_LEN': subj_len(P['r1']), 'HEAD_SUBJ_LEN': subj_len(P['head']),
    'SEAT_ITEMS': ' \\\n'.join('  ' + sq(w) for w in SEAT_ITEMS), 'KEYWORDS': ' \\\n'.join('  ' + sq(w) for w in KEYWORDS),
    'N_SEAT': str(len(SEAT_ITEMS)), 'N_KW': str(len(KEYWORDS)),
}
def fill(text):
    out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: TOK[m.group(1)] if m.group(1) in TOK else die('unknown token ' + m.group(1)), text)
    left = re.findall(r'\{\{[A-Z0-9_]+\}\}', out)
    if left: die('unfilled tokens ' + ' '.join(left))
    return out

prompt = fill(open(os.path.join(GS, 'prompt_gate21T1d.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate21T1d.TEMPLATE.sh.txt'), encoding='utf-8').read())
cap = open(CAPTURE, encoding='utf-8').read()
joined = re.sub(r'\n\s*', ' ', prompt)
miss = [w for w in SEAT_ITEMS if w not in prompt or w not in cap]
if miss: die('seat items not in BOTH the capture and the prompt (raw): %s' % miss)
missk = [w for w in KEYWORDS if w not in joined]
if missk: die('by-name keywords not in the joined prompt: %s' % missk)
stamp = datetime.datetime.now().strftime('%H%M%S')
for path, body, mode in ((PROMPT_OUT, prompt, 0o644), (LAUNCH_OUT, launch, 0o755)):
    if os.path.exists(path) and open(path, encoding='utf-8').read() != body:
        shutil.copy2(path, path + '.pre-' + stamp)
    with open(path, 'w', encoding='utf-8') as f: f.write(body)
    os.chmod(path, mode)
bn = subprocess.run(['bash', '-n', LAUNCH_OUT], capture_output=True, text=True)
if bn.returncode != 0: die('bash -n on the launcher rc %d: %s' % (bn.returncode, bn.stderr.strip()))
print('prompt  %s: %d lines, %d bytes' % (PROMPT_OUT, prompt.count('\n'), len(prompt.encode())))
print('launcher %s: %d lines, mode 755, bash -n rc 0' % (LAUNCH_OUT, launch.count('\n')))
print('seat items %d (raw, both files) · keywords %d (joined prompt) · develop %s · END_TREE %s' % (len(SEAT_ITEMS), len(KEYWORDS), P['develop'], P['end_tree']))
sys.exit(0)
