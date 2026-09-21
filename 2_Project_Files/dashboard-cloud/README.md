# dashboard-cloud — Wednesday's external dashboard (Phase 1 pilot, 2026-09-21)

**Live:** `https://wednesday-dashboard-e42e.azurewebsites.net/` — sign-in restricted to `kreiser.org@me.com`. **Synthetic rows only** until Phase 2.
**Study it implements:** `1_Project_Definition/Architecture/2026-09-21_external-dashboard-requirements.md` (Option A + the §4 encryption envelope from the first record). **Build report:** `REPORT_2026-09-21_pilot.md` (probe matrix, ids, cost, ACTIONS FOR KAM).

## Architecture as built
```
Kam's browser ──MFA (Entra, Easy Auth)──► App Service B1 Linux (FastAPI, gunicorn/uvicorn)
   │ decrypts client-side (WebCrypto,       │  GET /            viewer page
   │ private key in IndexedDB, never         │  GET /api/messages|cards?client=&since=   delta reads
   │ sent anywhere)                          │  GET /api/me, /api/pubkey
                                             │
wednesday-seat / tuesday-seat ──cert──► Entra ► JWT (roles) ──► POST /api/seat/messages|cards, GET /api/seat/messages?since=
   (MSAL client-credentials, certificate)   │  Easy Auth EXCLUDES /api/seat/*; the app validates issuer/audience/signature (JWKS)
   encrypt text to Kam's RSA-OAEP public key │  partition = token's Client.* roles; body naming another client -> 403
                                             ▼
                              Table storage `wedndashtkhrqh` (managed identity, shared key DISABLED)
                              tables messages / cards; PartitionKey=client (Secuura|Datasec|WED); RowKey=<ISO ts>_<id>
                              rows hold ciphertext + clear routing fields only — no prose column exists
```
Tenant `d500ebad-cf53-4f2a-a501-f831289e67fc`, subscription `0c57ab37-349c-47ae-a10f-e284a380bbb9`, resource group **`wednesday-dashboard-rg`** (australiaeast) — the ONLY RG this code touches.

## Identifiers (non-secret; also in `scripts/ids.conf`)
| Object | id |
|---|---|
| Entra app `wednesday-dashboard-web` (Easy Auth RP) | appId `c8ba2d4a-e863-438f-b5b6-88fcca491961`, SP `ba1d3b99-9446-47d6-b6c5-be6bc954d049`, user assignment required, Kam only |
| Entra app `wednesday-seat-api` (audience, app roles Seat.Write/Seat.Read/Client.Secuura/Client.Datasec/Client.WED, v2 tokens) | appId `68b210e3-3fd8-45c3-964d-2d596b4a8966` |
| Entra app `wednesday-seat` (roles Seat.Write, Seat.Read, Client.Secuura, Client.WED; certificate) | appId `a9edf1d0-6136-437a-81fa-2b9c313fba08` |
| Entra app `tuesday-seat` (roles Seat.Write, Seat.Read, Client.Datasec; certificate) | appId `7e96ab2d-fad2-4ff3-b28b-f9b3aadbc9f3` |
| App Service plan / web app | `wednesday-dashboard-plan` (B1) / `wednesday-dashboard-e42e` (MI `305da448-befb-4445-b827-6ff5bd49fa82`) |
| Storage account | `wedndashtkhrqh` |

## Envelope (scheme `rsa-oaep-sha256+aes-256-gcm/v1`, `seat/envelope.py` ⇄ `app/static/index.html`)
Per record: 32-byte data key → AES-256-GCM (12-byte IV) over UTF-8 text, **AAD = `client|kind|id|ts`**; data key wrapped RSA-OAEP(SHA-256) to Kam's public key (`app/keys/kam-pilot-public.pub`, kid = sha256(SPKI)[:16]). Clear on purpose (study §4.4): `client, view, ts, kind, id, role, seat`; cards also `status, option_keys, recommended, ruled, ruled_choice`. Cards encrypt a JSON of `{title, bluf, default_action, options[{key,label,detail}]}`.

## Layout
- `app/main.py` — the service. `app/static/index.html` — viewer. `app/keys/kam-pilot-public.pub` — PUBLIC envelope key (tracked).
- `seat/envelope.py`, `seat/seat_common.py`, `seat/post_message.py`, `seat/post_card.py` — the seat CLI (`--dry-run`, `--token-only`).
- `scripts/00_tenant_state.sh` (read-only), `01a_keys.sh`, `01b_identity.sh`, `02_storage.sh`, `03_local_matrix.sh`, `04_deploy.sh`, `04b_easyauth.sh`, `05_probe_live.sh`, `05b_webcrypto_decrypt.mjs`, `price_check.py` — idempotent, each asserts tenant/sub/user first.
- `requirements.txt` — pinned. `.venv/` is local and gitignored.

## Run the seat CLI (Wednesday's machine)
```
2_Project_Files/dashboard-cloud/.venv/bin/python 2_Project_Files/dashboard-cloud/seat/post_message.py \
  --seat wednesday --client Secuura --view Secuura --text "…" [--dry-run]
```
It needs `4_Credentials/dashboard-cloud/wednesday-seat.pem` + `.crt`. Tuesday's pair (`tuesday-seat.*`) is parked in the same folder for Kam to move to the mini — it is not distributed by this repo.

## Re-verify after any change
`bash scripts/05_probe_live.sh` — exit 0 only if all 28 probes pass (Easy Auth both branches, 401/403/201/400 matrix, raw-row ciphertext, offline decrypt +/− controls). Redeploy: `bash scripts/04_deploy.sh` (idempotent; zip guard refuses a private key in the zip).

## Not done (Phase 2+, needs Kam / Wednesday)
Real rows (wiring `chat_reply.sh` / `decision_queue.sh` to the seat CLI); Kam's messages/rulings from the browser back to the seats (write path for the viewer); multi-device key enrolment; custom domain `dash.kreiser.org`; sign-in/API logging to Log Analytics + alerts; export/delete path; Conditional Access (Entra Premium plans are Suspended in this tenant → Security Defaults only).
