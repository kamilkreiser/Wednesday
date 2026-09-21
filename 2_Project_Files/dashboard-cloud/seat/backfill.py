#!/usr/bin/env python3
"""backfill.py — Phase 2: copy the LOCAL chat streams + decision cards onto the live board, encrypted at write.

WHO POSTS WHAT (Wednesday's seat holds Client.Secuura + Client.WED only — Kam's 2026-09-08 split, enforced by the API):
  chat_wednesday.json   role=wednesday        -> partition = entry.project (Secuura|WED); view=wednesday
  chat_kam.json         role=kam              -> view=wednesday -> WED;  view absent -> WED with view=both;
                                                 view=tuesday  -> SKIPPED (Tuesday's partition; counted, left for her)
  chat_legacy.json      pre-split, frozen     -> role=kam -> WED (view=both); role=wednesday: project Datasec or a MBP seat
                                                 -> SKIPPED (Tuesday's); project Secuura -> Secuura; else -> WED
  chat_tuesday.json     Tuesday's stream      -> NEVER posted here; counted only
  decisions.json        cards                 -> client from client_project prefix; Datasec -> SKIPPED (counted)

EVERY row keeps its original timestamp: `ts` = the entry's ts converted to UTC (RowKey order == local order), `src_ts` = the
original string, `backfill=true`. Ids are deterministic (seat_common.row_id) so a re-run posts NOTHING NEW: the API answers
200 duplicate for a message it already holds, and updates a card in place. Counts are printed; prose never is.

Usage: backfill.py [--dry-run] [--only wednesday,kam,legacy,cards] [--limit N] [--workers 6] [--rate 12] [--base URL]
"""
import argparse, json, os, sys, time, threading, collections
from concurrent.futures import ThreadPoolExecutor
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc, envelope, post_card

ROOT = "/Volumes/DevMASTER/WEDNESDAY"
DATA = os.path.join(ROOT, "0_Brain", "dashboard", "data")

def load(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p): return []
    d = json.load(open(p, encoding="utf-8"))
    return [e for e in d if isinstance(e, dict)] if isinstance(d, list) else []

class Bucket:
    """Token bucket: at most `rate` requests per second across all workers."""
    def __init__(self, rate): self.rate = rate; self.lock = threading.Lock(); self.t = time.monotonic()
    def take(self):
        with self.lock:
            now = time.monotonic(); wait = self.t - now
            self.t = max(now, self.t) + 1.0 / self.rate
        if wait > 0: time.sleep(wait)

def plan_messages(only):
    """Yield (stream, client, view, role, ts_local, text) for every row Wednesday's seat may post; count the rest."""
    rows, skipped = [], collections.Counter()
    if "wednesday" in only:
        for e in load("chat_wednesday.json"):
            proj = (e.get("project") or "WED").strip()
            if proj == "Datasec": skipped["chat_wednesday.json: Datasec-tagged (Tuesday's partition)"] += 1; continue
            if proj not in ("Secuura", "WED"): proj = "WED"
            rows.append(("chat_wednesday.json", proj, "wednesday", "wednesday", e.get("ts", ""), e.get("text", "")))
    if "kam" in only:
        for e in load("chat_kam.json"):
            view = e.get("view")                                   # handled EXPLICITLY: the field says which tab he typed in
            if view == "tuesday": skipped["chat_kam.json: view=tuesday (Tuesday's partition)"] += 1; continue
            if e.get("attachments"): skipped["chat_kam.json: attachments not synced (Studio-local uploads; text posted)"] += 1
            rows.append(("chat_kam.json", "WED", "wednesday" if view == "wednesday" else "both", "kam", e.get("ts", ""), e.get("text", "")))
    if "legacy" in only:
        for e in load("chat_legacy.json"):
            if e.get("role") == "kam":
                rows.append(("chat_legacy.json", "WED", "both", "kam", e.get("ts", ""), e.get("text", ""))); continue
            proj = (e.get("project") or "").strip(); seat = e.get("seat") or ""
            if proj == "Datasec" or "MBP" in seat: skipped["chat_legacy.json: Datasec/MBP (Tuesday's partition)"] += 1; continue
            rows.append(("chat_legacy.json", "Secuura" if proj == "Secuura" else "WED", "wednesday", "wednesday", e.get("ts", ""), e.get("text", "")))
    skipped["chat_tuesday.json: Tuesday's whole stream (never posted by Wednesday)"] = len(load("chat_tuesday.json"))
    return rows, skipped

def plan_cards(only):
    cards, skipped = [], collections.Counter()
    if "cards" in only:
        for c in load("decisions.json"):
            client = post_card.client_of(c.get("client_project", ""))
            if client == "Datasec": skipped["decisions.json: Datasec cards (Tuesday's partition)"] += 1; continue
            cards.append((client, c))
    return cards, skipped

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--only", default="wednesday,kam,legacy,cards")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--workers", type=int, default=6); ap.add_argument("--rate", type=float, default=12)
    ap.add_argument("--seat", default="wednesday"); ap.add_argument("--base", default=None)
    ap.add_argument("--cert-dir", default=os.path.join(ROOT, "4_Credentials", "dashboard-cloud"))
    a = ap.parse_args()
    ids = sc.load_ids(); only = set(a.only.split(","))
    base = a.base or f"https://{ids['WEBAPP']}.azurewebsites.net"
    pub = envelope.load_public(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "keys", "kam-pilot-public.pub"))
    msgs, sk1 = plan_messages(only); cards, sk2 = plan_cards(only)
    if a.limit: msgs, cards = msgs[:a.limit], cards[:a.limit]
    plan = collections.Counter((s, c) for s, c, *_ in msgs)
    print(json.dumps({"plan_messages": {f"{s} -> {c}": n for (s, c), n in sorted(plan.items())},
                      "plan_cards": dict(collections.Counter(c for c, _ in cards)), "skipped": {**sk1, **sk2}}, indent=1))
    if a.dry_run: return 0
    class A: pass
    tok_args = A(); tok_args.seat = a.seat; tok_args.cert_dir = a.cert_dir; tok_args.tenant = ids["TENANT_ID"]; tok_args.api_appid = ids["API_APPID"]
    tok = sc.get_token(tok_args, ids)
    sess = requests.Session(); sess.headers["Authorization"] = f"Bearer {tok}"
    bucket = Bucket(a.rate); lock = threading.Lock()
    out = collections.Counter(); errs = collections.Counter()
    def post(path, body, label):
        bucket.take()
        try: r = sess.post(base + path, json=body, timeout=40)
        except Exception as e:
            with lock: out[f"{label} error"] += 1; errs[type(e).__name__] += 1
            return
        with lock:
            if r.status_code == 201: out[f"{label} posted (201)"] += 1
            elif r.status_code == 200: out[f"{label} already there (200 duplicate/updated)"] += 1
            else: out[f"{label} refused {r.status_code}"] += 1; errs[r.text[:80]] += 1
    def do_msg(m):
        stream, client, view, role, ts_local, text = m
        try: ts = sc.to_utc_z(ts_local)
        except Exception:
            with lock: out[f"{stream} unparseable ts (skipped)"] += 1
            return
        rid = sc.row_id(stream, ts_local, text)
        clear = {"client": client, "kind": "message", "id": rid, "ts": ts, "view": view, "role": role, "backfill": True, "src_ts": ts_local[:40]}
        env = envelope.encrypt_text(pub, text, clear)
        if len(text) >= 8: assert text not in json.dumps(env), "plaintext leaked into envelope"
        post("/api/seat/messages", {**clear, "envelope": env}, f"{stream} -> {client}")
    def do_card(item):
        client, card = item
        prose_d, clear_x = post_card.from_store(card)
        rid = post_card.card_id(card.get("id", ""))
        try: ts = sc.to_utc_z(card["ts"]) if card.get("ts") else sc.to_utc_z(card.get("ruled_ts") or "2026-08-21T00:00:00+10:00")
        except Exception: ts = "2026-08-21T00:00:00.000Z"
        clear = {"client": client, "kind": "card", "id": rid, "ts": ts, **clear_x, "backfill": True}
        if card.get("ts"): clear["src_ts"] = str(card["ts"])[:40]     # one local card has no ts: an empty src_ts is refused (400), so omit it
        env = envelope.encrypt_text(pub, json.dumps(prose_d, ensure_ascii=False), clear)
        post("/api/seat/cards", {**clear, "envelope": env}, f"decisions.json -> {client}")
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(do_msg, msgs)); list(ex.map(do_card, cards))
    print(json.dumps({"result": dict(sorted(out.items())), "errors": dict(errs), "seconds": round(time.time() - t0, 1),
                      "messages_planned": len(msgs), "cards_planned": len(cards)}, indent=1))
    return 0 if not errs else 1

if __name__ == "__main__":
    sys.exit(main())
