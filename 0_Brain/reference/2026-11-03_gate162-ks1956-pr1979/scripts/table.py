#!/usr/bin/env python3
# Condense logs/probe/*.json into logs/probe_table.log (one block per cell, base then head).
import json, glob, os, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979'
out = []
files = sorted(glob.glob(W + '/logs/probe/*.json'), key=lambda f: (os.path.basename(f).split('__')[1], os.path.basename(f).split('__')[2], os.path.basename(f).split('__')[0]))
SKIP = {'ver', 'cell', 'mr', 'tree', 'at', 'logLines'}
for f in files:
    d = json.load(open(f))
    out.append(f"=== {d['ver']} {d['cell']} mr={d['mr']}  counts={d.get('counts')}  boot={d.get('boot')}")
    for k, v in d.items():
        if k in SKIP or k == 'counts' or k == 'boot': continue
        out.append(f"  {k}: {json.dumps(v, default=str)[:900]}")
    errs = [l for p in d.get('logLines', []) for l in p if ' error: ' in l or ' warn: ' in l]
    for l in errs[:8]: out.append('  LOG ' + l[24:200])
open(W + '/logs/probe_table.log', 'w').write('\n'.join(out) + '\n')
print(len(files), 'cells')
