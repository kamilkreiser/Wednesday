#!/usr/bin/env python3
"""_mail_list_gate48b.py — ONE read-only AgentMail listing of wednesday-agent@ (GET messages?limit=100; touches NO seen-state), printing messages
whose subject names Seat B 48th, #1355, KS-1378, override, route1, or gate48b. Used ONLY to find the ids to capture; the key is read by name,
never printed. Usage: _mail_list_gate48b.py"""
import json, re, urllib.request
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=100', headers={'Authorization': 'Bearer ' + key}), timeout=60))
ms = r.get('messages', []); print('wednesday-agent@agentmail.to listed %d' % len(ms))
for m in ms:
    s = m.get('subject') or ''
    if re.search(r'B 48th|B48|1355|KS-1378|override|route1|gate48b', s, re.I): print(' ', m.get('message_id'), m.get('timestamp'), m.get('from'), '|', s[:230])
