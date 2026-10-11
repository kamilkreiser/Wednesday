# HPSM-POC: open HPSMPOC tickets sorted into buckets (screen, 2026-10-11)

DRAFT FOR FRIDAY. Read-only screen. Nothing was written to Jira, git or Azure.

## BLUF

**106 open non-epic tickets plus 9 epics. That matches Friday's 16:2x count.** Instrument: POST `/rest/api/3/search/jql`, JQL `project=HPSMPOC AND statusCategory != Done`, followed through `nextPageToken`. The result was 105 Task, 1 Sub-task and 9 Epic. Comments came from `/issue/{key}/comment`.

| Bucket | Count |
|---|---|
| **A**: agents can do it now | **24** |
| **K**: needs Kam | **44** |
| **H**: needs HP or another human | **19** |
| **X**: already done in code, or stale | **14** |
| **P**: parked by a ruling | **5** |
| Total | 106 |

**Code main read:** `76acd696a1c9` (#136, B203). I read it at the start of the screen and again just before writing. PR #137 (B202) was still **open, not merged** at the second read.

**Rulings read:** `1_Project_Definition/CLARIFICATIONS.md` on analysis `main` `47565b88` (C-01…C-83). The local working copy is stale (it ends at C-30), so I did not use it.

**Most of A is small hardening work. Little of it is visible to HP.** For Tuesday, the useful items are:
- the "what's new" page for the session (HPSMPOC-164);
- the hosted measurements owed before HP is invited (HPSMPOC-126, -196);
- hosted telemetry (HPSMPOC-224);
- one presenter-visible message (HPSMPOC-159).

Friday ruled on HPSMPOC-232 (comment of 11 Oct, 01:40) that only fixes change before HP's review on 13 Oct. The lanes below respect that, and the perf changes are marked "after 13 Oct".

## Bucket A: agents can do it now (24)

| Key | Summary | Reason and evidence |
|---|---|---|
| HPSMPOC-29 | [WS3-6] M3 happy-path demo in UAT | Follows -57 in the same lane once UAT exists. The happy path (sign-in, profile, assessment) is built (web/src/server/auth/entra.ts). |
| HPSMPOC-57 | [WS8-1] Dev, UAT and Demo environments via IaC | Demo is up. UAT is RULED (C-52, CLAR:555): "a Lane A seat runs its Entra steps and deploy under Kam's login" from `infra/env/uat.bicepparam`. The spend is approved (~A$49 a month). **Tier 1.** |
| HPSMPOC-126 | Deploy-time measurements owed (sign-out lock, zip, real-Entra, RCSI, start limit) | No result is recorded on the ticket since its one comment (1 Oct), although the demo has been deployed many times (C-55…C-83). The checklist gives each check. Read-only on hosted. **Tier 1** (real-Entra tamper matrix). |
| HPSMPOC-134 | [B79] Test of each operation's declared statuses against the code | The open half is the test. No such test exists at main (grep "declared status" finds only contract files). |
| HPSMPOC-148 | [B87] Mock parity: C-2 two-session curio, mock 429 has no detail | The surrogate and 429 halves merged in #105. C-3's "At most 1 follow-ups" is not found at main. Open: C-2 and B138 N-3 (the mock `problem()` writes no detail). |
| HPSMPOC-149 | [B87] Content060ApiTests still asserts the pinned literal | `Content060ApiTests.cs:119` `Assert.Equal("snapshot-policy-aligned@0.1.2", …)`. The fix shape (assert the constant instead) is in the ticket. |
| HPSMPOC-152 | [B84] Repo guard against raw hidden or text-direction characters | The escapes merged in #104. The guard is not built: no hit in `.github/` or `infra/tests/`. The B137 N-3 file list is in comment 2. **Tier 1** (Trojan Source class). |
| HPSMPOC-154 | Decision: laptop showcase start-up seed under the seed lock? | The ticket says "Friday or Kam decides". Option (a), leave it, closes the ticket. Option (b) is a small change to the api `ShowcaseStartup.cs`. Needs Friday's ruling first. |
| HPSMPOC-155 | CI has no SQL Server, so seed-lock and reset proofs run locally only | The fix shape is stated: a pinned SQL Server container in ci.yml with a by-name check, following the Azurite pattern. |
| HPSMPOC-159 | Presenter never sees the reset's "nothing changed, try again" | Still present at main: `web/src/api/client.ts:218` `throw new ApiError(r.status, null)`. The fix and the test are stated. |
| HPSMPOC-164 | [C-34] HP review sessions: a build HP can open, plus a "what's new" page | The hosted build and the feedback route are live (C-71, C-75). What is left is the per-session one-page "what changed" for Tue 13 Oct. It is a draft that Kam forwards. |
| HPSMPOC-196 | [B118 N-4] Measure the front end's X-Forwarded-For shape on hosted | Never measured (the ticket has 0 comments). The probe is stated. **Tier 1** (proxy trust). |
| HPSMPOC-220 | [B161] SM import: device list plus observed evidence | Phase A is built (C-73; `Ingest/ImportEvidence.cs`; `useSnapshot.ts:70` "observed"). There is no `PrinterCount` fill in `Ingest/`. Check the rest of the ticket's scope against C-73 Phase A. **Tier 1** (customer data). |
| HPSMPOC-224 | [B170] Hosted demo has no telemetry or app logs | No OpenTelemetry, AzureMonitor or ApplicationInsights reference in api/src, web/src or web/package.json at main. The fix shape includes scrubbing personal data. **Tier 1** (PII). |
| HPSMPOC-225 | [B172] Regex shape checks anchor with `$` (accepts "id\n") | 22 `GeneratedRegex(…$")` at main and 7 with `\z`. The fix shape is `\z` plus one table test. **Tier 1** (input validation). |
| HPSMPOC-226 | [B174] Feedback attachments follow-ups | N-4, N-5 and N-7 merged in #129 (3a9288a). Open for code: N-6 and N-8 (BFF), the `ContractTests.cs:50` "contract 0.12.0" word, and B177 N-1/N-2. N-3 and N-9 need Kam's word. **Tier 1** (upload limits). |
| HPSMPOC-227 | [B175] 6 opt-in live-API e2e tests fail; CI never runs them | Each spec's fault is named. Fix each spec, then add an on-demand CI job. |
| HPSMPOC-228 | [B176] Site timing follow-ups | Still present at main: `bff.ts:149` lists the dead readiness-report write regex (N-2), and `auth/cookies.ts:5` still says "10 minutes" (N-8). N-3, N-4, N-6 and N-9 have stated shapes. N-7's words go to Kam. **Tier 1** (bff/auth). |
| HPSMPOC-229 | [B172 R3] Imports: firmware rule and phase-2 errors, before switch-on | `ImportReader.cs` has no ASCII-letter rule. `ImportEndpoints.cs:189` says a failure "leaves the run pending". **Tier 1** (data integrity). |
| HPSMPOC-235 | [B182] BFF to API keep-alive | `bff.ts` names no dispatcher. Server-Timing is live (#130). This is a perf change, so after 13 Oct. |
| HPSMPOC-244 | [B196] F-22 cannot catch the focus regression (its partner has no plan) | Tests only. The mutant proof is given. The spec is still on its own mock space without a plan (`playbook-b17-clicks.spec.ts:60–87`). |
| HPSMPOC-245 | [B189 gate notes] N-1, N-2, N-4, N-5, N-6 | "Friday rules each open item". Shapes are given per item. |
| HPSMPOC-246 | [B193 gate notes] N-2, N-4, N-5, N-6, N-7 | "Friday rules each open item". Shapes are given per item. |
| HPSMPOC-247 | [B203] ImportRobustnessTests R2_2 times out in a parallel suite | Options (a) and (b) are stated, with (b) recommended. No `[Collection]` or timeout is set at main. |

## Bucket K: needs Kam (44)

| Key | Summary | Reason and evidence |
|---|---|---|
| HPSMPOC-5 | [CG-4] Event window and audience | The date is ruled (C-03, C-36 A). The window is open: attending Amplify is Kam's later decision (C-34 §C). |
| HPSMPOC-6 | [CG-5] Name the Security SME and a deputy PO | Comment of 27 Sep: neither is named. |
| HPSMPOC-11 | [WS1-1] Kick-off and SME cadence record | Comment of 3 Oct: "Kam names which session counts as the kick-off and states the SME cadence". |
| HPSMPOC-12 | [WS1-2] Demo story and 7-minute script | v1 is in the demo pack, a DRAFT FOR KAM (records/b110). No PO review is recorded. |
| HPSMPOC-14 | [WS1-4] Versioned rules schema | Closes when Kam rules RS-03…RS-10 and the "DB metadata" question (comment of 27 Sep). |
| HPSMPOC-16 | [WS1-6] Stack decision record | Waits on Kam's sign-off once the list of deviations is added (comment of 27 Sep). |
| HPSMPOC-35 | [WS4-5] Remediation mapping into buckets | "No code is left". It needs approved remediation content from the SME (Kam, C-05). |
| HPSMPOC-44 | [WS5-6] Report language and disclaimers | The text is a placeholder (ReportModelBuilder.DisclaimerPlaceholder). Datasec's SME owes it. |
| HPSMPOC-46 | [WS6-1] Approved HP/HPSM policy examples | `hpsm-guidance.synthetic.json` is a placeholder. The SME (Kam) owes the examples. |
| HPSMPOC-47 | [WS6-2] Finding to HP/HPSM mapping config | "No code is left". Waits on -46. |
| HPSMPOC-48 | [WS6-3] Recommendation view and report section | Built. "Implementation-ready" waits on -46. |
| HPSMPOC-51 | [WS7-1] Manual baseline and metric definitions | Needs baseline hours with their source, plus approval of M1–M7 (comment of 27 Sep). |
| HPSMPOC-52 | [WS7-2] Instrument metrics including overrides | Kam confirms T_idle/T_last (QA-129). The override metric waits on override existing. |
| HPSMPOC-55 | [WS7-5] Trial runs and metrics output | Needs SME trial runs plus -51. |
| HPSMPOC-58 | [WS8-2] CI/CD deploy job | Half 2 (a deploy job with a federated credential) "needs an Entra credential, so it is Kam's" (comment of 5 Oct). |
| HPSMPOC-60 | [WS8-4] Playwright event journey in UAT and Demo | Needs the final script (-12/-172, Kam's review) and UAT. |
| HPSMPOC-61 | [WS8-5] UAT execution and defect triage | Kam is the UAT owner. The M6 test script is a DRAFT FOR KAM (records/b114). |
| HPSMPOC-62 | [WS8-6] Freeze, fallback, rehearsal | Needs the presenter, the script and the rehearsal (Kam). |
| HPSMPOC-63 | [WS8-7] Event on-call, handover, Phase 2 backlog | The drafts await Kam (records/b110). The event-day roster is Kam's. |
| HPSMPOC-64 | [WS8-8] 30-day hypercare | The window must end by 31 Dec or the SOW must change: "Needs Kam and HP". |
| HPSMPOC-99 | Feedback B52 notes N-4 and N-9 | "N-4 is Kam's (his Automation rule)". N-9 waits on a scale-out. N-7 and N-8 merged in #109. |
| HPSMPOC-100 | Follow-up contact retention and erase (K10) | "K10 is Kam's ruling, not yet made". **Tier 1 when built** (data deletion). |
| HPSMPOC-109 | Route A: "sent" is not proof of delivery (O-1) | O-2 merged in #105. O-1 "a card for Kam if it needs a credential or a rule change". |
| HPSMPOC-162 | [C-34] AI at the printer: phase-one position | A DRAFT for Kam's review before any HP review (needs-kam). |
| HPSMPOC-163 | [C-34] Traffic-light meaning | A DRAFT for Kam, then HP vetting with the weights. |
| HPSMPOC-165 | [C-34] Good/better/best consulting offer content | Waits for Kam, Paul and Peter to settle a first package. |
| HPSMPOC-168 | [C-34] Industry choices and a fleet-size note | Industry has shipped, display only (#135, 3fa5c1b). The fleet-size note is still a proposal for Kam. |
| HPSMPOC-169 | [SOW] Re-base the stage-gate pack and CR log | Re-based as a DRAFT for Kam (records/b95, b109). |
| HPSMPOC-170 | [SOW] Deployment and administration guide | Admin guide v0 is a DRAFT FOR KAM (records/b110). The deploy half's defects are agent work once Kam accepts it. |
| HPSMPOC-171 | [SOW] Testing evidence and known limitations | v0 is a DRAFT FOR KAM (records/b110). |
| HPSMPOC-172 | [SOW] Demo pack | v0 is a DRAFT FOR KAM. Kam gives the presenter role and account and the support roster. |
| HPSMPOC-173 | [SOW] Phase 2 backlog document | v0 is a DRAFT FOR KAM (records/b110). |
| HPSMPOC-174 | [SOW] Weekly status report to HP | Every hours cell is "[KAM: hours]" (K-10). |
| HPSMPOC-175 | [SOW] AI tools record: two CONFIRM placeholders | Marked "Kam to confirm" (tenant, no-training). |
| HPSMPOC-176 | [SOW] Privacy documents (Datasec is controller) | RoPA and notice are a DRAFT FOR KAM (records/b109). |
| HPSMPOC-177 | Feedback comment: refuse the C-36 C invisible characters? | Title: "Needs Kam's word". No C-entry cites it. **Tier 1** (input validation). |
| HPSMPOC-178 | Customer name accepts hidden and text-direction characters | Title: "Needs Kam's word". No C-entry cites it. **Tier 1.** |
| HPSMPOC-187 | Template summary repeats one action per finding (second half) | The first half merged in #95 (C-48). The second half "is not ruled by Kam's card". The new template text needs his approval. |
| HPSMPOC-193 | [B118 N-1] Shared outbound addresses believed as proxy (LIVE) | "Narrowing is Kam's trade-off" (comment of 5 Oct, C-59). **Tier 1** (auth/proxy trust). |
| HPSMPOC-203 | Old report downloads under the new name's file name | "Kam decides (a) or (b)". C-53 leaves the file name of an issued report open. |
| HPSMPOC-204 | [FOR KAM] PDF profile caption wording | The label is for-kam. "NOT changed until he rules". |
| HPSMPOC-218 | Dependabot braces: the C-44 exception lapses 31 Oct | "A decision for Kam before 31 Oct" (renew, alias or drop). **Tier 1** (security). |
| HPSMPOC-237 | DECISION FOR KAM (money): a larger or second App Service plan | The label is needs-kam. It costs money. |
| HPSMPOC-240 | [C-69] Re-test FSS once a supported device is reachable | Needs a reachable supported HP device. Kam's "I have a printer on our network" is the open option. |

## Bucket H: needs HP or another human (19)

| Key | Summary | Reason and evidence |
|---|---|---|
| HPSMPOC-3 | [CG-2] Executed SOW (Purchase Order) | Signed on 28 and 29 Sep. "Fully executed only once the Purchase Order is approved" (HP). |
| HPSMPOC-21 | [WS2-3] Branding source | C-49 (CLAR:534): HP branding, "the PDF waits for" HP's assets. |
| HPSMPOC-31 | [WS4-1] SME content into the rules schema | The questions and weights are DRAFT. HP vets both (C-32 #6). |
| HPSMPOC-37 | [WS4-7] Golden scenarios reconcile | Kam approved the set (C-46). "HP has not yet approved the scores (H-2)". |
| HPSMPOC-82 | [HP-4] Security Manager live system and integration overview | The software arrived (Terry, 2 Oct). A live system and the API reference are still awaited. Label awaiting-hp. |
| HPSMPOC-83 | [HP-5] Quick Assess overview | awaiting-hp. HPSMPOC-181 says Quick Assess is out (2 Oct). |
| HPSMPOC-84 | [HP-6] Control Hub | Now an access request owned by Steve (comment of 1 Oct). |
| HPSMPOC-85 | [HP-7] Firmware vulnerability tool | awaiting-hp, 0 comments. |
| HPSMPOC-86 | [HP-8] Fleet Assessment tool | awaiting-hp (FTA release planned for December). |
| HPSMPOC-87 | [C-30] Customer questions aligned to policy principles | The wording and weights are DRAFT. HP vets (C-32 #6). |
| HPSMPOC-94 | [C-31] Guided expert remediation | Labelled needs-hp-content. Waits on the session with Jason O'Keefe's team. |
| HPSMPOC-97 | [Awaiting HP] Follow-ups from 29 Sep | The awaiting-hp checklist. |
| HPSMPOC-166 | [Awaiting HP] Follow-ups from 1 Oct | The awaiting-hp checklist. |
| HPSMPOC-167 | [C-34] Phase pages: align to HP's current deck | "Once HP sends its current generic deck". Label awaiting-hp. |
| HPSMPOC-180 | Rules schema `tier` without a version bump | Planned for "the next planned ruleset re-issue (the HP-vetted weights)". |
| HPSMPOC-181 | HP access and inputs, 4 workstreams | Labels awaiting-hp and hp-request. |
| HPSMPOC-191 | [C-45] SM 3.16 integration | The API adapter waits until "Terry answers Q2 and Q3". |
| HPSMPOC-241 | HP lab and integration questions | "Sent to Terry by Kam on 2026-10-08". Awaiting his answers. |
| HPSMPOC-242 | Paul's showcase feedback | Waits on Paul's detailed weekend notes (comment of 9 Oct). |

## Bucket X: already done in code, or stale (14)

| Key | Summary | Reason and evidence |
|---|---|---|
| HPSMPOC-13 | [WS1-3] Architecture pack: written PO approval | C-80 (analysis CLAR:864): "I approve M2 as Product Owner" (8 Oct). The pack is v0.3. |
| HPSMPOC-19 | [WS2-1] Figma flows | C-37 A (CLAR:383): the coded prototype is the UX, and no Figma will be made. |
| HPSMPOC-20 | [WS2-2] Prototype review and written PO approval | C-80 (CLAR:864). HP's own acceptance is tracked separately (SOW §4.2). |
| HPSMPOC-24 | [WS3-1] Entra sign-in with roles | The web Entra flow is at main (`web/package.json:21` oauth4webapi; `web/src/server/auth/entra.ts`). A real hosted sign-in was proven (C-70, CLAR:739). |
| HPSMPOC-88 | [C-30] Sections by audience | `audienceId` appears in content 0.5.0, 0.6.0 and 0.6.1 (`SeedContent/playbook-placeholder.0.6.1.content.json`). The five sections were shot live by B116. |
| HPSMPOC-90 | [C-30] Feedback button to Jira and email | Route A is live on hosted (C-75). The Admin list is at `web/src/app/(app)/admin/feedback/page.tsx`. Not measured: whether one hosted item was read back in Jira. |
| HPSMPOC-91 | [C-30] Client collateral packs 1–3 | Pack 2 is at main: `web/src/components/collateral/packs.ts:23,28` ("during"). The placeholders are labelled, as the acceptance asks. |
| HPSMPOC-95 | [C-31] Good/better/best tiers | C-32 ruled groupings only. `tier` is in rulesets 0.1.0–0.1.2, and `web/src/components/screens/RecommendationScreen.tiers.test.tsx` exists. |
| HPSMPOC-98 | Admin screen for the feedback list | `web/src/app/(app)/admin/feedback/page.tsx` ("Feedback received"). #129 (3a9288a) adds "HPSMPOC-98 attempts". |
| HPSMPOC-127 | R-009 AI refusal | Templates 1.0.2 merged as 04aae939 (#99, C-54). "Closing it is Friday's call". |
| HPSMPOC-207 | Hosted start-up seed wait and SQL login reset | The B195 retry narrowing is at main: `HostedDemoStartup.cs:179-186` (#133, a50b22d, live since C-83). Only the "watch each start" note is left. |
| HPSMPOC-238 | Flaky F-22 networkidle wait | Removed. `web/e2e/playbook-b17-clicks.spec.ts:73` waits on loaded content "not for `networkidle`" (#134, 03bd293). |
| HPSMPOC-239 | Vitest 5 s timeouts under load | `web/src/web-settings.test.ts:112` and `web/src/content/client-content.test.ts:32` `SCAN_TIMEOUT_MS = 120_000` (#134). |
| HPSMPOC-243 | [B183] Warm-up log notes, plus the B193 M-1 test gap | N-1 and N-2 are live (C-81, C-82). M-1 is pinned by `api/tests/HpsmPoc.Api.Tests/Assessment/HandledRaceLogTests.cs:98-108` (B195 item 4). |

## Bucket P: parked by a ruling (5)

| Key | Summary | Reason and evidence |
|---|---|---|
| HPSMPOC-92 | [Next phase] More sophisticated engagements | Kam's words in C-30: "next phase". Label next-phase. |
| HPSMPOC-96 | [Next phase] Voice or conversational assessment | C-31: Kam put it on the roadmap. Label next-phase. |
| HPSMPOC-117 | Audit LEDGER table absent on Azure SQL | Friday's reading (B60 ADDENDUM-7): "acceptable for the POC while ALL data is synthetic; decide before any real customer data". **Tier 1 when picked up.** |
| HPSMPOC-232 | Hosted first signed-in read ~2.4 s (caller write) | Friday's ruling (comment of 11 Oct, 01:40): "Nothing changes before HP's layout review on Tue 13 Oct". After that, a rolled-back write warm-up is the candidate. |
| HPSMPOC-234 | Web-side warm-up after a start | Friday's ruling (B196 ADDENDUM-1, comment of 11 Oct, 00:28): the connection part was DROPPED and the render part DEFERRED, because it needs PORT allowed by infra. |

## Epics (9, kept separate)

Each epic closes when its last child closes (the B29 comment on each). None has work of its own.

| Epic | Name | Open children in this screen |
|---|---|---|
| HPSMPOC-1 | Commercial & Governance | 3, 5, 6, 82–86, 97, 169, 174, 175, 176, 242 |
| HPSMPOC-10 | WS1 Discovery & Architecture | 11, 12, 13, 14, 16 |
| HPSMPOC-18 | WS2 UX/UI | 19, 20, 21 |
| HPSMPOC-23 | WS3 Core Platform | 24, 29, 88 |
| HPSMPOC-30 | WS4 Rules & Scoring | 31, 35, 37, 87 |
| HPSMPOC-38 | WS5 AI & Reporting | 44, 91 |
| HPSMPOC-45 | WS6 HP/HPSM Recommendation | 46, 47, 48, 94, 240, 241 |
| HPSMPOC-50 | WS7 Metrics & Commercial | 51, 52, 55, 92, 95 |
| HPSMPOC-56 | WS8 DevOps, QA & Event | 57, 58, 60–64, 90, 98, 99, 170–173, 232–239, 243–247 |

## Bucket A: proposed lanes

Each lane is file-disjoint from the others and sized for one builder session. They are ordered by value for HP's review on Tue 13 Oct. Lanes 1–2 write no code, so they collide with nothing.

1. **Lane R: review-day records (analysis repo only).**
   - Tickets: HPSMPOC-164 (the "what changed since the last session" page for 13 Oct, sent to Kam); triage sheets for Friday's rulings on -245, -246 and -154.
   - Touches: analysis `1_Project_Definition/Briefs/`, `Governance/`.
   - Not tier 1.
2. **Lane M: hosted measurements, read-only.**
   - Tickets: HPSMPOC-126 (items 1–5) and HPSMPOC-196 (X-Forwarded-For shape).
   - Touches: no code. Evidence goes in analysis `Briefs/`. Azure reads only, in `hpsm-poc-demo-rg`, under the project's `4_Credentials/.azure`.
   - **Tier 1** (real-Entra tamper matrix, proxy trust).
3. **Lane T: hosted telemetry.**
   - Ticket: HPSMPOC-224.
   - Touches: `api/src/HpsmPoc.Api/` (Program.cs, csproj), `web/instrumentation*` plus `web/package.json`, and `infra/modules/appservice.bicep` (read; the settings already exist).
   - **Tier 1** (personal data must be scrubbed).
   - It is a new capability. Friday decides whether it counts as a "fix" before 13 Oct.
4. **Lane W: web fixes the presenter and reviewers can see.**
   - Tickets: HPSMPOC-159; -228 web half (N-2 `bff.ts:149`, N-4, N-8 `auth/cookies.ts:5`, N-9); -226 BFF half (N-6, N-8); -148 (C-2, mock 429 detail); -244 and -227 (e2e).
   - Touches: `web/src/api/`, `web/src/server/` (bff.ts, auth/, mock/), `web/src/components/`, `web/e2e/`.
   - **Tier 1** because it touches bff and auth.
   - HPSMPOC-235 (keep-alive) joins this lane after 13 Oct.
5. **Lane V: API input and contract hardening.**
   - Tickets: HPSMPOC-225 (`\z` anchors); -134 (contract status test); -226 API half (`ContractTests.cs:50` word, B177 N-1); -149 (Content060ApiTests literal); -228 N-6 (warm-up log level).
   - Touches: `api/src/HpsmPoc.Modules.*/Endpoints/` and `Requests.cs` (excluding `Ingest/`), `api/src/HpsmPoc.Modules.Feedback/`, `api/tests/HpsmPoc.Api.Tests/` (Contract, Assessment).
   - **Tier 1.**
6. **Lane G: CI and repo guards.**
   - Tickets: HPSMPOC-152 (hidden-character guard, plus escapes in `GateRound2Tests.cs` and `FollowUpHardeningTests.cs`, which this lane owns); -155 (SQL Server in CI); -228 N-3 (R11 timer guard).
   - Touches: `.github/workflows/`, `infra/tests/`, `scripts/`, and those two test files.
   - **Tier 1.**
7. **Lane I: imports, before switch-on (imports are OFF on hosted).**
   - Tickets: HPSMPOC-229, -247, -220 (what is left of it).
   - Touches: `api/src/HpsmPoc.Modules.Assessment/Ingest/`, `api/tests/HpsmPoc.Api.Tests/Imports/`.
   - **Tier 1** (data integrity; the sweep of pending runs).
8. **Lane U: UAT environment (C-52), after 13 Oct.**
   - Tickets: HPSMPOC-57, then -29.
   - Touches: `infra/env/uat.bicepparam` and `infra/` (read), Entra objects under Kam's login.
   - **Tier 1** (Entra, environment). Spend is about A$49 a month, already approved.

## What I could not measure

- **Hosted state.** I made no Azure reads. HPSMPOC-126 and -196 are in bucket A because nothing is recorded on the tickets, not because I confirmed they were unmeasured on the site.
- **Rulings on unmerged analysis branches.** I read only analysis `main` `47565b8`. A ruling that sits only on an unmerged `records/*` branch or in a brief addendum would be missed. Friday's own rulings (on 232, 234 and 117) I took from Jira comments.
- **Ticket text.** Descriptions are long, so I read summaries, recommendations and the last comments. Some tickets with 4 or more comments were read only from their latest 2–3.
- **HPSMPOC-220.** Its full scope (device list entity, PrinterCount) is not checked against the C-73 Phase A text.
- **HPSMPOC-90.** I did not check whether one hosted feedback item was read back in Jira.
- **Builds and tests.** I built and ran no tests. Every check was `git grep` or `git show` at `76acd69`, with `--no-optional-locks`.
- **HP Restricted material.** Not opened.
