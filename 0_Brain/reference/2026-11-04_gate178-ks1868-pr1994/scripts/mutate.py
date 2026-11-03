#!/usr/bin/env python3
"""Gate 178 mutants: 8 sites x 7 kinds on nft.routes.ts at head; each run = the PR's 8 new test files (32 cells).
Writes runs/mutants.json (raw table). Restores the head blob at the end and checks its hash."""
import json, subprocess, sys, os

W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate178-ks1868-pr1994'
R = W + '/repo'
S = R + '/Blockchain/Dev/services/nft-certificate'
F = S + '/src/routes/nft.routes.ts'
HEAD = subprocess.check_output(['git', '-C', R, 'show', '74dc459edbb6:Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts'], text=True)
ENV = {'PATH': os.environ['PATH'], 'HOME': W + '/home', 'TMPDIR': W + '/tmp'}

GUARD = ("    let reason: string;\n    try {\n      reason = error instanceof Error ? error.message : String(error);\n"
         "    } catch {\n      reason = 'unreadable thrown value';\n    }\n")
assert HEAD.count(GUARD) == 8, HEAD.count(GUARD)

SITES = ['Error estimating cost', 'Error fetching certificates', 'Error fetching certificate\'', 'Error fetching tiers',
         'Error verifying transaction', 'Error verifying asset', 'Error pinning CID', 'Error unpinning CID']

def site_span(src, k):
    """Return (start, end) of the k-th guard block plus its logger line and the reply statement."""
    pos = -1
    for _ in range(k + 1):
        pos = src.index(GUARD, pos + 1)
    end = src.index('  }\n});', pos)
    return pos, end

KINDS = {
    'K1 raw read (guard removed)': lambda b: b.replace(GUARD, "    const reason = error instanceof Error ? error.message : String(error);\n"),
    'K2 constant changed': lambda b: b.replace("'unreadable thrown value'", "'gate178 other text'"),
    'K3 inner catch rethrows': lambda b: b.replace("    } catch {\n      reason = 'unreadable thrown value';", "    } catch (e) {\n      throw e;"),
    'K4 Error branch dropped (always String)': lambda b: b.replace("error instanceof Error ? error.message : String(error)", "String(error)"),
    'K5 logger.error dropped': lambda b: b.replace("    logger.error(", "    void (", 1),
    'K6 reply status 500->200': lambda b: b.replace("res.status(500)", "res.status(200)", 1),
    'K7 reply dropped': lambda b: b[:b.index('    res.status(500)')] + "    return;\n" + b[b.index('    res.status(500)'):],
}

def run():
    out = W + '/tmp/mut.json'
    p = subprocess.run([S + '/node_modules/.bin/vitest', 'run', '--root', S, '--reporter=json', '--outputFile=' + out, 'catch-guard-catch'],
                       env=ENV, capture_output=True, text=True, timeout=300)
    d = json.load(open(out))
    failed = [(f['name'].split('/')[-1][:40], a['title'][:22]) for f in d['testResults'] for a in f['assertionResults'] if a['status'] != 'passed']
    return p.returncode, d['numTotalTests'], failed

rows = []
try:
    # control: unmutated head
    open(F, 'w').write(HEAD)
    rc, tot, failed = run()
    rows.append({'site': '-', 'kind': 'CONTROL unmutated head', 'rc': rc, 'total': tot, 'failed': len(failed), 'verdict': 'pass' if not failed else 'FAIL'})
    for k, site in enumerate(SITES):
        for kind, fn in KINDS.items():
            a, b = site_span(HEAD, k)
            block = HEAD[a:b]
            nb = fn(block)
            assert nb != block, (site, kind)
            assert site.rstrip("'") in block
            open(F, 'w').write(HEAD[:a] + nb + HEAD[b:])
            rc, tot, failed = run()
            rows.append({'site': site.rstrip("'"), 'kind': kind, 'rc': rc, 'total': tot, 'failed': len(failed),
                         'verdict': 'KILLED' if failed else 'SURVIVED', 'by': sorted({x[1] for x in failed})})
            print(rows[-1]['site'], '|', kind, '|', rows[-1]['verdict'], len(failed), flush=True)
finally:
    open(F, 'w').write(HEAD)
    h = subprocess.check_output(['git', 'hash-object', F], text=True).strip()[:9]
    print('restored', h)
    json.dump(rows, open(W + '/runs/mutants.json', 'w'), indent=1)
