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
#       failed · 22 a conflict with no merge rule (hand it back, never guess) ·
#       24 the pull FAILED with no conflicted file (git's own text printed; nothing pushed)
# Exit codes MEASURED, not assumed: the first draft documented the no-message
# case as 2 and it is 1, because ${1:?} exits 1. Read through a pipe they all
# looked like 0 — zsh has no PIPESTATUS, so the rc is captured on its own line
# (learnings/2026-08-26_zsh-has-no-pipestatus).
set -u

# W is SELF-LOCATED, never a hardcoded volume (Kam 2026-08-25: DevMASTER is the
# master, the T9 is a sync copy; learnings/2026-08-25_travel-drive-stale-pointers:
# a sync copies the stale pointer along with the valid thing it points at).
# Superseded 2026-09-07 22:3x, kept one line away per the revert rule:
#   W=/Volumes/KK_T9_External_HDD/WEDNESDAY   <- dead on the Studio; that volume
#   is not mounted there, so every run of this tool exited 2 or worse.
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
W="$(cd -P "$SELF_DIR/../.." && pwd)"
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
SP_UNION_SB="$W/2_Project_Files/tools/union_scoreboard.py"
[ -s "$SP_UNION_CHAT" ] || { echo "missing union helper: $SP_UNION_CHAT" >&2; exit 2; }
[ -s "$SP_UNION_DEC" ]  || { echo "missing union helper: $SP_UNION_DEC" >&2; exit 2; }
[ -s "$SP_UNION_SB" ]   || { echo "missing union helper: $SP_UNION_SB" >&2; exit 2; }

FEEDS="agentmail brain_state datasec_calendar linear_personal linear_wed news
       parkinglot personal_calendar secuura_error tickets"

# PHASE 0 (2026-09-08, Kam's two-agent commission): the chat is no longer one
# shared mutable file. `chat_log.json` is DERIVED and untracked; the record lives
# in the frozen legacy file plus one stream per writer. Single-writer files do
# not conflict — that is the whole point — but they are still irreplaceable, so
# they are backed up and staged by name exactly as chat_log.json used to be.
CHATFILES="chat_legacy chat_wednesday chat_tuesday chat_friday chat_kam"   # chat_friday: third seat, 2026-09-23 (absent = skipped)

# 1. Back up the irreplaceable files BEFORE any git verb touches the tree.
for f in $CHATFILES decisions; do
  [ -f "$W/$D/$f.json" ] && cp "$W/$D/$f.json" "$SC/$f.backup.json"
done

# 2. Discard the ten regenerated feeds' local churn. They are rewritten within
#    seconds, so this costs nothing — and leaving them dirty is what makes the
#    autostash reapply conflict on all ten.
for f in $FEEDS; do
  [ -f "$W/$D/$f.json" ] && git -C "$W" checkout -- "$D/$f.json" 2>/dev/null
done

# 3. Stage them by NAME, plus whatever the caller asked for. chat_log.json is
#    deliberately absent: it is derived and gitignored, so staging it would
#    re-create the shared-file conflict this phase removed.
for f in $CHATFILES decisions; do
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
# 2026-09-22 15:1x (three stranded autostashes in one day — the hide builder's five edits shipped OLD in a
# deploy, and fifteen READYs lost their SUPERSEDED-BY appends): `rebase --autostash` prints "autostash could not
# be applied" and LEAVES the stash when the re-apply conflicts, and this script's rc stayed 0. A refusal nobody
# reads. The stash COUNT is the instrument: if it grows across the pull, the work is stranded — REFUSE (rc 6),
# name the stash, and restore by hand (`git show stash@{0}:<path>`; never drop). Read `git stash list` first.
STASH_BEFORE="$(git -C "$W" stash list | wc -l | tr -d ' ')"
for round in 1 2 3 4 5 6 7 8; do
  # 2026-09-19 FETCH_HEAD race: fetch without writing FETCH_HEAD, then rebase onto the ref (never `pull`).
  OUT="$( { { git -C "$W" fetch -q --no-write-fetch-head origin main || { sleep 1; git -C "$W" fetch -q --no-write-fetch-head origin main; }; } && git -C "$W" rebase --autostash origin/main; } 2>&1)"
  case "$OUT" in
    *"Successfully rebased"*|*"up to date"*|*"Fast-forward"*) break ;;
  esac
  CONF="$(git -C "$W" diff --name-only --diff-filter=U)"
  # Key on the CONDITION, not git's wording (learnings/2026-09-10_a-detector-keyed-on-remedy-text):
  # no rebase in progress AND HEAD contains origin/main = the pull succeeded in words this
  # case list does not know; anything else with no conflicted file is a failure.
  GD="$(git -C "$W" rev-parse --absolute-git-dir)"
  if [ -z "$CONF" ] && [ ! -d "$GD/rebase-merge" ] && [ ! -d "$GD/rebase-apply" ] \
     && git -C "$W" merge-base --is-ancestor origin/main HEAD; then
    break
  fi
  if [ -z "$CONF" ]; then
    # 2026-09-17 (ledger: a-refusal-nobody-reads, the push-tool costume). This line was
    # `[ -n "$CONF" ] || break`: a pull that was neither a success nor a conflict broke
    # out SILENTLY, the push then went nowhere, and the only output was "WARNING HEAD !=
    # origin" rc 3 - twice at 00:44 with the cause (an orphaned .git/rebase-merge/ holding
    # only an autostash) findable only by bash -x. A failure the tool swallows makes the
    # one mandated push path undiagnosable. Print git's own words and stop.
    echo "safe_push: PULL FAILED (round $round) with no conflicted file - nothing pushed. git said:" >&2
    printf '%s\n' "$OUT" >&2
    [ -d "$GD/rebase-merge" ] || [ -d "$GD/rebase-apply" ] && \
      echo "safe_push: a rebase directory exists - READ what it holds (autostash?) before any rebase --quit/--abort" >&2
    exit 24
  fi
  echo "safe_push: resolving round $round"
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    case "$f" in
      "$D/chat_log.json")
        # Should be unreachable after Phase 0 (the file is gitignored). If a
        # clone predating the cutover still tracks it, the answer is not a merge:
        # it is DERIVED, so settle the index and rebuild it from the streams
        # below. Nothing is decided by picking a side of a generated file.
        git -C "$W" checkout --theirs "$f" 2>/dev/null || git -C "$W" checkout --ours "$f"
        git -C "$W" add "$f" ;;
      "$D"/chat_legacy.json|"$D"/chat_wednesday.json|"$D"/chat_tuesday.json|"$D"/chat_friday.json|"$D"/chat_kam.json)
        # One writer per stream, so this is not expected — but a stream is
        # irreplaceable and the rule must exist BEFORE it is needed. Union on
        # (ts, text), exactly as the shared log used to be resolved.
        _b="$SC/$(basename "$f" .json).backup.json"
        git -C "$W" show ":2:$f" > "$SC/c_ours.json"   2>/dev/null
        git -C "$W" show ":3:$f" > "$SC/c_theirs.json" 2>/dev/null
        [ -s "$_b" ] || printf '[]' > "$_b"   # union_chat_log.py json.loads it
        python3 "$SP_UNION_CHAT" "$SC/c_ours.json" "$SC/c_theirs.json" \
                "$_b" "$W/$f" || exit 20
        git -C "$W" add "$f" ;;
      "$D/decisions.json")
        git -C "$W" show ":2:$f" > "$SC/d_ours.json"   2>/dev/null
        git -C "$W" show ":3:$f" > "$SC/d_theirs.json" 2>/dev/null
        python3 "$SP_UNION_DEC" "$SC/d_ours.json" "$SC/d_theirs.json" \
                "$SC/decisions.backup.json" "$W/$f" || exit 21
        git -C "$W" add "$f" ;;
      0_Brain/projects_index/scoreboard.md)
        # An append-at-top table BOTH Wednesday seats write. Union on whole rows,
        # upstream order preserved, our unique rows inserted after the separator.
        # Added 2026-09-07 after this script correctly REFUSED it (rc 22) rather
        # than guessing: 557 and 556 rows unioned to 559, five unique rows across
        # the two sides. Taking either side would have dropped the other's scores.
        git -C "$W" show ":2:$f" > "$SC/sb_ours.md"   2>/dev/null
        git -C "$W" show ":3:$f" > "$SC/sb_theirs.md" 2>/dev/null
        python3 "$SP_UNION_SB" "$SC/sb_ours.md" "$SC/sb_theirs.md" "$W/$f" || exit 23
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
STASH_AFTER="$(git -C "$W" stash list | wc -l | tr -d ' ')"
if [ "$STASH_AFTER" -gt "$STASH_BEFORE" ]; then
  echo "safe_push: REFUSED rc 6 — the pull STRANDED an autostash (stash count $STASH_BEFORE -> $STASH_AFTER). Work that was in the tree is now ONLY in:" >&2
  git -C "$W" stash list | head -1 >&2
  git -C "$W" stash show --name-only 'stash@{0}' 2>/dev/null | sed 's/^/    /' >&2
  echo "  Restore by hand (git show 'stash@{0}:<path>' > <path>, backup beside), then re-run. Never 'stash drop'." >&2
  exit 6
fi

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

# 5b. The chat log is derived too (Phase 0). After a pull that may have brought
#     the OTHER agent's stream in, rebuild Kam's reading surface from every
#     stream — otherwise his panel shows this seat's half of the conversation.
#     Untracked, so it is never staged; a failure is REPORTED, never swallowed.
if [ -x "$W/2_Project_Files/tools/chat_streams.py" ] || [ -f "$W/2_Project_Files/tools/chat_streams.py" ]; then
  python3 "$W/2_Project_Files/tools/chat_streams.py" >/dev/null || \
    echo "safe_push: WARNING — chat_log.json was NOT rebuilt; Kam's panel may be missing a seat" >&2
fi

git -C "$W" push 2>&1 | tail -2
H="$(git -C "$W" rev-parse HEAD)"; O="$(git -C "$W" rev-parse origin/main)"
if [ "$H" = "$O" ]; then echo "safe_push: HEAD == origin ($H)"; else
  echo "safe_push: WARNING HEAD $H != origin $O" >&2; exit 3; fi
