#!/usr/bin/env python3
"""fill_gate25.py — fill ONE gate25 kit's prompt + launcher templates from pins_<kit>.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home:
every path in the outputs is that directory). Re-reads origin develop and the four heads by `git ls-remote` (READ verb, from the Secuura checkout)
and REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate25.py
first, never filled. Pre-checks every seat item (raw, per LINE, in BOTH the capture and the filled prompt — the launcher's grep is line-based), every
by-name keyword and every kit-rule phrase (in the whitespace-joined prompt) exactly as the launcher will, and runs `bash -n` on the launcher. Keeps
any previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
Usage: fill_gate25.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
"""
import json, os, re, subprocess, sys, datetime, shutil
GS = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
KIT = K['kit']
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PROMPT_OUT = os.path.join(GS, K['prompt']); LAUNCH_OUT = os.path.join(GS, K['launcher'])
CAPTURE = os.path.join(GS, 'mail_%s_ready.md' % KIT)
ORDER = sorted(K['prs'])
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def die(m): print('REFUSING: ' + m); sys.exit(1)
P = json.load(open(os.path.join(GS, 'pins_%s.json' % KIT), encoding='utf-8'))
if P.get('fail') != 0: die('pins carry fail=%s — predict_gate25.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('the pins are a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != ORDER: die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), ORDER))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']: die('origin develop %s != pinned %s — run predict_gate25.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
print('fill (%s) at %s | home %s | origin agrees with the pins (develop %s, the four heads)' % (KIT, now(), GS, P['develop'][:12]))
SC = json.load(open(os.path.join(GS, 'stopcounts_%s.json' % KIT), encoding='utf-8'))

CFG = {
 'gate25T1': dict(
  TIERWORD='tier 1', TIER_DEF='TIER 1: THROUGH-CODE PLUS RUNTIME',
  GO='`GO: merge #1267, #1269, #1272, #1274 batch`', MERGE_AUTH='so all four are squashed by a MERGE SEAT Wednesday names, never by an author',
  ADDENDUM_COUNT='PER PR FILE (2 over 2 paths) for #1267, #1269, #1272 and #1274',
  SUBJECT='[QA -> Wednesday] TIER-1 GATE batch #1267 #1269 #1272 #1274 (Seat L8, round 25)',
  SEAT_ITEMS=['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
              'It does NOT protect status or currentLevel',
              'Measured against the unfixed route: 25 rows took 10048 ms.',
              'Red proof: at develop 11 of 14 red, 3 green.',
              'Red proof: with the product reverted to develop, W1 and W3 go RED and W2 stays',
              '**60 passed, 0 failed, 0 skipped (of 60)**'],
  KEYWORDS=['DECLARED-OVERLAP-1264', 'LOG-CONTENT', 'HDR-THROW', 'HDR-ON-500', 'UNREACHABLE-TODAY', 'ENV-NAN', 'ENV-ZERO', 'SCHEMA-SOURCES', 'SPEC-SHAPE',
            'KS-1327-LIMIT', 'MOCK-UPSERT-COLUMNS', 'SWALLOWED-SAVE-ERROR', 'STUBBED-GUARD', 'BASE-FIGURES-4DB87C3E', 'STATUS-VS-STATUSCODE', 'DELETED-IN-WINDOW'],
  RULES=[(41, ['THE DECLARED OVERLAP (DECLARED-OVERLAP-1264)', 'the 3-way merged blob, never the head blob', 'a merge seat that squashes #1267 with a whole-file copy of its head blob would REVERT #1264'], "the DECLARED OVERLAP (#1267 x #1264)"),
         (42, ['grade it as disclosed scope, NEVER as a defect of #1272', 'it is ticketed as KS-1327 (Backlog)', 'you do NOT grade #1272 NO GO for the limit KS-1327 carries'], "KS-849's known limit (KS-1327)"),
         (35, ['NO STACK, NO DOCKER.', 'listening on 127.0.0.1 only on an ephemeral port (port 0)', 'NEVER connect to the native Postgres on :5432'], 'no stack / no Docker / loopback only'),
         (43, ['a RUNTIME PROBE of the changed behaviour through the REAL module', 'TIER 1: THROUGH-CODE PLUS RUNTIME', 'each with a control that must be able to fail', 'EVIDENCE CLASS inline'], 'the TIER-1 runtime rule'),
         (44, ['RED PROOF (mandatory, YOUR worktree): revert credentialRepo.ts', 'RED PROOF (mandatory): errorHandler.ts at the parent', 'RED PROOF (mandatory): kyc/src/index.ts at the parent', 'RED PROOF (mandatory): m365-integration/src/index.ts at the parent'], 'the four mandatory red proofs'),
         (46, ['all four PRs link their ticket as `contributes`, none as `closes`'], 'the Linear link kinds')]),
 'gate25T2': dict(
  TIERWORD='tier 2 + tier 3', TIER_DEF='TIER 2: THROUGH-CODE',
  GO='`GO: merge #1268, #1270, #1271, #1273 batch`', MERGE_AUTH='so #1268 and #1271 are squashed by a MERGE SEAT Wednesday names, never by an author',
  ADDENDUM_COUNT='PER PR FILE (2 over 2 paths) for #1268 and #1270, (4 over 4 paths) for #1271, (1 over 1 path) for #1273',
  SUBJECT='[QA -> Wednesday] TIER-2 GATE batch #1268 #1270 #1271 #1273 (Seats L7 B29, round 25)',
  SEAT_ITEMS=['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
              'EQUIVALENT at 3155 and 89849 bytes, 0 diagnostics.',
              'includes() returns ["version"] for ALL THREE',
              "Under develop's walk with these cells present: exactly ONE red, W9.",
              'the three ks781 errors marked "after #1268 merges"',
              '**60 passed, 0 failed, 0 skipped (of 60)**'],
  KEYWORDS=['MAGIC-WORD-CLOSES', 'TITLE-OVER-92', 'NO-REFS-LINE', 'BACKTICK-SPAN', 'SUBSET-NOT-EQUAL', 'W13-UNDECIDED', 'KS1329-TSC', 'SYMLINK-SAMEPATH',
            'SYSTEMTEST-NO-PREFLIGHT', 'EMIT-PROOF', 'COMMENT-CLAIMS', 'K1B-SOURCE-TEXT', 'CALL-SHAPES', 'PARAGRAPH-JOIN'],
  RULES=[(40, ['A WRONG READING ON ANY REAL SHAPE = NO GO for that PR (blocking)', 'NAMES it (as a shape the check catches OR as a shape it declares safe)', 'THROUGH THE REAL CODE PATH — never a lifted regex, never a Python port', 'Do not soften the rule yourself'], 'THE READER RULE (#1268, #1273)'),
         (47, ['TIER 3 (#1270): THROUGH-CODE ONLY', 'TIER-3 PROOF FOR #1270 (EMIT-PROOF)', 'an instrument that cannot say DIFFERENT proves nothing', 'A DIFFERENT emit, or a code line in the diff = NO GO for that PR (blocking)'], "#1270's TIER-3 PROOF"),
         (48, ['Linear linked KS-1164 to #1271 as **`closes`**', 'the merge addendum must carry a shortened subject', '(measured: 90, 74, 101 and 83 chars with ` (#NNNN)` — #1271 OVER)'], "#1271's MAGIC-WORD-CLOSES + TITLE-OVER-92"),
         (35, ['NO DOCKER, NO STACK, NO PORT in this gate', 'NEVER connect to the native Postgres on :5432'], 'no Docker / no stack / no port'),
         (37, ['#1271 is a systemTest/ push: NOT APPLICABLE'], "#1271's fleet STOP is NOT APPLICABLE"),
         (44, ['DECLARED SCOPE (grade as disclosed scope, never as a defect of the PR)', 'A declared-scope item is still graded by THE READER RULE'], 'the declared scope'),
         (49, ["if it is LIVE at the GO it squashes its own PRs, otherwise the merge seat does"], "B 29th's merge authority")]),
}[KIT]

def sq(s): return "'" + s.replace("'", "'\\''") + "'"
rows = []
prrows = []
for n in ORDER:
    pr = P['prs'][n]; k = K['prs'][n]
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), pr['branch'], pr['head'], len(pr['paths']), pr['ahead'], pr['merge_base'], pr['behind'], ','.join(pr['paths']), k['tier']))
    fl = '; '.join('%s (%s; head blob %s; merged-blob target: %s %s)' % (p, [x for x in pr['numstat'] if x.endswith(p)][0].split('\t')[0] + '/' + [x for x in pr['numstat'] if x.endswith(p)][0].split('\t')[1],
                   pr['merged_blobs'][p]['head'], pr['merged_blobs'][p]['target'], pr['merged_blobs'][p]['merged']) for p in pr['paths'])
    prrows.append('- #%s %s (Seat %s, %s): head %s on branch %s, ONE commit on parent %s; merged tree over develop %s; files: %s.' % (
        n, ' + '.join(k['keys']), k['seat'], k['tier'], pr['head'], pr['branch'].replace('refs/heads/', ''), pr['parent'], pr['merged_tree'], fl))
def stoprow(n):
    s = SC[n]
    if not s.get('preflight_ran'): return '#%s %s (%s -> %s, rc %s): NO PREFLIGHT (a systemTest/ push: %d lines, the format gate only) — NOT APPLICABLE.' % (n, os.path.basename(s['log']), s['start'][:20], s['end'][:20], s['rc'], s['lines'])
    return '#%s %s (%s -> %s, rc %s): `pre_push_hook_base` %s, fixture_guard %s, `run_shell_suites` %s (region) / %s (prefixed), shell suites %s;' % (
        n, os.path.basename(s['log']), s['start'][:20], s['end'][:20], s['rc'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['run_shell_suites_prefixed'], s['shell_suites'])
m1 = ('Seat M1\'s five are ALL on it (#1262 4f5fe45b860b, #1263 f2baad995d88, #1264 65176ac3adf8, #1265 6f724ab6e1ef, #1266 df5e9f5da6d2) and its tree equals M1\'s expected END tree 6942101caa7be149c1fc4a254eefc75af3607b86 (measured).'
      if not P['m1_open'] and P['develop_tree'] == K['m1_end_tree'] else
      'Seat M1\'s still-OPEN PR(s) at the pin: %s — the kit\'s END_TREE_AFTER_M1 (develop + those + this kit) is %s; if M1 lands them first, launch step 3b re-pins.' % (P['m1_open'] or 'none', P['end_tree_after_m1']))
cols = ''
for o in P['probes'].get('1272', []):
    if o.startswith('dbSaveVerification DO UPDATE SET columns (READ): '): cols = o.split('(READ): ', 1)[1]
predict_out = sorted(f for f in os.listdir(GS) if re.match(r'predict_\d+\.out$', f))[-1]
V = {'GS': GS, 'KIT': KIT, 'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'BEHIND': str(P['behind_parent']), 'END_TREE': P['end_tree'],
     'END_SHORTSTAT': P['end_shortstat'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'PR_ROWS': '\n'.join(prrows), 'M1_STATE': m1,
     'PREDICT_OUT': predict_out, 'STOP_ROWS': ' '.join(stoprow(n) for n in ORDER), 'KYC_COLS': cols,
     'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'OVR': 'QAB25%s_' % KIT[-2:],
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
for path, text, mode in ((PROMPT_OUT, prompt, 0o644), (LAUNCH_OUT, launch, 0o755)):
    if os.path.exists(path) and open(path, encoding='utf-8').read() != text:
        shutil.copy2(path, path + '.pre-' + datetime.datetime.now().strftime('%H%M%S'))
    open(path, 'w', encoding='utf-8').write(text); os.chmod(path, mode)
r = subprocess.run(['bash', '-n', LAUNCH_OUT], capture_output=True, text=True)
if r.returncode != 0: die('bash -n on the launcher: %s' % r.stderr)
print('seat items %d (per line, both files) · keywords %d · kit rules %d · develop %s · END_TREE %s · prompt %d bytes · launcher bash -n rc 0'
      % (len(CFG['SEAT_ITEMS']), len(CFG['KEYWORDS']), len(CFG['RULES']), P['develop'], P['end_tree'], len(prompt.encode())))
print('wrote %s and %s' % (PROMPT_OUT, LAUNCH_OUT))
