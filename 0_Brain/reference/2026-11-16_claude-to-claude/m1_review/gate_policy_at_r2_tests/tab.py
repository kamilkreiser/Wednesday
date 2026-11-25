# QA-POLICY-AT-R2: join the probe outputs. usage: python3 -B tab.py <pout dir> [id prefix ...]
import json, sys, os
D = sys.argv[1]; pre = sys.argv[2:] or ['']
def load(n):
    L = [json.loads(l) for l in open(os.path.join(D, n))]
    meta = L[0]; return meta, {(r['id'], r['state']): r for r in L[1:]}
M = {k: load(f'{k}.jsonl') for k in ['phead_a', 'phead_b', 'pbase_a', 'pbase_b']}
keys = list(M['phead_a'][1].keys())
for k in keys:
    if not any(k[0].startswith(p) for p in pre): continue
    r = {n: M[n][1][k] for n in M}
    c = {n: r[n]['cols'] for n in r}
    place = 'PLACE-DEP' if (c['phead_a'] != c['phead_b'] or c['pbase_a'] != c['pbase_b']) else ''
    bh = 'base=head' if (c['phead_a'] == c['pbase_a'] and c['phead_b'] == c['pbase_b']) else 'base!=head'
    eq = all(r[n]['nov_eq_decide'] for n in r)
    pc = r['phead_a'].get('pieces_bash'); pcb = r['pbase_a'].get('pieces_bash')
    extra = f" pieces b/h {pcb}/{pc}" if pc is not None else ''
    if r['phead_a'].get('env_piece_pos') is not None or k[0].startswith('t4g'):
        extra += f" json-pieces {r['phead_a']['pieces_json']} .env-at {r['phead_a']['env_piece_pos']}"
    print(f"{k[0][:70]:70} | {k[1]:8} | head {c['phead_a']:16} vol {c['phead_b']:16} | base {c['pbase_a']:16} vol {c['pbase_b']:16} | {bh} {place} {'' if eq else 'NOV!=DECIDE'}{extra}")
for n, (m, _) in M.items(): print('#', n, 'fixture root', m['fixture_root'])
