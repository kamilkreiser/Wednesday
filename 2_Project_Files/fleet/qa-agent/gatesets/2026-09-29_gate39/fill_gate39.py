#!/usr/bin/env python3
r"""fill_gate39.py — fill the gate39 kit's prompt + launcher templates from pins_<kit>.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home:
every path in the outputs is that directory). Re-reads origin develop and every head by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate39.py
first, never filled. Pre-checks every seat item (raw, per LINE, in BOTH the capture and the filled prompt — the launcher's grep is line-based), every
by-name keyword and every kit-rule phrase (in the whitespace-joined prompt) exactly as the launcher will, runs the round's KEY SCANNER over every
MANDATED squash text block of the prompt (a block may carry no hyphenated KS key but its own PR's), and runs `bash -n` on the launcher. Keeps any
previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
THE SUBJECT RULE (STANDING_LINES 2026-09-27, "a declared squash subject NEVER carries the `(#n)` suffix, and its length is checked as it will LAND"):
every MANDATED subject is DECLARED WITHOUT ` (#n)`; fill REFUSES a declared subject matching `\(#\d+\)$` and one whose len(declared) + len(" (#n)")
exceeds 92, and prints each subject's declared and landed lengths. gate39: both titles land <= 92 (#1337 84, #1332 91 — gh_read_1.out), so SHORT is EMPTY
and every declared subject is the PR title as the PULLS API returned it; a SHORT entry, if planted, must still pass the key scan and both length rules.
Shape copied from gate38's fill (gate37 -> gate36 lineage); re-keyed to gate39's two rows (T2 + T1), no stack (no RETARGET tree), no sibling kit, TWO
merge-bases; kit rules 44 (the merge order, #1337 first), 55 (the last round under the two-NO-GO cap) and 56 (the full disk) are new this round.
Usage: fill_gate39.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
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
if P.get('fail') != 0: die('pins carry fail=%s — predict_gate39.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('the pins are a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != ORDER: die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), ORDER))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']: die('origin develop %s != pinned %s — run predict_gate39.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
if P.get('stacks') or P.get('declared_overlap') or P.get('noop_paths'): die('the pins carry a stack / an overlap / a no-op declaration (%s / %s / %s) — gate39 declares none; re-draft' % (P.get('stacks'), P.get('declared_overlap'), P.get('noop_paths')))
print('fill (%s) at %s | home %s | origin agrees with the pins (develop %s, the %d heads)' % (KIT, now(), GS, P['develop'][:12], len(ORDER)))
SC = json.load(open(os.path.join(GS, 'stopcounts_%s.json' % KIT), encoding='utf-8'))

CFG = {
 'gate39': dict(
  TIERWORD='T2 + T1', TIER_DEF='T1 ROWS ARE GRADED THROUGH CODE AND AT RUNTIME',
  GO='`GO: merge #1337, #1332 batch`', MERGE_AUTH='so both are squashed by Seat B 41st, the merge seat Wednesday names for this GO',
  ADDENDUM_COUNT='PER PR FILE (12 over 12 paths) for #1337 and #1332',
  SUBJECT='[QA -> Wednesday] GATE39 batch #1337 #1332 (Seat B41, round 39; T2 + T1: KS-888 the KS 764 guard, KS-1054 round 2 of 2)',
  # no SHORT subject this round: both PR titles land <= 92 (gh_read_1.out: #1337 84, #1332 91); each subject is declared WITHOUT the (#n) suffix
  SHORT={},
  SEAT_ITEMS=['1 failed / 14 passed (15)',
              '48 files, 1 failed / 944 (945)',
              '48 files, 945 / 945',
              '36 problems (1 error, 35 warnings)',
              '14 passed / 1 failed',
              'A hunk-offset mutation is NOT a valid control for `git apply --check`',
              "The READY's own A4 line is wrong.",
              'Two of the three sides you named were NOT driven',
              'The gateway runner was not driven',
              'A second pass changes none of those five on mine.',
              '88 files, 795 tests, 0 failed',
              '29 → 29, delta 0',
              'Three migrations that fail forever on the other two trees now succeed',
              'reference these four tables, so an earlier number changes far more than the blocker needs',
              "CORE's definitions alone vs 038a alone, two bare databases, four tables",
              'N-1332-5 is NOT in this commit',
              'The KS 764 guard reds on this branch',
              'A deploy must rebuild BOTH the migrations image and the api-gateway image.',
              '10 → 8 passed / 2 failed',
              'blind to a letter-suffixed migration',
              'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.'],
  KEYWORDS=['GUARD-GREEN-ON-END', 'PATCH-EQUALS-HELD-SPARK', 'GUARD-REDS-ON-BROKEN-REVOKE', 'GUARD-ARMS-ON-PRODUCT', 'A4-RED-COUNT', 'SWEEP-DRIFT-UNSEEN',
            'ESLINT-DELTA-ZERO', 'OFFSET-NOT-A-CONTROL', 'THREE-PATHS-DRILL', 'GATEWAY-RUNNER-TWICE', 'RUNMIG-THEN-GATEWAY', 'INIT-THEN-GATEWAY',
            'SECOND-BOOT-CHANGES-NOTHING', 'SCHEMA-EQUALITY-PG-DUMP', 'CERTIFICATIONS-NO-TENANT-POLICY', 'APP-ROLE-PROBE', 'LEXICAL-POSITION-038A',
            'LOCALE-COLLATION', 'MIGRATIONS-006-008-047', 'OTHER-MIGRATIONS-UNCHANGED', 'CORE-THROW-COUNTED', 'ERROR-FIELD-SET', 'PLATFORM-CORE-CATCH',
            'RUN-RECORD-WIRING', 'HEALTH-BODIES-AS-SERVED', 'READY-CODE-UNCHANGED', 'DEPLOY-READS-FAILED', 'COMPOSE-RUNNER-EXIT', 'ROUND1-DB-NOT-HEALED',
            'MIGRATIONS-IMAGE-REBUILD', 'TS2322-DELTA-ZERO', 'THE-POSTGRES', 'LAST-ROUND-CAP', 'PRE-EXISTING-RED', 'CROSS-PACKAGE-GUARDS', 'KS764-DRIFT-CELL',
            'MERGE-ORDER-1337-FIRST', 'TWO-BASES', 'SUBJECT-LANDS-AT', 'NOOP-VS-OVERLAP', 'NO-FOREIGN-KEY', 'ADDENDUM-ONE-LINE-PER-PR', 'SHARED-COUNTS',
            'GATEWAY-COUNTS', 'AUTH-COUNTS', 'TSC-EXCLUDES-TESTS', 'LOCAL-MODEL-PROVENANCE', 'DISK-ENOSPC', 'TIERING'],
  RULES=[(40, ['THE GUARD ROW (#1337;', 'the PR diff EQUALS the held Spark patch', 'packages/shared 1 failed / 945 -> 945 / 945', 'the guard must still RED on a broken revoke'], 'the #1337 guard row'),
         (41, ['THE START-UP ROW (#1332 ROUND 2 of 2;', 'on a REAL PostgreSQL over a unix socket (no TCP)', '(i) a bare database through the GATEWAY runner',
               '(ii) a bare database through `scripts/run-migrations.sh` THEN a gateway boot', '(iii) a docker/init-seeded database then a gateway boot',
               'byte-identical across (i), (ii), (iii) and develop\'s seeded path'], 'the #1332 three-path start-up row'),
         (42, ['NOT COVERED, DISCLOSED (#1332):', 'N-1332-5 (the deploy scripts read the flag) is UNRAISED by ruling', 'it is not a NO GO for this round'], 'the #1332 disclosed not-covered'),
         (43, ['THE POSTGRES (#1332):', 'SAY SO PLAINLY', 'a socket directory shorter than 103 bytes', 'NEVER the native Postgres on :5432, never a container'], 'the real-Postgres rule'),
         (44, ['MERGE ORDER: #1337 FIRST', 'the pre-existing KS-764 guard red that #1337 fixes'], 'the merge order, #1337 first'),
         (46, ['every PR links its ticket as `contributes`, none as `closes`'], 'the Linear link kinds'),
         (47, ['MG-3 KEY SCAN (measured by the drafter', 'a squash body is NEVER "the verbatim head commit message" here', 'startup-migrations.ts and 038a carry foreign hyphenated keys as CONTENT'], 'the MG-3 key scan'),
         (48, ['SQUASH SUBJECTS ARE DECLARED WITHOUT THE (#n) SUFFIX', 'len(declared) + len(" (#n)") <= 92', 'the merge tool refuses a declared subject matching'], 'the squash-subject rule'),
         (49, ['THE DECLARATION KEYS (NOOP-VS-OVERLAP;', '`merged_blob_paths` (a GENUINE overlap', '`noop_paths` (a squash-stack NO-OP'], 'the no-op vs overlap keys'),
         (51, ['the SUBJECT of the GO mail NAMES Seat B 41st', 'GO (Seat B 41st): merge 1337 1332 on gate39'], 'the GO subject names the merge seat'),
         (52, ['THE ADDENDUM IS ONE LINE PER PR in exactly this shape', '- #NNNN · head <sha12> · subject: `<subject>`', 'NO sub-bullets'], 'the addendum one-line-per-PR shape'),
         (53, ['PRE-EXISTING RED, NAMED (standing requirement 1', 'must be GREEN on END_TREE after #1337'], 'the pre-existing red, named, green after #1337'),
         (54, ['CROSS-PACKAGE GUARDS (standing requirement 2', 'RUN every suite that references a changed path', 'every suite that reads the migrations DIRECTORY'], 'the cross-package guards'),
         (55, ['THE LAST ROUND (the two-NO-GO cap', 'this is ROUND 2 of 2 for #1332'], 'the last round under the two-NO-GO cap'),
         (56, ['DISK: /Volumes/DevMASTER is FULL', 'STOP on any ENOSPC', 'goes on the Data volume'], 'the full-disk rule: Data volume, STOP on ENOSPC'),
         (35, ['NO DOCKER, NO STACK, NO TCP PORT in this gate', 'NEVER connect to the native Postgres on :5432'], 'no Docker / no stack / no TCP port')]),
}[KIT]

def sq(s): return "'" + s.replace("'", "'\\''") + "'"
# MANDATED squash text per PR (subject + the one Refs line) and the MEASURED key sets the merger must know about. The title is READ from
# gh_body_<n>.md (written by gh_read_gate39.py from the PULLS API), never typed; a title whose `<title> (#n)` exceeds 92 is replaced by the kit's
# SHORT proposal (the gate rules on it). The KEY SCANNER below runs over every mandated block before anything is written.
KS = r'KS-\d+'
SUFFIX = re.compile(r'\(#\d+\)$')
mand, keysets, sublens, SUBJ = [], [], [], {}
for n in ORDER:
    gb = open(os.path.join(GS, 'gh_body_%s.md' % n), encoding='utf-8').read()
    title = gb.splitlines()[0].split(' ', 1)[1]; body = gb.split('\n', 3)[3] if gb.count('\n') >= 3 else ''
    if title != P['titles'][n]: die('#%s title in gh_body_%s.md %r != the title predict read from the API %r — re-read (gh_read_gate39.py)' % (n, n, title, P['titles'][n]))
    own = K['prs'][n]['keys']
    short = CFG.get('SHORT', {}).get(n)
    decl = short or title
    lands = len(decl) + len(' (#%s)' % n)
    if SUFFIX.search(decl.strip()): die('#%s declared subject %r ENDS IN a (#n) suffix — GitHub appends it; declare it WITHOUT (STANDING_LINES 2026-09-27)' % (n, decl))
    if lands > 92:
        die('#%s declared subject %r lands at %d chars (declared %d + " (#%s)" %d) > 92 and the kit has no SHORT subject for it' % (n, decl, lands, len(decl), n, len(' (#%s)' % n)))
    SUBJ[n] = decl
    mand.append('MANDATED SQUASH TEXT #%s (declared %d, lands at %d): «%s\n\nRefs %s»' % (n, len(decl), lands, decl, ' '.join(own)))
    bk = sorted(set(re.findall(KS, body))); mk = P['prs'][n]['msg_keys']
    foreign = sorted((set(bk) | set(mk)) - set(own))
    tl = len(title) + len(' (#%s)' % n)
    keysets.append('#%s: own %s | PR body carries %s | its %d commit message(s) carry %s | FOREIGN keys the squash body must un-hyphenate: %s%s' % (
        n, own, bk, len(P['prs'][n]['commits']), mk, [f.replace('KS-', 'KS') for f in foreign] or 'none',
        ' | the PR title as read lands at %d chars — OVER 92, so the SHORT subject (declared %d, lands at %d) is mandated' % (tl, len(decl), lands) if short else ''))
    sublens.append('#%s declared %d / lands at %d%s' % (n, len(decl), lands, (' (the title would land at %d)' % tl) if short else ''))
rows, prrows, bases = [], [], {}
for n in ORDER:
    pr = P['prs'][n]; k = K['prs'][n]
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), pr['branch'], pr['head'], len(pr['paths']), pr['ahead'], pr['merge_base'], pr['behind'], ','.join(pr['paths']), k['tier']))
    fl = '; '.join('%s (%s; head blob %s; merged-blob target: %s %s)' % (p, [x for x in pr['numstat'] if x.endswith(p)][0].split('\t')[0] + '/' + [x for x in pr['numstat'] if x.endswith(p)][0].split('\t')[1],
                   pr['merged_blobs'][p]['head'], pr['merged_blobs'][p]['target'], pr['merged_blobs'][p]['merged']) for p in pr['paths'])
    stk = pr.get('stacked_on')
    prrows.append('- #%s %s (Seat %s, %s): head %s on branch %s, %d commit(s) (%s) over %s %s; %d behind %s; merged tree %s %s; files: %s.' % (
        n, ' + '.join(k['keys']), k['seat'], k['tier'], pr['head'], pr['branch'].replace('refs/heads/', ''), len(pr['commits']), ', '.join(c[:12] for c in pr['commits']),
        ('STACKED on #%s: its parent head' % stk) if stk else 'merge-base', pr['merge_base'], pr['behind'], ('#%s\'s head' % stk) if stk else 'the launch develop',
        ('over develop + #%s' % stk) if stk else 'over develop', pr['merged_tree'], fl))
    bases.setdefault(pr['merge_base'], []).append('#' + n + (' (STACKED on #%s: its chain base is #%s\'s head)' % (stk, stk) if stk else ''))
PUSHLOG_NAMES = {'1337': 'push41-ks764.rawlog', '1332': 'push41-ks1054.rawlog'}
def stoprow(n):
    s = SC[n]
    if s.get('log') == 'ABSENT': return '#%s: NO PUSH LOG in the seat record at drafting (%s) — the gate reads it if the seat has written it since, and says so; otherwise UNREAD.' % (n, os.path.basename(PUSHLOG_NAMES.get(n, '?')))
    if not s.get('preflight_ran'): return '#%s %s (%s -> %s, rc %s): NO PREFLIGHT (a systemTest/ push: %d lines, the format gate only) — NOT APPLICABLE.' % (n, os.path.basename(s['log']), s['start'][:20], s['end'][:20], s['rc'], s['lines'])
    return '#%s %s (%s lines): `pre_push_hook_base` %s, fixture_guard %s, `run_shell_suites` %s (region) / %s (prefixed), shell suites %s;' % (
        n, os.path.basename(s['log']), s['lines'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['run_shell_suites_prefixed'], s['shell_suites'])
inf = '%d open PRs, each path-disjoint: ' % len(P['inflight']) + ', '.join('#%s@%s' % (n, v['head'][:12]) for n, v in sorted(P['inflight'].items(), key=lambda x: -int(x[0])))
if not inf: inf = 'NONE open at this pin besides the kit; predict_gate39.py re-censuses at every re-pin'
predict_out = sorted(f for f in os.listdir(GS) if re.match(r'predict_\d+\.out$', f))[-1]
V = {'GS': GS, 'KIT': KIT, 'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'END_TREE': P['end_tree'], 'END_WITH_SIB': str(P['end_tree_with_sibling']),
     'END_SHORTSTAT': P['end_shortstat'],
     'STACKS': ' '.join('%s:%s' % (c, p) for c, p in sorted(P['stacks'].items())), 'SUBJ_LENS': ', '.join(sublens), 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'PR_ROWS': '\n'.join(prrows), 'ORDERS': str(P['orders']),
     'BASES': '; '.join('%s for %s' % (b, ', '.join(v)) for b, v in bases.items()), 'INFLIGHT': inf,
     'PREDICT_OUT': predict_out, 'STOP_ROWS': ' '.join(stoprow(n) for n in ORDER),
     'MANDATED': '\n'.join(mand), 'KEYSETS': '\n'.join(keysets),
     'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'OVR': 'QAB39_', 'NROWS': str(len(ORDER)), 'NWORD': WORDS[len(ORDER)],
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
mand = re.findall(r'MANDATED SQUASH TEXT #(\d+) \(declared \d+, lands at \d+\): «(.*?)»', prompt, re.S)
if not mand: die('no MANDATED SQUASH TEXT block in the prompt — the key scan has nothing to measure')
for n, text in mand:
    ks = sorted(set(re.findall(r'KS-\d+', text))); own = K['prs'][n]['keys']
    if not ks or sorted(set(ks) - set(own)): die('KEY SCAN: mandated squash text for #%s carries %s (own %s)' % (n, ks, own))
    subj = text.split('\n')[0]
    if SUFFIX.search(subj.strip()) or len(subj) + len(' (#%s)' % n) > 92: die('SUBJECT SCAN: mandated subject for #%s %r carries a (#n) suffix or lands over 92 (%d)' % (n, subj, len(subj) + len(' (#%s)' % n)))
print('key scan: %d mandated squash text block(s), each carries only its own key: %s' % (len(mand), ', '.join('#%s %s' % (n, sorted(set(re.findall(r'KS-\d+', t)))) for n, t in mand)))
print('subject scan: every declared subject WITHOUT a (#n) suffix, landed length <= 92: %s' % ', '.join('#%s %d->%d' % (n, len(t.split('\n')[0]), len(t.split('\n')[0]) + len(' (#%s)' % n)) for n, t in mand))
if len(mand) != len(ORDER): die('the prompt carries %d MANDATED blocks, the kit %d rows' % (len(mand), len(ORDER)))
for path, text, mode in ((PROMPT_OUT, prompt, 0o644), (LAUNCH_OUT, launch, 0o755)):
    if os.path.exists(path) and open(path, encoding='utf-8').read() != text:
        shutil.copy2(path, path + '.pre-' + datetime.datetime.now().strftime('%H%M%S'))
    open(path, 'w', encoding='utf-8').write(text); os.chmod(path, mode)
r = subprocess.run(['bash', '-n', LAUNCH_OUT], capture_output=True, text=True)
if r.returncode != 0: die('bash -n on the launcher: %s' % r.stderr)
print('seat items %d (per line, both files) · keywords %d · kit rules %d · develop %s · END_TREE %s · prompt %d bytes · launcher bash -n rc 0'
      % (len(CFG['SEAT_ITEMS']), len(CFG['KEYWORDS']), len(CFG['RULES']), P['develop'], P['end_tree'], len(prompt.encode())))
print('wrote %s and %s' % (PROMPT_OUT, LAUNCH_OUT))
