#!/usr/bin/env python3
r"""fill_gate40.py — fill the gate40 kit's prompt + launcher templates from pins_<kit>.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home:
every path in the outputs is that directory). Re-reads origin develop and the head by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate40.py
first, never filled. Pre-checks every seat item (raw, per LINE, in BOTH the capture and the filled prompt — the launcher's grep is line-based), every
by-name keyword and every kit-rule phrase (in the whitespace-joined prompt) exactly as the launcher will, runs the round's KEY SCANNER over every
MANDATED squash text block of the prompt (a block may carry no hyphenated KS key but its own PR's), and runs `bash -n` on the launcher. Keeps any
previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
THE SUBJECT RULE (STANDING_LINES 2026-09-27, "a declared squash subject NEVER carries the `(#n)` suffix, and its length is checked as it will LAND"):
every MANDATED subject is DECLARED WITHOUT ` (#n)`; fill REFUSES a declared subject matching `\(#\d+\)$` and one whose len(declared) + len(" (#n)")
exceeds 92, and prints each subject's declared and landed lengths. gate40: #1338's title as the PULLS API returns it is 85 chars and LANDS AT 93
(gh_read_1.out) — OVER 92 — so SHORT carries the declared subject (the title with ", and" -> ";": 81 declared, lands at 89), and it must pass the key
scan and both length rules like any other.
Shape copied from gate39's fill (gate38 -> gate37 lineage); re-keyed to gate40's ONE row (T1), no stack, no sibling kit; the kit rules are the ten
requirements of Wednesday's commission, each by name (40-44, 46-50), plus the key scan, the addendum shape, the Linear links, the declaration keys,
the full disk (51-55) and no-Docker (35).
Usage: fill_gate40.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
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
if P.get('fail') != 0: die('pins carry fail=%s — predict_gate40.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('the pins are a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != ORDER: die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), ORDER))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']: die('origin develop %s != pinned %s — run predict_gate40.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
if P.get('stacks') or P.get('declared_overlap') or P.get('noop_paths'): die('the pins carry a stack / an overlap / a no-op declaration (%s / %s / %s) — gate40 declares none; re-draft' % (P.get('stacks'), P.get('declared_overlap'), P.get('noop_paths')))
print('fill (%s) at %s | home %s | origin agrees with the pins (develop %s, the %d heads)' % (KIT, now(), GS, P['develop'][:12], len(ORDER)))
SC = json.load(open(os.path.join(GS, 'stopcounts_%s.json' % KIT), encoding='utf-8'))

CFG = {
 'gate40': dict(
  TIERWORD='T1', TIER_DEF='T1 ROWS ARE GRADED THROUGH CODE AND AT RUNTIME',
  GO='`GO (Seat B 42nd): merge 1338 on gate40`', MERGE_AUTH='it is squashed by the merge seat Wednesday names for this GO',
  ADDENDUM_COUNT='PER PR FILE (3 over 3 paths) for #1338',
  SUBJECT='[QA -> Wednesday] GATE40 batch #1338 (Seat B42, round 40; T1: KS-1370 validate reads the stored revoke, both halves)',
  # #1338's title lands at 93 (gh_read_1.out): the declared subject below lands at 89; declared WITHOUT the (#n) suffix
  SHORT={'1338': 'KS-1370: validate answers on the stored revoke; its usage write cannot revive one'},
  SEAT_ITEMS=['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
              'Two module instances with separate CJS caches were driven, NOT two OS processes.',
              'The drill runs as `postgres` (`rolsuper=t`, `rolbypassrls=t`)',
              'Cell R2 of the KS 888 file is what caught this, and it now passes unchanged',
              'This is a defensive path, not a live one',
              'my FIRST green was vacuous',
              "V2's no-key/no-hash and one-error-line pins are unchanged",
              '5 declarations = 7 executed cases',
              'No pin was weakened.',
              "So half (ii)'s extra stored read fires",
              'at most once per key per 30 s, not once per request.',
              'Only 5 of the 9 new cells are red-first',
              'at the base tip (W1 V1 V2 D1 F1)',
              '26 files / 275 tests, 0 failed',
              '`tsc -p services/security` — rc 0',
              'product file restored byte-identical',
              'The four platform suites were not run: service-internal change, no OpenAPI surface change.',
              '`usage_count` written from a stale copy is a lost update.',
              'The log reports the ratio but does not name which three skipped.',
              'The ticket moved Backlog -> In Progress on its own',
              "narrowing validate's own call site is the change that leaves revoke intact"],
  KEYWORDS=['REAL-POSTGRES-DRILL', 'RED-AT-BASE', 'GREEN-AT-HEAD', 'NON-SUPERUSER-ROLE', 'CARVE-OUT-UNDER-FORCE-RLS', 'SUPERUSER-IS-BLIND', 'STICKY-BOTH-WAYS',
            'KS888-R2-UNCHANGED', 'VANISHED-ROW-EVICTED', 'VANISHED-ROW-RESURRECTED-AT-BASE', 'EACH-HALF-LOAD-BEARING', 'FAILED-READ-503', 'MEMORY-ONLY-FROM-MEMORY',
            'USAGE-WRITE-LOG-ONLY', 'NO-KEY-NO-HASH-IN-LOGS', 'V2-PINS-UNTOUCHED', 'USAGE-UPDATE-UNDER-RLS', 'SILENT-ZERO-ROW-UPDATE', 'EXECUTE-GRANT-SOURCE',
            'TWO-PROCESSES', 'THE-POSTGRES', 'REPIN-LINE-BY-LINE', 'WEAKENED-PIN-BLOCKER', 'CROSS-PACKAGE-GUARDS', 'KS764-GUARD-CALL-SITE', 'GATEWAY-REFUSAL-CACHE',
            'SECURITY-DB-FAULT-END-TO-END', 'LOST-UPDATE-CANDIDATE', 'SUBJECT-LANDS-AT', 'TITLE-LANDS-93', 'NOOP-VS-OVERLAP', 'NO-FOREIGN-KEY',
            'ADDENDUM-ONE-LINE-PER-PR', 'SECURITY-COUNTS', 'SHARED-COUNTS', 'TSC-EXCLUDES-TESTS', 'DISK-ENOSPC', 'TIER1-CAP-ROUND-1', 'TIERING'],
  RULES=[(40, ['THE REAL-POSTGRES DRILL (#1338; requirement 1', 'on a REAL PostgreSQL over a unix socket (no TCP listener, not Docker), RED at the base and GREEN at the head, with controls both ways', 'The gate re-derives, it does not trust'], 'requirement 1: the real-Postgres drill, RED at base / GREEN at head, controls both ways'),
         (41, ['THE STORED READ AS A NON-SUPERUSER APPLICATION ROLE (requirement 2', 'a NOSUPERUSER NOBYPASSRLS application role', 'A gate that repeats the superuser drill has not tested the premise'], 'requirement 2: the stored read as a non-superuser application role'),
         (42, ['THE TWO DESIGN CALLS, each with a DISCRIMINATING ARM (requirement 3', 'revoked if EITHER the in-memory copy or the stored row says revoked', 'KS-888 cell R2 must pass unchanged', 'a vanished row answers `Key not found` and evicts the cache entry'], 'requirement 3: both design calls, each with a discriminating arm'),
         (43, ["KAM'S SPLIT FOR A FAILED STORED READ (requirement 4", "a configured database whose read fails -> 503 'Unable to verify key'", 'memory-only mode (isDbAvailable false) answers from memory and still refuses an in-memory revoke'], "requirement 4: Kam's split for a failed stored read"),
         (44, ["KAM'S KS-888 RULING KEPT (requirement 5", 'a failed usage write is logged once, never refused, no key or hash in any log', "(#1334's V2 pins untouched)"], "requirement 5: Kam's KS-888 ruling kept"),
         (46, ["#1334's RE-PIN (requirement 6", 'the 5 declarations / 7 cases that changed are read LINE BY LINE and judged', 'Name any weakened pin as a BLOCKER'], "requirement 6: #1334's re-pin read line by line"),
         (47, ['CROSS-PACKAGE GUARDS (requirement 7', "`git grep -l '<changed path>' -- '*.test.ts'`", 'plus the packages/shared KS 764 revoke call-site guard, run in the gate'], 'requirement 7: the cross-package guards'),
         (48, ["THE GATEWAY'S 30 s REFUSAL CACHE (requirement 8", 'State what a security-DB fault now does END TO END'], "requirement 8: the gateway's 30 s refusal cache, end to end"),
         (49, ['TIER 1 AND THE TWO-NO-GO CAP (requirement 9', 'this is ROUND 1 for this class'], 'requirement 9: Tier 1 and the two-NO-GO cap, round 1'),
         (50, ['THE GO STRING AND THE SUBJECT (requirement 10', 'the squash subject is declared WITHOUT `(#n)` and checked as declared + " (#1338)" <= 92 chars', 'the key scanner over any mandated body'], 'requirement 10: the GO string, the subject rule, the key scanner'),
         (51, ['MG-3 KEY SCAN (measured by the drafter', 'the key scanner over every mandated body', 'index.ts carries foreign hyphenated keys as CONTENT'], 'the MG-3 key scan'),
         (52, ['THE ADDENDUM IS ONE LINE PER PR in exactly this shape', '- #NNNN · head <sha12> · subject: `<subject>`', 'NO sub-bullets'], 'the addendum one-line-per-PR shape'),
         (53, ['every PR links its ticket as `contributes`, none as `closes`'], 'the Linear link kinds'),
         (54, ['THE DECLARATION KEYS (NOOP-VS-OVERLAP;', '`merged_blob_paths` (a GENUINE overlap', '`noop_paths` (a squash-stack NO-OP'], 'the no-op vs overlap keys'),
         (55, ['DISK: /Volumes/DevMASTER is FULL', 'STOP on any ENOSPC', 'goes on the Data volume'], 'the full-disk rule: Data volume, STOP on ENOSPC'),
         (35, ['NO DOCKER, NO STACK, NO TCP PORT in this gate', 'NEVER connect to the native Postgres on :5432'], 'no Docker / no stack / no TCP port')]),
}[KIT]

def sq(s): return "'" + s.replace("'", "'\\''") + "'"
# MANDATED squash text per PR (subject + the one Refs line) and the MEASURED key sets the merger must know about. The title is READ from
# gh_body_<n>.md (written by gh_read_gate40.py from the PULLS API), never typed; a title whose `<title> (#n)` exceeds 92 is replaced by the kit's
# SHORT proposal (the gate rules on it). The KEY SCANNER below runs over every mandated block before anything is written.
KS = r'KS-\d+'
SUFFIX = re.compile(r'\(#\d+\)$')
mand, keysets, sublens, SUBJ = [], [], [], {}
for n in ORDER:
    gb = open(os.path.join(GS, 'gh_body_%s.md' % n), encoding='utf-8').read()
    title = gb.splitlines()[0].split(' ', 1)[1]; body = gb.split('\n', 3)[3] if gb.count('\n') >= 3 else ''
    if title != P['titles'][n]: die('#%s title in gh_body_%s.md %r != the title predict read from the API %r — re-read (gh_read_gate40.py)' % (n, n, title, P['titles'][n]))
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
PUSHLOG_NAMES = {'1338': 's-b42-ks1370-42f8a5abc65e-push.out'}
def stoprow(n):
    s = SC[n]
    if s.get('log') == 'ABSENT': return '#%s: NO PUSH LOG in the seat record at drafting (%s) — the gate reads it if the seat has written it since, and says so; otherwise UNREAD.' % (n, os.path.basename(PUSHLOG_NAMES.get(n, '?')))
    if not s.get('preflight_ran'): return '#%s %s (%s -> %s, rc %s): NO PREFLIGHT (a systemTest/ push: %d lines, the format gate only) — NOT APPLICABLE.' % (n, os.path.basename(s['log']), s['start'][:20], s['end'][:20], s['rc'], s['lines'])
    return '#%s %s (%s lines): `pre_push_hook_base` %s, fixture_guard %s, `run_shell_suites` %s (region) / %s (prefixed), shell suites %s;' % (
        n, os.path.basename(s['log']), s['lines'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['run_shell_suites_prefixed'], s['shell_suites'])
inf = '%d open PRs, each path-disjoint: ' % len(P['inflight']) + ', '.join('#%s@%s' % (n, v['head'][:12]) for n, v in sorted(P['inflight'].items(), key=lambda x: -int(x[0])))
if not inf: inf = 'NONE open at this pin besides the kit; predict_gate40.py re-censuses at every re-pin'
predict_out = sorted(f for f in os.listdir(GS) if re.match(r'predict_\d+\.out$', f))[-1]
V = {'GS': GS, 'KIT': KIT, 'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'END_TREE': P['end_tree'], 'END_WITH_SIB': str(P['end_tree_with_sibling']),
     'END_SHORTSTAT': P['end_shortstat'],
     'STACKS': ' '.join('%s:%s' % (c, p) for c, p in sorted(P['stacks'].items())), 'SUBJ_LENS': ', '.join(sublens), 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'PR_ROWS': '\n'.join(prrows), 'ORDERS': str(P['orders']),
     'BASES': '; '.join('%s for %s' % (b, ', '.join(v)) for b, v in bases.items()), 'INFLIGHT': inf,
     'PREDICT_OUT': predict_out, 'STOP_ROWS': ' '.join(stoprow(n) for n in ORDER),
     'MANDATED': '\n'.join(mand), 'KEYSETS': '\n'.join(keysets),
     'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'OVR': 'QAB40_', 'NROWS': str(len(ORDER)), 'NWORD': WORDS[len(ORDER)],
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
