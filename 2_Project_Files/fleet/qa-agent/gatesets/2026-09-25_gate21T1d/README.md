# Gateset 2026-09-25_gate21T1d — README for Wednesday

The drafter launched NOTHING, sent NOTHING, tapped NOTHING and committed NOTHING. It wrote nothing outside its work dir (and the scratch clone +
controls dirs beside it in the session scratchpad).

This is ONE TIER-1 gate, **ROUND 2 of 2 (the cap)**, over ONE PR:
- **#1239** KS-1263, head `c8e1875c21e994a746e36c8b8efec8de1d9dbc98` (Seat B 27th, READY 11:05:25Z).

## 0. What the drafter measured (predict_1.out, gh_read, linear_reads, docker census)
- **The head's shape:** head^ == `42c20e998` (round 1's head), whose parent == BASE `6ab9d5021`. So the push was a fast-forward, 2 commits over BASE.
- **The round-2 delta is TEST-ONLY:** ks1228 +12/-0 and ks1263 +266/-9. The product blobs (documents.ts `ca5531ca…`, shareRepo.ts `1329fcee…`) are
  byte-identical to round 1's. So no new surface.
- **Develop** `33ccff807eb2bb0a43c5d03ceb88d877b86950e1` is 28 ahead of BASE. It MOVED during drafting from e68e2f0e8 (#1234's squash) via #1242
  KS-980 (33ccff807), which touched one file: the ks597 integration test. The kit was re-predicted and re-filled over it (predict_2.out, fill_3.out).
  - The move ∩ own paths = the same two known overlaps (documents.ts via #1225 + #1219; ks1228 via KS-1266).
  - It merges clean: merged tree = END_TREE `e666fb6e08b7efc84cf16c6820c9ac21a384688f`, by merge-tree AND apply --cached.
  - Patch-id is equal on both overlap paths.
- **THE REGION CHECK (re-measured):** the move's BASE-side hunks on documents.ts are 62, 64-65, 610-611, 841-849, 2333-2335 and 2341.
  - They sit in the header comment, the CREATE route and the /revoke comment.
  - /share is BASE 2128-2294 and /transfer-custody is BASE 1580-1935: **no hunk inside either.**
  - Both handlers are byte-equal BASE == develop, and merged == head.
  - The move touches none of db.ts, shareRepo.ts or packages/shared/src/db.
  - Substrate it does touch: run-migrations.sh (ab7826afb), originate package.json/lock (ecb1aa75a), the root lock (ba4016fb8). The gate runs
    develop's copies.
- **GitHub:** open, `mergeable True`. The compare develop...head reads merge_base BASE, ahead 2, behind 27, 6 files. The title is 89 chars ASCII. The
  body names KS-1155 ×2 and KS-1228 (hyphenated), and has no closing word.
- **Linear:** #1239 attaches to KS-1263 only (`contributes`, In Progress, 2 comments, the latest 11:04:35Z). KS-1304 and KS-1305 exist (both Backlog).
- **Routing:** `QA/Secuura-batch1239` is ABSENT (0). The control batch1234 is present (1).

Expected GO: `GO: merge #1239 batch`.

## 1. Read these WHOLE before launching
- **The prompt** `2026-09-25_secuura-batch1239-t1r2.prompt.txt`. It opens with `ultrathink`. It names `mail_gate21T1d_ready.md` (the READY, verbatim,
  TEXT_SHA256 `a02baa4b…`) and COMMISSION.md.
  - Sections: PRIOR ROUND (the round-1 report path); the head / BASE / move with the REGION CHECK; Wednesday's ruling (b); F1-F7 (the round-1
    dispositions); THE DISPOSABLE POSTGRES P0-P9; THE MATRIX; G-S2 (i)-(v); ALSO; leads (a)-(i); LOAD; the reaper; by-name items 1-12; merge authority;
    HOLDS; rules; the verdict, the addendum and the mail.
- **The launcher** `launch_qa_secuura_batch1239-t1r2.sh` (mode 755, `bash -n` rc 0). Opus by default: no `--model`.

## 2. The gate's design
**The database.** A disposable Postgres, `qa-g21T1d-pg-ks1263`, with a NAMED volume `qa_g21T1d_pg_ks1263`. It runs on the first proven-free port in
55450..55459, is labelled `com.secuura.qa.gate=gate21T1d`, and is removed at P9 with a proof of gone.
- It is built exactly as compose builds its postgres + migrations services: the same image, the docker/init AND docker/init-platform mounts, and
  run-migrations.sh with PLATFORM_DATABASE_URL=secuura_platform (docker-compose.yml's migrations service does the same).
- It also runs `log_statement=all`, so the statement log is a second witness of which withTenant branch ran and that it rolled back.

**The matrix (MODE T = MT=true + TEST_PLATFORM_DATABASE_URL → secuura_platform).**

| Run | Tree | Predicted |
|---|---|---|
| M-HEAD | head | 5/5 |
| M-DEVT | develop + the head's test file, byte-identical | 1 failed / 4. ROUTE-ROLLBACK red at :389 with "Expected: 0 / Received: 1"; the :387 status assertion passed; the route CONTROL green in the same run. RED-ATTRIBUTION: rows, never a connection, auth or module error. |
| M-BASE0 | the true merge-base | same as M-DEVT |
| M-MERGED | merged | 5/5 |
| T-TRAP | head, platform URL unset | 5 failed, each naming "getTenantManager() is null" (F3's red proof) |
| T-POOL | head, pool-branch ROLLBACK→COMMIT | D1/D2 + C7 red. The route cell is predicted GREEN: Postgres turns COMMIT of an aborted transaction into ROLLBACK. |
| T-ROUTE | head, round 1's module-client form in /share | ROUTE-ROLLBACK red "Received: 1" |
| MODE-F | head | 5 failed / 5 by name ('.prisma/client/default' ×3, KS-1305 ×2). The generated-client census comes first. Any green is VACUOUS. |
| C-CUSTODY | develop vs head | The drafter's add: a scratch route cell, with a DB trigger forcing the owner flip to fail. Round 2 did NOT commit one. The gate rules whether its absence blocks. |

**G-S2 (unit).**
- The head file is 29/29.
- With the tamper, the head file goes 1 failed / 28, G-S2 by title.
- The same tamper with round 1's ks1228 stays 29/29 (the gap).
- L1's SPLIT tamper reds exactly G-S1 and G-S2.
- The gate also reads whether `__txClient` is a different object from `prisma`.

## 3. What the launcher asserts on every run (`--check` and launch alike)
Exit codes in brackets:
- kit at home (2); one row, thinking directive, capture + commission named, no unfilled token (8);
- the head at its branch AND pull/1239/head (6); develop == pin (17);
- the compare: merge_base == BASE, ahead 2, behind 28, the 6 path NAMES (10);
- the head in full in the capture + prompt (20); the ticket (32); the tier / round-2-of-2 / cap lines (7);
- 23 seat items in BOTH files (30); 100 by-name keywords (33);
- base-invariant + region (34); disposable Postgres (35); mode rule / ruling (b) (36); F1-F7 (37); load + anchoring (38); holds (39); reaper (43);
- GO string (26); addendum (25); subject (23); BASE / R1 / develop / END_TREE (31);
- non-TTY launch (21); overrides at launch (16).

## 4. The routing line: NOT WRITTEN BY THE DRAFTER. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1239|coagent@agentmail.to|yes
Repin step 0 refuses with rc 1 without it (control R4).

## 5. THE LAUNCH COMMAND (copy + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate21T1d/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1d/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1d/repin_and_launch_gate21T1d.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1d/launch_qa_secuura_batch1239-t1r2.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad

The steps and their refusal codes:
- 0 routing (1).
- 0b moved kit: predict + fill re-run at the new home (8). Proved by controls R6 and F1 on a moved copy.
- 1 ls-remote develop + pull head + branch (2).
- 2 pulls API head + `mergeable`, re-read up to 3× while null (3).
- 3 head == pin on both instruments, open, not `mergeable:false` (11).
- 3b develop moved: re-pin with predict + fill in the same action, then develop re-read (10). Predict REFUSES a move into the handlers, db.ts,
  shareRepo.ts or packages/shared/src/db (controls P2 / P3).
- 4 usage gate (12).
- 5 `--check` (13).
- 6 `cockpit.sh add QA/Secuura-batch1239 <launcher>` (14), then a pane census.

Append `--dry-run` to rehearse steps 0-3.

## 6. Decide or know before launching
1. **Slot vs disposable: the drafter departed from your stated preference.** You preferred a free stack slot. Slots 2/3/4 WERE free at 11:09Z and
   11:21Z (0 volumes, 0 containers). The drafter still chose the disposable container, for three reasons:
   - (a) round 2's delta is test-only and no legs are owed, so a slot's only use would be its Postgres, at the cost of a 35-service `--rebuild`;
   - (b) a slot's S9 `--stop` KEEPS its volumes, which re-exhausts the pool Kam cleared at 20:52, while the disposable one is removed with a proof of
     gone;
   - (c) round 1 lost its slot to a race the S3 rule cannot see (batch1218-t2c).

   If you want the slot, say so before launch; the prompt's DB section would be re-drafted (S0-S9 from gate21T1c).
2. **The seat's MODE T platform DB may not have been a real secuura_platform** (lead b, READ ONLY).
   - Its env_up_b27.sh mounted docker/init only (no init-platform) and ran migrations WITHOUT PLATFORM_DATABASE_URL.
   - So its secuura_platform was created empty, and the tenants tables landed in the main DB.
   - Yet its runs printed "Loaded 0 tenant configs", a successful query. That is consistent with its platform URL naming the MAIN db.
   - It does not change the rollback mechanics: withTenant uses getDefaultPool() = DATABASE_URL. But your ruling (b) asked for a real
     secuura_platform, and the gate's run is the one that meets it.
3. **C-CUSTODY route cell.** Round 1's fix-shape asked for a route-level cell on BOTH routes; round 2 added /share only. The gate measures /transfer-custody
   itself (a scratch trigger cell) and rules whether the missing committed cell blocks. Under the cap, a NO GO ships nothing.
4. **MODE F generation:** the kit forbids `prisma generate` (your ruling: named residual, no package.json edit). If you want an INFORMATIONAL MODE F run
   on a generated client (the Dockerfile's `npx prisma generate`, no package.json edit), that is a new scope item — the drafter did not add it.
5. **Foreign on the box at 11:21Z:**
   - `s-b27-pg-ks1263` is still UP (127.0.0.1:55437), although the seat's READY says "Destroyed and proved gone before wrap". It was pre-wrap at the
     time.
   - Three anonymous volumes; 7b9c2cf8… was created 4 s after the seat's container start.
   - `qa-g21d-pg-ks980` was UP at 11:09Z and GONE at 11:21Z.

   The gate reports all of these and touches none.
6. **The squash:** own key only; the body drops KS-1155 and KS-1228. The subject can be the PR title (89 chars); the head commit subjects are 96 and 90.
7. **The seat's STOP count** (57 of 57, not 60) is a branch 27 behind develop: 3 suites were added on develop. The gate re-counts it statically, never
   by a run.

## 7. Controls: `controls_gate21T1d.sh <scratchpad> [--invert]`
Every control runs BOTH WAYS. A doctored arm must refuse with its own code. A PRISTINE twin goes through the same mechanism and must pass. `--invert`
flips every expectation.

The doctored arms and their twins pin develop to the launcher's pin (`pchk`), so a develop move mid-run cannot mask one as rc 17.

- **controls_1.out** (over e68e2f0e8, before the move and the final prompt edits): **90 OK / 0 MISMATCH of 90**, rc 0.
- **controls_2.out** (normal arm, final kit over 33ccff807): **90 OK / 0 MISMATCH of 90**, rc 0 (11:31Z-11:38Z).
- **controls_3.out** (`--invert`): **0 OK / 90 MISMATCH of 90**, rc 1 (to 11:47Z). Every control can fail.
- **repin_dryrun_1.out** rc 0 (over e68e2f0e8). **repin_dryrun_2.out**, re-run after the controls at 11:47Z: rc 0 over 33ccff807, `mergeable True`.
- **launcher_check_2.out** rc 0 over 33ccff807. (fill_2 rc 0 over e68e2f0e8; fill_3 first REFUSED on the develop move (rc 1, correct), then passed rc 0
  after predict_2.)

Covered: launcher P C C2 D V O G U H20 T I I2 K K2 B B2 S S2 S3 S4 R R2 R3 R4 R5 F F2 Y Y2 Hh Z A E E2 J W W2 N N2 M; repin R1-R6; predict P1
(older develop), P2/P3 (the region guard: a synthetic hunk inside /share, inside /transfer-custody), P2/twin (a hunk in /revoke passes); moved-kit
F1 (predict + fill + --check at a new home).

## 8. Files
- COMMISSION.md · README.md · PROPOSED_inbox_routing_line.txt
- mail_gate21T1d_ready.md (the READY capture) · gh_body_1239.md · linear_KS-1263.md
- predict_gate21T1d.py / predict_1.out / pins_gate21T1d.json
- prompt_gate21T1d.TEMPLATE.txt · launcher_gate21T1d.TEMPLATE.sh.txt · fill_gate21T1d.py / fill_*.out
- the prompt, the launcher, launcher_check_*.out
- repin_and_launch_gate21T1d.sh / repin_dryrun_*.out
- controls_gate21T1d.sh / controls_*.out
- gh_read_gate21T1d.py, linear_reads_gate21T1d.py
- _meas/: ready_raw_1 (the instrument's raw output), gh_read_1, linear_reads_1, docker_census_1, documents_head.ts, own1239.txt

## 9. NOT done / NOT measured by the drafter
No launch, mail, tap, commit, push, or routing-conf write. The Secuura checkout was touched only by read verbs (ls-remote, cat-file, show, diff,
log, merge-base, rev-parse, rev-list, ls-tree, grep, config --get). Every write verb ran in the scratch clone `<scratchpad>/g21T1d_sp/clone`. No
container, volume or port was created or touched: docker was READ only (info, ps, volume ls/inspect, image ls).

Not pre-run (these are the gate's job): any jest run, the database, MODE T / MODE F, the tampers, tsc, eslint.

UNMEASURED:
- whether the seat's test file passes on a compose-built secuura_platform (the seat's platform DB is in doubt, §6.2);
- whether `tenants` exists in the MAIN db under the compose build (the file's swallowed seed, lead e);
- whether the gate's `npm ci` leaves a generated Prisma client (MODE F's premise, census first);
- whether a C-CUSTODY route cell reaches the INSERT under the file's mock set;
- the usage gate's state and Docker's health at launch.
