#!/usr/bin/env python3
"""drafter_tsc.py — #1019 ROUND 2; derived from round 1's GATE tsc_eslint.py. INCLUDING tsc (program {"extends": "./tsconfig.json", "include": ["src/**/*"],
"exclude": ["node_modules","dist"]} — NOT `tsc -p`, whose tsconfig excludes src/__tests__) from services/api-gateway on r1 / r2 / head / dev; --listFilesOnly proof the
touched files are in the program, plus a CONTROL: the same count under the project tsconfig (the ks1187 test must be ABSENT there); error lines in the touched files;
NEW line-number-free (r2 vs r1, head vs dev, head vs r2); a PLANTED TS2322 in head's ks1187 test (+1), restored sha-identical. eslint BY RULE+message on proxy.ts and the
ks1187 test (r1, r2, head) with a --stdin firing control. Configs written in the drafter clone, quarantined by rename. Never rm."""
import os, re, json, subprocess, collections, datetime, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import drafter_run as R
T = R.T; CFG = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}'
PR = ['src/routes/proxy.ts', 'src/__tests__/ks843-erasure-scope-gate.test.ts', 'src/__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts']
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def including(t, label):
    d = T[t] + '/' + R.GW; cfg = d + '/tsconfig.qa-including.json'; open(cfg, 'w').write(CFG); tsc = T[t] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lfp = subprocess.run([tsc, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=d, capture_output=True, text=True); lf = lfp.stdout.splitlines()
    ctl = subprocess.run([tsc, '-p', '.', '--listFilesOnly'], cwd=d, capture_output=True, text=True).stdout.splitlines()
    inc = {p.split('/')[-1][:24]: any(x.endswith('/' + p) for x in lf) for p in PR}
    p = subprocess.run([tsc, '--noEmit', '-p', 'tsconfig.qa-including.json'], cwd=d, capture_output=True, text=True)
    errs = [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]; byf = collections.Counter(l.split('(')[0] for l in errs)
    print(ts(), label, 'listFiles', len(lf), '| __tests__ in program', sum(1 for x in lf if '/__tests__/' in x), '| touched files in program', inc,
          '| CONTROL project tsconfig listFiles', len(ctl), 'ks1187 test in it', any(x.endswith('/' + PR[2]) for x in ctl), '| rc', p.returncode, 'error lines', len(errs), 'files', len(byf), 'in touched files', sum(v for k, v in byf.items() if k in PR), flush=True)
    q = R.W + '/_quarantine_2026-09-17'; os.makedirs(q, exist_ok=True); os.rename(cfg, q + '/tsconfig.qa-including.%s.%s.json' % (label, datetime.datetime.now().strftime('%H%M%S%f')))
    return errs
norm = lambda ls: collections.Counter(re.sub(r'\(\d+,\d+\)', '', l) for l in ls)
print('drafter_tsc start', ts(), 'program', CFG)
res = {t: including(t, t) for t in ('r1', 'r2', 'head', 'dev')}
for t, ref in (('r2', 'r1'), ('head', 'dev'), ('head', 'r2')):
    new = norm(res[t]) - norm(res[ref]); gone = norm(res[ref]) - norm(res[t])
    print('NEW', t, 'vs', ref, sum(new.values()), list(new)[:5], '| GONE', sum(gone.values()), list(gone)[:5])
tp = T['head'] + '/' + R.GW + '/' + PR[2]; saved = open(tp, 'rb').read(); before = hashlib.sha256(saved).hexdigest()
s = saved.decode(); anchor = "import { describe"; assert s.count(anchor) == 1, s.count(anchor)
open(tp, 'w').write(s.replace(anchor, "export const qaPlantTS2322: number = 'qa'; // QA-PLANT-INCLUDING\n" + anchor))
assert open(tp).read().count('QA-PLANT-INCLUDING') == 1
planted = including('head', 'head+PLANT')
newp = norm(planted) - norm(res['head']); print('PLANT: NEW vs head', sum(newp.values()), list(newp))
open(tp, 'wb').write(saved); print('plant restored sha256 identical', hashlib.sha256(open(tp, 'rb').read()).hexdigest() == before)
dq = subprocess.run(['git', '-C', T['head'], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); print('head tracked porcelain after', len(dq.stdout.splitlines()))
def eslint(t, f, stdin_src=None):
    dev = T[t] + '/Blockchain/Dev'; es = dev + '/node_modules/.bin/eslint'; full = T[t] + '/' + R.GW + '/' + f
    args = [es, '--format', 'json'] + (['--stdin', '--stdin-filename', full] if stdin_src is not None else [full])
    p = subprocess.run(args, input=stdin_src, cwd=dev, capture_output=True, text=True)
    try: j = json.loads(p.stdout); msgs = [(m.get('ruleId'), m.get('severity'), m.get('message')) for x in j for m in x['messages']]
    except Exception: msgs = None
    return p.returncode, msgs, p.stderr[:200]
byrule = {}
for t in ('r1', 'r2', 'head'):
    for f in (PR[0], PR[2]):
        rc, msgs, err = eslint(t, f)
        crc, cm, _ = eslint(t, f, open(T[t] + '/' + R.GW + '/' + f).read() + "\nvar qaEslintControl = 1;\ndebugger;\n")
        byrule[(t, f)] = collections.Counter((m[0], m[1], m[2]) for m in (msgs or []))
        print(ts(), 'eslint', t, f.split('/')[-1][:40], 'rc', rc, 'messages', None if msgs is None else len(msgs), 'rules', sorted(collections.Counter(m[0] for m in (msgs or [])).items(), key=str), '| stderr', repr(err[:80]), '| CONTROL rc', crc, 'messages', None if cm is None else len(cm), 'rules', sorted({m[0] for m in (cm or [])}, key=str))
for f in (PR[0], PR[2]):
    for a, b in (('r2', 'r1'), ('head', 'r2')):
        new = byrule[(a, f)] - byrule[(b, f)]; gone = byrule[(b, f)] - byrule[(a, f)]
        print('eslint BY RULE+message NEW', a, 'vs', b, f.split('/')[-1], sum(new.values()), list(new)[:4], '| GONE', sum(gone.values()), list(gone)[:4])
print('drafter_tsc end', ts())
