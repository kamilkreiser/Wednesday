BLUF: 55 tickets could be completed by an agent now, with no new user-facing word, no ruling, no production touch: MPS Commercial Calculator 20 (1 of them conditional), HPSM-POC 8, Security Composer 12, NexusAI 20 (the NexusAI 20 are all test, tooling, CI or dead-code work; its product-code security fixes are held back as Opus-tier, not counted). Top lanes by value: (1) MPS M1 "API and contract" serial lane (204, 316, 290, 322, 325, 169, then 176) because the product owner's rulings of today unblocked 204, 316 and 176 and #102 landed; (2) MPS M2 "store and engine hardening" (323, 326, 327, 324), the fresh #102 gate follow-ups, one Major among them (322); (3) Composer L3 structure lane (PCOMP-40 to -44, ruled, plan says no card); (4) HPSM-POC test-teeth lanes P1 to P4 (320/327, 326/323, 328, 314/319), test-only. Separately, 112 MPS, 19 HPSM-POC, 8 NexusAI and 1 Composer tickets look done on main but are still open: record-seat Done candidates (section A). No lane shares a path with another lane of the same project except where stated as serial.

# Datasec: tickets an agent could complete now (read-only research, 2026-10-24, about 15:00 AEDT)

Researcher: read-only sub-agent for Tuesday. Wrote this one file. No Jira write, no mail, no chat, no publish tool, no HTTP to any hosted or production host, no `az`, no decision_queue/fleet_ack/scoreboard/briefs_staged, no git write verb. Jira = GET `/rest/api/3/search/jql` and issue/comment GETs only, every JQL `project = <KEY> AND ...`, credentials read inside the process from each project's own `4_Credentials/.env`. GitHub = `gh api -X GET` under each project's own `GH_CONFIG_DIR` (PR lists, one main-sha read, one tarball of MPS main `05c598f3` into the scratchpad). Scope: MPS (MPSCALC), HPSM-POC (HPSMPOC), Datasec Security Composer (key PCOMP, `JIRA.md:4`), NexusAI (RD). myPKI, CypherKey, Lead_Bot skipped.

## 0. How I measured (every count names its query)

| Count | Query / command | Result |
|---|---|---|
| MPS open | `project = MPSCALC AND statusCategory != Done`, paged by nextPageToken until isLast | 313 rows, all status `Backlog` (not capped) |
| HPSM-POC open | `project = HPSMPOC AND statusCategory != Done` | 126 rows: 123 Backlog, 3 In Progress (-87, -90, -91) |
| Composer open | `project = PCOMP AND statusCategory != Done` | 93 rows (4 epics), all Backlog; labels `held` 19, `needs-kam` 2 |
| NexusAI open | `project = RD AND statusCategory != Done` | 759 rows: To Do 369, Release Ready 199, Testing 172, In Progress 10, Put on Hold 7, Declined 2 |
| PRs | `repos/<repo>/pulls?state=all&per_page=100 --paginate` | MPS 106 PRs, HPSM-POC 207, NexusAI 100 (newest 100, capped by my page limit of 1 page, NOT paginated: older PRs unread) |
| Open PRs | `pulls?state=open` | MPS 0 rows; HPSM-POC 1 (#207); Composer 2 (#85 draft, #86 dependabot vite); NexusAI 1 (#67, stale since 7 Oct) |
| Mains | `commits/main` | MPS `05c598f3` (2026-10-24T03:24Z); HPSM-POC `8cd2c7f0` (03:25Z); Composer `308b7aa6` (2026-10-20); NexusAI `6a69fdf4` (2026-10-22) |

Jira status rule: MPS, HPSM-POC, Composer do NOT move status on merge (`JIRA.md` of MPS, quoted in the MPS ticket comments "no project rule moves a ticket on merge"; HPSM-POC and PCOMP rows are all Backlog despite merges). NexusAI does move status (CLAUDE.md:301-302: code change goes to `Testing`, a human moves it to `Release Ready`), so for RD the status field is evidence. I judged "done" from merged-PR text, main's code and the seats' own Jira comments.

Rulings of today (24 Oct) quoted by the caller are NOT yet in `CLARIFICATIONS.md` (its newest entry is C-56 at `1_Project_Definition/CLARIFICATIONS.md:1111`, tuesday section at :1121). I cite them as "caller context, 24 Oct". Rulings that are on file are cited with file:line.

## 1. MPS Commercial Calculator: 20 completable

Base: main `05c598f3`, 0 open PRs (query above), so no partition clash with an open PR. #102, #104, #105, #106 landed (L1/L2/L3 of the morning plan are all done: #105 = 228/195/219, #106 = 291/292/293/294, #104 = 318/319/320/303/200 partly). The morning file `2026-10-24_mps-next-lanes.md` listed 161/169/170/288/204 as blocked by #102: that block is lifted. Everything below was re-checked against the main tarball: 161 has no archive route (no hit for `archive` under `src/MpsCalc.Api`); 176 has no triage symbol (only unrelated proposal-template hits); 218 has no re-order row; 313 still compares `r.group` at `web/src/api/stub/stubApi.ts:209`; 316's wording is still "at most 100 characters" at `docs/API.md:425` and `docs/api/openapi.json:369`.

Ranked by value. Model tier is Sonnet seat unless stated. Gate: tier-1 QA gate for anything that touches `QuoteEndpoints.cs`, the engine, or stores.

### Lane M1: API and contract (SERIAL, one seat at a time; shares `QuoteEndpoints.cs`, `Dtos.cs`, `docs/API.md`, `docs/api/openapi.json`, `web/src/api/generated/**`)

| Order | Key | Summary | Why completable now | Paths | Size | Must NOT |
|---|---|---|---|---|---|---|
| 1 | MPSCALC-316 | Docs say quoteRef "at most 100 characters" but the API counts UTF-16 units | Ruled today (caller context): state the unit, "at most 100 UTF-16 code units (an emoji counts as two)". Ticket fix-shape is the same two doc places (`CLARIFICATIONS.md:856`, `BACKLOG.md:2361`) | `docs/API.md:425`, `docs/api/openapi.json:369`, regenerated `web/src/api/generated/schema.ts` and `openapi.snapshot.json` (they carry the phrase) | S | Not change the counting rule or any behaviour; not edit `QuoteEndpoints.cs` (it also holds a "100 char" hit; comment only, leave) |
| 2 | MPSCALC-290 | The unchanged-save sentence is false for a restricted owner of a purchase quote with manual items | Ticket recommendation: narrow the docs sentence | `docs/API.md`, `docs/api/openapi.json` | S | Not change `PricingPolicy.Apply` order |
| 3 | MPSCALC-204 | Out-of-range refusal: two lines at decimal minimum; range check answers before owner/state/existence | Ruled today: who and state first, then range (caller context; #102 landed, so the blocker named at `CLARIFICATIONS.md:1101` is gone). The "one line not two" half needs no ruling (`BACKLOG.md:1701-1705`) | `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (call site `:1534`), `Quotes/PurchaseValidation.cs`, tests | M | Not add a sentence (existing refusal words only); not change the numeric bounds |
| 4 | MPSCALC-322 | Body refusal prints a caller-chosen member name back whole (1,000,000 chars in, 2,000,115 out; CR/LF/NUL pass) | Filed today by gate B552 (Major, open instance of B538-1); C-55/C-56 (`CLARIFICATIONS.md:1101,1111`) approved only the root-case sentence, this fix needs no new sentence (bound/escape the existing detail) | `QuoteEndpoints.cs:1317-1320`, tests | S-M | Not introduce a new refusal sentence; if the only fix needs one, stop and word-pack it |
| 5 | MPSCALC-325 | Four draft-validation walks grow the answer with the input and stop at no cap (30 MB answer) | Gate B552-F1; hardening, tier 1 | `Quotes/PurchaseValidation.cs`, `QuoteEndpoints.cs` | M | Not add an "and N more" line unless the existing wording already has one (that would be a new word: stop and ask) |
| 6 | MPSCALC-169 | Name the source set the lineMarkups were resolved on | `QuoteEndpoints.cs:1012-1079` builds `LineMarkups` (next-lanes file); contract-only, a field beside `lineMarkupsOverlayVersion`, tier 2 | `QuoteEndpoints.cs`, `Dtos.cs`, openapi, API.md, generated, tests | M | Not show it in the UI (a label would be a word) |
| 7 | MPSCALC-176 | Feedback triage (status, priority, notes) for Administrators + "My feedback" for senders | Word pack approved today (caller context); acceptance "words approved first" is met; proposal lane #105 (which owned the contract files) is merged. Greps: no triage symbol in `src`/`web/src` | `src/MpsCalc.Api` (feedback), `Contracts/Dtos.cs`, openapi, API.md, generated client, `web/src` screens | L | Not ship wording other than the approved pack; triage sidecar must never rewrite the item file (acceptance) |

Opus note for M1: none. Sonnet with tier-1 gate (322, 325), tier-2 for the rest.

### Lane M2: store and engine hardening (disjoint from M1 except 324, which is serial after both)

| Order | Key | Summary | Why completable now | Paths | Size | Must NOT |
|---|---|---|---|---|---|---|
| 1 | MPSCALC-323 | Store file unopenable at first use keeps every source route 503 until restart | Gate B552-2 (Minor, new), regression vs previous head; fix = do not cache the failed first result | `src/MpsCalc.Api/Sources/ActiveSources.cs:100-105`, tests | S | Not change the operator line words |
| 2 | MPSCALC-326 | Null `tierPool` in a stored rental device row gives a 500 on rental calculation | Gate B552-F2 (Note, FACT) | `src/MpsCalc.Engine/Calculation/QuoteCalculator.cs:73-75`, tests | S | Not change any calculated figure; refusal, not default |
| 3 | MPSCALC-327 | A store with a null member is served with bodies that break the contract (40 of 188 cases) | Gate B552-F3; file path only, the governed path already refuses | `src/MpsCalc.Import/Store/ReferenceStoreDocument.cs`, `Sources/ActiveSources.cs`, tests | M | Not touch imported price rows or any real price-book data (synthetic fixtures only) |
| 4 | MPSCALC-324 | Four survivors of #102's own code (last body-refusal branch; store-load fault catch widened) | Test-only rows | tests; read-only on `QuoteEndpoints.cs` and `ActiveSources.cs` | S | Not change product code; runs AFTER M1-322 and M2-323 so the rows pin the final code |

### Lane M3: web small (disjoint from M1 and M2)

| Key | Summary | Why | Paths | Size | Must NOT |
|---|---|---|---|---|---|
| MPSCALC-313 | Stub mode cannot answer readyToExport or create a quote | `stubApi.ts:209` as ticketed; no words | `web/src/api/stub/stubApi.ts`, `web/e2e/b28.spec.ts`, `b30.spec.ts` | S | Not touch the real API client |
| MPSCALC-321 | Fleet grid: no row pins the focus rule width after Remove | Filed today, test-only | `web/src/screens/FleetGrid.tsx:41` area, a new test | S | Not change the focus rule |
| MPSCALC-317 (CONDITIONAL) | Add section before the price list loads starts without the 7% default | Ruled C-46 Q8 b (`CLARIFICATIONS.md:889`): ship, file a small ticket. Fix = disable Add section until inventory loads. A disabled hint would be a word | `web/src/screens/QuoteScreen.tsx:99-100`, `bom/PurchaseBomEditor.tsx:141`, `bom/bomModel.ts:51-53` | S | Not add any hint text; if the fix needs one, stop and word-pack |

### Lane M4: tests and scripts (disjoint from all)

| Key | Summary | Paths | Size | Must NOT |
|---|---|---|---|---|
| MPSCALC-218 | Price-audit tests lack re-order and description rows (my grep for re-order terms in `TargetWhatIfAuditApiTests.cs` returned 0 hits, so still open) | `tests/MpsCalc.Api.Tests/TargetWhatIfAuditApiTests.cs`, `CareKeyPatternApiTests.cs` | S | Not change `PriceAudit.cs` |
| MPSCALC-221 | Secret-scan false positive on a synthetic care key (`CareKeyPatternApiTests.cs:15`, constant still `care_0123456789abcdef01234567`) | same file as 218, so one seat does both | S | Not run or add a secret scanner |
| MPSCALC-205 | `package.sh` refuses a tree holding a Release build with unhelpful words | `scripts/package.sh` (guard near :45) | S | Not deploy or package for a host; operator message words only if they already exist (else word-pack) |
| MPSCALC-201 | Entra script follow-ups (group lookup before writes, flags) | `scripts/entra_apps.py` | S | NEVER run it against Entra; edit only |

### Opus-tier, completable (a recommendation exists, no ruling needed; run on Opus with a tier-1 Opus gate)

| Key | Summary | Why Opus | Paths |
|---|---|---|---|
| MPSCALC-288 | `callerCan.approve` false for a Blocking snapshot while reject still answers 200 | approval-design surface | `QuoteEndpoints.cs` (so serial AFTER M1), contract, tests |
| MPSCALC-302 | `prove` says AGREE for a count-preserving tamper | integrity-check design (`ParityProof.cs`) | `src/MpsCalc.Import/**` parity (disjoint from M1/M2) |

Total MPS: M1 7 + M2 4 + M3 3 (1 conditional) + M4 4 + Opus 2 = 20.

### MPS: looks completable but is NOT (excluded, with the reason)

- MPSCALC-153 (ink hint $0.70 editable): the ruling is in, but the product owner wants the words first; the hint is a new customer-facing word. Build can start, shipping cannot. Not counted.
- MPSCALC-261 (credits follow the normal approval rule): ruled today; also `CLARIFICATIONS.md:989-994` (C-50, Review issue raised, Approver approves). Money/approval logic (Opus tier), calc-register lane V4, and "a Review issue for any credit" is a new Review sentence = word pack first. Not counted.
- MPSCALC-161 (archive a quote): no ruling needed, but the quotes list gets a new action and confirmation (new words). Not counted.
- MPSCALC-170 server half: the "fleet[n]" refusal naming (B38-L1) is a refusal sentence change. Not counted.
- MPSCALC-195 residue: the rate-limit parenthesis is "one decision open" (PR #105 body). MPSCALC-200: needs real price-book counts (confidential, owed).

## 2. HPSM-POC: 8 completable (all test-only or CI; no word, no deploy)

Base: main `8cd2c7f0`. One open PR: #207 (HPSMPOC-334/-335/-336 tests, in CI). Those three are in flight, excluded. Lanes below avoid #207's paths (`attribution-preview.test.ts`, the `describeFailure` customer-name table test, `ApiFactoryHostStartRetryTests`).

| Lane | Key | Summary | Why completable (record) | Paths | Size | Must NOT |
|---|---|---|---|---|---|---|
| P1 | HPSMPOC-320 | UatOpenTests refused rows: B476-5 and B476-6 still open | Seat comment 2026-10-23 11:45: "stays open: B476-1 and -2 closed (PR #191), -5 and -6 not"; test-only | `api/tests/HpsmPoc.Api.Tests/Auth/UatOpenTests.cs` | S | Not change `UatOpenAuthentication.cs` |
| P1 | HPSMPOC-327 | UatOpenTests offset rows do not pin their own token life (mutants P4a/P4b survive) | Ticket "Done when (a test)" is precise | same file as 320, so same seat | S | Not change product code |
| P2 | HPSMPOC-326 | Held-name allowance: a name with MORE edge space is not pinned (mutants X8/Xm8) | Ticket "Done when (a test)"; PR #189 merged | `api/tests/.../Hpsmpoc178CustomerNameTests.cs`, `web/src/server/mock/customer-name.test.ts` | S | Not change `Requests.cs:146` |
| P2 | HPSMPOC-323 | Web/mock side: B478-4 (mock first-400 versus API list shape) still open; -2 (#197) and -5 (#202, #205) merged | Seat comment 24 Oct 05:05 | `web/src/server/mock/**` | S | Not change the wording of any message |
| P3 | HPSMPOC-328 | e2e runner source-text pins: four `liveApiRun` mutants (LR1/2/4/5) green; two more instances found by gate B523 | Test-only; ticket Done-when | `web/scripts/e2e.mjs:402-409`, `web/src/e2e-runner.test.ts:751-765` | S-M | Not run the live API mode against a hosted host |
| P4 | HPSMPOC-314 | SQL Server shard `api-other-and-feedback` grows toward the 20-minute limit (green max 18.32 min) | Ticket: measure per-namespace time and rebalance the two filters; CI-only | `.github/workflows/ci.yml` (matrix `:171`, filters `:247`) | M | Not change which tests run in total; not raise the limit without the measurement |
| P4 | HPSMPOC-319 | HostStartRetry: B469-5 (error number 1223 unproven at runtime) is the one item not met; -2 and -3 met | Seat comment 24 Oct 05:06 | `api/tests/.../Support/FeedbackApiFactory.cs`, `ci.yml` | S | Wait for #207 to merge first (it adds `ApiFactoryHostStartRetryTests`) |
| P5 (CONDITIONAL) | HPSMPOC-322 | Grouped executive summary: B477-5 (allowed-number set is global), -6 (title with "; " is ambiguous) | Minor, in `Reporting/Narrative/*`; B477-7 is a design choice and B477-8 is wording, so only -5/-6 | `api/src/HpsmPoc.Modules.Reporting/Narrative/Providers.cs`, `NarrativeOutputValidator.cs` | M | Not change the approved sentences (words ruled 22 Oct); stop if -5 needs one |

Counted 8 (P1 2, P2 2, P3 1, P4 2, P5 1). Unverified extra: HPSMPOC-228 (site-timing notes N-2..N-9; the 16 Oct comment says N-3/N-4/N-7 closed by PR #152; N-2 "drop the dead regex in `bff.ts`" looks open) is a small S candidate; I did not read the code, so it is not counted.

Partition: P1 (`Auth/`), P2 (`Assessment` tests + web mock), P3 (`web/scripts` + runner test), P4 (`ci.yml` + test support), P5 (`Reporting`): no shared path. P4/319 waits on #207.

## 3. Datasec Security Composer (PCOMP): 12 completable

Base: main `308b7aa6` (20 Oct); 2 open PRs: #85 (draft, "HOLD K6", the L1 content catalogue; C-97 `CLARIFICATIONS.md:1736`) and #86 (dependabot vite 8.3.0 to 8.3.4). Rulings on file: C-91 remediation states (`:1671`), C-92 content release waits for the reviewer round (`:1682`), C-94 (`:1704`), C-95 words card per lane (`:1715`), C-100 template approved (`:1777`). C-92 only holds CUTTING/DEPLOYING a content release; building on branches is allowed (C-100 "Does not settle (4)").

| Lane | Key | Summary | Why completable | Paths | Size | Must NOT |
|---|---|---|---|---|---|---|
| C-L3 (serial, shares one new migration and a contract bump) | PCOMP-43 | Document version and policy version as two numbers (L3-5) | Plan: no card needed; ticket text "the coordinator may start it" (after L3-1, #83 merged 2026-10-20) | `packages/db/migrations/*`, `rollback/*.down.sql`, `apps/api/src/**` | L | Not deploy; new screen words to a words card first (C-95) |
| C-L3 | PCOMP-44 | Output kinds `sm_policy_json`, `sm_policy_csv` added to the contract enum for L7 (L3-6) | same | `document.ts:173-199`, migration | M | Not build the export itself |
| C-L3 | PCOMP-40 | Attribute overrides stored (today 422 `ATTRIBUTE_OVERRIDE_NOT_BUILT`) (L3-2) | same | `document.ts:696`, `snapshot.ts:183`, migration | L | Not change released content |
| C-L3 | PCOMP-41 | Engagement governance record (L3-3) | same | migration, api | L | same |
| C-L3 | PCOMP-42 | Remediation states "after validation" and "controlled/staged" (L3-4) | Ruled C-91 (a); sibling C-23 applies to "auto" only | migration, contract | L | State names go on the words card before deploy |
| C-T | PCOMP-22 | Route B restore script: check the dump script is complete before step 2 | Ticket fix-shape exact (`tail ... grep 'PostgreSQL database dump complete'`) | DEPLOY Route B script and #290's db test | S | Not run against the demo VM |
| C-T | PCOMP-62 | Flaky web test `b116-s10-verify-dom.test.tsx:120` (waits on turns, not state) | gate fix-shape given | that test | S | Not change product code |
| C-T | PCOMP-63 | Comment-only: state the split-bound limit in `SINGLE_SPLIT_BOUND` comment | one sentence | `packages/engine/test/s47-...` | S | Not change a test |
| C-P | PCOMP-23 | Change-report footer drops its manifest hash line with a long target name | Owner's card (a): "a ticket for later"; fix-shape: footer line budget + test at 250+200 chars | PDF/report footer code | M | Not change other layout |
| C-P | PCOMP-12 | Expert typed editor writes every declared sub-answer at engagement level (latent, API refuses with 400) | code-read bug with exact file | `apps/web/src/screens/Discovery.tsx` (`typedDraftFor`) | M | Not change the 400 refusal |
| C-D | PCOMP-17 | `last_generate_input_hash` char(64) accepts a 63-char value: add a hex CHECK | additive migration | migration (take the number AFTER C-L3 so numbers do not collide) | S | Not alter existing rows |
| C-D | PCOMP-14 | Index on `audit_event (tenant_id, entity_type, entity_id)` | Low; additive migration; same migration-number rule | migration | S | Not combine with 17 in one migration without the migration owner |

Total 12. Partition: C-L3, C-T, C-P, C-D touch different directories, but ALL migrations (C-L3, 17, 14) are serial because they take the next migration number. Also available, not a ticket: dependabot #86 vite bump (S, CI only).

Not counted: PCOMP-82 (cover date in Sydney time, ruled COMP-15 a, changes a printed date label = word), PCOMP-77 (adds a "mark all local" action = word), PCOMP-31..39 (L1/L2, wait on the #85 hold and the content loader; L2-3 is a words card), PCOMP-67 (rides on #85's branch; the coordinator's choice), PCOMP-66 (struck by Tuesday).

## 4. NexusAI (RD): 20 completable, all test/tooling/CI/dead-code

Base: main `6a69fdf4` (22 Oct), 1 open PR (#67, 7 Oct, stale). NexusAI lands by same-commit fast-forward only (PR #105 body: "never squash, never rebase"), every product change needs a QA gate, and each new test suite changes `scripts/verify-expected-counts.json`, so any two lanes that add suites must be serial on that file (this is the partition rule for N1 and N2).

| Lane | Keys | Summary | Why / evidence | Size | Must NOT |
|---|---|---|---|---|---|
| N1 test cells (`__tests__/**`, counts file) | RD-860, RD-864, RD-865, RD-866, RD-871, RD-877, RD-818, RD-825, RD-873 | Add the missing red-proof cells named by gates 14 to 31: SVG title escape (860), real user sharing a word (864), whole-prompt pin (865), override cell seeds the wrong provider key (866), singular group noun (871), two surviving mutants (877), freeze narrowing (818), array-shaped role (825); RD-873 = CodeQL `js/insecure-temporary-file` alerts #95-#99 and #116 in test code | Each ticket states the mutant and the ask; "Ask: add a cell". RD-873's comment of 21 Oct: #95-#99 and #116 untouched | M (9 tickets, one seat) | Not change product code; not dismiss CodeQL alerts; counts file regenerated once |
| N2 tooling and CI | RD-847, RD-850, RD-851, RD-852, RD-854, RD-844, RD-827, RD-814, RD-815 | Lock tool BASE hard-coded to the old drive (`session-tools/nexusai-lock.sh:79`); Dockerfile-stage guard gaps (`__tests__/helpers/dockerfile-stages.js`); rd490 browser guard waits on cdnjs; stale shared `node_modules` (project folder only); workflow permissions and unpinned tags (CodeQL mediums, `.github/workflows/*`) | tickets read; tool/CI/config only | M | Not deploy; not change the Container Apps; 814/815 are workflow-permission changes: Sonnet with a security-minded gate |
| N3 server (`backend/server.js`, one seat) | RD-862, RD-876 | Remove dead `generateSQLFromCondition` (`server.js` about 6391-6497, no caller; Tuesday asked for it, ANSWER-24); restore the hard LIMIT on the default risk template (gate 29 N29-6) | RD-774/836 landed (PR #97), so the "remove after RD-774 lands" condition is met | S | Not change any other route; 876 is behaviour: tier-1 gate, Opus if the gate wants it |

Count 9 + 9 + 2 = 20. Opus-tier (not counted, completable by Opus with a tier-1 gate): the CodeQL product-code baseline (RD-762 to -773, -764 auth bypass, -765/-766 ReDoS, -769 property injection), RD-633/-634/-711/-744/-758/-793 security. RD-878 (non-string `risk_level` answers 500) would add a 400 sentence = word pack first.

## A. Look done on main but still open: record-seat candidates for a Done transition

Only the record seat moves Jira status. "Evidence" = merged PR number from the PR list read above.

- **MPS (112 tickets, all `Backlog` now):**
  - 74 strong (named in the 24 Oct next-lanes record section 3b and in #104/#105/#106 text, and every one confirmed non-Done by the open-set query): 137, 172 (#95); 174, 165 (#96); 160, 150 (#97); 151, 262, 263, 266 (#86); 198, 199, 208, 220, 301 (#103); 197, 211, 104 (#99); 189-193 (#100); 229 (#101); 214, 213, 231, 289, 304-311 (#82/#80/#83/#93/#92/#91); 244, 28, 245 (#89); 238-242, 249, 296-299, 27, 34 (#88/#90); 232-236, 209 (#85); 312 (#98 wording); 215, 216, 210, 217, 196, 230 (#102); 228, 219 (#105); 291, 292, 293, 294 (#106); 303, 318, 319, 320 (#104).
  - 38 title-only (merged PR title names the key; each needs a one-line check because a title can be a partial or a cross-reference): 95 (#33), 98 (#34), 100 (#35), 105 (#71), 109 (#49), 111 (#48), 136 (#67, web half only, Entra step open), 138, 186 (#51), 140 (#78, #74), 141 (#65), 142 (#76), 143 (#52), 145 (#68), 147 (#69), 156, 157 (#50), 158 (#77), 162, 164 (#59), 163 (#58), 166 (#56), 167 (#57), 168 (#55), 170 (#64; server half open), 171 (#54), 173 (#47), 175 (#53, #43), 177 (#44), 178 (#47), 179 (#63), 180 (#46), 182 (#66), 183 (#72), 184 (#45), 194 (#79), 203 (#81, retention half only), 227 (#84).
  - NOT done despite a merge mention: 195 (one decision open), 200 (counts owed), 295 (words only, unbuilt).
  - Counts: union computed by script = 112 (74 + 38). Query: set of keys in titles of merged PRs intersected with the open set.
- **HPSM-POC (19, each has a seat comment or PR saying merged):** HPSMPOC-187, -204 (#186); -177, -178 (#187, #189); -218 (#196 date fix; #206 removed the withdrawn braces exception: confirm the ticket's own done-when); -254 (#157; the hosted runtime half stays in -268); -292 (#171); -296, -297 (#193, #196); -310 (#192, #194; word 5a recorded); -311, -316 (#198); -312 (#185); -313, -317 (#201); -315 (#200); -318 (#199); -331 (ticket says "done in PR #203"); -333 (#205). Partial, keep open: -319, -320, -323, -308 (new instances after #183/#199).
- **Composer (1):** PCOMP-52 (L6-a policy PDF contents page, merged as #84 on 2026-10-20; the "Contents" word still needs the words card before a deploy, so Done = merged, not deployed). PCOMP-74/-80/-81 are half-done (radius half deployed); keep open.
- **NexusAI (8):** RD-774, RD-836 (In Progress; PR #97 landed 2026-10-20, gate 29, then HISTORY PR #102); RD-782, -783, -784, -785, -788, -789 (To Do; PR #98 body: 62 of 68 test-code alerts fixed, #116 and the five of RD-786 carried by RD-873. RD-786 and RD-787 stay open). For RD the next move is Testing, not Done. RD-478 is partial (slice #95 only).
  - Also 172 RD tickets sit in `Testing` and 199 in `Release Ready` (query above); moving Testing to Release Ready is a human verification step, not a record-seat call.

## B. Blocked, one line each

MPS (reason in brackets):
- 295 [words, deferred to the Paul review; product owner said leave as is at 09:24 today (`2026-10-24_mps-words-for-paul-review.md:7,21`)]; 153 [words first]; 261 [words + Opus + calc-register V4]; 161 [new words]; 170 server half [refusal wording].
- 300, 314, 163, 315 [coordinator's own call (Tuesday), not yet ruled; 315 also follows 256].
- 187 [needs a hosted deploy card]; 136 [owner's Entra group step + deploy]; 144 [waits for 202/203 live on the hosted site, C-35]; 222, 226, 202 [rollback design + ruling, Opus]; 224 [hosted runtime]; 203 [deploy-script follow-ups].
- 212 [folds into governed settings T-V11, waits for 286/287]; 260 [lender data]; 284, 285 [PR #84 / data not settled]; 128, 129, 157, 112, 113, 109, 95, 177, 188, 159 [carry `needs-ruling`].
- T-V4..V13 plan tickets, 39 open with lane labels v4 and above (query: labels `lane-v4` to `lane-v13`): ruled to build as planned (C-45, 20 Oct) but each lane brings a word pack and most touch the calculation register or contract; not screened for file overlap, UNMEASURED individually.
- UNSCREENED: about 43 older gate-residue tickets numbered 90 to 134 (for example 90-94, 96-103, 106-108, 110, 114-127, 130-135) and the spec rows 1-87: I did not read them; many may already be covered by merged PRs. A screening seat should classify them before the next planning round.
- 18 `question-for-kam` tickets (MPSCALC-68 to -88 range): product-owner questions.

HPSM-POC:
- Awaiting HP or the product owner: -5, -6, -21, -82 to -86, -97, -166, -181, -241 (HP inputs), -90/-91/-94 (`needs-kam`, `needs-sme-content`), -162 to -168 (`needs-kam`/`needs-hp-content`), -237 (money decision), -242 (the showcase feedback has not been written down), -257 (decision), -324 (decision), -180 and -203 (a call for the owner, C-29), -268 (hosted runtime: deploy), -309, -234, -235, -126, -193, -196, -246 N-4, -303 (all need a hosted measurement or deploy), -304 (resource cleanup needs `az`, out of bounds), -220, -191, -240 (HP Security Manager integration, needs the HP device), -170 to -176 (SOW deliverable drafts "FOR KAM"), -224 (telemetry: gate NO GO, stopped by the owner's rule), -310 words 5a, -117 (design), -100 (retention policy).
- -334, -335, -336: in flight (#207 in CI).

Composer:
- 31-39 (L1, L2) [hold K6 and #85 draft; L2-3 words card]; 45-51 [need L1/L2/L3]; 52-61 [need words or K8/L7]; 19, 20, 68-72, 76, 79, 84-89, 91, 92 [`held`]; 46 [`needs-kam`: "warn, never block" not ruled]; 94 [`needs-kam`]; 78 [ops: signing key]; 83, 90 [not ruled / half open]; 9, 16, 21, 25-28, 13 [ops or design calls the coordinator makes]; 29 [L0-1 records].

NexusAI:
- Of 369 To Do tickets I screened 100 (every To Do row with key >= 780 or priority High/Highest, listed from the open-set query); the other 269 (older, mostly Medium/Low `operations`) were NOT screened.
- RD-13, -20, -21, -28 (Partner Center, SOC2, pentest: external); RD-18, -93, -104, -368 (`needs-decision`); RD-536 (list for the product owner); RD-858 (`kam-decision`); RD-842 (feedback #10, user-facing data); RD-664, -662, -450, -643 (Marketplace, tenants, money); RD-869/-872 (`user-facing` wording); RD-50, -41, -49, -81 (infra, deploy).

## C. Partition summary (what can run in parallel)

- Across projects: all disjoint (separate repos).
- MPS: M1 serial; M2 parallel with M1 (324 last); M3 parallel; M4 parallel; Opus 288 after M1, Opus 302 parallel. Recommended first 4 seats: M1, M2, M3 + M4 combined.
- HPSM-POC: P1, P2, P3, P4 (after #207), P5 parallel.
- Composer: C-L3 serial; C-T, C-P parallel; C-D serial behind C-L3 on migration numbers.
- NexusAI: N1, N2, N3 parallel on code paths, but N1 and N2 both regenerate `scripts/verify-expected-counts.json` if they add suites, so land them one after the other (NexusAI lands fast-forward only).

## FOUND

1. The morning "blocked by #102" status of MPS 161/169/170/288/204 is stale: #102 merged 24 Oct 01:15Z and main is `05c598f3`; of the five, 204 and 169 are now buildable word-free; 288 is Opus; 161 and 170-server need words.
2. MPSCALC-322 to -327 and -321 were filed today by gates of #102/#103 and are the freshest completable work, one rated Major (322).
3. All three morning lanes (L1 #105, L2 #106, L3 #104) are merged, so the "ready lanes" file is fully consumed; its tickets are all open in Jira (74/74 non-Done).
4. HPSM-POC has no open product work that is word-free except the test-teeth tickets; the SOW drafts and HP items are all human-gated.
5. Composer's L3 structure lane is the only big word-free build; L1/L2 are on hold.

## NOT TESTED / UNMEASURED

- I did not read code for HPSM-POC, Composer or NexusAI (only tickets, seat comments and PR text); sizes for those are estimates from the tickets. MPS candidates were checked against the main tarball for 316, 313, 317, 218, 221, 205, 201, 161, 176, 204 (grep, with the caveat that several greps ran case-sensitive; the matches I report were positive hits, and the zero hits for 161 `archive` and 176 `triage` were re-run with `-i`).
- PR lists: MPS and HPSM-POC fully paged (106 and 207 rows); NexusAI only the newest 100 PRs (page cap), so older merges were not mapped.
- Whether HPSM-POC main, Composer main and NexusAI main carry the fixes the seat comments describe (I trusted the seats' merge shas, which agree with the PR list).
- The caller-supplied rulings of 24 Oct (316, 204, 261, 153, 176) are not in the record yet; confirm they are written into `CLARIFICATIONS.md` before a brief cites them.
- Whether the 38 title-only MPS "done" candidates are complete (partial merges possible).
- Not touched on purpose: myPKI, CypherKey, Lead_Bot, any hosted or production host, `az`, the decision queue, the scoreboard, `briefs_staged/`.
