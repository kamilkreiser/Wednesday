# dashboard-cloud — Wednesday's external dashboard (Phase 1 pilot 2026-09-21 → Phase 2 → Phase 3, all the same day)

**Live:** `https://wednesday-dashboard-e42e.azurewebsites.net/` (cockpit) and `/chat` — sign-in restricted to `kreiser.org@me.com`. **Phase 2: REAL rows** (the local chat streams + decision cards, encrypted at write; Wednesday's tools dual-write). The local board remains the record until Kam rules the cut-over.
**Phase 3 (Kam 12:50 "switch to using the live version only" + laptop/iPad keys; report `REPORT_2026-09-21_phase3.md`):** every record's data key is wrapped to Kam's whole KEY RING (`app/keys/kam-*-public.pub`: pilot, laptop, ipad) AND to the ADDRESSED SEAT's certificate public key (`app/keys/<seat>-seat-public.pub`; WED/Secuura → wednesday, Datasec → tuesday, ALL → both) — `wrapped_keys: [{kid, wrapped_key}…]`, top-level pair kept (= pilot). So any of Kam's devices reads any row, and a seat reads what Kam typed to its tab (`seat/get_kam_messages.py --decrypt`). Kam's reply route REFUSES (400) a reply not wrapped to the addressed seat. Probe/test rows carry `synthetic=true` and are hidden by the pages (never deleted). The seat-side readers (`tools/kam_msgs.sh`, `kam_rulings_today.sh`, `reconcile_rulings.py`) default to the LIVE board (`--source local|both` remain); `fleet/cockpit/live_chat_poll.sh` is the live twin of the chat wake (not yet armed). Migration `seat/migrate_rewrap.py` (idempotent) re-wrapped every existing row; re-run it after any Phase-2-era writer posts (Tuesday's seat until she pulls Phase 3).

**Study it implements:** `1_Project_Definition/Architecture/2026-09-21_external-dashboard-requirements.md` (Option A + the §4 envelope from the first record). **Build reports:** `REPORT_2026-09-21_pilot.md` (Phase 1), `REPORT_2026-09-21_phase2.md` (Phase 2: mirror layout, key folder, dual-write + backfill, cut-over notes).

## Architecture as built (Phase 2)
```
Kam's browser ──MFA (Entra, Easy Auth)──► App Service B1 Linux (FastAPI, gunicorn/uvicorn)
   │ decrypts client-side (WebCrypto);      │  GET /  GET /chat  GET /static/common.js   the local cockpit.html / chat.html layouts
   │ private key READ FROM A FOLDER HE      │  GET /api/messages?client=&since=  GET /api/cards?client=   delta / whole reads
   │ CHOSE ONCE (Chrome/Edge, File System   │  GET /api/me (+is_kam), GET /api/pubkey
   │ Access API) or imported once (Safari/  │  POST /api/kam/messages   Kam's reply, ENCRYPTED IN THE BROWSER to his own public key;
   │ iOS/Firefox); never sent anywhere      │       principal must be KAM_OBJECT_ID; view -> partition (wednesday->WED, tuesday->Datasec, both->ALL)
                                             │
wednesday-seat / tuesday-seat ──cert──► Entra ► JWT (roles) ──► POST /api/seat/messages|cards   GET /api/seat/messages?since=&author=kam
   (MSAL client-credentials, certificate)   │  Easy Auth EXCLUDES /api/seat/*; the app validates issuer/audience/signature (JWKS)
   tools/chat_reply.sh + decision_queue.sh  │  partition = token's Client.* roles; body naming another client -> 403; ALL readable by every seat, writable by Kam only
   dual-write via tools/_live_board.sh      │  messages: INSERT, repeat (client,ts,id) -> 200 duplicate (nothing written)
   seat/backfill.py copies the history      │  cards: RowKey card_<id> = STATE, repeat id -> 200 updated in place
                                             ▼
                              Table storage `wedndashtkhrqh` (managed identity, shared key DISABLED)
                              tables messages / cards; PartitionKey=client (Secuura|Datasec|WED|ALL); RowKey=<UTC ts>_<id> | card_<id>
                              rows hold ciphertext + clear routing fields only — no prose column exists
```
Tenant `d500ebad-cf53-4f2a-a501-f831289e67fc`, subscription `0c57ab37-349c-47ae-a10f-e284a380bbb9`, resource group **`wednesday-dashboard-rg`** (australiaeast) — the ONLY RG this code touches. Cost unchanged from Phase 1 (B1 ≈ USD 13.9/month + cents of Table storage).

## Identifiers (non-secret; also in `scripts/ids.conf`)
| Object | id |
|---|---|
| Entra app `wednesday-dashboard-web` (Easy Auth RP) | appId `c8ba2d4a-e863-438f-b5b6-88fcca491961`, SP `ba1d3b99-9446-47d6-b6c5-be6bc954d049`, user assignment required, Kam only |
| Kam's user object (the only principal allowed on `POST /api/kam/*`, app setting `KAM_OBJECT_ID`) | `c38fcea6-ff23-40c3-a875-e84e324910cf` |
| Entra app `wednesday-seat-api` (audience, app roles Seat.Write/Seat.Read/Client.Secuura/Client.Datasec/Client.WED, v2 tokens) | appId `68b210e3-3fd8-45c3-964d-2d596b4a8966` |
| Entra app `wednesday-seat` (roles Seat.Write, Seat.Read, Client.Secuura, Client.WED; certificate) | appId `a9edf1d0-6136-437a-81fa-2b9c313fba08` |
| Entra app `tuesday-seat` (roles Seat.Write, Seat.Read, Client.Datasec; certificate) | appId `7e96ab2d-fad2-4ff3-b28b-f9b3aadbc9f3` |
| App Service plan / web app | `wednesday-dashboard-plan` (B1) / `wednesday-dashboard-e42e` (MI `305da448-befb-4445-b827-6ff5bd49fa82`) |
| Storage account | `wedndashtkhrqh` |

## Envelope (scheme `rsa-oaep-sha256+aes-256-gcm/v1` + Phase 3 `wrapped_keys`, `seat/envelope.py` ⇄ `app/static/common.js`)
Per record: 32-byte data key → AES-256-GCM (12-byte IV) over UTF-8 text, **AAD = `client|kind|id|ts`**; data key wrapped RSA-OAEP(SHA-256) to Kam's public key (`app/keys/kam-pilot-public.pub`, kid = sha256(SPKI)[:16]). Both the seats (Python) and Kam's browser (WebCrypto, for his own replies) encrypt; only Kam's private key decrypts. Clear on purpose (study §4.4): `client, view, ts, kind, id, role, seat, backfill, src_ts`; cards also `status, option_keys (slugs ≤32), recommended, ruled, ruled_choice, ruled_ts, client_project`. Cards encrypt a JSON of `{title, bluf, default_action, options[{key,label,detail}], ruling_note, withdrawn_reason, delivered_artefact, local_id}`.

## The key-folder flow (Kam, 2026-09-21 11:45 — "check for it in a specific local drive; let the user define where")
- **Chrome / Edge:** key bar → *Choose the folder that holds the key…* → pick the folder ONCE. The directory handle is remembered in that browser's IndexedDB. On every visit the page asks the folder for read permission — **one click on *Unlock key*** (none, if Chrome was told "allow on every visit") — reads the file named in the *file* box (default `kam-pilot-private.pem`, per browser), imports it as a **non-extractable** WebCrypto key in memory, and decrypts. The PEM is never stored by the page and never leaves the machine (`common.js` has one request body, the envelope of Kam's reply; the server has no key route). *Forget key* drops the remembered folder.
- **Safari / iOS / Firefox** (no File System Access API): *Import key…* once; the non-extractable CryptoKey stays in that browser's IndexedDB. Same *Forget key*.
- The folder can be the drive's own `4_Credentials/dashboard-cloud/` on the Studio, or any folder Kam puts a copy of the key in on the laptop/phone (AirDrop/Files — never mail, never the repo).

## The dual-write (Phase 2, real rows)
`tools/chat_reply.sh` and `tools/decision_queue.sh` complete their LOCAL write exactly as before, then source `tools/_live_board.sh` and post the same record to the live board (message: same text, `ts` = the local entry's ts in UTC, `src_ts` = the original string, deterministic `id` = `bf-`sha256(stream|ts|text)[:20]; card: the card's current state via `seat/post_card.py --from-store`). A failed post is **loud** (stderr + `2_Project_Files/fleet/state/live_board_post_failures.log`) and **never** changes the tool's exit code; `LIVE_BOARD=0` disables it. The seat is `$WED_AGENT` (tree-resolved); Wednesday refuses Datasec locally (and the API would 403). `seat/backfill.py` copied the history once (idempotent — re-runs post nothing new; counts in the Phase 2 report). Tuesday's rows (her stream, Kam's `view=tuesday` rows, Datasec legacy rows, Datasec cards) are hers to backfill with her own certificate.

## Layout
- `app/main.py` — the service. `app/static/index.html` (cockpit mirror), `app/static/chat.html` (chat mirror), `app/static/common.js` (key access + envelope + row mapping). `app/keys/kam-pilot-public.pub` — PUBLIC envelope key (tracked).
- `seat/envelope.py` (Phase 3: `recipients_for`, `encrypt_record`, kid-selected `decrypt_text`, `rewrap`), `seat/seat_common.py`, `seat/post_message.py` / `post_card.py` (`--from-store`, `--synthetic`), `seat/backfill.py`, `seat/get_kam_messages.py` (`--decrypt`, `--json`), `seat/migrate_rewrap.py` (Phase 3 re-wrap, idempotent, `--dry-run`, `--sample`), `seat/mark_synthetic.py` — the seat CLI (`--dry-run`, `--token-only`).
- `scripts/00`–`07` as in Phase 1 (`04_deploy.sh` now also sets `KAM_OBJECT_ID`; `05_probe_live.sh` gained sections G and H); `01c_device_keys.sh` (laptop/iPad keys + seat public keys), `08_local_matrix_phase2.sh`, `08b_webcrypto_roundtrip.mjs`, `08c_local_matrix_phase3.sh` (Kam's reply route with the seat-kid guard, loopback), `09_webcrypto_phase3.mjs` (kid selection / device keys / reply wrapping in the page's own module), `09b_page_checks_phase3.mjs` (Updates-below-Needs-you DOM order + synthetic filter), `price_check.py`.
- `requirements.txt` — pinned. `.venv/` is local and gitignored.

## Run the seat CLI (Wednesday's machine)
```
2_Project_Files/dashboard-cloud/.venv/bin/python 2_Project_Files/dashboard-cloud/seat/post_message.py --seat wednesday --client Secuura --view wednesday --text "…" [--dry-run]
2_Project_Files/dashboard-cloud/.venv/bin/python 2_Project_Files/dashboard-cloud/seat/post_card.py --seat wednesday --from-store 0_Brain/dashboard/data/decisions.json --card-id <id>
2_Project_Files/dashboard-cloud/.venv/bin/python 2_Project_Files/dashboard-cloud/seat/get_kam_messages.py --seat wednesday [--since ROWKEY]
2_Project_Files/dashboard-cloud/.venv/bin/python 2_Project_Files/dashboard-cloud/seat/backfill.py --dry-run
```
Needs `4_Credentials/dashboard-cloud/wednesday-seat.pem` + `.crt`. Tuesday's pair (`tuesday-seat.*`) is parked in the same folder for Kam to move to the mini — it is not distributed by this repo, and while it sits here this machine CAN act as Tuesday (Phase 2 report, piece C).

## Re-verify after any change
`bash scripts/05_probe_live.sh` — exit 0 only if every probe passes (Phase 3 final run: 70 PASS / 0 FAIL). `bash scripts/08c_local_matrix_phase3.sh` for Kam's reply route; `node scripts/09_webcrypto_phase3.mjs <raw row json> <pubkeys json> <expected text>` and `node scripts/09b_page_checks_phase3.mjs` for the page code. `bash scripts/08_local_matrix_phase2.sh` for the Kam write path (needs no MFA: loopback with a simulated principal header). Redeploy: `bash scripts/04_deploy.sh` (idempotent; zip guard refuses a private key in the zip).

## Not done (Kam's call / Phase 3)
Cut-over of the local board (the Phase 2 report, piece D, lists what remains); Tuesday's wiring on the mini; in-browser test of the folder picker; fleet-mail events / usage gauges / attachments / ack lines on the live site; custom domain `dash.kreiser.org`; sign-in/API logging + alerts; export/delete path; Conditional Access (Entra Premium suspended → Security Defaults only).
