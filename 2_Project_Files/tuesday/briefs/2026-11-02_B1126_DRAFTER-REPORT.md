STARTABLE: YES

# B1126 drafter report (kit B1126 / SEAT-H103, drafted 13:29 to 13:40 AEDT by `date`)

## BLUF
Kit `2026-11-02_B1126_SEAT-H103_hpsmpoc-wake-close-pins-fix-round.md` (18,404 bytes by `wc -c`, 11 slot lines of four underscores by the kit's own grep, 0 non-ASCII) is one commit on `b1095/hpsmpoc-wake-close-path-and-narrative-pins` @ `2746b0737d51a261fcf69b76b76da4857ade7149`: five retry rows (R1-R5) and three guard rows (G1-G3) plus two comment-line fixes; three paths; no product behaviour change. Sonnet C2, ports 9580-9589, pane `Datasec/HPSM-POC-H103`; gate after it ROUND 2 OF 2 on class A (NO GO 1 before: B1107), class B NO GO 0 before, tier 1 Opus. B1126 was free (`ls` 0 before writing; `ls` of B1125 shows only an MPS kit). Startable once stamped. Two rows may have no distinguishing cell (G2, G3, Q-1, Q-2); the kit handles both without a silent skip.

Severity or STOP is written against every step line (THE WORK steps 1-8); every REFUSE is written against what will be live at launch (pane list, ports, main, branch, PRs) and none stops on a path outside the three.

## Facts re-measured (instrument, time)
- Main `4b3cefae71ca43f6f86d23c77dd75ae101a51fd3` (gh api ref, 13:29; `compare 4b3cefae...main` 0 files: main has not moved since the gate). Branch `2746b0737d51a261fcf69b76b76da4857ade7149` (compare main...branch: ahead 2, behind 1, 4 files = the kit's three plus `NarrativeOutputValidator.cs`). Open PRs 0; `matching-refs/heads/b1126` 0 (control `b1095` 1).
- Line pointers printed by `grep -n`/`awk NR` over raw files at `2746b07`: `SqlServerWakeRetry.cs` (123 lines) `:47` the table, set `:78 :85`, cleared `:89 :93 :99 :105`, read `:120`, comment `:42` (reads "takes it out when the open ends or the connection starts to close"); `SqlServerWakeOpenRetryTests.cs` (666 lines, `[Fact]` 22; control `NOSUCH-zz` 0) false sentence `:29-30`, product summary `:20-21` says the retried operation sends its commands again, `:181 :212 :334 :353 :598`; guard test (417 lines, `[Fact]` 16) `:39 :71 :405`; validator `:198 :300`. All eight lines the gate cites for a5 matched.
- CI at `2746b07` (679 lines, `grep -n`): `:87` job `api` test, `:252` / `:255` the SQL Server part filters, `:303` the `bad = sum(...)` line (every outcome `Passed`), `:314` the floor. Landing rule: records `CLARIFICATIONS.md:3617` (5,346 lines at 13:32).
- Partition by program (`compare` file lists, `grep -c -x -F -f`): b1104 @ `f762cc7a3021ef774c453980db91cd8fa5f89826` has 24 files, 6 under `api/` (Endpoints x3, two Assessment tests, `Contract/openapi.delta.json`); intersection with our three **0**; control b1095's list against itself 4. b1097 (7 files, 0 under `api/`): intersection 0. The "Main moved" pattern over the same lists: control line 1, main-moved 0, b1104 0, b1095 3. H100/H101/H102 sets are RELAYED from their kits (`web/` only); no branch of theirs is on origin except b1097. Only `b1104` and `b1095` are origin branches matching `b11xx`.
- Panes (`tmux list-panes -a -F '#{@cockpit_name}'`, 13:3x): `tuesday`, `Datasec/HPSM-POC-H101`, `-G285`, `-H100`, `Datasec/MPS-G284`, `-G283`, `-M76`, `fleet-monitor`. G280 (the B1107 gate) is gone; H102 (B1124) is not live yet; no H103.
- Ports: `lsof -nP -iTCP:9580-9589 -sTCP:LISTEN` 0; word-bounded scan `\b9[0-9]{3}\b` over the 127 non-`.pre-` SEAT kits of 2026-11-01 and -02: 9580-9589 in 0 hits; control `\b9561\b` in 3 lines (H100). Live listeners in 9500-9999: 9561, 9571, 9572 (H100, H101). B1124 declares no port block.
- Model: `model-routing.md` `:92` (C2), `:108` (G1), `:111` (G-cap); `models_latest.json:23` = `claude-sonnet-5-5`; `brief_seat.sh:24` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`. Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. `gh auth status` (project config): logged in as the project's Datasec account. `df -g` 36 available; load 6.11 at 13:31 (`uptime`). `.tools/b1126` and `.tools/wt-b1126-*` absent; `.tools/b1095/{lock.sh,heavy.sh,hv.sh,waitload7.sh,repeats.sh,plants.py,trxrows.py}` and `.tools/b198/lock.sh` exist.

## Why the rows are shaped as they are (design reading from source, UNRUN)
- **R1 needs an order, not just two connections.** With a5 (one shared key) a naive "A closes while B opens" cell stays green, because A's own good open already cleared the shared key before A's close. The cell goes red only if A's closing clear runs before B's opening set and A's failure is thrown after it. The kit states that order and requires a5 red in R1 and R2 on every run; the gate's W5 got only 155 of 200 retried under a5, which is the cost of an ungated cell.
- **R4/R5 are the E4 construction** at `.tools/b1107/scratch/B1107Rows.cs:645-690` (good open, state forced Closed outside EF, a second open fails leaving the state not Closed, then a failing close). PA2 differs only in the async cells and PA2b only in the sync cells (`c2-table-head-vs-PA2-PA2b.txt`), so there is one row per path.
- **G2 (b4):** `1,000 findings share this action` is refused with or without the thousands branch (without it the claim is read as `000`, which is also ungrounded), so the gate's literal cell may not turn b4 red. A form against a group size that the short reading would ground (my guess `1,005` vs size 5) is unrun. The kit makes the seat find the cell by program or STOP.
- **G3 (b5):** the claim number must follow a non-word character and be followed by white space, so removing it versus replacing it with a space leaves the neighbouring characters unchanged. I could not construct a cell by reading. The kit makes the seat search by program; no cell means no row and no stop.

## D-decisions made in the kit
- D-1 Paths are three (retry source comments only, retry test, guard test); `NarrativeOutputValidator.cs` stays byte-equal (B1107-12 is a Note, left).
- D-2 R3 (sync twin of `:598`) answers B1107-2 (a3); B1107-6 and -7 are comment-line edits in the gate's words, with `:42` and `:29-30` as measured.
- D-3 Plants: at most 14 (P0, a1, a2, a4-a7, a3, PA2, PA2b, b2, b4, b5, one comment edit); gate's rule set a1, a2, a4-a7 re-run so that a survivor is caught here and not by the next gate.
- D-4 Mechanics (clone, trees, fetch, helpers) by reference to the B1095 kit's step 3, helpers copied from `.tools/b1095/`, to hold the size cap; the property checks and the push are written out.
- D-5 Hard stop and target READY are left to Step 0 clocks (slot), outer bound the stamp's.

## Q-questions for Tuesday (each with a default)
- Q-1 G3: if the seat proves no distinguishing cell for b5, may the round end READY with no G3 row and the proof printed (the gate's Minor B1107-5 then remains for the next gate to judge as equivalent)? Default: yes, as written. Alternative: STOP, which blocks the whole round for a Minor.
- Q-2 G2: if no cell separates b4, the kit STOPs `NEEDS TUESDAY`. Default: as written. Alternative: treat it like G3.
- Q-3 Rows are async only for R1 and R2 (sync twins not required). Default: async only; the gate's a5 moved both sync and async, so the sync variant is a possible Minor next round.
- Q-4 The gate's class-B round number is unstated in B1107's verdict beyond "round 1 of 2, NO GO 0 before" and no NO GO counted. The kit writes "class B NO GO 0 before" and no round number for B. Default: as written.
- Q-5 Ports 9580-9589. Default: yes.

## Contradictions and oddities
- B1107-6 quotes "takes it out when the open ends"; line `:42` reads "...when the open ends or the connection starts to close". The claim is imprecise, not absent; the kit gives the gate's replacement wording.
- Tuesday's brief says the next gate is "ROUND 2 OF 2 on class A"; the G-cap line (`:111`) says "Two NO GO rounds on one class: STOP". Written both ways in the kit: a second NO GO on class A is a card.
- The gate's STATUS still lists the B1095 lanes G276/H98/H99 as absent and names G285/H100/H101 as new; this kit's pane list is the live 13:3x read, not the gate's.
- B1107-8 asks for the squash body to carry measured sentences; the builder cannot amend, so the kit tells the seat to write a true message and leaves the squash to Tuesday.

## UNMEASURED
No clone, build, test or plant was run. Not measured: whether `CloseFake`/`StateOnlyConnection` can host the gate for R1/R2 without a deadlock under a5 (the retried A run must not wait on the held B); that R1 and R2 turn a5 red on every run; G2's and G3's cells; whether PA2 and PA2b are red under R4/R5; the SQL Server leg; hosted CI and CodeQL; H100/H101/H102 path sets (relayed).

## Outside the fences
None. Read-only: `gh api -X GET` on `datasecau/HPSM-POC` (refs, compare, raw files at `2746b07`, `ci.yml`) and on `datasecau/HPSM-POC-analysis` (raw `CLARIFICATIONS.md` for the `:3617` line); reads of the project's `Briefs/` (B1107 STATUS and evidence), `.tools/b1107/scratch/B1107Rows.cs` lines 640-735, `ls` of `.tools`; `lsof`, `tmux`, `df`, `uptime`. Scratch copies only under the session scratchpad. No `cd`, decision_queue, Jira, az, ssh, docker, Artifact, Docs or message.
