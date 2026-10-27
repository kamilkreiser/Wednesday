STARTABLE: YES (after Tuesday stamps the seven slots; load1 2.57 at 20:22, all three heavy slots free, no MPS pane live)

# B848 drafter report: gate kit for PR #131 (MPS MPSCALC-356 submit-test hold), seat G183, tier 2

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B848_SEAT-G183_mps-131-feedback-submit-hold-gate-tier2.md` (73 lines; four-underscore line count 8, `@X@` count 0, non-ASCII 0). No `.pre-stamp` copy was written (the brief limits me to two files); Tuesday can `cp` before stamping. Drafted 20:22 to about 20:40 AEDT.

## BLUF
- Gates PR #131 head `aa8933ab...` on main `44137f7a...`, Sonnet, G2 (`model-routing.md:109`, G-cap `:111`), round 1 of 2, ports **7730-7739**, pane `Datasec/MPS-G183`, `BRIEF_SEAT_LEVEL=sonnet`. G183 and B848 unused (word-boundary scan of 318 non-`.pre-` 26/27 Oct files: 0 hits; control `G182` fires 5).
- PR #131 re-read at 20:22: open, not draft, 1 commit, +6 -1, one path, `blocked` (checks pending). Check-runs: `CodeQL` neutral, `Analyze (actions)` success, csharp/python/js-ts/dotnet/web/python jobs in progress. A zero alert read now would be NOT a pass; Check 8 waits.
- **The gate's own mutants:** L1 fixed 1000 ms delay, L2 bounded wait-for-created (own bound), L3 short 50 ms delay (all at `FeedbackEndpoints.cs:229-230`, differing from the builder's 750 ms / ~2 s); Pass A (OLD red at the pending assertion) and Pass B (NEW green), 3 runs each; retained assertion by SM1 (`StateOf` forcing `Created`) and SM2 (a reply-only edit at line 230); plants cw-weak A and B, P1 key `n == 2`, P2 key never occurring, P3 `n > 0`, P4 hold removed with seams kept, P5 release removed, T2, P6 background-task release race (20 runs); teardown with a held create plus a hang control.
- **T2 grading plan:** four steps: (i) read `Contract.Check` (`Contract.cs:84`, `JsonDocument.Parse(body).RootElement.Clone()`, which I confirmed by GET: the reply is a cloned snapshot before `Submit` returns) and the statements between `Submit` and the assertion; (ii) run T2 under L1/L2 3x each; (iii) controls that can see release position: cw-weak A (release before Submit, must be red) and the P6 racy release; (iv) rule: T2 green plus snapshot = **equivalent variant, Note** (the builder is right; its prediction and the builder kit's were wrong); Minor only for an observable release position the row misses; Major only if a pre-read release is green while cw-weak A is red.
- cw-weak B (old 400 ms timeout) is measured by the gate and graded "timeout line is load-bearing" (Note) if red at the wait under a late reply, as the builder says.

## Re-measured facts (instrument)
- PR #131 object, body, commit message, diff (`gh api -X GET`, 20:22); main `44137f7a` by `git/ref/heads/main`; open PRs #131, #121, #120 (#120/#121 each `web/package-lock.json`).
- `Contract.cs:84` `.Clone()` read by GET at the head (a case-sensitive grep ran first; the line printed, so not a false zero).
- Jira MPSCALC-356 read in process from the project `.env`: Backlog, labels lane-h / mpscalc-b840 / plan-b840-b840-1 / tier-2, 0 comments, control query 0.
- `CLARIFICATIONS.md` `landing rule` hits at 744, 774, 809, 829, 854 (`/usr/bin/grep -n -i -F`); 809 and 854 are the lines the builder kit cites.
- `lsof` for 7720-7729 and 7730-7739: rc 1 (nothing). Panes at 20:22: tuesday, Security-Composer-J28, NexusAI-R72, fleet-monitor. `.tools` heavy-slot listing empty. Load averages 2.57 2.52 2.92.
- Port scan: blocks 9700-9959 each had a hit in the kits of 26/27 Oct, so I went to the 7xxx run; 7730 had 0 hits in 318 files (controls `953x` 9 files, `770x` 5 files).

## D-decisions (mine, Tuesday overrides at the stamp)
- D1 The gate runs three late-reply mutants (L1, L2, L3) with its own spellings, not the builder's R1a/R1b.
- D2 SM2 (a reply-only edit) is added to the builder's SM1 so the retained-assertion proof does not depend on the shared `StateOf`.
- D3 A deliberate load cell (4 busy loops, at most 2 minutes, own pids, only while no other seat holds a slot) because the PR's risk is timing; Q-3.
- D4 The row's `TimeSpan.FromMinutes(5)` is flagged as a Note: the builder kit line 58 said "no time figure in the file" but the added line copies the retry test's own line; the gate grades it, not a defect.
- D5 Hard stop target 2 h verdict, 3.5 h hard stop after Step 0 (suggested; slots S5).

## Q-questions for Tuesday (each with a default)
- Q-1 Round count: default accept round 1 of 2 on PR #131 (builder kit line 31; B829 and B830 read GO WITH FINDINGS with NO GO 0 before).
- Q-2 T2 grading rule as written (equivalent variant = Note; Minor/Major only on a missed observable release position). Default: accept; the alternative is to ask the builder to reword the release comment (cosmetic).
- Q-3 Load cell with busy loops. Default: yes, only while no other seat holds a heavy slot; cut first if the load line is crowded.
- Q-4 CodeQL wait 60 s polls, 40-minute cap, GO WITH FINDINGS with "CodeQL PENDING" if still running.
- Q-5 Post-merge `localdomain` count check: Tuesday's act, listed in FOR TUESDAY (the gate reads #130's squash as a control).

## UNMEASURED (by me)
No build, test, mutant or C# compile ran. Not measured: that L1/L2/L3 build at 0 warnings and reach line 116; the 20-run cell; T2 and P6 at runtime; cw-weak A/B; SM2 compiles; teardown durations; Api and Engine/Import counts (RELAYED from the builder 3162/435/193); `refs/pull/131/merge` tree; whether b820/b821 are still live; the hosted run beyond 20:22; the push-run failure's run id 40458121077 (RELAYED from the ticket); my own bind control on 7730 (the gate does its own).

## Outside-the-fences disclosure
Read-only throughout: `gh api -X GET` under the project `GH_CONFIG_DIR`, one in-process Jira GET (token never printed), `lsof`, `tmux list-panes`, `uptime`, scratch python scripts in the session scratchpad (`scan.py`, `jira.py`) for the kit scan and the Jira read. No git write verb, no hosted-host HTTP, no card tool, no write except the two named files. A hook advisory about a case-sensitive grep fired once; the grep matched, so no false zero.

First line of STATUS the gate writes: `GATE VERDICT B848: PR #131 b843/mps-356-feedback-submit-test-hold <GO|GO WITH FINDINGS|NO GO> @ aa8933a (round 1 of 2 ...)` (the full form is in the kit).
