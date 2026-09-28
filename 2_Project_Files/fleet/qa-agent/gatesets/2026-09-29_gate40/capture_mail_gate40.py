#!/usr/bin/env python3
"""capture_mail_gate40.py — build the gate's CAPTURE for the gate40 kit (kit.json beside this script): mail_<kit>_ready.md + stopcounts_<kit>.json.

THIS ROUND ONE READY MESSAGE: Seat B 42nd's READY FOR QA mail for #1338 in wednesday-agent@, subject beginning
`[Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 42nd): #1338`. Wednesday's commission named the SUBJECT, not the id: the drafter found the id
by ONE read-only AgentMail API listing of wednesday-agent@ (GET /v0/inboxes/<inbox>/messages — it touches NO seen-state; inbox_digest.sh's seen file
is written only by its own listing modes, never by this script), filtered by that subject prefix (exactly one match, 2026-09-28T22:40:10Z). The
mail is then read BY ID (`inbox_digest.sh full <inbox> <message_id>`) and captured VERBATIM with its TEXT_SHA256; the by-id read's own Subject line must
begin with the prefix (asserted). For the PR the capture also carries (1) the PR BODY (gh_body_<n>.md, as read by gh_read_gate40.py), (2) EVERY commit
message in the PR's chain over its develop merge-base (read from the scratch clone, `git log --format=%B`), (3) the push log's fleet STOP counts, READ
by BOUNDED REGION between consecutive `=== <path> ===` headers, with a NOT-FOUND control (a header that does not exist must read NOT FOUND). Seat B
42nd's push log IS in its record folder this round (2026-09-29_seatB-42nd/raise/s-b42-ks1370-42f8a5abc65e-push.out + .rc/.start/.end, READ by `find`).
SEAT RECORDS captured whole: Seat B 42nd's handover, its three KS-1370 drill outputs (RED at 0de10857, GREEN with the fix, ARMS 16/16), its drill and
arms scripts (session scratchpad — a /private/tmp path that does not survive a reboot), and Seat B 41st's original repro script (the drill Seat B 42nd
re-used). Shape copied from gate39's capture (gate38 -> gate37 lineage), re-keyed for Seat B 42nd, one PR, no local-model READY.
Writes only beside this script. Usage: capture_mail_gate40.py <scratchpad dir>"""
import hashlib, json, os, re, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_%s.json' % K['kit']), encoding='utf-8'))
SP = sys.argv[1]
CL = os.path.join(SP, 'g40_sp', 'clone.git')   # the scratch clone predict_gate40.py builds (fetch from origin); capture runs AFTER predict
B42SP = '/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/5aacd245-a1d2-48d4-a516-8a4ccbbb32d8/scratchpad'   # Seat B 42nd's session scratchpad (READ)
B41SP = '/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad'   # Seat B 41st's (READ: the original KS-1370 repro)
REC = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/'
PUSHLOG = {'1338': REC + '2026-09-29_seatB-42nd/raise/s-b42-ks1370-42f8a5abc65e-push.out'}   # READ by `find` at drafting (2026-09-29 08:5x AEST)
DIGEST = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh'
READY_SUBJECT = {'1338': '[Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 42nd): #1338'}
READY_MAIL = {'1338': '<010001a0ea2cf58b-e6a9f8a3-6338-4012-ba2e-d00cdce350e4-000000@email.amazonses.com>'}   # found by the ONE read-only listing described above
READY_FILE = {}
FILES = [(REC + 'HANDOVER-seatB42-2026-09-29.md', 0), (REC + '2026-09-29_seatB-42nd/ks1370/RED-at-0de10857.txt', 0), (REC + '2026-09-29_seatB-42nd/ks1370/GREEN-with-fix.txt', 0),
         (REC + '2026-09-29_seatB-42nd/ks1370/ARMS-16-of-16.txt', 0), (B42SP + '/drill/ks1370drill.cjs', 0), (B42SP + '/drill/ks1370arms.cjs', 0), (B41SP + '/ks1370drill.cjs', 0)]
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
            'CONTROL_absent_header': last('/no_such_suite_gate40_control.test.sh'),
            'fixture_build_failed_lines': sum(1 for l in t if l.startswith('FIXTURE BUILD FAILED')),
            'verdict_line': inc[-1] if inc else 'NONE', 'preflight_ran': any('running preflight gate' in l for l in t),
            'rc': open(path.rsplit('.', 1)[0] + '.rc').read().strip() if os.path.exists(path.rsplit('.', 1)[0] + '.rc') else '?',
            'start': open(path.rsplit('.', 1)[0] + '.start').read().strip() if os.path.exists(path.rsplit('.', 1)[0] + '.start') else '?',
            'end': open(path.rsplit('.', 1)[0] + '.end').read().strip() if os.path.exists(path.rsplit('.', 1)[0] + '.end') else '?'}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# CAPTURE for %s (%s) — %s' % (K['kit'], K['pane'], now), '',
       'Seat B 42nd\'s READY FOR QA MAIL for #1338 (its id found by ONE read-only API listing filtered by the commissioned subject prefix, then read BY ID from',
       'wednesday-agent@) is captured VERBATIM below with its TEXT_SHA256, beside the PR\'s BODY, its COMMIT MESSAGE (over its develop merge-base) and its push log\'s STOP counts.', '']
print('capture_mail_gate40 (%s) %s clone %s' % (K['kit'], now, CL))
counts = {}
for n in sorted(K['prs']):
    p = K['prs'][n]
    body = open(os.path.join(G, 'gh_body_%s.md' % n), encoding='utf-8').read()
    head = body.splitlines()[1].split()[1]
    cb = P['prs'][n]['merge_base']
    assert head == P['prs'][n]['head'], 'gh_body head %s != pinned %s' % (head, P['prs'][n]['head'])
    msg = subprocess.run(['git', '--git-dir', CL, 'log', '--reverse', '--format=--- commit %H%n%B', '%s..%s' % (cb, head)], capture_output=True, text=True).stdout
    s = stop(PUSHLOG[n]); counts[n] = s
    if n in READY_MAIL:
        r = subprocess.run(['bash', DIGEST, 'full', 'wednesday-agent@agentmail.to', READY_MAIL[n]], capture_output=True, text=True)
        assert r.returncode == 0 and r.stdout.strip(), 'READY mail for #%s unreadable (rc %d): %s' % (n, r.returncode, r.stderr[-300:])
        rtxt, rsrc = r.stdout, 'READY FOR QA MAIL %s (wednesday-agent@, inbox_digest.sh full, by id)' % READY_MAIL[n]
        assert head[:12] in rtxt, 'the READY mail for #%s does not name the pinned head %s' % (n, head[:12])
        subj = [l for l in rtxt.splitlines() if l.startswith('Subject: ')][:1]
        assert subj and subj[0][len('Subject: '):].startswith(READY_SUBJECT[n]), 'the by-id read of #%s is not the commissioned READY (subject %r)' % (n, subj)
    else:
        rtxt, rsrc = open(READY_FILE[n], encoding='utf-8').read(), 'LOCAL-MODEL READY FILE %s (no READY mail id reached the drafter)' % READY_FILE[n]
    if n in READY_MAIL and n in READY_FILE:   # both: the seat's mail AND the local-model READY file the PR was raised from
        ft = open(READY_FILE[n], encoding='utf-8').read()
        rtxt, rsrc = rtxt + '\n\n### LOCAL-MODEL READY FILE %s TEXT_SHA256 %s\n\n' % (READY_FILE[n], sha(ft)) + ft, rsrc + ' + the local-model READY file'
    out += ['## #%s %s (Seat %s, %s) — head %s' % (n, ' + '.join(p['keys']), p['seat'], p['tier'], head), '',
            '#%s ticket line: #%s is %s.' % (n, n, ' + '.join(p['keys'])), '',
            '### %s TEXT_SHA256 %s' % (rsrc, sha(rtxt)), '', rtxt, '',
            '### PR BODY (gh_body_%s.md) TEXT_SHA256 %s' % (n, sha(body)), '', body, '',
            '### EVERY COMMIT MESSAGE IN THE CHAIN over %s (oldest first) TEXT_SHA256 %s' % (cb, sha(msg)), '', msg, '',
            '### PUSH LOG STOP COUNTS (READ, bounded region; %s)' % PUSHLOG[n], '', '```', json.dumps(s, indent=1, ensure_ascii=False), '```', '']
    print('#%s head %s ready sha %s (%s) body sha %s msg sha %s | push log: %s' % (n, head, sha(rtxt)[:16], rsrc[:40], sha(body)[:16], sha(msg)[:16], {k: v for k, v in s.items() if k != 'log'}))
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
