#!/usr/bin/env python3
"""capture_mail_gate29.py — build the gate's CAPTURE for ONE gate29 kit (kit.json beside this script): mail_<kit>_ready.md.

NO READY MESSAGE ID reached the drafter for either PR (Wednesday relayed heads read by ls-remote, with no message id): the seat records
(HANDOVER-seatB31-2026-09-26.md, 2026-09-26_seatB-31st/raise/) carry no agentmail message id, and finding a mail without its id needs an inbox
LISTING, which marks mail seen — forbidden. So each seat claim is captured from (1) the PR BODY (gh_body_<n>.md, as read by gh_read_gate29.py),
(2) EVERY commit message in the PR's chain (read from the scratch clone, `git show -s --format=%B`), (3) the seat records below, verbatim, each
with its TEXT_SHA256 (Seat B 31st's handover and its red/green/arm/lint outputs for #1290 and #1291).
Each PR's push log is READ for the fleet STOP counts by BOUNDED REGION between consecutive `=== <path> ===` headers (Seat L8's handover rule: the
log carries two summary forms and a prefix parser under-reports), with a NOT-FOUND control (a header that does not exist must read NOT FOUND).
Writes only beside this script. Usage: capture_mail_gate29.py <scratchpad dir>"""
import hashlib, json, os, re, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
SP = sys.argv[1]
CL = os.path.join(SP, 'g29_sp', 'clone.git')   # the scratch clone predict_gate29.py builds (fetch from origin); capture runs AFTER predict
H = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History'
B31 = H + '/2026-09-26_seatB-31st/raise'
PUSHLOG = {   # every path READ by `ls -t 2026-09-26_seatB-31st/raise/` at drafting (2026-09-26 09:1xZ)
    '1290': B31 + '/s-b31-ks1341b-a53228515d25-push.out',
    '1291': B31 + '/s-b31-ks1337-2c9022c519bd-push.out',     # a systemTest/ push: the format gate only, NO platform preflight
}
FILES = [H + '/HANDOVER-seatB31-2026-09-26.md',             # Seat B 31st: gate28 merges, KS-1344/1345 filed, the lock + containment traps
         B31 + '/b31-1341b-RED.out', B31 + '/b31-1341b-GREEN.out',     # #1290: red-first (cell alone) and green
         B31 + '/b31-1341b-armR3.out', B31 + '/armR3.py',               # #1290: the seat's arm R3 (production-only logger) and its script
         B31 + '/b31-1341b-lint-HEAD.out',                              # #1290: originate lint at head (22 warnings)
         B31 + '/b31-1337-RED.out', B31 + '/b31-1337-GREEN.out',       # #1291: red-first and green
         B31 + '/b31-1337-lint-HEAD.out', B31 + '/b31-1337-fmt.diff', B31 + '/b31-1337-lint-FINAL.out',   # #1291: 6 prettier errors -> eslint --fix -> rc 0
         B31 + '/b31-1337-BARE.out', B31 + '/b31-1337-PATCHED.out',    # #1291: the performance unit suite 1114 -> 1117
         B31 + '/b31-1337-push-console.log']                           # #1291: the push console (format gate only)
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
            'CONTROL_absent_header': last('/no_such_suite_gate29_control.test.sh'),
            'fixture_build_failed_lines': sum(1 for l in t if l.startswith('FIXTURE BUILD FAILED')),
            'verdict_line': inc[-1] if inc else 'NONE', 'preflight_ran': any('running preflight gate' in l for l in t),
            'rc': open(path[:-4] + '.rc').read().strip() if os.path.exists(path[:-4] + '.rc') else '?',
            'start': open(path[:-4] + '.start').read().strip() if os.path.exists(path[:-4] + '.start') else '?',
            'end': open(path[:-4] + '.end').read().strip() if os.path.exists(path[:-4] + '.end') else '?'}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# CAPTURE for %s (%s) — %s' % (K['kit'], K['pane'], now), '',
       'NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR\'s seat',
       'claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.', '']
print('capture_mail_gate29 (%s) %s clone %s' % (K['kit'], now, CL))
counts = {}
for n in sorted(K['prs']):
    p = K['prs'][n]
    body = open(os.path.join(G, 'gh_body_%s.md' % n), encoding='utf-8').read()
    head = body.splitlines()[1].split()[1]
    mb = subprocess.run(['git', '--git-dir', CL, 'merge-base', 'refs/g29/develop', head], capture_output=True, text=True).stdout.strip()
    msg = subprocess.run(['git', '--git-dir', CL, 'log', '--reverse', '--format=--- commit %H%n%B', '%s..%s' % (mb, head)], capture_output=True, text=True).stdout
    s = stop(PUSHLOG[n]); counts[n] = s
    out += ['## #%s %s (Seat %s, %s) — head %s' % (n, ' + '.join(p['keys']), p['seat'], p['tier'], head), '',
            '#%s ticket line: #%s is %s.' % (n, n, ' + '.join(p['keys'])), '',
            '### PR BODY (gh_body_%s.md) TEXT_SHA256 %s' % (n, sha(body)), '', body, '',
            '### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 %s' % sha(msg), '', msg, '',
            '### PUSH LOG STOP COUNTS (READ, bounded region; %s)' % PUSHLOG[n], '', '```', json.dumps(s, indent=1), '```', '']
    print('#%s head %s body sha %s msg sha %s | push log: %s' % (n, head, sha(body)[:16], sha(msg)[:16], {k: v for k, v in s.items() if k != 'log'}))
for f in FILES:
    t = open(f, encoding='utf-8').read()
    out += ['## SEAT RECORD %s TEXT_SHA256 %s' % (f, sha(t)), '', t, '']
    print('seat record %s sha %s (%d bytes)' % (f, sha(t)[:16], len(t)))
open(os.path.join(G, 'mail_%s_ready.md' % K['kit']), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(counts, open(os.path.join(G, 'stopcounts_%s.json' % K['kit']), 'w'), indent=1)
print('wrote mail_%s_ready.md (%d bytes) and stopcounts_%s.json' % (K['kit'], len('\n'.join(out)), K['kit']))
