# Completable-now sweep, morning 2026-11-09 (read-only drafter, Sonnet): DELTA on the 2026-11-08 evening sweep

Base: `2026-11-08_completable-sweep-evening.md` (read whole). Clocks are `date` prints: Jira dumps 07:51:35 to 07:51:45 AEDT (own pager under `python3 -I`, each project `.env` read in-process by name, no token printed, every JQL `project = <KEY> AND ( created >= -3650d )`, paged with `nextPageToken` to `isLast`; keys HPSMPOC, PCOMP, MPSCALC, RD), GitHub reads 07:51:59 to 07:53:11 (`gh api -X GET` under each project's own `GH_CONFIG_DIR`; source read with `contents?ref=fe75d7b2` raw, line numbers printed by `grep -n`/`sed -n` over the saved raw file), tmux read 07:52:14, file read of `decision_queue.sh`: none (no card read at all). No Jira, GitHub or project write; no mail, no hosted host. Skipped by instruction: myPKI, CypherKey, Lead_Bot. Model rows: `fleet/specs/model-routing.md` lines 92 (C2 build), 93 (C3 auth/security/money design), 94 (C4 data-destroying), 108 (G1 tier-1 gate), 109 (G2 tier-2 gate, tests/docs/tooling); ids `claude-sonnet-5-5` (`models_latest.json:23`), `claude-opus-5-5` (`:17`).

## BLUF
- **Free build lanes now: NexusAI 3 (N-A RD-959+960+961; N-B RD-970+971; N-D RD-977+978+979), HPSM-POC 0, Security Composer 0, MPS 0.** N-C (RD-973) is no longer free: `b1369/nexusai-rd973-rollback-race` @ `1f3365eb` holds it (READY, waits for b1340). MPSCALC-385 and -386 are gone (landed #165, #166, Done). Records: none unowned (HPSMPOC-447/-319/-308 are the running records seat's; MPS records are done at root `13db4d11`).
- **Top lanes in launch order (pairwise file-disjoint by path, disjoint from TAKEN):**
  1. **N-A RD-959+960+961** (`__tests__/rd573-jest-port-band-outside-ephemeral-range.test.js`, `__tests__/helpers/test-server.js`, `__tests__/rd591-cross-seat-isolation.test.js`). Why first: no new cell so no counts regeneration (not in conflict with the shared `scripts/verify-expected-counts.json` that b1340 and b1369 both edit), and it must land before the staged RD-757 kit, which edits the same helper and rd591. Sonnet C2 (`:92`), gate G2 Sonnet (`:109`).
  2. **N-B RD-970+971** (`scripts/refactor-inline-styles.js`, `scripts/csp-convert.py`). Header-only form of RD-970 plus the one-pattern RD-971 needs no new test file; a new test file means a counts regeneration after b1340 and b1369 land. Sonnet C2, G2 Sonnet.
  3. **N-D RD-977+978+979** (`scripts/role-capability-inventory.js`, `docs/role-capabilities.json`, `docs/ROLE-CAPABILITIES.md`, `tests/e2e/shell-layout.spec.js`). Launch last: the generated outputs carry `originMain` and `generatedAt` (`role-capability-inventory.js:593`, `:598-:599`), so regenerate AFTER b1340 lands (09:00). Sonnet C2, G2 Sonnet.
  - **Load caution:** each NexusAI lane is a full verify (`--maxWorkers=2`) beside b1340's landing check and b1369's pending gate. Machine load UNMEASURED. If one verify only is wanted, take N-A.
- **TAKEN (do not touch):** b1340's 7 files (`__tests__/helpers/log-wrap-shape.js`, `__tests__/rd477-customer-leftovers.test.js`, `__tests__/rd798-...`, `__tests__/rd799-...`, `__tests__/rd800-...`, `backend/server.js`, `scripts/verify-expected-counts.json`) and b1369's 3 files (`backend/simpleDb.js`, `__tests__/rd973-simpledb-rollback-before-reject.test.js`, `scripts/verify-expected-counts.json`); records seat's keys HPSMPOC-447, -319, -308.
- **HPSM-POC and Composer: nothing newly filed, nothing newly actionable.** HPSM: no row created after HPSMPOC-447 (06 Nov 19:56); only change since last night is #295 landed on main. Composer: newest `updated` over 127 rows is 06 Nov 11:01 (unchanged).
- **Kam-card NEEDS-WORD:** see the section below (carried rows, none new).

## Counts (instrument: own paged dump, frame `project = <KEY> AND ( created >= -3650d )`, to isLast; evening sweep's counts are the control)
| Board | Total | By state | Delta on evening | Control |
|---|---|---|---|---|
| HPSM-POC | 447 | Done 313, Backlog 131, In Progress 3 | none | evening 447 / 313 / 131 / 3: equal. Max key 447 (control: 447 keys listed, key range reaches 447) |
| Security Composer | 127 | Done 32, Backlog 95 | none | evening 127 / 32 / 95: equal; newest `updated` 2026-11-06T11:01 |
| MPS Calculator | 386 | Done 161, Backlog 225 | Done +3 (MPSCALC-106, -385, -386; each `updated` 2026-11-08T23:43), Backlog -3 | evening Done 158, Backlog 228: 158+3 = 161 and 228-3 = 225 close |
| NexusAI | 975 | To Do 395, Testing 240, Release Ready 199, Done 124, In Progress 8, Put on Hold 7, Declined 2 | none; newest `updated` 2026-11-07T06:29 | evening 975 and every state equal |

Predicate for "changed since evening": `updated >= 2026-11-08T20:00` or `created >= 2026-11-08T21:00` over the dumped rows; hits: HPSM 2 (-319, -446, both 20:56, before the evening sweep's dump), MPS 3, Composer 0, NexusAI 0. Control: the MPS predicate fired on the three tickets known to have moved, so it can fail.

Open PRs (`pulls?state=open`): HPSM-POC 0, MPS 0, NexusAI 0, Composer 3 (#91 dependabot, #86 dependabot, #85 HOLD; `updated` 2026-10-25, 2026-10-20, 2026-10-21). Control: `pulls?state=closed` lists #295 to #290 (HPSM-POC), #166 to #161 (MPS), #181 to #176 (NexusAI), #118 to #113 (Composer). NexusAI code scanning on main: 110 open (`code-scanning/alerts?state=open&ref=refs/heads/main`, paged; evening 110, equal).

## Verification of the "known since" list
| Claim | Result | Instrument |
|---|---|---|
| MPS #165 -> main `dc1b3f0c` | TRUE: #165 (`b1368/mpscalc-385-print-pending-flushsync`) merged 2026-11-08T12:15:02Z, merge sha `dc1b3f0c` | `pulls?state=closed` |
| MPS #166 -> `31234f5f` | TRUE: merged 12:28:11Z, and `commits/main` is `31234f5f` (current main) | `pulls?state=closed`, `commits/main` |
| Then records root `13db4d11` | TRUE locally, not on GitHub: `git rev-parse 13db4d11` in the project-root repo returns `13db4d11ef18d72c...`, on local `main` and `records/b1371`; subject "records B1371 (SEAT-R193) ... MPSCALC-106, -385, -386 ... moved to Done". It is not a commit of the `2_Project_Files` repo (`cat-file` there: not a valid object) nor on `datasecau/MPS-Commercial-Calculator` (`commits/13db4d11` 422). The root repo has no remote shown by `remote -v`. Not a Jira-vs-repo conflict: Jira Done matches | `git rev-parse`, `git branch --contains`, `gh api commits/<sha>` |
| MPSCALC-106, -385, -386 Done | TRUE, each `Done`, `updated` 2026-11-08T23:43 | Jira dump |
| HPSM-POC #295 -> main `2075486b` | TRUE: #295 (`b1372/hpsmpoc-447-retry-header`) merged 2026-11-08T19:15:15Z, main `2075486b` | `pulls?state=closed`, `commits/main` |
| HPSMPOC-446 Done | TRUE (Done since 2026-11-08 20:56, so it was already true in the evening sweep) | Jira dump |
| HPSMPOC-447, -319, -308 with a records seat | TRUE on the pane: `tmux list-panes -a` at 07:52 shows a pane titled "HPSM-POC records 447, 319, 308" (cwd TUESDAY). Jira: all three still `Backlog` at 07:51 (447 updated 06 Nov 19:56; 319 08 Nov 20:56; 308 06 Nov 19:57). TAKEN | tmux, Jira dump |
| HPSMPOC-319's third push | **Done on the CI side:** the `ci.yml` main push runs are `42514097403` (`2075486b`, success, 19:15Z 8 Nov), `42296681684` (`b14b6f29`, success), `42187059450` (`eaf77b3c`, success): three consecutive main pushes success. Predicate: the last three completed push runs on `main`. Control: the list returns 6 runs, all `completed success`. For the records seat, not a lane |
| NexusAI b1340 @ `2b60ff66`, 7 files | TRUE: `compare/main...b1340`: ahead 9, behind 2, last commit 2026-11-06T20:13:35Z; the seven files as listed in the TAKEN line (`server.js` +44 -44; counts file +3 -3). Has not landed (open PRs 0; main `fe75d7b2`) | `compare`, `commits/main` |
| NexusAI b1369 @ `1f3365eb`, simpleDb + rd973 test + counts | TRUE: ahead 1, behind 0, committed 2026-11-08T11:53:47Z; files `__tests__/rd973-simpledb-rollback-before-reject.test.js` +187, `backend/simpleDb.js` +2 -4, `scripts/verify-expected-counts.json` +3 -3. No PR open. READY/waits-for-b1340 is a relayed claim, not measured | `compare` |
| Composer PRs #85 #86 #91 held | TRUE: all three open, last `updated` 21 Oct, 20 Oct, 25 Oct | `pulls?state=open` |

## Panes and branches
- `tmux list-panes -a` at 07:52: 7 panes, session `fleet`; titles include "Tuesday boot: Datasec seat startup" and "HPSM-POC records 447, 319, 308". No pane titled for a NexusAI lane (b1340 is waiting for the 09:00 default; b1369 waits; neither has a visible pane). Control: the HPSM records pane is visible, so the title column works.
- NexusAI branches `b13xx` ahead of main: b1340, b1369 (the others in `b1335`, `b1336`, `b1344a/b`, `b1354` are the landed #174 to #180 heads). HPSM-POC and Composer: no new branch number above those named last night (filter `b13[5-9]|b14|records` on HPSM returned only the old `b14/user-test-fixes`; the Composer filter returned only old `b13`/`b12x`/`b14x` branches; branch bodies not read).
- Shared file: `scripts/verify-expected-counts.json` is edited by b1340 and b1369. Any lane that adds a cell or test file must regenerate it after both land (`npm run verify -- --maxWorkers=2 --update-counts`), one at a time.

## Per-ticket tables

### HPSM-POC (main `2075486b`): 0 free lanes
| Key | Scope | Paths | Open PR / live lane | Model | Readiness |
|---|---|---|---|---|---|
| HPSMPOC-447 | host-start retry filter misses a session lost before EF's migration proper; #295 landed form (b): the file header states what the retry accepts and the gap | `api/tests/HpsmPoc.Api.Tests/Support/HostStartRetry.cs` (and the Feedback copy) | none open; records pane running | Sonnet C2 / G2 | **Records (TAKEN)**; Jira still Backlog |
| HPSMPOC-319 | the last clause "green on 3 consecutive main pushes" | n/a | none | n/a | **Records (TAKEN)**; the CI condition now reads met (3 of 3 push runs success, above) |
| HPSMPOC-308 | CI SQL Server shard | n/a | records pane | n/a | **Records (TAKEN)** |
| HPSMPOC-446 | | | | | Done |
| rest of board (HP items, hosted measurements, product-owner words, In Progress -87/-90/-91 last updated 1 Oct to 23 Oct) | unchanged | | | | no new row beyond 447 (control: max key 447, created 06 Nov 19:56). Title-only rows UNMEASURED as before |

### Security Composer (main `a54250f4`): 0 free lanes
No row created or updated after 6 Nov 11:01 (newest `updated` over 127 rows: PCOMP-116 and PCOMP-119; control: PCOMP-119 reads Done with that stamp). Rows `updated` or `created` on or after 2 Nov that are not Done: PCOMP-127, -123, -121, -120, -116, -114, -98, -23 (all Backlog, last touched 2 to 6 Nov). PCOMP-62/66/67/113/117 as the earlier sweeps (PR #85 HOLD holds -66/-67; the others await words). Nothing newly actionable. A zero is a read zero from the list and `updated` check; the Backlog bodies were not re-read (the 29 unread content rows from the morning of 7 Nov are still UNMEASURED).

### MPS Calculator (main `31234f5f`): 0 free lanes
| Key | Readiness |
|---|---|
| MPSCALC-385, -386, -106 | **Done** (#165, #166, #164; Jira Done at 23:43 8 Nov) |
| MPSCALC-334 part B, -310, -198, -221/-302/-338/-339, -118 | NEEDS RULING / held, unchanged (none `updated` since 8 Nov 20:00; control above) |
| rest (225 Backlog) | unchanged; the 66 "Recorded; not moved" rows still UNMEASURED |

### NexusAI (main `fe75d7b2`)
All lines re-read at `fe75d7b2` from raw `contents?ref=`, printed with `grep -n`.
| Key | Scope, from its own text | Paths (measured) | Open PR / live lane | Model | Readiness |
|---|---|---|---|---|---|
| **RD-959 + 960 + 961** [N-A] | E3's control expects `DIALS` itself so `DIALS = 0` stays green; comments say E2/E3 turn red only on Linux; no `afterAll` in rd573 and rd591 so temp dirs pile up | rd573 test: `DIALS` :147, loop :156, wait :165, control `toEqual` :176, `mkdtemp` :120; `test-server.js` comments :56-:58 (ephemeral range / Linux), :147 and :155 lines in rd573 mention Linux; rd591 `mkdtemp` :65 and :166. `grep -c afterAll` over rd573 and rd591 = 0 (control: `mkdtemp` hits 3, so the grep reads these files) | none; serial before the staged RD-757 kit | Sonnet C2 `:92`, gate G2 `:109` | **READY.** No new cell, no counts change. Red-first plant: `DIALS = 0`. All three tickets To Do, 0 comments |
| **RD-970 + 971** [N-B] | `readIfPresent` treats ENOTDIR / EACCES-on-parent like ENOENT, or the header says only ENOENT is skipped; end tag `\s` becomes `[\t\n\f\r ]` | `scripts/refactor-inline-styles.js` (`readIfPresent` :245, uses :262, :288); `scripts/csp-convert.py` (`SCRIPT_BLOCK_RE` :109, end tag on :110) | none | Sonnet C2, G2 | **READY**; no test named for either script (last night's tree grep), so a new test file means a counts regeneration after b1340 and b1369. Test home UNMEASURED |
| **RD-977 + 978 + 979** [N-D] | rename sentinel `zz-b1344-none`; end handler span at the handler's close; reword shell-layout header to program counts | `scripts/role-capability-inventory.js` (sentinel :38 and :96; span :214-:219 `to = starts[s+1]`; `originMain` :593/:599, `generatedAt` :598), `docs/role-capabilities.json` (`"sentinel": "zz-b1344-none"` :14), `docs/ROLE-CAPABILITIES.md`, `tests/e2e/shell-layout.spec.js` (header :54-:62, `VENDOR` :151) | none | Sonnet C2, G2 | **READY with order condition** (regenerate outputs after b1340 lands). RD-978's "43 and 29" relayed, not re-read |
| RD-973 | `setQuickQuestions` ROLLBACK with no callback | `backend/simpleDb.js` | **TAKEN: b1369 @ `1f3365eb`** | Sonnet C2, G2 | **READY (branch exists), waits for b1340**; not a new lane |
| RD-972 | session revocation tests | `backend/server.js`, `backend/jsonStorage.js` | **TAKEN (b1340 edits server.js)** | Opus (C3 `:93`, G1 `:108`) | BLOCKED behind b1340 |
| RD-974/975/976, RD-926, RD-770/772/773 | `server.js` sites | `backend/server.js` | TAKEN | Sonnet C2; Opus gate for log-injection class | BLOCKED behind b1340 |
| RD-757, RD-771, RD-798 residue | as before | test-server.js and rd591; `static/js`; `learningManager.js` | staged kits, no pane | as before | STAGED; RD-757 serial after N-A |
| RD-937 and family (RD-938/939/940..956), RD-962/963 | roles-ui shell | static pages, tests that read header/tab markers | none | Sonnet | **NEEDS WORD** (below) |
| RD-958 family, RD-927, 929..933, 964..969 | role checks | `backend/server.js` | TAKEN | Opus (C3) | BLOCKED behind b1340 and the roles core |
| RD-936 | tokens: #180 landed 6 Nov | n/a | n/a | n/a | **Records / Tuesday's call**: still To Do (updated 6 Nov 17:36, 0 comments) |
| RD-934, RD-928 | word pack; foundation | n/a | n/a | n/a | RD-934 To Do (1 comment), RD-928 To Do (1 comment); Tuesday's call |

## NEEDS-WORD items that need a Kam card (carried from the evening sweep; I re-read none of the card or ticket rows this morning, so the "exact rows" are the evening's relay)
1. **RD-937 roles-ui shell** (and RD-939/938/940..956 behind it): the evening sweep relayed that the product owner's 2026-11-06 ruling accepts the twelve section-A rules only, and marks RD-937 rows **I-002, I-003, I-007, I-008** as new word, with RD-939 starting after RD-937/938. A card needs to rule those four rows (RELAYED; not re-read here; UNMEASURED today).
2. **RD-962, RD-963** (settings.html 60 px at 390; Printing tab 2 px at 820): need a roles-ui label and an ordering call because the new shell supersedes those pages.
3. **MPS held set** (MPSCALC-334 part B, -310, -198, -221, -302, -338, -339, -118): need rulings, unchanged.
4. **Composer words**: PCOMP-62/113/117/123/127/116 await words; -66/-67 await PR #85 HOLD. No new row.
5. **HPSM-POC**: nothing new needs a card; HPSMPOC-447's option call was effectively made (form b landed as #295).

## UNMEASURED
- Whether b1340 lands at 09:00 and whether its pane exists (no NexusAI pane at 07:52); whether b1369 is gated.
- Machine load with several NexusAI verifies at once.
- Whether `roles-foundation-route-census.test.js` ignores `meta.originMain`/`generatedAt` (the inventory strips a `generatedAt` line at :665 for a comparison; the census test was not read).
- Test home for RD-970/971; RD-973's other callers.
- RD-937's section-B/C row texts (carried, not re-read); RD-974 vs RD-688 duplication.
- Composer's 29 unread content rows and Backlog bodies; HPSM title-only rows and old branches; MPS 66 unread "Recorded; not moved" rows.
- Whether Jira comment fields in the dump were complete; this sweep read the last comment of HPSMPOC-447 and -319 only.
- Why the root repo `13db4d11` has no GitHub copy (no remote shown): not investigated.

READ-WHOLE-BY-TUESDAY: ____
