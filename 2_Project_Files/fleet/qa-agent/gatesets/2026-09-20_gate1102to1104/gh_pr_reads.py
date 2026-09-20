#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1102, #1103 and the ks-1272 PR (found by head sha among open PRs): head sha, files (name, status,
+/-), product bytes per PR from the FILES API, Refs lines, closing-phrase / completeness detectors with controls, ruleset 18499832.
Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout).
Derived from gatesets/2026-09-20_gate1100to1101/gh_pr_reads.py."""
import json, re, urllib.request, sys
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
API = REPO + 'pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+#?KS-\d+', re.I)
COMPLETE = re.compile(r'\b(complete[sd]?|completeness|fully pins|now complete|closes the ticket|entire scope|all of KS-\d+)\b', re.I)
assert COMPLETE.search('Completes KS-1282') and not COMPLETE.search('pins todays 403 and claims nothing further'), 'completeness detector controls'
assert CLOSING.search('Completes KS-1282') and not CLOSING.search('Whether KS-1282 is now complete'), 'closing detector controls'
HEAD = {'KS-1275': 'f5a599b077667a1fdda602744092d866df03c3fa', 'KS-1203': '47593b77b80a295b4113da8acf850b5c8b03fd7e', 'KS-1272': '9b668edba63e1328ab113058b47953a11d2a3ed6'}
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
found = {}
for p in opens:
    for tk, h in HEAD.items():
        if p['head']['sha'] == h: found[tk] = p['number']
print('open PRs listed', len(opens), '| by head sha:', found)
for tk in ('KS-1275', 'KS-1203', 'KS-1272'):
    if tk not in found: print('%s: NO OPEN PR at head %s yet' % (tk, HEAD[tk])); continue
    n = found[tk]
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = sorted(set(re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)))
    print('#%d %s head %s (pin ok %s) state %s mergeable %s mergeable_state %s base %s commits %d created %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | Refs lines %s | KS keys in body %s | KS keys in title %s | branch %s | body chars %d'
          % (n, tk, p['head']['sha'][:12], p['head']['sha'] == HEAD[tk], p['state'], p.get('mergeable'), p.get('mergeable_state'), p['base']['ref'], len(commits), p.get('created_at'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, sorted(set(re.findall(r'KS-\d+', b))), re.findall(r'KS-\d+', ti, re.I), br, len(b)))
    print('    title:', ti)
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    prod = [f['filename'] for f in files if '/src/__tests__/' not in f['filename']]
    print('    files outside src/__tests__/ (files API):', len(prod), prod, '| deletions total', sum(f['deletions'] for f in files))
    print('    ks501/KS-501 in branch/title/commit-subject:', [x for x in ('branch', 'title', 'subject') if re.search(r'ks-?501\b', {'branch': br, 'title': ti, 'subject': cm.splitlines()[0] if cm else ''}[x], re.I)], '| "86-line" / "85-line" / "recount" in body+commit:', [w for w in ('86-line', '85-line', 'recount', ':473', '22P02', 'IS NOT DISTINCT FROM') if w in b + cm])
    c = get(REPO + 'compare/develop...' + HEAD[tk])
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832 updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])])
