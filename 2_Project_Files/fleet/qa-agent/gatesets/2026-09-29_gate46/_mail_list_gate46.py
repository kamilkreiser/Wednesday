#!/usr/bin/env python3
"""_mail_list_gate46.py — ONE read-only AgentMail listing of wednesday-agent@ (GET messages?limit=100; touches NO seen-state), printing messages whose
subject names #1348, KS-1054, Seat B 45th / 46th or gate45 / gate46. Used ONLY to find the ids to capture; the key is read by name, never printed."""
import json, re, urllib.request
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=100', headers={'Authorization': 'Bearer ' + key}), timeout=60))
ms = r.get('messages', []); print('wednesday-agent@agentmail.to listed %d' % len(ms))
for m in ms:
    s = m.get('subject') or ''
    if re.search(r'1348|KS-1054|B 4[56]th|B4[56]|gate4[56]|N-1348', s): print(' ', m.get('message_id'), m.get('timestamp'), m.get('from'), '|', s[:260])
