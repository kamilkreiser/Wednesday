# Gateset 2026-09-30_gate49a — README for Wednesday

Written by the drafter, 2026-09-30 (all times from `date -u`). Every figure below comes from the kit's own output files, each named beside the figure.

## 0. Pin status and what remained to fill

The kit was drafted UNPINNED (`<PR>` / `<HEAD>` / `<BRANCH>` placeholders in kit.json; the unpinned copy is kept as `kit.json.pre-pin-041617`). Wednesday named **PR #1356, head `52dadb07f70d20da8f201b518eba4ebff05c8455`** at ~04:15Z, and the drafter pinned it. Everything that was left to fill is now filled:

| was a placeholder | how it was filled | where |
|---|---|---|
| `<PR>` (pane, launcher, prompt, report dir, GO, verdict subject, the `prs` key) | `pinpr_gate49a.py 1356 <head>` | kit.json (pinpr_1.out rc 0) |
| `<HEAD>` | the same; checked by `ls-remote refs/pull/1356/head` AND the branch AND the PULLS API | pinpr_check_1.out, pinpr_1.out |
| `<BRANCH>` | taken from the API (`head.ref`), never typed: `feature/ks-1378-in-range-lock-refresh-six-advisories-b49-a` | kit.json |
| the pins (develop, END_TREE, modes, unchanged blobs) | `pin_gate49a.py` | pin_1.out rc 0 -> pins_gate49a.json |
| the PR body, census, capture, key scan, lock delta, reach, overlaps | the instruments below, all at the pinned head | *_1.out (+ .rc) |
| the prompt, launcher, COMMISSION | `fill_gate49a.py` | fill_1.out rc 0 |

**Still NOT done (Wednesday's):** the routing line (section 4) and the launch.

**What the drafter did and did not do.** It launched nothing, added no routing line, sent no mail, tapped no pane, merged / committed / pushed nothing, posted nothing, changed no ticket or PR, deleted nothing (superseded outputs renamed `superseded_*`). It wrote only this kit directory and its session scratchpad (`g49a_sp/`: a `git clone --shared --no-checkout` of gate48b's scratch clone, fetched from origin only there; the synthetic plants; `refs/sim/itemA`, a SIMULATED head built from the seat's record copies before the PR existed). In `/Volumes/DevMASTER/!CODING/` it ran `ls-remote` and read files only. External reads: GitHub REST GETs, public advisory-API and npm-registry GETs, AgentMail listings and GETs by id (read-only). No install, audit, regen, build or suite.

## 1. The PR and the BLUF

| PR | ticket | tier | head | parent | ahead / behind | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1356 | KS-1378 | T1 | `52dadb07f70d20da8f201b518eba4ebff05c8455` | `3e3a68260d0e` (= develop) | 1 / 0 | 18 locks, **+90/-90** | 72 -> 80 (PR title == commit subject) |

- Pane `QA/Secuura-batch1356` (**not routed** — section 4). GO string (the GO mail's SUBJECT): `GO (Seat B 49th): merge 1356 on gate49a`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-30-batch1356-g49a/` (does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE49A #1356 (Seat B49 author and merger, round 49a; T1 KS-1378 in-range lock refresh: brace-expansion, fast-uri, ip-address in 18 locks)`.

**BLUF.**
- **Kit: READY to launch once the routing line is added.** Launcher `--check` rc 0 (launcher_check_1.out). Repin `--dry-run` rc 0 (repin_dryrun_1.out): the ONLY report is the missing routing line; `BOTH INSTRUMENTS AGREE with the pin, 1 of 1`; census `0 touch a kit path … outside reported_overlaps | 10 expected overlap(s)`.
- **Controls, both ways** (one unedited script, hashed in controls_sha.txt): normal **rc 0, 132 of 132 OK**; `--invert` **rc 1, 132 of 132 MISMATCH** (section 5).
- **Pins** (pin_1.out rc 0): develop `3e3a68260d0ef541b2410d323849d2639ddd6941` (tree `0693c2b391b6` = gate48b's END). #1356 alone over develop is clean. **END_TREE `9b61e858210de7dce3a76f7cfa24e7cb99bc231b`** (`18 files changed, 90 insertions(+), 90 deletions(-)`). All 18 paths recorded 100644; `.githooks/pre-push` 100755 is the control. `audit-baseline.json`, `baseline-contract.mjs`, `advisory-fetch-stub.mjs`, both service Dockerfiles, the root / mcp-server / nft-certificate manifests and `Blockchain/Dev/mobile/secuura-app/package-lock.json` are byte-equal at develop, head and END.
- **The real head's tree == the drafter's simulation built from the seat's record copies** (`refs/sim/itemA`, tree `9b61e858210d`): the seat's `itemA/locks/*.after.json` are exactly what was pushed.

**Drafter predictions (the gate re-derives each):**
- lockdelta_1.out `LOCKDELTA PASS: 0 FAIL of 118 checks`: 18 locks, **30 moves (7 PROD)**, ADDED 0 / REMOVED 0 in every lock, each changed entry differs in exactly {version, resolved, integrity}, no flag flipped, every move within its major. The moved set == the seat's claim one to one. **36 dependant ranges, all satisfied** (minimatch `^5.0.5` / `^5.0.8` / `^1.1.7`, ajv `^3.0.1`, express-rate-limit `^10.2.0`), with the `<major+1>.0.0` control refused 36 of 36. Registry-true for all 4 (package, version) pairs, the wrong-integrity and from-version controls False. All six advisory ranges read from the API: every to-version outside, every from-version inside. **Residue at the head: only `Blockchain/Dev/mobile/secuura-app` (5 brace-expansion entries, flagged PRODUCTION in that lock, 1.1.18 x4 + 2.1.4 — KS 769's scope).** The stub fixture's synthetic fast-uri range still covers 7 entries, so the planted-refusal control stays live.
- reach_1.out `REACH READ`: **11 Dockerfiles copy a moved lock, not 2** — only mcp-server (brace-expansion, fast-uri, ip-address) and nft-certificate (brace-expansion, fast-uri) move PRODUCTION entries; the other 9 move dev entries only. **0 Dockerfiles copy the root lock** (mcp-server's own COPY found as the control). At develop the same read gives 0 images (the control that the 11 come from the head). 5 test files name a changed path, all via the generic `package-lock.json` (lock-discovery.test.mjs and 3 `scripts/__tests__/*.test.sh` among them).
- overlaps_1.out `OVERLAPS READ: 10 PR(s)`: all 10 are dependabot PRs on the ROOT lock. All merge clean after #1356 except #649, which already conflicts on develop today (pre-existing). None touches a brace-expansion / fast-uri / ip-address entry.
- keyscan_1.out `KEYSCAN PASS: 6 checks, 0 FAIL, 0 FLAG`: title and commit subject `KS-1378: in-range lock refresh clears six new advisories across 18 locks` (72 -> 80), `Refs KS-1378` on its own line in the PR body and the commit, no foreign key on any surface (title, body, commit, branch name).
- capture_1.out `CAPTURE OK`: 10 mails by id from one listing (the READY 04:12:48Z names the head in full and the base); the LAUNCH BRIEF and ADDENDUM 1 by id + sha256 only; Wednesday's 4 ANSWER files for Seat B 49th. The seat's record has no `mail/READY-1356.txt`, so no record comparison was possible (reported, not refused).
- FUSE: 4 rows expire 2026-10-09 at develop and at the head (GHSA-337j, GHSA-wrjc, GHSA-frvp, GHSA-mwp4); #1356 adds none.

## 2. What the gate must rule (by name in the prompt; each re-derived, never trusted)
1. **RUNTIME-REACH, first.** Build mcp-server + nft-certificate at develop AND head (`-p g49aprobe-base` / `-p g49aprobe-head`, build only) and read the three packages' versions in the SERVED trees (including `/shared`, which comes from `packages/shared`'s lock — NOT moved by this PR). Wednesday's addition (b): the READY claims mcp-server serves 5.0.12 / 3.1.8 / 10.7.2, develop's images the control. Addition (c): node:24-alpine's own npm bundles brace-expansion 5.0.7 and ip-address 10.2.0; the gate says whether that copy is reachable at runtime — information, not a blocker.
2. **LOCK-DELTA-18, DEPENDENT-RANGES, REGISTRY-TRUE** with its own code and a real semver.
3. **REPRODUCE-REFRESH / PRISTINE-CONTROL**: its own refresh in node:24-alpine + npm 11.19.0 from a `git archive` of develop, `cmp` to the head; the pristine control that moves nothing.
4. **AUDIT-LEGS-BASE-HEAD, SIX-IDS-ABSENT, GATE-STILL-REFUSES, NO-BASELINE-ROW**: legs 6/7 rc 1 at develop with exactly the six, 0/0/0 at head, each id absent separately, the stub's `finding` mode rc 1 on both legs.
5. **SUITES** (Wednesday's addition (a)): both services at develop and head, each with AND without `packages/shared` built — the READY says red before the shared build on both trees (mcp 1 failed file, nft 2), green 5/5 and 38/38 after. **SHARED-GUARD-TESTS**: the 5 guard tests at both trees.
6. **NPM-CI-HEAD**: root + the standalone locks (or a named set of at least 6).
7. **CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS**: the 10 dependabot PRs reported, and whether a rebase of any of them could re-introduce a vulnerable version.
8. **Subject, body, branch, commit** + **PR-BODY-CLAIMS** line by line; **Linear** (Wednesday's addition (d)): one read-only query for the attachments citing #1356 (the READY: exactly 1, on KS-1378) — named exception X5, the only permitted read of a real `.env`, by key name, never printed.
9. **FOLLOW-ONS, FUSE-COUNT**: mobile residue under KS 769; whether 10.7.2 also clears GHSA-mwp4 (the row ITEM 2 removes); the stub fixture's stale "seven locks at 3.1.7" comment.

**Doubts the drafter found:** (a) **the numstat**: the seat's status mail (03:56Z) said +102/-102; the head is **+90/-90** (30 moves x 3 lines) — the PR body does not repeat +102, the gate says where it came from; (b) 11 images, not 2 (above); (c) the root lock's two PRODUCTION moves reach no image; (d) `/shared` in both images is outside this PR; (e) the two INERT locks and the zsh word-split slip are the seat's history — the gate's reproduction settles the bytes; (f) the PR body names KS 769 de-hyphenated but **not KS 729**, which Wednesday's plan asked for on the ip-address pair (keyscan INFO line) — a PR-BODY-CLAIMS item, not a key-scan failure; (g) the dependabot locks predate the advisories.

## 3. Pins and what the gate owes
- The prompt `2026-09-30_secuura-batch1356.prompt.txt` (36132 bytes, sha256 `98c834dc246f…`) carries 29 by-name keywords (fill_gate49a.py `KW`), each checked as a TOKEN.
- The launcher `launch_qa_secuura_batch1356.sh` (13455 bytes, `bca86578b0ef…`) refuses on: a missing keyword (33); the ticket (32); tier / FROZEN at ONE / round (7); the RUNTIME-FIRST rule (34); the authority line — Wednesday's ANSWER plan, "The 09-09 baseline grant is NOT used." (36); the HOLDS + named exceptions (39); the GO (26); the addendum rules incl. REPORT-HASH-LAST (25); verdict subject / report dir (23); develop / END_TREE in full (31); a kit file or gate48b's report not named, an unfilled token or a `<PR>` placeholder (8); the head not in both capture and prompt (20); a moved head (6); the compare (10); develop moved (17); non-TTY (21); overrides (16).
- **HOLDS vs gate48b:** every phrase the launcher checks is carried verbatim. Changed: "#1355 deploys nothing" -> "#1356 deploys nothing"; "You push to neither #1354 nor #1355" -> "You push to no PR". Named exceptions: X1 registry reads (npm ci, npm audit, the refresh); X2 the refresh containers with network on a scratch `git archive`; **X3 TWO builds** (`-p g49aprobe-base` and `-p g49aprobe-head`, `build mcp-server nft-certificate`, build only, left in place); X4 advisory / registry GETs; **X5 one read-only Linear query** (new, for Wednesday's addition (d)). gate48b's X3b (builder-stage build) and X5 (preflight) are not carried: the brief asked for neither.
- The capture `mail_gate49a_ready.md` (63483 bytes, `c7b08427bb0c…`). gate48b's report sha256 `5ae77e86d1ea…` == kit.json's; the fill refuses otherwise.
- `reported_overlaps` (kit.json): the 10 dependabot PRs with their heads, filled from the pre-pin census and re-read at the pin (0 HEAD MOVED). An overlap OUTSIDE that set refuses rc 15. `sequenced_out_of_kit` is EMPTY.

## 4. Routing line — NOT added
Back up the file first. Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (currently 159 lines, the last `QA/Secuura-batch1355|coagent@agentmail.to|yes`):
```
QA/Secuura-batch1356|coagent@agentmail.to|yes
```
Until it is present, step 0 of the launch action refuses rc 1 (control R1); R8 shows a routed temp file passing step 0 and stopping after 3b.

## 5. Controls: `controls_gate49a.sh <scratchpad> [--invert]`
- **132 controls.** One unedited script (`controls_gate49a.sh`, sha256 `7bde78f5d0ef…`, identical before run 1 at 04:29:56Z, before run 2 at 04:44:38Z and after run 2 at 04:57:21Z: controls_sha.txt). Normal (controls_1.out) **rc 0: `132 controls, OK 132, MISMATCH 0 | ssh-denied retries 0`**. `--invert` (controls_2.out) **rc 1: `132 controls, OK 0, MISMATCH 132`**.
- The first `--invert` attempt ran inside a tool job with a 30-minute cap and was stopped part-way by the drafter before the cap hit. Its partial output is kept as `superseded_controls_2_0_bgtimeout_stopped.out`, and run 2 was re-run in full on the same unedited script.
- **PN0-PN6, PNZ (pin):** the real head as a simulation (END, 18 files +90/-90, modes, mobile's lock byte-equal, the hook); `--develop` refused without `--simulate`; the mcp-server Dockerfile edited -> (K); a develop move on services/shared's lock -> (C); the mcp-server lock recorded 100755 -> MODE MISMATCH; an unrelated develop move -> NONE; a package.json added -> (B).
- **LD0-LD7 (lockdelta):** the real head (118 checks; the 30-move claim; the L4c / L5c / L6 controls; the mobile-only residue; the stub still live; CLAIM DIFFERS on +102); another mcp-server entry edited (L2 + 31 moves); fast-uri's integrity changed (L5, online); a dev flag added to root brace-expansion (L2 flags); ip-address 11.0.0 (L4 out of `^10.2.0`); admin's lock reverted (L0 missing); develop as the head (L0 0 paths); the semver table.
- **RE0-RE1 (reach):** the real head (11 images, 0 root copies, mcp's PROD row, the test controls) and develop (0 images).
- **OV0 (overlaps)** with its CT-CLEAN / CT-CONFLICT pair. **KS0-KS8 (keyscan):** `(#n)`, a foreign key, lands 93, `KS-13780`, no `Refs`, `Closes`, a foreign body key, a key outside a fence, a FALSE subject that still passes (truth is the gate's). **PP1-PP2 (pinpr):** refuses a pinned kit; refuses a malformed head.
- **L0-L21 + LK1-LK29 (launcher):** wrong head (6), develop moved (17), compare (10), GO / seat (26 x2), unfilled token / placeholder (8 x2), each keyword broken (33 x29), capture without the head (20), nine HOLDs (39 x9), non-TTY (21), develop in full (31), tier / round (7 x2), ticket (32), five addendum rules (25 x5), verdict subject (23), MOVED KIT (2), three kit files + the previous report (8 x4), RUNTIME-FIRST (34), authority (36).
- **R0-R8 (launch action):** dry run complete with the census line, an EXPECTED OVERLAP, Peter's #1351 reported and 1-of-1 agreement; no routing (1); reported set emptied -> #949 refuses (15); title key KS-1386 hits #1351 (15); a controls-only sequencing of #1351 at its head is reported (0) and at a WRONG head refuses (15); a `-l5-1` branch reported DISJOINT; stale head (11); moved develop (10); bad scratchpad (9); routed temp file stops after 3b.
- **KJZ / PRZ / PNZ:** kit.json, the filled prompt and the real pins sha256-unchanged by every control.
- **Not controlled:** on a real launch the usage gate (12), `cockpit.sh add` (14) and the override refusal (16); a `mergeable=False` refusal; a real re-pin across a develop move (the dry run's rc 10 only); capture_mail_gate49a.py and fill_gate49a.py are exercised by their real runs (capture_1.out, fill_1.out), not by plants.
- **Side effects, kept:** R1 / R8 wrote `launch_<HHMMSS>.*` step outputs here; the PN simulations wrote `pins_gate49a.SIM-*.json` (`SIM-itemA` is the pre-PR dry test).
- **The drafter's own instrument errors, caught and kept:** `superseded_capture_0_planconf_idonly.*` (the seat's plan confirmation was recorded id-only because its subject says "ADDENDUM"; now only Wednesday's briefs are id-only); `superseded_fill_0/1_*` (the launcher template carried the literal placeholder its own guard refuses); `superseded_fill_2_numstatwording.*` / `superseded_launcher_check_0_numstatwording.*` (the numstat sentence was reworded after the real head read +90/-90); `superseded_reach_0_movedbyname.*` (reach counted a lock as moved by NAME; the trial controls' RE1 caught it at develop — it now requires the lock to differ from develop at the tree read; the head's figures are unchanged).

## 6. Could not measure (the drafter)
No audit leg, install, regen, image build, served-file read or suite: every one of those is the seat's claim until the gate runs it. The census, Dockerfile COPY lines and test references are git READS; nothing in an image was read.

## 7. Files
- **Config:** kit.json (+ `kit.json.pre-pin-041617`, the unpinned kit) · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md (this).
- **Pin:** pinpr_gate49a.py -> pinpr_check_1.out, pinpr_1.out · pin_gate49a.py -> pin_1.out, pins_gate49a.json (+ .SIM-*.json).
- **Reads:** gh_read_gate49a.py -> gh_read_census_prepin.out/.json (pre-pin), gh_read_1.out, gh_read_1.json, gh_body_1356.md · capture_mail_gate49a.py -> capture_1.out, mail_gate49a_ready.md.
- **Instruments:** lockdelta_gate49a.py -> lockdelta_1.out · reach_gate49a.py -> reach_1.out · overlaps_gate49a.py -> overlaps_1.out, overlaps_gate49a.json · keyscan_gate49a.py -> keyscan_1.out (each with its .rc).
- **Prompt and launcher:** prompt_gate49a.TEMPLATE.txt + launcher_gate49a.TEMPLATE.sh.txt, filled by fill_gate49a.py (fill_1.out) -> the prompt, the launcher, COMMISSION.md; launcher_check_1.out, launcher_check_2.out (after the controls, rc 0); final_lsremote_1.out (04:57:49Z: develop 3e3a68260d0e, #1356 52dadb07f70d at branch and pull/head).
- **Launch:** repin_and_launch_gate49a.sh -> repin_dryrun_1.out.
- **Controls:** controls_gate49a.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt.

## 8. Re-draft recipe (a new head on #1356)
Restore `kit.json.pre-pin-041617` as kit.json (keep the pinned one as `kit.json.pinned-52dadb07`), then: `pinpr_gate49a.py 1356 <new head>` -> `pin_gate49a.py <sp>` -> `gh_read_gate49a.py` -> `lockdelta_gate49a.py <sp>` -> `reach_gate49a.py <sp>` -> `overlaps_gate49a.py <sp>` -> `keyscan_gate49a.py <sp>` -> `capture_mail_gate49a.py` -> `fill_gate49a.py` -> the controls both ways (update the head-specific patterns: `52dadb07f70d`) -> `--check` -> dry run. If develop moves, the launch action re-pins in the same action (rc 10 if the move reaches one of the 18 locks).

## 9. The ONE launch command (run it after the routing line in section 4 is added)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate49a/repin_and_launch_gate49a.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-30_gate49a/launch_qa_secuura_batch1356.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/cab52cfa-6cf1-4ddd-807b-05202d63388e/scratchpad
```
- The PR number (`1356`) and the head (`52dadb07f70d…`) that were placeholders (`<PR>` / `<HEAD>`) are now filled in the launcher name and its row.
- Append `--dry-run` for a dry run (rc 0 today, repin_dryrun_1.out). Argument 2 may be ANY existing Claude session scratchpad; if `g49a_sp/clone` is absent there, pin_gate49a.py rebuilds it on a re-pin.
