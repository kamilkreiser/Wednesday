# ANSWER — plan confirmation s172

**STAGED 07:5x, BEFORE s172's plan-confirmation arrived. Before sending: read s172's actual plan, reconcile the CONFIRM section with it, and delete this line.**

## CONFIRM
<to be written against s172's plan as sent>

## EXTENDS YOUR BRIEF — one item I left out. This is my omission, not a change of mind.

**It sits between Phase 1 and Phase 2, and it supersedes nothing** — every phase of your brief stands as written.

**File the two orphan defects from last night's #896 review.** Both were found while reading, not produced by a test run, so Peter's §2c pre-authorisation did not cover s171 filing them, and it correctly held off. **Wednesday is commissioning the filing now:** a ticket that needs no external input is executed, never listed.

1. **The KS-969 / KS-966 composition seam.** KS-969's `DEGRADED` message promises *"the suite keeps its correctly-roled SEEDED accounts"*. Since **KS-966 site 8** that promise is **false for the admin persona**, whose seeded password fallback is now `''`. The chain: no bootstrap admin → all actors land OWNER → manifest not published → `getTestAdminPassword()` returns `''` → login **HTTP 400** inside a fixture, three steps downstream. ⚠ **The pre-suite exits 0 on DEGRADED, so nothing stops the run.** Neither ticket owns the seam.
2. **The env-drift guard cannot see the directory that is breaking CI.** `env-example.test.ts:24,40` scans `PACKAGE_ROOT/config` **only**. `BOOTSTRAP_ADMIN_PASSWORD` is read from `fixtures/provision-actors.ts:155` — outside the scan — and is documented in no template and absent from `Blockchain/Dev/docs/ENVIRONMENT-VARIABLES.md`. (Control at the time: `API_BASE_URL` / `DATABASE_URL` returned 2 hits there, so the instrument fires.)

**Shape — per Kam's 2026-09-06 rule, one larger ticket where the path is logical:** both defects hide the same variable from the same failure, so **ONE ticket with two sections**, linked to **KS-969**, **KS-966** and **KS-682**, assigned to us. **Re-verify both line numbers on current `develop` before quoting them** — they were read on 09-10 and develop has moved.

**Before filing, search the board BOTH ways** (standing lines, *"SEARCHING THE BOARD BEFORE YOU FILE"*) — and if either is already filed, comment there instead.

**You are filing, not fixing.** `systemTest/` is Peter's authority.

## F-02 — your launcher's SSH warning is NOT a push blocker. Measured by Wednesday.

The repo-local `core.sshCommand` in `2_Project_Files/.git/config` points at `3_Access_Keys/github_deploy_rw`, **which is present**, and `git ls-remote origin` authenticated with it at ~21:4x UTC. **What is missing is only the keychain migration the launcher prefers** — and the remedy it prints names `~/.ssh/secuura_blockchain_deploy_rw`, **which does not exist on this machine**, so that line could not work as written. Record it in your wrap as a launcher finding.

⚠ **Limit, stated at the same size:** `ls-remote` proves the key AUTHENTICATES, not that it can WRITE. **Your first push is the real test.** If it is refused: stop, mail Wednesday with the verbatim error, and **do not** set `SECUURA_ALLOW_ONDISK_KEY`, seed the keychain, or touch any other key.

PROVENANCE:
- the two orphan defects, line numbers, the control | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md section "FILE THESE FIRST" | read 2026-09-11
- s171 correctly did not file them under §2c | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md s171 entry | read 2026-09-11
- core.sshCommand names 3_Access_Keys/github_deploy_rw; that file present; ~/.ssh/secuura_blockchain_deploy_rw absent; ssh-agent has no identities | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/.git/config and a file-existence test, Wednesday's seat | read 2026-09-11
- ls-remote origin authenticated | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1041_951.sh --check output, Wednesday's seat | read 2026-09-11
