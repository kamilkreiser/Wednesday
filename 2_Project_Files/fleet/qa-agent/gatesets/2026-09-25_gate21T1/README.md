# Gateset 2026-09-25_gate21T1 — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, committed NOTHING, wrote nothing outside this directory + its scratchpad)

ONE TIER-1 batch gate, round 21, round 1 of 2, over FOUR PRs on develop `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (== BASE; every head's parent):
**#1213 KS-530 PATCHLINE** `f2751859c01565df066a3cdbe008e7360de4205a` (Seat B 25th; 3 lock/manifest files) · **#1214 KS-528 DOMPATCH**
`6fce4d0b188655a520e97447d3bfb1749d22a435` (Seat B 25th; 4 locks + the ONE authorised baseline row removal) · **#1216 KS-975 SCOPENULL**
`c44b15dddaddac3dec1d4deff224efd01b7565f2` (Seat L2; security) · **#1217 KS-976 MSG400** `e83f344474028215ae827b2f74fd3a06566d4c23` (Seat L2; security).
13 paths, pairwise disjoint; END_TREE `e0c9da50521ba0657629218931e42bf7913df095` (three orders + `apply --cached`; `13 files changed, 370 insertions(+), 59 deletions(-)`).
Built in the shape of `../2026-09-23_gate20T1r2_1210/` (template + pins + fill) widened to four rows, with the batch guards of `../2026-09-23_gate20T1_seatB/`.
The expected GO: `GO: merge #1213, #1214, #1216, #1217 batch`.

## 0. The kit is SELF-LOCATING — it was drafted in the drafter's scratchpad
Every path in the prompt and launcher is the directory `fill_gate21T1.py` ran in. The launcher refuses (exit 2) if it is not in the directory it was
filled for; `repin_and_launch_gate21T1.sh` step 0b re-fills IN PLACE when the kit has been moved (proved: controls R6 + `movedkit_fill_1.out` /
`movedkit_check_1.out`: a copy re-filled at its new home and passed `--check` rc 0). So: copy the directory to its gatesets/ home and run the one command.

## 1. Read WHOLE before launching
- The prompt `2026-09-25_secuura-batch1213-t1.prompt.txt` (fill_2.out: 173 lines, 42582 B at the scratch home — the byte count changes with the home
  path when re-filled). Opens with `ultrathink`; names the capture `mail_gate21T1_ready.md` (the three READY FOR QA mails, verbatim by message id) and
  COMMISSION.md; the four `PR #N is KS-n.` rows; THE STACK S0-S9; THE BASELINE EDIT; THE LOCK DIFFS; LOAD; leads (a)-(k); by-name items 1-12; HOLDS;
  the GO string VERBATIM. Go-template braces (`{{.Names}}`, `{{index .Config.Labels …}}`) in the S2/S4 docker commands are intentional.
- The launcher `launch_qa_secuura_batch1213-t1.sh` (232 lines, mode 755, `bash -n` rc 0; sha256 changes on every fill because it stamps the time).
  Opus by the configured default: the exec line has NO `--model`.

## 2. What the launcher asserts at every run (`--check` and launch alike)
kit at its filled home (2) · four rows (8) · thinking directive + capture + commission at this dir + no unfilled fill token (8) · each head at its branch
AND refs/pull/N/head (6 — a STALE HEAD REFUSES) · origin develop == the pinned launch develop (17) · the compare per PR: merge_base BASE, ahead 1,
behind == pin, files 3/5/2/3 (10) · heads in full in capture + prompt (20) · `PR #N is KS-n.` in both (32) · tier lines (7) · 39 BOTH tokens (30) ·
70 by-name keywords (33) · the STACK rule (35) · the BASELINE rule (36) · the LOCK rule (37) · the LOAD rule (38) · the HOLDS (39) · merge authority +
GO string (26) · MERGE ADDENDUM (25) · subject / sender / four lines (23) · BASE / develop / END_TREE in full (31). Non-TTY launch refuses (21);
QAB1213_* overrides refuse at launch (16).

## 3. Controls — `controls_gate21T1.sh` -> `controls_2.out`: 24 OK / 0 MISMATCH (03:52:03Z; controls_1.out the same, 03:45:24Z)
Launcher: P positive 0 · C stale #1217 head 6 · D develop moved 17 · G no ultrathink 8 · U unfilled token 8 · O capture missing a seat item 30 ·
T ticket statement 32 · I tier line 7 · L keyword 33 · K stack rule 35 · K2 "a SKIP is not a pass" 35 · B baseline rule 36 · X lock rule 37 ·
Y load rule 38 · H holds 39 · A GO string 26 · N non-TTY 21 · M moved launcher 2. Repin: R1 positive dry run 0 · R2 stale head 11 · R3 pinned develop
stale 10 · R4 a REAL run with the routing line absent stops at step 0, rc 1 (skipped automatically once the line exists) · R5 bad scratchpad 9 ·
R6 moved-kit dry run 0 with the MOVED KIT line reported.

## 4. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST (`PROPOSED_inbox_routing_line.txt`)
Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (back it up first with a `$(date +%H%M)` stamp):
    QA/Secuura-batch1213|coagent@agentmail.to|yes
The repin script's step 0 checks for it (rc 1 if missing; control: the batch1204 line = 1). Drafter's read: batch1213 ABSENT (0 hits for `1213`).

## 5. The exact launch command (copy + re-pin + launch; run it in a shell that can reach tmux)
    cp -Rp /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fd48946b-a14b-4837-ab61-8d5d11816b69/scratchpad/gate21T1 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1 && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1/repin_and_launch_gate21T1.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1/launch_qa_secuura_batch1213-t1.sh <your session scratchpad under /private/tmp/claude-501/>
Steps: 0 routing (1) · 0b moved kit -> re-fill here (8) · 1 ls-remote develop + four pull heads + branches (2) · 2 pulls API (3) · 3 heads == pins on
both instruments, all open (11) · 3b develop re-read: unmoved -> go on; moved -> predict + fill in the same action, then develop re-read once more (10)
· 4 usage gate (12) · 5 `--check` (13) · 6 `cockpit.sh add QA/Secuura-batch1213 <launcher>` (14) + pane census. Append `--dry-run` to rehearse 0-3.

## 6. The stack (legs 3/4/8 for #1216 / #1217) — the repo's own scripts, found at BASE
- Start: `SECUURA_STACK_SLOT=<N> bash <clone>/Start_Up/start-secuura.sh --rebuild` (repo root; sources `Blockchain/Dev/scripts/stack_env.sh`, runs
  `Blockchain/Dev/scripts/stack_guard.sh` before a rebuild, `bootstrap-env.sh` for .env, builds serially `BUILDX_NO_DEFAULT_ATTESTATIONS=1 COMPOSE_BAKE=0
  docker compose --progress=plain -f docker-compose.local.yml build <svc>`, then `docker compose -f docker-compose.local.yml up -d`).
- Stop: `SECUURA_STACK_SLOT=<N> bash <clone>/Start_Up/start-secuura.sh --stop` (guarded `docker compose down`, volumes kept). (`Blockchain/Dev/stop-secuura.sh` is the other stop path.)
- Legs, as `Blockchain/Dev/scripts/preflight/preflight.sh` runs them (GATEWAY_URL default `http://localhost:6882`): `node scripts/preflight/spec-auth-conformance.mjs --base $GW` (3),
  `node scripts/preflight/path-resolvability.mjs --base $GW` (4), `node scripts/preflight/spec-endpoint-consistency.mjs --base $GW` (8), after `(cd scripts/preflight && npm ci --ignore-scripts --no-audit --no-fund)`.
- The daemon: Docker Desktop (`/Applications/Docker.app`, context desktop-linux), DOWN at the drafter's read (`docker_info_1.out`, rc 1); the prompt starts it with `open -a Docker`.
- Hazard carried into S2: `restart: unless-stopped` appears 40 times in `Blockchain/Dev/docker-compose.yml` — a pre-down stack can auto-start with the daemon; the gate reports it and never stops it, and builds in a free slot 2-4.

## 7. Files
COMMISSION.md · PROPOSED_inbox_routing_line.txt · lsremote_1.out · gh_read_gate21T1.py / gh_read_1.out / gh_body_{1213,1214,1216,1217}.md /
gh_comments_*.md · capture_mail_gate21T1.py / capture_list.out / capture_1.out (swept one non-READY in: "ALREADY" contains READY — fixed) /
capture_2.out (rc 0, 3 READY sections, all four keys) · mail_*.md (41 per-mail files + the combined mail_gate21T1_ready.md = 42) · linear_reads_gate21T1.py /
linear_reads_1.out · predict_gate21T1.py / predict_1.out + predict_2.out (rc 0, 0 hard fails each) / pins_gate21T1.txt / devlog_gate21T1.txt (empty:
develop == BASE) · docker_info_1.out · prompt_gate21T1.TEMPLATE.txt + launcher_gate21T1.TEMPLATE.sh.txt + fill_gate21T1.py / fill_1.out / fill_2.out
(+ the `.pre-034644` copies of fill 1's outputs) · launcher_check_1.out / _2.out · repin_and_launch_gate21T1.sh (NOT run for real; R4 ran for real and
stopped at step 0) · controls_gate21T1.sh / controls_1.out / controls_2.out · movedkit_fill_1.out / movedkit_check_1.out.

## 8. What the drafter measured that Wednesday may want before the GO (from predict_2.out / gh_read_1.out / linear_reads_1.out)
- #1214's baseline edit is EXACTLY one member (`accepted` 26 -> 25, removed [GHSA-jjmj-jmhj-qwj2], 0 added, 0 changed, `$comment` equal, text 0/7);
  #1213's baseline blob == BASE (the frvp re-date is NOT at this head).
- Lock census, all six locks: added 0 / removed 0; version-changed exactly the named packages (1213: @hono/node-server ×2; 1214: react-router-dom,
  react-router, @remix-run/router ×4); 0 other-field changes; 0 resolved/integrity moves on an unchanged version; libc/os/cpu counts unchanged.
- #1216: the principalScope function text byte-identical BASE -> head (control: explicitScope seen changing); its 4 changed lines naming principalScope are comments.
- #1217: `Key required` was 1 hit under services/security at BASE (index.ts:1476); at the head the product line uses `bodyRefusalMessage`; 0 under docs/.
- Linear: attachmentsForURL = own key only, `contributes`, on all four; KS-530 / KS-528 / KS-975 / KS-976 In Progress.
- **For the squash (MG-3):** #1217's PR body names KS-970 (archived) and KS-974 as content; the squash body must carry only KS-976 — lead (d) asks the gate to rule the wording.

## 9. NOT done / NOT measured by the drafter
No launch, mail, tap, commit or routing-conf write. The Secuura checkout was touched only with `ls-remote`, `cat-file -t`, `show`, `ls-tree`
and `config --get`; every git write verb ran in a scratch clone FROM ORIGIN under the scratchpad. NOT pre-run (the gate's job): any suite, tsc, eslint,
audit:gate / audit:locks / audit:contract, any red proof, `npm ci`, the stack. UNMEASURED: whether Docker Desktop comes up and how long the 27-service
serial `--rebuild` takes under five-seat load (time-boxed at 60 min in the prompt); which containers/volumes exist once the daemon is up (a slot 2-4
choice depends on it); whether legs 3/4/8 pass at develop; registry reachability for audit:gate; the usage gate's state at launch; the develop-moved
branch of step 3b end to end (develop has not moved — its parts ran over the current develop).
