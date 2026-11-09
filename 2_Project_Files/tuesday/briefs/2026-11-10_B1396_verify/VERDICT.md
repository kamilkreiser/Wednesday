VERIFY B1396 ROUND 2: GO WITH FINDINGS @ 3850c37

# Round 2: re-verification at head `3850c37413d2e38273e5782425095919caf66026`

**BLUF:** the Blocker, both Majors and all six Minors from round 1 are fixed at 3850c37. I confirmed each one by my own program or by reading at source. The re-run over all 22 changed paths finds 0 Blockers and 0 Majors. Three new Minors are byproducts of the fix round: opaque source brackets, two test names shortened by their prefix, and garbled fragments in quoted Jira summaries. None of them blocks landing. Analysis main has moved to `7656f1c3` (PR #187, records lane, touches only `CLARIFICATIONS.md`). The merge base is still `6670d18d`, so there is no overlap. The four landing files are written.

## R2.1 The fix commit (item 3)

| Check | Result | Instrument |
|---|---|---|
| New head | `3850c374`, a single parent `6b185f3f` (one forward commit, no rewrite) | `git fetch` into the scratch clone (push disabled), `git rev-list --parents -n1` |
| Paths touched by 6b185f3..3850c37 | 8, all of them among the 22 branch paths, all `M` (edit), none A outside, none D | `git diff --name-status 6b185f3 3850c37` |
| Lines | +85 / -83 across the 8 files; every change edits a line in place, and 2 lines are added in the privacy draft (the corrected retention basis) | `git diff --numstat` |
| Branch vs current main | 22 of 22 paths inside OWN, 0 outside (control: 3 planted, 3 reported); merge base `6670d18d` | `git diff --name-status origin/main...head` piped to `scope.py` |
| Main moved | `6670d18d` to `7656f1c3`, which changes only `1_Project_Definition/CLARIFICATIONS.md`: no overlap with the 22 paths | `git diff --name-only 6670d18d origin/main` |
| Stage-gate add-only still holds | the 11 modified stage-gate files are untouched by the fix commit; their diff against main is still 1 added line each and 0 deletions | `git diff --numstat` |

## R2.2 Round-1 findings, each confirmed (item 1)

| # | Was | At 3850c37 | Instrument | Status |
|---|---|---|---|---|
| F1 Blocker | ban-list name in a quoted test name, `testing-evidence.md:143` | identifier cut to `C26_the_1_0_1_rows_are_approved_by...`; underscore-aware name scan over the 11 new files + 11 added lines: **0** | `names2.py`; control: planted `_by_<name>_` line gives 1 | **fixed** |
| F2 Major | "31 Mar 2027, 90 days after the Week 10 end" | the basis is now design 15's draft-SOW M8 (31 Dec 2026) + 90 days, plus a new line: 90 days after the SOW End Date of 31 Dec 2026 and 118 days after Week 10's end on Thu 3 Dec 2026 | python: 31 Dec 2026 + 90 d = 2027-03-31; 3 Dec 2026 to 31 Mar 2027 = 118 d; `pdftotext` shows End Date 31 Dec 2026 | **fixed** |
| F3 Major | phrase counts 1/1/1 | "twenty-one calendar days" 0 exact and 1 with the bracketed numeral removed; Effective Date 3; End Date 3; statement of work 4 | `pdftotext` + count: exact 0, numeral-removed 1, 3, 3, 4 | **fixed** |
| F4 Minor | 24 coordinator, `.tools` and "branch b1396" pointers | internal-id scan over the 11 new files and 11 added lines: B-number 0, seat id 0, coordinator path 0 (2 false hits: DPIA risk id `R10` and the quoted "R11 guard"; plus F-N3 below) | `ids.py`; control: one planted line gives B-number 1, seat id 1, coordinator path 3 | **fixed** |
| F5 Minor | `Briefs/*_STATUS.md` pointers that do not resolve | 0 `Briefs/` pointers in the 11 new files (control: 9 in the round-1 copy of testing-evidence.md) | `grep -c` | **fixed** (replaced; see F-N1) |
| F6 Minor | C-22 attributed "the product owner's own tenant" | now "the project's own resource group in the HPSM-POC dev subscription, with Entra sign-in only and no keys", which matches C-22 | CLARIFICATIONS.md C-22 on analysis main | **fixed** |
| F7 Minor | content versions "0.3.0 to 0.7.0" | "0.2.0 to 0.7.0, including 0.6.1, and one unversioned placeholder file" | code tree at fa401da9 (SeedContent lists 0.2.0, 0.3.0, 0.4.0, 0.5.0, 0.6.0, 0.6.1, 0.7.0 and the unversioned file) | **fixed** |
| F8 Minor | UAT checklist tear-down, old line 196 | row now reads "Tear down (NOT FOR UAT: the customer's review site; teardown only on the product owner's explicit word; run only on a throw-away environment)" | read at `administration-and-deployment-guide.md:196` | **fixed** |
| F9 cosmetic | escaped pipes in prose | unchanged, which the addendum allows; renders correctly | read | accepted |

## R2.3 Full rule set at 3850c37 (item 2)

| Rule | 11 new files (whole) | 11 added stage-gate lines | Control at round 2 |
|---|---|---|---|
| R1 marker | 0 | n/a | plant: 0 -> 2 (fires) |
| R2 provenance (line and sentence level) | 0 | 0 | plants: 0 -> 1, 0 -> 1 (fire) |
| R3 signed-SOW 8-word run | 0 | 0 | real SOW 8-gram: 0 -> 1 (fires) |
| R4 names (`\b`) | 0 | 0 | SOW signatory: 0 -> 1 (fires) |
| R4b names, underscore-aware | 0 | 0 | planted underscore name: 1 (fires) |
| R5 secrets, ids, mailboxes, URLs, hosts | 0 | 0 | made-up host: 0 -> 1 (fires) |
| R6 placeholders | 0 | n/a | unlisted placeholder + TBD: 0 -> 2 (fires) |
| Internal ids: `\bB[0-9]{2,4}\b`, `SEAT-*`, coordinator and `.tools` paths, "branch b1396" | 0 (only the review hits listed under F4) | 0 | planted line: B-number 1, seat id 1, path 3 (fires) |

The controls ran on copies of `testing-evidence.md` (rules) and `ai-tools-and-versions-record.md` (internal ids) at the new head.

Pre-existing content of the 11 modified stage-gate files (old names, the 3 M2 SOW-run lines, and old lines without the round's marker or provenance form) gives **identical** counts at analysis main and at the head: R1 11, R2 333, R3 3, R4 153, R5 3, R6 1 on both. The branch adds nothing to them. As in round 1, they are on main already and outside this verdict.

## R2.4 Findings at round 2

| # | Severity | Where | Finding | Suggestion |
|---|---|---|---|---|
| F-N1 | Minor | 29 provenance brackets across 8 new files | Sources were replaced with "internal QA record, not in this repository". This meets rule 2's form and removes the internal ids, but a reader can no longer trace those rows (for example the model-id table and the gate results), and one MEASURED fact (ai-tools:32) now points at an untraceable source | Before issue, name the source in role words ("the project's gate records, 9 Nov") or mark the rows RELAYED |
| F-N2 | Minor | `testing-evidence.md:142, 144` | When the internal prefix was removed, two quoted test names lost their real leading `B19`. The cited lines are right (276 and 205 at 884fd72b), but the identifiers shown are suffixes, not the exact method names | Show them as `..._a_timeout_is_never_retried` with a leading ellipsis, or keep the method name exact |
| F-N3 | Minor | `known-limitations-and-open-defects.md:50-88` | Stripping the internal numbers from quoted Jira summaries left fragments: "(gate notes on)", "((T1))", "N-3 fixed by (live since C-83)", "(-4, -5)", and a code branch name "branch b467" remains. The column header still says only "names removed" | Tidy the fragments and say "names and internal ids removed" |

## R2.5 Spot checks (item 4): the 2 round-1 false facts, plus 6 fresh

| # | Claim (file:line at 3850c37) | Checked at | Result |
|---|---|---|---|
| 1 | privacy:124-126: 31 Mar 2027 is 90 days after the 31 Dec 2026 End Date and 118 days after Thu 3 Dec 2026 | python date arithmetic; `pdftotext` End Date | true (was false) |
| 2 | rebase:53: twenty-one calendar days 0 exact / 1 numeral-removed; Effective Date 3; End Date 3; statement of work 4 | `pdftotext` + count | true (was false) |
| 3 | testing-evidence:140: `Configured_azure_call_is_keyless_schema_constrained...` at line 158 of NarrativePipelineTests.cs at 884fd72b | `gh api contents?ref=884fd72b` | true |
| 4 | testing-evidence:141: `Network_failure_and_timeout_become_failed_outcomes` at line 336 | same | true |
| 5 | testing-evidence:142, 144: lines 276 and 205 hold the timeout and validator-refusal tests | same (real names carry a `B19_` prefix, F-N2) | true (line numbers) |
| 6 | testing-evidence:143: the C26 approval test is at ReviewAndTemplateTests.cs:102 | same | true |
| 7 | ai-tools:63: C-22 puts the model service in the project's resource group in the HPSM-POC dev subscription, Entra only, no keys | CLARIFICATIONS.md C-22 on analysis main | true |
| 8 | admin-guide:54: SeedContent holds content 0.2.0 to 0.7.0 incl. 0.6.1 + one unversioned file | code tree at fa401da9 | true |

8 of 8 true.

## R2.6 Landing text (step 5)

The analysis repository lands by merge commit (round 1: 5 of 5 recent merges have 2 parents). Written: `pr-title.txt`, `pr-body.txt`, `merge-subject.txt`, `merge-body.txt`. They are plain ASCII, contain no B-numbers, seat ids or person names, and state that the documents are drafts for the product owner, not approved and not sent. Only the merge body ends with the Co-Authored-By line.

---

# Round 1 (at 6b185f3, superseded by round 2 above)

VERIFY B1396: NO GO @ 6b185f3

# Independent verification: branch `b1396/hpsmpoc-documents` of the analysis repository at head `6b185f3faaf324765e8e37468441e621feb9b9e0`

Verifier: read-only. Scratch clone (no checkout, push URL disabled, no write verb on any origin) in the session scratchpad. Code facts were read with `gh api -X GET .../contents/<path>?ref=<sha>` at the sha the draft names (`fa401da9f7bd...`) and the trees at `fa401da9` and `884fd72b`. Jira was NOT read (fence); every Jira-sourced row is marked "not shown" unless another file corroborates it.

**BLUF:** one Blocker. `Deliverables/2026-11-10_testing-evidence/testing-evidence.md:143` quotes a test-method identifier that contains a ban-list person name (the product owner's first name, joined by underscores). The builder's name check, and my first one, use `\b` word boundaries, and an underscore counts as a word character, so neither saw it. An underscore-aware scan finds exactly 1 hit across the 11 new files and the 11 added lines. Its control: a planted `..._by_<name>_with...` line gives 0 with the `\b` checker and 1 with the underscore-aware one. Everything else holds: 22 of 22 paths are inside OWN, 0 lines are deleted, rules 1, 2, 3, 5 and 6 show 0 violations and every control fires, and 70 of 77 spot-checks are true. Because there is a Blocker, the four landing text files were NOT written (step 5 condition). **The fix is one line:** truncate the identifier before the name, for example `C26_the_1_0_1_rows_are_approved_...`. Then re-run the underscore-aware name scan and this verdict can move to GO WITH FINDINGS (2 Majors, 6 Minors below).

## 1. Scope (step 1)

| Check | Result | Instrument | Control |
|---|---|---|---|
| Branch head | `6b185f3f...` = the subject sha | `git rev-parse origin/b1396/hpsmpoc-documents` in the scratch clone | n/a |
| Merge base | `6670d18d` = analysis main now (main has not moved) | `git merge-base`, `gh api branches/main` | n/a |
| Changed paths inside OWN | **22 of 22** (11 A, 11 M); 0 outside | `git diff --name-status origin/main...branch` piped to my own `scope.py` (OWN: `Governance/stage-gates/`, `Deliverables/`, `Demo/`; `Architecture/2026-11-10_*` new files only) | 3 planted paths (CLARIFICATIONS.md, an M on an Architecture/2026-11-10_ path, `web/src/x.ts`): reported 3 |
| Add-only on the 11 modified stage-gate files | 1435 insertions, **0 deletions**; exactly 1 added line per modified file | `git diff --numstat` | n/a |
| Open analysis PRs | 1 (#187, records lane): touches only `CLARIFICATIONS.md`, no overlap with this branch | `gh api pulls?state=open` + `pulls/187/files` | n/a |
| Commits | 9, all plain-ASCII subjects with no B-number, seat id or person name | `git log origin/main..branch` | n/a |

## 2. Draft rules re-run (step 2)

Programs (mine, independent of the builder's): `vcheck.py` (R1 to R6), `vcontrols.py` (plants), `names2.py` (underscore-aware names), `scope.py`, `extra.py`. All are in the session scratchpad, which is not committed. I read the SOW from the signed PDF, `Source_Documents/2026-10-01_final-SOW/HP_Security_Services_Playbook_Digital_POC_GLOBAL_SOW.pdf`: sha256 `edb778c2...218d`, equal to the folder's `SHA256SUMS.txt`, 15 pages. Its text went through `pdftotext` (layout and raw), was held in memory only, and is printed nowhere.

| Rule | Over | Violations | Control (copy of a real branch file with one plant) |
|---|---|---|---|
| R1 DRAFT + exact not-sent line in first 5 lines | 11 new files | 0 | DRAFT and marker removed: 0 -> 2 (fires) |
| R2 provenance: every line or row ends with `[src: ... \| MARK]`, and no untagged sentence inside a tagged line | 11 new files + 11 added lines | 0 + 0 | new untagged line: 0 -> 1; untagged sentence inside a tagged line: 0 -> 1 (both fire) |
| R3 no 8-word run of signed-SOW text | 11 new files + 11 added lines | 0 + 0 (also 0 lines with a 7-word run) | a real SOW 8-gram planted: 0 -> 1 (fires) |
| R4 names (ban list + names from the SOW `Name`/`Signature` fields + PDF author), `\b` boundaries | 11 new files + 11 added lines | 0 + 0 | SOW signatory name planted: 0 -> 1 (fires) |
| **R4b names, underscore-aware** (`(?<![A-Za-z])name(?![a-z])`) | same | **1** (`testing-evidence.md:143`) | planted `_by_<name>_` line: `\b` checker 0, R4b 1 (shows the blind spot) |
| R4c capitalised non-dictionary words, reviewed by eye | 11 new files | 0 person names among 57 candidates (all products, months or plain words) | n/a (review) |
| R5 secrets, GUIDs, known tenant/subscription prefixes, mailboxes, URLs, host-like names, IPv4, key shapes, resource-name shapes | 11 new files + 11 added lines | 0 + 0 | a made-up App Service host name planted: 0 -> 1 (fires) |
| R6 placeholders labelled, listed under a closing `## Placeholders and confirmations`, nothing after it; no TBD, TODO, ??? or bare brackets | 11 new files | 0 | an unlisted `[PLACEHOLDER: ...]` and a `TBD` planted: 0 -> 2 (fires) |
| R3 SOW run | the signed SOW was readable | **RUN** (not NOT RUN) | as above |

Pre-existing, not introduced by this branch: the builder reports 3 old M2 lines with an SOW 8-word run (table labels and amounts) and 100 old stage-gate lines carrying person names. They are on analysis main already, the diff adds none (0 deletions; the added lines are clean above), and they are outside this verdict. The builder's re-base record discloses them (section 6) for a separate ruling.

## 3. Findings

| # | Severity | Where | Finding | Fix |
|---|---|---|---|---|
| F1 | **Blocker** | `Deliverables/2026-11-10_testing-evidence/testing-evidence.md:143` | A quoted test name contains a ban-list person name joined by underscores. The builder's R4 (`\b`) and STATUS "names 0" missed it: same root cause as my first pass, caught by the underscore-aware scan | Truncate the identifier before the name (the table already truncates long names with `...`), then re-run R4b |
| F2 | Major | `Architecture/2026-11-10_privacy-update-draft.md:124` | The draft says design 15 proposed deleting all data "by 31 Mar 2027, 90 days after the Week 10 end". Week 10 ends Thu 3 Dec 2026 (my calendar from Fri 25 Sep). Design 15:7 derives 31 Mar from "M8 on Thu 31 Dec 2026 + 90 days", the 23 Sep draft-SOW basis. Under the signed SOW, 31 Mar 2027 is 90 days after the SOW End Date (31 Dec 2026), not after Week 10 | Restate the basis: "90 days after 31 Dec 2026 (design 15 used the draft's M8 date; the signed SOW's End Date is the same day)", or flag it for re-basing |
| F3 | Major (low impact) | `Governance/stage-gates/2026-11-10_rebase-on-signed-sow.md:53` | My count over the signed text does not match three phrase counts. "twenty-one calendar days": exact 0 (the text carries a numeral in brackets between the words); "Effective Date": 3; "End Date": 3. The draft says 1, 1, 1. The other six counts agree (Figma 0, Adobe XD 1, QuestPDF 0, for review only 1, change control/request/order 0/0/0, statement of work 4). The conclusion (D-4 to D-7 stand) is unaffected | Say what was counted (the defining occurrence) or correct the counts |
| F4 | Minor | 24 lines across 8 of 11 new files | Provenance pointers into the coordinator's tree (`TUESDAY/2_Project_Files/tuesday/briefs/..._B1396_SEAT-H146_...md`), to `.tools/b1396/...` and to "branch b1396". None resolves from the analysis repository, and they carry a B-number and a seat id into deliverable text | Replace them with repo-relative or role wording before anything is issued |
| F5 | Minor | `testing-evidence.md` (12 lines), `known-limitations-...md` (3), and others | Cited `Briefs/*_STATUS.md` files (B1343, B1380, B1389, B1390, B1391) are not on analysis main (`git cat-file -e`: absent, 5 of 5), so the pointers do not resolve in the repository. They are honestly marked RELAYED | Leave as is for the draft, or note "untracked gate record" |
| F6 | Minor | `Deliverables/2026-11-10_ai-tools-record/ai-tools-and-versions-record.md:63` | "The ruling of 25 Sep placed the build's model service in the product owner's own tenant [C-22]": C-22 names the project's resource group in the HPSM-POC dev subscription. It does not say "the product owner's own tenant" | Use C-22's own wording |
| F7 | Minor | `Deliverables/2026-11-10_admin-guide/administration-and-deployment-guide.md:54` | "Playbook content files for versions 0.3.0 to 0.7.0". At fa401da9, SeedContent also holds 0.2.0, 0.6.1 and an unversioned placeholder | "0.2.0 to 0.7.0, plus an unversioned placeholder" |
| F8 | Minor | `administration-and-deployment-guide.md:196` | The UAT walk-through checklist ends with "Tear down: the resource group deletes". On UAT this would delete the only site HP holds a link to | Mark the step approval-class, or name a throw-away environment |
| F9 | Minor | `privacy-update-draft.md:68`, `phase2-backlog.md:152`, `testing-evidence.md:5-7`, others | Escaped pipes (`\|`) inside prose provenance brackets. Rendering is fine (a CommonMark escape), but it is inconsistent with the unescaped form used elsewhere | Optional |

No secret, tenant id, subscription id, mailbox or host name, no path outside OWN, and no claim presented as approved: every file says "Not sent. Not approved."; proposals and verdicts are labelled "proposed"; the two AI CONFIRMs stay open.

## 4. Spot checks (step 3): 77 checks, 70 true, 2 false, 5 not shown

Code facts at `fa401da9f7bdab21c46ad9717c964433a2d22650` (the sha the drafts name) unless stated; the instrument is `gh api -X GET repos/datasecau/HPSM-POC/contents/<path>?ref=<sha>` or the recursive git tree.

| # | Deliverable | Claim (draft file:line) | Checked at | Result |
|---|---|---|---|---|
| 1 | 169 | M1..M8 week-ends Thu 1 Oct, 8 Oct, 22 Oct, 5 Nov, 12 Nov, 19 Nov, 26 Nov, W10 27 Nov to 3 Dec (rebase:29-36) | python calendar from Fri 25 Sep 2026; SOW 4.1 weeks 1,2,4,6,7,8,9,10 | true |
| 2 | 169 | Payments 10k W1, 10k W2, 15k W6, 10k W9, 5k W10 = 50k (rebase:40) | SOW 6.2.1 table | true |
| 3 | 169 | Nine dated priced lines sum to 41k + SME 9k = 50k (rebase:41) | SOW 6.2 table | true |
| 4 | 169 | Gate calendar: 40, 33, 19, 5 days ago; in 2, 9, 16, 23 days (rebase:92-99) | date arithmetic from 10 Nov | true |
| 5 | 169 | change control/request/order 0/0/0; statement of work 4 (rebase:51) | `pdftotext` + count | true |
| 6 | 169 | twenty-one calendar days 1, Effective Date 1, End Date 1 (rebase:53) | `pdftotext` + count: 0 exact, 3, 3 | **false** (F3) |
| 7 | 169 | Figma 0, Adobe XD 1, QuestPDF 0, for review only 1 (rebase:53) | `pdftotext` + count | true |
| 8 | 169 | Signed copy sha256 starts `edb778c2daa7`, 15 pages (rebase:10) | `shasum -a 256`, `pdfinfo`, folder SHA256SUMS | true |
| 9 | 169 | Pack re-based 1 Oct in 347359e (rebase:20) | `git log -1 347359e`, date 2026-10-01 | true |
| 10 | 169 | CR_log.md:7 states no change-control clause (rebase:52) | `git show origin/main:.../CR_log.md` line 7 | true |
| 11 | 169 | One pointer line added per file, 0 old lines missing (rebase:72-82) | `git diff --numstat` 0 deletions; -U1 diff shows 1 added line each | true |
| 12 | 169 | SOW End Date is 31 Dec, Effective 25 Sep (rebase:54) | `pdftotext` | true |
| 13 | 170 | Four app roles (Caller.cs:12-15) | Caller.cs | true |
| 14 | 170 | Role matrix: Partner no metrics, Demo no write, Admin-only reset/export/erase (Caller.cs:19-33) | Caller.cs:19-32 | true |
| 15 | 170 | Admin and Consultant see all customers (Caller.cs:51) | Caller.cs:51 | true |
| 16 | 170 | Environment names dev, uat, demo (main.bicep:7) | main.bicep:7 | true |
| 17 | 170 | Hosted pin `snapshot-policy-aligned@0.1.2` (appservice.bicep:141) | appservice.bicep:141 | true |
| 18 | 170 | Feedback route automation only for demo, else off (appservice.bicep:128) | appservice.bicep:128 | true |
| 19 | 170 | Route values off/automation/rest, default off (IFeedbackSink.cs:30-38; FeedbackModule.cs:29) | both files | true |
| 20 | 170 | Web waits 90 s for the demo reset only (bff.ts:168-172, 205) | bff.ts | true |
| 21 | 170 | Backup storage `Local`, no other option (sql.bicep:71) | sql.bicep:71 | true |
| 22 | 170 | `/health` and `/health/ready` (Program.cs:149-150) | Program.cs | true |
| 23 | 170 | Rulesets placeholder + 0.1.0, 0.1.1, 0.1.2 (SeedContent) | tree at fa401da9 | true |
| 24 | 170 | Content files 0.3.0 to 0.7.0 (guide:54) | tree: also 0.2.0, 0.6.1, unversioned | not shown as stated (F7) |
| 25 | 170 | resetShowcase for presenter or Admin; resetDemoData Admin-only, re-seeds as new rows (openapi.yaml:1761-1763, 1844-1846) | openapi.yaml | true |
| 26 | 170 | Personal-data path at openapi.yaml:1889 | openapi.yaml:1889 `/api/v1/admin/users/{userId}/personal-data` | true |
| 27 | 170 | infra test `test_hosted_demo_pin.py` exists | tree | true |
| 28 | 170 | UAT two locks, switch off by default (UatOpenAuthentication.cs:27-35) | UatOpenAuthentication.cs:29-35 | true |
| 29 | 171 | API test files 223 / 223 (testing-evidence:25) | tree count `api/tests/**Tests.cs` | true |
| 30 | 171 | Web unit files 278 / 283 (:27) | tree count `web/src/**.test.ts(x)` | true |
| 31 | 171 | Playwright specs 57 / 59 (:28) | tree count `web/e2e/**.spec.ts` | true |
| 32 | 171 | Infra test files 10 (:29) | tree count `infra/tests/test_*.py` | true |
| 33 | 171 | Ten live-api specs (:32) | tree count | true |
| 34 | 171 | fa401da9 check-runs: 21 success, 1 skipped (:36-62) | `gh api commits/fa401da9/check-runs` (22 total) | true |
| 35 | 171 | 884fd72b: 21 success, 1 skipped, all complete (:64) | `gh api commits/884fd72b/check-runs` | true |
| 36 | 171 | PR 296 landed 10 Nov 03:03 AEDT as fa401da9, head 55d7d4ee (:13, :75) | `gh api pulls/296`: merged 16:03:25Z | true |
| 37 | 171 | PR 297 landed 03:54 AEDT as 884fd72b (:14) | `gh api pulls/297`: merged 16:54:05Z | true |
| 38 | 171 | UAT still ran 13ac7d7e at 03:31 (:15) | B1391 STATUS:16 | true |
| 39 | 171 | B1389 round 2 NO GO; API 3887/0/22 head, 3881/0/22 main; web 4094 vs 4072 (:74) | B1389 STATUS:1 | true |
| 40 | 171 | B1390 GO WITH FINDINGS; e2e 963/1/46 vs 950/0/46; web 4120 vs 4072 (:76) | B1390 STATUS:1, 123-127 | true |
| 41 | 171 | B1343 1319 passed, 2 Azurite not executed; SQLite 2217 (:77) | B1343 STATUS:1, 7 | true |
| 42 | 171 | B1380 API 3887/22/0; web 4089/4089 (:73) | B1380 STATUS:32, 70 | true |
| 43 | 171 | SOW 4.2 event-ready: zero Critical, no High blocking the script (known-limitations:12) | `pdftotext` 4.2 | true |
| 44 | 171 | appservice.bicep:128 backs "UAT feedback saved, not sent" (known-limitations:99) | appservice.bicep:128 | true |
| 45 | 171 | 144 open issues, 4 High (87, 90, 94, 97) (known-limitations:10, 20-23) | lanes.md census (144) only; Jira not read | not shown (count corroborated, priorities not) |
| 46 | 171 | Matrix 48 of 48 refs resolve; 09: 92 citations, 23 moved (:95, :117) | not re-run | not shown |
| 47 | 173 | 96 items = 45 S + 37 M + 13 L + 1 unsized (phase2:43) | sum of the per-ticket table rows | true (internally) |
| 48 | 173 | SOW: Phase 2 backlog is 1 electronic copy, issued at M8 Week 10 (phase2:11) | `pdftotext` 4.1 M8, 4.1.1 | true |
| 49 | 173 | 23 HP-waiting tickets, list as in the table (phase2:152-164) | lanes.md:20-32 key list (23 keys) | true |
| 50 | 173 | Catalogue epic + 12 tickets 448..460 (phase2:19) | lanes.md: bucket of 13 | true |
| 51 | 173 | 144 open: 141 Backlog, 3 In Progress (phase2:17) | lanes.md:18 | true (relayed) |
| 52 | 173 | Model/SKU retire 14 Apr 2027 (phase2:180; openai.bicep:3-5) | openai.bicep:4 | true |
| 53 | 173 | HPSMPOC-98, 120, 177 Done (phase2:137) | Jira not read | not shown |
| 54 | 173 | HPSMPOC-271 premise overtaken (phase2:174) | lanes.md:145 | true |
| 55 | 174 | W1 25 Sep to 1 Oct ... W10 27 Nov to 3 Dec; today in W7 (README:27-38) | python calendar | true |
| 56 | 174 | W1..W3 drafts on analysis main, none for W4+ (README:29-38) | `git ls-tree origin/main Governance/status-reports/` (3 files) | true |
| 57 | 174 | SOW 4.1.5 parts (a)(b)(c); (b) non-binding (README:13-15) | `pdftotext` 4.1.5 | true |
| 58 | 174 | SOW 3.4: weekly working-software reviews (README:17) | `pdftotext` 3.4 | true |
| 59 | 174 | C-34 section B: fortnightly in October, weekly in November (README:46) | CLARIFICATIONS.md:257 on analysis main | true |
| 60 | 174 | Ten priced lines incl. SME 36 h (TEMPLATE:36-50) | SOW 6.2 table (10 rows) | true |
| 61 | 174 | Milestone weeks/dates in the template (TEMPLATE:65-72) | SOW 4.1 + calendar | true |
| 62 | 175 | gpt-4.1-mini, 2025-04-14, Standard, 10 KTPM, NoAutoUpgrade, DefaultV2 (ai-tools:17) | openai.bicep:11-19, 44-48 | true |
| 63 | 175 | REST API version 2024-10-21 (provider cs:26) | AzureOpenAiNarrativeProvider.cs:26 | true |
| 64 | 175 | Deterministic provider is the default (NarrativePipeline.cs:15) | NarrativePipeline.cs:15 | true |
| 65 | 175 | Prompt versions 1.0.0 (25 Sep), 1.0.1 (26 Sep), 1.0.2 (5 Oct), all approved (ai-tools:18) | registry.json `approvedAt` | true |
| 66 | 175 | deepseek-v4-flash-0731, temperature 0 (spark_run.py:34, 213) | project `tools/spark/spark_run.py:34, 213` | true |
| 67 | 175 | Newest spark-runs folder 28 Sep (ai-tools:20) | `ls -lt .tools/spark-runs` | true |
| 68 | 175 | Published ids and not-before dates (fable 1 Sep, opus 22 Sep, sonnet 28 Sep, haiku 7 Oct 2027), checked 03:28 (ai-tools:32-39) | models_latest.json | true |
| 69 | 175 | SOW 4.1.4(e) keep record; 4.1.3 open-weight versions in testing evidence; two CONFIRMs (tenant, no-training) | `pdftotext` 4.1.3, 4.1.4 | true |
| 70 | 175 | uat.bicepparam:17-18 sets SKU and capacity (ai-tools:67) | uat.bicepparam:17-18 | true |
| 71 | 175 | C-22: model service in the product owner's own tenant (ai-tools:63) | CLARIFICATIONS C-22 (project dev subscription) | not shown (F6) |
| 72 | 176 | 33 tables at fa401da9, 21 at c2dd403, 12 new, 0 gone (privacy:33-35) | `ToTable` set diff of both SQL Server snapshots at both shas | true |
| 73 | 176 | 12 ToTable line numbers (privacy:49-60) | snapshot lines 142, 1555, 1331, 1644, 1732, 1792, 1402, 1468, 2243, 1982, 779, 2376 | true (12 of 12) |
| 74 | 176 | Identifiers dropped at import; kept CSV blanked; pre-change files keep them (ImportReader.cs:60-69) | ImportReader.cs:60-68 | true |
| 75 | 176 | Blob lifecycle 180 d, versions 7 d, soft delete 7 d (storage.bicep:11, 46-47, 70-71); logs 30 d (monitoring.bicep:10); feedback 12 months not enforced (FeedbackModule.cs:40-42); links 14/30 d, 120 min (FollowUpLink.cs:20-28); region australiaeast only (main.bicep:10-12) | each file and line | true (5 of 5) |
| 76 | 176 | Design 15 end date 31 Mar 2027 = "90 days after the Week 10 end" (privacy:124) | design 15:7 ("M8 on Thu 31 Dec 2026 + 90 days"); Week 10 ends 3 Dec | **false** (F2) |
| 77 | 176 | SOW 5: Supplier is Data Controller; controller/processor defined generally (privacy:15) | `pdftotext` PERSONAL DATA section | true |

Count: 77 checks, 70 true, 2 false (#6, #76), 5 not shown (#24, #45, #46, #53, #71). Per deliverable: 169: 12; 170: 16; 171: 18; 173: 8; 174: 7; 175: 10; 176: 6 rows covering 21 individual facts (#73 is 12 facts, #75 is 5).

## 5. Landing form (step 4)

| PR (analysis repo) | Merged (UTC) | merge_commit_sha | Parents | Form |
|---|---|---|---|---|
| #186 | 2026-11-08T21:00:59Z | 6670d18d | 2 | merge commit |
| #185 | 2026-11-08T10:09:29Z | e7986dc0 | 2 | merge commit |
| #184 | 2026-11-06T09:10:30Z | 84eb4106 | 2 | merge commit |
| #183 | 2026-11-06T04:49:41Z | b4432413 | 2 | merge commit |
| #182 | 2026-11-06T00:00:55Z | f529d3b4 | 2 | merge commit |

The house form is a **merge commit** (5 of 5 have 2 parents; the repo allows squash, merge and rebase). The squash subject and body files are therefore only needed if Tuesday picks squash for this PR.

## 6. Landing text files (step 5)

**NOT WRITTEN:** step 5 applies only if there are no Blockers, and F1 is a Blocker. After F1 is fixed (one line) and R4b is re-run to 0, the four files can be produced against the new head.

## 7. Fences kept

No `cd`. No git write verb on any origin: the scratch clone has `remote.origin.pushurl` set to DISABLED and was never pushed. No PR, no Jira, no mail, no board. No token printed. The SOW text and the names were held in memory only; the names are masked in program output and appear in no file. `_ledger.md`, WEDNESDAY, FRIDAY and non-Datasec trees were not read.
