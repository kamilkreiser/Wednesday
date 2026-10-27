BLUF: 0 BUILD lanes can START NOW (HPSM-POC 0, MPS 0, Composer 0, NexusAI 0): all 8 lanes of the 02:10 sweep are either landed (6) or in a live gate (2), and the Jira board has no new row and no update since 00:02 (`created >= "2026-10-28 02:00"` 0 on all four boards; `updated >= "2026-10-28 00:00"` 3 rows, all NexusAI: RD-892, -897, -898). What CAN start: 5 records lanes that are OWED (not build lanes): HPSM-POC (#236, #237, #238), Composer (#100), NexusAI (#134 now; #135 and #136 after they land), MPS (#132, which MERGED at 06:01:11 AEDT, see section 0). The 1 research step (NexusAI RD-897 step 1, "confirm dead") was never commissioned; I ran its search read-only in this sweep and the result is in section 3: `executeAnomalyFilter` has NO caller in 784 text blobs on main `3a1ac7f2`, so RD-897 step 2 (a guard) is NOT a lane and CC5 (retire or leave) is now a live card question, the product owner's per the ticket. Still held: PCOMP-106 and PCOMP-107 on the Kam card `composer-106-107-routeb-residue-round-1028` (default a at 09:00 today). Program: lane x open PR 0 hits across 12 pairs, lane x lane 1 hit across 2 pairs (PCOMP-106 x PCOMP-107, same file, on purpose), 7 planted controls behave. Kam's rulings today: 0 (`kam_rulings_today.sh`, 06:04:39, newest live row 21:59 yesterday). Two corrections to the relay: MPS #132 is MERGED, not open; the pane list shows only G192 (#135) and G193 (#136) under gate.

# Datasec: completable tickets, 06:00 sweep (read-only research, 2026-10-28)

Researcher: read-only sub-agent (claude-sonnet-5-5) for Tuesday. Clock from `date`: Wed 28 Oct 2026 06:00:38 AEDT at start, last read 06:04:51 AEDT. Method and shape: [[2026-10-28_datasec-completable-tickets-0210]] (read whole). Every figure below was re-measured now unless it says "carried". Fences kept: Jira GET only through a scratchpad reader (`sweep0600/jr.py`) that loads each project's OWN `.env` in-process (no token printed), every JQL `project = <KEY> AND ( ... )`, paged to isLast (page counts in section 2); `gh api -X GET` only, each under its own project's `GH_CONFIG_DIR`; no git verb touched any project repo; no HTTP to any hosted host; no az, ssh, docker; no `decision_queue.sh`; no mail, chat, Artifact or Docs tool. Rulings read through `kam_rulings_today.sh`. Only file written: this one (plus scratchpad scripts and a read-only copy of 784 NexusAI blobs under `scratchpad/sweep0600/nx/f/`). Times: GitHub gives UTC; AEDT is UTC+11.

## 0. What happened to each previous lane (each re-read at source)

| 02:10 lane | Now | Evidence (instrument) |
|---|---|---|
| H1 H-RULE (HPSMPOC-358) | LANDED, not deployed | HPSM-POC #237, squash `7c261879`, merged 2026-10-27T17:51:14Z (04:51 AEDT), 1 path `infra/tests/test_security_baseline.py` (`pulls/237/files`). `ci` and `Push on main dynamic` push success on `7c261879` (`actions/runs?branch=main`). Ticket HPSMPOC-358 still Backlog, no comment (the Jira `updated` stamp is 19:08 yesterday) |
| H2 H-WORDS (HPSMPOC-359, -360) | LANDED, not deployed | #236, squash `c00e2828`, merged 2026-10-27T18:17:08Z (05:17 AEDT), 4 paths: `UatOpenAuthentication.cs`, `infra/README.md`, `infra/env/uat.bicepparam`, `web/src/server/auth/config.ts` (the four H2 named; no test file). `ci` push success on `c00e2828`. Both tickets still Backlog, no comment |
| H3 H-LOGO (HPSMPOC-361) | LANDED, not deployed | #238, squash `5147ec5e`, merged 2026-10-27T18:16:17Z (05:16 AEDT), 3 paths: `HpLogo.test.tsx`, NEW `web/e2e/logon-chooser-corners.spec.ts`, `web/playwright.config.ts` (H3's proposal and its contingent file, as forecast). `ci` push success on `5147ec5e`. HPSM-POC main is now `c00e2828` (the relay's sha, confirmed). Ticket still Backlog |
| M1 M-DEPS (MPSCALC-347) | LANDED during this sweep (relay said open under gate G189) | MPS #132, squash `1a2a0294`, `merged_at` 2026-10-27T19:01:11Z = **06:01:11 AEDT**, 1 path `tests/MpsCalc.Api.Tests/PublishOutputTests.cs` (+66 -11). The merge came about 30 seconds after my first `date` read. Main CI on `1a2a0294`: `ci` and `Push on main` `in_progress` at 06:01 and again at 06:04:51 (NOT yet green; I did not wait). Ticket MPSCALC-347 still Backlog, no comment. No G189 pane in `tmux list-panes` |
| C1 C-DATE2 (PCOMP-105) | LANDED, not deployed | Composer #100, squash `bdcfde7b`, merged 2026-10-27T18:30:57Z (05:30 AEDT), 1 path `apps/api/test/b626-date-rule-rows.db.test.ts` (+20 -0, the file C1 named). Composer main is `bdcfde7b`; `Push on main dynamic` success on it. PCOMP-105 still Backlog, no comment |
| N1 N-PROBE (RD-894) | LANDED, not deployed | NexusAI #134, merge commit `3a1ac7f2`, merged 2026-10-27T18:11:20Z (05:11 AEDT), 2 paths `__tests__/rd891-probe-name-race.test.js` (+182) and `scripts/verify-expected-counts.json` (+2 -2). Counts file on main now reads `tests` 5223, `suites` 310 (`_updated` 2026-10-27T16:10:11Z; 5220 at 02:10, so +3 tests, +0 suites as forecast). CI on `3a1ac7f2`: `Build`, `npm-audit`, `Gitleaks Scan`, `Push on main dynamic` push success; `Deploy demo` skipped. RD-894 still To Do |
| N2 N-TAMPER (RD-895) | OPEN PR under live gate | NexusAI #136 (`b862/nexusai-895-tamper-control-cell`), 1 path `__tests__/rd407-concurrent-settings-writers.test.js` (+17 -5), head `fbd51a15`, mergeable_state `unstable` (checks still running). Check-runs on head: CodeQL, `scan`, 3 `Analyze` and `audit-production-deps` completed/success, `build` in_progress. Pane `%117 Datasec/NexusAI-G193`. NOT a lane |
| N3 N-LOOSE (RD-898) | OPEN PR under live gate | NexusAI #135 (`b856/nexusai-898-testing-label-exact-pins`), 1 path `__tests__/rd892-testing-dropdown-null-level.test.js` (+46 -13), head `4d466a9a`, mergeable_state `clean`. Pane `%116 Datasec/NexusAI-G192`. NOT a lane |
| N4a N-READER step 1 (RD-897) | NEVER COMMISSIONED; done as a read in this sweep | Result in section 3 (no caller). RD-897 has no Jira comment (`updated` 00:02): the record is not yet written there |
| N4b N-READER step 2 | MOOT on the measurement | Only "if step 1 finds a caller". It found none. Becomes CC5 (section 6) |
| held C-ROUTEB (PCOMP-106, -107) | STILL HELD | Both created 22:30, Backlog, no comment since. Card `composer-106-107-routeb-residue-round-1028` is the relay's: not read by me (fence: no `decision_queue.sh list`); default a at 09:00 |

## 1. State of the four repos and the live work (what no lane may use)

| Repo | Main now | CI at the tip (`actions/runs?branch=main&per_page=6`) | Open PRs (`pulls?state=open&per_page=100`; 4 or fewer rows, no second page) | Live or owed seats |
|---|---|---|---|---|
| HPSM-POC `datasecau/HPSM-POC` | `c00e2828` (#236) | `ci` push + `Push on main dynamic` success on `c00e2828`, `5147ec5e`, `7c261879` | 0 | none live. OWED: a records seat for #236 to #238 |
| MPS `datasecau/MPS-Commercial-Calculator` | `1a2a0294` (#132) | `ci` and `Push on main` `in_progress` on `1a2a0294`; success on `080f1608` | #121, #120 (dependabot, each `web/package-lock.json`) | none live. OWED: records for #132 (after main CI goes green is the safe moment) |
| Composer `datasecau/Datasec-Security-Composer` | `bdcfde7b` (#100) | `Push on main dynamic` success on `bdcfde7b` | #95 (2 files), #91, #86 (dependabot, 2 files each), #85 (draft HOLD K6, 57 files; `changed_files` 57) | none live. OWED: records for #100 |
| NexusAI `datasecau/Reporting_Dashboard_Au` | `3a1ac7f2` (#134) | 4 workflows success, `Deploy demo` skipped, on `3a1ac7f2` | #136, #135 (1 file each) | `%116` G192 (#135), `%117` G193 (#136). OWED: records for #134 now, #135 and #136 after they land |

Panes: `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` at 06:04 printed `%0 tuesday`, `%117 Datasec/NexusAI-G193`, `%116 Datasec/NexusAI-G192`, `%1 fleet-monitor`. Load averages 3.27 3.74 4.79 (`uptime`, 06:04). Listening TCP ports seen by `lsof -nP -iTCP -sTCP:LISTEN`: 5000, 7000, 49152, 49181, 49183, 49185, 59869. Carried from 02:10: MPS kits name `<MPS root>/.tools/dotnet/dotnet` (10.0.401).

## 2. How I measured (every count names its instrument, frame and a control that can fail)

| Count | Instrument and frame | Result | Control that could have failed |
|---|---|---|---|
| Open tickets per board | `project = <K> AND ( statusCategory != Done )`, paged to isLast at ~06:01; pages 2, 4, 2, 8 | HPSMPOC 123, MPSCALC 342, PCOMP 101, RD 776 (02:10: 123, 342, 101, 776: all 0 change) | negative `summary ~ "zzqxnonexistentphrase"` 0, 0, 0, 0; totals `issuekey is not EMPTY` 362, 356, 107, 894 (equal to 02:10) |
| Created since 02:00 | `created >= "2026-10-28 02:00"` | 0, 0, 0, 0 | the same filter lists `RD-897`, `RD-898` when set to `updated >= "2026-10-28 00:00"` (the wider `updated` filter returns 0, 0, 0, 3), so the filters can return rows |
| Updated since 18:30 yesterday | `updated >= "2026-10-27 18:30"` | HPSMPOC 8, MPSCALC 4, PCOMP 5, RD 12 (exactly the 02:10 numbers) | none of the 0-update boards changed: no Jira comment was written about #134, #236 to #238, #100 or #132 (Jira has not heard of any landing since 00:02) |
| Open PRs per repo | `pulls?state=open&per_page=100` | HPSM-POC 0, MPS 2, Composer 4, NexusAI 2 | `pulls?state=closed&sort=updated&direction=desc&per_page=8`: `merged_at` set on 8 of 8 rows for each repo (all merge shas in section 0 come from it) |
| Open-PR file lists | `pulls/<n>/files?per_page=100 --paginate` | NexusAI #135 1, #136 1; MPS #120 1, #121 1; Composer #95 2, #91 2, #86 2, #85 57 | Composer `pulls/85` `.changed_files` = 57 = rows listed; each landed PR's file count equals its stated `changed_files` (MPS #132 1) |
| NexusAI static census for RD-897 | `git/trees/main?recursive=1` (1021 entries, `truncated` false) then raw `contents/<path>?ref=main` of every text blob except `package-lock.json` | 960 text-extension blobs listed minus `package-lock.json` = 785 requested, 784 files fetched, 0 empty, 0 FAIL. Frame by folder: static 42, backend 96, `__tests__` 369, scripts 74, docs 93, tests 43 (the 785 vs 784 is one path the tree lists that did not save as a file; not identified) | positive control: `displayFilteredAnomalies` 3 hits (HISTORY.md 1, `static/js/index.js` 2: line 9257 the call, 9421 the definition) with the same `-i` grep; `zzqxnone` 0 files |
| Model rows | `/usr/bin/grep -n '^| <id> '` on `fleet/specs/model-routing.md`: L6 line 85, C2 line 92, C8 line 98, G1 line 108, G2 line 109, G-cap line 111 | found at those lines (same as 02:10) | `^| ZZ9 ` 0. `models_latest.json` `checked_at_local` 2026-10-28 03:55:59 +1100, `warnings` [] (about 2 h old) |
| Clock | `date` | 06:00:38 at start, 06:04:51 last read | |

## 3. The lanes: detail

One seat, one worktree, one branch per lane. Standing lines carried: PRIOR-WORK CHECK; no message to any human; Jira writes only where the kit's scope says; never delete (quarantine); the seat pushes its OWN branch only and Tuesday opens and lands the PR through CodeQL. Landing: MPS and Composer squash; NexusAI merge commit; HPSM-POC squash (carried). **None of these deploys anything.** HPSM-POC kits carry "This phase builds no integration with HP tools".

### Build lanes startable now: NONE

I looked for a startable ticket outside the 02:10 list and found none:
- Created or updated since 00:00 today: only RD-892, RD-897, RD-898 (all NexusAI, all spoken for below).
- HPSM-POC: HPSMPOC-362 (az what-if input list, "not scheduled"), HPSMPOC-357 and the HP-gated set, HPSMPOC-356 B734-9/-6 (rulings owed), all carried; HPSMPOC-311 (the revocations flake) already had a fix in #198 and its remaining clause (1000 consecutive green runs) is a measurement, not a lane. Carried, not re-read: HPSMPOC-349/-324/-343/-246.
- MPS: I re-read the last comment of MPSCALC-321 to -339 (19 tickets created 10-24 to 10-25): every one says its acceptance is MET or "in main", "the ticket stays Backlog" (records matter, no lane). MPSCALC-334 part B: "cannot be proven yet", the Playwright spec "does not load" (needs a seat on that and a ruling-free reason; not a lane). MPSCALC-342 and -345 `needs-ruling`; -343, -344 CC2; -349 SDK tie. Carried from 02:10 for the rest (-340, -341, -346, -348, -350 to -356).
- Composer: PCOMP-66, PCOMP-67 are Minor test-only rows ("RULED BY THE COORDINATOR") but their file `packages/content/test/b330-sm316-qgate.test.ts` is ABSENT on main (`contents?ref=main` 404; present on branch `b330/sm316-content-catalogue`, i.e. draft #85, HOLD K6), so they cannot start. PCOMP-95 and PCOMP-97 are landed (#92, #94 per their comments). PCOMP-98 held (round count), PCOMP-102 (a fix-shape question), PCOMP-24 (#95), PCOMP-23/-29 to -61 (draft #85).
- NexusAI: RD-885, RD-887 are in Testing with landing comments (records matter). RD-892 part (b), RD-893 remainder, RD-896 are the product owner's or need data; RD-884 step 2 and RD-886 B706-2 are CC3 and CC4. RD-897: below.

### Held

| Item | Why | What unblocks it |
|---|---|---|
| **PCOMP-106, then PCOMP-107** (C-ROUTEB; same file `packages/db/test/b778-route-b-script-complete.db.test.ts`) | G-cap (`model-routing.md` line 111) and C-107: a later PR's gate may be a forbidden "round 3" on the Route B class; 106 is the class itself. Unchanged since 02:10 | The Kam card `composer-106-107-routeb-residue-round-1028` (default a at 09:00 today). If a: 106 gets one more gated PR (round 3 of 3, last, tier 1 by G1 line 108); 107 (tier 2, G2 line 109) and the already-landed 105 fresh. They cannot run beside each other (one file) |

### Research step (a read, no gate, no path)

**N4a RD-897 step 1, "confirm dead" (never commissioned; done read-only here).** Ticket scope quoted: "Search the whole repository for executeAnomalyFilter, including any page that builds a call from a string, and record the result here"; "Filing this ticket builds nothing." Result at main `3a1ac7f2`, frame 784 text blobs (section 2):
- `executeAnomalyFilter` (case-insensitive) appears in exactly 3 lines: `static/js/index.js:9224` (the definition), `static/js/index.js:9261` (an error string "Failed to execute anomaly filter", not a call) and `HISTORY.md:8759` (the records seat's prose). In 41 other static files, in all of `backend/` (96 files, including `server.js`), `__tests__/` (369), `tests/` (43), `scripts/` (74), `docs/` (93): 0. `displayFilteredAnomalies` is called once, at 9257, inside `executeAnomalyFilter` itself, so it is reachable only through that function.
- String-built calls: csp-helpers (`static/js/csp-helpers.js` lines 85-97) dispatches a `data-csp-fn` name through `_registry[name]` or `window[name]`. 322 literal `data-csp-fn=` attributes in static (control: the same pattern counts them); none names `executeAnomalyFilter`; the only two dynamic `setAttribute('data-csp-fn', ...)` calls (index.js 2753, 8679) use the fixed names `reuseUserQuestion` and `toggleRedFlagAlertResults`. No `window.executeAnomalyFilter =` and no register call for it.
- Not measured: a call from a runtime-fetched string (data from the API), `.github/**` and other non-text-extension files (the tree has 1021 blobs, I fetched the 785 text-extension ones), GitHub code search (not used; it lags).
- Reading: nothing can call it; the function is dead, as the ticket suspected. Tuesday or the records seat writes that on RD-897 (I did not: Jira read only). This turns the ticket's step 3 into **CC5** (retire the dead function or leave it): the product owner's per the ticket, no build.

### Owed records lanes (records branches, not build lanes; each seat lands its own records branch)

Per DRAFTER_RULES, records seats are not Tuesday's to commission as a ref write; listed so none is forgotten. Each should read the Jira ticket and the landed PR, comment (Jira write only where its kit says), and add the project's own records entry.

| # | Project | What landed and is unrecorded | Paths it would touch (by the earlier records pattern, not re-read) | Note |
|---|---|---|---|---|
| R-H | HPSM-POC | #237 (HPSMPOC-358), #238 (HPSMPOC-361), #236 (HPSMPOC-359 + -360); main `c00e2828`; five tickets still Backlog with no landing comment | the project's records file and Jira comments | No deploy in this lane. The demo deploy state (HPSMPOC-268, comment 19:09 yesterday) is carried, no host probed |
| R-C | Composer | #100 (PCOMP-105), main `bdcfde7b`; ticket Backlog | `CLARIFICATIONS.md` and the ticket | PCOMP-105's CC1 half was "fresh round" by precedent; #100 landed, so the entry must say which gate round it had (read from its gate verdict, not mine) |
| R-N | NexusAI | #134 (RD-894) now; #135 (RD-898) and #136 (RD-895) after they land | `HISTORY.md` (the earlier records records, #128 and #133, touched it) | Wait for #135 and #136 if one records branch is wanted; one pass avoids two HISTORY.md conflicts. RD-897 step 1 result goes in the same entry |
| R-M | MPS | #132 (MPSCALC-347); main CI on `1a2a0294` still `in_progress` | the ticket comment | Wait for green on `1a2a0294` first (MPS main was red once, MPSCALC-356) |

Model row for records seats: not re-derived here (the records seats' own rows are in `model-routing.md`; I did not re-read them for this sweep). Port-free note: none of the lanes above opens a port; the research step is a read; the two live NexusAI gates are Tuesday's.

## 4. Not startable, with the reason (one line each)

PCOMP-106, -107 (card, section 3); PCOMP-66, -67 (file not on main, draft #85); MPSCALC-342, -345 (`needs-ruling`); MPSCALC-343, -344 (CC2); MPSCALC-349 (SDK tie), -334 part B (spec does not load); RD-892 part (b), RD-893 remainder, RD-896 (product owner / data); RD-897 (dead on the measurement: CC5); HPSMPOC-362, -357, -356 B734-9/-6 and the HP-gated set (carried). Records matters, not lanes: the 19 MPSCALC tickets and 02:10's list (each reads met with the ticket still open), PCOMP-95, -97, -103, -104, -105 (landed), HPSMPOC-354, -268, -358 to -361 (landed), RD-885, -887, -891 (Testing). The ~340 MPSCALC, ~770 RD To Do and PCOMP-29..-61 rows were not re-triaged (UNMEASURED); an overlooked startable ticket may exist.

## 5. PARTITION (program output, both directions)

Script `sweep0600/inter.py`: exact path or `dir/**` prefix match, both directions, same repo only. Lanes entered: N-READER step 2 (conditional, kept as the worst case: `static/js/index.js`, the NEW `__tests__/rd897-displayfilteredanomalies-null-level.test.js`, the counts file), C-ROUTEB PCOMP-106 and -107 (held; the Route B test file), N-READER step 1 (no path). Open-PR lists read from GitHub: NexusAI #135, #136; MPS #120, #121; Composer #95, #91, #86, #85; HPSM-POC 0.

| Check | Pairs | Hits | Which |
|---|---|---|---|
| lane x open PR, same repo | 12 (NexusAI 2 lanes x 2 PRs = 4; Composer 2 lanes x 4 PRs = 8) | 0 | none. The conditional N-READER step 2 is clear of #135 (`rd892-...test.js`) and #136 (`rd407-...test.js`); the counts file is in neither PR's list (so a regenerated counts file does not collide) |
| lane x lane, same repo | 2 (Composer 1: PCOMP-106 x -107; NexusAI 1: step 2 x step 1) | 1 | **PCOMP-106 x PCOMP-107 on `b778-route-b-script-complete.db.test.ts`** (on purpose, why they are sequenced) |
| landed PRs x each other | HPSM-POC #236/#237/#238: paths distinct (4 + 1 + 3 files, no name shared); NexusAI #134 and the live #135/#136: no shared file (`rd891`/counts vs `rd892` vs `rd407`) | 0 | by file name |

Planted controls in the same run (the first six must be non-zero, the made-up path zero): `rd892` test vs #135's own list 1; glob `web/**` vs MPS #120 1; #95's own test file vs #95 1; `package-lock.json` vs Composer #91 1; counts file vs itself (the lane x lane shape) 1; counts file vs a list holding it 1; `zzqx/none.cs` vs every open-PR list 0. All behaved. Limits: comparisons are by file name; #85 (57 files) and the dependabot PRs by name; each lane re-reads the open-PR list at launch; #135 and #136 are still open and could gain a commit.

## 6. Card candidates (the exact question, options, default)

1. **CC1 (carried, in flight): Composer PCOMP-106 and -107, round count on later PRs of the capped Route B class.** The card `composer-106-107-routeb-residue-round-1028` is the relay's (not read by me). Options as at 02:10: (a) 106 gets one more gated PR as round 3 of 3, last; 107 and 105 fresh; (b) 106 and 107 recorded as accepted residue; (c) all fresh. Default a at 09:00. PCOMP-105 already landed (#100) on the fresh-round reading.
2. **CC5 (NEW, firm now): RD-897, retire the dead function or leave it.** Fact: nothing can call `executeAnomalyFilter` (section 3 research step). Options: (a) leave it (dead code needs no guard), close RD-897 as unreachable after RD-892 part (b) is answered; (b) retire it in a gated PR (a product byte: delete `static/js/index.js` lines 9224 to ~9262 and `displayFilteredAnomalies` 9421 on; a gate would also need to pin that no caller exists). Default: (a). The product owner's per the ticket; no build lane starts either way until it is answered.
3. **CC2** (carried): MPSCALC-343/-344, a third extra row past the "cap of 2" (row F13). Default (a) one row, test-only.
4. **CC3** (carried, Azure action): NexusAI RD-884 step 2. Default (b) local vfs only, then ask.
5. **CC4** (carried): NexusAI RD-886 B706-2 (four tools naming the T9 volume). Default: repoint, quarantine nothing.

Dropped since 02:10: none of the lanes needs a card any more except CC1 (held) and CC5 (new). Recommended order if Kam is quiet: the records seats (R-N after #135 and #136 land, R-M after main CI is green, R-H, R-C any time), then post the RD-897 result.

## 7. Feedback check

Not re-measured (the commission asked for completable tickets). `kam_rulings_today.sh`: 0 rows today (freshness: newest live Kam row 486 min ago, 6 live rows fetched, 06:04:39). No new ticket exists to be read for a human message. Mail, the NexusAI app store and every product feedback store: not read (fences).

## UNMEASURED (said plainly)

- Whether MPS main goes green on `1a2a0294` (`in_progress` at 06:04:51). Whether CodeQL and the other checks on NexusAI #136's head finish green (`build` `in_progress`); #135's checks not read.
- The gate verdicts for #132, #134, #236 to #238 and #100 beyond the PRs' `merged_at` and the CI runs (no STATUS file read, no Jira comment exists).
- RD-897: runtime-fetched strings, non-text-extension blobs, one path the tree lists that did not save (785 requested, 784 fetched).
- Whether the Playwright spec added by #238 and the infra tests actually run in HPSM-POC CI beyond `ci` push success (not read at job level).
- The other open tickets (section 4): about 1,240 rows not re-triaged since 02:10 (0 changed on the boards since 00:02, so a new startable ticket would have to be an old one).
- The Kam card text and its status, the demo deploy state, any code-scanning alert total.
- Not touched on purpose: myPKI, CypherKey, Lead_Bot, any hosted or production host, az, ssh, docker, `decision_queue.sh` in any form, `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, any WEDNESDAY or FRIDAY tree, any git verb, any Jira or GitHub write.
- Outside-the-fences disclosure: Jira reader `sweep0600/jr.py` is mine, GET only on `/rest/api/3/search/jql` and `/rest/api/3/issue/<key>`, each project's OWN `.env` (NexusAI's base URL from `JIRA_SITE`); `gh api -X GET` only (pulls, pulls/<n>/files, commits, check-runs, actions/runs, git/trees, contents raw) via `gh.sh`, each under its own project's `GH_CONFIG_DIR`; local read-only commands: `date`, `uptime`, `tmux list-panes`, `lsof -nP -iTCP -sTCP:LISTEN`, `python3 -I`, `/usr/bin/grep`, `kam_rulings_today.sh`. I fetched 784 NexusAI blobs in parallel (10 at a time, 35 s). The case-sensitivity advisory fired on three of my model-row greps (they are exact-token id lookups with a ZZ9 control, and I re-ran the data greps with `-i`).

SWEEP DONE /Volumes/Laptop-DEV/TUESDAY/0_Brain/projects_index/2026-10-28_datasec-completable-tickets-0600.md
