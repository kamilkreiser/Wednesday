# QA-AUDIT-EMAIL-3: why each head survivor is shown, by MY reading of the NEW grammar (my oracle's reasons).
# Usage: python3 -I -B qa3_why.py <corpus prefix> <head.out> <label>
import sys, json
from collections import Counter, defaultdict
sys.path.insert(0, '/private/tmp/claude-501/qae3/h')
from qa3_lib import *
PFX, NEW, LABEL = sys.argv[1:4]
raws = [bytes.fromhex(l.strip()).decode() for l in open(PFX + '.hex')]
meta = [json.loads(l) for l in open(PFX + '.meta.jsonl')]
outs = [rec(l) for l in open(NEW)]
tot = Counter(); per = defaultdict(Counter); ex = {}; kinds = Counter()
for raw, m, o in zip(raws, meta, outs):
    pl = [x for x in m.get('planted', []) if '@' in x]
    if not pl: continue
    outside = strip(raw)
    for a in pl: outside = outside.replace(a, '')
    b = o['cleanw'].encode(); reasons = []; oracle_new(b, xn_ci=True, w5b='code', reasons=reasons)
    kept = {(s, E): (b1, b2, b3, b4) for s, E, b1, b2, b3, b4 in reasons}
    parts = link_parts_new(b, 'code')
    for a in pl:
        oa = outside + '\x00' + '\x00'.join(y for y in pl if y != a)
        k = leak(o['preview'], a, oa)
        if not k: continue
        ab = a.encode(); p = b.find(ab)
        if p < 0: r = 'W window end / not in the window'
        else:
            at = p + ab.index(b'@')
            tok = next(((st, ui) for st, ui in parts if st <= at < ui), None)
            if tok:
                st, ui = tok
                s = at
                while s > 0 and b[s - 1] in LOCAL: s -= 1
                if b'@' in b[st:at] and b.rfind(b'@', st, at) >= 0 and b[st:at].count(b'@'):
                    r = 'L an earlier @ in the same user-info part'
                elif s <= st:
                    r = 'L the user-info part reads as the address (joined by local-part bytes or nothing)'
                else:
                    j = b[s - 1]
                    r = 'L joined by %r (not an end byte)' % chr(j)
                    if b':' in b[st:s]: r += ' after a `:` (port: the URL rule masks to the @)'
            else:
                a2 = addr_at(b, at, True)
                if a2 and a2 in kept:
                    f = kept[a2]; names = [n for n, x in zip(('b1', 'b2', 'b3', 'b4'), f) if x]
                    r = 'C kept by ' + '+'.join(names)
                elif a2 is None: r = 'N not an address by the grammar'
                else:
                    cov = any(s_ <= p and p + len(ab) <= e_ for s_, e_ in o['emw'])
                    r = 'M masked; a copy elsewhere is shown' if cov else 'X OTHER'
        r = r + ('  [domain only]' if k == 'domain' else '')
        tot[r] += 1; per[r][m.get('tpl')] += 1; ex.setdefault(r, (m.get('tpl'), raw[:120], o['preview'][:120]))
print(f'[{LABEL}] head survivors by my reading of the new grammar: total {sum(tot.values())}')
for r in sorted(tot):
    print(f'{tot[r]:7}  {r}'); print('         templates:', dict(per[r].most_common(6))); print('         e.g.', repr(ex[r][1]), '->', repr(ex[r][2]))
