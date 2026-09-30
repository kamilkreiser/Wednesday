#!/usr/bin/env python3
"""lockdelta_gate49a.py — the drafter's READ of ITEM A's 18 locks (a PREDICTION for LOCK-DELTA-18 / DEPENDENT-RANGES / REGISTRY-TRUE /
ADVISORY-RANGES; the gate re-derives every line with its own code and reproduces the refresh itself — the drafter ran no npm). From the SCRATCH
clone (<scratchpad>/g49a_sp/clone), `git show` at the BASE (pins develop) and the HEAD (pins head; or --head <sha> for a control plant):
  L0 the changed paths == kit.json files (the 18 locks), all `package-lock.json`, 0 manifests, 0 other files; numstat per lock + sum
     (the seat claimed +102/-102: printed beside the measured sum as CLAIM MATCH / CLAIM DIFFERS — a claim, judged by the gate).
  L1 per lock: parses; lockfileVersion / name / top-level keys equal; the root "" entry (the manifest mirror) JSON-equal; entries equal in
     number; ADDED 0 / REMOVED 0.
  L2 per lock, EVERY changed entry listed with every field that differs and its flags (dev / devOptional / optional / peer: ABSENT = PROD);
     each changed entry's differing fields must be exactly {version, resolved, integrity} (a flag flip, a dependency-range change or any
     other field is a FAIL, named); every moved package is one of kit.json packages and stays in its MAJOR (an in-range refresh).
  L3 the moved set (lock, key, from -> to, PROD/dev) == kit.json claimed.moves_by_lock EXACTLY (30), and the PROD moves == claimed.prod_moves.
  L4 DEPENDENT-RANGES: for every moved entry, every dependant in the same lock (an entry whose dependencies / optionalDependencies /
     peerDependencies — plus devDependencies for the root and workspace entries — name the package AND whose node resolution walk lands on
     that entry): its declared range, and whether the HEAD version and the BASE version satisfy it (npm semver: ^ ~ x-ranges, hyphen, ||,
     comparators). FAIL if any head version is outside a dependant's range, or a moved entry has NO dependant. CONTROL L4c: the same
     evaluator judges <major+1>.0.0 against every one of those ranges and must say NOT satisfied every time; L4s: a fixed table of
     semver cases (each must hold) proves the evaluator.
  L5 REGISTRY-TRUE: for every distinct (package, to-version): `resolved` and `integrity` of every head entry == the npm registry's
     dist.tarball / dist.integrity (public GET https://registry.npmjs.org/<pkg>/<ver>). CONTROLS L5c: (1) the from-version's registry
     integrity and (2) the right integrity with ONE character flipped, compared the same way, must each read False.
  L6 ADVISORY-RANGES: each of the six advisories READ from the GitHub advisory API (authenticated GET of the public endpoint, GH_TOKEN by name):
     severity, published_at, its package's vulnerable ranges; every to-version OUTSIDE every range of its package; every from-version INSIDE
     at least one range of at least one advisory of its package (the control that the comparison can say yes).
  L7 RESIDUE at the head, over EVERY tracked package-lock.json (not only the 18): each brace-expansion / fast-uri / ip-address entry still
     inside any of the six ranges — lock, key, version, flag. Printed, never judged here: whether legs 6/7 read that lock (mobile/secuura-app is
     KS 769's declared scope) is the gate's. At develop (`--head <develop>`) the same census is the control that it fires.
  L8 THE STUB FIXTURE: advisory-fetch-stub.mjs's SYNTHETIC finding (fast-uri >=3.1.0 <4.0.0): the fast-uri entries at the head inside that range
     (the planted-refusal control the gate uses stays live only if at least one is).
  L9 the raw text: per lock `git diff -U0`: every changed line is a version / resolved / integrity line and there are 3 per move.
--offline (controls): skip L5 / L6 / L7's network reads and say so (NOT MEASURED). --head <sha>: judge that commit instead of the pinned head.
--pins <name>: read pins_gate49a.SIM-<name>.json (a dry test) instead of pins_gate49a.json.
rc 0 LOCKDELTA PASS / rc 1 FAIL. Writes nothing. Usage: lockdelta_gate49a.py <scratchpad> [--head <sha>] [--offline] [--pins <name>]"""
import json, os, re, subprocess, sys, urllib.request, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; OFF = '--offline' in A
PF = 'pins_gate49a.SIM-%s.json' % A[A.index('--pins') + 1] if '--pins' in A else 'pins_gate49a.json'
P = json.load(open(os.path.join(G, PF), encoding='utf-8'))
CL = os.path.join(SP, 'g49a_sp', 'clone'); N = P['pr']; BASE = P['develop']
HEAD = A[A.index('--head') + 1] if '--head' in A else P['pr_pins']['head']
FILES = sorted(K['prs'][N if N in K['prs'] else '<PR>']['files']); PKGS = K['packages']; CLAIM = K['claimed']
def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode not in ok: raise SystemExit('REFUSING: git %s rc %d %s' % (' '.join(a[:3]), r.returncode, r.stderr[:200]))
    return r.stdout
HEAD = git('rev-parse', HEAD + '^{commit}').strip()
bad = []; nchk = 0
def chk(tag, ok, msg):
    global nchk; nchk += 1
    print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
    if not ok: bad.append(tag)
def J(t, p): return json.loads(git('show', '%s:%s' % (t, p)))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('lockdelta_gate49a %s | %d locks at base %s and head %s | pins %s%s' % (now, len(FILES), BASE[:12], HEAD[:12], PF, ' (OFFLINE: L5/L6/L7 not measured)' if OFF else ''))
# ---- semver (npm semantics for plain x.y.z; pre-releases never satisfy a range without one) ----
def pv(s):
    m = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+.*)?', s.strip()); return (int(m[1]), int(m[2]), int(m[3]), m[4]) if m else None
def xr(s):   # partial version -> list with None for x/*/missing
    s = s.strip().lstrip('v=')
    if s in ('', '*', 'x', 'X'): return [None, None, None]
    ps = re.split(r'[.]', s.split('-')[0].split('+')[0]) + [None, None]
    return [None if (p is None or p in ('x', 'X', '*')) else int(p) for p in ps[:3]]
def comps(c):
    c = c.strip()
    m = re.match(r'^(\^|~>?|>=|<=|>|<|=)?\s*(.*)$', c); op, v = m.group(1) or '', m.group(2); M, m_, p = xr(v)
    if op == '^':
        M = M or 0
        if m_ is None: return [('>=', (M, 0, 0)), ('<', (M + 1, 0, 0))]
        if p is None: return [('>=', (M, m_, 0)), ('<', (M + 1, 0, 0) if M else (0, m_ + 1, 0))]
        if M: return [('>=', (M, m_, p)), ('<', (M + 1, 0, 0))]
        if m_: return [('>=', (0, m_, p)), ('<', (0, m_ + 1, 0))]
        return [('>=', (0, 0, p)), ('<', (0, 0, p + 1))]
    if op in ('~', '~>'):
        if M is None: return []
        if m_ is None: return [('>=', (M, 0, 0)), ('<', (M + 1, 0, 0))]
        return [('>=', (M, m_, p or 0)), ('<', (M, m_ + 1, 0))]
    if M is None: return [] if op in ('', '=', '>=', '<=') else [('<', (0, 0, 0))]
    if op in ('', '='):
        if m_ is None: return [('>=', (M, 0, 0)), ('<', (M + 1, 0, 0))]
        if p is None: return [('>=', (M, m_, 0)), ('<', (M, m_ + 1, 0))]
        return [('=', (M, m_, p))]
    if op == '>':
        if m_ is None: return [('>=', (M + 1, 0, 0))]
        if p is None: return [('>=', (M, m_ + 1, 0))]
        return [('>', (M, m_, p))]
    if op == '>=': return [('>=', (M, m_ or 0, p or 0))]
    if op == '<': return [('<', (M, m_ or 0, p or 0))]
    if op == '<=':
        if m_ is None: return [('<', (M + 1, 0, 0))]
        if p is None: return [('<', (M, m_ + 1, 0))]
        return [('<=', (M, m_, p))]
def sat(ver, rng):
    v = pv(ver)
    if v is None: return None
    if not re.fullmatch(r'[\s\d.xX*^~<>=|v-]*', rng or ''): return None   # npm: / file: / git / tag — not a semver range
    t = v[:3]
    for alt in (rng or '*').split('||'):
        alt = alt.strip(); cs = []
        h = re.fullmatch(r'(\S+)\s+-\s+(\S+)', alt)
        if h:
            lo, hi = xr(h[1]), xr(h[2]); cs.append(('>=', tuple(x or 0 for x in lo)))
            cs += [('<=', tuple(hi))] if None not in hi else ([('<', (hi[0] + 1, 0, 0))] if hi[1] is None else [('<', (hi[0], hi[1] + 1, 0))])
        else:
            for c in re.sub(r'(>=|<=|>|<|=|\^|~)\s+', r'\1', alt).split(): cs += comps(c)
        f = {'>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b, '>': lambda a, b: a > b, '<': lambda a, b: a < b, '=': lambda a, b: a == b}
        if all(f[o](t, x) for o, x in cs) and not v[3]: return True
    return False
CASES = [('5.0.12', '^5.0.5', True), ('6.0.0', '^5.0.5', False), ('1.1.21', '^1.1.7', True), ('2.0.0', '^1.1.7', False), ('0.2.5', '^0.2.3', True),
         ('0.3.0', '^0.2.3', False), ('3.1.8', '^3.0.1', True), ('3.1.8', '~3.1.7', True), ('3.2.0', '~3.1.7', False), ('10.7.2', '^10.0.1', True),
         ('10.7.2', '>=10.0.0 <10.7.1', False), ('10.7.2', '1.x || >=10.7.2', True), ('1.5.0', '1.2.3 - 1.9', True), ('2.0.0', '1.2.3 - 1.9', False),
         ('5.0.12', '*', True), ('5.0.12', '5.x', True), ('5.0.12', '>= 5.0.0, < 5.0.10'.replace(',', ''), False), ('5.0.12-rc.1', '^5.0.5', False)]
cfail = [c for c in CASES if sat(c[0], c[1]) != c[2]]
chk('L4s', not cfail, 'the semver evaluator holds on %d fixed cases (npm semantics; e.g. ^0.2.3 excludes 0.3.0, a pre-release never satisfies ^5.0.5): failures %s' % (len(CASES), cfail or 'none'))
# ---- node resolution walk ----
def parent(base):
    i = base.rfind('/node_modules/')
    if i >= 0: return base[:i]
    return ''
def resolve(pk, frm, name):
    base = frm
    while True:
        key = (base + '/node_modules/' + name) if base else 'node_modules/' + name
        if key in pk: return key
        if not base: return None
        base = parent(base) if '/node_modules/' in base else ''
def nameof(key): return key.rsplit('node_modules/', 1)[-1]
# ---- L0 ----
names = git('diff', '--name-only', BASE, HEAD).split('\n'); names = sorted(x for x in names if x)
ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in git('diff', '--numstat', BASE, HEAD).splitlines()}
sa, sd = sum(int(a) for a, d in ns.values() if a.isdigit()), sum(int(d) for a, d in ns.values() if d.isdigit())
chk('L0', names == FILES and all(p.endswith('/package-lock.json') for p in names), 'changed paths %d == the kit\'s 18 locks: %s | extra %s | missing %s | manifests changed %d | non-lock %d' % (
    len(names), names == FILES, sorted(set(names) - set(FILES)) or 'none', sorted(set(FILES) - set(names)) or 'none',
    sum(1 for p in names if p.endswith('package.json')), sum(1 for p in names if not p.endswith('package-lock.json'))))
print('    numstat sum +%d/-%d | the seat claimed %s: CLAIM %s' % (sa, sd, CLAIM['numstat'], 'MATCH' if '+%d/-%d' % (sa, sd) == CLAIM['numstat'] else 'DIFFERS'))
MOVES = {}; PROD = []; RES = {}
FLAGS = ('dev', 'devOptional', 'optional', 'peer')
def fl(e): return ','.join(f for f in FLAGS if e.get(f)) or 'PROD'
for lk in FILES:
    if lk not in names: continue
    b, h = J(BASE, lk), J(HEAD, lk); bp, hp = b.get('packages') or {}, h.get('packages') or {}
    top = sorted(set(b) | set(h)); topd = [x for x in top if x != 'packages' and b.get(x) != h.get(x)]
    add, rem = sorted(set(hp) - set(bp)), sorted(set(bp) - set(hp)); ch = sorted(k for k in set(bp) & set(hp) if bp[k] != hp[k])
    chk('L1 ' + lk, not topd and bp.get('') == hp.get('') and len(bp) == len(hp) and not add and not rem and b.get('lockfileVersion') == 3,
        'lockfileVersion %s | top-level fields that differ %s | root "" entry equal %s | entries %d -> %d | ADDED %d %s | REMOVED %d %s | changed %d' % (
            h.get('lockfileVersion'), topd or 'none', bp.get('') == hp.get(''), len(bp), len(hp), len(add), add[:3], len(rem), rem[:3], len(ch)))
    MOVES[lk] = []
    for k in ch:
        dk = sorted(x for x in set(bp[k]) | set(hp[k]) if bp[k].get(x) != hp[k].get(x)); nm = nameof(k)
        fb, fh = pv(bp[k].get('version', '')), pv(hp[k].get('version', ''))
        ok = dk == ['integrity', 'resolved', 'version'] and nm in PKGS and fb and fh and fb[0] == fh[0] and fh[:3] > fb[:3] and fl(bp[k]) == fl(hp[k])
        MOVES[lk].append('%s %s -> %s%s' % (k, bp[k].get('version'), hp[k].get('version'), ' PROD' if fl(hp[k]) == 'PROD' else ''))
        if fl(hp[k]) == 'PROD': PROD.append('%s %s' % (lk, k))
        chk('L2 %s %s' % (lk.replace('/package-lock.json', ''), k), ok, '%s -> %s | flags %s -> %s | fields that differ %s (want exactly integrity, resolved, version) | same major, upward: %s' % (
            bp[k].get('version'), hp[k].get('version'), fl(bp[k]), fl(hp[k]), dk, bool(fb and fh and fb[0] == fh[0] and fh[:3] > fb[:3])))
    RES[lk] = (bp, hp)
tot = sum(len(v) for v in MOVES.values())
cm = {lk: sorted(v) for lk, v in CLAIM['moves_by_lock'].items()}; gm = {lk: sorted(v) for lk, v in MOVES.items()}
diffl = sorted(set(cm) | set(gm)); dd = [(lk, sorted(set(gm.get(lk, [])) - set(cm.get(lk, []))), sorted(set(cm.get(lk, [])) - set(gm.get(lk, [])))) for lk in diffl if gm.get(lk, []) != cm.get(lk, [])]
chk('L3', not dd and tot == CLAIM['moves'], 'moves measured %d (claimed %d); per lock == the seat\'s claim (%s): %s' % (tot, CLAIM['moves'], 'claimed.moves_by_lock', 'EQUAL' if not dd else dd[:4]))
chk('L3p', sorted(PROD) == sorted(CLAIM['prod_moves']), 'PROD moves measured %d == claimed %d: %s' % (len(PROD), len(CLAIM['prod_moves']), sorted(PROD) == sorted(CLAIM['prod_moves']) or sorted(set(PROD) ^ set(CLAIM['prod_moves']))))
# ---- L4 ----
print('L4 DEPENDENT-RANGES — every dependant of every moved entry, its declared range, head / base satisfied')
nd = 0; nctl = 0; ctlbad = []
for lk in FILES:
    if lk not in RES: continue
    bp, hp = RES[lk]
    for mv in MOVES[lk]:
        k = mv.split(' ')[0]; nm = nameof(k); hv, bv = hp[k]['version'], bp[k]['version']; wrong = '%d.0.0' % (pv(hv)[0] + 1); deps = []
        for dkey, de in hp.items():
            rs = {}
            for fld in ('dependencies', 'optionalDependencies', 'peerDependencies') + (('devDependencies',) if not dkey.startswith('node_modules/') and '/node_modules/' not in dkey else ()):
                if nm in (de.get(fld) or {}): rs[fld] = de[fld][nm]
            for fld, rng in rs.items():
                if resolve(hp, dkey, nm) == k: deps.append((dkey or '(root)', fld, rng, sat(hv, rng), sat(bv, rng), sat(wrong, rng)))
        nd += len(deps); nctl += len(deps); ctlbad += [d for d in deps if d[5] is not False]
        good = bool(deps) and all(d[3] is True for d in deps)
        chk('L4 %s %s' % (lk.replace('/package-lock.json', ''), k), good, '%s -> %s | %d dependant(s): %s' % (bv, hv, len(deps), ' ; '.join('%s %s %r head %s base %s' % (d[0][-60:], d[1][:4], d[2], d[3], d[4]) for d in deps[:5]) + (' …' if len(deps) > 5 else '')))
chk('L4c', nctl > 0 and not ctlbad, 'CONTROL: <major+1>.0.0 judged against all %d dependant range(s) reads NOT satisfied every time (a wrong version is refused): %s' % (nctl, 'yes' if not ctlbad else 'NO %s' % ctlbad[:3]))
# ---- L5 / L6 / L7 ----
def _tok():
    try:
        for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
            if l.startswith('GH_TOKEN='): return l.split('=', 1)[1].strip().strip('"').strip("'")
    except OSError: pass
    return ''
_T = _tok()
def ADVGET(g): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/advisories/' + g, headers=dict({'Accept': 'application/vnd.github+json'}, **({'Authorization': 'Bearer ' + _T} if _T else {}))), timeout=60))
def inr(ver, rng):   # advisory range syntax: ">= 5.0.0, < 5.0.10" ; "< 1.1.12" ; "= 10.7.0"
    v = pv(ver)
    for c in rng.split(','):
        m = re.match(r'\s*(>=|<=|>|<|=)?\s*v?([\d.]+)', c); op, x = m.group(1) or '=', tuple(int(y) for y in (m.group(2).split('.') + ['0', '0'])[:3])
        if not {'>=': v[:3] >= x, '<=': v[:3] <= x, '>': v[:3] > x, '<': v[:3] < x, '=': v[:3] == x}[op]: return False
    return True
pairs = sorted(set((nameof(mv.split(' ')[0]), mv.split(' ')[1], mv.split(' ')[3]) for v in MOVES.values() for mv in v))
if OFF: print('NOT MEASURED L5 / L6 / L7: --offline (the registry and the advisory API were not read)')
else:
    for nm, fv, tv in pairs:
        rt = json.load(urllib.request.urlopen('https://registry.npmjs.org/%s/%s' % (nm, tv), timeout=60))['dist']
        rf = json.load(urllib.request.urlopen('https://registry.npmjs.org/%s/%s' % (nm, fv), timeout=60))['dist']
        ents = [(lk, hp[k]) for lk, (bp, hp) in RES.items() for k in hp if nameof(k) == nm and hp[k].get('version') == tv and k in [m.split(' ')[0] for m in MOVES[lk]]]
        eq = all(e.get('resolved') == rt['tarball'] and e.get('integrity') == rt['integrity'] for _, e in ents)
        i = rt['integrity']; flip = i[:12] + ('A' if i[12] != 'A' else 'B') + i[13:]
        c1 = any(e.get('integrity') == rf['integrity'] for _, e in ents); c2 = any(e.get('integrity') == flip for _, e in ents)
        chk('L5 %s@%s' % (nm, tv), bool(ents) and eq, '%d head entr(y/ies) resolved/integrity == registry dist (%s, %s…)' % (len(ents), rt['tarball'], i[:24]))
        chk('L5c %s@%s' % (nm, tv), not c1 and not c2, 'CONTROLS: the from-version %s registry integrity (%s…) reads %s; the right integrity with char 13 flipped reads %s (both must be False)' % (fv, rf['integrity'][:20], c1, c2))
    RNG = {}
    for g, meta in K['advisories'].items():
        a = ADVGET(g); r = [v.get('vulnerable_version_range') for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == meta['package']]
        fp = [v.get('first_patched_version') for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == meta['package']]
        RNG[g] = (meta['package'], r)
        tos = sorted(set(tv for nm, fv, tv in pairs if nm == meta['package'])); frs = sorted(set(fv for nm, fv, tv in pairs if nm == meta['package']))
        out = bool(r) and all(not inr(t, x) for t in tos for x in r); inside = [f for f in frs if any(inr(f, x) for x in r)]
        chk('L6 %s' % g, out, '%s %s published %s (claimed %s) | ranges %s | first patched %s | to-versions %s OUTSIDE every range: %s | from-versions inside (control): %s' % (
            meta['package'], a.get('severity'), a.get('published_at'), meta['claimed_severity'], r, fp, tos, out, inside or 'NONE'))
    for pk in PKGS:
        frs = sorted(set(fv for nm, fv, tv in pairs if nm == pk))
        ctl = all(any(inr(f, x) for g, (p2, rs) in RNG.items() if p2 == pk for x in rs) for f in frs)
        chk('L6c %s' % pk, bool(frs) and ctl, 'CONTROL: every from-version %s of %s is INSIDE at least one range of its advisories (the comparison can say yes)' % (frs, pk))
    print('L7 RESIDUE at %s over every tracked package-lock.json — entries still inside any of the six ranges' % HEAD[:12])
    alll = sorted(f for f in git('ls-tree', '-r', '--name-only', HEAD).split('\n') if f.endswith('package-lock.json') and '/node_modules/' not in '/' + f)
    resid = []
    for lk in alll:
        try: pk = (json.loads(git('show', '%s:%s' % (HEAD, lk))).get('packages') or {})
        except Exception: continue
        for k, e in pk.items():
            nm = nameof(k)
            if nm not in PKGS or 'version' not in e or not pv(e['version']): continue
            hits = [g for g, (p2, rs) in RNG.items() if p2 == nm and any(inr(e['version'], x) for x in rs)]
            if hits: resid.append((lk, k, e['version'], fl(e), hits))
    for r in resid: print('    RESIDUE %-58s %-60s %-8s %-6s %s' % (r[0], r[1][-60:], r[2], r[3], [h[:9] for h in r[4]]))
    print('L7 RESIDUE: %d entr(y/ies) in %d lock(s) of %d at the head: %s' % (len(resid), len(set(r[0] for r in resid)), len(alll), sorted(set(r[0] for r in resid)) or 'none'))
    fx = K['stub_fixture']; fu = []
    for lk in alll:
        try: pk = (json.loads(git('show', '%s:%s' % (HEAD, lk))).get('packages') or {})
        except Exception: continue
        fu += [(lk, k, e.get('version')) for k, e in pk.items() if nameof(k) == 'fast-uri' and sat(e.get('version', ''), fx['range'])]
    print('L8 STUB FIXTURE %s (%s %s): %d fast-uri entr(y/ies) at the head inside it, in %d lock(s) — the planted-refusal control %s' % (
        fx['id'], fx['package'], fx['range'], len(fu), len(set(x[0] for x in fu)), 'stays LIVE' if fu else 'would be DEAD'))
# ---- L9 ----
for lk in FILES:
    if lk not in names: continue
    d = git('diff', '-U0', BASE, HEAD, '--', lk)
    chg = [l for l in d.splitlines() if l[:1] in '+-' and not l.startswith(('+++', '---'))]
    okl = all(re.match(r'^[+-]\s+"(version|resolved|integrity)": ', l) for l in chg) and len(chg) == 6 * len(MOVES.get(lk, []))
    chk('L9 ' + lk.replace('/package-lock.json', ''), okl, 'git diff -U0: %d changed line(s) == 6 x %d moves, all version/resolved/integrity lines: %s | numstat %s' % (len(chg), len(MOVES.get(lk, [])), okl, ' '.join(ns.get(lk, ('?', '?')))))
print('LOCKDELTA %s: %d FAIL of %d checks | base %s head %s | %d locks, %d moves (%d PROD), %d dependant range(s) | numstat +%d/-%d | sha256 of the moved-set %s' % (
    'PASS' if not bad else 'FAIL', len(bad), nchk, BASE[:12], HEAD[:12], len(MOVES), tot, len(PROD), nd, sa, sd, hashlib.sha256(json.dumps(gm, sort_keys=True).encode()).hexdigest()[:16]))
raise SystemExit(1 if bad else 0)
