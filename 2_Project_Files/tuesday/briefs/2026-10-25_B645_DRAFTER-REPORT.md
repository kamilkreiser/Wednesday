# B645 DRAFTER REPORT (gate kit for MPS PR #110, ROUND 2 OF 2 (the cap), tier 1, SEAT-G107)

Drafted 2026-10-25 08:38-08:43 AEDT (clock from `date`) by the read-only gate-kit drafter (Sonnet 5.5). Nothing was built, run, cloned, fetched, mutated or bound; nothing was written in any project. Two files under `tuesday/briefs/`. No `.pre-stamp` copy was made: `cp` the kit to `.pre-stamp` before stamping.

## Startable
**Yes, once Tuesday stamps.** Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B645_SEAT-G107_mps-110-gate-round2-tier1.md`, 99 lines. Four-underscore slot lines: 8 (seven slots at lines 37-43, last line 99); `/usr/bin/grep -c -E '_''_''_''_'` = 8 at 08:43:20, control scratch file reads 1. `@[A-Z_]+@` count 0. Non-ASCII lines 0. Ports **9960-9969** per Tuesday's correction (see Q-1).

## Facts re-measured (MEASURED-BY-DRAFTER, `date` in brackets)
- `ls-remote` [08:39:11]: main `93e1cab5` (unmoved since round 1); branch = `refs/pull/110/head` = `650ddfb7ef8a9888afec53ccbee3f9547922f1c2`; `refs/pull/110/merge` = `da66d816ffcf5e2cb6695996110b6cf31afbb981` (round 1's `e9945088` is obsolete; object not in the shared clone). Nothing moved against Tuesday's 08:3x read.
- `pulls/110` GET: open, not draft, mergeable true, state `clean`, 3 commits, 5 files, +591 -4. `commits/da66d816`: parents `93e1cab5`, `650ddfb7`, tree `8264fee3...` = `rev-parse 650ddfb7^{tree}`. Commits chain `ff7a4ba4` -> `34ccb02b` -> `650ddfb7`. `compare` ahead 3 behind 0.
- Delta `34ccb02b..650ddfb7`: numstat `411 0` on the one new file; `src docs web .github scripts` Engine and Import test trees: 0 differing paths; `src` tree `f8d1a883a038` equal at both; validator blob `e7c6f862e6f0` and `GovernedNull.cs` blob `ccc2bc4175ee` equal; new file 411 lines, 0 non-ASCII; commit ends with the attribution line. `rev-list` `0 3` against main.
- Check-runs at the head [08:39]: 9 of 9 completed success. Analyses at `650ddfb`: 4 (csharp, javascript-typescript, python, actions), results 0, error empty. Open alerts 0 on the PR ref and on main. Open PRs: #110 and #111.
- SQL Server: `ci.yml` at the head has 0 lines naming it; `dotnet` job is build + test of `MpsCalc.slnx` (lines 42-43). Round 1's lineage has no SQL Server leg. Marked UNMEASURED-ON-SQLSERVER in the kit.
- Panes [08:39:17]: tuesday, MPS-G105 (%441), NexusAI-M8, Security-Composer-J12, MPS-M20 (%432), fleet-monitor. `heavy-slot-1` holder `B643 08:30:06 rounding` (G105). No `b645` tree. load averages 7.36 8.59 9.19. `models_latest.json` opus = `claude-opus-5-5`. `model-routing.md` G1 at `:108`, G-cap `:111`.
- Ports [08:40:12]: `lsof` 9960-9969 rc 1; `-w` scan of the 24-25 Oct `*SEAT*` briefs for `996[0-9]` lists nothing (control `9930` lists the B643 kit and its `.pre-stamp`). My own first read found 9920-9929 named by the live B642 (NexusAI M8) brief at line 20; Tuesday's correction agreed.
- The other live MPS seat G105 (B643, PR #111) is fenced in the kit's NOT YOURS section: ports 9930-9939, `.tools/b643`, `wt-b643-*`, `heavy-slot-1`, branch `b630/...`, head `0c275f48`.

## Decisions I made (D)
- **D1 Opus, row G1, `BRIEF_SEAT_LEVEL=opus`, pane `Datasec/MPS-G107`, suffix G107, findings `B645-n`.** Recommend accept.
- **D2 Ports 9960-9969** (Tuesday's correction, not 9920-9929). Accept.
- **D3 Checks renamed R1-R7** (not C1-C12) because round 2 is narrow: R1 closures of B619-1/-2/-3 rebuilt from B619's text with the 2x2 (hole at round 1's tests, killed at the head) and the zero-cost control pair (V3c); R2 delta/tree proof; R3 the 91 cases (typed expectations, literals re-derived by the gate's own probe, flake runs); R4 survivor hunt (carried N1-N6, V2a/b/w, V3b/c, V4c/d, plus 12 own G-mutants); R5 whole line; R6 B619-6 siblings map; R7 CI/CodeQL/merge/gitleaks/process. Round 1's 3000-document corpus is NOT redone because the `src` tree is byte-equal (stated in the kit). Recommend accept; strike if you want the corpus replayed at the head.
- **D4 Grading:** a survivor of V3, V2 or V4 is Major SAME CLASS (V4 raised from round 1's Minor because Tuesday commissioned it into the class); any reachable survivor in the class is Major; each Major is labelled SAME CLASS or NEW so Tuesday can apply the cap. Recommend accept.
- **D5 Cap statement written in the kit and the verdict:** same-class NO GO means Tuesday cards the product owner, no round 3 (routing `:111`; `CLARIFICATIONS.md:1072` RELAYED from the B634 brief).
- **D6 B619-4 ruling** (TERM_GAP at the first remaining row accepted) quoted as binding so the gate does not regrade it.
- **D7 Hard stop:** target verdict 2 h, HARD STOP 3.5 h after Step-0 `date`, never later than 12:30 AEDT (the B643 value). Round 1 took about 3 h for 35 mutants; this round is narrower but has about 25 mutant builds under load 7-11.
- **D8 Verdict token** GO / GO WITH FINDINGS / NO GO (B619's form).
- **D9 `Q-1: YES`** is needed for R1, R3, R4 (scratch rows, probe class, mutants in `-mut` only).
- **D10 Whole-Api once for V3 and N4** (the dangerous direction) at the head; the SQL Server statement as UNMEASURED.

## Questions for Tuesday (Q)
- **Q-1 (answered):** ports. The commission said 9920-9929; B642 (live NexusAI M8) holds it; kit uses 9960-9969 as you directed. Nothing further needed.
- **Q-2:** launch order against G105's `heavy-slot-1` and load1 7-11: launch G107 now through the one waiter (it waits for a free slot and load below 7), or hold until G105 finishes? My read: launch, the heavy-slot convention handles it, but both gates compete for the same two cores' worth of headroom.
- **Q-3:** the PR title and body were NOT re-read after the push (the body's text and the squash settings from B643's report apply: squash carries PR title and commit messages). The kit makes R2 re-read them. If the body still holds ticket keys, say whether you edit it before the squash.
- **Q-4:** the merge-ref `da66d816` is not in the shared clone, so the gate does the one in-clone fetch (B619 method). Confirm that the deploy-key fetch under the shared git lock is still approved for this seat.

## Not done / UNMEASURED
Every build, test, mutant, probe, clone, fetch and bind; the case x killer table (builder's, RELAYED); whether V3/V2/V4 survive in the whole Api project (round 1 ran only V3 and N-mutants wide); the PR title/body after the push; Jira (not read, none needed); CodeQL umbrella after any re-run; the new file's body beyond its header, helper signatures and theory attributes (read lines 1-25 and a grep of attributes, not the whole file).

## Fences kept
`git --no-optional-locks` read verbs only (`ls-remote`, `log`, `diff`, `rev-parse`, `rev-list`, `show`, `cat-file`); `gh api -X GET` only, under the project `GH_CONFIG_DIR`; no fetch, clone, worktree, checkout or merge-tree; no HTTP to any hosted host; no Jira; no `decision_queue.sh`; did not read `briefs_staged/`; no Artifact, Docs, mail, chat or publish tool; no person's name or decision-card id minted. Hook outcomes: two `cd` refusals and one `=======` separator refusal on the first calls, one zsh `$H:path` modifier error (re-run with `${H}:`); none wrote anything.
