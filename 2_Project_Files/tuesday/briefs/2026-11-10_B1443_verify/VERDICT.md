VERIFY B1443: GO WITH FINDINGS @ f5dcd98

# Independent verification: branch `b1443/hpsmpoc-sme-drafts` of the analysis repository at head `f5dcd986c27d575be3e171d86593cc1461913ad2`

Verifier: read-only. I used a scratch clone with no checkout in the session scratchpad. Its push URL is set to `DISABLED`, the deploy key is set repo-locally in the scratch clone only, and no write verb ran on any origin. I read code facts at code main `884fd72b238ec8dc0d566b0e9c18b5362f920a2b` with `gh api -X GET .../contents/<path>?ref=884fd72b` (36 files fetched). I read analysis facts at the branch head with `git show f5dcd986:<path>`, and the documents lane's admin guide at the commit the draft names, `6b185f3f`, plus that branch's current head. Jira was NOT read.

**BLUF:** 0 Blockers, 0 Majors, 7 Minors.
- **Scope:** 22 of 22 changed paths are under `1_Project_Definition/Architecture/content/2026-11-10_sme-drafts/`. All 22 are `A`: 885 insertions, 0 deletions, and 0 existing files edited.
- **Rules 1 to 5:** every rule shows 0 violations on my own programs, and every control fires. The name scan is underscore-aware. Its `_by_<name>_` plant gives 0 with a `\b` checker and 1 with the underscore-aware one. The SOW scan finds 0 runs at 8 words, and also 0 at 7 and at 6.
- **Provenance:** 635 of 635 `SOURCED` tags resolve, and 49 cited lines read at source are all true as facts. Two of those 49 have a pointer one line off (F1).
- **HPSMPOC-390:** the role definitions match the code's role gates at `884fd72b` (20 checks, all true).
- **Landing:** the form is a merge commit (5 of 5 recent merges have 2 parents).
- **Landing texts:** written, because there is no Blocker.

One lesson from tonight's sibling verdict applies again. The prescribed brief-number regex `\bB[0-9]{3,4}\b` has the same underscore blind spot as the old name scan. It reads 0 on the drafts, but an underscore-aware form finds 1, inside a cited path (F7, Minor).

## 1. Scope (step 1)

| Check | Result | Instrument | Control |
|---|---|---|---|
| Branch head | `f5dcd986...` = the subject sha; `git ls-remote` equal | `git rev-parse origin/b1443/...`, `git ls-remote origin 'refs/heads/b1443/*'` | n/a |
| Merge base | `6670d18d` (the brief's main) | `git merge-base origin/main <branch>` | n/a |
| Analysis main now | `7656f1c3`. It moved by one merge (#187, records) that touches only `CLARIFICATIONS.md`, appended at line 5770 onward (hunk `@@ -5769,0 +5770,30 @@`). Every `CLARIFICATIONS.md` line the drafts cite (42 to 5179) is unchanged | `git log 6670d18d..origin/main`, `git diff -U0` | n/a |
| Changed paths inside the owned folder | **22 of 22**; 0 outside | `git diff --name-only origin/main...<branch>` piped to `grep -v '^1_Project_Definition/Architecture/content/2026-11-10_sme-drafts/'`: 0 | the folder did not exist at main (`git ls-tree` 0 entries) |
| Add-only | 22 `A`, 0 `M`, 0 `D`; 885 insertions, 0 deletions | `git diff --name-status`, `--numstat` | n/a |
| "Copied unchanged" sheets of item 31 (01, 05, 06, 10) | header equal; every non-note cell equal in 1/1, 8/8, 6/6, 6/6 rows; each note keeps the original text (with the owner's first name swapped to "the product owner") plus an appended tag | `python3 -I` csv compare against `origin/main:.../SME-authoring-template-v0/*.csv` | n/a |
| Placed where the product loads it? | No. The analysis repository only; nothing in the code repository and nothing under `web/src/content/` | path list above | n/a |
| Open analysis PRs | 1 (#188, the documents branch): 22 files, 0 in this folder | `gh api pulls?state=open`, `pulls/188/files` | n/a |
| Commits | 10, one per item, plain ASCII (0 non-ASCII lines), 0 brief numbers, seat ids or names in messages | `git log --format=%B`, `grep -c '[^ -~]'`, `grep -ciE` | n/a |
| Analysis CI on the head | 0 check runs | `gh api commits/f5dcd986/check-runs` | n/a |

## 2. Draft rules re-run (step 2)

These are my programs, written independently of the builder's: `vcheck.py` (R1 to R5, plus brief-number, seat, coordinator and secret scans), `vcontrols.py` (plants), `sownames.py` (SOW signature-field names) and `resolve.py` (SOURCED resolution). All are in the session scratchpad and none is committed.

The SOW sources are three texts:
- the signed SOW, read with `pdftotext -layout` and `-raw` from `Source_Documents/2026-10-01_final-SOW/...GLOBAL_SOW.pdf`;
- the draft global SOW `.txt`;
- the v1 SOW `.txt`.

Together they give 8857 distinct 8-word runs. The texts were held in memory only, and none was printed or written.

The names come from the B1396 ban list plus 12 tokens from the signed SOW's Name, Signed-by and Signature fields and the PDF author, 14 tokens in all. They were printed masked only and are written nowhere.

| Rule | Over | Violations | Control (a copy of the real 390 draft with one plant) |
|---|---|---|---|
| R1 marker line in first 5 lines + `_DRAFT-FOR-KAM.(md\|csv)` name | 22 files | 0 | marker removed: 0 -> 1 (fires) |
| R2 every non-exempt line / CSV data row carries `SOURCED: path:line` or the AGENT-PROPOSED label (exempt: headings, table header + separator rows, blank, marker, `> NOTE:`) | 22 files | 0 | untagged line: 0 -> 1; untagged CSV row: 0 -> 1 (both fire) |
| R2 provenance resolves (path exists, line range in file at the sha named: code `884fd72b`, admin guide `6b185f3f`, else analysis `f5dcd986`) | 635 tags | 0 unresolved | planted out-of-range line and missing path: 0 -> 2 (fires) |
| R3a no 8-word run of SOW text | 22 files | 0 (also 0 lines with a 7-word run, 0 with a 6-word run) | a real SOW 8-gram planted: 0 -> 1 (fires) |
| R3b no verbatim standards text (ISO/IEC 27001, NIST CSF, CIS) | 22 files, read by eye | 0. The only standards content is in 393: identifiers plus short "What the link covers" cells (7 to 17 words) in plain drafter's words, none reading as control text. No other draft quotes a standard | n/a (by eye, as the brief asks) |
| R4 person names, underscore-aware `(?<![A-Za-z])<name>(?![a-z])` after stripping the exact token `DRAFT-FOR-KAM` | 22 files | 0 | `C26_reviewed_by_<name>_with_notes` planted: `\b` checker 0, underscore-aware 1 (fires and shows the blind spot); the real file with only the marker token: 0 |
| R4c capitalised words reviewed by eye | 22 files | 0 person names (all products, roles, settings or plain words) | n/a (review) |
| R5 approval claims (`approved`, `signed off`, `sign-off`, `signs it off`, `vetted`; marker line exempt) | 22 files | 2 hits, both justified, 0 claims: `01_ruleset...csv:2` is the template's column header (`approved_by`, `approved_at`); `393...md:3` is the condition the brief requires ("stays out ... until a mapping is supplied and approved"). A broader scan (`approv`, `endorse`, `validated`, `certified`, `agreed`, `accepted`) adds only descriptions of code operations ("approve a held item") and "approval cells stay empty": 0 claims | "The mapping was approved by the customer" planted: 0 -> 1 (fires) |
| Brief numbers `\bB[0-9]{3,4}\b` (as the brief words it) | 22 files | 0 | `See B1443` planted: 0 -> 1 (fires) |
| **Brief numbers, underscore-aware** `(^\|[^A-Za-z0-9])B[0-9]{3,4}([^0-9]\|$)` | 22 files | **1** (`394...md:24`, inside the cited path `Briefs/2026-10-30_B941_STATUS.md`): F7 | on that path string: `\b` form 0, underscore-aware 1 |
| Seat ids (`SEAT-x`, `[HDRG]nn(n)`), underscore-aware | 22 files | 0 (the only hits are the document id `D01` in `2026-08-12_D01-skeleton.md` source refs copied from the template) | `Drafted by SEAT-H153` planted: 0 -> 1 (fires) |
| Coordinator names (Tuesday, Wednesday, Friday, Thursday, Monday, Spark, coordinator) | 22 files | 0 | `Tuesday will land it` planted: 0 -> 1 (fires) |
| Secrets, GUIDs, tenant/host shapes, URLs, IPv4, mailboxes, long key-like strings, `-rg`, `.onmicrosoft.` | 22 files | 1 hit, not a secret: `46...md:40` "Admin (EWS) Password: Enable, min 12 chars" (an HP setting label and the baseline value) | `demo-x.azurewebsites.net` planted: 0 -> 1 (fires) |

ALL CONTROLS FIRE.

## 3. Findings

| # | Severity | Where | Finding | Fix |
|---|---|---|---|---|
| F1 | Minor | `37_reconciliation-pack...md:116`, `:117` | Two pointers are one line off. "B: a question left unanswered is left out of the score and raises no finding" cites scenarios `README.md:58`, which is B's next-engagement line; the statement is at `:59`. "C: ... lifts the overall from red to amber" cites `:71` (C's next-engagement line); the statement is at `:72`. Both facts are true. The builder's resolver checks only that a line exists, so it could not see this | `:58` -> `:59`, `:71` -> `:72` |
| F2 | Minor | `390_role-definitions...md` (8 tags: `:53`, `:70`, `:71`, `:79`, `:80`, `:85`, `:89`) | It cites `1_Project_Definition/Deliverables/2026-11-10_admin-guide/...` at `6b185f3f`. That file is on the documents branch (open PR #188), not on analysis main. At that branch's newer head `3850c374` the 13 cited lines are byte-equal (13 of 13), so the pointers hold today. If this PR lands before #188, they name a path that does not exist on main. The draft discloses this at `:7` | Land #188 first, or leave as is (disclosed) |
| F3 | Minor | `393_framework-alignment...md:24-45` | No edition of any standard is named. The identifiers fit ISO/IEC 27001:2022 Annex A (A.5.x, A.7.14, A.8.x), NIST CSF 2.0 (GV.PO, GV.RM, GV.OV, PR.AA, PR.PS and PR.IR exist only in 2.0) and CIS Controls v8 (1 to 17). That is the verifier's own knowledge, not a licensed text: I found none out of range. Every row is labelled AGENT-PROPOSED and the draft says the identifiers were written from memory | State the editions (27001:2022, CSF 2.0, CIS v8) in the NOTE lines |
| F4 | Minor | `31_rules-content/07_questions...csv` Q-S7-001, `09_finding_rules...csv` R-005 | The question wording (from v2 N-11: "regular checks for software weaknesses and settings that have drifted") is linked to control UQ-030 Syslog. R-005's action is "Set Syslog ... Enable, TCP 514 ...". The question asks about checking and the action configures logging, so a "No" answer is remedied by something the question did not ask. The template skeleton row was a logging-coverage KPI | For the subject expert: reword Q-S7-001 to ask about sending printer logs to a central collector, or relink it |
| F5 | Minor | `395_audience-testing-plan...md:49` | "No name, employer or customer data is written on the sheet" cites `CLARIFICATIONS.md:42`, which names GDPR as a build principle in general and does not state this rule. The line also carries AGENT-PROPOSED, so it is not untagged | Drop the SOURCED tag or point at a privacy line that says it |
| F6 | Minor | `390...md:6` ("the drafting brief"), `:7` and `:71` ("the documents lane"), `37...md:123` ("no other seat"), `31_rules-content/00_README...md:7` ("results are in the status file": a file that is not in the repository) | Internal process words in text written for the product owner. No B-number or seat id | Use role wording ("the documents draft", "nobody else") and "the drafter's record" |
| F7 | Minor | `394_assessment-principles...md:24` | The SOURCED path `1_Project_Definition/Briefs/2026-10-30_B941_STATUS.md:23` carries a brief number. The file is on analysis main and the line resolves and supports the claim, so this is an internal id only. The brief's own regex (`\b`) does not see it, because an underscore counts as a word character | Optional; or cite `CLARIFICATIONS.md:5179` alone, which already carries the claim |

Nothing else needs fixing:
- **Secrets and hosts:** no secret, tenant id, subscription id, mailbox or host, and no path outside the folder.
- **Approval:** nothing claims approval. Every file carries "Not loaded into the product. Not sent. Not approved."
- **Proposals:** every proposal is labelled as one. The 37 covering note, the 44 disclaimers, the 46 label sentence and the 394 principles are all AGENT-PROPOSED.
- **Security facts:** no security statement is presented as fact without a SOURCED tag. I listed every line that carries only AGENT-PROPOSED (61 lines) and read each: they are plans, wordings, open questions and limits, not security facts.

## 4. Spot checks (steps 2 and 3): 49 checks, 47 true, 2 true with an off pointer (F1), 0 false

Code facts are at `884fd72b238ec8dc0d566b0e9c18b5362f920a2b` (`gh api -X GET .../contents/<path>?ref=884fd72b`). Analysis facts are at `f5dcd986` (`git show`).

| # | Draft:line | Claim | Checked at | Result |
|---|---|---|---|---|
| 1 | 390:11 | Four roles, no Customer role | Caller.cs:12-17 (`Admin, Consultant, Partner, Demo`; `All = [...]`) | true |
| 2 | 390:18-21 | All four read; Admin, Consultant, Partner write; Demo no write | Caller.cs:42-43 `ReadRoles`/`WriteRoles`; AssessmentModule.cs:153-154 | true |
| 3 | 390:37 | Admin and Consultant see and change every customer | Caller.cs:51 `SeesAllCustomers`, :215, :224 | true |
| 4 | 390:27 | Partner sees and changes only the customers it owns | Caller.cs:216, :224, :235 (`OwnerUserId == caller.UserId`) | true |
| 5 | 390:57 | Demo sees only seeded sample customers | Caller.cs:217, :235 (`SeedKey is not null`) | true |
| 6 | 390:30, :62 | Audit trail: Admin, Consultant, Partner; not Demo | Caller.cs:25-26; AssessmentModule.cs:155 (`WriteRoles`), :223 | true |
| 7 | 390:32, :40, :59 | Metrics summary and attribution preview: Admin, Consultant, Demo; not Partner | Caller.cs:28-29; AssessmentModule.cs:157, :259, :261 | true |
| 8 | 390:48-49 | Admin alone: demo reset, personal-data export and erase | AssessmentModule.cs:156, :230, :232-233 (`AdminPolicy` = Admin) | true |
| 9 | 390:31, :50 | Feedback: any app role submits; Admin alone lists, downloads, approves, deletes | FeedbackModule.cs:102 (`Roles.All`), :103, :165-172 | true |
| 10 | 390:51 | Showcase reset: its presenter or an Admin | ShowcaseEndpoints.cs:140 | true |
| 11 | 390:12 | Role comes from sign-in; web session has only sign-in and sign-out for it | Caller.cs:83 (roles from the `roles` claim); session.ts:105-106, :158-161 (`resetDemo` and the rest do not touch `user`) | true |
| 12 | 390:33, :43, :63 | Menus: Partner without metrics, attribution and admin; Consultant without Action plan, with metrics and attribution; Demo as listed | GlobalNav.tsx:33-36, :40-56, filter at :63-64 (`!i.roles \|\| roles.includes(role)`) | true |
| 13 | 390:67 | Settings page is a placeholder | settings/page.tsx:7 | true |
| 14 | 390:81 (D3) | Partner view / Customer view switch changes route, not role | WorkspaceSwitch.tsx:2-3, :30-33 | true |
| 15 | 390:80 (D2) | Fifth identity "Client" for follow-up links, not an app role | Caller.cs:34-40; FollowUpLink.cs:53-54, :243 | true |
| 16 | 390:82 (D4) | UAT start page: visitor picks one of four levels | UatStartScreen.tsx:21-27, :81-84; UatOpenAuthentication.cs:64-70 | true |
| 17 | 390:83 (D5) | Review copy: feedback read, approve, delete open to anyone there, sent as Admin | FeedbackModule.cs:170-171 | true |
| 18 | 390:60 | Demo sees a customer by alias in result and report | AssessmentEndpoints.cs:519; ReportingEndpoints.cs:430 | true |
| 19 | 390:84 (D6) | API lets a Consultant write action plans; menu hides it | AssessmentModule.cs:239-247 (`write`); GlobalNav.tsx:33, :48 (`PARTNER_SIDE`) | true |
| 20 | 390:85 (D7) | Guide's Admin-only list omits feedback operations | admin guide :27 at `6b185f3f` (and byte-equal at `3850c374`) | true |
| 21 | 37:13 | A: 78.7 -> 93.6 green; SVC-02 gap 400.0 | draft-a expected.hand.json:11-15, :88-92 | true |
| 22 | 37:42 | A F-001 R-009 high 30-day priority 1 | draft-a expected.hand.json:60-65 | true |
| 23 | 37:15, :103 | C: 4.3 -> 51.1 red; F-011 R-005 medium 60-90-day 11 | draft-c expected.hand.json:11-15, :130-135 | true |
| 24 | 37:20, :22 | Expected file pins ruleset sha256; test compares overall, sections, findings, next engagement | DemoScenarioTests.cs:16, :104-111 | true |
| 25 | 37:115 | A: two high findings, overall stays green, network drives next engagement | scenarios README.md:45 | true |
| 26 | 37:116 | B: unanswered question left out of score, no finding | README.md:58 (cited) vs :59 (actual) | true, pointer off (F1) |
| 27 | 37:117 | C: fixing the high findings lifts red to amber | README.md:71 (cited) vs :72 (actual); 51.1 >= amber 40 (ruleset :32-34) | true, pointer off (F1) |
| 28 | 37:122-124 | 2026-10-04 decision on the draft demo set recorded; sending is the product owner's; customer's decision open | CLARIFICATIONS.md:504-510 | true (the draft words it as a decision and does not repeat any approval claim) |
| 29 | 44:13-21 | Nine report section titles | ReportModel.cs:18-26 | true |
| 30 | 44:25 | Placeholder disclaimer text | ReportModelBuilder.cs:30 | true |
| 31 | 44:50, :64 | Reports only for sample customers | ReportModelBuilder.cs:39 | true |
| 32 | 44:35, :42 | Answer basis list; consultant notes etc. not reproduced | ReportModelBuilder.cs:370, :379-380 | true |
| 33 | 44:37 | Most severe first, then timeframe | ReportModelBuilder.cs:52-54 | true |
| 34 | 44:38-39 | Narrative only after review; provenance says template or AI | NarrativeProvenance.cs:15-18, :27 | true |
| 35 | 395:72-73 | "Overall score" line; "Rating" column | ReportModelBuilder.cs:124, :156 | true |
| 36 | 46:23 | UQ-008 baseline "Enable, min 12 chars · Rotate 90 days" | bundle.json:374-379 | true |
| 37 | 46:24 | UQ-106 Telnet: Disable; path Network Services > Telnet | bundle.json:4196-4201, :5784-5788 | true |
| 38 | 46:27, :32 | UQ-030 Syslog baseline; UQ-098 High, TLS 1.2+ only | bundle.json:1232-1237, :3884-3889 | true |
| 39 | 46:55 | Synthetic guidance is "NOT HP policy"; pilot-first step; boundary | hpsm-guidance.synthetic.json:7-8, :29, :23 | true |
| 40 | 393:15-17 | Five framework profiles; ISO validate-against-licensed note; 69 mapping rows, all Essential Eight, none with an ISO/NIST/CIS control ref | bundle.json:14915, :14929; JSON read: 69 rows, `essential_eight` 69, non-null `framework_control_ref` 0 | true |
| 41 | 31 README:16; 395:76 | Bands 70 / 40 / 0, Green/Amber/Red in the ruleset | ruleset 0.1.2 json:25-40 | true |
| 42 | 55:11, :104 | 2026-10-23 decision settled M1-M7; baseline owed; idle limit not covered | CLARIFICATIONS.md:2530-2538 | true |
| 43 | 55:15-26 | M1, M2 definitions; idle 120 s, tail 30 s; server-side only; effort reduction only with a baseline | design-pack 07:10, :18-19, :28; 21:97 | true |
| 44 | 55:62-64 | Trial flag designed; summary filters on it, default include; only a test sets it true | 07:13; ReportingEndpoints.cs:1096, :1104; openapi.yaml:1725-1727; Entities.cs:88; MetricsSummaryTests.cs:104; `gh api search/code` IsTrialRun: 41 files (entity, DbContext, migrations and snapshots, ReportingEndpoints, the test). The search index covers the default branch, not a pinned sha | true (setter search corroborates; not exhaustive at the sha) |
| 45 | 87:14, :20, :21-22 | Fewer questions; plain wording for resellers; print-centric; printer maturity specifically | CLARIFICATIONS.md:201, :202, :261 | true |
| 46 | 394:24 | Training page built without principles; principles ticket separate | CLARIFICATIONS.md:5179; B941 STATUS:23 | true |
| 47 | 395:49 | Participant codes, no names | CLARIFICATIONS.md:42 (GDPR named as a principle only) | weak pointer (F5); the line is also AGENT-PROPOSED |
| 48 | 31 README:17 | Industry and size options follow the target customers | CLARIFICATIONS.md:265 (regulated: healthcare, financial services, public sector; 100+ devices; 250 vs 2500 unsettled) | true |
| 49 | 31 README:14, :18, :19, :23 | 01, 05, 06, 10 copied unchanged | cell-by-cell compare with template originals (section 1) | true (notes carry a role-word swap + tag, disclosed by the builder) |

Count: 49 checks, 47 true, 2 true with an off pointer (#26, #27), 0 false. Check #47 is counted as true because its claim is tagged AGENT-PROPOSED; the SOURCED half is the weak part (F5). Section 3 security content: 20 role-gate checks on HPSMPOC-390 (#1 to #20), all true at code main `884fd72b`; the brief asked for at least 5.

Not re-run:
- the template's own `to-json` check on the item-31 copies (the builder reports 23 owed -> 0, strict gate FAIL with 7 provisional by design);
- any engine or test;
- Jira.

## 5. Landing form (step 4)

| PR (analysis repo) | Merged (UTC) | merge_commit_sha | Parents | Form |
|---|---|---|---|---|
| #187 | 2026-11-09T17:26:57Z | 7656f1c3 | 2 | merge commit |
| #186 | 2026-11-08T21:00:59Z | 6670d18d | 2 | merge commit |
| #185 | 2026-11-08T10:09:29Z | e7986dc0 | 2 | merge commit |
| #184 | 2026-11-06T09:10:30Z | 84eb4106 | 2 | merge commit |
| #183 | 2026-11-06T04:49:41Z | b4432413 | 2 | merge commit |

The house form is a **merge commit** (5 of 5 have 2 parents; the repo allows merge, squash and rebase). This branch adds files only, in a folder no other branch touches. Main moved by #187 (CLARIFICATIONS append only) and the open #188 shares no path, so I expect no conflict. That expectation was DERIVED from disjoint path sets, not from a test merge.

## 6. Landing text files (step 5)

Written, since there is no Blocker. They are plain ASCII and carry no brief number, seat id or person name; the marker token is not used in them. All four were checked by program after writing (section 8).
- `pr-title.txt`
- `pr-body.txt`: states DRAFTS for the product owner's review, not loaded, not approved, not sent. It ends with the PR attribution line in ASCII form; the robot emoji was dropped to keep the file plain ASCII as the brief requires.
- `merge-subject.txt`: a custom subject. The default GitHub subject would carry the branch name, and that holds the brief number.
- `merge-body.txt`: ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## 7. Fences kept

- No `cd`, and no git write verb on any origin. The scratch clone has `remote.origin.pushurl` = `DISABLED` and was never pushed.
- No PR, no Jira, no mail, no board, and no token printed.
- The SOW text and the names were held in memory only. Names were printed masked and appear in no file.
- I did not read `_ledger.md` or any WEDNESDAY, FRIDAY or non-Datasec tree.
- Writes were made only in this folder and in the session scratchpad.

The builder's record also lists two deviations of its own: `cd /dev/null` inside a subshell, and `rm -rf` on scratch paths that did not exist. Both are outside the branch and outside this verdict's scope, and are noted here only.

## 8. Landing-text self-check

Program: an underscore-aware scan of the four landing files for:
- the 14 name tokens and the token `KAM`;
- `B[0-9]{3,4}` with no word boundary, case-insensitive;
- `SEAT-`, `H153`;
- non-ASCII bytes.

Results (MEASURED, `landcheck.py`):

| File | names | KAM | brief no. | seat id | non-ASCII |
|---|---|---|---|---|---|
| pr-title.txt | 0 | 0 | 0 | 0 | 0 |
| pr-body.txt | 0 | 0 | 0 | 0 | 0 |
| merge-subject.txt | 0 | 0 | 0 | 0 | 0 |
| merge-body.txt | 0 | 0 | 0 | 0 | 0 |
| CONTROL (pr-title + `by_<name>_x KAM b1443 SEAT-H153` + one arrow) | 1 | 1 | 1 | 2 | 1 |

This VERDICT itself: 0 name hits under the same underscore-aware scan (the marker token stripped). `merge-body.txt` ends with the Co-Authored-By line.
