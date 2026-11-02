import json, sys, collections
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945/logs/'
tag = sys.argv[1] if len(sys.argv) > 1 else ''
L = {f'{v}_{m}': json.load(open(W + f'pg_{tag}{v}_{m}.json')) for v in ('base', 'head') for m in ('st', 'mt')}
out = []
p = out.append
# (c) identical row sets on a healthy run
for m in ('st', 'mt'):
    b, h = L[f'base_{m}']['healthySnap'], L[f'head_{m}']['healthySnap']
    p(f'(c) healthy snapshot base==head mode={m}: {b == h}  per-table: ' + ', '.join(f'{k}={b[k] == h[k]}({len(h[k])} rows left)' for k in h))
p(f"(c) healthy snapshot st==mt at head: {L['head_st']['healthySnap'] == L['head_mt']['healthySnap']}")
for m in ('st', 'mt'):
    hb = [r for r in L[f'base_{m}']['results'] if r['name'] == 'healthy'][0]['per']
    hh = [r for r in L[f'head_{m}']['results'] if r['name'] == 'healthy'][0]['per']
    p(f'(c) healthy changed-row ids base==head mode={m}: ' + ', '.join(f"{k}:{hb[k]['changed'] == hh[k]['changed']}({len(hh[k]['changed'])})" for k in hh))
    p(f'    log rows + affected base vs head mode={m}: ' + ', '.join(f"{k}:{(hb[k]['logRows'], hb[k]['affected'])}/{(hh[k]['logRows'], hh[k]['affected'])}" for k in hh))
# (a) per-cell after-state of the failed policy
p('')
p('(a) failed-policy after-state (DATA/LOG/STAMP), base -> head, st | mt; others complete; returned contains failed policy')
names = [r['name'] for r in L['head_st']['results']]
for n in names:
    row = []
    for m in ('st', 'mt'):
        rb = [r for r in L[f'base_{m}']['results'] if r['name'] == n][0]
        rh = [r for r in L[f'head_{m}']['results'] if r['name'] == n][0]
        k = rh['kind']
        row.append(f"{rb['failedShape']}->{rh['failedShape']} oth {rb['othersComplete']}/{rh['othersComplete']} ret {k in rb['returned'] if k else '-'}/{k in rh['returned'] if k else '-'} rej '{rb['rejected']}'/'{rh['rejected']}'")
    p(f'  {n:55s} st: {row[0]} | mt: {row[1]}')
# trace: per policy unit, txids and pids and bypass
p('')
p('trace (healthy): per data type, the DELETE/UPDATE + INSERT log + STAMP statements -> distinct txids / pids; bypass GUC values; session user')
TBL = {'user_sessions': 'user_sessions', 'audit_logs': 'audit_logs', 'verification_requests': 'verification_requests', 'system_errors': 'system_errors', 'share_records': 'share_records'}
for key in ('base_st', 'head_st', 'base_mt', 'head_mt'):
    tr = [r for r in L[key]['results'] if r['name'] == 'healthy'][0]['trace']
    # the trace is ordered; segment it: target-table stmt, then data_deletion_log INSERT, then data_retention_policies UPDATE
    units, cur = [], []
    for t in tr:
        cur.append(t)
        if t['tbl'] == 'data_retention_policies':
            units.append(cur); cur = []
    desc = []
    for u in units:
        tx = len({t['txid'] for t in u}); pid = len({t['pid'] for t in u})
        desc.append(f"{u[0]['tbl']}:{len(u)}stmts/{tx}tx/{pid}pid")
    byp = collections.Counter(t['bypass'] for t in tr); who = collections.Counter(t['who'] for t in tr)
    p(f'  {key}: {len(tr)} traced statements; ' + '; '.join(desc) + f'; bypass={dict(byp)} who={dict(who)}')
# logs
p('')
p('error log lines (head, distinct, values elided to the shape):')
seen = set()
for key in ('head_st', 'head_mt', 'base_st', 'base_mt'):
    for r in L[key]['results']:
        for l in r['logLines']:
            s = l
            if (key[:4], s) not in seen:
                seen.add((key[:4], s)); p(f'  {key}: {s}')
open(W + f'judge_pg{tag}.log', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
