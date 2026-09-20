#!/usr/bin/env python3
"""list_ready_mail.py — read-only listing of wednesday-agent@ mails from secuura-blockchain@ since 2026-09-20T04:00Z (subject, ts, id). Prints no body, no key."""
import json, urllib.request
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
j = json.load(urllib.request.urlopen(urllib.request.Request(base + '?limit=50', headers=H), timeout=60))
for m in j.get('messages', []):
    if 'secuura-blockchain@' in str(m.get('from')) and (m.get('timestamp') or '') >= '2026-09-20T04:00':
        print(m.get('timestamp'), '|', m.get('subject'), '|', m.get('message_id'))
