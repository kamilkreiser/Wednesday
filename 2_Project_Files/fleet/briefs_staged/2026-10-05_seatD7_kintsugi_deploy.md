# LAUNCH BRIEF — Seat D 7th, Secuura/Blockchain (pane `Secuura/Blockchain-D`, token `d7`) — deploy develop `46c3e20cfbd2` to KINTSUGI, verify the RUNNING box, LIVE-SWEEP the critical path, then demo ONLY on Wednesday's GO — from Wednesday

⛔ **TOP LINE: NO WRITE TO THE SHARED CHECKOUT OR ITS `.git`. NO GIT LOCK. NO REF WRITE IN THE REPO.** Refuse the launcher's boot "pull latest if safe" line, and say so in your plan mail. Do not run `pull`, `fetch`, `checkout`, `reset`, `stash`, `worktree add`, `gc`, `prune` or `repack` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. Its HEAD is local `develop` `c56dd7c32edf` (drafter, `rev-parse HEAD`, 16:2x AEDT), far behind develop. **Never read a repo file from its working tree.** Read with `git show <sha>:<path>` (the objects for both `91a8f6b721bc` and `46c3e20cfbd2` are present; `cat-file -t` returns `commit`), or read your own clone. Your build source is a FRESH CLONE with its own `.git` (ITEM 0 (b)). You take no `.push-lock-*` and you touch none.

## BLUF
- **You are Seat D 7th.** In your project's `history.md`, Seat D 6th is the newest D seat (line 404, KS-1404 merged, round COMPLETE per `HANDOVER-seatD6-2026-10-05.md`). "seat d 7th" has 0 hits; the control "seat d 6th" has 4. Your pane is `Secuura/Blockchain-D`. Four other seats run this wave on the same inbox (CO-TENANT, below).
- **Your one job, in order:**
  1. Deploy develop **`46c3e20cfbd21acee0c67d544180c33deaa4c8ef`** to **KINTSUGI**.
  2. Verify the RUNNING box.
  3. **LIVE-SWEEP** the critical-path tickets that are fixed on develop.
  4. Send Wednesday a STATUS.
  5. **Only on Wednesday's explicit GO** (under the October grant, after kintsugi sweeps clean): run the same phases on **DEMO**.
  6. Write the handover, history entry and WRAP.

  Production does not exist and is not touched. You merge, push, raise and code nothing, write no anchor, post no ticket comment and change no ticket state.
- **Authority (verbatim):**
  - Kam, live board, card `secuura-kintsugi-deploy-for-31oct-1005` = **a**: *"Deploy develop to kintsugi now, then a live-sweep seat"*. Click time 16:22:05 per the wave partition; `decision_queue.sh show` records `ruled_ts=2026-10-05T16:23:06`.
  - Kam's October grant, 16:21:39: *"for the month of October, keep pushing, keep publishing, deploy all that works and is ready but only when its ready.  Deploy to both servers, demo and kintsugi"*. File: `0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md`. It expires at the end of Sat 2026-10-31.
  - Wednesday's reading of the grant: kintsugi first, plus a live sweep; demo after kintsugi sweeps clean. The KS-535 wallet rule, Phase 0, build-all-then-swap and migrations-in-the-middle are unchanged. Production, money, communication to Peter or Stuart, and anything irreversible are unchanged.
- **The pin is FIXED: deploy `46c3e20cfbd2`, tree `dab6adb69ea3c7966ec17111a139bb5bcfadb68c`. Do not chase develop.** The wave partition binds this ("D 7th deploys develop as it stands NOW (46c3e20c)"). Three other seats are pushing this wave: B 61st (merging #1381), F 2nd (the KS-1401 migration) and E 2nd (auth). If `ls-remote` shows develop has moved at ITEM 0, record both SHAs and the first-parent list of the move, and deploy `46c3e20cfbd2` anyway, unless Wednesday's ANSWER says otherwise. **#1381 and the KS-1401/KS-1376 migration are NOT in this round.** They reach kintsugi in a LATER deploy after they merge on a gate GO. That deploy is its own round, with a migration-on-live-data STOP by construction, and Wednesday commissions it separately. **Do not run it, even if both merge while you are live.**
- **From → to:** kintsugi was last recorded at **`91a8f6b721bc`**. Seat B 50th deployed it (FINAL STATE 12:28:23Z 2026-09-30), and Wednesday verified it externally at 12:37:36Z (`HANDOVER-seatB50-kintsugi-deploy.md:21-40`). The drafter found no later kintsugi deploy in `history.md` lines 1-1526 or in Wednesday's daily notes for 10-01 to 10-05. **The box's state since then is UNMEASURED.** Measure it at ITEM 0.
- **This is a SMALL round.** The range `91a8f6b721bc..46c3e20cfbd2` is **17 commits / 15 first-parent / 85 files / 46 under `Blockchain/Dev`**. It contains **0 `.sql` and 0 migration paths**. It does not touch `docker-compose.yml`, `.env.example`, `packages/shared`, `docker/init`, `scripts/run-migrations.sh` or `services/api-gateway`. The 39 non-Dev paths are `systemTest/akto` and `Projects Documents`. Instrument: drafter, `diff --name-status`/`--stat`, READ verbs on the shared `.git`.
- **Expected rebuild set: 17 images.** The drafter ran B 50th's own `service_map.py` read-only (it only uses `git show`) over the range; output is at `scratchpad/d7/service_map.out`, rc 0, with 7 controls. The 17 are: admin-frontend, analytics, anchoring, api-gateway, auth, billing, governance, kyc, m365-integration, migrations, nft-certificate, originate, referral, tenant-provisioning, timestamping, transfer and verifier-frontend. The other 16 build services have no changed input. B 50th took 2 h 08 min for 29 images; this round is roughly 60% of that work (UNMEASURED estimate).
- 🔴 **THE CARD'S PREMISE IS STALE, and this changes what the sweep proves.** The audit SUMMARY and the card's BLUF both say "kintsugi was last recorded on develop on 23 Sep". That is wrong: B 50th deployed `91a8f6b721bc` on 09-30, and Wednesday's own daily note 10-01 12:23 says so. Measured at source by the drafter (`merge-base --is-ancestor`), **29 of the 32 critical-path MERGED-AWAITING-SWEEP tickets in `audit_A.tsv` are already ancestors of `91a8f6b721bc`**. So they are probably already on kintsugi and **were deployed but never swept**. Only **3 are new in this round**:
  - **KS-1402** (`2d85b84e1`, #1374);
  - **KS-1404** (`14d40d445`, #1376; its subject carries no `(#n)`);
  - **KS-1399** (`723dc0722`, #1363, lockfiles only, no runtime surface).

  The sweep is owed for all 32 either way.
- 🔴 **KS-1404 lands FAIL-CLOSED on kintsugi, and that is a behaviour change the sweep must name.** These facts were read at `46c3e20` by the drafter:
  - the timestamping verifier refuses every real RFC 3161 DER token unless `TSA_TRUST_ANCHORS_PEM` is set (`qualified-tsa.ts:389-410`; `config/README.md:24-31`);
  - `docker-compose.yml`'s `timestamping` environment (lines 1225-1242+) does not pass that variable;
  - the runtime stage of `services/timestamping/Dockerfile` copies only `package*.json` and `dist`, so `config/tsa-trust-anchors.crt` is **not in the running image** (`build` is bare `tsc`). Pointing the variable at that path inside the container would therefore read nothing.

  Expected after the deploy: new real tokens verify `false` with reason `no trust anchor configured`. Stored rows still verify through the DB branch. **Measure it, report it and do not fix it.** No `.env` edit and no override edit. Kam's card `secuura-ks1404-tsa-trust-and-library-1004` (a) is **half done**: no seat has yet measured "`TSA_URL` per environment". Your ITEM 0 read of `TSA_URL` on each box is the first.
- **Demo (ITEM 7) is a BIG round, not this one's twin.** Demo's last recorded deploy is **`0f8fb33c3`** (s169, 2026-09-10, `history.md:5995`), UNMEASURED since. The range `0f8fb33c3..46c3e20cfbd2` is **575 commits / 450 first-parent / 1116 files / 522 under Dev**. It contains:
  - **A `038a`** and **M `039`**;
  - **M `docker/init/01-schema.sql` + `06-m365-tables.sql`**;
  - **M `run-migrations.sh`**;
  - **compose with two NEW variables, `ADMIN_USER_PASSWORD` and `GATEWAY_VOUCH_SECRET`**;
  - 30 files under `packages/shared`.

  Demo is ARM64, 2 vCPU, 4 GiB + 6 GiB swap (project `CLAUDE.md:12`), with ~11 GB free recorded on 09-10. It gets its own ITEM 0, its own plan STOP and its own migration STOP.

## THE PROCEDURE — PROVEN, COPY IT
Your project tree is `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/`. Read these first, by section:
1. `5_Project_History/HANDOVER-seatB50-kintsugi-deploy.md` (229 lines, whole). It holds the FINAL STATE, the rollback recipe, **the `/health` vs `/health/deep` correction**, the RLS finding, box facts, KS-535 and nine instrument traps.
2. **B 50th's scripts are the newest proven set.** Copy `5_Project_History/2026-09-30_seatB-50th/boot/` and `deploy/` into **`5_Project_History/2026-10-05_seatD-7th/`**. That includes `phase4_remote.sh` **v2**, the fixed gate. Never copy `phase4_remote.sh.v1-broken-gate`. Re-key before any use:
   - **tokens:** `seatB50`, `B50`, `B 50th` (as prose), `.rebuild-seatB50/`, `pre-20260930`, `new-20260930`, every older generation (`2026092[0-9]`, `seatB23`/`B23`, `seatA16`), env-var prefixes and absolute paths;
   - **non-token constants a token map cannot see:**
     - `phase0_remote.sh` `SCOPED` (29 → your measured 17) and `WANT_N`;
     - its precheck control `pre-20260923 count must be 29` (→ `pre-20260930` must be 29);
     - its fingerprint list (add `pre-20260930`);
     - `phase4_remote.sh:10` `ORDER` (28 → your measured swap set);
     - **`phase4_remote.sh:23-40`'s 038a gate.** That gate re-measured 038a for B 50th's round. This round has no new migration, so the gate becomes "0 unrecorded files in the clone's `migrations/`, measured in the same action, immediately before the api-gateway recreate".
   - **lettered tokens:** grep the copies for `int(`, `\d\d`, `[0-9]{2}` and `4[0-9]` (STANDING_LINES 391-392).
   - **the proof:** prove the re-key with a control that goes the other way.
3. **Inbox tools: the D lane's newest.** Copy `5_Project_History/2026-10-05_seatD-6th/raise/inbox_matchd6.py`, `inbox_watchd6.sh` and `watchproofd6.sh`. Re-key `d6` → `d7`, **including the DATA** (D 6th's trap 3: `wants.tsv` declared the predecessor's own LAUNCH BRIEF as FOR ME). Do not run them from D 6th's folder.

**Order:**
1. ITEM 0 MEASURE (read-only).
2. Plan confirmation mail: **STOP 1**.
3. Phase 0 re-tag.
4. rsync and build EVERYTHING, swapping nothing.
5. Migrations check, in the middle (STOP 2 only if anything is pending).
6. Swap one service at a time.
7. Verify the RUNNING box.
8. **DEPLOYED mail.**
9. LIVE SWEEP.
10. **STATUS mail.**
11. Demo only on GO.
12. Handover, history, WRAP.

### HOW YOU REACH THE BOXES (the drafter connected to neither)
- **Kintsugi:** `ssh -i "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/vm_secuura02_kintsugi" -o IdentitiesOnly=yes secuura@20.198.226.148`.
  - Facts: VM `secuura02-kintsugi-vm`; stack `/home/secuura/secuura/Dev`; compose project `dev`, `--profile phase2`; gateway `localhost:6882`; public front `https://kintsugi.secuura.net`.
  - B 50th inlined the `ssh -i` form, and there is **no `~/.ssh/config` alias** for either box (drafter: `Host` lines in `~/.ssh/config` name only `github-secuura`). The key file exists (399 B, mode 600, `ls -la`).
  - The NSG admits ONE `/32`. B 50th's egress `157.211.46.215` matched it on 09-30. **If SSH fails, STOP and mail your egress address. Never read or touch the NSG.**
- **Demo (ITEM 7 only):** `ssh -i ".../3_Access_Keys/vm_secuura02_demo" -o IdentitiesOnly=yes secuura@20.212.118.59` (project `CLAUDE.md:12`; key 411 B, mode 600).
  - Facts: VM `secuura02-demo-vm`; stack `/home/secuura/secuura/Dev` (`CLAUDE.md:18`).
  - **UNMEASURED by the drafter:** demo's compose project and profile, its NSG, and its public front. `CLAUDE.md:13` names `https://secuura02-demo.southeastasia.cloudapp.azure.com`; lesson `2026-09-10_kintsugi-first-then-demo-behind-gates.md:28` names `demo-pk.secuura.net`. Measure which one serves.
- **zsh traps:**
  - **a zsh scalar does not word-split.** `SSHC="ssh -i …"; $SSHC host` → rc 127 (B 50th trap 2). Inline the ssh.
  - `cd X && nohup … &` backgrounds the `cd` too (trap 6).

### ITEM 0 — MEASURE (read-only everywhere)
- **(a) develop:** run `ls-remote` from the shared checkout. It is a READ verb, and the checkout's `core.sshCommand` carries the on-disk `-i …/3_Access_Keys/github_deploy_rw` key. Report the full SHA, and name it as `ls-remote` (STANDING_LINES 287). If it is not `46c3e20cfbd2`, give the first-parent list of `46c3e20cfbd2..<new>` and say whether it holds any `.sql`, `migrations/` path or #1381. **Deploy `46c3e20cfbd2` regardless** unless ANSWERed otherwise.
- **(b) the build source, a FRESH CLONE:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/deploy-clones/seatD7-46c3e20cfbd2`. `deploy-clones/` holds `seatA16-3bad652d1`, `seatB23-6ab9d5021` and `seatB50-91a8f6b721bc` today.
  - Command shape: `git -c core.sshCommand='ssh -i …/3_Access_Keys/github_deploy_rw -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new' clone --no-checkout git@github.com:Secuura/Distributed_Secuura.git <dir>`, then `checkout --detach 46c3e20cfbd21acee0c67d544180c33deaa4c8ef`.
  - Assert: `rev-parse HEAD` == the pin; `HEAD^{tree}` == `dab6adb69ea3…`; porcelain is empty; the shared `.git/worktrees` count is UNCHANGED (**490** at the drafter's `ls | wc -l`, 16:3x).
  - Never `worktree add`. Never `--reference` the shared `.git`.
- **(c) the rebuild set, BY MEASUREMENT:** run your re-keyed `service_map.py` in your clone over `<box's MEASURED SHA>..46c3e20cfbd2`.
  - If the box is at `91a8f6b721bc`, the drafter expects the 17 listed in BLUF, with these reasons: api-gateway via `docs/openapi/secuura-api.yaml`, which is COPY + a bind mount; migrations + originate via `services/originate/`; the three frontends and governance/kyc via their lockfiles; the rest via their own `src`/openapi/lock paths.
  - **If the box is NOT at `91a8f6b721bc`, the set will be larger. Re-derive it, say so, and STOP for the plan.**
  - Report per image: in or out, and the path that put it in.
- **(d) kintsugi as it runs.** Read key NAMES only, never values. Measure:
  - **the deployed SHA:** hash the range's `Blockchain/Dev` paths on the box against BOTH `91a8f6b721bc` and `46c3e20cfbd2`, and plant one path the check must catch. Read `REVISION`: B 50th left sha16 `921a8d3b1fa0b5df`, 7,421 B.
  - **the census:**
    - B 50th left 32 healthy, 0 restarts except demo-service's KS-641 FATAL loop (~18 and climbing). Judge that loop by Id + Created + image, never by health.
    - `guardian` and `queue` exist only under `--profile phase2`.
  - **the rollback sets:** B 50th left nine, all fingerprint-identical. Re-read each fingerprint and count.

    | set | count | fingerprint |
    |---|---|---|
    | `pre-20260930` | 29 | `a07a76adebb7ee72` |
    | `pre-20260923` | 29 | `6b7a5bf6dc94db38` |
    | `pre-20260922` | 29 | `11910b7520c17cd4` |
    | `pre-20260919c` | 3 | — |
    | `pre-20260919b` | 3 | — |
    | `pre-20260919` | 33 | — |
    | `pre-20260918` | 33 | — |
    | `pre-2026-09-12` | 33 | — |
    | `pre-20260910` | 31 | — |
  - **disk:**
    - B 50th ended at **19,548 MB free**. Its 29-image build dipped **5,635 MB** (23,643 → minimum 18,009).
    - Forecast your 17-image dip from B 50th's per-image build log, not by ratio. State the arithmetic against the **4,000 MB minimum-free guard**.
    - Read disk **SETTLED**. The immediate-after-build reading is the transient peak (s169, `history.md` ~6028).
  - **the DB:** expect tracker rows **49**, highest file `048_ks754_widen_processed_by_to_text.sql`, and `038a` recorded = 1. List the clone's `migrations/*.sql` (52 tree entries at `46c3e20`, identical in count at `91a8f6b`) against `_secuura_migrations`, and report how many are UNRECORDED: 0 expected, with a planted fake filename that must read pending. Migration 048 must be recorded (STANDING_LINES 109); if it is not, STOP.
  - **the error-line baseline** (`errbase_remote.sh`). B 50th's is 4 distinct lines: billing `permission denied for schema public`, security `audit_logs.details … must be owner`, staking missing `svc_accumulated_rewards`, and demo-service KS-641.
  - **KS-535 BEFORE:** `sha256[0:16]` of `PLATFORM_WALLET_MNEMONIC` and `BLOCKFROST_API_KEY`, from `.env` AND from the running anchoring container.
    - B 50th read `695d09df873ff42b` / `142098c9528d0188` both before and after.
    - **Demo's mnemonic hash is `12ea1a07174c3f50`. Kintsugi's MUST differ.**
    - Run three controls: `$HOME` expands; the literal-string artefact reads `1d99a769a815b299` (the quoted-heredoc trap, a FALSE breach); the empty string reads `e3b0c44298fc1c14`.
    - *(Kintsugi's Blockfrost key was ruled by Kam to be demo's at one point (`history.md:13458`). KS-535 is about the MNEMONIC. Report the Blockfrost hash for before/after equality only.)*
  - **KS-1054 BEFORE — `/health/deep`, NEVER `/health`.**
    - `localhost:6882/health` is nginx's hard-coded 179 B `return 200` literal (`nginx-demo.conf`), so it can never carry `startupMigrations` (B 50th handover lines 3-19; Wednesday accepted that error as hers).
    - Read `curl -s localhost:6882/health/deep`. B 50th after: `startupMigrations {ran:true, applied:47, failed:0}`.
    - Run your clone's `Blockchain/Dev/deployment/azure/check-startup-migrations.sh '<body>'` on it. Expect **rc 0**.
    - Keep the `/health` body as the "cannot discriminate" control: rc 2 on both bases.
  - **KS-1404 env, on the running timestamping container:**
    - `TSA_URL`: its VALUE, which is a URL and not a secret, or ABSENT/EMPTY;
    - `TSA_TRUST_ANCHORS_PEM`: PRESENT/ABSENT/EMPTY only. Expected ABSENT, because compose does not pass it;
    - whether `/app/config/tsa-trust-anchors.crt` exists. Expected ABSENT; `dist` only.

    Plant a control on each read: a variable you know is set, such as `PORT=4004`, must read PRESENT.
- **(e) THE SWEEP PLAN (ITEM 6), proposed now, run later.** Build one row per ticket below. Each row gives:
  - the **fix commit** and whether it is an ancestor of the box's MEASURED pre-deploy SHA;
  - a **class**:
    - **R** — read-only and anonymous;
    - **L** — needs a login. A login WRITES `lastLoginAt`;
    - **W** — writes rows or calls out;
    - **X** — not probeable on this box, with the reason (e.g. KS-1054's case needs a FRESH database; KS-1369's needs load);
  - the probe, its expected result, and a control that can fail.

  Every row ALSO gets a **dist-bytes check**: a marker from the fix's own diff is present in the RUNNING container's `dist` and absent in the `:pre-` image (A 16th's V1 shape, `history.md:2977`). That proves DEPLOYED. It does not prove the behaviour.

  **L-class and W-class probes run only if Wednesday confirms them by name at STOP 1. R and dist-bytes need no extra word.**
- **(f) PLAN CONFIRMATION — STOP 1.** Subject: `[Secuura/Blockchain-D -> Wednesday] QUESTION: plan confirmation (Seat D 7th)`. Include:
  - the pin and develop-at-origin;
  - the clone's HEAD and tree;
  - the box's measured SHA against B 50th's record, with every difference named;
  - the rebuild set per image with its reason;
  - the disk arithmetic;
  - the Phase 0 stamp. Expected `pre-20261005`: take it from the box's UTC clock at Phase 0, and check by name AND id that it does not already exist. Give the tag count you will assert (expected 17);
  - the ordered swap plan, with the exact rollback for each service;
  - the migration reading;
  - the KS-535 BEFORE hashes;
  - the `/health/deep` BEFORE reading;
  - the KS-1404 env reading;
  - the sweep table from (e);
  - **Q-5F** (below);
  - the wall clock;
  - **the launcher's preflight warnings VERBATIM** (D 6th recorded F-02 "no SSH identity seeded", which is inert for a no-push seat);
  - **anything here your measurement contradicts.**

  **Wait for CONFIRMED.**
  - **Q-5F (Wednesday rules it; do not decide it yourself):** `secuura-test-discipline` §5f (`SKILL.md:540-550` at `46c3e20`) requires the live sweep "against a fully torn-down and rebuilt environment (§3), with all containers verified up". §3 (`:260-286`) means `down --volumes --rmi all` and a prune. **Kintsugi is swapped in place and can never be torn down this way** (it has live data, KS-535, and no prune). So a kintsugi PASS is a **close CANDIDATE**, and whether it satisfies §5f is Wednesday's ruling. Ask it as one question.

### ITEM 1 — Phase 0 re-tag
Re-tag every image the rebuild will overwrite, `:latest` → `:pre-20261005`, by name and id. Assert the count (17 if unmoved). Assert the nine older sets are byte-identical before and after (fingerprints). **No prune of any kind. No image deletion, `--remove-orphans`, `down`, `-v` or `rm`.** `--remove-orphans` deletes guardian + queue.

### ITEM 2 — rsync + build everything, nothing swapped
- **rsync from the CLONE** (`-a -c`, no `--delete`).
  - `.env`, `.env.local` and `docker-compose.override.yml` stay untouched: stat them before and compare after.
  - The content-file list must equal git's.
  - **Write an IN-PROGRESS `REVISION` at rsync time** and keep B 50th's beside it. The final one is written only once verified (B 50th: a `REVISION` must never claim a revision the containers are not running).
- **Build:** serial, `COMPOSE_BAKE=0`, `docker compose -p dev --profile phase2 --progress plain build <svc>`. **Never `-f`**: the untracked override feeds auth.
  - Each build: `cmd > out 2>&1; rc=$?`, with rc on its own line, never piped.
  - Use a fresh `.rebuild-seatD7/`. Stale `done.txt` files SKIP builds.
  - Record per image: rc, NEW id vs `:pre-20261005`, and the minimum free disk.
- **A build failure costs nothing: STOP and mail. Never deploy a partial set without Wednesday's word.**

### ITEM 3 — migrations: expected to be a measured NO-OP
- The range holds 0 `.sql` (drafter). **api-gateway's `startup-migrations.ts` scans `migrations/` when it boots.** Recreating api-gateway RUNS any unrecorded file.
- **Immediately before the api-gateway recreate, in the same action:** re-count the unrecorded files in the clone's `migrations/` against `_secuura_migrations`. **0 → proceed. Anything else → STOP 2** with the file names: `[Secuura/Blockchain-D -> Wednesday] QUESTION: unexpected pending migration (Seat D 7th)`. Apply nothing.
- **`dev-migrations` is rebuilt** (its Dockerfile COPYs `services/originate/`). Following B 50th, it is **NOT recreated**: it is a one-shot, there is nothing new to apply, and its baked `exit 4` stays unexercised. Say so in the plan. If you think it should run, ask.
- **The KS-1401/KS-1376 migration is NOT this round** (wave partition, line 26). If it has merged by the time you are here, it is still not yours.

### ITEM 4 — swap one service at a time
- **Expected swap set: 16** (the 17 minus `migrations`). Order: analytics, auth, billing, governance, kyc, m365-integration, nft-certificate, referral, tenant-provisioning, timestamping, transfer, originate, **anchoring, api-gateway** (last among the backends), then admin-frontend, verifier-frontend.
- Command: `docker compose -p dev --profile phase2 up -d --no-deps --force-recreate <svc>`, with a health read between swaps.
- **After api-gateway's recreate,** assert the yaml bind mount's container inode == its host inode (`phase4_remote.sh:14` shape), and that the served yaml's md5 == your clone's. The yaml changed this round (+83 lines).
- **On an unhealthy service:** run `docker tag dev-<svc>:pre-20261005 dev-<svc>:latest` and the same `up -d`, then STOP and mail the state of every service. Keep the new image as `:new-20261005`.
- **B 50th's traps:**
  - `phase4.sh` truncates `swapped.txt` and the launch redirect overwrites `phase4.master.log`. Copy both before any re-run.
  - **A gate that trips on the INSTRUMENT is fixed, re-proved and resumed. A gate that trips on a READING is a STOP and a mail** (Wednesday's ANSWER, 2026-09-30T12:37:50Z).

### ITEM 5 — verify the RUNNING box, not the steps' exit codes
- **Census vs ITEM 0:**
  - **Settled:** at least 300 s after the last swap, 0 restarts (except the KS-641 loop), and error lines == the ITEM 0 baseline with ZERO NEW lines.
  - Every non-swapped container is untouched, with a planted change caught.
  - Ten rollback sets are intact.
  - `GATEWAY_VOUCH_SECRET`: NONEMPTY 0 (B 50th's V10).
  - The final `REVISION` == the pin, written now.
- **KS-1054 on the live box:**
  - (i) `/health/deep` carries `startupMigrations` with `ran:true`, `failed:0`;
  - (ii) `check-startup-migrations.sh` gives **rc 0**. Controls on the same body: `failed` set to 1 → **rc 1**; a broken `python3` shim first on PATH → **rc 1** with "python3 is NOT on PATH or does not run"; the nginx `/health` literal → rc 2;
  - (iii) the api-gateway startup-migration log lines, verbatim. Expect file-stage `applied:0`.
  - Also read `https://kintsugi.secuura.net/health/deep` from the Mac (HTTP status + the same block).
- **KS-535 AFTER the restart:** both hashes == ITEM 0's, and the mnemonic hash != `12ea1a07174c3f50`. `.env` byte-identical (B 50th: sha16 `634e99a79cbc6ee5`, 16,719 B). The same three controls.
- **KS-1404 AFTER:** the same three env reads as ITEM 0 (d), on the NEW timestamping container.
- Print ratios (`N / N`), never "all". A probe you cannot run is **NOT RUN, with the reason**.
- **Then mail** `[Secuura/Blockchain-D -> Wednesday] DEPLOYED: kintsugi at 46c3e20cfbd2 (Seat D 7th)`. Include:
  - the full SHA;
  - per-service image ids, before (`:pre-20261005`) and after;
  - the migration count;
  - the raw `/health/deep`;
  - KS-535 (hashes and verdicts only);
  - the KS-1054 readings with their controls;
  - the KS-1404 env reading;
  - the settled census.

  **Go straight on to ITEM 6 in the same turn.**

### ITEM 6 — LIVE SWEEP of the critical path (read-only unless confirmed at STOP 1)
**The checklist is `audit_A.tsv` rows with `critical_path_31oct` starting `yes` AND `class == MERGED-AWAITING-SWEEP`: 32 rows** (drafter, `awk -F'\t'` on columns 12 and 2; 56 critical-path rows in total). The other 24 critical-path rows are GENUINE-DEFECT, HARDENING, NEEDS-HUMAN, TOOLING or UNVERIFIED. They have no fix to sweep, and are not yours.

Ancestry of each fix commit in `91a8f6b721bc` (drafter, `git log --grep` on the PR number + `merge-base --is-ancestor`). Re-derive this against the box's MEASURED pre-deploy SHA:
- **NEW in this round (3):**
  - KS-1404 `14d40d445` (#1376; the subject has no `(#n)`, found by its `KS-1404:` subject in the first-parent list);
  - KS-1402 `2d85b84e1` (#1374);
  - KS-1399 `723dc0722` (#1363). Lockfiles only, so class **X**: a push-gate fix with no runtime surface.
- **Already in `91a8f6b721bc` (29):** KS-1375 · KS-1371 · KS-1370 · KS-1369 · KS-1352 · KS-1348 · KS-1341 · KS-1284 · KS-1283 · KS-1269 · KS-1244 · KS-1232 · KS-1231 · KS-1228 · KS-1215 · KS-1207 · KS-1202 · KS-1195 · KS-1187 · KS-1175 · KS-1054 · KS-1028 · KS-999 · KS-974 · KS-962 · KS-932 · KS-871 · KS-753 · KS-730.

For each of the 32, report:
- the ticket, the fix SHA, and the dist-bytes result (DEPLOYED / NOT DEPLOYED, with the marker and the control);
- the probe class and result: **PASS / FAIL / UNMEASURED-with-reason**, with RAW values beside every verdict;
- **one drafted §5f line, NOT POSTED**:
  - **not a PASS:** the canonical shape, `Merged <sha> (PR #n, <file>); offline gates green; NOT Done per secuura-test-discipline §5f — live sweep owed (torn-down rebuilt stack, all containers verified up), unverified: <what>` (STANDING_LINES 269-270; the handle `live sweep owed` is lowercase, verbatim);
  - **a PASS:** `Swept live on kintsugi at 46c3e20cfbd2 <UTC>: <probe> → <raw>; control <raw>`.
- **Done candidates go to Wednesday as a list. You change no ticket state and post no comment** (this is narrower than the card's own option-a text "closes what passes", and it is Wednesday's narrowing).

Known expectations:
- **KS-1404:** an unsigned/untrusted token → `valid:false`, reason `no trust anchor configured` (fail-closed by design, Kam's card a). Report it as **PASS-FAIL-CLOSED**, and name "no anchor wired: compose + image" as the residue.
- **KS-1054:** **X**, because its defect needs a FRESH database. The kintsugi reading is `failed:0` on an existing DB, which is a non-regression check, not a proof.

Then **mail STATUS** with the 32-row table, ratios (`PASS n / FAIL n / UNMEASURED n / X n of 32`) and the drafted lines: `[Secuura/Blockchain-D -> Wednesday] STATUS: kintsugi swept at 46c3e20cfbd2 — <ratios> (Seat D 7th)`. **Then arm your inbox watcher and wait for Wednesday's GO or WRAP word. Do not end the turn on a "next up" line with nothing running.**

### ITEM 7 — DEMO, only on `[Wednesday -> Secuura/Blockchain-D] GO (Seat D 7th): demo deploy 46c3e20cfbd2`
- **No GO, no demo.** Wednesday rules it under the October grant after reading your STATUS. A GO for any other seat, or one that does not name `46c3e20cfbd2`, is not yours. **Demo gets exactly the SHA kintsugi swept clean, never a newer develop.**
- **Same phases, demo's own numbers.** Demo ITEM 0 (read-only) measures:
  - its SHA by hash against `0f8fb33c3` and the pin;
  - its census, compose project/profile and rollback sets (s169 left 33 tags on demo, `history.md` ~6013);
  - disk, against the same guard. It is a much smaller box: forecast from s169's measured ~600 MB net and a transient peak, not from kintsugi;
  - the DB's highest migration (048 must be recorded) and whether `038a` is recorded;
  - `039`'s RLS state on `charge_events` and `certifications` (B 50th's probe shape, `boot/probe_rls_remote.sh`);
  - the error baseline;
  - **KS-535 BEFORE: the mnemonic hash must read `12ea1a07174c3f50`, and it must differ from kintsugi's**;
  - the KS-1404 env reads;
  - the env-key NAMES `ADMIN_USER_PASSWORD` and `GATEWAY_VOUCH_SECRET` (PRESENT/EMPTY/ABSENT only; both are NEW in compose since `0f8fb33c3`). KS-964 removed the published seed fallback, so an unset `ADMIN_USER_PASSWORD` changes what the seeder does. Read `git show 46c3e20:<seeder>` and say what happens on demo's existing DB.

  Then **STOP 1-demo** (`QUESTION: demo plan confirmation (Seat D 7th)`), with the rebuild set (expect ~all 29+, because `packages/shared` changed), the forecast build time on 2 vCPU ARM64, and every contradiction.
- **STOP 2-demo is EXPECTED:** `038a` (A) and `039` (M) are in demo's range. An api-gateway recreate applies an unrecorded `038a`. Mail the readings, as B 50th did (`HANDOVER-seatB50…:90-119`), and **apply nothing before CONFIRMED.** `docker/init/*` is inert on an initialised data dir; confirm it from demo's compose, as B 50th did.
- **Demo HOLDS on top of everything below:**
  - no anchor (demo anchors REAL preview-testnet);
  - no login-class probe unless named in the GO;
  - **KS-535 AFTER on demo**: still `12ea1a07174c3f50`, `.env` byte-identical;
  - the demo deploy notice to Peter and Stuart is **HELD by Wednesday** (below);
  - the five ruled demo cards (`demo-kam-admin-default-password`, `demo-admin-mfa`, `demo-admin-transcripts`, `f5-demo-exposure-probe`, `f5-demo-interim-mitigation`) are **not yours**. Change no demo credential or identity.
- Then `DEPLOYED: demo at 46c3e20cfbd2 (Seat D 7th)`, with the same contents as ITEM 5.

### ITEM 8 — handover, history, WRAP
- **Handover:** `5_Project_History/HANDOVER-seatD7-kintsugi-deploy.md`. Put the FINAL STATE first (per box), then the rollback recipe per box, the sweep table, the KS-1404 anchor finding and every trap. Records go in `5_Project_History/2026-10-05_seatD-7th/`. Add a history entry at the TOP of `history.md`.
- **WRAP:** `[Secuura/Blockchain-D -> Wednesday] Session wrap 2026-10-05 (Seat D 7th)`.
- **The clone STAYS:** the follow-up round may reuse its object store, and the drive-hygiene policy (STANDING_LINES 397) excludes anything <3 days old or in use. Report its size. Nothing is deleted.

## CO-TENANT — five seats, one inbox (`secuura-blockchain@agentmail.to`, `inbox_routing.conf` lines 29, 36-40)
- **Yours:** mail tagged `[Wednesday -> Secuura/Blockchain-D]` AND naming **`(Seat D 7th)`**. Every mail you send uses `[Secuura/Blockchain-D -> Wednesday] … (Seat D 7th)`.
- **The other live seats this wave** (wave partition table):
  - **Seat E 2nd** `Secuura/Blockchain-E`, `e2`, `.push-lock-e2`, auth;
  - **Seat B 61st** `Secuura/Blockchain`, `b61`, `.push-lock-56`, merging #1381;
  - **Seat F 2nd** `Secuura/Blockchain-F`, `f2`, `.push-lock-f2`, the KS-1401 migration;
  - **Seat C 23rd** `Secuura/Blockchain-C`, `c23`, Linear board only.

  None of their mail, GOs or locks is yours. **Their merges move develop. That does not move your pin.**
- **OTHER_SEATS/FOREIGN** must hold: `seat d 6th`/`d6`, `seat d 5th`/`d5` (your pane's predecessors), `seat e 2nd`/`e2`, `seat e 1st`/`e1`, `seat b 61st`/`b61`, `seat b 60th`/`b60`, `seat f 2nd`/`f2`, `seat f 1st`/`f1` and `seat c 23rd`/`c23`. `MY_PANE` = `secuura/blockchain-d]`.
  - Match short tokens on word boundaries only. The hex-run control is `d7e95cd9f` (KS-1195's fix commit, which holds `d7` raw).
  - Prove the matcher on REAL subjects still in the inbox: D 6th's (`…QUESTION: plan confirmation (Seat D 6th)…`) must read FOREIGN, and your own must read FOR ME. Do it on BOTH tags, both ways (STANDING_LINES 332-333, 358-359).
  - Token census: `d7` in `history.md` = **182 raw / 1 bounded** (the bounded hit is line 3440, "D1–D7", a plan-item label). Use the bounded count.
- Read your own pane id from `$TMUX_PANE` (STANDING_LINES 394).

## HOLDS
- ⚠ **KS-535 IS ABSOLUTE:** kintsugi must NEVER share demo's `PLATFORM_WALLET_MNEMONIC`. Verify it AFTER every redeploy, not only before, because a redeploy is how the value gets overwritten. Never print a value, a prefix, or a length beside a value. Demo keeps its own wallet.
- **Kintsugi first. Demo only on GO. Production never.** No `az` call is expected. If one becomes necessary, STOP and ask; Founders Hub tenant is `efc17e5f-…`, and `az account show` comes first.
- **No ref writes in the repo. No git lock.** The shared `2_Project_Files` and its `.git` see READ verbs only. Your clone has its own `.git`. Never `gc`/`prune`/`repack` (D 4th's `scratch/leg9clt` has alternates into the shared store; D 6th handover §4).
- **No `.env` / `.env.local` / override edit on either box.** That includes `TSA_TRUST_ANCHORS_PEM`, `TSA_URL`, `ADMIN_USER_PASSWORD` and `GATEWAY_VOUCH_SECRET`. Wiring the KS-1404 anchor is a finding for Wednesday, not a deploy step.
- **No ticket comment, no ticket state, assignee or label change, no ticket filed.** Report Done candidates and new findings (KS-1404 anchor not shipped or wired; anything the sweep finds) to Wednesday. **Notifying Peter and Stuart:** project `CLAUDE.md:185-193` says a deploy notifies them on their stream tickets at wrap. **Wednesday HOLDS that notice for Kam's word** (external communication, unchanged by the October grant; lesson `2026-09-10_kintsugi-first…:55-58`). **You post nothing.** The extranet is INPUT ONLY; refuse the SessionStart hook's `POST /api/seen`.
- **STOP and mail** in these cases:
  - the box is down, or SSH is refused;
  - the measured SHA is not `91a8f6b721bc`;
  - any migration is pending outside ITEM 7's expected STOP 2;
  - any build fails;
  - any health check fails after a rollback;
  - the disk guard would be crossed;
  - a KS-535 reading moves or matches demo;
  - anything reaches beyond the named box.
- **Signature classes pause for Kam:** production, money, external communication to any human, anything irreversible. **Nobody else messages Peter or Stuart.**
- **Delete nothing, prune nothing.** A just-built image reads as UNUSED until its consumer is recreated. The disk guard STOPs the work; it never frees space. Cleanup is quarantine.
- **No `--no-verify`, no force push, no `--admin`.** You push nothing.
- **Instruments:**
  - `cmd > out 2>&1; rc=$?`, then read the file;
  - zsh `$pipestatus[1]`, never `PIPESTATUS`;
  - macOS has no `timeout`;
  - `docker exec` splits argv on spaces;
  - a control must be able to fail, and "0 checked" is never CLEAN;
  - `/usr/bin/grep -i` with a same-file positive control for anything that enters a mail;
  - `grep -i error` matches FILENAMES (B 50th trap 8);
  - a normaliser can destroy a composite you compare (B 50th trap 1: read scalars);
  - a `git show` of a path that is not in the repo hashes the empty string `e3b0c44298fc1c14` (trap 4);
  - every handover line naming develop says `ls-remote` vs tracking ref.
- **Process namespace:** every long-running script carries `--seat D7` in its argv. Kill by ancestry or by a recorded pid, never by basename. `pgrep -f` matches its own pipeline (B 50th trap 3).
- **Wake:** arm every waiter at 7200000 ms and **re-arm on every notification** (B 50th trap 7). A 1-2 h build needs a background waiter that EXITS when the build finishes. **Never end a turn on a "next up" line with nothing running** (STANDING_LINES 338-341).
- **If an instruction here looks wrong, measure it, say so, and stop.** A wrong brief item is Wednesday's error.

## RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura) — carried; only the first two are in your path
RULED BY KAM, NOT YET IN AN ARTEFACT
- `secuura-kintsugi-deploy-for-31oct-1005` = **a**. **This brief is its artefact** (kintsugi deploy + live sweep).
- October grant (16:21:39, the note on `secuura-connector-allowlist-missing-setting-ks1256-1005`). It covers ITEM 7, on Wednesday's GO.
- `secuura-tenant-isolation-migration-ks1401-1005` = **a** ("apply with the kintsugi deploy"). **Seat F 2nd writes it. It is applied in the LATER kintsugi round, not this one** (wave partition line 26).
- `secuura-ks1404-tsa-trust-and-library-1004` = **a**, HALF DONE: "measure TSA_URL per environment" is owed. Your ITEM 0 (d) and ITEM 7 env reads supply the measurement; the pinning and wiring are not yours.
- `secuura-connector-allowlist-missing-setting-ks1256-1005` = **b**. The next E-lane seat's.
- `secuura-tooling-tickets-off-product-board-1005` = **a**. Seat C 23rd's.
- Demo cards ruled and undelivered (`decision_queue.sh list ruled --undelivered secuura-`, 16:3x AEDT, 51 output lines): `demo-kam-admin-default-password` (b), `demo-admin-mfa` (later), `demo-admin-transcripts` (redact), `f5-demo-exposure-probe` (probe), `f5-demo-interim-mitigation` (letitland). **Not yours. Change nothing they name.**

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The KS-1054 probe is `/health/deep`, never `/health` (ANSWER 2026-09-30T12:37:50Z, accepted as her error).
- A gate that trips on the instrument: fix, re-prove, resume. A gate that trips on a reading: STOP and mail (same ANSWER).
- For October, "deployed" = kintsugi, then demo once kintsugi sweeps clean, each deploy on Wednesday's word under the grant. Demo no longer waits for Peter's nod in October (Wednesday's reading of the grant, said back to Kam with a correction offer, 16:2x).
- The Peter/Stuart deploy notice is HELD for Kam's word (external communication).
- B 50th's RLS finding was DELIVERED as **KS-1401** (B 52nd, 10-01 11:53; Wednesday's daily note line 64). It is not yours to re-file.
- Co-tenant routing: every mail names the seat AND uses that seat's own row tag (STANDING_LINES 358-359).

## VERIFIED BEFORE SENDING (deploy THIS)
**develop `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`**, tree `dab6adb69ea3c7966ec17111a139bb5bcfadb68c`. The drafter's `ls-remote` read it at 16:27:22 AEDT, rc 0, == the wave partition's figure. `91a8f6b721bc` (kintsugi's recorded SHA) is an ancestor (rc 0). `3ce8cd4026a6` (the audit's read point) is an ancestor (rc 0). The range holds 0 `.sql`. Every first-parent merge in it carries a "Merged by … on … GO" line except `e6daa806e` (KS-1403, lockfiles), whose body reads only `Refs KS-1403`. Its gate provenance is UNMEASURED by the drafter; Wednesday's "ready" test is hers to apply.

PROVENANCE:
- develop 46c3e20cfbd2 at origin; tree dab6adb69ea3; 91a8f6b721bc and 3ce8cd4026a6 ancestors (rc 0); both commits present locally | `git -c core.sshCommand=<on-disk key> ls-remote git@github.com:Secuura/Distributed_Secuura.git refs/heads/develop` 16:27:22 AEDT rc 0; `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files cat-file -t / rev-parse / merge-base --is-ancestor` (READ verbs) | read 2026-10-05
- the range 91a8f6b721bc..46c3e20cfbd2: 17 commits / 15 first-parent / 85 files / 46 under Blockchain/Dev; 0 .sql/migration paths; no compose/.env.example/packages/shared/docker/init/run-migrations/api-gateway change; first-parent list (#1361 … KS-1333) | `git rev-list --count / --first-parent`, `diff --name-status`, `diff --stat -- <paths>`, `log --first-parent --format` on the shared .git (READ) | read 2026-10-05
- the 17-image rebuild set, the 7 controls, the yaml COPY + bind mount, migrations+originate sharing services/originate | `python3 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-50th/boot/service_map.py <shared repo> 91a8f6b7… 46c3e20c…` rc 0 → /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b72c1f78-0eff-4438-a1d7-6dcd846422fb/scratchpad/d7/service_map.out (127 lines) | read 2026-10-05
- kintsugi at 91a8f6b721bc (FINAL STATE 12:28:23Z 09-30); /health is the nginx literal and /health/deep is the probe; rollback recipe; nine sets and their fps; 19,548 MB end / 5,635 MB dip; 4-line error baseline; KS-535 695d09df873ff42b / 142098c9528d0188, .env sha16 634e99a79cbc6ee5; REVISION sha16 921a8d3b1fa0b5df; 038a recorded; tracker 49; highest 048; egress 157.211.46.215; traps 1-9; migrations not recreated | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB50-kintsugi-deploy.md lines 3-229 | read 2026-10-05
- no kintsugi deploy after 09-30: history.md lines 1-1526 hold no deploy entry (the kintsugi hits at 465, 1208, 1350, 1522 are not deploys); Wednesday 10-01 12:23 records B 50th's deploy as delivered | `/usr/bin/grep -n -i` over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md and /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-10-0*.md | read 2026-10-05
- the card's "last recorded 23 Sep" premise; options a/b/c; ruled_ts 16:23:06 | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-kintsugi-deploy-for-31oct-1005` rc 0 | read 2026-10-05
- 32 critical-path MERGED-AWAITING-SWEEP rows (56 critical-path rows in total); 29 ancestors of 91a8f6b721bc, 3 new (KS-1402 2d85b84e1, KS-1404 14d40d445, KS-1399 723dc0722) | `awk -F'\t'` on cols 2/10/12 of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-05_ks-ticket-audit/audit_A.tsv; per PR `git log -1 -E --grep='(Merge pull request #N from|\(#N\)$)' 46c3e20` + `merge-base --is-ancestor <c> 91a8f6b…`; #1376 NOTFOUND by grep, located as 14d40d445 by subject in the first-parent list | read 2026-10-05
- the audit's stale-premise sentence; no live check by the auditors | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-05_ks-ticket-audit/SUMMARY.md line 6; audit_A.md lines 8, 56 | read 2026-10-05
- KS-1404 fail-closed with no anchor; TSA_TRUST_ANCHORS_PEM is not passed by compose; the crt is not in the runtime image | `git show 46c3e20:Blockchain/Dev/services/timestamping/{config/README.md (lines 14-31), src/tsa/qualified-tsa.ts (385-410), Dockerfile (35-59), package.json (build: tsc)}`; `git grep -n TSA_TRUST_ANCHORS_PEM|TSA_URL 46c3e20 -- Blockchain/Dev` (compose: TSA_URL only, :1244) | read 2026-10-05
- KS-1404 card half done (TSA_URL per env never measured; DigiCert G4 not pinned) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD6-2026-10-05.md lines 91-97; `decision_queue.sh show secuura-ks1404-tsa-trust-and-library-1004` | read 2026-10-05
- demo last recorded 0f8fb33c3 (s169, 09-10), 33 tags, ~600 MB net build, disk transient peak, migrations-image blind spot; range 575/450/1116/522; 038a A, 039 M, docker/init M ×2, run-migrations M, compose +ADMIN_USER_PASSWORD +GATEWAY_VOUCH_SECRET | history.md lines 5995-6040; `git rev-list --count / diff --name-status 0f8fb33c3..46c3e20 -- <paths>`; `comm` of `${VAR` names in compose at both SHAs (95 → 97) | read 2026-10-05
- demo host, IP, key, ARM64 2 vCPU 4 GiB + 6 GiB swap, stack path, two candidate public fronts | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 12-18; /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_kintsugi-first-then-demo-behind-gates.md line 28 | read 2026-10-05
- key files present (vm_secuura02_kintsugi 399 B, vm_secuura02_demo 411 B, both mode 600); no ~/.ssh/config Host alias for either box | `ls -la …/3_Access_Keys/`; `/usr/bin/grep -n -i '^Host ' ~/.ssh/config` | read 2026-10-05
- Peter/Stuart notify rule (on tickets at wrap); Wednesday holds it | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 185-193; learnings 2026-09-10_kintsugi-first-then-demo-behind-gates.md lines 55-58 | read 2026-10-05
- October grant text, expiry, reading; EXPIRING-GRANTS row | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md lines 1-29; /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md line 9 | read 2026-10-05
- Phase 0, build-all-then-swap, migrations in the middle, KS-535 AFTER | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_deploy-both-boxes-grant-expires-sunday.md lines 38-42; …_kintsugi-first-then-demo-behind-gates.md lines 45-54 | read 2026-10-05
- seats, tokens, locks, pin rule, the later round | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_wave_1630_partition.md lines 1-26 | read 2026-10-05
- inbox routing: all six Blockchain panes on secuura-blockchain@agentmail.to | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf lines 29, 36-40 | read 2026-10-05
- seat number: "seat d 7th" 0, control "seat d 6th" 4; d7 182 raw / 1 bounded (line 3440); no `seatD-7th` record folder; shared .git/worktrees 490; `.push-lock-*` present: `-e2` only | `/usr/bin/grep -c -i` + `grep -o -i -E '(^|[^0-9a-z])d7([^0-9a-z]|$)'` over history.md; `ls` of 5_Project_History, .git/worktrees, worktrees/ | read 2026-10-05
- D-lane inbox tools (inbox_matchd6.py 233 lines, inbox_watchd6.sh 103, watchproofd6.sh 230); MY_PANE `secuura/blockchain-d]`; F-02; zero ref writes; leg9clt alternates | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD6-2026-10-05.md lines 99-131; raise/inbox_matchd6.py line 117 | read 2026-10-05
- B 50th's phase0 constants (SCOPED 29, WANT_N, control pre-20260923 = 29, fp list), phase4 ORDER (:10), the 038a gate (:23-40), the inode line (:14), V10 vouch, V11 KS-535 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-50th/deploy/{phase0_remote.sh lines 1-25, phase4_remote.sh lines 9-40, verify_remote.sh lines 47-58} | read 2026-10-05
- §5f text and §3 teardown | `git show 46c3e20:.claude/skills/secuura-test-discipline/SKILL.md` lines 84-130, 260-286, 540-550 | read 2026-10-05
- standing lines cited (269-270 the §5f handle; 287 which develop; 332-333, 358-359 co-tenant; 338-341 next-up stall; 343-344 read from a SHA; 391-397 lettered tokens, $TMUX_PANE, no force push, drive hygiene; 109 migration 048) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md (397 lines, read whole) | read 2026-10-05
- UNMEASURED by the drafter (no host contacted): kintsugi's and demo's running SHA, census, disk, REVISION, rollback sets, DB tracker, error baseline, today's KS-535 hashes, /health/deep, TSA_URL and anchor env on either box, demo's compose project/profile/NSG/public front, whether the NSG still admits this Mac's egress, every sweep probe's result, and the build-time forecast | stated as UNMEASURED; the drafter connected only to github.com (`ls-remote`) | read 2026-10-05

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-05 16:37
    - One pin everywhere: 46c3e20cfbd2 / tree dab6adb69ea3, in BLUF, ITEM 0 (a)/(b), ITEM 5 and ITEM 7, and VERIFIED. Develop moving never moves it. #1381 and the KS-1401 migration are excluded in BLUF, ITEM 3 and RULED BY KAM, each pointing at the same later round.
    - STOP 1 precedes any box write. STOP 2 on kintsugi is conditional (0 pending expected, re-measured just before the api-gateway recreate). STOP 1-demo and STOP 2-demo are unconditional. Demo needs a GO naming this seat AND the SHA.
    - "No comment, no ticket state change" appears in BLUF, ITEM 6 and HOLDS. The card's own "closes what passes" is named as Wednesday's narrowing, not hidden.
    - The KS-535 values are inherited and stated as inherited: kintsugi 695d09df873ff42b / 142098c9528d0188, demo 12ea1a07174c3f50, spelled the same in ITEM 0 (d), ITEM 5, ITEM 7 and HOLDS. Today's are UNMEASURED.
    - /health/deep is the only KS-1054 probe. /health appears only as the cannot-discriminate control.
    - The 32/29/3 split is the drafter's ancestry against the RECORDED box SHA. ITEM 6 tells the seat to re-derive it against the MEASURED one.
    - The demo is ARM64 (CLAUDE.md:12) and its range is 575 commits. The kintsugi 2 h 08 min figure is never used as a demo forecast.
    - SSH alias: none exists. The inline `ssh -i` form is named for both boxes. The NSG is never touched.
