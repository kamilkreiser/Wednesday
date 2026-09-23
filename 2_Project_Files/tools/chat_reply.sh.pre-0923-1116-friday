#!/bin/bash
# chat_reply.sh — mirror a Wednesday conversational reply into the dashboard chat.
#
# WHY (Kam, 2026-08-17): the terminal interleaves conversation with fleet
# mechanics, so what he is reading scrolls away under agent traffic. The
# dashboard chat tile is the STABLE conversation surface: substantive replies
# to Kam are mirrored here (short form, pointers to documents for anything
# long). Fleet mechanics NEVER go through this script.
#
# Usage: chat_reply.sh [--project <Datasec|Secuura|WED>] [--file <path> [--file <path>…]] "message text"
#
# --file <path> (2026-09-22, Kam 15:26:48 "if I ask for a file to be shared, you can share it with me and place it there
# and I can download it at a later stage from the live site"): the file is encrypted on this machine and placed in the
# live board's FILE DRAWER as this seat (dashboard-cloud/seat/share_file.py — Kam's ring + this seat's key, the server
# stores bytes it cannot read), BEFORE the message is written; its file id is appended to the mirrored message so the
# live row carries `attachments: [id]` and Kam's page shows a chip. A share that fails is LOUD and REFUSES the whole
# reply (rc 5) — a message that says "here is the file" with no file is the 2026-09-09 `--file` incident again. The local
# stream entry carries the same note. (Until today `--file` was the one flag Wednesday kept typing that did not exist.)
# Appends {role: "wednesday", seat, project, ts, text} to
# 0_Brain/dashboard/data/chat_log.json atomically (write temp + mv). Never
# discards stderr. Refuses empty input.
#
# --project (Kam, 2026-09-07 11:12): tags the entry so each dashboard can choose
# which project's replies it displays / auto-speaks (per-browser filter, WED on
# by default). Omitted → "WED"; entries with no field at all read as "WED".
#
# ── DUAL-WRITE TO THE LIVE BOARD (Phase 2, Kam 2026-09-21 11:43) ─────────────
# After the local append + derived rebuild succeed, the SAME entry is posted to
# the external dashboard, encrypted to Kam's public key on this machine
# (tools/_live_board.sh -> dashboard-cloud/seat), with view=<this seat>. Local
# first, always; a failed post is LOUD on stderr + fleet/state/
# live_board_post_failures.log and never changes this script's exit code. The
# seat is $AGENT (below); Datasec is refused locally for the Wednesday seat.
# LIVE_BOARD=0 disables the post.
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
# ── PHASE 0: ONE WRITER PER FILE (Kam's 2026-09-08 11:50 commission) ─────────
# This script no longer touches chat_log.json. It appends ONLY to its own seat's
# stream and then regenerates the DERIVED chat_log.json from all streams. Two
# seats can never write one tracked file, so the conflict class that corrupted
# Kam's reading surface three times on 2026-09-08 cannot occur — by construction,
# the way the claims files have worked since 09-07 without a single conflict.
# The AGENT is what names the stream, and it is derived from the seat, never
# typed. An unknown host is REFUSED rather than defaulted: writing another
# agent's stream is exactly the failure this phase exists to make impossible.
# ── THE TREE DECIDES; THERE IS NO HOSTNAME GUESS LEFT (2026-09-09) ───────────
# This was a hostname map, and by today BOTH arms were wrong: Tuesday moved to
# Kamils-Mac-mini, so `Kamils-MBP* -> tuesday` names a machine she is not on.
#
# Tuesday's argument for REMOVING the stale arm rather than repointing it, adopted
# because it is this file's own logic rather than tidiness: the fallback can only
# fire when WED_AGENT is unset AND the tree has not resolved it — which is exactly
# the case where there is NO evidence about which seat this is. Mapping an
# unrecognised tree on a known-stale host to a named seat is a guess, and Kam's own
# words in Launch_Tuesday.command are that a seat guessing its own client is the
# failure the two-agent split exists to prevent. Deleting the arm converts that
# guess into the refusal already chosen everywhere else in this script.
#
# The travel case argues the same way rather than against it: if he ever runs the
# TUESDAY tree on the laptop, the TREE check resolves it correctly and the hostname
# arm was never needed.
seat_agent_default() {
  case "$(basename "$PROJECT_DIR")" in
    TUESDAY|Tuesday|tuesday)       echo "tuesday"   ;;
    WEDNESDAY|Wednesday|wednesday) echo "wednesday" ;;
    *)                             echo ""          ;;  # no evidence: no guess
  esac
}
AGENT="${WED_AGENT:-}"
[ -n "$AGENT" ] || AGENT="$(seat_agent_default)"
case "$AGENT" in
  wednesday|tuesday) ;;
  *) echo "chat_reply: cannot tell which agent this seat is (host '$(hostname -s 2>/dev/null)')." >&2
     echo "  Export WED_AGENT=wednesday or WED_AGENT=tuesday in the launcher. REFUSING —" >&2
     echo "  a guess here writes into the other agent's stream." >&2
     exit 2 ;;
esac
CHAT="$PROJECT_DIR/0_Brain/dashboard/data/chat_$AGENT.json"
STREAMS="$PROJECT_DIR/2_Project_Files/tools/chat_streams.py"
# ── PER-SEAT PROJECT DEFAULT (2026-09-08, s150) ──────────────────────────────
# Kam ruled on 2026-09-07 11:12 that the chat panel gets a per-project display
# filter, and chat.html has carried a complete, correct one since — chips per
# project, persisted per browser, his own messages always shown.
# MEASURED 2026-09-08 08:4x, which is why this block exists: of 1725 entries the
# `project` field read WED 64 / Datasec 6 / absent 1655, and `projOf()` maps an
# absent field to "WED" too. So BOTH seats' replies landed in ONE bucket and the
# filter had nothing to separate. The mechanism was never broken; nothing fed it.
# `--project` is wired correctly (line ~44 passes it through) — no seat passed it.
#
# THE MAPPING BELOW IS KAM'S SPLIT AND HE CALLED IT TEMPORARY, verbatim
# (panel, 2026-09-08 07:09): "for now, secuura on this machine and datasec on
# laptop". It is ONE line to change and it is deliberately the only place the
# machine->client assumption lives. If he re-splits, edit SEAT_PROJECT and nothing
# else. An unknown host falls back to "WED", never to a guess.
# Precedence: --project  >  $CHAT_PROJECT already in the environment  >  this
# per-seat default  >  "WED".
# ── KEYED ON THE SEAT, NOT THE HOSTNAME (Tuesday, 2026-09-09 — measured) ─────
# This used to key on hostname: Kamils-MBP* -> Datasec, Kamils-Mac-Studio* -> Secuura.
# **Tuesday moved to Kamils-Mac-mini on 2026-09-09, which matches NEITHER**, so it fell
# through to "" and then to "WED" — silently. Her boot report to Kam that afternoon was
# written with project=WED, so a message meant for his Datasec view landed in his WED
# bucket. Blast radius exactly one message; she read all ten of her WED-tagged entries
# before touching any, and retagged only her own in her single-writer stream.
#
# The seat is ALREADY resolved above, from WED_AGENT, and that resolver REFUSES rather
# than guessing when it cannot tell. Keying the project off it removes the second,
# weaker resolver entirely — byte-identical behaviour for the Wednesday seat, and no
# silent WED fallback for anyone else. Tuesday's recommendation, adopted whole.
#
# ⚠ AND THE REASON THIS WAS MISSED IS WORTH MORE THAN THE FIX: the morning's sweep
# grepped for the literal `wednesday` and this defect contains no agent name at all —
# it is a hostname map. **A grep for the seat name is structurally blind to it. The
# predicate that finds this class is HOSTNAME KEYS, not agent names.**
#
# Precedence is unchanged: --project > $CHAT_PROJECT > this per-seat default > "WED".
# If Kam re-splits the clients, this case is still the one line to edit.
seat_project_default() {
  case "$AGENT" in
    tuesday)   echo "Datasec" ;;   # his 2026-09-08 split: Datasec is Tuesday's
    wednesday) echo "Secuura" ;;   # Secuura + all general work is Wednesday's
    *)         echo "" ;;          # unreachable: the resolver above already refused
  esac
}
PROJECT="${CHAT_PROJECT:-}"
[ -n "$PROJECT" ] || PROJECT="$(seat_project_default)"
[ -n "$PROJECT" ] || PROJECT="WED"
FILES=()
while [ $# -gt 1 ]; do
  case "$1" in
    --project) [ -n "${2:-}" ] || { echo "chat_reply: --project needs a value (Datasec|Secuura|WED)" >&2; exit 2; }; PROJECT="$2"; shift 2 ;;
    --file)    [ -n "${2:-}" ] || { echo "chat_reply: --file needs a path" >&2; exit 2; }
               [ -f "$2" ] || { echo "chat_reply: --file $2: no such file — REFUSED (nothing written)" >&2; exit 2; }
               FILES+=("$2"); shift 2 ;;
    *) break ;;
  esac
done
MSG="${1:-}"
[ -n "$MSG" ] || { echo "chat_reply: empty message refused" >&2; exit 2; }
# ADVISORY (ledger w=4, 2026-09-18): flag unmeasured ABSENCE claims before they reach Kam. Never blocks,
# never changes the exit code. Arms: 2_Project_Files/tests/absence_claim_check_arms.sh
printf '%s' "$MSG" | bash "$SELF_DIR/absence_claim_check.sh" || true

# ── A REPEATED SENTENCE IS NOISE ON THE ONE SURFACE HE READS (Kam, 2026-09-16 14:50) ──
# His words: "you said that twice in 2 minutes.  can this be fixed?" — and it was the same
# shape he corrected on 2026-08-27 ("tell me what you need from me when you need it… do not
# repeat the standing list in every reply"). The habit: tailing every message with a standing
# status line ("the sync is still scanning, still zero deletions"), so an unchanged fact
# arrived twice inside two minutes on the surface he actually reads.
#
# He asked whether it could be FIXED, not whether I would be careful — so the check is here,
# in the path, rather than in a seat's memory (2026-08-07: a promise is not a mechanism).
# It refuses when a SENTENCE of this message already appeared in this seat's last few
# messages. Refusing rather than warning, because a warning printed to a terminal nobody is
# reading is exactly the failure class this whole tree keeps finding.
# CHAT_ALLOW_REPEAT=1 overrides, and the reason belongs in the message when it is used.
# CHAT_DRY=1 — run every check and print the verdict, WRITE NOTHING. Added in the same
# breath as the guard below, because arming the guard sent THREE test messages to Kam's real
# reading surface, which is precisely the noise he had just asked me to stop making. A tool
# whose only test path is production has no test path (2026-09-14: a gate in the coordinator's
# own path must be red-proofed from a seam, never by firing it at the principal).
if [ "${CHAT_ALLOW_REPEAT:-0}" != "1" ]; then
  REPEAT="$(CHAT_STREAM_FILE="$CHAT" python3 - "$MSG" <<'PYREP'
import json, os, re, sys
msg = sys.argv[1]
path = os.environ.get("CHAT_STREAM_FILE", "")
def sentences(t):
    # Sentence-ish, and normalised so punctuation and spacing drift cannot hide a repeat.
    out = []
    for raw in re.split(r"(?<=[.!?])\s+|\n+", t):
        n = re.sub(r"[^a-z0-9 ]+", " ", raw.lower())
        n = re.sub(r"\s+", " ", n).strip()
        # Short sentences repeat innocently ("Done.", "Sorry for the noise.") — only guard
        # ones long enough to be a restated FACT rather than a courtesy.
        if len(n.split()) >= 8:
            out.append(n)
    return out
try:
    log = json.load(open(path, encoding="utf-8"))
except Exception:
    print(""); raise SystemExit
recent = [e for e in log if e.get("role") == "wednesday"][-4:]
prev = set()
for e in recent:
    prev.update(sentences(e.get("text", "")))
for s in sentences(msg):
    if s in prev:
        print(s[:90]); raise SystemExit
print("")
PYREP
)"
  if [ -n "$REPEAT" ]; then
    echo "chat_reply: REFUSED — this repeats a sentence you already sent him in the last few messages:" >&2
    echo "  \"$REPEAT...\"" >&2
    echo "  Kam, 2026-09-16 14:50: \"you said that twice in 2 minutes.  can this be fixed?\"" >&2
    echo "  Report a status when it CHANGES, never as a sign-off. Rewrite without it," >&2
    echo "  or CHAT_ALLOW_REPEAT=1 if the repetition is genuinely the point (say why in the message)." >&2
    exit 3
  fi
fi
# ── A FLAG IS NOT A MESSAGE (2026-09-09, ledger — it cost three messages to Kam) ──
# `--project` is the ONLY flag this script has. Wednesday invoked it three times as
# `chat_reply.sh --file <path>`, so the literal string `--file` was mirrored to Kam's
# reading surface as the message and 2.3 KB of content — including a security finding
# and a merge hold — was never sent. The script printed its ordinary success line and
# its entry COUNT incremented each time, so nothing looked wrong from the caller's
# side. KAM noticed, not Wednesday: "multiple entries from you saying file".
# A message that begins with `--` is overwhelmingly a mis-invocation, and the cost of
# refusing a genuine one (re-send with a leading space) is nothing next to the cost of
# silently mirroring a flag name to the principal.
case "$MSG" in
  --*) echo "chat_reply: REFUSED — the message begins with '--', which is almost certainly" >&2
       echo "  a flag this script does not have. The flags are --project <Datasec|Secuura|WED> and" >&2
       echo "  --file <path> (share a file into the live drawer); both go BEFORE the positional message." >&2
       echo "  To send the CONTENT of a file as text pass \"\$(cat <path>)\"; to SHARE the file use --file." >&2
       echo "  (2026-09-09: three messages to Kam were lost exactly this way.)" >&2
       echo "  If you genuinely meant to send text starting with '--', prefix it with a space." >&2
       exit 2 ;;
esac
# A stream that does not exist yet is created empty — a fresh clone, or the first
# thing this seat has ever said. That is not an error; a MISSING stream is only a
# problem if something then writes the derived file instead, which nothing does.
[ -f "$CHAT" ] || printf '[]' > "$CHAT"

# ── CARD-ID GATE (2026-09-06 22:2x, mirror-reports-state w=7 → promoted) ──
# The FIRST of the three instances landed here: the panel told Kam a card existed
# that did not, because the line was written in the same batch as a refused add.
# Kam's panel is his reading surface; a line there is a receipt, not a forecast.
GATE="$PROJECT_DIR/2_Project_Files/fleet/card_id_gate.sh"
if [ -f "$GATE" ]; then
  _cg_tmp="$(mktemp)"; printf '%s' "$MSG" > "$_cg_tmp"
  if ! bash "$GATE" "$_cg_tmp"; then
    echo "  (gate: card_id_gate.sh — ledger w=7; nothing was mirrored to Kam's panel)" >&2
    rm -f "$_cg_tmp"; exit 1
  fi
  rm -f "$_cg_tmp"
fi
if [ "${CHAT_DRY:-0}" = "1" ]; then
  echo "chat_reply: DRY — all checks passed, nothing written (${#MSG} chars, ${#FILES[@]} file(s) would be shared)"
  exit 0
fi
# ── --file: share into the live drawer FIRST (encrypted here, as this seat); refuse the reply if any share fails ──
FILE_IDS=""
if [ "${#FILES[@]}" -gt 0 ]; then
  _sf_py="$PROJECT_DIR/2_Project_Files/dashboard-cloud/.venv/bin/python"; [ -x "$_sf_py" ] || _sf_py=python3
  _sf="$PROJECT_DIR/2_Project_Files/dashboard-cloud/seat/share_file.py"
  _sf_client="$(printf '%s' "$PROJECT" | cut -d/ -f1)"; case "$(printf '%s' "$_sf_client" | tr '[:upper:]' '[:lower:]')" in secuura*) _sf_client=Secuura ;; datasec*) _sf_client=Datasec ;; *) _sf_client=WED ;; esac
  for _f in "${FILES[@]}"; do
    _sf_out="$("$_sf_py" "$_sf" "$_f" --seat "$AGENT" --client "$_sf_client" --cert-dir "$PROJECT_DIR/4_Credentials/dashboard-cloud" --note "$(printf '%s' "$MSG" | head -c 200)" 2>&1)"; _sf_rc=$?
    _sf_id="$(printf '%s\n' "$_sf_out" | /usr/bin/grep -o 'file_id=[A-Za-z0-9._-]*' | head -1 | cut -d= -f2)"
    if [ "$_sf_rc" -ne 0 ] || [ -z "$_sf_id" ]; then
      echo "chat_reply: 🔴 REFUSED — the file share of $_f FAILED (rc=$_sf_rc); nothing was written, Kam was not told a file exists:" >&2
      printf '%s\n' "$_sf_out" | tail -4 | sed 's/^/  /' >&2; exit 5
    fi
    echo "live-board: file $_f shared into the drawer as $AGENT/$_sf_client (file_id=$_sf_id)"
    FILE_IDS="${FILE_IDS:+$FILE_IDS,}$_sf_id"
  done
  MSG="$MSG"$'\n'"📎 file$( [ "${#FILES[@]}" -gt 1 ] && echo s ) in the live drawer: $(for _f in "${FILES[@]}"; do printf '%s ' "$(basename "$_f")"; done)(id $FILE_IDS)"
fi
_TS_STATE="$PROJECT_DIR/2_Project_Files/fleet/state/live_board_last_local_ts"; mkdir -p "$(dirname "$_TS_STATE")" 2>/dev/null; : > "$_TS_STATE"
CHAT_FILE="$CHAT" CHAT_PROJECT="$PROJECT" CHAT_TS_OUT="$_TS_STATE" python3 - "$MSG" <<'PYEOF'
import json, os, sys, datetime, tempfile
path = os.environ["CHAT_FILE"]
msg = sys.argv[1]
# SELF-HEALING READ (2026-09-07): two Wednesday seats share this file through git, so a
# rebase can leave conflict markers in it. That corrupted Kam's reading surface three times
# today and each repair was by hand — a habit, not a mechanism. If the file will not parse,
# recover BOTH sides' entries, dedupe by (ts, role), re-sort. Nothing is dropped.
_raw = open(path).read()
try:
    log = json.loads(_raw)
except json.JSONDecodeError:
    # CORRECTED 2026-09-07 17:5x, MEASURED not reasoned. The previous repair stripped the
    # marker LINES and then salvaged objects with a per-object regex. That silently LOSES
    # entries whenever a conflict boundary falls INSIDE an object rather than between two:
    # the shared prefix ("role") stays outside the markers, so the two sides' remaining
    # fields end up in ONE brace-run and only one entry survives it. Run against the real
    # 17:2x conflict it returned 1624 entries where both sides hold 1630 — it dropped SIX,
    # including the two NEWEST messages (the Studio seat's 17:20 and the laptop's 17:23) —
    # and printed "REPAIRED". A repair that reports success while losing the most recent
    # messages is worse than one that refuses.
    # So: rebuild each SIDE as a whole document, parse both, union. The regex salvage is
    # kept as the last resort for a file too damaged for that, and now SAYS it is lossy.
    import re as _re
    def _side(_text, _keep):                      # _keep: 'ours' | 'theirs'
        _out, _state = [], 0
        for _l in _text.split('\n'):
            if _l.startswith('<<<<<<<'): _state = 1; continue
            if _l.startswith('=======') and _state == 1: _state = 2; continue
            if _l.startswith('>>>>>>>') and _state == 2: _state = 0; continue
            if _state == 0 or (_state == 1 and _keep == 'ours') or (_state == 2 and _keep == 'theirs'):
                _out.append(_l)
        return '\n'.join(_out)
    _entries, _how = [], None
    try:
        _ours = json.loads(_side(_raw, 'ours'))
        _theirs = json.loads(_side(_raw, 'theirs'))
        _entries = ([e for e in _ours if isinstance(e, dict)] +
                    [e for e in _theirs if isinstance(e, dict)])
        _how = 'both sides parsed as documents'
    except json.JSONDecodeError:
        _clean = '\n'.join(l for l in _raw.split('\n')
                            if not l.startswith(('<<<<<<<', '=======', '>>>>>>>')))
        for _m in _re.finditer(r'\{[^{}]*"ts"\s*:\s*"[^"]+"[^{}]*\}', _clean, _re.S):
            try: _entries.append(json.loads(_m.group(0)))
            except Exception: continue
        _how = 'REGEX SALVAGE — LOSSY, a side would not parse; entries may be missing'
    # dedupe on (ts, role, text-prefix): ts+role alone collides when two seats write in the
    # same second, and dropping a real message costs more than keeping a near-duplicate.
    _seen, log = set(), []
    for _e in _entries:
        _k = (_e.get('ts'), _e.get('role'), (_e.get('text') or '')[:120])
        if _k in _seen: continue
        _seen.add(_k); log.append(_e)
    log.sort(key=lambda e: str(e.get('ts', '')))
    sys.stderr.write('chat_reply: REPAIRED a conflict-marked log via %s -> %d entries\n'
                     % (_how, len(log)))
_ts = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
log.append({
    "role": "wednesday",
    "seat": __import__("socket").gethostname(),  # 2026-09-07: which machine wrote this (autoplay scope)
    "project": os.environ.get("CHAT_PROJECT") or "WED",  # 2026-09-07: per-dashboard display filter
    "ts": _ts,
    "text": msg,
})
d = os.path.dirname(path)
fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(log, f, ensure_ascii=False, indent=1)
os.replace(tmp, path)
print(f"appended to {os.path.basename(path)} ({len(log)} in this stream)")
# Phase 2: hand the generated ts back to the shell (state file named in CHAT_TS_OUT) so the live-board post carries the
# SAME timestamp — and therefore the same deterministic id the backfill computes — never a second clock reading.
if os.environ.get("CHAT_TS_OUT"):
    open(os.environ["CHAT_TS_OUT"], "w").write(_ts)
PYEOF
_rc=$?
_live_ts="$(cat "$_TS_STATE" 2>/dev/null)"
[ "$_rc" -eq 0 ] || exit "$_rc"
# Regenerate Kam's reading surface from every stream. Never discard stderr: a
# merge that refuses (a stream that will not parse) must be visible, because the
# panel would otherwise show a log that silently omits a seat.
python3 "$STREAMS" || {
  echo "chat_reply: the append SUCCEEDED but the derived chat_log.json was NOT rebuilt." >&2
  echo "  Kam's panel is now stale by one message. Fix the stream named above and re-run:" >&2
  echo "  python3 $STREAMS" >&2
  exit 4
}
# ── Phase 2: the same entry to the live board (encrypted here; the local write already happened above) ──
if [ -n "$_live_ts" ] && [ -f "$SELF_DIR/_live_board.sh" ]; then
  . "$SELF_DIR/_live_board.sh"
  LIVE_BOARD_ATTACHMENTS="$FILE_IDS" live_board_post_message "$AGENT" "$PROJECT" "$_live_ts" "$(basename "$CHAT")" "$MSG"
else
  echo "chat_reply: live-board post skipped (no ts captured or _live_board.sh missing) — local write is intact" >&2
fi
exit 0
