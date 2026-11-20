# B1765: reports A9 and A10 and the answers C-38 to C-44 applied to the OXPd architecture, plan and readiness note

Datasec / OXPd, 2026-11-20. One writer, commissioned by Tuesday (brief `2_Project_Files/tuesday/briefs/2026-11-20_B1765_OXPD-APPLY-A9-A10-AND-RULINGS_COMMISSION.md`). STATUS: COMPLETE. All three documents were edited and written to disk, the three PDFs re-rendered, and this file written last. A successor does not need to re-commission.

Backups: the six `.pre-B1765` files (three `.md`, three `.pdf`) were made with `cp -p` and compared with `cmp` (equal, six of six) before the first edit; none existed before.

## BLUF

1. **The gateway is read and the documents now say so.** `hpam-api` is three Azure Functions in front of Azure SignalR. The server can join it as designed. Two things changed in the design text: the phone-link relay is a template change and a new version of the Azure offer (not "one added endpoint"), and the gateway does not check who sends an unlock message. OQ-7 is answered in both halves.
2. **Question 10 has its fact, and is not decided.** The text, the recommendation ((b), with the two untested links named) and the wording of the default were updated; the default itself ((a), as Workpath) was NOT changed, because changing it would be a product decision.
3. **Deployment uses the HPK Deployment Utility, amended (C-43).** New section 8.7 in `02`, new work packages WP0.10 and WP5.8 in `03`. The utility is the operator's tool; the server's onboarding engine executes and repairs. That split is this design's default and is put to the product owner (OP-1).
4. **Small corrections from the earlier OXPd 1 tree (A10):** it is not new material; the Java fallback is no longer described as "1.8.4.1 jar, known to work"; its two keys are not the Workpath card key. Report A7 is qualified, not edited.
5. **Rulings applied:** sensitivity labels left out (C-38); the M577 recorded as stated and nothing more (C-39); the lists live on Jira `OXPD2-1` and `OXPD2-2` (C-41); phase 0 has started on the no-hardware work (C-42). C-44: nothing applied, as instructed.

## Counts (by program)

| Measure | `02_architecture.md` | `03_plan-of-attack-and-build.md` | `05_readiness-to-build.md` |
|---|---|---|---|
| Lines, before and after | 985 and 1,067 | 450 and 506 | 184 and 250 |
| Bytes, before and after | 185,078 and 224,376 | 84,752 and 109,229 | 20,181 and 35,974 |
| Placed edits (each anchor found exactly once before writing) | 51 | 44 | 20 |
| Diff hunks against the `.pre-B1765` backup | 45 | 35 | 18 |
| Hunks that are a pure deletion | 0 | 0 | 0 |
| Lines naming B1765 (control: lines naming B1760) | 66 (26) | 59 (16) | 2 (2) |
| PDF pages, before and after | 38 and 46 | 17 and 21 | 6 and 11 |

Other counts: F rows in `02`: 81 before and after (no requirement row added or removed). R rows in `02`: 30 and 31 (R31 added). Work-package rows in `03`: 57 and 59 (WP0.10, WP5.8 added). Open-point rows: 18 in `03` and 18 in `05`. Table rows whose column count differs from their header: `02` 15 before and 15 after (none new), `03` 0 and 0, `05` 0 and 0. `CLARIFICATIONS.md`, the analysis reports and the project folder `OXPd_2` were not written to (`git status` shows `CLARIFICATIONS.md` and A9 unmodified; nothing was ever opened for writing under `OXPd_2`).

Corrections: A9 proposed 22, **22 applied** (4 of them not in the proposed wording: PC5, PC7, PC17, PC20, see table 1). A10 proposed 8, **8 applied**. **Not applied: 0.** New open points: **18** (OP-1 to OP-18). Changes that are not a numbered correction of either report: table 3.

In `02`, five wordings were replaced rather than added to; in each the old words are quoted in the new text: P14 ("Spike against the simulator"), C3 ("OXPdLib 1.8.4.1 jar, known to work"), the 6.6 row for the earlier build's keys, W5 ("every printer of a tenant"), D26 (the draft's choice (a)). In `03` one row was replaced (OQ-10) with its old text kept inside it. In `05` the BLUF and question 10 were rewritten with the old text kept beneath and marked.

## 1. Report A9: its 22 proposed corrections

Citations: `A9:n` is line n of `analysis/A9_hpam-backend-gateway-and-infra.md`.

| PC | Document, place | Disposition | Change-log id | Source line |
|---|---|---|---|---|
| PC1 | `05` question 7, "Still open" point | Applied; the old point kept above the update | (05 update) | A9:302; A9:11, 234 |
| PC2 | `05` BLUF | Applied inside the rewritten BLUF (item 3); the old BLUF kept beneath | (05 update) | A9:303 |
| PC3 | `05` question 7 "Blocks" line | Applied as an added bracket | (05 update) | A9:304 |
| PC4 | `05` question 10 text | Applied | (05 update) | A9:305; A9:240-241 |
| PC5 | `05` question 10 recommendation and default | **Applied, not in the proposed wording.** Recommendation now (b), with the condition under which it weakens (the two untested links). Default kept as (a), reworded to say it is a default and not a decision | (05 update) | A9:306; A9:261 |
| PC6 | `05` kit item 12 | Applied; "Still needed" kept before the update | (05 update) | A9:307 |
| PC7 | `05` "not verified" list | **Applied, not in the proposed wording:** the two entries were not deleted (the text was the product owner's reading matter); an update says they are now in hand and that the phone app stays | (05 update) | A9:308; A9:245 |
| PC8 | `03` phase-0 input, gateway source | Applied | B1765 / GW-SOURCE | A9:309 |
| PC9 | `03` WP0.7 | Applied | B1765 / WP0.7 | A9:310; A9:255, 261, 236 |
| PC10 | `03` WP3.2 | Applied; also raised as OP-12 | B1765 / RELAY | A9:311; A9:236, 243 |
| PC11 | `03` §6 blocker line | Applied | B1765 / RELAY | A9:312 |
| PC12 | `03` OQ-7 and OQ-10 rows | Applied. OQ-10's default unchanged | B1765 / GW-SOURCE, B1765 / OQ-10 | A9:313 |
| PC13 | `02` P11 evidence | Applied | B1765 / GW-SOURCE | A9:314; A9:45-47, 51, 236 |
| PC14 | `02` §6.5 | Applied; the two earlier sentences kept | B1765 / GW-TRUST | A9:315; A9:240-241, 261 |
| PC15 | `02` W5 | Applied | B1765 / W5-WIDER | A9:316; A9:241, 293 |
| PC16 | `02` W27 | Applied | B1765 / W27-SETTINGS | A9:317; A9:242, 296 |
| PC17 | `02` R19 | **Applied, not in the proposed wording:** added as superseding clauses in both cells; the old words kept | B1765 / RELAY | A9:318; A9:243, 291 |
| PC18 | `02` R24 | Applied; the L and I scores left as they were and said to be un-re-estimated | B1765 / GW-TRUST | A9:319; A9:240 |
| PC19 | `02` §7.4 QR gateway row | Applied; the same contract also in F10, C7, M3 | B1765 / GW-CONTRACT | A9:320; A9:46-47, 51-52 |
| PC20 | `03` §8.1 licence line; `05` question 13; also `02` §7.5 and BLUF 4 | **Applied, not in the proposed wording:** "cheaper than this line assumed" was not written, because nothing was measured (the licence server's source was not sent). Who deploys the offer became OP-7 | B1765 / LICENCE-OFFER | A9:321; A9:246, 339 |
| PC21 | `02` §7.4 reporting row | Applied; also F63, C14 | B1765 / REPORT-COLS | A9:322; A9:244-245 |
| PC22 | `02` §8.1 first run | Applied | B1765 / FIRST-RUN | A9:323; A9:248 |

Also taken from A9 without being a numbered correction (its section 6 table and section 7.2): D5 (per-printer routing still unknown: P11, D11), D6 (the `realm` field: M3), D7 (the two scopes confirmed: §6.2), D15 (`infra_hpam` is the older back end: P13, D30), D16 (both features optional and off by default: F63, C7, C14, §8.1), X3 (SignalR Free tier, marked as general knowledge: R19), X5 (no gateway audit trail: §6.5, WP3.1), X6 (record time is arrival time: C14, WP5.5), X7 (Key Vault reference needs a template change: W27), section 5 (secret locations: §6.6, locations only).

## 2. Report A10: its 8 proposed corrections, and report A7

Citations: `A10:n` is line n of `analysis/A10_oxpd1-solution-earlier-work.md`.

| # | Document, place | Disposition | Change-log id | Source line |
|---|---|---|---|---|
| 1 | `02` P14 | Applied; the draft's words quoted | B1765 / P14-EMULATOR | A10:321; A10:29-31, 67, 172, 294 |
| 2 | `02` C3 | Applied; the draft's words quoted | B1765 / C3-JAR | A10:322; A10:186-187, 287 |
| 3 | `02` W3 evidence | Applied | B1765 / W3-KEYS | A10:323; A10:255-256, 288 |
| 4 | `02` §6.6, earlier build's keys | Applied | B1765 / SECRET-LOC | A10:324; A10:31, 237-238 |
| 5 | `02` P16 | Applied | B1765 / P16-JAR | A10:325; A10:186-190, 199-202 |
| 6 | `03` §8.1 line on the earlier build | Applied; the old line kept before the correction | B1765 / OLD-BUILD | A10:326; A10:29-31, 34, 255, 295 |
| 7 | `05` "not verified", sources list | Applied | (05 update) | A10:327 |
| 8 | `05` "not verified", backup-copy point | Applied | (05 update) | A10:328 |

**Report A7 is NOT edited.** The qualification is recorded in the change log of `02` (entry B1765 / A7-QUALIFIED) and here: A7 line 232 (the dead lookup "mirrors the Workpath scheme"), A7 line 474 (the scheme is "inherited from the Workpath product"), and A7's question 4 with the assumption at A7 line 440 that the two keys are the Workpath production keys, hold for the query shape only. The two keys are different values of different lengths under a different algorithm, and occur nowhere in the Workpath sources A10 searched; even if the lookup were wired in it could not find a card enrolled by today's Workpath app (A10:255-256, 288, 295, 330). A7 line 286 ("Working on the simulator") rests on one sentence of the author (A10:294).

For Tuesday to route, outside the three documents (A10:330): commission B1763's own "What arrived" line, and any card that told the product owner the OXPd 1 repository was new material. Not acted on here.

## 3. The answers C-38 to C-44, questions 7 and 10, and changes that are not a numbered correction

`CL:n` is line n of `CLARIFICATIONS.md`. `HPKU/` is the HPK Deployment Utility as sent: `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Source_Documents/2026-11-20_from-product-owner/HPK-Deployment-Utility-main/` (read only; nothing run).

| Input | Document, place | Change | Change-log id | Source line |
|---|---|---|---|---|
| C-38 | `02` F89; the closing paragraph of §3.8 | "not ruled" answered: left out, as today | B1765 / C38-LABELS | CL:236-242 |
| C-38 | `03` WP3.11 (scope and definition of done), E3.1, WP0.6 | The label hook struck; F89 no longer waits on WP0.6 | B1765 / C38-LABELS | CL:236-242 |
| C-38 | `05` question 7, third point | Ruled, with his words | (05 update) | CL:240 |
| C-39 | `05` new "State of the kit" list; `03` phase-0 inputs | The M577 recorded as stated; firmware and wipe not known; generation NOT established | B1765 / C39-C42-KIT | CL:244-250 |
| C-40 | `02` coverage note, P13, D30; `03` phase-0 inputs; `05` BLUF, "not verified" | What arrived, what did not (`cc-api`), `OXPD1` empty; the `cc-api` reading marked as A9's inference | B1765 / GW-SOURCE, B1765 / LEGACY | CL:252-258; A9:205 |
| C-41 | `02` header; `03` header, §8.3 lead, new §8.4; `05` BLUF item 5, question heading, new open-points section, kit list | Pointers to `OXPD2-1` (master list) and `OXPD2-2` (kit) | B1765 / HEADER, B1765 / OPEN-POINTS | CL:260-266 |
| C-42 | `05` BLUF (rewritten; old kept), kit item 1, "what can start" lead | Phase 0 has started on the no-hardware work; what waits is unchanged; folder `OXPd_2`, repository `datasecau/OXPd_2` | (05 update) | CL:268-274 |
| C-42 | `03` header, new BLUF item 8; `02` header | The same, shorter | B1765 / C42-START | CL:268-274 |
| C-43 | `02` new §8.7 (what the utility does: U1 to U10; fifteen steps classed) | New section | B1765 / C43-UTILITY | CL:276-282; A5:196-240, 304, 313-315, 340, 349; `HPKU/` lines in the section |
| C-43 | `02` P9, F60, F61, §4 deployment row, §5.1, C4, C16, W22, §8.1, §8.2, §8.3, §8.5, D26, new R31 | Every place that designs fleet deployment, onboarding or installation now names the utility and says what stays with the server | B1765 / C43-UTILITY | as above |
| C-43 | `03` §2, phase 5 goal, E5.2, WP0.3, WP1.11, WP2.2, WP5.2, WP5.3, WP5.6; new WP0.10 and WP5.8; new BLUF item 9; `05` BLUF item 4, WP0.3 row, new WP0.10 row | The plan follows | B1765 / C43-UTILITY | as above |
| C-44 | none | Nothing applied, as the commission says. The location is one row of `02` §6.6 (no value) and the note that he flags it to the owning team | B1765 / SECRET-LOC | CL:284-290; A9:213 |
| Question 10 | `05` question 10; `03` OQ-10 row; `02` §6.5, R24 | Precondition answered; two untested links named; recommendation (b) with its caveat; default unchanged; decision his | B1765 / GW-TRUST, B1765 / OQ-10 | A9:240-241, 259-261 |
| OQ-7 | `02` header, coverage note, P11, D11, change log; `03` header, BLUF 4 and 6, phase-0 inputs, E0.3, §6, §7, §8.3 lead and row; `05` BLUF, question 7, kit item 12, "not verified" | Answered in both halves | B1765 / GW-SOURCE | A9:255; CL:252-258 |
| A10 §6.1 (not a numbered correction) | `03` WP0.4, §5 contract-test row; `05` WP0.4 row | HP's 1.x jar taken from SDK 1.8.4.1 by SHA-256: two different jars carry the same file name | B1765 / JAR-HASH | A10:185-187, 201 |
| A9 §2.1 (not a numbered correction) | `03` WP0.4; `05` WP0.4 row | A stub of the gateway's three routes joins the test harness | B1765 / GW-STUB | A9:45-47, 53 |
| A9 D12 (not a numbered correction) | `03` S11, WP0.8, WP5.5; `05` new WP0.8 row | The report-field map has a no-hardware half | B1765 / REPORT-COLS | A9:244 |
| A9 §6.3 | `03` S7 | The two tenant tests and the relay test are written into the spike that already uses that tenant; no spike was added | B1765 / RELAY | A9:261, 290 |

### Searches behind this section

Every place in `02` and `03` that designs or plans deployment, onboarding or installation was found by reading both documents whole and by a count taken on the files as they stood before this pass (case-insensitive, by `/usr/bin/grep`): in `02`, `onboard` 30 lines, `install` 50, `deploy` 10, `uninstall` 4, the utility by name 4; in `03`, 15, 22, 10, 2 and 2; in `05`, 2, 4, 1, 0 and 0. Negative control `zzqxnotthere`: 0 in all three. Seventy-five lines of `02` and thirty-nine of `03` match one of those words; most are about installing an HPK or a bundle on one printer, a certificate, or Microsoft terms, and were read and left alone. The ones changed are in the row above.

In the utility's 98 C# files (`HPKU/src`): `soap` 0 hits, `httpclient` 0, `.bdl` 0, `discover` 0, `subnet` 0, `snmp` 0, `msiexec|docker|ssh |sc.exe|New-Service` 0, `oxpd` 1 (a comment). Positive control from the same run: `hpktool` 50 hits in 4 files. (The first, wider run over all file types gave `soap` 36 hits in 12 files: all in `.resx` resource files, 2 per file, which is that format's boilerplate; none in code.)

## 4. Points to ADD to the master list, Jira `OXPD2-1` (one ready sentence each; Tuesday posts them)

1. OP-1: Is the amended HPK Deployment Utility the operator's tool that starts and follows jobs which the Suite Server carries out, or must the utility do the work on each printer itself without the server? Default: the first, because the server must keep each printer's token, records and repair loop.
2. OP-2: Does "use the deployment utility" (C-43) also cover installing the server itself? Default: no; the server keeps its two packagings (C-17), and the utility has no code that installs software on a machine.
3. OP-3: The utility runs on Windows only; is a Windows PC for it acceptable at a site that takes the Linux packaging of the server? Default: yes, as for Workpath roll-outs today.
4. OP-4: Does the server's console also keep its own onboarding pages, or is the utility the only place a batch is started? Default: the utility only; the console shows status and repairs one printer.
5. OP-5: Where does the amended utility live and how is it released, given that a push to its main branch publishes a release today? Default: on a branch of its own repository, nothing to its main branch without your word, and not copied into `datasecau/OXPd_2`.
6. OP-6: May the amendment also change how the utility stores and passes the printer password for existing Workpath jobs, or is only the OXPd path to be done properly? Default: OXPd path only; Workpath jobs behave exactly as today.
7. OP-7: Who is meant to deploy the licence-server Azure Marketplace offer: Datasec only, or partners and customers too? Default: Datasec only; it bears on question 13 (sites with no internet).
8. OP-8: How many customers deployed the Azure side by the script and how many by the Marketplace offer? Default: both exist, so every gateway change ships as an offer version and as a script update.
9. OP-9: Is `v1.3.0` the gateway package live in the Marketplace today? Default: yes.
10. OP-10: Can the source of the phone app (HP Secure Authentication) be supplied, or may one sign-in message be captured in the test tenant? Default: capture it in the test tenant.
11. OP-11: Is `cc-api`, which was not among the repositories sent, the API of the older Keycloak back end and so not needed? Default: yes; not asked for again.
12. OP-12: The phone-link relay needs one address on each customer's gateway that accepts a request without a token, and a second update route for customers who deployed by script; go ahead on that basis? Default: yes, under "may change" (C-27), with the test in spike S7.
13. OP-13: Is there more of the earlier OXPd 1 work than what was sent on 2026-11-20 (another branch, a later working copy, the repository's history)? Default: no; what was sent is the last state.
14. OP-14: The README of the earlier OXPd 1 tree gives a printer administrator password as the "default", beside a lab address; is it a live password of a lab printer? Default: treated as live, never copied; whoever owns that printer should change it.
15. OP-15: Was the earlier OXPd 1 code ever run against a physical printer, and what was the "emulator" its author names (the tree was worked on a Windows ARM64 laptop)? Default: emulator only; nothing is treated as proven on hardware.
16. OP-16: Where did the two card keys written into the earlier OXPd 1 build come from, given that they are not today's Workpath card key? Default: made up or outdated; never carried into the product.
17. OP-17: May the earlier build's register and unregister tools be used once as a lab probe against the test printer, although they switch certificate checks off and register plain-HTTP addresses? Default: no; the phase-0 tests are written fresh.
18. OP-18: The repository `OXPD1` ("HP Authentication Suite OXPD V1.8") is empty; is it meant to receive anything? Default: ignored; new work goes to `datasecau/OXPd_2`.

Existing items on `OXPD2-1` whose state or text changed (four):

- Question 7 (source of the SharePoint app and of the gateway): ANSWERED IN FULL on 2026-11-20; the gateway is `hpam-api`, deployed by `hpam-marketplace`, and has been read (report A9).
- Sensitivity labels (the point raised from the SharePoint source): ANSWERED on 2026-11-20 (C-38), "Leave it out, as today".
- Question 10 (QR sign-in without MFA): the gateway has been read and does not check who sends an unlock message; two links of the attack are untested and will be tested in the test tenant; recommendation (b); default still (a), as Workpath; the decision is the product owner's.
- Question 13 (sites with no internet): a deployable licence server already exists as a second Azure Marketplace offer; who deploys it is OP-7; recommendation and default unchanged.

## 5. Items whose state changed on the kit list, Jira `OXPD2-2` (one ready sentence each)

1. Item 1 (the word to start, the project folder, the repository, the build pipeline): GIVEN on 2026-11-20 (C-42) for the no-hardware work; folder `OXPd_2`, repository `datasecau/OXPd_2`; the build pipeline is work package WP0.3, part of the work now started.
2. Items 4, 7 and 8 (the printers): the product owner holds an HP MFP M577 (C-39); its firmware version is not known, whether it may be wiped for developer mode is not known, and which OXPd generation it runs is not established, so one printer of each generation is still to be confirmed.
3. All 17 items: the product owner says all the kit is in hand and not configured (C-42); which items that covers is not stated and is being asked item by item.
4. Item 12 (the source code of the customer gateway): RECEIVED on 2026-11-20 (`hpam-api`, with `hpam-marketplace`; C-40) and read (report A9); still wanted: the phone app's source, or leave to capture one sign-in message in the test tenant.

Item 13 (the SharePoint source) was already marked received by B1760; no change.

## 6. What changes for the first build seat (the no-hardware work packages)

| Package | Changed? | What |
|---|---|---|
| Repository layout / WP0.3 | Yes | The server's admin API contract is its own project; no project for an installer or batch-onboarding screen for printers; the utility's code is not copied into `datasecau/OXPd_2` (default of OP-5) |
| WP0.4 | Yes | HP's 1.x jar from SDK 1.8.4.1, recorded by SHA-256 (two jars share the file name); a stub of the gateway's three routes added to the harness |
| WP0.5 | No | No new question to HP came from this pass |
| WP0.6 | Yes, smaller | F89 (sensitivity labels) no longer needs a check for scope: left out by ruling |
| WP0.7 | Yes | Its reading half is done by report A9; what is left needs the tenant |
| WP0.8 | Yes, new no-hardware half | The report-field map can be drafted against the 17 and 3 accepted columns |
| WP0.10 | New | The design note for amending the HPK Deployment Utility, and a build check. Not one of the twelve packages named with the word to start: Tuesday's and the product owner's call |
| WP1.1, WP1.3, WP1.4, WP1.5, WP1.10, WP3.8, WP3.12, WP4.1, WP4.2 | No | Not touched |
| WP1.11 (not on the no-hardware list, but its contract is) | Yes | Its onboarding calls are written down as a versioned contract, because the utility is later built against them |
| WP6.7 | No text change | The deviation register gains nothing by ruling; the sensitivity-label feature is "as today", so it is not a deviation |

## 7. Not done, and not read or verified

- **Nothing was run or built**: no code from any source tree, no build of the utility, no test. Every statement about behaviour is from reading, mine or a report's.
- **No network call, no Jira, no GitHub.** The Jira issues `OXPD2-1` and `OXPD2-2` and the repository `datasecau/OXPd_2` were not looked at; what the documents say about them is from `CLARIFICATIONS.md` (C-37, C-41, C-42).
- **A9's and A10's source trees were not opened.** Every `API/`, `MKT/`, `INF/` and `OX/` fact is taken from the two reports at the lines cited; I did not re-check a report line against the code. The reports' own limits apply (A9 section 10, A10 section 11), in particular: A9 read `02`, `03` and `05` by keyword, not whole.
- **The HPK Deployment Utility was read in part.** Whole: 16 small files (build properties, five enums, four entities, two utilities, one result model, one file-filter model, the release workflow, the tools readme). In part: `Worker.cs` lines 150-214, 355-464 and 735-1019 of 1,070 (460 lines); the six project files by search. Not read: the desktop application (6,179 lines in 26 C# files), the services and repositories, the seven migrations, `EncryptionUtils.cs` (deliberately: it holds a key), HP's HPKTool guide, the binaries. So "how many screens must change" and "what HPKTool can do to an OXPd printer" are not established, and the size of WP5.8 is an estimate.
- **Report A5** was read at lines 192-240 and 293-404, not whole.
- **Reports A1 to A4, A6 to A8, B1 to B3, C1, C2 and the review files R1 to R4 were not opened.** Where a new sentence relies on one of them, it does so through A9 or A10 and says so (for example "report A1 line 266 as cited at A9:277").
- **`review/B1757_APPLIED.md` was not read**; `review/B1760_APPLIED.md` was read whole (for its form).
- **`02`, `03`, `05`, `CLARIFICATIONS.md`, A9 and A10 were read whole** before the first edit.
- **The line numbers A9 and A10 give for `02`, `03` and `05`** are as the files stood after B1760; I placed each correction by its text, not by its line number, and every anchor was found exactly once by program.
- **The two links behind question 10 are untested**, as A9 says. The recommendation (b) in `05` rests on a reading of code and configuration.
- **Scores and sizes written by this pass are estimates**: R31 (3 and 3), WP0.10 (S-M), WP5.8 (M-L). The scores of R19 and R24 were left as they were.
- **C-34, C-35 and C-36** (a printer that can run OXPd, a reader and an old Windows PC, the HPSM Windows environment) were outside the commission's list and are not applied; `05` says so in its kit list.
- **The rendered PDFs** were checked by page count and by looking at two pages (page 1 of `05`, page 36 of `02`), not page by page.
- **Not a decision of mine, to be clear:** that the server executes and the utility fronts (section 8.7) is the design's default under OP-1; that the default of question 10 stays (a); that the server's own installer is outside C-43 (OP-2). Each is written as a default with the open point beside it.

## 8. Secrets

No secret value is in the three documents or in this file. New rows in `02` §6.6 give locations only. The two SHA-256 prefixes in `03` WP0.4 (`f2bb325f`, `debf18cd`) are checksums of HP's public SDK jar, taken from A10:185-187, and are not credentials. `EncryptionUtils.cs` in the utility was not opened. No tool output of this pass displayed a credential.
