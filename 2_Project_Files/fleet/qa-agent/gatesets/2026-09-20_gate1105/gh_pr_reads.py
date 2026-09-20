#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for PR #1105 (KS-1175 real fix + KS-1284 codec, Seat A 15th): head sha vs the pin, base, state,
mergeable_state, commits, the FILES API (12 files: name, status, +/-), the set of files OUTSIDE services/anchoring/** + the regenerated yaml +
VOCABULARY.md (want 0), body FACTS as booleans / counts (closing-word detector with controls; Refs lines want exactly KS-1175 / KS-1284 / KS-721;
names KS-1105 = its own PR number, the namespace trap), the compare API develop...head (want merge_base dc061f2bb, ahead 1, files 12), the PR
comment count, ruleset 18499832. Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env, read transiently).
Writes nothing (stdout). Derived from gatesets/2026-09-20_gate1100to1101/gh_pr_reads.py (data changed; the product-file predicate inverted:
this PR IS a product change, the assertion is that the product bytes stay inside services/anchoring/**)."""
import json, re, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
API = REPO + 'pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+#?KS-\d+', re.I)
assert CLOSING.search('Completes KS-1175') and CLOSING.search('Fixes KS-1284') and not CLOSING.search('Refs KS-1175') and not CLOSING.search('the real fix for KS-1175 is'), 'closing detector controls'
N = 1105; TICKET = 'KS-1175'
HEAD = 'e02d3ecb51a457b0eb490db1854f28c6b1af69ad'; DEV = 'dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa'
WANTREFS = ['KS-1175', 'KS-1284', 'KS-721']
ALLOWED_PREFIX = 'Blockchain/Dev/services/anchoring/'
ALLOWED_EXACT = {'Blockchain/Dev/docs/openapi/secuura-api.yaml', 'Blockchain/Dev/docs/VOCABULARY.md'}
p = get(API + str(N)); files = get(API + str(N) + '/files?per_page=100'); commits = get(API + str(N) + '/commits?per_page=100')
b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
cm = '\n'.join(c['commit']['message'] for c in commits)
refs_body = re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)
refs_commit = re.findall(r'^\s*Refs?:?\s+(KS-\d+)', cm, re.M | re.I)
print('#%d %s head %s (pin: %s) base %s (base sha %s = pinned develop: %s) state %s mergeable %s mergeable_state %s commits %d | closing(title/body/commit) %d/%d/%d | Refs body %s commit %s (want %s) | names KS-%d (its own PR number) in title/body/commit %s | KS keys in body %s | KS keys in title %s | branch %s | body chars %d | PR comments %d review_comments %d'
      % (N, TICKET, p['head']['sha'][:12], p['head']['sha'] == HEAD, p['base']['ref'], p['base']['sha'][:12], p['base']['sha'] == DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), len(commits),
         len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), refs_body, refs_commit, WANTREFS, N, ('KS-%d' % N) in (b + ti + cm),
         sorted(set(re.findall(r'KS-\d+', b))), re.findall(r'KS-\d+', ti, re.I), br, len(b), p.get('comments'), p.get('review_comments')))
tot_add = tot_del = 0
outside = []
for f in sorted(files, key=lambda x: x['filename']):
    print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    tot_add += f['additions']; tot_del += f['deletions']
    if not (f['filename'].startswith(ALLOWED_PREFIX) or f['filename'] in ALLOWED_EXACT): outside.append(f['filename'])
print('    files %d | +%d -%d | outside services/anchoring/** + yaml + VOCABULARY.md: %d %s (want 0)' % (len(files), tot_add, tot_del, len(outside), outside))
print('    added files: %s' % [f['filename'].split('/')[-1] for f in files if f['status'] == 'added'])
print('    migration/config/dependency paths in the files API (prisma/, migrations, package.json, package-lock.json, .env, docker, compose): %s (want [])'
      % [f['filename'] for f in files if re.search(r'prisma/|migration|package(-lock)?\.json|\.env|[Dd]ocker|compose', f['filename'])])
print('    body: "NOT DONE" present %s | "seven" present %s | "six originate-fronted" present %s | "sha256" present %s | "BACKLOG.md:155" present %s | "true"/"false" present %s'
      % ('NOT DONE' in b, 'seven' in b.lower(), 'six originate-fronted' in b.lower(), 'sha256' in b, 'BACKLOG.md:155' in b, ('"true"' in b and '"false"' in b)))
print('    commit message: "BACKLOG.md:155" present %s | "Refs KS-1175" %s | "Refs KS-1284" %s | "Refs KS-721" %s | closing words %d'
      % ('BACKLOG.md:155' in cm, 'Refs KS-1175' in cm, 'Refs KS-1284' in cm, 'Refs KS-721' in cm, len(CLOSING.findall(cm))))
c = get(REPO + 'compare/develop...' + HEAD)
print('compare develop...%s: merge_base %s (= pinned develop: %s) status %s ahead %d behind %d files %d' % (HEAD[:9], c['merge_base_commit']['sha'][:12], c['merge_base_commit']['sha'] == DEV, c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('head at pin (pulls API):', p['head']['sha'] == HEAD, '| Refs body as wanted:', sorted(set(refs_body)) == sorted(WANTREFS), '| Refs commit as wanted:', sorted(set(refs_commit)) == sorted(WANTREFS), '| closing words 0:', not (CLOSING.findall(ti) or CLOSING.findall(b) or CLOSING.findall(cm)), '| outside allowed 0:', not outside)
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832 updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])],
      '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'])
