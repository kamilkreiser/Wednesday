#!/usr/bin/env python3
"""c4_security_gateD2.py — gateD2 C4 SECURITY REVIEW, static, from git objects (READ ONLY) plus, with --fetch-anchors, two HTTPS GETs of the
providers' published root certificates. Every regex runs over CODE lines (comments blanked by lib code_lines) and sits beside a must-hit
control of the same regex that fires somewhere it should.
  V1 signature over the SIGNED ATTRIBUTES: the [0] tag replaced by SET OF (0x31) and webcrypto.subtle.verify over those bytes.
  V2 messageDigest == digest(eContent) compared;  V3 contentType attribute == id-ct-TSTInfo checked.
  V4 signingCertificate / signingCertificateV2 (OIDs 1.2.840.113549.1.9.16.2.12 / .2.47) checked — the COMMISSION names it; FAIL if the
     verifier never reads it (the probe's PF8 measures the runtime consequence).
  V5 EKU id-kp-timeStamping required;  V6 validity at genTime (notBefore / notAfter vs genTime) AND the chain engine's checkDate = genTime.
  V7 chain to the configured anchors: CertificateChainValidationEngine({trustedCerts: anchors ...}); INFO the `certs:` it is given
     (intermediates in the token are NOT passed when it is `[signer]` — the probe's PF5).
  V8 FAIL CLOSED: `anchors.length === 0` refuses BEFORE any token parse (the first statement of verifyRfc3161Token).
  V9 NO NETWORK AT VERIFY TIME: rfc3161-verify.ts imports exactly {node:crypto, asn1js, pkijs}; 0 fetch / http / https / net / axios / dns
     tokens in its code and in qualified-tsa's verifyTimestamp + readTrustAnchorsPem bodies; MUST-HIT: the same regex finds `fetch(` (or an
     http(s) client) in rfc3161-client.ts (the create path).
  V10 strict DER: BER indefinite length refused (findIndefinite called inside parseStrictDer), trailing bytes refused, canonical re-encode.
  V11 isQualified gone from non-test code under services/timestamping/src at HEAD; MUST-HIT: present at BASE.
  V12 MOCK PATH CLOSED in qualified-tsa.ts: 0 `verifyMockToken`, 0 `JSON.parse` in verifyTimestamp; non-0x30 tokens refused; MUST-HIT: base has both.
  V13 DB-ROW BRANCH UNCHANGED: index.ts blob == kit unchanged_must_equal == base blob, and its `SELECT * FROM ts_timestamps WHERE hash = $1 AND
      proof = $2` line is present (every kit unchanged_must_equal path compared).
  V14 THE COMMITTED BUNDLE (Wednesday 14:2xZ): config/tsa-trust-anchors.crt exists at HEAD, is ABSENT at base, parses into EXACTLY 2
      certificates whose SHA-256 fingerprints == kit anchors (computed here from the DER in the PEM, independent of pkijs); with
      --fetch-anchors each kit anchor is ALSO recomputed from its provider URL (redirects followed; DER or PEM) and must equal the bundle's.
  V15 ENV-ONLY LOADER: no non-test code names the bundle file (0 `tsa-trust-anchors` in code under Blockchain/Dev, compose / Dockerfiles
      included, MUST-HIT: the README names it); readTrustAnchorsPem reads process.env.TSA_TRUST_ANCHORS_PEM and returns undefined when unset
      (no default path).
  V16 config/README.md claims vs the tree: it names both CNs, both fingerprints (any separator / case), TSA_TRUST_ANCHORS_PEM, fail-closed
      when unset; every repo path it names exists at HEAD (printed). The gate reads the README itself; this check only catches drift.
  V17 request writer: der.ts strips AT MOST one leading 0x00 and adds no sign prefix (the code line), cell 16 exists; the BYTES are proven
      by the C3 request-bytes differential (forge at base vs der.ts at head).
  INFO: the signer fallback `?? certs[0]`; the SIG_ALG_BY_OID map (rsaEncryption absent -> PF6/PF11); ECDSA signatures passed to webcrypto
  unconverted (DER vs P1363 -> PF12); the messageDigest digest algorithm taken from the IMPRINT, not SignerInfo.digestAlgorithm (PF7).
--selftest: plants into copies of the HEAD texts (no repo write) — each removes one guard and must FAIL its row; the real head must PASS
except the rows the drafter predicts FAIL (V4, and V14-V16 while the bundle commit is absent).  --base-vs-base: base as head (must FAIL).
Usage: c4_security_gateD2.py --repo <clone> --head <sha> [--base sha] [--fetch-anchors] [--selftest | --base-vs-base]  rc 0 PASS / 1 FAIL / 2 usage"""
import hashlib, base64, json, os, re, sys, io, contextlib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gateD2 import K, git, now, Checks, has_commit, show, blob, code_lines

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--head' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); HEAD = opt('--head'); BASE = opt('--base', K['base'])
for s_ in (HEAD, BASE):
    if not re.fullmatch(r'[0-9a-f]{40}', s_ or '') or not has_commit(REPO, s_): print('REFUSING: %s is not a 40-hex commit in %s' % (s_, REPO)); raise SystemExit(2)
SVC = K['service']; NETRX = re.compile(r'\bfetch\s*\(|\brequire\(\s*[\'"](?:node:)?(?:https?|net|dns|tls)[\'"]|from\s+[\'"](?:node:)?(?:https?|net|dns|tls)[\'"]|\baxios\b|\bhttps?\.(?:request|get)\s*\(')
norm_fp = lambda s: re.sub(r'[^0-9A-F]', '', s.upper())


def func_body(code, name):
    """the {...} body of `function name(...)`: the parameter list and a `: {...}` return type are skipped by bracket matching"""
    m = re.search(r'(?:async\s+)?function\s+%s\s*\(' % re.escape(name), code)
    if not m: return None
    def match(i, o, c):
        d = 0
        for j in range(i, len(code)):
            d += (code[j] == o) - (code[j] == c)
            if d == 0: return j
        return None
    j = match(m.end() - 1, '(', ')')
    if j is None: return None
    k = j + 1
    while k < len(code) and code[k].isspace(): k += 1
    if k < len(code) and code[k] == ':':
        k += 1
        while k < len(code) and code[k].isspace(): k += 1
        if code[k] == '{': k = match(k, '{', '}') + 1
    i = code.index('{', k); e = match(i, '{', '}')
    return code[i:e + 1] if e is not None else None


def pem_certs(text):
    out = []
    for m in re.finditer(r'-----BEGIN CERTIFICATE-----([\s\S]*?)-----END CERTIFICATE-----', text or ''):
        try: der = base64.b64decode(re.sub(r'\s+', '', m.group(1)), validate=True)
        except Exception: continue
        out.append(der)
    return out


def fp(der): return ':'.join(re.findall('..', hashlib.sha256(der).hexdigest().upper()))


def fetch_anchor(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'gateD2-qa/1'})
    b = urllib.request.urlopen(req, timeout=60).read()
    if b'-----BEGIN CERTIFICATE-----' in b: return pem_certs(b.decode('ascii', 'replace'))[0], 'PEM', len(b)
    return b, 'DER', len(b)


def analyse(T, label, fetched=None):
    """T: dict of texts at the judged head (keys: verify, qtsa, client, der, test, bundle, readme, index_blob, base_*, code_refs, paths_exist)"""
    C = Checks(); V = code_lines(T['verify'] or ''); Q = code_lines(T['qtsa'] or ''); CL = code_lines(T['client'] or ''); D = code_lines(T['der'] or '')
    C.chk('V1 signature over signed attrs', bool(re.search(r'\[0x31\]', V)) and 'subtle.verify(' in V and 'signedBytes' in V and bool(re.search(r"!==\s*0xa0", V)),
          '[%s] SET OF substitution (0x31) %s | IMPLICIT [0] asserted %s | subtle.verify over signedBytes %s' % (label, bool(re.search(r'\[0x31\]', V)), bool(re.search(r"!==\s*0xa0", V)), 'subtle.verify(' in V and 'signedBytes' in V))
    C.chk('V2 messageDigest', bool(re.search(r'OID\.messageDigest', V)) and bool(re.search(r'declared\.equals\(actual\)', V)) and 'subtle.digest(' in V, 'messageDigest attr read %s | compared to digest(eContent) %s' % (bool(re.search(r'OID\.messageDigest', V)), bool(re.search(r'declared\.equals\(actual\)', V))))
    C.chk('V3 contentType attr', bool(re.search(r'attr\(OID\.contentType\)', V)) and bool(re.search(r'!==\s*OID\.tstInfo', V)), 'contentType attribute read and compared to id-ct-TSTInfo: %s' % (bool(re.search(r'attr\(OID\.contentType\)', V)) and bool(re.search(r'!==\s*OID\.tstInfo', V))))
    sc = re.findall(r'1\.2\.840\.113549\.1\.9\.16\.2\.(?:12|47)\b', V)
    C.chk('V4 signingCertificate(V2)', bool(sc), 'ESS signingCertificate / V2 OIDs read in the verifier: %d %s  <- the commission names this check; RFC 3161 2.4.1 requires the attribute; the probe PF8 measures a token WITHOUT it (README D1)' % (len(sc), sc))
    C.chk('V5 EKU', 'OID.timeStamping' in V and "'1.3.6.1.5.5.7.3.8'" in V and bool(re.search(r'purposes\.includes\(OID\.timeStamping\)', V)), 'id-kp-timeStamping required: %s' % bool(re.search(r'purposes\.includes\(OID\.timeStamping\)', V)))
    vt = bool(re.search(r'genTime\s*<\s*signer\.notBefore\.value\s*\|\|\s*genTime\s*>\s*signer\.notAfter\.value', V)); cd = bool(re.search(r'checkDate:\s*genTime', V))
    C.chk('V6 validity at genTime', vt and cd, 'signer validity vs genTime %s | chain checkDate = genTime %s' % (vt, cd))
    eng = re.search(r'new pkijs\.CertificateChainValidationEngine\(\{([^}]*)\}', V)
    C.chk('V7 chain to anchors', bool(eng) and 'trustedCerts: anchors' in (eng.group(1) if eng else '') and bool(re.search(r'if \(!chain\?\.result\)', V)), 'engine args %r | result checked %s' % (eng.group(1).strip() if eng else None, bool(re.search(r'if \(!chain\?\.result\)', V))))
    if eng: print('INFO V7 the engine is given certs %r — intermediates carried in the token are %s (probe PF5)' % (re.search(r'certs:\s*([^,]+)', eng.group(1)).group(1).strip() if re.search(r'certs:\s*([^,]+)', eng.group(1)) else None, 'NOT passed' if re.search(r'certs:\s*\[signer\]', eng.group(1)) else 'passed'))
    body = func_body(V, 'verifyRfc3161Token') or ''
    first = [l.strip() for l in body.split('\n')[1:] if l.strip()][:2]
    fc = len(first) == 2 and 'parseTrustAnchors' in first[0] and re.search(r"anchors\.length === 0\) return refuse\('no trust anchor configured'\)", first[1]) is not None
    C.chk('V8 fail closed first', fc, 'the first two statements of verifyRfc3161Token: %s' % first)
    imps = sorted(set(re.findall(r"^import\s+.*?from\s+'([^']+)'", T['verify'] or '', re.M)))
    qv = (func_body(Q, 'verifyTimestamp') or '') + (func_body(Q, 'readTrustAnchorsPem') or '')
    nv = NETRX.findall(V); nq = NETRX.findall(qv); nc = NETRX.findall(CL)
    C.chk('V9 no network at verify time', imps == ['asn1js', 'node:crypto', 'pkijs'] and not nv and not nq and bool(nc) and bool(qv),
          'verify-module imports %s (want asn1js, node:crypto, pkijs) | network tokens: verify module %d %s, qualified-tsa verifyTimestamp+readTrustAnchorsPem %d %s (bodies read %s) | MUST-HIT rfc3161-client.ts %d %s' % (imps, len(nv), nv[:2], len(nq), nq[:2], bool(qv), len(nc), nc[:2]))
    psd = func_body(V, 'parseStrictDer') or ''
    C.chk('V10 strict DER', 'findIndefinite(asn.result)' in psd and 'trailing bytes' in psd and 'reencoded.equals(der)' in psd, 'in parseStrictDer: findIndefinite %s | trailing bytes %s | canonical re-encode %s' % ('findIndefinite(asn.result)' in psd, 'trailing bytes' in psd, 'reencoded.equals(der)' in psd))
    C.chk('V11 isQualified dropped', T['isq_head'] == 0 and T['isq_base'] > 0, 'isQualified in non-test code under %s/src: head %d (want 0) | MUST-HIT base %d' % (SVC, T['isq_head'], T['isq_base']))
    qvt = func_body(Q, 'verifyTimestamp') or ''
    C.chk('V12 mock path closed', 'verifyMockToken' not in Q and 'JSON.parse' not in qvt and bool(re.search(r"tokenBuf\[0\] !== 0x30", qvt)) and T['mock_base'] > 0,
          'verifyMockToken in code %d | JSON.parse in verifyTimestamp %d | non-0x30 refused %s | MUST-HIT base verifyMockToken %d' % (Q.count('verifyMockToken'), qvt.count('JSON.parse'), bool(re.search(r"tokenBuf\[0\] !== 0x30", qvt)), T['mock_base']))
    C.chk('V13 DB-row branch unchanged', T['unchanged_ok'] and T['select_line'], 'kit unchanged_must_equal blobs equal at base, head and kit: %s %s | the DB-row SELECT line present in index.ts: %s' % (T['unchanged_ok'], T['unchanged_detail'], T['select_line']))
    bc = pem_certs(T['bundle']); bfp = sorted(fp(d) for d in bc); want = sorted(v['sha256'] for v in K['anchors'].values())
    fetched_ok = None
    if fetched is not None:
        fetched_ok = all(norm_fp(f) == norm_fp(K['anchors'][n]['sha256']) for n, (f, _, _) in fetched.items())
    C.chk('V14 committed bundle', T['bundle'] is not None and T['bundle_base'] is None and len(bc) == 2 and bfp == want and fetched_ok in (None, True),
          'bundle at head %s (%s) | at base %s | PEM blocks %d (want 2) | fingerprints %s | == kit %s | provider URLs recomputed %s' % (
              'PRESENT' if T['bundle'] is not None else 'ABSENT', K['bundle'], 'ABSENT' if T['bundle_base'] is None else 'PRESENT', len(bc), bfp, bfp == want,
              'not fetched (pass --fetch-anchors)' if fetched is None else {n: (f, how, size) for n, (f, how, size) in fetched.items()}))
    rtap = func_body(Q, 'readTrustAnchorsPem') or ''
    envonly = bool(re.search(r'const raw = process\.env\.TSA_TRUST_ANCHORS_PEM;', rtap)) and bool(re.search(r'if \(!raw \|\| !raw\.trim\(\)\) return undefined;', rtap)) and 'tsa-trust-anchors' not in rtap
    C.chk('V15 env-only loader', envonly and T['code_refs'] == [] and T['readme_names_bundle'],
          'readTrustAnchorsPem reads the env and returns undefined when unset, no default path: %s | code / compose / Dockerfile files naming the bundle: %d %s | MUST-HIT the README names it: %s' % (envonly, len(T['code_refs']), T['code_refs'][:4], T['readme_names_bundle']))
    R = T['readme'] or ''; RN = norm_fp(R)
    cl = {'both CNs': all(n in R for n in K['anchors']), 'both fingerprints': all(norm_fp(v['sha256']) in RN for v in K['anchors'].values()),
          'TSA_TRUST_ANCHORS_PEM': 'TSA_TRUST_ANCHORS_PEM' in R, 'fail closed when unset': bool(re.search(r'(?is)(unset|not set|empty).{0,120}(fail|refus|false)|fail[s -]*closed', R))}
    C.chk('V16 README claims', T['readme'] is not None and all(cl.values()) and not T['readme_missing_paths'], 'README at head %s | %s | repo paths it names that do NOT exist at head: %s' % (
        'PRESENT' if T['readme'] is not None else 'ABSENT', cl, T['readme_missing_paths'] or 'NONE'))
    strip = bool(re.search(r"content\.length > 1 && content\[0\] === 0x00 && \(content\[1\] & 0x80\) === 0 \? 1 : 0", D)); noprefix = 'Buffer.from([0x00' not in D and 'Buffer.from([0])' not in D
    C.chk('V17 request writer quirks', strip and noprefix and T['cell16'], 'at-most-one-zero strip line %s | no sign-prefix insertion %s | cell 16 present %s | the BYTES: C3 request-bytes differential' % (strip, noprefix, T['cell16']))
    print('INFO signer fallback `?? certs[0]` present: %s | SIG_ALG_BY_OID keys %s (rsaEncryption 1.2.840.113549.1.1.1 %s) | ECDSA DER->P1363 conversion %s | digest(eContent) uses %s' % (
        '?? certs[0]' in V, re.findall(r"'(1\.2\.840\.[0-9.]+)': \{ importParams", V), 'ABSENT' if "'1.2.840.113549.1.1.1'" not in V else 'present',
        'ABSENT' if not re.search(r'p1363|ieee|toP1363|derToRaw|rawSignature', V, re.I) else 'present', 'the IMPRINT algorithm (hashAlg)' if 'subtle.digest(hashAlg, eContent)' in V else 'other'))
    return C


def load(head):
    T = {}
    T['verify'] = show(REPO, head, K['verify_module']); T['qtsa'] = show(REPO, head, K['qtsa_module']); T['client'] = show(REPO, head, K['client_module'])
    T['der'] = show(REPO, head, K['der_module']); T['bundle'] = show(REPO, head, K['bundle']); T['bundle_base'] = show(REPO, BASE, K['bundle']); T['readme'] = show(REPO, head, K['bundle_readme'])
    def srcfiles(sha):
        return [l for l in git(REPO, 'ls-tree', '-r', '--name-only', sha, SVC + '/src').splitlines() if re.search(r'\.[cm]?[jt]s$', l) and '/__tests__/' not in l]
    def count(sha, tok): return sum(code_lines(show(REPO, sha, f) or '').count(tok) for f in srcfiles(sha))
    T['isq_head'] = count(head, 'isQualified'); T['isq_base'] = count(BASE, 'isQualified'); T['mock_base'] = code_lines(show(REPO, BASE, K['qtsa_module']) or '').count('verifyMockToken')
    det = {}; ok = True
    for p, b in K['unchanged_must_equal'].items():
        bh, bb = blob(REPO, head, p), blob(REPO, BASE, p); det[p.split('/')[-1]] = bh == bb == b; ok &= bh == bb == b
    T['unchanged_ok'] = ok; T['unchanged_detail'] = det
    T['select_line'] = "'SELECT * FROM ts_timestamps WHERE hash = $1 AND proof = $2 LIMIT 1'" in (show(REPO, head, K['index_module']) or '')
    refs = []
    for l in git(REPO, 'ls-tree', '-r', '--name-only', head, 'Blockchain/Dev').splitlines():
        in_svc_code = l.startswith(SVC + '/') and '/__tests__/' not in l and '/node_modules/' not in l and re.search(r'(\.[cm]?[jt]sx?|\.ya?ml|\.json|\.sh|Dockerfile[^/]*)$', l) and not l.endswith('package-lock.json')
        wiring = re.search(r'(docker-compose[^/]*\.ya?ml|Dockerfile[^/]*|/\.env[^/]*)$', l) is not None
        if in_svc_code or wiring:
            t = show(REPO, head, l) or ''
            if 'tsa-trust-anchors' in t: refs.append(l)
    T['code_refs'] = refs; T['readme_names_bundle'] = 'tsa-trust-anchors' in (T['readme'] or '')
    miss = []
    for m in sorted(set(re.findall(r'`((?:Blockchain/Dev/|services/|src/|config/|\./)[\w./-]+)`', T['readme'] or ''))):
        cands = [m.lstrip('./'), SVC + '/' + m.lstrip('./'), 'Blockchain/Dev/' + m.lstrip('./')]
        if not any(git(REPO, 'cat-file', '-e', '%s:%s' % (head, c), check=False)[0] == 0 for c in cands): miss.append(m)
    T['readme_missing_paths'] = miss
    T['cell16'] = "it('cell 16:" in (show(REPO, head, K['test_file']) or '')
    return T


print('c4_security_gateD2 %s | repo %s | base %s | head %s | mode %s' % (now(), REPO, BASE[:12], HEAD[:12], 'selftest' if '--selftest' in A else 'base-vs-base' if '--base-vs-base' in A else 'gate'))
fetched = None
if '--fetch-anchors' in A:
    fetched = {}
    for n, v in K['anchors'].items():
        der, how, size = fetch_anchor(v['url']); fetched[n] = (fp(der), how, size); print('INFO fetched %s from %s: %s %d B sha256 %s' % (n, v['url'], how, size, fp(der)))
if '--base-vs-base' in A:
    C = analyse(load(BASE), 'BASE as head'); n = C.nfail()
    print('C4 SECURITY %s (base-vs-base, a control: it MUST fail): %d FAIL of %d' % ('PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
T = load(HEAD)
if '--selftest' in A:
    SYN = ''
    if T['bundle'] is None:   # the bundle commit is not in this head: SYNTHESISE the ruled bundle + README so V14-V16 have a passing reference
        if fetched is None: print('REFUSING: --selftest on a head without the bundle needs --fetch-anchors (the synthetic bundle is built from the providers\' DER)'); raise SystemExit(2)
        ders = []
        for n, v in K['anchors'].items(): ders.append(fetch_anchor(v['url'])[0])
        T = dict(T, bundle=''.join('-----BEGIN CERTIFICATE-----\n%s\n-----END CERTIFICATE-----\n' % '\n'.join(re.findall('.{1,64}', base64.b64encode(d).decode())) for d in ders),
                 readme='# TSA trust anchors\n`config/tsa-trust-anchors.crt` pins %s. Loaded only from TSA_TRUST_ANCHORS_PEM; unset means every real token verifies false (fail closed).\n' % '; '.join('%s %s' % (n, v['sha256']) for n, v in K['anchors'].items()),
                 readme_names_bundle=True, readme_missing_paths=[])
        SYN = ' (SYNTHETIC bundle + README built from the fetched provider DER, because this head has no bundle commit)'
    def plant(key, a, b):
        t = dict(T); assert (t[key] or '').count(a) >= 1, 'plant anchor %r absent from %s' % (a, key); t[key] = t[key].replace(a, b, 1); return t
    FAKE_PEM = '\n'.join('-----BEGIN CERTIFICATE-----\n%s\n-----END CERTIFICATE-----' % base64.b64encode(b'not a real cert %d' % i).decode() for i in range(2))
    arms = [
        ('T0 real head' + SYN, T, None),
        ('T1 signature verify removed', plant('verify', 'subtle.verify(', 'subtle.noverify('), 'V1'),
        ('T2 messageDigest compare removed', plant('verify', 'declared.equals(actual)', 'true'), 'V2'),
        ('T3 EKU check removed', plant('verify', 'purposes.includes(OID.timeStamping)', 'true'), 'V5'),
        ('T4 fail-closed moved below the parse', plant('verify', "if (anchors.length === 0) return refuse('no trust anchor configured');", ''), 'V8'),
        ('T5 a fetch( in the verifier', plant('verify', 'const refuse =', 'void fetch("https://x");\nconst refuse ='), 'V9'),
        ('T6 an https import in the verifier', plant('verify', "import * as pkijs from 'pkijs';", "import * as pkijs from 'pkijs';\nimport * as https from 'https';"), 'V9'),
        ('T7 indefinite-length guard removed', plant('verify', 'findIndefinite(asn.result)', 'false'), 'V10'),
        ('T8 the loader names a default bundle path', plant('qtsa', 'const raw = process.env.TSA_TRUST_ANCHORS_PEM;', "const raw = process.env.TSA_TRUST_ANCHORS_PEM || 'config/tsa-trust-anchors.crt';"), 'V15'),
        ('T9 a bundle of 2 non-root blobs', dict(T, bundle=FAKE_PEM), 'V14'),
        ('T10 chain result unchecked', plant('verify', 'if (!chain?.result) {', 'if (false) {'), 'V7'),
        ('T12 the README loses a fingerprint', dict(T, readme=(T['readme'] or '').replace(K['anchors']['DigiCert Assured ID Root CA']['sha256'], 'REMOVED')), 'V16'),
        ('T13 a third certificate in the bundle', dict(T, bundle=(T['bundle'] or '') + (T['bundle'] or '').split('-----END CERTIFICATE-----')[0] + '-----END CERTIFICATE-----\n'), 'V14'),
        ('T11 a JSON.parse mock path back in verifyTimestamp', plant('qtsa', 'const tokenBuf = Buffer.from(token, \'base64\');', 'const tokenBuf = Buffer.from(token, \'base64\'); JSON.parse("{}");'), 'V12'),
    ]
    ok = 0; real_fails = None
    for name, t, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): C = analyse(t, name, fetched)
        f = C.failed()
        if want is None:
            real_fails = f; good = True   # the real head's failures are the PREDICTION, printed; each plant must ADD its row
            print('SELFTEST REF %s: failed %s (the drafter-predicted rows; each plant below must ADD its own)' % (name, f or 'NONE'))
        else:
            good = any(x.startswith(want + ' ') for x in f) and not any(x.startswith(want + ' ') for x in (real_fails or []))
            print('SELFTEST %s %s: want a NEW FAIL on %s | failed %s' % ('OK' if good else 'MISS', name, want, f))
        ok += good
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
C = analyse(T, 'HEAD', fetched); n = C.nfail()
print('C4 SECURITY %s: %d FAIL of %d checks | base %s | head %s%s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), BASE[:12], HEAD[:12], '' if fetched is not None else ' | anchors NOT fetched'))
raise SystemExit(1 if n else 0)
