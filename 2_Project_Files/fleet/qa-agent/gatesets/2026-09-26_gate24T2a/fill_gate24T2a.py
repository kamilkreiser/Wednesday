#!/usr/bin/env python3
"""fill_gate24T2a.py — fill the prompt + launcher templates from pins_gate24T2a.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop and the four heads by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate24T2a.py
first, never filled. Pre-checks every seat item (raw grep in BOTH the capture and the filled prompt) and every by-name keyword (in the
whitespace-joined prompt) exactly as the launcher will, and runs `bash -n` on the launcher. Keeps any previous output that differs as
<name>.pre-<HHMMSS>. Writes nothing outside its own directory. Derived from gate21T2d/e's fill scripts, re-keyed to FOUR rows (#1243, #1244, #1245,
#1248 — widened and frozen by Wednesday).
Usage: fill_gate24T2a.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-26_secuura-batch1243-t2.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_batch1243-t2.sh')
CAPTURE = os.path.join(GS, 'mail_gate24T2a_ready.md')
ORDER = ('1243', '1244', '1245', '1248')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate24T2a.json'), encoding='utf-8'))
if P.get('fail') != 0: die('pins_gate24T2a.json carries fail=%s — predict_gate24T2a.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('pins_gate24T2a.json is a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != sorted(ORDER): die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), list(ORDER)))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate24T2a.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a new READY, a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, the four heads)' % P['develop'][:9])

SEAT_ITEMS = [
    # #1243
    '0c89e2b503d9333829c277c50ad3b1a33f03cb96', '2ab6e373-59dc-4788-8a8a-4bb4708a9a4e', '43f16c80-df62-46c1-be52-5c10bc380688',
    'The defect is NOT confined to comments-only files.', "The ticket's second regression cell already passed at base.", '63 files / 1097 passed / 0 failed',
    'B1 + B2 red', 'ONLY B4 red', 'B4 + E2 red', 'the positive control reds', 'the CANARY reds', 'READYAML-SHAPES reds',
    'a routing cell cannot detect its own blindness', '12 seconds', 'KS-1300 item 1 (READYAML-UNGATED) NOT delivered, stays open', 'COMPUTED specifier',
    # #1244
    '146b620fda53f008b3384334a474b06a16235af3', '2d8faa53-3024-45d5-9833-60c00e566368', 'anchored only for KEY', 'GREEN before the fix',
    '63 files / 1096 passed / 0 failed', 'L02, L03, L08 red', 'exactly L02, L03, L08', 'T-6 exists because I was wrong about T-4',
    'The masked NAME SET is unchanged', 'QA-961-3 is documented, not fixed', '7 seconds',
    # #1245
    '1700b5ae7dd56ad3e30602a40b20ae6469c35350', 'e52d59f5-7dce-49fd-8237-fdeef3c7621d', '`expected fail` is a TWO-WORD label',
    'The renderer EXCLUDES `expected fail` from `passed`', '`tsconfig.json` EXCLUDES `tests`', '63 files / 1107 passed / 0 failed',
    'T-1 require a `passed` segment (the defect)', 'T-2 take the FIRST `Tests` line', 'T-5 reddened NOTHING on its first run',
    'T-6 the call site stops calling `readSuiteCounts`', 'the ":156 citations"', 'if #1241 is ever revived it rebases onto #1245',
    'That is four tier-2 READYs by your launch count',
    # #1248
    '2b4960172644b5ef0414b94d46d11974012c2007', 'bac4c257-ca17-48d5-b4d2-a5b4b6000d14', 'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
    '28 passed, 0 failed', '6 passed, 0 failed', '60 passed, 0 failed, 0 skipped (of 60)', 'I amended the commit message before pushing.',
    'A1 run FIRST, on your instruction', 'W8 only', 'A3 reds three cells here, not two.', 'resolves only from the workspace-root lockfile',
    'the pre-existing `no-control-regex` at `:539`',
]
KEYWORDS = [
    'TIER 2: THROUGH-CODE', 'THROUGH-CODE REVIEW', "RED-PROOF CHECK OF THE PR'S OWN PROOF", 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY',
    'A red proof must NAME WHY it went red', 'FINDINGS ONLY', 'A VERDICT IS VALID ONLY AT ITS HEAD', 'State the FAIL condition before each run',
    'One verdict PER PR', 'WIDENED to four', 'DO NOT GRADE #1241.', 'ROUND 1 OF 2', 'THIRD attempt', 'KS-1144', 'ORIGIN ROUNDS',
    '2026-09-25-batch1241-t2d', '2026-09-25-batch1241-t2e', '2026-09-25-batch1218-t2c', '2026-09-12-ks1098-961-644965d90-tier2-r1',
    '2026-09-13-ks828-900-981-04807ea0e-tier2-r1', 'T2C-ROUTING-HOME', 'RE-READ develop at your start', 'answer_seatB25_movedbase', 'THERE IS NO DECLARED OVERLAP',
    'PAIRWISE PATH-DISJOINT', 'DIRECTORY-level', 'merged-blob target', 'all 24 merge orders', 'a40cb9eea049', 'EXPORTED', 'utils.BS4fH3nR.js',
    'LAST-MATCH-STDERR', 'LIVE-SHAPE (MANDATORY', '(L1) CAPTURE', '(L2) THROUGH THE REAL FUNCTION', '(L3) THROUGH childSuiteCounts() ITSELF', '(L4) BYTE FOR BYTE',
    '(S1) fail-only', '(S2) skip-only', '(S3) todo-only', '(S4) expected-fail+pass', '(S5) fail+pass+skip', '(S6) pass-only', '(S7) a MULTI-FILE summary',
    '(S12) a `beforeAll` that throws', '(S15) no tests', '(S16)', '(S17)', '(S18) NO console output', '(E5)', 'THE RULE', 'od -c', 'cat -v', 'GATE-PROBE',
    'fixturesSlot.test.ts', 'echoline.out', '--reporter=default', '(R-D)', '(T-103)', '(T-FIRST)', '(T-NOSUM)', '(T-DUPOK)', '(T-CALL)', '(R-E)', 'CALLSITE-SCRAPE',
    'SYMMETRIC-FIXTURE', '(A-0)', '(A-1)', '(A-2)', '(K-1)', '(K-2)', '(K-3)', '(K-4)', 'MULTILINE-IMPORT', 'CANARY-IN-PACKAGE', '.ks1300-canary-',
    '(M-0)', '(T-1)', '(T-6)', '(T-5)', 'UNROWED-SIBLINGS', '(T-2) loosen the continuation filter', '(A-3)', '(A-4)', 'REAL-TREE-DELTA', 'CONT-DEFERRED',
    'DISCLOSED-LIMIT', 'PACKAGE SUITES, BEFORE / AFTER', '--no-file-parallelism', 'PRESUITE-URLPATH', 'slotGateEntrypoints.test.ts', '1122', '928 -> 930',
    'exits 127', 'TYPECHECK AND LINT DELTA', 'tsconfig.node.json', '--listFilesOnly', 'TS2322', 'prettier --check', 'KNIP-DELTA',
    'THE FLEET STOP COUNT: CLAIMABLE ONLY FOR #1248, BY READ', 'NOT-FOUND control', 'NO DOCKER, NO DATABASE', 'LOAD (standing', 'KS-1155',
    'LOGIN_STUB REAPER — YOUR OWN ONLY', 'LEADS for you to grade', 'STALE / LONG TITLES', 'THE ENVIRONMENT GAP', 'BY-NAME ITEMS', 'CENSUS v2',
    'LINEAR LINK HYGIENE', 'MERGE ADDENDUM', 'MG-1', 'MG-3', 'MG-11', 'STAYS In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD',
    'READ THE WHOLE TEST FILES', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree', '.push-lock-24',
    'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value', 'No memory maintenance',
    'Datasec files and mail are out of scope entirely', 'EVIDENCE CLASS', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE', 'WRITE report.md BEFORE THE MAIL',
    'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '2026-09-26-batch1243-t2a', 'the merging seat re-predicts', 'HOLDS (standing)',
    'mail_gate24T2a_ready.md', 'COMMISSION.md', 'liveshape_lift_2.out',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

rows = []
for n in ORDER:
    pr = P['prs'][n]
    for f in pr['files']:
        rows.append('  #%s %s %s (%s; BASE %s; merged-blob target over %s: %s)' % (n, f['path'], f['head_blob'], f['mode'], f['base_blob'][:12],
                    P['develop'][:9], 'the head blob' if f['merged_blob'] == f['head_blob'] else 'DIFFERS ' + f['merged_blob']))
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_TREE': P['base_tree'], 'DEVELOP': P['develop'],
    'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']), 'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']) or '  (none: develop == BASE)',
    'MOVE_PATHS': str(P['move_paths']), 'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'], 'FILES_TABLE': '\n'.join(rows),
    'PREDICT_OUT': 'the newest predict_N.out (pins_gate24T2a.json, measured_at %s)' % P['measured_at'],
    'HEAD_BLOB_1245': P['prs']['1245']['files'][0]['head_blob'],
    'SEAT_ITEMS': ' \\\n'.join('  ' + sq(w) for w in SEAT_ITEMS), 'KEYWORDS': ' \\\n'.join('  ' + sq(w) for w in KEYWORDS),
    'N_SEAT': str(len(SEAT_ITEMS)), 'N_KW': str(len(KEYWORDS)),
}
for n in ORDER:
    TOK['MT_' + n] = P['prs'][n]['merged_tree']
    TOK['PATHS_' + n] = ','.join(sorted(f['path'] for f in P['prs'][n]['files']))
def fill(text):
    out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: TOK[m.group(1)] if m.group(1) in TOK else die('unknown token ' + m.group(1)), text)
    left = re.findall(r'\{\{[A-Z0-9_]+\}\}', out)
    if left: die('unfilled tokens ' + ' '.join(left))
    return out

prompt = fill(open(os.path.join(GS, 'prompt_gate24T2a.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate24T2a.TEMPLATE.sh.txt'), encoding='utf-8').read())
cap = open(CAPTURE, encoding='utf-8').read()
for n in ORDER:
    if P['prs'][n]['head'] not in cap: die('the capture does not name #%s\'s head %s — run capture_mail_gate24T2a.py first' % (n, P['prs'][n]['head']))
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
