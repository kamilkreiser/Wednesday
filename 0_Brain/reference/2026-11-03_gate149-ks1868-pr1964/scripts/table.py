# Class-bar table: for every (route, layer, point, value), compare head-unreadable after-state vs base-ordinary after-state, per env.
import json, collections
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964'
D = {}
for v in ['base', 'head', 'merged', 'devnow']:
    for e in ['development', 'production']:
        for l in open(f'{W}/logs/probe/{v}_{e}.jsonl'):
            d = json.loads(l); D[(v, e, d['route'], d['layer'], d['point'], d['value'])] = d
def outcome(d):
    return (d['first']['status'], d['first']['code'], json.dumps(d['after1'], sort_keys=True), d['nonceLeft'],
            json.dumps(d['retry']), json.dumps(d['after2'], sort_keys=True), d['unhandled'] > 0, d['uncaught'] > 0)
UNREAD = ['revokedProxy', 'getterThrows', 'getterThrowsRevoked', 'msgBigInt', 'msgNullProto', 'msgSymbol']
ALLV = ['ordinary', 'plainString'] + UNREAD
viol = []; n = 0
rows = collections.OrderedDict()
for (v, e, r, L, p, val), d in D.items():
    if v != 'head' or val == 'none': continue
    ref = D[('base', e, r, L, p, 'ordinary')]
    n += 1
    if outcome(d) != outcome(ref): viol.append((e, r, L, p, val, outcome(d), outcome(ref)))
    m = D[('merged', e, r, L, p, val)]
    if outcome(m) != outcome(d): viol.append(('MERGED!=HEAD', e, r, L, p, val))
    dn = D[('devnow', e, r, L, p, val)]
    if outcome(dn) != outcome(D[('base', e, r, L, p, val)]): viol.append(('DEVNOW!=BASE', e, r, L, p, val))
print(f'head cells compared to base-ordinary (same env/route/injection): {n}; differences: {len(viol)}')
for x in viol: print('  DIFF', x)
# compact per-injection table (development), base by value vs head
print('\nroute/layer/point | base: per value (status; U=unhandled X=uncaught->index.ts exits) | head: all values')
for e in ['development', 'production']:
    print(f'\n== {e}')
    keys = sorted({(r, L, p) for (v, ee, r, L, p, val) in D if ee == e}, key=lambda k: list(D).index(next(kk for kk in D if kk[2:5] == k)))
    for k in keys:
        def cell(v, val):
            d = D.get((v, e) + k + (val,))
            if not d: return '-'
            s = str(d['first']['status'] or 'HANG')
            if d['uncaught']: s += 'X'
            elif d['unhandled']: s += 'U'
            return s
        base = ' '.join(f'{val}={cell("base", val)}' for val in ALLV)
        head = ' '.join(f'{val}={cell("head", val)}' for val in ALLV)
        a = D[('base', e) + k + ('ordinary',)]
        post = ''
        if a['retry'] is not None:
            post = f" | after 1st: {a['after1']} nonceLeft={a['nonceLeft']} | retry {a['retry']['status']} -> {a['after2']}"
        print(f'{k[0]:11} {k[1]} {k[2]:20} BASE {base}\n{"":36}HEAD {head}{post}')
