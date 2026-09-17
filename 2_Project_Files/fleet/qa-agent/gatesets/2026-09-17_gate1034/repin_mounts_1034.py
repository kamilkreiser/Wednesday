#!/usr/bin/env python3
"""drafter_mounts_1034.py TREE — READ census of every api-gateway route where authenticateToken runs (so the connector branch can run), from the tree's
source: `router.<verb|use>('<path>'` or `app.<verb|all|use>('<path>'` followed within 4 lines by `authenticateToken(<arg>)`, plus router-level
`router.use(authenticateToken(...))` files and their app mount prefix. Positive control: /api/credentials (optional) and /api/documents (required)
must be listed. Negative control: /api/batch must NOT be listed (no authenticateToken in batch.ts). Output out/mounts_<tree>.json."""
import json, os, re, sys
GS = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GS + '/repin_paths.json'))
tree = sys.argv[1]; SRC = PA['trees'][tree] + '/Blockchain/Dev/services/api-gateway/src'
rows = []
for f in sorted(os.listdir(SRC + '/routes')) + ['../index.ts']:
    p = SRC + '/routes/' + f
    if not p.endswith('.ts'): continue
    L = open(p).read().split('\n')
    for i, line in enumerate(L):
        m0 = re.search(r"\b(router|app)\.(get|post|put|patch|delete|use|all)\(\s*$", line)
        m = re.search(r"\b(router|app)\.(get|post|put|patch|delete|use|all)\(\s*(\[[^\]]*\]|'[^']*')", line if not m0 else line + ' ' + (L[i + 1].strip() if i + 1 < len(L) else ''))
        if not m: continue
        # v2: the window stops at the next router./app. statement (v1 read 5 lines and credited /api/oauth with /api/webhooks' authenticateToken)
        window = [L[i]]
        for j in range(i + 1, min(i + 7, len(L))):
            if re.search(r"\b(router|app)\.(get|post|put|patch|delete|use|all)\(", L[j]): break
            window.append(L[j])
        window = '\n'.join(window)
        a = re.search(r'authenticateToken\((true|false|)\)', window)
        if not a: continue
        paths = re.findall(r"'([^']*)'", m.group(3))
        for path in paths:
            rows.append(dict(file=f.replace('../', ''), line=i + 1, verb=m.group(2), path=path, required=(a.group(1) != 'false')))
    if re.search(r'router\.use\(authenticateToken\((true|false|)\)\)', '\n'.join(L)):
        rows.append(dict(file=f, line=[i + 1 for i, l in enumerate(L) if re.search(r'router\.use\(authenticateToken', l)][0], verb='use', path='<router-level>', required=True))
idx = open(SRC + '/index.ts').read()
for r in rows:
    if r['path'] == '<router-level>':
        mod = r['file'][:-3]; imp = re.search(r"import (\w+) from './routes/%s'" % re.escape(mod), idx)
        mnt = re.search(r"app\.use\('([^']+)',\s*%s\)" % imp.group(1), idx) if imp else None
        r['path'] = mnt.group(1) if mnt else '<unmounted>'
paths = {(r['path'], r['required']) for r in rows}
print('routes with authenticateToken in window:', len(rows), '| optional', sum(not r['required'] for r in rows), '| required', sum(r['required'] for r in rows))
print('CONTROL /api/credentials optional listed:', ('/api/credentials', False) in paths, '| /api/documents required listed:', ('/api/documents', True) in paths, '| NEGATIVE /api/batch listed:', any(r['path'].startswith('/api/batch') for r in rows))
for r in rows: print('  %-22s:%-5d %-6s %-8s %s' % (r['file'], r['line'], r['verb'], 'required' if r['required'] else 'OPTIONAL', r['path']))
json.dump(rows, open(GS + '/out_repin/mounts_%s.json' % tree, 'w'), indent=1)
