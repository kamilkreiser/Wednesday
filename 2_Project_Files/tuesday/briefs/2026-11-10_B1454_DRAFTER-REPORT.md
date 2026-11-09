STARTABLE: YES (once the stamp is done: slots S1, S2, S5-S14 and the READ-WHOLE line filled, S14 answered, and the D56 pane closed. See Q-1 to Q-3.)

# B1454 DRAFTER REPORT: SEAT-D57, HPSM-POC UAT deploy of 884fd72b (Demo Walkthrough, PR #297), a delta on fa401da9

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1454_SEAT-D57_hpsmpoc-uat-deploy-walkthrough.md`. At 04:54:04 AEDT it was 134 lines with sha256 `6cef5508bc9e83a811a577d65638333bf4ba9c880d2b6921c9baffca30e1878e`. One line was edited after that digest (the D-8 python note), so Tuesday re-prints the digest at the stamp. The drafter counted 13 lines holding four underscores: S1, S2, S5 to S14, and the last line. Lines with five or more underscores: 0. The last line is `READ-WHOLE-BY-TUESDAY: ____`.

## BLUF
- The kit deploys `TARGET` = `884fd72b238ec8dc0d566b0e9c18b5362f920a2b` on top of `PREV` = `fa401da9`, which B1391 deployed at 04:26:57-04:29:07 AEDT and whose STATUS ends `DEPLOYED B1391`. The range is 1 commit (#297) and 16 paths, all under `web/`. There are 0 `api/`, `infra/`, `scripts/` and `.github/` paths. CI is green on every job, CodeQL is green, and 0 alerts are open.
- **Expect one D-8 STOP unless S14 settles it first.** `web/src/lib/walkthrough.ts:146` adds the customer-facing fill-in words "the sample customer". The file is part of the walkthrough, but its path is not in the closed list of files Tuesday named (`content/walkthrough/**`, `components/walkthrough/**`, and the entry text in SignInScreen, UatStartScreen and AppShell). The kit adds slot S14, which takes `LIB FILL-IN IN` or `LIB FILL-IN OUT`.
- **The D56 pane is still open.** `tmux` at 04:47:30 listed `%12 Datasec/HPSM-POC-D56`, even though its STATUS ends DEPLOYED. The kit's pane REFUSE fires on any other `HPSM-POC-D*` pane, so Tuesday must close it before the launch (slot S10 (e)).
- The plant control is the reverse of B1391's: after the deploy the start page shows the option, count 1. The walkthrough is read-only for the seat: per walk, one `POST /api/auth/uat`, then 14 steps with 0 non-GET requests, then one sign-out. There are two walks (1280 and 390), and the second one is the restart.
- B1391 restamp 4b (no load gate on the local pair) is part of the kit from the start. The seat copies the way back, the identity pass, presig, live, walk and the other tools from `.tools/b1391/` by name into `.tools/b1454/` and edits each by hand.

## Facts re-measured with instruments (all read-only; `gh api -X GET` under the project GH_CONFIG_DIR; clocks from `date`, 04:45:49-04:54:04 AEDT)
- `branches/main` = `884fd72b...` (04:46:08). `commits/884fd72b`: one parent `fa401da9...`, subject "Web: Demo Walkthrough option and right-hand guided demo panel".
- `compare fa401da9...884fd72b`: ahead 1, behind 0, 1 commit, 16 files (+1618/-15), 0 files outside `web/`. 7 are product paths and 9 are test paths.
- `pulls/297`: merged true. `merge_commit_sha` = TARGET. Head `e9a36f7ec658d13e453b8fea98d0ad5825719389`, 2 commits, 16 changed files, merged at 16:54:05Z. The check-runs on the head are 23 of 23 success.
- CI push run `42659375588` completed/success. Every job passed (both SQL Server legs and 8 e2e shards included) except `dependency review`, which was skipped. CodeQL `Push on main` run `42659374837` succeeded. Open alerts: 0 (control: `fixed` reads 1). The deploy artifacts for 884fd72b and fa401da9 both read `expired=false` and expire on 2026-11-16.
- Tree proof (python3 over recursive trees): PR paths `2075486b..e9a36f7` = the 16 range paths. The TARGET blob equals the head blob for 16 of 16. Paths differing outside that set: 0 (a planted path reads 1). Schema regex hits: 0.
- `deploy-from-ci.sh` at TARGET is 109 lines: `:49` holds the predicate and `:68` / `:69` the two deploy lines. B1390-1 is at `steps.ts:130` at TARGET (`grep -n -i 'laptop sample'`). The fill-in is at `lib/walkthrough.ts:146`.
- `steps.ts` holds 0 targets under `/admin` or `/feedback`. Its single `admin|feedback` hit is a comment at `:200` (control: `home` 6). In `WalkthroughPanel.tsx`, `steps.ts` and `lib/walkthrough.ts`, the patterns `fetch(`, `<form`, `method=` and `type="submit"` all read 0 (control: `method="post"` in UatStartScreen.tsx reads 2).
- Ports 9970-9979: `lsof` shows 0 listeners (control: 14 across all ports). The kit scan covered 54 SEAT kits from 11-09 and 11-10 and hit 1: B1450 `:23` reserves 9970-9979 "to B1391 (D56)" (control: `994x` hits 4 kits). G375 uses 9680-9689 and G376 uses 9690-9699.
- Panes at 04:47:30: `%0 tuesday`, `%1 fleet-monitor`, then H147, D56, H142-H146, H153, R197, G374, G376 and G375. The G375 and G376 kits both say at `:12` that they touch no hosted host.
- `launch_when_cool.sh` and `brief_seat.sh` exist. model-routing `:96` is C6 Deploy with Opus "1st", and `:145` says Sonnet has no deploy rows. `models_latest.json` gives `levels.opus.model_id` = `claude-opus-5-5`.
- Name scan of the kit, underscore-aware, done in python: 0 for each name tried (control `x_by_steve_` reads 1). No decision-card id appears in the kit.
- `.tools/b1454` is absent. No file named B1454 or D57 exists in either briefs folder (control: `SEAT-D56` counts 5).

## D-decisions (in the kit; summary)
- D-1: pin TARGET. D-3: both packages; the API restarts with stamp-only code. D-7: the way back is to fa401da9, using packages copied from `.tools/b1391/target/` and proven by digest, with a CI re-fetch as the fallback.
- D-8: the closed list is defined by file, as instructed. The seat lists every new string with its `file:line`. B1390-1 is carried as is and named in the report. S14 decides the lib fill-in string.
- D-11 and D-13: the walkthrough is read-only, with one sign-in POST per walk and 0 mutating requests in the 14 steps. The panel must be absent on plain sign-ins. The sample customer must match the plain-Partner BEFORE pick, which is checked with GETs only.
- D-12: the readiness pages B1391 deployed must be unchanged.
- BUILD 4: the API package must be stamp-only on all 5 DLLs. Any code difference means an unlisted `api/` change, which is a STOP.

## Q-questions for Tuesday (each with a default)
- **Q-1. S14, the fill-in words "the sample customer" (`lib/walkthrough.ts:146`).** Default: `LIB FILL-IN IN`. The words are the walkthrough's own step text, used when no sample customer exists, and gate B1390 read `lib/walkthrough.ts` (Step 2). If you write OUT, the seat STOPs at D-8 before any hosted write.
- **Q-2. Close the D56 pane (`%12`) before the launch.** Default: close it. If it stays open, the pane REFUSE fires at Step 0.
- **Q-3. The launch waiter's load gate.** `launch_when_cool.sh` waits for load1 < 7 (`LOAD_MAX`), but load1 was 37.01 at 04:49:16 with about 11 builder and gate panes running, so the waiter may give up after 3600 s with rc 4 and launch nothing. Default: Tuesday launches the way it launched B1391 tonight. If a `LOAD_MAX` override is used, it goes outside the quoted command and is recorded in S2. The kit itself sets no hosted-step load gate.
- **Q-4. S6 content.** Default: `#297 only: head e9a36f7 (gated head 60639d1 + B1398 CI-fix e9a36f7, 3 paths), squash 884fd72b; B1390 GO WITH FINDINGS r2 of 2; carried: B1390-1 Minor (step 10 caveat, fix under gate G376), B1390-2..7 Notes`.
- **Q-5. S5.** Default: `42659375588`, which the drafter read as completed/success.
- **Q-6. The B1398 3-path claim.** The kit has the seat prove with `compare 60639d15...e9a36f7e` that it is 1 commit and 3 paths. The drafter did not run that compare (RELAYED from B1398 FINAL). Default: the seat measures it, and any other shape is a STOP.
- **Q-7. S10 (d), HP review session.** The drafter cannot know whether one is under way. Default: Tuesday states it.

## UNMEASURED (by the drafter)
- Every hosted fact: whether UAT still runs fa401da9, the settings, activity, database and deployment ids. All of it is RELAYED from B1391 STATUS W3 and AFTER. No `az` and no HTTP were used.
- The `60639d1..e9a36f7` shape, and whether `.tools/b1391/target/` is still byte-equal to the recorded digests. The seat measures both.
- Which customer `pickSample` picks on the real UAT API (B1390 left this open). The seat measures it first on the local pair against the real local API, then on UAT.
- Whether a person-name list exists under `.tools/b1390/`. If none is found, the kit tells the seat to mark the name scan UNMEASURED.
- The full set of new strings in `steps.ts` and `WalkthroughPanel.tsx`. The drafter sampled them; the seat extracts every one by program.

## Outside-the-fences disclosure
- No `az`, ssh or docker. No HTTP to any hosted host. No git write verb. `gh` was used with `-X GET` only, under the project GH_CONFIG_DIR. No `cd`, and `decision_queue.sh` was never run.
- The ledger was not read, and no grep went into `0_Brain/learnings/`.
- Local reads only: the drafter rules, the B1391 kit and STATUS, B1390 (first line, findings, Steps 1-8), B1398 whole, the headers of the B1450/B1451/B1452 kits, `.tools/` listings, `lsof`, `tmux list-panes`, `sysctl vm.loadavg`, the `launch_when_cool.sh` header, model-routing lines and `models_latest.json`.
- Scratch files (JSON trees, raw sources at TARGET) were written only to the session scratchpad. Two files were written in briefs: this report and the kit.
- One command failed harmlessly: `/usr/bin/grep -P` is not available on macOS. The name scan was re-run in python, and the kit now says so.
