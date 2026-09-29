#!/usr/bin/env python3
"""_mail_list_gate47.py — ONE read-only AgentMail listing of wednesday-agent@ (GET messages?limit=100; touches NO seen-state), printing messages whose
subject names #1349, #1350, #1348, KS-1374, KS-1054, Seat B 46th or gate46 / gate47. Used ONLY to find the ids to capture; the key is read by name, never printed."""
import json, re, urllib.request
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=100', headers={'Authorization': 'Bearer ' + key}), timeout=60))
ms = r.get('messages', []); print('wednesday-agent@agentmail.to listed %d' % len(ms))
for m in ms:
    s = m.get('subject') or ''
    if re.search(r'1349|1350|1348|KS-1374|KS-1054|B 46th|B46|gate4[67]', s): print(' ', m.get('message_id'), m.get('timestamp'), m.get('from'), '|', s[:260])
