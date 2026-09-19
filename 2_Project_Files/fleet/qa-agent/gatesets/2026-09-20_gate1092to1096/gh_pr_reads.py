#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1092-#1096: head sha, files (name, status, +/-), zero product bytes per PR from the FILES API,
and body FACTS as booleans / counts. Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout).
Derived from gatesets/2026-09-19_gate1084to1091/gh_pr_reads.py (data changed; + Refs KS-1282 on #1096, + the tier-1 body facts by name)."""
import json, re, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
API = 'https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#?KS-\d+', re.I)
TICKET = {1092: 'KS-1230', 1093: 'KS-1062', 1094: 'KS-739', 1095: 'KS-1238', 1096: 'KS-1238+KS-1282'}
HEAD = {1092: 'd1c35a0c3', 1093: 'b6c29f87b', 1094: '655b83efd', 1095: 'b62df6645', 1096: '789e6b984'}
WANTREFS = {1092: ['KS-1230'], 1093: [], 1094: [], 1095: ['KS-1238'], 1096: ['KS-1238', 'KS-1282']}
allok = True; t1ok = True; refsok = True
for n in range(1092, 1097):
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    refs = sorted(set(re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)))
    own_num = ('KS-%d' % n) in (b + ti)
    k1215 = [x for x in (('branch', br), ('title', ti)) if re.search(r'ks-?1215', x[1], re.I)]
    if refs != WANTREFS[n]: refsok = False
    print('#%d %s head %s (pin %s: %s) state %s mergeable %s mergeable_state %s base %s | title-closing %d body-closing %d | Refs lines %s (want %s) | names KS-%d (its own PR number) %s | keys named in body %s | ks1215/ks-1215 in branch/title %s | KS keys in title %s | KS keys in branch %s'
          % (n, TICKET[n], p['head']['sha'][:9], HEAD[n], p['head']['sha'].startswith(HEAD[n]), p['state'], p.get('mergeable'), p.get('mergeable_state'), p['base']['ref'],
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), refs, WANTREFS[n], n, own_num, sorted(set(re.findall(r'KS-\d+', b))), [x[0] for x in k1215],
             re.findall(r'KS-\d+', ti, re.I), re.findall(r'ks-\d+', br, re.I)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    prod = [f['filename'] for f in files if '/__tests__/' not in f['filename']]
    print('    files outside __tests__/ (files API):', len(prod), prod, '| deletions total', sum(f['deletions'] for f in files))
    if prod: allok = False
    if n in (1095, 1096) and (prod or len(files) != 1): t1ok = False
    if n == 1095:
        print('    #1095 body: "RAW598" %s | "RAW1297" %s | ":1297" %s | "597-598" %s | "N90-1" %s | "N83-2" %s | "PREFLIGHT INCOMPLETE" %s | "ks1215" %s'
              % tuple(w in b for w in ('RAW598', 'RAW1297', ':1297', '597-598', 'N90-1', 'N83-2', 'PREFLIGHT INCOMPLETE', 'ks1215')))
    if n == 1096:
        print('    #1096 body: "REFRESHNOAUTH" %s | "IV_REGLIVEONLY" %s | "TENANTSGETUNGUARDED" %s | ":254" %s | ":222" %s | "13" %s | "PREFLIGHT INCOMPLETE" %s | "KS-1215" %s | "unrevoke" %s'
              % tuple(w in b for w in ('REFRESHNOAUTH', 'IV_REGLIVEONLY', 'TENANTSGETUNGUARDED', ':254', ':222', '13', 'PREFLIGHT INCOMPLETE', 'KS-1215', 'unrevoke')))
print('ZERO PRODUCT BYTES in all five (files API):', allok)
print('TIER 1 #1095 and #1096: one file each, zero product bytes (files API):', t1ok)
print('Refs lines as wanted (#1092 KS-1230; #1093 / #1094 none; #1095 KS-1238; #1096 KS-1238 + KS-1282):', refsok)
