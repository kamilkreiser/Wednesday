#!/usr/bin/env python3
"""post_usage.py — publish THIS SEAT's weekly plan usage reading to the live board (2026-09-22).

Kam, on the live board 08:57:36: "with the local version, I was able to see the weekly usage count on both Wednesday and
Tuesday. Is this possible for the live version?"

Reads the seat's own usage_<seat>.json (written by tools/statusline_publish.sh on THIS machine — the figure reaches that
script on stdin from Claude Code and exists nowhere else) and POSTs it to POST /api/seat/usage as the seat, with the
seat's certificate token. The server attributes the row by the TOKEN (never the body), so this script cannot publish
another seat's number even if pointed at the other seat's file — and it refuses that locally first (the file's `agent`
must equal --seat).

Publishes NOTHING, and says why, when the file is missing, unreadable, names another seat, or its reading is older than
--max-age (default 1800 s = the page's "no reading" threshold; a seat that is not running stops writing its file, and a
stale figure republished as fresh would be exactly the faked state WED-73 forbids). The last stdout line is always
`rc=<n>`: 0 published (200/201) · 1 the API refused or is unreachable · 2 refused locally (seat/cert) · 3 nothing to
publish (missing/stale/unreadable file). Idempotent: the row is state (REPLACE, last write wins — this is the ONE publisher for the seat), so running this
every few minutes is safe; success is judged on the server's `stored` echo, never assumed from the status code.

Usage: post_usage.py --seat wednesday [--file PATH] [--max-age 1800] [--dry-run] [--token-only]
"""
import argparse, datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc

TREE_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))   # seat/ -> dashboard-cloud/ -> 2_Project_Files/ -> <tree>

def finish(rc: int, msg: str) -> int:
    print(msg); print(f"rc={rc}"); return rc

def main() -> int:
    ids = sc.load_ids()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seat", choices=["wednesday", "tuesday"], required=True, help="which seat identity (the launcher's word: $WED_AGENT / the tree name)")
    p.add_argument("--cert-dir", default=sc.DEFAULT_CERT_DIR, help="dir holding <seat>-seat.pem + .crt (default: THIS tree's 4_Credentials/dashboard-cloud)")
    p.add_argument("--file", default=None, help="the reading (default: <tree>/0_Brain/dashboard/data/usage_<seat>.json)")
    p.add_argument("--max-age", type=int, default=1800, help="seconds; an older reading is NOT published (default 1800)")
    p.add_argument("--base", default=f"https://{ids.get('WEBAPP','')}.azurewebsites.net")
    p.add_argument("--tenant", default=ids.get("TENANT_ID", sc.DEFAULT_TENANT))
    p.add_argument("--api-appid", default=ids.get("API_APPID", ""))
    p.add_argument("--dry-run", action="store_true", help="print the request body; no token, no HTTP")
    p.add_argument("--token-only", action="store_true", help="get a token and print its claims (no secrets); no HTTP to the app")
    a = p.parse_args()

    path = a.file or os.path.join(TREE_ROOT, "0_Brain", "dashboard", "data", f"usage_{a.seat}.json")
    if not os.path.isfile(path):
        return finish(3, f"NOTHING TO PUBLISH: no reading at {path} (the seat's statusline has not written one on this machine)")
    try:
        d = json.load(open(path))
    except Exception as e:
        return finish(3, f"NOTHING TO PUBLISH: {path} unreadable ({type(e).__name__})")
    if str(d.get("agent", "")) != a.seat:
        return finish(2, f"REFUSED locally: {path} names seat '{d.get('agent')}', not '{a.seat}' — a seat publishes ONLY its own reading")
    pct = d.get("pct")
    if isinstance(pct, bool) or not isinstance(pct, (int, float)) or not (0 <= float(pct) <= 100):
        return finish(3, f"NOTHING TO PUBLISH: pct {pct!r} is not a number 0..100")
    ts = str(d.get("ts", ""))
    try:
        t = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return finish(3, f"NOTHING TO PUBLISH: ts {ts!r} is not ISO-8601 UTC seconds")
    age = int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds())
    if age > a.max_age:
        return finish(3, f"NOTHING TO PUBLISH: reading is {age}s old (> {a.max_age}s) — the {a.seat} seat may not be running; the live board keeps its last row and shows its age")
    if age < -300:
        return finish(3, f"NOTHING TO PUBLISH: reading ts {ts} is in the future by {-age}s (clock?)")
    body = {"seat": a.seat, "pct": int(round(float(pct))), "resets_in": str(d.get("resets_in") or "")[:32], "ts": ts}
    if a.dry_run:
        print(json.dumps({"DRY_RUN": True, "url": a.base + "/api/seat/usage", "body": body, "reading_age_s": age}, indent=1)); return finish(0, "dry run: nothing sent")
    for ext in ("pem", "crt"):
        if not os.path.isfile(os.path.join(a.cert_dir, f"{a.seat}-seat.{ext}")):
            return finish(2, f"REFUSED locally: no {a.seat}-seat.{ext} in {a.cert_dir} (PORTABILITY.md)")
    try:
        tok = sc.get_token(a, ids)
    except SystemExit:
        return finish(1, "token FAILED (see stderr)")
    if a.token_only:
        c = sc.claims_of(tok); print(json.dumps({k: c.get(k) for k in ("aud", "azp", "roles", "tid", "exp")}, indent=1)); return finish(0, "token only")
    import requests
    try:
        r = requests.post(a.base + "/api/seat/usage", json=body, headers={"Authorization": f"Bearer {tok}"}, timeout=30)
    except requests.RequestException as e:
        return finish(1, f"POST failed: {type(e).__name__}")
    print(json.dumps({"status": r.status_code, "body": r.text[:300]}))
    if r.status_code in (200, 201):
        try: stored = r.json().get("stored", {})
        except Exception: stored = {}
        if stored.get("pct") != body["pct"] or stored.get("reading_ts") != ts:   # the server's word, not this script's assumption
            return finish(1, f"API answered HTTP {r.status_code} but STORED {stored} != sent {body['pct']}% @ {ts}")
        return finish(0, f"published {a.seat} {body['pct']}% (reading {age}s old, renews in '{body['resets_in']}') HTTP {r.status_code}")
    return finish(1, f"API refused HTTP {r.status_code}")

if __name__ == "__main__":
    sys.exit(main())
