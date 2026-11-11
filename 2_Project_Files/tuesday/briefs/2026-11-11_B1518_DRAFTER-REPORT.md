STARTABLE: YES

# B1518 DRAFTER REPORT (kit for seat R217, HPSM-POC records pass for #310 / #311 / #309 / #312)
Drafted 2026-11-11 19:37 to 19:55 AEDT (`date`). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1518_SEAT-R217_hpsmpoc-records-309-312.md` (233 lines, 14 Stamp slots + the last line as four-underscore lines; 0 non-ASCII bytes; an identical `.pre-stamp` beside it, `cmp` equal). Model Sonnet (`claude-sonnet-5-5`, level inside the launch quotes), rows C7 line 97 and G3 line 110 of `model-routing.md`, model id line 23 of `models_latest.json`.

## BLUF
1. One records pass, five analysis entries (C-359 to C-363: the 405/406 ruling, #309, #311, #312, #310 + the 271 correction), 16 Jira comments, up to 9 moves to Done in three slot groups, at most one create. 26 writes at most.
2. **Already recorded by R210, so dropped (checked at source):** user guide v0.4 = C-339, D60 deletion = C-340, the two guide tickets = HPSMPOC-468 and -469 (both read whole: marker and C-339 citation present). The seat comments on 468 only because #309 builds it.
3. **Two statements in the record are wrong at main and are corrected, with no ticket:** (a) comment 41012 / C-347 "the SDK no longer floats": `global.json` is a floor (10.0.401, latestFeature), hosted job installed 10.0.404; HPSMPOC-271 gets a correcting comment (stays Done); the SDK pin is "awaiting the product owner", never decided. (b) The B1496 gate's Minor "ci.yml never runs test_hidden_characters.py" is FALSE at source: ci.yml:630 -> validate.sh:21 -> test_security_baseline.py `main()` loads every `test_*.py` of the folder (lines 2856-2858). So the "ci.yml no hidden-characters step gap" is NOT ticketed; it is corrected in C-362.
4. **New finding nobody had ticketed:** main's own push run of #310's squash (b34046d1, run 42978565032) is RED on `api on SQL Server (api-assessment)`: 2 of 1431 tests (DemoResetUnseededTests.Never_seeded..., HostedDemoSeedRulesetDoorTests...), SqlException Execution Timeout Expired in Migrate (1 m 7 s, 1 m 8 s); the next three main commits are green (21 success + 1 skipped). Goes into the open-points ticket and C-363.
5. Done-rule outcomes the kit sets (Tuesday's slots decide): MOVE-A 461, 432, 409, 468, 465 (built by these PRs); MOVE-405 (declined by the ruling); MOVE-CLOSED 436, 439, 399 (met at main by earlier landings). Comment only: 462, 406, 357, 356, 408, 228 and the 271 correction.

## Per key: what the seat writes
| Key | Writes | Why (Done-when read at source) |
|---|---|---|
| 461 | comment + Done (MOVE) | "built and merged to main, or declined": ApiSteps.tsx:161 has no max-w; edges 1440: 1280.41 -> 1397.59 (review). Profile card :97 and follow-up panel :99 keep max-w-3xl -> ticket point 2 |
| 432 | comment + Done (MOVE) | "built or declined": FindingDetail.tsx TableScroll named by the caption; axe 1 -> 0 at 360 |
| 409 | comment + Done (MOVE) | "each item built or declined": item 1 by #274 (comment 40651), item 2 (region) by #309: 1 -> 0 node in 34 of 34 cells; keyboard extra Tab stop stated |
| 468 | comment + Done (MOVE) | title at steps.ts:144 reads "Delivery phases: ..."; ruling 14:34 "Match the menu" recorded in C-360 via slot RULING-468 |
| 465 | comment + Done (MOVE) | "built and merged, or declined": TrainingScreen.tsx:27/:34/:36; look probe not re-run by the review (said so) |
| 405 | comment + Done (MOVE-405) | Done-when 2nd clause "recorded as declined": met by C-359 + the 16:31 ruling; move needs RECORDS = WRITE |
| 436 | comment + Done (MOVE-CLOSED) | #302 (856d15d1): ReportingEndpoints.cs:186-187 refuses with narrative.no-findings; 2 tests; measured by comment 40710 |
| 439 | comment + Done (MOVE-CLOSED) | #300 (0820efe9): EngagementOverview.tsx:242/:245; 3 px / 3 px on cells with both kinds |
| 399 | comment + Done (MOVE-CLOSED, Tuesday's call) | all 4 clauses read met at main (menu 20 of 20 at 1024; stress 390 in 8 of 8; ring + line 320 met per comment 40747); evidence is probes at main, not part of the four PRs |
| 462 | comment only | fill-vs-outline fixed (globals.css:114-116) but review half neither done nor scoped; sidebar rows and skip link still square on focus |
| 406 | comment only | item 4 built (#311), item 5 declined (ruling), item 1 built earlier; items 2, 3 neither -> open |
| 357 | comment only | mock half met (360 in 8 of 8); UAT half never measured |
| 356 | comment only | line-break item pinned (#301) + bounded with:/image/retry pins (#311); unread bodies still not settled |
| 408 | comment only | item 2 part (a) built (#312), part (b) held for product owner |
| 228 | comment only | N-5 now built (#298, entra.ts:312); N-7 second half open; no Done-when line |
| 271 | correcting comment (Done, no move) | "the SDK still floats" |
| NEW | one create, labels landing-minor + rec-2026-11-11 | 4 points: a11y.spec.ts:39 near 30 s limit (3 reports); max-w-3xl card/panel; startingOwner code-point cut; red SQL Server shard on #310 squash. Duplicate searches 0 (a11y.spec, max-w-3xl, startingOwner; control Pkcs lists 16) |

## Facts re-measured by the drafter (instrument, time)
- Code main `c014503d38d5648b691ca4d3a86d91bf44f8caae` (`gh api -X GET commits/main` 19:37:49). PRs 309/310/311/312: merged true, 1 parent each, file counts 11/1/7/4, squash shas and times as in the kit (`pulls/<n>` GET). Check-runs per squash (`commits/<sha>/check-runs`): #310 22 = 19 success + 1 skipped + 2 failure; #311, #309, #312 22 = 21 success + 1 skipped. `compare` to main: ahead 3 / 2 / 1 / identical, behind 0.
- Open PRs on code repo 0; analysis repo 0 open; `pulls/99999` 404. Analysis main `49eebb28` (#195), raw `CLARIFICATIONS.md` 6203 lines, 2020801 bytes, sha256 prefix f58175c82adab617, 358 `### C-` headings, newest C-358 line 6196, C-263 line 5114 (once), C-359 0, `records/b1518` 0 (control `records/b1498` 1). Parents of #193/#194/#195: 2 each.
- Jira (REST GET, read in-process, token never printed): 405/406/461/432/409/468/465/462/439/436/399/357/356/408/228/323/469 Backlog, 271 Done; comment counts and newest ids in the kit. `key > HPSMPOC-469` reads 0. Duplicate searches: `a11y.spec` 0, `max-w-3xl` 0, `startingOwner` 0, `REC-LAND-` 0, `Phase decision` 0; controls `Pkcs` 16 keys, `Execution Timeout Expired` {273, 282}, `test_hidden_characters` {356, 152}.
- Code lines at c014503d (`gh api -X GET contents ... Accept raw`, `grep -n -F` / `awk NR=n`): every pointer in the kit's table (ApiSteps 161/97, FollowUpPanel 99, FindingDetail 38/175, PlaybookShell 20, steps.ts 144 (was 143 at 009421a2, the added ruling comment), steps.test.ts 29, GlobalNav 50, partner/parts.tsx 49, TrainingScreen 27/34/36, globals.css 114-116, remediation-store 56, RoadmapScreen 99, EngagementOverview 242/245, customer/parts.tsx 69, CustomerManagement 95/114, ReportingEndpoints 186-187, test class `[Fact]` 2, entra.ts 312/359/380, refresh-fanout 5 `it(`, csproj 32, global.json 3-4, ci.yml 46-48/189-191/579/630, validate.sh 21, test_security_baseline 2811/2856/2858, test_ci_workflow 34/42/50/416/429/444/1120). Counts: FindingDetail `overflow-x-auto` 0, ApiSteps `max-w-3xl` 1, PlaybookShell `<main` 1, steps.ts `Service offers` 0.
- Failed job log (job 130383313163, `actions/jobs/<id>/logs`): "Failed! - Failed: 2, Passed: 1429, Total: 1431"; error lines as quoted in the kit.
- Rulings: 468 relay read in `B1497_ADDENDUM-1` (14:34:14, option a "Match the menu"; the card id on its line 3 is NOT in the kit). 405/406: read the card by `decision_queue.sh show hpsmpoc-405-406-two-held-items-1111` into scratch (the exact id from Tuesday's own daily note line 93): option (a) "Leave both as they are" (detail "record both as declined; nothing changes on screen"), `ruled_ts` 2026-11-11T17:18:34+11:00; the daily note says the tap was 16:31 and a 17:03 store commit reverted then re-applied it. **The scope of the card is 405 whole and 406 ITEM 5 only** (its BLUF), not all of 406; the commission's wording "405 and 406 declined" is therefore narrowed in the kit: 406 stays open (items 2 and 3).
- Scanner pass: the 16 comment texts and the create description were scanned by the drafter with a Python regex set (Tuesday, gate, seat, brief, coordinator, kit, drafter, lane, HP, @, URL, B-numbers, 20+ hex, hpsmpoc-letter, nine names, other C-numbers, non-ASCII): 0 hits after fixes (4 found and fixed: "gate" in 357, "lane" and "B734-n" in 356, "@" in 356); summary scanned by eye.

## D-decisions (drafter)
- D-1 Five entries, not one per PR plus extras: ruling entry first (its numbers are cited by 405, 406 texts). The hidden-characters correction lives in C-362; the 271/SDK correction, the red shard and the open-points ticket in C-363.
- D-2 405's move is gated on RECORDS = WRITE (the Done-when needs the declination recorded).
- D-3 MOVE-CLOSED is a separate slot (436, 439, 399 were not changed by the four PRs; they are builder hand-overs the earlier C-324 entry left to a later pass). 399 is flagged as the one that needs Tuesday's acceptance of probe evidence.
- D-4 `REC-MERGE` word `FF` kept as commissioned but defined as "seat lands its own branch by the B1493 route" (analysis repo has a remote and CodeQL; head-pinned merge commit), not a fast-forward.
- D-5 The 357/399/439/228/436 closures are carried although they predate the four PRs, because the builders (#309, #312) handed them to the records seat and the earlier landing entry deferred them.
- D-6 No BACKLOG / JIRA.md / history appends (HPSM-POC's R210/R211 passes wrote none); left to Tuesday.
- D-7 Clocks: JIRA DONE 60, RECORDS 100, HARD STOP 130 min after Step 0 (26 writes), absolute 23:30.

## Q-questions for Tuesday (each with a default)
- Q-1 Slot RULING-405-406: the two times differ (tap 16:31 vs store ruled_ts 17:18:34). Default: stamp "16:31 on the live board as relayed" (the entry prints both times, "not reconciled").
- Q-2 The commission says "405 and 406 declined"; the card covers 406 item 5 only. Default: as the kit (406 stays open, comment only). Say if you meant all of 406.
- Q-3 MOVE-CLOSED for 399: accept the builder + review probes (menu 20 of 20, stress 390 in 8 of 8; the review reproduced the control in 4 of 8 cells) as the evidence? Default COMMENT-ONLY for the slot as a whole; set it CLOSE-IF-CHECKED only if you accept 399.
- Q-4 462 "review half" could be scoped as its own ticket to meet its Done-when; the kit does not do it ("awaiting the product owner"). Default: leave.
- Q-5 HPSMPOC-323 (landed #300 per C-324's census, never checked in Jira) is not in this pass. Default: out of scope; name it in the next pass.
- Q-6 The red SQL Server shard on #310's squash: the kit forbids any CI re-run. Default: record only; a later seat may look.

## UNMEASURED
No review site / UAT / demo page requested. Figures from the builders' probes and the reviews (axe counts, edges, 224 of 224, 2045 of 2045, 20 of 20 etc.) are RELAYED from the four STATUS and four VERDICT files, marked so in the texts, and the seat re-reads each line. The look of the Training page and the focus ring are not judged. Whether the red shard is a recurrence of 273/282/308 is not confirmed (said so). The card store's 17:18:34 vs the tap at 16:31 was not reconciled. The `Done` transition id (41) was not re-read for these keys (the seat reads it per key).

## Outside-the-fences disclosure
Read: Tuesday's own `0_Brain/daily_tuesday/2026-11-11.md` lines (inclusion greps on 405/406, 16:31, Match the menu); `decision_queue.sh show hpsmpoc-405-406-two-held-items-1111` once, output to scratch, read through an inclusion filter on the id (no `list`). Ran `gh api -X GET` only (pulls, commits, check-runs, contents raw, compare, matching-refs, actions job log) under the project's `GH_CONFIG_DIR`; Jira GET only through my scratch reader `/private/tmp/b1518-drafter/jr.py` (credentials read in-process by name, never printed). No git verb in any repo, no write outside the two kit files, the report and `/private/tmp/b1518-drafter/`. I never typed `cd` (two scratch variable names contained "cd_" as text only). The pretool hook advisories about case-sensitive greps fired; every absence I rely on (Match the menu 0, REC-LAND4 0, a11y.spec 0) came with a control from the same file or query. A Write call's ` ` escapes landed as literal U+2028/U+2029 in kit line 61; found by a non-ASCII scan and replaced by plain text in both copies (kit now 0 non-ASCII bytes).
