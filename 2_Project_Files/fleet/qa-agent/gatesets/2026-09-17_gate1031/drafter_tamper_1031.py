#!/usr/bin/env python3
"""drafter_tamper_1031.py — at HEAD be8596a29 in the drafter clone (never the checkout): the builder's 11-row table re-derived on the WHOLE originate suite
(T0, RP-DEV-DOCS, RP-DEV-CERTS, TN-VERSION, TN-SIGNCERT, TN-SIGNWALLET, TN-ISSUE, CASEFOLD-VERSION, SOURCEDATA-VERSION, NB-CASEFOLD, TI) plus the drafter's
own per-writer forms that no builder row can catch (X-VERSION-TRIM, X-SIGNCERT-AFTER-UPSTREAM, X-SIGNWALLET-SERVED, X-ISSUE-LOOSE, X-ISSUE-AFTER-HOLDER,
X-ISSUE-AFTER-ANCHOR). Each row: every scripted edit asserts its anchor count = 1 and exactly one QA-TAMPER marker; project tsc -p rc (a row that does not compile is
VOID); whole originate jest (json) with reds per KS-1213 describe block and reds / load failures outside the file; for X-* rows the drafter probe re-run on the
tampered tree (the consequence the builder's cells miss); restore by bytes + sha256 + git diff --quiet HEAD. Then: the test-including tsc program (head and dev,
listFilesOnly proof, planted control), eslint on the three PR files with a firing control, and generate-openapi --check at head. Never rm."""
import json, subprocess, datetime, os, hashlib, re, shutil, sys
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1031'
paths = json.load(open(GS + '/out/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
HT = paths['trees']['head']; DT = paths['trees']['dev']; DEV = '/Blockchain/Dev'; O = HT + DEV + '/services/originate'; BIN = HT + DEV + '/node_modules/.bin/'
FD = O + '/src/routes/documents.ts'; FC = O + '/src/routes/certifications.ts'; TF = 'ks1213-a-derived-writer-relabel-is-refused.test.ts'
ORIG = {FD: open(FD, 'rb').read(), FC: open(FC, 'rb').read()}; SHA0 = {k: hashlib.sha256(v).hexdigest() for k, v in ORIG.items()}
P('drafter_tamper_1031', now(), '| documents.ts', SHA0[FD][:16], '| certifications.ts', SHA0[FC][:16])
DEVSHA = paths['sha']['dev']
GUARD = "      if (metadata.documentType !== undefined && metadata.documentType !== source.type) {\n"
ISSUE_IF = "      if (req.body.parentDocumentId && derivedDataDocumentType !== undefined && derivedDataDocumentType !== (type || 'verification_certificate')) {\n"
ISSUE_BLOCK_START = "\n      // KS-1213: with parentDocumentId, the derived document is stored as the certification type\n"
ISSUE_BLOCK_END = "        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'data.documentType must equal the certification type when parentDocumentId is set' } });\n      }\n"
SC_COMMENT = "      // KS-1213: stored as `source.type`, served as `data.documentType || type`; same refusal as /version.\n"
SC_RET = "        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });\n      }\n"
def route_span(s, route):
    a = "  '" + route + "',\n"; assert s.count(a) == 1, (route, s.count(a)); i = s.index(a); j = s.find('documentsRouter.post(', i); return i, (j if j > 0 else len(s))
def sub_in_route(s, route, old, new):
    i, j = route_span(s, route); seg = s[i:j]; assert seg.count(old) == 1, (route, 'anchor in route', seg.count(old)); return s[:i] + seg.replace(old, new) + s[j:]
def once(s, old, new):
    assert s.count(old) == 1, ('anchor', old[:70], s.count(old)); return s.replace(old, new)
def edit_docs(fn):
    def f():
        s = ORIG[FD].decode(); s2 = fn(s); assert s2.count('QA-TAMPER') == 1, 'marker count'; open(FD, 'w').write(s2)
    return f
def edit_certs(fn):
    def f():
        s = ORIG[FC].decode(); s2 = fn(s); assert s2.count('QA-TAMPER') == 1, 'marker count'; open(FC, 'w').write(s2)
    return f
def dev_bytes(path, rel):
    def f(): open(path, 'wb').write(subprocess.run(['git', '-C', HT, 'show', DEVSHA + ':Blockchain/Dev/services/originate/' + rel], capture_output=True).stdout)
    return f
def move_sign_cert(s):
    i, j = route_span(s, '/:id/sign-cert'); seg = s[i:j]
    blk = SC_COMMENT + GUARD + SC_RET; assert seg.count(blk) == 1, 'sign-cert guard block'
    seg = seg.replace(blk, '')
    anchor = "      // 3. Mint the new versioned document row. contentHash matches the\n      //    source (bytes unchanged); the signature lives in data blob.\n"
    assert seg.count(anchor) == 1, 'sign-cert mint anchor'
    seg = seg.replace(anchor, "      // QA-TAMPER X-SIGNCERT-AFTER-UPSTREAM: the guard moved after the issuer-certs sign call\n" + GUARD + SC_RET + anchor)
    return s[:i] + seg + s[j:]
def move_issue(s, anchor, tag):
    i = s.index(ISSUE_BLOCK_START); j = s.index(ISSUE_BLOCK_END, i) + len(ISSUE_BLOCK_END); blk = s[i:j]
    assert s.count(ISSUE_BLOCK_START) == 1 and blk.count(ISSUE_IF) == 1
    s = s[:i] + s[j:]
    return once(s, anchor, "      // QA-TAMPER " + tag + "\n" + blk.lstrip('\n') + anchor)
FORMS = [
 ('T0', None, None),
 ('RP-DEV-DOCS', dev_bytes(FD, 'src/routes/documents.ts'), None),
 ('RP-DEV-CERTS', dev_bytes(FC, 'src/routes/certifications.ts'), None),
 ('TN-VERSION', edit_docs(lambda s: sub_in_route(s, '/:id/version', GUARD, GUARD.replace('if (', 'if (Date.now() < 0 && ').rstrip('\n') + ' // QA-TAMPER TN-VERSION\n')), None),
 ('TN-SIGNCERT', edit_docs(lambda s: sub_in_route(s, '/:id/sign-cert', GUARD, GUARD.replace('if (', 'if (Date.now() < 0 && ').rstrip('\n') + ' // QA-TAMPER TN-SIGNCERT\n')), None),
 ('TN-SIGNWALLET', edit_docs(lambda s: sub_in_route(s, '/:id/sign-wallet', GUARD, GUARD.replace('if (', 'if (Date.now() < 0 && ').rstrip('\n') + ' // QA-TAMPER TN-SIGNWALLET\n')), None),
 ('TN-ISSUE', edit_certs(lambda s: once(s, ISSUE_IF, ISSUE_IF.replace('if (', 'if (Date.now() < 0 && ').rstrip('\n') + ' // QA-TAMPER TN-ISSUE\n')), None),
 ('CASEFOLD-VERSION', edit_docs(lambda s: sub_in_route(s, '/:id/version', GUARD, "      if (metadata.documentType !== undefined && String(metadata.documentType).toUpperCase() !== String(source.type).toUpperCase()) { // QA-TAMPER CASEFOLD-VERSION\n")), None),
 ('SOURCEDATA-VERSION', edit_docs(lambda s: sub_in_route(s, '/:id/version', GUARD, "      if ({ ...source.data, ...metadata }.documentType !== undefined && { ...source.data, ...metadata }.documentType !== source.type) { // QA-TAMPER SOURCEDATA-VERSION\n")), None),
 ('NB-CASEFOLD', edit_docs(lambda s: once(s, "      if (dataDocumentType !== undefined && dataDocumentType !== docType) {\n", "      if (dataDocumentType !== undefined && String(dataDocumentType).toUpperCase() !== docType.toUpperCase()) { // QA-TAMPER NB-CASEFOLD\n")), None),
 ('TI', edit_docs(lambda s: sub_in_route(s, '/:id/version', GUARD, GUARD + "      // QA-TAMPER TI inert comment\n")), None),
 ('X-VERSION-TRIM', edit_docs(lambda s: sub_in_route(s, '/:id/version', GUARD, "      if (metadata.documentType !== undefined && (typeof metadata.documentType !== 'string' || metadata.documentType.trim() !== source.type)) { // QA-TAMPER X-VERSION-TRIM\n")), ['V-M06 trailing space', 'V-M07 leading space']),
 ('X-SIGNCERT-AFTER-UPSTREAM', edit_docs(move_sign_cert), ['C-M01 PROPERTY_DEED', 'C-OBO mismatch + onBehalfOf']),
 ('X-SIGNWALLET-SERVED', edit_docs(lambda s: sub_in_route(s, '/:id/sign-wallet', GUARD, "      if (metadata.documentType !== undefined && metadata.documentType !== ((source.data as Record<string, unknown> | undefined)?.documentType ?? source.type)) { // QA-TAMPER X-SIGNWALLET-SERVED\n")), ['W-L01 legacy CERTIFICATE/DEGREE + DEGREE', 'W-L02 legacy CERTIFICATE/DEGREE + CERTIFICATE']),
 ('X-ISSUE-LOOSE', edit_certs(lambda s: once(s, ISSUE_IF, ISSUE_IF.replace('derivedDataDocumentType !== undefined', "typeof derivedDataDocumentType === 'string'").rstrip('\n') + ' // QA-TAMPER X-ISSUE-LOOSE\n')), ['I-I03 number 7', 'I-I04 array [certificate]', 'I-I05 object']),
 ('X-ISSUE-AFTER-HOLDER', edit_certs(lambda s: move_issue(s, "      const id = uuidv4();\n", 'X-ISSUE-AFTER-HOLDER: the guard moved after the holder resolution')), ['I-I14 holderEmail']),
 ('X-ISSUE-AFTER-ANCHOR', edit_certs(lambda s: move_issue(s, "      const certification: Certification = {\n", 'X-ISSUE-AFTER-ANCHOR: the guard moved after the anchoring submit')), ['I-I01 PROPERTY_DEED']),
]
def suite(tag):
    out = GS + '/out/tamper/%s.json' % tag
    p = subprocess.run([BIN + 'jest', '--json', '--outputFile', out, '--silent'], cwd=O, capture_output=True, text=True, env=dict(os.environ, CI='1'))
    open(GS + '/out/tamper/%s.stderr' % tag, 'w').write(p.stderr)
    j = json.load(open(out)); inside = {}; outside = {}; loadfail = 0
    for s in j['testResults']:
        fails = [a for a in s['assertionResults'] if a['status'] == 'failed']
        if s['status'] != 'passed' and not s['assertionResults']: loadfail += 1
        if s['name'].endswith(TF):
            for a in fails:
                k = (a.get('ancestorTitles') or ['?'])[0]; k = re.sub(r' (as|with parentDocumentId as) .*', '', k).replace('KS-1213 POST /api/certifications/issue', 'issue')
                inside[k] = inside.get(k, 0) + 1
            inside['_run'] = len(s['assertionResults'])
        elif fails or s['status'] != 'passed':
            outside[s['name'].split('/src/')[-1]] = len(fails)
    return j, inside, outside, loadfail
def restore():
    for k, v in ORIG.items(): open(k, 'wb').write(v)
    ok = all(hashlib.sha256(open(k, 'rb').read()).hexdigest() == SHA0[k] for k in ORIG)
    rc = subprocess.run(['git', '-C', HT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode; return ok, rc
def probe(tag, ids):
    d = O + '/src/qa_probe'; os.makedirs(d, exist_ok=True); shutil.copyfile(GS + '/src/qa1031-drafter-probe.test.ts', d + '/qa1031-drafter-probe.test.ts')
    out = GS + '/out/tamper/%s.probe_rows.json' % tag
    p = subprocess.run([BIN + 'jest', '--testMatch', '**/qa_probe/*.test.ts', '--json', '--outputFile', GS + '/out/tamper/%s.probe_jest.json' % tag], cwd=O, capture_output=True, text=True, env=dict(os.environ, QA1031_ROWS_OUT=out, CI='1'))
    rows = json.load(open(out))
    for r in rows:
        if r['id'] in ids and r['who'] in ('ISSUER', 'CONN_DOCS', 'CONN_CERTS'):
            P('     probe under', tag, '|', r['who'], r['id'], '->', r['status'], r['code'], 'derived', r['derivedSaved'], 'stored', json.dumps(r['storedType']), 'served', json.dumps(r['servedGET'], ensure_ascii=True), 'signUpstream', r['signUpstream'], 'holderStub', r['holderStub'], 'anchors', r['anchorsUpstream'], 'saveCertification', r['saveCertification'])
os.makedirs(GS + '/out/tamper', exist_ok=True)
rows = {}
for tag, apply, probe_ids in FORMS:
    if apply: apply()
    tsc = subprocess.run([BIN + 'tsc', '--noEmit', '-p', '.'], cwd=O, capture_output=True, text=True)
    if tsc.returncode != 0:
        ok, drc = restore(); rows[tag] = dict(VOID=True, tsc=tsc.returncode, tsc_out=(tsc.stdout + tsc.stderr)[:400], restored=ok, diff_rc=drc)
        P(tag, now(), 'VOID tsc rc', tsc.returncode, (tsc.stdout + tsc.stderr).strip()[:300], '| restored', ok, drc); continue
    j, inside, outside, lf = suite(tag)
    if probe_ids: probe(tag, probe_ids)
    ok, drc = restore()
    rows[tag] = dict(tsc=0, suites=j['numTotalTestSuites'], tests=j['numTotalTests'], failed=j['numFailedTests'], pending=j['numPendingTests'], ks1213_reds=inside, outside=outside, load_failures=lf, restored_sha=ok, diff_quiet_rc=drc)
    P('%-26s %s | tsc 0 | %d/%d failed %d pending %d | ks1213 reds %s | outside %s | load failures %d | restored %s diff rc %d' % (tag, now(), j['numTotalTestSuites'], j['numTotalTests'], j['numFailedTests'], j['numPendingTests'], {k: v for k, v in inside.items()}, outside, lf, ok, drc))
json.dump(rows, open(GS + '/out/tamper_rows.json', 'w'), indent=1)
# test-including tsc program
for name, tree in (('head', HT), ('dev', DT)):
    od = tree + DEV + '/services/originate'; cfg = od + '/tsconfig.qa1031-with-tests.json'
    open(cfg, 'w').write(json.dumps({'extends': './tsconfig.json', 'compilerOptions': {'noEmit': True, 'types': ['jest', 'node']}, 'include': ['src/**/*'], 'exclude': ['node_modules', 'dist', 'src/qa_probe']}))
    lf = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', cfg, '--listFilesOnly'], cwd=od, capture_output=True, text=True).stdout
    lp = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', '.', '--listFilesOnly'], cwd=od, capture_output=True, text=True).stdout
    p = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', cfg], cwd=od, capture_output=True, text=True)
    errs = [l for l in p.stdout.splitlines() if re.match(r'^src/.*\(\d+,\d+\): error', l)]
    P('TSC-WITH-TESTS', name, now(), 'rc', p.returncode, '| ks1213 test in program', 'ks1213-a-derived' in lf, '| in project program', 'ks1213-a-derived' in lp, '| qa_probe in either', 'qa_probe' in lf or 'qa_probe' in lp, '| __tests__ files', lf.count('/__tests__/'), 'project', lp.count('/__tests__/'), '| error lines', len(errs), [e[:120] for e in errs[:3]])
    open(GS + '/out/tsc_with_tests_%s.out' % name, 'w').write(p.stdout + p.stderr)
tf = O + '/src/__tests__/' + TF; tb = open(tf, 'rb').read(); th = hashlib.sha256(tb).hexdigest()
open(tf, 'wb').write(tb + b"\nconst qaPlant1031: number = 'x'; // QA-PLANT\n")
p = subprocess.run([BIN + 'tsc', '-p', O + '/tsconfig.qa1031-with-tests.json'], cwd=O, capture_output=True, text=True)
open(tf, 'wb').write(tb); P('TSC PLANT errors in ks1213 test', sum(1 for l in p.stdout.splitlines() if 'ks1213' in l and 'error' in l), '(want >= 1) | restored', hashlib.sha256(open(tf, 'rb').read()).hexdigest() == th)
for rel in ('src/routes/documents.ts', 'src/routes/certifications.ts', 'src/__tests__/' + TF):
    for name, tree in (('head', HT), ('dev', DT)):
        od = tree + DEV + '/services/originate'
        if not os.path.exists(od + '/' + rel): P('ESLINT', name, rel.split('/')[-1], 'ABSENT'); continue
        p = subprocess.run([tree + DEV + '/node_modules/.bin/eslint', '-f', 'json', rel], cwd=od, capture_output=True, text=True)
        try:
            ms = json.loads(p.stdout)[0]['messages']; P('ESLINT', name, rel.split('/')[-1], 'rc', p.returncode, 'messages', len(ms), sorted({(m.get('ruleId'), m['message'][:60]) for m in ms})[:8])
        except Exception as e: P('ESLINT', name, rel, 'unparsed', type(e).__name__, (p.stdout + p.stderr)[:300])
fc = O + '/src/qa_probe/qa1031-eslint-control.ts'; open(fc, 'w').write('const qaUnused1031 = 1;\nexport {};\n')
p = subprocess.run([BIN + 'eslint', '-f', 'json', 'src/qa_probe/qa1031-eslint-control.ts'], cwd=O, capture_output=True, text=True)
try: P('ESLINT firing control', [m.get('ruleId') for m in json.loads(p.stdout)[0]['messages']])
except Exception as e: P('ESLINT firing control unparsed', (p.stdout + p.stderr)[:300])
os.rename(fc, fc + '.quarantined')
p = subprocess.run(['npm', 'run', 'generate-openapi', '--', '--check'], cwd=HT + DEV, capture_output=True, text=True)
P('OPENAPI generate-openapi --check at head rc', p.returncode, (p.stdout + p.stderr).strip()[-500:])
ok, drc = restore(); P('final restore', ok, 'diff rc', drc, '| end', now())
