"""main.py — Wednesday external dashboard (FastAPI on App Service Linux). Phase 1 pilot + Phase 2 (2026-09-21).

Two surfaces, two gates:
  VIEWER (Kam)  GET /            cockpit page (static/index.html — the local cockpit.html layout; decrypts client-side)
                GET /chat        chat page   (static/chat.html  — the local chat.html layout)
                GET /static/common.js        shared key/crypto/API module for both pages
                GET /api/messages?client=&since=   delta read (never the whole store)
                GET /api/cards?client=             cards are STATE (ruled/withdrawn change in place) -> read whole, no since
                GET /api/me                        who Easy Auth says I am (+ is_kam)
                GET /api/pubkey                    Kam's envelope PUBLIC key (the browser encrypts his replies with it)
                POST /api/kam/messages             Phase 2: Kam's reply path. Envelope only (the browser encrypts to his own
                                                   public key); `view` (the tab he typed in) decides the partition:
                                                   wednesday -> WED, tuesday -> Datasec, both -> ALL (broadcast).
     gate: App Service Easy Auth (Microsoft provider, requireAuthentication). The app ADDITIONALLY refuses any viewer
     route without the X-MS-CLIENT-PRINCIPAL-ID header (defence in depth), and the WRITE route additionally requires that
     principal id to equal KAM_OBJECT_ID (app setting) — Easy Auth strips/overwrites x-ms-client-principal-* on the way
     in and never forwards an anonymous request, so a forged header from outside never reaches this code (probe A8).

  SEAT API      POST /api/seat/messages   POST /api/seat/cards   GET /api/seat/messages?since=&author=&client=
                GET  /api/seat/health (anonymous liveness for probes)
     gate: Bearer JWT from the seat's client-credentials flow against wednesday-seat-api, validated HERE (issuer,
     audience, signature via the tenant JWKS, expiry). The token's `roles` decide the partitions: Client.<X> roles ->
     allowed clients; Seat.Write / Seat.Read -> verb. A body naming a client outside the token's roles is REFUSED 403 —
     the partition comes from the token, never from the body. Easy Auth excludes /api/seat/* so this validation is the
     only gate there. Seats READ their own partitions plus ALL (Kam's broadcast rows); no seat can WRITE ALL (no role).

Phase 2 idempotency: a message row is INSERTED, never replaced — a second POST with the same (client, ts, id) returns
200 {"duplicate": true} and writes nothing, so a re-run of the backfill posts nothing new. A card row is keyed by its id
alone (RowKey card_<id>) and is state: the first POST is 201, a later POST with the same id updates it (200 {"updated"}).

The server holds NO decryption key. `text` arrives as an envelope (seat/envelope.py or the browser's WebCrypto twin)
and is stored as ciphertext; the server never sees prose. Clear routing fields are validated and stored as columns.

Phase 3 (2026-09-21, D-2(b)): the envelope may carry `wrapped_keys: [{kid, wrapped_key}, ...]` — the same data key wrapped
to EVERY recipient: Kam's key ring (every app/keys/kam-*-public.pub: pilot, laptop, ipad) AND the addressed seat's
certificate public key (app/keys/<seat>-seat-public.pub; WED/Secuura -> wednesday, Datasec -> tuesday, ALL -> both).
Stored as a JSON string column, returned parsed. The top-level kid/wrapped_key pair stays for one release. The server
still cannot decrypt anything: it only knows PUBLIC keys and their kids, and uses them for ONE check — a Kam reply
(POST /api/kam/messages) must carry the addressed seat's kid(s), or it is refused 400 (an unreadable reply is a lost
reply; this makes "the seat can read what Kam typed" true by construction). GET /api/pubkeys serves the ring + seat keys.

Usage gauges (2026-09-22, Kam 08:57:36 on the live board: "with the local version, I was able to see the weekly usage count
on both Wednesday and Tuesday. Is this possible for the live version?"): each seat's statusline writes usage_<seat>.json
on ITS OWN machine (the figure reaches that script on stdin from Claude Code and exists nowhere else). seat/post_usage.py
POSTs that reading here as the seat, with the seat's certificate token: POST /api/seat/usage. The row is CLEAR (a
percentage is not prose and not secret) but ATTRIBUTED BY THE TOKEN — the seat name comes from the token's app id, a body
naming another seat is refused 403, and there is no anonymous or viewer write path, so a viewer cannot spoof a seat's
gauge. One row per seat (table `usage`, PartitionKey USAGE, RowKey <seat>; REPLACE — last write wins: there is ONE
publisher per seat and it only sends readings < 30 min old; the page always shows the reading's age). GET /api/usage (viewer, Easy Auth) serves both rows with the reading's age — the page decides what "stale"
means (as the local server does: the age is served, never hidden). GET /api/seat/usage (Seat.Read) is the seat-side
read-back used by the probes.

Hide / unhide (2026-09-22, Kam 14:27:09 on the Tuesday tab: "Please clean up your boards so you don't have any local model
workloads at this stage"): a message row can be HIDDEN — never deleted, never rewritten. POST /api/seat/hide and
POST /api/seat/unhide take {client, row_key | id} and are allowed ONLY for rows whose partition the calling seat's token
grants (the same R0 rule as a write: a Datasec/`tuesday`-tab row is the tuesday seat's, a WED/Secuura row the wednesday
seat's; no seat may hide ALL). The flag is a MERGE of clear columns onto the row (hidden, hidden_by, hidden_at, hidden_seat /
unhidden_*): the envelope and every other column are untouched. Every call appends an AUDIT row in the same `messages`
table under PartitionKey AUDIT (action, target, who, when, reason) — a partition no read route or page ever lists
(READ_PARTITIONS excludes it; migrate_rewrap leaves unknown partitions alone). Reads (viewer /api/messages, seat
/api/seat/messages) SKIP hidden rows unless ?hidden=1 (the reveal, for audit); GET /api/seat/hide/audit lists the audit rows
for the seat's partitions. Health reports hide_route: true.
"""
import json, logging, os, re, time, datetime, uuid, glob, hashlib, base64
from typing import Optional
import jwt, requests
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient, UpdateMode
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

log = logging.getLogger("wedcloud")
logging.basicConfig(level=logging.INFO)
logging.getLogger("azure").setLevel(logging.WARNING)  # SDK request/response dumps are noise; the app logs its own decisions

TENANT_ID = os.environ.get("TENANT_ID", "")
API_APPID = os.environ.get("SEAT_API_APPID", "")          # audience of seat tokens
STORAGE = os.environ.get("STORAGE_ACCOUNT", "")
KAM_OBJECT_ID = os.environ.get("KAM_OBJECT_ID", "")       # the ONLY principal allowed to write via /api/kam/*
CLIENTS = ("Secuura", "Datasec", "WED")                   # seat-writable partitions (token roles)
BROADCAST = "ALL"                                          # Kam's "both" rows; readable by every seat, written only by Kam
READ_PARTITIONS = CLIENTS + (BROADCAST,)
VIEW_TO_CLIENT = {"wednesday": "WED", "tuesday": "Datasec", "both": BROADCAST}
SEAT_APPS = {}  # client app id -> seat name, from env SEAT_APP_MAP="appid:wednesday,appid:tuesday"
for pair in os.environ.get("SEAT_APP_MAP", "").split(","):
    if ":" in pair:
        a, n = pair.split(":", 1); SEAT_APPS[a.strip()] = n.strip()
ISSUERS = (f"https://login.microsoftonline.com/{TENANT_ID}/v2.0", f"https://sts.windows.net/{TENANT_ID}/")
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
HERE = os.path.dirname(os.path.abspath(__file__))
PUBKEY_PATH = os.path.join(HERE, "keys", "kam-pilot-public.pub")
KEYS_DIR = os.path.join(HERE, "keys")
SEAT_OF_CLIENT = {"WED": ("wednesday",), "Secuura": ("wednesday",), "Datasec": ("tuesday",), BROADCAST: ("wednesday", "tuesday")}
KID_RE = re.compile(r"^[0-9a-f]{16}$")
B64_RE = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")

def _kid_of_pem(pem: str) -> str:
    """sha256(SPKI DER)[:16] — the same kid seat/envelope.py and common.js compute. PUBLIC keys only live here."""
    body = "".join(l for l in pem.splitlines() if l and not l.startswith("-----"))
    return hashlib.sha256(base64.b64decode(body)).hexdigest()[:16]

_ring_cache = {"t": 0, "v": None}
def public_keys() -> dict:
    """Kam's ring (pilot first) + the seat public keys, with kids. Read from disk, cached 60 s."""
    if _ring_cache["v"] is None or time.time() - _ring_cache["t"] > 60:
        kam = []
        files = sorted(glob.glob(os.path.join(KEYS_DIR, "kam-*-public.pub")))
        files.sort(key=lambda q: (0 if os.path.basename(q) == "kam-pilot-public.pub" else 1, q))
        for q in files:
            pem = open(q).read(); kam.append({"name": os.path.basename(q)[4:-11], "kid": _kid_of_pem(pem), "pem": pem})
        seats = {}
        for s in ("wednesday", "tuesday"):
            q = os.path.join(KEYS_DIR, f"{s}-seat-public.pub")
            if os.path.exists(q):
                pem = open(q).read(); seats[s] = {"kid": _kid_of_pem(pem), "pem": pem}
        _ring_cache["v"] = {"kam": kam, "seats": seats, "seat_of_client": {c: list(v) for c, v in SEAT_OF_CLIENT.items()}}
        _ring_cache["t"] = time.time()
    return _ring_cache["v"]
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")
ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
KEY_RE = re.compile(r"^[A-Za-z0-9._-]{0,32}$")             # option keys are slugs (measured up to 26 chars locally)
ENVELOPE_FIELDS = ("scheme", "kid", "iv", "wrapped_key", "ciphertext")

app = FastAPI(title="wednesday-dashboard", docs_url=None, redoc_url=None, openapi_url=None)

# ---------------- storage (managed identity; no account key anywhere) ----------------
_tables = {}
USAGE_TABLE = "usage"          # 2026-09-22: sibling of messages/cards in the SAME storage account (created on first use — a table, not a resource)
def table(name: str):
    if name not in _tables:
        cred = DefaultAzureCredential()
        svc = TableServiceClient(endpoint=f"https://{STORAGE}.table.core.windows.net", credential=cred)
        _tables[name] = svc.create_table_if_not_exists(name) if name == USAGE_TABLE else svc.get_table_client(name)
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

def require_partition(seat: dict, client: Optional[str], for_read: bool = False) -> str:
    allowed = tuple(READ_PARTITIONS) if for_read else CLIENTS
    if client not in allowed:
        raise HTTPException(400, f"client must be one of {allowed}")
    if client == BROADCAST and for_read:
        return client                       # every seat reads Kam's broadcast rows; nobody but Kam writes them
    if client not in seat["clients"]:
        # The check that must be able to fail: token says X, body says Y -> refused, empty.
        log.warning("R0 refusal: seat=%s roles=%s asked=%s", seat["seat"], sorted(seat["clients"]), client)
        raise HTTPException(403, "partition not granted to this seat")
    return client

def validate_envelope(body: dict, require_seat_kids_for: Optional[str] = None):
    env = body.get("envelope")
    if not isinstance(env, dict) or any(k not in env for k in ENVELOPE_FIELDS):
        raise HTTPException(400, f"envelope must carry {ENVELOPE_FIELDS}")
    if "text" in body or "plaintext" in body:
        raise HTTPException(400, "plaintext fields are refused; encrypt into the envelope")
    out = {k: str(env[k]) for k in ENVELOPE_FIELDS}
    wk = env.get("wrapped_keys")
    if wk is not None:
        if not isinstance(wk, list) or len(wk) > 8 or not all(isinstance(e, dict) and KID_RE.match(str(e.get("kid", ""))) and
               isinstance(e.get("wrapped_key"), str) and 0 < len(e["wrapped_key"]) <= 1024 and B64_RE.match(e["wrapped_key"]) for e in wk):
            raise HTTPException(400, "wrapped_keys must be a list (<=8) of {kid: 16 hex, wrapped_key: base64}")
        out["wrapped_keys"] = json.dumps([{"kid": e["kid"], "wrapped_key": e["wrapped_key"]} for e in wk])
    if require_seat_kids_for:
        # Phase 3: a Kam reply must be wrapped to the seat(s) that partition addresses, or nobody but Kam can ever read it.
        kids = {e["kid"] for e in (wk or [])} | {out["kid"]}
        need = {public_keys()["seats"][s]["kid"] for s in SEAT_OF_CLIENT[require_seat_kids_for] if s in public_keys()["seats"]}
        if not need <= kids:
            raise HTTPException(400, f"reply must be wrapped to the addressed seat key(s) {sorted(need)} (page out of date? reload)")
    return out

def validate_clear(body: dict, kind: str):
    ts = body.get("ts") or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    if not TS_RE.match(ts): raise HTTPException(400, "ts must be ISO-8601 UTC with Z")
    rid = body.get("id") or uuid.uuid4().hex[:10]
    if not ID_RE.match(rid): raise HTTPException(400, "id must be [A-Za-z0-9._-]{1,64}")
    return ts, rid

def clear_extras(body: dict) -> dict:
    """Phase 2 clear routing extras (study §4.4 — timestamps and flags, never prose)."""
    out = {}
    if body.get("backfill") is True: out["backfill"] = True
    if body.get("synthetic") is True: out["synthetic"] = True    # Phase 3: probe/test rows are BORN marked; the pages hide them (never deleted)
    src = body.get("src_ts")
    if src is not None:
        src = str(src)[:40]
        if not re.match(r"^[0-9T:.+\-Z]{1,40}$", src): raise HTTPException(400, "src_ts must be a timestamp")
        out["src_ts"] = src
    return out

def now_iso(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def insert_message(row: dict) -> bool:
    """INSERT semantics: returns True if written, False if the (PartitionKey, RowKey) already existed (nothing written)."""
    try:
        table("messages").create_entity(row)
        return True
    except ResourceExistsError:
        return False

def store_card(row: dict) -> bool:
    """Cards are state: returns True if created, False if an existing card was updated in place."""
    try:
        table("cards").create_entity(row)
        return True
    except ResourceExistsError:
        table("cards").update_entity(row, mode=UpdateMode.REPLACE)
        return False

def card_row(client: str, body: dict, env: dict, ts: str, rid: str, seat_name: str, written_by: str) -> dict:
    option_keys = body.get("option_keys") or []
    if not isinstance(option_keys, list) or not all(isinstance(k, str) and KEY_RE.match(k) for k in option_keys):
        raise HTTPException(400, "option_keys must be a list of slugs [A-Za-z0-9._-]{0,32} (the keys stay clear)")
    status = str(body.get("status") or "open")
    if status not in ("open", "ruled", "withdrawn"): raise HTTPException(400, "status")
    rec = str(body.get("recommended") or ""); rc = str(body.get("ruled_choice") or "")
    if not KEY_RE.match(rec) or not KEY_RE.match(rc): raise HTTPException(400, "recommended/ruled_choice must be slugs")
    ruled_ts = str(body.get("ruled_ts") or "")[:40]
    if ruled_ts and not re.match(r"^[0-9T:.+\-Z]{1,40}$", ruled_ts): raise HTTPException(400, "ruled_ts must be a timestamp")
    return {"PartitionKey": client, "RowKey": f"card_{rid}", "kind": "card", "id": rid, "ts": ts,
            "client_project": str(body.get("client_project") or client)[:64], "status": status,
            "option_keys": json.dumps(option_keys), "recommended": rec,
            "ruled": bool(body.get("ruled", False)), "ruled_choice": rc, "ruled_ts": ruled_ts,
            "seat": seat_name, "written_by": written_by, "written_at": now_iso(), **clear_extras(body), **env}

# ---------------- seat routes (Easy Auth excluded; own JWT gate) ----------------
@app.get("/api/seat/health")
def seat_health():
    return {"app": "wednesday-dashboard-cloud", "ok": True, "phase": "3", "ts": now_iso(), "kam_keys": len(public_keys()["kam"]), "seat_keys": sorted(public_keys()["seats"]),
            "usage_route": True,   # 2026-09-22 usage gauges
            "hide_route": True}    # 2026-09-22 hide/unhide (reversible, audited)

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
           "role": role, "seat": seat["seat"], "written_by": seat["appid"], "written_at": now_iso(), **clear_extras(body), **env}
    stored = {"client": client, "id": rid, "ts": ts, "row_key": row["RowKey"], "written_by": seat["seat"]}
    if insert_message(row):
        return {"stored": stored}
    return JSONResponse(status_code=200, content={"stored": stored, "duplicate": True})

@app.post("/api/seat/cards", status_code=201)
async def seat_post_card(request: Request):
    seat = seat_from_token(request)
    if not seat["write"]: raise HTTPException(403, "Seat.Write role required")
    body = await request.json()
    client = require_partition(seat, body.get("client"))
    env = validate_envelope(body)
    ts, rid = validate_clear(body, "card")
    row = card_row(client, body, env, ts, rid, seat["seat"], seat["appid"])
    stored = {"client": client, "id": rid, "ts": ts, "row_key": row["RowKey"], "written_by": seat["seat"]}
    if store_card(row):
        return {"stored": stored}
    return JSONResponse(status_code=200, content={"stored": stored, "updated": True})

def _query(tname: str, clients, since: Optional[str], limit: int, author: Optional[str] = None, include_hidden: bool = False):
    """Rows after `since` (RowKey order = ts order for messages), up to `limit` PER PARTITION, merged and sorted.
    Phase 2: the cap is per partition on purpose — a shared cap filled by the first partition starved the others.
    2026-09-22: rows with hidden=true are SKIPPED (not counted against the cap) unless include_hidden — the filter is applied
    here in code, not in the OData filter, because Table storage drops rows that LACK a property from a `ne` comparison."""
    out = []
    for c in sorted(clients):
        flt = "PartitionKey eq @c" + (" and RowKey gt @s" if since else "") + (" and role eq @a" if author else "")
        params = {"c": c, "s": since or "", "a": author or ""}
        n = 0
        for e in table(tname).query_entities(flt, parameters=params, results_per_page=min(limit, 1000)):
            if not include_hidden and e.get("hidden") is True: continue     # hidden (reversible): absent from every list unless ?hidden=1
            d = {k: v for k, v in e.items() if k not in ("PartitionKey", "RowKey")}
            d["client"] = c; d["row_key"] = e["RowKey"]
            if "option_keys" in d:
                try: d["option_keys"] = json.loads(d["option_keys"])
                except Exception: pass
            if isinstance(d.get("wrapped_keys"), str):
                try: d["wrapped_keys"] = json.loads(d["wrapped_keys"])
                except Exception: pass
            out.append(d); n += 1
            if n >= limit: break
    out.sort(key=lambda r: r["row_key"])
    return out

@app.get("/api/seat/messages")
def seat_get_messages(request: Request, client: Optional[str] = None, since: Optional[str] = None,
                      author: Optional[str] = None, limit: int = Query(200, le=1000), hidden: int = Query(0, ge=0, le=1)):
    """A seat reads its own partitions + ALL (Kam's broadcast). `author=kam` narrows to Kam's rows (role=kam) —
    this is how a seat picks up what Kam typed on the live site. The partition set is the token's, never the query's.
    `hidden=1` REVEALS hidden rows (they carry hidden/hidden_by/hidden_at); default lists skip them."""
    seat = seat_from_token(request)
    if not seat["read"]: raise HTTPException(403, "Seat.Read role required")
    clients = {require_partition(seat, client, for_read=True)} if client else (set(seat["clients"]) | {BROADCAST})
    if author is not None and not re.match(r"^[a-z]{1,32}$", author): raise HTTPException(400, "author")
    return {"messages": _query("messages", clients, since, limit, author, include_hidden=bool(hidden)), "clients": sorted(clients), "hidden_included": bool(hidden)}

# ---------------- hide / unhide (2026-09-22): reversible, audited, never deletes, never rewrites text ----------------
AUDIT_PARTITION = "AUDIT"       # same `messages` table; not in READ_PARTITIONS -> no read route / page / seat list ever returns it
ROWKEY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z_[A-Za-z0-9._-]{1,64}$")
REASON_RE = re.compile(r"^[A-Za-z0-9 ._:/()+'-]{0,160}$")
HIDE_SELECT = ["PartitionKey", "RowKey", "id", "ts", "view", "role", "seat", "hidden", "hidden_at", "hidden_by", "hidden_seat", "synthetic"]

def find_message(client: str, body: dict) -> dict:
    """The target row, by row_key (exact) or by id (must match exactly ONE row in the partition). Clear columns only are read."""
    t = table("messages")
    rk = body.get("row_key")
    if rk is not None:
        rk = str(rk)
        if not ROWKEY_RE.match(rk): raise HTTPException(400, "row_key must be <ISO UTC ts>_<id>")
        try: return t.get_entity(client, rk, select=HIDE_SELECT)
        except ResourceNotFoundError: raise HTTPException(404, "no such row")
    rid = body.get("id")
    if rid is None or not ID_RE.match(str(rid)): raise HTTPException(400, "row_key or id required")
    hits = list(t.query_entities("PartitionKey eq @c and id eq @i", parameters={"c": client, "i": str(rid)}, select=HIDE_SELECT))
    if not hits: raise HTTPException(404, "no such row")
    if len(hits) > 1: raise HTTPException(409, "id matches several rows; pass row_key")
    return hits[0]

async def set_hidden(request: Request, flag: bool):
    """Shared by /hide and /unhide. Gate = Seat.Write + the row's partition granted to the token (R0, exactly as a write):
    the tuesday seat may hide tuesday-tab (Datasec) rows, the wednesday seat WED/Secuura rows; ALL is nobody's to hide.
    Idempotent: hiding a hidden row is 200 changed=false — and still audited (the attempt is a fact)."""
    seat = seat_from_token(request)
    if not seat["write"]: raise HTTPException(403, "Seat.Write role required")
    body = await request.json()
    if not isinstance(body, dict): raise HTTPException(400, "json object required")
    client = require_partition(seat, body.get("client"))          # 403 for a partition outside the token's roles; 400 for ALL/unknown
    e = find_message(client, body)
    reason = str(body.get("reason") or "")[:200]
    if not REASON_RE.match(reason): raise HTTPException(400, "reason must be <=160 chars of [A-Za-z0-9 ._:/()+'-]")
    was = e.get("hidden") is True
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    verb = "hidden" if flag else "unhidden"
    patch = {"PartitionKey": client, "RowKey": e["RowKey"], "hidden": flag, f"{verb}_by": seat["appid"], f"{verb}_at": now, f"{verb}_seat": seat["seat"]}
    table("messages").update_entity(patch, mode=UpdateMode.MERGE)   # MERGE = only these columns change; envelope/text/routing untouched
    audit = {"PartitionKey": AUDIT_PARTITION, "RowKey": f"{now}_{uuid.uuid4().hex[:8]}", "kind": "hide_audit", "action": "hide" if flag else "unhide",
             "target_client": client, "target_row_key": e["RowKey"], "target_id": str(e.get("id") or ""), "target_view": str(e.get("view") or "")[:64],
             "seat": seat["seat"], "by": seat["appid"], "at": now, "reason": reason, "changed": was != flag}
    table("messages").create_entity(audit)
    log.info("%s %s/%s by seat=%s changed=%s", audit["action"], client, e["RowKey"], seat["seat"], was != flag)
    return {"row": {"client": client, "row_key": e["RowKey"], "id": e.get("id"), "ts": e.get("ts"), "view": e.get("view"), "hidden": flag},
            "changed": was != flag, "audit_row_key": audit["RowKey"], "by": seat["seat"]}

@app.post("/api/seat/hide")
async def seat_hide(request: Request):
    return await set_hidden(request, True)

@app.post("/api/seat/unhide")
async def seat_unhide(request: Request):
    return await set_hidden(request, False)

@app.get("/api/seat/hide/audit")
def seat_hide_audit(request: Request, limit: int = Query(200, le=1000)):
    """The audit rows (hide/unhide) whose target partition the seat may read; newest last. Seat.Read."""
    seat = seat_from_token(request)
    if not seat["read"]: raise HTTPException(403, "Seat.Read role required")
    mine = set(seat["clients"]) | {BROADCAST}
    out = []
    for e in table("messages").query_entities("PartitionKey eq @p", parameters={"p": AUDIT_PARTITION}, results_per_page=min(limit, 1000)):
        if e.get("target_client") not in mine: continue
        out.append({k: v for k, v in e.items() if k not in ("PartitionKey",)})
        if len(out) >= limit: break
    out.sort(key=lambda r: r["RowKey"])
    return {"audit": out, "clients": sorted(mine)}

# ---------------- usage gauges (2026-09-22): seat-published, token-attributed, clear ----------------
USAGE_PARTITION = "USAGE"
RESETS_RE = re.compile(r"^[A-Za-z0-9 ]{0,32}$")
SEATS = ("wednesday", "tuesday")

def usage_row_of(e) -> dict:
    d = {k: e[k] for k in ("seat", "pct", "resets_in", "reading_ts", "written_by", "written_at") if k in e}
    try:
        t = datetime.datetime.strptime(d.get("reading_ts", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        d["age_seconds"] = int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds())
    except Exception:
        d["age_seconds"] = None       # served as unknown; the page treats unknown as "no reading" (never as fresh)
    return d

def usage_rows() -> dict:
    """{seat: row|None} for both seats — the local /api/usage shape (None = nothing published)."""
    out = {s: None for s in SEATS}
    try:
        for e in table(USAGE_TABLE).query_entities("PartitionKey eq @p", parameters={"p": USAGE_PARTITION}):
            if e["RowKey"] in out: out[e["RowKey"]] = usage_row_of(e)
    except Exception as ex:
        log.warning("usage read failed: %s", type(ex).__name__)
        raise HTTPException(503, "usage store unavailable")
    return out

@app.post("/api/seat/usage", status_code=201)
async def seat_post_usage(request: Request):
    """The seat's weekly plan usage. ATTRIBUTION IS THE TOKEN'S: the row is written under the seat the token's app id maps
    to; a body `seat` that names another seat is refused 403 (a spoof attempt), an unmapped app id is refused 403. Values
    are clear and bounded (pct 0..100, resets_in <=32 chars of [A-Za-z0-9 ], reading ts ISO-8601 UTC seconds). One row
    per seat, replaced whole — last write wins (an "older reading is ignored" guard was built and REMOVED the same
    morning: it let a probe fixture sit on the board that the seat's real reading, older by the clock, could not displace)."""
    seat = seat_from_token(request)
    if not seat["write"]: raise HTTPException(403, "Seat.Write role required")
    if seat["seat"] not in SEATS:
        log.warning("usage refused: unmapped app id %s", seat["appid"][:8]); raise HTTPException(403, "token's app id is not a known seat")
    body = await request.json()
    if not isinstance(body, dict): raise HTTPException(400, "json object required")
    claimed = body.get("seat")
    if claimed is not None and str(claimed) != seat["seat"]:
        log.warning("usage SPOOF refused: token seat=%s body seat=%s", seat["seat"], str(claimed)[:16])
        raise HTTPException(403, f"usage rows are attributed by the token (this token is the {seat['seat']} seat)")
    pct = body.get("pct")
    if isinstance(pct, bool) or not isinstance(pct, (int, float)) or not (0 <= float(pct) <= 100): raise HTTPException(400, "pct must be a number 0..100")
    resets = str(body.get("resets_in") or "")[:40]
    if not RESETS_RE.match(resets): raise HTTPException(400, "resets_in must be <=32 chars of [A-Za-z0-9 ]")
    rts = str(body.get("ts") or "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", rts): raise HTTPException(400, "ts must be the reading's ISO-8601 UTC timestamp (seconds, Z)")
    try:
        rt = datetime.datetime.strptime(rts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        raise HTTPException(400, "ts is not a valid timestamp")
    if rt > datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5): raise HTTPException(400, "ts is in the future")
    row = {"PartitionKey": USAGE_PARTITION, "RowKey": seat["seat"], "kind": "usage", "seat": seat["seat"], "pct": int(round(float(pct))),
           "resets_in": resets, "reading_ts": rts, "written_by": seat["appid"], "written_at": now_iso()}
    t = table(USAGE_TABLE)
    try:
        t.create_entity(row)
        return {"stored": {"seat": seat["seat"], "pct": row["pct"], "reading_ts": rts}, "created": True}
    except ResourceExistsError:
        t.upsert_entity(row, mode=UpdateMode.REPLACE)
        return JSONResponse(status_code=200, content={"stored": {"seat": seat["seat"], "pct": row["pct"], "reading_ts": rts}, "updated": True})

@app.get("/api/seat/usage")
def seat_get_usage(request: Request):
    """Both seats' gauges for a seat (Seat.Read) — the probe's read-back; a percentage is not partition-scoped prose."""
    seat = seat_from_token(request)
    if not seat["read"]: raise HTTPException(403, "Seat.Read role required")
    return usage_rows()

# ---------------- viewer routes (Easy Auth gate + header check) ----------------
def viewer(request: Request) -> dict:
    pid = request.headers.get("x-ms-client-principal-id")
    if not pid:
        raise HTTPException(401, "no authenticated principal (Easy Auth header missing)")
    return {"id": pid, "name": request.headers.get("x-ms-client-principal-name", ""),
            "is_kam": bool(KAM_OBJECT_ID) and pid == KAM_OBJECT_ID}

def kam_only(request: Request) -> dict:
    """The write path: the Easy Auth principal must BE Kam (object id pinned by app setting). Anyone else -> 403, empty."""
    who = viewer(request)
    if not who["is_kam"]:
        log.warning("kam route refused: principal %s is not KAM_OBJECT_ID", who["id"][:8])
        raise HTTPException(403, "only Kam's principal may write here")
    return who

@app.get("/api/me")
def me(request: Request):
    return viewer(request)

@app.get("/api/messages")
def get_messages(request: Request, client: Optional[str] = None, since: Optional[str] = None, limit: int = Query(200, le=1000), hidden: int = Query(0, ge=0, le=1)):
    viewer(request)
    clients = {client} if client in READ_PARTITIONS else set(READ_PARTITIONS)
    return {"messages": _query("messages", clients, since, limit, include_hidden=bool(hidden)), "hidden_included": bool(hidden)}   # 2026-09-22: hidden rows skipped unless ?hidden=1

@app.get("/api/cards")
def get_cards(request: Request, client: Optional[str] = None, since: Optional[str] = None, limit: int = Query(1000, le=1000)):
    viewer(request)
    clients = {client} if client in READ_PARTITIONS else set(READ_PARTITIONS)
    return {"cards": _query("cards", clients, since, limit)}

@app.post("/api/kam/messages", status_code=201)
async def kam_post_message(request: Request):
    """Kam's reply from the live site. The BROWSER encrypts to his public key (this server never sees the prose);
    `view` is the tab he typed in and fixes the partition. The body's `client` must agree (the AAD binds it)."""
    who = kam_only(request)
    body = await request.json()
    view = str(body.get("view") or "")
    if view not in VIEW_TO_CLIENT: raise HTTPException(400, f"view must be one of {sorted(VIEW_TO_CLIENT)}")
    client = VIEW_TO_CLIENT[view]
    if body.get("client") not in (None, client): raise HTTPException(400, f"client for view={view} is {client}")
    env = validate_envelope(body, require_seat_kids_for=client)
    ts, rid = validate_clear(body, "message")
    row = {"PartitionKey": client, "RowKey": f"{ts}_{rid}", "kind": "message", "id": rid, "ts": ts, "view": view,
           "role": "kam", "seat": "kam", "written_by": f"easyauth:{who['id']}", "written_at": now_iso(), **env}
    stored = {"client": client, "id": rid, "ts": ts, "row_key": row["RowKey"], "written_by": "kam"}
    if insert_message(row):
        return {"stored": stored}
    return JSONResponse(status_code=200, content={"stored": stored, "duplicate": True})

@app.get("/api/usage")
def get_usage(request: Request):
    """The agent chips' figures: {wednesday: {pct, resets_in, reading_ts, age_seconds, ...}|null, tuesday: ...} — the local
    /api/usage shape. The age is SERVED, never hidden; the page renders 'no reading' past its threshold (WED-73)."""
    viewer(request)
    return usage_rows()

@app.get("/api/pubkey")
def pubkey(request: Request):
    viewer(request)
    return PlainTextResponse(open(PUBKEY_PATH).read())

@app.get("/api/pubkeys")
def pubkeys(request: Request):
    """Phase 3: Kam's key ring + the seat PUBLIC keys (with kids) — what the page wraps his replies to, and how it names the
    device key it holds. Public material only; there is still no route that accepts or returns a private key."""
    viewer(request)
    return public_keys()

NO_STORE = {"Cache-Control": "no-store"}

@app.get("/")
def index(request: Request):
    viewer(request)
    return FileResponse(os.path.join(HERE, "static", "index.html"), headers=NO_STORE)

@app.get("/chat")
def chat(request: Request):
    viewer(request)
    return FileResponse(os.path.join(HERE, "static", "chat.html"), headers=NO_STORE)

@app.get("/static/common.js")
def common_js(request: Request):
    viewer(request)
    return FileResponse(os.path.join(HERE, "static", "common.js"), media_type="application/javascript", headers=NO_STORE)

@app.get("/{path:path}")
def catch_all(path: str, request: Request):
    viewer(request)
    raise HTTPException(404, "no such page")
