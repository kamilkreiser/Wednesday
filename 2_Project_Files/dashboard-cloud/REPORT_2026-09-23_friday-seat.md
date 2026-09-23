# REPORT 2026-09-23 — live board: FRIDAY seat + tab, file hide, drawer-X fix (builder A)

Saved by Wednesday from the builder's final message (its own write was refused by the harness).
Brief: `fleet/briefs_staged/2026-09-23_friday_liveboard_builder.md`.

## 1. INCIDENT — test rows on the live board, then a ~23-minute outage
**Test rows.** The older local matrices (03, 08, 08c–08f) run the app on 127.0.0.1 **but against the REAL storage
account**, so "local" rows landed in the store Kam's page reads. 08c posted Kam-role rows without a synthetic mark; 08f
marks its row ~1 s after posting (Kam's open page caught it). Kam saw them and wrote 11:18:12 *"This was not me, it was
automatically generated."* Remedy (nothing deleted): 08c's two rows flagged `synthetic=true` at 01:17:08Z, 08f's was
already flagged; `kam_msgs.sh` now skips all three.
Rows written by the 11:15 run: messages/WED `2026-09-23T01:15:53.029Z_p3l-good-011552` (flagged) · messages/ALL
`…01:15:53.036Z_p3l-both-011552` (flagged) · messages/WED `…01:15:58.369Z_kam-fl-011556` (flagged) · messages/WED
`2026-09-22T00:00:56.000Z_hide-probe-011556` and messages/Datasec `…hide-probe-tue-011556` (synthetic) · 10 AUDIT rows
`01:15:57.976Z_8cfc6395`…`01:16:13.181Z_32a8f62f` · files/WED `01:15:56.731Z_f-4db1c859910c` (+blob, flagged) and
`01:15:59.875Z_f-seatrow-011556` (synthetic, never listed) · usage `wednesday` (overwritten since).
**Guard:** 03, 08, 08c, 08d, 08e, 08f now REFUSE (rc 2) unless the base URL is loopback AND `LIVE_STORE_MATRIX_OK=1`
is set deliberately; all six proven to refuse (`scripts/08_guard_refusals_0923.out`). 08c now marks its Kam rows at
post time. The new Friday matrix 08g runs on an in-memory double of the store.
**Outage 01:27–01:50Z (11:27–11:50 AEST).** SEAT_APP_MAP update → site restart; the zip deploy ~1 min later hit Kudu 502
and a hung oryx build; the container restarted into a half-replaced tree (`can't chdir to 'app'`) and the platform
STOPPED the site. The zip was sound (app/main.py at root, byte-identical). Cause most likely the deploy racing the
settings restart — not reproduced. Recovery: previous version redeployed, healthz 200 at 01:50:29Z + authenticated
read; new zip started locally with the site's own startup command; redeployed 01:52Z, healthz 200 throughout, new
code serving from 01:54:56Z. Three deploys, not the one the brief allowed.
Found, left: `get_kam_messages.py --json` does not filter synthetic rows (only the text output does).

## 2. Live now
Partition `Friday` (seat friday), FRIDAY tab on both pages (existing page colour token), Friday usage chip; seats can
hide their OWN file rows (none hidden); drawer-X fix `#drawer[hidden]` deployed. Live probe 05: 182/0. The Friday
partition holds one synthetic probe row `2026-09-23T01:56:13.725Z_probe-fri-015612`. Secret scan clean (covers Friday).

## 3. Entra
`friday-seat` appId **be8404ab-374f-4e7c-a4f4-29377e2da0ef**, SP e36cfbca-59d0-451f-90b3-51de97208c22, cert thumbprint
F38D4640C534314ADDF17E8BF08A3BE706A3EA69; roles exactly Seat.Write, Seat.Read, Client.Friday (asserted). App role
Client.Friday added to `wednesday-seat-api` (id 11111111-0000-4000-8000-000000000014). Key pair
`4_Credentials/dashboard-cloud/friday-seat.pem` (0600) + `.crt`; public `app/keys/friday-seat-public.pub`.
SEAT_APP_MAP read first, `be8404ab-…:friday` appended via `az webapp config appsettings set`.

## 4. Files (backups `.pre-0923-1111-friday` unless noted)
app/main.py · app/static/{common.js,index.html,chat.html,drawer.js} · seat/{envelope.py,seat_common.py,hide_message.py
(new `--file`),get_kam_messages.py,get_files.py,share_file.py,post_usage.py} · scripts/{04_deploy.sh,05_probe_live.sh
(section L),09b_page_checks_phase3.mjs} · README.md · scripts/ids.conf (`.pre-0923-1110-friday`) ·
scripts/08c (`.pre-0923-1117-friday`) · scripts/03,08,08d,08e,08f (`.pre-0923-1121-friday`) · scripts/07_secret_scan.sh
(`.pre-0923-1158-friday`). New: scripts/01d_friday_identity.sh, 08g_double_app.py, 08g_local_matrix_friday.sh,
app/keys/friday-seat-public.pub.
**Left:** `seat/publish_usage.sh:30` accepts only wednesday|tuesday — it was RUNNING (pid 9380); needs `friday` added
with the loop stopped, or the laptop cannot publish Friday's usage.

## 5. Arms
08g (in-memory double) 92/0 (friday writes only Friday, 403 on Secuura/Datasec/WED; reads Friday+ALL only; wed/tue 403
on Friday; Kam's friday-tab message wrapped to ring + friday key only; file hide owner/unhide/403/audit) · 08d 19/0 ·
08e 53/0 · 08f 26/0 (pre-guard) · 08c 16 + 1 expected-seat-count fail, updated not re-run · guard 6/6 refused ·
09b page checks 27/0 (red on the old pages) · real headless browser vs the double: FRIDAY tab switches, drawer X hides
(computed display none) · live 05 182/0 incl. 21 Friday · zip read: `"Friday"` ×3 in app/main.py, identical to disk.
**Wednesday's own check:** `get_kam_messages.py --seat friday` against LIVE → rc 0, readable partitions exactly
['ALL', 'Friday'].

## 6. Not tested
Kam's own browsers / a live Kam message on the FRIDAY tab (Entra blocks automated Kam posts) · the laptop · Friday
cannot read the 3 pre-existing ALL rows until `migrate_rewrap.py` (changes live rows; not run) · 08c post-edit.
