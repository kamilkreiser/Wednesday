#!/usr/bin/env python3
"""linear_read_gate45.py — READ-ONLY Linear GraphQL query (one `issue` query per key, no mutation anywhere in this file) of the
Secuura board: KS-1054 and KS-1374 — title, state, and EVERY comment (author, createdAt, id, body VERBATIM, BODY_SHA256).
Writes linear_gate45.md beside this script. The Secuura LINEAR_API_KEY is read by name from the Secuura .env and never printed.
A CORRECTION comment on KS-1374 is one whose body OPENS with 'Correction' (case-insensitive); THE SECOND CORRECTION (the one gate45 checks line by line)
is comment id dc9212b5-… (https://linear.app/secuura/issue/KS-1374/…#comment-dc9212b5). rc 0 only when that id is present on KS-1374.
Usage: linear_read_gate45.py"""
import hashlib, json, os, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
Q = 'query($id: String!) { issue(id: $id) { identifier title url state { name } comments(first: 100) { nodes { id createdAt updatedAt body user { name } } } } }'
assert 'mutation' not in Q
def q(ident):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': Q, 'variables': {'id': ident}}).encode(),
                               headers={'Authorization': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# gate45 LINEAR READ — KS-1054 and KS-1374, every comment VERBATIM', '',
       'Read %s by linear_read_gate45.py (GraphQL `issue` query only; no mutation). Comments oldest first. BODY_SHA256 = sha256 of the body as served.' % now, '']
corr = 0; second = None
for ident in ('KS-1054', 'KS-1374'):
    d = q(ident)
    if d.get('errors'): raise SystemExit('REFUSING: Linear error for %s: %s' % (ident, d['errors']))
    i = d['data']['issue']; cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
    print('%s | %s | state %s | %d comment(s)' % (i['identifier'], i['title'][:90], i['state']['name'], len(cs)))
    out += ['## %s — %s' % (i['identifier'], i['title']), '- state: %s' % i['state']['name'], '- url: %s' % i['url'], '- comments: %d' % len(cs), '']
    for c in cs:
        b = c['body'] or ''; isc = ident == 'KS-1374' and (b.lstrip().lower().startswith('correction') or c['id'].startswith('dc9212b5'))
        if ident == 'KS-1374' and c['id'].startswith('dc9212b5'): second = c['id']
        if isc: corr += 1
        print('   %s %s %-22s %s%s' % (c['createdAt'], c['id'][:8], (c['user'] or {}).get('name', '?')[:22], b.replace('\n', ' ')[:110], '   <== CORRECTION' if isc else ''))
        out += ['### %s comment %s%s' % (ident, c['id'], (' — THE SECOND CORRECTION (gate45 checks every factual line)' if c['id'].startswith('dc9212b5') else ' — a CORRECTION') if isc else ''), '- createdAt: %s | updatedAt: %s' % (c['createdAt'], c['updatedAt']),
                '- author: %s' % (c['user'] or {}).get('name', '?'), '- BODY_SHA256: %s' % hashlib.sha256(b.encode('utf-8')).hexdigest(), '', '```', b, '```', '']
open(os.path.join(G, 'linear_gate45.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('LINEAR READ %s: %d CORRECTION comment(s) on KS-1374, the SECOND %s -> linear_gate45.md' % ('OK' if second else 'SECOND CORRECTION NOT FOUND', corr, second))
raise SystemExit(0 if second else 1)
