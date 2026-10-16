# B155 · SEAT-A · Security Composer demo: remove the site password gate (Kam's instruction)

**From:** Tuesday (Datasec coordinator). **Project:** Datasec / Security Composer. **Written:** 2026-10-16 ~12:5x AEDT.
**Your STATUS file:** `1_Project_Definition/Briefs/2026-10-16_B155_STATUS.md`. It is your wrap; no mail. Its LAST line is one of:
`DONE: B155 gate removed @ <UTC time>` · `BLOCKED: B155 <one line>`.

## Kam's words (live board, verbatim, view=tuesday)
- 12:47:19 AEDT: "Paul is having the same issue looking at it, can you please reset his access details and send him and CC me on the email?"
- 12:48:48 AEDT: "Second thought, please remove the access requirement to the security composer so that anyone with the link can access the site."
- 12:49:00 AEDT: "Once it's done, please let me know."

The 12:48:48 message **supersedes** the 12:47:19 one: no password reset, no mail to Paul. Tuesday told Kam on the board (12:5x) that with the gate gone anyone with the link can sign in as any demo persona and change demo content, and that a backup comes first. He has not withdrawn the instruction. This is his decision; carry it out.

## What is there (measured today by seat B154; re-measure, do not trust)
Source: `1_Project_Definition/Briefs/2026-10-16_B154_STATUS.md` (FOUND table).
- Site `hpsm-composer-demo.australiaeast.cloudapp.azure.com`, one VM. Caddy `basic_auth` in `/opt/hpsm/Caddyfile` with 2 users: `{$DEMO_USER}` (kam) and `paul` (B39, C-17). nginx `edge` and the app containers sit behind Caddy.
- App sign-in is `idp-mock`: pick a persona, no password.
- B154 reached the box only through `az vm run-command` with the project's own `AZURE_CONFIG_DIR`. Use the same route. Add no SSH key and no NSG rule.

## Steps
0. Copy this brief unchanged into `1_Project_Definition/Briefs/` and record sha256 of both copies.
1. Identity: `az account show` (project config dir). Wrong tenant or subscription: STOP, `BLOCKED`.
2. **Dependency check before any change.** Does anything rely on the gate's identity: nginx `$remote_user`, an `Authorization`/`X-Forwarded-User`/`Remote-User` header read by the API, web or idp, the `{$DEMO_USER}` env var used anywhere but the gate? Also: is the Caddyfile produced by a deploy script or template in the repo (so the next deploy would put the gate back)? Read; change nothing yet. If the app needs the gate's identity to work, STOP and `BLOCKED` with what you found.
3. **Backups, on the box, before the change:** copy the Caddyfile to `/opt/hpsm/Caddyfile.pre-b155-<UTC stamp>`, and take a database dump of the demo database into a dated file under `/opt/hpsm/` (or the box's existing backup folder if one exists). Record path, size and sha256 of each. Put a REDACTED copy of the Caddyfile (bcrypt hashes replaced) in your evidence folder. Never print or copy a hash or password anywhere else.
4. **The change:** remove only the `basic_auth` block(s) for this site. Everything else in the Caddyfile stays byte-identical (show the diff, hashes redacted). `caddy validate`, then a graceful **reload** (not a container restart). If validate fails, restore the backup and `BLOCKED`.
5. **Verify, as a stranger would:**
   - `curl` with NO credential: `/`, `/health`, `/healthz`, `/site.json` return 200; TLS valid.
   - Real browser with no stored credential (fresh profile or incognito): the site opens without a username/password box; sign in via **Expert** → **Sign in** → Policy Designer Dashboard; open **Synthetic Customer B (demo content)**. Screenshot each.
   - Positive control: show that before the change a no-credential request got 401 (from step 2's reads or a request made before step 4).
6. If step 2 found a deploy script/template that would re-add the gate: do NOT edit the repo. Write it in STATUS under **FOR TUESDAY** with file and line; Tuesday decides the follow-up.
7. Records (project records repo, the way B154/B39 recorded): a CLARIFICATIONS entry (next free C number) quoting Kam's three messages above byte-for-byte, what changed, the backup paths, and how to put the gate back (restore the `.pre-b155` file, validate, reload). A history entry. Note that guide v1.5 still tells readers about a site username/password (COMP-16 holds guide edits: report, do not edit the guide).

## Rules
- Touch only the Caddyfile and the backups. No code, no image, no container rebuild, no account or persona change, no NSG/firewall change.
- Never delete anything. Backups stay. Nothing goes to Paul or any human.
- Secrets: read `4_Credentials/.env` by name only, never print values. gitleaks over anything you commit.
- If anything here disagrees with what you measure, say so in STATUS and act on the measurement only if it is safe and inside these rules; otherwise `BLOCKED`.

## STATUS shape
BLUF (what is live now, the proof) · FOR TUESDAY · FOUND · TESTED (each check, its instrument, its result, its control) · NOT TESTED · Records · last line token.
