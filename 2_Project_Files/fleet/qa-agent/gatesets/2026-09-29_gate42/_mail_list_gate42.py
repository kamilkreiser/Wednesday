#!/usr/bin/env python3
"""_mail_list_gate42.py — ONE read-only AgentMail API listing of wednesday-agent@ (GET messages?limit=100; touches NO seen-state), printing only
messages whose subject names PR #1339 (id, timestamp, from, subject). Used ONLY to find the round-2 READY mail's id; the key is read by name, never printed."""
import json, urllib.request
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=100', headers={'Authorization': 'Bearer ' + key}), timeout=60))
ms = r.get('messages', [])
print('listed %d messages' % len(ms))
for m in ms:
    s = m.get('subject') or ''
    if '1339' in s or 'B 44th' in s or 'B44' in s: print(m.get('message_id'), m.get('timestamp'), m.get('from'), '|', s)
