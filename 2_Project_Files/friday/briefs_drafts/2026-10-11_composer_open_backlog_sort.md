# Composer: every OPEN BACKLOG row sorted into one bucket (2026-10-11)

**Project:** Datasec / Security Composer. **Screen by:** a read-only Friday subagent. Nothing was written in the project tree.
**Rows from:** `BACKLOG.md` at records branch `records/b124` (`git --no-optional-locks show records/b124:BACKLOG.md`). Rulings: `1_Project_Definition/CLARIFICATIONS.md` at `records/b124`. C-62 to C-68 were read in full; the other rulings come from the headings and from the rows' own quotes.
**Code read at:** `4e00d573cc4c1ae215e2aad70e92a08e3218281b`. `ls-remote origin main` = `4e00d573…`. The project's local clone does not hold that commit, so it was fetched into a `git clone --shared` in this session's scratchpad. Every file:line below is `git show/grep 4e00d573`. This morning's screen (at a3502002) was not trusted: every row was re-checked.

## BLUF
- **OPEN rows: 101, not 99.** Friday's count split the rows on every `|`. Two rows have an escaped `\|` in their Item cell, so their State cell moved and they were missed:
  - **#155** ("admin_ews_passwo|rd…");
  - **#305** ("Devic\|e Contr\|ol").

  Splitting on ` | ` finds 301 rows (this matches Friday's count) and 101 that start "OPEN".
- **Bucket counts (101):**
  - **A** (agents can do it now): **49**. 12 of the 49 are marked **A(F)**: Friday chooses between options the row already states, and neither Kam nor Paul is needed.
  - **K** (needs Kam): **34**
  - **H** (needs Paul or HP): **2**
  - **X** (already done in code): **9**
  - **P** (parked by a ruling): **7**
- **The 9 X rows are open on paper only. Close them in records:**
  - #120, #202, #262, #266, #267, #268, #270: shipped before B120 and B121;
  - #283: its test half landed in B113;
  - #180: in Friday's own runbook.
- **Lanes for bucket A (§6):** five builder lanes that share no file, plus one Friday-side records/ops lane:
  - **T1-API:** contract + API, 7 rows;
  - **T1-DB:** migration 0022 + runbook + start-up script, 5 rows;
  - **T1-OUT:** renderers, 3 rows;
  - **T2-DETAILS:** web screens + CSS, 7 rows;
  - **T2-TESTS:** web test strength and build, 7 rows.
- **16 A rows are deliberately not in a lane** (§6, "not laned"). Each is optional, Guided-only while Guided is OFF (C-50/C-52), or would collide with T1-API's contract bump.

## 1. Bucket A: agents can do it now (49)

| # | Item | Reason and evidence at 4e00d573 |
|---|---|---|
| 27 | VM deploy scripts not in repo; container names assumed | Ops, read-only on the VM at the next deploy. Deploy seats already run `remote-update.sh` (C-68 shows `migrations applied: none`); confirm the names and the archive location there |
| 43 | A question mapped under several items has no "asked under" pointer | The row gives a one-line plan (`see: [...]`, contract bump). Size L; not laned (it collides with T1-API's contract) |
| 57 | Expert typed editor writes device-group sub-answers at engagement level | Still `draftKey(answerKey, null)`, `apps/web/src/screens/Discovery.tsx:200,269`; latent on today's content |
| 66 | In-flight cap is per caller, not overall | A(F): the row states two design choices; `apps/api/src/app.ts` |
| 67 | b09 e2e spec skips silently when the synthetic switch is OFF | Still `test.skip(!seed.syntheticContent…)`, `apps/web/e2e/b09-example-flow-through.spec.ts:27` |
| 68 | Untyped group-scoped table offers out-of-scope group columns | `Discovery.tsx:931,1055` (`groupScoped`); the fix shape is stated; latent |
| 69 | 429 instead of 401 for an expired token during a sign-in flood | A(F). Only a 401 ends the session (`apps/web/src/api/client.ts:47`); title `apps/web/src/api/problem.ts:79` |
| 70 | Failed-sign-in window per process, no per-source key | A(F), optional: "Fix-shape if wanted" (`X-Real-IP` / nginx `limit_req`) |
| 71 | Mutant B37-M2 survives (onRequestAbort give-back) | A(F): keep it or remove it; `apps/api/src/app.ts:302` |
| 72 | 7 code comments still name the old repo name | Still 7 hits (e.g. `apps/api/test/b20-rate-limit.db.test.ts:6`). Deferred only by B40's own reasoning; no ruling found |
| 84 | `up.sh` printed HEALTH RED straight after `compose up` on a fresh project | The row's fix shape is stale: `scripts/health-check.sh:8,44-56` already retries until a 90 s deadline (last touched `bb5e02d0`, S45). Measure where the race is first |
| 116 | Approver summary cannot show each exception's business reason | Needs a contract read (the row says so); derivable. The contract has no exception read (`document.ts:1775` area) |
| 140 | Off-guide token checker misreads `//` comments | Records tooling, not the code repo: `Briefs/2026-10-03_B47_evidence/b47-check-off-guide.cjs` |
| 146 | `withdrawException` takes no If-Match | Still none: `packages/api-contract/src/document.ts:1773-1784` has no `ifMatch`; fix shape stated |
| 150 | `submitReview` accepts a draft carrying critical `DECISION_STALE` | `apps/api/src/routes/lifecycle.ts:381-405` refuses only `REQUIRED_DISCOVERY_INCOMPLETE`; fix "as release does" |
| 152 | `listApprovals` scans `audit_event`, which has no index | Newest migration is `0021_policy_target.sql`; no `entity_id` index in `packages/db/migrations/` |
| 155 | Long setting keys break mid-word in S9's withdrawn section | Still `overflow-wrap: anywhere`, `apps/web/src/styles/screens-w3.css:547-550` |
| 157 | `withdrawn_exceptions` required on a closed schema | Optional: a versioning note for strict clients. Not laned |
| 158 | PDF cover dates read in UTC | A(F): the row asks Friday to decide ("decision"). Needs a time zone on the brand profile or the tenant; that is a schema choice, so not laned |
| 159 | PDF template version stays `policy-document/1` | A(F), "decision for Friday": a separate `policy-document-pdf/2` |
| 160 | Executive summary may spill with 16+ areas | No fold in `packages/renderers/src/policy-summary.ts` (grep finds none); fix "fold over 12" |
| 161 | `PLAIN_TRIGGER` copied word for word into the renderers | Still two copies, `apps/web/src/screens/w3/approverSummary.tsx:16` and `packages/renderers/src/policy-summary.ts:40`; no comparison test |
| 164 | Vite warns that the web bundle has chunks over 500 kB | `apps/web/vite.config.ts` has no `chunkSizeWarningLimit` or `manualChunks` |
| 169 | `listControls` rebuilds the snapshot per load | Measure first ("fix-shape if it shows"). Not laned |
| 176 | `Controls.last_generate` required on a closed schema | Optional, as #157. Not laned |
| 177 | Generator's user id is answered to the approver and the auditor | A(F): "Fix-shape if wanted: answer the id only to Datasec roles" |
| 178 | `last_generate_input_hash` has no hex CHECK | `packages/db/migrations/0020_generate_issues_kept.sql:22` is `char(64)` with no CHECK; fix shape: an additive CHECK |
| 179 | GenerateRecord description says "exactly as" | Contract text only; fix shape stated |
| 197 | Monospace problem-code line flagged by the one-font rule | A(F): two options. `apps/web/src/components/ui.tsx:383` `pc-mono`. Not laned |
| 212 | b68 e2e S9 width cell flakes for one frame after a resize | Test-side shape stated (wait for the layout to settle); `apps/web/e2e/b68-l3-approval.spec.ts` |
| 228 | Guided home counts answers one engagement at a time | Sequential loop in `apps/web/src/screens/GuidedHome.tsx:151-168`. Guided is OFF (C-50), so it has no demo value. Not laned |
| 231 | Read-only roles see the wizard's edit words | Still keyed on the engagement: `GuidedWizard.tsx:129` `readOnlyKind(engagementData)`, `:1093` "Save and finish". Guided-only. Not laned |
| 241 | Fake DOM cannot choose a radio | `apps/web/src/screens/fakeDom.testing.ts` has no `querySelectorAll` (grep finds none) |
| 246 | `draftKeyLabel` used by no screen | A(F), leave it or retire it (`apps/web/src/screens/w2/model.ts:1069`). Never delete without Friday's word. Not laned |
| 247 | Unexplained file `/opt/hpsm/524337` on the demo VM | Ops: read it and quarantine it at the next deploy, never delete. Not in C-68 or the B124 STATUS |
| 269 | Worksheet, change report and manifest are still titled by the HPSM name | `packages/renderers/src/worksheet.ts:246,279`, `change-report.ts:488`; the rule is already set (design §a.2) |
| 291 | `DEPLOY.md`'s Route B never run on 0020 | Fix shape stated: run it on a seat stack |
| 293 | A two-step restore cut at a statement boundary exits 0 | `DEPLOY.md:202-206` checks only `echo $?`, with no "dump complete" check |
| 294 | Name written by device-profile is not read back on getDeviceProfile | A(F), "Kam's or the lane-2 seat's call". The contract minor is the agent option. `apps/api/src/routes/inputs.ts:420-457` |
| 297 | C-65 AMENDMENT overstates Route A ("keeps the data") | Friday's records lane: a dated correction |
| 298 | A failed re-read after a 409 still says "the page now shows it" | Still there: `apps/web/src/screens/w1/problems.ts:38`, and the catch at `EngagementDetails.tsx:340`. The shape reuses the existing ErrorState and reload |
| 299 | "Choose a policy" offered on a stale-pinned engagement | A(F): "Friday rules whether to add it". `policyChooser` `EngagementDetails.tsx:741-751` has no pin check; `w1/problems.ts` has no `CONTENT_VERSION_CHANGED` |
| 301 | Two of B116's absence tests do not bite | Test change stated (use the platform_admin arm) |
| 302 | B116's `input ≤ picker` width check cannot fail | Test change stated (assert absolute widths) |
| 303 | setPolicyTarget's ETag header is not described in the contract | `document.ts:1412-1424` (`etag: true`, notes `B113_SET_TARGET` `:90`) never says which ETag; round-2 shape stated |
| 305 | 820 px tablet band: new mid-word breaks in the S9 register | Gate's shapes and test stated; `apps/web/src/styles/screens-w3.css` shares |
| 308 | A long engagement name with no spaces scrolls 390 sideways | `.pc-breadcrumb` `apps/web/src/styles/app.css:290-302` has no `overflow-wrap`; shape and test stated |
| 310 | b120 radii test does not pin the 3 held app.css shapes | `apps/web/src/styles/b120-radii.test.ts:29-37` scans only `screens-w1/w2/w3.css` |
| 311 | `tsc` on the e2e folder: 2 errors, silent in CI | Still `const [hi, lo] = …` at `apps/web/e2e/b109-approval-release-disabled.spec.ts:63` |

## 2. Bucket K: needs Kam (34)

| # | Item | Reason and evidence |
|---|---|---|
| 35 | Seat C wording shown in Guided (D-006 etc.) | "OPEN for Kam's word"; still `apps/web/src/guided/model.ts:356` |
| 42 | Controls "Customer said" vs the generation snapshot | "Kam's call between that hint and a stale marker" |
| 95 | No email sent at any point; the form says approvers "are invited" | Build mail (external comms) or reword; still `CreateEngagement.tsx:640` |
| 99 | No "version 2" after release | "KAM'S CALL". Note: `createDraft` exists in the contract (`document.ts:1670`), so this is a web control plus words, not a new API |
| 104 | Secret fields: 8 forms, each with a justification | The fix drops the justification rule for local values, a governance choice |
| 106 | Evidence ZIP, JWS and manifest unavailable (no signing key) | "ops; Friday/Kam". A signing key on Kam's demo |
| 129 | Ready-sheet footer "Reply to the email" | "Show Kam with the screenshots"; still `ReadySheet.tsx:134` |
| 131 | Past and far-future due dates accepted | "a product decision: warn or refuse" |
| 171 | Docker address pools run out on the laptop | Eased by C-39. What is left is the daemon's pool settings on Kam's machine |
| 172 | Two Guided users can add the same client name | "Friday's / Kam's call … a contract text change" |
| 173 | Both callers get 201 at once | With #172 |
| 182 | No screen starts the next draft | Coupled to #99's call. The API exists; there is no caller in `apps/web/src` and `Validation.tsx:121` points nowhere |
| 227 | Guided persona's demo data | "Kam's word: any fix is a demo-data change" |
| 236 | Paul's guide describes the old sign-in | "Kam's word on the note" |
| 257 | Feedback pill over G01's notes at 1280 | Would change C-22's ruled placement |
| 259 | Long names wrap the S5 breadcrumb | "No fix proposed; Friday's or Kam's call". A look question (the no-space case is #308) |
| 260 | `completeExpertSetup` with neither key nor name answers 200 | The stated `anyOf` would refuse today's only UI path (#285: the list is `[]`). Contract `document.ts:291-303` requires only environment and approvers; the alternative is "decision … for Kam" |
| 271 | Change POLICY_ALREADY_EXISTS words with the engine? | "Question for Kam" |
| 272 | S5 shows "HPSM" from the content release | Needs a content release; pinned engagements go read-only (C-05, C-64) |
| 277 | Tenantless role's Feedback refusal shows engineering words | "Kam's words" |
| 278 | 77 never-shown "Composer" strings in the bundle | "Kam's call whether view-source counts" (C-62) |
| 280 | Set-up card says "created without one" | "Kam's words" |
| 281 | `name: null` text runs the key into the sentence | "Kam's punctuation" |
| 282 | Clone resets the E8 level silently | "Kam's call" |
| 284 | S2's own "HPSM" lines | "Kam's words." |
| 285 | Every set-up sends neither key nor name | "Record beside #260"; it waits on #260's call |
| 286 | Rail ticks step 3 Complete with an empty list | "Kam's look" |
| 287 | Layout notes at 390 (S2 rail, S4 card) | "Kam's look" |
| 288 | List cells say "Not chosen" with no reason | "Kam's look." |
| 300 | Refused secret-shaped value stays in the input | "Kam's or Friday's call". Security plus new words, so Kam |
| 304 | Two VERSION_NOT_EDITABLE phrasings differ | "Kam's look, with NEW WORDS"; `apps/api/src/queries.ts:311-315` vs `routes/engagements.ts:202` |
| 306 | Approver inputs narrower (#219 trade-off) | "Kam's call (Q-2)" |
| 307 | Sign-in radio moves 5 px; Frameworks radios still 13 px | "Kam's look for the 5 px shift". The Frameworks half (`.pc-choice-card` outside `.pc-signin`, `app.css:882`) is agent-doable once proposed as its own row |
| 309 | "A clone", "An answer", "answer_key" words | "Kam's words." |

## 3. Bucket H: needs Paul or HP (2)

| # | Item | Reason and evidence |
|---|---|---|
| 15 | Q-13 ratification of the B09 typed answers and 28 mappings | "needs a Datasec SME and a second person"; the interim reviewers are Kam and Paul (C-57) |
| 265 | `online_service_in_use` links always count | "SME check (Kam and Paul, C-57) … No code change before they have spoken" |

## 4. Bucket X: already done (9)

| # | Item | Evidence |
|---|---|---|
| 120 | Web unit suite exits 1 (pill timer, fake DOM) | `apps/web/src/feedback/FeedbackWidget.tsx:341-347` returns early without `querySelectorAll` / `getBoundingClientRect` (#114's guard = #120's fix shape) |
| 202 | ESLint purity tests time out at 5 s | `packages/engine/test/purity-lint.test.ts:21,26`; `w3r2-minor4-purity-lint.test.ts:24,53` (`ESLINT_TEST_TIMEOUT_MS`) |
| 262 | n4 + n6 still hold | Both are closed: see #266 and #268 |
| 266 | `DEPLOY.md` has no 0021 rollback section | `DEPLOY.md:153` "## Rolling back a deploy that applied 0021" |
| 267 | purity-lint 5 s timeout under load | As #202 |
| 268 | `types.test.ts:297` title says 0.29.0 | `apps/web/src/feedback/types.test.ts:297` reads "is read from contract 0.31.0" |
| 270 | S2 rail "Policy" vs section title "HPSM Policy Details" | Both say "Policy": `apps/web/src/screens/w1/policyTarget.ts:31` (`sectionTitle`), used at `CreateEngagement.tsx:566`; rail `:793` |
| 283 | Clone's HPSM version not asserted | `apps/api/test/b103-policy-target.db.test.ts:362-367` "B113 #283: a clone … gets the running content's highest (5.9.0)" |
| 180 | Runbook step 6's SSH-closed proof | Not code: `FRIDAY/2_Project_Files/friday/composer_demo_deploy.md:28` already holds the #180 exception; B119/B124 used it (C-67, C-68) |

## 5. Bucket P: parked by a ruling (7)

| # | Item | Ruling |
|---|---|---|
| 79 | Sections in the rail only on the Guided level | Kam, B42 ADDENDUM-2 (quoted in the row): "the Expert rail unchanged" |
| 151 | Withdrawals before B56 carry no name | "accepted by design unless Friday rules otherwise". This is an acceptance, not a Kam card |
| 222 | Pill over a KPI label with the rail expanded | "Left by Friday's ruling (B87 ADDENDUM-1)" within C-22 |
| 223 | KPI tiles start ~1,200 px down at 390 | "Left by Friday's ruling (B87 ADDENDUM-1)"; Kam's to ask for |
| 226 | Guided home's 4-step guide not clickable | C-52 / C-50: Guided view hidden; "Left OPEN for when Guided is switched back on" |
| 235 | Guided switch is not an access control | Friday's ruling (a), "a KNOWN LIMIT" (B92 ADDENDUM-2). Nothing to build; it could be closed |
| 240 | Guided wizard stale-pin trap | C-50: "Same fix … when Guided comes back". Still open in code: `apps/web/src/guided/ReadOnlyNotice.tsx:19` does not read `pinned_to_running_releases` (S5's does, `screens/w2/expertSections.ts:127`) |

## 6. Lanes for bucket A (file-disjoint)

No two lanes write the same file. Where a lane only *reads* another lane's file, that is said.

### T1-API: contract and API correctness (tier 1), 7 rows
- **Rows:**
  - #146: If-Match on withdrawException;
  - #150: refuse submit on critical issues;
  - #303: setPolicyTarget ETag description;
  - #179: GenerateRecord wording;
  - #177: generated_by user id for Datasec roles only (A(F));
  - #294: optional `requested_hpsm_name` on DeviceProfile (A(F));
  - #116: an exception read for the approver summary.
- **Writes:**
  - `packages/api-contract/src/` (one contract bump for all rows);
  - `apps/web/src/api/schema.d.ts` (regenerated);
  - `apps/api/src/routes/` (`lifecycle.ts`, the exceptions route, `inputs.ts`, `engagements.ts` description only);
  - `apps/api/test/` (new DB tests);
  - `apps/web/src/screens/w3/approverSummary.tsx` (#116's web half only).
- **Gate:** `ci.sh`, CodeQL, red-first DB test per row.
- #150 changes what a salesperson can submit, so measure the demo examples' flow first.

### T1-DB: migration 0022, runbook and start-up script (tier 1), 5 rows
- **Rows:**
  - #152: audit_event index;
  - #178: hex CHECK;
  - #291: Route B on 0020;
  - #293: "dump complete" check before step 2;
  - #84: find the HTTP 000 race.
- **Writes:**
  - `packages/db/migrations/0022_*`;
  - `packages/db/rollback/0022_*.down.sql`;
  - `packages/db/test/`;
  - `DEPLOY.md` (a 0022 section, plus the #291/#293 fixes);
  - `scripts/` (`up.sh`, `health-check.sh`).
- **Note:** a migration-bearing deploy needs a down recipe (#26 rule in `DEPLOY.md`).

### T1-OUT: renderers (tier 1, output artefacts and their bytes), 3 rows
- **Rows:**
  - #269: titles by policy target name per design §a.2;
  - #160: fold areas over 12;
  - #161: a test that compares the two `PLAIN_TRIGGER` copies.
- **Writes:** `packages/renderers/src/`, `packages/renderers/test/`.
- **Reads only:** `apps/web/src/screens/w3/approverSummary.tsx`, which T1-API writes for #116. Run T1-OUT's #161 test after T1-API merges, or pin the words, not the file.
- #159 (a PDF-only template version, A(F)) can join if Friday rules on it.

### T2-DETAILS: Expert screens a salesperson sees (tier 2), 7 rows
- **Rows:**
  - #298: failed re-read: ErrorState + reload, no "now shows it";
  - #299: no chooser on a stale pin (A(F), Friday rules R-3);
  - #301: bite-proof absence arms;
  - #305: the 820 band;
  - #308: breadcrumb / h1 `overflow-wrap`;
  - #155: withdrawn Setting column;
  - #68: in-scope group columns only, latent; with #57 if the seat has time.
- **Writes:**
  - `apps/web/src/screens/EngagementDetails.tsx`;
  - `apps/web/src/screens/w1/` (`problems.ts`, `editability.ts`);
  - `apps/web/src/screens/Discovery.tsx`;
  - `apps/web/src/styles/app.css`, `apps/web/src/styles/screens-w3.css`;
  - their DOM tests under `apps/web/src/screens/`;
  - new e2e specs under `apps/web/e2e/`.
- **Gate:** rendered at 1280, 1180, 820 touch and 390, image + Mac Chrome.
- Any new sentence goes to Kam as NEW WORDS.

### T2-TESTS: web test strength, harness and build (tier 2), 7 rows
- **Rows:**
  - #302: absolute width assertion in the b116 spec;
  - #310: pin the 3 app.css held shapes;
  - #311: the two `tsc` errors in the b109 spec (and type-check `e2e/` in CI if Friday agrees);
  - #67: fail loudly instead of skipping;
  - #212: wait for the layout to settle;
  - #241: `querySelectorAll` on FakeNode;
  - #164: code-split or a stated chunk limit.
- **Writes:**
  - `apps/web/e2e/` (existing `b116-web-a4-a3-screens.spec.ts`, `b109-approval-release-disabled.spec.ts`, `b09-example-flow-through.spec.ts`, `b68-l3-approval.spec.ts`);
  - `apps/web/src/styles/b120-radii.test.ts`;
  - `apps/web/src/screens/fakeDom.testing.ts`;
  - `apps/web/vite.config.ts`;
  - `ci.sh`, only if #311's CI half is taken.
- **Does not write** any file that T2-DETAILS writes.

### Friday-side (not a builder lane): records and ops, 4 rows
- #297: a dated correction to C-65's AMENDMENT.
- #140: the `//` comment strip in `Briefs/2026-10-03_B47_evidence/b47-check-off-guide.cjs`, plus a self-test.
- #27 and #247: read-only on the VM at the next deploy seat; quarantine, never delete.
- Records also owe the 9 X closures (§4).

### A rows not laned (16)
- #43: an L-sized contract bump; next round after T1-API.
- #57: it joins T2-DETAILS if the seat has time.
- #66, #69, #70, #71, #157, #176, #197, #246: optional, or Friday's choice first.
  - #69 touches `apps/web/src/api/` and the contract, so it belongs with a later T1-API round.
- #158: schema choice for the time zone.
- #159: Friday's ruling first.
- #169: measure first.
- #228, #231: Guided-only while Guided is OFF.
- #72: comment-only; it touches files in four packages, so do it as its own chore.

## 7. What I could not measure
- **Rendered behaviour:** no browser, no stack and no tests were run. The layout rows (#155, #305, #308, #212) and the K look rows are code-read and row-text only.
- **#84:** whether the HTTP 000 race still happens, and in which script.
- **#169:** listControls cost under load.
- **#150:** whether refusing submit on criticals would block a demo example's flow.
- **Dependabot after B121:** the alert list was not read; `gh api` was not used. C-68 records the fastify / fast-uri / brace-expansion bumps.
- **Older rulings were not re-opened:** B42 ADDENDUM-2, B87 ADDENDUM-1, B92 ADDENDUM-2 and the C-22/C-50/C-52 texts are taken from the rows' own quotes and the CLARIFICATIONS headings.
  - One heading did not match a row's citation. #72 cites "C-18", but C-18 in this file is about a different subject. So #72 is treated as unruled (A).
- **The 820 band fix (#305):** whether any share set clears every break is a render question.
- **#283's X:** rests on the test's title and comment at `:362-367`. The test was not run.
