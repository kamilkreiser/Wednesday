#!/usr/bin/env python3
"""QA-DAEMON-NEXT (f) N2: `--relay-url wss://127.0.0.1:9/v1 --relay-pin xyz` starts; `invite` answers; every
`mailbox open failed` line of the log is printed (the comment at link.rs:571-574 says this run reaches
`no usable relay candidate`). Usage: python3 -B -I qa_n2.py <bin dir> <work dir (new)> <label>"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

q = Q(sys.argv[1], sys.argv[2])
label = sys.argv[3]
try:
    q.start("a", ["--relay-url", "wss://127.0.0.1:9/v1", "--relay-pin", "xyz"])
    inv = q.ctl("a", "invite", {})
    time.sleep(0.5)
    lines = [l for l in q.stderr("a").splitlines() if "mailbox open failed" in l]
    print(f"{label} | invite={json.dumps(inv)} | mailbox lines ({len(lines)}): {json.dumps(lines)}")
finally:
    print(f"{label} | left: {q.cleanup()}")
