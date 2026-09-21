"""main.py — Wednesday external dashboard, Phase 1 pilot (FastAPI on App Service Linux).

Two surfaces, two gates:
  VIEWER (Kam)  GET /            panel page (static/index.html; decrypts client-side)
                GET /api/messages?client=&since=   delta read (never the whole store)
                GET /api/cards?client=&since=
                GET /api/me                        who Easy Auth says I am
     gate: App Service Easy Auth (Microsoft provider, requireAuthentication). The
     app ADDITIONALLY refuses any viewer route without the X-MS-CLIENT-PRINCIPAL-ID
     header (defence in depth: if Easy Auth were ever switched off, these return 401,
     not data). Kam is the only assigned user, so the viewer sees all partitions.

  SEAT API      POST /api/seat/messages   POST /api/seat/cards   GET /api/seat/messages?since=
                GET  /api/seat/health (anonymous liveness for probes)
     gate: Bearer JWT from the seat's client-credentials flow against wednesday-seat-api,
     validated HERE (issuer, audience, signature via the tenant JWKS, expiry). The
     token's `roles` decide the partitions: Client.<X> roles -> allowed clients;
     Seat.Write / Seat.Read -> verb. A body naming a client outside the token's roles
     is REFUSED 403 — the partition comes from the token, never from the body.
     Easy Auth excludes /api/seat/* so this validation is the only gate there.

The server holds NO decryption key. `text` arrives as an envelope (seat/envelope.py)
and is stored as ciphertext; the server never sees prose. Clear routing fields are
validated and stored as columns.
"""
import json, logging, os, re, time, datetime, uuid
from typing import Optional
import jwt, requests
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient, UpdateMode

log = logging.getLogger("wedcloud")
logging.basicConfig(level=logging.INFO)
logging.getLogger("azure").setLevel(logging.WARNING)  # SDK request/response dumps are noise; the app logs its own decisions

TENANT_ID = os.environ.get("TENANT_ID", "")
API_APPID = os.environ.get("SEAT_API_APPID", "")          # audience of seat tokens
STORAGE = os.environ.get("STORAGE_ACCOUNT", "")
CLIENTS = ("Secuura", "Datasec", "WED")
SEAT_APPS = {}  # client app id -> seat name, from env SEAT_APP_MAP="appid:wednesday,appid:tuesday"
for pair in os.environ.get("SEAT_APP_MAP", "").split(","):
    if ":" in pair:
        a, n = pair.split(":", 1); SEAT_APPS[a.strip()] = n.strip()
ISSUERS = (f"https://login.microsoftonline.com/{TENANT_ID}/v2.0", f"https://sts.windows.net/{TENANT_ID}/")
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
HERE = os.path.dirname(os.path.abspath(__file__))
PUBKEY_PATH = os.path.join(HERE, "keys", "kam-pilot-public.pub")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")
ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
ENVELOPE_FIELDS = ("scheme", "kid", "iv", "wrapped_key", "ciphertext")

app = FastAPI(title="wednesday-dashboard pilot", docs_url=None, redoc_url=None, openapi_url=None)

# ---------------- storage (managed identity; no account key anywhere) ----------------
_tables = {}
def table(name: str):
    if name not in _tables:
        cred = DefaultAzureCredential()
        svc = TableServiceClient(endpoint=f"https://{STORAGE}.table.core.windows.net", credential=cred)
        _tables[name] = svc.get_table_client(name)
    return _tables[name]

# ---------------- seat token validation ----------------
_jwks_cache = {"t": 0, "client": None}
def jwks_client():
    if _jwks_cache["client"] is None or time.time() - _jwks_cache["t"] > 3600:
        _jwks_cache["client"] = jwt.PyJWKClient(JWKS_URL, cache_keys=True)
        _jwks_cache["t"] = time.time()
    return _jwks_cache["client"]

def seat_from_token(request: Request) -> dict:
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(401, "bearer token required")
    tok = auth.split(None, 1)[1].strip()
    try:
        key = jwks_client().get_signing_key_from_jwt(tok).key
        claims = jwt.decode(tok, key, algorithms=["RS256"], audience=[API_APPID, f"api://{API_APPID}"],
                            issuer=list(ISSUERS), options={"require": ["exp", "iss", "aud"]})
    except jwt.PyJWTError as e:
        log.warning("seat token rejected: %s", type(e).__name__)
        raise HTTPException(401, f"token invalid: {type(e).__name__}")
    if claims.get("tid") != TENANT_ID:
        raise HTTPException(401, "wrong tenant")
    roles = set(claims.get("roles") or [])
    clients = {r.split(".", 1)[1] for r in roles if r.startswith("Client.") and r.split(".", 1)[1] in CLIENTS}
    appid = claims.get("azp") or claims.get("appid") or ""
    return {"appid": appid, "seat": SEAT_APPS.get(appid, "unknown"), "oid": claims.get("oid"),
            "clients": clients, "write": "Seat.Write" in roles, "read": "Seat.Read" in roles}

def require_partition(seat: dict, client: Optional[str]) -> str:
    if client not in CLIENTS:
        raise HTTPException(400, f"client must be one of {CLIENTS}")
    if client not in seat["clients"]:
        # The check that must be able to fail: token says X, body says Y -> refused, empty.
        log.warning("R0 refusal: seat=%s roles=%s asked=%s", seat["seat"], sorted(seat["clients"]), client)
        raise HTTPException(403, "partition not granted to this seat")
    return client

def validate_envelope(body: dict):
    env = body.get("envelope")
    if not isinstance(env, dict) or any(k not in env for k in ENVELOPE_FIELDS):
        raise HTTPException(400, f"envelope must carry {ENVELOPE_FIELDS}")
    if "text" in body or "plaintext" in body:
        raise HTTPException(400, "plaintext fields are refused; encrypt into the envelope")
    return {k: str(env[k]) for k in ENVELOPE_FIELDS}

def validate_clear(body: dict, kind: str):
    ts = body.get("ts") or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    if not TS_RE.match(ts): raise HTTPException(400, "ts must be ISO-8601 UTC with Z")
    rid = body.get("id") or uuid.uuid4().hex[:10]
    if not ID_RE.match(rid): raise HTTPException(400, "id must be [A-Za-z0-9._-]{1,64}")
    return ts, rid

def now_iso(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------- seat routes (Easy Auth excluded; own JWT gate) ----------------
@app.get("/api/seat/health")
def seat_health():
    return {"app": "wednesday-dashboard-cloud", "ok": True, "phase": "pilot", "ts": now_iso()}

@app.post("/api/seat/messages", status_code=201)
async def seat_post_message(request: Request):
    seat = seat_from_token(request)
    if not seat["write"]: raise HTTPException(403, "Seat.Write role required")
    body = await request.json()
    client = require_partition(seat, body.get("client"))
    env = validate_envelope(body)
    ts, rid = validate_clear(body, "message")
    view = str(body.get("view") or client)[:64]
    role = str(body.get("role") or seat["seat"])[:32]
    row = {"PartitionKey": client, "RowKey": f"{ts}_{rid}", "kind": "message", "id": rid, "ts": ts, "view": view,
           "role": role, "seat": seat["seat"], "written_by": seat["appid"], "written_at": now_iso(), **env}
    table("messages").upsert_entity(row, mode=UpdateMode.REPLACE)
    return {"stored": {"client": client, "id": rid, "ts": ts, "row_key": row["RowKey"], "written_by": seat["seat"]}}

@app.post("/api/seat/cards", status_code=201)
async def seat_post_card(request: Request):
    seat = seat_from_token(request)
    if not seat["write"]: raise HTTPException(403, "Seat.Write role required")
    body = await request.json()
    client = require_partition(seat, body.get("client"))
    env = validate_envelope(body)
    ts, rid = validate_clear(body, "card")
    option_keys = body.get("option_keys") or []
    if not isinstance(option_keys, list) or not all(isinstance(k, str) and len(k) <= 4 for k in option_keys):
        raise HTTPException(400, "option_keys must be a list of short strings (the letters stay clear)")
    status = str(body.get("status") or "open")
    if status not in ("open", "ruled", "withdrawn"): raise HTTPException(400, "status")
    row = {"PartitionKey": client, "RowKey": f"{ts}_{rid}", "kind": "card", "id": rid, "ts": ts,
           "client_project": str(body.get("client_project") or client)[:64], "status": status,
           "option_keys": json.dumps(option_keys), "recommended": str(body.get("recommended") or "")[:4],
           "ruled": bool(body.get("ruled", False)), "ruled_choice": str(body.get("ruled_choice") or "")[:4],
           "seat": seat["seat"], "written_by": seat["appid"], "written_at": now_iso(), **env}
    table("cards").upsert_entity(row, mode=UpdateMode.REPLACE)
    return {"stored": {"client": client, "id": rid, "ts": ts, "row_key": row["RowKey"], "written_by": seat["seat"]}}

def _query(tname: str, clients, since: Optional[str], limit: int):
    out = []
    for c in sorted(clients):
        flt = f"PartitionKey eq @c" + (" and RowKey gt @s" if since else "")
        params = {"c": c, "s": since or ""}
        for e in table(tname).query_entities(flt, parameters=params, results_per_page=min(limit, 1000)):
            d = {k: v for k, v in e.items() if k not in ("PartitionKey", "RowKey")}
            d["client"] = c; d["row_key"] = e["RowKey"]
            if "option_keys" in d:
                try: d["option_keys"] = json.loads(d["option_keys"])
                except Exception: pass
            out.append(d)
            if len(out) >= limit: break
    out.sort(key=lambda r: r["row_key"])
    return out[-limit:]

@app.get("/api/seat/messages")
def seat_get_messages(request: Request, client: Optional[str] = None, since: Optional[str] = None, limit: int = Query(200, le=1000)):
    seat = seat_from_token(request)
    if not seat["read"]: raise HTTPException(403, "Seat.Read role required")
    clients = {require_partition(seat, client)} if client else seat["clients"]
    return {"messages": _query("messages", clients, since, limit), "clients": sorted(clients)}

# ---------------- viewer routes (Easy Auth gate + header check) ----------------
def viewer(request: Request) -> dict:
    pid = request.headers.get("x-ms-client-principal-id")
    if not pid:
        raise HTTPException(401, "no authenticated principal (Easy Auth header missing)")
    return {"id": pid, "name": request.headers.get("x-ms-client-principal-name", "")}

@app.get("/api/me")
def me(request: Request):
    return viewer(request)

@app.get("/api/messages")
def get_messages(request: Request, client: Optional[str] = None, since: Optional[str] = None, limit: int = Query(200, le=1000)):
    viewer(request)
    clients = {client} if client in CLIENTS else set(CLIENTS)
    return {"messages": _query("messages", clients, since, limit)}

@app.get("/api/cards")
def get_cards(request: Request, client: Optional[str] = None, since: Optional[str] = None, limit: int = Query(200, le=1000)):
    viewer(request)
    clients = {client} if client in CLIENTS else set(CLIENTS)
    return {"cards": _query("cards", clients, since, limit)}

@app.get("/api/pubkey")
def pubkey(request: Request):
    viewer(request)
    return PlainTextResponse(open(PUBKEY_PATH).read())

@app.get("/")
def index(request: Request):
    viewer(request)
    return FileResponse(os.path.join(HERE, "static", "index.html"), headers={"Cache-Control": "no-store"})

@app.get("/{path:path}")
def catch_all(path: str, request: Request):
    viewer(request)
    raise HTTPException(404, "no such page")
