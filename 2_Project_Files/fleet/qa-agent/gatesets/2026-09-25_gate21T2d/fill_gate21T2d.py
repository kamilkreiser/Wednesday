#!/usr/bin/env python3
"""fill_gate21T2d.py — fill the prompt + launcher templates from pins_gate21T2d.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop and both heads by `git ls-remote` (READ verb, from the Secuura checkout) and REFUSES
(rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate21T2d.py first, never
filled. Pre-checks every seat item (raw grep in BOTH the capture and the filled prompt) and every by-name keyword (in the whitespace-joined prompt)
exactly as the launcher will, and runs `bash -n` on the launcher. Keeps any previous output that differs as <name>.pre-<HHMMSS>. Writes nothing
outside its own directory. Derived from gate21T1c's fill_gate21T1c.py (two rows), with gate21T2c's tier-2 content.
Usage: fill_gate21T2d.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-25_secuura-batch1241-t2.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_batch1241-t2.sh')
CAPTURE = os.path.join(GS, 'mail_gate21T2d_ready.md')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate21T2d.json'), encoding='utf-8'))
if P.get('fail') != 0: die('pins_gate21T2d.json carries fail=%s — predict_gate21T2d.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('pins_gate21T2d.json is a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in P['prs']] + [P['prs'][n]['branch'] for n in P['prs']]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate21T2d.py first' % (L.get('refs/heads/develop'), P['develop']))
for n, p in P['prs'].items():
    if not (L.get('refs/pull/%s/head' % n) == L.get(p['branch']) == p['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a new READY, a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(p['branch']), p['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, both heads)' % P['develop'][:9])

SEAT_ITEMS = [
    'e2d0518df40228f0a183bc4223c7a6840821253e', 'a35569aa020e63b2660b60e48b4f0286c46b27fc',
    # #1241
    '2 failed / 6 passed', 'expected null to deeply equal { passed: 243, failed: 1 }', 'base 1085/1085', 'head 1090/1090', 'd9f45be175d2',
    'exactly 3 groups with passed at group 2', 'No live child vitest emitting a real skipped segment', '15 s budget at :127', 'KS-989 format gate',
    'KS-1226 therefore',
    # #1242
    'head 6/6 on the file', '14/14 (2 suites)', 'the P1 and P2 cells each FAIL', 'D1 and D2 FAIL', 'rolbypassrls false vs TRUE', 'DB-gate refuses loudly',
    'PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED', 'pre_push_hook_base.test.sh 28 passed / 0 failed', 's-b26-pg-ks980', 'postgres:15-alpine',
    '127.0.0.1:55432', 'applied=49 failed=0', '_secuura_migrations', 'Anonymous volume, no reuse', 'docker rm -f',
    'TEST_APP_DATABASE_URL exercised only in its COMPOSED form', 'NO CI wiring', 'pg_isready', 'writerOn()', 'expect(value, message)', 'git checkout --',
]
KEYWORDS = [
    'TIER 2 on both', 'THROUGH-CODE REVIEW', "RED-PROOF CHECK OF THE PR'S OWN PROOF", 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY',
    'A red proof must NAME WHY it went red', 'FINDINGS ONLY', 'A VERDICT IS VALID ONLY AT ITS HEAD', 'FROZEN at two', 'State the FAIL condition before each run',
    'INDEPENDENT REVIEW', 'local-model (Spark)', 'ORIGIN ROUNDS', '2026-09-17-ks1211-1030-e43af4934-tier2-r1', 'consumer_regex_probe.out', 'F-C (Minor)',
    'KS-1226 does NOT close on this PR', 'RE-READ develop at your start', 'answer_seatB25_movedbase', 'THERE IS NO DECLARED OVERLAP IN THIS BATCH',
    'SAME-PACKAGE neighbour', '1094', 'THE RED PROOFS — RE-RUN', '(R-A)', 'T-CAP', 'T-103', 'LIVE-SHAPE (MANDATORY', 'it.skip', 'it.todo',
    '--reporter=default', 'cat -v', 'REFUTED AT RUNTIME', 'vitest 4.1.9', 'R-A,B', '(R-C)', 'T-GUC', 'relforcerowsecurity',
    'THE DISPOSABLE POSTGRES — FOR #1242 ONLY', 'NO SECUURA STACK SLOT IS USED', 'P0 CENSUS BEFORE',
    '0ec12181dd377143118ab17a01b58beb9c09c8137a41a374a1a54ea1f5648dd7', 'P1 THE ENGINE IS NOT YOURS', 'P2 PORT', '55441..55449', 'NEVER 55432',
    'P3 CREDENTIALS', 'mode 0600', 'P4 CREATE', 'qa-g21d-pg-ks980', 'qa_g21d_pg_ks980', 'com.secuura.qa.gate=gate21T2d', 'P5 MIGRATIONS',
    '/opt/homebrew/opt/libpq/bin', 'P6 PRECONDITIONS', 'P7 THE CELLS', '(K0) DB-GATE', '(K1)', '(K2)', 'P8 THE RED PROOFS IN THE DATABASE',
    'P9 TEAR DOWN, ALWAYS', 'PROOF OF GONE', 'NEVER quit Docker Desktop', 'THE FLEET STOP COUNT IN FORCE AFTER #1218', 'LOAD (standing', 'KS-1155',
    'LOGIN_STUB REAPER — YOUR OWN ONLY', 'LEADS for you to grade', 'T-SUPER', 'SELFREAD-SHAPE', 'D1-ROLSUPER', 'APPDSN-ENCODING', 'INTEGRATION-UNWIRED',
    'LIVE-SKIP-SHAPE', 'SUMMARY-READ-103', 'TODO-SEGMENT', 'BY-NAME ITEMS', 'TIER AND ROUND', 'PER-FILE TYPECHECK DELTA 0', 'CENSUS v2',
    'LINEAR LINK HYGIENE', 'MERGE ADDENDUM', 'MG-1', 'MG-3', 'MG-11', 'STAY In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD',
    'READ THE WHOLE TEST FILE', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree',
    '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value',
    'No memory maintenance', 'Datasec files and mail are out of scope entirely', 'EVIDENCE CLASS', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE',
    'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '2026-09-25-batch1241-t2d', '2026-09-25-batch1218-t2c',
    '2026-09-25-batch1234-t1-r1', 'the merging seat re-predicts', 'HOLDS (standing)', 'mail_gate21T2d_ready.md', 'COMMISSION.md',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

def paths(n): return ','.join(sorted(f['path'] for f in P['prs'][n]['files']))
rows = []
for n in ('1241', '1242'):
    for f in P['prs'][n]['files']:
        rows.append('  #%s %s %s (%s; BASE %s; merged over %s: %s)' % (n, f['path'], f['head_blob'], f['mode'], f['base_blob'][:12], P['develop'][:9],
                                                                        'the head blob' if f['merged_blob'] == f['head_blob'] else 'DIFFERS ' + f['merged_blob']))
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_TREE': P['base_tree'], 'DEVELOP': P['develop'],
    'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']), 'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']),
    'MOVE_PATHS': str(P['move_paths']), 'MT_1241': P['prs']['1241']['merged_tree'], 'MT_1242': P['prs']['1242']['merged_tree'],
    'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'], 'FILES_TABLE': '\n'.join(rows), 'PATHS_1241': paths('1241'), 'PATHS_1242': paths('1242'),
    'SEAT_ITEMS': ' \\\n'.join('  ' + sq(w) for w in SEAT_ITEMS), 'KEYWORDS': ' \\\n'.join('  ' + sq(w) for w in KEYWORDS),
    'N_SEAT': str(len(SEAT_ITEMS)), 'N_KW': str(len(KEYWORDS)),
}
def fill(text):
    out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: TOK[m.group(1)] if m.group(1) in TOK else die('unknown token ' + m.group(1)), text)
    left = re.findall(r'\{\{[A-Z0-9_]+\}\}', out)
    if left: die('unfilled tokens ' + ' '.join(left))
    return out

prompt = fill(open(os.path.join(GS, 'prompt_gate21T2d.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate21T2d.TEMPLATE.sh.txt'), encoding='utf-8').read())
cap = open(CAPTURE, encoding='utf-8').read()
for n, p in P['prs'].items():
    if p['head'] not in cap: die('the capture does not name #%s head %s — run capture_mail_gate21T2d.py for that head first' % (n, p['head']))
joined = re.sub(r'\n\s*', ' ', prompt)
miss = [w for w in SEAT_ITEMS if w not in prompt or w not in cap]
if miss: die('seat items not in BOTH the capture and the prompt (raw): %s' % [(w, w in cap, w in prompt) for w in miss])
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
