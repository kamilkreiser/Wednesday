#!/usr/bin/env python3
"""post_card.py — encrypt a decision card's prose (title/bluf/options text) and POST it as this seat.
Clear fields: client, id, ts, status, option KEYS, recommended, ruled, ruled_choice, ruled_ts (the routing set, study §4.4).
A card is STATE on the live board: posting the same id again UPDATES it (200 {"updated": true}); the first post is 201.

Usage (hand-built):
  post_card.py --seat wednesday --client Secuura --title T --bluf B --option A "label" --option B "label" [--recommended A] [--dry-run]
Usage (Phase 2, from the local store — what tools/decision_queue.sh calls after every write):
  post_card.py --seat wednesday --from-store 0_Brain/dashboard/data/decisions.json --card-id <id> [--backfill]
     --client is derived from the card's client_project prefix (Secuura/… -> Secuura, Datasec/… -> Datasec, WED|Fleet -> WED);
     pass --client to override. The card's own `ts` (local) becomes src_ts; ts = its UTC form."""
import argparse, sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc

def client_of(client_project: str) -> str:
    head = (client_project or "").split("/", 1)[0].strip().lower()
    if head.startswith("secuura"): return "Secuura"
    if head.startswith("datasec"): return "Datasec"
    return "WED"                                     # WED*, Fleet*, anything general

def card_id(local_id: str) -> str:
    """Local ids are slugs; anything outside [A-Za-z0-9._-] or over 64 chars is hashed so the API accepts it."""
    if re.match(r"^[A-Za-z0-9._-]{1,64}$", local_id or ""): return local_id
    import hashlib; return "card-" + hashlib.sha256((local_id or "").encode()).hexdigest()[:20]

def from_store(card: dict) -> tuple:
    """Local decisions.json card object -> (prose dict, clear dict). Prose holds every human sentence; clear holds routing."""
    opts = [{"key": str(o.get("key", "")), "label": str(o.get("label", "")), "detail": str(o.get("detail", "") or "")}
            for o in card.get("options", []) if isinstance(o, dict)]
    prose = {"title": card.get("title", ""), "bluf": card.get("bluf", ""), "default_action": card.get("default_action", ""),
             "options": opts, "ruling_note": card.get("ruling_note") or card.get("ruling") or "",
             "withdrawn_reason": card.get("withdrawn_reason") or "", "delivered_artefact": card.get("delivered_artefact") or "",
             "local_id": card.get("id", "")}
    status = card.get("status") or "open"
    if status not in ("open", "ruled", "withdrawn"): status = "open"
    ruled_ts = card.get("ruled_ts") or card.get("withdrawn_at") or ""
    try: ruled_ts = sc.to_utc_z(ruled_ts) if ruled_ts else ""
    except Exception: ruled_ts = ""
    clear = {"option_keys": [o["key"][:32] for o in opts], "recommended": str(card.get("recommended") or "")[:32],
             "status": status, "ruled": status == "ruled", "ruled_choice": str(card.get("ruled_choice") or "")[:32],
             "ruled_ts": ruled_ts, "client_project": str(card.get("client_project") or "")[:64]}
    return prose, clear

if __name__ == "__main__":
    p = sc.common_args(argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter))
    # --client is required by common_args; relax it here because --from-store derives it
    for a in p._actions:
        if "--client" in a.option_strings: a.required = False
    p.add_argument("--title"); p.add_argument("--bluf")
    p.add_argument("--option", nargs=2, action="append", metavar=("KEY", "LABEL"))
    p.add_argument("--recommended", default=""); p.add_argument("--default-action", default="")
    p.add_argument("--status", default="open", choices=["open", "ruled", "withdrawn"]); p.add_argument("--ruled-choice", default="")
    p.add_argument("--from-store", default=None, help="path to the local decisions.json"); p.add_argument("--card-id", default=None)
    a = p.parse_args()
    if a.from_store:
        if not a.card_id: sys.exit("post_card: --from-store needs --card-id")
        store = json.load(open(a.from_store))
        card = next((c for c in store if isinstance(c, dict) and c.get("id") == a.card_id), None)
        if card is None: sys.exit(f"post_card: no card {a.card_id!r} in {a.from_store}")
        a.client = a.client or client_of(card.get("client_project", ""))
        a.id = a.id or card_id(card.get("id", ""))
        if not a.src_ts and card.get("ts"): a.src_ts = str(card["ts"])
        prose_d, clear = from_store(card)
        prose = json.dumps(prose_d, ensure_ascii=False)
    else:
        if not (a.client and a.title and a.bluf and a.option): sys.exit("post_card: need --client --title --bluf and >=1 --option (or --from-store)")
        prose = json.dumps({"title": a.title, "bluf": a.bluf, "default_action": a.default_action,
                            "options": [{"key": k, "label": l, "detail": ""} for k, l in a.option]})
        clear = {"option_keys": [k for k, _ in a.option], "recommended": a.recommended, "status": a.status,
                 "ruled": bool(a.ruled_choice), "ruled_choice": a.ruled_choice, "client_project": a.client}
    body = sc.build(a, "card", prose, clear)
    sys.exit(sc.send(a, "/api/seat/cards", body))
