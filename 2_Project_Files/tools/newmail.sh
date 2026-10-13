#!/bin/bash
# newmail.sh - prints the WHOLE body of every INBOUND/QUESTION/WRAP/OTHER row of wednesday-agent@ whose message id is not in
# the seen-ids file, then records those ids. Written 2026-10-13 after a minute-window filter missed a mail that arrived after
# the fetch bearing an earlier stamp (ledger row 2026-10-13, "MINUTE-WINDOW"). A SEEN-ID set, never a time window.
# First run on a fresh seat: seed the file with `bash newmail.sh --seed` AFTER reading the boot inbox whole.
W="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
D="${WED_NEWMAIL_DIR:-/private/tmp/wed_newmail}"; mkdir -p "$D"
set -a; . "$W/4_Credentials/.env"; set +a
bash "$W/2_Project_Files/fleet/inbox_digest.sh" --all > "$D/inbox_cur.txt" 2>&1
touch "$D/seen_ids.txt"
SEED=0; [ "${1:-}" = "--seed" ] && SEED=1
/usr/bin/grep -n -i -E '^\[(INBOUND|QUESTION|WRAP|OTHER)\]' "$D/inbox_cur.txt" | while IFS=: read -r n rest; do
  ID=$(sed -n "$((n+2))p" "$D/inbox_cur.txt" | sed 's/.*id: //')
  case "$ID" in "<"*) ;; *) continue;; esac
  if ! /usr/bin/grep -q -F -- "$ID" "$D/seen_ids.txt"; then
    if [ "$SEED" = 0 ]; then
      ENC=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$ID")
      echo "=========== $rest" | cut -c1-200
      curl -s -m 30 -H "Authorization: Bearer $AGENTMAIL_API_KEY" "https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages/$ENC" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('subject'));print(d.get('text') or d.get('preview'))"
    fi
    echo "$ID" >> "$D/seen_ids.txt"
  fi
done
echo "ROWS-IN-DIGEST: $(/usr/bin/grep -c -i -E '^\[(INBOUND|QUESTION|WRAP|OTHER)\]' "$D/inbox_cur.txt")  SEEN: $(wc -l < "$D/seen_ids.txt")"
