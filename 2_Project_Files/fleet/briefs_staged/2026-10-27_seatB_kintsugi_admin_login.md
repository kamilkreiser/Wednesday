## You are Seat B (lane Secuura/Blockchain-B, INVESTIGATION, read-only): find out why Stuart cannot log in to kintsugi as platform admin, and which platform-admin username(s) actually exist there

**Seat number:** derive "B <N>th" from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest Seat B row + 1). Establish which seat you are from the process table (your pane is `Secuura/Blockchain-B`), never from which mail looks like yours.

**Shared inbox:** `secuura-blockchain@` is shared with **Seat D 34th** (pane `Secuura/Blockchain-D`, %19), which is DEPLOYING develop ec3313a80440 to **DEMO** right now. Mail naming D 34th is not yours. **You do not touch demo at all.** Kintsugi's deploy finished 2026-10-26T18:49Z (D 34th), so kintsugi is quiet and safe to READ.

**Model line:** Opus, routing row C3 (a credential surface; read-only measurement first). Gauge 7d 26% at the brief.

## BLUF
1. **Kam's priority this morning.** Stuart ran his provisioning-key script against kintsugi and the platform-admin login was refused. Answer two questions **by measurement**: (a) **which platform-admin account(s) exist on kintsugi** (email, status), and which one is meant to be Stuart's; (b) **why the login fails**: wrong password, suspended or unseeded account, lockout, or something else.
2. **READ-ONLY.** No write to the database, `.env`, any account, any container. No rebuild. No password reset. Any fix is a credential change on a running system, and that is Kam's call: you PROPOSE it, smallest and reversible first, with its blast radius.
3. **No password value goes anywhere:** not into a mail, a ticket, a note, a log, your pane or a command line echo. Not even a hash. Presence, length and match/no-match are the only facts about a secret you may report.
4. **Nothing to Stuart or Peter.** No ticket comment and no extranet post. Wednesday gives your findings to Kam, and Kam answers Stuart.

## THE FAILURE (Kam pasted it into Wednesday's terminal 2026-10-27 ~06:2x AEDT, from Stuart's message of 2026-10-26 22:01 AEDT = 11:01Z)
```
./commission-provisioning-key.sh --k-url https://kintsugi.secuura.net --name "dev-ps provisioning key 2026-10-26" --admin-email admin@secuura.com
login failed: {"code": "UNAUTHORIZED", "message": "Invalid email or password"}
If this platform-k was just built from an untouched Blockchain/Dev/.env, its platform admin is NOT seeded:
since KS-966 the seeder writes admin@secuura.com suspended unless ADMIN_USER_PASSWORD is set AND
ALLOW_DEFAULT_SEED_PASSWORDS=true, both in that .env BEFORE the K build. K logs it as
"Demo user seeding skipped". (PS-855; docs/stack_slots_how_to.md section 5)
```
Stuart wrote "dont worry about it till tomorrow", which means today.

## WHAT WEDNESDAY KNOWS, AND HOW SURE (provenance, every line)
- 2026-10-13: Seat D 19th set up admin@secuura.com for Stuart on kintsugi. Record: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/_quarantine_2026-10-13/kintsugi-admin-for-kam-2026-10-13.txt` (path from Wednesday's 2026-10-26 21:49 note; Wednesday did not open the file).
- Candidate password: `ADMIN_USER_PASSWORD` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.kintsugi_dev_credentials` (dated 2026-08-20). **UNVERIFIED: no login has ever confirmed it.** Kam's own admin is in the Secuura `.env` as `KINTSUGI_KAM_ADMIN_*` (key names only; values not read).
- Kam sent Stuart a password himself on 2026-10-26 ~21:57 AEDT. **Which value he sent is UNMEASURED**; it is believed to be the candidate above.
- Kintsugi deploys around that time: D 32nd at 07:55Z on 10-26 (before Stuart's 11:01Z attempt), D 33rd at 14:32Z, D 34th at 18:49Z (both after). **Unmeasured: whether any deploy re-ran the seeder or changed the admin row.**

## QUEUE (in order, all read-only)
1. **Read the code first.** Find the login route, the admin seeder (KS-966) and any failed-login lockout or throttle, in the source at develop ec3313a80440 (your own worktree or `git show`). **Know the lockout rule**, and report the account's lockout state: Stuart's failures may already count against it.
2. **Read kintsugi's state:** the users table rows with a platform-admin role. Report email, status/suspended, any lockout or failed-attempt fields, created_at, updated_at, and password-changed-at if the schema has it. Use SELECT only, through the box's own psql in its container. Never select the hash column into output.
3. **Did the seeder run on kintsugi?** Check the services' logs since the last rebuild for "Demo user seeding skipped" or its success line, and whether kintsugi's `.env` HAS `ADMIN_USER_PASSWORD` and `ALLOW_DEFAULT_SEED_PASSWORDS` (presence and the boolean only; never the password value).
4. **Does the candidate password match?** Do an OFFLINE compare only, which carries no lockout risk and writes nothing: inside the container, run the product's own hash-verify function (bcrypt/argon2, whichever the code uses) against the stored hash, and print only `MATCH` or `NO MATCH`. Feed the candidate on stdin, never as a command-line argument and never through a file on the box. **No live login attempt in this round**, because a failed login writes counters and could lock the account. Do the same check for Kam's own `KINTSUGI_KAM_ADMIN_*` account.
5. **Propose the fix** (do not apply it): the smallest reversible change that gives Stuart a working platform-admin login. Name what it changes, what it touches, how to undo it, and whether it survives the next deploy. KS-966's seeding rule is the project's own design: say whether the fix works with it or around it. If a new password is needed, the proposal says it is generated on the box or into the Secuura `4_Credentials/` file (0600) and reaches Stuart only via Kam.

## REPORT
- One **STATUS mail** to Wednesday, BLUF first, with these headings: **USERNAMES** (every active platform admin on kintsugi, by email, with status), **WHY IT FAILS** (the measured cause, or the candidates still standing and what would separate them), **PROPOSED FIX** (as above), and **UNMEASURED**. Each finding carries FOUND / TESTED / HOW, controls included. If the users query returns zero rows, run a control that must return rows, such as the total user count.
- A handover at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-27_seatB-<N>th/HANDOVER.md`, plus your history.md row. Then wrap.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-10-27 ~06:2x (terminal): *"keep going with the tickets. prioritise the following [Stuart's login failure] and let me know the user name (admin for Stuart)"*. That is this brief.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-10-26 21:49: the kintsugi admin password is never pasted into chat or mail; Kam sends anything to Stuart.

## HOLDS
- Read-only on kintsugi. Do not touch demo (D 34th is deploying it). No rebuild, no `.env` edit, no DB write, no account change, no password reset.
- Client-facing communication is ticket comments only, and **none in this round**. The extranet is not a channel.
- Never delete; never edit a running script; no `kill` by name; your own worktree only; never write into another seat's tree.
- A doubt is a QUESTION mail (one question per mail) with a default. Approval-class items (any write to the box) always wait.

PROVENANCE:
- Stuart's error text and script command | Kam's paste into Wednesday's terminal (Stuart's message 2026-10-26 22:01 AEDT) | read 2026-10-27
- admin@secuura.com set up for Stuart 2026-10-13 by Seat D 19th; candidate password key ADMIN_USER_PASSWORD in .kintsugi_dev_credentials (2026-08-20, unverified) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-10-26.md (Wednesday's tree) line 188 (Wednesday's 21:49 note) | read 2026-10-27
- Kam sent Stuart a password ~21:57 AEDT | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-10-26.md (Wednesday's tree) line 190 | read 2026-10-27
- kintsugi deploys 07:55Z (D 32nd), 14:32Z (D 33rd), 18:49Z (D 34th) on 2026-10-26 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md (Wednesday's tree) handover blocks + D 34th DEPLOYED mail 18:49Z | read 2026-10-27
- D 34th deploying demo now | D 34th STATUS mail 19:00Z + your own 5_Project_History/2026-10-27_seatD-34th/evidence/heartbeat.demo.d4.d34.txt (batch 8/17 at 19:09:25Z) | read 2026-10-27
- "reversible" in QUEUE step 5 is a property you MEASURE, not one Wednesday asserts: I have not established the blast radius — establish it before acting (and no fix is applied in this round anyway) | unmeasured by Wednesday | read 2026-10-27
- KS-966 state In Progress, not completed, last comment 2026-09-11T11:35Z; title "Retire the published SYSTEM_ADMIN credential (Kam: rotate-properly)". So the default-admin seeding was retired DELIBERATELY: a proposed fix must not re-enable a published default password (ALLOW_DEFAULT_SEED_PASSWORDS with the old value) — read KS-966 whole before proposing | Linear ticket KS-966 | read 2026-10-27

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-27 06:22
