# External dashboard — Phase 1 PILOT report (2026-09-21)

**Builder:** Wednesday's builder agent (delegated 10:19). **Ruling:** Kam 10:15 — build it, deploy to the agent-controllable tenant `d500ebad`, encrypted rows so the shared tenant is acceptable.
**Scope today:** Phase 1 pilot, live in Azure, SYNTHETIC rows only. No commit, no push (Wednesday reviews).
**Written incrementally** — each step appends below as it lands. If this file ends mid-step, the builder was killed there.

## Log
- 10:19 dirs created: `2_Project_Files/dashboard-cloud/{app,seat,scripts}`, `4_Credentials/dashboard-cloud/` (chmod 700). Report opened.

## Inputs read (whole)
Study `1_Project_Definition/Architecture/2026-09-21_external-dashboard-requirements.md` §0–§7; `dashboard/server.py` (routes + handlers), `decisions.json` FIELD NAMES only (key-count script, no text read); `PORTS.md`; the four lessons named in the brief; both CLAUDE.md files.

### Open-question defaults taken (study §7) — STATED
| Q | Taken as |
|---|---|
| Q1 | **RULED by Kam 10:15**: tenant `d500ebad` (Datasec environment #5, controller `kreiser.org@me.com`), acceptable because rows are encrypted end-to-end. |
| Q2 | One store, partitioned by `client` (`Secuura`/`Datasec`/`WED`), claim enforced server-side from the token's app roles. |
| Q3 | Both phone + laptop; pilot uses ONE RSA-OAEP keypair Kam moves to his devices; new devices see only rows written after enrolment (Phase 2). |
| Q4 | USD 15–20/month band (B1 + Table storage + no Key Vault needed in the pilot — see cost section; the pilot has no server-side key to vault since the private key never touches Azure). |
| Q5 | Local machines remain the record; the site holds synthetic rows only today. |
| Q6 | Azure operator IS treated as in-model — the envelope is on from the FIRST record (Kam's 10:15 wording "as this would be encrypted"). |
| Q7 | No custom domain today; `*.azurewebsites.net` until m4/m5 pass. |
| Q8 | No mesh. |
| Q9 | MEASURED below: Entra Premium plans exist but are **Suspended** (since 2026-09-09) → effectively Free; Security Defaults state UNMEASURED (Graph refused the scope). |

## Step 0 — tenant state inherited (read-only) — 10:21
Script: `scripts/00_tenant_state.sh`, output `scripts/00_tenant_state.out`.
- `az account show`: tenantId `d500ebad-cf53-4f2a-a501-f831289e67fc`, subscription `0c57ab37-349c-47ae-a10f-e284a380bbb9` "Azure subscription 1", user `kreiser.org@me.com` → **ASSERTION PASS** (printed by the script; it exits 3 on mismatch — it CAN fail).
- Signed-in user object: id `c38fcea6-ff23-40c3-a875-e84e324910cf`, UPN `kreiser.org_me.com#EXT#@kreiserorgme.onmicrosoft.com` (an external/MSA-backed account in the tenant; `userType` returned null). Tenant display name "Default Directory", verified domain `kreiserorgme.onmicrosoft.com`.
- **Security Defaults: UNMEASURED.** `az rest GET /policies/identitySecurityDefaultsEnforcementPolicy` → `Forbidden: required scopes are missing in the token` (the CLI's Graph token lacks `Policy.Read.All`). Kam reads it in Entra admin centre → Properties → Manage security defaults. Not changed by me.
- **Licence tier:** `organization.assignedPlans` shows `AADPremiumService` (P1 `41781fb2…` and P2 `eec0eb4f…`) both **`Suspended` since 2026-09-09T17:28Z** (a lapsed trial); everything else enabled is M365 SKU plans. → Conditional Access is NOT available; MFA must come from Security Defaults (or per-user MFA). Q9 answer: Free-equivalent.
- App registrations named `wednesday*` / `tuesday*`: **none** (`[]`, `[]`) — nothing to reuse; everything below is created today.
- `az group exists -n wednesday-dashboard-rg` → `false`. Existing RGs (names only, read-only, all OFF LIMITS): datasec-sales-portal-rg, datasec-backups-rg, nexusai-staging-rg, nexusai-dev-rg, nexusai-marketplace-validate, mypki-demo-rg, hpas-quickquote-rg, hpsm-dev-rg, attio-bridge-rg, NetworkWatcherRG.
- az CLI 2.81.0.

## Step 1 — identities — 10:24–10:29
Scripts: `scripts/01a_keys.sh` (key material), `scripts/01b_identity.sh` (Entra objects; idempotent, tenant-asserted, exits on mismatch). Non-secret ids recorded in `scripts/ids.conf`.
Gitignore-at-creation: appended `2_Project_Files/dashboard-cloud/.env*`, `**/*.pem`, `**/*.key`, `**/*.pfx`, `**/*.out`, `**/.venv/`, `**/*.zip` (scoped to the pilot dir; `git ls-files` had 0 tracked .pem/.key/.pfx so nothing else changes status).

| Object | appId | objectId | SP id | credential |
|---|---|---|---|---|
| `wednesday-dashboard-web` (Easy Auth RP, AzureADMyOrg, ID tokens on, redirect `https://wednesday-dashboard-e42e.azurewebsites.net/.auth/login/aad/callback`) | `c8ba2d4a-e863-438f-b5b6-88fcca491961` | `7a5bec93-63f6-4c8a-8019-40050eb47f1d` | `ba1d3b99-9446-47d6-b6c5-be6bc954d049` | client secret `easyauth-2026-09-21`, **expires 2027-03-21T00:00:00Z** → ONLY in `4_Credentials/dashboard-cloud/easyauth-client-secret.json` (600) and later the web app setting |
| `wednesday-seat-api` (audience; identifierUri `api://68b210e3-…`; `requestedAccessTokenVersion=2`; app roles `Seat.Write`, `Seat.Read`, `Client.Secuura`, `Client.Datasec`, `Client.WED`, all `allowedMemberTypes=[Application]`) | `68b210e3-3fd8-45c3-964d-2d596b4a8966` | `0b5eb4b8-1e2b-479a-9c9d-65abf9e542e3` | `33d4ea4a-34b6-4221-8823-701b9a495948` | none |
| `wednesday-seat` | `a9edf1d0-6136-437a-81fa-2b9c313fba08` | `1c16deff-eeb8-4e7f-bb3f-7c13a6e36212` | `3514c8fc-c794-4ee7-a41d-3172b7b472c7` | certificate thumbprint `C11E2AECF3E9AD3BF3CD07042CEBC9E0CE9D16CC`, valid to 2027-09-21; **0 passwords** (checked) |
| `tuesday-seat` | `7e96ab2d-fad2-4ff3-b28b-f9b3aadbc9f3` | `20d9c1a7-bde9-45be-85a3-9f2d248dcd89` | `8c5f26a7-4d99-4e66-bb9f-af54d5516f83` | certificate thumbprint `3718B4C1B2F5C9B0E6549BDE1DCBCEFF047C93AA`, valid to 2027-09-21; **0 passwords** (checked) |

- `wednesday-dashboard-web` SP: `appRoleAssignmentRequired=true` (read back `true`); app-role assignments on it = exactly one principal, "kamil kreiser" (`c38fcea6-…`). → only Kam can sign in.
- Role grants (read back from Graph `appRoleAssignments`): `wednesday-seat` = Seat.Write, Seat.Read, **Client.Secuura, Client.WED**; `tuesday-seat` = Seat.Write, Seat.Read, **Client.Datasec**.
- Key material on disk (`4_Credentials/dashboard-cloud/`, dir 700): `kam-pilot-private.pem` (RSA-4096, 600), `wednesday-seat.pem` / `tuesday-seat.pem` (private, 600), `*.crt` (public certs). Public envelope key → `app/keys/kam-pilot-public.pub` (tracked, PEM SPKI). **Tuesday's private key is NOT distributed by me** — it sits in Wednesday's 4_Credentials for Kam to move to the mini.
- One fix on the way: `az ad app update --set api.requestedAccessTokenVersion=2` cannot address the nested property ("Couldn't find 'api'"); replaced with a Graph PATCH on the application object. Read back `tokenVersion=2`.

## Step 2 — resource group + store — 10:31
Script `scripts/02_storage.sh` (tenant-asserted; every command names `-g wednesday-dashboard-rg --subscription 0c57ab37-…`).
- `az group create wednesday-dashboard-rg` australiaeast, tags project/phase/owner/created. (Only RG touched today.)
- Storage account **`wedndashtkhrqh`**: Standard_LRS, StorageV2, `minimumTlsVersion=TLS1_2`, `allowBlobPublicAccess=false`, `httpsOnly=true`, australiaeast. Resource id `/subscriptions/0c57ab37-…/resourceGroups/wednesday-dashboard-rg/providers/Microsoft.Storage/storageAccounts/wedndashtkhrqh`.
- Tables `messages` and `cards` created with `--auth-mode login` (RBAC, no account key used). PartitionKey = `client`, RowKey = `<ISO ts>_<short id>`.
- RBAC: `Storage Table Data Contributor` granted to Kam's user (`c38fcea6-…`) scoped to the storage account only — this is what the probes use to read raw rows. The web app's managed identity gets the same role in Step 4.
- Shared-key access left enabled at account level for now (the SDK path via managed identity is the plan; if the MI path proves out, `--allow-shared-key-access false` is a Phase-2 hardening item and is noted in ACTIONS).

## Step 3 — the app, built and proven locally — 10:33–10:38
Framework: **FastAPI + gunicorn/uvicorn** (`requirements.txt`, pinned). Files: `app/main.py` (server), `app/static/index.html` (viewer), `app/keys/kam-pilot-public.pub`, `seat/envelope.py` (envelope v1), `seat/seat_common.py`, `seat/post_message.py`, `seat/post_card.py`.
- Envelope: per-record AES-256-GCM data key, 12-byte IV, data key wrapped RSA-OAEP-SHA256 to Kam's 4096-bit pilot public key; **AAD = `client|kind|id|ts`** so a ciphertext re-labelled to another partition fails to decrypt. `seat/envelope.py` self-test: positive, wrong-key negative, AAD-relabel negative → PASS.
- Server holds no private key; refuses any body carrying `text`/`plaintext` (400); takes the partition from the token's `Client.*` roles; `Seat.Write`/`Seat.Read` gate the verb; viewer routes refuse without the Easy Auth principal header (defence in depth).
- Seat CLI: MSAL client-credentials **with certificate** (thumbprint + private PEM from 4_Credentials), scope `api://<API_APPID>/.default`; `--dry-run` (encrypt + print body, no token, no HTTP) and `--token-only` (claims only) verified. Real tokens obtained for both seats: v2 issuer, `aud=68b210e3-…`, roles exactly as granted (wednesday: Seat.Write, Seat.Read, Client.Secuura, Client.WED; tuesday: Seat.Write, Seat.Read, Client.Datasec).
- One self-caught false positive: the per-record "plaintext not in envelope" guard tripped on a 1-char test string (any single char occurs in base64). Guard now applies to plaintexts ≥ 8 chars; the token-only probe uses a real synthetic sentence.
- **Local matrix** (`scripts/03_local_matrix.sh`, app on 127.0.0.1:47789 transiently, against the REAL storage account through my CLI credential) — LOCAL PROOF ONLY, repeated live in Step 5:
  health 200 · `/` no principal 401 · `/api/messages` no principal 401 · with principal header 200 · POST no token **401** · garbage token **401** · wednesday→Secuura **201** · wednesday→Datasec **403** · tuesday→Secuura **403** · tuesday→Datasec **201** · plaintext field **400** · card WED **201**.
  Rows written by this local run exist in the live tables (ids `local-alpha`, `local-delta`, `local-card1`) — all SYNTHETIC text.

## Step 4 — deploy — 10:41–10:58
Scripts: `scripts/04_deploy.sh` (plan, app, identity, RBAC, settings, zip deploy), `scripts/04b_easyauth.sh` (Easy Auth v2 PUT + read-back). Price check `scripts/price_check.py` BEFORE creating the plan: B1 Linux australiaeast **USD 0.019/h → 13.87/month** (Retail Prices API, source URL in the script output); Table LRS 0.0495 USD/GB-month; operations 0.00036 USD/10k. Within the band.
- Plan **`wednesday-dashboard-plan`**: Linux, **B1** (Basic, 1 worker). Web app **`wednesday-dashboard-e42e`** (`PYTHON|3.12`), `httpsOnly=true`, `ftpsState=Disabled`, `minTlsVersion=1.2`, HTTP/2 on, Always On on, client affinity off, **basic publishing credentials (FTP + SCM) disabled** (`allow=false` read back), system-assigned identity `305da448-befb-4445-b827-6ff5bd49fa82` with `Storage Table Data Contributor` scoped to `wedndashtkhrqh`. **No account key or connection string anywhere** — the app reaches Table storage via managed identity (proven by the live 201s in Step 5).
- App settings (names): SCM_DO_BUILD_DURING_DEPLOYMENT, TENANT_ID, SEAT_API_APPID, STORAGE_ACCOUNT, SEAT_APP_MAP, MICROSOFT_PROVIDER_AUTHENTICATION_SECRET (value read from 4_Credentials inside the script, never echoed), WEBSITE_AUTH_AAD_ALLOWED_TENANTS.
- Deploy method: **zip deploy** (`az webapp deploy --type zip`, Oryx build from `requirements.txt`). Zip = `requirements.txt`, `app/`, `seat/` only. Zip guard: 0 PEM private-key armour lines, positive control 1 public-key armour line in the public file AND 1 on a real private key file (the guard can fail — it did once, see below).
- Easy Auth v2 (`authsettingsV2` PUT, read back): `requireAuthentication=true`, `unauthenticatedClientAction=RedirectToLoginPage`, provider Microsoft, issuer `https://login.microsoftonline.com/d500ebad-…/v2.0`, clientId `c8ba2d4a-…`, secret via setting name, `allowedApplications=[c8ba2d4a-…]`, **`excludedPaths=["/api/seat/*"]`** (the seat routes bypass Easy Auth and are gated by the app's own JWT validation), cookie 8 h, token store on.

Three failures on the way, each fixed at root and re-verified (no-skip-on-failure):
1. `az --subscription X <cmd>` → "misspelled" — global arg must follow the subcommand; wrapped in a function.
2. Zip guard tripped: it grepped `BEGIN PRIVATE` and matched the viewer JS's own regex text (`/BEGIN PRIVATE KEY/`). Tightened to the PEM armour line `-----BEGIN …PRIVATE`, case-insensitive, with a positive control on a real key file that must return 1.
3. **First deploy: container exited 1 — `Error: can't chdir to '/home/site/wwwroot/app'`** (from `LogFiles/StartupLogs/*_failure.log`). Oryx extracts `output.tar.zst` to `/tmp/<hash>` and runs the startup command there, so the absolute path does not exist. Startup command changed to a relative `--chdir app`; restarted; `/api/seat/health` → 200 at 10:54:51 live.
4. (Process) I edited `04_deploy.sh` while it was still running; bash reads incrementally and died with "unexpected EOF" before the Easy Auth step. `bash -n` proves the file itself parses; the Easy Auth step became its own script `04b_easyauth.sh` and was applied + read back.

## Step 5 — PROVEN LIVE — 10:57–11:03
**Live URL: `https://wednesday-dashboard-e42e.azurewebsites.net/`**
Script `scripts/05_probe_live.sh` (exit 1 on any mismatch; final run: **ALL 28 PROBES PASS**). Full output below is the verbatim tee of the final run. Three earlier runs had HARNESS defects, each fixed and re-run: (i) I expected a bare 302 — Easy Auth returns **401 + `WWW-Authenticate: Bearer`** to non-browser clients and **302 → login.microsoftonline.com** to browsers (`Accept: text/html`); both are Easy Auth's refusal (empty body, `x-ms-middleware-request-id`), distinguishable from the app's own 401 which carries a JSON `detail` — the probe now asserts that distinction; (ii) the label was being passed to curl as a URL (`000401`); (iii) `loc()` truncated the Location header before the grep. None of these were site defects; the site's responses were identical across all runs.

### Probe matrix (final run, verbatim)
```
### A. Easy Auth gate (viewer surface)
PASS  GET / plain client: 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
PASS  GET / (browser Accept): 302 -> login.microsoftonline.com/<tenant>/oauth2/v2.0/authorize
      location: https://login.microsoftonline.com/d500ebad-cf53-4f2a-a501-f831289e67fc/oauth2/v2
      redirect carries client_id=c8ba2d4a-e863-438f-b5b6-88fcca491961
      redirect_uri=https%3A%2F%2Fwednesday-dashboard-e42e.azurewebsites.net%2F.auth%2Flogin%2Faad%2Fcallback
PASS  GET /api/messages plain: 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
PASS  GET /api/messages (browser Accept): 302 -> login.microsoftonline.com/<tenant>/oauth2/v2.0/authorize
PASS  GET /<nonexistent> plain: 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
PASS  GET /<nonexistent> (browser Accept): 302 -> login.microsoftonline.com/<tenant>/oauth2/v2.0/authorize
PASS  GET /api/pubkey plain: 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
PASS  GET /api/messages with FORGED x-ms-client-principal-* headers from outside: 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
### B. Seat API gate
PASS  GET /api/seat/health (excluded path, anonymous): expected 200 got 200
PASS  POST /api/seat/messages NO token: expected 401 got 401
      body: {"detail":"bearer token required"}
PASS  POST forged token: expected 401 got 401
      body: {"detail":"token invalid: PyJWKClientError"}
PASS  GET /api/seat/messages NO token: expected 401 got 401
### C. The partition (R0) — token roles decide, body is refused
      body: {"stored":{"client":"Secuura","id":"live-alpha-010022","ts":"2026-09-21T01:00:22.569Z","row_key":"2026-09-21T01:00:22.569Z_live-alpha-010022","written_by":"wedn
PASS  wednesday-seat -> client=Secuura: expected 201 got 201
      body: {"stored":{"client":"WED","id":"live-wed-010022","ts":"2026-09-21T01:00:23.999Z","row_key":"2026-09-21T01:00:23.999Z_live-wed-010022","written_by":"wednesday"}}
PASS  wednesday-seat -> client=WED: expected 201 got 201
      body: {"detail":"partition not granted to this seat"}
PASS  wednesday-seat -> client=Datasec (MUST refuse): expected 403 got 403
      body: {"detail":"partition not granted to this seat"}
PASS  tuesday-seat -> client=Secuura (MUST refuse): expected 403 got 403
      body: {"detail":"partition not granted to this seat"}
PASS  tuesday-seat -> client=WED (not granted to tuesday; MUST refuse): expected 403 got 403
      body: {"stored":{"client":"Datasec","id":"live-delta-010022","ts":"2026-09-21T01:00:30.206Z","row_key":"2026-09-21T01:00:30.206Z_live-delta-010022","written_by":"tues
PASS  tuesday-seat -> client=Datasec: expected 201 got 201
### D. Card + plaintext refusal
PASS  wednesday-seat card -> Secuura: expected 201 got 201
PASS  POST with a plaintext 'text' field: expected 400 got 400
      body: {"detail":"plaintext fields are refused; encrypt into the envelope"}
PASS  GET /api/seat/messages?client=Datasec with wednesday token: expected 403 got 403
PASS  GET /api/seat/messages (own partitions) with wednesday token: expected 200 got 200
      clients in response: ['Secuura', 'WED'] rows: 3 fields: ['ciphertext', 'client', 'id', 'iv', 'kid', 'kind', 'role', 'row_key', 'scheme', 'seat', 'ts', 'view', 'wrapped_key', 'written_at', 'written_by']
PASS  GET viewer /api/messages with a SEAT bearer token (a seat is not Kam; Easy Auth allowedApplications=[web app] refuses it): 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)
### E. Raw row = ciphertext; offline decrypt positive + negative controls
      raw row fields: ['PartitionKey', 'RowKey', 'Timestamp', 'ciphertext', 'etag', 'id', 'iv', 'kid', 'kind', 'role', 'scheme', 'seat', 'ts', 'view', 'wrapped_key', 'written_at', 'written_by']
      ciphertext (first 48 b64 chars): BcrqZ1CynEC8foJVASUGIEtkElJlEEihsFmj/Qo0sDVW/C16 ...
PASS  plaintext substring NOT in raw row
PASS  offline decrypt with the pilot private key == 'SYNTHETIC live alpha 010022 — wednesday writes Secuura'
PASS  wrong key refused: ValueError
PASS  row relabelled to another client refused (AAD): InvalidTag
### F. Rows per partition (counts only)
      messages/Secuura: 5
      messages/Datasec: 5
      messages/WED: 4
      cards total: 5
### RESULT: ALL PROBES PASS
```
Every row written by these probes is SYNTHETIC (`SYNTHETIC live … ` / `SYNTHETIC card …`). Store now holds messages Secuura 5 / Datasec 5 / WED 4, cards 5 — all synthetic (the first Secuura/Datasec/WED rows are from the Step 3 local run against the same store).

### Browser decrypt path — what was proven and by what
- `scripts/05b_webcrypto_decrypt.mjs` extracts the viewer page's OWN helper functions (`pemToDer`, `unb64`, `AAD`) from `index.html` and runs the page's decrypt sequence in **Node 24 `globalThis.crypto.subtle`** (the same WebCrypto API and parameters the browser uses: `importKey('pkcs8', RSA-OAEP/SHA-256, extractable=false, ['decrypt'])`, `RSA-OAEP decrypt`, `AES-GCM decrypt` with `additionalData`) against the real raw row fetched from the live table:
  `key imported: extractable = false, RSA-OAEP SHA-256 4096` · `PASS WebCrypto decrypt == expected synthetic text` · `PASS relabelled row (AAD) refused: OperationError` · `PASS wrong key refused: OperationError`.
- `node --check` on the page script: parses.
- **This is Node's WebCrypto, not Safari/Chrome.** The in-browser path (file picker → IndexedDB → render → `speechSynthesis`) is exercised only when Kam signs in with his MFA and loads the key — that is item (b) in ACTIONS FOR KAM. Stated plainly: a second implementation is not the browser.

### What the server can see (measured from the raw row)
Clear columns: `PartitionKey`(client), `RowKey`, `Timestamp`, `id`, `ts`, `kind`, `view`, `role`, `seat`, `written_by`, `written_at`, `scheme`, `kid`, `iv`, `wrapped_key`, `ciphertext`; cards add `client_project`, `status`, `option_keys`, `recommended`, `ruled`, `ruled_choice`. **No prose column exists.** The probe asserted the synthetic plaintext is absent from the raw row JSON and that only the pilot private key (in 4_Credentials, never in Azure) recovers it.

### Resources + cost (sources: Retail Prices API, `scripts/price_check.py`, australiaeast, USD, 2026-09-21)
`az resource list -g wednesday-dashboard-rg`:
| Resource | Type | SKU | Monthly estimate | Source |
|---|---|---|---|---|
| `wednesday-dashboard-plan` | Microsoft.Web/serverfarms | **B1** Basic Linux, 1 worker | **USD 13.87** (0.019/h × 730) | `…serviceName eq 'Azure App Service' and skuName eq 'B1'` → "Azure App Service Basic Plan - Linux, B1, 0.019 USD/1 Hour" |
| `wednesday-dashboard-e42e` | Microsoft.Web/sites | (runs on the plan) | 0 | — |
| `wedndashtkhrqh` | Microsoft.Storage/storageAccounts | Standard_LRS, Tables | **< USD 0.01** at the pilot's KB of data; 0.0495 USD/GB-month stored + 0.00036 USD per 10k operations (a 5-s poll ≈ 0.5M ops/month ≈ USD 0.02) | `…serviceName eq 'Storage' and productName eq 'Tables'` |
| Easy Auth, managed identity, Entra app registrations, RBAC | — | included / free | 0 | — |
| **Total** | | | **≈ USD 13.9–14/month** — inside the study's 15–20 band; no Key Vault was needed because no server-side key exists in this design | |
No SKU approached the USD 25 stop line.

### RBAC on the storage account (who can read raw rows)
`Storage Table Data Contributor`, scope = the storage account only: (1) Kam's user `kreiser.org@me.com` (for probes/admin), (2) the web app's system-assigned identity (`305da448-…`, appId `da5ef653-…`, displayName `wednesday-dashboard-e42e`). Nobody else. Shared-key access is still ENABLED at the account level (default) but unused — disabling it is listed for Kam/Phase 2.

### Post-probe hardening (11:03) — inside the RG only
`az storage account update wedndashtkhrqh --allow-shared-key-access false` → read back `allowSharedKeyAccess=false`. The app never held a key (managed identity), so nothing depended on it. Re-verified live: seat write → **201** (`live-nokey-010324`, WED), `/api/seat/health` → 200. The full 28-probe matrix was run again after the `ids.env→ids.conf` rename: **ALL PROBES PASS**.

Store at hand-over: messages Secuura 6 / Datasec 6 / WED 6, cards 6 — **every row synthetic**, written by the local matrix, the live probes and the hardening check.

## Step 6 — ACTIONS FOR KAM (action first, literal steps)

**(a) Sign in once and confirm MFA fires.** Open `https://wednesday-dashboard-e42e.azurewebsites.net/` on your phone and on the laptop. Only `kreiser.org@me.com` can sign in (Entra app `wednesday-dashboard-web` has *user assignment required* and exactly one assigned user — you). MFA: **I could not measure Security Defaults** (Graph refused `Policy.Read.All` to the CLI). The tenant's Entra Premium P1/P2 plans are **Suspended since 2026-09-09**, so Conditional Access is unavailable — MFA on this sign-in comes from Security Defaults or per-user MFA only. **Check:** Entra admin centre → Identity → Overview → Properties → *Manage security defaults* — it must say **Enabled**. If it is not, enable it (your action; I changed no tenant-wide security). Study measurement m5: screenshot the MFA prompt on a fresh browser.

**(b) Load the pilot private key into the page (this is what makes text readable).** The file is `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud/kam-pilot-private.pem` (RSA-4096, PKCS8, mode 600). Copy it to the device by a channel you trust (AirDrop / Files app; NOT mail, NOT the repo). In the page tap **Load private key…**, pick the file. The browser imports it as a non-extractable WebCrypto key into IndexedDB (per browser, per device; it is never uploaded — the server has no decrypt route). Rows then render; **Forget key** removes it. Tap **Autoplay** once (a user gesture is required on iOS before `speechSynthesis` will speak) — study measurement m8. Until you do this, the page shows every row as "🔒 encrypted", which is the correct state.

**(c) Easy Auth client secret expiry: 2027-03-21T00:00Z.** Six months from today. It lives in the web app setting `MICROSOFT_PROVIDER_AUTHENTICATION_SECRET` and in `4_Credentials/dashboard-cloud/easyauth-client-secret.json`. Before that date: `az ad app credential reset --id c8ba2d4a-e863-438f-b5b6-88fcca491961 --append …` then update the app setting (Wednesday can script it; it is the one secret in the design). Seat certificates expire **2027-09-21**.

**(d) Tuesday's certificate is parked, not distributed.** `4_Credentials/dashboard-cloud/tuesday-seat.pem` (private) + `tuesday-seat.crt` sit in WEDNESDAY's credentials folder on this drive. Move them to the mini's Tuesday `4_Credentials/` yourself (or tell Wednesday how you want them to travel). Until then Tuesday cannot write to the API — by design.

**(e) Only synthetic rows exist.** 18 messages + 6 cards, all prefixed `SYNTHETIC`. Real rows begin only when Wednesday wires `tools/chat_reply.sh` / `tools/decision_queue.sh` to `dashboard-cloud/seat/post_message.py` / `post_card.py` — Phase 2, not today, and per the study's dual-write default. To wipe the pilot rows at any point: the tables can be truncated (or the RG deleted) — one command, nothing outside `wednesday-dashboard-rg` is touched; I deleted nothing.

**(f) Optional, your call:** custom domain `dash.kreiser.org` (needs your DNS; Basic tier supports managed TLS); Log Analytics + sign-in alerting (S8 in the study) — adds a few USD/month; re-enable P1 (USD 7/user/month) if you want named-location Conditional Access.

## Step 7 — repo hygiene — 11:05
- Code under `2_Project_Files/dashboard-cloud/`: `README.md` (architecture as built, ids, no secrets), `PORTABILITY.md`, `requirements.txt`, `app/`, `seat/`, `scripts/` (00–07 + `price_check.py`), this report. **`scripts/ids.env` was renamed `ids.conf`** because the workspace's global `*.env` ignore would have silently kept the (non-secret) ids out of the repo and broken the seat CLI on any other machine; all references updated, probes re-run green.
- `.gitignore`: pilot patterns appended (see Step 1); `git check-ignore` confirms `4_Credentials/…`, `.venv/`, `*.pem`, `.env`, `*.out` are ignored and `app/keys/kam-pilot-public.pub` (PUBLIC key) is not.
- **Secret VALUE scan** `scripts/07_secret_scan.sh` — needles assembled at runtime (the first version self-matched its own literals and had `--exclude-dir` after `--`, so it scanned `.venv`; both fixed): PEM armour line 0 files (control 1) · Easy Auth secret value 0 (control 1) · 48-char body slices of all three private keys 0 (controls 1,1,1) · the storage connection-string key marker 0 (control 1 in a scratch fixture) · the az credential-reset JSON's password field name 0 (control 1) → **CLEAN**. (First run of the finished report FAILED on exactly this line, which quoted both markers literally — the prose was reworded; the scan is what caught it.)
- `git -C /Volumes/DevMASTER/WEDNESDAY status --porcelain -- 2_Project_Files/dashboard-cloud .gitignore`: ` M .gitignore` + 24 untracked files under `dashboard-cloud/` (listed by `-uall` above in the scratch log; `.venv/`, `__pycache__/`, `*.out` correctly absent). **Nothing committed, nothing pushed** — Wednesday reviews.
- Not touched: daily note, ledger, pickup, panel, any other project, any other resource group, any tenant-wide security setting. No mail sent, no panes tapped.

## Not done today (stated)
- In-browser (Safari/Chrome) decrypt + speech: proven with Node's WebCrypto on the page's own code, not in a browser session (needs Kam's MFA sign-in — ACTIONS (b)).
- Kam's write path (his messages/rulings from the browser to the seats): the viewer is read-only in the pilot.
- Real rows, dual-write wiring, multi-device enrolment, custom domain, logging/alerts, export/delete route, per-client m1–m3 latency measurements on mobile data (need Kam's phone).
- Security Defaults state: UNMEASURED (permission), listed for Kam.
