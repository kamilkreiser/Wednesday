# QA-AUDIT-EMAIL analysis: self-check of the Python model, survivors (b,c,d), differential + attribution (e).
# Usage: python3 -B qa_analyze.py <corpus prefix> <old.out> <new.out> [label]
import sys, json
from collections import defaultdict, Counter
PFX, OLD, NEW = sys.argv[1:4]; LABEL = sys.argv[4] if len(sys.argv) > 4 else 'head'
FMT = set([0xAD, 0x180E, 0xFEFF] + list(range(0x200B, 0x2010)) + list(range(0x202A, 0x202F)) + list(range(0x2060, 0x2065)))
def strip(s): return ''.join(c for c in s if ord(c) not in FMT)
def merge(sp):
    sp = sorted((s, e) for s, e in sp if s < e); out = []
    for s, e in sp:
        if out and s <= out[-1][1]: out[-1] = (out[-1][0], max(out[-1][1], e))
        else: out.append((s, e))
    return out
def cb(b, i): return i >= len(b) or (b[i] & 0xC0) != 0x80
def apply_mask(t, ranges):
    b = t.encode(); rs = []
    for s, e in ranges:
        s, e = min(s, len(b)), min(e, len(b))
        while not cb(b, s): s -= 1
        while not cb(b, e): e += 1
        if s < e: rs.append((s, e))
    rs.sort(); out = bytearray(); pos = 0; i = 0
    while i < len(rs):
        s, e = rs[i]; i += 1
        while i < len(rs) and rs[i][0] <= e: e = max(e, rs[i][1]); i += 1
        if s >= pos: out += b[pos:s]
        out += b'[REDACTED]'; pos = max(pos, e)
    out += b[pos:]; return out.decode()
def truncate(t):
    out = []; lines = 1
    for n, c in enumerate(t):
        if n == 240: break
        if c == '\n':
            if lines == 3: break
            lines += 1
        out.append(c)
    return ''.join(out)
# ---- the check's own oracle, from the lane brief's rule text (lines 42-51), literal readings ----
LOC = set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-')
DOM = set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-')
import os
VAR = os.environ.get('QAE_ORACLE', '')
WS_BYTE = set(b' \t\n\r\x0b\x0c')  # "a byte that is not whitespace": C isspace() bytes (includes U+000B)
def oracle(t, xn_ci=False, ws='byte'):
    b = t.encode(); n = len(b); toks = []; i = 0
    while True:
        p = b.find(b'://', i) if i < n else -1
        if p < 0: break
        s = p + 3; e = s
        while e < n and b[e] not in b' \t\n\r\x0c' and b[e] not in b'"\'<>`' and b[e] < 0x80: e += 1
        toks.append((s, e)); i = max(e, s)
    def in_tok(at): return any(s <= at < e for s, e in toks)
    r = []
    for at in range(n):
        if b[at] != 0x40 or in_tok(at): continue
        s = at
        while s > 0 and b[s - 1] in LOC: s -= 1
        while s < at and b[s] == 0x2E: s += 1
        if s == at: continue
        e = at + 1
        while e < n and b[e] in DOM: e += 1
        while e > at + 1 and b[e - 1] in b'.-': e -= 1
        def dok(d):
            labels = d.split(b'.')
            if len(labels) < 2 or any(len(l) == 0 for l in labels): return False
            last = labels[-1]
            okl = len(last) >= 2 and all(65 <= c <= 90 or 97 <= c <= 122 for c in last)
            okx = last[:4].lower() == b'xn--' if xn_ci else last[:4] == b'xn--'
            return okl or okx
        if not dok(b[at + 1:e]):
            if VAR == 'prefix':   # the variant of (c): longest prefix that, trimmed, passes (naive here; Rust copy is linear)
                t = next((t for t in range(e, at + 1, -1) if b[t - 1] not in b'.-' and dok(b[at + 1:t])), None)
            elif VAR == 'label':  # label-boundary-only: prefixes ending before a '.' (whole labels), trimmed
                t = next((t for t in range(e, at + 1, -1) if (t == e or b[t] == 0x2E) and b[t - 1] not in b'.-' and dok(b[at + 1:t])), None)
            else: t = None
            if t is None: continue
            e = t
        if e < n and b[e] == 0x3A and e + 1 < n:
            if ws == 'byte': nws = b[e + 1] not in WS_BYTE
            elif ws == 'rust': nws = b[e + 1] not in b' \t\n\r\x0c'
            else: nws = not b[e + 1:].decode('utf-8', 'ignore')[:1].isspace()
            if nws: continue
        r.append((s, e))
    return r
def leak(p, a):
    pb, ab = p.encode(), a.encode(); at = ab.index(b'@')
    if at >= 1 and at + 2 <= len(ab) and ab[at - 1:at + 2] in pb: return 'address'
    if len(ab) < 8 and ab in pb: return 'address'
    if ab[at:] in pb: return 'domain'
    ws = [ab] if len(ab) <= 8 else [ab[i:i + 8] for i in range(len(ab) - 7)]
    if any(w in pb for w in ws): return 'part'
    return None
def leak_ctx(p, a, outside):
    k = leak(p, a)
    if k != 'part': return k
    ab = a.encode(); ob = outside.encode(); pb = p.encode()
    ws = [ab] if len(ab) <= 8 else [ab[i:i + 8] for i in range(len(ab) - 7)]
    return 'part' if any(w in pb and w not in ob for w in ws) else None
def spans(s): return [] if s in ('', '-') else [tuple(map(int, x.split('-'))) for x in s.split(',')]
H = lambda s: bytes.fromhex(s).decode()
def rec(line):
    f = line.rstrip('\n').split('\t')
    clean = H(f[4]); cleanw = clean if f[5] == '=' else H(f[5])
    sm = f[8]; summ = H(sm) if not sm.startswith('E:') and sm != 'N' else sm
    return dict(find=spans(f[0]), findw=spans(f[1]), em=None if f[2] == '-' else spans(f[2]), emw=None if f[3] == '-' else spans(f[3]),
                clean=clean, cleanw=cleanw, redact=H(f[6]), preview=H(f[7]), summ=summ, full=f[9] if f[9] in ('-', 'N') else H(f[9]))
raws = [bytes.fromhex(l.strip()).decode() for l in open(PFX + '.hex')]
meta = [json.loads(l) for l in open(PFX + '.meta.jsonl')]
old = [rec(l) for l in open(OLD)]; new = [rec(l) for l in open(NEW)]
assert len(raws) == len(meta) == len(old) == len(new)
# ---- self-check of the Python model against the probe (control for every computed answer) ----
bad = Counter()
for raw, o, nw in zip(raws, old, new):
    for x in (o, nw):
        if strip(raw) != x['clean']: bad['strip'] += 1
        if apply_mask(x['clean'], x['find']) != x['redact']: bad['redact'] += 1
        if truncate(apply_mask(x['cleanw'], x['findw'])) != x['preview']: bad['preview'] += 1
        if x['full'] not in ('-',) and x['full'] != x['preview']: bad['chain full != preview'] += 1
        if not str(x['summ']).startswith('E:') and x['summ'] != x['redact']: bad['chain summary != redact'] += 1
print(f'[{LABEL}] model self-check mismatches: {dict(bad) or 0}')
# ---- survivors ----
def surv_rows(sections):
    rows = defaultdict(lambda: Counter())
    examples = {}
    for raw, m, o, nw in zip(raws, meta, old, new):
        if m['section'] not in sections: continue
        outside = strip(raw)
        for a in m['planted']: outside = outside.replace(a, '')
        for a in m['planted']:
            if '@' not in a: continue
            c = rows[(m['section'], m['template'])]; c['n'] += 1
            for tag, x in (('base', o), ('head', nw)):
                k = leak_ctx(x['preview'], a, outside)
                if k: c[f'{tag} preview {k}'] += 1
                if not str(x['summ']).startswith('E:'):
                    k2 = leak_ctx(x['summ'], a, outside)
                    if k2: c[f'{tag} summary {k2}'] += 1
                else: c[f'{tag} summary refused'] += 1
                if tag == 'head' and (k) and (m['section'], m['template']) not in examples:
                    examples[(m['section'], m['template'])] = (raw[:160], x['preview'][:160], a)
    return rows, examples
for secs, title in ((('b',), 'b placements'), (('c',), 'c glued-after'), (('d',), 'd literal forms')):
    rows, ex = surv_rows(secs)
    tot = Counter()
    for k, c in rows.items(): tot.update(c)
    print(f'\n[{LABEL}] === survivors: {title}: totals {dict(tot)}')
    for k in sorted(rows):
        c = rows[k]; hs = sum(v for kk, v in c.items() if kk.startswith('head preview'))
        hsum = sum(v for kk, v in c.items() if kk.startswith('head summary') and 'refused' not in kk)
        bs = sum(v for kk, v in c.items() if kk.startswith('base preview'))
        if secs == ('b',) and hs == 0 and hsum == 0: continue
        print(f"  {k[1]:34} n={c['n']:4} base-prev-surv={bs:4} head-prev-surv={hs:4} head-sum-surv={hsum:4} {dict((kk, v) for kk, v in c.items() if kk.startswith('head'))}")
        if k in ex: print('      e.g. raw', repr(ex[k][0][:110]), '-> preview', repr(ex[k][1][:110]))
    if secs == ('b',):
        print('  (templates with 0 head survivors in preview and summary omitted; count:', sum(1 for k, c in rows.items() if not any(kk.startswith('head preview') or (kk.startswith('head summary') and 'refused' not in kk) for kk in c)), 'of', len(rows), ')')
print(f'\n[{LABEL}] === table d: raw | base preview | head preview')
for raw, m, o, nw in zip(raws, meta, old, new):
    if m['section'] == 'd': print(f"  {m['template']:32} {raw!r:52} | {o['preview']!r} | {nw['preview']!r}")
# ---- differential + attribution ----
cnt = Counter(); first = {}
odiff = Counter(); oex = {}
for idx, (raw, m, o, nw) in enumerate(zip(raws, meta, old, new)):
    cnt['inputs'] += 1
    same = merge(o['find']) == merge(nw['find']) and o['redact'] == nw['redact'] and o['preview'] == nw['preview'] and merge(o['findw']) == merge(nw['findw']) and o['summ'] == nw['summ']
    orc, orcw = oracle(nw['clean']), oracle(nw['cleanw'])
    if nw['em'] is not None:
        if sorted(nw['em']) != sorted(orc) or sorted(nw['emw']) != sorted(orcw):
            for kind, kw in (('xn-- case-insensitive', dict(xn_ci=True)), ('unicode whitespace after :', dict(ws='unicode')), ('both', dict(xn_ci=True, ws='unicode'))):
                pass
            # classify the difference
            ci = oracle(nw['clean'], xn_ci=True)
            if sorted(nw['em']) == sorted(ci): key = 'code reads xn-- case-insensitively'
            else:
                key = 'other'
                if sorted(nw['em']) == sorted(oracle(nw['clean'], xn_ci=True, ws='ascii-rust')): key = 'other'
            odiff[key] += 1; oex.setdefault(key, (idx, raw[:120], nw['em'], orc))
    if same: cnt['identical'] += 1; continue
    em = nw['em'] if nw['em'] is not None else []; emw = nw['emw'] if nw['emw'] is not None else []
    u = merge(o['find'] + em); uw = merge(o['findw'] + emw)
    red_exp = apply_mask(nw['clean'], u)
    if len(raw.encode()) > 4 * 4096: summ_exp = 'E:FieldLimit("summary")'
    elif len(red_exp.encode()) > 4096: summ_exp = 'E:FieldLimit("summary")'
    else: summ_exp = red_exp
    lit = bool(merge(nw['find']) == u and merge(nw['findw']) == uw and nw['redact'] == red_exp
           and nw['preview'] == truncate(apply_mask(nw['cleanw'], uw)) and (em or emw) and nw['summ'] == summ_exp)
    orc_ok = sorted(em) == sorted(oracle(nw['clean'], xn_ci=True, ws='rust')) and sorted(emw) == sorted(oracle(nw['cleanw'], xn_ci=True, ws='rust'))
    if lit and orc_ok: cnt['attributed'] += 1
    else:
        cnt['unattributed'] += 1
        if lit: cnt['unattributed: rule true, oracle false'] += 1
        else: cnt['unattributed: rule false'] += 1
        first.setdefault('u', (idx, m['section'], m['template'], raw[:200], o['preview'][:120], nw['preview'][:120], em, oracle(nw['clean'], xn_ci=True, ws='rust')))
    for f in ('find', 'redact', 'preview', 'summ'):
        a, b = (merge(o[f]), merge(nw[f])) if f == 'find' else (o[f], nw[f])
        if a != b: cnt['differing ' + f] += 1
print(f'\n[{LABEL}] === differential: {dict(cnt)}')
if 'u' in first: print(f'[{LABEL}] FIRST UNATTRIBUTED:', first['u'])
print(f'[{LABEL}] oracle (literal: lower-case xn--, C-isspace byte after ":") vs emails differences: {dict(odiff)}')
for k, v in oex.items(): print('   e.g.', k, v)
# U+000B and unicode-whitespace readings, counted directly
vt = sum(1 for nw in new if nw['em'] is not None and sorted(nw['em']) != sorted(oracle(nw['clean'], xn_ci=True)))
uni = sum(1 for nw in new if nw['em'] is not None and sorted(nw['em']) != sorted(oracle(nw['clean'], xn_ci=True, ws='unicode')))
print(f'[{LABEL}] with xn-- read case-insensitively: inputs where code != oracle(C-isspace byte) = {vt}; != oracle(Unicode whitespace) = {uni}')

# every input (identical ones included): emails spans against the oracle with the code's three readings named
allm = 0; firstm = None
for idx, (raw, nw) in enumerate(zip(raws, new)):
    if nw['em'] is None: break
    if sorted(nw['em']) != sorted(oracle(nw['clean'], xn_ci=True, ws='rust')) or sorted(nw['emw']) != sorted(oracle(nw['cleanw'], xn_ci=True, ws='rust')):
        allm += 1; firstm = firstm or (idx, raw[:160], nw['em'], oracle(nw['clean'], xn_ci=True, ws='rust'))
print(f'[{LABEL}] every input: emails vs oracle (xn-- case-insensitive, Rust ASCII whitespace) mismatches = {allm}; first: {firstm}')
