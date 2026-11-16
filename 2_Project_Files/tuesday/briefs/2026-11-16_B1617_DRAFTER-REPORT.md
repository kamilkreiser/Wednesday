STARTABLE: YES (after the stamp; 5 questions below, each with a default the kit already assumes)

# B1617 drafter report: MPS Commercial Calculator, lane M-S, the dev stub's Duplicate and update pins (seat M145)

Drafted 2026-11-16 from 14:56 to about 15:11 AEDT (`date` printed 14:56:56, 14:57:07, 14:59:27, 15:00:21, 15:02:55, 15:04:36, 15:05:01 and 15:09:46). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1617_SEAT-M145_mps-lane-ms-stub-duplicate-and-update-pins.md` (90 lines, 12 stamp slots left as `____`) with sidecar `.measured` (115 lines, tags M00 to M12). `stamp_check.py <kit>` rc 0 (115 claims, 115 measured; about 55 of the rows are "INSTRUCTION to the seat" lines for names, paths and markers the seat writes).

## BLUF
- **Lane M-S fits one Sonnet seat in three parts, three commits: A = MPSCALC-404 refusals (a Seller's Duplicate of a draft holding a target GP, a manual item or a visible price is refused as the server refuses it; the eight rows that copy such a draft run as the Pricing analyst; a hidden-only Seller row stays), B = MPSCALC-405 (one row pinning the answer of a held rental update), C = MPSCALC-404 reference limits (typed reference over 100 UTF-16 units or with a control character is 400; the derived reference is cut as the server's `CopyRef`).** Model row C2 (the stub SOURCE changes; the commission said L6, same Sonnet model, Q1), gate G2, pane `Datasec/MPS-M145`, branch `b1617/mps-lane-ms-stub-duplicate-and-update-pins`. READY at Step 0 + 150 minutes, Part A pushed by +60, Part B by +90. Nothing deployed, no product byte.
- **The sweep's text for 404 missed the ticket's second half** (the typed-reference limit and the derived-reference cut are in 404's Recommendation and Acceptance). I made that Part C so it can be dropped without touching Parts A and B. It needs one new stub sentence (the 400 title): Q2.
- **Everything the kit claims about behaviour was run on a scratch tarball of main** (`npm ci --offline` from the machine cache, rc 0): main baseline 146 files / 1580 tests green, lint rc 0, typecheck rc 0. Gaps are real (7 of 7 plant rows green at base, each asserting today's gap, with a control that fires). A throw-away refusal turns **exactly eight existing rows red, all in the Duplicate block, and the row for a non-Seller caller and `client.duplicate.test.ts` stay green**: those eight are the rows to move to the analyst. The 405 plant is green on main; with `stubApi.ts:349` answering without `draftForCaller` it goes red while **all 100 stub and duplicate rows and the whole web suite (1580) stay green** (the ticket's claim, measured).
- **Two traps found and written into the kit:** (1) a control-character regex literal fails lint (`no-control-regex`; measured), so the kit demands a `charCodeAt` loop and bans `eslint-disable`; (2) a hidden-only Seller draft must hold NO fixed click rate or sell override (those are visible prices), and the existing `INTERNAL_KEYS` constant lacks `supplies`.

## Scope, key by key (each ticket read whole by Jira GET at 15:02)
| key | status | in slice? | reason |
|---|---|---|---|
| MPSCALC-404 | Backlog, 0 comments | IN, Parts A and C | the dev stub copies what the server's Duplicate refuses; ticket pointers are older than main (kit FACT 3 has main's) |
| MPSCALC-405 | Backlog, 0 comments | IN, Part B | the pin is missing; the code is right |
Held and dropped check (`ctx2.py` over the pickup, the 11-15 and 11-16 notes): 404 has two records-created mentions (pickup `:231`, note 11-15 `:104`), none a hold; 405 zero hits (control: 404 hits); 399, 334 older mentions only. PRs naming 404 or 405 (all 199 PRs): none; naming 399: #193 only (controls #72 and #181 present). Branches: nine origin branches touch `web/src/api/stub/` and each is a merged-PR head (#7, #12, #16, #40, #109, #111, #114, #178, #193; control: a nonexistent head returns 0 PRs).

## Facts re-measured with instruments (details in the sidecar)
- Main `5e80009525138879031c4b07a18436242dadf46c` at 14:57:07; open PRs 0; `heads/b1617` 0 rows (control `heads/b1593` 1).
- The server's order for a copy (printed by `grep -n`): reference validation and target GP (`QuoteEndpoints.cs:543`, `:1469`), then manual items, manual lines, visible prices (`PricingPolicy.cs:80`, `:115`, `:130`). The kit's order rows are DERIVED from those lines, not run on the server. The server refuses an EMPTY `manualItems` too (`is not null`, `:80`); the kit says the stub does not model that (Q4).
- Reference rules: `QuoteEndpoints.cs:1434` (length 100, UTF-16), `:1446` and `:1573` (control character: C0, DEL, C1), `CopyRef` `:584-601`; emoji counts two; the cut drops a split pair whole.
- The 400 title the server uses for a draft is "The draft is not valid." (`QuoteEndpoints.cs:1465`); the stub's own 400 pattern is `inventory.ts:107` with a `(stub)` suffix. That is why Q2 offers server title plus the suffix.
- CI web job (`ci.yml:45-89`): `npm ci`, lint, test, both browser modes, entra build plus bundle check. No other job reads a stub source file (0 files for `purchaseQuotes`, `stubApi`, `holdCopy`; control: `api/stub` hits `scripts/package.sh` and `scripts/deploy-package.py`). The only e2e spec naming a duplicate uses the route mock, not the stub (DERIVED).
- Machine: load 7.5; no heavy or git lock folders; no `Datasec/MPS-*` pane; 1151 GiB free.

## Chain inputs (rule 4), in execution order
| step | inputs | produced by / exists at |
|---|---|---|
| 0 | the kit, the STATUS path | exists at launch / this step |
| 1 setup + baseline | clone, identity, deploy key, node 24 to 26, machine npm cache | BASE and the machine (printed present above) |
| 2 predictions | baseline counts | step 1 |
| 3 Part A rows then fix | `stubApi.test.ts`, `purchaseQuotes.ts`, `holdCopy` at base | BASE; step 1 |
| 3 moved rows | the eight red rows named by the throw-away refusal | the run in step 3(a) / FACT 5 |
| 3 mutants | the committed Part A tree | step 3(c) |
| 4 Part B row | `stubApi.ts:349`, the analyst's stored hidden draft | BASE; the row itself stores it first |
| 4 Part B mutants | the Part B row, `purchaseQuotes.ts:51` | step 4 |
| 5 Part C rows | `holdCopy` with Part A's refusals in place | step 3 (pushed) |
| 6 checks, pre-scan | each part's diff | steps 3 to 5 |
| 8 push | each part's diff, the gitleaks canary | steps 3 to 6 |

## D-decisions the drafter took
- **D1** One Sonnet seat, three parts: A (the security-flavoured refusals) first, B (the cheap pin) second, C (the part that needs a new sentence) last so it can be dropped.
- **D2** A stub refusal reuses the stub's three existing titles verbatim (`purchaseQuotes.ts:95`, `:99`, `:101`); no new refusal code; the empty-`manualItems` edge is documented in the docstring, not modelled.
- **D3** The refusal check applies only to a caller WITHOUT internal-metrics, after `requireSeller` (so the non-Seller row keeps FORBIDDEN first), and in the server's order; Part C's reference checks go before them (the server validates first).
- **D4** Moved rows are MOVED, never dropped: the kit demands an old-name to new-name map and an assertion-by-assertion map, with `comm -23` and `-13` lists of test names.
- **D5** No browser step by the seat (vitest binds no port; no port block needed); the gate runs both Playwright modes and the entra build. The seat runs the entra build once at Part C's head.
- **D6** Mutants are per-check (mA1 to mA6, mB1 and mB2, mC1 to mC3) and each names the row it must turn red.

## QUESTIONS FOR TUESDAY (each with a default)
1. **Model row:** the commission names row L6 (test-only pin); Parts A and C edit stub source (a dev double). Default: row C2, same Sonnet model, gate G2. No effect on the launch line.
2. **The 400 title in Part C** (the one new stub sentence): default allowed as the server's own "The draft is not valid." plus ` (stub)`. If you say no, Part C does not run and READY says so; Parts A and B stand.
3. **Browser steps:** default the seat runs none; the G2 gate runs `npx playwright test` in both modes and the entra build. Say otherwise and the kit needs a port block (9980-9989 had 0 listeners at 15:04).
4. **Empty `manualItems` list** (server refuses it, stub would copy it): default documented in the docstring, not modelled.
5. **Out of scope, seen:** the stub's `draftForCaller` (`purchaseQuotes.ts:45`) does not omit `assumptions.targetGrossMargin` for a caller without internal-metrics, and no stub file mentions it. What the server answers on a READ is UNMEASURED. Default: the seat reports it and does not edit it; a ticket if the product owner wants it (not filed here).

## UNMEASURED
Whether hosted CI's `web` job agrees with the local runs (node 24 versus the box's 26.13); the entra production build and `check-bundle.mjs` after the change (the seat runs them); whether the CodeQL JavaScript pack runs on this repository; the whole-suite time under the heavy-lock protocol (the drafter's own run was about 12 seconds); how the server treats a whitespace-padded typed reference (the stub and the client trim, the server does not); whether the e2e `b352-followups` Clone spec reaches the stub (DERIVED: it uses the route mock); the server's behaviour for the order rows (DERIVED from source).

## Outside the fences (disclosure)
Read: the commission and SWEEP-1450, DRAFTER_RULES, the B1593 kit, report and STATUS (template), the B1566 kit lines 1-30 (web toolchain), `model-routing.md` rows (awk), `models_latest.json:23`, `brief_seat.sh:31`, project `.tools` listing, the pickup and the 11-15 and 11-16 notes through the sweep's `ctx2.py`, and at main (by `gh api -X GET .../contents` and a tarball): the five stub files, `types.ts`, `client.ts`, `personas.ts`, `generated/schema.ts`, `docs/API.md`, `QuoteEndpoints.cs`, `PricingPolicy.cs`, `ci.yml`, `web/package.json`, `eslint.config.js`, `check-bundle.mjs`. Jira: GET only (404, 405, 361, 399) through the sweep's `jdesc.py` (project `.env` in-process, token never printed). GitHub: `gh api -X GET` only (ref, pulls, branches, compare, tarball, contents). **Ran, beyond reads, under no heavy lock (none existed; load 6 to 8):** in a scratch tarball of main under `fleet/state/s282/r1617/tree/` (my folder): `npm ci --offline --ignore-scripts` (machine cache, rc 0), `npx vitest run` (whole suite several times, and single files), `npx eslint .`, `npx tsc -b`, throw-away edits to `purchaseQuotes.ts` and `stubApi.ts` (each restored and proved with `cmp`), and four plant test files and one lint plant file added there. **One slip:** `npx prettier --version` (I looked for a formatter) made npm print "The following package was not found and will be installed: prettier@3.10.1", so it may have contacted the npm registry once; nothing from it was used, and no other command reached the network. Wrote only: the kit, its sidecar, this report, my folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s282/r1617/` (sources at the pinned sha under `src/`, `tree/`, `main.tgz`, `plant404.test.ts`, `plant405.test.ts`, logs, `branches.txt`, `prs.jsonl`, `claims*.txt`). No Jira write, no git write verb in any project repo, no push, no PR, no az, docker or ssh, no hosted HTTP beyond the GETs above, no `decision_queue.sh`, no card read, no message, no WEDNESDAY or FRIDAY tree, no `_ledger.md`, no Artifact tool. `date` is the only clock source.

DRAFTED B1617: kit 90 lines, sidecar rc 0, questions 5
