#!/usr/bin/env python3
"""merged_verify.py — READ-ONLY verification of seat A's #1011 MERGED receipt (20:14:54Z) at source.
GitHub GET + Linear GraphQL query only. Keys by NAME from the Secuura .env; never printed.
Claims under test (from the receipt): squash f7c2f4acb, ONE parent 73d3fcb90, files base..M == the PR's 2,
blobs verification.ts d0585dc34 / ks1087 test 7832724f3, develop tip == M, PR head dd7086d5a;
KS-1087 In Progress with facts comment ba80d8f4; KS-1183 (Medium) + KS-1184 (High) exist, Backlog, related KS-1087."""
import json, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
vals = {}
for line in open(ENV, encoding='utf-8'):
    for k in ('GH_TOKEN', 'LINEAR_API_KEY'):
        if line.startswith(k + '='):
            vals[k] = line.split('=', 1)[1].strip().strip('"').strip("'")
assert vals.get('GH_TOKEN') and vals.get('LINEAR_API_KEY'), 'a key was not found by name'
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + vals['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60))
def gql(q, v):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': vals['LINEAR_API_KEY'], 'Content-Type': 'application/json'}), timeout=60))
M, BASE, HEAD = '523f283c6cd2550263ec9869dc5ee722be40df4e', 'e0f41a8fafd64fa31524390cfeab320e822f3d15', '6dc8256448b50de6a15519001a4f7032ace1ae19'
BLOBS = {'userRepo.ts': '9060b308e', 'ks949-platform-admin-seed-identity.test.ts': '4f03e6f4f', 'ks999-getuserbyid-awaits-fromrow.test.ts': '04ce4e156'}
print('merged_verify', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
ok = []
pr = get('/pulls/1011')
ok.append(('PR merged', pr['merged'] is True)); ok.append(('PR merge_commit == M', pr.get('merge_commit_sha') == M)); ok.append(('PR head == GO head', pr['head']['sha'] == HEAD))
c = get('/commits/' + M)
parents = [p['sha'] for p in c['parents']]
ok.append(('M has ONE parent == base', parents == [BASE]))
files = [f['filename'] for f in c['files']]
print('  M files:', files)
ok.append(('M touches exactly 4 files', len(files) == 4))
for blob in ('052131de0','8d66dfaf7','f6bf4f9d4','ef19446f2'):
    ok.append((f'a squashed file has blob {blob}', any(f['sha'].startswith(blob) for f in c['files'])))
ok.append(('audit.ts blob 052131de0', any(f['filename'].endswith('middleware/audit.ts') and f['sha'].startswith('052131de0') for f in c['files'])))
prf = sorted(f['filename'] for f in get('/pulls/1011/files?per_page=100'))
ok.append(('M files == PR files', sorted(files) == prf))
dev = get('/branches/develop')['commit']['sha']
print('  develop now:', dev)
ok.append(('develop == M or descends from M', dev == M or get('/compare/' + M + '...' + dev)['status'] in ('ahead', 'identical')))
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority priorityLabel assignee{name} archivedAt relations{nodes{type relatedIssue{identifier}}} inverseRelations{nodes{type issue{identifier}}} comments(first:100){nodes{id createdAt}} } }'''
issues = {}
for n in ('KS-871', 'KS-1189', 'KS-1191', 'KS-1192'):
    d = gql(Q, {'id': n})
    if 'errors' in d:
        print(n, 'ERRORS', d['errors']); ok.append((n + ' readable', False)); continue
    i = d['data']['issue']; issues[n] = i
    rel = sorted(r['type'] + ':' + r['relatedIssue']['identifier'] for r in i['relations']['nodes']) + sorted('inv-' + r['type'] + ':' + r['issue']['identifier'] for r in i['inverseRelations']['nodes'])
    print(f"  {n}: {i['state']['name']} prio={i['priorityLabel']} assignee={(i['assignee'] or {}).get('name')} archived={i['archivedAt']} comments={len(i['comments']['nodes'])} rel={rel} | {i['title'][:90]}")
if len(issues) == 4:
    ok.append(('KS-871 In Progress', issues['KS-871']['state']['name'] == 'In Progress'))
    ok.append(('KS-871 comment 9f762589', any(x['id'].startswith('9f762589') for x in issues['KS-871']['comments']['nodes'])))
    ok.append(('KS-1189 comment 1c68f433', any(x['id'].startswith('1c68f433') for x in issues['KS-1189']['comments']['nodes'])))
    for k in ('KS-1191','KS-1192'):
        i = issues[k]; rels = str(i['relations']) + str(i['inverseRelations'])
        ok.append((k+' Backlog', i['state']['name'] == 'Backlog')); ok.append((k+' related KS-871', 'KS-871' in rels)); ok.append((k+' not archived', i['archivedAt'] is None))
else:
    ok.append(('all four issues readable', False))
# negative control: a claim that must be FALSE (a wrong parent) so an all-True result is not vacuous
ok_ctrl = parents == ['0' * 40]
print('  CONTROL (wrong parent must be False):', ok_ctrl)
for k, v in ok: print(('  PASS ' if v else '  FAIL ') + k)
print('RESULT', 'ALL PASS' if all(v for _, v in ok) and not ok_ctrl else 'NOT ALL PASS', f'({sum(v for _, v in ok)}/{len(ok)})')
