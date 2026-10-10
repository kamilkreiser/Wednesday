# Composer screen: which BACKLOG rows an agent can act on now (2026-10-11)

**Project:** Datasec / Security Composer (code repo `datasecau/Datasec-Security-Composer`, formerly HPSM-light). **Screen by:** a read-only Friday subagent. Nothing was written in the project tree.
**Code read at:** `origin/main` = **`a3502002df54a44ae5063458862796076115766c`**, the build that is live on the demo (C-67, `Briefs/2026-10-10_B119_STATUS.md`). The local `main` checkout is stale at `0b2fca43`, so every code citation below is `git show/grep a3502002`, never the working tree.
**Inputs read:** `CLAUDE.md`; `BACKLOG.md`, all 288 rows; `1_Project_Definition/CLARIFICATIONS.md` (C-27…C-66 headings, C-62…C-66 in full); the 3 newest STATUS files, `Briefs/2026-10-10_B117_STATUS.md` (gate on B116), `…_B118_STATUS.md` (Q-3 words) and `…_B119_STATUS.md` (deploy a3502002, C-67).

## BLUF
- **Rows screened: 139.** That is every row not marked DONE, MERGED or DEPLOYED, plus the rows marked part-done or ready-for-review that still have an open half. Rows #215 and #218 share one line in the table.
- **Counts by class:**
  - **A** (an agent can act now): **44**
  - **K** (needs a ruling): **55**. Kam: 41. Friday's own choice between options, marked K(F): 14.
  - **H** (needs another human): **2**
  - **X** (parked, informational or blocked): **21**
  - **D** (the row is open but the code at a3502002 says it is done; see §3): **17**
  - A split row is counted once, by its A half (#75, #108, #123, #209, #290).
- **Lane 1, highest value to a salesperson (tier 2, `apps/web` only):** fix what a salesperson sees on the Expert screens.
  - #207: raw ids on Details.
  - #199: internal `answers[n]` paths in the error box.
  - #219: the narrow approver "Person" select on S2.
  - #210: "Authentication" breaks mid-word on S9.
  - #75, #123, #154: the radius half only (off-token radii in `screens-w*.css`).
  - #201: the hover colour, using an existing token.
  - #108 (b) and (d): the sign-in radio dots and the 390 px breadcrumb, measured first.
- **Lane 2 (tier 1, `apps/api` and the lockfile):** security and API correctness.
  - #254: the Dependabot advisories. B118 saw 4 open, 1 high, on 2026-10-10.
  - #292: setPolicyTarget's ETag header answers a 412.
  - #295: one as-of date per dashboard response.
  - #205: untrue "request changes" words for an approved version.
  - #208: the 200-character bound counts UTF-16 units, not characters.
  - #209 (a): add U+16FE4 to the invisible set.
  - #237: the API halves of the wall-clock timing tests.
- **17 rows are stale against the code** (§3). The biggest:
  - #261, #263, #264, #289, #266, #262, #268, #202 and #267 are shipped in a3502002 and live (C-67), but still say OPEN or "not merged".
  - #206, #211 (B116) and #120 (by #114's fix) are also done in the code.
  - #99 says "there is no API operation to open a new version", but `createDraft` is in the contract (`document.ts:1670`), and #182 says so.

Legend: **Size** S ≈ under half a day for one seat, M ≈ one seat-day, L = more than one seat or a contract/content release. **K(F)** = the row asks Friday (an agent) to choose between options. It is not actionable until Friday rules, but Kam is not needed.

## 1. Every open row

| # | Summary (row's own words, shortened) | Class | Reason / quote | Size | Would touch |
|---|---|---|---|---|---|
| 1 | Paul's user guide v1.2 | K | "Kam sends." | S | `1_Project_Definition/User_Guide/` |
| 4 | Find and record the Composer's Jira project | K | "key `PCOMP` … on HOLD (HPSM Q-05). Kam's call." | S | records |
| 7 | Decide re-accepts decided rows; tenant default; approver B; approver sees all | D | 7a/7b/7c merged (e0d8a3f, C-09); 7d "NOT REPRODUCED" | – | – |
| 9 | Phone and tablet design pass (C-03) | D | "BRIEFED … as B04"; B04 merged `9c7c71db` | – | – |
| 12 | Cold-reader product observations | D | 12a/12b/12c all merged (`0b2fca43`, `e0d8a3f`) | – | – |
| 13 | B02 left 4 test engagements on the demo | X | "Covered by Kam's #6 ruling … no new ask" | – | – |
| 15 | Q-13 ratification of B09 typed answers and 28 mappings | H | "needs a Datasec SME and a second person" | M | content mapping |
| 17 | Guide v1.3 | K | "sending is Kam's" | S | User_Guide |
| 21 | Examples A and B for Paul | K | "READY FOR REVIEW" (Kam) | – | – |
| 26 | `migrate` refuses an unknown recorded migration | K | "the choice … is Kam's/Friday's" | M | `packages/db/src/migrate.ts` |
| 27 | VM deploy scripts not in repo | K | "Friday/Kam, read-only on the VM" | S | VM, `DEPLOY.md` |
| 30 | Session end loses one screen's typing | K | "a data-handling choice for Kam" | M | `GuidedWizard.tsx` |
| 34 | Rolling back past B22 not proven | K(F) | "Friday decides at deploy whether to prove it" | M | `DEPLOY.md`, seat stack |
| 35 | Seat C wording shown in Guided | K | "OPEN for Kam's word" | S | `guided/model.ts`, `engine/questionnaire.ts` |
| 41 | CJK/Arabic/emoji print as boxes in the PDF | K | "OPEN: Kam's call on the size" | L | renderers, fonts |
| 42 | Controls "Customer said" vs the generation snapshot | K | "Kam's call between that hint and a stale marker" | M | Controls screen |
| 43 | A question mapped under several items has no pointer | A | plan given; "needs … a contract change" | L | engine questionnaire, contract, S5 |
| 54 | C1 characters accepted | K | "C1 stays text, still Kam's call" | S | `control-characters.ts` |
| 55 | Emptied box + Next deletes with no confirm | K | "KAM'S CALL" | S | `GuidedWizard.tsx` |
| 57 | Expert typed editor writes engagement level only | A | latent: content has 0 device-group sub-answers | M | `apps/web/src/screens/Discovery.tsx` |
| 61 | Scope refusal precedes group errors | X | "INFO (as the gate classed it)" | – | – |
| 63 | Identical rewrite bumps the revision | X | "FRIDAY'S DECISION, recorded: kept as built" | – | – |
| 64 | Intake stricter than the engine | X | "NOTED for deploy prep" | – | – |
| 66 | In-flight cap per caller, not overall | K(F) | "OPEN (design, Low). Choices: …" | M | `apps/api/src/app.ts` |
| 67 | b09 e2e spec skips when the switch is OFF | A | fix shape given (fail loud, or run only ON) | S | `apps/web/e2e/b09-example-flow-through.spec.ts` |
| 68 | Untyped group-scoped table offers out-of-scope columns | A | latent; fix shape given | M | `Discovery.tsx` |
| 69 | 429 instead of 401 under a sign-in flood | K(F) | "Fix-shape options" | S | `client.ts`, `problem.ts`, contract |
| 70 | Failed-sign-in window per process | X | "OPEN (informational …)" | – | – |
| 71 | Mutant B37-M2 survives | K(F) | "a decision, not a defect" | S | `apps/api/src/app.ts` |
| 72 | 7 comments name `HPSM-light` | X | "deferred: rename mentions after the redirect is retired" | S | 7 test files |
| 73 | B41 UX review, change 5 | K | "KAM'S CALL on the rendered proposal" | L | web-wide buttons |
| 75 | Off-token radii and `#ffffff` | A (radii) / K (`#ffffff`) | "`#ffffff` → a token (needs Kam's token approval)" | S | `apps/web/src/styles/screens-w1/w2/w3.css` |
| 76 | (b) End page heading touches tiles | A | Guided-only; Guided is OFF (C-50), so it has no demo value | S | `GuidedWizard.tsx` |
| 79 | Sections in the rail only on Guided level | X | "OPEN (Info; design)" | – | – |
| 84 | `up.sh` HEALTH RED on a fresh project | A | fix shape: retry; see UNMEASURED | S | `scripts/up.sh`, `scripts/health-check.sh` |
| 95 | No email is sent at any point | K | options: mails or reword (external comms) | L | worker, mail, create form |
| 99 | No "version 2" after release | K | "KAM'S CALL: build "Start version 2" or reword" | L | API, `EngagementDetails.tsx` |
| 101 | "not available in this release" across screens | K | "KAM'S CALL: hide unbuilt features, or build the top two" | L | Expert screens |
| 104 | Secret fields: 8 forms for 7 controls | A | fix shape given; drops a justification rule (flag to Friday) | L | X-CONTROLS: API + web |
| 106 | Evidence ZIP / JWS / manifest unavailable (no signing key) | K | "OPEN (ops; Friday/Kam)" | S | VM config |
| 108 | Naming; radio dots 5 px; q71; breadcrumb at 390 | A (b, d) / K (a) / X (c, Guided) | "(a) KAM'S CALL on the name" | S | `apps/web/src/styles/app.css` (sign-in, breadcrumb) |
| 109 | Repeated-questions modal | D | "PART FIXED … not merged"; B52 merged `5a8254b7` (PR #24) | – | – |
| 116 | Approver summary can't show exception reasons | A | "needs a contract read, so a later round" | M | contract, API, `w3/approverSummary.tsx` |
| 120 | Web unit suite exits 1 (pill timer) | D | fixed by #114's guard | – | – |
| 123 | Off-guide radii/`#ffffff` in w1/w2 CSS | A (radii) / K (`#ffffff`) | as #75 | S | `screens-w1.css`, `screens-w2.css` |
| 129 | Ready sheet footer "Reply to the email" | K | "Show Kam with the screenshots" | S | `ReadySheet.tsx` |
| 131 | Past and far-future due dates accepted | K | "a product decision: warn or refuse" | S | `guidedStart.ts`, `w1/validation.ts` |
| 140 | Token checker misreads `//` comments | A | tooling, evidence only | S | `Briefs/2026-10-03_B47_evidence/b47-check-off-guide.cjs` |
| 146 | `withdrawException` takes no If-Match | A | "If-Match on the draft's ETag (a contract change)" | M | contract, `apps/api` exceptions route |
| 150 | `submitReview` accepts a draft with criticals | A | "refuse submit on critical issues, as release does" | M | `apps/api/src/routes/lifecycle.ts`, contract |
| 151 | Older withdrawals carry no name | X | "accepted by design unless Friday rules otherwise" | – | – |
| 152 | `listApprovals` scans `audit_event` | A | "an index … (a migration)" | S | `packages/db/migrations/0022_*` |
| 154 | S9 withdrawn section 8 px vs register 6 px | A | "Goes with #75 / #123" | S | `screens-w3.css` |
| 155 | Long setting keys break mid-word | A | "With #107" | S | `screens-w3.css` |
| 157 | `withdrawn_exceptions` required on a closed schema | X | "OPEN (Low; noted)" | – | – |
| 158 | PDF cover dates in UTC | K(F) | "decision" | S | renderers, brand profile |
| 159 | PDF template version stays `/1` | K(F) | "decision for Friday" | S | renderers |
| 160 | Executive summary may spill at 16+ areas | A | fix shape: fold over 12 | S | `packages/renderers/src/policy-summary.ts` |
| 161 | `PLAIN_TRIGGER` copied word for word | A | shared module or comparison test | S | `approverSummary.tsx`, `policy-summary.ts` |
| 164 | Vite chunk > 500 kB warning | A | split by route or a stated limit | S | `apps/web` vite config |
| 169 | `listControls` rebuilds the snapshot | X | "Fix-shape if it shows"; not measured | – | – |
| 171 | Docker address pools exhausted | K(F) | "Friday/Kam, not a seat" | S | laptop Docker |
| 172 | Two Guided users can add the same client name | K | "Friday's / Kam's call … contract text change" | M | `engagements.ts` |
| 173 | Both callers get 201 at once | K | "with #172, Friday's / Kam's call" | M | `engagements.ts` |
| 176 | `last_generate` required on a closed schema | X | "Fix-shape if an external consumer appears" | – | – |
| 177 | Generator's user id answered to approver/auditor | K(F) | "Fix-shape if wanted" | S | contract, API |
| 178 | `last_generate_input_hash` has no hex CHECK | A | "an additive CHECK … in a later migration" | S | `packages/db/migrations/0022_*` |
| 179 | GenerateRecord text "exactly as" | X | "in the next contract text change" | S | contract text |
| 180 | Runbook step 6 SSH-closed proof | A | Friday's own file, outside the project | S | `FRIDAY/2_Project_Files/friday/composer_demo_deploy.md` |
| 182 | No screen starts the next draft | K | an option of #99, which is "KAM'S CALL" | M | `Validation.tsx:121`, `EngagementDetails.tsx` |
| 193 | Half 2: who adds a new customer's approver | K | "Half 2 NOT ruled" | M | `engagements.ts` |
| 197 | Monospace problem code flagged | K(F) | "Options: allow monospace … or page font" | S | `ui.tsx` |
| 199 | Error box leads with `answers[<n>]` | A | fix shape given (NEW WORDS for Kam after) | S | `apps/web/src/components/ui.tsx` |
| 201 | Row hover `#f7fafd` off-token | A | "a `--pc-` token … (or an existing surface token)" | S | `apps/web/src/styles/app.css` |
| 202 | ESLint purity tests time out | D | per-test timeout landed (B114) | – | – |
| 205 | API tells an approved version to request changes | A | "state-specific words, C-34's for approved" | S | `apps/api/src/queries.ts` |
| 206 | S9 strip doesn't re-read after Run validation | D | B116 | – | – |
| 207 | Details shows raw ids (Cloned from, Current release) | A | web shape given ("A clone", "Released") | S | `apps/web/src/screens/EngagementDetails.tsx` |
| 208 | `keptName` counts UTF-16 units | A | gate's fix shape | S | `apps/api/src/last-generate.ts` |
| 209 | U+16FE4 and lone combining marks pass | A (U+16FE4) / K(F) (marks) | "Friday / Kam to decide whether … combining marks is refused" | S | `apps/api/src/control-characters.ts` |
| 210 | S9 "Authentication" breaks mid-word | A | measured layout (B68) | S | `apps/web/src/styles/screens-w3.css` |
| 211 | S10 manifest verify unhandled rejection | D | B116 | – | – |
| 212 | b68 e2e width cell timing | A | "the cause is not yet known" | M | `apps/web/e2e/b68-l3-approval.spec.ts` |
| 219 | S2 "Person (required)" select is narrow | A | needs shots at 1280/1180/390 | S | `w1/ApproversTable.tsx`, `screens-w1.css` |
| 222 | Pill over a KPI label with the rail expanded | X | "Left by Friday's ruling (B87 ADDENDUM-1)" | – | – |
| 223 | KPI tiles 1,200 px down at 390 | X | "Left by Friday's ruling … Kam's to ask for" | – | – |
| 226 | Guided home guide not clickable | X | "Left OPEN for when Guided is switched back on" | – | – |
| 227 | Guided persona's demo data | K | "Kam's word: any fix is a demo-data change" | – | demo |
| 228 | Guided home counts one at a time | A | Guided-only (OFF): no demo value | S | `GuidedHome.tsx` |
| 231 | Read-only roles see the wizard's edit words | A | Guided-only (OFF): no demo value | S | `GuidedWizard.tsx` |
| 235 | Guided switch is not an access control | X | ruled "(a) — a KNOWN LIMIT" (see §3) | – | – |
| 236 | Paul's guide describes the old sign-in | K | "Kam's word on the note" | S | User_Guide |
| 237 | Three more wall-clock timing tests | A | engine half done; 2 API files left | S | `apps/api/src/s47-crf-scan-linear.test.ts`, `s47-crf2-scan-cost.test.ts` |
| 240 | Guided wizard stale-pin trap | X | "Same fix … when Guided comes back" | – | – |
| 241 | Fake DOM can't choose a radio | A | "if a DOM test needs it" | S | `apps/web/src/screens/fakeDom.testing.ts` |
| 246 | `draftKeyLabel` unused | K(F) | "Leave it, or retire it" | S | `w2/model.ts` |
| 247 | Unexplained file `/opt/hpsm/524337` | K | "Friday's or Kam's … on the next deploy" | S | VM |
| 249 | Lane 3a: E8 mapping content release | X | "BLOCKED: needs Kam's approval after Kam and Paul Waite's check" | L | `packages/content`, `content/**` |
| 252 | Lane 4: deploy the new content release | K | "KAM'S CALL (engagements become read-only …)" | L | demo |
| 254 | Dependabot advisories on main | A | "Friday's to commission"; fix shape given; alert ids UNMEASURED | M | `package-lock.json`, `package.json` files |
| 257 | Pill over G01 notes at 1280 | K | "Friday's or Kam's call" (changes C-22) | S | `pillPlacement.ts` |
| 258 | e2e pixel acceptances use a font no user has | K(F) | "Friday's to commission"; two options | M | `apps/web/e2e/`, `run.sh` |
| 259 | Long names wrap the S5 breadcrumb | K(F) | "No fix proposed; Friday's or Kam's call" | – | – |
| 260 | `completeExpertSetup` with neither key nor name → 200 | K | an `anyOf` would refuse today's UI path (#285); alternative "decision … for Kam" | M | contract, `engagements.ts` |
| 262 | n4 + n6 still hold | D | both closed (#266, #268) | – | – |
| 263 | Choose a target for an existing engagement | D | B113 + B116, live C-67 | – | – |
| 264 | Target panel counts not served | D | B113 A2 + B116, live C-67 | – | – |
| 265 | `online_service_in_use` links always count | H | "for the SME check (Kam and Paul, C-57)" | – | – |
| 266 | `DEPLOY.md` 0021 rollback section | D | B114, live | – | – |
| 267 | purity-lint 5 s timeout | D | as #202 | – | – |
| 268 | `types.test.ts:297` says 0.29.0 | D | now 0.31.0 | – | – |
| 269 | Worksheet/change report/manifest titled by HPSM name | A | "for a later lane (§a.2 …)" | M | `packages/renderers/**` |
| 270 | S2 rail "Policy" vs section 3's title | D | "closes with lane 3c" (live C-66) | – | – |
| 271 | Change POLICY_ALREADY_EXISTS words with the engine? | K | "Question for Kam" | – | – |
| 272 | S5 shows "HPSM" from the content release | K | "Needs a content release" (read-only consequence, C-05) | L | `content/**` |
| 273 | `problems.ts:13` / `catalogue.ts:37` HPSM sentence | K | waits on #271 | S | engine issues, web, API problem |
| 277 | Tenantless Feedback refusal shows engineering words | K | "Kam's words" | S | Feedback pill, API detail |
| 278 | 77 "Composer" strings in the bundle | K | "Kam's call whether view-source counts" | M | `content/**` |
| 280 | Set-up card "created without one" | K | "Kam's words" | S | `ExpertSetupCard` |
| 281 | `name: null` text runs key and sentence | K | "Kam's punctuation" | S | `w1/policyTarget.ts` |
| 282 | Clone resets E8 level silently | K | "Kam's call" | S | S2 |
| 283 | Clone's HPSM version not asserted | A | "a B103-style DB assertion of the clone's version" | S | `apps/api/test/` |
| 284 | S2's own "HPSM" lines | K | "Kam's words." | – | – |
| 285 | Every set-up sends neither key nor name | X | "Record beside #260" (records only) | – | – |
| 286 | Rail ticks step 3 Complete with `[]` | K | "Kam's look" | S | `CreateEngagement.tsx` |
| 287 | Layout notes at 390 | K | "Kam's look" | – | – |
| 288 | List cells "Not chosen" with no reason | K | "Kam's look." | S | `PolicyCell` |
| 289 | A4: edit the HPSM policy name | D | B113 + B116, live C-67 | – | – |
| 290 | 0021 rollback: (a) merge, (b) VM archive, (c) db test | A (c) / K (b) | (a) done; "(c) a db test pins the two-step Route B (none does …, not commissioned)" | S | `packages/db/test/` |
| 291 | Route B on 0020 not run | A | fix shape given | M | seat stack, `DEPLOY.md` |
| 292 | setPolicyTarget header is the engagement ETag → 412 | A | "Owner TBD"; fix shape given | S | `apps/api/src/routes/engagements.ts` |
| 293 | Two-step restore: a boundary-cut script exits 0 | A | "Owner TBD"; fix shape given | S | `DEPLOY.md`, `packages/db/test/` |
| 294 | Name not read back on getDeviceProfile | K(F) | "Kam's or the lane-2 seat's call" | S | contract |
| 295 | `coverageOf` reads `nowOf` per row | A | "if taken"; fix shape given | S | `engagements.ts`, `apps/api/src/coverage.ts` |
| 296 | Target silently changes ML2→ML3 on set-up | K(F) | "NEEDS FRIDAY'S RULING" | S | `engagements.ts` |
| 297 | C-65 AMENDMENT overstates Route A | A | "Friday's records lane" (docs) | S | `CLARIFICATIONS.md` (dated correction) |
| 215, 218 | E8 mapping build; lanes 2–4 | X | "Build = #249 (BLOCKED …)"; build rows #248–#252 | – | – |
| 261 | coverage as-of date | D | "not yet merged"; merged `abc97996`, live C-67 | – | – |

## 2. Proposed lanes (at most two, file-disjoint)

### Lane 1: Expert-screen polish a salesperson sees (tier 2, `apps/web` only)
**Rows:** #207, #199, #219, #210, and the radius-only halves of #75, #123 and #154 (no `#ffffff`, because that needs Kam's token approval). Also #201, using an existing surface token (no new token), and #108 (b) and (d), measured first and fixed only if they reproduce.

**Files:**
- `apps/web/src/screens/EngagementDetails.tsx`
- `apps/web/src/components/ui.tsx`
- `apps/web/src/screens/w1/ApproversTable.tsx`
- `apps/web/src/styles/app.css`
- `apps/web/src/styles/screens-w1.css`, `screens-w2.css`, `screens-w3.css`
- tests under `apps/web/src/**` and `apps/web/e2e/`

Nothing outside `apps/web`.

**Gate:** rendered tier-2 gate at 1280, 1180 and 390, in the pinned image and Mac Chrome.
- New words from #207 and #199 go to Kam as NEW WORDS after the build, as was done for C-64.

**Still open at a3502002:**
- **#207:** `EngagementDetails.tsx:612` falls back to `current_released_version_id`, and `:616` prints `cloned_from_policy_version_id`.
- **#199:**
  - `ui.tsx:358` strips only `/^answers\[\d+\]:\s*/`;
  - the API still answers `answers[${index}] repeats an answer_key…` (`apps/api/src/routes/inputs.ts:567`).
- **#75, #123:** off-token radii remain:
  - `screens-w1.css:22,34,172` (50%), `:60` (6px), `:157` (999px);
  - `screens-w2.css:19,206` (6px), `:57` (4px), `:68` (999px), `:228` (50%);
  - `screens-w3.css:35` (50%).
- **#201:** `app.css:580` `background: #f7fafd;`.
- **#210:** the Category share is `screens-w3.css:344` `width: 8%`. Whether the word still breaks is **UNMEASURED** (it needs a render).
- **#219:** `ApproversTable.tsx` and `screens-w1.css` set no column width for the approvers table (grep finds none). The rendered width is **UNMEASURED**.
- **#154:** **UNMEASURED** (it needs the computed frame on S9).
- **#108 (b), (d):** **UNMEASURED** (rendered only).

### Lane 2: API and dependency hardening (tier 1, `apps/api` and the lockfile)
**Rows:** #254, #292, #295, #205, #208, #209 (a) (U+16FE4 only; the combining-mark question stays with Friday) and #237 (its two API files).

**Files:**
- `package-lock.json` and any `package.json` the bumps need (root, `apps/api`, `apps/worker`, `apps/idp-mock`, `packages/service-kit`)
- `apps/api/src/routes/engagements.ts`
- `apps/api/src/coverage.ts`
- `apps/api/src/queries.ts`
- `apps/api/src/last-generate.ts`
- `apps/api/src/control-characters.ts`
- `apps/api/src/s47-crf-scan-linear.test.ts`, `apps/api/src/s47-crf2-scan-cost.test.ts`
- `apps/api/test/**`

None of these is in `apps/web`, so the lane is disjoint from Lane 1. The one shared surface is that a dependency bump rebuilds the web bundle too, so Lane 2's gate runs the full `ci.sh`.

**Gate:** tier-1 gate: `ci.sh`, CodeQL, `npm audit` (no moderate or higher), and red-first DB tests per row.
- The Dependabot alert ids need a `gh` login (UNMEASURED today).

**Still open at a3502002:**
- **#254:** `package-lock.json` still pins:
  - `ajv/node_modules/fast-uri` 3.1.7 (`:1832-1833`);
  - `fast-uri` 4.1.4 (`:2429-2430`);
  - `@redocly/openapi-core/node_modules/brace-expansion` 2.1.4 (`:1064-1065`);
  - `fastify` 5.12.3 (`:2445-2446`).

  All are the pre-bump versions named in the row.
- **#292:** `engagements.ts:946` `return reply.header("etag", body.etag)` on setPolicyTarget sends the Engagement body's ETag. B117 re-measured the 412 on the next draft edit.
- **#295:**
  - `engagements.ts:1319-1323` calls `coverageOf(tx, services, …)` per row;
  - `coverage.ts:60` reads `asOfString(nowOf(services))` on each call.
- **#205:** `queries.ts:314` reads "The editable version is in ${version.state}; request changes to return it to draft."
- **#208:** `last-generate.ts:32` uses `name.length <= 200`.
- **#209 (a):** `control-characters.ts:50` `INVISIBLE_ONLY` lists `\u{2800}\u{1D159}` but not U+16FE4.
- **#237:**
  - `s47-crf-scan-linear.test.ts:47-49` and `s47-crf2-scan-cost.test.ts:50-52` still time with `performance.now()` (wall clock);
  - the engine file has the new harness.

**Next candidate, not proposed now:** the runbook-proof trio #290 (c), #291 and #293 (`DEPLOY.md`, `packages/db/test/`). Still open at a3502002: `DEPLOY.md:203-206` applies the script after checking only `echo $?`, with no `dump complete` check. It is disjoint from both lanes, but it is worth less to a salesperson.

## 3. Rows whose text and code disagree

**The row says open, but the code at a3502002 says done:**

| Row | What the row says | What the code says |
|---|---|---|
| #261 | "FIXED on branch … not yet merged" | Merged in `abc97996` (PR #64) and live (C-67). |
| #263, #264, #289 | "OPEN. Needs an API operation first" | Shipped. Contract 0.31.0 (`packages/api-contract/src/document.ts:67-69`: setPolicyTarget, the counts, `requested_hpsm_name` on DeviceProfilePut); web `EngagementDetails.tsx:85,148`, `DeviceEstate.tsx:119,387-393`. Live C-67; gate B117 measured A2, A3 and A4. |
| #266 | "OPEN. Docs only" | `DEPLOY.md:153` "Rolling back a deploy that applied 0021" exists (PR #63). |
| #268 | "OPEN" | `apps/web/src/feedback/types.test.ts:297` reads `"is read from contract 0.31.0"`. |
| #262 | "OPEN … closes when both close" | Both have closed (#266, #268). |
| #202, #267 | "OPEN" | `packages/engine/test/purity-lint.test.ts:26` and `w3r2-minor4-purity-lint.test.ts:53,82` use `ESLINT_TEST_TIMEOUT_MS` (B114, `41c9e470`). |
| #206 | "OPEN" | `Approval.tsx:121-124,150` pass `flowRefresh` to the strip; `:394` `onDone={refresh}` (B116). |
| #211 | "OPEN" | `Release.tsx:1009-1016` catches inside `verify` and shows "Not checked" (B116). |
| #120 | "OPEN" | `FeedbackWidget.tsx:341-349` returns early without `querySelectorAll` or `getBoundingClientRect`. That is #120's own fix shape, landed as #114. |
| #109 | "PART FIXED … not merged" | B52 merged as `5a8254b7` (PR #24). |
| #9 | "BRIEFED … as B04" | B04 merged as `9c7c71db`. |
| #7, #12 | Sub-items "not merged" | Merged in `e0d8a3f6` and `0b2fca43` (C-09 deployed). |
| #270 | "Closes with lane 3c" | Lane 3c is live (C-66). "HPSM Policy Details" appears only in a test that asserts its absence (`b110-create-policy-dom.test.tsx:302`). |
| #290 (a) | — | Done (`41c9e470` on main). Only (b) and (c) remain. |
| #235 | "OPEN" | Its own state records Friday's ruling "(a) — a KNOWN LIMIT", which leaves no work. It could be closed. |

**The row says done (or decides), but the code or the record disagrees:**

| Row | What disagrees |
|---|---|
| #99 | The row says "there is no API operation to open a new version". But `createDraft` exists (`packages/api-contract/src/document.ts:1670`), and #182 says the API exists and only the web control is missing (`Validation.tsx:121` points to "the engagement details", which has no such control). Kam's card on #99 should be framed as a web control plus words, not a new API. |
| #76 | The state contradicts itself. It says "`Approval.tsx:174` … DEPLOYED (C-66)", and later in the same cell "Still OPEN: `Approval.tsx:174`'s inline opacity". Only (b) is really open. |
| #254 | The row records "2 moderate". B118's push read "4 vulnerabilities … (1 high, 3 moderate)" (`Briefs/2026-10-10_B118_STATUS.md`, NOT DONE (b)). The row understates the risk. |
| #84 | The row's fix shape is "retry the host-side edge checks". But `scripts/health-check.sh:44-69` already retries every check until a 90 s deadline, and it is unchanged since S45 (`bb5e02d0`), before B42 saw the race. Either the race is elsewhere (`up.sh`), or the fix shape is stale (UNMEASURED). |

**Not yet rows:** gate B117's findings F1–F7 on B116 (`Briefs/2026-10-10_B117_STATUS.md` FOUND) have no BACKLOG rows yet. The two Minors among them:
- **F1:** a failed re-read after a 409 says "the page now shows it".
- **F2:** "Choose a policy" is offered on a stale-pinned engagement.

## 4. UNMEASURED
- Rendered layout for #210, #219, #154 and #108 (b)/(d). This screen read code only; no browser was run.
- #254: which advisories the alerts are (GHSA ids, the one "high"). No `gh` login was used, and `npm audit` was not run (it would write nothing, but it needs `node_modules` in a worktree I may not create).
- #84: whether the HTTP 000 race still occurs, and in which script.
- #212: the cause of the one-frame 765 px track is "not yet known" (row). It was not probed.
- #150: whether refusing submit on criticals would block any demo example's existing flow. Code-read only (`lifecycle.ts:381-405` refuses only REQUIRED_DISCOVERY_INCOMPLETE among the conflicts read).
- #57, #68: latent on today's content. Not reachable on the demo, so not measured.
- The classes K(F)/A for #104 and #150: both change an API rule a salesperson can see. Friday may prefer to put them to Kam.
- Lane 1's assumption that `apps/web` CSS changes leave the B68 register shares (#142, #145, merged) intact. Re-measure in the gate.
