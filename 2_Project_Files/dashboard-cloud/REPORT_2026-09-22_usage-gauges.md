# External dashboard — usage gauges on the live board (report, written 2026-09-22 09:26:23 AEST)

**Builder:** Wednesday's usage-gauge builder subagent (delegated ~09:00). **Ask:** Kam, live board 2026-09-22 08:57:36 (verbatim): "One possible change to the live dashboard with the local version, I was able to see the weekly usage count on both Wednesday and Tuesday. Is this possible for the live version?" **Bound:** ~60 min; finished at 09:26 — no PARTIAL marker; nothing half-built was deployed (the first deploy carried a guard I then removed — see slip 1 — and the second deploy is the one probed 90/90).

## BLUF
**Yes, and it is live.** The agent chips on the live cockpit and chat pages now read `WEDNESDAY — 60%` (renewal + reading age in the tooltip) exactly as on the local board; Tuesday's chip reads `— no reading` until her seat runs the one arming command below (her seat publishes its own figure with its own certificate — nothing here can publish for her). Publisher armed on this seat (pid 9380, 120 s loop), doctor check + PORTABILITY item added, live probe matrix **90 PASS / 0 FAIL** (70 unchanged + 20 new), secret scan CLEAN, nothing deleted, nothing committed (Wednesday reviews), tenant assertion PASS on both deploys, no new Azure resource (one new TABLE `usage` inside the existing storage account — data plane, cents).

## Slips (mine, stated first)
1. **A guard that could pin a fixture on the board.** My first server version ignored a reading whose timestamp was older than the stored one ("out-of-order safety"). The probe's fixture (42 %, ts = now) was then *newer* than this seat's real reading (ts = the statusline's last heartbeat, 13 min earlier), so the real 60 % could not displace the fixture — the publisher printed "HTTP 200" and called it success, and the live board said 42 % for ~4 minutes (09:16–09:20, first deploy) — a probe value shown as real. Found by reading the raw row after the probe, not by the probe itself. Fixed at the root: guard removed (ONE publisher per seat; last write wins; the publisher only sends readings < 30 min old; the page always shows the age), the publisher now judges success on the server's `stored` echo, and probe I8 asserts the board is left at THIS seat's REAL reading (== `usage_wednesday.json`). Redeployed; re-probed.
2. **Silent harness arms.** Seven of my python probe arms were `|| FAIL=1` with no FAIL line: a `%` in a %-formatted print ("99% with") threw after the assertion passed, the probe returned rc 1 with "89 PASS / 0 FAIL" on the tally. Every arm of mine now prints a FAIL line; the tally and the rc agree (90/0, rc 0).
3. The loopback matrix's "missing file" arm reused a fixture filename a later step creates — on the second run the file existed and the seat-name refusal (rc 2) fired instead of rc 3. Arm fixed to a name nothing creates.
4. A `--dry-run` tick wrote the health file; fixed (dry runs never touch health). The already-running loop was restarted so the process on this seat is the file on disk.
5. One `cd` in a tool call (refused by the hook; re-issued) and one over-broad grep that swept a gateset scratch tree (timed out; narrowed).

## Built (paths, all under `2_Project_Files/dashboard-cloud/` except doctor.sh)
- **App** `app/main.py` (backup `main.py.pre-0907-usage`): `POST /api/seat/usage` (Seat.Write; **seat = the token's app id, never the body** — body `seat` naming another seat → 403 "usage rows are attributed by the token"; unmapped app id → 403; pct 0..100, `resets_in` ≤ 32 chars `[A-Za-z0-9 ]`, `ts` ISO-8601 UTC seconds, not in the future; one row per seat, REPLACE); `GET /api/seat/usage` (Seat.Read, both rows — the read-back); `GET /api/usage` (viewer, Easy Auth) — the local `/api/usage` shape `{wednesday: {seat,pct,resets_in,reading_ts,age_seconds,written_by,written_at}|null, tuesday: …}`; health gains `usage_route: true` (phase string unchanged — H1 still asserts "3"). Store: table `usage` (created on first use by the app's managed identity, Table Data Contributor; also created by the loopback run), PartitionKey `USAGE`, RowKey `<seat>`, clear columns only — a sibling table so `migrate_rewrap.py` / `mark_synthetic.py` (which scan messages+cards whole) see nothing new (re-checked: to_rewrap 0 / 0).
- **Pages** `app/static/index.html`, `chat.html` (backups `.pre-0907-usage`): the local page's block, one source difference (`WED.getJSON("/api/usage")`, 60 s poll). States: < 15 min → `— 60%`; 15–30 min → `— 60% (22m)` dimmed; absent or ≥ 30 min → `— no reading` dimmed, tooltip keeps the last figure + age ("last published 2h ago (60%); this seat may not be running"). Tooltip on a live figure: "weekly plan usage, published by the wednesday seat · renews in 5d 2h · reading 2m old". The two pages carry a byte-identical block (asserted). The "not synced yet — it lives on the Studio" tooltips are gone.
- **Publisher** `seat/post_usage.py` (new): reads `<tree>/0_Brain/dashboard/data/usage_<seat>.json`, refuses a file naming another seat (rc 2), publishes nothing on missing/unreadable/stale > 1800 s (rc 3, reason printed), POSTs as the seat, judges success on the server's `stored` echo; last stdout line is always `rc=<n>`. `seat/publish_usage.sh` (new): the loop — seat from **`fleet/cockpit/seat_resolve.sh`** (`$WED_AGENT`, else the tree name; never a hardcoded seat), `--once/--dry-run/--arm/--status`, 120 s interval, log `fleet/cockpit/logs/usage_publish.log`, health `fleet/cockpit/state/usage_publish.health` (OK / FAILING after 3 consecutive failures; idle ticks leave it alone), `--arm` idempotent (refuses a second loop for the seat).
- **Probes** `scripts/05_probe_live.sh` section I (backup `.pre-0907-usage`), `scripts/08d_local_matrix_usage.sh` (loopback :47792, real store, simulated Kam principal — 19 PASS), `scripts/09d_usage_page_checks.mjs` (the pages' own `usageState` in Node — 14 PASS). Outputs: `scripts/05_probe_live_usage_final.out`, `08d_local_matrix_usage.out`, `09d_usage_page_checks.out`, `04c_zip_deploy_only_usage.out` + `_usage2.out`, `07_secret_scan_usage.out`.
- **Doctor / portability**: `2_Project_Files/doctor.sh` (backup `doctor.sh.pre-0907-usage`) — "live usage publisher running; OK …" / WARN when not armed or FAILING (never a hard FAIL: a gauge is a degraded feature). `PORTABILITY.md` — state files + the per-boot `--arm` line. `README.md` — a "Usage gauges" section; "Not done" list updated.

## Deploy (path: `scripts/04c_zip_deploy_only.sh`, the Phase 3c route; tenant `d500ebad-…`, sub `0c57ab37-…`, RG `wednesday-dashboard-rg`, web app `wednesday-dashboard-e42e` — asserted by the script from `4_Credentials/.azure`)
- Deploy 1 (09:13:51, with the guard): `tenant assertion PASS` · `zip private-key markers: 0 (must be 0); positive control … 1` · `WARNING: Status: Site started successfully. Time: 47(s)` · health `usage_route:true` at 23:15:52Z.
- **Deploy 2 (09:21, the version probed):** `tenant assertion PASS` · `zip private-key markers: 0` · `WARNING: Status: Build successful. Time: 0(s)` · `Starting the site... Time: 46(s)` (the script's 600-char stderr head cuts before the "Site started" line — the proof that it started is the next item) · health at 23:23:02Z, 1 s after the deploy returned: `{"app":"wednesday-dashboard-cloud","ok":true,"phase":"3",…,"usage_route":true}`.
- Health now: `{"app":"wednesday-dashboard-cloud","ok":true,"phase":"3","ts":"2026-09-21T23:26:23Z","kam_keys":3,"seat_keys":["tuesday","wednesday"],"usage_route":true}`
- No new Azure resource; no setting, plan, identity or Easy Auth change (04c touches none). New table `usage` in the existing account (cents).

## Live probe matrix — `scripts/05_probe_live_usage_final.out`: **90 PASS / 0 FAIL, rc 0** (sections A–H unchanged, 70 PASS as in Phase 3; section I verbatim below)
```
### I. Usage gauges (2026-09-22) — seat-published, token-attributed, spoof refused, stale renders 'no reading'
PASS  I1 health: expected 200 got 200
PASS  I1 health: phase 3 + usage_route true
PASS  I2 GET /api/usage plain client (viewer route, Easy Auth gated): 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
PASS  I3 POST /api/seat/usage NO token: expected 401 got 401
PASS  I3 POST /api/seat/usage forged token: expected 401 got 401
PASS  I4 SPOOF: body seat=tuesday with the WEDNESDAY token (MUST refuse): expected 403 got 403
      body: {"detail":"usage rows are attributed by the token (this token is the wednesday seat)"}
PASS  I4 SPOOF: body seat=wednesday with the TUESDAY token (MUST refuse): expected 403 got 403
PASS  I4 pct=101 -> 400: expected 400 got 400
PASS  I4 ts not ISO -> 400: expected 400 got 400
      published wednesday 42% (reading 2s old, renews in '3d 4h') HTTP 200
PASS  I5 seat/post_usage.py --seat wednesday (fresh fixture 42%) rc: expected rc=0 got rc=0
PASS  I5 GET /api/seat/usage (seat read-back): expected 200 got 200
      wednesday row: {'seat': 'wednesday', 'pct': 42, 'resets_in': '3d 4h', 'reading_ts': '2026-09-21T23:24:44Z', 'age_seconds': 3} written_by: a9edf1d0… tuesday: None
PASS  I5 read-back: wednesday 42%, attributed to the WEDNESDAY app id by the token, reading_ts == fixture, age fresh
      raw row fields: ['PartitionKey', 'RowKey', 'Timestamp', 'etag', 'kind', 'pct', 'reading_ts', 'resets_in', 'seat', 'written_at', 'written_by']
PASS  I5 raw table row USAGE/wednesday: pct 42, written_by = wednesday app id (clear row, no envelope — a percentage is not prose)
PASS  I6 POST a 2h-old reading (99%) -> 200 replaced (last write wins; the page will show its age): expected 200 got 200
PASS  I6 stored echo: 99%, updated (no older-reading guard: a fixture must never be able to block the real reading)
      NOTHING TO PUBLISH: reading is 7201s old (> 1800s) — the wednesday seat may not be running; the live board keeps its last row and shows its age
PASS  I6 post_usage.py on a STALE reading (2h) publishes nothing: expected rc=3 got rc=3
PASS  I6 post_usage.py on a MISSING file publishes nothing: expected rc=3 got rc=3
PASS  I6 after the stale/missing attempts (nothing published) the row is the 2h-old 99% with age_seconds=7201 -> the page renders it as no reading
PASS  I7 page checks (usageState: fresh figure, ageing dimmed, stale >=30 min or absent -> 'no reading'; both pages identical): expected 0 got 0
      09d PASS lines: 14
      I8 real reading republished: published wednesday 60% (reading 1283s old, renews in '5d 2h') HTTP 200 rc=0
PASS  I8 the board is left at THIS seat's REAL reading: 60% @ 2026-09-21T23:03:25Z (== usage_wednesday.json)
### F. Rows per partition (counts only)
```
Secret scan (`07_secret_scan.sh`): `== RESULT: CLEAN`. Loopback matrix `08d`: 19 PASS / 0 FAIL. Page checks `09d`: 14 PASS.

## Publisher — arming state on THIS seat (Wednesday, the Studio)
- `publish_usage: RUNNING seat=wednesday pid(s) 9380  health: OK 2026-09-22 09:26:21 seat=wednesday published wednesday 60% (reading 1376s old, renews in '5d 2h') HTTP 200 `
- log: `2026-09-22 09:26:21 ok: published wednesday 60% (reading 1376s old, renews in '5d 2h') HTTP 200`
- Live row now (raw, `az storage entity query` table `usage`): `pct 60, reading_ts 2026-09-21T23:03:25Z, resets_in '5d 2h', seat wednesday` == `0_Brain/dashboard/data/usage_wednesday.json`.
- Armed as a detached loop from the script file (`publish_usage.sh --arm`, ppid 1) — the same shape as the live-chat poller (pid 14963, armed 2026-09-21 15:42 the same way). **Not in the launcher** (root file, out of my scope): after a reboot, `bash 2_Project_Files/dashboard-cloud/seat/publish_usage.sh --arm` (doctor warns until it is run). Wednesday may want the one-line spawn in `arm_wake_watch.sh`'s runner beside the poller's, once she claims that.
- **Honesty note on the reading's age:** the statusline writes `usage_<seat>.json` only when it renders (pct change, or a 300 s heartbeat per render). A seat inside one long tool call renders nothing, so its reading ages; at 30 min the live chip says `— no reading` (tooltip: last figure + age) while the local chip keeps showing the figure dimmed with its age. Same fact, two renderings — the live one follows the brief's 30-min rule. (This seat's reading is 21 min old as I write, because the parent session has been waiting on me.)

## What I did NOT test (stated)
- No browser: the chips are proven on the pages' own `usageState` in Node (09d) and the API round trip; the rendered DOM on a signed-in device is Kam's reload to prove (chip text `WEDNESDAY — 60%`, tooltip, dimming).
- Tuesday's seat end to end from the mini (her certificate, her file): her token was exercised only for the spoof refusal (I4: tuesday token + body seat=wednesday → 403). Her own publish is her arming paragraph below.
- The managed identity creating the `usage` table: the loopback run (Kam's CLI credential) created it first, so the app's `create_table_if_not_exists` was exercised as a no-op only.
- A reboot / launcher re-arm path; the FAILING (3 consecutive failures) branch of the loop was not exercised live (only read).

## For Tuesday — arming paragraph (verbatim, Wednesday sends it)
Tuesday: pull the tree (`dashboard-cloud/seat/post_usage.py`, `seat/publish_usage.sh`, the doctor.sh / PORTABILITY / README edits) on the mini, then run once from your tree: `bash 2_Project_Files/dashboard-cloud/seat/publish_usage.sh --once` — it resolves the seat from `fleet/cockpit/seat_resolve.sh` (`$WED_AGENT=tuesday` on your launcher, else the TUESDAY tree name), reads YOUR `0_Brain/dashboard/data/usage_tuesday.json` (written by your statusline_publish.sh; if it is older than 30 min or absent it prints "NOTHING TO PUBLISH" with `rc=3` and sends nothing — run a turn so the statusline writes, then retry), and POSTs it with `4_Credentials/dashboard-cloud/tuesday-seat.pem/.crt` to `POST /api/seat/usage`; expect a last line `rc=0` and the line above it `published tuesday NN% (...) HTTP 200|201`. Then arm the loop: `bash 2_Project_Files/dashboard-cloud/seat/publish_usage.sh --arm` (idempotent; `--status` shows the pid and the health line; log `fleet/cockpit/logs/usage_publish.log`), and re-run it after every reboot (`doctor.sh` warns while it is not armed). Acceptance: on the live board Kam's TUESDAY chip reads `— NN%` within 2 minutes; the server attributes the row by your token, so the Wednesday seat cannot publish it for you and a body naming another seat is refused 403 (probe I4 proves both directions).

## For Wednesday (wrap duties, not done by the builder by rule)
- Review + commit (scan CLEAN; backups `.pre-0907-usage` beside each edited file; `scripts/*.out` gitignored). Receipt Kam's 08:57 row: yes — live now; Tuesday's chip fills when she arms hers.
- Send Tuesday the paragraph above.
- Optional: the one-line spawn beside the poller's in `arm_wake_watch.sh` / the launcher so a reboot re-arms both.
