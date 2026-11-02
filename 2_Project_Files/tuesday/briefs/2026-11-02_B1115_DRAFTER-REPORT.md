STARTABLE: YES
# B1115 DRAFTER REPORT (kit `2026-11-02_B1115_SEAT-M74_mps-269-fix-round.md`, unstamped; reads 10:58:59 to 11:02 AEDT by `date`; routing row C8)

## BLUF
Builder fix round, seat M74, pane `Datasec/MPS-M74`, ports 9260-9269, on `b1093/mps-269-server-template-store` @ `717da6f8e6b1074c74e30a499215e92593852e2e`. Two new commits (A fixes+contract+docs, B re-sync), one fast-forward push to the same branch, no PR. Sonnet row C2 (`model-routing.md:92`); next gate G1 tier 1 Opus, ROUND 2 OF 2, NO GO 1 before; the kit tells the seat plainly it is the last round. Your four decisions are in the kit as the coordinator's, not the product owner's. Size 20,465 bytes (20.0 KiB; 20,000 decimal is 465 over: say if you want it cut further, the next cuts are plants 7-8 and the pointer list). Stamp slots: 8 lines with four underscores (7 slot lines plus the last line).

## Facts re-measured (instrument, control)
- Main `19d084fa8018094bf7ea9360433d0d87f8720e45` by `gh api -X GET git/ref/heads/main` 10:59:14 (project GH_CONFIG_DIR). Branch head `717da6f8...` by `matching-refs/heads/b1093` 10:59:15, equal to the gate's pin; control `matching-refs/heads/b1115` length 0.
- Main moved from the branch base `b7cf1ad0` by one commit (`compare` b7cf1ad0...19d084fa): 4 paths (ENGINE.md, PurchaseCalculator.cs, PurchaseInput.cs, PurchaseSiteAllocationTests.cs). Lane pattern hits 0; control (`docs/api/openapi.json`) 1. So the move does not touch the lane. Branch vs main: ahead 2, behind 1. The gate built the merged tree (619/193/3239).
- Open PRs 121, 120 (`pulls?state=open`).
- Ports: `lsof -nP -iTCP:9260-9269 -sTCP:LISTEN` 0 rows; control a `python3 -I -B` listener on 9269 printed 2 lines, then 0; all listeners 13. Word-bounded scan `grep -l -w -E '926[0-9]'` over the 256 non-`.pre-` files of `tuesday/briefs/` dated 11-01 and 11-02: 0 (control `927[0-9]`: 5; the whole 9000-9999 tens-block census showed 9260 free). Seat name: `-w M74` over the 116 SEAT kits 0 (control `M71` 15). B1115 files 0 before writing.
- Panes at 10:59 (`tmux list-panes -a`): tuesday, Security-Composer-G281, HPSM-POC-G282, HPSM-POC-G280, MPS-G279, MPS-G278, MPS-G277, fleet-monitor. `Datasec/MPS-M74` absent.
- All `file:line` pointers in the kit were printed by `grep -n`/`awk NR==n` over raw files fetched at `717da6f8` into scratch (TemplateStore 406/420/424/355/187/433, TemplateRules 16-17, TemplateEndpoints 135/229, TemplateIsolationTests 14/42-54/57-67, API.md 844/847/857-862/319-320, Program 70/88-90/112, QuoteFileStore 309/326, Overlay 425/758, openapi 470/501/534/549, tests 149/189/370). `CLARIFICATIONS.md:688` and `:1712` by `awk NR==n` on the project copy.
- Model ids: `models_latest.json:38` sonnet `claude-sonnet-5-5`; `model-routing.md` lines 92 (C2), 98 (C8), 108 (G1), 111 (G-cap) printed by `awk NR==n`.
- Existing state the seat must not touch: `.tools/b1093/`, `.tools/wt-b1093-fix` and `wt-b1093-mut` exist (M72's; fix worktree reads head `717da6f8`, 0 porcelain). The kit tells M74 to use `b1115` names. Repo git dir is `2_Project_Files/.git` (objects for `717da6f` are local; `19d084fa` needs one fetch, which the kit permits).

## D-decisions (defaults apply if silent)
- D-1 Seat M74, B1115, Sonnet, G1 on Opus, ports 9260-9269, launch line with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- D-2 Two commits (A, B) on top of the pin, one fast-forward push to the same branch. The old kit said "never push twice"; this is a second push to the branch overall but the seat's only one. Kit says so and STOPs on any non-fast-forward.
- D-3 Your decision 2 followed; B1105-8, -9, -10, -12 and the rest of -11 are LEFT (the status table lists them). B1105-11 rows only for name cases with B1105-4.
- D-4 B1105-5 test: the invalid act-as row also pins `Acting_as_a_role...` (`TemplateApiTests.cs:370`, accepts 400 or 403) to the status the build answers. This is a touch on an existing template test, inside Yours (`Template*.cs`); not a loosening.
- D-5 B1105-7 adds a new W1 log sentence and a `Program.cs` log call beside `:88-90` (Program.cs is already in Yours). B1105-2 and -4 reuse existing sentences; the changed ones are docs (W2) and the two contract wording lines.
- D-6 Clock: target READY 2 h, hard stop 3.5 h after Step 0 (drafter's suggestion).
- D-7 Plants 8, listed; properties checks limited to scope, no word, gitleaks as you asked.

## Q-questions for Tuesday (each with a default)
- Q-1 Heavy slot: `heavy-slot-1` has a holder file `B1105 10:59:27 step6` at 11:00:56 although the B1105 STATUS says it holds no slot and its last line is a VERDICT. Default: the seat takes `-2` or `-3`; if you know G278 is still running a step, hold the launch until it ends.
- Q-2 Size: 20,465 bytes against your 20 KB. Default accept; if you want under 20,000, delete plants 7-8 (and their line in "order of loss").
- Q-3 `:688` says "before it ships" and "nothing is deployed without his card"; your decision 4 says "before any deploy, not before a merge". The kit quotes the line and says Tuesday reads it that way, citing `:1712` for merge. Default as written; you decide if the wording should stay.
- Q-4 B1105-1 ruling: the kit's wording of the one docs sentence is left to the seat within your frame (trusts the file, does not detect a well-formed hand edit). Default accept.
- Q-5 Port block 9260-9269: default accept.
- Q-6 Launch window / stamp lines: left as slots for you.

## Contradictions found
- Heavy-slot holder vs the B1105 STATUS (Q-1).
- The B1105 STATUS FOR TUESDAY says B1105-5's fix is "three contract rows, re-sync"; the commit-plus-sync form (A then B) is carried as written. The gate's own findings list says `EntraAuthTests` 3 hunks, nothing weakened; the kit keeps that file in HOLDS.
- B1105 states `wt-b1105-base` was at `19d084fa`, not the kit's `b7cf1ad0` (its Corrections); the branch's merge base remains `b7cf1ad0`, so "behind 1" is real and the kit says no rebase.
- B1093 kit carried "exactly two commits, push once"; this round adds two more commits and a second push to that branch. The kit says so in its title and COMMITS section.

## UNMEASURED
No build, test, plant or sync run. Not measured: whether a test can create a mode-000 lock file on the seat's file system; whether `WellFormed` calls `NameOk` for stored names (the source line reads so); the 400 row text to reuse for B1105-5; how many new sentences the fixes add; whether the gate (G278) is still running anything; the Jira ticket state today (I did not GET Jira, as the kit makes the seat do it at PRIOR WORK).

## Outside-the-fences disclosure
Read-only reads only. No Jira, no card store, no `decision_queue.sh`. Scratch files (kit list, raw files at the pin) under the session scratchpad. One earlier Bash call was refused by the no-cd hook (my own `cd`); re-issued without it. Read B1105 STATUS through a persisted tool-result file of the project's Briefs copy, not elsewhere. Two Bash calls read `.tools` directory listings of the project (names only, including a large `wt-*` list) and the `heavy-slot-1/holder` file.
