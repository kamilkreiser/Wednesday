From Tuesday (the product owner's Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail channel from this project). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`.
# BRIEF B1540 - SEAT-D61: HPSM-POC: deploy code main at `TARGET` (the messaging change, with every commit between the last UAT deploy and `TARGET`) to the hosted UAT review copy ONLY: CODE ONLY, NO database write, NO API stop. Previous build kept and proven first, UAT's current trees downloaded read-only as the code backup, the two CI packages by the project script, live checks as seen (read-only), the new words read on the key pages, and a check that nothing held or next-phase is visible

**STARTABLE: NO until Tuesday has (1) filled every four-underscore slot (S1 to S16 and the READ-WHOLE line: 17 lines), (2) landed the messaging change on main by a head-pinned squash through CodeQL and written the landed main sha into S4, (3) re-read `branches/main` = S4, (4) confirmed that no `Datasec/HPSM-POC-D*` pane is open, and (5) answered Q-1 and Q-2 of the drafter's report (they set S13 and S16). After that the kit is YES.**

In this brief **`TARGET`** = the sha in slot S4 (the landed main sha; NOT known at drafting; **Step 0 refuses unless `branches/main` equals it**). **`T8`** = its first 8 hex. **`PREV`** = what UAT web AND API run now = `009421a28616c8b31dde86b59d4c4ca674c288fa` (**`PREV8`** = `009421a2`). This is **RELAYED, NOT MEASURED NOW** from the last line of `Briefs/2026-11-10_B1466_STATUS.md:271` (`DEPLOYED B1466: 009421a28616c8b31dde86b59d4c4ca674c288fa <the UAT web address>`) and its FOR TUESDAY 1 (`:223`). **What B1466 recorded:**
- Deployed 22:07:01-22:09:10 AEDT 2026-11-10 (11:07:01Z-11:09:10Z) by `scripts/deploy-from-ci.sh`, WITH the one Assessment migration `20261110003228_LedgerAuditAndFollowUpRetention` (applied 11:05:47Z-11:05:50Z).
- Active deployments: web `648087d4-f9ab-44cc-9e69-11b37f2d9440`, API `63357c6f-6490-4752-aadf-425c93c6c47b`. Web `.next/BUILD_ID` `NQga609FQ4iKZFwQ1rtsT`. CI run `42773429652` (CodeQL `42773429155`).
- Packages: web `9d6bb36cf20f4eaa244ed6774c416ce0ceafb79ec150451378978be0dbede19f` (16,558,555 B, 2116 files), API `1fd65b623d3665568e50a2615d25d3f4e5936880355a4f93a1f2e65dc574f9ec` (49,644,626 B, 122 files); `assessment.sql` `03f1afb36b5cb4261a5932f64da8a38b360a75e719fdff5bdccc25591b9e1bb5`, `feedback.sql` `2a587ac2824755f12d3e03f0dde768d3414e89e91c9ad85ac2b4f612b135d3c3`. Live-check AFTER: web 2116/2116, API 122/122, site-only 0 (`B1466_STATUS.md:197`). Wwwroot sha256 AFTER (prefixes only in the record): web `2eed0209...`, API `02ecbef5...`.
- New containers: web `2026-11-10T11:07:43.4577726Z Site started.`, API `11:08:35.7736805Z Site started.`, on images `node:24-lts_20261027.8` and `dotnetcore:10.0_20261027.8` (`:186`).
- PART P PASSED; watchdog `WINDOWS PASSED t+923`; no rollback; database 95 audit rows, `audit_event` APPEND_ONLY_LEDGER_TABLE.
- Two later records change the picture: **B1490 deleted the copy database `hpsmpoc-b1466-pre`** (`Briefs/2026-11-11_B1490_STATUS.md` last line `DONE: B1490 hpsmpoc-b1466-pre deleted 2026-11-10T23:54:29Z; databases now hpsmpoc, master; UAT health 200/200`), so the databases on the UAT server are {`hpsmpoc`, `master`}, and B1466's `rollback1466uat.sh rb1 COPY` is retired. **This kit has no schema step and never uses that script.**

**Whether UAT still runs `PREV` is UNMEASURED by the drafter** (no `az`, no HTTP to any hosted host). The instruments are REFUSE 2 and PRE-DEPLOY SIGNAL 3. **If UAT is not on `PREV` (a different BUILD_ID or active deployment id): STOP, because someone else deployed.** The deploy-STATUS listing (`for f in 'Briefs/'*STATUS.md`, last non-blank line begins `DEPLOYED`, `ROLLED BACK` or `PARTIAL`) read by the drafter at 13:1x AEDT 2026-11-12, newest last: B1391, B1454, B1460, B1466 (a shell loop over every `Briefs/*STATUS.md` printing the last non-blank line when it begins with those words; B1490's last line is `DONE:`, not a deploy; the B1507 to B1539 STATUS files end in `READY`, `RECORDS COMMITTED` or prose).

**Drafter's own measurements (MEASURED, read-only).** All by `gh api -X GET` under the project `GH_CONFIG_DIR`, plus read-only `shasum`/`ls` on this volume. Clocks are from `date`, 13:09:17-13:30 AEDT 2026-11-12. Raw JSON in the drafter's work folder `fleet/state/s272/d1540/`.
- `branches/main` = `c717ba1a945191ffa31f13320c19967a6cf7f15a` (13:10:02). Open PRs: 0 (13:10). **The messaging change is NOT on main yet:** branch `b1535/hpsmpoc-messaging-alignment` = `9308afa0c18f4f368b934145244036595e9fb813` (3 commits, ahead 3 / behind 0 of main, 24 files, +199/-151, `compare main...<branch>`). **The minimatch branch `b1538/hpsmpoc-minimatch-alert-9` does not exist on origin yet** (`branches/...` 404 at 13:1x; its kit says exactly two paths, `web/package.json` and `web/package-lock.json`).
- **The last UAT deploy and what is on main since it.** `compare 009421a2...main`: ahead 5, behind 0, **5 commits, each with ONE parent, linear; 28 files, +696/-36**. None of the five is on UAT: the records hold UAT closed since the hold of 2026-11-06 (see HOLDS FOUND).

| Commit | PR | PR head (merged) | Gate first line (`tuesday/briefs/2026-11-11_B<n>_verify/VERDICT.md`) | Paths (P = product, T = test) |
|---|---|---|---|---|
| `b34046d1` | #310 | `15be8814` | `GATE B1507: GO WITH FINDINGS @ 15be881 on main 009421a` (head = landed) | P `api/src/HpsmPoc.Modules.Assessment/HpsmPoc.Modules.Assessment.csproj` (Pkcs pin 10.0.14 to 10.0.15) |
| `448dc395` | #311 | `a2461ce7` | `GATE B1503: GO WITH FINDINGS @ a2461ce on main 009421a` (head = landed) | P `web/src/app/globals.css`, `.../partner/TrainingScreen.tsx`, `.../partner/parts.tsx`; T `infra/tests/test_ci_workflow.py`, `TrainingScreen.test.tsx`, `parts.moreLink.test.tsx`, `ui/Button.test.tsx` |
| `51b5a21e` | #309 | `0ccb1ec1` | `GATE B1497: GO WITH FINDINGS @ 4f084fb on main 009421a` (**gated head is NOT the landed head**) | P `.../customer/ApiSteps.tsx`, `.../customer/FindingDetail.tsx`, `.../playbook/PlaybookShell.tsx`, `web/src/content/walkthrough/steps.ts`; T 7 files |
| `c014503d` | #312 | `43a06592` | `GATE B1496: GO WITH FINDINGS @ 40217c1 on main 009421a` (**gated head is NOT the landed head**) | P `.../customer/remediation-store.ts`, `.../screens/RoadmapScreen.tsx`; T `remediation-store.test.ts`, `RoadmapScreen.register.test.tsx` |
| `c717ba1a` | #313 | `b6ab804a` | `GATE B1519: GO WITH FINDINGS @ b6ab804 on main c014503` (head = landed) | P `README.md`, `global.json` (SDK 10.0.401 floating to 10.0.404 exact, `rollForward` disable), `scripts/showcase.sh`; T `PkcsInPackageTests.cs`, `infra/tests/test_sdk_pin.py` |

  - PR numbers from `commits/<sha>/pulls`; gate lines are `head -n 1` of the VERDICT files (printed 13:1x). Majors by the `| <id> | Major` rows of each VERDICT: 0 in all five (Minor rows 4, 3, 5, 3, 4; control: the same pattern counts the Minor rows).
  - **The drafter could NOT prove #309 and #312 landed as gated.** `compare 4f084fb3...0ccb1ec1` reads ahead 4 / 8 files and `compare 40217c19...43a06592` reads ahead 5 / 19 files, because the landed heads sit on a newer base than the gated ones (the gate lines say "on main 009421a"; the heads were rebased onto later main). The seat proves it by the PR's own diff at each head (see the Closed-list proof). Q-3.
  - **Words in the five (MEASURED by reading all 28 patches):** ONE customer-visible text change, `steps.ts` step `offers` title "Service offers: Assess / Implement / Optimize" -> "Delivery phases: Assess / Implement / Optimize" (a comment cites the product owner's 2026-11-11 ruling). The rest is layout classes, a landmark (`<main id="main">` moved to wrap the top line and the page, PlaybookShell), an accessible region name "Evidence behind this finding" (a `TableScroll` label; the same string was the hidden caption), a longer-link tap height (`min-h-11`), the register's starting owner cut at the field limit (logic, no text), and a Training step-badge style.
- **Schema (MEASURED).** The schema regex `Migrations|Persistence|\.sql$` over the 28 paths reads **0** (control: a planted `.../Migrations/X.cs` reads 1). **Tree compare:** all 109 blob paths matching the regex have the same blob sha at `009421a2` and `c717ba1a` (from `git/trees/<sha>?recursive=1`, `truncated` false both, 1524 vs 1528 blobs; blob paths differing: 28 = the 28 files; control: a planted extra path makes the sets unequal). The newest migration ids are `20261110003228_LedgerAuditAndFollowUpRetention` (SqlServer) and `20261110003229_...` (Sqlite). **No migration in the range.** The messaging branch adds none either (its 24 files match the regex 0 times). **The API package at `c717ba1a`** (the CI artifact `deploy-api-c717ba1a...` id 13848431501 of run `43003397930`, downloaded by GET to the drafter's folder): `assessment.sql` `03f1afb3...` and `feedback.sql` `2a587ac2...` **equal PREV's** (both digests above); `files` 122 = PREV's 122, only-new 0, only-prev 0; differing 14 = 5 `HpsmPoc*.dll` + their PDBs, `System.Security.Cryptography.Pkcs.dll` (x2: root and `runtimes/win/lib/net10.0/`), and the two non-DLL files **`HpsmPoc.Api` (the app host) and `HpsmPoc.Api.deps.json`, whose diff is exactly the Pkcs version 10.0.14 -> 10.0.15, its fileVersion 10.0.1426.52326 -> 10.0.1526.53008 and its package hash/path lines** (`difflib` unified diff of the two `deps.json`, 6 hunks). So B1466's package property "every non-DLL/PDB file equal" does NOT hold unchanged; this kit's version (Package checks) allows exactly those two files. The messaging branch adds one more code change in the API: `ReportModelBuilder.cs` (the PDF tier sentence).
- **Deploy tooling (MEASURED).** `scripts/deploy-from-ci.sh` blob `0024302d1ea35f...` and `scripts/deploy-package.py` `77dc49939859ab...` and `.github/workflows/ci.yml` `06402836c6cfa7...` are **byte-identical at `009421a2` and `c717ba1a`** (`contents?ref=`, blob shas). The script at `c717ba1a`: 109 lines (sha256 prefix `5688b48e155d1694`), `:25` `set -euo pipefail`, `:49` the green-run predicate (`gh run list ... --workflow ci.yml --branch main --commit "$sha" --status success`), `:68` and `:69` the two `az webapp deploy ... --type zip --async false --clean true` lines (web, then API), `:89` its own `az webapp show` live-check line. `global.json` blob `163a6e14...` -> `89ddff24...` (SDK pin; affects the CI build only; `dotnet`'s shared runtimes on this machine are `Microsoft.NETCore.App` and `Microsoft.AspNetCore.App`; the SDK pin only blocks `dotnet build/run` from source in a clone of main, which this kit never does).
- **CI at `c717ba1a`** (13:1x): push run `ci` **`43003397930`** completed/success; `Push on main` (CodeQL) **`43003397326`** completed/success; 22 check-runs, 21 success and 1 skipped (`dependency review (pull requests; blocks on high/critical)`); open code-scanning alerts on main **0** (control: state `fixed` reads 1). Artifacts `deploy-web-c717ba1a...` (id 13847767403, 16,558,982 B, expires 2026-11-18T10:37:35Z) and `deploy-api-c717ba1a...` (id 13848431501, 49,716,186 B, expires 2026-11-18T10:43:45Z) read `expired=false`. The values at `TARGET` differ and are the seat's to measure.
- **The way back (code), MEASURED 13:1x:** `.tools/b1466/target/` holds `PREV`'s packages: `web/web.zip` sha256 `9d6bb36cf20f4eaa244ed6774c416ce0ceafb79ec150451378978be0dbede19f` (16,558,555 B), `api/api.zip` `1fd65b62...f9ec` (49,644,626 B), `RUN` `42773429652`; `assessment.sql` and `feedback.sql` beside them. PREV's CI artifacts read `expired=false` and expire **2026-11-17T07:24:32Z (web) / 07:26:23Z (API)**. The `.tools/b1466/rollback/` folder holds `6b0c5f2c`'s packages (B1460's PREV): **NOT this run's way back.**
- **The working set at `.tools/b1466/` (MEASURED by `shasum`/`wc -l`, 13:2x):** `identity_pass1466.sh` `edd7ef05` (19 lines), `presig1466.py` `71fc0dac` (200), `live1466.py` `9a7c5f6f` (54), `pkgcmp1466.py` `a6375308` (217), `lits1466.cjs` `95b118d7` (40), `words1466.py` `08a8624d` (143), `walk1466.cjs` `4c971633` (375), `cmpwalk1466.py` `45bda34b` (106), `pairseed1466.py` `77373cfc` (110), `webpair1466.py` `6100b350` (55), `deploy1466.sh` `740088c5` (47), `closedlist1466.py` `e3ed3d3d` (74), `cfgkeys1466.py` `979db24a` (17), `partf1466.cjs` `ae784da8` (75), `pfplant1466.py` `dfa70b44` (42), `lib1466.sh` `2419dab4` (34), `rollback1466uat.sh` `8a7df541` (60; **NOT ours: it restores the database**). **`walk1466.cjs` and `cmpwalk1466.py` read different from the digests B1466's STATUS printed (`c1c49fa8`, `0edacfe2`): they were edited after that line.** The seat copies by name, `cmp`s, and records the digests it got.
- **The words list the builder worked from:** `.tools/b1535/frozen.jsonl`, 52 lines, sha256 prefix `d0061038` (keys `id, cls, file, lines, n, old, new`; ids `M1 S1 S2 S3 H1 H2/H4 H3a H3b H5 P1 P2 P3a P3b P4 P5a-P5d W1-W6b W8-W10 W12-W14b W15-W17 W18a-c W19a-c R1 R3 R5a R5b V1 H6a P6 W7 W11 R2 R4`; files: `steps.ts` 25, `phase-flow.ts` 8, `PartnerDashboard.tsx` 6, `SignInScreen.tsx` 3, `PhaseFlow.tsx` 2, `RecommendationScreen.tsx` 2, one each in `layout.tsx`, `NextEngagementScreen.tsx`, `RevenueCalculator.tsx`, `RevenueResults.tsx`, `ServicesHub.tsx`, `PrototypeBanner.tsx`). The builder's STATUS (`Briefs/2026-11-12_B1535_STATUS.md`, 148 lines, last line `READY B1535: 9308afa0c18f4f368b934145244036595e9fb813`) reads BUILT for all 52 and HELD H6b (the Illustrative tag's title attribute, needs `parts.tsx`).
- Ports: block **9960-9969** proposed. `lsof -nP -iTCP:9900-9999 -sTCP:LISTEN` read 0 rows at 13:13 (control: all listeners 18). The word-boundary scan of the non-`.pre-` SEAT kits of 11-11 and 11-12 for `99xx` hits 9900-9909 (B1484, B1535, B1538), 9910-9919 (B1536), 9920-9939 (B1537, B1538), 9940-9949 (B1492), 9950-9959 (B1496, B1535); **9960-9969: 0 hits**. Live panes at 13:1x: `%0 tuesday`, `%168 Datasec/HPSM-POC-H161`, `%153 Datasec/MPS-M129`, `%1 fleet-monitor`, and five unnamed. H161 (minimatch builder) is a builder: its kit forbids `az` and any hosted host, so it is not a REFUSE 3 hit; **a PR from it may land on main before Step 0 (D-1)**.
- No `SEAT-D61` file and no `B1540` file existed in `tuesday/briefs/` before the drafter's two files (`ls | grep -c` 0, control: `B1539` reads 3). `.tools/b1540` absent (`ls | grep b1540` no match).

**Fact marks.** MEASURED = this drafter, read-only, as above. RELAYED = quoted from a named file. UNMEASURED = nobody ran it. **Source beats this brief: re-measure at source, and say in STATUS (Corrections) where they disagree.** Every `file:line` pointer here was printed by `grep -n` or `awk NR==n` at drafting; the seat reprints each it cites.

## WHAT THIS KIT IS (read first)
1. **The change is the words.** The product owner's feedback on the HP messaging is built on a branch (52 frozen string edits in 12 web files plus one PDF sentence in the API, and the tests that pin them). This kit ships it to the UAT review copy, with the five earlier landings that sit between UAT and main (their only visible text change is one walkthrough step title).
2. **This is a CODE-ONLY deploy.** B1466's migration, backup copy, API stop, temporary SQL rule and identity script are NOT part of it. **There is no `sqlcmd`, no SQL connection, no firewall write, no `az sql db` write and no `az webapp stop`/`start`.** Step 0 PROVES the no-schema claim (Closed-list proof and BUILD 3) and STOPS if it fails; then a schema step needs a different kit.
3. **"Backup first" in this kit** (slot S14 states the form; Q-4 in the report asks whether Tuesday wants a database copy, default NO):
   - the previous build is kept and PROVEN reachable before anything is written (`PREV`'s two packages, digest-checked, plus their CI artifacts);
   - UAT's CURRENT web and API trees are downloaded read-only (`live1540.py before`) and shown equal to `PREV`'s packages, so the code on UAT is held twice;
   - UAT's app-settings names and value hashes, the active deployment ids and the platform backup facts of `hpsmpoc` (point-in-time window, retention) are read and recorded; the restore point T0 is the UTC minute logged just before the deploy;
   - **no database copy is made** (no data changes; the copy of B1466 cost billed storage and was deleted by B1490), and **no database statement is run.**
4. **Order, fixed.** Step 0 and refuse checks, then BUILD (packages, proofs, words, way back, instruments, local pair), then PART P (BEFORE walk, deploy, AFTER walk), then PART F. **UAT stays UP throughout**: the project script deploys web, then API, each with the platform's own restart; no site is stopped by hand.
5. **Authority (the product owner's words, quoted verbatim; the stamp slot S2 carries the clocks).** The earlier records say UAT is held while HP reviews; **these two messages are the deploy word for THIS change and are read as lifting the hold for it** (slot S13 makes that a ruling, not an inference):
   - the product owner, live board 2026-11-12 10:51: *"please find attached additional feedback to the HP messaging. Please use these and deploy. If anything is not clear, please ask"*;
   - the product owner, live board 2026-11-12 11:21:32: *"messaging mapping looks good. deploy based on this and ticket anything left for later"*.
   - **The standing grant also applies** (`/Volumes/Datasec_DEV/TUESDAY/0_Brain/tasks/EXPIRING-GRANTS.md:23`, the TUESDAY row "push READY Datasec changes to the Composer demo + hosted HPSM-POC without a card", the product owner, typed 2026-10-16, no expiry stated, read again 2026-11-01): *"READY = QA gate at the deployed head + Tuesday's completion check + merged via CodeQL; runbook unchanged (backup, rollback, live check); report each deploy after it lands."* That row also says **"NOT: ... new customer-facing words"**: so the grant ALONE does not cover this deploy, and the two messages above carry the words. READY here = the QA gate passed at the head that landed + Tuesday's check + merged through CodeQL (slots S5, S6, S12).
6. **HOLDS FOUND that the product owner's two messages do not obviously cover (each is a question for Tuesday; this kit does not decide them):**
   - **H-1. The UAT hold itself is still the records' standing reading.** `1_Project_Definition/CLARIFICATIONS.md` of the analysis repository (origin main, 6286 lines at 13:2x): C-300 (`:5648`, the product owner's 2026-11-06 words *"Switch accounts, but leave UAT alone while HP reviews"* at `:5650` and *"yes, hold UAT but work on everything else..."* at `:5652`) says the hold *"has no end date ... ends on the product owner's word and on nothing else"* (`:5655`); and the entries written AFTER B1466 still end *"UAT is held"* (C-363 `:6254`, C-365 `:6275`, C-366 `:6285`). C-366 (`:6280`) records the 11:21 words as *"an instruction to deploy on the map and to ticket what the map leaves; it decides none of the map's held questions."* B1466 deployed on its own words ("go ahead and deploy to UAT", 2026-11-10) and the hold was read as lifted FOR THAT DEPLOY ONLY. **Q-1 (S13): are the 10:51 and 11:21 words read as lifting the hold for this deploy only? Default yes.**
   - **H-2. The five earlier landings (#309-#313) were merged "main only; UAT held" and have never been shown to the product owner on UAT.** Deploying main carries them. Their only visible text is one step title. **Q-2 (S16): do the two messages cover them? Default: yes, they ride, and the words list sent beside the deploy names the step title.** If the answer is no, this kit cannot be used as written (a deploy of a sha that excludes them does not exist on main).
   - **H-3. EXPIRING-GRANTS.md:23 "NOT: new customer-facing words"** (above): covered only by the two messages.
   - **H-4. EXPIRING-GRANTS.md:15** (the 2026-11-06/08 row "UAT untouched while HP reviews", its own text: *"The UAT hold ends on his word (no date given), not by inference"*): same as H-1.
   - **H-5. The held content rows and next-phase items must not appear** (the map's 13 C rows, K2, K3, H6b; the journey rename held by the product owner's 2026-11-10 ruling): checked live, see D-9.
   - **H-6. Whether an HP reviewer is in session on UAT now is UNMEASURED** (nobody can read it). Both apps restart in this window (a few minutes in all, the API's restart longest). Tuesday states in S10 (d) that it accepts this.
   - Project `CLAUDE.md` (51 lines) holds NO UAT hold: `/usr/bin/grep -c -i` over it reads `UAT` 0 and `deploy` 0 (controls: `Coordinator` 1, a no-such token 0). The local `1_Project_Definition/CLARIFICATIONS.md` (192 lines) is stale; the live records are the analysis repository's copy (H-1).
7. **Template and what carries over.** The last executed, PASSED UAT deploys are B1466 (with a migration; `Briefs/2026-11-10_B1466_STATUS.md`, 271 lines; kit `tuesday/briefs/2026-11-10_B1466_SEAT-D59_hpsmpoc-uat-deploy-main-migration.md`, 738 lines) and B1460 (code only; `Briefs/2026-11-10_B1460_STATUS.md`, 320 lines; kit `...B1460_SEAT-D58_hpsmpoc-uat-deploy-main.md`, 636 lines). **Read both kits and both STATUS files WHOLE** (PRIOR WORK). **Inherited unchanged unless this kit says otherwise:** the identity pass before EVERY `az` call; plain ARM GETs, never `az webapp show`; the PRE-DEPLOY SIGNALS and settings-hash compare; D-6 (platform image), D-11 (the non-GET list), D-14 (the review door), D-15 (no PDF), D-16 (customer counts 4/5/5/4 and the id-set hash BEFORE = AFTER); the walk router that ABORTS and counts every non-GET other than D-11's named calls and aborts GET prefetches of `/admin/feedback(/review)` outside PART F; the STATUS-first-line discipline; no names in STATUS; no message to any human.
   **What went wrong or was learned last time, and is carried here (B1460 FOR TUESDAY 5, B1466 Corrections and ADDENDA):**
   - the words extractor must read `${...}` template literals AND JSX text (B1460 5 (c)); plant a JSX phrase first;
   - the walker's empty-state test must exclude the walkthrough panel's text (5 (d));
   - **the favicon route-cache pair (`.next/server/route-cache/APP_ROUTE/<hash>/$/favicon.ico.{body,meta}`) is ALLOWED BY NAME as web site-only in the BEFORE live-check** (5 (e)); any other site-only file = STOP;
   - the panes regex reads "No \`az\`" with a backtick (B1460 Corrections 1);
   - the inherited `#US` check counted the whole DLL; it counts the `#US` heap only (B1466 Corrections 3);
   - **make the kit copy into `Briefs/` at Step 0, not at the end** (B1466 Corrections 5: it was forgotten and made late);
   - no `rm`, no `pgrep -f`, no `echo ===` in zsh (B1466 Corrections 6; B1460 5 (c), (g), (b));
   - a `cd` in an identity-pass line and an `ls` of `4_Credentials/` are slips (B1466 Corrections 4): open nothing but `.azure` and `.gh-config`;
   - **a deploy-time exposure window is NAMED, not hidden** (B1466 ADDENDUM-2/-3): here the window is the platform restart of each app; during the API's restart a request fails; say how long, from the container lines;
   - **B1466's S16 "start the API then deploy" problem does not exist here**: the API is never stopped by hand.
8. **Where the instruments are:** `.tools/b1466/` (listed above, MEASURED). **The seat COPIES what it needs by name into `.tools/b1540/`** (read-only source; `cmp` each copy), renames each to a `1540` name, hand-edits every hex, sha, BUILD_ID, window start and count map (never by `sed`), and runs each copy's plant control before relying on it. It never writes into `.tools/b1466/`, `.tools/b1460/` or `.tools/b1535/`. **NEW in this kit (written by the seat):** `rollback1540uat.sh`, `rollforward-guards` inside `deploy1540.sh`, `wordsmap1540.py` (D-8), `heldabsent1540.py` (D-9).

**What the product owner approved, and what is NOT covered.**
- **Covered:** the CI packages of `TARGET` to the two UAT apps by the project script (web, then API); read-only live checks; the read-only ARM reads named here; the way back (D-7); PART F's read-only feedback count. **Nothing else is written.**
- **NOT covered:**
  - `[PROD-CLASS]` any SQL statement, any firewall rule, any `az sql` write, any copy, restore or rename of a database;
  - `[PROD-CLASS]` any other database, server, group or subscription (`hpsm-poc-rg`, `hpsm-poc-demo-rg`, `hpsm-poc-sm-rg`: never even read);
  - `[PROD-CLASS]` a template deploy or what-if; any app-setting, vault, plan, access write; any web-app stop or restart other than the deploy's own;
  - any hosted-data reset, re-seed or demo-data change; any feedback item created, approved, deleted or moved; any narrative or readiness self-assessment on UAT; customers created, renamed, deleted;
  - deleting anything (quarantine by move);
  - anything after `TARGET`; the held and next-phase rows (D-9);
  - anything to HP or to any human; any claim to HP that a held or next-phase item is done.

**Closed-list proof of what reaches UAT** (re-measured by the seat at Step 0; property first, then "at least these", then "any other shape: prove it or STOP").
- *Property:*
  - `TARGET` is a descendant of `PREV` on main's first-parent line (`compare PREV...TARGET` behind_by 0); every commit in `PREV...TARGET` has ONE parent and was merged by a PR the seat prints with its number, head and gate verdict line;
  - every product path's blob at `TARGET` equals the blob at the head of the PR that changed it (a path shared by two PRs equals the LATER PR's head: **`steps.ts` and `steps.test.ts` are shared by #309 and the messaging PR**);
  - 0 blob paths differ between `PREV` and `TARGET` outside the union of the PRs' files;
  - **schema paths: 0.** `Migrations|Persistence|\.sql$` over the range reads 0; the recursive tree compare of those paths (109 at drafting) is equal PREV vs TARGET (control: a planted path makes it unequal); the package's `assessment.sql` equals `03f1afb3...` and `feedback.sql` equals `2a587ac2...` (any difference = STOP: a schema step needs a different kit);
  - **deploy-tooling paths: 0 beyond the listed:** `.github/` 0; `scripts/` only `scripts/showcase.sh`; `appsettings*` 0; `*.csproj` only the Assessment csproj's Pkcs line; `package*.json` only if the minimatch commit is in the range, and then EXACTLY `web/package.json` and `web/package-lock.json`; `global.json` as listed; `deploy-from-ci.sh`, `deploy-package.py`, `ci.yml` blob shas equal PREV's (`0024302d1ea3...`, `77dc49939859...`, `06402836c6cf...`);
  - **`infra/` paths: only `infra/tests/test_ci_workflow.py` and `infra/tests/test_sdk_pin.py`** (tests, not deployed);
  - NEW configuration keys read by added product lines: listed (`cfgkeys1540.py`); expected none. A new REQUIRED key = STOP;
  - **if the minimatch commit is in the range, it is "dev-only" by PROOF, not by its label:** the web package's `node_modules/` has 0 differences vs `PREV`'s and the package `server.js`/`.next` differ only in chunk/build-id files; the `overrides` entry names a package that is in no production dependency path (the seat prints `npm ls minimatch --omit=dev` from the package's lockfile, or reads the lockfile's `dev: true` flag for every `minimatch` entry; control: a production dependency's entry reads without `dev`). A production-path change = STOP.
- *At least these (drafter's reading at 13:1x):* the 5 commits above (28 paths); the messaging squash (3 branch commits squashed to ONE commit; 24 paths, of which `steps.ts` and `steps.test.ts` overlap with #309; union with the 28 = **50 paths**); optionally the minimatch squash (+2 = **52 paths**). Total commits expected: 6 (7 with minimatch).
- *Controls:* a planted extra path reads 1 differing; a planted `Migrations/` path fails the schema rule; a planted `.github/` path fails the tooling rule.
- **Any other shape** (a commit past these, a second migration, a changed `deploy-from-ci.sh`, `ci.yml` or `scripts/` path other than `showcase.sh`, a new `infra/` path, a Feedback change you cannot place): STOP and list it.
- **Landing proof (REFUSE 4 uses it):** for #309 and #312 (gated head differs from landed head), print the PR's own diff at the gated head and at the landed head (`compare <merge-base-of-that-head>...<head>` per head, then the per-file patches for the PR's own files) and prove the PRODUCT patches equal and the difference is test-only or rebase-only; any product-path difference = STOP with the diff. For the messaging PR: the landed head equals the gated head (`9308afa0...` is the builder's head; Tuesday's S6 names the gated one), or the seat proves the difference is test-only. Landing rule: **head-pinned squash**, quoted by the B1519 and B1538 kits from the analysis repository's `CLARIFICATIONS.md` ("The landing form is a head-pinned squash"); the seat does not land.

**CI at `TARGET`.** The pass predicate is the script's (`scripts/deploy-from-ci.sh:49`; print it with `grep -n -i`).
- The push run `ci` of `TARGET` (slot S5) is `completed/success`, with ALL THREE `api on SQL Server` legs success (a skipped leg = STOP), `infra (Bicep validate)` success (this runs the repo-wide hidden-character scan), every `web e2e` shard success (8 shards), `web build`, `web unit tests (vitest)` success.
- `Push on main` (CodeQL) success. Open code-scanning alerts on main 0 (control: `fixed` >= 1).
- Artifacts `deploy-web-<TARGET>` / `deploy-api-<TARGET>` read `expired=false`. Never re-run CI; never dismiss an alert.

**Identity and tenant (workspace rule 4; records, not assumed).** RELAYED from `B1466_STATUS.md:89` and `B1490_STATUS.md` (Identity pass):
- `IDENTITY PASS ... sub=a6b8fe11-d1b5-4293-8727-b34aba08a705 tenant=ec01829b-fdcb-4503-9834-eb2ffbd99169 name='Azure subscription 1' user=...@datasec-rd.com`;
- `AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.azure'`; `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config'`;
- which of the five Datasec environments this tenant is: NOT ASSERTED.

Rules:
- **`identity_pass1540.sh` (a `cmp`-checked copy of `identity_pass1466.sh` `edd7ef05`) runs before EVERY `az` call.** Control: `AZURE_CONFIG_DIR=/nonexistent` fails rc 2.
- `4_Credentials/.azure-sp` is never opened; `4_Credentials/` is never listed. An expired interactive login = STOP and ask.
- **Any authorization error is the boundary working: STOP and report it.** Never `az account set`, never work around it, never ask for a broader right.
- **Never `az webapp show`.** The project script's own live-check line (`deploy-from-ci.sh:89`) is the only exception. Use plain ARM GETs (`az rest --method get` on the site's resource id) and test the form against the activity log first (the log must show no new `publishxml/action` row from your reads, B1319).

**CLOCK.** Hard stop = Step 0 + 120 minutes (slot S3), written by you as an absolute AEDT clock at Step 0. No write START after it (the deploy counts). DONE no later than Step 0 + 150 minutes. Step 0 within 45 minutes of slot S1. **The only write class is the deploy (D-2); the cut-off applies to its START.**
- CHECKPOINT lines with `date`, in this order: Step 0 | CI green | package checks | words gate | rollback point taken | local pair | DATABASE STILL AWAKE (before) | UAT BEFORE walk | UAT deploy START | PART P PASSED | DATABASE STILL AWAKE (after) | PART F DONE | DONE. At every CHECKPOINT print the minutes left to the write cut-off.
- A write that has started is not killed. A way back that must start, starts within 60 s.
- **If anything is in doubt BEFORE the deploy START, leave UAT as it is and end `STOPPED: NEEDS TUESDAY <reason>`.**
- **Context band and handover.** If the kit's work may not fit one window: at about 70% context start no new part; at about 75% stop at a safe boundary (files whole, processes stopped by pid, ports free) and write `2026-11-12_B1540_HANDOVER.md` in the project's `1_Project_Definition/Briefs/` with sections done / in hand / next / processes left / decisions a successor keeps, and last line `HANDOVER B1540: next <part> <step> | done <parts>`. **Never hand over across the deploy START: finish or way-back first.**

**Model route.** Opus, `BRIEF_SEAT_LEVEL=opus`, model id `claude-opus-5-5`. Row C6 "Deploy" of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md:96` (printed by `awk NR==96`: the Opus column reads **1st** for a deploy; "Production is P1"); the id is the `opus` entry of `/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json` (`:17` `"model_id": "claude-opus-5-5"`, `:37` `"opus": "claude-opus-5-5"`). B1466's kit (`:202`) used the same row. STATUS quotes the `brief_seat: model=` line or says none was shown. **Never run /model in this pane.**

**This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only.** UAT feedback delivery is OFF (`Feedback__Route` `off`; re-read at Step 0). This seat sends and approves nothing.

## DRAFTER DECISIONS (D-n; Tuesday accepts or changes them at the stamp; the defaults apply if Tuesday is silent, except where a slot is REQUIRED)
- **D-1: PIN `TARGET`.**
  - At Step 0, `gh api -X GET branches/main` must equal S4. **If main at Step 0 differs from S4: STOP at once** (`STOPPED: NEEDS TUESDAY main moved to <sha>`), whether the newer commit is the minimatch change or anything else, because the closed list was proved for S4. No "deploy S4 anyway".
  - S4 not 40-hex, or `TARGET` not a descendant of `PREV`: STOP.
  - **The range may contain the minimatch commit** (a dev-only lockfile override that may land before or after the messaging squash). The seat lists EVERY commit from `PREV` (exclusive) to `TARGET` (inclusive) by program with its number, PR, head, gate line and EVERY path with +/-; a commit not in S6 or S12 = STOP.
  - After Step 0, if main moves past `TARGET`, deploy `TARGET` anyway and record it.
- **D-2: The write class, named, and only this one:** (w1) the project script's two `az webapp deploy` lines (`deploy-from-ci.sh:68-69`; web, then API; `--type zip --async false --clean true`); (w2) the D-7 way back if it fires (the same two lines with `PREV`'s zips). Nothing else: `[PROD-CLASS]` no what-if, no `az deployment`, no `az sql`, no stop/start/restart by hand, no app-setting, vault, plan, access or firewall write, no SQL connection.
- **D-3: Both packages, through the project script** (web, then API). The API restarts with NEW code (Pkcs 10.0.15 in the package; the PDF tier sentence). Whether an HP reviewer is in session is UNMEASURED; Tuesday states it in S10 (d).
- **D-4: Temporary access: NONE.**
  - No SQL firewall rule is opened. **Proof:** the SQL server's firewall list is exactly `AllowAllWindowsAzureIps` BEFORE and AFTER (ARM GET), and the activity log since Step 0 holds 0 `firewallRules/write` and 0 `/delete` rows (control: B1466's window had 2+2; the same query over `2026-11-10T11:03:00Z` to `11:06:00Z` is not re-run, quote `B1466_STATUS.md:198`). No `sqlcmd` binary is downloaded, and none exists in `.tools/b1540`.
- **D-5: THE DATABASE STAYS AWAKE (read-only).**
  - RELAYED baseline, B1466 W5 (`B1466_STATUS.md:203`): `status` Online, `autoPauseDelay` -1, `useFreeLimit` False, `pausedDate` None, `GP_S_Gen5` capacity 2, `minCapacity` 0.5, `maxSizeBytes` 34359738368; `databases/pause` since 2026-11-01T00:52:35Z **0** (control window 2).
  - Read by plain ARM GET before the window and after PART P. Any difference = STOP before the next write (before) / a finding (after). Databases on the server exactly {`hpsmpoc`, `master`} (B1490); a leftover `hpsmpoc-b1466-*` = STOP.
- **D-6: Platform-image rule, both UAT apps, as B1460 D-6.** The baseline is the Step 0 reading. RELAYED: web `NODE|24-lts` / `node server.js`; API `DOTNETCORE|10.0` / empty command line; images as above; active deployments `648087d4-...` (web) and `63357c6f-...` (API).
- **D-7: THE WAY BACK (code only; `rollback1540uat.sh`, written at BUILD 4, stub-run, never run unless a case fires).**
  - **RB-A (a deploy failure, a slot-S9 class, or a health window missed):**
    1. `az webapp deploy` `PREV`'s two packages from `.tools/b1540/rollback/009421a28616c8b31dde86b59d4c4ca674c288fa/` (web, then API), `--type zip --async false --clean true`, on the STARTED sites;
    2. wait for the API `/health` 200 and `/health/ready` 200 and the web `/api/health` 200;
    3. live-check against `PREV`'s packages (web 2116, API 122), BUILD_ID `NQga609FQ4iKZFwQ1rtsT` x1;
    4. D-5 (autoPauseDelay -1, Online);
    5. `ROLLED BACK`.
  - **There is no database step in any way back** (nothing was migrated; the copy is gone; B1466's RB-1/RB-2 do not apply). **The migration's `Down` never runs.**
  - `rollback1540uat.sh` guards before ANY `az` call: `repo-prev` HEAD = `PREV` (rc 96); `PREV`'s zip sha256 `9d6bb36c...` / `1fd65b62...` (rc 97); the group is exactly `hpsm-poc-uat-rg` and the sites are exactly the two UAT names (rc 95); the identity pass before each `az` call (rc 2).
  - Rows written by the walks between the deploy and the rollback (sign-in bookkeeping) are NOT lost: no database is restored.
- **D-8: THE WORDS GATE (a closed list by STRING).**
  - *Property:* every customer-facing string that is new or changed between `PREV` and `TARGET` is one of: (i) a `new` string of `frozen.jsonl` (52 lines), at the `file:line` re-printed at `TARGET` (the file is copied to `.tools/b1540/frozen.jsonl`, `cmp`-checked against `.tools/b1535/frozen.jsonl` `d0061038`); (ii) the step-title change "Delivery phases: Assess / Implement / Optimize" (`steps.ts`, #309); (iii) a string the seat lists with its reason from the earlier landings and the seat classes CODE or LAYOUT (a class name, a comment, `EVIDENCE_CAPTION`'s accessible name "Evidence behind this finding").
  - *Rules:*
    - **the `old` -> `new` mapping is applied, not only listed:** for each frozen row, `old` is absent and `new` present at `TARGET` on the stated lines (`wordsmap1540.py`; control: a planted row whose `old` still exists reads FAIL);
    - **`old` strings must read absent from every rendered page** (BEFORE-vs-AFTER, D-12), except where the row says the comment or a test fixture keeps it;
    - the `new` text equals the frozen text byte for byte, including the typographic characters it holds (U+2019 and U+2192, U+2014 where the row holds it; no code point outside U+2014, U+201C, U+201D, U+2019, U+2192, U+2022 net added; control: a planted U+00A0 and U+202E fire).
  - Use `words1540.py` = a copy of `words1466.py` (template literals and JSX text read) over the ADDED and REMOVED lines of every product path of the range; plant first (a phrase planted as JSX text into an in-memory diff must be listed OTHER, rc 1). **Any new customer-facing string not in the closed list = STOP before any hosted write**, listed with its `file:line`.
  - **The words sent to the product owner beside the deploy** are exactly the frozen `new` strings plus the step-title change (slot S11). STATUS lists EVERY new or changed string: file, `file:line` at `TARGET`, string, OLD text, the frozen id. Underscore-aware person-name scan (D-8 of B1460; tokens from `.tools/b1390/scripts/drive.mjs:90`, read in-process, never printed; pattern `(?<![A-Za-z])<name>(?![a-z])`; control: a planted `_by_<name>_` fires).
- **D-9: HELD AND NEXT-PHASE ITEMS ARE NOT VISIBLE (a closed check; `heldabsent1540.py`).**
  - *Property:* UAT shows nothing the product owner has held or put in the next phase. The held rows are the map's 13 C rows (`C-landing`, `H-hero`, `C-rename`, `C-training`, `R6`, `R7`, `C-modes`, `C-phase3`, `C-gbb`, `C-stages`, `C-metrics`, `C-coach`, `C-deck`), the D rows `K2` and `K3`, and `H6b` (map `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_hpsm-messaging-map.md`; Jira HPSMPOC-471 to -477 per `Briefs/2026-11-12_B1539_STATUS.md`).
  - *At least these checks (each with a control that can fail):*
    - **no new page route:** package page routes `TARGET` = `PREV` (58 = 58 in B1466; added 0, removed 0);
    - **the eight-step journey labels equal BEFORE** (the rename is held): `customer-nav` labels read on a customer page, BEFORE = AFTER;
    - **`Phase 3 - Managed service`** (page title at `/services/managed`) and the three delivery models "Partner delivered / Co-delivered / Referral" still read as BEFORE (C-phase3, C-modes);
    - **no Good / Better / Best packages page and no "operating mode" page text:** no AFTER page or route text contains "Good / Better / Best" or "operating mode" that BEFORE did not (the PDF/tier sentence R2 names "Tiers" only);
    - **the report keeps its cover "Security Assessment" and its section list** (no introduction, no change to "Next Engagement"; only visible if the report step's page is VIEWED; D-15 forbids a PDF);
    - **the coach lead** at `ConversationCoach` equals BEFORE; **the deck's own sentences** (`content/packages/`, `content/client/`, `SeedContent/`) are byte-equal in the package vs `PREV` (these paths are 0 in the range; the web package's content JSON files equal);
    - **the attribution preview** keeps its "next phase" / sample labelling as BEFORE;
    - **no HP-integration wording shown as done:** the P6 line "Tools named here are planned or subject to implementation until release validation is complete." reads once under each of the three "Tools / assets" headings on Home (D-9 reads it; this is a frozen row); the strings "Security Manager API", "Fleet Threat Assessment", "SIEM" on Home appear only inside the tool lists as BEFORE (the P6 row keeps them under the planned line).
  - Any held or next-phase item visible = a slot-S9 class (`ROLLED BACK` with the text and where).
- **D-10: Jira and records: this seat writes none.** STATUS lists the Jira keys the PR titles and squash subjects name (the drafter measured none in the five subjects).
- **D-11: No data written on UAT by the seat's own actions,** as B1466 D-11 / B1460 D-11. The only non-GET calls to UAT web/API are the sign-in POSTs, the sign-out POSTs and the two refused probes (403 `uat.action-off`), all COUNTED. Never click "Start a self-assessment". Never create, rename or delete a customer. Never open a feedback page's controls. **No SQL at all** (there is no SQL runner in `.tools/b1540`; a planted SQL string is not run).
- **D-12: Every page, BEFORE vs AFTER: the differences are CLOSED by the words list.**
  - Read BEFORE and AFTER at 1440 x 900 and 390 x 844 as Partner, Consultant, Admin and Demo (B1466 walk, `walk1540.cjs`), and the two walkthrough walks (14 steps each).
  - **Allowed AFTER differences (the property):** the visible text of a page AFTER equals its BEFORE text with the `frozen.jsonl` `old` -> `new` substitutions applied for that page (and the step-title substitution), nothing else. **The mechanical check:** apply the substitutions to the BEFORE text of each walked page IN PROCESS and compare with the AFTER text (the builder did exactly this locally: `mechanical == rendered` for Home in both states, B1535 STATUS PRIOR WORK). Any residue is listed with page, level, width and the diff; residue not explained = STOP (slot-S9 class).
  - *At least these pages differ (SEEN, per D-13):* Home (Partner level; Home for each level that shows the dashboard), the walkthrough cover and steps 1, 2, 3, 8, 12, 13, 14 and the bridge cells of steps 12 and 13, `/customers/<sample>/recommendation` (R1), `/customers/<sample>/next-engagement` (R3), `/revenue` (R4, R5a), `/revenue/results` (R4, R5b), `/services` (V1), the document `<meta name="description">` on every page (M1).
  - **Structure, AFTER (from #309 / #311 / #313), not text:** each signed-in page has exactly ONE `main` landmark (count 1; BEFORE the same count may be 1 with a different wrapper; print both); the finding detail's evidence table sits in a region named "Evidence behind this finding" where a finding with evidence is reached; the layout boxes may differ only in these places: the Training steps band, the header/tap links with `min-h-11`, the walkthrough bridge cells and the Home phase boxes (longer lines wrap; **no horizontal scroll that BEFORE did not have**, a slot-S9 class).
  - The runner and results pages of the readiness hub (D-12 of B1460), customer counts 4/5/5/4, the id-set hash, security views, refusals and the review door are EQUAL BEFORE and AFTER.
- **D-13: The change is proven live by measurement, not by assertion.** The SEEN table and the words, read in a real Chromium, GET-only navigation, at 1440 and 390: see PART P, P3 (e). Every frozen id that is reachable on UAT is read as `new` found / `old` absent; unreachable ids are named with the reason (R2 renders only on a scored result with tiers: where UAT's sample result shows it, read it; the PDF sentence is NOT shown: D-15).
- **D-14: The review door is NOT re-tested and NOT broken** (B1460 D-14, status only).
- **D-15: No live PDF.** The report step's page is VIEWED only. The API's PDF tier sentence (R2, `ReportModelBuilder.cs`) is proven by the live API DLL `#US` heap holding "Tiers are options informed by risk and scope" x1 (UTF-16LE; control: a no-such string x0), not by opening a PDF.
- **D-16: Hosted data is not reset,** as B1466 D-16 (customers 4/5/5/4; id-set hash BEFORE = AFTER). A removed or replaced row = rollback class. **No audit-row census by SQL**: the API's own reads only (the M1 probe below).
- **D-17: PART F, the UAT feedback store, READ-ONLY, after PART P PASSED.** The B1466 PART F procedure and controls exactly (`partf1540.cjs`, a copy of `partf1466.cjs` `ae784da8`). Print only the total, the counts by category and by state, the held count, and **the items newer than B1466's PART F read (2026-11-10 22:23 AEDT)** with the D-17 table for those items only (B1466 read 9 items, 0 held, 0 new since 2026-11-10 11:04:40 AEDT). No screenshot of either feedback page. `.tools/b1540/fb/*.json` mode 600, never in `Briefs/`.
- **D-18: The Pkcs pin shipped in the API package** is verified by the live-check (D-13): the live `System.Security.Cryptography.Pkcs.dll` bytes equal the package's (file version 10.0.1526.53008 at `c717ba1a`; the seat prints the value read at `TARGET` and the package's `deps.json` line). It changes how the API signs; nothing on UAT exercises it by a request this kit makes; say so in NOT TESTED.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, no other step; each count with a control that can fail)
- **FIRST STEP: the way back is reachable.**
  - Copy `PREV`'s packages from `.tools/b1466/target/{web,api,RUN}` by name, read-only, into `.tools/b1540/rollback/009421a28616c8b31dde86b59d4c4ca674c288fa/`.
  - `shasum -a 256` + `stat -f %z` must give web `9d6bb36cf20f4eaa244ed6774c416ce0ceafb79ec150451378978be0dbede19f` (16,558,555 B) and API `1fd65b623d3665568e50a2615d25d3f4e5936880355a4f93a1f2e65dc574f9ec` (49,644,626 B), file counts 2116 / 122, both `MANIFEST.json` `commit` = `PREV`, `RUN` = `42773429652`, and `assessment.sql` `03f1afb3...` (MEASURED by the drafter on the source copy at 13:1x for the two zips and RUN; the file counts and manifests are RELAYED from `B1466_STATUS.md:74`).
  - If absent or unequal, rebuild by `scripts/deploy-from-ci.sh fetch PREV` from a clean detached clone at `PREV` (its artifacts expire 2026-11-17T07:24:32Z / 07:26:23Z).
  - Digests unequal or artifacts expired: `STOPPED: NEEDS TUESDAY no proven way back`.
- **The last UAT deploy.**
  - `tail -n 1 'Briefs/2026-11-10_B1466_STATUS.md'` begins `DEPLOYED B1466: 009421a28616c8b31dde86b59d4c4ca674c288fa` (control: a scratch file ending `DEPLOY B1540: PENDING` counts 0 for `^DEPLOYED `).
  - The deploy-STATUS listing names no UAT deploy newer than B1466, and no `ROLLED BACK`/`PARTIAL` line newer (a newer one: read it whole; unexplained = STOP).
  - **Which build is live (UNMEASURED by the drafter):** public `GET /` names `NQga609FQ4iKZFwQ1rtsT` x1, and the live trees equal `PREV`'s packages (web 2116/2116 with only the favicon pair allowed site-only; API 122/122, site-only 0). Any other build = STOP.
- **Panes.** As B1460 REFUSE 3 (with its Corrections 1 regex). It fires ONLY on another `Datasec/HPSM-POC-D*` pane, or any pane whose kit lets it call a hosted HPSM-POC host or `az`. A builder pane (H161) whose kit forbids both does not fire. At drafting: 0 HPSM-POC-D panes. Re-list immediately before the deploy START.
- **The target.**
  - S4 is 40-hex and equals `branches/main` at Step 0 (D-1). S5 is numeric. S12 lists every PR number in the range, in merge order, and includes `309 310 311 312 313` and the messaging PR.
  - For every PR in S12: `merged` true; `merge_commit_sha` on main's first-parent line in `PREV..TARGET`; `head.sha` printed; check-runs on the head all success (control: a no-such PR 404).
  - Gate verdict lines printed (`head -n 1` of each VERDICT file named in S6). Each must read `GO` or `GO WITH FINDINGS` at the head that landed, or the Landing proof above shows the difference to be test-only or rebase-only. S6 carries each gate's open findings by id. **A Major in any gate's FINDINGS that S6 does not carry = STOP.** The messaging PR's gate line is in S6 (the drafter could not read it: no gate existed at drafting).
- **CI at `TARGET`.** As above; equal to S5 or another green run of `TARGET` (say which).
- **Stamp slots.**
  - `/usr/bin/grep -o -E '_{4}' <your copy> | wc -l` reads 0 (control: a five-underscore scratch file >= 1). The last line begins `READ-WHOLE-BY-TUESDAY: DONE`.
  - S7 is exactly `CODE ONLY; NO DATABASE WRITE; NO API STOP; BOTH PACKAGES; NO SQL RULE; NO WHAT-IF; NO TEMPLATE DEPLOY; NO APP SETTING WRITE; NO DATA RESET`.
  - S8 is exactly `UAT ONLY`.
  - S10 holds `CONFIRMED` for (a)-(g), with no `NOT CONFIRMED` and no `UNSET` in the VALUE part (count over the value part only; B1460 Correction (d)).
  - S11 is exactly `UAT WORDS: THE CLOSED LIST OF D-8, READ BY THE PRODUCT OWNER` or exactly `UAT WORDS: THE CLOSED LIST OF D-8, SENT TO THE PRODUCT OWNER BESIDE THE DEPLOY` (or `HOLD`: STOP at once).
  - S13 is exactly `UAT HOLD LIFTED FOR THIS DEPLOY ONLY: ACCEPTED`.
  - S14 is exactly `CODE BACKUP AND RESTORE POINT READ; NO DATABASE COPY`.
  - S15 is filled with text.
  - S16 is exactly `THE FIVE EARLIER LANDINGS 309-313 RIDE THIS DEPLOY: ACCEPTED`.
  - Anything else: STOP.
- **Clock.** Later than 45 min after S1, or fewer than 75 minutes to the write cut-off at Step 0: STOPPED ("not enough time").
- **Identity.** As above. PRIOR WORK is read WHOLE before the first `az` call.
- **Names, settings, route** (UNMEASURED today; RELAYED from B1466 PHASE 0 / `B1466_STATUS.md:90`). All read in-process; print only yes/no or the name list.
  - Sites exactly {`app-hpsmpoc-api-uat-25onzn`, `app-hpsmpoc-web-uat-25onzn`}.
  - SQL server exactly `sql-hpsmpoc-uat-25onzn`; databases on it exactly {`hpsmpoc`, `master`}; SQL firewall exactly `AllowAllWindowsAzureIps`; the Entra admin is the group `sg-hpsmpoc-sql-admins` (object id `c8f8b814-b85f-4b97-a390-cec81be1c64c`) and `azureADOnlyAuthentication` true (ARM GET only; nothing is changed).
  - Setting names API 35 / web 17, value hashes `fa62b3968883ca61` / `fe5590fba73ea35f` (comparable only with the same `h16`: say so). **`Feedback__Route` exactly `off`.** `Assessment__MigrateOnStartup` absent. `Assessment__Environment` and web `HPSM_ENVIRONMENT` exactly `uat`. `Auth__UatOpen__Enabled` `true`. `HPSM_DEMO_NOTICE` `off`. `HostedDemo__Seed__Enabled` true and `__OwnerObjectId` present.
- **Platform backup facts (read-only):** `earliestRestoreDate` at least 24 h older than now; short-term retention days (B1466: 7); LTR none; backup storage redundancy Local/Local (`az sql db show`, `az sql db str-policy show`, `az sql db ltr-policy show`, plain ARM GETs). Missing or younger than 24 h = STOP (no restore is made; the facts are the record).
- **Ports.** Block **9960-9969** (or the block Tuesday names in S10 (e)). Re-run `lsof -nP -iTCP:9960-9969 -sTCP:LISTEN` (expect 0) and a word-boundary scan of the non-`.pre-` SEAT kits of today and yesterday just before the first listener; take the next free 10-block if a live claim appears. Bind `127.0.0.1` only.
- **Live seats and trees.** `.tools/b1540` was absent at drafting (MEASURED); anything there you did not make: STOP. `.tools/b1466`, `.tools/b1460`, `.tools/b1535` are read by name only.

## PRE-DEPLOY SIGNALS (UAT; read ALL before the deploy START and before any way back; `presig1540.py` = a copy of `presig1466.py` `71fc0dac` with its SQL-level reads removed or turned into plain ARM GETs; plant controls first)
1. Both sites Running, HTTPS only, `alwaysOn` true; stacks as D-6 (plain ARM GET).
2. App-setting names, value hashes (in-process) and slot flags: API 35 / web 17 (summaries RELAYED from B1466 W4 = `fa62b3968883ca61` / `fe5590fba73ea35f`). KV references `Resolved`, except the two feedback webhook references `SecretNotFound` (pre-existing since B874).
3. Active deployments web `648087d4-f9ab-44cc-9e69-11b37f2d9440`, API `63357c6f-6490-4752-aadf-425c93c6c47b` (RELAYED); none in progress.
4. Platform lines newer than B1466's containers (web 2026-11-10T11:07:43Z, API 11:08:35Z): none, except as D-6 allows.
5. The ARM activity log of the group since **2026-11-10T11:15:48Z** (after B1466's last write, the read-back rule's delete at 11:15:47Z; the B1490 delete at 23:54:13Z-23:54:29Z is the only row expected: one `Microsoft.Sql/servers/databases/delete`), with BOTH `--start-time` and `--end-time`: restart / stop / start / config-write / sites-write / deployment counts 0; `publishxml/action` reads listed; SQL `databases/pause` since 2026-11-01T00:52:35Z 0; SQL `firewallRules/write` / `/delete` 0; SQL `databases/write` 0. Any other write = STOP; list it.
6. Plan `asp-hpsmpoc-uat` P0v3 x1 with `LastError` empty; access rules; SQL firewall (1); vault secret names (2); resources (14; B1490 deleted the 15th); tags: equal to B1466's W5.
7. The database as D-5; the public page build (`NQga609FQ4iKZFwQ1rtsT` x1); no `B1540_ADDENDUM-*.md`.

**Rule:** any difference not covered by D-6 STOPS before the next write, listing EVERY differing signal.

## BUILD (one attempt; fix root causes, never skip; nothing hosted is written in BUILD)
1. **Step 0 and PHASE 0 (read-only).**
   - Run `date` and the clock arithmetic (hard stop and write cut-off as absolute AEDT), then the REFUSE checks in order.
   - **Copy this brief unchanged into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/` NOW** (`cp -n`, then `cmp`; record both sha256s and the slot count 0). B1466 forgot this step and made the copy at the end.
   - **Write STATUS `1_Project_Definition/Briefs/2026-11-12_B1540_STATUS.md` right after Step 0:** first line `DEPLOY B1540: PENDING`, then a STATUS-NOW line kept current (step, next command, minutes to cut-off). Write no `DEPLOYED`, `ROLLED BACK`, `PARTIAL` or `STOPPED` line until you mean it.
   - Re-measure `compare PREV...TARGET` and print every commit with its PR and every path with its +/-.
2. **Clones (detached):**
   - `.tools/b1540/repo` at `TARGET` and `.tools/b1540/repo-prev` at `PREV`;
   - each from origin with the project deploy key by a per-command `-c core.sshCommand=...` (key never printed);
   - push URL `DISABLED-no-push`;
   - never a fetch, worktree or ref write in `2_Project_Files`; never a push. **The repo's own configured identity only; never `git -c user.name/user.email`, never `GIT_AUTHOR_*`/`GIT_COMMITTER_*`.** This seat commits nothing.
3. **Fetch and prove `TARGET`'s packages.**
   - From `repo`: `scripts/deploy-from-ci.sh fetch TARGET` (rc 0). Quote both `OK ... package` lines, both `MANIFEST.json` `commit` = `TARGET`, and `RUN` (= S5).
   - **No-schema proof:** the api package's `assessment.sql` = `03f1afb36b5cb4261a5932f64da8a38b360a75e719fdff5bdccc25591b9e1bb5` and `feedback.sql` = `2a587ac2824755f12d3e03f0dde768d3414e89e91c9ad85ac2b4f612b135d3c3`, byte-equal to `.tools/b1540/rollback/<PREV>/api/` (`cmp`). Unequal = STOP (`STOPPED: NEEDS TUESDAY a schema step is in the range`).
   - Record the new web `.next/BUILD_ID` (it must differ from `NQga609FQ4iKZFwQ1rtsT`). Control: `verify --expect-run 42773429652` on `TARGET`'s packages fails.
   - The SQL Server legs of CI (the ledger and retention tests still run there): all three success. `CHECKPOINT CI green`.
4. **Package checks, `TARGET` vs `PREV`, property first** (`pkgcmp1540.py`, `lits1540.cjs`; copies of the `1466` ones with their maps hand-edited; plant controls first).
   - **Web:**
     - page routes added 0, removed 0 (58 = 58 in B1466);
     - `node_modules/` 0 differences (this is the dev-only proof if the minimatch commit is in the range);
     - static/public equal;
     - the differing files are chunk, app and build-id files only;
     - `lits1540` UNEXPLAINED 0 both ways (the `encryptionKey` manifest classed by hand, redacted), and the added/removed literals are exactly the frozen `old`/`new` strings plus the step title and the class strings the builder listed;
     - for each frozen row: `new` count in the web package >= 1 and `old` count 0, except where the row's `old` is also held by a fixture the package does not ship; the **control** "Playbook Partner Readiness" present in BOTH;
     - a test-only string from a changed test file reads 0 in the web package.
   - **API, the property "every HpsmPoc DLL may carry code; every non-DLL/PDB file is EQUAL except `HpsmPoc.Api` (app host) and `HpsmPoc.Api.deps.json`, whose diff is exactly the Pkcs version, file-version and package hash/path lines (6 hunks at `c717ba1a`; print the diff)":**
     - 122 = 122 files expected (STOP on any other count);
     - `appsettings.json`, `*.runtimeconfig.json` and `SeedContent/` EQUAL (no new setting);
     - `System.Security.Cryptography.Pkcs.dll` (root and `runtimes/win/lib/net10.0/`) differ from `PREV`'s and have file version 10.0.1526.53008 (read by the PE version resource);
     - `HpsmPoc.Modules.Reporting.dll` `#US` heap holds the R2 sentence "Tiers are options informed by risk and scope, selected by the partner. None requires paid consulting or a hardware replacement." x1 / x0 (UTF-16LE; control: an existing sentence x1 / x1);
     - `HpsmPoc.Modules.Assessment.dll`: the range changes it only by the csproj's package reference (no C# source in `api/src` changes except `ReportModelBuilder.cs` in Reporting), so it may differ by the stamp and reference version only; a differing `#US` heap there = STOP. `HpsmPoc.Modules.Rules.dll` and `HpsmPoc.Modules.Feedback.dll`: 0 unnamed runs (stamp-only; at `c717ba1a` all five HpsmPoc DLLs already differ from PREV's by the embedded sha stamp);
     - every `TARGET` DLL embeds `T8` x1 and `PREV8` x0.
   - `CHECKPOINT package checks`.
5. **The words gate (D-8)** and the **held-absent plan (D-9)**: `wordsmap1540.py`, `words1540.py`, `heldabsent1540.py`; plant controls first; the full table in STATUS. `CHECKPOINT words gate`.
6. **The way back, proven and not run.**
   - `PREV`'s packages per REFUSE line 1. `verify --expect-commit PREV --expect-run 42773429652` rc 0 (control: `--expect-run <S5>` fails).
   - Download the BEFORE wwwroots read-only (as `live1466.py` did): `live1540.py before`. The live-check against `PREV`'s packages must be equal (web 2116/2116, API 122/122; only the favicon pair allowed site-only on the web).
   - **Write `rollback1540uat.sh`** (D-7: one path, sub-command `rb`). Guards as D-7. Each `az` write is preceded by the identity pass. **Stub run** (a scratch `PATH` `az` that answers `account show` with the records' identity and logs every other argv): the argv names `hpsm-poc-uat-rg`, the two UAT sites and `PREV`'s zips, with `--type zip --async false --clean true`, web then API; `TARGET`'s sha or zips appear 0 times; `sql`, `stop`, `restart`, `firewall`, `appsettings`, `delete`, `Down` and `feedback.sql` appear 0 times. Stub controls: HEAD check with `repo` (= `TARGET`) gives rc 96 with 0 calls; zips pointed at `TARGET`'s gives rc 97 with 0 calls; a group `hpsm-poc-rg` gives rc 95 with 0 calls.
   - `CHECKPOINT rollback point taken`.
7. **Instruments.**
   - Copy by name + `cmp` from `.tools/b1466/` (read-only), rename to `1540`, hand-edit: `identity_pass`, `presig`, `live`, `pkgcmp`, `words`, `lits`, `walk`, `cmpwalk`, `pairseed`, `webpair`, `deploy`, `cfgkeys`, `closedlist`, `partf`, `pfplant`. List which, with the digests got.
   - **New behaviour in `walk1540.cjs` / `cmpwalk1540.py`:** (a) the page text of every walked page saved BEFORE and AFTER, so `wordsmap1540.py` can apply the substitutions in process; (b) the `main` landmark count per page; (c) the walkthrough's cover and steps 1, 2, 3, 8, 12, 13, 14 including the bridge cells; (d) `<meta name="description">` read from the page HTML; (e) `cmpwalk` allows ONLY D-12's closed substitutions (the sidebar, Demo alias and logo readers of B1466 are kept as regression checks and must read EQUAL now).
   - **Forbidden-operation grep** `sql db |sqlcmd|deployment group (create|what-if)|appsettings (set|delete)|firewall-rule|webapp (stop|start|restart)|/submit|method: *.DELETE|Down\(` over `.tools/b1540/` programs (clones and packages excluded). It must list exactly: `rollback1540uat.sh` (the deploy lines only), `deploy1540.sh`, the PART F plant line and the router's abort list. **`sqlcmd`, `sql db`, `webapp stop|start|restart` must list 0 lines in `deploy1540.sh`, `rollback1540uat.sh` and `presig1540.py`'s write paths.** Name each line. Control: a planted line lists 1 more.
   - Never copied: `rollback1466uat.sh`, `schema1466.sh`, `rule1466.sh`, `sqlget1466.sh`, `sqlapply1466.sh`, `refusalpoll1466.sh`, `sqlboot1466.py`, `snap*`, shots, evidence trees, other seats' clones.
8. **Local proof (NO load gate; print `uptime` load1 beside each run; a timing-only failure is re-run once and both results written; run under `.tools/b1540/heavy.lock`, a seat-local `mkdir` lock).**
   - **(i) API seeder, SQLite, UAT-shaped** (as B1466 BUILD 7 (i), from the PUBLISHED packages with the machine's shared runtimes, NOT from source: the SDK pin blocks `dotnet build/run` in a clone): `TARGET`'s API boots twice on a `PREV`-seeded db. Expected now: **no migration applies** (history rows equal); the second line "...already in this database; nothing was written."; every table's row count and hash equal; boot 2 = boot 1. Plant: one added row reads 1 differing.
   - **(ii) Web pair** (as B1466 BUILD 7 (ii)): 4 levels sign in; route tables `TARGET` vs `PREV`; status differences 0; **the text residue after the frozen substitutions is 0 on every walked page, both levels of width** (this is the dry run of D-12; plant: a changed word on one page reads residue 1). If the local seed gives a level no rows for a page, say "not applicable locally" with the reason.
   - `CHECKPOINT local pair`.

## PART P: the window on UAT (`hpsm-poc-uat-rg`; web `app-hpsmpoc-web-uat-25onzn`, API `app-hpsmpoc-api-uat-25onzn`) `[PROD-CLASS]`
P1. **BEFORE (read-only; API up).**
- PRE-DEPLOY SIGNALS (all seven), D-5 (`CHECKPOINT DATABASE STILL AWAKE (before)`), and the platform backup facts. **Record T0 = the UTC minute now** (the restore point a later reader would use), and the app-settings hashes, active deployment ids and BEFORE wwwroot sha256s.
- The live-check of the downloaded wwwroots against `PREV`; `/health/ready` once, timed.
- The B1466 P1 walk at both widths: start page; 8 plain sign-ins; route tables per level; customers 4/5/5/4 and id-set hash; the readiness hub (Partner); the 14 walkthrough steps (two walks); Recent activity; the refusal matrix; D-14; the D-12 runner/results pages; PLUS the D-12 readers (page texts saved).
- **The API probe BEFORE:** as Partner, `GET /api/v1/assessments/<the sample customer's assessment>/follow-ups` (`AssessmentModule.cs:274` at `TARGET`; print the `file:line`). Record status and item count only (B1466: 200, 0 items).
- Screenshots `before-uat-<page>-<w>x<h>.png` into `Briefs/2026-11-12_B1540_evidence/` (start page; Partner home 1440 and 390; the walkthrough cover 1440; `/revenue` 1440). Never a feedback page. Open the key frames with the Read tool and describe them.
- `CHECKPOINT UAT BEFORE walk`.

P2. **THE WINDOW (`deploy1540.sh`).**
- Re-list panes. Re-read the addenda. Re-read the PRE-DEPLOY SIGNALS (W2 = W1 except the activity window). **Re-read origin main against S4.** Fresh identity pass. Cut-off check.
- `deploy1540.sh` (B1466's `deploy1466.sh` `740088c5` with its guards hand-edited and its stop/start lines REMOVED): before the cut-off; `B1540_ADDENDUM` 0; `repo` HEAD = `TARGET`; `RUN` = S5; live public build `NQga609FQ4iKZFwQ1rtsT` x1 and `TARGET`'s x0; origin main = `TARGET`; the API is Running.
- Then, in the same second as `DEPLOY START`, exactly `scripts/deploy-from-ci.sh deploy <TARGET> hpsm-poc-uat-rg app-hpsmpoc-web-uat-25onzn app-hpsmpoc-api-uat-25onzn` from `.tools/b1540/repo`.
- Exit 0 = done. Exit 3 = DEPLOYED BUT NOT PROVEN: STOP with the list. Exit 1: read the reason; no hand steps; D-7.
- Windows from deploy start: **web 420 s, API 900 s**; past a window, any non-200 starts `rollback1540uat.sh rb` within 60 s. The poller writes every 10 s (web `/api/health`, API `/health`); the heartbeat every 30 s to `.tools/b1540/logs/heartbeat.txt`.
- `CHECKPOINT UAT deploy START`. Record, from the platform lines, each app's new container `Site started.` time and the seconds between the old container's last line and the new one's, and the count of non-200 poll ticks (this is the user-visible gap; there is no hand-made downtime).

P3. **AFTER (read-only HTTP; only D-11's named non-GET calls).**
- (a) `/api/health` and `/health` 200 x3 ten seconds apart; `/health/ready` 200 (timed); `/` 200; `/customers` 307; session `{"signedIn":false}`; `login.microsoftonline.com` 0.
- (b) **THE API PROBE LIVE:** the same `GET .../follow-ups` as BEFORE: 200 and the same item count. A 5xx = slot-S9.
- (c) Start page = BEFORE; 8 of 8 plain sign-ins; walkthrough panel 0 on every one.
- (d) Route table BEFORE/AFTER per D-12 (`cmpwalk1540.py`: FAILS 0, S9 classes 0; plant: a route set to 500 reads S9 1; plant: one changed word reads residue 1).
- (e) **THE CHANGE LIVE, measured, in a SEEN table at 1440 and 390 (what is read, by frozen id, from `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_hpsm-messaging-map.md`):**
  - **the build:** the live web `.next/BUILD_ID` = the package's and named x1 on the public page; `<meta name="description">` (M1) reads the new sentence;
  - **sign-in (S1-S3):** if a sign-in screen is reachable by GET navigation on UAT, read S1 (lead), S2 (the two-line panel headline, 1280 only), S3; otherwise write "not shown on UAT" with the route list tried (the UAT start page is operational and unchanged, map Surface 2);
  - **Home (Partner), 1440 and 390:** H1 (lead), H2 and H4 (the two buttons "Start a customer assessment"), H3a/H3b (closing heading and sentence), H5, P1 (panel title "Assess. Implement. Optimize."), P2 (panel lead), P3a/P3b (legend and the 11 sr-only labels), P4 (theme "Applicable HP solutions"), P5a ("Possible commercial follow-up:"), P5b-d (the three sentences), P6 (the "planned or subject to implementation" line x3), H6a (the tile's "Estimate, not booked or recognised revenue." sub line);
  - **the walkthrough (both walks):** cover W1/W2; step 1 W3; step 2 W4/W5/W6a/W6b; step 3 W7 (the new caveat); step 8 W9/W10/W11 and W8 (title in the jump list); step 12 W12/W13 and the step-12 title "Delivery phases: Assess / Implement / Optimize"; step 13 W14a/W14b; step 14 W15/W16/W17; the bridge cells W18/W19 on steps 12 and 13;
  - **`/customers/<sample>/recommendation`:** R1 (lead); R2 only if the page renders a tiers sentence (else "not reached", D-13);
  - **`/customers/<sample>/next-engagement`:** R3; **`/revenue`:** R4 (banner second line), R5a; **`/revenue/results`:** R4, R5b; **`/services`:** V1;
  - every frozen `old` string reads ABSENT on every page walked (count per id);
  - **S15** states the expected SEEN values; a difference from S15 on a healthy site = STOP with the values (slot-S9 classes roll back).
- (f) Security views; refusals (403 `uat.action-off` x2); the D-14 door = BEFORE.
- (g) The words table (D-8) in STATUS; **the held-absent table (D-9)** in STATUS, each check with its control.
- (h) **Build proof:** live-check web and API = `TARGET`'s counts, site-only 0; the live `BUILD_ID` named x1 and `NQga609FQ4iKZFwQ1rtsT` x0; the live HpsmPoc DLLs embed `T8` x1; the live `HpsmPoc.Modules.Reporting.dll` `#US` holds the R2 sentence x1; the live Pkcs DLL equals the package's; active deployments both new.
- (i) The platform lines of the new containers, verbatim.
- (j) Settings hashes equal (W4 vs W3); SQL firewall exactly `AllowAllWindowsAzureIps`; databases exactly {`hpsmpoc`, `master`}.
- (k) D-12 runner and results pages = BEFORE.
- (l) **The activity log since Step 0:** exactly the deploy's rows (two `sites/extensions` or deployment writes per app as the platform logs them, the restarts of each app, and `publishxml/action` reads); **0 `firewallRules/write`, 0 `databases/write`, 0 `databases/delete`, 0 `webapp stop/start` by hand.** Anything else listed: STOP.
- (m) D-5 again (`CHECKPOINT DATABASE STILL AWAKE (after)`).

**Healthy and all passed: `PART P VERDICT: PASSED` (`CHECKPOINT PART P PASSED`).**
- Unhealthy past a window, a deployed app not answering, the API probe failing, or a slot-S9 class: `rollback1540uat.sh rb`, then `ROLLED BACK`.
- Any other miss on a healthy site: `STOPPED: NEEDS TUESDAY`, with the numbers and the one-command way back printed. **Still run PART F before the STOPPED line if the site is healthy.**

## PART F: the UAT feedback store (READ-ONLY; D-17)
Run only after `PART P VERDICT: PASSED`, or after a healthy-site STOP. Never after a way back.
- Run D-17. The only non-GET calls are 1 Admin sign-in POST and 1 sign-out POST, both counted.
- Write the counts and the table of items newer than 2026-11-10 22:23 AEDT under `## PART F: UAT feedback (read-only)`.
- `CHECKPOINT PART F DONE`.

## STANDING LINES
1. **PRIOR-WORK CHECK first, read WHOLE before the first `az` call; STATUS needs a `PRIOR WORK` section:**
   - this brief;
   - the B1466 kit (738 lines) and `Briefs/2026-11-10_B1466_STATUS.md` (271 lines); the B1460 kit (636 lines) and `Briefs/2026-11-10_B1460_STATUS.md` (320 lines; Corrections 1-7, FOR TUESDAY 5 (c)-(g), NOT TESTED); `Briefs/2026-11-11_B1490_STATUS.md` (the copy deletion; the changed way back);
   - `Briefs/2026-11-12_B1535_STATUS.md` (148 lines: BUILT/HELD, the layout table, the closing scans) and `.tools/b1535/frozen.jsonl`;
   - the messaging map `tuesday/briefs/2026-11-12_hpsm-messaging-map.md` (267 lines) and `Briefs/2026-11-12_B1539_STATUS.md` (the held tickets);
   - the gate VERDICT files named in S6 at their FINDINGS;
   - `scripts/deploy-from-ci.sh` at `TARGET` (109 lines at `c717ba1a`), `infra/README.md` at `TARGET` only for the deploy section (a database section is not used);
   - the project `CLAUDE.md`; `1_Project_Definition/CLARIFICATIONS.md` (local copy 192 lines is stale: the live records are in the analysis repository's copy read by `gh api -X GET` raw, C-300 and C-363 to C-366; control: `### C-366` hits 1, a no-such token 0).
2. **Never touch what the ruling does not name.** No `az` write and no HTTP except the named ones. No other group, not even a read (only the subscription-level `az group list`, names only). Never another subscription. Never `HP Reporting and Docs/`, any SOW, `2_Project_Files/HP Docs/`, `1_Project_Definition/Source_Documents/`, `.local/`, `4_Credentials/` (beyond `.azure` and `.gh-config`).
3. **Never delete** (`rm`, `rmdir`, `az ... delete`, `docker rm`, `--prune`). Quarantine by MOVE to `.tools/b1540/_quarantine/`.
4. **No message to any human**; nothing to HP; no Jira write; no person's name or e-mail in STATUS ("the product owner"). Synthetic data only: print no customer content beyond counts, titles and hashes. PART F summaries follow D-17.
5. **Secrets:**
   - never on argv, never printed, never in a kept file, STATUS or screenshot;
   - gitleaks over the evidence folder with a `ghp_`-shaped canary (rc 1; real rc 0);
   - `encryptionKey` values 0;
   - host names (`azurewebsites.net`, `scm.`, `vault.azure.net`, `database.windows.net`) 0 outside the STATUS last line (control 1);
   - dotted quads only `127.0.0.1` (control 1).
6. **CodeQL policy.** This seat lands nothing and opens no PR. Tuesday lands through CodeQL (Datasec org ruleset; never bypass, never dismiss an alert).
7. **Shell:**
   - never type `cd`; absolute single-quoted paths (they contain `!`);
   - `/usr/bin/grep -i` with a positive control for every count;
   - zsh: `pipestatus` or `bash -c`; never an unquoted word starting `=`; brace every `${VAR}`; no `$?` after a pipeline;
   - no `timeout`, no `pgrep -f`; wait by `kill -0` or done-markers;
   - `python3 -I -B` only; scratch in the session scratchpad, never `/tmp`;
   - hex and sha maps hand-edited, never by `sed`;
   - a `file:line` you cite is printed by `grep -n -i` or `awk NR==n` at `TARGET` just before you write it; a clock comes from `date` in the same action;
   - read a tool's usage from its header (or `az ... -h`), never by invoking it for effect;
   - **never `rm`**.
8. **Records: none in this seat.** STATUS and evidence only; nothing committed or pushed. Git identity is never overridden (see BUILD 2); if any commit is somehow made, print `git log --format='%h %ae | %ce'` for it and require both equal to the repo's configured email.
9. **STATUS sections** (`1_Project_Definition/Briefs/2026-11-12_B1540_STATUS.md`, evidence in `.../2026-11-12_B1540_evidence/`), in this order:
   - Step 0
   - **BLUF.** Its first line states any way back or stop. It carries in one line: the build id AS SEEN and the Home panel title AS SEEN. In a second line: **no schema step (digests), no database write, no API stop**, and the user-visible gap per app. **Anything "not shown" goes in the BLUF.**
   - PRIOR WORK
   - PHASE 0 and LIVE-BEFORE
   - Target, gate and CI proof (incl. the commit table for the whole range, the #309/#312 landing proof, the no-schema proof, the minimatch dev-only proof if present)
   - The words (D-8) and the held-absent table (D-9)
   - Package checks and the local proof
   - The way back (copied; digests; `rollback1540uat.sh` stub runs)
   - PRE-DEPLOY SIGNALS and the database (before; backup facts; T0)
   - PART P (BEFORE, deploy, AFTER: the SEEN table by frozen id; the API probe; the build proof; the activity rows)
   - **PART F**
   - Settings/access/spend (**no new spend: no copy database; say so**)
   - The way back (kept, NOT run; or run, with every step)
   - NOT TESTED
   - FOR TUESDAY, in six numbered items:
     1. UAT at `TARGET` (the sha, deployed times, deployment ids, BUILD_ID, CI run); main head at the deploy; **no schema step**; the user-visible gap.
     2. **A short note for the product owner, 4-7 lines, plain words:** what changed on UAT in his words (the promise line, the Home buttons, the phase panel, the walkthrough, the revenue pages' estimate wording, the services lead), the step-12 title, nothing held or next-phase visible, no data changed, how long each app was restarting, the feedback count and anything new.
     3. The tables.
     4. Records owed: a deploy C-entry for `TARGET` (no schema step) naming the PRs in S12 (including #309-#313 deployed here for the first time) and the product owner's two messages; and the list of what stays held (the tickets).
     5. The copy database is GONE (B1490): the way back is code-only; say what a database fault would need (the platform's point-in-time window, T0).
     6. Anything seen worth a ticket (e.g. B1466's open item: Demo Home's "Customer assessment pipeline" panel still names real customers to the Demo level).
   - Processes (the last 5 heartbeat lines; listeners 0)
   - Corrections

   Also the `CHECKPOINT` lines.

## PARTITION (named from both sides)
- **Yours:**
  - `.tools/b1540/` (incl. `repo`, `repo-prev`, `target/`, `rollback/`, `live/`, `logs/`, `fb/`, `_quarantine/`) and `1_Project_Definition/Briefs/2026-11-12_B1540_*`;
  - read-only `az` on `hpsm-poc-uat-rg` (ARM GETs, the activity log); read-only GETs on the two UAT hosts (plus D-11's named non-GET calls);
  - the D-2 write class (w1)-(w2), nothing else.
- **Not yours:**
  - every other group, database and subscription; the template; any app setting, vault secret or firewall rule; the demo data; any SQL connection;
  - `.tools/b1466/`, `.tools/b1460/`, `.tools/b1535/` (read-only: copy by name) and every other seat's tree;
  - `2_Project_Files` content (read only); records repositories;
  - any PR, branch, Jira ticket or message;
  - every real feedback item.
- **From the other side:**
  - Before you start, Tuesday has landed the messaging change (and the minimatch commit if it goes), filled the slots and confirmed no other HPSM-POC deploy seat.
  - Tuesday deploys nothing to UAT and changes nothing in `hpsm-poc-uat-rg` until your STATUS ends `DEPLOYED`, `ROLLED BACK` or `STOPPED`.
  - If anything lands on main while you run, you finish on `TARGET` (D-1 after Step 0).

## HOLDS (never, in this brief)
- No write START after the hard stop.
- No deploy of anything but `TARGET`'s two CI packages (or `PREV`'s in D-7).
- No what-if; no template deploy; no `az webapp show`.
- **No SQL of any kind: no `sqlcmd`, no `az sql` write, no firewall rule, no copy/restore/rename, no `feedback.sql`, no `assessment.sql`, no migration `Down`.**
- No app-setting or vault write. No web-app stop, start or restart except the deploy's own. No `delete`.
- No hosted demo-data reset, re-seed or edit. No customer created, renamed or deleted on UAT. No feedback item created, approved, deleted, moved or downloaded; no click on either feedback page; no screenshot of either.
- No narrative generated; no readiness self-assessment started; no walkthrough answer saved; no PDF opened; no account-menu level item clicked; no collapse control clicked.
- No held row (D-9) built or shown; no claim to HP that a next-phase item or an HP-tool integration is done.
- No new paid resource. No CI re-run. No code edit. No word edited. No claim to HP.

## Stamp
Pane `Datasec/HPSM-POC-D61` (suffix `D61`). MEASURED at drafting: no `SEAT-D61` file and no `B1540` file in `tuesday/briefs/` before the drafter's two files (`ls | grep -c` 0). `.tools/b1540` absent. Seat level `BRIEF_SEAT_LEVEL=opus`.
- (S1) STAMP (Tuesday, `date`; kit read whole with its line count; CI at `TARGET` and `branches/main` re-read at source; the messaging PR landed): ____
- (S2) LAUNCH AUTHORITY (verbatim, with clocks: the product owner's 10:51 and 11:21:32 messages of 2026-11-12 as quoted in WHAT THIS KIT IS item 5; the standing grant row; whether he read the words list, and his reply): ____
- (S3) HARD STOP (the rule): Step 0 plus 120 minutes, written by you as an absolute AEDT clock at Step 0; no write START after it; DONE no later than Step 0 plus 150 minutes; Step 0 within 45 minutes of slot S1: ____
- (S4) DEPLOY SHA = TARGET (40 hex; the landed main sha after the messaging squash, and after the minimatch squash if that lands first; = `branches/main` re-read by Tuesday at the stamp; one parent; a descendant of `009421a28616c8b31dde86b59d4c4ca674c288fa`): ____
- (S5) CI RUN at TARGET (push run `ci`; and the CodeQL `Push on main` run; both completed/success, with the run ids): ____
- (S6) WHICH PRs IN TARGET, their heads, their gate lines, and the open findings carried by id (the drafter's reading for the five earlier ones: #310 `15be8814` B1507 GO WITH FINDINGS, #311 `a2461ce7` B1503, #309 `0ccb1ec1` gated `4f084fb` B1497, #312 `43a06592` gated `40217c1` B1496, #313 `b6ab804a` B1519; Majors 0 in all five; plus the messaging PR with its gate line, and the minimatch PR if present): ____
- (S7) RULING 1, the route: `CODE ONLY; NO DATABASE WRITE; NO API STOP; BOTH PACKAGES; NO SQL RULE; NO WHAT-IF; NO TEMPLATE DEPLOY; NO APP SETTING WRITE; NO DATA RESET`: ____
- (S8) RULING 2, the site: `UAT ONLY`: ____
- (S9) RULING 3, the misses. Drafter default: take the way back RB-A and end ROLLED BACK when: a level does not sign in; a route that answered 200 before answers 5xx after; the API probe answers other than 200; `/health/ready` is not 200 past the API window; a security view answers 5xx for the known customer, or 2xx other than the not-found page for no-such-id; any non-GET request other than D-11's named calls is attempted from any walked page; the walkthrough panel appears on a plain level sign-in; the start page loses a level button, or the sidebar is absent on a signed-in page; the account menu is absent; a D-12 runner or results page differs from BEFORE, or the hub is absent, 5xx, or without its runs list; any existing customer row is removed or replaced; a horizontal scroll appears that BEFORE did not have; reset or customer-delete answers anything but 403 `uat.action-off`; the API or web refuses to start; a D-14 gated admin page stops redirecting a visitor with no session; **a page text residue after the frozen substitutions; a held or next-phase item visible (D-9); a signed-in page with other than one `main` landmark**. Every other miss on a healthy site (SEEN values differing from S15 included) = STOP, with the numbers and the one-command way back printed: ____
- (S10) RULING 4, seven items, each CONFIRMED / NOT CONFIRMED: (a) read-only copies by name from `.tools/b1466/` into `.tools/b1540/`, hand-edited; (b) the clones into `.tools/b1540/repo` and `repo-prev` (no go-sqlcmd download in this kit); (c) D-11, D-12, D-13, D-14, D-16 (no real feedback item touched; no customer, run or narrative created on UAT; a real Chromium walk, read-only); (d) **both UAT apps restart in the deploy (web then API, a few minutes in all; the API longer), with NEW API code, and whether an HP review session is under way is not measurable**; (e) ports 9960-9969 (or the block Tuesday names), and no other `Datasec/HPSM-POC-D*` pane present; (f) PART F as D-17 (counts and items since 2026-11-10 22:23); (g) **no database copy, no SQL, no firewall rule (S14), so the way back is code-only (D-7)**: ____
- (S11) RULING 5, the words on UAT (`UAT WORDS: THE CLOSED LIST OF D-8, READ BY THE PRODUCT OWNER` or `UAT WORDS: THE CLOSED LIST OF D-8, SENT TO THE PRODUCT OWNER BESIDE THE DEPLOY`): ____
- (S12) PULL REQUEST NUMBERS in the range, in merge order (expected `310 311 309 312 313` then the messaging PR, then the minimatch PR if it lands; from `commits/<sha>/pulls`): ____
- (S13) RULING 6, the UAT hold: `UAT HOLD LIFTED FOR THIS DEPLOY ONLY: ACCEPTED`: ____
- (S14) BACKUP FORM (exactly `CODE BACKUP AND RESTORE POINT READ; NO DATABASE COPY`; the alternative, a database copy as in B1466, needs a different kit): ____
- (S15) EXPECTATION AS SEEN (D-12 / P3 (e)): the live BUILD_ID is new; the Home panel title reads "Assess. Implement. Optimize."; the Home lead reads "A simpler way to sell, deliver and grow print security services with HP."; the buttons read "Start a customer assessment"; the walkthrough cover headline reads "The trust you've earned. The opportunity ahead." (typographic apostrophe); step 12's title reads "Delivery phases: Assess / Implement / Optimize"; the `/services` lead and `/revenue` banner as the frozen rows; every frozen `old` absent; held rows visible 0; `main` landmark count 1 on every signed-in page: ____
- (S16) EARLIER LANDINGS (exactly `THE FIVE EARLIER LANDINGS 309-313 RIDE THIS DEPLOY: ACCEPTED`, or `HOLD`: STOP at once): ____

**Commission (read-only to you):** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1540_SEAT-D61_hpsmpoc-uat-deploy-messaging.md`. **Step 0:** run the REFUSE checks in the order written, then copy this brief unchanged into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/` and record `cmp`, both sha256s and the slot count. Preflight: write "none (brief_seat launch)" or quote the launcher's warnings verbatim.
**Launch (Tuesday, ONE waiter, through the cool-load waiter, as a tracked background task; launch only after the stamp):** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/HPSM-POC-D61 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=opus WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1540_SEAT-D61_hpsmpoc-uat-deploy-messaging.md'"` (the form RELAYED from B1466's kit; the drafter `ls`-checked that `tuesday/tools/launch_when_cool.sh` and `tuesday/brief_seat.sh` exist, 13:2x). **Never run /model in this pane.**
**Last line of STATUS, exactly one of:**
`DEPLOYED B1540: <sha40> <site url>` (the sha is `TARGET`; the site url is the UAT web site's public address, written once, as the last line only), or
`PARTIAL B1540: DEPLOYED, NOT PROVEN, <reason>` (followed by a `STOPPED:` line only if it is the last), or
`STOPPED: NEEDS TUESDAY <one question>`.
(`ROLLED BACK` is a body line plus a final `STOPPED: NEEDS TUESDAY <one question>` last line.)

READ-WHOLE-BY-TUESDAY: ____
