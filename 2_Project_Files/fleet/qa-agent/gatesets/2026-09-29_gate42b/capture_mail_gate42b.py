#!/usr/bin/env python3
"""capture_mail_gate42b.py — the gate42b CAPTURE: four mails READ BY ID (AgentMail GET /v0/inboxes/<inbox>/messages/<id>; read-only, touches no
seen-state), each written VERBATIM with its TEXT_SHA256 into mail_gate42b_ready.md beside this script. Ids found by ONE read-only listing of
wednesday-agent@ and secuura-blockchain@ (drafter scratch mail_list_1.out). Kam's mail is the AUTHORITY the gate checks the diff against; the
READY is the author's CLAIM; the two Wednesday ANSWERs are context. The API key is read by name and never printed.
Usage: capture_mail_gate42b.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
KAM_TEXT = ('Re-date GHSA-frvp-7c67-39w9 (KS-530), GHSA-mwp4-54f8-5fhr (KS-729), GHSA-wrjc-x8rr-h8h6 and GHSA-337j-9hxr-rhxg (KS-528) to 2026-10-09. '
            'The real fixes stay on those tickets.')
MAILS = [('secuura-blockchain@agentmail.to', '<EB856837-268F-4CC7-B167-BE74B4824634@me.com>', 'KAM (the authority)', 'Audit baseline re-date'),
         ('wednesday-agent@agentmail.to', '<010001a0ebdc3e29-1652d1cb-352d-4b12-91c7-53daebd78ee1-000000@email.amazonses.com>', 'READY (the claim)', '[Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 44th): PR #1340'),
         ('wednesday-agent@agentmail.to', '<010001a0eb65cf64-4a37fa02-a76a-478d-8abc-0c28deb91669-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER on the fifth row jjmj)', '[Wednesday -> Secuura/Blockchain] ANSWER: baseline re-date (Seat B 44th) - Kam'),
         ('wednesday-agent@agentmail.to', '<010001a0eb6beab6-1e268cd2-6b7d-41c0-99a8-313e8149db04-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER on the base)', '[Wednesday -> Secuura/Blockchain] ANSWER: baseline re-date (Seat B 44th) - built')]
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
out = ['# gate42b CAPTURE — four mails read by id, VERBATIM', '',
       'Captured %s by capture_mail_gate42b.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), '',
       '#1340 is KS-530 + KS-729 + KS-528: the audit-baseline re-date of the four rows Kam named, to 2026-10-09.', '']
bad = 0
for inbox, mid, role, subj in MAILS:
    u = 'https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (inbox, urllib.parse.quote(mid, safe=''))
    m = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + key}), timeout=60))
    t = m.get('text') or m.get('extracted_text') or ''
    ok = (m.get('subject') or '').startswith(subj)
    if not ok: bad += 1
    out += ['## %s' % role, '- inbox: %s' % inbox, '- id: %s' % m.get('message_id'), '- from: %s' % m.get('from'), '- timestamp: %s' % m.get('timestamp'),
            '- subject: %s' % m.get('subject'), '- subject begins with the expected prefix: %s' % ok, '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    if role.startswith('KAM'):
        norm = ' '.join(t.split()); has = KAM_TEXT in norm
        out += ['- KAM BODY CHECK: the verbatim instruction (whitespace-normalised) is in the captured text: %s' % has, '']
        print('KAM mail from %s at %s | instruction verbatim present: %s' % (m.get('from'), m.get('timestamp'), has))
        if not has or 'kreiser.org@me.com' not in (m.get('from') or ''): bad += 1
    print('%-50s %s %s' % (role, m.get('timestamp'), 'SUBJECT OK' if ok else 'SUBJECT MISMATCH'))
open(os.path.join(G, 'mail_gate42b_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('CAPTURE %s: 4 mails, %d problem(s) -> mail_gate42b_ready.md' % ('OK' if bad == 0 else 'FAILED', bad))
raise SystemExit(1 if bad else 0)
