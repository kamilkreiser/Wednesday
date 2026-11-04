import json, sys, collections
base = json.load(open(sys.argv[1])); head = json.load(open(sys.argv[2]))
def ok(s): return 200 <= s < 400
out = []
for mode in ['matrixTest', 'matrixProd']:
    b = {(r['op'], r['shape']): r for r in base[mode]}
    h = {(r['op'], r['shape']): r for r in head[mode]}
    assert set(b) == set(h), 'cell sets differ'
    perm = []; changed = collections.Counter(); same = collections.Counter(); headRepNotRefused = []
    for k in sorted(b):
        rb, rh = b[k], h[k]
        more = rh['hits'] > rb['hits'] or (ok(rh['status']) and not ok(rb['status'])) or (rh['auth'] != rb['auth'] and 'bearer' in rh['auth'] and 'bearer' not in rb['auth'])
        if more: perm.append((k, rb, rh))
        key = (k[1], (rb['status'], rb['hits'], rb['validations']) == (rh['status'], rh['hits'], rh['validations']))
        (same if key[1] else changed)[k[1]] += 1
        if k[1].startswith('rep') and not (rh['status'] == 400 and rh['code'] == 'BAD_REQUEST' and rh['hits'] == 0 and rh['validations'] == 0):
            headRepNotRefused.append((k, rh))
    repBasePerm = sum(1 for k in b if k[1].startswith('rep') and (b[k]['hits'] > 0))
    print(f"{mode}: cells={len(b)} head-more-permissive={len(perm)} head-repeated-not-refused={len(headRepNotRefused)} base-repeated-forwarded={repBasePerm}")
    print('  unchanged by shape:', dict(same)); print('  changed by shape:', dict(changed))
    for p in perm[:20]: print('  MORE PERMISSIVE', p)
    for p in headRepNotRefused[:20]: print('  NOT REFUSED', p)
    # zero/one-key cells that changed at all
    diffs = [(k, b[k], h[k]) for k in sorted(b) if not k[1].startswith('rep') and (b[k]['status'], b[k]['hits'], b[k]['validations'], b[k]['auth']) != (h[k]['status'], h[k]['hits'], h[k]['validations'], h[k]['auth'])]
    print(f'  zero/one-key cells that differ base->head: {len(diffs)}')
    for d in diffs[:20]: print('   ', d)
