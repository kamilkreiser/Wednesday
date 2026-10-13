# DRAFT · MPS Commercial Calculator · hosted deploy pack: bf60fe83 → main 37f3b3ec (+ B83 slot)

**For:** Friday (laptop coordinator). Datasec / MPS Commercial Calculator only. **Status:** DRAFT, read-only measurement; nothing deployed, nothing posted.
**Measured:** 2026-10-13, ~19:30–19:45 AEDT. Project: `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`.

## 0 · Targets (measured)
- `git ls-remote origin refs/heads/main` = **`37f3b3ec27ac5585ec5606b18c2f1f36336f659d`**.
- Local clone **does not have `37f3b3ec`** (`cat-file -t` fails; local `origin/main` = `33f2cb41`). No fetch was run. So:
  - the commit list comes from the **GitHub compare API** (`compare/bf60fe83...37f3b3ec`): `status ahead`, `ahead_by 5`, `behind_by 0`, base `bf60fe83c02c703d5df11253629b268d25c78ab0`;
  - file:line references are read from the local commit **`e776635`** (PR #38's head). This is valid because **`37f3b3ec^{tree}` (GitHub API) = `e776635^{tree}` (local) = `098f46d1b83c069ead9358c86dc3a6df01334d3b`**. Same tree, same files, same lines.
- Main CI: run `38368593223` = `ci`, head `37f3b3ec…`, `push`, `main`, **success**. All 8 check runs on `37f3b3ec` are `success` (package, CodeQL actions/csharp/python/javascript-typescript, web, dotnet, python).
- Open code-scanning alerts (GitHub API, `state=open`): **0**.
- Hosted = `bf60fe83` is **not measured by me**. It is B73's record (`Briefs/2026-10-13_B73_STATUS.md:1-12`, feedback store ON at `MpsCalc__Feedback__Path=/home/data/feedback/`).

## 1 · SHIPS SINCE HOSTED: 5 commits, 5 PRs
`git log --oneline bf60fe83..37f3b3ec` could not run locally (sha missing). This is the compare API's list, oldest first, in the same one-line form:

```
553e7dc2 B74: overlay writer queue tests: arrival order and in-memory turns (MPSCALC-98, gate B71 Z-3) (#34)
13d8fd8b B75+B77: blank overlay author (whitespace/invisible) refused at read and write; OpenAPI retry prose (MPSCALC-100, -101) (#35)
d6361472 B80: itemised price summaries site-wide (rental parts, purchase class subtotals) — gate B84 GO WITH NOTES (#36)
33f2cb41 B85: rental parts shown in cents that always add up (R-28), guards E-3a + E-3c — gate B87 GO WITH NOTES (#37)
37f3b3ec B79+B86+B89: two proposal print buttons (short-form one-pager + full PDF), itemised rental proposal, home tiles fill the row — gates B88 + B90 GO WITH NOTES (#38)
```

| PR | Merged (UTC, API) | What | Gate verdict (source) |
|---|---|---|---|
| #34 `553e7dc2` | 2026-10-12 23:57:22 | B74: tests only (overlay writer queue) | **No tier-1 gate.** PR body: *"Tests only (tier 2; Friday reviewed at source)."* No B-gate STATUS names B74. |
| #35 `13d8fd8b` | 2026-10-13 01:42:57 | B75 + B77: an author that shows nothing is refused, at read and at write; OpenAPI retry text | **B76 GO WITH NOTES** (round 1, `B76_STATUS.md:1`, `:8`); **B78 GO WITH NOTES** (round 2 of 2, `B78_STATUS.md:1`, `:8`) |
| #36 `d6361472` | 2026-10-13 04:10:51 | B80: itemised price summaries site-wide | **B84 GO WITH NOTES** (`B84_STATUS.md:1`, merge `:11`) |
| #37 `33f2cb41` | 2026-10-13 06:30:43 | B85: rental parts in cents that always add up; guards | **B87 GO WITH NOTES** (`B87_STATUS.md:1`, merge `:11`) |
| #38 `37f3b3ec` | 2026-10-13 08:20:26 | B79 + B86 + B89: two print buttons, one-pager, itemised rental proposal, home tiles fill the row | **B88 NO GO** (round 1, G-1, `B88_STATUS.md:1`) → B89 fix → **B90 GO WITH NOTES** (round 2 of 2, 0 blockers, notes N-6…N-8 Low; `B90_STATUS.md:1`, merge `:7`) |

Diff `bf60fe83..37f3b3ec`: **64 files, +6,228 / −66** (local `git diff --stat bf60fe83 e776635`, same tree).

### Slot: B83 feedback attachments (after gate B91)
- Branch `b83/feedback-attachments` = **`6cae6be0d38d5f38a6c323d27f9a9f7cabe23be9`** (`ls-remote`). Seat says READY FOR GATE (`B83_STATUS.md:327`).
- Gate B91: brief and evidence folder exist; **no `B91_STATUS.md` yet**. Verdict: ______ (fill after B91).
- PR / merge sha / main CI: ______.
- If B83 joins this deploy, the new main sha replaces `37f3b3ec` everywhere in this pack, and the card id changes with it.

## 2 · Migrations, settings, store formats (measured on the same tree)
| Check | Result |
|---|---|
| Migration steps: `git grep -n -i migrat e776635 -- src` | **0 hits** (rc 1) |
| `infra/`, `scripts/`, `.github/`, `tools/`, `package.sh` changed in range | **none** (empty `diff --name-only`) |
| `appsettings*.json` changed in range | **none** (empty `diff --numstat`) |
| Setting keys read by code (`"MpsCalc:…` in `src`) | **identical set** at `bf60fe83` and at main (13 keys; no new setting) |
| Overlay format string | unchanged: `"mpscalc-catalogue-overlay/1"`, `CatalogueOverlayStore.cs:25` at both |
| Feedback format strings | unchanged in range (`FeedbackStore.cs` not in the diff): `mpscalc-feedback/1` `:21`, `mpscalc-feedback-ticket/1` `:35` |
| `QuoteFileStore.cs`, `ApiJson.cs` | not in the diff (snapshot reading rules unchanged) |
| API contract version | `0.3.0-b17` → **`0.5.0-b85`** (`docs/api/openapi.json:5`) |

**What does change in stored data and reading:**
1. **Overlay read and write rule** (`src/MpsCalc.Api/Inventory/CatalogueOverlayStore.cs`, +75/−1, B75+B77): an audit author made only of characters that show nothing is now **refused at boot** (`WellFormed`, `IsMissingAuthor`, 21 written-out ranges), and the store **refuses to write** such a document (new check in the write path). The format string is unchanged, but a hosted `overlay.json` with such an author would stop the site starting. **Pre-swap check: PRE-1 must be the B75 amended version** (`B75_STATUS.md:104-127`; file `Briefs/2026-10-13_B75_evidence/pre1_amended.sh`), which supersedes B69's. B73 found no `overlay.json` on hosted at its backup (`B75_STATUS.md:15-17`, citing `B73_STATUS.md:9`). Whether one has been written since then is UNMEASURED.
2. **DevStub sign-in** (`src/MpsCalc.Api/Infrastructure/DevStubAuth.cs`, +2/−1): a blank or invisible user header is refused. This is local dev-stub only; hosted uses Entra.
3. **Quote and snapshot files gain optional members** (B80: `CalculationResult.cs` +48, `PurchaseResult.cs` +25, `Contracts/Dtos.cs` +88, new `MonthlyParts.cs`; B85: the `…InCents` members). There are no format-string changes, and every new member is optional, so old files load (`B80_STATUS.md:95-100`). **Forward is safe; rollback is not (E-2 below).**

**E-2, quoted from B84's STATUS (`Briefs/2026-10-13_B84_STATUS.md`):**
- `:51` *"**E-2 (ticket, High for operations, does not block merging): rollback to pre-B80 code hides every quote submitted or approved under B80.**"*
- `:52` *"Base reads snapshots with `UnmappedMemberHandling.Disallow` (`ApiJson.cs:20`, `QuoteFileStore.cs:365`). It refuses each head-written snapshot, then refuses the quote that refers to it (`QuoteFileStore.cs:411`). The result is 404 and a log line; files stay on disk."*
- `:53` *"Drafts survive the rollback. Re-deploying head brings the hidden quotes back."*
- `:54` *"This belongs in the hosted-deploy card as a pre-deploy item."*
- `:222` *"The hosted deploy card should state: "after this deploy, rolling back to pre-B80 code hides every quote submitted or approved since. Roll forward, or restore with a B80-aware reader.""*
- And the pre-B80 side, `:213`: *"On screen: S1 shows the total and *"Breakdown not available for this calculation."* (`PriceBreakdown.tsx:66`). S5 and both S9 rows show it too (3 notes). The proposal renders (12 pages)."* (At main this string is `web/src/components/PriceBreakdown.tsx:74`.)
- Gate B87 reproduced E-2 on B85 (`B87_STATUS.md:9`, `:348`): *"The pre-deploy note on the hosted card should now say "pre-B85" as well as "pre-B80"."*

**What this means for this deploy (my reading of the above, not a new measurement):**
- The rollback target for this deploy is `bf60fe83`, which is **pre-B80 and pre-B85**. So E-2 applies in full.
- Every **existing** hosted quote is pre-B80. After the deploy, approved and submitted quotes show *"Breakdown not available for this calculation."* and their purchase document keeps its old tables. Drafts show a breakdown after their next calculation.
- There is also B84 E-6 (Low): pre-B80 data gives empty part cells with no note in S2 and S6 (`B84_STATUS.md:214`).
- B87's E87-3 (pre-B85 calculations keep B80's cent display) **cannot occur on hosted**, because hosted goes straight from pre-B80 to B85. No hosted quote can be stored with B80-only parts.
- **B83 slot:** if B83 ships, its own rollback note applies too (`B83_STATUS.md:102-105`). Pre-B83 code refuses every `/2` feedback item at start: it names each one in the log, nothing is lost, and the items come back on roll-forward.

## 3 · NEW WORDS for Kam's words card (at main `37f3b3ec`; file:line read on the identical tree `e776635`)
Approval sources searched:
- `1_Project_Definition/CLARIFICATIONS.md`: 380 lines. It has **no entry** for the one-pager mock, for B79's button words, or for B80's labels.
- `Design/2026-10-12_one-pager/NEW_WORDS.md` §A, approved with card `mpscalc-one-pager-mockup-1012` = **a** (`decisions.json`, ruled 2026-10-12 18:04:07). Strings from it are marked **APPROVED (mock)**.

Count: **26 new strings. 9 APPROVED (mock), 17 NOT YET APPROVED.** Existing words reused in new places are listed separately in §3c and are not counted.

### 3a · NOT YET APPROVED (17)
| # | String (verbatim) | Where at main | Listed by | Approved? |
|---|---|---|---|---|
| 1 | `Short-form proposal (PDF)` | `web/src/screens/ProposalPage.tsx:21` (button) | B79 STATUS NEW WORDS; B88 §8 | **No.** Built from Kam's 12:31:16 request ("short form proposal"), not his verbatim words and not in the mock |
| 2 | `Full proposal (PDF)` | `web/src/screens/ProposalPage.tsx:22` (button) | B79 STATUS; B88 §8 | **No as written.** The mock's #2 `Full proposal` was approved for a switch that was not built; ` (PDF)` is new |
| 3 | `Short-form proposal` (aria-label) | `web/src/proposal/OnePager.tsx:134` | B79 STATUS; B88 §8 | No |
| 4 | `Base charge (device and service) / month` | `web/src/components/PriceBreakdown.tsx:58` | B80 §10 (offers `Hardware / month` as an alternative on the card); B84 §9 | No |
| 5 | `Mono print / month` | `PriceBreakdown.tsx:60` | B80 §10; B84 §9 | No |
| 6 | `Colour print / month` | `PriceBreakdown.tsx:61` | B80 §10; B84 §9 | No |
| 7 | `Options are included in the base charge.` | `web/src/screens/PriceView.tsx:143` | B80 §10; B84 §9 | No |
| 8 | `Hardware, ex GST` | `PriceBreakdown.tsx:66` | B80 §10; B84 §9; B86/B88 reuse | No |
| 9 | `Software, ex GST` | `PriceBreakdown.tsx:67` | B80 §10; B84 §9 | No |
| 10 | `Supplies, ex GST` (only when not zero) | `PriceBreakdown.tsx:68` | B80 §10; B84 §9 | No |
| 11 | `Services, ex GST` (only when not zero) | `PriceBreakdown.tsx:69` | B80 §10; B84 §9 | No |
| 12 | `Other, ex GST` (only when not zero) | `PriceBreakdown.tsx:70` | B80 §10; B84 §9 | No |
| 13 | `Package price by class` (customer PDF §5 heading) | `web/src/proposal/template/sections.ts:443` | B80 §10; B84 §9 | No |
| 14 | `Breakdown not available for this calculation.` | `PriceBreakdown.tsx:74` | B80 §10 + §5; B84 §5, §9 | No. **On hosted, every existing approved or submitted quote will show it** (§2) |
| 15 | `Monthly charge breakdown` (aria) | `PriceView.tsx:142` | B80 §10; B84 §9; B88 §8 | No |
| 16 | `Purchase total breakdown` (aria) | `web/src/screens/bom/PurchaseResultView.tsx:149` | B80 §10; B84 §9; B88 §8 | No |
| 17 | `Section {n} total by class` (aria) | `web/src/screens/bom/PurchaseBomEditor.tsx:202` | B80 §10; B84 §9 | No |

The Kam card for B85's rounding (`mpscalc-rental-parts-cents-rounding-1013` = a) said "No new words". It does not approve labels 4–6. B85, B86 and B89 each declare **0 new words** (B85 `:222`, B86 `:300`, B89 `:136`), and gates B87 (`:7`), B88 (`:11`) and B90 (`:6`) confirm 0 undeclared.

### 3b · APPROVED (mock) (9): one-pager `NEW_WORDS.md` §A, card `mpscalc-one-pager-mockup-1012` = a
| Mock # | String (verbatim) | Where at main | Listed by |
|---|---|---|---|
| #7 | `For purchase quotes only: a rental quote has no proposal template yet.` | `ProposalPage.tsx:24` (shown `:295`, `aria-describedby` `:286`) | B79 STATUS; B88 §8 |
| #8 | `MANAGED PRINT PROPOSAL · SUMMARY` | `OnePager.tsx:24` | B79; B88 |
| #9 | `and {n} more packages` | `OnePager.tsx:27` | B79; B88 |
| #10 | `+{n} more` | `OnePager.tsx:28` | B79; B88 |
| #11 | `and {n} more rates (see full proposal)` | `OnePager.tsx:29` | B79; B88 (rendered). **Look item [B79-3]: n = 1 reads "and 1 more rates"** |
| #12 | `Optional items are listed in the full proposal.` | `OnePager.tsx:25` | B79; B88 |
| #13 | `{n} items to confirm before contract` | `OnePager.tsx:30` | B79; B88 |
| #14 | `1 item to confirm before contract` | `OnePager.tsx:30` | B79; B88 (rendered) |
| #15 | ` …` (cut mark) | `OnePager.tsx:26` (`CUT_MARK`; used `:50`, `:63`) | B79; B89; B90 `:6` |

### 3c · Existing words reused in new places (not new; shown so nothing looks invented)
- `Software / month` on `PriceView.tsx:127` (existing card) **and** `PriceBreakdown.tsx:59` (new block row). On S10, `ProposalPage.tsx:82` (card) **and** the block. → **O-3 (known look item): `Software / month` is shown twice** on S1 and on the S10 rental proposal (B80 §10; B86 REPORT 3; B87 `:54`). B86 notes that B85's cents rounding may make the two figures differ by a cent.
- `Monthly charge ex GST` (`PriceView.tsx:121`, `:243`; `ProposalPage.tsx:66`, `:87` as `Monthly charge ex {taxName}`): B80 §10 reuse.
- `Total ex GST` (`PurchaseResultView.tsx:54`, `:187`): B80 §10 reuse (deviation from the brief's sum line, stated there).
- `Class` column (`PurchaseResultView.tsx:48,70,86`; `PurchaseBomEditor.tsx:217`) with values from `CLASS_LABELS` (`InventoryScreen.tsx:16-21`, unchanged since `bf60fe83`): B80 §10; B84 §9 reuse.
- `Package` as the head of the PDF §5 class table (`ProposalDocument.tsx:380`) and `TOTAL {term}-MONTH FLEET PACKAGE` (`ProposalDocument.tsx:383`): **B84 extras** (§9 `:264-265`, "existing words, newly used here"). On the one-pager, `Package` (`OnePager.tsx:192`) and `TOTAL …` (`OnePager.tsx:219`) are mock §B reuses.
- One-pager template strings in a new place: `Commercial Summary and Next Steps` (`sections.ts:22`), `Proposal basis` (`sections.ts:71`), the sub-line `{term}-month support | STANDARD PRICING`, and the aria names `Executive Summary`, `Intended outcomes`, `Recommended next steps`. Source: B88 §8 and mock `NEW_WORDS.md` §B.

### 3d · B83 words (after gate B91)
*(Empty on purpose. Fill from gate B91's NEW WORDS verdict. The seat's own list is `B83_STATUS.md` §12, `:255`; it is not copied here until B91 rules.)*

## 4 · DRAFT card (decision_queue shape; NOT written to `decisions.json`)
Template: `mpscalc-hosted-deploy-bf60fe8-1013`. I kept its fields `id, client_project, title, bluf, default_action, options[key,label,detail], recommended, status, seat` and dropped `prior_rulings_overridden` (it names other clients' cards). There is no `_override_prior`. Friday sets `ts` when posting.

```json
{
  "id": "mpscalc-hosted-deploy-37f3b3e-1013",
  "client_project": "Datasec/MPS-Calculator",
  "title": "MPS calculator: put today's five merged changes (itemised prices, two print buttons, one-pager) on the hosted site, and approve their words?",
  "bluf": "Kam: tap a to deploy main 37f3b3e to the hosted site AND approve the 17 new on-screen words listed below; b deploys but the words are held; c holds everything.\n\nWhat users will see change: every price summary is itemised (rental: base, software, mono print, colour print per month, always adding up to the cent; purchase: hardware, software, supplies, services, other); the Proposal page has two buttons, 'Short-form proposal (PDF)' (the one-pager you approved on 12 Oct) and 'Full proposal (PDF)' (every page); rental proposals are itemised; the home tiles fill the row.\n\nShips since hosted bf60fe8 (5 PRs): #34 B74 overlay queue tests (tests only, Friday review) · #35 B75+B77 an invisible catalogue-edit author is refused (B76, B78 GO WITH NOTES) · #36 B80 itemised summaries (B84 GO WITH NOTES) · #37 B85 rental parts in cents (B87 GO WITH NOTES) · #38 B79+B86+B89 two buttons + one-pager + itemised rental proposal + tiles (B88 NO GO, fixed, B90 GO WITH NOTES). Main CI green, 0 open code-scanning alerts. No migration, no new setting, no infra change.\n\nWords needing your yes (17): 'Short-form proposal (PDF)', 'Full proposal (PDF)', screen-reader 'Short-form proposal'; 'Base charge (device and service) / month' (alternative offered: 'Hardware / month'), 'Mono print / month', 'Colour print / month'; 'Options are included in the base charge.'; 'Hardware, ex GST', 'Software, ex GST', 'Supplies, ex GST', 'Services, ex GST', 'Other, ex GST'; 'Package price by class' (customer PDF); 'Breakdown not available for this calculation.'; screen-reader 'Monthly charge breakdown', 'Purchase total breakdown', 'Section n total by class'. Already approved with the one-pager mock (9): the rental reason, 'MANAGED PRINT PROPOSAL · SUMMARY', the 'more packages/more/more rates' lines, 'Optional items are listed in the full proposal.', the 'items to confirm' lines and the ' …' cut mark. Known look items: 'Software / month' shows twice on the price screen and on the rental proposal (O-3); 'and 1 more rates' is not singular.\n\nBefore you tap, the one-way part: after this deploy, rolling back to the current hosted code hides every quote submitted or approved after the deploy (they return 'not found'; files stay on disk; drafts are fine; deploying forward again brings them back). Roll forward, never back. Today's approved quotes on the site were made before itemising, so they show their total with 'Breakdown not available for this calculation.'; drafts itemise after their next calculation.\n\nGating counts the seat runs on hosted before the swap (any non-zero = STOP, nothing deployed): PRE-1 in its B75 version (an invisible catalogue-edit author would stop the site starting; no catalogue file existed at the last deploy) and P-1. Feedback attachments (B83) are still in their QA gate and are not in this deploy.",
  "default_action": "nothing is deployed; Friday asks again tomorrow",
  "options": [
    {
      "key": "a",
      "label": "Deploy main and approve the words as listed",
      "detail": "Seat F ships main 37f3b3e to the same hosted link after a backup and the PRE-1 (B75 version) / P-1 counts. No setting change; the feedback store stays on. The 17 listed words are approved as written. Rollback target stays bf60fe8, with the rollback warning above."
    },
    {
      "key": "b",
      "label": "Deploy, words held",
      "detail": "Same deploy as a, but the 17 words are not approved: Friday brings a words card with alternatives (for example 'Hardware / month') and any word you change goes through a seat and a gate before a later deploy. Users see the words as built until then."
    },
    {
      "key": "c",
      "label": "Hold",
      "detail": "The hosted site stays on bf60fe8. The five changes stay on main only. Nothing about stored quotes changes."
    }
  ],
  "recommended": "a",
  "status": "open",
  "seat": "friday"
}
```

*(If B83 passes B91 and is merged first, Friday replaces the main sha, the card id, the ships line, the B83 words from §3d and the B83 rollback line before posting.)*

## 5 · UNMEASURED
- **Hosted actually runs `bf60fe83`.** This is B73's record only. I made no hosted probe (no `/health`, no bundle read, no settings read).
- **Whether hosted has an `overlay.json` now.** B73 saw none at its backup. Any catalogue edit since then is unknown, and so is PRE-1's result on it.
- **How many hosted quotes are approved or submitted** (that is, how many will show "Breakdown not available"), and P-1 today.
- **Rollback package for `bf60fe83`**: B73 says it is kept under `.tools/wt-B73-release/.local/deploy-packages/bf60fe83…/` (`B73_STATUS.md:211`). I did not hash or verify it.
- **`git log --oneline` on the local clone**: not possible, because `37f3b3ec` is missing locally and no fetch was run. The list is from the compare API. File:lines are read on `e776635`, whose tree is equal to main's.
- **The words rendered on the hosted build.** The counts and lines come from source plus the gates' renders (B84 §9, B88 §8, B90 §6). Nothing was rendered by me.
- **B83 / gate B91**: verdict, final sha, words, PR and CI. All pending.
- **Whether `Full proposal (PDF)` counts as covered by the mock's approved `Full proposal`.** That is a ruling for Friday or Kam, not a measurement. It is listed here as not approved.
