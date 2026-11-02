STARTABLE: YES

# B1124 drafter report (kit B1124 / SEAT-H102, drafted 13:15 to 13:31 AEDT by `date`)

## BLUF
Kit `2026-11-02_B1124_SEAT-H102_hpsmpoc-311-flake-closeout.md` (18,082 bytes by `wc -c`, 11 slot lines of four underscores by `grep -c`, 0 non-ASCII) closes HPSMPOC-311 with evidence: the planted-red demonstration and the 1000-run record, in the one test file `web/src/server/auth/revocations.race.test.ts`. Sonnet C2 (`model-routing.md:92`), gate G2 (`:109`), pane `Datasec/HPSM-POC-H102`, no port block. The outcome may be ZERO commits (evidence only) or ONE commit if a measured red proves a test defect; a product break (a red whose shortfall exceeds the file's own 20 ms slack, or any other red) is a STOP finding. Startable once stamped; no STOP found at drafting. Main `4b3cefae` is unchanged at 13:31; no H102 pane, no `b1124*` ref, no `.tools/b1124`.

## Facts re-measured (instrument, time)
- Main `4b3cefae71ca43f6f86d23c77dd75ae101a51fd3` (`gh api -X GET git/ref/heads/main`, 13:15:52 and 13:31); open PRs 0; `compare main...main` ahead 0 behind 0 files 0.
- Test file at the pin (raw, 206 lines, `grep -n`): `:122` `expect(b.waited).toBeGreaterThanOrEqual(300);` (inside the row at `:96`, two variants), `:147` the wait row, `:149` `staleMs: 400`, `:153` `CLOCK_SLACK_MS = 20`, `:160` `>= 400 - CLOCK_SLACK_MS`. Old form at parent f653c3bb `:156` `>= 400` (`gh api` raw at that ref). PR #198 squash 2d05b95a: three files, parent f653c3bb (`commits/2d05b95a`).
- Product `revocations.ts` (220 lines): `:29`, `:93`, `:102`, `:107` printed by `grep -n`. Stale time counts from the lock file's `mtimeMs` (`:102`), so the wait is measured from the file's own time; a coarse Linux file time is the plausible 399 (a reading, not measured).
- CI: job name at `ci.yml:451` (NOT `:476` as the sweep says), `node-version: 24` `:463`, `run: npm test` `:478`; `web/package.json` `:10`, `:11`, `:12`. `vitest.config.mts` exists (tree), `vitest.config.ts` does not.
- Jira HPSMPOC-311 read with the project helper: Backlog, labels b473-2026-10-22, flaky-test, test; one comment (PR #198 merged, "Not moved to Done: the Done-when asks for the same test run 1000 times in a row"). Its done-when and the product-break clause are quoted in the kit.
- Node 24: `.tools/node24/bin/node --version` v24.21.0. Helpers present: `.tools/b198/lock.sh`, `.tools/b1113/{hv.sh,heavy.sh,waitload7.sh}` (headers read). `df -g` 36 GiB free; load1 7.19 at 13:31 (the waiter decides).
- Ports: `listen(` / `createServer` count 0 in the test, `revocations.ts`, the child (control: a planted line counts 1). `lsof -nP -iTCP:9500-9999 -sTCP:LISTEN`: 9561, 9571, 9572 (H100, H101). The word-bounded scan `\b9[0-9]{3}\b` over 125 non-`.pre-` SEAT kits of 11-01 and 11-02 printed 9570 and 9579 (B1122) among many; control: the same scan names 9561 and 9900. No block is needed. Free by both instruments if one is ever wanted: 9580-9589.
- Partition (program `python3 -I -B`): `compare main...<branch>` file sets of b1095 (4), b1097 (7), b1104 (24) and the kit-declared sets of H100 (B1113) and H101 (B1122) intersect `revocations.race.test.ts` and `revocations.ts` in 0 (control: `SqlServerWakeRetry.cs` found in b1095). Live panes (13:21 `tmux list-panes -a -F '#{@cockpit_name}'`): tuesday, HPSM-POC-H101, -G285, -H100, -G280, MPS-G284, -G283, -M76, fleet-monitor. One `launch_when_cool` process was seen at 13:21 and gone by 13:21:32.
- Landing: main's last commit (HPSMPOC-405/409 squash) has 1 parent (`commits/<sha>`). The written rule `CLARIFICATIONS.md:3617` is the records repository's and was NOT re-read (the local copy is the old 29 KB file): RELAYED from B1122.

## Severity and REFUSE cross-checks (done)
- Every step 0 to 7 carries its failure class (STOP, FIX or REPORT) in its text; step 4 and 5 state which cell or red is which class; the product-break STOP is quoted from the ticket.
- Every REFUSE line was run against what will be live at launch: stamp slots (pre-stamp copy reads 11; fires until stamped, by design); `.tools/b1124` and `wt-b1124-*` absent (control `.tools/b1113` present); `b1124*` ref 0 and open PRs 0; main-moved grep over `compare main...main` 0 files; no H102 pane (tmux 0 hits for H102, control: H101 1); `df` 36 against 25; `gh auth status` account kamilDatasec; Node 24.21.0. None fires now. The tmux grep also confirms H101 is the live pane the kit names.

## D-decisions made in the kit
- D-1 Zero commits is legal: the ticket's remaining clauses are measurements. Without it a seat would invent an edit to have something to gate. The last line has an EVIDENCE-ONLY form.
- D-2 The red-then-green demonstration uses a deterministic plant (the lock file's time set k ms behind the clock with `utimesSync`, k in 1, 10, 19, 21, 40) beside product plants (d = 1, 10, 40). A plain 1 ms product break is not reliably red under the old assertion (5 ms polling overshoot), so predictions are written first and counts are reported.
- D-3 The 1000-run record: whole file 1000 times if seconds-per-run x 1000 is at most 9000, else the wait row alone 1000 times plus the two `:96` rows 1000 times (they hold `:122`). Chunks of 50 under the heavy lock at load1 below 7.
- D-4 Classification of a red by the file's own `CLOCK_SLACK_MS` (20 ms): at most 20 = test defect (FIX); above 20 or any other red = product finding (STOP).
- D-5 The `:122` bound is changed only if a measured red shows it; then 1000 runs restart from zero at the pushed head.
- D-6 Gate G2 reads the STATUS in the evidence-only case.
- D-7 No ticket key, card id or B-number in changed lines or the message (HPSM model kit B1122 rule).

## Q-questions for Tuesday (each with a default)
- Q-1 With zero commits, does G2 run on the STATUS alone? Default: yes (cheap, one tester).
- Q-2 Should the deterministic file-time rows become permanent test rows? Default: no (they test the slack's arithmetic; the evidence stays in STATUS).
- Q-3 Target READY is "about 4 hours": 1000 vitest launches may take over 2 hours on this loaded machine. Default: as written, hard stop 20:00.
- Q-4 One waiter at a time: B1124 and B1125 are both drafted. Default: B1124 first (owner's first project), B1125 after it launches and is verified.
- Q-5 Confirm no port block (none needed). Default: yes.

## Contradictions
- Sweep says CI name at `ci.yml:476`; `grep -n` prints `:451` (`:478` is right).
- Sweep says the 1000 runs cost "about 7 minutes of one core"; that counts only the 400 ms of waiting, not 1000 vitest start-ups. UNMEASURED per-run time is why the kit measures it first.
- Sweep's "NH4 reads `revocations.ts`": true; the kit also requires its blob equal to main.
- The ticket text says the `it(` is at `:147` and the assertion at `:156`; at main they are `:147` and `:160` (the slack added four lines).

## UNMEASURED
No npm, vitest, plant or repeat was run (read-only drafter). Not measured: seconds per run; whether macOS can ever show the 399; the margin of `:122` (`b.waited` against 300); the Linux coarse-tick behaviour (a reading); that `utimesSync` before the product reads the file time yields the predicted shortfall (the seat predicts first); the written landing rule text; that the CodeQL ruleset is silent on a test-only PR.

## Outside the fences
None. Read-only: `gh api -X GET` (contents at the pins, refs, compare, commits) under the HPSM-POC `.gh-config`; `ls -d`, `lsof`, `tmux list-panes`, `ps`; the project Jira helper `.tools/b1007/jira.py` for one key (prints; no token); `node24/bin/node --version`. Scratch copies of raw files under the session scratchpad only. No decision_queue, Jira write, Azure, mail or message; no `cd`; no Artifact or Docs call. `gh auth status` printed a masked token prefix once; no secret reached a file.
