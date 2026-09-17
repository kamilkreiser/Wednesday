#!/usr/bin/env python3
"""drafter_probe_tamper.py ROW... — run qa1023-drafter-probe (QA_STAGES=test,limiter) on the HEAD tree under a drafter G tamper (forms read from drafter_tamper.py's
ROWS by exec of its ROWS block only), then compare to the untampered head rows: does the drafter's instrument see what the seat's suite does not? Restore by bytes + sha."""
import hashlib, json, os, re, subprocess, sys, datetime
GSD = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GSD + '/drafter_paths.json')); WT = PA['trees']['head']; DEVT = PA['trees']['dev']
AU = WT + '/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
src = open(GSD + '/drafter_tamper.py').read(); blk = src[src.index("REQ = "):src.index("def ts():")]
ns = {'open': open, 'PA': PA}; exec("DEVT = PA['trees']['dev']\n" + blk, ns); ROWS = {r[0]: r for r in ns['ROWS']}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def P(*a): print(' '.join(str(x) for x in a), flush=True)
BASE = json.load(open(GSD + '/rows/rows_head_head.json'))
def cell(r): f = r.get('fwd') or []; return (r['status'], r['code'], tuple(x['userId'] for x in f), tuple(x['bearerSub'] for x in f), tuple((t or 'null') for t in (r.get('tenants') or [])), len(r.get('incr') or []))
for rid in sys.argv[1:]:
    _, anchor, repl, _, _, names = ROWS[rid]
    orig = open(AU, 'rb').read(); osha = sha(AU); assert orig.decode().count(anchor) == 1
    open(AU, 'wb').write(orig.decode().replace(anchor, repl).encode()); P(datetime.datetime.now().strftime('%H:%M:%S'), rid, 'applied', sha(AU) != osha, '|', names)
    try:
        env = dict(os.environ, QA_LABEL='tamper_' + rid, QA_STAGES='test,limiter')
        p = subprocess.run(['python3', GSD + '/drafter_run.py', 'probe', 'head'], env=env, capture_output=True, text=True); P(p.stdout.strip().splitlines()[1][:300] if p.stdout.strip() else p.stderr[-500:])
    finally:
        open(AU, 'wb').write(orig); P('restored sha equal', sha(AU) == osha, 'git diff --quiet', subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD']).returncode == 0)
    T = json.load(open(GSD + '/rows/rows_tamper_%s.json' % rid))
    for stage in ('test', 'limiter'):
        d = [(b.get('prefix', ''), b.get('mount', b.get('id')), b.get('case', ''), cell(b), cell(t)) for b, t in zip(BASE[stage], T[stage]) if cell(b) != cell(t)]
        if stage == 'limiter':  # per-request random keys make bucket hashes differ; compare shape only
            d = [x for x in d if x[3][:5] != x[4][:5] or x[3][5] != x[4][5]]
        P('  ', rid, stage, 'rows differing from untampered head:', len(d))
        for x in d[:8]: P('     ', x[0], x[1], x[2], '| head', x[3], '| tampered', x[4])
