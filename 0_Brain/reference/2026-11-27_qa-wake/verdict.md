NO GO

QA verdict on the lane `2_Project_Files/wake/` (WED-170 step 1, round 2). Independent checker; written 2026-11-27 12:55:27 AEDT (from `date`). I edited nothing in the lane (37 file hashes identical before and after: `lane_hashes_before.txt`, `lane_hashes_after.txt`), nothing in `0_Brain/tasks/`, and the launcher's sha256 is unchanged (`480c56c5...`). Every write test ran on scratch trees.

**What decides the verdict.** One Blocker, in the handover tool: two writes started at the same moment can lose a block that the tool reported as written. Everything else that the brief called dangerous held: no live grant binding the Wednesday seat is dropped today (54 of 54 dropped rows judged; 53 right, 1 doubtful, 0 wrong), the other two seats' prompt text is byte-identical, a failed pack build falls back to the legacy prompt, and nothing new can execute at launch. With the Blocker fixed and the five Majors answered, this is a GO WITH NOTES.

The builder's own numbers reproduce: 116 checks passed, 0 failed (`suite_run.txt`); 56 of 56 mutants caught (`suite_mutants.txt`); the stored launcher diff equals a fresh build of it.

## FINDINGS

### Blocker

**B1. Two handover writes at the same moment lose an acknowledged block.**
- Ran: `scripts/race.py` on scratch `WEDNESDAY` trees (a copy of `handover.sh` and `handover_core.py`, the real seat guard files). Three parts: 150 trials of two `handover.sh write --stdin` processes started together with 9 KB blocks; one deterministic interleave using a wrapper (`scripts/wrap.py`) that runs the unmodified engine with `os.replace` paused; a second run of 40 trials that captured stderr.
- Printed (`handover_race_crash.txt`): `NATURAL RACE: 150 trials of two simultaneous writes: both acknowledged 102; one refused/errored 48; acknowledged block LOST 23`. Interleave: `writer A rc 0 (handover: written ...); writer B rc 0 (handover: written QA-B)` then `final state is B True; S0 in archive x1; A in archive x0 ... block A LOST (acknowledged 'written', now in neither file)`. Second run (`extra_race_reason_and_seed_run.txt`): 4 lost in 40; 10 refusals with the tool's own "changed on disk while this write was being prepared" message.
- Why: both writers read the same old state, both pass the "changed on disk" check, and the second pair of renames overwrites the first writer's state and archive. The check narrows the window; it does not close it. The loser's block is in neither file and both exit 0.
- Reach: it needs two writers for one seat at once (a seat's checkpoint beside a rotation or wrap script, or a sub-agent). The proposed prompt tells the seat to write "at every checkpoint, rotation and wrap", so two writers is a normal case, not an exotic one.
- Smallest fix: take an exclusive lock for the whole of `cmd_write` from the first read to the second rename (`fcntl.flock` on a lock file such as `0_Brain/tasks/STATE-<seat>.lock`, or on the tasks directory's descriptor), and add a test that runs two writes together and asserts every acknowledged block is the state or in the archive. About ten lines.

### Major

**M1. The grants filter's "proof" does not hold for rows that have not been written yet.** No real row is wrongly dropped today (table below). But 15 of 23 hostile LIVE rows I wrote were dropped.
- Ran: `scripts/wp2.py`, calling `classify_grant` on a copy of the tool, seat wednesday, today 2026-11-27. Output: `filter_hostile_and_check_attack.txt`.
- Dropped as "dead marker": a marker word used as the subject (`CLOSED PRs may be reopened...`, `DEAD LETTER queue may be purged`, `EXPIRED certificates may be renewed...`, `RETIRED laptops may be wiped`), a hyphenated word (`CLOSED-LOOP deploys allowed`), a struck-through marker followed by a revival (`~~**EXPIRED 2026-11-20**~~ **REVIVED by Kam...`), and `CLOSED 2026-11-20, then REOPENED by Kam`.
- Dropped as "other seat": `TUESDAY (and ALL SEATS): ...`, and a row led by FRIDAY whose scope cell says it binds WEDNESDAY too. Only the first cell is searched for this seat's name, and "all seats" is not looked for at all.
- Dropped as "past date": an EXPIRES cell that starts with the GIVEN date, one that starts with a START date (`2026-11-20 onwards, until further notice`), `END OF SUNDAY 2026-11-22, then kept alive until further notice`, `... or the EVENT, whichever is LATER`, `Sunday 2026-11-22 at first; Kam moved it to Mon 30 Nov`, `... CONTINUED by Kam on the 23rd`. A bare ISO date at the start of the cell counts as an end date, and only the words chang, extend, renew, re-affirm and re-read stop the drop.
- The builder's suite does not guard two of these edges: my mutants Q07 (marker without a word boundary) and Q08 (other-seat match without a separator) both pass all 30 W checks.
- Smallest fix: (a) a dead marker counts only when it is followed by a date or the word "since", and never when it is struck through or the cell also says REOPENED, REVIVED, RENEWED or RE-AFFIRMED; (b) the other-seat drop searches the WHOLE row for this seat's name and for all seats, every seat, both seats, fleet; (c) the past-date drop needs an explicit end form (END OF, until, a weekday with the date) and is cancelled by "until further notice", "later", "continu", "kept alive", "moved", "stands"; (d) a fixture row for each of the 15.

**M2. A pack part can shrink to one placeholder line while the build exits 0, and the prompt then tells the seat not to read the source.**
- Ran: `scripts/wp_tests.py` section 3 on a scratch tree built from copies of the Wednesday seat's sources. Output: `wakepack_attacks.txt`.
- Exit 0 and a pack written for: rules card missing (pack 51,929 B, one line `NO RULES CARD ...`); rules card of 0 bytes; rules card whose "Most reinforced" heading is renamed (one line `has no 'Most reinforced' section`); grants file missing (`No grants file`); grants file empty; grants table indented by one space (`0 rows in the file, 0 kept here`, although 76 rows are there); ledger missing; ledger with no dated row; `rules_card.py` missing; persona of 0 bytes.
- The launcher hunk treats exit 0 as success, and the new step 2 says the pack "REPLACES these whole reads ... Do NOT read those whole at boot". So a seat can boot with no rules, or with no grants, on one line of notice inside a 60 KB file. The legacy prompt's own fallback (rules card failed: read the by-tier digest) is bypassed.
- Correctly refused: persona or kam.md missing (rc 2); an unreadable file (rc 1, a Python traceback, nothing written).
- Smallest fix: `wake_pack.py` exits non-zero, writing nothing, when the rules card is absent or its top section is not found, when the grants file is absent, or when the grants file holds pipe lines but zero rows were parsed; the launcher then falls back as it already does for any non-zero exit.

**M3. The fallback is safe but not loud.** When the build fails the Wednesday prompt is byte-identical to today's (good), and the only notice is one `echo` printed before doctor's preflight and before the launcher's `clear`.
- Ran: `scripts/harness.py` (`launcher_harness.txt`). For over budget (rc 3), a crash (rc 1), a missing source (rc 2), `wake_pack.py` missing and `python3` not found: `LEGACY (byte-identical to the original)` and `says anything about the failure IN THE PROMPT False`.
- The doctor snippet (proposal 4) is silent when no pack file exists, so a build that has never succeeded has no backstop at all.
- Effect: the seat boots correctly on the old reads, but neither the seat nor Kam is told; a pack that fails every day would go unseen.
- Smallest fix: in hunk B add a branch for `[ "$AGENT" = "wednesday" ]` with `WAKE_PACK_OK` not 1 that appends three lines to `INITIAL_PROMPT` ("the wake pack was NOT built (rc, first line); the legacy read list is in force; say so in the boot note"). It stays inside the seat test, so the other seats' text is still identical.

**M4. Proposals 2 and 3 write a new contradiction into files that all three seats read, and proposal 2 removes a sentence recorded as Kam's ruling.**
- Proposal 2, replacement A, new item 3: "`INDEX.md` is read by section, on demand; never whole at boot". Proposal 3, new item 4: "`tasks/TASKS.md` and `projects_index/INDEX.md`: on demand, by section". Both are worded for every seat. The launcher prompt for Tuesday and Friday is unchanged and still mandates `TASKS.md`, `INDEX.md` and every file in `entries/` (legacy step 4), as does the Wednesday fallback. The proposals' stated purpose is to end contradictions between these files and the launcher.
- I considered rating this a Blocker ("changes another seat's boot") and did not: the prompt bytes of those seats are unchanged and the new text itself says the prompt is the read list. It is still a changed instruction in a file they read at step 1.
- Owner's rule: replacement A deletes "**... the full lesson load STAYS.**" (2026-08-06, attributed to Kam) and replaces it with a sentence that says the ruling "described a brain of 28 lessons". The later chain is real (the launcher cites his 2026-09-02 words for WED-139, and step 3b of the same file records it), and the builder flagged it. It is still Kam's sentence in Kam's rules file: his word, not a coordinator's edit.
- Replacements B (master drive) and C (voice) are true contradiction fixes: the file's own header carries Kam's 2026-08-25 ruling, and `voice/speak.sh` line 13 records that Kam chose Matilda Premium.
- Smallest fix: word item 3 (and proposal 3's item 4) per seat, as item 2 already is ("a seat on a pack: on demand; a seat not yet on a pack: as its prompt says"); put replacement A's lesson-load sentence to Kam.

**M5. `seed --from-legacy` leaves the legacy file's standing sections behind and does not say so.**
- Ran: the dry seed against the real file (allowed), and `seed --run` on a scratch tree holding a copy (`real_tree_readonly_verbs.txt`, `extra_race_reason_and_seed_run.txt`).
- The newest block maps faithfully: 6 lines, 0 lost, the heading carried into the FLOOR line; 3 bullets mapped by label, 3 placed under FIRST WORK verbatim; OPEN CARDS and GRANTS IN PLAY written as "none stated". The dry run wrote nothing (tasks listing identical before and after; the legacy file's sha unchanged).
- Lost: the file also ends with `## OWED (in order, after the floor)` (line 916) and `## STANDING (unchanged; ...)` (line 923): 8 non-blank lines, 1,694 bytes. None of it is in the seeded block and the seed's report does not mention it. Once a STATE file exists, the pack no longer prints its "read the STANDING and OWED sections in the file" sentence and the new prompt's instruction to read them applies only when there is NO state file. `proposed/README.md` puts the seed BEFORE the launcher change, so on that order those sections are never read again.
- Smallest fix: the seed report names every legacy `## ` heading outside the newest block that contains OWED or STANDING, with its line and size, and either maps the OWED section into the OWED part or tells the coordinator to carry it by hand.

### Minor

**m1. `--check` reads green on a hand-edited pack.** `strip_volatile` drops EVERY line that begins `generated: `, not only the header's. Ran `scripts/wp2.py`: a hand-added line `generated: QA-HAND-EDIT: Kam ruled today that every grant below is renewed...` in the pack body printed `--check rc 0 | OK: wake pack current`; the same for a hand-added line in the sidecar. Every other staleness kind went red as claimed (source newer, earlier build date, content, sidecar missing or changed, pack missing, changed budget or flag, a source changed with its mtime set back). Fix: strip only the one header line (the first match inside the front matter; line 2 of the sidecar).

**m2. Hunk B trusts exit 0 without looking for the file.** Harness case "rc 0 but NO pack file on disk": the pack prompt is still chosen and names a file that is not there. Not reachable from the tool as written (it exits 0 only after the rename); one test closes it: `[ -s "$WAKE_PACK" ]` in the guard.

**m3. Unreadable files give a traceback, not a refusal.** `wake_pack.py` on a mode-000 rules card or grants file: rc 1 with `PermissionError`; `handover.sh write` on a mode-000 state file: rc 1 with a traceback (documented codes are 2, 3, 4). Nothing is written or lost in either case and the launcher falls back. Fix: catch `OSError` at the read.

**m4. Test seams are live in the production path.** `HANDOVER_TREE` pointed at a scratch `TUESDAY` tree from a `WEDNESDAY` tree's copy of the tool, with `WED_AGENT` unset: rc 0, `STATE-tuesday.md` written in the TUESDAY tree. With `WED_AGENT=wednesday`, as the launcher exports it: refused, rc 2. `HANDOVER_TEST_STAMP` lets a caller type the clock; `HANDOVER_TEST_BREAK` exists only to corrupt the archive. The engine called directly with `--seat tuesday` writes `STATE-tuesday.md` with no guard at all. None of these writes a file named for another seat inside this seat's own tree, and every guard case in the brief held (below). Fix: honour the seams only when a second variable such as `HANDOVER_TESTING=1` is set.

**m5. A stack is still possible inside one block.** Accepted, rc 0: a second dated block under a `# ` heading with `### ` parts; an indented `  ## SECOND BLOCK`; a zero-width space after a part name. All are bounded by the 10,000-byte cap, which is the real defence. Refused as they should be: full-width and Cyrillic look-alike headings, a non-breaking space or a tab after `##`, a `##` inside a code fence (refused as a foreign heading; the message says to use `###`).

**m6. Proposal 5 ignores the lane's whole `out/` directory.** Checked with a scratch excludes file (`proposals_extra.txt`): `2_Project_Files/wake/out/STATUS_round1.md` and `out/tests_last_run.txt` become ignored. STATUS.md calls round 1's status "kept" there; ignored, it never reaches git. Fix: ignore `2_Project_Files/wake/out/WAKE-*` only, or move the round-1 status up a level. The other patterns behave as claimed (packs and temp files ignored, both STATE files not ignored).

**m7. The doctor snippet discards stderr** (`bash "$HO" --where 2>/dev/null`), against the lane's own rule, so a seat-guard refusal turns into a silently skipped check.

**m8. The suite misses 9 of my 18 mutants** (`qa_mutants.txt`). Missed: Q01 rename order swapped (state before archive); Q02 the changed-on-disk check removed; Q03 temp-file read-back removed; Q05 trailing newline no longer ensured; Q07 dead marker without a word boundary; Q08 other-seat match without a separator; Q11 `--check` ignores a sidecar whose content differs; Q15 `check` ignores a header naming another seat; Q17 an unreadable state file treated as absent (this one would lose the old block from the archive). Caught: Q04 cap off by one (H05b), Q06 seat guard blinded to `WED_AGENT` (H14c), Q09 budget counts characters (W12b), Q10 rule sentence cut at 70 (W09b), Q12 date found anywhere in the cell (W05, W05c, W17, W17b), Q13 hunk B ignores `WAKE_PACK_OK` (P04, P04b, P08), Q14 hunk A ignores the exit code (P04), Q16 every row dropped (7 checks), Q18 strike-through not unwrapped (4 checks).

### Notes

**N1. Line 24 (CLOSED because made PERMANENT).** The marker leads the cell and covers the whole row. The grant under it is struck through and was TUESDAY's. The permanent rule is recorded: lesson file `2026-11-21_no-fable-unless-flagged-opus-is-the-default.md` exists in `0_Brain/learnings/` (positive control: 7 file names contain `2026-11-2`), and `_rules_index.tsv` lists it `live`, seat `tuesday`. On the Wednesday rules card it appears once, on line 418, inside the "Not on this card: other seats only" list; it is not in the pack (0 hits; control: `fable` 5 hits). The Tuesday card names it once (count only). So for the Wednesday seat the drop is right: this seat never held the rule. Before Tuesday's cut-over, confirm it sits in the part of Tuesday's card that her pack would carry.

**N2. Line 65 (PREMISE ENDED), the one doubtful row.** It is a restriction on this seat, not a permission; its marker says the premise ended, and the cell goes on to say "Re-read with Kam before relying on the 80% figure". Dropping a restriction is the unsafe direction. It was dropped under ruling 4, so the coordinator chose this; say so to Kam or keep rows whose marker is PREMISE ENDED.

**N3. Line 26 is right for Wednesday and would be wrong for Friday.** It is a HOLD, led by TUESDAY, with an end date of 2026-12-10, on a project of the client Wednesday must not touch. A Friday pack would drop it by the same rule while keeping line 63, a FRIDAY-led push permission with no expiry on the same project. Friday is not cut over in this round; fix M1(b) before she is.

**N4. Kept rows that are plainly dead or another seat's: 10 of 22** (lines 34, 45, 52, 58, 60, 70, 71, 73, 74, 111; list of kept lines in `kept_rows_lines.txt`). Cost only, as designed. Line 45 is a live-looking twin of line 41, which is marked EXPIRED.

**N5. A backtick pair already executes at launch, for all three seats.** Not introduced by this lane. Harness with a stub `note_entry.sh` (`launcher_p09.txt`): today's prompt contains the stub's output; with proposal 9 it contains the literal command and the stub does not run; one line changes per seat. Proposal 9 is correct, and it changes Tuesday's and Friday's boot text, so it is outside this round unless both seats claim it. The hunks of proposal 1 add no backtick and no `eval`; their two `$(...)` are the build call and a `printf | tail`.

**N6. The census BEFORE figure includes two conflict copies** in `projects_index/entries/` (25,322 + 98,869 bytes), which the script counts and labels. Without them the reduction is 84.5%, not 86%. Re-measured now (`census_rerun.txt`): 1,278,137 bytes before; 178,792 after as proposed; the pack alone 61,994 bytes, 15,499 estimated tokens of 60,000.

**N7. The new prompt also moves two small reads to on demand**: `TASKS.md` (a pointer in the pack, as the brief asked) and the scoreboard head, which the brief did not list. The coordinator should know the second is in the change.

**N8. Proposal 6 dates its new wrap rule "Kam 2026-11-27".** His words that day were the go for steps 1 to 3; the rule's wording is the coordinator's. Proposal 7 changes what doctor prints on Tuesday's and Friday's machines once `STATE-wednesday.md` travels by git (a warning becomes an OK line): intended, and still a change to their doctor output. Proposal 8 is one safe line; its order caveat is stated.

**N9. Smaller observations.** A crash between the two renames leaves the old block in both files, a duplicate archive entry on the next write and a `STATE-<seat>.md.tmp.<pid>` file; nothing is lost and `check` stays green. A block of exactly 10,000 bytes with no final newline is refused as 10,001. A symlinked state file is replaced by a regular file and the link's target is left untouched (its content is copied into this seat's archive). The x-clock pattern lets `T11:4x`, `1x:30` and `11:4x5` through, as `note_entry.sh`'s does. Tokens are bytes/4: an estimate, with a fourfold margin here. The date filter uses the machine's local date; a drop needs today to be after the end date, so the only early drop is on a machine set to a zone ahead of Kam's. Conflict-copy names in other styles (`(Conflict_On_`, `sync-conflict`, `conflicted copy`, ` 2.md`) are counted as family files; this tree's own style, `(conflict_on_`, and `.pre-` are never read.

### Attacks that failed (passes, with evidence)

- **Other seats' prompt text is byte-identical.** Harness, original against patched scratch copy: tuesday 19,217 bytes, sha `9cf6f7d3b875eb46` both sides; friday 19,204 bytes, sha `bd40e653f86e229b` both sides; the patched region printed nothing, called `python3` zero times and created no pack for either seat. Structure agrees: the diff has 91 added lines and 0 removed; the 13 names the hunks assign are used nowhere in today's launcher.
- **The diff applies and parses.** `patch` on a scratch copy: rc 0, both dry and real; `/bin/bash -n` (GNU bash 3.2.57) rc 0; none of `declare -A`, `mapfile`, `${var,,}`, `&>>`, `|&`, `coproc` in the added lines (control: 6 `if [` lines). No `set -e` in the launcher, so a failed build cannot stop it.
- **Nothing in the build's output can execute.** A stub build printing backticks, `$(touch ...)` and quotes: no `PWNED*` file created; the text arrived literally in the prompt.
- **A reworded slice marker falls back** to the legacy text with a warning.
- **Conservation under odd input.** CRLF, no trailing newline, a NUL byte, non-UTF-8 bytes, a block containing the archive's own heading pattern, a block containing a front-matter fence: each stored byte for byte, each found exactly once in the archive after the next write, `check` rc 0. Sizes: 9,999 and 10,000 accepted, 10,001 refused with nothing written.
- **Hand edits lose nothing.** A block appended by hand: `check` rc 1, and the next write archives what is on disk verbatim with a NOTE. Header removed, header broken, body emptied, text added on top of the archive: every earlier byte still present.
- **Seat guard.** A `TUESDAY` tree holding `STATE-wednesday.md`: the write goes to `STATE-tuesday.md`, the Wednesday file untouched. `WED_AGENT=wednesday` on a TUESDAY tree: rc 2, nothing written. Trees named `SOMETHING`, `wednesday_copy`, `WEDNESDAY 2`, `TuEsday`: rc 2 with or without `WED_AGENT`.
- **The x-clock override.** No variable: rc 3. A 14-character reason: rc 3. A 15-character reason: rc 0, `xclock_override:` in the header and, after the next write, `| x-clock override: quoting a grant` in the archive heading. Fifteen spaces: rc 3.
- **Read-only directory, unreadable state:** nothing replaced, both files unchanged.
- **Budget.** Manifest total equals the file size on disk (62,033); tokens equal bytes/4 rounded up (15,509); a budget of exactly 15,509 passes and 15,508 refuses with rc 3 and no file, no sidecar, no temp file. Over budget with an older pack present leaves the old pack and sidecar untouched (stale, and the launcher does not use them).
- **Conflict copies and `.pre-` files.** Nine planted poison files (rules card, grants, state, ledger, persona, families): the pack and the sidecar identical apart from the generated line; the poison word absent.
- **Proposals 2 to 9:** each quoted OLD text is in today's target exactly once; the three shell targets pass `bash -n` with the replacement applied on scratch copies; each file has a ROLLBACK line, and each is a plain `git revert` or the one `patch -R`.

## GRANTS TABLE

All 54 rows of the real sidecar `out/WAKE-wednesday.dropped.txt`, judged from each row's own text in `0_Brain/tasks/EXPIRING-GRANTS.md`. My rebuild of the pack from today's files drops the same 54 rows. For rows led by another seat only the leading word is shown.

| 10 | dead marker | DEAD since Thu | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 11 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 13 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 14 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 15 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 16 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 17 | other seat | FRIDAY: ... | right | one other seat leads the cell; a permission to that seat on a general project; it gives this seat nothing and binds it to nothing |
| 18 | dead marker | DEAD since Tue | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 19 | dead marker | DEAD since 2026-11-23 | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 21 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 22 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 23 | other seat | FRIDAY: ... | right | one other seat leads the cell; a permission to that seat on a general project; it gives this seat nothing and binds it to nothing |
| 24 | dead marker | CLOSED 2026-11-21 — | right | the struck-through grant under the marker was TUESDAY's; the permanent rule is a live lesson indexed for the tuesday seat (see finding N1), not a rule for this seat |
| 25 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 26 | other seat | TUESDAY: ... | right | one other seat leads the cell; a HOLD on a project of the client this seat is forbidden to touch; right for wednesday, NOT safe for a friday pack (see finding N3) |
| 27 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 28 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 29 | dead marker | ENDED 2026-11-20 at | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 30 | dead marker | ENDED 2026-11-19 evening | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 31 | other seat | FRIDAY: ... | right | one other seat leads the cell; a permission to that seat on a general project; it gives this seat nothing and binds it to nothing |
| 32 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 33 | dead marker | ENDED 2026-11-18 07:36 | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 35 | dead marker | EXPIRED 2026-11-17 07:26 | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 37 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 39 | dead marker | EXPIRED end of | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 41 | dead marker | EXPIRED 2026-11-06 ~10:1x | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 42 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 43 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 48 | dead marker | EXPIRED 2026-11-02 ~06:0x | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 49 | past date | BOTH HALVES RETIRED | right | EXPIRES cell is a true end date (a 14-day acceptance window ending 2026-11-09); the first cell records both halves retired |
| 50 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 53 | dead marker | EXPIRED 2026-10-18 ~19:0x | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 54 | dead marker | EXPIRED 2026-10-18 ~19:0x | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 55 | dead marker | EXPIRED 2026-10-15 ~09:0x | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 56 | other seat | TUESDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 57 | dead marker | EXPIRED 2026-10-11 ~11:5x | right | marker leads the cell and covers the whole row; the row's own text records its end event as happened; the grant under it was another seat's |
| 59 | past date | TODAY: mainly the | right | EXPIRES cell is the row's true end date, weeks past; no later date and no extension in the row |
| 61 | dead marker | EXPIRED 2026-10-09 ~09:0x | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 62 | dead marker | EXPIRED 2026-10-09 ~09:0x | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 63 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 64 | dead marker | EXPIRED 2026-10-07 ~08:4x | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 65 | dead marker | PREMISE ENDED 2026-10-07 | doubtful | the marker says the premise ended, not that the row is dead; the row is a RESTRICTION on this seat and its own text says to re-read it with Kam before relying on it; dropped under ruling 4 (see finding N2) |
| 67 | past date | WEEK INSTRUCTION: as | right | EXPIRES cell is the row's true end date, weeks past; no later date and no extension in the row |
| 68 | dead marker | EXPIRED 2026-10-04 (the | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 69 | dead marker | ENDED 2026-09-27 ~13:15 | right | marker leads the cell and covers the whole row; the row's own text says its date or end event has passed and says not to rely on it (this seat's own old grant) |
| 72 | dead marker | END EVENT REACHED | right | marker leads the cell (after the warning sign); the row says the grant is spent and must be re-asked; it was given at another seat's board view |
| 97 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 98 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 104 | other seat | FRIDAY: ... | right | one other seat leads the cell; this seat is named nowhere in the row as bound (keyword search of the whole row); the scope is that seat's own work |
| 125 | past date | AWAY 2 DAYS | right | EXPIRES cell is the true end date (end of Sunday 2026-09-20); the row already sits under the file's Expired heading |
| 126 | past date | Ornith q4 ONLY; | right | EXPIRES cell is the true end date (end of Sunday 2026-09-20); the row already sits under the file's Expired heading |
| 134 | past date | RESTRICTION (not a | right | EXPIRES cell is the true end date (end of Sunday 2026-09-20); the row already sits under the file's Expired heading |
| 141 | past date | Deploy freely to | right | EXPIRES cell is the true end date (end of Sunday 2026-09-13); ten weeks past |
| 142 | past date | Both boxes end | right | EXPIRES cell is the true end date (end of Sunday 2026-09-13); ten weeks past |

COUNTS: right 53, wrong 0, doubtful 1, total 54

Counts: **right 53, wrong 0, doubtful 1 (line 65)**. Handled as the brief asked: EVENT rows are kept (lines 12, 36, 45); the EXTENDED row is kept although its EXPIRES cell is a past date (line 66); the RENEWED row is kept (line 40, whose outer date is today); a row ending today is kept and would be dropped tomorrow.

## TESTED

Scope covered:
1. The builder's suite and mutant pass, re-run by me in scratch; 18 mutants of my own.
2. The grants filter: all 54 dropped rows and all 22 kept rows read in the real register; 25 hostile rows through `classify_grant`; the date boundary.
3. The handover tool on scratch trees: odd bytes, sizes, headings, hand edits, symlinks, permissions, the seat guard, the x-clock override, a crash between the two renames (done by killing the process with `os._exit` from a wrapper at the second rename, not by a read-only directory), a deterministic interleave, 190 natural races.
4. The wake pack on a scratch tree built from copies of the Wednesday seat's sources: 16 source faults, 19 `--check` cases, the budget boundary, 13 planted files; one read-only build from the real tree into scratch.
5. The launcher proposal: applied to a scratch copy; static checks; a harness that evaluates the prompt region for each seat from the original and the patched copy, with `python3`, `hostname` and `note_entry.sh` stubbed and every other variable set to a sentinel. The launcher was never run.
6. Proposals 2 to 9: old-text counts, replacements applied to scratch copies, `bash -n`, the gitignore patterns with a scratch excludes file, the facts they cite (speak.sh, rules_card.py flags, pointer targets).
7. The dry seed against the real legacy file, and `seed --run` on a scratch copy.
8. From the builder's "did NOT test" list: the crash between the renames, the changed-on-disk refusal (it fires: 10 of 40; it does not close the race), non-UTF-8 input.

NOT tested, and why:
- A real launch, and the statusline after a pack boot: the launcher starts a seat; forbidden.
- `doctor.sh` with proposals 4 and 7 in it, and `nas_staleness.sh` with proposal 8: I may not run either script; I checked text, syntax and the builder's stubbed D group only.
- The pack, census and seed on Tuesday's and Friday's real files: another seat's content. The filter was judged for the Wednesday seat only; N3 is from the register's rows, not from a Friday build.
- Real token counts: bytes/4 only; no tokenizer was used (no network).
- Durability across a power cut: the tool fsyncs its temp files but not the directory; not simulated.
- Two pack builds at once, and a pack build during a handover write.
- How a seat actually reads the changed sentences of proposals 2, 3 and 6: text was compared, no session was run.
- The lane's `_quarantine_2026-11-27/` cache file: not opened.

## HOW

Commands (all paths absolute; scratch root `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-wake/`):
- `WAKE_TEST_SCRATCH=<scratch>/suite bash 2_Project_Files/wake/tests/run.sh` and `... --mutants`, with `PYTHONDONTWRITEBYTECODE=1`.
- `python3 scripts/qa_mutants.py <scratch>/qmut` (copies the tools, edits the copy, runs the builder's `run_tests.py` with `WAKE_UNDER_TEST`).
- `python3 scripts/ho_tests.py`, `scripts/race.py <scratch>/race 150`, `scripts/extra.py` (handover, on trees named WEDNESDAY, TUESDAY and others under scratch).
- `python3 scripts/wp_tests.py`, `scripts/wp2.py` (wake pack, `--root` on a scratch tree).
- `patch <scratch copy> 01_launcher_boot_prompt.diff`; `/bin/bash -n`; `python3 scripts/harness.py`; `scripts/h09.py`.
- `python3 scripts/props.py`; `git -c core.excludesFile=<scratch file> check-ignore` (a read).
- Against the real tree, only: `handover.sh --where`, `check`, `show`, `seed --from-legacy` (dry); `wake_pack.py --seat wednesday --out <scratch>`; `wake_census.sh --seat wednesday --pack <scratch pack>`; reads with `sed`, `awk`, `/usr/bin/grep`.

Controls: every absence above is a `/usr/bin/grep -i -c` count beside a positive control from the same file (given in the finding). The lane's 37 files were hashed before and after (identical). `0_Brain/tasks/` was listed before and after (identical); no `STATE-` file and no `0_Brain/wake/` directory exist. Mutant Q16 (drop every row) is a control that the suite can go red on the grants part: 7 checks did.

Things of mine that errored or were wrong, and what I did:
- My first launcher harness gave each variant its own stub project path, so the two prompts differed by 54 bytes of path and read as NOT identical. Fixed (one stub path per seat) and re-run; the figures above are from the second run.
- My first "generated:" attack also added a blank line and was correctly caught; the precise attack (one line, nothing else) is the one reported in m1.
- A hook refused one of my commands because a grep pattern contained the letters of a delete command; I read the file with `cat` instead.
- I copied a rebuilt sidecar into this directory, then moved it out to scratch (`mv -n`), because it carries 80 characters of other seats' rows; the builder's identical file is at `2_Project_Files/wake/out/WAKE-wednesday.dropped.txt`.
- While judging rows I printed register rows led by other seats to my terminal, as the brief allows; none of that text is in this report beyond a leading word.
- `git status` at the end shows modified dashboard data files; they are not mine (I wrote only under this directory and scratch).

Raw outputs beside this file: `suite_run.txt`, `suite_mutants.txt`, `qa_mutants.txt`, `handover_attacks.txt`, `handover_race_crash.txt`, `extra_race_reason_and_seed_run.txt`, `wakepack_attacks.txt`, `filter_hostile_and_check_attack.txt`, `launcher_patch.txt`, `launcher_harness.txt`, `launcher_p09.txt`, `prompt_wednesday_new_harness.txt`, `proposals_check.txt`, `proposals_extra.txt`, `real_tree_readonly_verbs.txt`, `real_pack_build.txt`, `census_rerun.txt`, `kept_rows_lines.txt`, `lane_hashes_before.txt`, `lane_hashes_after.txt`, `tasks_ls_before.txt`, `tasks_ls_after.txt`, and my scripts in `scripts/`.
