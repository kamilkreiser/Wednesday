#!/usr/bin/env python3
"""drafter_tsc.py — #1023; derived from the #1019r2 drafter_tsc.py. INCLUDING tsc program (NOT tsc -p, which excludes src/__tests__) on head / dev with --listFilesOnly
proof the ks1207 test is in it + CONTROL (absent from the project program); error lines in touched files; NEW line-number-free head vs dev; a PLANTED TS2322 in head's
ks1207 test (+1), restored sha-identical. eslint BY RULE+message on auth.ts (head, dev) and the ks1207 test (head) with a --stdin firing control. Configs quarantined."""
import os, re, json, subprocess, collections, datetime, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import drafter_run as R
T = R.T; CFG = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}'
PR = ['src/middleware/auth.ts', 'src/__tests__/ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts']
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def including(t, label):
    d = T[t] + '/' + R.GW; cfg = d + '/tsconfig.qa-including.json'; open(cfg, 'w').write(CFG); tsc = T[t] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lf = subprocess.run([tsc, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=d, capture_output=True, text=True).stdout.splitlines()
    ctl = subprocess.run([tsc, '-p', '.', '--listFilesOnly'], cwd=d, capture_output=True, text=True).stdout.splitlines()
    inc = {p.split('/')[-1][:24]: any(x.endswith('/' + p) for x in lf) for p in PR}
    p = subprocess.run([tsc, '--noEmit', '-p', 'tsconfig.qa-including.json'], cwd=d, capture_output=True, text=True)
    errs = [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]; byf = collections.Counter(l.split('(')[0] for l in errs)
    print(ts(), label, 'listFiles', len(lf), '| touched in program', inc, '| CONTROL project listFiles', len(ctl), 'ks1207 test in it', any(x.endswith('/' + PR[1]) for x in ctl),
          '| rc', p.returncode, 'error lines', len(errs), 'files', len(byf), 'in touched files', sum(v for k, v in byf.items() if k in PR), flush=True)
    q = R.W + '/_quarantine_2026-09-17'; os.makedirs(q, exist_ok=True); os.rename(cfg, q + '/tsconfig.qa-including.%s.%s.json' % (label, datetime.datetime.now().strftime('%H%M%S%f')))
    return errs
norm = lambda ls: collections.Counter(re.sub(r'\(\d+,\d+\)', '', l) for l in ls)
print('drafter_tsc start', ts())
res = {t: including(t, t) for t in ('head', 'dev')}
new = norm(res['head']) - norm(res['dev']); gone = norm(res['dev']) - norm(res['head']); print('NEW head vs dev', sum(new.values()), list(new)[:5], '| GONE', sum(gone.values()), list(gone)[:5])
tp = T['head'] + '/' + R.GW + '/' + PR[1]; saved = open(tp, 'rb').read(); before = hashlib.sha256(saved).hexdigest()
s = saved.decode(); anchor = "import { describe"; assert s.count(anchor) == 1
open(tp, 'w').write(s.replace(anchor, "export const qaPlantTS2322: number = 'qa'; // QA-PLANT-INCLUDING\n" + anchor)); assert open(tp).read().count('QA-PLANT-INCLUDING') == 1
try:
    planted = including('head', 'head+PLANT'); newp = norm(planted) - norm(res['head']); print('PLANT: NEW vs head', sum(newp.values()), list(newp))
finally:
    open(tp, 'wb').write(saved); print('plant restored sha256 identical', hashlib.sha256(open(tp, 'rb').read()).hexdigest() == before)
def eslint(t, f, stdin_src=None):
    dev = T[t] + '/Blockchain/Dev'; es = dev + '/node_modules/.bin/eslint'; full = T[t] + '/' + R.GW + '/' + f
    p = subprocess.run([es, '--format', 'json'] + (['--stdin', '--stdin-filename', full] if stdin_src is not None else [full]), input=stdin_src, cwd=dev, capture_output=True, text=True)
    try: j = json.loads(p.stdout); msgs = [(m.get('ruleId'), m.get('severity'), m.get('message')) for x in j for m in x['messages']]
    except Exception: msgs = None
    return p.returncode, msgs, p.stderr[:200]
byrule = {}
for t, f in (('head', PR[0]), ('dev', PR[0]), ('head', PR[1])):
    rc, msgs, err = eslint(t, f); crc, cm, _ = eslint(t, f, open(T[t] + '/' + R.GW + '/' + f).read() + "\nvar qaEslintControl = 1;\ndebugger;\n")
    byrule[(t, f)] = collections.Counter(msgs or [])
    print(ts(), 'eslint', t, f.split('/')[-1][:40], 'rc', rc, 'messages', None if msgs is None else msgs, '| stderr', repr(err[:80]), '| CONTROL rc', crc, 'messages', None if cm is None else len(cm), 'rules', sorted({m[0] for m in (cm or [])}, key=str))
n = byrule[('head', PR[0])] - byrule[('dev', PR[0])]; g = byrule[('dev', PR[0])] - byrule[('head', PR[0])]; print('eslint auth.ts BY RULE+message NEW head vs dev', sum(n.values()), list(n), '| GONE', sum(g.values()), list(g))
print('head tracked porcelain after', len(subprocess.run(['git', '-C', T['head'], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.splitlines()))
print('drafter_tsc end', ts())
