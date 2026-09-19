#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1077-#1083: head sha, files (name, status, +/-), zero product bytes per PR from the FILES API,
and body FACTS as booleans / counts. Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout).
Derived from gatesets/2026-09-19_gate1070to1076/gh_pr_reads.py."""
import json, re, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
API = 'https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#?KS-\d+', re.I)
TICKET = {1077: 'KS-1258', 1078: 'KS-1260', 1079: 'KS-1062', 1080: 'KS-1230', 1081: 'KS-1206', 1082: 'KS-739', 1083: 'KS-1238'}
allok = True
for n in range(1077, 1084):
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100')
    b = p.get('body') or ''
    refs = sorted(set(re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)))
    own_num = ('KS-%d' % n) in (b + (p.get('title') or ''))
    print('#%d %s head %s state %s mergeable %s mergeable_state %s base %s | title-closing %d body-closing %d | Refs lines %s | names KS-%d (its own PR number) %s | keys named in body %s'
          % (n, TICKET[n], p['head']['sha'][:9], p['state'], p.get('mergeable'), p.get('mergeable_state'), p['base']['ref'],
             len(CLOSING.findall(p.get('title') or '')), len(CLOSING.findall(b)), refs, n, own_num, sorted(set(re.findall(r'KS-\d+', b)))))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    prod = [f['filename'] for f in files if '/__tests__/' not in f['filename']]
    print('    files outside __tests__/ (files API):', len(prod), prod)
    if prod: allok = False
    if n == 1083:
        low = b.lower()
        print('    #1083 body: "verification.ts:516" %s | "RAW516" %s | "75b0024e" %s | "(iii)" %s | "(v)" %s' % ('verification.ts:516' in b, 'RAW516' in b, '75b0024e' in b, '(iii)' in b, '(v)' in b))
    if n == 1077:
        print('    #1077 body: "CHECKER_NO_RESULT" %s | "re-run" %s' % ('CHECKER_NO_RESULT' in b, 're-run' in b.lower()))
print('ZERO PRODUCT BYTES in all seven (files API):', allok)
