"""G189 judge: head vs base, per cell. Usage: python3 -I judge.py base.jsonl head.jsonl [--exclude-row X]
Permissiveness ranks (higher = more permissive):
  create: 2 = passed and SKIPPED the workflow gate (forwarded to originate), 1 = passed through the workflow gate,
          0 = refused (any non-2xx, including a hang).
  info:   non-200 = (0,); 200 -> compare allow-list sets ([] = everything) and workflowPolicy bypass.
  put:    (rank of the follow-up restricted create after the save, put 2xx?) lexicographic.
"""
import json, sys, collections

def load(p):
    d = {}
    for l in open(p):
        r = json.loads(l)
        d[(r['reader'], r['redis'], r['key'], r['row'])] = r
    return d

def crank(o):
    if 200 <= o['status'] < 300:
        return 2 if o['path'] == 'orig' else 1
    return 0

def cmp_info(b, h):
    if b['status'] != 200 and h['status'] != 200: return 0
    if b['status'] != 200: return 1
    if h['status'] != 200: return -1
    bt, ht = b['types'], h['types']
    loose = strict = False
    if not ht and bt: loose = True
    elif ht and not bt: strict = True
    elif ht and bt:
        if not set(ht) <= set(bt): loose = True
        if not set(bt) <= set(ht): strict = True
    bb, hb = b['policy'] == 'bypass', h['policy'] == 'bypass'
    if hb and not bb: loose = True
    if bb and not hb: strict = True
    if loose: return 1
    if strict: return -1
    return 0

def cmp(reader, b, h):
    if reader.startswith('create'):
        x, y = crank(b), crank(h)
    elif reader == 'info':
        return cmp_info(b, h)
    else:
        x = (crank(b['follow']), 1 if 200 <= b['status'] < 300 else 0)
        y = (crank(h['follow']), 1 if 200 <= h['status'] < 300 else 0)
    return (y > x) - (y < x)

def outcome(r):
    if r['reader'].startswith('create'): return f"{r['status']} {r['code'] or r['path']}"
    if r['reader'] == 'info': return f"{r['status']} {r['code'] or (r['types'], r['policy'])}"
    return f"{r['status']} {r['code'] or ''} sets={r['sets']} row={r['rowOriginAfter']} follow={r['follow']['status']} {r['follow']['code'] or r['follow']['path']}"

base, head = load(sys.argv[1]), load(sys.argv[2])
assert set(base) == set(head), 'cell sets differ'
tot = collections.Counter(); per = collections.defaultdict(collections.Counter)
loose_list, strict_list, byp_diff = [], [], []
ident = 0
for k in sorted(base):
    reader, redis, key, row = k
    c = cmp(reader, base[k], head[k])
    bypass = key == 'B' or row == 'B'
    if bypass:
        tot['bypass_cells'] += 1
        if outcome(base[k]) != outcome(head[k]): byp_diff.append((k, c, outcome(base[k]), outcome(head[k])))
        if c > 0: tot['bypass_looser'] += 1
        continue
    tot['ratio_cells'] += 1
    lab = {1: 'looser', -1: 'stricter', 0: 'same'}[c]
    tot[lab] += 1; per[reader][lab] += 1
    if outcome(base[k]) == outcome(head[k]): ident += 1
    if c > 0: loose_list.append((k, outcome(base[k]), outcome(head[k])))
    if c < 0: strict_list.append((k, outcome(base[k]), outcome(head[k])))

print('cells', len(base), dict(tot), 'byte-identical outcomes among ratio cells:', ident)
for r in sorted(per): print('  ', r, dict(per[r]))
print('LOOSER (ratio cells):', len(loose_list))
for x in loose_list: print('  ', x)
print('STRICTER (ratio cells):', len(strict_list))
for x in strict_list: print('  ', x)
print('BYPASS cells that differ:', len(byp_diff))
for x in byp_diff: print('  ', x)
