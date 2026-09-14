#!/usr/bin/env python3
"""linear_read.py — READ-ONLY Linear GraphQL reads for the #799 (KS-764) TIER-1 gate set. Key sourced by NAME
(LINEAR_API_KEY) from the Secuura .env; never printed. comments(first:50) sorted client-side by createdAt; never
last:N. includeArchived:true everywhere. Also the board search by SYMBOL/path for the hypotheses this brief names."""
import json, sys, urllib.request, datetime, re
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
key = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY not found by name'
print('LINEAR_API_KEY: set')
def gql(q, v):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60)
    j = json.load(r)
    assert 'errors' not in j, j.get('errors')
    return j['data']
Q = '''query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true, first:5){ nodes{
  identifier title state{name} priorityLabel assignee{name} archivedAt updatedAt createdAt description branchName
  attachments(first:20){nodes{url title}}
  relations(first:20){nodes{type relatedIssue{identifier}}}
  inverseRelations(first:20){nodes{type issue{identifier}}}
  comments(first:50){nodes{id createdAt user{name} body bodyData}} }}}'''
S = '''query($q:String!){ issues(filter:{team:{key:{eq:"KS"}}, or:[{title:{containsIgnoreCase:$q}},{description:{containsIgnoreCase:$q}}]}, includeArchived:true, first:40){ nodes{ identifier title state{name} archivedAt } } }'''
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
HEAD = '6da848891'
for n in [764, 860, 779, 643, 650, 742, 780, 577, 578, 795, 485, 876]:
    d = gql(Q, {'n': n})['issues']['nodes']
    if not d:
        print(f'KS-{n}: NOT FOUND'); continue
    i = d[0]
    json.dump(i, open(f'{G}/linear/ks{n}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    att = [a['url'].split('/')[-1] if 'github.com' in (a['url'] or '') else (a['title'] or a['url'])[:40] for a in i['attachments']['nodes']]
    print(f"KS-{n}: {i['state']['name']} | {i['priorityLabel']} | assignee={(i['assignee'] or {}).get('name')} | archived={i['archivedAt']} | updated={i['updatedAt']} | created={i['createdAt']} | attachments={att} | comments={len(cs)} | desc chars={len(i['description'] or '')} | branch={i['branchName']} | title={i['title'][:110]!r}")
    print(f"   relations={[ (r['type'], r['relatedIssue']['identifier']) for r in i['relations']['nodes']]} inverse={[ (r['type'], r['issue']['identifier']) for r in i['inverseRelations']['nodes']]}")
    for c in cs:
        b = c['body'] or ''
        bd = c.get('bodyData') or ''
        mentions = bd.count('suggestion_userMentions') if isinstance(bd, str) else 0
        print(f"   comment {c['id'][:8]} {c['createdAt']} {(c['user'] or {}).get('name')} chars={len(b)} at-signs={b.count('@')} mention-nodes={mentions} head={HEAD in b} KS={sorted(set(re.findall(r'KS-\d+', b)))}")
        if n in (764, 779, 780):
            open(f"{G}/linear/ks{n}_comment_{c['id'][:8]}.md", 'w', encoding='utf-8').write(b)
    if n == 764:
        open(f'{G}/linear/ks764_description.md', 'w', encoding='utf-8').write(i['description'] or '')
print('--- board search by SYMBOL/path (title OR description, includeArchived)')
for q in ['decideKeyRevoke', 'decideTenantAccess', 'caller has no tenant', 'caller has no organisation', 'normOrgId', 'normaliseOrgId', 'isOrgBoundedRole', 'ORG_BOUNDED_ROLES', 'lookupKeyForRevoke', 'extractTenantContext', 'req.tenantId', 'svc_api_keys', 'api-keys/:id', '/api/keys/:id', 'Not authorised to revoke', 'decision.status', 'default-tenant', 'a0000000-0000-4000-8000-000000000001', 'organization_id', 'ks860', 'listen(0', 'stale dist', 'packages/shared/dist', 'revoke']:
    r = gql(S, {'q': q})['issues']['nodes']
    print(f"search {q!r}: {len(r)} -> {[(x['identifier'], x['state']['name'], 'A' if x['archivedAt'] else '') for x in r]}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
