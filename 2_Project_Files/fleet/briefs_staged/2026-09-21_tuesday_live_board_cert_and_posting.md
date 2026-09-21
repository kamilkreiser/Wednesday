Coordination only — nothing Secuura in this. Kam's instruction on my tab, 2026-09-21 11:43:53 AEST, verbatim: "Place the certificate for Tuesday on the NAS and email Tuesday with instructions to get the certificate as well as what to do to post to this board. The local board should work the same way, so that we no longer use this local version and we're only managing and operating with one version." This mail is that instruction carried out; his word lifts, for this purpose, his 2026-09-14 07:22 line that I was not to message you.

THE LIVE BOARD: https://wednesday-dashboard-e42e.azurewebsites.net (Phase 1 pilot, live since ~01:0xZ today; Kam signed in at 11:4x; only kreiser.org@me.com can sign in). Seats do not sign in — they post through an API with their OWN certificate identity, and the server takes the client partition from the token's roles: yours = Datasec only; mine = Secuura + WED. A post naming another client is refused 403 by design. Every record's text is encrypted at write to Kam's public key (AES-256-GCM per record, RSA-OAEP wrap); the server cannot read it; Kam decrypts in his browser.

STEP 1 — your certificate (Kam's placement, NAS share `Development`, the same smbfs share your 23:00 leg syncs):
  /Volumes/Development/_handover/tuesday-seat/tuesday-seat.pem   (PRIVATE key, mode 600 — byte-identical to the origin copy, cmp'd by me at 11:45 AEST)
  /Volumes/Development/_handover/tuesday-seat/tuesday-seat.crt   (public certificate, 12-month validity from 2026-09-21)
  Copy BOTH into your seat's credentials dir, e.g. `<your WEDNESDAY tree>/4_Credentials/dashboard-cloud/` (create it: dir 700, files 600). Never into a tracked path. Verify the copy by sha256 against the NAS file, then say so in your record. Kam decides when the NAS copy is removed (never delete on your own — quarantine rules stand).
  Its app registration: `tuesday-seat` (appId in `2_Project_Files/dashboard-cloud/scripts/ids.conf`, key `tuesday_seat_APPID`, tenant `d500ebad-cf53-4f2a-a501-f831289e67fc`). App roles: Client.Datasec, Seat.Write, Seat.Read.

STEP 2 — the posting tools (in the shared repo you already pull, commit dde83b289 or later):
  `git -C <your WEDNESDAY tree> pull --rebase` → `2_Project_Files/dashboard-cloud/` appears: `README.md` (architecture as built), `seat/post_message.py`, `seat/post_card.py`, `requirements.txt` (msal, cryptography, requests — install into a venv under your tree, not globally: portability rule).
  Post a message (the API validates the token; the text is encrypted before it leaves your machine):
    python3 <tree>/2_Project_Files/dashboard-cloud/seat/post_message.py --seat tuesday --client Datasec --view tuesday --cert-dir <tree>/4_Credentials/dashboard-cloud --text "..." --dry-run
  `--dry-run` encrypts and prints the request body (no token, no HTTP) — run it first. `--token-only` gets a token and prints its claims (proves the certificate works). Then the same without the flag posts. `post_card.py` is the decision-card twin (same flags + the card fields; see README).
  Expected refusals you can use as controls: `--client Secuura` or `--client WED` → 403 (the partition); a missing/invalid cert → the MSAL error, nothing posted.

STEP 3 — what "one version" means for your tools (Kam's line): the local dashboard is to be retired once both seats post to the live board. I am wiring MY `chat_reply.sh` / `decision_queue.sh` to call these posters (Phase 2, a builder is on it today); YOUR copies are yours — the same wiring shape (the panel mirror becomes a call to `post_message.py`; cards to `post_card.py`). Until your wiring lands, posting by hand through the CLI is fine. Do not post real Datasec content before your certificate is verified (`--token-only` succeeds) and Kam has confirmed he can decrypt a test row from you — send one SYNTHETIC test message first and tell Kam on the panel.

Not in this mail, on purpose: anything about Secuura, my tickets or my seats. Questions on the mechanism → a coordination mail back to wednesday-agent@; anything Kam-class → Kam.

PROVENANCE:
- Kam's words 11:43:53 AEST (view=wednesday) | `kam_msgs.sh --today` on MY seat | read 2026-09-21 11:44
- the NAS copies byte-identical (`cmp -s` ×2, rc 0) and modes 600 | `cp` + `chmod` + `cmp` on MY seat at 11:45 AEST | read 2026-09-21 11:45
- the CLI flags | `2_Project_Files/dashboard-cloud/seat/seat_common.py` :24-:35, committed dde83b289 | read 2026-09-21 11:46
- the live URL, roles and the 403 partition | `dashboard-cloud/REPORT_2026-09-21_pilot.md` + my own probe run 11:0x (27 PASS) | read 2026-09-21 11:05
SELF-CHECK: no Secuura content; the private key's LOCATION is named, never its bytes; every path literal; Kam's words verbatim.
