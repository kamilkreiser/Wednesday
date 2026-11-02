# mutants.py : per guard occurrence (7) x 5 mutant forms, product only, tests untouched, sha-restored each run
import re, subprocess, hashlib, json, sys, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate113-ks1868-pr1931'
D = W + '/repo/Blockchain/Dev'; SRC = D + '/services/auth/src/routes/'
OUT = W + '/logs/mutants_run.json'
PAT = re.compile(r"let reason: string;\n(\s*)try \{\n\s*reason = (.+?);\n(\s*)\} catch \{\n\s*reason = 'unreadable thrown value';\n\s*\}")
sha = lambda b: hashlib.sha256(b).hexdigest()
def forms(m):
    ind, rhs = m.group(1), m.group(2)
    var = re.match(r'\(?(\w+)', rhs).group(1)
    c = ind[:-2] if len(ind) >= 2 else ''
    g = lambda tbody, cbody: f"let reason: string;\n{ind}try {{\n{ind}  {tbody}\n{c}}} catch {{\n{ind}  {cbody}\n{c}}}"
    return {
        'undo_guard': f"let reason: string = {rhs};",
        'fallback_rethrows': g(f"reason = {rhs};", "throw new Error('mutant');"),
        'wrong_constant': g(f"reason = {rhs};", "reason = 'x';"),
        'always_constant': g("reason = 'unreadable thrown value';", "reason = 'unreadable thrown value';"),
        'fallback_reads_value': g(f"reason = {rhs};", f"reason = String({var});"),
    }
results = []
for fn in ('auth.ts', 'internal.ts', 'issuerCerts.ts', 'oauth.ts'):
    p = SRC + fn; orig = open(p, 'rb').read(); h0 = sha(orig); txt = orig.decode()
    ms = list(PAT.finditer(txt))
    for k, m in enumerate(ms):
        for name, rep in forms(m).items():
            mut = txt[:m.start()] + rep + txt[m.end():]
            open(p, 'w').write(mut)
            jf = W + '/logs/_mut.json'
            subprocess.run([D + '/node_modules/.bin/vitest', 'run', '--root', D + '/services/auth', 'ks1868-internal', 'ks1868-oauth', 'ks1868-issuer-certs', 'ks1868-auth-rehash', '--reporter=json', '--outputFile=' + jf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            open(p, 'wb').write(orig)
            ok = sha(open(p, 'rb').read()) == h0
            try:
                d = json.load(open(jf)); red = [f"{os.path.basename(f['name']).split('-')[1]}:{a['title'].split()[2]}" for f in d['testResults'] for a in f['assertionResults'] if a['status'] != 'passed']
                tot = d['numTotalTests']
            except Exception as e:
                red = ['NO_JSON ' + str(e)]; tot = 0
            r = {'file': fn, 'site': k, 'line': txt[:m.start()].count('\n') + 1, 'mutant': name, 'red': red, 'total': tot, 'restored': ok}
            results.append(r); print(json.dumps(r), flush=True)
            if not ok: sys.exit('RESTORE FAIL')
json.dump(results, open(OUT, 'w'), indent=1)
print('killed', sum(1 for r in results if r['red']), 'of', len(results))
