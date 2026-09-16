#!/usr/bin/env python3
"""drafter_tsc.py — derived by asserted substitution from the round-1 GATE's including_tsc.py (READ). INCLUDING tsc (program {"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules","dist"]}, from services/api-gateway)
on base / head / merged; --listFilesOnly proof both PR files are in the program; NEW vs base line-number-free; a PLANTED positive control in head's ks1176 test
(+1 TS2322 expected at the plant), restored sha-identical. eslint on both PR files (base: enforcement.ts only; head) with a firing control via --stdin at the
same path. Configs written in MY clone, quarantined by rename. Never rm."""
import os, re, json, subprocess, collections, datetime, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import drafter_run as R
T = R.T; CFG = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}'
PR = ['src/services/enforcement.ts', 'src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts', 'src/routes/verification.ts']
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def including(t, label):
    d = T[t] + '/' + R.GW; cfg = d + '/tsconfig.qa-including.json'; open(cfg, 'w').write(CFG); tsc = T[t] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lfp = subprocess.run([tsc, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=d, capture_output=True, text=True); lf = lfp.stdout.splitlines()
    inc = {p.split('/')[-1]: any(x.endswith('/' + p) for x in lf) for p in PR}
    p = subprocess.run([tsc, '--noEmit', '-p', 'tsconfig.qa-including.json'], cwd=d, capture_output=True, text=True)
    errs = [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]; byf = collections.Counter(l.split('(')[0] for l in errs)
    print(ts(), label, 'listFiles', len(lf), 'listFiles stderr', len(lfp.stderr), '| __tests__ in program', sum(1 for x in lf if '/__tests__/' in x), '| PR files in program', inc, '| rc', p.returncode, 'error lines', len(errs), 'files', len(byf), 'in PR files', sum(v for k, v in byf.items() if k in PR), flush=True)
    q = R.W + '/_quarantine_2026-09-17'; os.makedirs(q, exist_ok=True); os.rename(cfg, q + '/tsconfig.qa-including.%s.%s.json' % (label, datetime.datetime.now().strftime('%H%M%S%f')))
    return errs
norm = lambda ls: collections.Counter(re.sub(r'\(\d+,\d+\)', '', l) for l in ls)
print('including_tsc start', ts(), 'program', CFG)
res = {t: including(t, t) for t in ('base', 'r1', 'head', 'merged')}
for t, ref in (('r1', 'base'), ('head', 'base'), ('merged', 'base'), ('head', 'r1')):
    new = norm(res[t]) - norm(res[ref]); gone = norm(res[ref]) - norm(res[t])
    print('NEW vs', ref, t, sum(new.values()), list(new)[:5], '| GONE', sum(gone.values()), list(gone)[:5])
# planted control in head's ks1176 test
tp = T['head'] + '/' + R.GW + '/' + PR[1]; saved = open(tp, 'rb').read(); before = hashlib.sha256(saved).hexdigest()
s = saved.decode(); anchor = "import { describe"; assert s.count(anchor) == 1, s.count(anchor)
open(tp, 'w').write(s.replace(anchor, "export const qaPlantTS2322: number = 'qa'; // QA-PLANT-INCLUDING\n" + anchor))
assert open(tp).read().count('QA-PLANT-INCLUDING') == 1
planted = including('head', 'head+PLANT')
newp = norm(planted) - norm(res['head']); print('PLANT: NEW vs head', sum(newp.values()), list(newp))
open(tp, 'wb').write(saved); print('plant restored sha256 identical', hashlib.sha256(open(tp, 'rb').read()).hexdigest() == before)
dq = subprocess.run(['git', '-C', T['head'], 'status', '--porcelain'], capture_output=True, text=True); print('head porcelain after', len(dq.stdout.splitlines()), dq.stdout[:200])
# eslint
for t, files in (('base', [PR[0], PR[2]]), ('r1', PR), ('head', PR)):
    dev = T[t] + '/Blockchain/Dev'; es = dev + '/node_modules/.bin/eslint'
    for f in files:
        full = T[t] + '/' + R.GW + '/' + f
        p = subprocess.run([es, '--format', 'json', full], cwd=dev, capture_output=True, text=True)
        try: j = json.loads(p.stdout); n = sum(len(x['messages']) for x in j)
        except Exception: j = None; n = 'NOJSON'
        src = open(full).read() + "\nvar qaEslintControl = 1;\ndebugger;\n"
        c = subprocess.run([es, '--format', 'json', '--stdin', '--stdin-filename', full], input=src, cwd=dev, capture_output=True, text=True)
        try: cj = json.loads(c.stdout); cn = sum(len(x['messages']) for x in cj); rules = sorted({m.get('ruleId') for x in cj for m in x['messages']}, key=str)
        except Exception: cn = 'NOJSON'; rules = c.stderr[:300]
        print(ts(), 'eslint', t, f.split('/')[-1], 'rc', p.returncode, 'messages', n, '| stderr', repr(p.stderr[:200]), '| CONTROL (+var +debugger via stdin, same path) rc', c.returncode, 'messages', cn, 'rules', rules)
print('including_tsc end', ts())
