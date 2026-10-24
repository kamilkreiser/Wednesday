# Tuesday kit-drafter rules (read whole before drafting)

Tracked file, written 2026-10-25 by Tuesday s168 because the 2026-10-25 01:25 rules file lived in a
session scratchpad and died with its seat (learnings/2026-09-20_prepared-in-a-scratchpad-is-lost).
Every Agent-tool drafter Tuesday commissions for a Datasec kit reads this file first. Each rule
names the ledger row (`0_Brain/learnings/_ledger_laptop_datasec.md`) that earned it.

## What you produce
- ONE brief file `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/<date>_B<NNN>_SEAT-<seat>_<topic>.md`
  and ONE report `<date>_B<NNN>_DRAFTER-REPORT.md` beside it. Write ONLY those two files, with the
  Write/Edit tools. Never use Artifact, Docs, mail, chat, or any publish/upload tool (10-18 Artifact row).
- Copy the SHAPE of the template kit you are given (STATUS-file channel, fact marks MEASURED / RELAYED /
  UNMEASURED, REFUSE AT ONCE, THE WORK by steps, STANDING LINES, STATUS-NOW, last-line markers,
  PARTITION from both sides, HOLDS, the `## Stamp` slots, `READ-WHOLE-BY-TUESDAY: ____` as the last line).
  Leave every Stamp slot as four underscores; Tuesday stamps. Never write a typed clock where a slot is.
- The report starts `STARTABLE: YES|NO`, then BLUF, facts re-measured with instruments, D-decisions,
  Q-questions for Tuesday (each with a default), UNMEASURED, and an outside-the-fences disclosure.

## Fences (breaking one is worse than a weaker kit)
1. READ-ONLY outside your two files. Never `decision_queue.sh list` in any form; a card is read only by
   `decision_queue.sh show <exact Datasec id>` into a scratch file, read through an inclusion filter on the id
   (10-21 / 10-23 card-store rows). Never read `fleet/briefs_staged/`, `projects_index/scoreboard.md`,
   `0_Brain/learnings/_ledger.md`, or any WEDNESDAY / FRIDAY tree or non-Datasec project.
2. Jira: every JQL is `project = <KEY> AND ( ... )` WITH the parentheses (10-25 0120 row). Use the project's own
   read helpers (they read the project `.env` in-process; never print a token).
3. Git in a project repo: READ verbs only, `--no-optional-locks`: ls-remote, log, show, diff, cat-file, ls-tree,
   rev-parse, rev-list, merge-base, grep. FORBIDDEN there: fetch, pull, `merge-tree --write-tree`, worktree,
   checkout, commit, any ref write (10-20 merge-tree row). A project's local checkout may be stale: read origin
   (ls-remote, `gh api -X GET`).
4. `gh` is `-X GET` only, under the project's own `GH_CONFIG_DIR`
   (`/Volumes/Laptop-DEV/!CODING/Datasec/<Project>/4_Credentials/.gh-config`). No HTTP to any hosted, demo or
   production host, not even GET (10-16 production row). No az, ssh, docker.
5. Never type `cd` (a hook refuses it). Absolute single-quoted paths (`!CODING` contains `!`). `/usr/bin/grep`.
   Read a tool's usage from its header (`sed -n 1,40p`), never by invoking it (10-18, 10-24 probe rows).
6. Every number carries its instrument and a control that can fail; name the frame of every census; a zero is a
   suspect until a control fires (2026-09-08 false-absence lesson).
7. No person's name (client staff, reviewers) and no decision-card id in the KIT text the seat will copy into
   commits or comments; cite a ruling as "the product owner's <date> ruling" (10-16 / 10-20 naming rows).
   The report may name card ids.

## Things every kit must get right
- **Ports:** the block Tuesday assigned, checked by `lsof -nP -iTCP:<block> -sTCP:LISTEN` AND a word-boundary scan of
  the non-`.pre-` SEAT kits of today and yesterday, plus the live pane list (10-25 port row). Report hits.
- **Round counts** name what they count: "NO GO <n> of 2 on class <X>", read from earlier gates' verdict lines (10-25 row).
- **Locks** are named by PATH and purpose; a shared ref lock wraps ref writes only; heavy jobs take a seat-local lock (10-22 lock row).
- **Closed lists** (allowed reds, classes, rows, paths) are stated as a PROPERTY first, then "at least these", and end with
  "any other shape: prove it meets the property or STOP" (10-21 / 10-22 instances rows).
- **CI predicates:** before specifying any check, read the CI step that will judge it and write its pass predicate into the
  kit (10-23 SQL Server rows). HPSM-POC Api test rows ask "does it run on SQL Server as CI does?".
- **Landing:** the seat pushes its own branch only; Tuesday opens and lands PRs through CodeQL (Datasec org ruleset; never
  bypass, never dismiss an alert). Read the project's landing rule (squash vs merge commit) and quote it with its source.
- **Records seats** land their own records branch; a ref write in a project repo is never Tuesday's (10-23 self-land row).
- **Model row** from `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md` (Sonnet first on this seat
  unless the table says Opus), with the line number; the model id from
  `/Volumes/Laptop-DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json`.
- **Standing lines** every Datasec kit carries: PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned);
  no message to any human; Jira writes only where the kit's scope says so; never delete (quarantine); HPSM-POC kits also
  carry "This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools,
  SIEM); next-phase items are stored and architected only".
- **The launch line** follows the template: `WED_USAGE_STOP=100 bash .../fleet/cockpit/cockpit.sh add <Datasec/Name> "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '<project dir>' '<kit path>'"`
  with `BRIEF_SEAT_LEVEL=sonnet` or `BRIEF_SEAT_LEVEL=opus` ALWAYS written inside the quotes, matching the model row.
  **`brief_seat.sh` defaults to Opus** (line 24): a launch line without the level runs a Sonnet-routed seat on Opus.
  (Corrected 2026-10-25 10:3x: this line first said "add the level only when Opus", and B651/B652 launched on Opus.)
