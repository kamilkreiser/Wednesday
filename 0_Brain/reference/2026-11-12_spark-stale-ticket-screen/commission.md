# Commission: Spark NIGHTLY STALE-TICKET SCREEN (routine (b) of Kam's 2026-11-12 standing instruction). Wednesday, 11:3x AEDT.

## Authority and why
- Read whole: `0_Brain/learnings/2026-11-12_spark-for-harness-and-token-heavy-simple-tasks.md` (Kam 11:34 + 11:36 "please implement this plan as a standard routine going forward").
- Board seats spend hours checking whether an open ticket's cited code still exists, is already fixed, or duplicates another. That is simple, bulky and checkable: the Spark proposes; a Claude board seat confirms before ANY board change. The screen itself writes NOTHING to the board.

## Read before building
- `2_Project_Files/local-model/spark/` (runner, tunnel, ONE request at a time: use the existing queue/lock; never call the endpoint while another round is live).
- `2_Project_Files/fleet/board_count.sh` (paginated counts; never a capped total) and the Linear read pattern the fleet uses (key from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, sourced in-process, never echoed; GraphQL, `comments(first:50)` sorted client-side).
- `0_Brain/learnings/2026-09-07_a-classification-list-is-a-representation-not-an-instruction.md` and `2026-09-14_true-duplicates-are-closed-and-archived-by-us-no-external-review.md` (what a confirmed duplicate means).
- The sibling pilot `0_Brain/reference/2026-11-12_spark-test-digest-harness/commission.md` (same verify-every-claim shape; do not touch its files).

## Build (in `2_Project_Files/local-model/stale_screen/`, tracked)
1. `screen.py --limit N --out <dated dir>`: for each open KS ticket (Backlog/Todo/In Progress; skip tickets assigned to Peter or Stuart; skip the no-write partition if one is named in the latest S-seat record), extract every code citation deterministically (paths, `file:line`, symbols in backticks); resolve each at live develop (read via `git -C <shared checkout> ls-remote` for the sha and `git show/grep` in a `--shared` clone in the job's own scratch; never fetch into the shared checkout) -> FACTS (path exists? symbol present? line text now?). Then ask the Spark, per ticket, with the ticket text + FACTS, for ONE proposal: STILL-VALID / LIKELY-FIXED / CITATION-MOVED / POSSIBLE-DUPLICATE-OF <key> / CANNOT-TELL, with a one-line reason that cites a FACT. A CHECKER refuses any proposal whose reason cites a fact not in FACTS, or a duplicate key that is not an open ticket.
2. Output per run: `proposals.tsv` (key, proposal, reason, facts-hash) + `report.md` (counts per class, BLUF first). NO board write, NO comment, NO state change.
3. A nightly launchd job installed the scheduler's way (look at how `install_all_jobs.sh` and the existing night jobs are templated; read headers, never run a write tool to learn its usage), window 01:00-05:00, refuses while a Spark round is live or the tunnel is down (says so in its log), bounded by N tickets per night (start N=60). doctor.sh check + PORTABILITY item for the job (machine-local dependency rule).
4. Arms (`tests/arms.sh`) before arming the job: a ticket whose cited file was deleted (must read LIKELY-FIXED or CITATION-MOVED, never STILL-VALID), a ticket with no citations (CANNOT-TELL), a planted Spark reason citing an invented fact (REFUSED), Spark unreachable (job exits cleanly, logged), the refuse-while-round-live gate.
5. One real dry run on 20 tickets now (Spark one request at a time; wait if the digest pilot holds it) and report the class counts plus 5 proposals you checked at source by hand.

## Limits
Secuura only. Read-only on project checkouts and on Linear. Never delete files. Never print credential values. No mail or board writes. Gitignore run-output dirs at creation. Do not edit a running script.

## Output
`report.md` in THIS folder: built paths, arms table, the 20-ticket dry run, the job's install state (armed or not, and why), NOT TESTED. Final message: a 10-line summary.
