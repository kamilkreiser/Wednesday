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
    does not offer, is REPORTED and skipped — never fuzzy-matched. A `note:` tap
    (free text, no key) is REPORTED LOUDLY and counted, never applied — see NOTE_TAP.
  * It never rules ANOTHER SEAT'S CLIENT. decisions.json is shared between the
    coordinators; hard rule 2 (no cross-client contamination) applies to the
    bookkeeping too. Out-of-scope taps are REPORTED so the other seat can act,
    and are only applied under an explicit --all.

WHERE THE TAPS COME FROM (Phase 3, 2026-09-21 — Kam 12:50 "switch to using the
live version only"): his taps on the LIVE board's cards arrive as rows on the
live store, encrypted to his keys AND to this seat's certificate key. They are
read through dashboard-cloud/seat/get_kam_messages.py --decrypt as $WED_AGENT
(the API returns only this seat's partitions + his broadcasts — R0 holds by
construction). RECONCILE_SOURCE=live|local|both:
  both  (DEFAULT) the local chat_kam.json AND the live board, one tap per card
        (newest wins across both) — his taps land on whichever board he used.
  live  the live board only.   local  chat_kam.json only (and ALWAYS when
        RECONCILE_CHAT points at a fixture: the arms never touch the API).
A live fetch failure is LOUD and exits 2: a reconciler that quietly falls back
to the local file would drop every live tap while looking healthy — the exact
failure this tool was written to end.

Usage:
  reconcile_rulings.py            # report only, changes nothing (default)
  reconcile_rulings.py --apply    # rule the cards in THIS seat's scope
  reconcile_rulings.py --all      # widen to every client (say why, out loud)
"""
import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# RECONCILE_DECISIONS / RECONCILE_CHAT (2026-09-21): point the tool at fixtures so
# the arms in tests/reconcile_rulings_arms.sh never read or rule the live store.
# DECISIONS is also handed to decision_queue.sh as DQ_FILE, so an --apply against
# a fixture rules THAT fixture and can never reach the live file by the back door.
KAM_STREAM = Path(os.environ.get("RECONCILE_CHAT") or ROOT / "0_Brain" / "dashboard" / "data" / "chat_kam.json")
DECISIONS  = Path(os.environ.get("RECONCILE_DECISIONS") or ROOT / "0_Brain" / "dashboard" / "data" / "decisions.json")
DQ_TOOL    = ROOT / "2_Project_Files" / "tools" / "decision_queue.sh"
GET_LIVE   = ROOT / "2_Project_Files" / "dashboard-cloud" / "seat" / "get_kam_messages.py"
VENV_PY    = ROOT / "2_Project_Files" / "dashboard-cloud" / ".venv" / "bin" / "python"
SOURCE     = (os.environ.get("RECONCILE_SOURCE") or ("local" if os.environ.get("RECONCILE_CHAT") else "both")).strip().lower()
if SOURCE not in ("live", "local", "both"):
    sys.exit(f"REFUSED — RECONCILE_SOURCE must be live|local|both (got {SOURCE!r})")

# "Decision <id>: <key> — <label>[ | note: ...]".  The id and key are taken from
# the text; the label is deliberately IGNORED (the key is what rules the card —
# 2026-09-06 ledger w=107: copy the letter from the card, never from the wording).
TAP = re.compile(r"^Decision\s+(?P<id>[A-Za-z0-9][A-Za-z0-9_.-]*)\s*:\s*(?P<key>[A-Za-z0-9][A-Za-z0-9_-]*)\s*(?:—|-{1,2}|$)")

# "Decision <id> note: <free text>" — Kam's OTHER ruling form, typed on the panel.
# Until 2026-09-21 (ledger w=2, measured 2026-09-20 19:4x) these matched nothing:
# the run said "taps found: 2 · to rule: 0" and both rulings — "actioned. remove
# card" and "remove the rule and make the fix" — were dropped without a line.
# A note is NEVER turned into an option key (that would be a guess); it is printed
# LOUDLY, counted in the summary, and handed to a human with the exact
# `decision_queue.sh withdraw` call ready — because "discuss this with me further"
# and "delete this card" are both notes, and only a reader can tell which closes.
NOTE_TAP = re.compile(r"^Decision\s+(?P<id>[A-Za-z0-9][A-Za-z0-9_.-]*)\s*:?\s*note\s*:\s*(?P<note>.+)$", re.S)

# WHOSE CARDS THIS SEAT MAY RULE — derived from WED_AGENT, never hardcoded.
#
# Until 2026-09-20 this block read `OUT_OF_SCOPE_CLIENTS = {"datasec"}` with no
# seat check at all: it was written from the WEDNESDAY seat's point of view and
# was simply wrong on Tuesday's, where Datasec is the ONLY thing in scope. The
# effect was silent and one-directional — Tuesday ran the reconciler, it reported
# "skipped: OUT OF SCOPE ... the other coordinator's card" for its OWN client, and
# Kam's taps on Datasec cards never reached them. Measured twice on 2026-09-20
# (nexusai-degraded-flip-and-live-deployments, tapped 21:14, skipped on both a
# report and an --apply run). A reconciler that silently drops the principal's
# rulings for its own client is worse than none, because the seat believes it ran.
#
# Matching is on the client half of "Client/Project", case-folded, with an
# id-prefix fallback for cards whose client_project is missing or odd.
DATASEC_CLIENTS  = {"datasec"}
DATASEC_PREFIXES = ("nexusai-", "datasec-", "vision-", "mypki-", "cypherkey-", "leadbot-")

SEAT = os.environ.get("WED_AGENT", "").strip().lower()
if SEAT not in ("tuesday", "wednesday", "friday"):
    # A guess-by-default must become a REFUSAL (2026-09-09, the seat-resolver
    # lesson; Kam's own words in Launch_Tuesday.command: "a seat that guesses its
    # own client is precisely the failure the two-agent split exists to prevent").
    sys.stderr.write(
        "reconcile_rulings: WED_AGENT is %r, which is not 'tuesday', 'wednesday' or 'friday'.\n"
        "  This tool RULES CARDS, so a guessed seat would rule another client's decisions.\n"
        "  Fix: launch through Launch_Tuesday.command / Launch_Wednesday.command / Launch_Friday.command,\n"
        "  or export WED_AGENT=tuesday|wednesday|friday in this shell. REFUSING.\n" % (SEAT or None))
    sys.exit(2)

def _is_datasec(card):
    cp = str(card.get("client_project", "")).strip()
    client = cp.split("/", 1)[0].strip().lower() if cp else ""
    if client in DATASEC_CLIENTS:
        return True
    return str(card.get("id", "")).lower().startswith(DATASEC_PREFIXES)

def in_scope(card):
    # FRIDAY (2026-09-23, Kam 10:49 — the laptop seat, BOTH clients): a card the friday
    # seat created carries seat="friday" (decision_queue.sh add). The friday seat rules
    # ONLY those cards, and wednesday/tuesday NEVER rule a seat=friday card. Friday cannot
    # take a client half of the complement below, because it works both clients.
    if SEAT == "friday":
        return card.get("seat") == "friday"
    if card.get("seat") == "friday":
        return False
    # Tuesday rules Datasec and nothing else; Wednesday rules everything else.
    # The two seats are exact complements over every NON-friday card (unchanged), so no
    # such card is rulable by both and none is rulable by neither.
    return _is_datasec(card) if SEAT == "tuesday" else not _is_datasec(card)

def load(p, what):
    try:
        return json.loads(p.read_text())
    except Exception as e:
        sys.exit(f"REFUSED — {what} unreadable ({p}): {e}")

def load_live():
    """Kam's rows from the LIVE board as this seat, decrypted with the seat's certificate key (Phase 3). 7-day window,
    max cap (the API caps PER PARTITION oldest-first; get_kam_messages warns on stderr if a partition hits the cap).
    Any failure is fatal and loud — never an empty list that reads as 'no taps'."""
    import datetime, subprocess
    if not VENV_PY.exists():
        sys.exit(f"REFUSED — live source needs {VENV_PY} (PORTABILITY.md); set RECONCILE_SOURCE=local to read the local file only")
    if not (ROOT / "4_Credentials" / "dashboard-cloud" / f"{SEAT}-seat.pem").exists():
        sys.exit(f"REFUSED — live source needs 4_Credentials/dashboard-cloud/{SEAT}-seat.pem on this machine; set RECONCILE_SOURCE=local")
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M")
    r = subprocess.run([str(VENV_PY), str(GET_LIVE), "--seat", SEAT, "--cert-dir", str(ROOT / "4_Credentials" / "dashboard-cloud"), "--decrypt", "--json", "--limit", "1000", "--since", since],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit(f"REFUSED — live board read failed (rc={r.returncode}): {' '.join(r.stderr.split())[:300]}")
    if r.stderr.strip():
        sys.stderr.write(r.stderr)
    out = []
    synthetic = 0
    for m in json.loads(r.stdout).get("messages", []):
        if m.get("synthetic") in (True, "true", "True"):
            synthetic += 1; continue   # a probe row wearing role=kam is NOT Kam's word — never a tap (Wednesday, 2026-09-21 15:0x)
        if m.get("decrypt_error"):
            sys.stderr.write(f"  live row {m.get('row_key')} not readable by this seat ({m['decrypt_error']}) — read it on the live board\n")
            continue
        out.append({"role": "kam", "ts": m.get("ts_local") or m.get("ts"), "view": m.get("view"), "text": m.get("text", ""), "source": "live"})
    if synthetic:
        sys.stderr.write(f"  live: {synthetic} synthetic (probe) row(s) skipped — not Kam's word\n")
    return out

def main():
    apply_ = "--apply" in sys.argv[1:]
    widen  = "--all" in sys.argv[1:]
    for a in sys.argv[1:]:
        if a not in ("--apply", "--all"):
            sys.exit(f"REFUSED — unknown argument {a!r}. Usage: reconcile_rulings.py [--apply] [--all]")

    msgs = []
    if SOURCE in ("local", "both"):
        msgs = load(KAM_STREAM, "Kam's chat stream")
        if isinstance(msgs, dict):
            msgs = msgs.get("messages", [])
    live = load_live() if SOURCE in ("live", "both") else []
    n_local = sum(1 for m in msgs if isinstance(m, dict) and m.get("role") == "kam")
    msgs = list(msgs) + live
    cards = load(DECISIONS, "decisions.json")
    if not isinstance(cards, list):
        sys.exit("REFUSED — decisions.json is not a list")
    by_id = {c.get("id"): c for c in cards if isinstance(c, dict)}

    # Newest tap per card wins: Kam re-tapping is him correcting himself, and the
    # LAST thing he said is what he meant. Sorted by timestamp, not file order.
    # taps[cid] = (key, ts, note): a <key> tap has note=None, a note: tap has key=None.
    taps = {}
    for m in msgs:
        if not isinstance(m, dict):
            continue
        text = str(m.get("text", "")).strip()
        mt = TAP.match(text)
        if mt:
            key, note = mt.group("key"), None
        else:
            mt = NOTE_TAP.match(text)
            if not mt:
                continue
            key, note = None, " ".join(mt.group("note").split())
        ts = str(m.get("ts", ""))
        cid = mt.group("id")
        if cid not in taps or ts >= taps[cid][1]:
            taps[cid] = (key, ts, note)

    todo, skipped, notes = [], [], []
    for cid, (key, ts, note) in sorted(taps.items(), key=lambda kv: kv[1][1]):
        card = by_id.get(cid)
        if card is None:
            skipped.append((cid, key, ts, "UNKNOWN CARD — no such card — NOT fuzzy-matched"))
            continue
        status = card.get("status")
        if status != "open":
            # already ruled (by a seat, or by an earlier run) — leave it alone
            if note is not None:
                # a note on a closed card is still Kam's words. If it PREDATES the
                # close, the seat that closed the card had it in front of it (the
                # 09-20 pair were withdrawn by hand within a minute of the note);
                # if it is NEWER than the close, Kam wrote on a closed card and
                # nobody may have read it — say so. Same isoformat on both sides.
                closed_at = str(card.get("ruled_ts") or card.get("withdrawn_at") or "")
                if ts > closed_at and card.get("withdrawn_reason") != note:
                    skipped.append((cid, key, ts,
                                    f"card is {status!r} since {closed_at[:16]} but this note is NEWER "
                                    f"— {note!r} — read it, it is recorded nowhere"))
            elif card.get("ruled_choice") != key:
                skipped.append((cid, key, ts,
                                f"card is {status!r} with choice {card.get('ruled_choice')!r}, "
                                f"tap says {key!r} — CONFLICT, left for a human"))
            continue
        if not widen and not in_scope(card):
            skipped.append((cid, key, ts,
                            f"OUT OF SCOPE for this seat ({card.get('client_project')!r}) — "
                            f"the other coordinator's card, reported not ruled"))
            continue
        if note is not None:
            notes.append((cid, ts, note))
            continue
        keys = [o.get("key") for o in card.get("options", []) if isinstance(o, dict)]
        if key not in keys:
            skipped.append((cid, key, ts, f"option {key!r} not offered by the card (has {keys}) — NOT guessed"))
            continue
        todo.append((cid, key, ts))

    print(f"source={SOURCE} (local kam rows: {n_local}, live rows: {len(live)}, seat={SEAT}) · "
          f"taps found: {len(taps)} · to rule: {len(todo)} · notes: {len(notes)} "
          f"(flagged, NOT applied) · skipped: {len(skipped)}")
    for cid, key, ts, why in skipped:
        print(f"  SKIP  {cid} -> {key or 'note'}  ({ts[:16]})  {why}")
    for cid, ts, note in notes:
        # LOUD on purpose: this is a principal's ruling the tool cannot apply
        # mechanically. The withdraw line is ready to paste IF the note closes the
        # card; if it is a question, answer it on the panel and leave the card open.
        print(f"  UNPARSEABLE-KEY RULING — {cid} — {note}   (tapped {ts[:16]})")
        print(f"      if this CLOSES the card:  bash {DQ_TOOL} withdraw {cid} {json.dumps(note)}")
    if not todo:
        if notes:
            print(f"nothing applied — {len(notes)} note ruling(s) above need a human")
        else:
            print("nothing to reconcile" if not skipped else "nothing applied")
        return 0
    for cid, key, ts in todo:
        if not apply_:
            print(f"  WOULD RULE  {cid} -> {key}   (tapped {ts[:16]})")
            continue
        r = subprocess.run(["bash", str(DQ_TOOL), "rule", cid, key],
                           capture_output=True, text=True,
                           env={**os.environ, "DQ_FILE": str(DECISIONS)})
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
