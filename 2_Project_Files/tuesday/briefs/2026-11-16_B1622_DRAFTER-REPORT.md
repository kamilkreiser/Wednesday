STARTABLE: YES (after the stamp; 6 questions below, each with a default the kit already assumes)

# B1622 drafter report: MPS Commercial Calculator, lane M-D, developer docs (seat M147)

Drafted 2026-11-16 from 15:44 to about 15:58 AEDT (`date` printed 15:44:54, 15:45:12, 15:48:13, 15:50:58, 15:52:49, 15:56:17 and 15:56:22). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1622_SEAT-M147_mps-lane-md-developer-docs.md` (95 lines, 12 stamp slots left as `____`) with sidecar `.measured` (110 lines; 62 measured by program, 48 "INSTRUCTION to the seat"). `stamp_check.py <kit>` rc 0 (110 claims, 110 measured).

## BLUF
- **Lane M-D is docs only and fits one Sonnet seat in four parts, one commit each: A = MPSCALC-390 (a clause in ENGINE.md rows X-33 and X-46), B = MPSCALC-394 (the source version id sentence in the API.md Validate bullet), C = MPSCALC-371 (the template-store paragraph, corrected from the code), D = a RE-READ of MPSCALC-195, 316 and 200 (records-only is a good result).** Model row C2 (`model-routing.md:92`), gate G3 as the commission says (row G2 `:109` also names docs: Q6), pane `Datasec/MPS-M147`, branch `b1622/mps-lane-md-developer-docs`. READY at Step 0 + 120 minutes. No npm, no dotnet, no listener (dotnet only if Q1 = YES). Nothing deployed.
- **`docs/api/openapi.json` is never edited: the project has no generator of it.** `web/scripts/sync-contract.mjs` only copies the contract into `web/src/api/generated/` (three `writeFileSync`, lines 23, 30, 37), and a sync test fails if they differ. The commission allowed the file only "via the project's own generator", so the G2-if-regenerated branch does not arise; 316's contract places (`maxLength` 100 at `:988` and `:1036`) and the C# sentence (`QuoteEndpoints.cs:1436`) are reported as outside the lane.
- **No CI job reads these docs.** The only test naming IMPORTER.md (`OutputGuardTests.cs`) writes its own bytes into a temporary repo; nothing reads ENGINE.md or API.md. Docs hold 0 Cf/Cc characters at base; the kit demands ASCII-only added lines.
- **Three of the six tickets are already partly built, which changes the work.** 371: the three sentences the ticket names (B1118-2/-3/-4) ARE on main at API.md:895-908; what remains is the earlier gate's N7 (b), (c), (d) (lower event count, "stray" temporary file, "even one answered 404" as an example). 316: the agreed sentence is already in API.md:438 and openapi.json:369. 195: clauses 1, 2, 5, 6, 7 read MET at the last record; clause 3 and the engine-target sentence cannot be built (no words given).
- **200 cannot be finished without reading a price book.** Clauses 2 and 3 (the A3 15 and A4 3 unread rows) need counts from the local store; the records comment says so itself. The kit forbids `.local/` and any price book and ends 200 as NOT MET (Q2). The sweep listed 200 as firm; this is a real gap in that listing.

## Scope, key by key (each read whole by Jira GET)
| key | status | in slice? | reason |
|---|---|---|---|
| MPSCALC-390 | Backlog, 0 comments | IN, Part A (Part A2 conditional) | both rows lack one condition the code has; main's pointers equal the ticket's (X-33 `:160`, X-46 `:173`, importer `:656`, `:703`); the stale comment is a test file, outside the lane's paths |
| MPSCALC-394 | Backlog, 0 comments | IN, Part B | `API.md:704` states only that ids are unique; the rule is built (code `SourceDocumentChecks.cs:85-92`, `IdKey` `:133`) |
| MPSCALC-371 | Backlog, 2 comments | IN, Part C | corrected from the code, no word review (the 2026-11-11 acceptance on developer-only docs, quoted in the kit) |
| MPSCALC-195 | Backlog, 5 comments | Part D re-read | clause 3 and the engine-target sentence NOT BUILDABLE (Q3); clause 4 to re-derive; clause 1 to re-read against the code |
| MPSCALC-316 | Backlog, 4 comments | Part D re-read | docs places done; the rest is contract and code (outside the lane) |
| MPSCALC-200 | Backlog, 1 comment | Part D re-read | NOT BUILDABLE without the price-book store (Q2) |
Held and dropped check: the sweep's `ctx2.py` run (sweep1450) covered 390, 200, 371, 394, 195 and 316: 390 has one old pickup line (517, "waiting for B1527"), the others zero hits (positive controls fired there). I did not re-run the pickup grep in this drafting beyond the tickets' own comments (UNMEASURED: whether B1527 has landed); the kit's PRIOR WORK makes the seat re-read comments newer than 2026-11-11.

## Facts re-measured with instruments (details in the sidecar)
- Main `5e80009525138879031c4b07a18436242dadf46c` at 15:45 (`gh api -X GET .../git/ref/heads/main`); open PRs 0 (control: 199 PRs listed, #72 and #181 present); `heads/b1622` 0 rows, `heads/b1617` 1 row (the M-S lane, `web/src/api/stub` only, 3 ahead, 0 `docs/` files).
- Branches: 221 origin branches compared with main; 88 differ in some `docs/` file; 14 of those are not the head of a merged PR, all last committed 2026-10-10 to 2026-10-16.
- Code pointers printed by `grep -n -F` at the sha (X-33 refusal `PurchaseCalculator.cs:667-678` order; `Resolve` `:123-131`; importer `:651`, `:656`, `:703`; id rule `SourceDocumentChecks.cs:80-92`, `:133`, `:189`; template store `:35`, `:312-320`, `:442-467`; quote store `:330`).
- Machine: load 11.77 at 15:52; 1143 GiB free; no lock folder under `<project>/.tools`; one `Datasec/MPS-` pane (the records seat R244). dotnet `10.0.404` at `<project>/.tools/dotnet-10.0.404/` printed `10.0.404` (only Part A2 would use it).

## Chain inputs (rule 4), in execution order
| step | inputs | produced by / exists at |
|---|---|---|
| 0 | the kit, the STATUS path | exists at launch / this step |
| 1 setup | clone, identity, deploy key, base blobs | BASE and the machine |
| 2 predictions | the base docs and code lines | step 1 |
| 3 Part A | `ENGINE.md` rows, `PurchaseCalculator.cs`, `PriceBookImporter.cs` | BASE |
| 4 Part B | `API.md` Validate bullet, `SourceDocumentChecks.cs`, three id test files | BASE (and Part A's commit only for the branch) |
| 5 Part C | `API.md` persistence bullet, `TemplateStore.cs`, `TemplateEndpoints.cs`, `QuoteFileStore.cs`, `TemplateStoreTests.cs` | BASE; Part B's edit sits in the same file (different lines) |
| 6 Part D | the three clause tables | BASE; Parts A to C |
| 7 checks | each part's diff | steps 3 to 6 |
| 9 push | each part's diff, the gitleaks canary | steps 3 to 7 |
| 10 Part A2 (conditional) | `PurchasePageEstimate.cs`, dotnet toolchain | BASE; `.tools/dotnet-10.0.404` |

## D-decisions the drafter took
- **D1** One Sonnet seat, four parts; each part a separate commit so Tuesday can drop one.
- **D2** Docs words are written from the printed code lines; every added clause has a claims-table row (text, source line, what code change would falsify it). No mutant runs: nothing is executed.
- **D3** `openapi.json` and `web/src/api/generated/**` are never touched (no generator; the sync test would go red on a hand edit).
- **D4** Part C changes a sentence only where a printed line shows it false or short; N7 (b), (c), (d) are each WRITTEN or LEFT with the reason. No new probe, no run.
- **D5** Part D is a table exercise; the engine-target sentence and the rate-limit parenthesis are NOT written (the words the product owner accepted are not in a file the lane may read).
- **D6** The stale test comment (390) is not edited by default (outside the commission's owned paths); a conditional Part A2 carries the exact change and its dotnet checks if Tuesday says yes.

## QUESTIONS FOR TUESDAY (each with a default)
1. **The stale test comment** (`tests/MpsCalc.Engine.Tests/PurchasePageEstimate.cs:10`, 390's third item): default not edited, reported (the commission's owned paths are docs only). Say YES and Part A2 runs: a comment-only change plus `dotnet build` and the Engine tests (HEAVY). No other lane owns that file.
2. **MPSCALC-200** needs counts from the local price-book store to explain the A3 (15) and A4 (3) unread rows. Default: the seat reads no store, writes nothing about those rows, and 200 stays NOT MET. If you want the counts, that is a separate grant (counts only) and a separate kit.
3. **MPSCALC-195 clause 3** (the "(whole seconds, at least 1)" parenthesis at `API.md:760`) and the **drafted engine-target sentence** the product owner accepted: neither text is in any file the lane may read. Default: not written, reported; Tuesday or the records seat supplies the words if they exist.
4. **MPSCALC-394:** U+212A, U+212B and the combining U+0345 are left unsaid unless a test pins them (the records note says "pinned neither way"). Default: unsaid, listed in STATUS.
5. **MPSCALC-316:** the double parenthesis at `API.md:438` (a gate Note) and the remaining places (contract `maxLength`, C# sentence). Default: reported, not edited.
6. **Gate tier:** G3 as commissioned; `model-routing.md:109` row G2 names docs. Default G3; raise at the stamp if you want a read of the claims tables by an independent gate.

## UNMEASURED
Whether main's code has moved since 15:45 (the seat re-reads); the HTTP status each `TemplateUnavailableReason` maps to (the kit makes the seat read it before writing a status); N7's "probe" claims (no probe run); whether the B1623 kit (M-E) names a path of this lane (its kit was drafted beside this one; the seat's PRIOR WORK compare would show it, and the commission's own text gives M-E only `web/` paths); whether B1527 has landed (pickup line 517); the `docs/API.md` wrap width (the seat prints the longest line of `:703-709`).

## Outside the fences (disclosure)
Read: the commission, SWEEP-1450 (lane text, sections 5 and 6), DRAFTER_RULES, the B1617 kit, sidecar and report (template), the MPS `CLAUDE.md` (lines 50 and the pricebook rows), `model-routing.md` rows (sed), `models_latest.json:23`, `brief_seat.sh:31`, a CLARIFICATIONS entry (C-108: one grep printed a long neighbouring entry by mistake, read and not used), and at main by a tarball of the sha (`gh api -X GET .../tarball/<sha>`, extracted under my folder) the three docs, `openapi.json`, `PurchaseCalculator.cs`, `PriceBookImporter.cs`, `SourceDocumentChecks.cs`, `TemplateStore.cs`, `TemplateEndpoints.cs`, `QuoteFileStore.cs`, `OutputGuardTests.cs`, `ci.yml`, `sync-contract.mjs`. Jira: GET only (390, 394, 371, 195, 316, 200, 189) through my own helpers `jdesc.py` (copied from the sweep's folder) and `jall.py` (new, in my folder). GitHub: `gh api -X GET` only (ref, pulls, branches, 221 compares, commits, tarball). No price book, no `.local`, no `Source_Documents`, no `decision_queue.sh`, no card, no ledger, no mail, no push, no PR, no az, no npm or dotnet run (only `dotnet --version`), no hosted HTTP. Wrote only: the kit, its sidecar, this report, and my folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s283/b1622/` (tree and tarball of main, ticket dumps `t*.txt` `c*.txt`, `claims.sh`, `fillside.py`, branch and PR lists, `compare_docs.tsv`, a `_quarantine` folder holding the first contents-API copy of the docs). `date` is the only clock source.

DRAFTED B1622: kit 95 lines, sidecar rc 0, questions 6
