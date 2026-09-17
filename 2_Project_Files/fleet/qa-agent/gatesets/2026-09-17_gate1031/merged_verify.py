import json, os, re, urllib.request
# Wednesday's at-source verification of seat A's MERGED #1031 receipt (13:19:07Z). Shape: gate1030/merged_verify.py.
tok = os.environ['GH_TOKEN']; lk = os.environ['LINEAR_API_KEY']
def gh(p):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura' + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q}).encode(), headers={'Authorization': lk, 'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r))
ok = []
def chk(n, c, v): ok.append(bool(c)); print('PASS' if c else 'FAIL', n, str(v)[:160])
pr = gh('/pulls/1031'); sq = pr['merge_commit_sha']
chk('#1031 merged', pr['merged'], sq); chk('squash 732c13459', (sq or '').startswith('732c13459'), sq)
cmp = gh('/compare/' + sq + '...develop'); chk('develop contains squash', cmp['behind_by'] == 0, (cmp['status'], cmp['ahead_by']))
c = gh('/commits/' + sq); ps = [p['sha'] for p in c['parents']]
chk('one parent 27e53ec3a', len(ps) == 1 and ps[0].startswith('27e53ec3a'), ps)
chk('tree 007cca429 (gate prediction)', c['commit']['tree']['sha'].startswith('007cca429'), c['commit']['tree']['sha'])
fs = {f['filename']: f['sha'] for f in c['files']}
chk('3 files', len(fs) == 3, sorted(fs))
chk('documents.ts e3eeb5a68', any(k.endswith('originate/src/routes/documents.ts') and v.startswith('e3eeb5a68') for k, v in fs.items()), fs)
chk('certifications.ts 20934ee94', any(k.endswith('originate/src/routes/certifications.ts') and v.startswith('20934ee94') for k, v in fs.items()), fs)
chk('ks1213 test 808282689', any('ks1213' in k and v.startswith('808282689') for k, v in fs.items()), fs)
msg = pr['title'] + '\n' + (pr['body'] or '') + '\n' + c['commit']['message']
cl = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(#\d+|KS-\d+|PS-\d+)', msg); chk('no closing phrase aimed at a ticket', not cl, cl)
d = lin('{ a: issue(id:"KS-1213"){ state{name} comments(first:100){nodes{id}} } b: issue(id:"KS-1228"){ title state{name} } c: issue(id:"KS-1229"){ title state{name} } }')['data']
chk('KS-1213 In Progress', d['a']['state']['name'] == 'In Progress', d['a']['state'])
chk('KS-1213 comment c8ff0ab1', any(n['id'].startswith('c8ff0ab1') for n in d['a']['comments']['nodes']), len(d['a']['comments']['nodes']))
chk('KS-1228 exists', d['b'] is not None, d['b'])
chk('KS-1229 exists', d['c'] is not None, d['c'])
ctl = lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found', ctl.get('data') is None or ctl['data'].get('issue') is None, '')
print('ALL', 'PASS' if all(ok) else 'FAIL', sum(ok), '/', len(ok))
