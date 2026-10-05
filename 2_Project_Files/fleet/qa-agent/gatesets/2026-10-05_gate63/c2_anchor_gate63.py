#!/usr/bin/env python3
"""c2_anchor_gate63.py — C2 THE ANCHOR FILE for #1388 (Wednesday's Q-SCOPE ruling, checked by TWO independent instruments:
a Python PEM/DER reader and the openssl binary). READ verbs only in the repo; fixtures go to $G63_SCRATCH/fixtures.

  A1  certificate count in config/tsa-trust-anchors-dtrust.crt == 1 (python PEM blocks AND `openssl storeutl -certs` agree);
      CONTROL the two-root bundle counts 2 on both instruments
  A2  its DER sha256 == 4d24807b9cad5110f40ed79d934346d7c9b0290431dc9b11a40bbb86fcf2aef6 (python) AND openssl's SHA-256
      fingerprint agrees
  A3  the file is BYTE-EQUAL to PEM block 1 of the committed bundle config/tsa-trust-anchors.crt (at the SAME tree), and the
      bundle itself is byte-identical at base and head (no new trust smuggled into the bundle); CONTROL block 2 differs
  A4  DigiCert ABSENT: the DigiCert Assured ID Root CA DER sha256 (3e9099b5…) is not in the file, and openssl's subject and
      issuer name no DigiCert; CONTROL the same scan finds DigiCert in the bundle
  A5  openssl: subject CN == D-TRUST Root CA 1 2017, self-signed (subject == issuer), notAfter in 2032 (INFO: dates)
  A6  0 bytes outside the PEM armour (no comment, no second object, no trailing junk)
  A7  config/README.md at the head names the same fingerprint (the README's recorded figure agrees with the file)
--selftest   fixture copies in $G63_SCRATCH/fixtures: T0 the REAL head file passes; every arm must FAIL its named check.
Usage: c2_anchor_gate63.py --repo <git dir> [--head <sha>] | --file F --bundle B [--bundle-base B0] [--readme R] | --selftest [--repo R]
rc 0 all PASS / rc 1 any FAIL or 0 checked."""
import base64, hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate63 import K, git, Tally, SCRATCH

PEM_RX = re.compile(rb'-----BEGIN CERTIFICATE-----\r?\n.*?-----END CERTIFICATE-----\r?\n?', re.S)
OPENSSL = '/opt/homebrew/bin/openssl' if os.path.exists('/opt/homebrew/bin/openssl') else 'openssl'


def blocks(b): return PEM_RX.findall(b)


def der_of(block):
    body = re.sub(rb'-----(BEGIN|END) CERTIFICATE-----', b'', block)
    return base64.b64decode(re.sub(rb'\s+', b'', body), validate=False)


def ossl(args, data):
    p = subprocess.run([OPENSSL] + args, input=data, capture_output=True)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def ossl_count(data, scratch):
    """openssl storeutl counts certificates in a FILE (independent of the python regex)."""
    os.makedirs(scratch, exist_ok=True)
    f = os.path.join(scratch, 'storeutl_input.%d.crt' % os.getpid()); open(f, 'wb').write(data)
    p = subprocess.run([OPENSSL, 'storeutl', '-noout', '-certs', f], capture_output=True)
    out = p.stdout.decode() + p.stderr.decode()
    m = re.search(r'Total found:\s*(\d+)', out)
    q = os.path.join(scratch, '_quarantine'); os.makedirs(q, exist_ok=True)
    os.replace(f, os.path.join(q, os.path.basename(f)))   # quarantine, never rm
    return int(m.group(1)) if m else -1


def judge(f, bundle, bundle_base, readme, t, scratch):
    fb = blocks(f); bb = blocks(bundle)
    oc_f = ossl_count(f, scratch); oc_b = ossl_count(bundle, scratch)
    t.check('A1', len(fb) == 1 and oc_f == 1 and len(bb) == 2 and oc_b == 2,
            'file certs python %d / openssl %d (want 1/1); CONTROL bundle python %d / openssl %d (want 2/2)' % (len(fb), oc_f, len(bb), oc_b))
    fps = [hashlib.sha256(der_of(x)).hexdigest() for x in fb]
    rc, o, _ = ossl(['x509', '-noout', '-fingerprint', '-sha256'], f)
    ofp = re.sub(r'[^0-9a-f]', '', o.split('=', 1)[1].lower()) if rc == 0 and '=' in o else ''
    t.check('A2', fps == [K['dtrust_der_sha256']] and ofp == K['dtrust_der_sha256'],
            'python DER sha256 %s; openssl SHA-256 %s (want %s on both)' % ([x[:16] for x in fps], ofp[:16], K['dtrust_der_sha256'][:16]))
    eq1 = bool(bb) and f == bb[0]; diff2 = len(bb) > 1 and f != bb[1]; bstable = bundle_base is None or bundle_base == bundle
    t.check('A3', eq1 and diff2 and bstable,
            'file == bundle block 1: %s (%d vs %d bytes); CONTROL file != block 2: %s; bundle byte-identical base->head: %s' % (
                eq1, len(f), len(bb[0]) if bb else -1, diff2, 'n/a (no base given)' if bundle_base is None else bstable))
    bfps = [hashlib.sha256(der_of(x)).hexdigest() for x in bb]
    subj = []
    for x in fb:
        rc, o, _ = ossl(['x509', '-noout', '-subject', '-issuer'], x); subj.append(o)
    bsubj = ''.join(ossl(['x509', '-noout', '-subject'], x)[1] for x in bb)
    dc_in_file = K['digicert_der_sha256'] in fps or any(re.search(r'digicert', s, re.I) for s in subj) or re.search(rb'digicert', f, re.I)
    dc_ctl = K['digicert_der_sha256'] in bfps and bool(re.search(r'DigiCert', bsubj))
    t.check('A4', not dc_in_file and dc_ctl, 'DigiCert in the file: %s; CONTROL DigiCert found in the bundle (digest + subject): %s' % (bool(dc_in_file), dc_ctl))
    rc, o, _ = ossl(['x509', '-noout', '-subject', '-issuer', '-enddate', '-startdate'], f)
    cn = re.search(r'subject=.*?CN\s*=\s*([^,\n]+)', o); iss = re.search(r'issuer=(.*)', o); sub = re.search(r'subject=(.*)', o)
    end = re.search(r'notAfter=(.*)', o)
    ok5 = rc == 0 and cn and cn.group(1).strip() == K['dtrust_cn'] and sub and iss and sub.group(1).strip() == iss.group(1).strip() and end and '2032' in end.group(1)
    t.check('A5', bool(ok5), 'openssl rc %d; CN %r; self-signed %s; notAfter %r' % (
        rc, cn.group(1).strip() if cn else None, bool(sub and iss and sub.group(1).strip() == iss.group(1).strip()), end.group(1).strip() if end else None))
    junk = PEM_RX.sub(b'', f)
    t.check('A6', len(junk) == 0, 'bytes outside the PEM armour: %d %r' % (len(junk), junk[:60]))
    if readme is not None:
        t.check('A7', K['dtrust_der_sha256'] in readme.lower().replace(':', ''), 'config/README.md names %s: %s' % (
            K['dtrust_der_sha256'][:16], K['dtrust_der_sha256'] in readme.lower().replace(':', '')))


def from_repo(repo, head):
    show = lambda r, p: subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (r, p)], capture_output=True).stdout
    git(repo, 'rev-parse', head)   # read-verb guard + existence
    return (show(head, K['anchor_file']), show(head, K['bundle_file']), show(K['base'], K['bundle_file']),
            show(head, 'Blockchain/Dev/services/timestamping/config/README.md').decode('utf-8', 'replace'))


def selftest(repo):
    import io, contextlib
    fx = os.path.join(SCRATCH, 'fixtures'); os.makedirs(fx, exist_ok=True)
    f, b, b0, rd = from_repo(repo, K['head'])
    open(os.path.join(fx, 'c2_real_anchor.crt'), 'wb').write(f); open(os.path.join(fx, 'c2_real_bundle.crt'), 'wb').write(b)
    def run(ff, bb=b, bb0=b0, r=rd):
        t = Tally()
        with contextlib.redirect_stdout(io.StringIO()): judge(ff, bb, bb0, r, t, fx)
        return t
    t0 = run(f); ok = int(not t0.fails and t0.n == 7); total = 1
    print('SELFTEST %s T0 the REAL head file (fixture c2_real_anchor.crt): %d checked, fails %s' % ('OK' if ok else 'MISS', t0.n, t0.fails))
    bl = blocks(b)
    flip = lambda s: s.replace(b'MIIGnjCCBFagAwIBAgIDD+Sd', b'MIIGnjCCBFagAwIBAgIDD+Se', 1)
    arms = [('the DigiCert block appended', lambda: f + bl[1], ['A1', 'A4']),
            ('the whole two-root bundle shipped as the anchor', lambda: b, ['A1', 'A3', 'A4', 'A6']),
            ('one base64 character flipped', lambda: flip(f), ['A2', 'A3']),
            ('a leading comment line', lambda: b'# D-Trust root\n' + f, ['A3', 'A6']),
            ('CRLF line endings', lambda: f.replace(b'\n', b'\r\n'), ['A3']),
            ('the DigiCert block ALONE', lambda: bl[1], ['A2', 'A3', 'A4', 'A5']),
            ('an empty file', lambda: b'', ['A1', 'A2', 'A3', 'A5'])]
    for name, mk, want in arms:
        ff = mk(); assert ff != f, 'tamper did not land: ' + name
        p = os.path.join(fx, 'c2_arm_%02d.crt' % total); open(p, 'wb').write(ff)
        t = run(ff); total += 1; g = set(want) <= set(t.fails); ok += g
        print('SELFTEST %s %s (fixture %s): want FAIL %s | got %s' % ('OK' if g else 'MISS', name, os.path.basename(p), want, t.fails))
    t = run(f, bb0=b + b'\n'); total += 1; g = 'A3' in t.fails; ok += g
    print('SELFTEST %s the bundle changed base->head (one byte appended at base): want FAIL A3 | got %s' % ('OK' if g else 'MISS', t.fails))
    colon = ':'.join(K['dtrust_der_sha256'][i:i + 2] for i in range(0, 64, 2)).upper()
    rd2 = rd.replace(colon, ':'.join(['00'] * 32)).replace(K['dtrust_der_sha256'], '0' * 64)
    assert rd2 != rd and K['dtrust_der_sha256'] not in rd2.lower().replace(':', ''), 'README tamper did not land (ex1 history: an INERT arm)'
    t = run(f, r=rd2); total += 1; g = 'A7' in t.fails; ok += g
    print('SELFTEST %s README fingerprint altered: want FAIL A7 | got %s' % ('OK' if g else 'MISS', t.fails))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A: raise SystemExit(selftest(opt('--repo', K['checkout'])))
    scratch = os.path.join(SCRATCH, 'fixtures')
    if opt('--file'):
        rd = lambda k: open(opt(k), 'rb').read() if opt(k) else None
        f, b, b0 = rd('--file'), rd('--bundle'), rd('--bundle-base'); r = rd('--readme'); r = r.decode() if r else None
    else:
        f, b, b0, r = from_repo(opt('--repo', K['checkout']), opt('--head', K['head']))
    print('c2_anchor_gate63 openssl %s | file %d bytes | bundle %d bytes' % (ossl(['version'], b'')[1].strip(), len(f), len(b)))
    t = Tally(); judge(f, b, b0, r, t, scratch); raise SystemExit(t.end())
