From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to.

# BRIEF B207 (SEAT B): HPSM-POC — B202 fix round 1 of 2: re-base onto main WITHOUT a force-push, then M-1 / M-3 / M-2 / N-1, and the alias ruling on the Automation metrics body (N-3)
**From:** Friday, 15:05 2026-10-11. **Seat:** Datasec/HPSM-POC-B, pane Datasec/HPSM-POC-B. The project's own launcher picks the newest `Briefs/` file containing `_SEAT-B_` (`Launch_Claude.command:110`); this brief is that file. Report `Briefs/2026-10-11_B207_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · NEW WORDS · Records). Last line `READY FOR GATE — b202/attribution-preview-r1 @ <sha>` (the sha read by `ls-remote` after your last push) or `STOPPED: NEEDS FRIDAY` + one question.
**Tier 1** (B202 changed the data model; this round adds no migration and changes one existing API body). Gate round 2 follows as **deltas on the B204 seat** (Seat C); then Kam sees screenshots; then Friday deploys. **Deploy is NOT in this brief.**

## WHERE THIS COMES FROM (read these whole, first)
- `Briefs/2026-10-11_B202_SEAT-B_attribution-preview-and-keys.md` (your B202 brief) and `Briefs/2026-10-11_B202_STATUS.md` (your report: head `62bc3c56147a792049fcbf8136029b78c83ed87b`, 5 commits on `f18359b`).
- `Briefs/2026-10-11_B204_STATUS.md` (the gate). Its verdict lines, verbatim: **"B202 62bc3c5: GO WITH NOTES"** / **"MERGE 3fa5c1b+62bc3c5: STOP — merge-tree conflicts in 7 files (listed below); mechanical: a rebase --onto 3fa5c1b f18359b gives tree a50b999f = the gated head tree, 0 conflicts"**. Findings used here: M-1, M-2, M-3, N-1, N-3 (B204 STATUS :87-124). Its evidence `Briefs/2026-10-11_B204_evidence/item0/merge-tree.txt` gives the full tree id.
- **Kam's alias ruling** (relayed verbatim in B202's brief :12): `hpsmpoc-customer-names-alias-1011` → **(a) "Keep names; alias wherever data leaves the partner"**: *"ORG-nnnnn on anything HP or an export sees."* Ruled 2026-10-11T12:50:18+11:00. The other B202 AUTHORITY rulings (B202 brief :8-15) still stand unchanged.

## PINS (Friday read each one, 2026-10-11 ~04:01Z; instrument inline)
| What | Value | Instrument |
|---|---|---|
| `main` | `3fa5c1b239be39e376717ecf854c9e4af7b52d5d` (B200 squash, PR #135) | `git -C 2_Project_Files --no-optional-locks ls-remote origin refs/heads/main` at 04:00:47Z; `friday_as.sh datasec gh api repos/datasecau/HPSM-POC/pulls/135` → merged, `merge_commit_sha` 3fa5c1b…; `…/commits/main` → tree `3e430382bc250bffa8ee6028140496278c5195ce` |
| `b200/industry-field` | `f18359b70060f2035238025ece0518966a356185`, tree `3e430382bc250bffa8ee6028140496278c5195ce` (byte-equal to main's) | `ls-remote` 04:00:47Z; `git rev-parse 'f18359b^{tree}'` |
| `b202/attribution-preview` | `62bc3c56147a792049fcbf8136029b78c83ed87b`, tree **`a50b999fa3fe85018337f71705a322652fa06c2b`** | `ls-remote` 04:00:47Z; `git rev-parse '62bc3c5^{tree}'`; same id in `B204_evidence/item0/merge-tree.txt` (both the gated head and the `--merge-base f18359b 3fa5c1b 62bc3c5` result) |
| `b202/attribution-preview-r1` | **does not exist** | `ls-remote … refs/heads/b202/attribution-preview-r1` → no line |
| PR #136 (`b203/import-minimise`, Seat D, `Ingest/*` only) | open, not merged, head `9fb82eb5446cf2259418e687a700837b06506b8f` | `friday_as.sh datasec gh api repos/datasecau/HPSM-POC/pulls/136`; `ls-remote` |
| Your worktree `.tools/wt-b202` | on `b202/attribution-preview` @ `62bc3c5`, 0 status lines | `git -C .tools/wt-b202 --no-optional-locks rev-parse HEAD` / `status --porcelain \| wc -l` |

The five B202 commits and their trees (`git log --reverse --format='%h %T' f18359b..62bc3c5`): `86b6ff3` `1b8b2039…`, `e0c5093` `fe4dca88…`, `9a69442` `5007800e…`, `b1860a5` `ff19b02b…`, `62bc3c5` `a50b999f…`. Because main's tree equals `f18359b`'s, a re-base replays each commit onto an identical tree: **each replayed commit's tree must equal its original's**, not just the tip.

**At your start, re-read main** (`ls-remote`) and PR #136 (`friday_as.sh` is Friday's; you use `ls-remote` and the PR's merge state if your `gh` is logged in, else say UNMEASURED):
- main = `3fa5c1b` → proceed.
- main moved, and the new main is PR #136's merge commit (B203, file-disjoint from you; B204 N-10 measured `9fb82eb` merging with `62bc3c5` cleanly and touching no migration file) → **still re-base onto `3fa5c1b`** exactly as below (the tree proof depends on it), and report in BLUF a read-only `git merge-tree --write-tree <new main> <your tip>` result (clean or the conflicting paths). Friday decides whether a second re-base is needed.
- main moved to anything else → **STOP**.

## BASE AND ITEM 0 — RE-BASE WITHOUT A FORCE-PUSH (do this before any new commit)
A force-push is Kam's signature class. **`b202/attribution-preview` is NOT force-pushed, NOT deleted, NOT reset, NOT renamed**; it stays at `62bc3c5` on origin for the record.
- Worktree: your own `.tools/wt-b202` (verify clean at `62bc3c5` first; if it is not clean, STOP — never discard). Scratch `.tools/b207/`. Every code-repo ref write (branch create, rebase, commit, push, any fetch) under the shared lock `.tools/.git-lock` (copy `.tools/b202/lock.sh` to `.tools/b207/`; never remove another seat's lock). `3fa5c1b` is already in the local object store (`git cat-file -e 3fa5c1b…` → present), so no fetch should be needed; if you need one, take the lock.
- Steps:
  1. `git switch -c b202/attribution-preview-r1` in `.tools/wt-b202` (from `62bc3c5`).
  2. `git rebase --onto 3fa5c1b239be39e376717ecf854c9e4af7b52d5d f18359b70060f2035238025ece0518966a356185` (rewrites the NEW branch only).
  3. **Prove before anything else:** `git rev-parse 'HEAD^{tree}'` = `a50b999fa3fe85018337f71705a322652fa06c2b`; `git log --reverse --format='%T' 3fa5c1b..HEAD` = the five original trees above, in order; `git rev-list --count 3fa5c1b..HEAD` = 5; `git rev-parse 'HEAD~5'` = `3fa5c1b…`. Save the transcript to evidence. **If any id differs, STOP** (do not resolve conflicts by hand: the gate's proof is that there are none).
  4. Before push: `ls-remote` shows `b202/attribution-preview` = `62bc3c5` and `-r1` absent. Then `git push origin b202/attribution-preview-r1` (a new branch; **no `--force`, no `--force-with-lease`, no `+refspec`**). `ls-remote` after: `-r1` = your re-based tip, old branch still `62bc3c5`. Record both lines.
- Every later commit in this round goes on top of that pushed tip as a fast-forward. If a push is ever refused as non-fast-forward, STOP.

## PORTS: 6720–6729 only
Friday checked, 2026-10-11T04:01:55Z: `lsof -nP -iTCP:6720-6729` → no process; `docker inspect` of every container's `HostConfig.PortBindings` → none binds 6720–6729; no current brief or STATUS allocates them. In use or reserved elsewhere: 6660–6669 (your B202), 6670–6679 (Seat D B203), **6680–6699 (Seat C B204, still live for gate round 2)**, 6740–6749 (Seat E B205). Plan: 6720 SQL Server (`b207-mssql`, the CI image), 6721 Azurite (`b207-azurite`), 6722 / 6723 API head / mutant, 6724 OIDC stub if needed, 6725 / 6726 web head / mutant, 6727–6729 Playwright and spare. **Re-check with `lsof` before every bind** and state the check in your STATUS.

## THE ROUND (in order; red-first for every new test: the log of it red, then green)
1. **M-1 — the wins' visibility filter.** A regression test (in the showcase or hosted-seed preview tests, e.g. `api/tests/HpsmPoc.Api.Tests/Assessment/AttributionPreviewTests.cs` or `DemoResetTests.cs`) that runs the Admin demo reset **twice** and asserts the `getAttributionPreview` revenue totals (all four categories, and the win count if the body has it) **equal one seed's** — for an **Admin** caller AND a **Demo** caller. The gate measured head holding 70,000 / 13,500 / 12,000 / 25,500 USD after 1, 2 and 3 resets, and **mutant a02** (`AttributionPreviewEndpoints.cs:37`, `engagementIds.Contains(w.EngagementId)` dropped, `w.Synthetic` kept) doubling them after the second reset. **Red-first = your test is RED under a02** (apply a02 in scratch, run, log, restore, show the restore EQUAL by `git diff --quiet`), green at the tip. Run it on SQLite AND your SQL Server.
2. **M-3 — the tag and the zero guard** (vitest in `web/src/components/screens/AttributionPreviewScreen.test.tsx`; e2e in `web/e2e/attribution-preview.spec.ts`):
   - Assert the **"Preview: next phase" Tag inside the PageHeader's tags** (scoped to the header's tag container, NOT `getByText(...).first()`, which the eyebrow alone satisfies; B204 :111). Must go **red under w03** (`AttributionPreviewScreen.tsx:149`, the tag removed), in vitest AND the e2e spec.
   - Render with `notKeyed.customers = 0` and assert **no notKeyed alert**. Must go **red under w01** (`:167`, `> 0` → `>= 0`).
   - Log each mutant red, restored, green.
3. **M-2 — a COMPLETE NEW WORDS table, plus one copy fix.**
   - **Copy fix:** at `AttributionPreviewScreen.tsx:169` the notKeyed body reads "`{N} of their assessments count in the totals and the months…`", which shows "0 of their assessments count…" when none do (B204 measured it in the mock). Write new wording that is true for **0, 1 and N** assessments (and singular/plural customers); test all three cases. It is NEW WORDS for Kam: say it is proposed.
   - **The table** (string · where `file:line` at your final tip · why), covering EVERY string the gate listed (B204 :97-107) and every string B202's table had, so it stands alone:
     - the assessments tile hint (`From this site's own records: every assessment of the customers you can see. N engagements, N partners.`);
     - the column headers `Month`, `Partner`, `Engagements`, `Customer`, `Engagement`, `Industry`, `Staff`, `Printers`, `First assessment`, and the category columns;
     - the three table captions; the screen-reader header suffix ` revenue influenced (sample)`;
     - `Loading the preview…` (:157);
     - the roles line ` The service shows this preview to Admin, Consultant and Demo accounts.` (:161), noting that its order differs from the Partner screen's "Consultant, Admin and Demo users" — list both; do not change either (Kam rules words);
     - the empty-state line `An engagement appears here once a customer is added.` (:174) and its title;
     - the **full** alert title and body (:151-154), every sentence, not cut at "…";
     - the page lead (:150) and the **three section leads** (By month / By partner / By engagement), each in full;
     - the old AND new notKeyed copy;
     - every string item 5 adds to the Automation metrics screen.
     A Playwright or vitest probe that collects every rendered text line on the page (as B204 did, `item3/ui/head.json`) and diffs it against your table is the instrument: **0 rendered lines missing from the table**, stated with its count.
4. **N-1 — four comments say the migration back-filled keys; it does not** (B202 STATUS BLUF: "Existing customers are NOT back-filled"; B204 measured 0 rows in the three tables after up). Correct: `Attribution/AttributionKeys.cs:10` ("the B202 migration back-filled every customer made before"), `Persistence/AttributionEntities.cs:11` ("v4 when the B202 migration back-filled it"), `:18-19` ("back-filled by the B202 migration for every customer before it"), `Endpoints/CustomerEndpoints.cs:129` ("(or the back-fill)"). Say what is true: customers made before B202 have no key row and the preview counts them under `notKeyed`. **Comment-only:** show `git diff` of this commit touches only comment lines (no token outside `//` / `///`).
5. **N-3 — Kam's alias ruling on `getMetricsSummary`.**
   - **Where:** `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs:594` `customerName = names[a.CustomerId]` (names read at :568-569), inside `MetricsSummary` :548. Roles: `Roles.MetricsSummaryPolicy` = Admin, Consultant, Demo (`AssessmentModule.cs:153`, route :255); `Identity/Caller.cs:28` says *"Not Partner: the dashboard is Datasec's."* B204 measured the name in Demo's body (N-3); this is the "Automation metrics" screen HP sees at the event.
   - **So, by the policy, everything this body returns has already left the partner:** replace `customerName` with the stored alias `ORG-nnnnn` (`AttributionKeys.Alias(aliasNo)`, the same `customer_key.alias_no` the preview shows; `AttributionKeys.cs:20`) **for every role this endpoint serves**. A customer with no key row (made before B202; hosted until a reset) gets **no alias and never its name**: return null and show a NEW WORDS label on screen. Prove the alias for a seeded customer equals the alias `getAttributionPreview` shows for it.
   - **STOP and ask Friday** if you find that the change would alter what a Partner sees of their OWN customers (for example a Partner+Demo token, B204 N-5, seeing a customer it owns), or that some caller of this body is inside the partner. The alias applies where data leaves the partner, not inside it. **Do not touch** bodies a partner or the customer reads about itself (e.g. the client follow-up's `customerName`, contract :3787-3790).
   - **Red-first:** an API test (in `MetricsSummaryTests.cs`) asserting, for Admin, Consultant and Demo, that the body carries no live or deleted customer name and that each run's alias matches `^ORG-[0-9]{5,}$` (or is null for a pre-key customer) — RED at your re-based tip, green after. The existing assertion `MetricsSummaryTests.cs:93` (`customerName` = "Quollridge Demo (SYNTHETIC)") changes: list it in HOW. Add a mutant (name back in the body) and show it killed.
   - **Contract:** `MetricsSummary.runs.items` (`api/tests/HpsmPoc.Api.Tests/Contract/openapi.yaml:3243-3247`, `required` includes `customerName`) changes, which is a non-additive change to an existing operation. The contract is `0.16.0-draft` on this unmerged branch: extend B202's 0.16.0-draft changelog paragraph with it unless the contract's own provenance rules require a bump; say which and why. Both copies byte-identical (sha256), `openapi.merged.json`, `npm run gen:api` (`schema.gen.ts`), `contract-drift.test.ts` (:207 pins this `required` list).
   - **Web consumers** (in your partition for this item only): `web/src/lib/metrics-dashboard.ts:11-12, :54`, `web/src/components/screens/MetricsDashboardScreen.tsx:96` (the row's link text), mock `web/src/server/mock/metrics-summary.ts:60` (from the mock store's B202 keys), `web/src/api/client.metrics.test.ts:11`, and their tests; `web/e2e/metrics-dashboard.spec.ts`.
   - **Measure and list in NEW WORDS** everything this changes on the Automation metrics screen (`/metrics`): the Customer column's values, the pre-key label, any caption or hint. Screenshots before (re-based tip) and after, 1440 and one phone, mock build.
   - **Measure, do not change** (FOUND, for Friday): the row still links to `/customers/{customerId}/metrics`, and `customerId` stays in the body (the ruling names names; B202's preview omitted ids). Report whether that linked page shows the customer's name to a Demo caller.
6. **Partition.**
   - **Yours:** the files B202 touched (B202 STATUS HOW :88-114), plus `ReportingEndpoints.cs` and its tests, plus the item-5 web consumers named above, plus the contract copies.
   - **NOT yours — Seat D (B203):** anything under `api/src/HpsmPoc.Modules.Assessment/Ingest/*`, `api/tests/HpsmPoc.Api.Tests/Imports/**`, `api/tests/HpsmPoc.Modules.Assessment.Tests/Ingest/**`, `ImportEntities.cs`, the import tables' config in `AssessmentDbContext.cs`; `.tools/wt-b203`, `.tools/b203/`, ports 6670–6679.
   - **NOT yours — Seat C (B204, round 2 to come):** `.tools/wt-B204-*`, `.tools/b204/`, `Briefs/2026-10-11_B204_*`, containers `b204-*`, ports 6681–6699. **Seat E (B205):** `.tools/b205/`, containers `b205-*`, ports 6740–6749. Never stop, reuse or remove another seat's containers.
   - **No migration change** (no file under `Persistence/Migrations/` and no `*ModelSnapshot.cs` changes; show `git diff --stat <re-based tip>..<final>` with none). Prove 0 files under the B203 paths in `git diff --name-only 3fa5c1b..<final>`.
7. **Suites and report.** Full API suite on SQLite (with your own Azurite so the blob tests run); SQL Server classes on `b207-mssql` (Attribution*, MetricsSummaryTests, ShowcaseSeedTests, DemoReset, HostedDemo*, CustomerApi, ProvenanceViewTests, PersistenceTests; prove it is SQL Server with `@@VERSION` in the log, password masked); vitest, typecheck, lint, build; Playwright at 1280 and 390 (attribution-preview, metrics-dashboard, a11y, responsive, nav-dead-ends); gitleaks over `3fa5c1b..<final>`. Known flakes (B204 N-8: `ImportRobustnessTests.R2_2`; B202: the 700 ms timing floor) are re-run alone and reported, never skipped.

## PRIOR WORK (cite file:line at your re-based tip; its tree equals `62bc3c5`'s, so these Friday-read lines at `62bc3c5` hold)
`AttributionPreviewEndpoints.cs:29-38` (visible scope, keys, wins filter :37); `AttributionPreviewScreen.tsx:148-174` (header + tag :149, alert :151-154, loading :157, roles line :161, notKeyed :167-171, empty state :174); `AttributionKeys.cs:7-12, :20`; `AttributionEntities.cs:11, :17-19`; `CustomerEndpoints.cs:128-129`; `ReportingEndpoints.cs:548-601` (names :568, `customerName` :594); `AssessmentModule.cs:153, :255, :257`; `Caller.cs:28-29`; `MetricsDashboardScreen.tsx:81, :96`; `metrics-dashboard.ts:11-12, :54`; mock `metrics-summary.ts:60`; `MetricsSummaryTests.cs:93`; `contract-drift.test.ts:207`; `openapi.yaml:3243-3247`; e2e `attribution-preview.spec.ts:37, :63`; `AttributionPreviewScreen.test.tsx:53, :69`.

## HOLDS (verbatim from B202, then two lines added for this round)
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)).
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert. **Friday opens the PR.**
- No deploy, no Azure, no setting change; nothing to HP or any human.
- Never delete; quarantine.
- Never print a secret.
- Scoring/priorities unchanged (industry ruling a). No real revenue, no HP data feed, no HP partner id. No AI narrative touches the preview.
- *(Added)* Stop any process of yours by port + cwd (check its working directory first); never by name; never another seat's.
- *(Added)* No force-push of any kind, no branch delete, no rewrite of `b202/attribution-preview` (item 0).

## REPORT
`Briefs/2026-10-11_B207_STATUS.md`, evidence `Briefs/2026-10-11_B207_evidence/` (summaries; kits and raw logs stay in `.tools/b207/`, no scripts in records, B100):
- **BLUF:** the re-base proof (tip tree = `a50b999f…`, the five trees, the push lines from `ls-remote`), main at start and end, the N-3 role reasoning, and the notKeyed copy choice.
- **FOUND** (including the `customerId` / linked-page measurement from item 5).
- **TESTED** (red-first log for every new test, each mutant a02 / w03 / w01 / your N-3 mutant red then restored EQUAL, suites as item 7).
- **HOW** (commits, each with its files; every existing test you changed).
- **NOT TESTED** (honestly; anything UNMEASURED says what would close it).
- **PRIOR WORK** (file:line).
- **NEW WORDS** (the complete table, item 3).
- **Records** (containers left, worktree, ports free at the end by `lsof`).
- Last line: `READY FOR GATE — b202/attribution-preview-r1 @ <sha>` (sha from `ls-remote` after your last push), or `STOPPED: NEEDS FRIDAY` + one question.

## UNMEASURED at draft time (and what closes each)
- Whether PR #136 merges during the round: closed by your start and end `ls-remote` of main (rule above).
- Whether a Partner+Demo token's body could include that partner's own customers on `getMetricsSummary`: closed by your item-5 test with such a token (B204 N-5 measured "seeded customers only" on the preview, not on this endpoint).
- Whether `/customers/{id}/metrics` shows the customer's name to Demo: closed by your item-5 measurement (report only).
- Ports 6720–6729 free at your start: closed by your `lsof` re-check.
