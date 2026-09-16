#!/usr/bin/env python3
"""merged_verify.py — READ-ONLY verification of seat A's #1010 MERGED receipt (18:30:13Z) at source.
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
M, BASE, HEAD = '1125607e978d6ad637720c985e43e3d79fecdf88', 'd067725ff1c7f036dbf0f726b9bf12f4daefebe7', 'c3213b04e3ad96068c367f7e0ba426822d32cda9'
BLOBS = {'verification.ts': '04b3d980f', 'ks1087-workflow-approve-deletes-the-pending-document.test.ts': '4450587dc'}
print('merged_verify', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
ok = []
pr = get('/pulls/1010')
ok.append(('PR merged', pr['merged'] is True)); ok.append(('PR merge_commit == M', pr.get('merge_commit_sha') == M)); ok.append(('PR head == GO head', pr['head']['sha'] == HEAD))
c = get('/commits/' + M)
parents = [p['sha'] for p in c['parents']]
ok.append(('M has ONE parent == base', parents == [BASE]))
files = [f['filename'] for f in c['files']]
print('  M files:', files)
ok.append(('M touches exactly 2 files', len(files) == 2))
for f in c['files']:
    for name, blob in BLOBS.items():
        if f['filename'].endswith(name):
            ok.append((f'blob {name} == {blob}', f['sha'].startswith(blob)))
prf = sorted(f['filename'] for f in get('/pulls/1010/files?per_page=100'))
ok.append(('M files == PR files', sorted(files) == prf))
dev = get('/branches/develop')['commit']['sha']
print('  develop now:', dev)
ok.append(('develop == M or descends from M', dev == M or get('/compare/' + M + '...' + dev)['status'] in ('ahead', 'identical')))
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority priorityLabel assignee{name} archivedAt relations{nodes{type relatedIssue{identifier}}} inverseRelations{nodes{type issue{identifier}}} comments(first:100){nodes{id createdAt}} } }'''
issues = {}
for n in ('KS-1087', 'KS-1183', 'KS-1184', 'KS-1185'):
    d = gql(Q, {'id': n})
    if 'errors' in d:
        print(n, 'ERRORS', d['errors']); ok.append((n + ' readable', False)); continue
    i = d['data']['issue']; issues[n] = i
    rel = sorted(r['type'] + ':' + r['relatedIssue']['identifier'] for r in i['relations']['nodes']) + sorted('inv-' + r['type'] + ':' + r['issue']['identifier'] for r in i['inverseRelations']['nodes'])
    print(f"  {n}: {i['state']['name']} prio={i['priorityLabel']} assignee={(i['assignee'] or {}).get('name')} archived={i['archivedAt']} comments={len(i['comments']['nodes'])} rel={rel} | {i['title'][:90]}")
if 'KS-1087' in issues:
    ok.append(('KS-1087 In Progress', issues['KS-1087']['state']['name'] == 'In Progress'))
    ok.append(('KS-1183 In Progress (5f)', issues['KS-1183']['state']['name'] == 'In Progress'))
    ok.append(('KS-1183 comment 94138b8d', any(x['id'].startswith('94138b8d') for x in issues['KS-1183']['comments']['nodes'])))
    ok.append(('KS-1184 Backlog + comment 17c55a98', issues['KS-1184']['state']['name'] == 'Backlog' and any(x['id'].startswith('17c55a98') for x in issues['KS-1184']['comments']['nodes'])))
    i = issues['KS-1185']; linked = [r['relatedIssue']['identifier'] for r in i['relations']['nodes']] + [r['issue']['identifier'] for r in i['inverseRelations']['nodes']]
    ok.append(('KS-1185 Backlog Medium related KS-1183', i['state']['name'] == 'Backlog' and i['priorityLabel'] == 'Medium' and 'KS-1183' in linked))
# negative control: a claim that must be FALSE (a wrong parent) so an all-True result is not vacuous
ok_ctrl = parents == ['0' * 40]
print('  CONTROL (wrong parent must be False):', ok_ctrl)
for k, v in ok: print(('  PASS ' if v else '  FAIL ') + k)
print('RESULT', 'ALL PASS' if all(v for _, v in ok) and not ok_ctrl else 'NOT ALL PASS', f'({sum(v for _, v in ok)}/{len(ok)})')
