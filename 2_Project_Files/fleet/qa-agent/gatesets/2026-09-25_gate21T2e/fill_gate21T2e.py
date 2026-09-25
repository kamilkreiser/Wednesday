#!/usr/bin/env python3
"""fill_gate21T2e.py — fill the prompt + launcher templates from pins_gate21T2e.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop and the head by `git ls-remote` (READ verb, from the Secuura checkout) and REFUSES
(rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate21T2e.py first, never
filled. Pre-checks every seat item (raw grep in BOTH the capture and the filled prompt) and every by-name keyword (in the whitespace-joined prompt)
exactly as the launcher will, and runs `bash -n` on the launcher. Keeps any previous output that differs as <name>.pre-<HHMMSS>. Writes nothing
outside its own directory. Derived from gate21T2d's fill_gate21T2d.py, re-keyed to ONE row (#1241 round 2).
Usage: fill_gate21T2e.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-25_secuura-1241-r2-t2.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_1241-r2-t2.sh')
CAPTURE = os.path.join(GS, 'mail_gate21T2e_ready.md')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate21T2e.json'), encoding='utf-8'))
if P.get('fail') != 0: die('pins_gate21T2e.json carries fail=%s — predict_gate21T2e.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('pins_gate21T2e.json is a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
pr = P['pr']
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin', 'refs/heads/develop', 'refs/pull/1241/head', pr['branch']], capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate21T2e.py first' % (L.get('refs/heads/develop'), P['develop']))
if not (L.get('refs/pull/1241/head') == L.get(pr['branch']) == pr['head']):
    die('#1241 head moved: pull %s, branch %s, pinned %s — a new head needs a new READY, a re-capture and a re-draft' % (L.get('refs/pull/1241/head'), L.get(pr['branch']), pr['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, the head)' % P['develop'][:9])

SEAT_ITEMS = [
    'b4427d416592b40eb5ddb8727b2d6c31f3c7d067', 'e2d0518df402', '12e840dc-9775-4267-bd00-5b07ff4f43ee',
    '`passed` emitted unconditionally', 'two-word label', 'read by segment NAME, not position', '5 cells RED', '4 cells RED',
    'Restored byte-identical both times', '10/10 green', 'Full file 13/13', '`childSuiteCounts` reads LIVE',
    'binding, and tampering it reds them', 'Package unit suite 1095/1095', '`tsc --noEmit -p tsconfig.json` clean',
    'Your N-1 and N-2 findings are', 'the 15-leg preflight DID NOT RUN on this push', '6 seconds', 'KS-1306', 'KS-1307', 'KS-1308',
    'KS-1309', 'There is no N-4', '3bad652d17cf', 'shared store delta 0', 'still In Progress', 'getStateString',
]
KEYWORDS = [
    'TIER 2: THROUGH-CODE', 'THROUGH-CODE REVIEW', "RED-PROOF CHECK OF THE PR'S OWN PROOF", 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY',
    'A red proof must NAME WHY it went red', 'FINDINGS ONLY', 'A VERDICT IS VALID ONLY AT ITS HEAD', 'State the FAIL condition before each run',
    'ROUND 2 OF 2 — THE CAP', 'SHIPS NOTHING and TICKETS THE RESIDUE', 'RESIDUE TICKET', 'is a DECISION and OUT of scope', 'ORIGIN ROUNDS',
    '2026-09-25-batch1241-t2d', 'B-1 LIVE-SKIP-SHAPE', 'N-1 SUMMARY-READ-103', 'N-2 SELFREAD-SHAPE', '2026-09-17-ks1211-1030-e43af4934-tier2-r1',
    'RE-READ develop at your start', 'answer_seatB25_movedbase', 'THERE IS NO DECLARED OVERLAP', 'FAST-FORWARD', 'e68e2f0e837df86da527d775a3a49c631b0f5b17',
    'module-private', 'NOT exported', 'index.UpGiHP7g.js', 'utils.BS4fH3nR.js', 'SummaryReporter', 'if (!this.isTTY) this.options.summary = false;',
    'CONDITIONAL', 'LIVE-SHAPE (MANDATORY', '(L1) CAPTURE', '(L2) THROUGH THE REAL FUNCTION', '(L3) THROUGH childSuiteCounts() ITSELF', '(L4) BYTE FOR BYTE',
    '(S1) skip+fail+pass', '(S2) skip+pass', '(S3) todo+pass', '(S4) expected-fail+pass', '(S5) pass-only', '(S6) fail-only', '(S7) a MULTI-FILE summary',
    '(S8) skip-only', '(S9) todo-only', '(S10) orientation', 'it.skip', 'it.todo', 'it.fails', '--reporter=default', 'cat -v', 'GATE-PROBE',
    'fixturesSlot.test.ts', '(E1)', '(E4)', 'THE RULE', 'od -c', '(R-A)', '(R-D)', '(R-B)', '(R-C) T-CALL', '(R-E)', 'T-103', 'Tamper :93 ALONE',
    'PACKAGE SUITE, BEFORE / AFTER', '--no-file-parallelism', 'PRESUITE-URLPATH', 'slotGateEntrypoints.test.ts', '1095', '1099',
    'PER-FILE TYPECHECK DELTA 0', 'TS2322', 'prettier --check', 'THE FLEET STOP COUNT: NOT CLAIMABLE FOR #1241', 'NO DOCKER, NO DATABASE',
    'LOAD (standing', 'KS-1155', 'LOGIN_STUB REAPER — YOUR OWN ONLY', 'LEADS for you to grade', 'THE RENDERER', 'CALLSITE', 'SYMMETRIC-FIXTURE',
    'FIRST-MATCH', 'STALE-BODY', 'CAPTURE-PROVENANCE', 'LIVE-SHAPE-FAILONLY', 'report.md:188', 'INTEGRATION-UNWIRED', 'BY-NAME ITEMS', 'TIER AND ROUND',
    'CENSUS v2', 'LINEAR LINK HYGIENE', 'MERGE ADDENDUM', 'MG-1', 'MG-3', 'MG-11', 'STAYS In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD',
    'READ THE WHOLE TEST FILE', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree',
    '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value',
    'No memory maintenance', 'Datasec files and mail are out of scope entirely', 'EVIDENCE CLASS', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE',
    'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '2026-09-25-batch1241-t2e', '2026-09-25-batch1218-t2c',
    'the merging seat re-predicts', 'HOLDS (standing)', 'mail_gate21T2e_ready.md', 'COMMISSION.md',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

FILES_TABLE = '#1241 %s %s (%s; round-1 head %s; BASE and develop %s; merged over %s: %s)' % (
    pr['path'], pr['head_blob'], pr['mode'], pr['r1_blob'][:12], pr['base_blob'][:12], P['develop'][:9],
    'the head blob' if pr['merged_blob'] == pr['head_blob'] else 'DIFFERS ' + pr['merged_blob'])
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_TREE': P['base_tree'], 'DEVELOP': P['develop'],
    'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']), 'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']),
    'MOVE_PATHS': str(P['move_paths']), 'SINCE_R1': '; '.join(P['since_r1']) or 'NOTHING', 'PERF_SINCE': ', '.join(P['perf_since_r1']) or 'NONE',
    'MT': pr['merged_tree'], 'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'], 'FILES_TABLE': FILES_TABLE, 'HEAD_BLOB': pr['head_blob'],
    'PREDICT_OUT': 'the newest predict_N.out (pins_gate21T2e.json, measured_at %s)' % P['measured_at'], 'PATHS_1241': pr['path'],
    'SEAT_ITEMS': ' \\\n'.join('  ' + sq(w) for w in SEAT_ITEMS), 'KEYWORDS': ' \\\n'.join('  ' + sq(w) for w in KEYWORDS),
    'N_SEAT': str(len(SEAT_ITEMS)), 'N_KW': str(len(KEYWORDS)),
}
def fill(text):
    out = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: TOK[m.group(1)] if m.group(1) in TOK else die('unknown token ' + m.group(1)), text)
    left = re.findall(r'\{\{[A-Z0-9_]+\}\}', out)
    if left: die('unfilled tokens ' + ' '.join(left))
    return out

prompt = fill(open(os.path.join(GS, 'prompt_gate21T2e.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate21T2e.TEMPLATE.sh.txt'), encoding='utf-8').read())
cap = open(CAPTURE, encoding='utf-8').read()
if pr['head'] not in cap: die('the capture does not name the head %s — run capture_mail_gate21T2e.py first' % pr['head'])
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
