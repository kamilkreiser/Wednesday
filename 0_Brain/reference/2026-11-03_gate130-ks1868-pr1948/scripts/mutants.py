#!/usr/bin/env python3
# Gate 130 mutants: each mutant applied at ONE site in the product only, tests untouched; sha256-restored after every run.
import hashlib, re, subprocess, sys, json, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948'
S = W + '/repo/Blockchain/Dev/services/security/src'
SITES = [('db.ts', 0, 'hook', 'ks1868-security-db-message'), ('db.ts', 1, 'probe', 'ks1868-security-db-message'),
         ('index.ts', 0, 'audit', 'ks1868-security-audit-event-message'), ('index.ts', 1, 'event', 'ks1868-security-audit-event-message'),
         ('index.ts', 2, 'usage', 'ks1868-security-validate-message'), ('index.ts', 3, 'stored', 'ks1868-security-validate-message'),
         ('index.ts', 4, 'lookup', 'ks1868-security-validate-message')]
PAT = re.compile(r'( *)const m = err\?\.message;\n( *)reason = m === undefined \|\| m === null \? m : String\(m\);\n')
MUT = {
  'M0_revert':        lambda i1, i2: f'{i1}reason = err?.message;\n',
  'M1_no_coerce':     lambda i1, i2: f'{i1}const m = err?.message;\n{i2}reason = m;\n',
  'M2_coerce_all':    lambda i1, i2: f'{i1}const m = err?.message;\n{i2}reason = String(m);\n',
  'M3_constant':      lambda i1, i2: f'{i1}const m = err?.message;\n{i2}reason = \'unreadable thrown value\'; void m;\n',
  'M4_typeof_string': lambda i1, i2: f'{i1}const m = err?.message;\n{i2}reason = m === undefined || m === null ? m : typeof m === \'string\' ? m : \'unreadable thrown value\';\n',
  'M5_null_coerced':  lambda i1, i2: f'{i1}const m = err?.message;\n{i2}reason = m === undefined ? m : String(m);\n',
  'M6_rethrow_unreadable': lambda i1, i2: f'{i1}const m = err?.message;\n{i2}reason = m === undefined || m === null ? m : String(m);\n{i2}if (reason === \'\\u0000never\') throw err;\n',
}
# M6 is a NO-OP control (a branch that never fires): it must SURVIVE, proving the harness can report a survivor.
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
rows = []
for f, idx, name, tests in SITES:
    p = f'{S}/{f}'; orig = open(p).read(); h0 = sha(p)
    ms = list(PAT.finditer(orig)); assert len(ms) == (2 if f == 'db.ts' else 5), (f, len(ms))
    m = ms[idx]
    for mk, fn in MUT.items():
        new = orig[:m.start()] + fn(m.group(1), m.group(2)) + orig[m.end():]
        open(p, 'w').write(new)
        log = f'{W}/logs/mut_{name}__{mk}.log'
        rc = subprocess.call(['bash', W + '/scripts/vt.sh', log, tests])
        open(p, 'w').write(orig); ok = sha(p) == h0
        txt = open(log).read()
        fails = sorted(set(re.findall(r'FAIL .*?> ((?:RED|control) ks1868 [A-Z]\d+)', txt)))
        assertion = txt.count('AssertionError'); other = len(re.findall(r'(TypeError|ReferenceError|SyntaxError|Transform failed)', txt))
        summ = re.findall(r'Tests +(.*)', txt)
        rows.append({'site': name, 'mutant': mk, 'rc': rc, 'verdict': 'KILLED' if rc != 0 else 'SURVIVED', 'failed_cells': fails,
                     'assertionErrors': assertion, 'otherErrors': other, 'tests': summ[-1] if summ else '?', 'restore': ok})
        print(json.dumps(rows[-1]), flush=True)
        if not ok: sys.exit('RESTORE FAILED ' + p)
json.dump(rows, open(W + '/logs/mutants_table.json', 'w'), indent=1)
