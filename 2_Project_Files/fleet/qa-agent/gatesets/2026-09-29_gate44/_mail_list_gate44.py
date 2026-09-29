#!/usr/bin/env python3
"""_mail_list_gate44.py — ONE read-only AgentMail listing of wednesday-agent@ (GET messages?limit=100; touches NO seen-state), printing messages whose
subject names any of #1346-#1347, their keys, or Seat B 45th. Used ONLY to find the ids to capture; the key is read by name, never printed."""
import json, re, urllib.request
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=100', headers={'Authorization': 'Bearer ' + key}), timeout=60))
ms = r.get('messages', []); print('wednesday-agent@agentmail.to listed %d' % len(ms))
for m in ms:
    s = m.get('subject') or ''
    if re.search(r'134[67]|KS-1054|KS-1374|B 45th|B45|gate44|N-1332-5', s): print(' ', m.get('message_id'), m.get('timestamp'), m.get('from'), '|', s[:260])
