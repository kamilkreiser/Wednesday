#!/usr/bin/env python3
"""fill_gate61.py — FILL the gate61 prompt and launcher from their templates with the PR / HEAD / develop / branch the LAUNCH ACTION just
read, and write pins_gate61.json. Called by repin_and_launch_gate61.sh immediately before launch (re-pin and launch are ONE action, Kam
2026-09-18); never trusted from an earlier run: the launcher refuses a pin older than G61_MAX_PIN_AGE_S (exit 9).
Refuses (rc 1) unless: PR == kit pr; HEAD == kit head and DEVELOP == kit develop (40 lowercase hex: every C1-C6 expectation and the Q-M
prediction were drafted against them — a moved head or develop is a RE-DRAFT, not a fill); the branch == kit branch and matches branch_rx;
the READY still hashes to kit seat_ready_sha256; the previous report (gate57, the Q-M precedent) still hashes to kit prev_report_sha256; every double-brace
token is filled; the filled prompt carries every by-name keyword (as a token).
--simulate <name>: write `<name>.SIM.prompt.txt`, `<name>.SIM.launcher.sh` and `pins_gate61.SIM-<name>.json` instead (exercise only; never
launched).
Usage: fill_gate61.py --pr <n> --head <sha> --develop <sha> --branch <ref-without-refs/heads/> [--simulate name]"""
import hashlib, json, os, re, sys, time, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]
if '--help' in A or '-h' in A or not all(x in A for x in ('--pr', '--head', '--develop', '--branch')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
PR, HEAD, DEV, BR, SIM = opt('--pr'), opt('--head'), opt('--develop'), opt('--branch'), opt('--simulate')
bad = []
if PR != K['pr']: bad.append('PR %r != kit pr %s (this kit is drafted for ONE PR)' % (PR, K['pr']))
for n, v in (('HEAD', HEAD), ('DEVELOP', DEV)):
    if not re.fullmatch(r'[0-9a-f]{40}', v or ''): bad.append('%s %r is not 40 lowercase hex' % (n, v))
if HEAD != K['head']: bad.append('HEAD MOVED: %s != kit head %s — every expectation and the Q-M prediction are head-specific: RE-DRAFT (README section 6)' % (HEAD, K['head']))
if DEV != K['develop']: bad.append('STALE BASE: develop %s != kit develop %s — RE-DRAFT, or judge a later merge-in with c4 qm (README section 6)' % (DEV, K['develop']))
if BR != K['branch'] or not re.match(K['branch_rx'], BR or ''): bad.append('branch %r != kit branch %s / rx %s' % (BR, K['branch'], K['branch_rx']))
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.isfile(p) else 'ABSENT'
PREV = os.environ.get('G61_PREV_REPORT') or K['prev_report']   # controls-only override for a SIM fill
if h(PREV) != K['prev_report_sha256']: bad.append('previous report (gate57, the Q-M precedent) sha256 %s != kit %s' % (h(PREV), K['prev_report_sha256']))
READY = os.environ.get('G61_READY') or K['seat_ready']
if h(READY) != K['seat_ready_sha256']: bad.append('the READY sha256 %s != kit %s (it changed since drafting)' % (h(READY), K['seat_ready_sha256']))
BRIEF = os.environ.get('G61_BRIEF') or K['seat_brief']
if h(BRIEF) != K['seat_brief_sha256']: bad.append('the seat brief sha256 %s != kit %s (it changed since drafting)' % (h(BRIEF), K['seat_brief_sha256']))
if bad:
    for b in bad: print('REFUSING: ' + b)
    raise SystemExit(1)
KEYWORDS = ['C1-PIN', 'END-TREE', 'NO-TRAILER', 'SUBJECT-EXACT', 'EXEC-BIT', 'C2-MIGRATION', 'LIVE-SQL-GUARD', 'MUST-NOT', 'NULL-ONLY-BACKFILL',
            'C3-SUITE', 'C3-RED-FIRST', 'C3-TAMPER', 'NON-BYPASS', 'IDEMPOTENCE-NONCE', 'DATA-SAFETY', 'POLICY-FIDELITY', 'C3B-PROBE',
            'WRITER-CENSUS', 'C4-DOCS', 'C4-MERGE-IN', 'Q-M', 'C5-PR-TEXT', 'CLOSING-WORD', 'NEVER-DEMO', 'C6-NOT-COVERED', 'KEYSCAN-OWN-KEY',
            'READY-CLAIMS', 'PR-BODY-CLAIMS', 'PREFLIGHT-INCOMPLETE', 'COLLISION-CENSUS', 'NOT-TESTED-LIST', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
pn = ('pins_gate61.SIM-%s.json' % SIM) if SIM else 'pins_gate61.json'
ep = int(time.time()); at = datetime.datetime.fromtimestamp(ep, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
f = lambda t: t.replace('{PR}', PR)
prompt_name = (SIM + '.SIM.prompt.txt') if SIM else f(K['prompt_template_out'])
launcher_name = (SIM + '.SIM.launcher.sh') if SIM else f(K['launcher_template_out'])
V = {'PR': PR, 'HEAD': HEAD, 'DEVELOP': DEV, 'BRANCH': BR, 'PINNED_AT': at, 'PINNED_EPOCH': str(ep), 'GS': G, 'GO': f(K['go_template']),
     'VERDICT_SUBJECT': f(K['verdict_subject_template']), 'REPORT': f(K['report_template']), 'PREV_REPORT': K['prev_report'], 'PREV_SHA': K['prev_report_sha256'],
     'RULING': K['ruling'], 'QM': K['q_m'], 'READY': K['seat_ready'], 'READY_SHA': K['seat_ready_sha256'], 'SEAT_BRIEF': K['seat_brief'], 'SEAT_BRIEF_SHA': K['seat_brief_sha256'], 'B50': K['b50_handover'], 'SIB_REPORT': K['sibling_report'], 'SIB_SHA': K['sibling_report_sha256'],
     'CHARTER': K['charter'], 'END_TREE': K['end_tree'], 'SUBJECT': K['squash_subject_declared'], 'SUBJECT_LEN': str(len(K['squash_subject_declared'])),
     'LAUNCHER': launcher_name, 'PROMPT': prompt_name, 'FILES_CSV': ','.join(sorted(K['files'])), 'KEYWORDS': ' '.join(KEYWORDS), 'PINS': pn,
     'N_KW': str(len(KEYWORDS)), 'AHEAD': str(K['compare_ahead']), 'NFILES': str(len(K['files']))}
def fill(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: print('REFUSING: %s leaves unfilled tokens %s' % (src, left)); raise SystemExit(1)
    return t
P = fill('prompt_gate61.TEMPLATE.txt'); L = fill('launcher_gate61.TEMPLATE.sh.txt')
J = re.sub(r'\n\s*', ' ', P); miss = [w for w in KEYWORDS if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), J)]
if miss: print('REFUSING: the filled prompt lacks keyword(s) %s' % miss); raise SystemExit(1)
open(os.path.join(G, prompt_name), 'w', encoding='utf-8').write(P)
lp = os.path.join(G, launcher_name); open(lp, 'w', encoding='utf-8').write(L); os.chmod(lp, 0o755)
pins = {'pr': PR, 'head': HEAD, 'develop': DEV, 'branch': BR, 'pinned_at': at, 'pinned_epoch': ep, 'prompt': prompt_name, 'launcher': launcher_name,
        'go': V['GO'], 'verdict_subject': V['VERDICT_SUBJECT'], 'report': V['REPORT'], 'simulated': bool(SIM), 'prompt_sha256': hashlib.sha256(P.encode()).hexdigest()}
json.dump(pins, open(os.path.join(G, pn), 'w'), indent=2); open(os.path.join(G, pn), 'a').write('\n')
print('FILLED %s | PR #%s head %s develop %s | %s, %s, %s | %d keywords | prompt sha256 %s' % (at, PR, HEAD[:12], DEV[:12], prompt_name, launcher_name, pn, len(KEYWORDS), pins['prompt_sha256'][:16]))
