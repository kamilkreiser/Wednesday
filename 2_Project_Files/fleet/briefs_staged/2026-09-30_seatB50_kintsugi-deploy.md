# LAUNCH BRIEF — Seat B 50th, Secuura/Blockchain (pane `Secuura/Blockchain`) — deploy develop to KINTSUGI, verify the RUNNING box, report DEPLOYED — from Wednesday

⛔ **TOP LINE — NO WRITE TO THE SHARED CHECKOUT OR ITS `.git`.** Refuse the launcher's boot "pull latest if safe" line and say so in your plan mail. No `pull`, `fetch`, `checkout`, `reset`, `stash` or `worktree add` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. It sits at HEAD `37205947ddd2` (drafter, `rev-parse HEAD`, 19:3x AEST) — far behind develop, so **never read a repo file from its working tree**; read `git show <sha>:<path>` or read your own clone. Your build source is a FRESH CLONE (ITEM 0 (b)).

## BLUF
- **You are Seat B 50th.** Your project's `history.md` has Seat B 49th as the newest B seat (line 106) and no B 50th entry. **Seat D 1st** (pane `Secuura/Blockchain-B`) is a separate series. It is wrapping now and is NOT you.
- **Your one job:** deploy develop to **KINTSUGI** and verify the RUNNING box. Then mail Wednesday **DEPLOYED**, write the handover and the history entry, and wrap. **Kintsugi ONLY. Never demo** (demo is UAT and moves only on Peter's nod). **Production does not exist and is not touched.** No merge, push, PR, product code, anchor, or ticket comment.
- **Authority (Kam, live board 2026-09-30 14:18:29, verbatim):** *"Do everything you can to resolve and once tested and deployed let me know"*. This concerns Stuart's KS-1395 and the KS-1379/KS-1380 direction. Wednesday's reading, receipted to Kam at the time: **"deployed" = KINTSUGI only**. This deploy is that word. Wednesday reports to Kam; you report to Wednesday.
- **Target: develop `91a8f6b721bc70cb8c352a694c330e85edd9ef23`**, tree `d485add27eabcbbcfa12242158d14cafd71bb01b`. Wednesday verified it at source at 19:27 AEST. The drafter re-read it with `ls-remote` at 19:33:08 AEST. **Re-pin at ITEM 0 and deploy whatever develop is THEN, naming the full SHA.** If develop has moved, record both SHAs and the `diff --stat` of the move in the plan mail. A move that brings in #1360 or any `.sql` is a STOP (see HOLDS).
- **From → to:** kintsugi last ran `6ab9d5021e96` (Seat B 23rd, 2026-09-23 13:40:41Z). The drafter found **no later kintsugi deploy** in your `history.md` or in Wednesday's daily notes for 09-24 to 09-30. **The box's current state is UNMEASURED.** You measure it at ITEM 0.
- **This is not B 23rd's small range.** `6ab9d5021e96..91a8f6b721bc` = **174 commits / 137 first-parent / 632 files / 202 under `Blockchain/Dev`**. That includes 37 `package-lock.json`, 16 `package.json`, 16 under `packages/shared/`, **one NEW migration and one MODIFIED migration** (ITEM 3), a one-line comment in `docker-compose.yml`, and `.env.example` (drafter, `git diff --name-only`/`--name-status`, READ verbs on the shared `.git`). **Expect a full rebuild.** B 23rd's 29 images took 2 h 10 min.
- **Today's PRs, all first-parent in the range:** #1349 KS-1374 · #1350 KS-1054 · #1354 KS-470 · #1355 KS-1378 · #1356 KS-1378 lock refresh · #1357 + #1359 KS-1054 (a broken python3 fails closed; the rc-1 messages) · **#1358 KS-1380** (15 lockfiles; merged by PeterObeden at 07:28Z as merge `a5ab2ca9aa11`, without a gate). Also in the range: Peter's #1351, #1352 and #1353.
- **Kam's usage is at 70% of the weekly allowance.** Keep your context lean: reuse B 23rd's scripts, never re-derive them. Read files by section, not whole. **Necessity clause for this cloud launch: a deploy cannot be done by a local model.**

## THE PROCEDURE — PROVEN, COPY IT
Your project tree is `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/`. Read first:
1. `5_Project_History/HANDOVER-seatB23-kintsugi-deploy.md` (9.5 KB, whole) and `5_Project_History/2026-09-23_seatB-23rd/KINTSUGI-DEPLOY-STATE.md` (8.5 KB). These record the last deploy and its gotchas.
2. B 23rd's scripts in `5_Project_History/2026-09-23_seatB-23rd/deploy/`: `phase0_remote.sh`, `phase1_verify_remote.sh`, `build.sh`, `preswap_baseline_remote.sh`, `phase4_remote.sh`, `verify_remote.sh`, `errbase_remote.sh`, `wait_build.sh`, `wait_swap.sh`. Also `boot/probe_remote.sh` and `boot/service_map.py`. **Copy them into your own record folder `5_Project_History/2026-09-30_seatB-50th/` and re-key them before use:** seat name as prose, `seatB23`/`B23` tokens, the `pre-20260923` stamp, the `.rebuild-seatB23/` directory, env-var prefixes and absolute paths. Grep for EVERY predecessor generation (`2026092[0-9]`, `seatA16`, `B23`). Prove the re-key with a control that goes the other way (STANDING_LINES.md, the entries dated 09-25 and 09-27).
3. Wednesday's `fleet/briefs_staged/2026-09-22_seatA16_kintsugi-deploy-3bad652d1.md` (path below): **ITEMs 0-5 only**, by section. ITEM 6 (the anchor) and ITEM 7's comments do NOT apply.

**Order, unchanged:**
1. ITEM 0 MEASURE, read-only.
2. Mail Wednesday the plan confirmation — **STOP 1**.
3. Phase 0 re-tag, so a rollback exists before anything moves.
4. rsync and build EVERYTHING, swapping nothing.
5. Migrations in the middle — **STOP 2**, see ITEM 3.
6. Swap one service at a time.
7. Verify the RUNNING box.
8. DEPLOYED mail, handover, history, wrap.

### ITEM 0 — MEASURE (read-only everywhere)
- **(a) develop:** `ls-remote` from the shared checkout. It is a READ verb and its `core.sshCommand` carries the on-disk deploy key. Report the full SHA. Also run `git merge-base --is-ancestor a5ab2ca9aa11 <pin>` and say whether **#1358 is IN your pin**. Say whether #1360's revert is in it.
- **(b) the build source — a FRESH CLONE:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/deploy-clones/seatB50-<sha12>`. `deploy-clones/` is a sibling of `2_Project_Files`, and it holds `seatA16-…` and `seatB23-…` already. Use A16's ITEM 0 (b) command shape: `git -c core.sshCommand='ssh -i …/3_Access_Keys/github_deploy_rw -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new' clone --no-checkout …`, then `checkout --detach <pin>`. Assert `rev-parse HEAD` == the pin and `HEAD^{tree}` == the pin's tree (`d485add27eab…` if unmoved). Assert porcelain is empty. Assert the shared `.git/worktrees` count is UNCHANGED (475 at the drafter's `ls | wc -l`). Never `worktree add`. Never `--reference` the shared `.git`.
- **(c) the rebuild set, by MEASUREMENT:** run B 23rd's `service_map.py` in your clone over the range `<box's measured SHA>..<pin>`. The drafter expects every backend image and most frontends, because `packages/shared` and 37 locks changed. It also expects **analytics, billing and governance** to build only BECAUSE #1358 is in the pin. The gate49b post-merge audit found they build at develop and FAIL at #1358's first parent. Report per image: in/out and the reason.
- **(d) kintsugi as it runs** (key NAMES only, never values). Host `secuura02-kintsugi-vm`, `20.198.226.148`. Key `3_Access_Keys/vm_secuura02_kintsugi`. Stack `/home/secuura/secuura/Dev`, compose project `dev`, `--profile phase2`. Gateway on `localhost:6882`. Public front `https://kintsugi.secuura.net`. The NSG admits one `/32`. If SSH fails, STOP and mail your egress address. Never touch the NSG. Measure these:
  - **the deployed SHA:** hash the range's `Blockchain/Dev` paths on the box against BOTH `6ab9d5021e96` and the pin. Plant one path that the check must catch. Read what `REVISION` holds.
  - **the container census:** B 23rd left 35 containers, 27/27 healthy after settling, and demo-service in its KS-641 FATAL loop (judge it by Id + Created + image).
  - **the rollback sets:** B 23rd lists eight, from `pre-20260923` ×29 back to `pre-20260910` ×31.
  - **disk:** B 23rd left **24,020 MB free**. Its 29-image build dipped to a minimum of 20,508 MB. There are now ~30 more images on the box.
  - **the DB's highest migration**, and whether `038a_ks1054_core_tables_before_039` is recorded in `_secuura_migrations`.
  - **the error-line baseline** (`errbase_remote.sh`; B 23rd's was 5 distinct lines).
  - **KS-535 BEFORE:** `sha256[0:16]` of `PLATFORM_WALLET_MNEMONIC` and of `BLOCKFROST_API_KEY`, from `.env` AND from the running anchoring container. B 23rd read `695d09df873ff42b` / `142098c9528d0188`. **Demo's mnemonic hash is `12ea1a07174c3f50`, and kintsugi's MUST differ.** Mind B 23rd's trap: `\"\$VAR\"` inside a quoted heredoc hashes the literal string, which gives `1d99a769a815b299`, a FALSE breach. Run an expansion control and an empty-var control.
  - **the KS-1054 BEFORE control:** `curl -s localhost:6882/health` on the box. The running gateway predates #1332, so the drafter expects `startupMigrations` to be ABSENT. Run your clone's `Blockchain/Dev/deployment/azure/check-startup-migrations.sh '<body>'` on it. The expected result is **rc 2** (PASS-WITH-SKIP, script lines 18-39).
- **(e) PLAN CONFIRMATION — STOP 1.** Subject `[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (Seat B 50th)`. Include:
  - the pin, whether #1358 is in it and whether #1360 is in it;
  - the clone's HEAD and tree;
  - the box's measured SHA against B 23rd's record, with every difference named;
  - the rebuild set, per image, with its reason;
  - the disk arithmetic against the **4000 MB minimum-free guard**;
  - the Phase 0 stamp `pre-20260930` (use the box's UTC clock; check by name AND id that it does not already exist) and the tag count you will assert;
  - the ordered plan, with the exact rollback for each service;
  - the ITEM 3 migration reading;
  - the KS-535 BEFORE hashes;
  - the KS-1054 BEFORE control;
  - the wall clock;
  - **the launcher's preflight warnings VERBATIM**;
  - **anything here your measurement contradicts.**

  **Wait for CONFIRMED.**

### ITEM 1 — Phase 0 re-tag
Re-tag every image the rebuild will overwrite, `:latest` → `:pre-20260930`, by name and id. Assert the count. Assert the older sets are byte-identical before and after. **No prune of any kind. No image deletion, `--remove-orphans`, `down`, `-v` or `rm`.** `--remove-orphans` deletes guardian + queue.

### ITEM 2 — rsync + build everything, nothing swapped
- **rsync** from the CLONE (`-a -c`, no `--delete`). `.env`, `.env.local` and `docker-compose.override.yml` stay untouched: stat them before, compare after. The file list must equal git's. Write `REVISION` and keep the old one beside it.
- **Build:** serial, `COMPOSE_BAKE=0`, `docker compose -p dev --profile phase2 --progress plain build <svc>`. **Never `-f`**: the untracked override feeds auth.
  - **Each build writes to a file with rc on its own line** (`cmd > out 2>&1; rc=$?`), never piped.
  - Use a fresh `.rebuild-seatB50/`. Stale `done.txt` files SKIP builds.
  - Record per image: rc, the NEW id vs `:pre-20260930`, and the minimum free disk.
- **A build failure costs nothing: STOP and mail.** That includes analytics, billing or governance failing, which means #1358 is not in effect in your pin. **Never deploy a partial set without Wednesday's word.**

### ITEM 3 — migrations: a conditional STOP 2 is expected this time
- **What the range holds (drafter, `--name-status`):**
  - `A migrations/038a_ks1054_core_tables_before_039.sql`: 99 lines, four `CREATE TABLE IF NOT EXISTS` (oauth_apps, svc_webhooks, certifications, charge_events), 0 `DROP`;
  - `M migrations/039_rls_fail_closed.sql` (+44/−6);
  - `M docker/init/06-m365-tables.sql` (a `docker/init` script; by Postgres convention it runs only on an EMPTY data dir — UNMEASURED, confirm from compose);
  - `M scripts/run-migrations.sh`, which adds `exit 4` when `pg_isready` is absent.
- **Both runners skip a file that is already recorded and apply one that is not** (038a header lines 10-11 and 19-27). **api-gateway's own `startup-migrations.ts` scans `migrations/` when it boots** (lines 7, 105). So **recreating api-gateway RUNS migrations**: 038a will apply on that recreate if it is unrecorded. The edit to the already-recorded 039 will NOT re-run.
- **Before swapping api-gateway, and before running anything:** measure whether 038a is recorded, and whether the four tables exist. Then mail `[Secuura/Blockchain -> Wednesday] QUESTION: migration 038a (Seat B 50th)` with those numbers. **Apply nothing before CONFIRMED.** No down-migrations exist.

### ITEM 4 — swap one service at a time
- Command: `docker compose -p dev --profile phase2 up -d --no-deps --force-recreate <svc>`, with a health read between swaps. anchoring and api-gateway go LAST among the backends. Recreate postgres/redis/pgbouncer only if their image id changed.
- After api-gateway's recreate, assert that the yaml bind mount's container inode == its host inode. Lesson `2026-09-10_a-single-file-bind-mount-binds-the-inode`: the recreate is the only thing that rebinds it.
- **If a service is unhealthy:** roll it back (`docker tag dev-<svc>:pre-20260930 dev-<svc>:latest` + the same `up -d`), then STOP and mail the state of every service.

### ITEM 5 — verify the RUNNING box, not the steps' exit codes
- **Census vs ITEM 0.** `REVISION` == the pin. **Settled:** at least 5 min after the last swap, 0 restarts, and error lines == the baseline. `/health/deep` healthy. Every non-swapped container untouched, and a planted change caught. The rollback sets intact. `GATEWAY_VOUCH_SECRET` NON-EMPTY nowhere.
- **KS-1054 ON THE LIVE BOX** — read the RUNNING behaviour. Exit codes are not evidence (the bind-mount lesson). Put RAW values beside every verdict:
  - (i) `curl -s localhost:6882/health` on the box now carries `startupMigrations` with `ran: true` and `failed: 0` (shape: `startupMigrationStatus.ts` lines 26-42). Read `/health/deep` too.
  - (ii) Your clone's `check-startup-migrations.sh '<that live body>'` gives **rc 0**. Controls on the same live body:
    - the ITEM 0 pre-deploy body gives **rc 2** (the field was absent);
    - the live body with `failed` set to 1 gives **rc 1**;
    - **run with a broken `python3` first on PATH (a shim that exits 1)**, it gives **rc 1** and the line "python3 is NOT on PATH or does not run". This is #1357's fail-closed (script line 79).
  - (iii) Read the startup-migration lines in the api-gateway log: what `applied`/`failed` counted, and whether 038a was applied.
- **KS-535 AFTER the restart:** both hashes == ITEM 0's, and the mnemonic hash != `12ea1a07174c3f50`. `.env` byte-identical.
- Print ratios (`N / N`), never "all". A probe you cannot run is **NOT RUN, with the reason**.

### ITEM 6 — DEPLOYED, handover, history, wrap
- **Mail** `[Secuura/Blockchain -> Wednesday] DEPLOYED: kintsugi at <sha12> (Seat B 50th)`. Include:
  - the full SHA deployed, and whether #1358 and #1360 are in it;
  - **per-service image ids before (`:pre-20260930`) and after**;
  - migrations run: which, by which runner, and the counts;
  - the raw `/health` and `/health/deep` output;
  - the KS-535 re-verification (hashes and equality verdicts, never values);
  - the three KS-1054 readings with their controls;
  - the settled census.
- **Post no ticket comment. Message no human.** Wednesday writes the report to Kam.
- Then the handover `5_Project_History/HANDOVER-seatB50-kintsugi-deploy.md` (FINAL STATE first, then the rollback recipe). Records go in `5_Project_History/2026-09-30_seatB-50th/`. Add a history entry at the TOP. Wrap with `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-30 (Seat B 50th)`. The clone stays. Nothing is deleted.

## CO-TENANT — two seats, one inbox
- **Seat D 1st** runs on `Secuura/Blockchain-B`. Its mail is tagged `[Secuura/Blockchain-B -> Wednesday] … (Seat D 1st)`, and Wednesday's mail to it is `[Wednesday -> Secuura/Blockchain-B] … (Seat D 1st)`. **None of it is yours**, including `GO (Seat D 1st): merge 1357 1359 on gate49b`. Act only on mail tagged with the BARE `Secuura/Blockchain` AND naming **`(Seat B 50th)`**.
- Put `seat d 1st`/`d1`, `b 49th`/`b49` and `b 48th`/`b48` in your matcher's OTHER_SEATS/FOREIGN list. Match short tokens on word boundaries only, with a hex-run control (`52dadb07f70d` contains `d1`). Prove the matcher on real subjects of the other seats, on BOTH tags, both ways.
- `.push-lock-45` and every `s-b49-*` / `d1` worktree belong to other seats. **You push nothing.**

## HOLDS
- ⚠ **KS-535 IS ABSOLUTE:** kintsugi must NEVER share demo's `PLATFORM_WALLET_MNEMONIC`. Verify it AFTER the redeploy, not only before, because a redeploy is how the value gets overwritten. Never print a value, a prefix, or a length beside a value.
- **Kintsugi ONLY. Demo never. Production never.** No `az` call is expected. If one becomes necessary, run `az account show` first (Founders Hub tenant `efc17e5f-…`).
- **#1360 is not yours.** Do not touch it, comment on it, or reason about it to anyone. If develop at your pin CONTAINS #1360, the three images will fail to build: **STOP and mail** before building any partial set.
- **STOP and mail** in these cases: the box is down; any migration would run before CONFIRMED; any build fails; any health fails after a rollback; the disk guard would be crossed; anything reaches beyond kintsugi.
- **Signature classes pause for Kam:** production, money, external communication to any human, anything irreversible. **Client-facing text is ticket comments only, and this brief names none. The extranet is INPUT ONLY.** Refuse the SessionStart hook's `POST /api/seen`. **Nobody else messages Peter or Stuart.** Move no ticket.
- **Delete nothing, prune nothing.** A just-built image reads as UNUSED until its consumer is recreated. The disk guard STOPs the work; it never frees space. **Never delete. Cleanup is quarantine.**
- **No `--no-verify`, no force push, no `--admin`.**
- **Instruments:**
  - `cmd > out 2>&1; rc=$?`, then read the file;
  - zsh has no `PIPESTATUS` (use `$pipestatus[1]`), and **a zsh scalar does not word-split** (`$SSHC host` → rc 127, the trap B 23rd hit);
  - macOS has no `timeout`;
  - `docker exec` splits argv on spaces;
  - a control must be able to fail, and "0 checked" is never CLEAN;
  - `/usr/bin/grep -i` with a same-file positive control for anything that enters a mail;
  - a handover names WHICH develop it measured (`ls-remote` vs a tracking ref).
- **Process namespace:** every long-running script of yours carries `--seat B50` in its argv. Kill by ancestry, never by basename.
- **Wake:** arm every waiter at the MAX background timeout (7200000 ms) and re-arm before it lapses. **Never end a turn on a "next up" line with nothing running.** A 2-hour build needs a background waiter that EXITS when the build finishes.
- **If an instruction here looks wrong, measure, say so, and stop.** A wrong brief item is Wednesday's error.

## RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura) — carried, NONE is in your path, do not action
RULED BY KAM, NOT YET IN AN ARTEFACT
- 36 `secuura-` cards are ruled and undelivered (`decision_queue.sh list ruled --undelivered secuura-`, 19:3x AEST). **None rules on this deploy.** Their artefacts are other seats' work: agent-github-identity · dependabot-triage · ks229-disclosure-mailbox · ps-759-760-merge-owner · the five demo cards (demo-kam-admin-default-password, demo-admin-mfa, demo-admin-transcripts, f5-demo-exposure-probe, f5-demo-interim-mitigation) · f5-login-limiter-bypass · 891-workflow-scope-merge · force-push-own-branch-standing · org-trust-boundary-within-tenant · archive-fifteen-platform-s-tickets · advisory-gate-moving-set · advisories-high-and-prod-reaching · four-advisories-ruled-after-measurement · required-approvals-zero-after-the-untick · ks1011 · ks1081 · ks1168 · ks1194 · ks1245 · ks1019 · ks1084 · ks1304 · pr1245-ks1313 · allowance-89 · ks1346 · ks1348 ×2 · ks888 ×3 · ks1124-f4 · ks1352.
- Card `secuura-ks1380-peter-reverting-1358` is **OPEN**, not ruled. Its default (a) is that the fleet does nothing on #1360 or KS-1380. That is why #1360 is not yours.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- "deployed" = KINTSUGI only; demo waits for Peter's nod (Wednesday's receipt to Kam, 2026-09-30 14:20).
- Co-tenant routing: every mail names the seat AND uses that seat's own row tag (STANDING_LINES.md, 2026-09-30 entry; Wednesday 14:24).
- gate49b comment ruling (19:14): the KS-1054 ×2 and amended KS-1395 texts are posted after the merges, and **not by you**. KS-1387 is HELD. KS-1380 is not posted.
- B 23rd's `.dockerignore` finding (09-23 11:16:28Z): `tests` does not exclude `__tests__`, so a change in `packages/shared/src/__tests__/` rebuilds ~23 images. It is a FINDING only. Do not fix it in this deploy.

## VERIFIED BEFORE SENDING (deploy THIS unless develop has moved)
**develop `91a8f6b721bc70cb8c352a694c330e85edd9ef23`**, tree `d485add27eabcbbcfa12242158d14cafd71bb01b` == gate49b END. Wednesday verified it at 19:27 AEST; the drafter's `ls-remote` agreed at 19:33:08 AEST. #1358's merge `a5ab2ca9aa11` IS an ancestor (`merge-base --is-ancestor` rc 0). #1360 is NOT merged: develop == the tip that followed #1359.

PROVENANCE:
- develop 91a8f6b721bc70cb8c352a694c330e85edd9ef23 at origin; tree d485add27eab; #1358 merge a5ab2ca9aa11 ancestor (rc 0), parents 3a0d9812262b / 6cf5c3629cd6 | `git -c core.sshCommand=<on-disk key> ls-remote git@github.com:Secuura/Distributed_Secuura.git refs/heads/develop` at 19:33:08 AEST, rc 0; `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files rev-parse / merge-base --is-ancestor` (READ verbs) | read 2026-09-30
- Wednesday's own source verification (93a10a06dfd2 → 91a8f6b721bc, tree d485add27eab == gate49b END; #1358 by PeterObeden 07:28:02Z; #1360 opened 07:38:55Z; gate49b audit: images build at develop, fail at #1358's first parent) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-30.md entries 17:37, 18:35, 19:14, 19:27 | read 2026-09-30
- Kam's words "Do everything you can to resolve and once tested and deployed let me know" at 14:18:29, and Wednesday's KINTSUGI-only receipt | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-30.md entry 14:20 | read 2026-09-30
- the range 6ab9d5021e96..91a8f6b721bc: 174 commits / 137 first-parent / 632 files / 202 under Blockchain/Dev; 37 lockfiles, 16 package.json, 16 packages/shared; A 038a, M 039, M docker/init/06-m365-tables.sql, M run-migrations.sh (+34/−3, exit 4); compose +1/−1 (a comment on RATE_LIMIT_MAX_REQUESTS); .env.example +5 comment lines; today's PRs first-parent at fplog lines 1-11 | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files rev-list --count / diff --name-only / --name-status / --stat / log --first-parent`, READ verbs, 19:3x AEST | read 2026-09-30
- 038a content (4 CREATE TABLE IF NOT EXISTS, 0 DROP; header lines 10-11 and 19-27); api-gateway startup-migrations.ts scans migrations/ (lines 7, 105); health.ts serves startupMigrations (lines 94, 199); startupMigrationStatus.ts shape (26-42); check-startup-migrations.sh rc 0/1/2 semantics (lines 18-39) and the python3 fail-closed guard (line 79) | `git show 91a8f6b721bc:<path> | cat -n` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-30
- KS-1054 commits in range: #1332 0de108577, #1346 8ba2da02d, #1348 a72149a1a, #1350 37205947d, #1357 93a10a06d, #1359 91a8f6b72 | `git log --first-parent` + `git show --stat` on the shared .git (READ) | read 2026-09-30
- kintsugi last deployed 6ab9d5021e96 by Seat B 23rd (13:40:41Z 2026-09-23); 29 images / 28 swapped / 2 h 10 min; host, IP, key, stack, `-p dev --profile phase2`, never -f, rollback recipe, eight rollback sets, 24,020 MB free, min 20,508 MB, error baseline 5 lines, the heredoc KS-535 trap 1d99a769a815b299, the zsh word-split trap, the __tests__ finding | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB23-kintsugi-deploy.md lines 3-36 | read 2026-09-30
- gateway localhost:6882, public front https://kintsugi.secuura.net, NSG one /32 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-23_seatB-23rd/KINTSUGI-DEPLOY-STATE.md lines 4, 6, 17, 33 | read 2026-09-30
- KS-535 hashes: kintsugi 695d09df873ff42b / 142098c9528d0188 (09-23 before and after), demo 12ea1a07174c3f50 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md line 1305 (Seat B 23rd entry) | read 2026-09-30
- no kintsugi deploy after 09-23: 4 kintsugi mentions in history.md lines 7-1301, none a deploy; Wednesday's daily notes 09-24..09-30 carry no kintsugi deploy (09-25 line 100 "NOT deployed … only on Kam's tap") | `/usr/bin/grep -n -i kintsugi` over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md and /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-2*.md, 2026-09-30.md | read 2026-09-30
- seat number: Seat B 49th = newest B entry (history.md line 106); "seat b 50th" 0 hits (control "seat b 49th" 4); Seat D 1st at line 24 on -B | `/usr/bin/grep -n -i` over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-09-30
- the proven procedure (ITEMs 0-5, fresh-clone command, the KS-535 sha16 method) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-22_seatA16_kintsugi-deploy-3bad652d1.md lines 25-71; /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-23_seatB23_kintsugi-deploy.md | read 2026-09-30
- B 23rd's scripts (phase0/phase1_verify/build/preswap_baseline/phase4/verify/errbase/wait_build/wait_swap, boot/probe_remote.sh, boot/service_map.py) exist | `ls` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-23_seatB-23rd/deploy and /boot | read 2026-09-30
- shared checkout HEAD 37205947ddd2, porcelain non-?? 0, .git/worktrees 475; core.sshCommand = the on-disk `-i` form; deploy-clones holds seatA16-3bad652d1 + seatB23-6ab9d5021; launcher key wiring at Launch_Claude.command lines 126-140 | `git rev-parse HEAD / status --porcelain / config --get core.sshCommand`, `ls` under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/ | read 2026-09-30
- KS-535 absolute; kintsugi first; measure the box before deploying | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_kintsugi-first-then-demo-behind-gates.md lines 45-54 | read 2026-09-30
- Phase 0 re-tag before building; build everything before swapping; migrations in the middle; re-verify KS-535 AFTER | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_deploy-both-boxes-grant-expires-sunday.md lines 38-42 | read 2026-09-30
- a single-file bind mount keeps the old inode; only a recreate rebinds it; verify the outcome, not the deploy's signals | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-10_a-single-file-bind-mount-binds-the-inode.md lines 9-35 | read 2026-09-30
- demo moves only on Peter's nod | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md lines 232, 238-239 | read 2026-09-30
- co-tenant routing, watcher max timeout, next-up stall, re-key rules, read-from-a-SHA, pipes, verdict ratios, never delete | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md lines 63-105, 217-219, 287-291, 302-303, 329-344, 358-362 | read 2026-09-30
- Seat D 1st's lane and co-tenancy; #1358/#1360 not acted on | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD1-2026-09-30.md lines 1-8, 376-380 | read 2026-09-30
- 36 undelivered secuura- cards; secuura-ks1380-peter-reverting-1358 OPEN with default (a) | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` (rc 0, 36) and `show secuura-ks1380-peter-reverting-1358`, 19:3x AEST | read 2026-09-30
- routing: Secuura/Blockchain and Secuura/Blockchain-B share secuura-blockchain@agentmail.to | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf lines 29, 36 | read 2026-09-30
- UNMEASURED by the drafter (no host contacted): kintsugi's running SHA, census, disk, REVISION, the DB's highest migration, whether 038a is recorded, today's KS-535 hashes, today's /health body, whether python3 exists on the VM, whether the NSG still admits this Mac's egress; the seat closes each at ITEM 0 with the instrument named there | stated as UNMEASURED; the drafter connected only to github.com (ls-remote) | read 2026-09-30

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-30 19:52
    - One job: deploy the pinned develop to kintsugi and verify the running box. STOP 1 comes before any box write. STOP 2 comes before any migration, including the api-gateway recreate that runs 038a. A build failure is a STOP. No merge, push, comment, anchor, or demo action.
    - The #1360 rule appears in BLUF, ITEM 0 (a), ITEM 2 and HOLDS, and says the same each time: measure it at the pin; if it is in the pin (or the three images fail), STOP before any partial set is deployed.
    - "No ticket comment" appears in ITEM 6 and HOLDS. The only ruled texts named, in the gate49b ruling, are marked not this seat's.
    - KS-535: B 23rd's hashes are inherited and stated as inherited. Demo's 12ea1a07174c3f50 is spelled the same everywhere. Today's hashes are UNMEASURED.
    - The KS-1054 BEFORE (rc 2, field absent) is a drafter's EXPECTATION from #1332's merge date, marked "the drafter expects". The seat measures it.
