#!/usr/bin/env python3
"""fill_gate58.py — FILL the gate58 prompt and launcher from their templates with the PR / HEAD / develop / branch the LAUNCH ACTION just read,
and write pins_gate58.json. Called by repin_and_launch_gate58.sh immediately before launch (re-pin and launch are ONE action, Kam 2026-09-18);
never trusted from an earlier run: the launcher refuses a pin older than G58_MAX_PIN_AGE_S (exit 9).
Refuses (rc 1) unless: PR is digits; HEAD and DEVELOP are 40 lowercase hex; DEVELOP == kit base (every C2-C6 expectation was drafted against
it: a moved develop is a RE-DRAFT, not a fill); the branch matches kit branch_rx; the previous report (gate54f) still hashes to kit prev_report_sha256; every
double-brace token is filled; the filled prompt carries every by-name keyword.
--simulate <name>: write `<name>.SIM.prompt.txt`, `<name>.SIM.launcher.sh` and `pins_gate58.SIM-<name>.json` instead (exercise only; a SIM
launcher's GS is this directory but its prompt path is the SIM prompt, and it is never launched).
Usage: fill_gate58.py --pr <n> --head <sha> --develop <sha> --branch <ref-without-refs/heads/> [--simulate name]"""
import hashlib, json, os, re, sys, time, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
if '--help' in A or '-h' in A or not all(x in A for x in ('--pr', '--head', '--develop', '--branch')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR, HEAD, DEV, BR, SIM = opt('--pr'), opt('--head'), opt('--develop'), opt('--branch'), opt('--simulate')
bad = []
if not re.fullmatch(r'\d+', PR): bad.append('PR %r is not digits' % PR)
for n, v in (('HEAD', HEAD), ('DEVELOP', DEV)):
    if not re.fullmatch(r'[0-9a-f]{40}', v or ''): bad.append('%s %r is not 40 lowercase hex' % (n, v))
if DEV != K['base']: bad.append('STALE BASE: develop %s != kit base %s — every C2-C6 expectation was drafted against the base; a develop move is a RE-DRAFT (README section 7)' % (DEV, K['base']))
if not re.match(K['branch_rx'], BR or ''): bad.append('branch %r does not match kit branch_rx %s' % (BR, K['branch_rx']))
PREV = os.environ.get('G58_PREV_REPORT') or K['prev_report']   # controls-only override for a SIM fill
ps = hashlib.sha256(open(PREV, 'rb').read()).hexdigest() if os.path.isfile(PREV) else 'ABSENT'
if ps != K['prev_report_sha256']: bad.append('previous report (gate54f) sha256 %s != kit %s' % (ps, K['prev_report_sha256']))
if bad:
    for b in bad: print('REFUSING: ' + b)
    raise SystemExit(1)
KEYWORDS = ['C1-PIN', 'C2-LOCKDIFF', 'C3-INTEGRITY', 'C4-BASELINE', 'C5-LEGS', 'C5-FROZEN-CLOCK', 'C5-BASE-CONTROL', 'C5-BITE', 'C5-INSTALL-ROOT',
            'C6-NOT-COVERED', 'END-TREE', 'MODES', 'NO-TRAILER', 'KEYSCAN-OWN-KEY', 'NO-ARCHIVED-KEY', 'METHOD-STATED', 'PR-BODY-CLAIMS', 'READY-CLAIMS',
            'PREFLIGHT-INCOMPLETE', 'COLLISION-CENSUS', 'NOT-TESTED-LIST', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
pn = ('pins_gate58.SIM-%s.json' % SIM) if SIM else 'pins_gate58.json'
ep = int(time.time()); at = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
f = lambda t: t.replace('{PR}', PR)
prompt_name = (SIM + '.SIM.prompt.txt') if SIM else f(K['prompt_template_out'])
launcher_name = (SIM + '.SIM.launcher.sh') if SIM else f(K['launcher_template_out'])
V = {'PR': PR, 'HEAD': HEAD, 'DEVELOP': DEV, 'BRANCH': BR, 'PINNED_AT': at, 'PINNED_EPOCH': str(ep), 'GS': G, 'GO': f(K['go_template']),
     'VERDICT_SUBJECT': f(K['verdict_subject_template']), 'REPORT': f(K['report_template']), 'PREV_REPORT': K['prev_report'], 'PREV_SHA': K['prev_report_sha256'],
     'RULING': K['ruling'], 'READY': K['seat_ready'], 'LAUNCHER': launcher_name, 'PROMPT': prompt_name, 'FILES_CSV': ','.join(sorted(K['files'])),
     'KEYWORDS': ' '.join(KEYWORDS), 'PINS': pn, 'N_KW': str(len(KEYWORDS))}
def fill(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: print('REFUSING: %s leaves unfilled tokens %s' % (src, left)); raise SystemExit(1)
    return t
P = fill('prompt_gate58.TEMPLATE.txt'); L = fill('launcher_gate58.TEMPLATE.sh.txt')
J = re.sub(r'\n\s*', ' ', P); miss = [w for w in KEYWORDS if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), J)]
if miss: print('REFUSING: the filled prompt lacks keyword(s) %s' % miss); raise SystemExit(1)
open(os.path.join(G, prompt_name), 'w', encoding='utf-8').write(P)
lp = os.path.join(G, launcher_name); open(lp, 'w', encoding='utf-8').write(L); os.chmod(lp, 0o755)
pins = {'pr': PR, 'head': HEAD, 'develop': DEV, 'branch': BR, 'pinned_at': at, 'pinned_epoch': ep, 'prompt': prompt_name, 'launcher': launcher_name,
        'go': V['GO'], 'verdict_subject': V['VERDICT_SUBJECT'], 'report': V['REPORT'], 'simulated': bool(SIM),
        'prompt_sha256': hashlib.sha256(P.encode()).hexdigest()}
json.dump(pins, open(os.path.join(G, pn), 'w'), indent=2); open(os.path.join(G, pn), 'a').write('\n')
print('FILLED %s | PR #%s head %s develop %s | %s, %s, %s | %d keywords | prompt sha256 %s' % (at, PR, HEAD[:12], DEV[:12], prompt_name, launcher_name, pn, len(KEYWORDS), pins['prompt_sha256'][:16]))
