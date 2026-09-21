#!/usr/bin/env python3
"""post_card.py — encrypt a decision card's prose (title/bluf/options text) and POST it as this seat.
Clear fields: client, id, ts, status, option KEYS, recommended, ruled, ruled_choice (the routing set, study §4.4).
Usage: post_card.py --seat wednesday --client Secuura --title T --bluf B --option A "label" --option B "label" [--recommended A] [--dry-run]"""
import argparse, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc
p = sc.common_args(argparse.ArgumentParser(description=__doc__))
p.add_argument("--title", required=True); p.add_argument("--bluf", required=True)
p.add_argument("--option", nargs=2, action="append", metavar=("KEY", "LABEL"), required=True)
p.add_argument("--recommended", default=""); p.add_argument("--default-action", default="")
p.add_argument("--status", default="open", choices=["open", "ruled", "withdrawn"]); p.add_argument("--ruled-choice", default="")
a = p.parse_args()
prose = json.dumps({"title": a.title, "bluf": a.bluf, "default_action": a.default_action,
                    "options": [{"key": k, "label": l, "detail": ""} for k, l in a.option]})
clear = {"option_keys": [k for k, _ in a.option], "recommended": a.recommended, "status": a.status,
         "ruled": bool(a.ruled_choice), "ruled_choice": a.ruled_choice, "client_project": a.client}
body = sc.build(a, "card", prose, clear)
sys.exit(sc.send(a, "/api/seat/cards", body))
