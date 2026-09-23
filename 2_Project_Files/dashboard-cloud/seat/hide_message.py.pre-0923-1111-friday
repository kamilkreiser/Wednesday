#!/usr/bin/env python3
"""hide_message.py — a SEAT hides (or unhides) a message row of ITS OWN tab on the live board (2026-09-22).

Kam, on the Tuesday tab 14:27:09: "Please clean up your boards so you don't have any local model workloads at this stage."
The live board had no hide route; rows were only ever added. This is the reversible one:

  POST /api/seat/hide    {client, row_key | id, reason}   -> the row gains hidden=true (+ hidden_by/at/seat, MERGED onto the
  POST /api/seat/unhide  {client, row_key | id, reason}      row: envelope and every other column untouched); an AUDIT row is
                                                            appended in the same table (PartitionKey AUDIT). NOTHING IS DELETED.
  GET  /api/seat/hide/audit                                 -> the audit rows for this seat's partitions
  GET  /api/seat/messages?hidden=1                          -> the reveal (hidden rows listed with their hidden_* columns)

The server allows a hide ONLY for a partition the seat's token grants (R0, exactly as a write): the tuesday seat may hide
Datasec (`tuesday`-tab) rows, the wednesday seat WED/Secuura rows, nobody ALL. This script cannot widen that — it only
chooses which certificate signs the request (--seat), and the token's roles decide.

Usage:
  hide_message.py --seat tuesday --client Datasec --row-key 2026-09-21T03:23:01.079Z_bf-af542c5dc54b942b076d --reason "…"
  hide_message.py --seat tuesday --client Datasec --id bf-af542c5dc54b942b076d --unhide
  hide_message.py --seat tuesday --client Datasec --list-hidden          (the ?hidden=1 reveal, hidden rows only, no text)
  hide_message.py --seat tuesday --audit                                 (audit rows this seat may see)
The last stdout line is always `rc=<n>`: 0 done (200) · 1 the API refused (403/404/409/400 — the body is printed) or unreachable ·
2 refused locally (token). --dry-run prints the request and sends nothing.
"""
import argparse, json, os, sys
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seat_common as sc

def finish(rc: int, msg: str) -> int:
    print(msg); print(f"rc={rc}"); return rc

def main() -> int:
    ids = sc.load_ids()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seat", choices=["wednesday", "tuesday"], required=True, help="which certificate signs the request; the token's roles decide what may be hidden")
    p.add_argument("--cert-dir", default=sc.DEFAULT_CERT_DIR)
    p.add_argument("--client", choices=["Secuura", "Datasec", "WED"], default=None, help="the row's partition (tuesday tab = Datasec, wednesday tab = WED / Secuura)")
    p.add_argument("--row-key", default=None, help="<ISO UTC ts>_<id> — exact")
    p.add_argument("--id", default=None, help="the row's id (must match exactly one row in the partition)")
    p.add_argument("--reason", default="", help="<=160 chars [A-Za-z0-9 ._:/()+'-]; goes to the audit row, never the message")
    p.add_argument("--unhide", action="store_true", help="reverse a hide (the same call shape, action=unhide)")
    p.add_argument("--list-hidden", action="store_true", help="GET /api/seat/messages?hidden=1 (for --client or all of the seat's partitions) and print ONLY the hidden rows (clear columns, no text)")
    p.add_argument("--audit", action="store_true", help="GET /api/seat/hide/audit")
    p.add_argument("--since", default=None, help="with --list-hidden: RowKey floor")
    p.add_argument("--base", default=f"https://{ids.get('WEBAPP','')}.azurewebsites.net")
    p.add_argument("--tenant", default=ids.get("TENANT_ID", sc.DEFAULT_TENANT))
    p.add_argument("--api-appid", default=ids.get("API_APPID", ""))
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    if a.list_hidden or a.audit:
        tok = sc.get_token(a, ids)
        if a.audit:
            r = requests.get(a.base + "/api/seat/hide/audit", params={"limit": 1000}, headers={"Authorization": f"Bearer {tok}"}, timeout=30)
            if r.status_code != 200: return finish(1, f"HTTP {r.status_code}: {r.text[:300]}")
            d = r.json(); rows = d.get("audit", [])
            print(f"audit rows visible to the {a.seat} seat (partitions {d.get('clients')}): {len(rows)}")
            for e in rows:
                print(f"  {e.get('at')} {e.get('action'):6} {e.get('target_client')}/{e.get('target_row_key')} by seat={e.get('seat')} changed={e.get('changed')} reason={e.get('reason')!r}")
            return finish(0, f"{len(rows)} audit row(s)")
        params = {"limit": 1000, "hidden": 1}
        if a.client: params["client"] = a.client
        if a.since: params["since"] = a.since
        r = requests.get(a.base + "/api/seat/messages", params=params, headers={"Authorization": f"Bearer {tok}"}, timeout=30)
        if r.status_code != 200: return finish(1, f"HTTP {r.status_code}: {r.text[:300]}")
        d = r.json(); rows = d.get("messages", []); hid = [m for m in rows if m.get("hidden") is True]
        print(f"partitions {d.get('clients')}: {len(rows)} rows listed with hidden=1, of which HIDDEN: {len(hid)}")
        for m in hid:
            print(f"  {m.get('client')}/{m.get('row_key')} view={m.get('view')} hidden_at={m.get('hidden_at')} hidden_seat={m.get('hidden_seat')} src_ts={m.get('src_ts')}")
        return finish(0, f"{len(hid)} hidden row(s)")

    if not a.client: return finish(2, "REFUSED locally: --client is required for hide/unhide")
    if not (a.row_key or a.id): return finish(2, "REFUSED locally: --row-key or --id is required")
    body = {"client": a.client, "reason": a.reason}
    if a.row_key: body["row_key"] = a.row_key
    else: body["id"] = a.id
    path = "/api/seat/unhide" if a.unhide else "/api/seat/hide"
    if a.dry_run:
        print(json.dumps({"DRY_RUN": True, "url": a.base + path, "body": body}, indent=1)); return finish(0, "dry run — nothing sent")
    tok = sc.get_token(a, ids)
    try:
        r = requests.post(a.base + path, json=body, headers={"Authorization": f"Bearer {tok}"}, timeout=30)
    except requests.RequestException as e:
        return finish(1, f"UNREACHABLE: {type(e).__name__}")
    print(json.dumps({"status": r.status_code, "body": r.text[:600]}, indent=1))
    if r.status_code != 200: return finish(1, f"{'unhide' if a.unhide else 'hide'} REFUSED: HTTP {r.status_code}")
    d = r.json()
    return finish(0, f"{'unhidden' if a.unhide else 'hidden'}: {d['row']['client']}/{d['row']['row_key']} changed={d.get('changed')} audit={d.get('audit_row_key')} as seat={d.get('by')}")

if __name__ == "__main__":
    sys.exit(main())
