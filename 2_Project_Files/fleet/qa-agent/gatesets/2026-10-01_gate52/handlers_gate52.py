#!/usr/bin/env python3
"""handlers_gate52.py — the drafter's PREDICTION for requirements 1, 2 and 3 (THE RUNTIME TRUTH), a STATIC reading of blobs at the heads in the
SCRATCH clone. It is NOT a request: the gate reads each handler itself and cites file:line at the head.
RUNTIME: express / body-parser / express-validator versions in the root lock and the three service locks (kit.json locks), and each service's
express.json mount line. Under body-parser 1.x an ABSENT JSON body reaches the handler as {} (`req.body = req.body || {}`) — the gate cites that
line from the installed package; this instrument only reads the lock versions.
PART 1 — #1367, THE ENVELOPE (kit envelope_op RL1, GET /api/referrals/{code}): at #1367's head, read
  (a) the handler block (route anchor -> its closing `});`): every response it writes (`res.status(N).json(`, bare `res.json(` = 200,
      `next(error)` = delegated to the error handler), with file:line; the 200 body's top-level keys and its `data` keys; the 404 body's keys;
      the 404 condition (does it reference isActive?);
  (b) the spec block in the registry file (spec_anchor -> the next registerPath): the declared status keys; the 200 schema's top-level keys,
      its `data` keys and which are .optional();
  (c) the generated yaml at the head: the 200's two `required:` lists;
  (d) shared ErrorResponseSchema: success / error.code / error.message (the error envelope the spec's 4xx/5xx use).
  ENVELOPE OK when: handler 200 keys == spec keys (top and data), the yaml required lists == the spec's non-optional keys, every status the
  handler writes is declared, and the handler's 404 body has the ErrorResponse shape. Any disagreement is a FAIL (the gate rules it a Major).
  INFO lines (never a FAIL): spec statuses the handler never writes itself, the 404 description vs its condition, optional keys.
PART 2 — #1368, ABSENT BODY (kit operations TP1 / VV1 at #1368's head, control RG-CTL): per operation, file:line of the route, the validator,
  the fields (zod object or express-validator chain) with which are REQUIRED, every 4xx branch between the validator and the first 2xx write,
  and the kit's named guard (with its 400). Verdict REJECTS-EMPTY when a field is required OR the named guard answers 400; else ACCEPTS-EMPTY.
  For VV1 the alias line and the req.body destructure must name all four kit aliases. CONTROL RG-CTL (POST /api/referrals/generate, PR B's
  claim): must read ACCEPTS-EMPTY with NO 4xx branch after its parse — an extra branch there is exactly what made gate51a's TENANT control read
  ACCEPTS on a handler that rejects.
Overrides (controls): --tree-<n> <sha> (read #n's half at another commit). rc 0 PASS / rc 1 FAIL. Usage: handlers_gate52.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
P = json.load(open(os.path.join(G, 'pins_gate52.json'), encoding='utf-8'))
CL = os.path.join(SP, 'g52_sp', 'clone'); ORDER = K['order']; NA, NB = ORDER
T = {n: opt('--tree-' + n, P['pr_pins'][n]['head']) for n in ORDER}
def show(t, path):
    r = subprocess.run(['git', '-C', CL, 'show', '%s:%s' % (t, path)], capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: git show %s:%s rc %d' % (t[:12], path, r.returncode))
    return r.stdout.splitlines()
def first(lines, needle, start=0, end=None):
    for i in range(start, len(lines) if end is None else min(end, len(lines))):
        if needle in lines[i]: return i
    return None
def block_end(lines, i):
    d = 0; seen = False
    for j in range(i, len(lines)):
        d += lines[j].count('(') - lines[j].count(')')
        if '(' in lines[j]: seen = True
        if seen and d <= 0: return j
    return len(lines) - 1
def _strip(t):
    t = re.sub(r'//[^\n]*', '', t)
    return re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`[^`]*`", "''", t)
def _parse(t, k):
    """t[k] == '{': an object literal -> ({key: [offset, nested dict or None, value text]}, offset of its closing brace)"""
    out = {}; k += 1; n = len(t)
    while k < n:
        while k < n and t[k] in ' \t\n,': k += 1
        if k >= n or t[k] == '}': return out, k
        m = re.match(r"(\.\.\.)?\s*([A-Za-z_$][A-Za-z0-9_$]*|'')\s*(:)?", t[k:])
        key = m.group(2) if m and not m.group(1) else None; k += m.end() if m else 0
        has_val = bool(m and m.group(3)) or (m and m.group(1))
        start = k; nested = None; d = 0; nsr = None
        while k < n:
            c = t[k]
            if c == '{' and nested is None and ((d == 0 and t[start:k].strip() == '') or (d == 1 and re.search(r'(z\s*\.\s*object|\.object)\s*\(\s*$', t[start:k]))):
                ns0 = k; nested, k = _parse(t, k); k += 1; nsr = (ns0, k); continue
            if c in '([{': d += 1
            elif c in ')]}':
                if d == 0: break
                d -= 1
            elif c == ',' and d == 0: break
            k += 1
        vt = (t[start:nsr[0]] + '{...}' + t[nsr[1]:k]) if nsr else t[start:k]   # the value text OUTSIDE a nested object (its own modifiers only)
        if key and not (m and m.group(1)): out[key] = [start, nested, vt.strip() if has_val else '']
    return out, k
def obj_keys(lines, i):
    """keys of the FIRST object literal opening on line i (or after): {key: [lineno, nested, value text]}"""
    t = _strip('\n'.join(lines[i:i + 80])); k = t.find('{')
    if k < 0: return {}
    o, _ = _parse(t, k)
    def fix(dct):
        for v in dct.values():
            v[0] = i + 1 + t[:v[0]].count('\n')
            if v[1]: fix(v[1])
        return dct
    return fix(o)
res = []; info = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('OK  ' if ok else 'FAIL', tag, msg))
print('handlers_gate52 | #%s tree %s | #%s tree %s | clone %s' % (NA, T[NA][:12], NB, T[NB][:12], CL))
for lk in K['locks']:
    p = json.loads('\n'.join(show(T[NB], lk))).get('packages', {})
    print('RUNTIME %s at %s: express %s | body-parser %s | express-validator %s' % (lk, T[NB][:12], p.get('node_modules/express', {}).get('version'), p.get('node_modules/body-parser', {}).get('version'), p.get('node_modules/express-validator', {}).get('version')))
for svc, f in K['express_json'].items():
    ls = show(T[NB], f); i = first(ls, 'express.json(')
    print('MOUNT %s: %s:%s %s' % (svc, f.replace('Blockchain/Dev/services/', ''), i + 1 if i is not None else 'ABSENT', ls[i].strip() if i is not None else ''))
# ---------------- PART 1 ----------------
E = K['envelope_op']; t = T[E['pr']]
print('=== PART 1 #%s %s %s (tree %s)' % (E['pr'], E['id'], E['op'], t[:12]))
hl = show(t, E['file']); r = first(hl, E['route'])
if r is None: chk('%s route' % E['id'], False, 'route anchor %r ABSENT in %s' % (E['route'], E['file']))
else:
    e = block_end(hl, r); writes = []
    for j in range(r, e + 1):
        m = re.search(r'res\.status\((\d{3})\)\.json\(', hl[j])
        if m: writes.append((m.group(1), j))
        elif re.search(r'\bres\.json\(', hl[j]): writes.append(('200', j))
        if re.search(r'\bnext\((err|error)\)', hl[j]): writes.append(('next(error)', j))
    print('    handler %s:%d-%d | writes %s' % (E['file'].replace('Blockchain/Dev/services/', ''), r + 1, e + 1, ['%s@:%d' % (s, j + 1) for s, j in writes]))
    w200 = [j for s, j in writes if s == '200']; hk = obj_keys(hl, w200[0]) if w200 else {}
    hdata = (hk.get('data') or [0, None])[1] or {}
    print('    handler 200 body (:%s): top %s | data %s' % (w200[0] + 1 if w200 else 'NONE', sorted(hk), ['%s:%d' % (k2, v[0]) for k2, v in sorted(hdata.items())]))
    w404 = [j for s, j in writes if s == '404']; h404 = obj_keys(hl, w404[0]) if w404 else {}
    h404e = sorted(((h404.get('error') or [0, None])[1] or {}).keys())
    ci = next((x for x in range(w404[0], r, -1) if re.match(r'^\s*if \(', hl[x])), None) if w404 else None
    c404 = hl[ci].strip() if ci is not None else ''
    print('    handler 404 body (:%s): top %s | error %s | its condition (:%s) %r references isActive: %s' % (w404[0] + 1 if w404 else 'NONE', sorted(h404), h404e, (ci + 1) if ci is not None else '-', c404, 'isActive' in c404))
    sl = show(t, E['spec_file']); s = first(sl, E['spec_anchor'])
    if s is None: chk('%s spec' % E['id'], False, 'spec anchor %r ABSENT' % E['spec_anchor'])
    else:
        se = first(sl, 'sharedRegistry.registerPath(', s + 1) or len(sl)
        ri = first(sl, 'responses:', s, se); statuses = []
        for j in range(ri, se):
            m = re.match(r'^    (\d{3}):', sl[j])
            if m: statuses.append((m.group(1), j))
        s200 = [j for st, j in statuses if st == '200'][0] if any(st == '200' for st, _ in statuses) else None
        zo = first(sl, 'z.object({', s200, se) if s200 is not None else None
        top = obj_keys(sl, zo) if zo is not None else {}
        dz = first(sl, '.object({', top['data'][0] - 1, se) if 'data' in top else None
        dk = obj_keys(sl, dz) if dz is not None else {}
        sopt = sorted(k2 for k2, v in dk.items() if '.optional()' in v[2])
        print('    spec %s:%d-%d | statuses %s | 200 z.object :%s top %s | data .object :%s %s | optional %s' % (
            E['spec_file'].replace('Blockchain/Dev/services/', ''), s + 1, se, [x for x, _ in statuses], (zo or -1) + 1, sorted(top), (dz or -1) + 1, sorted(dk), sopt))
        yl = show(t, K['yaml']); yp = first(yl, '  %s:' % E['spec_path']); yg = first(yl, '    get:', yp) if yp is not None else None
        y200 = first(yl, '        "200":', yg) if yg is not None else None; yreq = []
        if y200 is not None:
            yend = next((j for j in range(y200 + 1, len(yl)) if re.match(r'^        "\d{3}":', yl[j]) or re.match(r'^    \S', yl[j])), len(yl)); cur = None
            for j in range(y200, yend):
                if yl[j].strip() == 'required:': cur = []; yreq.append((j + 1, cur)); continue
                m = re.match(r'^\s+- (\S+)$', yl[j])
                if m and cur is not None: cur.append(m.group(1))
                elif cur is not None and not m: cur = None
        print('    yaml %s get 200 (:%s): required lists %s' % (E['spec_path'], (y200 or -1) + 1, ['%s@:%d' % (v, ln) for ln, v in yreq]))
        rs = show(t, 'Blockchain/Dev/packages/shared/src/openapi/responses.ts'); er = first(rs, "'ErrorResponse',")
        erk = obj_keys(rs, first(rs, '.object({', er)) if er is not None else {}
        erek = sorted(((erk.get('error') or [0, None])[1] or {}).keys())
        req_of = lambda dd: sorted(x for x, vv in dd.items() if '.optional()' not in vv[2])
        ertop_req = req_of(erk); erer_req = req_of((erk.get('error') or [0, None])[1] or {})
        print('    shared ErrorResponseSchema (responses.ts:%s): top %s (required %s) | error %s (required %s)' % ((er or -1) + 1, sorted(erk), ertop_req, erek, erer_req))
        undeclared = sorted(set(st for st, _ in writes if st.isdigit()) - set(x for x, _ in statuses))
        chk('%s 200 top keys' % E['id'], sorted(hk) == sorted(top) and bool(hk), 'handler %s == spec %s' % (sorted(hk), sorted(top)))
        chk('%s 200 data keys' % E['id'], sorted(hdata) == sorted(dk) and bool(hdata), 'handler %s == spec %s' % (sorted(hdata), sorted(dk)))
        want_req = [sorted(set(dk) - set(sopt)), sorted(top)]
        got_req = sorted([sorted(v) for _, v in yreq])
        chk('%s yaml required' % E['id'], got_req == sorted(want_req), 'yaml required lists %s == the spec\'s non-optional keys %s' % (got_req, sorted(want_req)))
        chk('%s statuses declared' % E['id'], not undeclared and any(st == '404' for st, _ in writes), 'handler writes %s; undeclared in the spec: %s' % (sorted(set(st for st, _ in writes)), undeclared or 'NONE'))
        chk('%s 404 envelope' % E['id'], bool(h404) and set(ertop_req) <= set(h404) <= set(erk) and bool(erer_req) and set(erer_req) <= set(h404e) <= set(erek),
            '404 body top %s error %s within ErrorResponse top %s (required %s) error %s (required %s)' % (sorted(h404), h404e, sorted(erk), ertop_req, erek, erer_req))
        never = sorted(set(x for x, _ in statuses) - set(st for st, _ in writes))
        info.append('INFO %s: spec statuses the handler never writes itself: %s (401 is jwtAuthenticate at the /api mount, the rest via next(error) / gateway / limiter — the gate rules each)' % (E['id'], never))
        info.append('INFO %s: the 404 is described "%s" but its condition %r references isActive: %s (an inactive code answers 200 with isActive:false?)' % (
            E['id'], next((re.search(r"description: '([^']+)'", sl[j]).group(1) for st, j in statuses if st == '404' and re.search(r"description: '([^']+)'", sl[j])), '?'), c404, 'isActive' in c404))
        info.append('INFO %s: spec-optional data keys %s; the handler writes each unconditionally (an undefined value drops from JSON; a null would not)' % (E['id'], sopt))
# ---------------- PART 2 ----------------
print('=== PART 2 #%s absent body (tree %s)' % (NB, T[NB][:12]))
def zfields(lines, i):
    out = []; depth = 0
    for j in range(i, min(i + 60, len(lines))):
        l = lines[j]
        if j > i and depth == 1:
            m = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(z\..*)$', l)
            if m: out.append((m.group(1), not re.search(r'\.optional\(\)|\.default\(|\.nullish\(\)', l), j + 1))
        depth += l.count('{') - l.count('}')
        if j > i and depth <= 0: break
    return out
for o in K['operations'] + K.get('control_operations', []):
    t = T[o['pr']]; want = o['expect']; ls = show(t, o['file']); r = first(ls, o['route'])
    if r is None: chk(o['id'], False, 'route anchor %r ABSENT in %s' % (o['route'], o['file'])); continue
    v = first(ls, o['validator'], r, r + 15)
    if v is None: chk(o['id'], False, 'validator %r not within 15 lines of %s:%d' % (o['validator'], o['file'], r + 1)); continue
    if o['schema'] == 'EXPRESS-VALIDATOR':
        fl = [(m.group(1), '.optional()' not in ls[j], j + 1) for j in range(r, v) for m in [re.search(r"body\('([A-Za-z_]+)'\)", ls[j])] if m]; how = 'express-validator chain'
    else:
        sl = show(t, o['schema_file']); si = first(sl, o['schema']); fl = zfields(sl, si) if si is not None else []; how = 'named zod .parse at :%d, schema :%s' % (v + 1, (si or -1) + 1)
    end2 = next((j for j in range(v, min(v + 80, len(ls))) if re.search(r'res\.(status\(2\d\d\)\.)?json\(\{\s*(success: true|hash)', ls[j]) or re.search(r'res\.status\(2\d\d\)', ls[j])), min(v + 80, len(ls)))
    br = [(j + 1, ls[j].strip()) for j in range(v, end2) if re.match(r'^\s*if \(', ls[j]) and any(re.search(r'status\(4\d\d\)', ls[x]) for x in range(j, min(j + 4, end2 + 1)))]
    g = first(ls, o['guard'], v, end2 + 1) if o.get('guard') else None
    g400 = g is not None and any('status(400)' in ls[x] for x in range(g, g + 4))
    req = [n for n, q, _ in fl if q]
    verdict = 'REJECTS-EMPTY' if req or g400 else 'ACCEPTS-EMPTY'
    extra = ''
    if o.get('aliases'):
        al = first(ls, o['alias_line'], v, end2 + 1); ds = first(ls, '= req.body || {}', v, end2 + 1)
        aok = al is not None and ds is not None and all(re.search(r'\b%s\b' % a, ls[al]) for a in o['aliases']) and all(re.search(r'\b%s\b' % a, ls[ds]) for a in o['aliases'])
        extra = ' | aliases %s: coalesce :%s %r, destructure :%s, all named: %s' % (o['aliases'], (al or -1) + 1, ls[al].strip() if al is not None else '', (ds or -1) + 1, aok)
        if not aok: verdict += ' (ALIASES MISSING)'
    ok = verdict == want and (want == 'REJECTS-EMPTY' or not br)
    chk('%s %s' % (o['id'], o['op']), ok, 'route %s:%d | validator :%d (%s) | fields %s | required %s | 4xx branches after the validator %s | guard %r :%s answers 400: %s%s | %s (want %s)%s' % (
        o['file'].replace('Blockchain/Dev/services/', ''), r + 1, v + 1, how, ['%s%s:%d' % (n, '' if q else '?', ln) for n, q, ln in fl], req or 'NONE',
        ['%d %s' % b for b in br] or 'NONE', o.get('guard'), (g or -1) + 1 if g is not None else '-', g400, extra, verdict, want, '  <- CONTROL (PR B\'s claim)' if o in K.get('control_operations', []) else ''))
for x in info: print(x)
nf = res.count(False)
print('HANDLERS %s: %d checks, %d FAIL | envelope %s at %s | absent-body %s at %s | control %s' % (
    'PASS' if nf == 0 else 'FAIL', len(res), nf, E['id'], T[E['pr']][:12], '/'.join(o['id'] for o in K['operations']), T[NB][:12], '/'.join(o['id'] for o in K.get('control_operations', []))))
raise SystemExit(1 if nf else 0)
