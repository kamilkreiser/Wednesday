# dashboard-cloud — PORTABILITY (what is machine-local vs on-drive)

On-drive, gitignored, must travel with the drive (`4_Credentials/dashboard-cloud/`, dir 700):
- `kam-pilot-private.pem` (600) — Kam's envelope private key. Loses it = every pilot row unreadable (synthetic today).
- `wednesday-seat.pem` + `.crt` — Wednesday's API certificate (private + public). `tuesday-seat.pem` + `.crt` — parked for the mini.
- `easyauth-client-secret.json` (600) — the Easy Auth client secret (also set as the web app setting). Expires **2027-03-21**.
- `4_Credentials/.azure/` — the `az` login state (Kam's MFA login for `kreiser.org@me.com`, tenant d500ebad).

Machine-local, re-creatable:
- `2_Project_Files/dashboard-cloud/.venv/` (python3.12 -m venv + `pip install -r requirements.txt`).
- `az` CLI ≥ 2.81, `openssl`, `node` ≥ 20 (only for `scripts/05b_webcrypto_decrypt.mjs`), `zip/unzip`.

In Azure (not on the drive): the web app, plan, storage account, Entra objects — recreated by the numbered scripts if lost.
