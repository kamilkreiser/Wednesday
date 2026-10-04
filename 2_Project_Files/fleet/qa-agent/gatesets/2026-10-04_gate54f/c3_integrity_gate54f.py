#!/usr/bin/env python3
"""c3_integrity_gate54f.py — gate54f C3: recompute http-cache-semantics' integrity FROM THE REGISTRY TARBALLS ITSELF (public npm registry,
read-only HTTPS GETs; tarballs are hashed in memory and never written), and match the locks at --head against it.
  I1 4.3.0: sha512(tarball bytes) base64 == kit integrity 4.3.0 == the registry packument's dist.integrity; dist.tarball == kit resolved;
     second instrument: sha1(tarball) == dist.shasum.
  I2 4.2.0: the same, against kit integrity 4.2.0 (the base value).
  I3 NEGATIVE CONTROL, same instrument: sha512(4.2.0) != sha512(4.3.0); one flipped byte of the 4.3.0 tarball gives a different sha512.
  I4 the locks at --head: each lock's node_modules/http-cache-semantics: version == 4.3.0 AND integrity == the RECOMPUTED 4.3.0 value
     (and != the recomputed 4.2.0 value). The root lock's base entry carries no integrity: an ABSENT integrity there is reported, and
     PASSES only with version 4.3.0 (a doubt for the gate to rule — README D1). At the base SHA this check FIRES: every lock reads 4.2.0.
  --advisories (optional, the drafter's C5 prediction): ONE POST to the registry's bulk advisory endpoint (a query; it writes nothing)
     with the versions of http-cache-semantics, braces and node-forge pinned in every tracked package-lock.json at --head; reports which of
     the three kit advisories match which version. Expectation at the base: all three match; ch52 matches 4.2.0 and NOT 4.3.0.
Usage: c3_integrity_gate54f.py --repo <clone> --head <sha> [--advisories]   (rc 0 PASS / 1 FAIL / 2 usage / 3 network)"""
import json, sys, os, hashlib, base64, urllib.request, urllib.error, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54f import K, git, commit, show, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--head' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); H = commit(REPO, opt('--head')); PKG = K['pkg']; FROM, TO = K['from_version'], K['to_version']
REG = 'https://registry.npmjs.org/'


def fetch(url, data=None):
    for i in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers={'Accept': 'application/json', 'Content-Type': 'application/json'} if data else {'Accept': '*/*'})
            return urllib.request.urlopen(req, timeout=60).read()
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            print('RETRY %d %s: %s' % (i + 1, url, e), file=sys.stderr); time.sleep(5)
    print('NETWORK: %s unreachable after 3 tries' % url); raise SystemExit(3)


def sri(b): return 'sha512-' + base64.b64encode(hashlib.sha512(b).digest()).decode()


print('c3_integrity_gate54f %s | repo %s | head %s | registry %s' % (now(), REPO, H, REG))
C = Checks()
meta = json.loads(fetch(REG + PKG)); V = meta['versions']
calc = {}
for v in (FROM, TO):
    d = V[v]['dist']; tb = fetch(d['tarball']); calc[v] = sri(tb); s1 = hashlib.sha1(tb).hexdigest()
    print('INFO %s@%s tarball %s | %d bytes | sha512 %s | sha1 %s' % (PKG, v, d['tarball'], len(tb), calc[v], s1))
    C.chk('I%s %s' % ('1' if v == TO else '2', v), calc[v] == K['integrity'][v] == d.get('integrity') and d['tarball'] == K['resolved'][v] and s1 == d.get('shasum'),
          'recomputed == kit (builder) %s | == registry dist.integrity %s | dist.tarball == kit resolved %s | sha1 == dist.shasum %s' % (
              calc[v] == K['integrity'][v], calc[v] == d.get('integrity'), d['tarball'] == K['resolved'][v], s1 == d.get('shasum')))
    if v == TO: tb43 = tb
flip = bytearray(tb43); flip[len(flip) // 2] ^= 0x01
C.chk('I3 negative control', calc[FROM] != calc[TO] and sri(bytes(flip)) != calc[TO],
      'sha512(%s) != sha512(%s): %s | one flipped byte of the %s tarball changes its sha512: %s (the instrument can say NO)' % (FROM, TO, calc[FROM] != calc[TO], TO, sri(bytes(flip)) != calc[TO]))
for path, cfg in sorted(K['locks'].items()):
    e = json.loads(show(REPO, H, path))['packages'].get(K['bump_key'], {}); i = e.get('integrity')
    which = 'ABSENT' if i is None else (TO if i == calc[TO] else (FROM if i == calc[FROM] else 'NEITHER'))
    ok = e.get('version') == TO and (which == TO or (which == 'ABSENT' and cfg['role'] == 'root'))
    C.chk('I4 %s' % path.replace('Blockchain/Dev/', ''), ok, 'version %s | integrity matches the recomputed %s%s' % (
        e.get('version'), which, ' (root lock: stripped entry, README D1)' if which == 'ABSENT' else ''))

if '--advisories' in A:
    want = {PKG: set(), 'braces': set(), 'node-forge': set()}; where = {}
    locks = [l.split('\t')[1] for l in git(REPO, 'ls-tree', '-r', H).splitlines() if l.split('\t')[1].endswith('package-lock.json')]
    for lp in locks:
        try: pk = json.loads(show(REPO, H, lp)).get('packages', {})
        except ValueError: continue
        for k, v in pk.items():
            n = k.rsplit('node_modules/', 1)[-1]
            if n in want and v.get('version'): want[n].add(v['version']); where.setdefault((n, v['version']), set()).add(lp)
    q = {n: sorted(vs | ({FROM, TO} if n == PKG else set())) for n, vs in want.items()}
    print('INFO advisory query over %d tracked locks at %s: %s' % (len(locks), H[:12], json.dumps(q)))
    adv = json.loads(fetch(REG + '-/npm/v1/security/advisories/bulk', json.dumps(q).encode()))
    hits = {}
    for n, lst in adv.items():
        for a in lst:
            gid = str(a.get('url', '')).rstrip('/').split('/')[-1]
            print('INFO advisory %s on %s range %r severity %s' % (gid, n, a.get('vulnerable_versions'), a.get('severity')))
            hits.setdefault(gid, (n, a.get('vulnerable_versions')))
    for gid in sorted(K['advisories']):
        print('ADVISORY %s %s | %s' % (gid, 'MATCHED' if gid in hits else 'NOT MATCHED', hits.get(gid, ('-', '-'))))
    import re
    def inr(v, rng):  # tiny semver-range reader for the forms the registry returns (`<x`, `<=x`, `>=x <y`, `||`); NOT a full semver
        t = lambda s: tuple(int(p) for p in s.split('-')[0].split('.'))
        for alt in rng.split('||'):
            ok = True
            for op, ver in re.findall(r'(<=|>=|<|>|=)?\s*(\d+\.\d+\.\d+[^\s]*)', alt):
                a, b = t(v), t(ver)
                ok &= {'<': a < b, '<=': a <= b, '>': a > b, '>=': a >= b, '=': a == b, '': a == b}[op]
            if ok: return True
        return False
    ch = K['forbidden_row']
    if ch in hits:
        r = hits[ch][1]; print('INFO %s range %r: %s in range %s | %s in range %s' % (ch, r, FROM, inr(FROM, r), TO, inr(TO, r)))
        C.chk('IA ch52 vs the bump', inr(FROM, r) and not inr(TO, r), '%s@%s vulnerable %s, @%s vulnerable %s' % (PKG, FROM, inr(FROM, r), TO, inr(TO, r)))
    else:
        C.chk('IA ch52 vs the bump', False, '%s did not come back from the bulk query' % ch)
    for gid in ('GHSA-vfj7-8cjw-p6xm', 'GHSA-86w9-cpqp-85rv'):
        if gid in hits:
            n, r = hits[gid]; vul = sorted(v for v in want[n] if inr(v, r))
            print('INFO %s %s range %r: pinned versions in range %s, locks %s' % (gid, n, r, vul, sorted(set().union(*[where.get((n, v), set()) for v in vul])) if vul else []))
n = C.nfail()
print('INTEGRITY %s: %d FAIL of %d checks | head %s | 4.3.0 %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), H[:12], calc[TO]))
raise SystemExit(1 if n else 0)
