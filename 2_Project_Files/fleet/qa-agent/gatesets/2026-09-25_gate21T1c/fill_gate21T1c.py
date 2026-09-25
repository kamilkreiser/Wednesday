#!/usr/bin/env python3
"""fill_gate21T1c.py — fill the prompt + launcher templates from pins_gate21T1c.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop and both heads by `git ls-remote` (READ verb, from the Secuura checkout) and REFUSES
(rc 1) if they disagree with the pins — a stale pin is re-measured with predict_gate21T1c.py first, never filled. Pre-checks every seat item (raw
grep in BOTH the capture and the filled prompt) and every by-name keyword (in the whitespace-joined prompt) exactly as the launcher will, and runs
`bash -n` on the launcher. Keeps any previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
Usage: fill_gate21T1c.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-25_secuura-batch1234-t1.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_batch1234-t1.sh')
CAPTURE = os.path.join(GS, 'mail_gate21T1c_ready.md')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate21T1c.json'), encoding='utf-8'))
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1234/head', 'refs/pull/1239/head'],
                    capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d' % ls.returncode)
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate21T1c.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ('1234', '1239'):
    if L.get('refs/pull/%s/head' % n) != P['prs'][n]['head']: die('#%s head moved: %s != %s' % (n, L.get('refs/pull/%s/head' % n), P['prs'][n]['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, both heads)' % P['develop'][:9])

SEAT_ITEMS = [
    '6320a61d86b5d3fb9b693ea5fefb42050e1d2a43', '42c20e998a1a69887b8378968a8ff4f19106c24b',
    '41 passed, 8 failed', '49 passed, 0 failed', 'shell suites: 57 passed, 0 failed, 0 skipped (of 57)', 'preflight.sh:643',
    '28 passed, 0 failed', 'PROTOCOL-CLEAN', 'contributes', 'db.ts:302-336', 'index.ts:225', 'adminConfig.ts:30', 'services.bicep:798',
    '2 failed / 27', 'G-S1', 'G-S2', '74 / 865', 'MULTI_TENANCY_ENABLED=false', 'withTenant', 'D1/D2', 'C7', 'RUNNER_SH', 'KS-1135', 'KS-1089',
    '218', '/transfer-custody', 'KS-1155',
]
KEYWORDS = [
    'TIER 1 on both', 'THROUGH-CODE REVIEW', "RED-PROOF CHECK OF THE PR'S OWN PROOF", 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY',
    'A red proof must NAME WHY it went red', 'FINDINGS ONLY', 'A VERDICT IS VALID ONLY AT ITS HEAD', 'FROZEN at two', 'RE-READ develop at your start',
    'answer_seatB25_movedbase', 'PATCH-ID EQUALITY', 'THE STACK — ONCE, FOR #1239', 'S0 CENSUS BEFORE', 'S1 START / WAIT FOR THE ENGINE',
    'S2 IMMEDIATELY, BEFORE STARTING ANYTHING', 'restart: unless-stopped', 'S3 SLOT', 'SECUURA_STACK_SLOT', 'S4 BUILD ONCE', 'S5 LEGS 3/4/8',
    'spec-auth-conformance.mjs', 'path-resolvability.mjs', 'spec-endpoint-consistency.mjs', 'LEG 4 HONESTY', 'S8 ATTRIBUTION', 'S9 TEAR DOWN, ALWAYS',
    'VOLUMES KEPT', 's-b26-pg-ks980', ':55432', 'THE ROLLBACK CELLS, IN BOTH MULTI_TENANCY MODES', 'THE TRAP THE DRAFTER MEASURED',
    'falling back to single-tenant mode', 'R0 PRECONDITIONS', 'R1 THE COMMITTED CELLS AS SHIPPED', 'R2 BRANCH WITNESS', 'T-POOL', 'T-PRISMA',
    'R3 THE ROUTE-LEVEL RED PROOF', 'D-SHARE', 'C-CUSTODY', 'g21c_flip', 'R4 THE POOL-IDENTITY QUESTION', 'getDefaultPool()', 'tenant-context.ts:93',
    'R5 THE req.db MEASUREMENT CONDITION', 'R6 THE RESIDUAL RULE', 'the APP role', 'VACUOUS', 'the throw-never-return rule',
    'FLEET SAFETY RULE 1 IS IN FORCE', "--grep '#1218'", 'run_shell_suites.test.sh', 'rule 2\'', 'THE SEAT\'S RED PROOF', '/bin/bash (3.2.57',
    "WEDNESDAY'S Q3 CONDITION", 'KS1127-push1.out', 'rss_short_tmpdir', 'SKIP classifier', 'PIPESTATUS[0]', 'LOAD (standing', 'KS-1155',
    'LOGIN_STUB REAPER — YOUR OWN ONLY', 'LEADS for you to grade', 'BY-NAME ITEMS', 'TIER AND ROUND', 'THE RED PROOFS, RE-RUN',
    'PER-FILE TYPECHECK DELTA 0', 'CENSUS v2', 'LINEAR LINK HYGIENE', 'MERGE ADDENDUM', 'MG-1', 'MG-3', 'MG-11', 'STAY In Progress', 'KEY-FREE',
    'NOT-PINNED', 'CARRY-FORWARD', 'READ THE WHOLE TEST FILE', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it',
    'Never enter any seat worktree', '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN',
    'never print a credential value', 'No memory maintenance', 'Datasec files and mail are out of scope entirely', 'NOT-TESTED.written-first.md',
    'THE CONTEXT RULE', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '2026-09-25-batch1234-t1-r1',
    '2026-09-25-batch1224-t1-r1', '2026-09-25-batch1213-t1-r1', '2026-09-25-batch1225-t2-r1', 'the merging seat re-predicts', 'HOLDS (standing)',
    'mail_gate21T1c_ready.md', 'COMMISSION.md', 'ROUTE-ROLLBACK', 'POOL-BRANCH-WITNESS', 'PLATFORM-URL-TRAP', 'RSS-TMPDIR-RESTORE', 'QA8-BASH32',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

def paths(n): return ','.join(sorted(f['path'] for f in P['prs'][n]['files']))
rows = []
for n in ('1234', '1239'):
    for f in P['prs'][n]['files']:
        extra = (' MERGED %s over %s (OVERLAP: the move touched it; patch-id %s equal)' % (f['merged_blob'], P['develop'][:9], f['patch_id'][:12])
                 if f['overlap'] else '')
        rows.append('  #%s %s %s (%s; BASE %s)%s' % (n, f['path'], f['head_blob'], f['mode'], f['base_blob'] if f['base_blob'] == 'ABSENT' else f['base_blob'][:12], extra))
npaths = sum(len(P['prs'][n]['files']) for n in P['prs'])
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_TREE': P['base_tree'], 'DEVELOP': P['develop'],
    'DEVELOP_SHORT': P['develop'][:9], 'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']),
    'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']), 'MOVE_PATHS': str(P['move_paths']), 'MT_1234': P['prs']['1234']['merged_tree'],
    'MT_1239': P['prs']['1239']['merged_tree'], 'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'], 'NPATHS': str(npaths),
    'FILES_TABLE': '\n'.join(rows), 'PATHS_1234': paths('1234'), 'PATHS_1239': paths('1239'),
    'SEAT_ITEMS': ' \\\n'.join('  ' + sq(w) for w in SEAT_ITEMS), 'KEYWORDS': ' \\\n'.join('  ' + sq(w) for w in KEYWORDS),
    'N_SEAT': str(len(SEAT_ITEMS)), 'N_KW': str(len(KEYWORDS)),
}
def fill(text):
    out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: TOK[m.group(1)] if m.group(1) in TOK else die('unknown token ' + m.group(1)), text)
    left = re.findall(r'\{\{[A-Z0-9_]+\}\}', out)
    if left: die('unfilled tokens ' + ' '.join(left))
    return out

prompt = fill(open(os.path.join(GS, 'prompt_gate21T1c.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate21T1c.TEMPLATE.sh.txt'), encoding='utf-8').read())
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
