# QA-AUDIT-EMAIL-2 analysis (new code): model self-check, my oracle of the NEW grammar (written from build brief
# items 1-3 and the coordinator's rulings 1-2 on top of the first lane's grammar text), my differential with my own
# attribution, the headline-promise search (b0), and survivors with a three-part leak check.
# Usage: python3 -I -B qa2_diff.py <corpus prefix> <base.out> <head.out> <label> [--surv]
import sys, json
from collections import Counter, defaultdict
PFX, OLD, NEW, LABEL = sys.argv[1:5]; SURV = '--surv' in sys.argv
FMT = {0xAD, 0x180E, 0xFEFF} | set(range(0x200B, 0x2010)) | set(range(0x202A, 0x202F)) | set(range(0x2060, 0x2065))
def strip(s): return ''.join(c for c in s if ord(c) not in FMT)
def merge(sp):
    out = []
    for s, e in sorted((s, e) for s, e in sp if s < e):
        if out and s <= out[-1][1]: out[-1] = (out[-1][0], max(out[-1][1], e))
        else: out.append((s, e))
    return out
def is_cb(b, i): return i >= len(b) or (b[i] & 0xC0) != 0x80
def widen(b, sp):
    out = []
    for s, e in sp:
        s, e = min(s, len(b)), min(e, len(b))
        while not is_cb(b, s): s -= 1
        while not is_cb(b, e): e += 1
        if s < e: out.append((s, e))
    return merge(out)
def mask(t, sp):
    b = t.encode(); out = bytearray(); pos = 0
    for s, e in widen(b, sp):
        out += b[pos:s] + b'[REDACTED]'; pos = e
    return (out + b[pos:]).decode()
def trunc(t):
    o = []; lines = 1
    for n, c in enumerate(t):
        if n == 240: break
        if c == '\n':
            if lines == 3: break
            lines += 1
        o.append(c)
    return ''.join(o)
# ---------------- my oracle ----------------
LOCAL = set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-')
DOM = set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-')
LET = set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
RWS = set(b' \t\n\x0c\r')       # Rust is_ascii_whitespace (the brief names it for "its end"; U+000B is not in it)
def stop(c): return c in RWS or c in b'"\'<>`' or c >= 0x80
def dom_ok(d, xn_ci):
    labels = d.split(b'.')
    if len(labels) < 2 or any(not l for l in labels): return False
    last = labels[-1]
    xn = last[:4] == b'xn--' or (xn_ci and last[:4].lower() == b'xn--')
    return (len(last) >= 2 and all(c in LET for c in last)) or (len(last) >= 4 and xn)
def trim(d): return d.rstrip(b'.-')
def tokens(b):
    n = len(b); out = []; i = 0
    while i < n:
        p = b.find(b'://', i)
        if p < 0: break
        st = p + 3; en = st
        while en < n and not stop(b[en]): en += 1
        ui = next((k for k in range(st, en) if b[k] in b'/?#'), en)
        out.append((st, ui, en)); i = max(en, st)
    return out
def oracle(t, xn_ci=False, git_ci=False, info='/?#', want_reasons=False):
    b = t.encode() if isinstance(t, str) else t; n = len(b); toks = tokens(b); sp = []; why = []
    if info != '/?#':
        toks = [(st, next((k for k in range(st, en) if b[k] in info.encode()), en), en) for st, ui, en in toks]
    for at in range(n):
        if b[at] != 0x40: continue
        if any(st <= at < ui for st, ui, en in toks): continue
        s = at
        while s > 0 and b[s - 1] in LOCAL: s -= 1
        while s < at and b[s] == 0x2E: s += 1
        if s == at: continue
        e = at + 1
        while e < n and b[e] in DOM: e += 1
        run = b[at + 1:e]
        d = trim(run)
        if not dom_ok(d, xn_ci):
            d = next((trim(run[:k]) for k in range(len(run), 0, -1) if dom_ok(trim(run[:k]), xn_ci)), None)
            if d is None: continue
        E = at + 1 + len(d)
        if E < n and b[E] == 0x3A:
            q = E + 1; te = q
            while te < n and not stop(b[te]): te += 1
            after = b[q:te]
            if after[:1] in (b'/', b'~') or b'/' in after or after.endswith(b'.git') or (git_ci and after.lower().endswith(b'.git')):
                continue
        sp.append((s, E))
    return sp
# the OLD grammar's three exclusions, each tested on its own, for the class of a new span (rule written before the run)
def classes(b, s, E):
    at = b.index(b'@', s); K = set()
    if any(st <= at < en for st, ui, en in tokens(b)): K.add('1-link')
    e = at + 1
    while e < len(b) and b[e] in DOM: e += 1
    while e > at + 1 and b[e - 1] in b'.-': e -= 1
    if E != e: K.add('3-glued')          # the span is a strict prefix of the trimmed run: the old whole-run test failed
    elif E + 1 < len(b) and b[E] == 0x3A and b[E + 1] not in RWS: K.add('2-colon')
    return K
# ---------------- read ----------------
def spans(s): return [] if s in ('', '-') else [tuple(map(int, x.split('-'))) for x in s.split(',')]
H = lambda s: bytes.fromhex(s).decode()
def rec(line):
    f = line.rstrip('\n').split('\t')
    clean = H(f[4]); cleanw = clean if f[5] == '=' else H(f[5]); sm = f[8]
    return dict(find=spans(f[0]), findw=spans(f[1]), em=spans(f[2]), emw=spans(f[3]), clean=clean, cleanw=cleanw,
                redact=H(f[6]), preview=H(f[7]), summ=sm if sm.startswith('E:') or sm == 'N' else H(sm), full=f[9] if f[9] in ('-', 'N') else H(f[9]))
raws = [bytes.fromhex(l.strip()).decode() for l in open(PFX + '.hex')]
meta = [json.loads(l) for l in open(PFX + '.meta.jsonl')]
for m in meta:
    m.setdefault('tpl', m.get('template')); m.setdefault('sec', m.get('section'))
old = [rec(l) for l in open(OLD)]; new = [rec(l) for l in open(NEW)]
assert len(raws) == len(meta) == len(old) == len(new), (len(raws), len(meta), len(old), len(new))
def summ_of(raw, red): return 'E:FieldLimit("summary")' if len(raw.encode()) > 4 * 4096 or len(red.encode()) > 4096 else red
# ---------------- self-check of my model ----------------
bad = Counter()
for raw, o, nw in zip(raws, old, new):
    for x in (o, nw):
        if strip(raw) != x['clean']: bad['strip'] += 1
        if mask(x['clean'], x['find']) != x['redact']: bad['redact'] += 1
        if trunc(mask(x['cleanw'], x['findw'])) != x['preview']: bad['preview'] += 1
        if x['summ'] != summ_of(raw, x['redact']): bad['summary'] += 1
        if x['full'] not in ('-',) and x['full'] != x['preview']: bad['full'] += 1
print(f'[{LABEL}] inputs {len(raws)}; model self-check mismatches: {dict(bad) or 0}')
# ---------------- (b0) the headline promise ----------------
b0 = 0; b0first = None
for idx, (raw, o, nw) in enumerate(zip(raws, old, new)):
    for kc, kt in (('find', 'clean'), ('findw', 'cleanw')):
        bb = o[kt].encode()
        ob, nb = widen(bb, o[kc]), widen(bb, nw[kc]); j = 0; lost = None
        for s, e in ob:   # every byte covered at the base must be covered at the head
            while j < len(nb) and nb[j][1] <= s: j += 1
            if not (j < len(nb) and nb[j][0] <= s and nb[j][1] >= e): lost = (s, e); break
        if lost:
            b0 += 1; b0first = b0first or (idx, meta[idx]['tpl'], kc, lost, raw[:160], o['preview'][:160], nw['preview'][:160]); break
    else:
        # output level: a base-masked stretch of 4+ bytes that the head preview or summary shows and the base did not
        bb = o['cleanw'].encode()
        for s, e in widen(bb, o['findw']):
            seg = bb[s:e].decode('utf-8', 'ignore')
            if len(seg) >= 4 and seg in nw['preview'] and seg not in o['preview'] and seg not in nw['cleanw'].replace(seg, '', 1):
                b0 += 1; b0first = b0first or (idx, meta[idx]['tpl'], 'preview shows a base mask', seg[:60], raw[:160]); break
print(f'[{LABEL}] (b0) inputs where a byte the base masked is not masked at the head: {b0}; first: {b0first}')
# ---------------- (e) differential + attribution ----------------
cnt = Counter(); first = {}; byK = Counter(); multi = 0
orc_mis = Counter(); orc_first = {}
import os
CACHE = PFX + '.oracle.json'
if os.path.exists(CACHE):
    ORC = json.load(open(CACHE))
else:
    ORC = []
    for raw in raws:
        c = strip(raw); bb = raw.encode(); e = min(len(bb), 65536)
        while e < len(bb) and (bb[e] & 0xC0) == 0x80: e -= 1
        w = strip(bb[:e].decode())
        ORC.append([sorted(oracle(c)), sorted(oracle(c, xn_ci=True)), sorted(oracle(w)), sorted(oracle(w, xn_ci=True))])
    json.dump(ORC, open(CACHE, 'w'))
ORC = [[sorted(tuple(x) for x in l) for l in r] for r in ORC]
def orc_of(idx, kt, ci): return ORC[idx][(0 if kt == 'clean' else 2) + (1 if ci else 0)]
for idx, (raw, m, o, nw) in enumerate(zip(raws, meta, old, new)):
    cnt['inputs'] += 1
    # (vi) every input: emails spans against my oracle (code readings switched on one by one to name each decision)
    for kt, ke in (('clean', 'em'), ('cleanw', 'emw')):
        got = sorted(nw[ke]); lit = orc_of(idx, kt, False)
        if got != lit:
            if got == orc_of(idx, kt, True): key = 'D1 xn-- compared case-insensitively'
            else: key = 'OTHER'
            orc_mis[key] += 1; orc_first.setdefault(key, (idx, m['tpl'], nw[kt][:140], got, lit, orc_of(idx, kt, True)))
            break
    same = (merge(o['find']) == merge(nw['find']) and merge(o['findw']) == merge(nw['findw']) and o['redact'] == nw['redact']
            and o['preview'] == nw['preview'] and o['summ'] == nw['summ'])
    if same: cnt['identical'] += 1; continue
    why = []
    for kc, ke, kt in (('find', 'em', 'clean'), ('findw', 'emw', 'cleanw')):
        bt = nw[kt].encode(); O, N, oe, ne = merge(o[kc]), merge(nw[kc]), set(o[ke]), set(nw[ke])
        if not all(any(a <= s and e <= b for a, b in N) for s, e in O): why.append(f'(i) {kc}')
        if N != merge(o[kc] + nw[ke]): why.append(f'(ii) {kc}')
        if not oe <= ne: why.append(f'(iii) {ke}')
        if sorted(nw[ke]) != orc_of(idx, kt, True): why.append(f'(vi) {ke} vs oracle(code xn-- reading)')
        for sp in ne - oe:
            K = classes(bt, *sp)
            if not K: why.append(f'(iv) {ke} span {sp} in no class')
            elif kc == 'find': byK['+'.join(sorted(K))] += 1
    u = merge(o['find'] + nw['em']); uw = merge(o['findw'] + nw['emw'])
    red = mask(nw['clean'], u)
    if nw['redact'] != red or nw['preview'] != trunc(mask(nw['cleanw'], uw)) or nw['summ'] != summ_of(raw, red): why.append('(v) outputs')
    if why:
        cnt['unattributed'] += 1; first.setdefault('u', (idx, m['sec'], m['tpl'], raw[:200], o['preview'][:140], nw['preview'][:140], why[:4]))
    else:
        cnt['attributed'] += 1
        ks = set()
        for sp in set(nw['em']) - set(o['em']): ks |= classes(nw['clean'].encode(), *sp)
        for sp in set(nw['emw']) - set(o['emw']): ks |= classes(nw['cleanw'].encode(), *sp)
        if not ks: ks = {'(summary or truncation only)'}
        cnt['attributed, inputs with ' + '+'.join(sorted(ks))] += 1
        if len(ks) > 1: multi += 1
print(f'[{LABEL}] (e) differential: {dict(sorted(cnt.items()))}; inputs where more than one class applies: {multi}')
print(f'[{LABEL}] (e) new spans by class set (clean text): {dict(byK)}')
if 'u' in first: print(f'[{LABEL}] FIRST UNATTRIBUTED:', first['u'])
print(f'[{LABEL}] (vi) every input, emails vs my literal oracle: {dict(orc_mis) or 0}')
for k, v in orc_first.items(): print(f'   first {k}:', v)
# ---------------- survivors ----------------
def leak(pv, a, outside):
    pb, ab, ob = pv.encode(), a.encode(), outside.encode(); at = ab.index(b'@')
    def shows(w): return w in pb and w not in ob
    if ab in pb: return 'whole'
    if len(ab) < 8: return None
    if at >= 1 and at + 2 <= len(ab) and shows(ab[at - 1:at + 2]): return 'around-@'
    if any(shows(ab[i:i + 8]) for i in range(len(ab) - 7)): return 'window'
    return None
if SURV:
    rows = defaultdict(Counter); ex = {}; ctl = Counter()
    for raw, m, o, nw in zip(raws, meta, old, new):
        outside = strip(raw)
        for a in m['planted']: outside = outside.replace(a, '')
        for a in [x for x in m['planted'] if '@' in x]:
            ctl['planted'] += 1
            if leak(trunc(strip(raw)[:65536]), a, outside): ctl['identity flags'] += 1
            else: ctl['not visible without redaction'] += 1
            c = rows[(m['sec'], m['tpl'])]; c['n'] += 1
            for tag, x in (('base', o), ('head', nw)):
                oa = outside + '\x00' + '\x00'.join(y for y in m['planted'] if y != a)
                k = leak(x['preview'], a, oa)
                if k: c[f'{tag} prev'] += 1; c[f'{tag} prev {k}'] += 1
                if x['summ'].startswith('E:'): c[f'{tag} sum refused'] += 1
                elif leak(x['summ'], a, oa): c[f'{tag} sum'] += 1
                if tag == 'head' and k and (m['sec'], m['tpl']) not in ex: ex[(m['sec'], m['tpl'])] = (raw[:120], x['preview'][:120])
    tot = Counter()
    for c in rows.values(): tot.update(c)
    print(f'[{LABEL}] survivors totals: planted {tot["n"]}, base preview {tot["base prev"]}, head preview {tot["head prev"]}, head summary {tot["head sum"]} (refused at head {tot["head sum refused"]}); leak-check control: identity previews flag {ctl["identity flags"]} of {ctl["planted"]} planted (the rest, {ctl["not visible without redaction"]}, lie past the 240-character cut of an unmasked preview; they are counted, since a mask before them can bring them into view)')
    for k in sorted(rows):
        c = rows[k]
        if c['head prev'] or c['head sum']:
            print(f"  {k[0]} {k[1]:22} n={c['n']:4} base={c['base prev']:4} head={c['head prev']:4} headsum={c['head sum']:4} {dict((kk, v) for kk, v in c.items() if kk.startswith('head prev '))}")
            if k in ex: print('      e.g.', repr(ex[k][0]), '->', repr(ex[k][1]))
