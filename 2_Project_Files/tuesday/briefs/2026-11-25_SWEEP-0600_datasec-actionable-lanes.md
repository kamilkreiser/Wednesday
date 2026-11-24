# SWEEP-0600: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-25 about 06:00)

Commissioned by Tuesday (s325), Sonnet, routing row C8, read-only. Form and old state: `2026-11-24_SWEEP-1110_datasec-actionable-lanes.md` (read whole; every lane re-checked below against the boards and GitHub as they are now). Scope: Jira RD (NexusAI), MPSCALC, PCOMP. **HPSM-POC was not swept, counted, read or listed; OXPd is swept separately.** Fences kept: Jira GET only (credentials read by name in-process, never printed), `gh api -X GET` under each project's own `GH_CONFIG_DIR`, writes only this file and `fleet/state/s325/sweep0600/`, no `cd`, nothing deleted, no message to any human, no card-store write. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s325/sweep0600/` (GET-only scripts copied from s321 and read before use; dumps `RD_open.tsv`, `MPSCALC_open.tsv`, `PCOMP_open.tsv`, three `*_done.tsv`, `RD_todo_keys.txt`).

## BLUF

| project | open now (predicate; every page read to the end) | agent-actionable now (predicate below) | lanes |
|---|---|---|---|
| MPS Calculator (MPSCALC) | **166** (`project = MPSCALC AND ( statusCategory != Done )`, 2 pages, rows 166 = unique 166; all Backlog). Unchanged: same key set, 0 status or `updated` changes against the 11-24 dump | **0** | none. MPSCALC-272 is now **HELD by Kam** (card `datasec-mps-mpscalc272-tiles-1124` = a, 2026-11-24 15:24: "Hold until the figures exist"), so it leaves the conditional list; 427 and 431 stay "built, records only" |
| Security Composer (PCOMP) | **75** (`project = PCOMP AND ( statusCategory != Done )`, 1 page, rows 75 = unique 75; all Backlog). Was 76: **PCOMP-130 Done** (PR 133, squash d06508f8, 2026-11-24T00:42Z; ticket comment 2026-11-24T12:32 "Fixed on main") | **0** (was 1) | none. PCOMP-66 stays HELD (pickup line 340), PCOMP-36 stays open |
| NexusAI (RD) | **905** (`project = RD AND ( statusCategory != Done )`, 10 pages, rows 905 = unique 905): To Do 370, Testing 319, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 905) | **78 To Do keys** (76 carried + 3 new RD-1037, RD-1038, RD-1039, minus RD-577, which is already fixed on main, see below) | 7 (NX-S2, NX-W2 new, NX-B, NX-F1, NX-F2, NX-T, NX-X; one NexusAI seat at a time, jest lock) |

**Actionable predicate (unchanged from SWEEP-1110):** the ticket needs no new word from Kam or a client human, no ruling, no production touch, no deploy, no money, no external message; is not already built (comments, merged PR or a read at main); and no HELD or DROPPED line in the pickup names it. Counts of keys, not of seat-hours.

**Census controls (key diff by `comm` and stamp diff by `join`, against the 11-24 dumps in `fleet/state/s321/sweep/`):**
- RD open 901 -> 905: gone 0; new RD-1036, RD-1037, RD-1038, RD-1039 (all To Do, created 2026-11-24). Status moves: **RD-1021, RD-1026, RD-1031, RD-1034 To Do -> Testing** (records passes B2043 and B2055). `updated` only: RD-1022 (To Do, 2026-11-24T15:57, the PR 247 review's evidence comment). To Do 370 - 4 moved + 4 new = 370; Testing 315 + 4 = 319 (sums to 905). RD Done 130 (unchanged; 130 + 905 = 1035 keys, was 1031, +4 new).
- MPSCALC: gone 0, new 0, 0 stamp changes; Done 267 (unchanged); 166 + 267 = 433.
- PCOMP: gone PCOMP-130 (now Done), new 0; Done 54 -> 55; 75 + 55 = 130. No stamp change on any other key.
- Nothing newer than RD-1039: `GET RD-1040` and `RD-1041` return 404. **The new RD security ticket for the plain data-source routes (the "F-Q0" ticket) is NOT on the board yet** (records seat R321, B2073, is in session; not counted as commissioned).

Origin mains at sweep time (`gh api -X GET .../commits/main`; `pulls?state=open` returned **0 open PRs** in all three repos): NexusAI `11149d3f` (merge of #251, RD-1036, 2026-11-24T16:43Z); MPS `56f508a7` (#228, unchanged since 2026-11-22); Composer `d06508f8` (#133). Every file claim below is from origin main.

Standing facts that bind: MPS seats push a branch only, Friday/Tuesday opens the PR (CodeQL rule), nothing deploys without a card; Composer: no deploy of a changed content release (pickup top block), the demo is Kam's; NexusAI: nothing deploys (C-224 demo hold), `npm run verify`, one jest lock holder at a time; model rule 2026-11-21: Opus default, Fable only when flagged. HPSM hold to 2026-12-10 respected.

## RANKED LANES (value and size)

| rank | lane | keys | size | why this rank | gate |
|---|---|---|---|---|---|
| 1 | **NX-S2** (server bundle), re-checked first | RD-1017, RD-893 (remainder), RD-974, RD-975, RD-896 (measure only, builds nothing) | S each; about 3 h for the four builds, one file `backend/server.js` (plus one test file each) | The pickup's named next lane ("NX-S2 ... after RD-1036 lands"); RD-1036 landed (PR 251 touched only `static/js/admin.js`, one new test, `scripts/verify-expected-counts.json`, so `server.js` is free). **Re-verified at main `11149d3f`:** RD-1017 real: `AUDIT_ACTIONS.SETTINGS_CHANGE` is read at `backend/server.js` lines 17366 and 17616 and the object `AUDIT_ACTIONS` (lines 432 to 459) has no such key (read of the whole object). RD-974 real: `new Date(job.Job_Start_Time \|\| Date.now())` at 20292 and 20397 (the ticket's 20089 and 19984 have drifted). RD-975 real: `dateFields` at 13411 lists `created_at` first. RD-893 partly landed (PR 131: `RISK_CONDITION_PUT_FIELDS` at 21357 and lower-casing of `risk_level` at 21665), but the type checks on `condition_text`, `is_active`, `email_recipients` in the PUT at 21647 to 21681 are still absent (the ticket's own comment says so: "Open on this ticket: measurement (1) and the type checks"). RD-896 says "Measure first and build nothing": a read-only count over a data copy, not a build. | G2 |
| 2 | **NX-W2** (new: hardening residue of RD-1026) | RD-1039 | S to M, about 1.5 to 2 h | Filed 2026-11-24 after PR 248; Low (the ticket proves none of it is reachable by an AI endpoint or a viewer today), but fully specified with acceptance: write the other status rows through `escapeHtml` or as text (`static/js/index.js` 3466, 3470, 3474, 3478, 3569; `static/js/first-run-setup.js` 1486, 4127, 4240, plus 1468 and 1471), and make the tool lookup at `backend/llm/azureOpenAIAdapter.js` line 307 refuse names such as `constructor` (`Object.hasOwn`). No word, no ruling. Overlap to sequence: RD-1014 (NX-X) lists first-run lines and says whichever lands second drops the rows the first fixed; NX-F1 edits `first-run-setup.js` too, so NX-W2 runs before NX-F1 and NX-X, never alongside | G2 (G1 if the builder widens past the listed rows) |
| 3 | **NX-T** adds **RD-1037** (new) | RD-1037 (joins the 34 NX-T keys) | S, about 1 h | Test tooling only: the harnesses boot the server on a data folder with no persistence sentinel, so the real volume-wiped alarm fires in tests (127 lines in one generator log; a first-boot banner adds 18 lines to the contrast suite). Files: `scripts/qa-surface-up.sh` (names the sentinel 0 times per the ticket) and the test boot helpers. Acceptance proposed in the ticket: a harness boot raises no sentinel line, the real alarm still fires on a wiped volume (one cell). The alarm text's product code was not read by the ticket's author; the builder reads it first | G2 |
| 4 | NX-B, NX-F1, NX-F2 (now with **RD-1038**), NX-T (rest), NX-X | the carried keys (SWEEP-1110 tables) | per the 11-22 sizes | Not re-sized. **RD-1038 (new, joins NX-F2):** the dashboard anomalies tab's High Risk label colour reads 3.96 and 4.46 to 1 in dark and 3.82 in light, below the 4.5 the contrast suite asks; the ticket says the file and line of the label colour are UNMEASURED, so the builder first finds the source; coupling to know: the light baseline is bound to the 982-row reference dataset (decide dataset and label together; PR 246 re-measured the baselines); NX-F2 caution carried (PR 244 and 246 files re-read at `11149d3f`). RD-1026 leaves NX-F2 (landed) | per lane |

Disjointness by directory: NX-S2 owns `backend/server.js` (the five handler regions named) plus one new test file per key and `scripts/verify-expected-counts.json` (regenerated by Tuesday at each landing); NX-W2 owns `static/js/index.js`, `static/js/first-run-setup.js`, `backend/llm/azureOpenAIAdapter.js` (and `backend/llm/tools.js` read) plus one new test; NX-T/RD-1037 owns `scripts/qa-surface-up.sh` and test harness helpers. NX-S2 and NX-W2 share no source path (only `scripts/verify-expected-counts.json`, which Tuesday regenerates), but it is one NexusAI repo, one jest lock: sequence NX-S2, NX-W2, NX-T. Composer and MPS have no build lane, so the two other repos are idle.

## What changed since SWEEP-1110 (one line per lane)

- **NX-S1 (RD-1021, RD-1034): DONE** (PR 247, merge 04a6b89d); both Testing with landing comments. The PO answered the open question: follow-up RD-1036.
- **NX-W (RD-1026): DONE** (PR 248, merge dd0698a6; 20 cells, 11 red at base); Testing. Its residue is the new **RD-1039** (lane NX-W2).
- **RD-1036 (viewer-safe Data Sources list): LANDED** (PR 251, merge 11149d3f; files `static/js/admin.js` +27, `__tests__/rd1036-viewer-data-sources-list.test.js` +322, `scripts/verify-expected-counts.json`). Board still **To Do**: its records pass (comment + move to Testing, B2073/R321) is in session. Not counted as work. The plain route `GET /api/data-sources` still returns every non-secret field to any `config.read` caller (the pickup's "Q-0"); that is the F-Q0 ticket R321 is to file (not on the board yet).
- **NX-S2:** shrinks from six keys to five. **RD-577 drops out: already fixed on main.** The only read the ticket's correction says is status reporting (`keyVaultStatus`, line 18585) now reads `encryptionKeyVaultState()`, which reads `KEYVAULT_NAME` and `KEYVAULT_KEY_NAME` (`backend/encryptionService.js` lines 98, 176, 315); the comment at 18580 names RD-577 + RD-518. The two `KEY_VAULT_NAME` reads left (lines 767 and 795) are the behavioural and inert ones the correction comment says this ticket must NOT touch (RD-578). So RD-577 is "built, records only" (a comment and a move; Tuesday's reading, not a build). RD-1021 left NX-S2. The other keys' line numbers drifted by +10 to +13 since 11-24; the substance is unchanged.
- **NX-B, NX-F1, NX-T, NX-X:** unchanged (`updated` stamps of every carried key unchanged, 0 status changes). NX-T gains RD-1037. NX-F2 loses RD-1026, gains RD-1038 (net 15).
- **C-T2 (PCOMP-130): DONE** (PR 133). Composer has no actionable build left.
- **M-R (MPSCALC-272): now HELD** by Kam's 2026-11-24 15:24 ruling; no longer "conditional". No MPS lane.
- **RD-1035:** DROPPED by Kam's ruling (card c "Leave it", 2026-11-24 11:28); stays out of every lane.

## 1. MPS Commercial Calculator (MPSCALC)

Open 166, all Backlog; Done 267 (unchanged); no PR merged since #228; 0 open PRs; no ticket created after MPSCALC-433; no `updated` stamp changed (stamp comparison of all 166 keys against the 11-24 dump). **0 agent-actionable builds.**

- **Built, records only:** MPSCALC-427 (#228) and MPSCALC-431 (#226).
- **HELD (Kam, 2026-11-24 15:24):** MPSCALC-272. When MPSCALC-315 lands, Tuesday brings one word pack. Owed to the next MPS records pass: a C-entry of the ruling and a comment on MPSCALC-272 (pickup).
- **Excluded (carried unchanged, stamps unchanged):** 195, 316 remainder, 360, 419, 421, 424, 425, 395 and 372, 278, 283, 274; seed epics, question-for-Kam tasks 69 to 85, `needs-ruling` tickets and the roughly 48 built-and-open tickets. Not re-read for text today.

## 2. Security Composer (PCOMP)

Open 75 (all Backlog); Done 55. Main `d06508f8`; 0 open PRs. PCOMP-130 Done (see above). PCOMP-66 (engine edit, G1) stays HELD; PCOMP-36 stays open; every other key unchanged by stamp. **Binding top block still stands:** main carries a NEW content release; no Composer deploy ships it. **0 agent-actionable builds.** (Held and excluded groups carried from SWEEP-1110 section 2: PCOMP-44, the reviewer-round hold, the Guided hold, the owner's seven calls, words, deploy and ops, epics.)

## 3. NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

Open 905: To Do 370, Testing 319, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2. Main `11149d3f`. Merged since SWEEP-1110 (main d96a83d3): #247 (RD-1021 + RD-1034), #248 (RD-1026), #249 and #250 (records history), #251 (RD-1036). No PR open.

### New keys since SWEEP-1110

| key | verdict | note |
|---|---|---|
| RD-1036 | landed (#251), records owed | board To Do; R321 comments and moves it |
| RD-1037 | **ACTIONABLE (NX-T)** | harness persistence sentinel; Low; read whole today (description and recommendation) |
| RD-1038 | **ACTIONABLE (NX-F2)** | High Risk label contrast; Low; source file UNMEASURED by the ticket; dataset coupling |
| RD-1039 | **ACTIONABLE (NX-W2)** | hardening residue of RD-1026; Low; read whole today |

Pickup check (whole-file counts via python; positive control RD-1011 = 17 hits): RD-1036 5, RD-1037 2, RD-1038 2, RD-1039 2, RD-1022 1, RD-1035 3; every hit is a records or owed line; **no HELD or DROPPED line names RD-1037, RD-1038, RD-1039 or any NX-S2 key** (RD-1017, 577, 896, 974, 975: 0 hits; RD-893: 1, the older sweep line). The only holds on NexusAI are the C-224 demo hold (no deploy), one lane at a time, and RD-1035 dropped.

### Re-screen of the carried keys

All 76 other carried To Do keys: board stamp and status unchanged since the 11-24 dump (stamp diff; only RD-1021, 1022, 1026, 1031, 1034 changed). NX-S2 keys re-read at main as above (RD-1017, 974, 975, 893 real; RD-577 stale; RD-896 measurement-only). RD-1021 and RD-1026 moved to Testing.

### Actionable keys by lane (78)

| lane | count | keys |
|---|---|---|
| NX-S2 | 5 | RD-974, RD-975, RD-893, RD-896, RD-1017 |
| NX-W2 | 1 | RD-1039 |
| NX-B | 9 | RD-455, 744, 745, 750, 824, 728, 759, 578, 1023 |
| NX-F1 | 11 | RD-117, 188, 176, 416, 151, 371, 373, 540, 687, 396, 1016 |
| NX-F2 | 15 | RD-144, 351, 164, 222, 220, 259, 261, 483, 613, 832, 512, 513, 515, 145, **1038** |
| NX-T | 35 | the 34 carried keys of SWEEP-1110 plus **RD-1037** |
| NX-X | 2 | RD-1014, RD-1015 |
| total | **78** | 5 + 1 + 9 + 11 + 15 + 35 + 2 = 78 (the 11-24 count of 79 minus RD-1021, 1026, 1034 moved to Testing and RD-577 stale, plus RD-1037, 1038, 1039) |

Cross-lane exceptions carried: RD-396 also edits `backend/services/riskAlertScheduler.js`; RD-515 edits F1's `first-run-setup.html` from F2's banner-guard tests (after F1); RD-1016 before RD-1014 (`settings.js`); RD-145, 745, 397, 918 need the Dockerfile (NX-T); NX-X (RD-1014, 1015) runs alone and last, and after NX-W2 (shared first-run rows).

### NexusAI: conditional (not counted)

RD-1019, RD-1022 (its stamp changed: the PR 247 review added evidence that `GET /api/log-analytics/status` returns the primary workspace's ids and a key-held flag to a viewer; the ticket stays a question), RD-1020, RD-1029, RD-763, RD-764, RD-1006, 1009, 1010. The coming F-Q0 ticket (plain data-source routes returning every non-secret field) waits on the product owner's open card or its default.

### NexusAI: excluded (with the reason)

- **Landed on main, records only:** RD-538, 563, 969, 729, 826, 970, 731 (partly), 972, 929, 977, 978; RD-1036 (PR 251); **RD-577 (fixed on main by the RD-518 work; new this sweep)**.
- **Held or needs a ruling or Kam:** RD-805, 768, 1025, 1028, 433, 610, 612, 622, 644, 522, 884, 546, 193, 583, 584, 305, 313.
- **Product owner, dropped or a customer-facing word:** RD-1035 (DROPPED by Kam), RD-702, 636, 1029, and the roles-UI chain RD-937 to 957.
- **Not agent work:** epics RD-6, 7, 8; business and compliance RD-13, 20, 21, 22, 28, 29, 30, 31, 34; Azure and secrets RD-50, 54, 55, 83; Jira and session tooling RD-233, 287, 449; marketplace items; feature requests RD-146, 400, 401, 842; RD-1004 (dated 2026-12-18); RD-1001 (launcher-side).
- **In Progress (8), Put on Hold (7), Declined (2):** counts only. **Testing 319 and Release Ready 199:** not work.
- **Other To Do keys (about 280, the `operations` residue and QA-gate findings):** not re-read; UNMEASURED beyond titles and stamps.

## 4. Questions for Tuesday (each with a default)

1. **RD-577:** already fixed on main by the RD-518 work (read above). Default: treat as records only (a comment citing `encryptionService.js` lines 98, 176 and `server.js` 18585, then Testing), drop it from NX-S2; do not build.
2. **RD-896** is a measurement ("build nothing") and needs a data copy or data the PO supplies. Default: leave it out of the first NX-S2 seat; keep it a read-only line for later.
3. **RD-1038:** the ticket leaves the label's source unread and ties the fix to a dataset choice. Default: builder reads source first and fixes the colour at its source under NX-F2; if the dataset must change, stop and report.
4. **Sequence:** NX-S2, then NX-W2, then NX-T/RD-1037 (one seat at a time). Default: launch NX-S2 next now that RD-1036 has landed.
5. **Records owed that this sweep saw but did not touch:** RD-1036 comment and move (R321, in session); the F-Q0 ticket (R321); RD-577 comment; MPSCALC-272 hold C-entry and comment.

## 5. How measured, and NOT tested

- Instruments: GET-only paginated Jira `search/jql` (page size 100, `jqdump.py` to the last page; rows = unique for all six dumps), `jdesc.py` and `lastc.py` for ticket text and last comments, `gh api -X GET` for mains, open and closed PR lists and PR file lists, file reads at main through `rg.sh`; `comm`, `join` over the dumps. Positive controls: RD-1011 in the pickup (17 hits), the two `SETTINGS_CHANGE` reads at 17366 and 17616 (and the whole `AUDIT_ACTIONS` object read lines 432 to 459, so the absence of `SETTINGS_CHANGE` is a read, not a grep miss), `Job_Start_Time || Date.now()` at 20292 and 20397.
- **Not tested:** (a) the 166 MPS, 74 other Composer and about 280 NexusAI To Do tickets were not re-read for text, only for key list and `updated` stamps; (b) of the 78 RD actionable keys only RD-1037, 1038, 1039 (whole), and RD-1017, 893, 896, 974, 975, 577 (description head and last comment plus the source lines) were read today; the rest rely on the 11-11 deep read, the 11-22 screen and unchanged stamps; (c) no test was run, no CI or CodeQL state was read for #247 to #251 (the pickup records them); (d) RD-577's fix was read from source (`keyVaultStatus` and `encryptionKeyVaultState`), not exercised; (e) sizes are estimates for the kit drafter to confirm; (f) the label source for RD-1038 and the harness helpers for RD-1037 were not located; (g) the pickup was searched by a python whole-file regex for the keys named, not read line by line (about 1,559 lines).
- Disclosures: no write outside this file and the scratch folder; no Jira or GitHub write; no token printed; no deletion; HPSM-POC not read.

READ-WHOLE-BY-TUESDAY: ____
