#!/usr/bin/env python3
"""api_read.py — READ-ONLY GitHub GETs + Linear queries for the #1023 (KS-1207) drafter. Keys by NAME (GH_TOKEN, LINEAR_API_KEY) from the Secuura .env, never printed.
GitHub: PR 1023 (head sha, base, state, title, body), compare develop...head (merge_base, ahead, behind, files), commits (messages), and a closing-phrase scan of
title / body / commit messages with planted controls. Linear: KS-1207 (state, branchName, attachments linkKind, comments incl. 1c90d0fc), attachmentsForURL pull/1023,
controls pull/1019 and pull/99999. Raw JSON under gh/ and linear/."""
import json, re, os, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; G = os.path.dirname(os.path.abspath(__file__))
K = {}
for line in open(ENV, encoding='utf-8'):
    for n in ('GH_TOKEN', 'LINEAR_API_KEY'):
        if line.startswith(n + '='): K[n] = line.split('=', 1)[1].strip().strip('"').strip("'")
print('keys set:', {n: bool(K.get(n)) for n in ('GH_TOKEN', 'LINEAR_API_KEY')}, '| read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
def gh(p):
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura' + p, headers={'Authorization': 'Bearer ' + K['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSE = re.compile(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?|closing|fixing|resolving|completing)\b[:\s]+(KS-\d+|#\d+)')
ctl = {x: bool(CLOSE.search(x)) for x in ('Closes KS-1207', 'fixes #12', 'Refs KS-1207', 'the fix for KS-1207 is here')}
print('closing-phrase regex controls', ctl); assert ctl == {'Closes KS-1207': True, 'fixes #12': True, 'Refs KS-1207': False, 'the fix for KS-1207 is here': False}
pr = gh('/pulls/1023'); json.dump(pr, open(G + '/gh/pr1023.json', 'w'), indent=1)
print('PR 1023 state', pr['state'], 'merged', pr['merged'], 'head', pr['head']['sha'], pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'][:9], '| title', repr(pr['title']))
print('   title closing phrases', CLOSE.findall(pr['title']), '| body closing phrases', CLOSE.findall(pr['body'] or ''), '| body KS ids', sorted(set(re.findall(r'KS-\d+', pr['body'] or ''))), '| body chars', len(pr['body'] or ''))
c = gh('/compare/develop...' + pr['head']['sha']); print('compare develop...head merge_base', c['merge_base_commit']['sha'], 'ahead', c['ahead_by'], 'behind', c['behind_by'], 'files', [(f['filename'].split('/')[-1], f['sha'][:9], f['additions'], f['deletions']) for f in c.get('files') or []])
cm = gh('/pulls/1023/commits'); print('commits', len(cm))
for x in cm: print('   ', x['sha'][:9], [p['sha'][:9] for p in x['parents']], repr(x['commit']['message'].split('\n')[0][:100]), '| closing', CLOSE.findall(x['commit']['message']))
L = K['LINEAR_API_KEY']
def gql(q, v): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': L, 'Content-Type': 'application/json'}), timeout=60))
d = gql('''query($id:String!){ issue(id:$id){ identifier title state{name type} priority branchName attachments{nodes{url metadata createdAt}} comments(first:50){nodes{id createdAt body}} } }''', {'id': 'KS-1207'})
i = d['data']['issue']; json.dump(i, open(G + '/linear/KS-1207.json', 'w'), indent=1, ensure_ascii=False)
print('KS-1207 state', i['state'], 'prio', i['priority'], 'branch', i['branchName'], '| title', repr(i['title'][:120]))
for a in i['attachments']['nodes']: print('   attachment', a['url'], 'linkKind', (a.get('metadata') or {}).get('linkKind'), a['createdAt'])
for cmt in sorted(i['comments']['nodes'], key=lambda z: z['createdAt']): print('   comment', cmt['id'][:8], cmt['createdAt'], 'chars', len(cmt['body']), '| 1c90d0fc' if cmt['id'].startswith('1c90d0fc') else '', '| first line', repr(cmt['body'].split('\n')[0][:140]))
for u in ('1023', '1019', '99999'):
    d = gql('''query($u:String!){ attachmentsForURL(url:$u){ nodes{ metadata issue{ identifier state{name} } } } }''', {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/' + u})
    ns = d['data']['attachmentsForURL']['nodes']; print('attachmentsForURL pull/' + u, len(ns), [(a['issue']['identifier'], a['issue']['state']['name'], (a.get('metadata') or {}).get('linkKind')) for a in ns])
