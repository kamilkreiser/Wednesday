# B1755 drafter commission — MPS hosted deploy kit RE-CUT for main 50d2a471 (after the settings-file fix landed) (SEAT-D68)
Commissioned by Tuesday (s294), 2026-11-19. Drafter model: OPUS (routing row C8's exception: the kit is for a deploy whose
infrastructure apply replaces every app setting of a hosted site). You DRAFT a kit and a card-facts sheet; you deploy
nothing, run no `az`, and send no request to any hosted host.

## What you write (three files, all under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`)
1. `2026-11-19_B1755_SEAT-D68_mps-hosted-deploy-main-50d2a471.md` (+ `.measured` sidecar): ONE deploy kit, a RE-CUT of
   `2026-11-19_B1749_SEAT-D67_mps-hosted-deploy-main-317bbb14.md` (read it WHOLE with its report
   `2026-11-19_B1749_DRAFTER-REPORT.md` and its commission `2026-11-19_B1749_DRAFTER_COMMISSION.md`: the commission's
   SCOPE, REQUIRED and HOW sections bind you unchanged except where this file says otherwise) in the form of the last
   real run `2026-11-16_B1607_SEAT-D63_mps-showcase-deploy-main.md` and its STATUS in the MPS project
   (`1_Project_Definition/Briefs/2026-11-16_B1607_STATUS.md`: Corrections, Deviations and every STOP first).
2. `2026-11-19_B1755_CARD-FACTS.md`: the facts for ONE decision card to the product owner (Tuesday writes and posts the
   card, you do not): see "The card-facts sheet" below.
3. Your drafter report as TEXT in your reply (Tuesday saves it).
Follow `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` whole (read its newest sections of
2026-11-19). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s294/d1755/` only.

## What changed since B1749 (each read at source by Tuesday today; re-read each yourself)
- **Main is `50d2a47195957a8b0c914ab2972d0dc703f9bee3`** (Tuesday, `gh api` 20:14:39). Three squashes sit on top of the
  commit B1749 pinned (317bbb14): #218 `e036c966` (one refusal sentence in the Api says UTF-16 code units, MPSCALC-316),
  #219 `73eef991` (the purchase result shows the server's projection table to callers who receive it, MPSCALC-267:
  six web paths), #220 `50d2a471` (the settings-file fix: seven infra, test and docs paths). The hosted site was last
  deployed at 5e800095 (RELAYED from the 16 November records; the seat measures it first).
- **The product owner's ruling that governs now:** card `mps-deploy-apply-would-remove-feedback-setting-1119`, ruled a at
  2026-11-19T18:39:18 ("Fix the settings file first, then deploy once"; option detail: "A small reviewed code change puts
  the feedback setting into the file and pins the sign-in ids and the budget date, so the step changes only what you
  approved. It merges, then I bring you one new deploy card with the measured before-and-after comparison. Nothing
  deploys tonight."). Read it with `decision_queue.sh show <id>` and quote it from the store. The earlier card
  `mps-hosted-deploy-main-317bbb14-1119` (ruled a at 18:00) is marked NOT DEPLOYED and superseded: its ruling is NOT an
  authority for this kit. **There is NO ruling yet for this deploy: the kit's COMMISSION slot stays empty for the NEW
  card's tap, and the kit REFUSES at Step 0 without it.**
- **The fix as landed** (read the seven files at 50d2a471): `MpsCalc__Feedback__Path` is in `infra/modules/showcase.bicep`;
  both client id parameters have no default and length 36; `infra/env/showcase.bicepparam` reads both id variables with no
  fallback; `budgetStartDate` defaults to the literal `2026-10-01`; `infra/env/showcase.app-setting-names.txt` lists the
  18 names; `infra/tests/test_infra.py` pins them.
- **The independent review of the fix** (`2026-11-19_B1754_verify/VERDICT.md` and
  `2026-11-19_B1754_verify/FOR-THE-DEPLOY-CARD.md`: read both WHOLE). Its ten measures ARE this kit's pre-write and
  read-back checks; carry every one as a numbered step with its expected reading and its STOP. Its finding F1 binds the
  kit: the id rule is a LENGTH rule, so the seat compares each supplied id BY HASH with the live `AzureAd__ClientId` and
  `MpsCalc__Spa__ClientId` before the what-if, and STOPs on any difference; the ids are taken in memory from the live
  settings, never printed, never written to a file. Its F3 and item 8: the budget's behaviour on an update with the same
  past start date is UNMEASURED and the budget and the settings resource have no dependency: the kit says what the seat
  does if the deployment ends Failed on the budget (read every live name and value hash back first; STOP; never retry).

## Scope of the deploy the kit describes
- Commit `50d2a47195957a8b0c914ab2972d0dc703f9bee3` and NO other; main moved at Step 0 = STOP and ask. Pin the CI package
  by commit (`scripts/deploy-from-ci.sh`, as B1749's report finding 6 read it: re-read the script at 50d2a471); name the
  CI run of 50d2a471's own push to main and its artifact with its expiry (the run may still be in progress when you
  read: then the kit's Step 0 waits for it and STOPs on a non-success).
- The infrastructure apply WITH the measured comparison: names and a hash of each value before (never a value), the
  what-if, the predicted difference stated as exactly "added `MpsCalc__Templates__Path`; removed none; changed none";
  ANY other difference = STOP with the list, the apply does not run; the same dump after, compared by program with two
  controls. The live names must equal the committed list minus the templates path BEFORE the apply (review measure 1).
- Run once WITHOUT the id variables before the real what-if: it must stop at the parameter file before any request
  (review measure 5; the first live proof of the refusal).
- Order of apply and package swap, the backup, roll forward only, the way back, one restart: as B1749 decided unless the
  new main changes the reasoning (say so if it does).
- **What rides along, listed for the card:** every commit between the deployed 5e800095 and 50d2a471 (list them all by
  program with one plain line each, and mark which change what a user of the hosted site SEES). In particular #219: an
  internal-only table with TEN NEW WORDS the product owner has not seen (the word pack is
  `<MPS project>/1_Project_Definition/Briefs/2026-11-19_B1746_WORD-PACK.md`: read it; C-45 at CLARIFICATIONS.md line 654
  says new customer-facing words come to him as a word pack before they ship). State from the code who can see that
  table on the hosted site (the review B1752 found only a caller with internal-metrics is sent a projection:
  `2026-11-19_B1752_verify/VERDICT.md`), and whether any hosted persona has internal-metrics.
- The three seller checks: the expired test login's renewal is the product owner's own separate step (his rulings of
  2026-11-12 and 2026-11-16, and the superseded 18:00 card's option text). The kit does NOT assume they are skipped: it
  carries a slot `SELLER-CHECKS` that Tuesday fills from the NEW card's ruling (run / skipped by ruling).
- The template create-and-list check (MPSCALC-372's acceptance) needs a signed-in Seller, Approver or Administrator and
  the only machine login is expired (B1749 report finding 5): the kit carries a slot `TEMPLATE-CHECK` (run with a named
  caller / not run, the store proven by the start log and the settings only) that Tuesday fills from the NEW card.
- Subscription scope (B1749 report finding 4): state exactly what is written outside the resource group (the
  subscription-level deployment record; the resource group and its tags re-asserted) from `infra/main.bicep` at
  50d2a471 and the review's compiled-template comparison.
- The Azure login: the 16 November seat used the project's own `az` USER login under the project `AZURE_CONFIG_DIR`
  (B1749 report finding 7). The kit's Step 0 checks it read-only (`az account show`: tenant and subscription equal the
  kit's), and an expired or absent login is a STOP that goes to the product owner as a pasteable `az login` line, never
  a workaround, never another identity.
- Model for the deploy seat: OPUS. Records and tickets are a later records pass, not the seat's.

## The card-facts sheet (`2026-11-19_B1755_CARD-FACTS.md`): plain words, no ids of ours, every line with its instrument
For each: the fact, MEASURED (by whom, how, when) or RELAYED (from which record) or UNMEASURED.
1. What deploys: the commit, and the list of what rides along since the last deploy, each in one plain line, with what a
   user of the hosted site sees differently (if anything).
2. The settings difference: measured against the names SAVED ON 16 NOVEMBER (not a live read): added the template place,
   removed none, changed none when the same two ids are supplied. Say plainly that the live site is read by the deploy
   BEFORE any write and that any other difference stops it.
3. What the fix does and does NOT guarantee: the two ids can no longer be blank; a WRONG id would still change four
   sign-in settings, so the deploy compares them by hash first (review F1).
4. What is still unmeasured until the deploy's own what-if: Azure's refusal at apply time; the budget service on an
   update; today's live settings.
5. The ten new words of the internal table (list them from the word pack, with where each shows and who can see it).
6. The decisions the card must carry as options or sub-choices, each with the drafter's recommended default and its
   reason: (i) deploy now / not; (ii) the three seller checks: run after he renews the test login, or skipped again;
   (iii) the template check: with which caller, or not run; (iv) the words: approved as written, or the deploy waits.
   Keep it to ONE card: say how these fit one decision with at most four options.
7. What the product owner must DO himself, if anything, as literal steps (for example an `az login` line if the login
   has expired: mark it "only if the seat reports the login expired").

## Limits (as B1749's HOW, repeated)
Read-only everywhere except your three outputs and your scratch. Project:
'/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' (code at origin by `gh api -X GET` under the
project's own GH_CONFIG_DIR, account kamilDatasec; the local checkout is stale). NO `az` command of any kind, no request
to any hosted host, no deploy, no build, no mail, no Jira write (Jira GET allowed, credentials by name in-process).
`decision_queue.sh` only with `show` and `list`. NEVER read `.local/`, `Source_Documents/**`, a price book or any secret
value; NEVER print an Entra client id or the second column of a saved settings file (first column only; values compared
by boolean or hash in-process). Nothing of HPSM-POC or any other project. No `cd`; no unquoted word starting with `=`;
absolute single-quoted paths; never delete; clocks from `date`; every zero with a positive control; every total
recomputed by program from its parts; a test or command selector checked against the names it must match.
`stamp_check.py <kit>` must exit 0; Stamp slots unfilled; ASCII; built whole, temp file, `os.replace`.
First line of your reply: `STARTABLE: YES|NO - why` (YES means: startable once the new card is ruled and the slots are
filled). Then: files; the ride-along list; the predicted settings difference; the STOP list; what differs from B1749
and why; corrections to this commission; D/Q defaults; UNMEASURED.
