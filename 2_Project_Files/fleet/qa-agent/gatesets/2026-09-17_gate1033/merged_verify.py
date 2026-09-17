import json, os, re, urllib.request
# Wednesday's at-source verification of Seat B's MERGED #1033 receipt (13:41:42Z). Shape: gate1030/merged_verify.py.
tok = os.environ['GH_TOKEN']; lk = os.environ['LINEAR_API_KEY']
def gh(p):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura' + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
def lin(q):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q}).encode(), headers={'Authorization': lk, 'Content-Type': 'application/json'}); return json.load(urllib.request.urlopen(r))
ok = []
def chk(n, c, v): ok.append(bool(c)); print('PASS' if c else 'FAIL', n, str(v)[:150])
pr = gh('/pulls/1033'); sq = pr['merge_commit_sha']
chk('#1033 merged', pr['merged'], sq); chk('squash 3961c2add', (sq or '').startswith('3961c2add'), sq)
cmp = gh('/compare/' + sq + '...develop'); chk('develop contains squash', cmp['behind_by'] == 0, (cmp['status'], cmp['ahead_by']))
c = gh('/commits/' + sq); ps = [p['sha'] for p in c['parents']]
chk('one parent 732c13459', len(ps) == 1 and ps[0].startswith('732c13459'), ps)
chk('tree ad795aa72 (gate prediction)', c['commit']['tree']['sha'].startswith('ad795aa72'), c['commit']['tree']['sha'])
fs = {f['filename']: f['sha'] for f in c['files']}; chk('5 files', len(fs) == 5, sorted(fs))
for name, blob, pred in [('audit-baseline', '91d8b71c9', lambda k: k.endswith('scripts/audit/audit-baseline.json')), ('root lock', '646c19f6f', lambda k: k == 'Blockchain/Dev/package-lock.json'),
                         ('root package.json', '773443a9f', lambda k: k == 'Blockchain/Dev/package.json'), ('originate lock', '4c1800aee', lambda k: k.endswith('services/originate/package-lock.json')),
                         ('originate package.json', 'd4435238d', lambda k: k.endswith('services/originate/package.json'))]:
    hits = [(k, v) for k, v in fs.items() if pred(k)]; chk(name + ' ' + blob, len(hits) == 1 and hits[0][1].startswith(blob), hits)
msg = pr['title'] + '\n' + (pr['body'] or '') + '\n' + c['commit']['message']
cl = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(#\d+|KS-\d+|PS-\d+)', msg); chk('no closing phrase aimed at a ticket', not cl, cl)
d = lin('{ a: issue(id:"KS-763"){ state{name} comments(first:100){nodes{id}} } b: issue(id:"KS-1216"){ comments(first:100){nodes{id}} } }')['data']
chk('KS-763 In Progress', d['a']['state']['name'] == 'In Progress', d['a']['state'])
chk('KS-763 comment 45ff3f49', any(n['id'].startswith('45ff3f49') for n in d['a']['comments']['nodes']), len(d['a']['comments']['nodes']))
chk('KS-1216 comment 67dedbec', any(n['id'].startswith('67dedbec') for n in d['b']['comments']['nodes']), len(d['b']['comments']['nodes']))
ctl = lin('{ issue(id:"KS-999999"){ id } }'); chk('control KS-999999 not found', ctl.get('data') is None or ctl['data'].get('issue') is None, '')
print('ALL', 'PASS' if all(ok) else 'FAIL', sum(ok), '/', len(ok))
