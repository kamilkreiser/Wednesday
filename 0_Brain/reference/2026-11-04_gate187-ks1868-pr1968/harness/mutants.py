#!/usr/bin/env python3
"""Gate 187 mutant driver. Applies one line-level mutant at a time to the head copy in mut/m, runs
(a) the PR's two new test files and (b) the gate187 harness cells, records killed-by for each, restores.
Every mutation asserts the line it replaces matches the expected head text (so a mutant cannot silently miss)."""
import json, os, re, shutil, subprocess, sys

W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate187-ks1868-pr1968'
M = f'{W}/mut/m/Blockchain/Dev/services/vc-issuer'
HEADSRC = f'{W}/scratch/head/Blockchain/Dev/services/vc-issuer/src'
PR_TESTS = ['src/__tests__/ks1868-credentialrepo-read-catches-unreadable-throw.test.ts',
            'src/__tests__/ks1868-vc-issuer-db-pool-error-and-ready-hook-unreadable-throw.test.ts']
SITES = {  # site: (file, coercion line, constant line, logger line)
    'poolListener': ('db.ts', 35, 37, 39),
    'readyHook': ('db.ts', 87, 89, 91),
    'getById': ('repositories/credentialRepo.ts', 122, 124, 126),
    'getRecordById': ('repositories/credentialRepo.ts', 170, 172, 174),
    'getByHash': ('repositories/credentialRepo.ts', 205, 207, 209),
}
COERCE = 'reason = m === undefined || m === null ? m : String(m);'
CONST = "reason = 'unreadable thrown value';"
MUTS = {
    'A_const_text': ('const', CONST, "reason = 'unreadable';"),
    'B_drop_String': ('coerce', COERCE, 'reason = m;'),
    'C_drop_nullpass': ('coerce', COERCE, 'reason = String(m);'),
    'D_catch_rethrows': ('const', CONST, "throw new Error('g187 mutant rethrow');"),
    'E_log_detail(Q3 control)': ('log', '{ error: reason }', '{ error: reason, detail: (err as any)?.detail }'),
}

def run(outfile, args):
    subprocess.run(['bash', f'{W}/harness/run_suite.sh', M, outfile] + args, check=False)
    txt = re.sub(r'\x1b\[[0-9;]*m', '', open(outfile).read())
    tests = re.search(r'^\s+Tests\s+(.*)$', txt, re.M)
    rc = re.search(r'^rc=(\d+)', txt, re.M)
    return (tests.group(1).strip() if tests else 'NO SUMMARY'), int(rc.group(1)) if rc else -1

def cells(kind):
    p = f'{W}/runs/cells_{kind}_m.json'
    return {(r['site'], r['value']): r for r in json.load(open(p))}

H = {}
for kind in ('repo', 'db'):
    H.update({(r['site'], r['value']): r for r in json.load(open(f'{W}/runs/cells_{kind}_head.json'))})

rows = []
os.makedirs(f'{W}/runs/mut', exist_ok=True)
for site, (f, lc, lk, ll) in SITES.items():
    for mname, (which, old, new) in MUTS.items():
        line = {'coerce': lc, 'const': lk, 'log': ll}[which]
        path = f'{M}/src/{f}'
        shutil.copyfile(f'{HEADSRC}/{f}', path)
        L = open(path).read().split('\n')
        assert old in L[line - 1], (site, mname, L[line - 1])
        L[line - 1] = L[line - 1].replace(old, new)
        open(path, 'w').write('\n'.join(L))
        tag = f'{site}__{mname.split("(")[0]}'
        pr_sum, pr_rc = run(f'{W}/runs/mut/{tag}__prtests.txt', PR_TESTS)
        h_sum, h_rc = run(f'{W}/runs/mut/{tag}__harness.txt', ['src/__tests__/gate187-'])
        C = {}
        C.update(cells('repo')); C.update(cells('db'))
        keys = ('threw', 'value_out', 'initDb', 'lines', 'reasonType', 'reason', 'tokenInLogs')
        diffs = sorted(f'{k[0]}x{k[1]}' for k in C if k[0] == site and any(C[k].get(x) != H[k].get(x) for x in keys))
        tok = sorted(k[1] for k in C if k[0] == site and C[k].get('tokenInLogs'))
        rows.append(dict(site=site, mutant=mname, pr_tests=pr_sum, pr_rc=pr_rc, pr_killed=pr_rc != 0,
                         harness_rc=h_rc, harness_cells_differing=len(diffs), harness_killed=len(diffs) > 0,
                         differing=diffs, token_cells=tok))
        shutil.copyfile(f'{HEADSRC}/{f}', path)
        print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open(f'{W}/runs/mutants.json', 'w'), indent=1)
