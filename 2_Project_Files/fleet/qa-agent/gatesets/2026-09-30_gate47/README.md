# Gateset 2026-09-30_gate47 — README for Wednesday

Written 2026-09-29T15:23Z by the drafter (times from `date -u`; the kit is dated by AEST, 2026-09-30). Every figure below is read from the kit's own output files, each named beside it.

**What the drafter did and did not do.**
- It launched nothing, added no routing line, sent no mail, tapped no pane, merged / committed / pushed nothing, posted nothing, changed no ticket or PR, and deleted nothing. Superseded outputs were renamed (`superseded_*`, `*_sshdenied*`, `*_pre1351*`, `*_parsebug*`), not removed.
- It wrote this kit directory (text files only) and scratch under its session scratchpad `g47_sp/`:
  - `clone`: a `git clone --shared --no-checkout` of the `407373b1…/screen0929/base` clone, fetched from origin ONLY there with the Secuura deploy key (develop, `refs/pull/1349|1350|1351/head`);
  - the synthetic control commits (plumbing in that clone) and the control plants under `controls_<HHMMSS>/`.
- The Secuura checkout was touched by read verbs only (`ls-remote`; `grep` of `.git/config` for its sshCommand line). The seat's record folder was read only.
- GitHub: REST GET only (gh_read_1.*, gh_body_1349.md / 1350.md; gh_read_overlap_1.out / .json, gh_body_1351.md; the launcher's compares; the repin's PULLS reads).
- Linear: TWO read-only GraphQL `issue` queries, KS-1374 and KS-1054 (linear_read_gate47.py; no mutation in the file).
- AgentMail: ONE read-only listing of wednesday-agent@ (_mail_list_1.out) and eleven by-id GETs (capture_mail_gate47.py). Nothing sent.
- The drafter ran no suite, install, lint or script drive. Its only measurements of subject behaviour are git plumbing (pins, census, merge-tree).

**gate47 = TWO PRs, one batch, authored AND merged by Seat B 46th (pane %74). Order #1349 then #1350; each is ROUND 1 of its own PR.**

| PR | ticket | tier | head (ls-remote pull/head == branch == API == fetched) | parent | behind develop | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1349 | KS-1374 | T2 | `daab8ff3bff564ee89d4e03cb36a9af04d9b4c9e` | `8c810023f9c9` | 1 | 2 | 71 -> 79 (PR title verbatim) |
| #1350 | KS-1054 | T1 | `8f4f0ef1496304cc853532b686e92bb886fa027d` | `a72149a1a803` (= develop) | 0 | 4 | 72 -> 80 (PR title verbatim) |

- Pane `QA/Secuura-batch1349`. **It is NOT routed by the drafter**, see §4.
- GO string, as the GO mail's SUBJECT: `GO (Seat B 46th): merge 1349 1350 on gate47`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-30-batch1349-g47/` (does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE47 #1349 #1350 (Seat B46 author and merger, round 47; T2: KS-1374 pace keyed on the scan target; T1: KS-1054 a skipped migration check stops reading as a pass)`.

## 1. BLUF
- **Kit: NOT READY to launch as it stands. The launch action REFUSES rc 15, correctly, on an out-of-kit PR that opened while the drafter worked:**
  - **#1351** (KS-1386), opened 2026-09-29T14:37:24Z by **PeterObeden**, a client human. Head `eac2dae2afb7`, 2 commits, 297 paths, based on `8c810023f9c9`.
  - It touches `systemTest/akto/src/setup/aktoRateLimit.ts`, a #1349 path (gh_read_overlap_1.out, overlap_probe_1.out, repin_dryrun_1.out rc 15).
  - **Wednesday decides the sequencing, never the drafter.** To launch anyway, add #1351 at its head to kit.json `sequenced_out_of_kit` (EMPTY by drafting; the format is in `sequenced_note`). Then add the routing line (§4).
  - The census honours that entry ONLY while #1351's head equals the one she pinned (control R0w).
- **Everything else passes:**
  - launcher `--check` rc 0 (launcher_check_1.out, and again after the controls: launcher_check_2.out). It confirms 2 of 2 heads at branch AND pull/head, 2 of 2 GitHub compares == the pins, and 51 by-name keywords present as tokens.
  - A repin dry run BEFORE #1351 existed gave rc 0 (repin_dryrun_0_pre1351.out: `DRY RUN COMPLETE`, census 20 other open PRs, 0 touching a kit path). Its only report was the absent routing line.
  - The current dry run (repin_dryrun_1.out) gives **rc 15** on #1351. With a controls-only stand-in for Wednesday's sequencing it reaches `DRY RUN COMPLETE` (control R0s).
- **Pins** (pin_1.out, rc 0; ls-remote 2026-09-29T14:11:11Z):
  - develop `a72149a1a803d802430568254e7fa9afa7029321` = #1348's squash (tree `72b5d2e84e99`), re-read.
  - #1349 is 1 behind. The move `8c810023f9c9..a72149a1a803` touched deploy.sh and the ks1054 test: `reaches its own paths: NONE`. #1350 sits on develop.
  - Overlap #1349 x #1350: 0 of 6 paths. Each PR merges cleanly ALONE (trees `245e8fa4d84e` / `1d27893bf46c`).
  - Chain 1349 -> 1350 clean; REVERSE order gives the same tree. **END_TREE `6930599560c93f3a6cd929cc634b537a2eeb2eaf`** (`6 files changed, 611 insertions(+), 36 deletions(-)`).
- **Recorded modes** (pin (H), at head / alone / chain / END): `MODE SUMMARY: 6 path(s) pinned, 6 OK`. The three #1350 scripts are 100755 and its test is 100644 in the same commit; #1349's two paths are 100644.
- **The hook** (pins (I), (J)): `.githooks/pre-push` `ffc25ebc37d4`, preflight.sh `270b8913c009` and check-package-format.sh are IDENTICAL at develop, both heads and END. #1349 has 0 of 2 paths under Blockchain/Dev/ (the preflight fast-skips); #1350 has 4 of 4 (the control). The preflight has 15 legs (`TOTAL_LEGS=15`, headers `1/15`…`15/15`).
- **Controls, both ways** (controls_gate47.sh, one unedited script, sha256 `87e3d1842063…` before run 1 and after run 2, controls_sha.txt):
  - normal (controls_1.out, **rc 0**): `SUMMARY gate47: 103 controls, OK 103, MISMATCH 0 | ssh-denied retries 0`;
  - `--invert` (controls_2.out, **rc 1**): `103 controls, OK 0, MISMATCH 103`.
- **Test census** (testrefs_1.out, rc 0, at END): **7 test files** — the two own tests; the api-gateway `ks1054-startup-migration-failure-on-health.test.ts` (names deploy-all.sh); and four akto unit tests reaching aktoRateLimit (`aktoContainer`, `aktoRateLimit`, `ks1374-platform-limit-from-env`, `tierPacing`). CT-POS x2, CT-NEG and CT-TREE all OK.
- **Key scan** (keyscan_1.out, rc 0): `KEYSCAN PASS: 12 checks over 2 PRs, 0 FAIL, 0 FLAG line(s)`. Each subject carries only its own key; bodies `Refs KS-1374` / `Refs KS-1054`. KS8 shows that a FALSE subject also passes the scan: truth is the gate's to rule.
- **Heads re-read at the end** (final_lsremote_1.out, 2026-09-29T15:22:30Z): develop `a72149a1a803`, #1349 `daab8ff3bff5`, #1350 `8f4f0ef14963` (pull/head and branch), and #1351 still `eac2dae2afb7`. `every pin still current: True`.

## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated; each is a by-name item the gate must RULE)
1. **OUT-OF-KIT-1351 (MEASURED, overlap_probe_1.out).**
   - Textually, #1351 is clean alone over develop, against each kit head, and over END.
   - It changes aktoRateLimit.ts +11/-8 (the exec runner and the mongoContainer docstring), not isLocalScanTarget's hunk.
   - READ: it also changes `slotDefaultUrl()` to return `''` when no slot is named, and `secuuraUrl` to `env('SECUURA_API_URL') || slotDefaultUrl(…)`. #1349's new docstring ("With BOTH unset … always `http://localhost:<slot port>`") and its CONTROL C3 describe behaviour #1351 removes. A textual merge cannot see this.
   - It moves cited lines: `.env.example` OVERRIDE_APP_URL :123 -> :130, `configuration.md` :424 -> :439.
   - Who merges first is Wednesday's call. Peter is a client human, so nothing is sent to him.
2. **HOOK-LINE-CITE (READ).** The READY and #1349's PR body cite the skip `[ -z "$changed" ] && exit 0` at `.githooks/pre-push:254`. It is `:259` at every tree (blob identical at all four). `:5` is right. This is the wrong-tree line-number class (the shared checkout sits at `3bad652d17cf`).
3. **PR-BODY-CLAIMS, the callers-untouched suite count (READ).** #1350 PR body :32 says "the suite read 36/0 green". The READY says "22 passed / 0 failed", and the seat's own `item3/after-predicate.log` ends `22 passed, 0 failed`. The gate re-creates that state (CALLER-CELLS-1350).
4. **The drafted KS-1374 tick (READ, drafted_texts_gate47.md).**
   - The 7500 figure holds only when the target reads local AND `RATE_LIMIT_MAX_REQUESTS=10000` reaches the harness's env AND the override variable is unset. That is `Math.floor(10000 * 0.75)`; any not-local target gives `Math.floor(2000 * 0.75)` = 1500. The existing checklist line says "a raised local `.env`"; the draft drops that condition.
   - "one tamper arm" is not in the test file. It was the seat's manual run, the same class as gate46's N-1348-7.
   - The draft REPLACES the checklist line's text. The existing line cites `systemTest/akto/src/setup/scanOptions.ts:98` (the file is `src/scan/`) and `.env.example:122` (`:123` at the head).
   - The gate computes the numbers BY RUNNING the code (NUMBERS-FROM-CODE-1349).
5. **The drafted KS-1054 comment (READ).**
   - Its factual anchors check out on read: `a72149a1a803` is #1348's squash (git log: parent `8c810023f9c9`, subject `… (#1348)`), and `b82bebb3` names `1bb58b4ebb97` (linear_gate47.md).
   - It is silent on the one exit-status change in #1350 (python3 absent now FAILS a deploy).
   - "Offline gates green" is true only once gate47 says GO.
   - It calls #1350 an unmerged "follow-up", so posting timing matters (DRAFT-POST-TIMING).
6. **#1350's subject** does not name the python3-absent exit-status change. The gate rules SUBJECT-TRUE-OF-DIFF.
7. **Wednesday's python3 ruling premise (READ).** The ruling says "deploy-all.sh already fails a deploy without python3 (`:299`)". At develop, `:299` / `:331` are `python3 -c … 2>/dev/null || echo ""`, so they cannot abort. The deploy fails via the "Admin login" smoke row's FAIL and the `FAIL>0` exit: true in outcome, but under a row that names the login, not the parser. The gate measures it (PYTHON3-ABSENT-FAILS-CLOSED).
8. **#1349 test C5 comment (READ).** It cites `aktoRateLimit.ts:146-156` for the override block. At the head, `platformRequestsPerMinute()` opens at `:159` (it was `:144` at `8c810023f9c9`; this PR's docstring grew it). A stale reference that lands on develop.
9. **#1349 PR body (READ):** "a malformed URL → NOT local (paces at 2000, never faster)". 2000 is the platform budget; the pace is 1500.
10. **CLASS-ROUND-1349 (READ).**
    - KS-1374 had two gates on #1347 (gate45 = "round 2 of 2"). Its GO shipped #1347 and ticketed N-1347-11; #1349 builds that residue.
    - The rule allows "re-open the class as its own commission later", but says "a third round on the same class needs Kam's word on a card". Same question for #1350 after #1348's round 2 of 2.
    - Carried to the gate and to Wednesday; not fixable by the author.
11. **`return 1` occurs twice in deploy.sh at #1350's head (`:488`, `:904`), and `exit 2` five times in the predicate.** Tamper anchors must be proved unique; the seat's own T4 anchor matched 0 lines and refused.
12. **Carried for ruling, not required:**
    - the kept EMPTY / non-JSON divergence (deploy.sh exits 1, deploy-all.sh now SKIPs; with Kam, gate45 N-1348-3);
    - N-1346-9 out of scope;
    - the `audit:gate` note that `GHSA-v2v4-37r5-5v8g` / `GHSA-mwp4-54f8-5fhr` are no longer reported (baseline cleanup owed; note, not fix);
    - #1349's NOT COVERED list.
13. **Environmental, MEASURED.** GitHub intermittently DENIED the Secuura deploy key's SSH auth under burst load: 3 of 5 `ls-remote` denied at 14:51:57-14:52:10Z (scratch lsr_series.out), then 6 of 6 OK at 5 s spacing at 15:05Z. Two dry runs refused rc 2 on it (repin_dryrun_1a/1b_sshdenied.out), which is fail-closed as intended. The controls harness retries an SSH-denied run (up to 3 times, 20 s apart) and counts retries; the formal runs needed 0. A first controls pair ran CONCURRENTLY by drafter error and a second pair hit this flake; both are kept as `superseded_*`.

## 3. Pins and what the gate owes
- The prompt `2026-09-30_secuura-batch1349.prompt.txt` (47720 bytes, sha256 `13029ba84c82…`) carries the requirements by 51 keywords (fill_gate47.py `KW`). The launcher checks each **as a token**, so `MODES` is not satisfied by `MODES-X` (controls LK1-LK15). It refuses a prompt missing:
  - a keyword (33);
  - either ticket line (32);
  - the tier lines: `#1349 T2`, `#1350 T1`, "The batch is FROZEN at TWO PRs", "a DEPLOY-PATH RUNTIME change", "ROUND 1 of its own PR", "a round-1 NO GO goes back to the author for round 2", "ship the closed instances, ticket the residue" (7);
  - the HOLDS, gate46's verbatim plus "NO checklist tick", "no Akto scan against any stack" and "No audit-baseline row edited" (39);
  - the GO (26);
  - the addendum rules incl. `MG-1 6 over 6 paths`, the three 100755 modes, `drafted texts: KS-1374`, REPORT-HASH-LAST and TRUE-OF-THE-DIFF (25);
  - the verdict subject or the report dir (23);
  - develop / END_TREE in full (31);
  - the capture, Linear read (must hold `b82bebb3`, `dc9212b5` and the UNTICKED N-1347-11 line), drafted texts, overlap probe, commission, or gate46's report path (8).
- **What the gate must do, by name** (the commission's 14, all present):
  - HOOK-SKIPPED-LEGS-1349: the 15 legs enumerated at the head, each MEASURED / NOT MEASURED with its reason, at head and END; plus FORMAT-GATE-1349 and AUDIT-LEGS-1349;
  - SUITE-1349 (93/1654 -> 94/1663, red-first 4/5, the tamper);
  - SUITE-1350-MACOS / SUITE-1350-GNU (python:3.12-slim, `--rm --network none`, read-only mount, versions printed; the whole runner on GNU NOT MEASURED if git is still absent);
  - CALLER-CELLS-1350 (R1 red AND the real deploy.sh failing over ABSENT in the re-created state);
  - N-1348-6-BOTH-WAYS; R8-EXECUTES (the skip-call tamper, with the old grep as the control); PYTHON3-ABSENT-FAILS-CLOSED (both scripts);
  - TAMPER-ARMS-1350 (T1-T8); MODES;
  - DRAFTED-COMMENTS-CHECKED (row per claim, POST AS-IS / POST AMENDED + text / DO NOT POST);
  - CLEAN-MERGE (+ census); the subjects (key-scan, <= 92, TRUE OF THE DIFF, `Refs`, no closing keyword);
  - REPORT-HASH-LAST; TIERING (the rule: a round-1 NO GO goes back for round 2; the one-PR GO form if only one may merge).
- Capture `mail_gate47_ready.md` (60457 bytes, sha256 `59f505749b3b…`): 11 mails, both heads checked in the READY and in the handover, 0 problems (capture_1.out). The READY as captured is byte-identical to the seat's `mail/READY-gate47.txt` (TEXT_SHA256 `d09cf68a7f20…`; drafts_1.out `READY == seat file: True`).
- Drafted texts `drafted_texts_gate47.md` (sha256 `462258629e24…`): KS-1374 555 chars `fe7ba98c4555…`; KS-1054 595 chars `3a5227e14526…`.
- Linear `linear_gate47.md` (33442 bytes): `KS-1374 In Progress, 5 comment(s), N-1347-11 checklist line(s) 1 (unticked 1), dc9212b5 …, 0 created AFTER gate46 | KS-1054 In Progress, 6 comment(s), raise comment b82bebb3-…, 0 created AFTER gate46`. Peter's KS-1374 comment f878a031 is in it, as data.
- gate46's report sha256 `269ac9b34c56…` equals the hash in Wednesday's gate46 GO (fill refuses otherwise).
- Launcher `launch_qa_secuura_batch1349.sh` (13877 bytes, sha256 `06fc761d951e…`). COMMISSION.md filled.

**Tiers derived (the tiering file's own criteria, `0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`):**
- **#1350 = T1:** "anything deploying to dev or demo". It is a runtime change to deploy.sh / deploy-all.sh / the predicate; KS-1054 was T1 in gates 44-46.
- **#1349 = T2:** "follow-up PRs whose MECHANISM the prior gate already measured". gate45 measured N-1347-11 and wrote this fix. It is a harness + unit test, no deploy, no product security surface; #1347 (same file) was T2 in gates 44-45.

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, after line 154 (`QA/Secuura-batch1348r2|coagent@agentmail.to|yes`, currently the last line). Back up the file first:
```
QA/Secuura-batch1349|coagent@agentmail.to|yes
```
- Until the line is present, the launch action's step 0 refuses with rc 1 (control R1 measures that refusal on an empty routing file). R8 shows the same run with the line present passing step 0 and stopping at 3b.
- **Also required before a launch:** Wednesday's `sequenced_out_of_kit` entry for #1351 in kit.json (§1), or #1351 closed / changed so that it no longer touches a kit path. Otherwise step 2b refuses rc 15.

## 5. Controls: `controls_gate47.sh <scratchpad> [--invert]` — 103 controls
- **PN0-PN7b + PNZ, pin_gate47.py:**
  - PN0 is the real subject as a simulation: PASS; END_TREE; reverse == END; 6 modes OK; #1349's move reaches NONE; overlap 0 of 6; hook IDENTICAL; path classes 0/2 and 4/4.
  - PN1 / PN1b: a wrong head for #1349 / #1350.
  - **PN3 / PN3b / PN4: a planted CONFLICT** — a #1349 stand-in that also edits deploy.sh on the line #1348 inserted after. Results: `(E) #1349 does not merge ALONE cleanly`, `step #1349 NOT clean`, `(C) … the develop move touches its own path`.
  - PN5: a #1349 stand-in that also edits the predicate prints `OVERLAP #1349 x #1350` and refuses.
  - PN6 / PN7 / PN7b: deploy.sh RECORDED 100644, the ks1054 test 100755, and aktoRateLimit.ts 100755, each giving `MODE MISMATCH`.
  - PNZ: the real pins are sha256-unchanged.
- **TR0-TR5, testrefs:**
  - the real census (7 files, PASS);
  - at develop #1349's test cannot be found (CT-POS FAIL, as it must), #1350's is found, and CT-TREE is not run;
  - a census pointed at nothing FAILS CT-POS for both PRs;
  - deploy.sh: BASENAME 1 where PATH 0;
  - CT-TREE.
- **KS0-KS9b, keyscan:** `(#n)`; a foreign key in each subject; lands at 93; a missing `Refs`; `Closes`; a foreign key in the body; a FLAG on a planted PR body; KS8 a FALSE subject that PASSES; titles == declared.
- **L0-L19 + LK1-LK15, the launcher** (exit code in brackets):
  - wrong heads: #1349 and #1350 (6 ×2);
  - moved develop (17); wrong compare paths (10);
  - a **foreign-seat GO** `Seat B 45th` (26) and a wrong merge seat (26);
  - an unfilled token (8);
  - **each of the 15 commission keywords broken to `<KW>-X` (33 ×15)**;
  - a capture without either head (20 ×2);
  - six dropped HOLDs: tickets, Peter, `.env`, docker, `az`, checklist tick (39 ×6);
  - the real launch path non-TTY (21); develop not in full (31);
  - the tier line and the round-1 rule (7 ×2); a ticket line (32);
  - MG-1, REPORT-HASH-LAST, TRUE-OF-THE-DIFF and the drafted-texts clause (25 ×4); the verdict subject (23);
  - a MOVED KIT (2);
  - the Linear read, the drafted texts, gate46's report and the overlap probe not named (8 ×4).
- **R0-R8, the launch action:**
  - **R0: the REAL census refuses rc 15 on #1351** (the live state);
  - R0s / R0q / R0c / R0b: a controls-only stand-in for Wednesday's sequencing (`G47_SEQUENCED` at #1351's current head) reaches `DRY RUN COMPLETE`, prints `SEQUENCED OUT-OF-KIT #1351`, `1 sequenced by Wednesday`, 2 of 2 heads;
  - **R0w: the stand-in at a WRONG head refuses rc 15**;
  - R1: no routing line (1);
  - R2: kit-path overlap via package-lock.json (15, #572); R3: title key KS-1297 (15, #1253);
  - R4: DISJOINT OUT-OF-KIT, dependabot (0, #945);
  - R5 / R5b: a stale head pin for each PR (11 ×2);
  - **R6: a moved develop (10)**;
  - R7: a bad scratchpad (9);
  - R8: a routed temp file, stopping at 3b (0).
- **Not controlled:**
  - on a real launch: the usage gate (5), `cockpit.sh add` (7) and the override refusal (4);
  - a `mergeable=False` refusal;
  - the REAL re-pin across a develop move (only the dry run's rc 10 is controlled).
- **Side effects, kept:**
  - R1 / R8 (and superseded runs) wrote `launch_<HHMMSS>.*` step outputs into this kit;
  - TR1 wrote `testrefs_gate47.a72149a1a803.json`;
  - the PN simulations wrote `pins_gate47.SIM-*.json`.
- **The R-series depends on live GitHub state:** #1351 open at `eac2dae2afb7`, #572 / #1253 / #945 open. If those move, R0 / R0s / R2-R4 change for that reason.

## 6. Could not measure
- The drafter ran no suite, install, lint, preflight, audit or script drive. Every seat figure is the seat's claim:
  - 93/1654 -> 94/1663; red-first 4/5; 14/0 -> 36/0 on macOS + GNU; 19/14; 22/0; T1-T8; 61/0/0;
  - `audit:gate` / `audit:locks`; the formatting gate "1 package checked".
- The 7500 / 1500 figures are READ arithmetic from the head's code (`PLATFORM_REQUESTS_PER_MINUTE` 2000, `RATE_LIMIT_HEADROOM` 0.75, `Math.max(1, Math.floor(…))`). They have not been run; the gate runs them.
- Not measured: whether #1349's tests pass over #1351 (the semantic coupling, §2.1); whether the whole shell runner runs on any local GNU image (gate46 N-1348-10: no git there); GitHub's own CI (retired; `mergeable_state` `unstable`).

## 7. Files
- Config: kit.json (incl. the EMPTY `sequenced_out_of_kit`) · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md
- Pins: pin_gate47.py -> pin_1.out (+ .rc), pins_gate47.json (+ .SIM-*.json from controls) · final_lsremote_1.out (+ .raw)
- Reads:
  - gh_read_gate47.py -> gh_read_1.out, gh_read_1.json, gh_body_1349.md, gh_body_1350.md
  - gh_read_overlap_gate47.py -> gh_read_overlap_1.out, gh_read_overlap.json, gh_body_1351.md
  - linear_read_gate47.py -> linear_read_1.out (+ .rc), linear_gate47.md
  - _mail_list_gate47.py -> _mail_list_1.out
- Checks: testrefs_gate47.py -> testrefs_1.out (+ .rc), testrefs_gate47.json · keyscan_gate47.py -> keyscan_1.out (+ .rc) · overlap_probe_gate47.py -> overlap_probe_1.out
- Capture: capture_mail_gate47.py -> capture_1.out (+ .rc), mail_gate47_ready.md · drafts_gate47.py -> drafts_1.out (+ .rc), drafted_texts_gate47.md
- Prompt and launcher: prompt_gate47.TEMPLATE.txt and launcher_gate47.TEMPLATE.sh.txt. fill_gate47.py fills them into 2026-09-30_secuura-batch1349.prompt.txt, launch_qa_secuura_batch1349.sh and COMMISSION.md (fill_1.out). Then launcher_check_1.out / launcher_check_2.out (+ .rc).
- Launch:
  - repin_and_launch_gate47.sh -> repin_dryrun_1.out (+ .rc 15);
  - repin_dryrun_0_pre1351.out (rc 0, before #1351) and repin_dryrun_1a/1b_sshdenied.out (rc 2, the SSH flake);
  - launch_<HHMMSS>.* (written by controls R1 / R8).
- Controls: controls_gate47.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt · superseded_concurrent_* and superseded_sshflake_* (earlier pairs, kept)

## 8. The ONE launch command (after the routing line, §4, AND Wednesday's #1351 sequencing entry, §1)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate47/repin_and_launch_gate47.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate47/launch_qa_secuura_batch1349.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ffc4a192-4894-4f1e-abfb-22149b1bd26c/scratchpad
```
- For a dry run, append `--dry-run`. Today it gives rc 15 on #1351 (repin_dryrun_1.out).
- Argument 2 may be ANY existing Claude session scratchpad (`/private/tmp/claude-501/*/scratchpad*`). If `g47_sp/clone` is absent there, pin_gate47.py rebuilds it on a re-pin.
- If develop moves, the launch re-pins in the same action (step 3b: pin, then testrefs, then fill; this re-asserts the modes, the overlap and the reverse END).
  - It refuses rc 10 if the move reaches any of the 6 paths or a chain step is unclean.
  - A moved head refuses rc 11.
  - Another open PR touching a kit path or titled KS-1374 / KS-1054 refuses rc 15, unless Wednesday sequenced it at its current head.
- Final re-read of the heads (final_lsremote_1.out, 2026-09-29T15:22:30Z): develop `a72149a1a803`, #1349 `daab8ff3bff5`, #1350 `8f4f0ef14963`, #1351 `eac2dae2afb7`. Every pin is still current: **True**.
