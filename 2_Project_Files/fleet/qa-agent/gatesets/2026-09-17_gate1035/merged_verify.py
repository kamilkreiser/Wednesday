import json, os, re, urllib.request
# Wednesday's at-source verification of seat A 8th's MERGED #1035 receipt (16:04:22Z). Shape: gate1033/merged_verify.py.
tok = os.environ['GH_TOKEN']; lk = os.environ['LINEAR_API_KEY']
def gh(p):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura' + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q}).encode(), headers={'Authorization': lk, 'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r))
ok = []
def chk(n, c, v): ok.append(bool(c)); print('PASS' if c else 'FAIL', n, str(v)[:150])
pr = gh('/pulls/1035'); sq = pr['merge_commit_sha']
chk('#1035 merged', pr['merged'], sq); chk('squash 34cdcfb26', (sq or '').startswith('34cdcfb26'), sq)
cmp = gh('/compare/' + sq + '...develop'); chk('develop contains squash', cmp['behind_by'] == 0, (cmp['status'], cmp['ahead_by']))
c = gh('/commits/' + sq); ps = [p['sha'] for p in c['parents']]
chk('one parent 3961c2add', len(ps) == 1 and ps[0].startswith('3961c2add'), ps)
chk('tree d21341805 (gate prediction)', c['commit']['tree']['sha'].startswith('d21341805'), c['commit']['tree']['sha'])
fs = {f['filename']: f['sha'] for f in c['files']}; chk('2 files', len(fs) == 2, sorted(fs))
for name, blob, pred in [('verification.ts', 'f888e8cd0', lambda k: k.endswith('services/api-gateway/src/routes/verification.ts')), ('ks1204 test', 'f1f9840ed', lambda k: 'ks1204' in k)]:
    hits = [(k, v) for k, v in fs.items() if pred(k)]; chk(name + ' ' + blob, len(hits) == 1 and hits[0][1].startswith(blob), hits)
msg = pr['title'] + '\n' + (pr['body'] or '') + '\n' + c['commit']['message']
cl = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(#\d+|KS-\d+|PS-\d+)', msg); chk('no closing phrase aimed at a ticket', not cl, cl)
chk('PR body names booleans (N-D)', re.search(r'(?i)boolean', pr['body'] or '') is not None, '')
d = lin('{ a: issue(id:"KS-1204"){ state{name} comments(first:100){nodes{id}} } b: issue(id:"KS-1231"){ state{name} priority } c: issue(id:"KS-1232"){ state{name} } d: issue(id:"KS-1233"){ state{name} priority } e: issue(id:"KS-1234"){ state{name} } f: issue(id:"KS-1230"){ comments(first:100){nodes{id}} } }')['data']
chk('KS-1204 In Progress', d['a']['state']['name'] == 'In Progress', d['a']['state'])
chk('KS-1204 comment 6897942a', any(n['id'].startswith('6897942a') for n in d['a']['comments']['nodes']), len(d['a']['comments']['nodes']))
for k, t in [('b', 'KS-1231'), ('c', 'KS-1232'), ('d', 'KS-1233'), ('e', 'KS-1234')]:
    chk(t + ' exists, Backlog', d[k] is not None and d[k]['state']['name'] == 'Backlog', d[k])
chk('KS-1230 comment bb04aa38', any(n['id'].startswith('bb04aa38') for n in d['f']['comments']['nodes']), len(d['f']['comments']['nodes']))
ctl = lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found', ctl.get('data') is None or ctl['data'].get('issue') is None, '')
print('ALL', 'PASS' if all(ok) else 'FAIL', sum(ok), '/', len(ok))
