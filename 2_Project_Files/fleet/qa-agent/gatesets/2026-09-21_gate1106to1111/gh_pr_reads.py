#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1106-#1111: head sha vs pin, files (name, status, +/-), product bytes per PR from the FILES API,
Refs lines, closing-phrase / completeness detectors with controls, the compare develop...head (merge_base, ahead, behind, files), ruleset 18499832.
Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout).
Derived from gatesets/2026-09-20_gate1102to1104/gh_pr_reads.py."""
import json, re, urllib.request, sys, subprocess
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
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
PRS = [(1106, 'KS-1232', '2abc82d11014f00567b75a6b8fab5ec5e78f9df2'), (1107, 'KS-753', '7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30'),
       (1108, 'KS-1234', '4904c081c4f9be776acef78349bc10384f10de35'), (1109, 'KS-1279', 'f592268af36b282029e50ff2fa1ebe2614304b81'),
       (1110, 'KS-880', 'a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c'), (1111, 'KS-1223', '3d1ea289a0c367af5cd0d060322e46fc900a1c76')]
DEV = 'cbae988dbe90ebe556459ada2cb437eaf80e2402'; BASE = '778e6cfe2b6061d60ffcf3a57a951c84dc152b67'
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens)[-8:])
for n, tk, h in PRS:
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = sorted(set(re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)))
    print('#%d %s head %s (pin ok %s) state %s mergeable %s mergeable_state %s base %s commits %d created %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | Refs lines %s | KS keys in body %s | KS keys in title %s | branch %s | body chars %d | reviews-requested %d'
          % (n, tk, p['head']['sha'][:12], p['head']['sha'] == h, p['state'], p.get('mergeable'), p.get('mergeable_state'), p['base']['ref'], len(commits), p.get('created_at'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, sorted(set(re.findall(r'KS-\d+', b))), re.findall(r'KS-\d+', ti, re.I), br, len(b), len(p.get('requested_reviewers') or [])))
    print('    title:', ti)
    print('    commit subject:', cm.splitlines()[0] if cm else '')
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    prod = [f['filename'] for f in files if '/src/__tests__/' not in f['filename'] and '/scripts/__tests__/' not in f['filename']]
    print('    files outside __tests__/ (files API):', len(prod), prod, '| additions total', sum(f['additions'] for f in files), '| deletions total', sum(f['deletions'] for f in files))
    for w in ('complete', 'INCOMPLETE', '12/15', 'SKIPPED', '231/231', '907/907', 'no-useless-assignment', 'INT-1', 'a785e7cb93b4', '2e981e7779dc'):
        c = len(re.findall(re.escape(w), b)); 
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832 updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])])
# namespace trap: do PRs #1232/#753/#1234/#1279/#880/#1223 exist (numbers that are these tickets' numbers)? read-only
for q in (1232, 753, 1234, 1279, 880, 1223):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r' % (q, pq['state'], (pq.get('title') or '')[:70]))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
