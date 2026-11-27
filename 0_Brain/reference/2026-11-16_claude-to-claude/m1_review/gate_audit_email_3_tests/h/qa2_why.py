# QA-AUDIT-EMAIL-2: why each head survivor of a corpus is shown (my reading of the head grammar), by class.
# Usage: python3 -I -B qa2_why.py <corpus prefix> <head.out>
import sys, json
from collections import Counter, defaultdict
ARGS = sys.argv[1:3]; sys.argv = ['x', 'x', 'x', 'x', 'x']
src = open('/private/tmp/claude-501/qae3/h/qa2_diff.py').read().split('# ---------------- read ----------------')[0]
exec(src)
def leak(pv, a, outside):
    pb, ab, ob = pv.encode(), a.encode(), outside.encode(); at = ab.index(b'@')
    def shows(w): return w in pb and w not in ob
    if ab in pb: return 'whole'
    if len(ab) < 8: return None
    if at >= 1 and at + 2 <= len(ab) and shows(ab[at - 1:at + 2]): return 'around-@'
    if any(shows(ab[i:i + 8]) for i in range(len(ab) - 7)): return 'window'
    return None
PFX, NEW = ARGS
raws = [bytes.fromhex(l.strip()).decode() for l in open(PFX + '.hex')]
meta = [json.loads(l) for l in open(PFX + '.meta.jsonl')]
for m in meta: m.setdefault('tpl', m.get('template')); m.setdefault('sec', m.get('section'))
outs = [l.rstrip('\n').split('\t') for l in open(NEW)]
def reason(b, at, toks):
    n = len(b)
    for st, ui, en in toks:
        if st <= at < ui:
            return 'U1 user-info: no / ? # between the :// and the @' if ui == en else 'U2 user-info: @ before the first / ? #'
    s = at
    while s > 0 and b[s - 1] in LOCAL: s -= 1
    while s < at and b[s] == 0x2E: s += 1
    if s == at: return 'N1 no local part (byte before @ not a local byte)'
    e = at + 1
    while e < n and b[e] in DOM: e += 1
    run = b[at + 1:e]; d = trim(run)
    if not dom_ok(d, True):
        d = next((trim(run[:k]) for k in range(len(run), 0, -1) if dom_ok(trim(run[:k]), True)), None)
        if d is None: return 'N2 no valid domain prefix'
    E = at + 1 + len(d)
    if E < n and b[E] == 0x3A:
        q = E + 1; te = q
        while te < n and not stop(b[te]): te += 1
        after = b[q:te]
        g = '(glued to a link) ' if d != trim(run) or (len(run) > 0 and b'http' in d.lower()[-8:]) else ''
        if after[:1] == b'/': return 'C1 colon then /' + (' [glued to a link: run passes]' if b'//' == after[:2] and any(d.lower().endswith(x) for x in (b'http', b'https', b'ftp', b'ssh')) else '')
        if after[:1] == b'~': return 'C2 colon then ~'
        if b'/' in after: return 'C3 colon then a token holding a later /'
        if after.endswith(b'.git'): return 'C4 colon then a token ending .git'
    return None
tot = Counter(); ex = {}; per = defaultdict(Counter)
for raw, m, f in zip(raws, meta, outs):
    pv = bytes.fromhex(f[7]).decode(); clean = bytes.fromhex(f[4]).decode(); cleanw = clean if f[5] == '=' else bytes.fromhex(f[5]).decode()
    outside = strip(raw)
    for a in m.get('planted', []): outside = outside.replace(a, '')
    b = cleanw.encode(); toks = tokens(b)
    for a in [x for x in m.get('planted', []) if '@' in x]:
        pb, ab = pv.encode(), a.encode()
        oa = (outside + '\x00' + '\x00'.join(y for y in m['planted'] if y != a)).encode()
        # visible?
        at_a = ab.index(b'@'); vis = ab in pb or (len(ab) >= 8 and ((at_a >= 1 and ab[at_a-1:at_a+2] in pb and ab[at_a-1:at_a+2] not in oa) or any(ab[i:i+8] in pb and ab[i:i+8] not in oa for i in range(len(ab) - 7))))
        if not vis: continue
        p = b.find(ab)
        if p < 0: r = 'W window end (the address is cut by the 64 KiB window)'
        else:
            r = reason(b, p + at_a, toks)
            if r is None:
                ems = [tuple(map(int, x.split('-'))) for x in f[3].split(',')] if f[3] not in ('', '-') else []
                cov = any(s <= p and p + len(ab) <= e for s, e in ems)
                r = 'M address masked; a copy of it elsewhere is shown' if cov else 'X OTHER'
        tot[r] += 1; per[r][m.get('tpl')] += 1; ex.setdefault(r, (m.get('tpl'), raw[:150], pv[:150]))
for r in sorted(tot):
    print(f'{tot[r]:6}  {r}'); print('        templates:', dict(per[r].most_common(8))); print('        e.g.', repr(ex[r][1]), '->', repr(ex[r][2]))
