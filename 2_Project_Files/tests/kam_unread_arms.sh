#!/bin/bash
# Arms for kam_rulings_today.sh --unread + its read marker, and the chat_reply.sh advisory that uses them
# (Friday ledger w=2, 2026-09-29: Kam's 16:28 deploy GO sat unread ~2.5 h). Canned live-board replies only:
# no network, no post (chat_reply runs with CHAT_DRY=1). Each arm prints PASS/FAIL; exit 1 if any fail.
T="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../tools" && pwd)"; K="$T/kam_rulings_today.sh"
S="$(mktemp -d)"; F=0; P=0; N=0
DAY="$(date +%Y-%m-%d)"; YDAY="$(date -v-1d +%Y-%m-%d)"; OFF="$(date +%z | sed 's/\(..\)$/:\1/')"
row(){ printf '{"role":"kam","ts":"%sT%s%s","text":"%s","view":"%s","source":"live"}' "$DAY" "$1" "$OFF" "$2" "$3"; }
printf '[%s,%s]' "$(row 10:00:00 'first ruling' friday)" "$(row 11:00:00 'second message' friday)" > "$S/two.json"
printf '[%s,%s,%s]' "$(row 10:00:00 'first ruling' friday)" "$(row 11:00:00 'second message' friday)" "$(row 12:00:00 'Please publish the changes' friday)" > "$S/three.json"
printf '[%s,%s,%s]' "$(row 10:00:00 'first ruling' friday)" "$(row 11:00:00 'second message' friday)" "$(row 12:30:00 'for the other seat' tuesday)" > "$S/other.json"
printf 'not json' > "$S/broken.json"
export WED_AGENT=friday KAM_READ_MARKER="$S/marker"
k(){ KAM_RULINGS_LIVE_JSON_FILE="$1" bash "$K" "${@:2}" 2>&1; }
check(){ N=$((N+1)); if [ "$2" = yes ]; then echo "PASS  $1"; P=$((P+1)); else echo "FAIL  $1"; F=1; fi; [ -n "${3:-}" ] && echo "      $3"; }
has(){ case "$1" in *"$2"*) echo yes ;; *) echo no ;; esac; }

o="$(k "$S/two.json" --unread)"; check "a no marker: unread lists ALL of today's rows and says no read is recorded" "$( [ "$(has "$o" 'UNREAD 2 — no full read')" = yes ] && [ "$(has "$o" 'second message')" = yes ] && echo yes || echo no)" "$(echo "$o" | head -1)"
check "b --unread never creates the marker" "$( [ ! -e "$S/marker" ] && echo yes || echo no)"
k "$S/two.json" >/dev/null; check "c a full read records the newest SHOWN row" "$(has "$(cat "$S/marker" 2>/dev/null)" "${DAY}T11:00:00")" "marker=$(cat "$S/marker" 2>/dev/null)"
o="$(k "$S/two.json" --unread)"; check "d nothing new after a full read: UNREAD 0" "$(has "$o" 'UNREAD 0')" "$(echo "$o" | head -1)"
o="$(k "$S/three.json" --unread)"; check "e a newer row is shown by its text" "$( [ "$(has "$o" 'UNREAD 1')" = yes ] && [ "$(has "$o" 'Please publish the changes')" = yes ] && [ "$(has "$o" 'second message')" = no ] && echo yes || echo no)" "$(echo "$o" | tail -1)"
check "f --unread did not advance the marker" "$(has "$(cat "$S/marker")" "${DAY}T11:00:00")"
o="$(k "$S/other.json" --unread)"; check "g a newer row on the OTHER seat's tab is not this seat's unread" "$(has "$o" 'UNREAD 0')" "$(echo "$o" | head -1)"
printf '%sT23:00:00%s\n' "$YDAY" "$OFF" > "$S/marker"; o="$(k "$S/two.json" --unread)"; check "h yesterday's marker counts as no read today" "$(has "$o" 'UNREAD 2 — no full read')" "$(echo "$o" | head -1)"
k "$S/broken.json" --unread >/dev/null; rc=$?; check "i a broken board reply exits non-zero (chat_reply then says UNREADABLE, not 0)" "$( [ "$rc" != 0 ] && echo yes || echo no)" "rc=$rc"
# chat_reply integration (CHAT_DRY=1 writes nothing; the reconcile is skipped so no network is touched)
k "$S/two.json" >/dev/null
cr(){ CHAT_DRY=1 CHAT_REPLY_NO_RECONCILE=1 KAM_RULINGS_LIVE_JSON_FILE="$1" bash "$T/chat_reply.sh" --project Datasec "arm test message" 2>&1; }
o="$(cr "$S/three.json")"; rc=$?; check "j chat_reply prints the unread row LOUDLY and still exits 0" "$( [ "$rc" = 0 ] && [ "$(has "$o" 'KAM HAS WRITTEN SINCE YOUR LAST READ')" = yes ] && [ "$(has "$o" 'Please publish the changes')" = yes ] && echo yes || echo no)" "rc=$rc"
o="$(cr "$S/two.json")"; check "k chat_reply is silent when nothing is unread (and the DRY verdict still prints)" "$( [ "$(has "$o" 'KAM HAS WRITTEN')" = no ] && [ "$(has "$o" 'DRY')" = yes ] && echo yes || echo no)"
o="$(cr "$S/broken.json")"; rc=$?; check "l chat_reply says the read FAILED on a broken board, and still exits 0" "$( [ "$rc" = 0 ] && [ "$(has "$o" 'could not be read')" = yes ] && echo yes || echo no)" "rc=$rc"
mkdir -p "$S/_quarantine"; mv "$S"/*.json "$S/marker" "$S/_quarantine/" 2>/dev/null
echo "TOTAL: $P/$N passed   (scratch: $S)"
exit $F
