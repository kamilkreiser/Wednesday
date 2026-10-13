#!/bin/bash
# newmail.sh - prints every INBOUND/QUESTION/WRAP/OTHER row of wednesday-agent@ whose message id is not in the seen-ids file,
# then records those ids. A SEEN-ID set, never a time window (ledger 2026-10-13 "MINUTE-WINDOW").
#
# 2026-10-13 14:3x (ledger, inbox read through a frame, w=4): the bodies are long, I piped this through `head -c`, and the
# rows past the cut were RECORDED AS SEEN while never read (a READY FOR GATE sat 35 min). So now:
#   1. an INDEX of every new row (class, time, from, subject) is printed FIRST, one line each, before any body;
#   2. the full bodies are ALSO written to $D/batch_<UTC stamp>.txt, so a cut stdout loses nothing;
#   3. the last line says how many rows were new and where the batch file is.
# NEVER pipe this through head/tail/cut: read the index, then read the batch file by offset if a body is long.
# First run on a fresh seat: seed the file with `bash newmail.sh --seed` AFTER reading the boot inbox whole.
W="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
D="${WED_NEWMAIL_DIR:-/private/tmp/wed_newmail}"; mkdir -p "$D"
set -a; . "$W/4_Credentials/.env"; set +a
bash "${WED_NEWMAIL_DIGEST:-$W/2_Project_Files/fleet/inbox_digest.sh}" --all > "$D/inbox_cur.txt" 2>&1
DIGRC=$?
touch "$D/seen_ids.txt"
# 2026-10-13 23:3x (ledger "NEW-ROWS: 0 ROWS-IN-DIGEST: 0", a false zero hid J 10th's READY ~3 min): a digest with
# ZERO class rows is a FAILED read (the whole-inbox digest always holds rows), never "no new mail". Refuse loudly.
DIGROWS=$(/usr/bin/grep -c -i -E '^\[(INBOUND|QUESTION|WRAP|OTHER)\]' "$D/inbox_cur.txt")
if [ "$DIGROWS" -eq 0 ]; then
  echo "FAILED: the inbox digest held 0 class rows (inbox_digest rc=$DIGRC). This is NOT 'no new mail': re-read the inbox by the API before any sentence. Digest output, first 10 lines:"
  head -n 10 "$D/inbox_cur.txt"
  exit 3
fi
SEED=0; [ "${1:-}" = "--seed" ] && SEED=1
NEW="$D/new_rows.txt"; : > "$NEW"
/usr/bin/grep -n -i -E '^\[(INBOUND|QUESTION|WRAP|OTHER)\]' "$D/inbox_cur.txt" | while IFS=: read -r n rest; do
  ID=$(sed -n "$((n+2))p" "$D/inbox_cur.txt" | sed 's/.*id: //')
  case "$ID" in "<"*) ;; *) continue;; esac
  if ! /usr/bin/grep -q -F -- "$ID" "$D/seen_ids.txt"; then
    printf '%s\t%s\n' "$ID" "$rest" >> "$NEW"
  fi
done
COUNT=$(wc -l < "$NEW" | tr -d ' ')
BATCH="$D/batch_$(date -u +%Y%m%dT%H%M%SZ).txt"
if [ "$SEED" = 0 ] && [ "$COUNT" -gt 0 ]; then
  echo "NEW ROWS: $COUNT (index first; full bodies follow and are also in $BATCH)"
  cut -f2 "$NEW" | cut -c1-230 | nl -ba
  : > "$BATCH"
  while IFS="$(printf '\t')" read -r ID rest; do
    ENC=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$ID")
    { echo "=========== $rest" | cut -c1-200
      curl -s -m 30 -H "Authorization: Bearer $AGENTMAIL_API_KEY" "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages/$ENC" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('subject'));print(d.get('text') or d.get('preview'))"
    } >> "$BATCH"
  done < "$NEW"
  cat "$BATCH"
fi
cut -f1 "$NEW" >> "$D/seen_ids.txt"
echo "NEW-ROWS: $COUNT  ROWS-IN-DIGEST: $(/usr/bin/grep -c -i -E '^\[(INBOUND|QUESTION|WRAP|OTHER)\]' "$D/inbox_cur.txt")  SEEN: $(wc -l < "$D/seen_ids.txt")  BATCH: ${BATCH}"
