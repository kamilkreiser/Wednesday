#!/usr/bin/env python3
"""merged_verify.py — READ-ONLY verification of seat A's #1008 MERGED receipt (17:22:11Z) at source.
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
M, BASE, HEAD = 'f7c2f4acb28875e3665a61c8eaaad5c54bd3aa55', '73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5', 'dd7086d5aa574285beffc515f9371a438621f25d'
BLOBS = {'verification.ts': 'd0585dc34', 'ks1087-workflow-approve-deletes-the-pending-document.test.ts': '7832724f3'}
print('merged_verify', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
ok = []
pr = get('/pulls/1008')
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
prf = sorted(f['filename'] for f in get('/pulls/1008/files?per_page=100'))
ok.append(('M files == PR files', sorted(files) == prf))
dev = get('/branches/develop')['commit']['sha']
print('  develop now:', dev)
ok.append(('develop == M or descends from M', dev == M or get('/compare/' + M + '...' + dev)['status'] in ('ahead', 'identical')))
Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority priorityLabel assignee{name} archivedAt relations{nodes{type relatedIssue{identifier}}} inverseRelations{nodes{type issue{identifier}}} comments(first:100){nodes{id createdAt}} } }'''
issues = {}
for n in ('KS-1087', 'KS-1183', 'KS-1184'):
    d = gql(Q, {'id': n})
    if 'errors' in d:
        print(n, 'ERRORS', d['errors']); ok.append((n + ' readable', False)); continue
    i = d['data']['issue']; issues[n] = i
    rel = sorted(r['type'] + ':' + r['relatedIssue']['identifier'] for r in i['relations']['nodes']) + sorted('inv-' + r['type'] + ':' + r['issue']['identifier'] for r in i['inverseRelations']['nodes'])
    print(f"  {n}: {i['state']['name']} prio={i['priorityLabel']} assignee={(i['assignee'] or {}).get('name')} archived={i['archivedAt']} comments={len(i['comments']['nodes'])} rel={rel} | {i['title'][:90]}")
if 'KS-1087' in issues:
    ok.append(('KS-1087 In Progress', issues['KS-1087']['state']['name'] == 'In Progress'))
    ok.append(('facts comment ba80d8f4 present', any(x['id'].startswith('ba80d8f4') for x in issues['KS-1087']['comments']['nodes'])))
for n, lab in (('KS-1183', 'Medium'), ('KS-1184', 'High')):
    if n in issues:
        i = issues[n]
        ok.append((f'{n} Backlog', i['state']['name'] == 'Backlog')); ok.append((f'{n} priority {lab}', i['priorityLabel'] == lab))
        linked = [r['relatedIssue']['identifier'] for r in i['relations']['nodes']] + [r['issue']['identifier'] for r in i['inverseRelations']['nodes']]
        ok.append((f'{n} related KS-1087', 'KS-1087' in linked))
# negative control: a claim that must be FALSE (a wrong parent) so an all-True result is not vacuous
ok_ctrl = parents == ['0' * 40]
print('  CONTROL (wrong parent must be False):', ok_ctrl)
for k, v in ok: print(('  PASS ' if v else '  FAIL ') + k)
print('RESULT', 'ALL PASS' if all(v for _, v in ok) and not ok_ctrl else 'NOT ALL PASS', f'({sum(v for _, v in ok)}/{len(ok)})')
