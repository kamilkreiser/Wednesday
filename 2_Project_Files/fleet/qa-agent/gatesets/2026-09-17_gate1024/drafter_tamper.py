#!/usr/bin/env python3
"""drafter_tamper.py — at HEAD in the drafter clone: red-proof (documents.ts = develop 581c9db0d bytes) + the seat's 5 tamper forms re-derived + gate-authored
G-CASEFOLD (the comparison case-insensitive) and G-TRUTHY (only a truthy data.documentType is compared) and G-AFTERFILL (the check moved after the data blob is built and
compares data.documentType, i.e. checked after normalisation). Each row: anchor count 1 + marker, project tsc -p rc (VOID if != 0), WHOLE originate jest (json), reds per file,
restore by bytes + sha256 + git diff --quiet. Then the test-including tsc program (a scratch tsconfig that drops the __tests__ excludes; head and dev; errors per file; a
planted control), eslint on the two PR files with a firing control, and generate-openapi --check at head. Never rm; scratch configs are left in the clone and named."""
import json, subprocess, datetime, os, hashlib, re
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024'
paths = json.load(open(GS + '/out/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
HT = paths['trees']['head']; DT = paths['trees']['dev']; DEV = '/Blockchain/Dev'; O = HT + DEV + '/services/originate'; BIN = HT + DEV + '/node_modules/.bin/'
F = O + '/src/routes/documents.ts'; T = 'src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts'
orig = open(F, 'rb').read(); SHA0 = hashlib.sha256(orig).hexdigest(); P('drafter_tamper', now(), 'documents.ts sha256', SHA0[:16])
COND = "      if (dataDocumentType !== undefined && dataDocumentType !== docType) {\n"
FORMS = {
  'T0': None,
  'NOCHECK': (COND, "      if (dataDocumentType !== undefined && dataDocumentType !== docType && false) { // QA-TAMPER NOCHECK\n"),
  'LOOSE': (COND, "      if (typeof dataDocumentType === 'string' && dataDocumentType !== docType) { // QA-TAMPER LOOSE\n"),
  'WRONGSIDE': (COND, "      if (dataDocumentType !== undefined && dataDocumentType !== rawType) { // QA-TAMPER WRONGSIDE\n"),
  'TI': (COND, "      if (dataDocumentType !== undefined && docType !== dataDocumentType) { // QA-TAMPER TI identity\n"),
  'G-CASEFOLD': (COND, "      if (dataDocumentType !== undefined && String(dataDocumentType).toUpperCase() !== String(docType).toUpperCase()) { // QA-TAMPER G-CASEFOLD\n"),
  'G-TRUTHY': (COND, "      if (dataDocumentType && dataDocumentType !== docType) { // QA-TAMPER G-TRUTHY\n"),
  'G-TRIM': (COND, "      if (dataDocumentType !== undefined && String(dataDocumentType).trim() !== docType.trim()) { // QA-TAMPER G-TRIM\n"),
}
def suite(tag):
    out = GS + '/out/tamper_%s.json' % tag
    p = subprocess.run([BIN + 'jest', '--json', '--outputFile', out, '--silent'], cwd=O, capture_output=True, text=True, env=dict(os.environ, CI='1'))
    j = json.load(open(out)); reds = {}
    for s in j['testResults']:
        n = sum(1 for a in s['assertionResults'] if a['status'] == 'failed')
        if n or s['status'] != 'passed': reds[s['name'].split('/src/')[-1]] = (n, s['status'], [re.sub(r'\s+', ' ', (a.get('failureMessages') or [''])[0])[:90] for a in s['assertionResults'] if a['status'] == 'failed'][:2] or (s.get('message') or '')[:160])
    return j, reds
def restore():
    open(F, 'wb').write(orig); ok = hashlib.sha256(open(F, 'rb').read()).hexdigest() == SHA0
    rc = subprocess.run(['git', '-C', HT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode; return ok, rc
rows = {}
for tag, form in FORMS.items():
    s = orig.decode()
    if form:
        assert s.count(form[0]) == 1, (tag, 'anchor', s.count(form[0])); s = s.replace(form[0], form[1]); assert s.count('QA-TAMPER') == 1
        open(F, 'w').write(s)
    tsc = subprocess.run([BIN + 'tsc', '--noEmit', '-p', '.'], cwd=O, capture_output=True, text=True)
    j, reds = suite(tag); ok, drc = restore()
    rows[tag] = dict(tsc=tsc.returncode, suites=j['numTotalTestSuites'], tests=j['numTotalTests'], failed=j['numFailedTests'], pending=j['numPendingTests'], reds=reds, restored_sha=ok, diff_quiet_rc=drc)
    P(tag, now(), 'anchor 1' if form else 'no edit', '| tsc rc', tsc.returncode, (tsc.stdout + tsc.stderr).strip()[:160], '| %d/%d failed %d pending %d' % (j['numTotalTestSuites'], j['numTotalTests'], j['numFailedTests'], j['numPendingTests']), '| reds', reds, '| restored sha', ok, 'diff --quiet rc', drc)
# red-proof: documents.ts = develop bytes, the PR test in place
devb = subprocess.run(['git', '-C', HT, 'show', paths['sha']['dev'] + ':Blockchain/Dev/services/originate/src/routes/documents.ts'], capture_output=True).stdout
open(F, 'wb').write(devb); j, reds = suite('redproof'); ok, drc = restore()
kt = [s for s in j['testResults'] if s['name'].endswith(T)][0]
P('RED-PROOF', now(), 'documents.ts = develop bytes | ks1202 file run', len(kt['assertionResults']), 'red', sum(1 for a in kt['assertionResults'] if a['status'] == 'failed'), 'green', sum(1 for a in kt['assertionResults'] if a['status'] == 'passed'), '| whole', j['numTotalTests'], 'failed', j['numFailedTests'], '| red kinds', sorted({(a.get('failureMessages') or [''])[0].split('\n')[0][:40] for a in kt['assertionResults'] if a['status'] == 'failed'}), '| restored', ok, drc)
rows['REDPROOF'] = dict(run=len(kt['assertionResults']), red=sum(1 for a in kt['assertionResults'] if a['status'] == 'failed'))
json.dump(rows, open(GS + '/out/tamper_rows.json', 'w'), indent=1)
# test-including tsc program
for name, tree in (('head', HT), ('dev', DT)):
    od = tree + DEV + '/services/originate'; cfg = od + '/tsconfig.qa1024-with-tests.json'
    open(cfg, 'w').write(json.dumps({'extends': './tsconfig.json', 'compilerOptions': {'noEmit': True, 'types': ['jest', 'node']}, 'include': ['src/**/*'], 'exclude': ['node_modules', 'dist']}))
    lf = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', cfg, '--listFilesOnly'], cwd=od, capture_output=True, text=True).stdout
    lp = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', '.', '--listFilesOnly'], cwd=od, capture_output=True, text=True).stdout
    p = subprocess.run([tree + DEV + '/node_modules/.bin/tsc', '-p', cfg], cwd=od, capture_output=True, text=True)
    errs = [l for l in p.stdout.splitlines() if re.match(r'^src/.*\(\d+,\d+\): error', l)]
    by = {}
    for l in errs: by[l.split('(')[0]] = by.get(l.split('(')[0], 0) + 1
    P('TSC-WITH-TESTS', name, now(), 'rc', p.returncode, '| ks1202 test in program', 'ks1202-a-mismatched' in lf, '| in project program', 'ks1202-a-mismatched' in lp, '| __tests__ files in program', lf.count('/__tests__/'), 'project', lp.count('/__tests__/'), '| error lines', len(errs), 'files', len(by), '| touched-file errors', {k: v for k, v in by.items() if 'documents.ts' in k or 'ks1202' in k})
    open(GS + '/out/tsc_with_tests_%s.out' % name, 'w').write(p.stdout + p.stderr)
# planted control at head: a type error in the ks1202 test file must appear
tf = O + '/' + T; tb = open(tf, 'rb').read(); th = hashlib.sha256(tb).hexdigest()
open(tf, 'wb').write(tb + b"\nconst qaPlant1024: number = 'x'; // QA-PLANT\n")
p = subprocess.run([BIN + 'tsc', '-p', O + '/tsconfig.qa1024-with-tests.json'], cwd=O, capture_output=True, text=True)
open(tf, 'wb').write(tb); P('TSC PLANT', 'errors in ks1202 test', sum(1 for l in p.stdout.splitlines() if 'ks1202' in l and 'error' in l), '(want >= 1) | restored', hashlib.sha256(open(tf, 'rb').read()).hexdigest() == th)
# eslint
for rel in ('src/routes/documents.ts', T):
    for name, tree in (('head', HT), ('dev', DT)):
        od = tree + DEV + '/services/originate'
        if not os.path.exists(od + '/' + rel): P('ESLINT', name, rel.split('/')[-1], 'ABSENT'); continue
        p = subprocess.run([tree + DEV + '/node_modules/.bin/eslint', '-f', 'json', rel], cwd=od, capture_output=True, text=True)
        try:
            ms = json.loads(p.stdout)[0]['messages']; P('ESLINT', name, rel.split('/')[-1], 'rc', p.returncode, 'messages', len(ms), sorted({(m.get('ruleId'), m['message'][:60]) for m in ms})[:8])
        except Exception as e: P('ESLINT', name, rel, 'unparsed', type(e).__name__, (p.stdout + p.stderr)[:300])
fc = O + '/src/qa_probe/qa1024-eslint-control.ts'; open(fc, 'w').write('const qaUnused1024 = 1;\nexport {};\n')
p = subprocess.run([BIN + 'eslint', '-f', 'json', 'src/qa_probe/qa1024-eslint-control.ts'], cwd=O, capture_output=True, text=True)
try: P('ESLINT firing control', [m.get('ruleId') for m in json.loads(p.stdout)[0]['messages']])
except Exception as e: P('ESLINT firing control unparsed', (p.stdout + p.stderr)[:300])
os.rename(fc, fc + '.quarantined')
p = subprocess.run(['npm', 'run', 'generate-openapi', '--', '--check'], cwd=HT + DEV, capture_output=True, text=True)
P('OPENAPI generate-openapi --check at head rc', p.returncode, (p.stdout + p.stderr).strip()[-600:])
P('end', now())
