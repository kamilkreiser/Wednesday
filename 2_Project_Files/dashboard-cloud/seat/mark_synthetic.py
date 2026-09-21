#!/usr/bin/env python3
"""mark_synthetic.py — Phase 3: mark the probe/test rows on the live board with the clear flag `synthetic=true` so both live
pages HIDE them (Kam 12:48: "I can see there's a lot of secure synthetic cards"). NOTHING IS DELETED — the rows stay, the seats
still read them, and the flag is a MERGE on the entity (idempotent: a row already flagged is skipped).

HOW A ROW IS CLASSIFIED (never a guess on a real row):
  * by ID pattern (clear metadata, every partition): local-*, live-*, probe-*, p3-*, p3l-*, kam-local-*, phase2-livetest*,
    live-card-*, local-card*, and the one Phase-2 Datasec test row bf-8897ef1d40d1* ("SYNTHETIC refused row", Phase 2 report);
  * by TEXT, for WED / Secuura / ALL rows only (decrypted with the WEDNESDAY seat key, text never printed): a message whose
    text starts with "SYNTHETIC" or "[PHASE2-TEST]", a card whose title starts with "SYNTHETIC".
  * Datasec rows: ID pattern ONLY — their text is never decrypted here. Unmatched Datasec rows are counted as "left alone".
Usage: mark_synthetic.py [--dry-run] [--tables messages,cards]   (AzureCliCredential; AZURE_CONFIG_DIR as the launcher sets it)
"""
import argparse, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envelope, seat_common as sc
from azure.identity import AzureCliCredential
from azure.data.tables import TableServiceClient, UpdateMode

CRED = "/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"
ID_PAT = re.compile(r"^(local-|live-|probe-|p3-|p3l-|kam-local-|phase2-livetest|live-card-|local-card|bf-8897ef1d40d1)")
ENV_KEYS = ("scheme", "kid", "iv", "wrapped_key", "ciphertext", "wrapped_keys")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--tables", default="messages,cards")
    a = ap.parse_args()
    ids = sc.load_ids(); wed = envelope.load_private(os.path.join(CRED, "wednesday-seat.pem"))
    svc = TableServiceClient(endpoint=f"https://{ids['STORAGE']}.table.core.windows.net", credential=AzureCliCredential())
    grand = {}
    for tname in a.tables.split(","):
        t = svc.get_table_client(tname); cnt = collections.Counter(); todo = []; reasons = collections.Counter()
        for e in t.list_entities(results_per_page=1000):
            c = e["PartitionKey"]; kind = e.get("kind", tname); cnt[(c, "rows")] += 1
            if e.get("synthetic") is True: cnt[(c, "already marked")] += 1; continue
            why = None
            if ID_PAT.match(str(e.get("id", ""))): why = "id pattern"
            elif c in ("WED", "Secuura", "ALL"):
                try:
                    txt = envelope.decrypt_text(wed, {k: e[k] for k in ENV_KEYS if k in e}, {"client": c, "kind": kind, "id": e.get("id"), "ts": e.get("ts")})
                    if kind == "card":
                        try: title = str(json.loads(txt).get("title", ""))
                        except Exception: title = ""
                        if title.startswith("SYNTHETIC"): why = "card title SYNTHETIC"
                    elif txt.startswith("SYNTHETIC") or txt.startswith("[PHASE2-TEST]"): why = "text SYNTHETIC/[PHASE2-TEST]"
                except Exception as ex:
                    cnt[(c, f"unreadable by wednesday seat ({type(ex).__name__})")] += 1
            else:
                pass   # Datasec: id pattern only (text never read)
            if why: todo.append((c, e["RowKey"], why)); cnt[(c, "to mark")] += 1; reasons[(c, why)] += 1
            else: cnt[(c, "left alone (real)")] += 1
        print(f"\n== {tname}")
        for (c, k), n in sorted(cnt.items()): print(f"   {c:8} {k:44} {n}")
        for (c, w), n in sorted(reasons.items()): print(f"   {c:8}   reason: {w:36} {n}")
        if a.dry_run:
            for c, rk, why in todo:
                if c == "Datasec": print(f"   Datasec would mark {rk}  ({why})")
            grand[tname] = {"to_mark": len(todo)}; continue
        done = collections.Counter()
        for c, rk, why in todo:
            t.update_entity({"PartitionKey": c, "RowKey": rk, "synthetic": True}, mode=UpdateMode.MERGE); done[c] += 1
        after = collections.Counter((e["PartitionKey"], "synthetic") for e in t.list_entities(select=["PartitionKey", "synthetic"]) if e.get("synthetic") is True)
        print(f"   marked: {dict(done)}   after re-scan synthetic per partition: {dict((c, n) for (c, _), n in after.items())}")
        grand[tname] = {"marked": sum(done.values()), "after_synthetic": dict((c, n) for (c, _), n in after.items())}
    print("\n== summary", json.dumps(grand))

if __name__ == "__main__":
    sys.exit(main())
