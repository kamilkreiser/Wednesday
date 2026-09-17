#!/usr/bin/env python3
"""drafter_farm_1034.py TREE... — the per-ENTRY node_modules farm (gate1028/drafter_setup_farm.py) + a vitest 4.1.11 overlay: the EIGHT hoisted entries whose
version differs between the checkout install (0a2b1603f lock, 4.1.10) and develop 27e53ec3a's lock (vitest, @vitest/{expect,mocker,pretty-format,runner,snapshot,spy,utils})
are linked to WORKDIR/vitest41111b (exact lock pins) instead of the checkout. `.bin` is linked per entry too, so `.bin/vitest` still points at the CHECKOUT's
4.1.10: every run invokes `node <tree>/Blockchain/Dev/node_modules/vitest/vitest.mjs` (asserted 4.1.11 below). Shared dist built per tree; @secuura/shared
asserted IN TREE from api-gateway/src. Never rm."""
import os, subprocess, datetime, json, sys
GSD = os.path.dirname(os.path.abspath(__file__))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; DEV = 'Blockchain/Dev'; PER_ENTRY = ['packages/shared', 'services/api-gateway']
PA = json.load(open(GSD + '/repin_paths.json')); W = PA['W']; T = PA['trees']; S = W + '/vitest41111/node_modules'
OVER = {'vitest': S + '/vitest'} | {'@vitest/' + x: S + '/@vitest/' + x for x in ('expect', 'mocker', 'pretty-format', 'runner', 'snapshot', 'spy', 'utils')}
def P(*a): print(' '.join(str(x) for x in a), flush=True)
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
for tree in sys.argv[1:]:
    wt = T[tree]
    n, sk, ov = farm_dir(os.path.join(REPO, DEV, 'node_modules'), os.path.join(wt, DEV, 'node_modules'), True); P('farm', tree, 'Dev/node_modules entries', n, 'skipped', sk, '| vitest 4.1.11 overlay entries', ov, '(want 8)')
    assert ov == 8
    for rel in PER_ENTRY:
        n, sk, _ = farm_dir(os.path.join(REPO, DEV, rel, 'node_modules'), os.path.join(wt, DEV, rel, 'node_modules'), False); P('   per-entry farm', rel, 'entries', n, 'skipped', sk)
    wh = [p for p in (os.path.join(wt, DEV, x, 'node_modules') for x in ('', 'packages/shared', 'services/api-gateway')) if os.path.islink(p)]
    P('   wholesale node_modules links (node_modules itself a symlink):', len(wh))
    p = subprocess.run([wt + '/' + DEV + '/node_modules/typescript/bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True); P('  shared dist build rc', p.returncode, (p.stdout + p.stderr).strip()[-300:])
    p = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r, r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + DEV + '/services/api-gateway/src', capture_output=True, text=True)
    P('  resolve @secuura/shared from api-gateway/src:', p.stdout.strip(), p.stderr.strip()[:300])
    p = subprocess.run(['node', wt + '/' + DEV + '/node_modules/vitest/vitest.mjs', '--version'], cwd=wt + '/' + DEV + '/services/api-gateway', capture_output=True, text=True); P('  vitest via node_modules/vitest/vitest.mjs:', p.stdout.strip(), p.stderr.strip()[:200])
    p = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/vitest', '--version'], cwd=wt + '/' + DEV + '/services/api-gateway', capture_output=True, text=True); P('  CONTROL .bin/vitest (checkout link, expected 4.1.10):', p.stdout.strip(), p.stderr.strip()[:200])
    p = subprocess.run(['node', '-e', "for (const m of ['vitest/package.json','@vitest/mocker/package.json','@vitest/runner/package.json','vite/package.json']) { const r=require.resolve(m); console.log(m, require(r).version, require('fs').realpathSync(r)) }"], cwd=wt + '/' + DEV + '/services/api-gateway', capture_output=True, text=True)
    P('  resolved versions from api-gateway:\n   ' + p.stdout.strip().replace('\n', '\n   '), p.stderr.strip()[:300])
