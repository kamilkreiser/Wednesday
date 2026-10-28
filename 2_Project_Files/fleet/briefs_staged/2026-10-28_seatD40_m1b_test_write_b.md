## You are Seat D 40th in pane %__ (Wednesday fills the pane id from the launcher's "pane ... added (%NN)" line; if `$TMUX_PANE` differs, trust `$TMUX_PANE` and say so in your plan confirmation; lane Secuura/Blockchain-D, DEPLOY class, SHORT seat): ONE test write on KINTSUGI ONLY, as Kam ruled (card `secuura-m1b-test-write-credential-1028` = b). Reads, one gateway POST, one GET, report, handover, wrap. **No demo. No deploy, no swap, no config change, no restart, no migration, no prune.**

**Routing receipt:** `model: claude-opus-5-5 -- C6 (box rights, credential handling) -- gauge ~77% -- as Seat D 40th`. Launch with `SEAT_MODEL_ENV` (STANDING_LINES 2026-10-27: launch on the routed model, never `/model` afterwards); the launcher must print `[seat-model] launching on <model>`; quote it, with `ps` as the second instrument (D 38th and D 39th could not read the line; `ps` accepted).

**State you inherit (Seat D 39th, HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-28_seatD-39th/HANDOVER.md`, read whole by the drafter 2026-10-28; its "FOR A SUCCESSOR, IF KAM RULES" option (b) is your procedure):** the 2a reads are DONE (0 of 18 kintsugi documents mis-filed by #1756, by two instruments; 0 of 4 on demo). No write has been made on either box and no credential has been read. The #1756 fix is on the box (develop `bd6697e079fc`) and has never been observed live. **Develop has since moved (D 39th's ls-remote: `d531abd5f34b`), but the BOX has not been redeployed: you measure the box, never develop, and build and clone nothing.**

## BLUF
1. **Ruling (Kam, live board 2026-10-28 22:09:01 AEDT; queue ruled_ts 22:09:20+11:00):** card option **b "Use the rotated admin login, acting as a tenant"**. Card detail: the seat reads the admin credential Kam rotated on 27 Oct by path (never printed, never in mail) and creates as super-admin under `X-Tenant-Override`; it proves the fix and shows the audit blind spot; "unmeasured whether the override is honoured for this account (role-case check)". Wednesday's reading told to Kam: **KINTSUGI ONLY; the demo would need Kam's separate word.** Verbatim text below under RULED BY KAM.
2. **You do, in this order:** plan confirmation and WAIT for GO; the role-case check (before any credential is read); pick an override tenant read-only; ONE `POST /api/documents`; the proof reads; report; handover. Nothing else writes.
3. **If the document lands under the DEFAULT tenant (`a0000000-0000-4000-8000-000000000001`), the fix is NOT live: STOP, mail, do nothing further.**
4. **Nothing is posted to any ticket. Nothing goes to Peter or Stuart. No Linear writes.** Results go to Wednesday only.

## QUEUE
1. **Boot and plan confirmation (no box command yet).**
   - FIRST tool call: snapshot `4_Credentials/.launch_preflight_last.txt` WITH its launch stamp (Seat C 25th's catch). Identity from `$TMUX_PANE` against the pane id in line 1.
   - Read `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-m1b-test-write-credential-1028` and confirm `choice='b'`; read `list ruled --undelivered secuura-` and report every line dated 2026-10-28 or later.
   - Read D 39th's HANDOVER whole, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` (the 2026-10-27/28 lines at the bottom: launch-with-model, interpreter count before editing a script, stop only your own PIDs), and `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md` line 26. **Say plainly: this round is reads plus ONE test write, authorised by Kam's card ruling b, not by the deploy grant.**
   - Mail PLAN CONFIRMATION to Wednesday: preflight warnings VERBATIM; the `[seat-model]` line; your reading of steps 2-5, including the **named side effects** (one preview-testnet anchor from the box's own wallet, an `anchor_store` row, a `documents` row, a `documents.create` audit row, and a `DOCUMENT_CREATED` event; expected `action_provenance` +0 and `platform_document_registry` +0, single-tenant by design) and the thread-token flag; and any open point. **WAIT for a Wednesday GO that names Seat D 40th before ANY box command or any credential read.** A mail naming another seat is not for you.
2. **FIRST box check, read-only, BEFORE reading any credential: is `X-Tenant-Override` honoured for this admin account's role?** (D 39th flagged it UNMEASURED.)
   - Gating read, in its own call: `ssh -i 3_Access_Keys/vm_secuura02_kintsugi -o IdentitiesOnly=yes -o BatchMode=yes secuura@20.198.226.148 'bash -s' -- BEFORE kintsugi < 5_Project_History/2026-10-28_seatD-39th/tools/pre_d39.sh`. Want `REVISION_PIN=MATCH40` (`bd6697e079fc`), `.env` HELD, `KS535 stops=0`, vouch secret EQUAL-NONEMPTY, `STATE_THREAD_NFT_ENABLED=UNSET`, demo-service exited. Any other REVISION head is a STOP.
   - Read the code at the pin by `git -C 2_Project_Files show bd6697e079fc:<path>` (read verbs only; D 39th's handover cites `auth/src/routes/auth.ts:302` where the JWT role claim is the raw DB value `role: user.role`, and `api-gateway/src/middleware/auth.ts:515-517` where the override is honoured only on an exact match against `['super_admin','SUPER_ADMIN','SYSTEM_ADMIN','platform_admin']`). Verify those lines yourself and name them.
   - Read the admin account's `users.role` and `status` and `tenant_id` from the kintsugi DB in the M1 read-only pattern (see HOLDS: `default_transaction_read_only=on`, TEMP-table control that must be REFUSED); ids, role, status, tenant only, no email, name, hash or credential column. Compare the stored role string to the exact-case list.
   - **If the role would not be honoured: STOP. Mail `QUESTION`/REPORT: "the write is not runnable as ruled" (override would be ignored; a write would file under the admin's own tenant and read as "fix not live" falsely). No credential read, no write.**
   - Only if the role matches, the second proof comes after login: base64-decode ONLY the JWT payload and print ONLY its `role` and `tenantId` claims (never the token).
3. **Choose the override tenant, read-only:** an EXISTING ACTIVE non-default tenant, from the `@@TENANTS` block of the v3 audit tool (kintsugi: 6 active tenants; the pool is 12 users / 6 tenants), preferably one that also appears in `@@CALLERS`; confirm `tenants.status = 'active'` in the platform DB. Report it by id sha16 only in mail (no slug, no name). If none exists, report "no impact possible by construction": the write is NOT RUNNABLE, STOP.
4. **BEFORE counts** (T0 `2026-10-19T16:48:00Z`, SWAP `2026-10-28T06:08:34Z`): `... 'bash -s' -- 2026-10-19T16:48:00Z 2026-10-28T06:08:34Z BEFORE < 5_Project_History/2026-10-28_seatD-39th/tools/m1b_audit_d39_v3.sh` (v3 only; v1 is broken on jsonb, v2 lacks 6c). Section 4 = counts, section 8 = caller pool. BEFORE values to compare (D 39th, 2026-10-28; re-measure, do not trust):

   | | kintsugi BEFORE |
   |---|---|
   | REVISION | bd6697e079fc, 113,045 B |
   | .env sha16 / bytes | b2b12c5ae67d1a5b / 16,894 |
   | KS-535 mnemonic sha16 / len; blockfrost | 695d09df873ff42b / 158; 142098c9528d0188 |
   | vouch secret sha16 | 9c2fbbcc7351b60b |
   | documents (DEFAULT / other) | 49 (49 / 0) |
   | audit_logs / documents.create | 772 / 24 |
   | anchor_store (confirmed / failed / non-final) | 40 (38 / 2 / 0) |
   | action_provenance | 106 |
   | platform_document_registry (main / platform) | 0 / 0 |
   | tracker | 56 / 055 |
   | api-gateway / originate image | e4f498d363f4 / bb93d9703e4b |
   | demo-service | exited, 19,232 restarts |
   | api-gateway StartedAt | 2026-10-28T06:08:34Z |

   Also record `docker inspect` `StartedAt` and `RestartCount` of `secuura-api-gateway` and `secuura-originate`, rendered with `TZ=Australia/Sydney date -r <epoch>` (UTC and AEDT, a second instrument), and re-read `STATE_THREAD_NFT_ENABLED`. **If the thread-token flag is SET, do not write: QUESTION.**
5. **The credential and the ONE write.**
   - **Credential:** read BY PATH only from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/kintsugi-admin-rotated-2026-10-27.txt` (exists, mode 600, never read by D 39th) into a shell/script variable inside a small python3 urllib script that reads the file itself. **Never echo, never in argv, never into a file, mail, ticket or log; print only statuses and the new id. Never the old published default for `admin@secuura.com`.** Read it only after Wednesday's GO and after step 2 passed. Do not read the demo credential file.
   - Login: `POST <gateway>/api/auth/login` `{"email":...,"password":...}`; token at `data.accessToken`, user at `data.user.{id,role}` (source `auth/src/routes/auth.ts:330, 622, 631, 652`). If MFA is required (`:414`, `:528`) that is a STOP and QUESTION, not a retry.
   - **Gateway URL:** kintsugi's public host is UNMEASURED by the drafter and D 39th. Read the box's Caddy config; the alternative is on the box against `http://localhost:6882` (compose nginx gateway in front of api-gateway). State your pick in the plan confirmation.
   - **The write:** ONE `POST <gateway>/api/documents`, `Content-Type: application/json`, header `X-Tenant-Override: <the step-3 tenant id>`, body exactly `{"title":"M1b test write 2026-10-28 Seat D 40th"}` (use the real run date, keep the fixed words). No documentType (skips the workflow gate, `enforcement.ts:116-117`, `:215-219`); no documentUuid (skips the idempotent path, `documents.ts:680-706`). Through the gateway only, never SQL. Record the HTTP status and the response `id`. A 4xx/5xx is a result; re-send only on Wednesday's word (one write means one).
6. **Proof reads** (read-only session, same TEMP-table control; and `pre_d39.sh AFTER`, `m1b_audit_d39_v3.sh ... AFTER`):
   - (i) `documents.tenant_id` of the new row (found by `external_id`) = the override tenant AND != DEFAULT. **Equal to DEFAULT: the fix is NOT live; STOP, mail, do nothing further.**
   - (ii) owner = the admin (a cross-tenant owner in instrument O, expected).
   - (iii) the P2 audit row records the admin's OWN tenant (class B, uid=true): the known class-B blind spot. **Report it as a finding, not a failure.**
   - (iv) `GET <gateway>/api/documents/<id>` as the same caller with the SAME `X-Tenant-Override`: **200 expected** (the defect's symptom was 201 then 404). Report the status.
   - (v) AFTER counts: documents +1 (49 -> 50, all under the override tenant, DEFAULT stays 49), audit_logs +1, `documents.create` +1, anchor_store +1 with non-final 0 (a non-final anchor row is a FINDING; do not fix), action_provenance +0 expected, platform_document_registry +0 expected.
   - (vi) HOLDS AFTER identical to BEFORE: REVISION `bd6697e079fc`, `.env` sha16 `b2b12c5ae67d1a5b`, KS-535 hashes (stops 0), vouch secret equal, container `StartedAt` and `RestartCount` unchanged, tracker 56/055, demo-service still exited.
7. **Cleanup default: LEAVE and tag.** Report id, tenant (sha16), created_at and the exact title. `POST /api/documents/:id/revoke` (anchors again, a second write with an on-chain side effect) only on Wednesday's word (QUESTION).
8. **REPORT mail** (one, then FINAL): role-case check result and the JWT `role`/`tenantId` claims; override tenant (id sha16); write status and new id; proof (i)-(vi); BEFORE/AFTER table; the class-B finding; what remains unmeasurable (below); holds. Then the handover at `5_Project_History/2026-10-28_seatD-40th/` (evidence in it), **the history entry on Wednesday's word**, and wrap. **Nothing to any ticket, Peter or Stuart.**

## HOLDS
- **No deploy, swap, recreate, restart (`docker restart`, `compose up/down/start/stop/kill`), no `.env` or config change, no migration, no prune, no `docker rm`, no image or tag change, no rsync, no `bootstrap-env.sh`/`start-secuura.sh` on a box.** One POST and one GET only.
- **Every database read in a read-only session** (`-e PGOPTIONS='-c default_transaction_read_only=on -c TimeZone=UTC'`, `psql -X -v ON_ERROR_STOP=1`, `current_setting('default_transaction_read_only')` = `on` in BOTH databases, the TEMP-table firing control REFUSED with "read-only transaction", else STOP). The D 39th v3 tool carries this; use v3 unchanged (copy, never edit in place; new tools `*_d40.*`, refuse overwrite). SELECT only; no INSERT/UPDATE/DELETE by you, ever; no repair of any mis-filed document; no new user, tenant, key or connector row.
- **ADMIN CREDENTIAL (Kam):** the rotated file is read by path only, into a variable, only after Wednesday's written GO, never echoed, never in a file, mail, ticket or log; the old published default is never used or quoted. Any artefact you write is scanned for the password value before commit/handover (a hit is a STOP). You touch no admin or user row.
- **KS-535 ABSOLUTE:** wallet/blockfrost hashes (sha16 only) are not touched; kintsugi mnemonic `695d09df873ff42b` len 158, blockfrost `142098c9528d0188`. A moved hash is a STOP.
- **Kintsugi only.** Demo is Stuart's UAT: no demo command, no demo credential read, no demo write, without Kam's separate word relayed by Wednesday naming Seat D 40th.
- `secuura-demo-service-crash-loop` (Kam 2026-09-05): `docker stop` only; do NOT `docker start` it.
- Production, money, external comms, irreversible: pause for Kam. No `az`, `--no-verify`, force push, `--admin`. **NO git push this round** (a push need is a STOP and QUESTION). `2_Project_Files` is READ-ONLY; code reads use `git -C 2_Project_Files show bd6697e079fc:<path>`.
- **PID-only kills** (never `pkill`/`killall` by name). Never edit a running script (count interpreters with `comm` bash and args naming it; `lsof`). Exit codes on their own line (`cmd > out 2>&1; rc=$?`; zsh `$pipestatus[1]`). zsh does not word-split a scalar. Never `cd`; absolute paths. A gating read is its own call. Greps over text that may differ by case use `-i` with a positive control. Ssh remote args are re-parsed by the remote shell: labels `[A-Za-z0-9._:-]`. A private TMPDIR must be SHORT (`/tmp/seatD40`). `curl -I` writes headers into the `-o` file. Arm any watcher at the 7,200,000 ms maximum and re-arm before it lapses. Rotate in the 80-90 band, handover first.
- **Not covered:** any second write; any `PUT/PATCH/DELETE`; `POST /api/batch/certifications` (files under the default tenant regardless, KS-1084; never the test route); any attempt to make a DB or pooler fail; any look at container filesystems beyond a read.

## PARTITION
**Yours:** kintsugi through the project's tooling and your own folder `5_Project_History/2026-10-28_seatD-40th/` (tools, evidence, mail log, handover) and the history.md entry on Wednesday's word. **The one write** is the single document the gateway creates into kintsugi's database. **NOT yours:** demo; the board seat (Seat G), triage and build seats; Peter's merges; `2_Project_Files`; Linear. **Shared inbox:** Wednesday's mail to you arrives at the project inbox `secuura-blockchain@agentmail.to`, shared with other live Secuura seats (pane list: read it at your launch; the drafter did not). You touch none of their files, worktrees, containers or the push lock (you push nothing). **A GO is acted on only if it names Seat D 40th.** Read the inbox at start and at every step boundary. No Docker on the Studio.

## UNMEASURED (what the drafter could not establish)
- **Everything on kintsugi today.** The drafter touched no box and read no credential: the admin account's stored role, whether the override is honoured, the REVISION head, hashes, counts, StartedAt/RestartCount, the thread-token flag, the tenant pool.
- **Kintsugi's gateway URL** (Caddy config unread); whether the admin login needs MFA; whether the 6 active tenants include one usable as an override target.
- The audit row's tenant for the override case is expected to be class B (admin's own JWT tenant) per code reading by D 39th; not measured.
- Whether the registry write stays 0 (expected, by design: `MULTI_TENANCY_ENABLED=false`, `verification.ts:526`, `db.ts:372-379`).
- The drafter did not re-run `list ruled --undelivered secuura-`; the seat does.
- The earlier 18 documents are NOT attributable by this write; it proves the fix live only.

## RULED BY KAM
- Card `secuura-m1b-test-write-credential-1028` = **b "Use the rotated admin login, acting as a tenant"** (ruled_ts 2026-10-28T22:09:20.035016+11:00; live board 22:09:01 AEDT). Wednesday's reading: kintsugi only; demo needs Kam's separate word.
- Card `secuura-1756-misfiled-docs-what-next-1028` = b "Measure first" (live board 2026-10-28 18:12:56 AEDT): results to Kam before anything to Peter or Stuart.
- Admin credentials HOLD (Seat B 69th rotated `admin@secuura.com` on both boxes): as in HOLDS.
- Kam's October deploy grant (`EXPIRING-GRANTS.md` line 26) covers deploy rounds; it is not the basis for this round.

RULED BY KAM, NOT YET IN AN ARTEFACT
- **Verbatim, live board 2026-10-28 22:09:01 AEDT:** "Decision secuura-m1b-test-write-credential-1028: b — Use the rotated admin login, acting as a tenant". Card option b text (read by the drafter via `decision_queue.sh show`, 2026-10-28): "The seat reads the admin credential you rotated on 27 Oct by path (never printed, never in mail) and creates as super-admin under X-Tenant-Override. Proves the fix and shows the audit blind spot; unmeasured whether the override is honoured for this account (role-case check)." The card's default was c (no write); it was overridden by this ruling. The repair of any mis-filed document remains Kam's decision after he sees numbers.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The four held containers stay held (`pgbouncer`, `nginx-gateway`, `demo-service`, `demo-overlay`) (2026-10-19T18:56:34Z).
- D 38th's "no test write" is LIFTED for the single kintsugi document of this round only, by Kam's card ruling above.
- Cleanup = leave and tag; revoke only on her word (D 39th plan, GO 07:57:26Z). Path/status split YES; thread-token flag SET = QUESTION (D 39th plan GO).
- Seat D reads, builds, swaps and reports; it opens no PR and edits no source. Notices post only on Wednesday's word (none this round).
- **Mail discipline (Secuura):** to `wednesday-agent@agentmail.to` (not Tuesday), subject `[Secuura/Blockchain -> Wednesday] <topic>` (the `-D` pane tag; name `Seat D 40th` on body line 1), via a re-keyed `send_d39.py` -> `send_d40.py` (assert the substitution target exists, size floor, refuse overwrite; grep the new tool case-insensitively, excluding comments, for `d33`..`d39`, `seatD-39th`, `bd6697e079fc` outside the pin line, and stale subjects: a tool can be correctly named and still measure last round), NO CC to Kam, read-back identical, **no secret values, no tenant slugs, no emails, no document titles beyond the fixed test title; tenant and user ids as sha16 only.** Milestones: PLAN CONFIRMATION, REPORT, FINAL. Blocked: `QUESTION: <topic>` (Context 1-3 lines + paths / one Question / Meanwhile / Needed-by); after ~15 minutes without an answer proceed on the safest reading UNLESS approval-class (the credential read, the write, the revoke, anything demo ALWAYS pause). STATUS every ~20 minutes inside a step over 20 minutes.

## STOP and mail on
A box `REVISION` head other than `bd6697e079fc...`; `.env` hash or tracker moved; a KS-535 hash moved; `StartedAt` or `RestartCount` moved; the read-only guard not on or the TEMP-table control succeeding; **the admin role not honoured by the override (before any credential read)**; MFA required; no active non-default tenant; thread-token flag SET; **the test document filed under the DEFAULT tenant (fix not live)**; a non-final anchor row you cannot explain; any step that would need a second write or a demo touch; any hit when scanning your artefacts for the credential value.

## STILL OPERATIVE (from D 39th, for a successor)
1. `audit_logs.details` is jsonb: use `->>`, never a text regex.
2. The live schema is not the migration file (no owner FK on live `documents`): read `pg_constraint` before citing a constraint.
3. audit_logs pairs to a document by time only (resource_id NULL for a create).
4. `STATE_THREAD_NFT_ENABLED` and `SIMULATE_ANCHORING` were UNSET on kintsugi (D 39th): re-read both.
5. The registry-empty "finding" was RETRACTED (by design); no ticket.
6. Rollback stamps `pre-20261028k8` / `pre-20261028d8` and their idfps stay on the boxes untouched.

PROVENANCE:
- Kam's ruling `secuura-m1b-test-write-credential-1028` choice b, ruled_ts 2026-10-28T22:09:20.035016+11:00; card title, options a/b/c, default c, option b text (read by the drafter 2026-10-28 (the 22:09:01 AEDT live-board time and verbatim line are from the launching instruction) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-m1b-test-write-credential-1028` | read 2026-10-28
- Procedure for option (b), tool paths, gateway IPs (kintsugi 20.198.226.148), BEFORE table, role-case finding (`auth.ts:302`, `middleware/auth.ts:515-517`), `documentWriteRoles.ts:37`, login route lines, side effects, holds, proofs, tenants (6 active kintsugi), pools (12 users / 6 tenants), credential file path and mode 600, never read (read whole by the drafter 2026-10-28 (code line numbers are D 39th's, not re-read by the drafter) | `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-28_seatD-39th/HANDOVER.md` | read 2026-10-28
- Develop moved to `d531abd5f34b`, boxes still on `bd6697e079fc` (the drafter ran no ls-remote) | same HANDOVER, D 39th's `git ls-remote` 10:2xZ 2026-10-28 | read 2026-10-28
- Brief shape, HOLDS, mail discipline, STOP list, PARTITION, shared inbox rule (read whole 2026-10-28; its other-seat pane list (R 6th, X 3rd, ...) is NOT carried because it was 18:3x and stale) | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-28_seatD39_m1b_measure_first.md` | read 2026-10-28
- Standing lines (launch on routed model; PID-only kills; interpreter count before editing; launch preflight in FIRST tool call; pane id in the first line; short TMPDIR; re-keyed tool checked for previous round's ids) | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` bottom lines | read 2026-10-28
- Ordinal: `/usr/bin/grep -i -c 'Seat D 40th'` over `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` = 0 and over `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/` (grep -r -c, non-zero filtered) = no file; positive control `'Seat D 39th'` over history.md = 1 (this brief itself is the first file to name D 40th; the briefs_staged control was not separately run for `Seat D 39th`) | those paths | read 2026-10-28
- Routing receipt model `claude-opus-5-5`, C6, gauge ~77% | the launching instruction from Wednesday (not independently read from `models_latest.json` by the drafter) | read 2026-10-28

- KS-535 state Done, 6 comments, newest 2026-08-02T00:44:49Z; named ONLY as the label of the standing wallet-isolation hold, NOT queued work | Linear GraphQL issues(includeArchived:true, number 535, team KS), read by Wednesday at 18:4x for the D 39th brief | read 2026-10-28
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-28 22:12
