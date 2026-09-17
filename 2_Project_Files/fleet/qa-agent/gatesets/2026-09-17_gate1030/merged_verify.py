import json, os, re, urllib.request
# Wednesday's at-source verification of Seat B's MERGED #1030 receipt (12:22:59Z). Shape: gate1028/merged_verify.py.
tok = os.environ['GH_TOKEN']; lk = os.environ['LINEAR_API_KEY']
def gh(p):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura' + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(r))
def lin(q):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q}).encode(), headers={'Authorization': lk, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r))
ok = []
def chk(n, c, v): ok.append(bool(c)); print('PASS' if c else 'FAIL', n, str(v)[:160])
pr = gh('/pulls/1030'); sq = pr['merge_commit_sha']
chk('#1030 merged', pr['merged'], sq)
chk('squash bb848b828', (sq or '').startswith('bb848b828'), sq)
cmp = gh('/compare/' + sq + '...develop'); chk('develop contains squash', cmp['behind_by'] == 0, (cmp['status'], cmp['ahead_by'], cmp['behind_by']))
c = gh('/commits/' + sq); ps = [p['sha'] for p in c['parents']]
chk('one parent 0a2b1603f', len(ps) == 1 and ps[0].startswith('0a2b1603f'), ps)
chk('tree 567ff9457 (gate prediction)', c['commit']['tree']['sha'].startswith('567ff9457'), c['commit']['tree']['sha'])
fs = {f['filename']: f['sha'] for f in c['files']}
chk('43 files', len(fs) == 43, len(fs))
prf = {}
page = 1
while True:
    b = gh('/pulls/1030/files?per_page=100&page=%d' % page)
    prf.update({f['filename']: f['sha'] for f in b})
    if len(b) < 100: break
    page += 1
chk('file set == PR head file set', set(fs) == set(prf), (len(fs), len(prf)))
chk('43/43 blobs == PR head', all(fs.get(k) == v for k, v in prf.items()), sum(fs.get(k) == v for k, v in prf.items()))
targets = [('scripts/audit/audit-baseline.json', 'b647dd66e'), ('Blockchain/Dev/package-lock.json', '5bd5680f8'),
           ('frontend/issuer/package-lock.json', 'd51db26d5'), ('services/auth/package-lock.json', '2d91a356a'),
           ('services/api-gateway/package-lock.json', '5ec55d86d'), ('services/vc-issuer/package-lock.json', 'b0b66b501'),
           ('services/referral/package-lock.json', 'c7bd74580'), ('systemTest/performance/package-lock.json', '91563c0d8')]
for suffix, blob in targets:
    hits = [(k, v) for k, v in fs.items() if (k == suffix if suffix.startswith('Blockchain/Dev/package') else k.endswith(suffix))]
    chk(suffix + ' ' + blob, len(hits) == 1 and hits[0][1].startswith(blob), hits)
# control: a wrong blob prefix must not match
chk('control: baseline != 000000000', not any(k.endswith('audit-baseline.json') and v.startswith('000000000') for k, v in fs.items()), '')
msg = pr['title'] + '\n' + (pr['body'] or '') + '\n' + c['commit']['message']
closing = re.findall(r'(?i)\b(close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(#\d+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#\d+|KS-\d+|PS-\d+)', msg)
chk('no closing phrase aimed at an issue/ticket', not closing, closing)
q = '{ a: issue(id:"KS-1211"){ state{name} comments(first:100){nodes{id}} attachments{nodes{url metadata}} } b: issue(id:"KS-1224"){ title state{name} assignee{email} } c: issue(id:"KS-1225"){ title state{name} assignee{email} } d: issue(id:"KS-1226"){ title state{name} assignee{email} } }'
d = lin(q)['data']
chk('KS-1211 In Progress', d['a']['state']['name'] == 'In Progress', d['a']['state'])
chk('KS-1211 comment 1d974cf4', any(n['id'].startswith('1d974cf4') for n in d['a']['comments']['nodes']), len(d['a']['comments']['nodes']))
att = [n for n in d['a']['attachments']['nodes'] if n['url'].endswith('/pull/1030')]
chk('pull/1030 attachment present', len(att) == 1, [n['url'] for n in att])
for k, t in (('b', 'KS-1224'), ('c', 'KS-1225'), ('d', 'KS-1226')):
    chk(t + ' exists, Backlog', d[k] is not None and d[k]['state']['name'] == 'Backlog', d[k])
ctl = lin('{ issue(id:"KS-999999"){ id } }')
chk('control KS-999999 not found', ctl.get('data') is None or ctl['data'].get('issue') is None, '')
print('ALL', 'PASS' if all(ok) else 'FAIL', sum(ok), '/', len(ok))
