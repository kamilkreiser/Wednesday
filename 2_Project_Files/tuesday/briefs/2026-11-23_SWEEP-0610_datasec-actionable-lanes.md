# SWEEP-0610: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-23 morning)

Commissioned by Tuesday (s314), model Sonnet, routing row C8, in-session read-only. Clock from `date`: 06:11 AEDT at the last measurement. Form and old state: `2026-11-22_SWEEP-1450_datasec-actionable-lanes.md` (read whole first; every lane in it was dated 2026-11-22 14:50 and is re-checked below). Scope: Jira RD (NexusAI), MPSCALC, PCOMP. **HPSM-POC and OXPd were not swept, counted, read or listed** (hold to 2026-12-10, `tuesday/holds/HPSM-POC.hold`; OXPd is Tuesday's own). Fences kept: Jira GET only (credentials read by name in-process from each project's own `4_Credentials/.env`, never printed), `gh api -X GET` under each project's own `GH_CONFIG_DIR`, no write to any board or repository, no `cd`, nothing deleted, no message to any human. Scratch and instruments: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/sweep/` (the GET-only scripts copied from `fleet/state/s308/sweep/`, each read before use; dumps `RD_open.tsv`, `MPSCALC_open.tsv`, `PCOMP_open.tsv`, the three `*_done.tsv`, `pickup_hits.tsv`).

## BLUF

| project | open now (predicate; every page read to the end) | actionable now | lanes | notable exclusions |
|---|---|---|---|---|
| MPS Calculator (MPSCALC) | **166** (`project = MPSCALC AND ( statusCategory != Done )`, 2 pages, unique 166; all Backlog). Was 171 | **0 builds.** All seven of the 11-22 keys are now merged (PRs 226, 227, 228): 428, 429, 430, 432, 433 are Done; **427 and 431 are built, records only** (open by Tuesday's MOVE; 431's "first failure names the key" line is met by the sub-test label only) | 0 build lanes; one conditional (M-R, MPSCALC-272, Tuesday's call on words) | 195, 316 rest, 360, 419, 421, 424, 425, 395/372, 278; 272/283/274 words |
| Security Composer (PCOMP) | **77** (`project = PCOMP AND ( statusCategory != Done )`, 1 page; all Backlog). Unchanged | **1 new: PCOMP-67** (test-only, one file; its only block, "PR #85 is not landed", is gone: #85 landed 2026-11-20). **PCOMP-36/37 were built by #131** (36 stays open; 37 met on its letter): records only. Conditional: PCOMP-66 (engine edit, G1) | 2 (C-T PCOMP-67; C-E PCOMP-66 conditional) | PCOMP-44 (ruled hold), the reviewer-round hold, the Guided hold, owner's seven calls; the top-of-pickup no-deploy block binds |
| NexusAI (RD) | **898** (`project = RD AND ( statusCategory != Done )`, 9 pages, unique 898): To Do 370, Testing 312, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 | **80 To Do keys**: the 78 still-open of the 11-22 set (RD-175 and RD-349 landed in #240 and are Testing) plus **RD-1030 and RD-1031 (new)**; 7 conditional carried; **RD-1032 excluded (a brand decision)** | 8 (NX-P new, NX-S, NX-B, NX-F1, NX-F2, NX-T, NX-X; one seat at a time in practice, jest lock) | the 11 landed-awaiting-records keys, the held/ruling keys, Testing and Release Ready (511) |

Census controls (`board_count.sh` through `bc.sh`; every line printed "limit was 5001, so this is a real count and not a cap"): MPSCALC open 166 + Done 267 = 433 created, count 433 holds; PCOMP 77 + 52 = 129, count 129 holds; RD 898 + 130 = 1028, count 1028 holds. In every dump `rows` = `unique`. Key arithmetic against the 11-22 lists (`comm`-style diff of key sets): MPS 171 - 5 gone (428, 429, 430, 432, 433, all Done) = 166, 0 new; PCOMP 77, key set identical, 0 `updated` stamps changed; RD 895 + 3 new (RD-1030, 1031, 1032) = 898, To Do 369 + 3 - 2 moved to Testing (RD-175, RD-349) = 370, Testing 310 + 2 = 312.

Origin mains at sweep time (`gh api -X GET repos/.../commits/main`; `pulls?state=open` returned **0 open PRs** in all three repos): MPS `56f508a7` (#228, 2026-11-22T07:58Z); Composer `423516cb` (#131, 2026-11-22T17:16Z); NexusAI `3c3be156` (#241, records, 2026-11-22T17:56Z). Local `2_Project_Files` checkouts were not used: every file claim below is from origin main.

Standing facts that bind (pickup top and each project's `CLAUDE.md`): MPS seats push a branch only, Friday/Tuesday opens the PR (CodeQL rule), nothing deploys without a card; Composer: no deploy of a changed content release, the push-to-demo grant does NOT cover main since #85 (card `composer-pr85-land-held-deploys-1120`; the `CONTENT_HASH` refusal in every deploy kit); NexusAI: nothing deploys (C-224 demo hold), `npm run verify` (never bare `npm test`), one jest lock holder at a time; HPSM excluded; model rule 2026-11-21: Opus by default, Fable only when flagged (the lane gates below say Sonnet or Opus per the routing table, none Fable).

## RANKED LANES (value and size; the first two close in about 2 hours for one build seat)

| rank | lane | keys | size | why this rank | gate |
|---|---|---|---|---|---|
| 1 | **NX-P** (permission table) | RD-1030 | S, about 1.5 to 2 h | Delivers a promise already made to the product owner (card `nexusai-rd1011-read-routes-viewer-1120` option a: "the permission table is then brought into line ... in the next NexusAI change"); the pickup (line 74, DELTA 1362 item 3) names RD-1030 as that answer; no behaviour changes today (the table is read by no backend code), so risk is low and the red/green proof is a unit cell | G2, Sonnet builder |
| 2 | **C-T** (Composer test plant) | PCOMP-67 | XS, about 1 h | One line-group in one test file; newly unblocked by #85's landing; independent of every NexusAI lane (no jest-lock contention, different repo); the ticket gives the gate's own regression ("T1d must be RED and T1e too") | G2, Sonnet builder; branch only, no deploy, no release touched |
| 3 | **NX-F2b** (contrast suite upkeep) | RD-1031 | S to M, about 2 to 2.5 h | Cleans two stale files of the suite after #240; needs a stood-up local surface and a real Chrome/Playwright run in both modes (`npm run test:contrast`); a builder who cannot run it STOPS rather than guessing. Runs after NX-P (one NexusAI seat at a time) | G2 |
| 4 | **NX-S** (server) | RD-1021 (Opus, M, G1: viewer-reachable dialling), then the S bundle RD-1017, 577, 893, 896, 974, 975 | M + S each | The pickup's "next security lane" (RD-1021); the bundle is small server fixes in one file (`backend/server.js`), so one seat | G1 for 1021, G2 the rest |
| 5 | **C-E** (credential scan) | PCOMP-66 | S to M, conditional | Product edit in `packages/engine/src/secrets.ts` (test-only path, 0 product callers); the ticket carries the fix shape and a 72 + 18 member regression; needs differential, linear-time and db checks. Conditional only on Tuesday reading the old "deferred, outside a narrow round" ruling as lapsed | G1, Opus |
| 6 | NX-B, NX-F1, NX-F2, NX-T, NX-X | the carried keys (tables below) | per 11-22 sizes | Not re-sized today; see the 11-22 sweep's "Sizes and gates" | per lane |
| 7 | **M-R** (MPS review tiles) | MPSCALC-272 | M | Words-pending lane, Tuesday's call (below) | G2 |

Disjointness of the proposed lanes, by directory: NX-P owns `backend/services/capabilities.js` plus the two named test files (taken out of NX-S, which keeps `backend/server.js` and its helpers); C-T owns one file in `packages/content/test/`; C-E owns `packages/engine/src/secrets.ts` and its test; they share no path. NX-F2b owns `tests/e2e/dark-mode-contrast.spec.js` and `tests/e2e/light-baselines.json` (inside the 11-22 NX-F2 lane's `tests/e2e/**`).

---

## 1. MPS Commercial Calculator (MPSCALC)

Open 166, all Backlog. What landed since the 11-22 sweep (merged PRs, `pulls?state=closed`, the three newest by `merged_at`): **#226** (MPSCALC-430, 431, 432, 433; 2026-11-22T05:32Z), **#227** (MPSCALC-429; 07:27Z), **#228** (MPSCALC-427, 428; 07:58Z). The pickup (line 305) records R298 (READY 17add5bd) moving 428 and 429 to Done with 427 left open by Tuesday's MOVE; the board shows 430, 432 and 433 Done as well (the pickup line 376 listed their records pass as owed; I did not read who moved them). Done count 262 -> 267 (`MPSCALC_done.tsv`). Of the 166 still open, only two carry an `updated` stamp later than the 11-22 dump (MPSCALC-427: 2026-11-22T19:48; MPSCALC-431: 2026-11-22T17:20); the other 164 are unchanged since the 11-22 read (stamp comparison of all 171 keys, program), so their 11-20 classes are carried (see NOT tested).

### Actionable now: none as a build

The 11-22 sweep's seven keys are all built:

| key | state now | evidence |
|---|---|---|
| MPSCALC-428, 429, 430, 432, 433 | Done | board status, #226/#227/#228 |
| **MPSCALC-427** | **built, records only** | #228 (squash 56f508a7) carries `overflow-wrap: anywhere` at `web/src/proposal/proposal.css:71` and a committed Chrome print check; the 2026-11-22T19:48 comment reads "every line of this ticket's acceptance check reads met ... This note moves nothing and the ticket stays open until a later note moves it". A move to Done is Tuesday's reading, not a build |
| **MPSCALC-431** | **built, records only** | #226 (squash ec281cfb): `new_problems` at `infra/tests/test_infra.py:318`; four acceptance lines met, one ("the first failure printed names the key of the defect") "met by the sub-test label only and not by the message" (comment 2026-11-22T17:20). Whether to read it met and move the ticket is Tuesday's call (the pickup's own note: line 381, "leaves 431 open unless Tuesday reads it met") |

### Proposed lanes: none to build

No MPS key meets the build predicate today (the 11-20 evening sweep's B class went 6 -> 0 with these builds; nothing new was filed since; no MPS ticket has been created after MPSCALC-433). Pickup check (whole-file `/usr/bin/grep -o -i`, positive control RD-1011: 19 hits): MPSCALC-427 8 hits, MPSCALC-431 1 hit, MPSCALC-272 3 hits (the hit lines read "Tuesday's own reads owed" and "NOT STARTED ... MPSCALC-272 on pending words": no HELD or DROPPED line).

### Conditional (not counted): M-R, words-pending

**MPSCALC-272** [T-V7-1] "Review summary tiles (staff-only)": ticket text "Start: now, no ruling needed (plan section 4) ... Depends on: nothing ... New words go to the product owner's words gate before any deploy"; acceptance: "The tiles show the server's figures for the quote under review; a caller without internal-metrics sees none and the response carries none; component test". Files: `web/src/screens/Lifecycle.tsx` (exists at main; `grep -n -E 'internal-metrics|internalMetrics|summary|Tile|tile'` returned 0 hits in its 264 lines, so no tiles exist yet) and NEW `web/src/screens/review/**`; tests beside `Lifecycle.test.tsx`/`Lifecycle.b444.test.tsx`. Same shape as #219 and #221 (built on pending words, merged, words ride the deploy card). New customer-visible words are in play (tile labels), so it is Tuesday's call per lane (the standing default of the 11-20 sweep: yes, nothing deployed). Whether the server already sends all six figures was NOT read.

### Excluded (each as in the 11-22 sweep unless noted)

MPSCALC-195 (accepted engine-target sentence not on a readable record; OWED to Tuesday), 316 remainder (C-64 reach ruling not made), 360 (Tuesday owes a confirmation), 419 (needs `az` against the showcase subscription), 421 (a records action on a withdrawn advisory), 424 (a question for the product owner), 425 ("WAITS for his word; it is not to be started"), 395 and 372 (expired seed secret / deployment), 278 (two of three clauses landed; open for records), 283 (field-help catalogue, words-gated), 274 (needs a contract field whose name C-116 holds). The seed epics (MPSCALC-1 to 15), the question-for-Kam tasks (69 to 85), `needs-ruling` tickets (129, 144, 153, 157, 159, 177, 188, 222, 226, 261, 316) and the roughly 48 built-and-open tickets (the 11-20 evening sweep's JOB 4 table, 49 of 49 pull requests checked merged) are carried unchanged: their `updated` stamps are all older than this sweep's predecessor read. Spot re-reads for this sweep (last comments of MPSCALC-135, 297, 251, 369, 407, 402, 110, 223) agree with those classes: each is built-in-part with "the ticket stays open", a word of the product owner pending, or a deploy/host read.

---

## 2. Security Composer (PCOMP)

Open 77 (3 Bug, 4 Epic, 70 Task; all Backlog), Done 52. Key set identical to the 11-22 dump; no `updated` stamp changed (the Composer records pass for #131 is owed, see the pickup DELTA 1362 item 3). **Change since the 11-22 sweep: PR #131 merged** (squash 423516cb, 2026-11-22T17:16Z): "Baselines: default values per template row, as a draft data file", adding exactly three files (`content/baselines/default-baseline.json` 132 rows, 350 field targets; `content/baselines/README.md`; `packages/content/test/b1948-cw2-baselines.test.ts`, 12 cells). Per its body: no content release changes, both `CONTENT_HASH` files, `release-draft/bundle.json` and `content/sources/SOURCES.json` byte-identical to main, nothing deploys.

**The binding rule (pickup top):** main carries a NEW content release since #85; no Composer deploy to any host may ship it; the push-to-demo grant does not cover it. It does not stop builds; cutting the release, rebuilding the examples and any new customer word remain Kam's.

### PCOMP-36 and 37: built, records only

| key | state | what remains |
|---|---|---|
| PCOMP-37 | **built (#131), met on its letter** (the 28 CONDITIONAL/MANUAL rows read `"variable"` with the control decision in `set_by`) | records move only (pickup DELTA 1362 item 3: "PCOMP-37 met on its letter") |
| PCOMP-36 | **built in part (#131); stays open** | per the PR body and `content/baselines/README.md` Limits: only 4 of 34 typed boolean fields carry a value (2 true, 2 false), 16 sit on variable rows, **14 "wait for a reading of the template"**; 33 remediation states wait for PCOMP-42 (held); 21 rows hold null until the plain enable value is mapped. The 14-field reading is a possible later builder step, but it is a reading of the template (a judgement), not a mechanical change: **not counted as actionable**; named as Tuesday's call (Q2) |

The README line "No code reads it at this commit" is owed to lane L2-3 (PCOMP-38, held: words), per the pickup.

### Actionable (new): PCOMP-67 (lane C-T), conditional PCOMP-66 (lane C-E)

| key | scope (the ticket's own text) | files it would touch (read at main 423516cb) | size | proof it is still true on main |
|---|---|---|---|---|
| **PCOMP-67** | "The plant swap in the Q-03/Q-04 test leaves the generic Compare alternative unplanted ... dropping the Compare alternative from the second fragment now leaves the whole test green. Fix-shape (the gate's words): exercise every alternative: give the pattern one plant per alternative (or loop the alternation's alternatives in the plant check), keeping the distinctive one. Regression: T1d must be RED (and T1e too)." Test-only, "not compiled into dist, no customer artefact" | `packages/content/test/b330-sm316-qgate.test.ts` only (lines 71 to 75: the pattern `["constraint", ":(Constraint\|Policy", "ControlValue\|Compare)"]` with the plant `["constraint", ":Policy", "ControlValue"]`, so the Compare alternative is unplanted; the check at 196 to 205 uses `plant`) | XS | lines 71 to 75 printed from main; the ticket's own block ("PR #85 is not landed") is stale: #85 merged 2026-11-20T21:28Z, the file is now on main |
| **PCOMP-66** (conditional) | "The rendered-text scan can miss a directive that begins inside an exempt label run: the B350-5 fix opened a sibling bypass in the test-only renderedTextCredentialShapes variant (matchesDirectiveValue, the resume at found.index + found[0].length - value.length, line 51)"; fix shape (the gate's words): "report when EITHER main's alignment OR the resume-at-value-token alignment finds a non-exempt match whose value reads as a secret (both linear, so is the union). Regression cells: the 72 + 18 members; the four B350-5 strings stay flagged" | `packages/engine/src/secrets.ts` (`matchesDirectiveValue` at lines 44 to 58, resume at 51; used at 348) plus a new or extended test; 0 product callers per B424 R0f | S to M | lines 44 to 58 printed from main |

**PCOMP-66 caveats:** it is an engine source edit in the credential detector's scan loop (G1, Opus, the ticket says it needs "the differential, linear-time and db checks"); the ticket was "struck from fix round 3" as outside a narrow round, so whether that deferral lapsed with the landing is Tuesday's reading (Q3). Neither ticket touches `content/sources/SOURCES.json`, `content/release-*/**`, any `CONTENT_HASH` file or `packages/renderers`; the gate checks that with `git diff --name-only`. Pickup check (whole-file grep, control PCOMP-36: 9 hits): PCOMP-66 0 hits, PCOMP-67 0 hits, PCOMP-37 2 hits; the hold-word lines that mention PCOMP-36 (666, 681, 687) are the superseded "CW-2 not commissioned: wait for the card" notes (the card is ruled a and CW-2 was built as B1948): no HELD or DROPPED line names any key above.

### Excluded (with the line that sets each; unchanged from 11-22 unless noted)

- **PCOMP-44**: ruled HOLD (card `composer-pcomp44-refusal-words-or-hold-1101` option a, 2026-11-01).
- **Reviewer-round hold** (C-71 COMP-1 (b), C-92, C-99): PCOMP-19, 20, 31 to 35 (built on #85, records only), 38, 39, 92 and the 17 behind them (42, 45 to 51, 53 to 61). PCOMP-38 (L2-3, words) and PCOMP-39 (L2-4) are the next L2 lanes and are NOT buildable: words or reviewer-held.
- **Guided hold**: PCOMP-68, 69, 72, 75, 84, 85, 86, 87, 88, 90. **Owner's seven calls**: PCOMP-9, 70, 71, 73, 76, 91, 123.
- **Other `held`-labelled**: PCOMP-79 and PCOMP-89 (words/guide). **Words**: PCOMP-128 (DEPLOY.md, item 5 needs approved wording and item 2 a new operator command), PCOMP-129 (the hint's words), PCOMP-11 (contract change plus two new words), PCOMP-79.
- **Deploy, VM, environment, ops**: PCOMP-2, 10, 13, 16, 18, 25, 28, 78, 93. **Records and notes with nothing to build**: PCOMP-64, 65 (an informational Note), 12 and 23 (built, #119/#120), 41 (built, #87), 52 (built, #84).
- **Epics/guide/ratification**: PCOMP-1 to 8, 94 (`needs-kam`), 46 (`needs-kam`).

---

## 3. NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

Open 898: To Do 370, Testing 312, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 898). Main `3c3be156`. **Since the 11-22 sweep (main `8858e5d1`) two PRs merged:** #240 (RD-349 and RD-175; 8 files: `static/css/index-styles.css`, `static/css/dark-mode.css`, `static/css/tokens.css`, `scripts/derive-brand-tokens.js`, `scripts/verify-expected-counts.json`, `docs/BRAND.md`, `__tests__/fixtures/index-light-failure-baseline.json`, new `__tests__/rd349-rd175-readable-text-on-its-ground.test.js`; squash 50b7c40c) and #241 (records, HISTORY.md only; merge commit 3c3be156). The records seat (R301) moved RD-349 and RD-175 to Testing (board agrees: both Testing, `updated` 2026-11-23T04:13) and filed **RD-1030, RD-1031, RD-1032**. No other RD ticket's `updated` stamp changed (program comparison of all 895 keys against the 11-22 dump: only 175 and 349 differ), so the 11-22 deep reads of the carried keys still stand.

### New tickets (read whole: descriptions and the lines they cite)

| key | verdict | scope | files (verified at main 3c3be156) | size |
|---|---|---|---|---|
| **RD-1030** | **ACTIONABLE (lane NX-P, rank 1)** | The permission table still lists `GET /api/data-sources/:id/describe-table` and `GET /api/data-sources/:id/discover-tables` under `config.read` (a viewer holds it) after the product owner's 2026-11-20 ruling that they stay administrator-only (as #236 landed). Proposal (the ticket says "a proposal, not decided; the form follows the ruled option"): move the two rows to the existing `admin.read`; change cell P2 of the RD-1011 test to expect it; add the opposite-case cell to the census (every inventory route a viewer is refused on maps to a capability the viewer does not hold; it must fail at main on exactly these two rows and pass after) | `backend/services/capabilities.js` (rows at lines 155 and 156 inside the `config.read` block; `admin.read` defined at 96, block at 175; `READS_TODAY` at 107: all printed), `__tests__/rd1011-four-routes-administrator-only.test.js` (cell P2; file lists the two keys at line 33), `__tests__/rd929-capability-design-census.test.js` (the new cell beside the PENDING_GATE test at line 60), `scripts/verify-expected-counts.json` (cell counts, regenerated by Tuesday at landing). `docs/role-capabilities.json` lines 111 and 112 already say the wire's side (`requireAdminFor`) and need no change | S |
| **RD-1031** | **ACTIONABLE (lane NX-F2b, rank 3)** | After #240 the end-to-end contrast suite is stale: remove (or narrow to what still fails) the `.consumable-text` allow-list entry at `tests/e2e/dark-mode-contrast.spec.js:182`; regenerate `tests/e2e/light-baselines.json` (36 KPI-label lines at the old grey, `rgb(127, 140, 141)` on white 3.48, from line 27; command per the ticket: `UPDATE_LIGHT_BASELINES=1`); run the suite once against a stood-up local server in both modes and read its dead-excusal guard. Keep the other entries | the two files above; `npm run test:contrast` is `playwright test` (package.json line 34) and is outside `npm run verify`, so nothing in the verify says it is stale | S to M |
| **RD-1032** | **EXCLUDED (needs the product owner)** | Light-mode cyan, yellow and magenta toner fills read 1.74, 1.29 and 2.58 to 1 on the light track; the ticket says "each of the four fills is a brand colour with its own role, so the choice of values is a brand decision (BRAND.md section 8, rule 1) and is the product owner's, not an agent's" | (would be `static/css/index-styles.css`) | n/a |

### Re-screen of the 78 carried keys

All 78 are still To Do on the board (program check of the 80 key set: 78 To Do, 2 Testing). Main moved only by #240/#241, so no carried key is newly landed: #240 names only RD-349 and RD-175 and touches CSS selectors (KPI labels, import description and drop text, toner percentage and bars), none of which a carried ticket names, **except a possible same-line overlap for the dark-mode and index-styles edits of RD-164, RD-222, RD-261, RD-351 (NX-F2): a builder re-reads those CSS lines at 3c3be156 before editing.** Controls re-run on main `3c3be156` (`gh api -X GET`, counted on the untruncated text): `backend/server.js` (22,813 lines) still has 2 reads of `AUDIT_ACTIONS.SETTINGS_CHANGE` (lines 17363 and 17613) and 0 definitions of it (RD-1017 real); `GET /api/setup/data-sources` at 17163 and `GET /api/debug/data-sources` at 18393 (RD-1021 real); `static/index.html` has `role="tablist"` 0 hits, control `tab-button` present (lines 361, 362; RD-144 real). The other keys were not re-run on main (carried: their text is unchanged since the 11-11 deep read and the 11-22 landing screen).

Pickup check (whole-file grep, positive control RD-1011: 19 hits): RD-1021 5 hits, RD-1026 2, RD-759 3, RD-1014 2, RD-893 1, RD-1030 2, RD-1031 1, RD-1032 1; the other carried keys 0. **No HELD or DROPPED line names any proposed key**: the two hold-word lines that mention RD-1021 read "THEN: ... RD-1021 the two sibling routes as the next security lane" and "the next security lane beside RD-1021" (queue, not hold). The only holds are the C-224 demo hold (no deploy) and one NexusAI lane at a time.

### Lanes (directory partition; one NexusAI seat at a time in practice)

NX-P is new. NX-S, NX-B, NX-F1, NX-F2, NX-T and NX-X are the 11-22 lanes with their owned-file lists unchanged (`2026-11-22_SWEEP-1450_datasec-actionable-lanes.md` section 3, "Lanes", "Cross-lane exceptions" and "Sizes and gates" remain the reference and are not restated), with two edits: `backend/services/capabilities.js` moves from NX-S to NX-P; RD-175 and RD-349 leave NX-F2 (Testing). Cross-lane exceptions carried: RD-396 also edits `backend/services/riskAlertScheduler.js` (give that edit to NX-B or sequence); RD-515 edits `first-run-setup.html` (F1's file) from F2's banner-guard tests: after F1; RD-1016 before RD-1014 (one file, `settings.js`); RD-145, 745, 397, 918 need the Dockerfile (NX-T); NX-X (RD-1014, RD-1015) runs alone, last, after F1 and F2 land. `scripts/verify-expected-counts.json` is regenerated by Tuesday at each landing (#240 changed it).

### Actionable (80 keys), by lane (status and `updated` read from the board at this sweep)

**NX-P** (1 keys)

| key | type | status | updated | ticket title (trimmed to 150) |
|---|---|---|---|---|
| RD-1030 | Task | To Do | 2026-11-23 | The permission table still lists GET describe-table and GET discover-tables of the data-source routes under config.read, a capability a viewer holds,  |

**NX-S** (7 keys)

| key | type | status | updated | ticket title (trimmed to 150) |
|---|---|---|---|---|
| RD-974 | Bug | To Do | 2026-11-07 | The automatic insights check for unusual print times gives a job with no Job_Start_Time the current time, so undated jobs count as off-hours when it r |
| RD-975 | Bug | To Do | 2026-11-07 | The business-hours report reads created_at before the job's own start time, so a seeded row is judged by when the store was seeded and not by when it  |
| RD-893 | Task | To Do | 2026-10-27 | PUT /api/risk-conditions/:id leaves its other fields unchecked (condition_text, is_active and email_recipients accept any type) and stores risk_level  |
| RD-896 | Task | To Do | 2026-10-27 | Risk conditions stored with a mixed-case risk_level before PR #131 stay out of the High, Medium and Low lists and the alert mailer until saved again:  |
| RD-577 | Bug | To Do | 2026-11-11 | Key Vault status reporting reads KEY_VAULT_NAME but the template sets KEYVAULT_NAME (server.js:631, :642, :17733) — every Marketplace deploy shows 'no |
| RD-1017 | Bug | To Do | 2026-11-20 | AUDIT_ACTIONS.SETTINGS_CHANGE is used at backend/server.js lines 17353 and 17600 (add and remove a data source) and defined nowhere, so those two audi |
| RD-1021 | Bug | To Do | 2026-11-20 | Two sibling routes still let a signed-in viewer make the server use stored data-source sign-in details: GET /api/setup/data-sources tests every enable |

**NX-B** (9 keys)

| key | type | status | updated | ticket title (trimmed to 150) |
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

| key | type | status | updated | ticket title (trimmed to 150) |
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

**NX-F2** (16 keys)

| key | type | status | updated | ticket title (trimmed to 150) |
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
| RD-1031 | Task | To Do | 2026-11-23 | The end-to-end contrast suite still excuses the toner label (tests/e2e/dark-mode-contrast.spec.js line 182) and its light baselines still list the KPI |

**NX-T** (34 keys)

| key | type | status | updated | ticket title (trimmed to 150) |
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

| key | type | status | updated | ticket title (trimmed to 150) |
|---|---|---|---|---|
| RD-1014 | Bug | To Do | 2026-11-20 | Values from outside are still written into the page as HTML or into quote-unsafe attributes after RD-861: scan file names, print-log user names and pr |
| RD-1015 | Task | To Do | 2026-11-20 | RD-835 residue: four CSV writers still write numeric cells (sheets, pages, size) without the helper, a leading space or look-alike before an equals si |

### NexusAI: conditional (not counted: investigate first, or a choice the ticket leaves open; carried unchanged from 11-22, none moved)

RD-1019 (a question about the Marketplace webhook vs the global sign-in check; first step is to run it), RD-1022 (does a viewer reach five more connecting routes; "decide with the product owner" if one does), RD-1020 (boot-time refusal for `MARKETPLACE_SKIP_JWT`: a design choice, default refuse to mount the router), RD-1029 (fixed short reason changes what the setup wizard shows: new words), RD-763 and RD-764 (CodeQL judgement tickets: read first, record the reading for Kam), RD-1006, 1009, 1010 (census first, then per-handler fixes). **Updated link:** the permission-table ticket the 11-22 sweep (Q5) said was "not yet filed" is now **RD-1030** (above).

### NexusAI: excluded (with the reason)

- **Landed on main, records only (11 To Do keys, all still To Do on the board)**: RD-538 (#203), 563 and 969 (#198), 729 (#218), 826 (#202), 970 (#192), 731 (#194, partly), 972 (#195), 929, 977, 978 (#197). Pickup names the next NexusAI records pass.
- **Held, needs a ruling or Kam**: RD-805 and RD-768 (CodeQL alerts left open by design), RD-1025 (product owner's word first), RD-1028 (design choice, no fix shape), RD-433, 610, 612, 622, 644, 522, 884, 546, 193, 583, 584, 305, 313 (as in 11-22).
- **Needs the product owner or a customer-facing word**: **RD-1032 (new)**, RD-702, 636, RD-1029, the roles-UI chain RD-937 to 957 (35 To Do keys with `roles-ui-2026-11`).
- **Not agent work**: epics RD-6, 7, 8; business/hiring/compliance RD-13, 20, 21, 22, 28, 29, 30, 31, 34; Azure and secrets RD-50, 54, 55, 83; Jira and session tooling RD-233, 287, 449; marketplace-labelled Partner Center items (26 To Do keys); feature requests RD-146, 400, 401, 842.
- **In Progress (8), Put on Hold (7), Declined (2)**: RD-49, 81, 427, 431, 432, 450, 643, 662; RD-18, 32, 33, 41, 93, 104, 743; RD-300, 564 (counts only; titles not re-read; "whether the three 2026-09 plans merged" stays UNMEASURED).
- **RD-1004** (picomatch audit exception, re-check on or before 2026-12-18: dated work) and **RD-1001** (stale `core.sshCommand` on the records working copy: launcher-side).
- **Testing 312 and Release Ready 199**: not work.
- **The other To Do keys (about 280, the `operations`-labelled residue and QA-gate findings)**: not re-read; UNMEASURED beyond titles and `updated` stamps.

---

## 4. Questions for Tuesday (each with a default)

1. **MPS has no build lane today.** Default: start nothing on MPS from this sweep; the two records items are (a) MPSCALC-427: read the 2026-11-22T19:48 comment's "met" reading and move it Done or leave it, and (b) MPSCALC-431: read whether the sub-test label meets "the first failure printed names the key" and move it or leave it open with that line named.
2. **PCOMP-36's 14 undecided boolean fields** ("wait for a reading of the template"). Default: leave PCOMP-36 open per the pickup, with the Composer records pass for #131 stating what is met; do not commission a reading lane until Tuesday reads whether 36 may close on the 4-of-34 cut.
3. **PCOMP-66 (engine edit, deferred in round 3 of PR #85).** Default: build only PCOMP-67 now (C-T); hold PCOMP-66 until Tuesday reads the deferral as lapsed, then Opus builder with a G1 gate.
4. **MPSCALC-272 on pending words.** Default (the 11-20 sweep's): yes, per lane, nothing deployed; the tile words go on the deploy card.
5. **NexusAI order.** Default: NX-P (RD-1030) now, then NX-F2b (RD-1031), then RD-1021 (NX-S), RD-1026 (NX-F2), then the NX-T residues; NX-X last; one NexusAI seat at a time. RD-1032 is a card for the product owner at most (Tuesday's call), not a seat.
6. **Records owed that this sweep saw but did not touch:** Composer records pass for #131; NexusAI landed-but-To Do keys (11); MPS 427/431 reading (Q1).

## 5. How measured, and NOT tested

- Instruments: paginated Jira `search/jql` (GET, page size 100, 0.25 s apart; `jqdump.py` read each page to `isLast`, so no capped first page), `board_count.sh` through `bc.sh`; `jdesc.py`/`lastc.py` for ticket text and last comments; `gh api -X GET` for mains, open and closed PR lists, PR bodies and file lists, and file reads at main through `rg.sh`; `/usr/bin/grep`, `awk`, `diff`, `join` over the dumps. Positive controls: RD-1011 in the pickup (19 hits), PCOMP-36 in the pickup (9 hits), `tab-button` in `static/index.html`, the two `SETTINGS_CHANGE` reads in `server.js`, the 80 rows of the generated lane tables (0 "NOT OPEN").
- **Not tested:** (a) The 164 unmoved MPS tickets, the 77 Composer tickets and about 280 NexusAI To Do tickets were not re-read for text, only for key list and `updated` stamps; their classes are carried from the 11-20 and 11-22 sweeps and say so. (b) Of the 80 RD actionable keys, only RD-1030 and RD-1031 were read whole and re-checked against main today, plus the controls named in section 3 (RD-144, 1017, 1021); the other 77 carry the 11-11 deep read plus the 11-22 landing screen; the 11-22 file lists which were verified there. (c) PCOMP-67's claim that the fix makes T1d and T1e red was NOT run; only the unplanted alternative at lines 71 to 75 was read on main. (d) MPSCALC-272: whether the server already sends all six figures was not read. (e) RD-1031's suite was not run (needs a stood-up surface). (f) Sizes and time guesses (about 1.5 to 2 h, 1 h, 2 to 2.5 h) are estimates from the ticket scope, to be confirmed by the kit drafter's own reads. (g) The checks of mains read origin only; no push-run or CodeQL state was read for #226, #227, #228, #131 or #240 (the pickup records them as closed).
- Disclosures: no write outside this file and the scratch folder `fleet/state/s314/sweep/` (which holds the dumps above, the copied GET-only scripts, `mk_tables.py` and the generated `rd_tables.md`); no Jira or GitHub write; no deletion; the pickup `NEXT-PICKUP-TUESDAY.md` was read, never edited; one `gh` call set used each project's own `GH_CONFIG_DIR` (NexusAI, MPS, Composer separately, one per repo); no token printed.

READ-WHOLE-BY-TUESDAY: ____
