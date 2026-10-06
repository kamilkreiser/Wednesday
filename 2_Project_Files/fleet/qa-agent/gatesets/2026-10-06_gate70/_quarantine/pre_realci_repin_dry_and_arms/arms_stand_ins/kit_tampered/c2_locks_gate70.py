#!/usr/bin/env python3
"""c2_locks_gate70.py — the LOCK instruments for #1397 (KS-1425). Read verbs only; the plan is derived from the BASE, never from the head.

  diff    --repo R --head H [--base B] [--integrity-json F] [--json-out F]
          THE PLAN (from the base alone): every entry, in every IN-SCOPE lock, of the four packages at the old version
          (proxy-addr 2.0.7, source-map-js 1.2.1, postcss-selector-parser 7.1.4 (7.x only), smol-toml 1.8.0).
          L1  changed path set == the planned lock set (36) + the baseline; mobile untouched
          L2  per lock: top-level keys / order / values equal except `packages`; `packages` key SET and ORDER equal (0 added, 0 removed)
          L3  per entry: changed entries == the plan EXACTLY; each: version old->new; the changed fields == {version} + whichever of
              {resolved, integrity} the entry ALREADY HAS (D1: only the fields present); field set and field order unchanged;
              every other field equal; resolved == the registry tarball URL of the new version
          L4  integrity: ONE value per new version across all its entries; == --integrity-json (c3's tarball-derived sri) when given
          L5  counts: entries 54, field writes 158, version-only entries 2 (all in the root lock), per package 16/33/1/4
          L6  indent: detected PER FILE, base indent == head indent, BOTH round-trip byte-exact (no file reformatted); census of
              indent 2 / 4 over every tracked lock at the head
          W1  parent walk at the HEAD (lib resolve_path, npm's nearest node_modules): every changed entry has >= 1 parent, and EVERY
              parent's declared range admits the new version (lib satisfies — independent of the repo's semver). 0 orphans.
          W2  the parent declarations are identical at base and head (the refresh moved no range)
          W3  LIVE NEGATIVE CONTROL: the untouched postcss-selector-parser 6.1.4 entries' parents must NOT admit 7.1.6 (the walk can say no)
  parse   --repo R --rev REV | --dir D   in-scope locks only: per package, entries inside the advisory's vulnerable range;
          postcss-selector-parser split 6.x / 7.x. --expect-clean asserts 0 vulnerable for the 3 fixed ids and 0 psp 7.x < 7.1.6.
          Also: the mobile lock is read and REPORTED (it must still show source-map-js 1.2.1 — the parser can see what scope excludes).
  --selftest   synthetic locks: an added entry, a removed entry, a 4th field, a reordered field, a resolved ADDED to a version-only
               entry, a wrong version, a reindented file, an out-of-range parent, an orphan — each must FAIL.
rc 0 / 1."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate70 import K, Tally, git, git_bytes, tracked_locks, in_scope, roundtrip_exact, detect_indent, pkg_name, parents_of, satisfies, _parse

PLAN = K['plan']


def is_old(name, ver):
    p = PLAN.get(name)
    return bool(p) and ver == p['old']


def tarball_url(name, ver):
    return 'https://registry.npmjs.org/%s/-/%s-%s.tgz' % (name, name.split('/')[-1], ver)


def entry_findings(path, be, he):
    """[] if the head entry is exactly the planned rewrite of the base entry."""
    name = pkg_name(path); p = PLAN[name]; f = []
    if be.get('version') != p['old']: f.append('base version %s != plan old %s' % (be.get('version'), p['old']))
    if he.get('version') != p['new']: f.append('head version %s != plan new %s' % (he.get('version'), p['new']))
    if list(be) != list(he): f.append('field set/order changed %s -> %s' % (list(be), list(he)))
    allowed = {'version'} | ({'resolved', 'integrity'} & set(be))
    changed = {k for k in set(be) | set(he) if be.get(k) != he.get(k)}
    if changed != allowed: f.append('changed fields %s != allowed %s' % (sorted(changed), sorted(allowed)))
    if 'resolved' in he and he['resolved'] != tarball_url(name, p['new']): f.append('resolved %s' % he['resolved'])
    return f, len(changed)


def lock_diff(lock, braw, hraw, plan_paths):
    """per-lock findings, the changed entries, field writes, version-only count, indents."""
    f = []; b = json.loads(braw); h = json.loads(hraw)
    if [k for k in b if k != 'packages'] != [k for k in h if k != 'packages'] or any(b[k] != h[k] for k in b if k != 'packages'):
        f.append('top-level keys/values outside `packages` changed')
    bp, hp = b.get('packages', {}), h.get('packages', {})
    added, removed = sorted(set(hp) - set(bp)), sorted(set(bp) - set(hp))
    if added or removed: f.append('entries added %s removed %s' % (added[:3], removed[:3]))
    if [k for k in bp if k in hp] != [k for k in hp if k in bp]: f.append('`packages` key ORDER changed')
    changed = [k for k in hp if k in bp and bp[k] != hp[k]]
    if set(changed) != set(plan_paths): f.append('changed entries %s != plan %s' % (sorted(set(changed) - set(plan_paths))[:3] or '', sorted(set(plan_paths) - set(changed))[:3] or ''))
    writes = 0; vonly = 0; integ = {}
    for k in changed:
        if pkg_name(k) not in PLAN: continue
        ef, n = entry_findings(k, bp[k], hp[k]); writes += n
        f += ['%s: %s' % (k, x) for x in ef]
        if 'resolved' not in bp[k] and 'integrity' not in bp[k]: vonly += 1
        if 'integrity' in hp[k]: integ.setdefault(pkg_name(k), set()).add(hp[k]['integrity'])
    rb, ib = roundtrip_exact(braw); rh, ih = roundtrip_exact(hraw)
    if not (rb and rh and ib == ih): f.append('indent: base %s round-trip %s, head %s round-trip %s' % (ib, rb, ih, rh))
    return f, changed, writes, vonly, integ, ih, (bp, hp)


def plan_for(pk):
    return [k for k, e in pk.items() if not e.get('link') and pkg_name(k) in PLAN and is_old(pkg_name(k), e.get('version'))]


def walk(pk_head, pk_base, path, new):
    ph = parents_of(pk_head, path); pb = parents_of(pk_base, path)
    bad = [(p, f, r) for (p, f, r) in ph if not satisfies(new, r)]
    return ph, pb, bad


def cmd_diff(repo, base, head, integ_json, json_out):
    t = Tally()
    changed_paths = [l for l in git(repo, 'diff', '--name-only', base, head).split('\n') if l]
    locks_base = tracked_locks(repo, base)
    plan = {}
    for l in locks_base:
        if not in_scope(l): continue
        pk = json.loads(git_bytes(repo, base, l)).get('packages', {})
        pp = plan_for(pk)
        if pp: plan[l] = pp
    n_plan = sum(len(v) for v in plan.values())
    t.info('PLAN', 'from the BASE %s: %d in-scope locks of %d tracked; planned %d entries in %d locks' % (base[:12], sum(1 for l in locks_base if in_scope(l)), len(locks_base), n_plan, len(plan)))
    want_paths = set(plan) | {K['baseline_path']}
    oos = [l for l in changed_paths if not in_scope(l)]
    t.check('L1', set(changed_paths) == want_paths and not oos, 'changed %d paths == planned %d locks + the baseline: extra %s missing %s | out-of-scope touched %s' % (
        len(changed_paths), len(plan), sorted(set(changed_paths) - want_paths)[:3] or 'none', sorted(want_paths - set(changed_paths))[:3] or 'none', oos or 'none'))
    tot_w = tot_v = tot_e = 0; per_pkg = {}; integ = {}; l2 = []; l3 = []; l6 = []; w1 = []; w2 = []; w3 = []; orphans = []; walked = 0
    for l in sorted(plan):
        braw = git_bytes(repo, base, l); hraw = git_bytes(repo, head, l)
        f, ch, w, v, ig, ind, (bp, hp) = lock_diff(l, braw, hraw, plan[l])
        tot_w += w; tot_v += v; tot_e += len(ch)
        for k in ch: per_pkg[pkg_name(k)] = per_pkg.get(pkg_name(k), 0) + 1
        for n, s in ig.items(): integ.setdefault(n, set()).update(s)
        for x in f:
            (l6 if x.startswith('indent') else l2 if ('top-level' in x or 'added' in x or 'ORDER' in x) else l3).append('%s: %s' % (l, x))
        for k in ch:
            ph, pb, bad = walk(hp, bp, k, PLAN[pkg_name(k)]['new']); walked += 1
            if not ph: orphans.append('%s %s' % (l, k))
            w1 += ['%s %s <- %s %s %r' % (l, k, p or '<root>', fld, r) for (p, fld, r) in bad]
            if sorted(ph) != sorted(pb): w2.append('%s %s parents base %d head %d' % (l, k, len(pb), len(ph)))
        for k, e in hp.items():   # W3 live negative control on the untouched 6.x copies
            if pkg_name(k) == 'postcss-selector-parser' and e.get('version', '').startswith('6.'):
                ps = parents_of(hp, k); w3.append((l, k, ps, [satisfies('7.1.6', r) for (_, _, r) in ps]))
    t.check('L2', not l2, '0 entries added, 0 removed, key order and top-level fields unchanged in %d locks %s' % (len(plan), l2[:3] or ''))
    t.check('L3', not l3 and tot_e == n_plan, 'changed entries %d == plan %d; every entry exactly version(+resolved+integrity where present) %s' % (tot_e, n_plan, l3[:3] or ''))
    want_pkg = dict((n, p['entries']) for n, p in PLAN.items())
    measured_int = {}
    if integ_json:
        measured_int = json.load(open(integ_json))['new_sri']
    one = all(len(s) == 1 for s in integ.values())
    match = all(next(iter(integ[n])) == measured_int.get(n) for n in integ) if measured_int else None
    t.check('L4', one and match is not False, 'one integrity per new version %s | == tarball-derived (%s) %s' % (
        dict((n, next(iter(s))[:22]) for n, s in integ.items()), 'c3 json' if integ_json else 'NOT GIVEN: L4b NOT RUN', match))
    t.check('L5', tot_e == K['plan_totals']['entries'] and tot_w == K['plan_totals']['field_writes'] and tot_v == K['plan_totals']['version_only_entries'] and per_pkg == want_pkg,
            'entries %d (kit %d) | field writes %d (kit %d) | version-only %d (kit %d) | per package %s (kit %s)' % (
                tot_e, K['plan_totals']['entries'], tot_w, K['plan_totals']['field_writes'], tot_v, K['plan_totals']['version_only_entries'], per_pkg, want_pkg))
    census = {}; by_lock = {}
    for l in tracked_locks(repo, head):
        n = detect_indent(git_bytes(repo, head, l).decode()); by_lock[l] = n; census[n] = census.get(n, 0) + 1
    t.check('L6', not l6, 'indent preserved + byte-exact round-trip at base AND head in %d locks %s | head census indent->locks %s' % (len(plan), l6[:3] or '', census))
    t.check('W1', not w1 and not orphans and walked == tot_e, 'parent walk: %d entries walked, %d parent ranges NOT admitting the new version %s, %d orphans %s' % (
        walked, len(w1), w1[:3], len(orphans), orphans[:3]))
    t.check('W2', not w2, 'parent declarations identical base vs head %s' % (w2[:3] or ''))
    w3ok = bool(w3) and all(ps and not any(adm) for (_, _, ps, adm) in w3)
    t.check('W3', w3ok, 'LIVE NEGATIVE CONTROL: %d untouched psp 6.x entries; their parents admit 7.1.6: %s' % (
        len(w3), ['%s %s %s' % (l.split('/')[-2], [r for (_, _, r) in ps], adm) for (l, k, ps, adm) in w3][:4]))
    rp = json.loads(git_bytes(repo, base, K['root_lock']))['packages']
    nl = [e for k, e in rp.items() if k and not e.get('link')]
    root_res = {'non_link': len(nl), 'with_resolved': sum(1 for e in nl if 'resolved' in e), 'without_resolved': sum(1 for e in nl if 'resolved' not in e)}
    names = set(PLAN) | {'sprintf-js'}; allv = 0; allv_locks = set()
    for l in locks_base:
        for k, e in json.loads(git_bytes(repo, base, l)).get('packages', {}).items():
            if not e.get('link') and pkg_name(k) in names: allv += 1; allv_locks.add(l)
    t.info('CENSUS', 'root lock at the base: %s | entries of the five packages at ANY version over all %d tracked locks (mobile included): %d in %d locks' % (
        root_res, len(locks_base), allv, len(allv_locks)))
    if json_out:
        json.dump({'base': base, 'head': head, 'entries': tot_e, 'field_writes': tot_w, 'version_only': tot_v, 'locks': len(plan), 'per_package': per_pkg,
                   'integrity': dict((n, sorted(s)) for n, s in integ.items()), 'indent_census': census, 'indent_by_lock': by_lock,
                   'root_resolved_census': root_res, 'five_any_version_entries': allv, 'tracked_locks': len(locks_base)}, open(json_out, 'w'), indent=1)
        print('JSON %s' % json_out)
    return t.end()


def parse_locks(read, locks):
    res = {}; detail = {}
    for l in locks:
        pk = json.loads(read(l)).get('packages', {})
        for k, e in pk.items():
            n = pkg_name(k)
            if e.get('link') or n not in PLAN and n != 'sprintf-js': continue
            v = e.get('version')
            if not v: continue
            if n == 'postcss-selector-parser':
                bucket = 'psp%s' % v.split('.')[0]
                if satisfies(v, PLAN[n]['vulnerable']): res[bucket] = res.get(bucket, 0) + 1; detail.setdefault(bucket, []).append('%s %s %s' % (l, v, 'dev' if e.get('dev') else 'PROD'))
            elif n == 'sprintf-js':
                if satisfies(v, '<=1.1.3'): res['sprintf-js'] = res.get('sprintf-js', 0) + 1
            elif satisfies(v, PLAN[n]['vulnerable']):
                res[n] = res.get(n, 0) + 1; detail.setdefault(n, []).append('%s %s' % (l, v))
    return res, detail


def cmd_parse(repo, rev, d, expect_clean):
    t = Tally()
    if d:
        locks = sorted(os.path.relpath(os.path.join(r, 'package-lock.json'), d) for r, ds, fs in os.walk(d) if 'package-lock.json' in fs and '/node_modules' not in r and '/.git' not in r)
        read = lambda l: open(os.path.join(d, l), 'rb').read()
        src = 'dir %s' % d
    else:
        locks = tracked_locks(repo, rev); read = lambda l: git_bytes(repo, rev, l); src = 'rev %s' % rev[:12]
    scope = [l for l in locks if in_scope(l)]; mobile = [l for l in locks if not in_scope(l)]
    res, detail = parse_locks(read, scope)
    mres, _ = parse_locks(read, mobile)
    print('PARSE %s: %d locks, %d in scope; vulnerable in scope %s' % (src, len(locks), len(scope), res))
    for b, rows in sorted(detail.items()):
        for r in rows[:6]: print('  %s %s' % (b, r))
    t.info('MOBILE', 'out of scope (%s): vulnerable there %s — the parser SEES what scope excludes' % (mobile, mres))
    t.check('S1', len(mobile) == len(K['out_of_scope_lock_dirs']) and mres.get('source-map-js', 0) > 0,
            'CONTROL: the mobile lock is present and the same parser counts source-map-js < 1.2.2 there: %d' % mres.get('source-map-js', 0))
    if expect_clean:
        z = dict((n, res.get(n, 0)) for n in ('proxy-addr', 'source-map-js', 'smol-toml', 'psp7'))
        t.check('S2', not any(z.values()), 'EXPECT-CLEAN: in-scope vulnerable %s (want all 0) | psp 6.x (baselined by intent) %d | sprintf-js (baselined) %d' % (
            z, res.get('psp6', 0), res.get('sprintf-js', 0)))
    else:
        t.info('S2', 'no --expect-clean: counts reported only (a base control is EXPECTED to be non-zero)')
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def dump(o, n=2): return (json.dumps(o, indent=n) + '\n').encode()
    root = {'name': 'x', 'version': '1.0.0', 'dependencies': {'express': '^4.0.0'}}
    pa_old = {'version': '2.0.7', 'resolved': tarball_url('proxy-addr', '2.0.7'), 'integrity': 'sha512-OLD', 'license': 'MIT'}
    pa_new = dict(pa_old, version='2.0.8', resolved=tarball_url('proxy-addr', '2.0.8'), integrity='sha512-NEW')
    ex = {'version': '4.22.3', 'dependencies': {'proxy-addr': '~2.0.7'}}
    def lock(pa, extra=None):
        pk = {'': root, 'node_modules/express': ex, 'node_modules/proxy-addr': pa}
        pk.update(extra or {}); return {'name': 'x', 'version': '1.0.0', 'lockfileVersion': 3, 'requires': True, 'packages': pk}
    B = dump(lock(pa_old)); pp = ['node_modules/proxy-addr']
    f = lock_diff('t', B, dump(lock(pa_new)), pp)[0]; rep(not f, 'the planned three-field rewrite passes: %s' % (f or 'clean'))
    rep(lock_diff('t', B, dump(lock(pa_new, {'node_modules/zz': {'version': '1.0.0'}})), pp)[0], 'PLANTED added entry FAILS')
    L = lock(pa_new); del L['packages']['node_modules/express']; rep(lock_diff('t', B, dump(L), pp)[0], 'PLANTED removed entry FAILS')
    rep(lock_diff('t', B, dump(lock(dict(pa_new, dev=True))), pp)[0], 'PLANTED 4th field (dev flip) FAILS')
    rr = {'version': '2.0.8', 'integrity': 'sha512-NEW', 'resolved': tarball_url('proxy-addr', '2.0.8'), 'license': 'MIT'}
    rep(lock_diff('t', B, dump(lock(rr)), pp)[0], 'PLANTED reordered fields FAIL')
    vo_old = {'version': '2.0.7', 'license': 'MIT'}; vo_bad = {'version': '2.0.8', 'resolved': tarball_url('proxy-addr', '2.0.8'), 'license': 'MIT'}
    rep(not lock_diff('t', dump(lock(vo_old)), dump(lock({'version': '2.0.8', 'license': 'MIT'})), pp)[0], 'D1: a version-only entry rewritten version-only passes')
    rep(lock_diff('t', dump(lock(vo_old)), dump(lock(vo_bad)), pp)[0], 'PLANTED resolved ADDED to a version-only entry FAILS (D1 shape)')
    rep(lock_diff('t', B, dump(lock(dict(pa_new, version='2.0.9'))), pp)[0], 'PLANTED wrong version FAILS')
    rep(lock_diff('t', B, dump(lock(pa_new), 4), pp)[0], 'PLANTED reindent 2 -> 4 FAILS (D2)')
    rep(not lock_diff('t', dump(lock(pa_old), 4), dump(lock(pa_new), 4), pp)[0], 'D2: an indent-4 file kept at indent 4 passes')
    rep(lock_diff('t', B, B.replace(b'"name": "x",', b'"name":  "x",'), [])[0], 'PLANTED one non-canonical space (round-trip not exact) FAILS')
    pk = lock(pa_new)['packages']; ph, pb, bad = walk(pk, pk, 'node_modules/proxy-addr', '2.0.8'); rep(len(ph) == 1 and not bad, 'walk: express ~2.0.7 admits 2.0.8')
    pk2 = dict(pk); pk2['node_modules/express'] = {'version': '4.0.0', 'dependencies': {'proxy-addr': '~2.0.6 <2.0.8'}}
    rep(walk(pk2, pk2, 'node_modules/proxy-addr', '2.0.8')[2], 'PLANTED out-of-range parent FAILS')
    pk3 = {'': {'name': 'x'}, 'node_modules/proxy-addr': pa_new}; rep(not walk(pk3, pk3, 'node_modules/proxy-addr', '2.0.8')[0], 'PLANTED orphan has 0 parents (W1 fails it)')
    nest = {'': root, 'node_modules/express': ex, 'node_modules/proxy-addr': dict(pa_new, version='1.0.0'), 'node_modules/express/node_modules/proxy-addr': pa_new}
    rep([p for (p, _, _) in parents_of(nest, 'node_modules/express/node_modules/proxy-addr')] == ['node_modules/express'] and not parents_of(nest, 'node_modules/proxy-addr'),
        'nearest node_modules walk: a nested copy shadows the hoisted one')
    cases = [('2.0.8', '~2.0.7', True), ('2.0.8', '^2.0.7', True), ('7.1.6', '^6.1.2', False), ('7.1.6', '^7.1.4', True), ('7.1.6', '^7.1.1', True),
             ('1.9.0', '^1.8.0', True), ('1.9.0', '^1.6.1', True), ('1.0.3', '~1.0.2', True), ('1.1.3', '~1.0.2', False), ('1.2.2', '^1.2.1', True),
             ('2.0.8', '>=1.1.0 <2.0.8', False), ('2.0.7', '>=1.1.0 <2.0.8', True), ('1.8.0', '<=1.8.0', True), ('1.9.0', '<=1.8.0', False),
             ('0.2.5', '^0.2.3', True), ('0.3.0', '^0.2.3', False), ('1.5.0', '1.x || >=2.5.0', True), ('2.4.0', '1.x || >=2.5.0', False),
             ('1.2.3', '1.2.0 - 1.3', True), ('1.4.0', '1.2.0 - 1.3', False), ('3.0.0', '*', True), ('2.0.8', '>= 2.0.7', True)]
    bad = [c for c in cases if satisfies(c[0], c[1]) != c[2]]
    rep(not bad, 'independent semver subset: %d hand cases %s' % (len(cases), bad or 'all agree'))
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    if A[0] == 'diff':
        head = opt('--head', K['pr']['head_expected']); base = opt('--base', K['pr']['parents'][0])
        print('C2 diff #%s head %s base %s' % (K['pr']['pr'], head, base))
        return cmd_diff(opt('--repo'), base, head, opt('--integrity-json'), opt('--json-out'))
    if A[0] == 'parse':
        return cmd_parse(opt('--repo'), opt('--rev'), opt('--dir'), '--expect-clean' in A)
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
