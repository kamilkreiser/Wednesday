#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1070-#1076: head sha, files (name, status, +/-), and body FACTS as booleans / counts.
Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout only)."""
import json, re, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
API = 'https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#?KS-\d+', re.I)
for n in range(1070, 1077):
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100')
    b = p.get('body') or ''
    refs = sorted(set(re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)))
    print('#%d head %s state %s mergeable %s mergeable_state %s base %s | title-closing %d body-closing %d | Refs lines %s | keys named in body %s'
          % (n, p['head']['sha'][:9], p['state'], p.get('mergeable'), p.get('mergeable_state'), p['base']['ref'],
             len(CLOSING.findall(p.get('title') or '')), len(CLOSING.findall(b)), refs, sorted(set(re.findall(r'KS-\d+', b)))))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    if n == 1071:
        low = b.lower()
        print('    #1071 body: "non-ruled" %s | "/unrevoke" %s | "index:-1" or "index: -1" %s | "15:22:07" %s | "400 before 404" or "before its 404" %s | "404 before 400" %s'
              % ('non-ruled' in low, '/unrevoke' in low, ('index:-1' in low or 'index: -1' in low), '15:22:07' in b, ('400 before 404' in low or 'before its 404' in low), '404 before 400' in low))
        for l in b.splitlines():
            if 'non-ruled' in l.lower(): print('    #1071 NON-RULED line length', len(l), 'sha1', __import__('hashlib').sha1(l.encode()).hexdigest()[:12])
    if n == 1076:
        prod = [f['filename'] for f in files if '/__tests__/' not in f['filename']]
        print('    #1076 files outside __tests__/:', len(prod), prod)
