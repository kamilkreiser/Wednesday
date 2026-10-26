# Datasec sweep 20:05: completable tickets and new feedback (read-only, 2026-10-26)

Drafter: read-only sub-agent for Tuesday. Clock from `date`: Mon 26 Oct 2026 20:06:16 AEDT at start (09:06:16Z), 20:13:08 AEDT (09:13:08Z) at the last Jira read, 20:12:47 at the last GitHub read. The feedback and change window opens where `2026-10-26_SWEEP-1430_completable-and-feedback.md` ended: 14:31:46 AEDT = 03:31:46Z. Method and shape copied from that file; every figure below was re-measured now, none copied. GitHub times are Z (AEDT = Z + 11 h). Jira times are as the API prints them (+1100). The Jira JQL window used `"2026-10-26 14:31"` (the account's own zone, assumed AEDT; the 07:49 and 18:53 controls fired as expected, so the filter works).

## BLUF

1. Counts (completable now firm / conditional / blocked-on-words / blocked-on-ruling (new or re-read) / production-HP / new human feedback). Frames: `project = <KEY> AND ( statusCategory != Done )`, page size 100, paged to `isLast` true.
   - HPSMPOC 116 open (2 pages; Backlog 113, In Progress 3): 1 marginal firm (HPSMPOC-349) / 1 conditional (HPSMPOC-228 N-8 half) / words 8 carried / ruling 8 carried (+ HPSMPOC-352 clause 2 re-read) / HP set carried / 0 human feedback. Jira: 0 created, 0 updated since 14:31.
   - MPSCALC 334 open (4 pages; all Backlog; was 325 at 14:30, +9 new): 4 firm (MPSCALC-340, -341, -346, -348) / 3 conditional (-343, -344, -347) / words 1 new (-345) / ruling 1 new (-342) / 0 human feedback. 9 created (MPSCALC-340 to -348), all by one account, the seat account, 0 comments on them.
   - PCOMP 96 open (1 page; all Backlog): 2 firm (PCOMP-62, -63) / 1 serial (PCOMP-22 behind #94) / 1 conditional (PCOMP-12) / words and ruling carried / 0 human feedback. Jira: 0 created, 0 updated since 14:31.
   - RD 765 open (8 pages; To Do 358, Testing 189, Release Ready 199, In Progress 10, Put on Hold 7, Declined 2 = 765): 1 firm (RD-886 part B706-1; session-tools is outside git) / 4 conditional (RD-878 serial behind #120, RD-870 measure first, RD-873, RD-884 step 1) / ruling 7 carried (incl. RD-883) / 0 human feedback. Jira: 0 created, 0 updated since 14:31.
2. CI is RUNNING again. Latest main push runs (instrument below): HPSM-POC 3 success then 1 in progress; MPS 2 success; Composer has no ci workflow (only CodeQL and Dependabot) and its last main push run is a success from 25 Oct; NexusAI main `cb8c8b19` Build in progress (Gitleaks and npm-audit success). The 3 earlier failures on main (HPSM `1523cd2d`, MPS `2e7f9d8a` and `1ac8ab8a`) are from before the first success after the pause. See "CI state" below.
3. PRs landed since 03:31:46Z (merged_at): HPSM-POC #221 (04:58:03Z), #223 (04:58:07Z), #226 (07:10:18Z), #227 (09:11:09Z, during this sweep); MPS #117 (04:51:18Z), #122 (07:01:29Z); Composer none; NexusAI #119 (09:06:38Z). Closed without merge: HPSM-POC #224 (06:51:07Z, replaced by #226), MPS #118 (06:51:40Z, replaced by #122).
4. Corrections to the in-flight list you gave me (re-measured from origin): (a) HPSM-POC #227 is NOT in flight, it merged 09:11:09Z as `1e3ea8a9`; main CI on it is in progress. (b) HPSM-POC #222 (HPSMPOC-354, head `7b3f3c76`, one file `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs`) IS open and was not on your list. (c) NexusAI #119 is NOT in flight, it merged 09:06:38Z. (d) MPS builder B754's branch `b745/mps-walk-caps` already carries two commits (`7a41626e` the supplies-null walk, `d259ae1d` the five BOM walks, 04:40 and 04:43Z), ahead 2 behind 2 of main, no PR yet; it touches exactly 2 files. (e) B752's branch `b744/mps-feedback-triage-my-feedback` head `6896aa43` (07:56:49Z) matches your list, ahead 1 behind 2 of main, no PR yet, 18 files all inside the declared paths. Everything else on your list matched: Composer #94 head `abd07d35`, #95 head `867f3402`; NexusAI #118 head `610a8759`, #120 head `882705bd` with 9 paths.
5. Top lanes (disjoint from each other and from all flight, checked by program): (a) M-EDGES MPSCALC-340 then -341; (b) M-PARITY MPSCALC-346 (firm), then -343 and -344 if the extra-row cap is waived; (c) M-PUBLISH MPSCALC-348 (firm) and -347; (d) C-TESTS PCOMP-62 and PCOMP-63; (e) N-CODEQL RD-873 (CodeQL is running again so closure can be read); (f) N-TOOLS RD-886 B706-1; (g) H-RUNNER HPSMPOC-349 (marginal) and H-GUARD HPSMPOC-228 N-8 (conditional). HPSM-POC has little left that is agent-completable.
6. Feedback since 14:31:46: no human item found on Jira or GitHub. Every comment and every creation is by the seat account (GitHub: 2 issue comments, both the same one-sentence note "Replaced by a new pull request from the same branch and head, so the code scan can start", on HPSM #224 and MPS #118; Jira: 9 new MPSCALC tickets, 0 comments anywhere).

## State of the four repos (origin, `gh api -X GET`, each under its own `GH_CONFIG_DIR`, re-read 20:12 AEDT)

| Repo | main | Open PRs (files; head) | Landed since 03:31:46Z (merged_at Z) |
|---|---|---|---|
| HPSM-POC | `1e3ea8a9` (09:11:08Z) | #222 HPSMPOC-354 (1 file, `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs`; `7b3f3c76`; last update 21:50Z 25 Oct) | #221 (04:58:03Z), #223 (04:58:07Z), #226 (07:10:18Z, the HP logo; 17 files, 1 `hp-logo`, 0 `e2e-runner`), #227 (09:11:09Z). #224 closed unmerged |
| MPS | `1137f119` (07:01:28Z) | #120, #121 dependabot (each `web/package-lock.json`). No PR for `b744` or `b745` (0 each, `pulls?head=`; control `b711` returned 2) | #117 (04:51:18Z), #122 (07:01:29Z). #118 closed unmerged |
| Composer | `8347f91b` (21:46:34Z 25 Oct; unchanged) | #95 (2 files `apps/api/src/routes/engagements.ts`, `apps/api/test/b712-setup-target-locked.db.test.ts`; `867f3402`); #94 (1 file `packages/db/test/b616-deploy-commands.db.test.ts`; `abd07d35`); #91, #86 dependabot; #85 draft (57 files; 0 are `DEPLOY.md`, `api-contract`, `schema.d.ts`, `b116-s10`, `s47-crf2`, `engagements.ts`) | none |
| NexusAI | `cb8c8b19` (09:06:38Z) | #118 RD-867 (1 file `__tests__/sustainability-logger-live.test.js`; `610a8759`); #120 (9 files: `__tests__/helpers/dockerfile-stages.js`, `__tests__/rd618-csp-intake-residue.test.js`, `__tests__/rd774-risk-sql-templates.test.js`, `__tests__/rd777-776-validators-input-filter.test.js`, `__tests__/rd801-feedback-log-injection.test.js`, `__tests__/rd848-no-redundant-copy.test.js`, `backend/logSafe.js`, `backend/simpleDb.js`, `scripts/verify-expected-counts.json`; `882705bd`) | #119 (09:06:38Z, records). |

Landing rule (read from the main commit titles, `commits/main` and `pulls`): HPSM-POC, MPS and Composer main commits are squash titles ending `(#N)`; NexusAI main's last commit is `Merge pull request #119 from datasecau/records/b727`, a merge commit. Source: `gh api -X GET repos/<r>/commits/main`, not a settings read; the repository merge settings were not read.

MPS in-flight branch measures (`compare/main...<branch>`): `b744` ahead 1 behind 2, 18 files: `docs/API.md`, `docs/api/openapi.json`, `src/MpsCalc.Api/Feedback/{FeedbackDtos,FeedbackEndpoints,FeedbackLog,FeedbackStore}.cs`, `tests/MpsCalc.Api.Tests/{EntraAuthTests,FeedbackTriageTests}.cs`, `web/src/feedback/{FeedbackAdminPanel.test.tsx,FeedbackAdminPanel.tsx,FeedbackDialog.tsx,FeedbackTriage.test.tsx,MyFeedback.test.tsx,MyFeedbackPanel.tsx,api.ts,feedback.css,stub.ts,words.ts}`. `b745` ahead 2 behind 2, 2 files: `src/MpsCalc.Api/Quotes/PurchaseValidation.cs`, `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs`. Control: `compare/main...zz-nope` answered 404.

Instruments and controls: `commits/main`, `pulls?state=open&per_page=100`, `pulls/<n>/files`, `pulls/<n>/reviews`, `pulls?state=closed&sort=updated&direction=desc` filtered to `merged_at > 2026-10-26T03:31:46Z` (control: the same call filtered to `merged_at > 2026-10-25T00:00Z` returned 10, 9, 4 and 7 merged PRs for HPSM-POC, MPS, Composer, NexusAI), `issues/comments?since=` and `pulls/comments?since=` (control `since=2026-09-01`: issue comments 6, 3, 3, 7; review comments 12, 11, 5, 26), `issues?state=all&since=` filtered to non-PR (0 in all four), `contents/<path>` (404 on made-up `nope/zz.txt`, real paths answered sizes). A 404 on a real path therefore means "not on origin main".

## CI state, per repo (latest main push run conclusions; `actions/runs?branch=main&event=push`, read 20:1x AEDT)

- HPSM-POC (workflow `ci`): `1e3ea8a9` push 09:11:12Z in progress (5 jobs in progress, 1 skipped, 2 success when read); `68ebdbf7` 07:10:20Z success; `58a863a0` 04:58:10Z success; `ebff49d5` 04:58:05Z success; `1523cd2d` 03:00:14Z failure (9 jobs `failure`, 2 `skipped`; for those 9 jobs the list of steps with conclusion `failure` was empty, which reads as jobs that did not start, but no positive control exists for that step selector, so weak). The PR #227 head run (`ci`, pull_request) read in progress at 08:52:19Z with the CodeQL `dynamic` run success; it then merged.
- MPS (workflow `ci`): `1137f119` 07:01:32Z success; `2d8fede4` 04:51:20Z success (4 jobs success); `2e7f9d8a` 02:43:05Z failure (3 jobs failure, 1 skipped); `1ac8ab8a` 21:47:58Z failure. The first success after the pause on this repo is 04:51:20Z.
- Composer: workflows listed are `Dependabot Updates` and `CodeQL` only (no `ci`); main "Push on main" runs: latest `8347f91b` 21:46:37Z 25 Oct success, none since (no main push since). PR #94 head `abd07d35`: `CodeQL`, `Analyze (csharp)`, `Analyze (javascript-typescript)` all success (08:42:50Z). PR #95 head `867f3402`: `Analyze (javascript-typescript)` and `Analyze (csharp)` both completed `failure` at 03:31:43Z, with no output text; not re-run since (head unchanged). Whether those two failures were the pause or a real result is UNMEASURED; the job logs were not read.
- NexusAI: main `cb8c8b19` 09:06:41Z: Gitleaks Scan success, npm-audit success, Build in progress; `61154bba` 23:08:29Z Build success (deploy-demo `skipped`). Build durations for the last 3 completed main runs: 45.6, 56.8 and 43.2 min (`run_started_at` to `updated_at`), so `cb8c8b19` should finish about 09:50 to 10:05Z. PR #118 head `610a8759`: Build run attempt 3 started 09:05:18Z, in progress at the step "Run tests (verify gate)"; CodeQL, Analyze x3, scan, audit-production-deps success. PR #120 head `882705bd`: Build started 09:01:26Z, same step, in progress; CodeQL checks success.
- Control: HPSM main run list returned 8 rows; the NexusAI jobs query returned the named step for the running job; the same `jobs` query on a completed run (MPS `1137f119` latest main run) returned `success x4`, so the grouping works.

## HPSM-POC (HPSMPOC): 116 open, Backlog 113, In Progress 3

Frame: `project = HPSMPOC AND ( statusCategory != Done )`, 2 pages, `isLast` true; total `project = HPSMPOC AND ( issuekey is not EMPTY )` 354 (4 pages); negative control `summary ~ "zzqxnonexistentphrase"` 0. Window: `project = HPSMPOC AND ( created >= "2026-10-26 14:31" )` 0; `... ( updated >= "2026-10-26 14:31" )` 0; controls `... ( updated >= "2026-10-26 07:49" )` 0 and `... ( updated >= "2026-10-25 18:53" )` 12 (the filter fires; the 12 equals the 14:30 file's figure), so no HPSMPOC record or ticket changed since 14:31. Consequence: records owed for #221 (HPSMPOC-353), #223 and #227 (HPSMPOC-343 follow-up) and #226 (the HP logo): not written yet on Jira.

### COMPLETABLE now (firm)

| Key | Scope | Paths | Open PR or live lane touching them |
|---|---|---|---|
| HPSMPOC-349 (open clause only; marginal) | The remaining clause: make the comment-proof runner rows reflow-tolerant or record each as needing neither. The 26 Oct 00:13 comment reads the clause as not built and says no formatter is configured in `web/`; the comment-stripping half merged in #220. So the honest result is likely a record plus at most one reflow row. `web/src/e2e-runner.test.ts` is 76,107 bytes on origin, `markerStep` 15 hits (positive control; the made-up token returns 0) | `web/src/e2e-runner.test.ts` | None: #226 (17 `web/` files) has 0 `e2e-runner` paths; #222 is `api/` |

### CONDITIONAL

| Key | Scope and condition | Paths | Note |
|---|---|---|---|
| HPSMPOC-228 N-8 half only | The R11 guard reads comments as code (strip comments before matching, or prove the loop at run time). N-3 was closed earlier. Completable only if the ticket's other items (N-2 dead regex in a product file, routeTemplate lowercase, warm-up log level) are left out and N-8 is still open: the line numbers moved (`DISPATCH_LOOP` now at line 727 of `infra/tests/test_security_baseline.py`, 97,191 bytes; the ticket cites 638 to 640), so whether N-8 was already fixed is UNMEASURED. First step is a prior-work read | `infra/tests/test_security_baseline.py` | None open (#222 is one `api/tests` file). Ticket was filed as ruling-blocked in the 14:30 file; the test-only half is the part that could be completable |

In flight or landed, not offered: HPSMPOC-354 (#222 open, no gate state read), HPSMPOC-343 follow-up (#227 merged 09:11:09Z; records owed), HPSMPOC-353 (#221 merged), the HP logo (#226 merged).

### Re-read, not completable by an agent
HPSMPOC-352 clause 2 (the 6+ and mirrored-split boundaries): its 26 Oct comment quotes the gate: not met and "out of lane by the product owner's decision" (ruling). HPSMPOC-318 (the 600 ms row would be green under the accepted floor; the green side near 1190 to 1200 ms is unmeasured on SQL Server; the row would be in `RequestTimingLogTests.cs`, which #222 holds). HPSMPOC-319 B469-5 (needs a recorded real error 1223 from a CI job or local run; no agent can make one on demand). HPSMPOC-311 and -315 (done-when is 1000 and 60 consecutive runs; a hosted-CI or long-loop task). HPSMPOC-314 (capacity measure over the last 10 main pushes; a records move). HPSMPOC-271 (needs an owner and cadence for the Pkcs pin or the hosted ticket Done; a decision). HPSMPOC-292 (accepted behaviour recorded; characterization test merged). HPSMPOC-99 (N-4 is the product owner's, N-9 waits for a scale-out). HPSMPOC-246 (one item, N-4's record, is for a deploy seat). HPSMPOC-226 (B177 N-1 words). HPSMPOC-322 (branch-only, no PR; words-adjacent).

### BLOCKED-ON-WORDS (carried; 0 HPSMPOC tickets updated since 14:31 so no new word can have arrived on Jira)
HPSMPOC-162, -163, -165, -167, -168, -94, -91, -242, and HPSMPOC-310 / -204 are built (records, not lanes) as at 14:30.

### BLOCKED-ON-RULING (carried, not re-read except -352)
HPSMPOC-324, -203, -257, -237, -228 (apart from the N-8 half), -177 and the rest of the 14:30 list.

### Not agent-completable (production or HP)
The hosted-demo and VM tickets (-268, -303, -304, -309, -234, -235, -126, -117, -224, -207), the "awaiting HP" set (-82 to -86, -97, -166, -181, -241) and SOW/event items (-169 to -176, -5, -6, -20, -21 and the workstream epics). Not individually re-read; labels only.

## MPS Commercial Calculator (MPSCALC): 334 open, all Backlog

Frame: `project = MPSCALC AND ( statusCategory != Done )`, 4 pages, `isLast` true; total `project = MPSCALC AND ( issuekey is not EMPTY )` 348 (4 pages); negative control 0. Window: `created >= "2026-10-26 14:31"` 9 (MPSCALC-340 to -348, all `created` 19:08 to 19:09 +1100); `updated >= "2026-10-26 14:31"` 9 (the same nine); control `updated >= "2026-10-25 18:53"` 14 (nine plus five older). Creator on each of the nine is one account id (the seat account). Each ticket was read through `comments()`: 0 comments on all nine. Records owed: #117 and #122 landed (MPSCALC-336, -302 carry the landing notes through the new nine); MPSCALC-325's four walks were in #112; nothing else new.

### COMPLETABLE now (firm)

| Key | Scope | Paths (MEASURED on origin main `1137f119`: sizes) | Open PR or live lane touching them |
|---|---|---|---|
| MPSCALC-340 [B732-1,2] | Tests only: two more rows in the edges file. B732-1: a second sheet that records the same references as a real sheet with other prices (first group stays in force). B732-2: a group whose last supply has no rows cell, with a device link naming the other references then the separator and a space (the document validates today). Each dies under the gate's scratch edit at `ReferenceDocumentValidator.cs:187`. No product byte, no word. Class-round note in the ticket: the fourth NO GO on the class; the new rows are expected to be the closing pins | `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs` (22,081 bytes) | None: #117 landed; B752 holds `EntraAuthTests.cs` and `FeedbackTriageTests.cs`, not this file |
| MPSCALC-341 [B732-3] | Tests only, same file: six assertions of the new refusal body (stage status, validate status, issue count, activate sentence, active version, current reference) and the twin fact's empty-issues assertion are pinned by no mutant the gate ran. Pin each by a targeted mutant or weak-copy pair, or record as a guard. The activate sentence is not a new word (older rows pin it at `GovernedNull.cs:87`, `GovernedNullClass.cs:335`) | the same edges file | Serial with -340 (same file) |
| MPSCALC-346 [B740-5] | Tests only: four AllAgree-is-false assertions that cannot fail on their stores, two assertions never first to fail, one guard that cannot detect its own tamper. Drop them or replace with assertions that can fail (e.g. the report is refused); no extra row required | `tests/MpsCalc.Import.Tests/PanelParityMultisetTests.cs` (18,151 bytes) | None: #122 landed; B754 holds `src/MpsCalc.Api/Quotes/**` |
| MPSCALC-348 [B722-2] | A comment only: the comment above the publish target in `src/MpsCalc.Api/MpsCalc.Api.csproj` (lines 31 to 34) still gives the older patch as its tie example; update to the current tie. No version is typed in the ticket and no behaviour changes; acceptance says only comment lines change and the file stays well-formed XML | `src/MpsCalc.Api/MpsCalc.Api.csproj` (2,119 bytes) | None |

### CONDITIONAL

| Key | Scope and condition | Paths | Note |
|---|---|---|---|
| MPSCALC-343 [B740-1] | One test row (lower-case twin of a map-held SKU on a sheet no device maps; exact lost-SKU sentence; control row). The gate called this a third extra row past its cap of 2 extra rows and asked for the product owner's word, so completable only if that cap does not bind the build seat (UNMEASURED which reading applies) | `tests/MpsCalc.Import.Tests/PanelParityMultisetTests.cs` | Same file as -346 and -344: one lane, in series |
| MPSCALC-344 [B740-2,3] | Two sentence-only survivors; each needs a new row (N14-s plant; a block that lists a lost SKU twice). Same row-cap condition | same file | as above |
| MPSCALC-347 [B722-1] | Either accept the `deps.json` one-entry assertion as structural (a record, no code) or add a scratch-publish row that copies the assembly without listing it so the assertion can be forced. The accept branch needs a ruling-shaped judgement from the coordinator; the row branch is test-only | `tests/MpsCalc.Api.Tests/PublishOutputTests.cs` (4,952 bytes, 87 lines) | The scratch publish runs dotnet locally, not a hosted job |

In flight and not offered: MPSCALC-176 (B752, branch `b744` head `6896aa43`, 18 files as listed above; no PR yet), MPSCALC-338 and -339 (B754, branch `b745` head `d259ae1d`, 2 files; no PR yet; both ticket bodies still show 0 comments). Records only: MPSCALC-336 (#117), MPSCALC-302 (#122 replaced #118), MPSCALC-325, -316 (#107 built the ruled wording).

### BLOCKED-ON-WORDS
MPSCALC-345 [B740-4] (new): `docs/IMPORTER.md` lines 89 to 90 still word the panel check as a count; the sentence is the product owner's; the gate's proposed words are not approved. MPSCALC-169, -288 (follow-up words owed, as at 14:30). V0 to V11 lane features assumed to need words (not individually read).

### BLOCKED-ON-RULING
MPSCALC-342 [B732-SURVIVORS] (new, labelled `needs-ruling`): five survivors and an open-ended strip-one-character family at lines 184, 187 and 207 of the validator; which characters to pin, or accept as residue, is the coordinator's and the product owner's. MPSCALC-310 (Part B not built). The `needs-ruling` label count on the open set is 25 and `question-for-kam` 18 (label counts from the open set, not individually read).

## Security Composer (PCOMP): 96 open, all Backlog

Frame: `project = PCOMP AND ( statusCategory != Done )`, 1 page, `isLast` true; total 97; negative control 0; `created >= "2026-10-26 14:31"` 0; `updated >= "2026-10-26 14:31"` 0; controls `updated >= "2026-10-26 07:49"` 0 and `updated >= "2026-10-25 18:53"` 0. Weak evidence (a zero beside a zero): PCOMP tickets were last touched 25 Oct 13:03 (newest `updated` in the open set; PCOMP-14, -17, -97 at 2026-10-25T13:03), so the board is simply quiet; the window filter itself was shown to fire on the other three boards.

### COMPLETABLE now (firm)

| Key | Scope | Paths | Open PR or live lane touching them |
|---|---|---|---|
| PCOMP-62 | A web test flaky under load: `apps/web/src/screens/b116-s10-verify-dom.test.tsx:120` expects "Hash mismatch" after `downloadManifest()`; make it wait on state, not elapsed turns. Evidence in the ticket: 1 failure in 4 `ci:node` runs under four busy loops; the file alone was green 12 of 12. Test-only; no word. The regression check is a local loop under load (heavy, seat-local) | `apps/web/src/screens/b116-s10-verify-dom.test.tsx` (8,522 bytes) | None: #85 has 0 hits for the path (57 files listed and counted) |
| PCOMP-63 | Comment only: in `packages/engine/test/s47-crf2-linear-detector.test.ts` (31,463 bytes) the SINGLE_SPLIT_BOUND comment should state that the split sees super-linear growth in one string only; the ticket gives the sentence's content, no regression to add | `packages/engine/test/s47-crf2-linear-detector.test.ts` | None |

### SERIAL

| Key | Scope | Paths | Reason |
|---|---|---|---|
| PCOMP-22 | Restore script cut at a statement boundary exits 0 with 0 rows restored: check the dump ends with "PostgreSQL database dump complete" before step 2; add a test with a boundary-cut script. Opus, C4 destroying path (model-routing line 94) | `DEPLOY.md` (58,013 bytes) Route B section; one new db test in `packages/db/test/` (not `b616-*`) | Wait for #94 (`b616-deploy-commands.db.test.ts` reads `DEPLOY.md`; head `abd07d35`, its CodeQL success at 08:42:50Z) to land |

### CONDITIONAL

| Key | Scope and condition | Paths | Note |
|---|---|---|---|
| PCOMP-12 | The Expert Discovery typed editor writes every sub-answer at the engagement level (latent: both content releases declare 0 device-group sub-answers). Completable only if the fix needs no new on-screen sentence; a fix visible on screen becomes BLOCKED-ON-WORDS. Not read past the description | `apps/web/src/screens/Discovery.tsx` (not size-checked; #85 file list scanned for the name: not individually grepped) | Treat as unconfirmed |

Landed since 14:30 that changes the picture: PCOMP-96 (remove the "B587:" prefix) is ALREADY DONE: PR #93 (`0b52848c`, 12:11:09Z 25 Oct, "Contract: take the internal work-number prefix off two approved API sentences") touched `document.ts`; measured the literal `B587:` at `packages/api-contract/src/document.ts`, `openapi.json` and `apps/web/src/api/schema.d.ts`: 2, 2 and 2 hits at `cece687e` (positive control) and 0, 0 and 0 at main `8347f91b`. A records move, not a lane. (The 14:30 file did not list PCOMP-96; this closes that question.)

In flight, not offered: PCOMP-24 (#95; its two CodeQL checks failed at 03:31:43Z and have not been re-run), PCOMP-97 (#94). PCOMP-95 landed in #92 (record owed).

### BLOCKED
Words: PCOMP-94, PCOMP-69, PCOMP-77 (the 2026-10-12 ruling adds a "mark all local" action, which is a new on-screen label), PCOMP-74/-75/-80/-81 (looks). Ruling: PCOMP-46 (warn, never block, still open), PCOMP-9 (design call), PCOMP-65, PCOMP-82, PCOMP-83 (Blocker; half 1 fixed in PR #38, half 2 needs a design), PCOMP-11 (contract change). Ops on the VM or demo (not agent work): PCOMP-10, -18, -78, -93. Behind draft #85: PCOMP-66, -67, -23 and PCOMP-29 to -61 (not individually read). Dev environment risks recorded only: PCOMP-26, -27, -28.

## NexusAI (RD): 765 open

Frame: `project = RD AND ( statusCategory != Done )`, 8 pages, `isLast` true; To Do 358 + Testing 189 + Release Ready 199 + In Progress 10 + Put on Hold 7 + Declined 2 = 765 (identical to the 14:30 file); total 882 (9 pages); negative control 0. Window: `created >= "2026-10-26 14:31"` 0; `updated >= "2026-10-26 14:31"` 0; controls `updated >= "2026-10-26 07:49"` 11 (RD-883 to -886, RD-882, -854, -852, -851, -850, -847, -843: the 14:30 file's eleven) and `updated >= "2026-10-25 18:53"` 11. The newest `updated` among the open set is 2026-10-26T11:41 (Jira zone), so no RD ticket moved after the 14:31 mark.

### COMPLETABLE now (firm)

| Key | Scope | Paths | Open PR or live lane touching them |
|---|---|---|---|
| RD-886 (part B706-1 only) | `session-tools/c57-id-superset.sh` still defaults `LOCK_BASE` to the T9 path (re-measured in the local file: line 38, `LOCK_BASE="${NEXUSAI_LOCK_BASE:-/Volumes/KK_T9_External_HDD/...}"`; the made-up token returned 0 hits). One-line follow-up plus a string arm. Item 3 (repoint or retire four other tools) needs a decision and stays open | `session-tools/c57-id-superset.sh` in the NexusAI project directory. `session-tools/` and that file are NOT on origin (404 on both, beside real paths `scripts/verify-expected-counts.json` 496 bytes and `backend/logSafe.js` 2,257 bytes answering), so no PR and no CI | None; do not edit the lock tool itself |

### CONDITIONAL

| Key | Scope and condition | Paths | Note |
|---|---|---|---|
| RD-878 | `PUT /api/risk-conditions/:id` with a non-string `risk_level` answers 500; completable only if the refusal reuses the existing 400 text ("Invalid risk level. Must be: low, medium, or high"); a new sentence makes it BLOCKED-ON-WORDS. Not re-read in `server.js` this sweep (the 14:30 figure :21233/:21249 is not re-measured) | `backend/server.js` (1,107,905 bytes), one new test, `scripts/verify-expected-counts.json` | SERIAL BEHIND #120: the counts file is in #120's nine paths (checked by program: the only overlap between any lane and any flight) |
| RD-870 | Measure first (read-only): which questions reach `generateUserActivityAnalysis`; then share one capture function or name why not ("name why not" is a ruling) | read-only, then `backend/server.js` and a test | after RD-878 in the chain |
| RD-873 | CodeQL js/insecure-temporary-file and file-system-race alerts 96, 97, 98, 99 and 116 in test code; re-shape in code, never dismiss. CodeQL is running again, so closure can now be read by alert number: measured now by `code-scanning/alerts/<n>`: 96, 97, 98, 99 `open` (`js/insecure-temporary-file`) and 116 `open` (`js/file-system-race`), all at `refs/heads/main` `cb8c8b19`; control alert 95 reads `fixed` at `19b7106b`; made-up alert 999999 answered 404 | `__tests__/erasure-verdict-is-derived-from-failures.test.js` (10,937 bytes), `__tests__/initialize-files-uses-shared-recovery-list.test.js` (5,680), `__tests__/helpers/rd407-setting-writer.js` (3,418), `__tests__/rd407-concurrent-settings-writers.test.js` (32,195) | None of these four is in #118 or #120. Whether the re-shape changes a test count and so the counts file is UNMEASURED; if it does, it joins the counts chain |
| RD-884 | Step 1 only (read earlier release and build records for a registry build of a commit carrying Dockerfile lines 46 and 100). Step 2 needs a registry or docker build: a production-class touch, not agent-completable | read-only | step 2 excluded |

In flight and not offered: RD-885, RD-849 and RD-876 part 1 (PR #120, 9 paths), RD-867 (PR #118). Records (not lanes): RD-847 and the B703 tickets (Testing). The #119 records PR merged 09:06:38Z.

### BLOCKED-ON-WORDS
RD-872, RD-869, RD-876 part 2 (the "limited" notice and show-all button), carried.

### BLOCKED-ON-RULING
RD-883 (cap the length of a filtered value, and the size), RD-858, RD-855, RD-859, RD-868, RD-845, RD-842; also `needs-decision` To Do tickets RD-884, RD-622, RD-612, RD-610, RD-368 (labels read; not individually re-read). The label `needs-decision` appears on 15 open tickets. RD-861 and the ~350 older To Do tickets were not read.

### Production touch
The 189 Testing and 199 Release Ready tickets; the 10 In Progress (marketplace, hosted deploy, VM decommission: RD-662, -643, -450, -81, -49 and others) are production-adjacent by label.

## LANES (disjoint, priority HPSM-POC, MPS, Composer, NexusAI)

Rule: a lane's YOURS paths share no path with another lane's YOURS, nor with any open PR file list or in-flight branch, except the declared serial shares. One seat, one branch per lane. Push the seat's own branch only; Tuesday opens PRs and lands them through CodeQL. Model: test-only rows go to model-routing line 85 (L6 test-only pin) and line 92 (C2) at Sonnet first; PCOMP-22 is Opus (line 94).

| Lane | Tickets | YOURS | NOT YOURS | Model | Serial? |
|---|---|---|---|---|---|
| H-RUNNER (marginal) | HPSMPOC-349 open clause | `web/src/e2e-runner.test.ts` | all `api/**`, `infra/**`, other `web/**` | Sonnet, line 85 | no |
| H-GUARD (conditional) | HPSMPOC-228 N-8 half | `infra/tests/test_security_baseline.py` | `api/**`, `web/**` | Sonnet, line 85 | no; prior-work read first |
| M-EDGES | MPSCALC-340, then -341 | `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs` | `src/**`, `docs/**`, the Feedback files B752 holds, `QuoteWalkCaps*`, `PurchaseValidation.cs` | Sonnet, line 85 | -340 then -341 (one file) |
| M-PARITY | MPSCALC-346 firm; -343, -344 only if the row cap is waived | `tests/MpsCalc.Import.Tests/PanelParityMultisetTests.cs` | `src/MpsCalc.Import/**` (no product byte), `docs/IMPORTER.md` (words) | Sonnet, line 85 | in series inside the lane |
| M-PUBLISH | MPSCALC-348 firm; -347 conditional | `src/MpsCalc.Api/MpsCalc.Api.csproj` (comment lines only), `tests/MpsCalc.Api.Tests/PublishOutputTests.cs` | any version number, `web/package-lock.json` (#120, #121) | Sonnet, line 85 | no |
| C-TESTS | PCOMP-62, PCOMP-63 | `apps/web/src/screens/b116-s10-verify-dom.test.tsx`, `packages/engine/test/s47-crf2-linear-detector.test.ts` | `DEPLOY.md`, `packages/db/**`, `apps/api/**`, `content/**`, #85 files | Sonnet, line 85 | no |
| C-RESTORE | PCOMP-22 | `DEPLOY.md` Route B section; one new db test in `packages/db/test/` (not `b616-*`) | `packages/db/test/b616-deploy-commands.db.test.ts`, `apps/api/**` | Opus, line 94 | YES: after #94 lands |
| N-CODEQL | RD-873 | the four test paths listed above | `backend/**`, the #120 files, the counts file | Sonnet, line 85 | no; reads closure by alert number |
| N-TOOLS | RD-886 part B706-1 | `session-tools/c57-id-superset.sh` | everything in git | Sonnet, line 92 | no |
| N-SERVER | RD-878, then RD-870 (conditional) | `backend/server.js` regions, one new test, `scripts/verify-expected-counts.json` | the nine #120 files except as declared | Sonnet, line 92 | YES: after #120 lands (counts file) |

Cross-lane check, RUN AS A PROGRAM this time (python3 -I over the lane YOURS lists against every lane pair and against every open-PR file list measured above plus the two MPS branch lists): lane-vs-lane overlaps 0; lane-vs-flight overlaps exactly 1: N-SERVER with NexusAI #120 on `scripts/verify-expected-counts.json` (declared serial). Controls that fire: a deliberate probe (`src/MpsCalc.Api/Quotes/PurchaseValidation.cs` against B754's file list) returned the overlap, and `scripts/verify-expected-counts.json` in the #120 list returned True. M-WALKS and N-CHAIN from the 14:30 file are gone: their tickets are now in flight (B754, #120).

## FEEDBACK since 14:31:46 AEDT (03:31:46Z, 26 Oct)

- PRs landed (merged_at Z), as in the table above: HPSM-POC #221, #223, #226, #227; MPS #117, #122; NexusAI #119. Composer 0.
- New tickets (created since 14:31): HPSMPOC 0, PCOMP 0, RD 0, MPSCALC 9 (MPSCALC-340 to -348), all created by the seat account, with the labels `mpscalc-b751` and `plan-b751-*` (the records pass for the gates B732, B740 and B722), two labelled `needs-ruling` (MPSCALC-342, -345). Comments since 14:31 on any ticket: 0 on the four boards (no ticket other than those nine was updated; the nine carry 0 comments). Across all comments read in this sweep (on the tickets I opened; not counted) exactly one author id appears, so a human cannot be told from the seat on Jira by id; by that id every item is the seat account's. Control: the 14:30 file's 11 comments since 25 Oct 18:53 on HPSMPOC are in the `updated >= 2026-10-25 18:53` count of 12 here.
- GitHub: `issues/comments?since=2026-10-26T03:31:46Z` returned 1 on HPSM-POC (#224, 06:51:07Z) and 1 on MPS (#118, 06:51:39Z), 0 on Composer and NexusAI; each is the same 89-character sentence closing a PR that was replaced to start the code scan, and each was written by the account that authored the PRs (user id equal to the PR author's on #221 to #227, #117, #118, #122, #94, #95, #85, #118, #119, #120; type User, association member). `pulls/comments?since=` 0 on all four. `pulls/<n>/reviews` 0 for every open PR (#222; #120, #121; #95, #94, #91, #86, #85; #118, #120) and for the merged #227. Non-PR issues since: 0 on all four. So: no feedback item from a human on Jira or GitHub in this window.
- Not read (fences): mail, the NexusAI app store, QuickQuote, Vision, the HPSM Composer store, decision cards, chat boards, the fleet inbox. "No new feedback" holds only for Jira and GitHub.
- Cards Tuesday owes (from this window): MPSCALC-342 (which characters to pin at the three lines, or accept the residue), MPSCALC-345 (the importer docs sentence), MPSCALC-343/-344 (waive the extra-row cap?), HPSMPOC-352 clause 2 stays with the product owner's earlier decision; the 14:30 owes still stand (RD-883, RD-884 measurement path, RD-876 part 2 words, MPSCALC-169 and MPSCALC-288 follow-up words, PCOMP-46).

## FOUND

1. #227 merged during this sweep (09:11:09Z) and #119 merged at 09:06:38Z, 22 seconds after it began; HPSM-POC has one open PR (#222) not on your list. Those two lanes are no longer protected paths; #222 is.
2. PCOMP-96 is already done by #93 (measured both ends: 2 hits per file at `cece687e`, 0 at `8347f91b`). A records move.
3. MPSCALC-338 and -339 are built on branch `b745` at `d259ae1d` (04:43Z) and not yet a PR; the branch head (04:43Z) is about 4.5 hours old at 09:13Z, so if B754 is on round 2 that round is either unpushed or not on this branch. UNMEASURED which.
4. The MPS gate residues from B732 and B740 and B722 were ticketed as MPSCALC-340 to -348 at 19:08 to 19:09 (+1100); seven of nine are test-only or comment-only, which makes MPS the richest source of completable lanes.
5. CodeQL is back: PR heads #94, #118 and #120 show green CodeQL checks, and alert state is readable by number; Composer #95's two analyses failed at 03:31:43Z and have not been re-run.
6. No human has written on any board or PR in this window.

## TESTED (controls that could fail)

- Board totals: negative control 0 on all four; `issuekey is not EMPTY` 354, 348, 97, 882; RD status sum 765; MPSCALC open set 334 equals 348 total minus 14 Done (not separately counted).
- Window filters: `updated >= "2026-10-25 18:53"` returned 12 (HPSMPOC), 14 (MPSCALC), 0 (PCOMP), 11 (RD); `updated >= "2026-10-26 07:49"` returned 0, 9, 0, 11; the 14:31 window returned 0, 9, 0, 0 and the nine MPS tickets are those created. The PCOMP zeros are weak (see its frame).
- Instrument note: counts of the window were taken both by paging the search endpoint (`POST /rest/api/3/search/jql`) and by `POST /rest/api/3/search/approximate-count` at 20:13; the two agreed (0, 9, 0, 0).
- GitHub: file-list controls (counts above, e.g. #85 57 rows, #226 17 rows with `hp-logo` 1 and `e2e-runner` 0); `compare` on a made-up branch 404; contents 404 on `nope/zz.txt`; `code-scanning/alerts/999999` 404 against alerts 95 to 99 and 116 answering; merged-since controls 10, 9, 4, 7.
- Contents greps: `grep -c zzqxnone` returned 0 on the fetched `document.ts` and `test_security_baseline.py` and on the local `c57-id-superset.sh`, while real tokens (`B587`: 35 hits in `document.ts`; `DISPATCH_LOOP` at lines 727 and 760; `markerStep` 15; `LOCK_BASE=` line 38) hit.
- Lane overlap program: see the LANES section (two controls fired).
- Weak: whether any lane's source blob text matches the ticket's line numbers (I read file sizes, not the cited lines, for the MPS test files, `PublishOutputTests.cs`, `Discovery.tsx`); HPSMPOC-228's current state; the "did not start" reading of the 3 pre-pause main failures rests on an empty failed-steps list with no positive control.

## HOW

Jira: `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/.tools/b649/jira.py` loaded in-process through `importlib` inside `python3 -I` scripts (the same helper SWEEP-1430 used; POST to the search endpoint, plus POST to the approximate-count endpoint and GETs of single issues and their comments through the helper's own `api`/`comments`); every JQL is `project = <KEY> AND ( ... )`; pagination by `nextPageToken` until `isLast`; credentials in-process only, never printed. GitHub: `gh api -X GET` under each repo's own `GH_CONFIG_DIR` (one `case`-free shell function taking the project folder and repo; no associative arrays; the first script's output files collided on a case-insensitive filesystem for the `open_pcomp` and `open_PCOMP` names, so the Jira lists were re-fetched into fresh files before any count was written down). Model lines from `fleet/specs/model-routing.md` (lines 85, 92, 93, 94, 108, 109 read directly). Scratch scripts and fetched copies are in the session scratchpad.

## UNMEASURED

- Mail, app stores, cards, chat, CLARIFICATIONS, the repository merge settings.
- Verdicts of any live gate (B752, B754, #118, #120, #94, #95, #222) and whether #222 is gated.
- Why Composer #95's two CodeQL analyses failed at 03:31:43Z; whether `cb8c8b19`, `1e3ea8a9`, #118 and #120 Build runs finish green (all in progress).
- Whether the MPSCALC-343/-344 extra-row cap binds a build seat; whether MPSCALC-347 should be accepted or built; whether HPSMPOC-228 N-8 is still open; whether the RD-873 re-shape changes the counts file; whether PCOMP-12 needs a new sentence.
- RD-878's current line numbers, RD-870's reach, RD-884's registry answer.
- Not individually read: the ~330 older MPSCALC tickets beyond the nine new ones and the dozen re-read, PCOMP-29 to -61 and -66/-67/-23 behind #85, the HPSMPOC blocked and HP sets (carried), ~350 older RD To Do tickets.
- Jira timestamps are compared as printed (+1100 assumed to be AEDT); load and run times.

## Outside-the-fences disclosure

- My first GitHub script wrote its PR-list output files with names that differ only by case from the Jira output files (`open_pcomp.json` over `open_PCOMP.json`, `open_rd.json` over `open_RD.json`) on a case-insensitive disk, which broke one Python read of the Jira lists; I re-fetched the Jira lists (read-only) and re-ran before counting. No figure here comes from the broken read.
- One `ls` of `/Volumes/Laptop-DEV/!CODING/Datasec/` and of the HPSM-POC `4_Credentials/` folder (names only) to find the helper and the config directories, and one local `grep` of NexusAI `session-tools/c57-id-superset.sh` (the file is outside git). No `.env` was opened or printed; the Jira helper reads it in-process.
- I used `gh api -X GET` on `code-scanning/alerts/<n>` and `actions/runs/<id>/jobs` and `check-runs` (read-only API GETs on the GitHub API host only); no hosted, demo or production host was contacted. One Jira call per ticket and per window; no Jira write. No git command in any project clone (all code reads were origin contents or compare calls). No mail, chat, Artifact, Docs or decision-queue call, no scoreboard, `_ledger*`, WEDNESDAY or FRIDAY tree. I wrote only this file.
- No person's name is printed in this file; reviewers and client staff are referred to as the product owner or the seat account.

SWEEP DONE /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_SWEEP-2005_completable-and-feedback.md
