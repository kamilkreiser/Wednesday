# SWEEP-1110: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-24 late morning)

Commissioned by Tuesday (s321), Sonnet, routing row C8, read-only. Form and old state: `2026-11-23_SWEEP-0610_datasec-actionable-lanes.md` (every lane re-checked below against the boards and GitHub as they are now). Scope: Jira RD (NexusAI), MPSCALC, PCOMP. **HPSM-POC and OXPd were not swept, counted, read or listed.** Fences kept: Jira GET only (credentials read by name in-process, never printed), `gh api -X GET` under each project's own `GH_CONFIG_DIR`, no write except this file and `fleet/state/s321/sweep/`, no `cd`, nothing deleted, no message to any human. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s321/sweep/` (GET-only scripts copied from s314 and read before use; dumps `RD_open.tsv`, `MPSCALC_open.tsv`, `PCOMP_open.tsv`, three `*_done.tsv`, `rd_tables.md`).

## BLUF

| project | open now (predicate; every page read to the end) | agent-actionable now (predicate below) | lanes |
|---|---|---|---|
| MPS Calculator (MPSCALC) | **166** (`project = MPSCALC AND ( statusCategory != Done )`, 2 pages, unique 166; all Backlog). Unchanged: same key set, 0 status or `updated` changes | **0** | none (427 and 431 stay "built, records only"; 272 conditional on words) |
| Security Composer (PCOMP) | **76** (`project = PCOMP AND ( statusCategory != Done )`, 1 page, unique 76; all Backlog). Was 77: PCOMP-37 and PCOMP-67 Done, PCOMP-130 new | **1: PCOMP-130** (test-only; its ticket says "Not ruled: whether and when to do it", so Tuesday's default applies, as for PCOMP-67) | 1 (C-T2). PCOMP-66 stays HELD (pickup line 288) |
| NexusAI (RD) | **901** (`project = RD AND ( statusCategory != Done )`, 10 pages, unique 901): To Do 370, Testing 315, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 | **79 To Do keys**: the 78 still-open carried keys plus **RD-1034 (new)**. RD-1030, RD-1032 are Testing; RD-1031 is built (PR 246); RD-1033 Testing; RD-1035 excluded | 7 (NX-S1 new shape, NX-W, NX-S2, NX-B, NX-F1, NX-F2, NX-T, NX-X; one NexusAI seat at a time, jest lock) |

**Actionable predicate:** the ticket needs no new word from Kam or a client human, no ruling, no production touch, no deploy, no money, no external message, is not already built (comments or merged PR), and no HELD or DROPPED line in the pickup names it. The 78 carried RD keys keep their 11-11 deep read and 11-22 landing screen (the `updated` stamp of every one is unchanged since the 11-23 sweep); only RD-1021, RD-1026, RD-1034 and PCOMP-130 were read whole today.

Census controls: `board_count.sh` was not rerun; each project's open plus Done dump was read to the end (RD 901 + 130 = 1031 keys, MPSCALC 166 + 267 = 433, PCOMP 76 + 54 = 130), each with `rows` = `unique`. Key diff against the 11-23 dumps (`comm`): RD gone 0, new RD-1033 (Testing), RD-1034 and RD-1035 (To Do), so 898 + 3 = 901; To Do 370 + 2 new - 2 moved to Testing (RD-1030, RD-1032) = 370; Testing 312 + 2 moved + 1 new = 315. MPSCALC gone 0, new 0. PCOMP gone PCOMP-37, PCOMP-67 (both Done), new PCOMP-130; PCOMP-36's `updated` changed (2026-11-23T06:27, the records comment for #131).

Origin mains at sweep time (`gh api -X GET .../commits/main`; `pulls?state=open` returned **0 open PRs** in all three repos): NexusAI `d96a83d3` (merge of #246, 2026-11-23T14:06Z); MPS `56f508a7` (#228, unchanged); Composer `8b9ab200` (#132, 2026-11-22T20:08Z). Every file claim below is from origin main.

Standing facts that bind: MPS seats push a branch only, Friday/Tuesday opens the PR (CodeQL rule, MPS CLAUDE.md line 51), nothing deploys without a card; Composer: no deploy of a changed content release (pickup top block), the demo is Kam's; NexusAI: nothing deploys (C-224 demo hold), `npm run verify`, one jest lock holder at a time; model rule 2026-11-21: Opus default, Fable only when flagged. HPSM hold to 2026-12-10 respected.

## RANKED LANES (value and size; the first two close in about 2 hours for one build seat)

| rank | lane | keys | size | why this rank | gate |
|---|---|---|---|---|---|
| 1 | **NX-S1** (viewer-reachable dialling plus the stale permission comments) | RD-1021 with RD-1034 bundled | M, about 2 h (RD-1034 is comment-only, XS) | The pickup's named next NexusAI build after RD-1031 ("NexusAI: RD-1031 then RD-1021 (SWEEP-0610)"; RD-1031 has landed). Security class, measured by the ticket's review at the wire. RD-1034 edits the same two files RD-1021 must touch (`backend/services/capabilities.js` about text line 96 and the row at 156; the RD-1011 test header), so one seat. PR 242 body states "the rows of RD-1021 and RD-1022 stay under config.read": the row move is exactly this lane's. Re-verified at main: `GET /api/setup/data-sources` at `backend/server.js:17163`, `GET /api/debug/data-sources` at 18393, `capabilities.js:96` still reads "administrator-only reads: audit, incidents, retention, state, users, provisioning" | G1, Opus builder |
| 2 | **C-T2** (Composer test plants) | PCOMP-130 | XS, about 1 h | Different repo, so no jest-lock contention and runs in parallel with rank 1. Test-only: one file, `packages/content/test/b330-sm316-qgate.test.ts` (patterns at line 88 `(True\|False)` plant `False`, line 97 `(png\|svg\|jpg)` plant `png`; the `morePlants` argument PR 132 added is at lines 25, 31, 37 and used at 208 to 214). Fix shape and regression (three mutants must turn red, 10 of 10 tests and same names) are in the ticket. Not compiled into the product, touches no content release file | G2, Sonnet builder; branch only, PR by Tuesday, no deploy. Tuesday's default (as for PCOMP-67) is yes |
| 3 | **NX-W** (chat status line escape) | RD-1026 | S, about 1 to 1.5 h | A real XSS shape, re-verified at main: `static/js/index.js` line 3523 assigns `${label}` (built from `args.pattern`, `args.userName`, `args.printerName`, `args.department`, lines 3517 to 3521) to `statusDiv.innerHTML`; the page's `escapeHtml` is at line 113. One file plus one new test. Runs after rank 1 (one NexusAI seat). The ticket's sibling rows (3466, 3478 and others) are NOT in scope | G2 (G1 if the builder widens past the label) |
| 4 | **NX-S2** (server bundle) | RD-1017, 577, 893, 896, 974, 975 | S each, one file `backend/server.js` | Unchanged from 11-23 minus RD-1021 (now rank 1). Control re-run at main: 2 reads of `AUDIT_ACTIONS.SETTINGS_CHANGE` at lines 17363 and 17613 and 0 definitions (RD-1017 real). Must follow rank 1 (same file, `server.js`) | G2 |
| 5 | NX-B, NX-F1, NX-F2, NX-T, NX-X | the carried keys (`rd_tables.md` and tables below) | per the 11-22 sizes | Not re-sized. NX-F2 caution: PR 244 (main now) edited `static/css/index-styles.css`, `static/css/dark-mode.css`, `static/css/tokens.css`, `scripts/derive-brand-tokens.js`; a builder of RD-164, 222, 261, 351 re-reads those CSS lines at `d96a83d3` first. PR 246 edited `tests/e2e/dark-mode-contrast.spec.js` and `light-baselines.json` (NX-F2b is done) | per lane |
| 6 | **M-R** (MPS review tiles) | MPSCALC-272 | M | Conditional: tile words are customer-visible, so Tuesday's call per lane (standing default: yes, nothing deployed, words on the deploy card). Not counted | G2 |

Disjointness by directory: NX-S1 owns `backend/server.js` (the two routes only) plus `backend/services/capabilities.js` plus the rd1011 and rd929 test files; NX-W owns `static/js/index.js` and one new test; C-T2 owns one file under `packages/content/test/` in another repository. NX-S2 shares `backend/server.js` with NX-S1 and so runs after it (same repo, one seat in any case). The three share no path with each other except that sequencing.

---

## 1. MPS Commercial Calculator (MPSCALC)

Open 166, all Backlog; Done 267 (unchanged); no PR merged since #228; 0 open PRs; no ticket created after MPSCALC-433; no `updated` stamp changed since the 11-23 dump (stamp comparison of all 166 keys). So the 11-23 conclusion stands: **0 agent-actionable builds.**

- **Built, records only:** MPSCALC-427 (#228) and MPSCALC-431 (#226): moving them is Tuesday's reading, as in 11-23 Q1.
- **Conditional (not counted): MPSCALC-272** (M-R, review summary tiles; `web/src/screens/Lifecycle.tsx` and new `web/src/screens/review/**`): words pending, Tuesday's call. Pickup: 3 hits for MPSCALC-272, none a HELD or DROPPED line (whole-file grep, positive control RD-1011: 19 hits).
- **Excluded (carried unchanged, stamps unchanged):** 195, 316 remainder, 360, 419, 421, 424, 425, 395 and 372, 278, 283, 274; seed epics 1 to 15, question-for-Kam tasks 69 to 85, `needs-ruling` tickets (129, 144, 153, 157, 159, 177, 188, 222, 226, 261, 316) and the roughly 48 built-and-open tickets. Not re-read for text today: their stamps are unchanged.

## 2. Security Composer (PCOMP)

Open 76 (all Backlog); Done 54. Changes since 11-23: **PCOMP-67 Done** (PR 132, squash 8b9ab200, "plants every alternative of its middle pattern"); **PCOMP-37 Done**; **PCOMP-130 new** (row #496, filed by B2007); PCOMP-36's comment (2026-11-23T06:27, records for #131, "Recorded; not moved": 4 of 34 typed fields carry a value, 14 wait on a reading of the template). Main `8b9ab200`; 0 open PRs. **Binding top block:** main carries a NEW content release; no Composer deploy ships it; it does not stop test-only or data-only builds; cutting the release, rebuilding the examples and any new customer word remain Kam's.

| key | scope (the ticket's own text) | files (read at main 8b9ab200) | size | state |
|---|---|---|---|---|
| **PCOMP-130 (actionable, lane C-T2)** | In `packages/content/test/b330-sm316-qgate.test.ts` two patterns keep one plant for an alternation, `(True\|False)` (plant False, line 88) and `(png\|svg\|jpg)` (plant png, line 97), so dropping True, svg or jpg leaves the file green. Fix: use the `morePlants` argument with one extra plant per unplanted alternative; regression: each of the three mutants turns the plant check red, the unmutated file stays 10 of 10 tests with the same names. Test-only, no customer artefact, no content release file | that one file | XS | Pickup: 3 hits, all the records lines (B2007, "new PCOMP-130 Task, row #496"); no HELD or DROPPED line. Dropping svg and jpg "not re-run for this ticket" per the ticket; the builder measures |

**Excluded or not counted:** PCOMP-66 (engine edit in `packages/engine/src/secrets.ts`, G1) is HELD by the pickup (line 288: "PCOMP-66 HELD (Tuesday's call, sweep Q3 default)"; 1 hit); PCOMP-36 stays open (14 fields wait on a reading of the template: a judgement, not a build); PCOMP-44 (ruled hold), the reviewer-round hold (19, 20, 31 to 35, 38, 39, 92 and behind them 42, 45 to 51, 53 to 61), the Guided hold (68, 69, 72, 75, 84 to 88, 90), the owner's seven calls (9, 70, 71, 73, 76, 91, 123), words (79, 89, 11, 128, 129), deploy and ops (2, 10, 13, 16, 18, 25, 28, 78, 93), epics and ratification (1 to 8, 94, 46). Carried from 11-23: key sets otherwise identical and `updated` stamps unchanged for all other keys.

## 3. NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

Open 901: To Do 370, Testing 315, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 901). Main `d96a83d3`. **Merged since the 11-23 sweep (main 3c3be156):** #242 (RD-1030: `backend/services/capabilities.js`, two test files, `scripts/verify-expected-counts.json`), #243 (two audit-flush test readers, RD-1033), #244 (RD-1032 toner fills: CSS files, `derive-brand-tokens.js`, BRAND.md, two tests), #245 (records), #246 (RD-1031: `tests/e2e/dark-mode-contrast.spec.js`, `light-baselines.json`). No PR is open. The only `updated` stamps that changed on previously-open keys are RD-1030 and RD-1032 (both now Testing); the other carried keys are untouched.

### New or changed since 11-23

| key | verdict | note |
|---|---|---|
| RD-1030 | Testing (landed, #242) | not work |
| RD-1031 | **built, records only** | still To Do on the board; PR 246 landed on main d96a83d3 (branch `b2013/rd1031-contrast-suite-upkeep`); pickup (a5 after DELTA 1387) lists "NexusAI records pass (RD-1031 comment + Testing)" as owed |
| RD-1032 | Testing (landed, #244) | not work |
| RD-1033 | Testing (landed, #243, after-the-fact ticket) | not work |
| **RD-1034** | **ACTIONABLE (bundled into NX-S1)** | Two comments stale after RD-1030: the `admin.read` about text at `backend/services/capabilities.js:96` does not name the two data-source reads (verified at main); `__tests__/rd1011-four-routes-administrator-only.test.js` lines 9 and 10 call all four routes a default (true now only of the two test routes); and the table file header's route count (205 against 203). Comment-only; the ticket says "in the next change to either file", which NX-S1 is. Pickup: 1 hit, a records line, no HOLD |
| RD-1035 | **EXCLUDED (needs the product owner)** | forced-colours rendering of the Fleet Health toner bars; the ticket says how the bar looks in that mode is "a design choice for the product owner"; 0 pickup hits (control RD-1011: 19) |

### Re-screen of the 78 carried keys

All 78 are still To Do (program check against the s314 lane map: 78 To Do; the other 2 of the 80 are RD-175 and RD-349, Testing). RD-1021 and RD-1026 re-read whole and verified true at main today (above). Controls re-run at `d96a83d3`: 2 reads and 0 definitions of `AUDIT_ACTIONS.SETTINGS_CHANGE` in `backend/server.js` (22,813 lines); `GET /api/setup/data-sources` at 17163 and `GET /api/debug/data-sources` at 18393. Pickup check (whole-file counts, control RD-1011: 19): RD-1021 9, RD-1026 3, RD-1030 9, RD-1031 14, RD-1033 3, RD-1034 1, RD-1035 0; RD-893 1; RD-1017, 577, 896, 974, 975 0. **No HELD or DROPPED line names RD-1021, RD-1026, RD-1034 or any NX-S key**; the only holds are the C-224 demo hold (no deploy) and one NexusAI lane at a time.

### Lanes (directory partition)

NX-S1 (RD-1021 plus RD-1034) and NX-W (RD-1026) are the new shapes; NX-P and NX-F2b are done. NX-S2, NX-B, NX-F1, NX-F2, NX-T, NX-X are the 11-22 lanes (owned-file lists in `2026-11-22_SWEEP-1450_datasec-actionable-lanes.md`, "Lanes", "Cross-lane exceptions", "Sizes and gates"), with two edits: RD-1026 moves from NX-F2 to NX-W; RD-1021 and RD-1034 form NX-S1. Cross-lane exceptions carried: RD-396 also edits `backend/services/riskAlertScheduler.js`; RD-515 edits F1's `first-run-setup.html` from F2's banner-guard tests (after F1); RD-1016 before RD-1014 (`settings.js`); RD-145, 745, 397, 918 need the Dockerfile (NX-T); NX-X (RD-1014, RD-1015) runs alone and last. `scripts/verify-expected-counts.json` is regenerated by Tuesday at each landing (#242, #244 changed it).

### Actionable keys by lane (status and `updated` from the board at this sweep; 79 keys: 78 below plus RD-1034)

**NX-S** (7 keys)

| key | type | status | updated | title (150) |
|---|---|---|---|---|
| RD-974 | Bug | To Do | 2026-11-07 | The automatic insights check for unusual print times gives a job with no Job_Start_Time the current time, so undated jobs count as off-hours when it r |
| RD-975 | Bug | To Do | 2026-11-07 | The business-hours report reads created_at before the job's own start time, so a seeded row is judged by when the store was seeded and not by when it  |
| RD-893 | Task | To Do | 2026-10-27 | PUT /api/risk-conditions/:id leaves its other fields unchecked (condition_text, is_active and email_recipients accept any type) and stores risk_level  |
| RD-896 | Task | To Do | 2026-10-27 | Risk conditions stored with a mixed-case risk_level before PR #131 stay out of the High, Medium and Low lists and the alert mailer until saved again:  |
| RD-577 | Bug | To Do | 2026-11-11 | Key Vault status reporting reads KEY_VAULT_NAME but the template sets KEYVAULT_NAME (server.js:631, :642, :17733) — every Marketplace deploy shows 'no |
| RD-1017 | Bug | To Do | 2026-11-20 | AUDIT_ACTIONS.SETTINGS_CHANGE is used at backend/server.js lines 17353 and 17600 (add and remove a data source) and defined nowhere, so those two audi |
| RD-1021 | Bug | To Do | 2026-11-20 | Two sibling routes still let a signed-in viewer make the server use stored data-source sign-in details: GET /api/setup/data-sources tests every enable |

**NX-B** (9 keys)

| key | type | status | updated | title (150) |
|---|---|---|---|---|
| RD-455 | Bug | To Do | 2026-09-15 | SCIM provisioning: saving a group-mapping change without generating a new bearer token is refused (400 INVALID_SCIM_TOKEN), so every mapping edit rota |
| RD-744 | Bug | To Do | 2026-10-05 | RD-685 C-F1: after a hard-link refusal, a changed or deleted inode on our name lets the LIVE re-drive certify 'purged' while the outside name keeps th |
| RD-745 | Bug | To Do | 2026-10-06 | RD-685 C-F2/C-F3: a non-normalised DATA_DIR (trailing slash or ./data) makes two of our own names refuse each other forever; inside() and lstat mutant |
| RD-750 | Bug | To Do | 2026-10-05 | RD-684 B-P1: one erasure ledger record lists the re-created feedback.json in BOTH filesPurged and filesFailed |
| RD-824 | Task | To Do | 2026-10-06 | RD-640 L-A5: a store/copy link failing EACCES, EPERM or ENOTDIR keeps the erasure purged_incomplete forever; should ENOTDIR (a path through a file) jo |
| RD-728 | Bug | To Do | 2026-09-29 | RD-628 G2 false-red when MACHINE_ID or WEBSITE_SITE_NAME is set in the runner env: scrub them; and 'read through this module only' is imprecise (batch |
| RD-759 | Task | To Do | 2026-11-12 | CSP intake: userinfo still kept for a leading U+00A0/U+2028/U+FEFF, an @ only as %40, and data: with @ (gate 12 f1 unit shapes, after RD-735 round 2) |
| RD-578 | Bug | To Do | 2026-11-11 | AzureADManager reads KEY_VAULT_NAME (never set) so its Key Vault init always throws on Marketplace deploys — correcting the name changes AUTH behaviou |
| RD-1023 | Task | To Do | 2026-11-20 | The SCIM router writes two audit entries with the router-relative path, scim_rate_limited and scim_auth_failed (scimProvisioning.js lines 120 and 156) |

**NX-F1** (11 keys)

| key | type | status | updated | title (150) |
|---|---|---|---|---|
| RD-117 | Bug | To Do | 2026-11-16 | first-run-setup applies a CSP-blocked inline style — error on every load of the page a fresh customer deployment lands on |
| RD-188 | Bug | To Do | 2026-11-16 | The first-run wizard violates the product's own CSP ~20 times per session — a style the product itself sets is refused by style-src-attr 'none' (P9-07 |
| RD-176 | Bug | To Do | 2026-09-02 | Provisioning mode cards paint their ground from JS inline styles, so the dark fix has to win by !important — move them to the state classes the compon |
| RD-416 | Bug | To Do | 2026-09-14 | First-run polish: opening User Access throws a page error (first-run-setup.js:3517), the page overflows 49px at 390px width, and configuration refusal |
| RD-151 | Story | To Do | 2026-09-01 | Cost settings errors are shown as a page banner and the server's actionable `details` is discarded — render inline beside the offending field (P3-08) |
| RD-371 | Bug | To Do | 2026-09-12 | RD-148 round-1 residuals F-4/F-5/F-6: revoke UI shows an unlabelled local-time date, has no live region and loses focus, and double-POSTs for a non-ad |
| RD-373 | Bug | To Do | 2026-09-07 | N-3 + N-5: the still-live revoke warning is partly covered by the Feedback widget, and the revoke handler has two silent-return paths |
| RD-540 | Task | To Do | 2026-09-18 | The PRECONDITION cell in rd465-first-run-open-window.test.js passes with the entire page script emptied - it asserts the fixture's own preset 'active' |
| RD-687 | Bug | To Do | 2026-09-26 | First-run's danger status branches are unreachable: no caller passes 'error' to the data-source badge, and the component-check and final-validation el |
| RD-396 | Bug | To Do | 2026-09-12 | RD-150 residue (gate F-2, F-3): red_flag_enabled stored as '' or 0 renders the Settings toggle OFF (settings.js:937) while the risk-alert scheduler st |
| RD-1016 | Task | To Do | 2026-11-20 | static/js/settings.js defines escapeHtml twice (lines 93 and 2440) and the page uses the second, which returns an array or an object unescaped, so the |

**NX-F2** (15 keys)

| key | type | status | updated | title (150) |
|---|---|---|---|---|
| RD-144 | Bug | To Do | 2026-09-01 | Dashboard tab strip has no tablist/tab/tabpanel semantics — WCAG 4.1.2 (SUS-10, pre-existing) |
| RD-351 | Bug | To Do | 2026-09-06 | .tab-button has no project focus style — the UA default focus ring is now blue on a blue-adjacent ground after RD-251 (pre-existing, surfaced by the g |
| RD-164 | Bug | To Do | 2026-09-02 | Dark mode's neutral card border #3a3a5a on #1e1e3f is 1.47:1 — below the 3:1 that the tinted variants in the same stylesheet are held to (WCAG 1.4.11, |
| RD-222 | Bug | To Do | 2026-09-02 | The wizard's ACTIVE step-number chip is white on a translucent-white composite at 3.74:1 in LIGHT, on all five tabs — measured and marked failing in p |
| RD-220 | Bug | To Do | 2026-09-07 | P11-07: console errors on every dashboard load, four families — three /api/normalized/* 503s, an empty high-risk query, CSP style-src-attr violations, |
| RD-259 | Bug | To Do | 2026-09-07 | index.html reports 9 console errors on load (index-offline.html 1) — logged by QA pass 13b and deliberately not chased |
| RD-261 | Bug | To Do | 2026-09-03 | brand-buttons.css is a single point of failure for the brand — if it fails to load, all 42 .btn-primary on 10 pages render Bootstrap #0d6efd permanent |
| RD-483 | Task | To Do | 2026-09-17 | The open-access banner sits 24px (admin.html) and 32px (legal.html) below the top of the page instead of at the very top |
| RD-613 | Task | To Do | 2026-09-22 | The storage-wiped alarm banner renders only on the dashboard: Settings, admin pages and first-run setup never fetch /api/status/persistence (S59 findi |
| RD-832 | Task | To Do | 2026-10-07 | admin.html logs two '403 (Forbidden)' resource loads in open mode on a fresh install; the URLs were not captured |
| RD-512 | Task | To Do | 2026-09-17 | RD-490 banner guard does not check the dark theme: the open-site banner's visibility and ink are measured in the default (light) theme only |
| RD-513 | Task | To Do | 2026-09-17 | RD-490 banner guard measures one viewport (1366x900): phone-width concealment of the open-site banner is unguarded |
| RD-515 | Task | To Do | 2026-09-17 | RD-490 banner guard does not cover the inline first-run open-site note (.nx-open-access-banner--inline) on the User Access step |
| RD-1026 | Bug | To Do | 2026-11-20 | The chat page writes the tool-call status label (static/js/index.js line 3523) into the page as HTML and an AI endpoint can fill it: the review ran a  |
| RD-145 | Bug | To Do | 2026-09-01 | All vendor CSS/JS loads from cdn.jsdelivr.net — in an egress-filtered tenant every icon disappears again (SUS-17, pre-existing) |

**NX-T** (34 keys)

| key | type | status | updated | title (150) |
|---|---|---|---|---|
| RD-134 | Task | To Do | 2026-08-27 | All 12 schedulers had zero test coverage because requiring any scheduler under jest crashes at load (node-cron -> ESM-only uuid) — the blocker is now  |
| RD-249 | Bug | To Do | 2026-09-03 | qa-surface-up.sh races itself on node_modules when two surfaces are stood at the SAME head — the second npm ci deletes the first's install and exits 5 |
| RD-320 | Bug | To Do | 2026-09-05 | The erasure write-guard's corpus and runtime patch set are both vocabularies: three of four corpus members cannot fail its clauses, and nine fs routes |
| RD-345 | Bug | To Do | 2026-09-06 | RD-340 residues from the round-3 gate: F21 the header + limits block still specify the round-2 reader, F22 default-import and .then wiring unseen, F23 |
| RD-348 | Bug | To Do | 2026-09-06 | CI's gate depends on python3 and nothing declares it — RD-339's wrapper drives tests/test_normaliser.py through execFileSync('python3'), relying on ub |
| RD-352 | Bug | To Do | 2026-09-06 | RD-341 QA-F4: four callee shapes yield neither a row nor a verdict - the label guard's docstring promises it FAILS LOUDLY on what it cannot read, and  |
| RD-355 | Bug | To Do | 2026-09-06 | RD-341 QA-R2-F1: the label guard's second declared limit is over-general - it says an object-literal KEY write is skipped, but only { onSource: x } is |
| RD-353 | Bug | To Do | 2026-09-15 | The launcher's Jira banner reports the PAGE CAP as a count: in-progress reads 100 where the true figure is 165, because jira_count pipes `jira issue l |
| RD-378 | Bug | To Do | 2026-09-08 | The F-2 census's write detector follows a const/let declarator but not an assignment, a computed member, or an object-held alias of writeFileSync |
| RD-379 | Bug | To Do | 2026-09-08 | The scheduler-vocabulary test's env restore is justified by a cross-file leak risk that jest's per-file process.env isolation makes impossible — and t |
| RD-384 | Bug | To Do | 2026-09-08 | RD-376 gate findings F-1..F-5, all RECORD-LEVEL: the 'exactly two ways' reconciliation claim is five, entra-provisioning-ui passes against a reader th |
| RD-387 | Bug | To Do | 2026-09-14 | RD-293 gate residue: the new seed warning has no guard, near-miss SEED_DEMO_DATA values are still silent, and two concurrent boots double-seed |
| RD-394 | Bug | To Do | 2026-09-12 | RD-382 residue (gate F-1..F-4): JIRA.md's normalised recipes fail from the project root; the JIRA_SITE normaliser mishandles uppercase schemes, //, wh |
| RD-397 | Bug | To Do | 2026-09-12 | RD-327 residue (gate N-1, P-1): build-commit-sha.sh calls a tree clean with plain git status --porcelain, so it stamps HEAD under showUntrackedFiles=n |
| RD-426 | Bug | To Do | 2026-09-14 | Three suites fail under heavy machine load and pass alone: setup-rate-limit-allowance, erasure-health-branches and rate-limit-allowance failed 6 cells |
| RD-539 | Task | To Do | 2026-09-18 | The RD-490 round-1 mutation harness cannot be reused as-is: 5 of its 15 anchors no longer exist against the round-2 guard, so a stale anchor edits not |
| RD-566 | Task | To Do | 2026-09-19 | RD-561 gate residue (B-1..B-3): 'no env opt-out' has no cell; guard refuses -w2/--max-workers=2/--runInBand=true and accepts empty --maxWorkers=; JIRA |
| RD-572 | Bug | To Do | 2026-09-19 | RD-568 residue: auth-gate-fail-closed leaks a legacy machine-id into the shared worker HOME; gate Lows A-1 (cell claims more than it checks) and A-2 ( |
| RD-580 | Bug | To Do | 2026-09-20 | RD-342's gitleaks preflight has never run: the launcher reads preflight-gitleaks.sh from the stale 2_Project_Files clone (cd2b543), where it is absent |
| RD-586 | Bug | To Do | 2026-09-21 | jira-query.sh --count returns a real-looking 0 (exit 0) for a status NAME that does not exist -- Jira's /search/jql answers HTTP 200 {} for an unresol |
| RD-595 | Task | To Do | 2026-09-21 | rd523 and rd545 now require an RFC1918 interface on the test host and bind stand-ins on its real LAN address — deliberate for RD-516's trusted-stored  |
| RD-597 | Task | To Do | 2026-09-21 | NEW-1's guard 3 cannot distinguish a connection refusal from an accept-then-reset: the openai SDK reports both as 'Connection error.', so the cell's t |
| RD-599 | Bug | To Do | 2026-09-21 | RD-518 r3 H-01: the ANONYMOUS cell in rd518-r3-health-detail-decision measures a 401, not a redaction, and nothing now drives the open-window anonymou |
| RD-600 | Bug | To Do | 2026-09-21 | RD-518 r3 H-02: the precondition cell reads roles via /api/auth/check, which bypasses the middleware, so it stays green with NO req.user — only the ad |
| RD-623 | Task | To Do | 2026-09-22 | RD-524 gate-3 polish F-A3/F-A4/F-A6: READY overstated 'every M1 red behavioural', no cell for the feedback-attachments directory as evidence, 'Open Se |
| RD-668 | Task | To Do | 2026-11-03 | Under jest the Key Vault SDK cannot load ('@azure/keyvault-keys not installed (Unexpected token export)'), so any suite reaching EncryptionService.ini |
| RD-726 | Bug | To Do | 2026-09-28 | RD-696 cell 5 reds with EINVAL on a long TMPDIR (socket path over 104 bytes), and the 250 ms exit delay is unguarded: short socket base + an M-B2-shap |
| RD-757 | Bug | To Do | 2026-10-27 | RD-591 g3: a FOREIGN connect-write-close dial reads 'vanished' and is COUNTED in a positive-arrival cell (rd549 O4/C2/C10 go green on a foreign dialer |
| RD-829 | Task | To Do | 2026-10-07 | Gate 14 findings for RD-430 + RD-694 item 4: the manifest _about's '147 occurrences' total is false on today's tree (144), the READY named the wrong f |
| RD-918 | Task | To Do | 2026-11-03 | RD-913 follow-up: sqlite3 6 arrives through an install script that npm 11.19 warns about on every install, and docker/Dockerfile.backend still builds  |
| RD-810 | Task | To Do | 2026-11-17 | CodeQL baseline (test code, medium): js/file-access-to-http in tests/uat-run.js:30 - a file-read value is sent in the UAT runner's request |
| RD-1018 | Task | To Do | 2026-11-20 | The committed cells for RD-445 mock the token library, so a weakened verification (the audience option dropped from the verify call, a widened flag te |
| RD-1024 | Task | To Do | 2026-11-20 | RD-1011 and RD-1012 residue: no committed cell counts the stored-source read for a refused caller, none tests a role that is neither viewer nor admin, |
| RD-1027 | Task | To Do | 2026-11-20 | RD-1008 residue: no committed cell turns red when only one of the five route-side class checks is reverted, none asserts the fallback answer on the PO |

**NX-X** (2 keys)

| key | type | status | updated | title (150) |
|---|---|---|---|---|
| RD-1014 | Bug | To Do | 2026-11-20 | Values from outside are still written into the page as HTML or into quote-unsafe attributes after RD-861: scan file names, print-log user names and pr |
| RD-1015 | Task | To Do | 2026-11-20 | RD-835 residue: four CSV writers still write numeric cells (sheets, pages, size) without the helper, a leading space or look-alike before an equals si |

**NX-S1 / NX-W additions (in the lists above or new):** RD-1021 (in NX-S above, moves to NX-S1), RD-1034 (new, NX-S1), RD-1026 (in NX-F2 above, moves to NX-W).

### NexusAI: conditional (not counted; carried unchanged, none moved)

RD-1019, RD-1022 (a viewer's reach to five more connecting routes; PR 242 states its rows stay under `config.read`), RD-1020, RD-1029, RD-763, RD-764, RD-1006, 1009, 1010.

### NexusAI: excluded (with the reason)

- **Landed on main, records only (11 To Do keys carried from 11-23, plus RD-1031):** RD-538, 563, 969, 729, 826, 970, 731 (partly), 972, 929, 977, 978; and **RD-1031 (PR 246)**.
- **Held or needs a ruling or Kam:** RD-805, 768, 1025, 1028, 433, 610, 612, 622, 644, 522, 884, 546, 193, 583, 584, 305, 313.
- **Product owner or a customer-facing word:** RD-1035 (new), RD-702, 636, 1029, and the roles-UI chain RD-937 to 957 (`roles-ui-2026-11`).
- **Not agent work:** epics RD-6, 7, 8; business and compliance RD-13, 20, 21, 22, 28, 29, 30, 31, 34; Azure and secrets RD-50, 54, 55, 83; Jira and session tooling RD-233, 287, 449; marketplace items; feature requests RD-146, 400, 401, 842. RD-1004 (dated work, 2026-12-18) and RD-1001 (launcher-side).
- **In Progress (8), Put on Hold (7), Declined (2):** counts only. **Testing 315 and Release Ready 199:** not work.
- **Other To Do keys (about 280, the `operations` residue and QA-gate findings):** not re-read; UNMEASURED beyond titles and stamps.

## 4. Questions for Tuesday (each with a default)

1. **PCOMP-130:** "Not ruled: whether and when to do it" is the ticket's own line. Default: build it (same class as PCOMP-67, which you took), branch only, no deploy.
2. **RD-1034 rides with RD-1021** in NX-S1. Default: yes, one seat, G1 Opus.
3. **RD-1035 (forced-colours bars):** a design choice for the product owner; Tuesday's call whether it earns a card at all. Default: no card now.
4. **PCOMP-66 stays HELD**, **PCOMP-36 stays open**, **MPSCALC-427 and 431** reading: unchanged from 11-23 Q1 to Q3. **MPSCALC-272:** default yes per lane, tile words ride the deploy card.
5. **Records owed that this sweep saw but did not touch:** NexusAI records pass (RD-1031 comment and Testing; B2015 follow-ups); the carried landed-but-To Do keys.

## 5. How measured, and NOT tested

- Instruments: GET-only paginated Jira `search/jql` (page size 100, `jqdump.py` to `isLast`), `jdesc.py` and `lastc.py` for ticket text and last comments, `gh api -X GET` for mains, open and closed PR lists, PR file lists and bodies, and file reads at main through `rg.sh`; `comm`, `join` over the dumps. Positive controls: RD-1011 in the pickup (19 hits), the two `SETTINGS_CHANGE` reads, `statusDiv.innerHTML` at line 3523, the `morePlants` lines.
- **Not tested:** (a) the 164 unmoved MPS, 75 other Composer and about 280 NexusAI To Do tickets were not re-read for text, only for key list and `updated` stamps; classes are carried; (b) of the 79 RD actionable keys only RD-1021, RD-1026 and RD-1034 were read whole today; (c) PCOMP-130's mutants were not run; (d) no CI or CodeQL state was read for #242 to #246 (the pickup records Build, CodeQL, Gitleaks, npm-audit success on d96a83d3); (e) sizes are estimates for the kit drafter to confirm; (f) I did not read the board comments of RD-1031 to see whether the records pass already ran (the board still shows To Do and a stamp of 2026-11-23T04:14); (g) `NEXT-PICKUP-TUESDAY.md` DELTA 1394 to 1363 were read by targeted greps and the top-of-file blocks, not line by line.
- Disclosures: no write outside this file and the scratch folder; no Jira or GitHub write; no token printed; no deletion.

READ-WHOLE-BY-TUESDAY: ____
