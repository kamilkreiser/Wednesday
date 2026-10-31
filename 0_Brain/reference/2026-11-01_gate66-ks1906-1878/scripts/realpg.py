#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate66-ks1906-1878/scripts')
import run as R
res = {}
def go(tag, edits):
    for db in ('g66boot', 'g66mig'):
        with R.swapped(edits):
            rc, st = R.probe(tag, db)
        red = sorted(k for k, v in st.items() if v != 'passed')
        res[f'{tag}/{db}'] = {'rc': rc, 'n': len(st), 'red': red}
        print(tag, db, 'rc', rc, 'cells', len(st), 'red', len(red), flush=True)
mode = sys.argv[1]
if mode == 'head': go('head', [])
if mode == 'base': go('baseprod', [(r, None, R.base_bytes(r)) for r in R.PROD])
json.dump(res, open(R.G + f'/evidence/realpg_summary_{mode}.json', 'w'), indent=1)
