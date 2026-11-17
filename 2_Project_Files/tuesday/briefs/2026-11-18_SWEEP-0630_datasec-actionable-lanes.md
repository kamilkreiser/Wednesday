# SWEEP-0630: Datasec tickets agents can build now, in lanes (read-only sweep, 2026-11-18 early morning)

Written by a read-only sweep drafter from 06:09 to about 06:20 AEDT (`date` read 06:09:17 at start, 06:18:32 near the end). Form and instruments copied from `2026-11-17_SWEEP-2025_datasec-actionable-lanes.md`: the GET-only scripts `jqdump.py`, `jdesc.py`, `jcom.py`, `rg.sh`, `bc.sh` were copied into `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s288/sweep0630/` (the only place written besides this file; dumps, ticket reads and trees are there). Fences kept: no Jira write, no GitHub write, no git write, no push, no mail, no `az`, no deploy, no `cd`, no token printed, no `decision_queue.sh`, no hosted HTTP, nothing under Secuura, WEDNESDAY or FRIDAY read.

**Standing constraint this morning (given in the commission, not measured by me):** the new picomatch advisory GHSA-fc5q-39xc-vjpf (no fix) makes NexusAI's production `npm audit` and HPSM-POC's dev-tools audit fail on every new PR until Kam rules (card `nexusai-picomatch-advisory-audit-1118`). So NexusAI and HPSM lanes can be built and gated but not merged. MPS and Composer are not blocked.

## BLUF

**4 firm keys in 3 lanes on 2 projects, plus 1 conditional key: HPSM-POC 0 keys (0 lanes), Security Composer 0, MPS Calculator 1 firm key (MPSCALC-364) plus 1 conditional (MPSCALC-316) in 1 lane, NexusAI 3 keys (RD-980, RD-717, RD-749) in 2 lanes, Vision 0 (paused, not swept).** Everything the SWEEP-2025 lanes proposed is landed or held; nothing from them is re-proposed. The two project boards that were nearly empty last night stay nearly empty: new work came only from reading tickets the earlier sweeps carried unread (the MPS records notes of 2026-11-11 and the NexusAI test tail).

Recommended order (section 9, at most four): **1. M-D4** (MPSCALC-364, then 316 if Tuesday confirms; MPS, not blocked, can merge). **2. NX-L** (RD-980, test-only; waits to merge). **3. NX-M** (RD-717 and RD-749, test-only; waits to merge). Composer and HPSM-POC have no lane to rank. NX-L and NX-M are in one repository and share `scripts/verify-expected-counts.json` and the jest lock: one NexusAI seat at a time. NexusAI PR #220 (RD-689) and #219 (records) are already built and are waiting to merge: they are not lanes.

**Feedback sweep (standing boot rule): NOT MEASURED for Composer and NexusAI.** Neither live store can be read inside these fences (NexusAI's is a file on an Azure share read by a script that needs `az`; Composer's is the hosted app's database, read through a VM command; both are fenced; the tuesday-agent mail inbox is fenced as "no mail"). The only signals read were Jira: no new feedback-shaped ticket since 2026-11-17 20:00 in either project (section 6). That is "no ticket", not "no feedback".

**`lane-v` read-first classifier (12 of 48 read):** 1 is small and buildable now (MPSCALC-364, a developer-docs correction ruled on 11-11), 1 more is conditional (MPSCALC-316). The other 10 are landed-and-waiting-records (297, 306), need a decision or new words or a design (310, 314, 288, 233, 368, 315, 237), or are a larger test build (251). Section 7.

### Board census (measured)

Counts are `board_count.sh jira` through `bc.sh`, JQL `project = <KEY> AND ( ... )`; every line printed `limit was 5001, so this is a real count and not a cap`. The same sets were dumped with the GET-only `jqdump.py` (`unique` equalled `rows` in all eight dumps). Control that can fail: open + Done = created since 2000 in all four.

| project | open now | open at SWEEP-2025 | change by `comm` of the key lists | by status (measured) | buildable keys | lanes |
|---|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 146 (362 Done; 146 + 362 = 508 = count since 2000) | 148 | HPSMPOC-507 and 508 left (Done, #333 and #332); none new | 143 Backlog, 3 In Progress (87, 90, 91) | 0 | 0 |
| Security Composer (PCOMP) | 81 (48 Done; 81 + 48 = 129) | 81 | none; 0 created and 0 updated since 20:00 | 81 Backlog | 0 | 0 |
| MPS Calculator (MPSCALC) | 165 (245 Done; 165 + 245 = 410) | 165 | none; 0 updated since 20:00 | 165 Backlog | 1 firm + 1 conditional | 1 |
| NexusAI (RD) | 870 (129 Done; 870 + 129 = 999) | 869 | RD-1003 new; none gone (RD-995, 1002, 734, 730 moved to Testing and are still open) | To Do 360, Testing 294, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 | 3 | 2 |
| Vision Sales Portal | not re-swept | 16 (06:00 on 11-17) | not read | paused | 0 | 0 |

Status arithmetic (a check that can fail): NexusAI To Do 363 to 360 is minus 4 (RD-995, 1002, 734, 730 to Testing) plus 1 (RD-1003); Testing 290 to 294 is plus 4. Both read right. "Open at SWEEP-2025" is that file's census (RD 869 from its 20:31 re-dump).

Origin state (all `gh api -X GET` under each project's own `GH_CONFIG_DIR`, read today): HPSM-POC main `36c557ad` (#333, 2026-11-17T11:35:33Z), 0 open PRs; MPS `125f7a52` (#209, unchanged), 0 open PRs; Composer `b4681297` (#130, unchanged), 1 open: draft #85 (HOLD K6); NexusAI `2de5e84c` (#218, 2026-11-17T16:12:54Z), 2 open PRs: #220 `b1683/nexusai-lane-nx-c-stale-comments` (RD-689; files `__tests__/rd385-shipped-root-markdown-identifiers.test.js`, `backend/server.js`, `backend/services/schedulers/healthSweeperScheduler.js`) and #219 `records/b1684-history` (`HISTORY.md` only). Control: `state=closed` printed each project's latest merges (HPSM #333 to #329; MPS #209 to #205; Composer #130 to #127; NexusAI #218 to #214). NexusAI open code-scanning alerts on main: 22 (`length` of one page, list under 100), same count as SWEEP-2025; never dismiss one.

Standing line for every HPSM kit (no HPSM lane is proposed, so it is only carried): this phase builds no integration with HP tools; nothing deploys.

### Lane table

| lane | project | keys | owns (code repository paths, line numbers printed today at main) | model row, gate | size | merge |
|---|---|---|---|---|---|---|
| M-D4 | MPS | MPSCALC-364 (firm); MPSCALC-316 residue (conditional, step 2) | `docs/API.md` (382 to 383), `docs/api/openapi.json` (1509), `web/src/api/generated/openapi.snapshot.json` (1509), `web/src/api/generated/schema.ts` (1520), `src/MpsCalc.Api/Contracts/Dtos.cs` (comment, 466); step 2 adds `docs/api/openapi.json` (988, 1036), `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (1436) and `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs` (235) | Sonnet, C2 (`model-routing.md` line 92), G2 (line 109); step 2 is a customer-visible refusal sentence, so Tuesday may raise it to G1 (line 108) | S (step 1); S (step 2) | free to merge |
| NX-L | NexusAI | RD-980 | `__tests__/rd798-log-injection-chat-and-learning.test.js` (434 to 439, 489 to 499, 529 to 535), `__tests__/rd799-log-injection-auth-and-storage.test.js` (287, the cell title; read first), `scripts/verify-expected-counts.json` only if a cell is added (it is `tests` 5870, `suites` 377 at lines 4 and 5) | Sonnet, C2 (line 92), G2 (line 109) | M | waits (audit) |
| NX-M | NexusAI | RD-717, RD-749 (read first) | `__tests__/rd681-clear-undecryptable-key.test.js` (cells at 100 to 119), `__tests__/rd684-redrive-keeps-surviving-target.test.js` (describe at 109, cells F1 to F6b at 110 to 236), `scripts/verify-expected-counts.json` | Sonnet, L6 (line 85) fallback, else C2 (line 92); G2 (line 109) | M | waits (audit) |

Model ids and rows as in SWEEP-2025 (rows unchanged; line numbers printed today by `awk NR` over `fleet/specs/model-routing.md`: L3 line 82, L6 line 85, C2 line 92, C3 line 93, G1 line 108, G2 line 109, G3 line 110). Spark is not this seat's (pickup top), so the L-rows run on Sonnet (the "esc" column). Ports: none requested.

## 1. HPSM-POC (HPSMPOC): 0 buildable

Open 146 (143 Backlog, 3 In Progress: 87, 90, 91, Kam-owned C-30 items). Main `36c557ad`, 0 open PRs. HPSMPOC-507 and 508 are Done (#333, #332); no new key since SWEEP-2025 (`comm` prints nothing new). No key was found that is small, ruled, and free of a decision. Read today and why each stays out:

- **HPSMPOC-470** (four open points): point 3 landed in #327 (comment 41295); points 2 and 5 are "not decided" (comments 41295, 41128); point 4 was diagnosed and "no test change was built" (comment 41277); point 1 (the a11y journey test near its 30 s limit) names no fix and "built or recorded as declined" is the done-when: a choice, not a spelled-out change.
- **HPSMPOC-408**: items 1 and 3 landed in #265; the open half (the three limits as real sentences) is words for the product owner (records comment of 2026-11-11 20:12: "held for the product owner").
- **HPSMPOC-357, 431**: the layout half is landed (#244, #278) and the tickets wait on a UAT measurement (hosted), not a build.
- **HPSMPOC-246, 228, 207, 343, 503**: each is either "ruled; waits on a deploy seat", a hosted observation, a diagnosis ("find the cause first; propose no bound"), or landed with only a records move left.
- Excluded as in SWEEP-2025 and unchanged: the 21 HTML-phase keys (`fleet/state/s279/sweep1925/hpsm_html_all.tsv`, 21 rows; control: HPSMPOC-464 is in it, 1 hit; HPSMPOC-408, 470, 431, 357, 246, 228, 207, 343, 506, 406, 428, 315 are not, 0 hits each), the held and awaiting-HP keys, the deploy-round keys (497 to 502), HPSMPOC-356 (held on card `hpsmpoc-356-residue-not-wanted-1117`; see section 8).

## 2. Security Composer (PCOMP): 0 buildable

Open 81, all Backlog, key set identical to SWEEP-2025 (`comm` prints nothing in either direction); main `b4681297`; draft PR #85 (HOLD K6) stays held. 0 tickets created or updated since 2026-11-17 20:00. Read today: PCOMP-74, 80, 81 (the style leftovers ruled on 2026-11-11 "Yes to all three"): the change they wait for is **already on main** as commit `5d3bf82d` (2026-11-11T09:13:06Z, "The white is one named style value, and the withdrawn list's setting key takes the code-style font"; `--pc-on-primary` is at `apps/web/src/styles/tokens.css:16`, and a pattern scan for `#fff`/`#ffffff` over all nine other stylesheets under `apps/web/src/styles/` and `apps/web/src/feedback/feedback.css` printed no literal, control: the same scan hit `tokens.css:15` and `:16`). These three are a records move to Done, not a build. PCOMP-123 and PCOMP-23 (change report footer; the policy-PDF half would edit `packages/renderers/src/document-pdf.ts`, which the held #85 also touches; "whether the ticket is Done is not ruled"), PCOMP-13 and 16 (environment; closed or ordered by the coordinator, not a seat build), PCOMP-65 (a Note, nothing to build), PCOMP-7 and 8 (superseded or built), PCOMP-70 and 71 (held, the owner's call), PCOMP-78 (ops, "Yes, at the next deploy": a deploy item). Carried excluded: the `held` family and the sample-policy-document content keys (PCOMP-29 to 61), PCOMP-46 and 94 (`needs-kam`), PCOMP-66 and 67, PCOMP-128 and 129 (words).

## 3. MPS Calculator (MPSCALC): 1 lane

Open 165, all Backlog; main `125f7a52`; 0 open PRs. Key set identical to SWEEP-2025 (so MPSCALC-410 and 207 are still open and still held on card `mps-410-openapi-195-wording-1117`). Pricebook values are confidential: none appears here.

### Buildable now

**M-D4: MPSCALC-364** (published sentences about the four staff list columns say no row carries them). The product owner's 2026-11-11 ruling (comment 41072, record entry C-109) says developer-only docs "are written from what the code does and do not go to the product owner's word review"; this ticket was named in it as exactly that case ("Not built: the corrected sentences are queued with their own review"). Printed today at main `125f7a52`:
- `docs/API.md:382` to `:383`: "... Until lane V2 fills them no row carries them."
- `docs/api/openapi.json:1509`: the `oneOffGp` description ends "... and until the Home work fills it." The same text is at `web/src/api/generated/openapi.snapshot.json:1509` and `web/src/api/generated/schema.ts:1520`.
- `src/MpsCalc.Api/Contracts/Dtos.cs:466`: a code comment, "Absent until lane V2 fills them, and for a quote that has no calculation."
- What the code does, printed: `src/MpsCalc.Api/Quotes/QuoteFigures.cs:125` to `:128`: purchase carries `HardwareProfit`, nothing for the per-year figure, `PurchaseTotalExTax`, `DealProfit`; rental carries only `Portfolio?.ContractValueExTax` (the TCV); the comment at `:121` to `:123` says the per-year and whole-term figures wait on result fields (lane V4, MPSCALC-315).
- The web copies are generated from the contract by `web/scripts/sync-contract.mjs` (its header, printed: "Copies the API contract from a git ref into src/api/generated/ ... this script never edits it"), so the builder edits `docs/api/openapi.json` by hand and then runs that script against its own commit; the snapshot and `schema.ts` are its output. The builder reads the script's usage from its header, not by running it first.
- Why no ruling: the product owner's 11-11 ruling covers developer-only text. **One caution for Tuesday:** `docs/api/openapi.json` is the same file the held card `mps-410-openapi-195-wording-1117` asks about (whether the contract's clause at the MPSCALC-410 line changes). That card concerns a different line, but if Tuesday reads the held card as "no change to `openapi.json` wording until Kam answers", M-D4 waits. I did not read the card (no `decision_queue.sh`).
- Red-first for a docs change: a before-and-after count of the old phrases over the five files (`/usr/bin/grep -i -c 'no row carries'` and `'until the Home work'` with a positive control on the unedited file), and the project's contract test that compares the snapshot to the contract (the ticket MPSCALC-316 comment 40096 says it exists: "contract test 1 passing"; name UNMEASURED).
- Size S. Owns the five paths above only.

**Step 2, conditional: MPSCALC-316 residue.** Comment 41071 (record entry C-108, 11-11): the product owner accepted all four docs/words corrections incl. this one; "the agreed sentence (at most 100 characters, an emoji counts as two) is to be used in the remaining places that comment 40472 lists." Printed today: `docs/api/openapi.json:988` and `:1036` hold `"maxLength": 100` for `quoteRef` (the second with a description that has no unit sentence); `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:1436` holds `errors.Add("quoteRef is at most 100 characters and customer at most 200.");` and the test that pins it is `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs:235` (found by a GET code search, 2 hits, both files above). `docs/API.md:440` already carries "at most 100 UTF-16 code units (an emoji counts as two)". Whether the agreed sentence reaches the code's refusal text is Tuesday's reading (the 2026-10-24 ruling said "no code change"; the 11-11 acceptance says "remaining places that comment 40472 lists", and 40472 lists the `QuoteEndpoints.cs` sentence). It is customer-visible (an API error body), so it is a G1 candidate; I propose G2 only if Tuesday reads it as already-agreed words. If not, do step 1 only.

### Excluded (MPSCALC), with the reason

- **Held on cards for Kam (see section 8):** MPSCALC-410, MPSCALC-207 (card `mps-410-openapi-195-wording-1117`), and MPSCALC-195 (its clause wording; same card by the commission's words).
- **Landed and waiting a records move, not builds:** MPSCALC-306 (overflow fixed in #91, gate B354), 297 (#90, #91), 130 (style half in #178), 162 and 163 (landed; 163's "20 group runs under load" is a measurement, not a build), 170 (#196 built the id; stays open on the 195 docs sentence), 189 (clause 5 is a docs sentence on `docs/API.md`: the same file as the held 410; carried).
- **Needs a refusal sentence or a name (words) before a build:** MPSCALC-233 (ruled "Refuse" on 11-11, but "the refusal and its rows are queued with their own review"; the new refusal text has no recorded approval), 288 (option a chosen: a new `callerCan.reject` member "and new words"), 368 (a field name is proposed for approval), 237 (new status and fields).
- **Open choice or a design:** MPSCALC-314 (a longer interval, a minimum gap, or server-side coalescing: "has not been ruled"), 310 (a seam or accept a mutant: "needs a product decision"), 315 (a result field and a register row first), 251 (clause 3 met; the sign-in leg is "not built": a larger test build, read first), 135 (the stub and no-API legs of the smoke journey are red; "not built"; a build that needs a seam in the dev stub, so not a spelled-out change).
- **Carried unchanged from SWEEP-2025:** 369 (a record, not a Done), 372, 395 (hosted), 224, 223, 222, 226 (hosted or rollback decisions), 194, 169, 118, 110, 139, 316's `needs-ruling` label is left as is (no label edits).
- **The seed epics and tasks** (`spec-seed`, `plan-E01` to `plan-E14`, `mpscalc-seed-2026-09-30`): plan headings, not agent tickets.
- MPS Calculator **feedback** is excluded by Kam's 2026-10-12 rule (section 6).

## 4. NexusAI (RD): 2 lanes (3 keys), build-and-gate only until the audit rule lands

Open 870 (To Do 360, Testing 294). Main `2de5e84c`; open PRs #220 (RD-689, built, waiting to merge) and #219 (records, `HISTORY.md` only). Not re-proposed: RD-995 (#216), RD-1002, RD-734, RD-730, RD-729 A-F1 (#218), RD-689 (#220). New since SWEEP-2025: RD-1003 (`needs-decision`; held on card `nexusai-rd1003-action-route-signin-1118`).

### Buildable now (waits to merge)

**NX-L: RD-980** (the log-sink test files: four weaknesses, all in test code). Ticket text read today (no comments on it: `jcom.py` printed `total 0`): one test-only change, red first, then an independent review. Printed today at main `2de5e84c`:
- `__tests__/rd798-log-injection-chat-and-learning.test.js:436` is the job-line mask the ticket names (`.replace(/^( {3}• )\S[^\n]*?( - \d+ sheets \()/gm, '$1<local-time>$2')`), inside `clockMasked` at `:434`; the cells it feeds: `C-BODY-HOURS LIVE` at `:467`, `IN 198 201` at `:484`, `OUT 198 201` at `:489`, `IN 190` at `:494`, `OUT 190` at `:499`; the mask's own cell `MASK-JOB-TIME` at `:529`; the route 190 masks at `:437` and `:438`.
- The harness takes a per-cell `env:` (`:138`, `:215` pass `env: { SEED_DEMO_DATA: 'true' }`), so item 3 (set `LC_ALL` and `LANG` for the server child) needs no harness edit, only the cell's env. Not measured: whether a locale env is enough to turn the 12 cells red under another locale (the ticket's number, relayed).
- Item 4 (retitle a cell): the ticket says line 272 of `__tests__/rd799-log-injection-auth-and-storage.test.js`; at main the line has moved (`:270` is cell `S-171`). The cell about the state lines and MISSING is `:287` (`C-PLAIN 169 and 170 - the state lines print the first 8 characters, the full state, and MISSING for an absent cookie`). The builder finds the stale title by text; I did not decide which cell the ticket meant.
- Why no ruling: "(a proposal, not decided)" is the ticket's wording for the fix shape, but every item edits test code only, the ticket asks for no product change, and where it offers two options (item 2: freeze one value per state with masks removed, or drop the two masks) the builder takes the first listed and says so in the PR text. A change in a test's expected value is not at stake: the plants must turn red.
- Size M. Gate G2 (tests only). The counts file moves only if a cell is added (the negative plants may be rows of the existing `MASK-JOB-TIME` cell, per the ticket).

**NX-M: RD-717 and RD-749** (test gaps, read first). Both are Minor test-coverage tickets filed by the 2026-09-28 gate batches with explicit fix shapes and no product change.
- RD-717: "cells that each redden one of M-A1..M-A4, in particular one that reads settings.json raw after the route answers". The suite is `__tests__/rd681-clear-undecryptable-key.test.js` (exists at main; `describe` at `:100`, cells at `:101`, `:107`, `:111`, `:115`; the audit helper at `:98`); the product route is `backend/server.js:16577` (`storedAoaiFields`) to `:16608` (`auditLog(AUDIT_ACTIONS.AI_CONFIG_CLEARED ...)`), printed today and not edited.
- RD-749: "one cell per mutant in the RD-684 re-drive suite, each red under its mutant and green on main", mutants M-B4 (only ENOENT resolves), M-B5 (dedupe), M-B6 (the early read), M-B7 (the live push's field). The suite is `__tests__/rd684-redrive-keeps-surviving-target.test.js` (exists at main; `describe` at `:109`, cells F1 `:110`, F2 `:124`, F3 `:136`, F4 `:165`, F6 `:213`, F6b `:227`, F5 `:236`).
- **Read first, and a stop condition:** both tickets are dated September and point at older branches. At main a mutant may already be killed by a later change; the builder plants each mutant on a scratch copy and keeps a cell only if the mutant is green today (that is the ticket's own acceptance). A mutant already red at main is recorded as "already guarded" and dropped. The product line numbers of RD-684's code were not located here (UNMEASURED).
- Why no ruling: test-only, red-first, nothing customer-visible. Not in this lane (read, found unbuildable): RD-728 and RD-726 name test files (`rd628-two-machine-id-derivations.test.js`, `rd696-listen-failure-remedies.test.js`) that are **not in the main tree** (a list of 1,042 blobs has neither; the neighbours `rd568-harness-one-machine-identity.test.js` and `rd533-listen-error-fails-loudly.test.js` are present, so I did not guess); RD-727's file name is cut off in the text I read (`rd646-647-redis-fail-clo...`) and the main tree lists no `rd646` or `rd647` test file (a pattern over the tree printed only helpers `rd607-fake-redis.js` and `rd607-redis-limiters-keep-their-own-counts.test.js` for redis); RD-724 is a marketplace package test port; RD-908 was decided 11-03 ("leave as a standalone change ... rides with the next change to `rd891-probe-name-race.test.js`"); RD-911's last half is a choice "the product owner decides between two things".
- Size M. Gate G2 (line 109). Shares `scripts/verify-expected-counts.json` and the single jest lock with NX-L: one seat at a time.

### Excluded (NexusAI), with the reason

- **Held on cards for Kam (section 8):** RD-994 (NX-A), RD-1000, RD-1003, and the picomatch advisory.
- **Needs a decision or a reading of production behaviour:** RD-974 and RD-975 (what an undated job counts as; a report's figures change; "a proposal, not decided"), RD-981 (a transaction race in `backend/simpleDb.js:620`; the ticket "needs an independent review and a decision on whether any caller of this method reaches production"), RD-967, 969, 966 (500 and 403 answers on routes; "find what ... needs"), RD-972 (landed in #195, a verify-and-move note), RD-977, 978 (landed in #197, a verify-and-move note), RD-970 (landed in #192, a hybrid choice for the reader), RD-983 (landed in #208).
- **Roles UI family** (RD-930 to 957, `roles-ui-2026-11`): designs, new words and a word pack first (RD-934). Not agent lanes today.
- **Carried unchanged:** RD-1001 (launcher write), RD-997, 990, 989 (design decisions on routes and pages), RD-768, RD-405, RD-731, RD-757, RD-740, RD-984, RD-742, RD-605, RD-930, 931, the erasure family (RD-744, 745, 750, 824: row C4, Opus), the demo hold (nothing deploys), Testing (294) and Release Ready (199) are not work, the 7 Put on Hold and 8 In Progress keys.
- Not read, so not counted: the other 70-odd `qa-gate-finding`, `operations` and `tests` To Do keys the label scan lists (82 To Do keys match `test|qa-gate|flaky|tooling|test-infra`; 10 were read today).

## 5. Vision Sales Portal: excluded whole, not re-swept

The 2026-09-29 pause stands (lesson `2026-10-12_boot-sweeps-all-feedback-repositories.md`: lifted for QuickQuote FEEDBACK work only) and the product is production. Not read.

## 6. Feedback items (the standing boot rule)

Where feedback lands, from each project's own docs, read today:

- **NexusAI:** `settings.json['feedbackItems']` on the Azure file share `nexusai-data` (storage account named in `2_Project_Files/scripts/feedback-sweep.sh`); `CLAUDE.md` "Boot-time feedback sweep" says run `cd 2_Project_Files && ./scripts/feedback-sweep.sh`. The script reads the share with `az storage file download` (its own header: "az storage file download to a temp dir, plus Jira GET searches"). **`az` is fenced for this sweep: the store was not read. This is NOT "0 items".** Jira signal only: `project = RD AND ( summary ~ "\"Feedback #\"" )` prints 26 rows (the match is loose: the `#` is dropped, so it matches any "feedback" word); the same query narrowed to created or updated since `2026-11-17 20:00` prints 1 row, **RD-1003**, a ticket about the feedback router's internal action route (an engineering item, held on a card), not a feedback submission. So: no new feedback ticket since 20:00; the store itself unmeasured.
- **Security Composer:** the project has a Feedback widget and admin screen (`apps/web/src/feedback/FeedbackWidget.tsx`, `feedback-admin.spec.ts`; `BACKLOG.md` rows 41, 73, 75, 82), but its own `CLAUDE.md` has no feedback section (0 matches) and I found no sweep script. The 2026-10-16 sweep records the store as needing `az vm run-command` and says the GET writes audit rows (`0_Brain/projects_index/2026-10-16_feedback-sweep-2.md`). **Not read (fenced). Not "0 items".** Jira signal: `summary ~ feedback OR labels in (feedback, user-feedback, in-app-feedback, hp-feedback)` prints 0 rows over the whole project (positive control on the same account and JQL form: `summary ~ guided` prints 17 rows; `/usr/bin/grep -i -c feedback` over the open and Done dumps prints 0 and 0), and 0 tickets were created or updated since 20:00. So: no feedback ticket exists; the store is unmeasured.
- **Excluded by Kam's rule, not read:** HPSM-POC feedback, the Security Configuration tool, the MPS Calculator feedback (his 2026-10-12 12:01 words; the lesson says "at the moment" and keeps the exclusion until he says otherwise).
- **Mail** (the `tuesday-agent@` inbox receives copies for the Vision stores) was not read: "no mail" is a fence here.

## 7. The 48 `lane-v*` MPS keys: a 12-key read-first sample

Counts: 48 open keys carry a `lane-v*` label (measured by label match over `mps_open.tsv`: `/usr/bin/grep -c lane-v` prints 48, same as SWEEP-2025; 2 of them also carry `needs-ruling`: MPSCALC-316 and 261). I read 12 and did not classify the rest.

| key | what I read | small, self-contained, no new words, no ruling? |
|---|---|---|
| MPSCALC-364 | developer-docs sentences stale against `QuoteFigures.cs:125` to `:128`; the 11-11 ruling covers developer-only text (comment 41072) | **Yes** (lane M-D4) |
| MPSCALC-316 | the unit sentence is built in `docs/API.md:440`; the agreed sentence still owed in 3 places (comment 41071) | **Conditional** (step 2 of M-D4; the refusal sentence is customer-visible) |
| MPSCALC-297 | landed in #90 and #91; its last clause is blocked by 135 (comment 41135) | No: a records move |
| MPSCALC-306 | landed in #91 (gate B354 GO WITH FINDINGS) | No: a records move |
| MPSCALC-251 | first-load spec is in CI under the stub; "the sign-in leg is not built" | No: a larger test build |
| MPSCALC-310 | "needs a product decision" (a seam or accept the mutant), comment of 11-10 | No: a decision |
| MPSCALC-314 | "the choice is open and has not been ruled" | No: a decision |
| MPSCALC-288 | option a chosen: a new `callerCan.reject` member "and new words" (comment 40127) | No: new words |
| MPSCALC-233 | ruled "Refuse" (comment 41083) but "the refusal and its rows are queued with their own review"; a new refusal sentence | No: new words |
| MPSCALC-368 | the six figures are hidden; "a name for the field is proposed for the product owner's approval" | No: a name needs approval |
| MPSCALC-315 | needs a result field and a calculation-register row before any number | No: design |
| MPSCALC-237 | new status and fields (D-12 a ruled the feature in; "new words go to the words gate") | No: a feature with words |

Verdict: 1 of 12 buildable now, 1 conditional. The sample was chosen for likely-small keys (tests, docs, one-line fixes) and found that most small ones have already landed; the remaining 36 are the larger v13 pack (screens, settings, proposal formats) and are not expected to be small. The ticket that said "commission a read-first classifier" can be closed on this evidence for the small ones; the rest stay a product-owner pack.

## 8. WAITING ON KAM (items for the next cards)

Named by the commission, each on its own card (not enumerated from the store; `list` is never used): RD-994 (NX-A; card `nexusai-audit-entry-limits-994-1118`); MPSCALC-410 and MPSCALC-207 (card `mps-410-openapi-195-wording-1117`); RD-1000 (card `nexusai-chat-bound-145-146-1117`); HPSMPOC-356 (card `hpsmpoc-356-residue-not-wanted-1117`); RD-1003 (card `nexusai-rd1003-action-route-signin-1118`); the new picomatch advisory (card `nexusai-picomatch-advisory-audit-1118`), which also gates every NexusAI and HPSM merge today.

My additions, from this sweep (a reading, not a card id): whether M-D4 may touch `docs/api/openapi.json` while the 410 card is open (section 3); whether the agreed sentence of MPSCALC-316 reaches the refusal text in `QuoteEndpoints.cs:1436` (G1 or G2); MPSCALC-233's refusal sentence; MPSCALC-288 and 368 words and name; MPSCALC-314 (the autosave choice); RD-974 and RD-975 (what an undated job counts as); HPSMPOC-470 points 1, 2 and 5; the carried list: HPSM HTML phase (21), 13 held, MPS `question-for-kam` and `needs-ruling` keys (22), Composer PCOMP-128, 129, 46, 94 and the Guided hold, Vision's pause.

## 9. Recommended order

1. **M-D4 (MPSCALC-364, S; step 2 MPSCALC-316 if confirmed):** the only buildable lane that can also merge today; one MPS seat; docs and generated copies. Start only after Tuesday reads the held 410 card as not covering `openapi.json:1509`.
2. **NX-L (RD-980, M):** build and gate now; merge when the picomatch card is ruled and the audit passes. One NexusAI seat.
3. **NX-M (RD-717, RD-749, M):** the same seat after NX-L (counts file and jest lock); read-first, may shrink to one key.
4. (none further: HPSM-POC and Composer have no lane.)

Lane 1 is in a different repository from lanes 2 and 3 and can run beside them under the machine-load rule (one waiter, load1 under 7). PR #220 is built and waits to merge; it is not a lane. NX-L and NX-M do not touch `backend/server.js`, so they do not collide with #220.

## 10. Disjointness check (by path)

- **MPS:** M-D4 owns `docs/API.md` (382 to 383), `docs/api/openapi.json` (1509; step 2 adds 988, 1036), `web/src/api/generated/openapi.snapshot.json`, `web/src/api/generated/schema.ts`, `src/MpsCalc.Api/Contracts/Dtos.cs` (comment at 466); step 2 adds `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` (1436) and `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs` (235). **Shared files with the held lanes** (not proposed today): MPSCALC-410 owns `docs/API.md` (the clause near 706 in SWEEP-2025's reading; line numbers have since moved to main's current text) and perhaps `docs/api/openapi.json`; MPSCALC-207 owns `src/MpsCalc.Import/PriceBookImporter.cs`. When those lanes run, they and M-D4 must go in series on `docs/API.md` and `docs/api/openapi.json` (different lines, same files, so a rebase).
- **NexusAI:** NX-L (`rd798-...test.js`, `rd799-...test.js`) and NX-M (`rd681-...test.js`, `rd684-...test.js`) share no test file. Both may add a cell, so both touch `scripts/verify-expected-counts.json` and the one jest lock: serial. Neither touches `backend/server.js` (PR #220 does) or `HISTORY.md` (PR #219 does). If RD-1003 or RD-994 later run (held), they would own `backend/server.js` and are serial with #220 first.
- **HPSM-POC, Composer:** no lane; nothing to check.
- **Across projects:** three different repositories, different `GH_CONFIG_DIR`, different Jira projects: no shared file. Only the machine-load rule couples them.

## 11. Card candidates (one line each: question and recommended default)

1. **M-D4 and the 410 card:** may MPSCALC-364 edit `docs/api/openapi.json:1509` (a description, not the 410 clause) before Kam answers the 410/195 card? Default: yes; it is developer-only text under the 11-11 ruling, and the card is about a different clause.
2. **MPSCALC-316 residue:** does the agreed sentence also replace the refusal text at `QuoteEndpoints.cs:1436` and its pin at `QuoteRefusalOrder.cs:235`? Default: yes (comment 41071 says "remaining places comment 40472 lists", and 40472 lists that sentence); gate G1 because it is a customer-visible error body.
3. **NX-L, RD-980 item 2:** freeze one value per pinned state, or drop the two masks? Default: freeze one value per state (keeps the cells' power); the seat records the pick in the PR.
4. **Records (Tuesday's, not Kam's):** PCOMP-74, 80, 81 are landed in `5d3bf82d` (name the commit on each ticket and move them) and MPSCALC-306, 297 have no remaining clause except that 297 waits for 135; the 11-11 "Done means merged" rule applies.

## Method and disclosures

- Instruments: `jqdump.py` (GET-only; credentials read in-process from each project's own `4_Credentials/.env` by variable name, never printed) for eight board dumps, four `updated >= "2026-11-17 20:00"` dumps, and five feedback and control queries; `bc.sh` (wrapper of `board_count.sh jira`) for eight counts; `jdesc.py` and `jcom.py` (GET-only) for ticket bodies and comments: HPSMPOC-408, 470, 431, 357, 246, 228, 207, 343, 503; MPSCALC-135, 130, 162, 163, 170, 189, 297, 310, 251, 288, 314, 306, 364, 233, 315, 368, 316, 237; PCOMP-74, 80, 81, 123, 23, 13, 16, 78, 65, 7, 8, 70, 71; RD-980, 978, 977, 970, 983, 969, 967, 975, 974, 972, 981, 911, 908, 749, 728, 726, 727, 717, 724. `rg.sh` (one file at a time through `gh api -X GET repos/<repo>/contents/<path>` at main) and `gh api -X GET` git trees (`pcomp_tree.txt` 974 blobs, `mps_tree.txt` 720, `rd_tree_now.txt` 1,042) for every "printed today" line; `gh api -X GET search/code` for two phrase checks in the MPS repository (2 hits and 1 hit, noted above; the code-search index may lag main); `commits?path=` for one Composer file history. Every GitHub read was under that project's own `GH_CONFIG_DIR`.
- Counts and controls: all four open + Done = created checks hold (508, 410, 129, 999). The `comm` of key lists against SWEEP-2025's files (`fleet/state/s286/sweep2025/{hpsm,mps,pcomp}_open.tsv` and `rerun/rd_open2.tsv`) reads: HPSM minus 507 and 508, NexusAI plus RD-1003, MPS and Composer unchanged.
- Not measured: whether any pane currently holds a ticket here (no pane list read); which contract test compares the MPS snapshot to the contract (named only by MPSCALC-316's comment); whether a locale env alone turns RD-980's 12 cells red; which RD-684 and RD-681 mutants are still green at main; the product line numbers of RD-684's code; the bodies of 72 NexusAI test-tail To Do keys beyond the 10 read; the 36 `lane-v` MPS keys beyond the 12 read; the held cards' contents (no `decision_queue.sh`); the picomatch advisory and whether it truly blocks every merge (taken from the commission); the live feedback stores (section 6); any CodeQL change since SWEEP-2025 beyond the count of 22; Vision (not re-swept).
- Corrections to SWEEP-2025's reading that this sweep found: PCOMP-74, 80, 81 were read as "records only" there; today they were checked at main and the build they wait for is on main as `5d3bf82d` (so "records only" was right, and the evidence is now printed). One earlier sentence ("a style build with its own review") was a ticket phrase, not a pending build.
- Outside the one-output-file rule: the scratch folder named at the top (dumps, ticket reads, trees, `rerun/`). No WEDNESDAY, FRIDAY, Secuura or other client read, no ledger file read, no mail, no hosted HTTP, no `az`. A hook refused one command (a `==` echo word at the start of a loop echo, and an unquoted `$R` with spaces); both were rewritten. A first call to `rg.sh` passed `-i` where the script expects a pattern and printed grep's usage (no data harmed); it was rerun with the right arguments. Clocks come from `date`.

READ-WHOLE-BY-TUESDAY: ____
