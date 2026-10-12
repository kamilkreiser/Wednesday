import subprocess, hashlib, sys, re, json, os
S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3'
D = S + '/mut/Blockchain/Dev'
CK = D + '/scripts/typecheck-tests/check.cjs'
ORIG = open(CK, 'rb').read()
SHA = hashlib.sha256(ORIG).hexdigest()
assert SHA.startswith('c862a80d1b3ace00'), SHA
SUITE = 'src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts'
C6_INSERT = """
for (const [pkgName, subs] of sourceSpecifiers(serviceDir)) { const found = packageJsonOf(pkgName); if (!found) continue;
  for (const sub of subs) { const t = declTargetsFor(found.pkg, sub); if (t.length && !anyResolves(found.pkgRoot, t, 'declaration') && t.some((x) => isJudgeable(x, 'declaration')))
    staleFatal.push({ pkgName, rel: t.map(stripDot).join(' or '), asImported: `'${pkgName}${sub ? '/' + sub : ''}'`, corroboration: 'none' }); } }
// The runtime-only note."""
M = [
 # --- the author's own mutants (anchors copied verbatim from 5_Project_History/2026-10-12_seatV-5th/tools/mutants1517r3.py)
 ('G2_secuura_filter_removed', "  if (!m) continue;                                  // not an @secuura module: never ours to reinterpret",
  "  if (false) { continue; }\n  if (!m) { staleFatal.push({pkgName:'@secuura/shared',rel:'(forced)',asImported:\"'forced'\",corroboration:e.code}); continue; }"),
 ('G3_no_declared_target_fatal', "  if (targets.length === 0) continue;", "  if (targets.length === 0) { staleFatal.push({pkgName,rel:'(none declared)',asImported:`'${m[1]}'`,corroboration:e.code}); continue; }"),
 ('G4_resolving_target_called_missing', "  if (anyResolves(found.pkgRoot, targets, 'declaration')) continue; // a real error, not a stale build", "  if (false) continue;"),
 ('G5_uninstalled_fatal', "  if (!found) continue;  // FATAL-SIDE: not installed, so leg 1 owns it", "  if (!found) { staleFatal.push({pkgName,rel:'(uninstalled)',asImported:`'${m[1]}'`,corroboration:e.code}); continue; }"),
 ('G6_variants_removed', "  for (const e of SUFFIX[kind]) { out.push(rel + e); out.push(path.posix.join(rel, 'index' + e)); }", "  // variants removed"),
 ('G9_die1', "  die(2, lines.join('\\n'));", "  die(1, lines.join('\\n'));"),
 ('G10_note_made_fatal', "    staleNotes.push({ pkgName, rel: judgeable.map(stripDot).join(' or '), asImported: `'${pkgName}${sub ? '/' + sub : ''}'` });",
  "    staleFatal.push({ pkgName, rel: judgeable.map(stripDot).join(' or '), asImported: `'${pkgName}${sub ? '/' + sub : ''}'`, corroboration: 'forced' });"),
 ('G12_scan_node_modules_dist', "      if (e.name === 'node_modules' || e.name === 'dist' || e.name.startsWith('.')) continue;", "      if (e.name.startsWith('.')) continue;"),
 # --- mine (non-corroboration)
 ('A9_star_head_off_by_one', '    const head = k.slice(0, -1);', '    const head = k.slice(0, -2);'),
 ('A11_first_target_only', "  targets.some((t) => variantsOf(t, kind).some((v) => fs.existsSync(path.join(pkgRoot, v))));", "  targets.slice(0, 1).some((t) => variantsOf(t, kind).some((v) => fs.existsSync(path.join(pkgRoot, v))));"),
 # --- my corroboration mutants
 ('C1_any_module_any_code_TS7016_or_2307', "  /(?:Cannot find module|Could not find a declaration file for module) '(@secuura\\/[^']+)'/;\nconst SPLIT_SPEC = /^(@secuura\\/[a-z0-9._-]+)(?:\\/(.*))?$/;",
   "  /(?:Cannot find module|Could not find a declaration file for module) '([^']+)'/;\nconst SPLIT_SPEC = /^((?:@[^/]+\\/)?[^/]+)(?:\\/(.*))?$/;"),
 ('C2_TS2307_any_module', "  /(?:Cannot find module|Could not find a declaration file for module) '(@secuura\\/[^']+)'/;\nconst SPLIT_SPEC = /^(@secuura\\/[a-z0-9._-]+)(?:\\/(.*))?$/;",
   "  /(?:Cannot find module '(?=[^']+')|Could not find a declaration file for module '(?=@secuura\\/))([^']+)'/;\nconst SPLIT_SPEC = /^((?:@[^/]+\\/)?[^/]+)(?:\\/(.*))?$/;"),
 ('C3_on_disk_check_ignored', "const anyResolves = (pkgRoot, targets, kind) =>\n  targets.some(", "const anyResolves = (pkgRoot, targets, kind) => kind === 'runtime' &&\n  targets.some("),
 ('C4_any_mention_of_specifier', "  /(?:Cannot find module|Could not find a declaration file for module) '(@secuura\\/[^']+)'/;", "  /(@secuura\\/[^'\"\\s]+)/;"),
 ('C5_ignore_diagnostic_entirely_scan_decides', '\n// The runtime-only note.', C6_INSERT),
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
