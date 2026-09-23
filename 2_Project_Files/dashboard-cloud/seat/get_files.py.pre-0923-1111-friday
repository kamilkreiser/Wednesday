#!/usr/bin/env python3
"""get_files.py — a SEAT lists the live board's file drawer and fetches (decrypts) files (2026-09-22).

GET /api/seat/files[?client=&since=]  with the seat's certificate token: the ready file rows of this seat's partitions + ALL —
Kam's uploads (direction=upload) and the seats' shares (direction=shared). The meta (name, note, size, sha256, mime) is
decrypted with <seat>-seat.pem; a row not wrapped to this seat is reported, never guessed.
--fetch <dir>: downloads GET /api/seat/files/<client>/<row_key>/blob, decrypts with the seat key (envelope.decrypt_file),
verifies the plaintext sha256 against the meta and writes <dir>/<id>_<name>. Nothing is overwritten (an existing target is
reported and skipped). Every download is audited by the server.

Usage: get_files.py --seat wednesday [--since ROWKEY] [--client X] [--ids id1,id2] [--fetch DIR] [--json] [--include-synthetic]
"""
import argparse, hashlib, json, os, sys, datetime
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc, envelope

def main():
    ids = sc.load_ids()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seat", choices=["wednesday", "tuesday"], required=True)
    ap.add_argument("--cert-dir", default=sc.DEFAULT_CERT_DIR)
    ap.add_argument("--base", default=f"https://{ids.get('WEBAPP','')}.azurewebsites.net")
    ap.add_argument("--tenant", default=ids.get("TENANT_ID")); ap.add_argument("--api-appid", default=ids.get("API_APPID", ""))
    ap.add_argument("--since", default=None); ap.add_argument("--limit", type=int, default=200); ap.add_argument("--client", default=None)
    ap.add_argument("--ids", default=None, help="comma-separated file ids to keep (e.g. a message row's attachments)")
    ap.add_argument("--fetch", default=None, help="directory to write the DECRYPTED files into")
    ap.add_argument("--json", action="store_true"); ap.add_argument("--include-synthetic", action="store_true")
    a = ap.parse_args()
    tok = sc.get_token(a, ids); H = {"Authorization": f"Bearer {tok}"}
    params = {"limit": a.limit}
    if a.since: params["since"] = a.since
    if a.client: params["client"] = a.client
    r = requests.get(a.base + "/api/seat/files", params=params, headers=H, timeout=30)
    if r.status_code != 200:
        sys.stderr.write(f"get_files: HTTP {r.status_code}: {r.text[:200]}\n"); print("rc=1"); return 1
    d = r.json(); rows = d.get("files", [])
    if not a.include_synthetic: rows = [x for x in rows if x.get("synthetic") is not True]
    if a.ids:
        want = set(a.ids.split(",")); rows = [x for x in rows if x.get("id") in want]
    priv = envelope.load_private(os.path.join(a.cert_dir, f"{a.seat}-seat.pem"))
    fetched = 0; failed = 0
    for x in rows:
        clear = {"client": x["client"], "kind": "file", "id": x["id"], "ts": x["ts"]}
        try: x["meta"] = json.loads(envelope.decrypt_text(priv, x, clear))
        except KeyError: x["decrypt_error"] = "not wrapped to this seat"
        except Exception as e: x["decrypt_error"] = f"decrypt failed: {type(e).__name__}"
        if a.fetch and "meta" in x:
            os.makedirs(a.fetch, exist_ok=True)
            safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in str(x["meta"].get("name") or "file"))[:120]
            target = os.path.join(a.fetch, f"{x['id']}_{safe}")
            if os.path.exists(target): x["fetched"] = target; x["fetch_note"] = "exists, not overwritten"; continue
            rb = requests.get(f"{a.base}/api/seat/files/{x['client']}/{x['row_key']}/blob", headers=H, timeout=300)
            if rb.status_code != 200: x["fetch_error"] = f"HTTP {rb.status_code}"; failed += 1; continue
            try:
                pt = envelope.decrypt_file(priv, x, clear, rb.content)
            except Exception as e:
                x["fetch_error"] = f"blob decrypt failed: {type(e).__name__}"; failed += 1; continue
            if hashlib.sha256(pt).hexdigest() != x["meta"].get("sha256"): x["fetch_error"] = "plaintext sha256 mismatch"; failed += 1; continue
            with open(target, "wb") as f: f.write(pt)
            x["fetched"] = target; fetched += 1
        for k in ("ciphertext", "wrapped_key", "wrapped_keys", "iv", "iv_blob", "kid", "scheme"): x.pop(k, None)
    if a.json: print(json.dumps({"files": rows, "clients": d.get("clients"), "fetched": fetched, "failed": failed}, indent=1, ensure_ascii=False)); return 0 if not failed else 1
    print(f"partitions {d.get('clients')}: {len(rows)} file(s)" + (f"; fetched {fetched}, failed {failed} -> {a.fetch}" if a.fetch else ""))
    for x in rows:
        m = x.get("meta") or {}
        print(f"  {x.get('ts')} | {x.get('client'):8} {x.get('direction'):7} by={x.get('seat')} id={x.get('id')} size={x.get('size')} "
              + (f"name={m.get('name')!r} note={m.get('note')!r}" if m else f"[{x.get('decrypt_error')}]") + (f" -> {x['fetched']}" if x.get("fetched") else "") + (f" FETCH FAILED: {x['fetch_error']}" if x.get("fetch_error") else ""))
    print(f"rc={0 if not failed else 1}"); return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())
