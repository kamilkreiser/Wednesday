# SWEEP-1450: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-22 afternoon)

Commissioned by Tuesday (s308), model Sonnet, routing row C8, in-session read-only. Clock from `date`: 14:55:59 AEDT at the last measurement. Form: `2026-11-11_SWEEP-1326_datasec-actionable-lanes.md` (read first) and the newest full sweep `2026-11-20_SWEEP-EVENING_datasec-backlog-refresh.md` (read for MPS and Composer state). Scope: Jira RD (NexusAI), MPSCALC, PCOMP. **HPSM-POC and OXPd were not swept, counted, read or listed** (hold to 2026-12-10: `tuesday/holds/HPSM-POC.hold`). Fences kept: Jira GET only, `gh api -X GET` under each project's own `GH_CONFIG_DIR`, no write to any project or board, no `cd`, no token printed, nothing deleted, no mail. Scratch and instruments: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/sweep/` (GET-only `jqdump.py`, `jdesc.py`, `lastc.py`, `bc.sh`, `rg.sh`, copied from `fleet/state/s299/sweep_evening/`, each read before use).

## BLUF

| project | open now (predicate) | actionable now | lanes proposed | notable exclusions |
|---|---|---|---|---|
| MPS Calculator (MPSCALC) | **171** (`project = MPSCALC AND ( statusCategory != Done )`, 2 pages, unique 171; all Backlog) | **7**: MPSCALC-427, 428, 429, 430, 431, 432, 433 (all filed 2026-11-20/22 by records passes; all test-only, comment-only or one CSS rule; none touches a word a customer sees) | 4 (M-P, M-S, M-I, M-V) | 195, 316 rest, 360, 419, 421, 424, 425 (see section 1); 272/283 words-pending (Tuesday's call) |
| Security Composer (PCOMP) | **77** (`project = PCOMP AND ( statusCategory != Done )`, 1 page; all Backlog) | **2**: PCOMP-36, 37 (lane CW-2); everything else held, ruled hold, words, or built-and-open | 1 (CW-2) | PCOMP-44 (ruled hold 11-01), the 25 reviewer-round-hold keys, the Guided hold, PCOMP-31 to 35 and 52 (built, records only); the top-of-pickup deploy block binds every Composer deploy |
| NexusAI (RD) | **895** (`project = RD AND ( statusCategory != Done )`, 9 pages, unique 895): To Do 369, Testing 310, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 | **80** To Do keys (65 carried from the 11-11 reads and re-screened for landing, 5 ruled since, 10 new from the 11-20 records passes); plus 7 conditional (investigate first) | 6 (NX-S, NX-B, NX-F1, NX-F2, NX-T, NX-X); one NexusAI seat at a time in practice (jest lock) | Testing and Release Ready (509) are not work; 11 To Do keys landed and wait for records only; in-progress seats and the held CodeQL/ruling items (section 3) |

Census controls (counted by `board_count.sh` through `bc.sh`, 14:4x; every line printed "limit was 5001, so this is a real count and not a cap"; dumps by paginated `jqdump.py` to the last page, `rows` = `unique` in all six): MPSCALC open 171 + Done 262 = 433 created, count 433 holds; PCOMP 77 + 52 = 129, count 129 holds; RD 895 + 130 = 1025, count 1025 holds. Key arithmetic against the last lists: MPS 171 (11-20 17:42) - 7 gone (314, 417, 418, 420, 422, 423, 426, all now Done) + 7 new (427 to 433) = 171; PCOMP 78 - 1 gone (PCOMP-29, Done 2026-11-20 21:29) = 77; RD 879 (11-19 16:30 key list) - 0 gone + 16 new (RD-1014 to RD-1029) = 895, and To Do 359 + 16 - 6 moved to Testing (RD-1008, 1011, 1012, 1013, 835, 861) = 369.

Origin mains at sweep time (all `gh api -X GET`): MPS `9c9a7219` (#225, 2026-11-21T13:02Z; 0 open PRs); Composer `3638da61` (#85 merged 2026-11-20T21:28Z; 0 open PRs listed); NexusAI `8858e5d1` (#239, records, 2026-11-20T21:05Z; 0 open PRs listed). Local `2_Project_Files` checkouts were not used: every file claim below is from origin main.

Standing facts that bind (read from the pickup top and each project's `CLAUDE.md`): MPS seats push a branch only, Friday/Tuesday opens the PR (CodeQL rule), nothing goes to a human without Kam's send; Composer: no deploy, and the push-to-demo grant does NOT cover main since PR 85 landed (pickup top block, card `composer-pr85-land-held-deploys-1120`); NexusAI: nothing deploys (C-224 demo hold, as quoted in the pickup), protocol v1.3, tests via `npm run verify` and one jest lock holder at a time; HPSM excluded.

---

## 1. MPS Commercial Calculator (MPSCALC)

Open 171, all Backlog (15 Epic, 156 Task). 159 of the 171 carry an `updated` stamp earlier than 2026-11-20T17:40 (the 11-20 evening sweep's read); the 12 that moved are MPSCALC-278, 427 to 433 (new) and the five Done keys left the list. Everything not named below keeps the 11-20 evening classes (B 6 -> 0 after the builds; L 48, W 34, R 13, H 0, C 1, D 12, X 4, P 8, S 21, O 24, adjusted by the seven keys that left and the seven that joined); **those unmoved tickets were not re-read** (see NOT tested).

What landed since the 11-20 evening sweep (merged PRs, `gh api -X GET pulls?state=closed`): #223 (MPSCALC-314, autosave gap, 2026-11-20T08:34Z), #224 (MPSCALC-418, infra test pins, 08:34Z), #225 (MPSCALC-420 and 417, ENGINE.md and infra/README.md, 2026-11-21T13:02Z). Done on the board: 314, 417, 418, 420, 422, 423, 426. Newest records: R293 (C-190) verified by Tuesday, per the pickup (DELTA 1303 item 4).

### Actionable (7 tickets; all still true at origin main `9c9a7219`: blob shas printed, matching the shas the tickets name)

| key | scope sentence (from the ticket's own text) | files it would touch (at 9c9a7219) | size | proof it is still open on main |
|---|---|---|---|---|
| MPSCALC-433 | "Change the one step number in the comment so that it names the step the runbook numbers for the what-if, and nothing else in the file" (comment only; run `infra/tests/test_validate_script.py`, 6 tests, and the CI python loop) | `infra/scripts/validate.sh` line 4 (blob 26968eb0; prints "and is infra/README.md step 3."); reads `infra/README.md` 59 (what-if is step 2) and 65 (create is step 3) | XS | line 4 printed; README lines 59 and 65 printed |
| MPSCALC-432 | "Add the seven [site properties: always on, HTTP/2, remote debugging, 32-bit worker, startup command, client affinity, public network access] to the site table of the same file, each red under a planted change of the template source and green without it" (the pin-or-absence choice per property is the builder's) | `infra/tests/test_infra.py` (blob c0e6a272; `SITE_EXPECT` at line 120, read at 143); reads `infra/modules/showcase.bicep` | M | `SITE_EXPECT` at 120 printed (blob sha equals the ticket's) |
| MPSCALC-431 | "Compare each mutant result with the unmutated result and assert exactly one new problem ... and guard the deletion of a missing setting with a message that names the key" | `infra/tests/test_infra.py` only (the two mutant classes) | S-M | same blob c0e6a272 |
| MPSCALC-430 | "One test that asserts the expected number of rows of the three tables and of the list of plants ... each shown red by emptying its table and green without it" | `infra/tests/test_infra.py` only (`COMPUTED_SETTINGS` 247, `PINNED_LITERALS` 259 printed) | S | same blob |
| MPSCALC-429 | "Add two cells to `QuoteScreen.autosave.test.tsx`: an explicit save 5 seconds into a gap makes the next autosave wait until 10 seconds after that save, and a second save request restarts the running gap timer; each red under the one-line change" | `web/src/screens/QuoteScreen.autosave.test.tsx` (blob 940d8cdf); reads `QuoteScreen.tsx` (`armGap` at 240, called at 268 printed) | S | blob sha equals the ticket's |
| MPSCALC-428 | "Decide the places where a code can start on the text as it stood before any strip, in one pass (no cascade); remove any U+0001 from the text nodes and attribute values before the marks are written; add a cell for each, and the missing split-figure cell" | `web/src/proposal/unpriced.test.tsx` (blob eb3f7e7b; U+0001 mark comment at 139 printed) | M | blob printed |
| MPSCALC-427 | "Let a part code break inside the stream cards of the full proposal (an overflow-wrap rule on the card items), then print the unpriced full proposal with a 60-character code in the first stream card of a seven-package proposal and compare it with a short code: same page count, same text size"; the ticket says to measure real catalogue part-code LENGTHS first, "a program that prints only the lengths and reads no price" | `web/src/proposal/proposal.css` (`.pd-cards` 67, `.pd-card` 68, `.pd-bullets` 70 printed), `web/src/proposal/ProposalDocument.tsx` (`Cards` at 112, stream cards near 345), a PDF check (new test file or an addition) | M | lines printed |

Cautions the tickets themselves carry: MPSCALC-427 needs the catalogue lengths measured from the local pricebook store (`2_Project_Files/.local/pricebooks/`, gitignored, 0600, confidential: lengths only, never a price, never pasted), and the PDF page-count check needs a real Chrome print: a builder who cannot run it STOPS rather than guessing. MPSCALC-428 and 429 and 430 to 432 are "no product byte, no word of the product owner" by their own text.

### Proposed lanes (file-disjoint: no path in two lanes)

| lane | keys | owns | why disjoint |
|---|---|---|---|
| M-I (infra tests) | MPSCALC-430, 431, 432 | `infra/tests/test_infra.py` | one file, so one lane and one seat; the three tickets share it |
| M-S (infra script) | MPSCALC-433 | `infra/scripts/validate.sh` (reads, never edits, `infra/README.md` and `infra/tests/test_validate_script.py`) | shares no file with M-I; `test_infra.py` has 0 mentions of that comment |
| M-V (screen test) | MPSCALC-429 | `web/src/screens/QuoteScreen.autosave.test.tsx` | web/src/screens, nothing in common with M-P or M-I |
| M-P (proposal) | MPSCALC-427, 428 | `web/src/proposal/**` (css, `ProposalDocument.tsx`, `unpriced.test.tsx`, a new PDF check) | one directory, one seat: 427's PDF check may add to or read `unpriced.test.tsx`, so the two keys are not split |

M-S is XS and rides with any seat that is already open; M-I, M-V, M-P are G2 by their own scope (tests, one CSS rule). All four can run side by side but the MPS heavy-job rules of the last kits apply (one waiter, load1 under the stated limit). Branch only; Tuesday or Friday opens the PR.

### Not counted, with the reason (each is carried from the 11-20 evening sweep unless noted)

- **MPSCALC-195**: its accepted engine-target sentence is on no record a seat may read (kit B1741 FACT 2); pickup line 625 and 643 name it OWED: re-draft it and card the exact words to Kam. Not buildable.
- **MPSCALC-316 remainder**: `docs/api/openapi.json` `maxLength` and the C-64 reach ruling are NOT RULED (C-184 "Work owed"); the two sibling messages have no ticket.
- **MPSCALC-360**: Tuesday owes a confirmation after a worked reading (answers file); not a build.
- **MPSCALC-419** (needs `az` against the showcase subscription and a coordinator go), **MPSCALC-421** (a records action: read the alert again), **MPSCALC-424** (settle what "recorded" means as a question with a default for the product owner), **MPSCALC-425** ("WAITS for his word; it is not to be started"), **MPSCALC-395 and 372** (the seed identity's expired secret, an Entra write for the product owner).
- **MPSCALC-278**: two of three clauses landed (#221, #222, the latter named MPSCALC-278 in its title); open for records. Updated 2026-11-20T20:19.
- **Words-pending lanes, Tuesday's call (not counted)**: MPSCALC-272 [T-V7-1] "Review summary tiles (staff-only)", ticket text "Start: now, no ruling needed ... Depends on: nothing"; files `web/src/screens/Lifecycle.tsx` plus new `web/src/screens/review/**`; same shape as #219 and #221 (built on pending words, merged). The pickup names it "Tuesday's own reads owed" (lines 380 and 393): no HELD or DROPPED line. MPSCALC-283 (field-help catalogue) is words-gated the same way and was not read to lane shape. MPSCALC-274 needs a contract field whose exact name C-116 holds.
- The 33 other W keys, the 13 R keys, the 12 D keys and the 21 S keys are unchanged from the 11-20 evening classes (staleness control: their `updated` stamps predate 11-20 17:40).
- Pickup check (`/usr/bin/grep` over the whole pickup, positive control RD-1011 17 hits): MPSCALC-427 2 hits, 429 1, 433 2, 428/430/431/432 0; the hits read "filed", "for a later MPS wave" (line 64: "MPSCALC-433 (one-line) for a later MPS wave"; line 78 the same), no HELD or DROPPED line for any proposed key. MPSCALC-195 7 hits, all OWED.

---

## 2. Security Composer (PCOMP)

Open 77, all Backlog (3 Bug, 4 Epic, 70 Task). Done 52. **Change since the 11-20 evening sweep: PCOMP-29 (the L0-1 crosswalk) is Done; PR #85 merged to Composer main** (`3638da61`, "L1 SM 3.16 content catalogue: release built, not cut (#85)", 2026-11-20T21:28Z), after card `composer-pr85-land-held-deploys-1120` ruled a. The nine tickets with `updated` 2026-11-20T21:29 (PCOMP-31 to 35, 42, 44, 52, and 29) were touched by the records pass in the same minute; their last comments say "pull request 85 ... not merged" and are now stale by one minute.

**The binding rule (pickup top, verbatim in short):** main now carries a NEW content release; no Security Composer deploy to any host may ship it and the push-to-demo grant does not cover it; every Composer deploy kit carries the refusal (`CONTENT_HASH` line in `tuesday/DRAFTER_RULES.md`). It does not stop builds. Cutting the release, rebuilding the examples and any new customer word remain Kam's (C-92, C-97, C-100).

### Actionable (2 tickets, one lane) and the evidence

| key | scope (ticket title, and the plan lane's cut) | files | size |
|---|---|---|---|
| PCOMP-36 | L2-1 "per item: class, target per field, default severity, remediation state, unsupported handling, from the APPROVED template, in a new content/baselines/ data file" (C-100 approved the template) | NEW `content/baselines/<one data file>.json`, `content/baselines/README.md`, NEW `packages/content/test/<lane>-baselines.test.ts` | M |
| PCOMP-37 | L2-2 "the 28 CONDITIONAL/MANUAL items carry 'variable' plus the Composer question or control decision that sets them (same new data file)" | same new file | S |

Source: Tuesday's own analyst B1797 (`tuesday/briefs/2026-11-20_B1797_COMPOSER-LANE-PLAN.md`, sections 1 and 4, lane CW-2, read for this sweep, not the whole 158 lines), which read all 30 held keys whole on 2026-11-20 evening; B1743 (pickup line 642) agrees: "only PCOMP-36/37 buildable". **Two changes since that plan: (1) its CW-2 was "stacked on held PR #85, merge only after it lands": #85 has landed, so the base is now main `3638da61`, no stacking; (2) its CW-1 (PCOMP-29) is Done.** The pickup (line 327) says CW-2 was "NOT commissioned: Tuesday's choice is to wait for his answer to this card first"; the card is ruled a (pickup top block), so that wait is satisfied. No HELD or DROPPED line names PCOMP-36 or 37 (whole-file grep: PCOMP-36 4 hits, PCOMP-37 0 hits, all in those two DELTA lines and the 642 line).

**Lane CW-2 (the only lane).** Owns by property: every file inside the NEW directory `content/baselines/` and new test files named for the lane under `packages/content/test/`; closed list proven at the gate by `git diff --name-only`. Must NOT touch: `content/sources/SOURCES.json`, `packages/content/src/**`, `content/release-demo/**`, `content/release-draft/**` (any change there IS a release, his), `packages/engine/**`. The data file carries enumerations and typed values only and NO sentence (the template's `_meta`: "Source wording from a client sample, de-identified. Not Datasec's words"); PCOMP-36's "target value per field" is met for 34 typed boolean fields only, so whether PCOMP-36 may close with that cut is Tuesday's reading, said at the gate. Gate tier G2 while no code reads the file; G1 the moment a loader or test reads it into the bundle. Heavy jobs only under `.tools/composer-heavy.lock` (analyst's note from kit B1581). **What would STOP it:** a sentence needed in the file (words card K9); a typed value wanted for an untyped field; an `item_key`/`field_key` absent from main; any edit outside the closed list; any state "after validation" or "controlled/staged" (PCOMP-42's). **The plan was written when #85's head was the base; its claim that `content/baselines/` is absent was read at the old main: a builder must re-run `git ls-tree` on 3638da61 (UNMEASURED today, not re-checked here).**

### Excluded (with the line that sets each)

- **PCOMP-44**: ruled HOLD, card `composer-pcomp44-refusal-words-or-hold-1101` option a, 2026-11-01 10:05 ("until the renderers exist"); the renderers wait behind the reviewer-round hold.
- **Reviewer-round hold (C-71 COMP-1 (b), C-92, C-99; no end named, "the owner says so")**, carried from the 11-20 evening sweep: PCOMP-19, 20, 31 to 35, 38, 39, 92 (the 29 left as Done) and the 17 behind them (42, 45 to 51, 53 to 61). PCOMP-36 and 37 are the two the plan carved out of that hold because C-92 says "Permits now: L1 and L2 may be built and merged on branches"; the plan reads them as BUILD NOW on that sentence, and that reading is Tuesday's to confirm at the gate.
- **Guided hold (C-71 COMP-2, no Guided work until he turns it back on)**: PCOMP-68, 69, 72, 75, 84, 85, 86, 87, 88, 90.
- **Owner's seven calls**: PCOMP-9, 70, 71, 73, 76, 91, 123.
- **Built and open, records only**: PCOMP-31 to 35 (built on #85, now on main), PCOMP-52 (the table of contents, #84, 308b7aa6, 2026-10-20).
- Pickup line 111 and the DELTA blocks: a Composer records pass is OWED (main `3638da61` checks and alerts read to the end, records for #85); not a ticket build.

---

## 3. NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

Open 895: To Do 369, Testing 310, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 895; types 417 Bug, 403 Task, 72 Story, 3 Epic). Testing and Release Ready (509) are not work (JIRA.md flow To Do, In Progress, Testing, Release Ready, Done) and were not read individually. Main `8858e5d1`; since the 11-11 sweep the NexusAI queue merged #198 to #238 (code PRs: 198, 199, 200, 201, 202, 203, 204, 205, 206, 208, 209, 211, 212, 216, 218, 220, 221, 222, 223, 225, 227, 229, 231, 233, 234, 236, 238; the rest are records PRs).

**How the actionable set was built (so the number can be audited).** (1) Took the 11-11 sweep's "Actionable (about 104 keys)" tables (its deep reads of about 190 last comments and 45 descriptions): the keys extracted by program from those tables are 109 (`rd_1111_all.txt`); today 77 of them are still To Do, 28 are Testing, 3 Done, 1 Release Ready. (2) Screened the 77 against merged PR titles AND bodies (the body read for each of 30 code PRs; `rd_pr_keys.txt`): RD-538 (#203), 563 and 969 (#198 title), 729 (#218), 826 (#202 title) are LANDED but still To Do (records move owed), so they are not actionable; RD-970 (the ENOTDIR fix is #192's title, 2026-11-11), RD-731 (#194, 13 of 14 suites: last comment "Landed on main in part"), RD-972 (#195: last comment "Landed on main") and RD-929, 977, 978 (#197) are landed too; RD-805 and RD-768 are NOT built (PR bodies of #209 and #211: "read and reported only"; alerts stay open, "nothing is decided for them" in the 11-17 sweep), RD-740 (cause undetermined), RD-820 (needs a seam), RD-763 and RD-764 (CodeQL judgement tickets: read first, record the reading for Kam, so conditional) are not counted. 77 - 5 - 1 - 2 - 2 - 2 = 65 carried. (3) Ruled since the 11-11 sweep (11-11 19:00 wave-3 sweep, rulings of 14:15 to 14:34) and still To Do, added: RD-349 (brand contrast ruling; queued by Tuesday as N-L with RD-175, pickup lines 507, 521, 625), RD-759 third shape (refuse `data:` addresses carrying an at-sign; N-O), RD-810 (fix, red first, never dismiss), RD-577 (status read only), RD-578 (own PR, own red proof, Opus) = 5. (RD-175 was already among the 65.) (4) New since 11-19 16:30: RD-1014 to RD-1029 (16 keys, all `records-pass-1120`, `security`): 10 actionable (1014, 1015, 1016, 1017, 1018, 1021, 1023, 1024, 1026, 1027), 4 conditional (1019, 1020, 1022, 1029), 2 excluded (1025, 1028). **Total 65 + 5 + 10 = 80** (lane tables below list exactly these 80; checked by program: 78 in five lanes plus RD-1014 and RD-1015 in NX-X, no key twice).

Programmatic controls on origin main `8858e5d1` (read by `gh api -X GET`, counted by `grep -c` on the untruncated text): `static/index.html` has `role="tablist"` count 0 (control: `tab-button` 10; RD-144 real); `cdn.jsdelivr.net` present at lines 12, 13, 16, 1069 (RD-145 real); `backend/server.js` (1,139,811 bytes) has 2 reads of `AUDIT_ACTIONS.SETTINGS_CHANGE` (lines 17363 and 17613) and 0 definitions of it (control: `AUDIT_ACTIONS` 41 hits; RD-1017 real); the risk-condition guard `if (updates.risk_level && (typeof ...` at line 21654 (RD-893/892 residue real); `KEY_VAULT_NAME` 3 hits and `KEYVAULT_NAME` 2 in `server.js` (RD-577 real); `GET /api/setup/data-sources` at 17163 and `GET /api/debug/data-sources` at 18393 (RD-1021 real); `tool_call` case at `static/js/index.js` 3506 (RD-1026's label line drifted by about 17 lines since the ticket); `static/first-run-setup.html` has 0 `style="` hits (RD-117 and RD-188's own 11-16 comment says the same and orders one real-browser run to count refused styles before any fix: a read-only first step). Not re-run on main (carried): the 60 others of the 65 (their `updated` stamps are all before 2026-11-11T13:30 except RD-117, 188, 175 (11-11 and 11-16 comments, read for 117, 188), so no ticket text changed since the deep read).

**Pickup (whole-file grep, positive control RD-1011: 17 hits).** The queue the pickup names: N-L (RD-349, RD-175), N-O (RD-759), then RD-929 drafting (already landed #197: records only), RD-1021 as "the next security lane", RD-1026 "the next security lane beside RD-1021", and OWED: "the NexusAI permission-table ticket" (card `nexusai-rd1011-read-routes-viewer-1120` option a: "The permission table is then brought into line with it in the next NexusAI change"; lines 111, 214) which a records seat must file first: it is not on the board yet. **No HELD or DROPPED line names any proposed key**; the only holds are the C-224 demo hold (no deploy) and one NexusAI lane at a time (the jest lock). RD-1004 (the picomatch audit exception, re-check on or before 2026-12-18) is dated work, not for today.

### Lanes (directory partition; the first-listed owner of a shared file wins; one seat at a time in practice)

1. **NX-S, server.** Owns `backend/server.js` and `jsonStorage.js`, `simpleDb.js`, `intentRouter.js`, `queryPreprocessor.js`, `ticketStore.js`, `costCentreMap.js`, `docs/role-capabilities.json`, `docs/ROLE-CAPABILITIES.md`, `backend/services/capabilities.js`. Any new handler gate needs the inventory regenerated from a non-dot tree (11-11 sweep note). RD-1021 is Opus (security, viewer-reachable dialling) with a G1 gate; the rest Sonnet.
2. **NX-B, backend periphery.** Owns `backend/**` not in NX-S: `backend/services/scimProvisioning.js`, `entraProvisioning.js`, `dataErasure.js`, `backend/azure-ad.js`, `backend/services/cspReport.js`, `backend/encryptionService.js`. RD-744 and RD-578 Opus.
3. **NX-F1, first-run, login and settings pages.** Owns `static/{login,first-run-setup,settings}.html`, `static/js/{first-run-setup,settings,entra-provisioning-ui}.js`, `static/css/first-run-setup-styles.css`.
4. **NX-F2, dashboard.** Owns `static/index.html`, `static/js/{index,admin,chart-details}.js`, `static/css/**` less the first-run stylesheet, `tests/e2e/**`. RD-145 last (needs the Dockerfile, which NX-T owns).
5. **NX-T, tests, scripts and CI.** Owns `scripts/**`, `.github/**`, `docs/**` (less the role-capability files), `__tests__/**`, `tests/uat-run.js`, `Dockerfile`, `package.json`, `scripts/verify-expected-counts.json` (regenerated by Tuesday at landing).
6. **NX-X, escaping sweep (RD-1014, RD-1015).** Reads and edits `static/js/index.js`, `first-run-setup.js` and `settings.js` across the whole page set (72, 82 and 11 interpolation rows, per RD-1014): it overlaps F1 and F2 on every file, so it runs AFTER both have landed, alone. Medium (security), Opus candidate for 1014.

Cross-lane exceptions: RD-396 also edits `backend/services/riskAlertScheduler.js` (NX-B owns `backend/**`; give that edit to NX-B or sequence); RD-515 edits `first-run-setup.html` (F1's file) from F2's banner-guard tests: sequence after F1; RD-1016 (settings.js) and RD-1014 (settings.js) are one file: 1016 first, inside F1; RD-145 and RD-745, 397, 918 need the Dockerfile: NX-T gives them; RD-1018's new cell is a plain-node cell in `__tests__/` loading `backend/marketplaceJwt.js` (read only).

### Actionable (80 keys), by lane

Scope text is the ticket's own title (trimmed to 150 characters); types are Jira's. The 11-11 sweep's per-key sizes and file lists remain the reference for the carried keys (every carried row is in its tables under the same lane names S, B, F1, F2, T).

**NX-S (server: backend/server.js and the files only it uses)** (7 keys)

| key | type | scope (ticket title, trimmed) |
|---|---|---|
| RD-974 | Bug | The automatic insights check for unusual print times gives a job with no Job_Start_Time the current time, so undated jobs count as off-hours when it r |
| RD-975 | Bug | The business-hours report reads created_at before the job's own start time, so a seeded row is judged by when the store was seeded and not by when it  |
| RD-893 | Task | PUT /api/risk-conditions/:id leaves its other fields unchecked (condition_text, is_active and email_recipients accept any type) and stores risk_level  |
| RD-896 | Task | Risk conditions stored with a mixed-case risk_level before PR #131 stay out of the High, Medium and Low lists and the alert mailer until saved again:  |
| RD-577 | Bug | Key Vault status reporting reads KEY_VAULT_NAME but the template sets KEYVAULT_NAME (server.js:631, :642, :17733) — every Marketplace deploy shows 'no |
| RD-1017 | Bug | AUDIT_ACTIONS.SETTINGS_CHANGE is used at backend/server.js lines 17353 and 17600 (add and remove a data source) and defined nowhere, so those two audi |
| RD-1021 | Bug | Two sibling routes still let a signed-in viewer make the server use stored data-source sign-in details: GET /api/setup/data-sources tests every enable |

**NX-B (backend periphery, no server.js)** (9 keys)

| key | type | scope (ticket title, trimmed) |
|---|---|---|
| RD-455 | Bug | SCIM provisioning: saving a group-mapping change without generating a new bearer token is refused (400 INVALID_SCIM_TOKEN), so every mapping edit rota |
| RD-744 | Bug | RD-685 C-F1: after a hard-link refusal, a changed or deleted inode on our name lets the LIVE re-drive certify 'purged' while the outside name keeps th |
| RD-745 | Bug | RD-685 C-F2/C-F3: a non-normalised DATA_DIR (trailing slash or ./data) makes two of our own names refuse each other forever; inside() and lstat mutant |
| RD-750 | Bug | RD-684 B-P1: one erasure ledger record lists the re-created feedback.json in BOTH filesPurged and filesFailed |
| RD-824 | Task | RD-640 L-A5: a store/copy link failing EACCES, EPERM or ENOTDIR keeps the erasure purged_incomplete forever; should ENOTDIR (a path through a file) jo |
| RD-728 | Bug | RD-628 G2 false-red when MACHINE_ID or WEBSITE_SITE_NAME is set in the runner env: scrub them; and 'read through this module only' is imprecise (batch |
| RD-759 | Task | CSP intake: userinfo still kept for a leading U+00A0/U+2028/U+FEFF, an @ only as %40, and data: with @ (gate 12 f1 unit shapes, after RD-735 round 2) |
| RD-578 | Bug | AzureADManager reads KEY_VAULT_NAME (never set) so its Key Vault init always throws on Marketplace deploys — correcting the name changes AUTH behaviou |
| RD-1023 | Task | The SCIM router writes two audit entries with the router-relative path, scim_rate_limited and scim_auth_failed (scimProvisioning.js lines 120 and 156) |

**NX-F1 (first-run, settings, login, entra-ui pages)** (11 keys)

| key | type | scope (ticket title, trimmed) |
|---|---|---|
| RD-117 | Bug | first-run-setup applies a CSP-blocked inline style — error on every load of the page a fresh customer deployment lands on |
| RD-188 | Bug | The first-run wizard violates the product's own CSP ~20 times per session — a style the product itself sets is refused by style-src-attr 'none' (P9-07 |
| RD-176 | Bug | Provisioning mode cards paint their ground from JS inline styles, so the dark fix has to win by !important — move them to the state classes the compon |
| RD-416 | Bug | First-run polish: opening User Access throws a page error (first-run-setup.js:3517), the page overflows 49px at 390px width, and configuration refusal |
| RD-151 | Story | Cost settings errors are shown as a page banner and the server's actionable `details` is discarded — render inline beside the offending field (P3-08) |
| RD-371 | Bug | RD-148 round-1 residuals F-4/F-5/F-6: revoke UI shows an unlabelled local-time date, has no live region and loses focus, and double-POSTs for a non-ad |
| RD-373 | Bug | N-3 + N-5: the still-live revoke warning is partly covered by the Feedback widget, and the revoke handler has two silent-return paths |
| RD-540 | Task | The PRECONDITION cell in rd465-first-run-open-window.test.js passes with the entire page script emptied - it asserts the fixture's own preset 'active' |
| RD-687 | Bug | First-run's danger status branches are unreachable: no caller passes 'error' to the data-source badge, and the component-check and final-validation el |
| RD-396 | Bug | RD-150 residue (gate F-2, F-3): red_flag_enabled stored as '' or 0 renders the Settings toggle OFF (settings.js:937) while the risk-alert scheduler st |
| RD-1016 | Task | static/js/settings.js defines escapeHtml twice (lines 93 and 2440) and the page uses the second, which returns an array or an object unescaped, so the |

**NX-F2 (dashboard page, css, e2e)** (17 keys)

| key | type | scope (ticket title, trimmed) |
|---|---|---|
| RD-144 | Bug | Dashboard tab strip has no tablist/tab/tabpanel semantics — WCAG 4.1.2 (SUS-10, pre-existing) |
| RD-351 | Bug | .tab-button has no project focus style — the UA default focus ring is now blue on a blue-adjacent ground after RD-251 (pre-existing, surfaced by the g |
| RD-164 | Bug | Dark mode's neutral card border #3a3a5a on #1e1e3f is 1.47:1 — below the 3:1 that the tinted variants in the same stylesheet are held to (WCAG 1.4.11, |
| RD-175 | Bug | P8-07: span.consumable-text is white on the light #e9ecef toner track at 1.19:1 in BOTH modes — dark-mode.css has no consumable rule; the designer's t |
| RD-222 | Bug | The wizard's ACTIVE step-number chip is white on a translucent-white composite at 3.74:1 in LIGHT, on all five tabs — measured and marked failing in p |
| RD-349 | Bug | #7f8c8d survives on three more selectors after RD-251 — and .metric-card .metric-label is JS-created dashboard KPI text at 3.48:1 that no static sweep |
| RD-220 | Bug | P11-07: console errors on every dashboard load, four families — three /api/normalized/* 503s, an empty high-risk query, CSP style-src-attr violations, |
| RD-259 | Bug | index.html reports 9 console errors on load (index-offline.html 1) — logged by QA pass 13b and deliberately not chased |
| RD-261 | Bug | brand-buttons.css is a single point of failure for the brand — if it fails to load, all 42 .btn-primary on 10 pages render Bootstrap #0d6efd permanent |
| RD-483 | Task | The open-access banner sits 24px (admin.html) and 32px (legal.html) below the top of the page instead of at the very top |
| RD-613 | Task | The storage-wiped alarm banner renders only on the dashboard: Settings, admin pages and first-run setup never fetch /api/status/persistence (S59 findi |
| RD-832 | Task | admin.html logs two '403 (Forbidden)' resource loads in open mode on a fresh install; the URLs were not captured |
| RD-512 | Task | RD-490 banner guard does not check the dark theme: the open-site banner's visibility and ink are measured in the default (light) theme only |
| RD-513 | Task | RD-490 banner guard measures one viewport (1366x900): phone-width concealment of the open-site banner is unguarded |
| RD-515 | Task | RD-490 banner guard does not cover the inline first-run open-site note (.nx-open-access-banner--inline) on the User Access step |
| RD-1026 | Bug | The chat page writes the tool-call status label (static/js/index.js line 3523) into the page as HTML and an AI endpoint can fill it: the review ran a  |
| RD-145 | Bug | All vendor CSS/JS loads from cdn.jsdelivr.net — in an egress-filtered tenant every icon disappears again (SUS-17, pre-existing) |

**NX-T (tests, scripts, CI, Dockerfile)** (34 keys)

| key | type | scope (ticket title, trimmed) |
|---|---|---|
| RD-134 | Task | All 12 schedulers had zero test coverage because requiring any scheduler under jest crashes at load (node-cron -> ESM-only uuid) — the blocker is now  |
| RD-249 | Bug | qa-surface-up.sh races itself on node_modules when two surfaces are stood at the SAME head — the second npm ci deletes the first's install and exits 5 |
| RD-320 | Bug | The erasure write-guard's corpus and runtime patch set are both vocabularies: three of four corpus members cannot fail its clauses, and nine fs routes |
| RD-345 | Bug | RD-340 residues from the round-3 gate: F21 the header + limits block still specify the round-2 reader, F22 default-import and .then wiring unseen, F23 |
| RD-348 | Bug | CI's gate depends on python3 and nothing declares it — RD-339's wrapper drives tests/test_normaliser.py through execFileSync('python3'), relying on ub |
| RD-352 | Bug | RD-341 QA-F4: four callee shapes yield neither a row nor a verdict - the label guard's docstring promises it FAILS LOUDLY on what it cannot read, and  |
| RD-355 | Bug | RD-341 QA-R2-F1: the label guard's second declared limit is over-general - it says an object-literal KEY write is skipped, but only { onSource: x } is |
| RD-353 | Bug | The launcher's Jira banner reports the PAGE CAP as a count: in-progress reads 100 where the true figure is 165, because jira_count pipes `jira issue l |
| RD-378 | Bug | The F-2 census's write detector follows a const/let declarator but not an assignment, a computed member, or an object-held alias of writeFileSync |
| RD-379 | Bug | The scheduler-vocabulary test's env restore is justified by a cross-file leak risk that jest's per-file process.env isolation makes impossible — and t |
| RD-384 | Bug | RD-376 gate findings F-1..F-5, all RECORD-LEVEL: the 'exactly two ways' reconciliation claim is five, entra-provisioning-ui passes against a reader th |
| RD-387 | Bug | RD-293 gate residue: the new seed warning has no guard, near-miss SEED_DEMO_DATA values are still silent, and two concurrent boots double-seed |
| RD-394 | Bug | RD-382 residue (gate F-1..F-4): JIRA.md's normalised recipes fail from the project root; the JIRA_SITE normaliser mishandles uppercase schemes, //, wh |
| RD-397 | Bug | RD-327 residue (gate N-1, P-1): build-commit-sha.sh calls a tree clean with plain git status --porcelain, so it stamps HEAD under showUntrackedFiles=n |
| RD-426 | Bug | Three suites fail under heavy machine load and pass alone: setup-rate-limit-allowance, erasure-health-branches and rate-limit-allowance failed 6 cells |
| RD-539 | Task | The RD-490 round-1 mutation harness cannot be reused as-is: 5 of its 15 anchors no longer exist against the round-2 guard, so a stale anchor edits not |
| RD-566 | Task | RD-561 gate residue (B-1..B-3): 'no env opt-out' has no cell; guard refuses -w2/--max-workers=2/--runInBand=true and accepts empty --maxWorkers=; JIRA |
| RD-572 | Bug | RD-568 residue: auth-gate-fail-closed leaks a legacy machine-id into the shared worker HOME; gate Lows A-1 (cell claims more than it checks) and A-2 ( |
| RD-580 | Bug | RD-342's gitleaks preflight has never run: the launcher reads preflight-gitleaks.sh from the stale 2_Project_Files clone (cd2b543), where it is absent |
| RD-586 | Bug | jira-query.sh --count returns a real-looking 0 (exit 0) for a status NAME that does not exist -- Jira's /search/jql answers HTTP 200 {} for an unresol |
| RD-595 | Task | rd523 and rd545 now require an RFC1918 interface on the test host and bind stand-ins on its real LAN address — deliberate for RD-516's trusted-stored  |
| RD-597 | Task | NEW-1's guard 3 cannot distinguish a connection refusal from an accept-then-reset: the openai SDK reports both as 'Connection error.', so the cell's t |
| RD-599 | Bug | RD-518 r3 H-01: the ANONYMOUS cell in rd518-r3-health-detail-decision measures a 401, not a redaction, and nothing now drives the open-window anonymou |
| RD-600 | Bug | RD-518 r3 H-02: the precondition cell reads roles via /api/auth/check, which bypasses the middleware, so it stays green with NO req.user — only the ad |
| RD-623 | Task | RD-524 gate-3 polish F-A3/F-A4/F-A6: READY overstated 'every M1 red behavioural', no cell for the feedback-attachments directory as evidence, 'Open Se |
| RD-668 | Task | Under jest the Key Vault SDK cannot load ('@azure/keyvault-keys not installed (Unexpected token export)'), so any suite reaching EncryptionService.ini |
| RD-726 | Bug | RD-696 cell 5 reds with EINVAL on a long TMPDIR (socket path over 104 bytes), and the 250 ms exit delay is unguarded: short socket base + an M-B2-shap |
| RD-757 | Bug | RD-591 g3: a FOREIGN connect-write-close dial reads 'vanished' and is COUNTED in a positive-arrival cell (rd549 O4/C2/C10 go green on a foreign dialer |
| RD-829 | Task | Gate 14 findings for RD-430 + RD-694 item 4: the manifest _about's '147 occurrences' total is false on today's tree (144), the READY named the wrong f |
| RD-918 | Task | RD-913 follow-up: sqlite3 6 arrives through an install script that npm 11.19 warns about on every install, and docker/Dockerfile.backend still builds  |
| RD-810 | Task | CodeQL baseline (test code, medium): js/file-access-to-http in tests/uat-run.js:30 - a file-read value is sent in the UAT runner's request |
| RD-1018 | Task | The committed cells for RD-445 mock the token library, so a weakened verification (the audience option dropped from the verify call, a widened flag te |
| RD-1024 | Task | RD-1011 and RD-1012 residue: no committed cell counts the stored-source read for a refused caller, none tests a role that is neither viewer nor admin, |
| RD-1027 | Task | RD-1008 residue: no committed cell turns red when only one of the five route-side class checks is reverted, none asserts the fallback answer on the PO |
**NX-X (escaping sweep, runs after NX-F1 and NX-F2 have landed)** (2 keys)

| key | type | scope (ticket title, trimmed) |
|---|---|---|
| RD-1014 | Bug | Values from outside are still written into the page as HTML or into quote-unsafe attributes after RD-861: scan file names, print-log user names, printer host names in data-arg (the review's census: 165 interpolations, none wrapped in an escape; 11 chat-region rows are RD-1008's and excluded). Recommendation: route attribute values through `escapeAttrValue`, element content through `escapeHtml`/`textContent`, people-fillable rows first |
| RD-1015 | Task | RD-835 residue: four CSV writers still write numeric cells (sheets, pages, size, two anomaly cells) without `csvCell` (`static/js/index.js` 5874, 6124, 5957, 5958, 5977, 6145); the leading-space and look-alike-character cases to be decided only after one real spreadsheet has opened a generated file |

### Sizes and gates (guess, to be confirmed by the kit drafter's own reads)

NX-S: RD-1021 M, G1 Opus; RD-974, 975, 893, 896, 577 S, G2 (RD-974/975: PR #198's body says "Not in this change: RD-974 and RD-975", red-first recommendation given); RD-1017 S (choose: add the key, or point at an existing tag; the ticket says to state that a new tag changes what the audit export's action filter returns). NX-B: RD-744, 578 Opus; RD-455 M (the same files as RD-405's residue; not RD-405); RD-1023 S (copy the `requestPath` import form of `entraProvisioning.js`; read the existing cells first, one may pin the old relative path; note the file is `backend/services/scimProvisioning.js`, the ticket's `scimProvisioning.js lines 120 and 156` read there, not under `backend/routes/`). NX-F1/F2: mostly S to M, G2; RD-145 L, last. NX-T: S each, G2; RD-134 L.

## 3a. NexusAI: conditional (not counted: investigate first, or a choice the ticket leaves open)

| key | why conditional | first step an agent can take |
|---|---|---|
| RD-1019 | "a question, not a defect claim": does the global sign-in check let Microsoft's Marketplace webhook through on a sign-in-enforced instance (`server.js` list from 2223, check at 2905, router mounted at 22491)? | run it: server on a loopback port, correct HMAC and a loopback-signed bearer token, no cookie, read the status; only then decide an exemption (an exact-match set like the one at 2656), which touches the auth gate |
| RD-1022 | "Does a signed-in viewer make the server use the stored primary workspace's sign-in details through five routes?" | boot with the review's outbound-connect fence, call as a seeded viewer; if a route connects, "decide with the product owner whether a viewer is meant to run it" (Kam's) |
| RD-1020 | boot-time refusal when `MARKETPLACE_SKIP_JWT` is true and `NODE_ENV` is not development/test: "decide the allowed values ... whether to remove the flag altogether" | adds a refusal or FATAL line operators see; a small design choice, default: refuse to mount the router |
| RD-1029 | `/api/ai/status` returns an endpoint's own error text in `details.error` | fixed short reason changes what the setup wizard shows (new words): needs the words check |
| RD-763, RD-764 | CodeQL judgement tickets in `server.js`: "read first; fix or record the reading for Kam; no ruling needed to start" (11-11 sweep) | a read-only reading document |
| RD-1006, RD-1009, RD-1010 | census first (every `auditLog(` site; 30 route handlers over HTTP), then a per-handler fix of the RD-1007 shape; RD-1006's cap was "option (a) of the product owner's" ruling (read the ticket first) | the census is an agent job; fixes follow it |

## 3b. NexusAI: excluded (with the reason)

- **Landed on main, records only (move to Testing, comment): 11 To Do keys**: RD-538 (#203), 563 and 969 (#198), 729 (#218), 826 (#202), 970 (#192), 731 (#194, partly: 13 of 14 suites), 972 (#195), 929, 977, 978 (#197). Pickup lines 754 and 111 name the next records pass.
- **Held, needs a ruling or Kam**: RD-805 and RD-768 (CodeQL alerts left open by design; "file mode change is visible to the product"), RD-1025 (needs the product owner's word before any build: the open window after an administrator reset), RD-1028 (design choice: no fix shape), RD-433 (SEED_DEMO_DATA guard: ruled, but the banner words are new and go to the owner first), RD-610, 612, 622 (needs-decision, words), RD-644 (post-resubmission), RD-522 (cross-cutting scrub, "run LAST, alone", a scripted clean-up with its own review), RD-884, 546, 193, 583, 584, 305, 313 (product or policy choice, carried from the 11-11 exclusion list).
- **Needs a client or a customer-facing word**: RD-702, 636 (first-run text on encryption at rest), RD-1029 (see above), the roles-UI chain RD-937 to 957 (held on word rows; 35 To Do keys carry the `roles-ui-2026-11` label).
- **Not agent work**: epics RD-6, 7, 8; business, hiring and compliance RD-13, 20, 21, 22, 28, 29, 30, 31, 34; Azure, secrets and other projects RD-50, 54, 55, 83; Jira and session tooling RD-233, 287, 449; marketplace-labelled Partner Center items RD-414, 415, 467, 468, 469, 473 and the rest of the 26 `marketplace` To Do keys; feature requests RD-146, 400, 401, 842. (RD-353 and RD-580 are launcher-side scripts under `scripts/`; they are counted in NX-T, not excluded.)
- **In Progress (8), Put on Hold (7), Declined (2)**: RD-49, 81, 427, 431, 432, 450, 643, 662; RD-18, 32, 33, 41, 93, 104, 743; RD-300, 564 (titles read; the three 2026-09 plans RD-427, 431, 432 are stale and "whether they merged" is UNMEASURED).
- **RD-1004** (picomatch audit exception, re-check by 2026-12-18) and **RD-1001** (stale `core.sshCommand` on the records working copy: a configuration write that belongs to the launcher).
- **Testing 310 and Release Ready 199**: not work.
- **The other To Do keys (about 280: the `operations`-labelled residue and QA-gate findings that the 11-11 sweep classed "not individually examined" or "needs a decision")**: not re-read; UNMEASURED beyond titles for this sweep.

## 4. Questions for Tuesday (each with a default)

1. **PCOMP-36/37 under the reviewer-round hold.** The plan reads C-92 "Permits now: L1 and L2 may be built and merged on branches" as releasing them; PCOMP-36 can close only for the 34 typed boolean fields. Default: build CW-2 as planned on main `3638da61`, no sentence in the file, G2 gate, and say at the gate whether 36 closes on the cut. A deploy stays refused (pickup top).
2. **MPSCALC-427 needs the catalogue's part-code lengths from the local pricebook store.** Default: the builder prints lengths only, from the gitignored store, never a price; if the store is unreachable the lane builds the CSS rule and the 60-character PDF check and reports the lengths as UNMEASURED.
3. **MPSCALC-272 and the other words-pending lanes** (same shape as #219 and #221, built on pending words, words on the deploy card): default per the 11-20 sweep: yes, per lane, nothing deployed.
4. **NexusAI queue order.** Default: N-L (NX-F2 first rows RD-349, 175), N-O (RD-759, in NX-B), then RD-1021 (NX-S, the pickup's "next security lane") and RD-1026 (NX-F2), then NX-T residues; NX-X last. One NexusAI seat at a time (jest lock).
5. **The permission-table ticket** (pickup lines 111, 214) is still not filed; it belongs to NX-S's files and to the next NexusAI records seat.

## 5. How measured, and NOT tested

- Instruments: paginated Jira `search/jql` (GET, page size 100, 0.25 s apart, credentials read in-process from each project's `4_Credentials/.env`, never printed), `board_count.sh` through `bc.sh`; `gh api -X GET` for mains, PR lists, PR bodies, tree lists and file reads under each project's own `GH_CONFIG_DIR`; `/usr/bin/grep`, `comm`, `awk`.
- **Not tested:** (a) the 159 unmoved MPS and 77 Composer tickets and about 280 NexusAI To Do tickets were not re-read for text, only for `updated` stamps and key lists; their classes are carried and say so. (b) Of the 80 RD keys only 8 were re-verified against origin main (RD-144, 145, 117, 188, the 893/892 guard, 577, 1017, 1021); the others carry the 11-11 deep read plus the landing screen by PR title and body. A PR body can name a key without building it (RD-974, 975, 768, 805 were named under "Not in this change"): those four are therefore NOT treated as landed, the five title-named keys are. (c) The merged-PR screen read 100 PRs by `updated`, the 30 code PRs' bodies, and not commit messages or branch-only work: a local-only built branch (the 11-11 sweep named four) is unmeasured. (d) Composer: `content/baselines/` absence and the `git ls-tree` of main `3638da61` were not re-read here (the plan's claim was at the old main). (e) No test, build, server, deploy or browser was run; every "real browser" or "run it" step is the builder's. (f) `PCOMP` labels and statuses are read from the dump only. (g) The 11-20 evening sweep's 4 MPS lanes M-1..M-4 are all done; none re-proposed.
- Disclosures: no write outside this file and the scratch folder `fleet/state/s308/sweep/` (which holds the dumps `MPSCALC_*`, `PCOMP_*`, `RD_*`, key lists, the merged-PR list, a copy of `backend/server.js` and `static/index.html` at main `8858e5d1`, and the copied GET-only scripts); no Jira or GitHub write; no deletion.

READ-WHOLE-BY-TUESDAY: ____
