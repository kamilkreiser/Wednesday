#!/usr/bin/env python3
"""c2_integrity_gateD2.py — gateD2 C2: RECOMPUTE the added packages' integrity FROM THE REGISTRY TARBALLS (public npm registry, read-only HTTPS
GETs; tarballs are hashed in memory and never written) and match both locks at --head (a NEW COPY of gate54f's c3_integrity, re-keyed).
  I1 for each kit integrity_pkgs name@version: sha512(tarball) as SRI == the registry packument's dist.integrity; dist.tarball == the lock's
     `resolved`; second instrument sha1(tarball) == dist.shasum.
  I2 every ADDED entry of every kit lock at --head (root 5, service 7): `integrity` == the RECOMPUTED value and `resolved` == dist.tarball.
     kit integrity_required (pkijs, asn1js) must be present in BOTH locks.
  I3 NEGATIVE CONTROL, same instrument: one flipped byte of the pkijs tarball changes its sha512; pkijs 3.4.0's dist.integrity != 3.4.1's.
  At the BASE sha I2 FIRES: no lock carries the added entries (base-vs-base reading).
Usage: c2_integrity_gateD2.py --repo <clone> --head <sha>   (rc 0 PASS / 1 FAIL / 2 usage / 3 network)"""
import json, sys, os, hashlib, base64, urllib.request, urllib.error, time, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, commit, show, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--head' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); H = commit(REPO, opt('--head')); REG = K['registry']


def fetch(url):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={'Accept': '*/*'}), timeout=60).read()
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            print('RETRY %d %s: %s' % (i + 1, url, e), file=sys.stderr); time.sleep(5)
    print('NETWORK: %s unreachable after 3 tries' % url); raise SystemExit(3)


def sri(b): return 'sha512-' + base64.b64encode(hashlib.sha512(b).digest()).decode()


print('c2_integrity_gateD2 %s | repo %s | head %s | registry %s' % (now(), REPO, H, REG))
C = Checks(); calc = {}; dist = {}; tb_pk = None
for name, v in sorted(K['integrity_pkgs'].items()):
    meta = json.loads(fetch(REG + urllib.parse.quote(name, safe='@')))
    d = meta['versions'][v]['dist']; tb = fetch(d['tarball']); calc[name] = sri(tb); dist[name] = d; s1 = hashlib.sha1(tb).hexdigest()
    if name == 'pkijs':
        tb_pk = tb; other = meta['versions'].get('3.4.0', {}).get('dist', {}).get('integrity')
    print('INFO %s@%s tarball %s | %d bytes | sha512 %s | sha1 %s' % (name, v, d['tarball'], len(tb), calc[name], s1))
    C.chk('I1 %s@%s' % (name, v), calc[name] == d.get('integrity') and s1 == d.get('shasum'), 'recomputed == registry dist.integrity %s | sha1 == dist.shasum %s' % (calc[name] == d.get('integrity'), s1 == d.get('shasum')))
for path, cfg in sorted(K['locks'].items()):
    pk = json.loads(show(REPO, H, path) or '{"packages": {}}')['packages']; bad = []; seen = []
    for key, v in sorted(cfg['added'].items()):
        nm = key.split('node_modules/', 1)[-1]; e = pk.get(key)
        if e is None: bad.append((nm, 'ABSENT')); continue
        seen.append(nm)
        if e.get('integrity') != calc.get(nm): bad.append((nm, 'integrity %s' % ('== recomputed' if e.get('integrity') == calc.get(nm) else 'OTHER ' + str(e.get('integrity'))[:24])))
        if e.get('resolved') != dist.get(nm, {}).get('tarball'): bad.append((nm, 'resolved %s' % e.get('resolved')))
    req = [r for r in K['integrity_required'] if r not in seen]
    C.chk('I2 %s' % path.replace('Blockchain/Dev/', ''), not bad and not req, '%d added entries matched against the recomputed tarballs | problems %s | required %s missing %s' % (len(seen), bad or 'NONE', K['integrity_required'], req or 'NONE'))
flip = bytearray(tb_pk); flip[len(flip) // 2] ^= 0x01
C.chk('I3 negative control', sri(bytes(flip)) != calc['pkijs'] and other is not None and other != calc['pkijs'], 'a flipped byte changes pkijs sha512: %s | pkijs 3.4.0 dist.integrity %s != 3.4.1 recomputed: %s' % (
    sri(bytes(flip)) != calc['pkijs'], str(other)[:24], other != calc['pkijs']))
n = C.nfail()
print('INTEGRITY %s: %d FAIL of %d checks | head %s | pkijs %s | asn1js %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), H[:12], calc['pkijs'][:30], calc['asn1js'][:30]))
raise SystemExit(1 if n else 0)
