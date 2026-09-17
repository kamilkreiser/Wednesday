import json, os, re, urllib.request
# Wednesday's at-source verification of seat A's MERGED #1029 receipt (12:49:37Z). Shape: gate1030/merged_verify.py.
tok = os.environ['GH_TOKEN']; lk = os.environ['LINEAR_API_KEY']
def gh(p):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura' + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q}).encode(), headers={'Authorization': lk, 'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r))
ok = []
def chk(n, c, v): ok.append(bool(c)); print('PASS' if c else 'FAIL', n, str(v)[:160])
pr = gh('/pulls/1029'); sq = pr['merge_commit_sha']
chk('#1029 merged', pr['merged'], sq); chk('squash 27e53ec3a', (sq or '').startswith('27e53ec3a'), sq)
cmp = gh('/compare/' + sq + '...develop'); chk('develop contains squash', cmp['behind_by'] == 0, (cmp['status'], cmp['ahead_by']))
c = gh('/commits/' + sq); ps = [p['sha'] for p in c['parents']]
chk('one parent bb848b828', len(ps) == 1 and ps[0].startswith('bb848b828'), ps)
chk('tree 38dd44d8c (gate prediction)', c['commit']['tree']['sha'].startswith('38dd44d8c'), c['commit']['tree']['sha'])
fs = {f['filename']: f['sha'] for f in c['files']}
chk('1 file', len(fs) == 1, sorted(fs))
chk('ks1072 test blob d9c98320e', any('ks1072-the-latest-anchor-selector' in k and v.startswith('d9c98320e') for k, v in fs.items()), fs)
msg = pr['title'] + '\n' + (pr['body'] or '') + '\n' + c['commit']['message']
cl = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(#\d+|KS-\d+|PS-\d+)', msg); chk('no closing phrase aimed at a ticket', not cl, cl)
d = lin('{ a: issue(id:"KS-1180"){ state{name} comments(first:100){nodes{id}} } b: issue(id:"KS-1227"){ title state{name} } }')['data']
chk('KS-1180 In Progress', d['a']['state']['name'] == 'In Progress', d['a']['state'])
chk('KS-1180 comment 17822539', any(n['id'].startswith('17822539') for n in d['a']['comments']['nodes']), len(d['a']['comments']['nodes']))
chk('KS-1227 exists, Backlog', d['b'] is not None and d['b']['state']['name'] == 'Backlog', d['b'])
ctl = lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found', ctl.get('data') is None or ctl['data'].get('issue') is None, '')
print('ALL', 'PASS' if all(ok) else 'FAIL', sum(ok), '/', len(ok))
