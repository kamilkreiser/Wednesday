import subprocess, hashlib, sys, re, json, os
S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3'
D = S + '/mut/Blockchain/Dev'
CK = D + '/scripts/typecheck-tests/check.cjs'
ORIG = open(CK, 'rb').read()
SHA = hashlib.sha256(ORIG).hexdigest()
assert SHA.startswith('458b26cdb851efe0'), SHA
SUITE = 'src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts'
C6_INSERT = """
for (const [pkgName, subs] of sourceSpecifiers(serviceDir)) { const found = packageJsonOf(pkgName); if (!found) continue;
  for (const sub of subs) { const t = declTargetsFor(found.pkg, sub); if (t.length && !anyResolves(found.pkgRoot, t, 'declaration') && t.some((x) => isJudgeable(x, 'declaration')))
    staleFatal.push({ pkgName, rel: t.map(stripDot).join(' or '), asImported: `'${pkgName}${sub ? '/' + sub : ''}'`, corroboration: 'none' }); } }
// The runtime-only note."""
M = [
 ('T1_trycatch_removed_VALID_both_anchors', [("try {\nfor (const [pkgName, subpaths] of sourceSpecifiers(serviceDir)) {", "{\nfor (const [pkgName, subpaths] of sourceSpecifiers(serviceDir)) {"),
   ("} catch {\n  // Advisory only: a note we cannot compute is a note we do not print. Never a failure.\n}", "}")], None),
 ('K3_code_check_AND_anchor_both_removed', [("  if (e.code !== 'TS2307' && e.code !== 'TS7016') continue;\n", ""), ("  /^(?:Cannot find module|Could not find", "  /(?:Cannot find module|Could not find")], None),
 ('T2_catch_swallows_into_exit0_control', [("} catch {\n  // Advisory only: a note we cannot compute is a note we do not print. Never a failure.\n}", "} catch { process.exit(0); }")], None),
]
def score(tag):
    r = subprocess.run([D + '/node_modules/.bin/vitest', 'run', SUITE, '-t', 'KS-1517', '--reporter=json', '--outputFile=' + S + f'/out/mut_{tag}.json'], cwd=D + '/services/auth', capture_output=True, text=True)
    j = json.load(open(S + f'/out/mut_{tag}.json'))
    res = [t for f in j['testResults'] for t in f['assertionResults'] if t['status'] in ('passed', 'failed')]
    failed = [t['title'][:80] for t in res if t['status'] == 'failed']
    return len(res), failed
only = set(sys.argv[1:])
n, failed = score('BASELINE')
print('BASELINE unmutated:', n, 'cells,', len(failed), 'failed', failed); sys.stdout.flush()
assert not failed, 'baseline not green'
results = {}
for mid, old, new in M:
    if only and mid not in only: continue
    src = ORIG.decode()
    pairs = old if isinstance(old, list) else [(old, new)]
    bad = [(o, src.count(o)) for o, n_ in pairs if src.count(o) != 1]
    if bad: print(mid, 'ANCHOR COUNT', [b[1] for b in bad]); continue
    mutated = src
    for o, n_ in pairs: mutated = mutated.replace(o, n_)
    assert mutated != src
    open(CK, 'w').write(mutated)
    try:
        n, failed = score(mid)
    finally:
        open(CK, 'wb').write(ORIG)
    assert hashlib.sha256(open(CK, 'rb').read()).hexdigest() == SHA
    results[mid] = failed
    print(mid, 'KILLED' if failed else 'SURVIVED', f'{len(failed)}/{n}', failed[:3]); sys.stdout.flush()
print('restored sha256/16', hashlib.sha256(open(CK, 'rb').read()).hexdigest()[:16])
n, failed = score('BASELINE_AFTER')
print('BASELINE after:', n, 'cells,', len(failed), 'failed')
