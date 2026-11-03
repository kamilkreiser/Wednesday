import json, sys
# Pair base/head rows from probe.jsonl and print one line per cell.
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
by = {}
for r in rows: by.setdefault((r['cell'], r['val']), {})[r['variant']] = r
def fmt(r):
    if r is None: return 'MISSING'
    if r['cell'].startswith('bf'):
        x = r.get('resp', {})
        s = f"{x.get('status')} {x.get('ms')}ms down={r.get('downstream')} writes={r.get('writes')} plant={r['plantInLogs']} unh={len(r['unhandled'])}"
        return s + ' | ' + (x.get('body') or '')[:90]
    st = (r.get('statuses') or '').split(',')
    rle = []
    for x in st:
        if rle and rle[-1][0] == x: rle[-1][1] += 1
        else: rle.append([x, 1])
    return f"[{' '.join(f'{a}x{b}' for a, b in rle)}] allowed={r.get('allowed')}/{r.get('N')} limitHdr={r.get('limitHdr')} hintWin={r.get('hint')} ctr={r.get('redisCounter')} plant={r['plantInLogs']} unh={len(r['unhandled'])}"
for (c, v), d in by.items():
    print(f"{c:15} {v:20} BASE {fmt(d.get('base'))}")
    print(f"{'':15} {'':20} HEAD {fmt(d.get('head'))}")
