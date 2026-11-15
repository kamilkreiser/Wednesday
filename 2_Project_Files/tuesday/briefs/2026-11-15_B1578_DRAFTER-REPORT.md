STARTABLE: YES

# DRAFTER REPORT B1578 (MPS builder: MPSCALC-170 clause 1, the stable fleetLineId), drafted 15:04 to about 15:25 AEDT 2026-11-15

## BLUF
Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1578_SEAT-M140_mps-170-fleet-line-id.md` (93 lines), sidecar `.measured` beside it (85 claims, 85 measured or marked as instructions, `stamp_check.py <kit>` rc 0). Seat `SEAT-M140`, pane `Datasec/MPS-M140`, branch `b1578/mps-170-fleet-line-id` from main `3a69065a6e35ed5b5f9ee76ea8f3648f60ee13cc`, port block 9930-9939 (web server on 9931 only), model Sonnet (row C2), **gate after G1**. It builds the product owner's 2026-11-15 ruling (card `mpscalc-170-fleet-line-id-name-1115`, option a, read by `decision_queue.sh show` into scratch): an optional `fleetLineId` on `FleetLineDto` and the contract's `FleetLineInput`; the server assigns ids, keeps them across saves, falls back to the same `lineNumber` for a line sent without one, and works them out deterministically on read for old quote documents; the price audit pairs fleet lines by id, so the ticket's remove-and-renumber case records only the removed line's entries. No new word anywhere a person reads; no web source change except the three generated contract copies (commit 2, made by `sync-contract.mjs`). Stamp slots and `READ-WHOLE-BY-TUESDAY: ____` are left for Tuesday.

## A finding Tuesday should see before the stamp
- **The card's wording does not match the code on one point.** The card (and the commission) say the id "sits beside the existing fleetLineNumber". In the code the fleet line's own number is `LineNumber` / JSON `lineNumber` (`Dtos.cs:39`); `fleetLineNumber` is on the hardware and software lines that point AT a fleet line (`Dtos.cs:53`, `:60`). The kit puts `fleetLineId` on the fleet line beside `lineNumber` and leaves the BOM lines pointing by number. That matches the ruling's intent ("a stable id on each fleet line") and adds no other name, so I did not treat it as a STOP. Q5.
- **There is a rollback hazard for the deploy card (DERIVED, not run).** Snapshots are read with `ApiJson.Options`, which refuses unknown members (`QuoteFileStore.cs:365`, `ApiJson.cs:23`). Once a snapshot is taken carrying `fleetLineId`, a build older than this one cannot read it. Quote documents are fine (`ReferenceStore.JsonOptions`, default skip, `QuoteFileStore.cs:122`). The kit makes the seat write this under FOR TUESDAY.

## Design of the kit
- PROPERTIES P1 to P5, not code: (P1) the field and its contract text, whose description must not start with "internal" because `internalNames.ts:14` would then treat it as an internal field. (P2) Ids are assigned on create (caller ids are not kept), and on save in this order: keep a held id, then take the id of the stored line with the same number, then mint a new one. This runs BEFORE `SameDraft` (`QuoteEndpoints.cs:178`) and BEFORE the audit, so the web's save of an unchanged draft without ids stays a no-op. An unknown or repeated id is treated as no id: no refusal and no new sentence. The id goes to every caller who reads the draft. (P3) Old documents get the same ids worked out on every read, a read does not rewrite the document, the next save persists them, and snapshots are never rewritten. (P4) The audit pairs by id; drafts without ids still pair by number through the existing `Pairs`, so every existing unit row stays green unedited. (P5) The id never reaches an audit entry, a proposal, an export, a refusal or a screen.
- Rows R1 to R11 come first and must be red at main. At main, sending `fleetLineId` is refused 400 because of the Disallow setting. R1 is the ticket's case and also runs without ids as a control. R6 to R8 seed an old-shape document into a fresh file store. R7 measures B159-9 on a stored quote whose two lines share number 1.
- Seven planted mutants (mF1 to mF7), each tied to a named row.
- Census by program (FACT 9): the REWRITE and UNAFFECTED lists, each proven by whole-suite runs. Raw lists are in scratch `census_raw.txt`.
- Two commits on one branch, because `sync-contract.mjs` reads the contract from a committed ref (FACT 8; `contract.sync.test.ts` is red at commit 1 by design). One plain push at the end.
- Toolchains are named by path: `.tools/dotnet-10.0.404` as `DOTNET_ROOT` printed `10.0.404`. MPS has no drive-local node (MEASURED), so the default is the machine node v26.13.0 with a "CI uses 24" note in STATUS (Q4).

## Facts re-measured with instruments (each in the sidecar)
- Main is `3a69065a...` (`gh api -X GET .../git/ref/heads/main`, 15:04). Open PRs: 0. `matching-refs/heads/b1578`: 0 rows. 194 PRs paginated; only #64 names 170. `fleetLineId` occurs 0 times on main (control: `fleetLineNumber` 150 occurrences in 38 files).
- MPSCALC-170 is Backlog, with comments 39487, 39537 and 40395, read whole by my own GET-only helper `jira_get.py`. Control: MPSCALC-361 reads Done. JQL was not used; reads were by key only.
- Every `file:line` in the kit was printed by `grep -n` over the tarball of `3a69065a`.
- Ports: `lsof -nP -iTCP:9930-9939 -sTCP:LISTEN | wc -l` printed 0 (control: the unfiltered count printed 22). Over the 26 non-`.pre-` SEAT kits of 14 and 15 Nov, a scan for `993x` found 0 files (control: `992x` found 1). Live panes at 15:11: MPS-R233, MPS-M138, MPS-M139, HPSM-POC-H165, HPSM-POC-H166, NexusAI-N130.
- Partition with M139 (B1573): it writes `tests/MpsCalc.Api.Tests/LaneMA*.cs` only. My kit's test files are `FleetLineId*.cs`, and `LaneMA*` is listed as NOT yours. M138 writes no repo file. R233 writes root records and Jira only. **The two lanes share no path.**
- `PricingPolicy.cs` names `fleet` 0 times (control: `bomLines` 12). `ApiHost.cs:152` `Seller(bool internalMetrics = true)`.

## Chain-step input table (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit, project root | Tuesday's stamp; exists |
| 1 | origin main, clone, baseline runs, `names-base.txt` | origin; Step 1 itself |
| 2 predictions | rows' intended shape, mutant list | the kit; before Step 3 |
| 3 rows red | clone at base, host helpers | Step 1; base |
| 4 implement + commit 1 | rows from Step 3 | Step 3 |
| 5 mutants | commit 1 in the clone | Step 4 |
| 6 commit 2 | commit 1 sha, `node_modules` (`npm ci` of Step 1) | Steps 1 and 4 |
| 7 checks | head (commit 2), `names-base.txt`, baseline counts | Steps 1 and 6 |
| 8 property checks | `<base>..HEAD` | Step 6 |
| 9 push | checks green | Steps 7 and 8 |
| 11 STATUS | all of the above | Steps 0 to 9 |

## D-decisions (mine)
- D1: Seat number M140. The highest earlier `SEAT-M` in the briefs folder is M139 (B1573, by listing).
- D2: Gate G1, not G2. The change alters every quote document's stored shape and the audit's pairing, and no prior gate has measured this mechanism.
- D3: No refusal for unknown or repeated ids. They are treated as no id, which avoids any new user-readable sentence (the ruling says "staff see no new word").
- D4: Create mints every id and keeps no caller id. Duplicate keeps the source's ids, because the existing Duplicate row asserts the copy's draft equals the source's apart from `quoteRef`.
- D5: Both browser steps are required (port 9931). The web change is types and snapshot only, but CI runs them and the gate wants the run.
- D6: READY target is Step 0 + 270 min, with commit 1 by +180. The duration of a whole dotnet suite is UNMEASURED by me (B1573's report estimated about 8.5 min, RELAYED).

## Q-questions for Tuesday (each with a default)
- Q1: Model row. Default: Sonnet, row C2 (`model-routing.md:92`), then an Opus gate at G1 (`:108`). Alternative: Opus under C3 (`:93`), if you read the price audit's pairing as a money design surface.
- Q2: Version diff. Default: leave `DraftChanges` unchanged and require R10 (a revise with no edit lists no `fleetLineId` path). A line whose id changes at a number would then show a `fleet[n].fleetLineId` path in the API diff, which no screen reads. Alternative: exclude `fleetLineId` from the diff, which needs one more line in `Mapping.cs`.
- Q3: Stubs. Default: neither the web dev stub (`web/src/api/stub/**`) nor the demo stub (`tools/demo/test/stub_api.py`, whose `FLEET_FIELDS` lists the old set) is taught the id. The field is optional, the web never reads it, and the seeder never sends it. File a later fidelity ticket if wanted.
- Q4: Node. Default: the machine `/opt/homebrew/bin/node` v26.13.0 with the "CI uses 24" note (the precedent of B1566). Alternative: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/node24/bin` (v24.21.0), read-only, first on PATH. That is another project's folder, so I did not default to it.
- Q5: Card wording vs code ("beside the existing fleetLineNumber"; see above). Default: proceed with `fleetLineId` on the fleet line beside `lineNumber`, BOM lines unchanged, no card back to the product owner. Alternative: re-ask the product owner before launch.

## UNMEASURED
- Whether the derived-on-read ids and the save rules pass the whole suite. No build was run by me.
- The run time of the dotnet suite and the browser steps here.
- Whether any existing row compares a create response's draft byte for byte with what was sent. The static census found none, but the seat's whole-suite run decides.
- The snapshot rollback hazard (DERIVED from `ApiJson` Disallow).
- That `sync-contract.mjs` runs clean in a `--no-checkout`-then-checkout clone with `npm ci` done. Read from source only.

## Outside the fences
None. What I read:
- the commission, the rules file, the B1573 and B1566 kits and reports, the B1574/B1572 kits (lane lines only) and the B1577 ANSWER-1;
- the decision card, by `decision_queue.sh show mpscalc-170-fleet-line-id-name-1115` into scratch `card170.txt` (inclusion check `grep -c` on the id gave 1; no `list` was run);
- MPSCALC-170 and MPSCALC-361 by GET, the project `BACKLOG.md` rows B36-N4 and B102-1 (read-only), the project `CLAUDE.md:50`, and the project `.env` key NAMES only;
- the main tarball via `gh api -X GET` under the project `GH_CONFIG_DIR`, `model-routing.md`, `models_latest.json` and `brief_seat.sh`;
- `lsof`, `tmux list-panes`, and `ls` of the project `.tools`.

No project write, ref write, Jira write, az, hosted HTTP or message. Hook refusals: one (an unquoted `======` separator in an echo; no effect). Scratch in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1578/`: `main.tgz` and `tar/`, `jira_get.py`, `j170.json`/`.txt`, `j361.json`, `card170.txt`, `pulls.tsv`, `census_raw.txt`, `kits.txt`, `fill.py`, `measured.init`, `check.out`.

DRAFTED B1578: kit 93 lines, sidecar rc 0, questions 5
