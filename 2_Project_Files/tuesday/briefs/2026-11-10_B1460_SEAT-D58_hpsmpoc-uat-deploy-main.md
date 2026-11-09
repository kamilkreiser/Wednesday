From Tuesday (the product owner's Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail channel from this project). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`.
# BRIEF B1460 - SEAT-D58: HPSM-POC: deploy main at `TARGET` (slot S4: today's five landed lanes #298-#302 plus the step-10-reword and readiness-hub PR) to the hosted UAT review copy ONLY, as a DELTA on what UAT runs now: the web package AND the API package (THIS RANGE HAS API CODE) by the project script; NO schema step, no what-if, no template, no app-setting write, no demo-data reset; then a READ-ONLY census of UAT's own feedback store

In this brief **`TARGET`** = `6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb` (slot S4; **`T8`** = its first 8 hex), the squash of the step-10-reword and readiness-hub PR (slot S12 names its number) on top of main `0820efe9ff08d32bc0d4710643081abb268f4725`. **`PREV`** = what UAT web AND API run now = `884fd72b238ec8dc0d566b0e9c18b5362f920a2b` (**`PREV8`** = `884fd72b`). This is **RELAYED, NOT MEASURED NOW**, from the LAST line of `Briefs/2026-11-10_B1454_STATUS.md` (`DEPLOYED B1454: 884fd72b238ec8dc0d566b0e9c18b5362f920a2b <the UAT web address>`, printed by the drafter with `tail -n 1` at 09:28) and its FOR TUESDAY 1 and PART P. **What B1454 recorded:**
- Deployed 05:31:39-05:33:45 AEDT 2026-11-10 (2026-11-09T18:31:39Z-18:33:45Z) by `scripts/deploy-from-ci.sh`.
- Active deployments: web `9212fb0b-4878-46be-9d53-d7cb108d8742`, API `802ab059-93d3-4e73-a41c-fdd75ccca6e2`. Web `.next/BUILD_ID` `bytHj28aj21cVQmgGGcmh`. CI run `42659375588`.
- Packages: web `279f184a64a0b4253a832020bf2f261993186f86ea61a8b741088ed4ac445548` (16,542,627 B, 2115 files), API `7741578de7653c3c68b89916b2df8e0b53eeac368aba0fdc0345b3986cbb3303` (49,630,884 B, 122 files). Live-check AFTER: web 2115/2115, API 122/122, site-only 0.
- PART P PASSED. Watchdog `WINDOWS PASSED t+921`. No rollback.
- New containers: web `18:32:24.6135103Z Site started.`, API `18:33:20.9202919Z Site started.`, on images `appsvc/node:24-lts_20261027.8` and `appsvc/dotnetcore:10.0_20261027.8`.

**Whether UAT still runs `PREV` is UNMEASURED by the drafter** (no `az`, no HTTP to any hosted host). The instruments are REFUSE 2 and PRE-DEPLOY SIGNAL 3. **If UAT is not on `PREV` (a different BUILD_ID or active deployment id): STOP, because someone else deployed.** The deploy-STATUS listing (`/usr/bin/grep -l -E '^(DEPLOYED|ROLLED BACK|PARTIAL)' 'Briefs/'*STATUS.md | tail -3`) at 09:28 listed, newest last, B1307, B1391, B1454.

**Drafter's own measurements (MEASURED, read-only).** All by `gh api -X GET` under the project `GH_CONFIG_DIR`, with clocks from `date` in the same command, 09:21-09:28 AEDT 2026-11-10. **They cover `PREV...0820efe9` only; the seat re-measures the full range at `TARGET`.**
- `branches/main` = `0820efe9ff08d32bc0d4710643081abb268f4725` (09:21:11).
- `compare 884fd72b...0820efe9`: status ahead, ahead 5, behind 0, **5 commits, 18 files, +720/-48**:

| Commit | Parent | PR | PR head | Subject |
|---|---|---|---|---|
| `192c0a94` | `884fd72b` | #298 | `d7df877a` | "Web sign-in: parallel calls of one session share one token renewal" |
| `90d30d5f` | | #299 | `aca2290c` | "Demo Walkthrough: step 10 note names both waits of the laptop report screen" |
| `7d4e3142` | | #301 | `0cdfc74e` | "Tests: held-name boundary rows, CI reader line-break guard, e2e load waits" |
| `856d15d1` | | #302 | `c0a5fa17` | "Narratives: refuse a finding explanation of no visible finding before anything is stored or sent" |
| `0820efe9` | | #300 | `b18457c2` | "Web: one row spacing in Recent activity; mock lists customer text problems in one 400" |

- **CI at `0820efe9`:** push run `ci` `42689075848` completed/success. Every job passed (`api (ASP.NET Core)`, the three `api on SQL Server` legs, `web build (...)`, `web unit tests (vitest)`, `web (Next.js)`, `infra (Bicep validate)`, `secrets (gitleaks, full history)`, 8 `web e2e` shards) except `dependency review`, which was skipped (pull requests only). `Push on main` (CodeQL) `42689076911` completed/success. Open code-scanning alerts on main: **0** (control: state `fixed` reads 1). Artifacts `deploy-web-0820efe9...` (16,544,562 B) and `deploy-api-0820efe9...` (49,698,221 B) read `expired=false` and expire 2026-11-16.
- **Tree proof** (recursive trees of `0820efe9` and `884fd72b` plus the five PR heads, blobs only, python3 -I -B):
  - the union of the five PRs' `pulls/N/files` = the range's 18 paths exactly, with 0 paths shared between PRs;
  - the blob at `0820efe9` equals the blob at that PR's head for 3/3, 2/2, 5/5, 5/5 and 3/3 paths;
  - blob paths differing outside the union: **0** (control: a planted path reads 1);
  - check-runs on each head: 23 of 23 success;
  - schema regex `Migrations|Persistence|\.sql$` over the differing blobs: **0**;
  - `scripts/deploy-from-ci.sh` blob `0024302d1ea3` and `scripts/deploy-package.py` blob `77dc49939859` are EQUAL at `PREV` and `0820efe9`;
  - `deploy-from-ci.sh` at `0820efe9` is 109 lines: `:49` the green-run predicate, `:68`/`:69` the two `az webapp deploy ... --type zip --async false --clean true` lines (`/usr/bin/grep -n -i -E 'webapp deploy|--status success'`; control: the header comments `:10` and `:18` also hit).
- **Gate lines** (first lines of `Briefs/2026-11-10_B14{50,51,52,53,55}_STATUS.md`, printed by `head -n 1`):
  - #298: B1450 `GO WITH FINDINGS @ d7df877` (round 1 of 2);
  - #300: B1451 `GO WITH FINDINGS @ 121ee23`. The head moved ONE commit to `b18457c2`, 1 path `web/src/server/mock/customer-shape.test.ts` ("write the two right-to-left overrides as escapes"; MEASURED `compare 121ee23...b18457c2`: ahead 1, 1 file);
  - #299: B1452 `GO WITH FINDINGS @ aca2290`;
  - #301: B1453 `GO WITH FINDINGS @ 0cdfc74`;
  - #302: B1455 `GO WITH FINDINGS @ c0a5fa1`.
  - Graded Majors in those five: 0. B1452-1 names "what would flip it to a Major"; it stays Minor because UAT's sample is at report-issued (B1454 measured).
- **The pending PR** (MEASURED 09:23, UNSTABLE: it is still building): `refs/heads/b1392/hpsmpoc-caveat-reword` = `9302bc0dd94b8cec4c0dec1270abee28c969eae6`. `compare 0820efe9...9302bc0d`: ahead 2, 7 paths, all under `web/`: `e2e/playbook-event-states.spec.ts`, `e2e/playbook.ts`, `src/app/(app)/assessments/page.tsx`, `src/components/readiness/AssessmentsHub.myreadiness.test.tsx`, `src/components/readiness/AssessmentsHub.tsx`, `src/content/walkthrough/steps.test.ts`, `src/content/walkthrough/steps.ts`. Open PRs: 0 at 09:23.
- Ports 9970-9979: `lsof` LISTEN **0** at 09:25:07 (control: all listeners 17).

**The 18 paths of `PREV...0820efe9` (MEASURED, `compare`; m = modified, a = added):**

| Path | +/- | Kind |
|---|---|---|
| `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs` | m +6/-0 | **API PRODUCT CODE** |
| `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs` | m +69/-0 | test |
| `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc436NoFindingExplanationTests.cs` | a +83/-0 | test |
| `api/tests/HpsmPoc.Api.Tests/Contract/ContractTests.cs` | m +1/-1 | test |
| `infra/tests/test_ci_workflow.py` | m +80/-7 | **infra TEST only** |
| `web/e2e/html-layout.spec.ts` | m +6/-2 | test |
| `web/e2e/logon-logo-link.spec.ts` | m +2/-0 | test |
| `web/src/components/customer/EngagementOverview.tsx` | m +16/-3 | product |
| `web/src/components/customer/residualLinks.targets.test.tsx` | m +57/-4 | test |
| `web/src/content/walkthrough/steps.test.ts` | m +10/-0 | test |
| `web/src/content/walkthrough/steps.ts` | m +1/-1 | product |
| `web/src/lib/dates.test.ts` | m +3/-1 | test |
| `web/src/server/auth/entra.ts` | m +63/-19 | product; Entra mode only |
| `web/src/server/auth/refresh-fanout.test.ts` | a +153/-0 | test |
| `web/src/server/mock/api.ts` | m +4/-4 | product; mock mode only |
| `web/src/server/mock/customer-detail.ts` | m +24/-6 | product; mock mode only |
| `web/src/server/mock/customer-name.test.ts` | m +52/-0 | test |
| `web/src/server/mock/customer-shape.test.ts` | a +90/-0 | test |

**Product (non-test) paths: 6**; test paths 12. **Not in the range: any `.github/`, `scripts/`, `package*.json`, `*.csproj` or `appsettings` path. Not in the range: any migration. Added lines of the 6 product paths that read a configuration key (`process.env.`/`process.env[`, `Configuration[`, `GetValue<`, `GetEnvironmentVariable(`): 0** (control: a planted line reads 1). Added lines with a hidden or text-direction character: 0 (control: a plant reads 1).

**Fact marks.**
- MEASURED: this drafter at drafting, read-only (`gh api -X GET`, `ls`, `lsof`, `tmux list-panes`, `/usr/bin/grep`, `awk`, `sed -n`, `tail`, `head`, `shasum`, `stat`, python3 -I -B over downloaded JSON and raw files).
- RELAYED: quoted from a named file.
- UNMEASURED: nobody ran it.
- **Source beats this brief: re-measure at source, and say in STATUS (Corrections) where they disagree.**

**WHAT THIS KIT IS (read first).**
1. **Six product changes, three of them visible on UAT.**
   - **(C) Step 10 caveat** (#299, then reworded again by the pending PR): the presenter note in the Demo Walkthrough panel at step 10.
   - **(R) Readiness hub** (the pending PR only): on `/assessments` the H1 and the tab read "Playbook Partner Readiness", and the hub LEADS with the CURRENT statements when the newest completed run is on an older content version. The sidebar label stays "My readiness". Background, RELAYED from `tuesday/briefs/2026-11-10_readiness_investigation/FINDINGS.md`: B1391 had recorded "the 16 new statements are NOT SHOWN ON UAT", but that line never reached the product owner. **This seat reports what it SEES on the page (heading text, first panel title, statement count). "Deployed" is not "visible".**
   - **(A) Recent activity spacing** (#300): on a customer's overview page, layout only, no new words.
   - **Not visible on UAT:**
     - **(N) The API refuses a finding explanation of no visible finding** (#302: `ReportingEndpoints.cs` +6). This is the API's only product change. UAT's web never sends that request (drafter: a GitHub code search for the kind `finding-explanation` hits only `web/src/api/schema.gen.ts` in `web/`).
     - **(E) Shared token renewal in Entra mode** (#298, `entra.ts`). UAT runs the open UAT sign-in, not Entra.
     - **(M) The mock's one-list 400** (#300, `server/mock/*`). UAT uses the real API, not the mock.
2. **THIS IS NOT A WEB-ONLY DELTA. The API package carries code.** B1454's API proof was "stamp-only 5 of 5". Here the property is: **`HpsmPoc.Modules.Assessment.dll` (the assembly holding `Endpoints/ReportingEndpoints.cs`) carries code differences; the other 4 `HpsmPoc*.dll` are stamp-only; every non-DLL/PDB file is EQUAL.** Any code difference in another DLL, or any changed non-DLL file, means an `api/` change nobody listed: STOP (BUILD 4). The behaviour is proven on the local pair (BUILD 7 (iii)) and by CI's test results (BUILD 3). **It is never exercised on UAT**: a narrative request is a write.
3. **`infra/` is in the range, but only as a test file** (`infra/tests/test_ci_workflow.py`). Nothing under `infra/` is deployed by this seat: no template, no what-if, no Bicep. The seat proves that every `infra/` path in `PREV...TARGET` sits under `infra/tests/`. Any other `infra/` path = STOP.
4. **No migration.** The schema regex over the range reads 0 at `0820efe9`. The seat re-measures it at `TARGET` and proves that `TARGET`'s `assessment.sql` and `feedback.sql` digests equal `PREV`'s (BUILD 3).
5. **Authority (RELAYED by Tuesday; the drafter did not read the board or the terminal).** The product owner, live board 2026-11-10 09:06, verbatim: **"also, please check all feedback items and deploy"**. In the Tuesday terminal, about 09:09, verbatim: **"don't wait, deploy as soon as it's ready"**. **UAT ONLY. Never production, never the demo.** "Ready" = the step-10-reword and readiness-hub PR landed on main through its gate and CodeQL, with CI green at `TARGET` (slots S4, S5, S6). "Check all feedback items" = PART F below (READ-ONLY). **This lifts the UAT hold (ruled 2026-11-06) for THIS deploy ONLY** (slot S13); the hold stands for everything else. A correction arrives as `B1460_ADDENDUM-*.md` in `tuesday/briefs/`. Read each one whole before the first `az` call and again before the deploy START. One that changes the site or the sha is a STOP until Tuesday restamps.
6. **Template and what carries over.** The kit that deployed cleanly this morning is `tuesday/briefs/2026-11-10_B1454_SEAT-D57_hpsmpoc-uat-deploy-walkthrough.md`; read it WHOLE. Its record is `Briefs/2026-11-10_B1454_STATUS.md` (387 lines at drafting); read it WHOLE: the programs, the way-back script, the identity pass, the local pair, PART P, Corrections 1-6, FOR TUESDAY. **Inherited unchanged unless this kit says otherwise:**
   - the identity pass before EVERY `az` call;
   - plain ARM GETs, never `az webapp show`;
   - clock checkpoints;
   - D-5, D-6, D-9;
   - the PRE-DEPLOY SIGNALS and the settings-hash compare;
   - the STATUS-first-line discipline;
   - the no-schema proof;
   - no message to any human;
   - B1391's restamp 4b (no load gate on the local pair).
   
   **B1454's fixes are carried by copying B1454's FIXED instruments, not B1391's:** the `lits` output redacts the server-action `encryptionKey` (B1454 Corrections 2); the walker reads "Step n of 14" with `textContent`; `webpair` pins the seed owner from the seeded database; status and lists are read by in-page GETs (B1454 Corrections 3, FOR TUESDAY 5 (b)/(c)).
7. **WHERE THE INSTRUMENTS ARE (MEASURED by `ls` at 09:28).**
   - `.tools/b1454/` holds D57's working set: `identity_pass1454.sh`, `presig1454.py`, `live1454.py`, `pkgcmp1454.py`, `words1454.py`, `lits1454.cjs`, `walk1454.cjs`, `cmpwalk1454.py`, `pairseed1454.py`, `webpair1454.py`, `deploy1454.sh`, `rollback1454uat.sh` (sha256 `f52193f753990c256aea1731a7b69cd7853fc000eb5a40b26a0bd8d4cdb6dc9a`, MEASURED), `statusnow.py`, `stub/`, plus `repo` (HEAD = `PREV`), `repo-rb` (HEAD = `fa401da9`) and `target/`.
   - `target/` holds `PREV`'s two verified packages, MEASURED by `shasum -a 256` and `stat` at 09:28: web.zip `279f184a...` 16,542,627 B; api.zip `7741578d...` 49,630,884 B; `assessment.sql` `8a4084b696aad699e2c3f405f0f6f3188bfdff451a6a1f725f369b1d478e220c`; `feedback.sql` `2a587ac2824755f12d3e03f0dde768d3414e89e91c9ad85ac2b4f612b135d3c3`; both `MANIFEST.json` `commit` = `PREV`; `RUN` = `42659375588`.
   - `.tools/b1460/` is ABSENT (MEASURED: `ls -d` fails).
   - **The seat COPIES what it needs by name into `.tools/b1460/`** (read-only source; `cmp` each copy), renames each to a `1460` name, hand-edits every hex, sha, BUILD_ID and count map (never by `sed`; STANDING 7), and runs each copy's plant control before relying on it. It never writes into `.tools/b1454/`, never runs a program in place there, and never moves anything there.

**What the product owner approved, and what is NOT covered.**
- **Covered:** the CI packages of `TARGET` to the two UAT apps by the project script; read-only checks; the way back; PART F's read-only listing of the UAT feedback store.
- **NOT covered** (each is `[PROD-CLASS]` or a data/permission write):
  - `[PROD-CLASS]` any database write, schema step, or `.sql` file run;
  - `[PROD-CLASS]` any hosted-data reset, re-seed or demo-data change;
  - `[PROD-CLASS]` any app-setting, vault, plan, firewall or access write;
  - `[PROD-CLASS]` a template deploy or what-if;
  - any new paid resource;
  - any `az` call to any other group;
  - **any feedback item created, approved, deleted, or moved to another state (PART F is GET only)**;
  - any narrative generated on UAT;
  - any readiness self-assessment started on UAT;
  - anything after `TARGET`;
  - anything to HP or to any human.
- UAT is the site HP reviewers open, so every write to it is production-class. The script's two `az webapp deploy` lines are the ONLY ones.

**Closed-list proof of what reaches UAT** (re-measured by the seat at Step 0; property first, then "at least these", then "any other shape: prove it meets the property or STOP").
- *Property:*
  - every commit in `PREV...TARGET` is on main, merged by a pull request the seat prints with its number, head, and gate verdict line;
  - every path is either a test path (`/tests/`, `/e2e/`, `*.test.*`, `*.spec.*`) or one of the product paths of the slot-S6 PR rows;
  - every `api/` product path is under `api/src/HpsmPoc.Modules.Assessment/` (so only `HpsmPoc.Modules.Assessment.dll` may carry code);
  - every `infra/` path is under `infra/tests/`;
  - no path matches `Migrations|Persistence|\.sql$`;
  - no `.github/`, `scripts/`, `package*.json`, `*.csproj` or `appsettings*` path;
  - no added line of a product path reads a configuration key that `PREV` does not already read (list every NEW key; each is checked against the UAT setting NAMES, API 35 / web 17; a new required key = STOP);
  - `scripts/deploy-from-ci.sh` and `scripts/deploy-package.py` blobs are equal at `PREV` and `TARGET`;
  - for every path, the blob at `TARGET` equals its blob at the head of the PR that changed it (no path is shared between PRs; if one is, its blob equals the LATER PR's head), with 0 blob paths differing between `PREV` and `TARGET` outside the union of the PRs' files.
- *At least these:* the 5 commits and 18 paths above (#298-#302), plus the pending PR's squash (slot S12) and its paths (7 `web/` paths at its head `9302bc0d` at drafting, RELAYED from the drafter's 09:23 compare; the seat re-measures at the landed head).
- Controls:
  - the schema regex over `compare a3a06b9a...69338b64` (a range with a `.sql` path, as B1454 used) reads >= 1 (B1454 read 11);
  - a planted extra path reads 1 differing;
  - a planted `api/src/HpsmPoc.Api/x.cs` path fails the "only Modules.Assessment" rule.
- **Any other shape** (a 7th commit, an `api/` path in another project, an `infra/` path outside `tests/`, a blob that is not the head's): prove it meets the property or STOP and list it.

**CI at `TARGET`.** The pass predicate is the script's (`scripts/deploy-from-ci.sh:49`, printed by the seat with `grep -n -i`; `:50` stops when none). Requirements:
- The push run `ci` of `TARGET` (slot S5) is `completed/success`, with:
  - `api (ASP.NET Core)` success;
  - ALL THREE `api on SQL Server` legs success (a skipped leg = STOP: this range changes API code);
  - `infra (Bicep validate)` success (it runs the repo-wide hidden-character and workflow-reader tests, DRAFTER_RULES 8);
  - every web-e2e shard job success (read the CURRENT job names from the run).
- `Push on main` (CodeQL) success.
- Open code-scanning alerts on main: 0 (control: state `fixed` >= 1).
- **The API change's own tests ran and passed:** download the run's `api-test-results` artifact (GET) and count the test cases whose name contains `Hpsmpoc436` with outcome Passed: >= 1, Failed 0 (control: a no-such test-name token counts 0, and the total of passed tests is > 100).
- Never re-run CI; never dismiss an alert.
- Artifacts `deploy-web-<TARGET>` and `deploy-api-<TARGET>` read `expired=false`.

**Identity and tenant (workspace rule 4; records, not assumed).** RELAYED from `B1454_STATUS.md` REFUSE 7 (and C-07 of `CLARIFICATIONS.md`):
- subscription "Azure subscription 1" `a6b8fe11-d1b5-4293-8727-b34aba08a705`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, user masked `...@datasec-rd.com`;
- the project's own interactive `az` login: `AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.azure'`; `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config'`;
- which of the five Datasec environments this tenant is: NOT ASSERTED.

Rules:
- **`identity_pass1460.sh` (a copy of `identity_pass1454.sh`, `cmp` first) runs before EVERY `az` call** (the four comparisons; control: `AZURE_CONFIG_DIR=/nonexistent` fails rc 2).
- `4_Credentials/.azure-sp` is never opened. An expired interactive login = STOP and ask.
- Any mismatch or authorization error is the boundary working: STOP and report it. Never `az account set`, never work around it, never ask for a broader right.
- **Never `az webapp show`** (Azure CLI 2.90.0 fetches the publish profile with secrets on each call). Every site read is a plain ARM GET (`az rest --method get` on the site's resource id), as `presig1454.py` did. The project script's own `az webapp deploy` lines and live-check reads are the exceptions.

**CLOCK.** Hard stop = Step 0 + 120 minutes (slot S3), written by you as an absolute AEDT clock at Step 0. No write START after it (the deploy counts). DONE no later than Step 0 + 150 minutes. Step 0 within 45 minutes of slot S1.
- CHECKPOINT lines with `date`, in this order: Step 0 | CI green | package checks | rollback point taken | local pair | DATABASE STILL AWAKE (before) | UAT BEFORE walk | UAT deploy START | PART P PASSED | DATABASE STILL AWAKE (after) | PART F DONE | DONE. At every CHECKPOINT print the minutes left to the write cut-off.
- A write that has started is not killed. A way back that must start, starts within 60 s.
- PART F is read-only and may run after the write cut-off, but not after DONE's limit.
- **If anything is in doubt, leave UAT as it is, do nothing more, and end `STOPPED: NEEDS TUESDAY <reason>`.**

**Model route.** Opus: `fleet/specs/model-routing.md` row C6 "Deploy" at `:96` ("**1st**" in the Opus column) and `:145` ("Sonnet as coordinator, as deploy seat, or as tier-1 gate: no rows"), both MEASURED by the drafter with `grep -n -i deploy` at 09:25. `BRIEF_SEAT_LEVEL=opus`. Model id `claude-opus-5-5` (`0_Brain/dashboard/data/models_latest.json`, `levels.opus.model_id`, MEASURED at drafting). STATUS quotes the `brief_seat: model=` line or says none was shown. **Never run /model in this pane.**

**Landing (Tuesday's).** Every PR in the range landed, or lands, as a squash through CodeQL (the Datasec org ruleset; never bypass, never dismiss an alert). MEASURED: main has squash merges only (`0820efe9`'s five commits each have one parent and one PR). This seat lands nothing and opens no PR.

**This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only.** UAT feedback delivery is OFF (`Feedback__Route` `off`; re-read at Step 0). This seat sends and approves nothing.

**Carried from B1454 (its Corrections and FOR TUESDAY 5):**
- (a) No `cd` and no `rm`, ever. Quarantine by move. No `/tmp`.
- (b) PRIOR WORK is read WHOLE before the first `az` call.
- (c) The deploy-STATUS control is a scratch file ending `DEPLOY B1460: PENDING`, which counts 0 for `^DEPLOYED `.
- (d) Slot S10's label contains "CONFIRMED / NOT CONFIRMED": count `NOT CONFIRMED` over the VALUE part only.
- (e) Zip deploys write no ARM deployment or restart rows, only `publishxml/action` reads (B1454 counted 4).
- (f) **Until PART F, the walk guard ABORTS GET prefetches of `/admin/feedback` and `/admin/feedback/review` and counts them** (B1454 aborted 24 BEFORE and 26 AFTER per walk). PART F is the ONLY place those two pages are loaded.
- (g) The `/customers` instrument counts 4/5/5/4. Compare BEFORE vs AFTER with the SAME instrument.
- (h) The loopback refused probes read 401 `signin-required`, so measure the refusals on UAT.
- (i) **A secret-shaped value never reaches a log, STATUS or the session output** (B1454 Corrections 2: its first `lits` run printed the Next server-reference `encryptionKey`). Copy `lits1454.cjs`, which redacts the field, and re-run its redaction check (0 key-shaped strings in its logs; control: an unredacted copy of a manifest line reads 1).
- (j) A timing-only local failure is re-run once and both results are written (restamp 4b).
- (k) Main may move during the run (B1454 saw it move once): D-1.

## DRAFTER DECISIONS (D-n; Tuesday accepts or changes them at the stamp; the defaults apply if Tuesday is silent)
- **D-1: PIN `TARGET`, not "main".** If main moves past `TARGET`, deploy `TARGET` anyway and record it. Never a later commit; never an unmerged branch. The seat REFUSES unless `gh api -X GET branches/main` equals slot S4 at Step 0 AND the Closed-list proof holds, OR main is a later commit whose ancestry contains `TARGET` (then record it and deploy `TARGET`). **Slot S4 not 40-hex, or `TARGET` not a descendant of `0820efe9ff08d32bc0d4710643081abb268f4725`: STOP at once.**
- **D-2: ONE write class: the two `az webapp deploy` lines of the project script** (`deploy-from-ci.sh:68-69`, printed by `grep -n -i`: the web zip, then the API zip, `--type zip --async false --clean true`). `[PROD-CLASS]` No what-if, no `az deployment`, no `az sql ...` write, no app-setting, vault, plan, firewall or access write, no `sqlcmd`.
- **D-3: Both packages, through the project script** (web, then API; there is no web-only mode). The API restarts with NEW code in `HpsmPoc.Modules.Assessment.dll` (the HPSMPOC-436 refusal). This is accepted under the product owner's "deploy" ruling. Whether an HP reviewer is in session now is UNMEASURED; Tuesday states it in slot S10 (d).
- **D-4: No temporary access of any kind.** The SQL firewall is exactly `AllowAllWindowsAzureIps` before and after.
- **D-5: THE DATABASE STAYS AWAKE** (read-only, before the deploy and after PART P). RELAYED baseline, B1454 "D-5 after", 05:47 AEDT: `status` Online, `autoPauseDelay` -1, `useFreeLimit` False, `pausedDate` None, `GP_S_Gen5` capacity 2, `minCapacity` 0.5, `maxSizeBytes` 34359738368; `databases/pause` since 2026-11-01T00:52:35Z **0** (control window 2026-11-01T00:24:13-00:52:00Z: 2). Any difference: list it, and STOP before the next write.
- **D-6: Platform-image rule, both UAT apps** (baseline = the Step 0 reading). RELAYED baseline: web `NODE|24-lts` / `node server.js`; API `DOTNETCORE|10.0` / empty command line; images `node:24-lts_20261027.8`, `dotnetcore:10.0_20261027.8`; active deployments `9212fb0b-...` (web) and `802ab059-...` (API).
  - **Record and continue (platform state):** an unchanged or newer image of the SAME stack and major, with no activity-log action, the same deployment ids, settings and trees equal, and the site healthy.
  - **Still a STOP:** a different stack or major; a `linuxFxVersion` or `appCommandLine` change; any activity-log write; a different active deployment id; any setting or tree difference.
- **D-7: The way back (code only) = `PREV` = `884fd72b`.** `rollback1460uat.sh` (BUILD 5) puts `PREV`'s two packages back on the two UAT apps with `--clean true`, then runs the live-check and checks for live `BUILD_ID` `bytHj28aj21cVQmgGGcmh`. There is no schema step, so nothing to undo there. The database needs no undo either: `PREV`'s API reads the same schema (the `.sql` digests are equal, BUILD 3). A rollback ends the run (D-9). After a rollback the `884fd72b` site returns: the walkthrough with the B1390-1 caveat, the readiness hub as "My readiness".
- **D-8: THE WORDS GATE (a closed list by STRING; the product owner reads the words before UAT).**
  - *Property:* every customer-facing string that is new or changed on UAT is one of:
    - (i) the strings listed in `tuesday/briefs/2026-11-10_B1460_WORDS-FOR-KAM.md` (as Tuesday amends it), or
    - (ii) the pending PR's strings that Tuesday lists in slot S14.
    
    Each must be at the `file:line` written there, re-printed at `TARGET`.
  - **At least these (MEASURED by the drafter's extractor over `PREV...0820efe9`, plant 1 of 1, comment-plant 0):**
    - `web/src/content/walkthrough/steps.ts:130`: the step 10 caveat, CHANGED. At `0820efe9` it reads: "...On the laptop sample this screen shows "No report yet" until the assessment is completed and scored, and then waits for the approved narrative: score the assessment and approve the narrative before you show it, and do not promise either wait for every customer." **The pending PR changes this line again**: at its 09:23 head it drops the score-and-approve instruction. The seat re-extracts at `TARGET` and compares with S14.
    - `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs:187`: NEW API reply "There is no visible finding to explain." (code `narrative.no-findings`).
    - `web/src/server/mock/customer-detail.ts:74` "name takes 1 to 120 characters." and `:76` "industry takes at most 80 characters." These are NEW in the mock (mock mode only, not on UAT) and equal to the API's existing words at `Requests.cs:141`/`:149`.
    - `customer-detail.ts:59`/`:77` "The request is malformed" and `:63` (the hidden-character message): moved, with the same words.
    - `EngagementOverview.tsx`: no new words (class names and element ids only).
    - `entra.ts:335`/`:373`: two `[auth]` server-log lines, moved with the same words (not customer-facing).
    - The pending PR at 09:23 adds, RELAYED and UNSTABLE, for Tuesday's S14:
      - `AssessmentsHub.tsx:87` `${READINESS_TITLE}: current statements`;
      - `:88` "A new self-assessment asks these ${n} statements in ${m} areas. Your latest completed self-assessment used an earlier set of statements; its results are in the list below.";
      - `:99` "Start a self-assessment" (moved);
      - `:131` the header: title `READINESS_TITLE` (= "Playbook Partner Readiness", `web/src/content/readiness.ts:11`), eyebrow "My readiness", and the lead text unchanged;
      - `assessments/page.tsx` tab title `READINESS_TITLE` (the root layout template appends " · HP Security Services Playbook", `web/src/app/layout.tsx:7` at the pending head `9302bc0d`).
  - **Any new customer-facing string not in (i) or (ii) is a STOP before any hosted write** (list it with its `file:line`).
  - **Instrument:** `words1460.py` = a copy of `words1454.py`, with its closed list REPLACED by (i)+(ii). It runs over the ADDED and REMOVED lines of every product path of `PREV...TARGET`, normalised as B1454 did; comments are skipped across lines; `file:line` is the new-file line at `TARGET`. Run the plant first: a phrase planted into an in-memory copy of `EngagementOverview.tsx`'s diff must be listed OTHER, rc 1.
  - **STATUS lists EVERY new or changed string** (file, `file:line` at `TARGET`, the string, OLD text where changed), plus a count per file. **The seat never invents, judges or edits a word.**
  - The person-name scan over the new strings is **UNDERSCORE-AWARE**: use `(?<![A-Za-z])<name>(?![a-z])` in `python3 -I -B` `re` (`_` split first), with the cover-name tokens B1454 used (`.tools/b1390/scripts/drive.mjs:90`, read in-process, never printed). Its control plants `_by_<name>_` and must fire.
- **D-9: One attempt; a rollback ends the run.** A deploy that fails before the app answers is fixed only by the way back, then `STOPPED:`.
- **D-10: Jira and records: this seat writes none.** STATUS lists every Jira key the squash subjects and PR titles name (MEASURED for #298-#302: the subjects name none; the census maps them to HPSMPOC-228, -439, -323, -352, -356 and -436, RELAYED from `tuesday/briefs/2026-11-10_feedback_census/CENSUS.md`).
- **D-11: No data written on UAT. The walkthrough, the readiness hub and the feedback pages are READ-ONLY to the seat.**
  - The ONLY non-GET calls to UAT are these, all COUNTED:
    - the start page's own sign-in POSTs (`POST /api/auth/uat` 303: the level buttons, and the Demo Walkthrough option, which posts the same route);
    - sign-out POSTs (`POST /api/auth/signout`);
    - the refused probes as B1454 ran them: Admin `POST /api/v1/admin/demo/reset` naming a NON-EXISTENT seed set, and Admin `DELETE /api/v1/customers/<random uuid>`, each answering 403 `uat.action-off`.
  - **Per walkthrough context:** exactly ONE `POST /api/auth/uat`, then the 14 steps with 0 non-GET requests, then exactly one `POST /api/auth/signout`.
  - **On the readiness hub, never click "Start a self-assessment"** (it creates a run). Never open a runner page's controls.
  - **In PART F, never click anything inside the two feedback pages.** MEASURED at source `0820efe9` (`api/src/HpsmPoc.Modules.Feedback/FeedbackModule.cs:170-172`): approve and delete are NOT switched off on the review copy; they are open to anyone there.
  - The walk's request router ABORTS and counts every other non-GET `/api` request. Any count > 0 = a slot-S9 class.
  - The account menu's level items POST `/api/auth/uat`: open the menu and read its items only.
  - If `Feedback__Route` is not exactly `off` at Step 0: STOP before any write.
  - Local SQLite data written by the LOCAL pair is allowed (scratch, 127.0.0.1 only).
- **D-12: The readiness pages: the hub changes BY DESIGN; nothing else does.** Read BEFORE and AFTER, read-only, as Partner at 1440 and 390:
  - **The runner and results pages linked from the hub** (B1454: two 0.3.0 runner pages with own statements 4 / 4, and two results pages): text hashes BEFORE = AFTER. A difference = STOP.
  - **The hub `/assessments`:** the differences are confined to:
    - (1) the H1 and the document title;
    - (2) the header's eyebrow;
    - (3) the FIRST panel, which is the old run's overview BEFORE and the current-statements panel AFTER (as D-13 (R) expects).
    
    The hub's runs list section is equal BEFORE and AFTER. Any other hub difference = STOP with the text diff. The hub absent, 5xx, or without the runs list = a slot-S9 class.
- **D-13: The change is proven live by measurement, not by assertion.**
  - **(R) Readiness, as a Partner user, GET-only walking** (sign in with the Partner level button, navigate by URL `/assessments`, read the DOM, sign out). **Expectation (slot S15):** as written in slot S15 below. **Record what is SEEN, verbatim:**
    - the `h1` text;
    - `document.title`;
    - the first panel's heading text (the first `section` or panel under the header; AFTER expected `[data-testid="readiness-current"]`, RELAYED from the pending PR at 09:23);
    - the count of statements in that panel (`li` elements inside it) and the count of areas (`[data-testid="readiness-current-area"]`);
    - the sidebar entry's label for `/assessments`;
    - whether the "Start a self-assessment" control is present (present/absent only; NEVER clicked);
    - BEFORE the same fields (BEFORE expected: H1 "My readiness", first panel = the old run's overview).
    
    Do this at 1440 x 900 and 390 x 844, with a screenshot of each AFTER hub (`after-uat-readiness-hub-<w>x<h>.png`). Open the 1440 one with the Read tool and describe it. **If what is seen differs from S15 in any field: STOP with the seen values (not a rollback unless D-12's slot-S9 clause fires).**
  - **(C) Step 10 caveat on UAT:** in each of the two walkthrough walks, read the panel's "Presenter accuracy note" text at step 10 and compare it IN PROCESS with `TARGET`'s `steps.ts` caveat string (equal = PASS; print both lengths and a hash; the text itself is already in D-8's table).
  - **(W) Walkthrough unchanged otherwise:** two walks, as in B1454 D-13: 1280 x 900, then a NEW context at 390 x 844 (the restart). Record the per-step table (step, path, status, `h1`, non-GET count, empty state). Each row must equal B1454's AFTER row (RELAYED: paths `/home` x3, `/workspace`, `/engagements`, `/customers/<sample>/{assessment,results,recommendation,narrative,report}`, `/action-plan`, `/services`, `/revenue`, `/home`; h1 Home, Home, Home, Customers, Engagements, Guided assessment, Score & findings, HP/HPSM recommendation, Narrative review, Executive report, Partner Action Plan, Delivery phases, Revenue Calculator, Home; all 200) and this seat's BEFORE row for the same path. The sample customer's id-hash equals the BEFORE `pickSample` pick (B1454: `d46a48c8cf875af1`). Each walk makes exactly 1 `POST /api/auth/uat` and 1 `POST /api/auth/signout`, and 0 others.
  - **(A) Recent activity:** on the sample customer's overview page (`/customers/<sample>`, if it has one), as Partner at 1440 and 390: the "Recent activity" entries' text equals BEFORE after whitespace normalisation (titles and detail lines unchanged). Record each linked entry's accessible name equal to its title (`aria-labelledby` resolved) AFTER. No click.
  - **Plain sign-ins show no walkthrough panel:** on every one of the 8 level sign-ins, the walkthrough panel (`[data-testid="walkthrough-panel"]`) counts **0**.
  - **(N), (E), (M) are not measurable on UAT without a write or another mode.** They are proven at BUILD 3 (CI tests), BUILD 4 (packages) and BUILD 7 (local pair), and STATUS says so in NOT TESTED.
- **D-14: The review door is NOT re-tested and NOT broken.** Status only, with no session, no redirects followed and no body kept: `/admin/feedback/review` 200, `/admin/feedback/review/` 308, and `/admin`, `/admin/feedback`, `/home`, `/workspace`, `/customers` 307 to `/?next=...` (= B1454 BEFORE and AFTER). A regression is a slot-S9 class.
- **D-15: No live PDF.** The report step's page is VIEWED only. No download or print control is clicked. No feedback attachment is downloaded.
- **D-16: Hosted data is not reset, and not read beyond counts (except PART F).** Customers per level (4/5/5/4 with the B1454 instrument, RELAYED) and the customer-id set hash: BEFORE = AFTER. A removed or replaced row = rollback class. A changed count otherwise = STOP with the numbers.
- **D-17 (NEW): PART F, the UAT feedback store, READ-ONLY, after PART P PASSED** (the product owner: "please check all feedback items"). The feedback census found that the route to Jira has been OFF on UAT since early November, so items sent on UAT are saved only in UAT's own database and have never been read (RELAYED, `tuesday/briefs/2026-11-10_feedback_census/CENSUS.md`, "One gap I could not close"). **Facts at source (MEASURED at `0820efe9`, none of them in the range):**
  - `GET /api/v1/feedback` is `listFeedback`, Admin role only (`FeedbackModule.cs:166`). It takes `limit` 1-200 (default 50), `category` (one of `review, bug, idea, content, question`) and `state`. It returns newest first by id, with no cursor (`FeedbackEndpoints.cs:50-56`, `:209-227`).
  - The "Feedback received" page (`/admin/feedback`) lists **ONLY category `review`** (`web/src/components/feedback/AdminFeedback.tsx:75`, `category: "review"`), so it does NOT show every item.
  - The approval page (`/admin/feedback/review`) lists `state=held` (`FeedbackReview.tsx:42`). On UAT its Approve and Delete are LIVE for anyone (D-11).
  - Each item carries id, category, comment (null once erased), page, `submittedAt`, the submitter's user id and roles, the delivery state, `erasedAt`, and the attachment facts.

  **The procedure:**
  1. In a NEW browser context, sign in with the **Admin** level button (one `POST /api/auth/uat`, counted). The request router ABORTS every non-GET other than that sign-in and the final sign-out, and ABORTS every GET whose path contains `/attachments/` (no download).
  2. Load `/admin/feedback` and read the DOM only: the H1, the rendered item count, and the state filter's presence. **Never touch the filter, a Download link or anything else.**
  3. Load `/admin/feedback/review` and read the DOM only: the H1, the rendered held-item count, and the Approve/Delete button counts. **NEVER click.**
  4. **ONE in-page `fetch('/api/v1/feedback?limit=200', {method:'GET'})`** (all categories), saved to `.tools/b1460/fb/all.json` (mode 600; NOT in `Briefs/` or evidence). If it returns exactly 200 items, the list may be truncated: then also GET `?category=<c>&limit=200` for each of the 5 categories, take the union by id, and say which frame you have. Any category still at 200 = report "possibly truncated", and STOP before claiming completeness.
  5. Sign out (counted).
  
  **Controls:**
  - the rendered count of `/admin/feedback` = the number of items in `all.json` with category `review`;
  - the rendered count of the approval page = the number with state `held`;
  - a router plant (a page-side `fetch('/api/v1/feedback/x/submit',{method:'POST'})` run on the LOCAL pair, never on UAT) is counted 1 and ABORTED.
  
  **STATUS gets the PART F table:** id (`FB-` id as returned), date (AEDT, from `submittedAt`), category, delivery state, held (y/n), shown on "Feedback received" (y/n), shown on the approval page (y/n), page (the path with every customer id replaced by `<customer>`), attachments (count only), erased (y/n), and **a text summary of at most 25 words in your own words, with NO person name, NO e-mail, NO customer name and no quotation beyond 8 words.** Never print the submitter's user id. Print roles only, as a count per role.
  
  Before the table goes into STATUS, run the UNDERSCORE-AWARE name scan (D-8's tokens, control `_by_<name>_`) over the summaries; e-mail shapes = 0 (control: a planted `a@b.example` reads 1). Then add counts by category and by state, and the newest and oldest dates. **No screenshot of either feedback page** (the comment text stays out of evidence). Add a line "items newer than 2026-11-03 (the last hand copy to Jira, CENSUS)": their count.
  
  **PART F never fails PART P.** A PART F problem is a STOP of PART F only, written in STATUS, and UAT stays as deployed.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, no other step; each count with a control that can fail)
- **FIRST STEP: the way back is reachable.** Copy `PREV`'s packages from `.tools/b1454/target/{web,api,RUN}` by name, read-only, into `.tools/b1460/rollback/884fd72b238ec8dc0d566b0e9c18b5362f920a2b/`. Then `shasum -a 256` + `stat -f %z` must give web `279f184a64a0b4253a832020bf2f261993186f86ea61a8b741088ed4ac445548` (16,542,627 B) and API `7741578de7653c3c68b89916b2df8e0b53eeac368aba0fdc0345b3986cbb3303` (49,630,884 B), file counts 2115 / 122, both `MANIFEST.json` `commit` = `PREV`, and `RUN` = `42659375588` (MEASURED by the drafter on the source copy at 09:28; control: the two digests differ). **If the copy is absent or unequal, rebuild by the project script** (`scripts/deploy-from-ci.sh fetch PREV` from a clean detached clone at `PREV`, BUILD 2) and require the same digests. Digests unequal, or artifacts expired (they expire 2026-11-16): `STOPPED: NEEDS TUESDAY no proven way back`. **NEVER deploy without a proven way back.** `fa401da9`'s packages are NOT the way back.
- **The last UAT deploy.** `tail -n 1 'Briefs/2026-11-10_B1454_STATUS.md'` begins `DEPLOYED B1454: 884fd72b238ec8dc0d566b0e9c18b5362f920a2b` (control: a scratch file ending `DEPLOY B1460: PENDING` counts 0 for `^DEPLOYED `). The deploy-STATUS listing names no UAT deploy newer than B1454; for a newer one, or a `ROLLED BACK` line, read it whole (unexplained = STOP). **Which build is live (UNMEASURED by the drafter):** public `GET /` names `bytHj28aj21cVQmgGGcmh` x1, and the live trees equal `PREV`'s packages by `deploy-package.py live-check` (web 2115/2115, API 122/122, site-only 0). Any other build = STOP, UAT untouched.
- **Panes (word it exactly).** Print `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` and classify every pane by name. **The REFUSE fires ONLY on:**
  - (a) another `Datasec/HPSM-POC-D*` pane. **`Datasec/HPSM-POC-D57` is included:** its STATUS ends `DEPLOYED B1454`, but MEASURED at 09:25:07 the pane `%24 Datasec/HPSM-POC-D57` was still listed. Tuesday closes it before this launch (slot S10 (e)).
  - (b) any other pane whose kit lets it call a hosted HPSM-POC host or `az`.
  
  It does **NOT** fire on a builder (`-H*`), records (`-R*`) or gate (`-G*`) pane whose kit forbids hosted calls. List each with its kit's no-hosted line (`/usr/bin/grep -n -i -E 'no az|hosted host'` over the kit the pane names; control: the kit names `hosted`). Non-HPSM panes (`NexusAI-*`, `MPS-*`, `Security-Composer-*`, `fleet-monitor`) are listed by name only. They are other projects: never read their kits beyond the name, never touch them.
  
  HPSM panes at drafting (MEASURED 09:25:07): `%0 tuesday`, `%11 -H147`, `%13 -H142` (builds the pending PR's branch; kit B1392 `:15` "...HPSM-POC deploys nothing. You touch..."), `%14 -H143`, `%15 -H144`, `%16 -H145`, `%17 -H146`, `%18 -H153`, `%19 -R197`, `%20 -G374`, `%21 -G376`, `%22 -G375`, `%23 -G377`, `%24 -D57`, `%25 -G378`. Re-list immediately before the deploy START. Never wait for, message or touch such a pane, its branch or its worktree.
- **The target.**
  - Slot S4 is 40-hex and a descendant of `0820efe9`. Slot S5 is numeric. Slot S12 lists `298 299 300 301 302 <the pending PR>`.
  - For EVERY PR in S12: `merged` true; `merge_commit_sha` on main's first-parent line in `PREV..TARGET`; `head.sha` printed; check-runs on the head all success (control: a no-such PR number 404).
  - **The gate verdict lines are printed** (`head -n 1` of B1450, B1451, B1452, B1453, B1455, and the pending PR's gate named in S6). Each must begin `GATE VERDICT B<n>:` and read `GO` or `GO WITH FINDINGS` at the head that landed.
  - Where the landed head is past the gated head (MEASURED: #300, gated `121ee23`, landed `b18457c2`, +1 commit, 1 test path), prove by `compare <gated>...<landed>` that the extra commits touch only the paths named. Any product path outside the gate = STOP.
  - Slot S6 carries each gate's open findings by id. A Major in any gate's FINDINGS that S6 does not carry = STOP.
  - **D-1 holds.**
- **CI at `TARGET`.** As above; equal to slot S5 or another green run of `TARGET` (say which).
- **Stamp slots.**
  - `/usr/bin/grep -o -E '_{4}' <your copy> | wc -l` reads 0 (control: a five-underscore scratch file >= 1).
  - `/usr/bin/grep -c -E '@(TARGET|READINESS)@' <your copy>` reads 0: a slot token left unfilled = STOP (control: a scratch line built by joining `@`, `TARGET` and `@` reads 1).
  - The last line begins `READ-WHOLE-BY-TUESDAY: DONE`.
  - S7 is exactly `CODE ONLY; NO SCHEMA STEP; NO WHAT-IF; NO TEMPLATE DEPLOY; NO APP SETTING WRITE; NO DATA RESET`.
  - S8 is exactly `UAT ONLY`.
  - S10 holds `CONFIRMED` for (a)-(f), with no `NOT CONFIRMED` and no `UNSET` in the VALUE part.
  - S11 is exactly `UAT WORDS: THE CLOSED LIST OF D-8, READ BY THE PRODUCT OWNER` (or `HOLD`: STOP at once).
  - S13 is exactly `UAT HOLD LIFTED FOR THIS DEPLOY ONLY: ACCEPTED`.
  - S14 lists the pending PR's strings by `file:line`, or reads exactly `NONE`.
  - S15 is filled with text (not the slot token).
  - Anything else: STOP.
- **Clock.** Run `date` at Step 0. Later than 45 min after slot S1, or the hard stop passed, or fewer than 60 minutes to the write cut-off: STOPPED ("not enough time").
- **Identity.** As above. PRIOR WORK (STANDING 1) is read WHOLE before the first `az` call.
- **Names, settings, route** (UNMEASURED today; RELAYED from B1454 REFUSE 8 and W4). All read in-process; print only yes/no or the name list, never a value.
  - `az webapp list -g hpsm-poc-uat-rg --query "[].name" -o tsv` = exactly `app-hpsmpoc-api-uat-25onzn` and `app-hpsmpoc-web-uat-25onzn` (by program; control: one character changed differs).
  - SQL server exactly `sql-hpsmpoc-uat-25onzn`; database `hpsmpoc` as D-5.
  - SQL firewall exactly `AllowAllWindowsAzureIps`.
  - Setting names API 35 / web 17.
  - **`Feedback__Route` exactly `off`.**
  - `Assessment__MigrateOnStartup` absent (MEASURED at source: when true it migrates the feedback store at startup, `FeedbackModule.cs:151-155`; absent = no migration).
  - **`Assessment__Environment` and web `HPSM_ENVIRONMENT` exactly `uat`.**
  - `Auth__UatOpen__Enabled` `true`; `HPSM_DEMO_NOTICE` `off`.
  - `HostedDemo__Seed__Enabled` true and `HostedDemo__Seed__OwnerObjectId` present.
- **Ports.** Block **9970-9979 ONLY** (D57's block; D57 ended `DEPLOYED` at 05:49).
  - MEASURED at drafting (09:25:07): `lsof -nP -iTCP:9970-9979 -sTCP:LISTEN | wc -l` = 0 (control: all listeners 17).
  - The word-boundary scan `(^|[^0-9a-f])997[0-9]([^0-9a-f]|$)` over the 58 non-`.pre-` SEAT kits of 9 and 10 Nov in `tuesday/briefs/` hit 3 files: B1391 (D56, ended), B1450 `:23` (the reservation "to B1391 (D56)") and B1454 (D57, ended) (control: `994[0-9]` hits 6 files). G377's and G378's kits list 9940-9999 / 9900-9999 as "taken at drafting" (blocks other kits named then, D57's among them), not as their own claim.
  - The seat re-runs both scans just before the first listener (this kit set aside) and takes the next free 10-block if either fires with a claim other than D56's or D57's.
  - **Not to use:** 9940-9969, 9980-9999, 9520-9529, 9570-9599, 9680-9739, 9640-9649, 9670-9679.
  - Bind `127.0.0.1` only.
- **Live seats and trees.** Other seats' trees (every `.tools/b13*`, `.tools/b14*` other than `b1460`), branches, ports and locks are never yours. `.tools/b1454/` is read by name only. `.tools/b1460` was absent at drafting (MEASURED); anything there you did not make: STOP.

## PRE-DEPLOY SIGNALS (UAT; read ALL before the deploy, and again before any way back; `presig1460.py` = a copy of `presig1454.py`)
1. Both sites Running, HTTPS only, `alwaysOn` true; `linuxFxVersion` / `appCommandLine` as D-6 (plain ARM GET).
2. App-setting names, value hashes (in-process; never print a value) and slot flags: API 35 / web 17. Value-hash summaries RELAYED from B1454 W4 = `fa62b3968883ca61` / `fe5590fba73ea35f` (comparable only if computed by an unchanged hash function: say so). Switches as REFUSE "Names". Key Vault references `Resolved`, except the two feedback webhook references, which read `SecretNotFound` (pre-existing since B874).
3. Active deployments: web `9212fb0b-4878-46be-9d53-d7cb108d8742`, API `802ab059-93d3-4e73-a41c-fdd75ccca6e2` (RELAYED); none in progress.
4. Platform lines newer than B1454's containers (web 2026-11-09T18:32:24Z, API 18:33:20Z): none, except as D-6 allows.
5. The ARM activity log of the group since **2026-11-09T18:33:46Z** (after B1454's `DEPLOY END 18:33:45Z`), read with BOTH `--start-time` and `--end-time`:
   - restart / stop / start / config-write / sites-write / deployment counts **0**;
   - `publishxml/action` reads listed (B1454's own after-reads made 4);
   - SQL `databases/pause` since 2026-11-01T00:52:35Z **0**;
   - SQL `firewallRules/write` and `/delete` since 18:33:46Z **0**.
   
   **Any write in that window = STOP; list it.**
6. Plan `asp-hpsmpoc-uat` P0v3 x1 with `LastError` empty; access rules, SQL firewall (1), vault secret names (2), resource list (14) and tags: saved and equal to B1454 W4.
7. The database as D-5; the public page build (`bytHj28aj21cVQmgGGcmh` x1); no new `B1460_ADDENDUM-*.md`.

**Rule:** any difference not covered by D-6 STOPS before the next write, listing EVERY differing signal.

## BUILD (one attempt; fix root causes, never skip; nothing hosted is written in BUILD)
1. **Step 0 and PHASE 0 (read-only).**
   - Run `date` and do the clock arithmetic (hard stop and write cut-off as absolute AEDT clocks), then the REFUSE checks in order.
   - Copy this brief unchanged into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/`; record `cmp`, both sha256s and the slot count.
   - **Write STATUS `1_Project_Definition/Briefs/2026-11-10_B1460_STATUS.md` right after Step 0:** first line `DEPLOY B1460: PENDING`, then a STATUS-NOW line kept current (step, next command, minutes to the cut-off). Write no `DEPLOYED`, `ROLLED BACK` or `STOPPED` line until you mean it (a watcher fires on them).
   - Re-measure `compare PREV...TARGET` and print every commit with its PR number and every path with its +/-.
2. **Clones (detached).**
   - `.tools/b1460/repo`: a clone of origin with the project deploy key, set by a per-command `-c core.sshCommand=...` from `3_Access_Keys/github_deploy_rw` (never printed); push URL `DISABLED-no-push`; `checkout --detach TARGET`.
   - `.tools/b1460/repo-rb`: detached at `PREV`.
   - Never `git fetch`, `worktree add` or a ref write in `2_Project_Files`; never a push. Do NOT reuse `.tools/b1454/repo`: it is D57's tree.
3. **Fetch and prove `TARGET`'s packages.**
   - From `repo`: `scripts/deploy-from-ci.sh fetch TARGET` (rc 0). Quote both `OK ... package` lines, both `MANIFEST.json` `commit` = `TARGET`, and the `RUN` file (= S5).
   - Record the new web `.next/BUILD_ID` (it must differ from `bytHj28aj21cVQmgGGcmh`). Copy to `.tools/b1460/target/`; `diff -r` must be equal.
   - Control: `verify --expect-run 42659375588` on `TARGET`'s packages fails.
   - **No-schema proof:** `TARGET`'s `assessment.sql` and `feedback.sql` sha256 equal `PREV`'s (`8a4084b6...` / `2a587ac2...`, MEASURED on `.tools/b1454/target/api/` at 09:28; unequal = STOP). The range schema regex reads 0.
   - **The API change's tests passed in CI** (the `api-test-results` artifact; see CI above).
   - `CHECKPOINT CI green`.
4. **Package checks, `TARGET` vs `PREV`, property first** (`pkgcmp1460.py` and `lits1460.cjs` are copies of the `1454` versions with their maps hand-edited; run the plant controls first).
   - **Web:**
     - page routes (`app-paths-manifest.json`): added 0, removed 0 (B1454: 58 = 58; neither the range nor the pending PR adds a route at drafting);
     - `node_modules/`: 0 differences (control: `node_modules/next` >= 900 files in both);
     - static/public equal;
     - the differing files are chunk, app and build-id files, each explained.
   - **Bundle-wide literal property** (`lits1460.cjs`, redaction on): every `TARGET`-only literal is a build, chunk or route name, bundler-generated, or verbatim in `TARGET`'s source of the range's web product paths; every `PREV`-only literal is explained; UNEXPLAINED 0 both ways. Checks (files containing each, `TARGET` / `PREV`):
     - `TARGET`'s step 10 caveat >= 1 / 0;
     - `PREV`'s caveat 0 / >= 1;
     - the hub's lead-panel sentence start "A new self-assessment asks these" >= 1 / 0 (if S14 lists it);
     - control: "Playbook Partner Readiness" >= 1 in BOTH.
   - **Test code does not ship:** one string unique to `web/src/server/auth/refresh-fanout.test.ts` and one unique to `web/src/server/mock/customer-shape.test.ts` (each printed with `git grep -n -F` at `TARGET`) read 0 in the web package (control: a product string >= 1).
   - **API, the property "Assessment carries code; the rest is stamp-only":**
     - the file count is equal (122 = 122 expected);
     - every non-DLL/PDB file is EQUAL (`appsettings.json`, `*.runtimeconfig.json`, `*.deps.json`, `assessment.sql`, `feedback.sql`, every `SeedContent/` file);
     - **`HpsmPoc.Api.dll`, `Modules.Feedback`, `Modules.Reporting`, `Modules.Rules`: 0 unnamed runs each** (B1454's PE method; plant first: a flipped byte outside the named regions reads 1 unnamed run);
     - **`HpsmPoc.Modules.Assessment.dll`: unnamed runs >= 1 EXPECTED** (the HPSMPOC-436 guard). Its `#US` user-string heap holds "There is no visible finding to explain." x1 at `TARGET` and x0 at `PREV`, and `narrative.no-findings` x1 / x0 (UTF-16LE search; control: "is not a visible finding of this assessment." x1 in BOTH);
     - an unnamed run in any OTHER DLL = an unlisted `api/` change: STOP;
     - each `TARGET` DLL embeds `T8` x1 and `PREV8` x0 (control: `PREV`'s embed `PREV8` x1).
   - `CHECKPOINT package checks`.
5. **The way back, proven and not run.**
   - `PREV`'s packages per REFUSE line 1. `deploy-package.py verify --expect-commit PREV --expect-run 42659375588` rc 0 (control: `--expect-run 42689075848` fails).
   - Download the BEFORE wwwroot of both UAT apps read-only (as `live1454.py` did; token in-process, never printed; sha256 recorded). The live-check against `PREV`'s packages must be equal (B1454 AFTER: web wwwroot sha256 begins `7fbe5a7c`, API begins `b0804c26`, RELAYED, truncated in its STATUS).
   - `rollback1460uat.sh` = a copy of `rollback1454uat.sh` (sha256 `f52193f7...6dc9a`, MEASURED; `cmp` the copy first, then hand-edit). Guards before ANY `az` call:
     - `repo-rb` HEAD = `PREV` `884fd72b...` (rc 96);
     - `PREV`'s zip sha256 `279f184a...` / `7741578d...` (rc 97);
     - the identity pass (rc 2).
     
     Then `az webapp deploy` web then API to `hpsm-poc-uat-rg`, `--type zip --async false --clean true`, with an identity pass before each. Then the live-check against `PREV`'s packages (web 2115, API 122) and `BUILD_ID` `bytHj28aj21cVQmgGGcmh` x1.
   - After editing: `/usr/bin/grep -c -E 'fa401da9|dD6A9DDYNcVDCTsrvmQbE|ba763dfe|5584ff04'` reads 0 (control: the unedited copy >= 1).
   - **Stub run** (a scratch `PATH` `az` that answers `account show` with the records' identity and logs every other argv): the argv names `hpsm-poc-uat-rg`, the two UAT sites in order, and `PREV`'s zips; `TARGET`'s sha or zips appear in argv 0 times. Controls:
     - the HEAD check with `repo`'s HEAD (= `TARGET`): rc 96 with 0 calls;
     - zips pointed at `TARGET`'s package dir: rc 97 with 0 calls.
   - `CHECKPOINT rollback point taken`.
6. **Instruments.**
   - Copy by name + `cmp` from `.tools/b1454/` (read-only), rename to `1460`, hand-edit: `identity_pass`, `presig`, `live`, `pkgcmp`, `words`, `lits`, `walk`, `cmpwalk`, `pairseed`, `webpair`, `deploy`, `rollback`, `statusnow` (list which).
   - **New behaviour to WRITE into the walker (`walk1460.cjs`) and the comparator (`cmpwalk1460.py`):**
     - (a) the D-13 (R) readiness reader: the SEEN fields, the "Start a self-assessment" control counted and never clicked;
     - (b) the D-13 (C) step-10 caveat reader, with in-process equality to `TARGET`'s source;
     - (c) the D-13 (A) Recent-activity reader;
     - (d) the PART F reader of D-17. Its router aborts every non-GET but the two allowed, and every `/attachments/` GET. Plant on the LOCAL pair: a page-side `POST .../submit` is counted 1 and aborted.
     - (e) `cmpwalk` allows these differences only: on `/assessments`, the D-12 hub differences; inside the walkthrough at step 10, the caveat text; on the customer overview, whitespace in Recent activity. Everything else must be equal.
   - After copying, `/usr/bin/grep -c -E '1454|fa401da9|dD6A9DDYNcVDCTsrvmQbE'` per file reads 0, except where a file quotes B1454 as the PRIOR deploy (list those; control: an unedited copy counts >= 1).
   - `/usr/bin/grep -l -i -E 'sql db update|deployment group (create|what-if)|appsettings set|appsettings delete|sqlcmd|firewall-rule (create|delete)|/submit|method: *.DELETE'` over `.tools/b1460/` programs (clones and package trees excluded) lists only the PART F plant line and the router's abort list (name each; control: plant one line, and it lists 1 more).
   - **Never copied:** schema, seed, `sqlcmd` or feedback-write instruments; `shots-*`, `uat/`, `live/`, `vals/`, `presig/` evidence; other seats' clones.
7. **The local pair on the port block** (NO load gate: restamp 4b, carried). Print `uptime` load1 beside each run. A check that fails on timing alone is re-run once and both results are written; a failure that is not timing-only is a STOP. Run under `.tools/b1460/heavy.lock`.
   - Run `TARGET` web + API UAT-shaped (SQLite; in-process keys, never printed; `WEBSITE_SITE_NAME` containing `-uat-`), and `PREV`'s pair as the control, each on its own copy of a database that `PREV`'s API seeded (as `pairseed1454.py`/`webpair1454.py`, with the seed owner pinned).
   - **(i) API seeder:** `TARGET`'s API boots twice on a `PREV`-seeded db. Each boot logs "...already in this database; nothing was written.", and every table's row count and row hash are equal (plant: one added row reads 1 differing). The `demo` label refuses to start (negative control).
   - **(ii) Web:**
     - the 4 levels sign in;
     - route tables `TARGET` vs `PREV`: status differences 0; text differences only where `cmpwalk` (e) allows;
     - the panel 0 on plain sign-ins;
     - **the readiness hub on `TARGET` shows what S15 expects for the local Partner, and `PREV` shows the old hub (plant).** Say whether the local Partner's newest completed run is on an older version; if the local seed has no completed run, say so and mark (R) LOCAL as NOT APPLICABLE (UAT is where it counts);
     - the 14-step walk against the REAL local API, with step 10's caveat = `TARGET`'s source string.
   - **(iii) NEW, the API change (HPSMPOC-436), local `TARGET` API only, then `PREV` as control:** as the local Admin or Partner, with the API's own route for `generateNarrative` read from `TARGET`'s source (print its `file:line`), send ONE request with kind `finding-explanation` and `findingIds: []` against a scored seeded assessment (with the `If-Match` precondition the endpoint needs, `ReportingEndpoints.cs:169`).
     - `TARGET` answers **422 with code `narrative.no-findings`**, and the `narratives` table's row count and hash are UNCHANGED.
     - `PREV` (control) does NOT answer `narrative.no-findings` (record what it answers, and that it may store a failed row on its own scratch db).
     - **Never on UAT.**
   - A failed start or an unproven page = STOP before any write. `CHECKPOINT local pair`.

## PART P: the packages to UAT (`hpsm-poc-uat-rg`; web `app-hpsmpoc-web-uat-25onzn`, API `app-hpsmpoc-api-uat-25onzn`) `[PROD-CLASS]`
P1. **BEFORE (read-only).**
- PRE-DEPLOY SIGNALS (all seven) and D-5 (`CHECKPOINT DATABASE STILL AWAKE (before)`); the live-check of the downloaded wwwroots against `PREV`; `/health/ready` once, timed.
- **The start page BEFORE:** four level buttons in DOM order (partner, consultant, admin, demo), none disabled; the Demo Walkthrough option count 1 (B1454 AFTER).
- Per level: the signed-in landing and the route table at 390 and 1440, with visible text kept; the panel 0 on each.
- Customers per level and the id-set hash (D-16).
- **The readiness hub BEFORE as Partner (D-13 (R) fields).**
- **The 14 jump targets as a plain Partner** (GETs only; the BEFORE row each AFTER step is compared with).
- **The Recent-activity entries of the sample customer.**
- The refusal matrix (403 `uat.action-off` x2); D-14 status-only; the D-12 runner and results pages hashed.
- Screenshots `before-uat-<page>-<w>x<h>.png` (the start page at 1280 x 900 and 390 x 844; Partner home; **the readiness hub at 1440 x 900**; the sample customer's report page as a plain Partner; **never `/admin/feedback` or `/admin/feedback/review`**) into `Briefs/2026-11-10_B1460_evidence/`. Open the key frames with the Read tool and describe them.
- `CHECKPOINT UAT BEFORE walk`.

P2. **Deploy.** `[PROD-CLASS]`
- Start the poller and the watchdog (`deploy1460.sh`, a copy of `deploy1454.sh` with its guards hand-edited): before the write cut-off; `B1460_ADDENDUM` count 0; `repo` HEAD = `TARGET`; `RUN` = S5; live public build `bytHj28aj21cVQmgGGcmh` x1 and `TARGET`'s BUILD_ID x0.
- Fresh identity pass. Re-list the panes. Re-read the addenda and the PRE-DEPLOY SIGNALS (firewall = `AllowAllWindowsAzureIps`). Re-read origin main against S4 (D-1).
- Then, in the same second as `DEPLOY START`, run exactly `scripts/deploy-from-ci.sh deploy TARGET hpsm-poc-uat-rg app-hpsmpoc-web-uat-25onzn app-hpsmpoc-api-uat-25onzn` from `.tools/b1460/repo`. **These are the only `az` writes of the run: the script's two `az webapp deploy` lines. No `--restart`, no setting.**
- Exit 0 = done. Exit 3 = DEPLOYED BUT NOT PROVEN: STOP with the list. Exit 1: read the reason; no hand steps.
- Windows from deploy start: **web 420 s, API 900 s** (B1454 took 2 min 6 s, RELAYED). Past a window, any non-200 starts `rollback1460uat.sh` within 60 s.
- Wait by `kill -0` or done-marker files. Write a heartbeat every 30 s to `.tools/b1460/logs/heartbeat.txt`.
- `CHECKPOINT UAT deploy START`.

P3. **AFTER (read-only HTTP to the UAT hosts; only D-11's named non-GET calls).**
- (a) `/api/health` and `/health` 200 x3, ten seconds apart; `/health/ready` 200 (timed); `/` 200; `/customers` 307 to `/?next=%2Fcustomers`; `/api/auth/session` `{"signedIn":false}`; `login.microsoftonline.com` 0.
- (b) **Start page:** equal to BEFORE (the level buttons and the walkthrough option, text hash).
- (c) **8 of 8 plain sign-ins** (four levels x 390/1440), each signed out (counted); **walkthrough panel 0 on every one**.
- (d) **Route table BEFORE/AFTER:**
  - every BEFORE route at every level and width = AFTER in status, and in visible text except where D-12 / D-13 allow (the `/assessments` hub; Recent-activity whitespace);
  - routes only before 0, only after 0;
  - customers per level and the id-set hash = BEFORE (D-16);
  - pages without the sidebar 0; console errors not above BEFORE; 5xx 0.
- (e) **THE CHANGE LIVE, measured (D-13):**
  - **(R)** the readiness SEEN table at both widths vs S15;
  - **(C)** the step 10 caveat in both walks, equal to `TARGET`'s source;
  - **(W)** the two 14-step tables;
  - **(A)** the Recent-activity check;
  - screenshots: the hub AFTER at both widths, walkthrough step 10 at both widths (`after-uat-walk-10-<w>x<h>.png`), and the start page at both widths. Open the key frames yourself and describe them: the hub's H1, the first panel title and the statement count as SEEN in the frame.
- (f) **Security views:** known customer 200 x4 and `no-such-id` 404 x4 per level = BEFORE.
- (g) **The words table (D-8)** in STATUS.
- (h) Refusals = BEFORE (403 `uat.action-off` x2); the D-14 door = BEFORE.
- (i) **Build proof:**
  - live-check web = `TARGET`'s file count, API = `TARGET`'s;
  - live `BUILD_ID` = the package's, x1 on the public page; `bytHj28aj21cVQmgGGcmh` x0;
  - the 5 live API DLLs embed `T8` x1 and `PREV8` x0;
  - the live `HpsmPoc.Modules.Assessment.dll` holds "There is no visible finding to explain." x1;
  - active deployments both new (record them).
- (j) The platform lines of the new containers, verbatim. UAT keeps no readable API stdout: say so (the local boots of this exact package stand in).
- (k) **Settings hashes equal** (W4 vs W3, as B1454; firewall only `AllowAllWindowsAzureIps`).
- (l) D-12 runner and results pages = BEFORE.
- (m) D-5 again (`CHECKPOINT DATABASE STILL AWAKE (after)`). The activity log since `DEPLOY START`: no SQL writes, `databases/pause` 0, only `publishxml/action` reads.

**Healthy and all passed: `PART P VERDICT: PASSED` (`CHECKPOINT PART P PASSED`).**
- Unhealthy past a window, a deployed app not answering, or a slot-S9 class: run `rollback1460uat.sh` (D-7 only), then write `ROLLED BACK`.
- Any other miss on a healthy site (D-13 (R) seen values differing from S15 included): `STOPPED: NEEDS TUESDAY`, with the numbers and the one-command way back printed. **Still run PART F before the STOPPED line if the site is healthy.**

## PART F: the UAT feedback store (READ-ONLY; D-17)
Run only after `PART P VERDICT: PASSED`, or after a healthy-site STOP. Never after a rollback.
- Run D-17 exactly. The only non-GET calls are 1 Admin sign-in POST and 1 sign-out POST, both counted. Print the router's abort counts (non-GET 0 attempted by the pages is expected; `/attachments/` GETs aborted: count).
- Write the D-17 table and its counts into STATUS under `## PART F: UAT feedback (read-only)`.
- `CHECKPOINT PART F DONE`.

## STANDING LINES
1. **PRIOR-WORK CHECK first, read WHOLE before the first `az` call:**
   - this brief;
   - the B1454 kit and `Briefs/2026-11-10_B1454_STATUS.md` (the last UAT deploy by this script; the source of every RELAYED hosted value here);
   - the five gate STATUS files (B1450, B1451, B1452, B1453, B1455) at their FINDINGS and VERDICT sections, plus the pending PR's gate STATUS;
   - `tuesday/briefs/2026-11-10_B1460_WORDS-FOR-KAM.md`;
   - `tuesday/briefs/2026-11-10_readiness_investigation/FINDINGS.md`;
   - `tuesday/briefs/2026-11-10_feedback_census/CENSUS.md` (BLUF and "One gap");
   - `scripts/deploy-from-ci.sh` at `TARGET`;
   - the project `CLAUDE.md`;
   - `1_Project_Definition/CLARIFICATIONS.md` (C-07; a search of `deploy`, `UAT`, `feedback`, `readiness`; control: `C-07` hits, a no-such token 0).
   
   STATUS needs a `PRIOR WORK` section. A READY without one is returned.
2. **Never touch what the ruling does not name.** No `az` write and no HTTP except: the two UAT apps (PART P, PART F), read-only `az` on `hpsm-poc-uat-rg`, and the way back. Nothing of any other group, not even a read (only the subscription-level `az group list`, names only). Never another subscription or database. Never `HP Reporting and Docs/`, any SOW, `2_Project_Files/HP Docs/`, `1_Project_Definition/Source_Documents/`, `.local/`, `4_Credentials/` (beyond the `.azure` and `.gh-config` directories), or `.tools/backup-*`.
3. **Never delete** (`rm`, `rmdir`, `az ... delete`, `--prune`). Quarantine by MOVE to `.tools/b1460/_quarantine/`. Other seats' trees: only the files this brief names, by name, read-only. **A real feedback item is never approved, deleted, moved to another state, or downloaded; it is listed only in PART F, by GET.**
4. **No message to any human**; nothing to HP; no Jira write; no person's name or e-mail in STATUS ("the product owner"). Synthetic data only: print no customer content beyond row counts, page titles and hashes. **The one exception is PART F's summaries (D-17 rules: own words, no names, at most 8 quoted words).**
5. **Secrets:** never on argv, never printed, never in a kept file, STATUS or screenshot.
   - Run gitleaks over the evidence folder with a `ghp_`-shaped canary (rc 1); the real scan must be rc 0.
   - Run the 64-character base64 key shape scan (canary rc 1; real 0 beyond sha256 digests), and `encryptionKey` values 0 in logs and STATUS.
   - Keep host names out of the evidence: `azurewebsites.net`, `scm.`, `vault.azure.net` and `database.windows.net` read 0 outside the STATUS last line (control 1).
   - A dotted-quad scan over STATUS and evidence reads only `127.0.0.1` (control 1).
   - `.tools/b1460/fb/*.json` is mode 600 and is never copied into `Briefs/`.
6. **CodeQL policy.** This seat lands nothing and opens no PR.
7. **Shell:**
   - Never type `cd` (a hook refuses it). Use absolute single-quoted paths (they contain `!`).
   - Use `/usr/bin/grep -i` with a positive control for every count.
   - The Bash tool is zsh: use `pipestatus` or `bash -c`; quote any URL containing `?`; brace every `${VAR}:path`; never an unquoted word starting `=`; wrap `set -- $x` word-splitting in `bash -c`.
   - macOS has no `timeout`. Wait with `kill -0` or done-marker files, never `pgrep -f`.
   - Python only as `python3 -I -B`. Scratch goes under the session scratchpad, never `/tmp`.
   - Hex and sha maps are hand-edited, never passed through `sed`.
   - A `file:line` pointer you cite is printed by `grep -n -i` or `awk NR==n` over the raw file at `TARGET` just before you write it.
   - Read a tool's usage from its header, never by invoking it.
8. **Records: none in this seat.** STATUS and evidence only; nothing committed or pushed.
9. **STATUS sections** (`1_Project_Definition/Briefs/2026-11-10_B1460_STATUS.md`, evidence in `.../2026-11-10_B1460_evidence/`), in this order:
   - Step 0
   - **BLUF.** Its first line states any rollback or stop. **It carries the readiness SEEN values in one line** (H1, first panel title, statement count, sidebar label). **Anything "not shown" goes in the BLUF, never only in the body** (the readiness investigation's lesson).
   - PRIOR WORK
   - PHASE 0 and LIVE-BEFORE
   - Target, gate and CI proof (the PR rows, every gate verdict line, the `121ee23...b18457c2` proof, the tree/blob proof, the config-key scan, the `infra/tests/`-only proof, the Hpsmpoc436 test count)
   - **The words (D-8):** EVERY new or changed string by file with `file:line` and the OLD text; the name scan
   - Package checks (web literal property; API: 4 stamp-only + Assessment's user strings) and the local pair (seeder double boot; the 14-step walk; the readiness hub; the HPSMPOC-436 refusal)
   - The way back (copied or rebuilt; digests; stub)
   - PRE-DEPLOY SIGNALS and the database (before)
   - No schema step
   - PART P (BEFORE, deploy, AFTER: the route table per level and width; the readiness SEEN table; the step 10 caveat; the (W) tables; the build proof)
   - The database (after)
   - **PART F: UAT feedback (read-only)**
   - Settings/access/spend (no new spend)
   - The way back
   - NOT TESTED (Firefox and WebKit; screen reader; axe if absent; Entra mode, including #298's shared renewal; the mock's 400 list (mock mode); the HPSMPOC-436 refusal on UAT (it is a write; proven locally and in CI); a live PDF; SQL Server beyond CI's legs)
   - FOR TUESDAY, in five numbered items:
     1. UAT at `T8`, and the main head at the deploy.
     2. **A short note for the product owner, 4-7 lines, plain words:** what the readiness page now shows, AS SEEN (heading, first panel, number of statements and areas); the step 10 presenter note's new wording is live; Recent activity spacing; nothing else visible changed; how many feedback items UAT holds, how many are held for review, how many arrived after 3 Nov, and the 2-3 themes in plain words.
     3. The tables.
     4. Records owed: a deploy C-entry for `TARGET`; the landing C-entries for #298-#302 and the pending PR; a C-entry for PART F's findings.
     5. Anything seen worth a ticket, including any feedback item that asks for a change.
   - Processes (the last 5 heartbeat lines)
   - Corrections
   
   Also the `CHECKPOINT` lines.

## PARTITION (named from both sides)
- **Yours:** `.tools/b1460/` (including `repo`, `repo-rb`, `target/`, `rollback/`, `live/`, `logs/`, `fb/`, `_quarantine/`) and `1_Project_Definition/Briefs/2026-11-10_B1460_*`; read-only `az` on `hpsm-poc-uat-rg`; read-only GETs on the two UAT hosts (plus D-11's named non-GET calls). Exactly one write class: the script's two `az webapp deploy` lines (PART P), and `rollback1460uat.sh` if a window is breached or a slot-S9 class fires.
- **Not yours:**
  - every other group, database and subscription;
  - the template; any app setting, firewall rule or vault secret; the demo data;
  - `.tools/b1454/` (read-only: copy by name), `.tools/b1391/`, `.tools/b1390/` (`drive.mjs:90` read in-process only) and every other seat's tree;
  - `2_Project_Files` content (read only); records and analysis repositories;
  - any PR, branch, Jira ticket or message;
  - every real feedback item on UAT (read by GET in PART F only);
  - the H142 builder's branch and every gate pane.
- **From the other side:**
  - Before you start, Tuesday has landed the pending PR, closed the D57 pane, and filled slots S1, S2, S4-S15.
  - Builder, records and gate panes deploy nothing and touch no hosted host; none waits for you, and you wait for none.
  - If anything lands on main while you run, you finish on `TARGET` (D-1).
  - Tuesday deploys nothing to UAT and changes nothing in `hpsm-poc-uat-rg` until your STATUS ends `DEPLOYED` or `STOPPED`, and does not reset the hosted demo data in that window.

## HOLDS (never, in this brief)
- No write START after the hard stop.
- No deploy of anything but `TARGET`'s two CI packages (or the way back's `PREV` packages). No deploy of an unmerged branch.
- No what-if; no template deploy; **no `az webapp show`** (plain ARM GET only).
- No `az sql db update`, pause, resume, copy, restore, export or import. No SQL statement of any kind, no `sqlcmd`, no `.sql` file run.
- **No hosted demo-data reset, re-seed or edit.**
- No firewall rule created or deleted. No compute size, sku or backup-policy change. No app-setting or vault write. No restart other than the deploy's own. No `delete`.
- **No feedback item created, approved, deleted, moved to another state or downloaded on UAT. No click on either feedback page. No screenshot of either feedback page. No comment text in evidence.**
- **No narrative generated on UAT. No readiness self-assessment started on UAT ("Start a self-assessment" never clicked).**
- On the walkthrough: no answer saved; no tick, submit, score or approval; the step 10 caveat never followed; no click inside page content; the "All demo screens" list never opened.
- No new assessment created on UAT. No level item of the account menu clicked. No PDF opened.
- No new paid resource. No CI re-run. No code edit. No word edited. No browser install. No claim to HP.
- No production-class action beyond the two named deploy lines.

## Stamp
Pane `Datasec/HPSM-POC-D58` (suffix `D58`). MEASURED at drafting: no `SEAT-D58` kit and no `HPSM-POC-D58` name in `tuesday/briefs/` or `Briefs/` (control: `SEAT-D57` counts 1). B-number B1460 (MEASURED: no `B1460` file in `tuesday/briefs/` or `Briefs/` before the drafter's three files; no `.tools/b1460`). Seat level `BRIEF_SEAT_LEVEL=opus`.
- (S1) STAMP: Tuesday (s262), 2026-11-10 10:19:40 AEDT (`date`). Kit read whole (630 lines before the stamp). CI at TARGET read at source 10:19: run 42717134381 completed/success (every job success except `dependency review`, skipped, PR-only), SQL Server legs 3 of 3 success; CodeQL 42717132328 completed/success; artifacts deploy-web-/deploy-api-6b0c5f2c... expired=false; branches/main = TARGET; load1 2.72.
- (S2) LAUNCH AUTHORITY: the product owner, live board 2026-11-10 09:06, verbatim: "also, please check all feedback items and deploy"; Tuesday terminal ~09:09, verbatim: "don't wait, deploy as soon as it's ready". UAT ONLY. Words: every string of S14 plus the WORDS-FOR-KAM summary was sent to him on the live board (bf-97f8ba297db8 and bf-6ea307688e10) with "no reply means I go ahead"; he replied "thanks" at 09:29 and raised no word. Launched through launch_when_cool.sh with LOAD_MAX unchanged unless this line says otherwise.
- (S3) HARD STOP (the rule): Step 0 plus 120 minutes, written by you as an absolute AEDT clock at Step 0; no write START after it; DONE no later than Step 0 plus 150 minutes; Step 0 within 45 minutes of slot S1.
- (S4) TARGET-SHA (the pending PR's squash on main; a descendant of `0820efe9ff08d32bc0d4710643081abb268f4725`; the seat refuses unless origin main equals this value and the Closed-list proof holds, or main is a later descendant per D-1): 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb (PR #303 squash; MEASURED by Tuesday with `gh api -X GET`: merged true, merge_commit_sha = this, ONE parent 0820efe9ff08d32bc0d4710643081abb268f4725, tree a1eeaabbf031a9aa5b4efbe855c99e8db0e41138 = the tree gate B1392-2 predicted; = branches/main at 10:02 AEDT)
- (S5) CI RUN at TARGET: 42717134381 (push run `ci`; CodeQL `Push on main` 42717132328). Tuesday launches only after both read completed/success; the seat re-reads both per CI at TARGET.
- (S6) WHICH PRs IN TARGET, their heads, their gate lines, and the open findings carried by id: #298 head d7df877a, B1450 GO WITH FINDINGS, B1450-1..6 Minor; #299 head aca2290c, B1452 GO WITH FINDINGS, B1452-1..5 Minor; #300 head b18457c2 (gated 121ee23 + 1 test-path commit), B1451 GO WITH FINDINGS, B1451-1..4 Minor; #301 head 0cdfc74e, B1453 GO WITH FINDINGS, B1453-1 Minor, -2..10 Notes; #302 head c0a5fa17, B1455 GO WITH FINDINGS, B1455-1..2 Minor; **#303 head 9302bc0dd94b8cec4c0dec1270abee28c969eae6, gate B1392-2 GO WITH FINDINGS @ 9302bc0 on main 0820efe, F1-F3 Minor, F4-F5 Note, 0 Major, 0 Blocker. ITS VERDICT IS NOT IN `Briefs/`: it is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1392-2_verify/VERDICT.md`, first line `GATE B1392-2: GO WITH FINDINGS @ 9302bc0 on main 0820efe`. For #303 the REFUSE 'begins GATE VERDICT B<n>:' rule reads `GATE B1392-2:` instead (Tuesday's ruling at this stamp); GO / GO WITH FINDINGS at the landed head 9302bc0 is still required.**
- (S7) RULING 1, the route: CODE ONLY; NO SCHEMA STEP; NO WHAT-IF; NO TEMPLATE DEPLOY; NO APP SETTING WRITE; NO DATA RESET
- (S8) RULING 2, the site: UAT ONLY
- (S9) RULING 3, the package leg's misses. Drafter default: roll back the CODE at once and end ROLLED BACK when:
  - a level does not sign in;
  - a route that answered 200 before answers 5xx after;
  - a security view answers 5xx for the known customer, or 2xx other than the not-found page for no-such-id;
  - any non-GET request other than D-11's named calls is attempted from a security view, from any of the 14 walkthrough steps, from the readiness hub, or from a PART F page;
  - the walkthrough panel appears on a plain level sign-in;
  - the start page loses a level button, or the sidebar is absent on a signed-in page;
  - the account menu is absent, so that Sign out is unreachable;
  - a D-12 runner or results page differs from BEFORE, or the hub is absent, 5xx, or without its runs list;
  - any existing hosted row is removed or replaced (D-16);
  - a horizontal scroll appears that BEFORE did not have;
  - reset or customer-delete answers anything but 403 uat.action-off;
  - the API refuses to start;
  - a D-14 gated admin page stops redirecting a visitor with no session.
  
  Every other miss on a healthy site, including readiness seen values that differ from S15 = STOP, with the numbers and the one-command way back printed: DRAFTER DEFAULT ACCEPTED AS WRITTEN
- (S10) RULING 4, six items, each CONFIRMED / NOT CONFIRMED:
  - (a) read-only copies by name from `.tools/b1454/` into `.tools/b1460/`, hand-edited;
  - (b) the clone of the project's origin into `.tools/b1460/repo` and `repo-rb`;
  - (c) D-11, D-12, D-13, D-14, D-16 (no real feedback item touched; no new run or narrative created on UAT; a real Chromium walk of the 14 walkthrough steps and the readiness hub on the live site, read-only);
  - (d) the UAT API restart for a minute or two, with NEW API code (HPSMPOC-436), with no HP review session under way;
  - (e) the port block 9970-9979 (or the block Tuesday names), and no `Datasec/HPSM-POC-D*` pane other than this one present (the D57 pane closed);
  - (f) PART F, the read-only listing of every UAT feedback item by an Admin-level GET, with summaries in STATUS per D-17.
  
  Values: (a) CONFIRMED; (b) CONFIRMED; (c) CONFIRMED; (d) CONFIRMED: whether an HP reviewer is in session is UNMEASURED by Tuesday; the product owner ordered this deploy now ("don't wait, deploy as soon as it's ready"), so the API restart of a minute or two is accepted under his word; (e) CONFIRMED: ports 9970-9979; Tuesday closed the D57 pane %24 at 09:3x through pane_close.sh (rc 0); (f) CONFIRMED
- (S11) RULING 5, the words on UAT: UAT WORDS: THE CLOSED LIST OF D-8, READ BY THE PRODUCT OWNER
- (S12) PULL REQUEST NUMBERS: 298 299 300 301 302 303
- (S13) RULING 6, the UAT hold: UAT HOLD LIFTED FOR THIS DEPLOY ONLY: ACCEPTED
- (S14) RULING 7, the pending PR's customer-facing strings (D-8 (ii); `file:line` at `TARGET` and the string, or exactly `NONE`). Re-printed by Tuesday at 9302bc0 (= TARGET's tree for these paths, gate-measured merge tree = head tree; the seat re-prints at TARGET):
  - `web/src/content/walkthrough/steps.ts:130` CHANGED caveat: "The report holds sample content; it is not HP-approved guidance. On the laptop sample this screen shows \"No report yet\" until the assessment is completed and scored, and then waits for the approved narrative; do not promise either wait for every customer."
  - `web/src/components/readiness/AssessmentsHub.tsx:87` NEW: "${READINESS_TITLE}: current statements" (renders "Playbook Partner Readiness: current statements")
  - `web/src/components/readiness/AssessmentsHub.tsx:88` NEW: "A new self-assessment asks these ${n} statements in ${m} areas. Your latest completed self-assessment used an earlier set of statements; its results are in the list below." (renders with 16 and 4)
  - `web/src/components/readiness/AssessmentsHub.tsx:99` MOVED: "Start a self-assessment" (same words, `:148` is the existing one)
  - `web/src/components/readiness/AssessmentsHub.tsx:131` CHANGED: PageHeader title `READINESS_TITLE` (= "Playbook Partner Readiness", `web/src/content/readiness.ts:11`), eyebrow "My readiness" (was the H1 text), lead unchanged
  - `web/src/app/(app)/assessments/page.tsx:6` CHANGED: metadata title `READINESS_TITLE` (tab renders "Playbook Partner Readiness · HP Security Services Playbook" via `web/src/app/layout.tsx:7` template)
- (S15) READINESS EXPECTATION (D-13 (R); what the Partner must SEE on `/assessments` AFTER): the `h1` reads "Playbook Partner Readiness"; `document.title` reads "Playbook Partner Readiness · HP Security Services Playbook"; the header eyebrow reads "My readiness"; IF the Partner's newest completed run is on an older content version (UAT's is, per the readiness FINDINGS: the 0.3.0 deck run), the FIRST panel is `[data-testid="readiness-current"]`, its heading reads "Playbook Partner Readiness: current statements", it holds 4 `[data-testid="readiness-current-area"]` and 16 statements (state which element your reader counts, and the count), and its line reads "A new self-assessment asks these 16 statements in 4 areas. ..."; the "Start a self-assessment" control is present EXACTLY ONCE on the page (never clicked); the old run is still listed in the runs list (`[data-testid="readiness-list"]`) with its "View results" link; the sidebar entry for `/assessments` reads "My readiness". If UAT's Partner has NO run on an older version, the lead-with-current panel is not expected: report what is seen and STOP for Tuesday (do not roll back).

**Commission (read-only to you):** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1460_SEAT-D58_hpsmpoc-uat-deploy-main.md`. **Step 0:** run the REFUSE checks in the order written, then copy this brief unchanged into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/` and record `cmp`, both sha256s and the slot count. Preflight: write "none (brief_seat launch)" or quote the launcher's warnings verbatim.
**Launch (Tuesday, ONE waiter, through the cool-load waiter, run as a tracked background task; the level is inside the quotes; launch only after the stamp, after the pending PR has landed, and after the D57 pane is closed):** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/HPSM-POC-D58 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=opus WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1460_SEAT-D58_hpsmpoc-uat-deploy-main.md'"`. `launch_when_cool.sh` and `brief_seat.sh` exist at those paths (MEASURED by `ls -l` at 09:25). load1 at drafting was 29.97 (09:25:07). **Never run /model in this pane.**
**Last line of STATUS, exactly one of:**
`DEPLOYED B1460: <sha40> <site url>` (the sha is `TARGET`; the site url is the UAT web site's public address, written once, as the STATUS last line only), or
`STOPPED: NEEDS TUESDAY <one question>`.
(`ROLLED BACK` is a body line plus a final `STOPPED: NEEDS TUESDAY <one question>` last line.)

READ-WHOLE-BY-TUESDAY: DONE (s262, 10:19 AEDT 2026-11-10; lines 1-630 read before the stamp, the slot edits re-checked by the kit's own counts: `_{4}` 0 after this line, `@(TARGET|READINESS)@` 0 with a firing control)
