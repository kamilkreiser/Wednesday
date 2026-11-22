STARTABLE: YES

# B1940 DRAFTER REPORT: kit `2026-11-23_B1940_SEAT-X39_oxpd2-f1-round2.md` (lane F1, round 2 of 2, seat Datasec/OXPd2-X39)

Drafted 2026-11-23 01:19 to about 01:55 AEDT by a read-only Opus drafter for Tuesday. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s312/d1940/` (below `<d>`). `stamp_check.py <kit>`: 174 claims, 174 measured, rc 0 (sidecar `.measured` beside the kit, write clock in its first line, kit size in its last).

## BLUF
- The round is built and measured: ONE fast-forward commit on top of `c15e13f5` changing three files (`CloudDeviceTokenHolder.cs` +23 -6, its `README.md` +16 -9, `CloudDeviceTokenHolderTests.cs` +41 -1); SignIn untouched (parts a to c hold, four files byte for byte HEAD1).
- FOUND 1: `DisposeLate(entry, call)` takes `entry.Sync` and skips the dispose when the late answer `ReferenceEquals` `entry.Held`. Cell T14 (the gate's G1 shape) red at `c15e13f5` (`T14: the late answer's clean-up disposed the held token`), green after, red under `mLateDisposesHeld` only.
- FOUND 2: `answer.IsDisposed` re-checked in `Finish` under `entry.Sync`. No deterministic cell (as the gate foresaw). Control = the surviving mutant `mNoDisposedRecheck` (348 / 0) plus the drafter's G4-shape race probe, 3000 runs a run: fix 0, 0, 0 all-zero; head 8; mutant 11, 16.
- FOUND 3: NAMED in the Limits line (with a late-answer variant the gate did not list, H4); no refusal built. FOUND 4: "does not check".
- The retracted README sentence is rewritten LAST from the code at the new head, each clause with its `file:line` (BLUF 4 of the kit).
- A FOUND-1 variant the gate did not list was found and closed by the same line: two issuer calls in progress for one registration, the second's answer X held, then the first's late answer is X (probe C: head X disposed / served all-zero; fix kept / served bytes).

## FACTS RE-MEASURED (instrument named; all MEASURED by the drafter, macOS arm64)
- Origin (`gh api -X GET`, project GH_CONFIG_DIR, 01:41): branch `b1935/...` = `c15e13f5`; `main` = `39f57d6a` (pull request 26, lane F2, MOVED since the commission's read of `c480a0c8`); `compare c15e13f5...main` diverged ahead 1 behind 1, base `c480a0c8`; `matching-refs/heads/b1940` 0; no open pull request; `.private` / `.permissions.push` `true true`.
- `main` 39f57d6a touched 7 paths, 0 in the four owned folders (`owned_count.py`, control 7). `hosted2.py 39f57d6a --total 1664 ...`: `HOSTED 39f57d6a...: PASS`.
- THE TOOLS: the seven reused programs sha256 equal to kit B1935's table; `mutants_f1r2.py` new (seven mutants; `--list` seven rows).
- Runs: HEAD1 UP 347/0; red (fresh clone2, cells only) 348/1 T14; green UP 348/0, SignIn 62/0; mutants: mAuditOneTry 62/1 B08, mEmptyTaken 62/4, mSameObjectHeld/Disposed/Accepted 348/1 T13, mLateDisposesHeld 348/1 T14, mNoDisposedRecheck 348/0; rebuild after every undo (each 0/0); loop UP 10 of 10; whole solution on clone2 `total: 1669` / 1665 / 4 / failed 0; merge shape (main 39f57d6a + round 1 + both patches, clone3) `total: 1671` / 1667 / 4; `RULES: clean (530 files)`; `Ran 111 tests`; `SURFACE: equal (3 folders)` vs HEAD1 and BASE1 (control 3 of 3); `WORDS: clean (2 files)` over 80 added lines + message (control 13 of 13); gitleaks control rc 1, seven texts rc 0; ASCII 0 (control 1); second `apply --check` refused.
- T14's timing form was MEASURED before it was chosen (probe A at head): completing the late answer on the test thread was not yet cleaned up in 1 of 1000 and 1 of 3000 runs and read GREEN once in 6000; inside `Task.Run` without a wait 19999 of 20000; inside `Task.Run` plus the wait on `Issued.Count == 2` (the cell's form) 20000 of 20000 red, on the fix 0 of 20000.

## D-DECISIONS (all Tuesday's defaults as coordinator, in the kit)
D1 late clean-up skips the held object under the lock (Q1). D2 re-check in `Finish` (Q3). D3 FOUND 3 NAMED; the drafter does NOT think a refusal small and safe (cross-entry lock order or an unlocked read, plus a new identity rule), so no state table or model run is offered (Q2). D4 "does not check". D5 one cell T14 (Task.Run + wait form, Q4). D6 one fast-forward commit, no rebase.

## Q-QUESTIONS FOR TUESDAY (each with a default; Q1 to Q3 STOP-CLASS, S4 in words)
- Q1 default a (skip the held object in the late clean-up, under `entry.Sync`); b name it only; c never dispose late answers (T06/T11 would go red).
- Q2 default a NAME (two registrations + its late variant); b refuse (not built, not modelled); c holder-owned byte copies (closes H3/H4/H5/H12, changes the issuer ownership rule).
- Q3 default a re-check with a named survivor and the race probe as control; b a test seam in the holder for a deterministic cell (a product change; not built).
- Q4 T14's form (default Task.Run + wait). Q5 Opus. Q6 120/90 min, pane X39, G1 round 2 of 2.
- For the stamp: S2 must note `main` = `39f57d6a` (moved; disjoint); the branch's hosted totals are unaffected (`--total 1669 --rules 530 --skipped-windows 21`).

## CHAIN INPUTS (rule 4; also in the kit)
Step 0 kit + stamp; 1 `<src>` (exists, 11 files), `<repo>` local values, origin; 2 the three files at HEAD1 (Step 1's clone); 3 the patches (Step 1 copy) + baseline build (Step 1); 4 green tree (Step 3), `mutants_f1r2.py` (Step 1), the seat's loop script (written in Step 4); 5 green tree after rebuilds (Step 4), lock hashes (Step 1); 6 staged tree (Step 5), message (Step 1); 7 staged tree, `run_step.py` (Step 1); 8 commit (Step 7), fetch; 9-10 commit, origin.

## UNMEASURED / NEVER RUN BY THE DRAFTER
`clone.py seat`; the commit, identity read and `run_step.py` neutral scan; `dotnet publish` and the release guard on this tree (RELAYED from round 1 STATUS: 10 and 11 files); the locked restore with `--force`; the push; `hosted2.py` on a head of this round; anything on Linux or Windows; the probes on any other machine; whether the real issuer ever answers a held or shared object (it is not in the library). The race counts are one machine's and are not rates.

## OUTSIDE-THE-FENCES DISCLOSURE
- Wrote only: the kit, its `.measured`, this report, and scratch under `<d>/` (three draft clones with push URL `invalid://no-push`; `gate/` with the tools, two patches, message and `mutants_f1r2.py`; logs; probes quarantined to `<d>/_quarantine/probe-files/`; gitleaks control to `<d>/_quarantine/gl-control-code`; the runner's released locks to `<d>/_quarantine/locks/`).
- In my own scratch clones only: `git switch`, `git apply` (and one `git apply -R` of my own fix to measure the probes at head, then re-applied), mutant edits (each undone and proved). No write to the project, its checkout, `.tools/`, Jira or GitHub; `gh` GET only; no `cd`; nothing deleted; no message to anyone; no card read.
- Heavy jobs: every dotnet job and test executable through `heavy.py` and the shared wave lock, one at a time; lock waits up to 8 (another holder, presumably seat X36); no lock broken. Load1 2.46 to 6.71.
- Read the gate's probe file `g1938/scratch/ZG1938UpProbes.cs` (shapes only; nothing copied into a patch) and round 1's STATUS in the project's `Briefs/` (read only, for tool wordings).
