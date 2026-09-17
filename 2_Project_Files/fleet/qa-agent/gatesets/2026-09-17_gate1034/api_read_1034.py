#!/usr/bin/env python3
"""api_read_1034.py — READ-ONLY GitHub GETs, Linear queries and AgentMail GETs for the #1034 (KS-1215) TIER 1 drafter. Keys by NAME
(GH_TOKEN, LINEAR_API_KEY from the Secuura .env; AGENTMAIL_API_KEY from Wednesday's .env); never printed. GitHub: GET only. Linear: query only.
AgentMail: GET only (list + get of wednesday-agent@ messages whose subject names KS-1215, and coagent@'s). Raw JSON under out/gh, out/linear, out/mail."""
import json, os, re, sys, time, urllib.request, urllib.error, urllib.parse, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1034'
K = {}
for env, names in (('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', ('GH_TOKEN', 'LINEAR_API_KEY')), ('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', ('AGENTMAIL_API_KEY',))):
    for line in open(env, encoding='utf-8'):
        for n in names:
            if line.startswith(n + '='): K[n] = line.split('=', 1)[1].strip().strip('"').strip("'")
def now(): return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
print('api_read_1034', now(), '| keys set:', {n: bool(K.get(n)) for n in ('GH_TOKEN', 'LINEAR_API_KEY', 'AGENTMAIL_API_KEY')})
assert all(K.get(n) for n in ('GH_TOKEN', 'LINEAR_API_KEY', 'AGENTMAIL_API_KEY'))
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def gh(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + K['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}), timeout=60))
def save(sub, n, o): open(os.path.join(G, 'out', sub, n), 'w', encoding='utf-8').write(json.dumps(o, indent=1, ensure_ascii=False) if not isinstance(o, str) else o)
H = 'fd81a75f0688f6cbe1e5f79b061bb1369c88f477'; N = '1034'
CLOSE = re.compile(r'(?i)\b(?:close[sd]?|closing|fix(?:e[sd]|ing)?|resolve[sd]?|resolving|complete[sd]?|completing|implement(?:s|ed|ing)?)\s*:?\s+(?:#\d+|[A-Z]{2,}-\d+|https?://\S*(?:linear\.app|github\.com)\S*)')
ctl = [len(CLOSE.findall(x)) for x in ('Fixes KS-1215', 'closes #1034', 'Resolves: KS-1215', 'Refs KS-1215', 'the fix for KS-1215 is here')]
print('closing-phrase regex controls', ctl); assert ctl == [1, 1, 1, 0, 0]
MODE = sys.argv[1] if len(sys.argv) > 1 else 'all'
if MODE in ('all', 'gh'):
    pr = gh('/pulls/' + N)
    for _ in range(4):
        if pr.get('mergeable') is not None: break
        time.sleep(3); pr = gh('/pulls/' + N)
    save('gh', 'pr1034.json', pr); body = pr.get('body') or ''; save('gh', 'pr1034_body.md', body)
    print('PR #1034', pr['state'], 'draft', pr['draft'], 'merged', pr['merged'], '| head', pr['head']['sha'], '== pin', pr['head']['sha'] == H, pr['head']['ref'], '| base', pr['base']['ref'], pr['base']['sha'])
    print('  title:', repr(pr['title']), '| title closing', CLOSE.findall(pr['title']), '| mergeable', pr.get('mergeable'), pr.get('mergeable_state'), '| commits', pr['commits'], 'files', pr['changed_files'], '+%d -%d' % (pr['additions'], pr['deletions']))
    print('  body chars', len(body), 'at-signs', body.count('@'), 'closing', CLOSE.findall(body), 'Refs KS-1215', body.count('Refs KS-1215'), 'Test Evidence', body.count('Test Evidence'), 'KS ids', {k: len(re.findall(re.escape(k) + r'(?![0-9])', body)) for k in sorted(set(re.findall(r'KS-[0-9]+', body)))})
    files = gh('/pulls/' + N + '/files?per_page=100'); save('gh', 'pr1034_files.json', files); mine = set()
    for f in files: mine.add(f['filename']); print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'], f['filename'])
    for c in gh('/pulls/' + N + '/commits?per_page=100'):
        print('  commit', c['sha'], 'parents', [p['sha'][:9] for p in c['parents']], 'closing', CLOSE.findall(c['commit']['message']), 'KS ids', sorted(set(re.findall(r'KS-[0-9]+', c['commit']['message']))), '|', c['commit']['message'].split('\n')[0][:110])
    c = gh('/compare/develop...' + H); save('gh', 'compare_develop_head.json', c)
    print('  compare develop...head: merge_base %s status %s ahead %d behind %d files %d %s' % (c['merge_base_commit']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(c.get('files') or []), [(f['filename'].split('/')[-1], f['sha'][:9]) for f in c.get('files') or []]))
    print('  reviews', len(gh('/pulls/' + N + '/reviews')), '| review comments', len(gh('/pulls/' + N + '/comments')), '| issue comments', len(gh('/issues/' + N + '/comments')))
    dev = gh('/branches/develop')['commit']['sha']; print('  develop (branches API)', dev)
    opn = gh('/pulls?state=open&per_page=100'); print('  open PRs:', len(opn), sorted(p['number'] for p in opn))
    D = 'Blockchain/Dev/'
    for p in sorted(opn, key=lambda p: p['number']):
        if p['number'] == int(N): continue
        fs = {f['filename'] for f in gh('/pulls/%d/files?per_page=100' % p['number'])}
        gw = sorted(x for x in fs if x.startswith(D + 'services/api-gateway/') or x.startswith(D + 'packages/shared/src/'))
        if gw or (fs & mine): print('  open #%d head %s files %d | shared-with-1034 %s | api-gateway/shared-src files %d %s | %s' % (p['number'], p['head']['sha'][:9], len(fs), sorted(fs & mine), len(gw), gw[:6], p['title'][:70]))
if MODE in ('all', 'linear'):
    L = K['LINEAR_API_KEY']
    def gql(q, v): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': q, 'variables': v}).encode(), headers={'Authorization': L, 'Content-Type': 'application/json'}), timeout=60))
    Q = '''query($id:String!){ issue(id:$id){ identifier title state{name type} priority branchName description updatedAt relations{nodes{type relatedIssue{identifier}}} attachments{nodes{url metadata createdAt}} comments(first:100){nodes{id createdAt body user{name} botActor{name}}} history(first:30){nodes{createdAt fromState{name} toState{name} actor{name}}} } }'''
    print('linear read at', now())
    for n in ('KS-1215', 'KS-744', 'KS-1207'):
        d = gql(Q, {'id': n})
        if 'errors' in d: print(n, 'ERRORS', d['errors']); continue
        i = d['data']['issue']; save('linear', n + '.json', i)
        cs = sorted(i['comments']['nodes'], key=lambda z: z['createdAt'])
        print(f"{n}: state={i['state']['name']}/{i['state']['type']} prio={i['priority']} comments={len(cs)} branch={i['branchName']!r} relations={[r['type']+':'+r['relatedIssue']['identifier'] for r in i['relations']['nodes']]} title={i['title'][:130]!r}")
        for a in i['attachments']['nodes']: print(f"   attachment {a['url']} linkKind={(a.get('metadata') or {}).get('linkKind')!r} created={a['createdAt']}")
        for h in i['history']['nodes']:
            if h.get('toState'): print(f"   history {h['createdAt']} {(h.get('fromState') or {}).get('name')} -> {h['toState']['name']} actor={(h.get('actor') or {}).get('name')}")
        with open(f'{G}/out/linear/{n}.comments.md', 'w', encoding='utf-8') as fh:
            fh.write('# DESCRIPTION\n' + (i.get('description') or '') + '\n')
            for cm in cs:
                who = (cm.get('user') or {}).get('name') or (cm.get('botActor') or {}).get('name')
                fh.write(f"\n\n# COMMENT {cm['id']} {cm['createdAt']} {who}\n{cm['body']}\n")
                print(f"   comment {cm['id'][:8]} {cm['createdAt']} {who} chars={len(cm['body'])} closing={CLOSE.findall(cm['body'])} first={cm['body'][:90]!r}")
    AQ = '''query($u:String!){ attachmentsForURL(url:$u){ nodes{ url metadata createdAt issue{ identifier state{name} } } } }'''
    for u in ('1034', '1028', '99999'):
        d = gql(AQ, {'u': 'https://github.com/Secuura/Distributed_Secuura/pull/' + u}); ns = d['data']['attachmentsForURL']['nodes']
        print(f"attachmentsForURL pull/{u}: {len(ns)} {[(a['issue']['identifier'], a['issue']['state']['name'], (a.get('metadata') or {}).get('linkKind')) for a in ns]}")
if MODE in ('all', 'mail'):
    A = 'https://api.agentmail.to/v0/inboxes/'
    def am(p): return json.load(urllib.request.urlopen(urllib.request.Request(A + p, headers={'Authorization': 'Bearer ' + K['AGENTMAIL_API_KEY']}), timeout=60))
    for inbox in ('wednesday-agent@agentmail.to', 'coagent@agentmail.to'):
        got = []; tok = None
        for _ in range(8):
            q = {'limit': 100}
            if tok: q['page_token'] = tok
            d = am(urllib.parse.quote(inbox) + '/messages?' + urllib.parse.urlencode(q))
            got += d.get('messages', []); tok = d.get('next_page_token')
            if not tok: break
        hits = [m for m in got if 'KS-1215' in (m.get('subject') or '') or '#1034' in (m.get('subject') or '')]
        print('mail', inbox, 'listed', len(got), '| subject names KS-1215 or #1034:', len(hits), '| control subject names KS-1194:', sum('KS-1194' in (m.get('subject') or '') for m in got))
        for m in sorted(hits, key=lambda m: m.get('timestamp') or ''):
            full = am(urllib.parse.quote(inbox) + '/messages/' + urllib.parse.quote(m['message_id']))
            txt = full.get('text') or full.get('extracted_text') or ''
            fn = re.sub(r'[^A-Za-z0-9]+', '_', (m.get('timestamp') or '')[:19] + '_' + (m.get('subject') or ''))[:120] + '.md'
            save('mail', fn, 'SUBJECT: %s\nTS: %s\nFROM: %s\nTO: %s\nLABELS: %s\n\n%s' % (full.get('subject'), full.get('timestamp'), full.get('from'), full.get('to'), full.get('labels'), txt))
            print('   ', m.get('timestamp'), '|', m.get('from'), '->', m.get('to'), '|', m.get('subject'), '| chars', len(txt), '->', fn)
print('api_read_1034 end', now())
