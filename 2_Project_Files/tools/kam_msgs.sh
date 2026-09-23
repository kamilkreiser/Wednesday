#!/bin/bash
# kam_msgs.sh — read Kam's recent panel messages WITH their metadata.
#
# WHY THIS EXISTS (2026-09-10, twice in one hour, both costing Kam):
#   1. His 08:58 message carried view="tuesday" — it was typed at the TUESDAY tab.
#      Wednesday read only .text, answered it as its own, and had to retract.
#   2. His 09:09 message was the four characters "now?" WITH the document he had
#      been asked for ATTACHED. Wednesday read only .text and told him a
#      four-character message could not tell it anything. He then exported a PDF
#      he did not need to make.
#
# Both are one failure: a panel message is a STRUCTURED RECORD (text + view +
# attachments) and reading one field of it is not reading the message. The
# routing data existed and was correct both times; the CONSUMER was missing —
# which is the same sentence the 2026-09-09 lesson wrote about `view`, and it
# was still true a day later because nothing was built.
#
# PHASE 3 (2026-09-21, Kam 12:50 "switch to using the live version only" / 14:05
# "interact normally while I'm traveling"): Kam now types on the LIVE board
# (https://wednesday-dashboard-e42e.azurewebsites.net). His rows there are
# encrypted to his keys AND to this seat's certificate key, so the seat reads them
# through dashboard-cloud/seat/get_kam_messages.py --decrypt (tools/_kam_live.sh).
#   NOTE the API caps rows PER PARTITION, oldest-first after --since: the live read
#   uses a 3-day window and the 1000 cap, and a partition that hits the cap is
#   WARNED on stderr (the newest rows are the ones cut). Older: --source local.
#   --source live   (DEFAULT) the live board, as $WED_AGENT; the API returns only
#                   this seat's partitions + his broadcasts, so a tuesday-tab row
#                   never reaches Wednesday's read (R0) — the view warning below
#                   still fires on any 'both'/foreign tag that does arrive.
#   --source local  the old chat_log.json (the local board — a fallback, and the
#                   only place his LOCAL-board replies land).
#   --source both   union of the two, de-duplicated on (UTC minute, text), each
#                   line tagged [live]/[local]. A live fetch failure is LOUD and
#                   exits 2 — never a quiet empty list that reads as "he said nothing".
# Live rows CARRY attachments since 2026-09-22 (the file drawer: Kam attaches on the live page; the bytes are encrypted to
# his ring + this seat's key). The att=N flag is real for [live] rows; --fetch-attachments <dir> downloads + decrypts them
# with this seat's key (dashboard-cloud/seat/get_files.py --fetch) and prints the local paths under each message.
#
# Usage: kam_msgs.sh [n] [--brief] [--source live|local|both] [--fetch-attachments <dir>]   last n Kam messages (default 6)
set -u
N=6; MODE=""; SOURCE="${KAM_MSGS_SOURCE:-live}"; FETCH_DIR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --brief) MODE="--brief" ;;
    --source) SOURCE="${2:-}"; shift ;;
    --source=*) SOURCE="${1#--source=}" ;;
    --fetch-attachments) FETCH_DIR="${2:-}"; [ -n "$FETCH_DIR" ] || { echo "kam_msgs: --fetch-attachments needs a directory" >&2; exit 2; }; shift ;;
    --*) echo "kam_msgs: unknown flag $1" >&2; exit 2 ;;
    *) N="$1" ;;
  esac; shift
done
case "$SOURCE" in live|local|both) ;; *) echo "kam_msgs: --source must be live|local|both (got '$SOURCE')" >&2; exit 2 ;; esac
ROOT="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LIVE_JSON="[]"
if [ "$SOURCE" != "local" ]; then
  . "$ROOT/2_Project_Files/tools/_kam_live.sh"
  # 3-day window, max cap: the API caps PER PARTITION oldest-first, so a wide window + small cap cuts the NEWEST rows
  # (measured 14:25 today: a 14-day/400 read lost the 02:48Z rows). get_kam_messages warns on stderr if a partition hits the cap.
  LIVE_JSON="$(kam_live_json --limit 1000 --since "$(date -u -v-3d +%Y-%m-%dT%H:%M 2>/dev/null || date -u +%Y-%m-%dT00:00)")" || exit 2
fi
FETCHED_JSON="{}"
if [ -n "$FETCH_DIR" ] && [ "$SOURCE" != "local" ]; then
  # the ids of the live rows shown are fetched with this seat's key; get_files.py prints one JSON, its rc is the fetch verdict
  _ids="$(printf '%s' "$LIVE_JSON" | python3 -c 'import json,sys;print(",".join(a["id"] for m in json.load(sys.stdin) for a in m.get("attachments",[])))')"
  if [ -n "$_ids" ]; then
    FETCHED_JSON="$("$ROOT/2_Project_Files/dashboard-cloud/.venv/bin/python" "$ROOT/2_Project_Files/dashboard-cloud/seat/get_files.py" --seat "${WED_AGENT:-}" --cert-dir "$ROOT/4_Credentials/dashboard-cloud" --ids "$_ids" --fetch "$FETCH_DIR" --json ${KAM_LIVE_BASE:+--base "$KAM_LIVE_BASE"} ${KAM_LIVE_INCLUDE_SYNTHETIC:+--include-synthetic} 2>"$FETCH_DIR.kam_msgs_fetch.err")" || echo "kam_msgs: ⚠️  attachment fetch reported failures (see $FETCH_DIR.kam_msgs_fetch.err)" >&2
  fi
fi
python3 - "$ROOT" "$N" "$MODE" "$SOURCE" "$LIVE_JSON" "$FETCHED_JSON" <<'PY'
import json,sys,os,datetime
root,n,mode,source,live_json=sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5]
try: fetched={f["id"]:f for f in json.loads(sys.argv[6]).get("files",[])}
except Exception: fetched={}
def utc_minute(ts):
    try: return datetime.datetime.fromisoformat(str(ts).replace("Z","+00:00")).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M")
    except Exception: return str(ts)[:16]
rows=[]
if source in ("local","both"):
    p=os.path.join(root,'0_Brain/dashboard/data/chat_log.json')
    d=json.load(open(p)); msgs=d if isinstance(d,list) else d.get('messages',d)
    for m in msgs:
        if m.get('role')=='kam': rows.append(dict(m, source='local'))
if source in ("live","both"):
    rows.extend(json.loads(live_json))
# de-dup (both): a backfilled live row IS the local message; same UTC minute + same text = one message
if source=="both":
    seen={}; out=[]
    for m in rows:
        k=(utc_minute(m.get('ts','')), " ".join(str(m.get('text','')).split()))
        if k in seen: continue
        seen[k]=1; out.append(m)
    rows=out
rows.sort(key=lambda m: utc_minute(m.get('ts','')))
ks=rows[-n:]
print(f"# source={source}" + (f" · seat={os.environ.get('WED_AGENT','unset')}" if source!='local' else "") + f" · showing last {len(ks)} of {len(rows)} Kam messages")
if not ks: print('no Kam messages found'); raise SystemExit(0)
for m in ks:
    ts=m.get('ts','')
    view=m.get('view') or '(none)'
    atts=m.get('attachments') or []
    text=str(m.get('text',''))
    src=m.get('source','local')
    # THE TWO FLAGS THAT WERE MISSED. Loud, because the failure was quiet.
    warn=''
    # FRIDAY SEAT (2026-09-23): for WED_AGENT=friday "addressed to me" is view=friday. Every other seat keeps the
    # original wednesday-relative reading byte-for-byte (the tuesday seat's reading is NOT changed here — see
    # fleet/REPORT_2026-09-23_friday-seat-tools.md: it flags her own view=tuesday rows too, a pre-existing gap).
    me='friday' if (os.environ.get('WED_AGENT') or '').strip().lower()=='friday' else 'wednesday'
    if view == 'both': warn += '  *** view=both — a BROADCAST: addressed to Wednesday AND Tuesday; she sees it too ***'
    elif view and view not in (me,'', None): warn += '  *** view=%s — NOT addressed to %s; route it, do not answer it ***' % (view, me.capitalize())
    if atts: warn += '  *** %d ATTACHMENT(S) — the message is not only its text ***' % len(atts)
    if m.get('decrypt_error'): warn += '  *** LIVE ROW NOT READABLE BY THIS SEAT (%s) — he wrote; read it on the live board ***' % m['decrypt_error']
    print('%s | [%s] view=%-10s | chars=%-5d | att=%d%s' % (ts, src, view, len(text), len(atts), warn))
    for a in atts:
        f=fetched.get(a.get('id'))
        if f and f.get('fetched'): print('      -> %s   FETCHED: %s' % ((f.get('meta') or {}).get('name','?'), f['fetched']))
        elif f and f.get('fetch_error'): print('      -> %s   FETCH FAILED: %s' % (a.get('id'), f['fetch_error']))
        else: print('      -> %s   %s' % (a.get('name','?'), a.get('path','?')))
    if mode != '--brief':
        print('  ' + (text if len(text) < 4000 else text[:4000] + ' …[TRUNCATED IN DISPLAY]'))
    print()
# A cap on the store is a frame: say so rather than let a full-length message read as complete.
capped=[m for m in ks if len(str(m.get('text','')))>=2000]
if capped: print('WARNING: %d of these are >=2000 chars — the OLD input cap was exactly 2000. If one ends mid-sentence it was truncated at source.' % len(capped))
PY
