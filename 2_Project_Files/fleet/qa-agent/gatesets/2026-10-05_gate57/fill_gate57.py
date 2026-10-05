#!/usr/bin/env python3
"""fill_gate57.py — FILL the gate57 prompt and launcher from their templates with the TWO PRs' numbers / heads / branches and develop that
the LAUNCH ACTION just read (repin_and_launch_gate57.sh re-reads all of them from the PULLS API and ls-remote and calls this), and write
pins_gate57.json. A NEW COPY of fill_gate56a.py, re-keyed for #1380 + #1381. Re-pin and launch are ONE action (Kam 2026-09-18): the
launcher refuses a pin older than G57_MAX_PIN_AGE_S (exit 9).
Refuses (rc 1) unless: PR1 / PR2 are digits, differ, and == kit prs.pr1 / pr2 numbers; HEAD1 / HEAD2 / DEVELOP are 40 lowercase hex and the
heads differ; DEVELOP == kit cut_base OR --behind <n> > 0 is given (the launch action proved the advance disjoint; README section 7); each
branch matches its own kit branch_rx and not the sibling's; the previous reports (gate55, gateD2) still hash to the kit's sha256; the READY
still hashes to kit seat_ready_sha256; every double-brace token is filled; the filled prompt carries every by-name keyword.
Controls-only: G57_PREV_REPORT / G57_PREV_REPORT_2 (scratch stand-ins, so a simulation reads nothing under !CODING/).
--simulate <name>: write `<name>.SIM.prompt.txt`, `<name>.SIM.launcher.sh` and `pins_gate57.SIM-<name>.json` (exercise only; never launched).
Usage: fill_gate57.py --pr1 n --head1 sha --branch1 ref --pr2 n --head2 sha --branch2 ref --develop sha [--behind n] [--simulate name]"""
import hashlib, json, os, re, sys, time, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
NEED = ('--pr1', '--head1', '--branch1', '--pr2', '--head2', '--branch2', '--develop')
if '--help' in A or '-h' in A or not all(x in A for x in NEED):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR1, H1, B1, PR2, H2, B2, DEV = (opt(x) for x in NEED); SIM = opt('--simulate'); BEHIND = opt('--behind', '0')
P1, P2 = K['prs']['pr1'], K['prs']['pr2']
bad = []
for n, v, k in (('PR1', PR1, P1), ('PR2', PR2, P2)):
    if not re.fullmatch(r'\d+', v or ''): bad.append('%s %r is not digits' % (n, v))
    elif v != k['number']: bad.append('%s %s != kit %s (this kit was drafted for #%s %s)' % (n, v, k['number'], k['number'], k['ticket']))
for n, v in (('HEAD1', H1), ('HEAD2', H2), ('DEVELOP', DEV)):
    if not re.fullmatch(r'[0-9a-f]{40}', v or ''): bad.append('%s %r is not 40 lowercase hex' % (n, v))
if H1 == H2: bad.append('HEAD1 == HEAD2')
if not re.fullmatch(r'\d+', BEHIND): bad.append('--behind %r is not digits' % BEHIND)
elif DEV != K['cut_base'] and int(BEHIND) == 0: bad.append('develop %s != cut_base %s with --behind 0: a develop advance must be proved disjoint by the launch action first' % (DEV[:12], K['cut_base'][:12]))
for n, br, P, S in (('BRANCH1', B1, P1, P2), ('BRANCH2', B2, P2, P1)):
    if not (re.match(P['branch_rx'], br or '') and not re.match(S['branch_rx'], br or '')):
        bad.append('%s %r must match %s and not %s' % (n, br, P['branch_rx'], S['branch_rx']))
for envn, kp, ks in (('G57_PREV_REPORT', 'prev_report', 'prev_report_sha256'), ('G57_PREV_REPORT_2', 'prev_report_2', 'prev_report_2_sha256')):
    f = os.environ.get(envn) or K[kp]
    h = hashlib.sha256(open(f, 'rb').read()).hexdigest() if os.path.isfile(f) else 'ABSENT'
    if h != K[ks] and not os.environ.get(envn): bad.append('%s sha256 %s != kit %s' % (K[kp], h[:16], K[ks][:16]))
rh = hashlib.sha256(open(K['seat_ready'], 'rb').read()).hexdigest() if os.path.isfile(K['seat_ready']) else 'ABSENT'
if rh != K['seat_ready_sha256']: bad.append('the READY %s sha256 %s != kit %s (it changed after drafting: re-read it)' % (K['seat_ready'], rh[:16], K['seat_ready_sha256'][:16]))
if not os.path.isfile(K['charter']): bad.append('charter %s absent' % K['charter'])
if bad:
    for b in bad: print('REFUSING: ' + b)
    raise SystemExit(1)
KEYWORDS = ['C1-PIN', 'END-TREE', 'NO-TRAILER', 'SUBJECT-EXACT', 'C2-GOLDEN', 'C2-TAMPER', 'C2-SUITE', 'C2-DOCFIX', 'Q-27', 'N-1375-1',
            'C3-SHAPE', 'C3-RED-FIRST', 'C3-PROBE', 'C3-SUITE', 'C3-TSC', 'C4-DOCS', 'C4-PREDICT', 'Q-M', 'C5-PREFLIGHT', 'PREFLIGHT-INCOMPLETE',
            'C6-SCOPE', 'KEYSCAN-OWN-KEY', 'NOT-COVERED', 'READY-CLAIMS', 'PR-BODY-CLAIMS', 'COLLISION-CENSUS', 'NOT-TESTED-LIST', 'TIERING',
            'DISK-ENOSPC', 'REPORT-HASH-LAST']
PB = (K.get('predictions_by_develop') or {}).get(DEV)
if DEV == K['cut_base']:
    DEV_NOTE = 'develop == cut_base: the READY\'s END_TREEs apply (#%s lands as its head tree %s; T2 %s).' % (PR1, P1['ready_end_tree'], P2['ready_end_tree'])
elif PB:
    DEV_NOTE = ('develop ADVANCED to %s (%s commit(s) past cut_base, disjoint from every kit path): the READY\'s END_TREEs are STALE. The drafter re-derived at THIS develop: '
                '#%s lands as %s (not its head tree) and T2 == %s (%s). Re-derive both yourself with `c4b_predict_gate57.py --develop %s` and quote YOURS; '
                'the GO must name the END_TREE at the develop it merges onto.') % (DEV, BEHIND, PR1, PB['pr1_end_tree'], PB['t2'], PB['source'][:80], DEV)
else:
    DEV_NOTE = ('develop ADVANCED to %s (%s commit(s) past cut_base, disjoint from every kit path), a develop the drafter did NOT predict: the READY\'s END_TREEs are STALE. '
                'Re-derive #%s\'s landed tree and T2 with `c4b_predict_gate57.py --develop %s` and quote yours; the GO must name the END_TREE at the develop it merges onto.') % (DEV, BEHIND, PR1, DEV)
pn = ('pins_gate57.SIM-%s.json' % SIM) if SIM else 'pins_gate57.json'
ep = int(time.time()); at = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
f = lambda t: t.replace('{PR1}', PR1).replace('{PR2}', PR2)
prompt_name = (SIM + '.SIM.prompt.txt') if SIM else f(K['prompt_template_out'])
launcher_name = (SIM + '.SIM.launcher.sh') if SIM else f(K['launcher_template_out'])
V = {'PR1': PR1, 'HEAD1': H1, 'BRANCH1': B1, 'PR2': PR2, 'HEAD2': H2, 'BRANCH2': B2, 'DEVELOP': DEV, 'CUT_BASE': K['cut_base'], 'BEHIND': BEHIND,
     'PINNED_AT': at, 'PINNED_EPOCH': str(ep), 'GS': G, 'GO1': K['go_template'].replace('{PR}', PR1), 'GO2': K['go_template'].replace('{PR}', PR2),
     'VERDICT_SUBJECT': f(K['verdict_subject_template']), 'REPORT': f(K['report_template']), 'PREV_REPORT': K['prev_report'], 'PREV_SHA': K['prev_report_sha256'],
     'PREV_REPORT_2': K['prev_report_2'], 'PREV_SHA_2': K['prev_report_2_sha256'], 'CHARTER': K['charter'], 'SEAT_BRIEF': K['seat_brief'], 'READY': K['seat_ready'],
     'READY_SHA': K['seat_ready_sha256'], 'RULING': K['ruling'], 'T2': P2['ready_end_tree'], 'T1': P1['ready_end_tree'],
     'FILES1': ','.join(sorted(P1['files'])), 'FILES2': ','.join(sorted(P2['files'])), 'N1': str(len(P1['files'])), 'N2': str(len(P2['files'])),
     'DEV_NOTE': DEV_NOTE, 'LAUNCHER': launcher_name, 'PROMPT': prompt_name, 'KEYWORDS': ' '.join(KEYWORDS), 'PINS': pn, 'N_KW': str(len(KEYWORDS))}
def fill(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: print('REFUSING: %s leaves unfilled tokens %s' % (src, left)); raise SystemExit(1)
    return t
P = fill('prompt_gate57.TEMPLATE.txt'); L = fill('launcher_gate57.TEMPLATE.sh.txt')
J = re.sub(r'\n\s*', ' ', P); miss = [w for w in KEYWORDS if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), J)]
if miss: print('REFUSING: the filled prompt lacks keyword(s) %s' % miss); raise SystemExit(1)
open(os.path.join(G, prompt_name), 'w', encoding='utf-8').write(P)
lp = os.path.join(G, launcher_name); open(lp, 'w', encoding='utf-8').write(L); os.chmod(lp, 0o755)
pins = {'pr1': PR1, 'head1': H1, 'branch1': B1, 'pr2': PR2, 'head2': H2, 'branch2': B2, 'develop': DEV, 'behind': int(BEHIND), 'pinned_at': at, 'pinned_epoch': ep,
        'prompt': prompt_name, 'launcher': launcher_name, 'go1': V['GO1'], 'go2': V['GO2'], 'verdict_subject': V['VERDICT_SUBJECT'], 'report': V['REPORT'],
        'routing_line': f(K['routing_line_template']), 'simulated': bool(SIM), 'prompt_sha256': hashlib.sha256(P.encode()).hexdigest()}
json.dump(pins, open(os.path.join(G, pn), 'w'), indent=2); open(os.path.join(G, pn), 'a').write('\n')
print('FILLED %s | #%s %s + #%s %s | develop %s (behind %s) | %s, %s, %s | %d keywords | prompt sha256 %s' % (
    at, PR1, H1[:12], PR2, H2[:12], DEV[:12], BEHIND, prompt_name, launcher_name, pn, len(KEYWORDS), pins['prompt_sha256'][:16]))
