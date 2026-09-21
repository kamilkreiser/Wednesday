#!/usr/bin/env python3
"""get_kam_messages.py — a SEAT reads what Kam typed on the live site (Phase 2; the cut-over successor of kam_msgs.sh).

GET /api/seat/messages?author=kam&since=<row_key>  with the seat's certificate token. The API returns Kam's rows from
THIS seat's partitions plus ALL (his broadcast/"both" rows) — Wednesday sees WED + Secuura + ALL, Tuesday sees Datasec +
ALL; the partition set comes from the token's roles, never from this script. Rows are CIPHERTEXT: a seat cannot read
Kam's prose (only Kam's private key can). What a seat gets is the clear routing: ts, view, id, client — enough to know
THAT he wrote, WHERE (which tab) and WHEN; the text itself reaches the seat by the local panel today (see the report,
piece D — cut-over is Kam's call).

Usage: get_kam_messages.py --seat wednesday [--since ROWKEY] [--limit 200] [--json]
"""
import argparse, sys, os, json
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc

if __name__ == "__main__":
    ids = sc.load_ids()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seat", choices=["wednesday", "tuesday"], required=True)
    ap.add_argument("--cert-dir", default="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud")
    ap.add_argument("--base", default=f"https://{ids.get('WEBAPP','')}.azurewebsites.net")
    ap.add_argument("--tenant", default=ids.get("TENANT_ID")); ap.add_argument("--api-appid", default=ids.get("API_APPID", ""))
    ap.add_argument("--since", default=None); ap.add_argument("--limit", type=int, default=200); ap.add_argument("--json", action="store_true")
    ap.add_argument("--client", default=None, help="one partition (must be in the seat's roles or ALL)")
    a = ap.parse_args()
    tok = sc.get_token(a, ids)
    params = {"author": "kam", "limit": a.limit}
    if a.since: params["since"] = a.since
    if a.client: params["client"] = a.client
    r = requests.get(a.base + "/api/seat/messages", params=params, headers={"Authorization": f"Bearer {tok}"}, timeout=30)
    if r.status_code != 200:
        sys.stderr.write(f"get_kam_messages: HTTP {r.status_code}: {r.text[:200]}\n"); sys.exit(1)
    d = r.json()
    if a.json: print(json.dumps(d, indent=1)); sys.exit(0)
    print(f"partitions readable by this seat: {d.get('clients')}  rows: {len(d.get('messages', []))}")
    for m in d.get("messages", []):
        print(f"{m.get('ts')} | client={m.get('client'):8} view={str(m.get('view')):10} id={m.get('id')} "
              f"{'backfill' if m.get('backfill') else 'live'} written_by={str(m.get('written_by'))[:20]}  [ciphertext {len(m.get('ciphertext',''))} b64 chars]")
