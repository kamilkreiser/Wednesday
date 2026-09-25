# Gateset 2026-09-25_gate21T2d — README for Wednesday

The drafter launched NOTHING, sent NOTHING, tapped NOTHING and committed NOTHING. It wrote nothing outside
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate21T2d/`.

This is ONE TIER-2 batch gate, the round's FOURTH, round 1 of 2, over TWO PRs from ONE seat (Seat B 26th), FROZEN:
- **#1241** KS-1226 item 2, `e2d0518df40228f0a183bc4223c7a6840821253e` — systemTest/performance `unitSuiteSlotIndependence.test.ts` (the file is its own product)
- **#1242** KS-980, `a35569aa020e63b2660b60e48b4f0286c46b27fc` — originate `ks597-issuer-organization-id.integration.test.ts` (test-only, DB-backed)

Routing `QA/Secuura-batch1241`. GO string: `GO: merge #1241, #1242 batch`.

## 1. Pins (measured, predict_3.out at 10:25:56Z; re-read in repin_dryrun_2.out at 10:26:53Z)
- BASE for both heads: `aa600af94d69ad59db279d32cbbd7596931a739b`. Each head is ONE commit whose parent is BASE; merge-base(develop, head) == BASE.
- Develop: `e68e2f0e837df86da527d775a3a49c631b0f5b17`, 10 ahead of BASE.
  - The commits: #1240, then the eight gate21T2c squashes #1218 … #1238, then **#1234 KS-1127 RSSCOUNT, which landed at ~10:1xZ during the drafter's
    controls** (controls_2.out: 73 arms read exit 17).
  - Wednesday's commissioning read was `c41e268eb`. That tree is exactly gate21T2c's predicted END_TREE `15dfe75db96e…`.
  - #1234 touches run-shell-suites.sh + its test only, disjoint from both PRs. It **changes the runner's summary line** to `shell suites: N passed,
    F failed, S skipped (of N)`. The prompt tells the gate the STOP line now carries a skipped segment.
- Instruments: `ls-remote` from the Secuura checkout (read verb only), a fetch FROM ORIGIN into a scratch clone under `_sp/` (`--shared` from the
  checkout, write verbs only there), the GitHub compare and pulls APIs.
- **No declared overlap.** The move's 14 paths ∩ each PR's one path = EMPTY. #1241 ∩ #1242 = EMPTY.
- Merged trees over e68e2f0e8: #1241 `7d425e5ac19d021b8e47fd3958ac595e0fad5b3a`, #1242 `3d71522b696407628949ebec76d731a04ece9241` — each diff(develop, merged)
  == its own path at the head blob; numstat 47/1 and 93/2 equal BASE..head.
- END_TREE `4ee2ff4a5f43e86eea1a018ff57eba71666c410f`, both orders + `apply --cached` agree: 2 files, +140/−3.
- Fleet STOP count (static, no suite run): 59 shell suites at BASE → 60 at develop and on the END_TREE; #1218 is on develop (1609ecbf6).

## 2. What the gate owes (the prompt, `2026-09-25_secuura-batch1241-t2.prompt.txt`)
**#1241 — LIVE-SHAPE decides it.** The drafter READ the checkout's installed vitest (4.1.9; the lockfile pins 4.1.11). Both of its summary
renderers print `failed | passed | expected fail | skipped | todo (total)`, so skipped comes AFTER passed. The PR's regex (and its cells) accept
skipped only BEFORE passed. predict's table: on vitest 4's order, e.g. `Tests  1 failed | 243 passed | 1 skipped (245)`, the HEAD regex returns NULL,
exactly as BASE does. The ticket's example line looks like a line the 09-17 gate COMPOSED for its probe's controls (the ticket calls F5
"measured (probe, controls)"), not an observed vitest line. The prompt makes the gate:
- run a real vitest 4.1.11 with a skipped test, piped, and quote the `Tests` line;
- apply both regexes to it;
- rule NO GO if the head regex is NULL on the live line.

Also for #1241:
- the seat's two-step red proof;
- **T-CAP**: make the group capturing. Predicted red: R1, R2 and C1.
- **T-103**: change only :103's reading. Predicted: all 5 cells stay green, because `readSummary` re-implements :103.
- package counts: 1085 → 1090 at the head; the merged prediction is 1094, because develop carries #1236's +4.

**#1242 — THE DISPOSABLE POSTGRES (P0–P9) + T-GUC.**
- No stack slot is free. At 09:21:53Z Docker had 0 containers, but slots 2, 3 and 4 each hold KEPT volumes; slot 4 was created 09:00:00Z by the
  running tier-1 gate batch1234.
- So the gate runs ONE container `qa-g21d-pg-ks980` (postgres:15-alpine, present locally) on its own named volume `qa_g21d_pg_ks980`. It binds only
  127.0.0.1, on the first proven-free port in 55441..55449; the lsof control on :5432 must show the instrument discriminates.
- Credentials are generated into `private/pg.env` (0600) and never printed.
- The DB is built with docker/init + `run-migrations.sh`, using the host libpq at `/opt/homebrew/opt/libpq/bin`, because pg_isready is not on PATH —
  the seat's side finding.
- Tear-down removes that container and that volume only, with a proof of gone: 0 containers, `volume inspect` fails, `volume ls` == the P0 list, 0
  listeners.
- Red proofs:
  - the seat's arms A,B and C;
  - **T-GUC**, the gate's own: drop the `platform_admin` arm from the organizations policy in the gate's DB. Expected: the BASE file's P1 cell stays
    GREEN, which is the defect, and the HEAD's P1 cell + D2 go RED.
- Also **T-SUPER** (lead f): D1 reads `rolbypassrls` only and never `rolsuper`.

## 3. What the launcher asserts on every run (`--check` and launch alike)
Exit codes in brackets:
- kit at home (2);
- two rows / thinking directive / capture + commission / no unfilled token (8);
- heads at branch AND pull/N/head (6); develop == pin (17);
- the GitHub compare per PR: merge_base == BASE, ahead 1, behind 10, file NAMES (10);
- heads in full in capture + prompt (20); tickets (32); tier lines + round (7);
- 33 seat items in BOTH files (30); 113 by-name keywords (33);
- base-invariant, no overlap (34); disposable Postgres (35); red proof (36); fleet STOP after #1218 (37); load + anchoring (38); holds (39);
- LIVE-SHAPE (40); T-GUC (41); reaper (43);
- GO string (26); addendum (25); subject (23); BASE / develop / END_TREE (31);
- non-TTY launch (21); overrides at launch (16).

## 4. The routing line: NOT WRITTEN BY THE DRAFTER. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1241|coagent@agentmail.to|yes
The drafter's read: batch1241 is ABSENT (0); the control batch1234 is present (1). Without the line, repin step 0 refuses with rc 1 (control R4).

## 5. THE ONE LAUNCH COMMAND (copy to gatesets/ + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate21T2d/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2d/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2d/repin_and_launch_gate21T2d.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2d/launch_qa_secuura_batch1241-t2.sh <your session scratchpad under /private/tmp/claude-501/>

Step 0b sees a MOVED KIT and re-runs predict + fill at the new home in the same action. Both re-read origin and refuse on any disagreement. Controls
R6 and F1 prove this on a moved copy.

The steps and their refusal codes:
- 0 routing (1)
- 0b moved kit: predict + fill (8)
- 1 ls-remote (2)
- 2 pulls API + `mergeable`, re-read up to 3× while null (3)
- 3 heads == pins on both instruments, open, not `mergeable:false` (11)
- 3b develop moved → predict + fill, then develop re-read (10)
- 4 usage gate (12)
- 5 `--check` (13)
- 6 `cockpit.sh add QA/Secuura-batch1241` (14), then a pane census

**Rehearsal:** append `--dry-run` to the last command to rehearse steps 0–3.
- `repin_dryrun_1.out`: rc 0 at 09:34:49Z over c41e268eb.
- `repin_dryrun_2.out`: rc 0 at 10:26:53Z over e68e2f0e8, `mergeable True` ×2. Both were null at 09:20:54Z.

## 6. Decide or know before launching
1. **#1241 will most likely fail on LIVE-SHAPE (READ ONLY, strong).** You can:
   - (a) launch as drafted and let the gate measure it and rule. The drafter's recommendation: it costs minutes, and #1242 is graded in the same
     session.
   - (b) hold #1241 and send Seat B 26th the vitest-order evidence (predict_1.out section (f)) before any gate. The kit is frozen at two, so (b)
     needs a one-row re-draft.
2. **The Postgres plan for #1242 is a disposable container, not a slot.** No slot is free: slots 2, 3 and 4 each hold kept volumes.
   - The gate may remove exactly ONE volume, its own named `qa_g21d_pg_ks980`. The HOLDS carve out that exception. If you want no volume rm at all,
     change P4 to an anonymous volume and P9 to `docker rm -f -v <name>` + a proof of gone.
   - The port range is 55441..55449. 55432 (the seat's) is excluded.
3. **Seat B 26th left an anonymous volume behind.** Volume `0ec12181dd37…` was created at 07:43:16Z; the seat's container started at 07:43:11Z.
   `docker rm -f` without `-v` keeps an anonymous volume, so the READY's "Torn down" is partly refuted. The gate REPORTS it and never removes it.
   Tell the seat to remove its own volume, or rule it harmless.
4. **`mergeable: null` policy.** As in gate21T1c, null is reported after 3 reads, not refused; `false` refuses.
5. **The tier-1 gate batch1234 (pane %16) looks finished with Docker.** Its evidence has 39_S9_teardown and 98_final_census, and at 09:21Z there were
   0 containers. The prompt still never touches a slot.
6. **#1242's "FULL originate integration 14/14 (2 suites)" vs THREE files** matched by `jest.integration.config.js`. The gate's K2 runs the config
   unfiltered at BASE, head and merged. A red rightsHolders suite at BASE is pre-existing.
7. **The seat asked Wednesday in its READY** whether to file the run-migrations.sh / pg_isready finding. That is still unanswered, and it is yours;
   the gate only confirms it by reading the script.

## 7. Controls: `controls_gate21T2d.sh <scratchpad> [--invert]`
Every control runs BOTH WAYS:
- A DOCTORED arm plants one defect and must refuse with its own code.
- A PRISTINE twin goes through the same override or copy mechanism and must pass.
- `--invert` flips every expectation, which proves each control can fail.

Runs:
- **controls_1.out: 89 OK / 1 MISMATCH.** The mismatch was F2, a drafter harness bug. The predict simulations refused correctly (rc 1) but crashed on
  the END_TREE step before writing their SIM pins, so F2 had nothing to swap in. Fixed:
  - predict records the conflict as a hard fail and still writes its FAIL-carrying pins (`.pre-f2fix` kept);
  - F2 now asserts that the SIM pins file exists and was swapped in (else rc 96, never a vacuous pass).
- **controls_2.out: 17 / 73 — INVALID.** Develop moved mid-run (#1234 landed), so the doctored arms read exit 17. I stopped the run and re-predicted
  over e68e2f0e8 (predict_3.out). The doctored and twin arms now pin `QAB1241_CUR_DEV` to the launcher's own pin, via `pchk` (`.pre-devpin` kept).
  P, D, M/twin, N2 and the repin arms still read the live develop.
- **controls_4.out (normal): 90 OK / 0 MISMATCH of 90**, rc 0, 10:26–10:40Z.
- **controls_5.out (`--invert`): 0 OK / 90 MISMATCH of 90**, rc 1, to 10:54:48Z.

Covered:
- launcher: P, C, D, V, O, G, U, H20, T, I, I2, K, B, B2, S–S5, X, F–F3, Y–Y3, Hh, Q–Q3, R, R2, Z, A, E, J, W, N, N2, M;
- repin: R1–R6;
- predict: P1/P2 (a FOREIGN edit of each PR's own file over develop → refuses) + twin;
- fill: F2 (refuses SIM pins) and F1 (moved-copy re-fill + `--check`).

After the controls, one prompt sentence changed: predict_1.out became predict_3.out as the newest measurement. I re-filled (fill_5.out), and
`--check` (launcher_check_4.out) and the dry run (repin_dryrun_3.out, rc 0, 10:55:20Z) both pass. No rule anchor changed.

## 8. Files
- COMMISSION.md · README.md · PROPOSED_inbox_routing_line.txt
- predict_gate21T2d.py / predict_1..3.out (3 = the pinned one) / predict_simforeign124{1,2}_1.out (rc 1, the negative controls) / pins_gate21T2d.json
- prompt_gate21T2d.TEMPLATE.txt · launcher_gate21T2d.TEMPLATE.sh.txt · fill_gate21T2d.py / fill_N.out
- the rendered prompt, the launcher (`bash -n` rc 0), launcher_check_1.out
- repin_and_launch_gate21T2d.sh / repin_dryrun_N.out
- controls_gate21T2d.sh / controls_N.out
- mail_gate21T2d_ready.md + mail_seatB26th_ready_1241.md / _1242.md (verbatim, TEXT_SHA256) and capture_mail_gate21T2d.py / capture_1.out
- gh_read_gate21T2d.py / gh_read_1.out / gh_body_*.md / gh_comments_*.md
- linear_reads_gate21T2d.py / linear_reads_1.out / linear_KS-1226.md / linear_KS-980.md
- docker_info_1.out
- `_sp/`: the drafter's scratch clone and control workdirs. The launch command excludes it.

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, commit, push or routing-conf write.
- The Secuura checkout was touched only by read verbs: ls-remote, config --get, and `clone --shared` reading it as the source of a scratch clone
  under `_sp/`. The checkout's installed vitest dist and docker-compose.yml were read as plain files. Every git write verb ran in the scratch clone.
- The inbox was read only as `inbox_digest.sh full wednesday-agent@agentmail.to '<id>'` for the two ids.
- Docker was read only: info, ps, volume ls/inspect, image ls.
- Not pre-run (the gate's job): any suite, tsc, a red proof, a live vitest summary, the database.
- UNMEASURED:
  - the live vitest 4.1.11 summary shape (the drafter's claim is READ from 4.1.9's dist);
  - whether all 49 migrations apply cleanly with the host libpq client;
  - secuura_app's grants after the migrations;
  - whether T-GUC's policy recreate separates BASE from HEAD as predicted;
  - T-SUPER's outcome;
  - the rightsHolders suite on a fresh DB;
  - Docker's health, the usage gate and the machine load at launch;
  - the step-3b re-pin end to end.
- Not controlled:
  - exit 16 (needs a TTY);
  - the repin's `mergeable=False` refusal (no override);
  - the real launch path.
