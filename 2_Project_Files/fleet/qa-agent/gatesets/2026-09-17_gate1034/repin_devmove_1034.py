#!/usr/bin/env python3
"""repin_devmove_1034.py NEWDEV — judge a develop move that landed DURING the re-pin, by content, in the re-pinner clone (read verbs on the checkout;
merge-tree --write-tree in the clone only). Never rm, never cd."""
import json, os, subprocess, sys, datetime
GS = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GS + '/repin_paths.json')); C = PA['C']
H = PA['sha']['head']; D = PA['sha']['dev']; N = sys.argv[1]
GW = 'Blockchain/Dev/services/api-gateway'; SH = 'Blockchain/Dev/packages/shared'
def run(*c, inp=None): p = subprocess.run(list(c), capture_output=True, text=True, input=inp); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('repin_devmove_1034', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), 'new develop', N)
print('object in clone:', run('git', '-C', C, 'cat-file', '-t', N)[1:])
print('log:', run('git', '-C', C, 'log', '--format=%H parents %P tree %T | %s', D + '..' + N)[1])
print('3961c2add ancestor of new develop:', run('git', '-C', C, 'merge-base', '--is-ancestor', D, N)[0] == 0)
files = run('git', '-C', C, 'diff', '--name-only', D, N)[1].split('\n'); print('files 3961c2add..new', len(files), files)
PRF = [GW + '/src/middleware/auth.ts', GW + '/src/routes/platform.ts', GW + '/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts']
print('touches a #1034 file:', [f for f in files if f in PRF])
G = [GW + '/src/', GW + '/package.json', GW + '/vitest.config.ts', GW + '/vitest.setup.ts', GW + '/tsconfig.json', SH + '/src/', 'Blockchain/Dev/eslint.config.mjs']
print('GUARDED hits:', [f for f in files if any(f == g or (g.endswith('/') and f.startswith(g)) for g in G)])
for f in files: print('  blob', f.split('/')[-1], run('git', '-C', C, 'rev-parse', '--verify', '-q', D + ':' + f)[1][:9] or 'ABSENT', '->', run('git', '-C', C, 'rev-parse', '--verify', '-q', N + ':' + f)[1][:9] or 'ABSENT')
rc, o, e = run('git', '-C', C, 'merge-tree', '--write-tree', '--name-only', H, N); lines = o.split('\n')
print('merge-tree --write-tree (IN THE CLONE) e4624218b x new develop rc', rc, 'tree', lines[0], 'conflicted-name lines', len(lines) - 1, e[:200])
M = lines[0]; HT = run('git', '-C', C, 'rev-parse', H + '^{tree}')[1]
md = run('git', '-C', C, 'diff', '--name-only', HT, M)[1].split('\n'); print('merged tree vs head tree files', md, '| = new develop own delta:', sorted(md) == sorted(files))
print('merged tree vs head tree, every differing blob = new develop blob:', all(run('git', '-C', C, 'rev-parse', M + ':' + f)[1] == run('git', '-C', C, 'rev-parse', N + ':' + f)[1] for f in md))
for f in PRF: print('  merged', f.split('/')[-1], run('git', '-C', C, 'rev-parse', M + ':' + f)[1][:9], '= head:', run('git', '-C', C, 'rev-parse', M + ':' + f)[1] == run('git', '-C', C, 'rev-parse', H + ':' + f)[1])
for sub in (GW + '/src', SH + '/src'): print('  subtree', sub, 'head', run('git', '-C', C, 'rev-parse', H + ':' + sub)[1][:9], 'merged', run('git', '-C', C, 'rev-parse', M + ':' + sub)[1][:9], 'new develop', run('git', '-C', C, 'rev-parse', N + ':' + sub)[1][:9])
