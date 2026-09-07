#!/bin/bash
# safe_push.sh — commit + pull --rebase + push the WEDNESDAY repo without ever
# risking the two irreplaceable files in 0_Brain/dashboard/data/.
#
# WHY THIS EXISTS (enforcement, not advice). On 2026-09-07 a blanket
# `git checkout <sha> -- 0_Brain/dashboard/data` as a conflict resolution
# destroyed FOUR of Kam's rulings and three whole cards. He re-ruled three of
# them fifty minutes later because his panel showed them open again. They were
# unrecoverable: the cards had never been committed, so git held nothing.
#
# That directory holds TWO irreplaceable files and ten regenerated feeds:
#   chat_log.json   — Kam's conversation. Merge by UNION on (ts, text).
#   decisions.json  — the decision queue, i.e. Kam's RULINGS. Merge by UNION on
#                     card id, KEEPING THE RULED VERSION.
#   the other ten   — rewritten continuously by the dashboard server. Discarding
#                     their local churn costs nothing and is what stops the
#                     autostash reapply conflicting on all ten, every time.
#
# Measured on 2026-09-07, twice in one evening, and this is why union is not
# optional: chat sides of 1677 and 1669 unioned to 1679; decisions sides of 179
# and 177 unioned to 180 — and one of those sides still had a card OPEN that the
# other had ruled. Equal counts prove nothing. Every side was missing something.
#
# Usage: safe_push.sh "<commit message>" [extra path to stage ...]
#   chat_log.json and decisions.json are always staged BY NAME. Never `add -A`.
# Exit: 0 pushed · 1 no commit message (bash's ${1:?}) · 2 usage/env, incl. a
#       missing union helper · 3 pushed but HEAD != origin · 20/21 a union script
#       failed · 22 a conflict with no merge rule (hand it back, never guess)
# Exit codes MEASURED, not assumed: the first draft documented the no-message
# case as 2 and it is 1, because ${1:?} exits 1. Read through a pipe they all
# looked like 0 — zsh has no PIPESTATUS, so the rc is captured on its own line
# (learnings/2026-08-26_zsh-has-no-pipestatus).
set -u

W=/Volumes/KK_T9_External_HDD/WEDNESDAY
D=0_Brain/dashboard/data
MSG="${1:?usage: safe_push.sh \"<commit message>\" [path ...]}"; shift || true

SC="${SAFE_PUSH_SCRATCH:-${TMPDIR:-/tmp}/safe_push.$$}"
mkdir -p "$SC" || { echo "cannot create scratch $SC" >&2; exit 2; }

# The union helpers live BESIDE this script in a tracked path, on purpose: a
# mechanism a successor must run is recorded by its PATH, and a script pointing
# at a session scratchpad is a ghost the moment the session ends
# (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
SP_UNION_CHAT="$W/2_Project_Files/tools/union_chat_log.py"
SP_UNION_DEC="$W/2_Project_Files/tools/union_decisions.py"
[ -s "$SP_UNION_CHAT" ] || { echo "missing union helper: $SP_UNION_CHAT" >&2; exit 2; }
[ -s "$SP_UNION_DEC" ]  || { echo "missing union helper: $SP_UNION_DEC" >&2; exit 2; }

FEEDS="agentmail brain_state datasec_calendar linear_personal linear_wed news
       parkinglot personal_calendar secuura_error tickets"

# 1. Back up the two irreplaceable files BEFORE any git verb touches the tree.
for f in chat_log decisions; do
  [ -f "$W/$D/$f.json" ] && cp "$W/$D/$f.json" "$SC/$f.backup.json"
done

# 2. Discard the ten regenerated feeds' local churn. They are rewritten within
#    seconds, so this costs nothing — and leaving them dirty is what makes the
#    autostash reapply conflict on all ten.
for f in $FEEDS; do
  [ -f "$W/$D/$f.json" ] && git -C "$W" checkout -- "$D/$f.json" 2>/dev/null
done

# 3. Stage the two by NAME, plus whatever the caller asked for.
for f in chat_log decisions; do
  [ -f "$W/$D/$f.json" ] && git -C "$W" add "$D/$f.json"
done
for p in "$@"; do git -C "$W" add "$p" || exit 2; done

if git -C "$W" diff --cached --quiet; then
  echo "safe_push: nothing staged"
else
  git -C "$W" commit -m "$MSG" >/dev/null || { echo "commit failed" >&2; exit 2; }
  echo "safe_push: committed — $MSG"
fi

# 4. Pull, resolving each conflict by the file's OWN rule. Never by side,
#    never by directory.
for round in 1 2 3 4 5 6 7 8; do
  OUT="$(git -C "$W" -c rebase.autoStash=true pull --rebase 2>&1)"
  case "$OUT" in
    *"Successfully rebased"*|*"up to date"*|*"Fast-forward"*) break ;;
  esac
  CONF="$(git -C "$W" diff --name-only --diff-filter=U)"
  [ -n "$CONF" ] || break
  echo "safe_push: resolving round $round"
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    case "$f" in
      "$D/chat_log.json")
        git -C "$W" show ":2:$f" > "$SC/c_ours.json"   2>/dev/null
        git -C "$W" show ":3:$f" > "$SC/c_theirs.json" 2>/dev/null
        python3 "$SP_UNION_CHAT" "$SC/c_ours.json" "$SC/c_theirs.json" \
                "$SC/chat_log.backup.json" "$W/$f" || exit 20
        git -C "$W" add "$f" ;;
      "$D/decisions.json")
        git -C "$W" show ":2:$f" > "$SC/d_ours.json"   2>/dev/null
        git -C "$W" show ":3:$f" > "$SC/d_theirs.json" 2>/dev/null
        python3 "$SP_UNION_DEC" "$SC/d_ours.json" "$SC/d_theirs.json" \
                "$SC/decisions.backup.json" "$W/$f" || exit 21
        git -C "$W" add "$f" ;;
      0_Brain/learnings/_boot_digest*.md)
        # derived from the lesson files; settle it, then regenerate from source below
        git -C "$W" checkout --theirs "$f" 2>/dev/null || git -C "$W" checkout --ours "$f"
        git -C "$W" add "$f" ;;
      *)
        echo "safe_push: REFUSING — no merge rule for $f. Resolve by hand." >&2; exit 22 ;;
    esac
  done <<< "$CONF"
  GIT_EDITOR=true git -C "$W" rebase --continue >/dev/null 2>&1
done

# 5. A digest is derived: after any conflict, rebuild it from the lesson files
#    rather than leaving whichever side happened to win.
if ! git -C "$W" diff --quiet -- 0_Brain/learnings/_boot_digest.md \
                                 0_Brain/learnings/_boot_digest_by_tier.md 2>/dev/null; then
  python3 "$W/2_Project_Files/tools/boot_digest.py" >/dev/null 2>&1
  python3 "$W/2_Project_Files/tools/boot_digest.py" --by-tier >/dev/null 2>&1
  git -C "$W" add 0_Brain/learnings/_boot_digest.md 0_Brain/learnings/_boot_digest_by_tier.md 2>/dev/null
  git -C "$W" diff --cached --quiet || \
    git -C "$W" commit -m "digests regenerated from the lesson files after a conflict" >/dev/null
fi

git -C "$W" push 2>&1 | tail -2
H="$(git -C "$W" rev-parse HEAD)"; O="$(git -C "$W" rev-parse origin/main)"
if [ "$H" = "$O" ]; then echo "safe_push: HEAD == origin ($H)"; else
  echo "safe_push: WARNING HEAD $H != origin $O" >&2; exit 3; fi
