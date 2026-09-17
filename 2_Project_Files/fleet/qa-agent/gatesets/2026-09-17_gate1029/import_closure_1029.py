#!/usr/bin/env python3
"""import_closure_1029.py — READ-ONLY (git show / ls-tree on the Secuura checkout): the relative-import closure of the ks1072 test inside
services/api-gateway at a given commit, plus the @secuura/* specifiers reached. Used to pick the launcher's JUDGED path blobs.
Usage: import_closure_1029.py <commit>"""
import os, re, subprocess, sys
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
C = sys.argv[1]
GW = 'Blockchain/Dev/services/api-gateway/'
T = GW + 'src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts'
ls = subprocess.run(['git', '-C', REPO, 'ls-tree', '-r', '--name-only', C, '--', GW + 'src'], capture_output=True, text=True).stdout.split()
have = set(ls)
IMP = re.compile(r'''(?:import\s[^'"]*?from\s*|import\s*\(\s*|require\(\s*|export\s[^'"]*?from\s*)['"]([^'"]+)['"]''')
def show(p): return subprocess.run(['git', '-C', REPO, 'show', C + ':' + p], capture_output=True, text=True).stdout
def resolve(base, spec):
    d = os.path.normpath(os.path.join(os.path.dirname(base), spec))
    for cand in (d, d + '.ts', d + '.js', d + '/index.ts', d + '/index.js'):
        if cand in have: return cand
    return None
seen, todo, ext = set(), [T], set()
while todo:
    f = todo.pop()
    if f in seen: continue
    seen.add(f)
    for spec in IMP.findall(show(f)):
        if spec.startswith('.'):
            r = resolve(f, spec)
            if r: todo.append(r)
            else: print('UNRESOLVED', f, spec)
        else: ext.add(spec)
print('commit', C, '| closure files', len(seen))
for f in sorted(seen):
    b = subprocess.run(['git', '-C', REPO, 'rev-parse', C + ':' + f], capture_output=True, text=True).stdout.strip()
    print('  ', b, f)
print('external specifiers', sorted(ext))
