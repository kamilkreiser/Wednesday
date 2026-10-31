# SWEEP 2026-10-31: MPS Commercial Calculator and Security Composer (read-only)

Method: Jira GET only (search/jql, paged by token; MPSCALC 4 pages, PCOMP 2 pages), credentials read in-process from each project's own env file, nothing printed. Controls: max key equals issue count on both boards (MPSCALC 356 of 356, PCOMP 113 of 113, no gaps/duplicates); status counts add up (342+14, 100+13); comment fetch not truncated (0 issues with total above returned); landed-evidence regex found 0 hits on a planted nonsense term. Classification is by label, comment text and the ruling records; it is evidence-based, not a re-test of any ticket. Jira Backlog status is NOT reliable here: the projects record no rule that moves a ticket on merge, so merged work still sits in Backlog.

## 1. MPS Commercial Calculator (board MPSCALC, repo datasecau/MPS-Commercial-Calculator)

BLUF: of 342 open issues (327 tasks/bugs + 15 epics) only about 61 are real new work; 168 are merged-but-not-closed; the first build lane to start is the V4 engine slice (MPSCALC-254 + -256, both named 'now' in the build plan, rulings D-03/D-04/D-05 already given).

Counts (open non-epic = 327; epics open 15; Done 14; board total 356):
- ACTIONABLE: 61
- NEEDS-RULING: 49 (17 are the original questions-for-owner MPSCALC-68..88; 15 are web screen lanes needing a word pack; the rest are single design/word questions)
- BLOCKED: 10
- DONE-PENDING-RECORD: 168 (comment on the ticket says merged/landed/ruled-record-only; ticket still Backlog)
- UNVERIFIED-SEED (extra class): 39 (MPSCALC-16..65 spec-seed tickets; most are built in part or whole by the shell/engine/API/BOM PRs but have no landing comment; a records seat must check each against main and close or re-scope)
- Check: 327 + 15 epics = 342 open.
- Caveat: the DONE class is by comment evidence (a landing comment names the ticket). A ticket whose comment says only 'merged work names this ticket' may be partly done; the records seat should test each Done-when. Open sweep of keys 90-135 (old, no comment) may include items fixed by later PRs: first step for each is 'measure on main'.

### ACTIONABLE, ranked
Rank 1-9 are the lane starts; the rest are clusters. Size S/M/L is a guess.
1. MPSCALC-254 | [T-V4-3] per-group monthly volume basis | size M | files: Engine/Calculation/PurchaseCalculator.cs, QuoteCalculator.cs, Input/*, docs/ENGINE.md, calculation register (new row) | fix: add basis switch (fleet total or per device) multiplied by quantity once; register row + red-first test; plan lists it as startable now
2. MPSCALC-256 | [T-V4-5] annual figures + projection breakdown | size M | files: Engine result types, QuoteCalculator.cs, docs/ENGINE.md, register | fix: monthly x12 and a projection breakdown in the result; additive figures only; startable now
3. MPSCALC-252 | [T-V4-1] billable device groups with fleet quantity and per-device components | size L | files: Engine/Input/QuoteInput.cs, PurchaseInput.cs, PurchaseCalculator.cs, Api Dtos.cs, openapi.json | fix: sections become groups (D-05 ruled a); includes the purchase-pair test of the version-diff route noted in its comment; gates -253, -255, -257, -269
4. MPSCALC-253 | [T-V4-2] component quantity rules perDevice/fixedPerGroup/manual | size M | files: same Engine input + calculator files as -252 | fix: needs -252 first
5. MPSCALC-258 | [T-V4-7] tier basis: per pool plus quote-level manual override on purchase | size M | files: Engine tier qualification, Input, register, docs | fix: D-03 ruled a; number-changing so tier 1 gate
6. MPSCALC-259 | [T-V4-8] purchase sell basis: markup kept, margin allowed per section | size M | files: PurchaseCalculator.cs, Input, register | fix: D-04 ruled a; still no default margin
7. MPSCALC-261 | [T-V4-12] rental credits and credit authorisation | size M | files: QuoteInput.cs, PurchaseInput.cs, QuoteCalculator.cs, WorkbookRules.cs, ENGINE.md, register | fix: ruled: credit is a visible negative sell line, raises a Review issue, any Approver incl. owner approves, audited (label still says needs-ruling; the ruling is in the ticket comment)
8. MPSCALC-255 / -257 / -315 | [T-V4-4] per-group service fee; [T-V4-6] sites on groups; [B347-7] per-year GP carried on list | size M each | files: Engine result + Api list mapping | fix: -315 needs a result field from -256; -255 and -257 need -252
9. MPSCALC-237 | [T-V0-7] acceptance reference + date on Won; Issued status | size M | files: Api Contracts/Dtos.cs, QuoteEndpoints.cs, QuoteStore.cs, Mapping.cs, QuoteEvents.cs, PriceAudit.cs, openapi.json, API.md, web generated client | fix: D-12 a ruled; Issued status after approval; only on approved unchanged quote. Overlaps -312 and -288 on the contract files
10. MPSCALC-312 | [B347-4] contract words say readyToExport is refused 400; server answers 200 | size S | files: docs/api/openapi.json:81 and copies (snapshot, schema.ts, types.ts), docs/API.md:355-360 | fix: reword the group parameter text; do it in the same contract-sync pass as -237
11. MPSCALC-284 / -285 | [T-V10-2] software billing column; [T-V10-3] governed term column for care packs | size M each | files: Importer (tools/MpsCalc.ImportCli), catalogue map, Engine software pricing | fix: PR #84 importer is landed so V10 is unblocked; tier 1
12. MPSCALC-286 / -287 / -212 | [T-V11-1] approval thresholds as governed settings; [T-V11-2] trading entity defaults; [MPSCALC-212] typical click rates into the same store | size M each | files: Api settings store, Dtos, openapi.json, web hint words file (212 removes values from it) | fix: D-10 a (warnings only) and D-14 c (setting per quote, Datasec default) are ruled; -212 depends on -286/-287; any new screen word still goes through the word pack
13. MPSCALC-269 | [T-V6-1] server template store (versioned, archive instead of delete) | size L | files: new Api store + endpoints, openapi.json | fix: after -252; tier 1
14. MPSCALC-161 | quotes list: owner may archive a quote | size M | files: QuoteEndpoints.cs, QuoteStore.cs, web QuoteList.tsx | fix: default K-16: owner archives a Draft or Rejected quote, hidden from lists, kept on disk; button label is a new word (use existing words or add to a word pack)
15. MPSCALC-343 / -344 / -349 | parity-proof survivors (case-insensitive held set; two sentence-only survivors); csproj comment tie | size S each | files: tools/MpsCalc.ImportCli parity-proof tests, src/MpsCalc.Api/MpsCalc.Api.csproj:31-34 | fix: test-only row on the importer's synthetic store kills -343 (gate scratch row F13); -344 sentence-only; -349 comment only. -345 (docs word) is NEEDS-RULING
16. MPSCALC-300 / -314 / -317 | [B319-3] quantity audit noise; [B348-2] autosave writes history per typing pause; [B483-Q8] Add section before price list loaded | size S-M | files: web quote screen / autosave hook (shared files: overlap among the three) | fix: one web bug lane; -314 touches autosave and revision counting so tier 2 gate
17. MPSCALC-195 / -200 / -201 / -205 | docs owed (negative inputs, line numbers, rate-limit wording); importer coverage table contradictions; Entra script follow-ups; packaging guard N-6 | size S each | files: docs/API.md, docs/ENGINE.md, docs/IMPORTER.md, tools scripts | fix: pure docs/script chores; the Entra script is run only with an explicit brief
18. MPSCALC-90 / -91 / -92 / -94 / -97 / -99 / -102 / -103 | source-store refusals, overlay mutants, feedback store overlap, lifecycle lock, rollback snapshots | size S-M each | files: src/MpsCalc.Api source/overlay/feedback stores and tests | fix: old gate residue with no comment: MEASURE ON MAIN FIRST; several may be fixed by PRs #99-#132. Overlap: 90/91/92/99/94 all in the source version store
19. MPSCALC-96 / -116 / -118 / -119 / -120 / -127 / -133 / -134 / -135 | e2e stub mode red, census list, stub breakdown fields, infra test fallback, contract version rule, ENGINE.md rounding sentence, pdf evidence, pdfText helper, smoke journey | size S each | files: web/e2e/*, web stub, infra/tests, docs/ENGINE.md | fix: test-infra and docs chores; measure on main first (the stub and e2e files were reworked by later PRs)
20. MPSCALC-106 / -107 / -108 / -110 / -114 / -115 / -117 / -131 / -132 | browser-pricing and colour guards; print and proposal layout (one-pager fit, BOM table cut, rental devices table, 26+ sites, 500 lines) | size S-M each | files: web/src/proposal/*, print CSS, guard tests | fix: layout and guard tests, no new words intended; -131/-132 touch the customer-facing rental book so a word check applies; overlap: 110/114/115/131/132 share the proposal print files
21. MPSCALC-121 / -122 / -123 / -124 / -125 / -126 | feedback form wedge, attachment refusals, upload memory limit, store lock across writes, rollback duplicate item, deploy script rc 0 early | size S-M each | files: Api feedback store + web feedback dialog; deploy script | fix: -121 and -122 add refusal sentences (new words); -126 is deploy-script only and does not deploy anything

Overlaps: V4 chain (-252..-259, -261, -315) all edit the same Engine input/calculator/ENGINE.md/register files: run as one sequential lane, -254 and -256 first. -237, -312 (and the landed -288) share the contract files: one contract-sync pass. -286/-287/-212 share the settings store. Old store/feedback/proposal clusters above share files inside each cluster.

### NEEDS-RULING (default in brackets)
- MPSCALC-68, -69, -70, -72, -73, -74, -75, -76, -77, -78, -79, -80, -82, -83, -85, -87, -88 | the original owner questions (partner product model, brand, build team, relation to the sibling products, price-book cadence and permission, pricing owner and approvers, approval thresholds, rule defects, escalation, service costs, device rules, retention, concurrency, spec re-send, FX, next currencies) | [default: leave open; none blocks the V4 or V0 lanes; ask only -74 (price-book cadence/permission) when a deploy of a refreshed book is wanted]
- MPSCALC-243, -246, -264, -265, -267, -268, -270, -271, -272, -273, -274, -275, -276, -277..-283 | web screen lanes (wizard, Issued queue, group editor, assistant, projection table, site allocation, template screens, review tiles/checklist, proposal formats, help/field help, trading-entity line) | question: approve a drafted word pack per lane? [default: an agent drafts the pack in the lane brief and holds the build until approved; -272/-274 staff-only words are the safest first pack]
- MPSCALC-169 | name field for the source versions behind line markups | question: approve exact field name and contract words? [default: agent proposes name + words in a pack; build after approval]
- MPSCALC-112, -128, -129 | one-pager 'rates' singular sentence; duplicate 'Software / month' label; three untrue rental-proposal sentences | question: approve replacement sentences? [default: agent drafts the sentences; no code until approved]
- MPSCALC-113, -177 | home tiles wrap at mid widths; feedback pill covers content on a phone | question: which layout? [default: 3+3 grid at mid widths; pill moves to bottom-right with a smaller icon]
- MPSCALC-229 | colour rate printed for a class with no colour pages | question: print or suppress? [default: suppress]
- MPSCALC-202, -222, -224, -226 | deploy PRE-1 count scope; rollback past care-pack/staging classes; patched Xml assembly missing in hosted runtime; rollback below item-class change | question: accept roll-forward-only and the Xml residual until the host image updates? [default: accept, record, no code; -202 limit the count to the refusals the boot actually makes]
- MPSCALC-342, -345 | validator survivors residue; importer docs word for the panel check (word pack W-345) | question: accept the survivors as residue and approve the one docs sentence? [default: accept residue; approve sentence after the agent drafts it]

### BLOCKED (named blocker)
- MPSCALC-144: waits on the reviewer supplying the large-format source (ruled: add only after it arrives)
- -149 / -154: phase 2 by ruling (CSV import wizard, fleet template)
- -152: later phase by ruling (meter billing)
- -159: needs promotional/rebate data from the vendor; none in hand
- -181: needs an Azure database resource and money (needs a card); later phase
- -187: hosted production check; needs a hosted-deploy card
- -223: hosted runbook change rides a hosted deploy card
- -225: env file lacks the app client id and hosted host; the product owner must supply
- -260: finance/lease mode waits on lender data; builds nothing now

### DONE-PENDING-RECORD and UNVERIFIED-SEED
- 168 tickets carry a landing comment (or a ruled-record-only/acceptance-met comment: -188, -288, -295, -341). Needs one records seat to close them in bulk once the product owner/coordinator confirms the close rule (the project says no rule moves a ticket on merge; recommend adopting 'Done = merged to main, not deployed', as the Composer board already does).
- 39 spec-seed tickets (MPSCALC-16..20, -23..26, -29..36, -40..55, -57..60, -62..65 as open) need a records check against main before closing.

### Open PRs
- #121 Bump zod 4.6.5 to 4.6.7 in /web (dependabot; updated 2026-10-26)
- #120 Bump undici 8.11.2 to 8.12.3 in /web (dependabot; updated 2026-10-26)
- Both are dependency bumps, not feature work. Not re-checked for CI state in this sweep. Landing rule in the project: seats push a branch only; the coordinator merges after CodeQL is green.
- Last landed: #132 (squash 1a2a0294, 2026-10-27). Main is 1a2a0294; hosted site runs e027ebd0 (relayed in the project history, not probed). Hosted deploys are one card per deploy, so nothing below is deployable without a card.

### Owed items in the coordinator pickup that name MPS
- Word-pack lanes still owed: W-345 (importer docs word), W-169/288 (source-set field name; -288's wording is already ruled and recorded), N-LIMIT; rows -343/-344 were 'not launched' pending a row-cap word.
- Hosted MPS deploys: card per deploy; main is ahead of the hosted showcase (e027ebd0) by PRs #98..#132, undeployed.
- No dated follow-up for MPS remains live (the 10-26 / 10-27 round-cap defaults were all executed and the landings recorded).

## 2. Security Composer (board PCOMP, repo datasecau/Datasec-Security-Composer)

BLUF: of 100 open issues (96 tasks/bugs + 4 epics) the cheapest real work is the L2/L3 sample-policy structure lanes and a records lane (L0-1) on branches; 43 are blocked (19 held by ruling, the content-release chain behind a held draft PR, and the reviewer's answers); 12 are merged-not-closed; merged PRs #88-#105 are not yet on the demo (a demo deploy is available under the push-to-demo grant once each is READY).

Counts (open non-epic = 96; epics open 4; Done 13; board total 113):
- ACTIONABLE: 34
- NEEDS-RULING: 7
- BLOCKED: 43 (of which 19 carry the held label)
- DONE-PENDING-RECORD: 12
- Check: 96 + 4 epics = 100 open. Held label count by program: 19 (matches the board's own 19).

### ACTIONABLE, ranked
1. PCOMP-40..44 | L3-2..L3-6: attribute overrides storage, engagement governance, remediation states, document version/policy, output kinds sm_policy_* | size L (each) | files: packages/db migrations, contract, packages/*, apps/api | fix: structure only; no card needed per the build plan for the storage part; migrations + contract bumps are shared files so run strictly one lane at a time. Screen words (L5) are separate and need the word pack. Branches only; release timing stays with the hold on the content release
2. PCOMP-36..39 | L2-1..L2-4: per-item class, variable values, why/customisation text, solution-compatibility | size M each | files: new data files under content/ (disjoint from the loader) | fix: template approved (C-100 on the record); building on branches is permitted, the release is what is timed; comment on PCOMP-36 says the files stay disjoint from the loader
3. PCOMP-52 | L6-1 (L6-a): PDF table of contents | size L | files: document/PDF generator in packages/ and apps/ | fix: named 'now, no card' in the build plan; check no new customer-facing words (a TOC adds headings only)
4. PCOMP-29 | L0-1 crosswalk: 132 sample rows to SM 3.16 items and the 123 registry controls | size M | files: 1_Project_Definition/Content/ (records only, no code) | fix: one row per sample row with SM ids and flags for the 11 absent and the no-item Self-Healing row; reads the sibling catalogue read-only
5. PCOMP-98 / -102 / -112 / -113 | test-scanner and DEPLOY.md-test residue: cross-line context (16 accepted lost cells), cut-script footer check, year-class setup failure, four row-8 pins unnamed | size S-M each | files: packages/db/test/b778-route-b-script-complete.db.test.ts, DEPLOY.md, date-rule test file | fix: all test-only/words-in-DEPLOY.md follow-ups; these are the round-cap residue the product owner chose to ticket; low value, do after the lane starts. Overlap: all four edit the same Route B test file
6. PCOMP-12 (Bug) / -83 (Bug) | Expert typed editor writes every declared sub-answer at engagement level; Guided-added client gets only the source tenant's consultants (half 1 fixed, half 2 open) | size M each | files: apps/web/src/screens/Discovery.tsx (-12); guided review API (-83) | fix: -83 is marked Blocker in its title; read the open half before starting; -12 latent (both releases declare 0 device-group sub-answers)
7. PCOMP-77 / -82 | mark-all-local action for secret fields (ruled yes); PDF cover date in Sydney time from the brand profile (ruled) | size M each | files: apps/web control screen (-77); brand profile + PDF cover (-82) | fix: both ruled in C-71; -82 needs a column/migration so sequence after the L3 migrations
8. PCOMP-74 / -75 / -80 / -81 | CSS token cleanups (off-guide radii, font half, h4 margins, frame) | size S each | files: apps/web app.css and screens-w*.css | fix: no words; the radius halves already deployed, the font/other halves remain; overlap: same CSS files
9. PCOMP-21 / -23 / -24 / -15 / -26 / -27 / -28 / -66 / -67 / -93 / -16 / -12 / -13 chores | Route B proof for 0020; change-report footer hash; pending Guided start residual; listControls perf; MinIO digest/uid/anonymous pull risks; test-only notes; records amend; docker networks | size S each | files: DEPLOY.md, scripts/ci.sh, compose.yaml, packages/* | fix: measure-first chores; -28 needs a machine allowed to pull; -13 is a not-reproduced close that is the coordinator's call (listed under NEEDS-RULING)

### NEEDS-RULING (default in brackets)
- PCOMP-46 | confirm 'warn, never block' for conditional items | [default: warn, never block]
- PCOMP-9 | tolerate unknown recorded migrations at migrate, or add a down-migration convention | [default: add the down-migration convention; keep the guard]
- PCOMP-11 | ask a shared question once and show 'asked under' on the other items (contract bump + screen text) | [default: approve the screen sentence in a word pack, then build]
- PCOMP-13 | close health-check RED on fresh compose as not reproduced | [default: accept and close]
- PCOMP-49, -50, -51 | L5 screens (words and looks go on cards before any deploy) | [default: agent drafts the word pack per screen; build after approval]

### BLOCKED (named blocker)
- 19 held (label): the Essential Eight mapping review and its content release (PCOMP-19, -20, -91) held until the reviewer's current round ends; the Guided/Expert UX and wording items (PCOMP-68..73, -76, -79, -84..90, -92) held on purpose
- PCOMP-31..35 (L1 content catalogue): the built release is in draft PR #85, held until the reviewer's round ends because a new release makes engagements pinned to the running release read-only
- PCOMP-45, -47, -48 (L4 engine) and -53, -54 (L6 document), -55..57 (L7 export): wait on L1 to L3 landing
- PCOMP-58 (L8 bridge) and -59..61 (L9 round trip on the sibling Security Manager): wait on a cross-project measurement on the sibling product
- PCOMP-94 (L0-2): the five questions sit with the reviewer; the product owner sent them and the follow-up was closed by him ('leave it with me'); no answers on record yet
- PCOMP-6: needs a Datasec SME plus a second person ratification; PCOMP-8: needs the new release cut first
- PCOMP-10, -18, -25, -78: need read-only or write access to the demo VM or a release-signing key configured (operator action)

### DONE-PENDING-RECORD (12)
- PCOMP-14, -17 (PR #89), -22 (PR #96), -62, -63 (PR #90), -95 (PR #92), -96 (PR #93), -97 (PR #94) carry facts-only landing comments and stay Backlog; PCOMP-5, -7, -64, -65 are stale/superseded/info per their own comments. The Composer rule (since PCOMP-99) is 'Done = merged to main, not deployed', moved on the coordinator's instruction: a records seat can move these on that basis.

### Open PRs
- #95 Refuse a second target from Guided expert setup when the policy already holds one (branch b712/composer-setup-target-lock; gated go-with-follow-ups at head 867f3402 per the pickup). Not landed: a board ask on re-running its checks for a code scan has default HOLD. A code scan needs a NEW PR from the same branch (close and reopen), per the pickup.
- #85 (DRAFT) HOLD: L1 SM 3.16 content catalogue; release built, not cut; held until the reviewer's round ends.
- #91 Bump @vitest/mocker and vitest; #86 Bump vite 8.3.0 to 8.3.4 (dependabot).
- Merged and NOT deployed to the demo: #88 to #105 (route B and date-rule tests, DEPLOY.md words, migration 0027 index via #89, contract prefix removal #87/#93, round cap #96). A demo deploy is permitted without a card under the push-to-demo grant once the change is READY (QA gate passed + coordinator check + merged via CodeQL), with backup, rollback and live check; content that makes engagements read-only is excluded.

### Owed items in the coordinator pickup that name the Composer
- The reviewer's answers to the five policy-template questions: the 16:30 follow-up on 10-26 was sent and closed by the product owner ('leave it with me'); no answers are on record, so L0-2, L1 release timing and the E8 mapping still wait.
- Board ask on re-running checks for Composer #95 (default HOLD); an older open setup-card is also listed as open.
- Composer records seat after the latest landing: DONE (records for #105 complete; PCOMP-110/-111 Done, PCOMP-113 filed). Nothing else owed there.

## 3. Recommendation
1. Start the MPS V4 engine lane with MPSCALC-254 and -256 (one builder, engine files only, tier 1 gate), then -252 as the next slice. No ruling outstanding, no words, no hosted touch.
2. In parallel (disjoint repo): a Composer lane on L3 structure (PCOMP-40 first) on a branch, plus a records seat for the L0-1 crosswalk (PCOMP-29).
3. One MPS records seat to close the 168 landed tickets and check the 39 seeds; adopt the Composer's 'Done = merged, not deployed' rule for MPS.
4. Draft the word packs for the web lanes (MPSCALC-272/-274 first, staff-only words) so they stop blocking.
