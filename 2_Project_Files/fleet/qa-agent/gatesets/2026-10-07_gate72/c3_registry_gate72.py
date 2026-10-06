#!/usr/bin/env python3
"""c3_registry_gate72.py — INTEGRITY FROM THE DOWNLOADED TARBALL, and the advisories, for #1406 (KS-1437). Carried from
c3_registry_gate70.py; [g72] marks changes. Network: registry.npmjs.org READS only (tarball GETs, packument GETs, and the bulk-advisory
query POST — leg 7's own instrument). Never npm. Tarballs are untrusted DATA: written to a FRESH dir, hashed, never unpacked here.

  tarballs --repo R --head H --base B --out DIR [--json-out F]          (REQUIRED: --repo --head --base --out)
     T1  each NEW tarball (shell-quote 1.11.0, sdk 1.31.0, pbkdf2 3.1.7) DOWNLOADED, sha512'd HERE == the packument's dist.integrity
     T2  NEGATIVE CONTROL: each OLD tarball (shell-quote 1.9.0, sdk 1.29.0, pbkdf2 3.1.5 + 3.1.6) is downloaded too; its sri != the new
         one, == its own dist.integrity, and == every integrity the BASE locks carry for that old version (> 0 such entries where the
         base carries integrity at all; the root lock carries none — reported, not counted)
     T3  every changed head entry that carries `integrity` == the DOWNLOADED sri of its new version (0 mismatches over N > 0)
     T4  [g72] RESOLVED: every changed head entry carrying `resolved` == the tarball URL actually downloaded
     T5  the READY's quoted prefixes (kit plan integrity_prefix_ready) are prefixes of the downloaded sri (a third, written source)
     --json-out writes {"new_sri", "old_sri", "dir"} for c2 diff --integrity-json (L4b).
  advisories [--json-out F]
     A1  bulk query of the 3 NEW versions returns {} exactly (no advisory at all, not only "none of the three")
     A2  CONTROL: the OLD versions return pqg4 / 6qxp / 477h (the query can say yes), with the kit's vulnerable ranges
     A3  severities measured == kit (critical / high / moderate)
     A4  [g72] the three ids are each returned for EXACTLY the package the kit names (no id moved package)
     A5  [g72] MOBILE CLAIM (commit body: "1.8.3, below the advisory's 1.8.4 floor, so it is not vulnerable to this one either"): the
         query of shell-quote 1.8.3 does NOT return pqg4 (the sentence's literal claim) — and every OTHER id it returns is PRINTED with
         severity (drafter, 21:08Z: GHSA-w7jw-789q-3m8p critical, GHSA-395f-4hp3-45gv high). INFO for the gate to rule, never a pass of
         "mobile is safe".
  --selftest   sri of known bytes, the prefix check, the id reader, the A1 exact-{} predicate (no network).
rc 0 / 1 / 2 refused / 3 network failure (NOT RUN, never a pass)."""
import json, os, sys, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate72 import (K, Tally, git, git_bytes, tracked_locks, in_scope, pkg_name, sri_sha512, http_get, bulk_advisories, ids_of,
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
    new_sri, old_sri, reg = {}, {}, {}
    try:
        for n, p in PLAN.items():
            meta = packument(n)
            for v in [p['new']] + p['old']:
                data = http_get(tgz_url(n, v)); fn = os.path.join(outdir, '%s-%s.tgz' % (n.replace('/', '_').lstrip('@'), v))
                open(fn, 'wb').write(data); s = sri_sha512(data)
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
    t.check('T5', all(new_sri[n].startswith(PLAN[n]['integrity_prefix_ready']) for n in PLAN), 'the READY\'s quoted prefixes match: %s' % dict((n, new_sri[n].startswith(PLAN[n]['integrity_prefix_ready'])) for n in PLAN))
    if json_out:
        json.dump({'new_sri': new_sri, 'old_sri': old_sri, 'dir': outdir}, open(json_out, 'w'), indent=1); print('JSON %s' % json_out)
    return t.end()


def exact_empty(resp): return isinstance(resp, dict) and resp == {}


def cmd_advisories(json_out):
    t = Tally(); three = K['three_ids']
    try:
        raw_new = bulk_advisories(dict((n, [p['new']]) for n, p in PLAN.items()))
        old = ids_of(bulk_advisories(dict((n, p['old']) for n, p in PLAN.items())))
        mob = ids_of(bulk_advisories({'shell-quote': [K['mobile_shell_quote']['pinned']]}))
    except (urllib.error.URLError, OSError, KeyError, ValueError) as e:
        print('NETWORK FAILURE: %s — A1-A5 NOT RUN (never a pass)' % e); return 3
    print('NEW versions -> %s' % json.dumps(raw_new)); print('OLD versions -> %s' % old); print('MOBILE shell-quote %s -> %s' % (K['mobile_shell_quote']['pinned'], mob))
    t.check('A1', exact_empty(raw_new), 'the 3 new versions return %s (want exactly {})' % json.dumps(raw_new)[:200])
    t.check('A2', set(three) <= set(old) and all(old[PLAN[n]['ghsa']][2] == PLAN[n]['vulnerable'] for n in PLAN),
            'CONTROL: the OLD versions return %s with ranges %s' % (sorted(set(old) & set(three)), dict((i, old.get(i, (0, 0, 'ABSENT'))[2]) for i in three)))
    sv = dict((PLAN[n]['ghsa'], (old.get(PLAN[n]['ghsa'], (None, None))[1], PLAN[n]['severity'])) for n in PLAN)
    t.check('A3', all(a == b for a, b in sv.values()), 'severity measured vs kit %s' % sv)
    t.check('A4', all(old.get(PLAN[n]['ghsa'], (None,))[0] == n for n in PLAN), 'each id on its kit package %s' % dict((PLAN[n]['ghsa'], old.get(PLAN[n]['ghsa'], ('ABSENT',))[0]) for n in PLAN))
    others = dict((i, v[1]) for i, v in mob.items() if i not in three)
    t.check('A5', K['plan']['shell-quote']['ghsa'] not in mob, 'MOBILE shell-quote %s: pqg4 returned %s (want False: the literal claim) | OTHER ids it IS affected by: %s — RULE the commit-body sentence' % (
        K['mobile_shell_quote']['pinned'], K['plan']['shell-quote']['ghsa'] in mob, others or 'none'))
    if json_out: json.dump({'new': raw_new, 'old': old, 'mobile': mob}, open(json_out, 'w'), indent=1)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(sri_sha512(b'') == 'sha512-z4PhNX7vuL3xVChQ1m2AB9Yg5AULVxXcg/SpIdNs6c5H0NE8XYXysP+DGNKHfuwvY7kxvUdBeoGlODJ6+SfaPg==', 'sri of the empty input == the published sha512 of ""')
    rep(sri_sha512(b'a') != sri_sha512(b'b'), 'PLANTED different bytes give a different sri')
    rep(ids_of({'x': [{'github_advisory_id': 'GHSA-1', 'severity': 'low', 'vulnerable_versions': '<1'}], 'y': [{'url': 'https://github.com/advisories/GHSA-2', 'severity': 'high'}]}) ==
        {'GHSA-1': ('x', 'low', '<1'), 'GHSA-2': ('y', 'high', None)}, 'advisory ids read from github_advisory_id OR the url tail')
    rep(not 'sha512-AAAA'.startswith(PLAN['pbkdf2']['integrity_prefix_ready']), 'PLANTED bogus sri does not carry the READY prefix')
    rep(exact_empty({}) and not exact_empty({'pbkdf2': []}) and not exact_empty({'x': [{'url': 'u/GHSA-9'}]}), 'A1 predicate: only exactly {} passes ({"pbkdf2": []} is not {})')
    rep(tgz_url('@modelcontextprotocol/sdk', '1.31.0') == 'https://registry.npmjs.org/@modelcontextprotocol/sdk/-/sdk-1.31.0.tgz', 'scoped tarball URL shape')
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
