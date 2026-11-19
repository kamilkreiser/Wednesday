SWEEP-1630: 10 buildable keys, 10 candidate decisions

# SWEEP-1630: Datasec backlog, what can be built next and what few decisions would unblock the most (read-only sweep, 2026-11-19 late afternoon)

Written by a read-only sweep analyst for Tuesday. Clock from `date`: 16:30:19 AEDT at start; 16:56:39 AEDT at the write of this file. Form and instruments copied from `2026-11-19_SWEEP-1115_datasec-actionable-lanes.md` and `fleet/state/s292/sweep1115/` (bc.sh, rg.sh, jqdump.py, jdesc.py, jcom.py, each read before use, all GET-only) into `fleet/state/s293/sweep1630/`, where I added four more GET-only scripts (flags.py, lastc.py, dgrep.py, classify.py). Fences kept: no Jira, GitHub or git write, no mail, no az, no deploy, no request to an app host, no jest, no server, no token printed, `gh api -X GET` under each project's own `GH_CONFIG_DIR`, `decision_queue.sh prior` only (five calls, see How measured).

## BLUF

**HPSM-POC was EXCLUDED, as commissioned (Kam's hold to 2026-12-10: "no more HPSM work for the next 3 weeks or until I request something new", live board 16:25:45): its Jira board, repository and project folder were not swept, counted, read or listed.** Frame for every "all tickets" claim below: Jira projects MPSCALC, PCOMP and RD, `statusCategory != Done`, counted by `board_count.sh` through `bc.sh` at 16:30 (RD includes 2 tickets in status Declined, which Jira does not treat as Done).

**10 buildable keys: NexusAI 7 (RD-1011, RD-1012, RD-1013, RD-175, RD-349, RD-1008, RD-759), MPS Calculator 2 (MPSCALC-195, MPSCALC-316), Security Composer 1 conditional (PCOMP-44).** The NexusAI keys fall in three serial lanes after N-J (N-K, N-L, N-M) plus one small spare (N-O). MPS is one docs-and-wording lane (M-G). PCOMP-44 is a coordinator's start (question 3).

**Why the rest is blocked** (open now: MPS 162, Composer 78, NexusAI top 60 by rank):
- MPS: 35 need words, 46 are already landed on main and only wait for a records move or a reading, 23 are unread or seed without a record, 21 are umbrellas or already answered, 11 need a deploy or a renewed secret, 11 need a ruling.
- Composer: 24 sit behind a hold (10 under the Guided hold, 13 behind the reviewer's round, 1 on held PR #85), 17 wait on an unbuilt predecessor in the same program, 9 are umbrellas or superseded.
- NexusAI top 60: 23 need a ruling, 9 need design or a measurement first, 5 need words.

**The few decisions that free the most (section Job 2):** MPS: (1) approve one words pack for the v13.4.1 lanes (35 keys), (2) authorise a hosted deploy of main and renew the seed identity's expired secret (11), (3) one answer sheet for the open Questions for Kam (11). Composer: (1) lift or keep the reviewer-round hold (13 now, and the 17 behind them), (2) turn Guided back on or keep it off (10), (3) seven owner's calls. NexusAI: (1) the roles-UI section B and C word pack and the hide-or-disable rule (RD-989 plus the shell program), (2) the CodeQL baseline disposition (5), (3) the mail-secret and key-input package (3), (4) one group answer for unparsed request bodies (2). None of these is already answered by a prior ruling I could find; where a prior ruling narrows one, it is quoted.

**Three things found already answered or already built, which change what to do:** (a) RD-532 (banner above the loading overlay), RD-577 (key-vault status read) and PCOMP-52 (policy PDF table of contents) are built on main while their tickets read open; (b) RD-175, RD-349 and RD-759 carry the product owner's 2026-11-11 ruling and the code at main still has the defect, so they are buildable now (N-L, N-O); (c) MPSCALC-195 and MPSCALC-316 carry the product owner's C-108 acceptance of the exact docs sentences and the work is owed (M-G). Details and evidence below.

**Recommended order for NexusAI after N-F and N-J land:** N-K, N-L, N-M (N-O spare). One conflict to decide: RD-929 (permission-core wiring, Opus, `backend/server.js`) is already drafted-after-N-J; N-K also edits `backend/server.js` and the capability pending list, so N-K should run after RD-929 or be folded into it (question 2).

## Class list (closed; printed first as commissioned)

- **B** Buildable now (passes the predicate).
- **F** In flight in an existing NexusAI lane (N-F, N-J).
- **L** Landed on main; ticket open for a records move, a verification, or a residual clause that is the coordinator's reading.
- **W** Needs customer-facing words, or a name or wording the product owner has not approved.
- **R** Needs a product-owner ruling or answer not yet given.
- **H** Waits on a named hold, a dated step or an outside release.
- **C** Waits on a client human (the reviewer, an SME) or on their data or file.
- **D** Needs a deploy, a hosted measurement, a renewed secret or an Azure step.
- **X** Needs an HP tool, HP or lender data, an outside system or a purchase.
- **P** Planned build too large or design-first for one lane, or waits on a named unbuilt predecessor.
- **S** Stale, duplicate, umbrella or already answered (evidence given; nothing proposed closed).
- **O** Other: too vague, test-infrastructure, records-process, or not read far enough.

A ticket gets one class: the first reason that stops it, read from its description, labels and last comment (descriptions to 300 to 1,500 characters, last comment only; see What was NOT tested). The class is my reading, not a ruling.

## Board census (counts through `board_count.sh`; every line printed "limit was 5001, so this is a real count and not a cap")

| project | open now (statusCategory != Done) | Done (dump) | created since 2000 | control: open + Done = created | open at SWEEP-1115 (11:10) | change by `comm` of key lists | buildable keys | lanes |
|---|---|---|---|---|---|---|---|---|
| MPS Calculator (MPSCALC) | 162 | 253 | 415 | 162 + 253 = 415 holds | 163 | gone MPSCALC-415 (Done, landed as #217); none new | 2 | 1 (M-G) |
| Security Composer (PCOMP) | 78 | 51 | 129 | 78 + 51 = 129 holds | 78 | none gone, none new | 1 (conditional) | 0 or 1 |
| NexusAI (RD) | 879 | 130 | 1009 | 879 + 130 = 1009 holds | 873 | gone none; new RD-1008 to RD-1013 (6) | 7 (in the top-60 frame and the ruled block) | 3 + 1 spare |
| HPSM-POC | EXCLUDED | | | | | | | |

Controls that can fail: key-list arithmetic: MPS 163 - 1 + 0 = 162, Composer 78, NexusAI 873 + 6 = 879, each equal to the measured open count. Positive controls for the Done lists: `MPSCALC-415` 0 hits in `MPSCALC_open.tsv` and 1 in `MPSCALC_done.tsv`; `RD-793` is in `RD_open.tsv` with status Testing (landed in #231, still open); `RD-1003` is 0 in open and 1 in `RD_done.tsv`. The RD open set splits as To Do 359, Testing 304, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 = 879. Dumps: `rows` = `unique` in all six (162, 253, 78, 51, 879, 130).

Origin state (`gh api -X GET` under each project's own `GH_CONFIG_DIR`; `gh api user` login contains "datasec": count 1 for each of the three): NexusAI main `9373976e` (#231 merge, 2026-11-19), 1 open PR (#232, `records/b1738-history`, the history pull request, under checks). MPS main `317bbb14` (2026-11-19T00:48Z, #217), 0 open PRs. Composer main `b4681297` (2026-11-15), 1 open PR, draft #85 `b330/sm316-content-catalogue` (held). The tree listings were taken at those mains (NexusAI 1,050 blobs, Composer 974); blob shas below are from them.

## JOB 1: the next buildable keys

Predicate (quoted from SWEEP-1115, plus one rule from Tuesday's answers): open (statusCategory != Done), status To Do or Backlog, not named on a held, dropped or ruled-against line, the ticket says what to change, no new customer words, no client human's open question, no deploy, no Partner Center, no HP-tool integration, and still true at main (checked by `rg.sh` or the `gh api` contents reads). Developer documents are not word-reviewed (C-109 option b, applied by Tuesday to MPSCALC-415 in SWEEP-1115 answers).

### NexusAI: the next three serial lanes after N-J, and one spare

NexusAI lanes run serially (one jest lock, one expected-counts file). Candidates read: the 67 To Do tickets with label security or records-pass-* (top 60 by rank are classified in Job 2); of them I read 34 not read by SWEEP-1115 (RD-1008 to RD-1013 among them), plus ten more with the 2026-11-11 ruling comment (RD-433, 175, 349, 532, 577, 522, 636, 610, 612, 622). Ticket and code were compared for every key in a lane.

| lane | keys | files at main 9373976e (blob prefix) | size | gate guess | order |
|---|---|---|---|---|---|
| N-K | RD-1011, RD-1013, RD-1012 | `backend/server.js` (668e343f32; lines 15962, 15987, 16053, 17385), `backend/services/capabilities.js` (1c58b35ad9; PENDING_GATE at 222), `docs/role-capabilities.json` (ae3373eaa9) and `docs/ROLE-CAPABILITIES.md` (regenerated by `scripts/role-capability-inventory.js`), `backend/services/accessAudit.js` (d36cf0c717; `requestPath` at 49 to 52), `backend/routes/entraProvisioning.js` (d8b183b4ce; line 167), new `__tests__/rd1011-*`, `rd1012-*`, `rd1013-*`, the expected-counts file | M | G1 with an Opus read (same shape as N-S: it changes who may call routes) | after N-F, N-J, and after RD-929 or inside it (question 2) |
| N-L | RD-349, RD-175 | `static/css/index-styles.css` (eb79bc10cf; `#7f8c8d` at lines 112, 567, 592; `.consumable-text` at 292 with `color: white`), `static/css/dark-mode.css` (e90297efa7), new contrast cells beside `__tests__/loading-overlay-contrast.test.js` and `__tests__/brand-chrome-contrast.test.js`, the expected-counts file | S to M | G2 (look change, measured contrast ratios in the cells) | any time after N-J; touches no JS or server file |
| N-M | RD-1008 | `backend/server.js` (668e343f32; `chatErrorText` at 1437, and the two code-string tests at 7598 and 7653), `static/js/index.js` (c6ca346ab0; line 3512 writes `data.message` with `innerHTML`), the file that defines the redirect-refusal error class (not named on the ticket; the builder reads it), new test file, the expected-counts file | S to M | G2 plus the CodeQL check (an XSS sink); G1 if you want server error text treated as security core | after N-F lands (both edit `static/js/index.js`) |
| N-O (spare) | RD-759 | `backend/services/cspReport.js` (f68287be53), `__tests__/rd759-796-csp-intake-edges-and-typed-fields.test.js` (exists), the expected-counts file | S | G2 | whenever a slot is free |

**N-K: RD-1011 + RD-1013 + RD-1012** (all three filed today by the #231 records pass, all follow RD-793 and RD-990 which just landed).
- RD-1011 (Task, Medium): four routes that make the server connect with a data source's stored sign-in details still have no role check: `POST /api/data-sources/:id/test` (15962), `GET /api/data-sources/:id/describe-table` (15987), `GET /api/data-sources/:id/discover-tables` (16053), `POST /api/setup/data-sources/:id/test` (17385). Printed at main: each handler opens with `try` and no role call; the helper `requireAdminFor` is at line 19093 (a function, count of `requireAdminFor(req, res)` calls 34, so the helper is in wide use) and is setup-mode aware, which the ticket says keeps the first-run wizard working. Fix (ticket): give each handler the check as its first statement, take the two test routes off `PENDING_GATE` in `backend/services/capabilities.js`, regenerate the role inventory with the project's own script. Cells in the ticket: viewer refused 403 on each with 0 outbound connects; administrator unchanged; open window unchanged; no session still 401.
- RD-1013 (Task, Low): `entra_provisioning_forbidden` audit entry records `req.path` (relative to the router) at `backend/routes/entraProvisioning.js:167`; the fix is a one-line import of `requestPath` from `accessAudit.js`.
- RD-1012 (Bug, Low): `requestPath` returns the request target as sent, so an absolute-form target or a raw `#` leaks into the audit path field (accessAudit.js 49 to 52); fix is to take only the pathname.
- Why one lane: the same audit helper and the same capability inventory; RD-1013 follows whatever RD-1012 does to the helper. **What would STOP it:** (1) the one answer RD-1011 asks for: whether `discover-tables` and `describe-table` must stay open to a viewer; the ticket proposes refusing all four and I found no prior ruling that says otherwise (the nearest, `CLARIFICATIONS.md` line 2922, reads the open window as unchanged, which the helper already keeps); builder default: refuse all four, Tuesday's call. (2) RD-1012 asks the builder to "decide and pin in a cell" how a percent-encoded path is recorded (as sent or decoded); a builder choice, not a product word. (3) the `rd929-capability-design-census` test reading a changed `PENDING_GATE` as a red census (the builder regenerates the inventory with its own script; the same risk named for N-S in SWEEP-1115, which landed in #231, so it is known to work).

**N-L: RD-349 + RD-175** (both carry the product owner's 2026-11-11 14:34 acceptance of all 17 quick recommendations; the comments say "queued as its own change with its own review"; none is in the pickup, 0 hits for both keys).
- RD-349: three selectors still carry `#7f8c8d` (3.48:1 on white, fails AA): `.metric-card .metric-label` (line 112, the dashboard KPI labels), line 567 and line 592 (printed: `.file-description` and `.drop-text`). Ruling for it (comment, quoted): "the same grey-text contrast ruling is applied to the three further places (the dashboard KPI labels among them)".
- RD-175: `span.consumable-text` is white on the light `#e9ecef` toner track (1.19:1). Printed at main: `index-styles.css:292` still sets `color: white` with a text-shadow outline; `dark-mode.css` has 0 lines naming `consumable` (the same grep on `index-styles.css` finds lines 241, 277, 292, the control). Ruling (comment, quoted): "the white toner text on its light track is fixed" in both modes.
- **What would STOP it:** the colour value is a look choice inside a ruled direction; the ticket cites RD-251 as the earlier change that moved the tab buttons off this grey, and the ruling comment says "the same grey-text contrast ruling", which the builder must read; G2 review of measured ratios resolves it. **RD-532 is NOT in this lane because it is already built:** `static/css/open-access-banner.css` lines 12 to 18 carry `z-index: 10000` with a comment citing "RD-532 (the product owner's 2026-11-11 ruling)", above the overlay's 9999; the ticket is still To Do. That is a records move (class L), not a build.

**N-M: RD-1008** (Bug, Medium, filed 11:55 today from the independent review of #229): `chatErrorText` (server.js 1437) decides to keep an AI endpoint's own error words by comparing the string `AI_ENDPOINT_REDIRECT_REFUSED` against `error.code`, and the AI client library copies `code` from an endpoint's HTTP error body, so a hostile endpoint can put its text into a stream error event, which `static/js/index.js:3512` writes into the chat bubble with `innerHTML` (printed at main: `textDiv.innerHTML = ... ${data.message}`). Fix (ticket): match the error's class (or the adapter's constant message) at server.js 1437, 7598 and 7653, and write the event's message as text at index.js 3512. Cells: a stand-in endpoint answering 400 and 500 with the code and an HTML text, over HTTP; a page cell that an event with angle brackets shows as text. No new customer word; no product decision. **What would STOP it:** `static/js/index.js` is the N-F lane's file until N-F lands; the class name is not referenced in `server.js` (0 hits of `AiEndpointRedirectError` in the 22,800-line file; control: `AI_ENDPOINT_REDIRECT_REFUSED` has hits at 1437, 7598, 7653), so the builder must find where the class is defined.

**N-O (spare): RD-759** (Low): a `data:` address that carries an at-sign keeps the text after it in the CSP report intake. PR #186 fixed the other two shapes (comment 2026-11-12 00:58: "its build is still owed"); the 11-11 ruling (quoted from the comment): "the security-policy intake refuses data: addresses that carry an at-sign". Printed at main: `backend/services/cspReport.js` line 37 names `data` only in a comment; 0 refusal for it (the same file's `RD-759` comments at 69 and 107 are the two landed shapes, the control that the grep finds the ticket's own markers).

**Conditional spares (ruled or answered, shape not fully read):** RD-578 (ruled 11-11: "may be fixed now, the sign-in one reviewed on its own"; its own text says first establish whether the template provisions the vault secrets; a reading of `azure-marketplace/combined/mainTemplate.json`, then a lane); RD-390 (SCIM panel type guard, fix shape written, tier 1, M); RD-433, RD-522, RD-610, RD-612, RD-622 (all ruled 11-11, "queued as its own change"; RD-610/612/622 are the erasure and wipe-alarm design, large). None was read to lane shape.

**To be ticketed (no ticket scopes it): `AUDIT_ACTIONS.SETTINGS_CHANGE` is used and never defined.** At main `9373976e`, `backend/server.js` has the name on 2 lines, 17353 (`add_data_source`) and 17600 (`remove_data_source`), both `auditLog(AUDIT_ACTIONS.SETTINGS_CHANGE, ...)`; the `AUDIT_ACTIONS` object opens at line 431 and defines CONFIG_CHANGE at 432 (control) but no key of that name, so both rows carry an undefined action. Board: an exact-token scan (`SETTINGS_CHANGE`, description and comments) over the 403 RD tickets whose text matches by stem found 2: RD-1006 (To Do), which names it and says in terms that it "does not scope" it, and RD-994 (Testing), which cites it at an older line. So it is named but not ticketed. Suggested ticket: Task, Low, security/records: add the key (or use CONFIG_CHANGE) and a cell that every `AUDIT_ACTIONS.X` use has a key; one-word choice for the builder. It would ride in N-K (same file, same audit area) if ticketed in time.

### MPS Calculator: one lane, two keys (re-run of the census and the predicate)

Result: **2 buildable keys, MPSCALC-195 and MPSCALC-316, as one developer-docs and wording lane, M-G.** The zero SWEEP-1115 gave for the rest still holds; the control that SWEEP-1115 used (MPSCALC-415 was found by the same predicate) now reads as landed (#217, Done).

| lane | keys | files at main 317bbb14 | size | gate | notes |
|---|---|---|---|---|---|
| M-G | MPSCALC-195, MPSCALC-316 | `docs/ENGINE.md` (195: the accepted engine-target sentence), `docs/API.md` and `docs/api/openapi.json` (316: the agreed sentence), `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` line 1436 (316: the refusal sentence), generated `web/src/api/generated/**` via `sync-contract.mjs` | S to M | G2 (docs words read against code) | the one C# edit is a string; see question 1 |

- **MPSCALC-316.** Ruling C-108 (the product owner's 2026-11-11 14:34 acceptance of all 29 quick recommendations, row quoted in `CLARIFICATIONS.md` line 2711): "Accept all four. Each brings text into line with what the product does", and "Work owed ... 316: the remaining places comment 40472 lists." Comment 40472 lists the places that still say 100 characters: printed at main: `QuoteEndpoints.cs:1436` still reads `quoteRef is at most 100 characters and customer at most 200.` (the sentence is on 1 line, control: the same file's other lines print), and `docs/api/openapi.json` carries `maxLength: 100` at lines 988 and 1036 (a schema value; the agreed sentence goes in the `description` beside it). The docs sentence itself is already on main (`docs/API.md:441`: "at most 100 UTF-16 code units (an emoji counts as two)"). Ticket text itself says the choice is "state the unit once".
- **MPSCALC-195.** C-108: "the drafted engine-target sentence is accepted", work owed: "the sentence into the engine docs". The 2026-11-18 ruling (comment, quoted by the ticket's last note): "195 recorded as agreed ... the engine-target sentence stays as accepted on 11 November (comment 41070, entry C-108)"; the last note adds that C-108 lists putting it in the docs "as work owed, which no read of this note shows done". Of the seven clauses the 11-18 note reads six as met. The accepted sentence's own text is not on the ticket (comment 41070 does not quote it), so the builder takes it from the B102 and B163 status files named by the ticket; if it cannot be found the key drops out.
- **What would STOP it:** the sentence text not found (195); the error sentence in C# being read as customer-facing words (it is an API refusal message shown by the app: question 1); MPSCALC-195 clause 4's "the coordinator's reading" is not a build item.
- **Conditional, not counted:** MPSCALC-189 (clause 5, a docs sentence for the Unicode id classes; the file is not named in the note I read), MPSCALC-233 (ruled C-119, refuse a clone whose typed reference already exists; the refusal answer is a new API behaviour and the earlier ruling "holds every contract change until you approve the exact name", C-116), MPSCALC-161 (ruled C-115 "Archive"; a feature with UI labels). Each carries its ruling but needs a words or contract reading.

### Security Composer: 0 firm, 1 conditional

Result: **0 firm; PCOMP-44 conditional** (control: the predicate fired for MPS and NexusAI in the same run, so a zero here is not the predicate failing to match anything).
- **PCOMP-44 (L3-6, size L, tier 1 migration and contract):** add `sm_policy_json` and `sm_policy_csv` to the output-kind enum in `packages/api-contract/src/document.ts` for lane L7. Ticket: "The plan says no card is needed; NOT started under the default ... the coordinator may start it (it shares the 0022 migration and the contract bump with L3-1, so after B322 lands)"; "Depends: L3-a none". L3-1 landed (PR #87, migration 0024). Printed at main `b4681297`: `document.ts` has 0 lines with `sm_policy` (control: the same file has `hpsm_policy_id` at 1272, which matches a looser pattern, so the grep reads the file). The migration number is now past 0027 (migrations 0020 to 0027 are in the tree). Value: low until L7 (which waits on the reviewer-round hold). I count it as buildable only if you say start (question 3).
- **PCOMP-52 is already built:** the policy PDF table of contents exists at main (`packages/renderers/src/policy-document.ts:53 to 60` "B323 (plan L6-1, gap D08): /3 adds the table of contents", `POLICY_PDF_TOC_TITLE = "Contents"`; `document-pdf.ts:147 to 176`; `document.ts:49 to 53`), and the ticket's 11-11 comment says "Still open: the build of the table of contents". Class L, not a build.
- Composer open alerts and PR #85: not re-read; main unchanged since 11-15.

## JOB 2: why the rest is blocked

Frames: MPS and Composer: every open ticket (statusCategory != Done). NexusAI: the top 60 by rank (To Do, label security or records-pass-*, priority then newest; 67 in the frame, 60 classified). The other NexusAI open tickets (819 of 879: 304 Testing and 199 Release Ready are built and waiting, 292 other To Do, 8 In Progress, 7 Put on Hold, 2 Declined, 7 more inside the label frame) are NOT classified here.

### Arithmetic (counts must sum to the open count)

**MPS Calculator, 162 open:**

| class | count |
|---|---|
| B | 2 |
| L | 46 |
| W | 35 |
| R | 11 |
| C | 1 |
| D | 11 |
| X | 4 |
| P | 8 |
| S | 21 |
| O | 23 |
| sum | 162 (open count 162: holds) |

MPS arithmetic: 2 + 46 + 35 + 11 + 1 + 11 + 4 + 8 + 21 + 23 = 162.

**Security Composer, 78 open:**

| class | count |
|---|---|
| B | 1 |
| L | 4 |
| W | 5 |
| R | 7 |
| H | 24 |
| C | 3 |
| D | 6 |
| P | 17 |
| S | 9 |
| O | 2 |
| sum | 78 (open count 78: holds) |

Composer arithmetic: 1 + 4 + 5 + 7 + 24 + 3 + 6 + 17 + 9 + 2 = 78.

**NexusAI top 60 by rank (frame: 60 of 67; the 7 below rank 60 are RD-718, 650, 569, 504, 55, 393, 54, unclassified):**

| class | count |
|---|---|
| B | 5 |
| F | 3 |
| L | 4 |
| W | 5 |
| R | 23 |
| H | 3 |
| D | 3 |
| X | 2 |
| P | 9 |
| S | 1 |
| O | 2 |
| sum | 60 (open count 60: holds) |

NexusAI arithmetic: 5 + 3 + 4 + 5 + 23 + 3 + 3 + 2 + 9 + 1 + 2 = 60.

### Keys by class (key numbers only; MPSCALC-, PCOMP- and RD- prefixes dropped)

| class | MPS | Composer | NexusAI top 60 |
|---|---|---|---|
| B | 195 316 | 44 | 759 1008 1011 1012 1013 |
| F | - | - | 445 835 861 |
| L | 26 27 28 32 33 34 35 36 40 41 42 45 46 47 48 49 50 51 53 54 55 57 62 64 65 74 124 140 155 157 158 162 170 177 189 236 244 245 248 258 269 306 310 359 369 407 | 12 23 41 52 | 421 498 972 983 |
| W | 121 129 130 139 154 156 161 169 194 233 237 243 246 264 265 267 268 270 271 272 273 274 275 276 277 278 279 280 281 282 283 286 287 368 402 | 11 79 89 128 129 | 473 487 702 714 989 |
| R | 69 75 76 79 80 82 83 110 288 314 360 | 9 70 71 73 76 91 123 | 368 392 439 455 517 546 621 633 634 655 763 764 768 792 805 806 858 859 925 997 1006 1009 1010 |
| H | - | 19 20 29 31 32 33 34 35 36 37 38 39 67 68 69 72 75 84 85 86 87 88 90 92 | 742 984 1004 |
| C | 144 | 6 8 94 | - |
| D | 103 135 173 187 222 224 226 251 297 372 395 | 10 16 18 25 28 78 | 511 758 1001 |
| X | 152 153 159 260 | - | 21 364 |
| P | 149 181 212 261 284 285 315 358 | 42 45 46 47 48 49 50 51 53 54 55 56 57 58 59 60 61 | 390 420 557 578 635 820 834 845 927 |
| S | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 78 85 118 120 188 223 | 1 2 3 4 5 7 13 65 93 | 810 |
| O | 16 17 18 19 20 23 24 25 29 30 31 43 44 52 58 59 60 63 123 133 163 200 333 | 64 66 | 370 725 |

Reading notes for the classes that are not obvious:
- **MPS L (46):** 25 are seed tasks of the 2026-09-30 spec whose last note reads "Recorded; not moved" with a merged pull request, 21 are later tickets with the same note or with the build named; the note on most says "the ticket stays open" for a clause that is the coordinator's reading or a words item. These are the largest block of tickets that are not backlog work. Done rule C-79 (quoted on MPSCALC-195): "Done means merged to main, the same as Composer, with each Done-when clause met". Whether a records pass moves them is Tuesday's; I propose nothing.
- **MPS O (23):** 18 are seed tasks (E01 to E14 tickets) with 0 comments since 2026-09-30, which I did not read beyond title and one line, so whether they are built, superseded by the v13.4.1 tickets or still wanted is unmeasured; the other 5 are MPSCALC-123, 133, 163, 200, 333 (each needs a measurement or a test run that a builder, not this sweep, would do).
- **MPS W (35):** most are the v13.4.1 lane V2 to V11 tickets ("New feature, tier 2 (words)"): the ticket itself says the words go to the product owner first. MPSCALC-169, 194, 368, 402 carry a 2026-11-11 acceptance whose own text still sends the exact name or sentence to him.
- **Composer H (24):** 10 under the Guided hold (PCOMP-68, 69, 72, 75, 84, 85, 86, 87, 88, 90), 13 behind the reviewer's round (PCOMP-19, 20, 29, 31 to 39, 92), 1 on held PR #85 (PCOMP-67).
- **NexusAI R (23):** the CodeQL baseline family (768, 763, 764, 805, 806), the key and mail-secret package (633, 634), single rulings (368, 392, 439, 455, 517, 546, 621, 655, 792, 858, 859, 925, 997, 1006, 1009, 1010). RD-633's own text says "do NOT build until Tuesday rules": that one is inside your backlog grant, not Kam's (question 4).

### Holds relied on (line that sets each, date, end)

| hold | line quoted | date | names an end? |
|---|---|---|---|
| HPSM (excluded) | "no more HPSM work for the next 3 weeks or until I request something new" and "keep working on other outstanding tickets and the backlog" (Kam, live board 16:25:45 and 16:26:43) | 2026-11-19 | yes, 3 weeks (the pickup says to 2026-12-10) |
| Composer Guided hold | `CLARIFICATIONS.md` line 1298, C-71 COMP-2: "(a) Hold them all. | No Guided work until you turn it back on." (applied on PCOMP-75 comment 41225 of 2026-11-15: "not to be built while the Guided hold stands") | 2026-10-12 | no |
| Composer reviewer-round hold | `CLARIFICATIONS.md` line 1764: "The owner holds the review until the reviewer's current review round ends ... lane 3a stays blocked until then"; C-92 K6: "the content release waits until the reviewer's current review round ends" | 2026-10-23 ~11:32 | no |
| Composer held PR #85 | label `held`; PCOMP-67's fix rides that branch ("PR #85 is not landed") | 2026-10-21 | no |
| NexusAI picomatch dated step | RD-1004: "allowed through the end of 2026-12-18 in Sydney, or until a fix" | 2026-11-18 | yes, 2026-12-18 |
| NexusAI no alert dismissed without Kam | C-190 (cited on RD-763, 764, 806, 810) | standing | no |
| MPS hosted deploy | `CLARIFICATIONS.md` line 1708: "A hosted deploy of code main 5d96a3dc ... not ruled (the hosted showcase runs e027ebd0, relayed); every sentence of the earlier sections that waits on one still waits" | recorded 2026-11 | no |

### Candidate decisions, ranked by tickets freed (at most 5 per project; no cards written)

Prior-ruling check: `decision_queue.sh prior` on the subject words of five of them (output: for the NexusAI viewer-route, unparsed-body, and SETTINGS_CHANGE phrasings, 0 to 3 unrelated messages; for MPS and Composer, unrelated cards; none answers any of them), then `grep` of each project's `1_Project_Definition/CLARIFICATIONS.md`.

**MPS Calculator**

| # | decision (one sentence) | frees (keys) | already decided? |
|---|---|---|---|
| M1 | Approve one words pack (labels, proposal text, help topics, the Enterprise book, hint catalogue) for the v13.4.1 lanes V2 to V11 so builders may use it. | 35: 121 129 130 139 154 156 161 169 194 233 237 243 246 264 265 267 268 270 271 272 273 274 275 276 277 278 279 280 281 282 283 286 287 368 402 | Partly. D-02 to D-14 (C-45) rule the features in, "the Enterprise text to the product owner as words" (MPSCALC-277); C-116 holds "every contract change until you approve the exact name"; C-109 (b) keeps developer docs out of word review. No ruling approves the words themselves. |
| M2 | Authorise a hosted deploy of main (317bbb14) and renew the seed identity's expired client secret (AADSTS7000222, MPSCALC-395). | 11: 103 135 173 187 222 224 226 251 297 372 395 | No: `CLARIFICATIONS.md:1708` "not ruled". MPSCALC-144 has a ruling (card mpscalc-large-format-manual-items-1017 = b, 2026-10-17) that waits on a deploy being live. |
| M3 | Answer the open Questions for Kam as one sheet (Q-03 brand, Q-09 roles, Q-10 thresholds, Q-13 service costs, Q-14 device rules, Q-16 retention, Q-17 fleet size) and rule the four design-rule tickets (110, 288, 314, 360). | 11: 69 75 76 79 80 82 83 110 288 314 360 | Partly: Q-12 and Q-19 were answered 2026-11-11 ("Confirm", MPSCALC-78 and 85 are counted in class S); D-10 a (Review warnings at the reviewer's three values) reads as answering Q-10 in MPSCALC-286's text but no note on MPSCALC-76 says so; MPSCALC-288 was ruled 2026-10-25 (keep listing) with a separate reject rule owed. |

Not a decision, and the largest lever on the MPS count: the 46 class-L tickets need a records move under Done rule C-79 (Tuesday's, not the product owner's). The 23 class-O tickets need reading first.

**Security Composer**

| # | decision | frees | already decided? |
|---|---|---|---|
| C1 | Say when the reviewer's current review round ends (or lift the hold), so lane 3a, the L1 and L2 content tickets, and the Essential Eight mapping review may start. | 13: 19 20 29 31 32 33 34 35 36 37 38 39 92, and it unblocks the 17 class-P tickets behind them (L3 to L9) | No end is named by either line (table above). K1, K3, K4, K5, K7, K8, K9, K10 are ruled (C-86 to C-96), so only the timing is open. |
| C2 | Turn Guided back on, or confirm it stays off for good (then the ten tickets close as not wanted). | 10: 68 69 72 75 84 85 86 87 88 90 | No: C-71 COMP-2 (a) says "until you turn it back on", no date. |
| C3 | Seven owner's calls: PDF fonts for CJK/Arabic/emoji (+17.9 MB image, PCOMP-70), refuse DEL/C1 characters or keep (71), the Guided UX review decisions a to c (73), hide unbuilt controls or build the top two (76), engagements read-only on a content release (91), footer sizing (123), and the migration-tolerance design call (9). | 7: 9 70 71 73 76 91 123 | C-71 ruled the other COMP-1 to COMP-17 rows 2026-10-12; none of these seven. |

**NexusAI (top 60 by rank)**

| # | decision | frees | already decided? |
|---|---|---|---|
| N1 | Rule the roles-UI section B and C word pack and the one front-end rule (hide or disable a control a viewer cannot use, or show the refusal in plain words). | RD-989 and the shell lanes' wording: 1 in the top-60 frame, and the roles-UI program tickets RD-928 to RD-957 (30, none started except L0, L2 and parts) as measured in SWEEP-1115 | Partly: section A, twelve rules, ruled 2026-11-06 21:12; B and C not sent. |
| N2 | Disposition of the CodeQL baseline alerts: may builders restructure the guards in RD-763 and RD-764 (12 alerts) or record a reading and leave dismissal to Kam. | 5: 763 764 768 805 806 | Partly: C-190 (no dismissal without Kam) and RD-810 ruled 2026-11-16 22:44 "leave the alert open, recorded as intended". |
| N3 | Rule the mail-secret and key-input package: re-encrypt plaintext secrets at boot (RD-633 proposal), what to do about a guessable machine-id input on App Service and dev (RD-634 "goes to Kam with the package"), and key drift overwriting secrets with null (RD-635). | 3: 633 634 635 (and the words 714, 702, 636) | No ruling found. RD-633 says "do NOT build until Tuesday rules": it may be Tuesday's under the grant. |
| N4 | One group answer for unparsed request bodies: a viewer gets 400 or 403 where a route has its own admin check, and the development error handler's text. | 2: 1009 1010 | No. RD-1010: "needs one decision for the group". |
| (single) | Fourteen rulings that each free one key: 368 392 439 455 517 546 621 655 792 858 859 925 997 1006 | 14, one each | Each ticket's own text says so; none found answered. |

### Already answered, therefore buildable or already built (found)

- Buildable on the ruling: RD-175, RD-349 (N-L), RD-759 (N-O), RD-1011 default (N-K), MPSCALC-195 and MPSCALC-316 (M-G). Ruled and queued but not read to lane shape: RD-433, 522, 610, 612, 622, 578; MPSCALC-161, 233.
- Built on main while the ticket reads open (evidence above): RD-532, RD-577 (`server.js` at about 18562: `keyVaultStatus` now reads the corrected state, with a comment naming RD-577 and RD-518), PCOMP-52, and from SWEEP-1115 RD-421, 972, 983, 498.
- Answered but ticket open: MPSCALC-120 ("Yes. It is already the practice and is written down", 2026-11-11), MPSCALC-78 and 85 ("Confirm"), MPSCALC-188 (ruled (a), record only, no code), RD-810 (ruled: leave open), MPSCALC-195 (six of seven clauses read met).

### Stale or duplicate candidates (nothing proposed closed)

| key | evidence |
|---|---|
| RD-532 | banner z-index 10000 above overlay 9999 at `static/css/open-access-banner.css` 12 to 18, comment cites the ruling |
| RD-577 | `keyVaultStatus` corrected at main; comment cites RD-577 and RD-518 |
| PCOMP-52 | TOC built at main (`policy-document.ts`, `document-pdf.ts`, `document.ts`) |
| PCOMP-5, PCOMP-7 | last comment 2026-10-23: "stale" and "superseded" (guide moved to v1.5) |
| PCOMP-13, PCOMP-65 | comment: closing as not reproduced is the coordinator's; an informational note, nothing to build |
| RD-300, RD-564 | status Declined but counted open by Jira (statusCategory != Done) |
| MPSCALC-1 to 14 | umbrella epics of the 2026-09-30 seed; children are the 46 class-L and 23 class-O tickets |
| PCOMP-1 to 4 | umbrella tickets ("Grouping rule ... Member rows") |

## EXCLUDED and why

- **HPSM-POC (HPSMPOC board, HPSM-POC repository, project folder): excluded by Kam's hold to 2026-12-10 and by this commission; nothing of it was swept, counted, read or listed.** (The hold file under `tuesday/holds/` was also not opened.)
- Not swept: Vision Sales Portal, myPKI, CypherKey, Lead_Bot and other Datasec projects (not in the commission).
- NexusAI tickets in Testing (304) and Release Ready (199): built and waiting, not candidates.
- Anything needing a deploy, UAT hold or Partner Center step: outside the sweep.

## QUESTIONS for Tuesday

1. **M-G and the C# string:** C-108 accepts the sentence "in the remaining places comment 40472 lists", and one of them is an error message in `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:1436`. Developer docs are out of word review (C-109 b); is an API refusal message a developer word or a customer word? Default: build the docs and the schema description, leave the C# string to a words pass, which still frees MPSCALC-195 and half of MPSCALC-316.
2. **N-K against RD-929:** RD-929 (Opus, `backend/server.js`, drafted after N-J) and N-K both change `server.js` and the capability pending list. Run N-K inside RD-929's lane, or after it? Default: after.
3. **PCOMP-44** (enum values for a lane that waits on the reviewer-round hold): start it now, or leave it with the rest of the sample-policy program? Default: leave it.
4. **How many of the class R tickets are Tuesday's own under the 11-06 backlog grant?** RD-633 says "until Tuesday rules"; SWEEP-1115 answers say "Decisions are Tuesday's under the 11-06 backlog grant; none is Kam's". If most of the 23 NexusAI class-R and the 11 MPS class-R are within the grant, the decisions above are yours, not a question list for Kam.
5. **RD-1011:** refuse all four routes (ticket's proposal and my default), or leave `discover-tables` and `describe-table` open to a viewer?
6. **Records:** the 46 MPS class-L, 4 NexusAI class-L and 4 Composer class-L tickets are landed work. Do you want a records pass to move them (Done rule C-79), or leave them?
7. **Declined:** RD-300 and RD-564 are Declined yet open in Jira's category. Intended?

## FOUND / TESTED / HOW

**FOUND.** 10 buildable keys (NexusAI 7, MPS 2, Composer 1 conditional); 3 serial NexusAI lanes plus a spare; one MPS docs lane; one census finding to ticket (SETTINGS_CHANGE); 3 built-but-open tickets (RD-532, RD-577, PCOMP-52); 10 candidate decisions; the MPS board is mostly words (35), landed work (46) and unread seeds (23); the Composer board is mostly two holds that name no end (23 of 24 hold keys) and an unbuilt chain (17).

**TESTED.** (a) Counts: `board_count.sh` through `bc.sh` for open and created-since-2000 in MPSCALC, PCOMP, RD; Done and open sets dumped by `jqdump.py`; arithmetic controls and `comm` against the 11:10 key lists; positive controls named above. (b) Origin: `gh api -X GET` for commits, pulls, user (count 1 per project) and recursive trees. (c) Ticket text: `jdesc.py` for 34 NexusAI tickets (descriptions 1,100 to 1,500 characters, up to 6,000 for the lane keys' fix shapes), ten ruled NexusAI tickets, `lastc.py` for all 105 non-seed MPS tickets and all 78 Composer tickets (description head and last comment head, 260 to 330 characters; 1,500 to 2,600 for about 14), `jcom.py` for MPSCALC-316 and 195. (d) Code at main: `server.js` (22,800 lines) and `static/js/index.js` (9,404) fetched and grepped; `capabilities.js`, `accessAudit.js`, `entraProvisioning.js`, `cspReport.js`, `index-styles.css`, `open-access-banner.css/js` by `gh api` contents; MPS `QuoteEndpoints.cs`, `openapi.json`, `API.md`, `ENGINE.md` by `rg.sh`; Composer `document.ts`, renderers files. (e) Exact-token scan for `SETTINGS_CHANGE` over 403 tickets (descriptions and comments). (f) `decision_queue.sh prior` five times (read-only); grep of three `CLARIFICATIONS.md` files for the holds and rulings quoted.
**NOT tested:** any test, build or server (nothing run; a build seat holds the NexusAI lock); the NexusAI tickets below rank 60 and outside the label frame (819 of 879 open); 18 MPS seed tasks with no comment (read by title only); every class is my reading of a description head and the last comment, not of the whole ticket; RD-175's and RD-349's exact colour choices; RD-578, RD-390, RD-433, RD-522, RD-610, RD-612, RD-622, MPSCALC-161, 189, 233 to lane shape; whether the Composer reviewer's round has ended (not readable here); the AI client library's error class location for RD-1008; hosted state of anything (no az); CodeQL and Dependabot alert counts (not asked this time); the roles-UI program state since SWEEP-1115 beyond what the RD-1011 and RD-989 texts say; `decision_queue.sh show` (not run). Limits met: a zsh unquoted-array split (rewritten with an array), a hook refusal of an unquoted `$F` loop (rewritten under `bash`), and `grep -E` repetition limits on two long-line greps (rewritten); no data harmed, nothing written to any board, repository or host.

**HOW.** Instruments, dumps (`*_open.tsv`, `*_done.tsv`), per-ticket flags (`mps_flags.tsv`, `pcomp_flags.tsv`), reading files (`rd_read_a.txt`, `rd_read_b.txt`, `rd_read_c.txt`, `mps_lc1.txt`, `mps_lc2.txt`, `pcomp_lc.txt`), the class map (`classify.py`, `classes.json`) and the fetched mains (`server_main.js`, `index_main.js`, `css_main.css`, `rd_tree_blobs.tsv`, `pc_tree.txt`) are in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/sweep1630/`. Clocks from `date`. Document built whole by `build_doc.py`, written to a temp file beside the target, then `os.replace`.

READ-WHOLE-BY-TUESDAY: ____
