# Friday's own calls: proposed dispositions (Datasec), 2026-10-13 ~03:3x AEDT

Datasec only (MPS Commercial Calculator, Security Composer, HPSM-POC). This is the input `friday-calls.md` §1, one row per call, re-measured. Kam accepted his 42 pack decisions as defaults (2026-10-12 ~20:12). These are the coordinator's own calls.
Drafted by a read-only subagent. Nothing was posted, ticketed, sent or written outside this file.

## Instruments (all read-only, taken 03:2x–03:3x AEDT)
- **GH-MAIN:** `friday_as.sh datasec gh api repos/datasecau/<repo>/commits/main`. MPS = `d711b42c` (#29 B53), HPSM-POC = `a5fd6355` (#146 B230), Composer (`datasecau/Datasec-Security-Composer`) = `eddb484b` (#74 B135). These match Friday's mains. HPSM-POC-analysis = `bb1e8887`.
- **GH-PRS:** `gh api …/pulls?state=closed` (merged since 10-11 12:00Z) and `…/pulls/<n>` + `/files`.
  - MPS: #27, #28 (b49, F1), #29 (b53). 0 open PRs.
  - HPSM-POC: #143, #144, #145 (B228/B229), #146 (B230). **#147 B231 is OPEN**: `mergeable_state` = `blocked`, head `62aa1a6f`.
  - Composer: #69–#72, **#73 (B134), #74 (B135)**, merged 12:29Z.
- **GH-SEC:** `gh api repos/…` (`security_and_analysis`), `…/rulesets?includes_parents=true`, `…/rules/branches/main`, `…/code-scanning/default-setup`, `-i …/vulnerability-alerts`. The org ruleset body (`orgs/datasecau/rulesets/24139430`) gave a 404: the token lacks `admin:org`, so the ruleset's conditions are UNMEASURED.
- **REC:** records repos, read with `for-each-ref`, `show <ref>:BACKLOG.md`, `merge-base --is-ancestor`, and STATUS files.
  - MPS records: `main` `01ef803`; `records/b53` `d05a289`, `b54` `1129a25`, `b58` `c267f27`.
  - Composer records: `main` `dab4854d`; `records/b134` `23419a8f`, `b135` `446cb227`, `b136` `c6da79ff`.
  - HPSM analysis BACKLOG at `bb1e8887`, through the contents API.
- **CODE:**
  - MPS and HPSM-POC: `git grep`, `ls-tree` and `show` at the main SHAs. Both are in the local clones (`cat-file -t` = commit).
  - Composer `eddb484b` is **not** in the local clone, so it was read through the contents and trees API (978 tree paths).
- **HOST:** `ps`; `lsof -nP -iTCP:6670-6689 -sTCP:LISTEN`; `docker network ls`; `docker ps -a`.
- **NOT READ:** Jira (no instrument in my sources). Every Jira state below is UNMEASURED.

Disposition key:
- **CLOSED-ALREADY:** already resolved by a merge, STATUS or setting.
- **RULE-DEFAULT:** take the drafter's default.
- **RULE-OTHER:** a different ruling, stated in the row.
- **KAM-CARD:** only for money, production, comms to a human, irreversible changes, or a change to what users can do.
- **NEEDS-MEASUREMENT:** a named instrument must be read first.

## MPS Commercial Calculator (10)

| id | call (one sentence) | STATE NOW (instrument → what it showed) | PROPOSED | reason | who acts |
|---|---|---|---|---|---|
| M1 MPSCALC-61 | Are dependency scanning and DAST "org settings" left to Friday? | GH-SEC on MPS: `code_security` enabled. `dependabot_security_updates` enabled. `vulnerability-alerts` → **HTTP 204 (on)**. CodeQL default setup `configured` (csharp, js/ts, python, actions; 2026-10-10). `secret_scanning` **disabled**. No DAST exists. Control: the same calls on HPSM-POC and Composer return the same shape. | **RULE-OTHER:** close the scanning half as already on. Record DAST as not adopted for this phase. Secret scanning only through a Kam card, if wanted. | Dependency and code scanning are measured on. Turning on secret scanning for a private repo is a paid GitHub feature, so it is money. | Friday (Jira comment and transition) |
| M2 CodeQL ruleset row (BACKLOG :46) | The CodeQL ruleset did not block the first push to MPS `main`: chase it? | GH-SEC: org ruleset `24139430` "Security scan rule" is `active` on MPS `main`. Its rules are `deletion`, `non_fast_forward`, `code_scanning` (CodeQL, errors / high_or_higher) and `required_status_checks` (`do_not_enforce_on_create: false`). The same ruleset id is on HPSM-POC and Composer (control). REC: the row is still `[ ]` at records `main` and `b58`. | **CLOSED-ALREADY** | The ruleset now covers this repo. The 09-30 miss was the branch-creating push, before coverage. | records seat (tick the row and cite this read) |
| M3 Leak scanner not versioned (:162) | Version the per-seat leak scanner? | CODE: `ls-tree -r d711b42c` (342 paths) has 0 paths matching `leak` or `scan`. Control: `tools/` lists 10 paths. B58 STATUS `:288` used its own `leak58.py`, so seats are still rebuilding it per round. | **RULE-OTHER:** version it as `tools/leakscan/` plus a test, in the code repo, through a CodeQL PR. | It holds no confidential values (it reads the git-ignored avoid lists by path). Rebuilt copies have already had a blind spot (B05). | MPS build seat (docs/scripts lane, tier 3) |
| M4 [B08A2-6] build servers (:195) | Who stops the shared-SDK MSBuild/VBCSCompiler servers? | HOST: `ps` shows 0 VBCSCompiler / MSBuild.dll / build-server processes now. CODE: `run-demo.sh:293` and `PublishOutputTests.cs:39` already pass `-nodeReuse:false` (and `UseSharedCompilation=false` in run-demo). | **RULE-OTHER:** a standing brief line. Seats build with `-nodeReuse:false -p:UseSharedCompilation=false`. Nobody runs `dotnet build-server shutdown` while another seat is live. Then close the row. | It avoids a cross-seat kill. Nothing is running to clean up today. | Friday (brief template); records seat (close the row) |
| M5 [B38-N5] (+ gates MPSCALC-47) | Mark the 7 cost-bearing input fields `Internal` and add the "shown via the result DTO" comment? | CODE `d711b42c`: `ExportFieldRegistry.cs:55-56` maps **both** `Internal` and `NotShown` → `InternalOnly`. The fields are classified in `Proposal.cs` (`:29` `N = NotShown`, `:163`). Not touched by #28 or #29 (GH-PRS file lists). | **RULE-OTHER:** yes, do it. A label-only change that is guarded by the export-registry test. | The export class is identical either way, so there is no output change. It records the gate's intent and unblocks MPSCALC-47. | MPS build seat. Shares `Proposal.cs` with F3 (the one-pager), so run it in F3 or after it. |
| M6 MPSCALC-56 Entra SSO | Move MPSCALC-56 to Done (proposed 10-11)? | Jira: **UNMEASURED** (not read). Code evidence per the lane table (`#11 9fe66dc`, `#12 98d829f`) was not re-read. | **RULE-DEFAULT:** move it to Done. | It has been live since #10. It is a bookkeeping write. | Friday (Jira read, then transition) |
| M7 [B42-L4] duplicate JSON keys | Refuse duplicate keys? | GH-PRS: #29 body: "B42-L4". REC: B53 STATUS `:20` "DONE, Friday's default (refuse)". Gate B57 STATUS `:9` "(9) B42-L4 duplicate keys refused: GO WITH NOTES". Merged in `d711b42c`. The row is still `[ ]` at `records/b53:BACKLOG.md:574`. | **CLOSED-ALREADY** | It was built, gated and merged with the default. | records seat (tick `[B42-L4]`; note `[B53-R7]` last-wins on activate) |
| M8 B43-Q5 may need `Program.cs` | Route-local fix, or BLOCKED-BY-FILES? | REC: B53 STATUS `:17` "DONE, route-local (no `Program.cs` change)". B57 closure table: `[B43-Q5]` CLOSED-WITH-NOTES. #29 file list has no `Program.cs`. | **CLOSED-ALREADY** | It was built without F2's file. | records seat (tick `[B43-Q5]`) |
| M9 B27-H4 "503 while running" arm | Build 503 only where the contract lists it, else BLOCKED-BY-FILES? | REC: B54 STATUS `:11-12`: 503 `DiskUnreadable` on POST and PATCH (16/16 store, 8/8 API). `:137-139`: the `GET /inventory/audit` 503 arm is "**not needed**" (audit serves the last good in-memory document), so it is not built and not BLOCKED. B57 `:12` "(H-4) malformed overlay.json: GO WITH NOTES". B54 is **not merged**: `b54` `e6c9ced` was NO GO on W-1/W-2/W-3, and the fix round `b58` `727c7c89` is "READY FOR GATE" (B58 `:290`). | **CLOSED-ALREADY:** accept "audit arm not needed". | The arm question is settled on the merits. What remains is B58's gate, not this call. | Friday (gate B58, then the PR); records seat (record the audit-arm ruling) |
| M10 Ports 6670–6689 | Friday's port range overrides B41's note? | REC: B53 used 6670–6679 (`B53_STATUS:150,321`). B54 used 6681–6682 (`B54_STATUS:179,183`). HOST: `lsof … 6670-6689` rc 1 (0 listeners). Control: `lsof` lists `:7000` and `:5000` listening. | **CLOSED-ALREADY** | Both seats used the assignment without collision. | none |

## Security Composer (17)

| id | call | STATE NOW | PROPOSED | reason | who acts |
|---|---|---|---|---|---|
| C1 K-Q8 (#152, #178) | Spend migration 0022 on two Low rows now? | REC: both rows `OPEN` at `records/b136`. BACKLOG is unchanged b133 → b136 (`diff --stat records/b133 records/b136 -- BACKLOG.md` = empty; both files 310 lines). | **RULE-DEFAULT:** hold. Fold into the next migration-bearing round with Lane RUNBOOK. | A migration costs a restore cycle. Both rows are Low and unreachable in practice. | none now; a future build seat |
| C2 K-Q12 (#72) | Rename the 7 `HPSM-light` comments now? | The trigger is met: #73 (B134) merged 12:29Z. CODE `eddb484b` (contents API): **7/7 files still hold `HPSM-light`**, 1 each. Control: `policy-summary.ts` = 0. | **RULE-DEFAULT:** now, as a one-commit, comment-only chore. | Its blocker (Lane OUT's directory) has merged. | Composer build seat (7 files: see Seats) |
| C3 K-Q20 (#269 file-name half) | Rename download file names by `policyTitle`? | REC: B134 STATUS `:55` and `:196` "Package file names (`render.ts:170`) are still HELD (K-Q20)". Merged as is (#73: 6 files, no `render.ts`). | **RULE-DEFAULT:** no. Keep the file names. | Stored outputs and e2e downloads pin them. The default is already in force. | records seat (record the ruling on #269) |
| C4 K-Q21 (#159) | PDF-only template version `policy-document-pdf/2`? | CODE `eddb484b`: `policy-document.ts` holds `policy-document/1` (1 hit). There are 0 `pdf/2` hits in `policy-document.ts`, `policy-summary.ts`, `model.ts` or `render.ts`. #73 merged without it, so **the default's vehicle ("join B134 by ADDENDUM") is gone.** | **RULE-OTHER:** yes, but as its own one-row renderers chore in the next Composer build round, not an ADDENDUM. | B134 has already merged. The bump is renderer-only. | Composer build seat (`packages/renderers/src/policy-document.ts` / `document-pdf.ts` + a test) |
| C5 K-Q23 (#66, #70, #71) | In-flight cap, per-address sign-in limit, mutant B37-M2? | REC: all 3 `OPEN` at b136 (b133 → b136 unchanged). | **RULE-DEFAULT:** leave as built. Close #71 as "keep". | Not measured to matter at demo scale. | records seat |
| C6 K-Q24 (#69) | 429 vs 401 for an expired token under a flood? | REC: `OPEN` (low; only under a flood). Row cites `apps/api/src/app.ts`, `apps/web/src/api/client.ts:47`, `problem.ts:79`. Whether the web already handles this 429 is UNMEASURED. | **RULE-DEFAULT:** the web ends the session on that 429 when its own token clock says expired. | No new words. The token has expired anyway, so the user loses nothing they had. | Composer build seat (web: `client.ts` / `problem.ts`), measure-first |
| C7 K-Q25 (#157, #176) | Required properties on closed schemas? | REC: both `OPEN` (Low; noted). | **RULE-DEFAULT:** no change until an external consumer exists. Close as noted. | The web ships with the API. | records seat |
| C8 K-Q26 (#197) | Monospace problem-code line vs the one-font rule? | REC: `OPEN` (design). The "token rule" is a gate instrument (B47/B67 evidence), not product code. There is no font or token test in the code tree (tree grep: only `tokens.css`). | **RULE-DEFAULT:** allow monospace for codes in the token rule. | No visible change. It ends a standing false hit at every gate. | Friday (gate brief text); records seat (close) |
| C9 K-Q27 (#246) | `draftKeyLabel` unused? | REC: `OPEN` (Low) "Leave it … never delete". | **RULE-DEFAULT:** leave it. | Never delete. | records seat |
| C10 K-Q28 (#313) | Accept the 0.011 px overlap; B135 strengthens #314's test only? | GH-PRS: #74 includes `b129-register-band.test.ts`. REC: B135 STATUS `:183` "#313 … held, no CSS change". B136 `:13` "B135 #314: GO". Merged in `eddb484b`. | **CLOSED-ALREADY** | It was built as defaulted. #313 now only needs its "accepted" record. | records seat (close #313 accepted, #314 done) |
| C11 K-Q32 (#26, #34, #154 font, #209(b), #296) | #296(a) guard arm; #209(b) refuse combining-mark-only names; hold the rest? | REC: #26 DEFERRED, #34 DOCUMENTED NOT PROVEN, #154 font half open, #209 (a) DEPLOYED (b) open, #296 "NEEDS FRIDAY'S RULING". Unchanged at b136. | **KAM-CARD** (one line on the next words/look card, default "yes, as drafted"). Hold #26, #34 and #154. | #209(b) and #296(a) each **refuse input the product accepts today**. That changes what users can do. | Kam (card); then a Composer build seat |
| C12 K-Q30 (#171) | Docker address pools: keep per-seat explicit subnets? | HOST: `docker network ls` = **38 networks** (19 `b128*`, 8 `b129*`, 4 `b122*`, 4 `pc*`, plus the 3 defaults). `docker ps -a` = 271 containers (0 running). **The pack says C-39 eased this 30 → 7. It has regrown.** | **RULE-DEFAULT:** keep per-seat explicit subnets. Separately, Friday clears stale seat networks (the row's own fix shape: "Friday/Kam, not a seat"). | The subnets keep briefs working. Regrowth is a housekeeping issue, not a pool-size one. | Friday (prune stale seat stacks after confirming no seat owns them) |
| C13 13 DONE-ALREADY rows | Close #120, 202, 267, 262, 266, 268, 270, 283, 180, 79, 151, 222, 235 in records? | REC: all 13 still `OPEN` at b136. CODE `eddb484b` spot checks, 6 of 13 hold: #202/#267 `ESLINT_TEST_TIMEOUT_MS = 660_000` (`purity-lint.test.ts:21`); #266 `DEPLOY.md:153` 0021 section; #268 `types.test.ts:297` "contract 0.32.0"; #262 follows from #266 + #268; #270 `policyTarget.ts:31` `sectionTitle: "Policy"`; #120 `FeedbackWidget.tsx:341-346` guard. #283, #180, #79, #151, #222 and #235 were not re-read. | **RULE-DEFAULT:** close all 13. | The code evidence holds where measured. The other 6 close by ruling or by the runbook (lane table §5). | records seat |
| C14 #269 scope (worksheet.ts in B134) | Read the worksheet as a policy artefact? | GH-PRS: #73 files include `worksheet.ts` and `change-report.ts`. B136 "#269 titles: GO WITH NOTES". Merged. **New, from B136-N1 (`:83`, Q (1) `:394`):** with a named target, the generation block still prints "Policy <HPSM name>" (`model.ts:406`) on the same page. | **CLOSED-ALREADY** (scope). The B136-N1 follow-on is listed below as N1. | It was built and gated as read. | records seat (#269 → "FIXED for worksheet and change report; file names HELD") |
| C15 records `main` behind `records/b133` | Briefs point at b133 (not at records main)? | REC: records `main` `dab4854d` is an ancestor of b133, b134, b135 and b136 (rc 0 each). **b134 is not an ancestor of b136** (rc 1), so records now sit on **three divergent branches** (b134, b135, b136), all off b133. | **RULE-OTHER:** a records seat folds b133 → b136 plus b134 and b135 into records `main` now, before the next brief. | Pointing each brief at "the newest branch" no longer names one branch. | records seat |
| C16 history.md not written this round | Friday folds history himself? | REC: `records/b136:5_Project_History/history.md` tops out at B133. There are 0 entries for B134, B135 or B136. | **RULE-DEFAULT:** Friday folds. The fold is owed now (3 entries). | It was a deliberate practice change. Its debt is now measurable. | Friday or a records seat (with C15) |
| C17 Lane RUNBOOK and Lane APPROVER | Brief them for the third pane or the next round? | Briefs list: no RUNBOOK or APPROVER brief exists in the project `Briefs/` or `friday/briefs_drafts/`. The only Composer brief after B136 is `B137_SEAT-F_demo-deploy-b134-b135`. | **RULE-DEFAULT:** the next round. RUNBOOK pairs with C1's migration round. APPROVER carries NEW WORDS for Kam. | It is unchanged since drafting. | Composer build seats (next round) |

## HPSM-POC (10)

| id | call | STATE NOW | PROPOSED | reason | who acts |
|---|---|---|---|---|---|
| P1 HPSMPOC-154 | Laptop showcase seed: (a) close or (b) change `ShowcaseStartup.cs`? | CODE: `api/src/HpsmPoc.Api/Showcase/ShowcaseStartup.cs`, last commit `ca554a6` (B14). Untouched by #143–#146. Jira UNMEASURED. | **RULE-DEFAULT:** (a) close. | The laptop showcase is single-user. | Friday (Jira) |
| P2 HPSMPOC-245 | Rule B189 notes N-1, N-2, N-4, N-5, N-6 | Analysis BACKLOG `bb1e8887`: 0 hits for `b189` (case-insensitive; control: 21 `hpsmpoc` hits). Jira UNMEASURED. The next BFF lane is gated on B231, which is **PR #147 OPEN, blocked**. | **RULE-DEFAULT:** accept N-1 and N-2. Ticket N-4 to N-6 into the next BFF lane after #147 merges. | They are durations-only notes. The BFF files are held by #147. | Friday (Jira); later an HPSM build seat (`web/src/server/bff.ts`) |
| P3 HPSMPOC-246 | Rule B193 notes N-2, N-4 to N-7 | BACKLOG: 0 hits for `b193` (same control). Jira UNMEASURED. HPSMPOC-232 ("nothing changes before 13 Oct") lapses today. | **RULE-DEFAULT:** accept N-2. The deploy seat records N-4. N-5 to N-7 go to a timing lane after 13 Oct. | < 0.02 % of the floor. | Friday (Jira); the next HPSM deploy seat; a later timing lane |
| P4 HPSMPOC-248, -249 | Transition both to Done? | GH-PRS: #144 `caa5a971` merged (B224; gate B227 GO WITH NOTES). Jira UNMEASURED. | **RULE-DEFAULT:** Friday transitions both. | Done by #144. | Friday (Jira read, then write) |
| P5 BACKLOG :105 gate B211 N-3 | When to spend the hash-CHECK migration? | CODE `a5fd6355`: `AssessmentDbContext.cs:283` `ck_import_file_hash` and `:286` `ck_import_file_stored_hash` are still `LIKE 'sha256:' + 64 × '_'`. BACKLOG `:105` is still `[ ]`. Imports are OFF on hosted (B230 STATUS `:53`). | **RULE-OTHER:** hold. Fold it into the first HPSM round that needs a migration anyway (the same rule as Composer K-Q8). | Its fix shape is optional. Imports are off on hosted. A migration costs a deploy step. | none now |
| P6 HPSMPOC-229 R3-2 sweep | Leave the pending-run sweep out of B230? | GH-PRS #146: "R3-2, first half". B230 STATUS `:178`: the sweep "stays on HPSMPOC-229 for Friday". B232: "R3-2 first half: CLOSED". | **RULE-DEFAULT:** it stays on the ticket. Brief it as a start-up lane after 13 Oct, before imports are switched on hosted. | It is new start-up behaviour (`Program.cs`, hosted). Imports are off. | a later HPSM build seat |
| P7 B231 item 3 (228 N-9, B220 S-N1) | Keep the case-variant/near-miss tidy-up in B231? | REC: B231 STATUS `:16` built it. B232: "BFF timeout table (N-2, N-9, S-N1): CLOSED (rows 7/7; controls 14/14)". GH-PRS: #147 is **open, blocked** (B233 is fixing CodeQL alert #11 in `web/e2e/hosted-reset.spec.ts`). | **CLOSED-ALREADY** (the call). The merge is pending. | It was kept, built and gated. | Friday (merge #147 after B233) |
| P8 HPSMPOC-149 | Pinned-literal test: hold until B229 lands? | GH-PRS: B228/B229 merged as #145 `55759461` (11:54Z). CODE `a5fd6355`: `Content060ApiTests.cs:119` and `Content061ApiTests.cs:61` still `Assert.Equal("snapshot-policy-aligned@0.1.2", …)`. | **RULE-OTHER:** release the hold. It is READY-NOW. | Its stated blocker has landed. | HPSM build seat (`api/tests/HpsmPoc.Api.Tests/Assessment/Content06{0,1}ApiTests.cs`) |
| P9 HPSMPOC-152 | Hidden-character guard as an `infra/tests` rule? | CODE `a5fd6355`: `git grep -l -i 'bidi\|trojan\|202[AaEe]' -- .github infra/tests scripts` = 0. Control: `def test` hits in 3 `infra/tests` files. 13 files in `infra/tests/`. | **RULE-DEFAULT:** build it as a new `infra/tests` rule. No workflow edit. | The CI infra job already runs `infra/tests`. | HPSM build seat (a new `infra/tests/test_hidden_characters.py`) |
| P10 Parked 92, 96, 117, 232, 234 | Keep them parked? | Jira UNMEASURED. HPSMPOC-232's own window ("before 13 Oct") ends today. | **RULE-DEFAULT:** stay parked. Mark 232 as spent, not reopened. | They are next-phase or ruled. | Friday (Jira comment on 232) |

## New Friday calls surfaced since 10-12 (not in the pack; not counted)
- **N1 (Composer, B136-N1 / Q1):** with a named target, should the generation block keep printing "Policy <HPSM name>"? The proposal is to keep it as is (a relabel is Kam's words). Records #269 as "FIXED for worksheet and change report".
- **N2 (Composer, B136 Q2 / Q3):** is the ≤ 2 s blind window acceptable for #143's soft check? Does #164 close on the limit-with-reason option?
- **N3 (MPS, B58 `:277-278`):** [B58-R1] asks whether an empty `by` equals a missing one, which would tighten the boot check, so PRE-1 must count it first. It also asks Friday to accept that an NFD/NFC pair on a normalisation-sensitive disk opens (identity compare, not NFC).
- **N4 (HPSM, pack §2 item 1):** schedule the UAT stand-up for 14 Oct and ask Kam for a login window in chat. C-52 is already approved.

## Summary

**Counts (from the 37 rows above):**
- CLOSED-ALREADY: **8** (M2, M7, M8, M9, M10, C10, C14, P7)
- RULE-DEFAULT: **20** (M6, C1, C2, C3, C5, C6, C7, C8, C9, C12, C13, C16, C17, P1, P2, P3, P4, P6, P9, P10)
- RULE-OTHER: **8** (M1, M3, M4, M5, C4, C15, P5, P8)
- KAM-CARD: **1** (C11)
- NEEDS-MEASUREMENT: **0**. Jira was unread, so M6, P1–P4 and P10 each start with a Friday Jira GET before the write.
- 8 + 20 + 8 + 1 = 37.

**Rows that need a build seat, by project and files touched:**
- **MPS**
  - M3: `tools/leakscan/**` (new). Disjoint from everything in flight. Tier 3.
  - M5: `src/MpsCalc.Api/Quotes/Proposal.cs` plus `tests/…/QuoteApiTests.ExportRegistry.cs`. **Collides with F3** (the one-pager, `Proposal.cs`), so put it inside F3 or after it. It is disjoint from B58 (`Inventory/**`) and B60 (b47 onto main).
- **Composer:** these three lanes are mutually disjoint by path.
  - **Chore lane C2:**
    - `apps/api/test/b20-rate-limit.db.test.ts`
    - `apps/web/src/markupText.test.ts`
    - `apps/web/src/markupText.testing.ts`
    - `apps/web/src/screens/w2/b20-draft-key-label.test.ts`
    - `packages/api-contract/src/openapi.test.ts`
    - `packages/content/src/b20-codeql-redos.test.ts`
    - `packages/renderers/test/b20-slug.test.ts`
    - Comments only.
  - **Renderers lane C4:** `packages/renderers/src/policy-document.ts` (and `document-pdf.ts` if the constant splits there) plus a new `packages/renderers/test/b13x-*.test.ts`. It shares no path with C2.
  - **Web lane C6:** `apps/web/src/api/client.ts`, `apps/web/src/api/problem.ts` and their tests.
  - **Next round:** C17 RUNBOOK (`DEPLOY.md`, `scripts/health-check.sh`) with C1's migration. C17 APPROVER (`apps/web/src/screens/w3/approverSummary.tsx`).
  - **After Kam's card:** C11 (`apps/api/src/control-characters.ts` for #209(b); `guidedStart.ts` for #296(a)).
- **HPSM-POC:** P8 and P9 are disjoint from each other, from #147 (`web/**`) and from B234 (`.github/workflows/ci.yml` only).
  - **P8:** `api/tests/HpsmPoc.Api.Tests/Assessment/Content060ApiTests.cs` and `Content061ApiTests.cs`. Adds to the `api` CI job.
  - **P9:** a new `infra/tests/test_hidden_characters.py`.
  - **Later:** P2 (`web/src/server/bff.ts`, after #147 merges); P3's timing lane and P6's sweep (`Program.cs`), after 13 Oct.

**Rows for a records seat:**
- **MPS:** M2, M4, M7, M8, M9 (tick or close rows on a records branch).
- **Composer:** C3, C5, C7, C8, C9, C10, C13, C14, plus **C15 (fold the three divergent branches into `main`)** and C16 (history for B134–B136).

**Friday's own writes:**
- Jira: M1, M6, P1, P2, P3, P4, P10.
- Gate and brief text: M4, C8.
- Merges: B58's gate, then #147.
- Housekeeping: C12 Docker network prune.
- The N1–N4 rulings.

## Where the pack's text disagreed with what I measured
1. **C12 / K-Q30:** the pack says C-39 eased the networks 30 → 7. `docker network ls` now shows **38** (35 seat- or project-named).
2. **M9 / B27-H4:** the pack's frame was "503 only where the contract lists it, else BLOCKED-BY-FILES". B54 took a third path: the audit arm is **not needed**, so it was neither built nor BLOCKED (`B54_STATUS:139`). B54 itself is NOT merged (B57 NO GO; B58 awaits its gate).
3. **C4 / K-Q21:** the default "join B134 by ADDENDUM" can no longer happen. B134 merged (#73) without it. `policy-document/1` is still the only version.
4. **C2 / K-Q12:** "after B134 merges" is now true, and all 7 hits remain.
5. **P8 / HPSMPOC-149:** "hold until B229 lands": B229/B228 landed as #145.
6. **M1 / MPSCALC-61:** "dependency scanning … org settings". Dependabot alerts (204), security updates and CodeQL default setup are all already **on**. Only DAST and secret scanning are absent.
7. **M2:** the "ruleset did not block" row is stale. The org ruleset is now active on MPS `main` with a CodeQL rule.
8. **C15:** the pack's "briefs point to b133" is overtaken. Records now split three ways (b134, b135, b136), and `main` is behind all of them.
9. **Context for POC-1** (Kam's row, not mine): gate B232 projects the `api` job at **645 s** against the 900 s cap after B230 (margin 255 s), from the 852 s (= 14m12s) base. So Friday's 14m12s is the pre-B230 base, not today's margin.
