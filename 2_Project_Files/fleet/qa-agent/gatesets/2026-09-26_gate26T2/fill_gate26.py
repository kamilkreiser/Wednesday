#!/usr/bin/env python3
"""fill_gate26.py — fill ONE gate26 kit's prompt + launcher templates from pins_<kit>.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home:
every path in the outputs is that directory). Re-reads origin develop and every head by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate26.py
first, never filled. Pre-checks every seat item (raw, per LINE, in BOTH the capture and the filled prompt — the launcher's grep is line-based), every
by-name keyword and every kit-rule phrase (in the whitespace-joined prompt) exactly as the launcher will, runs the round's KEY SCANNER over every
MANDATED squash text block of the prompt (a block may carry no hyphenated KS key but its own PR's), and runs `bash -n` on the launcher. Keeps any
previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
Shape copied from gate25's fill_gate25.py; re-keyed to N rows, per-PR merge-bases and the key scan.
Usage: fill_gate26.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil
GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
KIT = K['kit']
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, K['prompt']); LAUNCH_OUT = os.path.join(GS, K['launcher'])
CAPTURE = os.path.join(GS, 'mail_%s_ready.md' % KIT)
ORDER = sorted(K['prs'])
WORDS = {4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight'}
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def die(m): print('REFUSING: ' + m); sys.exit(1)
P = json.load(open(os.path.join(GS, 'pins_%s.json' % KIT), encoding='utf-8'))
if P.get('fail') != 0: die('pins carry fail=%s — predict_gate26.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('the pins are a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != ORDER: die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), ORDER))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']: die('origin develop %s != pinned %s — run predict_gate26.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
print('fill (%s) at %s | home %s | origin agrees with the pins (develop %s, the %d heads)' % (KIT, now(), GS, P['develop'][:12], len(ORDER)))
SC = json.load(open(os.path.join(GS, 'stopcounts_%s.json' % KIT), encoding='utf-8'))

CFG = {
 'gate26T1': dict(
  TIERWORD='tier 1', TIER_DEF='TIER 1: THROUGH-CODE PLUS RUNTIME',
  GO='`GO: merge #1274, #1280, #1281, #1282, #1283, #1284 batch`', MERGE_AUTH='so all six are squashed by a MERGE SEAT Wednesday names, never by an author',
  ADDENDUM_COUNT='PER PR FILE (2 over 2 paths) for #1274, (3 over 3 paths) for #1280, (2 over 2 paths) for #1281, #1282, #1283 and #1284',
  SUBJECT='[QA -> Wednesday] TIER-1 GATE batch #1274 #1280 #1281 #1282 #1283 #1284 (Seats L8 B29 B30, round 26; #1274 round 2 of 2)',
  SEAT_ITEMS=['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
              'MEASURED, through the real route: with more rows than the limit, the answer was',
              'TWO PERSISTING SITES, NOT ONE. The ticket, its gate report and my own first',
              'originate 878 -> 886, 74 -> 75 suites. Six red arms, one per writer plus the',
              'originate 878 -> 889, 74 suites both (an existing cell file was extended rather',
              'originate 878 -> 890, 74 -> 75 suites. Five red arms: the original ternary',
              'The cell that proves it was failing 9 of 12 when this seat adopted it, and the',
              '**60 passed, 0 failed, 0 skipped (of 60)**'],
  KEYWORDS=['LIMIT-TRUNC', 'R3-KNOWN-LIMIT-KS1335', 'ROTATION', 'ENV-ROUND2', 'LAST-SENT-AT-SOURCES', 'STALE-BODY-1274', 'HEAL-SITES-TWO', 'TOBLOCKHEIGHT-EDGES', 'WRITE-REACHED', 'RAW-HEIGHT-KS1333', 'CARRY-FIVE-WRITERS', 'READ-PER-WRITE', 'SIMULATED-NOT-CARRIED',
            'KS730-THREE-TOGETHER', 'NODE-ENV-MATRIX', 'LOG-CONTENT', 'LOG-SINK', 'STALE-COMMENT-532', 'FIXTURE-TRAP-DOES-NOT-EXIST', 'UNCONDITIONAL-LEAK-KS1334',
            'SOURCE-CELL-WEAKER', 'DOCBLOCK-DISPLACED', 'BASE-FIGURES-D7CDECF1'],
  RULES=[(48, ['ROUND 2 OF 2 FOR #1274 — THE CAP', 'LIMIT-TRUNC must be CLOSED at runtime', 'the healthy-row rotation cells do NOT cover the permanently failing row', 'you do NOT grade #1274 NO GO for the limit KS-1335 carries'], 'the #1274 round-2 cap rule'),
         (41, ['THE KS-730 SET (KS730-THREE-TOGETHER)', 'grade each of #1282, #1283 and #1284 on its own AND the three together on END_TREE', 'KS-730 stays In Progress after all three'], 'the KS-730 set'),
         (42, ['DECLARED SCOPE (grade as disclosed scope, never as a defect of the PR)', 'KS-1333 (Backlog)', 'KS-1334 (Backlog)'], 'the declared scope (KS-1333, KS-1334)'),
         (35, ['NO STACK, NO DOCKER.', 'listening on 127.0.0.1 only on an ephemeral port (port 0)', 'NEVER connect to the native Postgres on :5432'], 'no stack / no Docker / loopback only'),
         (43, ['a RUNTIME PROBE of the changed behaviour through the REAL module', 'TIER 1: THROUGH-CODE PLUS RUNTIME', 'each with a control that must be able to fail', 'EVIDENCE CLASS inline'], 'the TIER-1 runtime rule'),
         (44, ['RED PROOF (mandatory): verification.ts and verificationV2.ts at the parent', 'RED PROOF (mandatory): anchorStateSync.ts at the parent', 'RED PROOF (mandatory): systemErrors.ts at the parent', 'RED PROOF (mandatory): gdpr.ts at the parent', 'RED PROOF (mandatory): adminConfig.ts at the parent', 'RED PROOF (mandatory): m365-integration/src/index.ts at the parent of round 2'], 'the six mandatory red proofs'),
         (46, ['all six PRs link their ticket as `contributes`, none as `closes`'], 'the Linear link kinds'),
         (47, ['MG-3 KEY SCAN (measured by the drafter', 'KS1304 and KS1334 for #1284'], 'the MG-3 key scan')]),
 'gate26T2': dict(
  TIERWORD='tier 2', TIER_DEF='TIER 2: THROUGH-CODE',
  GO='`GO: merge #1245, #1261, #1268, #1275, #1276, #1277, #1278, #1279 batch`', MERGE_AUTH='so all eight are squashed by a MERGE SEAT Wednesday names, never by an author',
  ADDENDUM_COUNT='PER PR FILE (2 over 2 paths) for #1245, #1268, #1275 and #1278, (3 over 3 paths) for #1276, (1 over 1 path) for #1261, #1277 and #1279',
  SUBJECT='[QA -> Wednesday] TIER-2 GATE batch #1245 #1261 #1268 #1275-#1279 (Seats L6 L7 B28 B29 B30, round 26; three at the cap)',
  SHORT={'1245': 'KS-1313 SUMMARYREAD: read the vitest summary by label set, from vitest\'s own block',
         '1275': 'KS-1179: correct the N1 reachability claim, pin the N2 contract, fix TS7006',
         '1277': 'KS-1319: the wiring check survives a comment-out; derive nested and async walkers',
         '1278': 'KS-1314: catch a prettier-wrapped parser import; pin the loaders'},
  SEAT_ITEMS=['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
              'systemTest/performance unit suite 1115 -> 1120, 63 files both. The round-2 anchor',
              'THE THIRD RULE IS BEYOND THE GATE\'S TWO STATED SHAPES, and it is there because',
              'TWO halves, and each is needed -- proved by an arm that restores one at a time:',
              'EMIT BYTE-IDENTICAL, which is the requirement this change was held to:',
              'FIVE operations\' published schemas move, not two, because both bases are shared.',
              '  setupFiles commented out, the OLD check -> 7/7 FULLY GREEN',
              'systemTest/performance 1104/1104 bare -> 1106/1106 patched (63 files, +2',
              'satisfied the cell while being exactly the thing it reads as "a role RLS',
              '**60 passed, 0 failed, 0 skipped (of 60)**'],
  KEYWORDS=['MANIFEST-BY-NAME', 'TWO-HALVES', 'IMPORT-SCOPE-AST', 'MANIFEST-DRIFT', 'STALE-BODY-1261', 'RETURNED-ESCAPE', 'NEVER-REFERENCED-RULE', 'NEWEXPR-ARGS', 'KS1318-BLOB-IDENTICAL', 'KILLED-AFTER-LOOKALIKE', 'H1-FAMILY', 'STATUS-REFUSAL', 'EXIT-HOOK-AFTER-SUMMARY', 'ERRORS-LINE-LIVE', 'INERT-CLAUSE', 'CALLSITE-STILL-TEXT',
            'JOINED-CLAIM', 'MACHINE-PATH', 'TITLE-OVER-92', 'EMIT-PROOF', 'TS2349-RECORDED', 'NO-REFS-LINE', 'SPEC-SHAPE', 'FIVE-OPERATIONS', 'COMMENT-OUT-WIRING',
            'FIXTURE-TREE-ONLY', 'PRETTIER-CAPTURED', 'LOADERS-PIN', 'NO-DB-GUARD', 'DB-LEG-NOT-RUN', 'BASE-FIGURES-PER-PR'],
  RULES=[(40, ['A WRONG READING ON ANY REAL SHAPE = NO GO for that PR (blocking)', 'NAMES it (as a shape the check catches OR as a shape it declares safe)', 'THROUGH THE REAL CODE PATH — never a lifted regex, never a Python port', 'Do not soften the rule yourself'], 'THE READER RULE (#1245, #1261, #1268, #1277, #1278)'),
         (41, ['ROUND 3 OF 3 — THE LAST ROUND', 'H1 KILLED-AFTER-LOOKALIKE must read NULL', 'H1b and H1c must stay NULL', 'AT THE CAP A NO GO SHIPS NOTHING'], 'the #1245 round-3 cap rule'),
         (43, ['ROUND 2 OF 2 FOR #1261 — THE CAP', 'you ALSO revert the REAL lines in YOUR worktree', 'Grade both halves THROUGH THE REAL CELL'], 'the #1261 round-2 cap rule'),
         (42, ['ROUND 2 OF 2 FOR #1268 — THE CAP', 'GRADE THE THIRD RULE EXPLICITLY', 'W9 STILL reads false'], 'the #1268 round-2 cap rule'),
         (47, ['EMIT PROOF FOR #1275 (EMIT-PROOF)', 'an instrument that cannot say DIFFERENT proves nothing', 'A DIFFERENT emit = NO GO for #1275 (blocking)'], 'the #1275 EMIT PROOF'),
         (48, ['TITLE-OVER-92: four squash subjects are OVER 92', '(measured: 98, 102, 104 and 116 chars with ` (#NNNN)`'], 'TITLE-OVER-92'),
         (35, ['NO DOCKER, NO STACK, NO PORT in this gate', 'NEVER connect to the native Postgres on :5432'], 'no Docker / no stack / no port'),
         (37, ['#1245 and #1278 are systemTest/ pushes: NOT APPLICABLE'], 'the systemTest/ fleet STOP is NOT APPLICABLE'),
         (44, ['DECLARED SCOPE (grade as disclosed scope, never as a defect of the PR)', 'A declared-scope item is still graded by THE READER RULE'], 'the declared scope'),
         (46, ['all eight PRs link their tickets as `contributes`, none as `closes`'], 'the Linear link kinds'),
         (49, ['THE DB LEG OF #1279 IS NOT RUN (DB-LEG-NOT-RUN)', 'its red proof is READ ONLY'], 'the #1279 DB leg')]),
}[KIT]

def sq(s): return "'" + s.replace("'", "'\\''") + "'"
# MANDATED squash text per PR (subject + the one Refs line) and the MEASURED key sets the merger must know about. The title is READ from
# gh_body_<n>.md (written by gh_read_gate26.py from the PULLS API), never typed; a title whose `<title> (#n)` exceeds 92 is replaced by the kit's
# SHORT proposal (the gate rules on it). The KEY SCANNER below runs over every mandated block before anything is written.
KS = r'KS-\d+'
mand, keysets = [], []
for n in ORDER:
    gb = open(os.path.join(GS, 'gh_body_%s.md' % n), encoding='utf-8').read()
    title = gb.splitlines()[0].split(' ', 1)[1]; body = gb.split('\n', 3)[3] if gb.count('\n') >= 3 else ''
    own = K['prs'][n]['keys']
    subj = '%s (#%s)' % (title, n)
    short = CFG.get('SHORT', {}).get(n)
    if len(subj) > 92:
        if not short: die('#%s squash subject is %d chars and the kit has no SHORT proposal for it' % (n, len(subj)))
        subj = '%s (#%s)' % (short, n)
    mand.append('MANDATED SQUASH TEXT #%s: «%s\n\nRefs %s»' % (n, subj, ' '.join(own)))
    bk = sorted(set(re.findall(KS, body))); mk = P['prs'][n]['msg_keys']
    foreign = sorted((set(bk) | set(mk)) - set(own))
    keysets.append('#%s: own %s | PR body carries %s | its %d commit message(s) carry %s | FOREIGN keys the squash body must un-hyphenate: %s%s' % (
        n, own, bk, len(P['prs'][n]['commits']), mk, [f.replace('KS-', 'KS') for f in foreign] or 'none',
        ' | the PR title as read is %d chars with ` (#%s)` — OVER 92' % (len('%s (#%s)' % (title, n)), n) if len('%s (#%s)' % (title, n)) > 92 else ''))
rows, prrows, bases = [], [], {}
for n in ORDER:
    pr = P['prs'][n]; k = K['prs'][n]
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), pr['branch'], pr['head'], len(pr['paths']), pr['ahead'], pr['merge_base'], pr['behind'], ','.join(pr['paths']), k['tier']))
    fl = '; '.join('%s (%s; head blob %s; merged-blob target: %s %s)' % (p, [x for x in pr['numstat'] if x.endswith(p)][0].split('\t')[0] + '/' + [x for x in pr['numstat'] if x.endswith(p)][0].split('\t')[1],
                   pr['merged_blobs'][p]['head'], pr['merged_blobs'][p]['target'], pr['merged_blobs'][p]['merged']) for p in pr['paths'])
    prrows.append('- #%s %s (Seat %s, %s): head %s on branch %s, %d commit(s) (%s) over merge-base %s; %d behind the launch develop; merged tree over develop %s; files: %s.' % (
        n, ' + '.join(k['keys']), k['seat'], k['tier'], pr['head'], pr['branch'].replace('refs/heads/', ''), len(pr['commits']), ', '.join(c[:12] for c in pr['commits']), pr['merge_base'], pr['behind'], pr['merged_tree'], fl))
    bases.setdefault(pr['merge_base'], []).append('#' + n)
def stoprow(n):
    s = SC[n]
    if not s.get('preflight_ran'): return '#%s %s (%s -> %s, rc %s): NO PREFLIGHT (a systemTest/ push: %d lines, the format gate only) — NOT APPLICABLE.' % (n, os.path.basename(s['log']), s['start'][:20], s['end'][:20], s['rc'], s['lines'])
    return '#%s %s (%s -> %s, rc %s): `pre_push_hook_base` %s, fixture_guard %s, `run_shell_suites` %s (region) / %s (prefixed), shell suites %s;' % (
        n, os.path.basename(s['log']), s['start'][:20], s['end'][:20], s['rc'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['run_shell_suites_prefixed'], s['shell_suites'])
inf = '; '.join('#%s head %s (%s paths: %s)' % (n, v['head'], v['state'], ', '.join(os.path.basename(p) for p in v['paths'])) for n, v in sorted(P['inflight'].items()))
if not inf: inf = 'NONE in flight at this pin — every Seat B 30th fix round that was in flight at the first pin has been added to one of the two kits; predict_gate26.py re-censuses at every re-pin'
predict_out = sorted(f for f in os.listdir(GS) if re.match(r'predict_\d+\.out$', f))[-1]
V = {'GS': GS, 'KIT': KIT, 'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'END_TREE': P['end_tree'], 'END_WITH_SIB': P['end_tree_with_sibling'],
     'END_SHORTSTAT': P['end_shortstat'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'PR_ROWS': '\n'.join(prrows), 'ORDERS': str(P['orders']),
     'BASES': '; '.join('%s for %s' % (b, ', '.join(v)) for b, v in bases.items()), 'INFLIGHT': inf,
     'PREDICT_OUT': predict_out, 'STOP_ROWS': ' '.join(stoprow(n) for n in ORDER),
     'MANDATED': '\n'.join(mand), 'KEYSETS': '\n'.join(keysets),
     'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'OVR': 'QAB26%s_' % KIT[-2:], 'NROWS': str(len(ORDER)), 'NWORD': WORDS[len(ORDER)],
     'ROWS': '\n'.join(rows), 'ROWS_SUMMARY': ' · '.join('#%s %s (%s, %s)' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['seat'], K['prs'][n]['tier']) for n in ORDER),
     'TIERWORD': CFG['TIERWORD'], 'TIER_DEF': CFG['TIER_DEF'], 'GO': CFG['GO'], 'MERGE_AUTH': CFG['MERGE_AUTH'], 'ADDENDUM_COUNT': CFG['ADDENDUM_COUNT'], 'SUBJECT': CFG['SUBJECT'],
     'SEAT_ITEMS': ' \\\n'.join('  ' + sq(w) for w in CFG['SEAT_ITEMS']), 'KEYWORDS': ' \\\n'.join('  ' + sq(w) for w in CFG['KEYWORDS']),
     'SEAT_BLOCK': '\n'.join('- ' + w for w in CFG['SEAT_ITEMS']),
     'N_SEAT': str(len(CFG['SEAT_ITEMS'])), 'N_KW': str(len(CFG['KEYWORDS'])),
     'KIT_RULES': '\n'.join('%s || { echo "REFUSING: %s" >&2; exit %d; }' % (' && '.join('has %s' % sq(p) for p in ph), lab.replace('"', "'"), ex) for ex, ph, lab in CFG['RULES']),
     'KIT_EXITS': ' '.join('exit %d: %s.' % (ex, lab) for ex, ph, lab in CFG['RULES']), 'KIT_RULE_NAMES': ' / '.join(lab for ex, ph, lab in CFG['RULES'])}
def fill(t):
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    return t
prompt = fill(open(os.path.join(GS, 'prompt_%s.TEMPLATE.txt' % KIT), encoding='utf-8').read())
launch = fill(open(os.path.join(GS, 'launcher_%s.TEMPLATE.sh.txt' % KIT), encoding='utf-8').read())
left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', prompt + launch)))
if left: die('unfilled tokens: %s' % left)
cap = open(CAPTURE, encoding='utf-8').read()
online = lambda w, t: any(w in l for l in t.splitlines())
joined = re.sub(r'\n\s*', ' ', prompt)
miss = [w for w in CFG['SEAT_ITEMS'] if not online(w, prompt) or not online(w, cap)]
if miss: die('seat items not on one line in BOTH the prompt and the capture: %s' % miss)
missk = [w for w in CFG['KEYWORDS'] if w not in joined]
if missk: die('by-name keywords absent from the joined prompt: %s' % missk)
missr = [p for ex, ph, lab in CFG['RULES'] for p in ph if p not in joined] + [p for p in (CFG['TIER_DEF'], CFG['GO'].strip(), CFG['MERGE_AUTH'], CFG['ADDENDUM_COUNT']) if p not in joined]
if missr: die('kit-rule phrases absent from the joined prompt: %s' % missr)
for n in ORDER:
    if not re.search(r'(?<![0-9a-f])%s(?![0-9a-f])' % P['prs'][n]['head'], cap): die('the capture does not name #%s head %s' % (n, P['prs'][n]['head']))
# THE KEY SCANNER over every MANDATED squash text: blocks `MANDATED SQUASH TEXT #<n>: «…»` — the ONLY hyphenated key allowed is the PR's own
mand = re.findall(r'MANDATED SQUASH TEXT #(\d+): «(.*?)»', prompt, re.S)
if not mand: die('no MANDATED SQUASH TEXT block in the prompt — the key scan has nothing to measure')
for n, text in mand:
    ks = sorted(set(re.findall(r'KS-\d+', text))); own = K['prs'][n]['keys']
    if not ks or sorted(set(ks) - set(own)): die('KEY SCAN: mandated squash text for #%s carries %s (own %s)' % (n, ks, own))
    if n in ORDER and '(#%s)' % n in text and len(text.split('\n')[0]) > 92: die('KEY SCAN: mandated subject for #%s is %d chars (> 92)' % (n, len(text.split('\n')[0])))
print('key scan: %d mandated squash text block(s), each carries only its own key: %s' % (len(mand), ', '.join('#%s %s' % (n, sorted(set(re.findall(r'KS-\d+', t)))) for n, t in mand)))
for path, text, mode in ((PROMPT_OUT, prompt, 0o644), (LAUNCH_OUT, launch, 0o755)):
    if os.path.exists(path) and open(path, encoding='utf-8').read() != text:
        shutil.copy2(path, path + '.pre-' + datetime.datetime.now().strftime('%H%M%S'))
    open(path, 'w', encoding='utf-8').write(text); os.chmod(path, mode)
r = subprocess.run(['bash', '-n', LAUNCH_OUT], capture_output=True, text=True)
if r.returncode != 0: die('bash -n on the launcher: %s' % r.stderr)
print('seat items %d (per line, both files) · keywords %d · kit rules %d · develop %s · END_TREE %s · prompt %d bytes · launcher bash -n rc 0'
      % (len(CFG['SEAT_ITEMS']), len(CFG['KEYWORDS']), len(CFG['RULES']), P['develop'], P['end_tree'], len(prompt.encode())))
print('wrote %s and %s' % (PROMPT_OUT, LAUNCH_OUT))
