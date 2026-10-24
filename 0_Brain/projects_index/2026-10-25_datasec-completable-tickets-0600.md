BLUF: Five lanes can START NOW with an empty program-computed intersection against every open PR and against each other, plus two lanes that start only on a word (8 lanes, 28 lane pairs and 11 lane-vs-PR pairs checked, 0 overlaps; 11 planted controls all fire). Model: Sonnet for all of them (Datasec has no local tier; routing table C2, G1/G2; no row here is an auth, security-design or data-destroying build, so no Opus).
1. HPSM-POC H-CI: HPSMPOC-314 (rebalance the two SQL Server test shards; the ticket's "limit 20" is stale, main says 30). Path `.github/workflows/ci.yml`. Sonnet, gate tier 2.
2. MPS M-A2: MPSCALC-325 (cap the four draft-validation walks). Paths `src/MpsCalc.Api/Quotes/PurchaseValidation.cs`, `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs`, NEW `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs`. Sonnet, tier 1. (MPSCALC-331 and -333 are in open PR #110 and are NOT in this lane.)
3. MPS M-WEB: MPSCALC-334 (stub test file, bundle key list, one `exact: true`) and MPSCALC-329 (reword two header comments only). Paths `web/src/api/stub/stubApi.test.ts` (NEW), `web/src/api/stub/stubApi.ts` (only if the rental stub is taken), `web/scripts/check-bundle.mjs`, `web/e2e/bom.spec.ts`, `tests/MpsCalc.Engine.Tests/ReconciliationContractRemainder.cs`. Sonnet, tier 2.
4. Composer C-TEST: PCOMP-62 (make a flaky wait state-based) and PCOMP-63 (one comment). Paths `apps/web/src/screens/b116-s10-verify-dom.test.tsx`, `packages/engine/test/s47-crf2-linear-detector.test.ts`. Sonnet, tier 2.
5. NexusAI N-CI: RD-814 (least-privilege `permissions` on three workflows; read each job first, an OIDC login needs `id-token`). Paths `.github/workflows/build.yml`, `deploy.yml`, `npm-audit.yml`. Sonnet, tier 1 (workflow change gets its own review).
On a word: 6. HPSM-POC H-AUDIT: HPSMPOC-348, starts when Tuesday names style A or B (candidate in section 3; recommendation B). Path `web/src/audit-dev.test.ts` (ci.yml read-only). Sonnet, tier 2. 7. MPS M-FEEDBACK: MPSCALC-176 (large feature, approved word pack on file; reserve, start only with capacity). Sonnet, tier 2.
Candidate, NOT startable: NexusAI RD-844 real fix (section 2): the route/stub choice makes the guard measure setup.html and status.html with the Font Awesome stylesheet stubbed, so it wants a one-line owner ruling first.
CARD candidates (word-blocked or ruling-blocked, one question each): see section 4 (10 rows).
Feedback: NO human in Jira or GitHub since 21:00 AEDT (every Jira comment and ticket is the seat account 616503; zero GitHub issue comments on six repos). One bot item, unchanged from the 01:20 file: the CodeQL review comment on merged HPSM-POC PR #211 (alert #13, js/file-system-race); no open ticket names it. Mail and the NexusAI app store NOT measured.

# Datasec: completable tickets and feedback, 06:00 sweep (read-only research, 2026-10-25)

Researcher: read-only sub-agent (claude-sonnet-5-5) for Tuesday. Clock from `date`: Sun 25 Oct 2026 05:49:56 AEDT at start, 05:56:20 AEDT at the last Jira read (intersection run a few minutes earlier) (UTC = AEDT minus 11 h; the feedback window opens 21:00 AEDT 24 Oct = 10:00Z). Base and method: [[2026-10-25_datasec-completable-tickets-0120]] (shape cloned; its lane partition, intersection program and feedback table are the template). Scope: MPS Calculator (MPSCALC), HPSM-POC (HPSMPOC), Security Composer (PCOMP), NexusAI (RD). Skipped: myPKI, CypherKey, Lead_Bot. Jira = GET only, every JQL is `project = <KEY> AND ( ... )` with the parentheses around everything after the project clause (the helper builds it; no JQL was typed without it), totals only through the nextPageToken read until isLast. Credentials read in-process from each project's own `4_Credentials/.env`, never printed. GitHub = `gh api -X GET` with that project's own `GH_CONFIG_DIR`. No git write verb, no clone, fetch, build or test; no HTTP to any production host. Wrote this one file (plus scratchpad scripts and fetched read-only copies).

## 0. What changed since 01:20 (each read at source)

| Item | Source | Result |
|---|---|---|
| HPSM-POC PR #212 landed | `pulls/212` | merged 2026-10-24T17:56:39Z (04:56 AEDT), squash `09641a91`; files: `Hpsmpoc178CustomerNameTests.cs`, `HostStartRetryTests.cs`, `web/src/e2e-runner.test.ts`, `web/src/server/mock/customer-name.test.ts` (= HPSMPOC-344 property half, -347, -349). Main is `09641a91`; open PRs 0 |
| The three tickets after #212 | JQL key in (...) | HPSMPOC-344, -347, -349 are still Backlog (last updated 00:39 to 00:43 AEDT, before the merge): record moves for the records seat |
| MPS | `commits/main`, open pulls | main unchanged `93e1cab5`; PR #110 open, head `34ccb02b`, 4 files (`ReferenceDocumentValidator.cs`, `QuoteRefusalOrder.cs`, `QuoteRefusalOrderGuard.cs`, NEW `SourceLifecycleTests.GovernedNull.cs`). The new test file is named `GovernedNull`, not the `B610GovernedNull` name the 01:20 file proposed |
| Composer | same | main unchanged `e019ac3a`. Open: #89 (11 files: DEPLOY.md, migrations 0026 and 0027 with reversers, `packages/db/test/**` rows incl. `b616-b593-survivors.db.test.ts`), #88 head `0ba2a6b0` (3 files: `apps/api/src/app.ts`, `apps/api/test/b593-year-zero-date.db.test.ts`, `packages/api-contract/src/openapi.test.ts`; updated 18:42Z = 05:42 AEDT), #86 (2 files), #85 (draft HOLD, 57 files) |
| NexusAI | same | main MOVED `bda30039` -> `19b7106b` (PR #108, nodemailer / smtp-server, merged 14:52Z): `package.json` and `package-lock.json` are no longer held by an open PR. Open: #110 head `2f9c3e1b` (3 files: `backend/server.js`, `__tests__/erasure-reaches-every-read-location.test.js`, `__tests__/rd407-concurrent-settings-writers.test.js`) and #67 |
| NexusAI #110 round 2 | `pulls/110/commits` | four commits: RD-862 delete (15:13Z), RD-844 domcontentloaded change (15:17Z), RD-873 (15:27Z), then the REVERT of the RD-844 change at 18:40Z (05:40 AEDT), "RD-844 stays open". The PR title and body still describe RD-844 as done (not yet edited; the net diff has no guard file). `mergeable_state` unstable |
| NexusAI #67 | `pulls/67` | `mergeable_state` is now `dirty` (merge conflicts), last updated 7 Oct. Measured here for the first time (the 01:20 file had "unknown") |
| Jira since 01:20 | `updated >= "2026-10-25 01:20"` | 0 issues on all four boards; created since 21:00 unchanged (HPSMPOC 3, MPSCALC 4, PCOMP 0, RD 0) |
| Composer #88 / #89 | file lists | #88's three files are exactly the C-API lane of the 01:20 file; #89 holds C-DB (0026, 0027, DEPLOY.md, db tests) |

## 1. How I measured (every count names its query)

| Count | Query / command | Result |
|---|---|---|
| Open per board | `project = <K> AND ( statusCategory != Done )`, nextPageToken until isLast | HPSMPOC 119, MPSCALC 320, PCOMP 93, RD 760 (all equal to the 01:20 file) |
| Created since 21:00 | `project = <K> AND ( created >= "2026-10-24 21:00" )` | HPSMPOC 3 (-347, -348, -349), MPSCALC 4 (-331..-334), PCOMP 0, RD 0; creator of all 7 is `616503` |
| Done since 21:00 | `project = <K> AND ( statusCategory = Done AND statusCategoryChangedDate >= "2026-10-24 21:00" )` | HPSMPOC 7 (-345, -342, -340, -338, -337, -328, -320), others 0 |
| Updated since 21:00 | `project = <K> AND ( updated >= "2026-10-24 21:00" )` | HPSMPOC 12, MPSCALC 18, PCOMP 0, RD 9 |
| Control, non-zero | `project = <K> AND ( created >= "2026-10-21 00:00" )` | HPSMPOC 45, MPSCALC 19, PCOMP 94, RD 6 (the created filter fires on every board) |
| Main shas and open PRs | `commits/main`, `pulls?state=open&per_page=100` | HPSM-POC `09641a91`, 0 open; MPS `93e1cab5`, #110; Composer `e019ac3a`, #89 #88 #86 #85; NexusAI `19b7106b`, #110 #67 |
| Open PR file lists | `pulls/<n>/files --paginate` | MPS #110 4; Composer #89 11, #88 3, #86 2, #85 57; NexusAI #110 3, #67 3 |
| Trees | `git/trees/<sha>?recursive=1` | HPSM-POC 1323 blobs, MPS 644, Composer 951, NexusAI 955; none truncated. Every lane path below exists on main unless marked NEW (program check: 0 missing) |
| Ticket text | issue GET plus comment GET | each ticket named in sections 2 and 3 was read (description; comments where the count is noted) |

## 2. NexusAI RD-844, the real fix: candidate lane N-GUARD (NOT startable until the question in 2.4 is answered)

Ticket (read in full, one comment): the rd490 guard waits for the page `load` event; two pages (`setup.html`, `status.html`) load `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css`, so a slow CDN failed main's push Build once (38340787055, 3 failed cells, `page.goto` timeout 20000 ms). The same SHA passed on rerun. The ticket's own recommendation lists two ways: route or abort the page's off-host requests, or wait for `domcontentloaded` plus the banner.

What I read on main `19b7106b`:
- `tests/e2e/open-access-banner-guard.js` line 294: `page.goto(url, { waitUntil: 'load', timeout: 20000 })`; the page-level hard limit is `hardTimeoutMs = 45000` (line 284); `trackRequests` waits up to `QUIET_TIMEOUT_MS = 15000` for no request in flight (line 72, 259-276).
- The RD-844 first attempt (waiting for `domcontentloaded`) was written and then REVERTED in open PR #110. Its PR body records the builder's finding: "a stylesheet that never answers still fails later (about 46 s)". That is the reason `domcontentloaded` alone is not the fix: a stylesheet link in the head blocks rendering, and the 45 s hard limit then trips. So the fix is the route/stub option.
- `git/trees`: three pages name cdnjs (`static/setup.html` line 8, `static/status.html` line 9, plus `marketplace-landing.html`, which the guard does not measure; the ticket's grep says the same three). Bootstrap comes from jsDelivr on the same two pages and that host has not failed in the 40-run history the ticket measured.
- The banner's own `static/css/open-access-banner.css` and `static/js/open-access-banner.js` contain no `fa-`, `font-awesome`, `icon` or `url(` (grep with positive controls on the html files, which do match). So the banner itself does not use the icon font.
- RD-721 (vendor the CDN assets into the image) is in status Testing; `setup.html` and `status.html` on main still link cdnjs, so it has not removed the dependency.

Scope (files): `tests/e2e/open-access-banner-guard.js` (add an off-host route in `guardPage`, before `page.goto`: answer requests to host `cdnjs.cloudflare.com` with an empty 200 `text/css` stand-in; count the requests it rewrote and put the count in the returned measurement `m`), and `__tests__/rd490-open-access-banner-browser.test.js` (the cells below). `tests/e2e/open-access-banner-concealments.js` read-only. `scripts/verify-expected-counts.json` must NOT change (see PR #67 below). No product file, no `static/**`.

What the test must show (red-first, each at the unmodified guard first):
1. A cdnjs request that never answers (the test serves a route that never fulfils) makes the UNMODIFIED guard fail on setup.html and status.html (timeout) and the modified guard pass both, in under the 20 s navigation limit. This is the failure the ticket describes, reproduced on demand, not waited for.
2. The stand-in rewrites ONLY cdnjs: on every measured page the rewritten-request count is 1 on setup and status and 0 on the other ten; jsDelivr and local requests are untouched (counted).
3. The measurement count does not change (the run line `[RD-490] ... 60 measurements` stays 60) and no cell is added, so the counts file is untouched. If a new cell is wanted, it adds to the `tests` and `suites` totals in `scripts/verify-expected-counts.json`, which open PR #67 also edits (and #67 is now `dirty`): do not add cells until #67 is closed or merged.
4. Every existing red cell is still red on the check that must catch it, and every identity control stays green with the stand-in in place.
5. A one-time comparison, recorded in the PR: the banner measurements (box, contrast, ink fraction, covered check) on setup.html and status.html with the stand-in against the same pages with the real stylesheet, on a fast network. That run needs an outbound request to cdnjs, a public CDN, not a production host; the builder runs it, not this sweep.

Needs a product-owner ruling? RECOMMEND YES, one line. The guard's contract (header of the file) is "seen as a person sees it". With the stand-in the guard measures two pages without their icon glyphs, which is a different page from the one a person loads. The ticket's own recommendation names the stub option, but it was written by a seat, not the owner, and the guard is the owner's mitigation for the open-site banner. The change is test-only and the banner does not use the icon font, so I rate the risk low; it is still a change to what the mitigation measures. Question (one): "May the open-site banner guard measure setup.html and status.html with the Font Awesome stylesheet answered by an empty stand-in instead of loaded from the CDN?"

Ordering: the guard files are not in #110's net diff now (checked: 3 files, none in the guard), so the file intersection is empty today. The branch history of #110 holds an add and a revert of the same two files; start N-GUARD after #110 lands, or at least re-read #110's file list at launch. Model: Sonnet, gate tier 2 (test-only; the gate checks the red proofs).

## 3. HPSMPOC-348 candidate (lane H-AUDIT, starts on Tuesday's word)

Ticket read in full. Today's state on main `09641a91`: `web/src/audit-dev.test.ts` (168 lines) holds `auditStepAssertions(ci)`: three text assertions over the workflow (production step name plus its run line as one exact string; the dev step's run line by regex `\n {8}run: node scripts\/audit-dev\.mjs\n`; the old plain-audit line must be absent) and an `it.each` of eight mutated copies of the run lines, each of which must throw. The workflow's two audit steps are at `.github/workflows/ci.yml` lines 387-388 and 392-393, in job `web-build` (lines 369-447; job `web` is a different job at line 524). The five survivors the gate found: N1 and N2 (`continue-on-error: true` after the production or dev run line), N3 and N4 (`if: false`), N6 (dev step name changed; N5, the production name, is already pinned).

Two styles (both test-only, both inside `web/src/audit-dev.test.ts`; `ci.yml` is read, never edited):
- Style A (text block): slice each step's block from its exact `      - name: <name>\n` line to the next `\n      - ` or `\n      #` and assert it is exactly the name line plus the run line, then pin the dev step's name. Stays in the file's present idiom (strings, `it.each` over mutated copies). A harmless extra comment inside a block would turn it red.
- Style B (structure): parse `ci.yml` with `yaml` and assert that in job `web-build` the two steps found by their run values deep-equal `{ name, run }` only (so any added key, `continue-on-error`, `if`, `timeout-minutes`, `env`, is red, and N6 is red through the name). `yaml` 2.9.1 is already in `web/package.json` devDependencies (line 47) and resolved in `web/package-lock.json` (`node_modules/yaml`, version 2.9.1; positive control: `node_modules/vitest` matches 1); no lock change, no new dependency. The test file does not import `yaml` today (0 matches in a 168-line file whose imports I read).
- My recommendation: B. It states the intent (the step is exactly a name and a command) and is not defeated by comment or whitespace edits; the cost is a stricter test that also refuses a future legitimate `timeout-minutes` on those steps, which is a decision for Tuesday. Not measured: whether either style turns N1-N4 and N6 red (the builder proves it; I ran nothing).
Done when: N1, N2, N3, N4, N6 each shown red in an in-memory mutated copy; the eight run-line rows and the real-file premise row unchanged; N5 still red. Sonnet, tier 2. Intersection: no open PR on HPSM-POC; the path is in no other lane.

## 4. Not startable, listed as CARD candidates (word-blocked or ruling-blocked, one question each)

| Item | Why not a lane | The one question |
|---|---|---|
| RD-844 real fix | section 2 | May the open-site banner guard measure setup.html and status.html with the Font Awesome stylesheet answered by an empty stand-in? |
| RD-850, -851, -852, -854 | each adds test cells, so each edits `scripts/verify-expected-counts.json`; open PR #67 also edits it, is stale since 7 Oct and is now `dirty` | Close PR #67 (or merge it after conflict repair) so these four can start? |
| RD-876 | the ticket says the owner decides the ceiling of the default risk template | What ceiling should the default risk template carry (a number or no ceiling)? |
| RD-847 | "decide the canonical lock base ... switch every seat at one moment"; the tool is in use | Switch the lock tool's base at one moment, and when? |
| RD-815 | `deploy-demo.yml` runs on every push to main, so landing it can deploy the demo | May a workflow change that redeploys the demo on its own merge land, and in what window? |
| MPSCALC-290 | the open part is the `openapi.json:218` sentence; narrowing it is a new word | Approve the narrowed sentence (text to be supplied)? |
| MPSCALC-169 | adds a field beside `lineMarkupsOverlayVersion` with new openapi and API text | Approve the new field and its contract words? |
| MPSCALC-288 | "decide whether the canApprove queue should still list such a quote" | Should the approval queue still list such a quote, yes or no? |
| MPSCALC-332, -330 | -332: choice between ruling the vanished-file wording acceptable and saying it once; -330 needs a product minimum for the colour-pages threshold | -332: is the vanished-file wording acceptable as written? (-330 is a second question, queue it) |
| PCOMP-42, -44 | new governance values and enum, contract bump; need migration 0028, after PR #89 lands (it holds 0026 and 0027) | Approve the new governance value wording ("after validation", "controlled/staged") for -42? (-44 follows) |

Also not lanes, with the reason (no card needed): PCOMP-22 (Opus; its file `DEPLOY.md` is in PR #89, so wait for #89), PCOMP-23 (the footer line budget probably lives in `packages/renderers/src/document-pdf.ts`, which draft PR #85 edits; `change-report.ts` imports `renderDocumentPdf` from it; program: `document-pdf.ts` vs #85 = 1 overlap, `change-report.ts` and its test vs #85 = 0, so it stays out until the builder proves the fix needs only `change-report.ts`), PCOMP-12 (a UI behaviour change in `apps/web/src/screens/Discovery.tsx`; I read only the ticket head and cannot rule out a new label, so it is held), HPSMPOC-322 (branch b467 has no PR; conditional, could need a new approved sentence), HPSMPOC-343 (a ticket comment, a Jira write for a records seat), RD-827 ("Tuesday's call"; shared worktree installs), MPSCALC-332/-330 above. B593-2, -3, -9, -10 and PCOMP-17/-14 are now in PRs #88 and #89.

## 5. Lanes that can START NOW (5 firm, 2 on a word) and the intersection

One seat, one worktree, one branch per lane. Load rule stays: one waiter, load1 < 7. Ranked in the product owner's order: HPSM-POC, MPS, Composer, NexusAI.

| # | Lane | Tickets | Model / gate | YOURS (may edit) | NOT YOURS |
|---|---|---|---|---|---|
| 1 | HPSM-POC H-CI | HPSMPOC-314 | Sonnet / 2 | `.github/workflows/ci.yml` (the `api-sqlserver-shard` job: lines 163-350, filters at 250 and 253; premise check first: the ticket says limit 20, main says `timeout-minutes: 30` at line 168 since HPSMPOC-308; if no rebalance is measurable from run data, record that and stop) | every `web/**`, every `api/**` |
| 2 | MPS M-A2 | MPSCALC-325 | Sonnet / 1 | `src/MpsCalc.Api/Quotes/PurchaseValidation.cs` (pattern `MaxNullEntriesListed = 20` at line 22 and `errors.Count < MaxNullEntriesListed` at line 70), `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (the four walks), NEW `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs` (stop if a sentence must say "first 20") | everything in PR #110 (`ReferenceDocumentValidator.cs`, `QuoteRefusalOrder.cs`, `QuoteRefusalOrderGuard.cs`, `SourceLifecycleTests.GovernedNull.cs`), `docs/**`, `web/**`, `src/MpsCalc.Api/Feedback/**` |
| 3 | MPS M-WEB | MPSCALC-334, -329 (reword) | Sonnet / 2 | `web/src/api/stub/stubApi.ts` (conditional), NEW `web/src/api/stub/stubApi.test.ts`, `web/scripts/check-bundle.mjs`, `web/e2e/bom.spec.ts`, `tests/MpsCalc.Engine.Tests/ReconciliationContractRemainder.cs` | `src/**`, `tests/MpsCalc.Api.Tests/**`, `web/src/feedback/**`, `docs/**` |
| 4 | Composer C-TEST | PCOMP-62, -63 | Sonnet / 2 | `apps/web/src/screens/b116-s10-verify-dom.test.tsx`, `packages/engine/test/s47-crf2-linear-detector.test.ts` (comment only) | `apps/web/package.json` and `package-lock.json` (PR #86), `apps/api/**` (#88), `packages/db/**`, `DEPLOY.md` (#89), all 26 `packages/engine` and `packages/renderers` paths of draft #85 |
| 5 | NexusAI N-CI | RD-814 | Sonnet / 1 | `.github/workflows/build.yml`, `.github/workflows/deploy.yml`, `.github/workflows/npm-audit.yml` | `backend/server.js` and the two erasure tests (PR #110), `scripts/verify-expected-counts.json` and `backend/validators.js` (PR #67), `tests/e2e/**` |
| 6 | HPSM-POC H-AUDIT (on word) | HPSMPOC-348 | Sonnet / 2 | `web/src/audit-dev.test.ts` | `.github/workflows/ci.yml` (read-only; lane 1 edits it, so lanes 1 and 6 never share it as an edit path), `web/package.json`, `web/package-lock.json` |
| 7 | MPS M-FEEDBACK (reserve) | MPSCALC-176 | Sonnet / 2 | `src/MpsCalc.Api/Feedback/**`, `web/src/feedback/**`, `tests/MpsCalc.Api.Tests/Feedback*`, `web/e2e/b47-feedback.spec.ts`, `web/e2e/b83-feedback-attachments.spec.ts`, `docs/API.md`, `docs/api/openapi.json`, `web/src/api/generated/**` | everything in lanes 2 and 3 and PR #110. Approved words: the 46-row register `1_Project_Definition/Registers/2026-10-24_mps-176-feedback-triage-approved-words.md` exists (10,541 bytes; listed, not opened) |
| (cand.) | NexusAI N-GUARD | RD-844 | Sonnet / 2 | `tests/e2e/open-access-banner-guard.js`, `__tests__/rd490-open-access-banner-browser.test.js` | not startable until the section 2 question is answered; in the program below |

### Intersection by program (script `inter.py` in the scratchpad; exact path or `**` / `*` prefix match, both directions)

Inputs: the lane path lists above (7 lanes plus the N-GUARD candidate = 8 sets, NEW file names included) against the open PR file lists read from GitHub and against each other.

| Check | Result |
|---|---|
| Lane x open PR | 11 pairs (MPS 3 lanes x #110; Composer 1 lane x #89, #88, #86, #85; NexusAI 2 lanes x #110, #67; HPSM-POC has no open PR, so 0 pairs by construction, control: its closed list is non-empty, #210 to #212), 0 overlaps |
| Lane x lane | 28 pairs, 0 overlaps |
| Path existence | every non-NEW path exists on main (0 missing); globs match 6, 20, 7 and 3 existing files (MPS Feedback source, `web/src/feedback`, `Feedback*` tests, `web/src/api/generated`); NEW names (`QuoteWalkCaps.cs`, `stubApi.test.ts`) are absent from main (0 matches) |
| Held and excluded sets against PRs | RD-850..854 paths vs #67: 1 overlap (`scripts/verify-expected-counts.json`), the reason they are held; PCOMP-22 `DEPLOY.md` vs #89: 1 overlap; PCOMP-23 `document-pdf.ts` vs #85: 1 overlap, `change-report.ts` and its test vs #85: 0 |

Controls that could have been non-zero, same script, same run: planted same-path (`stubApi.ts` vs itself) 1; planted glob (`src/MpsCalc.Api/Feedback/**` vs `FeedbackStore.cs`) 1; planted lane-vs-lane (M-WEB vs M-WEB plus M-A2) 5; planted `apps/api/src/app.ts` against PR #88's real list (3 files) 1; planted `DEPLOY.md` against #89's real list 1; planted `ReferenceDocumentValidator.cs` against MPS #110's real list 1; planted `scripts/verify-expected-counts.json` against #67 1; planted `backend/server.js` against NexusAI #110 1; planted `document-pdf.ts` against #85 1; planted glob `packages/renderers/**` against #85 14; planted glob `web/src/**` against H-AUDIT 1. Limits: NEW file names are my proposals (a builder who picks others must stay in the same directory); PR #85 and #86 were compared by file name; PRs #88, #89 and NexusAI #110 are moving (builders live), so each lane must re-read the three file lists at launch; lane 4 carries a semantic risk only the builder can see (a comment-only edit is safe, a code edit in `packages/engine/test` is outside it).

## 6. Record-seat candidates added since 01:20 (not lanes)

- HPSM-POC: HPSMPOC-344 (property half), -347 and -349 met by PR #212 (squash `09641a91`); -344's other half was met by #210 earlier. Records seat moves them.
- NexusAI: RD-862 and RD-873 ride PR #110; RD-844 stays open (its real fix is section 2).
- PR #110's title and body still say RD-844 is fixed by the `domcontentloaded` wait; that change was reverted at 05:40 AEDT. The builder must correct the body before the gate reads it (read at source: title unchanged).
- Composer: B593-2 and B593-3 ride #88; B593-9, B593-10, PCOMP-17 and PCOMP-14 ride #89 (migrations 0026 and 0027).
- HPSM-POC: CodeQL alert #13 wants a ticket if Tuesday wants it fixed in code (section 7); never dismissed by a builder.

## 7. FEEDBACK CHECK (window opened at 21:00 AEDT 24 Oct = 10:00Z)

BLUF: new human feedback since 21:00 AEDT: NO. Client-human response in Jira or GitHub: NO. New ticket by a non-seat account: NO. Items found: 1 bot comment (CodeQL on a merged PR, the same one the 01:20 file reported; nothing new since 01:20). Mail and the NexusAI app store: NOT MEASURED.

| Store | Query | Result | Control that could have been non-zero |
|---|---|---|---|
| NexusAI (RD Jira) | created / updated since 21:00; comment GET on each updated ticket | 0 created; 9 updated (RD-881, -877, -871, -866, -865, -864, -860, -825, -818), 9 comments since 10:00Z, all author `616503`; since 01:20: 0 | `created >= "2026-10-21 00:00"` returned 6 |
| Security Composer (PCOMP Jira) | same | 0 created, 0 updated | the same filter returned 94 |
| MPS Calculator (MPSCALC Jira) | same | 4 created (-331..-334, seat), 18 updated, 14 comments, all `616503`; since 01:20: 0 | filter returned 19 |
| HPSM-POC (HPSMPOC Jira) | same | 3 created (-347..-349, seat), 12 updated, 9 comments, all `616503`; since 01:20: 0 | filter returned 45 |
| Vision Sales Portal feedback (VSP Jira) | `project = VSP AND ( created >= ... )` / `updated` | 0 created, 0 updated; total 89 (read through the paginated search) | `created >= "2026-09-01 00:00"` returned 25 |
| HPSM Policy Composer feedback (HPSM Jira) | same | 0 created, 0 updated; total 41 | no positive control for the window; the total equals the 41 of earlier sweeps |
| GitHub issue comments | `issues/comments?since=2026-10-24T10:00:00Z` | 0 on HPSM-POC, MPS, Composer, NexusAI, Vision Portal and QuickQuote (6 repos) | `since=2026-10-01` on QuickQuote returned 3 |
| GitHub review comments | `pulls/comments?since=...` | HPSM-POC 1 (`github-advanced-security[bot]`, 2026-10-24T11:44:21Z, PR #211, path `web/src/e2e-runner.liveApiRun.test.ts`); the other five 0 | the call returned the bot row |
| GitHub items touched | `issues?state=all&since=...` | HPSM-POC #210 to #212, MPS #107, #109, #110, Composer #87 to #89, NexusAI #106, #108 (dependabot), #109, #110: all by the seat account or a bot; Vision Portal and QuickQuote 0 | |
| Code scanning behind the bot comment | `code-scanning/alerts/13`; `alerts?state=open&ref=refs/heads/main` on HPSM-POC | alert #13 rule js/file-system-race, ref `refs/pull/211/head`, created 11:44:18Z, `dismissed_at` null, `fixed_at` null (the `state` field came back null, so I cannot read it directly); main has 0 open alerts | an open list returned numbers on NexusAI (238, 237, 236) and Vision Portal (31, 30, 29), so the call fires |
| Ticket for the alert | `project = HPSMPOC AND ( text ~ "file-system-race" )`, `( text ~ "liveApiRun" )` | only HPSMPOC-328 (Done) and -345 (Done): both Done, so no OPEN ticket names it: NOT a duplicate of an open ticket | `text ~ "code-scanning"` returned 48 rows; a nonsense token returned 0 |

Per item, new since 21:00 AEDT:
1. CodeQL alert #13 comment on merged HPSM-POC PR #211. Source: GitHub review comment (bot). Duplicate of an existing ticket: no open one (only the two Done tickets that touched that file). Already in the 01:20 file, so not new since 01:20.
No other item. Not human signals: every Jira and GitHub row is the shared seat account (`616503`, the seat's GitHub account) or a bot; that account cannot separate the product owner from a seat, same caveat as the earlier files.

## FOUND

1. The RD-844 `domcontentloaded` idea cannot work alone: the builder of PR #110 measured that a never-answering stylesheet still fails at about 46 s (the guard's own 45 s limit), and reverted it. Only the route/stub option fixes the ticket, and that option changes what the guard measures on two pages (section 2).
2. PR #110's title and body still claim RD-844 is fixed after the revert commit.
3. NexusAI main moved to `19b7106b` (PR #108 merged): `package.json` and `package-lock.json` are free of open PRs. PR #67 is now conflicted (`dirty`), which strengthens the case for closing it so RD-850..854 can start.
4. HPSMPOC-348's two audit steps are in job `web-build`, not job `web`. `yaml` 2.9.1 is already a resolved dev dependency of `web/`, so style B needs no lock change.
5. PCOMP-23 looked like a lane at 01:20 but its footer code probably sits in `document-pdf.ts`, which draft #85 edits. It is held.
6. HPSMPOC-314 still carries the stale "limit 20" (30 since HPSMPOC-308; main line 168).
7. The MPS test file in PR #110 is named `SourceLifecycleTests.GovernedNull.cs`; the 01:20 file's proposed name was different.

## UNMEASURED (said plainly)

- Mail (coordinator inbox and shared inbox): not read; the fences forbid mail tools. The feedback BLUF is Jira and GitHub only.
- The NexusAI in-app feedback store (`settings.json` on the Azure file share): needs the Azure credentials and the sweep script; no `az` call was made. The inventory's other stores (Vision Portal Postgres, QuickQuote table) need credentials or a production host and were not read; their GitHub repos and Jira projects were.
- HPSM Policy Composer's GitHub repo: not read (the project's `gh` is not logged in, same as earlier sweeps). The HPSM window query has no positive control.
- Whether main's CodeQL analysis has run on `09641a91` (main has 0 open alerts on HPSM-POC; alert #13's `state` field returned null) and whether NexusAI alerts #95 to #99 and #116 are still open.
- Whether the lock tool and the three workflow files in RD-814 need an `id-token` permission: I read the ticket, not the workflow bodies.
- Whether PR #110's body will be corrected, and whether PRs #88, #89 and NexusAI #110 move again: they were read at 05:4x AEDT; the builders were live.
- Code bodies: I read ticket text, a few code anchors (the guard's lines 72, 259-276, 284-294; `PurchaseValidation.cs` lines 22 and 70; `ci.yml` lines 163-253, 369-393; `audit-dev.test.ts` whole), not the code of each lane. Style A and style B for HPSMPOC-348 were reasoned, not run.
- The RD-844 stand-in: I did not run the guard, so "the banner does not use the icon font" is a grep over the banner's css and js (0 matches against a positive control on the html pages), not a measurement of the rendered page with and without the stylesheet.
- PCOMP-12, -62, -63: read the ticket head and anchors only; PCOMP-62's flake was measured by a gate seat, not re-run.
- RD board beyond the 01:20 lists: the 760 open RD tickets were not re-triaged; only the tickets named here were read, so a startable RD ticket outside this list may exist.
- Not touched on purpose: myPKI, CypherKey, Lead_Bot, any hosted or production host, `az`, docker, the decision queue, the staged-briefs folder, any coordinator ledger, any non-Datasec client, any git write, any Jira or GitHub write.
