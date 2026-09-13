#!/usr/bin/env python3
"""linear_read.py — READ-ONLY Linear GraphQL reads for the #983 (KS-823) TIER-1 gate set. Key sourced by NAME
(LINEAR_API_KEY) from the Secuura .env; never printed. comments(first:50) sorted client-side by createdAt; never last:N.
includeArchived:true everywhere. Second half: board search by SYMBOL/path (title OR description containsIgnoreCase)."""
import json, sys, urllib.request, datetime, re
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
key = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY not found by name'
def gql(q, v):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60)
    j = json.load(r)
    assert 'errors' not in j, j.get('errors')
    return j['data']
Q = '''query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true, first:5){ nodes{
  identifier title state{name} priorityLabel assignee{name} archivedAt updatedAt createdAt description branchName
  labels(first:10){nodes{name}}
  attachments(first:20){nodes{url title}}
  relations(first:20){nodes{type relatedIssue{identifier}}}
  inverseRelations(first:20){nodes{type issue{identifier}}}
  comments(first:50){nodes{id createdAt user{name} body bodyData}} }}}'''
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
HEAD = 'f62c975c1'; PARENT = 'e62eab87a'
WANT = {'e64ec267', '0dc34f52', 'ae44fc27', '127be01e', '2bd1eed7', 'c93826d9', 'c1fac6b7', '07033bb9'}
for n in [823, 790, 835, 1003, 820, 821, 822, 255, 458, 43, 825, 831, 799, 841, 798]:
    d = gql(Q, {'n': n})['issues']['nodes']
    if not d: print(f'KS-{n}: NOT FOUND'); continue
    i = d[0]
    json.dump(i, open(f'{G}/linear/ks{n}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    att = [a['url'].split('/')[-1] for a in i['attachments']['nodes'] if 'github.com' in a['url']]
    desc = i['description'] or ''
    print(f"{i['identifier']} [{i['state']['name']}] {i['priorityLabel']} assignee={i['assignee']['name'] if i['assignee'] else None} labels={[l['name'] for l in i['labels']['nodes']]} archived={i['archivedAt']} created={i['createdAt']} updated={i['updatedAt']} PRs={att} attachments={len(i['attachments']['nodes'])} comments={len(cs)} desc={len(desc)}c at-signs={desc.count('@')} branch={i['branchName'][:80]!r} title={i['title'][:100]!r}")
    print('   related:', [(r['type'], r['relatedIssue']['identifier']) for r in i['relations']['nodes']], 'inverse:', [(r['type'], r['issue']['identifier']) for r in i['inverseRelations']['nodes']])
    if n in (823, 790, 835, 1003):
        open(f'{G}/linear/ks{n}_desc.md', 'w', encoding='utf-8').write(desc)
    for c in cs:
        b = c['body'] or ''; bd = c['bodyData'] or ''
        mention = bd.count('suggestion_userMentions')
        flag = '  <<< named id' if c['id'][:8] in WANT else ''
        if n in (823, 790, 835, 1003) or c['id'][:8] in WANT:
            open(f"{G}/linear/ks{n}_comment_{c['id'][:8]}.md", 'w', encoding='utf-8').write(b)
        print(f"   comment {c['id'][:8]} {c['createdAt']} {c['user']['name'] if c['user'] else 'bot'} chars={len(b)} at-signs={b.count('@')} mention-nodes={mention} head={HEAD in b} parent={PARENT in b} KS={sorted(set(re.findall(r'KS-\d+', b)))}{flag}")
S = '''query($q:String!){ issues(filter:{team:{key:{eq:"KS"}}, or:[{title:{containsIgnoreCase:$q}},{description:{containsIgnoreCase:$q}}]}, includeArchived:true, first:40){ nodes{ identifier title state{name} archivedAt } } }'''
print('--- board search by SYMBOL/path (title OR description, includeArchived:true)')
for q in ['verifyRefreshToken', 'readClientId', 'OAuthTokenClaims', 'OAuthMintOptions', 'client_id', 'refresh_token', '/api/auth/refresh', 'authRoutes.post(\'/refresh\'', 'denylistRefreshJti', 'rotateSessionRefreshToken', 'grant_type=refresh_token', 'token binding', 'invalid_client', 'getAppByClientId', 'verifyClientSecret', 'readClientSecret', 'is_active', 'generateTokenPair', 'jwt.ts', 'routes/oauth.ts', 'routes/auth.ts', 'KS-823', 'grandfather', 'fail-closed', 'ks823', 'ks790', 'KS-790']:
    r = gql(S, {'q': q})['issues']['nodes']
    print(f"search {q!r}: {len(r)} -> {[(x['identifier'], x['state']['name'], 'A' if x['archivedAt'] else '') for x in r]}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
