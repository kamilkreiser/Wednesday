#!/usr/bin/env python3
"""c3_registry_gate78.py — INTEGRITY FROM THE DOWNLOADED TARBALL, and the advisories, for #1435 (KS-1452). Carried from
c3_registry_gate72.py; [g78] marks this kit's changes. Network: registry.npmjs.org READS only (tarball GETs, packument GETs, and the
bulk-advisory query POST — leg 7's own instrument, audit-locks.mjs). Never npm. Tarballs are untrusted DATA: written to a FRESH dir,
hashed, never unpacked, never executed.

  tarballs --repo R --head H --base B --out DIR [--json-out F]          (REQUIRED: --repo --head --base --out)
     T1  the NEW tarball (handlebars 4.7.10) DOWNLOADED, sha512'd HERE == the packument's dist.integrity
     T2  NEGATIVE CONTROL: the OLD tarball (4.7.9) is downloaded too; its sri != the new one, == its own dist.integrity, and == every
         integrity the BASE locks carry for 4.7.9 (> 0 such entries; the root lock carries none — counted separately, reported)
     T3  every changed head entry that carries `integrity` == the DOWNLOADED sri of 4.7.10 (0 mismatches over N > 0; builder: 4)
     T4  RESOLVED: every changed head entry carrying `resolved` == the tarball URL actually downloaded
     T5  [g78] the READY's FULL integrity strings (new AND old) == the downloaded sri, and the READY's tarball size (712,317 B) == the
         downloaded byte count (a third, written source)
     --json-out writes {"new_sri", "old_sri", "bytes", "dir"} for c2 diff --integrity-json (L4b) and gh prtext.
  advisories [--json-out F]
     A1  bulk query of 4.7.10 returns {} exactly (no advisory at all, not only "none of the three")
     A2  CONTROL: 4.7.9 returns the three ids (8r5x / p8wg / xw65), each with the kit's vulnerable range >=4.0.0 <=4.7.9
     A3  severities measured == kit (critical / critical / moderate)
     A4  each id is returned for handlebars (no id moved package)
     A5  [g78] VERSION FACTS (packument): 4.7.10 == dist-tags.latest; the ONLY release-shaped version above 4.7.9; its publish time
         printed; the lock-relevant field delta 4.7.9 -> 4.7.10 (optionalDependencies subtracted from dependencies, as npm writes the
         lock) == kit field_delta_ready (builder: dependencies.minimist ^1.2.5 -> ^1.2.8, "every other lock-relevant field EQUAL")
  --selftest   sri of known bytes, the id reader, the A1 exact-{} predicate, the version / field-delta predicates (no network).
rc 0 / 1 / 2 refused / 3 network failure (NOT RUN, never a pass)."""
import json, os, sys, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate78 import (K, Tally, git, git_bytes, tracked_locks, in_scope, pkg_name, sri_sha512, http_get, bulk_advisories, ids_of,
                        packument, tgz_url, req, opt)

PLAN = K['plan']


def lock_integrities(repo, rev, name, ver):
    out = []; noint = 0
    for l in tracked_locks(repo, rev):
        if not in_scope(l): continue
        for k, e in json.loads(git_bytes(repo, rev, l)).get('packages', {}).items():
            if pkg_name(k) == name and e.get('version') == ver and not e.get('link'):
                if 'integrity' in e: out.append((l, k, e['integrity']))
                else: noint += 1
    return out, noint


def cmd_tarballs(repo, base, head, outdir, json_out):
    t = Tally()
    if os.path.exists(outdir) and os.listdir(outdir):
        print('REFUSED: %s exists and is not empty — give a FRESH directory (a reused download proves nothing)' % outdir); return 2
    os.makedirs(outdir, exist_ok=True)
    new_sri, old_sri, reg, nbytes = {}, {}, {}, {}
    try:
        for n, p in PLAN.items():
            meta = packument(n)
            for v in [p['new']] + p['old']:
                data = http_get(tgz_url(n, v)); fn = os.path.join(outdir, '%s-%s.tgz' % (n.replace('/', '_').lstrip('@'), v))
                open(fn, 'wb').write(data); s = sri_sha512(data); nbytes['%s@%s' % (n, v)] = len(data)
                (new_sri.__setitem__(n, s) if v == p['new'] else old_sri.setdefault(n, {}).__setitem__(v, s))
                reg[(n, v)] = meta['versions'][v]['dist'].get('integrity')
                print('DOWNLOADED %s %s %d bytes -> %s | sri %s... | registry dist.integrity %s...' % (n, v, len(data), fn, s[:30], (reg[(n, v)] or 'ABSENT')[:30]))
    except (urllib.error.URLError, OSError, KeyError, ValueError) as e:
        print('NETWORK FAILURE: %s — T1-T5 NOT RUN (never a pass)' % e); return 3
    t.check('T1', all(new_sri[n] == reg[(n, PLAN[n]['new'])] for n in PLAN), 'new tarballs sha512 == registry dist.integrity: %s' % dict((n, new_sri[n] == reg[(n, PLAN[n]['new'])]) for n in PLAN))
    t2 = {}; ok2 = True
    for n in PLAN:
        for v, s in old_sri[n].items():
            rows, noint = lock_integrities(repo, base, n, v)
            row = (s != new_sri[n], s == reg[(n, v)], len(rows), sum(1 for x in rows if x[2] == s), noint)
            t2['%s@%s' % (n, v)] = row
            ok2 &= row[0] and row[1] and row[2] == row[3] and (row[2] + row[4]) > 0
    t.check('T2', ok2, 'NEGATIVE CONTROL per old version (old!=new, old==registry, base entries WITH integrity, of them == the downloaded OLD sri, base entries WITHOUT integrity): %s' % t2)
    changed = []; resolved = []
    for l in [x for x in git(repo, 'diff', '--name-only', base, head).split('\n') if x.endswith('package-lock.json')]:
        hp = json.loads(git_bytes(repo, head, l)).get('packages', {}); bp = json.loads(git_bytes(repo, base, l)).get('packages', {})
        for k, e in hp.items():
            if k in bp and bp[k] != e and pkg_name(k) in PLAN:
                if 'integrity' in e: changed.append((l, k, e['integrity'] == new_sri[pkg_name(k)]))
                if 'resolved' in e: resolved.append((l, k, e['resolved'] == tgz_url(pkg_name(k), PLAN[pkg_name(k)]['new'])))
    mism = [c for c in changed if not c[2]]
    t.check('T3', changed and not mism, 'changed head entries carrying integrity: %d, == the DOWNLOADED sri: %d, mismatches %d %s' % (len(changed), len(changed) - len(mism), len(mism), mism[:3]))
    rb = [r for r in resolved if not r[2]]
    t.check('T4', resolved and not rb, 'changed head entries carrying resolved: %d, == the downloaded URL: %d %s' % (len(resolved), len(resolved) - len(rb), rb[:3]))
    t5 = dict((n, (new_sri[n] == PLAN[n]['integrity_ready'], old_sri[n].get(PLAN[n]['old'][0]) == PLAN[n]['integrity_old_ready'],
                   nbytes['%s@%s' % (n, PLAN[n]['new'])], PLAN[n]['tarball_bytes_ready'])) for n in PLAN)
    t.check('T5', all(a and b and c == d for a, b, c, d in t5.values()), 'the READY\'s FULL strings (new ==, old ==) and tarball bytes (measured, READY): %s' % t5)
    if json_out:
        json.dump({'new_sri': new_sri, 'old_sri': old_sri, 'bytes': nbytes, 'dir': outdir}, open(json_out, 'w'), indent=1); print('JSON %s' % json_out)
    return t.end()


def exact_empty(resp): return isinstance(resp, dict) and resp == {}


RELEASE = __import__('re').compile(r'^\d+\.\d+\.\d+$')
LRF = K['lock_relevant_fields']


def lock_fields(m):
    """the lock-relevant fields of a packument version, `dependencies` minus its optionalDependencies (as npm writes the lock)."""
    out = dict((k, m[k]) for k in LRF if k in m)
    if isinstance(out.get('dependencies'), dict) and isinstance(m.get('optionalDependencies'), dict):
        out['dependencies'] = dict((x, y) for x, y in out['dependencies'].items() if x not in m['optionalDependencies'])
    return out


def field_delta(a, b):
    """sorted 'field' or 'field/key' paths that differ between two lock-field dicts."""
    out = []
    for k in sorted(set(a) | set(b)):
        x, y = a.get(k), b.get(k)
        if isinstance(x, dict) and isinstance(y, dict):
            out += ['%s/%s' % (k, z) for z in sorted(set(x) | set(y)) if x.get(z) != y.get(z)]
        elif x != y: out.append(k)
    return out


def above(versions, floor):
    t = tuple(int(x) for x in floor.split('.'))
    return sorted((v for v in versions if RELEASE.match(v) and tuple(int(x) for x in v.split('.')) > t), key=lambda v: tuple(int(x) for x in v.split('.')))


def cmd_advisories(json_out):
    t = Tally(); three = K['three_ids']
    try:
        raw_new = bulk_advisories(dict((n, [p['new']]) for n, p in PLAN.items()))
        old = ids_of(bulk_advisories(dict((n, p['old']) for n, p in PLAN.items())))
        meta = dict((n, packument(n)) for n in PLAN)
    except (urllib.error.URLError, OSError, KeyError, ValueError) as e:
        print('NETWORK FAILURE: %s — A1-A5 NOT RUN (never a pass)' % e); return 3
    print('NEW versions -> %s' % json.dumps(raw_new)); print('OLD versions -> %s' % old)
    t.check('A1', exact_empty(raw_new), 'the new version(s) return %s (want exactly {})' % json.dumps(raw_new)[:200])
    rng = dict((i, old.get(i, (0, 0, 'ABSENT'))[2]) for i in three)
    t.check('A2', set(three) <= set(old) and all(rng[i] == PLAN[n]['vulnerable'] for n in PLAN for i in PLAN[n]['ghsas']),
            'CONTROL: the OLD version(s) return %s of the three, with ranges %s (kit %s); every id returned: %s' % (
                sorted(set(old) & set(three)), rng, dict((n, PLAN[n]['vulnerable']) for n in PLAN), sorted(old)))
    sv = dict((i, (old.get(i, (None, None))[1], sev)) for n in PLAN for i, sev in PLAN[n]['ghsas'].items())
    t.check('A3', all(a == b for a, b in sv.values()), 'severity measured vs kit %s' % sv)
    t.check('A4', all(old.get(i, (None,))[0] == n for n in PLAN for i in PLAN[n]['ghsas']), 'each id on its kit package %s' % dict((i, old.get(i, ('ABSENT',))[0]) for i in three))
    a5 = {}
    for n, p in PLAN.items():
        m = meta[n]; ab = above(m.get('versions', {}), p['old'][-1])
        fd = field_delta(lock_fields(m['versions'][p['old'][-1]]), lock_fields(m['versions'][p['new']]))
        a5[n] = {'latest': m.get('dist-tags', {}).get('latest'), 'above_old': ab, 'published': (m.get('time') or {}).get(p['new']),
                 'field_delta': fd, 'ok': m.get('dist-tags', {}).get('latest') == p['new'] and ab == [p['new']] and fd == p['field_delta_ready']}
        dn, do = m['versions'][p['new']].get('dependencies', {}), m['versions'][p['old'][-1]].get('dependencies', {})
        print('A5 %s: latest %s | release-shaped versions above %s: %s | %s published %s | lock-field delta %s | minimist %r -> %r' % (
            n, a5[n]['latest'], p['old'][-1], ab, p['new'], a5[n]['published'], fd, do.get('minimist'), dn.get('minimist')))
    t.check('A5', all(v['ok'] for v in a5.values()), 'VERSION FACTS: latest == new, the only release above old, field delta == kit %s: %s' % (
        dict((n, PLAN[n]['field_delta_ready']) for n in PLAN), dict((n, v['ok']) for n, v in a5.items())))
    if json_out: json.dump({'new': raw_new, 'old': old, 'a5': a5}, open(json_out, 'w'), indent=1)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(sri_sha512(b'') == 'sha512-z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXcg/SpIdNs6c5H0NE8XYXysP+DGNKHfuwvY7kxvUdBeoGlODJ6+SfaPg==', 'sri of the empty input == the published sha512 of ""')
    rep(sri_sha512(b'a') != sri_sha512(b'b'), 'PLANTED different bytes give a different sri')
    rep(ids_of({'x': [{'github_advisory_id': 'GHSA-1', 'severity': 'low', 'vulnerable_versions': '<1'}], 'y': [{'url': 'https://github.com/advisories/GHSA-2', 'severity': 'high'}]}) ==
        {'GHSA-1': ('x', 'low', '<1'), 'GHSA-2': ('y', 'high', None)}, 'advisory ids read from github_advisory_id OR the url tail')
    rep(PLAN['handlebars']['integrity_ready'] != PLAN['handlebars']['integrity_old_ready'], 'the READY\'s new and old strings differ (T5 cannot pass with one swapped for the other)')
    rep(exact_empty({}) and not exact_empty({'handlebars': []}) and not exact_empty({'x': [{'url': 'u/GHSA-9'}]}), 'A1 predicate: only exactly {} passes ({"handlebars": []} is not {})')
    rep(tgz_url('handlebars', '4.7.10') == 'https://registry.npmjs.org/handlebars/-/handlebars-4.7.10.tgz', 'tarball URL shape')
    vs = ['4.7.8', '4.7.9', '4.7.10', '4.0.0-alpha.1', '5.0.0-beta.1', '4.7.10-rc.1']
    rep(above(vs, '4.7.9') == ['4.7.10'], 'A5: only release-shaped versions above 4.7.9 count (pre-releases excluded): %s' % above(vs, '4.7.9'))
    rep(above(vs + ['4.7.11'], '4.7.9') == ['4.7.10', '4.7.11'], 'PLANTED a 4.7.11 release: A5 "only version above" FIRES')
    m9 = {'dependencies': {'minimist': '^1.2.5', 'uglify-js': '^3.1.4'}, 'optionalDependencies': {'uglify-js': '^3.1.4'}, 'engines': {'node': '>=0.4.7'}, 'license': 'MIT'}
    m10 = json.loads(json.dumps(m9)); m10['dependencies']['minimist'] = '^1.2.8'
    rep(field_delta(lock_fields(m9), lock_fields(m10)) == ['dependencies/minimist'], 'A5 field delta: minimist only (uglify-js subtracted from dependencies)')
    m11 = json.loads(json.dumps(m10)); m11['engines'] = {'node': '>=6'}
    rep(field_delta(lock_fields(m9), lock_fields(m11)) == ['dependencies/minimist', 'engines/node'], 'PLANTED an engines move: A5 field delta FIRES')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    try:
        if A[0] == 'tarballs':
            return cmd_tarballs(req(A, '--repo'), req(A, '--base', True), req(A, '--head', True), req(A, '--out'), opt(A, '--json-out'))
        if A[0] == 'advisories': return cmd_advisories(opt(A, '--json-out'))
    except SystemExit as e:
        print(e); return 2
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
