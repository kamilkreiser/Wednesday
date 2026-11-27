READY FOR QA

WED build seat "wake" (WED-170 step 1), round 3. Status written 2026-11-27 13:38:38 AEDT (from `date`). Nothing outside `2_Project_Files/wake/` and the session scratchpad was written; no shared file was edited; no proposal was applied; the checker's directory was read, never written. Earlier statuses are kept unchanged at `out/STATUS_round1.md` and `out/STATUS_round2.md`.

## ROUND 3 (ANSWER-3.md and the checker's `verdict.md`, both read whole)

**Suite: 177 checks passed, 0 failed (round 2: 116). Mutants: 114 of 114 caught (round 2: 56 of 56).**

| # | Item | What changed | Checks | Mutants |
|---|---|---|---|---|
| 1 | **B1, the Blocker: two writes at once lost an acknowledged block** | The WHOLE write (first read of the state file to the second rename) now runs under an exclusive lock: `mkdir` on `0_Brain/tasks/STATE-<seat>.lock.d`, with an `owner` file holding pid, host and start time. A second writer WAITS (`HANDOVER_LOCK_WAIT`, default 20 s) and then refuses with rc 5 and a loud message; there is no path on which it writes unlocked. A lock whose holder is not running is refused at once as STALE with the exact `mv -n` recovery line; the tool removes only a lock it took itself. The checker's deterministic interleave is lifted into the suite (`tests/wrap_replace.py`, check R01) with its crash between the renames (R05), and a 200-trial concurrent test (R08). | R01 to R08 (11 checks) | 8 |
| 2 | **M1, the grants filter** | Rules rewritten as ANSWER-3 sets them (details below the table). PREMISE ENDED is no longer a dead marker. All 23 of the checker's hostile live rows are now kept and both of its controls still drop (re-run read-only against its own row list). 37 new fixture rows: its 15, and more of my own. | W05, W05b, W05c, W05d, W15, W19, W19b | 28 |
| 3 | **M2, no placeholder parts** | A missing, empty or unreadable source, a rules card without "Most reinforced", a missing `rules_card.py`, a grants file or ledger whose table header is not found, indented grant rows, or no state source at all is a FAILED BUILD: exit 2, nothing written, last line `wake_pack: FAILED — part <x>: <why>`. An empty table is believed only when its header was found. | W18a to W18o (15 fixtures), W18z, W16 | 7 |
| 4 | **M3, loud fallback; m2** | Hunk A counts the build as done only when it exits 0 AND the pack file exists and is not empty, and keeps the reason. Hunk B puts a four-line notice as the FIRST lines of the prompt (directly after `ultrathink`): the pack failed, why (the build's last line), this boot is on the legacy reads, first act is to tell Kam on the panel, write it in the boot note, and fix or ticket it. The legacy prompt under the notice is byte-identical. The doctor snippet warns when a cut-over seat has no pack. | P04, P04b, P04c, P16, P17, P15, P15b, D06 | 6 |
| 5 | **M4, proposals 2 and 3** | Both rewritten: each ADDS one paragraph scoped in words to "a seat that boots on a wake pack" and changes no existing sentence, so Tuesday's and Friday's prompts stay consistent with the rules files. Kam's sentence "the full lesson load STAYS" is left in place. New `proposed/FOR-KAM_lesson-load-ruling.md`: the sentences as they stand, what his later rulings replaced in practice, what he would be confirming, and the exact replacement if he does. | P10, P18 | 3 |
| 6 | **M5, the seed and the standing sections** | `seed --from-legacy` now carries the legacy file's `## OWED` section into OWED and its `## STANDING` section under FIRST WORK behind a named line, each with its legacy line number. If the result does not fit the cap, `--run` REFUSES with the list to place by hand. The dry report states what was taken from where by line number, and names a dated block it did not carry. | S09, S09b, S10, S11 | 3 |
| 7 | **The Minors** | m1 `--check` compares sha256 of the whole pack and sidecar against a rebuild; no line is skipped. m3 unreadable files are refusals naming the path (rc 2 for the pack, rc 4 for the handover), no traceback. m4 the three test seams are refused unless the target tree is under `/tmp`, `/private/tmp` or `/var/folders`; the engine also refuses a seat that is not its tree's. m5 any heading line of any level, indented or behind a zero-width character, that is not exactly one of the five parts is refused. m6 the gitignore proposal ignores `out/WAKE-*` only. m7 the doctor snippet shows `handover.sh`'s refusal instead of discarding it. m8 the nine missed mutants are in the suite (below). | W11h to W11j, W18o, H24, H25 to H25d, H10b to H10h, P19, D07 | 15 |
| 8 | **Census (N6)** | BEFORE is reported both ways, and the headline reduction is against the lower one (without the two sync-conflict copies). | C07 | 1 |
| 9 | **Proposal 9 (N5)** | Marked "ALL SEATS: needs Tuesday's and Friday's agreement"; not in this round's launcher diff and not in the order to apply. | P20 | 1 |

**The nine mutants of the checker's that round 2 missed, now caught:** Q01 rename order swapped (R05), Q02 changed-on-disk check removed (R06), Q03 temp read-back removed (R07), Q05 trailing newline not ensured (H22), Q07 dead marker without a date or word boundary (W05), Q08 other-seat match without a separator (W05), Q11 `--check` ignores a changed sidecar (W11i), Q15 `check` ignores a header naming another seat (H23), Q17 an unreadable state file treated as absent (H24).

Also answered from the verdict's notes: N7 (the scoreboard head and the other ledger's headlines also move to on demand for this seat: now stated in `proposed/01_launcher_boot_prompt.md`); N8 (proposal 6 no longer carries Kam's name and date for wording that is the coordinator's; proposal 7 says it changes one doctor line on the other seats' machines).

### The filter's rules now (a row is dropped only when one is proven; everything else is kept)

1. **Dead marker.** The first cell, after emphasis marks, starts with DEAD, EXPIRED, ENDED, LAPSED, CLOSED, RETIRED or END EVENT REACHED; the marker is followed by a DATE (optionally after "since", "end of", a weekday); it is not struck through; and the cell carries none of REOPENED, REVIVED, RENEWED, RE-AFFIRMED, REINSTATED, RESTORED, EXTENDED, RESUMED, REACTIVATED, RE-GRANTED, CONTINUED, STILL LIVE, NOT DEAD.
2. **Another seat's.** The first cell leads with other seats' names and a separator, this seat is not among them, and NO cell of the row names this seat (in any case, or by its short name in capitals), all / every / both / other seats, coordinators or agents, the fleet, or this seat's client. Friday serves every client, so nothing is dropped for her by this class.
3. **Past end date.** Exactly four cells; the EXPIRES cell STARTS with an explicit end form (END OF, until / through / ends / expires, or a weekday with the date); it holds exactly one date (a date written in words counts as a second); that date is before today; and the row carries none of EVENT, until further notice, extended, renewed, no end, later, continued, kept alive, moved, stands, onwards, at first, whichever, unless, at least, provisional, pending, ongoing.

### Where ANSWER-3 and the verdict differ, and which I took (ANSWER-3 asked for this)

| Point | ANSWER-3 | verdict.md | Taken |
|---|---|---|---|
| Lock mechanism | `mkdir` on a lock directory with pid and start time | `fcntl.flock` on a lock file | ANSWER-3's: it is explicit, and it leaves evidence a person can read after a death |
| What must follow a dead marker | "a date, a dash or a colon" | "a date or the word since" | the stricter: only what BOTH allow, a date (optionally after "since"). A marker followed only by a colon or a dash is kept. Every dead row in the real register has a date |
| The fallback notice | first act is to tell Kam on the panel and fix or ticket it | "say so in the boot note" | both |
| Seams | inert unless the tree is under temp or scratch | a second variable `HANDOVER_TESTING=1` | ANSWER-3's (stricter: no variable can switch a seam on for a real tree; `TMPDIR` is not consulted either) |
| `--check` | content hash | strip only the one header line | ANSWER-3's: sha256 of the whole file against a rebuild |
| Seed's OWED section | carry it, or refuse with the list if it does not fit | name it in the report, map it or tell the coordinator | ANSWER-3's (carry; refuse with the list over the cap) plus the report |

### Things the checker's own scripts will show differently now, and why

- **`scripts/race.py`, interleave part.** Its writer B pauses at the first rename until a gate file appears, and the script opens the gate only AFTER writer A returns. With the lock, A cannot finish while B holds it, so A waits 20 s and is REFUSED with rc 5 (`LOCK BUSY`, nothing written). The script's last line prints "LOST" whenever A is in neither file, without looking at A's exit code; A was not acknowledged, so nothing acknowledged is lost. Its line for writer A shows rc 5. My R01 is the same interleave with A started in the background, so both finish and both blocks are checked.
- **`scripts/race.py`, crash part.** After the engine is killed between the renames, the "next normal write" is now rc 5 with `STALE LOCK` and the recovery line, because the dead writer's lock is still there (ANSWER-3: reported, never removed silently). After the recovery line is run, the write succeeds and the archive holds the duplicate (R05 to R05c).
- **`scripts/qa_mutants.py`.** Several of its needles no longer occur in the rewritten code and will report MUTANT-ERROR; the same nine mutations are in `tests/mutants.py` against today's code.
- **Its `###` case** (accepted in round 2) is now refused by m5; a bold line is the sub-title form.

## The real run, re-measured (read-only; output only under `out/`)

Measured 2026-11-27 13:28:13 AEDT (the census script's own `date` line). Tokens are bytes/4, an estimate. The legacy pickup and today's note were growing while I worked (the pickup 290,504 bytes in round 2, 304,347 now).

| | Bytes | Est. tokens |
|---|---|---|
| BEFORE, without the 2 sync-conflict copies in `entries/` (**the honest figure**) | 1,178,129 | 294,533 |
| BEFORE, with them (the prompt says "every file in entries/") | 1,302,320 | 325,580 |
| BEFORE, without `INDEX.md` and `entries/` at all | 679,739 | 169,935 |
| AFTER: the pack alone | 72,681 | 18,171 |
| AFTER: pack + both rules files + week instruction + the two daily notes (as proposed) | 203,856 | 50,964 |
| AFTER, if Kam rules earlier notes on demand | 93,291 | 23,323 |

**Headline reduction: 82.6%** (1,178,129 to 203,856 bytes, against BEFORE without the conflict copies). Against BEFORE with them: 84.3%. Against BEFORE without the index and entries: 70.0%. Budget used by the pack: 18,171 of 60,000.

After, per part of the pack:

| Part | Source bytes | Bytes in pack | Est. tokens |
|---|---|---|---|
| a. identity (3 files, verbatim) | 9,811 | 9,944 | 2,488 |
| b. rules: "Most reinforced" verbatim | 113,173 | 6,623 | 1,656 |
| b. rules: 29 family headings with counts, fetch lines | generated | 3,626 | 907 |
| c. state: legacy pickup, first block only (no STATE file exists yet) | 304,347 | 6,299 | 1,575 |
| d. grants: 31 of 76 rows kept | 87,458 | 34,970 | 8,743 |
| e. own ledger: 20 rows reduced | 32,222 | 8,628 | 2,157 |
| f. pointers | generated | 645 | 162 |
| headings, manifest, header | | 1,946 | 487 |
| **total** | | **72,681** | **18,171** |

### The real register under the new rules: 76 rows, 45 dropped, 31 kept

| | Round 2 | Round 3 | Lines (round 3) |
|---|---|---|---|
| Dropped: dead marker | 22 | 21 | 10, 18, 19, 24, 29, 30, 33, 35, 39, 41, 48, 53, 54, 55, 57, 61, 62, 64, 68, 69, 72 |
| Dropped: another seat's | 24 | 20 | 11, 15, 16, 17, 21, 22, 23, 25, 26, 27, 28, 32, 37, 42, 43, 50, 63, 97, 98, 104 |
| Dropped: past end date | 8 | 4 | 49, 59, 126, 142 |
| Kept: this seat's | 10 | 10 | 9, 12, 20, 36, 38, 40, 45, 46, 47, 58 |
| Kept: unclassified | 12 | 21 | 13, 14, 31, 34, 44, 51, 52, 56, 60, 65, 66, 67, 70, 71, 73, 74, 75, 111, 125, 134, 141 |

- Every one of the 45 rows dropped now is among the 53 the checker judged "right". None is new.
- Nine rows that round 2 dropped are now kept, each by a rule ANSWER-3 set: line 65 (PREMISE ENDED is no longer a marker); lines 13, 14, 31 and 56 (another seat leads, but a cell says every agent, the fleet or every seat, or names this seat); lines 67, 125, 134 and 141 (a past end date, but the row carries a keep-alive word or names this seat). The pack grew by about 11 KB for it; ANSWER-3 accepts that price.
- Line 26 (another seat's HOLD) is still dropped for the Wednesday seat, as the checker judged right. On fixtures, a Friday build keeps that shape of row (check W19, fixture G54) and a Tuesday build shows it as her own (W19b). Friday's real files were not read.
- The sidecar `out/WAKE-wednesday.dropped.txt` lists all 45 with class, line number and proof. With `--trust-expired-heading`: 27 kept, pack 68,442 bytes.

### The dry seed against the real legacy pickup

`handover.sh seed --from-legacy`: rc 0, nothing written, an 8,031-byte block (cap 10,000; no fault, so `--run` would be accepted). Saved at `out/seed_dry_wednesday.block.txt`, the report beside it. From the report: newest block heading at line 11, body lines 12 to 18 (4 bullets mapped by label, 3 unknown or plain bullets under FIRST WORK); standing section `## OWED (in order, after the floor)` at line 933, lines 934 to 938, 5 non-blank lines, 1,010 bytes, into OWED; standing section `## STANDING (unchanged; the lessons carry the detail)` at line 940, lines 941 to 943, 3 non-blank lines, 685 bytes, under FIRST WORK. Those are the 8 lines the checker found left behind (1,695 bytes by my count, 1,694 by its).

## What exists (bytes)

| File | Bytes | Note |
|---|---|---|
| `ANSWER-1.md` | 3,873 |  |
| `ANSWER-2.md` | 1,597 |  |
| `ANSWER-3.md` | 8,118 |  |
| `BRIEF.md` | 9,420 |  |
| `DESIGN.md` | 10,846 | one page, plus round 2 and round 3 sections |
| `handover.sh` | 7,123 | the one-block handover: seat guard, seam guard, clock from `date`, argument checks |
| `handover_core.py` | 32,534 | its engine: validation, lock, conservation assert, atomic writes, seed |
| `out/STATUS_round1.md` | 12,975 |  |
| `out/STATUS_round2.md` | 16,656 |  |
| `out/WAKE-wednesday.dropped.txt` | 6,858 |  |
| `out/WAKE-wednesday.md` | 72,681 |  |
| `out/WAKE-wednesday.trust-expired-heading.dropped.txt` | 7,524 |  |
| `out/WAKE-wednesday.trust-expired-heading.md` | 68,442 |  |
| `out/census_wednesday.txt` | 3,749 |  |
| `out/seed_dry_wednesday.block.txt` | 8,031 |  |
| `out/seed_dry_wednesday.report.txt` | 1,064 |  |
| `out/tests_last_mutants.txt` | 10,141 |  |
| `out/tests_last_run.txt` | 16,576 |  |
| `proposed/01_launcher_boot_prompt.diff` | 8,749 |  |
| `proposed/01_launcher_boot_prompt.md` | 4,812 |  |
| `proposed/02_root_CLAUDE_md.md` | 3,486 |  |
| `proposed/03_brain_CLAUDE_md.md` | 1,574 |  |
| `proposed/04_doctor_check.md` | 2,382 |  |
| `proposed/05_gitignore.md` | 2,017 |  |
| `proposed/06_wrap_step.md` | 2,018 |  |
| `proposed/07_doctor_pickup_warning.md` | 2,578 |  |
| `proposed/08_nas_staleness.md` | 1,525 |  |
| `proposed/09_prompt_backtick.md` | 2,298 |  |
| `proposed/FOR-KAM_lesson-load-ruling.md` | 3,949 | the question for Kam (round 3) |
| `proposed/README.md` | 4,335 |  |
| `proposed/build_launcher_diff.py` | 3,090 |  |
| `proposed/doctor_check_snippet.sh` | 2,680 |  |
| `proposed/launcher_hunk_A.sh` | 1,778 |  |
| `proposed/launcher_hunk_B.sh` | 6,305 |  |
| `tests/mutants.py` | 23,304 | the 114 mutants |
| `tests/run.sh` | 745 | the runner |
| `tests/run_tests.py` | 101,577 | 177 checks in seven groups |
| `tests/seam_fixture/WEDNESDAY/0_Brain/tasks/README.txt` | 146 | a non-temp tree for check H25; nothing is written in it |
| `tests/wrap_replace.py` | 2,088 | the wrapper lifted from the checker's `scripts/wrap.py` (pause, crash, edit, truncate) |
| `wake_census.sh` | 7,188 | before (both ways) and after, in bytes and estimated tokens |
| `wake_pack.py` | 39,119 | the fixed-budget wake pack: build, filter, sidecar, `--check` |
| `_quarantine_2026-11-27/__pycache__/` | | a cache directory from round 1; moved, not removed |

## Tests

Run: `bash 2_Project_Files/wake/tests/run.sh` (about 2 minutes; the 200-trial race is about 40 s of it) and `bash 2_Project_Files/wake/tests/run.sh --mutants` (about 20 minutes; `WAKE_MUTANT_GROUPS=W` runs one group's mutants). The scratch directory must be under a system temp directory, because the handover seams are honoured only there; the runner says so and stops if it is not.

**177 passed, 0 failed.** By group: H handover 53, W wake pack 52, P launcher and text proposals 31, S seed 15, R lock and races 11, C census 8, D doctor snippet 7.

R08's own count line: `trials 200, both acknowledged 200, one refused 0, acknowledged block LOST 0, base block not once in archive 0`.

**Mutants: 114 of 114 caught.** The list is `tests/mutants.py`. Four mutants also crash their group after the named check has gone red; a crash is reported as a failure, never as a skip. The per-item mutant counts in the table above are my own tally of that list by subject; the total is the run's. The lock mutant ("the lock is removed") turns R01 and R02 red.

Tail of the last run (`out/tests_last_run.txt`):

```
PASS R07 a temp file that does not read back as written stops the write: rc 4, state and archive unchanged, the temp file named
PASS R08 200 trials of two simultaneous writes: every acknowledged block is in the state file or the archive
     R08 counts: trials 200, both acknowledged 200, one refused 0, acknowledged block LOST 0, base block not once in archive 0
checks: 177 passed, 0 failed, 177 total (groups HWCPDSR)
```

Tail of the mutant run (`out/tests_last_mutants.txt`):

```
RED-AS-EXPECTED m113 M3: doctor is silent when a cut-over seat has no pack :: went red: D06
RED-AS-EXPECTED m114 m7: doctor discards handover.sh's stderr :: went red: D07
mutants: 114 of 114 caught (each tool broken in a scratch copy; the lane's files are untouched)
```

Note for the checker: groups P and D read the real launcher, `CLAUDE.md`, `0_Brain/CLAUDE.md`, `.gitignore`, `doctor.sh` and `scheduler/nas_staleness.sh` (read only). Once a proposal is applied, P05, P07, P10, P11, P13 and P14 go red by design. Check H25 uses `tests/seam_fixture/`, a tree in the lane that is deliberately not under a temp directory, to prove the seams are refused there; nothing is written in it.

## Deviations from the brief and the answers, each with its reason

1. **`handover.sh` has an engine file, `handover_core.py`** (round 1): byte-exact work is safe in Python.
2. **Seat comes from `tools/seat_note.sh`, which sources `seat_resolve.sh`** (round 1): an unknown tree refuses.
3. **Extra verb `handover.sh check`** (round 1).
4. **A new exit code, 5**, for a held or stale lock, so a caller can tell "run it again" from a refused block (3) or an I/O fault (4).
5. **After a writer dies, the next write is refused until a person runs the recovery line.** ANSWER-3 says a stale lock is never removed silently; the cost is that a rotation after a crash needs one `mv -n`. The message gives the exact line.
6. **Dead marker needs a date** (the stricter of the two texts, see the table above). A row marked `DEAD:` with no date is kept.
7. **Two weekday idioms do not count as "naming the seat"**: the register's clock stamp (`` `date -j`: Wednesday ``) and the name directly followed by a date. The seats are named after weekdays and the register stamps weekday names in most rows; without this, nearly every other seat's row would be kept for a stamp. A fixture row with a stamp AND a real mention is kept (G59), and a mutant covers the case where the exclusion swallowed the text after it.
8. **The seat's client is one word per seat** (Secuura for Wednesday, Datasec for Tuesday). "General" is not treated as Wednesday's client word, because Friday's own rows use it for her project; a row that binds this seat by a general project it does not name will not be caught by the client rule (the seat-name and all-seats rules still apply).
9. **m5 is stricter than round 2 in one visible way:** `## FLOOR (4 seats)` is refused; the heading must be exactly `## FLOOR`. A sub-title inside a part is a bold line.
10. **The M2 list is a little longer than ANSWER-3's:** a missing `rules_card.py`, an empty identity file, and "no state file and no legacy pickup" also fail the build, on the same principle.
11. **The doctor snippet treats a seat as "on the pack" once its state file exists**, and warns about a missing pack only from then on, so the warning does not fire on Tuesday's and Friday's machines before they adopt it.
12. **`--check` rebuilds with the stamp it reads from the pack's own front matter** and compares hashes; a pack whose front matter has no stamp is a fault.
13. **The test runner is Python behind `tests/run.sh`; mutants are in `tests/mutants.py`** (round 1 and 3).
14. **Read-only commands outside the brief's list:** `git check-ignore` with a scratch excludes file, `patch` on scratch copies. No `git status` this round.

## What I could not fix, or did not test

- **Nothing in ANSWER-3's nine items is left unfixed.** The limits below are what remains untested.
- No real launch; no real handover or seed write (against the real tree: `--where`, `check` and the dry `seed` only); `doctor.sh` and `nas_staleness.sh` not run with the proposals in them.
- The lock was tested with two writers on one machine. A lock left by a writer on ANOTHER host (the tree is synced between machines) cannot be judged dead by its pid, so it is waited on and then refused with the recovery line; that path is covered only by R04's shape (no usable owner), not by a real second host. The lock directory is in the gitignore proposal so it should not travel by git; a drive sync could still copy it.
- Three or more simultaneous writers, and a writer starved past 20 s by a queue of others, were not tested.
- Durability across a power cut: temp files are fsynced, the directory is not.
- The filter was run on the real register for the Wednesday seat only. Tuesday's and Friday's packs ran on fixtures; how their real rows classify is not measured.
- The keep-alive word list is English prose matching. A row that keeps itself alive in words the list does not hold, with an explicit past end date and nothing else, would still be dropped; the sidecar is the backstop for that.
- The seed's label map is drawn from the Wednesday pickup's labels; other seats' legacy files were not read.
- The statusline percentage after a pack boot; real token counts (bytes/4 only).

## QUESTIONS

None open.
