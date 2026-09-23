#!/usr/bin/env python3
"""share_file.py — a SEAT shares a file with Kam through the live board's file drawer (2026-09-22).

Kam, live board 15:26:48: "create a download button next to autoplay replies and stop so that if I ask for a file to be
shared, you can share it with me and place it there and I can download it at a later stage from the live site".

The file is encrypted HERE before it leaves this machine (seat/envelope.encrypt_file): one AES-256-GCM data key over the
bytes (the blob) and over a small meta JSON {name, note, size, sha256, mime} (the row's ciphertext), wrapped to Kam's whole
key ring + this partition's seat key — the same recipient set as a message. The server stores ciphertext it cannot read.
Two calls: POST /api/seat/files (the row, pending) -> PUT /api/seat/files/<client>/<row_key>/blob (the bytes; the server
checks size + sha256 of the CIPHERTEXT and marks the row ready). The API takes the partition from the TOKEN's roles —
--client outside them -> 403 (the wednesday seat cannot share into Datasec, exactly as post_message.py).

Usage: share_file.py <path> [--note "..."] [--client WED|Secuura|Datasec] [--seat wednesday] [--msg-id ID] [--synthetic] [--dry-run]
Prints `file_id=<id> row_key=<rk> client=<c> size=<n> drawer=<url>` and, last, `rc=<n>`: 0 ready · 1 the API refused / unreachable ·
2 refused locally (missing file, over the bound) · 3 the bytes were refused after the row was created (row stays pending, never listed).
"""
import argparse, hashlib, json, mimetypes, os, sys
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc, envelope

FILE_MAX = 32 * 1024 * 1024   # ciphertext bound, mirrors app/main.py FILE_MAX

def finish(rc, msg):
    print(msg); print(f"rc={rc}"); return rc

def main():
    ids = sc.load_ids()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path")
    p.add_argument("--note", default="", help="one line shown in the drawer (encrypted, <=300 chars)")
    p.add_argument("--seat", choices=["wednesday", "tuesday"], default=os.environ.get("WED_AGENT") or "wednesday")
    p.add_argument("--client", choices=["Secuura", "Datasec", "WED"], default=None, help="partition (default: the seat's home partition; the API refuses one outside the token)")
    p.add_argument("--cert-dir", default=sc.DEFAULT_CERT_DIR)
    p.add_argument("--base", default=f"https://{ids.get('WEBAPP','')}.azurewebsites.net")
    p.add_argument("--tenant", default=ids.get("TENANT_ID", sc.DEFAULT_TENANT)); p.add_argument("--api-appid", default=ids.get("API_APPID", ""))
    p.add_argument("--msg-id", default=None, help="the message row this file belongs to (clear linkage)")
    p.add_argument("--id", default=None); p.add_argument("--synthetic", action="store_true"); p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    if not a.client: a.client = {"wednesday": "WED", "tuesday": "Datasec"}[a.seat]
    if not os.path.isfile(a.path): return finish(2, f"REFUSED locally: no such file {a.path}")
    data = open(a.path, "rb").read()
    if len(data) + 16 > FILE_MAX: return finish(2, f"REFUSED locally: {len(data)} bytes + 16 > the bound {FILE_MAX}")
    if len(data) == 0: return finish(2, "REFUSED locally: empty file")
    import datetime, uuid
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    rid = a.id or ("f-" + uuid.uuid4().hex[:10])
    clear = {"client": a.client, "kind": "file", "id": rid, "ts": ts}
    meta = {"name": os.path.basename(a.path)[:200], "note": a.note[:300], "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "mime": mimetypes.guess_type(a.path)[0] or "application/octet-stream"}
    env, ct = envelope.encrypt_file(data, meta, clear)
    assert meta["name"] not in json.dumps(env) or len(meta["name"]) < 8, "name leaked into envelope"
    body = {**clear, "view": "wednesday" if a.seat == "wednesday" else "tuesday", "role": a.seat, "size": len(ct), "sha256": hashlib.sha256(ct).hexdigest(),
            "iv_blob": env.pop("iv_blob"), "envelope": env}
    if a.msg_id: body["msg_id"] = a.msg_id
    if a.synthetic: body["synthetic"] = True
    if a.dry_run:
        print(json.dumps({"DRY_RUN": True, "url": a.base + "/api/seat/files", "body": body, "blob_bytes": len(ct)}, indent=1)); return finish(0, "dry run — nothing sent")
    tok = sc.get_token(a, ids); H = {"Authorization": f"Bearer {tok}"}
    try:
        r = requests.post(a.base + "/api/seat/files", json=body, headers=H, timeout=30)
    except requests.RequestException as e:
        return finish(1, f"UNREACHABLE: {type(e).__name__}")
    print(json.dumps({"status": r.status_code, "body": r.text[:400]}, indent=1))
    if r.status_code != 201: return finish(1, f"row REFUSED: HTTP {r.status_code}")
    rk = r.json()["stored"]["row_key"]
    r2 = requests.put(f"{a.base}/api/seat/files/{a.client}/{rk}/blob", data=ct, headers={**H, "Content-Type": "application/octet-stream"}, timeout=300)
    print(json.dumps({"status": r2.status_code, "body": r2.text[:400]}, indent=1))
    if r2.status_code != 200: return finish(3, f"bytes REFUSED: HTTP {r2.status_code} (row {rk} stays pending; it is never listed)")
    return finish(0, f"file_id={rid} row_key={rk} client={a.client} size={len(data)} drawer={a.base}/chat#files")

if __name__ == "__main__":
    sys.exit(main())
