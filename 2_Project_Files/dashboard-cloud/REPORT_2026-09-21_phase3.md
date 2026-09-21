# External dashboard — Phase 3 report (2026-09-21)

**Builder:** Wednesday's Phase-3 builder agent (delegated ~14:05). **Ruling:** Kam 12:50:55 (verbatim in the brief) — switch to the live version only; a new key for the laptop and one for the iPad. Design D-2(b) (Tuesday's shape, adopted by Wednesday): the record's data key is wrapped to Kam's key(s) AND the addressed seat's existing certificate public key.
**Scope:** (a) multi-recipient envelope + seat-side decrypt · (b) kam-laptop + kam-ipad device keys + re-wrap migration · (c) seat-side cut-over readers + watcher poller design. No commit, no push (Wednesday reviews). Local server + dual-write untouched.
**Written incrementally** — each piece appends below as it lands. If this file ends mid-piece, the builder was killed there.

## BLUF
See the full BLUF further down (written at 14:42, after the final probe run): (a) per-seat wrapped keys LIVE and proven, (b) laptop + iPad keys on the drive + all 2974 msgs / 232 cards re-wrapped (0 failed, idempotent), (c) the three readers default to the live board + a live poller with arms (not armed), plus Kam's two 12:48 asks (Updates un-stuck, synthetic rows hidden). **70/70 live probes PASS, secret scan CLEAN, nothing committed, nothing deleted.**

## Slips (mine, stated first)
Eight, consolidated at the end of this file under "Slips (mine) — consolidated"; the two that touched the world: ONE real tap into Wednesday's pane at 14:28:45 (poller arm with the fake tap helper unset), and a first `kam_msgs.sh` arm that would have silently cut Kam's newest rows (caught, fixed, warning added).

## Log
- 14:0x report opened. Read whole: the brief, the pilot report, the Phase 2 report, README, `seat/envelope.py`, `seat/seat_common.py`, `seat/get_kam_messages.py`, `seat/post_message.py`, `app/main.py`, `app/static/common.js`, `scripts/ids.conf`.
- 14:05 `az account show` (AZURE_CONFIG_DIR=4_Credentials/.azure): user `kreiser.org@me.com`, tenant `d500ebad-…`, sub `0c57ab37-…` → **ASSERTION PASS**. Token expiry measured: ARM 15:23:50, **storage 15:06:57** — so the az-dependent steps (migration, deploy, probes) run FIRST; if a call asks for a login I stop and report. `pgrep` for chat_reply/decision_queue/_live_board/kam_msgs/reconcile/kam_rulings/backfill/05_probe: none running.
- Also read: `scripts/04_deploy.sh`, `05_probe_live.sh`, `05b`/`08b` mjs, `07_secret_scan.sh`, `01a_keys.sh`, `seat/backfill.py`, `seat/post_card.py`, `tools/kam_msgs.sh`, `tools/reconcile_rulings.py`, `tools/kam_rulings_today.sh`, `tools/chat_push.sh`, `tools/tap_wednesday.sh`, `tools/_live_board.sh` (Wednesday edited it at 13:17 — `.pre-0921-1316-cardcertdir`), the chat leg of `fleet/cockpit/wake_watch.sh` (lines 140–167), the key bar + decrypt call sites in `index.html` / `chat.html`.
- Order of work chosen: (b-keys) → (a-envelope code) → (b-migration, az) → deploy (az) → probes (az) → (c) tools + poller.
- 14:06 **(b) keys generated** — `scripts/01c_device_keys.sh` (idempotent; output `01c_device_keys.out`): `kam-laptop-private.pem` + `kam-ipad-private.pem` (RSA-4096 PKCS8, mode 600) in `4_Credentials/dashboard-cloud/`; public halves `app/keys/kam-laptop-public.pub` / `kam-ipad-public.pub`; the two seat certs' PUBLIC keys exported to `app/keys/wednesday-seat-public.pub` / `tuesday-seat-public.pub` (SPKI from the .crt — public, tracked). kids (sha256(SPKI)[:16], = `envelope.kid_of` — the pilot's `ed9ec4e1156c5982` equals the Phase 2 report's, so the two computations agree): pilot `ed9ec4e1156c5982`, laptop `2ccbe41a20d93001`, ipad `c6d1765a828b469e`, wednesday-seat `8e844615d15e931e` (2048), tuesday-seat `8ad86866fc0d5680` (2048).
- 14:08 **(a) `seat/envelope.py`** rewritten (backup `envelope.py.pre-0921-1407-phase3`): `recipients_for(client)` = Kam ring (every `app/keys/kam-*-public.pub`, pilot first) + seat(s) by partition (`SEAT_OF_CLIENT`: WED/Secuura→wednesday, Datasec→tuesday, ALL→both); `encrypt_text(pub, text, clear, recipients=)` emits `wrapped_keys:[{kid,wrapped_key}…]` with the top-level `kid`/`wrapped_key` KEPT = the first ring entry (pilot) for one release; `encrypt_record(text, clear)` is the Phase-3 default writer; `unwrap_data_key` (bytes only, kid-selected) / `decrypt_text` fall back to the top-level pair for pre-migration rows; `rewrap(env, dk, recipients)` is idempotent. Scheme string unchanged (`…/v1`) — `wrapped_keys` is additive. Self-test: **PASS** (positive, wrong-key, AAD-relabel, multi-recipient ×3, non-recipient KeyError, rewrap idempotent, JSON-string wrapped_keys as Table storage returns it). Recipient sets resolved on this drive: WED/Secuura = pilot+ipad+laptop+wednesday-seat; Datasec = pilot+ipad+laptop+tuesday-seat; ALL = all five.
- 14:10 **(b) migration DRY-RUN** `seat/migrate_rewrap.py --dry-run` (output `scripts/migrate_dryrun.out`): BEFORE — messages 2974 rows (ALL 1 / Datasec 16 / Secuura 735 / WED 2222), cards 232 (Datasec 4 / Secuura 195 / WED 33); **all 3206 to rewrap, 0 already complete, 0 the pilot cannot unwrap**. (Phase 2 hand-over said 2961 msgs / 227 cards; the delta is Wednesday's dual-write since 12:47.)
- 14:10 ADDENDUM from Wednesday (Kam 14:05:04: "let's get the live site fully functioning and tested today so that we can interact normally while I'm traveling"): `05_probe_live.sh` gets a Phase 3 section run against the LIVE URL (per-seat decrypt ±, each device key on a migrated row, pilot still works, reply path wraps to the seat(s), live readers return Kam's rows); (c) readers are load-bearing. No browser is connected by me; what a browser still has to prove is stated in the report.
- 14:11 **(b) MIGRATION RUN 1** `seat/migrate_rewrap.py --sample 3 --workers 8` (output `scripts/migrate_run1.out`): messages **2974 rewrapped / 0 failed** (ALL 1, Datasec 16, Secuura 735, WED 2222) in 23.0 s; cards **232 rewrapped / 0 failed** (Datasec 4, Secuura 195, WED 33) in 1.7 s. After re-scan: every row `complete` (2974 / 232), 0 incomplete. Datasec rows were re-wrapped by unwrapping the DATA KEY only (`unwrap_data_key`, bytes) — their text was never decrypted. Sample table (3 rows per partition × 5 keys) in the piece (b) section below: every Kam key opens every row; the seat keys open exactly their partitions (ALL → both), `n/a` elsewhere.
- 14:12 **MIGRATION RUN 2 (idempotency)**: 2974 + 232 `already complete`, **0 processed** (`scripts/migrate_run2_idempotent.out`).
- 14:12 Kam's live rows read straight from the table with the WEDNESDAY seat key (`written_by` = `easyauth:*`, role=kam): **5 rows** — WED 3, ALL 1, Datasec 1. Three (02:07Z) are the Phase-2 LOCAL-MATRIX synthetic rows (`kam-local-020736`, `kam-local-both-020736`, `kam-local-tue-020736` — the last is `view=tuesday` → Datasec, counted, NOT decrypted). Kam's REAL words are the two 02:48Z rows (quoted in the BLUF section). Negative arm in the same read: the tuesday seat key raised `KeyError` on both WED rows. **Slip (harness label, not a defect):** my one-off printout labelled the ALL row "FAIL: tuesday key decrypted a WED row" — an ALL row is wrapped to BOTH seats by design (it is Kam's broadcast), so that line was a wrong label on a correct result.
- 14:13 `app/main.py` (backup `main.py.pre-0921-1412-phase3`): `validate_envelope` accepts `wrapped_keys` (≤8 × {kid 16-hex, wrapped_key b64 ≤1024}) → stored as a JSON string column, parsed on read in `_query`; **`POST /api/kam/messages` REFUSES 400 a reply not wrapped to the addressed seat kid(s)** (the server knows only PUBLIC keys; this is the one thing it checks with them); new `GET /api/pubkeys` = ring (pilot first) + seat public keys + `seat_of_client`; `/api/pubkey` kept; health reports `phase 3, kam_keys, seat_keys`.
- 14:14 `app/static/common.js` (backup `.pre-0921-1414-phase3`): kid of the imported private key computed in the page (SPKI DER rebuilt from the key's n/e via a throw-away extractable import; the kept CryptoKey stays non-extractable) and stored beside an imported key (IndexedDB `kam-kid`); `decryptRow` selects the `wrapped_keys` entry by kid, trial-fallback for a pre-Phase-3 import (remembers the kid); `encryptText` wraps to the ring + the addressed seat(s) from `/api/pubkeys`, top-level pair = pilot entry; folder read tries the configured filename then `kam-pilot/laptop/ipad-private.pem`. `index.html` / `chat.html` (backups `.pre-0921-1414-phase3`): key bar names the device key ("key: unlocked — laptop key …"), Safari note names `kam-ipad-private.pem`, ring pre-loaded at boot. `node --check` on the module and both page scripts: rc 0.
- 14:15 Seat writers → full recipient set: `seat/seat_common.py` (`build` → `envelope.encrypt_record`; `--pubkey` now optional = single-key compat), `seat/backfill.py`, and the dual-write helper `tools/_live_board.sh` (backup `.pre-0921-1415-phase3`; `bash -n` rc 0; not running per pgrep). `post_message.py --dry-run` body: kids `[pilot, ipad, laptop, wednesday-seat]`, top-level pair == first entry.
- 14:16 **`scripts/09_webcrypto_phase3.mjs`** — the page's OWN `common.js` in Node 24 WebCrypto (not a browser): **29/29 PASS** (`09_webcrypto_phase3.out`): page-computed kid == seat kid for pilot/laptop/ipad; the migrated live row `…_live-wed-010022` decrypts with EACH device key kid-selected; legacy-import trial fallback; outsider key refused both ways; AAD relabel refused; page-made replies for view=wednesday/tuesday/both carry exactly ring+seat kids and decrypt in `envelope.py` with the addressed seat key(s) + Kam's keys, the OTHER seat key refused (KeyError); static: still one body-sending fetch.
- 14:17 **DEPLOYED** (`scripts/04_deploy.sh`, backup `.pre-0921-1415-phase3`, only change: zip excludes `*.pre-*`; output `04_deploy_phase3.out`): tenant assertion PASS; zip guard 0 private markers / controls 1,1; Oryx build OK; Easy Auth v2 re-applied (require=true, excluded `/api/seat/*`); `/api/seat/health` → **`phase 3, kam_keys 3, seat_keys [tuesday, wednesday]` at 04:17:44Z**. No new resources.
- 14:21 **LIVE PROBE MATRIX** `scripts/05_probe_live.sh` (backup `.pre-0921-1419-phase3`; section H added, H6 then tightened to `--since 02:00Z`): first full run **67 PASS / 0 FAIL — ALL PROBES PASS** (`05_probe_live_phase3.out`). Post-migration writers verified by metadata: every row written since 04:10Z (6 messages, 1 card) carries 4 kids — no old-envelope writer is active.
- 14:24 `seat/get_kam_messages.py --decrypt` (backup `.pre-0921-1419-phase3`): opens rows with `<seat>-seat.pem`, `--json` adds `text`/`decrypt_error`/`ts_local`; **warns when a partition returns exactly `--limit` rows** (the API caps PER PARTITION oldest-first — a 14-day/400 read silently lost Kam's 02:48Z rows in my first `kam_msgs.sh` arm; fixed by a 3-day window + 1000 cap + the warning).
- 14:25 **(c) readers** — `tools/_kam_live.sh` (new, sourced): live rows as `$WED_AGENT`, refuses an unset/unknown seat (rc 2), fails LOUDLY (rc 2) on venv/cert/HTTP — never a quiet empty list. `tools/kam_msgs.sh` (backup `.pre-0921-1424-phase3`): `--source live` (DEFAULT) / `local` / `both` (union, de-dup on UTC-minute+text, `[live]`/`[local]` tags); the view warning now says a `both` row is a BROADCAST (addressed to both seats) instead of "not addressed to Wednesday". `tools/kam_rulings_today.sh` (backup same tag): same `--source`, seat filter + fail-open unchanged, live FRESHNESS line ("the board itself, not a copy"), the stale-copy warning scoped to the local file. `tools/reconcile_rulings.py` (backup same tag): `RECONCILE_SOURCE=live|local|both` (default `both`; `local` forced when `RECONCILE_CHAT` points at a fixture) — live taps + local taps, newest per card wins; live failure = REFUSED rc≠0. Arms run: all sources × both tools, no-seat refusal, tuesday-seat R0 (2 rows, text withheld), `tests/reconcile_rulings_arms.sh` **23 PASS / 0 FAIL**.
- 14:28 **(c) poller** `fleet/cockpit/live_chat_poll.sh` (new; NOT wired): 30 s loop, `get_kam_messages.py --since <row_key watermark>` (ciphertext suffices to know THAT/WHEN/WHICH TAB), live-typed rows only (`written_by easyauth:*`), one tap per tick via `tap_wednesday.sh`, watermark `state/live_chat_polled_through` advance-only and ONLY after tap rc 0; first run initialises to the newest row and wakes for nothing; `--once`, `--dry-run`, `LIVE_POLL_STATE`/`LIVE_POLL_TAP` for arms. Arms (scratch state, fake tap): initialise-no-wake ✓ · watermark before 02:48Z → "would tap 2" ✓ · fake tap rc 0 → watermark advances ✓ · re-tick → 0 new ✓ · fake tap rc 3 (guard) → watermark unchanged ✓ · bad seat refused ✓. **Two slips caught by the arms:** (i) the first version's inline python had an f-string escape SyntaxError and the tick still returned rc 0 and "initialised" an empty watermark — fixed (JSON via env, an empty parse = failed tick, watermark untouched); (ii) in a PATH-restriction arm I left `LIVE_POLL_TAP` unset, so the REAL `tap_wednesday.sh` delivered ONE tap into Wednesday's pane at 14:28:45 ("[live-board] 2 new message(s) from Kam … 12:48 …") — true content, unintended delivery; `fleet/cockpit/logs/live_chat_poll.log` and `tap_wednesday.log` show it.
- 14:30 **`scripts/08c_local_matrix_phase3.sh`** (loopback :47791, simulated Easy Auth principal = Kam, REAL store): `/api/pubkeys` as Kam → 3 Kam public + 2 seat public keys, no private material; a page-module reply NOT wrapped to the wednesday seat → **400** (server guard); malformed `wrapped_keys` → 400; wrapped to ring+seat → 201; view=both → ALL 201; wednesday seat reads both back `--decrypt` == the text; refused replies NOT stored; tuesday seat does NOT receive the WED row (R0) but decrypts the ALL row; raw WED reply row opens with pilot/laptop/ipad/wednesday-seat, tuesday-seat KeyError. **ALL PASS** (`08c_local_matrix_phase3.out`). Two synthetic Kam rows added by this matrix (`p3l-good-042952` WED, `p3l-both-042952` ALL).
- 14:31 ADDENDUM 2 from Wednesday (Kam's 12:48 replies): (1) un-stick the Updates panel, render it at the BOTTOM below Needs-you (live page only); (2) mark the synthetic rows (`synthetic=true`, never delete) and filter them from both live pages; prove both.
- 14:35 Synthetic rows (addendum 2): `app/main.py` accepts the clear flag `synthetic=true`; `post_message.py`/`post_card.py --synthetic` (probe rows are now BORN marked; `05_probe_live.sh` passes it); `seat/mark_synthetic.py` dry-run then run: **51 messages + 14 cards marked** (see table below), 4 Datasec messages + 4 Datasec cards left alone (real, Tuesday's; text never read); re-run: 0 to mark. Pages: `common.js` `isSynthetic`/`hidden`, both pages skip such rows at ingestion (`sinceM` still advances), the cockpit footer shows "N synthetic hidden". Nothing deleted.
- 14:35 Updates un-stuck (addendum 2): live `index.html` — the pinned `#needscroll` region is gone; `#needs` then `#feed` inside ONE `#feedscroll`, Updates rendered BELOW the Needs-you cards. Local `cockpit.html` untouched (asserted by the check). `scripts/09b_page_checks_phase3.mjs`: **7/7 PASS** (DOM order, local page still pinned, CSS rule gone, render order, synthetic filter on the pages' own ingestion statements for messages/cards/chat).
- 14:36 **REDEPLOYED** (`04_deploy_phase3b.out`): guard 0/1/1, build OK, site started, health `phase 3` at 04:35:53Z.
- 14:37 **FINAL LIVE PROBE MATRIX: 70 PASS / 0 FAIL — ALL PROBES PASS** (`scripts/05_probe_live_phase3_final.out`, verbatim section H below). Secret scan (`07_secret_scan.sh`, extended to the two device keys): **CLEAN** (9 needles, control ≥1 each); tools/ and fleet/cockpit/ scanned for the armour line + 5 key slices: 0 hits; `git ls-files` key files: 0.
- 14:40 Final migration consistency check found **1 Datasec row written at 04:09:53Z by the TUESDAY seat (Phase-2 writer, pilot-only)** — re-wrapped (bytes only); store now 100 % complete again (messages 2991: ALL 2 / Datasec 21 / Secuura 737 / WED 2231; cards 234). → "For Tuesday" + "For Wednesday".
- 14:42 README.md + PORTABILITY.md updated for Phase 3.

## BLUF
**Done and proven live (70/70 probes, scan CLEAN, nothing committed):** (a) every row on the live board is now wrapped to Kam's whole key ring AND to the addressed seat's certificate key (D-2(b)); the Wednesday seat reads and decrypts Kam's live replies through the API (`tools/kam_msgs.sh` — default source is now the live board). (b) `kam-laptop` and `kam-ipad` RSA-4096 keys exist on this drive (paths in ACTIONS); the migration re-wrapped all 2974 messages + 232 cards (0 failed, idempotent, sample-verified with every key, pilot still works). (c) the three readers (`kam_msgs.sh`, `kam_rulings_today.sh`, `reconcile_rulings.py`) read the live board (local/both remain); the live poller exists with arms and is NOT wired into `wake_watch.sh`. Plus Kam's two 12:48 asks: Updates renders below Needs-you (un-stuck), and 51 messages + 14 cards of synthetic probe rows are flagged and hidden (not deleted). Local server and dual-write untouched.
**Kam's live words (WED partition, 2 real rows; the other 02:07Z rows are Phase-2 synthetic):**
- 02:48:18Z (12:48:18 AEST, view=wednesday): "Fantastic, this looks great now. For the updates, please remove the updates stickingness so that it just goes at the bottom of the fleet activity that needs me. Also, I can see there's a lot of secure synthetic cards. Do you need me to action these or are these tests only?"
- 02:48:32Z (12:48:32 AEST, view=wednesday): "Lastly, can you please confirm that Tuesday is posting to this new board? Reading from it."
**Answer material for Wednesday's receipt:** the synthetic cards were tests only (now hidden); Tuesday IS posting to the board (her seat wrote a Datasec row at 14:09:53 AEST today, dual-write id `bf-7101…`) but with the Phase-2 writer, so her rows are pilot-only until she pulls Phase 3 (re-wrap covers them meanwhile); whether she READS from it is not visible to me (no read log) — her `get_kam_messages.py` needs her Phase-3 copy.
**What only a browser can still prove:** the folder picker / one-click unlock (Chrome), the Safari/iPad Import-once, the key bar naming the device key, and the un-stuck Updates rendering — I connected no browser (rule); the page code was executed in Node WebCrypto on its own module.

## Piece (a) — multi-recipient envelope. FOUND / TESTED / HOW
- FOUND: Phase 2 wrapped to the pilot key only; a seat could not read Kam's live replies; `wrapped_key`/`kid` single pair; browser `decryptRow` used the top-level pair.
- BUILT: `seat/envelope.py` (`recipients_for`, `encrypt_record`, kid-selected `unwrap_data_key`/`decrypt_text`, `rewrap`), `app/main.py` (`wrapped_keys` validated + stored as JSON, parsed on read; `/api/pubkeys`; **Kam's reply route refuses 400 unless wrapped to the addressed seat kid(s)**), `app/static/common.js` (kid at import, kid-selected decrypt + trial fallback, reply wrapping to ring + seat(s) from `/api/pubkeys`, device filenames), `seat/get_kam_messages.py --decrypt`, `seat/seat_common.py`/`backfill.py`/`tools/_live_board.sh` writers → full recipient set. Shape: `wrapped_keys:[{kid,wrapped_key}…]` + top-level `kid`/`wrapped_key` kept (= pilot entry) for one release; scheme string unchanged. Browser selects by kid; a pre-Phase-3 imported key finds its entry by trial once and remembers the kid.
- TESTED: `envelope.py` self-test PASS · `09_webcrypto_phase3.mjs` 29/29 (page kid == seat kid ×3; migrated row with each device key; outsider refused; replies for wednesday/tuesday/both open with the addressed seat key(s) and the other seat is refused) · `08c_local_matrix_phase3.sh` ALL PASS (guard 400 / malformed 400 / 201 / seats read back / R0 / offline negative) · live H3/H4/H6 (below).
- HOW: `2_Project_Files/dashboard-cloud/.venv/bin/python seat/envelope.py` · `node scripts/09_webcrypto_phase3.mjs <row.json> <pubkeys.json> "<expected>"` · `bash scripts/08c_local_matrix_phase3.sh` · `bash scripts/05_probe_live.sh`.

## Piece (b) — device keys + migration. FOUND / TESTED / HOW
- Keys (`scripts/01c_device_keys.sh`, idempotent): `4_Credentials/dashboard-cloud/kam-laptop-private.pem` (kid `2ccbe41a20d93001`), `kam-ipad-private.pem` (kid `c6d1765a828b469e`), both RSA-4096 PKCS8 mode 600; public halves in `app/keys/`; seat public keys `wednesday-seat-public.pub` (kid `8e844615d15e931e`) / `tuesday-seat-public.pub` (`8ad86866fc0d5680`). Pilot kid `ed9ec4e1156c5982` unchanged.
- Migration `seat/migrate_rewrap.py` — counts (BEFORE → AFTER, complete = carries every required kid):
  | table / partition | rows before | complete before | rewrapped (run 1) | failed | complete after | run 2 (idempotency) |
  |---|---|---|---|---|---|---|
  | messages / ALL | 1 | 0 | 1 | 0 | 1 | already complete |
  | messages / Datasec | 16 | 0 | 16 (data-key bytes only, text untouched) | 0 | 16 | already complete |
  | messages / Secuura | 735 | 0 | 735 | 0 | 735 | already complete |
  | messages / WED | 2222 | 0 | 2222 | 0 | 2222 | already complete |
  | cards / Datasec | 4 | 0 | 4 (bytes only) | 0 | 4 | already complete |
  | cards / Secuura | 195 | 0 | 195 | 0 | 195 | already complete |
  | cards / WED | 33 | 0 | 33 | 0 | 33 | already complete |
  | **totals** | **2974 msgs / 232 cards** | 0 | **2974 / 232** | **0** | **2974 / 232** | **0 processed** |
  Later today: +1 Datasec message (Tuesday's Phase-2 writer, 04:09:53Z) re-wrapped at 14:40; store at hand-over 2991 msgs / 234 cards, 100 % complete.
- Sample-decrypt table (run 1, 3 random migrated rows per partition × every key; `ok` = the key opens the row, `n/a` = not a recipient, refused):
  | row_key | pilot | laptop | ipad | wednesday-seat | tuesday-seat |
  |---|---|---|---|---|---|
  | ALL/2026-09-21T02:07:40.515Z_kam-local-both-0207 | ok | ok | ok | ok | ok |
  | Datasec/…01:00:30.206Z_live-delta-010022 (bytes only) | ok | ok | ok | n/a | ok |
  | Datasec/…00:59:55.401Z_live-delta-005947 (bytes only) | ok | ok | ok | n/a | ok |
  | Datasec/…00:37:11.095Z_local-delta (bytes only) | ok | ok | ok | n/a | ok |
  | Secuura/2026-09-16T05:06:11.897Z_bf-2e4ca7422c8e7d7a | ok | ok | ok | ok | n/a |
  | Secuura/2026-09-09T23:08:07.556Z_bf-871410fbc05a75fd | ok | ok | ok | ok | n/a |
  | Secuura/2026-09-17T08:31:26.561Z_bf-967a9b0116bcf6d9 | ok | ok | ok | ok | n/a |
  | WED/2026-09-01T10:39:09.486Z_bf-f8a9688a74bff6bc | ok | ok | ok | ok | n/a |
  | WED/2026-09-06T20:02:05.658Z_bf-80700a420a938351 | ok | ok | ok | ok | n/a |
  | WED/2026-09-08T04:10:33.103Z_bf-3c2841362266c927 | ok | ok | ok | ok | n/a |
  | cards: Datasec ×3 (bytes only) / Secuura ×3 / WED ×3 | ok | ok | ok | per partition | per partition |
  (full table in `scripts/migrate_run1.out`; the 14:40 late row `Datasec/…04:09:52.396Z_bf-7101…`: ok ok ok n/a ok.)
- HOW: `AZURE_CONFIG_DIR=… .venv/bin/python seat/migrate_rewrap.py --dry-run` → `… --sample 3` → `…` (re-run = 0).

## Piece (c) — cut-over readers + poller. FOUND / TESTED / HOW
- `tools/kam_msgs.sh [n] [--brief] [--source live|local|both]` — default **live**. `tools/kam_rulings_today.sh [DAY] [--source …]` — default **live**; freshness line for the live board; stale-copy warning only for the local file. `tools/reconcile_rulings.py` — `RECONCILE_SOURCE` default **both** (local file + live), fixtures force local. All three keep their headers, guards (view discipline, fail-open, seat scope, note taps, unknown-card refusal) and exit codes; a live failure is loud (rc 2 / REFUSED), never a quiet empty result. Shared helper `tools/_kam_live.sh`.
- `fleet/cockpit/live_chat_poll.sh` — written + armed (6 arms), NOT wired. **The one-line change `wake_watch.sh`/`arm_wake_watch.sh` needs** (in the runner, once Wednesday claims it): `pgrep -f "cockpit/live_chat_poll.sh" >/dev/null || nohup bash "$HERE/live_chat_poll.sh" >> "$HERE/logs/live_chat_poll.log" 2>&1 &`. Nothing else in `wake_watch.sh` changes: its local `chat_log.json` leg keeps covering local-board replies; the poller covers live-board replies with its own watermark (`state/live_chat_polled_through`), so the two cannot double-wake the same row (different sources, different keys).
- TESTED: arms in the log above; `tests/reconcile_rulings_arms.sh` 23/23; live H6 (both seats via the API).

## Live probe matrix — FINAL run 14:37, section H verbatim (A–G unchanged from Phase 2, all PASS)
```
### H. Phase 3 (2026-09-21) — per-seat wrapped keys, device keys, migrated rows, live readers
PASS  H1 health phase 3: expected 200 got 200
PASS  H1 health: phase 3, kam_keys 3, seat_keys [tuesday, wednesday]
PASS  H2 GET /api/pubkeys plain client (viewer route, Easy Auth gated): 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
PASS  H3 wednesday-seat -> WED (Phase 3 writer): expected 201 got 201
      raw row kids: ['ed9ec4e1156c5982', 'c6d1765a828b469e', '2ccbe41a20d93001', '8e844615d15e931e']
PASS  H3 raw row wrapped_keys kids == recipients_for(WED) (pilot, ipad, laptop, wednesday-seat)
PASS  H3 kam-pilot-private.pem decrypts the new WED row == expected
PASS  H3 kam-laptop-private.pem decrypts the new WED row == expected
PASS  H3 kam-ipad-private.pem decrypts the new WED row == expected
PASS  H3 wednesday-seat.pem decrypts the new WED row == expected
PASS  H3 tuesday-seat.pem REFUSED on the WED row (KeyError: not a recipient)
PASS  H4 tuesday-seat -> Datasec (Phase 3 writer): expected 201 got 201
PASS  H4 Datasec row kids == recipients_for(Datasec) (pilot, ipad, laptop, tuesday-seat)
PASS  H4 kam-laptop-private.pem unwraps the Datasec row's DATA KEY (bytes only, text untouched)
PASS  H4 kam-ipad-private.pem unwraps the Datasec row's DATA KEY (bytes only, text untouched)
PASS  H4 tuesday-seat.pem unwraps the Datasec row's DATA KEY (bytes only, text untouched)
PASS  H4 wednesday-seat.pem REFUSED on the Datasec row (KeyError: not a recipient)
PASS  H5 kam-laptop-private.pem decrypts the MIGRATED row == the pilot's decrypt (279 chars, not printed)
PASS  H5 kam-ipad-private.pem decrypts the MIGRATED row == the pilot's decrypt (279 chars, not printed)
PASS  H5 wednesday-seat.pem decrypts the MIGRATED row == the pilot's decrypt (279 chars, not printed)
PASS  H5 pilot key still decrypts the migrated row
PASS  H6 wednesday seat get_kam_messages --decrypt --json rc: expected 0 got 0
      partitions: ['ALL', 'Secuura', 'WED'] kam rows: 6 live (easyauth) rows: 6 decrypted: 6 errors: 0 foreign: 0
PASS  H6 wednesday seat decrypts EVERY live Kam row in its partitions (WED+ALL, 6 rows since 02:00Z, >=4 known); 0 foreign rows
      partitions: ['ALL', 'Datasec'] kam rows: 3 live rows: 3 decrypted: 3 foreign: 0 (Datasec text NOT printed, NOT written to disk)
PASS  H6 tuesday seat sees only ALL+Datasec and decrypts its live Kam rows; no WED row reaches it (R0)
PASS  H7 wednesday seat GET WED rows today: expected 200 got 200
      WED rows today: 44 synthetic=true among them: 23 this run's own probe rows found marked: ['probe-dup-043617', 'live-wed-043617', 'p3-wed-043617']
PASS  H7 this run's 3 synthetic WED rows are PRESENT in the seat API and carry synthetic=true (the pages hide them; nothing deleted)
PASS  H7 page checks (DOM order Updates-below-Needs-you; synthetic filter in the pages' own ingestion code): expected 0 got 0
      09b PASS lines: 7
### F. Rows per partition (counts only)
      messages/Secuura: 737 (synthetic, hidden by the pages: 14)
      messages/Datasec: 21 (synthetic, hidden by the pages: 17)
      messages/WED: 2231 (synthetic, hidden by the pages: 24)
      messages/ALL: 2 (synthetic, hidden by the pages: 2)
      cards total: 234 (synthetic, hidden: 15)
### RESULT: ALL PROBES PASS          (70 PASS / 0 FAIL)
```
Secret scan line: `== RESULT: CLEAN` (armour line, Easy Auth secret, 48-char body slices of pilot + laptop + ipad + both seat keys, connection-string marker, credential-reset password key — each 0 files with a positive control ≥ 1).

## Synthetic rows hidden (marked `synthetic=true`, never deleted; counts at hand-over)
| partition | messages hidden | cards hidden | classified by |
|---|---|---|---|
| WED | 24 | 3 | id pattern 22 + text prefix 2 (wednesday-seat decrypt); cards: id 2 + title 1 |
| Secuura | 14 | 11 | id pattern (`local-alpha`, `live-alpha-*`, `live-card-*` …) |
| Datasec | 17 | 0 | **id pattern ONLY** (text never read); 4 messages + 4 cards left alone as real |
| ALL | 2 | — | id pattern (`kam-local-both-*`, `p3l-both-*`) |
Every probe row written from now on is born marked (`--synthetic`), including this afternoon's.

## ACTIONS FOR KAM (action first)
**(1) Laptop — one import step.** Copy `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud/kam-laptop-private.pem` to a folder on the laptop by a channel you trust (AirDrop / Finder — never mail, never the repo). Open `https://wednesday-dashboard-e42e.azurewebsites.net/` (MFA sign-in), key bar → **Choose the folder that holds the key…** → pick that folder. The page finds `kam-laptop-private.pem` by itself (it tries the configured name, then the pilot/laptop/ipad names) and shows **"key: unlocked — laptop key from folder …"**. Chrome/Edge only; on Safari use **Import key…** with the same file.
**(2) iPad (Safari) — import once.** Copy `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud/kam-ipad-private.pem` to the iPad (AirDrop → Files). Open the site in Safari, sign in, key bar → **Import key…** → pick the file. Safari has no folder access, so the key is imported once into that browser's storage (non-extractable) — **Forget key** removes it. The bar shows **"key: unlocked — ipad key (imported copy in this browser)"**. Tap **auto-play replies** once if you want them spoken.
**(3) The pilot key still works everywhere** — every row (old and new) carries all three of your kids; the Studio's Chrome keeps its remembered folder. Nothing to redo there.
**(4) Your two 12:48 asks are done on the live site:** Updates now sits at the bottom under Needs-you (no pin); the synthetic test rows are hidden (they were tests only — nothing for you to action). The Tuesday question is answered in the BLUF.
**(5) Nothing was deleted, nothing committed.** Wednesday reviews the diff and commits.

## For Tuesday (her wiring — the exact shape; no mail sent by me)
1. Pull the Phase 3 tree: `dashboard-cloud/seat/envelope.py`, `seat_common.py`, `get_kam_messages.py`, `app/keys/*.pub` (public; the ring + both seat public keys), `tools/_live_board.sh`, `tools/_kam_live.sh`, `tools/kam_msgs.sh`, `tools/kam_rulings_today.sh`, `tools/reconcile_rulings.py`, `fleet/cockpit/live_chat_poll.sh`. **Until she does, every row her seat posts is pilot-only** (measured: her 04:09:53Z Datasec row) — unreadable on the laptop/iPad and by her own seat; Wednesday's idempotent `migrate_rewrap.py` fixes them after the fact.
2. Her keys: `4_Credentials/dashboard-cloud/tuesday-seat.pem` + `.crt` on the mini (the copy still parked on this drive is Phase 1 ACTION (d)). `WED_AGENT=tuesday`. Her `--decrypt` opens Datasec rows and Kam's `view=tuesday` / `both` replies (`recipients_for(Datasec)` = ring + tuesday-seat; ALL = both seats). She never sees WED/Secuura rows (token partitions).
3. Commands: `.venv/bin/python seat/get_kam_messages.py --seat tuesday --decrypt` · `WED_AGENT=tuesday tools/kam_msgs.sh` · `WED_AGENT=tuesday tools/kam_rulings_today.sh` · `WED_AGENT=tuesday RECONCILE_SOURCE=both tools/reconcile_rulings.py` · poller `WED_AGENT=tuesday fleet/cockpit/live_chat_poll.sh` (her own watermark on the mini; the tap helper there is hers — `LIVE_POLL_TAP` if it is not `tap_wednesday.sh`). The chat_push mail-to-Tuesday leg is NOT needed for live rows: her poller sees `view=tuesday` (Datasec) and `both` (ALL) rows directly.
4. Her backfill arm (Phase 2 D-1) is unchanged and still hers; `backfill.py` now writes the full recipient set.

## For Wednesday (wrap duties, not done by the builder by rule)
- Review + commit (scan CLEAN; the `.pre-0921-*-phase3` backups are beside each edited file; `scripts/*.out` are gitignored). Receipt Kam's two 12:48 rows.
- `doctor.sh` items per rule 3a: `dashboard-cloud/.venv` + `4_Credentials/dashboard-cloud/{kam-laptop,kam-ipad}-private.pem` + `wednesday-seat.pem` present (the live readers depend on the seat key now); optional: `migrate_rewrap.py --dry-run` = 0 to rewrap (catches Phase-2-era writers).
- Claim `arm_wake_watch.sh` for the one-line poller spawn (above), then arm it; until then live-board replies wake nobody — `kam_msgs.sh` (live default) is the manual read.
- Re-run `seat/migrate_rewrap.py` after Tuesday's posts until she pulls Phase 3.
- The accidental real tap at 14:28:45 into the Wednesday pane (slip ii) — read and dismiss.

## NOT done (stated)
- No browser session: folder picker / one-click unlock / Safari import / key-bar wording / Updates position are proven on the page's own code in Node (WebCrypto + DOM-order checks), not rendered. Kam's device imports are the test.
- The poller is not armed (by brief); `wake_watch.sh` untouched.
- Tuesday's seat still posts pilot-only rows until she pulls Phase 3 (her side).
- The local server and dual-write are untouched (by brief); the local `chat_log.json` legs of `wake_watch.sh`/`chat_push.sh` still exist for local-board replies.
- Attachments, fleet mail, usage tiles: unchanged from Phase 2 (not on the live site).
- `chat.html` (the chat mirror) has no Updates panel, so item (1) touched `index.html` only.

## Slips (mine) — consolidated
1. One `cd /tmp` in a tool call (refused by the hook; re-issued). 2. Three tool calls with `rm -f` on non-literal paths (refused; rewritten to avoid temp files / pipe instead). 3. The one-off "FAIL: tuesday key decrypted a WED row" label on an ALL row (wrong label, correct behaviour). 4. `kam_msgs.sh` first arm used a 14-day/400 read that silently cut Kam's newest rows — found by the arm, fixed with a narrow window, max cap and a loud truncation warning in `get_kam_messages.py`. 5. `view=both` was labelled "not addressed to Wednesday" — fixed to BROADCAST. 6. Poller v1: f-string SyntaxError made a parse failure look like "nothing new" (rc 0) — fixed, an empty parse is now a failed tick. 7. Poller arm 6 left `LIVE_POLL_TAP` unset → ONE real tap delivered into Wednesday's pane at 14:28:45. 8. `09b` first pointed at a wrong local cockpit path (ENOENT; corrected to `2_Project_Files/dashboard/cockpit.html`).
