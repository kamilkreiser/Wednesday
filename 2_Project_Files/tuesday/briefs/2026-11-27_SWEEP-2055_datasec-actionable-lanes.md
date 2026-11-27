# SWEEP-2055: Datasec tickets agents can work now, in lanes (read-only sweep, Fri 27 Nov 2026 evening)

Commissioned by Tuesday s335 from `2026-11-27_SWEEP-2055_COMMISSION.md`; `DRAFTER_RULES.md` read whole first; form and baseline `2026-11-26_SWEEP-0446_datasec-actionable-lanes.md` (read whole; every row it lists was re-checked, not copied). Written by one in-session sweep agent, first instrument call Fri 27 Nov 2026 20:53:01 AEDT, last `date` print 20:59:22 AEDT. **HPSM-POC was not read, counted or listed (Kam's hold to the end of 2026-12-10); myPKI, CypherKey, Lead_Bot skipped; OXPd not swept (planned separately).** Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/sweep2055/` (`RD.tsv`, `MPSCALC.tsv`, `PCOMP.tsv` fresh dumps, `rd_tickets.txt`, `rd_paths.txt`, `rd_tree.txt`, `prior_rd.txt`, `card_*.txt`).

## BLUF

| project | open (instrument + predicate) | actionable now | lanes |
|---|---|---|---|
| NexusAI (RD) | **916** (was 911): To Do 369, Testing 331, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 916) | **65 To Do keys** (4 + 4 + 25 + 32); 5 of them new today (RD-1046 to RD-1050); RD-455 and RD-981 already have a drafted, unstamped kit | 4: L1 server, L2 backend periphery, L3 static front end, L4 tests/scripts/CI. **All four need the jest lock at verify** (see section 1.5) |
| MPS Calculator (MPSCALC) | **165** (was 166), all Backlog | **0** | 0. All six of yesterday's keys left the actionable set: 233, 316, 120, 135, 297 landed on main (#229, #230) and wait on the product owner's reading; 195 is Done |
| Security Composer (PCOMP) | **74** (was 75), all Backlog | **0** | 0. PCOMP-23 landed (#134, 3222c898) and is Done; nothing else is buildable (reviewer-round hold, Guided hold, words, content-release chain) |

Counts: `bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/board_count.sh jira <site> <email> <token> '<jql>'` (token sourced transiently in a subshell, never printed), every JQL `project = <KEY> AND ( statusCategory != Done )`; each printed `TOTAL=n (limit was 5001, so this is a real count and not a cap)`; the dump `jq.py dump` (GET, every page) has the same row count (916, 165, 74). RD per-status counts by board_count.sh with `status = "<name>"` each returning non-zero (369, 331, 199, 8, 7, 2 = 916), so no zero rests on an unresolved status name.

Main shas (`gh api -X GET repos/<org>/<repo>/commits`, each under the project's own `GH_CONFIG_DIR`): NexusAI `d2aeecf8` (was e789995a; 34 commits, PRs 261 to 268), MPS `c295071b` (was 56f508a7; #229, #230), Composer `3222c898` (was d06508f8; #134). Open pull requests: 0 in all three. NEXT-PICKUP DELTA 1548 names no NexusAI, MPS or Composer seat live (jest and lock state UNMEASURED: no lock folder was read).

**Top three by value across the three projects:** (1) NexusAI L2, RD-455 (SCIM mapping edit forces a new bearer token and breaks Entra's job) with RD-981: kit B2139 is drafted (STARTABLE, UNSTAMPED), needs only its stamp naming BASE `d2aeecf8`. (2) NexusAI L3, RD-1014 (Medium: 165 unescaped HTML or `data-arg` writes in three scripts) then RD-1038 (a contrast failure that keeps the e2e contrast suite red). (3) NexusAI L1, RD-1010 (30 body-read handlers that 500 on a body no parser read) with RD-1048 and RD-1050.

What changed since yesterday's sweep, by program (`comm` of the key lists and of the Jira `updated` stamps): MPS gone 195, new none; PCOMP gone PCOMP-23, new none, no `updated` stamp changed; RD gone none, new RD-1046, RD-1047, RD-1048, RD-1049, RD-1050; RD To Do left for Testing: RD-1023, RD-1043, RD-1044, RD-1045, RD-983. Only 6 RD stamps changed (RD-1009, 1023, 1043, 759, 893, 983: all from yesterday's actionable set), so yesterday's 290 excluded NexusAI keys have no Jira change since; the 34 main commits cite only RD-1009, 1015, 1016, 1023, 1043, 1044, 1045, 744, 745, 750, 759, 824, 893 (program `grep -o RD-[0-9]+` over the compare), so no excluded key was fixed by a landing.

Reading of "actionable": no new word of Kam's, no ruling, no client human, no production touch, no device run, no money, no external message, not already built or landed, no HELD or DROPPED line in the pickup or the 11-26 and 11-27 notes. `NEXT-PICKUP-TUESDAY.md`, `daily_tuesday/2026-11-26.md` and `2026-11-27.md` were concatenated and every remaining key counted by word-boundary scan: keys with 0 hits (the carried lane 3 and 4 keys) have no held or dropped line; the keys with hits (RD-455, 728, 820, 981, 1010, 1014, 1038, 1046 to 1050) had every hit read (section 1.6).

---

## 1. NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

### 1.1 Census and frame
- JQL `project = RD AND ( statusCategory != Done )`: **916**. To Do 369, Testing 331, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2. Testing and Release Ready are not work: counted, not read.
- Origin main `d2aeecf8cda67265cc316646953c45d92b861f77` (`gh api -X GET commits`; tree read by `git/trees/<sha>?recursive=1`, `truncated` false, 1085 blobs; every file path below was tested for existence in that tree by program, `paths.py`, control: a known path matches, `__tests__/rd1045-boot-folders-are-persistent.test.js`). The local `2_Project_Files` checkout is stale (HEAD cd2b543, shown by `git log -1`), so nothing was read from it.
- Authority (NexusAI `CLAUDE.md`, as read by yesterday's sweep and not re-read): Tuesday may authorise merges and ticket moves; production, money, external comms, irreversible need Kam; C-224 demo-deploy hold stands (card `nexusai-demo-deploy-c224-1123` ruled a, read with `decision_queue.sh show`): **no deploy from any lane below.**
- Description plus newest comments of all 70 candidate keys (the 65 below, plus RD-728, 810, 353, 580, 539) were read by program today (`rd_tickets.txt`, first 520 characters of the description and the newest comments), the five new tickets in full, and every file path in every description and in the newest five comments was tested against the tree (`rd_paths.txt`). A key that was NOT read beyond that opening is marked "carried" only where its ticket text had no file path and its stamp is older than 2026-11-17.

### 1.2 Landed since yesterday (excluded: built, on main; the board still reads To Do for these and a records pass owns the move)
RD-893 and RD-1009 (PR 263), RD-759 (PR 265, with RD-1023 now Testing), RD-744, 745, 750, 824 (PR 267), RD-1016 and RD-1015 part (1) (PR 268), RD-1043, 1044, 1045 (PR 261, now Testing). RD-1015 parts (2) and (3) need a real spreadsheet and a choice about changing export bytes (section 4, W3). Records still owed: the PR 267 pass (kit B2151, seat R340) and the PR 268 pass (B2150's FOR-RECORDS names the comments and the one new Low ticket to file: a CSV number cell holding a comma, a quote or a line break), per DELTA 1537 item (3). A records seat is agent work but holds the Jira write, `CLARIFICATIONS.md` and `HISTORY.md` alone: not counted in the lanes.

### 1.3 Actionable (To Do, buildable now). Sizes: S under 1.5 h, M 1.5 to 4 h, L more. J = needs the jest lock.

#### L1, server (owns `backend/server.js`, `backend/services/scimProvisioning.js`, one NEW test file per key; J)
| key | title (short) | why actionable | size | files (read at `d2aeecf8`) |
|---|---|---|---|---|
| RD-1010 | 30 body-read handlers answer a body no parser read with a 500 | list is in the ticket; census over HTTP first, then early check keeping each field-read line byte-identical; the 400-versus-403 order is taken from each route's own answer and recorded (the decision queue `prior` check on this subject: 0 matches, control: the RD-1038 subject returned 3) | M | `backend/server.js` (many regions, ticket lists the lines) + census script/cells |
| RD-820 | `validateConditionWithAI`'s own AI-off gate has no cell | extract the function with injected deps, add a cell and a mutant; leave the Azure/Ollama body alone | M | `backend/server.js` (:5926 and :6969 as ticketed, line numbers unmeasured today) + one new backend module + 1 test |
| RD-1048 | PUT `/api/risk-conditions/:id` keeps the old `kql_query` when the text changes | new today; fix shape: clear `kql_query` when `condition_text` differs (proposal in the ticket; the regenerate-in-PUT alternative is the coordinator's default choice, not Kam's); `prior` 0 matches | S | `backend/server.js` (PUT, ticket cites 21397; readers 5141, 21544, 21613) + 1 test |
| RD-1050 | a refused SCIM token with a body the JSON parser refuses writes no audit row | new today; ticket cites mount at `server.js:22444-22446` and limiter at `scimProvisioning.js:128`, comment 142-149; fix shape: token check before the parser, or an error handler writing the same thin row; `prior` 0 | S | `backend/server.js` (22444-22446), `backend/services/scimProvisioning.js` + 1 test with the real mount |

Order: RD-1010 (census first), RD-1050, RD-1048, RD-820. Opus-class review for RD-1010. RD-416 part (3) (HTTP 502 to 4xx for a refused configuration) would land here but names no code: UNMEASURED which 4xx; it is left out of L1 (section 1.5 exclusions).

#### L2, backend periphery (owns `backend/services/entraProvisioning.js`, `backend/routes/entraProvisioning.js`, `backend/simpleDb.js`, `backend/services/cspReport.js`, `__tests__/rd759-796-csp-intake-edges-and-typed-fields.test.js`, `backend/seedDemoData.js`; J)
| key | title (short) | why actionable | size | files |
|---|---|---|---|---|
| RD-455 | SCIM: saving a mapping edit without a new token is refused (400 INVALID_SCIM_TOKEN) | real bug, measured twice; **kit B2139 (seat N182) drafted and STARTABLE, UNSTAMPED, its REFUSE 4(b) now satisfied** (kit 2 landed in PR 267: main contains it; the stamp must name BASE `d2aeecf8`) | M | `backend/services/entraProvisioning.js`, `backend/routes/entraProvisioning.js` + a NEW test file |
| RD-981 | `setQuickQuestions` late INSERT after ROLLBACK | same kit B2139: sequential INSERTs; the production-caller question is answered by the drafter (only tests call the simpleDb method; text search only) | S-M | `backend/simpleDb.js` + a NEW test file |
| RD-1049 | CSP intake: a `data:` authority-form address keeps an at-sign; two wordings owed | new today; the product owner's 2026-11-11 ruling on RD-759 (refuse `data:` with an at-sign) is the authority; fix shape: move the refusal above the host branch (the review's mutant turned no cell red, so a new cell is needed); `prior` 0 | S | `backend/services/cspReport.js` (96-99 as ticketed, comment 97-98), the rd759 test header lines 10-11, 18 |
| RD-387 | RD-293 gate residue: seed warning has no guard, near-miss `SEED_DEMO_DATA` values silent, two boots double-seed | carried, files from ticket text, existence verified; **may touch the seed call site in `server.js`, which L1 owns: sequence after L1 or take the call site out** (UNMEASURED which file holds the warning) | M | `backend/seedDemoData.js`, `__tests__/rd293-seed-runs-on-local-boot-path.test.js` |

Order: RD-455+RD-981 (the kit), RD-1049, RD-387. **RD-728 is EXCLUDED** (the drafter measured: its two targets do not exist at main; they live on the unmerged RD-628 branch, RD-628 being in Testing).

#### L3, static front end (owns `static/**` (html, js, css), `tests/e2e/**`, and `backend/services/riskAlertScheduler.js` for RD-396 only; J + a real browser for the first-run and contrast keys)
| key | title (short) | size | files (ticket text, existence verified) |
|---|---|---|---|
| RD-1038 | High Risk label 3.96 / 4.46 to 1 dark, 3.82 light; the contrast suite asks 4.5 | S | `static/css/index-styles.css` (:1310 as read 11-26), `static/css/dark-mode.css`, the contrast baselines. Colour choice: prior rulings exist (`nexusai-rd160-brand-chrome-contrast` darker `#00719f` on text-bearing chrome; `nexusai-brand-chrome-dark-token` leave; `nexusai-rd180-badge-label-colour` A label everything `#000000`): the seat applies them and records the token it picked |
| RD-1014 | outside values written as HTML or quote-unsafe `data-arg` (165 sites; PR 255 fixed ten) | L | `static/js/index.js`, `first-run-setup.js`, `settings.js`; **kit 2 of this lane per DELTA 1537; builds on RD-1016's single `escapeHtml` (landed)**; shares `index.js` with RD-1015's landed hunk |
| RD-117, RD-188, RD-220 | first-run and dashboard console CSP-refused inline styles (three tickets, one class) | M (three, one measure-first kit) | `static/js/first-run-setup.js`, `static/first-run-setup.html`, `static/js/index.js`; first step is one real-browser count of refused inline styles at main (named in RD-117 and RD-188's 2026-11-16 comment) |
| RD-259 | `index.html` reports 9 console errors on load, `index-offline.html` 1 | M | `static/index.html`, `static/index-offline.html`, `static/js/index.js` (with RD-220) |
| RD-144 | dashboard tab strip has no tablist/tab/tabpanel semantics (WCAG 4.1.2) | S-M | `static/index.html`, `static/js/index.js` (with RD-351) |
| RD-351 | `.tab-button` has no focus style | S | `static/css/index-styles.css` |
| RD-151 | cost settings errors shown as a banner; render the server's `details` beside the field | S-M | `static/settings.html`, `static/js/settings.js`, test `__tests__/settings-cost-form.test.js` (that test file is L4's: one cell added, coordinate) |
| RD-164 | dark-mode neutral card border 1.47:1 | S | `static/css/dark-mode.css` |
| RD-222 | wizard active step chip 3.74:1 in light | S | `static/css/first-run-setup-styles.css`, `dark-mode.css` |
| RD-176 | provisioning mode cards painted by inline styles | S-M | `static/js/entra-provisioning-ui.js`, `static/css/*` |
| RD-371, RD-373 | revoke UI date label, live region, double-POST; warning covered by the Feedback widget | S-M each | `static/js/entra-provisioning-ui.js` (one owner for both; RD-371's live-region half is on an unmerged branch `rd-372-r2-s57`: re-check at main) |
| RD-396 | `red_flag_enabled` `''`/0 shows OFF while the scheduler runs | S-M | `static/js/settings.js` (937), `backend/services/riskAlertScheduler.js` |
| RD-416 | first-run User Access page error (`first-run-setup.js:3517`), 49 px overflow at 390 px | S-M | `static/js/first-run-setup.js`, `static/css/first-run-setup-styles.css`; part (3) HTTP 502 to 4xx excluded |
| RD-261 | `brand-buttons.css` single point of failure; nothing asserts the fallback | S-M | `static/css/brand-buttons.css` + a cell |
| RD-483 | open-access banner 24/32 px below the top | S | `static/admin.html`, `static/legal.html` |
| RD-512, RD-513, RD-515 | banner guard: dark theme, phone width, inline first-run note | M (one guard file, one owner) | `tests/e2e/open-access-banner-guard.js`, `static/first-run-setup.html`; the guard's jest wrapper `__tests__/rd490-open-access-banner-browser.test.js` is L4's file: take it into L3 for these three and say so |
| RD-613 | storage-wiped alarm banner only on the dashboard | M | `static/js/*.js` pages + `static/settings.html`, admin pages |
| RD-687 | first-run danger status branches unreachable | S-M | `static/js/first-run-setup.js` |
| RD-832 | admin.html logs two 403s in open mode | S-M | `static/js/admin.js` (measure URLs first) |
| RD-145 | all vendor CSS/JS loads from `cdn.jsdelivr.net` | L, **last** | all `static/*.html` + new vendored files; `prior` 0; adds third-party files to the repo (licence line per file) |

Order: RD-1038, RD-1014 (kit 2), then the first-run class (RD-117, 188, 220, 259, 416, 687), then the dashboard items (RD-144, 351, 164, 222, 261, 483, 613, 832), then the revoke UI (371, 373, 176, 151, 396), the banner guard (512, 513, 515), RD-145 last. Carried and not re-read beyond the opening and newest comments: RD-144, 145, 164, 176, 222, 259, 261, 351, 483, 513, 515, 613, 687, 832.

#### L4, tests, scripts, CI, package (owns `scripts/**`, `.github/**`, `package.json`, `JIRA.md`, `__tests__/helpers/**` and every EXISTING `__tests__/*` file except the two named above for L2 and L3; J)
| key | title (short) | size | files |
|---|---|---|---|
| RD-1046 | `qa-surface-up.sh` first-boot block: retry after a partial first attempt skips the block with no sentinel; mktemp log never removed; unusable TMPDIR exits 1 not 13 | S-M | `scripts/qa-surface-up.sh` (243-258 as ticketed), `__tests__/rd1044-qa-surface-first-boot-block.test.js` (exists); new today, fix shapes are proposals in the ticket |
| RD-249 | `qa-surface-up.sh` races on `node_modules` (two surfaces, one head) | S | same script: **one owner with RD-1046, do RD-1046 first** |
| RD-1047 | 57 test files still call a tmpdir function; move to the persistent root and add a lint cell | L (mechanical, 57 files; heavy jest) | the 58 files the ticket lists, `__tests__/helpers/persistent-temp-root.js`, `__tests__/rd1045-boot-folders-are-persistent.test.js`; **runs LAST or alone: every existing test file in its list conflicts with any other lane's edit to it** (the list includes `rd893-risk-level-stored-lowercase` and `rd878-risk-condition-put-risk-level-type`: L1's cells go in NEW files only) |
| RD-134 | schedulers had zero test coverage (blocker solved, coverage not) | M | `__tests__/` new files for the 12 schedulers in `backend/services/schedulers/` (read only) |
| RD-320 | erasure write-guard corpus and runtime patch set are vocabularies | M | `__tests__/helpers/erasure-write-guard.js` + its tests |
| RD-345, 352, 355, 378, 379, 384 | label-guard and census residues from gates (test-only) | S each | `__tests__/helpers/import-graph.js`, `__tests__/sustainability-stand-in-labels.test.js`, `__tests__/auth-gate-fail-closed.test.js`, `__tests__/scheduler-failure-vocabulary.test.js`, `__tests__/entra-provisioning-ui.test.js` |
| RD-348 | CI depends on `python3` and nothing declares it | S | `.github/workflows/build.yml` (setup-python step or one declared line); hosted CI is the only proof of a workflow change |
| RD-394 | JIRA.md normalised recipes fail from the project root; `JIRA_SITE` normaliser gaps | S-M | `JIRA.md`, `scripts/lib/jira-site.sh`, `__tests__/rd382-jira-site-scheme.test.js`; the launcher half (`Launch_Claude.command`, outside the repo) is EXCLUDED |
| RD-586 | `jira-query.sh --count` returns 0 for an unresolvable status name | S | `scripts/jira-query.sh` (no test file exists for it today: a new cell or a shell check) |
| RD-397 | `build-commit-sha.sh` calls a tree clean with plain `git status` | S | `scripts/build-commit-sha.sh` |
| RD-426 | three suites fail under heavy load, pass alone | S-M | `__tests__/setup-rate-limit-allowance.test.js`, `erasure-health-branches.test.js`, `rate-limit-allowance.test.js` (measure first; not proven flaky) |
| RD-540 | PRECONDITION cell in the rd465 test passes with the page script emptied | S | `__tests__/rd465-first-run-open-window.test.js` |
| RD-566, RD-572 | verify-guard residue; `auth-gate-fail-closed` leaks a machine-id into the shared worker HOME | S each | `scripts/` guard, `JIRA.md`, `__tests__/auth-gate-fail-closed.test.js` (with RD-378) |
| RD-595, 597, 599, 600, 623 | test-hygiene Lows from RD-574, RD-518, RD-524 gates | S each | `__tests__/rd523-aoai-redirect-refused.test.js`, `rd545-ai-test-limit-survives-ai-off.test.js`, `ai-config-aoai-save.test.js`, `rd518-r3-health-detail-decision.test.js` (RD-623's F-A6 'Open Settings shown to viewers' is a `static` UI change: L3's, or left out) |
| RD-668 | Key Vault SDK cannot load under jest; suites silently use the machine-id fallback | M | jest config in `package.json`, test setup |
| RD-918 | sqlite3 6 install-script warning on every install: add the allow-list APPROVE entry (never deny; part (b) answered by PR 155) | S | `package.json` + lockfile, hosted audit job proves it; **same file as RD-668: one owner** |
| RD-726, 757, 829 | EINVAL on long TMPDIR; foreign dial counted in a positive cell; manifest `_about` total 147 vs 144 | S-M each | `__tests__/rd696-listen-failure-remedies.test.js`, `__tests__/rd591-cross-seat-isolation.test.js`, `scripts/verify-expected-counts.json` is Tuesday's (not touched) |
| RD-1018 | RD-445 cells mock the token library: add a cell with the real library against a loopback key set | M | `backend/marketplaceJwt.js` is READ only (mutant at line 90); new test file |
| RD-1024 | RD-1011/1012 residue: three cell gaps and a stale comment | S | `backend/services/accessAudit.js` (comment at line 48 only: no other lane owns it), tests |
| RD-1027 | RD-1008 residue: three cell gaps | S-M | `__tests__/rd1008-hostile-endpoint-chat-routes.test.js`, `rd1008-endpoint-error-code-is-not-trusted.test.js` |

Order: RD-1046 then RD-249 (script), RD-348, RD-394, RD-586, RD-397 (text and tooling: the only L4 keys whose own proof is not a jest cell), the test-only residues, RD-668 with RD-918, RD-134, RD-1047 last.

### 1.4 Lanes (at most 4, file-disjoint, by value), both sides
1. **L2 first** (a kit exists): owns the six files named above. **Must NOT touch** `backend/server.js`, `backend/services/scimProvisioning.js`, `static/**`, `scripts/**`, `.github/**`, `package.json`, any other existing test file.
2. **L1**: owns `backend/server.js` and `backend/services/scimProvisioning.js` (RD-1050 only). Must NOT touch `backend/services/entraProvisioning.js`, `backend/routes/entraProvisioning.js`, `backend/simpleDb.js`, `backend/services/cspReport.js`, `static/**`, `scripts/**`, existing test files (new files only).
3. **L3**: owns `static/**`, `tests/e2e/**`, `backend/services/riskAlertScheduler.js` (RD-396 only), and the one guard wrapper `__tests__/rd490-open-access-banner-browser.test.js`. Must NOT touch `backend/**` otherwise, `scripts/**`, `__tests__/helpers/**`, any other existing test file.
4. **L4**: as above. Must NOT touch `backend/**` except the comment line in `accessAudit.js`, `static/**`, `tests/e2e/**`, the rd759 test file and the rd490 guard wrapper.
Partition checked by name (not by a program over diffs): the only shared paths are (a) `backend/server.js` between L1 and RD-387 (L2), (b) `__tests__/settings-cost-form.test.js` between RD-151 (L3) and L4, (c) `package.json` and `scripts/verify-expected-counts.json` (the second regenerated by Tuesday at landing, never listed). New test files per key are additive.

### 1.5 Jest: serial or beside
- **Needs the jest lock (serial, one NexusAI seat at a time) until B2175's rd490 port-band fix lands:** every build above, in the order L2 (RD-455 + RD-981), L1, L3, L4 (RD-1047 last). Reason: each lane's own `npm run verify` is the whole jest suite; I found no key whose landing gate skips it.
- **May run beside the lock (no jest in the seat):** (a) kit DRAFTING for any lane (B2139 precedent: drafted and dry-read with no jest and no lock; its RUN is predicted, not measured); (b) the two NexusAI records passes owed (PR 267, PR 268) as one single-writer seat; (c) the read-first measurements named in L3's first step (a real-browser console count needs a browser, not jest: UNMEASURED whether a browser and jest may share the machine).
- **Lock state UNMEASURED:** no lock folder read; DELTA 1548 lists no NexusAI seat live.

### 1.6 Notes on the keys that had notes lines
- RD-455 and RD-981: DELTA 1520-1537 and B2139's report: lane 2 kit 3, UNSTAMPED, waits on the stamp with BASE `d2aeecf8`; drafter Q-3 (keep narrowed to an already-scim configuration) has a default (the narrowing); the decision store was NOT searched by the drafter (no exact card id), so I ran `prior` on the lane's subjects: see section 4.
- RD-728: drafter's measurement only; I did not re-run it (UNMEASURED today; the test path `__tests__/rd628-two-machine-id-derivations.test.js` is also absent from the tree I read: `/usr/bin/grep -c` of the tree file for `rd628-two-machine` printed 0; control `rd1045-boot` printed 1).
- RD-1010, RD-820: DELTA of 11-26 names them next in lane 1; RD-1014: DELTA 1537 names lane 3 kit 2 next; RD-1038: only a records line (11-25). No HELD or DROPPED line names any key in 1.3.

### 1.7 EXCLUDED (To Do 369 = 65 actionable + 9 landed + 5 new exclusions + 290 carried exclusions; assigned 369, missing 0, extra 0, by program)
- **Landed on main, records only (9):** RD-893, RD-1009, RD-744, RD-745, RD-750, RD-759, RD-824, RD-1015 (part 1; parts 2 and 3 need a real spreadsheet and a byte-change choice), RD-1016.
- **New exclusions today (5):** RD-728 (targets not on main), RD-810 (the product owner ruled 2026-11-17 to leave the alert open, recorded as intended, no code change), RD-353 and RD-580 (the launcher `Launch_Claude.command` is outside the repository and the coordinator's; RD-580's own text says not to fix the launcher), RD-539 (the harness `run-mut.py` lives in QA evidence, not in the repository).
- **Carried exclusions unchanged (290):** yesterday's classes by Jira stamps and commit scan above: needs a ruling or word (38: RD-193, 305, 313, 433, 522, 546, 578, 583, 584, 610, 612, 622, 636, 644, 702, 763, 764, 768, 805, 840, 858, 876, 884, 892, 896, 925, 927, 989, 997, 1006, 1019, 1020, 1022, 1025, 1028, 1029, 1041, 1042), dropped by Kam (RD-1035), diverged unmerged branch (RD-967), landed per the 11-25 sweep records only (22), Roles UI chain (30: RD-928 to RD-957, 966), not agent work (61), operations and gate-finding residue read by title only (132, UNMEASURED beyond title and label), needs-decision label (RD-368), brand palette residue (10, UNMEASURED), CodeQL baseline (RD-806). The full key lists are in section 6 of the 11-26 file; this sweep re-read none of them beyond the stamp comparison.
- Statuses that are not work: Testing 331, Release Ready 199, In Progress 8 (RD-49, 81, 427, 431, 432, 450, 643, 662 per yesterday: not re-read), Put on Hold 7, Declined 2.

---

## 2. MPS Commercial Calculator (Jira MPSCALC, repo `datasecau/MPS-Commercial-Calculator`)

### 2.1 Census
- `project = MPSCALC AND ( statusCategory != Done )`: **165** (board_count.sh `TOTAL=165`, dump 165 rows, all Backlog). Yesterday 166.
- Origin main `c295071b550133ef836710e7fc1865f6ea0c006b` (#230, merged 2026-11-26 10:30 AEDT by the comment's own record), after #229 `15bca4ec`. Open PRs 0. Local checkout stale (on `b03/api` as of yesterday; not read).

### 2.2 Yesterday's six actionable keys, re-read at today's main
- MPSCALC-233, 316, 120: landed by #229; MPSCALC-135, 297: landed by #230; MPSCALC-195: Done (its card `datasec-mps-195-engine-sentence-1126` ruled b, delivered, ticket moved). Newest comment of each of the five read today (records notes of 2026-11-26): each says the ticket **stays open for the product owner's or the coordinator's reading**, and names what is not built:
  - 233: a DERIVED reference (no body, blank reference) is not refused, so a source copied twice gives two copies with one reference; "a rule for that case (a counter or a refusal) is a product choice and no word of the product owner covers it". Create and draft edits do not refuse a clash either (outside the ruling's scope).
  - 316: two sibling messages still say "characters" for the same UTF-16 count (`QuoteEndpoints.cs` :1458 account manager and delivery site, at most 200; :1462 opportunity notes): "no accepted sentence"; whether the acceptance reaches the two schema places is not ruled.
  - 120: the version rule section is silent on which of 18 unbumped contract changes it covered: "the coordinator's to say, or a words question".
  - 135: whether a skip counts as green (clause 4) is the product owner's reading of his own wording.
  - 297: whether a hosted run at phone width is required is the coordinator's call under the Done rule.
  Each is a words or ruling item: not agent-buildable now.
- **Actionable now: 0.** Evidence: no ticket other than those five and 195 changed (`updated` stamp comparison against the 11-26 dump: 5 changed, all listed; no new key); the two landings cite only those keys (#229: 233, 316, 120; #230: 135, 297, commit subjects read); the only MPS HELD line I found in the three notes, by key scan (MPSCALC-233 7 hits, 135 12, 272 10, 360 3; the lines with 233, 135 and 272 read) is MPSCALC-272 (card `datasec-mps-mpscalc272-tiles-1124` ruled a, hold until MPSCALC-315's figures exist, read by `show`).

### 2.3 EXCLUDED (165 = 5 landed-awaiting-reading + 160 carried classes; assigned 165, missing 0, extra 0)
Carried unchanged from 11-26 (every stamp unchanged): epics 15 (1 to 15); spec-seed umbrellas 42; question-for-kam 10 (69, 74, 75, 76, 78, 79, 80, 82, 83, 85); needs-ruling label 10; later phase 5; held by Kam 1 (272); owner approval of exact words or design 18; lane-v words or client data 28 (the words pack, section 4 W5); built, open, records reading only 22; hosted, deploy, secret, device, external 7; blocked 2 (212, 360). The full key lists are in section 3 of the 11-26 file; the sum is 15 + 42 + 10 + 10 + 5 + 1 + 18 + 28 + 22 + 7 + 2 = 160, plus the five above = 165.

### 2.4 Lanes
None. Records-only (agent work, single writer, not a code lane): the five landed keys already carry their records notes (C-193, C-194).

### 2.5 UNMEASURED
Whether the stub and no-API smoke legs are still red is moot (#230's hosted run reads green/skipped per MPSCALC-135's note); the 160 carried exclusions were not re-read beyond stamps; local price-book counts (140, 200); the unlocated runbook (223).

---

## 3. Security Composer (Jira PCOMP, repo `datasecau/Datasec-Security-Composer`)

### 3.1 Census
- `project = PCOMP AND ( statusCategory != Done )`: **74** (board_count.sh `TOTAL=74`, dump 74 rows, all Backlog). Yesterday 75; gone: PCOMP-23 (Done); new: none; no `updated` stamp changed.
- Origin main `3222c898` (#134 "Policy document footer: hold the first line to what fits above the hash line", merged 2026-11-25T23:31Z). PR 85 merged 2026-11-20. Open PRs 0. Content releases: the two `CONTENT_HASH` files were NOT re-read today; yesterday's values (`release-demo` 5db37614, `release-draft` 5679855b) stand as read by yesterday's sweep, and #134's commit subject names no content path (UNMEASURED by blob read today). **Kam's hold (pickup): no deploy of a changed content release without his own card; DRAFTER_RULES line 99 binds.**

### 3.2 Actionable now: 0
- PCOMP-23 (yesterday's only key): built by #134 (gate B2117, `FOR-RECORDS.md` read), board Done. Remaining notes from that gate are not tickets: the DOCX footer clipped (F1), page label wrapping over three lines (F2), clipping by code point (F5), other brand fonts unmeasured (F6): "candidates for a later pass only if wanted", no ticket exists, and filing one is a Jira write this sweep does not make.
- Everything else was excluded yesterday for reasons that have not changed (no stamp moved, no Composer commit but #134): epics 4 (PCOMP-1 to 4); held label 19; needs-kam 2 (46, 94); needs ruling or words 6 (11, 36, 65, 123, 128, 129); held by comment or by Tuesday 2 (66, 75); reviewer-round hold, content release, L1-L9 chain 22; device, SM tool, deploy, VM, environment, ops, guide 15; built, records only 4 (12, 41, 52, 64). Sum 4 + 19 + 2 + 6 + 2 + 22 + 15 + 4 = 74 (assigned 74, missing 0, extra 0). The full key lists are in section 4 of the 11-26 file.
- Any ticket whose only end is a deploy or whose work changes the content release (the L1-L9 chain, PCOMP-8 rebuild of examples, customer words) is EXCLUDED on Kam's hold; none was reopened.

### 3.3 Lanes
None. UNMEASURED: per-branch compare of the origin branches; reproduction of any open defect on main.

---

## 4. WAITING-ON-KAM (each with its question and the card that carries it)

Cards are read only where I could name an exact id from the three notes I read; the full open-card list is not read (`decision_queue.sh list` is forbidden here), so "no card found" means none named in those three files.

| id | question | card |
|---|---|---|
| W1 NexusAI RD-1041 (`/api/setup/status` answers every signed-in role the workspace, tenant and client ids) | Which roles may read which fields of that route: refuse the roles the permission table excludes (as the 11-25 card did for the data-sources routes), or something narrower? | **no card yet.** `datasec-nexusai-datasources-all-roles-fields-1125` is RULED a (delivered to RD-1040's kit) and covers the plain data-sources route only; whether option a also covers this route is Tuesday's reading (Q1 below) |
| W2 NexusAI RD-1042 | Text-or-test choice (a product choice) | no card yet |
| W3 NexusAI RD-1015 parts (2) and (3) | May the CSV bytes change for a leading space or look-alike before an equals sign, and for a negative amount with a currency sign (needs a real spreadsheet to measure)? | no card yet (and the new Low ticket for a comma, quote or line break in a number cell is for the PR 268 records pass) |
| W4 NexusAI demo deploy | Any deploy of the merged work | `nexusai-demo-deploy-c224-1123`, RULED a 2026-11-23, delivered C-314; the C-224 demo-deploy hold stands: nothing in this sweep deploys |
| W5 MPS words pack for the v13.4.1 lanes (the 28 lane-v tickets and 35 in the 11-19 sweep) | New customer and staff words, client data (284, 285), approval values (286, 287) | pickup text of 2026-11-19 lists it as a candidate "NOT yet posted"; **no card found** today |
| W6 MPS MPSCALC-233, 316, 120, 135, 297 | 233: what a derived (not typed) clone reference should do on a clash (counter or refusal); 316: the sentence for the two sibling messages and whether the schema places count; 120: which contract changes the version rule covers; 135: does a skip count as green; 297: is a hosted phone-width run required | no card found for any of the five; the records notes name each as "not ruled" |
| W7 MPS MPSCALC-272 | review summary tiles | `datasec-mps-mpscalc272-tiles-1124`, RULED a (hold until MPSCALC-315's figures exist) |
| W8 Composer: has the reviewer's current round ended (30 tickets wait on that answer) | Release of the held content-release chain and Guided hold | `composer-review-round-ended-1120` is **WITHDRAWN**; no live card found. `composer-pr85-land-held-deploys-1120` ruled a: deploys of a changed content release stay refused |
| W9 Composer PCOMP-46, 94, 123, 128, 129, 11, 36, 65 | confirmations, words, a measurement left as owner's choice | no card found |

## 5. Questions for Tuesday (each with a default)
1. **RD-1041.** Does the 11-25 card's ruling a (refuse routes to roles the permission table excludes) also cover `/api/setup/status`? Default: no; keep RD-1041 excluded and post one card.
2. **Start order for NexusAI.** One jest lock. Default: stamp B2139 (RD-455 + RD-981) now; then L3 kit 2 (RD-1014 with RD-1038), then L1 (RD-1010), then L4 starting with RD-1046; RD-1047 last (57 existing test files).
3. **MPS and Composer have no lane.** Default: spare capacity goes to NexusAI and to a single NexusAI records pass (PR 267 and 268, one writer); no sweep of MPS or Composer again until a ruling card lands or a new ticket opens.
4. **RD-387** straddles L1 and L2 (seed call site). Default: take it out of the first wave.
5. **RD-728** is excluded because its targets are on an unmerged branch. Default: leave excluded until RD-628's branch lands.

## 6. Method, UNMEASURED and disclosures
- Instruments: `board_count.sh` (counts); `jq.py` (a copy of yesterday's read-only helper, GET only, credentials read in process from each project's `.env`, never printed) for dumps and issue reads; `gh api -X GET` under each project's own `GH_CONFIG_DIR` for commits, compare, git trees; `decision_queue.sh prior --id x --title ...` (read-only; the RD-1038 subject returned 3 matches as the positive control, the other seven returned 0) and `decision_queue.sh show <exact id>` into scratch for six exact ids; `/usr/bin/grep`, python and `comm` over the dumps. Controls: every census equals its dump row count; RD sums 369 + 331 + 199 + 8 + 7 + 2 = 916; the RD To Do partition is 290 + 65 + 9 + 5 = 369 by program, missing 0, extra 0; the MPS and PCOMP key sets are yesterday's minus one with none new (by `comm`).
- UNMEASURED: whether any `wip/*` or `records/*` NexusAI branch carries unmerged work (not looked at); the 132 operations residue, 10 brand and 1 CodeQL NexusAI keys beyond title and label; the files of the carried L3 and L4 keys beyond ticket text and path existence (no code was read for them today; line numbers in the table are the tickets' own, read 11-26 for RD-1038, RD-1044, RD-1045 only); `HEAD` content of both Composer `CONTENT_HASH` files; any lock or live seat state; browser availability beside jest; MPS carried 160 and Composer carried 74-key reasons beyond stamps; a card named only in text I did not read.
- Writes: this file and the scratch folder only. No Jira, GitHub, card, mail, az, ssh, docker, hosted-host, test or build action; no `cd`; nothing deleted. Credentials were sourced in subshells and never printed. No agent was commissioned.
- READ-WHOLE-BY-TUESDAY: ____
