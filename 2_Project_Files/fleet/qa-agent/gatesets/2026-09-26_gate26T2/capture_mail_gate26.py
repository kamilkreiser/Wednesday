#!/usr/bin/env python3
"""capture_mail_gate26.py — build the gate's CAPTURE for ONE gate26 kit (kit.json beside this script): mail_<kit>_ready.md.

NO READY MESSAGE ID reached the drafter for any of the eleven PRs (Wednesday relayed heads "per mail", with no message id): the seat records
(HANDOVER-seatL7-2026-09-26.md, 2026-09-26_seatL7/, 2026-09-26_seatB-29th/, 2026-09-26_seatB-30th/) carry no agentmail message id, and finding a
mail without its id needs an inbox LISTING, which marks mail seen — forbidden. So each seat
claim is captured from (1) the PR BODY (gh_body_<n>.md, as read by gh_read_gate26.py), (2) the head COMMIT MESSAGE (read from the scratch clone,
`git show -s --format=%B`), (3) the seat HANDOVER files, verbatim, each with its TEXT_SHA256, and (4) Seat L8's FLEET measurement on d7cdecf1.
Each PR's push log is READ for the fleet STOP counts by BOUNDED REGION between consecutive `=== <path> ===` headers (Seat L8's handover rule: the
log carries two summary forms and a prefix parser under-reports), with a NOT-FOUND control (a header that does not exist must read NOT FOUND).
Writes only beside this script. Usage: capture_mail_gate26.py <scratchpad dir>"""
import hashlib, json, os, re, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
SP = sys.argv[1]
CL = os.path.join(SP, 'g26_sp', 'clone.git')   # the scratch clone predict_gate26.py builds (fetch from origin); capture runs AFTER predict
H = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History'
PUSHLOG = {   # every path READ by `find -name "*<head12>*push.out"` under 5_Project_History at drafting (2026-09-26 ~09:4x AEST)
    '1245': H + '/2026-09-26_seatB-29th/raise/s-b29-pr1245-ff-cb31a58c190f-push.out',
    '1275': H + '/2026-09-26_seatL7/raise/s-l7-ks1179-d852e56b912f-push.out',
    '1276': H + '/2026-09-26_seatB-29th/raise/s-b29-ks794-737a4069c631-push.out',
    '1277': H + '/2026-09-26_seatL7/raise/s-l7-ks1319-702171eaadbe-push.out',
    '1278': H + '/2026-09-26_seatL7/raise/s-l7-ks1314-c321bcce2a9a-push.out',
    '1279': H + '/2026-09-26_seatB-29th/raise/s-b29-ks1306-dabde931df5e-push.out',
    '1280': H + '/2026-09-26_seatB-29th/raise/s-b29-ks1129-12c197a9215e-push.out',
    '1281': H + '/2026-09-26_seatB-29th/raise/s-b29-ks1074-c3374e3129cc-push.out',
    '1282': H + '/2026-09-26_seatB-29th/raise/s-b29-ks730a-34a67a9e4805-push.out',
    '1283': H + '/2026-09-26_seatB-29th/raise/s-b29-ks730b-f92b7c19e98d-push.out',
    '1284': 'LOCATED AT RUN TIME',
    '1274': H + '/2026-09-26_seatB-30th/raise/s-b30-ks934-ff-8e94f5fb3e6d-push.out',   # round 2 (the fix round), READ by find at 10:3x
    '1268': H + '/2026-09-26_seatB-30th/raise/s-b30-ks1318-ff-5ac42fafeee1-push.out',   # round 2 (the fix round), READ by find at 10:4x
    '1261': H + '/2026-09-26_seatB-30th/raise/s-b30-ks1293-ff-0b2fdbb1b819-push.out',   # round 2 (the fix round), READ by find at 10:5x
}
import glob
_p1284 = sorted(glob.glob(H + '/2026-09-26_seatB-30th/raise/*dfc2468a547f*push.out') + glob.glob(H + '/2026-09-26_seatB-29th/raise/*dfc2468a547f*push.out'))
PUSHLOG['1284'] = _p1284[-1] if _p1284 else H + '/2026-09-26_seatB-30th/raise/NO-PUSH-LOG-FOUND-for-dfc2468a547f-push.out'
FILES = [H + '/2026-09-26_seatL8/measurements/fleet-measurement-RESULT-d7cdecf1.md']   # the fleet count on develop d7cdecf1 (Seat L8)
if any(K['prs'][n]['seat'] == 'L7' for n in K['prs']): FILES.append(H + '/HANDOVER-seatL7-2026-09-26.md')
# Seat B 29th and Seat B 30th left NO handover file at drafting (their dirs hold lock-holder.json, lock-released.txt and raise/ only — READ)
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
            'CONTROL_absent_header': last('/no_such_suite_gate26_control.test.sh'),
            'fixture_build_failed_lines': sum(1 for l in t if l.startswith('FIXTURE BUILD FAILED')),
            'verdict_line': inc[-1] if inc else 'NONE', 'preflight_ran': any('running preflight gate' in l for l in t),
            'rc': open(path[:-4] + '.rc').read().strip() if os.path.exists(path[:-4] + '.rc') else '?',
            'start': open(path[:-4] + '.start').read().strip() if os.path.exists(path[:-4] + '.start') else '?',
            'end': open(path[:-4] + '.end').read().strip() if os.path.exists(path[:-4] + '.end') else '?'}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# CAPTURE for %s (%s) — %s' % (K['kit'], K['pane'], now), '',
       'NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR\'s seat',
       'claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.', '']
print('capture_mail_gate26 (%s) %s clone %s' % (K['kit'], now, CL))
counts = {}
for n in sorted(K['prs']):
    p = K['prs'][n]
    body = open(os.path.join(G, 'gh_body_%s.md' % n), encoding='utf-8').read()
    head = body.splitlines()[1].split()[1]
    msg = subprocess.run(['git', '--git-dir', CL, 'show', '-s', '--format=%B', head], capture_output=True, text=True).stdout
    s = stop(PUSHLOG[n]); counts[n] = s
    out += ['## #%s %s (Seat %s, %s) — head %s' % (n, ' + '.join(p['keys']), p['seat'], p['tier'], head), '',
            '#%s ticket line: #%s is %s.' % (n, n, ' + '.join(p['keys'])), '',
            '### PR BODY (gh_body_%s.md) TEXT_SHA256 %s' % (n, sha(body)), '', body, '',
            '### HEAD COMMIT MESSAGE TEXT_SHA256 %s' % sha(msg), '', msg, '',
            '### PUSH LOG STOP COUNTS (READ, bounded region; %s)' % PUSHLOG[n], '', '```', json.dumps(s, indent=1), '```', '']
    print('#%s head %s body sha %s msg sha %s | push log: %s' % (n, head, sha(body)[:16], sha(msg)[:16], {k: v for k, v in s.items() if k != 'log'}))
for f in FILES:
    t = open(f, encoding='utf-8').read()
    out += ['## SEAT RECORD %s TEXT_SHA256 %s' % (f, sha(t)), '', t, '']
    print('seat record %s sha %s (%d bytes)' % (f, sha(t)[:16], len(t)))
open(os.path.join(G, 'mail_%s_ready.md' % K['kit']), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(counts, open(os.path.join(G, 'stopcounts_%s.json' % K['kit']), 'w'), indent=1)
print('wrote mail_%s_ready.md (%d bytes) and stopcounts_%s.json' % (K['kit'], len('\n'.join(out)), K['kit']))
