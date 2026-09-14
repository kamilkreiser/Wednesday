#!/usr/bin/env python3
"""linear_read.py — READ-ONLY Linear GraphQL reads for the L7 TIER-2 gate set (#918 r2 / #924 / #925). Key sourced by NAME
(LINEAR_API_KEY) from the Secuura .env; never printed. comments(first:50) sorted client-side by createdAt; never last:N.
includeArchived:true everywhere. Then a board search by SYMBOL/path (title OR description containsIgnoreCase)."""
import json, sys, urllib.request, datetime, re
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
G = sys.argv[1]
key = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('LINEAR_API_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY not found by name'
def gql(q, v):
    r = urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': key, 'Content-Type': 'application/json'}), timeout=60)
    j = json.load(r)
    assert 'errors' not in j, j.get('errors')
    return j['data']
Q = '''query($n:Float!){ issues(filter:{team:{key:{eq:"KS"}}, number:{eq:$n}}, includeArchived:true, first:5){ nodes{
  identifier title state{name} priorityLabel assignee{name} archivedAt updatedAt createdAt description branchName
  parent{identifier} attachments(first:20){nodes{url title}}
  relations(first:20){nodes{type relatedIssue{identifier}}}
  inverseRelations(first:20){nodes{type issue{identifier}}}
  comments(first:50){nodes{id createdAt user{name} body bodyData}} }}}'''
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
HEADS = {'b54487216': 918, 'b85f1db24': 924, '5341b1dae': 925, 'a4f71cde6': 903}
WANT = {'94125113', 'affad068', 'f7c3bb90', 'e265a29d', '4be081ee', '7c19d519', '09e17ee8', 'e1e526bc'}
for n in [926, 773, 1046, 1149, 771, 485, 991, 731, 687, 1032, 1033, 1034, 1047, 1138, 1148, 1075, 1077, 962, 772]:
    d = gql(Q, {'n': n})['issues']['nodes']
    if not d:
        print(f'KS-{n}: NOT FOUND'); continue
    i = d[0]
    json.dump(i, open(f'{G}/linear/ks{n}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    att = [a['url'].split('/')[-1] for a in i['attachments']['nodes'] if 'github.com' in a['url']]
    desc = i['description'] or ''
    print(f"{i['identifier']} [{i['state']['name']}] {i['priorityLabel']} assignee={i['assignee']['name'] if i['assignee'] else None} parent={i['parent']['identifier'] if i['parent'] else None} archived={i['archivedAt']} created={i['createdAt']} updated={i['updatedAt']} PRs={att} comments={len(cs)} desc={len(desc)}c at-signs={desc.count('@')} title={i['title'][:110]!r}")
    print('   related:', [(r['type'], r['relatedIssue']['identifier']) for r in i['relations']['nodes']], 'inverse:', [(r['type'], r['issue']['identifier']) for r in i['inverseRelations']['nodes']])
    if n in (926, 773, 1046, 1149):
        open(f'{G}/linear/ks{n}_desc.md', 'w', encoding='utf-8').write(desc)
        print('   desc KS ids:', sorted(set(re.findall(r'KS-\d+', desc))), 'PR refs:', sorted(set(re.findall(r'#\d{3,4}', desc))))
    for c in cs:
        b = c['body'] or ''; bd = c['bodyData'] or ''
        mention = bd.count('suggestion_userMentions')
        heads = [f'#{v}' for k, v in HEADS.items() if k in b]
        flag = '  <<< named id' if c['id'][:8] in WANT else ''
        if n in (926, 773, 1046, 1149, 485) or c['id'][:8] in WANT:
            open(f"{G}/linear/ks{n}_comment_{c['id'][:8]}.md", 'w', encoding='utf-8').write(b)
        print(f"   comment {c['id'][:8]} {c['createdAt']} {c['user']['name'] if c['user'] else 'bot'} chars={len(b)} at-signs={b.count('@')} mention-nodes={mention} heads={heads} KS={sorted(set(re.findall(r'KS-\d+', b)))} PRs={sorted(set(re.findall(r'#\d{3,4}', b)))}{flag}")
S = '''query($q:String!){ issues(filter:{team:{key:{eq:"KS"}}, or:[{title:{containsIgnoreCase:$q}},{description:{containsIgnoreCase:$q}}]}, includeArchived:true, first:40){ nodes{ identifier title state{name} archivedAt } } }'''
print('\nboard search by symbol/path (title OR description, includeArchived):')
for q in ['check-environment', 'run-code-guards', 'HOMED_ELSEWHERE', 'ServerAliveInterval', 'rc 141', 'idle SSH', 'TOTAL_LEGS', 'PREFLIGHT INCOMPLETE', 'PREFLIGHT_STRICT_LEGS', 'lockfile-cleanroom', 'CHECKED[*]', 'Homebrew', 'secuura/shared', 'preflight_deps', 'run_code_guards', 'check-akto-container-names', 'start-environment.sh', 'docker info', 'step header', 'denominator', 'Nothing failed', 'leg 15', 'packages/shared is not built', 'manifest_readers_agree', 'check-npm-audit', 'Playwright suite', 'test:unit', 'run-shell-suites']:
    r = gql(S, {'q': q})['issues']['nodes']
    print(f"  search {q!r}: {len(r)} -> {[(x['identifier'], x['state']['name'], 'A' if x['archivedAt'] else '') for x in r]}")
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
