import hashlib, json, re, subprocess, sys
S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/eaa04c5f-0a63-4ff7-879d-d52477f7a663/scratchpad/g1512'
A = S + '/head/Blockchain/Dev/services/api-gateway'
P = A + '/src/routes/platform.ts'
T = 'src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts'
ORIG = open(P).read()
SHA = hashlib.sha256(ORIG.encode()).hexdigest()[:16]

LOGLINE = [l for l in ORIG.split('\n') if l.strip().startswith("logger.error('Document lookup failed")][0]
EXPR = LOGLINE[LOGLINE.index('{ error: ') + 9: LOGLINE.rindex(' });')]
assert EXPR.startswith('err instanceof Error') and EXPR.endswith("typeof err"), EXPR

def rep(src, old, new, n=1):
    assert src.count(old) == n, (old, src.count(old))
    return src.replace(old, new)

L = {'L1', 'L2', 'L3', 'L4'}
muts = []  # name, fn(src)->src, expected red set
muts.append(('B1 log removed', lambda s: rep(s, LOGLINE + '\n', ''), L))
muts.append(('B2 String(err)', lambda s: rep(s, EXPR, 'String(err)'), {'L3', 'L4'}))
muts.append(('B3 object logs values (JSON.stringify)', lambda s: rep(s, "Object.keys(err).join(', ')", 'JSON.stringify(err)'), {'L3'}))
muts.append(('B4 object logs type only', lambda s: rep(s, " + ' with fields [' + Object.keys(err).join(', ') + ']'", ''), {'L3'}))
muts.append(('B5 thrown text leaks to client', lambda s: rep(s, "message: 'Document lookup failed' } });\n      }\n    },", "message: 'Document lookup failed: ' + String((err as any)?.message ?? err) } });\n      }\n    },"), {'L1', 'L2', 'L3', 'L4', 'G1'}))
muts.append(('B6 wrong level (warn)', lambda s: rep(s, "logger.error('Document lookup failed", "logger.warn('Document lookup failed"), L))
muts.append(('B7 route name dropped from context', lambda s: rep(s, "logger.error('Document lookup failed (GET /api/platform/document-lookup)'", "logger.error('Document lookup failed'"), L))
muts.append(('B8 blanket logging on the 400 path', lambda s: rep(s, "        if (!hash && !documentId) {\n", "        if (!hash && !documentId) {\n          logger.error('Document lookup failed (GET /api/platform/document-lookup)', { error: 'bad' });\n"), {'G2'}))
muts.append(('B9 blanket logging on the 503 path', lambda s: rep(s, "        if (!platformDbUrl) {\n          return res.status(503)", "        if (!platformDbUrl) {\n          logger.error('Document lookup failed (GET /api/platform/document-lookup)', { error: 'nodb' });\n          return res.status(503)"), {'G3'}))
# mine
muts.append(('O1 log err.stack for Errors', lambda s: rep(s, LOGLINE, LOGLINE.replace("err instanceof Error ? err.message", "err instanceof Error ? err.stack")), set()))
muts.append(('O2 log the request query', lambda s: rep(s, LOGLINE, LOGLINE.replace('{ error: ', '{ query: req.query, error: ')), set()))
muts.append(('O3 log the full err object', lambda s: rep(s, LOGLINE, "        logger.error('Document lookup failed (GET /api/platform/document-lookup)', { error: err });"), L))
muts.append(('O4 swallow errors thrown by logger (try/catch around log)', lambda s: rep(s, LOGLINE, '        try {\n' + LOGLINE + '\n        } catch { /* swallow */ }'), set()))
muts.append(('O5 log twice', lambda s: rep(s, LOGLINE, LOGLINE + '\n' + LOGLINE), L))
muts.append(('O6 meta key renamed (err instead of error)', lambda s: rep(s, LOGLINE, LOGLINE.replace('{ error: ', '{ err: ')), L))
muts.append(('O7 also log on the success path', lambda s: rep(s, "          res.json({\n            success: true,\n            results:", "          logger.error('Document lookup failed (GET /api/platform/document-lookup)', { error: 'ok' });\n          res.json({\n            success: true,\n            results:"), {'G4'}))
muts.append(('O8 catch answers 502 instead of 500', lambda s: rep(s, "res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Document lookup failed' } });\n      }\n    },", "res.status(502).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Document lookup failed' } });\n      }\n    },"), {'L1', 'L2', 'L3', 'L4', 'G1'}))
muts.append(('O9 Error logs String(err) not message', lambda s: rep(s, LOGLINE, LOGLINE.replace("err instanceof Error ? err.message", "err instanceof Error ? String(err)")), set()))
muts.append(('O10 thrown string logged with prefix', lambda s: rep(s, ": typeof err === 'string' ? err :", ": typeof err === 'string' ? 'str:' + err :"), {'L2'}))
muts.append(('O11 null falls to typeof (object-branch guard dropped to Object.keys on null)', lambda s: rep(s, "typeof err === 'object' && err !== null ?", "typeof err === 'object' ?"), set()))

def run():
    out = S + '/out/mut.json'
    subprocess.run(['npx', 'vitest', 'run', T, '--reporter=json', '--outputFile=' + out], cwd=A, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    j = json.load(open(out))
    red = set(); n = 0
    for f in j['testResults']:
        for a in f['assertionResults']:
            n += 1
            if a['status'] != 'passed':
                red.add(re.search(r'KS-1510 (\w\d)', a['title']).group(1))
    return red, n

sel = sys.argv[1:]
red0, n0 = run()
print(f'CONTROL (unmutated) red={sorted(red0)} of {n0}  product sha/16={SHA}')
for name, fn, exp in muts:
    if sel and not any(name.startswith(x) for x in sel): continue
    try:
        new = fn(ORIG)
    except AssertionError as e:
        print(f'{name}: MUTATION DID NOT APPLY {e}'); continue
    open(P, 'w').write(new)
    try:
        red, n = run()
    finally:
        open(P, 'w').write(ORIG)
    sha = hashlib.sha256(open(P).read().encode()).hexdigest()[:16]
    print(f'{name}: red={sorted(red)} of {n} expected={sorted(exp)} {"EXACT" if red == exp else "DIFF"} sha {SHA}={sha} {"restored-identical" if sha == SHA else "NOT-RESTORED"}')
