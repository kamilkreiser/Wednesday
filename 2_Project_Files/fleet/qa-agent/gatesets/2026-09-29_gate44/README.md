# Gateset 2026-09-29_gate44 — README for Wednesday

Written 2026-09-29T09:43Z by the drafter (times from `date -u`). Every figure below is read from the kit's own output files, each named beside it.
The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory (text files only) and scratch under its session scratchpad `g44_sp/`: `clone` (a `git clone --shared --no-checkout` of Wednesday's `screen0929/base` clone, fetched from origin ONLY there with the Secuura deploy key), the synthetic control commits (made by plumbing in that clone) and the control plants under `controls_<HHMMSS>/`. It did NOT write the routing line (§4).
The Secuura checkout was touched by read verbs only (`ls-remote` in the launcher, the repin and the final read). GitHub: REST GET only (gh_read_1.out / gh_read_1.json, gh_body_<n>.md; the launcher's compares; the repin's PULLS reads). Linear: ONE read-only GraphQL `issue` query per key, KS-1054 and KS-1374 (linear_read_gate44.py, no mutation in the file). AgentMail: ONE read-only listing of wednesday-agent@ (_mail_list_1.out) and seven by-id GETs (capture_mail_gate44.py); no seen-state touched, nothing sent. No npm install, suite, tsc, eslint or deploy-script run by the drafter (§6).

**gate44 = TWO PRs from Seat B 45th, who is also the MERGER. T1: #1346 (a DEPLOY-PATH change, full weight). T2: #1347 (through-code). Merge order 1346, then 1347, each squash on the previous tip. Both merge cleanly AS-IS. #1346 does NOT need a rebase.**

| PR | ticket | tier | head (ls-remote pull/head == branch == API == fetched) | parent | behind develop | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1346 | KS-1054 (N-1332-5) | T1 | `2075c3ec70789d9a87a6359fccf1a58d97db3255` | `0aa9b52c691b` | **5** | 4 | 79 -> 87 |
| #1347 | KS-1374 (A+B+C) | T2 | `2c4b98253b1fa820c4fe08585dad5da57947ffb4` | `bd740147c3d8` | 0 | 5 | 84 -> **92** |

Pane `QA/Secuura-batch1346` (**NOT routed by the drafter**, see §4). GO string, as the GO mail's SUBJECT: `GO (Seat B 45th): merge 1346 1347 on gate44`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-29-batch1346-g44/`. Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE44 batch #1346 #1347 (Seat B45, round 44; T1: KS-1054 deploy scripts read startupMigrations; T2: KS-1374 local limit + Akto reads it)`.

## 1. BLUF
- **Kit: READY to launch once the routing line is added (§4).**
  - Launcher `--check` rc 0 (launcher_check_1.out: `all guards pass:`): 2 of 2 heads at the branch AND at pull/head, 2 of 2 GitHub compares equal the pins, and 40 by-name keywords present.
  - Repin `--dry-run` rc 0 (repin_dryrun_1.out: `DRY RUN COMPLETE 2026-09-29T09:43:28Z`). It printed `BOTH INSTRUMENTS AGREE with the pin, 2 of 2` and the census line `20 other open PR(s) read | 0 touch a kit path or carry a kit key`. The only thing it reported was that the routing line is absent, which is the one thing the real run would refuse on.
- **Pins** (pin_1.out, rc 0, ls-remote at 2026-09-29T09:22:49Z): develop is `bd740147c3d88fbf45af109fd68fd35f602c2914`, which equals the commission's develop. Each head equals its branch, the PULLS API head (gh_read_1.out) and the fetched ref.
- **#1346 is FIVE commits behind, not two** (pin (B): `ahead 1 behind 5`). The commission said two. The five commits are gate43's squashes #1341-#1345, `0aa9b52c691b..bd740147c3d8`, touching 11 paths. Pin (C) found `reaches its own paths: NONE`. So "main moved", but not in a way that reaches its cells, and **no rebase is needed**. Evidence that it merges cleanly AS-IS:
  - pin (E): merge-tree rc 0, alone tree `fd0d6bc033a9…`;
  - pin (F): the first chain step is clean, `diff(tip, new) == own paths: True`, `blobs+modes == head: True`;
  - GitHub also reports `mergeable: True` for #1346.
- **END_TREE `0c16f76bd6ccffb38130966e428f47ba2e8da82d`** (pin (F)/(G)).
  - Chain 1346 -> 1347: both steps clean.
  - `diff(develop, END)` is exactly the union of the 9 own paths, and every END blob and mode equals its head's: `9 files changed, 501 insertions(+), 14 deletions(-)`.
  - Reverse order gives the same tree: True.
  - Overlap: `1 pair(s) checked, 0 overlapping | 9 path(s) in total, 9 distinct`.
- **Recorded modes** (pin (H), `git ls-tree`; `core.filemode` is false, so the disk bit proves nothing): the helper `check-startup-migrations.sh` is **100755** at head, alone tree, chain step and END. The same holds for deploy-all.sh and deploy.sh. The control is the test file in the same commit, **100644** at all four. `MODE SUMMARY: 4 path(s) pinned, 4 OK | pins seen: ['100644', '100755']`.
- **Controls, both ways** (controls_gate44.sh, one unedited script, sha256 `1703af86a6f7…` before the first run and after the second, controls_sha.txt):
  - normal (controls_1.out, rc 0): `SUMMARY gate44: 58 controls, OK 58, MISMATCH 0`
  - `--invert` (controls_2.out, rc 1): `SUMMARY gate44: 58 controls, OK 0, MISMATCH 58` (every control can fail).
- **Test census** (testrefs_1.out, rc 0, `git grep` at END over Blockchain/** AND systemTest/**): **18 test files**.
  - A BASENAME class was needed. The new ks1054 shell suite reaches deploy-all.sh only as `"$AZ/deploy-all.sh"`, so the PATH spelling finds 0 and BASENAME finds 2.
  - Controls: CT-POS for both PRs, CT-NEG, CT-TREE (3 of 3 new test files are absent at develop), and CT-KNOWN (`bootstrap_env_canonical_template.test.sh` is listed).
  - #1347's api-gateway test reads `index.ts` and `docker-compose.yml`, and neither is a changed path. It is printed as `OWN-TEST-NO-CHANGED-PATH`, and the gate runs it anyway.
- **Key scan** (keyscan_1.out, rc 0): `KEYSCAN PASS: 12 checks over 2 PRs, 0 FAIL, 0 FLAG line(s)`.
  - Each title equals its declared subject, and the only key in it is the PR's own. No subject carries `(#n)`.
  - Landed lengths are 87 and **92**. #1347 is on the limit: legal, but control KS3 shows that one more character fails at 93.
  - Mandated bodies are `Refs KS-1054` and `Refs KS-1374`. No foreign hyphenated key appears on any live surface.
- **Heads re-read at the end**: final_lsremote_1.out (2026-09-29T09:44:52Z). Every pin is still current: True.

## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated; every one is in the prompt as a by-name item the gate must RULE)
1. **BEHIND-5-NOT-2** (MEASURED, above).
2. **DEPLOY-SH-EXIT-CODE-1346 — deploy.sh probably still exits 0 over failed migrations** (READ, prediction).
   - At the head, `verify_deployment()` only `log_error`s and increments `ERRORS`. Its last command is `log_error`, an `echo`, so it never returns non-zero. Neither `deploy_services` nor the `verify` / `full` case branches test its result.
   - deploy.sh therefore prints "startup migrations FAILED" and "found N issue(s)" and would exit 0. That is the same strength as the pre-existing `"healthy"` grep Kam named at deploy.sh:823.
   - deploy-all.sh does fail: it runs `smoke_test`, and then `exit 1` when `FAIL > 0`.
   - The PR title says "fail on failures", and Kam's ruling says "the deploy reads as failed". The gate drives `deploy.sh -e dev verify` with stubs and rules on it.
3. **RAN-FALSE-1346** (READ).
   - The gateway's own `startupMigrationStatus.ts` at develop says "`ran: false` … is NOT the same as a clean run". `runStartupMigrations()` returns that state when DATABASE_URL is unset.
   - The predicate ignores `ran`, so `{ran:false, failed:0}` prints "✓ startupMigrations: 0 failed" and passes.
4. **PASS-LINE-ON-SKIP-1346** (READ). For an ABSENT, non-JSON or empty body the predicate exits 0, and deploy-all.sh then records `✓ Startup migrations` as a PASS. That is a verdict composed separately from the work (the STANDING_LINES verdict-line class). The ABSENT warning is printed above it.
5. **Predicate edges** (READ):
   - `startupMigrations` with `failed` null or missing reads as ABSENT and passes.
   - A Python bool is an int, so `failed: true` fails with "True migration(s)".
   - With python3 missing from PATH, `|| echo UNPARSEABLE` would report "not JSON … SKIPPED" and pass.
   - The gate measures each one.
6. **W1-GREEN-AT-BASE-1347** (READ, and the author says the same): the api-gateway cell titled `RED KS-1374 W1` is green at develop, because `index.ts:474` already reads `RATE_LIMIT_MAX_REQUESTS`. The file is a PIN with no red half.
7. **LOWER-LIMIT-1-UNPACED-1347** (READ, not measured). RATE_LIMIT_MAX_REQUESTS=1 is a positive safe integer, so `platformRequestsPerMinute()` returns 1 and `derivedRateLimit()` returns floor(0.75) = 0. `tierPacing.ts` says "0 means unthrottled". That falsifies "never paces faster" / "a LOWER limit is honoured" at one value.
8. **PROD-COMPOSE-TEMPLATE-1347** (READ).
   - `docker-compose.production.yml:16` says "Copy .env.example to .env", and its gateway reads `${RATE_LIMIT_MAX_REQUESTS:-100}` (line 105).
   - At the head, `.env.example` carries 10000. A production-compose host seeded fresh from the template would therefore run at 10000, not 100.
   - The CORRECTION says "Demo and production limits are unchanged". The PR body says "No platform runtime change".
9. **CI-TEMPLATE-1347** (READ): `.github/workflows/internal-audit.yml:94` runs `cp env.example .env`, and the old comment said 2000 "Applies to local + CI". The `docker-compose.yml:497` comment "(default aligns with env.example)" is now stale, and #1347 does not touch it.
10. **DOTENV-ORDER-1347** (the author's own NOT COVERED item; READ, so the gate knows where to measure).
    - `loadEnvFiles` runs only inside `loadConfig()`.
    - In the integration config, globalSetup `limiterSettleSetup` (which calls `loadConfig()`) runs before `tierPacingSetup` in the MAIN process.
    - `tests/securityWorkflows.test.ts:63-64` calls `pacedBudgetMs()` at MODULE SCOPE in a WORKER.
    - Whether the worker sees the dotenv value is the open question. The prompt asks the gate to measure it with a scratch vitest config.
    - The loader also reads the LOCAL `Blockchain/Dev/.env` whatever stack the scan targets.
11. **CORRECTION-LINES-1347** (READ; linear_gate44.md, KS-1374 comment `4c4b7ea6…`, 09:12:03Z, BODY_SHA256 `dd920bb5efbe…`).
    - The drafter verified two line claims:
      - `aktoRateLimit.ts:60` at develop is `export const PLATFORM_REQUESTS_PER_MINUTE = 2000;`. TRUE.
      - `systemTest/schemathesis/scripts/runner/config.py:234` is `raw = int(os.environ.get("RATE_LIMIT_MAX_REQUESTS", …))`. TRUE.
    - Three claims need a ruling:
      - "the demo … runs that compose file with its own .env" cannot be verified from the repo.
      - "Demo and production limits are unchanged" is contradicted by doubt 8 for a fresh production-compose seed.
      - "one api-gateway test pins the global limiter" is true only as text plus an own instance.
    - The gate tables every line.
12. **PETER-0914-1347** (READ): Peter (client) commented on KS-1374 at **09:14:01Z**, two minutes AFTER the correction and after #1347 was raised:
    > "I added this yesterday as a temporary fix, as I did not want to update the codebase · systemTest/akto/src/setup/aktoRateLimit.ts:60"

    - That line was introduced by `4f7766a3e` (KS-1286, 2026-09-28).
    - #1347 Part C replaces the hard-coded pacing it describes.
    - **This is new client input that postdates the PR, and Wednesday should see it before the GO, whatever the gate rules.** The gate is held: `You NEVER reply to Peter`.
13. Linear side effect disclosed by the author: KS-1374 moved Todo -> In Progress through branch automation. It is not gate business.
14. GitHub `mergeable_state: unstable` on both PRs (CI does not start on this account). Both push preflights read 12/15 legs (3, 4 and 8 skipped).

## 3. Pins and what the gate owes
- The prompt `2026-09-29_secuura-batch1346.prompt.txt` (33549 bytes, sha256 `2e625c5333aa…`) carries Wednesday's requirements by 40 keywords (fill_gate44.py `KW`). The launcher refuses a prompt that is missing any of the following:
  - a keyword (exit 33);
  - the tickets (32) or a tier line, including "a DEPLOY-PATH change" (7);
  - the HOLDS, including "No `az` command of any kind" and "You NEVER reply to Peter" (39);
  - the GO (26);
  - the addendum and **REPORT-HASH-LAST** rules (25);
  - the verdict subject or the report dir (23);
  - develop / END_TREE in full (31);
  - the Linear read, the capture or the commission by path (8).
- **REPORT-HASH-LAST (the gate43 lesson)**: `## MERGE ADDENDUM` is the LAST thing written to report.md, and nothing goes into report.md after the verdict mail. Late evidence goes to `evidence/late_<HHMMSS>.md`, and the mail body carries `sha256 report.md = <hex>`. Controls L13 and L13b prove the launcher refuses a prompt without these rules.
- The requirements, by name:
  1. red at base, green at head and right-reason tampers per PR. For #1346 this includes TAMPER-MODE-100644-1346 (a RECORDED 100644 helper, checked out fresh) and TAMPER-KEY-ON-ERROR-1346. For #1347 it includes a develop-compatible akto probe.
  2. whole suites before and after: the shell suite (`run-shell-suites.sh`), api-gateway, and the akto unit suite with its OWN `npm ci`, each with tsc.
  3. every census file RUN.
  4. subjects and bodies.
  5. #1346 on the deploy path, driven with STUB az/curl/docker/sleep, never a real environment.
  6. overlap, chain, END, and rebase-or-not.
  7. the #1347 through-code items (i)-(vi).
- Launcher `launch_qa_secuura_batch1346.sh` (11840 bytes, sha256 `6cdca10b8ab0…`).
- Capture `mail_gate44_ready.md` (90969 bytes, sha256 `7c0ae7fde14b…`) holds seven mails with 8 head checks and 0 problems:
  - Seat B 45th's READY for both PRs, its STATUS raising #1346, and its STATUS holding for gate44;
  - Wednesday's ANSWER to the READY and the LAUNCH BRIEF to Seat B 45th;
  - Tuesday's two ROUTED copies of Kam's KS-1374 instruction.
- Linear read `linear_gate44.md` (12249 bytes, sha256 `d2b718b581d2…`).
- COMMISSION.md (filled).

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, after line 150 (`QA/Secuura-batch1341…`). Back up the file first:
```
QA/Secuura-batch1346|coagent@agentmail.to|yes
```
Until the line is present, the launch action's step 0 refuses with rc 1. Control R1 measures that refusal on an empty routing file, and R8 shows the same run with the line present passing step 0 and stopping at 3b. The dry run found no other refusal.

## 5. Controls: `controls_gate44.sh <scratchpad> [--invert]`
- **PN0-PN7 + PNZ, pin_gate44.py:**
  - PN0: the real subject as a simulation (PASS, 0 overlapping, END and REVERSE `0c16f76bd6cc…`, MODE SUMMARY 4 OK).
  - PN1: a head it was not given refuses and names #1347.
  - PN2: a PLANTED OVERLAP, a synthetic #1347 head appending to #1346's deploy.sh. It prints `OVERLAP #1346 x #1347`, and the chain refuses on the blob.
  - PN3: a planted CONFLICT at the exact insertion point #1346 uses in deploy-all.sh (`step #1347 NOT clean`).
  - PN4: a #1346 stand-in touching a path the gate43 move touched (`(C) #1346: the develop move touches its own path`).
  - **PN6**: the helper RECORDED 100644, so `MODE MISMATCH` (want 100755).
  - **PN7**: the test file RECORDED 100755, so `MODE MISMATCH` (want 100644). This is the other direction.
  - PNZ: the real pins are sha256-unchanged afterwards.
- **TR0-TR5, testrefs_gate44.py:** the real census (18 files, PASS). The census at develop does not list the ks1054 suite. A census pointed at nothing must FAIL CT-POS. CT-KNOWN holds. The BASENAME class finds deploy-all.sh (2) where PATH finds 0. The OWN-TEST-NO-CHANGED-PATH line prints.
- **KS0-KS7, keyscan_gate44.py:** a `(#n)` suffix; a foreign key in a subject; #1347's subject **plus one character** (`declared 85, lands at 93`); a missing `Refs KS-1054`; `Closes`; a foreign `KS-206` in a body; and a FLAG that must print on a planted PR body (`KS-1332`).
- **L0-L16, the launcher** (exit code in brackets): wrong head (6), moved develop (17), wrong compare paths (10), a foreign-seat GO (26), an unfilled token (8), a dropped keyword (33), a capture without #1347's head (20), two dropped HOLDs (39, 39), the real launch path non-TTY (21), develop not in full (31), a tier line (7), a ticket line (32), the addendum MG-1 rule (25), **the REPORT-HASH-LAST rule (25)**, the verdict subject (23), a MOVED KIT (2), a prompt not naming the Linear read (8).
- **R0-R8, the launch action** (exit code in brackets):
  - the dry run (0) and its census line;
  - a real run without the routing line (1);
  - a kit-path overlap via G44_OVERLAP_EXTRA against the real open PRs (15);
  - a title-key overlap via G44_TITLE_KEY=KS-1297 (15, names #1253);
  - the DISJOINT OUT-OF-KIT line made to print via G44_WIDEN_RX on the real dependabot PRs (0);
  - a stale head pin (11), a moved develop (10), a bad scratchpad (9);
  - a real run with a routed temp file stopping at 3b (0).
- **Not controlled:**
  - on a real launch: the usage gate (5), `cockpit.sh add` (7) and the override refusal (4);
  - a `mergeable=False` refusal;
  - the REAL re-pin across a develop move. Step 3b rewrites the kit's own files, so only the dry run's rc 10 refusal is controlled.
- **Side effects, kept:**
  - The R1 / R8 real runs wrote `launch_<HHMMSS>.*` step outputs into this kit: 0935/0938 from controls_1, 0941/0942 from controls_2.
  - TR1 wrote `testrefs_gate44.bd740147c3d8.json`.
  - The PN simulations wrote `pins_gate44.SIM-{real,ovl,cfl,mov,m644,m755}.json`.

## 6. Could not measure
The drafter ran no suite, tsc, eslint, install, deploy-script drive or runtime probe. Every red / green / suite / tsc figure in the commit messages, PR bodies and READY mail is the seat's claim. That includes:
- the 0/11 -> 11/0 shell figures;
- api-gateway 90/805 -> 91/812;
- akto unit 92/1632 -> 93/1643;
- the six Part A arms and the develop probe.

The following were not measured, and each is a gate item:
- deploy.sh's exit code (doubt 2);
- the dotenv/worker order (doubt 10);
- the RATE_LIMIT_MAX_REQUESTS=1 case (doubt 7);
- which compose file the live demo runs, and its real limit (off-repo).

## 7. Files
- Config: kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md
- Pins: pin_gate44.py -> pin_1.out (+ .rc), pins_gate44.json (+ .SIM-*.json from controls) · final_lsremote_1.out
- Reads: gh_read_gate44.py -> gh_read_1.out, gh_read_1.json, gh_body_1346.md, gh_body_1347.md · linear_read_gate44.py -> linear_read_1.out (+ .rc), linear_gate44.md · _mail_list_gate44.py -> _mail_list_1.out
- Checks: testrefs_gate44.py -> testrefs_1.out (+ .rc), testrefs_gate44.json · keyscan_gate44.py -> keyscan_1.out (+ .rc)
- Capture: capture_mail_gate44.py -> capture_1.out (+ .rc), mail_gate44_ready.md
- Prompt and launcher: prompt_gate44.TEMPLATE.txt, launcher_gate44.TEMPLATE.sh.txt, fill_gate44.py -> 2026-09-29_secuura-batch1346.prompt.txt + launch_qa_secuura_batch1346.sh + COMMISSION.md (fill_1.out), launcher_check_1.out (+ .rc)
- Launch: repin_and_launch_gate44.sh -> repin_dryrun_1.out (+ .rc) · launch_<HHMMSS>.* (written by controls R1 / R8)
- Controls: controls_gate44.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt

## 8. The ONE launch command (after the routing line, §4)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate44/repin_and_launch_gate44.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate44/launch_qa_secuura_batch1346.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/35f90900-da39-4310-a097-bf496fc89a5b/scratchpad
```
- For a dry run, append `--dry-run` (repin_dryrun_1.out is one, rc 0). Argument 2 may be ANY existing Claude session scratchpad (`/private/tmp/claude-501/*/scratchpad*`). If `g44_sp/clone` is absent there, pin_gate44.py rebuilds it on a re-pin.
- If develop moves, the launch re-pins in the same action (step 3b: pin, then testrefs, then fill; the re-pin re-asserts the recorded modes).
  - It refuses rc 10 if the move reaches either PR's own paths, if a chain step is unclean, or if a mode pin fails.
  - A moved head refuses rc 11.
  - Any other open PR touching one of the 9 paths, or titled with a kit key, refuses rc 15.
- Final re-read of the heads, final_lsremote_1.out (2026-09-29T09:44:52Z): develop `bd740147c3d8`, pull heads #1346 `2075c3ec7078` and #1347 `2c4b98253b1f`, each equal to its branch. Every pin is still current: **True**.
