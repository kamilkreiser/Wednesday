#!/bin/bash
# _kam_live.sh — sourced by kam_msgs.sh / kam_rulings_today.sh: fetch Kam's LIVE-BOARD rows as this seat, decrypted, in the
# LOCAL message shape. Phase 3 of the external dashboard (Kam 12:50:55 2026-09-21: "switch to using the live version only";
# 14:05:04: "so that we can interact normally while I'm traveling").
#
# WHAT IT DOES: runs dashboard-cloud/seat/get_kam_messages.py --seat $WED_AGENT --decrypt --json [--since ROWKEY] with the
# dashboard-cloud venv python, and prints ONE JSON list of {role:"kam", ts:<local ISO with offset>, utc, view, text,
# attachments:[], client, id, row_key, source:"live"} — the shape the local readers already parse. Rows the seat cannot
# open (not wrapped to it) come through with text "" and decrypt_error set, never dropped: the caller sees THAT he wrote.
#
# WHAT IT REFUSES: no WED_AGENT -> refuse (a seat that guesses reads the other seat's tab — 2026-09-09 seat-resolver lesson;
# the API's token decides the partitions, so the seat name here only picks the certificate, but a wrong pick is still a
# wrong read). No venv / no certificate / HTTP failure -> a LOUD line on stderr and exit 2. NEVER a quiet empty list: an
# empty list must mean "he wrote nothing", not "the fetch failed" (the 2026-09-07 stale-copy lesson, on a new source).
#
# Usage (sourced):  kam_live_json [--since ROWKEY] [--limit N]   -> JSON on stdout; rc 0 ok / 2 refused or failed
_kl_root() { cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd; }
kam_live_json() {
  local root; root="$(_kl_root)"
  local seat="${WED_AGENT:-}"
  case "$seat" in wednesday|tuesday) ;; *) echo "kam-live: 🔴 REFUSED — WED_AGENT is '${seat:-unset}' (neither wednesday nor tuesday); a guessed seat reads the wrong tab. export WED_AGENT=… or use --source local" >&2; return 2 ;; esac
  local py="$root/2_Project_Files/dashboard-cloud/.venv/bin/python"
  [ -x "$py" ] || { echo "kam-live: 🔴 FAILED — no venv at 2_Project_Files/dashboard-cloud/.venv (PORTABILITY.md); use --source local" >&2; return 2; }
  [ -f "$root/4_Credentials/dashboard-cloud/$seat-seat.pem" ] || { echo "kam-live: 🔴 FAILED — no certificate 4_Credentials/dashboard-cloud/$seat-seat.pem on this machine; use --source local" >&2; return 2; }
  # --cert-dir is passed from THIS tree (never the tool's Studio default): the 2026-09-21 13:17 card-path bug on the mini was exactly a
  # missing --cert-dir, invisible on the Studio where the default equals the tree path (Wednesday, 15:0x).
  # the fetch + reshape run in ONE python so stderr is captured in-process (no temp file, nothing to delete)
  python3 - "$py" "$root/2_Project_Files/dashboard-cloud/seat/get_kam_messages.py" "$seat" "$root/4_Credentials/dashboard-cloud" "$@" <<'PYEOF'
import json, sys, subprocess
py, tool, seat, cert_dir, *rest = sys.argv[1:]
import os
extra = (["--base", os.environ["KAM_LIVE_BASE"]] if os.environ.get("KAM_LIVE_BASE") else []) + (["--include-synthetic"] if os.environ.get("KAM_LIVE_INCLUDE_SYNTHETIC") == "1" else [])   # 2026-09-22: loopback matrix affordances (08f); unset in normal use
r = subprocess.run([py, tool, "--seat", seat, "--cert-dir", cert_dir, "--decrypt", "--json", *extra, *rest], capture_output=True, text=True)
if r.returncode != 0 or not r.stdout.strip():
    sys.stderr.write("kam-live: 🔴 FAILED — get_kam_messages.py rc=%d: %s\n" % (r.returncode, " ".join(r.stderr.split())[:300]))
    sys.exit(2)
d = json.loads(r.stdout); out = []
skipped = 0
for m in d.get("messages", []):
    if m.get("synthetic") in (True, "true", "True") and os.environ.get("KAM_LIVE_INCLUDE_SYNTHETIC") != "1":
        skipped += 1; continue   # a probe row wearing role=kam is NOT Kam's word (Wednesday, 2026-09-21 15:0x)
    out.append({"role": "kam", "ts": m.get("ts_local") or m.get("ts"), "utc": m.get("ts"), "view": m.get("view"), "text": m.get("text", ""),
                "attachments": [{"id": a, "name": "(live file %s — encrypted; kam_msgs.sh --fetch-attachments <dir>)" % a, "path": "live:%s/%s" % (m.get("client"), a)} for a in (m.get("attachments") or []) if isinstance(a, str)],   # 2026-09-22 file drawer
                "client": m.get("client"), "id": m.get("id"), "row_key": m.get("row_key"), "source": "live",
                **({"decrypt_error": m["decrypt_error"]} if m.get("decrypt_error") else {})})
if skipped: sys.stderr.write("kam-live: %d synthetic (probe) row(s) skipped — not Kam's word\n" % skipped)
print(json.dumps(out, ensure_ascii=False))
PYEOF
}
