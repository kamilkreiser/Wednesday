#!/usr/bin/env python3
"""drafter_tamper.py ROW... — the seat's 7 rows + the gate's 3 tampers on the HEAD tree (9ba0caf78) of the drafter clone. Derived from the round-1 GATE's tamper.py
(anchors for TA/TW/TK/TR/TI copied from it; enforcement.ts's product lines are unchanged r1 -> r2, only the why-comment moved). Each row: text anchor count
asserted = 1, marker asserted = 1, project tsc --noEmit -p . rc (a non-compiling tamper is VOID), whole api-gateway suite with the denominator asserted 49/428
pending 0, restore from saved bytes with sha256 == git HEAD blob and `git diff --quiet` asserted. Optional SPELL=<rows> runs the spellings harness under the tamper.
Never rm; stderr kept per run."""
import os, sys, json, hashlib, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drafter_run as R
TREE = 'head'; WT = R.T[TREE]; GWP = WT + '/' + R.GW
ENF = 'src/services/enforcement.ts'; VER = 'src/routes/verification.ts'
DEN = (49, 428)
FIX = "        const requestedType = body.documentType || body.type;\n"
ROWS = {
 'T0': (None, None, None, 'READY 0'),
 'TF': (VER, FIX, "        const requestedType = body.documentType; // QA-TAMPER-TF fix reverted\n", 'READY 1 (F1)'),
 'TA': (ENF, "  const userRank = userIdx === -1 ? 0 : userIdx;\n", "  const userRank = userIdx; // QA-TAMPER-TA ranking reverted\n", 'READY 4 (A1, A3, D-SSD, F3)'),
 'TW': (ENF, "  const userRank = userIdx === -1 ? 0 : userIdx;\n", "  const userRank = userIdx === -1 ? 99 : userIdx; // QA-TAMPER-TW unknown satisfies everything\n", 'READY 4 (A2, A3, D-standard, E-gated)'),
 'TK': (ENF, "  return userRank >= reqIdx;\n", "  return userRank > reqIdx; // QA-TAMPER-TK\n", "READY 9 (round-1's 8 + F3)"),
 'TR': (ENF, "  return userRank >= reqIdx;\n", "  return reqIdx !== -1 && userRank >= reqIdx; // QA-TAMPER-TR unknown required fails closed\n", 'READY 1 (C)'),
 'TI': (ENF, "  const userRank = userIdx === -1 ? 0 : userIdx;\n", "  // QA-TAMPER-TI inert comment\n  const userRank = userIdx === -1 ? 0 : userIdx;\n", 'READY 0'),
 'G-F3CTRL': (VER, FIX, "        const requestedType = body.documentType || (body.type ? 'QA_TAMPER_REFUSES_EVERY_TYPE_KEY' : undefined); // QA-TAMPER-GF3CTRL\n", 'drafter: aimed at the F3 CONTROL (allowed DOCUMENT via type -> 201)'),
 'G-REV': (VER, FIX, "        const requestedType = body.type || body.documentType; // QA-TAMPER-GREV reversed precedence\n", 'drafter: reversed precedence'),
 'G-BOTH': (VER, "        if (allowedTypes.length > 0 && requestedType && !allowedTypes.includes(requestedType as string)) {\n",
            "        if (allowedTypes.length > 0 && body.documentType && body.type && !allowedTypes.includes(requestedType as string)) { // QA-TAMPER-GBOTH only when both present\n", 'drafter: allow-list only when both fields present'),
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def blob_ok(rel):
    b = subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD:' + R.GW + '/' + rel], capture_output=True, text=True).stdout.strip()
    h = subprocess.run(['git', 'hash-object', GWP + '/' + rel], capture_output=True, text=True).stdout.strip()
    return b == h, b[:9], h[:9]
results = []
SPELL = os.environ.get('SPELL', '').split(',')
for row in sys.argv[1:]:
    rel, old, new, pred = ROWS[row]
    R.P('ROW-START', row, TREE, R.ts(), 'predicted-by', pred)
    if rel:
        p = GWP + '/' + rel; s = open(p).read(); saved = open(p, 'rb').read(); before = sha(p)
        c = s.count(old); R.P('anchor count', c); assert c == 1
        open(p, 'w').write(s.replace(old, new))
        mk = new.split('// ')[-1].split()[0]; mc = open(p).read().count(mk); R.P('marker', mk, 'count', mc); assert mc == 1
    trc = R.tsc(TREE)
    r = R.vitest(TREE, [], 'tamper_%s' % row)
    if rel and row in SPELL:
        R.probe(TREE, 'qa1014r2-drafter-spellings.test.ts', 'spell_head' + row, 'rows_spell_head%s.json' % row)
    if rel:
        open(p, 'wb').write(saved); ok, b, h = blob_ok(rel); R.P('restore sha256 identical', sha(p) == before, 'HEAD blob', b, 'worktree', h, ok); assert ok and sha(p) == before
    dq = subprocess.run(['git', '-C', WT, 'diff', '--quiet'], capture_output=True, text=True); R.P('git diff --quiet rc', dq.returncode); assert dq.returncode == 0
    den_ok = bool(r) and (r['files'], r['tests']) == DEN and r['pending'] == 0
    R.P('DENOMINATOR', (r['files'], r['tests']) if r else None, 'expected', DEN, 'pending', r and r['pending'], 'OK' if den_ok else 'DENOMINATOR-MISMATCH')
    results.append(dict(row=row, tsc_rc=trc, void=trc != 0, files=r and r['files'], tests=r and r['tests'], failed=r and r['failed'], pending=r and r['pending'], failed_suites=r and r['failed_suites'],
                        reds=[x[1] for x in (r['notpassed'] if r else [])], decisive=[x[3].split('\n')[0][:160] for x in (r['notpassed'] if r else [])], predicted_by=pred, denominator_ok=den_ok))
    json.dump(results, open(R.GS + '/tamper_head_%s.json' % '_'.join(sys.argv[1:])[:80], 'w'), indent=1)
R.P('tamper end', R.ts())
