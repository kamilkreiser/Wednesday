#!/usr/bin/env python3
"""fill_gate24T2d.py — fill the prompt + launcher templates from pins_gate24T2d.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop and the three heads by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate24T2d.py
first, never filled. Pre-checks every seat item (raw, per LINE, in BOTH the capture and the filled prompt — the launcher's grep is line-based) and
every by-name keyword (in the whitespace-joined prompt) exactly as the launcher will, and runs `bash -n` on the launcher. Keeps any previous output
that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory. Derived from gate24T2b's fill script, re-keyed to SEVEN rows, no stack.
Usage: fill_gate24T2d.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-26_secuura-batch1250r2-t2.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_batch1250r2-t2.sh')
CAPTURE = os.path.join(GS, 'mail_gate24T2d_ready.md')
ORDER = ('1250', '1253', '1262', '1263', '1264', '1265', '1266')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate24T2d.json'), encoding='utf-8'))
if P.get('fail') != 0: die('pins_gate24T2d.json carries fail=%s — predict_gate24T2d.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('pins_gate24T2d.json is a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != sorted(ORDER): die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), list(ORDER)))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate24T2d.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a new READY, a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, the seven heads)' % P['develop'][:9])

SEAT_ITEMS = [
    'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
    # #1250 round 2 (READY by id)
    '2b8dcb824dd2c5cd4b92757934d7de9d28813a22', 'c2637fc1-12ef-47a8-a6e2-a878cc609623', 'ec78da20-166f-4de8-b9df-420c210f5503',
    '(INT installable=no, TERM installable=yes)', '56 passed, 2 failed', 'rc=0 suites_started=2 verdict_lines=1', 'rc=1 suites_started=2 verdict_lines=1',
    'bash discards INT in a background job', 'My round 2 prints 0 such lines in either green run', 'N-1250-b TIMING-CELL is unfixed',
    'The PTY route is owed as its own ticket.',
    # #1253 round 2 (PR body; no READY id)
    '91e066264004fdb22c67efb0c25fc44375ec6eac', '10 → 12 cells; green 12/0', 'both ABORT, so they are not the swallowing class',
    'It does NOT catch a `(` several lines', 'fire on the measurably-safe `|| true` shape', 'if bf; then :; fi', 'bf && :',
    # #1262 (READY by id)
    '3b319485d1e3a58f30e4190a7898d7562cb80c3b', '80657a5b-df4e-4f3c-8f3a-ecafa1e818b4', 'aeb1d404-3918-4e02-bd2e-7ef4251b7d3e', 'Expected: 0, Received: 1',
    'the cell REFUSES unless the connection is `127.0.0.1` on 55410-55419.', 'is MOCKED for this whole file', '7 passed / 7 at head',
    'MODE F (Prisma branch of withTenant) NOT RUN',
    # #1263 (READY by id; the round-25 widen)
    '3c33f936fe3985ab40b72b78bda15a6959448e18', '74ebba0d', 'All 31 changed lines in `git diff -U0` are comment lines', 'pre and post emit byte-identical at **10,805 bytes**',
    '941/941 bare -> 941/941 patched', '1,429 / 14,178,318 B', 'No new assertion.',
    # #1264 (READY by id; the second round-25 widen)
    '2e95121dfc475a09c81d61d61f9a81148b6bb0b9', 'develop vs head: **EQUIVALENT**, emit 6490 vs 6490 bytes, 0 diagnostics either side.', 'bare 129/129 -> patched 129/129',
    # #1265 and #1266 (PR bodies; no READY id)
    '87ef6a1b088754ab773f541ddb273acce8dfab4f', '1104/1104 bare → 1108/1108 patched', '952f4329de97cd7f94ab6363e670248c456d0a54', '129/129 at develop',
    # Wednesday's RULING (a)
    'An UNREACHABLE is a measurement, never a skip', 'INT-to-pid: nowhere, bash rule 2',
]
KEYWORDS = [
    'ROUND 2 OF 2', 'THE CAP', 'INT-PID-CONSTANT', 'RULE2-UNDER-SETM', 'RUNNER-MASKS-INT', 'BG-STDIN', 'ORPHAN-ON-SIGNAL', 'LATENCY-UNPINNED', 'TIMING-CELL',
    'SAFE-SHAPES-FLAGGED', 'CMDSUB-MULTILINE', 'OPENER-WITH-CONTENT', 'STALE-CONTROL', 'OWNER-UNASSERTED-AT-BASE', 'REFUSAL-SCOPE', 'LOCALHOST-ALSO',
    'MODE-F-NOT-RUN', 'THE READER RULE', '(R-A)', '(R-B)', '(R-C)', '(R-D)', '(R-E)', '(R-F)', '(R-G)', '(R-1)', '(R-2)', '(G0)', '(G1)', '(G2)', '(G3)',
    '(G4)', '(I-H)', '(I-B)', '(I-O)', '(I-T0)', '(I-R)', '(I-C)', 'RUNNER_SH', 'SUBJ_SH', 'set -m', '--runInBand', 'jest.integration.config.js',
    'shellcheck', 'TYPECHECK AND LINT DELTA', 'TS2322', 'prettier --check', 'exits 127', 'the one allowed standalone run', 'NOT-FOUND control',
    'LOAD (standing', 'KS-1155', 'LOGIN_STUB REAPER — YOUR OWN ONLY', 'LEADS for you to grade', 'BY-NAME ITEMS', 'CENSUS v2', 'LINEAR LINK HYGIENE',
    'MERGE ADDENDUM', 'MG-1', 'MG-3', 'MG-11', 'STAYS In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD', 'READ THE WHOLE TEST FILES',
    'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree', 'RESTORE DISK MODES FROM THE INDEX',
    'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value', 'No memory maintenance', 'Datasec files and mail are out of scope entirely',
    'EVIDENCE CLASS', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to',
    'wednesday-agent@agentmail.to', '2026-09-26-batch1250r2-t2d', 'the merging seat re-predicts', 'HOLDS (standing)', 'mail_gate24T2d_ready.md',
    'COMMISSION.md', 'trapprobe_1.out', 'maskprobe_1.out', 'readerprobe_1.out', '2026-09-26-batch1249-t2b', 'never removed', 'KS-1201',
    'STREAM-SEPARATED', 'PRESUITE-URLPATH', 'COLD CACHE', 'GO WITH FINDINGS', 'RESIDUE TO TICKET', '127.0.0.1:55419', '0ec12181dd37', '0187e1998e06',
    'THE TIMING CELL', 'N-1250-b', 'MAGIC-WORD-CLOSES', 'CENSUS-CLAIM', '(T3-a)', '(T3-b)', '(T3-c)', '(T3-d)', '(T3-e)', 'transpileModule', 'removeComments', 'KS879CENSUS', 'STALEAUTOCREATE', 'UNROWEDSIBLINGS', 'PRESENTATIONPINS', 'LABEL-SHAPE', '(K-1)', '(K-2)', '(K-3)', '(K-4)', '(P-1)', '(P-2)', '(P-3)', 'tamper_ks1120.py', 'COMMENT-CLAIMS', 'TIER-3 PROOF FOR #1263 AND #1264',
    'no `cd` in a shared command line', "perl -e 'alarm N; exec @ARGV'", 'nothing deleted (quarantine)', 'never edit a script while it runs',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

rows = []
for n in ORDER:
    pr = P['prs'][n]
    for f in pr['files']:
        rows.append('  #%s %s %s (%s; parent %s%s; merged-blob target over develop %s: %s)' % (n, f['path'], f['head_blob'], f['mode'], f['parent_blob'][:12],
                    '; round 1 %s' % f['round1_blob'][:12] if f.get('round1_blob') else '', P['develop'][:9], 'the head blob' if f['merged_blob'] == f['head_blob'] else 'DIFFERS ' + f['merged_blob']))
def label(k):
    ins = k.split('+'); held = [n for n in ORDER if n not in ins]
    return 'all seven (END_TREE)' if not held else '%s (held: %s)' % (' + '.join('#' + n for n in ins), ' '.join('#' + n for n in held))
LABEL = {k: label(k) for k in P['subsets']}
subs = ['  develop + %-52s %s (%d order(s); `%s`)' % (LABEL[k], v['tree'], v['orders'], v['shortstat']) for k, v in sorted(P['subsets'].items(), key=lambda kv: -len(kv[0]))]
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_TREE': P['base_tree'], 'DEVELOP': P['develop'],
    'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']), 'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']) or '  (none: develop == BASE)',
    'END_ORDERS': str(P['subsets']['+'.join(sorted(ORDER))]['orders']), 'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'], 'FILES_TABLE': '\n'.join(rows), 'SUBSETS_TABLE': '\n'.join(subs), 'RED62': P['red62'],
    'PREDICT_OUT': 'the newest predict_N.out (pins_gate24T2d.json, measured_at %s)' % P['measured_at'],
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

prompt = fill(open(os.path.join(GS, 'prompt_gate24T2d.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate24T2d.TEMPLATE.sh.txt'), encoding='utf-8').read())
cap = open(CAPTURE, encoding='utf-8').read()
for n in ORDER:
    if P['prs'][n]['head'] not in cap: die('the capture does not name #%s\'s head %s — run capture_mail_gate24T2d.py first' % (n, P['prs'][n]['head']))
joined = re.sub(r'\n\s*', ' ', prompt)
online = lambda w, t: any(w in l for l in t.split('\n'))
miss = [w for w in SEAT_ITEMS if not online(w, prompt) or not online(w, cap)]
if miss: die('seat items not on ONE LINE in BOTH the capture and the prompt: %s' % [(w, online(w, cap), online(w, prompt)) for w in miss])
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
print('seat items %d (per line, both files) · keywords %d (joined prompt) · develop %s · END_TREE %s · red base %s' % (len(SEAT_ITEMS), len(KEYWORDS), P['develop'], P['end_tree'], P['red62']))
sys.exit(0)
