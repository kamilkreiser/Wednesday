# Spark nightly stale-ticket screen — report (routine (b), 2026-11-12)

Filed by Wednesday from the building agent's returned text (its Write was refused by the harness), ~12:0x AEDT. Wednesday did not re-run the arms or re-check the five hand reads; the numbers are the agent's.

## BLUF
- Built `2_Project_Files/local-model/stale_screen/` (screen.py, nightly.sh, tests/arms.sh, .gitignore), `scheduler/jobs/stalescreen.plist.template`, a Wednesday-only skip in `scheduler/install_all_jobs.sh`, a doctor.sh block, PORTABILITY item 28. Backups `.pre-1112-stalescreen` beside both edited scripts.
- **Arms 22/22 PASS** (incl. a real-Spark arm: a deleted-file ticket reads LIKELY-FIXED citing the deleting commit, never STILL-VALID). No Linear write path exists (gql() asserts query-only; 0 `mutation`).
- **Dry run, 20 stalest of 635 eligible (761 open KS read), develop 088fa84da10c, ~4 s/ticket:** STILL-VALID 8, CITATION-MOVED 2, LIKELY-FIXED 1, CANNOT-TELL 4, duplicates 0, REFUSED 5 (invented numbers, slash-joined paths, an unparseable reply).
- **Five proposals checked at source by the agent: 3 right (KS-638, KS-807, KS-748), 2 wrong in ways the checker cannot see** (KS-824 LIKELY-FIXED: a true fact, wrong inference: the constraint name is Postgres's auto-name; KS-699 STILL-VALID: the Spark misread the ticket). **Every proposal is a LEAD for a Claude seat, never a finding.** LIKELY-FIXED resting on SYMBOL_ABSENT alone is the weakest class (1/1 wrong); CITATION-MOVED is the cheapest to confirm.
- **Job ARMED:** `com.wednesday.stalescreen`, 01:15 nightly, window 01:00-05:00, 60 tickets, single-instance lock, 05:00 deadline, always exit 0. launchd kickstart at 11:59 logged `REFUSED - outside the 01:00-05:00 window (hour 11)` rc 0 (~/Library/Logs/wednesday_stalescreen.out). Stop with `launchctl bootout gui/$(id -u)/com.wednesday.stalescreen` (do not re-run the installer). **The first real fire is tonight and is NOT TESTED.**

## Precision fixes the dry run forced (all re-run)
1. "File was edited" is not evidence of a fix. 2. "Refs KS-n" in a commit is not evidence of a fix (own work vs reference now split). 3. A symbol absent from the repo, with no cited file, is NOT_IN_REPO and cannot support LIKELY-FIXED. 4. Extractor: `process.env` dropped; dotted `table.column` falls back to the column.

## Finding for the digest harness (routine (a))
`digest.py` uses the Spark WITHOUT taking `spark/state/round.lock` (vLLM showed 1 running request with no lock). The screen now also reads vLLM's running/waiting counters before each request. **OWED: digest.py takes round.lock the same way** (one-request discipline; same protocol as round.sh).

## NOT TESTED
The first 01:15 fire (full 60, deadline, --update-state rotation); a live POSSIBLE-DUPLICATE (0/20; stub + unit only); the fetch path without the deploy key; >5000-char tickets (head+tail truncated) and unrecognised citation styles; a second lock-free client mid-request; Linear rate limits at 60; repeatability of a class across identical runs (temperature 0, not repeated).

## How a board seat uses it
Read `runs/<date>/proposals.tsv` (its `basis=` column lists the statuses of the cited facts): confirm CITATION-MOVED cheaply; READ STILL-VALID and LIKELY-FIXED at source before any comment or close; a REFUSED row carries the Spark's original class in its reason. Nothing reaches the board without a Claude seat's source read.
