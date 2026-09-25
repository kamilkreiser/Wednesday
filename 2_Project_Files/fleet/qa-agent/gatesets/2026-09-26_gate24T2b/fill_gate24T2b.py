#!/usr/bin/env python3
"""fill_gate24T2b.py — fill the prompt + launcher templates from pins_gate24T2b.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home: every
path in the outputs is that directory). Re-reads origin develop, the seven heads and #1248's head (the stack base) by `git ls-remote` (READ verb,
from the Secuura checkout) and REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is
re-measured with predict_gate24T2b.py first, never filled. Pre-checks every seat item (raw grep in BOTH the capture and the filled prompt) and every
by-name keyword (in the whitespace-joined prompt) exactly as the launcher will, and runs `bash -n` on the launcher. Keeps any previous output that
differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory. Derived from gate24T2a's fill script, re-keyed to SEVEN rows + the stack.
Usage: fill_gate24T2b.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil

GS = os.path.dirname(os.path.abspath(__file__))
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, '2026-09-26_secuura-batch1249-t2.prompt.txt')
LAUNCH_OUT = os.path.join(GS, 'launch_qa_secuura_batch1249-t2.sh')
CAPTURE = os.path.join(GS, 'mail_gate24T2b_ready.md')
ORDER = ('1249', '1250', '1251', '1252', '1253', '1254', '1255')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def die(m):
    print('REFUSING: ' + m); sys.exit(1)

P = json.load(open(os.path.join(GS, 'pins_gate24T2b.json'), encoding='utf-8'))
if P.get('fail') != 0: die('pins_gate24T2b.json carries fail=%s — predict_gate24T2b.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('pins_gate24T2b.json is a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != sorted(ORDER): die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), list(ORDER)))
refs = ['refs/heads/develop', 'refs/pull/1248/head'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']:
    die('origin develop %s != pinned %s — run predict_gate24T2b.py first' % (L.get('refs/heads/develop'), P['develop']))
if L.get('refs/pull/1248/head') != P['h1248']: die('#1248 (the stack base) moved: %s != %s — #1249 needs a new READY and a re-draft' % (L.get('refs/pull/1248/head'), P['h1248']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a new READY, a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
print('fill at', now(), '| home', GS, '| origin agrees with the pins (develop %s, the seven heads, #1248 %s)' % (P['develop'][:9], P['h1248'][:9]))

SEAT_ITEMS = [
    'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
    # #1249
    '6eb283d058184f1f0fabdc3c3184a817db4fb94b', 'ffa40d2b-87d7-479c-a472-69a75dcdc05b', 'The equality target for #1249 is the MERGED blob',
    'Replacing that Set with an array', '1 failed / 237 passed', 'Arm B1 disables the walk. It reds the four new controls and does NOT red J2.',
    '47 files / 934 passed / 0 failed', '930 → 934', 'B2 `Set` -> array in `addExport`', "B4 J2's own expectation flipped -> J2",
    # #1250
    'c78f4093fb531bceb94a8e9defb59350d8c60b73', 'ededa074-38a9-4885-849f-497ea9216637', 'a168426c-6686-4661-be83-7930c44f256c', '52 passed, 3 failed',
    'The other 49 pre-existing cells are byte-identical between the two runs.', 'PASSED against the unfixed runner.',
    'The `INT`/`TERM` arms of the trap are NOT exercised by a cell', 'The trap lists them; that much is unverified.',
    'The 16 pre-existing `/tmp/rss.*` directories are NOT cleaned up.',
    # #1251
    '8020adae99129f4b7194fef32f1ea5b762819d90', 'c3bee428-c57d-4090-a060-3850222ace30', 'reddened NOTHING — 25/25.',
    'stop checking the ADDRESS -> the wrong-host control', 'host check never matches -> 6 cells', 'Nothing on develop trips this today',
    # #1252
    'ca7337fa04e04e5438bc79a5abe215424fcb33ef', '82e55642-18d7-4eb0-8484-2cbb537ed8c1', '4eb28af2-b6d5-440f-94d6-1e88d22fea55', '1 failed / 11 passed',
    'B2 the registry read matches nothing -> EXCLUSIONHOLDS reds', '870 passed / 870, 74/74 suites', 'it also passed on the base BEFORE I edited',
    'leg 8 is the served-spec-vs-yaml check', '`generate-openapi --check` covers source-vs-disk, NOT served-vs-disk.', "No cell pins KS-1299's wording.",
    # #1253
    '6b88e4f03e82e3da0672efb1bb757ba5da912d6a', 'eb1cc744-c3bd-4ca0-8934-1b10006cff09', 'this worktree carries the base runner', 'anchors reverted in a copy',
    '`repo_state` un-widened in a copy', 'one call site wrapped in a subshell', "Cell 7's first draft could not fail.",
    'NB-1218-c is pinned STATICALLY, not behaviourally.', 'The 12-of-12 call-site census covers `pre_push_hook_base.test.sh` only.',
    # #1254
    'da0c94968a7423c340b3a3b76244bda536d1f6d2', '1b79094b-7578-4063-9f4a-ebd9cc204d42', 'Then I removed `setupFiles` from the config',
    'TWO TAMPER ARMS DID NOT APPLY AND PRINTED A CLEAN PASS', '48 files / 933 passed / 0 failed', "Tonight's load was", '4.8-9.2',
    'D6 remove the wiring -> the wiring pin', 'Both audit rows lapse `2026-09-30T00:00Z`',
    # #1255
    '59245ff0b11c6b760ba5e2a9daedc5927e915e10', '2f9b93a6-d32e-4dc2-87c8-ceeb86ba3564', 'arm: truthiness at :2663 (/sign-cert)',
    'arm: truthiness at :2932 (/sign-wallet)', 'That line carries the TEST name only', '877/877, 74/74 suites', 'untampered re-run 122/122',
]
KEYWORDS = [
    'STACKED', 'DO NOT GRADE #1248.', 'develop + #1248', 'END_TREE_NOSTACK', 'THE ONE DECLARED OVERLAP', 'TRAP-SWALLOWS-TERM', 'TIMING-CELL',
    'TRAILING-PIPE', 'THE READER RULE', 'LENGTH-ONLY', 'ESCAPE-MISMATCH', 'LEG-8-PORT', 'SUBSTRING-VERB', 'NESTED', 'DERIVE-MARKERS', 'BUDGET-LEAK',
    'ROUTE-ISOLATION', 'STOP-RECORD-OVERWRITTEN', 'CALLSITE-SCRAPE', '(B1)', '(B2)', '(B3)', '(B4)', '(R-0)', '(R-1)', '(R-2)', '(R-3)', '(C0)',
    '(V0)', '(G0)', '(P0)', 'D1-D6', '--no-file-parallelism', '--runInBand', 'spec-endpoint-consistency.mjs', 'summarise', 'shellcheck',
    'TYPECHECK AND LINT DELTA', 'TS2322', 'prettier --check', 'PACKAGE SUITES, BEFORE / AFTER', 'exits 127', '48 files / 941', '878',
    'the one allowed standalone run', 'NOT-FOUND control', 'NO DOCKER, NO DATABASE', 'LOAD (standing', 'KS-1155', 'LOGIN_STUB REAPER — YOUR OWN ONLY',
    'LEADS for you to grade', 'STALE / LONG TITLES', 'BY-NAME ITEMS', 'CENSUS v2', 'LINEAR LINK HYGIENE', 'MERGE ADDENDUM', 'MG-1', 'MG-3', 'MG-11',
    'STAYS In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD', 'READ THE WHOLE TEST FILES', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN',
    'NEVER a fetch into it', 'Never enter any seat worktree', '.push-lock-24', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID',
    'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value', 'No memory maintenance', 'Datasec files and mail are out of scope entirely',
    'EVIDENCE CLASS', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to',
    'wednesday-agent@agentmail.to', '2026-09-26-batch1249-t2b', 'the merging seat re-predicts', 'HOLDS (standing)', 'mail_gate24T2b_ready.md',
    'COMMISSION.md', 'trapprobe_1.out', 'predict_3.out', '2026-09-26-batch1243-t2a', 'never remove', 'KS-1201',
    'STREAM-SEPARATED', 'PRESUITE-URLPATH', 'COLD CACHE', 'GO WITH FINDINGS', 'BOTH STATES ARE LEGAL',
]

def sq(s):  # a bash single-quoted word
    return "'" + s.replace("'", "'\"'\"'") + "'"

rows = []
for n in ORDER:
    pr = P['prs'][n]
    for f in pr['files']:
        rows.append('  #%s %s %s (%s; parent %s; merged-blob target over its grading base %s: %s)' % (n, f['path'], f['head_blob'], f['mode'], f['parent_blob'][:12],
                    pr['grading_base'][:9], 'the head blob' if f['merged_blob'] == f['head_blob'] else 'DIFFERS ' + f['merged_blob']))
TOK = {
    'GS': GS, 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'BASE': P['base'], 'BASE_TREE': P['base_tree'], 'DEVELOP': P['develop'],
    'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind']), 'MOVE_LOG': '\n'.join('  ' + l for l in P['move_log']) or '  (none: develop == BASE)',
    'END_TREE': P['end_tree'], 'END_SHORTSTAT': P['end_shortstat'], 'END_TREE_NOSTACK': P['end_tree_nostack'], 'END_ORDERS': str(P['end_orders']),
    'FILES_TABLE': '\n'.join(rows), 'H1248': P['h1248'], 'STACK_MODE': P['stack_mode'], 'DEV48_TREE': P['dev48_tree'],
    'R1249_ALONE': P['r1249_alone']['numstat'], 'DEDICATED': ', '.join(P.get('k1252', {}).get('dedicated', [])) or 'UNREAD',
    'GUARD_LINES': ':' + ' :'.join(str(x) for x in P['k1255']['guard_lines']),
    'PREDICT_OUT': 'the newest predict_N.out (pins_gate24T2b.json, measured_at %s)' % P['measured_at'],
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

prompt = fill(open(os.path.join(GS, 'prompt_gate24T2b.TEMPLATE.txt'), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_gate24T2b.TEMPLATE.sh.txt'), encoding='utf-8').read())
cap = open(CAPTURE, encoding='utf-8').read()
for n in ORDER:
    if P['prs'][n]['head'] not in cap: die('the capture does not name #%s\'s head %s — run capture_mail_gate24T2b.py first' % (n, P['prs'][n]['head']))
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
print('seat items %d (raw, both files) · keywords %d (joined prompt) · develop %s · stack %s · END_TREE %s · END_TREE_NOSTACK %s' % (len(SEAT_ITEMS), len(KEYWORDS), P['develop'], P['stack_mode'], P['end_tree'], P['end_tree_nostack']))
sys.exit(0)
