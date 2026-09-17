#!/usr/bin/env python3
"""drafter_tamper.py ROW... — the seat's 5 rows + the gate's own tampers on the HEAD tree (8b8996f8b; api-gateway tree b4f66d471) of the drafter clone.
Derived from the #1017 set's drafter_tamper.py. Each row: text anchor count asserted = 1, marker asserted = 1, project tsc --noEmit -p . rc (a
non-compiling tamper is VOID), WHOLE api-gateway suite with the denominator asserted 54/481 pending 0, restore from saved bytes with sha256 == git HEAD
blob and `git diff --quiet` asserted. Never rm; stderr kept per run."""
import os, sys, json, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drafter_run as R
TREE = 'head'; WT = R.T[TREE]; GWP = WT + '/' + R.GW
PX = 'src/routes/proxy.ts'
DEN = (54, 481)
CALL = "    const { verdict, canonicalPath } = erasureDoorVerdict(collapseRepeatedSlashes(original), erasureDoorCaseSensitive);\n"
CS = "  const erasureDoorCaseSensitive = Boolean((erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive);\n"
BRANCHES = "    if (verdict === 'not-door') {\n      next();\n      return;\n    }\n    if (verdict === 'undetermined') {\n"
RESTORE = "      req.url = original;\n      next(err as Error | undefined);\n"
ROWS = {
 'T0': (None, None, None, 'READY 0'),
 'T739': (PX, CALL, "    void collapseRepeatedSlashes; const qaQ = original.indexOf('?'); const { verdict, canonicalPath } = erasureDoorVerdict((qaQ === -1 ? original : original.slice(0, qaQ)).replace(/\\/{2,}/g, '/') + (qaQ === -1 ? '' : original.slice(qaQ)), erasureDoorCaseSensitive); // QA-TAMPER-T739 whole-string collapse restored\n",
          'READY 7 (4 test-mode target-form cells, 2 production v1, the ks843 source cell)'),
 'TC': (PX, CALL, "    const { verdict, canonicalPath } = ((p: string): { verdict: string; canonicalPath: string | null } => { const s = p.replace(/^[A-Za-z][A-Za-z0-9+\\-.]*:\\/\\/[^/?#]*/, '').replace(/[?#].*$/, ''); return /^\\/erasures(\\/|$)/i.test(s) ? { verdict: 'door', canonicalPath: s } : { verdict: 'not-door', canonicalPath: null }; })(collapseRepeatedSlashes(original)); void erasureDoorCaseSensitive; // QA-TAMPER-TC canonical check removed (raw prefix match, absolute-form aware)\n",
        'READY 8 (the 5 spellings, 2 x 400, the ks843 source cell)'),
 'TW': (PX, BRANCHES, "    if (verdict === 'not-door' && false) {\n      next();\n      return;\n    }\n    if (verdict !== 'door') { // QA-TAMPER-TW the 400 widened to every non-door gdpr path\n",
        'READY 4 (3 Tightening A controls + ks843-erasure-path-bypass non-erasure path untouched)'),
 'TI': (PX, CS, "  // QA-TAMPER-TI inert comment\n" + CS, 'READY 0'),
 'G-HARDFALSE': (PX, CS, "  const erasureDoorCaseSensitive = Boolean(false && (erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive); // QA-TAMPER-GHARDFALSE the router read replaced by a constant false\n",
                 'drafter: 0 (Tightening B READ is indistinguishable from a hard-coded false while the router is case-insensitive)'),
 'G-HARDTRUE': (PX, CS, "  const erasureDoorCaseSensitive = Boolean(true || (erasureDoor as unknown as { caseSensitive?: boolean }).caseSensitive); // QA-TAMPER-GHARDTRUE the verdict case-sensitive, the router not\n",
                'drafter: the upper-case real-app cell (+ any ks843 case-shape behaviour cells)'),
 'G-ROUTERCS': (PX, "  const erasureDoor = Router();\n", "  const erasureDoor = Router({ caseSensitive: true }); // QA-TAMPER-GROUTERCS\n",
                'drafter: ks843 source pin (Router literal) + upper-case real-app cell + ks843 case-shape cells; the READ follows'),
 'G-NOCOLLAPSE': (PX, CALL, "    const { verdict, canonicalPath } = erasureDoorVerdict(original || collapseRepeatedSlashes(original), erasureDoorCaseSensitive); // QA-TAMPER-GNOCOLLAPSE\n",
                  'drafter: 1 (ks843 source pin only; the verdict drops empty segments itself)'),
 'G-NORESTORE': (PX, RESTORE, "      req.url = req.url || original; // QA-TAMPER-GNORESTORE\n      next(err as Error | undefined);\n",
                 'drafter: ks1187 admitted control (spelled forwarded canonical) + ks843 source pin'),
 'G-NODECODE': (PX, "      decoded = decodeURIComponent(raw.split(';')[0]);\n", "      decoded = raw.split(';')[0] || decodeURIComponent(''); // QA-TAMPER-GNODECODE\n",
                'drafter: percent-escape verdict + real-app cells, the undecodable 400 cells'),
 'G-NOPARAMS': (PX, "      decoded = decodeURIComponent(raw.split(';')[0]);\n", "      decoded = decodeURIComponent(raw); // QA-TAMPER-GNOPARAMS\n",
                'drafter: ;param verdict + canonical + real-app cells'),
 'G-DOTS': (PX, "      if (segment === '' || segment === '.') continue;\n", "      if (segment === '') continue; // QA-TAMPER-GDOTS\n", 'drafter: dot-segment verdict + real-app cells'),
 'G-CLIMB': (PX, "        if (segments.length === 0) return { verdict: 'undetermined', canonicalPath: null };\n", "        if (segments.length === 0) continue; // QA-TAMPER-GCLIMB\n",
             'drafter: the climbing verdict cells + the climbing 400 real-app cell'),
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def blob_ok(rel):
    b = subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD:' + R.GW + '/' + rel], capture_output=True, text=True).stdout.strip()
    h = subprocess.run(['git', 'hash-object', GWP + '/' + rel], capture_output=True, text=True).stdout.strip()
    return b == h, b[:9], h[:9]
results = []
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
    trc = R.tsc(TREE)
    r = R.vitest(TREE, [], 'tamper_%s' % row)
    if rel:
        open(p, 'wb').write(saved); ok, b, h = blob_ok(rel); R.P('restore sha256 identical', sha(p) == before, 'HEAD blob', b, 'worktree', h, ok); assert ok and sha(p) == before
    dq = subprocess.run(['git', '-C', WT, 'diff', '--quiet'], capture_output=True, text=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
    den_ok = bool(r) and (r['files'], r['tests']) == DEN and r['pending'] == 0
    R.P('DENOMINATOR', (r['files'], r['tests']) if r else None, 'expected', DEN, 'pending', r and r['pending'], 'OK' if den_ok else 'DENOMINATOR-MISMATCH')
    results.append(dict(row=row, tsc_rc=trc, void=trc != 0, files=r and r['files'], tests=r and r['tests'], failed=r and r['failed'], pending=r and r['pending'], failed_suites=r and r['failed_suites'],
                        reds=[x[0].split('/')[-1] + ' :: ' + x[1] for x in (r['notpassed'] if r else [])], decisive=[x[3].split('\n')[0][:200] for x in (r['notpassed'] if r else [])], predicted_by=pred, denominator_ok=den_ok))
    json.dump(results, open(R.GS + '/tamper_head_rows.json', 'w'), indent=1)
R.P('tamper end', R.ts())
