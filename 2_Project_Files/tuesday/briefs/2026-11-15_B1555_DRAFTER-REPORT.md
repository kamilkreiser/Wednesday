STARTABLE: YES (one reading, Q1, needs your eye at the stamp; the kit already holds the default and STOPs on any other)

# B1555 DRAFTER REPORT (SEAT-N127, NexusAI lane S, viewer write-gates set), drafted Sun 15 Nov 2026 05:44 to 05:56 AEDT (`date` at start 05:45:10, last read 05:55:03, last `date` 05:56:28)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1555_SEAT-N127_nexusai-lane-s-viewer-write-gates.md` (169 lines, 5 blank `____` slots, ASCII, no person name, no card id). Sidecar `.md.measured`: `stamp_check.py` prints `132 claims, 132 measured, 0 not measured`, rc 0 (run alone, not through a pipe).

## BLUF
- One kit takes the whole viewer write-gates set (RD-958, 964, 965, 966, 968): 20 routes gated (16 RD-958, 3 RD-964, the managed-identity read), the model-switch fixed password removed, the two router-level gates made letter-case proof, the managed-identity check made to dial only inside Azure, four RD-965 routes and 16 RD-966 rows pinned by cells (no handler change), inventory regenerated, K for the counts (six new suites). Permission core and erasure design are named in the kit as later kits and are not started.
- Level Opus, row **C3** (`model-routing.md:93`), gate **G1** (`:108`), model `claude-opus-5-5` (`models_latest.json:17`, map `:37`); launch line carries `BRIEF_SEAT_LEVEL=opus`. The seat builds on a fresh branch `b1555/nexusai-lane-s-viewer-write-gates` off main `ab5a16e9`, red-first, one jest-lock acquisition, pushes, ends `READY B1555: <sha>`; opens no PR, merges nothing; HOLD 2 and the DEPLOY-DEMO paragraph say a merge to main would start Deploy demo.
- The letter-case bypass of the 2026-11-10 NO GO is an explicit row: cells CASE-1 to CASE-5 (four routed forms per route as a viewer; administrator control on the same forms; unrouted forms 404; raw request lines through `net`; persistence of a viewer's marked write) and plants P2 (drop the `i` flag: CASE-1, 4, 5 must go red, the blocker reproduced) and P3 (the old branch's letter-regex plant). The seat also prints the seeded viewer's stored role string (the compare is exact: `authEnforcement.js:647`).
- Biggest risk found in measuring: the ruling's "no admin routes in open (no sign-in) mode" collides with the written first-run rule. Default kept: the open window is UNCHANGED (Q1).

## Facts re-measured (instrument; control)
1. Main = `ab5a16e92a20ee356604bd52be04c7029961207a`, tree `0eee6919...`, `gh api -X GET .../branches/main` 05:45; `git hash-object` of `backend/server.js` = `73aded3f5bfc` = contents-API blob (control: `capabilities.js` `3a117b7ffd69` and `docs/role-capabilities.json` `75bab6e517dd` equal both ways). Counts file 5612 / 343. Open PRs 0; `heads/b1555*` 0 (control `heads/b1545` 1). Last run set on main: Build success, Deploy demo `completed`/`skipped`, Gitleaks and npm-audit success; `actions/variables` `total_count` 0.
2. All five tickets read whole by my own GET-only reader (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s275/d_nxs/jira_get.py`, a copy of the previous drafter's helper with one comment changed; token read in-process, never printed; single-issue GETs, so the `project = RD AND ( ... )` JQL rule did not arise): each To Do, one comment dated 2026-11-11 14:58 carrying the ruling; texts saved as `rd958.txt` ... `rd968.txt` in the work folder. Ruling quoted in `CLARIFICATIONS.md:2680-2682` (sed on both lines holds the phrase; control line 2681 does not).
3. The route set at main, by `grep -n -F` over the contents-API file: 13 in-handler registrations (lines in the kit), `POST /api/models/switch` `:19121` with `password !== 'access'` at `:19125` (literal count 1 at main), the 3 RD-964 routes `:7787 :16090 :17535`, managed-identity `:14465` with `checkManagedIdentityAvailable` `:539` and the dial `:555`; feedback and sustainability mounts `:21981`, `:22051`; router files `sustainability.js:339`, `feedback.js:337,487`. RD-691 landed: the agent route is gone, so RD-958 is 16 routes, not 17.
4. Per-route statuses by role read by program from the committed inventory JSON (203 rows, `meta.routeRows` 203). **The old branch's test carries stale values** (business-hours 500 there, 400 at main): the kit tells the seat to print its own table from the base inventory (Step 1b) and hard-code from that, never from the old branch.
5. RD-966: 16 rows whose administrator and open answers differ: 14 open 403 (all `/api/admin/*`, control path prefix `/api/zzz/` 0), 2 open 401.
6. **Traps (each read at source):** `scripts/role-capability-inventory.js:635,637` uses `POST /api/settings/costs` as the "must read ungated" scan control and throws if it reads gated (so gating costs breaks `--generate`); `__tests__/rd978-handler-span-scan.test.js:84` pins `[43, 29]` (every in-handler gate moves it); `:68` and `:90` of the same file pin `GET /api/settings/emails` and `POST /api/support/ticket` as ungated (why the kit does not gate them). Express 5 (`package.json:58` `^5.1.0`) routes case-insensitively; the string `case sensitive routing` is 0 in `server.js` (control `app.set(` 1).
7. Prior-work check: `compare main...<ref>` over all 37 `heads/b1*` refs (program `census.py`, output `census.out`, 37 lines): exactly two refs are ahead, `b1480/nexusai-s-viewer-write-gates` (7 ahead, 52 behind) and `b1480/nexusai-s-setup-column-mapping` (12 ahead, 52 behind), both touching ten of the kit's path list; the other 35 ahead 0. Nothing for these five tickets is on main (`git/trees` of main: no rd958, 964, 965, 966, 968 or rd793 test file; the rd436, rd929, rd977, rd978, route-census files exist). The old branch's server patch and four test files were read from the contents API at its head `ef0ff56e` (work folder `old/`). Its last verdict (2026-11-11) GO WITH FINDINGS; the 2026-11-10 verdict NO GO, Blocker F1 (letter case on the sustainability config), closed by `f7639de`.
8. Alerts: 64 open on main, 29 in `backend/server.js` (paged `code-scanning/alerts`, `alerts.tsv`). **I did not match alert lines against the edit windows** (UNMEASURED; the kit makes Step 1a do it).
9. Deploy: `deploy-demo.yml` `on:` printed at `:24-34` (push to main, `paths-ignore` `**.md`, `docs/**`, `tests/**`, `workflow_dispatch`), jobs gated at `:53`, `:91`.
10. Slot and ports: `names.py` (sha256 of realpath, `% 19`, formula from `test-server.js:74,89-93`; control `b1430-nodot/b1` -> 6) over 112 trees: no slot has zero trees; slot 1 has 3 idle trees (`b1483-nodot/v36`, `v37`, `.tools/b1545/clone`) and the band 20640-21279 printed 0 listeners (control machine-wide 14). Names for slot 1 under `b1555-nodot`: `old2 new3 inv14 inv18 mut3 v7 chk16 chk17`. Ports 9770-9779: `lsof` 0 rows; word-boundary scan `-w -E '977[0-9]'` over the 29 non-`.pre` SEAT kits of 11-12 to 11-15: 0 hits (control `997[0-9]` hits the previous NexusAI kit, 2). Live panes at 05:55: `tuesday`, `fleet-monitor`, `Datasec/NexusAI-R229` (a records seat; its kit mentions `backend/server.js` only as a line to read; no code path); a `Datasec/Security-Composer-R228` pane listed at 05:47 had gone by 05:55 (the kit says so).
11. Lock base listing `queue-docker queue-jest released`; load `2.80 2.38 1.89` at 05:47.
12. Model rows: `awk NR==92/93/108/109` of `model-routing.md` print C2, C3, G1, G2 (the C3 row says Sonnet "no", Opus "1st"; the C2 row's text excludes "auth-design").
13. Landing rule: `CLARIFICATIONS.md:2067` "Merge path: open a PR from the gated branch, wait for CodeQL ... land the SAME commit. Never squash, never rebase" (also appears at `:2611`, the kit cites `:2067`).

## D-decisions (mine, each with the alternative)
- D1 Whole set in one kit, not split: the five tickets share one mechanism (`requireAdminFor`), one inventory regeneration and one hard-coded status table; splitting would force two inventory drives and two verifies of about 20 minutes each. If you judge 20 routes and 6 test files too large for one Opus window, split RD-964/968 (the three setup routes and the managed-identity route) into a second kit; the kit carries a context band and handover form for that case.
- D2 Router-level gates stay in `server.js` with `/i`, `routes/*.js` untouched (lane B partition, and the old branch's shape, GO WITH FINDINGS).
- D3 RD-965 four routes: comments plus pin cells, no re-gate (reads and public-by-design routes; the ruling says "administrators only for writes"; the `rd978` pins at `:68`, `:90` stay true). RD-966: pin only, under the default open-window reading.
- D4 Managed identity: admin-only plus an early return before the metadata dial unless `isAzureDeployment` (`server.js:689`); inventory fence `cellsWithRefusedDial` must lose that route (proved against the BASE control drive `inv14`).
- D5 Hard-code the status literals from the BASE inventory print, never from the old branch and never read from the inventory inside a test (circular).
- D6 Chain order fixed from the previous seat's Corrections: inventory before any cell that reads the regenerated docs; `chain.done` written when a step ENDS green; every tool prints a `--plan` and starts nothing, proved before the lock (that seat ran a whole mutation step outside the lock by calling `mut.sh --dry`); ONE acquisition (that seat took six); the `--check` line "runtime rows N; committed rows N" copied from a real run (from its STATUS; the kit does not quote the old wrong wording).
- D7 K is PREDICTED needed (six new suites, about 23 cells: pair about 5635 / 349), unlike the previous kit; step 7 is expected to refuse on counts only, then `--update-counts` in `v7`, commit K, plain verify at `chk17`.
- D8 `scripts/role-capability-inventory.js` and `rd978-...:84` are in OWNS (one control line and one pin); the previous kit called the script "not yours". The old branch edited both the same way.

## Q-questions for Tuesday (each with the default the kit already holds)
- **Q1 Open mode.** "No admin routes in open (no sign-in) mode" versus Kam's first-run rule (C-01, `authEnforcement.js:630`) and `decide()` (`capabilities.js:249` allows mode `open`). A literal reading would refuse the installer on mail, costs, first-run completion. Default: open window unchanged; the 14+2 admin rows that already refuse in open mode are pinned (RD-966). If the product owner meant the stricter reading, that is a separate ruling and ANSWER file before launch, and rd436's open-window write probe (`POST /api/settings/business-hours`) breaks.
- **Q2 RD-793.** The old branch also gates the four data-source mutators (RD-793, not in your list) and moves two connection tests to the L1 list. Default: NOT in this kit (named under Never; carried as OWED in READY); a later small kit.
- **Q3 Router gate placement.** Default: `/i` regex gates in `server.js` (D2). Alternative: pass the gate into the routers so routing and gating cannot disagree (the 2026-11-10 verdict's own suggestion) but that edits `routes/feedback.js` and `routes/sustainability.js`, lane B files.
- **Q4 "Only inside Azure".** Default predicate `isAzureDeployment` (`AZURE_MANAGED_APP`/`AZURE_MARKETPLACE`) plus the existing App Service variables; a plain Azure VM without those flags would no longer be detected. Say if the Azure VM case must keep working.
- **Q5 RD-965 reads.** Default: `GET /api/settings/emails` and `GET /api/risk-conditions` stay viewer-readable (field masking belongs to the permission core, RD-930 to 932); `POST /api/support/ticket` stays public. Change at the stamp if the ruling should cover them.
- **Q6 Gate tier.** Default G1 Opus (security surface). The two earlier gates on this surface were Opus.

## Chain input table (rule 4: each input exists at BASE or is made by an earlier step)
| step | inputs | produced by |
|---|---|---|
| 1 red-first (`old2`) | six new test files | commit A, before the chain, in `wt` |
| 2 inventory (`inv14` BASE, `inv18` A) | BASE tree; A | BASE clone; A |
| (commit I inside step 2) | the two docs from `inv18` | step 2 |
| 3 new-cells (`new3`) | A + I's two docs | A; step 2 |
| 4 related, 4b e2e (`new3`, `old2`) | same tree; main for the control | steps 2, 3 |
| 5 mut (`mut3` at I) | I | step 2 |
| 6 mainmove | `origin/main` | fetch |
| 7 p-plain (`chk16` at head) | head | A, I (M) |
| 8 u-update (`v7`) | head | same |
| 9 kstep | counts file from `v7` | step 8 |
| 10 p-plain-K (`chk17` at K) | K | step 9 |

## UNMEASURED (nobody has; the kit measures at the step shown)
- That a server in the harness answers every cell as predicted (I booted nothing and ran no jest, fences). Red-first prediction of about 15 red and 8 green of 23 is read from source and the inventory, not run.
- New `[gated, gatedWrites]` pair in `rd978` (predicted 60 and 45); the exact cell count (23 predicted); the final pair (about 5635 / 349).
- Which `static/` callers break for a viewer after gating (the kit asks for the list in READY; I did not grep static, only counted 42 static js and html files).
- Whether the e2e browser script runs on this machine (Chrome, playwright).
- Alerts inside the edit windows (Step 1a).
- Organisation-level `CI_DEPLOY_ENABLED`.
- Lock hold of about 100 to 130 minutes is arithmetic from the previous seat's timings (inventory 152 s and 151 s, verify about 20 minutes), not measured on this change.
- The sweep's frame note gave 973 blobs for NexusAI; my tree read returned 1005 blobs (1065 entries, `truncated` false). I did not resolve the difference (the sweep's four numbers may be in a different project order); nothing in the kit relies on it.

## Outside-the-fences disclosure
- Writes: the kit, its `.measured` sidecar, this report, and files in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s275/d_nxs/` (`jira_get.py`, `slots.py`, `names.py`, `census.py`, `fill.py`, `rd958.txt` to `rd968.txt`, fetched copies under `main/` and `old/`, `refs.txt`, `census.out`, `alerts.tsv`, `tree.txt`). I moved my own first `.measured` skeleton to my session scratchpad when I re-initialised after a text edit.
- GitHub: `gh api -X GET` only, under the project's `GH_CONFIG_DIR`; contents, compare, trees, matching-refs, code-scanning, actions runs and variables reads. Jira: GET only, five issues and their comments. No az, ssh, docker, mail, `decision_queue.sh`, `fleet/briefs_staged`, scoreboard, `_ledger.md`, WEDNESDAY, FRIDAY, Secuura or other non-Datasec tree.
- Reads of project state outside GitHub: `CLARIFICATIONS.md` lines 2067, 2611, 2672-2700 and a phrase search; the NexusAI Briefs folder (B1545 STATUS Corrections and `--check` lines, B1553 STATUS tail); `.tools/` directory listings of b1532 and b1545 (names only); `session-tools/locks-laptop-1017` listing; `session-tools/b1375/scanlib1114.py:20` (byte count only); the project `.env` read in-process by the Jira helper; `tmux list-panes`, `lsof`, `uptime`. Read the B1480 and B1480-2 verdict files, the B1545 kit, DRAFTER-REPORT and the B1553 kit's OWNS block.
- DRAFTER_RULES.md names `/Volumes/Laptop-DEV/...`; I used `/Volumes/Datasec_DEV` everywhere.
- Hook events: my first Bash call contained a `cd` and was refused (nothing ran); several advisories on `grep | cut` and a `$?` read after a pipe; I re-ran the stamp check alone for its rc. No fence was bypassed.
- Weakest parts: the RD-968 no-dial cell (depends on the preload's refused-dial record, read from the helper's header only), the predicted red-first split, and Q1.
