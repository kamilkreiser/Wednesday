SWEEP-1115: 4 lanes

# SWEEP-1115: Datasec tickets agents can build now, in lanes (read-only sweep, 2026-11-19 late morning)

Written by a read-only sweep drafter. Clock from `date`: 11:10:21 AEDT at start; 11:16:42 AEDT after the file was written. Form copied from `2026-11-18_SWEEP-2305_datasec-actionable-lanes.md` (read whole first). Instruments (`bc.sh`, `jqdump.py`, `jdesc.py`, `jcom.py`, `rg.sh`) copied from `2_Project_Files/fleet/state/s291/sweep2305/` into `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s292/sweep1115/` (each read before use; all GET-only). One edit to the copy: `jqdump.py` also writes priority, updated and created columns (columns 6 to 8 of the `.tsv`). Fences kept: no Jira write, no GitHub write (`gh api -X GET` only), no git write, no mail, no `az`, no deploy, no `cd`, no token printed, `decision_queue.sh` not run at all (not needed), nothing under Secuura, WEDNESDAY or FRIDAY read.

Excluded by the commission (the NexusAI records pass B1730 is filing these now): other unguarded `req.body` reads, the final error handler's development text, the RD-523 code-string exception and the chat bubble `innerHTML`. No lane below touches those subjects; RD-1005 and RD-1007 (landed in #229, still open on the board, To Do, as the records pass has not run) are not lanes.

## BLUF

**4 buildable lanes holding 6 keys: NexusAI 3 lanes (RD-793 + RD-990; RD-835 + RD-861; RD-445 item 2 only), MPS Calculator 1 lane (MPSCALC-415), HPSM-POC 0, Security Composer 0.** All four are file-disjoint. Predicate for "buildable": open (statusCategory != Done), status To Do or Backlog, not named on any held, dropped or ruled-against line in the pickup or the notes of 11-18 and 11-19 (grep, section Excluded), the ticket says what to change, no new customer words, no client human's open question, no deploy, no Partner Center, no HP-tool integration, and still true at main (checked by `rg.sh`).

Recommended order (at most 4, file-disjoint):
1. **M-F: MPSCALC-415** (one table cell in `docs/IMPORTER.md`, size S, G2; needs your C-109 reading, question 1).
2. **N-S: RD-793 + RD-990** (the only `backend/server.js` lane; four handlers get `requireAdminFor`, one path expression fixed in two rows; size M; gate G2 with an Opus read, or G1 if you want the permission change treated as permission-core work).
3. **N-F: RD-835 + RD-861** (browser scripts only, no server file; size M; G2).
4. **N-J: RD-445 item 2** (one middleware file, size S; needs a one-word choice, question 3).

N-S, N-F and N-J can be built side by side by file; whether they can run side by side given the single jest lock is question 4. A fifth item, RD-1006, is design-sized and not a lane (see below).

## Board census

All counts are `board_count.sh jira` through `bc.sh`, predicate `project = <KEY> AND ( <clause> )`; every line printed `limit was 5001, so this is a real count and not a cap`. The same sets were dumped by `jqdump.py` (`rows` = `unique` in all eight dumps).

| project | open now (statusCategory != Done) | Done (dump) | created since 2000 | control: open + Done = created | open at SWEEP-2305 | change by `comm` of key lists | buildable keys | lanes |
|---|---|---|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 145 | 365 | 510 | 145 + 365 = 510 holds | 146 | gone HPSMPOC-510 (Done); none new | 0 | 0 |
| MPS Calculator (MPSCALC) | 163 | 252 | 415 | 163 + 252 = 415 holds | 163 | gone MPSCALC-414 (Done); new MPSCALC-415 | 1 | 1 |
| Security Composer (PCOMP) | 78 | 51 | 129 | 78 + 51 = 129 holds | 78 | none gone, none new | 0 | 0 |
| NexusAI (RD) | 873 | 130 | 1003 | 873 + 130 = 1003 holds | 871 | gone none; new RD-1006, RD-1007 | 5 (RD-793, 990, 835, 861, 445 item 2) | 3 |

Controls that can fail: the key-list arithmetic (HPSM 146 - 1 = 145; MPS 163 - 1 + 1 = 163; Composer 78; NexusAI 871 + 2 = 873) equals the measured open count in all four; positive controls for the Done lists: `HPSMPOC-510` is 0 hits in `HPSMPOC_open.tsv` and 1 in `HPSMPOC_done.tsv`; `MPSCALC-414` 0 and 1; `RD-1003` 0 in `RD_open.tsv` and 1 in `RD_done.tsv`. The "no HPSM or Composer key changed" claim is a zero on the field `updated >= "2026-11-18 22:30"` (HPSMPOC 0 rows, PCOMP 0 rows); positive control on the same field and window: MPSCALC returned 1 row (MPSCALC-415, updated 00:22 today).

Origin state now (`gh api -X GET` under each project's own `GH_CONFIG_DIR`; `gh api user` login contained 'datasec': count 1 for each of the four): HPSM-POC main `d8a1de6d` (#336 merged), 0 open PRs, Dependabot open 1, code-scanning open 0. MPS main `b65a7f3b` (#216), 0 open PRs, Dependabot 1, code-scanning 0. Composer main `b4681297` (unchanged since 11-15), 1 open PR: draft #85 `b330/sm316-content-catalogue` (HELD), Dependabot 0, code-scanning 0. NexusAI main `46050e25` (#229, 2026-11-19T00:04Z), 0 open PRs, Dependabot 1, code-scanning **22** open (the call form returns real rows here, which is the positive control for the three zeros). `state=closed` printed each repository's last three merges (HPSM #336, #335, #334; MPS #216, #215, #214; Composer #130, #129, #128; NexusAI #229, #228, #227), so the call form works. Open alerts were counted, not read.

## Lanes

| lane | project | keys | owns (paths, at main) | model row | gate | size | merge |
|---|---|---|---|---|---|---|---|
| M-F | MPS | MPSCALC-415 | `docs/IMPORTER.md` line 17 (the last sentence of one cell only) | L1 (one file, one hunk) on Sonnet | G2 (docs, word review of the one sentence against `ParityProof.cs`) | S | yes after gate and CodeQL (MPS rule); 0 open PRs |
| N-S | NexusAI | RD-793, RD-990 | `backend/server.js` (lines 15947, 16010, 16031, 17565 for RD-793; 556 for RD-990), `backend/services/accessAudit.js` (line 50), new `__tests__/rd793-*.test.js` and `__tests__/rd990-*.test.js`, regenerated `docs/role-capabilities.json` and `docs/ROLE-CAPABILITIES.md` (by `scripts/role-capability-inventory.js`), the expected-counts file | C2 on Sonnet for RD-990; C3 on Opus if the builder treats RD-793 as permission-core (the roles-UI itemised document puts permission rows at Opus C3 with G1) | G1 if Tuesday reads RD-793 as permission-core; otherwise G2 | M | yes if checks green; this is the only `server.js` lane |
| N-F | NexusAI | RD-835, RD-861 | `static/js/index.js` (eight `esc` closures at 5833, 5893, 5907, 5934, 5947, 5975, 5987, 6014; the user table around 5633 and `userNameWithInfo` at 6238), `static/js/settings.js` (`showValidationModal` at 1696), `static/js/first-run-setup.js` (`testConnection` at 2955), tests under `__tests__/` (extend or sit beside `rd778-dom-text-stays-text.test.js`), the expected-counts file | C2 on Sonnet | G2 | M | yes if checks green |
| N-J | NexusAI | RD-445 (item 2 only) | `backend/marketplaceJwt.js` (113 to 117), one new test file in `__tests__/` (there is no existing test for this file in the tree), the expected-counts file | C2 on Sonnet | G2 | S | yes if checks green |

Model-routing line numbers were not re-printed this time (they are in SWEEP-2305: L1 line 80, C2 line 92, C3 line 93, G1 line 108, G2 line 109); the row names above are carried from that sweep, not re-read.

### M-F: MPSCALC-415 (one stale cell in a developer document)

Ticket scope, quoted: "Change only the last sentence of that one cell so that it says what the proof does with the colour panels (it counts the section's SKUs per sheet, checks the owed device and SKU pairs, and does not compare the records with the approved workbook or re-read the book); read each word against `ParityProof.cs`; keep the words any mapped model sheet; no other byte of docs/IMPORTER.md changes; no source, test or contract byte changes." The ticket adds that whether this sentence goes to the product owner's word review "is not decided here" (C-109) and is "the coordinator's reading to make".

Printed at main `b65a7f3b` (the commit the ticket cites):
- `docs/IMPORTER.md:17` is the row "Colour panels outside the map (MPSCALC-147)"; the phrase `counts them and compares the governed options only` is on that one line (count 1) and the words `any mapped model sheet` are on the same line (count 1, the positive control).
- `docs/IMPORTER.md:1 to :6` opens "Price-book importer - lane 2A", names the spec rows and the CLI `mpscalc-import`: on its face a developer's document (spec rows, register ids, ADR). That is my reading, not the ticket's; it is yours to make (question 1).
- `src/MpsCalc.Import/Parity/ParityProof.cs:190 to :202`: the owed (device, SKU) list built from the distinct block SKUs and the `SequenceEqual` refusal at 199 to 202, as the ticket says.
- Red-first for a words change: count of the old phrase over `docs`, `src`, `tests`, `.github` before (1) and after (0), positive control on the unedited line; no other byte of the file changes (a diff of the file shows one hunk on one line); the statement at `docs/IMPORTER.md:91 to :94` still reads true.
- Answer to the commission: **buildable as written if you read this document as developer-only**; if you read it as customer-facing it is a words question for the product owner and drops out of the lanes.

### N-S: RD-793 and RD-990 (the `backend/server.js` lane)

**RD-793** (High, To Do, labels operations, s89r, security; updated 11-06): four routes that change data sources check no role: `DELETE /api/data-sources/:id` (`backend/server.js:15947`), `POST /api/data-sources/:id/tables` (`:16010`), `DELETE /api/data-sources/:id/tables/:tableName` (`:16031`), `DELETE /api/setup/data-sources/:id` (`:17565`). Printed at main `46050e25`: each handler opens with its `try` and no role call (lines 15947 to 15952, 16010 to 16014, 16031 to 16035, 17565 to 17570); the helper to use exists: `requireAdminFor(req, res)` at `:19081` (403 `Admin access required`, open window unchanged) and is used by the sibling writers `POST /api/data-sources` (`:15817`) and `PUT /api/data-sources/:id` (`:15847`). The committed inventory shows `DELETE /api/data-sources/:id` with `"gateInHandler":[]` (`docs/role-capabilities.json:108`, positive control that the gap is current). The ticket's own fix: "the same one-line guard ... so the open window stays as C-01/C-178 rule it", ruled by Tuesday's mail on RD-761's design (named on the ticket). Red-first: a viewer on a configured deployment gets 403 on each of the four; an open-window caller is unchanged. Not a new word: the refusal text is the existing `Admin access required`.

**RD-990** (Medium, To Do, labels records-pass-1115, roles-ui-2026-11, security): a refusal answered inside a mounted router is audited with the router-relative path (`/`, `/6`). Printed: `backend/services/accessAudit.js:50` reads `path: req.path`; `backend/server.js:556` reads `path: req.path` in the STATE_MUTATION row (the ticket says line 540 at an older main; the line moved, the code is the same). The ticket's fix: record `req.baseUrl + req.path` (or the path part of `req.originalUrl`, never the query) in one place used by both rows, keep the six detail keys. The ticket says "No decision is needed from the reader." Red-first: put `req.path` back on a copy and the three cells fail.

Why one lane: both edit `backend/server.js` and the capability inventory, and `server.js` lanes cannot run in parallel. Size M together. **What would STOP it:** the inventory test `__tests__/rd929-capability-design-census.test.js` (205 routes) reading a changed `gateInHandler` as a red census (the builder regenerates the inventory with its own script; if the census compares a hand-kept expectation, the lane needs an addendum); RD-1003's decision (the internal `-action` route's own caller check, a Kam decision) if the builder's guard change touches the feedback router; any wish to add the sixteen more write routes of RD-958 (that is #200, in Testing, not this lane).

### N-F: RD-835 and RD-861 (browser scripts)

**RD-835** (Medium, To Do, security; updated 10-08): CSV exports quote values but do not neutralise a leading `=`, `+`, `-`, `@`, tab or CR, so a device or user named `=HYPERLINK(...)` becomes a live formula in the admin's spreadsheet. Printed at main `46050e25`: eight identical `const esc = (val) => \`"${(val || '').toString().replace(/"/g, '""')}"\`` closures at `static/js/index.js` lines 5833, 5893, 5907, 5934, 5947, 5975, 5987, 6014 (count 8, as the ticket says; the lines moved by 11 from the ticket's 5822). Fix shape (ticket): one shared `esc` for all eight sites that prefixes such a value with a single quote (OWASP). Red-first: one cell per export with a `=cmd` value.

**RD-861** (Medium, To Do, labels security, xss): three sinks still write server or AI values as HTML: `static/js/settings.js` `showValidationModal` (function at 1696; `validationResult.suggestion` at 1713 and `.message` at 1720 are concatenated into `html`), `static/js/first-run-setup.js` `testConnection` (function at 2955; `result.innerHTML` at 2975 and 2993), and the `static/js/index.js` user table (`userNameWithInfo(u.userName, u.userClass)` at 5633; `userNameWithInfo` at 6238; the class values come from code today, so the lowest risk). Ticket ask: escape or use `textContent`, red-first with a markup payload, CodeQL shows no new alert. The existing cells for the sister change are `__tests__/rd778-dom-text-stays-text.test.js` (in the tree).

Why one lane: both change `static/js/index.js`. Size M. **What would STOP it:** the RD-131 drum section deliberately matches the old CSV behaviour with a cell that pins the match (ticket RD-835 says so); the builder must move that cell with the shared `esc`, not around it; a customer-visible word appearing in a new refusal or note (none is asked); CodeQL reporting a new alert on the PR (the merge rule). Note RD-1005 and the records-pass follow-up (c) mention "chat bubble innerHTML": that is a different file region (the chat bubble) and the lane does not touch it.

### N-J: RD-445 item 2 only (the Marketplace JWT bypass)

**RD-445** (Medium, To Do, s59, security; three items, written 09-14 at older code): item 2 says `backend/marketplaceJwt.js` accepts any bearer token when `MARKETPLACE_SKIP_JWT=true`; "confirm no template, compose file, workflow or doc sets it; refuse to honour it when NODE_ENV=production (or remove it), and log loudly when it is on; cell: production + flag -> still verifies." Printed at main `46050e25`: `backend/marketplaceJwt.js:113 to :117` is the bypass (a `logger.warn` and `req.marketplaceTokenPayload = { iss: 'skipped', sub: 'skipped' }`); the only caller is `backend/marketplace-api.js:83` (`router.use('/webhooks', jwtMiddleware())`; `:37` the require). Counts of `SKIP_JWT`: `azure-marketplace/combined/mainTemplate.json` 0 (control: the file printed 609 lines), `.github/workflows/build.yml` 0 (93 lines), `docker-compose.yml` 0 (301 lines), `backend/server.js` 0 (22788 lines); so nothing in those four sets it, as the ticket asks the builder to confirm. Items 1 (`verify-group`, `backend/server.js:4197`) and 3 (the sign-in callback's `error.message`) are in `server.js` and are not in this lane; the ticket stays open for them.

Size S. **What would STOP it:** the choice "refuse in production" versus "remove the flag" (question 3; default: refuse when `NODE_ENV=production`, keep the loud log); the builder finding a hosted setting that uses the flag (not readable here, no `az`); no Partner Center step is part of this change.

## Roles-UI program state (card `nexusai-roles-ui-seven-1106`, ruled a; `ITEMISED-CHANGES.md` and `WORD-PACK.md` read as listed below, measured against the live board)

**Ticketed: yes, all 136 rows.** The itemised table has 136 row ids (`^| I-nnn ` count 136). The tickets RD-927 to RD-957 (31 keys; RD-927 is the finding, RD-928 to RD-957 the program) name 135 of them (`I-nnn` ids found by regex in the descriptions, 135 unique; positive control `I-001` 1 hit); the one missing, `I-123` (viewer can write configuration), is named in RD-958 (1 hit). Descriptions were fetched at 30,000 characters (not truncated in practice: the file is 107,101 bytes for 31 tickets).

**Board state (label `roles-ui-2026-11`): 44 open (36 To Do, 8 Testing) and 2 Done (RD-992, RD-1003).** Predicate: `labels` contains `roles-ui-2026-11` in `RD_open.tsv` / `RD_done.tsv`. Of the 36 To Do, RD-927 to RD-957 (31) are the program tickets, none moved to Testing; RD-966, 967, 969, 989, 990 are findings. The 8 in Testing are RD-958, 962, 963, 964, 965, 968, 988, 995 (built and merged, awaiting verification).

**Built and landed (measured from the ticket comments, not inferred from titles):**
- L0 foundation, RD-928: both parts landed (inventory as #178, `993be21a`; layout recorder as #179, `fab4fa41`); the ticket is still To Do on the board ("stays open").
- L2 tokens, RD-936: #180 (`33db7181`) landed with the generated palette; ticket still To Do.
- Permission core, RD-929: the design as data landed (#197, `backend/services/capabilities.js`, a census test over the 205 routes of the inventory); nothing in the product reads it yet. #216 (NX-R, RD-995) landed the role table's own-caller check for the internal `-action` route. The build (a capability check per route, the role source) is **still owed**.
- Write gates for a viewer, #200 (RD-958 seventeen routes, RD-964 three, RD-968 one): in Testing. Denial audit rows (#201, RD-932 in part). RD-988 and RD-965 in Testing.
- The word pack (RD-934): the product owner ruled section A, all twelve decisions as recommended (comment 11-06 21:12); sections B and C follow the twelve rules, a row the rules do not decide is "not ruled" and uses the existing word or asks.
- Not started (no comment, To Do): the shell (RD-937 sidebar, 938 top bar, 939 page split), all pages (RD-944 to RD-954), drawer, table toolkit, help, search (RD-940 to RD-943), settings in the shell (RD-955), dark mode (RD-956), docs (RD-957), later roles (RD-933), row scope (RD-930) and sensitive fields (RD-932 rest), assistant answers (RD-931). RD-930, 931 and 947 carry the 11-11 ruling (accepted recommendations) with "queued as its own change".

**What blocks the rest (each read at the ticket or the itemised document):**
1. The permission-core wiring (RD-929) is a design-first Opus C3 job on `backend/server.js` with a G1 gate (itemised section 7 lane L1). The itemised order puts it before any role is shown: L6, L7, L8, L10, L11, L12, L13 depend on L1 parts. It has a stated condition from the #216 review (comment 11-18 01:10: the `-action` route must keep its own caller check when the table is wired through `decide()`), and that route's open question is RD-1003 (Done on the board; "a decision for Kam" in the 11-18 note).
2. RD-989 (21 call sites in four static files that now meet a viewer 403) needs one rule chosen: hide or disable the control for a viewer, or leave it and show the refusal in plain words. That is a product wording choice (customer words).
3. The shell lanes (L3 onward) need L0 (landed), L2 (landed in part), and "words". The twelve section-A rules are ruled; a build that meets a string those rules do not decide must use the existing word or ask. No section B or C pack has been sent for a row-by-row ruling.
4. No NexusAI demo deploy: C-224 (until RD-876 part 2 lands; RD-876 reads To Do) and C-239 (Nexus after other projects). Everything above builds and merges but does not deploy.
5. `static/js/index.js` (9,404 lines at `46050e25`) is the choke point (itemised section 7: L4 splits it before page lanes run in parallel); N-F in this sweep edits it, so it should land before L3.
Not measured: the 8 Testing keys' verification state beyond their status; whether any itemised row is satisfied by a ticket outside the label.

## Excluded

NexusAI: of 357 To Do keys, the label predicate (security or records-pass-*) left **65 To Do** (220 keys with the labels across all open statuses; 63 Release Ready and 91 Testing are built and waiting, not candidates). Grepping each of the 65 keys in the pickup and the notes of 11-18 and 11-19: only RD-1004, 1005, 1006, 1007 and RD-1001 appear (positive control: RD-1007, 19 hits); 0 of the other 60 are held or ruled against there. I then read descriptions and last comments of 28 candidates (descriptions capped at 1,400 characters, comments at 700, so some tails are unread):

| key | reason | source |
|---|---|---|
| RD-1005, RD-1007 | landed in #229; records pass B1730 is moving them; excluded by commission | pickup; commission |
| RD-1004 | the 2026-12-18 picomatch calendar step (dated, not now) | pickup line 98 |
| RD-1006 | design-sized, see question 5 | ticket read whole |
| RD-1001 | `core.sshCommand` on the records working copy names an unmounted volume: a host setting, not a code lane | pickup |
| RD-972 | landed as #195 (comment 11-12 00:58 verifies it on main); ticket open for verification | comment |
| RD-421 | landed in #209 (comment 11-17 01:42); open for verification | comment |
| RD-498 | built and merged inside RD-495 (comments of 09-21 and 09-22); a records close | comments |
| RD-983 | landed as #208 (comment 11-16 21:43); open for verification | comment |
| RD-806, RD-805 | part landed; alerts 235 to 237 and 145, 146 stay open; no alert is dismissed without Kam (C-190); RD-994 carried the audit part | comments 11-16, 11-17 |
| RD-810 | ruled 11-16 22:44: leave the alert open, recorded as intended; no code change | comment |
| RD-768 | alerts 112 and 113 need a file mode 0600 change that "is visible to the product" and was left out of #209 on purpose: a product choice | comment 11-17 01:42 |
| RD-997 | "decide whether the limiter should also sit ahead of express.static ... first read whether counting static files against the same counter is wanted": a decision; server.js | ticket |
| RD-927 | roles-UI permission core (Opus C3, G1); measure first; a viewer's read rights are the product owner's question 3 (ruled, but the build is the program's L1b) | ticket |
| RD-925 | "settle what a legal table name is" (Azure's rule not measured): a decision before a build | ticket |
| RD-859 | client-sent KQL stored; the fix shape is not stated and RD-774's ruling is a related decision | ticket |
| RD-820 | extracting a function into a module is "a product refactor of an AI path" outside the ruled scope; design-first | ticket |
| RD-792 | Azure Government and China endpoints: a product decision (offer or remove the options) | ticket |
| RD-714 | the code is on a branch (`rd-413-truthful-mail-secret-storage-s84m`) never on main; mail-state wording | ticket |
| RD-702 | the truthful wording is "drafted for the product owner's approval first" (comment 11-11): customer words | comment |
| RD-487 | the UI must say "what is now in force": new customer words and a design | ticket |
| RD-725 | the test it repairs (`rd594-kv-identity-open-window`) is not in the tree at main (0 hits in `rd_tree.txt` for `rd594`; control: `rd778` 1 hit); it lives on a branch | ticket; tree |
| RD-621, RD-517, RD-439 | old (September) gate findings with design choices (sentinel format; wizard re-test; a revocation list); not a stated change | tickets |
| RD-989 | needs one front-end rule chosen (customer words) | ticket |
| RD-368, RD-858 | `needs-decision` / `kam-decision` | labels |
| RD-21, RD-54, RD-55, RD-364 | pen test, key rotation, history scrub, a hygiene set: a purchase, a tenant, a rotation or too wide | titles |
| RD-879, 816, 913, 881 and the other Testing or Release Ready security keys | built, awaiting records or verification; not To Do | status column |
| RD-928 to RD-957 (roles-UI program) | the program, see its section; none is a one-lane key and the permission core is design-first | tickets |
| RD-1003, RD-994 | Done and Testing; no lane | board |
| the other ~30 of the 65 (not read) | not read: this sweep stopped at 28 candidates and three lanes; their dates and titles are in `rd_rank.txt` | scratch |

Other projects, carried from SWEEP-2305 (no change in the key lists, measured above):
| key | reason | source |
|---|---|---|
| HPSMPOC-510 | Done (landed as #336) | `HPSMPOC_done.tsv` |
| MPSCALC-414 | Done (landed as #216) | `MPSCALC_done.tsv` |
| MPSCALC-195, 120, 200, 407, 402, 333, 372, 316, lane-v keys (47), 233, 288, 368, 237, 314, 310, 315, 251, 135 and the rest | as SWEEP-2305: words, designs, decisions, records moves or larger builds; none updated since 22:30 yesterday except 415 | `MPSCALC_open.tsv`; SWEEP-2305 Excluded |
| MPSCALC-69 to 85 | Kam's questions (`question-for-kam`) | SWEEP-2305 |
| HPSMPOC HTML-phase keys (21), 470, 408, 431, 357, 246, 228, 207, 343, 503, In Progress 87, 90, 91 | as SWEEP-2305: product-owner words, hosted measurement, deploy, or Kam-owned | SWEEP-2305 |
| any HP-tool integration | HPSM builds only this phase, no integration | commission |
| PCOMP (all 78) | the Guided hold and `held` labels, words, design calls and held PR #85; none updated since 22:30; 0 buildable | SWEEP-2305 |
| Vision, myPKI, CypherKey, Lead_Bot | skipped | commission |
| any deploy, UAT hold, Partner Center step | outside the sweep | commission |

## Questions for Tuesday

1. **MPSCALC-415: is `docs/IMPORTER.md` developer-only under C-109?** My reading from its opening (lane 2A, spec and ADR ids, the importer CLI) is yes, so the sentence is corrected from the code without the product owner's word review, as MPSCALC-414's comment was. Default: build it (G2, one cell). If you read it as customer-facing, it is a words question for Kam.
2. **N-S gate and model:** RD-793 adds a role refusal to four data-source routes; RD-990 only changes a logged path. Default: G2 with an Opus read of the RD-793 diff; raise to G1 + Opus C3 if you want it treated as permission-core.
3. **N-J (RD-445 item 2):** refuse the bypass when `NODE_ENV=production` (default), or remove `MARKETPLACE_SKIP_JWT` entirely? One word for the builder.
4. **Parallel NexusAI lanes and the jest lock:** may N-S, N-F and N-J build side by side (they share no file) or must they queue behind the single jest lock? I read no rule that allows or forbids it; I assumed the machine-load rule, not the lock, decides.
5. **RD-1006 (audit file not fully bounded after RD-994):** can a design-first drafter start without a ruling? **Yes for a read-only census** of every `auditLog(` site in `backend` (48 in `backend/server.js` per the ticket) marking each bounded, bounded elsewhere or unbounded, and a design note; **no for the build**, because the ticket says how an over-long value is shown for a row the guard cannot refuse (identity provider claims, SCIM) "needs the product owner's word if it is not the same for every kind: ask on this ticket". It also edits `server.js`, so it queues behind N-S. Do you want that census as a drafter lane?
6. **The roles-UI permission-core wiring (RD-929):** the only roles-UI step that is buildable without words is the capability wiring (Opus C3, G1, `server.js`). It does not fit this sweep (design-first, large, a `server.js` lane that conflicts with N-S). Do you want it drafted after N-S lands, and is RD-1003's answer recorded as the condition the #216 review named?

## How measured

**FOUND.** 4 lanes, 6 keys (NexusAI 5 keys in 3 lanes, MPS 1). HPSM-POC 0 and Composer 0 (key lists unchanged but for the Done move of HPSMPOC-510). Roles-UI: 136 of 136 rows ticketed; 44 open and 2 Done under the label; program tickets RD-928 to RD-957 all still To Do on the board, with L0, tokens, the permission design and the write gates landed in part.

**TESTED.** (a) Four project counts by `bc.sh` (open and created-since-2000) with Done from `jqdump.py`; control open + Done = created in all four (510, 415, 129, 1003); key-list differences by `comm` against `s291/sweep2305/*_open.tsv` (a LC_ALL=C sort); the arithmetic is the control. (b) Origin state by `gh api -X GET` (commits, pulls, Dependabot alerts, code-scanning alerts, user); `gh api user` count 1 on each of the four. (c) Ticket text and the last comments by `jdesc.py` and `jcom.py` for 28 NexusAI candidates, MPSCALC-415 and RD-1006 (descriptions capped; MPSCALC-415 read at 3,500 characters; RD-990 at 3,800), and 31 roles-UI tickets at 30,000 characters. (d) Code at `46050e25` (NexusAI) and `b65a7f3b` (MPS) by `rg.sh`: the eight `esc` lines, the sink lines, the four data-source handlers, `requireAdminFor`, `marketplaceJwt.js`, `accessAudit.js`, the inventory json, `docs/IMPORTER.md:17`, `ParityProof.cs:188-202`; the tree of `46050e25` (`rd_tree.txt`, 1,108 paths) for test files. (e) `/usr/bin/grep` over the pickup and the two notes for every To Do candidate key (65), then DROPPED/HELD lines read. (f) Itemised row ids by regex over `ITEMISED-CHANGES.md` and the ticket text.
**NOT tested:** any test or build (nothing run); the other ~30 of the 65 NexusAI candidates (not read); whether `rd929-capability-design-census.test.js` compares a hand-kept expectation (not read); hosted use of `MARKETPLACE_SKIP_JWT` (no `az`); whether the 8 Testing roles-UI keys are verified; `WORD-PACK.md` sections B and C (not read beyond headings); `decision_queue.sh` (not run); HPSM and Composer keys not updated since 22:30 yesterday are carried from SWEEP-2305, not re-read. Limits met: three zsh quoting slips (an unquoted array split, `grep -P` absent on this macOS `grep`, an `=` separator word); each rewritten, no data harmed; nothing written to any board, repository or host.

**HOW.** Instruments and scratch in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s292/sweep1115/` (`*_open.tsv`, `*_done.tsv`, `rd_rank.txt`, `rd_read1.txt` to `rd_read3.txt`, `roles_tickets.txt`, `rd_tree.txt`, `items.all`, `items.tix`). Clocks from `date`.

READ-WHOLE-BY-TUESDAY: ____
