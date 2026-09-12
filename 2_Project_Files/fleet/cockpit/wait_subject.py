#!/usr/bin/env python3
"""Session-side wait for ONE mail subject in wednesday-agent@ (the watcher's mail leg
drops QA verdicts sent through Wednesday's own send path). Exits when a message whose
subject contains NEEDLE and whose timestamp is after SINCE arrives, or after 5
consecutive API failures, or after MAX_POLLS. Prints subject + timestamp only, never a body.
Usage: wait_subject.py '<needle>' '<since ISO, e.g. 2026-09-12T23:00:00Z>' [poll_s=120] [max_polls=90]
"""
import json, re, sys, time, urllib.request

needle, since = sys.argv[1], sys.argv[2]
poll = int(sys.argv[3]) if len(sys.argv) > 3 else 120
max_polls = int(sys.argv[4]) if len(sys.argv) > 4 else 90
key = None
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env'):
    m = re.match(r'\s*(?:export\s+)?AGENTMAIL_API_KEY\s*=\s*["\']?([^"\'\s]+)', line)
    if m:
        key = m.group(1)
if not key:
    print("WAIT ABORT: AGENTMAIL_API_KEY not found", flush=True)
    sys.exit(3)
url = "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages?limit=30"
fails = 0
for i in range(max_polls):
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Bearer " + key}), timeout=30))
        fails = 0
        for msg in d.get("messages", []):
            ts = msg.get("timestamp", "")
            subj = msg.get("subject", "")
            if ts > since and needle in subj:
                print(f"WAIT HIT after poll {i}: {ts} | {subj}", flush=True)
                sys.exit(0)
    except Exception as e:  # stated, never swallowed
        fails += 1
        print(f"poll {i} API error ({fails}/5): {e}", flush=True)
        if fails >= 5:
            print("WAIT ABORT: 5 consecutive API failures", flush=True)
            sys.exit(4)
    time.sleep(poll)
print(f"WAIT TIMEOUT after {max_polls} polls — no subject containing {needle!r} since {since}", flush=True)
sys.exit(5)
