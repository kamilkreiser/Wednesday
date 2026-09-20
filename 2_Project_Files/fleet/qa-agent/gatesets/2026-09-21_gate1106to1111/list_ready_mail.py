#!/usr/bin/env python3
"""list_ready_mail.py — read-only: list the newest messages in wednesday-agent@ (timestamp | message id | from | subject). Key by NAME from the
WEDNESDAY .env; never printed. Derived from gatesets/2026-09-20_gate1102to1104/list_ready_mail.py (which read the key from the environment)."""
import json, os, sys, urllib.request
k = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): k = line.split('=', 1)[1].split('#')[0].strip().strip('"').strip("'")
if not k:
    print("AGENTMAIL_API_KEY unset"); sys.exit(2)
base = "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages"
r = urllib.request.urlopen(urllib.request.Request(base + "?limit=60", headers={"Authorization": "Bearer " + k}), timeout=60)
d = json.load(r)
msgs = d.get("messages", d if isinstance(d, list) else [])
print("count", len(msgs))
for m in msgs:
    print(m.get("timestamp") or m.get("created_at"), "|", m.get("message_id"), "|", (m.get("from") or "")[:40], "|", m.get("subject"))
