#!/bin/bash
# chat_reply.sh — mirror a Wednesday conversational reply into the dashboard chat.
#
# WHY (Kam, 2026-08-17): the terminal interleaves conversation with fleet
# mechanics, so what he is reading scrolls away under agent traffic. The
# dashboard chat tile is the STABLE conversation surface: substantive replies
# to Kam are mirrored here (short form, pointers to documents for anything
# long). Fleet mechanics NEVER go through this script.
#
# Usage: chat_reply.sh [--project <Datasec|Secuura|WED>] "message text"
# Appends {role: "wednesday", seat, project, ts, text} to
# 0_Brain/dashboard/data/chat_log.json atomically (write temp + mv). Never
# discards stderr. Refuses empty input.
#
# --project (Kam, 2026-09-07 11:12): tags the entry so each dashboard can choose
# which project's replies it displays / auto-speaks (per-browser filter, WED on
# by default). Omitted → "WED"; entries with no field at all read as "WED".
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
CHAT="$PROJECT_DIR/0_Brain/dashboard/data/chat_log.json"
PROJECT="WED"
if [ "${1:-}" = "--project" ]; then
  [ -n "${2:-}" ] || { echo "chat_reply: --project needs a value (Datasec|Secuura|WED)" >&2; exit 2; }
  PROJECT="$2"; shift 2
fi
MSG="${1:-}"
[ -n "$MSG" ] || { echo "chat_reply: empty message refused" >&2; exit 2; }
[ -f "$CHAT" ] || { echo "chat_reply: no chat log at $CHAT" >&2; exit 1; }

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
CHAT_FILE="$CHAT" CHAT_PROJECT="$PROJECT" python3 - "$MSG" <<'PYEOF'
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
log.append({
    "role": "wednesday",
    "seat": __import__("socket").gethostname(),  # 2026-09-07: which machine wrote this (autoplay scope)
    "project": os.environ.get("CHAT_PROJECT") or "WED",  # 2026-09-07: per-dashboard display filter
    "ts": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(),
    "text": msg,
})
d = os.path.dirname(path)
fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(log, f, ensure_ascii=False, indent=1)
os.replace(tmp, path)
print(f"mirrored to dashboard chat ({len(log)} messages)")
PYEOF
