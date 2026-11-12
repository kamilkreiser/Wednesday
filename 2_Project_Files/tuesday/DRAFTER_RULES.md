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
   **Every name scan a kit asks a seat to run is UNDERSCORE-AWARE** (2026-11-10, B1396 verifier: a test method
   name joined a ban-list first name with underscores, and the `\b`-bounded scans of the builder AND the
   verifier's first pass both read 0, because `_` is a word character). Write the pattern as
   `(?<![A-Za-z])<name>(?![a-z])` (or split on `_` first), and its control plants `_by_<name>_` and must fire.
8. **A gate runs every CI job whose TESTS READ the changed files, not only the jobs whose PATHS were touched**
   (2026-11-10, HPSM #300: gate B1451 skipped `infra` because no infra path changed, graded two literal
   U+202E in a web test file Minor "unless a CI step refuses it", and hosted CI's `infra` job then refused it via
   `infra/tests/test_hidden_characters.py`, which scans EVERY tracked file). On HPSM-POC the infra job's repo-wide
   scans (hidden characters, and any other test that walks `git ls-files`) run in every gate, whatever paths changed.

## Things every kit must get right
- **Never make "the alert reads fixed or absent on `refs/pull/N/head`" a landing condition on NexusAI: that read cannot fail** (measured 2026-11-06: 40 of 40 closed PRs read js results 0 on their head analysis; main reads 122). The check that can fail is main's analysis at the merge commit, after landing: the ticket moves on that, and a fix that leaves the alert open is a new round. Added 2026-11-06 by s249.
- **Never write `az webapp show` into a kit that holds a hosted site read-only** (Azure CLI 2.90.0: it calls `list_publishing_profile_xml_with_secrets`, so each call fetches the site's publish profile and leaves a `publishxml/action` row; B1319 measured 8). Name a plain ARM GET (`az rest --method get` on the site's resource id) and have the seat test it against the activity log first. Added 2026-11-06 by s247.
- **A `file:line` pointer and a clock are printed by a program, never remembered** (ledger 2026-11-02: B1087 and B1088 both carried a window for the drafter's own reads ending later than the clock; B1088 carried nine line pointers marked MEASURED, off by one or short, two of them inside Jira text). Generate each `file:line` with `grep -n` or `awk NR==n` over the raw file at the pinned sha just before writing it; a clock comes from `date` in the same action or the kit says "at drafting".
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
- **Git identity is never overridden.** Every kit that lets a seat commit, cherry-pick or merge says: the repo's own configured identity only; never `git -c user.name/user.email`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*`; and its READY section prints `git log --format='%h %ae | %ce'` for every new commit, each equal to the repo's configured email. (Added 2026-11-11 by s265: R208 overrode the identity on a cherry-pick in the MPS root records repo and commit 9e847dc4 carries Kam's personal address as committer in a Datasec repo; contained only because that repo has no remote.)
- **Every long kit carries a context band and a handover form.** Any kit whose work may not fit one window (a guide, a multi-row chain, a walk with many captures) says: at about 70% context start no new part; at about 75% stop at a safe boundary (files whole, processes stopped by pid, ports free) and write `<date>_B<n>_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps) with last line `HANDOVER B<n>: next <part> <step> | done <parts>`. (Added 2026-11-11 by s265: U4 reached 51% with only its inventory done and no band; fixed by ADDENDUM-1.)
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
- **The STAMP and READ-WHOLE slot values in `slots.json` attest what TUESDAY read; never write a read Tuesday has not done.**
  Write only the facts YOU measured, marked as yours ("the drafter read ..."), plus `@NOW@` (stamp_brief fills no `@SEAT@`: never write it; corrected 2026-11-06 by s250 after two kits carried it). Never "Tuesday re-checked
  X", "Tuesday printed at source Y" or "the drafter's report lines 1-N" as Tuesday's read: Tuesday writes those after doing them.
  No `<clock>`, `<session>` or other angle-bracket placeholder in a value. (Added 2026-11-04 by s240: B1253's and B1255's
  drafters both pre-wrote attestations of reads Tuesday had not done; caught at the stamp and rewritten.)

## MEASURED LITERALS (added 2026-11-12 by Tuesday s274; ledger w=3 REGRESSION, the stamped-text-not-measured family)
Three seats halted in one evening on literals a kit told them to match that nobody had run: a name said to appear "once" (it was on 2 lines), a step that needed files a later step makes, and a tool line quoted in a wording the tool never prints. Reading a kit checks its sense; only an instrument checks its literals.
1. Before you report STARTABLE, run `python3 -I -B /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/stamp_check.py <your kit> --init` (it writes `<kit>.measured`, one `<id> | TODO` line per literal the kit tells a seat to match: a backticked or quoted string beside a count or output word).
2. Replace EVERY `TODO` with what you ran and what it printed: `<id> | grep -c -F '<literal>' <file at ref> -> 1` or `<id> | <tool> --check (run at <ref>) -> runtime rows 205; committed rows 205`. A literal you cannot measure is reworded in the kit to say so (UNMEASURED) or removed; never left as an expectation.
3. Expected TOOL OUTPUT lines are copied from a real run or a saved log of one, never written from the tool's docs or another kit.
4. Every chain step lists its inputs, and each input is produced by an EARLIER step or exists at BASE (print that table in the report).
5. Your last check: `stamp_check.py <kit>` exits 0. Tuesday re-runs it and spot-measures at least five sidecar lines before the stamp.
