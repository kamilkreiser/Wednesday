# QA-AUDIT-EMAIL-3 library (new code): model of strip / apply_mask / truncate / summary limits (copied in form from
# the last check's qa2_diff.py), MY oracle of the NEW grammar (written from build brief items 1 and 2 and RULINGS 1
# and 2, readings in my STATUS, 16:30), the OLD grammar (the last lane's, for my class rule), and the leak check.
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
def window(raw):
    bb = raw.encode(); e = min(len(bb), 65536)
    while e < len(bb) and (bb[e] & 0xC0) == 0x80: e -= 1
    return strip(bb[:e].decode())
def summ_of(raw, red): return 'E:FieldLimit("summary")' if len(raw.encode()) > 4 * 4096 or len(red.encode()) > 4096 else red

LOCAL = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-')
DOM = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-')
LET = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
ALNUM = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
RWS = frozenset(b' \t\n\x0c\r')        # Rust is_ascii_whitespace: NOT 0x0B
def stop(c): return c in RWS or c in b'"\'<>`' or c >= 0x80
INFO_END = frozenset(b'/?#,;)]}|&([{\x0b')   # RULING 1
SCHEME = ALNUM | frozenset(b'+.-')            # RULING 1

def nexts(b, pred):
    """nx[i] = first j >= i with pred(b[j]) (or len)."""
    n = len(b); nx = [n] * (n + 1); j = n
    for i in range(n - 1, -1, -1):
        if pred(b[i]): j = i
        nx[i] = j
    return nx

def dom_ok(d, xn_ci):
    labels = d.split(b'.')
    if len(labels) < 2 or any(not l for l in labels): return False
    last = labels[-1]
    xn = last[:4] == b'xn--' or (xn_ci and last[:4].lower() == b'xn--')
    return (len(last) >= 2 and all(c in LET for c in last)) or (len(last) >= 4 and xn)
def trim(d): return d.rstrip(b'.-')

def addr_at(b, at, xn_ci):
    """The span (s, E) of the address at this `@` by the grammar of the last lane (unchanged), or None."""
    n = len(b); s = at
    while s > 0 and b[s - 1] in LOCAL: s -= 1
    while s < at and b[s] == 0x2E: s += 1
    if s == at: return None
    e = at + 1
    while e < n and b[e] in DOM: e += 1
    run = b[at + 1:e]; d = trim(run)
    if not dom_ok(d, xn_ci):
        d = None
        for k in range(len(run), 0, -1):          # naive: every prefix from the longest
            if run[k - 1] in b'.-': continue      # its trimmed form equals a shorter prefix's, tried later
            t = trim(run[:k])
            if dom_ok(t, xn_ci): d = t; break
        if d is None: return None
    return (s, at + 1 + len(d))

def link_parts_new(b, w5b='lit', info=INFO_END, scheme_test=True):
    """[(start, user-info end)] of the tokens that shelter (RULING 1). w5b='lit': a `://` inside an UNOPENED token
    may open its own token (my primary reading); 'code': the search resumes at the token's end either way."""
    n = len(b); out = []; i = 0; nst = None
    while True:
        p = b.find(b'://', i)
        if p < 0: break
        st = p + 3; en = st
        while en < n and not stop(b[en]): en += 1
        opened = (not scheme_test) or (p > 0 and b[p - 1] in SCHEME)
        if opened:
            ui = next((k for k in range(st, en) if b[k] in info), en)
            out.append((st, ui)); i = max(en, st)
        else:
            i = p + 1 if w5b == 'lit' else max(en, st)
    return out

def link_parts_old(b):
    """The last lane's: every `://`, user-info to the first / ? # or the token's end."""
    n = len(b); out = []; i = 0
    while True:
        p = b.find(b'://', i)
        if p < 0: break
        st = p + 3; en = st
        while en < n and not stop(b[en]): en += 1
        ui = next((k for k in range(st, en) if b[k] in b'/?#'), en)
        out.append((st, ui, en)); i = max(en, st)
    return out

def oracle_new(t, xn_ci=False, w5b='lit', git_ci=False, b3_before_trim=False, clauses='ab', reasons=None):
    """MY oracle of the NEW grammar. Returns sorted spans. clauses: 'ab' the ruling; switches name decisions."""
    b = t.encode() if isinstance(t, str) else t; n = len(b)
    parts = link_parts_new(b, w5b)
    sheltered = bytearray(n + 1)
    for st, ui in parts:
        for k in range(st, ui): sheltered[k] = 1
    nstop = nexts(b, stop); nslash = nexts(b, lambda c: c == 0x2F)
    sp = []
    for at in range(n):
        if b[at] != 0x40 or sheltered[at]: continue
        a = addr_at(b, at, xn_ci)
        if a is None: continue
        s, E = a
        if E < n and b[E] == 0x3A:
            q = E + 1; te = nstop[q] if q <= n else n
            after = b[q:te]
            A = after[:1] == b'~' or nslash[q] < te or after.endswith(b'.git')
            loc = b[s:at]
            if b3_before_trim:
                s0 = at
                while s0 > 0 and b[s0 - 1] in LOCAL: s0 -= 1
                loc = b[s0:at]
            b1 = q < n and b[q] == 0x2F; b2 = q < n and b[q] == 0x7E
            b3 = loc == b'git' or (git_ci and loc.lower() == b'git'); b4 = after.endswith(b'.git')
            B = b1 or b2 or b3 or b4
            keep = (A and B) if clauses == 'ab' else (B if clauses == 'b' else A)
            if reasons is not None and keep: reasons.append((s, E, b1, b2, b3, b4))
            if keep: continue
        sp.append((s, E))
    return sp

def oracle_old(t, xn_ci=True):
    """The last lane's grammar (for my class rule and a check of the base's `emails`)."""
    b = t.encode() if isinstance(t, str) else t; n = len(b)
    parts = link_parts_old(b); sh = bytearray(n + 1)
    for st, ui, en in parts:
        for k in range(st, ui): sh[k] = 1
    nstop = nexts(b, stop); nslash = nexts(b, lambda c: c == 0x2F); sp = []
    for at in range(n):
        if b[at] != 0x40 or sh[at]: continue
        a = addr_at(b, at, xn_ci)
        if a is None: continue
        s, E = a
        if E < n and b[E] == 0x3A:
            q = E + 1; te = nstop[q]; after = b[q:te]
            if after[:1] == b'~' or nslash[q] < te or after.endswith(b'.git'): continue
        sp.append((s, E))
    return sp

def classes(b, s, E, parts=None, nstop=None):
    """My rule (iv): the set of OLD exclusions that, each alone, drop this span's `@`."""
    at = b.index(b'@', s); K = set()
    if parts is None: parts = link_parts_old(b)
    import bisect
    k = bisect.bisect_right([p[0] for p in parts], at) - 1 if not isinstance(parts, tuple) else bisect.bisect_right(parts[1], at) - 1
    pl = parts[0] if isinstance(parts, tuple) else parts
    if k >= 0 and pl[k][0] <= at < pl[k][1]: K.add('L')
    n = len(b)
    if E < n and b[E] == 0x3A:
        q = E + 1
        te = nstop[q] if nstop is not None else next((j for j in range(q, n) if stop(b[j])), n)
        after = b[q:te]
        if after[:1] == b'~' or b'/' in after or after.endswith(b'.git'): K.add('C')
    return K

def leak(pv, a, outside):
    """three-part leak check: whole (when under 8 bytes), the `@` with a byte each side, an 8-byte window;
    each only when that text is not in the rest of the input. Returns None / 'whole' / 'around-@' / 'window' / 'domain'."""
    pb, ab, ob = pv.encode(), a.encode(), outside.encode(); at = ab.index(b'@')
    def shows(w): return w in pb and w not in ob
    if ab in pb: return 'whole'
    if len(ab) < 8: return None
    if at >= 1 and at + 2 <= len(ab) and shows(ab[at - 1:at + 2]): return 'around-@'
    wins = [i for i in range(len(ab) - 7) if shows(ab[i:i + 8])]
    if not wins: return None
    if b"]" + ab[at:at + 9] in pb and not any(i < at for i in wins): return "domain"   # a mask then `@` and the domain (W-13)
    return 'window'

def spans(s): return [] if s in ('', '-') else [tuple(map(int, x.split('-'))) for x in s.split(',')]
def H(s): return bytes.fromhex(s).decode()
def rec(line):
    f = line.rstrip('\n').split('\t')
    clean = H(f[4]); cleanw = clean if f[5] == '=' else H(f[5]); sm = f[8]
    return dict(find=spans(f[0]), findw=spans(f[1]), em=spans(f[2]), emw=spans(f[3]), clean=clean, cleanw=cleanw,
                redact=H(f[6]), preview=H(f[7]), summ=sm if sm.startswith('E:') or sm == 'N' else H(sm),
                full=f[9] if f[9] in ('-', 'N') else H(f[9]))
