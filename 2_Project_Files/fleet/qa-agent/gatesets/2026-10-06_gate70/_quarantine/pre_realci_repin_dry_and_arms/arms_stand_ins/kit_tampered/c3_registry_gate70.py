#!/usr/bin/env python3
"""c3_registry_gate70.py — INTEGRITY FROM THE DOWNLOADED TARBALL, and the advisories, for #1397 (KS-1425). Network: registry.npmjs.org READS
only (tarball GETs, packument GETs, and the bulk-advisory query POST, which is the registry's read endpoint). Never npm.

  tarballs --repo R --head H [--base B] --out DIR [--json-out F]
     T1  each of the 4 FIXED tarballs (proxy-addr 2.0.8, source-map-js 1.2.2, postcss-selector-parser 7.1.6, smol-toml 1.9.0) is
         DOWNLOADED into DIR (a fresh mkdir, never reused), sha512'd here, and equals the registry packument's dist.integrity
     T2  NEGATIVE CONTROL: each OLD tarball (2.0.7, 1.2.1, 7.1.4, 1.8.0) is downloaded too; its sri != the fixed one, and == the
         integrity the BASE locks carry for the old version (so the instrument can tell two tarballs apart AND reads locks right)
     T3  every changed head entry that carries `integrity` equals the DOWNLOADED sri of its new version (0 mismatches over N)
     T4  in-repo POSITIVE control at the BASE: every lock that ALREADY pinned a fixed version (proxy-addr 2.0.8 x12 at drafting,
         postcss-selector-parser 7.1.6 in systemTest/akto) carries exactly the downloaded sri
     T5  the brief's quoted prefixes (kit plan integrity_prefix_brief) are prefixes of the downloaded sri (a third, written source)
     --json-out writes {"new_sri": {...}, "old_sri": {...}} for c2 diff --integrity-json (L4b).
  advisories [--json-out F]
     A1  bulk query of the 4 FIXED versions returns NONE of the 5 ids (the refresh clears them at the source)
     A2  CONTROL: the bulk query of the OLD versions returns jqcg / 68fv / rj75 / r4xh (the query can say yes)
     A3  the 2 baselined ids at their pinned versions (sprintf-js 1.0.3, postcss-selector-parser 6.1.4) are returned and their
         severity is NOT high / critical (no HIGH or CRITICAL is baselined); sprintf-js latest still affected (no fix exists)
     A4  the severities of the fixed ids match the kit (critical / high / moderate)
  --selftest   sri of known bytes, the prefix check, the mismatch / missing classification (no network).
rc 0 / 1 / 3 network failure (NOT RUN, never a pass)."""
import json, os, sys, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate70 import K, Tally, git, git_bytes, tracked_locks, in_scope, pkg_name, sri_sha512, http_get, bulk_advisories

PLAN = K['plan']


def tgz_url(name, ver): return 'https://registry.npmjs.org/%s/-/%s-%s.tgz' % (name, name.split('/')[-1], ver)


def lock_integrities(repo, rev, name, ver):
    out = []
    for l in tracked_locks(repo, rev):
        if not in_scope(l): continue
        for k, e in json.loads(git_bytes(repo, rev, l)).get('packages', {}).items():
            if pkg_name(k) == name and e.get('version') == ver and 'integrity' in e:
                out.append((l, k, e['integrity']))
    return out


def cmd_tarballs(repo, base, head, outdir, json_out):
    t = Tally()
    if os.path.exists(outdir) and os.listdir(outdir):
        print('REFUSED: %s exists and is not empty — give a FRESH directory (a reused download proves nothing)' % outdir); return 2
    os.makedirs(outdir, exist_ok=True)
    new_sri, old_sri, reg = {}, {}, {}
    try:
        for n, p in PLAN.items():
            meta = json.loads(http_get('https://registry.npmjs.org/%s' % n))
            for which, v, store in (('new', p['new'], new_sri), ('old', p['old'], old_sri)):
                data = http_get(tgz_url(n, v)); fn = os.path.join(outdir, '%s-%s.tgz' % (n.replace('/', '_'), v))
                open(fn, 'wb').write(data); store[n] = sri_sha512(data)
                reg[(n, v)] = meta['versions'][v]['dist'].get('integrity')
                print('DOWNLOADED %s %s %d bytes -> %s | sri %s... | registry dist.integrity %s...' % (n, v, len(data), fn, store[n][:30], (reg[(n, v)] or 'ABSENT')[:30]))
    except (urllib.error.URLError, OSError, KeyError, ValueError) as e:
        print('NETWORK FAILURE: %s — T1-T5 NOT RUN (never a pass)' % e); return 3
    t.check('T1', all(new_sri[n] == reg[(n, PLAN[n]['new'])] for n in PLAN), 'fixed tarballs sha512 == registry dist.integrity: %s' % dict((n, new_sri[n] == reg[(n, PLAN[n]['new'])]) for n in PLAN))
    base_old = dict((n, lock_integrities(repo, base, n, PLAN[n]['old'])) for n in PLAN)
    t2 = dict((n, (old_sri[n] != new_sri[n], old_sri[n] == reg[(n, PLAN[n]['old'])], len(base_old[n]), sum(1 for x in base_old[n] if x[2] == old_sri[n]))) for n in PLAN)
    t.check('T2', all(a and b and c > 0 and c == d for (a, b, c, d) in t2.values()),
            'NEGATIVE CONTROL old != new / old == registry / base-lock old entries with integrity / of them == the downloaded OLD sri: %s' % t2)
    changed = []
    for l in [x for x in git(repo, 'diff', '--name-only', base, head).split('\n') if x.endswith('package-lock.json')]:
        hp = json.loads(git_bytes(repo, head, l)).get('packages', {}); bp = json.loads(git_bytes(repo, base, l)).get('packages', {})
        for k, e in hp.items():
            if k in bp and bp[k] != e and pkg_name(k) in PLAN and 'integrity' in e:
                changed.append((l, k, e['integrity'] == new_sri[pkg_name(k)]))
    mism = [c for c in changed if not c[2]]
    t.check('T3', changed and not mism, 'changed head entries carrying integrity: %d, == the DOWNLOADED sri: %d, mismatches %d %s' % (len(changed), len(changed) - len(mism), len(mism), mism[:3]))
    pos = dict((n, lock_integrities(repo, base, n, PLAN[n]['new'])) for n in PLAN)
    pbad = [(n, l) for n, rows in pos.items() for (l, k, s) in rows if s != new_sri[n]]
    t.check('T4', sum(len(v) for v in pos.values()) > 0 and not pbad, 'IN-REPO POSITIVE CONTROL at the base: entries already at the fixed version %s, mismatches %d %s' % (
        dict((n, len(v)) for n, v in pos.items()), len(pbad), pbad[:3]))
    t.check('T5', all(new_sri[n].startswith(PLAN[n]['integrity_prefix_brief']) for n in PLAN), 'the brief\'s quoted prefixes match: %s' % dict((n, new_sri[n].startswith(PLAN[n]['integrity_prefix_brief'])) for n in PLAN))
    if json_out:
        json.dump({'new_sri': new_sri, 'old_sri': old_sri, 'dir': outdir}, open(json_out, 'w'), indent=1); print('JSON %s' % json_out)
    return t.end()


def ids_of(resp):
    out = {}
    for pkg, advs in resp.items():
        for a in advs:
            gid = a.get('github_advisory_id') or (a.get('url') or '').rsplit('/', 1)[-1]
            out[gid] = (pkg, a.get('severity'), a.get('vulnerable_versions'))
    return out


def cmd_advisories(json_out):
    t = Tally(); five = set(K['five_ids'])
    try:
        fixed = ids_of(bulk_advisories(dict((n, [p['new']]) for n, p in PLAN.items())))
        old = ids_of(bulk_advisories(dict((n, [p['old']]) for n, p in PLAN.items())))
        bl = ids_of(bulk_advisories(dict((r['package'], [r['pinned']]) for r in K['baseline']['new_rows'].values())))
        latest = json.loads(http_get('https://registry.npmjs.org/sprintf-js'))['dist-tags']['latest']
        lat = ids_of(bulk_advisories({'sprintf-js': [latest]}))
    except (urllib.error.URLError, OSError, KeyError, ValueError) as e:
        print('NETWORK FAILURE: %s — A1-A4 NOT RUN (never a pass)' % e); return 3
    print('FIXED versions -> %s' % fixed); print('OLD versions -> %s' % old); print('BASELINED pins -> %s' % bl); print('sprintf-js latest %s -> %s' % (latest, lat))
    t.check('A1', not (set(fixed) & five), 'the 4 fixed versions return %d of the five ids %s' % (len(set(fixed) & five), sorted(set(fixed) & five)))
    want_old = set(K['fixed_ids']) | {PLAN['postcss-selector-parser']['ghsa']}
    t.check('A2', want_old <= set(old), 'CONTROL: the OLD versions return %s (want %s)' % (sorted(set(old) & five), sorted(want_old)))
    sev = dict((i, bl[i][1]) for i in K['baseline']['new_rows'] if i in bl)
    t.check('A3', len(sev) == 2 and not any(s in ('high', 'critical') for s in sev.values()) and 'GHSA-hp3w-g68c-fv3c' in lat,
            'baselined ids returned at their pins with severity %s (no high/critical) | sprintf-js latest %s still affected: %s' % (sev, latest, 'GHSA-hp3w-g68c-fv3c' in lat))
    sv = dict((PLAN[n]['ghsa'], (old.get(PLAN[n]['ghsa'], (None, None))[1], PLAN[n]['severity'])) for n in PLAN)
    t.check('A4', all(a == b for a, b in sv.values()), 'severity measured vs kit %s' % sv)
    if json_out: json.dump({'fixed': fixed, 'old': old, 'baselined': bl}, open(json_out, 'w'), indent=1)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(sri_sha512(b'') == 'sha512-z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXcg/SpIdNs6c5H0NE8XYXysP+DGNKHfuwvY7kxvUdBeoGlODJ6+SfaPg==', 'sri of the empty input == the published sha512 of ""')
    rep(sri_sha512(b'a') != sri_sha512(b'b'), 'PLANTED different bytes give a different sri')
    rep(ids_of({'x': [{'github_advisory_id': 'GHSA-1', 'severity': 'low', 'vulnerable_versions': '<1'}], 'y': [{'url': 'https://github.com/advisories/GHSA-2', 'severity': 'high'}]}) ==
        {'GHSA-1': ('x', 'low', '<1'), 'GHSA-2': ('y', 'high', None)}, 'advisory ids read from github_advisory_id OR the url tail')
    rep(not 'sha512-AAAA'.startswith(PLAN['proxy-addr']['integrity_prefix_brief']), 'PLANTED bogus sri does not carry the brief prefix')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    if A[0] == 'tarballs':
        if not opt('--out'): print('REFUSED: --out <fresh dir> required'); return 2
        return cmd_tarballs(opt('--repo'), opt('--base', K['pr']['parents'][0]), opt('--head', K['pr']['head_expected']), opt('--out'), opt('--json-out'))
    if A[0] == 'advisories': return cmd_advisories(opt('--json-out'))
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
