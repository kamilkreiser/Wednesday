# Composer BACKLOG screen — 2026-10-13 (Friday, read-only)

**Bottom line:** of the 308 rows in BACKLOG.md, 135 are plainly finished. That leaves 173 to classify:

| Bucket | Rows |
|---|---|
| A. An agent can act now | 31 |
| B. Kam has to decide | 22 |
| C. Needs a Datasec SME, Paul or content text | 4 |
| D. Closed, superseded or parked, but the row still reads open | 112 (92 closed or superseded, 20 parked by a ruling) |
| E. Unclear | 4 |

Most of A is web-only work that Kam has already ruled on in C-71. Start with Lane W.

**Sources read:**
- `!CODING/Datasec/Datasec Security Composer/BACKLOG.md`: 308 numbered rows, #1 to #318. Numbers 117–119 and 133–139 do not exist.
- That project's `CLAUDE.md`.
- `1_Project_Definition/CLARIFICATIONS.md`: C-01 to C-74. C-71, the COMP-1 to COMP-19 decisions pack, settles many rows.

**Git (read verbs only):**
- The local clone does not have `ef916ce2`. Its `origin/main` is `9d0e53ff`. Per C-74, `9d0e53ff` is the parent of `ef916ce2`, and `ef916ce2` adds only PR #77 (B144: API refusals, web bundle unchanged).
- So "in main" below means "an ancestor of `9d0e53ff`", checked with `merge-base --is-ancestor`. Anything in it is live on the demo, because C-74 deployed `ef916ce2`.
- Whether `ef916ce2` itself contains a given commit: UNMEASURED locally.

**Method:** the latest update in a row's state cell wins. Where a row's head says MERGED or DEPLOYED and its "Was:" history says "not merged", I counted the row as finished.

---

## A. Agent-actionable now (31 rows)

No Kam ruling, client human or SME text is needed beyond what is already on record.

**C-71's condition still applies:** new words and looks go to Kam on a card before any demo deploy. That is marked "words card" or "look card" below. Building is not blocked by it.

| Row | Fix shape (one line) | Files (from the row) | Size | Auth or security surface? |
|---|---|---|---|---|
| #42 | COMP-13 (a): show "Answers changed after the documents were generated: Generate again" beside "Customer said" when the answers are newer than the last Generate. The words are approved in C-71's words list. Not on main (`git grep`: 0 hits). | `apps/web` Controls (`answered_at` vs the generation time) | S | No |
| #43 | Add each questionnaire item's other mapped questions (`see: [...]`) to the engine table, serve them in the contract, and show "Asked under E04". Words card. | `packages/engine`, `packages/api-contract`, `apps/web` | M | No |
| #57 | The typed editor should write a device-group typed sub-answer per group. Latent: 0 such sub-answers in either release. | `apps/web/src/screens/Discovery.tsx` (`typedDraftFor`) | S | No |
| #69 | Last clause only: reword the contract's 429 description "from this caller" so it covers the failed-sign-in limit too. The web half is deployed (C-72). | `packages/api-contract/src/document.ts:988` | S | Yes, adjacent: sign-in limit wording only, no behaviour change |
| #84 | Retry the host-side edge health checks for a few seconds before printing RED. | `scripts/up.sh`, `health-check.sh` | S | No |
| #95 | COMP-4 (a): remove "they are invited to sign in". It is still there on main at `CreateEngagement.tsx:640`. | `apps/web/src/screens/CreateEngagement.tsx` | S | No |
| #99 + #182 (one fix) | COMP-3 (a): a consultant-only "Start the next draft" on the engagement page, calling the existing `createDraft`. No web caller exists on main. The button label goes to Kam as words first (COMP-3). | `apps/web` `EngagementDetails.tsx`, `Validation.tsx:129` | M | Yes, adjacent: a consultant-only control (role check, using the existing API authz) |
| #104 | COMP-11 (a): no justification needed for a local value, plus one "mark every secret field local" action. | Controls lane (`apps/web` control detail; the justification rule may live in `apps/api`, UNMEASURED) | M | Yes: secret-field handling |
| #106 | COMP-7 (a): set a release signing key at the next deploy. This is an operations step on the deploy card, not code. | Demo VM / deploy runbook | S | Yes: release signing key |
| #107 (c only) | Approval readiness tiles overlap at 1280 ("Dependenci" over "Device"). Measure first: later polish rounds may already have fixed it (UNMEASURED). (a), (b) and (d) are merged. | `apps/web` Approval / `screens-w3.css` | S | No |
| #116 | Screen half: the customer approver's summary should show each exception's reason from `listExceptions`. The API half is deployed (C-70). 0 web callers per the row. | `apps/web/src/screens/w3/approverSummary.tsx` | M | Yes, adjacent: shows the customer approver data that the existing authz-scoped read returns. No authz change. |
| #129 | COMP-19 (a): footer reads "Questions before the session? Ask your Datasec contact." (C-71 words list). Old text still at `ReadySheet.tsx:134-135` on main. | `apps/web/src/screens/ReadySheet.tsx` | S | No |
| #131 | COMP-14 (a): warn, never refuse, on past or far-future due dates. Warning text goes to Kam as words. | `apps/web` `screens/guidedStart.ts`, `w1/validation.ts` | S | No |
| #140 | The off-guide token checker should strip `//` comments, with a self-test. Evidence tooling, not in the code repo. | `Briefs/2026-10-03_B47_evidence/b47-check-off-guide.cjs` | S | No |
| #152 | Add an index `audit_event (tenant_id, entity_type, entity_id)` in a new migration, with a down-recipe. No such index exists on main. | `packages/db/migrations` | S | No |
| #154 | Font half: the withdrawn list's setting key should use the register's monospace. Look card. | `apps/web/src/styles/screens-w3.css`, `w3/withdrawn.tsx` | S | No |
| #158 | COMP-15 (a): add a time zone (Australia/Sydney) on the brand profile, for the cover date only. Where the brand profile lives: UNMEASURED. | `packages/renderers` + brand profile | M | No |
| #166 | Residual only: `DEPLOY.md:150` still says "Not yet run end to end on a seat stack". Gate B63 ran it. Correct the sentence. | `DEPLOY.md` | S | No |
| #169 | Measure `listControls` stale-check cost first; add a cache or change marker only if it shows. | `apps/api` (`buildSnapshot`) | S | No |
| #170 (b only) | Replace the selected-state ring's `box-shadow` (still at `screens-w2.css:133` on main) with a 2 px border or outline. Look card. | `apps/web/src/styles/screens-w2.css` | S | No |
| #178 | Add an additive CHECK `~ '^[0-9a-f]{64}$'` on `policy_version.last_generate_input_hash`. | `packages/db/migrations` | S | No |
| #282 | COMP-12 (a): add the clone sentence ("The source was at Level Three…; the clone starts at the policy's Level Two."). The words are approved in C-71's list. | `apps/web` clone path | S | No |
| #290 (c only) | Add a db test that pins the two-step Route B. (a) is done: PR #63 is in C-67. (b) is a VM read for the deploy seat. | `packages/db/test` | S | No |
| #291 | Run Route B for 0020 on a seat stack. If it refuses, document the two-step form. | Seat stack, `DEPLOY.md` | M | No |
| #293 | Before step 2, check the dump script ends "PostgreSQL database dump complete". The phrase is not in `DEPLOY.md` on main. | `DEPLOY.md` (+ #290's db test) | S | No |
| #297 | Records: add a dated correction under C-65's AMENDMENT ("keeps the data but the policy-target key"). | `1_Project_Definition/CLARIFICATIONS.md` (records seat) | S | No |
| #300 | COMP-5 (a): clear the box when a value is refused as a secret (422 SECRET_VALUE_…). No new words. | `apps/web` (B116 screens) | S | **Yes: secret values on screen** |
| #315 | Footer line budget so `manifest <hash>` survives a long target or customer, with a test at 250 + 200 characters. Kam made it a ticket (C-72). Same defect in the policy PDF. | `packages/renderers` | S | No |
| #316 | `completeExpertSetup` should refuse with 409 or keep an existing target on a pending Guided start. Friday called it a ticket (B144 Q3). New refusal words go on a words card. | `apps/api` `routes/engagements.ts`, `packages/api-contract` | M | No (state guard; not authz) |
| #317 | Add `\p{M}` to the web copy of `INVISIBLE_ONLY`, so the refusal shows inline. Confirmed missing at `deviceEstate.ts:142` on main. Friday marked it optional. | `apps/web/src/screens/w1/deviceEstate.ts` | S | No (input validation) |

### Lanes for bucket A (file-disjoint by directory; 4 lanes)

**Lane W, web (`apps/web/src/**`):** #42, #57, #95, #99+#182, #107c, #116, #129, #131, #154, #170b, #282, #300, #317. That is 13 rows, 12 fixes.

**Lane A, API, contract and engine (`apps/api`, `packages/api-contract`, `packages/engine`):** #43, #69, #104, #169, #316.
- #43 and #104 also touch `apps/web`. Run their web half after Lane W merges (or hand it to Lane W) to keep the lanes file-disjoint.

**Lane R, renderers (`packages/renderers`):** #158, #315.

**Lane O, database, deploy docs, ops and records (`packages/db`, `DEPLOY.md`, `scripts/`, VM, records, Briefs tooling):** #84, #106, #140, #152, #166, #178, #290c, #291, #293, #297.
- #152 and #178 can share one migration.
- #106 belongs on the next deploy card.

**Start with Lane W.**
- **User value:** it holds most of Kam's already-ruled product items.
  - COMP-3 next-draft button (#99/#182, a Medium product gap that two screens already promise).
  - COMP-4 honesty reword (#95).
  - COMP-5 secret-value clearing (#300).
  - COMP-13 hint (#42).
  - COMP-12 sentence (#282).
  - COMP-19 footer (#129).
- **Risk:** it is web only, with no migration, no contract change and no content release.
- **Words:** for #95, #42, #282 and #129 they are already approved in C-71's words list. Only #99's button label and #131's warning text need a words card.
- **Order inside the lane:** #300 first (a security fix, S), then #95, #129, #42, #282 (S, words approved), then #99+#182 (M).

Lane O is low-risk housekeeping, but users see none of it. Lanes A and R carry contract and output changes, so their gates cost more.

---

## B. Kam's decision (22 rows)

| Row | The decision | Options the row offers | Ruling on record |
|---|---|---|---|
| #26 | `migrate` refuses unknown recorded migrations: tolerate them, or adopt a down-migration convention in the migrator | Tolerate / convention | None. In practice each migration since has shipped a down-recipe (0019, 0020, 0021 per #25, #166, #266). Kam or Friday could close this as "convention adopted". |
| #75 | `#ffffff` literals → a new token (`--pc-on-primary`), plus the held 50 % / 999px shapes | Approve a token change / keep | None. `#ffffff` is still in 20+ CSS lines on main. Change 5 of #73 is parked (COMP-17), but this token question is not named there. |
| #123 | The same token question (`#ffffff`, 50 % / 999px) on the Expert screens | As #75 | None |
| #193 (half 2) | Who adds the customer approver for a client a Guided user created | A platform administrator (as now) / option (b) in `B67_STATUS` Item 3 | None. Half 1 is ruled and merged (C-35, PR #38). Guided is OFF; COMP-2 may hold it. |
| #214 | Q4: may an unreleased version be the starting point for a copy? Also B89 N3: three sentences still say "in this tenant" (words) | Yes / no | None found in CLARIFICATIONS |
| #247 | A stray 15-byte file `/opt/hpsm/524337` on the demo VM: may a deploy seat read it and quarantine it? | Read and quarantine / leave | None. The demo is Kam's (CLAUDE.md). |
| #257, #286, #287, #288, #306, #307 | Six small look items (pill over G01's notes box, step-3 tick, layout notes, "Not chosen" with no reason, input widths, 5 px radio shift) | Accept / change | C-71 COMP-18 (a): Friday brings **one look card with screenshots**. The card is not yet ruled. Next step: an agent builds the card; then Kam decides. |
| #269 | Residue: relabel the generation block's "Policy <HPSM name>" (B134 Q1 is Kam's words), and the package manifest's title | Relabel / keep | Worksheet and change report are done (C-72). Friday's C3 holds the file names. The relabel has no ruling. |
| #271 + #273, #277, #280, #281, #284, #304, #309 | The seven pending error and refusal phrasings. #271 is the question and #273 the build for the same POLICY_ALREADY_EXISTS sentence. | A proposal each | C-71 COMP-19 (a): they come to Kam on **one words card with a proposal each**. Not yet ruled. Next step: Friday drafts the card. |
| #318 | The B67_BLANK contract sentence should name combining marks | Reword / leave | None. Friday: "wording is Kam's". It could ride on the COMP-19 words card. |

---

## C. Needs a Datasec SME, Paul or content text (4 rows)

| Row | What is needed |
|---|---|
| #15 | Q-13 ratification of the B09 typed answers and 28 mappings (12 SME items) by a Datasec SME and a second person. C-57 names Kam and Paul as interim reviewers of the **E8 mapping** only. Whether that also covers Q-13: UNMEASURED. |
| #249 | Lane 3a content release: BLOCKED on Kam and Paul's check of the E8 mapping, then Kam's approval (C-57) |
| #253 | The SME check itself: names, date and changes recorded in the DRAFT file's `sme_check` (C-57 named the reviewers) |
| #265 | `online_service_in_use` links have no deciding item. Part of the SME check (C-57, #253's list); no code before then. |

---

## D. Closed, superseded or parked, but the row still reads open (112 rows, for the records seat)

### D1. Closed or superseded (92 rows)

**Merged into main and live, but the row still says "not merged" or "not deployed".** Each commit was checked as an ancestor of `9d0e53ff`.

- **#7:** 7c went in through PR #7 `e0d8a3f6`; 7a and 7b through PR #6 `3b9a663`.
- **#9:** the B04 mobile pass merged as PR #2 `9c7c71db`; the row still says "BRIEFED".
- **#12:** 12a went in through PR #8 `0b2fca4` and 12c through PR #7.
- **#18:** the row's own note says it is stale (C-09).
- **#24:** superseded by C-24; built and merged as PR #25 `eb364cc` (see #88).
- **#28, #85, #111, #122:** `e36fcde`, deployed C-41.
- **#39, #40, #44, #45, #46, #47, #48:** `0412eb6`, deployed C-14.
- **#93, #100, #102** (`e00ffe9`), **#94, #163** (`3fad49a`), **#98** (`6d026a7`), **#103** (`ff751b8`), **#114** (`51bec14`), **#124** (`461e083`), **#141** (`eda2623`): all deployed with C-33 `6d026a7`.
- **#96, #121** (`7377099`), **#203, #204** (`d09c895`): deployed C-43.
- **#109:** its other half is in #77, merged.
- **#112, #181, #185, #186, #187, #192, #196:** `b2cb29d`, deployed C-44.
- **#125, #126, #130, #132, #174:** `3d92736`, deployed C-41.

**Closed by a ruling, but the row still reads OPEN:**
- **#66, #70, #71:** Friday C5.
- **#79, #120, #151, #180, #202, #222, #235, #262, #266, #267, #268, #270, #283:** Friday C13.
- **#157, #176:** Friday C7.
- **#164, #212:** Friday N2.
- **#172, #173:** COMP-8.
- **#197:** Friday C8.
- **#246:** Friday C9.
- **#259:** COMP-18, "the breadcrumb item is accepted as before".
- **#260, #285:** COMP-9.
- **#278:** COMP-10.
- **#312:** COMP-6. The row still says "KAM DECIDES".
- **#313, #314:** Friday C10.

**Deployed, but the stale words "OPEN, next round" remain:**
- **#159, #160, #161:** C-72, "Open / held part: none".
- **#302, #310, #311:** C-72, test-only.

**Fixed on main, checked with `git grep`:**
- **#67:** no `skip(` left in `b09-example-flow-through.spec.ts`.
- **#72:** 0 `HPSM-light` mentions at `9d0e53ff` (C-72).
- **#241:** `querySelectorAll` is in `fakeDom.testing.ts:286`.

**Superseded by later rows or work:**
- **#1** (guide v1.2) and **#17** (v1.3): v1.4 and v1.5 folders now exist in `User_Guide/`. Whether v1.5 was sent to Paul: UNMEASURED; no row tracks it.
- **#3:** its blocker #2 is DONE, and CLAUDE.md says all 74 branches are carried as remote-tracking refs.
- **#21:** examples rebuilt; EXAMPLE A and B have been in use since (C-68 and later). Inferred; no Kam acceptance is recorded.
- **#215:** the build is now #249.
- **#218:** the build is now #248–#252.

**Information or deploy-prep notes with nothing left to do:** #61 (INFO), #64 (prep for the C-15 deploy, long past), #276 (INFORMATION ONLY).

### D2. Parked by a ruling (20 rows)

Nothing to build until Kam unparks them. Mark them PARKED rather than OPEN.

- **COMP-17**, "keep all six parked":
  - #4
  - #41
  - #54 (C1 half; the DEL half was fixed by PR #38)
  - #73 (change 5)
  - #101
  - #108 (a)
- **COMP-2**, "hold them all; no Guided work until you turn it back on":
  - #30, #35, #55, #223, #226, #228, #231, #240
  - #108 (c)
  - **#76 (b)** and **#83 (End half):** both are Guided-only. COMP-2 does not list them, but its words "No Guided work" cover them. Friday should confirm that reading.
- **COMP-16**, "hold both": #227, #236.
- **COMP-1 (b)**, "after Paul's current review round": #252, #272.

(#108 appears once and is held by both COMP-17 and COMP-2.)

---

## E. Unclear (4 rows)

| Row | What is missing |
|---|---|
| #27 | Partly answered: C-72 and C-74 show that `remote-update.sh` runs migrate ("migrations applied: none; already applied: 21"). Still missing: whether the VM's deploy scripts should be copied into the repo, and confirmation of the container names. That needs VM read access, which only Kam's deploy grant gives. |
| #34 | Whether Friday still wants a proof of "rolling back past B22". The demo is now many deploys past B22; the recorded way back (C-72, C-74) goes one build at a time. |
| #171 | Whether to close: Composer's `pc-*` networks are 0 after C-73. The 31 networks left belong to another Datasec project, so the remaining pool pressure is not a Composer item. |
| #258 | The README note is deployed (C-67). The process question (calibrate e2e pixel checks to a real font, or measure in a host browser) is "Friday's to close or commission". No ruling is recorded. |

---

## Summary

All counts are taken from the lists above.

| Bucket | Rows |
|---|---|
| Rows in BACKLOG.md | 308 |
| Plainly finished (not listed) | 135 |
| A. Agent-actionable now | 31 (30 fixes: #99 and #182 are one) |
| B. Kam's decision | 22 (14 of them already routed to one look card (COMP-18) or one words card (COMP-19)) |
| C. SME, Paul or content | 4 |
| D. Closed, superseded or parked, row reads open | 112 (D1 closed or superseded 92, D2 parked by a ruling 20) |
| E. Unclear | 4 |

**Check:** 31 + 22 + 4 + 112 + 4 = 173 classified, and 173 + 135 = 308.

**Closed count:** 135 plainly finished + 92 closed or superseded (D1) = **227 closed**. The 20 in D2 are parked, not closed.

**UNMEASURED:**
- Whether `ef916ce2` itself contains a given commit; checked against its parent `9d0e53ff` instead.
- #107 (c) on today's main.
- Where the brand profile lives (#158).
- Whether #104's justification rule sits in the API.
- Whether guide v1.5 was sent to Paul.
- Whether C-57 covers #15.
