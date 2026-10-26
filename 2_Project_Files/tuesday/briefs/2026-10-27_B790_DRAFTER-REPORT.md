STARTABLE: YES

# B790 drafter report (Sonnet drafter, 2026-10-27 06:12-06:2x AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B790_SEAT-M18_nexusai-887-rd774-row.md` (152 lines). Shape copied from the B777 kit (read whole, both the stamped and the `.pre-stamp` form for the slot lines). Seat `Datasec/NexusAI-M18`, ports 8760-8769, launch line carries `BRIEF_SEAT_LEVEL=sonnet`.

## BLUF
RD-887 is completable now: three keys (`NaN`, `'abc'`, `null`) added inside the existing RD-876 cell of `__tests__/rd774-risk-sql-templates.test.js`, tests only, one path, one commit. A row inside a cell moves no count, so the counts file stays at 5170 / 307 and is NOT in the diff; the kit forbids `--update-counts` (it would rewrite `_updated`). The kit makes the seat prove the gap first (mutant `|| 101` survives the unedited file), then red after the edit, plus three control mutants. Two things to rule on: the limit `0` also returns 100 (Q-1), and your instruction said "verify counts regenerated" while the right behaviour is "verify reads the pinned pair, nothing regenerated" (D-3).

## Facts re-measured (instrument; control)
- RD-887: Jira GET through `session-tools/b774/b774lib.py` (loaded by importlib, read-only `get`; no token printed). 200; Task, Low, To Do, labels `b750-finding` `b774-2026-10-27` `qa-gate-finding`, 0 comments, 0 links, created 02:36. Control: `RD-zzz` answers 404. RD-876 (To Do) and RD-774 (In Progress) read too.
- Source gate finding B750-1 read in `Briefs/2026-10-26_B750_STATUS.md` (lines 325-360 and the matrix grep): S5 (`|| 101`) survives 87 of 87, S5b (parameter default 101) reddens `defaultUnset`, `{limit:"abc"}` and `{limit:null}` return 101 over HTTP under S5. The ticket's line numbers hold at main.
- Main = `e24f16f5f41203ceb701b3578e80e2a9b1b616f6` (`ls-remote` and `gh api commits/main` agree; PR #122 merge). Moved since the sweep's frame: #123 (RD-878) and #122 landed; the counts file moved to 5170 / 307 as a result (the sweep read it correctly, 5170 / 307).
- Test file at main: blob `dfc7a44838c1`, 631 lines, 41815 bytes (raw contents saved and read); the RD-876 cell is at `:146`, one `expect({six keys}).toEqual({...})`. `grep -F 'NaN'` over the cell lines finds nothing (the arm is unpinned). Product line `backend/simpleDb.js:805` read verbatim; `|| 100` occurs once in that file (`grep -n -i -F`; control `RISK_RUN_MAX_ROWS` hits `:8` and `:805`). Blob `0d07e81a927b`.
- Counts: `scripts/verify-expected-counts.json` blob `9712206a584f`, 5170 / 307. Depth-1 census of main's recursive tree = 307 (equals `suites`). `verify-suite.sh` blob `eb9731f5cd97`, `build.yml` blob `e4e5c095263f`; CI predicate (`build.yml:83-84` `npm run verify -- --maxWorkers=2`, node 24 at `:29`) written into the kit.
- Branches/PRs: open PRs 0 (control `pulls/120/files` lists a file). Compare of every `b595`, `b703`, `b713`, `b746`, `b770`, `b777`, `records/*` head to main: ahead 0 for all 12 (control: the same compare shows behind > 0, so it reads). `refs/heads/b790*` empty (control `b777*` prints a line); `worktrees/b790-*`, `session-tools/b790*` absent (control: `b777` names exist). `records/b788` does not exist yet. Path intersection: empty.
- M18: word-boundary scan `NexusAI-M18\b` over non-`.pre-` kits dated 26-27 Oct = 0 hits; control scan for `M17` fires. Panes at 06:1x: `tuesday`, `Datasec/NexusAI-R53`, `Datasec/Security-Composer-G165`, `Datasec/MPS-R52`, `fleet-monitor`.
- Ports 8760-8769: `lsof` empty (rc 1); positive control (python listener on 8765) listed then freed (rc 1); word-boundary scan of 8750-8799 over 84 non-`.pre-` SEAT kits dated 26-27 Oct = 0 hits (scan control `8715` fires, `a8715` does not). Block 8700-8719 and 8727-8748 are named by other kits, which is why I did not reuse them. The parallel MPS kit B789 is another repository; if its drafter picked 8760-8769 the ports are only loopback test binds, but check at stamp.
- Lock tool sha256 `cf01bafb...971f` (same as B777's). `queue-jest/` empty. load1 2.26 at 06:14.
- Model: `model-routing.md:85` row L6 (test-only pin) quoted; its Sonnet column reads "1st fallback: a Sonnet raise seat applies the ready golden", its first choice is the local worker, which is not usable on Datasec (project memory: Ornith is Studio-only), so Sonnet is first. C2 (`:92`) is also satisfied. Gate G2 (`:109`) tier 2. Model id `claude-sonnet-5-5` from `models_latest.json`; `brief_seat.sh` defaults to Opus without the level (read at lines 15-30).
- Landing rule: project `CLARIFICATIONS.md` `:2067`, `:2068`, `:2073` quoted; last two landings (#123, #122) were head-pinned merge commits (C-225 text).
- Kit self-checks: lines with four underscores = 9 (8 slots plus last line); `@[A-Z_]+@` = 0; no non-ASCII; no person's name; no decision-card id.

## D-decisions (mine, for you to overrule)
- D-1 Rows, not a cell: the ticket's own words say a row inside the cell moves no count. Keys `defaultAtNaN`, `defaultAtAbc`, `defaultAtNull` (the ticket's `abc` and `null`, plus the NaN its fix shape names), in-process shape; the HTTP alternative would boot a server and add a cell (count moves).
- D-2 Mutant-first: the seat shows `|| 101` leaves the unedited cell green (the survival), then red after the edit. Control mutants: M2 (`|| 1`), M3 (arm removed; sqlite's NaN-bound behaviour is unmeasured, reported either way), M4 (parameter default 101: must redden `defaultUnset` ONLY, proving the new keys pin the arm and not the default).
- D-3 Counts: the seat never runs `--update-counts`; the proof is that the plain verify reads `5170 / 307` and the counts file is byte-identical to main (blob `9712206a584f`). This is how I read "verify counts regenerated"; a regenerate would rewrite `_updated` and put a second path in the diff.
- D-4 Title of the cell left alone (a rename changes a test id; the title's "default 100 unchanged" stays true).
- D-5 `0` is probed and not pinned (D-ZERO): `parseInt(0, 10)` is 0, falsy, so `0` returns 100 while `-5` returns 1. Whether that is intended is the product owner's, not a test's.
- D-6 Gate tier 2 (Sonnet), because the mechanism was already measured by the source gate.
- D-7 Time: target READY 2 h, hard stop 3.5 h after Step 0, as you asked, written as relative guidance in the Stamp slot (a typed absolute time is yours); one verify, a baseline, a green run and four short mutant runs. Load is low (2.26).
- D-8 Partition: one path. B788's `records/b788` touches `HISTORY.md` only and its other writes are in the project folder and Jira (the seat only reads those). RD-876 part 2 will touch the same clamp and cell later; named in the kit, and the REFUSE "main moved" check covers it.

## Questions for Tuesday (each with a default)
- Q-1 The limit `0` returns 100 rows on main by the same arm. Default: not pinned, probed, reported in FOR TUESDAY; you decide whether to ask the product owner. Alternative (not drafted): pin `0` -> 100 in the same cell, which would lock in behaviour that may be unintended.
- Q-2 Gate tier. Default tier 2 (Sonnet, G2). Raise to tier 1 only if you read a test-only row on a clamp that guards a ceiling as G1 material.
- Q-3 Port block. Default 8760-8769 (free and unnamed). The seat is expected to bind nothing.
- Q-4 Launch timing. Default: launch now; the lock is empty, the lane is disjoint from the live seats.

## UNMEASURED
That the three limits return 100 on this node (read from the line and relayed from the gate's HTTP probe for `abc` and `null`); what `0` returns by running; that M1 survives in the rd774 file alone; sqlite's behaviour with a NaN bound limit (M3); the printed failure shape; verify wall time at this load; CodeQL on the new head; Linux runner and node 24; whether `Deploy demo` stays skipped at the eventual merge.

## Outside-the-fences disclosure
- Wrote only the two files above. No Artifact, Docs, mail or chat tool. No `cd`; absolute paths. No `decision_queue.sh`, no `briefs_staged`, no scoreboard, no `_ledger.md`, no WEDNESDAY or FRIDAY tree.
- Scratch files in the session scratchpad (`rd887.py`, and raw copies of the rd774 test, `simpleDb.js`, `security-fixes.test.js` and the counts file at main `e24f16f5`). The `security-fixes.test.js` copy was downloaded but not read.
- Read the finished source-gate STATUS (`Briefs/2026-10-26_B750_STATUS.md`) and the project `CLARIFICATIONS.md` by line/grep (lines 2060-2075, 2405-2426); listed the names in `worktrees/` and `session-tools/` (grep counts only). Read the previous kit B777 and its `.pre-stamp` and drafter report from the briefs folder.
- Reading the Jira ticket executed `b774lib.py` module code (which also loads a sibling `jira-adf.py`); only its `get` and `adf_texts` were called. Two other GETs: RD-876, RD-774, and the RD-zzz control.
- One loopback listener on 127.0.0.1:8765 for 6 seconds (positive port control), released (lsof empty after). All GitHub calls were `gh api -X GET` under the NexusAI `GH_CONFIG_DIR`; `git ls-remote` only in the repo. No hosted host contacted; no fetch, clone, npm or jest.
