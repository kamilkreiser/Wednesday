#!/usr/bin/env python3
"""G156 mutants on head db.ts. Each mutant: exact single-occurrence replace, run the PR's new test file AND the
full governance suite (jest), record killed/survived, restore by `git checkout --` and verify the blob sha."""
import json, subprocess, sys, pathlib
W = pathlib.Path('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate156-ks1868-pr1973')
R = W / 'repo'
G = R / 'Blockchain/Dev/services/governance'
DB = G / 'src/db.ts'
J = R / 'Blockchain/Dev/node_modules/.bin/jest'
T = G / 'src/__tests__/ks1868-governance-db-pool-error-and-ready-hook-unreadable-throw.test.ts'
HEAD_BLOB = 'fb610b5708c57c63790f9fd7425ac7110f71f0a0'

def block(ind, msg):
    s = ' ' * ind
    return (f"{s}let reason: string | null | undefined;\n{s}try {{\n{s}  const m = err?.message;\n"
            f"{s}  reason = m === undefined || m === null ? m : String(m);\n{s}}} catch {{\n"
            f"{s}  reason = 'unreadable thrown value';\n{s}}}\n{s}dbLog('error', '{msg}', {{ error: reason }});\n")

def muts(site, ind, msg):
    b = block(ind, msg); s = ' ' * ind
    return [
        (f'{site}1 try/catch removed', b, f"{s}const m = err?.message;\n{s}const reason = m === undefined || m === null ? m : String(m);\n{s}dbLog('error', '{msg}', {{ error: reason }});\n"),
        (f'{site}2 err?.message -> err.message', b, b.replace('err?.message', 'err.message')),
        (f'{site}3 String(m) -> m (no coercion)', b, b.replace('String(m)', '(m as any)')),
        (f'{site}4 null/undefined passthrough removed', b, b.replace('m === undefined || m === null ? m : String(m)', 'String(m)')),
        (f'{site}5 catch constant changed', b, b.replace("'unreadable thrown value'", "'unknown'")),
        (f'{site}6 catch returns without logging', b, b.replace(f"{s}  reason = 'unreadable thrown value';\n", f"{s}  return;\n")),
    ]

MUTS = muts('P', 6, 'DB pool unexpected error') + muts('H', 4, 'DB ready boot work failed')

def jest(name, *args):
    out = W / f'logs/mut_{name}.json'
    rc = subprocess.run([str(J), '--config', str(G / 'jest.config.js'), '--rootDir', str(G), '--ci', '--json', '--outputFile', str(out), *args],
                        cwd=str(W / 'logs/cwd'), capture_output=True, text=True).returncode
    try:
        j = json.loads(out.read_text())
        fails = [a['title'][:40] for s in j['testResults'] for a in s['assertionResults'] if a['status'] != 'passed']
        return rc, j['numFailedTests'], j['numTotalTests'], fails, j['numRuntimeErrorTestSuites']
    except Exception as e:
        return rc, None, None, [str(e)], None

def blob():
    return subprocess.run(['git', '-C', str(R), 'hash-object', str(DB)], capture_output=True, text=True).stdout.strip()

results = []
orig = DB.read_text()
assert blob() == HEAD_BLOB
for i, (name, old, new) in enumerate(MUTS):
    n = orig.count(old)
    if n != 1 or old == new:
        results.append({'mutant': name, 'error': f'occurrences={n} identical={old == new}'}); continue
    DB.write_text(orig.replace(old, new))
    tag = f'm{i}'
    new_rc, new_f, new_t, new_fails, _ = jest(tag + '_new', str(T))
    full_rc, full_f, full_t, full_fails, rte = jest(tag + '_full')
    subprocess.run(['git', '-C', str(R), 'checkout', '-q', '--', 'Blockchain/Dev/services/governance/src/db.ts'], check=True)
    assert blob() == HEAD_BLOB, 'restore failed'
    results.append({'mutant': name, 'newTest': f'rc={new_rc} failed {new_f}/{new_t}', 'newFails': new_fails,
                    'fullSuite': f'rc={full_rc} failed {full_f}/{full_t} runtimeErrSuites={rte}',
                    'verdict': 'KILLED' if (new_f or full_f or new_rc or full_rc) else 'SURVIVED'})
    print(json.dumps(results[-1]), flush=True)
(W / 'logs/mutants.json').write_text(json.dumps(results, indent=1))
print('restored blob', blob())
