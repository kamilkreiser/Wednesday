#!/usr/bin/env python3
"""capture_mail_gate34.py — build the gate's CAPTURE for the gate34 kit (kit.json beside this script): mail_<kit>_ready.md + stopcounts_<kit>.json.

NO READY MESSAGE ID reached the drafter for any PR (Wednesday relayed PR numbers, heads, tickets and rulings in her commission, with no agentmail id for the
seat's READYs); finding a READY without its id needs an inbox LISTING, which marks mail seen — forbidden. So each seat claim is captured from (1) the PR
BODY (gh_body_<n>.md, as read by gh_read_gate34.py), (2) EVERY commit message in the PR's chain over its develop merge-base (no stack in gate34; read
from the scratch clone, `git log --format=%B`), (3) Seat B 36th's raise records below, each verbatim with its TEXT_SHA256. Seat B 36th's raise/ holds
NO per-item RED / GREEN / suite files this round (READ by `ls -la 2026-09-28_seatB-36th/raise/` at drafting: push logs, its tooling, watch proofs) —
its red / green / suite / tsc / lint figures are claims in its PR bodies; its `exclude: []` tsconfigs sit in its quarantine/ and are captured here.
Each PR's push log is READ for the fleet STOP counts by BOUNDED REGION between consecutive `=== <path> ===` headers, with a NOT-FOUND control (a
header that does not exist must read NOT FOUND). Shape copied from gate34's capture (gate32 lineage), re-keyed for Seat B 36th's five raises, no stack.
Writes only beside this script. Usage: capture_mail_gate34.py <scratchpad dir>"""
import hashlib, json, os, re, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_%s.json' % K['kit']), encoding='utf-8'))
SP = sys.argv[1]
CL = os.path.join(SP, 'g34_sp', 'clone.git')   # the scratch clone predict_gate34.py builds (fetch from origin); capture runs AFTER predict
B36 = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-36th'
PUSHLOG = {   # every path READ by `ls -la 2026-09-28_seatB-36th/raise/` at drafting (2026-09-27 22:3xZ)
    '1316': B36 + '/raise/s-b36-ks1346c-14fc80fb144c-push.out',
    '1317': B36 + '/raise/s-b36-ks1346d-2a688b240549-push.out',
    '1318': B36 + '/raise/s-b36-ks747-62f9a288cf60-push.out',
    '1319': B36 + '/raise/s-b36-ks908-07f42897e2af-push.out',
    '1320': B36 + '/raise/s-b36-ks692-b9111f2bfad2-push.out',
}
FILES = [(B36 + '/quarantine/tsconfig.ks1346c.json', 0), (B36 + '/quarantine/tsconfig.ks1346d.json', 0), (B36 + '/quarantine/tsconfig.ks747.json', 0),
         (B36 + '/quarantine/tsconfig.ks908.json', 0), (B36 + '/quarantine/tsconfig.ks692.json', 0),
         (B36 + '/raise/s-b36-ks1346c-14fc80fb144c-stubs.txt', 0), (B36 + '/raise/s-b36-ks1346d-2a688b240549-stubs.txt', 0), (B36 + '/raise/s-b36-ks747-62f9a288cf60-stubs.txt', 0),
         (B36 + '/raise/s-b36-ks908-07f42897e2af-stubs.txt', 0), (B36 + '/raise/s-b36-ks692-b9111f2bfad2-stubs.txt', 0)]
def sha(t): return hashlib.sha256(t.encode('utf-8')).hexdigest()
def stop(path):
    """bounded-region parse: for each `=== <path> ===` header, the LAST `N passed, M failed` line before the next header"""
    if not os.path.exists(path): return {'log': 'ABSENT'}
    t = open(path, encoding='utf-8', errors='replace').read().splitlines()
    regions, cur = {}, None
    for l in t:
        m = re.match(r'^=== (\S+) ===\s*$', l)
        if m: cur = m.group(1); regions[cur] = []; continue
        if cur: regions[cur].append(l)
    def last(hdr_suffix):
        ks = [k for k in regions if k.endswith(hdr_suffix)]
        if not ks: return 'NOT FOUND'
        c = [re.search(r'(\d+) passed, (\d+) failed', l) for l in regions[ks[-1]]]
        c = [x for x in c if x]
        return '%s/%s' % (c[-1].group(1), c[-1].group(2)) if c else 'HEADER, NO SUMMARY'
    rs = [re.search(r'run_shell_suites: (\d+) passed, (\d+) failed', l) for l in t]; rs = [x for x in rs if x]
    ss = [re.search(r'shell suites: (\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)', l) for l in t]; ss = [x for x in ss if x]
    inc = [l.strip() for l in t if 'PREFLIGHT INCOMPLETE' in l or 'PREFLIGHT PASSED' in l or 'PREFLIGHT FAILED' in l]
    return {'log': path, 'lines': len(t), 'pre_push_hook_base': last('/pre_push_hook_base.test.sh'), 'fixture_guard': last('/pre_push_hook_base_fixture_guard.test.sh'),
            'run_shell_suites_region': last('/run_shell_suites.test.sh'),
            'run_shell_suites_prefixed': ('%s/%s' % (rs[-1].group(1), rs[-1].group(2))) if rs else 'NOT FOUND',
            'shell_suites': ('%s passed, %s failed, %s skipped (of %s)' % ss[-1].groups()) if ss else 'NOT FOUND',
            'CONTROL_absent_header': last('/no_such_suite_gate34_control.test.sh'),
            'fixture_build_failed_lines': sum(1 for l in t if l.startswith('FIXTURE BUILD FAILED')),
            'verdict_line': inc[-1] if inc else 'NONE', 'preflight_ran': any('running preflight gate' in l for l in t),
            'rc': open(path[:-4] + '.rc').read().strip() if os.path.exists(path[:-4] + '.rc') else '?',
            'start': open(path[:-4] + '.start').read().strip() if os.path.exists(path[:-4] + '.start') else '?',
            'end': open(path[:-4] + '.end').read().strip() if os.path.exists(path[:-4] + '.end') else '?'}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# CAPTURE for %s (%s) — %s' % (K['kit'], K['pane'], now), '',
       'NO READY MESSAGE ID reached the drafter for any PR of this kit (a listing would mark mail seen). Each PR\'s seat claims are captured from its',
       'PR BODY, its COMMIT MESSAGES (over its develop merge-base) and the Seat B 36th records below, each verbatim with its TEXT_SHA256.', '']
print('capture_mail_gate34 (%s) %s clone %s' % (K['kit'], now, CL))
counts = {}
for n in sorted(K['prs']):
    p = K['prs'][n]
    body = open(os.path.join(G, 'gh_body_%s.md' % n), encoding='utf-8').read()
    head = body.splitlines()[1].split()[1]
    cb = P['prs'][n]['merge_base']
    assert head == P['prs'][n]['head'], 'gh_body head %s != pinned %s' % (head, P['prs'][n]['head'])
    msg = subprocess.run(['git', '--git-dir', CL, 'log', '--reverse', '--format=--- commit %H%n%B', '%s..%s' % (cb, head)], capture_output=True, text=True).stdout
    s = stop(PUSHLOG[n]); counts[n] = s
    out += ['## #%s %s (Seat %s, %s) — head %s' % (n, ' + '.join(p['keys']), p['seat'], p['tier'], head), '',
            '#%s ticket line: #%s is %s.' % (n, n, ' + '.join(p['keys'])), '',
            '### PR BODY (gh_body_%s.md) TEXT_SHA256 %s' % (n, sha(body)), '', body, '',
            '### EVERY COMMIT MESSAGE IN THE CHAIN over %s (oldest first) TEXT_SHA256 %s' % (cb, sha(msg)), '', msg, '',
            '### PUSH LOG STOP COUNTS (READ, bounded region; %s)' % PUSHLOG[n], '', '```', json.dumps(s, indent=1, ensure_ascii=False), '```', '']
    print('#%s head %s body sha %s msg sha %s | push log: %s' % (n, head, sha(body)[:16], sha(msg)[:16], {k: v for k, v in s.items() if k != 'log'}))
for f, tail in FILES:
    t = open(f, encoding='utf-8', errors='replace').read()
    if tail:
        tl = '\n'.join(t.splitlines()[-tail:])
        out += ['## SEAT RECORD %s — TAIL (last %d of %d lines); the WHOLE file\'s TEXT_SHA256 %s' % (f, tail, len(t.splitlines()), sha(t)), '', tl, '']
    else:
        out += ['## SEAT RECORD %s TEXT_SHA256 %s' % (f, sha(t)), '', t, '']
    print('seat record %s sha %s (%d bytes)%s' % (f, sha(t)[:16], len(t), ' TAIL %d' % tail if tail else ''))
open(os.path.join(G, 'mail_%s_ready.md' % K['kit']), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(counts, open(os.path.join(G, 'stopcounts_%s.json' % K['kit']), 'w'), indent=1)
print('wrote mail_%s_ready.md (%d bytes) and stopcounts_%s.json' % (K['kit'], len('\n'.join(out)), K['kit']))
