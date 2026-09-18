Seat A 12th successor (Secuura/Blockchain), from Wednesday

⚠ TWO SEATS SHARE THIS INBOX TODAY. This brief is for **seat A 12th** (the kintsugi rebuild). A second seat, **Seat B 2nd**, will be launched after your plan confirmation lands; its brief's subject names "Seat B 2nd". A mail naming Seat B is not yours; do not act on it. Seat B writes code in its own worktrees; you deploy and write NO product code, so your paths do not overlap.

## BLUF
**One job: the KINTSUGI REBUILD to develop as it stands, today (Saturday 19 Sep AEST), ending with #1038's Redis deploy action run VERBATIM and #1045's read-only settings check.** Kintsugi only, never demo. Kam is away Sat 19 + Sun 20; his standing words are quoted below. You merge nothing and raise nothing.

## ITEM 0: boot, before any write
- Read your predecessor's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-11th-successor-2026-09-18.md` (FINAL STATE at the top; the rebuild section is quoted from my brief to it).
- **develop has MOVED since that handover and I do not know what landed.** The 11th left it at `52df64f844b7b3aabf7df57284c5f4e2ab8a07a2`; my `ls-remote` at 06:04 AEST today reads `59412d0575dff3243f5f0ccd1e50608ddb920d6c`. UNMEASURED by me (I hold no client git identity): read `git log --oneline 52df64f84..59412d057` (or whatever develop is when you start) in your first turn and put the list in your plan confirmation. If anything in it adds a MIGRATION, a new compose service, or a new required env var, STOP and tell me before Phase 0.
- **Measure kintsugi's current commit yourself**; the 11th's handover says `a105cd32b` (its claim, not re-derived by me).
- Send me your plan confirmation (QUESTION mail, topic `plan confirmation`) before the first write to kintsugi.

## QUEUE, in order, every step gated on the previous step's rc
**1. THE KINTSUGI REBUILD** (Stuart's dev box, ~2 h). Build to develop AS IT STANDS when you start. Run the 9th's runbook exactly: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-18_seatA-9th/KINTSUGI-REBUILD-STATE.md`. Phase 0: NEW rollback tags named for today (the `pre-20260918` set already exists; verify BY NAME, 33 build services, 36 compose). `-p dev --profile phase2`. **Never `--remove-orphans`.** `--no-deps` on named services (postgres stays up). A phase-state file on disk; rotate only at a phase boundary. **Baseline `secuura-demo-service` BEFORE** (it crash-loops pre-existing without `DEMO_SERVICE_ENABLED`; a CHANGED failure mode is a stop). Verify by BEHAVIOUR, not by steps. Expect the KS-1245 smoke red (#1037's `/health/deep` shows degraded) and record it as the test lagging.
**2. THEN #1038's DEPLOY ACTION, VERBATIM, the most important line in this brief:** *after the new api-gateway image is live on EVERY replica, per Redis: `redis-cli -u "$REDIS_URL" TTL secuura:gateway:notif:platform-settings`. If > 0: `PERSIST secuura:gateway:notif:platform-settings` and re-read -1. If -2: the allow-list has ALREADY failed open, so re-enter the connector integrations in admin settings and confirm TTL = -1. If -1: nothing to do.* Run it AFTER every replica is on the new image, never before (an old replica's next admin write re-arms the TTL). Mail me the TTL you read BEFORE and AFTER.
**3. #1045's READ-ONLY settings check (the batch gate's N45-4, kintsugi ONLY):** `redis-cli -u $REDIS_URL GET secuura:gateway:notif:platform-settings` (in no-Redis mode, `GET /api/v1/admin/settings` as SYSTEM_ADMIN). Classify the `integrations` container (array / object / other) and each connector's `config.allowedDocumentTypes`. Change nothing; mail me what you read. An OBJECT container means the allow-list is already failing open (KS-1231).
- **SSH:** the NSG admits `157.211.46.215/32` only and the address is dynamic. If SSH fails, STOP and mail me the address you egress from. **Do not touch the NSG yourself.**
- **KS-1256 (High) is NOT fixed by this rebuild or by #1038.** The allow-list still fails open on a Redis close/error/eviction. Do not describe the rebuild as closing it.
- At wrap: the rule-7 comments (KS-485 @peter, KS-772 @stuart.jamieson) naming what kintsugi now runs, mentions verified.

## HOLDS: do not do these
- **Nothing to demo.** Kam 10:27: demo takes only kintsugi-proven work, and only after Peter's nod.
- **No merges, no PRs, no product code.** Seat B raises code; you deploy.
- **KS-1250 and KS-1175 are Kam's.** Not yours in any form.
- **No messages to humans** beyond the rule-7 ticket comments.
- Never `--no-verify`, never a force-push. **Never delete. Quarantine.** Never enter `5_Project_History/quarantine/`. `/api/seen` is never called.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-09-18 10:27, panel, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."*
- 2026-09-18 14:14, panel, verbatim: *"I'm going to be away for the next two days, so please keep going with tickets and activity while I'm away. Push merge and deploy whatever is ready. Whenever it's ready."* Wednesday's reading, said back to him and acknowledged at 14:16 with no correction: kintsugi only, not demo; the signature classes still pause.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-18 (the 11th's brief): the rebuild is Saturday, kintsugi only; #1038's action verbatim; KS-1256 is not closed by it.
- 2026-09-18 (the 11th's GO for #1045): its read-only settings check goes into the rebuild, never run on demo.

## What Wednesday owes you
- An answer to your plan confirmation and to anything you ask; a receipt for your TTL/settings mail.

PROVENANCE:
- origin develop = 59412d0575dff3243f5f0ccd1e50608ddb920d6c | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 06:04:40 AEST, YOUR checkout | read 2026-09-19
- the 11th's final develop 52df64f84, kintsugi a105cd32b, the #1038 action text, the #1045 check text | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-11th-successor-2026-09-18.md, YOUR project | read 2026-09-19
- KS-1256 Backlog P2 unassigned; KS-1250 Backlog P4; KS-1175 Backlog P2; KS-1245 Backlog P3, 0 comments; KS-1231 Backlog P2 | Secuura Linear GraphQL, read-only query run by Wednesday 06:05 AEST (17 of 17 returned) | read 2026-09-19
- the rebuild runbook exists (12011 bytes) | ls of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-18_seatA-9th/KINTSUGI-REBUILD-STATE.md, 06:04 AEST, YOUR project | read 2026-09-19
- KS-485 Todo P2 (the rule-7 stream for Peter, last comment 2026-09-18T07:01Z); KS-772 Todo P2 (the rule-7 stream for Stuart, last comment 2026-09-18T07:01Z) | Secuura Linear GraphQL, read-only query run by Wednesday 06:06 AEST (2 of 2 returned) | read 2026-09-19
- weekly usage 44%, under the 90% cap | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check, 06:03 AEST, my project | read 2026-09-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-19 06:06
- One job (the rebuild + two post-deploy reads); no merge, PR or code anywhere in the queue.
- develop's move is stated as UNMEASURED with the instrument that closes it; kintsugi's commit is the handover's claim, to be measured.
- Demo appears only under HOLDS; KS-1250/KS-1175/KS-1256 appear only as holds/awareness.
- The shared-inbox warning names Seat B 2nd, which launches after this seat's plan confirmation.
