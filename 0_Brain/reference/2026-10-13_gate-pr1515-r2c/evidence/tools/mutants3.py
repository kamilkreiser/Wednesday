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
 ('C1_any_module_any_code', "  /^(?:Cannot find module|Could not find a declaration file for module) '(@secuura\\/[^']+)'/;\nconst SPLIT_SPEC = /^(@secuura\\/[a-z0-9._-]+)(?:\\/(.*))?$/;",
   "  /^(?:Cannot find module|Could not find a declaration file for module) '([^']+)'/;\nconst SPLIT_SPEC = /^((?:@[^/]+\\/)?[^/]+)(?:\\/(.*))?$/;"),
 ('C3_on_disk_check_ignored', "const anyResolves = (pkgRoot, targets, kind) =>\n  targets.some(", "const anyResolves = (pkgRoot, targets, kind) => kind === 'runtime' &&\n  targets.some("),
 ('C5_corroboration_removed_scan_decides', '\n// The runtime-only note. It must never fail the check.', C6_INSERT + ' It must never fail the check.'),
 ('T1_trycatch_removed', "try {\nfor (const [pkgName, subpaths] of sourceSpecifiers(serviceDir)) {", "{\nfor (const [pkgName, subpaths] of sourceSpecifiers(serviceDir)) {"),
 ('T1b_trycatch_swallows_fatal_too', "if (staleFatal.length > 0) {\n  const pkgs", "if (false) {\n  const pkgs"),
 ('K1_code_check_removed_anchor_kept', "  if (e.code !== 'TS2307' && e.code !== 'TS7016') continue;\n", ""),
 ('K2_anchor_removed_code_kept', "  /^(?:Cannot find module|Could not find", "  /(?:Cannot find module|Could not find"),
 ('F1_isFile_guard_removed', "      if (!e.isFile()) continue;\n", ""),
 ('S1_size_cap_removed', "      try { if (fs.statSync(f).size > SCAN_MAX_BYTES) continue; } catch { continue; }\n", ""),
 ('S2_size_cap_ignores_error_branch_to_read', "const SCAN_MAX_BYTES = 4 * 1024 * 1024;", "const SCAN_MAX_BYTES = 64 * 1024 * 1024;"),
 ('A9_star_head_off_by_one', '    const head = k.slice(0, -1);', '    const head = k.slice(0, -2);'),
 ('A11_first_target_only', "  targets.some((t) => variantsOf(t, kind).some((v) => fs.existsSync(path.join(pkgRoot, v))));", "  targets.slice(0, 1).some((t) => variantsOf(t, kind).some((v) => fs.existsSync(path.join(pkgRoot, v))));"),
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
    c = src.count(old)
    if c != 1: print(mid, 'ANCHOR COUNT', c); continue
    open(CK, 'w').write(src.replace(old, new))
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
