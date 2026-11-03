# q2bar.py: class bar + sentinel for the originate dispatchEvent cells (reference = base V01 per site).
import json
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992/results/'
B = [json.loads(l) for l in open(W + 'q2_base.jsonl')]; H = [json.loads(l) for l in open(W + 'q2_head.jsonl')]
K = lambda r: (r['out'], r['rowsLogged'].replace(':object', ':x').replace(':string', ':x').replace(':symbol', ':x'), r['sentToStandIn'])
ref = {r['site']: K(r) for r in B if r['value'].startswith('V01')}
tot = eq = chg = 0; more_sent = 0; sb = sh = 0; hm = 0; bad = []
for b, h in zip(B, H):
    sb += b['sentinelLines']; sh += h['sentinelLines']; hm += h['sentinelLines'] > b['sentinelLines']
    if b['value'].startswith('V01'): continue
    tot += 1; e = K(h) == ref[b['site']]; eq += e; chg += K(b) != K(h)
    if len(h['sentToStandIn'].split(',')) > len(ref[b['site']][2].split(',')) or 'wh1' in h['sentToStandIn']: more_sent += 1
    if not e: bad.append((b['site'], b['value'], K(b), K(h)))
print(f'Q2 non-ordinary cells {tot}; head = base-ordinary {eq}; changed {chg}; head sends beyond base-ordinary (or to wh1) {more_sent}')
for x in bad: print('  head!=base-ordinary', x)
print(f'sentinel log lines base {sb} head {sh}; cells head prints more {hm}')
