#!/usr/bin/env python3
"""fill_gate56a.py — FILL the gate56a prompt and launcher from their templates with the TWO PRs' numbers / heads / branches and develop
that the LAUNCH ACTION just read (repin_and_launch_gate56a.sh re-reads all of them from the PULLS API and ls-remote and calls this), and
write pins_gate56a.json. A NEW COPY of fill_gate55.py, re-keyed for two PRs. Re-pin and launch are ONE action (Kam 2026-09-18): the
launcher refuses a pin older than G56A_MAX_PIN_AGE_S (exit 9).
Refuses (rc 1) unless: PR3 / PR4 are digits and differ; HEAD3 / HEAD4 / DEVELOP are 40 lowercase hex and the heads differ; DEVELOP == kit
base (a moved develop before EITHER merged is a re-draft); each branch carries its own key and not the sibling's (kit branch_rx); the
charter exists; every double-brace token is filled; the filled prompt carries every by-name keyword.
The previous round's report (gateD2) is HASHED AND RECORDED, not compared: the drafter found no pinned sha256 for it (README section 6).
Controls-only: G56A_PREV_REPORT (a scratch stand-in for that report, so a simulation reads nothing under !CODING/).
--simulate <name>: write `<name>.SIM.prompt.txt`, `<name>.SIM.launcher.sh` and `pins_gate56a.SIM-<name>.json` (exercise only; never launched).
Usage: fill_gate56a.py --pr3 n --head3 sha --branch3 ref --pr4 n --head4 sha --branch4 ref --develop sha [--simulate name]"""
import hashlib, json, os, re, sys, time, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
NEED = ('--pr3', '--head3', '--branch3', '--pr4', '--head4', '--branch4', '--develop')
if '--help' in A or '-h' in A or not all(x in A for x in NEED):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR3, H3, B3, PR4, H4, B4, DEV, SIM = (opt(x) for x in NEED + ('--simulate',))
P3, P4 = K['prs']['pr3'], K['prs']['pr4']
bad = []
for n, v in (('PR3', PR3), ('PR4', PR4)):
    if not re.fullmatch(r'\d+', v or ''): bad.append('%s %r is not digits' % (n, v))
if PR3 == PR4: bad.append('PR3 == PR4 (%s): two PRs are gated' % PR3)
for n, v in (('HEAD3', H3), ('HEAD4', H4), ('DEVELOP', DEV)):
    if not re.fullmatch(r'[0-9a-f]{40}', v or ''): bad.append('%s %r is not 40 lowercase hex' % (n, v))
if H3 == H4: bad.append('HEAD3 == HEAD4')
if DEV != K['base']: bad.append('STALE BASE: develop %s != kit base %s — re-draft (README section 7)' % (DEV, K['base']))
for n, br, P, S in (('BRANCH3', B3, P3, P4), ('BRANCH4', B4, P4, P3)):
    if not (re.search(P['branch_rx'], br or '') and not re.search(S['branch_rx'], br or '')):
        bad.append('%s %r must carry %s and not %s' % (n, br, P['branch_rx'], S['branch_rx']))
if not os.path.isfile(K['charter']): bad.append('charter %s absent' % K['charter'])
if bad:
    for b in bad: print('REFUSING: ' + b)
    raise SystemExit(1)
PREV = os.environ.get('G56A_PREV_REPORT') or K['prev_report']   # CONTROLS-ONLY override (a scratch stand-in); a real launch refuses any G56A_*
ps = hashlib.sha256(open(PREV, 'rb').read()).hexdigest() if os.path.isfile(PREV) else 'ABSENT'
KEYWORDS = ['C1-PIN', 'ONE-PATH', 'NO-TRAILER', 'SUBJECT-EXACT', 'KEYSCAN-OWN-KEY', 'END-TREE', 'C2-DIFF-SHAPE', 'C3-FROZEN-CLOCK', 'C3-LAPSE-COMPARISON',
            'C3-FUSE-STILL-EXISTS', 'C4-SECURITY', 'C4-NO-WIDENING', 'C5-NOT-COVERED', 'C5-AUTHORITY', 'METHOD-STATED', 'PR-BODY-CLAIMS', 'COLLISION-CENSUS',
            'NOT-TESTED-LIST', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
pn = ('pins_gate56a.SIM-%s.json' % SIM) if SIM else 'pins_gate56a.json'
ep = int(time.time()); at = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
f = lambda t: t.replace('{PR3}', PR3).replace('{PR4}', PR4)
prompt_name = (SIM + '.SIM.prompt.txt') if SIM else f(K['prompt_template_out'])
launcher_name = (SIM + '.SIM.launcher.sh') if SIM else f(K['launcher_template_out'])
V = {'PR3': PR3, 'HEAD3': H3, 'BRANCH3': B3, 'PR4': PR4, 'HEAD4': H4, 'BRANCH4': B4, 'DEVELOP': DEV, 'PINNED_AT': at, 'PINNED_EPOCH': str(ep), 'GS': G,
     'GO3': K['go_template'].replace('{PR}', PR3), 'GO4': K['go_template'].replace('{PR}', PR4), 'VERDICT_SUBJECT': f(K['verdict_subject_template']),
     'REPORT': f(K['report_template']), 'PREV_REPORT': K['prev_report'], 'PREV_SHA': ps, 'CHARTER': K['charter'], 'SEAT_BRIEFS': ', '.join(K['seat_briefs']),
     'LAUNCHER': launcher_name, 'PROMPT': prompt_name, 'PATH3': P3['path'], 'PATH4': P4['path'], 'KEYWORDS': ' '.join(KEYWORDS), 'PINS': pn, 'N_KW': str(len(KEYWORDS))}
def fill(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: print('REFUSING: %s leaves unfilled tokens %s' % (src, left)); raise SystemExit(1)
    return t
P = fill('prompt_gate56a.TEMPLATE.txt'); L = fill('launcher_gate56a.TEMPLATE.sh.txt')
J = re.sub(r'\n\s*', ' ', P); miss = [w for w in KEYWORDS if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), J)]
if miss: print('REFUSING: the filled prompt lacks keyword(s) %s' % miss); raise SystemExit(1)
open(os.path.join(G, prompt_name), 'w', encoding='utf-8').write(P)
lp = os.path.join(G, launcher_name); open(lp, 'w', encoding='utf-8').write(L); os.chmod(lp, 0o755)
pins = {'pr3': PR3, 'head3': H3, 'branch3': B3, 'pr4': PR4, 'head4': H4, 'branch4': B4, 'develop': DEV, 'pinned_at': at, 'pinned_epoch': ep, 'prompt': prompt_name,
        'launcher': launcher_name, 'go3': V['GO3'], 'go4': V['GO4'], 'verdict_subject': V['VERDICT_SUBJECT'], 'report': V['REPORT'],
        'routing_line': f(K['routing_line_template']), 'prev_report_sha256_at_fill': ps, 'simulated': bool(SIM), 'prompt_sha256': hashlib.sha256(P.encode()).hexdigest()}
json.dump(pins, open(os.path.join(G, pn), 'w'), indent=2); open(os.path.join(G, pn), 'a').write('\n')
print('FILLED %s | #%s %s + #%s %s | develop %s | %s, %s, %s | %d keywords | prev report sha256 %s | prompt sha256 %s' % (
    at, PR3, H3[:12], PR4, H4[:12], DEV[:12], prompt_name, launcher_name, pn, len(KEYWORDS), ps[:16], pins['prompt_sha256'][:16]))
