#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1084-#1091: head sha, files (name, status, +/-), zero product bytes per PR from the FILES API,
and body FACTS as booleans / counts. Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout).
Derived from gatesets/2026-09-19_gate1077to1083/gh_pr_reads.py (+ the #1090/#1091 zero-product assertion by name, + the ks1215 / KS-1215 lint read)."""
import json, re, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
API = 'https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#?KS-\d+', re.I)
TICKET = {1084: 'KS-1269', 1085: 'KS-1258', 1086: 'KS-1230', 1087: 'KS-1206', 1088: 'KS-1062', 1089: 'KS-739', 1090: 'KS-1238', 1091: 'KS-1238'}
HEAD = {1084: '946cdfd78', 1085: 'c3d9ca2e2', 1086: 'b0bcf733f', 1087: 'd4658c021', 1088: '734a8f0bd', 1089: 'a64390edf', 1090: 'bd45f3b4f', 1091: 'dad4786c8'}
allok = True; t1ok = True
for n in range(1084, 1092):
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    refs = sorted(set(re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)))
    own_num = ('KS-%d' % n) in (b + ti)
    k1215 = [x for x in (('branch', br), ('title', ti)) if re.search(r'ks-?1215', x[1], re.I)]
    print('#%d %s head %s (pin %s: %s) state %s mergeable %s mergeable_state %s base %s | title-closing %d body-closing %d | Refs lines %s | names KS-%d (its own PR number) %s | keys named in body %s | ks1215/ks-1215 in branch/title %s'
          % (n, TICKET[n], p['head']['sha'][:9], HEAD[n], p['head']['sha'].startswith(HEAD[n]), p['state'], p.get('mergeable'), p.get('mergeable_state'), p['base']['ref'],
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), refs, n, own_num, sorted(set(re.findall(r'KS-\d+', b))), [x[0] for x in k1215]))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    prod = [f['filename'] for f in files if '/__tests__/' not in f['filename']]
    print('    files outside __tests__/ (files API):', len(prod), prod)
    if prod: allok = False
    if n in (1090, 1091) and (prod or len(files) != 1): t1ok = False
    if n in (1090, 1091):
        print('    #%d body: "verification.ts:521" %s | "platform.ts:239" %s | "RAW521" %s | "TENANTSORGPROV" %s | "TENANTSUNGUARDED" %s | "(iii)" %s | "(iv)" %s | ":598" %s | ":1297" %s'
              % (n, 'verification.ts:521' in b, 'platform.ts:239' in b, 'RAW521' in b, 'TENANTSORGPROV' in b, 'TENANTSUNGUARDED' in b, '(iii)' in b, '(iv)' in b, ':598' in b, ':1297' in b))
    if n == 1084:
        print('    #1084 body: "KS-1155" %s | "db.retry" %s | "-1" %s | "NON-RULED" %s | "e9fc521" %s' % ('KS-1155' in b, 'db.retry' in b, '-1' in b, 'NON-RULED' in b, 'e9fc521' in b))
print('ZERO PRODUCT BYTES in all eight (files API):', allok)
print('TIER 1 #1090 and #1091: one file each, zero product bytes (files API):', t1ok)
