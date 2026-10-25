STARTABLE: YES (after Tuesday's stamp; launch_when_cool, load1 was 7.3-8.9 at 14:43-14:44)

# B674 drafter report (kit: `2026-10-25_B674_SEAT-G118_composer-92-gate-tier2.md`, 90 lines)

Drafted 14:43-14:50 AEDT by `date`, read-only. Shape cloned from the B659 gate kit; content from the B671 builder kit and STATUS, the B626 findings, and the added file read at the head by `gh api contents`.

## BLUF
Tier 2 (row G2, `model-routing.md:109`; G-cap `:111`), Sonnet (`claude-sonnet-5-5`, `BRIEF_SEAT_LEVEL=sonnet` in the launch line), round 1 of 2 on its own count, B674 / SEAT-G118 / pane `Datasec/Security-Composer-G118`, ports 9700-9709. Seven checks: C1 delta and provenance, C2 the six mutants rebuilt by the gate (18 x 9 matrix, plus the same six against the neighbour and contract files), C3 the gate's own extra mutants with survivors, C4 names and stability (3x, alone, shuffle, TZ, ordered), C5 CI route and suites, C6 CodeQL, merge in its own clone, overlap, C7 PRIOR WORK, NEW WORDS, disclosures. Slot lines: 7 plus the last line (grep count 8 before stamping; the `@[A-Z_]+@` count is 0).

## Facts re-measured with instruments (14:43-14:50)
- `ls-remote`: main `667830ed`; branch = `refs/pull/92/head` = `dc32e143dec9b0e446a90db876cd2927efb3f937`; `refs/pull/92/merge` = `f75c2ff6`, parents main and head, tree `0d923356...` (= the builder's head tree; main unmoved). Control: `refs/heads/b6*` lists the other branches.
- `gh api -X GET pulls/92`: open, not draft, 1 commit, 1 file +195 -0, created 03:42Z, `mergeable_state` blocked. `pulls/92/files`: the one path. Open PRs #92, #91, #86, #85.
- Check-runs on the head: 2 total, both `Analyze (...)` `in_progress`; `code-scanning/analyses?ref=refs/pull/92/head`: 0 rows (no positive control run by me; the kit makes the gate run it with main as the row-count control). Ruleset `Security scan rule` active.
- The added file (195 lines, raw): 3 `describe(`, 9 `it(` = 18 run-time rows, 11 `expect(`, one warm-up line, 0 non-ASCII, 0 `skip|only|todo|retry|console.`, `B626` on 12 lines. Control `zzz-no-such-string-7f3a` = 0. The four `app.ts` anchor lines at main each = 1.
- Ports: `lsof -nP -iTCP:9700-9709 -sTCP:LISTEN` rc 1. Word scan of the 2026-10-24/25 non-`.pre-` kits: the only real port claim is B620 (G95, finished, pane gone) and its mention in B622; all other 970x hits are non-port numbers. B674 and G118 unused in kits, `Briefs/` and `.tools` (counts 0). Pane list: tuesday, MPS-M24, Security-Composer-J14, MPS-M23, MPS-G116, NexusAI-G115, fleet-monitor.
- Builder STATUS (read whole) still holds two unfilled template tokens (CodeQL poll line and final-read line): measured by reading; the kit makes the gate count them (Minor).

## D-decisions
- D1: gate plumbing may be copied from the finished B626 gate's `.tools/b626/scripts/` (common, heavy, build, dbone, dbtest, unit, names, titles); every mutant driver, battery and oracle there is forbidden, as are the builder's `.tools/b671` and `.tools/b627`. Reason: the task said the gate must rebuild the mutants itself and never run the builder's or B626's scripts. Needs Q-3 at the stamp (default: yes, plumbing only). I did not read those plumbing files beyond the first 30 lines of `heavy.sh` (seen: it already carries the cross-seat gate, heartbeat, lock released by move); fit is UNMEASURED.
- D2: the six mutant edits are written into the kit as prose from the B671 kit's table (G01, G02, G05-G07, N18), with G05/G06/G07 specified by which regex group. I did not read `mutants_c4.py`.
- D3: "survivor" is defined as surviving the new file, the neighbour file and the contract file, then the whole API db suite, then an oracle; only then a Major. Property first, "at least" list, "any other shape" clause (house rule).
- D4: class property for round 1 of 2 written into ROUND COUNT; B626's round 2 is cited as RELAYED history, not this PR's count (the B671 kit states the coordinator's ruling).
- D5: finding ids `B626-n` in describe names, the commit message and the fixture name `B626 date rule rows draft`: default Note (commission allowed it; neighbour precedent to be measured by the gate: `B618` count). The B659 template graded a `B6xx` id in a title Minor. See Q-1.
- D6: reading leads A-H are attack points, not findings; lead F (a product mutant probe that shifts the stored instant) is optional and a Note at most.
- D7: hard-stop suggestion: target 2 h, hard stop 3.5 h after Step 0, no later than 19:00 AEDT (the template used 16:00; this one starts after 15:00 and load is high). Tuesday names the time.

## Questions for Tuesday (each with a default)
- Q-1: grade of the finding ids in titles (Note or Minor). Default: Note.
- Q-2: the Essential Eight SOW path for the unit step. Default: the path the B659 stamp named (`1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md`), read-only bind mount only, existence stat only.
- Q-3: plumbing copy from `.tools/b626/scripts/` (D1). Default: YES.
- Q-4: scratch probes and product mutants in `-mut`/`-probe` only. Default: YES.
- Q-5: port block 9700-9709 was B620's earlier today (finished). Default: accept.
- Q-6: the kit asks the gate to run the `packages/db` group once; the PR touches nothing there. Default: keep (CI's own `test-db.sh` runs both configs), drop if load forces it.

## UNMEASURED
No build, test, container, mutant or probe ran. Not measured: that the copied plumbing files fit here; the red sets (RELAYED from the builder); the `Analyze` outcome (in progress); the unit and API-db counts; that `analyses` for the head is empty because the scans were still running; the rate-limit claim (72 calls); the pre-commit hook; whether a seventh reachable survivor exists (the gate's job in C3).

## Outside-the-fences disclosure
- Created a byte-identical copy `2026-10-25_B674_SEAT-G118_composer-92-gate-tier2.md.pre-stamp` beside the kit (a `cp -n` slip: Tuesday makes this copy at stamp). A delete was refused by the no-delete hook, so it is left in place; it is the unstamped copy (slot count 8) and Tuesday can use it as the control or move it.
- Two `Bash` calls were refused by the no-`cd` hook (my own `cd /dev/null` and a first call with `cd`), nothing ran. No fetch, no git write, no docker, no az, no HTTP to a hosted host, no decision-queue, no Artifact/Docs/mail. `gh` was `-X GET` under the project `GH_CONFIG_DIR`. Scratch copies of `app.ts` and the added file were written in the session scratchpad.
