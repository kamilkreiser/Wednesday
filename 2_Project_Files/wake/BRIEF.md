# BRIEF: WED build seat "wake" (WED-170 step 1). Build the WAKE PACK and the ONE-BLOCK HANDOVER for the Wednesday seat. New files only, inside your lane; nothing shared is edited; the round ends at READY FOR QA.

Commissioned by Wednesday (coordinator), 2026-11-27. Model: claude-fable-5-2 (Kam, 2026-11-27: Fable for this project's agents).

## AUTHORITY (verbatim)
- Kam, live board 2026-11-27 11:43:30: "thank you.  I like your recommendations.  Please put this into action for you.  Each external drive will now also hold the dB.  once you finish and test, prepare instructions and send to Tuesday and Friday"
- Kam, live board 2026-11-27 11:43:52: "Decision wed-fleet-structure-v2-go-steps-1-3-1127: a — Go, steps 1 to 3 in that order"
- Wednesday's reading: built and tested on the WEDNESDAY seat first. Tuesday's and Friday's boots do not change in this round.

## READ FIRST (whole, in this order)
1. This brief.
2. The design: `/Volumes/DevMASTER/WEDNESDAY/1_Project_Definition/Architecture/2026-11-27_fleet-structure-v2-design.md` (section 1 and "Input from the other seats").
3. The census, sections A and B: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_fleet-structure-research/current_structure_census.md`.
4. The code you build beside (read, never edit): `/Volumes/DevMASTER/WEDNESDAY/Launch_Wednesday.command` (the boot prompt, about lines 590 to 875), `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/rules_card.py`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/seat_resolve.sh`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/note_entry.sh` (as the model of a tool that refuses in the path).
Do NOT read the lessons, the ledgers, the daily notes or the pickup files for content; you need their STRUCTURE only. Never read `4_Credentials/` or `3_Access_Keys/`. Files whose path contains `tuesday`, `friday`, `laptop_datasec` or `daily_tuesday` belong to other seats: sizes and structure only, never content into your outputs.

## THE PROBLEM, MEASURED
The Wednesday seat's boot prompt mandates about 917 KB of whole-file reads (about 229K tokens by bytes divided by 4). The handover file `0_Brain/tasks/NEXT-PICKUP.md` is 287 KB: 106 blocks stacked in 14 days under a header that says "never stack". `EXPIRING-GRANTS.md` is 87 KB, mostly rows that are dead or another seat's. The rule that keeps these small exists only as a sentence; nothing enforces it.

## WHAT YOU BUILD (all under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake/`)

### 1. `handover.sh` — the one-block handover
- Seat-aware by `seat_resolve.sh` (never a hardcoded seat name). State file `0_Brain/tasks/STATE-<seat>.md`; archive `0_Brain/tasks/STATE-<seat>-archive.md`.
- `handover.sh write --stdin` replaces the state file's single block with the new one and, IN THE SAME ACTION, appends the previous block verbatim to the top of the archive under a generated timestamp heading. Conservation is asserted before anything is written (bytes of old block in == bytes appended); on any mismatch it writes nothing and says why. Writes go by temp file then atomic rename.
- It REFUSES a block over a size cap (default 10,000 bytes; a variable) with the size, the cap and what to cut. It refuses an empty block. It refuses a typed placeholder clock such as `11:4x`.
- The block has fixed headed parts the tool checks are present: FLOOR (who is running), FIRST WORK, OWED, OPEN CARDS, GRANTS IN PLAY. Free text under each.
- `handover.sh show` prints the current block; `handover.sh --where` prints the paths and writes nothing; `--dry` on write prints what would happen.
- It does NOT touch `NEXT-PICKUP.md`. The legacy file stays as it is until the coordinator cuts over.

### 2. `wake_pack.py` — the fixed-budget wake pack
- `wake_pack.py --seat <seat> [--budget-tokens 60000] [--out <path>]` writes ONE generated file (default `0_Brain/wake/WAKE-<seat>.md`; in this round write ONLY to a path under your lane, e.g. `out/WAKE-wednesday.md`, never into `0_Brain/`).
- Parts, in order, each with its source path, bytes and estimated tokens in a manifest table at the top:
  a. identity: `0_Brain/identity/persona.md`, `voice-protocol.md`, `0_Brain/people/kam.md`, verbatim.
  b. rules: the "Most reinforced" section of the seat's rules card, verbatim, then ONLY the family headings with their line counts, and one line saying how to fetch a family or a trigger (`rules_card.py --at <trigger>`; check that flag exists and name the real command).
  c. state: the seat's STATE block (if no state file exists yet, say so in the pack and point at the legacy pickup's first block only).
  d. live grants: rows of `0_Brain/tasks/EXPIRING-GRANTS.md` that are this seat's and not dead. A row is dropped ONLY when the tool can prove it: its text marks it DEAD, or it names another seat in its first cell, or it carries a parseable end date that is in the past. A row the tool cannot classify is KEPT and counted as "unclassified" in the manifest. Fail toward inclusion: a live grant dropped is worse than a dead one kept.
  e. own ledger: each row of the seat's own ledger reduced to its date, its bold headline and its "Rule:" sentence, with the file path for the rest.
  f. pointers (paths only, no content): tasks file, the design, the project index, how to read Kam's messages (`tools/kam_msgs.sh`, `tools/kam_rulings_today.sh`).
- Over budget: exit non-zero, write nothing, print the parts largest first. `--check` exits non-zero if any source is newer than the pack or the pack is missing.
- Globs exclude `(conflict_on_` and `.pre-` files. Python standard library only. macOS bash 3.2 for shell.

### 3. `wake_census.sh` — the measurement
Prints, for a seat: the bytes and estimated tokens the CURRENT boot prompt mandates (the census table A3/A4 method, re-measured from the files today) beside the wake pack's. This is the before and after the coordinator shows Kam.

### 4. `proposed/` — changes to shared files, as PROPOSALS ONLY (you apply none of them)
One file per target, each a unified diff or exact replacement text plus a one-paragraph reason: the boot prompt in `Launch_Wednesday.command` for the WEDNESDAY seat only (other seats' text byte-identical: say how your diff guarantees it); the session-start lines in `/Volumes/DevMASTER/WEDNESDAY/CLAUDE.md` and `0_Brain/CLAUDE.md` that contradict the launcher (census A7 lists five); a `doctor.sh` check that the pack is fresh and the handover is one block; a `.gitignore` line for generated packs; the wrap step that writes the handover through the tool. Include a rollback line for each.

### 5. `tests/` and `STATUS.md`
- A test runner (`tests/run.sh`) using scratch copies and fixtures only: never the real state or grants files as write targets. For every refusal a must-succeed case beside it; for every "dropped" class in the grants filter a fixture row that is dropped AND one that must be kept; a planted over-budget part; a planted conflict-copy file that must not be read; a stacked second write that must leave exactly one block and a longer archive. Show each test can fail (break the thing, see red, restore).
- Then ONE real read-only run: build the pack from the real files into your lane's `out/` and run the census. Record the numbers.

## HOLDS (the whole session)
- You write ONLY under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake/` and your session scratchpad. No edit to any existing file anywhere. No `git add`, commit, push, stash, checkout or branch; no mail; no board or chat post; no `note_entry`; no `decision_queue`; no cockpit command; no Linear call; no network call.
- Never `rm`: move with `mv -n` into `_quarantine_<date>/` inside your lane. Never `cd` in a shell command (a hook refuses it): absolute paths. No unquoted word starting with `=`. `/usr/bin/grep -i`, with a positive control before you write that something is absent. Never type a clock: use `date`.
- Other WED build seats may be running in sibling lanes (`2_Project_Files/brain-db/`, later `2_Project_Files/skills-registry/`). Their directories are not yours; do not read or write them.
- If the brief looks wrong or contradicts itself, say so in STATUS.md under QUESTIONS and take the stricter reading. A design choice inside these requirements is yours: make it, write one line saying why.

## STATUS.md (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake/STATUS.md`), updated at every stop
First line one of: `WORKING`, `QUESTION` (you are blocked; one question), `READY FOR QA`. Then: what exists (files with sizes), the test run's output tail and pass/fail counts, the real-run numbers (before and after, per part), every deviation from this brief with its reason, what you did NOT test, and QUESTIONS. Do not wait for an answer to a design note: write `DESIGN.md` (one page) first, then build. Stop at READY FOR QA; a separate checker reads your work next.

PROVENANCE:
- boot reads 917 KB / about 229K tokens; pickup 287,068 B with 106 stacked blocks; grants 87,458 B | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_fleet-structure-research/current_structure_census.md sections A3, A4, B5 | read 2026-11-27
- Kam's two messages | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_msgs.sh output | read 2026-11-27
- Tuesday's constraints (seat name resolved from the tree; guards not bypassed) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_in_003900.txt | read 2026-11-27
