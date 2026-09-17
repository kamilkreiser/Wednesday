#!/usr/bin/env python3
"""redraft_farm_1035.py — (1) side install of develop's vitest 4.1.11 closure (drafter_vitest41111_1035.py, re-pointed at the CURRENT develop 3961c2add's lock,
asserting its vitest closure = 732c13459's); (2) the per-ENTRY node_modules farm with the 8-entry vitest overlay (drafter_farm_1035.py) for head / dev / merged;
shared dist built per tree; @secuura/shared asserted IN TREE; vitest version via node_modules/vitest/vitest.mjs (4.1.11) with the .bin/vitest control (4.1.10).
Never rm; stderr kept."""
import json, os, subprocess, datetime
GS = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GS + '/out/r2/paths.json')); W = PA['W']; C = PA['C']; T = PA['trees']
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; DEV = 'Blockchain/Dev'; PER_ENTRY = ['packages/shared', 'services/api-gateway']
def now(): return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def closure(sha):
    lock = json.loads(subprocess.run(['git', '-C', C, 'show', sha + ':Blockchain/Dev/package-lock.json'], capture_output=True, text=True).stdout)['packages']
    def resolve(name, frm):
        base = frm
        while True:
            k = (base + '/' if base else '') + 'node_modules/' + name
            if k in lock: return k
            if not base: return None
            i = base.rfind('/node_modules/'); base = base[:i] if i >= 0 else ''
    seen = {}; stack = ['node_modules/vitest']
    while stack:
        k = stack.pop()
        if k in seen: continue
        seen[k] = lock[k]['version']
        for dep in list((lock[k].get('dependencies') or {}).keys()):
            r = resolve(dep, k)
            if r: stack.append(r)
    return seen
P('redraft_farm_1035', now())
cd, cb = closure(PA['sha']['dev']), closure(PA['sha']['base'])
P('vitest closure at develop', PA['sha']['dev'][:9], len(cd), 'entries | == 732c13459 closure:', cd == cb, '| vitest', cd['node_modules/vitest'])
top = {k[len('node_modules/'):]: v for k, v in cd.items() if k.count('node_modules/') == 1}
S = W + '/vitest41111'; os.makedirs(S)
json.dump({'name': 'qa1035-vitest-41111-side', 'private': True, 'dependencies': dict(sorted(top.items()))}, open(S + '/package.json', 'w'), indent=1)
t0 = now(); p = subprocess.run(['npm', 'install', '--ignore-scripts', '--no-audit', '--no-fund', '--no-package-lock'], cwd=S, capture_output=True, text=True)
open(S + '/npm_install.log', 'w').write(p.stdout + '\n--stderr--\n' + p.stderr); P('npm install rc', p.returncode, t0, '->', now(), '| stderr tail', p.stderr[-400:])
bad = [(n, v, (json.load(open(S + '/node_modules/' + n + '/package.json'))['version'] if os.path.exists(S + '/node_modules/' + n + '/package.json') else 'ABSENT')) for n, v in top.items()]
bad = [b for b in bad if b[1] != b[2]]; P('closure hoisted packages at lock version:', len(top) - len(bad), '/', len(top), '| mismatches', bad[:10])
SN = S + '/node_modules'
OVER = {'vitest': SN + '/vitest'} | {'@vitest/' + x: SN + '/@vitest/' + x for x in ('expect', 'mocker', 'pretty-format', 'runner', 'snapshot', 'spy', 'utils')}
def farm_dir(src, dst, dev_root):
    os.mkdir(dst); n = 0; skipped = []; over = 0
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): skipped.append(ent); continue
        s = os.path.join(src, ent)
        if dev_root and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)):
                t = os.readlink(os.path.join(s, sub)); os.symlink(os.path.normpath(os.path.join(dst, ent, t)), os.path.join(dst, ent, sub))
        elif dev_root and ent == '@vitest':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)):
                k = ent + '/' + sub; tgt = OVER.get(k, os.path.join(s, sub)); over += k in OVER; os.symlink(tgt, os.path.join(dst, ent, sub))
        elif dev_root and ent in OVER:
            os.symlink(OVER[ent], os.path.join(dst, ent)); over += 1
        else:
            os.symlink(s, os.path.join(dst, ent))
        n += 1
    return n, skipped, over
for tree, wt in T.items():
    n, sk, ov = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', tree, 'Dev/node_modules entries', n, 'skipped', sk, '| vitest overlay entries', ov, '(want 8)'); assert ov == 8
    for rel in PER_ENTRY:
        n, sk, _ = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    P('   wholesale node_modules links:', sum(os.path.islink(os.path.join(wt, DEV, x, 'node_modules')) for x in ('', 'packages/shared', 'services/api-gateway')))
    p = subprocess.run([wt + '/' + DEV + '/node_modules/typescript/bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('  shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r.slice(-60), r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE', '| ts', require('typescript/package.json').version, '| eslint', require('eslint/package.json').version, '| tsx', require('tsx/package.json').version, process.version)", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src', capture_output=True, text=True)
    P('  resolve from api-gateway/src:', p.stdout.strip(), p.stderr.strip()[:300])
    p = subprocess.run(['node', wt + '/' + DEV + '/node_modules/vitest/vitest.mjs', '--version'], cwd=wt + '/' + DEV + '/services/api-gateway', capture_output=True, text=True); P('  vitest.mjs:', p.stdout.strip(), p.stderr.strip()[:200])
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/vitest', '--version'], cwd=wt + '/' + DEV + '/services/api-gateway', capture_output=True, text=True); P('  CONTROL .bin/vitest (checkout link):', p.stdout.strip(), p.stderr.strip()[:200])
    P('  tracked porcelain', len(subprocess.run(['git', '-C', wt, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.splitlines()))
P('redraft_farm_1035 end', now())
