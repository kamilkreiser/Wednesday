# Drafter report: B517-B520 (+ B522), MPS Calculator builder briefs

Drafted 2026-10-23 11:30-11:50 AEDT by Tuesday's brief drafter (Sonnet 5.5). Read-only everywhere except the ten brief files below and this report. Nothing stamped, launched, sent or written to Jira; no HTTP to any app or hosted host. Inputs read whole: the lane screen (`0_Brain/projects_index/2026-10-23_datasec-lanes.md`), the MPS `CLAUDE.md`, the B484, B509 and B510 briefs, `models_latest.json`; Jira MPSCALC GETs of 26 tickets (descriptions and comments); the code of main `e027ebd0` from `gh api -X GET .../tarball/e027ebd0...` (main re-read by `ls-remote` and `git/ref`: still `e027ebd09640cad95d5b18716c6e6fb8e870835e`, no `b5*` branch, 0 open PRs).

## Files (each plus a byte-identical `.pre-stamp`)

| Brief | Seat / pane | Branch | Model row, gate | Ports | Lines | Open stamp lines |
|---|---|---|---|---|---|---|
| `2026-10-23_B517_SEAT-M1_mps-contract-docs.md` | M1 `Datasec/MPS-M1` | `b517/mps-contract-docs-wording` | Sonnet, C2/C8; G2 Sonnet | 8620-8629 | 145 | 8 |
| `2026-10-23_B518_SEAT-M2_mps-api-input-hardening.md` | M2 `Datasec/MPS-M2` | `b518/mps-api-input-hardening` | Sonnet, C2; G1 Opus | 8630-8639 | 138 | 8 |
| `2026-10-23_B519_SEAT-M3_mps-pricing-policy-leak-tests.md` | M3 `Datasec/MPS-M3` | `b519/mps-pricing-policy-leak-tests` | **Opus** `claude-opus-5-5`, C3; G1 Opus | 8640-8649 | 123 | 8 |
| `2026-10-23_B520_SEAT-M4_mps-source-lifecycle-hardening.md` | M4 `Datasec/MPS-M4` | `b520/mps-source-lifecycle-hardening` | Sonnet, C2; G1 Opus | 8650-8659 | 129 | 8 |
| `2026-10-23_B522_SEAT-M16_mps-deal-usage-colour-row.md` | M16 `Datasec/MPS-M16` (new lane) | `b522/mps-deal-usage-colour-rate-row` | Sonnet, C2; G2 Sonnet (G1 if a word changes) | 8660-8669 | 123 | 8 |

Open stamp slots, same in every brief (8 lines hold the four-underscore pattern: 7 slots + the last line): `STAMP`, `LAUNCH WINDOW`, `Stamped by`, `Launch authority`, `Hard stop and target READY` (drafter suggestions: M1 3h/5h, M2 4h/7h, M3 3h/5h, M4 4h/7h, M16 2h/4h), `Main at launch` (expected `e027ebd09640cad95d5b18716c6e6fb8e870835e`), `Model receipt line and load1`, and `READ-WHOLE-BY-TUESDAY: ____`. The REFUSE check `grep -c -E '_''_''_''_'` reads 8 on the `.pre-stamp` copy (verified).
Model line in each: `model: <id> -- C2 build (M3: C3 build) -- P1-P4 none -- gauge 89% (Tuesday no-90% grant)`; ids from `models_latest.json` (`claude-sonnet-5-5`, `claude-opus-5-5`). Launch commands use `BRIEF_SEAT_LEVEL=sonnet` (M3: `opus`).

## NUMBER COLLISION: B521 is taken, my fifth brief is B522

While I was building, another drafter wrote `2026-10-23_B521_SEAT-J4_composer-pcomp-cleanup.md` and `B521_DRAFTER-REPORT.md`. My new-lane brief was first written as B521; I moved those two files (mine) to the scratchpad and re-issued it as **B522** (seat `Datasec/MPS-M16`). If another drafter takes B522 before you read this, one of the two must be renumbered; my files reference `b522`/`B522` throughout.

## Corrections to the lane screen (all MEASURED against `e027ebd0`)

- **M1** gains `web/src/api/generated/SOURCE.txt` (`sync-contract.mjs` writes it; `contract.test.ts` pins it). M1 runs the full .NET + web CI line, because the Api test project links `docs/api/openapi.json` (`tests/MpsCalc.Api.Tests.csproj:29`).
- **ENGINE.md is also the calculation register** (X-table, X-32 is the last row). B518's ticket MPSCALC-196 asks for a register row first; the partition forbids a second writer of `docs/ENGINE.md` (M1 is the single writer). So B518 writes the row TEXT into its STATUS (before the red test) and **Tuesday has it inserted after B517 lands** (a deliberate, stated deviation; alternative: let B518 append X-33 at the table end, which M1's X-31 edit would not overlap line-wise but would break the screen's pairwise-disjoint claim).
- **M2** gains two new test paths (`DealUsageNoCountedDevice*.cs`, `StoreLoadRows*.cs`).
- **M4**: `SourceLifecycleTests*.cs` in the screen's list matches 17 existing files; the brief makes new rows go in NEW `SourceLifecycleTests.B520*.cs` files.
- **Heavy slots:** `heavy-slot-1` is held by a stale `B483` holder (do not touch); with five MPS seats plus HPSM seats, only slots 2 and 3 are usable. Expect queueing. Load1 read 9.97 at 11:30, 5.15 at 11:39.
- **R23 (`Datasec/MPS-R23`, pane `%315`) is now live** (it was not at the start). Its Yours list (records root files, `.tools/b509`, Jira MPSCALC one ticket + six comments) is disjoint from all five briefs; each brief names it from both sides. Live panes at 11:46: `%0 tuesday`, `%1 fleet-monitor`, `%316 Datasec/HPSM-POC-H1`, `%315 Datasec/MPS-R23`, `%314 Datasec/HPSM-POC-R22`, `%313 Datasec/HPSM-POC-F3`. Each brief carries the list measured at its build and a "re-measure at start" order.

## Tickets: kept, narrowed, dropped (with why)

Per-ticket reproduction is in each brief's census section (file:line at main). "Reproduces" is by code reading and the cited line; nothing was run.

**B517 / M1 (docs and contract words):** MPSCALC-127 keep (ENGINE.md:60). -219 keep (5 of 6 sub-items reproduce; IMPORTER.md:16 sentence not reproduced, left). -290 keep, **docs half only** (narrow the API.md:262 sentence; `PricingPolicy.cs:71-74` untouched; the ticket's other fix is an unruled behaviour change). -312 keep (server accepts readyToExport: `QuoteFigures.cs:149,227,287`; stale words in 5 places). **-195 narrowed to ONE residual** (B161-16, the `fleet[n]` = line number sentence; negatives, what-if/reason and the owner sentence are already corrected at main; the rate-limit parenthesis is a choice and the parity figure is an addition: back to the records seat for re-scope). **-200 DROPPED: already fixed** (`294` absent from IMPORTER.md, care rows restated at :121/:127, A3 gap explained at :116).

**B518 / M2:** all six keep: -215 (`PurchaseValidation.cs:25` `$` anchor; inventory PATCH answers 404 at main, not the ticket's 400: not changed, flagged), -216 (`ApiJson.cs:24` + store-before-audit at `QuoteEndpoints.cs:84/89`), -210, -217, -196 (the two Blocking issues exist only inside `DealUsageOf`), plus **-230 added** (ruling below).

**B519 / M3:** -197 keep (`PricingPolicy.cs:76-79,110` `First()`; fix = judge every request line; **NOT** a save-time refusal of repeated numbers, which the ticket gates on a hosted count nobody may run), -211 keep (tests only), -104 keep (tests only; E-A2 mutant built in the mutant tree). **-310 DROPPED:** it needs a src seam in `QuoteEndpoints.cs`/`QuoteFigures.cs` (B518's file); re-lane after B518.

**B520 / M4:** -190, -191, -192 keep; -193 keep (B157-10 may carve out if it needs `Program.cs`); **-189 NARROWED** to the fail-open state word (the case/Unicode-twin id rule is a choice nobody ruled: question for Tuesday). **-92 DROPPED: already fixed** (catch filters `IsDocumentFault` at `SourceDocumentChecks.cs:149,179`; the brief asks the seat to census it once and add it back as a sixth commit only if a probe shows it reproduces). **-99 DROPPED:** reproduces (`SourceLifecycle.cs:549,598`) but the fix makes `Step` async and the callers are `SourceAdminEndpoints.cs` (no lane owns it), Minor, DevStub-only; re-lane with that file.

**B522 / M16:** MPSCALC-229 only (ruled; disjoint from M1-M4 and every screen lane: `Proposal.cs` + new test file + the rows of `B103DealUsageProposalTests.cs` the ruling contradicts).

## Where the two rulings landed (quoted verbatim in the briefs, with the card's `ruled_ts`; the user reported "11:25", the store says 11:26:24 and 11:26:27)

**Card `mpscalc-deal-usage-edge-rules-1023`**, choice a *"Accept all three recommendations"*, ruled 2026-10-23T11:26:24.632638+11:00; option detail *"Lane D builds them with tests; any new wording still comes to you first."* Its three recommendations (BLUF, verbatim):
1. *"(1) The one-pager repeats the same mono and colour pair per device class and its six-rate cap hides rows with four or more classes (MPSCALC-228): recommended, one combined pair per deal."* -> **NOT in B517-B522.** It is not disjoint from the serial lane S1: `ProposalUsageRate.deviceClass` is `required` in the contract (`openapi.json:1884`, `Dtos.cs`), the one-pager and full proposal print a "Device class" column (`OnePager.tsx:307-316`, `ProposalDocument.tsx:417,500`), and `Proposal.cs:525` builds the rows. So it is a contract + words change in **S1**, after B517 and after B522 (B522 and S1 both edit the same `CopyPurchase` block). Named in the partition of all five briefs as "not yours".
2. *"(2) A colour rate prints for a class with no colour pages (MPSCALC-229): recommended, print a colour rate only for classes with estimated colour pages."* -> **B522 / M16** (new lane; `Proposal.cs` only, no contract, no words). Interplay with (1) recorded: after the pair is combined it reads "the deal's colour row prints only when the deal has estimated colour pages".
3. *"(3) A deal whose only device is optional calculates and prints a proposal with no rates (MPSCALC-230): recommended, block it like the empty-quote rule."* -> **B518 / M2** (`QuoteEndpoints.cs:1440` `IsEmpty`/`EmptyQuote`, "Add at least one device." reused byte for byte; the seat chooses where a counted device can be known).

**Card `mpscalc-rental-credit-authorisation-1023`**, choice a *"Any credit raises a Review issue and an Approver must approve it"*, ruled 2026-10-23T11:26:27.945438+11:00; detail *"The plan's recommendation: a visible negative line, a Review issue, an authorisation step."* (MPSCALC-261, T-V4-12). -> **NOT in B517-B522; belongs to serial lane S2** (and its approval step to S1): 261's Where is `Engine/Input/QuoteInput.cs`, `PurchaseInput.cs`, `Calculation/QuoteCalculator.cs`, `PurchaseCalculator.cs`, `WorkbookRules.cs`, `ENGINE.md` (S2's list) and the approval path (`QuoteEndpoints.cs`, S1/M2). It is tier 1, lane V4 wave 2. B518, B519 and B522 carry the ruling verbatim in their partitions as "not yours, do not build". Ready-to-paste carry text for the S2 brief (and S1 for 228) below.

### Carry text for the future serial briefs (not written by me)

**S1 (add):** "RULED 2026-10-23T11:26:24.632638+11:00 (live board, the product owner's choice a, "Accept all three recommendations"): (1) "The one-pager repeats the same mono and colour pair per device class and its six-rate cap hides rows with four or more classes (MPSCALC-228): recommended, one combined pair per deal." Build with tests; the contract (`ProposalUsageRate.deviceClass` is required) and the printed 'Device class' column change with it, so the new column wording is a WORDS-DRAFT for the words gate ('any new wording still comes to you first'). Lands after B517 and B522 (same `Proposal.cs` block)."

**S2 (add):** "RULED 2026-10-23T11:26:27.945438+11:00 (live board, choice a): 'Any credit raises a Review issue and an Approver must approve it' (MPSCALC-261, T-V4-12: a visible negative sell line, a Review issue for any credit, an authorisation step; the approval step touches the Approver path in `QuoteEndpoints.cs`, which S1 owns). Red-first, a calculation-register row in ENGINE.md for the new rule, tier 1, G1 Opus."

## What each brief contains (the template)

Cloned from B510 (today's standing lines) and B484/B509 (MPS conventions): REFUSE AT ONCE with controls (stamp-slot count, main/compare, branch and tree absence, open PRs, `gh` account, port block with a lsof positive control, fact checks that can fail against `git show e027ebd0:<path>`; I ran every fact string against the tarball, each counted exactly 1); the commission per ticket with red-first and boundary/property rows; named mutants with sha256 restore; property checks by program (paths, no skip, test-name multiset lost 0, non-ASCII, person/id scan, gitleaks with canary, hosted-host scan); the CI line once at the final head (`dotnet build -c Release` 0 warnings, `dotnet test --no-build`, web `npm ci`/lint/test/`VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`); heavy-slot convention (`<project>/.tools/heavy-slot-1..3`, stale `B483` holder reported not touched); no provider matrix in MPS (stated); the one known timing-sensitive test; WORDS-DRAFT rule (merge to main is not a deploy; nothing ships before the words gate); CodeQL standing line (branch only, Tuesday opens the PR non-draft and lands by squash with the head pinned); partition from both sides (the other four lanes, R23/B509's Yours list, the screen's M5-M15, serial S1/S2, HPSM and Composer seats); intersection program with controls; STATUS sections; final-line forms (`READY FOR QA` / `STOPPED: NEEDS TUESDAY` / `BLOCKED`).

## Merge order I recommend

B517 first (S1 and S2 wait for it). B518, B519, B520, B522 are pairwise disjoint and disjoint from B517 (any order; B522 before S1). The only soft coupling: B518 and B522 each define "counted device" (X-25) privately; both briefs say to keep their own predicate and to state in DESIGN that the two are equal.

## Things for you to decide or know

1. The B522 number clash above.
2. The ENGINE.md register-row deviation for MPSCALC-196 (Tuesday inserts the row after B517).
3. Hosted count of repeated BOM line numbers (B519 does not refuse repeated numbers at save): yours to commission if you want the refusal.
4. MPSCALC-189's case/Unicode-twin id rule (a choice; B520 pins today's behaviour with one row and asks you).
5. Inventory PATCH answers 404 for a malformed key (ticket 215 expected 400): B518 reports, does not change.
6. B518's new 400/409 sentences (null-entry paths, "Add at least one device." reuse) and B520's possible content-refusal sentence are WORDS-DRAFT: they come back in the seats' STATUS for the product owner's words gate; nothing deploys before it.
7. After the squash, the regenerated client header names a branch sha not on main (the old B163-6 artefact); B517 says so and does not chase it.
8. Drafter did not run `usage_gate.sh`; model lines carry the brief's "gauge 89% (Tuesday no-90% grant)" as instructed.

SELF-CHECK: the ten brief files re-read (M1 whole; the others by section); `cmp` brief vs `.pre-stamp` equal for all five; underscore count 8 each; no person name (the only `Kam*` hits are the `gh` account name and the scan word list); no decision-card id outside the quoted rulings; no card id or Jira key is required in code, commits or tests by any brief.
