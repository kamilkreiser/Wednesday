#!/usr/bin/env python3
"""c3_integrity_gate58.py — gate58 C3: recompute the integrity of the FIVE new tarballs FROM THE REGISTRY BYTES (public npm registry,
read-only HTTPS GETs; tarballs hashed in memory, never written) and match every lock at --head that carries them.
`npm ci --dry-run` returns rc 0 on a lock with a bogus integrity (B 56th, measured): leg 2 is NOT integrity evidence; this is.
  I1 per package (browserslist 4.28.7, postcss-selector-parser 6.1.4, caniuse-lite 1.0.30001814, electron-to-chromium 1.5.444,
     node-releases 2.0.57): sha512(tarball) base64 == kit integrity == the registry's dist.integrity; dist.tarball == kit resolved;
     second instrument: sha1(tarball) == dist.shasum.
  I2 NEGATIVE CONTROL per package, same instrument: the OLD version's tarball (kit neg_control: the base ROOT lock's version) hashes to
     ITS OWN registry integrity and NOT to the new one; one flipped byte of the new tarball changes its sha512.
  I3 every tracked package-lock.json at --head: every entry of those five packages AT THE NEW VERSION carries integrity == the
     RECOMPUTED value and resolved == the registry tarball (an entry at the new version with no integrity FAILS). Count printed.
  I4 the 23 ruled entries (kit locks.*.expected_changes) are at the new version at --head (at the BASE this FIRES: every one is old).
--plant <pkg>: in memory, give that package's ruled entries in every ruled lock the OLD version's integrity before I3/I4 (a planted
wrong edit: must FAIL naming them). Nothing is written.
Usage: c3_integrity_gate58.py --repo <clone> --head <sha> [--plant <pkg>]   (rc 0 PASS / 1 FAIL / 2 usage / 3 network)"""
import json, sys, os, hashlib, base64, urllib.request, urllib.error, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate58 import K, git, commit, show, now, Checks, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--head' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
REPO = opt('--repo'); H = commit(REPO, opt('--head')); PLANT = opt('--plant'); PK = K['packages']
if PLANT and PLANT not in PK: print('REFUSING: --plant must be one of %s' % sorted(PK)); raise SystemExit(2)
REG = 'https://registry.npmjs.org/'


def fetch(url):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={'Accept': '*/*'}), timeout=120).read()
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            print('RETRY %d %s: %s' % (i + 1, url, e), file=sys.stderr); time.sleep(5)
    print('NETWORK: %s unreachable after 3 tries' % url); raise SystemExit(3)


def sri(b): return 'sha512-' + base64.b64encode(hashlib.sha512(b).digest()).decode()


print('c3_integrity_gate58 %s | repo %s | head %s | registry %s%s' % (now(), REPO, H, REG, (' | PLANT: %s carries the OLD integrity in memory' % PLANT) if PLANT else ''))
C = Checks(); calc = {}
for n, P in sorted(PK.items()):
    to, old = P['to'], P['neg_control']
    out = {}
    for v in (to, old):
        d = json.loads(fetch(REG + n + '/' + v))['dist']; tb = fetch(d['tarball']); s5 = sri(tb); s1 = hashlib.sha1(tb).hexdigest()
        out[v] = (d, tb, s5, s1)
        print('INFO %s@%s tarball %s | %d bytes | sha512 %s | sha1 %s' % (n, v, d['tarball'], len(tb), s5, s1))
    d, tb, s5, s1 = out[to]; calc[n] = s5
    C.chk('I1 %s@%s' % (n, to), s5 == P['integrity'][to] == d.get('integrity') and d['tarball'] == P['resolved'][to] and s1 == d.get('shasum'),
          'recomputed == kit %s | == registry dist.integrity %s | dist.tarball == kit resolved %s | sha1 == dist.shasum %s' % (
              s5 == P['integrity'][to], s5 == d.get('integrity'), d['tarball'] == P['resolved'][to], s1 == d.get('shasum')))
    od, otb, os5, _ = out[old]; flip = bytearray(tb); flip[len(flip) // 2] ^= 0x01
    C.chk('I2 %s negative control' % n, os5 == od.get('integrity') == P['integrity'][old] and os5 != s5 and sri(bytes(flip)) != s5,
          'OLD %s tarball hashes to its OWN registry integrity %s | and NOT to %s\'s %s | one flipped byte of the %s tarball changes its sha512 %s' % (
              old, os5 == od.get('integrity'), to, os5 != s5, to, sri(bytes(flip)) != s5))

locks = sorted(l.split('\t')[1] for l in git(REPO, 'ls-tree', '-r', H).splitlines() if l.split('\t')[1].endswith('package-lock.json'))
seen = {n: 0 for n in PK}; bad = []; ruled_bad = []
for lp in locks:
    t = show(REPO, H, lp)
    try: pk = json.loads(t).get('packages', {})
    except ValueError: bad.append((lp, 'UNPARSEABLE')); continue
    if PLANT and lp in K['locks']:
        for key in K['locks'][lp]['expected_changes']:
            if key.rsplit('node_modules/', 1)[-1] == PLANT and key in pk: pk[key] = dict(pk[key], integrity=PK[PLANT]['integrity'][PK[PLANT]['neg_control']])
    for k, v in pk.items():
        n = k.rsplit('node_modules/', 1)[-1]
        if n in PK and v.get('version') == PK[n]['to']:
            seen[n] += 1
            if v.get('integrity') != calc[n] or v.get('resolved') != PK[n]['resolved'][PK[n]['to']]:
                bad.append((lp.replace('Blockchain/Dev/', ''), k, 'integrity %s' % ('ABSENT' if 'integrity' not in v else ('== recomputed' if v['integrity'] == calc[n] else 'MISMATCH')),
                            'resolved %s' % ('== registry' if v.get('resolved') == PK[n]['resolved'][PK[n]['to']] else v.get('resolved'))))
    if lp in K['locks']:
        for key, e in K['locks'][lp]['expected_changes'].items():
            if pk.get(key, {}).get('version') != e['to']: ruled_bad.append((lp.replace('Blockchain/Dev/', ''), key.rsplit('node_modules/', 1)[-1], pk.get(key, {}).get('version')))
C.chk('I3 every lock at head', not bad, '%d tracked locks read | entries at the new version per package %s | mismatched %d %s' % (len(locks), json.dumps(seen), len(bad), bad[:4]))
C.chk('I4 the 23 ruled entries at the new version', not ruled_bad, 'ruled entries NOT at the kit version: %d %s' % (len(ruled_bad), ruled_bad[:5]))
n = C.nfail()
print('INTEGRITY %s: %d FAIL of %d checks | head %s | 5 tarballs recomputed' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), H[:12]))
raise SystemExit(1 if n else 0)
