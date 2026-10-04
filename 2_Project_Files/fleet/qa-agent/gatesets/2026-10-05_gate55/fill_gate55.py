#!/usr/bin/env python3
"""fill_gate55.py — FILL the gate55 prompt and launcher from their templates with the PR number / HEAD / develop / branch the LAUNCH ACTION
just read (the PR number and head arrive with Seat B 58th's READY; the launch action re-reads both from the PULLS API and ls-remote and
calls this), and write pins_gate55.json. A NEW COPY of fill_gate54a.py, re-keyed, plus a MOVED-HEAD refusal. Re-pin and launch are ONE
action (Kam 2026-09-18): the launcher refuses a pin older than G55_MAX_PIN_AGE_S (exit 9).
Refuses (rc 1) unless: PR is digits; HEAD and DEVELOP are 40 lowercase hex; DEVELOP == kit base (a moved develop is a RE-DRAFT, README
section 7); HEAD == kit expected_head (every C1-C5 expectation — blobs, numstat, the doc blocks' line numbers — was drafted at that head:
a moved head is a RE-DRAFT, never a fill); the branch matches kit branch_rx; gate54a's report hashes to kit prev_report_sha256; the charter
exists; every double-brace token is filled; the filled prompt carries every by-name keyword.
--simulate <name>: write `<name>.SIM.prompt.txt`, `<name>.SIM.launcher.sh` and `pins_gate55.SIM-<name>.json` (exercise only; never launched).
Controls-only: G55_PREV_REPORT (a stand-in report path), G55_PREV_SHA (its expected sha256) — the launch action refuses a REAL launch with
any G55_* set (rc 16), so these can only ever shape a simulation.
Usage: fill_gate55.py --pr <n> --head <sha> --develop <sha> --branch <ref-without-refs/heads/> [--simulate name]"""
import hashlib, json, os, re, sys, time, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
if '--help' in A or '-h' in A or not all(x in A for x in ('--pr', '--head', '--develop', '--branch')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR, HEAD, DEV, BR, SIM = opt('--pr'), opt('--head'), opt('--develop'), opt('--branch'), opt('--simulate')
PREV = os.environ.get('G55_PREV_REPORT') or K['prev_report']; PREV_SHA = os.environ.get('G55_PREV_SHA') or K['prev_report_sha256']
bad = []
if not re.fullmatch(r'\d+', PR or ''): bad.append('PR %r is not digits' % PR)
for n, v in (('HEAD', HEAD), ('DEVELOP', DEV)):
    if not re.fullmatch(r'[0-9a-f]{40}', v or ''): bad.append('%s %r is not 40 lowercase hex' % (n, v))
if DEV != K['base']: bad.append('STALE BASE: develop %s != kit base %s — a develop move is a RE-DRAFT (README section 7)' % (DEV, K['base']))
if HEAD != K['expected_head']: bad.append('MOVED HEAD: %s != kit expected_head %s (%s) — a RE-DRAFT (README section 7)' % (HEAD, K['expected_head'], K.get('superseded_heads', {}).get(HEAD or '', 'not a head the drafter saw')))
if not re.match(K['branch_rx'], BR or ''): bad.append('branch %r does not match kit branch_rx %s' % (BR, K['branch_rx']))
ps = hashlib.sha256(open(PREV, 'rb').read()).hexdigest() if os.path.isfile(PREV) else 'ABSENT'
if ps != PREV_SHA: bad.append('previous-round report %s sha256 %s != %s' % (PREV, ps, PREV_SHA))
if not os.path.isfile(K['charter']): bad.append('charter %s absent' % K['charter'])
if bad:
    for b in bad: print('REFUSING: ' + b)
    raise SystemExit(1)
KEYWORDS = ['C1-PIN', 'END-TREE', 'MODES', 'NO-TRAILER', 'KEYSCAN-OWN-KEY', 'PR0-ABSENT', 'COTENANT-ABSENT', 'C2-REGEN', 'C2-DRIFT-CONTROL', 'C2-CHECK-OPENAPI',
            'C3-CELLS', 'C3-SUITES', 'C3-TSC', 'C4-DOCS-S4', 'C4-KS1402-BYTE-IDENTICAL', 'C5-HANDLER', 'C6-NOT-COVERED', 'METHOD-STATED', 'PR-BODY-CLAIMS',
            'COLLISION-CENSUS', 'NOT-TESTED-LIST', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
pn = ('pins_gate55.SIM-%s.json' % SIM) if SIM else 'pins_gate55.json'
ep = int(time.time()); at = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
f = lambda t: t.replace('{PR}', PR)
prompt_name = (SIM + '.SIM.prompt.txt') if SIM else f(K['prompt_template_out'])
launcher_name = (SIM + '.SIM.launcher.sh') if SIM else f(K['launcher_template_out'])
V = {'PR': PR, 'HEAD': HEAD, 'DEVELOP': DEV, 'BRANCH': BR, 'PINNED_AT': at, 'PINNED_EPOCH': str(ep), 'GS': G, 'GO': f(K['go_template']),
     'VERDICT_SUBJECT': f(K['verdict_subject_template']), 'REPORT': f(K['report_template']), 'PREV_REPORT': K['prev_report'], 'PREV_SHA': K['prev_report_sha256'],
     'CHARTER': K['charter'], 'SEAT_BRIEF': K['seat_brief'], 'LAUNCHER': launcher_name, 'PROMPT': prompt_name, 'FILES_CSV': ','.join(sorted(K['files'])),
     'N_FILES': str(len(K['files'])), 'KEYWORDS': ' '.join(KEYWORDS), 'PINS': pn, 'N_KW': str(len(KEYWORDS)), 'EXPECTED_TREE': K['expected_tree']}
def fill(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: print('REFUSING: %s leaves unfilled tokens %s' % (src, left)); raise SystemExit(1)
    return t
P = fill('prompt_gate55.TEMPLATE.txt'); L = fill('launcher_gate55.TEMPLATE.sh.txt')
J = re.sub(r'\n\s*', ' ', P); miss = [w for w in KEYWORDS if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), J)]
if miss: print('REFUSING: the filled prompt lacks keyword(s) %s' % miss); raise SystemExit(1)
open(os.path.join(G, prompt_name), 'w', encoding='utf-8').write(P)
lp = os.path.join(G, launcher_name); open(lp, 'w', encoding='utf-8').write(L); os.chmod(lp, 0o755)
pins = {'pr': PR, 'head': HEAD, 'develop': DEV, 'branch': BR, 'pinned_at': at, 'pinned_epoch': ep, 'prompt': prompt_name, 'launcher': launcher_name,
        'go': V['GO'], 'verdict_subject': V['VERDICT_SUBJECT'], 'report': V['REPORT'], 'routing_line': f(K['routing_line_template']), 'simulated': bool(SIM),
        'prompt_sha256': hashlib.sha256(P.encode()).hexdigest()}
json.dump(pins, open(os.path.join(G, pn), 'w'), indent=2); open(os.path.join(G, pn), 'a').write('\n')
print('FILLED %s | PR #%s head %s develop %s | %s, %s, %s | %d keywords | prompt sha256 %s' % (at, PR, HEAD[:12], DEV[:12], prompt_name, launcher_name, pn, len(KEYWORDS), pins['prompt_sha256'][:16]))
