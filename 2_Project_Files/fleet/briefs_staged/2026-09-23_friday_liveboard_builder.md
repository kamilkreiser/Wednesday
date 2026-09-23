# BRIEF — live board: add the FRIDAY seat + tab, extend hide to FILE rows, ONE deploy (WED, dashboard-cloud)

Commissioned by Wednesday (the Studio coordinator seat), 2026-09-23 ~11:10 AEST, on Kam's words
(live board, view=wednesday, verbatim):
- 10:49:26 *"…I'm thinking of changing the name of my laptop agent to Friday and creating a new folder… You might
  as well also add a Friday tab to the dashboard and give it the necessary keys etc. So create a new agent called
  Friday… Friday will work on both Secura and Dataset projects from this laptop."* and *"Please clear all the
  download files for now."*
- 10:57:27 *"the X that closes the files pop-up does not work."*

WHOSE IT IS / WHERE IT LANDS: Wednesday's own project (WED). Code under
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/`. Cloud: tenant `d500ebad-cf53-4f2a-a501-f831289e67fc`,
subscription `0c57ab37-349c-47ae-a10f-e284a380bbb9`, resource group **`wednesday-dashboard-rg` ONLY**, web app
`wednesday-dashboard-e42e`, and Entra app registrations in that tenant. All ids: `scripts/ids.conf`.

## HARD BOUNDARIES (read twice)
1. `export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure` in EVERY shell that runs `az`; assert
   `az account show` = that tenant + sub + `kreiser.org@me.com` first (`scripts/00_tenant_state.sh` shows how).
2. **The same subscription holds `datasec-sales-portal-rg` = Vision Sales Portal PRODUCTION. Never read-modify it, never
   list-and-act across the sub.** Every mutating `az` names `wednesday-dashboard-rg` or an Entra object id explicitly.
3. **Never delete anything** (files, rows, app registrations, secrets). Backups beside every file you edit:
   `<file>.pre-0923-<HHMM>-friday` with HHMM from `$(date +%H%M)` captured in the same command as the `cp`.
4. Private keys are generated into `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud/` ONLY (0600), never into
   the tracked tree, never printed, never committed. Run `scripts/07_secret_scan.sh` before you report.
5. **Do NOT commit or push.** Leave your changes in the working tree; Wednesday verifies at source and commits. Another
   seat (Tuesday) commits to this repo concurrently — never `git stash`, `git checkout --`, `reset`, `pull`.
6. The Bash tool is zsh. Never `cd` (a hook refuses it — use absolute paths). No `timeout` (macOS) — use a background
   job + an until-loop. Never send stderr to /dev/null; write command output to a file in your scratchpad and read it.
7. Never edit a running script (bash reads by byte offset).

## THE DESIGN (decided — do not redesign; if something here is impossible, STOP and say why in the report)
**A new client PARTITION `Friday`, owned by a new seat `friday`.** Friday serves both Secuura and Datasec from Kam's
laptop, so it cannot be mapped onto either existing partition without breaking R0 (a Friday reply about Datasec must
not be readable by the wednesday seat, and vice versa). Its own partition gives it its own conversation:
- `VIEW_TO_CLIENT`: add `friday -> "Friday"` (server `app/main.py:100` and page `app/static/common.js:38`).
- `CLIENTS` (`main.py:97`) gains `"Friday"`; `SEAT_OF_CLIENT` (`:110`) gains `"Friday": ("friday",)`; BROADCAST
  (`"ALL"`) becomes readable/wrapped for all THREE seats; `SEATS` (`:424`) gains `"friday"`; the loop at `:129` and any
  other `("wednesday","tuesday")` literal gains friday — **grep the WHOLE app + seat/ + scripts/ for every such literal
  (`/usr/bin/grep -rn -i tuesday`), with a positive control, and list each site you changed or deliberately left.**
- Hide ownership: a Friday-partition row is the friday seat's to hide; nobody else's.
- Usage gauges: a `friday` chip exactly like the other two (null until the laptop publishes).
- `seat/seat_common.py:32` `--seat` choices gain `friday`; the other seat CLIs keep working unchanged for the old seats.
- Pages (`index.html`, `chat.html`, `common.js`, `drawer.js`): a **FRIDAY** tab/toggle beside WEDNESDAY and TUESDAY,
  following the existing pattern exactly (Kam types into it → `view=friday`; replies from `seat=friday`/`client=Friday`
  render there; `drawer.js:21 whoOf` names "Friday"). Reuse the existing tab styling; no new colours outside the page's
  existing tokens (the style-guide rule).

**Identity (Entra), following `scripts/01b_identity.sh` for the tuesday seat:**
- Add an app role **`Client.Friday`** to the API app `wednesday-seat-api` (appId in ids.conf `API_APPID`).
- New app registration **`friday-seat`** with a certificate credential; roles on the API: `Seat.Write`, `Seat.Read`,
  `Client.Friday` — **and NOT Client.Secuura / Client.Datasec / Client.WED.** Admin-consent the assignments the same
  way 01b did.
- Cert pair → `4_Credentials/dashboard-cloud/friday-seat.pem` (0600) + `friday-seat.crt`; public key →
  `app/keys/friday-seat-public.pub` (same format as `tuesday-seat-public.pub`). Record `friday_seat_APPID=` in ids.conf.
- The web app's `SEAT_APP_MAP` setting gains `<friday appId>:friday`. ⚠ `04c`'s header records `az webapp config set`
  failing with NoRegisteredProviderFound on this CLI — if `az webapp config appsettings set` fails the same way, use
  `az rest` against an api-version the provider accepts, and record which one worked. **Read the current setting value
  first and APPEND; never replace it with a guessed value.**

**Files hide (the drawer clear):** `seat_hide` (`main.py:399`) merges onto `table("messages")` only; file rows live in
`FILE_TABLE` (`:146`), and `file_query` ALREADY skips `hidden is True` (`:615`). Extend hide/unhide to file rows (a
`kind`/`table` discriminator in the request, same ownership rule, same audit row shape) and extend
`seat/hide_message.py` (or a sibling) so a seat can hide its own FILE row by row key. Do NOT hide any existing row —
Wednesday does the clearing after the deploy, in an order Kam asked for.

**Already in the tree, must ride this deploy:** the drawer-X fix — `#drawer[hidden] { display:none; }` in BOTH
`app/static/index.html` and `app/static/chat.html` (backups `.pre-0923-1058-drawerhidden`). Keep it.

## VERIFY BEFORE DEPLOY (local)
Run the existing local matrices (`scripts/08c_local_matrix_phase3.sh`, `08e_local_matrix_hide.sh`,
`08f_local_matrix_files.sh`, `08d_local_matrix_usage.sh`) — all old arms still pass — PLUS new arms, each able to fail:
- friday seat token (or the local test double the matrices use) can POST to `Friday`; is **403** on `Secuura`, `Datasec`,
  `WED`; can read `Friday` + `ALL`; reading `Secuura`/`Datasec`/`WED` returns nothing of theirs.
- wednesday and tuesday seats are **403** writing `Friday` and cannot read Friday rows.
- a Kam `view=friday` message lands in `Friday` wrapped to Kam's ring + the friday seat key (and NOT to the other seats).
- file hide: the owning seat hides its own file row → `file_query` stops listing it; unhide restores; another seat's
  hide of it is refused; an audit row is written.
- page: the FRIDAY tab renders; the drawer X closes the drawer (`#drawer[hidden]` computed display none).

## DEPLOY (ONE deploy)
`scripts/04c_zip_deploy_only.sh` with `EXPECT_MARKER` set to a string that exists ONLY in the new `main.py` (e.g. the
`"Friday"` client literal) — **read the ZIP, not the disk**, before upload (the 2026-09-22 deploy shipped an OLD main.py;
`REPORT_2026-09-22_hide-rows.md`). Then `scripts/05_probe_live.sh` (all old sections) + live probes of the new arms that
can be run live with the real friday cert (post one `--synthetic` row to Friday, read it back, confirm 403 on another
client; mark it synthetic so no seat reads it as Kam's word). Health check green.

## REPORT (the deliverable)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/REPORT_2026-09-23_friday-seat.md`, BLUF first, then
FOUND / TESTED / HOW for each piece: every file changed (path + backup name), every literal site changed or left, the
Entra objects created (app id, role ids — no secrets), the SEAT_APP_MAP before/after, the deploy's zip marker line, each
arm with its command and output file, and **a NOT-TESTED list** (e.g. a real browser on Kam's devices). Last line of your
final message: the report path.
