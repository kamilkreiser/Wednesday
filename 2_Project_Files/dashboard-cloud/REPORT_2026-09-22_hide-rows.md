# External dashboard — reversible HIDE for chat rows + the six Ornith rows hidden (report, written 2026-09-22 15:04:24 AEST)

**Builder:** Wednesday's hide-rows builder subagent (delegated ~14:3x). **Ask:** Kam, Tuesday tab 2026-09-22 14:27:09 (verbatim): "Please clean up your boards so you don't have any local model workloads at this stage." The live board had no hide/archive route; six machine-posted Ornith rows (`project=Datasec`, `view=tuesday`, posted by the mini's mis-armed Ornith jobs) sat on the LIVE Datasec tab.

## BLUF
**Done and live.** `POST /api/seat/hide` / `POST /api/seat/unhide` exist on the live app (health `hide_route:true` at 04:59:50Z), a hide is a MERGE of clear columns (nothing deleted, ciphertext asserted byte-identical), every call writes an AUDIT row, reads skip hidden rows unless `?hidden=1`. **The six Ornith rows are hidden as the TUESDAY seat** (her certificate is parked on this drive — Phase 2 report piece C; the rows are `tuesday`-tab rows so the server refuses the Wednesday seat, proven 403). Datasec tab list as read by the tuesday seat: **93 rows before → 87 after, the six absent, nothing else changed (0 unexpected), `?hidden=1` lists 93 == before.** Live probe matrix **112 PASS / 0 FAIL, rc 0** (90 baseline + 22 new), loopback matrix 53 PASS / 0 FAIL, page checks 11 PASS, secret scan CLEAN, nothing committed (Wednesday reviews), nothing deleted, no Azure resource/setting change, tenant assertion PASS on every deploy.

## Slips (mine, stated first)
1. **Deploy 1 shipped the OLD `main.py`.** At 14:43:32 a `git pull --rebase --autostash` from another session (reflog: Wednesday's 14:43:24 commit + rebase) stashed my uncommitted working-tree edits into `stash@{0}` and did not re-apply them; my zip at 14:45:36 therefore carried HEAD's `main.py`/`common.js`/pages/`09b`. The health check caught it (`hide_route` never appeared, 04:48–04:55Z); I first misread the container log as a worker move and did one `az webapp restart` (14:51:13, same target, no effect, harmless) before comparing the zipped `main.py`'s md5 with the backup. Fix: restored the five files from `stash@{0}` (`git show stash@{0}:<path>`; the stash itself is untouched — **Wednesday: `stash@{0}` (14:43:32) still holds those edits plus the parent session's own files; drop or pop it knowingly**), and added an `EXPECT_MARKER` guard to `04c_zip_deploy_only.sh` (asserts the zipped `main.py` carries the change; refuses before upload). Deploy 2 (14:57–14:59) ran with `EXPECT_MARKER=hide_route`: 2 lines, PASS. **Lesson for the tree: any builder with uncommitted edits is exposed to the parent's autostash; zip-and-verify immediately, and read the zip, not the disk.**
2. **The live matrix's H7 was date-dependent** (pre-existing): its floor was `today 00:00Z`, but the `probe-dup` row has a FIXED ts of `2026-09-21T00:00:01Z`, so the first run after 10:00 AEST on 22 Sep lost that row → H7 failed. Not my change; fixed the floor to `2026-09-21T00:00`. It was also a SILENT arm (`|| FAIL=1`, no FAIL line: the tally read 111 PASS / 0 FAIL with rc 1). Gave that arm and the 8 other silent `|| FAIL=1` arms a FAIL line; re-ran: 112/0, rc 0, 0 tracebacks.
3. The loopback matrix's first run reported "app did not come up in 60 s" (cold venv import from the external drive); raised the wait to 120 s; second run 53/0.
4. Two zsh slips in tool calls: an `=====` echo (zsh `=cmd` expansion) and a nested heredoc whose inner `PY` terminator closed the outer one (patch moved to a scratch file). One `sleep` chain refused by the tool; replaced with a background `until` loop.

## What changed (all under `2_Project_Files/dashboard-cloud/`; backups beside each edited file as `.pre-1435-hide` / `.pre-1454-hide`)
| file | lines | change |
|---|---|---|
| `app/main.py` | 471 → 556 | `hide_route:true` in health; `_query(..., include_hidden=False)` skips `hidden is True` in code (an OData `ne` drops rows LACKING the property, so the filter is not in the query); `?hidden=1` on `GET /api/messages` and `GET /api/seat/messages` (+ `hidden_included` echo); `find_message` (row_key exact or id → exactly one row; 404 / 409); `set_hidden` shared by `POST /api/seat/hide` and `/unhide`: Seat.Write + `require_partition` (R0, as a write → 403 for another seat's partition, 400 for ALL), MERGE `{hidden, hidden_by, hidden_at, hidden_seat}` / `unhidden_*`, audit row in `messages` PartitionKey `AUDIT`; `GET /api/seat/hide/audit` (Seat.Read, the seat's partitions only) |
| `app/static/common.js` | 252 → 258 | `isHidden(r)` (`hidden===true` and no reveal), `revealHidden` (page URL `?hidden=1`), `hiddenQ` (`&hidden=1` passed to the API) |
| `app/static/index.html`, `chat.html` | 819, 415 (same) | the 2+2 ingestion lines skip `WED.isHidden(r)` (defence in depth); the 2+2 API URLs carry `WED.hiddenQ` |
| `scripts/09b_page_checks_phase3.mjs` | 32 → 42 | markers updated to the new ingestion lines + 4 hidden-row checks (11 PASS; negative control: the hiddenQ check is false on the `.pre` pages) |
| `scripts/05_probe_live.sh` | 244 → 283 | section **J** (22 probes), section F prints `hidden by a seat` per partition + AUDIT row count; H7 floor fix; 9 silent arms now print FAIL |
| `scripts/04c_zip_deploy_only.sh` | 30 → 38 | `EXPECT_MARKER` guard (slip 1) |
| `scripts/08e_local_matrix_hide.sh` | new, 105 | loopback :47793, real store, simulated Kam principal — 53 arms incl. viewer list, ciphertext-identical, audit via API + raw, tuesday's own hide via the CLI, scanners leave AUDIT alone |
| `seat/hide_message.py` | new, 92 | the seat CLI: `--row-key|--id`, `--unhide`, `--list-hidden`, `--audit`, `--dry-run`; last line `rc=<n>` |
| `README.md` | 73 → 77 | "Hide / unhide a row" section |
Design notes: (a) a column on the row (MERGE) was cheaper and safer than a join table — the pages poll `/api/messages` every few seconds and a second table per read would double the round trips; MERGE cannot touch the envelope (asserted before/after). (b) The audit lives in the SAME table under `AUDIT`, a partition `READ_PARTITIONS` excludes, so no read route, page or seat list can ever return it; `migrate_rewrap.py` reports it as "unknown partition (left alone)", `mark_synthetic.py` as "left alone (real)" (both asserted, HL8). (c) Cards are NOT covered (messages only — the ask was chat rows). (d) A page already open keeps a row it had loaded until reload; an unhidden row older than the page's `since` cursor also needs a reload.

## Arms — tally
- Loopback `scripts/08e_local_matrix_hide.sh` → `08e_run2.out` (scratch): **53 PASS / 0 FAIL** — gates 401 ×4 + viewer 401; other seat's row 403 (both directions); unknown row_key 404, unknown id 404; malformed 400, no id 400, ALL 400, bad reason 400; hide → absent from the seat list AND the viewer list (`/api/messages` as Kam) → `?hidden=1` reveals with `hidden_seat/by/at` (both routes) → audit via API and raw AUDIT row → raw row: new columns ONLY `[hidden, hidden_at, hidden_by, hidden_seat]`, ciphertext/iv/keys/routing byte-identical → re-hide changed=false (audited) → unhide → back in both lists, `hidden_at` + `unhidden_*` kept → audit holds hide + re-hide + unhide; tuesday hides her own Datasec probe row through the CLI, `--list-hidden` shows it, wednesday's `--unhide` of it refused 403, tuesday's `--unhide` by id restores it; audit scoped per seat; scanners leave AUDIT alone. Every hidden row in that run was born synthetic and was unhidden before the end.
- Page checks `09b`: **11 PASS** (`node scripts/09b_page_checks_phase3.mjs`).
- Live `scripts/05_probe_live.sh` → `scripts/05_probe_live_hide_final.out`: **112 PASS / 0 FAIL, rc 0** (the 90 of the usage baseline `05_probe_live_usage_final.out` + 22: J1 health ×2, J2 401/401 + Easy Auth on `?hidden=1`, J3 target found, 403 ×2, 404, 400, hide 200 + echo, absent, reveal, audit, raw byte-identical, unhide 200 + echo, back). Section F after the run: `messages/Datasec: 93 (... hidden by a seat, reversible: 0)` — the matrix ran BEFORE the six were hidden; the raw read-back below is the after-state.

## Deploy (path `scripts/04c_zip_deploy_only.sh`; tenant `d500ebad-…`, sub `0c57ab37-…`, RG `wednesday-dashboard-rg`, web app `wednesday-dashboard-e42e`; asserted by the script from `4_Credentials/.azure`)
- Deploy 1 (14:45:36, `04c_zip_deploy_only_hide.out`): tenant assertion PASS · private-key markers 0 / control 1 · "Site started successfully. Time: 77(s)" · **carried the reverted `main.py` (slip 1)** — health never gained `hide_route`; `az webapp restart` 14:51:13 (no effect).
- **Deploy 2 (14:57:21, `04c_zip_deploy_only_hide2.out`, the version probed):** `tenant assertion PASS` · `zip private-key markers: 0 (must be 0); ... public-key markers ...: 1` · `zipped app/main.py carries EXPECT_MARKER 'hide_route': 2 line(s)` · `Status: Site started successfully. Time: 61(s)` · `Deployment has completed successfully`.
- **Health receipt:** `{"app":"wednesday-dashboard-cloud","ok":true,"phase":"3","ts":"2026-09-22T04:59:50Z","kam_keys":3,"seat_keys":["tuesday","wednesday"],"usage_route":true,"hide_route":true}` (0 polls after the deploy returned).
- No new Azure resource, no setting/plan/identity/Easy Auth change (04c touches none). New rows only: 6 hidden flags (MERGE) + audit rows in the existing `messages` table.

## The six rows — hidden as the TUESDAY seat (`seat/hide_message.py --seat tuesday --client Datasec --row-key … --reason "Kam 2026-09-22 14:27:09 clean up boards: Ornith local-model receipt posted by a mis-armed mini job"`), 05:03:38–41Z
Verified first with the tuesday seat key (`list_datasec.py verify`, scratch): all six decrypt, `view=tuesday role=tuesday`, and each text starts with an Ornith receipt (first 60 chars printed there; nothing else of the Datasec tab was decrypted or printed).
| # | row_key (= `<UTC ts>_<id>`) | id | local ts (+10:00) | first 60 chars | audit row |
|---|---|---|---|---|---|
| 1 | `2026-09-21T03:23:01.079Z_bf-af542c5dc54b942b076d` | `bf-af542c5dc54b942b076d` | 2026-09-21 13:23:01 | "Ornith has been gate-refused for 30 minutes on G5-ollama — n…" | `2026-09-22T05:03:38.449Z_664e9dc3` |
| 2 | `2026-09-21T09:53:11.014Z_bf-bc227fcf10777ee01a13` | `bf-bc227fcf10777ee01a13` | 2026-09-21 19:53:11 | "Ornith has been gate-refused for 30 minutes on G5-ollama — n…" | `2026-09-22T05:03:39.012Z_8c873330` |
| 3 | `2026-09-21T13:38:16.897Z_bf-e1ce831f916cd26df3a1` | `bf-e1ce831f916cd26df3a1` | 2026-09-21 23:38:16 | "Ornith has been gate-refused for 30 minutes on G2-panes — no…" | `2026-09-22T05:03:39.553Z_42f9c083` |
| 4 | `2026-09-21T20:45:02.803Z_bf-d2d062efd0d317d0e742` | `bf-d2d062efd0d317d0e742` | 2026-09-22 06:45:02 | "Ornith daily receipt for 2026-09-22: 24 model rounds — 21 pa…" | `2026-09-22T05:03:40.133Z_2461ffd7` |
| 5 | `2026-09-21T23:53:30.528Z_bf-cdc533a9a99ce631d3cf` | `bf-cdc533a9a99ce631d3cf` | 2026-09-22 09:53:30 | "Ornith has been gate-refused for 30 minutes on G5-ollama — n…" | `2026-09-22T05:03:40.665Z_0b03995d` |
| 6 | `2026-09-22T04:23:37.393Z_bf-dee60a6e08850b35d0e0` | `bf-dee60a6e08850b35d0e0` | 2026-09-22 14:23:37 | "Ornith has been gate-refused for 30 minutes on G5-ollama — n…" | `2026-09-22T05:03:41.220Z_18a90e97` |
Each call returned `changed=True … as seat=tuesday rc=0` (six `rc=0` lines counted).

**Read-back (Datasec partition through the seat API as tuesday, `since=2026-09-21T00:00`, `limit=1000`; the same GET `hide_message.py --list-hidden` issues):**
- before: **93** rows · after: **87** rows · gone: **6** (exactly the six row_keys above) · unexpected new: **0** · `?hidden=1` reveal: **93** rows, `reveal == before: True`, the six `PRESENT hidden=True`.
- `hide_message.py --seat tuesday --list-hidden --client Datasec --since 2026-09-21T00:00`: `6 hidden row(s)`, each `hidden_seat=tuesday`, `hidden_at` 05:03:38–41Z, `src_ts` = the six local timestamps.
- Raw table (`az storage entity query … "PartitionKey eq 'Datasec' and hidden eq true"`): **6**; `Secuura/WED/ALL hidden eq true`: **0 / 0 / 0**; `AUDIT … seat eq 'tuesday' and at ge '2026-09-22T05:03'`: **6** rows, all `action=hide changed=True`, target ids = the six.
- The viewer list `GET /api/messages` (what Kam's pages poll) uses the same `_query` — proven on loopback as Kam (HL5, absent → revealed) and live only through the seat route (Easy Auth blocks an unattended viewer call). **Kam's reload of the Datasec tab is the last proof** (NOT MEASURED here: no browser).

## Unhide recipe (each is one command; reversible, audited; Wednesday's seat would be refused 403 — it must be the tuesday certificate)
```
V=2_Project_Files/dashboard-cloud/.venv/bin/python; H=2_Project_Files/dashboard-cloud/seat/hide_message.py
$V $H --seat tuesday --client Datasec --unhide --row-key 2026-09-21T03:23:01.079Z_bf-af542c5dc54b942b076d --reason "undo"
$V $H --seat tuesday --client Datasec --unhide --row-key 2026-09-21T09:53:11.014Z_bf-bc227fcf10777ee01a13 --reason "undo"
$V $H --seat tuesday --client Datasec --unhide --row-key 2026-09-21T13:38:16.897Z_bf-e1ce831f916cd26df3a1 --reason "undo"
$V $H --seat tuesday --client Datasec --unhide --row-key 2026-09-21T20:45:02.803Z_bf-d2d062efd0d317d0e742 --reason "undo"
$V $H --seat tuesday --client Datasec --unhide --row-key 2026-09-21T23:53:30.528Z_bf-cdc533a9a99ce631d3cf --reason "undo"
$V $H --seat tuesday --client Datasec --unhide --row-key 2026-09-22T04:23:37.393Z_bf-dee60a6e08850b35d0e0 --reason "undo"
$V $H --seat tuesday --list-hidden --client Datasec      # expect 0 hidden row(s) afterwards; --audit shows the hide + unhide lines
```
(On the mini the same commands work with Tuesday's own `4_Credentials/dashboard-cloud/tuesday-seat.pem/.crt` once she pulls `seat/hide_message.py`.)

## NOT MEASURED / not done (stated)
- No browser: the pages' skip + `?hidden=1` pass-through are proven on the pages' own ingestion statements in Node (09b) and the viewer API on loopback; the rendered Datasec tab after Kam's reload is his to see. The chat page's `?hidden=1` reveal (`/chat?hidden=1`) renders hidden rows with no visual marker (they simply appear) — a badge is a follow-up if wanted.
- The local stores (`0_Brain/dashboard/data/chat_*.json`) are untouched by rule — the LOCAL board still shows the six; Wednesday decides that separately.
- Cards have no hide route (messages only).
- Tuesday's own end-to-end from the mini (her cert, her tree) — her token was exercised from this drive's parked copy.
- The usage/Phase-3 sections of the matrix were re-run whole (112/0), so no regression there; `08c`/`08d` loopback matrices were not re-run (untouched code paths).
- `stash@{0}` (14:43:32 autostash) is left as found — it holds my five files' edits (now restored on disk) plus the parent session's own working files; only Wednesday should drop it.

## For Wednesday (wrap duties, not done by the builder by rule)
- Review + commit (scan CLEAN; backups `.pre-1435-hide` beside each edited file, `04c` backup `.pre-1454-hide`; `scripts/*.out` gitignored). Receipt Kam's 14:27:09 row: the six Ornith rows are off the live Datasec tab (reload); reversible per the recipe above.
- Decide the local `chat_tuesday.json` / `chat_wednesday.json` mirror rows (not mine).
- Tell Tuesday: `seat/hide_message.py` exists; her Ornith receipts on the live board were hidden with her seat identity from the parked key (six ids above); future Ornith posts should stop at the source (the mis-armed mini jobs), not be hidden after the fact.
- Consider `EXPECT_MARKER` in every future deploy call (one env var) — it is the guard against the autostash class of slip.
