#!/usr/bin/env python3
"""c2_lockdiff_gateD2.py — gateD2 C2 LOCKS: the root lock and the timestamping service lock, diffed ENTRY BY ENTRY and FIELD BY FIELD as
parsed JSON plus a text-hunk containment test, base blob vs head blob, from SHAs with read-only git verbs (a NEW instrument on gate54f's
c2_lockdiff shape; the allowed delta here is a REMOVE + a closure ADD, not a version bump).
Per lock (kit.json `locks`):
  L1 entries: REMOVED == kit removed (node-forge, @types/node-forge) exactly; ADDED keys == kit added keys exactly (root 5, service 7);
     CHANGED (present at both, unequal) == [kit changed_entry] exactly; every top-level key other than `packages` equal.
  L2 the changed (workspace) entry: only kit changed_entry_fields differ; its dependencies / devDependencies delta == kit manifest_delta
     (- node-forge, + pkijs 3.4.1, + asn1js 3.0.10; - @types/node-forge) and NOTHING else in either map moved.
  L3 each added entry: version == kit; resolved == the registry tarball URL for that name@version; integrity present (sha512-); no
     dev / optional / devOptional / peer flag (prod); license present. (Integrity is RECOMPUTED from the tarball by c2_integrity_gateD2.py.)
  L4 collateral over every entry present at BOTH: flag flips (dev/optional/devOptional/peer, including a field DROPPED) 0; version movement 0;
     libc: count of entries carrying `libc` base == head == kit libc_base, every libc array value-equal.
  L5 manifest agreement at head: services/timestamping/package.json dependencies / devDependencies == this lock's workspace entry.
  L6 text: cut every removed entry's block out of the base text and every added entry's block out of the head text (and the workspace
     entry's block from both): the two residues must be line-identical (trailing commas normalised) — nothing outside those blocks moved.
     A value-equal entry whose FIELD ORDER moved (same lines, other order) is cut too, PASSES L6, and is printed `INFO L6-REORDER` for the gate.
Verdict `LOCKDIFF PASS|FAIL: <n> FAIL of <m> | base <sha12> head <sha12>` + one `ENTRIES <lock> removed r added a changed c flips f libc b->h
versions v` line per lock.
--selftest  plants built IN MEMORY from the base blob and the kit's drafted first commit's blob (no repo write):
  T0 base vs base -> FAIL (0 removed)            T1 the drafted head -> PASS         T2 + a `"dev": true` on another entry -> FAIL (flips 1)
  T3 service: one libc array removed -> FAIL (libc 10 -> 9)   T4 an unrelated version moved -> FAIL (L1 changed 2, versions 1)
  T5 an extra added entry -> FAIL (L1)            T6 node-forge left in -> FAIL (L1 removed)   T7 an unrelated entry's `dev` DROPPED -> FAIL
  T8 pkijs 3.4.0 -> FAIL (L3)    (T1 also asserts the root lock's ONE value-equal reorder, http-cache-semantics, is named)
  rc 0 only if EVERY arm returns its expected verdict AND names the expected collateral.
Usage: c2_lockdiff_gateD2.py --repo <clone> --base <sha> --head <sha>  |  --repo <clone> --selftest   (rc 0 PASS / 1 FAIL / 2 usage)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, commit, show, find_member, member_span, opcodes, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); FL = K['flag_fields']; MAN = K['service'] + '/package.json'


def tarball(name, v):
    return '%s%s/-/%s-%s.tgz' % (K['registry'], name, name.split('/')[-1], v)


def spans(text, keys):
    ls = text.split('\n'); out = []
    for k in keys:
        i = find_member(ls, k) if k else next((j for j, l in enumerate(ls) if l.strip() == '"": {'), None)
        if i is not None:
            s = member_span(ls, i)
            if s: out.append(s)
    return out


def check_lock(C, path, bt, ht, man):
    cfg = K['locks'][path]; lb, lh = json.loads(bt), json.loads(ht); pb, ph = lb['packages'], lh['packages']
    add = sorted(set(ph) - set(pb)); rem = sorted(set(pb) - set(ph)); both = set(pb) & set(ph)
    chg = sorted(k for k in both if pb[k] != ph[k]); tk = sorted(k for k in set(lb) | set(lh) if k != 'packages' and lb.get(k) != lh.get(k))
    tag = path.replace('Blockchain/Dev/', '')
    C.chk('L1 %s entries' % tag, rem == sorted(cfg['removed']) and add == sorted(cfg['added']) and chg == [cfg['changed_entry']] and not tk,
          'REMOVED %s (want %s) | ADDED %s (want %s) | CHANGED %s (want [%r]) | top-level keys differing %s' % (rem, sorted(cfg['removed']), add, sorted(cfg['added']), chg[:6], cfg['changed_entry'], tk or 'NONE'))
    eb, eh = pb.get(cfg['changed_entry'], {}), ph.get(cfg['changed_entry'], {})
    fchg = sorted(f for f in set(eb) | set(eh) if eb.get(f) != eh.get(f)); okd = True; why = []
    for fld, d in K['manifest_delta'].items():
        b, h = dict(eb.get(fld) or {}), dict(eh.get(fld) or {})
        want = {k: v for k, v in b.items() if k not in d['remove']}; want.update(d['add'])
        if h != want: okd = False; why.append('%s: got -%s +%s' % (fld, sorted(set(b) - set(h)), sorted((k, h[k]) for k in set(h) - set(b))))
    C.chk('L2 %s workspace entry %r' % (tag, cfg['changed_entry']), set(fchg) <= set(cfg['changed_entry_fields']) and okd,
          'fields changed %s (allowed %s) | dependency delta == kit manifest_delta: %s %s' % (fchg, cfg['changed_entry_fields'], okd, why))
    bad3 = []
    for k, v in sorted(cfg['added'].items()):
        e = ph.get(k) or {}; nm = k.split('node_modules/', 1)[-1]
        prob = [x for x, ok in (('version %s' % e.get('version'), e.get('version') == v), ('resolved %s' % e.get('resolved'), e.get('resolved') == tarball(nm, v)),
                                ('integrity', str(e.get('integrity', '')).startswith('sha512-')), ('flags %s' % [f for f in FL if e.get(f)], not any(e.get(f) for f in FL)),
                                ('license', bool(e.get('license')))) if not ok]
        if prob: bad3.append((k, prob))
    C.chk('L3 %s added entries' % tag, not bad3 and len(cfg['added']) == len([k for k in cfg['added'] if k in ph]), '%d added entries | problems %s' % (len(cfg['added']), bad3 or 'NONE'))
    flips = sorted(k for k in both if any(pb[k].get(f) != ph[k].get(f) for f in FL))
    vers = sorted(k for k in both if pb[k].get('version') != ph[k].get('version'))
    lcb = sorted(k for k in pb if 'libc' in pb[k]); lch = sorted(k for k in ph if 'libc' in ph[k])
    lneq = sorted(k for k in set(lcb) | set(lch) if pb.get(k, {}).get('libc') != ph.get(k, {}).get('libc'))
    C.chk('L4 %s collateral' % tag, not flips and not vers and len(lcb) == len(lch) == cfg['libc_base'] and not lneq,
          'flag flips/drops (%s) %d %s | version movement %d %s | libc entries %d -> %d (kit %d) | libc arrays unequal %d %s' % (
              '/'.join(FL), len(flips), flips[:3], len(vers), vers[:3], len(lcb), len(lch), cfg['libc_base'], len(lneq), lneq[:3]))
    if man is not None:
        mj = json.loads(man); mm = {f: mj.get(f) or {} for f in ('dependencies', 'devDependencies')}
        lm = {f: eh.get(f) or {} for f in ('dependencies', 'devDependencies')}
        C.chk('L5 %s == manifest' % tag, mm == lm, 'head %s dependencies/devDependencies == the lock\'s workspace entry: %s%s' % (
            MAN.split('/')[-2] + '/package.json', mm == lm, '' if mm == lm else ' | differ %s' % sorted(set(mm['dependencies'].items()) ^ set(lm['dependencies'].items()))[:4]))
    def index(text):   # key -> (start, end) of every packages member, one pass
        ls = text.split('\n'); out = {}
        for j, l in enumerate(ls):
            m = re.match(r'^    "([^"]*)": \{$', l)
            if m:
                sp = member_span(ls, j)
                if sp: out[m.group(1)] = sp
        return ls, out
    lsb, ib = index(bt); lsh, ih = index(ht)
    norm = lambda L, sp: [x.rstrip().rstrip(',') for x in L[sp[0]:sp[1] + 1]]
    reord = sorted(k for k in both if pb[k] == ph[k] and k in ib and k in ih and norm(lsb, ib[k]) != norm(lsh, ih[k]))
    reord_ok = all(sorted(norm(lsb, ib[k])) == sorted(norm(lsh, ih[k])) for k in reord)
    def residue(L, I, keys):   # the text with every named member block cut out, trailing commas normalised
        cut = set()
        for k in keys:
            if k in I: cut.update(range(I[k][0], I[k][1] + 1))
        return [l.rstrip().rstrip(',') for j, l in enumerate(L) if j not in cut]
    rb = residue(lsb, ib, cfg['removed'] + [cfg['changed_entry']] + reord); rh = residue(lsh, ih, list(cfg['added']) + [cfg['changed_entry']] + reord)
    ops = opcodes(bt, ht); res = opcodes('\n'.join(rb), '\n'.join(rh))
    C.chk('L6 %s text' % tag, bool(ops) and not res and reord_ok, '%d hunk(s), -%d/+%d line(s) | with the removed / added / workspace blocks cut out (and %d value-equal REORDERED block(s)), residues (%d / %d lines) differ in %d hunk(s) %s' % (
        len(ops), sum(o[2] - o[1] for o in ops), sum(o[4] - o[3] for o in ops), len(reord), len(rb), len(rh), len(res), [(o[0], o[1] + 1, rb[o[1]][:60] if o[1] < len(rb) else '', rh[o[3]][:60] if o[3] < len(rh) else '') for o in res[:3]]))
    for k in reord:
        print('INFO L6-REORDER %s %s: value-equal, same lines, FIELD ORDER differs | base %s | head %s  <- not an allowed add/remove: the gate rules (README D4)' % (
            tag, k, [x.split(':')[0].strip() for x in norm(lsb, ib[k])[1:-1]], [x.split(':')[0].strip() for x in norm(lsh, ih[k])[1:-1]]))
    return {'removed': len(rem), 'added': len(add), 'changed': len(chg), 'flips': len(flips), 'versions': len(vers), 'libc': (len(lcb), len(lch)), 'reorders': len(reord)}


def run(pairs, man):
    C = Checks(); facts = {}
    for path in sorted(K['locks']):
        bt, ht = pairs[path]
        if bt is None or ht is None:
            C.chk('L0 %s present' % path, False, 'blob missing at base %s / head %s' % (bt is None, ht is None)); continue
        facts[path] = check_lock(C, path, bt, ht, man)
    return C, facts


def lines_of(text): return text.split('\n')


def plant_devflip(text):
    ls = lines_of(text); d = json.loads(text)['packages']
    k = next(k for k in sorted(d) if k.startswith('node_modules/') and not any(d[k].get(f) for f in FL) and 'version' in d[k] and k not in sum([list(c['added']) for c in K['locks'].values()], []))
    i = find_member(ls, k); vi = next(j for j in range(i, i + 6) if ls[j].strip().startswith('"version":'))
    ind = ls[vi][:len(ls[vi]) - len(ls[vi].lstrip())]; ls[vi + 1:vi + 1] = ['%s"dev": true,' % ind]
    return '\n'.join(ls), k


def plant_devdrop(text):
    ls = lines_of(text); d = json.loads(text)['packages']
    k = next(k for k in sorted(d) if k.startswith('node_modules/') and d[k].get('dev') is True)
    a, b = member_span(ls, find_member(ls, k)); j = next(j for j in range(a, b + 1) if ls[j].strip().startswith('"dev": true'))
    if not ls[j].rstrip().endswith(','): ls[j - 1] = ls[j - 1].rstrip().rstrip(',')
    del ls[j]; return '\n'.join(ls), k


def plant_libc(text):
    ls = lines_of(text); st = [j for j, l in enumerate(ls) if l.strip() == '"libc": [']
    if not st: return None
    a, b = member_span(ls, st[0])
    if not ls[b].rstrip().endswith(','): ls[a - 1] = ls[a - 1].rstrip().rstrip(',')
    del ls[a:b + 1]; return '\n'.join(ls)


def plant_version(text, key=None, to=None):
    ls = lines_of(text); d = json.loads(text)['packages']
    k = key or next(k for k in sorted(d) if k.startswith('node_modules/') and 'version' in d[k] and k not in sum([list(c['added']) for c in K['locks'].values()], []))
    a, b = member_span(ls, find_member(ls, k)); j = next(j for j in range(a, b + 1) if ls[j].strip().startswith('"version":'))
    ls[j] = re.sub(r'"version": "[^"]+"', '"version": "%s"' % (to or '0.0.0-gD2plant'), ls[j]); return '\n'.join(ls), k


def plant_added(text):
    ls = lines_of(text); i = find_member(ls, 'node_modules/pkijs'); ind = ls[i][:len(ls[i]) - len(ls[i].lstrip())]
    ls[i:i] = ['%s"node_modules/zz-gated2-planted": {' % ind, '%s  "version": "0.0.1"' % ind, '%s},' % ind]; return '\n'.join(ls)


def plant_keep_forge(base, head):
    bl = lines_of(base); a, b = member_span(bl, find_member(bl, 'node_modules/node-forge')); blk = bl[a:b + 1]
    if not blk[-1].rstrip().endswith(','): blk[-1] = blk[-1] + ','
    hl = lines_of(head); i = find_member(hl, 'node_modules/pkijs'); hl[i:i] = blk; return '\n'.join(hl)


if '--selftest' in A:
    B = commit(REPO, K['base']); H = commit(REPO, K['drafted_first_commit'])
    print('c2_lockdiff_gateD2 SELFTEST %s | repo %s | base %s | drafted head %s (plants in memory; nothing written)' % (now(), REPO, B[:12], H[:12]))
    base = {p: show(REPO, B, p) for p in K['locks']}; head = {p: show(REPO, H, p) for p in K['locks']}; man = show(REPO, H, MAN)
    ROOT, SVC = 'Blockchain/Dev/package-lock.json', K['service'] + '/package-lock.json'
    arms = []
    def arm(name, hd, want_pass, expect):
        print('\n=== ARM %s (expected %s) ===' % (name, 'PASS' if want_pass else 'FAIL'))
        C, f = run({p: (base[p], hd[p]) for p in base}, man); got = C.nfail() == 0; ok = expect(f)
        for p in sorted(f): print('  ENTRIES %s removed %d added %d changed %d flips %d libc %d->%d versions %d' % (p, f[p]['removed'], f[p]['added'], f[p]['changed'], f[p]['flips'], f[p]['libc'][0], f[p]['libc'][1], f[p]['versions']))
        print('ARM %s: verdict %s (expected %s) | named collateral %s -> %s' % (name, 'PASS' if got else 'FAIL', 'PASS' if want_pass else 'FAIL', 'as expected' if ok else 'NOT as expected', 'OK' if (got == want_pass and ok) else 'MISMATCH'))
        arms.append(got == want_pass and ok)
    arm('T0 base-vs-base', dict(base), False, lambda f: all(f[p]['removed'] == 0 for p in f))
    arm('T1 drafted head', dict(head), True, lambda f: f[ROOT]['added'] == 5 and f[SVC]['added'] == 7 and all(f[p]['removed'] == 2 for p in f) and f[ROOT]['reorders'] == 1 and f[SVC]['reorders'] == 0)
    T2 = {}; who = {}
    for p in head: T2[p], who[p] = plant_devflip(head[p])
    print('\n(T2 plants "dev": true on %s)' % json.dumps(who))
    arm('T2 + a dev flip', T2, False, lambda f: all(f[p]['flips'] == 1 for p in f))
    T3 = dict(head); T3[SVC] = plant_libc(head[SVC])
    arm('T3 service libc removed', T3, False, lambda f: f[SVC]['libc'] == (10, 9) and f[ROOT]['libc'] == (0, 0))
    T4 = {}; vk = {}
    for p in head: T4[p], vk[p] = plant_version(head[p])
    print('\n(T4 moves the version of %s)' % json.dumps(vk))
    arm('T4 an unrelated version moved', T4, False, lambda f: all(f[p]['versions'] == 1 and f[p]['changed'] == 2 for p in f))
    arm('T5 an extra added entry', {p: plant_added(head[p]) for p in head}, False, lambda f: f[ROOT]['added'] == 6 and f[SVC]['added'] == 8)
    arm('T6 node-forge left in', {p: plant_keep_forge(base[p], head[p]) for p in head}, False, lambda f: all(f[p]['removed'] == 1 for p in f))
    T7 = {}; dk = {}
    for p in head: T7[p], dk[p] = plant_devdrop(head[p])
    print('\n(T7 drops `"dev": true` from %s)' % json.dumps(dk))
    arm('T7 a dev field DROPPED', T7, False, lambda f: all(f[p]['flips'] == 1 for p in f))
    arm('T8 pkijs 3.4.0', {p: plant_version(head[p], 'node_modules/pkijs', '3.4.0')[0] for p in head}, False, lambda f: all(f[p]['versions'] == 0 for p in f))
    n = arms.count(False)
    print('\nSELFTEST %s: %d of %d arms returned their expected verdict and collateral' % ('OK' if n == 0 else 'MISMATCH', len(arms) - n, len(arms)))
    raise SystemExit(1 if n else 0)

B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head') or sys.exit('--head <sha> is required (or --selftest)'))
print('c2_lockdiff_gateD2 %s | repo %s | base %s | head %s' % (now(), REPO, B, H))
C, f = run({p: (show(REPO, B, p), show(REPO, H, p)) for p in K['locks']}, show(REPO, H, MAN))
n = C.nfail()
print('LOCKDIFF %s: %d FAIL of %d checks | base %s head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), B[:12], H[:12]))
for p in sorted(f): print('ENTRIES %s removed %d added %d changed %d flips %d libc %d->%d versions %d' % (p, f[p]['removed'], f[p]['added'], f[p]['changed'], f[p]['flips'], f[p]['libc'][0], f[p]['libc'][1], f[p]['versions']))
raise SystemExit(1 if n else 0)
