# DESIGN: wake pack and one-block handover (WED-170 step 1)

One page. Written before the build; choices that are mine carry a one-line reason.

## Files

| File | Role |
|---|---|
| `handover.sh` | thin bash front: resolves the seat, reads the clock with `date`, hands over to `handover_core.py` |
| `handover_core.py` | validation, conservation assert, atomic writes (bytes are exact in Python; bash 3.2 strips trailing newlines) |
| `wake_pack.py` | builds or checks one pack file per seat under a token budget |
| `wake_census.sh` | before (the current prompt's mandated whole reads, census A3/A4 method) beside after (the pack) |
| `proposed/` | diffs and replacement text for shared files; none applied |
| `tests/run.sh` | runs `tests/run_tests.py` on generated fixtures in a scratch tree; `--mutants` breaks each tool and expects red |

## handover

- **Seat**: `tools/seat_note.sh` (which sources `seat_resolve.sh`). Why: it is the existing guard for seat-owned writes; an unrecognised tree or a `WED_AGENT` that disagrees with the tree refuses, where bare `seat_resolve` would default to wednesday.
- **State file** = a generated header (seat, written stamp, block bytes, block sha256) + the block. The block is the bytes from stdin, one trailing newline ensured.
- **One block is a property of the format**: exactly the five `##` headings, each once, each with text under it, no other `##` heading. Two blocks pasted into one write are refused as duplicate headings. Why the sha in the header: `handover.sh check` can then see a hand-appended block, which a sentence could not.
- **Write**: compose new state and new archive in memory; assert conservation there (old block found byte-for-byte at the computed offset; archive growth = heading + old block + separator; every earlier archive byte still present) before any file is touched; write temp files beside the targets; read them back and compare; confirm the files on disk did not change meanwhile; rename archive first, state second. Why that order: a crash between the two leaves the old block in both files (a duplicate), never in neither.
- **Archive entry heading is `#` (h1)**, because the block's own parts are `##`.
- **Refusals** (rc 3, all faults printed in one go): empty; over the cap (`HANDOVER_CAP_BYTES`, default 10000) with per-part sizes largest first; a clock with an x digit (note_entry.sh's pattern); heading faults. rc 2: seat or usage. rc 4: conservation or I/O.
- **No override for the x-clock refusal.** Why: the brief says refuses; an override weakens it. Offered under QUESTIONS.
- Added verb `check` (not in the brief). Why: the doctor proposal needs a command that can say "one block".
- Never reads or writes `NEXT-PICKUP*.md`.

## wake pack

- Sources by seat come from one table (ledger and legacy pickup names, the same mapping the launcher holds).
- Every part is a list of sections; the manifest has one row per section: source path, source bytes, bytes in the pack, estimated tokens (bytes/4, rounded up), then an overhead row and the total.
- **Grants filter** drops a row only on proof, in this order:
  1. *dead marker*: the first cell, after markup, STARTS with `DEAD`, `EXPIRED`, `ENDED` or `LAPSED` (upper case). Why "starts with": the word DEAD inside a live row's prose must not kill it.
  2. *another seat*: the first cell starts with another seat's name in upper case followed by `:`, `(` or a dash, AND this seat's name appears nowhere in that cell.
  3. *past end date*: the row has exactly four cells, the EXPIRES cell starts with an end-date form (`END OF SUNDAY 2026-11-08`, `MONDAY 2026-11-09`, `until 2026-11-20`), that date is before today, no later date stands in that cell, and neither cell says changed, extended, renewed, re-affirmed or re-read.
  Everything else is kept. A kept row that leads with this seat's name is "this seat's"; any other kept row is "unclassified" and counted.
- **Rows under the file's `## Expired` heading** are kept by default and counted separately. Why: the brief lists three drop classes and a heading is none of them (stricter reading). `--trust-expired-heading` drops them; both numbers go in STATUS.
- **State part**: the STATE file whole; if absent, a plain statement plus the legacy pickup's first `##` block only.
- **Ledger part**: date, first bold run, and the sentence after `Rule:` or `Rule (...):`; a row without one says so.
- **Budget**: over budget exits 3, writes nothing, prints parts largest first.
- **`--check`**: missing pack; any source (or the tool) newer than the pack; pack built on an earlier date (the date filter depends on today); content differs from a rebuild.
- Globs go through one function that skips `(conflict_on_` and `.pre-` names.
- Test seams: `--root`, `--today`.

## census

Re-measures the A3 list from the files (same items as A4: both rules files, identity, people, rules card or the by-tier digest, own ledger, pickup, grants, tasks, INDEX, every file in `entries/`, week instruction, yesterday's and today's notes). After = the pack alone, and the pack plus what the proposed prompt still mandates whole.

## proposals

The launcher change is additive only (zero removed lines), every added line sits inside `if [ "$AGENT" = "wednesday" ]`, and the new prompt reuses the old one's head and tail by slicing rather than a second copy. A harness evaluates the real prompt region for each seat with and without the change and compares bytes.

## Round 2 (ANSWER-1, 2026-11-27)

- **x-clock override**: `HANDOVER_ALLOW_XCLOCK='<reason, 15 characters or more>'`. The reason is stored in the block's header (`xclock_override:`) because the archive heading is written later, when the block is replaced; the heading then carries it. No x-clock in the block: nothing is recorded.
- **Dead markers** now also CLOSED, RETIRED, PREMISE ENDED, END EVENT REACHED; still only as the leading words of the first cell.
- **Sidecar** `<pack name>.dropped.txt`: one line per dropped grant row (class, line in the grants file, proof, first 80 characters of the first cell). Written before the pack; `--check` covers it; the pack names it.
- **`handover.sh seed --from-legacy`**: dry by default. Each bullet of the legacy pickup's newest block goes to a part by its leading bold label (FLOOR; anything with OWED; FIRST WORK or NEXT; CARD or "for Kam"; GRANT). A bullet whose label is not recognised, and a plain bullet, go under FIRST WORK verbatim: nothing is dropped. Why FIRST WORK: an unrecognised line is the one the successor should read first. Legacy text with an x-digit clock is seeded with a fixed, recorded reason. Refuses when a state file exists.
- **Doctor snippet takes the seat from `handover.sh --where`**, not from doctor's `_DOC_AGENT`, which defaults to wednesday on a Tuesday tree.
- **Daily notes** are one line of hunk B: `WAKE_NOTES="whole"` or `"ondemand"`.

## Round 3 (ANSWER-3 and the checker's verdict, 2026-11-27)

- **The write lock (Blocker B1).** `mkdir` on `0_Brain/tasks/STATE-<seat>.lock.d` is the lock; an `owner` file inside holds pid, host and start time. It is taken before the first read of the state file and released after the second rename, so the read, the conservation assert, both temp files and both renames are one critical section. A second writer polls for `HANDOVER_LOCK_WAIT` seconds (default 20, clamped to 0.2 to 300) and then refuses with rc 5; there is no path on which it writes without the lock. A lock whose holder (same host) is not running is refused at once as STALE with the exact `mv -n` recovery line. The tool removes only the lock it took itself. Why mkdir and not flock: ANSWER-3 names it, it leaves evidence a person can read after a death, and it needs no open descriptor to survive.
- **Dead marker, the stricter of the two texts.** ANSWER-3 says the marker must be followed by "a date, a dash or a colon"; the verdict says "a date or the word since". I took what both allow: a DATE (optionally after since / end of / a weekday). Every dead row in the real register has one. A marker with only a colon or a dash after it is kept.
- **"Names this seat"** is any occurrence of the seat's name in any cell, in any case, except two forms that are a weekday by construction (the register's clock stamp, and the name directly followed by a date). The seats are named after weekdays; without that exception almost every other-seat row would be kept for a stamp.
- **A seat that serves every client (friday) drops nothing by the other-seat class.** Why: any other seat's hold can bind a project she drives.
- **Past end date** needs an explicit end form at the start of the EXPIRES cell, exactly one date in the cell (dates written in words count as a second date), and no keep-alive word anywhere in the row. "Not renewed" / "not extended" are removed before the word search: "Not renewed by inference" is the register's stock phrase and negates a renewal.
- **A failed build, not a placeholder (M2).** Every source is read through one function that raises on missing, empty or unreadable; structure checks raise on a card without its top section, a grants file or ledger without its table header, indented table rows, a state source without a block. Exit 2, nothing written, last line `wake_pack: FAILED — part ...`. An empty table is believed only when its header was found.
- **`--check` compares sha256 of the whole file** against a rebuild made with the stamp read from the pack's own front matter (the sidecar's own second line). No line is skipped, so nothing can hide behind a prefix.
- **Loud fallback (M3).** Hunk A records why in `WAKE_FAIL`; hunk B puts a four-line notice directly after the prompt's `ultrathink` line. The legacy prompt below it is byte-identical. The build's last line always starts `wake_pack: FAILED` on a failure, so "why" is one line.
- **Seams inert in production (m4).** Honoured only when the target tree's real path is under `/tmp`, `/private/tmp` or `/var/folders`. The list is fixed in the code and `TMPDIR` is not consulted: a variable the caller sets must not be able to switch a seam on. The engine also refuses a seat that is not its tree's.
- **Headings (m5).** Inside a block the only heading lines are the five parts, written exactly. Any other line that Markdown would read as a heading (levels 1 to 6, indented, or behind a zero-width character) is refused. Consequence: sub-titles are bold lines, and `## FLOOR (4 seats)` is refused where round 2 accepted it.
- **Seed (M5).** Standing sections are the `## ` headings outside the newest block that START with OWED or STANDING. OWED lines go into OWED, STANDING lines under FIRST WORK behind a named bold line, both with the legacy line number. A dated block whose heading merely mentions OWED is reported as not carried. If the result fails validation (the cap included) `--run` refuses with the list.
