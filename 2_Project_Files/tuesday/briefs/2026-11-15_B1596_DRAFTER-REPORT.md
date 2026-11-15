STARTABLE: YES

# DRAFTER REPORT B1596 (MPS LaneMA round 3, hand-off row only; MPSCALC-99), drafted 19:44 to 19:55 AEDT 2026-11-15

## BLUF
Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1596_SEAT-M144_mps-lanema-round3-handoff-fix.md` (83 lines), sidecar `.measured` beside it (59 claims, 59 measured, `stamp_check.py <kit>` rc 0). Seat `SEAT-M144` (the highest earlier `SEAT-M<n>` in the briefs folder is 141; M142 and M143 are being drafted in this wave), pane `Datasec/MPS-M144`, work number B1596, model **Opus** (D1), gate after G2 round 3, the last. One forward commit on `b1564/mps-lane-ma-source-wait-pins` (head 29b1bea25f59d1caf64dc9d92f109e571b86a46e), tests only, one file, one method. All Stamp slots and `READ-WHOLE-BY-TUESDAY: ____` are left for Tuesday.

## Design of the kit
- **Scope as a property (P5):** the only blob that differs is `tests/MpsCalc.Api.Tests/LaneMAPollAndHandOffTests.cs`, and every hunk's old side lies in lines 117 to 166 (the hand-off method), checked by a seat-written `@@` parser with a planted control. `LaneMAParkedPool.cs`, `LaneMAClause5Tests.cs`, the poll row and the product stay byte for byte. F2', F3', I1 to I3 are named closed, not reopened.
- **The fix by property (P1):** remove the `LeaveFree` pin at `:122`; nothing replaces it that takes threads away; assertions and thresholds word for word.
- **P2 slack prints (DERIVED, mine):** the row prints `slack2` (release instant minus the latest second-step give-up; about 500 ms at the 1.5 s release) and `slack3` (earliest third-step deadline minus the last third step's finish; a lower bound is allowed), with a 250 ms floor in every fix run and NO assertion on a slack. Reason: the gate's evidence is load-dependent (7 of 60 at load about 19, quiet below 10), so the kit also asks for a load-independent quantity, the slack, that can be read at any load.
- **P3 release point:** default stays 1500 ms. May move to 1250 to 1500 only on a measured larger worst-case min slack over at least 20 runs at each value, with the pacing delay listed and shown not to be what passes the row. Below 1250 forbidden: the second steps give up at about 1000 ms after hand-in, so a 1200 ms release (the gate's optional suggestion) leaves about 200 ms, below the 250 floor (DERIVED, 1250 minus 1000). I departed from the commission's "optionally release at ~1.2 s" on this arithmetic and said so in the kit.
- **Proof:** (A) the gate's own interleaved A/B, row alone, 4 CPUs, 60 strict pairs `base-tree` (29b1bea2, never edited) against the fix; the A/B counts only if `base-tree` shows at least 1 red (the control that can fail), else up to 60 more pairs once, else "did NOT discriminate" is written down; (B) full LaneMA batches on the fix, 20 at 4, 10 at 2, 10 unset, 0 red; (C) mutant m2 3 runs at each of 2, 4, unset, plus m0 and m1 once each at 4 for collateral; (D) the whole Api project once at 4 (the round-2 gate left it NOT RUN). Mutant forms are the round-2 gate's (RELAYED, built 0 warnings there).
- **Three trees:** `clone` (the fix), `base-tree` (unchanged control), `mut-tree` (mutants, made after the fix commit).
- **Main moved, plan stated:** no merge of main (template B1573 made none; Tuesday lands by head-pinned squash). The old kit's "main touching `.github/` is a STOP" is REWRITTEN as a property, because main now legitimately carries a `ci.yml` change: STOP only if main's changed paths against the branch include a `LaneMA*` test file, `OverlayResidueTests.B54.cs` or `SourceLifecycle.cs` (control: a planted `LaneMAClause5Tests.cs` line fires).
- Launch line carries `BRIEF_SEAT_LEVEL=opus` inside the quotes. HEAVY protocol, REFUSE AT ONCE, STANDING LINES, HOLDS, context band and HANDOVER form carried from B1573 with B1596 names.

## Facts re-measured with instruments (sidecar has each)
- Branch: `gh api -X GET .../git/matching-refs/heads/b1564` (19:44) -> ONE row, `29b1bea25f59d1caf64dc9d92f109e571b86a46e`. Main: `.../git/ref/heads/main` -> `56578ac6a0371d111fa196e579718f9cf41fa2bc`. (`git ls-remote` in the project clone FAILED: its `core.sshCommand` names the old `/Volumes/Laptop-DEV/...` key path, so I read origin by `gh api -X GET` as the rules allow; a fix to that config path is the project owner's, not mine; REPORTED.)
- Compare `29b1bea...main`: 17 changed paths (`.github` 1, `scripts` 3, `web` 13; `grep -c` over the printed list), 0 matching `LaneMA|OverlayResidueTests.B54|SourceLifecycle.cs`; control: a planted `LaneMAClause5Tests.cs` line prints 1. (The first read I made of this list I miscounted as 12 `web`; corrected to 13 by program before finishing.)
- Open PRs: one, `#196` (`b1578/mps-170-fleet-line-id`, head 08a62f26), 12 files, 0 of them the names above; `src/MpsCalc.Api/Quotes/*`, `Contracts/Dtos.cs` and two test files only.
- Main's tree (`git/trees/main?recursive=1`, 797 paths): `LaneMA` 0, control `LaneM5SourceLockWait` 1 (the branch is not landed).
- Pointers printed by `awk NR==n`/`grep -n` over raw files fetched at 29b1bea2: hand-off file `:16 :21 :80 :117 :118 :121 :122 :129 :130 :134-140 :141 :142 :144-150 :164 :165 :166`; `SourceLifecycle.cs` `:90` (LockPoll 25 ms), `:630`, `:665`, `:667`, `:672`, `:705`; `OverlayResidueTests.B54.cs` `:359 :377 :386`; `ci.yml` `:30 :42 :43`. NOTE: the commission and gate say the hand-off pin is at `:122` and the throw at `:150`: both confirmed; `FreeThreads` is `:21` (the gate wrote `:20` for the older head).
- Jira (GET only, scratch `jget.py`, control `MPSCALC-361` reads Done): MPSCALC-99 Backlog, 2 comments, newest id 41109, nothing newer than the round-2 kit's mark.
- Pickup and today's note read for the key: `NEXT-PICKUP-TUESDAY.md` lines 62, 72, 89, 99 list the cap card as WAITING (stale: it is now ruled; the daily note line 151 records the ruling 19:43:43 and this drafter's commission); no DROPPED or HELD line names MPSCALC-99 or LaneMA (`grep -n -i` over both files, the hits read; control: the same grep hits B1573 lines).
- Model: row C2 `model-routing.md:92`, escalation "as C1", C1 `:91` reads "Two measured failures by Sonnet on one item: Opus"; G2 `:109`; G-cap `:111` reads "A third round needs Kam's word on a card"; `models_latest.json:17` `claude-opus-5-5`; `brief_seat.sh:31` default opus. Toolchain: `.tools/dotnet-10.0.404/dotnet --version` printed `10.0.404`.
- Ports: `lsof -nP -iTCP:9990-9999 -sTCP:LISTEN | wc -l` -> 0 at 19:49:49 (control: unfiltered 18; 9980-9989 also 0). Word-boundary scan of the non-`.pre-` SEAT kits of 14 and 15 Nov: 9940, 9950, 9960, 9980 blocks are taken by B1579, B1580, B1581, B1587; 9910 by B1573; 9990-9999 is unused as a RANGE (11 kits mention four-digit 999x tokens that are not a block; I did not read each: UNMEASURED which, so Q4).
- Heavy locks: `.tools/.heavy-lock-1`, `-2` and `.git-lock` absent at 19:4x (`ls` printed "No such file"; control: `ls .tools` lists entries). Load `13.13 12.66 15.33` at 19:47.
- Panes at 19:44: `Datasec/MPS-R240`, `HPSM-POC-H168`, `HPSM-POC-H167`, coordinator panes; no `MPS-M144`.

## Chain-step input table (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit, project root | Tuesday's stamp, exists |
| 1 setup | branch head, clone, `base-tree` | origin, Step 0 |
| 2 reproduce | `base-tree` build | Step 1 |
| 3 predictions | Step 2's numbers | Step 2 |
| 4 fix | Step 2 and 3 | Step 3 |
| 5 A, B | `clone` build with the fix, `base-tree` | Step 4, Step 1 |
| 5 C | `mut-tree` made after the fix commit | the commit of Step 6 (first part) |
| 5 D | `clone` build | Step 4 |
| 6 checks, push | tables A to D, one commit | Step 5 |
| 7 STATUS | all | Steps 0 to 6 |
NOTE on order: `mut-tree` needs the fix commit and Step 5 C therefore follows the LOCAL commit; the PUSH of Step 6 waits for C. The kit says `mut-tree` is created after the fix commit exists; the commit is local, the push is last.

## D-decisions (mine)
- D1: model Opus, not the Sonnet the earlier rounds used: C2's escalation column is "as C1" and C1's reads "Two measured failures by Sonnet on one item: Opus"; this item has two Sonnet NO GO rounds. Tuesday may overrule in S4/S7 (then change `BRIEF_SEAT_LEVEL` in the launch line to `sonnet` and S7).
- D2: no merge of main; STOP rewritten as a path property (above).
- D3: release stays 1500 ms by default; below 1250 forbidden (arithmetic above).
- D4: READY target Step 0 + 180 min, fix pushed by +150 (UNMEASURED: two builds, 120 single-row runs at about 15 s, 40 batches at about 13 s, 11 mutant runs, one full suite).
- D5: a slack is printed, never asserted.

## Q-questions for Tuesday (each with a default)
- Q1: Slack floor. Default: 250 ms for `slack2` and `slack3` in every fix run (half of the 500 ms margin the failing runs lost; DERIVED, not measured).
- Q2: Load. The gate saw the fault only at load 17 to 25 and the commission says "at load 17-25", but a seat that makes no load of its own cannot choose it. Default: NO seat-made load; if `base-tree` shows 0 red in 60 (then 120) pairs the kit reports "A/B did not discriminate" and leans on the slack table and the kill. Alternative: authorise a bounded low-priority CPU burner for the A/B only (it would perturb other seats' timing gates; I did not offer it).
- Q3: Model Opus (D1). Default: Opus.
- Q4: Port block. I proposed 9990-9999 (no listener; no kit uses it as a range) but other drafters of this wave may pick the same; Tuesday settles in S7. None is bound by these tests.

## UNMEASURED
Whether pin removal alone clears the fault (the gate named it; nobody has run the fix; the kit requires the A/B); whether any row printed at the hosted runner stays quiet; how long the whole run takes; the real load on the box at the seat's run; main's `SourceLifecycle.cs` equality with the head's (not fetched: the compare lists no such path, a path-set argument, not a byte comparison); the build summary literal `0 Warning(s)` (no build run by me; `TreatWarningsAsErrors true` is read at `Directory.Build.props:6`).

## Outside the fences
None that wrote. Read: the commission file, DRAFTER_RULES, the B1573 kit, report and VERDICT, the round-2 builder's STATUS (grep of its hand-off lines), the pickup and today's note (grep), `model-routing.md`, `models_latest.json`, `brief_seat.sh`, `stamp_check.py` header, the briefs folder listing, raw project files by `gh api -X GET` into my scratch, `lsof`, `tmux list-panes`, `ls` of the project `.tools`, `git ls-remote` (failed on the stale key path, no write), `git config --get` on the root records repo (count only, address not copied), and ONE file of another drafter's scratch (`d1593/jget.py`, copied with `sed` into `d1596/jget.py`, GET-only, credentials read in-process, never printed). Hook events: two advisory grep notices; one refusal at the start (an unquoted `=====` in an echo); no effect. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s279/d1596/` (`head/` raw files, `fill.py`, `jget.py`, `MPSCALC-99.txt`, `MPSCALC-361.txt`, `compare_main.txt`, `main_tree.txt`, `pr196_files.txt`). The harness noted the kit file changed on disk after my own scripted edits (two small pointer and count corrections); I re-ran `stamp_check.py` on the final file: rc 0.

DRAFTED B1596: kit 83 lines, sidecar rc 0, questions 4
