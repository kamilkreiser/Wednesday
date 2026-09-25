#!/usr/bin/env python3
"""fill_gate24T2c.py — fill the prompt + launcher templates from pins_gate24T2c.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop and the seven heads by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate24T2c.py first,
never filled. Pre-checks every seat item (raw grep in BOTH the capture and the filled prompt) and every by-name keyword (in the whitespace-joined prompt)
exactly as the launcher will, and runs `bash -n` on the launcher. Keeps any previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside
its own directory. Derived from gate24T2b's fill script, re-keyed to this batch's seven rows (no stack).
Usage: fill_gate24T2c.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-26_secuura-batch1245r2-t2.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_batch1245r2-t2.sh')
CAPTURE = os.path.join(GS, 'mail_gate24T2c_ready.md')
ORDER = ('1245', '1256', '1257', '1258', '1259', '1260', '1261')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate24T2c.json'), encoding='utf-8'))
if P.get('fail') != 0: die('pins_gate24T2c.json carries fail=%s — predict_gate24T2c.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('pins_gate24T2c.json is a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != sorted(ORDER): die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), list(ORDER)))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate24T2c.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a new READY, a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, the seven heads)' % P['develop'][:9])

SEAT_ITEMS = [
    # #1245
    '65eb964271b0d6895e90fe8f5ffcbbbb9a484050', '7f3989cd-8428-4868-addb-1f3c465699dc', 'S19: a test that logs BOTH a ` Test Files ` line AND a `Tests` line to STDOUT.',
    'load 5.79 (base at develop `6e2a00bfe`: 63 / 1089 / 0)', 'My first E1 applied cleanly and tampered NOTHING', 'anchor on the FIRST ` Test Files ` -> ',
    'cannot see an inline regex creeping back. Neither alone covers the other.', 'alternative in your fix list', 'but it would be round 3, which the cap forbids',
    'A TTY child (ANSI is stripped unconditionally, so it cannot reach the parse)', 'the 15-leg preflight did NOT run; 12 s, format gate only;',
    # #1256
    '5a41ed7fea96ab77ed1dc263ae0c7d25c9846440', '6ad49b00-c50d-464e-bcfd-6675011b57a7', 'T6b double-quoted   -> NEW guard red · OLD guard blind', 'real pre-edit file',
    'it reported ITSELF', '869/869, 74/74 suites', "The guard still scans THIS service's `__tests__` only.",
    # #1257-#1260 (one mail) + L5's declared counts
    'd1db0d41ac52359c231cd22abf11124204645d97', 'ff90fbf9d7e351104404e3eaad505a673e656c1e', '8a2a28f50eb3453db7284da0f098f6a819d40145', '62e69d23b2507780316f1930123c7d57ebba3ae2',
    '8828f8b1-ab10-4a87-b82c-8b72b2a32571', 'a60c002f-f2eb-4055-ae48-145add61769b', '95590d10-4f54-450a-b55e-3b4dbd1c6227', '9698865f-574b-4bf1-848f-23d3cc361977',
    '#1257 ran 0 of 15 legs, by design', '18/0 green, 16/0 + 4 leaked on the base, 14/4 red', 'the errexit DEATH is UNREPRODUCED-ON-THIS-HOST', '#1258: no real PostgreSQL anywhere.',
    '#1259: CASE 6b compares two cwds, not all of them.', '#1257: the cell counts LISTENERS, not processes', '#1258 is tier 2', 'HEAD `3bad652d17cf`',
    'the log is EMPTY', 'RED on the base: 6 passed, 1 failed', 'Base suite run in place LEAKS EXACTLY 4', 'RED, one call site put back inside `$( )`: 14 passed, 4 failed',
    'BASE returns non-zero at 8 of 8, HEAD at 0 of 8', 'My first CASE 6b could not fail.', 'the fleet STOP count does not move',
    # #1261
    'eab8d7031b1b19071a66715ca0aabd9c5cb29c6d', 'c4688275-dab8-47ed-839d-7213ea3acd0d', 'A DNS spy cannot distinguish `:1` from `:2`', 'the static cell refuses a scan finding fewer than 8',
    'The two N arms necessarily redden both cells', '871/871, 75', '`*.integration.test.ts` is NOT scanned', '`import * as dns` yields a namespace whose `lookup` is',
]
KEYWORDS = [
    'THE CAP ROUND', 'SHIPS NOTHING', 'DO NOT grade it', 'END_TREE_NO1245', 'THERE IS NO DECLARED OVERLAP', 'THE RUNNING SIBLING BATCH gate24T2b', 'LIVE-SHAPE',
    'KILLED-AFTER-LOOKALIKE', 'JOINED', 'CALLSITE-STILL-TEXT', 'MUST-CHANGE', 'T-CALL (i)', 'T-CALL (iii)', 'T-CALL (iv)', '(E6)', '(H1)', '(H8b)', '(L4)', '(T-210)', '(T-INCLUDES)',
    'THE READER RULE', 'REVERT-SKIPS', 'NODNS-EGRESS', 'SELF-SCAN', 'BACKTICK', 'NAMED-FACTORY', 'LISTENER-COUNT', 'CASE6B-TWO-CWDS', 'KS1139-CLOSES?',
    'STOP-RECORD-OVERWRITTEN', 'UNREPRODUCED-ON-THIS-HOST', '(K0)', '(K2)', '(M0)', '(W0)', '(A0)', '(A1)', 'arms1293.py', 'arms1159.py', 'tamper1313r2.sh',
    '--no-file-parallelism', '--runInBand', '--json', 'shellcheck', 'NOT INSTALLED', 'KNIP-DELTA', 'TYPECHECK AND LINT DELTA', 'TS2322', 'prettier --check',
    'PACKAGE SUITES, BEFORE / AFTER', 'exits 127', 'the one allowed standalone run', 'NOT-FOUND control', 'NO DOCKER, NO DATABASE', 'LOAD (standing', 'KS-1155',
    'LOGIN_STUB REAPER — YOUR OWN ONLY', 'LEADS for you to grade', 'BY-NAME ITEMS', 'CENSUS v2', 'LINEAR LINK HYGIENE', 'MERGE ADDENDUM', 'MG-1', 'MG-3', 'MG-11',
    'STAYS In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD', 'READ THE WHOLE TEST FILES', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it',
    'Never enter any seat worktree', '.push-lock-24', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value',
    'No memory maintenance', 'Datasec files and mail are out of scope entirely', 'EVIDENCE CLASS', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE',
    'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '2026-09-26-batch1245r2-t2c', 'the merging seat re-predicts',
    'HOLDS (standing)', 'mail_gate24T2c_ready.md', 'COMMISSION.md', 'liveshape_2.out', 'predict_5/6/7.out', '2026-09-26-batch1243-t2a', 'KS-1201', 'STREAM-SEPARATED',
    'PRESUITE-URLPATH', 'COLD CACHE', 'INERT TAMPER', 'GO WITH FINDINGS', 'no `timeout` binary', 'absolute paths only', 'no PIPESTATUS', '${A[@]+"${A[@]}"}',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

rows = []
for n in ORDER:
    pr = P['prs'][n]
    for f in pr['files']:
        rows.append('  #%s %s %s (%s; base %s; merged-blob target over develop: %s)' % (n, f['path'], f['head_blob'], f['mode'], f['parent_blob'][:12],
                    'the head blob' if f['merged_blob'] == f['head_blob'] else 'DIFFERS ' + f['merged_blob']))
SAD = P['stop_at_develop']
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_TREE': P['base_tree'], 'DEVELOP': P['develop'], 'DEVELOP_SHORT': P['develop'][:9],
    'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']), 'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']) or '  (none: develop == BASE)',
    'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'], 'END_TREE_NO1245': P['end_tree_no1245'], 'END_ORDERS': str(P['end_orders']),
    'FILES_TABLE': '\n'.join(rows), 'R2_1245': ', '.join('%s %s' % (k, v) for k, v in sorted(P['r2_1245'].items())),
    'STOP_AT_DEVELOP': '`pre_push_hook_base` 28/0, `fixture_guard` %d/0, `run_shell_suites` %d/0, `shell suites` 60 of 60 (the drafter\'s static cell census of develop %s)' % (SAD['fixture_guard'], SAD['run_shell_suites'], P['develop'][:9]),
    'PREDICT_OUT': 'the newest predict_N.out (pins_gate24T2c.json, measured_at %s)' % P['measured_at'],
    'SEAT_ITEMS': ' \\\n'.join('  ' + sq(w) for w in SEAT_ITEMS), 'KEYWORDS': ' \\\n'.join('  ' + sq(w) for w in KEYWORDS),
    'N_SEAT': str(len(SEAT_ITEMS)), 'N_KW': str(len(KEYWORDS)),
}
for n in ORDER:
    pr = P['prs'][n]
    TOK['MT_' + n] = pr['merged_tree']; TOK['PATHS_' + n] = ','.join(sorted(f['path'] for f in pr['files']))
    TOK['MB_' + n] = pr['compare']['merge_base']; TOK['AH_' + n] = str(pr['compare']['ahead']); TOK['BH_' + n] = str(pr['compare']['behind'])
def fill(text):
    out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: TOK[m.group(1)] if m.group(1) in TOK else die('unknown token ' + m.group(1)), text)
    left = re.findall(r'\{\{[A-Z0-9_]+\}\}', out)
    if left: die('unfilled tokens ' + ' '.join(left))
    return out

prompt = fill(open(os.path.join(GS, 'prompt_gate24T2c.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate24T2c.TEMPLATE.sh.txt'), encoding='utf-8').read())
cap = open(CAPTURE, encoding='utf-8').read()
for n in ORDER:
    if P['prs'][n]['head'] not in cap: die('the capture does not name #%s\'s head %s — run capture_mail_gate24T2c.py first' % (n, P['prs'][n]['head']))
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
print('seat items %d (raw, both files) · keywords %d (joined prompt) · develop %s · END_TREE %s · END_TREE_NO1245 %s · STOP at develop %s' % (len(SEAT_ITEMS), len(KEYWORDS), P['develop'], P['end_tree'], P['end_tree_no1245'], SAD))
sys.exit(0)
