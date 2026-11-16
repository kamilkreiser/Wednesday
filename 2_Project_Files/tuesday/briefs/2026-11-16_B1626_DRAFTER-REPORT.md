STARTABLE: YES (after the stamp; 6 questions below, each with a default the kit already assumes)

# B1626 drafter report: MPS Commercial Calculator, lane M-T, test stability under load (seat M149)

Drafted 2026-11-16 from 16:29 to 16:41 AEDT (`date` printed 16:29:24, 16:29:31, 16:29:39, 16:30:51, 16:31:36, 16:32:12, 16:32:32, 16:33:46, 16:34:05, 16:34:51, 16:35:02, 16:39:29, 16:39:51, 16:39:56 and the closing 16:41:05). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1626_SEAT-M149_mps-lane-mt-web-wait-budgets-and-overlay-group-under-load.md` (89 lines, 12 stamp slots left as `____`) with sidecar `.measured` (92 lines). `stamp_check.py <kit>` rc 0 (92 claims, 92 measured; about 40 of the rows are "INSTRUCTION to the seat" lines). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s283/b1626/` (tarballs and tree of main, plants in `plants/`, run logs, `jcount.py`, `ctx2.py`, `jdesc.py`, `fill.py`).

## BLUF
- **Lane M-T fits one Sonnet seat as two parts: A = MPSCALC-369 (web), B = MPSCALC-163 (dotnet, measurement).** Row L6 (test-only), gate G2, pane `Datasec/MPS-M149`, branch `b1626/mps-lane-mt-web-wait-budgets-and-overlay-group-under-load`. READY at Step 0 + 270 minutes (the two loops of 20 counted runs are the long part); Part A pushed by +90. Nothing deployed, no product byte.
- **The sweep's text for 369 ("more counted runs") would have repeated B1502's loop and probably failed the same way. The drafter found why.** The one failed row of the five in B1502's 19-of-20 loop was "Unable to find an element with the text: DEMO-A3C-50" at 1298 ms, not a timeout: that is the testing library's own default wait (`asyncUtilTimeout: 1000`, `@testing-library/dom/dist/config.js:15`), which the repository's 15_000 per-row budget (six rows, MPS #173) never touches. Both files hold 22 awaited query lines and 0 explicit waits. **A deterministic plant reproduces the failure on demand** (make `getQuote` wait 1500 ms in a copy of the file): PriceReason 3 of 3 red at about 1005 ms with that exact text; PurchaseBomEditor 8 of 13 red at about 1003 ms. With explicit 10_000 ms waits on the four awaits of PriceReason the plant is 3 of 3 green (giving only the first wait the option leaves row 1 red at its later `waitFor`: 2 of 3). So Part A is red-first (plant), then the change (explicit waits inside the 15_000 budget, no assertion touched), then the counted loop.
- **163 needs only its measurement** (clauses 1, 2 and 4 are MET per its own comment; the 20 group runs under load were never made). The "group" is the xUnit collection `OverlayTimingGroup` (10 classes carrying `[Collection(...)]`, 31 attributes) plus `OverlayHostedStoreTests` (19), which is the builder's own "overlay concurrency set". **The drafter could NOT run the dotnet side**: a restore from the machine cache fails at main (`NU1102`, Xml 10.0.15 absent, nearest 10.0.13) and the registry is outside a drafter's fences. The kit gives the seat the B1593 precedent (one registry restore of that single package, seat-local) as Q2; if Tuesday says no, Part B does not run and READY says so.
- Baseline at main: 146 files, 1610 tests passed, eslint rc 0, `tsc -b` rc 0 (load 14.9, 16 s). The machine was at load 12 to 20 the whole drafting window, so a counted loop (load above 7) can run immediately.

## Scope, key by key (each ticket read whole by Jira GET at 16:29)
| key | status | in slice? | reason |
|---|---|---|---|
| MPSCALC-369 | Backlog, 3 comments (newest 2026-11-11T22:24: 19 of 20 clean) | IN, Part A | the five rows' default waits; loop of 20 counted runs is its acceptance |
| MPSCALC-163 | Backlog, 3 comments (newest 2026-11-01T01:56: clause 3 unmeasured) | IN, Part B | only "20 group runs green under load"; edit only on a test-side cause |
Held and dropped check (`ctx2.py` over the pickup, the 11-15 and 11-16 notes): 369 has 4 pickup hits, 163 has 0; no window carries a hold or drop word; control key 404 prints hits with a flavour window. PRs naming 369: #173, #178; naming 163: #58 (all merged; 202 PRs, controls #72, #181). No open PR at 16:39:56.

## Facts re-measured with instruments (details in the sidecar)
- Main `efe6cdd5e156c20bb9b17c36d170f1bf0355f60a` at 16:39:56. **It moved twice while I drafted** (`72fa8d9c` -> `9c219cbb` when #201 landed 16:32:46 -> `efe6cdd5` when #202 landed 16:37:01); the second move is `docs/**` only, and all measured files are identical across the three (compare lists).
- Wait census: 18 and 4 lines naming `findBy`/`findAllBy`/`waitFor(` in the two files; `grep -c -i timeout` 0 and 0 (control `15_000`: 2 and 4); `setup.ts` does not change the default (0 hits). Rows calling the helper `open`: PriceReason `:37 :43 :49`; PurchaseBomEditor `:40 :64 :78 :185 :190` (the kit demands the 15_000 layer on each, since the helper's waits rise to 10_000).
- Overlay set by program (python over `tests/MpsCalc.Api.Tests/*.cs`): ten collection classes `LaneL2FeedbackUploadStreamTests`, `LaneL2SourceStageArrivalTests`, `LaneM5SourceLockWaitTests`, `LaneMAClause5Tests`, `LaneMAPollAndHandOffTests`, `OverlayGateB57TimingTests`, `OverlayGateB71TimingTests`, `OverlayGateFindingsTests`, `OverlayQueueTests`, `OverlayResidueTimingTests`. None uses a listener (the only file in `Overlay*`/`Lane*` that does is `OverlayGateB76Tests.B77.cs`, not in the set).
- Branch census: 225 origin branches, 25 with no PR head; 24 compared against the lane's paths; 10 differ and the newest of them is 2026-10-16 (old working branches, none live).
- B1502's counted loop table (RELAYED): 25 runs, 20 counted, failures: run 1 (a five row, load 17.21), runs 3, 19, 20 (other files: `QuoteScreenDevices.b445`, `PageEstimate.b456`, `PurchaseBomEditor.addSectionWait`).

## Chain inputs (rule 4), in execution order
| step | inputs | produced by / exists at |
|---|---|---|
| 0 | the kit, the STATUS path | exists at launch / this step |
| 1 setup + baseline | clone, identity, deploy key, node 24 to 26, machine npm cache | BASE and the machine (printed present above) |
| 2 predictions | baseline counts, plant counts of FACT 5 | step 1; the drafter's runs |
| 3 plant | the two base test files; `mkplant.py` (the seat writes it) | BASE; the seat |
| 4 change | the plant's red names, the rows that call `open(` | step 3; BASE |
| 4 mutants | the regenerated plants from the COMMITTED files | step 4 change |
| 5 loop | the pushed head, the gate script, the lock folders | step 4 push; the seat's scripts |
| 6 Part B restore | the machine cache, the seat-local `nuget.config` | the machine; the seat (Q2) |
| 6 set and group run | the built test dll, the class list by program | step 6 build |
| 6 loop | the filter, the gate script | step 6 set; step 5's scripts |
| 7 checks, 8 push | each commit's diff | steps 4 and 6 |

## D-decisions the drafter took
- **D1** Plant first, change second, loop third. The change cannot be proven red by a loop (a loop is probabilistic); the 1500 ms plant is deterministic and reproduces B1502's exact text.
- **D2** Explicit waits at 10_000 ms (inside the 15_000 row budget) on every awaited query of the helpers and the five rows; the rows that share a helper get the same 15_000 layer; a pair check proves no assertion line changed. No global `configure(...)` and no edit of `web/src/test/setup.ts` (not owned; would touch every test file).
- **D3** A loop counts only runs whose load1 read immediately before the start is above 7.0; the seat makes no load (as B1502 did); the load gate (under 24 on two reads) still applies. A fix restarts the 20 at the new head; at most two fix rounds.
- **D4** Part B edits only the six Overlay test files, and only for a test-side cause; the five `Lane*` classes run in the group but are never edited; a product limit is named (the ticket's own [B54-R2]).
- **D5** Part B starts after Part A is pushed and its loop is done or stopped, so the two heavy loops never overlap.
- **D6** The kit makes the seat report counts, never "Done": the Done reading is the coordinator's.

## QUESTIONS FOR TUESDAY (each with a default)
1. **Model row and gate:** the commission names L6 and G2; both fit (tests only). Default: L6, G2. Q1 in the S4 slot.
2. **NuGet for Part B:** the machine cache lacks Xml 10.0.15, so the seat's restore needs ONE registry restore of that single package into a seat-local folder (the B1593 precedent, `B1593_STATUS.md:68`). Default: allowed, named in STATUS. If you say no, Part B does not run and READY says so (369 still completes).
3. **The counting rule:** counted = load1 above 7.0 read right before the start; the seat makes no load; a seat's own previous run is not excluded (said in STATUS if relevant). Default: as B1502.
4. **Other load-sensitive files** B1502 saw (`QuoteScreenDevices.b445`, `PageEstimate.b456`, `PurchaseBomEditor.addSectionWait`, `QuoteScreen.addSectionWait`, `InventoryPickerMany`): not in this lane. Default: the seat names any failure there with file and row and does not edit; a follow-up lane if you want one.
5. **The five `Lane*` classes** in the same collection and the product limit [B54-R2]: a red there is named, not edited. Default: yes.
6. **Done reading:** the seat reports "N of 20 counted runs clean" for each ticket; the coordinator's records seat decides Done. Default: yes.

## UNMEASURED
Everything on the dotnet side: restore with the registry, build warnings, the filter, the list and case count of the eleven classes, the group's wall time and any red under load; the hardened PurchaseBomEditor plant (the drafter ran only the base plant and the PriceReason fix); whether 10_000 ms waits suffice at the loads the afternoon shows (the seat's loop answers); hosted CI against local node 26 versus CI node 24; CodeQL pre-scan for this repository; whether `userEvent` typing itself ever slows past the 15_000 row budget (never seen).

## Outside the fences (disclosure)
Read: the commission, SWEEP-1450 (M-T lane, section 6), DRAFTER_RULES, the B1617 kit, report, sidecar and STATUS (template), model-routing lines 85 and 109, `models_latest.json:23`, `brief_seat.sh:31`, project `CLAUDE.md:50`, B1502, B1593, B105 and B157 STATUS lines, the pickup and the 11-15 and 11-16 notes through `ctx2.py`; at main by `gh api -X GET` tarballs: the two web test files, `web/src/test/setup.ts`, `vite.config.ts`, the testing-library `config.js`, `ci.yml`, the overlay and `Lane*` test files. Jira: GET only through my own `jcount.py` and a copy of the sweep's `jdesc.py` (project `.env` in-process, token never printed). GitHub: `gh api -X GET` only (ref, pulls paginated, branches, compare, commits, tarballs). **Ran, beyond reads, under no heavy lock (none existed; load 12 to 20):** in a scratch tarball of main under `fleet/state/s283/b1626/tree/`: `npm ci --offline --ignore-scripts` (rc 0), `npx vitest run` whole twice (rc 0, 1580 then 1610 tests), `npx eslint .` and `npx tsc -b` (rc 0), four plant runs (plants kept in `plants/`, not in the tree), and one `dotnet restore --source ~/.nuget/packages` (rc 1, NU1102; wrote `dotnet_home/` and `obj/` in my tree only). No registry call by me; no dotnet build or test. One stray: a stamp_check output redirected to `/tmp/b1626_sc.txt` (a scratch note; harmless, not deleted). Wrote only: the kit, its sidecar, this report and my folder. No Jira write, no git write verb in any project repo, no push, no PR, no az, docker or ssh, no hosted HTTP beyond the GETs above, no `decision_queue.sh`, no card read, no message, no WEDNESDAY or FRIDAY tree, no `_ledger.md`, no Artifact tool. `date` is the only clock source.

DRAFTED B1626: kit 89 lines, sidecar rc 0, questions 6
