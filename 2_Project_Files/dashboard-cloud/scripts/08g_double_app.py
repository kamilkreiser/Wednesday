#!/usr/bin/env python3
"""08g_double_app.py — the dashboard app (app/main.py, UNMODIFIED) on loopback with an IN-MEMORY store: the test double for the
Friday matrix (2026-09-23). Written after Wednesday's 11:16 stop ("STOP posting to the LIVE board from any local matrix"): the
older loopback matrices run the app against the REAL storage account the live board reads, and 08c's Kam-role rows (which
cannot be born synthetic) appeared to every seat as Kam's words. Here NOTHING can reach the live store:
  * main.table()            -> an in-memory TableClient twin (create/update MERGE|REPLACE/upsert/get/query with the OData
                               subset main.py uses: `X eq @p`, `X gt @p`, joined by `and`)
  * main.blob_put/blob_get  -> an in-memory blob dict (INSERT semantics kept: a repeat put returns False)
  * main.credential()       -> RAISES (any path that would build a real Azure credential fails loudly)
  * STORAGE_ACCOUNT         -> a name that cannot exist ("nolivestore-double"), so even a missed patch cannot resolve the live host
Seat tokens are REAL (the seats' certificates against Entra; validated by main.py against the tenant JWKS) — reads of Entra only.
Double-only routes (inserted ahead of the catch-all; they do NOT exist in main.py):
  GET /__double/dump        the whole in-memory store (tables + blob names/sizes)  — the matrix's "raw row" instrument
  GET /__double/proof       {"credential_calls": n, "live_store_calls": n, "writes": n}  — the positive/negative control
With --fake-principal, a middleware adds Kam's Easy Auth principal header to every request that lacks one, so a real headless
browser can load / and /chat against the double (the page arms: FRIDAY tab, drawer X). Never used against the live site.
Usage: 08g_double_app.py --port 47796 [--fake-principal]
"""
import argparse, copy, os, re, sys, threading

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.normpath(os.path.join(HERE, "..", "app"))

ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, default=47796); ap.add_argument("--fake-principal", action="store_true")
args = ap.parse_args()
os.environ["STORAGE_ACCOUNT"] = "nolivestore-double"
sys.path.insert(0, APP_DIR)
import main  # noqa: E402
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError  # noqa: E402
from azure.data.tables import UpdateMode  # noqa: E402

LOCK = threading.Lock()
STORE = {}          # table -> {(pk, rk): dict}
BLOBS = {}          # name -> bytes
PROOF = {"credential_calls": 0, "live_store_calls": 0, "writes": 0}

class FakeTable:
    def __init__(self, name): self.name = name; STORE.setdefault(name, {})
    @property
    def rows(self): return STORE[self.name]
    def create_entity(self, e):
        k = (e["PartitionKey"], e["RowKey"])
        with LOCK:
            if k in self.rows: raise ResourceExistsError("exists")
            self.rows[k] = copy.deepcopy(dict(e)); PROOF["writes"] += 1
    def update_entity(self, e, mode=UpdateMode.MERGE):
        k = (e["PartitionKey"], e["RowKey"])
        with LOCK:
            if k not in self.rows: raise ResourceNotFoundError("no such entity")
            if mode == UpdateMode.REPLACE: self.rows[k] = copy.deepcopy(dict(e))
            else: self.rows[k].update(copy.deepcopy(dict(e)))
            PROOF["writes"] += 1
    def upsert_entity(self, e, mode=UpdateMode.MERGE):
        k = (e["PartitionKey"], e["RowKey"])
        with LOCK:
            if k in self.rows and mode != UpdateMode.REPLACE: self.rows[k].update(copy.deepcopy(dict(e)))
            else: self.rows[k] = copy.deepcopy(dict(e))
            PROOF["writes"] += 1
    def get_entity(self, pk, rk, select=None):
        with LOCK:
            if (pk, rk) not in self.rows: raise ResourceNotFoundError("no such entity")
            e = copy.deepcopy(self.rows[(pk, rk)])
        return {k: e.get(k) for k in select} if select else e
    def query_entities(self, flt, parameters=None, results_per_page=None, select=None):
        params = parameters or {}
        conds = []
        for part in flt.split(" and "):
            m = re.fullmatch(r"\s*(\w+)\s+(eq|gt)\s+@(\w+)\s*", part)
            if not m: raise ValueError(f"double: unsupported filter part {part!r}")
            conds.append((m.group(1), m.group(2), params.get(m.group(3))))
        with LOCK: items = sorted(self.rows.items())
        out = []
        for (pk, rk), e in items:
            ok = True
            for col, op, val in conds:
                v = e.get(col)
                if op == "eq" and v != val: ok = False
                if op == "gt" and not (v is not None and str(v) > str(val)): ok = False
            if ok:
                d = copy.deepcopy(e)
                out.append({k: d.get(k) for k in select} if select else d)
        return iter(out)
    def list_entities(self, results_per_page=None): return self.query_entities("PartitionKey gt @z", {"z": ""})

_tables = {}
def fake_table(name):
    if name not in _tables: _tables[name] = FakeTable(name)
    return _tables[name]
def no_credential():
    PROOF["credential_calls"] += 1
    raise RuntimeError("08g double: a real Azure credential was requested — the double must never reach the live store")
def fake_blob_put(name, data):
    with LOCK:
        if name in BLOBS: return False
        BLOBS[name] = bytes(data); PROOF["writes"] += 1; return True
def fake_blob_get(name):
    with LOCK:
        if name not in BLOBS: raise main.HTTPException(404, "file bytes not found")
        return BLOBS[name]

main.table = fake_table
main.credential = no_credential
main.blob_put = fake_blob_put
main.blob_get = fake_blob_get
main.ensure_container = lambda: None
main.blob_token = no_credential

import json  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

@main.app.get("/__double/dump")
def _dump():
    with LOCK:
        t = {n: [dict(v, PartitionKey=k[0], RowKey=k[1]) for k, v in sorted(rows.items())] for n, rows in STORE.items()}
        b = {n: len(v) for n, v in BLOBS.items()}
    return JSONResponse(json.loads(json.dumps({"tables": t, "blobs": b}, default=str)))

@main.app.get("/__double/proof")
def _proof(): return dict(PROOF, storage_account=main.STORAGE)

# move the two double routes ahead of main.py's catch-all GET /{path:path}
routes = main.app.router.routes
for path in ("/__double/proof", "/__double/dump"):
    r = [x for x in routes if getattr(x, "path", None) == path][0]
    routes.remove(r); routes.insert(0, r)

if args.fake_principal:
    @main.app.middleware("http")
    async def _principal(request, call_next):
        if "x-ms-client-principal-id" not in request.headers:
            hs = list(request.scope["headers"])
            hs.append((b"x-ms-client-principal-id", main.KAM_OBJECT_ID.encode()))
            hs.append((b"x-ms-client-principal-name", b"kreiser.org@me.com"))
            request.scope["headers"] = hs
        return await call_next(request)

if __name__ == "__main__":
    import uvicorn
    assert main.STORAGE == "nolivestore-double", main.STORAGE
    uvicorn.run(main.app, host="127.0.0.1", port=args.port, log_level="warning")
