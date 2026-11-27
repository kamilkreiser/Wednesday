# QA-AUDIT-EMAIL-3 analysis (new code): model self-check, (b0) promise search, differential with MY attribution and
# MY oracle on every input, hosts now hidden, survivors with the three-part leak check.
# Usage: python3 -I -B qa3_diff.py <corpus prefix> <base.out> <head.out> <label> [--surv] [--hosts]
import sys, json, os, re
from collections import Counter, defaultdict
sys.path.insert(0, '/private/tmp/claude-501/qae3/h')
from qa3_lib import *
PFX, OLD, NEW, LABEL = sys.argv[1:5]; SURV = '--surv' in sys.argv; HOSTS = '--hosts' in sys.argv
raws = [bytes.fromhex(l.strip()).decode() for l in open(PFX + '.hex')]
meta = [json.loads(l) for l in open(PFX + '.meta.jsonl')]
for m in meta:
    m.setdefault('tpl', m.get('template')); m.setdefault('sec', m.get('section')); m.setdefault('planted', [])
old = [rec(l) for l in open(OLD)]; new = [rec(l) for l in open(NEW)]
assert len(raws) == len(meta) == len(old) == len(new), (len(raws), len(meta), len(old), len(new))
P = lambda *a: print(f'[{LABEL}]', *a)
# ---- model self-check
bad = Counter()
for raw, o, nw in zip(raws, old, new):
    for x in (o, nw):
        if strip(raw) != x['clean']: bad['strip'] += 1
        if mask(x['clean'], x['find']) != x['redact']: bad['redact'] += 1
        if trunc(mask(x['cleanw'], x['findw'])) != x['preview']: bad['preview'] += 1
        if x['summ'] != summ_of(raw, x['redact']): bad['summary'] += 1
P(f'inputs {len(raws)}; model self-check mismatches (both sides): {dict(bad) or 0}')
# ---- oracles (cached per corpus): new grammar code-xn reading lit-W5b; + code-W5b; + literal xn; old grammar
CACHE = PFX + '.qa3orc.json'
if os.path.exists(CACHE):
    ORC = json.load(open(CACHE))
else:
    ORC = []
    XN = re.compile(rb'[xX][nN]--')
    for raw in raws:
        row = []
        for t in (strip(raw), window(raw)):
            bt = t.encode()
            a = oracle_new(bt, xn_ci=True, w5b='lit'); c = oracle_new(bt, xn_ci=True, w5b='code')
            l = oracle_new(bt, xn_ci=False, w5b='lit') if XN.search(bt) else a
            o = oracle_old(bt, xn_ci=True)
            row.append([a, c, l, o])
        ORC.append(row)
    json.dump(ORC, open(CACHE, 'w'))
ORC = [[[sorted(tuple(x) for x in l) for l in kt] for kt in r] for r in ORC]
# ---- base `emails` against the OLD grammar (a check of my model of the base)
ob = sum(1 for i, o in enumerate(old) if sorted(o['em']) != ORC[i][0][3] or sorted(o['emw']) != ORC[i][1][3])
P(f'base emails vs my model of the OLD grammar: {ob} inputs differ')
# ---- (b0) the headline promise: one input where a byte covered at the base is not covered at the head
b0 = 0; b0first = None
for idx, (raw, o, nw) in enumerate(zip(raws, old, new)):
    hit = None
    for kc, kt in (('find', 'clean'), ('findw', 'cleanw')):
        bb = o[kt].encode(); obs, nbs = widen(bb, o[kc]), widen(bb, nw[kc]); j = 0
        for s, e in obs:
            while j < len(nbs) and nbs[j][1] <= s: j += 1
            if not (j < len(nbs) and nbs[j][0] <= s and nbs[j][1] >= e): hit = (kc, (s, e)); break
        if hit: break
    if not hit:
        bb = o['cleanw'].encode()
        for s, e in widen(bb, o['findw']):
            seg = bb[s:e].decode('utf-8', 'ignore')
            for tag, txt, otxt in (('preview', nw['preview'], o['preview']), ('summary', nw['summ'], o['summ'])):
                if txt.startswith('E:'): continue
                if len(seg) >= 4 and seg in txt and seg not in otxt and seg not in nw['cleanw'].replace(seg, '', 1):
                    hit = (tag + ' shows a base mask', seg[:60]); break
            if hit: break
    if hit:
        b0 += 1; b0first = b0first or (idx, meta[idx]['tpl'], hit, raw[:160], o['preview'][:160], nw['preview'][:160])
P(f'(b0) inputs where a byte the base masked is not masked at the head: {b0} of {len(raws)}; first: {b0first}')
# ---- (e) differential + attribution, (vi) on every input
cnt = Counter(); first = {}; byK = Counter(); multi = 0; orc = Counter(); orc_first = {}; hosts = Counter(); host_rows = []
d1 = 0
for idx, (raw, m, o, nw) in enumerate(zip(raws, meta, old, new)):
    cnt['inputs'] += 1
    key = None
    for kt, ke, j in (('clean', 'em', 0), ('cleanw', 'emw', 1)):
        got = sorted(nw[ke]); a, c, l, _ = ORC[idx][j]
        if got != a:
            key = 'D-W5b (a `://` in an unopened token never opens one)' if got == c else 'OTHER'
            orc_first.setdefault(key, (idx, m['tpl'], nw[kt][:160], got[:6], a[:6]))
        if l != a: d1 += 1
        if key: break
    if key: orc[key] += 1
    same = (merge(o['find']) == merge(nw['find']) and merge(o['findw']) == merge(nw['findw']) and o['redact'] == nw['redact']
            and o['preview'] == nw['preview'] and o['summ'] == nw['summ'])
    if same: cnt['identical'] += 1; continue
    why = []; ks = set(); multi_here = False
    for kc, ke, kt, j in (('find', 'em', 'clean', 0), ('findw', 'emw', 'cleanw', 1)):
        bt = nw[kt].encode(); O, N, oe, ne = merge(o[kc]), merge(nw[kc]), set(o[ke]), set(nw[ke])
        jj = 0; okc = True
        for s_, e_ in O:
            while jj < len(N) and N[jj][1] <= s_: jj += 1
            if not (jj < len(N) and N[jj][0] <= s_ and e_ <= N[jj][1]): okc = False; break
        if not okc: why.append(f'(i) {kc}')
        if ne - oe:
            OP = link_parts_old(bt); OPT = (OP, [p[0] for p in OP]); NST = nexts(bt, stop)
        if N != merge(o[kc] + nw[ke]): why.append(f'(ii) {kc}')
        if not oe <= ne: why.append(f'(iii) {ke}')
        if sorted(nw[ke]) != ORC[idx][j][0]: why.append(f'(vi) {ke}')
        for sp in sorted(ne - oe):
            K = classes(bt, *sp, parts=OPT, nstop=NST)
            if not K: why.append(f'(iv) {ke} span {sp} in no class')
            else:
                if kc == 'find': byK['+'.join(sorted(K))] += 1
                ks |= K
                if len(K) > 1: multi_here = True
            if HOSTS and kc == 'find' and K == {'L'}:
                at = bt.index(b'@', sp[0])
                for st, ui, en in OP:
                    if st <= at < ui:
                        if ui < en and sp[1] == ui:            # the old part ended at / ? # right after this domain: the link's host
                            p3 = st - 3
                            opened = p3 > 0 and bt[p3 - 1] in SCHEME
                            nui = next((k for k in range(st, en) if bt[k] in INFO_END), en)
                            k2 = ('no scheme byte' if not opened else repr(chr(bt[nui])))
                            hosts[k2] += 1; host_rows.append((idx, m['tpl'], k2, raw[:120], o['preview'][:120], nw['preview'][:120]))
                        break
    u = merge(o['find'] + nw['em']); uw = merge(o['findw'] + nw['emw'])
    red = mask(nw['clean'], u)
    if nw['redact'] != red or nw['preview'] != trunc(mask(nw['cleanw'], uw)) or nw['summ'] != summ_of(raw, red): why.append('(v) outputs')
    if why:
        cnt['unattributed'] += 1; first.setdefault('u', (idx, m['sec'], m['tpl'], raw[:200], o['preview'][:140], nw['preview'][:140], why[:4]))
    else:
        cnt['attributed'] += 1
        cnt['attributed ' + ('+'.join(sorted(ks)) if ks else '(no new span: summary/truncation only)')] += 1
        if multi_here: multi += 1
P(f'(e) differential: {dict(sorted(cnt.items()))}; inputs with a span in more than one class: {multi}')
P(f'(e) new spans by class set (clean text): {dict(byK)}')
if 'u' in first: P('FIRST UNATTRIBUTED:', first['u'])
P(f'(vi) every input, head emails vs my oracle (code xn-- reading): {dict(orc) or 0}; inputs where the literal xn-- reading differs (D1): {d1}')
for k, v in orc_first.items(): P(f'   first {k}:', v)
if HOSTS:
    P(f'hosts now hidden (class L span = the host after an old user-info part ended by / ? #), by the byte that now ends the part: {dict(hosts)}')
    with open(PFX + '.' + LABEL + '.hosts.tsv', 'w') as f:
        for r in host_rows: f.write('\t'.join(map(str, r)) + '\n')
# ---- survivors
if SURV:
    rows = defaultdict(Counter); ex = {}; ctl = Counter()
    for raw, m, o, nw in zip(raws, meta, old, new):
        outside = strip(raw)
        for a in m['planted']: outside = outside.replace(a, '')
        for a in [x for x in m['planted'] if '@' in x]:
            oa = outside + '\x00' + '\x00'.join(y for y in m['planted'] if y != a)
            ctl['planted'] += 1
            if leak(trunc(strip(raw)[:65536]), a, oa): ctl['identity flags'] += 1
            c = rows[(m['sec'], m['tpl'])]; c['n'] += 1
            for tag, x in (('base', o), ('head', nw)):
                k = leak(x['preview'], a, oa)
                if k == 'domain': c[f'{tag} domain'] += 1
                elif k: c[f'{tag} prev'] += 1
                if x['summ'].startswith('E:'): c[f'{tag} sum refused'] += 1
                else:
                    ks = leak(x['summ'], a, oa)
                    if ks and ks != 'domain': c[f'{tag} sum'] += 1
                if tag == 'head' and k and (m['sec'], m['tpl']) not in ex: ex[(m['sec'], m['tpl'])] = (raw[:110], x['preview'][:110], k)
    tot = Counter()
    for c in rows.values(): tot.update(c)
    P(f'survivors: planted {tot["n"]}; address shown base {tot["base prev"]} -> head {tot["head prev"]}; domain only base {tot["base domain"]} -> head {tot["head domain"]}; head summary shows {tot["head sum"]} (refused base {tot["base sum refused"]}, head {tot["head sum refused"]}); leak control: identity previews flag {ctl["identity flags"]} of {ctl["planted"]}')
    for k in sorted(rows):
        c = rows[k]
        if c['head prev'] or c['head domain'] or c['base prev'] != c['head prev']:
            P(f"  {k[0]} {k[1]:26} n={c['n']:4} shown base={c['base prev']:4} head={c['head prev']:4} domain base={c['base domain']:3} head={c['head domain']:3} headsum={c['head sum']:4}" + (f"   e.g. {ex[k][0]!r} -> {ex[k][1]!r}" if k in ex else ''))
