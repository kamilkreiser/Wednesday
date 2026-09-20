import json, os, urllib.request, urllib.parse, sys
k = os.environ.get("AGENTMAIL_API_KEY", "")
if not k:
    print("AGENTMAIL_API_KEY unset"); sys.exit(2)
base = "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages"
r = urllib.request.urlopen(urllib.request.Request(base + "?limit=30", headers={"Authorization": "Bearer " + k}), timeout=60)
d = json.load(r)
msgs = d.get("messages", d if isinstance(d, list) else [])
print("count", len(msgs))
for m in msgs:
    print(m.get("timestamp") or m.get("created_at"), "|", m.get("message_id"), "|", (m.get("from") or "")[:40], "|", m.get("subject"))
