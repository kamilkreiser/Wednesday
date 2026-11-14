STARTABLE: YES (after the stamp; 6 questions below, each with a default the kit already assumes)

# B1564 drafter report: MPS Commercial Calculator, lane M-A, slice 1 (seat M135)

Drafted 2026-11-15 09:58 to about 10:20 AEDT (`date` printed 09:58:53, 10:02:34, 10:05:15, 10:09:41 and 10:10:24 in the reads). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1564_SEAT-M135_mps-lane-ma-api-stores.md` (+ `.measured`). Stamp slots left as `____`; `stamp_check.py` rc 0 (85 claims, 85 measured; 19 behaviour lines S01 to S19 beside them).

## BLUF
- **Slice 1 (one Sonnet seat, about 3 hours, tests plus one document, no product byte):** PART A MPSCALC-99 (the open clause 5 and the three held review findings, new `LaneMA*.cs` test files only, red-first by planted mutants m0, m1, m2) and PART B MPSCALC-170 (a contract NAME PROPOSAL for the stable fleet line id, a document in STATUS, no code; clock-gated like B1554: Part A pushed by Step 0 + 120 minutes or Part B does not start).
- **Why not the whole key list in one seat:** only 91 and 233 carry the product owner's 2026-11-11 "quick recommendations" rulings among the M-A keys (grep of the Jira dumps: `quick recommendations` count 1 each in 91 and 233, 0 in the other 13). 91 is already built; 233 cannot be built inside lane M-A's paths. The rest are test-only evidence (independent mutant re-runs) that is only independent in a different seat.
- **Main moved since B1554:** the kit base is `ccc41367...` (compare `0bb3ed12...main` printed `ahead ahead 1 behind 0 files 8`: PR #192, the deploy-script change). Open PRs 0.
- **Nothing in the kit touches the records seat's files** (B1562, pane `Datasec/MPS-R232`, live at 10:02): Part A writes only `tests/MpsCalc.Api.Tests/LaneMA*.cs` on a branch; no Jira, no root records.

## Scope, key by key (re-read by Jira GET at 10:00; each ticket's comments whole)
| key | status | in slice 1? | reason (comment id) |
|---|---|---|---|
| 99 | Backlog | **IN, Part A** | newest 41109: clause 5 and the three review findings "are not addressed" (40921 Open paragraph). Tests only. |
| 170 | Backlog | **IN, Part B (proposal only)** | open clause 1: needs "a stable fleet line id in the contract"; no comment names or approves a field name (0 hits for `lineId`/`line_id`/`lineKey` in the ticket dump; control: `fleet line` 4 hits). Build waits for the approved name. |
| 91 | Backlog | LEFT: ALREADY-ON-MAIN | ruling 41090: "refuses to start, in place of starting fresh". Main already does it: `SourceLifecycle.cs:327-332` (marker present, registry missing: "Start refused ... never re-initialised over a lost registry") and the row `SourceLifecycleTests.B53.cs:253-276`. One residue: a reference-only store from before the marker (no registry, no marker, empty `versions/`) still starts fresh (`IsEmptyStore` `:1079`); the hosted site cannot reach it (the ticket text says Entra mode refuses the source store). A records closing; the kit makes the seat re-prove it in PRIOR WORK. |
| 233 | Backlog | LEFT (slice 3) | ruling 41083 "A cloned quote whose typed reference already exists is refused". Not buildable inside M-A: the refusal sentence is a customer-visible word nobody has approved; the contract text it changes is `docs/api/openapi.json:369` ("not required to be unique"), `docs/API.md:430` and the generated copies `web/src/api/generated/openapi.snapshot.json:369`, `schema.ts:402` (M-E and M-W1 paths); and "exists" is undecided (Q2). It also reverses an existing row: `QuoteApiTests.V0Duplicate.cs:160` `V0_two_clones_of_one_quote_may_share_the_derived_reference`. |
| 123 | Backlog | LEFT | 41108: streaming built (#176); the other half is "a bound on concurrent uploads (a setting, so the product owner's call)", no ruling. |
| 163 | Backlog | LEFT | 40390 clause 3: "20 group runs green under load: unmeasured"; a seat cannot make the load. |
| 324, 325, 338, 333, 331, 340, 341, 207, 302 | Backlog | LEFT (slice 2) | independent mutant re-runs, no commit. Most clauses read MET at main; NOT MET are 324 (S7, S8, S9 killed only by the builder's own record), 331 (answer location), 333 (4b) and 341 (first-to-fail); what releases them is an independent run (comments 40948, 40938, 40949, 40929, 40923, 40931, 40951, 40944, 40947) or a stamped cap reading. 331's third clause is a different answer location and needs a ruling that narrows it. 341's own text asks for "a ruling that a measurement-only ticket may move, and an independent re-run". |

## Next slices (proposed)
- **Slice 2: an Opus EVIDENCE seat, no commit, no PR:** plant and run the named mutants of 324 (Q13, S7, S8, S9), 325, 338 (cap removed on the five BOM walks), 333 (the 4b order gap Sf), 340 (first-group-wins and the empty default), 341 (each of the six assertions first to fail), 207 and 302 (the panel multiset), in a throw-away tree, and write one evidence file per key with the red or green per row. Model: Opus (independence from the builders; heavy runs under the HEAVY lock and the load gate of 24). It belongs in a separate seat, not in the builder and not in the slice-1 gate. The slice-1 gate (tier G2) re-runs only slice 1's three planted mutants.
- **Slice 3: 233 build, then 170 build,** each only after its words or name is approved: 233 needs the refusal sentence (a word pack to the product owner), a decision on "exists", and a shared grant for the contract text (`docs/api/openapi.json`, `docs/API.md:430`, `web/src/api/generated/**`: sequence it with the M-E and M-W seats). 170 needs the approved name from Part B.

## Prior work (per key; the kit makes the seat repeat it)
PRs naming the keys (all 192 PRs, paginated; controls #72 and #181 present) [S03]: 99 by #176 (`acd6aec0`), #170 (`97cf7a9a`), #100 (`e3624f00`); 123 by #176; 163 by #58; 170 by #64 (`6cf4e453`); 233 by #85 (`f2584d36`); 207 by #84 and #180; 302 by #118 and #180; 91 by none; 324 to 341 by #172, #174, #180. Branches: `matching-refs/heads/b1564` 0 rows (control `heads/b1554` 1 row). Origin has 214 branches; the squash leftovers are not individually proven merged (UNMEASURED). The B1554 branch exists and is not on my paths.

## Census (by program; the frame is the unpacked tree of main `ccc41367`)
- **Slice 1 changes no product behaviour,** so no existing test pins anything it changes. `/usr/bin/grep -rl -i -E 'LaneMA|SourceLifecycle|LockTimeout' tests infra scripts tools web/e2e` -> 41 files (control: `LaneM5SourceLockWaitTests.cs` is among them); `LaneMA` alone -> 0 files (so the new names collide with nothing; control: `ls tests/MpsCalc.Api.Tests | grep -c '^LaneM5'` 2 and `'^LaneL2'` 4). Verdict for the 41: all UNAFFECTED (rewrites 0; removed lines 0 by the property check; existing files never edited). Rows nearest the work: `LaneM5SourceLockWaitTests.cs` 1 theory (4 data rows), `LaneL2SourceStageArrivalTests.cs` 1 fact, `OverlayResidueTests.B54.cs` 11 attribute lines (the H3 theory at `:550-554` runs 16, 32 and 64). The jobs that read the changed paths: `dotnet` only (`ci.yml:31`); `package` (`:110`) and `python` (`:85`) read none (the 41 files are all under `tests/`).
- **For slice 3 (233), the rows that pin the behaviour it would change:** `QuoteApiTests.V0Duplicate.cs` (12 lines naming `/duplicate`; the one that must be reconsidered is `:160`), `QuoteApiTests.Duplicate.cs` (12), `EntraAuthTests.cs` (3), `QuoteApiTests.RebateDefaultNoRights.cs` (2), `QuoteRefusalOrder.cs` (2), `QuoteApiTests.Lifecycle.cs` (2), and 1 each in `QuoteInputHardening.Enums.cs`, `QuoteApiTests.V0Opportunity.cs`, `QuoteApiTests.RentalAudit.cs` (counts of `/duplicate` lines per file, `grep -rc`, control: `V0Duplicate.cs` 18 lines for `duplicate`); the web side: `web/src/api/client.duplicate.test.ts`, `web/src/screens/QuoteScreen.toolbar.test.tsx`, `web/e2e/b352-followups.spec.ts`. Rewrite or unaffected is for that kit to decide row by row.

## Chain inputs (rule 4), in execution order
| step | input | produced by |
|---|---|---|
| 0 | the kit file, STATUS path | exists at launch / this step |
| 1 setup | kit copy, `2_Project_Files` repo, `3_Access_Keys/github_deploy_rw` (printed present), `.tools/dotnet-10.0.404` (printed 10.0.404) | step 0; BASE |
| 1 baseline | clone + main-tree | step 1 setup; `main-names.txt` and baseline trx are produced here |
| 2 predictions | baseline names, new-row design | step 1 baseline |
| 3 rows | predictions file, clone, main-tree, `tests/MpsCalc.Api.Tests/Infrastructure/SourceStores.cs` and `ApiHost.cs` (both printed at base) | steps 1, 2; BASE |
| 3 mutant runs | the new row files copied into main-tree (untracked), the one-line mutant | step 3 rows, step 1 main-tree |
| 4 checks and push | head trx and name list, `comm` against `main-names.txt`, the commit | steps 1, 3 |
| 5 Part B | pushed Part A, files read at the clone | step 4 |
The kit's own numbering runs CHECKS (item 6) and the property checks (item 7) before the push (item 8); item 4 says so.

## D-decisions the drafter took
- D1: 91 is not a build (main already refuses). D2: 233 stays out of slice 1 (paths and words). D3: the three mutants are specified by property and by their one line (m0 blocking turn at `:630` in the form `Step` uses at `:602`; m1 `Thread.Sleep` for `Task.Delay` at `:705`; m2 `GiveUpTurn` completes its turn at once at `:665`), because the review record that holds the exact mutants was not read (it lives in the project's briefs; the kit tells the seat to locate it and to name any difference). D4: gate tier G2 (tests only), raise to G1 on request. D5: the C# pre-scan rows are the drafter's own: the standard's step 7 has JS and Python rows and no C# row (printed: 0 hits for a C# row name); `codeql` is not on the machine (`command -v` printed nothing), `gitleaks` is (canary rc 1, clean rc 0, run in a scratch folder).

## QUESTIONS FOR TUESDAY (each with a default)
1. **Slice shape.** Slice 1 = 99 tests + 170 proposal, 233 deferred. Default: as drafted. Alternative: put 233 in slice 1 with a named grant on `docs/api/openapi.json`, `docs/API.md:430` and `web/src/api/generated/**` (serializes with M-E and M-W).
2. **What "exists" means for 233** (the product owner's words: "Two quotes with one reference break the audit trail"). Options: (a) the source quote's own reference only (what comment 40417 names); (b) any quote the caller can read; (c) any quote in the store (leaks to a seller that another owner holds that reference). Also whether the derived `-COPY` repeat is refused (it is today allowed, `V0Duplicate.cs:160`). Default: (b) for a TYPED reference only, derived repeats stay allowed; ask the product owner only if you disagree.
3. **The 233 refusal sentence** is a new customer-visible word. Default: slice 3 drafts it as a SLOT and a word pack; nothing ships before his word.
4. **91.** Default: a records seat records ALREADY-ON-MAIN (marker refusal at `SourceLifecycle.cs:327-332`, row `B53.cs:253-276`) and names the pre-marker residue; no build.
5. **Slice 2 evidence seat on Opus, no commit.** Default: yes, one seat, kit B-next, after slice 1 lands (it shares the dotnet suite and the HEAVY slots). If the product owner would rather give a "stamped cap reading" for 325, 338, 340, the runs for those three can be dropped.
6. **170 proposal routing.** Default: the seat writes the proposal in STATUS; Tuesday relays it to the product owner as a name card (the kit says `NAME PROPOSED: PENDING APPROVAL` and builds nothing).

## UNMEASURED
No dotnet build or test was run by the drafter (HEAVY; not her work): the 3483 Api tests relayed from PR #180's body are RELAYED; the stability of any `OverlayTimingGroup` row under load; whether m1 (poll) can be turned red deterministically (the kit tells the seat to say so with proof, not to fake a pin); the exact text of the three review findings' mutants (D3); the build summary wording "0 Warning(s)" (the kit relies on rc 0 under warnings-as-errors, `ci.yml:41`); whether the squash leftovers on origin are merged.

## Outside the fences (disclosure)
Read: this task's named sources, the two precedent kits, the gate standard, `stamp_check.py` (header), `brief_seat.sh` (header, line 31), `model-routing.md` lines 92, 108-109, `models_latest.json:23`, the project `CLAUDE.md:50` and `1_Project_Definition/CLARIFICATIONS.md` (grep only), the staged kits B1557, B1560, B1562 and B1554 by grep of their Lane tables, and the Jira MPSCALC dumps of the 15 keys (own GET-only `jget.py`, token read in-process, never printed). Wrote only inside `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s276/d1564/` (dumps, tarball of main, a scratch git repo for the property-check controls, `fill_sidecar.py`) plus the kit, its `.measured` sidecar and this report. No Jira write, no git write verb in any project repo, no push, no PR, no az, no hosted HTTP, no tmux send-keys, no message. One `gh api -X GET` tarball download of main under the project's `GH_CONFIG_DIR`. `date` is the only clock source.

DRAFTED B1564: kit 84 lines, sidecar rc 0, questions 6
