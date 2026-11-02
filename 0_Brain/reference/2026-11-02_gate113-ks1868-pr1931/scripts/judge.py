# judge.py <base.jsonl> <head.jsonl> : mechanical checks, rc 1 on any fail
import json, sys
def load(p):
    d = {}; ob = None
    for l in open(p):
        r = json.loads(l)
        if r['id'] == '__outbound': ob = r['outbound']
        else: d[r['id']] = r
    return d, ob
B, obB = load(sys.argv[1]); H, obH = load(sys.argv[2])
fails = []; n = 0
def chk(c, msg):
    global n; n += 1
    if not c: fails.append(msg)
SHAPES = ['ordinary','revoked','getter','nullproto','string','undef','msgProxy','msgSymbol','msgToStr','msgNullProto']
def fam(i):
    for s in SHAPES:
        if i.endswith('_' + s): return i[:-len(s)-1], s
    return i, None
OUT = ('status','success','errCode','tokenInBody','codeInLocation','cookie','st','unhandled')
def outcome(r): return {k: r[k] for k in OUT}
def nostack(logs): return [{**l, 'vals': {k: v for k, v in l.get('vals', {}).items() if k != 'stack'}} for l in logs]
def logs_masked(r):
    return [(l['lvl'], l['msg'], tuple(l.get('keys', [])), l['threw']) for l in r['logs']]
CONST = 'unreadable thrown value'
chk(set(B) == set(H), 'scenario sets differ')
changed = []
for i in sorted(H):
    b, h = B[i], H[i]
    if outcome(b) != outcome(h) or nostack(b['logs']) != nostack(h['logs']) or b['bodyLeaks'] != h['bodyLeaks']:
        changed.append(i)
print('CHANGED base->head:', len(changed))
for i in changed:
    f, s = fam(i); b, h = B[i], H[i]; o = H.get(f + '_ordinary')
    stdiff = {k: (b['st'][k], h['st'][k]) for k in h['st'] if b['st'][k] != h['st'][k]}
    print(f"  {i}: base {b['status']} unh={b['unhandled']} -> head {h['status']} unh={h['unhandled']}; st diff {stdiff}")
    chk(o is not None, f'{i}: no ordinary control')
    if o:
        chk(outcome(h) == outcome(o), f'{i}: head outcome != head ordinary outcome')
        chk(logs_masked(h) == logs_masked(o), f'{i}: head log shape != ordinary log shape')
        el = [l for l in h['logs'] if l['lvl'] in ('warn','error') and 'error' in l.get('keys', [])]
        chk(len(el) == 1 and el[0]['vals']['error'] == CONST, f'{i}: head does not log exactly one constant')
    chk(b['status'] in ('NO_RESPONSE', 500) or b['unhandled'] > 0, f'{i}: base was not a failure')
    chk(not h['bodyLeaks'], f'{i}: head body leaks')
# fail-closed: every scenario where a CHECK failed or a pre-issue step threw issues nothing at head
SIDE = ('login_rehash', 'logout_denylist')   # post-check, non-fatal side steps by design
for i, h in H.items():
    f, s = fam(i)
    refused = any(k in i for k in ('badpw','mfa','suspended','locked','unknown','badsecret','denied','invalid','non2xx','forbidden'))
    failing = (s is not None and not f.startswith(SIDE)) or refused
    if failing:
        st = h['st']
        chk(st['sessions'] == 0 and st['tokenPairs'] == 0 and st['connectorTokens'] == 0 and st['authCodes'] == 0, f'{i}: issued state on a failure')
        chk(not h['tokenInBody'] and not h['codeInLocation'] and h['cookie'] != 'set', f'{i}: credential in response on a failure')
        chk(h['success'] is not True and h['status'] not in (200, 201, 302), f'{i}: success status on a failure')
# side-step sites: head unreadable == head ordinary on outcome (rehash: login after full gate)
for i, h in H.items():
    f, s = fam(i)
    if f in SIDE and s in ('revoked','getter'):
        chk(outcome(h) == outcome(H[f + '_ordinary']), f'{i}: side step head != ordinary')
# no new disclosure: head constant-path logs never carry the ordinary secret
for i, h in H.items():
    f, s = fam(i)
    if s in ('revoked','getter'):
        chk(all('hunter2' not in json.dumps(l) for l in h['logs']), f'{i}: secret in head log')
chk(obB == [] and obH == [], f'outbound calls {obB} {obH}')
for d in (B, H):
    for i, r in d.items():
        chk(all(c in ('127.0.0.1', 'localhost', '::1') for c in r['connects']), f'{i}: non-loopback connect {r["connects"]}')
print(f'checks {n} fails {len(fails)}')
for x in fails: print('FAIL', x)
sys.exit(1 if fails else 0)
