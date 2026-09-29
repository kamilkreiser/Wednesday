#!/usr/bin/env python3
"""linear_read_gate47.py — READ-ONLY Linear GraphQL queries (one `issue` query per ticket, no mutation anywhere in this file) of the Secuura board:
KS-1374 (#1349) and KS-1054 (#1350) — title, state, the DESCRIPTION VERBATIM (KS-1374's checklist lives there: the N-1347-11 item the seat's draft
would tick), and EVERY comment (author, createdAt, updatedAt, id, body VERBATIM, BODY_SHA256). Writes linear_gate47.md beside this script.
rc 0 only when ALL hold: KS-1054's #1348 raise comment b82bebb3 is present (the drafted KS-1054 facts comment names it); KS-1374's description
carries an N-1347-11 checklist line and that line is UNTICKED (`- [ ]`) — the seat says it is untouched; KS-1374's dc9212b5 comment is present
(the brief: never edited again). Comments created after gate46's verdict (2026-09-29T13:26Z) are marked `AFTER gate46`, so a comment posted
before gate47 read it is visible. The Secuura LINEAR_API_KEY is read by name, never printed. Usage: linear_read_gate47.py"""
import hashlib, json, os, re, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('LINEAR_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'LINEAR_API_KEY unset'
Q = 'query($id: String!) { issue(id: $id) { identifier title url description updatedAt state { name } comments(first: 100) { nodes { id createdAt updatedAt body user { name } } } } }'
assert 'mutation' not in Q
GATE46_VERDICT = '2026-09-29T13:26:00'
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# gate47 LINEAR READ — KS-1374 and KS-1054, description and every comment VERBATIM', '',
       'Read %s by linear_read_gate47.py (GraphQL `issue` query only; no mutation). Comments oldest first. BODY_SHA256 = sha256 of the body as served.' % now, '']
bad = []; summ = []
for ident in ('KS-1374', 'KS-1054'):
    r = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': Q, 'variables': {'id': ident}}).encode(),
                               headers={'Authorization': key, 'Content-Type': 'application/json'})
    d = json.load(urllib.request.urlopen(r, timeout=60))
    if d.get('errors'): raise SystemExit('REFUSING: Linear error on %s: %s' % (ident, d['errors']))
    i = d['data']['issue']; cs = sorted(i['comments']['nodes'], key=lambda c: c['createdAt']); desc = i.get('description') or ''
    out += ['## %s — %s' % (i['identifier'], i['title']), '- state: %s' % i['state']['name'], '- url: %s' % i['url'], '- issue updatedAt: %s' % i['updatedAt'],
            '- comments: %d' % len(cs), '- DESCRIPTION_SHA256: %s' % hashlib.sha256(desc.encode('utf-8')).hexdigest(), '', '### %s DESCRIPTION (verbatim)' % ident, '', '```', desc, '```', '']
    print('%s | %s | state %s | %d comment(s) | description %d chars' % (i['identifier'], i['title'][:90], i['state']['name'], len(cs), len(desc)))
    after = 0; found = {}
    for c in cs:
        b = c['body'] or ''; a = c['createdAt'] >= GATE46_VERDICT; e = c['updatedAt'][:19] > c['createdAt'][:19] and c['updatedAt'] >= GATE46_VERDICT
        for pre in ('b82bebb3', 'dc9212b5'):
            if c['id'].startswith(pre): found[pre] = c['id']
        after += a
        tag = (' — THE #1348 RAISE COMMENT (the KS-1054 draft names it)' if c['id'].startswith('b82bebb3') else '') + \
              (' — dc9212b5 (the brief: never edit again)' if c['id'].startswith('dc9212b5') else '') + (' — AFTER gate46' if a else '') + (' — EDITED AFTER gate46' if e else '')
        print('   %s %s %-22s %s%s' % (c['createdAt'], c['id'][:8], (c['user'] or {}).get('name', '?')[:22], b.replace('\n', ' ')[:100], tag))
        out += ['### %s comment %s%s' % (ident, c['id'], tag), '- createdAt: %s | updatedAt: %s' % (c['createdAt'], c['updatedAt']),
                '- author: %s' % (c['user'] or {}).get('name', '?'), '- BODY_SHA256: %s' % hashlib.sha256(b.encode('utf-8')).hexdigest(), '', '```', b, '```', '']
    if ident == 'KS-1054':
        if 'b82bebb3' not in found: bad.append('KS-1054: the #1348 raise comment b82bebb3 is NOT present')
        summ.append('KS-1054 %s, %d comment(s), raise comment %s, %d created AFTER gate46' % (i['state']['name'], len(cs), found.get('b82bebb3'), after))
    else:
        lines = [l for l in desc.splitlines() if 'N-1347-11' in l]
        cb = [l for l in lines if re.match(r'^\s*[-*]\s*\[[ xX]\]', l)]
        unt = [l for l in cb if re.match(r'^\s*[-*]\s*\[ \]', l)]
        print('   KS-1374 description lines naming N-1347-11: %d | checklist line(s): %d | UNTICKED: %d' % (len(lines), len(cb), len(unt)))
        for l in cb: print('     %s' % l.strip()[:200])
        if not cb: bad.append('KS-1374: no checklist line names N-1347-11 in the description')
        elif len(unt) != len(cb): bad.append('KS-1374: the N-1347-11 checklist line is TICKED already (the seat says untouched)')
        if 'dc9212b5' not in found: bad.append('KS-1374: comment dc9212b5 is NOT present')
        summ.append('KS-1374 %s, %d comment(s), N-1347-11 checklist line(s) %d (unticked %d), dc9212b5 %s, %d created AFTER gate46' % (i['state']['name'], len(cs), len(cb), len(unt), found.get('dc9212b5'), after))
open(os.path.join(G, 'linear_gate47.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('LINEAR READ %s: %s -> linear_gate47.md' % ('OK' if not bad else 'FAILED', ' | '.join(summ)))
raise SystemExit(1 if bad else 0)
