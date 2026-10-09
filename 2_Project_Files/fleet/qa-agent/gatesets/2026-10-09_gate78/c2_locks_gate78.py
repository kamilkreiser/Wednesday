#!/usr/bin/env python3
"""c2_locks_gate78.py — the LOCK instruments for #1435 (KS-1452). Read verbs only. Carried from c2_locks_gate72.py; [g72] marks gate72's
changes, [g78] this kit's. THE PLAN IS DERIVED FROM THE BASE + THE REGISTRY, NEVER FROM THE HEAD (nor from the builder's plan.json / READY).

  diff  --repo R --head H --base B  [--integrity-json F] [--json-out F]          (REQUIRED: --repo --head --base)
        PLAN: every entry, in every IN-SCOPE lock at the BASE, of handlebars whose version is inside the advisories' vulnerable range
        (>=4.0.0 <=4.7.9). EXPECTED head entry = a MODEL: version -> 4.7.10; resolved / integrity rewritten ONLY where the base entry
        carries them (the root entry carries neither and must keep neither); every lock-relevant field (dependencies, optionalDependencies,
        engines, bin, ...) taken from the REGISTRY packument of 4.7.10, key order kept from the base.
        M0  MODEL CONTROL: the same model fed the 4.7.9 packument reproduces every BASE entry exactly (the model can read locks)
        L1  changed path set == the planned lock set; mobile untouched
        L2  per lock: top-level keys / values equal except `packages`; `packages` key SET and ORDER equal (0 added, 0 removed); no
            `overrides` in any changed lock's root entry
        L3  [g72 SEMANTIC] each changed entry == its model at EVERY LEAF and in key ORDER (leaf_diff empty); the changed set == the plan
        L4  integrity: ONE value for 4.7.10; == the registry dist.integrity; == --integrity-json (c3's DOWNLOADED sri) when given
        L5  counts: entries 5, leaf field writes 18 (kit), per-entry field set == kit plan_fields_drafter (the builder's claim: root
            version + dependencies/minimist; each standalone version + resolved + integrity + dependencies/minimist)
        L6  indent detected PER FILE, base == head, BOTH round-trip byte-exact
        L7  [g78 MASKED BYTE COMPARE] each head lock with every changed entry put back to its BASE entry, re-serialised at its own indent,
            is BYTE-IDENTICAL to the base blob (the builder's "with the handlebars entry masked, every lock is byte-identical to develop",
            by an independent instrument)
        LT  [g72 TEXTUAL] `git diff -U0` per lock: #'-' lines == #'+' lines == #leaf writes in that lock, and every -/+ line carries the
            JSON-encoded old/new value of a planned leaf (a line diff that answers a different question than L3)
        W1  IN RANGE, MUST-PASS: every parent (nearest node_modules walk, root + workspace devDependencies included) of every changed entry
            declares a range that ADMITS 4.7.10 (lib satisfies, independent of the repo's semver); >= 1 parent each (0 orphans). The
            declaring-parent COUNT is printed (builder: "all 7 declaring parents say ^4.7.9")
        W1f IN RANGE, MUST-FAIL: the same ranges do NOT admit the next major (handlebars 5.0.0)
        W2  parent declarations identical at base and head (no range moved)
        W4  [g72] NO CASCADE: every dependency the NEW entry declares resolves (nearest walk from it) to an entry whose version satisfies
            the declared range — the widened range (minimist ^1.2.5 -> ^1.2.8) named with the version it resolves to; 0 unresolved, 0
            unsatisfied (an UNRESOLVED optionalDependency, e.g. uglify-js, is skipped BY NAME, never silently)
  parse --repo R --rev REV | --dir D  [--expect-clean]   EVERY tracked lock (the builder's census says 45): handlebars entries, flag,
        version; vulnerable count in scope and out of scope, printed separately.
        S1 CONTROL: the parser SEES handlebars (> 0 entries over the tracked locks at REV) and READ the out-of-scope mobile lock
        S2 (--expect-clean) in-scope vulnerable 0 over > 0 entries; S3 (--expect-clean) [g78] exactly kit plan_totals.entries entries at
           the new version (builder: "exactly 5 at 4.7.10")
  --selftest   synthetic locks: every planted defect class must FAIL; semver hand cases.
rc 0 / 1 / 2 refused / 3 registry unreachable (NOT RUN, never a pass)."""
import json, os, re, subprocess, sys, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate78 import (K, Tally, git, git_bytes, tracked_locks, in_scope, roundtrip_exact, detect_indent, pkg_name, parents_of,
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
            if k == 'dependencies' and isinstance(nv, dict) and isinstance(m.get('optionalDependencies'), dict):
                # [g78] the registry packument repeats every optionalDependency inside `dependencies`; npm's lock writes it ONLY
                # under optionalDependencies (M0 caught this on handlebars' uglify-js at draft, 2026-10-09)
                nv = dict((x, y) for x, y in nv.items() if x not in m['optionalDependencies'])
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


def entry_span(lines, key, n):
    """[g78] (start, end) line indices of the `packages` entry `key` as TEXT: the line `<2n spaces>"<key>": {` through the first later
    line that is `<2n spaces>}` or `<2n spaces>},`. None if absent or ambiguous (the caller FAILS on None)."""
    opener = ' ' * (2 * n) + json.dumps(key, ensure_ascii=False) + ': {'
    starts = [i for i, l in enumerate(lines) if l.rstrip('\n') == opener]
    if len(starts) != 1: return None
    for j in range(starts[0] + 1, len(lines)):
        if lines[j].rstrip('\n') in (' ' * (2 * n) + '}', ' ' * (2 * n) + '},'): return starts[0], j
    return None


def masked_equal(braw, hraw, changed):
    """[g78] a BYTE compare, never a re-serialisation: in the head's TEXT, each changed entry's line span is replaced by the base's
    span for the same key; the result must equal the base BYTES. A stray byte anywhere outside the changed entries fails it."""
    n = detect_indent(hraw.decode('utf-8'))
    if n is None or n != detect_indent(braw.decode('utf-8')): return False
    bl = braw.decode('utf-8').splitlines(True); hl = hraw.decode('utf-8').splitlines(True)
    for k in changed:
        sb, sh = entry_span(bl, k, n), entry_span(hl, k, n)
        if sb is None or sh is None: return False
        hl = hl[:sh[0]] + bl[sb[0]:sb[1] + 1] + hl[sh[1] + 1:]
    return ''.join(hl).encode('utf-8') == braw


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


def walk_children(hp, path, verbose=False):
    e = hp[path]; bad = []; widened = []
    opt_peer = set(k for k, v in (e.get('peerDependenciesMeta') or {}).items() if v.get('optional'))
    for fld in ('dependencies', 'optionalDependencies', 'peerDependencies'):
        for name, rng in (e.get(fld) or {}).items():
            tgt = resolve_path(hp, path, name)
            if tgt is None:
                if fld == 'optionalDependencies' or name in opt_peer:
                    print('  W4 SKIPPED BY NAME %s %s %s %r: unresolved, optional' % (path, fld, name, rng)); continue
                bad.append('%s %s %r UNRESOLVED' % (fld, name, rng)); continue
            v = hp[tgt].get('version')
            if not v or not satisfies(v, rng): bad.append('%s %s %r -> %s %s NOT SATISFIED' % (fld, name, rng, tgt, v))
            elif verbose: print('  W4 %s %s %s %r -> %s %s satisfied' % (path, fld, name, rng, tgt, v))
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
    tot_e = tot_w = 0; per_pkg = {}; integ = {}; fieldsets = {}; walked = 0; by_lock = {}; n_parents = 0; l7 = []
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
        mk = masked_equal(braw, hraw, ch)
        if not mk: l7.append(l)
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
            ph, pb, bad, badf = walk_parents(hp, bp, k, PLAN[n]['new'], PLAN[n]['next_major']); walked += 1; n_parents += len(ph)
            if not ph: orphans.append('%s %s' % (l, k))
            w1 += ['%s %s <- %s %s %r' % (l, k, p or '<root>', fl, r) for (p, fl, r) in bad]
            w1f += ['%s %s <- %s %s %r admits %s' % (l, k, p or '<root>', fl, r, PLAN[n]['next_major']) for (p, fl, r) in badf]
            if sorted(ph) != sorted(pb): w2.append('%s %s parents base %d head %d' % (l, k, len(pb), len(ph)))
            print('WALK %s %s %s: parents %s' % (l.replace('Blockchain/Dev/', ''), n, PLAN[n]['new'], ['%s %s %r' % (p or '<root>', fl, r) for (p, fl, r) in ph]))
            w4 += ['%s %s: %s' % (l, k, x) for x in walk_children(hp, k, verbose=True)]
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
    t.check('L7', not l7 and tot_e > 0, 'MASKED BYTE COMPARE: every changed entry put back to its base entry -> each head lock byte-identical to its base blob: %d/%d %s' % (
        len(plan) - len(l7), len(plan), l7[:3] or ''))
    t.check('LT', not lt, 'TEXTUAL: per lock -/+ lines == leaf writes, every line carries a planned old/new value %s' % (lt[:3] or ''))
    t.check('W1', not w1 and not orphans and walked == tot_e, 'IN RANGE must-pass: %d entries walked, %d declaring parents in all, %d parent ranges NOT admitting the new version %s, %d orphans %s' % (
        walked, n_parents, len(w1), w1[:3], len(orphans), orphans[:3]))
    t.check('W1f', not w1f and walked > 0, 'IN RANGE must-fail: parent ranges admitting the NEXT MAJOR %d %s' % (len(w1f), w1f[:3]))
    t.check('W2', not w2, 'parent declarations identical base vs head %s' % (w2[:3] or ''))
    t.check('W4', not w4 and walked > 0, 'NO CASCADE: every dependency of every changed head entry resolves and satisfies its range %s | widened ranges: %s' % (w4[:3] or '', widened))
    if json_out:
        json.dump({'base': base, 'head': head, 'entries': tot_e, 'field_writes': tot_w, 'locks': len(plan), 'per_package': per_pkg, 'fieldsets': fieldsets,
                   'integrity': dict((n, sorted(s)) for n, s in integ.items()), 'indent_by_lock': by_lock, 'widened': widened,
                   'tracked_locks': len(locks_base), 'declaring_parents': n_parents, 'masked_equal_failures': l7}, open(json_out, 'w'), indent=1)
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
    new = dict((n, p['new']) for n, p in PLAN.items())
    at_new = [r for r in detail if r[3] == new.get(r[2])]
    print('PARSE %s: %d tracked locks, %d in scope, %d out of scope %s; entries of the plan package(s) %d in scope, %d out of scope; vulnerable in scope %s, out of scope %s; at the new version %d' % (
        src, len(locks), len(scope), len(mobile), mobile, len(detail), len(mdet), res, mres, len(at_new)))
    for row in detail: print('  %s %s %s %s vulnerable=%s %s' % row)
    for row in mdet: print('  OUT-OF-SCOPE %s %s %s %s vulnerable=%s %s' % row)
    t.check('S1', len(detail) + len(mdet) > 0 and len(mobile) == len(K['out_of_scope_lock_dirs']),
            'CONTROL: the parser SEES %d plan-package entries over %d tracked locks, and READ the %d out-of-scope lock(s) %s (its entries: %d)' % (
                len(detail) + len(mdet), len(locks), len(mobile), mobile, len(mdet)))
    if expect_clean:
        t.check('S2', not any(res.values()) and len(detail) > 0, 'EXPECT-CLEAN: in-scope vulnerable %s over %d entries (want 0 over > 0)' % (res, len(detail)))
        t.check('S3', len(at_new) == K['plan_totals']['entries'], 'EXPECT-CLEAN: entries at the new version %d (kit %d)' % (len(at_new), K['plan_totals']['entries']))
    else:
        t.info('S2', 'no --expect-clean: counts reported only (a base control is EXPECTED to be non-zero)')
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    def dump(o, n=2): return (json.dumps(o, indent=n) + '\n').encode()
    common = {'license': 'MIT', 'optionalDependencies': {'uglify-js': '^3.1.4'}, 'bin': {'handlebars': 'bin/handlebars'}, 'engines': {'node': '>=0.4.7'}}
    meta = {'handlebars': {'versions': {
        '4.7.9': dict(common, dist={'integrity': 'sha512-OLD'}, dependencies={'minimist': '^1.2.5', 'neo-async': '^2.6.2', 'source-map': '^0.6.1', 'uglify-js': '^3.1.4', 'wordwrap': '^1.0.0'}),
        '4.7.10': dict(common, dist={'integrity': 'sha512-NEW'}, dependencies={'minimist': '^1.2.8', 'neo-async': '^2.6.2', 'source-map': '^0.6.1', 'uglify-js': '^3.1.4', 'wordwrap': '^1.0.0'})}}}
    # the REAL registry shape: an optionalDependency is repeated inside `dependencies` (M0 caught it at draft)
    deps_old = {'minimist': '^1.2.5', 'neo-async': '^2.6.2', 'source-map': '^0.6.1', 'wordwrap': '^1.0.0'}
    # a standalone entry (dev) and the root entry shape (no resolved / integrity)
    old = {'version': '4.7.9', 'resolved': tgz_url('handlebars', '4.7.9'), 'integrity': 'sha512-OLD', 'dev': True, 'license': 'MIT',
           'dependencies': dict(deps_old), 'bin': {'handlebars': 'bin/handlebars'}, 'engines': {'node': '>=0.4.7'},
           'optionalDependencies': {'uglify-js': '^3.1.4'}}
    root = {'name': 'x', 'version': '1.0.0', 'devDependencies': {'ts-jest': '^29.4.11'}}
    tj = {'version': '29.4.11', 'dev': True, 'dependencies': {'handlebars': '^4.7.9'}}
    def lock(hb, extra=None, tjx=None, mm='1.2.8'):
        pk = {'': root, 'node_modules/ts-jest': tjx or tj, 'node_modules/handlebars': hb, 'node_modules/minimist': {'version': mm, 'dev': True},
              'node_modules/neo-async': {'version': '2.6.2'}, 'node_modules/source-map': {'version': '0.6.1'}, 'node_modules/wordwrap': {'version': '1.0.0'}}
        pk.update(extra or {}); return {'name': 'x', 'version': '1.0.0', 'lockfileVersion': 3, 'requires': True, 'packages': pk}
    exp = model(old, 'handlebars', '4.7.10', meta['handlebars']); pp = ['node_modules/handlebars']; E = {'node_modules/handlebars': exp}
    rep(not leaf_diff(model(old, 'handlebars', '4.7.9', meta['handlebars']), old), 'M0 the model fed the OLD packument reproduces the base entry')
    nopt = json.loads(json.dumps(meta)); [v.pop('optionalDependencies') for v in nopt['handlebars']['versions'].values()]
    rep(leaf_diff(model(old, 'handlebars', '4.7.9', nopt['handlebars']), old), 'PLANTED packument without optionalDependencies: the model keeps uglify-js in dependencies and M0 FIRES')
    rep(sorted(x[1] for x in leaf_diff(old, exp)) == ['dependencies/minimist', 'integrity', 'resolved', 'version'], 'a standalone entry moves exactly version / resolved / integrity / dependencies/minimist')
    B = dump(lock(old))
    def fl(h, e=E, b=B): f = lock_findings(b, h, pp, e)[0]; return f['L2'] + f['L3'] + f['L6']
    rep(not fl(dump(lock(exp))), 'the modelled rewrite passes')
    rep(fl(dump(lock(exp, {'node_modules/zz': {'version': '1.0.0'}}))), 'PLANTED added entry FAILS')
    L = lock(exp); del L['packages']['node_modules/wordwrap']; rep(fl(dump(L)), 'PLANTED removed entry FAILS')
    rep(fl(dump(lock(dict(exp, dev=False)))), 'PLANTED dev flag flip FAILS')
    rr = dict([('integrity', exp['integrity'])] + [(k, v) for k, v in exp.items() if k != 'integrity'])
    rep(fl(dump(lock(rr))), 'PLANTED reordered fields FAIL (order is a leaf of its own)')
    stale = dict(exp, dependencies=dict(deps_old))
    rep(fl(dump(lock(stale))), 'PLANTED STALE dependencies.minimist ^1.2.5 (a three-field writer) FAILS')
    ro = {'version': '4.7.9', 'license': 'MIT', 'dependencies': dict(deps_old), 'bin': {'handlebars': 'bin/handlebars'}, 'engines': {'node': '>=0.4.7'},
          'optionalDependencies': {'uglify-js': '^3.1.4'}}
    rexp = model(ro, 'handlebars', '4.7.10', meta['handlebars']); RE_ = {'node_modules/handlebars': rexp}; RB = dump(lock(ro))
    rep(not fl(dump(lock(rexp)), RE_, RB) and sorted(x[1] for x in leaf_diff(ro, rexp)) == ['dependencies/minimist', 'version'] and 'resolved' not in rexp,
        'root shape: version + dependencies/minimist only, no resolved / integrity, passes')
    rep(fl(dump(lock(dict(rexp, resolved=tgz_url('handlebars', '4.7.10')))), RE_, RB), 'PLANTED resolved ADDED to the root (version-only) entry FAILS')
    rep(fl(dump(lock(dict(exp, version='4.7.11')))), 'PLANTED wrong version FAILS')
    rep(fl(dump(lock(exp), 4)), 'PLANTED reindent 2 -> 4 FAILS')
    rep(not lock_findings(dump(lock(old), 3), dump(lock(exp), 3), pp, E)[0]['L6'], 'an indent-3 file kept at indent 3 passes (indent is per file)')
    rep(fl(B.replace(b'"name": "x",', b'"name":  "x",'), E, B), 'PLANTED one non-canonical space (round-trip not exact) FAILS')
    L = lock(exp); L['packages'][''] = dict(root, overrides={'handlebars': '4.7.10'}); rep(fl(dump(L)), 'PLANTED `overrides` in the root entry FAILS')
    # L7 masked byte compare
    H = dump(lock(exp))
    rep(masked_equal(B, H, pp), 'L7: the head with the handlebars entry masked is byte-identical to the base')
    rep(not masked_equal(B, dump(lock(exp, {'node_modules/wordwrap': {'version': '1.0.1'}})), pp), 'PLANTED collateral entry (wordwrap 1.0.1) FIRES L7')
    rep(not masked_equal(B, H.replace(b'"lockfileVersion": 3', b'"lockfileVersion":  3'), pp), 'PLANTED one stray byte outside the entry FIRES L7')
    rep(not masked_equal(B, dump(lock(exp), 4), pp), 'PLANTED reindent FIRES L7')
    rep(not masked_equal(B, H, ['node_modules/nope']), 'PLANTED a changed key absent from both texts: L7 FAILS (None is never a pass)')
    rep(not masked_equal(B, H.replace(b'"wordwrap": "^1.0.0"', b'"wordwrap": "^1.0.1"', 1), []), 'L7 with NO entry masked sees the real change (the masking is what makes it pass)')
    # textual
    import difflib
    def u0(a, b):
        return '\n'.join(difflib.unified_diff(a.decode().split('\n'), b.decode().split('\n'), n=0, lineterm=''))
    w = {'node_modules/handlebars': leaf_diff(old, exp)}
    rep(not line_check(u0(B, H), w), 'LT: the real -U0 lines match the 4 leaf writes')
    rep(line_check(u0(B, H.replace(b'"license": "MIT",\n      "dependencies"', b'"license": "ISC",\n      "dependencies"')), w), 'PLANTED an extra changed line (license) FAILS LT')
    # walks
    pk = lock(exp)['packages']
    rep(not walk_parents(pk, pk, 'node_modules/handlebars', '4.7.10', '5.0.0')[2], 'W1 must-pass: ts-jest ^4.7.9 admits 4.7.10')
    rep(not walk_parents(pk, pk, 'node_modules/handlebars', '4.7.10', '5.0.0')[3], 'W1f must-fail: ^4.7.9 does NOT admit 5.0.0')
    pk2 = lock(exp, tjx={'version': '29.4.11', 'dependencies': {'handlebars': '*'}})['packages']
    rep(walk_parents(pk2, pk2, 'node_modules/handlebars', '4.7.10', '5.0.0')[3], 'PLANTED parent range `*` admits the next major: W1f FIRES')
    pk3 = lock(exp, tjx={'version': '29.4.11', 'dependencies': {'handlebars': '~4.7.9 <4.7.10'}})['packages']
    rep(walk_parents(pk3, pk3, 'node_modules/handlebars', '4.7.10', '5.0.0')[2], 'PLANTED out-of-range parent FAILS W1')
    pk4 = {'': {'name': 'x'}, 'node_modules/handlebars': exp}; rep(not walk_parents(pk4, pk4, 'node_modules/handlebars', '4.7.10', '5.0.0')[0], 'PLANTED orphan has 0 parents (W1 fails it)')
    pk6 = lock(exp)['packages']; pk6[''] = dict(root, dependencies={'handlebars': '^4.7.9'})
    rep(len(walk_parents(pk6, pk6, 'node_modules/handlebars', '4.7.10', '5.0.0')[0]) == 2, 'W1 counts BOTH declarers (root direct + ts-jest): originate\'s shape')
    rep(not walk_children(pk, 'node_modules/handlebars'), 'W4: children resolve and satisfy (uglify-js optional, skipped by name)')
    rep(walk_children(lock(exp, mm='1.2.6')['packages'], 'node_modules/handlebars'), 'PLANTED minimist 1.2.6 under ^1.2.8: W4 CASCADE FIRES')
    pk5 = lock(exp)['packages']; del pk5['node_modules/neo-async']; rep(walk_children(pk5, 'node_modules/handlebars'), 'PLANTED unresolved child FAILS W4')
    cases = [('4.7.10', '^4.7.9', True), ('5.0.0', '^4.7.9', False), ('4.7.8', '^4.7.9', False), ('4.7.9', '>=4.0.0 <=4.7.9', True),
             ('4.7.10', '>=4.0.0 <=4.7.9', False), ('3.0.8', '>=4.0.0 <=4.7.9', False), ('4.0.0', '>=4.0.0 <=4.7.9', True),
             ('1.2.8', '^1.2.8', True), ('1.2.5', '^1.2.8', False), ('1.2.8', '^1.2.5', True), ('2.0.0', '^1.2.8', False),
             ('0.6.1', '^0.6.1', True), ('0.7.0', '^0.6.1', False), ('3.19.3', '^3.1.4', True), ('4.7.10-rc.1', '^4.7.9', False),
             ('1.2.3', '1.2.0 - 1.3', True), ('1.4.0', '1.2.0 - 1.3', False), ('3.0.0', '*', True), ('4.7.10', '4.x', True), ('4.7.10', '~4.7.0', True)]
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
