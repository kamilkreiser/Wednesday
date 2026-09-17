#!/usr/bin/env python3
"""tampers.py ROW... — #1019 gate tampers on THIS gate's HEAD tree (8b8996f8b; api-gateway tree b4f66d471). Each row: tracked porcelain asserted 0 before;
text anchor count asserted = 1 (Python str.count); marker asserted = 1; project `tsc --noEmit -p .` rc (a non-compiling tamper is VOID); WHOLE api-gateway
suite, denominator asserted 54/481 pending 0; restore from saved bytes, sha256 == pre-tamper AND worktree blob == git HEAD blob AND `git diff --quiet`.
Forms are the drafter's (brief item 7 table) so the counts are comparable, plus the gate's own W-aimed rows. predicted-by stated per row. Never rm."""
import os, sys, json, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run as R
TREE = 'head'; WT = R.T[TREE]; GWP = WT + '/' + R.GW
PX = 'src/routes/proxy.ts'
DEN = (54, 481)
CALL = "    const { verdict, canonicalPath } = erasureDoorVerdict(collapseRepeatedSlashes(original), erasureDoorCaseSensitive);\n"
CS = "  const erasureDoorCaseSensitive = Boolean((erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive);\n"
BRANCHES = "    if (verdict === 'not-door') {\n      next();\n      return;\n    }\n    if (verdict === 'undetermined') {\n"
RESTORE = "      req.url = original;\n      next(err as Error | undefined);\n"
POP = "      if (segment === '..') {\n        if (segments.length === 0) return { verdict: 'undetermined', canonicalPath: null };\n"
ROWS = {
 'T0': (None, None, None, 'seat 0 / drafter 0'),
 'T739': (PX, CALL, "    void collapseRepeatedSlashes; const qaQ = original.indexOf('?'); const { verdict, canonicalPath } = erasureDoorVerdict((qaQ === -1 ? original : original.slice(0, qaQ)).replace(/\\/{2,}/g, '/') + (qaQ === -1 ? '' : original.slice(qaQ)), erasureDoorCaseSensitive); // QA-TAMPER-T739 whole-string collapse restored\n", 'seat 7 / drafter 7'),
 'TC': (PX, CALL, "    const { verdict, canonicalPath } = ((p: string): { verdict: string; canonicalPath: string | null } => { const s = p.replace(/^[A-Za-z][A-Za-z0-9+\\-.]*:\\/\\/[^/?#]*/, '').replace(/[?#].*$/, ''); return /^\\/erasures(\\/|$)/i.test(s) ? { verdict: 'door', canonicalPath: s } : { verdict: 'not-door', canonicalPath: null }; })(collapseRepeatedSlashes(original)); void erasureDoorCaseSensitive; // QA-TAMPER-TC canonical check removed (raw prefix match, absolute-form aware)\n", 'seat 8 / drafter 8'),
 'TW': (PX, BRANCHES, "    if (verdict === 'not-door' && false) {\n      next();\n      return;\n    }\n    if (verdict !== 'door') { // QA-TAMPER-TW the 400 widened to every non-door gdpr path\n", 'seat 4 / drafter 4'),
 'TI': (PX, CS, "  // QA-TAMPER-TI inert comment\n" + CS, 'seat 0 / drafter 0'),
 'G-HARDFALSE': (PX, CS, "  const erasureDoorCaseSensitive = Boolean(false && (erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive); // QA-TAMPER-GHARDFALSE\n", 'drafter 0'),
 'G-HARDTRUE': (PX, CS, "  const erasureDoorCaseSensitive = Boolean(true || (erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive); // QA-TAMPER-GHARDTRUE\n", 'drafter 3'),
 'G-ROUTERCS': (PX, "  const erasureDoor = Router();\n", "  const erasureDoor = Router({ caseSensitive: true }); // QA-TAMPER-GROUTERCS\n", 'drafter 5'),
 'G-NOCOLLAPSE': (PX, CALL, "    const { verdict, canonicalPath } = erasureDoorVerdict(original || collapseRepeatedSlashes(original), erasureDoorCaseSensitive); // QA-TAMPER-GNOCOLLAPSE\n", 'drafter 1'),
 'G-NORESTORE': (PX, RESTORE, "      req.url = req.url || original; // QA-TAMPER-GNORESTORE\n      next(err as Error | undefined);\n", 'drafter 1'),
 'G-NODECODE': (PX, "      decoded = decodeURIComponent(raw.split(';')[0]);\n", "      decoded = raw.split(';')[0] || decodeURIComponent(''); // QA-TAMPER-GNODECODE\n", 'drafter 6'),
 'G-NOPARAMS': (PX, "      decoded = decodeURIComponent(raw.split(';')[0]);\n", "      decoded = decodeURIComponent(raw); // QA-TAMPER-GNOPARAMS\n", 'drafter 3'),
 'G-DOTS': (PX, "      if (segment === '' || segment === '.') continue;\n", "      if (segment === '') continue; // QA-TAMPER-GDOTS\n", 'drafter 2'),
 'G-CLIMB': (PX, "        if (segments.length === 0) return { verdict: 'undetermined', canonicalPath: null };\n", "        if (segments.length === 0) continue; // QA-TAMPER-GCLIMB\n", 'drafter 3'),
 # the gate's own, aimed at the W class (dot segment after erasures)
 'Q-WFIX': (PX, POP, "      if (segment === '..') {\n        if (segments.length === 0 || (typeof segments[0] === 'string' && (caseSensitive ? segments[0] : segments[0].toLowerCase()) === 'erasures')) return { verdict: 'undetermined', canonicalPath: null }; // QA-TAMPER-QWFIX fix-shaped: a .. once the first segment names the door is undetermined\n",
            'gate (me) 0: no existing cell has a dot segment after erasures, so the fix-shaped direction is unpinned'),
 'Q-WPOPFIRST': (PX, POP, "      if (segment === '..') {\n        if (segments.length === 1) continue; // QA-TAMPER-QWPOPFIRST a .. may never pop the first segment (widens the door)\n        if (segments.length === 0) return { verdict: 'undetermined', canonicalPath: null };\n",
            'gate (me) >=1: U03 consent/../../erasures style climbing cells change verdict; the W direction itself still unpinned'),
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def blob_ok(rel):
    b = subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD:' + R.GW + '/' + rel], capture_output=True, text=True).stdout.strip()
    h = subprocess.run(['git', 'hash-object', GWP + '/' + rel], capture_output=True, text=True).stdout.strip()
    return b == h, b[:9], h[:9]
out = R.EV + '/tampers_table.json'
results = json.load(open(out)) if os.path.exists(out) else []
for row in sys.argv[1:]:
    rel, old, new, pred = ROWS[row]
    R.P('ROW-START', row, TREE, R.ts(), 'predicted-by', pred)
    dq0 = subprocess.run(['git', '-C', WT, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); R.P('tracked porcelain before', len(dq0.stdout.splitlines())); assert not dq0.stdout.strip()
    if rel:
        p = GWP + '/' + rel; s = open(p).read(); saved = open(p, 'rb').read(); before = sha(p)
        c = s.count(old); R.P('anchor count', c); assert c == 1
        open(p, 'w').write(s.replace(old, new))
        mk = [w for w in new.split() if w.startswith('QA-TAMPER-')][0]
        mc = open(p).read().count(mk); R.P('marker', mk, 'count', mc); assert mc == 1
    try:
        trc = R.tsc(TREE)
        r = R.vitest(TREE, [], 'tamper_%s' % row)
    finally:
        if rel:
            open(p, 'wb').write(saved); ok, b, h = blob_ok(rel); R.P('restore sha256 identical', sha(p) == before, 'HEAD blob', b, 'worktree', h, ok); assert ok and sha(p) == before
    dq = subprocess.run(['git', '-C', WT, 'diff', '--quiet'], capture_output=True, text=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
    den_ok = bool(r) and (r['files'], r['tests']) == DEN and r['pending'] == 0
    R.P('DENOMINATOR', (r['files'], r['tests']) if r else None, 'expected', DEN, 'pending', r and r['pending'], 'OK' if den_ok else 'DENOMINATOR-MISMATCH')
    results.append(dict(row=row, form=(new or '').strip()[:400], tsc_rc=trc, void=trc != 0, files=r and r['files'], tests=r and r['tests'], failed=r and r['failed'], pending=r and r['pending'],
                        failed_suites=r and r['failed_suites'], reds=[x[0].split('/')[-1] + ' :: ' + x[1] for x in (r['notpassed'] if r else [])],
                        decisive=[x[3].split('\n')[0][:220] for x in (r['notpassed'] if r else [])], predicted_by=pred, denominator_ok=den_ok, at=R.ts()))
    json.dump(results, open(out, 'w'), indent=1)
R.P('tamper end', R.ts())
