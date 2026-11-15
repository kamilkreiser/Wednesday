# Deploy round 2026-11-16: the rides-along census (Tuesday s281, drafter C8)

Drafted by a read-only Sonnet drafter, Mon 16 Nov 2026, 07:30-07:55 AEDT (every clock below is a `date` printed in the same shell call). Commission: `tuesday/briefs/2026-11-16_DEPLOY-ROUND_COMMISSION.md` (read whole). Rules: `tuesday/DRAFTER_RULES.md` (read whole). Scratch and raw outputs: `fleet/state/s281/deploy-census/`.

**Fences kept.** No deploy, dispatch, re-run, push, PR, merge, Jira/Linear write, mail, board post, Artifact, `az` write/login/restart, no `cd`, no token or secret printed. `gh` was `-X GET` only (each project's own `4_Credentials/.gh-config`). `az` was `account show` first, then read verbs only, each under the project's own `4_Credentials/.azure`. Marks: **MEASURED** = this drafter ran it today; **RELAYED** = read in another seat's file; **DERIVED** = arithmetic or source reading; **NOT MEASURED** = nobody ran it, with the reason.

**Two disclosed departures from the letter of DRAFTER_RULES section 4.** DRAFTER_RULES fence 4 says "no HTTP to any hosted host, no az". The commission (newer and specific to this census) permits `az` read verbs and `curl` GETs of public health/version endpoints, so I did exactly these and nothing else: (1) HPSM UAT: 3 GETs (web `/api/health`, API `/health`, web `/`); (2) NexusAI demo: 1 GET (`/api/health`); (3) MPS showcase: 1 GET (`/`); (4) Composer demo: 3 GETs (`/site.json`, `/healthz`, `/api/v1/healthz`). No request carried a cookie, token, body or feedback path. The Composer demo host was read from `COMPOSER_DEMO_URL` in the project `.env` (URL line only; user and password lines never read) and is not written anywhere. If Tuesday reads the rule as stricter than the commission, the GETs are in section "What I touched" at the end and can be discarded.

---

## BLUF table

| project | environment | deployed sha -> main sha | PRs riding | deploy-time steps | holds needing Kam |
|---|---|---|---|---|---|
| **HPSM-POC** | **No demo exists** (group `hpsm-poc-demo-rg` gone, MEASURED). Only hosted sites: **UAT** `hpsm-poc-uat-rg` (web `app-hpsmpoc-web-uat-25onzn`, API `app-hpsmpoc-api-uat-25onzn`), which is the site HP reviews | `576231b7` (UAT, deployed 11-12; web BUILD_ID matches live, API leg RELAYED) -> `678a1153` | **9** (#317-#325) | **YES, 4 kinds:** (1) one migration bundle (new append-only table `narrative_revision`), (2) then re-run `infra/sql/api-identity.sql` (new DENY), (3) hosted setting `HostedDemo__DraftRuleset` must move to `snapshot-policy-aligned@0.1.4` WITH the API (else the API refuses to start), (4) the forwarded-proof value on both apps (fail-closed without it). Never run the migration Down. Also: the last deploy's API leg failed once on a Kudu 504 | **YES: the whole HPSM leg.** UAT hold (EXPIRING-GRANTS.md:16) is not lifted by 'c' as I read it, and there is no demo to deploy to. See Q1 |
| **MPS Calculator** | Hosted **showcase** `app-mpscalc-showcase-u6agl3edszqvs`, RG `mpscalc-showcase-rg`, sub `a6b8fe11` (treated as live with real users' data by its last kit) | `0bb3ed12` (RELAYED 11-12; served bundle `Da9pY_Zr` MEASURED = the bundle that deploy recorded) -> `5e800095` | **8** (#192-#199) | No migration, no new setting (DERIVED). Deploy SCRIPT changed (two extra overlay reads, roll-forward-only rule). Package gains the patched Xml assembly (MPSCALC-224 host read belongs to this deploy). **Rollback after this deploy has a caveat** (#196: snapshots written by the new build are refused by an older build) | Needs a per-deploy card (the showcase is "NOT under the standing push-to-demo grant", B1542 kit :18); 'c' may or may not be that card (Q4). Part B stop words PENDING a word pack. Seller checks need a fresh seed secret (expired 11-12) |
| **NexusAI** | Container App `nexusaidev-app` (RG `nexusai-dev-rg`, sub `0c57ab37`, tenant #5), revision `nexusaidev-app--0000100`, sole active, Healthy | `17fc6c51` (RELAYED S99O + MEASURED: revision image tag `2.2.1-s99o-17fc6c5`, and live `build` = first 16 hex of sha256 of that sha) -> `d1152289` | **121** (#58...#205; 49 touch files that ship in the image, 72 are tests/docs/CI/records only) | No migration, no new env var. **The CI deploy route cannot run** (repo variable `CI_DEPLOY_ENABLED` unset, no `demo` GitHub environment): the deploy is a manual `az acr build` + `az containerapp update` swap by digest (S99O template). Image is rebuilt from a Dockerfile, `package.json` and lockfile that all changed since the running image | **YES: C-224** (no demo deploy until RD-876 part 2 lands; part 2 has NOT landed). 'c' does not name it; needs Kam's word (Q2) |
| **Security Composer** | Demo VM (compose stack under `/opt/hpsm/composer`), URL in project `.env`; `/site.json` answers `{"environment":"demo","guided_view":false}` (MEASURED) | `d70edf70` (RELAYED B986 last line 10-31; live contract version cannot be read publicly; served web bundle `B-n1v2_U` equals what B986 recorded, which proves web unchanged only) -> `b4681297` | **26** (#95, #106-#130) | **No migration** (0 files under `migrations/`), no `content/`, contract unchanged at 0.37.0. Dependencies change (fastify, undici, fast-uri, ip-address, vite, vitest): the VM rebuilds. Words gate (customer-visible text) must be re-run | **Probably YES:** Composer CLARIFICATIONS records "a deploy only on the product owner's card" 17 times (plus a variant at :2732); EXPIRING-GRANTS.md:24 grants push-to-demo without a card. They conflict (Q3). Footer-look row #474 OPEN, NOT RULED |

Four of four projects measured to a deployed sha with a stated instrument. UAT for HPSM, and every production-class system, stays untouched.

---

## Questions for Tuesday (each with a default)

1. **Q1 HPSM: what is the "hosted demo"?** Evidence: `hpsm-poc-demo-rg` was decommissioned 11-05 (B1303 STATUS last line: `DECOMMISSIONED: hpsm-poc-demo-rg ... group gone (ResourceGroupNotFound, exists false) at 13:47:34 AEDT`) and I re-measured it today: `az group exists -n hpsm-poc-demo-rg` = `false`, `az resource list -g hpsm-poc-demo-rg` = ResourceGroupNotFound (control: `hpsm-poc-uat-rg` lists 14 resources). The only HPSM sites left are the two UAT apps; `hpsm-poc-rg` ("dev") holds no site (Log Analytics, App Insights, OpenAI account, one action group). The word "demo" survives only as the app's mode (`HostedDemo__DraftRuleset`, "Demo alias", "Demo copy" of a report): UAT runs in that mode. Card `hpsmpoc-deploy-round-scope-1116` option a said "hosted demo now, UAT after HP's review", which reads as if a demo still existed. **Default: HPSM has no demo environment, so HPSM is out of the 'c' round; UAT stays held (EXPIRING-GRANTS.md:16); say so to Kam in plain words.** If Kam wants UAT in the round that is his word (it is the site HP reviews), plus the writes in the HPSM row (migration, grant script, setting).
2. **Q2 NexusAI: does 'c' lift C-224?** C-224 (Kam, 10-26 20:23:37) says no NexusAI demo deploy until RD-876 part 2 (the notice and the show-all button) lands. I found no merged PR that delivers part 2 (0 of 121 PR bodies describe it; #120 is part 1, #127 is a test pin, #204 caps the Log Analytics run). 'c' names "demos too" but not C-224. **Default: NexusAI is held until Kam says in words that the demo goes out without part 2 (or part 2 lands).** I did not check Jira RD-876 (no Jira access in a drafter).
3. **Q3 Composer: standing grant or card?** Grant row EXPIRING-GRANTS.md:24 allows push to the Composer demo "without a card"; Composer's own CLARIFICATIONS ends 17 entries with "a deploy only on the product owner's card" (last at :2830; a variant at :2732), and CLAUDE.md:30 says "never deploy to it without Kam's word". 'c' is a word from Kam. **Default: treat 'c' as the card for Composer provided the list on the board names it, but run the words gate on the customer-visible PRs first (#95, #113, #119, #120, #122, #124, #125, #130).** I did not measure whether each new customer-visible string is ruled (that is a seat's job: B986 Step 3 is the template).
4. **Q4 MPS: is 'c' the per-deploy card?** B1542's own kit says the showcase "is NOT under the standing push-to-demo grant" and deploys on a card. Also open: Part B stop words of #192 are "PENDING the product owner's approval" (PR #192 body line 1) and pickup:297 says they are "a WORD PACK for Kam before any deploy". **Default: MPS needs Kam's word on the Part B stop words, in addition to 'c'.** Also: is the seed identity's client secret renewed? (expired 11-12, pickup:388); if not, the three Seller checks are UNMEASURED again, as they were on 11-12.
5. **Q5 NexusAI deploy route:** `deploy-demo.yml` cannot run (see below), so the deploy is a manual swap. CLAUDE.md:277 says a demo Container Apps deploy is "Tuesday-authorisable". **Default: manual swap by digest per the S99O `swap-verify.sh` shape, a NexusAI deploy seat, Opus.** Confirm.
6. **Q6 NexusAI viewer pages:** #200 and #204 make 20 write routes answer a viewer 403 "once sign-in is configured"; PR #200's own body says the pages that call them "will show a 403 to a signed-in viewer; that is owed to the front-end lane". Whether the demo has sign-in configured is NOT MEASURED. **Default: ask Kam whether the demo should carry that before the front-end lane lands** (it is also the very thing the demo audience may click).
7. **Q7 Tenants:** MPS showcase and HPSM UAT live in tenant `ec01829b-...` / sub `a6b8fe11-...` (the `datasec-rd.com` one); NexusAI and the Composer VM live in the agent-controllable tenant #5 (`d500ebad-...`, sub `0c57ab37-...`). Which of the five Datasec environments `ec01829b` is stays UNRESOLVED (CLAUDE.md hard rule 4); I assert nothing. Each deploy seat must run its own project's `az account show` pass first.
8. **Q8 Order and one-at-a-time:** the four deploys share no resource. **Default: one deploy seat at a time, in the order MPS, Composer, NexusAI** (cheapest rollback first; MPS and Composer have a kept previous package/archive; NexusAI keeps the previous digest). Not decided by me.

---

## 1. HPSM-POC

**Environment today (MEASURED 07:3x-07:4x).** `az account show` under `HPSM-POC/4_Credentials/.azure`: sub `a6b8fe11-d1b5-4293-8727-b34aba08a705`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`. `az group exists -n hpsm-poc-demo-rg` = false. Groups present: `hpsm-poc-rg`, `hpsm-poc-sm-rg`, `NetworkWatcherRG`, `mpscalc-showcase-rg`, `hpsm-poc-uat-rg`. UAT group: 2 sites (`app-hpsmpoc-web-uat-25onzn`, `app-hpsmpoc-api-uat-25onzn`), plan `asp-hpsmpoc-uat`, SQL server `sql-hpsmpoc-uat-25onzn` (databases `hpsmpoc`, `master`), vault, storage, OpenAI account, identities, Log Analytics, App Insights. Deployed by `scripts/deploy-from-ci.sh deploy <sha> hpsm-poc-uat-rg <web> <api>` from a project clone under `.tools/` (B1540 P2), triggered by a seat; CI (`ci.yml`) has no deploy job and no cloud credentials (PR #322 body: "ci.yml builds and tests on a push to main and keeps the build packages; it has no deploy job").

**Deployed now.** `576231b7697bf6a758d8091e9099c0dd60c2dce7` = squash of #316, merged 2026-11-12T06:17:24Z (`gh api commits`, MEASURED). Source: `1_Project_Definition/Briefs/2026-11-12_B1540_STATUS.md` last line `DEPLOYED B1540: 576231b7... https://app-hpsmpoc-web-uat-25onzn.azurewebsites.net` (RELAYED; second attempt, line 222 `PART P VERDICT: PASSED`). **Live check, MEASURED 07:40-07:41:** web `/` 200 and the page holds BUILD_ID `6O6hbyfZwF7nqAmqe7MVh` x1 (the build B1540 STATUS :71 records for TARGET) and PREV's `NQga609FQ4iKZFwQ1rtsT` x0 (control: both counted by the same `grep -c -F` on the same file); web `/api/health` 200 `{"status":"ok","service":"hpsm-poc-web"}`; API `/health` 200 `Healthy`. The API's own sha is not exposed by any endpoint: RELAYED only.

**Main head** `678a1153d28be006a088a3b1fba8f5aab52e8d0e` (`gh api branches/main`, MEASURED 07:3x). `compare 576231b7...main`: `ahead`, ahead_by 9, behind_by 0, 120 files. Control: #316's merge sha is `576231b7` and ahead_by (9) equals the 9 merged PRs found.
CI on main head: `ci` run 43753987454 completed/success attempt 1; 21 of 22 check-runs success, the 22nd is `dependency review (pull requests; ...)` skipped (PR-only job); open code-scanning alerts 0; open PRs 0. Packages `deploy-web-678a1153...` and `deploy-api-678a1153...` exist, not expired (expire 2026-11-22T19:55Z / 19:58Z).

**What rides along (9 PRs, merge order):**

| PR | merged AEDT | user-visible effect (one plain line) | deploy-time? |
|---|---|---|---|
| #317 | 11-15 07:34 | The HP reviewer's Demo view shows each customer's alias (not its stored name) on six more pages; every in-progress answer count reads "N of M scored questions answered" | no |
| #318 | 11-15 13:14 | Behind the scenes: the API believes a forwarded client address only when a shared header value from the web front end arrives with it | **YES, setting:** API `ForwardedHeaders__Proof` and web `HPSM_FORWARD_PROOF` as Key Vault references, "a separate infra change"; fail-closed (only the unknown-link limit is affected) until stored on both. A Key Vault reference that does not resolve makes the API refuse to start (PR body "What a deploy needs first") |
| #319 | 11-15 16:04 | none (a test's own timeout) | no |
| #320 | 11-15 20:13 | The industry field becomes a four-choice list (Healthcare, Financial services, Public sector, Other); new question-set version (ruleset 0.1.3, content 0.7.1) | **YES, setting:** `HostedDemo__DraftRuleset` ships WITH the API or the host refuses to start (PR body "Deploy notes" 1); existing sample customers keep old stamps until a Demo reset (needs force while frozen) |
| #321 | 11-15 21:50 | The assessor can say how each answer is known, on the live question card (web only) | no (PR: "No migration. No API or contract change.") |
| #322 | 11-15 22:39 | The executive report PDF gets a contents page with section links and a header link back to it | note: the Demo copy of a report issued BEFORE the deploy is refused "This report changed after it was issued" until re-issued |
| #323 | 11-16 02:21 | Reviewer's question changes: reordered and reworded questions, two answers added ("Partly", "Covered another way"); new set ruleset 0.1.4, content 0.7.2; still 16 questions | **YES, setting:** `HostedDemo__DraftRuleset` moves to `snapshot-policy-aligned@0.1.4` (PR body: "in all three places tied together (appservice.bicep, test_security_baseline.py, HostedDemoTests.cs)"); the new API and the new setting must ship together (the API refuses to start when the seed ruleset and the setting differ, in both directions); in-progress sample "Quokka Freight" cannot be scored until a Demo reset |
| #324 | 11-16 03:14 | Approved narratives can be edited again, each earlier review kept in a new append-only table | **YES, migration:** "Run the Assessment migration bundle: one new migration, one new table", THEN re-run `infra/sql/api-identity.sql` (one new DENY UPDATE, DELETE on `poc.narrative_revision`; the table must exist first). Never run the migration's Down on a hosted database once revision rows exist (PR #324 body "Deploy-time effects" 1, 2, 5) |
| #325 | 11-16 06:43 | none (a test waits for the server's reading instead of racing it) | no |

**Holds touching a deploy (quotes by file:line, printed by a program today):**
- `0_Brain/tasks/EXPIRING-GRANTS.md:16`: "UAT untouched while HP reviews" (Kam 11-06 10:12:54 "yes, hold UAT but work on everything else"; re-read 11-08 as reaffirmed; "The UAT hold ends on his word (no date given), not by inference"). **'c' does not name UAT and I do not read it as lifting this.**
- `0_Brain/tasks/EXPIRING-GRANTS.md:9`: Kam 11-15 19:15:40 "a - Allow the one migration (gated, not deployed) | note: deploy as well" and 19:16:20 "once all changes are made, deploy to all systems so everything is synced and has all recent changes"; the row's own text: "to every HPSM-POC hosted environment", and "the exact list of what rides along [goes] on the live board". Today the only HPSM hosted environment is UAT, which is the held one. **This is the conflict Q1 asks Kam to resolve.**
- `0_Brain/daily_tuesday/2026-11-16.md:51`: "Why a card and not the 19:16 grant alone: ... it conflicts with the live 11-06 'UAT untouched while HP reviews' hold".
- `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:64`: card `hpsmpoc-deploy-round-scope-1116` "(rec a: hosted demo now, UAT after HP's review, HPSM only; DEFAULT HOLD ...)".
- Class: B1540 marks Part P `[PROD-CLASS]`; the HP link in B1303 says UAT "is the site HP has a link to".

**Deploy route (if Kam does put HPSM in, template = B1540 SEAT-D61 `tuesday/briefs/2026-11-12_B1540_SEAT-D61_hpsmpoc-uat-deploy-messaging.md`, records B1543).** (a) Gate: CI package for the exact sha (artifacts above). (b) PRE-DEPLOY SIGNALS, D-5 `CHECKPOINT DATABASE STILL AWAKE`, backup of the live wwwroots as the code backup, a database copy/restore point (T0) BEFORE the migration (B1466 used `hpsmpoc-b1466-pre`, deleted later by D60). (c) Order: migration bundle, `api-identity.sql` re-run, then code AND setting together (`HostedDemo__DraftRuleset`, in one window), then optionally the forwarded-proof pair as a separate change. These are Azure writes beyond B1540's "code only, NO database write"; they are approval-class (UAT, prod-class). (d) The deploy command: `scripts/deploy-from-ci.sh deploy <sha> hpsm-poc-uat-rg app-hpsmpoc-web-uat-25onzn app-hpsmpoc-api-uat-25onzn`; windows web 420 s, API 900 s; exit 3 = deployed but not proven.
**Known hazard (MEASURED in the last attempt):** B1540's first attempt landed web and then the API zip upload failed with Kudu HTTP 504, leaving UAT mixed (web new, API old) for about 17 minutes until RB-A restored the old packages (STATUS :168). The second attempt passed. Worth a retry rule or a `deployments/latest` read in the next deploy script (STATUS :235(a)).
**Rollback.** Code: RB-A = redeploy the previous packages kept in `.tools/b1540/rollback/<sha>/` (here `576231b7`'s packages would need to be captured as the code backup before the swap; B1540 captured `009421a2`'s), wait for API `/health`+`/health/ready` and web `/api/health`, live-check equality and BUILD_ID. **Database: there is no safe Down once `narrative_revision` rows exist** (#324 body); restore is from the pre-migration copy or point-in-time backup, and a restore loses everything written since. A code-only rollback leaves the new table in place (harmless to older code; not measured).
**Live checks a deploy seat runs** (B1540 P3): `/api/health` and `/health` 200 x3 ten seconds apart, `/health/ready` 200; `/` 200, `/customers` 307, session `{"signedIn":false}`; the follow-ups API probe before = after; 8 plain sign-ins; route tables before/after; security views and refusals (403 `uat.action-off`); words table; BUILD_ID named x1 and PREV's x0; DLLs embed the new sha x1; settings hashes equal; SQL firewall exactly `AllowAllWindowsAzureIps`; databases exactly {`hpsmpoc`, `master`}; activity log shows only the deploy's rows (0 `firewallRules/write`, `databases/write`, `databases/delete`). New for this round: the new question-set version on a fresh snapshot, `api-identity.sql` DENY present, a re-edit of a test narrative writes a `narrative_revision` row.
**NOT MEASURED for HPSM:** UAT's current `HostedDemo__DraftRuleset` value (reading app settings prints values; a hashing wrapper is the B1303/B1540 way); whether App Service passes the proof header web to API unchanged (#318 says not measured); whether the Key Vault reference for the proof exists; the API's deployed sha by any live instrument.

---

## 2. MPS Commercial Calculator

**Environment today.** Hosted **showcase** `app-mpscalc-showcase-u6agl3edszqvs`, RG `mpscalc-showcase-rg`, sub `a6b8fe11...`, tenant `ec01829b...` (MEASURED: `az account show` under the MPS `.azure`; ARM GET of the site, not `az webapp show`, per DRAFTER_RULES: `state` Running, `enabled` true). Deployed by `scripts/deploy-from-ci.sh fetch <sha>` then `deploy <sha> <rg> <site>` (header read from main with `gh api`; it downloads the CI artifact `deploy-mpscalc-<sha>`, verifies it, runs PRE-1 on the overlay, `az webapp deploy --clean true`, then live-checks the wwwroot). `ci.yml` is the only workflow; it builds the package and keeps it 7 days; no deploy job. Variables 0, environments 0 (MEASURED).

**Deployed now.** `0bb3ed12808d72d3187c51d56852b7ecd2174666` (RELAYED: `2026-11-12_B1542_STATUS.md` last line `DEPLOYED: 0bb3ed12... live-check 0; ... bundle BbrcPc3D->Da9pY_Zr = package 50/50 ... store 23/23 equal ... rollback e027ebd0 open`). **MEASURED 07:37:** `GET /` 200 and the HTML names `index-Da9pY_Zr.js` x1 (control: the same file grep for any other `index-*.js` name returns only that one). That equals the bundle the deploy recorded, so no web change has gone out since; it cannot distinguish API-only changes, so the API sha is RELAYED.
**Main head** `5e80009525138879031c4b07a18436242dadf46c` (MEASURED). `compare 0bb3ed12...main`: ahead_by 8, behind_by 0, 44 files; control: 8 merged PRs found after #191 (= `0bb3ed12`). CI: `ci` run 43724577328 success, `Push on main` 43724577088 success; package `deploy-mpscalc-5e80009525138879031c4b07a18436242dadf46c` exists, not expired (to 2026-11-22T14:44:30Z); open code-scanning alerts 0; open PRs 0.

**What rides along (8 PRs):**

| PR | merged AEDT | user-visible effect | deploy-time? |
|---|---|---|---|
| #192 | 11-15 09:18 | none for customers: deploy script only. PRE-1 (the pre-deploy check of the hosted price overlay) now refuses every form the app's reader refuses; **the deploy rolls forward only** (refuses a package older than the first build that knows care-pack/staging once the store holds such rows) | script change; "The Part B stop words are PENDING the product owner's approval" (PR body line 1) |
| #193 | 11-15 12:59 | none on hosted (dev stub saves a held rental quote, follows the rebate default and Duplicate); touches `web/src` stub files, so the served bundle may still change (NOT MEASURED) | no |
| #194 | 11-15 14:28 | none: deploy script order (overlay re-read runs last; a shallow checkout is "undecided"; three patterns end at end-of-string) | script |
| #195 | 11-15 18:42 | none: CI runs four PDF text specs | no |
| #196 | 11-15 20:04 | Fleet lines get a stable id so the price audit follows a renumbered line | **Rollback caveat (PR body "Deploy note (rollback)"):** a snapshot written by the new build carries `fleetLineId`; an older build "refuses that snapshot at load, and refuses every quote that refers to it"; "A rollback after deploy therefore needs those snapshots kept readable, or a roll forward". Old quotes get ids computed on read; stored files are not rewritten until the next save |
| #197 | 11-15 21:59 | The rental price screen shows "Software / month" once (the summary card is removed; the breakdown row stays) | no |
| #198 | 11-15 22:16 | none (regression rows for the source lock waits) | no |
| #199 | 11-16 01:28 | none visible; the API package now ships the patched `System.Security.Cryptography.Xml` 10.0.15 | **MPSCALC-224 host read is part of the deploy** (PR body line 16, pickup:85): "The package reaches a host only on its own deploy card. The host-side read (the docker-log patch line and the loaded Xml file version) belongs to that deploy." |

**Migration:** none (0 of 44 changed paths contain `migrat`, 0 contain `bicep` or `appsettings`; control: 6 of the 44 start with `src/`). **New app setting:** none (DERIVED from the file list; the new optional keys of the last round, `MpsCalc:Templates:Path` and `MpsCalc:Feedback:RateLimit:PerHour`, are still absent on hosted and still not needed; templates stay in memory and are lost at restart, RELAYED B1542).

**Holds (file:line, quoted):**
- `tuesday/briefs/2026-11-12_B1542_SEAT-D62_mps-hosted-deploy-0bb3ed12.md:18`: "The card above is a per-deploy authority; **the hosted MPS site is NOT under the standing push-to-demo grant**."
- `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:297`: "Part B's stop words are a WORD PACK for Kam before any deploy."
- `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:85`: "MPS #199 lane M-O (224/397/398) -> 5e800095 (squash; 224 stays OPEN for its host read)."
- `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:388`: "D62 STOPPED 18:27: the seed identity's client secret EXPIRED (AADSTS7000222), so no Seller GET (quote list, /quotes/figures POST-1, inventory)" (and :375 "Seller reads UNMEASURED by Kam's 18:36 ruling").
- MPSCALC-224's host read: **Kam's 'c' does not lift it** (it is a part of the deploy, not a block): the deploy seat must do it. Whether the deploy itself is allowed is Q4.
- Class: the project's `CLAUDE.md` has 0 lines matching `showcase|production` (no positive control run); the B1542 kit still treats the showcase as "live with real users' data".

**Deploy route.** Template: `2026-11-12_B1542_SEAT-D62_mps-hosted-deploy-0bb3ed12.md` (clone of B500/B448), records B1544. Steps: Step 0 refusals, WORDS check against the product owner's rulings, CI check (green run + artifact for the exact sha), target asserts, backup of the store counts, `scripts/deploy-from-ci.sh fetch 5e80009525138879031c4b07a18436242dadf46c` then `deploy ... mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs` from the target sha's worktree; exit 3 = deployed but not proven; **never `az webapp show`** (it fetches the publish profile); use a plain ARM GET. Expected after: bundle `Da9pY_Zr` replaced by a new bundle if web changed; Pkcs `10.0.15` and Xml `10.0.15` in the API deps; `RuntimeSuccessful` x1; 401s on unauthenticated routes; store counts equal before and after.
**Rollback.** A code rollback is to the kept package: `deploy-mpscalc-0bb3ed12...` still exists on GitHub (MEASURED, not expired, expires 2026-11-19T04:30:15Z; whether a local copy is kept is NOT MEASURED), so a deploy seat must copy it into the project BEFORE the swap (B1542 had to rely on a local zip because `e027ebd0`'s artifact had expired). But **#196 means a rollback after this deploy needs the new snapshots kept readable or a roll forward**; and #192's roll-forward-only rule refuses a package older than the floor once care-pack/staging rows exist.
**Live checks:** B1542's list: served bundle vs package (50/50 files), Pkcs 2/2 and the new Xml, settings 0/0/0 changes, store 23/23 equal before/after, reference MATCH, leak 0 new, start log clean (Accept lines, 0 refused, host 10.0.15), 401s on 15 routes including templates GET/POST; Seller quote/figures/inventory reads need a working seed secret (Q4).
**NOT MEASURED for MPS:** the API's live sha; whether the seed secret has been renewed; whether `web/src` stub changes (#193) alter the shipped bundle; the live host's Xml file version (that is MPSCALC-224's read).

---

## 3. NexusAI

**Environment today (MEASURED 07:3x).** `az account show` under `NexusAI/4_Credentials/.azure`: sub `0c57ab37-349c-47ae-a10f-e284a380bbb9`, tenant `d500ebad-cf53-4f2a-a501-f831289e67fc` (#5). Container App `nexusaidev-app` in `nexusai-dev-rg`: `az containerapp show`: provisioningState Succeeded, activeRevisionsMode Single, latest = latestReady = `nexusaidev-app--0000100`; the only revision (created 2026-10-16T05:17:20Z, active, traffic 100, Healthy); image `nexusaidevacrfa39.azurecr.io/nexusai@sha256:c12c43e538f1274c1a7ba180f2cdfd595be63ec16eee0e45c690903734e08e4f`; 22 env names (same count as the S99O handover). Public health (host not repeated here; it is in the scratch file `nx_app.json`): `GET /api/health` 200 `{"status":"ok"...,"version":"2.2.1","build":"def3ac7e654fdacd"}` (07:34:55 AEDT).
**How it is deployed.** The repo has a gated workflow `deploy-demo.yml` (push to main builds an image in ACR; a `demo`-environment reviewer click gates the swap) **but it cannot run today: repository variables = 0 (so `CI_DEPLOY_ENABLED` is unset; `deploy` and `build` both skip), GitHub environments = only `dev` (no `demo` environment, so no required reviewer exists).** Evidence: `gh api actions/variables` total_count 0 (control: the same token lists one environment, `dev`); last 5 `Deploy demo` runs all `skipped`; of the 239 runs of that workflow, 0 were non-skipped in the newest 100. So the real route is the manual one S99O used: `az acr build` the image, then `az containerapp update --image <digest>` with a verified swap (template `session-tools/s99o/deploy/swap-verify.sh`, `HANDOVER-S99O.md`). **There is no tracked Tuesday kit for a NexusAI demo deploy** (I found only `2026-10-25_B658_SEAT-M10_nexusai-815-demo-workflow-pin.md`, which pins workflow actions). That absence is the first finding: a deploy kit must be drafted.

**Deployed now.** `17fc6c5157d5446cc015e97555fdc1ffcdc986ee` = merge of PR #86 (RD-846), 2026-10-16T04:16:55Z. Three independent reads agree: (1) ACR tag of the running digest `c12c43e5...` is `2.2.1-s99o-17fc6c5` (`az acr repository show-manifests`); (2) `HANDOVER-S99O.md:9` (`Demo = nexusaidev-app--0000100 ... tag 2.2.1-s99o-17fc6c5`); (3) live `build` `def3ac7e654fdacd` = first 16 hex of `sha256` of that 40-hex sha (`printf %s <sha> | shasum -a 256` gives `def3ac7e654fdacd`; control: the same on main's sha gives `2a833eea082f0bbe`, different).
**Main head** `d1152289f7c0f2d97b4bd82187488c47d51c65fc` = the merge of #205. `compare 17fc6c5...main`: ahead, ahead_by **406** commits, behind_by 0, 260 files (merge-commit style: one PR is several commits, so the PR count is NOT ahead_by; control: PR #86's merge sha equals the deployed sha and #205's equals main). CI on main head: `Build` 43741131028 success, `npm-audit` success, `Gitleaks` success, `Deploy demo` 43741130949 skipped; **open code-scanning alerts: 63** (not a deploy blocker I know of; recorded). Open PRs 0.

**What rides along: 121 PRs (#58...#205), 49 of which touch files that ship in the image** (`backend/`, `static/`, `Dockerfile`, `package.json`, `package-lock.json`; measured per PR with `pulls/<n>/files`), 72 do not (tests, docs, CI, tooling, HISTORY records). Merged strictly after #86's merge time, base main, by `gh api pulls?state=closed` (control: #86 and #205 are in the 184 merged-PR list; #86 excluded, #205 included). The "effect" is each PR's own title; the ones a demo viewer will see:
- **Sign-in and roles:** #200 administrators only on 20 write and setup routes (settings, restart, backup, model switch, feedback edit, first-run reset, chat cache, managed-identity status), the model switch loses its fixed password; #201 every refused request writes an audit row, a role change records before/after; #195 changing a user's access ends their sessions; #204 a viewer cannot re-triage; #199 retires `GET/POST /api/settings/agent` (the five stored values stay).
- **Risk conditions:** #97 risk SQL comes only from 13 fixed server templates, request SQL refused; #120 a 1,000-row ceiling (silent cut: **this is RD-876 part 1; part 2 not landed**); #204 Log Analytics risk run capped at 1,000 rows; #131/#132 edited risk level stored lower-case, empty level listed; #203 custom-SQL control removed from the Testing page.
- **Pages:** #187 Settings brand line wraps at phone width, dashboard tile rows two per row 768-991 px; #203 open-site banner above the loading overlay; #205 first-run AI re-save keeps the AI setting, step 3 "enforce" shows success, endpoint slash stripped, sign-in icons digest, absolute asset paths; #180 generated shell palette tokens; #94 DOM text stays text (XSS fix).
- **Assistant:** #92/#93/#99/#143/#147/#150 user-lookup fixes (a pronoun-led question is not a user lookup, plural nouns, roster checks); #95 Ollama runtime slice; #198 `GET /api/models` answers 200 and two settings writes validate before write.
- **Dependencies (image rebuild):** #104, #105, #107, #108, #149, #152 (archiver 8, sqlite3 6, joi 18.3.1, follow-redirects 1.16.2, nodemailer, smtp-server, body-parser). `Dockerfile` and `package.json`/lockfile all differ from the running image, so the ACR build is a real rebuild. `backend/simpleDb.js` changed (#158 retires unused SQLite risk-condition writers; no schema change).
- **Security hardening with no visible change:** #58, #70, #88, #89, #112, #172, #182, #184, #186, #189, #197.

**Deploy-time flags.** Migrations: 0 paths contain `migrat` (260 files). New environment variables: none known (PR bodies: 3 of 121 match `migrat|schema|setting|env`, read: #108 (library text), #131 ("no migration", stored mixed-case rows unchanged), #199 (stored values untouched)); **env names must stay identical (22)** as S99O verified. Persistence: settings and data live on the Azure Files share `nexusai-data`; the S99O backup `4_Credentials/demo-share-backup-2026-10-16-s99o-pre-rd846/` is the shape to repeat. #131 changes the stored form of an edited risk level for new edits only. #201 adds audit rows (growth on the share). #200: viewers get 403s on pages a viewer can reach until the front-end lane (Q6).
**The full list (121; all measured):**

| PR | merged AEDT | ships in the image? | title (what the PR says it changes) |
|---|---|---|---|
| #87 | 10-17 13:07 | YES (Dockerfile) | RD-848: drop the build stage's duplicate COPY of the npm pair; guard every stage |
| #88 | 10-17 17:40 | YES (backend) | RD-801+RD-822: feedback log-injection fix (merged with main 065a0d8) |
| #89 | 10-17 19:15 | YES (backend) | RD-802: provisioning log-injection fix (merged with main b89c938) |
| #90 | 10-17 21:02 | no (tests/docs/CI/tooling only) | RD-828 gate-14 slice 2: census/labeller/filter cells (merged with main 55047f4) |
| #58 | 10-18 21:43 | YES (backend) | RD-761: Log Analytics endpoint allow-list at the sink + writer admin gate (CodeQL #23-#26) |
| #70 | 10-19 00:06 | YES (backend) | RD-775: aiReadiness — identify the API key by an opaque id, never a hash (CodeQL js/insufficient-password-hash) |
| #95 | 10-19 02:32 | YES (backend) | RD-794: Ollama runtime slice (RD-478), stacked on RD-761 — gate 25 landing PR |
| #94 | 10-19 10:58 | YES (static) | RD-778: js/xss-through-dom x8 — DOM text stays text (DRAFT) |
| #92 | 10-19 20:14 | YES (backend) | RD-856: a pronoun-led question is not a user lookup (DRAFT) |
| #93 | 10-19 23:26 | YES (backend) | RD-857: whole-word skip list + department/location guard in the user lookup (DRAFT, stacked on #92) |
| #91 | 10-20 03:22 | no (tests/docs/CI/tooling only) | RD-476: assistant system prompt — answer from the data only, name what is missing, cite sources (DRAFT, Kam's ruling pending) |
| #96 | 10-20 06:48 | no (tests/docs/CI/tooling only) | C-170 / RD-460: self-contained Marketplace package, forward-merged with main 888203c (counts-only TURN) |
| #100 | 10-20 14:43 | no (tests/docs/CI/tooling only) | HISTORY: S101O 2026-10-18/20 entry (docs only) |
| #99 | 10-20 16:59 | YES (backend) | RD-863: plural group nouns and Object.prototype names are not user lookups (G28-1) |
| #98 | 10-20 22:16 | no (tests/docs/CI/tooling only) | RD-782..789: CodeQL alerts in test code (RD-786 21 of 26) |
| #97 | 10-21 04:12 | YES (backend) | RD-774 + RD-836: risk-condition SQL from fixed server templates only; request SQL refused; admin-only writers |
| #104 | 10-21 10:00 | YES (package-lock.json) | RD-879: follow-redirects 1.16.0 -> 1.16.1 (lockfile only; GHSA-q3jh-wrc6-jgq8, GHSA-8r9p-f939-6h3c, high) |
| #103 | 10-21 16:14 | no (tests/docs/CI/tooling only) | RD-780: group the alternation in propose-dark-retheme.js (CodeQL #244, #245) |
| #102 | 10-21 17:25 | no (tests/docs/CI/tooling only) | Records B362: HISTORY entry for the PR #97 landing (RD-774 + RD-836), gate 29 records |
| #101 | 10-21 23:28 | no (tests/docs/CI/tooling only) | RD-874 + RD-875: settings-plant guards in three tests; tests/uat-run.js has no default target and honours the port |
| #105 | 10-23 07:42 | YES (package-lock.json) | deps: nodemailer 10.0.9 -> 10.2.1, ip-address 10.7.2 -> 10.7.4 (GHSA-39m8-27wv-hr27, GHSA-rxp7-6hxx-x8q5), lockfile only |
| #107 | 10-24 20:28 | YES (package-lock.json) | deps: body-parser 2.3.0 -> 2.4.0 (lockfile only; GHSA-27r3-jxmh-p828) RD-881 |
| #106 | 10-24 22:04 | no (tests/docs/CI/tooling only) | Test cells for eight test-strength tickets (N1) |
| #109 | 10-25 00:05 | no (tests/docs/CI/tooling only) | Records: HISTORY.md entry for the 24 Oct landings and ticket moves |
| #108 | 10-25 01:52 | YES (package-lock.json, package.json) | Bump nodemailer and smtp-server |
| #110 | 10-25 07:22 | YES (backend) | RD-862, RD-873: dead function removed, test writes bounded |
| #111 | 10-25 07:36 | no (tests/docs/CI/tooling only) | Give Build, Package and npm-audit a read-only GITHUB_TOKEN |
| #114 | 10-25 12:49 | no (tests/docs/CI/tooling only) | Records B656: HISTORY entry for the PR #110 and PR #111 landings |
| #113 | 10-25 12:53 | no (tests/docs/CI/tooling only) | RD-815: pin the demo workflow's azure/login steps to a commit |
| #112 | 10-25 17:34 | YES (backend) | RD-777 + RD-776: validators.js input filter for CodeQL #83, #84, #43 (supersedes #67) |
| #115 | 10-25 19:41 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the PR #112 landing |
| #116 | 10-25 23:41 | no (tests/docs/CI/tooling only) | RD-844: banner guard answers the cdnjs stylesheet with an empty stand-in |
| #117 | 10-26 10:08 | no (tests/docs/CI/tooling only) | RD-882, RD-850, RD-851, RD-852, RD-843: test cells for the validators filter, the Dockerfile stage model and the CSP intake residue |
| #119 | 10-26 20:06 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the PR #117 landing and the 26 Oct follow-ups |
| #120 | 10-26 20:43 | YES (backend) | RD-885, RD-849, RD-876 part 1: git-env-proof helper, C1 escapes in logSafe, a 1,000-row run ceiling |
| #118 | 10-27 02:07 | no (tests/docs/CI/tooling only) | RD-867: bind the sustainability logger's live test stand to loopback |
| #121 | 10-27 03:57 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the PR #120 and PR #118 landings |
| #123 | 10-27 04:59 | YES (backend) | RD-878: PUT /api/risk-conditions/:id answers 400, not 500, for a risk_level that is not a string |
| #122 | 10-27 05:38 | no (tests/docs/CI/tooling only) | RD-873: re-shape test writes so CodeQL stops flagging them (alerts 96 98 99) |
| #124 | 10-27 07:03 | no (tests/docs/CI/tooling only) | Records B788: HISTORY entry for the PR #123 and PR #122 landings |
| #125 | 10-27 08:37 | no (tests/docs/CI/tooling only) | RD-887: pin the fallback to 100 of the risk-run row clamp for a limit that is not a number |
| #126 | 10-27 09:54 | no (tests/docs/CI/tooling only) | Records B795: HISTORY entry for the PR #125 landing |
| #127 | 10-27 11:07 | no (tests/docs/CI/tooling only) | Risk query limit: pin today's answers for 0, Infinity, empty and 2.9 (tests only) |
| #128 | 10-27 12:46 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the PR #127 landing and the odd-row-limit ruling |
| #129 | 10-27 16:15 | YES (backend) | RD-891: one write-probe helper with a unique, exclusive probe name |
| #130 | 10-27 19:35 | no (tests/docs/CI/tooling only) | RD-873 / RD-811: four test sites re-shaped for their CodeQL alerts |
| #131 | 10-27 19:36 | YES (backend) | RD-893: store an edited risk level lower-case so the level lists find it |
| #132 | 10-27 23:05 | YES (static) | Testing page: list a condition whose stored risk level is empty (RD-892 part a) |
| #133 | 10-28 01:07 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the PR #129 to #132 landings and their follow-up tickets |
| #134 | 10-28 05:11 | no (tests/docs/CI/tooling only) | Write probe: pin the unlink error handling, the foreign-file safety and the descriptor close (RD-894) |
| #135 | 10-28 06:07 | no (tests/docs/CI/tooling only) | Testing dropdown: pin the exact empty-level label and add padded and accented level rows (RD-898) |
| #136 | 10-28 06:54 | no (tests/docs/CI/tooling only) | Concurrent settings writers: the control cell no longer passes on a thrown error alone (RD-895) |
| #137 | 10-28 08:34 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the PR #134 to #136 landings |
| #138 | 10-29 12:48 | YES (static) | RD-897: remove the dashboard script's unused anomaly filter and its display helper |
| #141 | 10-29 16:03 | no (tests/docs/CI/tooling only) | Records B893: HISTORY entry for the PR #138 landing |
| #140 | 10-29 18:19 | no (tests/docs/CI/tooling only) | RD-899: pin the write probe's write step and its descriptor close when the write fails |
| #142 | 10-29 18:55 | no (tests/docs/CI/tooling only) | Records B894: HISTORY entry for the RD-868 and RD-869 rulings |
| #139 | 10-29 19:55 | no (tests/docs/CI/tooling only) | RD-900: count a tamper-cell refusal only with the product code and a torn sample (test only) |
| #144 | 10-29 23:02 | no (tests/docs/CI/tooling only) | RD-407: the fresh-install controls count retries instead of timing them |
| #145 | 10-30 04:21 | no (tests/docs/CI/tooling only) | Records B915: HISTORY entry for the PR #140, #139 and #144 landings |
| #143 | 10-30 10:09 | YES (backend) | RD-869 RD-870: check the user roster before the skip list, one shared name capture |
| #146 | 10-30 12:11 | no (tests/docs/CI/tooling only) | Records B927: HISTORY entry for the PR #143 landing (RD-869, RD-870) |
| #147 | 11-01 10:00 | YES (backend) | RD-910: a roster read that is a list holding an empty entry now keeps only its rows |
| #148 | 11-01 12:03 | no (tests/docs/CI/tooling only) | Records B1029: HISTORY entry for the PR #147 landing (RD-910) |
| #149 | 11-01 16:49 | YES (package-lock.json) | RD-913: lockfile only, raise follow-redirects to 1.16.2 and joi to 18.3.1 |
| #150 | 11-01 21:32 | YES (backend) | RD-912: keepRosterRows keeps only the rows of the chat route's two later roster reads and of the sibling lookup's roster read |
| #151 | 11-01 23:23 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the PR #149 and PR #150 landings (RD-913, RD-912) |
| #152 | 11-02 02:25 | YES (backend, package-lock.json, package.json) | RD-913: archiver 8, sqlite3 6 and a scoped jest transform; production audit reads zero |
| #153 | 11-02 05:03 | no (tests/docs/CI/tooling only) | Records B1088: HISTORY entry for the PR #152 landing (RD-913) |
| #154 | 11-02 12:20 | no (tests/docs/CI/tooling only) | Records: sqlite3 successor ruling and the assessment's findings (RD-919) |
| #155 | 11-02 21:59 | no (tests/docs/CI/tooling only) | RD-923: retire the legacy docker compose path |
| #156 | 11-02 23:44 | YES (backend) | RD-915, RD-920, RD-922: pin the export's compression level, make insertPrinterLog return the new id and finalize, make clear_db.js wait for each statement |
| #157 | 11-03 01:32 | no (tests/docs/CI/tooling only) | Records B1149: HISTORY entry for the ten low-risk ticket decisions and the two landings |
| #158 | 11-03 05:56 | YES (backend) | RD-904, RD-905, RD-906: retire the unused SQLite risk-condition writers |
| #159 | 11-03 08:20 | no (tests/docs/CI/tooling only) | Records B1187: HISTORY entry for the landing of #158 and the retirement decision |
| #161 | 11-03 12:37 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the landings of #155 and #156 (RD-923, RD-915, RD-920 to Testing) |
| #160 | 11-03 12:54 | YES (backend) | RD-917: streamExport rejects on a closed destination, drops a vanished file from the manifest, and settles with a directory at a by-name site |
| #162 | 11-03 14:57 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the landing of #160 (RD-917 to Testing; counts file released) |
| #163 | 11-03 20:28 | no (tests/docs/CI/tooling only) | RD-922: the reset script empties all six tables, pinned by a failure-path test |
| #164 | 11-03 22:27 | no (tests/docs/CI/tooling only) | Records B1235: HISTORY entry for the landing of #163 as a move to Testing |
| #165 | 11-04 13:26 | YES (backend) | RD-902: the sync on GET /api/risk-conditions runs only when the administrator check passes |
| #166 | 11-04 14:59 | no (tests/docs/CI/tooling only) | Records B1274: HISTORY entry for the landing of #165 as a move to Testing |
| #167 | 11-04 22:35 | no (tests/docs/CI/tooling only) | RD-924: K1 pins the first-run input of the RD-902 read-path check and asserts sign-in is configured |
| #168 | 11-05 02:19 | no (tests/docs/CI/tooling only) | Records B1292: HISTORY entry for the landing of #167 (RD-924) |
| #169 | 11-05 09:09 | YES (package.json) | RD-916: the jest block moves to jest.config.js, and two cells hold the default transform entry and the resolved plugin |
| #170 | 11-05 17:18 | no (tests/docs/CI/tooling only) | Records B1308: HISTORY entry for the landing of #169 as a move to Testing |
| #171 | 11-06 12:22 | no (tests/docs/CI/tooling only) | Records: pass over RD-782 to RD-789, RD-774 and RD-836 |
| #172 | 11-06 15:27 | YES (backend) | RD-798: five AI-suggestion log lines go through logSafe, and a cell red at the base holds each one |
| #173 | 11-06 17:15 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the landing of #172 and the ticket pass over it |
| #174 | 11-06 18:27 | no (tests/docs/CI/tooling only) | RD-573: the jest port band moves below Linux's ephemeral range, and a cell judges it |
| #175 | 11-06 19:12 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the roles-and-layout tickets (RD-927 to RD-958) |
| #176 | 11-06 21:05 | no (tests/docs/CI/tooling only) | RD-779, RD-781, RD-790, RD-803, RD-809, RD-812, RD-813: eight CodeQL alerts in developer tools and hand-run test pages are fixed by seven small edits that touch no product file |
| #177 | 11-06 22:24 | no (tests/docs/CI/tooling only) | Records: HISTORY entry for the word pack decisions and the owed findings |
| #178 | 11-07 00:01 | no (tests/docs/CI/tooling only) | RD-928: add a route-to-capability inventory measured over HTTP, with a census that fails on a route with no row |
| #179 | 11-07 03:40 | no (tests/docs/CI/tooling only) | RD-928: a browser harness records today's layout at four widths and both themes, and its record writer refuses a link or an existing path |
| #180 | 11-07 06:34 | YES (static) | RD-936: the generated shell palette tokens, the guide section that rules them and a guard that measures every pair in a browser engine |
| #181 | 11-07 07:25 | no (tests/docs/CI/tooling only) | Records: landings of RD-928 parts A and B, and their review findings |
| #182 | 11-09 08:35 | YES (backend) | Wrap 44 flagged log lines in logSafe so request text cannot forge log entries (RD-798, RD-799, RD-800) |
| #183 | 11-09 15:31 | no (tests/docs/CI/tooling only) | RD-959, RD-960, RD-961: the port band E3 control counts a literal 64, the comments name the host condition, and the tests remove the directories they make |
| #184 | 11-09 17:19 | YES (backend) | RD-973: setQuickQuestions waits for the ROLLBACK to finish before it rejects, and a cell judges the order |
| #185 | 11-10 07:55 | no (tests/docs/CI/tooling only) | HISTORY.md: records for pull requests 180, 183 and 184 |
| #186 | 11-11 02:20 | YES (backend) | CSP intake: trim Unicode edge spaces and the BOM, drop userinfo behind %40, and type and bound violatedDirective and lineNumber (RD-759, RD-796) |
| #187 | 11-11 03:12 | YES (static) | RD-962, RD-963: Settings brand line wraps at phone width; dashboard tile rows go two per row from 768 to 991 px |
| #188 | 11-11 07:14 | no (tests/docs/CI/tooling only) | RD-979: the shell-layout recorder header states the VENDOR counts its program prints, and a test keeps it true |
| #189 | 11-11 09:32 | YES (backend) | Learning log lines: write the learned query and description through logSafe (RD-798, alerts 152 and 153) |
| #190 | 11-11 12:03 | no (tests/docs/CI/tooling only) | CI: checkout and setup-node on their Node 24 majors, and Build asserts a Chromium-family browser before the verify gate (RD-605, RD-544) |
| #191 | 11-11 15:10 | no (tests/docs/CI/tooling only) | RD-407: the past-budget missing-settings tests keep the name missing for the whole call and count the retry waits instead of timing them (test only) |
| #192 | 11-11 17:25 | no (tests/docs/CI/tooling only) | Tooling: refactor-inline-styles.js skips a path under a file, and csp-convert.py ends a script block only on HTML end-tag whitespace (RD-970, RD-971) |
| #193 | 11-11 19:22 | no (tests/docs/CI/tooling only) | Tests: every rd412-smtp-route cell passes when run alone (RD-720) |
| #194 | 11-11 21:03 | no (tests/docs/CI/tooling only) | Tests: thirteen suites pass from a git-archive extract through one trackedFiles() helper (RD-731) |
| #195 | 11-11 23:25 | YES (backend) | RD-972 RD-976: a user update that changes access ends that user's sessions, and confirm-clarification reads the chat's context map |
| #196 | 11-12 03:30 | no (tests/docs/CI/tooling only) | RD-982: a nested jest run gets its own port band, and bootServer accepts a 200 only from its own child |
| #197 | 11-12 05:07 | YES (backend) | RD-929 RD-977 RD-978: the L1 permission design as a capability table over the route inventory, a plain sentinel word, and a handler scan that ends at the registration's close |
| #198 | 11-12 14:58 | YES (backend) | RD-969, RD-563: the two settings writes validate before they write and answer 400, and GET /api/models answers 200 |
| #199 | 11-12 21:39 | YES (backend) | RD-691: retire GET and POST /api/settings/agent, leaving the five stored values untouched |
| #200 | 11-15 09:17 | YES (backend) | RD-958 RD-964 RD-965 RD-966 RD-968: administrators only on the write and setup routes; the model switch loses its fixed password; the managed identity check stays inside Azure |
| #201 | 11-15 15:28 | YES (backend) | RD-932: every refused request writes an audit row, reads included, and a role change records its before and after |
| #202 | 11-15 17:44 | no (tests/docs/CI/tooling only) | RD-576, RD-590, RD-826: pin three test cells (an incomplete override reaches its own check, a stale label corrected, the withheld-link warning asserted) |
| #203 | 11-15 20:09 | YES (static) | RD-532, RD-538, RD-858: open-site banner above the loading overlay, banner guard edge cell, custom-SQL control removed from the Testing page |
| #204 | 11-16 01:15 | YES (backend) | RD-988, RD-926, RD-888: viewer re-triage refused, model answers logged on one line, Log Analytics risk run capped at 1,000 rows |
| #205 | 11-16 04:26 | YES (static) | RD-456, RD-492, RD-808, RD-475, RD-560, RD-481: first-run AI re-save keeps the AI setting, step 3 enforce shows success, endpoint slash stripped, sign-in icons digest, absolute asset paths |

(49 of 121 ship in the image.)

**Holds (file:line):**
- `NexusAI/1_Project_Definition/CLARIFICATIONS.md:2412`: "C-224. THE PRODUCT OWNER'S RULING (2026-10-26 20:23:37 AEDT, relayed by Tuesday): PR #120 lands with all three commits, RD-876 part 1 among them, and no NexusAI demo deploy goes out until RD-876 part 2 (the notice and the show-all button) lands." It is restated as "unchanged / stands" in 40+ later entries; last at `:2944` ("Related: ... [[C-224]] ... Recorded by the NexusAI records pass of 2026-11-15").
- `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:395`: "NexusAI main 27c0b71e: Deploy demo run 43151703534 SKIPPED, both jobs skipped (C-224 intact)." and `:23` "NOT deployed (C-224 demo hold, no word on deploy)".
- **Does 'c' lift it? No, not by itself.** C-224 is a specific ruling about specific missing behaviour (the notice and the show-all button); 'c' says "All Datasec projects' demos too" and names no ruling. Needs Kam's word (Q2). I have not found RD-876 part 2 landed.
- Authority otherwise: `NexusAI/CLAUDE.md:277` "a demo Container Apps deploy is now Tuesday-authorisable"; `:325` "deploy only on the coordinator's GO (Tuesday's) after the pass" (the testing-agent review before every deploy, `:315`).

**Deploy route** (S99O's, to be turned into a kit): identity pass (`az account show` must read tenant `d500ebad...`, sub `0c57ab37...`; project identity `nexusai-claude-deploy`); back up the share (`share-backup.sh` shape); `az acr build` the exact main sha into `nexusaidevacrfa39` with a `2.2.1-<seat>-<sha7>` tag; capture env names + secretRefs (22) before; swap by digest (`az containerapp update --container-name nexusai-api --image <digest>`); wait until only the new revision is active (RD-302: the old one stops serving only when it terminates, "verify after it terminates", CLAUDE.md:226); check health `OK`, the `build` equals `sha256(<new sha>)[:16]`, env names identical; Log Analytics read for sign-in / Entra-group failures (`group-watch.sh`).
**Rollback.** Swap back by digest to `nexusaidevacrfa39.azurecr.io/nexusai@sha256:c12c43e538f1274c1a7ba180f2cdfd595be63ec16eee0e45c690903734e08e4f` (the tag `2.2.1-s99o-17fc6c5` is present in the dev ACR, MEASURED; older anchor: `nexusaireleaseacr` tag `2.2.0`, MEASURED present). `swap-verify.sh` rolls back automatically on any failed check and verifies the old image is again the only active one. The share is not rolled back by an image swap; restore from the share backup only on a data problem.
**Live checks:** `GET /api/health` `status` OK/DEGRADED (DEGRADED allowed, must be visible), `/api/public/status` 200, `/js/index.js` 200 (the workflow's own smoke), `build` field = expected, 0 failures in Log Analytics since the new revision started, persistence sentinel not missing (`persistence.volumeWiped` false on health), env names/secretRefs equal, then a person's sign-in through Entra with the group check exercised (the S99O handover noted it was NEVER exercised: "0 failures over 0 sign-ins").
**NOT MEASURED for NexusAI:** Jira state of RD-876 part 2; whether sign-in is configured on the demo (decides whether #200/#204 403s bite); the 63 open code-scanning alerts' severities; the `scripts/` folder's presence in the image.

---

## 4. Security Composer

**Environment today.** The Composer **demo VM** (docker compose stack under `/opt/hpsm/composer`, API healthz on loopback; demo content ON, Basic auth at the edge). Sub `0c57ab37` / tenant #5 (MEASURED `az account show` under the Composer `.azure`; the kit's D1 expects `kreiser.org@me.com`). Public reads today (MEASURED 07:3x): `GET /site.json` 200 `{ "environment": "demo", "guided_view": false }`; `GET /healthz` 200 returns the web page (the API healthz is loopback only); `GET /api/v1/healthz` 404 problem JSON. **How deployed:** by a deploy seat over SSH to the VM, with a temporary key and NSG rule (B986 D2, D8), `git archive` of the target sha, `/opt/hpsm/remote-update.sh <archive> secrets/demo-switch.env` (migrations then compose build on the VM); the project `CLAUDE.md` says never from `Launch_Claude.command`. The GitHub repo has no deploy workflow and only the dynamic CodeQL and Dependabot workflows (MEASURED `actions/workflows`); CI is the local docker `scripts/ci.sh`; GitHub's 2 check-runs on main head are both CodeQL success.

**Deployed now.** `d70edf70fc43bb69737b2a242ba56480ce79f0d8` (RELAYED: `2026-10-31_B986_STATUS.md` last line `DEPLOYED: B986 demo @ d70edf70... | migrations 0023-0027 ... count 27 | contract 0.37.0 | backup composer-before-d70edf7-20261031T0636Z.dump | rollback kept 308b7aa (composer-308b7aa.tar.gz) | live check ok`). I looked for any later `DEPLOYED:`/`ROLLED BACK:` last line in `Briefs/*STATUS.md`: none after B986 (loop over all STATUS files; control: it prints B537 and B986). **Not measured live:** the demo's commit (the only read is `az vm run-command invoke`, a POST action I did not run; the public side exposes no sha). Partial live support: the served web bundle `index-B-n1v2_U.js` equals the bundle B986's evidence recorded (`live_checks.txt`) so no web change has been served since; contract version is 0.37.0 at both d70edf70 and main (`CONTRACT_VERSION` read at both refs, line 122), so a contract-version read cannot tell them apart.
**Main head** `b4681297d974ac3d8e74a4a12baeb9ea41962c52` (MEASURED). `compare d70edf70...main`: ahead, ahead_by 26, behind_by 0, 42 files; control: 26 merged PRs found (25 numbered #106-#130, plus #95 which merged 11-01 15:03 from an earlier branch); #105's squash is `d70edf70`. Open PRs: 1, #85 (draft "HOLD K6: L1 SM 3.16 content catalogue", not in range). Open code-scanning alerts 0.

**What rides along (26 PRs):**

| PR | merged AEDT | user-visible effect |
|---|---|---|
| #95 | 11-02 02:03 | Guided expert setup refuses a second target when the policy already holds one (API) |
| #106 | 10-31 18:52 | none (a test pins a late digest verdict) |
| #107 | 11-01 11:57 | none (date-rule test row) |
| #108 | 11-01 12:14 | none (deploy guide wording; the 0021 Route B check) |
| #109 | 11-02 00:53 | none (restore-script test rows) |
| #110 | 11-02 10:07 | none (engine performance test timing) |
| #111 | 11-02 12:50 | none (deploy guide command guard test) |
| #112 | 11-02 21:02 | none (guard tests) |
| #113 | 11-03 06:44 | **Change report footer: the first line is held to what fits above the hash line (one case still open)** (renderers) |
| #114 | 11-03 11:07 | none (deploy guide restore check) |
| #115 | 11-03 18:32 | none (deploy guide) |
| #116 | 11-03 22:36 | none (Route B check tests) |
| #117 | 11-03 23:47 | none (footer test row) |
| #118 | 11-04 07:16 | none (CI type-checks DB tests) |
| #119 | 11-10 07:24 | A typed discovery sub-answer is answered per device group (web) |
| #120 | 11-10 14:04 | **Change report footer laid out as the PDF writer does (the "three-dots" cut look): 63 of 265 changed first lines are 1 to 3 code points shorter than the longest sound prefix; 100 names cut shorter than at main** (BACKLOG.md:470 row #474) |
| #121 | 11-10 17:21 | none (deploy guide) |
| #122 | 11-11 15:07 | Secret fields supplied locally need no justification; new "Mark all secret fields local" action (web + API) |
| #123 | 11-11 16:26 | none for the demo (dev stack scripts: MinIO digest copies, objects volume recovery name) |
| #124 | 11-11 17:36 | Banner reads the singular for one marked field; deploy guide two-step way back for 0020/0024/0025 |
| #125 | 11-11 20:13 | The white is one named style value; the withdrawn list's setting key takes the code-style font (web styles) |
| #126 | 11-12 13:22 | Dev tooling only (vitest 5.0.5, vite 8.3.4) |
| #127 | 11-12 21:10 | Dev tooling only (minimatch override under eslint) |
| #128 | 11-13 13:59 | **Runtime dependency updates: undici, fast-uri, fastify, ip-address** (Dependabot alerts) |
| #129 | 11-15 13:16 | none (deploy guide: Route B lines of 0023, 0026, 0027) |
| #130 | 11-15 16:56 | The policy PDF cover's Date line is the brand profile's local day |

**Deploy-time flags.** Migrations: 0 changed files under `migrations/` or `rollback/` (42-file list printed whole; control: `apps/` has 21 hits). `content/` paths 0; `compose.yaml`, `docker/` 0; `scripts/up.sh`, `stack-diagnostics.sh`, `ci.sh` and two test scripts change (dev stack; whether the demo's `remote-update.sh` touches `up.sh` is NOT MEASURED). `package.json`/`package-lock.json` and `apps/web/package.json` change (#126, #127, #128): the VM build pulls new versions. `packages/api-contract` 0 paths. Not a content release; the held content release #85 is not in the range (control: it is the only open PR).
**Words gate.** B986 ran a NEW WORDS table (every added customer-facing string tested against a ruling). That must run again for #95, #113, #119, #120, #122, #124, #125, #130. **NOT MEASURED here.**

**Holds (file:line):**
- `Datasec Security Composer/CLAUDE.md:30`: "The live demo site is Kam's: click through it, never reconfigure it, never deploy to it without Kam's word."
- `Datasec Security Composer/1_Project_Definition/CLARIFICATIONS.md:2830` (and 16 earlier entries: :2548, :2568, :2588, :2604, :2620, :2636, :2652, :2668, :2684, :2700, :2716, :2748, :2765, :2782, :2798, :2813): "**Permits now:** ... a deploy only on the product owner's card." (:2668 adds "the two new words go to the words card first (C-95)").
- `0_Brain/tasks/EXPIRING-GRANTS.md:24`: "TUESDAY: push READY Datasec changes to the Composer demo + hosted HPSM-POC without a card ... merge-once-tested on EVERY Datasec project", from Kam 2026-10-16 ~11:4x "yes, the push to demo when ready applies to you now" (originally `:35`, 10-06 19:31 "Once it's ready, push to demo. Don't wait on my word."). B986 deployed under it. Its conditions: READY = QA gate + completion check + merged via CodeQL; "NOT: money, humans, a content release that makes engagements read-only".
- **The footer look, `Datasec Security Composer/BACKLOG.md:470`:** "The footer look after Composer PR #120: 63 of 265 changed first lines are 1 to 3 code points shorter than the longest sound prefix ... **OPEN, NOT RULED, awaiting the product owner**; row only, no ticket. A look-sized question, not a defect against the hash line." The look change itself was approved 11-10 13:33 ("Land the improved fix (labels always whole)"). A deploy ships the look he has not yet ruled on.
- `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:43`: the earlier round-cap card for the footer (`composer-pcomp23-footer-round-cap-1103`), which names "the three-dots footer".
- **Does 'c' lift it?** 'c' is Kam's word on the demos, which satisfies "Kam's word" (CLAUDE.md:30) and plausibly "the product owner's card" for the demo; it does NOT rule on the open footer-look row #474, and the words gate is separate. Needs Tuesday to state this reading to Kam with the list (Q3).

**Deploy route.** Template: `2026-10-31_B986_SEAT-D42_composer-demo-deploy-merged-main.md` (clone of B537/B147): Steps 0-3 touch no resource (gates on every PR, deployed-vs-target delta measured from the VM read, new-words gate), then the runbook: D1 identity (`kreiser.org@me.com`, tenant `d500ebad`, sub `0c57ab37`), D2 temporary SSH key + NSG rule, D3 before-state counts (read-only SQL inside `BEGIN READ ONLY; ... ROLLBACK;`), **D4 BACKUP FIRST (`pg_dump -Fc`, proven by a throwaway restore)**, D5 the way back written before the swap, D6 archive and `remote-update.sh`, D7 live check, D8 remove temp access and prove it, D9 cost. No migration this round, so the migrate step prints `migrations applied: none; already applied: 27`.
**Rollback.** B986's: Route A (down-recipes, newest first) is NOT needed with no migration; the way back is the previous build's archive (`/opt/hpsm/composer-d70edf7.tar.gz` will exist only if this deploy keeps it: B986 kept `308b7aa`'s) re-run through `remote-update.sh`; Route B (restore the dump) is the fallback and "loses everything written since". Rollback is Tuesday's call. **Live checks (B986 D7):** `composer` tree = target by per-file manifest; `composer.prev` = `d70edf70`; healthz contract `0.37.0`; markers per change counted in the dist; ledger count 27 and the 5 checksums unchanged; row counts equal; objects container id unchanged; all services healthy, 0 API >= 500; `kam` 200 and the second account 200, wrong password 401; read-only real-browser walk at 1280x800 and 390x844 with 0 console errors and no non-GET; the PDF cover Date and the footer on a generated sample (new this round).
**NOT MEASURED for Composer:** the deployed sha by any instrument; the words status of the customer-visible PRs; whether `remote-update.sh` uses `scripts/up.sh`; free space on the VM for a backup (needs the VM read).

---

## 5. What I touched (for Tuesday's audit)

- `gh api -X GET` only, four repos, each under its own project config. `gh auth status` was run once under the HPSM config (it prints a masked token prefix; nothing was copied anywhere).
- `az`: `account show` (x4, one per project config); HPSM: `group list`, `group exists`, `resource list -g hpsm-poc-uat-rg|hpsm-poc-rg|hpsm-poc-demo-rg`; MPS: one `az rest --method get` on the site's ARM id (not `az webapp show`); NexusAI: `containerapp show` (selected fields only), `containerapp revision list`, `acr repository show-manifests`, `acr repository show-tags` x2; Composer: `account show` only.
- `curl` GETs listed at the top. Raw responses are in the scratch directory (`hp_probe.out`, `nx_health.json`, `mps_root.html`, `pc_probe.out`); none holds a secret.
- Files written: this file, and scratch files under `fleet/state/s281/deploy-census/` (PR lists `*_prs_*.tsv`, PR bodies `*bodies/`, `nx_deploy-demo.yml`, `mps_deploy-from-ci.sh`, `pc_DEPLOY.md`, `build_doc.py`).
- One background shell (a `grep -rl` over the briefs folder) overran the tool's 120 s timeout and was moved to the background; it only reads.

---

## 6. For Kam (plain words, no shas, no ticket numbers)

What would go out to the demo copies, if you say go:

- **HPSM-POC: nothing, unless you say otherwise.** The demo copy was deleted on 5 November to save money. The only hosted copy left is the review site HP looks at, and you told me to keep my hands off it while HP reviews. If you want it updated anyway, it carries nine changes (a four-choice industry list, reworded and reordered questions, a contents page in the PDF, editable approved narratives, the HP reviewer's alias view), plus a database change, a permissions script, and a setting that has to move with it. That is a bigger operation than the earlier updates, so it needs your word and a quiet window.
- **MPS Calculator: eight small changes**, mostly behind the scenes (safer deploy scripts, a security library update), plus two things people will see: the rental price screen shows "Software / month" once, and fleet lines keep a stable number. It needs your go for this specific copy, and the wording of the new deploy stop messages still waits on you. One catch: if we ever have to roll it back, quotes saved after the update may stop loading; we would roll forward instead.
- **NexusAI: a lot, 121 changes since 16 October**, about 49 of them in the running software: sign-in and role limits (viewers can no longer change settings, an audit trail of refused requests), safer risk-condition handling, a 1,000-row cap on risk queries, page fixes, the assistant's name look-ups, and library updates. **Your earlier rule still blocks it: no demo update until the notice and "show all" button for the 1,000-row cap are built, and that has not been built.** Also, viewers will see "admin only" refusals on some pages until the screen work catches up. And the automatic route for updating this demo is switched off, so a person-run swap is needed.
- **Security Composer: 26 changes**, no database change: footer and cover-date fixes in the PDFs, the "mark all secret fields local" button, per-device-group discovery answers, a library security update. Its own rule says a deploy waits for your card, and the footer look (the cut-short names) is still waiting for your ruling. Your "all demos" word may be enough; tell me if you want me to read it that way.

What I need from you: (1) is HPSM out of this round, or do you want the HP review site updated; (2) can NexusAI go out without the "show all" button; (3) is "all demos" your card for Composer and MPS, and do you approve the MPS stop-message wording.

---

DRAFTED DEPLOY-CENSUS: 4/4, questions 8
