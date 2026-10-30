#!/usr/bin/env python3
"""Gate 24 mutants of the api-gateway Dockerfile vs the KS-1823 text test.
usage: python3 -I mutants.py <clone>   (restores the Dockerfile by sha256 after each mutant)"""
import hashlib, subprocess, sys, pathlib
clone = pathlib.Path(sys.argv[1])
pkg = clone / 'Blockchain/Dev/services/api-gateway'
df = pkg / 'Dockerfile'
vitest = clone / 'Blockchain/Dev/node_modules/.bin/vitest'
test = 'src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts'
orig = df.read_bytes(); h0 = hashlib.sha256(orig).hexdigest()
RM = 'RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*\n'
COPY = 'COPY docs/openapi/ ./docs/openapi/\n'
BUILD = 'RUN npm run build\n'
FINAL_COPY = 'COPY --from=builder /app/docs/openapi ./docs/openapi\n'
M = {
 'M1 rm line commented out': (RM, '# ' + RM),
 'M2 rm moved after npm run build (same stage)': (RM + '# Relax strict unused-variable checks for production build\n# Build TypeScript\n' + BUILD,
     '# Relax strict unused-variable checks for production build\n# Build TypeScript\n' + BUILD + RM),
 'M3 rm moved to runtime stage after final COPY': (RM, None),
 'M4 second spec COPY re-added after the rm (re-imports backups)': (RM, RM + COPY),
 'M5 runtime stage ALSO copies docs/openapi from the build context': (FINAL_COPY, FINAL_COPY + 'COPY docs/openapi/ ./docs/openapi/\n'),
 'M6 rm without -f (unmatched glob fails the build)': (RM, RM.replace('rm -f', 'rm')),
 'M7 rm -f with || true appended': (RM, RM.rstrip('\n') + ' || true\n'),
}
res = []
for name, (a, b) in M.items():
    s = orig.decode()
    assert s.count(a) == 1, (name, s.count(a))
    if b is None:  # M3
        s = s.replace(a, '').replace(FINAL_COPY, FINAL_COPY + RM)
    else:
        s = s.replace(a, b)
    df.write_text(s)
    p = subprocess.run([str(vitest), 'run', '--root', str(pkg), test], capture_output=True, text=True)
    out = p.stdout + p.stderr
    line = [l.strip() for l in out.splitlines() if 'Tests ' in l]
    verdict = 'KILLED' if p.returncode != 0 else 'SURVIVED'
    res.append(f'{name}: {verdict} rc={p.returncode} {line[-1] if line else "?"}')
    df.write_bytes(orig)
    assert hashlib.sha256(df.read_bytes()).hexdigest() == h0
print('\n'.join(res)); print('restored sha256', h0)
