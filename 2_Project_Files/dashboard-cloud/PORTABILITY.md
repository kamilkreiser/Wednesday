# dashboard-cloud — PORTABILITY (what is machine-local vs on-drive)

On-drive, gitignored, must travel with the drive (`4_Credentials/dashboard-cloud/`, dir 700):
- `kam-pilot-private.pem` (600) — Kam's envelope private key. Loses it = every row unreadable (REAL rows since Phase 2, 2026-09-21). **Phase 2 key-folder flow:** the browser reads this file from a folder Kam chooses once per browser (Chrome/Edge) — on the Studio that can be this very folder; on the laptop/phone a copy moved by AirDrop/Files (never mail, never the repo). Safari/iOS/Firefox import it once into that browser's IndexedDB instead.
- `wednesday-seat.pem` + `.crt` — Wednesday's API certificate (private + public); the dual-write in `tools/chat_reply.sh` / `decision_queue.sh` needs it on THIS machine. `tuesday-seat.pem` + `.crt` — parked for the mini; **while parked here this machine can act as Tuesday** — move them.
- `easyauth-client-secret.json` (600) — the Easy Auth client secret (also set as the web app setting). Expires **2027-03-21**.
- `4_Credentials/.azure/` — the `az` login state (Kam's MFA login for `kreiser.org@me.com`, tenant d500ebad).

Machine-local, re-creatable:
- `2_Project_Files/dashboard-cloud/.venv/` (python3.12 -m venv + `pip install -r requirements.txt`). **The dual-write uses it** (`tools/_live_board.sh` falls back to `python3`, which then needs `msal`, `cryptography`, `requests` — without them every post fails LOUDLY into `fleet/state/live_board_post_failures.log` and the local write still succeeds). `doctor.sh` item: venv present + `import msal, cryptography, requests` OK.
- `az` CLI ≥ 2.81, `openssl`, `node` ≥ 20 (only for `scripts/05b_webcrypto_decrypt.mjs` and `08b_webcrypto_roundtrip.mjs`), `zip/unzip`.
- Per browser (not on the drive, not in Azure): the remembered key FOLDER handle / imported CryptoKey (IndexedDB `wedpanel`), the key filename (`localStorage wed_key_filename`), the agent toggle / project filters / autoplay (the same localStorage keys the local board used).

State files written by the dual-write (on-drive, untracked): `2_Project_Files/fleet/state/live_board_last_local_ts` (the last local ts handed to the live post), `2_Project_Files/fleet/state/live_board_post_failures.log` (every post that did not reach the live board — read it after a network outage).

In Azure (not on the drive): the web app, plan, storage account (the REAL rows — encrypted; only the private key above reads them), Entra objects — recreated by the numbered scripts if lost; the rows are re-created by `seat/backfill.py` from the local streams while those still exist.
