#!/usr/bin/env python3
"""reconcile_rulings.py — fold Kam's panel taps into the decision cards.

WHY THIS EXISTS (2026-09-10, measured cost). The cockpit's ruling button posts a
CHAT MESSAGE and deliberately never touches decisions.json — one writer per file,
the Phase 0 principle. The consequence nobody costed: **a ruling only reaches its
card if a Wednesday seat is awake to read the chat.** On 2026-09-10 Kam tapped
four cards across 09:00–10:32; three were still `open` when a fresh seat booted
at 10:34 and had to record them by hand. Earlier the same morning another set sat
`open` for 17 minutes while he re-tapped, concluded the buttons were broken, and
said so four times.

WHAT IT DOES NOT DO, ON PURPOSE:
  * It never writes decisions.json itself. It shells out to decision_queue.sh,
    which stays the single writer. This tool only decides WHICH rule calls to make.
  * It never rules a card that is not `open`. A ruled card is Kam's record and a
    re-rule would overwrite his choice and its timestamp.
  * It never guesses. A tap naming an unknown card id, or an option key the card
    does not offer, is REPORTED and skipped — never fuzzy-matched.
  * It never rules ANOTHER SEAT'S CLIENT. decisions.json is shared between the
    coordinators; hard rule 2 (no cross-client contamination) applies to the
    bookkeeping too. Out-of-scope taps are REPORTED so the other seat can act,
    and are only applied under an explicit --all.

Usage:
  reconcile_rulings.py            # report only, changes nothing (default)
  reconcile_rulings.py --apply    # rule the cards in THIS seat's scope
  reconcile_rulings.py --all      # widen to every client (say why, out loud)
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KAM_STREAM = ROOT / "0_Brain" / "dashboard" / "data" / "chat_kam.json"
DECISIONS  = ROOT / "0_Brain" / "dashboard" / "data" / "decisions.json"
DQ_TOOL    = ROOT / "2_Project_Files" / "tools" / "decision_queue.sh"

# "Decision <id>: <key> — <label>[ | note: ...]".  The id and key are taken from
# the text; the label is deliberately IGNORED (the key is what rules the card —
# 2026-09-06 ledger w=107: copy the letter from the card, never from the wording).
TAP = re.compile(r"^Decision\s+(?P<id>[A-Za-z0-9][A-Za-z0-9_.-]*)\s*:\s*(?P<key>[A-Za-z0-9][A-Za-z0-9_-]*)\s*(?:—|-{1,2}|$)")

# This seat coordinates Secuura + Wednesday's own work + general/unlabelled.
# Every DATASEC card belongs to the other coordinator (Kam named the split
# 2026-09-08). Matching is on the client half of "Client/Project", case-folded.
OUT_OF_SCOPE_CLIENTS = {"datasec"}

def in_scope(card):
    cp = str(card.get("client_project", "")).strip()
    client = cp.split("/", 1)[0].strip().lower() if cp else ""
    if client in OUT_OF_SCOPE_CLIENTS:
        return False
    # An id-prefix fallback for cards whose client_project is missing or odd:
    # a bare "nexusai-"/"datasec-" id is Datasec's regardless of the field.
    cid = str(card.get("id", "")).lower()
    if cid.startswith(("nexusai-", "datasec-", "vision-", "mypki-", "cypherkey-", "leadbot-")):
        return False
    return True

def load(p, what):
    try:
        return json.loads(p.read_text())
    except Exception as e:
        sys.exit(f"REFUSED — {what} unreadable ({p}): {e}")

def main():
    apply_ = "--apply" in sys.argv[1:]
    widen  = "--all" in sys.argv[1:]
    for a in sys.argv[1:]:
        if a not in ("--apply", "--all"):
            sys.exit(f"REFUSED — unknown argument {a!r}. Usage: reconcile_rulings.py [--apply] [--all]")

    msgs = load(KAM_STREAM, "Kam's chat stream")
    if isinstance(msgs, dict):
        msgs = msgs.get("messages", [])
    cards = load(DECISIONS, "decisions.json")
    if not isinstance(cards, list):
        sys.exit("REFUSED — decisions.json is not a list")
    by_id = {c.get("id"): c for c in cards if isinstance(c, dict)}

    # Newest tap per card wins: Kam re-tapping is him correcting himself, and the
    # LAST thing he said is what he meant. Sorted by timestamp, not file order.
    taps = {}
    for m in msgs:
        if not isinstance(m, dict):
            continue
        mt = TAP.match(str(m.get("text", "")).strip())
        if not mt:
            continue
        ts = str(m.get("ts", ""))
        cid, key = mt.group("id"), mt.group("key")
        if cid not in taps or ts >= taps[cid][1]:
            taps[cid] = (key, ts)

    todo, skipped = [], []
    for cid, (key, ts) in sorted(taps.items(), key=lambda kv: kv[1][1]):
        card = by_id.get(cid)
        if card is None:
            skipped.append((cid, key, ts, "no such card — NOT fuzzy-matched"))
            continue
        status = card.get("status")
        if status != "open":
            # already ruled (by a seat, or by an earlier run) — leave it alone
            if card.get("ruled_choice") != key:
                skipped.append((cid, key, ts,
                                f"card is {status!r} with choice {card.get('ruled_choice')!r}, "
                                f"tap says {key!r} — CONFLICT, left for a human"))
            continue
        if not widen and not in_scope(card):
            skipped.append((cid, key, ts,
                            f"OUT OF SCOPE for this seat ({card.get('client_project')!r}) — "
                            f"the other coordinator's card, reported not ruled"))
            continue
        keys = [o.get("key") for o in card.get("options", []) if isinstance(o, dict)]
        if key not in keys:
            skipped.append((cid, key, ts, f"option {key!r} not offered by the card (has {keys}) — NOT guessed"))
            continue
        todo.append((cid, key, ts))

    print(f"taps found: {len(taps)} · to rule: {len(todo)} · skipped: {len(skipped)}")
    for cid, key, ts, why in skipped:
        print(f"  SKIP  {cid} -> {key}  ({ts[:16]})  {why}")
    if not todo:
        print("nothing to reconcile" if not skipped else "nothing applied")
        return 0
    for cid, key, ts in todo:
        if not apply_:
            print(f"  WOULD RULE  {cid} -> {key}   (tapped {ts[:16]})")
            continue
        r = subprocess.run(["bash", str(DQ_TOOL), "rule", cid, key],
                           capture_output=True, text=True)
        # never discard stderr — a failure you cannot diagnose costs more than it saves
        out = (r.stdout or "").strip() or (r.stderr or "").strip()
        print(f"  {'RULED' if r.returncode == 0 else 'FAILED'}  {cid} -> {key}   {out}")
        if r.returncode != 0:
            return 1
    if not apply_:
        print("\n(report only — nothing was changed. re-run with --apply)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
