#!/usr/bin/env python3
"""fill_gate48b.py — fill the gate48b prompt, launcher and COMMISSION.md from their templates, pins_gate48b.json and kit.json. TWO PRs, #1354 then #1355.
Refuses (rc 1) when: the pins are missing, a simulation, or not full shas; a pinned head is SUPERSEDED (kit.json superseded_heads — the ruled
#1354 head has not landed); a head's parent is not one kit.json allows; a pinned file list != kit.json's; the mode pins fail or cannot discriminate
(need both 100644 and 100755); an UNCHANGED pin is not byte-equal; gate48a's report no longer hashes to kit.json prev_report_sha256; a drafter
summary file (lockdelta_1.out, baseline_1.out, lockcensus_1.out, overlaps_1.out, image_read_1.out, keyscan_1.out, gh_read_1.out, capture_1.out)
does not end in its PASS / OK / DONE / READ line; lockdelta / baseline / lockcensus / overlaps were measured at other heads / END than the pins;
gh_read_1.out read other heads than the pins; an output keeps an unfilled {{TOKEN}}; or the filled prompt lacks a keyword AS A TOKEN (bounded by a
non-[A-Za-z0-9-] character). Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate48b.py"""
import json, os, re, sys, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate48b.json'), encoding='utf-8'))
ORDER = K['order']
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate48b.json is a SIMULATION (%s)' % P['simulate'])
for x in ('develop', 'develop_tree', 'end_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (x, P.get(x)))
for n in ORDER:
    p = P['prs'][n]; k = K['prs'][n]
    for x in ('head', 'merge_base', 'parent'):
        if not re.fullmatch(r'[0-9a-f]{40}', p.get(x) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (n, x))
    if p['head'] in (K.get('superseded_heads') or {}).get(n, []) or p.get('superseded'): raise SystemExit('REFUSING: #%s is pinned at a SUPERSEDED head %s — the ruled head has not landed' % (n, p['head']))
    if p['parent'] not in (k.get('expected_parent_any') or [k.get('expected_parent')]): raise SystemExit('REFUSING: #%s head parent %s is not an allowed parent' % (n, p['parent']))
    if sorted(p['files']) != sorted(k['files']): raise SystemExit('REFUSING: #%s pinned files != kit.json files' % n)
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']:
    raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate (need both 100644 and 100755)')
UN = P.get('unchanged') or {}
if not UN or not all(v['same'] for v in UN.values()): raise SystemExit('REFUSING: an UNCHANGED pin is not byte-equal: %s' % UN)
def txt(f): return open(os.path.join(G, f), encoding='utf-8').read()
def last(f, want):
    t = [l for l in txt(f).strip().splitlines() if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['ROW-PERMANENT-FIELDS', 'CONTRACT-LINE-ONLY', 'LOCK-DELTA-BOTH', 'UPDATE-VERB-CORRECTION', 'AUDIT-LEGS-HEAD-END', 'NO-BASELINE-ROW', 'ISSUER-IMAGE', 'SUITES',
      'UNDICI-MAJOR-RUNTIME', 'ROOT-LOCK-CONSUMERS', 'PUSH-PREFLIGHT', 'FOLLOW-ONS', 'FUSE-COUNT',
      'CLEAN-MERGE', 'END-TREE', 'MODES', 'OUT-OF-KIT-CENSUS',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'SUBJECT-TRUE-OF-DIFF', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD', 'PR-BODY-CLAIMS',
      'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
GHJ = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))
for n in ORDER:
    if GHJ['prs'][n]['head'] != P['prs'][n]['head']: raise SystemExit('REFUSING: gh_read_1.json read #%s at %s, the pin is %s — re-run gh_read' % (n, GHJ['prs'][n]['head'][:12], P['prs'][n]['head'][:12]))
def subj(n): return K['prs'][n].get('subject') or GHJ['prs'][n]['title']
rows, trows, srows = [], [], []
for n in ORDER:
    p = P['prs'][n]; k = K['prs'][n]; files = sorted(p['files'])
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), k['branch'], p['head'], len(files), p['ahead'], p['merge_base'], p['behind'], ','.join(files), k['tier']))
    trows.append('| #%s | %s | %s | `%s` | `%s` | `%s` | %d / %d | %d (%s) | %d -> %d |' % (n, ' + '.join(k['keys']), k['tier'], p['head'], p['parent'][:12], p['merge_base'][:12], p['ahead'], p['behind'], len(files),
                 '; '.join(x.replace('\t', ' ') for x in p['numstat']), len(subj(n)), len(subj(n)) + len(' (#%s)' % n)))
    srows.append('- #%s: `%s` — declared %d, lands %d (%s)' % (n, subj(n), len(subj(n)), len(subj(n)) + len(' (#%s)' % n), 'the LIVE PR title as read at the pin (gh_read_1.json)' + (', == the commit subject' if p['subject_commit'] == GHJ['prs'][n]['title'] else ', != the commit subject %r' % p['subject_commit'])))
table = '\n'.join(['| PR | ticket | tier | head | parent | merge-base | ahead / behind develop | files | declared subject -> lands |', '|---|---|---|---|---|---|---|---|---|'] + trows)
MODE_LINE = 'Recorded modes (pin (H), `git ls-tree`): %d PR path(s) all 100644 and OK at head / alone / chain step / END; CONTROL `.githooks/pre-push` 100755 at develop / both heads / END (not a PR path: the instrument reads a second value in the same run).' % sum(not m['control'] for m in MS)
HK = P.get('hooks') or {}
HOOK_LINE = 'THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT, THE AUDIT LEGS, THE ISSUER DOCKERFILE (pin (I), (K)): ' + '; '.join('%s %s %s (%s)' % (x.split('/')[-1], v['develop'][0], v['develop'][1][:12], 'IDENTICAL in every tree' if len(set(tuple(y) if y else None for y in v.values())) == 1 else 'DIFFERS between trees — the contract, by #1354' ) for x, v in HK.items()) + '.'
ALONE_LINE = 'Each PR ALONE over develop (pin (E)): ' + '; '.join('#%s merge-tree clean, tree `%s`' % (n, P['prs'][n]['alone_tree']) for n in ORDER) + '.'
CH = P['chain']
CHAIN_LINE = 'in order ' + ' -> '.join('#%s on %s clean (squash %s, tree %s%s)' % (st['pr'], ('develop' if i == 0 else '#%s\'s squash' % CH[i - 1]['pr']), st['squash_sim'][:12], st['tree'][:12], (', NO-OP: %s' % ', '.join(st['noop'])) if st['noop'] else '') for i, st in enumerate(CH)) + ';'
import subprocess
SHORTSTAT = [l for l in txt('pin_1.out').splitlines() if 'git diff --shortstat develop END' in l][-1].split(': ', 1)[1]
prev = K['prev_report']; prev_sha = hashlib.sha256(open(prev, 'rb').read()).hexdigest()
if prev_sha != K['prev_report_sha256']: raise SystemExit('REFUSING: gate48a report sha256 %s != kit %s' % (prev_sha, K['prev_report_sha256']))
LD = last('lockdelta_1.out', 'LOCKDELTA PASS'); BL = last('baseline_1.out', 'BASELINE PASS'); LC = last('lockcensus_1.out', 'CENSUS DONE')
OV = last('overlaps_1.out', 'OVERLAPS READ'); IR = last('image_read_1.out', 'IMAGE READ OK'); KS = last('keyscan_1.out', 'KEYSCAN PASS')
h1 = txt('lockdelta_1.out').splitlines()[0]
if ('base %s' % P['develop'][:12]) not in h1 or ('head %s' % P['prs']['1355']['head'][:12]) not in h1: raise SystemExit('REFUSING: lockdelta_1.out was measured at another develop / #1355 head — re-run it')
h2 = txt('baseline_1.out').splitlines()[0]
if ('#1354 head %s' % P['prs']['1354']['head'][:12]) not in h2 or ('END %s' % P['end_tree'][:12]) not in h2 or 'CONTROL SUBJECT' in h2: raise SystemExit('REFUSING: baseline_1.out was measured at another #1354 head / END — re-run it')
if P['end_tree'] not in txt('lockcensus_1.out').splitlines()[0]: raise SystemExit('REFUSING: lockcensus_1.out was measured at another tree than END — re-run it')
if ('squash_sim %s' % P['squash_sim'][:12]) not in txt('overlaps_1.out').splitlines()[0]: raise SystemExit('REFUSING: overlaps_1.out was measured over another squash chain — re-run it')
vl = [l.strip() for l in txt('lockcensus_1.out').splitlines() if l.strip().startswith('VULNERABLE entries:')]
LOCKCENSUS = '%s; %s' % (LC, vl[0][:200] if vl else 'no VULNERABLE line')
GH = txt('gh_read_1.out'); last('gh_read_1.out', 'GH READ OK')
cl = [l for l in GH.splitlines() if l.startswith('CENSUS ')]
CENSUS_LINE = (cl[-1] if cl else 'no CENSUS line') + ' (at %s; the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)' % last('gh_read_1.out', 'GH READ OK').split(' at ')[-1]
CAP = last('capture_1.out', 'CAPTURE OK'); ct = txt('capture_1.out')
CAPTURE_LINE = 'the READY and the seat\'s thread read by id, verbatim, with TEXT_SHA256; Kam\'s card ruling from decisions.json; any LATE mail on #1354\'s new head; Wednesday\'s four ANSWER files (%s; %s).' % (
    ' | '.join(l.strip() for l in ct.splitlines() if l.startswith(('READY as captured', 'KAM RULING', 'LATE mails'))), CAP)
rr = txt('row_reason_gate48b.md'); m = re.search(r'reason sha256 ([0-9a-f]{64})', rr)
if not m: raise SystemExit('REFUSING: row_reason_gate48b.md carries no reason sha256')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
h4, h5 = P['prs']['1354']['head'], P['prs']['1355']['head']
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'END_TREE': P['end_tree'], 'MEASURED_AT': P['measured_at'],
     'FILLED_AT': now, 'PIN_TABLE': table, 'ROWS': '\n'.join(rows), 'SUBJECT_TABLE': '\n'.join(srows), 'H': h5, 'H_SHORT': h5[:12], 'H_1355': h5, 'H_1354': h4, 'H_1354_SHORT': h4[:12],
     'MODE_LINE': MODE_LINE, 'HOOK_LINE': HOOK_LINE, 'ALONE_LINE': ALONE_LINE, 'CHAIN_LINE': CHAIN_LINE, 'SHORTSTAT': SHORTSTAT, 'CAPTURE_LINE': CAPTURE_LINE, 'REASON_SHA': m.group(1),
     'LOCKDELTA': LD, 'BASELINE': BL, 'LOCKCENSUS': LOCKCENSUS, 'OVERLAPS': OV, 'IMAGE_READ': IR, 'CENSUS_LINE': CENSUS_LINE,
     'KEYSCAN': KS, 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)), 'PREV_REPORT': prev, 'PREV_SHA': prev_sha,
     'VERDICT_SUBJECT': '[QA -> Wednesday] GATE48B #1354 #1355 (Seat B48 merger, round 48b; T2 KS-470 r53p permanent on Kam ruling (c), then T1 KS-1378 undici 7.30.0 override + js-yaml 5.4.2)'}
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for a, v in V.items(): t = t.replace('{{%s}}' % a, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    with open(os.path.join(G, dst), 'w', encoding='utf-8') as f: f.write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes)' % (dst, len(t.encode('utf-8'))))
fill('prompt_gate48b.TEMPLATE.txt', K['prompt']); fill('launcher_gate48b.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = txt(K['prompt'])
missing = [w for w in KW if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), pt)]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) as a token %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | 2 rows | %d keywords | #1354 %s | #1355 %s | gate48a report sha256 %s' % (now, P['develop'], P['end_tree'], len(KW), h4[:12], h5[:12], prev_sha[:12]))
