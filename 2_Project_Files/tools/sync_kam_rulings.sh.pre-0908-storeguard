#!/bin/bash
# sync_kam_rulings.sh — write Kam's panel rulings into the decision queue.
#
# WHY THIS EXISTS (ledger w=93, 2026-09-08, KAM-CAUGHT). Kam rules a card on the
# dashboard panel. The ruling lands in chat_log.json as text — "Decision <id>:
# <key> — <label>" — and NOTHING writes it into decisions.json. So the panel
# keeps showing the card as OPEN and re-serves it to him. On 2026-09-08 he ruled
# six cards between 07:07 and 07:10, answered five of them a SECOND time, and
# said so himself: "PS - I already ansered these above." At 10:19 he asked for it
# directly: "and clear fleet activity items once answered."
#
# Until now the bridge was a seat remembering to transcribe by hand. That works
# until a seat rotates mid-morning and the successor does not know to do it —
# which is the definition of a ritual nothing triggers
# (learnings/2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual.md).
#
# SAFETY, because this writes his decisions:
#   - It ONLY rules cards that are currently UNRULED. An already-ruled card is
#     never touched, so a second run cannot overwrite a ruling.
#   - It ONLY takes the choice key from HIS OWN message text. It never infers a
#     key, never picks a default, and never rules a card he wrote a NOTE on
#     without choosing an option (that is the hpsm-* case of 2026-09-08 07:08:23
#     — a note is not a ruling, and inventing a choice for him is worse than
#     leaving the card open).
#   - It refuses a key that is not one of that card's declared options.
#   - --dry-run prints what it WOULD do and writes nothing. Default IS dry-run;
#     --apply is required to write. A tool that writes his rulings should not do
#     so because someone typed its name.
#
# Usage: sync_kam_rulings.sh [--dry-run|--apply] [--since YYYY-MM-DD]
# Exit:  0 ok (with or without changes) · 2 usage · 3 missing input
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
W="$(cd -P "$SELF_DIR/../.." && pwd)"
CHAT="$W/0_Brain/dashboard/data/chat_log.json"
DQ="$SELF_DIR/decision_queue.sh"

MODE=dry
SINCE="$(date '+%Y-%m-%d')"
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) MODE=dry; shift ;;
    --apply)   MODE=apply; shift ;;
    --since)   SINCE="${2:?--since needs YYYY-MM-DD}"; shift 2 ;;
    *) echo "usage: sync_kam_rulings.sh [--dry-run|--apply] [--since YYYY-MM-DD]" >&2; exit 2 ;;
  esac
done
[ -s "$CHAT" ] || { echo "sync_kam_rulings: no chat log at $CHAT" >&2; exit 3; }
[ -x "$DQ" ] || [ -s "$DQ" ] || { echo "sync_kam_rulings: no decision_queue.sh at $DQ" >&2; exit 3; }

PLAN="$(python3 - "$CHAT" "$W/0_Brain/dashboard/data/decisions.json" "$SINCE" <<'PY'
import json, re, sys
chat, dec, since = sys.argv[1], sys.argv[2], sys.argv[3]

msgs = json.load(open(chat))
msgs = msgs if isinstance(msgs, list) else msgs.get('messages', msgs)

cards = json.load(open(dec))
cards = cards if isinstance(cards, list) else cards.get('decisions', cards)
by_id = {c.get('id'): c for c in cards if c.get('id')}

# His ruling messages look like:  Decision <id>: <key> — <label>   (em dash or hyphen)
pat = re.compile(r'^\s*Decision\s+([A-Za-z0-9._-]+)\s*:\s*([A-Za-z0-9._-]+)\s*(?:[—-]|$)')

seen = {}
for m in msgs:
    if m.get('role') != 'kam':
        continue
    ts = str(m.get('ts', ''))
    if ts[:10] < since:
        continue
    hit = pat.match(str(m.get('text', '')))
    if hit:
        # a later message on the same card supersedes an earlier one
        seen[hit.group(1)] = (hit.group(2), ts[:19])

for cid, (key, ts) in sorted(seen.items()):
    card = by_id.get(cid)
    if card is None:
        print(f"SKIP\t{cid}\t{key}\tno such card in decisions.json")
        continue
    # SCHEMA, READ NOT ASSUMED (2026-09-08): a ruled card carries status='ruled'
    # and ruled_choice. There is no 'ruled' key. The first draft of this script
    # checked card.get('ruled'), which does not exist, so every card read as
    # UNRULED and a --apply would have re-written 11 existing rulings of his.
    # Caught only because --dry-run is the default. Check BOTH fields.
    existing = card.get('ruled_choice')
    if card.get('status') == 'ruled' or existing:
        print(f"OK\t{cid}\t{existing or 'ruled'}\talready ruled — untouched")
        continue
    opts = [o.get('key') for o in card.get('options', []) if o.get('key')]
    if key not in opts:
        print(f"REFUSE\t{cid}\t{key}\tnot one of this card's options ({', '.join(opts)})")
        continue
    print(f"RULE\t{cid}\t{key}\this panel message {ts}")
PY
)"

[ -n "$PLAN" ] || { echo "sync_kam_rulings: no panel rulings found since $SINCE"; exit 0; }

printf '%s\n' "$PLAN" | while IFS=$'\t' read -r verb cid key note; do
  printf '  %-7s %-52s %-16s %s\n' "$verb" "$cid" "$key" "$note"
done

if [ "$MODE" != apply ]; then
  N="$(printf '%s\n' "$PLAN" | grep -c '^RULE' || true)"
  echo "  (dry run — $N would be written. Re-run with --apply to write them.)"
  exit 0
fi

printf '%s\n' "$PLAN" | grep '^RULE' | while IFS=$'\t' read -r _ cid key _; do
  bash "$DQ" rule "$cid" "$key" >/dev/null 2>&1 \
    && echo "  WROTE   $cid -> $key" \
    || echo "  FAILED  $cid -> $key (decision_queue refused; card left open)" >&2
done
exit 0
