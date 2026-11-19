STARTABLE: YES - main 46050e25 read at source, both tickets read whole, the frozen patch (four gates, the audit path helper, the pending list, two rewritten tests) applies on scratch copies with node --check rc 0 in all three modes, the old-answer census found no test pinning a viewer's answer on the four routes but FOUR hand-kept expectations that move (capabilities.js pending list, rd988 count, rd978 scan pin, the generated inventory), slot 5 free, stamp_check rc 0 (199 of 199 claims measured)

# B1733 DRAFTER REPORT - SEAT-N157, NexusAI lane N-S: RD-793 and RD-990 (data-source writes admin-only; audit row full path)

Drafter: an Agent-tool drafter for Tuesday (s292). Clocks from `date`: first 11:18:27, then 11:23:08, 11:31:03, 11:40:14, 11:40:36 AEDT Thu 19 Nov 2026 (plus the writes after). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1733_SEAT-N157_nexusai-lane-ns-datasource-admin.md` (259 lines, 87375 bytes, ASCII, sha256 prefix f0559d8a59d4c0d1 at the final stamp_check; 5 four-underscore lines: four slots and the last line). Sidecar `.measured` (199 lines). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s292/d1733/`.

## BLUF
- One lane, one seat, serial, six commits: A793 (four `requireAdminFor` gates in `server.js` +12, the pending list in `capabilities.js`, two existing tests whose hand-kept numbers move), A990 (`requestPath` helper in `accessAudit.js` used by both audit rows, `server.js` +2 -2), I (the regenerated `docs/role-capabilities.json` and `docs/ROLE-CAPABILITIES.md`, by the tool), T793 and T990 (two new test files, made inside the chain), K (counts). Model C2 Sonnet (pilot), gate G1 Opus 5.5 (Tuesday's ruling), HARD STOP proposed 17:00 AEDT.
- The sweep's STOP condition ("the census compares a hand-kept expectation, then the lane needs an addendum") IS MET, and the kit is that addendum: `backend/services/capabilities.js` `PENDING_GATE['RD-793']` lists SIX routes (the four and the two `/test` routes); `rd929` recomputes it from the committed inventory; `rd988` T7 pins `requireAdminFor(` = 30 in `server.js` (34 after); `rd978` pins the scanned gated-route count through `GATED_SINCE_REVIEW` (60 and 45 become 64 and 49).
- No existing test sends one of the four routes as a viewer and pins the answer. The two that send any (`rd800`, open window; `rd994` U-OTHER, unit) are unaffected.
- Express measured on the project's own 5.2.1: the RD-990 defect is real, `req.baseUrl` plus `req.path` would add a trailing slash the client did not send, so the helper reads the path part of `req.originalUrl` below a router and keeps `req.path` below none.
- CodeQL: STEP CQ runs `pr_codeql_check.sh` twice (at the A990 head before the waiter, at the K head before the push), tables into STATUS `## CodeQL`, rc 1 a MAJOR and a landing blocker. ONE jest acquisition (the two inventory drives and the three verifies inside it).

## FACTS RE-MEASURED (instrument -> result; each has a claim line in the sidecar)
- `gh api -X GET .../branches/main` (11:18, again 11:40) -> `46050e25f8b0b6acc972a0e033ea9a738b57b7d4`, tree `49793dfa56c5640b495d010989ee2f3b75baf364`, the #229 merge; open PRs -> 0; `compare/46050e25...main` -> identical; `compare/46050e25...37fb1bcb` -> behind (the ancestor control); `git/matching-refs/heads/b1733` -> 0 (control: `heads/main` 1).
- Tarball of 46050e25 into scratch; `git hash-object` of eight files equals the contents API sha for each (`server.js` 0335a98ea26f, `accessAudit.js` 88ccb423d90f, `capabilities.js` 675c480901df, `rd988` f33fe0997267, `rd978` 74681a9a61dd, the JSON ca762e459b84, the MD 1da0f520c929, counts 1b0fcf15967b); `server.js` 22788 lines; counts file 6041 / 382.
- Jira GET (`jget.py` shape of d1726, project `.env` in-process): RD-793 To Do High Task, labels operations s89r security, 1 comment; RD-990 To Do Medium Task, labels records-pass-1115 roles-ui-2026-11 security, 0 comments; token pattern in output -> 0.
- `awk NR==n` at 46050e25: the four registrations 15947, 16010, 16031, 17565 (each opens with `try {`, or `const dsId` at 17566); `requireAdminFor` 19081; siblings 15817, 15847, 17231; `path: req.path,` at server.js:556 and accessAudit.js:50; the require line at :462; `requireAdminFor(` count 30 (definition + 29 calls).
- Frozen patch (`apply1733.py`, three modes on scratch copies): `node --check` rc 0 on every patched file; `server.js` A793 +12 -0 blob 655b807ec963, A990 +2 -2 blob e2d8a82993cd, both +14 -2 blob 668e343f3207, A793-then-A990 equals both-at-once for `server.js` and `accessAudit.js`; `accessAudit.js` +11 -2 blob d36cf0c717ab; `capabilities.js` +1 -2 blob 1c58b35ad9e6; `rd988` +2 -2 blob 60150600ae3b; `rd978` +5 -3 blob ca45a65f2d8a; `server.js` non-ASCII bytes 3913 -> 3913; bidi/zero-width added 0; CRLF 0; `requireAdminFor(` 34 after.
- `predict1733.js` (the tool's own `scanFile` over the patched copy): gated routes/writes BASE 60/45 (the four read `[]`), HEAD 64/49 (the four read `["requireAdminFor"]`); `rd929` recomputation over the committed rows with viewer 403 on the four: equals the new list `true`, equals the OLD list `false` (control that the cell can fail); viewer counts base `400:29 403:71 404:10`, head `400:28 403:75 404:7`.
- Express: `routerpath.js` required the project's own `node_modules/express` (5.2.1) by absolute path: router-answered GET `/api/setup/entra-provisioning` read `req.path` `/`, `req.baseUrl` the mount, same at `res.json` and at `finish`; PATCH `/api/feedback/6` read `/6` and `/api/feedback`; the plain route read empty `baseUrl`; the helper returned the full path with the query dropped and `/api/plain` unchanged; with a trailing-slash request it kept the slash.
- Helper on the patched `accessAudit.js` (`node -e`, no server): `/api/x`, `/api/feedback/6`, `/api/setup/entra-provisioning`; keys of `denialDetails` six; exports `denialDetails`, `denialReason`, `requestPath` (BASE exports two, `requestPath` undefined).
- Slot program (`slot1733.py`): 8 controls equal to their kits; 138 non-`.pre-` files of 18-19 Nov scanned; slots named 0-4, 6-10, 12-16; free 5, 11, 17, 18; slot 5 band 23200-23839; `lsof` 0 rows (control 12-13 listeners without the range); trees `old2 probe7 new11 mut21 v23 chk41 chk52` all slot 5, none existing; no `b1733` path under the project (`.tools`, root, Briefs).
- Open alerts: 22 (13 on `server.js`), control `state=fixed` 100 rows; #233 `js/user-controlled-bypass` at `server.js:16851` sits after three of the four insertions.
- STATUS files of 17-19 Nov: 24, 23 end `READY`, the records seat B1730's ends `RECORDS B1730: PENDING | JIRA pending`; no live pane `Datasec/NexusAI-*` (`tmux`: tuesday, fleet-monitor).
- `readers1733.py`: frame 466 `.js` (384 `.test.js`); run list 34, helper 1, non-jest 0, scanners 73 (58 outside the run list); `census1733.py`: 24 files carry an indicator (23 tests, 1 helper); `tests/` 28 files, 0 name `data-sources` (control: `first-run-setup.js` 12).
- Model-routing rows by `awk NR==n`: P4 :50, C2 :92, C3 :93, G1 :108, G2 :109; `models_latest.json:23` `claude-sonnet-5-5`; `CLARIFICATIONS.md:2067` the landing rule; `build.yml:29/:64/:93`; `deploy-demo.yml:29-:32`.

## OLD-ANSWER TEST CENSUS (summary; the table is in the kit's THE CENSUS)
Frame: every `.js` under `__tests__` and `tests` (466 files); indicators: a data-source route literal, the inventory or its readers, `PENDING_GATE`/`ROUTE_CAPABILITY`, `requireAdminFor`. 24 files hit; dispositions:
- **REWRITE (in A793):** `rd988-feedback-triage-admin-only.test.js` (`toBe(30)` -> 34, title), `rd978-handler-span-scan.test.js` (`GATED_SINCE_REVIEW` +4, title and comment), the product file `capabilities.js` pending list.
- **REGENERATE (commit I):** `docs/role-capabilities.json` (four rows: viewer, `gateInHandler`, `capability`; meta), `docs/ROLE-CAPABILITIES.md` (four rows, three count rows, generated-at line).
- **UNAFFECTED as files, order-sensitive:** `rd929` (red between A793 and I by design, green at I), `roles-foundation-route-census` C5 (needs both docs regenerated together), `rd958-viewer-write-gates` X2 (`kept: 2` holds only because the key `RD-793` stays: Q-4).
- **UNAFFECTED:** `rd800` (open-window DELETE; the gate lets it through and the log line follows the gate; control `:133` POST already gated passes in the same harness), `rd994` (unit), `rd761-law-writers`, `rd830`, `data-source-save-log-redaction`, `discover-tables-tenant-mask` (POST/PUT//test only; `DELETE` literal 0, `/tables` route 0), `rd958-write-gate-path-variants`, `rd964`, `rd965`, `rd966`, `rd968`, `rd932-*`, `rd972`, `rd1007`, `rd691`, `rd977`, the seed helper.
- **RD-990 side:** no test pins a relative path in a row (13 audit-reading files; router-route words only in `rd966:62-:64`, status literals); `rd932-access-audit-unit` U2 builds a stub with no `baseUrl`, which keeps `req.path`.
- Remaining risk said in the kit: paths built in helper modules and browser tests are not followed (only `roles-inventory-seed.js` is a helper and names no route; `tests/e2e` names none); backstop = chain step 4 (all readers at the product commits plus the regenerated inventory, before any new test file exists).
- Static callers: only the first-run wizard (`first-run-setup.js` :1997 :2022 :2317 :2423) calls the four routes; `admin.js` calls PUT only.

## D-DECISIONS (the drafter's)
- D-1 Two product commits (A793, A990) plus I, so each ticket has its own commit and the inventory is regenerated once on the final product tree; `rd929` is red between A793 and I by design and no jest runs there.
- D-2 The gate is the FIRST statement of each handler (before `dsId` and the `Deleting:` log line in the setup delete), written as a 3-line block identical in the four places; reuse of `requireAdminFor` (the ticket's `adminGateRefuses` one-liner is that helper today).
- D-3 `requestPath` in `accessAudit.js`, `req.path` when `req.baseUrl` is empty, else the path part of `req.originalUrl` (fallback `baseUrl + path`); used by `denialDetails` and, through the existing import at :462, by the STATE_MUTATION row.
- D-4 `PENDING_GATE['RD-793']` keeps its key with the two `/test` routes (keeps `rd958` X2 green; the routes stay viewer-reachable).
- D-5 The BASE control drive of the inventory (B1555's rule) plus a drift D rule: unexplained drift between the committed JSON (2026-11-17) and the BASE drive is a STOP.
- D-6 CodeQL twice, CQ-1 before the waiter (a reshape is cheap there), CQ-2 at the K head before the push.
- D-7 Cells: rd793 in two boots (enforced with real created sources, open), the viewer calls act on real ids so the BASE red proves the handler ran (the effect cells E1-E4 re-read the source after the refusal); rd990 reads both audit rows through the administrator's export, with a planted query word that must be absent from every row.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- Q-1 Gate placement and helper: DEFAULT `requireAdminFor` as the first statement of the four handlers. Alternative: after the existing `try {` (not recommended: a thrown helper would then answer 500 through the catch).
- Q-2 The refusal text: DEFAULT the existing `Admin access required` (no new word).
- Q-3 The path expression: DEFAULT the `requestPath` helper described (originalUrl path part below a router). Alternative: `req.baseUrl + req.path` (the ticket's first option; reads `/api/setup/entra-provisioning/` with a slash the client did not send, measured).
- Q-4 The two `/test` routes (`POST /api/data-sources/:id/test`, `POST /api/setup/data-sources/:id/test`; viewer 404 today, they dial with a stored credential): DEFAULT left out and kept on the pending list under the `RD-793` key; the records seat files a ticket for them and RD-793 is not closed as complete until then. Alternative: gate all six in this lane (two more handlers, two more inventory rows, `requireAdminFor(` 36, `rd978` +6, key removed and `rd958` X2 rewritten to `kept: 1`): larger, not named by the ticket.
- Q-5 The Entra router's own audit row (`backend/routes/entraProvisioning.js:167`, relative path inside the router): DEFAULT left out (a third file; the ticket calls it not measured). Alternative: include it with the same helper.
- Q-6 The rewrites of `rd988` and `rd978` inside A793 (the kit's FOUND 5 carve-out of the "pinned old answer is a STOP" hold): DEFAULT yes.
- Q-7 CodeQL cadence: DEFAULT CQ-1 and CQ-2 (about 3-6 minutes each, UNMEASURED for this tool). Alternative: CQ-2 only.
- Q-8 Slot 5 (named by no file of 18-19 Nov by the strict regex; a loose regex hit 17 noisy files) and HARD STOP 17:00 AEDT: DEFAULT as written; alternatives slots 11, 17, 18.
- Q-9 `N3` (the one anonymous cell, expected 401 from the global sign-in gate): DEFAULT kept; if the seat's BASE read is not 401, the candidate is recorded and dropped.

## CHAIN INPUTS (each input produced by an EARLIER step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| Step 0 | the kit, this report, B1726 STATUS and kit, B1555 kit, B1728 kit, codeql README and GATE_STEP, B1727 and B1729 verdicts | BASE (files exist) |
| Step 1 | clone of 2_Project_Files, deploy key, `.tools/b1728/clone` identity | BASE |
| Step 1b | the clone at BASE; census programs the seat writes | Step 1 |
| A793, A990 | apply script, msg files, anchor counts | Step 1b(i), seat before lock |
| CQ-1 | clone with BASE and A990, tool, seat-local lock | A990, BASE |
| chain 0-1 | old2 at BASE, run list | Step 1b(iii), trees |
| chain 2 | old2 clean `backups/` | BASE |
| chain 3 | new11 at A990, step 2's output (BASE control), `invdiff.py` | A990, step 2 |
| commit I | step 3's two files | step 3 |
| chain 4 | new11 at I, step 1's per-file counts | I, step 1 |
| chain 5 | probe7 at BASE + PROBE files from `mkT.py --probe` | mkT.py (before lock), BASE |
| chain 6 | kept lists from step 5, `mkT.py --kept`, msg-T793/T990 | step 5, before lock |
| chain 7-8 | new11 re-detached at T990, scanner list | step 6, Step 1b(iii) |
| chain 9 | mut21 at T990, plant specs, `plants-predicted.json` | step 6, before lock |
| chain 11-12 | chk41 and v23 at T990 | step 6 |
| chain 13 | counts file from v23, msg-K | step 12 |
| chain 14 | chk52 at K | step 13 |
| CQ-2, push | clone with K head | step 14 |

## SLOTS TUESDAY MUST STAMP (recommended values; each is Tuesday's own read, not the drafter's)
- STAMP: the time and what Tuesday read (the kit lines, this report's BLUF, FOUND 5 and THE CENSUS) plus the Q-ANSWERS line. Recommended Q-ANSWERS: Q-1 first statement; Q-2 reuse `Admin access required`; Q-3 the `requestPath` helper; Q-4 leave the `/test` routes out, key `RD-793` stays, records seat files a ticket for them; Q-5 Entra row out; Q-6 yes; Q-7 CQ-1 and CQ-2; Q-8 slot 5, 17:00; Q-9 keep N3. Checks Tuesday can run before writing "checked at source": `python3 -I -B apply1733.py <tree root> <out> both` on a scratch tree of 46050e25 (expect rc 0, `server.js` blob 668e343f3207, `node --check` rc 0, `requireAdminFor(` 34), and `node predict1733.js` (60/45 to 64/49).
- HEADS AT LAUNCH: origin main `46050e25f8b0b6acc972a0e033ea9a738b57b7d4` (re-read at launch), counts 6041/382, `46050e25` an ancestor of it (identical at 11:40), `b1733/nexusai-lane-ns-datasource-admin` absent at origin, open PRs 0, newest NexusAI STATUS ending `READY` is B1728 (`READY B1728: 2ec6937792ffc48abbd11a2928b293c954e14cd5`); note B1730 (records seat) ends `RECORDS B1730: PENDING | JIRA pending` and is excluded by REFUSE 4(a).
- LAUNCH WINDOW: load1 about 5.0 at 11:40 (re-read), live seats beside: none writing a path of OWNS-B1733, jest FIFO length 0 and no holder (locks dir holds `queue-docker`, `queue-jest`, `released`), one waiter.
- HARD STOP: 17:00 AEDT Thursday 2026-11-19 (weekday confirmed by `date -j -f`), PREDICTED need about 1.5 hours reading, census, tools, A793, A990, CQ-1, then about 2.3 hours lock hold, then CQ-2 and push.
- Launch line is in the kit (`BRIEF_SEAT_LEVEL=sonnet` inside the quotes, pane `Datasec/NexusAI-N157`).

## CORRECTIONS TO THE COMMISSION'S FACTS
- "a viewer/non-admin getting 200 today": the committed inventory shows viewer 404, 400, 404, 404 on the sentinel word (the request reached the handler); 200 only with a real id (the handler deletes). The census therefore pins on "reaches the handler", not on a literal 200.
- "the four data-source handlers get the admin check" understates the permission-table coupling: `PENDING_GATE['RD-793']` lists six routes (the two `/test` routes too), so four leave and two stay; `rd958` X2 pins the key count 2.
- The sweep's "`rd929` (205 routes) reading a changed `gateInHandler` as a red census": the inventory has 203 rows, and `rd929` does not read `gateInHandler`; it recomputes the pending set from the viewer column. The cells that DO move are `rd988` T7 (`requireAdminFor(` 30), `rd978` (gated-route pin) and the pending list.
- The ticket's `adminGateRefuses` guard is today the helper `requireAdminFor`; the sibling writers' comment names "setup-mode-aware admin gate".
- Line pointers hold at 46050e25 (556, 50, 15947, 16010, 16031, 17565, 19081); RD-990's "server.js:540" is 556 as the sweep said.
- RD-990 is not three audit rows but at least three PLACES with a defect; one more audit call (`entraProvisioning.js:167`) shares it and is left out (Q-5).
- Counts file at main is 6041/382 (the sweep's earlier text spoke of 6009/380 at an older main).

## UNMEASURED
- Every HTTP answer of the new cells (no server, no jest by the drafter): the create of four sources under `bootShape` (the `rd830` form ran under `bootServer`), the viewer's BASE 200 bodies, the anonymous 401 of N3, the audit export rows for the three router places (PREDICTED from the Express probe and `rd932`); whether `rd800`'s open window still prints the `Deleting:` line after the gate (PREDICTED yes; the gate returns true in the open window).
- The regenerated inventory (the BASE drive's drift against the committed 2026-11-17 file; `meta.fence` machine drift); the capability sentence the tool derives; the page counts after the drive.
- The scanner list and per-file reader counts at the seat's base; the CodeQL verdict (the tool was not run by the drafter; B1731 measured it on #229 only); durations (CodeQL 3-6 minutes RELAYED from B1728, lock hold RELAYED from B1726/B1555).
- The hosted CodeQL check on the landing head; Linux; a browser render of the first-run wizard.

## OUTSIDE-THE-FENCES DISCLOSURE
- Wrote only the kit, its `.measured` sidecar (`stamp_check.py --init` then my `measure1733.py` rewrote it; an earlier init skeleton was moved to scratch as `old_init1.measured`, not deleted) and this report, plus scratch files under `fleet/state/s292/d1733/`. The kit was edited in place several times with Python replaces (one edit stripped backticks around two-character spans and merged some adjacent code spans; I repaired the new-cells section and the first findings; a few enumerations remain merged spans, cosmetic only).
- Read-only reads outside Tuesday's tree: the NexusAI project's Briefs STATUS files (last lines, the B1726 `## Corrections` heading count), `.tools` listings (`b1555`, `b1726`, `b1728`) and the `locks-laptop-1017` listing, `1_Project_Definition/CLARIFICATIONS.md` line 2067 only, `session-tools` existence, `tmux list-panes`, `lsof`.
- `gh api -X GET` only under the NexusAI `GH_CONFIG_DIR` (login count 1): branches, compare, matching-refs, pulls, commits, contents (sha), code-scanning alerts (open and fixed), the 80 MB tarball of 46050e25 into scratch. Jira GET only (RD-793, RD-990). No `decision_queue.sh`, no mail, no push, no PR, no project file edited.
- Ran `node` on scratch copies (`--check`, `predict1733.js`, `routerpath.js`), and required the project's own `node_modules/express` by absolute path from a scratch script (read-only; it opened a loopback server on an ephemeral port for under a second). No jest, no inventory drive, no CodeQL run, no project server.
- One hook refusal on my side: a `rm -rf` and two commands containing `cd` were blocked by hooks; nothing was deleted or changed by them.
