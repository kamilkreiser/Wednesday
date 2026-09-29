# Gateset 2026-09-29_gate46 — README for Wednesday

Written 2026-09-29T12:58Z by the drafter (times from `date -u`). Every figure below is read from the kit's own output files, each named beside it.

**What the drafter did and did not do.**
- It launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR, and deleted nothing.
- It wrote this kit directory (text files only) and scratch under its session scratchpad `g46_sp/`:
  - `clone`: a `git clone --shared --no-checkout` of Wednesday's `screen0929/base` clone, fetched from origin ONLY there, with the Secuura deploy key (develop, `refs/pull/1348/head`);
  - the synthetic control commits (plumbing in that clone) and the control plants under `controls_<HHMMSS>/`;
  - the return-probe driver and its outputs under `probe/`.
- It did NOT write the routing line (§4).
- The Secuura checkout was touched by read verbs only: `ls-remote` in the launcher, the repin and the final read.
- GitHub: REST GET only (gh_read_1.out / gh_read_1.json, gh_body_1348.md; the launcher's compare; the repin's PULLS reads).
- Linear: ONE read-only GraphQL `issue` query, KS-1054 (linear_read_gate46.py; no mutation in the file).
- AgentMail: ONE read-only listing of wednesday-agent@ (_mail_list_1.out) and six by-id GETs (capture_mail_gate46.py). No seen-state touched, nothing sent.
- The ONLY measurement of subject behaviour is drafter_return_probe.out (§2.1): deploy.sh's real summary block driven the way the round-2 test drives it, on macOS bash 3.2 and in `python:3.12-slim` (`docker run --rm --network none`, probe dir mounted read-only). The drafter ran no suite, install or deploy-script drive (§6). One side effect outside `g46_sp/`: that probe's CONTROL `mktemp -t` left one empty file under the macOS user TMPDIR (`/var/folders/…/T/ks1054_summary_drive.*`).

**gate46 = ONE PR, #1348 KS-1054, ROUND 2 OF 2 under the Tier-1 cap.** Author Seat B 45th, who has wrapped (WRAP 12:31:48Z in the capture). **The SUCCESSOR, Seat B 46th, merges.**
- **Clean-merge prediction: #1348 merges cleanly AS-IS over develop `8c810023f9c9` (#1347's squash). No rebase is needed.**

| PR | ticket | tier | head (ls-remote pull/head == branch == API == fetched) | parent | behind develop | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1348 | KS-1054 | T1 | `94e31db501cd01aaec7437418d7efbb592b1b59a` | `1bb58b4ebb97` (round 1; merge-base `8ba2da02d980`) | 1 | 2 | 77 -> 85 (PR title verbatim) |

- Pane `QA/Secuura-batch1348r2`. **It is NOT routed by the drafter**, see §4.
- GO string, as the GO mail's SUBJECT: `GO (Seat B 46th): merge 1348 on gate46`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-29-batch1348r2-g46/` (does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE46 #1348 round 2 of 2 (Seat B45 author, Seat B46 merges, round 46; T1: KS-1054 red proof reads the return value, mktemp portable)`.

## 1. BLUF
- **Kit: READY to launch once the routing line is added (§4).**
  - Launcher `--check` rc 0 (launcher_check_1.out: `all guards pass:`): 1 of 1 head at the branch AND at pull/head, the GitHub compare equal to the pins, 48 by-name keywords present.
  - Repin `--dry-run` rc 0 (repin_dryrun_1.out: `DRY RUN COMPLETE 2026-09-29T12:41:58Z`): `BOTH INSTRUMENTS AGREE with the pin, 1 of 1`; census `20 other open PR(s) read | 0 touch a kit path or carry a kit key`; GitHub `mergeable True`. Its only report was that the routing line is absent, the one thing the real run refuses on.
- **Pins** (pin_1.out, rc 0; ls-remote 2026-09-29T12:34:31Z):
  - develop `8c810023f9c9ac060a7aff24f0933ae3b8734479` = #1347's squash on `8ba2da02d980` (the brief's develop, re-read).
  - The head equals its branch, the PULLS API head (gh_read_1.out) and the fetched ref. The PULLS commit list is exactly 2: `1bb58b4ebb97` (round 1) and `94e31db501cd` (round 2). Round 2 is a fast-forward.
  - **(R) round-2 delta: diff(round 1, head) names ONLY the ks1054 test file (+13/-1); deploy.sh blob+mode BYTE-EQUAL round 1 vs head (`d7f94298488b`, 100755).** The product gate45 measured correct is the product under test.
- **Clean-merge status**:
  - #1348 is 1 behind. The move `8ba2da02d980..8c810023f9c9` is #1347's squash, 6 paths (both env templates, docker-compose.yml, the api-gateway ks1374 test, aktoRateLimit.ts and its test): `reaches its own paths: NONE` (pin (C)).
  - Pin (E): merge-tree over develop rc 0; simulated squash diff == its 2 own paths; every blob + mode == head.
  - **END_TREE `72b5d2e84e9972988dfa00cb623a85770b434310`** (`2 files changed, 76 insertions(+)`).
- **Recorded modes** (pin (H)): deploy.sh **100755**, the ks1054 test **100644**, at head, round 1 and END. `MODE SUMMARY: 2 path(s) pinned, 2 OK | pins seen: ['100644', '100755']`.
- **Controls, both ways** (controls_gate46.sh, one unedited script, sha256 `34367ffe1aea…` before run 1 and after run 2, controls_sha.txt):
  - normal (controls_1.out, **rc 0**): `SUMMARY gate46: 68 controls, OK 68, MISMATCH 0`;
  - `--invert` (controls_2.out, **rc 1**): `SUMMARY gate46: 68 controls, OK 0, MISMATCH 68`.
- **Test census** (testrefs_1.out, rc 0, `git grep` at END): **1 test file**, the ks1054 suite itself; deploy.sh reached only by BASENAME (PATH 0, BASENAME 1). CT-POS, CT-NEG, CT-TREE (END blob `0203b34e1970` == head, != develop `bc87f5f0a728`) all OK.
- **Key scan** (keyscan_1.out, rc 0): `KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL, 0 FLAG line(s)`. Subject key KS-1054 only, no `(#n)`, 77 -> lands 85. Body `Refs KS-1054`. PR title, PR body and both commit messages carry KS-1054 only (non-KS tokens N-1346-x / N-1348-x are information). KS8 shows a subject that is FALSE of the diff also passes the key scan: truth is the gate's.
- **Heads re-read at the end**: final_lsremote_1.out (2026-09-29T12:57:27Z): develop `8c810023f9c9`, #1348 pull/head and branch `94e31db501cd`. `every pin still current: True`.

## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated; each is a by-name item in the prompt the gate must RULE)
1. **The round-2 fix, driven at block level (MEASURED, drafter_return_probe.out).** With the function wrapper the driver rc IS the return value on bash 3.2.57 AND bash 5.2.37/GNU coreutils 9.7: `return 1` -> 1, `return 0` -> 0, `return 7` -> 7 at ERRORS=2; 0 at ERRORS=0. The round-1 top-level driver (CONTROL) gives 1 / 2 for every N. The unconditional tamper gives rc 1 at ERRORS=0 (E2 would red). The round-2 mktemp template works on GNU; `mktemp -t ks1054_summary_drive` is refused there (`too few X's`). **This is the block, not the suite**: the gate runs the suite on both runners (SUITE-MACOS-BASH32, SUITE-GNU-DEBIAN, TAMPER-RETURN-0-REDS-E1, TAMPER-UNCONDITIONAL-REDS-E2).
2. **TAMPER-ARM-COMMENT-1348 (READ).** test :124 (round 2) says "The TAMPER_RETURN_ZERO arm below drives it." `git grep -n TAMPER_RETURN_ZERO` at the head finds ONLY that comment. There is no such arm in the file; the PR body says the arm is "now present and driven". The seat drove the tamper by hand. This comment would land on develop. The gate rules its severity under the cap.
3. **E1-ANY-NONZERO-1348 (READ).** E1 is `[[ "$RC_FAIL" != "0" ]]` (:144): any non-zero rc greens it, including an environmental 127. E2 (rc must be 0) is the pair that catches that. The gate rules whether the pair suffices.
4. **`        return 1` occurs TWICE in deploy.sh** (:488 and :878 at the head). A tamper must anchor on the summary's one; the seat's own first tamper refused on that.
5. **The cap wording.** Wednesday's gate46 commission: "a NO GO ships nothing on this class and goes to Kam as a card." Her 12:13Z GO mail (in the capture) withdrew her own "ships nothing" wording for #1347 in favour of the tiering rule ("ship the closed instances, ticket the residue"). For one PR the fix and its proof ship together, so the two readings likely coincide. The prompt carries the commission's line verbatim and asks the gate to say if it thinks the rule's text should govern.
6. **The PR body** (gh_body_1348.md) keeps round 1's text above the `# ROUND 2` section, including the NOT COVERED #3 line gate45 called false (N-1348-5), which the round-2 section corrects. The squash body is composed, so this does not reach history.
7. **KS-1054 raise comment b82bebb3** is unedited, and no comment was added after gate45 (linear_read_1.out: `0 created AFTER gate45, 0 edited after gate45`). gate45 found it implies E1 proves the return value. At round 2 that becomes true of the head. No ticket comment names the round-2 head.
8. **N-1348-3** (deploy.sh aborts on nginx page / demo login / empty or non-JSON /health) is in scope and already with Kam. **N-1346-2/-3/-4** are named not fixed: not required. The gate re-confirms deploy.sh's rows beside gate45's figures, since deploy.sh is byte-equal.
9. GitHub reports `mergeable True (unstable)`: CI does not start on this account. The READY quotes the push preflight at 12/15 legs (3, 4, 8 skipped).

## 3. Pins and what the gate owes
- The prompt `2026-09-29_secuura-batch1348r2.prompt.txt` (27914 bytes, sha256 `b79ca1a47560…`) carries the requirements by 48 keywords (fill_gate46.py `KW`). The launcher refuses a prompt that is missing any of the following:
  - a keyword (exit 33; L6 / L6b SUITE-GNU-DEBIAN / L6c controlled);
  - the ticket (32) or the tier lines, "The gate is FROZEN at ONE PR", "ROUND 2 OF 2 under the Tier-1 cap" and "a NO GO on #1348 ships NOTHING of it (no round 3) and goes to Kam as a card" (7);
  - the HOLDS, including "No `az` command of any kind", "You NEVER reply to Peter", "Never read or write a real `.env`" and "Docker runs are `--rm --network none` with the source mounted READ-ONLY" (39);
  - the GO (26);
  - the addendum rules, **REPORT-HASH-LAST** and "EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF" (25);
  - the verdict subject or the report dir (23);
  - develop / END_TREE in full (31);
  - the capture, the Linear read (must contain `b82bebb3`), the commission, the drafter probe, or gate45's report path (8).
- **What the gate must do, by name:**
  1. N-1348-1 and N-1348-2 re-checked as ROWS with evidence (N-1348-1-RECHECK, N-1348-2-RECHECK).
  2. The ks1054 suite on **macOS bash 3.2 AND a GNU/Debian image** (python:3.12-slim for the CI-equivalent reading; ubuntu:24.04 for mktemp only, since it lacks python3), with `bash --version` / `mktemp --version` in the same run; if no GNU image can run, **NOT MEASURED, said plainly**. Both images are present locally (`docker images`, 12:36Z).
  3. Red at base (E1 alone) on both; **`return 1` -> `return 0` must red E1**; **an unconditional-return tamper must red E2**, on both; the real deploy.sh with a clean body rc 0, and non-zero under the unconditional tamper.
  4. Everything that held in gate45 still holds: N-1348-1…-5 as rows; the deploy-path table re-driven with stubs beside gate45's figures; pre-existing arms; modes; the round-2 delta test-only.
  5. Whole suites develop / head / END; census; END over #1347's squash.
  6. Subject key-scanned, landed <= 92, TRUE of the (whole-PR) diff; body `Refs KS-1054`, no closing keyword.
  7. The cap: a NO GO ships nothing and goes to Kam as a card.
- **REPORT-HASH-LAST**: `## MERGE ADDENDUM` is the LAST thing written to report.md, and NOTHING goes into report.md after the verdict mail. Late evidence goes to `evidence/late_<HHMMSS>.md`. The mail body carries `sha256 report.md = <hex>`. Controls L13b / L13c prove the launcher refuses a prompt that drops these.
- Launcher `launch_qa_secuura_batch1348r2.sh` (12276 bytes, sha256 `937595025a3f…`).
- Capture `mail_gate46_ready.md` (33198 bytes, sha256 `a6740f2b29d4…`): six mails, the READY head-checked, 0 problems (capture_1.out). The READY is 12:30:10Z; the WRAP 12:31:48Z.
- Linear read `linear_gate46.md` (11729 bytes, sha256 `b27eb118abbc…`): `LINEAR READ OK: 6 comment(s) on KS-1054, raise comment b82bebb3-…`.
- gate45's report sha256 `4794da1d3faa…` (fill_1.out), equal to the hash in Wednesday's 12:13Z GO mail.
- COMMISSION.md (filled).

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, after line 153 (`QA/Secuura-batch1348|coagent@agentmail.to|yes`, currently the last line). Back up the file first:
```
QA/Secuura-batch1348r2|coagent@agentmail.to|yes
```
Until the line is present, the launch action's step 0 refuses with rc 1. Control R1 measures that refusal on an empty routing file. R8 shows the same run with the line present passing step 0 and stopping at 3b. The dry run found no other refusal.

## 5. Controls: `controls_gate46.sh <scratchpad> [--invert]`
- **PN0-PN7 + PNZ, pin_gate46.py:**
  - PN0: the real subject as a simulation (PASS; END_TREE `72b5d2e84e99…`; MODE SUMMARY 2 OK; the move reaches NONE; deploy.sh BYTE-EQUAL round 1 vs head).
  - PN1: a head it was not given refuses.
  - PN2: a round-2 stand-in that ALSO edits deploy.sh: `(R) the round-2 delta … != the declared` and `deploy.sh changed between round 1 and the head`.
  - PN3: a planted CONFLICT on docker-compose.yml:497, the line #1347 rewrote: `(E) #1348 NOT clean over develop`; PN4, the same run: `(C) … the develop move touches its own path`.
  - PN6: deploy.sh RECORDED 100644, so `MODE MISMATCH`. PN7: the test RECORDED 100755, so `MODE MISMATCH`.
  - PNZ: the real pins are sha256-unchanged.
- **TR0-TR5, testrefs_gate46.py:** the real census (1, PASS); the census at develop (PASS, CT-TREE not run there); a census pointed at nothing FAILS CT-POS; BASENAME 1 where PATH 0; CT-TREE.
- **KS0-KS9, keyscan_gate46.py:** `(#n)` suffix; a foreign key in the subject; the subject plus 8 characters (`declared 85, lands at 93`); a missing `Refs KS-1054`; `Closes`; a foreign `KS-206` in the body; a FLAG on a planted PR body (`KS-1332`); KS8 a FALSE subject ("…only when startup migrations have failed") PASSES the scan; KS9 `title == declared: True`.
- **L0-L17, the launcher** (exit code in brackets): wrong head (6), moved develop (17), wrong compare paths (10), a foreign-seat GO `Seat B 45th` (26), an unfilled token (8), dropped keywords TAMPER-RETURN-0-REDS-E1 / SUITE-GNU-DEBIAN / TAMPER-UNCONDITIONAL-REDS-E2 (33 ×3), a capture without the head (20), four dropped HOLDs incl. the docker hold (39 ×4), the real launch path non-TTY (21), develop not in full (31), the tier line (7) and the cap line (7), the ticket line (32), MG-1 (25), REPORT-HASH-LAST (25), TRUE-OF-THE-DIFF (25), the verdict subject (23), a MOVED KIT (2), the Linear read not named (8), the drafter probe not named (8).
- **R0-R8, the launch action:** the dry run (0) and its census line; a real run without the routing line (1); a kit-path overlap via G46_OVERLAP_EXTRA=package-lock.json (15, #572); a title-key overlap via G46_TITLE_KEY=KS-1297 (15, #1253); DISJOINT OUT-OF-KIT via G46_WIDEN_RX on the dependabot PRs (0, #945); a stale head pin (11); a moved develop (10); a bad scratchpad (9); a real run with a routed temp file that stops at 3b (0).
- **Not controlled:** on a real launch, the usage gate (5), `cockpit.sh add` (7) and the override refusal (4); a `mergeable=False` refusal; the REAL re-pin across a develop move (only the dry run's rc 10 is controlled).
- **Side effects, kept:** R1 / R8 wrote `launch_<HHMMSS>.*` step outputs into this kit (1247/1250 from controls_1, 1255/1256 from controls_2); TR1 wrote `testrefs_gate46.8c810023f9c9.json`; the PN simulations wrote `pins_gate46.SIM-{real,prod,cfl,m644,m755}.json`.

## 6. Could not measure
- The drafter ran no suite, install, tsc, shellcheck, deploy-script drive or runtime probe beyond drafter_return_probe.out (the extracted block only).
- The seat's claims are NOT the drafter's measurements: macOS 14/0; GNU 14/0 on python:3.12-slim with `mktemp --version`; `return 0` tamper -> E1 red alone, 13/1; deploy.sh sha256 equal to round 1 after restore (pin (R) does show deploy.sh byte-equal round 1 vs head by blob).
- Not measured, each a gate item: the suite on either runner; E1/E2 under tampers inside the real suite; the real deploy.sh drive at round 2; whole shell runner under GNU; GitHub's own ubuntu-latest runner (the local images are approximations).

## 7. Files
- Config: kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md
- Pins: pin_gate46.py -> pin_1.out (+ .rc), pins_gate46.json (+ .SIM-*.json from controls) · final_lsremote_1.out
- Reads: gh_read_gate46.py -> gh_read_1.out, gh_read_1.json, gh_body_1348.md · linear_read_gate46.py -> linear_read_1.out (+ .rc), linear_gate46.md · _mail_list_gate46.py -> _mail_list_1.out
- Checks: testrefs_gate46.py -> testrefs_1.out (+ .rc), testrefs_gate46.json · keyscan_gate46.py -> keyscan_1.out (+ .rc) · drafter_return_probe.out (driver drafter_return_probe.sh.txt)
- Capture: capture_mail_gate46.py -> capture_1.out (+ .rc), mail_gate46_ready.md
- Prompt and launcher: prompt_gate46.TEMPLATE.txt and launcher_gate46.TEMPLATE.sh.txt; fill_gate46.py fills them into 2026-09-29_secuura-batch1348r2.prompt.txt, launch_qa_secuura_batch1348r2.sh and COMMISSION.md (fill_1.out). Then launcher_check_1.out (+ .rc).
- Launch: repin_and_launch_gate46.sh -> repin_dryrun_1.out (+ .rc) · launch_<HHMMSS>.* (written by controls R1 / R8)
- Controls: controls_gate46.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt

## 8. The ONE launch command (after the routing line, §4)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate46/repin_and_launch_gate46.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate46/launch_qa_secuura_batch1348r2.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/35f90900-da39-4310-a097-bf496fc89a5b/scratchpad
```
- For a dry run, append `--dry-run`. repin_dryrun_1.out is one, rc 0.
- Argument 2 may be ANY existing Claude session scratchpad (`/private/tmp/claude-501/*/scratchpad*`). If `g46_sp/clone` is absent there, pin_gate46.py rebuilds it on a re-pin.
- If develop moves, the launch re-pins in the same action (step 3b: pin, then testrefs, then fill; the re-pin re-asserts the recorded modes and the round-2 delta).
  - It refuses rc 10 if the move reaches either of the PR's paths, if the squash is unclean, or if a mode pin fails.
  - A moved head refuses rc 11.
  - Any other open PR touching one of the 2 paths, or titled with KS-1054, refuses rc 15.
- Final re-read of the heads, final_lsremote_1.out (2026-09-29T12:57:27Z): develop `8c810023f9c9`, pull/head and branch `94e31db501cd`. Every pin is still current: **True**.
