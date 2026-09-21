#!/usr/bin/env python3
"""post_message.py — encrypt a message to Kam's envelope key and POST it as this seat.
Usage: post_message.py --seat wednesday --client Secuura --view Secuura --text "..." [--dry-run]
The API takes the partition from the TOKEN's roles; --client outside them -> 403 (by design)."""
import argparse, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc
p = sc.common_args(argparse.ArgumentParser(description=__doc__))
p.add_argument("--text", required=True); p.add_argument("--view", default=None); p.add_argument("--role", default=None)
a = p.parse_args()
body = sc.build(a, "message", a.text, {"view": a.view or a.client, "role": a.role or a.seat})
sys.exit(sc.send(a, "/api/seat/messages", body))
