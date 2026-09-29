#!/usr/bin/env python3
"""linear_read_gate46.py — READ-ONLY Linear GraphQL query (one `issue` query, no mutation anywhere in this file) of the Secuura board: KS-1054 —
title, state, and EVERY comment (author, createdAt, updatedAt, id, body VERBATIM, BODY_SHA256). Writes linear_gate46.md beside this script.
The #1348 RAISE comment (b82bebb3-…, gate45 checked it line by line) must be present: rc 0 only then. Comments created after round 1's head was
raised are marked `AFTER gate45` so the gate reads any round-2 text first. The Secuura LINEAR_API_KEY is read by name, never printed.
Usage: linear_read_gate46.py"""
import hashlib, json, os, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
Q = 'query($id: String!) { issue(id: $id) { identifier title url state { name } comments(first: 100) { nodes { id createdAt updatedAt body user { name } } } } }'
assert 'mutation' not in Q
GATE45_VERDICT = '2026-09-29T12:11:23'
r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': Q, 'variables': {'id': 'KS-1054'}}).encode(),
                           headers={'Authorization': key, 'Content-Type': 'application/json'})
d = json.load(urllib.request.urlopen(r, timeout=60))
if d.get('errors'): raise SystemExit('REFUSING: Linear error: %s' % d['errors'])
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
i = d['data']['issue']; cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt'])
out = ['# gate46 LINEAR READ — KS-1054, every comment VERBATIM', '',
       'Read %s by linear_read_gate46.py (GraphQL `issue` query only; no mutation). Comments oldest first. BODY_SHA256 = sha256 of the body as served.' % now, '',
       '## %s — %s' % (i['identifier'], i['title']), '- state: %s' % i['state']['name'], '- url: %s' % i['url'], '- comments: %d' % len(cs), '']
raise_c = None; after = 0; edited = 0
print('%s | %s | state %s | %d comment(s)' % (i['identifier'], i['title'][:90], i['state']['name'], len(cs)))
for c in cs:
    b = c['body'] or ''; a = c['createdAt'] >= GATE45_VERDICT; e = c['updatedAt'][:19] > c['createdAt'][:19] and c['updatedAt'] >= GATE45_VERDICT
    if c['id'].startswith('b82bebb3'): raise_c = c['id']
    after += a; edited += e
    tag = (' — THE #1348 RAISE COMMENT (gate45 checked it line by line)' if c['id'].startswith('b82bebb3') else '') + (' — AFTER gate45' if a else '') + (' — EDITED AFTER gate45' if e else '')
    print('   %s %s %-22s %s%s' % (c['createdAt'], c['id'][:8], (c['user'] or {}).get('name', '?')[:22], b.replace('\n', ' ')[:100], tag))
    out += ['### KS-1054 comment %s%s' % (c['id'], tag), '- createdAt: %s | updatedAt: %s' % (c['createdAt'], c['updatedAt']),
            '- author: %s' % (c['user'] or {}).get('name', '?'), '- BODY_SHA256: %s' % hashlib.sha256(b.encode('utf-8')).hexdigest(), '', '```', b, '```', '']
open(os.path.join(G, 'linear_gate46.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('LINEAR READ %s: %d comment(s) on KS-1054, raise comment %s, %d created AFTER gate45, %d edited after gate45 -> linear_gate46.md' % ('OK' if raise_c else 'RAISE COMMENT NOT FOUND', len(cs), raise_c, after, edited))
raise SystemExit(0 if raise_c else 1)
