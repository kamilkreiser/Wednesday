# My mutant driver: the author's 12 mutant anchors (read from their file as DATA, read-only) + my own, applied to MY scratch copy.
import hashlib, re, subprocess, sys, ast
S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ad6cb59d-4a2f-44e5-b355-5685c7d2a2e1/scratchpad/g1515d'
W = S + '/head/Blockchain/Dev'
C = W + '/scripts/typecheck-tests/check.cjs'
P = open(C, encoding='utf8').read()
BASE = hashlib.sha256(P.encode()).hexdigest()[:16]
src = open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-12_seatV-5th/tools/mutants1517r2.py', encoding='utf8').read()
M = None
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'M':
        M = ast.literal_eval(node.value)
MINE = [
 ("X1 quoteAt off by one (filter rejects every real specifier)",
  "const quoteAt = m.index + m[0].indexOf(m[1]) - 1;", "const quoteAt = m.index + m[0].indexOf(m[1]);"),
 ("X2 backslash escape consumes 1 char, not 2",
  "if (src[i] === '\\\\') { i += 2; continue; }", "if (src[i] === '\\\\') { i += 1; continue; }"),
 ("X3 a newline no longer ends a ' or \" string",
  "        if (src[i] === '\\n' && q !== '`') { i += 1; break; }\n", ""),
 ("X4 EVERY array entry must resolve (not ANY)",
  "const resolved = targets.some((t) =>", "const resolved = targets.every((t) =>"),
 ("X5 candidates() keeps only the first array entry",
  "  if (Array.isArray(v)) return v.flatMap(candidates);", "  if (Array.isArray(v)) return v.length ? candidates(v[0]) : [];"),
 ("X6 block comments not recorded as ranges",
  "      i = Math.min(i + 2, N); comments.push([s0, i]); continue;", "      i = Math.min(i + 2, N); continue;"),
]
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
LIST = (M if which in ('all', 'author') else []) + (MINE if which in ('all', 'mine') else [])
def cells():
    r = subprocess.run(['node', W + '/node_modules/vitest/vitest.mjs', 'run',
        'src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts', '-t', 'KS-1517'],
        cwd=W + '/services/auth', capture_output=True, text=True)
    o = r.stdout + r.stderr; m = re.search(r'^\s+Tests\s+(.*)$', o, re.M)
    return r.returncode, (m.group(1).strip() if m else 'NO TESTS LINE')
print('baseline sha256/16:', BASE, flush=True)
rc, l = cells(); print('UNMUTATED rc=%d | %s' % (rc, l), flush=True)
killed = 0; n = 0
try:
    for name, old, new in LIST:
        if P.count(old) != 1:
            print('%-58s ANCHOR MISS (%d)' % (name, P.count(old)), flush=True); continue
        n += 1
        open(C, 'w', encoding='utf8').write(P.replace(old, new, 1))
        rc, l = cells()
        open(C, 'w', encoding='utf8').write(P)
        ok = hashlib.sha256(open(C, encoding='utf8').read().encode()).hexdigest()[:16] == BASE
        killed += rc != 0
        print('%-58s %-12s restored=%s | %s' % (name, 'KILLED' if rc else 'SURVIVED', ok, l), flush=True)
finally:
    open(C, 'w', encoding='utf8').write(P)
print('KILLED %d / %d; final sha256/16 %s' % (killed, n, hashlib.sha256(open(C, encoding='utf8').read().encode()).hexdigest()[:16]))
