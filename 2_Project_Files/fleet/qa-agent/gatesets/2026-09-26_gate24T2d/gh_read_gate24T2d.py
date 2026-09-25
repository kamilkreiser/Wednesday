#!/usr/bin/env python3
"""gh_read_gate24T2d.py — READ-ONLY GitHub reads (REST GET only) for gate24T2d over #1250 (round 2), #1253 (round 2), #1262, #1263, #1264 #1265 and #1266 (the round-25 widens, #1266 = Seat L8 KS-1120 tier 2 test-only; Seat L7 KS-1140 and Seat L8 KS-1281, tier 3 comment-only; Seat L7 KS-1315, tier 2 test-only). GH_TOKEN by NAME
from the Secuura .env, never printed. Per PR: head / state / mergeable / base / draft / title (length, ASCII) / body (KS keys, Refs lines, closing-
word+key count, the round-2 markers; saved as gh_body_<n>.md) / files / commits (each with its parents) / compare against the CURRENT develop /
issue comments (gh_comments_<n>.md). Then the WIDEN census: every OPEN PR (newest first), those on ROUND-25 branches (`-b29-`, `-l7r25-`,
`-l8r25-`: Seats B 29th / L7 / L8 per their launch briefs), and those in the sibling kit gate24T2c (#1245 #1256 #1257-#1261) for the record.
Writes only beside this script. Usage: gh_read_gate24T2d.py <develop>"""
import json, os, re, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
A = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(A + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
DEV = sys.argv[1]
print('gh_read_gate24T2d', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'current develop', DEV)
for n in ('1250', '1253', '1262', '1263', '1264', '1265', '1266'):
    p = get('pulls/' + n)
    print('=== #%s head %s state %s merged %s mergeable %s mergeable_state %s draft %s base %s head.ref %s' % (n, p['head']['sha'], p['state'], p['merged'], p.get('mergeable'), p.get('mergeable_state'), p['draft'], p['base']['ref'], p['head']['ref']))
    t = p['title']; b = p['body'] or ''
    print('title (%d chars, ascii %s): %s' % (len(t), t.isascii(), t))
    print('body %d chars; KS keys %s; Refs lines %s; closing-word+key %d; hyphenated foreign keys %s' % (len(b), sorted(set(re.findall(r'KS-\d+', b))), re.findall(r'(?im)^\s*Refs\b.*$', b),
          len(re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+', b)), sorted(set(re.findall(r'KS-\d+', b)) - {'KS-1302', 'KS-1303', 'KS-1297', 'KS-1310', 'KS-1311', 'KS-1140', 'KS-1281', 'KS-1315', 'KS-1120'})))
    print('body markers: round 2 %s | environment matrix %s | UNREACHABLE %s | ruling %s | NOT COVERED %s' % ('ound 2' in b or 'OUND 2' in b, 'matrix' in b.lower(), b.count('UNREACHABLE'), b.count('uling'), 'NOT COVERED' in b.upper()))
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write('#%s %s\nhead %s\n\n%s\n' % (n, t, p['head']['sha'], b))
    f = get('pulls/%s/files?per_page=100' % n); print('files', len(f))
    for x in f: print('  %-8s +%d -%d %s %s' % (x['status'], x['additions'], x['deletions'], x['sha'], x['filename']))
    cs = get('pulls/%s/commits?per_page=100' % n); print('commits', len(cs))
    for c in cs: print('  %s parent %s | %s' % (c['sha'], ','.join(q['sha'][:12] for q in c['parents']), c['commit']['message'].splitlines()[0]))
    c = get('compare/%s...%s' % (DEV, p['head']['sha']))
    print('compare CURRENT develop...head: status %s merge_base %s ahead %d behind %d files %d %s' % (c['status'], c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c['files']), sorted(x['filename'] for x in c['files'])))
    com = get('issues/%s/comments?per_page=100' % n)
    with open(os.path.join(G, 'gh_comments_%s.md' % n), 'w', encoding='utf-8') as fh:
        for x in com: fh.write('--- comment %s by %s at %s\n%s\n' % (x['id'], x['user']['login'], x['created_at'], x['body']))
    print('issue comments', len(com), [(x['user']['login'], x['created_at']) for x in com])
op = get('pulls?state=open&per_page=100&sort=created&direction=desc')
print('=== WIDEN census: %d OPEN PRs; newest fifteen: %s' % (len(op), [(x['number'], x['head']['ref'][:70], x['created_at']) for x in op[:15]]))
r25 = [x for x in op if re.search(r'-(b29|l7r25|l8r25)-', x['head']['ref'])]
print('  OPEN PRs on ROUND-25 branches (-b29- / -l7r25- / -l8r25-): %s' % ([(x['number'], x['head']['sha'], x['head']['ref'], x['created_at']) for x in r25] or 'NONE'))
sib = [x for x in op if x['number'] in (1245, 1256, 1257, 1258, 1259, 1260, 1261)]
print('  sibling kit gate24T2c PRs still open: %s' % [(x['number'], x['head']['sha'][:12]) for x in sib])
