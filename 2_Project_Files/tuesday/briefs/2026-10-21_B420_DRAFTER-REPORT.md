# B420 drafter report (Sonnet 5.5, read-only), 2026-10-21 20:03-20:22 AEDT

Files written (three, as asked, all in `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/`):
1. `2026-10-21_B420_SEAT-G36_nexusai-gate33-pr101-repin2.md` (the re-pinned kit, 174 lines, sha256 `cd820874a7d217d7a39884042b0d02cef5744735754b24e8689fbc9deefc7b32`).
2. `2026-10-21_B420_launch_qa_nexusai_gate33_repin2.sh` (the launcher copy, 800 lines, mode 644, sha256 `3ef87589ee5b36676338c4b51d1dec530656660a435a4b42926e142f18d3ed5f`; NOT installed anywhere).
3. this report.

Deviations from "Write only" that you should know about, own actions: after the first Write of the launcher I used Edit three times on that same draft (removed one junk line I had left in guard 22M that would have aborted under `set -u`; removed a person's first name from one prompt sentence; dropped two words from guard 19's list). I also built two throwaway harness scripts in the session scratchpad (`.../scratchpad/harness.sh`, `harness2.sh`, `harness_neg1.sh`, `harness_neg2.sh`) to run the launcher's text and git guards against the kit; they are not deliverables. No `rm`, no Artifact/Docs/mail/chat/publish tool, no fetch/pull/push/worktree/checkout/reset/stash/commit/`merge-tree --write-tree`, no npm/node/jest/HTTP, no `--check` run of the launcher.

## Measured facts (read verbs only; times AEDT; instrument beside each)
- **Refs** (`git --no-optional-locks ls-remote origin`, 20:03:29 rc 0 attempt 1; again 20:18:35 rc 0): `refs/heads/main` `b8715182808a2c1cf64f009b1a6e23758c63e43a` (unchanged between the two reads); `refs/heads/rd-874-875-test-guards-uat-port-r11` = `refs/pull/101/head` = `7c11c78f174a91ed2a376110966da19e775311e7`; `refs/pull/102/head` `b8715182…`; `refs/pull/103/head` `940dac40b34840e22190c83d4b9ce6ee6b526e6b`; `refs/pull/67/head` `94b288cc64d6348ebd75b502a8712a543358e51b`. All equal the task's pins.
- **Chain** (`log --format='%H %T %P' b8715182..7c11c78f`, `cat-file -t`, `rev-parse ^{tree}`): five commits, three merges (`rev-list --merges --count` 3; parent counts 2 2 2 1 1; `--first-parent` count 5, which B419 did not measure and B411's report had flagged as unmeasured). Head `7c11c78f` tree `71817e8c…` parents `5cc06298 b8715182`; `5cc06298` tree `d88cff88…` parents `48a17df8 c139e4a8`; `48a17df8` tree `bb71baa0…` parents `6e947f4d 115a775b`; `6e947f4d` tree `eb5fc01a…` parent `a7e8f4f9`; `a7e8f4f9` tree `3358d239…` parent `d463f881`. Main `b8715182` tree `fbef3a20…` parents `b52b46fb 940dac40`; `c139e4a8` tree `aeb3b687…`; `d463f881` tree `53d51c59…`. `rev-list --left-right --count b8715182...7c11c78f` = `0 5`; `merge-base --is-ancestor b8715182 7c11c78f` rc 0; `c139e4a8`, `115a775b`, `b52b46fb`, `940dac40` are all ancestors of main (rc 0 each).
- **Diffs** (`diff --name-status/--numstat/--name-only`): `b8715182 7c11c78f` = the same six paths (5 M + 1 A; numstat 2/0, 2/0, 103/0, 2/0, 3/3, 35/12 = +147/-15). Name-list sha256: space-joined `f4db97c6…795c` (the pin's form), newline-joined `55ad421b…`. `48a17df8 5cc06298` = `package-lock.json`. **`5cc06298 7c11c78f` = `M HISTORY.md` (22/0), `M scripts/propose-dark-retheme.js` (2/2)**; `c139e4a8 b8715182` = the same two paths. Control: `5cc06298 b8715182` prints 8 paths. Patch equality: sha256 of `git diff c139e4a8 5cc06298` = of `git diff b8715182 7c11c78f` = `52081b4cb20159e6c84d400e18477c6bac9e9f2825c8cb5fa1aaf26177a0530a` (12466 bytes), and the `--binary` forms are equal too; the control `b8715182 5cc06298` differs (the launcher's guard 22M uses it).
- **Blobs** (`rev-parse <rev>:<path>`): all six PR blobs at the head equal the old head's and equal what B419 recorded (auth-gate `5db407a5…`, rd395 `0c92455e…`, rd875 `ca3ca561…`, scim `b9aeef8b…`, counts `a2f40639…`, uat-run `e5370d2d…`); main's blobs `d91f441a…`, `f02e4770…`, `23df5947…`, `c050e783…`, `3841b60a…`. `package.json` `384805d9…`, `package-lock.json` `9cae0533…`, `deploy-demo.yml` `953b2a2f…`, `backend/jsonStorage.js` `2abb5cf4…` identical at main and head. `HISTORY.md` `fd455216…` and `scripts/propose-dark-retheme.js` `46e9a0ff…` identical at main and head (old head: `01215cc9…`, `9a4163ed…`). `rd490` `75ed1aa5…`, `rd545` `4711147f…`, `helpers/test-server.js` `bb45cd78…` identical at main and head. `jsonStorage.js:1085` and `:1287` read the S8a anchor and the fallback line. `tests/uat-run.js`: `azurecontainerapps` 1 hit at main, 0 at head; `require.main === module` 1 hit at head. `server.js` at `b8715182`: `:9011` a condition, `:9023` the `logger.info('Risk condition query detected:'` call.
- **Counts** (`git show … | python3 -I`): head `a2f40639…` = 4971/305 (`_updated 2026-10-20T18:32:47.785Z`); main `c050e783…` = 4964/304. `*.test.js` files: 307 at head, 306 at main.
- **Suites touched by the merges** (`git grep`): four test files read `HISTORY.md` (`boot-probe-log-redaction`, `image-content-exposure`, `rd385-shipped-root-markdown-identifiers`, `rd503-shipped-docs-c51-leftovers`; plus a non-test python script); no test names `propose-dark-retheme`; no file under `__tests__ tests scripts` mentions `follow-redirects` (0 matches, control: `package-lock` counts 4/4/2).
- **PR** (`gh api pulls/101`, 20:03:56 and 20:18): open, draft false, head `7c11c78f`, base `b8715182`, 5 commits, 6 files, +147/-15, `mergeable` true, `mergeable_state` `unstable`, `updated_at` 08:55:43Z. Open PRs: #101 and #67. #67: `mergeable` false, `dirty`, files `__tests__/rd777-776-validators-input-filter.test.js`, `backend/validators.js`, the counts file. **The body is unchanged and still stale** (counts 4934/303 -> 4941/304, 4941/4941, the #97/#67 "TURN" sentence, "read after the PR is opened"; no head sha).
- **Check-runs at the new head** (`commits/7c11c78f/check-runs`): `CodeQL` 119131839103, `Analyze (actions)` 119131526451, `Analyze (python)` 119131526086, `Analyze (javascript-typescript)` 119131525926 (completed 08:58:10Z = 19:58:10 AEDT), `scan` 119131539744, `audit-production-deps` x2 119131539952 / 119131516951: **all `completed / success`**. **`build` 119131539751 is `in_progress`** (run `39572998589`, started 19:55:48 AEDT, in step `Run tests (verify gate)`), still `in_progress` at my last read 20:18:35 (about 23 minutes in). Workflow runs for the head: Build (pending), Gitleaks Scan success, npm-audit pull_request and push success, dynamic `PR #101` success, no `Deploy demo` run.
- **Code scanning on the PR ref** (`analyses?ref=` filtered to `commit_sha`; `alerts?state=open&ref=`; `alerts/151/instances?ref=`): analyses javascript-typescript `1995095044` (1 result), python `1995087219` (0), actions `1995086343` (0), tool 2.27.2, no error; open alerts on `refs/pull/101/head` = 1: **#151** `js/file-access-to-http`, warning / medium, `tests/uat-run.js:43`, instance commit `7c11c78f`. On main #151 is open at `:30` (commit `b8715182`); #244 and #245 `fixed` (`fixed_at 2026-10-21T05:17:19Z`). The single-alert GET with `?ref=refs/pull/101/head` still returns main's instance (`:30`): the instrument caveat stands.
- **The old head's Build** (the R2 question): check-run `119024287892` on `5cc06298` is `completed / failure`; run `39539672911` failed in step `Run tests (verify gate)` (job-level read only; I did not read the log). The other seven checks were success. These old ids (`119024…`, analyses `1993686228/1993680404/1993679502`) are void for the new head and the kit says so.
- **Deploy demo** (workflow `333076536`, `actions/workflows/<id>/runs`): newest three are `skipped` (`39548454701` on `940dac40`, `39512084383` on `c139e4a8`, `39463981478` on `115a775b`). **No `Deploy demo` run is listed for main's own head `b8715182`** (the push runs there are Push on main, Build, Gitleaks Scan, npm-audit; Build `39555320727` success). The kit sends this to r7 to name.
- **Floor** (20:04 and 20:18): jest lock base `locks-laptop-1017` has no `nexusai-jest.lock`, `queue-jest/` empty; lock tool sha256 `3c33f5ae…` equals the pin; `vm.loadavg` `{ 2.39 2.41 2.66 }` at 20:04, `{ 5.79 5.33 4.25 }` at 20:18 (my harness run printed 8.02 once at about 20:15); `/Volumes` = Laptop-DEV, Macintosh HD, Recovery (T9 unmounted); `inbox_routing.conf` lines 235-238 = gate30, gate31, gate32, gate29, no gate33 line; `follow-redirects-1.16.1.tgz` and `-1.16.0.tgz` are each listed once in the npm cache index (content blobs UNMEASURED); `models_latest.json` `levels.sonnet.model_id` = `claude-sonnet-5-5` (python `-I`).
- **STATUS files**: `B419_STATUS.md` 128 lines, sha256 `1bcdb4d2e0951dea8180f2508bc02d36699a049a250789f7780f206a24894c23`, last line `READY: #101 7c11c78f… · main b8715182… unchanged · parents … · counts a2f40639… unchanged · main clone status unchanged 34 files · checks started 8/8`. B405, B414, B362 STATUS shas read: `2337f37e…`, `1779aee9…`, `ee30fb95…` (not used as pins).

## Stamp slots left for Tuesday (exactly as B411 had them)
`grep -o -E '@[A-Z][A-Z_0-9]*@'` on the kit prints three hits on two lines (lines 7 and 10):
1. `@STAMP_TIME@`, Stamp paragraph (line 7), and again in the `MAIN-STAMP:` line (line 10): fill both with `YYYY-MM-DD HH:MM AEDT` from `date`, no seconds.
2. `@LAUNCH_AUTH@`, Stamp paragraph (line 7).
3. Not a slot but required: the last line `READ-WHOLE-BY-TUESDAY: PENDING` -> `READ-WHOLE-BY-TUESDAY: DONE <AEDT time> <note>`.
Also before launch (FILL AT STAMP section): re-read main by `ls-remote`; add the routing line `QA/NexusAI-gate33|tuesday-agent@agentmail.to|no` after `inbox_routing.conf:238`; install the launcher; apply the corrected PR-body sentence. No `.pre-stamp` copy was written. No person's name in the kit or launcher (`grep -c -i` of three first/last names = 0 in both, control: the original launcher had one hit, now removed); no other client's name (the only "vision" hit is inside "revision").

## What changed in the kit relative to B411 (a list, not a diff)
Pins: main `c139e4a8` -> `b8715182` (tree `fbef3a20`), head `5cc06298` -> `7c11c78f` (tree `71817e8c`), PR101 base `b8715182`, commits 4 -> 5, `rev-list --left-right` `0 4` -> `0 5`; pane `Datasec/NexusAI-G36`, B-number B420, STATUS and evidence paths `…B420_STATUS.md` / `…B420_evidence/`; routing line position after `:238`; chain is five commits with three merges (WRONG item 1); the escalation triggers gain the third merge (only `HISTORY.md` + `scripts/propose-dark-retheme.js` relative to `5cc06298`); r0 reads each merge against its first parent, the guarded-set test against main only (so `HISTORY.md` in the third merge is not misread), patch equality `c139e4a8..5cc06298` vs `b8715182..7c11c78f`; counts blobs unchanged (head `a2f40639…` 4971/305, main `c050e783…` 4964/304, H1b still expects `PASS 4971/4971 … 305`); the four `HISTORY.md` readers and `propose-dark-retheme` added to WRONG item 8 and r3/r5; the old CodeQL / check-run / Build ids declared void (WRONG item 4, R2); PR-body sentence rewritten for the new head (WRONG item 3); #102/#103 overlap and merge-tree checks marked moot (both landed, ancestors of main), only #67 remains; r4 now waits for "the four legs" (the `CodeQL` check-run plus the three `Analyze (…)` check-runs) and re-runs nothing; r7 names the missing `Deploy demo` run for main's head; r9(f) sets the three Build runs side by side (`39475920383` on `48a17df8`, `39539672911` on `5cc06298`, `39572998589` on `7c11c78f`); R2 restated for the new head's `build` (success / failure / pending each spelled out; no re-run; the old red stays evidence, not a clearance); g33 store refs: drop `p102`/`p103`, add `m2` (old head), `pre` (`c139e4a8`), `root` (`d463f881`); verdict line `B420/PR101 … @ 7c11c78 tree 71817e8` with a "merge 3 = HISTORY.md + propose-dark-retheme.js only" field and "four legs completed", landing checklist "descendant of main … by 5 commits"; launch line uses the pane `Datasec/NexusAI-G36`. Kept verbatim from B411: R1, R3-R7 shapes, T0-T5 forms, MODEL RULE, rows' controls, the `Not tested by this gate:` line, H-rules, HELD, the `READ-WHOLE` last line. Not carried: the "Dependabot" line (a ticket decision, never in a kit).

## Launcher
**Route.** The installed launcher (`fleet/qa-agent/launchers/launch_qa_nexusai_gate33.sh`, sha256 `2882c012…`, 750 lines, mode 644) is still the B359-pinned form: B411's proposed copy `…_repin.sh` was never made. The draft is a full derivation of the INSTALLED file with B411's change list applied to the new head (not a patch on a launcher that does not exist), as `2026-10-21_B420_launch_qa_nexusai_gate33_repin2.sh` beside the kit.

**The exact steps Tuesday runs (after reading the diff and the kit):**
```
cp '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B420_launch_qa_nexusai_gate33_repin2.sh' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate33_repin2.sh'
cmp '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B420_launch_qa_nexusai_gate33_repin2.sh' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate33_repin2.sh'; echo cmp_rc=$?      # must print 0
cmp '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate33.sh' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate33_repin2.sh'; echo control_rc=$?   # must print 1 (the control can fail)
shasum -a 256 '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate33_repin2.sh'    # expect 3ef87589ee5b…ed5f
bash -n '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate33_repin2.sh'; echo bashn_rc=$?   # 0
```
then stamp the kit, add the routing line, `bash '<installed>/launch_qa_nexusai_gate33_repin2.sh' --check` (rc 0 expected; it needs a live `tuesday` pane and at least one builder or QA pane with exactly one claude under it), then `chmod +x`, then the cockpit line in the kit. The installed `launch_qa_nexusai_gate33.sh` stays untouched.

**What I verified on the draft (not a substitute for `--check`):** `bash -n` rc 0. I cut the guards that need no tmux or origin (6, 18M, 7/8, 22, 22M, 93, 93U, 70, 70N, 31, 10/17, 11, 12-20, 41, 82, 19, 24, 53/71, 76/77/79) into a scratch harness with `MAIN_SHA=$BASE` and ran it against the unstamped kit: prints `HARNESS_ALL_TEXT_AND_GIT_GUARDS_PASSED mode=0` (the only output besides it was the load NOTE). Negative controls in the same harness: pin `PATCH_SHA` altered -> `REFUSING: the PR's patch changed across the third merge`; a bogus token added to guard 12's list -> `REFUSING: brief does not declare 'zzz-absent'`. NOT exercised: guards 9, 40, 18T, 18 (stamp, PIN-HEADS parse against a stamped kit, `ls-remote`), 90 (lock queue, uses the live lock base), 38R/86 (tmux), 32S (stamp/route) and the exec tail. The first `--check` is therefore the real test of those.

**Change list, adjusted for the new head (B411 report items 1-9):**
1. `BRIEF` -> the B420 kit; `ROUTE_NAME` kept `QA/NexusAI-gate33`, new `PANE_NAME` `Datasec/NexusAI-G36`; subject unchanged.
2. Pins: `BASE` b8715182 / `BASE_TREE` fbef3a20; new `ROOT` d463f881, `PRE` c139e4a8, `OLD_HEAD` 5cc06298, `M1_SHA` 48a17df8; `HEAD_SHA` 7c11c78f / `HEAD_TREE` 71817e8c; `PATHS_SHA` unchanged (space-joined); `NUMSTAT` unchanged; counts blobs head `a2f40639` (4971 305), base `c050e783` (4964 304), mode-0 M0 counts 4964 304; `LOCK_BLOB` 9cae0533; new `PATCH_SHA` 52081b4c…; PIN-HEADS PR101 commits 5.
3. Chain: five rows `sha tree parents` with the three merges; first-parent chain check; counts 5 / 5 first-parent / 3 merges / left-right `0 5` / ancestry (replaces the linear `= 2` tests); guard 6 and 18M include `ROOT`, `PRE`, `OLD_HEAD`, `M1_SHA`, #97's head and require `PRE`/`ROOT`/#97 in M0's ancestry.
4. New guard 22M: merge 2 = `package-lock.json`; merge 3 = `HISTORY.md scripts/propose-dark-retheme.js`; equals main's own side (`PRE..BASE`); two controls that can fail (`6e947f4..48a17df`, `5cc0629..b8715182`); patch equality with its own control; `HISTORY.md` and `propose-dark-retheme.js` blobs = main's. Guard 93 adds the `jsonStorage.js` blob and the two anchor lines (`:1085` exact line).
5. Guard 31: the B355 READY line check -> the B419 STATUS last line (`READY: #101 <head> · main <BASE> unchanged`); B355/B362/B405/B419 STATUS and the B355 builder brief existence-only; B419 sha NOTE; the B355 PR-TEXT check dropped.
6. Report path: `EXPECT_REPORT` = `…/Briefs/2026-10-21_B420_STATUS.md`; the `Report:` regex now reads `…_STATUS.md`; the brief must name the B420 evidence directory.
7. Prompt rewritten (five commits, three merges, r9, merge content, "THE CI REDS"); guard 12/19/53/71 lists updated (r9, L-R8, `B420/PR101: …[ (CI pending: <names>)] @ 7c11c78 tree 71817e8 `).
8. Stamp regexes unchanged (generic `@[A-Z][A-Z_0-9]*@`; the MAIN-STAMP regex requires `launched YYYY-MM-DD HH:MM AEDT`).
9. 38R/86: `Datasec/NexusAI-F36` added as a candidate builder pane; guard 86 and the QA peer census exclude both the route and pane names.

**Unified diff against the installed launcher** (`diff -U0 installed draft`; the two file paths are abbreviated to `...`; ten very long prompt lines are shown as one-line change notes, marked `[long line]`, because pasting 2-3 KB paragraphs twice would bury the real edits; the full text is `diff -u '<installed>' '<draft>'`, 624 lines, 107,573 bytes, which Tuesday can re-run. The one prompt edit made after this diff was taken, removing a person's first name from the first prompt paragraph, is noted in the first long-line entry):
```
--- .../fleet/qa-agent/launchers/launch_qa_nexusai_gate33.sh
+++ .../tuesday/briefs/2026-10-21_B420_launch_qa_nexusai_gate33_repin2.sh
@@ -2,5 +2,6 @@
-# launch_qa_nexusai_gate33.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 33): a TIER-2 GATE THROUGH CODE, ROUND 1 (not a re-gate), B355 (SEAT-R11)
-# RD-874 + RD-875, PR #101, branch rd-874-875-test-guards-uat-port-r11 @ 6e947f4 (TWO commits over main d463f88; 6 paths, +147/-15) — one gated head, one verdict,
-# ONE report. RD-874 = three settings-plant guards (gate 32's G32-1); RD-875 = tests/uat-run.js has no default target and honours the port (N30-2 / N32).
-# (derived 2026-10-21 by Tuesday's launcher-drafting sub-agent from launch_qa_nexusai_gate32.sh; the drafter ran ONLY `bash -n` and an unstamped `--check` — see
-#  2026-10-21_gate33_LAUNCHER-REPORT.md beside this file. Tuesday stamps the kit, adds the routing line, re-runs `--check`, then chmod +x.)
+# launch_qa_nexusai_gate33_repin2.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 33, RE-PIN 2): a TIER-2 GATE THROUGH CODE, ROUND 1 (not a re-gate), B355 (SEAT-R11)
+# RD-874 + RD-875, PR #101, branch rd-874-875-test-guards-uat-port-r11 @ 7c11c78 (FIVE commits over main b8715182: 2 PR commits + 3 forward merges; 6 paths, +147/-15) — one gated
+# head, one verdict, ONE report. RD-874 = three settings-plant guards (gate 32's G32-1); RD-875 = tests/uat-run.js has no default target and honours the port (N30-2 / N32).
+# DRAFT (2026-10-21 20:0x, Tuesday's brief drafter B420): derived from the INSTALLED launch_qa_nexusai_gate33.sh (750 lines, sha256 2882c012…, the B359-pinned form) by applying the
+# B411/B412 drafter report's launcher change list adjusted for the new head. NOT installed anywhere; Tuesday copies it into fleet/qa-agent/launchers/ as
+# launch_qa_nexusai_gate33_repin2.sh, runs `cmp`, `bash -n`, stamps the kit, adds the routing line, runs `--check`, then `chmod +x`. See the B420 drafter report beside this file.
@@ -8,2 +9,3 @@
-#   PR101 rd-874-875-test-guards-uat-port-r11 @ 6e947f4 (2 commits over d463f88: a7e8f4f RD-874, 6e947f4 RD-875)
-#   M0 = the MAIN pin Tuesday STAMPS (d463f88 at drafting = mode '0': main = the PR's base, the gated tree IS the landing tree). If main has moved at the stamp the
+#   PR101 rd-874-875-test-guards-uat-port-r11 @ 7c11c78 (5 commits: a7e8f4f RD-874, 6e947f4 RD-875, 48a17df merge main 115a775 (PR #97), 5cc0629 merge main c139e4a (PR #104),
+#   7c11c78 merge main b8715182 (PRs #102 + #103); chain root d463f88)
+#   M0 = the MAIN pin Tuesday STAMPS (b8715182 at drafting = mode '0': main = the PR's base, the gated tree IS the landing tree). If main has moved at the stamp the
@@ -12 +14 @@
-# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate33' "bash '.../fleet/qa-agent/launchers/launch_qa_nexusai_gate33.sh'"
+# LAUNCHED ONLY VIA: cockpit.sh add 'Datasec/NexusAI-G36' "bash '.../fleet/qa-agent/launchers/launch_qa_nexusai_gate33_repin2.sh'"
@@ -15,5 +17,4 @@
-# AUTHORITY: Tuesday's gate-33 commission (B359, 2026-10-21), the kit's TIER 2 argument (routing v1.0 row G2: tests-only / tooling follow-up whose mechanism a prior
-# gate already measured) and its ESCALATION RULE (any weakened auth/SCIM test guarantee stops the grading and hands the PR to TIER 1 / Opus).
-# THE MODEL RULE: <first name>, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION.
-# The MODEL is the kit's MODEL line (tier 2, routing v1.0 row G2, Sonnet), which must equal models_latest.json levels.sonnet.model_id (the template ALSO ran on
-# Sonnet: it already read levels.sonnet.model_id — no Opus-to-Sonnet re-point was needed).
+# AUTHORITY: Tuesday's gate-33 commission (B359, re-pinned B411, re-pinned B420, 2026-10-21), the kit's TIER 2 argument (routing v1.0 row G2: tests-only / tooling follow-up
+# whose mechanism a prior gate already measured) and its ESCALATION RULE (any weakened auth/SCIM test guarantee stops the grading and hands the PR to TIER 1 / Opus).
+# THE MODEL RULE: live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION.
+# The MODEL is the kit's MODEL line (tier 2, routing v1.0 row G2, Sonnet), which must equal models_latest.json levels.sonnet.model_id.
@@ -23,18 +24,17 @@
-# PATTERN: launch_qa_nexusai_gate32.sh (prompt EMBEDDED, --check mode, PIN-table parser, C-192 lsr retry, lock-tool pin 90, the LIVE negative-control seat
-# derivation 38R, guard 86, stamp + route refusals LAST) over gate 33's content. CHANGES, each deliberate (full list in the LAUNCHER-REPORT):
-#   - STAMP: the kit's slots are '@MAIN_SHA@' (x2: MAIN-STAMP line + PIN-HEADS MAIN row) and '@STAMP_TIME@' (x1), NOT gate 32's '@SLOT': the placeholder detector is
-#     a generic '@[A-Z][A-Z_0-9]*@' (gate 32's literal-'@SLOT' counter would have counted ZERO slots here and let an unstamped kit launch).
-#   - 40: PIN-HEADS has TWO rows, MAIN + PR101 (branch, head 6e947f4, base d463f88, 2 commits). (gate 32: MAIN + PR98 + GATED.)
-#   - 18: refuses when the branch OR refs/pull/101/head is not 6e947f4.
-#   - 7/8: the chain base d463f88 <- a7e8f4f <- 6e947f4 (2 rows), linear, merge-base = base, first-parent count 2. 22D (the gate-32 delta) is DROPPED.
-#   - 22: the SIX paths (5 M + 1 A) pinned by sha256, numstat table, every blob pinned (head, and main for the 5 M); 5 of 6 are test code/tooling and the 6th is the
-#     counts file; guarded set (backend/ static/ templates/ .github/ bicep/ Dockerfile package*.json HISTORY.md CLARIFICATIONS.md) = 0.
-#   - 93: lockfile, package.json, deploy-demo.yml same blobs at M0 and head and equal their pins; the HEAD counts file is blob 9a723cd = 4941/304; BASE's is a28458a =
-#     4934/303; M0's is READ (in mode 0 it must equal BASE's); deploy-demo gates BOTH jobs at M0; tests/uat-run.js source premises (see 93U).
-#   - 31: the builder's B355 STATUS must end with the READY line for 6e947f4 (sha NOTEd, a CLAIM); the PR-TEXT sha NOTEd; gate 32's report must read COMPLETE and carry G32-1;
-#     gate 32's instruments the kit copies BY NAME are PINNED by sha256 (gate 30's seven + mutant texts and gate 27's instruments are no longer required).
-#   - 12/19/53/71: the kit-declaration lists are REWRITTEN for this kit's own words (rows r0-r8 + r1c, T0-T5, limits L-R1..L-R7 + L-Y1, tags qa-g33-, G33-<n>/N33-<n>,
-#     verdict lines 'B359/PR101: …' and 'LANDING CHECKLIST: PR #101 …').
-#   - DROPPED (gate-32-specific): 22D, the rd407 / html-dom / RD-786-open-site pins, the G30 report/instrument/mutant pins, the 'qa-g32' guards, gate 29/30 brief
-#     requirements, section 3b / 7 / PRIOR ROUND headings (this kit has none), the kit's 'never --first-parent' phrase (the code itself never uses --first-parent for ancestry).
-#   - The PROMPT is rewritten for gate 33 from the KIT (round 1, S8a red-proof, uat-run mutants + no-socket spy, counts, PR text, the TIER-1 escalation).
+# CHANGES against the installed launch_qa_nexusai_gate33.sh (each deliberate; the unified diff is in the B420 drafter report):
+#   - BRIEF -> the B420 kit; the report is a STATUS file in NexusAI's Briefs (guard 10 reads 'Report: `…_STATUS.md`'); PANE_NAME 'Datasec/NexusAI-G36' is added beside ROUTE_NAME
+#     'QA/NexusAI-gate33' (the route name is still what the routing line and the mail subjects use).
+#   - PINS: BASE (= mode-0 main) b8715182 tree fbef3a20; ROOT d463f881 (the chain root); PRE c139e4a8 (main before #102/#103); OLD_HEAD 5cc06298; HEAD 7c11c78f tree 71817e8c;
+#     counts: head a2f40639 = 4971/305, main c050e783 = 4964/304; lockfile blob 9cae0533; patch sha256 52081b4c… (the PR's own diff before and after the third merge).
+#   - 40: PIN-HEADS PR101 now '… | 5 | IN' with base b8715182.
+#   - 6/18M: the commits that must exist now include ROOT, PRE and #97's head; PRE and ROOT must be in M0's ancestry.
+#   - 7/8: the chain is FIVE rows with FULL parent lists (three merges), each row's first parent = the previous row, row 1's parent = ROOT; counts: 5 commits, 5 first-parent,
+#     3 merges, left-right '0 5'.
+#   - 22M (NEW): merge 2 (48a17df -> 5cc0629) = package-lock.json only; merge 3 (5cc0629 -> 7c11c78) = HISTORY.md + scripts/propose-dark-retheme.js only AND equal to main's own side
+#     (PRE..BASE); patch equality sha256(diff PRE OLD_HEAD) = sha256(diff BASE HEAD) = the pin; the two controls that make those checks able to fail.
+#   - 93: lockfile 9cae053 at M0 and the head; jsonStorage.js blob 2abb5cf4 and its two anchor lines; counts 4971/305 (head), 4964/304 (base and, in mode 0, M0).
+#   - 31: the B355 READY-line check is REPLACED by the B419 STATUS last line ('READY: #101 <head> · main <BASE> unchanged'); B355/B362/B405/B419 STATUS and the B355 builder brief
+#     are existence-only; the B355 PR-TEXT file check is DROPPED.
+#   - 12/19/53/71: the kit-declaration lists are updated for the B420 kit's words (row r9, limit L-R8, 'B420/PR101: …[ (CI pending: <names>)] @ 7c11c78' verdict line).
+#   - PROMPT rewritten for the new head (five commits, three merges, main b8715182, r9 CI reds, the merge-content check).
+#   - 38R/86: the candidate builder panes add Datasec/NexusAI-F36; guard 86 and the QA/ peer census exclude BOTH the route name and the pane name.
@@ -47 +47 @@
-# Usage: launch_qa_nexusai_gate33.sh [--check]
+# Usage: launch_qa_nexusai_gate33_repin2.sh [--check]
@@ -58 +58 @@
-# the kit's three at-sign placeholders are '@MAIN_SHA@' x2 and '@STAMP_TIME@' x1; this regex is generic on purpose (any '@NAME@' left = unstamped)
+# the kit's three at-sign placeholders are the stamp time (x2) and the launch authority (x1); this regex is generic on purpose (any '@NAME@' left = unstamped)
@@ -66 +66 @@
-BRIEF="$TBRIEFS/2026-10-21_B359_SEAT-G24_nexusai-gate-pr101-tier2.md"
+BRIEF="$TBRIEFS/2026-10-21_B420_SEAT-G36_nexusai-gate33-pr101-repin2.md"
@@ -81,2 +81,5 @@
-STATUS_B355="$BRIEFS_NX/2026-10-21_B355_STATUS.md"
-PR101TEXT="$BRIEFS_NX/2026-10-21_B355_PR-TEXT.md"
+STATUS_B355="$BRIEFS_NX/2026-10-21_B355_STATUS.md"        # existence only (a CLAIM)
+STATUS_B362="$BRIEFS_NX/2026-10-21_B362_STATUS.md"        # existence only (a CLAIM)
+STATUS_B405="$BRIEFS_NX/2026-10-21_B405_STATUS.md"        # existence only (a CLAIM)
+STATUS_B419="$BRIEFS_NX/2026-10-21_B419_STATUS.md"        # the forward-merge seat's STATUS: its last line is the READY line (a CLAIM, checked)
+B419_STATUS_SHA='1bcdb4d2e0951dea8180f2508bc02d36699a049a250789f7780f206a24894c23'
@@ -107,2 +110,3 @@
-ROUTE_NAME='QA/NexusAI-gate33'
-EXPECT_REPORT="$RPTS/2026-10-21-gate33-b359-pr101/report.md"
+ROUTE_NAME='QA/NexusAI-gate33'          # the answer route / mail-subject name / the routing-line key
+PANE_NAME='Datasec/NexusAI-G36'         # the pane this kit is launched in (the seat label)
+EXPECT_REPORT="$BRIEFS_NX/2026-10-21_B420_STATUS.md"
@@ -113,2 +117,6 @@
-# ---- the pins (cross-checked against the kit's PIN-HEADS, guard 40; each MEASURED 2026-10-21 by read verbs)
-BASE='d463f8817fba925dee7e78c5216df3d5ea8ad073'; BASE_TREE='53d51c59698401237b1b1573fa942bf9f650b51d'   # the PR's base (main when the PR was cut). NB: the KIT has the two tree ids SWAPPED (it calls 53d51c5 the head's); git says base 53d51c5, head eb5fc01 (MEASURED rev-parse)
+# ---- the pins (cross-checked against the kit's PIN-HEADS, guard 40; each MEASURED 2026-10-21 20:0x by read verbs)
+BASE='b8715182808a2c1cf64f009b1a6e23758c63e43a'; BASE_TREE='fbef3a204e1b918a3bfe8c3edf4720516c78ee03'   # the PR's base = main at the stamp (a merge commit: parents b52b46fb #102 and 940dac40 #103)
+ROOT='d463f8817fba925dee7e78c5216df3d5ea8ad073'; ROOT_TREE='53d51c59698401237b1b1573fa942bf9f650b51d'   # the chain root: the first PR commit's parent (main when the PR was cut)
+PRE='c139e4a85d38c0809672efd45b111fefa0cceec4'; PRE_TREE='aeb3b6871fde175e71c22866775802fcb0061139'     # main before #102/#103 = the second merge's main side (PR #104)
+OLD_HEAD='5cc062981f9045bd3a0991a3c53e481748f22478'; OLD_TREE='d88cff88b722b6551db961180e1abaef3242dd43'   # the head gated by NO gate: B411's pin; the third merge's first parent
+M1_SHA='48a17df83847c87d47625611eb3775be259b5362'     # the first merge (main 115a775 = PR #97)
@@ -116 +124 @@
-HEAD_SHA='6e947f4d15411d6b0ac15547addb30799bda0782'; HEAD_TREE='eb5fc01a4ce22237f28f325db0c5292e4d376f1a'   # the head under gate 33 (RD-875 commit)
+HEAD_SHA='7c11c78f174a91ed2a376110966da19e775311e7'; HEAD_TREE='71817e8c6b4f211752ca0d49beaa285f1363f1a4'   # the head under gate 33 (third merge: main b8715182)
@@ -118,5 +126,8 @@
-P97_REF='refs/pull/97/head'; P97_NOTED='115a775b6d5808629f493ef7a3f602d8c5853a22'   # NOTEd only: another mover (S101O); its head is NOT this gate's pin
-P67_REF='refs/pull/67/head'; P67_NOTED='94b288cc64d6348ebd75b502a8712a543358e51b'
-# the chain, oldest first: <full sha> <tree> (each commit's parent is the previous row; row 1's parent is BASE)
-CHAIN='a7e8f4f9e280e13f8de4a5c211ab39a6746461ac 3358d239b4edc08a810fc1a3d7160b677160dd98
-6e947f4d15411d6b0ac15547addb30799bda0782 eb5fc01a4ce22237f28f325db0c5292e4d376f1a'
+P97_REF='refs/pull/97/head'; P97_NOTED='115a775b6d5808629f493ef7a3f602d8c5853a22'   # LANDED; its ref is NOTEd only (the first merge's second parent)
+P67_REF='refs/pull/67/head'; P67_NOTED='94b288cc64d6348ebd75b502a8712a543358e51b'   # the one other open PR (dirty); NOTEd only
+# the chain, oldest first: <full sha> <tree> <parents, comma-joined> (row 1's first parent is ROOT; every later row's FIRST parent is the previous row)
+CHAIN='a7e8f4f9e280e13f8de4a5c211ab39a6746461ac 3358d239b4edc08a810fc1a3d7160b677160dd98 d463f8817fba925dee7e78c5216df3d5ea8ad073
+6e947f4d15411d6b0ac15547addb30799bda0782 eb5fc01a4ce22237f28f325db0c5292e4d376f1a a7e8f4f9e280e13f8de4a5c211ab39a6746461ac
+48a17df83847c87d47625611eb3775be259b5362 bb71baa06d8ef6d4c28f0c651091e591106fd703 6e947f4d15411d6b0ac15547addb30799bda0782,115a775b6d5808629f493ef7a3f602d8c5853a22
+5cc062981f9045bd3a0991a3c53e481748f22478 d88cff88b722b6551db961180e1abaef3242dd43 48a17df83847c87d47625611eb3775be259b5362,c139e4a85d38c0809672efd45b111fefa0cceec4
+7c11c78f174a91ed2a376110966da19e775311e7 71817e8c6b4f211752ca0d49beaa285f1363f1a4 5cc062981f9045bd3a0991a3c53e481748f22478,b8715182808a2c1cf64f009b1a6e23758c63e43a'
@@ -124 +135,7 @@
-PATHS_SHA='f4db97c617800403ec8a35133455733c22aaadb7a63d76f1b5d8a2a05797795c'   # sha256 of the sorted, space-joined 6-path list (git diff --name-only BASE HEAD)
+PATHS_SHA='f4db97c617800403ec8a35133455733c22aaadb7a63d76f1b5d8a2a05797795c'   # sha256 of the sorted, SPACE-joined 6-path list (git diff --name-only BASE HEAD); the newline-joined form is 55ad421b…
+PATCH_SHA='52081b4cb20159e6c84d400e18477c6bac9e9f2825c8cb5fa1aaf26177a0530a'    # sha256 of git diff PRE OLD_HEAD = of git diff BASE HEAD (the PR's own patch, before and after the third merge)
+MERGE2_PATHS='package-lock.json'
+MERGE3_PATHS='HISTORY.md scripts/propose-dark-retheme.js'
+HIST='HISTORY.md'; HIST_BLOB='fd4552161832a49f0180acf22dd47bb4c6d85abf'
+DARK='scripts/propose-dark-retheme.js'; DARK_BLOB='46e9a0ff156476eea4679d4a39d68c8a4f8d2a13'
+JS='backend/jsonStorage.js'; JS_BLOB='2abb5cf487d75f2ce1730a028ade1b39cde31fd2'
@@ -130 +147 @@
-scripts/verify-expected-counts.json 9a723cdc3bec7d2863b6501cc52928ec93760efc a28458adef1e24416865a425201dc4bc840f9f30
+scripts/verify-expected-counts.json a2f40639f40ce312d8e8bff8e7f5fd1afe22a5b4 c050e78328616b96862512739e8cffc6b4a6e603
@@ -140 +157 @@
-COUNTS_FILE='scripts/verify-expected-counts.json'; COUNTS_BLOB_HEAD='9a723cdc3bec7d2863b6501cc52928ec93760efc'; COUNTS_BLOB_BASE='a28458adef1e24416865a425201dc4bc840f9f30'
+COUNTS_FILE='scripts/verify-expected-counts.json'; COUNTS_BLOB_HEAD='a2f40639f40ce312d8e8bff8e7f5fd1afe22a5b4'; COUNTS_BLOB_BASE='c050e78328616b96862512739e8cffc6b4a6e603'
@@ -142 +159 @@
-LOCK='package-lock.json'; LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
+LOCK='package-lock.json'; LOCK_BLOB='9cae05330520966bac5535ce713ab994ba6abe35'
@@ -145 +162,2 @@
-# counts file; THIS PR legitimately edits it (it is one of the six), so it is excluded here and pinned by blob / numstat / counts instead.
+# counts file; THIS PR legitimately edits it (it is one of the six), so it is excluded here and pinned by blob / numstat / counts instead. The guarded set is applied to
+# BASE..HEAD (against MAIN), never to OLD_HEAD..HEAD: HISTORY.md is main's own file in the third merge (guard 22M reads that diff by its exact two paths).
@@ -165,0 +184 @@
+patch_sha() { g diff --binary "$1" "$2" 2>/dev/null | shasum -a 256 | cut -d' ' -f1; }
@@ -199 +218 @@
-[long line, 2475 chars] You are the fleet QA/testing agent ... gate 33: a TIER-2 GATE ... (item: 6e947f4, TWO commits over d463f881, PR #97/#67 not mentioned)
+[long line, 3042 chars] same opening, rewritten for the new head: five commits and three forward merges (48a17df main 115a775 = PR #97; 5cc0629 main c139e4a = PR #104; 7c11c78 main b8715182 = PRs #102/#103), main b8715182 tree fbef3a20, head tree 71817e8c, chain root and old-head trees named; a possessive first name before "Mac mini" removed (edited after this diff was taken)
@@ -201,2 +220,2 @@
-READ YOUR COMMISSION FIRST, whole: .../tuesday/briefs/2026-10-21_B359_SEAT-G24_nexusai-gate-pr101-tier2.md
+READ YOUR COMMISSION FIRST, whole: .../tuesday/briefs/2026-10-21_B420_SEAT-G36_nexusai-gate33-pr101-repin2.md
-[long line] It opens with the item, ... the builder's STATUS (read WHOLE; a CLAIM) ... the carried rulings and THE MODEL RULE ... (r0 to r8 and r1c) ...
+[long line] ... the builders' STATUS files (read WHOLE; CLAIMS) ... the carried rulings R1 to R7 (R2 is the CI reds) and THE MODEL RULE ... (r0 to r9 and r1c) ...
@@ -204 +223 @@
-[long line] THE ESCALATION RULE (binding, ...) ... ESCALATED TO TIER 1, not GO or NO GO. That escalation hands the PR to a new tier-1 gate; ...
+[long line] same, with one added sentence before "That escalation hands the PR ...": "The same escalation follows a path beyond the six in the diff against main, a second merge (5cc0629) that carries more than package-lock.json relative to 48a17df, and a third merge (7c11c78) that carries more than HISTORY.md and scripts/propose-dark-retheme.js relative to 5cc0629."
@@ -206 +225 @@
-[long line] THE MODEL RULE (<first name>, live board 2026-09-30 09:07, card (b)): ... (the mutants are one-line renames, a port number, a boolean and a deleted guard). ...
+[long line] THE MODEL RULE (live board 2026-09-30 09:07, card (b)): ... (... a deleted guard; the CI-red plants are a local listener and a local connection). ...
@@ -208 +227 @@
-[long line, 2434 chars] THE PROPERTIES ... (1) DELTA AND SCOPE (r0): two commits ...
+[long line, 3247 chars] THE PROPERTIES ... (1) DELTA AND SCOPE (r0): five commits ... MERGE CONTENT ...; (4) counts 4971/305 vs main 4964/304; (5) all four code-scanning legs; (6) overlap with PR #67 only; (10) THE CI REDS (r9, R2)
@@ -210 +229 @@
-[long line] MAIN MUST NOT MOVE: ... that d463f881 is in its ancestry ... what landed since d463f881 ... (PR #97 from S101O and PR #67 are the likeliest movers, and both also edit the counts file) ...
+[long line] MAIN MUST NOT MOVE: ... that d463f881 and c139e4a8 are in its ancestry ... what landed since b8715182 ... (PR #67 is the only other open PR and also edits the counts file) ...
@@ -214 +233 @@
-[long line, 1756 chars] THE LOCK (C-63) ... SHARED with gate 29 (QA/NexusAI-gate29, LIVE ...), S101O, any landing hold and the builders ... (the floor read 10 to 17 at drafting, so expect to wait)
+[long line, 1630 chars] THE LOCK (C-63) ... SHARED with any landing hold, other gates and the builders ... over 8, poll every 20 s and log each wait.
@@ -216 +235 @@
-[long line] NODE_MODULES WITHOUT THE HOST REGISTRY ... share lock 19477a9 (the PR touches no package file) ... an ENOTCACHED is NOT RUN ...
+[long line] ... share lock 9cae053 (the PR touches no package file; the lock bump to follow-redirects 1.16.1 came in with main) ... an ENOTCACHED (the one new tarball is follow-redirects 1.16.1) is NOT RUN ...
@@ -218 +237 @@
-[long line, 1586 chars] FLOOR DISCIPLINE ... (r0, r1c, r4, r5 a to c, r6 ...) ... expect VERDICT: PASS — 4941/4941 tests passed across 304 suites ... expect 4941/304 ...
+[long line, 1610 chars] FLOOR DISCIPLINE ... (r0, r1c, r4, r5, r6, r7, r8, r9 a and b ...) H4 includes the r9 plants ... expect VERDICT: PASS — 4971/4971 tests passed across 305 suites ... expect 4971/305 ...
@@ -220 +239 @@
-[long line, 1770 chars] THE INSTRUMENT RULES H-1 TO H-36 ... "the builder's evidence"/"the builder's session-tools files" ...
+[long line, 1770 chars] same, "the builders' ..." in those places
@@ -222 +241 @@
-[long line, 1893 chars] TREES AND WRITES ... refs g33/m0, g33/head, g33/c1, and g33/p97 and g33/p67 ... (LIVE: the builders' and S101O's) ... (S101O may be live)
+[long line, 2019 chars] TREES AND WRITES ... refs g33/m0, g33/head, g33/c1, g33/c2, g33/m1, g33/m2, g33/pre, g33/root, and g33/p97 and g33/p67 ... (LIVE: the builders' and the forward-merge seat's; the root checkout carries modified files that are not yours) ... (a seat may be live) ... EXCLUSIVE ... R9
@@ -224 +243 @@
-[long line] RE-PIN at start, mid and end: ... (and refs/pull/97/head and refs/pull/67/head, the other movers) ...
+[long line] ... (and refs/pull/97/head and refs/pull/67/head, the noted refs) ...
@@ -226 +245 @@
-[long line] QUESTIONS: your routing name is QA/NexusAI-gate33. If you must ask, ...
+[long line] QUESTIONS: your routing name is QA/NexusAI-gate33 and your pane is Datasec/NexusAI-G36. If you must ask, ...
@@ -232 +251 @@
-[long line] Lead the body with the TWO lines ... the B359/PR101 verdict line and the LANDING CHECKLIST line ...
+[long line] ... the B420/PR101 verdict line and the LANDING CHECKLIST line ...
@@ -237 +256 @@
-[long line] Rule 2 stands: ... carrying the builder's stated limits, every declared limit L-R1 to L-R7 and L-Y1 ...
+[long line] ... carrying the builders' stated limits, every declared limit L-R1 to L-R8 and L-Y1 ...
@@ -285,2 +304,2 @@
-[ "$(pfld "$PIN" PR101 3)" = "$BR" ] && [ "$(pfld "$PIN" PR101 4)" = "$HEAD_SHA" ] && [ "$(pfld "$PIN" PR101 5)" = "$BASE" ] && [ "$(pfld "$PIN" PR101 6)" = "2" ] \
-  || { echo "REFUSING: PIN-HEADS PR101 is not $BR @ 6e947f4, base d463f88, 2 commits — re-pin kit AND launcher" >&2; exit 40; }
+[ "$(pfld "$PIN" PR101 3)" = "$BR" ] && [ "$(pfld "$PIN" PR101 4)" = "$HEAD_SHA" ] && [ "$(pfld "$PIN" PR101 5)" = "$BASE" ] && [ "$(pfld "$PIN" PR101 6)" = "5" ] \
+  || { echo "REFUSING: PIN-HEADS PR101 is not $BR @ 7c11c78, base b8715182, 5 commits — re-pin kit AND launcher" >&2; exit 40; }
@@ -318,4 +337,4 @@
-[ "$(ref_now "refs/heads/$BR")" = "$HEAD_SHA" ] || { echo "REFUSING: origin $BR is '$(ref_now "refs/heads/$BR")', not 6e947f4 — the head MOVED; re-pin kit AND launcher (a new head is a new kit amendment and a new CodeQL run)" >&2; exit 18; }
-[ "$(ref_now "$PR_REF")" = "$HEAD_SHA" ] || { echo "REFUSING: $PR_REF is '$(ref_now "$PR_REF")', not 6e947f4 — PR #101 moved (or the ref is unreadable); re-pin kit AND launcher" >&2; exit 18; }
-[ "$(ref_now "$P97_REF")" = "$P97_NOTED" ] || echo "NOTE: $P97_REF is '$(ref_now "$P97_REF")', not the drafter's ${P97_NOTED:0:8} — PR #97 (another mover, also edits the counts file) moved; the gate re-reads it (r5)" >&2
-[ "$(ref_now "$P67_REF")" = "$P67_NOTED" ] || echo "NOTE: $P67_REF is '$(ref_now "$P67_REF")', not the drafter's ${P67_NOTED:0:8} — PR #67 (another mover, also edits the counts file) moved; the gate re-reads it (r5)" >&2
+[ "$(ref_now "refs/heads/$BR")" = "$HEAD_SHA" ] || { echo "REFUSING: origin $BR is '$(ref_now "refs/heads/$BR")', not 7c11c78 — the head MOVED; re-pin kit AND launcher (a new head is a new kit amendment and a new CodeQL run)" >&2; exit 18; }
+[ "$(ref_now "$PR_REF")" = "$HEAD_SHA" ] || { echo "REFUSING: $PR_REF is '$(ref_now "$PR_REF")', not 7c11c78 — PR #101 moved (or the ref is unreadable); re-pin kit AND launcher" >&2; exit 18; }
+[ "$(ref_now "$P97_REF")" = "$P97_NOTED" ] || echo "NOTE: $P97_REF is '$(ref_now "$P97_REF")', not the drafter's ${P97_NOTED:0:8} — PR #97 landed long ago; its ref moved, which the gate re-reads (r5)" >&2
+[ "$(ref_now "$P67_REF")" = "$P67_NOTED" ] || echo "NOTE: $P67_REF is '$(ref_now "$P67_REF")', not the drafter's ${P67_NOTED:0:8} — PR #67 (the other open PR, also edits the counts file) moved; the gate re-reads it (r5)" >&2
@@ -326 +345 @@
-for S in "$MAIN_SHA" "$BASE" $CHAIN_SHAS; do
+for S in "$MAIN_SHA" "$BASE" "$ROOT" "$PRE" "$OLD_HEAD" "$M1_SHA" "$P97_NOTED" $CHAIN_SHAS; do
@@ -332,2 +351,7 @@
-[ "$(tree_of "$BASE")" = "$BASE_TREE" ] || { echo "REFUSING: d463f88 is not tree 53d51c5 (the measured main)" >&2; exit 18; }
-g merge-base --is-ancestor "$BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: d463f88 is not in M0 ${MAIN_SHA:0:7}'s ANCESTRY — M0 is not a descendant of the PR's base d463f88" >&2; exit 18; }
+[ "$(tree_of "$BASE")" = "$BASE_TREE" ] || { echo "REFUSING: b8715182 is not tree fbef3a2 (the measured main)" >&2; exit 18; }
+[ "$(tree_of "$ROOT")" = "$ROOT_TREE" ] && [ "$(tree_of "$PRE")" = "$PRE_TREE" ] && [ "$(tree_of "$OLD_HEAD")" = "$OLD_TREE" ] \
+  || { echo "REFUSING: the chain root d463f88 / the previous main c139e4a / the old head 5cc0629 do not carry the measured trees (53d51c5 / aeb3b68 / d88cff8)" >&2; exit 18; }
+g merge-base --is-ancestor "$BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: b8715182 is not in M0 ${MAIN_SHA:0:7}'s ANCESTRY — M0 is not a descendant of the PR's base b8715182" >&2; exit 18; }
+for S in "$PRE" "$ROOT" "$P97_NOTED"; do
+  g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: ${S:0:7} (the chain root, the previous main or PR #97's head) is not in M0 ${MAIN_SHA:0:7}'s ancestry" >&2; exit 18; }
+done
@@ -347 +371 @@
-  echo "NOTE: M0 ${MAIN_SHA:0:7} is $LANDED_N commit(s) past d463f88 — what landed: $LANDED — T0 applies (mode moved: the gated tree is the head; the merged tree is r5(d), hold qa-g33-H3)" >&2
+  echo "NOTE: M0 ${MAIN_SHA:0:7} is $LANDED_N commit(s) past b8715182 — what landed: $LANDED — T0 applies (mode moved: the gated tree is the head; the merged tree is r5(d), hold qa-g33-H3)" >&2
@@ -349 +373 @@
-  [ -z "$OVERLAP" ] || { echo "REFUSING: what landed since d463f88 touches PR #101 path(s) '$OVERLAP' — T0: STOP and mail a QUESTION; re-brief (a landed PR #97 / #67 touches the counts file: expected, and a re-stamp)" >&2; exit 18; }
+  [ -z "$OVERLAP" ] || { echo "REFUSING: what landed since b8715182 touches PR #101 path(s) '$OVERLAP' — T0: STOP and mail a QUESTION; re-brief (a landed PR #67 touches the counts file: expected, and a re-stamp)" >&2; exit 18; }
@@ -354 +378 @@
-  [ -z "$MC0" ] || { echo "REFUSING: the legacy merge-tree of 6e947f4 onto M0 shows conflict markers in '$MC0' — T0: STOP; re-brief" >&2; exit 18; }
+  [ -z "$MC0" ] || { echo "REFUSING: the legacy merge-tree of 7c11c78 onto M0 shows conflict markers in '$MC0' — T0: STOP; re-brief" >&2; exit 18; }
@@ -360,3 +384,3 @@
-# 7 / 8 — the head's chain: d463f88 <- a7e8f4f <- 6e947f4, oldest first, each parent = the previous row, EVERY tree; linear; the gated head is row 2.
-PREV="$BASE"
-while read -r CSHA CTREE; do
+# 7 / 8 — the head's chain: d463f88 <- a7e8f4f <- 6e947f4 <- 48a17df(+115a775) <- 5cc0629(+c139e4a) <- 7c11c78(+b8715182), oldest first, FULL parent lists, EVERY tree; the gated head is row 5.
+PREV="$ROOT"
+while read -r CSHA CTREE CPAR; do
@@ -364 +388,2 @@
-  [ "$(parents_of "$CSHA")" = "$PREV" ] || { echo "REFUSING: the parent of ${CSHA:0:7} is '$(parents_of "$CSHA")', not ${PREV:0:7} — the chain is not the briefed 2 linear commits" >&2; exit 7; }
+  [ "$(parents_of "$CSHA")" = "${CPAR//,/ }" ] || { echo "REFUSING: the parents of ${CSHA:0:7} are '$(parents_of "$CSHA")', not '${CPAR//,/ }' — the chain is not the briefed 5 commits with 3 merges" >&2; exit 7; }
+  [ "${CPAR%%,*}" = "$PREV" ] || { echo "REFUSING: the first parent of ${CSHA:0:7} is '${CPAR%%,*}', not the previous chain row ${PREV:0:7}" >&2; exit 7; }
@@ -371,4 +396,8 @@
-  || { echo "REFUSING: the chain does not end at 6e947f4 tree eb5fc01" >&2; exit 8; }
-[ "$(g merge-base "$HEAD_SHA" "$BASE" 2>/dev/null)" = "$BASE" ] && [ "$(g rev-list --count "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "2" ] \
-  && [ "$(g rev-list --count --first-parent "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "2" ] \
-  || { echo "REFUSING: 6e947f4 is not 2 linear commits over d463f88 (merge-base, count, first-parent count)" >&2; exit 8; }
+  || { echo "REFUSING: the chain does not end at 7c11c78 tree 71817e8" >&2; exit 8; }
+g merge-base --is-ancestor "$BASE" "$HEAD_SHA" 2>/dev/null \
+  && [ "$(g merge-base "$HEAD_SHA" "$BASE" 2>/dev/null)" = "$BASE" ] \
+  && [ "$(g rev-list --count "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "5" ] \
+  && [ "$(g rev-list --count --first-parent "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "5" ] \
+  && [ "$(g rev-list --count --merges "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "3" ] \
+  && [ "$(g rev-list --left-right --count "${BASE}...${HEAD_SHA}" 2>/dev/null | tr '\t' ' ')" = "0 5" ] \
+  || { echo "REFUSING: 7c11c78 is not 5 commits (3 merges) over b8715182 (descendant, merge-base, count, first-parent count, merge count, left-right 0 5)" >&2; exit 8; }
@@ -396 +425 @@
-# 22 — the SIX paths (5 M + 1 A): the list PINNED, numstat and every blob PINNED, five of six test code/tooling and the sixth the counts file, none in the guarded set.
+# 22 — the SIX paths (5 M + 1 A) against MAIN (BASE..HEAD): the list PINNED, numstat and every blob PINNED, five of six test code/tooling and the sixth the counts file, none in the guarded set.
@@ -401 +430 @@
-[ "$(printf '%s' "$(printf '%s\n' "$PL" | tr '\n' ' ' | sed 's/ $//')" | shasum -a 256 | cut -d' ' -f1)" = "$PATHS_SHA" ] || { echo "REFUSING: the sorted 6-path list's sha256 is not ${PATHS_SHA:0:12}… — the PR's file set moved" >&2; exit 22; }
+[ "$(printf '%s' "$(printf '%s\n' "$PL" | tr '\n' ' ' | sed 's/ $//')" | shasum -a 256 | cut -d' ' -f1)" = "$PATHS_SHA" ] || { echo "REFUSING: the sorted, space-joined 6-path list's sha256 is not ${PATHS_SHA:0:12}… — the PR's file set moved" >&2; exit 22; }
@@ -409 +438 @@
-  [ "$(blob "$HEAD_SHA" "$PP")" = "$PH" ] || { echo "REFUSING: $PP is not blob ${PH:0:8} at 6e947f4" >&2; exit 22; }
+  [ "$(blob "$HEAD_SHA" "$PP")" = "$PH" ] || { echo "REFUSING: $PP is not blob ${PH:0:8} at 7c11c78" >&2; exit 22; }
@@ -411 +440 @@
-    [ -z "$(blob "$BASE" "$PP")" ] || { echo "REFUSING: $PP exists at d463f88 — it is briefed as ADDED" >&2; exit 22; }
+    [ -z "$(blob "$BASE" "$PP")" ] || { echo "REFUSING: $PP exists at b8715182 — it is briefed as ADDED" >&2; exit 22; }
@@ -413 +442 @@
-    [ "$(blob "$BASE" "$PP")" = "$PM" ] || { echo "REFUSING: $PP is not blob ${PM:0:8} at d463f88" >&2; exit 22; }
+    [ "$(blob "$BASE" "$PP")" = "$PM" ] || { echo "REFUSING: $PP is not blob ${PM:0:8} at b8715182" >&2; exit 22; }
@@ -419 +448,16 @@
-# 93 — the premises at source: lockfile, package.json and workflow the SAME blobs at M0 and the head and equal the pins; the counts (BASE 4934/303, HEAD 4941/304, M0 READ); deploy gate.
+# 22M (NEW) — what the three merges carry: merge 2 = package-lock.json only; merge 3 = HISTORY.md + scripts/propose-dark-retheme.js only AND equal to main's own side; the PR's own
+# patch byte-identical before and after (the third merge); each check has a control that can fail. A failure here is a Blocker AND a TIER-1 ESCALATION trigger in the kit: REFUSE.
+[ "$(paths_of "$M1_SHA" "$OLD_HEAD")" = "$MERGE2_PATHS" ] || { echo "REFUSING: merge 2 (48a17df -> 5cc0629) carries '$(paths_of "$M1_SHA" "$OLD_HEAD")', not '$MERGE2_PATHS' — the kit's escalation trigger" >&2; exit 22; }
+[ "$(paths_of "$OLD_HEAD" "$HEAD_SHA")" = "$MERGE3_PATHS" ] || { echo "REFUSING: merge 3 (5cc0629 -> 7c11c78) carries '$(paths_of "$OLD_HEAD" "$HEAD_SHA")', not '$MERGE3_PATHS' — the kit's escalation trigger" >&2; exit 22; }
+[ "$(paths_of "$PRE" "$BASE")" = "$MERGE3_PATHS" ] || { echo "REFUSING: main's own side (c139e4a -> b8715182) is '$(paths_of "$PRE" "$BASE")', not '$MERGE3_PATHS'" >&2; exit 22; }
+CTL2="$(paths_of 6e947f4d15411d6b0ac15547addb30799bda0782 "$M1_SHA")"      # a known multi-path diff: the merge-2 test must be able to FAIL on it
+[ -n "$CTL2" ] && [ "$CTL2" != "$MERGE2_PATHS" ] || { echo "REFUSING: the merge-2 control (6e947f4 -> 48a17df, a multi-path diff) read '$CTL2' — the check cannot fail (C-40)" >&2; exit 22; }
+CTL3="$(paths_of "$OLD_HEAD" "$BASE")"                                      # old head vs main = the six PR paths + main's two = more than two paths
+[ "$(printf '%s\n' "$CTL3" | wc -w | tr -d ' ')" -gt 2 ] || { echo "REFUSING: the merge-3 control (5cc0629 -> b8715182) read '$CTL3' — the check cannot fail (C-40)" >&2; exit 22; }
+PS_OLD="$(patch_sha "$PRE" "$OLD_HEAD")"; PS_NEW="$(patch_sha "$BASE" "$HEAD_SHA")"
+[ "$PS_OLD" = "$PATCH_SHA" ] && [ "$PS_NEW" = "$PATCH_SHA" ] || { echo "REFUSING: the PR's patch changed across the third merge (c139e4a..5cc0629 sha256 ${PS_OLD:0:12}…, b8715182..7c11c78 sha256 ${PS_NEW:0:12}…, pin ${PATCH_SHA:0:12}…)" >&2; exit 22; }
+[ "$(patch_sha "$BASE" "$OLD_HEAD")" != "$PATCH_SHA" ] || { echo "REFUSING: the patch-equality control (b8715182..5cc0629, which includes main's two paths) equals the pin — the check cannot fail (C-40)" >&2; exit 22; }
+[ "$(blob "$HEAD_SHA" "$HIST")" = "$HIST_BLOB" ] && [ "$(blob "$BASE" "$HIST")" = "$HIST_BLOB" ] && [ "$(blob "$HEAD_SHA" "$DARK")" = "$DARK_BLOB" ] && [ "$(blob "$BASE" "$DARK")" = "$DARK_BLOB" ] \
+  || { echo "REFUSING: HISTORY.md / scripts/propose-dark-retheme.js are not main's blobs (fd45521 / 46e9a0f) at the head — the third merge carries more than main's side" >&2; exit 22; }
+
+# 93 — the premises at source: lockfile, package.json, workflow and jsonStorage.js the SAME blobs at M0 and the head and equal the pins; the counts (BASE 4964/304, HEAD 4971/305, M0 READ); deploy gate.
@@ -421,2 +465,2 @@
-  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] \
-    || { echo "REFUSING: ${S:0:7} does not carry lockfile 19477a9 / package.json 384805d / deploy-demo.yml 953b2a2 (ruling m, r0, r7)" >&2; exit 93; }
+  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] && [ "$(blob "$S" "$JS")" = "$JS_BLOB" ] \
+    || { echo "REFUSING: ${S:0:7} does not carry lockfile 9cae053 / package.json 384805d / deploy-demo.yml 953b2a2 / jsonStorage.js 2abb5cf (ruling m, r0, r7, r1)" >&2; exit 93; }
@@ -424,3 +468,7 @@
-[ "$(blob "$HEAD_SHA" "$COUNTS_FILE")" = "$COUNTS_BLOB_HEAD" ] && [ "$(counts_at "$HEAD_SHA")" = "4941 304" ] || { echo "REFUSING: the head's counts file is not blob 9a723cd = 4941/304 (+7 cells, +1 suite)" >&2; exit 93; }
-[ "$(blob "$BASE" "$COUNTS_FILE")" = "$COUNTS_BLOB_BASE" ] && [ "$(counts_at "$BASE")" = "4934 303" ] || { echo "REFUSING: the base's counts file is not blob a28458a = 4934/303" >&2; exit 93; }
-[ "$MODE" != "0" ] || [ "$M0_COUNTS" = "4934 303" ] || { echo "REFUSING: mode 0 but M0's counts file reads '$M0_COUNTS', not 4934 303" >&2; exit 93; }
+[ "$(cntF "$HEAD_SHA" "$JS" "this.settingsFile = path.join(dataDir, 'settings.json');")" = "1" ] && [ "$(cntF "$HEAD_SHA" "$JS" "this.settingsFile = path.join(fallbackDir, 'settings.json');")" = "1" ] \
+  || { echo "REFUSING: jsonStorage.js at the head lacks the S8a anchor at :1085 or the fallback line at :1287 (r1)" >&2; exit 93; }
+[ "$(g show "${HEAD_SHA}:${JS}" 2>/dev/null | sed -n '1085p' | grep -cF "this.settingsFile = path.join(dataDir, 'settings.json');")" = "1" ] \
+  || { echo "REFUSING: the S8a anchor is not at jsonStorage.js:1085 at the head (r1)" >&2; exit 93; }
+[ "$(blob "$HEAD_SHA" "$COUNTS_FILE")" = "$COUNTS_BLOB_HEAD" ] && [ "$(counts_at "$HEAD_SHA")" = "4971 305" ] || { echo "REFUSING: the head's counts file is not blob a2f40639 = 4971/305 (+7 cells, +1 suite)" >&2; exit 93; }
+[ "$(blob "$BASE" "$COUNTS_FILE")" = "$COUNTS_BLOB_BASE" ] && [ "$(counts_at "$BASE")" = "4964 304" ] || { echo "REFUSING: main's counts file is not blob c050e783 = 4964/304" >&2; exit 93; }
+[ "$MODE" != "0" ] || [ "$M0_COUNTS" = "4964 304" ] || { echo "REFUSING: mode 0 but M0's counts file reads '$M0_COUNTS', not 4964 304" >&2; exit 93; }
@@ -449 +497 @@
-[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as the builder read (T4) — the gate records it" >&2
+[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as the builders read (T4) — the gate records it" >&2
@@ -455,2 +503,2 @@
-# 31 — the builder's STATUS (a CLAIM; ends with the READY line for the head), the PR text, gate 32's report/instruments (PINNED), standing references.
-for f in "$STATUS_B355" "$PR101TEXT" "$BRIEF_B355" "$CLAR" "$BRIEF32" "$TEMPLATE" "$G32_REPORT" "$CHARTER" \
+# 31 — the builders' STATUS files (CLAIMS; existence only, except B419's last line = the READY line for the head), gate 32's report/instruments (PINNED), standing references.
+for f in "$STATUS_B355" "$STATUS_B362" "$STATUS_B405" "$STATUS_B419" "$BRIEF_B355" "$CLAR" "$BRIEF32" "$TEMPLATE" "$G32_REPORT" "$CHARTER" \
@@ -464,3 +512,3 @@
-tail -n 1 "$STATUS_B355" | grep -qF "READY FOR QA: B355 RD-874 + RD-875 @ $HEAD_SHA" || { echo "REFUSING: the builder's B355 STATUS no longer ends with the READY line for 6e947f4" >&2; exit 31; }
-[ "$(fsha "$STATUS_B355")" = "40f080ef8ff805464de712919d3177b43f2e47e39bb733e6240b955fb09b8546" ] || echo "NOTE: the builder's B355 STATUS sha256 is not the drafter's 40f080ef… (the file is a CLAIM and changed since drafting; the gate reads it WHOLE)" >&2
-[ "$(fsha "$PR101TEXT")" = "b8c5cfd0e5617ff3114c5d7b3fba244056222e639f1b33ae4895e03584072260" ] || echo "NOTE: the B355 PR-TEXT sha256 is not the drafter's b8c5cfd0… (the gate's r6 compares the LIVE PR body, not this file alone)" >&2
+sed '/^[[:space:]]*$/d' "$STATUS_B419" | tail -n 1 | grep -qF "READY: #101 $HEAD_SHA · main $BASE unchanged" \
+  || { echo "REFUSING: the forward-merge seat's B419 STATUS no longer ends with the READY line for 7c11c78 on main b8715182" >&2; exit 31; }
+[ "$(fsha "$STATUS_B419")" = "$B419_STATUS_SHA" ] || echo "NOTE: the B419 STATUS sha256 is not the drafter's 1bcdb4d2… (the file is a CLAIM and changed since drafting; the gate reads it WHOLE)" >&2
@@ -477,2 +525,2 @@
-# 10 / 17 — the report path from the brief's §11; no stale report; the brief names its sources.
-REPORT="$(grep -oE 'Report: `[^`]*/report\.md`' "$BRIEF" | head -1 | sed -E 's/^Report: `//; s/`$//')"
+# 10 / 17 — the report path from the brief's §11 (a STATUS file in NexusAI's Briefs); no stale report; the brief names its sources.
+REPORT="$(grep -oE 'Report: `[^`]*_STATUS\.md`' "$BRIEF" | head -1 | sed -E 's/^Report: `//; s/`$//')"
@@ -482,2 +530,3 @@
-for P in "2026-10-20_B336_SEAT-G23_nexusai-gate32-pr98-round2.md" "2026-10-21_B355_SEAT-R11_nexusai-rd874-rd875.md" "2026-10-21_B355_STATUS.md" "2026-10-21_B355_PR-TEXT.md" \
-         "2026-10-20-gate32-b336-pr98-r2" "ADDENDUM-1" "qa-file32.sh" "qa-applymut.py" "qa-netbelt.sb" \
+[ ! -e "$BRIEFS_NX/2026-10-21_B420_evidence" ] || echo "NOTE: $BRIEFS_NX/2026-10-21_B420_evidence already exists — the gate reads it before it writes (never overwrite another run's evidence)" >&2
+for P in "2026-10-20_B336_SEAT-G23_nexusai-gate32-pr98-round2.md" "2026-10-21_B355_SEAT-R11_nexusai-rd874-rd875.md" "2026-10-21_B355_STATUS.md" "2026-10-21_B362_STATUS.md" \
+         "2026-10-21_B405_STATUS.md" "2026-10-21_B419_STATUS.md" "2026-10-21_B420_STATUS.md" "2026-10-21_B420_evidence" "ADDENDUM-1" "qa-file32.sh" "qa-applymut.py" "qa-netbelt.sb" \
@@ -500 +549 @@
-         'LEGITIMATE SHAPES' 'NOT RUN under ruling (o) EXTENDED' 'NEVER EXECUTED'; do
+         'LEGITIMATE SHAPES' 'NOT RUN under ruling (o) EXTENDED' 'NEVER EXECUTED' 'THE CI REDS' 'three forward merges' 'CI pending'; do
@@ -504 +553 @@
-         'r0' 'r1' 'r1c' 'r2' 'r3' 'r4' 'r5' 'r6' 'r7' 'r8' 'C-209' 'C-190' 'C-68' 'T0' 'T1' 'NAMED NOT RUN' 'NOT RUN' '--replace' \
+         'r0' 'r1' 'r1c' 'r2' 'r3' 'r4' 'r5' 'r6' 'r7' 'r8' 'r9' 'C-209' 'C-190' 'C-68' 'T0' 'T1' 'NAMED NOT RUN' 'NOT RUN' '--replace' \
@@ -506 +555,2 @@
-         'MERGES GO FIRST' 'QUEUE, NEVER TAKE OVER' 'Sonnet' 'PROVISIONAL' 'CodeQL is NOT RUN by this gate' 'FINDINGS-ONLY' 'never squash' 'SAME commit' 'is NEVER executed'; do
+         'MERGES GO FIRST' 'QUEUE, NEVER TAKE OVER' 'Sonnet' 'PROVISIONAL' 'CodeQL is NOT RUN by this gate' 'FINDINGS-ONLY' 'never squash' 'SAME commit' 'is NEVER executed' \
+         'THE CI REDS' 'MERGE CONTENT' 'THREE forward merges'; do
@@ -511 +561 @@
-for S in "$HEAD_SHA" "$HEAD_TREE" "$C1_SHA" "$BASE" "$BASE_TREE" "$LOCK_SHA_INST"; do
+for S in "$HEAD_SHA" "$HEAD_TREE" "$C1_SHA" "$BASE" "$BASE_TREE" "$ROOT" "$PRE" "$OLD_HEAD" "$LOCK_SHA_INST"; do
@@ -524 +574 @@
-for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
+for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME" "$PANE_NAME"; do
@@ -551,2 +601,2 @@
-r2 r3 r4 r5 r6 r7 r8 M0 d463f88 6e947f4 a7e8f4f PR%#101 PR%#97 PR%#96 PR%#67 19477a9 RD-874 RD-875 RD-810 SEAT-R11 B355 S101O
-L-R1 L-R7 L-Y1 H-1 H-3 H-4 H-6 H-14 H-17 H-20 H-21 H-24 H-27 H-28 H-29 H-31 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
+r2 r3 r4 r5 r6 r7 r8 r9 M0 b8715182 d463f88 c139e4a 7c11c78 5cc0629 48a17df 6e947f4 a7e8f4f PR%#101 PR%#97 PR%#96 PR%#67 9cae053 RD-874 RD-875 RD-810 SEAT-R11 SEAT-F36 B355 B420
+L-R1 L-R8 L-Y1 H-1 H-3 H-4 H-6 H-14 H-17 H-20 H-21 H-24 H-27 H-28 H-29 H-31 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
@@ -557 +607 @@
-H2 H4 H1a H1b H3 qa-g33-H3 node%--check --update-counts"
+H2 H4 H1a H1b H3 qa-g33-H3 node%--check --update-counts Datasec/NexusAI-G36 QA/NexusAI-gate33 follow-redirects"
@@ -572,2 +622,2 @@
-for L in L-R1 L-R2 L-R3 L-R4 L-R5 L-R6 L-R7 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
-for R in r0 r1 r1c r2 r3 r4 r5 r6 r7 r8; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
+for L in L-R1 L-R2 L-R3 L-R4 L-R5 L-R6 L-R7 L-R8 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
+for R in r0 r1 r1c r2 r3 r4 r5 r6 r7 r8 r9; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
@@ -623 +673 @@
-for V in '`B359/PR101: <GO|GO WITH FINDINGS|NO GO|ESCALATED TO TIER 1> @ ' '`LANDING CHECKLIST: PR #101 '; do
+for V in '`B420/PR101: <GO|GO WITH FINDINGS|NO GO|ESCALATED TO TIER 1>[ (CI pending: <names>)] @ 7c11c78 tree 71817e8 ' '`LANDING CHECKLIST: PR #101 '; do
@@ -659,2 +709,2 @@
-# Gate 33 adds Datasec/NexusAI-R11 (the B355 builder, finished) to the candidate list; a missing pane is a NOTE, never a refusal.
-for NAME in Datasec/NexusAI-O Datasec/NexusAI-W17 Datasec/NexusAI-L7 Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-P Datasec/NexusAI-R Datasec/NexusAI-R11 Datasec/Security-Composer-W13 Datasec/Security-Composer-G22 Datasec/HPSM-POC-D5 "$COORD_NAME"; do
+# Gate 33 adds Datasec/NexusAI-R11 (the B355 builder) and Datasec/NexusAI-F36 (the B419 forward-merge builder) to the candidate list; a missing pane is a NOTE, never a refusal.
+for NAME in Datasec/NexusAI-O Datasec/NexusAI-W17 Datasec/NexusAI-L7 Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-P Datasec/NexusAI-R Datasec/NexusAI-R11 Datasec/NexusAI-F36 Datasec/Security-Composer-W13 Datasec/Security-Composer-G22 Datasec/HPSM-POC-D5 "$COORD_NAME"; do
@@ -672,3 +722,3 @@
-[ "$NEG_BUILDERS" -ge 1 ] || { echo "REFUSING: no live builder seat among Datasec/NexusAI-O/W17/L7/M/N/P/R/R11, Security-Composer-W13/G22, HPSM-POC-D5 — at least ONE negative control is required" >&2; exit 38; }
-# fleet-monitor and every live 'QA/*' pane other than this gate's own (gate 29 is LIVE at drafting): a negative control when exactly one claude runs under it.
-EXTRA="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep -E '^(QA/|fleet-monitor$)' | grep -vxF "$ROUTE_NAME" | sort -u)"
+[ "$NEG_BUILDERS" -ge 1 ] || { echo "REFUSING: no live builder seat among Datasec/NexusAI-O/W17/L7/M/N/P/R/R11/F36, Security-Composer-W13/G22, HPSM-POC-D5 — at least ONE negative control is required" >&2; exit 38; }
+# fleet-monitor and every live 'QA/*' pane other than this gate's own (route name AND pane name): a negative control when exactly one claude runs under it.
+EXTRA="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep -E '^(QA/|fleet-monitor$)' | grep -vxF -e "$ROUTE_NAME" -e "$PANE_NAME" | sort -u)"
@@ -692,4 +742,4 @@
-# 86 — no live gate-33 session already exists.
-for P in $(pane_pid_of "$ROUTE_NAME"); do
-  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 33 is live; do not start a second session" >&2; exit 86; fi
-  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
+# 86 — no live gate-33 session already exists (under the route name OR the pane name).
+for P in $(pane_pid_of "$ROUTE_NAME") $(pane_pid_of "$PANE_NAME"); do
+  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME or $PANE_NAME (pid $P) already runs a claude — gate 33 is live; do not start a second session" >&2; exit 86; fi
+  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME or $PANE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
@@ -698 +748 @@
-# 32S / 40 — LAST: the coordinator's stamp (0 '@NAME@' placeholders anywhere in the kit: MAIN_SHA x2 + STAMP_TIME x1; the LAST line reads
+# 32S / 40 — LAST: the coordinator's stamp (0 '@NAME@' placeholders anywhere in the kit: the stamp time x2 + the launch authority x1; the LAST line reads
@@ -705,2 +755,2 @@
-GUARDS='9 40 18T 18 6 18M 7 8 90 22 93 93U 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 79 38R 86'
-SUMMARY="ls-remote attempts this run: ... ancestry carries d463f88; the 2 PR commits not on M0; ... 2 linear commits over d463f88; ... head counts 4941 304, base counts 4934 303; lockfile/package/workflow blobs = M0's; ..."   [long line, condensed]
+GUARDS='9 40 18T 18 6 18M 7 8 90 22 22M 93 93U 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 79 38R 86'
+SUMMARY="ls-remote attempts this run: ... ancestry carries d463f88 and c139e4a; the 5 PR commits not on M0; ... 5 commits over b8715182 with 3 merges, full parent lists and trees checked, left-right 0 5; ... merge 2 = package-lock.json only, merge 3 = HISTORY.md + propose-dark-retheme.js only = main's side, patch sha256 ${PATCH_SHA:0:8}… equal before and after; head counts 4971 305, base counts 4964 304; lockfile/package/workflow/jsonStorage blobs = M0's; ...; B419 READY line for the head present; ..."   [long line, condensed]
@@ -713 +763 @@
-  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32S): $NSLOT at-sign placeholder(s) remain in the brief (MAIN_SHA x2 + STAMP_TIME x1), or its last line is not 'READ-WHOLE-BY-TUESDAY: DONE …' (it reads: '${LASTLINE:0:60}') — the coordinator reads the kit whole and stamps before launch" >&2
+  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32S): $NSLOT at-sign placeholder(s) remain in the brief (the stamp time x2 + the launch authority x1), or its last line is not 'READ-WHOLE-BY-TUESDAY: DONE …' (it reads: '${LASTLINE:0:60}') — the coordinator reads the kit whole and stamps before launch" >&2
@@ -720 +770 @@
-  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = the stamped pin ${MAIN_SHA:0:12} exactly; the branch and $PR_REF at 6e947f4; T9 unmounted (18T)"
+  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = the stamped pin ${MAIN_SHA:0:12} exactly; the branch and $PR_REF at 7c11c78; T9 unmounted (18T)"
@@ -736 +786 @@
-[long line, 1542 chars] VERIFIED BY THE LAUNCHER AT $PIN_TS ... PR #101 @ 6e947f4 (two linear commits over d463f88; 4941/304) ... 
+[long line, 1916 chars] VERIFIED BY THE LAUNCHER AT $PIN_TS ... the head 7c11c78: 5 commits over b8715182 with 3 merges; 4964/304 -> 4971/305; merge 2 and merge 3 contents; P97/P67 notes ...
```
(Line-number note: the hunks use the installed file's numbering on the left and the draft's on the right. In the draft the `MODEL RULE` header comment no longer carries a person's first name; the original had it twice, in a comment and in the prompt paragraph.)

## Questions for Tuesday, each with a recommendation
1. **Pane label versus route name.** The task gives the pane `Datasec/NexusAI-G36`; the answer route, mail subjects and the launcher's routing guard still use `QA/NexusAI-gate33`. I kept both (the route name is the routing-file key, the pane name is only used for "no second session" and the negative-control exclusion). Recommend: add `QA/NexusAI-gate33|tuesday-agent@agentmail.to|no` after line 238 as written. If you want the pane name to be the route, change `ROUTE_NAME` and the four subject strings together and re-stamp; do not edit one without the other (guard 20 would refuse).
2. **Start while `build` is still pending?** The four code-scanning legs are complete, so the gate can start; `build` (run `39572998589`) has been `in_progress` since 19:55:48 (about 23 minutes at 20:18). Recommend: launch as soon as the stamp, routing line and `--check` are done, without waiting; the gate reads the Build at start and end, appends ` (CI pending: build)` if it is still pending, and treats a failure as a Blocker for landing under R2. Waiting buys only a tidier verdict line, and the gate's lock-free rows run for an hour or more first.
3. **R2 and the old head's red.** The old head's Build is `completed / failure` (job-level only). The kit makes the gate read the failing suites of all three Builds (`48a17df8`, `5cc06298`, `7c11c78f`) and set them side by side, without re-running anything. Recommend: keep R2 as written; if the new head's Build comes back green, that is evidence that the cause is not in #101's code and still not a clearance of the old red or proof of who held port 38900.
4. **Offline cache for `follow-redirects-1.16.1`.** The cache index lists the tarball; content for the whole lock is unmeasured, and the ruling (m) says an `ENOTCACHED` makes every jest row NOT RUN. Recommend: before launch, one offline `npm ci` in a scratch clone (your side, not the gate's) to prove the cache, or a pre-launch one-tarball registry ruling as B392 had; otherwise rule now that a NOT RUN is acceptable.
5. **Apply the corrected PR-body sentence before the gate** (kit WRONG item 3). The body is still the 4941/304 text and names no head. A gh write by you or a NexusAI seat. Recommend: before launch, so r6 grades the live text instead of a stale one.
6. **Report location** is now `Briefs/2026-10-21_B420_STATUS.md` in both the kit and the launcher (guard 10). Recommend accept (it matches your B411 instruction).
7. **No `Deploy demo` run for main's own head `b8715182`** (the latest three skipped runs are on `940dac40`, `c139e4a8`, `115a775b`). The kit sends it to r7 to name and does not call it a finding. Recommend: nothing before launch.
8. **Landing order.** #101 is now the only open PR besides #67 (dirty, conflicts with the counts file). Recommend: land #101 first on a GO; if #67 lands first, #101 needs a fourth forward merge and a new gate.
9. **Carried, not mine to rule:** C-68 `:671` versus "no regeneration" (B405 and B419 both flagged); the 33 modified files and 1 untracked file in the NexusAI root checkout (B414 item 3, B419 open item 2; the kit tells the gate not to touch or read them); the Dependabot "2 vulnerabilities" notice.

## Earliest time the gate can start
All four code-scanning legs at `7c11c78f` (`CodeQL`, `Analyze (actions)`, `Analyze (python)`, `Analyze (javascript-typescript)`) were `completed / success` at my first read, 20:03:56; the last to finish was `Analyze (javascript-typescript)` at 19:58:10 AEDT (08:58:10Z). The three analyses were created by 19:58:00. So the Analyze condition is already met, and the earliest start is bounded only by Tuesday's own steps: read-whole, stamp, routing line, install and `--check` the launcher, and a launch-time load1 below 7 (load was 5.79 at 20:18, 2.39 at 20:04). `build` is not a start condition (question 2); it was still `in_progress` at 20:18:35.

## Could not measure
No jest, node, npm, mutant, plant, spy, `--check` run of the launcher (so guards 9, 40, 18T, 18, 90, 38R, 86, 32S and the exec tail are untested); the failing suites inside any of the three Build runs (job-level conclusions only); the new head's `build` result; whether the offline cache holds every tarball of the lock; the four `HISTORY.md` readers' results at the merged tree (predicted PASS, READ-ONLY-INFERRED; main's own push Build `39555320727` is success); `rd545`'s `reservePort` path for port 42881 (still nobody's read); whether GitHub reaches `mergeable_state` `clean`; `server.js` beyond the two log lines; CLARIFICATIONS.md text (rule numbers come from the earlier kits and the B419 STATUS).
