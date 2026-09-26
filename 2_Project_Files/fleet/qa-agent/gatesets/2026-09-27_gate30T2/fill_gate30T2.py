#!/usr/bin/env python3
"""fill_gate30T2.py — fill ONE gate30T2 kit's prompt + launcher templates from pins_<kit>.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home:
every path in the outputs is that directory). Re-reads origin develop and every head by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate30T2.py
first, never filled. Pre-checks every seat item (raw, per LINE, in BOTH the capture and the filled prompt — the launcher's grep is line-based), every
by-name keyword and every kit-rule phrase (in the whitespace-joined prompt) exactly as the launcher will, runs the round's KEY SCANNER over every
MANDATED squash text block of the prompt (a block may carry no hyphenated KS key but its own PR's), and runs `bash -n` on the launcher. Keeps any
previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
Shape copied from gate29's fill_gate29.py; re-keyed to gate30T2's four rows (all T2; sibling kit gate30T1).
Usage: fill_gate30T2.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil
GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
KIT = K['kit']
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, K['prompt']); LAUNCH_OUT = os.path.join(GS, K['launcher'])
CAPTURE = os.path.join(GS, 'mail_%s_ready.md' % KIT)
ORDER = sorted(K['prs'])
WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight'}
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def die(m): print('REFUSING: ' + m); sys.exit(1)
P = json.load(open(os.path.join(GS, 'pins_%s.json' % KIT), encoding='utf-8'))
if P.get('fail') != 0: die('pins carry fail=%s — predict_gate30T2.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('the pins are a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != ORDER: die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), ORDER))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']: die('origin develop %s != pinned %s — run predict_gate30T2.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
print('fill (%s) at %s | home %s | origin agrees with the pins (develop %s, the %d heads)' % (KIT, now(), GS, P['develop'][:12], len(ORDER)))
SC = json.load(open(os.path.join(GS, 'stopcounts_%s.json' % KIT), encoding='utf-8'))

CFG = {
 'gate30T2': dict(
  TIERWORD='tier 2', TIER_DEF='TIER 2: THROUGH-CODE',
  GO='`GO: merge #1293, #1295, #1298, #1299 batch`', MERGE_AUTH='so all four are squashed by Seat B 32nd, the merge seat Wednesday names for this GO',
  ADDENDUM_COUNT='PER PR FILE (7 over 7 paths) for #1293, #1295, #1298 and #1299',
  SUBJECT='[QA -> Wednesday] GATE30T2 batch #1293 #1295 #1298 #1299 (Seat B32, round 30; T2 KS-1344, KS-1337 akto, KS-1347, KS-1339)',
  SHORT={'1293': 'KS-1344: clear the logger per environment in ks1341a and assert the call list'},
  SEAT_ITEMS=['Test-only. One file, one hunk, +3/−1. No product bytes change.',
              '8 passed, 0 failed — completely blind',
              'Tests:       2 failed, 6 passed, 8 total',
              'patched 962 passed / 0 failed (82 suites)',
              'whether A2 should also assert a whole call list is a separate question, not decided here',
              'a function-name suffix on the hunk header, and one extra trailing context line',
              'Tests  1 failed | 2 passed (3)',
              'patched 70 files / 1236 tests passed',
              'A missing gate is not a passing gate.',
              'There are two goldens under similar names',
              '[format-gate] 1 package(s) checked, 0 skipped, 0 failed',
              'The playwright site is untouched',
              'not a clean rung-4 result',
              'All matched files use Prettier code style!',
              '22 problems (0 errors, 22 warnings)',
              'Test files only — no auth product code changes.',
              'runs vitest, not jest.',
              'Tests  835 passed (835)',
              '**37 errors at my head and 37 at the tip.**',
              'One token was changed on review, and here is the whole delta:',
              '15 problems (0 errors, 15 warnings)',
              'Tests: 1 failed, 3 passed, 4 total',
              'patched 966 passed / 0 failed',
              'The count floor is not weakened, and that is asserted rather than claimed:',
              'This changes **only the order in which two existing assertions fail**.',
              'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.'],
  KEYWORDS=['KS1344-TAMPER-2X2', 'DOUBLE-LOG-ARM', 'A1-NAMES-ENV', 'A2-UNCHANGED', 'TEST-ONLY-NO-PRODUCT-BYTE', 'KS1344-AFTER-PART-C', 'ORIGINATE-962-962',
            'TSC-EXCLUDES-TESTS', 'LINT-22-WARNINGS', 'GOLDEN-BLOB-IDENTITY', 'FILEURLTOPATH-FIX', 'SPACED-PATH-RED', 'CELL-READS-FIRST-STEP-LINE',
            'DOD2-APPROXIMATION', 'NOT-COVERED-TRUE', 'KS1337-STAYS-OPEN', 'TWO-GOLDENS', 'SPACED-PATH-SUITE', 'OWN-LINT-FORMAT-UNIT',
            'NO-PLATFORM-PREFLIGHT', 'AKTO-1233-1236', 'TEST-FILES-ONLY-AUTH', 'SPACED-CHECKOUT-RED', 'REAL-PROOF-SPACED', 'ONE-NON-GOLDEN-TOKEN',
            'TSC-TEST-INCLUSIVE', 'AUTH-832-835', 'KS1347-STAYS-OPEN', 'TEST-FILES-ONLY-ORIGINATE', 'OFFENDER-FIRST-RED', 'FLOOR-KEPT',
            'CELL-EXECUTES-KS1293-TEXT', 'REAL-SCAN-NAMES-FILE', 'ORIGINATE-962-966', 'BASE-FIGURES-PER-PR'],
  RULES=[(40, ['THE RED FOR #1293 COMES FROM A PRODUCT TAMPER', "A1 rows RED at #1293's head and GREEN at the tip under the same tamper", '#1293 IS TEST-ONLY: any product byte in #1293 is a finding'], 'the #1293 product-tamper red'),
         (41, ['RED DESIGN AND DISCLOSURE FOR #1295', 'the RED cell must still red on `toBe` or `existsSync`'], 'the #1295 red design and disclosure'),
         (42, ["THE AKTO PACKAGE'S OWN GATES", '`npm run test:unit` (vitest, vitest.unit.config.ts) at develop, head and END_TREE'], 'the #1295 own lint / format / unit'),
         (43, ['A UNIT RUN FROM A SPACED PATH', 'as gate29 did for #1291'], 'the #1295 spaced-path suite'),
         (44, ['KS-1347 — TEST FILES ONLY (WIDEN #1298', 'any path outside src/__tests__/ is a NO GO for #1298 under the rule', 'THE REAL PROOF FROM A SPACED CHECKOUT'], 'the #1298 test-files-only widen rule'),
         (45 + 3, ['KS-1339 — TEST FILES ONLY (WIDEN #1299', 'make it go red on purpose once', 'THE CELL EXECUTES TEXT'], 'the #1299 test-files-only widen rule'),
         (37, ['For #1295 the fleet STOP count is NOT APPLICABLE'], 'the #1295 fleet STOP NOT APPLICABLE'),
         (35, ['NO DOCKER, NO STACK, NO PORT in this gate', 'NEVER connect to the native Postgres on :5432'], 'no Docker / no stack / no port'),
         (47, ['MG-3 KEY SCAN (measured by the drafter', 'a squash body is NEVER "the verbatim head commit message" here'], 'the MG-3 key scan'),
         (46, ['all four PRs link their tickets as `contributes`, none as `closes`'], 'the Linear link kinds')]),
}[KIT]

def sq(s): return "'" + s.replace("'", "'\\''") + "'"
# MANDATED squash text per PR (subject + the one Refs line) and the MEASURED key sets the merger must know about. The title is READ from
# gh_body_<n>.md (written by gh_read_gate30T2.py from the PULLS API), never typed; a title whose `<title> (#n)` exceeds 92 is replaced by the kit's
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
inf = '%d open PRs, each path-disjoint: ' % len(P['inflight']) + ', '.join('#%s@%s' % (n, v['head'][:12]) for n, v in sorted(P['inflight'].items(), key=lambda x: -int(x[0])))
if not inf: inf = 'NONE open at this pin besides the kit; predict_gate30T2.py re-censuses at every re-pin'
predict_out = sorted(f for f in os.listdir(GS) if re.match(r'predict_\d+\.out$', f))[-1]
V = {'GS': GS, 'KIT': KIT, 'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'END_TREE': P['end_tree'], 'END_WITH_SIB': P['end_tree_with_sibling'],
     'END_SHORTSTAT': P['end_shortstat'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'PR_ROWS': '\n'.join(prrows), 'ORDERS': str(P['orders']),
     'BASES': '; '.join('%s for %s' % (b, ', '.join(v)) for b, v in bases.items()), 'INFLIGHT': inf,
     'PREDICT_OUT': predict_out, 'STOP_ROWS': ' '.join(stoprow(n) for n in ORDER),
     'MANDATED': '\n'.join(mand), 'KEYSETS': '\n'.join(keysets),
     'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'OVR': 'QAB30T2_', 'NROWS': str(len(ORDER)), 'NWORD': WORDS[len(ORDER)],
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
