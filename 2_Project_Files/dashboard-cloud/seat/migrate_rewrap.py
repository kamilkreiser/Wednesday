#!/usr/bin/env python3
"""migrate_rewrap.py — Phase 3 migration: re-wrap EVERY existing row's data key to the full recipient set (D-2(b)).

For each row in `messages` and `cards` (every partition, paged, full scan):
  required kids = Kam's whole ring (pilot + laptop + ipad — every app/keys/kam-*-public.pub) + the partition's seat(s)
                  (WED/Secuura -> wednesday-seat, Datasec -> tuesday-seat, ALL -> both), per envelope.recipients_for.
  * already carries every required kid in `wrapped_keys`            -> SKIPPED (idempotent)
  * else: the data key is UNWRAPPED with the PILOT private key (bytes only — the prose is never decrypted here, so
    Datasec-partition rows are re-wrapped without their text ever being touched), wrapped to the missing recipients, and
    the row is MERGED with the new `wrapped_keys` JSON (the top-level kid/wrapped_key pair is kept untouched).
  * a row the pilot key cannot unwrap (kid mismatch) is COUNTED and left alone.
--dry-run plans and counts, writes nothing. --sample N re-reads N migrated rows per partition and verifies each key of the
set opens them: WED/Secuura/ALL rows by full decrypt compared to the pilot's decrypt (text never printed); Datasec rows by
DATA-KEY bytes only (no text decrypt at all). Counts and a row_key x key -> ok/fail table are printed; prose never is.

Auth: the caller's `az` login (AzureCliCredential honours AZURE_CONFIG_DIR) — Storage Table Data Contributor on the account.
Usage: migrate_rewrap.py [--dry-run] [--tables messages,cards] [--sample 3] [--workers 8] [--limit N]
"""
import argparse, json, os, sys, time, collections, random, threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envelope, seat_common as sc
from azure.identity import AzureCliCredential
from azure.data.tables import TableServiceClient, UpdateMode

CRED = "/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"
ENV_KEYS = ("scheme", "kid", "iv", "wrapped_key", "ciphertext", "wrapped_keys")

def env_of(e: dict) -> dict: return {k: e[k] for k in ENV_KEYS if k in e}
def clear_of(e: dict) -> dict: return {"client": e["PartitionKey"], "kind": e.get("kind"), "id": e.get("id"), "ts": e.get("ts")}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--tables", default="messages,cards")
    ap.add_argument("--sample", type=int, default=0); ap.add_argument("--workers", type=int, default=8); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--pilot-key", default=os.path.join(CRED, "kam-pilot-private.pem"))
    ap.add_argument("--verify-keys", default="kam-pilot-private.pem,kam-laptop-private.pem,kam-ipad-private.pem,wednesday-seat.pem,tuesday-seat.pem")
    a = ap.parse_args()
    ids = sc.load_ids()
    pilot = envelope.load_private(a.pilot_key); pilot_kid = envelope.kid_of_private(pilot)
    ring = {c: envelope.recipients_for(c) for c in envelope.SEAT_OF_CLIENT}
    req = {c: [envelope.kid_of(pk) for _, pk in r] for c, r in ring.items()}
    print(json.dumps({"pilot_kid": pilot_kid, "required_kids_per_partition": {c: [(n, envelope.kid_of(pk)) for n, pk in r] for c, r in ring.items()}}, indent=1))
    svc = TableServiceClient(endpoint=f"https://{ids['STORAGE']}.table.core.windows.net", credential=AzureCliCredential())
    grand = {}
    for tname in a.tables.split(","):
        t = svc.get_table_client(tname)
        rows = list(t.list_entities(results_per_page=1000))
        if a.limit: rows = rows[:a.limit]
        before = collections.Counter(); todo = []
        for e in rows:
            c = e["PartitionKey"]; before[(c, "rows")] += 1
            if c not in req: before[(c, "unknown partition (left alone)")] += 1; continue
            have = set(envelope.kids_of(env_of(e)))
            missing = [k for k in req[c] if k not in have]
            if not missing: before[(c, "already complete")] += 1; continue
            if pilot_kid not in have: before[(c, "pilot cannot unwrap (left alone)")] += 1; continue
            before[(c, "to rewrap")] += 1; todo.append(e)
        print(f"\n== {tname}: {len(rows)} rows scanned")
        for (c, k), n in sorted(before.items()): print(f"   {c:8} {k:36} {n}")
        if a.dry_run: grand[tname] = {"scanned": len(rows), "to_rewrap": len(todo)}; continue
        done = collections.Counter(); errs = collections.Counter(); lock = threading.Lock(); migrated = collections.defaultdict(list)
        def work(e):
            c = e["PartitionKey"]
            try:
                dk = envelope.unwrap_data_key(pilot, env_of(e))          # bytes only
                wk = envelope.rewrap(env_of(e), dk, ring[c])
                t.update_entity({"PartitionKey": c, "RowKey": e["RowKey"], "wrapped_keys": json.dumps(wk)}, mode=UpdateMode.MERGE)
                with lock: done[(c, "rewrapped")] += 1; migrated[c].append(e["RowKey"])
            except Exception as ex:
                with lock: done[(c, "FAILED")] += 1; errs[f"{type(ex).__name__}: {str(ex)[:80]}"] += 1
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=a.workers) as ex: list(ex.map(work, todo))
        print(f"   -> {sum(done.values())} processed in {time.time()-t0:.1f}s")
        for (c, k), n in sorted(done.items()): print(f"   {c:8} {k:36} {n}")
        if errs: print("   errors:", dict(errs))
        # AFTER count: re-scan and recount completeness
        after = collections.Counter()
        for e in t.list_entities(results_per_page=1000):
            c = e["PartitionKey"]; after[(c, "rows")] += 1
            if c in req:
                have = set(envelope.kids_of(env_of(e))); after[(c, "complete" if all(k in have for k in req[c]) else "INCOMPLETE")] += 1
        print(f"   after re-scan:"); [print(f"   {c:8} {k:36} {n}") for (c, k), n in sorted(after.items())]
        grand[tname] = {"scanned": len(rows), "rewrapped": sum(n for (c, k), n in done.items() if k == "rewrapped"), "failed": sum(n for (c, k), n in done.items() if k == "FAILED"),
                        "after_complete": sum(n for (c, k), n in after.items() if k == "complete"), "after_incomplete": sum(n for (c, k), n in after.items() if k == "INCOMPLETE")}
        # SAMPLE verification with EACH key
        if a.sample:
            keys = []
            for kf in a.verify_keys.split(","):
                p = os.path.join(CRED, kf)
                if os.path.exists(p): keys.append((kf, envelope.load_private(p)))
            print(f"   sample verify ({a.sample}/partition of the rows migrated in THIS run) — keys: {[k for k, _ in keys]}")
            print(f"   {'row_key':52} " + " ".join(f"{k[:14]:>14}" for k, _ in keys))
            for c, rks in sorted(migrated.items()):
                for rk in random.sample(rks, min(a.sample, len(rks))):
                    e = t.get_entity(c, rk); env = env_of(e); clear = clear_of(e)
                    ref_dk = envelope.unwrap_data_key(pilot, env)
                    cells = []
                    for kf, pk in keys:
                        expected = envelope.kid_of_private(pk) in req[c]
                        try:
                            if c == "Datasec": ok = envelope.unwrap_data_key(pk, env) == ref_dk           # bytes only, never the text
                            else: ok = envelope.decrypt_text(pk, env, clear) == envelope.decrypt_text(pilot, env, clear)
                            cells.append("ok" if (ok and expected) else ("ok-UNEXPECTED" if ok else "fail"))
                        except Exception:
                            cells.append("n/a" if not expected else "FAIL")
                    print(f"   {c + '/' + rk[:44]:52} " + " ".join(f"{x:>14}" for x in cells))
            print("   (ok = this key opens the row; n/a = key is not a recipient of that partition, refused as it must be)")
    print("\n== summary", json.dumps(grand))
    return 0

if __name__ == "__main__":
    sys.exit(main())
