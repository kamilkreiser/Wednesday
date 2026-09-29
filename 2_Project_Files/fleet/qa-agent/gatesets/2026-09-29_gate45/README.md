# Gateset 2026-09-29_gate45 — README for Wednesday

Written 2026-09-29T11:26Z by the drafter (times from `date -u`). Every figure below is read from the kit's own output files, each named beside it.

**What the drafter did and did not do.**
- It launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR, and deleted nothing.
- It wrote this kit directory (text files only) and scratch under its session scratchpad `g45_sp/`:
  - `clone`: a `git clone --shared --no-checkout` of Wednesday's `screen0929/base` clone, fetched from origin ONLY there, with the Secuura deploy key (`refs/pull/1348/head`, `refs/pull/1347/head`, develop);
  - the synthetic control commits (made by plumbing in that clone) and the control plants under `controls_<HHMMSS>/`;
  - the return-probe drivers.
- It did NOT write the routing line (§4).
- The Secuura checkout was touched by read verbs only: `ls-remote` in the launcher, the repin, and the final read.
- GitHub: REST GET only (gh_read_1.out / gh_read_1.json, gh_body_<n>.md; the launcher's compares; the repin's PULLS reads).
- Linear: ONE read-only GraphQL `issue` query per key, KS-1054 and KS-1374 (linear_read_gate45.py; no mutation in the file).
- AgentMail: ONE read-only listing of wednesday-agent@ (_mail_list_1.out) and nine by-id GETs (capture_mail_gate45.py). No seen-state was touched and nothing was sent.
- The ONLY measurement of subject behaviour is drafter_return_probe.out (§2.1). The drafter ran no suite, npm install, tsc, eslint or deploy-script drive (§6).

**gate45 = TWO PRs from Seat B 45th, who is also the MERGER.**
- T1: #1348 (KS-1054, the deploy.sh half, a DEPLOY-PATH change, full weight).
- T2: #1347 (KS-1374 **ROUND 2 OF 2**, the last round under the cap: a NO GO ships nothing of it).
- Merge order: 1348, then 1347, each squash on the previous tip.
- **Both merge cleanly AS-IS over develop `8ba2da02d980`. No rebase is needed.**

| PR | ticket | tier | head (ls-remote pull/head == branch == API == fetched) | parent | behind develop | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1348 | KS-1054 | T1 | `1bb58b4ebb97d2fa9f04bddd961ad499b6106e09` | `8ba2da02d980` (= develop) | 0 | 2 | 77 -> 85 (PR title) |
| #1347 | KS-1374 r2 | T2 | `18bc5123ce90b4c2cf2a9b22f141e1c2b81083c0` | `2c4b98253b1f` (round 1; merge-base `bd740147c3d8`) | **1** | 6 | 83 -> 91 (**drafter's proposal, NOT the title**; the title is 84 -> 92) |

- Pane `QA/Secuura-batch1348`. **It is NOT routed by the drafter**, see §4.
- GO string, as the GO mail's SUBJECT: `GO (Seat B 45th): merge 1348 1347 on gate45`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-29-batch1348-g45/`.
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE45 batch #1348 #1347 (Seat B45, round 45; T1: KS-1054 deploy.sh exits non-zero on verify issues; T2: KS-1374 round 2 of 2)`.

## 1. BLUF
- **Kit: READY to launch once the routing line is added (§4).**
  - Launcher `--check` rc 0 (launcher_check_1.out: `all guards pass:`). It confirms 2 of 2 heads at the branch AND at pull/head, 2 of 2 GitHub compares equal to the pins, and 53 by-name keywords present.
  - Repin `--dry-run` rc 0 (repin_dryrun_1.out: `DRY RUN COMPLETE 2026-09-29T11:25:46Z`). It printed `BOTH INSTRUMENTS AGREE with the pin, 2 of 2` and the census line `20 other open PR(s) read | 0 touch a kit path or carry a kit key`. Its only report was that the routing line is absent, which is the one thing the real run would refuse on.
- **Pins** (pin_1.out, rc 0; ls-remote at 2026-09-29T11:07:07Z):
  - develop is `8ba2da02d980e7e8065e8ce614b034adc2b7c2eb`, equal to the commission's develop, and equal to #1346's squash on `bd740147c3d8`.
  - Each head equals its branch, the PULLS API head (gh_read_1.out) and the fetched ref.
  - #1347's head's parent is round 1 `2c4b98253b1f`, so round 2 is a fast-forward, as claimed.
- **Clean-merge status (commission: "predict whether #1347 merges cleanly")**:
  - #1347 is 1 behind. The move `bd740147c3d8..8ba2da02d980` is #1346's four paths, and pin (C) found `reaches its own paths: NONE`.
  - Pin (E): #1347 ALONE over develop gives merge-tree rc 0, tree `e889329f530b…`, with diff == own paths and blobs+modes == head.
  - Pin (F): chain 1348 -> 1347 is clean at both steps.
  - GitHub also reports `mergeable: True` for both (repin_dryrun_1.out).
- **END_TREE `9222b67ef2039327a9debfb25a652c1bbf7e8fc8`** (pin (F)/(G)):
  - `diff(develop, END)` is exactly the union of the 8 own paths, and every END blob and mode equals its head's: `8 files changed, 573 insertions(+), 14 deletions(-)`.
  - The reverse order gives the same tree: True.
  - Overlap: `1 pair(s) checked, 0 overlapping | 8 path(s) in total, 8 distinct`.
- **Recorded modes** (pin (H)): deploy.sh is **100755** and the ks1054 test file is **100644**, at head, alone tree, chain step and END. `MODE SUMMARY: 2 path(s) pinned, 2 OK | pins seen: ['100644', '100755']`.
- **Controls, both ways** (controls_gate45.sh, one unedited script, sha256 `4e3584927c41…` before run 1 and after run 2, controls_sha.txt):
  - normal (controls_1.out, rc 0): `SUMMARY gate45: 66 controls, OK 66, MISMATCH 0`;
  - `--invert` (controls_2.out, rc 1): `SUMMARY gate45: 66 controls, OK 0, MISMATCH 66`.
- **Test census** (testrefs_1.out, rc 0, `git grep` at END over Blockchain/** and systemTest/**): **41 test files**.
  - #1347 round 2 now changes `docker-compose.yml` (one comment line, :497), which accounts for 27 of the hits.
  - deploy.sh is reached only by BASENAME: PATH finds 0 and BASENAME finds 1, the ks1054 suite via `$AZ/deploy.sh`.
  - CT-POS #1348 1 of 1, CT-POS #1347 2 of 2 (the api-gateway cell now reads a CHANGED path), CT-NEG 0, CT-TREE (2 NEW test files absent at develop), CT-KNOWN.
- **Key scan** (keyscan_1.out, rc 0): `KEYSCAN PASS: 12 checks over 2 PRs, 0 FAIL, 0 FLAG line(s)`.
  - Each subject's only key is its own. No subject carries `(#n)`. Landed lengths are 85 and 91.
  - Mandated bodies are `Refs KS-1054` and `Refs KS-1374`.
  - Control KS8 shows the scan PASSES #1347's stale title too (84 -> 92). The key scan cannot judge TRUTH, so the gate must (§2.4).
- **Heads re-read at the end**: final_lsremote_1.out (2026-09-29T11:26:00Z) shows develop `8ba2da02d980`, #1348 `1bb58b4ebb97` and #1347 `18bc5123ce90`, each equal to its branch. `every pin still current: True`.

## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated; every one is in the prompt as a by-name item the gate must RULE)
1. **E1 IS BLIND TO THE RETURN VALUE — #1348 (MEASURED, drafter_return_probe.out, bash 3.2.57).**
   - E0-E2 run deploy.sh's extracted summary block as a SCRIPT (`bash "$TMPDRV"`), so its `return` is at top level.
   - A top-level `return N` in a non-sourced script is an error ("can only `return' from a function…"). It exits **rc 1 for `return 1`, `return 0` and `return 7` alike**.
   - So with `return 0`, E1 would still read green, while the real function returns 0 and deploy.sh exits 0 over failed migrations.
   - Control: the same block as a FUNCTION body gives rc 1 for `return 1` and rc 0 for `return 0`.
   - E2 (clean -> rc 0) does work, and a return made unconditional WOULD red it. That is the arm Wednesday named; the gate must re-prove it (TAMPER-UNCONDITIONAL-RETURN-1348).
   - The fix itself reads right. What the finding weakens is the red proof's claim.
2. **MKTEMP-GNU-1348** (READ, a prediction).
   - Test :124 runs `mktemp -t ks1054_summary_drive`, with no X's. BSD mktemp accepts a prefix. GNU coreutils refuses a template without ≥3 trailing X's.
   - The shell suites run on `ubuntu-latest` (pr-security-gates.yml:44/:100, security-scan.yml:495).
   - Predicted on CI: TMPDRV is empty, then `bash ""` gives rc 127, so **E2 reds** and E1 is green for the wrong reason.
   - `run-shell-suites.sh:255/:267` uses XXXXXX templates itself.
   - The drafter could not run GNU mktemp: the only local image is node:24-alpine, which has busybox mktemp, and no image was pulled. The gate measures.
3. **BEHAVIOUR-WIDER-THAN-MIGRATIONS-1348** (READ).
   - `verify_deployment` counts FOUR conditions:
     - a portal serving the default nginx page;
     - `/health` without `"healthy"`;
     - startup migrations failed;
     - the demo login failing.
   - The `return 1` now fails deploy.sh on all four, where before it exited 0 on all four.
   - The subject says "counts issues", which is true of the code. The PR body and Kam's ruling frame migrations.
   - Wednesday's R2-A said "exactly as deploy-all.sh does", and deploy-all.sh fails on ANY smoke FAIL. The gate rules on it.
4. **SUBJECT-TRUE-OF-DIFF-1347** (READ).
   - The live title, `KS-1374: raise the local templates and make the Akto harness read the platform limit`, was written for round 1. At round 2 `.env.example` is back at 2000, so ONE template is raised. The harness reads the variable only for a local target.
   - The drafter declared a PROPOSAL instead: `KS-1374: env.example goes to 10000 and Akto reads the limit only for a local target` (83 -> 91).
   - The gate rules whether it is true. The override is read for any target, and see doubt 5.
   - If the proposal is not true, the gate writes one that is. #1348's declared subject is its title, and it is true only if deploy.sh itself exits non-zero (REQUIREMENT 5).
5. **OVERRIDE-APP-URL-1347** (READ).
   - `isLocalScanTarget()` keys on `SECUURA_API_URL`.
   - `systemTest/akto/.env.example:122` says `OVERRIDE_APP_URL` overrides "the target URL sent to akto-testing".
   - If the engine can hit a remote host while `SECUURA_API_URL` is local or unset, then N-1347-1 is narrowed, not closed.
6. **DOTENV-ORDER-TARGET-1347** (READ). Round 2 adds a second call-time read, `SECUURA_API_URL`, which usually lives in the akto `.env`, not the shell.
   - A module-scope call in a worker before `loadEnvFiles` would read the target as UNSET, which counts as local.
   - A shell-exported 10000 would then pace a demo scan at 7500.
   - The gate measures this with a scratch vitest config.
7. **Cell R7** (READ). Its title says "the override NAME is not one either env template defines". Its body at :213 compares the constant to a string. Whether it reads any template is for the gate.
8. **SECOND-CORRECTION-LINES-1347** (READ; linear_gate45.md, comment `dc9212b5`, 10:59:09Z, BODY_SHA256 `a15971d19ae5…`).
   - It says "a demo scan (limit 2000)" and also "The demo's own limit was not read at any point".
   - The other lines (production compose :16/:105, bootstrap-env canonical, floor at 1, CI at 10000, the tunnel caveat) are for the gate's table.
9. **PR-BODY-STALE-1347** (READ). gh_body_1347.md keeps round 1's Part B above the ROUND 2 section: "Both templates get the edit", "`env.example` and `.env.example` set … 10000", "the compose fallback … untouched", "Touched: 5 files".
   - The squash body is composed, so this does not reach develop. It is a client-readable PR surface.
10. **N-1347-5 / -7 / -8 carry over** (READ).
    - The FIRST correction's line-9 overclaim is not addressed by the second correction.
    - Round 2's body repeats the "0 passed AND 0 failed" load-failure wording for R-cells at round 1, which gate44 measured as N failed / 1 passed for the analogous case.
    - `AND-0` is still in the body.
11. **`env.example:189-198`** (READ) still says "Harnesses read this same variable … aktoRateLimit.ts". Since round 2 that is true only for a local target.
12. **`docker-compose.yml:497`'s new comment** (READ) says "…including the demo VM", which the repo cannot show.
13. **NAMED-NOT-FIXED-1348** (READ). Wednesday's GO asked for N-1346-2/-3 "if they are one-line … else name them in the handover". The seat named N-1346-2/-3/-4 as not fixed.
    - The gate GRADES this and does not require the fixes.
    - It also checks every line of the KS-1054 raise comment `b82bebb3`.
14. GitHub reports `mergeable_state: unstable` on both PRs: CI does not start on this account. Both push preflights read 12/15 legs, with legs 3, 4 and 8 skipped.

## 3. Pins and what the gate owes
- The prompt `2026-09-29_secuura-batch1348.prompt.txt` (41845 bytes, sha256 `e2197f964f8c…`) carries Wednesday's requirements by 53 keywords (fill_gate45.py `KW`). The launcher refuses a prompt that is missing any of the following:
  - a keyword (exit 33);
  - the tickets (32) or the tier lines, including "a DEPLOY-PATH change", "KS-1374 ROUND 2 OF 2" and "a NO GO on #1347 ships NOTHING" (7);
  - the HOLDS, including "No `az` command of any kind", "You NEVER reply to Peter" and "Never read or write a real `.env`" (39);
  - the GO (26);
  - the addendum rules, **REPORT-HASH-LAST** and "EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF" (25);
  - the verdict subject or the report dir (23);
  - develop / END_TREE in full (31);
  - the capture, the Linear read (which must contain `dc9212b5`), the commission, the drafter probe, or gate44's report path (8).
- **REPORT-HASH-LAST**: `## MERGE ADDENDUM` is the LAST thing written to report.md, and nothing goes into report.md after the verdict mail. Late evidence goes to `evidence/late_<HHMMSS>.md`. The mail body carries `sha256 report.md = <hex>`. Controls L13b and L13c prove the launcher refuses a prompt that drops these rules.
- The requirements, by name:
  1. #1348:
     - E1 red at base (13/1, E1 alone) and 14/0 at head;
     - **E2 re-proved on the block AND the real function**;
     - the unconditional-return tamper must red E2;
     - `return 0`;
     - GNU mktemp;
     - the pre-existing arms.
  2. #1347:
     - red-first against ROUND 1 for N-1347-1 (7500 -> 1500) and N-1347-3 (0 -> 1), with a round-1-compatible probe;
     - **through the REAL loader, a non-local target with a raised local .env paces ≤ 1500 and a local one 7500**, with the round-1 row as the control;
     - the host forms;
     - OVERRIDE_APP_URL;
     - the target read's dotenv order;
     - tampers on R1, R5, R6 and R9;
     - the override name absent.
  3. **Every gate44 finding N-1347-1…10 as a row** (CLOSED / NARROWED / OPEN), with evidence. This includes the CI-test-assumes-2000 check (Wednesday ruled CI stacks in scope).
  4. Whole suites before and after, with tsc: shell, api-gateway, and akto unit with its OWN `npm ci`, at develop, round 1 (akto), each head and END.
  5. The 41-file census, classified and RUN.
  6. Subjects that are TRUE of the diff, and bodies.
  7. #1348 on the deploy path with STUBS, covering:
     - `verify`, `services` and `full`;
     - every call site under `set -e`;
     - the ERR trap line;
     - all four ERRORS conditions;
     - both scripts side by side.
  8. Order, END and clean merge.
  9. The second correction, line by line, the stale PR body, and the last-round cap.
- Launcher `launch_qa_secuura_batch1348.sh` (12814 bytes, sha256 `2e03220e4af4…`).
- Capture `mail_gate45_ready.md` (39302 bytes, sha256 `8abe62c92376…`): nine mails, 10 head checks, 0 problems (capture_1.out).
- Linear read `linear_gate45.md` (19013 bytes, sha256 `7b5ff79c7304…`): `LINEAR READ OK: 2 CORRECTION comment(s) on KS-1374, the SECOND dc9212b5-aaec-42fc-9733-ba57737d5ae0`.
- COMMISSION.md (filled).

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, after line 152 (`QA/Secuura-batch1346…`, currently the last line). Back up the file first:
```
QA/Secuura-batch1348|coagent@agentmail.to|yes
```
Until the line is present, the launch action's step 0 refuses with rc 1. Control R1 measures that refusal on an empty routing file. R8 shows the same run with the line present passing step 0 and stopping at 3b. The dry run found no other refusal.

## 5. Controls: `controls_gate45.sh <scratchpad> [--invert]`
- **PN0-PN7 + PNZ, pin_gate45.py:**
  - PN0: the real subject as a simulation (PASS, 0 overlapping, END and REVERSE `9222b67ef203…`, MODE SUMMARY 2 OK, and the #1347 move reaches NONE of its paths).
  - PN1: a head it was not given refuses and names #1347.
  - PN2: a PLANTED OVERLAP, a synthetic #1347 appending to deploy.sh. It prints `OVERLAP #1348 x #1347`, and the chain step refuses on the blob.
  - PN3: a planted CONFLICT at the exact line #1348 inserts after (`step #1347 NOT clean`).
  - PN4: a #1347 stand-in touching deploy-all.sh, a path the #1346 move touched (`(C) #1347: the develop move touches its own path`).
  - **PN6**: deploy.sh RECORDED 100644, so `MODE MISMATCH`.
  - **PN7**: the test file RECORDED 100755, so `MODE MISMATCH`.
  - PNZ: the real pins are sha256-unchanged.
- **TR0-TR5, testrefs_gate45.py:**
  - the real census (41, PASS);
  - the census at develop does not list the ks1374 akto file;
  - a census pointed at nothing FAILS CT-POS;
  - CT-KNOWN;
  - BASENAME finds deploy.sh (1) where PATH finds 0;
  - CT-POS #1347 finds 2 of 2.
- **KS0-KS9, keyscan_gate45.py:**
  - a `(#n)` suffix;
  - a foreign key in a subject;
  - #1347's subject **plus two characters** (`declared 85, lands at 93`);
  - a missing `Refs KS-1054`;
  - `Closes`;
  - a foreign `KS-206` in a body;
  - a FLAG on a planted PR body (`KS-1332`);
  - KS8: the stale live title PASSES the key scan, so the scan cannot judge truth;
  - KS9: `title == declared: False` prints for #1347.
- **L0-L17, the launcher** (exit code in brackets):
  - wrong head (6), moved develop (17), wrong compare paths (10), a foreign-seat GO (26), an unfilled token (8), a dropped keyword `TAMPER-RETURN-0-1348` (33), a capture without #1347's head (20);
  - three dropped HOLDs (39, 39, 39);
  - the real launch path non-TTY (21);
  - develop not in full (31);
  - a tier line (7) and the round-2 cap line (7);
  - a ticket line (32);
  - the addendum MG-1 rule (25), REPORT-HASH-LAST (25), the TRUE-OF-THE-DIFF rule (25);
  - the verdict subject (23);
  - a MOVED KIT (2);
  - the Linear read not named (8), the drafter probe not named (8).
- **R0-R8, the launch action** (exit code in brackets):
  - the dry run (0) and its census line;
  - a real run without the routing line (1);
  - a kit-path overlap via G45_OVERLAP_EXTRA=package-lock.json against the real open PRs (15, #572);
  - a title-key overlap via G45_TITLE_KEY=KS-1297 (15, names #1253);
  - DISJOINT OUT-OF-KIT made to print via G45_WIDEN_RX on the real dependabot PRs (0);
  - a stale head pin (11), a moved develop (10), a bad scratchpad (9);
  - a real run with a routed temp file that stops at 3b (0).
- **Not controlled:**
  - on a real launch: the usage gate (5), `cockpit.sh add` (7) and the override refusal (4);
  - a `mergeable=False` refusal;
  - the REAL re-pin across a develop move (only the dry run's rc 10 is controlled).
- **Side effects, kept:**
  - R1 / R8 wrote `launch_<HHMMSS>.*` step outputs into this kit: 1118/1119 from controls_1, 1123/1125 from controls_2.
  - TR1 wrote `testrefs_gate45.8ba2da02d980.json`.
  - The PN simulations wrote `pins_gate45.SIM-{real,ovl,cfl,mov,m644,m755}.json`.

## 6. Could not measure
- The drafter ran no suite, tsc, eslint, install, deploy-script drive or runtime probe. The one exception is the return probe (drafter_return_probe.out), which runs deploy.sh's extracted summary block under /bin/bash 3.2.57.
- The following figures are the seat's claims, not the drafter's measurements:
  - 14/0 and 13/1 red-first (E1 alone);
  - akto 93/1643 -> 93/1654;
  - the api-gateway cell 7/7;
  - tsc 0;
  - eslint 0 with its control;
  - the round-1 red-first quotes `expected 7500 to be less than or equal to 1500` and `expected 0 to be greater than 0`.
- Not measured, and each is a gate item:
  - GNU mktemp (doubt 2);
  - OVERRIDE_APP_URL (doubt 5);
  - the target dotenv order (doubt 6);
  - bash 5's top-level `return` status;
  - the live demo's real limit (off-repo).

## 7. Files
- Config: kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md
- Pins: pin_gate45.py -> pin_1.out (+ .rc), pins_gate45.json (+ .SIM-*.json from controls) · final_lsremote_1.out
- Reads:
  - gh_read_gate45.py -> gh_read_1.out, gh_read_1.json, gh_body_1348.md, gh_body_1347.md
  - linear_read_gate45.py -> linear_read_1.out (+ .rc), linear_gate45.md
  - _mail_list_gate45.py -> _mail_list_1.out
- Checks: testrefs_gate45.py -> testrefs_1.out (+ .rc), testrefs_gate45.json · keyscan_gate45.py -> keyscan_1.out (+ .rc) · drafter_return_probe.out
- Capture: capture_mail_gate45.py -> capture_1.out (+ .rc), mail_gate45_ready.md
- Prompt and launcher: prompt_gate45.TEMPLATE.txt and launcher_gate45.TEMPLATE.sh.txt. fill_gate45.py fills them into 2026-09-29_secuura-batch1348.prompt.txt, launch_qa_secuura_batch1348.sh and COMMISSION.md (fill_1.out). Then launcher_check_1.out (+ .rc).
- Launch: repin_and_launch_gate45.sh -> repin_dryrun_1.out (+ .rc) · launch_<HHMMSS>.* (written by controls R1 / R8)
- Controls: controls_gate45.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt

## 8. The ONE launch command (after the routing line, §4)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate45/repin_and_launch_gate45.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate45/launch_qa_secuura_batch1348.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/35f90900-da39-4310-a097-bf496fc89a5b/scratchpad
```
- For a dry run, append `--dry-run`. repin_dryrun_1.out is one, rc 0.
- Argument 2 may be ANY existing Claude session scratchpad (`/private/tmp/claude-501/*/scratchpad*`). If `g45_sp/clone` is absent there, pin_gate45.py rebuilds it on a re-pin.
- If develop moves, the launch re-pins in the same action (step 3b: pin, then testrefs, then fill; the re-pin re-asserts the recorded modes).
  - It refuses rc 10 if the move reaches either PR's own paths, if a chain step is unclean, or if a mode pin fails.
  - A moved head refuses rc 11.
  - Any other open PR touching one of the 8 paths, or titled with a kit key, refuses rc 15.
- Final re-read of the heads, final_lsremote_1.out (2026-09-29T11:26:00Z): develop `8ba2da02d980`, pull heads #1348 `1bb58b4ebb97` and #1347 `18bc5123ce90`, each equal to its branch. Every pin is still current: **True**.
