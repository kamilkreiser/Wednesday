# B1757: the Fable review (B1753) applied to the OXPd architecture and plan

Datasec / OXPd, 2026-11-20. One writer. Documents edited: `02_architecture.md`, `03_plan-of-attack-and-build.md` (backups `*.pre-B1757` beside them). Reviews applied: `R1_parity.md`, `R2_platforms.md`, `R3_security-and-integration.md`, `R4_consistency-and-coverage.md`. No secret value is in this file: locations only.

## BLUF

1. All 92 findings in the four review files have a disposition: 69 APPLIED, 14 OPEN FOR THE PRODUCT OWNER, 8 SPIKE, 1 REJECTED.
2. No finding failed at its source. Every finding that changes a decision, a phase, an exit criterion or a requirement row was opened at the report line or library line it cites (column 5); two line numbers were off by one in the copy and are noted. The one rejection asks for no document change.
3. One finding is applied in part: R4-26 asks for a new CLARIFICATIONS entry, and that file is outside this pass.
4. Both PDFs were re-rendered with the house renderer (02: 36 pages, 03: 16 pages); the earlier PDFs are kept as `.pre-B1757`.

## How to read the table

Ids: `R1-nn` and `R4-nn` as in their files; lanes R2 and R3 both number from F1, so they are written `R2-Fn` and `R3-Fn`. Severity is the reviewer's, copied by program. "Source opened" is what this pass read to confirm the finding: `A1 line n` is a line of the report in `analysis/`; file paths are in the library copy (read-only); "card qNN" is the question card in `0_Brain/dashboard/data/decisions.json`; "internal" means the finding is one part of the documents against another and no outside source decides it. Where two lanes found the same thing it was applied once and both rows say so.

| id | severity | disposition | where applied, or why not | source opened |
|---|---|---|---|---|
| R1-01 | Major | APPLIED | 02 §3.1 sentence replaced; new §3.7 (F70-F80 and the map of seven rows carried in prose); F7, F8, §7.4 tagged. Applied once with R4-04. Program check after the edit: 90 of 90 A6 rows cited in 02 | A6 lines 549-640 (rows 14-85 opened one by one) |
| R1-02 | Major | APPLIED | 02 §3.1 baseline text, P17, new rows F81-F89, F58, F59, §5.6.2, §5.6.5; 03 E6.8, WP3.5, WP3.6, WP3.11, WP4.3, WP4.6. F87 and F89 carry a stated condition (dead `isSIOEnabled` switch; interface use unknown) | A2 lines 122-132, 187-193, 206-207, 282-290, 334, 339-340; A3 lines 227-257, 343; A4 lines 144, 290 |
| R1-03 | Major | OPEN FOR THE PRODUCT OWNER | OQ-4. Documents conform to the narrowest reading: OneDrive personal out until answered. 02 coverage note, §5.6.3, D34, R21, C19, BLUF 11; 03 BLUF 1, phase 3 order, WP3.9 conditional, WP0.6, §6 | `CypherOneDrive-main/.github/workflows/release.yml:130` (one assemble task, business); A1 lines 171, 240; card q15 option b detail |
| R1-04 | Major | OPEN FOR THE PRODUCT OWNER | OQ-7 (the SharePoint source must be supplied). 02 coverage note, P3, §5.6.3, R17, new R30; 03 phase-0 inputs, WP0.6, WP3.4, §6. Applied once with R4-08 | `HP-AuthSuite-Manager-main/src/Core/Utilities/AuthSuiteApps.cs:11-16`; `HPAuthenticationManager-main/app/src/main/AndroidManifest.xml:10-16`; A4 lines 237, 301 |
| R1-05 | Major | APPLIED | 03 new WP3.10, WP3.11, WP3.12, WP3.13; F15 into WP1.4 and phase 3 step 1; tile enablement into WP3.13 | internal (03 work-package tables against 02 §3) |
| R1-06 | Major | APPLIED | 02 F30 reworded: no licence-gated tiles | A5 line 90; A4 line 254 |
| R1-07 | Major | APPLIED | 02 §7.2 OneDrive/SharePoint row (`Mail.Send` when F38 is on, `User.Read`), first-run scope check; F38 names the consent and the changed sender; 03 WP3.10 | A6 lines 353-364; A4 line 177 |
| R1-08 | Major | SPIKE | New spike S9 (03). 02 §5.6.5 Pull and W17: exact whole-value match, rule fixed after S9, no longer "UPN"; 03 E4.3, WP4.3 | `UniversalPrint-main/.../directprint/PullPrintProcessor.kt:125, 618, 835-836`; `.../GetJobsIPPTask.kt:88`; A3 line 385 |
| R1-09 | Major | SPIKE | New spike S11 and WP0.8 (03). 02 §7.4, F63, C14: record shape stated as coded, marked unproven, `platform` conditional; 03 E5.5, WP5.5. Applied with R4-19 | `HPAuthenticationManager-main/.../reporting/ReportingClient.kt:51-90`; `.../reporting/StatsRepository.kt:97-114` |
| R1-10 | Major | APPLIED | 02 new F58, C12, §5.6.5 (capability report, non-commercial clouds); 03 new WP4.6, E4.8, E4.9, E4.10 | A3 lines 118, 246-257, 343; `UniversalPrint-main/.../directprint/PrintService.kt:115` |
| R1-11 | Minor | APPLIED | 03 E4.2 (two polling cycles plus transfer, interval stated in WP4.2); 02 §5.6.5 cites Workpath's 10 s. The reviewer's "60 s at p95" was not adopted: no source gives it. Applied with R4-13 | `UniversalPrint-main/.../directprint/DirectPrintProcessor.kt:76`; A6 line 488 |
| R1-12 | Minor | APPLIED | 02 §7.6: Workpath rows carry serial, licence state, last seen only | A5 lines 106, 146, 326 |
| R1-13 | Minor | APPLIED | 02 §7.5: rule kept (card q11 option detail), mixed-fleet difference and the "not found" case added | A5 lines 335-336; card q11 |
| R1-14 | Minor | APPLIED | 02 F5, C8; 03 phase-0 reader list by product (eight rows), §8 Q8 row. Applied with R4-03 | `HPAuthenticationManager-main/app/packaging_contents_release/hpk.xml:45-80` (six id pairs); A6 lines 183-192; A1 lines 282-288 |
| R1-15 | Minor | APPLIED | 02 F35, §5.6.2: reply is reply-all, no forward | A2 lines 128, 130, 161 |
| R1-16 | Major | OPEN FOR THE PRODUCT OWNER | OQ-5. Default: out under C-19; A6 row 24 outside the E6.8 gate until ruled. 02 §3.7, D34; 03 §8.1, E3.1, E6.8. Applied once with R4-05 | A6 lines 411, 574; cards q12, q15 |
| R1-17 | Major | APPLIED | 02 D18 fixed to a converter component on the server (card q16 option detail "server conversion"); the "server-held location" variant dropped; C11, §5.6.1, F88; 03 new spike S12, WP0.9, E3.5 | A2 lines 164-166, 206-207; card q16 |
| R1-18 | Minor | OPEN FOR THE PRODUCT OWNER | OQ-9. "(ruled, C-14)" removed from the reuse of `CLIENT_ID_UP`; marked assumption, not ruled. 02 §7.1, §5.6.5; 03 §8.1, §8.3. Applied once with R3-F10 and R4-10 | A3 line 420; A6 lines 366, 509; card q17 option a detail |
| R1-19 | Minor | APPLIED | 02 C14: device events removed | A1 line 403; `ReportingClient.kt:56-59` |
| R1-20 | Minor | APPLIED | 02 F56 marked more than Workpath, outside the parity gate; 03 E3.1, E6.8 (deviation register; approval is OQ-6) | A3 line 241 |
| R2-F1 | Major | APPLIED | 02 C3, D3, BLUF 7: CoreWCF for agents marked inferred, not HP's advice; 03 S2 widened to the client side, §8.1 language line | `OXPd1-NET-Java/Support-Forum/2025-01-24-37773710045075-...md:1, 10, 97, 114` (the reviewer's :113 is :114 in the copy); C1 lines 114, 361, 461 |
| R2-F2 | Major | APPLIED | 02 §5.8 failure behaviour, N7, §5.5.1, new R28: the OXPd 2 USB target is critical; stale-read guard; 03 S1 stale-tap measurement, WP1.2 | `OXPd2/Docs/SDK-Documentation/guides/usbAccessoriesRegistration.md:113` (reviewer's :112); `.../openapi/usbAccessories.openapi.json:8213` |
| R2-F3 | Major | APPLIED | 02 D33, BLUF 8 and 11, §4 signing row, R1: four undated HP items; 03 BLUF 3, §6 blocker, WP0.5. Written under the narrow reading of Q1 (OQ-1) | `OXPd2/Docs/platform-versions.md:9-21`; `OXPd2/Docs/oxpd2-download.md:42`; B3 lines 18, 378 |
| R2-F4 | Major | APPLIED | 03 E1.9 replaced (production bundle + HP's written answer; no group self-certified untested); 02 §8.2 signing paragraph, R10 | `OXPd2/Docs/publish.md:97-99`; B1 line 150 |
| R2-F5 | Major | APPLIED | 03 phase-0 inputs: HP developer account and LDB Service Key, pilot firmware, simulator guide, Windows lab PC with its virtualisation settings; §6 blocker | B1 line 207; B3 lines 345-351, 402-404; C1 lines 339-340 |
| R2-F6 | Major | APPLIED | 02 §5.8 keys paragraph, §6.2 Universal Print keys row, §8.1 Backup and HA rows, C12, C15, D28, W16, R14, new R26; 03 E6.4, WP5.7. Applied once with R3-F8 | internal (02 against itself); A3 §5.2 item 2 as cited |
| R2-F7 | Major | SPIKE | New spike S10 (03). 02 §5.8 (virtual IP on both packagings, NLB citation corrected, DNS not relied on), N7, D27, R26; 03 E6.4 | `OXPd1-NET-Java/Support-Forum/2024-01-05-24843001539475-How-to-set-up-the-NLB-environment.md:8-19` |
| R2-F8 | Minor | APPLIED | 03 §5 Contract row, WP0.4, WP1.2: the callback contracts are in the SDK's service-target specifications | `OXPd2/SDK/OXPd2-SDK-Beta-10/specifications/com.hp.ext.service.authentication/1/0/serviceTarget.openapi.json` (`postPromptResult` 5 matches); B3 lines 137-141, 295; B2 line 361 |
| R2-F9 | Minor | APPLIED | 02 C2, C19, §5.4, §5.5.1: endpoints named as in the Beta 10 specification; 03 S1 records the record type | `.../guides/usbAccessoriesRegistration.md:6`; `OXPd2/SDK/README_Beta_10.txt:16`; B3 line 138 |
| R2-F10 | Minor | APPLIED | 02 §5.4 `PostMessage(serial, messageId)`, C19; 03 WP3.12 | `.../guides/applicationServiceOverview.md:765, 773`; B1 lines 192, 293 |
| R2-F11 | Minor | APPLIED | 02 C9, §4 browser row; 03 E2.5 (device memory, soak test). The reviewer's "start at 300 KB" was not adopted: no source gives it. Applied once with R4-14 | `OXPd1-NET-Java/Support-Forum/2020-01-15-360038344494-Browser-Memory-problem.md:23`; C2 line 132 |
| R2-F12 | Minor | APPLIED | 02 N11, §4 browser row: two OXPd 1.x engines; 03 real-device test row, phase-0 device line | C2 lines 131-133 |
| R2-F13 | Minor | APPLIED | 02 §8.1 prerequisites, §5.6.5 Direct and delivery path; 03 S6 records the IPP-over-TLS port | `.../guides/printJobIppExtensions.md:28-30`; `OXPd1-NET-Java/Docs/oxpd-ipp-extensions-specification.md:81-83`; C1 line 123; C2 line 117 |
| R2-F14 | Minor | APPLIED | 02 §8.5: what uninstall removes marked unproven; 03 S8 pass condition | `.../guides/solutionManagerOverview.md:313-317`; B1 line 178 |
| R2-F15 | Minor | APPLIED | 02 §8.3 step 2a also reads `GetSignInMethods`; 03 S2 | C1 lines 138, 171 |
| R2-F16 | Minor | APPLIED | 02 §6.4 session-end bullet, §5.5.2 note: pages report the timeout, 300 s until reported | C2 lines 69, 74 |
| R2-F17 | Minor | APPLIED | 03 "seven assumptions" and "eight spikes" corrected to thirteen (S1-S13). Applied once with R4-15 | internal (03) |
| R2-F18 | Minor | APPLIED | 02 §5.6.1, D13: Print-URI no longer "for very large files"; 03 S6 600-page job on both paths | C2 line 141 |
| R2-F19 | Minor | REJECTED | No document change is asked for: the finding is against report B2, and 02 already says a new reader model needs a new signed bundle (§4 card-readers row; F5). Recorded as already carried | B1 line 318; 02 §4 |
| R2-F20 | Minor | APPLIED | 02 §5.5.1 sequence and note: `fullyQualifiedUserName` | B2 line 119 |
| R2-F21 | Minor | APPLIED | 02 §6.4, D7, N2, §4 identity row, C6, C14, §5.9 deny-list, new R22. Applied once with R3-F3 | B2 lines 125, 276, 386 |
| R2-F22 | Minor | APPLIED | 02 §8.2 new repair paragraph (depends on OQ-2), new R29 | B1 line 208; B3 lines 349-350; `.../guides/exampleOverviewGuide.md:155-157`; B2 line 72 |
| R2-F23 | Minor | APPLIED | 02 C19: five application agents named. Applied once with R4-28 | internal (02); B1 line 192 |
| R3-F1 | Major | APPLIED | 02 §6.2 key row (card-blob AND QR key, two routines), §6.5, D5 | Held at source by Tuesday (`CardValidator.kt:10` = `Encryptor.kt:12`, compared by hash). Not re-opened in this pass: files that hold a key literal were not opened. A1 line 544 |
| R3-F2 | Major | OPEN FOR THE PRODUCT OWNER | OQ-8. "Old and rotated" no longer asserted for this key; default: treated as live. 02 §6.2, §6.6 title, D5, new R27; 03 phase-0 key line | A1 line 544; CLARIFICATIONS C-3 (general sentence) |
| R3-F3 | Major | APPLIED | 02 §6.4 bullet 1, D7, N2, §4, C6, C14, §5.5.1, §5.9, new R22: no handle in OXPd 2 custom attributes. Applied once with R2-F21 | `.../openapi/authentication.openapi.json` (`customAttributes` description); B2 line 386 |
| R3-F4 | Major | SPIKE | S1 and S2 corrected (03): does each panel browser send the per-device credential on page requests. 02 §6.1 panel-pages rule and §6.4 binding marked unproven; new R23 | `.../guides/applicationServiceRegistration.md:129-134`; `OXPd1-NET-Java/Docs/oxpd-security-model-overview.md` ("HTTP Authentication", 1 match) |
| R3-F5 | Major | SPIKE | S1 corrected (03): token survival after soft reboot, power loss, firmware update; which credential `reissueInstallCode` accepts. 02 §6.2 states the consequence; new R29; turns on OQ-2 | `.../openapi/solutionManager.openapi.json` path `/solutions/{solutionId}/reissueInstallCode` (Role-Based: local device administrator only); `.../guides/exampleOverviewGuide.md:155` |
| R3-F6 | Major (cross-lane: R2 owns §8.2; reported because §6.3 rests on it) | APPLIED | 02 §8.2 steps 3-10 reordered (context with install, CA import, `reissueInstallCode`, exchange); §6.3; 03 S1 proves the order, WP1.11 | `.../guides/securityModel.md:105-109`; `.../guides/solutionPackagingUtility.md:162`; B2 lines 72-73 |
| R3-F7 | Major | SPIKE | S5 corrected (03): parts (c) and (d), the reverse direction. 02 §6.4 write-back made conditional; R12; new R25 | `HPAuthenticationManager-main/.../repository/MicrosoftSsoRepository.kt:137-149`; A1 lines 134, 476 |
| R3-F8 | Major | APPLIED | With R2-F6 (same places); E6.4 prints a Direct job from the second node | internal (02); A3 §5.2 item 2 as cited |
| R3-F9 | Major | SPIKE | New spike S13 (03). 02 §7.3, §8.5, W18, §5.6.5: orphan report, deregistration not promised; 03 WP4.5, E5.7 | 0 files match `deregister|unregisterPrinter|@DELETE` under `UniversalPrint-main/app/src/main` (control `api/v1.0/register`: 2 files); A3 line 153 |
| R3-F10 | Major | OPEN FOR THE PRODUCT OWNER | OQ-9, with R1-18 and R4-10. 02 §7.1 also carries the three bounding facts (client id in the device token, sovereign clouds, device code blocked) | A3 lines 118, 162, 420; A6 lines 366, 509; card q17 |
| R3-F11 | Major | OPEN FOR THE PRODUCT OWNER | OQ-10 (what to do with No-MFA + QR if the gateway does not bind the publisher). Default: as Workpath (C-7, C-16), risk recorded. The reviewer's "off until fixed" was not written as the design: that is the product owner's choice. 02 §6.5, new R24; 03 WP0.7 definition of done | A1 lines 274, 526 |
| R3-F12 | Major | OPEN FOR THE PRODUCT OWNER | OQ-2, with R4-01 (same places) | card q07 option a detail and default text; B1 line 586 |
| R3-F13 | Minor | APPLIED | 02 BLUF 6, §6.7 heading and lead; 03 E6.1, WP6.1. Applied once with R4-12 | internal (02 §6.7 W2, W3) |
| R3-F14 | Minor | APPLIED | 02 §6.1 boundary B2 | `OXPd1-NET-Java/Support-Forum/2021-07-20-4403971370131-Support-of-TLS-Client-Authentication.md:37, 88`; C2 line 118 |
| R3-F15 | Minor | APPLIED | 02 §6.3 Protocol bullet | C2 lines 124-125 |
| R3-F16 | Minor | APPLIED | 02 §7.2 sign-in hub source cell and OneDrive row source; F78 | A1 line 174; A6 lines 349-355 |
| R3-F17 | Minor | APPLIED | 02 §6.6 retitled "principal"; eight location rows added (locations only) | Report lists only (A1, A2, A3, A4, A5, A7, B3, C1 section 8): the secret-bearing files were NOT opened; `Rentals.cshtml` located by file name |
| R3-F18 | Major (R7 records half) | APPLIED | 02 R7; 03 §6 gateway blocker, S7 | A6 line 345; internal (02 M1, M4) |
| R3-F19 | Minor | APPLIED | 02 new risks R22-R30 | internal |
| R3-F20 | Minor | APPLIED | 02 W2 future key custody | internal (inferred, as the reviewer says) |
| R4-01 | Major (Kam's reading; see open readings) | OPEN FOR THE PRODUCT OWNER | OQ-2. Documents conform to the card's option detail: OXPd 2 discards the admin password; a stored copy is "not ruled". 02 §4 trust row, §6.2, §8.2 step 9 and repair; 03 S1, §8.3. Applied once with R3-F12 | card q07: option a detail "newer ones discard it"; default text |
| R4-02 | Blocker | APPLIED | BLOCKER. 02 C2 technology cell (own generated clients; HP's library lab-only), BLUF 7, R1, R16; 03 WP0.4, E0.4 (release build fails on `OXPd2Lib.dll`). Cost recorded: HP supports only its signed library | Held at source by Tuesday; re-read here: card q20 option a detail; B3 lines 295, 501 |
| R4-03 | Major | SPIKE | S3 corrected (03): first step taps each of the six ids on the Workpath printer. 02 F5, C8; 03 WP1.3, phase-0 list. With R1-14 | card q08 option a detail; A1 lines 282-288; A7 line 392; `hpk.xml:45-80` |
| R4-04 | Major | APPLIED | With R1-01 | A6 lines 549-640; program count over 02 (72 of 90 before, 90 of 90 after) |
| R4-05 | Major | OPEN FOR THE PRODUCT OWNER | OQ-5, with R1-16 | A6 lines 411, 574; cards q12, q15 |
| R4-06 | Major | APPLIED | 03 E3.1 and E6.8: three named classes of deviation with the C-entry for each ruled one, a deviation register, named items outside the gate; unruled choices need approval (OQ-6); WP6.7 | internal (02 F18, F38, F43, F51, F56, F63; cards q16, q17, q21) |
| R4-07 | Major | APPLIED | Phase order. Criteria fixed: E3.1 excludes F17 (exits E4.3) and F18, F43, F77, F78 (exit new E5.8); E4.1 through the admin API; E4.7 moved to E5.7. Order fixed: new WP1.11 in phase 1. 03 §3, §4, §6 | internal (03 against 02) |
| R4-08 | Major | OPEN FOR THE PRODUCT OWNER | OQ-7, with R1-04 | `AndroidManifest.xml:10-16`; A4 line 237 |
| R4-09 | Major | OPEN FOR THE PRODUCT OWNER | OQ-11. 02 §8.6: the central-server sentence no longer credits C-26; not offered in release 1 | card q05 options a and b |
| R4-10 | Major | OPEN FOR THE PRODUCT OWNER | OQ-9, with R1-18 and R3-F10; the reviewer's token test is in spike S13 | card q17 option a detail; A3 line 420; A6 line 509 |
| R4-11 | Major | APPLIED | 03 new WP5.7 (HA pair); 02 N7 (2-minute target as a target), §8.1 HA row with the database topology note, §5.8 | internal; forum thread of R2-F7 |
| R4-12 | Major | APPLIED | With R3-F13 | internal (02 §6.7) |
| R4-13 | Major | APPLIED | 03 E4.2, E1.1, E2.5 (2 s marked own budget), E6.6 (threshold is OQ-14) | C1 line 200 (10 s script limit); 02 N6 |
| R4-14 | Minor | APPLIED | With R2-F11 | C2 line 132; C1 line 466 |
| R4-15 | Minor | APPLIED | With R2-F17 | internal (03) |
| R4-16 | Minor | APPLIED | 03 E2.4: architecture test instead of a diff between parallel phases | internal (03) |
| R4-17 | Minor | APPLIED | 03 WP1.4 (minimal enrolment), WP3.3 (enrolment completeness) | internal (03) |
| R4-18 | Minor | APPLIED | 02 N11, new F80: panel classes restated | A6 lines 490, 580; card q09 default text |
| R4-19 | Minor | APPLIED | 03 E5.5; with R1-09 | internal; `ReportingClient.kt:66-90` |
| R4-20 | Minor | APPLIED | 02 N9 lists the real licence payload | internal (02 §7.5, §7.6) |
| R4-21 | Minor | APPLIED | 02 header (C-1 to C-30), §8.2 step 1a (S1); 03 Q1 row (D33), §6 blocked-spike list | internal |
| R4-22 | Minor | APPLIED | 02 §5.8, §8.1 (sizing inferred), §4 (HP validation of HPKs not ruled) | cards q10, q19 |
| R4-23 | Minor | APPLIED | 03 §8.1: the three uncited report questions added with their assumptions; HP Token Proxy noted; §8 intro. The closed-network case is OQ-13 | A4 line 312; A5 line 367; A6 line 509; B1 line 627 |
| R4-24 | Minor | OPEN FOR THE PRODUCT OWNER | OQ-12. 03 §8.1 OXPd 1.9 line; design stays on 1.8.4.1 | C1 lines 405, 515; CLARIFICATIONS C-1 |
| R4-25 | Minor | APPLIED | 02 header records the reading (OQ-15); §8.1 outbound proxy | CLARIFICATIONS C-1 |
| R4-26 | Minor | APPLIED | IN PART. 02 header now says where the card option detail lives. NOT DONE: the proposed new CLARIFICATIONS entry (C-31), because CLARIFICATIONS is outside the files this pass may write | `0_Brain/dashboard/data/decisions.json` (25 cards read by program) |
| R4-27 | Minor | APPLIED | 03 F rows named in work packages (F15 WP1.4; F17 WP4.3; F18, F43, F61, F67, F77, F78 WP5.3; F30, F36 WP3.13; F38 WP3.10; F42 WP3.12; F64 WP1.1); S6 scan upload; S1, S2 first-request check | internal (03 against 02) |
| R4-28 | Minor | APPLIED | With R2-F23 | internal (02) |
| R4-29 | Minor | APPLIED | 03 phase-0 FS 4.7 device, E6.8 lowest and highest firmware, real-device row; 02 D32 "expected, untested" | C2 line 260; cards q09, q25 |

## Counts (by program, from the table above and from the four review files)

| disposition | count |
|---|---|
| APPLIED | 69 |
| OPEN FOR THE PRODUCT OWNER | 14 |
| SPIKE | 8 |
| REJECTED | 1 |
| **total** | **92** |

Findings in the four files, counted by matching the id column of each findings table: R1 20, R2 23, R3 20, R4 29, total 92. The dispositions sum to the same number. By the reviewers' severity: 1 Blocker, 44 Major, 47 Minor.

## REJECTED

- **R2-F19**: No document change is asked for: the finding is against report B2, and 02 already says a new reader model needs a new signed bundle (§4 card-readers row; F5). Recorded as already carried. Read: B1 line 318; 02 §4.

No finding was rejected for failing at its source.

## OPEN FOR THE PRODUCT OWNER (14 findings, fifteen questions)

The findings map to the open questions written out in `05_readiness-to-build.md` and listed in 03 §8.3. OQ-1, OQ-3, OQ-6, OQ-13, OQ-14 and OQ-15 come from findings whose own disposition is APPLIED (the text was corrected and a question remains).

| OQ | Title | Findings |
|---|---|---|
| OQ-1 | What "HP confirmed" covers | reading of Q1; R2-F3 |
| OQ-2 | A stored admin password for the newer printers | reading of Q7; R4-01, R3-F12 (with R3-F5, R2-F22) |
| OQ-3 | "Full match" means what Workpath ships, and no more | reading of Q15 |
| OQ-4 | OneDrive personal | R1-03 |
| OQ-5 | Sign-in for HP Advance and LRS VPSX | R1-16, R4-05 |
| OQ-6 | Approval of the design choices that differ from Workpath | R4-06, R1-20 |
| OQ-7 | The SharePoint app's source | R1-04, R4-08 |
| OQ-8 | Is the card and QR key in the library live | R3-F2 |
| OQ-9 | The server's use of Datasec's Universal Print registration | R1-18, R3-F10, R4-10 |
| OQ-10 | QR sign-in without MFA if the gateway does not check the sender | R3-F11 |
| OQ-11 | One central server for several sites | R4-09 |
| OQ-12 | Anything newer than OXPd 1.8.4.1 from HP | R4-24 |
| OQ-13 | Sites with no internet | R4-23 |
| OQ-14 | The pilot's defect threshold | R4-13 |
| OQ-15 | The reading of "intra-environments" | R4-25 |

## SPIKE (8 findings)

| Spike | What changed | Findings |
|---|---|---|
| S1 (corrected) | install order, token survival, re-issue credential, USB record type, stale tap, page credential | R3-F4, R3-F5 (and applied findings R2-F2, R2-F9, R3-F6) |
| S2 (corrected) | client-side half; `GetSignInMethods`; 401 challenge on the WebKit panel | R3-F4 (and R2-F1, R2-F15) |
| S3 (corrected) | first step on the Workpath printer for the two conditional readers | R4-03 |
| S5 (corrected) | reverse direction, parts (c) and (d) | R3-F7 |
| S9 (new) | Pull identity value | R1-08 |
| S10 (new) | HA switch-over on both packagings | R2-F7 |
| S11 (new) | reporting record shape | R1-09 |
| S13 (new) | Universal Print registration client and removal | R3-F9 |
| S6, S7, S8 (corrected), S12 (new) | IPP port, large jobs, scan upload; tenant with no interactive method; uninstall read-back; converter fidelity | from applied findings R2-F13, R2-F18, R4-27, R3-F18, R2-F14, R1-17 |

## NOT DONE

- **R4-26, second half**: the new CLARIFICATIONS entry copying each card's title, default text and tapped option detail was not written. CLARIFICATIONS is not one of the files this pass may write.
- Nothing else: every finding id is named in a change-log entry of 02 or 03 (checked by program: 92 of 92).

## FOUND / TESTED / HOW

- **Edits** were made by three scripts for 02 (133 replacements, plus 1 later) and two for 03 (82, plus 3 later), each replacement required to match exactly once or nothing was written. The existing change-log entries were not altered: the new entries are appended after the old "Still owed" line.
- **Checks run after the edits, by program**: A6 rows cited in 02: 90 of 90 (72 before). Every F id cited in 02 or 03 is defined in 02 (74 F rows). Every work package cited is defined. Spikes defined S1 to S13, none cited that is not defined. Risks R1 to R30, decisions, weaknesses: no reference to an undefined id. The 25 answers in 03 §8 against CLARIFICATIONS: 25 of 25 match label and C-number. Leftover-phrase search (for example "S1-S8", "six decoders", "six application agents", "HP's own advice", "in scope for release 1", "under 2 MB"): 0 hits outside change-log quotations, with the positive control that three phrases quoted inside the new change-log entries were found (1 hit each).
- **Secrets**: no secret value was printed by any command in this pass. Source lines were displayed with string literals of 16 or more characters replaced by a marker; files that hold key literals, keystores, `config.properties`, `.cfg`, `.pem` and `.key` files were not opened. Both documents were scanned for secret-shaped strings of 32 or more characters: all hits are file paths.
- **Not tested**: nothing was built or run against a device or a tenant. Section numbers cited as `[A2 §4.3]`, `[A1 §4.3-4.4]`, `[A4 §4.2-4.3]`, `[C1 §4.17]` in the new text are the reviewers' and were not all opened; where this pass opened a source it cites the report line instead. The mermaid diagrams were edited as text and not rendered. The PDFs were checked by text extraction (the new entries are present; absent from the backups) and by eye on one page each.
- **Instrument notes**: two of the reviewers' line numbers are one off in the library copy (`usbAccessoriesRegistration.md` 112 is 113; the forum thread's 113 is 114); the documents cite the lines as opened here. A search for a bundled specification file in the SDK's `specifications/` folder found none at depth 2, so the reviewer's suggestion to use it was not written into WP0.4.
