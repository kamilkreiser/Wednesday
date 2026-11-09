# Spec check: B_demo_walkthrough_spec.md against the demo file and HPSM-POC main

Drafted 2026-11-09 21:36 to about 21:55 AEDT (`date` at the first read: Mon 9 Nov 2026 21:36:23 AEDT). Read-only throughout.
Marks: MEASURED = printed by a named instrument this run; UNMEASURED = nobody has.
Main = detached worktree `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1381/main`, HEAD printed by `git log -1` = `2075486` (the sha the spec and the builder brief name). Paths below are relative to that worktree; `W` = `web/src`.

## BLUF
- **Spec against the demo file: 0 mismatches.** 14 of 14 steps, same order, and every table column (time, title, view, key, purpose, say, caveat) plus all 14 cues are string-equal to the demo's `beats` array (python3 -I -B, `json.loads` of the array at DEMO:563-577 vs the spec's table rows; 0 differing cells of 14 x 8; control: the cell compare printed MISMATCH on none, and a never-present string "Xtitle" counted 0 in the spec).
- **Spec against main: 3 mismatches in the build instructions (B.1 to B.3) plus 1 talk-track claim not supported as worded (D, "each finding"), and 1 claim UNMEASURED (services-page pricing label).** Routes: 13 of 13 page targets exist; the sign-in/UAT security claims all hold.
- **Most dangerous: the spec's sample-customer lookup cannot work as written.** It selects `synthetic && stage === "report"` (spec section 3.3, `useReportSample.ts`), but the customer list item has no `stage` field (`web/src/api/schema.gen.ts:1370-1390`; the field that exists is `latestAssessmentStatus`, value `"report-issued"`, `:1375`). Built literally, steps 6-10 are disabled on every host. On the laptop (mock) mode there is also no "Kookaburra Council (sample)" at all. A builder who trusts the spec ships a walkthrough whose five middle steps do nothing.
- Security claims (section 4 of the spec): no mismatch found. Details and lines in part C.

## A. The demo file (python3 -I -B, regex then `json.loads`)
Instrument: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1109/f-1c6fabb2c95c_HP_Security_Services_Playbook_v2_0_Aligned_Partner_Demo.html`, the `const beats=[...]` array.

| Fact | Measured | Control |
|---|---|---|
| Number of steps | 14 (MEASURED) | the parse printed 14 and the spec table has 14 rows (regex `^\| \d+ \| \d+:\d\d` printed `rows 14`) |
| Order (title, view) | 1 Open with the opportunity/cover, 2 Reveal the Playbook/dashboard, 3 Assess -> Implement -> Optimize/dashboard, 4 Customers/customers, 5 Engagements/engagements, 6 Assessment/assessment, 7 Reveal an explainable security gap/score, 8 From finding to HP-backed action/hpsm, 9 Narrative/narrative, 10 Executive report/report, 11 Action plan/action, 12 Service offers/offers, 13 Revenue/revenue, 14 Close/dashboard (MEASURED) | identical to spec rows, 0 cell differences |
| Presenter notes (`caveat`) | present on steps 7, 8, 9, 10, 12, 13 only (6 of 14) (MEASURED: key list per step). The spec's table shows a caveat on exactly those six | key lists printed |
| `<a ... href>` anchors in the file | 0 (MEASURED) | the same regex on the string `<a class=x href="y">` counts 1, so it can fire |
| `https://` URLs | 1: the HP logo image on wikimedia (`DEMO:264`) (MEASURED) | printed set has one member |
| Step "link target" | none is a URL. Each jump is `<button data-demo="jump" data-index>` (`DEMO:596`), i.e. an in-demo screen switch (MEASURED by reading the printed line 596). The "link target" of a step is its `view` | |
| Sidebar entries | 13 partner (3+3+3+4) and 8 customer (4+4) in `MENU_SPEC` (`DEMO:456`) (MEASURED, counted from the printed line); Partner allow-list has 10 (`DEMO:457`) | |

Spec lines DEMO:289 (9 journey steps), DEMO:456-457, DEMO:582, DEMO:596 and DEMO:645 print what the spec says they hold (MEASURED, sed). Other DEMO line cites (DEMO:219, 223, 264, 307, 317, 328, 384, 387, 599-643) were not re-read: UNMEASURED.

## B. Step by step: does the app route the spec maps to exist at main?
Instrument: `find web/src/app -name page.tsx` (listing printed; 58 pages), `ls web/src/app/api/auth`, `grep -n`. A route is EXISTS if its page.tsx is present and the page does not redirect (`redirect|notFound|permanent` grep over the six top-level pages printed nothing; control: the same grep over `proxy.ts` hits its redirects).

| # | Demo view | Spec route | Page file at main | Result |
|---|---|---|---|---|
| 1 | cover | none | none | as spec: no route; MEASURED that no cover page exists |
| 2 | dashboard | `/home` | `app/(app)/home/page.tsx` | EXISTS |
| 3 | dashboard | `/home` | same | EXISTS |
| 4 | customers | `/workspace` | `app/(app)/workspace/page.tsx` | EXISTS; sidebar entry `GlobalNav.tsx:46` |
| 5 | engagements | `/engagements` | `app/(app)/engagements/page.tsx` | EXISTS; `GlobalNav.tsx:47` |
| 6 | assessment | `/customers/{K}/assessment` | `app/(app)/customers/[customerId]/assessment/page.tsx` | EXISTS, but see mismatch 3 |
| 7 | score | `/customers/{K}/results` | `.../results/page.tsx` | EXISTS |
| 8 | hpsm | `/customers/{K}/recommendation` | `.../recommendation/page.tsx` | EXISTS |
| 9 | narrative | `/customers/{K}/narrative` | `.../narrative/page.tsx` | EXISTS |
| 10 | report | `/customers/{K}/report` | `.../report/page.tsx` | EXISTS |
| 11 | action | `/action-plan` | `app/(app)/action-plan/page.tsx` | EXISTS; Partner allowed `GlobalNav.tsx:33,48` |
| 12 | offers | `/services` | `app/(app)/services/page.tsx` | EXISTS; `GlobalNav.tsx:50` |
| 13 | revenue | `/revenue` | `app/(app)/revenue/page.tsx` | EXISTS; `GlobalNav.tsx:51` |
| 14 | dashboard | `/home` | same as 2 | EXISTS |

First path segments of all routes (`home`, `workspace`, `engagements`, `customers`, `action-plan`, `services`, `revenue`) are all in `RETURN_SEGMENTS` (`W/server/auth/returnPath.ts:7-10`) (MEASURED). The auth-gate proxy returns 404 for an unknown customer id (`W/proxy.ts:16-26`, `:115`); `customerForRoute` accepts a prototype id or `^CUST-[0-9A-Za-z-]{3,64}$` (`W/lib/customers.ts:71`, `:83-88`), so a real API id passes (MEASURED).

### Mismatches against main
1. **[MOST DANGEROUS] `stage` does not exist on the list item.** Spec 3.3 picks `synthetic && stage === "report"`. `CustomerSummary` (`schema.gen.ts:1370-1390`) has `id, name, synthetic, latestAssessmentStatus, overallScore, band, priorityRisks, nextService*, lastActivityAt`; no `stage` (control: the same block holds `latestAssessmentStatus`). Use `latestAssessmentStatus === "report-issued"`.
2. **Laptop (mock) mode has no Kookaburra sample, and its prototype customer follows a different code path.** Prototype customers are Quollridge (`W/lib/customers.ts:29-35`, `hasAssessment: true`; `DEMO_CUSTOMER_ID = "quollridge"` `:67`), Sample customer B and C (`:43-60`, `hasAssessment: false`). The mock API knows `CUST-SYN-QUOLLRIDGE`, `-SAMPLE-B`, `-SAMPLE-C`, `-PARTNER-SELF` (grep over `W/server/mock`); "Kookaburra Council (sample)" is in `api/src/HpsmPoc.Modules.Assessment/Showcase/ShowcaseSeeder.cs:120` (the real API seeder, stage Report) and in `W/components/customer/content.ts:67` (a content map), not in the mock list. So in mock mode the spec's `useReportSample` finds nothing and steps 6-10 would be disabled, which contradicts the spec's own e2e line "on a mock run ... check that step 10 shows the report page" (spec 3.5). Decide which customer the mock mode uses (Quollridge, `hasAssessment: true`, prototype screens) before building.
3. **Step 6 opens a different page for the API sample than the spec describes.** `AssessmentScreen.tsx:58-59`: when `customer.hasAssessment` is false (every API customer, `customers.ts:87`) it renders `ApiAssessments` ("start one, resume it, or see its result"), not the 16-question runner. Same split for steps 7, 9, 10: `ResultsScreen.tsx:25`, `NarrativeScreen.tsx:30` (`ServiceNarrative`), `ReportScreen.tsx:157` (`ServiceReportStep`). The spec says only "PARTIAL" for the audience filter. The pages also carry write buttons (`ReportScreen.tsx:200-220`, `ServiceReport.tsx:106-150` Generate; `NarrativeScreen.tsx:111-121` Draft) which are fine as long as the panel never clicks them. I found no write on mount in these five screens' source (grep over useEffect/POST/PUT: only the announcer effect `AssessmentScreen.tsx:50`) but did not run them: UNMEASURED at runtime.
Confirmation, not a mismatch: step 8's "Good / Better / Best" exists in the Recommendation screen** (`RecommendationScreen.tsx:27-29` `TIERS`), consistent with the spec; but the spec says the sidebar entry is gone by design: confirmed `GlobalNav.test.ts:78-79`. No mismatch; listed so the gate does not look for a sidebar entry.
(Count: 3 mismatches above; the claim-level item is in part D.)

Customer-workspace "framework alignment" is held: `W/components/shell/customer-nav.ts:23` `built: false, held: true`, and no `security/[customerId]/frameworks/page.tsx` exists (page list printed) (MEASURED, as the spec says).

## C. Security claims, at main
| Spec claim | Result | Evidence |
|---|---|---|
| A Partner sign-in path already exists for UAT | TRUE (MEASURED) | `W/components/screens/UatStartScreen.tsx:21-26` four levels, partner first; `:41-51` each is `<form method="post" action="/api/auth/uat">` with hidden `level` (+ optional `next`) |
| What gates it | Env flag plus label plus key (MEASURED) | `W/server/auth/config.ts:73-85`: `HPSM_UAT_OPEN_SIGNIN` must be exactly `on` (`:74-75`), `HPSM_ENVIRONMENT === "uat"` (`:76`), on App Service a site name containing `-uat-` (`:77`), no dev-header (`:78`), `HPSM_UAT_OPEN_KEY` of 32 bytes or more (`:79-81`), `AUTH_SECRET` 32 or more (`:82-84`). Any failure returns `off` (fail closed). API side: same two locks or the host refuses to start (`api/src/HpsmPoc.Api/Auth/UatOpenAuthentication.cs:119-124` and the Refuse calls; partner = seed owner `:129`) |
| The route is POST-only, same-origin, 404 outside UAT | TRUE (MEASURED) | `W/app/api/auth/uat/route.ts:6` exports only `POST`; `chooseUatLevel` `W/server/auth/uatOpen.ts:104-122` (405 non-POST `:105`, `sameOrigin` `:106`, form-encoded only `:109`, exactly one valid `level` `:115`); `routes.ts:22,38` and `:17` return 404 in mock and for non-UAT |
| Entra being active hides/disables it | TRUE, with one precision (MEASURED) | `resolveAuth` decides UAT BEFORE Entra (`config.ts:71-86`, Entra from `:87`). The two are one `kind` each (`config.ts:42`), so `/` renders `UatStartScreen` only when `authUi() === "uat"` (`W/app/page.tsx:23`) and the Entra screen otherwise (`:24-26`; `SignInScreen.tsx:41`). With Entra active, `/api/auth/uat` answers 404 (`routes.ts:23` falls to `handler ? ... : 404`, handler null for `uatChooseRoute` `:38`). **Precision:** a server with the UAT switch on AND complete Entra settings runs UAT, not Entra (`:74-85` returns first). "Entra is configured" is therefore not the test; the test is `authUi()`. |
| The set of auth routes | 5 under `app/api/auth` (MEASURED, `find ... route.ts`): `callback/microsoft-entra-id` (GET), `session` (GET), `signin` (GET), `signout` (POST), `uat` (POST). Others under `app/api`: `health`, `v1/[...path]`. The spec's list matches. Note `signin` is an existing GET (`signin/route.ts:6`), which begins Entra and mints no session in itself | |
| Mock mode picker exists | TRUE (MEASURED) | `SignInScreen.tsx:44-80`, sign-in dispatch `:63-64`; `resolveAuth` returns mock only when not hosted (`config.ts:87`) |
| `?next=` cannot carry a query | TRUE (MEASURED) | `returnPath.ts:19-23` (`CHARS` has no `?`) |
| Reset never on UAT | TRUE (MEASURED) | `W/components/shell/AppShell.tsx:135` |
| Partner object scope, shared identity | `UatOpenAuthentication.cs:129` partner = seed owner (MEASURED); `Caller.cs:28` metrics not for Partner (MEASURED); the scope-by-owner lines `Caller.cs:207-236` not re-read: UNMEASURED |

## D. Talk-track claims
| Claim (demo step) | Verdict | Evidence |
|---|---|---|
| "The customer name is not sent to the AI" (step 9) | **SUPPORTED** for the narrative input (MEASURED); the provider call path itself UNMEASURED | `api/src/HpsmPoc.Modules.Reporting/Narrative/NarrativeInput.cs:23-26`: the input type has no customer-name property; `Organisation` is "always the literal 'the organisation'"; `NarrativeInputProjector.cs:35` sets `Organisation: NarrativeInput.OrganisationPlaceholder`. I did not trace `AzureOpenAiNarrativeProvider.cs` to confirm that nothing else is added to the request, and a guard test `NarrativeGuardTests` named in `NarrativeInput.cs:24` was not run. The demo's own caveat (step 9) says the prototype does not send data to AI; the app does have an Azure OpenAI provider |
| "Each finding maps to a named HP Security Manager policy setting" (step 8) | **NOT SUPPORTED as worded** (MEASURED) | `api/src/HpsmPoc.Api/SeedContent/snapshot-policy-aligned.0.1.2.ruleset.json`: 54 recommendations carry `hpsmPath` + `recommendedSetting` (first at `:2226`, `:2231`), but of 16 findings (objects with a `recommendationRefs` key) only 13 have a non-empty list (python3 -I -B count, control 0 for a never-present key), so 3 of 16 findings name no setting. Remediation text for findings reads "The detailed action wording is being finalised." (`:1669`). Safe wording: "recommendations name an HP Security Manager setting where one is mapped" |
| Pricing on steps 12-13 | **SUPPORTED as illustrative, not as approved** (MEASURED) | `web/src/components/partner/RevenueCalculator.tsx:3` ("ILLUSTRATIVE content"); `web/src/content/partner/partner-showcase.v0.1.0.json:4` `"label": "ILLUSTRATIVE"`. An "unapproved sample" label on `ServicesHub.tsx`: grep found none: **UNMEASURED** for the services page |
| "A person reviews and approves the narrative before it enters the report" (step 9) | consistent with the review flow (`ApiNarrative.tsx` calls `reviewNarrative`; `NarrativeScreen.tsx:125` approved state) - MEASURED by grep only, not run | |

## E. Not verified
- Runtime behaviour of any page (no server was started; nothing was run).
- Whether `/customers/{K}/results` shows current-versus-target bars (spec said unverified; still unverified).
- DEMO line cites other than those listed in part A.
- The Entra branch of `SignInScreen.tsx:103-146` beyond its signature.
- Whether `HostedDemo:Seed:OwnerObjectId` is configured on the real UAT host (config of a hosted host; not touched).
- Port conflict (see the gate kit): block 9640-9649 is already named in the kits of B1377 and B1380 (`grep -n -w` printed lines in both), so the gate should not use it unless Tuesday confirms.
