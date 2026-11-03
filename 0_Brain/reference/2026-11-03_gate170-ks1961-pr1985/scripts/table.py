import json, sys
# Gate 170: group probe.jsonl rows by (cell, val) and print dev / r1 / head side by side, plus the comparisons.
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
by = {}
for r in rows: by.setdefault((r['cell'], r['val']), {})[r['variant']] = r
def rle(s):
    out = []
    for x in (s or '').split(','):
        if out and out[-1][0] == x: out[-1][1] += 1
        else: out.append([x, 1])
    return ' '.join(f'{a}x{b}' for a, b in out)
more = []; same_bytes = []; diff_bytes = []
for (c, v), d in by.items():
    dv, r1, hd = d.get('dev'), d.get('r1'), d.get('head')
    if c.startswith('bf'):
        f = lambda r: f"{r['resp']['status']} {r['resp']['ms']}ms down={r['downstream']} unh={len(r['unhandled'])} plant={r['plantInLogs']} | {r['resp']['body'][:70]}"
        print(f"{c:13} {v:18} DEV  {f(dv)}\n{'':32} R1   {f(r1)}\n{'':32} HEAD {f(hd)}")
        if hd['downstream'] > dv['downstream']: more.append((c, v, dv['downstream'], hd['downstream']))
        continue
    f = lambda r: f"[{rle(r['statuses'])}] allowed={r['allowed']}/{r['N']} kind={r['perKind']} hdr={r['limitHdr']} hint={r['hint']} ctr={r['redisCounter']} plant={r['plantInLogs']} unh={len(r['unhandled'])} logs={len(r['logs'])}"
    print(f"{c:13} {v:18} DEV  {f(dv)}\n{'':32} R1   {f(r1)}\n{'':32} HEAD {f(hd)}")
    if hd['allowed'] > dv['allowed']: more.append((c, v, dv['allowed'], hd['allowed']))
    keys = ['statuses', 'allowed', 'limitHdr', 'hint', 'redisCounter', 'calls', 'bodies', 'logs', 'plantInLogs', 'unhandled']
    norm = lambda r: {k: r.get(k) for k in keys}
    (same_bytes if norm(dv) == norm(hd) else diff_bytes).append((c, v, [k for k in keys if norm(dv)[k] != norm(hd)[k]]))
print('\n=== HEAD MORE PERMISSIVE THAN DEV (downstream/allowed):', len(more))
for x in more: print('  ', x)
print('=== limiter cells identical dev==head on', 'statuses,allowed,limitHdr,hint,ctr,calls,bodies,logs,plant,unhandled:', len(same_bytes))
for x in same_bytes: print('   SAME', x[0], x[1])
print('=== limiter cells differing dev vs head:', len(diff_bytes))
for x in diff_bytes: print('   DIFF', x[0], x[1], x[2])
