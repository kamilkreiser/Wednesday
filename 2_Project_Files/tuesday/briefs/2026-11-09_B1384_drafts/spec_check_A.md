# Spec check: A_partner_readiness_spec.md against the layout v2.1 (drafter, 2026-11-09)

Marks: MEASURED = printed by a named program in this check; UNMEASURED = not run.
Instruments: `python3 -I -B` (regex extraction of the JS arrays from the raw HTML lines, no eye reading),
`/usr/bin/grep -i` with a control, `sed -n` over the read-only worktree `.tools/b1380/base` (HEAD 2075486, confirmed by `git log --oneline -1`).
Layout file = `.../kam_attachments_1109/f-84472617d43a_..._Layout_Alignment.html` (L21). Cross-check = the v2.0 demo (D20).

## BLUF
- **Layout transcription in the spec: 0 mismatches.** 16 statements, order, 4 group names, group membership, intro, caveats and seed state all MATCH the layout (MEASURED).
- **Code pointers at main 2075486: 3 mismatches or omissions, all small** (below). Nothing the spec says about the layout is wrong.
- **Most dangerous one:** `ReadinessContentTests.cs:21` is `Assert.Equal(6, ContentSeeder.SeedFromDirectory(...))` (a COUNT of packages), and `:22` lists the six versions. The spec (section 2.4) names only "the catalog list assertion". Adding package 0.7.0 turns BOTH red, and the test's name also says "010_030_040_050_060_and_061". A builder who fixes only the list will still have a red test on the count. (MEASURED, lines printed.)
- A second hazard the spec does not state: `locateQuestionSet` returns the FIRST package holding the set, in `PACKAGES` order, so after 0.7.0 is appended it STILL returns 0.3.0 (pinned by `content.test.ts:115-116`). The Firmware task and the hub's "start" button therefore keep using 0.3.0 unless the builder adds a separate `readinessPackage`. The spec's step 3 does say to add `readinessPackage`, but R4 words it as "if `locateQuestionSet` starts returning the new set". DERIVED from registry.ts:118-124 + content.test.ts:115-116; not run.

## 1. Layout statements (MEASURED, python3 -I -B regex over L21 line 732 and 791)
| Item | Spec | Layout | Result |
|---|---|---|---|
| `const READINESS=[...]` | section 1.3, 16 rows | L21:732, 16 entries | MATCH, 16 of 16 byte-equal (string compare of each spec cell with the extracted array element) |
| Order 1..16 | table order | array order | MATCH |
| `readinessGroups` | 4 names | L21:791: Strategy and engagement / Assessment and expertise / Implementation and delivery / Managed service and growth | MATCH |
| Group membership | rows 1-4, 5-8, 9-12, 13-16 | `slice(j*4,j*4+4)` at L21:733 and L21:805 | MATCH (checked per row: group number = (n-1)//4+1, group name = array element) |
| Heading format `${j+1}. ${g}` | section 1.3 | L21:805 `<h3>${j+1}. ${g}</h3>` | MATCH |
| No trailing full stops | section 1.3 note | none in the 16 strings | MATCH |
| D20 identical | section 1.5 | D20:362 and D20:421 equal L21:732 and L21:791 (list equality True) | MATCH |
| Intro lead | "Establish how prepared your organisation is to sell, assess, implement and support HP print security services." | L21:805, substring present | MATCH |
| Panel intro | "Select the statements that reflect your current capability. These are draft working statements, not official HP accreditation criteria." | L21:805, printed | MATCH |
| Caveat "illustrative" | "16 illustrative capability statements" | L21:805 and L21:733; also 'Illustrative capability assessment' at L21:804 | MATCH |
| Caveat "draft examples" | "The statements in this interactive version are draft examples." | L21:733 | MATCH |
| Seed state | first 11 ticked, L21:667 | L21:667 `readiness:Array.from({length:16},(_,i)=>i<11)` | MATCH (per area 4/4/3/0, arithmetic) |
| Band chip and text | thresholds 12/8/4, "Band definitions from the user guide: 12-16 Ready to start; 8-11 Solid foundation; 4-7 Foundation building needed; 0-3 Let's connect." | L21:805 printed | MATCH |
| Priorities | first 5 unticked, numbered 01.., group name under each; empty text "No unchecked statements. Validate delivery capacity and evidence quality before offering customer engagements." | L21:805 printed (`slice(0,5)`, `padStart(2,'0')`) | MATCH |
| "Next customer engagement" panel text | present | present on L21:805 (phrase found) | MATCH (text of the sentence itself not compared char by char: UNMEASURED) |
| Metric tiles | Readiness score / Capability coverage / Learning priorities / Practice areas with the captions listed | L21:805 printed for 3 of 4 captions; "Self-reported readiness only" found | MATCH |
| No band "plan" in the layout | section 1.4 | the only "next 30 days" is L21:730, the ACTION PLAN table, not a readiness band | MATCH |
| "Playbook Partner Readiness" absent from the layout | section 1.1 | 0 hits (`/usr/bin/grep -i -c` = 0; control `partner readiness` = 6 lines) | MATCH |
| Line pointers into L21 (661, 733, 759, 804, 805, 828, 851, 853, 956) | listed | each string found on the cited line | MATCH |
| Two other area-name lists | section 1.6 | L21:733 has 'Practice strategy / Delivery skills / Operational readiness / Commercialisation' | MATCH (spec chose L21:791, which is what the sidebar route renders) |

Not in the spec but present in the layout (not a mismatch, for the builder's information): the tile 'Partner readiness' also appears at L21:701 (a non-partner-home page) with a "Sample capab..." caption; 'Practice readiness' at 804, 956, 1115. UNMEASURED beyond the grep.

## 2. Code pointers at main 2075486 (MEASURED, `sed -n` of the cited line and a string test; the strings were chosen loosely, so an OK means "the thing is on that line", not "the claim is true")
All of these OK: registry.ts 21, 69, 118, 126; content.test.ts 115, 116; ShowcaseSeeder.cs 82, 89 (`ReadinessTicks = [1, 2, 3, 5, 6, 8, 9, 11, 13, 14, 16]`, spread 3/3/2/3), 164-171 (167 `$"Q-RDY-{n:00}"`), 459-460; assessments/page.tsx:4; readiness/[assessmentId]/page.tsx:8 ("Partner readiness self-assessment"); result/page.tsx:8 ("Readiness results"); ReadinessRunner.tsx 46 (`useSnapshot(assessmentId, set)`), 48, 58, 93, 132 (`Partner Readiness Assessment`); useSnapshot.ts 85-89 (`stampedSet`), 330 (`set: own`); AssessmentsHub.tsx 84 (`My readiness`), 85 (`ReadinessOverview set={found.set}`), 89 (H2 "Partner readiness self-assessment"); ReadinessResult.tsx 43, 59, 72; learning-priorities.ts 28 (`limit = 5`); FirmwareTask.tsx 31 (`AREA`), 35 (`locateQuestionSet(READINESS_SET_ID)`); customer/content.ts 102 (the Q-RDY-04 comment); PartnerDashboard.tsx 111, 116 (label "Partner readiness"); home-next-actions.ts 10; GlobalNav.tsx 44; partner/testing.ts 13; fixtures.ts 41 (`READINESS_IDS`); ReadinessReportModelBuilder.cs 80-81, 169; ReadinessContentTests.cs 15 (`StatementsSha256 = "71c29734..."`); ReadinessReportGoldenTests.cs 143 (the file is under `Modules.Reporting.Tests/Readiness/`, the spec gave it as a bare name); PartnerDashboard.text.test.tsx 44; AssessmentsHub.myreadiness.test.tsx 43; appsettings.json 11.
Content files: set title at 0.3.0 api/web `:233`, client `:206`, 0.6.1 set `:3733`, module `:431`; `Q-RDY-01` at 268 / 268 / 241 / 3768. All as the spec says.
Package census (python3 -I -B, JSON, all `api/.../SeedContent/playbook-placeholder.*.content.json`): the readiness set is byte-equal in id+text+section across 0.3.0, 0.4.0, 0.5.0, 0.6.0, 0.6.1 (1 distinct hash of 5; control: two different strings hash differently). API seed and web `packages/` copies byte-identical for all five; client copy exists for all five.

Mismatches:
1. **Count of packages.** Spec section 2.1: "identical in all six live packages (0.3.0 to 0.6.1)". Measured: the set exists in FIVE (0.3.0, 0.4.0, 0.5.0, 0.6.0, 0.6.1); 0.1.0 has none. (The six is the count of packages the API loads, `ReadinessContentTests.cs:21`.) Harmless to the build.
2. **`AssessmentsHub.tsx:47-48`** ("the hub shows the newest completed run", R2). The cited lines are inside the Start button's `catch`. The logic is at **`AssessmentsHub.tsx:70-73`** (`newestFirst`, `latest = ...find(status !== "in-progress")`). The claim itself stands.
3. **`ReadinessContentTests.cs:20-23`** is cited for "the catalog list"; it also holds the **count** `Assert.Equal(6, ...)` at `:21` and the test name that lists six versions (the most dangerous item above). Section 2.4 omits the count.

Also noted, pointer is right but wording thin: spec 5.3 says add `readinessPackage`; the reason it is mandatory (locateQuestionSet stays on 0.3.0) is stated only as a risk, see BLUF.

## 3. UNMEASURED
- Rendered behaviour of the layout page in a browser (not opened); every claim here is source text.
- The spec's test-file list in section 2.4 beyond the files named above (e2e specs, `session-tasks.test.ts`, Journey.cs, golden outlines) was not individually opened; only `playbook-readiness.spec.ts` and three other readiness-named e2e files were confirmed to exist.
- Whether the spec's "no readiness email templates" holds: not searched.
- Hash value of 0.3.0 in `PACKAGE_HASHES`: not recomputed.
