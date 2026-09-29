#!/usr/bin/env python3
"""fill_gate48a.py — fill the gate48a prompt, launcher and COMMISSION.md from their templates, pins_gate48a.json and kit.json.
Refuses (rc 1) when: the pins are missing, a simulation, or not full shas; the head's parent is not kit.json's expected_parent; the pinned file
list != kit.json's; the mode pins fail or cannot discriminate (need both 100644 and 100755 in the pin set); an UNCHANGED pin (baseline-contract.mjs)
is not byte-equal; gate47's report no longer hashes to the sha256 in Wednesday's gate47 GO (kit.json prev_report_sha256); a drafter summary file
(keyscan_1.out, lockdiff_1.out, baseline_1.out, lockcensus_1.out, gh_read_1.out, capture_1.out, drafts_1.out) does not end in its PASS / OK / DONE
line; lockdiff_1.out or baseline_1.out was measured at another develop / head than the pins; an output keeps an unfilled {{TOKEN}}; or the filled
prompt lacks a keyword AS A TOKEN (bounded by a non-[A-Za-z0-9-] character, so `MODES` is not satisfied by `MODES-X`).
Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate48a.py"""
import json, os, re, sys, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate48a.json'), encoding='utf-8'))
ORDER = K['order']; N = ORDER[0]
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate48a.json is a SIMULATION (%s)' % P['simulate'])
for x in ('develop', 'develop_tree', 'end_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (x, P.get(x)))
p = P['prs'][N]; k = K['prs'][N]
for x in ('head', 'merge_base', 'parent'):
    if not re.fullmatch(r'[0-9a-f]{40}', p.get(x) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (N, x))
if p['parent'] != k['expected_parent']: raise SystemExit('REFUSING: #%s head parent %s is not the expected %s' % (N, p['parent'], k['expected_parent']))
if sorted(p['files']) != sorted(k['files']): raise SystemExit('REFUSING: #%s pinned files != kit.json files' % N)
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']:
    raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate (need both 100644 and 100755): %s' % MS)
UN = P.get('unchanged') or {}
if not UN or not all(v['same'] for v in UN.values()): raise SystemExit('REFUSING: an UNCHANGED pin is not byte-equal at develop / head / END: %s' % UN)
def last(f, want):
    t = open(os.path.join(G, f), encoding='utf-8').read().strip().splitlines()
    t = [l for l in t if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['LOCK-DIFF-ONE-ENTRY', 'JSYAML-OUT-OF-RANGE', 'BASELINE-ROW-FIELDS', 'CONTRACT-BYTE-EQUAL', 'FUSE-COUNT', 'AUDIT-GATES-HEAD-END',
      'CLAUSE2-REMEASURE', 'EXCEPTION-CHECKED', 'GRANT-CLAUSES', 'REASON-TEXT-TRUE', 'DRAFTED-TICKETS-CHECKED',
      'CLEAN-MERGE', 'END-TREE', 'MODES', 'OUT-OF-KIT-CENSUS',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'SUBJECT-TRUE-OF-DIFF', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD', 'PR-BODY-CLAIMS',
      'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
files = sorted(p['files'])
row = '  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (N, ' + '.join(k['keys']), k['branch'], p['head'], len(files), p['ahead'], p['merge_base'], p['behind'], ','.join(files), k['tier'])
table = '\n'.join(['| PR | ticket | tier | head | parent | merge-base | ahead / behind develop | files | declared subject -> lands |', '|---|---|---|---|---|---|---|---|---|',
                   '| #%s | %s | %s | `%s` | `%s` | `%s` | %d / %d | %d (%s) | %d -> %d |' % (N, ' + '.join(k['keys']), k['tier'], p['head'], p['parent'][:12], p['merge_base'][:12], p['ahead'], p['behind'], len(files),
                   '; '.join(x.replace('\t', ' ') for x in p['numstat']), len(k['subject']), len(k['subject']) + len(' (#%s)' % N))])
subj = '- #%s: `%s` — declared %d, lands %d (%s)' % (N, k['subject'], len(k['subject']), len(k['subject']) + len(' (#%s)' % N), 'the PR title verbatim, == the commit subject' if k['subject'] == k['title'] else 'the DRAFTER PROPOSAL, not the PR title')
MODE_LINE = 'Recorded modes (pin (H), `git ls-tree`): ' + '; '.join('%s %s %s%s' % ('#' + m['pr'] if not m['control'] else 'CONTROL', m['path'].split('/')[-1], m['want'], ' (not a PR path: the instrument reads a second value in the same run)' if m['control'] else '') for m in MS) + ' — all %d OK at head / alone / END (the control at develop / head / END).' % len(MS)
HK = P.get('hooks') or {}
if not HK: raise SystemExit('REFUSING: pins carry no hook reading (pin (I))')
HOOK_LINE = 'THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT (pin (I), (K)): ' + '; '.join('%s %s %s (%s)' % (x.split('/')[-1], v['develop'][0], v['develop'][1][:12], 'IDENTICAL at develop, head and END' if len(set(tuple(y) if y else None for y in v.values())) == 1 else 'DIFFERS between trees') for x, v in HK.items()) + '.'
ALONE_LINE = 'The PR ALONE over develop (pin (E)): merge-tree clean, tree `%s`; its squash on develop (commit-tree, pin (F)) has the same tree.' % p['alone_tree']
prev = K['prev_report']; prev_sha = hashlib.sha256(open(prev, 'rb').read()).hexdigest()
if prev_sha != K['prev_report_sha256']: raise SystemExit('REFUSING: gate47 report sha256 %s != the GO\'s %s' % (prev_sha, K['prev_report_sha256']))
LD = last('lockdiff_1.out', 'LOCKDIFF PASS'); BL = last('baseline_1.out', 'BASELINE PASS'); LC = last('lockcensus_1.out', 'CENSUS DONE')
for f, lab in (('lockdiff_1.out', LD), ('baseline_1.out', BL)):
    hd = open(os.path.join(G, f), encoding='utf-8').read().splitlines()[0]
    if ('base %s' % P['develop'][:12]) not in hd or ('head %s' % p['head'][:12]) not in hd:
        raise SystemExit('REFUSING: %s was measured at another develop / head than the pins (%s) — re-run it' % (f, hd[:160]))
lc0 = open(os.path.join(G, 'lockcensus_1.out'), encoding='utf-8').read()
if P['end_tree'] not in lc0.splitlines()[0]: raise SystemExit('REFUSING: lockcensus_1.out was measured at another tree than the pinned END_TREE — re-run it')
vl = [l.strip() for l in lc0.splitlines() if l.strip().startswith('VULNERABLE entries:')]
LOCKCENSUS = '%s; %s' % (LC, vl[0] if vl else 'no VULNERABLE line')
GH = open(os.path.join(G, 'gh_read_1.out'), encoding='utf-8').read(); last('gh_read_1.out', 'GH READ OK')
cl = [l for l in GH.splitlines() if l.startswith('CENSUS ')]
CENSUS_LINE = (cl[-1] if cl else 'no CENSUS line') + ' (at %s; the launch action re-reads it, rc 15 on any hit)' % last('gh_read_1.out', 'GH READ OK').split(' at ')[-1]
CAP = last('capture_1.out', 'CAPTURE OK')
cap_txt = open(os.path.join(G, 'capture_1.out'), encoding='utf-8').read()
CAPTURE_LINE = 'ELEVEN mails read by id, verbatim, with TEXT_SHA256 (the READY, the leg-7 thread both ways, ROUTE B, the committed status, the handover) plus Wednesday\'s three clause-4 chat entries to Kam (%s; %s).' % (
    ' | '.join(l.strip() for l in cap_txt.splitlines() if l.startswith(('READY as captured', 'CLAUSE-4'))), CAP)
DR = last('drafts_1.out', 'DRAFTS OK'); dtx = open(os.path.join(G, 'drafts_1.out'), encoding='utf-8').read()
DRAFTS_LINE = 'both texts VERBATIM with SHA256, read from the seat\'s record folder `ks470/` because the READY names them but does not carry them (%s; %s).' % (
    ' | '.join(l.strip() for l in dtx.splitlines() if re.match(r'^(override|cleanroom) ', l)), DR)
rr = open(os.path.join(G, 'row_reason_gate48a.md'), encoding='utf-8').read()
m = re.search(r'reason sha256 ([0-9a-f]{64})', rr)
if not m: raise SystemExit('REFUSING: row_reason_gate48a.md carries no reason sha256')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'END_TREE': P['end_tree'], 'MEASURED_AT': P['measured_at'],
     'FILLED_AT': now, 'PIN_TABLE': table, 'ROWS': row, 'SUBJECT_TABLE': subj, 'H': p['head'], 'H_SHORT': p['head'][:12],
     'MODE_LINE': MODE_LINE, 'HOOK_LINE': HOOK_LINE, 'ALONE_LINE': ALONE_LINE, 'CAPTURE_LINE': CAPTURE_LINE, 'DRAFTS_LINE': DRAFTS_LINE, 'REASON_SHA': m.group(1),
     'LOCKDIFF': LD, 'BASELINE': BL, 'LOCKCENSUS': LOCKCENSUS, 'CENSUS_LINE': CENSUS_LINE,
     'KEYSCAN': last('keyscan_1.out', 'KEYSCAN PASS'), 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)), 'PREV_REPORT': prev, 'PREV_SHA': prev_sha,
     'VERDICT_SUBJECT': '[QA -> Wednesday] GATE48A #1354 (Seat B47 author and merger, round 48a; T2: KS-470 js-yaml 5.4.2 fixed, undici GHSA-r53p accepted to 2026-10-09)'}
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for a, v in V.items(): t = t.replace('{{%s}}' % a, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    with open(os.path.join(G, dst), 'w', encoding='utf-8') as f: f.write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes)' % (dst, len(t.encode('utf-8'))))
fill('prompt_gate48a.TEMPLATE.txt', K['prompt']); fill('launcher_gate48a.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = open(os.path.join(G, K['prompt']), encoding='utf-8').read()
tok = lambda w: re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), pt) is not None
missing = [w for w in KW if not tok(w)]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) as a token %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | 1 row | %d keywords | head #%s %s | gate47 report sha256 %s' % (now, P['develop'], P['end_tree'], len(KW), N, p['head'][:12], prev_sha[:12]))
