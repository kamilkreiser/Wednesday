#!/usr/bin/env python3
"""c2_locks_gate72.py — the LOCK instruments for #1406 (KS-1437). Read verbs only. Carried from c2_locks_gate70.py; [g72] marks changes.
THE PLAN IS DERIVED FROM THE BASE + THE REGISTRY, NEVER FROM THE HEAD (nor from the builder's plan.json).

  diff  --repo R --head H --base B  [--integrity-json F] [--json-out F]          (REQUIRED: --repo --head --base)
        PLAN: every entry, in every IN-SCOPE lock at the BASE, of shell-quote / @modelcontextprotocol/sdk / pbkdf2 whose version is
        inside the advisory's vulnerable range. [g72] EXPECTED head entry = a MODEL: version -> new; resolved / integrity rewritten ONLY
        where the base entry carries them (root entries carry neither and must keep neither); every lock-relevant field (dependencies,
        engines, peerDependencies, ...) taken from the REGISTRY packument of the NEW version, key order kept from the base.
        M0  MODEL CONTROL: the same model fed the OLD version's packument reproduces every BASE entry exactly (the model can read locks)
        L1  changed path set == the planned lock set; mobile untouched
        L2  per lock: top-level keys / values equal except `packages`; `packages` key SET and ORDER equal (0 added, 0 removed); no
            `overrides` in any changed lock's root entry
        L3  [g72 SEMANTIC] each changed entry == its model at EVERY LEAF and in key ORDER (leaf_diff empty); the changed set == the plan
        L4  integrity: ONE value per new version; == the registry dist.integrity; == --integrity-json (c3's DOWNLOADED sri) when given
        L5  counts: entries 7, leaf field writes 18 (kit), per-entry field set == kit plan_fields_drafter (the drafter's PREDICTION)
        L6  indent detected PER FILE, base == head, BOTH round-trip byte-exact
        LT  [g72 TEXTUAL] `git diff -U0` per lock: #'-' lines == #'+' lines == #leaf writes in that lock, and every -/+ line carries the
            JSON-encoded old/new value of a planned leaf (a line diff that answers a different question than L3)
        W1  IN RANGE, MUST-PASS: every parent (nearest node_modules walk, root + workspace devDependencies included) of every changed entry
            declares a range that ADMITS the new version (lib satisfies, independent of the repo's semver); >= 1 parent each (0 orphans)
        W1f IN RANGE, MUST-FAIL: the same ranges do NOT admit the package's next major (shell-quote 2.0.0, sdk 2.0.0, pbkdf2 4.0.0)
        W2  parent declarations identical at base and head (no range moved)
        W4  [g72] NO CASCADE: every dependency the NEW entry declares resolves (nearest walk from it) to an entry whose version satisfies
            the declared range — the two widened ranges (@hono/node-server, to-buffer) named; 0 unresolved, 0 unsatisfied
  parse --repo R --rev REV | --dir D  [--expect-clean]   in-scope locks: entries of the three packages inside each vulnerable range;
        S1 CONTROL: the out-of-scope mobile lock is read too and its shell-quote 1.8.3 is SEEN (the parser sees what scope excludes)
  --selftest   synthetic locks: every planted defect class must FAIL; 26 semver hand cases.
rc 0 / 1 / 2 refused / 3 registry unreachable (NOT RUN, never a pass)."""
import json, os, re, subprocess, sys, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate72 import (K, Tally, git, git_bytes, tracked_locks, in_scope, roundtrip_exact, detect_indent, pkg_name, parents_of,
                        resolve_path, satisfies, leaf_diff, packument, tgz_url, req, opt)

PLAN = K['plan']; LRF = K['lock_relevant_fields']


def is_vuln(name, ver):
    p = PLAN.get(name)
    return bool(p) and bool(ver) and satisfies(ver, p['vulnerable'])


def model(base_entry, name, ver, meta):
    """The entry npm would write for `name@ver` given the base entry's SHAPE: same key order, resolved / integrity only if present."""
    m = meta['versions'][ver]; out = {}
    for k, v in base_entry.items():
        if k == 'version': out[k] = ver
        elif k == 'resolved': out[k] = tgz_url(name, ver)
        elif k == 'integrity': out[k] = m['dist']['integrity']
        elif k in LRF:
            if k not in m: continue                       # the field disappears in the new version
            nv = m[k]
            if isinstance(v, dict) and isinstance(nv, dict):
                nv = dict([(x, nv[x]) for x in v if x in nv] + [(x, nv[x]) for x in sorted(nv) if x not in v])
            out[k] = nv
        else: out[k] = v                                   # dev / devOptional / optional / peer flags: npm keeps them
    for k in LRF:                                          # a lock-relevant field that APPEARS in the new version
        if k not in out and k not in base_entry and k in m: out[k] = m[k]
    return out


def lock_findings(braw, hraw, plan_paths, expected):
    """per-lock: findings by class, changed keys, leaf writes."""
    f = {'L2': [], 'L3': [], 'L6': []}; b = json.loads(braw); h = json.loads(hraw)
    if [k for k in b if k != 'packages'] != [k for k in h if k != 'packages'] or any(b[k] != h[k] for k in b if k != 'packages'):
        f['L2'].append('top-level keys/values outside `packages` changed')
    bp, hp = b.get('packages', {}), h.get('packages', {})
    added, removed = sorted(set(hp) - set(bp)), sorted(set(bp) - set(hp))
    if added or removed: f['L2'].append('entries added %s removed %s' % (added[:3], removed[:3]))
    if [k for k in bp if k in hp] != [k for k in hp if k in bp]: f['L2'].append('`packages` key ORDER changed')
    if 'overrides' in hp.get('', {}): f['L2'].append('root entry carries `overrides`')
    changed = [k for k in hp if k in bp and bp[k] != hp[k]]
    if set(changed) != set(plan_paths):
        f['L3'].append('changed entries: extra %s missing %s' % (sorted(set(changed) - set(plan_paths))[:3], sorted(set(plan_paths) - set(changed))[:3]))
    writes = {}
    for k in changed:
        d = leaf_diff(bp[k], hp[k]); writes[k] = d
        if k in expected:
            dm = leaf_diff(expected[k], hp[k])
            if dm: f['L3'].append('%s != model: %s' % (k, ['%s %s %r->%r' % x for x in dm][:4]))
    rb, ib = roundtrip_exact(braw); rh, ih = roundtrip_exact(hraw)
    if not (rb and rh and ib == ih): f['L6'].append('indent: base %s round-trip %s, head %s round-trip %s' % (ib, rb, ih, rh))
    return f, changed, writes, ih, (bp, hp)


def line_check(diff_text, writes):
    """LT: -U0 lines vs leaf writes. Returns findings."""
    minus = [l[1:] for l in diff_text.split('\n') if l and l[0] == '-' and not l.startswith('---')]
    plus = [l[1:] for l in diff_text.split('\n') if l and l[0] == '+' and not l.startswith('+++')]
    leaves = [x for d in writes.values() for x in d]
    bad = []
    if not (len(minus) == len(plus) == len(leaves)): bad.append('lines -%d +%d vs leaf writes %d' % (len(minus), len(plus), len(leaves)))
    if any(x[0] != 'change' for x in leaves): bad.append('non-change leaf kinds %s' % sorted(set(x[0] for x in leaves)))
    olds = [json.dumps(x[2], ensure_ascii=False) for x in leaves]; news = [json.dumps(x[3], ensure_ascii=False) for x in leaves]
    bad += ['- line carries no planned old value: %s' % l.strip()[:80] for l in minus if not any(o in l for o in olds)]
    bad += ['+ line carries no planned new value: %s' % l.strip()[:80] for l in plus if not any(n in l for n in news)]
    return bad


def walk_parents(hp, bp, path, new, nmaj):
    ph = parents_of(hp, path); pb = parents_of(bp, path)
    return ph, pb, [(p, f, r) for (p, f, r) in ph if not satisfies(new, r)], [(p, f, r) for (p, f, r) in ph if satisfies(nmaj, r)]


def walk_children(hp, path):
    e = hp[path]; bad = []; widened = []
    opt_peer = set(k for k, v in (e.get('peerDependenciesMeta') or {}).items() if v.get('optional'))
    for fld in ('dependencies', 'optionalDependencies', 'peerDependencies'):
        for name, rng in (e.get(fld) or {}).items():
            tgt = resolve_path(hp, path, name)
            if tgt is None:
                if fld == 'optionalDependencies' or name in opt_peer: continue
                bad.append('%s %s %r UNRESOLVED' % (fld, name, rng)); continue
            v = hp[tgt].get('version')
            if not v or not satisfies(v, rng): bad.append('%s %s %r -> %s %s NOT SATISFIED' % (fld, name, rng, tgt, v))
    return bad


def fetch_meta():
    return dict((n, packument(n)) for n in PLAN)


def cmd_diff(repo, base, head, integ_json, json_out, meta=None):
    t = Tally()
    try:
        meta = meta or fetch_meta()
    except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
        print('REGISTRY UNREACHABLE: %s — c2 diff NOT RUN (never a pass)' % e); return 3
    changed_paths = [l for l in git(repo, 'diff', '--name-only', base, head).split('\n') if l]
    locks_base = tracked_locks(repo, base)
    plan = {}
    for l in locks_base:
        if not in_scope(l): continue
        pk = json.loads(git_bytes(repo, base, l)).get('packages', {})
        pp = [k for k, e in pk.items() if not e.get('link') and pkg_name(k) in PLAN and is_vuln(pkg_name(k), e.get('version'))]
        if pp: plan[l] = pp
    n_plan = sum(len(v) for v in plan.values())
    t.info('PLAN', 'from the BASE %s + the registry: %d in-scope locks of %d tracked; %d vulnerable entries in %d locks: %s' % (
        base[:12], sum(1 for l in locks_base if in_scope(l)), len(locks_base), n_plan, len(plan),
        ['%s %s' % (l.replace('Blockchain/Dev/', '').replace('/package-lock.json', '') or 'root', pkg_name(k)) for l in sorted(plan) for k in plan[l]]))
    oos = [l for l in changed_paths if not in_scope(l)]
    t.check('L1', set(changed_paths) == set(plan) and not oos, 'changed %d paths == planned %d locks: extra %s missing %s | out-of-scope touched %s' % (
        len(changed_paths), len(plan), sorted(set(changed_paths) - set(plan))[:3] or 'none', sorted(set(plan) - set(changed_paths))[:3] or 'none', oos or 'none'))
    m0 = []; l2 = []; l3 = []; l6 = []; lt = []; w1 = []; w1f = []; w2 = []; w4 = []; orphans = []; widened = []
    tot_e = tot_w = 0; per_pkg = {}; integ = {}; fieldsets = {}; walked = 0; by_lock = {}
    for l in sorted(plan):
        braw = git_bytes(repo, base, l); hraw = git_bytes(repo, head, l)
        bp = json.loads(braw)['packages']
        expected = {}
        for k in plan[l]:
            n = pkg_name(k); be = bp[k]
            ctl = leaf_diff(model(be, n, be['version'], meta[n]), be)
            if ctl: m0.append('%s %s: %s' % (l, k, ctl[:2]))
            expected[k] = model(be, n, PLAN[n]['new'], meta[n])
        f, ch, writes, ind, (bp, hp) = lock_findings(braw, hraw, plan[l], expected)
        l2 += ['%s: %s' % (l, x) for x in f['L2']]; l3 += ['%s: %s' % (l, x) for x in f['L3']]; l6 += ['%s: %s' % (l, x) for x in f['L6']]
        lt += ['%s: %s' % (l, x) for x in line_check(git(repo, 'diff', '-U0', base, head, '--', l), writes)]
        tot_e += len(ch)
        for k in ch:
            n = pkg_name(k); per_pkg[n] = per_pkg.get(n, 0) + 1; tot_w += len(writes[k])
            fieldsets['%s %s' % (l, k)] = sorted(x[1] for x in writes[k])
            if 'integrity' in hp[k]: integ.setdefault(n, set()).add(hp[k]['integrity'])
            for x in writes[k]:
                if x[1].startswith('dependencies/'): widened.append('%s %s %s %r -> %r' % (l.split('/')[-2] if l != K['root_lock'] else 'root', n, x[1], x[2], x[3]))
            if n not in PLAN: continue
            ph, pb, bad, badf = walk_parents(hp, bp, k, PLAN[n]['new'], PLAN[n]['next_major']); walked += 1
            if not ph: orphans.append('%s %s' % (l, k))
            w1 += ['%s %s <- %s %s %r' % (l, k, p or '<root>', fl, r) for (p, fl, r) in bad]
            w1f += ['%s %s <- %s %s %r admits %s' % (l, k, p or '<root>', fl, r, PLAN[n]['next_major']) for (p, fl, r) in badf]
            if sorted(ph) != sorted(pb): w2.append('%s %s parents base %d head %d' % (l, k, len(pb), len(ph)))
            print('WALK %s %s %s: parents %s' % (l.replace('Blockchain/Dev/', ''), n, PLAN[n]['new'], ['%s %s %r' % (p or '<root>', fl, r) for (p, fl, r) in ph]))
            w4 += ['%s %s: %s' % (l, k, x) for x in walk_children(hp, k)]
        by_lock[l] = ind
    t.check('M0', not m0, 'MODEL CONTROL: the model fed the OLD packument reproduces %d base entries exactly %s' % (n_plan, m0[:2] or ''))
    t.check('L2', not l2, '0 entries added, 0 removed, key order + top-level fields unchanged, no overrides, in %d locks %s' % (len(plan), l2[:3] or ''))
    t.check('L3', not l3 and tot_e == n_plan, 'SEMANTIC: changed entries %d == plan %d; every changed entry == its base+registry model at every leaf and in key order %s' % (
        tot_e, n_plan, l3[:3] or ''))
    reg_int = dict((n, meta[n]['versions'][PLAN[n]['new']]['dist']['integrity']) for n in PLAN)
    measured = json.load(open(integ_json))['new_sri'] if integ_json else {}
    one = all(len(s) == 1 for s in integ.values())
    reg_ok = all(next(iter(integ[n])) == reg_int[n] for n in integ)
    dl_ok = all(next(iter(integ[n])) == measured.get(n) for n in integ) if measured else None
    t.check('L4', one and reg_ok and dl_ok is not False, 'one integrity per new version %s | == registry dist.integrity %s | == DOWNLOADED sri (%s) %s' % (
        dict((n, next(iter(s))[:24]) for n, s in integ.items()), reg_ok, 'c3 json' if integ_json else 'NOT GIVEN: L4b NOT RUN', dl_ok))
    kf = K['plan_fields_drafter']
    t.check('L5', tot_e == K['plan_totals']['entries'] and tot_w == K['plan_totals']['field_writes'] and fieldsets == dict((k, sorted(v)) for k, v in kf.items()),
            'entries %d (kit %d) | leaf field writes %d (kit %d) | per package %s | per-entry field sets == kit prediction %s %s' % (
                tot_e, K['plan_totals']['entries'], tot_w, K['plan_totals']['field_writes'], per_pkg, fieldsets == dict((k, sorted(v)) for k, v in kf.items()),
                '' if fieldsets == dict((k, sorted(v)) for k, v in kf.items()) else fieldsets))
    t.check('L6', not l6, 'indent preserved + byte-exact round-trip at base AND head in %d locks %s | head indents %s' % (len(plan), l6[:3] or '', sorted(set(by_lock.values()))))
    t.check('LT', not lt, 'TEXTUAL: per lock -/+ lines == leaf writes, every line carries a planned old/new value %s' % (lt[:3] or ''))
    t.check('W1', not w1 and not orphans and walked == tot_e, 'IN RANGE must-pass: %d entries walked, %d parent ranges NOT admitting the new version %s, %d orphans %s' % (
        walked, len(w1), w1[:3], len(orphans), orphans[:3]))
    t.check('W1f', not w1f and walked > 0, 'IN RANGE must-fail: parent ranges admitting the NEXT MAJOR %d %s' % (len(w1f), w1f[:3]))
    t.check('W2', not w2, 'parent declarations identical base vs head %s' % (w2[:3] or ''))
    t.check('W4', not w4 and walked > 0, 'NO CASCADE: every dependency of every changed head entry resolves and satisfies its range %s | widened ranges: %s' % (w4[:3] or '', widened))
    if json_out:
        json.dump({'base': base, 'head': head, 'entries': tot_e, 'field_writes': tot_w, 'locks': len(plan), 'per_package': per_pkg, 'fieldsets': fieldsets,
                   'integrity': dict((n, sorted(s)) for n, s in integ.items()), 'indent_by_lock': by_lock, 'widened': widened,
                   'tracked_locks': len(locks_base)}, open(json_out, 'w'), indent=1)
        print('JSON %s' % json_out)
    return t.end()


def parse_locks(read, locks):
    res = {}; detail = []
    for l in locks:
        for k, e in json.loads(read(l)).get('packages', {}).items():
            n = pkg_name(k)
            if e.get('link') or n not in PLAN: continue
            v = e.get('version')
            detail.append((l, k, n, v, is_vuln(n, v), 'dev' if e.get('dev') else 'PROD'))
            if is_vuln(n, v): res[n] = res.get(n, 0) + 1
    return res, detail


def cmd_parse(repo, rev, d, expect_clean):
    t = Tally()
    if d:
        locks = sorted(os.path.relpath(os.path.join(r, 'package-lock.json'), d) for r, ds, fs in os.walk(d)
                       if 'package-lock.json' in fs and '/node_modules' not in r and '/.git' not in r)
        read = lambda l: open(os.path.join(d, l), 'rb').read(); src = 'dir %s' % d
    else:
        locks = tracked_locks(repo, rev); read = lambda l: git_bytes(repo, rev, l); src = 'rev %s' % rev[:12]
    scope = [l for l in locks if in_scope(l)]; mobile = [l for l in locks if not in_scope(l)]
    res, detail = parse_locks(read, scope); mres, mdet = parse_locks(read, mobile)
    print('PARSE %s: %d locks, %d in scope; entries of the three packages %d; vulnerable in scope %s' % (src, len(locks), len(scope), len(detail), res))
    for row in detail: print('  %s %s %s %s vulnerable=%s %s' % row)
    for row in mdet: print('  OUT-OF-SCOPE %s %s %s %s vulnerable-to-the-plan-range=%s %s' % row)
    sq = [r for r in mdet if r[2] == 'shell-quote']
    t.check('S1', len(mobile) == len(K['out_of_scope_lock_dirs']) and any(r[3] == K['mobile_shell_quote']['pinned'] for r in sq),
            'CONTROL: the mobile lock is present and the same parser SEES its shell-quote %s: %s' % (K['mobile_shell_quote']['pinned'], [r[3] for r in sq]))
    if expect_clean:
        t.check('S2', not any(res.values()) and len(detail) > 0, 'EXPECT-CLEAN: in-scope vulnerable %s over %d entries (want 0 over > 0)' % (res, len(detail)))
    else:
        t.info('S2', 'no --expect-clean: counts reported only (a base control is EXPECTED to be non-zero)')
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def dump(o, n=2): return (json.dumps(o, indent=n) + '\n').encode()
    meta = {'pbkdf2': {'versions': {
        '3.1.6': {'dist': {'integrity': 'sha512-OLD'}, 'license': 'MIT', 'dependencies': {'to-buffer': '^1.2.2', 'sha.js': '^2.4.12'}, 'engines': {'node': '>= 0.10'}},
        '3.1.5': {'dist': {'integrity': 'sha512-OLD5'}, 'license': 'MIT', 'dependencies': {'to-buffer': '^1.2.1', 'sha.js': '^2.4.12'}, 'engines': {'node': '>= 0.10'}},
        '3.1.7': {'dist': {'integrity': 'sha512-NEW'}, 'license': 'MIT', 'dependencies': {'to-buffer': '^1.2.2', 'sha.js': '^2.4.12'}, 'engines': {'node': '>= 0.10'}}}}}
    root = {'name': 'x', 'version': '1.0.0', 'dependencies': {'crypto-browserify': '^3.12.1'}}
    old = {'version': '3.1.6', 'resolved': tgz_url('pbkdf2', '3.1.6'), 'integrity': 'sha512-OLD', 'license': 'MIT',
           'dependencies': {'sha.js': '^2.4.12', 'to-buffer': '^1.2.2'}, 'engines': {'node': '>= 0.10'}}
    cb = {'version': '3.12.1', 'dependencies': {'pbkdf2': '^3.1.2'}}
    def lock(pb, extra=None, cbx=None, tb='1.2.2'):
        pk = {'': root, 'node_modules/crypto-browserify': cbx or cb, 'node_modules/pbkdf2': pb, 'node_modules/sha.js': {'version': '2.4.12'},
              'node_modules/to-buffer': {'version': tb}}
        pk.update(extra or {}); return {'name': 'x', 'version': '1.0.0', 'lockfileVersion': 3, 'requires': True, 'packages': pk}
    exp = model(old, 'pbkdf2', '3.1.7', meta['pbkdf2']); pp = ['node_modules/pbkdf2']; E = {'node_modules/pbkdf2': exp}
    rep(not leaf_diff(model(old, 'pbkdf2', '3.1.6', meta['pbkdf2']), old), 'M0 the model fed the OLD packument reproduces the base entry')
    B = dump(lock(old))
    def fl(h, e=E, b=B): f = lock_findings(b, h, pp, e)[0]; return f['L2'] + f['L3'] + f['L6']
    rep(not fl(dump(lock(exp))), 'the modelled rewrite passes')
    rep(fl(dump(lock(exp, {'node_modules/zz': {'version': '1.0.0'}}))), 'PLANTED added entry FAILS')
    L = lock(exp); del L['packages']['node_modules/sha.js']; rep(fl(dump(L)), 'PLANTED removed entry FAILS')
    rep(fl(dump(lock(dict(exp, dev=True)))), 'PLANTED extra field (dev flip) FAILS')
    rr = dict([('integrity', exp['integrity'])] + [(k, v) for k, v in exp.items() if k != 'integrity'])
    rep(fl(dump(lock(rr))), 'PLANTED reordered fields FAIL (order is a leaf of its own)')
    # the root shape: version-only + a dependency range that MUST move (3.1.5 -> 3.1.7 moves to-buffer)
    vo = {'version': '3.1.5', 'license': 'MIT', 'dependencies': {'sha.js': '^2.4.12', 'to-buffer': '^1.2.1'}, 'engines': {'node': '>= 0.10'}}
    vexp = model(vo, 'pbkdf2', '3.1.7', meta['pbkdf2']); VE = {'node_modules/pbkdf2': vexp}; VB = dump(lock(vo))
    rep(not fl(dump(lock(vexp)), VE, VB) and vexp['dependencies']['to-buffer'] == '^1.2.2' and 'resolved' not in vexp, 'root shape: version + dependencies[to-buffer] -> ^1.2.2, no resolved, passes')
    stale = dict(vexp, dependencies={'sha.js': '^2.4.12', 'to-buffer': '^1.2.1'})
    rep(fl(dump(lock(stale)), VE, VB), 'PLANTED STALE dependencies range (a three-field writer) FAILS')
    rep(fl(dump(lock(dict(vexp, resolved=tgz_url('pbkdf2', '3.1.7')))), VE, VB), 'PLANTED resolved ADDED to a root (version-only) entry FAILS')
    rep(fl(dump(lock(dict(exp, version='3.1.8')))), 'PLANTED wrong version FAILS')
    rep(fl(dump(lock(exp), 4)), 'PLANTED reindent 2 -> 4 FAILS')
    rep(not lock_findings(dump(lock(old), 3), dump(lock(exp), 3), pp, E)[0]['L6'], 'an indent-3 file kept at indent 3 passes (indent is per file)')
    rep(fl(B.replace(b'"name": "x",', b'"name":  "x",'), E, B), 'PLANTED one non-canonical space (round-trip not exact) FAILS')
    L = lock(exp); L['packages'][''] = dict(root, overrides={'pbkdf2': '3.1.7'}); rep(fl(dump(L)), 'PLANTED `overrides` in the root entry FAILS')
    # textual
    import difflib
    def u0(a, b):
        return '\n'.join(difflib.unified_diff(a.decode().split('\n'), b.decode().split('\n'), n=0, lineterm=''))
    H = dump(lock(exp)); w = {'node_modules/pbkdf2': leaf_diff(old, exp)}
    rep(not line_check(u0(B, H), w), 'LT: the real -U0 lines match the 3 leaf writes')
    rep(line_check(u0(B, H.replace(b'"license": "MIT",\n      "dependencies"', b'"license": "ISC",\n      "dependencies"')), w), 'PLANTED an extra changed line (license) FAILS LT')
    # walks
    pk = lock(exp)['packages']
    rep(not walk_parents(pk, pk, 'node_modules/pbkdf2', '3.1.7', '4.0.0')[2], 'W1 must-pass: crypto-browserify ^3.1.2 admits 3.1.7')
    rep(not walk_parents(pk, pk, 'node_modules/pbkdf2', '3.1.7', '4.0.0')[3], 'W1f must-fail: ^3.1.2 does NOT admit 4.0.0')
    pk2 = lock(exp, cbx={'version': '3.12.1', 'dependencies': {'pbkdf2': '*'}})['packages']
    rep(walk_parents(pk2, pk2, 'node_modules/pbkdf2', '3.1.7', '4.0.0')[3], 'PLANTED parent range `*` admits the next major: W1f FIRES')
    pk3 = lock(exp, cbx={'version': '3.12.1', 'dependencies': {'pbkdf2': '~3.1.2 <3.1.7'}})['packages']
    rep(walk_parents(pk3, pk3, 'node_modules/pbkdf2', '3.1.7', '4.0.0')[2], 'PLANTED out-of-range parent FAILS W1')
    pk4 = {'': {'name': 'x'}, 'node_modules/pbkdf2': exp}; rep(not walk_parents(pk4, pk4, 'node_modules/pbkdf2', '3.1.7', '4.0.0')[0], 'PLANTED orphan has 0 parents (W1 fails it)')
    rep(not walk_children(pk, 'node_modules/pbkdf2'), 'W4: children resolve and satisfy')
    rep(walk_children(lock(exp, tb='1.2.1')['packages'], 'node_modules/pbkdf2'), 'PLANTED to-buffer 1.2.1 under a ^1.2.2 range: W4 CASCADE FIRES')
    pk5 = lock(exp)['packages']; del pk5['node_modules/sha.js']; rep(walk_children(pk5, 'node_modules/pbkdf2'), 'PLANTED unresolved child FAILS W4')
    cases = [('1.11.0', '^1.8.1', True), ('2.0.0', '^1.8.1', False), ('1.31.0', '^1.27.0', True), ('2.0.0', '^1.27.0', False),
             ('3.1.7', '^3.1.3', True), ('3.1.7', '^3.1.2', True), ('3.1.7', '^3.1.5', True), ('4.0.0', '^3.1.3', False),
             ('1.9.0', '>=1.8.4 <1.11.0', True), ('1.11.0', '>=1.8.4 <1.11.0', False), ('1.8.3', '>=1.8.4 <1.11.0', False),
             ('1.29.0', '>=1.12.0 <1.31.0', True), ('1.31.0', '>=1.12.0 <1.31.0', False), ('3.1.6', '<=3.1.6', True), ('3.1.7', '<=3.1.6', False),
             ('1.19.17', '^1.19.9 || ^2.0.5', True), ('2.0.5', '^1.19.9 || ^2.0.5', True), ('1.19.8', '^1.19.9 || ^2.0.5', False),
             ('1.2.2', '^1.2.2', True), ('1.2.1', '^1.2.2', False), ('0.2.5', '^0.2.3', True), ('0.3.0', '^0.2.3', False),
             ('1.2.3', '1.2.0 - 1.3', True), ('1.4.0', '1.2.0 - 1.3', False), ('3.0.0', '*', True), ('2.0.8', '>= 2.0.7', True)]
    bad = [c for c in cases if satisfies(c[0], c[1]) != c[2]]
    rep(not bad, 'independent semver subset: %d hand cases %s' % (len(cases), bad or 'all agree'))
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        if A[0] == 'diff':
            repo = req(A, '--repo'); head = req(A, '--head', True); base = req(A, '--base', True)
            print('C2 diff #%s head %s base %s' % (K['pr']['pr'], head, base))
            return cmd_diff(repo, base, head, opt(A, '--integrity-json'), opt(A, '--json-out'))
        if A[0] == 'parse':
            if not opt(A, '--dir'):
                req(A, '--repo'); req(A, '--rev', True)
            return cmd_parse(opt(A, '--repo'), opt(A, '--rev'), opt(A, '--dir'), '--expect-clean' in A)
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
