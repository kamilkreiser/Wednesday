#!/usr/bin/env python3
r"""fill_gate42.py — fill the gate42 kit's prompt + launcher templates from pins_<kit>.json, IN THE DIRECTORY THIS SCRIPT LIVES IN (the kit's home:
every path in the outputs is that directory). Re-reads origin develop and the head by `git ls-remote` (READ verb, from the Secuura checkout) and
REFUSES (rc 1) if they disagree with the pins, if the pins are a SIMULATION or carry a FAIL — a stale pin is re-measured with predict_gate42.py
first, never filled. Pre-checks every seat item (raw, per LINE, in BOTH the capture and the filled prompt — the launcher's grep is line-based), every
by-name keyword and every kit-rule phrase (in the whitespace-joined prompt) exactly as the launcher will, runs the round's KEY SCANNER over every
MANDATED squash text block of the prompt (a block may carry no hyphenated KS key but its own PR's), and runs `bash -n` on the launcher. Keeps any
previous output that differs as <name>.pre-<HHMMSS>. Writes nothing outside its own directory.
THE SUBJECT RULE (STANDING_LINES 2026-09-27, "a declared squash subject NEVER carries the `(#n)` suffix, and its length is checked as it will LAND"):
every MANDATED subject is DECLARED EXPLICITLY (gate42: fill REFUSES a row with no SHORT entry — a subject is declared, never defaulted) and WITHOUT
` (#n)`; fill REFUSES a declared subject matching `\(#\d+\)$` and one whose len(declared) + len(" (#n)") exceeds 92, and prints each subject's declared
and landed lengths. gate42: #1339's title as the PULLS API returns it is 75 chars and lands at 83 (gh_read_1.out); SHORT declares it verbatim (Wednesday's
Q5: title and Refs unchanged for round 2). The mandated body carries ONE `Refs` line per own key (Refs KS-1378, Refs KS-729 — the PR body's two Refs lines;
both commit messages carry only the first).
Shape copied from gate41's fill (gate40 -> gate39 lineage); re-keyed to gate42's ONE row (T1, ROUND 2 OF 2), no stack, no sibling kit; the kit rules are
the seven requirements of Wednesday's gate42 commission, each by name (40-44, 46-47), the prior round's findings re-checked (48, gate41 lineage), the lock-touched suites (49), the
call-site sink at the head (50), plus the key scan, the addendum shape, the Linear links, the declaration keys, the disk rule (51-55) and no-Docker /
npm-only egress (35). Three fill tokens are MEASURED, never typed: {{CENSUS}} (predict's census from the pins), {{IPSUM}} (installprobe_gate42.json's
summary) and {{REPORT}} (kit.json `report`).
Usage: fill_gate42.py [<scratchpad>]   (the argument is accepted for the repin script's calling convention and unused)
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
if P.get('fail') != 0: die('pins carry fail=%s — predict_gate42.py did not pass' % P.get('fail'))
if P.get('simulation') != 'none': die('the pins are a SIMULATION (%s) — never fill from a simulated develop' % P.get('simulation'))
if sorted(P['prs']) != ORDER: die('the pins carry PRs %s, the kit is frozen at %s' % (sorted(P['prs']), ORDER))
refs = ['refs/heads/develop'] + ['refs/pull/%s/head' % n for n in ORDER] + [P['prs'][n]['branch'] for n in ORDER]
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin'] + refs, capture_output=True, text=True)
if ls.returncode != 0: die('ls-remote rc %d: %s' % (ls.returncode, ls.stderr.strip()))
L = {l.split('\t')[1]: l.split('\t')[0] for l in ls.stdout.strip().splitlines()}
if L.get('refs/heads/develop') != P['develop']: die('origin develop %s != pinned %s — run predict_gate42.py first' % (L.get('refs/heads/develop'), P['develop']))
for n in ORDER:
    pr = P['prs'][n]
    if not (L.get('refs/pull/%s/head' % n) == L.get(pr['branch']) == pr['head']):
        die('#%s head moved: pull %s, branch %s, pinned %s — a new head needs a re-capture and a re-draft' % (n, L.get('refs/pull/%s/head' % n), L.get(pr['branch']), pr['head']))
if P.get('stacks') or P.get('declared_overlap') or P.get('noop_paths'): die('the pins carry a stack / an overlap / a no-op declaration (%s / %s / %s) — gate42 declares none; re-draft' % (P.get('stacks'), P.get('declared_overlap'), P.get('noop_paths')))
print('fill (%s) at %s | home %s | origin agrees with the pins (develop %s, the %d heads)' % (KIT, now(), GS, P['develop'][:12], len(ORDER)))
SC = json.load(open(os.path.join(GS, 'stopcounts_%s.json' % KIT), encoding='utf-8'))

CFG = {
 'gate42': dict(
  TIERWORD='T1', TIER_DEF='T1 ROWS ARE GRADED THROUGH CODE AND AT RUNTIME',
  GO='`GO (Seat B 44th): merge 1339 on gate42`', MERGE_AUTH='it is squashed by the merge seat Wednesday names for this GO',
  ADDENDUM_COUNT='PER PR FILE (30 over 30 paths) for #1339',
  SUBJECT='[QA -> Wednesday] GATE42 batch #1339 round 2 (Seat B44, round 42; T1: KS-1378 the four-package advisory bump, round 2 of 2 - the LAST round)',
  # #1339's title lands at 83 (gh_read_1.out): declared EXPLICITLY (gate42's fill refuses a row with no declared subject), WITHOUT the (#n) suffix
  SHORT={'1339': 'KS-1378: bump morgan, nodemailer, ip-address and undici off five advisories'},
  SEAT_ITEMS=['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
              'legs 3 4 8 — local stack not up; you can clear this by starting it.',
              'audit-gate: 23 distinct advisories reported, 25 baselined.',
              'OK — no advisories outside the triaged baseline.',
              'OK — no standalone-lock advisories outside the triaged baseline.',
              '2 baseline entries are no longer reported — remove:',
              '77 files / 836 tests, ALL PASS, rc 0',
              '89 suites / 1058 tests, ALL PASS, rc 0',
              '2 suites / 11 tests failed, 87 / 1047 passed, rc 1',
              'the import removed, annotations kept:',
              'the annotations reverted, import kept:',
              'The auth suite is GREEN on the PRE-FIX file (77 / 836).',
              'host `npm ci` WORKS on this machine.',
              'is `npm install` (npm 11.5.1, `edgesOut`), not `npm ci`.',
              'N-1339-2 is TICKETED: KS 1379',
              'mobile `undici@6.28.0` is inside GHSA-3wwx-pv8p-q78v and is out of scope (mobile tree, KS 769).',
              'This commit edits no baseline row.',
              'nodemailer 10.0.12 · morgan 1.12.1 · ip-address 10.7.2 · @types/nodemailer 8.0.1',
              'Every VALUE use of `nodemailer` is untouched',
              'I passed `--no-verify` to `git commit`.',
              '19.8 h, computed 2026-09-29T04:09:23Z',
              '1937 packages in 29 s',
              "src/services/email.ts(73,18): error TS2503: Cannot find namespace 'nodemailer'.",
              "`export type { SendMailOptions, Transporter } from './mailer/index.js';` — a TYPE.",
              "Kam's four ids cover EVERY row at the fuse"],
  KEYWORDS=['CLEAN-INSTALL-NODEMAILER-10', 'TSC-AUTH-ON-10', 'TSC-ORIGINATE-ON-10', 'DOCKERFILE-BUILD-PATH', 'AUTH-SUITE-ON-10', 'ORIGINATE-SUITE-IS-JEST', 'N-1339-1-CLOSED',
            'LEGS-6-7-RED-AT-BASE', 'LEGS-6-7-GREEN-AT-HEAD', 'BASELINE-BYTE-IDENTICAL', 'MORGAN-QUOTE-ESCAPED', 'UNDICI-SCOPED-TO-JSDOM', 'IP-ADDRESS-NO-9X', 'AUDIT-LEG-6', 'AUDIT-LEG-7',
            'CLEANUP-ROWS-NAMED', 'OUT-OF-SCOPE-LOCKS', 'RUNTIME-MOVED-QUEUE-MSGPACKR-2', 'RUNTIME-MOVED-MSAL-NODE-6', 'STANDALONE-SUITES-RUNTIME-MOVED', 'KS-1379-CONDITION',
            'ROUND2-DIFF-LINE-BY-LINE', 'ROUND2-NO-SCOPE-CREEP', 'VALUE-USES-UNCHANGED', 'TYPE-ONLY-IMPORT-ELIDED', 'NODEMAILER-CHANGELOG-9-TO-10', 'CALL-SITES-PER-SERVICE', 'ESM-CJS-DUAL-BUILD',
            'TEST-FILES-BY-PATH', 'EMAIL-IMPORTERS-RUN', 'CROSS-PACKAGE-GUARDS', 'LOCK-DISCOVERY-CONTRACT', 'LOCK-SUITES-BEFORE-AFTER', 'DECLARED-OPEN-OVERLAPS',
            'GO-STRING-SEAT-B-44TH', 'SUBJECT-LANDS-AT', 'REFS-TWO-KEYS', 'MERGE-ORDER-1339-FIRST', 'REDATE-PR-OUT-OF-KIT', 'NOOP-VS-OVERLAP', 'NO-FOREIGN-KEY', 'ADDENDUM-ONE-LINE-PER-PR',
            'GATE41-FINDINGS-RECHECKED', 'TSC-EXCLUDES-TESTS', 'AUDIT-FUSE', 'DISK-ENOSPC', 'TIER1-CAP-ROUND-2', 'LAST-ROUND', 'TIERING'],
  RULES=[(40, ['A CLEAN INSTALL, tsc ON auth AND originate, AND BOTH SUITES ON NODEMAILER 10 (requirement 1', 'a clean `npm ci` per affected lock, never an incremental install', 'ON THE DOCKERFILE BUILD PATH', 'with the runner its package.json names — JEST'], 'requirement 1: a clean install resolving nodemailer 10, tsc rc 0 on auth AND originate on the Dockerfile build path, both suites'),
         (41, ['EVERYTHING THAT HELD IN gate41 STILL HOLDS (requirement 2', 'at the BASE (RED: the five NEW advisories', "must be BYTE-IDENTICAL to develop's"], 'requirement 2: everything that held in the prior round still holds (legs 6-7 red at base / green at head, baseline byte-identical)'),
         (42, ['THE RUNTIME-MOVED SERVICES, STANDALONE (requirement 3', "get a clean STANDALONE `npm ci` plus that service's OWN suite in THIS gate", "run each workspace's OWN suite IN that standalone install"], 'requirement 3: clean standalone installs + suites for the runtime-moved services (queue, m365 / shared)'),
         (43, ['THE ROUND-2 DIFF, LINE BY LINE AGAINST N-1339-1 (requirement 4', "WHOLE, every line, against gate41's N-1339-1"], 'requirement 4: the round-2 diff read line by line against N-1339-1'),
         (44, ['EVERY TEST FILE THAT REFERENCES A CHANGED PATH (requirement 5', "`git grep -l '<path>' -- '*.test.ts' '*.test.js'` over the WHOLE monorepo", 'Run EVERY one so named'], 'requirement 5: every test file that references a changed path is run'),
         (46, ['THE GO STRING, THE SUBJECT AND THE MERGE ORDER (requirement 6', 'MERGE ORDER: #1339 ALONE, and it merges FIRST', 'The re-date PR is NOT in this kit'], 'requirement 6: the GO string, the subject rule, the merge order (#1339 first)'),
         (47, ['TIER 1, ROUND 2 OF 2 — THE LAST ROUND (requirement 7', 'this is ROUND 2 OF 2 for this class', 'A NO GO here is the SECOND'], 'requirement 7: Tier 1, round 2 of 2, the last round'),
         (48, ['EVERY gate41 FINDING, RE-CHECKED (GATE41-FINDINGS-RECHECKED', 'Each: CLOSED / STILL OPEN / NEW'], 'every finding of the prior round re-checked'),
         (49, ['EVERY SUITE TOUCHED BY A CHANGED LOCKFILE (LOCK-SUITES-BEFORE-AFTER', 'with before/after counts', 'A lock change can break a service without touching its code'], 'every suite a changed lock touches, before/after counts'),
         (50, ['NODEMAILER 9 -> 10 AT THE CALL SITES (NODEMAILER-CHANGELOG-9-TO-10', 're-drive the sink ONCE per service at the head through the tsc-EMITTED JS'], 'the call sites driven on nodemailer 10 through the emitted JS'),
         (51, ['MG-3 KEY SCAN (measured by the drafter', 'the key scanner over every mandated body', 'the audit tool prints advisory keys and ticket keys hyphenated'], 'the MG-3 key scan'),
         (52, ['THE ADDENDUM IS ONE LINE PER PR in exactly this shape', '- #NNNN · head <sha12> · subject: `<subject>`', 'NO sub-bullets'], 'the addendum one-line-per-PR shape'),
         (53, ['every PR links its ticket as `contributes`, none as `closes`'], 'the Linear link kinds'),
         (54, ['THE DECLARATION KEYS (NOOP-VS-OVERLAP;', '`merged_blob_paths` (a GENUINE overlap', '`noop_paths` (a squash-stack NO-OP'], 'the no-op vs overlap keys'),
         (55, ['DISK: every clone, worktree, install and build goes on the Data volume', 'STOP on any ENOSPC', 'never under /Volumes/DevMASTER'], 'the disk rule: Data volume, STOP on ENOSPC'),
         (35, ['NO DOCKER, NO STACK, NO TCP LISTENER beyond 127.0.0.1 port 0 in this gate', 'the ONLY outbound requests are the npm registry and the npm advisory API'], 'no Docker / no stack / npm-only egress')]),
}[KIT]

def sq(s): return "'" + s.replace("'", "'\\''") + "'"
# MANDATED squash text per PR (subject + the one Refs line) and the MEASURED key sets the merger must know about. The title is READ from
# gh_body_<n>.md (written by gh_read_gate42.py from the PULLS API), never typed; a title whose `<title> (#n)` exceeds 92 is replaced by the kit's
# SHORT proposal (the gate rules on it). The KEY SCANNER below runs over every mandated block before anything is written.
KS = r'KS-\d+'
SUFFIX = re.compile(r'\(#\d+\)$')
mand, keysets, sublens, SUBJ = [], [], [], {}
for n in ORDER:
    gb = open(os.path.join(GS, 'gh_body_%s.md' % n), encoding='utf-8').read()
    title = gb.splitlines()[0].split(' ', 1)[1]; body = gb.split('\n', 3)[3] if gb.count('\n') >= 3 else ''
    if title != P['titles'][n]: die('#%s title in gh_body_%s.md %r != the title predict read from the API %r — re-read (gh_read_gate42.py)' % (n, n, title, P['titles'][n]))
    own = K['prs'][n]['keys']
    short = CFG.get('SHORT', {}).get(n)
    if not short: die('#%s has NO declared subject (SHORT) — gate42 declares every subject explicitly; the title as read (%d chars, lands at %d) is never defaulted' % (n, len(title), len(title) + len(' (#%s)' % n)))
    decl = short
    lands = len(decl) + len(' (#%s)' % n)
    if SUFFIX.search(decl.strip()): die('#%s declared subject %r ENDS IN a (#n) suffix — GitHub appends it; declare it WITHOUT (STANDING_LINES 2026-09-27)' % (n, decl))
    if lands > 92:
        die('#%s declared subject %r lands at %d chars (declared %d + " (#%s)" %d) > 92 and the kit has no SHORT subject for it' % (n, decl, lands, len(decl), n, len(' (#%s)' % n)))
    SUBJ[n] = decl
    mand.append('MANDATED SQUASH TEXT #%s (declared %d, lands at %d): «%s\n\n%s»' % (n, len(decl), lands, decl, '\n'.join('Refs ' + k for k in own)))
    bk = sorted(set(re.findall(KS, body))); mk = P['prs'][n]['msg_keys']
    foreign = sorted((set(bk) | set(mk)) - set(own))
    tl = len(title) + len(' (#%s)' % n)
    keysets.append('#%s: own %s | PR body carries %s | its %d commit message(s) carry %s | FOREIGN keys the squash body must un-hyphenate: %s%s' % (
        n, own, bk, len(P['prs'][n]['commits']), mk, [f.replace('KS-', 'KS') for f in foreign] or 'none',
        ' | the PR title as read lands at %d chars; the declared subject %s the title (declared %d, lands at %d)' % (tl, 'EQUALS' if decl == title else 'DIFFERS FROM', len(decl), lands)))
    sublens.append('#%s declared %d / lands at %d%s' % (n, len(decl), lands, ' (== the PR title as read)' if decl == title else (' (the title would land at %d)' % tl)))
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
PUSHLOG_NAMES = {'1339': 'push.out'}
def stoprow(n):
    s = SC[n]
    if s.get('log') == 'ABSENT': return '#%s: NO PUSH LOG in the seat record at drafting (%s) — the gate reads it if the seat has written it since, and says so; otherwise UNREAD.' % (n, os.path.basename(PUSHLOG_NAMES.get(n, '?')))
    if not s.get('preflight_ran'): return '#%s %s (%s -> %s, rc %s): NO PREFLIGHT (a systemTest/ push: %d lines, the format gate only) — NOT APPLICABLE.' % (n, os.path.basename(s['log']), s['start'][:20], s['end'][:20], s['rc'], s['lines'])
    return '#%s %s (%s lines): `pre_push_hook_base` %s, fixture_guard %s, `run_shell_suites` %s (region) / %s (prefixed), shell suites %s;' % (
        n, os.path.basename(s['log']), s['lines'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['run_shell_suites_prefixed'], s['shell_suites'])
inf = '%d open PRs, each path-disjoint: ' % len(P['inflight']) + ', '.join('#%s@%s' % (n, v['head'][:12]) for n, v in sorted(P['inflight'].items(), key=lambda x: -int(x[0])))
if not inf: inf = 'NONE open at this pin besides the kit; predict_gate42.py re-censuses at every re-pin'
predict_out = sorted(f for f in os.listdir(GS) if re.match(r'predict_\d+\.out$', f))[-1]
# MEASURED fill tokens: the census from the pins (predict (e)), the install-probe summary from installprobe_<kit>.json — never typed
CZ = P['measured'][ORDER[0]]['census']
rp = lambda x: x[len('Blockchain/Dev/'):] if x.startswith('Blockchain/Dev/') else x   # repo paths, Blockchain/Dev/ elided (systemTest/ etc. stay whole)
census = '(paths under Blockchain/Dev/ unless they start systemTest/ or another repo root) by exact path %s; naming any package-lock.json %s; importing email.ts by its module spelling `services/email` — auth (%d): %s; originate (%d): %s' % (
    {k: [rp(x) for x in v] for k, v in CZ['exact'].items()} or 'NONE', [rp(x) for x in CZ['broad']],
    len(CZ['email_importers']['services/auth']), [rp(x) for x in CZ['email_importers']['services/auth']],
    len(CZ['email_importers']['services/originate']), [rp(x) for x in CZ['email_importers']['services/originate']])
IPJ = json.load(open(os.path.join(GS, 'installprobe_%s.json' % KIT), encoding='utf-8'))
if not all(IPJ.get('controls', {}).values()): die('installprobe_%s.json controls are not ALL PASS — re-run installprobe_%s.py before filling' % (KIT, KIT))
IS = IPJ['_summary']
ipsum = 'installprobe_%s.json, npm %s / node %s, controls %d/%d PASS: Dockerfile build path %s; runtime-moved standalone suites %s; moved copies base -> head: queue msgpackr %s -> %s, m365 identity-nested msal-node %s -> %s, shared msal-node %s -> %s' % (
    KIT, IPJ['npm'], IPJ['node'], sum(IPJ['controls'].values()), len(IPJ['controls']),
    {k: 'rc %s / %s err' % (v['build_rc'], v['n_errors']) for k, v in IS['tsc'].items()},
    {k: (v['summary'] or ['rc %s' % v['rc']]) for k, v in IS['standalone_suites'].items()},
    [v for p_, v in IS['runtime_copies']['base_queue'] if p_.endswith('/msgpackr')], [v for p_, v in IS['runtime_copies']['head_queue'] if p_.endswith('/msgpackr')],
    [v for p_, v in IS['runtime_copies']['base_m365-integration'] if p_.endswith('identity/node_modules/@azure/msal-node')], [v for p_, v in IS['runtime_copies']['head_m365-integration'] if p_.endswith('identity/node_modules/@azure/msal-node')],
    [v for p_, v in IS['runtime_copies']['base_shared'] if p_.endswith('/@azure/msal-node')], [v for p_, v in IS['runtime_copies']['head_shared'] if p_.endswith('/@azure/msal-node')])
V = {'GS': GS, 'KIT': KIT, 'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'END_TREE': P['end_tree'], 'END_WITH_SIB': str(P['end_tree_with_sibling']),
     'END_SHORTSTAT': P['end_shortstat'],
     'STACKS': ' '.join('%s:%s' % (c, p) for c, p in sorted(P['stacks'].items())), 'SUBJ_LENS': ', '.join(sublens), 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now(), 'PR_ROWS': '\n'.join(prrows), 'ORDERS': str(P['orders']),
     'BASES': '; '.join('%s for %s' % (b, ', '.join(v)) for b, v in bases.items()), 'INFLIGHT': inf,
     'PREDICT_OUT': predict_out, 'STOP_ROWS': ' '.join(stoprow(n) for n in ORDER), 'REPORT': K['report'], 'CENSUS': census, 'IPSUM': ipsum,
     'MANDATED': '\n'.join(mand), 'KEYSETS': '\n'.join(keysets),
     'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'OVR': 'QAB42_', 'NROWS': str(len(ORDER)), 'NWORD': WORDS[len(ORDER)],
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
