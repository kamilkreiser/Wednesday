## You are Seat D 33rd (lane Secuura/Blockchain-D, DEPLOY): deploy develop `5f689991861b3b9be295797a437ef18b6f55a492` to KINTSUGI, verify, then DEMO, then stop `secuura-demo-service` on both boxes as the last step

**Why you exist:** Seat D 32nd left both boxes on develop `28e2d27de337` (the #1690 merge) and wrapped. Develop has since gained 22 first-parent squashes, all small. You hold box rights; no other Secuura seat does. **No merge, no PR, no secret change, no source edit in this round.** The EMITTER_SIGNING_SECRET is already set on both boxes by D 32nd (do not touch `.env`).

**Decisions already made. Not yours to reopen; a doubt is a QUESTION, not a deviation.**
1. **AUTHORITY:** Kam's October deploy grant `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md`, extended "until further notice" 2026-10-19 18:22:57 AEDT (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md`): kintsugi first and verified, then demo, no card per deploy. You re-gate nothing.
2. **demo-service stop** is Kam's 2026-09-05 ruling (card `secuura-demo-service-crash-loop`): `docker stop` only, `docker start` is the undo, nothing else. Extended to both boxes by Wednesday 2026-10-26T10:54:45Z. Every deploy recreates it (`restart: unless-stopped`), so the stop is the LAST step on each box.
3. **Model line:** Opus, routing row C6.

**Read FIRST, whole:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-26_seatD-32nd/HANDOVER.md` (tools in its `evidence/tools/`, stamps used, KS-535 figures, the three instrument defects, the demo-service stop), then `.../2026-10-26_seatD-31st/HANDOVER.md` (BusyBox grep trap 5.1), `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/DEPLOY-BLOCKERS.md`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` (read-only).

## BLUF
1. **Target is develop `5f689991861b3b9be295797a437ef18b6f55a492`, valid ONLY if your A1 re-pin reads exactly that.** A moved develop is a STOP and QUESTION: this brief names a SHA.
2. The delta is 22 squashes, 60 files, **zero `.sql`, no lockfile, no `packages/shared` source, no anchoring or originate runtime code**. Runtime-relevant: api-gateway (3 files), vc-issuer (1 file), `.dockerignore`, two `package.json`. REBUILT counts are measured per box, never assumed.
3. Kintsugi fully verified, then demo. D 32nd's builds took about 2 h 20 m per box. Heartbeat file.
4. Done = tested + works + deployed, evidence on the ticket.

## THE DELTA (Wednesday read it in her cache clone; you re-derive it against each box's REVISION)
Range `28e2d27de337..5f689991861b`, `git log --first-parent`, 22 squashes (PR / ticket): **runtime** #1712 KS-1731 (credential list orders `created_at DESC, id DESC`), #1700 KS-1649 (portal states the connector key rate limit), #1702 KS-1635 (dead `meetsVerificationLevel` dep removed), #1694 KS-1289 (`.dockerignore` excludes nested `__tests__`), #1693 KS-1391 (issuer `test` script); **tests/tooling/docs only** #1711 KS-1735, #1714 KS-1729, #1710 KS-1551, #1709 KS-1554, #1708 KS-1728, #1706 KS-1714, #1707 KS-1636, #1705 KS-1578, #1703 KS-1602, #1704 KS-1566, #1701 KS-1713, #1689 KS-1716, #1697 KS-1527, #1695 KS-1513, #1692 KS-1560, #1699 KS-1524, #1698 KS-1548.
Files, grouped (60): api-gateway 21 (18 tests; runtime: `src/index.ts`, `src/routes/verification.ts` [15 lines removed], `src/docs/developer-portal.html`); `Blockchain/Dev/scripts` 12 (tooling and baselines, not in images); security 5 (tests + `tsconfig.test.json`); vc-issuer 4 (3 tests; runtime: `src/repositories/credentialRepo.ts`, 1 line, KS-1731); `packages/shared` 2 (BOTH under `src/__tests__`, no source); `frontend/issuer` 2 (`package.json` gains a `test` script, plus a test); `systemTest` 6; originate 1 (a test file only); m365-integration 1 (`tsconfig.test.json`); auth 1 (test); `.dockerignore` 1; root `package.json` 1 (`check:test-types` adds two services); docs/CLAUDE.md 3.
- **`.sql`: NONE** (Wednesday, 22:31: `git diff --name-only 28e2d27de337 5f689991861b -- Blockchain/Dev/migrations` = 0 lines; FIRING control: the same path filter over `32964477f~1..5f689991861b` prints `055_ks1557_...sql`). Re-derive it in YOUR clone against each box's REVISION with your own firing control. Any `.sql` in YOUR delta is a STOP and QUESTION.
- **Rebuild scope:** no lockfile changed (control: `package-lock` filter over `1ae6f17d19a8..5f689991861b` reads 33, so the filter fires). `packages/shared` has test files only, but `.dockerignore` now excludes `**/__tests__`, which changes the build context of every service; the `package.json` edits (root, issuer) may cache-MISS an `npm ci` layer. Do not predict a count: build all, verify with `verify_build`.
- **Emitter hop (B7 order):** NOT touched. No file under `services/anchoring`; `services/originate` has one test file, no runtime code. **Keep D 32nd's order** (originate immediately before anchoring, api-gateway LAST). Re-check this with your own grep of YOUR delta for `anchoring|originate|emitter` outside `__tests__`; a runtime hit there is a QUESTION before swapping those two.
- Fix strings (derive exact strings from the diff; `fixes_live_d32b.sh` searches `/app` AND `/shared/dist`, keep its shared-side control): KS-1731 ordering in vc-issuer `credentialRepo`, KS-1635 verification route, KS-1649 portal sentence. Each 0/0 BEFORE the swap, running>=1 / rollback=0 AFTER.

## QUEUE
### A. PIN, DELTA, PRECHECK
- **A0.** Establish your seat from `@cockpit_name`. Re-run `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-`; report any line dated 2026-10-26 or later. Read the inbox for Wednesday's messages (it is shared; see PARTITION).
- **A1. Re-pin** immediately before building: `git ls-remote origin refs/heads/develop`. Must read `5f689991861b3b9be295797a437ef18b6f55a492`. Anything else: STOP and QUESTION.
- **A2.** Deploy clone `deploy-clones/seatD33-5f689991861b`, `--single-branch --branch develop`, repo-local `core.sshCommand` with keepalive, `core.hooksPath=.githooks`; `git rev-parse HEAD` asserted equal the pin. Never `2_Project_Files` (KS-907). `deploy-clones/seatV2-5f689991861b` is Seat V 2nd's: read-only to you, never reused.
- **A3. Delta from git** against each box's own `REVISION` head (expected `28e2d27de337` on both, UNMEASURED: you read it): `git log --first-parent`, `git diff --name-only`, grouped to services; confirm it matches THE DELTA above (22 / 60 / 0 `.sql`) or report the difference. A box REVISION that is not `28e2d27de337` is a STOP and QUESTION.
- **A4. Migration state, read-only, per box:** tracker 56 rows / max 055 / no 056 (D 32nd's figures); a change is a STOP.
- **A5.** DEPLOY-BLOCKERS rows, KS-1079, KS-1730: reads only; a fix is a QUESTION.
- Mail **STATUS A** before any box write.

### B. KINTSUGI
- **B1. Phase 0** from RUNNING ids (`phase0_d32.sh` re-keyed), an UNUSED stamp read on the box (stamps already used: `pre-20261026k1`, `pre-20261026d1`, `pre-20261026k2`, `pre-20261026d2`; take `k3` / `d3` only after confirming absent on the box), refuse empty fingerprint `e3b0c44298fc1c14`. Rollback: re-tag `:<stamp>` to `:latest`, then `docker compose -p dev --profile phase2 up -d --no-deps --force-recreate <svc>`. **NEVER `-f` (kintsugi has a `docker-compose.override.yml`; demo has none). NEVER `--remove-orphans`.** Stack dir `/home/secuura/secuura/Dev`, project `-p dev`. Preserve `.env` untouched; assert its hash unchanged before and after (no edit this round). Keep your own `.env` copy outside the stack dir.
- **B2. rsync** the clone to the stack dir with `--checksum` (not size+mtime), exclude list `node_modules .git dist output .env .env.local`, no `--delete`. Verify: sends equal `git diff --name-only` under `Blockchain/Dev` (`comm` 0/0/N) with a wrong-range control that overlaps and fires.
- **B3. Build everything BEFORE any swap**: batches of at most two, load gate 6, 12,000 MB disk floor (`batch_build_d32.sh`), detached on the box with a done-marker and one background job whose exit re-invokes you (quoted heredoc for waiter bodies). Use `wait_build_d32b.sh` (it counts processes by `comm`, never infers a stall from unchanged rows). Heartbeat file path named in every STATUS (batch n of N, free disk). No prune. Demo has 3,893 MB RAM: load-gate waits are expected there.
- **B4. NEW-ID** with `verify_build_d32.sh` against the pre-build `:latest` snapshot, never the exit code. `migrations` rebuilt, NEVER run. `demo-service` held. A service with UNCHANGED id needs no swap; prove it from the delta (D 32nd's frontend case) rather than assume it.
- **B5. KS-535, ABSOLUTE.** sha16 only, BEFORE the first swap and AFTER the last. **Figures are from D 32nd's handover (read 2026-10-26), NOT from the old D 32nd brief**: kintsugi mnemonic `695d09df873ff42b` len 158 and blockfrost `142098c9528d0188`; demo mnemonic `12ea1a07174c3f50` len 144 and blockfrost `1ed6121f284091df`; `CARDANO_NETWORK=preview`, `SIMULATE_ANCHORING` absent. Kintsugi's `695d09df873ff42b` must NOT appear on demo. A moved hash is a STOP. Use `ks535_now_d32.sh`; keep its hasher controls.
- **B6. Swaps** (`swap_driver_d32.sh` order; derive the set with `swapset_d32.py`): REBUILT minus the held four minus `migrations`, api-gateway LAST, originate immediately before anchoring. Before originate/anchoring read `anchor_store` for non-final rows (read-only; baseline kintsugi 33 / non-final 0, demo 339 / non-final 0; a non-final row is a QUESTION). Held: `pgbouncer`, `nginx-gateway`, `demo-service`, `demo-overlay` (recreating it RUNS it). Infra `StartedAt` before and after; movement is a STOP. The four held stay held.
- **B7. Smoke.** (a) anchoring logs `[emitter-guard] ACTIVE`, 0 `FAIL-CLOSED` (any FAIL-CLOSED is a STOP and you may roll those two back unasked); originate cannot emit that line (D 32nd proved `emitter-guard` is absent from its source and image; its assertion is `[gateway-provenance] ACTIVE`): read the substitute, say so. (b) The connector-initiated labelled create stays UNMEASURABLE (Wednesday's route (3) of 08:03:02Z: `api_keys` has 0 rows on both boxes); create NO key, run NO labelled create. Record `action_provenance` before and after: baseline kintsugi 90, demo 4,782; a deploy must move neither. (c) `/health/deep` ready:true 5/5, `/api/<nonexistent>` 404, sweep rows PASS/FAIL/UNMEASURABLE/NOT SWEPT (`/api/health` is the 404 decoy, `/health/deep-zzz-nonexistent` the 200 catch-all: controls, never passes). (d) Fix strings per THE DELTA, BEFORE 0/0 and AFTER running>=1 / rollback=0. Both boxes hold `vc_credentials_store` = 0 rows, so a string probe proves delivery only; say so. (e) REVISION: keep the previous as `REVISION.pre-5f689991861b` (name it for the INCOMING sha: `REVISION.pre-1ae6f17d19a8` and `REVISION.pre-28e2d27de337` already exist, never overwrite one), assert byte-identical, write, read back.
- **B8. demo-service stop, LAST on the box:** after smoke, REVISION and the final KS-535 read, `docker stop secuura-demo-service` and nothing else. Read back `exited`, RestartCount unchanged over 2 minutes, 0 new log lines. `secuura-demo-overlay` reading `exited` is by design (KS-654), leave it. Whether `DEMO_SERVICE_ENABLED` should be true is NOT yours.
- Mail **DEPLOYED kintsugi** (evidence path) before demo.

### C. DEMO
Only after kintsugi verified; re-read kintsugi's `REVISION` head equals `5f689991861b`. Repeat B1 to B8 with demo's values, batches of TWO (2 vCPU). Outside base `https://demo-pk.secuura.net`; kintsugi `https://kintsugi.secuura.net`. Demo carries Stuart's uat-ps traffic: you write nothing to it beyond the deploy.

### D. TICKETS (drafts only for humans)
- **D1. Done with live evidence ON the ticket** (SHA, image-id check, fix-string rows, smoke rows), only for tickets whose PR is in the delta AND whose own behaviour was measured live: read each ticket's state newest first with a control (a ticket number that does not exist returns 0 nodes) before moving it. Delta tickets = the KS numbers in THE DELTA. Test-only and tooling-only PRs prove delivery, not a runtime change; where the evidence is a string probe, say "delivered" and ask in a QUESTION before Done if unsure. A failed smoke leaves the ticket where it is. **KS-1683 stays as D 32nd left it (In Progress, behaviour check UNMEASURABLE)** unless two principals each hold at least one credential row by then; if so, run the two-call check D 32nd specified, asserting each sees only its own rows and still sees its own. **KS-1717 stays In Review, untouched.**
- **D2. Rule-7 notices** (project `CLAUDE.md`: one BLUF comment per person; `@peter` KS-485, `@stuart.jamieson` KS-772; extranet is not a channel). Verbatim facts only: SHA, time, what changed (22 test/tooling/doc squashes plus the three runtime edits), no secret change, no migration, rollback stamps, NOT swept, demo-service stopped. **DRAFT both to `evidence/` with size and sha256/16 and return them in DEPLOYED. Post only on Wednesday's mailed "POST NOTICES"** (external comms are Kam's class): pre-send hash gate, absent-id control, `suggestion_userMentions` read-back, report comment ids.

## 5. COMMS
Mail `wednesday-agent@agentmail.to`, subject `[Secuura/Blockchain -> Wednesday] <topic>`, via `send.py` (read-back identical), no secrets. Milestones: PLAN CONFIRMATION (launcher preflight warnings VERBATIM) · STATUS A · per box: build (NEW-ID table, heartbeat path), DEPLOYED · final DEPLOYED (SHAs, stamps, swaps OK of N, rollbacks, smoke rows, infra StartedAt, KS-535 before/after, REVISIONs, disk, demo-service stop read-back, UNMEASURED, drafts). Then wrap and STOP. STATUS every ~20 min inside any step over 20 min, with a figure that moves; silence over 30 min is reportable. Blocked: `QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by); after ~15 min proceed on the safest reading UNLESS approval-class (prod, money, comms, irreversible, unnamed box write).

## 8. NOT COVERED, AND THE STOP RULE
- **Not covered:** production, money, any human comment before "POST NOTICES", any `.env` edit, secret change, key change, `az`, prune, any test write (no labelled create, no key), deploying any SHA but the pinned one, source edit, any PR or merge, force push, delete (quarantine), `docker start` of demo-service.
- **STOP and mail on:** develop differing from the pin; a box REVISION other than `28e2d27de337`; a `.sql` in the delta; tracker moved; `.env` hash moved; a wallet hash that moved or kintsugi's on demo; infra `StartedAt` moved; a rollback; SAME-ID on a service that must change; `FAIL-CLOSED`; disk under floor; a production host; non-final anchor row. Rolling back to a tagged image needs no answer; passing a STOP does.

## PARTITION
**Yours:** both boxes through the project's tooling, your clone `deploy-clones/seatD33-5f689991861b`, `5_Project_History/2026-10-26_seatD-33rd/`, the D1 moves.
**NOT yours:** these seats share the inbox `secuura-blockchain@agentmail.to` right now, and a mail naming one is not for you: **Seat S 2nd (%13, merge seat)**, **T 2nd (%14)**, **U 2nd (%15)**, **R 3rd (%16)**, **V 2nd (%17)**. They own their own PRs, clones, worktrees and pushes; none touches your boxes or tickets, and you touch none of theirs. `2_Project_Files` is READ-ONLY. No Docker on the Studio.

## HOLDS
- Production, money, external comms, irreversible: pause for Kam. No `az`, prune, `--no-verify`, force push, `--admin`. Never delete; quarantine. Never edit a running script.
- **NO git push this round** (read-only clone); a push need is a STOP and QUESTION.
- Exit codes on their own line, never through a pipe. zsh does not word-split a scalar (inline the ssh command or use an array). Rotate in the 80-90 band, handover first.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Gate check: re-run the A0 `decision_queue.sh` line; nothing was newly ruled for this round.
- `secuura-demo-service-crash-loop` (Kam 2026-09-05, 14:53 + panel 16:42): `docker stop` only, `docker start` is the undo. Applied to both boxes by D 32nd; this round re-applies it as the last step.
- Other ruled cards (KS-1695, KS-1688, m365 admin, KS-1628, KS-1709) are not this round; do not act.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The four held containers stay held; they need a ruling, not a fix (2026-10-19T18:56:34Z). demo-service's restart loop is KS-1079's.
- Route (3) for the connector-initiated create: UNMEASURABLE, no key, no labelled create (2026-10-26T08:03:02Z). KS-1717: no state change (08:13:57Z).
- Seat D reads, builds, swaps and reports; it opens no PR and edits no source. Notices post only on Wednesday's word.
- Demo takes a build only after kintsugi is verified. Never quote a rebuild count across boxes.

PROVENANCE:
- Both SHAs exist as commits (target `5f689991861b3b9be295797a437ef18b6f55a492`, base `28e2d27de33734c3ad7d2909c3019a9f530d4629`) | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src rev-parse` | read 2026-10-26
- Target is CURRENT origin develop tip at 22:31 AEDT | `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src ls-remote origin refs/heads/develop` (Wednesday) = `5f689991861b3b9be295797a437ef18b6f55a492`; seat re-pins (A1) | read 2026-10-26
- Migrations delta 0, WITH a control that fires: `diff --name-only 28e2d27de337 5f689991861b -- Blockchain/Dev/migrations` = 0 lines; the same path filter over `32964477f~1..5f689991861b` prints `055_ks1557_backfill_connector_create_for_versioned_documents.sql`; `ls-tree --name-only 5f689991861b Blockchain/Dev/migrations/` = 59 entries | same clone (Wednesday) | read 2026-10-26
- 22 first-parent commits; 60 files with the grouped counts; 0 `.sql`; no lockfile; `packages/shared` only `src/__tests__`; no anchoring file; originate 1 test file | same clone: `log --first-parent --oneline`, `rev-list --first-parent --count`, `diff --name-only 28e2d27de337 5f689991861b` filtered | read 2026-10-26
- Wider range `1ae6f17d19a8..5f689991861b`: 137 files, 0 `.sql`, 33 lockfile hits (the lockfile filter fires; the `.sql` one does not, hence the tree-count control, which the drafter did NOT run: UNMEASURED) | same clone | read 2026-10-26
- Runtime diffs (`**/__tests__` ignore line; issuer `test` script; `check:test-types` two more services; api-gateway and vc-issuer 4+/19-) | same clone, `diff` on those paths | read 2026-10-26
- PR-to-runtime-file mapping (KS-1731 = credentialRepo, KS-1635 = verification.ts) | inferred from titles; UNMEASURED at line level | read 2026-10-26
- Box state, KS-535 figures, anchor_store, action_provenance, api_keys, tracker, durations, stamps used, B7 order unanswered, demo-service stop and counts, ticket states as left, Route (3), KS-1717 ruling | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-26_seatD-32nd/HANDOVER.md (a seat's report; the seat re-reads each box) | read 2026-10-26
- Box REVISION now = `28e2d27de337`; stamps `k3`/`d3` free; current ticket states | UNMEASURED: the seat reads them | read 2026-10-26
- Tools listed exist; `seatV2-5f689991861b` clone dir exists | `ls .../5_Project_History/2026-10-26_seatD-32nd/evidence/tools` and `ls .../Blockchain/deploy-clones` | read 2026-10-26
- October grant extended 2026-10-19 18:22:57 AEDT | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md | read 2026-10-26
- Rule-7 notice rule | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 185 to 200 (as cited in D 32nd's brief; not re-read now) | read 2026-10-26
- Shared-inbox seats S 2nd %13, T 2nd %14, U 2nd %15, R 3rd %16, V 2nd %17 | Wednesday's drafting instruction; not re-read from their handovers | read 2026-10-26

- KS-1079 state Backlog (open, last comment 2026-10-26T10:58Z, 3 comments) | Linear ticket KS-1079 (Wednesday, read-only, comments first:50 sorted client-side) | read 2026-10-26
- KS-1683 state In Progress (open, last comment 2026-10-26T10:57Z) | Linear ticket KS-1683 | read 2026-10-26
- KS-1730 state Backlog (open, last comment none) | Linear ticket KS-1730 | read 2026-10-26
- KS-485 state Todo (open, last comment 2026-10-26T11:02Z) | Linear ticket KS-485 | read 2026-10-26
- KS-772 state Todo (open, last comment 2026-10-26T11:02Z) | Linear ticket KS-772 | read 2026-10-26
- KS-654 state Deployed to UAT (ARCHIVED, last comment 2026-09-05T06:48Z; cited only as the reason demo-overlay reads exited) | Linear ticket KS-654 (includeArchived) | read 2026-10-26
- KS-907 state Tested Not Deployed (ARCHIVED, last comment 2026-09-14T12:15Z; cited only for the never-2_Project_Files rule) | Linear ticket KS-907 (includeArchived) | read 2026-10-26

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-26 22:33
