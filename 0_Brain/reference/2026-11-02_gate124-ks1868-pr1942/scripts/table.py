# gate 124 judge: usage table.py <logs dir> [planted]
import json, sys
L = sys.argv[1]; planted = len(sys.argv) > 2
def load(n):
    d = {}
    for l in open(f'{L}/probe_{n}.jsonl'):
        r = json.loads(l); d[(r['site'], r['v'])] = r
    return d
B, H = load('base'), load('head')
if planted:  # plant: make one head unreadable cell differ in state
    k = next(k for k in H if k[1] == 'rp'); H[k]['state'] = dict(H[k]['state'], charges=['PLANTED'])
UNREAD = ['rp', 'tg', 'grp', 'gtj']; READ = ['ord', 'str', 'obj']
def route_lines(r):
    return [x for x in r['logs'] if x['level'] in ('warn', 'error') and not x['message'].startswith('Failed to issue certification')]
def outer(r):
    return [x for x in r['logs'] if x['message'].startswith('Failed to issue certification') or x['message'].startswith('Failed to issue verification')]
ok = diff = pre = 0; rows = []
sites = sorted({k[0] for k in H})
for s in sites:
    for v in sorted({k[1] for k in H if k[0] == s}):
        b, h = B[(s, v)], H[(s, v)]
        probs = []
        if not h['fired'] and v != 'none': probs.append('NOT FIRED')
        if h['escaped'] or h['unhandled']: probs.append('escaped/unhandled at head')
        if v in UNREAD:
            o = H[(s, 'ord')]
            for fld in ('status', 'body', 'state', 'sql', 'anchorCalls', 'deletes'):
                if h[fld] != o[fld]: probs.append(f'{fld} != ordinary')
            if [x['message'] for x in route_lines(h)] != [x['message'] for x in route_lines(o)]: probs.append('log lines != ordinary')
            exp = '[object Object]' if v == 'gtj' else 'unreadable thrown value'  # gtj: the message IS readable by String(); it is coerced, not unreadable
            for x in route_lines(h):
                if x['message'] in [y['message'] for y in route_lines(o) if y['error'] == 'g124 ordinary SECRETVAL'] and x['error'] != exp: probs.append('site reason not ' + exp + ': ' + x['error'][:40])
            if probs and 'through the real chargeEvents catch' in s and all(b[f] == h[f] for f in ('status','body','state','sql')):
                probs = ['PRE-EXISTING base == head (the real chargeEvents catch converts the value first)']
            if outer(h): probs.append('outer catch reached at head')
        elif v in READ or v == 'none':
            for fld in ('status', 'body', 'state', 'sql', 'anchorCalls', 'deletes'):
                if b[fld] != h[fld]: probs.append(f'{fld} base != head')
        if probs and probs[0].startswith('PRE-EXISTING'): pre += 1
        elif probs: diff += 1
        else: ok += 1
        def summ(r):
            st = r['state']; return f"{r['status']} rows={len(st['certRows'])} ev={len(st['events'])} ch={len(st['charges'])} der={st['derivedDocs']} leg={st['legacyStatus'][:4]}"
        logd = ''
        if [x['error'] for x in route_lines(b)] != [x['error'] for x in route_lines(h)]:
            logd = f" LOG {[x['error'][:30] for x in route_lines(b)]} -> {[x['error'][:30] for x in route_lines(h)]}"
        rows.append(f"{s} | {v} | base {summ(b)} | head {summ(h)} | {'OK' if not probs else 'DIFF ' + ';'.join(probs)}{logd}")
print('\n'.join(rows)); print(f'JUDGE OK={ok} DIFF={diff} PRE-EXISTING={pre}')
