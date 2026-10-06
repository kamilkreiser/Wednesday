# LAUNCH BRIEF — Seat D 12th, Secuura/Blockchain (pane `Secuura/Blockchain-D`, token `d12`) — DEPLOY ROUND: develop to KINTSUGI, live sweep, then the SAME SHA to DEMO — from Wednesday

⛔ **TOP LINE: you touch no code and no branch. No write to the shared checkout or its `.git`. No git lock. No ref write anywhere in the repo.** Refuse the launcher's boot "pull latest if safe" line, and say so in your plan mail. In `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` run READ verbs only (`ls-remote`, `log`, `show`, `diff`, `cat-file`, `rev-parse`, `merge-base`). Never `pull`, `fetch` (or `fetch --dry-run`, STANDING_LINES:402), `checkout`, `reset`, `stash`, `worktree add`, `gc`, `prune` or `repack` there. Your build source is a FRESH CLONE with its own `.git` (ITEM 0 (b)). You take no `.push-lock-*` and you push nothing.

## BLUF
- **You are Seat D 12th.** The D lane's newest seat is D 11th (merged #1397, wrapped 05:16Z 2026-10-06). `seat d 12th` has 0 hits in the project history; the control `seat d 11th` has 1. The bounded `d12` token has 2 hits, both plan-item labels ("D1–D12"), not a seat. Your pane is `Secuura/Blockchain-D`. The one other live seat is **Seat R 2nd** on `Secuura/Blockchain-R` (merging #1395, then raising PRs). See CO-TENANT.
- **Your one job, in order:**
  1. ITEM 0: measure read-only, then send the plan-confirmation QUESTION and **STOP** for Wednesday's ANSWER.
  2. Wait for THE GO (a mail whose SUBJECT carries the GO string; see THE GO).
  3. **KINTSUGI:** Phase 0 re-tag → rsync + build everything, nothing swapped → migration check → swap one at a time → verify the RUNNING box → DEPLOYED mail → LIVE SWEEP → STATUS mail with the sweep result quoted.
  4. **DEMO, only if kintsugi swept clean:** the same phases with demo's own numbers, its own plan STOP and its own migration STOP → DEPLOYED mail → sweep → STATUS.
  5. Handover, history entry, WRAP.
- **One deploy seat.** A second deploy seat runs only if Wednesday says so in a mail. Kam's cap is two (grant below).
- **DEVELOP_AT_DEPLOY** is the develop SHA you read by `ls-remote` at ITEM 0. Every box gets that one SHA. Demo gets exactly the SHA kintsugi swept clean, never a newer develop.
- **Production does not exist and is not touched. No money. Never edit a secret. No force push. No `--no-verify`.** You merge, push, raise and code nothing, change no ticket state, and post no ticket comment.

## AUTHORITY (verbatim, with sources)
- **Kam's October deploy grant**, live board 2026-10-05 16:21:39: *"for the month of October, keep pushing, keep publishing, deploy all that works and is ready but only when its ready.  Deploy to both servers, demo and kintsugi"*. File: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md`. Its row in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md` (line 12) reads: *"Ready = merged on a QA gate GO + verified at source; kintsugi first + live sweep, then demo (lifts "demo waits for Peter's nod" for October). Unchanged: production, money, comms to Peter/Stuart, irreversible; KS-535 wallet rule; Phase 0 re-tag."* **Expiry: end of Saturday 2026-10-31.** The grant file's "How to apply" item 2: *"Report each deploy … what went where, the SHA, what the live sweep found. The grant removes the pause, not the receipt."*
- **Kam's card `secuura-headroom-before-90pct-stop-1006` = a**, clicked 19:30:00 on 2026-10-06 (the store's `ruled_ts` reads 19:31:10): option a, *"Spark pipeline first, then one deploy"*, detail *"… Then one deploy round of everything merged to kintsugi, then demo (your October grant). The KS-1402 build waits for the renewal."*
- **Kam, 19:30:43, verbatim:** *"No one else is sharing this seat, so you can use up to 100%, but do it as the recommendation above with Spark on all tickets and one or maybe two deployers."* File: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-06_use-to-100pct-spark-all-tickets-one-or-two-deployers.md`, and its EXPIRING-GRANTS row (line 10): *"at most two deploy seats (kintsugi, then demo, under the October grant). KS-1402's build is NOT unparked."*
- **Kintsugi first** — Kam, email 2026-09-10 13:22: *"Kintsugi is our dev box so things should always be deployed there first."* File: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_kintsugi-first-then-demo-behind-gates.md`. Its line 49-52: *"KS-535 IS ABSOLUTE … kintsugi must never share demo's `PLATFORM_WALLET_MNEMONIC`. Two deployments on one wallet select the same UTxOs and race … Any kintsugi deploy brief carries this by name."*
- **Merge order for this exact build** — Kam's card `secuura-ks1404-anchors-before-049-merge-order-1005` = a (2026-10-05 19:52): *"The build that has the wiring and no 049 goes to kintsugi, gets swept, then goes to demo. #1383 merges straight after."* DEVELOP_AT_DEPLOY carries the KS-1404 wiring (#1388) and does NOT carry 049 (#1383 is unmerged; ls-remote below). **This round is that build.**

## WHAT THE BOXES RUN (recorded; measure both at ITEM 0)
- **Kintsugi: last recorded at develop `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`** (tree `dab6adb69ea3`), deployed by Seat D 7th, FINAL STATE 08:01:19Z 2026-10-05. Record: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD7-kintsugi-deploy.md` (240 lines). Its facts you need:
  - ten rollback sets, newest `pre-20261005` ×17 (fp `38db468630789d0d`);
  - `REVISION` sha16 `54b9ad2a64c83ed9`, 11,679 B;
  - disk 12,657 MB free settled after its round;
  - main tracker 49 rows, platform tracker 1, 0 pending once measured by the runner's own `/platform/i` routing;
  - error baseline FIVE lines (billing permission-denied, security `audit_logs` owner, staking `svc_accumulated_rewards`, demo-service KS-641, issuer-frontend nginx refusing `GET /.git/config`);
  - KS-535: mnemonic `695d09df873ff42b`, blockfrost `142098c9528d0188`, `.env` sha16 `634e99a79cbc6ee5` (16,719 B);
  - `/health/deep` `startupMigrations {ran:true, applied:46, failed:0}`;
  - `NODE_ENV=development`; demo-service's KS-641 restart loop (same Id `39b34c120cf6`).
  - No kintsugi deploy after D 7th is recorded: Seat D 8th (10-05) measured both boxes READ-ONLY for KS-1404 and deployed nothing; history entries D 8th → E 8th name no deploy. **The box's state since 08:17Z 2026-10-05 is UNMEASURED.**
- **Demo: last recorded at `0f8fb33c3416`** (s169, 2026-09-10, history.md line 7443: "BOTH BOXES REBUILT AND VERIFIED ON `0f8fb33c3`"). Seat D 7th did NOT start demo (its handover, "NOT RUN"). Seat D 8th read demo READ-ONLY on 10-05: `TSA_URL` present-but-empty, no anchor, runs `docker-compose.yml` only (no override), `ts_timestamps` 1 MOCK row. **Demo's SHA, census, disk, tags and DB since 09-10 are UNMEASURED.** Demo's KS-535 mnemonic hash on record: `12ea1a07174c3f50`.

## WHAT THIS ROUND CARRIES (measured by the drafter at source, READ verbs + a scratch clone)
- **develop at origin = `f556373b941823931a9858a788c478e50e822a79`** (#1396 KS-1256), tree `1aa966ca162b`, `ls-remote` 08:36:27Z 2026-10-06. `46c3e20cfbd2` is an ancestor (rc 0). `#1395` (KS-1305) head `1bdfbe0f2f06` is OPEN; `#1383` (049) head `32e8459bc0f5` is OPEN.
- **Kintsugi range `46c3e20cfbd2..f556373b9418`: 25 commits / 14 first-parent / 134 files / 69 under `Blockchain/Dev`.** First-parent, newest first:
  - `f556373b9` #1396 KS-1256 (connector allow-list fails closed 503)
  - `f42161da3` #1393 KS-1278 (revoke keyed on the resolved row)
  - `add9a3b8b` #1397 KS-1425 (lock refresh across the services' lockfiles)
  - `4eaf7741a` #1394 KS-723 (GET /api/anchors/tx/{txHash} in the OpenAPI contract)
  - `3f9ff4e1e` #1385 KS-938 (MFA disable NULLs seed + backup codes)
  - `22b268143` #1389 KS-1330 (run-shell-suites.sh; no image)
  - `f01798064` #1391 (docs: project history; no image)
  - `c5101866e` #1390 KS-1408 (systemTest schemathesis pin; no image)
  - `d784b613c` #1388 KS-1404 (timestamping ships its anchor; compose points at it)
  - `3cb93b9c7` #1392 KS-1411 (akto image pin; no image)
  - `232623892` #1384 KS-1210 (OAuth app scopes + by-id routes)
  - `32e058975` #1387 KS-1388 (observability env examples; no image)
  - `0f2422925` #1382 KS-1005 (change-password reads the hash it verifies)
  - `f01c1da57` #1381 KS-1345 (failed webhooks list → 500)
- **Migrations in the kintsugi range: NONE.** 0 `.sql`, 0 paths under `migrations/`, no `run-migrations.sh`, no `docker/init`. (046, 047 and 048 already exist at `46c3e20` and are recorded on kintsugi; they are not new.) `migrations/` holds 50 `.sql` at develop, the same set D 7th measured.
- **Env/config change in the kintsugi range: ONE compose line.** `docker-compose.yml` timestamping gains `TSA_TRUST_ANCHORS_PEM=${TSA_TRUST_ANCHORS_PEM:-/app/config/tsa-trust-anchors-dtrust.crt}`, and `services/timestamping/Dockerfile` now copies `/app/config` into the runtime stage (`+COPY --from=builder /app/config ./config`). The anchor is effective with **no `.env` edit**. Compose `${VAR` names 97 → 98, the only addition `TSA_TRUST_ANCHORS_PEM`.
- **KS-1256 adds NO env var.** It reads the Redis key `platform-settings` (`verification.ts` ~:1230-1250) and refuses connector document creates with 503 when Redis is unavailable or the read throws. Kam's card `secuura-connector-allowlist-missing-setting-ks1256-1005` = b keeps "no restriction" when the setting is unset; card `secuura-ks1256-redis-outage-stops-connector-creates-1006` = a accepts the 503 during a Redis outage. **Behaviour change to name in your STATUS: a Redis outage on a box now stops Platform-S connector document creates.**
- **Rebuild set, measured: 30 images** (D 7th's `service_mapd7.py`, run read-only over this range, rc 0, every control firing). KS-1425's lockfile refresh reaches nearly every service: admin-frontend, analytics, anchoring, api-gateway, auth, billing, demo-overlay, demo-service, governance, guardian, issuer-frontend, kyc, m365-integration, mcp-server, migrations, nft-certificate, originate, prism, queue, referral, security, staking, tenant-provisioning, timestamping, tokenisation, transfer, vc-issuer, verifier-frontend, wallet-connector, website-frontend. **This is NOT D 7th's 17.** Re-derive it in your clone at ITEM 0 against the box's MEASURED SHA.
- **If #1395 merges before you launch,** DEVELOP_AT_DEPLOY is its squash. Its head touches `services/originate/src/db.ts`, one new test and the two `Projects Documents/*.html`: no migration, no compose, no env (drafter, `diff --name-status` merge-base..head). Originate is already in the set.
- **Demo range `0f8fb33c3..f556373b9418`: 600 commits / 464 first-parent / 1,152 files / 534 under Dev, 28 under `packages/shared`.** It carries **`migrations/038a_ks1054_core_tables_before_039.sql` (ADDED)**, **`migrations/039_rls_fail_closed.sql` (MODIFIED)**, `docker/init/01-schema.sql` + `06-m365-tables.sql` (M), `scripts/run-migrations.sh` (M), and **three new compose variables: `ADMIN_USER_PASSWORD`, `GATEWAY_VOUCH_SECRET`, `TSA_TRUST_ANCHORS_PEM`**. `packages/shared` changed, so expect every image. Demo is ARM64, 2 vCPU, 4 GiB + 6 GiB swap (project `CLAUDE.md:12`).

## THE PROCEDURE — PROVEN, COPY IT
Your project tree is `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/`. Read first:
1. `5_Project_History/HANDOVER-seatD7-kintsugi-deploy.md` (240 lines, whole): the two-DB migration gate, the FINAL STATE, rollback, box facts, eleven instrument traps.
2. `Blockchain/Dev/deployment/KINTSUGI-REBUILD-RUNBOOK.md` at DEVELOP_AT_DEPLOY via `git show` (445 lines): §3 Phase 0, §5 build all then swap, §6 migrations then swap, §7 revision stamp, §9 verification.
3. `.claude/skills/secuura-test-discipline/SKILL.md` §5f (lines 540-552 at develop) and §3 teardown (260-287), via `git show`.

**Tools: D 7th's set is the newest proven deploy set.** Copy `5_Project_History/2026-10-05_seatD-7th/boot/` and `deploy/` into `5_Project_History/2026-10-06_seatD-12th/`. Use **`deploy/phase4_remote_d7.sh`'s two-DB pending gate**, never B 50th's 038a gate. Re-key before any use:
- tokens: `seatD7`, `D7`, `d7`, `D 7th`, `.rebuild-seatD7/`, `pre-20261005`, `new-20261005`, every older generation (`seatB50`, `pre-20260930` and back), absolute paths;
- constants a token map cannot see: `phase0_remote_d7.sh`'s `SCOPED` count (17 → your measured set) and `WANT_N`; its precheck controls and fingerprint list (add `pre-20261005` ×17 `38db468630789d0d`); `phase4`'s `ORDER`;
- lettered tokens: grep the copies for `int(`, `\d\d`, `[0-9]{2}` (STANDING_LINES:392);
- prove the re-key with a control that goes the other way.

**Inbox tools: the D lane's newest** are D 11th's `5_Project_History/2026-10-06_seatD-11th/raise/inbox_matchd8.py`, `inbox_watchd8.sh` and `watchproofd8.sh`. Re-key the seat to `d12`, put `d 11th`/`d11` in OTHER_SEATS (backward) and `d 13th`/`d13` (forward, STANDING_LINES trap-4 forward half), and prove the unknown-addressee arm with a seat in NEITHER list (STANDING_LINES, R 1st). D 11th's own lesson: *"run trap4 and namecheck, do not read them."*

### HOW YOU REACH THE BOXES (the drafter connected to neither)
- **Kintsugi:** `ssh -i "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/vm_secuura02_kintsugi" -o IdentitiesOnly=yes secuura@20.198.226.148`. Stack `/home/secuura/secuura/Dev`; compose project `dev`, `--profile phase2`; gateway `localhost:6882`; front `https://kintsugi.secuura.net`. Runs `docker-compose.yml` + an untracked `docker-compose.override.yml` (feeds auth): **never `-f`**.
- **Demo:** `ssh -i "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/vm_secuura02_demo" -o IdentitiesOnly=yes secuura@20.212.118.59`. Stack `/home/secuura/secuura/Dev`. Runs `docker-compose.yml` only. Compose project and profile UNMEASURED: read them from the running containers' labels before any compose command. Front: project `CLAUDE.md:13` names `https://secuura02-demo.southeastasia.cloudapp.azure.com`; the 09-10 lesson names `demo-pk.secuura.net`. Measure which serves.
- The kintsugi NSG admits ONE `/32` (egress `157.211.46.215` matched on 10-05). **If SSH fails, STOP and mail your egress address. Never read or touch an NSG. No `az` call.**
- zsh: a scalar does not word-split (`SSHC="ssh -i …"; $SSHC` → rc 127): inline the ssh or use a function. `rc=$?` on its own line; never `PIPESTATUS`.

### ITEM 0 — MEASURE (read-only everywhere), then STOP
- **(a) develop:** `ls-remote` from the shared checkout (READ verb; its `core.sshCommand` carries the on-disk deploy key). Run with `env -u GIT_SSH_COMMAND`. Report the full SHA and call it DEVELOP_AT_DEPLOY. If it is not `f556373b9418`, give the first-parent list of `f556373b9418..DEVELOP_AT_DEPLOY` and say whether it holds any `.sql`, any `migrations/` path, any compose/`.env.example` change, or #1383.
- **(b) the build source, a FRESH CLONE:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/deploy-clones/seatD12-<first 12 of DEVELOP_AT_DEPLOY>` (`deploy-clones/` holds `seatA16-…`, `seatB23-…`, `seatB50-…`, `seatD7-46c3e20cfbd2` today). `git -c core.sshCommand='ssh -i …/3_Access_Keys/github_deploy_rw -o IdentitiesOnly=yes' clone --no-checkout git@github.com:Secuura/Distributed_Secuura.git <dir>`, then `checkout --detach <full sha>`. Assert: HEAD == DEVELOP_AT_DEPLOY; tree recorded; porcelain empty; own `.git`; `objects/info/alternates` ABSENT. Never `worktree add`, never `--reference` the shared `.git` (D 7th trap 11).
- **(c) the rebuild set:** your re-keyed `service_map` in your clone over `<kintsugi's MEASURED SHA>..DEVELOP_AT_DEPLOY`. Expect the 30 above if the box is at `46c3e20cfbd2`. Per image: in/out and the path that put it in.
- **(d) kintsugi as it runs** (key NAMES only, never values):
  - deployed SHA: `REVISION` (expect sha16 `54b9ad2a64c83ed9`) + content hash of the range's `Blockchain/Dev` paths against `46c3e20cfbd2` and DEVELOP_AT_DEPLOY, with a planted mismatch the check must catch;
  - census, restarts (KS-641 loop judged by Id + Created + image), rollback sets and fingerprints (ten sets);
  - **disk, SETTLED.** D 7th: 17 images dipped 8,222 MB (19,290 → 11,068). B 50th: 29 images dipped 5,635 MB. **You start near 12,657 MB with a 4,000 MB guard: ~8,657 MB of headroom for 30 images.** Forecast from both per-image build logs (`.rebuild-seatD7/`, `2026-09-30_seatB-50th`), state the arithmetic, and say plainly if the forecast crosses the guard. **You never free space.** See Q-DISK.
  - DB: main and platform trackers counted SEPARATELY by the runner's `/platform/i` routing (D 7th's gate), 0 pending expected on both, with a planted fake filename that must read pending; 048 recorded (STANDING_LINES:109);
  - error baseline (five lines);
  - **KS-535 BEFORE:** `sha256[0:16]` of `PLATFORM_WALLET_MNEMONIC` and `BLOCKFROST_API_KEY`, from `.env` AND the running anchoring container; three controls (`$HOME` expands; the literal-string artefact reads `1d99a769a815b299`; empty string `e3b0c44298fc1c14`). Mnemonic must read `695d09df873ff42b` and must NOT read demo's `12ea1a07174c3f50`;
  - `/health/deep` (NEVER `/health`, which is nginx's 179 B literal) + `check-startup-migrations.sh` rc;
  - timestamping env: `TSA_URL` value or EMPTY; `TSA_TRUST_ANCHORS_PEM` PRESENT/ABSENT/EMPTY; whether `.env` defines `TSA_TRUST_ANCHORS_PEM` (NAME only: a box value would override the new default); whether `/app/config` exists; a `PORT` control that must read PRESENT;
  - Redis: whether the gateway reports Redis available (`/health/deep` or the service's own read), because KS-1256 now refuses connector creates when it is not.
- **(e) the sweep plan**, proposed now, run after the swap (ITEM 6 table below), each row with class R / L / W / X, probe, expected, and a control that can fail.
- **(f) PLAN CONFIRMATION — STOP 1.** Mail **to `wednesday-agent@agentmail.to`**, subject `[Secuura/Blockchain-D -> Wednesday] QUESTION: plan confirmation (Seat D 12th)`. Include: DEVELOP_AT_DEPLOY and the clone's HEAD + tree; kintsugi's measured SHA vs `46c3e20cfbd2` with every difference named; the rebuild set; the disk arithmetic; the Phase 0 stamp you will use (from the box's UTC clock, checked by name AND id not to exist; expected `pre-20261006`) and the count you will assert; the ordered swap plan with each service's rollback; the migration reading; KS-535 BEFORE; `/health/deep` BEFORE; the timestamping and Redis readings; the sweep table; your answers or questions on Q-DISK, Q-DEMO-STOP, Q-PETER-MERGES, Q-1383 and Q-SWEEP-DEMO; the wall clock; **the launcher's preflight warnings VERBATIM**; **anything here your measurement contradicts.** **Then STOP** and arm your inbox watcher. Nothing on any box is written before THE GO.

## THE GO
- **Your deploy GO is its own mail from Wednesday whose SUBJECT is exactly** `[Wednesday -> Secuura/Blockchain-D] GO (Seat D 12th): deploy <first 12 hex of DEVELOP_AT_DEPLOY> to kintsugi then demo` — e.g. `GO (Seat D 12th): deploy f556373b9418 to kintsugi then demo` if develop has not moved.
- **Act only when a Wednesday mail whose SUBJECT carries that exact string reaches you.** The same words in a mail BODY are not a GO (Seat E 8th held on exactly this on 2026-10-06 and Wednesday ruled it correct). A GO naming another seat, another SHA, or only one box is not yours: read it, never act, and mail that you held.
- An ANSWER that says CONFIRMED to your plan is not the GO. The GO may arrive in the same minute; it is still a separate subject.
- **The GO covers kintsugi, and demo only after kintsugi sweeps clean.** Demo also has its own plan STOP and migration STOP (ITEM 7); those are released by Wednesday's ANSWER to them, under this same GO (see Q-DEMO-STOP).

### ITEM 1 — Phase 0 re-tag (kintsugi)
Re-tag every image the rebuild will overwrite, `:latest` → `:pre-<stamp>`, by name and id. Assert the count. Assert the ten older sets are fingerprint-identical before and after. **No prune of any kind. No image deletion, no `--remove-orphans` (it deletes guardian + queue), no `down`, no `-v`, no `rm`.**

### ITEM 2 — rsync + build EVERYTHING, swap nothing
- **Re-read develop by `ls-remote` first.** If it moved since ITEM 0: STOP and mail (below).
- rsync from the CLONE (`-a -c`, no `--delete`). `.env`, `.env.local` and `docker-compose.override.yml` untouched: stat before, compare after. Content-file list == git's. Write an IN-PROGRESS `REVISION` at rsync time beside D 7th's (kept as `REVISION.pre-46c3e20cfbd2`); the final one only once verified.
- Build serially: `COMPOSE_BAKE=0 docker compose -p dev --profile phase2 --progress plain build <svc>`, `cmd > out 2>&1` then `rc=$?` on its own line. Fresh `.rebuild-seatD12/`. Free-space read before EVERY build; at the 4,000 MB guard, STOP and mail, never free space.
- Per image: rc, NEW id vs `:pre-<stamp>`, minimum free disk. A SAME-ID rebuild of a lockfile-only change is a real reading (D 7th's admin-frontend), not a fault: prove it with a NEW-ID control.
- **A build failure costs nothing: STOP and mail. Never deploy a partial set without Wednesday's word.**

### ITEM 3 — migrations: expected a measured NO-OP on kintsugi
api-gateway's `startup-migrations.ts` applies any unrecorded file when it boots. **Immediately before the api-gateway recreate, in the same action:** run D 7th's two-DB pending count. **0 on both DBs → proceed. Anything else → STOP 2**, subject `[Secuura/Blockchain-D -> Wednesday] QUESTION: unexpected pending migration (Seat D 12th)`, with the file names. Apply nothing. `dev-migrations` is rebuilt and NOT recreated (one-shot, nothing new), as D 7th did.

### ITEM 4 — swap one service at a time
- `docker compose -p dev --profile phase2 up -d --no-deps --force-recreate <svc>`, a health read between swaps. Backends first, **anchoring and api-gateway last among the backends**, then the frontends. **timestamping's recreate is what applies the new compose `TSA_TRUST_ANCHORS_PEM` default**: read its env and `/app/config` straight after.
- After api-gateway: the yaml bind mount's container inode == host inode, and the served yaml md5 == your clone's (KS-723 changed it).
- **On an unhealthy service:** `docker tag dev-<svc>:pre-<stamp> dev-<svc>:latest`, the same `up -d`, then STOP and mail the state of every service. Keep the new image as `:new-<stamp>`.
- A gate that trips on the INSTRUMENT: fix, re-prove, resume. A gate that trips on a READING: STOP and mail.

### ITEM 5 — verify the RUNNING box, then the DEPLOYED mail
- Settled census ≥300 s after the last swap: 0 restarts except the KS-641 loop; error lines == the ITEM 0 baseline with ZERO NEW lines; non-swapped containers untouched (planted change caught); rollback sets intact (eleven); final `REVISION` == DEVELOP_AT_DEPLOY, written now.
- `/health/deep` `startupMigrations` `ran:true`, `failed:0`; `check-startup-migrations.sh` rc 0 with its three controls (failed→1 → rc 1; broken `python3` shim → rc 1; the nginx `/health` literal → rc 2). Also `https://kintsugi.secuura.net/health/deep` from the Mac.
- **KS-535 AFTER the restart:** both hashes == ITEM 0's; mnemonic != `12ea1a07174c3f50`; `.env` byte-identical; same three controls. **A move or a match with demo is a STOP.**
- Ratios (`N / N`), never "all". A probe you cannot run is NOT RUN, with the reason.
- **Mail** `[Secuura/Blockchain-D -> Wednesday] DEPLOYED: kintsugi at <DEVELOP_AT_DEPLOY 12> (Seat D 12th)`: box, full SHA, **rollback tag**, per-service image ids before/after, migration count, raw `/health/deep`, KS-535 hashes and verdicts, timestamping env, settled census. **Go straight on to ITEM 6 in the same turn.**

### ITEM 6 — LIVE SWEEP on kintsugi (secuura-test-discipline §5f evidence)
§5f (develop, `SKILL.md:542-545`): *"A runtime-behaviour change is not done — and the ticket does not move to Done — on offline quality-gate green alone. It needs a live sweep on the correct host (§2), against a fully torn-down and rebuilt environment (§3), with all containers verified up."* Kintsugi is swapped in place and is never torn down (live data, KS-535, no prune). Wednesday ruled on 2026-10-05 (D 7th ANSWER ruling 7): **a kintsugi in-place PASS is a DONE CANDIDATE ONLY**; every row's §5f status stays `live sweep owed`.

Every row gets a **dist-bytes check**: a CODE marker (not a comment; D 7th trap 5) from the fix's own diff PRESENT in the running container and ABSENT in `:pre-<stamp>`. Shared-package code lives at `/app/node_modules/@secuura/shared/dist`, not `/app/dist`.

| ticket | fix | class | probe → expected (control) |
|---|---|---|---|
| KS-1404 | `d784b613c` | R | timestamping env `TSA_TRUST_ANCHORS_PEM` PRESENT = `/app/config/tsa-trust-anchors-dtrust.crt` (unless `.env` overrides), file EXISTS and readable by uid 1001 (control: a fabricated path reads ABSENT). A real-token verify is W (it calls the TSA): only if Wednesday names it. |
| KS-723 | `4eaf7741a` | R | served yaml declares `GET /api/anchors/tx/{txHash}` (control: a fabricated path 0) + md5 == clone |
| KS-1256 | `f556373b9` | X / R | the 503 path needs a Redis outage: **never stop Redis on a box.** R: Redis reads available; dist-bytes `isRedisAvailable` marker in the gateway dist |
| KS-1005 | `0f2422925` | L | change-password with a WRONG current password on the test account → not 404 (the defect was 404 for every user); writes nothing |
| KS-1210 | `232623892` | L | register an OAuth app with a scope outside the published nine → refused (control: the response for a valid scope is NOT sent, it would write) |
| KS-938 | `3f9ff4e1e` | W | MFA enable/disable writes rows: NOT run unless named |
| KS-1278 | `f42161da3` | W | a revoke writes: NOT run unless named. **No SELECT over past revokes** (Kam's card `secuura-uuid-revokes-never-wrote-status-history-1006` = c, "Don't measure") |
| KS-1345 | `f01c1da57` | X | needs a failed DB query; dist-bytes only |
| KS-1425 | `add9a3b8b` | X | lockfiles; NEW-ID/SAME-ID per image is the reading |
| KS-1305 | (if #1395 is in) | X | needs a missing generated Prisma client; dist-bytes only |
| KS-1330, KS-1388, KS-1408, KS-1411 | — | X | no image input (service_map: NONE) |

**L rows run only as a dedicated test/QA account** (D 7th used `admin@secuura.com`, a seeded test account; one login, token reused). Never a human's account. W rows run only if Wednesday names them at STOP 1. Per row report: dist-bytes DEPLOYED / NOT DEPLOYED with marker + control; PASS / FAIL / UNMEASURED-with-reason, raw values beside every verdict; one drafted line, **NOT POSTED**: a PASS as `Swept live on kintsugi at <sha12> <UTC>: <probe> → <raw>; control <raw>`, anything else in the canonical shape `Merged <sha> (PR #n, <file>); offline gates green; NOT Done per secuura-test-discipline §5f — live sweep owed (torn-down rebuilt stack, all containers verified up), unverified: <what>` (STANDING_LINES:270, handle `live sweep owed` lowercase).

**Then mail STATUS, with the sweep result QUOTED in it:** `[Secuura/Blockchain-D -> Wednesday] STATUS: kintsugi swept at <sha12> — PASS n / FAIL n / UNMEASURED n / X n of N (Seat D 12th)`. **"Kintsugi swept clean"** = every row DEPLOYED by dist-bytes or by a SAME-ID reading, 0 FAIL, 0 new error lines, KS-535 PASS. Anything else: STOP; demo does not start.

### ITEM 7 — DEMO, the same way, only after a clean kintsugi STATUS
- **Re-read develop by `ls-remote`.** Demo gets the kintsugi SHA. If develop moved, report it; it does not move demo's SHA.
- **Demo ITEM 0 (read-only):** SHA by `REVISION` + content hash against `0f8fb33c3` and DEVELOP_AT_DEPLOY; census; compose project/profile from container labels; rollback sets (s169 left 33 tags); **disk SETTLED** (~11 GB free on 09-10; demo builds natively on 2 vCPU ARM64 with 4 GiB: build ONE image at a time, the 07-2x history records a batch of 4 OOM'ing it); both trackers by the two-DB gate, whether `038a` is recorded, whether `039` is recorded and its RLS state on `charge_events` and `certifications`; error baseline; **KS-535 BEFORE: the mnemonic must read `12ea1a07174c3f50` and must differ from kintsugi's**; timestamping env; the env-key NAMES `ADMIN_USER_PASSWORD`, `GATEWAY_VOUCH_SECRET`, `TSA_TRUST_ANCHORS_PEM` (PRESENT/EMPTY/ABSENT only). Compose says an unset `ADMIN_USER_PASSWORD` makes the seeder skip that account (`docker-compose.yml:789-811` at develop): say what that does on demo's existing DB.
- **STOP 1-demo:** `QUESTION: demo plan confirmation (Seat D 12th)` with the rebuild set (expect all), the forecast build time on ARM64, disk arithmetic, the Phase 0 stamp, and every contradiction.
- **STOP 2-demo is EXPECTED:** `038a` is unrecorded on demo unless measured otherwise, and an api-gateway recreate applies it to live data. Read `git show DEVELOP_AT_DEPLOY:Blockchain/Dev/migrations/038a_ks1054_core_tables_before_039.sql` and say whether it is idempotent on an existing DB. `039` is MODIFIED in range: the runner tracks by filename, so a modified, already-recorded `039` is NOT re-applied; say what that means. `docker/init/*` is inert on an initialised data dir: confirm from demo's compose. **Apply nothing before Wednesday's ANSWER.**
- **Demo holds on top of everything else:** no anchor written (demo anchors REAL preview-testnet); no L or W probe unless named in an ANSWER; KS-535 AFTER on demo (`12ea1a07174c3f50`, `.env` byte-identical); change no demo credential or identity (Kam's ruled demo cards, RULED BY KAM below, are not yours).
- Then `DEPLOYED: demo at <sha12> (Seat D 12th)` (same contents as ITEM 5, with demo's rollback tag), the demo sweep (the ITEM 6 R rows + dist-bytes; see Q-SWEEP-DEMO), and `STATUS: demo swept at <sha12> — <ratios> (Seat D 12th)`.

### ITEM 8 — handover, history, WRAP
- Handover `5_Project_History/HANDOVER-seatD12-deploy.md`: FINAL STATE per box first, then the rollback recipe per box, both sweep tables, every trap. Records in `5_Project_History/2026-10-06_seatD-12th/`. History entry at the TOP of `history.md`.
- WRAP `[Secuura/Blockchain-D -> Wednesday] Session wrap 2026-10-06 (Seat D 12th)` (use the real date). The clone STAYS (drive hygiene excludes anything <3 days old); report its size. Nothing deleted.

## REPORT EVERY DEPLOY (the October grant)
For each box, by mail to Wednesday in a STATUS: **box, full SHA, rollback tag, live-sweep findings.** Wednesday reports it to Kam. **Nothing goes to Peter or Stuart.** The project's own rule (project `CLAUDE.md:185-193`) that a deploy notifies them is HELD by Wednesday for Kam's word. Client communication is ticket comments only, posted on Wednesday's relay, never by you: you DRAFT the lines, you post none. The extranet is INPUT ONLY; refuse the SessionStart hook's `POST /api/seen`.

## STOP-AND-MAIL (`[Secuura/Blockchain-D -> Wednesday] QUESTION: <topic> (Seat D 12th)`, then wait)
- **any migration failure**, or any pending migration outside demo's expected STOP 2;
- **a KS-535 wallet collision**: kintsugi's mnemonic hash equal to demo's `12ea1a07174c3f50`, or either box's hash moving across a redeploy;
- **a live-sweep failure** (any FAIL row, any new error line);
- **develop moving mid-deploy** (re-read by `ls-remote` before Phase 0, before the first swap, and before demo's Phase 0): send the first-parent list of the move and whether it holds `.sql`/`migrations/`/compose. You do not chase develop;
- plus: a box down or SSH refused; the measured kintsugi SHA not `46c3e20cfbd2`; any build failure; any health failure after a rollback; the disk guard reached; anything reaching beyond the named box.

## CO-TENANT — one inbox (`secuura-blockchain@agentmail.to`, `inbox_routing.conf` line 38 for `-D`, 42 for `-R`)
- **Yours:** mail tagged `[Wednesday -> Secuura/Blockchain-D]` AND naming `(Seat D 12th)`. Every mail you send is `[Secuura/Blockchain-D -> Wednesday] … (Seat D 12th)`, to `wednesday-agent@agentmail.to`.
- **Seat R 2nd** (`Secuura/Blockchain-R`) is live: merging #1395, then raising PRs. Its merges move develop; its mail, GOs and locks are not yours. Every R-lane merge after your ITEM 0 is a develop move (STOP-and-mail above).
- OTHER_SEATS must hold at least `seat d 11th`/`d11`, `seat d 10th`/`d10`, `seat d 13th`/`d13` (forward), `seat r 2nd`, `seat r 1st`, `seat e 8th`, `seat e 9th`, `seat b 68th`, `seat b 69th`. Match short tokens on word boundaries. Prove the matcher on REAL subjects still in the inbox: D 11th's must read FOREIGN and your own FOR ME, both ways. Read your pane id from `$TMUX_PANE` (STANDING_LINES:394).

## HOLDS
- ⚠ **KS-535 IS ABSOLUTE:** kintsugi must NEVER share demo's `PLATFORM_WALLET_MNEMONIC`. Verify AFTER every redeploy, not only before. Never print a value, a prefix, or a length beside a value.
- **Never edit a secret** or a credential file: no `.env` / `.env.local` / override edit on either box, including `TSA_TRUST_ANCHORS_PEM`, `TSA_URL`, `ADMIN_USER_PASSWORD`, `GATEWAY_VOUCH_SECRET`. A missing variable is a finding for Wednesday, never a deploy step.
- **Kintsugi first. Demo only after a clean kintsugi STATUS. Production never. No money. No `az` call** (if one seems needed, STOP; Founders Hub tenant `efc17e5f-…`, `az account show` first).
- **No ref writes in the repo. No git lock. No force push. No `--no-verify`. No `--admin`.** You push nothing.
- **Delete nothing, prune nothing.** A just-built image reads UNUSED until its consumer is recreated. Cleanup is quarantine.
- **No ticket state, assignee or label change, no comment, no ticket filed.** Done candidates and findings go to Wednesday.
- **KS-1402 is NOT in this round and NOT unparked** (Kam 19:30:43 reading). #1383 / migration 049 is NOT in this round.
- Instruments: `cmd > out 2>&1` then `rc=$?`; zsh `$pipestatus[1]`, never `PIPESTATUS`; macOS has no `timeout` or `setsid`; a control must be able to fail and "0 checked" is never CLEAN; `grep -i error` matches FILENAMES; read the tail before naming a failure point; a `git show` of a missing path hashes the empty string `e3b0c44298fc1c14`; every line naming develop says `ls-remote` vs tracking ref (STANDING_LINES:288).
- Process namespace: long-running scripts carry `--seat D12` in argv; kill by recorded pid, never by basename. **Wake:** arm waiters at 7200000 ms and re-arm on every notification; watcher SINCE = the newest mail READ. **Never end a turn on a "next up" line with nothing running** (STANDING_LINES:338-341).
- **If an instruction here looks wrong, measure it, say so, and stop.** A wrong brief item is Wednesday's error.

## OPEN QUESTIONS FOR WEDNESDAY (answer them in your plan mail; the drafter's recommendation follows each)
- **Q-DISK:** 30 images against ~8,657 MB of headroom on kintsugi, after per-image dips of 8,222 MB (17 images) and 5,635 MB (29 images) in the last two rounds. *Recommendation:* forecast at ITEM 0; if it crosses the guard, STOP at the plan; nothing is pruned without Wednesday's ruling (deletion is a Kam-class question).
- **Q-DEMO-STOP:** does the single GO also release demo's STOP 1-demo and STOP 2-demo (038a on live data), or does each need an ANSWER? *Recommendation:* each needs Wednesday's ANSWER, under the same GO; no new GO subject.
- **Q-PETER-MERGES:** #1390, #1391 and #1392 are merge commits by Peter, outside our QA gate. Measured: none reaches an image. *Recommendation:* deploy DEVELOP_AT_DEPLOY whole; record those three as "no image input" in the report.
- **Q-1383:** Kam's card says #1383 merges straight after this build reaches kintsugi and demo. *Recommendation:* Wednesday holds #1383's merge until this seat's demo DEPLOYED mail; if it lands earlier, it is a develop move (STOP-and-mail) and it is NOT deployed in this round.
- **Q-SWEEP-DEMO:** what makes demo's sweep "clean"? *Recommendation:* this round's R rows + dist-bytes for every row in ITEM 6, plus D 7th's shipped-code markers (`2026-10-05_seatD-7th/boot/markers_live.tsv`, 15 rows, and its `deploy/distbytes*` probes; its handover counts 22 shipped-code rows) as a dist-bytes check, because demo has never received them.

RULED BY KAM, NOT YET IN AN ARTEFACT
- `secuura-headroom-before-90pct-stop-1006` = a: "Spark pipeline first, then one deploy". **This brief is its deploy artefact.**
- `secuura-ks1404-anchors-before-049-merge-order-1005` = a: "Hold #1383's merge until the anchor wiring has merged … The build that has the wiring and no 049 goes to kintsugi, gets swept, then goes to demo. #1383 merges straight after." → this round is that build.
- `secuura-tenant-isolation-migration-ks1401-1005` = a: "it lands with the kintsugi deploy card, never demo". Later read by Kam's 19:52 merge-order card ("so demo can get both in October"). Not in this round: 049 is unmerged.
- `secuura-connector-allowlist-missing-setting-ks1256-1005` = b ("Keep 'no restriction' when unset") and `secuura-ks1256-redis-outage-stops-connector-creates-1006` = a ("Accept: fail closed (503) during a Redis outage"): both shipped in #1396; you name the 503-on-outage behaviour in STATUS.
- `secuura-uuid-revokes-never-wrote-status-history-1006` = c ("Don't measure"): no SELECT over past revokes on either box.
- `secuura-ks1404-tsa-trust-and-library-1004` = a: one provider's root (D-Trust), shipped in #1388; you measure that it is wired.
- Demo cards ruled and not yours (`secuura-demo-kam-admin-default-password` = b, `secuura-demo-admin-mfa` = later, `secuura-demo-admin-transcripts` = redact, `secuura-f5-demo-exposure-probe` = probe, `secuura-f5-demo-interim-mitigation` = letitland): change nothing they name.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- KS-1054's probe is `/health/deep`, never `/health` (ANSWER 2026-09-30T12:37:50Z).
- A gate that trips on the instrument: fix, re-prove, resume. A gate that trips on a reading: STOP and mail (same ANSWER).
- Migration pending is counted per DB by the runner's `/platform/i` routing, never the whole set against one tracker (ANSWER to D 7th 2026-10-05T06:25:12Z ruling 4).
- dist-bytes uses the newest rollback tag that PREDATES each fix; where none does, PRESENT-ONLY, ONE-SIDED, stated as such (ruling 6).
- A kintsugi in-place PASS is a DONE CANDIDATE ONLY; the §5f status stays `live sweep owed` (ruling 7, Q-5F).
- L rows only as a dedicated test/QA account, never a human's; W rows not run unless named (rulings 8, 9).
- The clone-not-worktree assertion replaces the moving `.git/worktrees` count (ruling 2).
- A GO is read from the SUBJECT, never the body (ruling on Seat E 8th's QUESTION, 2026-10-06 18:38).
- For October, "deployed" = kintsugi, then demo once kintsugi sweeps clean; demo does not wait for Peter's nod. The Peter/Stuart deploy notice is HELD for Kam's word.

PROVENANCE:
- develop f556373b941823931a9858a788c478e50e822a79 at origin; refs/pull/1395/head 1bdfbe0f2f06; refs/pull/1383/head 32e8459bc0f5 (both open) | `env -u GIT_SSH_COMMAND git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files -c core.sshCommand=<its own config> ls-remote origin refs/heads/develop refs/pull/1395/* refs/pull/1383/*` 08:36:27Z rc 0 | read 2026-10-06
- tree 1aa966ca162b; 46c3e20cfbd2 ancestor (rc 0); range 25 commits / 14 first-parent / 134 files / 69 Dev; first-parent list; 0 .sql, 0 migrations paths; compose + timestamping Dockerfile diffs; compose ${VAR names 97 → 98 (+TSA_TRUST_ANCHORS_PEM) | `git clone --shared --no-checkout` into /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f0e28319-8d07-45b6-8996-e0df55e228d3/scratchpad/deploydraft/repo + `fetch git@github.com:Secuura/Distributed_Secuura.git <sha>` rc 0; `rev-list --count`, `log --first-parent`, `diff --name-status`, `comm` | read 2026-10-06
- 30-image rebuild set and its controls | `python3 -I -B /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatD-7th/boot/service_mapd7.py <scratch repo> 46c3e20c… f556373b…` rc 0, 186 lines | read 2026-10-06
- #1395 touches originate db.ts + one test + two Projects Documents html, 0 migration/compose/env paths | `git diff --name-status $(merge-base 1bdfbe0f2 f556373b9) 1bdfbe0f2` in the scratch repo | read 2026-10-06
- KS-1256 reads Redis platform-settings, no env var; 503 on unavailable/throw | `git show f556373b9418` (body + verification.ts diff) in the scratch repo | read 2026-10-06
- demo range 0f8fb33c3..f556373b9418: 600 / 464 / 1152 / 534 Dev / 28 packages/shared; 038a A, 039 M, docker/init M ×2, run-migrations.sh M; compose + ADMIN_USER_PASSWORD, GATEWAY_VOUCH_SECRET, TSA_TRUST_ANCHORS_PEM; 50 .sql at develop; ADMIN_USER_PASSWORD seeder note at compose 789-811 | `rev-list`, `diff --name-status`, `comm`, `ls-tree`, `git grep` in the scratch repo | read 2026-10-06
- kintsugi at 46c3e20cfbd2 (D 7th FINAL STATE 08:01:19Z 10-05), its sets, REVISION, disk, trackers, error baseline, KS-535 hashes, /health/deep, traps, demo NOT RUN | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD7-kintsugi-deploy.md lines 1-240 | read 2026-10-06
- no deploy after D 7th; D 8th read both boxes read-only (TSA, compose files) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md headers lines 25-987 (`grep '^## 2026-10-0[56]'`) and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD8-2026-10-05.md lines 1-20 | read 2026-10-06
- demo last recorded 0f8fb33c3 (s169 09-10), KS-535 demo 12ea1a07174c3f50, ~600 MB net build, disk transient peak | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md lines 7443-7500 | read 2026-10-06
- demo box facts (ARM64 2 vCPU 4 GiB + 6 GiB swap, IP, key, stack path, front URL) and the KS-535 rule | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 10-20 | read 2026-10-06
- Wednesday's rulings 2, 4, 6, 7, 8, 9 to D 7th | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatD-7th/mail/answer1.txt lines 1-18 | read 2026-10-06
- October grant text, expiry, how-to-apply; EXPIRING-GRANTS rows 10 and 12 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md lines 1-29; /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md lines 10, 12 | read 2026-10-06
- Kam 19:30:43 grant and reading | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-06_use-to-100pct-spark-all-tickets-one-or-two-deployers.md lines 1-26 | read 2026-10-06
- kintsugi-first + KS-535 text | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_kintsugi-first-then-demo-behind-gates.md lines 11-58 | read 2026-10-06
- card options and ruled_ts (headroom 19:31:10; anchors-before-049 a; tenant-isolation a; uuid-revokes c; ks1256 redis a; allowlist b; demo admin password b) and 59 undelivered secuura- rulings | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show <id>` and `list ruled --undelivered secuura-` rc 0 | read 2026-10-06
- merges #1381-#1397 verified at source by Wednesday; Peter's #1390-#1392; GO-from-subject ruling (E 8th 18:38); R 2nd live; drafter commissioned | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-10-05.md lines 239, 268, 278, 289, 313; /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-10-06.md lines 55, 79, 218, 236, 293, 302, 310, 317, 322 | read 2026-10-06
- seat census: `seat d 12th` 0, `seat d 11th` 1; d12 bounded 2 (plan labels); deploy-clones listing; D 11th inbox tools at raise/ | `/usr/bin/grep -c -i` and `grep -o -i -E` over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md; `ls` and `find` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/deploy-clones and 5_Project_History/2026-10-06_seatD-11th (Secuura/Blockchain project) | read 2026-10-06
- pane names (Secuura/Blockchain-D line 16, -R line 20); inbox routing (-D line 38, -R line 42) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/launchers.conf; /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf | read 2026-10-06
- §5f and §3 text; runbook sections | `git show f556373b9418:.claude/skills/secuura-test-discipline/SKILL.md` lines 260-287, 540-552; `git show f556373b9418:Blockchain/Dev/deployment/KINTSUGI-REBUILD-RUNBOOK.md` (445 lines, headings) | read 2026-10-06
- standing lines cited (96, 109, 270, 288, 338-341, 392, 394, 395, 397, 400, 402, 406, R 1st precedence) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md (414 lines) | read 2026-10-06
- KS-1256 In Progress; KS-1278 In Progress; KS-1425 In Progress; KS-723 In Progress; KS-938 In Progress; KS-1305 In Progress; KS-1404 In Progress; KS-1210 In Progress; KS-1005 In Progress; KS-1388 In Progress; KS-1345 In Progress; KS-1330 In Progress | Linear GraphQL https://api.linear.app/graphql `issue(id)` with LINEAR_API_KEY from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env, 08:39:15Z, control KS-99999 NOTFOUND | read 2026-10-06
- KS-1408 Done; KS-1411 Done; KS-1401 In Progress; KS-1376 Backlog; KS-1402 In Progress; KS-1054 In Progress; KS-1348 In Progress; KS-535 Done (archived; its title is an anchor-status defect, the fleet's "KS-535 rule" is the wallet rule in the project CLAUDE.md); KS-641 Deployed to UAT (archived) | same Linear read, 08:39:15Z | read 2026-10-06
- UNMEASURED by the drafter (no host contacted): both boxes' running SHA, census, disk, REVISION, tags, trackers, error baselines, today's KS-535 hashes, /health/deep, timestamping and Redis readings, demo's compose project/profile and live front, whether the NSG still admits this Mac's egress, every sweep result, build-time and disk forecasts | stated as UNMEASURED; the drafter connected only to github.com and api.linear.app | read 2026-10-06

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-06 19:52
    - One SHA rule everywhere: DEVELOP_AT_DEPLOY read at ITEM 0; demo gets the kintsugi-swept SHA; a develop move after ITEM 0 is STOP-and-mail in BLUF, ITEM 2, ITEM 7 and STOP-AND-MAIL.
    - STOP 1 precedes any box write; THE GO is subject-borne only; demo needs a clean kintsugi STATUS plus its own two STOPs (Q-DEMO-STOP).
    - Kintsugi range: 0 migrations (BLUF, ITEM 3); demo range: 038a A + 039 M (ITEM 7). 046-048 are named as pre-existing, not new.
    - KS-535 values are inherited and labelled so: kintsugi 695d09df873ff42b / 142098c9528d0188, demo 12ea1a07174c3f50, the same in AUTHORITY, ITEM 0, ITEM 5, ITEM 7, HOLDS.
    - No comment, no ticket state change, nothing to Peter or Stuart: BLUF, ITEM 6, REPORT EVERY DEPLOY, HOLDS.
    - The rebuild set is 30 (not 17) in WHAT THIS ROUND CARRIES, ITEM 0 (c) and Q-DISK.
