#!/usr/bin/env python3
"""Gate 175 mutants on the changed catch lines of PR 1990 and PR 1991.
Each mutant edits ONE occurrence in ONE head file of the clone, runs the PR's own test file(s) for that module,
records killed/survived, and restores the head blob. Raw table -> results/mutants.tsv."""
import re, subprocess, sys, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991'
D = W + '/repo/Blockchain/Dev'
ENV = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'HOME': W + '/home', 'TMPDIR': W + '/tmp'}
PS, SS = D + '/packages/shared', D + '/services/shared'
T = 'src/__tests__/ks1868-'
SITES = {
    PS + '/src/db/auto-migrate.ts': (PS, [T + 'auto-migrate-run-migrations-catch-unreadable-throw.test.ts'],
        [('${detail}', '${err.message || err}')]),
    PS + '/src/db/tenant-context.ts': (PS, [T + 'tenant-context-get-pool-catch-unreadable-throw.test.ts'],
        [('message: reason', 'message: err.message')]),
    PS + '/src/db/tenant-pool-manager.ts': (PS, [T + 'tenant-pool-manager-refresh-configs-catch-unreadable-throw.test.ts'],
        [("tenant configs:', reason)", "tenant configs:', err.message)")]),
    PS + '/src/middleware/tenant-rate-limiter.ts': (PS, [T + 'tenant-rate-limiter-fail-open-catch-unreadable-throw.test.ts'],
        [('allowing request: ${reason}', 'allowing request: ${err.message}'), ('      next();\n    }\n  };', '    }\n  };')]),
    PS + '/src/vault/key-vault.ts': (PS, [T + 'key-vault-get-secret-catch-unreadable-throw.test.ts'],
        [('error: reason,', 'error: err.message,')]),
    SS + '/src/cache/cache-middleware.ts': (SS, [T + 'cache-middleware-lookup-catch-unreadable-throw.test.ts'],
        [('{ error: reason }', '{ error: String(error) }')]),
    SS + '/src/cache/connection-pool.ts': (SS, [T + 'connection-pool-create-remove-catches-unreadable-throw.test.ts'],
        [('error: String(error) });', 'error: String(caught) });'), ('lastError = caught as Error;', 'lastError = new Error(error);'),
         ('{ error: reason }', '{ error: String(error) }')]),
    SS + '/src/cache/redis-client.ts': (SS, [T + 'redis-client-connect-catch-unreadable-throw.test.ts'],
        [('{ error: reason }', '{ error: String(error) }')]),
    SS + '/src/security/redis-security-store.ts': (SS, [T + 'redis-rate-limit-store-get-increment-unreadable-throw.test.ts',
        T + 'redis-brute-force-store-get-set-unreadable-throw.test.ts', T + 'redis-csrf-store-generate-validate-unreadable-throw.test.ts'],
        [('{ error: reason }', '{ error: String(error) }')]),
}
GUARD = re.compile(r"\} catch \{\n(\s*)(\w+) = 'unreadable thrown value';")

def occurrences(src, needle):
    out, i = [], src.find(needle)
    while i != -1:
        out.append(i); i = src.find(needle, i + 1)
    return out

def mutants(src):
    ms = []
    for k, m in enumerate(GUARD.finditer(src)):
        ms.append((f'G1 inner-catch-rethrows#{k+1}', src[:m.start()] + "} catch (g175m) {\n" + m.group(1) + "throw g175m;" + src[m.end():]))
    for k, i in enumerate(occurrences(src, "'unreadable thrown value'")):
        ms.append((f'G2 constant-changed#{k+1}', src[:i] + "'g175 mutated'" + src[i + len("'unreadable thrown value'"):]))
    return ms

def run(root, tests):
    r = subprocess.run([D + '/node_modules/.bin/vitest', 'run', '--root', root] + tests, env=ENV, capture_output=True, text=True, timeout=300)
    return r.returncode

rows = []
for path, (root, tests, extra) in SITES.items():
    orig = open(path).read()
    rc0 = run(root, tests)
    print('CONTROL unmutated', os.path.relpath(path, D), 'rc', rc0, flush=True)
    assert rc0 == 0, 'unmutated head must pass'
    ms = mutants(orig)
    for a, b in extra:
        for k, i in enumerate(occurrences(orig, a)):
            ms.append((f'G3 use-line {a[:28]!r}#{k+1}', orig[:i] + b + orig[i + len(a):]))
    for name, msrc in ms:
        assert msrc != orig
        open(path, 'w').write(msrc)
        try:
            rc = run(root, tests)
        finally:
            open(path, 'w').write(orig)
        rows.append((os.path.relpath(path, D), name, 'KILLED' if rc != 0 else 'SURVIVED'))
        print(*rows[-1], sep='\t', flush=True)
with open(W + '/results/mutants.tsv', 'w') as f:
    f.write('file\tmutant\tresult\n')
    for r in rows: f.write('\t'.join(r) + '\n')
print('total', len(rows), 'killed', sum(r[2] == 'KILLED' for r in rows), 'survived', sum(r[2] == 'SURVIVED' for r in rows))
