#!/usr/bin/env python3
"""lockdelta_gate49b.py — the POST-MERGE AUDIT read of #1358 (merged by PeterObeden at 07:28:02Z as a merge commit, before any gate; kit.json
post_merge_audit). HEAD = the MERGE COMMIT (what landed), BASE = its FIRST PARENT (develop just before), plus L8: every landed blob == #1358's PR head blob.
Was: the drafter's READ of #1358 (KS-1380, Seat D 1st): 15 package-lock.json moved so every lock agrees with packages/shared on
@types/express-serve-static-core and @types/pg. Base = #1358's MERGE-BASE (its own delta, even when develop has moved on), develop = pins develop (L6 reads it too), head = pins #1358 head, END = pins end_tree. All reads are `git show` in the
SCRATCH clone (<scratchpad>/g49b_sp/clone), never the checkout. A PREDICTION for the gate, never evidence.
  L0 the changed paths == kit.json's 15 locks, 0 package.json, 0 non-lock; numstat sum vs the seat's claim (+81/-77).
  L1 per lock: lockfileVersion / name / every top-level key but `packages` / the root "" entry EQUAL; entry key sets EQUAL (ADDED 0 / REMOVED 0).
  L2 every CHANGED entry is an @types/express-serve-static-core or @types/pg entry (kit types_packages, any depth); the fields that differ are a
     subset of {version, resolved, integrity}; no flag (dev / devOptional / optional / peer) flips. INFO: entries whose `resolved` / `integrity`
     were ABSENT at base and PRESENT at head (a base entry `npm ci` could not integrity-check).
  L3 the moves: count vs the seat's 27; each to-version == packages/shared's lock version of that package (the target); every move inside its
     MAJOR; the flag of each moved entry (ABSENT = PRODUCTION) — every PRODUCTION move is listed by lock.
  L4 DEPENDENT RANGES: every dependant (an entry whose dependencies / optionalDependencies / peerDependencies — and devDependencies of the root and
     workspace entries — name the package AND whose node resolution walk lands on the moved entry) satisfies the head version; CONTROL: <major+1>.0.0
     must satisfy NONE. L4s: the semver evaluator on fixed cases.
  L5 REGISTRY-TRUE (public GET https://registry.npmjs.org/<pkg>/<ver>; --offline skips): every head entry's resolved / integrity == the registry's
     dist; CONTROLS: the from-version's integrity and the right integrity with one character flipped compare False.
  L6 AGREEMENT (the drafter's OWN implementation, not the seat's lockagree_d1.py): every tracked package-lock.json under Blockchain/Dev except
     packages/shared, at base / head / END: TOP-LEVEL copies of each types package vs packages/shared's version — the base must DISAGREE (the
     instrument fires: the seat claims 15 of 27) and head / END must AGREE (0 of 27). NESTED copies (a non-top-level key) are counted separately:
     the seat's cell cannot see them; they are reported, not refused.
  L7 IMAGE REACH of the moved locks (a git read): every Dockerfile that COPIES a moved lock's directory `package*.json` / `package-lock.json`,
     and whether its final stage omits dev; the root lock's PRODUCTION move names the Dockerfiles that copy the ROOT lock (expected 0) with a
     CONTROL (the analytics Dockerfile's own COPY is found).
rc 0 LOCKDELTA PASS / rc 1 FAIL. --head <commit> (controls): judge a plant instead of the merge commit (BASE = its first parent).
Usage: lockdelta_gate49b.py <scratchpad> [--pins <name>] [--offline] [--head <commit>]"""
import json, os, re, subprocess, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; OFF = '--offline' in A
PF = 'pins_gate49b.SIM-%s.json' % A[A.index('--pins') + 1] if '--pins' in A else 'pins_gate49b.json'
P = json.load(open(os.path.join(G, PF), encoding='utf-8'))
CL = os.path.join(SP, 'g49b_sp', 'clone'); AU = K['post_merge_audit']; N = AU['pr']
HEAD = A[A.index('--head') + 1] if '--head' in A else AU['merge_commit']
HEAD = subprocess.run(['git', '-C', CL, 'rev-parse', HEAD + '^{commit}'], capture_output=True, text=True).stdout.strip()
BASE = subprocess.run(['git', '-C', CL, 'rev-parse', HEAD + '^1'], capture_output=True, text=True).stdout.strip()
DEV = P['develop']; PRH = AU['head']; END = P['end_tree']; FILES = sorted(AU['files']); CLAIM = AU['claimed']
PKGS = K['types_packages']; SHL = K['shared_lock']
FLAGS = ('dev', 'devOptional', 'optional', 'peer')
res = []
def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode not in ok: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a[:4]), r.returncode, r.stderr.strip()[:300]))
    return r.stdout
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
def J(t, p): return json.loads(git('show', '%s:%s' % (t, p)))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('lockdelta_gate49b %s | #%s | %d locks at base %s and head %s | develop %s | END %s | pins %s%s' % (now, N, len(FILES), BASE[:12], HEAD[:12], DEV[:12], (END or '')[:12], PF, ' (OFFLINE: L5 not measured)' if OFF else ''))
# ---- semver (npm semantics for plain x.y.z; copied from gate49a's lockdelta, same fixed cases) ----
def pv(s):
    m = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+.*)?', s.strip()); return (int(m[1]), int(m[2]), int(m[3]), m[4]) if m else None
def xr(s):
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
    if not re.fullmatch(r'[\s\d.xX*^~<>=|v-]*', rng or ''): return None
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
CASES = [('4.19.9', '^4.17.33', True), ('5.0.0', '^4.17.33', False), ('8.23.1', '*', True), ('8.23.1', '^8.10.2', True), ('9.0.0', '^8.10.2', False),
         ('4.19.9', '~4.19.8', True), ('4.20.0', '~4.19.8', False), ('0.2.5', '^0.2.3', True), ('0.3.0', '^0.2.3', False), ('8.23.1-rc.1', '^8.10.2', False)]
cfail = [c for c in CASES if sat(c[0], c[1]) != c[2]]
chk('L4s', not cfail, 'the semver evaluator holds on %d fixed cases: failures %s' % (len(CASES), cfail or 'none'))
def parent(base):
    i = base.rfind('/node_modules/')
    return base[:i] if i >= 0 else ''
def resolve(pk, frm, name):
    base = frm
    while True:
        key = (base + '/node_modules/' + name) if base else 'node_modules/' + name
        if key in pk: return key
        if not base: return None
        base = parent(base) if '/node_modules/' in base else ''
def nameof(key): return key.rsplit('node_modules/', 1)[-1]
def fl(e): return ','.join(f for f in FLAGS if e.get(f)) or 'PROD'
# ---- L0 ----
names = sorted(x for x in git('diff', '--name-only', BASE, HEAD).split('\n') if x)
ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in git('diff', '--numstat', BASE, HEAD).splitlines()}
sa, sd = sum(int(a) for a, d in ns.values()), sum(int(d) for a, d in ns.values())
chk('L0', names == FILES and all(p.endswith('/package-lock.json') for p in names), 'changed paths %d == the kit\'s 15 locks: %s | extra %s | missing %s | manifests %d | non-lock %d' % (
    len(names), names == FILES, sorted(set(names) - set(FILES)) or 'none', sorted(set(FILES) - set(names)) or 'none', sum(1 for p in names if p.endswith('package.json')), sum(1 for p in names if not p.endswith('package-lock.json'))))
print('    numstat sum +%d/-%d | the seat claimed %s: CLAIM %s' % (sa, sd, CLAIM['numstat'], 'MATCH' if '+%d/-%d' % (sa, sd) == CLAIM['numstat'] else 'DIFFERS'))
for p in names:
    if ns[p][0] != ns[p][1]: print('    numstat NOTE %s +%s/-%s (not symmetric: see L2 INFO for fields ABSENT at base)' % (p, ns[p][0], ns[p][1]))
# ---- target versions from packages/shared ----
SH = J(BASE, SHL)['packages']; TGT = {pk: (SH.get('node_modules/' + pk) or {}).get('version') for pk in PKGS}
SHH = J(HEAD, SHL)['packages']; TGTH = {pk: (SHH.get('node_modules/' + pk) or {}).get('version') for pk in PKGS}
chk('L3t', TGT == TGTH and all(TGT.values()) and TGT == CLAIM['targets'], 'packages/shared targets at base %s == at head %s == the claim %s' % (TGT, TGTH, CLAIM['targets']))
MOVES = []; ABSENTB = []
for p in FILES:
    b, h = J(BASE, p), J(HEAD, p); bp, hp = b['packages'], h['packages']
    tk = sorted(set(b) | set(h)); same_top = all(b.get(k) == h.get(k) for k in tk if k != 'packages')
    add, rem = sorted(set(hp) - set(bp)), sorted(set(bp) - set(hp))
    chk('L1 ' + p.replace('Blockchain/Dev/', ''), same_top and bp.get('') == hp.get('') and not add and not rem, 'top-level keys (but packages) equal %s | root "" entry equal %s | entries %d -> %d | ADDED %d REMOVED %d' % (
        same_top, bp.get('') == hp.get(''), len(bp), len(hp), len(add), len(rem)))
    for k in sorted(bp):
        if k in hp and bp[k] != hp[k]:
            diff = sorted(x for x in set(bp[k]) | set(hp[k]) if bp[k].get(x) != hp[k].get(x))
            ok = nameof(k) in PKGS and set(diff) <= {'version', 'resolved', 'integrity'} and all(bool(bp[k].get(f)) == bool(hp[k].get(f)) for f in FLAGS)
            MOVES.append(dict(lock=p, key=k, pkg=nameof(k), frm=bp[k].get('version'), to=hp[k].get('version'), flag=fl(hp[k]), fields=diff, ok=ok,
                              top=(k == 'node_modules/' + nameof(k)), absent_at_base=[x for x in ('resolved', 'integrity') if x not in bp[k] and x in hp[k]]))
            if bp[k].get('resolved') is None or bp[k].get('integrity') is None: ABSENTB.append('%s %s' % (p.replace('Blockchain/Dev/', ''), k))
bad2 = [m for m in MOVES if not m['ok']]
chk('L2', not bad2, '%d changed entr(y/ies); every one an %s entry, fields within {version, resolved, integrity}, no flag flipped: %s' % (len(MOVES), '/'.join(PKGS), 'yes' if not bad2 else 'NO: %s' % [(m['lock'], m['key'], m['fields']) for m in bad2]))
print('    INFO L2 entries whose resolved / integrity were ABSENT at base and PRESENT at head: %d %s' % (len(ABSENTB), ABSENTB or ''))
print('    MOVE TABLE (lock · key · from -> to · flag):')
for m in MOVES: print('      %s · %s · %s -> %s · %s' % (m['lock'].replace('Blockchain/Dev/', ''), m['key'], m['frm'], m['to'], m['flag']))
inmaj = all(pv(m['frm']) and pv(m['to']) and pv(m['frm'])[0] == pv(m['to'])[0] for m in MOVES)
totgt = all(m['to'] == TGT.get(m['pkg']) for m in MOVES)
chk('L3', len(MOVES) == CLAIM['moves'] and inmaj and totgt, '%d moves (claimed %d) | every move inside its major: %s | every to-version == packages/shared\'s: %s | top-level %d, nested %d' % (
    len(MOVES), CLAIM['moves'], inmaj, totgt, sum(m['top'] for m in MOVES), sum(not m['top'] for m in MOVES)))
PROD = [m for m in MOVES if m['flag'] == 'PROD']
print('    PRODUCTION moves (no dev / devOptional / optional flag): %d %s' % (len(PROD), ['%s %s %s->%s' % (m['lock'].replace('Blockchain/Dev/', ''), m['key'], m['frm'], m['to']) for m in PROD] or ''))
print('    devOptional moves: %s' % (['%s %s' % (m['lock'].replace('Blockchain/Dev/', ''), m['key']) for m in MOVES if 'devOptional' in m['flag']] or 'none'))
# ---- L4 ----
ND = 0; NBAD = 0; NCTL = 0
for m in MOVES:
    pk = J(HEAD, m['lock'])['packages']
    for dk, de in pk.items():
        for sec in ('dependencies', 'optionalDependencies', 'peerDependencies') + (('devDependencies',) if ('node_modules/' not in dk) else ()):
            rng = (de.get(sec) or {}).get(m['pkg'])
            if rng is None or resolve(pk, dk, m['pkg']) != m['key']: continue
            s = sat(m['to'], rng); ND += 1
            if s is not True: NBAD += 1; print('    L4 NOT SATISFIED %s: %s %s %s needs %r, head %s (%s)' % (m['lock'].replace('Blockchain/Dev/', ''), dk or '(root)', sec, m['pkg'], rng, m['to'], s))
            ctl = '%d.0.0' % (pv(m['to'])[0] + 1)
            if sat(ctl, rng) is not True: NCTL += 1
chk('L4', ND > 0 and NBAD == 0 and NCTL == ND, '%d dependant range(s) of the moved entries, all satisfied by the head version: %s | CONTROL <major+1>.0.0 refused by %d of %d' % (ND, NBAD == 0, NCTL, ND))
# ---- L5 ----
if not OFF:
    for pkg in PKGS:
        for tv in sorted(set(m['to'] for m in MOVES if m['pkg'] == pkg)):
            ents = [J(HEAD, m['lock'])['packages'][m['key']] for m in MOVES if m['pkg'] == pkg and m['to'] == tv]
            rt = json.load(urllib.request.urlopen('https://registry.npmjs.org/%s/%s' % (pkg.replace('/', '%2F'), tv), timeout=60))['dist']
            eq = all(e.get('resolved') == rt['tarball'] and e.get('integrity') == rt['integrity'] for e in ents)
            chk('L5 %s@%s' % (pkg, tv), bool(ents) and eq, '%d head entr(y/ies) resolved/integrity == registry dist (%s, %s…)' % (len(ents), rt['tarball'], rt['integrity'][:24]))
            fvs = sorted(set(m['frm'] for m in MOVES if m['pkg'] == pkg)); c1 = []
            for fv in fvs:
                rf = json.load(urllib.request.urlopen('https://registry.npmjs.org/%s/%s' % (pkg.replace('/', '%2F'), fv), timeout=60))['dist']; c1.append(rf['integrity'] == rt['integrity'])
            i = rt['integrity']; flip = i[:13] + ('A' if i[13] != 'A' else 'B') + i[14:]
            chk('L5c %s@%s' % (pkg, tv), not any(c1) and flip != rt['integrity'], 'CONTROLS: the from-version(s) %s integrity == the to-version\'s: %s; one flipped character compares equal: %s (all must be False)' % (fvs, c1, flip == rt['integrity']))
else: print('NOT MEASURED L5: --offline')
# ---- L6 ----
def agree(tree, label):
    locks = [l for l in git('ls-tree', '-r', '--name-only', tree, '--', 'Blockchain/Dev').splitlines() if l.endswith('/package-lock.json') and l != SHL]
    ref = {pk: (J(tree, SHL)['packages'].get('node_modules/' + pk) or {}).get('version') for pk in PKGS}
    checked = 0; top = []; nested = []
    for l in locks:
        try: pk = J(tree, l)['packages']
        except Exception: continue
        if not any(('node_modules/' + x) in pk for x in PKGS): continue
        checked += 1
        for x in PKGS:
            v = (pk.get('node_modules/' + x) or {}).get('version')
            if v is not None and v != ref[x]: top.append('%s: %s %s != %s' % (l.replace('Blockchain/Dev/', ''), x, v, ref[x]))
            for k, e in pk.items():
                if k.endswith('/node_modules/' + x) and e.get('version') != ref[x]: nested.append('%s: %s %s != %s' % (l.replace('Blockchain/Dev/', ''), k, e.get('version'), ref[x]))
    dl = sorted(set(t.split(':')[0] for t in top))
    print('    L6 %s %s: %d lock(s) carry a top-level types package (of %d locks) | ref %s | TOP-LEVEL disagreeing lock(s) %d | nested disagreeing copies %d' % (label, tree[:12], checked, len(locks), ref, len(dl), len(nested)))
    for t in top: print('       top  %s' % t)
    for t in nested: print('       NESTED %s' % t)
    return checked, dl, nested
cb, db, nb = agree(BASE, 'base'); cd, dd, ndv = agree(DEV, 'develop'); ch, dh, nh = agree(HEAD, 'head'); ce, de_, ne = agree(END, 'END') if END else (0, ['n/a'], [])
chk('L6', cb > 0 and len(db) > 0 and not dd and not dh and not de_ and ch == cb == ce, 'base: %d of %d disagree (the instrument fires; the seat claims 15 of 27) | develop as read now: %d disagree (want 0: it contains the merge), set %s | head: %d of %d | END: %d of %d | the seat\'s cell reads top-level only; nested disagreeing copies base %d / head %d / END %d (reported)' % (
    len(db), cb, len(dd), dd == db, len(dh), ch, len(de_), ce, len(nb), len(nh), len(ne)))
print('    L6 base disagreeing set == the 15 changed locks: %s' % (sorted('Blockchain/Dev/' + x for x in db) == FILES))
# ---- L8 (post-merge) ----
l8 = [p for p in FILES if git('rev-parse', '%s:%s' % (HEAD, p)).strip() != git('rev-parse', '%s:%s' % (PRH, p)).strip()]
chk('L8', not l8, 'every one of the 15 landed blobs at the merge %s == #%s\'s PR head %s blob: %s | CONTROL the base blob differs from the head for %d of 15' % (
    HEAD[:12], N, PRH[:12], 'yes' if not l8 else 'NO: %s' % l8, sum(1 for p in FILES if git('rev-parse', '%s:%s' % (BASE, p)).strip() != git('rev-parse', '%s:%s' % (PRH, p)).strip())))
# ---- L7 ----
dfs = [l for l in git('ls-tree', '-r', '--name-only', HEAD, '--', 'Blockchain/Dev').splitlines() if os.path.basename(l).startswith('Dockerfile')]
reach = {}; rootc = []; ctl = False
for d in dfs:
    t = git('show', '%s:%s' % (HEAD, d))
    for line in t.splitlines():
        s = line.strip()
        if not s.upper().startswith('COPY') or '--from' in s: continue
        for p in FILES:
            dd = os.path.dirname(p).replace('Blockchain/Dev/', '')
            if dd == 'Blockchain/Dev': dd = ''
            if dd and re.search(r'(^|\s)%s/package(\*|-lock)?\.?json|(^|\s)%s/package\*\.json' % (re.escape(dd), re.escape(dd)), s): reach.setdefault(p, set()).add(d)
        if re.search(r'COPY\s+(\./)?package(\*|-lock)\.?json', s, re.I) and 'Blockchain/Dev/Dockerfile' not in d: rootc.append('%s: %s' % (d, s[:90]))
        if d.endswith('services/analytics/Dockerfile') and 'services/analytics/package' in s: ctl = True
for p in FILES: print('    L7 %s -> %s' % (p.replace('Blockchain/Dev/', ''), sorted(reach.get(p, [])) or 'no Dockerfile copies it'))
print('    L7 ROOT-lock copies (a COPY of package*.json / package-lock.json at the context root): %d %s | CONTROL analytics Dockerfile COPY found: %s' % (len(rootc), rootc[:4] or '', ctl))
chk('L7', ctl, 'the COPY instrument fires on the analytics Dockerfile (the control); %d of 15 moved locks are copied by a Dockerfile' % sum(1 for p in FILES if reach.get(p)))
nf = res.count(False)
print('LOCKDELTA %s: %d FAIL of %d checks | %d moves (%d PROD), %d locks, base %d / head %d disagreeing, nested base %d / head %d' % (
    'PASS' if nf == 0 else 'FAIL', nf, len(res), len(MOVES), len(PROD), len(FILES), len(db), len(dh), len(nb), len(nh)))
raise SystemExit(1 if nf else 0)
