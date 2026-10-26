STARTABLE: YES (after Tuesday stamps the 7 slots and the last line; both branch heads and main unmoved at 01:54 AEDT; ports 8660-8669 free; no B772/G159/.tools/b772 anywhere)

# B772 DRAFTER REPORT (drafted Tue 27 Oct 2026 from 01:53 AEDT)

## BLUF
1. One tier-2 batch gate (Sonnet, `BRIEF_SEAT_LEVEL=sonnet`, row G2 line 109) for `b767/hpsmpoc-355-pkcs-rows @ 784dc978` (3 paths) and `b768/hpsmpoc-356-228-infra-tests @ a3fa1c0e` (2 paths), both ahead 2 / behind 0 on main `4c067e4f`, file-disjoint; one verdict per branch, round 1 of 2 each, on one combined first line and one combined last line.
2. The gate re-measures: builder-named mutants m1..m3c, plus four unnamed (u1..u4) for branch 1; guard mutants g1..g7 (g6, g7 unnamed) and ten plants (5 red, 5 harmless) against head AND base guard for branch 2; AST-equality of commit 1 with a planted-constant control; csproj comment-only proof with a planted pin change as control; names lost; class, Api project (SQLite), reader, whole infra.
3. The csproj files make this a tier-1 escalation surface under G2: the kit makes "any byte outside an XML comment" a STOP for tier 1, and demands a program proof with controls that can fail.
4. The SQL Server leg is UNMEASURED-ON-SQLSERVER (no docker): the kit writes the shard predicate (ci.yml lines 254-255 filter includes the Pkcs class; proof step fails on any non-Passed outcome; floor 110) and caps branch 1 at GO WITH FINDINGS (conditional) until the PR's shard is read by Tuesday. No PR exists yet for either branch.
5. Ports 8660-8669 (lsof rc 1; word-boundary scan of non-`.pre-` SEAT kits of 10-26 and 10-27 for `866x` = 0 hits, control `860x` hits B758, B767, B770). The gate should bind none.
6. Q-questions below; the main ones: Q1 B734 class overlap (default different class, round 1), Q2 the csproj STOP rule, Q3 the combined verdict line.

## Facts re-measured (instrument, control)
- `gh api -X GET git/matching-refs/heads/main` = `4c067e4f...`; `heads/b767` -> `784dc978...`; `heads/b768` -> `a3fa1c0e...` (control: the refs exist and equal the kit's shas; they equal what the builders' STATUS files state).
- `compare main...b767/...` ahead 2 behind 0, files 113/0, 2/2, 1/1 (gh jq `.files[]`); `compare main...b768/...` ahead 2 behind 0, files 23/13 and 199/3. The user's brief numbers match; sums 116/3 and 222/16 match the builders' `git diff --stat`.
- `git --no-optional-locks cat-file -t` of all three shas in the shared checkout = `commit` (the shared checkout holds them, so a clone of it needs no fetch for them; the kit still orders the one fetch so the gate reads `gh/` refs).
- `pulls?state=open` = #222 only, `b709/hpsmpoc-timing-rows-354`.
- `lsof -nP -iTCP:8660-8669 -sTCP:LISTEN` empty rc 1. `tmux list-panes -a`: tuesday, Datasec/NexusAI-M16, Datasec/MPS-M38, Datasec/MPS-G158, Datasec/MPS-G157, fleet-monitor (no HPSM-POC-G159, no H39/H40/R50 pane; the records seat pane R50 is not listed, so the records seat is either not yet launched or closed: UNMEASURED which). `ls briefs | grep -E 'G159|B772'` = 0 before my files; `.tools/b772` and `.tools/wt-b772-*` absent (`ls -d` error; control: `.tools/b767` lists).
- Routing: `sed -n 109p model-routing.md` prints row G2 (tests-only/config/CI/tooling, Sonnet first, "11 Sonnet-tier gates on 10-12 ... Opus has gated tier 2 until now"). Model id `claude-sonnet-5-5` from `models_latest.json` (`grep` of the sonnet block; line number not re-read this time).
- `ci.yml` at main (read via `git show`): `on:` push main / pull_request / workflow_dispatch (lines 14-18); shard filter lines 254-255 (the Pkcs class is in `api-other-and-feedback`); proof step (floor 110, any non-Passed outcome fails); `infra` job runs `bash infra/scripts/validate.sh`, whose line 21 is `BICEP="$BICEP" python3 tests/test_security_baseline.py`.
- Builder STATUS first lines: B733 line 1 `GATE VERDICT B733: pr225 GO WITH FOLLOW-UPS round 1 of 2 ...` (pin bump, different class), B734 line 1 `GATE VERDICT B734: #221 GO WITH FINDINGS @ 22d5c13 (round 2 of 2, THE CAP, on class "closing the open lists of the shard-job reader" ...` (neighbouring to Class B).
- Kit self-checks: four-underscore line count 8 (7 slots + last line), `@[A-Z_]+@` count 0, non-ASCII 0, no person name (grep for the owner's names = 0). Control: the same pattern counts are what the kit's REFUSE section tells the seat to expect.

## D-decisions (mine, for Tuesday to accept or override)
- D1 Ports 8660-8669 as commissioned; the gate binds none (api tests host in-process; infra is Python), a listener at start is a STOP.
- D2 One first line carrying both verdicts (so the round-count instrument, which reads only first lines, sees both classes); one combined last line. A per-branch split into two STATUS files was rejected: one session, one channel, one watcher line.
- D3 Finding ids `B772a-n`, `B772b-n`, `B772s-n` (shared).
- D4 Unnamed-mutant survivors (u3, g7) are Notes (row-strength gaps), not Majors; builder-named mutants that survive are Major M1. This keeps round 1 from being decided by an invented mutant.
- D5 Branch 1 verdict capped at GO WITH FINDINGS (conditional) while SQL Server / the shard / the `api` job are unread; same for the infra job until a PR exists. Nothing starts on a bare branch push (ci.yml `on:`).
- D6 Load rule below 8 (the dotnet builders used 8), target 100 min, hard stop 160 min, never after 06:30 AEDT 27 Oct (the builders' own window).
- D7 The pre-existing `B254 (HPSMPOC-254)` header on the reworded Api csproj line is a Note (carried, byte-equal outside the reworded words), whereas a new `B###` in code/messages/test names is a Blocker per the builder kits' hygiene rule; a ticket key in a code comment is the project's convention (Note), in a test name a finding.
- D8 The gate may not touch `.tools/b767`, `.tools/b768`, their trees or scripts; it writes its own mutant scripts from the kit text. Predictions in the kit are labelled hypotheses, not facts.
- D9 The "R11 guard" in the commission is named in the kit by its mechanism (the dispatcher stays-awake guard); the label R11 appears in the B768 builder kit (line 57) and is quoted in the kit's first paragraph.

## Q-questions for Tuesday (each with a default)
- Q1 Does B734's class ("closing the open lists of the shard-job reader", NO GO 0, cap round, GO WITH FINDINGS) count as Class B (reader docstring plus dispatcher guard)? Default: NO, different class and PR; both classes round 1 of 2. The gate raises it back as a Q if it disagrees, never rules.
- Q2 The csproj files: keep "any byte outside an XML comment = STOP for tier 1 (G1)"? Default YES (G2 text treats config as tier 2 but the template's escalation line names csproj; both csproj edits are claimed comment-only).
- Q3 Accept the single combined verdict line (D2)? Default YES.
- Q4 Should the gate also run the whole Api project on the BASE for the names diff (about 5.5 min, builder's figure)? Default YES, cut first if the hard stop nears.
- Q5 Do you want the gate to read the PRs' CI if you open them before the gate ends? Default: it re-reads `pulls?state=open` at start and verdict and judges any check-run it finds, noting paused/billing starts as NOT STARTED.
- Q6 The records seat pane (R50) is not in `tmux list-panes`: is the records branch `records/b771` untouched by this gate? Default: yes, it is NOT YOURS in the kit and nothing in the gate reads it.

## UNMEASURED
Nothing was built or run. Not measured: that the head class and Api project reach the builders' counts on this machine (SDK 10.0.402 vs CI 10.0.403); that u1..u4 / g1..g7 behave as predicted (my reading of source, labelled so in the kit); whether the a-mut tree can build offline; that the new rows leave the 110-database floor alone (argued); the runner's Python; any real GitHub workflow parse; whether the records seat pane is live; the line number of the model id in `models_latest.json`.

## Outside-the-fences disclosure
Read-only: the kit templates and rules above; `ci.yml` and `validate.sh` via `git show` at main; the two builder STATUS files and kits; first lines of B733/B734 STATUS; `gh api -X GET` only (matching-refs, compare, pulls) under the project's `GH_CONFIG_DIR`; `lsof`, `tmux list-panes`, `ls` of `.tools` (a listing, which printed a long set of tree names; nothing opened). No `decision_queue.sh`, no Jira, no `fleet/briefs_staged/`, no `scoreboard.md`, no `_ledger.md`, no WEDNESDAY/FRIDAY tree, no fetch, no clone, no git write, no mail/chat/Artifact/Docs tool. One tool call was refused by a hook (a `cd` and an unquoted `=`-word): re-issued without them. One `gh` jq call errored (array not object) and was re-run. Written: only the two files named by the commission (`.../briefs/2026-10-27_B772_SEAT-G159_hpsmpoc-355-356-batch-gate-tier2.md` and this report).
