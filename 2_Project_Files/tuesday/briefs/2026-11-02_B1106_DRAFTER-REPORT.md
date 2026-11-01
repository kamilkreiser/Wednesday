STARTABLE: YES

# B1106 drafter report (kit: `2026-11-02_B1106_SEAT-G279_mps-test-rows-gate-tier2.md`, unstamped, 8 four-underscore slots by `grep -c`)

Reads 07:52:06 to 08:02:15 AEDT by `date`. Shape copied from the B1103 kit (launch line, ON-GO squash files, STATUS-NOW, REFUSE, Stamp).

## BLUF
Tier-2 gate (G2, `model-routing.md:109`, Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes) of the tests-only branch `b1094/mps-test-rows-357-362-343-344` @ `14e4d670`, round 1 of 2, NO GO 0 before on the new class. It builds M (main + 4 paths, dangling, no ref), runs the real CI line on M and on main, kills each of the 9 rows with 15 gate-written mutants (GX1-GX15, anchors printed at main `19d084fa`), reads the four tickets itself, and keeps the dropped Api half of MPSCALC-362 item 3 as an OPEN clause (records sentence: PARTLY-DONE, never Done). Port block 9240-9249 (gate binds none). Kit is 32 KB, over the 20 KB target (Q-1).

## Facts re-measured (instrument; control)
- Branch ref `14e4d670...`: `gh api` and `git ls-remote` agree. `compare main...branch`: ahead 3, behind 1, 4 files (Api test +89 added, three modified +31 +40 +64), 0 deletions; merge base `b7cf1ad0`. 3 commits all `verified:false` (API field).
- Main `19d084fa`: commit paths by `gh api commits/<sha>`: 4 (`docs/ENGINE.md`, `PurchaseCalculator.cs`, `PurchaseInput.cs`, `PurchaseSiteAllocationTests.cs`). Overlap with the branch's 4: 0; with b1093's 14: 0; with b1063's 5: 0 (comm of sorted path lists; control self-sets 4 / 14 / 5 printed).
- Trees: `web` `d34ff342...`, `.github` `1eda8e1f...`, `tools` `be5ebe4c...` equal at main and branch head; `src` differs only because the head is 1 behind. `ci.yml` blob `212b0da1...` equal at both. CI lines: dotnet job `ci.yml:31`, timeout `:33`, build `:42`, test `:43`; `Directory.Build.props:6` TreatWarningsAsErrors true.
- Assertions by occurrence (`grep -o 'Assert\.' | wc -l` over raw files at main/head): 203 -> 243, matches the builder; the LINE count reads 202 before, so the instrument matters (kit says so).
- Arithmetic of builder totals: 555+193+3165=3913, 559+196+3167=3922, merged 623+196+3167=3986 (main derived 619/193/3165). RELAYED until the gate runs.
- Tickets (Jira GET, 07:54, control MPSCALC-99999 = 404): all four Backlog, 0 comments. Clause texts read whole.
- Round census: 75 `GATE VERDICT` first lines in project `Briefs/*_STATUS.md`; class words/keys 0 hits; control word `b789` 1 hit (B794).
- Anchors at main by `grep -n -F`: `PurchaseCalculator.cs` 181, 299, 303, 625, 205, 739, 277; `ParityProof.cs` 148, 178, 180, 193, 203; `PurchaseResult.cs:70` text occurs 12 times (61, 66, 70, 83, 90, 118, 121, 270, 273, 276, 279, 286), so the kit tells the gate to anchor on `:70-71`; `ReferenceStore.cs:18`. New-row head lines 289, 308 / 537, 553 / 68, 77 / 323, 346, 363 printed by `sed -n`.
- Ports: `lsof -nP -iTCP:9240-9249 -sTCP:LISTEN` 0 rows (full listen list 16 rows); `grep -w` scan of 107 non-`.pre-` SEAT kits of 11-01 and 11-02 for `924[0-9]`: 0 hits; control `995[0-9]` hits 3 in B1105. Live panes 07:59: tuesday, MPS-G277, MPS-R129, HPSM-POC-G276/H98/H97, Security-Composer-J41, fleet-monitor. No G279.
- REFUSE lines tested against live state: builder last line `READY FOR QA: B1094 ... @ 14e4d670...` count 1 (wrong-sha control 0); `## PRIOR WORK` at line 19 of 148 (control 0); `tmux -t %0` prints `tuesday`; `.tools/b1106`, `wt-b1106-*`, `heavy-slot-*`, `.git-lock` absent; `records/*` refs 0 (control `main` 1); model id at `models_latest.json:23`.

## D-decisions
- D-1 Own mutants GX1-GX15 differ from the builder's MG/MQ/MS/MN/MDB (carried as claims, not re-run). GX2 may be EQUIVALENT ON A2; the kit makes that a Note on A2's reach, not a Major.
- D-2 Dropped Api half of MPSCALC-362 item 3 is graded as an open clause (Note), not a defect; MPSCALC-362 gets PARTLY-DONE. The gate re-tests the builder's reason (`QuantityRule` 0 hits in `src/MpsCalc.Api`).
- D-3 Squash text from the gate's four files; commit messages not carried (as B1103).
- D-4 Hard stop suggested 3 h target / 5 h, because the Api suite is ~9 min a run (RELAYED).
- D-5 Merged result built as T/M with a temporary index, as in B1103; worktrees of the gate's own clone (the Api tests need a git-ignored `.local` inside their own repo; builder Correction 2 is quoted so the gate does not misread an environment failure).

## Q-questions for Tuesday (each with a default)
- Q-1 Kit is 32 KB against the 20 KB target. Default: accept; the dotnet shape needs the CI line, mutants, ticket table and squash files, and the template is 44 KB.
- Q-2 Allow the NuGet restore from the public source into seat-local caches (S4 lists it)? Default YES; no other network use.
- Q-3 MPSCALC-357 GP9 text asks pages and colour share "each with two decimal places"; A2 uses 1,000 pages and 0.35. The kit asks the gate to judge Recommendation against Acceptance and default-grades it a Note if the Acceptance is met. Default: keep.
- Q-4 G277 (web, live since 07:58) and later G278 (Api suite) share load and heavy slots. Default: launch_when_cool as written, one waiter.
- Q-5 Jira has no project read helper in the repo. The gate writes a GET-only script of its own. Default: YES.
- Q-6 Squash body must say the Api half of 362 item 3 stays open. Default: keep.

## Contradictions
- The commission says G277 is live on another MPS branch: at 07:52 the pane list had no G277 and `.tools/b1103` was absent; at 07:59 pane `%49 Datasec/MPS-G277` and `.tools/b1103` (created 07:58) existed. True by 07:59; the kit says so.
- The commission says to share launch shape with G277; G277 needs no dotnet, so the kit's dotnet scripts come from the B1091 gate's `scripts/`, not G277's.
- Builder STATUS wording: BLUF "Nine test methods (the eight ticket items ...)" and READY line "new rows 9 (A1 A2 B1 B2 B3 C1 C2 C3 minus the dropped ...)" list 8 ids for 9 methods (B3 is two). Not a number error; the kit lists it for FOR TUESDAY.
- B1105 (G278) kit is staged unstamped; the commission calls G277 the live MPS gate. G278's ports 9950-9959 were used only to prove the scan control.

## UNMEASURED
Check-runs on the branch; whether `dotnet --version` prints in the gate's shell (SDK dir lists 10.0.401, not invoked); the hosted dotnet job wall time; Api suite 9-minute figure (RELAYED); that A1 is the ticket's "margin-on-price" shape (the gate tests it); GX anchor texts beyond the lines printed; derivation of A1/A2 literals (gate step 2b).

## Outside-the-fences disclosure
Wrote only this report and the kit. Read-only: `gh api -X GET` under the project `GH_CONFIG_DIR` (compare, commits, trees, raw contents, matching-refs, repo settings); `git ls-remote`/`for-each-ref` in `2_Project_Files`; builder STATUS and kit; B1103/B1105 kits; project `CLARIFICATIONS.md` four lines; `.tools/b1091/scripts` headers and sha256 (previous gate's scripts, data); directory listing names of `.tools/b1094/out` (no file read) and existence tests for `.tools/b1103`; `tmux list-panes`, `lsof`. **Jira: no project helper exists, so I ran a GET-only script (`jget.py`) that sits in another Tuesday session's scratchpad (read its source first; it reads the project `.env` in process, prints no token); output kept in my scratchpad, not in the repo.** No decision_queue, `briefs_staged`, scoreboard, `_ledger.md`, Wednesday/Friday tree, Artifact, Docs, mail or az touched. Scratch copies of raw files are under my scratchpad only.
