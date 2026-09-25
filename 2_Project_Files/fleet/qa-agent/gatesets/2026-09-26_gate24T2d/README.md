# Gateset 2026-09-26_gate24T2d — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane and committed nothing. It wrote only under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9df682b4-df07-4cdb-b01c-fee44dc335fd/scratchpad/gate24T2d/`. No container was started, no port bound.

This kit is ONE batch gate over SEVEN PRs from FOUR seats: five tier 2 and two tier 3. Two of the PRs are AT THE CAP. Your four WIDEN messages grew
it from three to seven (7 of the cap of 8), and per your last message it is FROZEN at seven:
- **#1250** KS-1302 + KS-1303 **ROUND 2 OF 2** (L5, wrapped), `2b8dcb824dd2c5cd4b92757934d7de9d28813a22`.
  - Three commits on BASE `6e2a00bfed57`: round 1 `c78f4093fb53`, then R2, then R2b. Fast-forward, no force. 2 files, +248/-5.
  - Graded against **your RULING (a)** and against the round-1 SIGTERM property.
- **#1253** KS-1297 **ROUND 2 OF 2** (L5, wrapped), `91e066264004fdb22c67efb0c25fc44375ec6eac`.
  - Two commits on BASE: round 1 `6b88e4f03e82`, then R2. 1 file, +258/-3.
  - Graded under THE READER RULE.
- **#1262** KS-1310 + KS-1311 (B 28th, wrapped), `3b319485d1e3a58f30e4190a7898d7562cb80c3b`.
  - One commit on `fa25c9b10fb4`. 1 integration test file, +283/-1.
  - Postgres on **127.0.0.1:55419 only**. Docker is used for this PR and no other.
- **#1263** KS-1140 (L7, LIVE, **T3**), `3c33f936fe3985ab40b72b78bda15a6959448e18`.
  - One commit on develop `4db87c3e4b98`. Comments only, in the ks879 test (+25/-6).
- **#1264** KS-1281 (L8, LIVE, **T3**), `2e95121dfc475a09c81d61d61f9a81148b6bb0b9`.
  - One commit on `4db87c3e4b98`. Comments only, in vc-issuer's PRODUCT file `credentialRepo.ts` (+9/-4).
- **#1265** KS-1315 (L7, LIVE, T2), `87ef6a1b088754ab773f541ddb273acce8dfab4f`.
  - One commit on `4db87c3e4b98`. Test-only: four rows in systemTest/performance's k6DockerRedaction test (+35/-0).
  - A systemTest/ push skips the preflight, so its fleet STOP count is NOT APPLICABLE.
- **#1266** KS-1120 (L8, LIVE, T2), `952f4329de97cd7f94ab6363e670248c456d0a54`.
  - One commit on `4db87c3e4b98`. **Test-only** (+54/-0 in vc-issuer's ks1020 test, cells X1 and X2). Your message called it "a PRODUCT
    change"; the file list says test-only, so tier 2 and not tier 1.

Routing: `QA/Secuura-batch1250r2`. GO string: `GO: merge #1250, #1253, #1262, #1263, #1264, #1265, #1266 batch` (or the subset).
- #1250, #1253 and #1262 go to a MERGE SEAT, because their authors have wrapped.
- #1263-#1266 are merged by their own LIVE authors (L7, L8).

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4).
  - Pinned over develop `4db87c3e4b98b8e366c3dd60d5f399917bad5086` (#1255's squash). That develop was unmoved at every read, the last at 18:53Z.
  - gate24T2c is RUNNING over the same develop, and its seven PRs are path-disjoint from all seven of ours.
  - If gate24T2c's GO subset merges first, launch step 3b re-pins in the same action.
- **#1250: predicted NO GO at the cap, by the drafter's LIVE probe of the real runner** (a PREDICTION; the gate measures).
  - **The product fix works.** SIGTERM to round 2's runner gave rc 143, no further suite, no verdict, and the dir removed. Round 1 swallowed it: rc 0
    and a green verdict. Your conditions (2)-(4) read MET.
  - **But condition (1) fails for one arm: RULE2-UNDER-SETM + INT-PID-CONSTANT.**
    - The suite reports "SIGINT to the pid" as UNREACHABLE through a CONSTANT branch. No probe runs for it, and it counts as 1 of the 58 passes.
    - Its harness starts the runner under `set -m`. With job control on, bash does NOT ignore SIGINT in the background job: `trap -p INT` is
      non-empty there (measured).
    - Round 2 under INT-to-pid in that exact shape gave rc 130, no suite, no verdict, dir removed. Round 1 and develop gave rc 0 and
      `shell suites: 2 passed`.
    - So the arm is predicted REACHABLE and DISCRIMINATING. Its UNREACHABLE is vacuously green, and your commission rule makes that a NO GO.
    - The premise behind ruling (a) ("bash ignores SIGINT in an asynchronous job") holds only WITHOUT job control (§6 decision 1).
  - Also measured, non-blocking:
    - RUNNER-MASKS-INT: under round 2's runner EVERY suite starts with INT ignored, so the INT arms can never assert under leg 14, hook or not.
    - BG-STDIN: a suite's stdin is now /dev/null.
    - ORPHAN-ON-SIGNAL: a suite's `&` grandchild survives every signal on every runner, develop included.
- **#1253: predicted NO GO at the cap under THE READER RULE** (the REAL guard with SUBJ_SH, 12 shapes, readerprobe_1.out).
  - All five swallowing shapes are now flagged.
  - **But cell 9 FLAGS the named-safe `bf || true`, `false || bf`, `if bf; then :; fi` and `bf && :`.** Your commission says they "must NOT be"
    flagged, and the HOLD line said "each not flagged".
  - It also MISSES a multi-line `x=$(` / call / `)`.
  - STALE-CONTROL: cell 10 still runs the round-1 ERE, so its `ok` text describes a predicate that no longer exists (§6 decision 2).
- **#1262: predicted GO WITH FINDINGS (READ only; nothing was run against a DB).**
  - The owner assertion NEVER RAN at the red base (OWNER-UNASSERTED-AT-BASE): the red stops one `expect` earlier. The gate measures it by a
    reordering probe.
  - The refusal also admits `localhost` and gates DEFAULT_DB only (LOCALHOST-ALSO, REFUSAL-SCOPE).
  - :55419 was free at 18:53Z against a control of 41 LISTEN lines. The two foreign docker volumes are noted, never to be touched.
- **#1263: predicted GO WITH FINDINGS.**
  - All 31 changed lines are comments, and the comment-stripped text is equal (port). The gate owes the TypeScript emit proof with its DIFFERENT
    control.
  - **MAGIC-WORD-CLOSES:** the PR body's "This does not close KS-1140's GF-1" made Linear link KS-1140 as **`closes`**. A squash would close the
    ticket (§6 decision 4).
- **#1264: predicted GO WITH FINDINGS.**
  - All 13 changed lines are comments. The files the comment names do create `vc_credentials_store` (READ).
  - The "no CREATE on schema public" grant is UNMEASURED.
- **#1265: predicted GO WITH FINDINGS (READ).** The T-1 target line occurs once in develop's `k6_docker.ts`, and the four rows are present, with
  L04 named `KEY` exactly. The gate owes K-1..K-4: T-1 gives 7 red at head and 3 at develop, and the naming arm turns L04 green.
  - N-1244-a is gate24T2a's finding, not gate24T2b's as relayed. The prompt points at the right report.
- **#1266: predicted GO WITH FINDINGS (READ).** The gate owes P-1..P-3 from `tamper_ks1120.py`: T4 reds X1 only and T5 reds X2 only, and both stay
  129/129 green at develop without the cells.
- **Widen:** all four round-25 PRs on origin at the re-pin are IN (#1263-#1266; gh_read_5.out). None was excluded, and the batch is FROZEN at seven.
  - **#1265's and #1266's READY mails were NOT read.** You named them as "the newest READY … mail", and finding a mail without its id needs a
    listing, which marks mail seen. Their PR bodies are captured instead (§6 decision 5).
- **The N-1250-b TIMING CELL rule you carried is in the prompt, and a launcher guard checks it (exit 38).**
  - If it reds, it is re-run ONCE with the load recorded, and a green re-run is not a NO GO. It never decides the cap.
  - The SIGTERM properties are graded independently of it.

## 2. Pins — predict_4.out at 19:01:37Z (rc 0; predict_1..3 were the 3-, 4- and 5-PR pins, superseded by your widens)
- **develop `4db87c3e4b98b8e366c3dd60d5f399917bad5086`**, tree `ff4f372afe71…`. That tree equals gate24T2b's END_TREE_GO.
  - It is 10 ahead of BASE `6e2a00bfed577528de1ee02b41cb5a0e99172b35`, and the move touches 20 paths.
  - The move ∩ every PR's own paths is **EMPTY**.
- **Chains (measured):**
  - #1250 = [c78f4093fb53, 86ba93d25211, 2b8dcb824dd2] on BASE;
  - #1253 = [6b88e4f03e82, 91e066264004] on BASE;
  - #1262 = [3b319485d1e3] on fa25c9b10fb4;
  - #1263, #1264, #1265 and #1266 = one commit each on 4db87c3e4b98.
  - Every round-1 head is an ancestor of its round-2 head, so both pushes were fast-forward.
- **Round-2 deltas:** #1250 +96/-0 (suite) and +35/-2 (runner); #1253 +153/-10.
- **Merged trees over develop:**
  - #1250 `6a39630c02754815ee7bdb479d61363a0a9a89b7`;
  - #1253 `bfc41266c3341f8af3acd9de79f8010a633e22e7`;
  - #1262 `94c974f232cea6625941554097643610b9a33dbe`;
  - #1263 `4d78948085b03cf315f24ab7129a2dc36baae4b6`;
  - #1264 `04987eff04658199ddf18496e2f01b96c1ee05b3`;
  - #1265 `21f29ad9e4a8f09de708b84f49ffafbcdb03bfb5`;
  - #1266 `38d8333f94289ce955a09b44f4344a4998215cba`.
  - Checks (1)-(3) hold for all seven. Every merged blob equals its head blob, and every mode is 100644, unchanged.
- **END_TREE `de3ef49027d7a434a36c421f632105bcfd8b35cd`** (develop + all seven): 8 files, +912/-19.
  - It is identical in 53 orders (every ordered pair merged first, plus every rotation of the sorted order and of its reverse, prefix-memoised), and
    `apply --cached` agrees. The drafter did not run all 5,040 orders; that is in §9.
  - **The four CAP VARIANTS are pinned the same way:**
    - both L5 PRs held (#1262-#1266) → `23e12ac141561a5296c3758ddd98600f68193197`;
    - #1253 held → `4cf0131924bae309e03b7981496a926ee29db521`;
    - #1250 held → `f9e01751de66225c2dda6f457df0be27436e0436`;
    - all seven → the END_TREE.
- **PAIRWISE:** all 21 pairs are path-disjoint, and gate24T2c's 7 are disjoint from all 7. gate24T2c's #1245 sits in systemTest/performance beside
  #1265, but on different files.
  - Couplings by content or execution:
    - #1250's runner EXECUTES #1253's guard at leg 14;
    - #1263's ks879 walks #1262's, #1264's and #1266's `.ts` files (0 raw control bytes, port);
    - #1258 (gate24T2c) changes run-migrations.sh, which #1262's DB uses;
    - #1261's comment calls ks1263 "127.0.0.1:1", which goes stale once #1262 merges.
- **GitHub compare** develop...head, launcher `--check` rc 0 (launcher_check_4.out):
  - #1250: merge_base BASE, ahead 3, behind 10;
  - #1253: merge_base BASE, ahead 2, behind 10;
  - #1262: merge_base fa25c9b1, ahead 1, behind 5;
  - #1263 to #1266: merge_base 4db87c3e, ahead 1, behind 0.
  - Files == own paths on all seven (launcher_check_5.out), and `mergeable` was True ×7 at 19:04Z (repin_dryrun_3.out).
- **Instruments:**
  - `ls-remote` from the Secuura checkout (a read verb);
  - a scratch clone at `_sp/g24d_sp/clone.git` (`git clone --bare --no-local`, NO alternates), fetched from origin;
  - REST GET and Linear queries;
  - seat records read as plain files;
  - `lsof` for the port;
  - the drafter's three live probes in `_sp/trapprobe`, `_sp/maskprobe` and `_sp/readerprobe`.

## 3. What the gate owes (the prompt `2026-09-26_secuura-batch1250r2-t2.prompt.txt`, 75.3 KB)
- **THE CAP:** a round-2 NO GO ships nothing. The PR stays open and is not built on, and the residue is TICKETED: the gate names each residue ticket,
  and you or a successor files it. The cap raises the cost of a NO GO, "never the bar and never the leniency".
- **#1250 under RULING (a), first and cheap:**
  - (R-A) and (R-B): the head suite in a normal shell and in an INT-ignoring parent;
  - (R-C): condition (2), the head suite with the round-1 runner, TERM and INT-group red;
  - (R-D): develop's runner;
  - **(R-E) INT-PID-PROBE:** a copy of the suite with only the constant INT-pid skip removed, run with the head, round-1 and develop runners;
  - (R-F) LATENCY: the foreground reverted, do the arms still pass?
  - (R-G): the re-raise removed;
  - the fixture probe across 6 arms × 3 runners, with suite and grandchild liveness;
  - RUNNER-MASKS-INT and BG-STDIN, plus the census of the 60 suites.
- **#1253 THE READER RULE:** 12 shapes at the c2 call site (not c0 or c1, which are cells 10 and 11's own anchors), run through the REAL guard with
  SUBJ_SH. Each shape's BEHAVIOUR is also measured (abort reaches the suite, or is swallowed). Plus G0-G4.
- **#1262 DB:**
  - port proof with a control; an anonymous volume; every DB variable pointed at :55419; never :5432;
  - (I-B) red at `33ccff807eb2` with the head's file planted;
  - (I-O) the owner measured by a reorder probe;
  - (I-T0) an inert trigger must fail the cell;
  - (I-R) the refusal fires on 55420;
  - (I-C) `pg_trigger`/`pg_proc` 0/0 after every run;
  - torn down and proven gone, with the two foreign volumes untouched;
  - MODE F only if Prisma generates offline (KS-1305).
- **#1263 / #1264 TIER-3 PROOF:**
  - (T3-a) `transpileModule` with removeComments, parent == head;
  - (T3-b) a one-token DIFFERENT control;
  - (T3-c) the -U0 line check with its control;
  - (T3-d) suites equal (packages/shared 941; vc-issuer 129, with shared BUILT first);
  - (T3-e) ks879 on END.
  - A DIFFERENT emit, or a code line, is NO GO.
- **#1265 (K-1..K-4):**
  - T-1 at head gives 7 red, read from `--json` fullName;
  - T-1 at develop gives L02, L03 and L08 only;
  - the naming arm turns L04 green;
  - test:unit goes 1104 → 1108, and lint is run.
- **#1266 (P-1..P-3):** T4 reds X1 only; T5 reds X2 only; both stay 129/129 green at develop. vc-issuer goes 129 → 131 (shared built), and tsc is
  run on the new test file directly.
- **Suites (serial):**
  - the two changed shell suites standalone in the gate's worktrees: BASE → round 1 → head → END, 49 → 55 → 58 and 6 → 10 → 12;
  - originate unit at develop and at #1262 (must be equal) and the ks1263 integration file only;
  - packages/shared and vc-issuer for the T3 PRs;
  - lint, tsc, shellcheck, prettier;
  - no other integration file is run.
- **Fleet STOP:** claimable for the six Blockchain/Dev PRs BY READ (predict (k), anchored, with a NOT-FOUND control):
  - #1250: 28/0, 6/0, **58/0**, 60/60, with in-hook `INT installable=no` and **2 UNREACHABLE cells**;
  - #1253: 28/0, **12/0**, 49/0, 60/60;
  - #1262, #1263, #1264 and #1266: 28/0, 6/0, 49/0, 60/60;
  - #1265: NOT APPLICABLE (a systemTest/ push: the format gate only).
  - The six with a preflight are all INCOMPLETE 12/15, with legs 3/4/8 skipped.
  - **After merge: fixture_guard 12/0 if #1253 merges, run_shell_suites 58/0 if #1250 merges.** The denominator stays 60.
- **Carried:** STREAM-SEPARATED, PRESUITE-URLPATH, the KS-1155 one re-run, the tamper-APPLIED rule, and your TIMING CELL rule.
- Time-box 240 min. Report dir `reports/2026-09-26-batch1250r2-t2d/`.

## 4. The routing line is NOT written by the drafter. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1250r2|coagent@agentmail.to|yes
The drafter's read found `QA/Secuura-batch1250r2` ABSENT (grep -c 0, rc 1; routing_read_1.out and routing_read_2.out). Without it, repin step 0 refuses
with rc 1. Controls R4 and R4b prove that.

## 5. THE ONE LAUNCH COMMAND (copy to gatesets/ + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9df682b4-df07-4cdb-b01c-fee44dc335fd/scratchpad/gate24T2d/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2d/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2d/repin_and_launch_gate24T2d.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2d/launch_qa_secuura_batch1250r2-t2.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9df682b4-df07-4cdb-b01c-fee44dc335fd/scratchpad

**The moved kit.** Step 0b sees a MOVED KIT and re-runs predict and fill at the new home, in the same action. Predict makes a fresh `--no-local` clone
under `<scratchpad>/g24d_sp` (about 25 s). Controls R6 and F1 prove that the moved kit works.

If develop moves (gate24T2c's GO subset), 3b re-pins over it. A move on any PR's own path refuses, and has to be re-predicted by hand.

The steps and their refusal codes:
- 0 routing (1)
- 0b moved kit: predict + fill (8)
- 1 ls-remote (2)
- 2 the PULLS API ×7 (3)
- 3 heads == pins on both instruments, open, not `mergeable:false` (11). A launcher still pinned to a ROUND-1 head refuses: control R2r.
- 3b develop moved → predict + fill, then develop re-read (10)
- **3c :55419 free, against a LISTEN-table control (15)**
- 4 usage gate (12)
- 5 `--check` (13)
- 6 `cockpit.sh add QA/Secuura-batch1250r2` (14), then a pane census

**Rehearsal:** append `--dry-run`. repin_dryrun_3.out ended rc 0 at 19:04:59Z.

## 6. Decide or know before launching
1. **#1250: the INT-to-pid arm is drafted as BLOCKING** (a vacuously green arm is NO GO; condition (1) is not met where the probe could answer YES).
   The drafter's probe predicts NO GO at the cap.
   - **What that costs:** the round-2 runner fix itself measured correct, yet ships nothing.
   - **What a NO GO leaves on develop:** no trap at all (the `/tmp/rss.*` residue, KS-1302), the `| tee` wait (KS-1303), and develop's own
     INT-to-pid rc 0 + green verdict.
   - **To grade it by your ruling's letter instead** (the pid arm accepted as unreachable):
     - edit the sentence "if YOU measure that an arm the PR reports UNREACHABLE is in fact REACHABLE … NO GO for #1250 (blocking)" in the prompt
       TEMPLATE's RULING paragraph;
     - leave the exit-41 anchor ("A signal arm that is vacuously green is a NO GO" is your text, so keep it or edit both);
     - then re-fill.
   - Either way, the gate MEASURES R-E and reports it.
2. **#1253: SAFE-SHAPES-FLAGGED is drafted as BLOCKING,** from your commission's "`false || bf` and `|| true` must NOT be" flagged. The drafter predicts
   NO GO at the cap.
   - The seat's cell 12 argues the other way: a whitelist is bare-only by design, so it records the flag and asserts only that the shape aborts.
   - Reach today is 0: the 12 call sites are bare.
   - To rule the strict whitelist acceptable instead, edit THE READER RULE's #1253 sentence and the exit-40 anchor `'`false || bf` and `|| true` must
     NOT be flagged'`, then re-fill. CMDSUB-MULTILINE (a miss, a named class) would then decide.
3. **#1262's Docker:** the gate may run Docker for #1262 only, binding **127.0.0.1:55419** (B 29th's live range is 55410-18).
   - At 18:53Z the port had 0 listeners against a control of 41. Launch step 3c refuses if it is busy.
   - The foreign volumes `0ec12181dd37…` and `0187e1998e06…` are named for the gate never to touch.
4. **#1263 MAGIC-WORD-CLOSES:** Linear's attachment for #1263 is `closes` KS-1140 (linear_reads_3.out), triggered by "does not close KS-1140's GF-1".
   Before a squash, either L7 re-words the body and the link is set back to `contributes`, or you rule that KS-1140 closes (its READY says "Ticket
   left In Progress").
5. **Three READYs were never captured: #1253 round 2, #1265 and #1266.** No message id reached the drafter for them, and a listing would mark mail
   seen. Their seat items come from the PR bodies (gh_body_<n>.md). To capture the mails as well, hand the ids, add them to
   `capture_mail_gate24T2d.py`, and re-run capture + fill.
6. **Merge seats:** #1250, #1253 and #1262 need a merge seat you name.
   - M1's brief names #1262 (and says L5's PRs are "never yours"). L5 wrapped, so #1250 and #1253 need a named merger if they are GO.
   - #1263 and #1265 (L7), and #1264 and #1266 (L8), are merged by their live authors.
7. **MG-3 / MG-11:**
   - Un-hyphenate the foreign keys in the squash bodies: KS1127 and KS1135 (#1250's round-1 commit), KS1293 (#1262's commit; its body also names
     KS1305), KS1090 (#1264's body), KS1111 and KS1098 (#1265), and KS1020 (#1266's body).
   - Titles are 83 / 83 / 77 / 77 / 73 / 76 / 75 chars: all ≤ 92 even with ` (#NNNN)`.
8. **`mergeable: null` policy** is as in gate24T2b: null is reported after 3 reads, not refused; `false` refuses.
9. **The drafter's leftovers** (never delete; REPORTED):
   - the probe's develop-runner arms left `/tmp/rss.0FLxcj`, `/tmp/rss.6R8Lgh`, `/tmp/rss.9hG5P0`, `/tmp/rss.lgCPgT`, `/tmp/rss.PEEmTu` and
     `/tmp/rss.qhzyTm`. That is KS-1302 reproduced;
   - the probe's own `sleep 30` grandchildren were ended by pid (2 were still alive, 13 had already exited; trapprobe_1.out).

## 7. Controls: `controls_gate24T2d.sh <scratchpad> [--invert]`
CONTROLS_SUMMARY

## 8. Files
- COMMISSION.md (with the LEGITIMATE SHAPES tables) · README.md · PROPOSED_inbox_routing_line.txt · routing_read_1.out, routing_read_2.out
- **Pins:**
  - predict_gate24T2d.py;
  - predict_1.out (3 PRs) and predict_2.out (4 PRs), both rc 0 and superseded;
  - predict_3.out (5 PRs, rc 0, superseded);
  - **predict_4.out (rc 0, the pinned run, 7 PRs)** with predict_4.time;
  - pins_gate24T2d.json.
- **Prompt and launcher:**
  - prompt_gate24T2d.TEMPLATE.txt and launcher_gate24T2d.TEMPLATE.sh.txt;
  - fill_gate24T2d.py with fill_1..5.out (rc 0; fill_5 is the pinned fill);
  - the rendered prompt `2026-09-26_secuura-batch1250r2-t2.prompt.txt` and the launcher `launch_qa_secuura_batch1250r2-t2.sh` (`bash -n` rc 0);
  - launcher_check_1..5.out (rc 0). `.pre-*` files are earlier fills.
- **Repin and controls:** repin_and_launch_gate24T2d.sh with repin_dryrun_1..3.out; controls_gate24T2d.sh with controls_1.out (normal) and
  controls_2.out (--invert), plus their .rc files. controls_0_aborted_widen1265.out is a 5-PR run stopped by the drafter when #1265 arrived
  (17 OK / 0 MISMATCH at the stop), quarantined.
- **Captured reads:**
  - capture_mail_gate24T2d.py → mail_gate24T2d_ready.md and mail_ready_<n>.md (1250, 1262, 1263 and 1264 by id; 1253, 1265 and 1266 = PR bodies),
    with the RULING (a) and FIX ROUNDS files and 5 prior-report sha256s. capture_1..5.out; capture_5 is the pinned capture;
  - raw_ready_1250/1262/1263/1264.txt (the first reads, same sha256 as the capture);
  - gh_read_gate24T2d.py with gh_read_1..5.out, gh_body_<n>.md and gh_comments_<n>.md;
  - linear_reads_gate24T2d.py with linear_reads_1..5.out and linear_KS-*.md;
  - widen_census_1.out;
  - env_read_1.out (ports, docker, volumes).
- **Drafter's live probes (PREDICTIONS only):**
  - drafter_trapprobe_g24d.sh with trapprobe_1.out;
  - drafter_maskprobe_g24d.sh with maskprobe_1.out;
  - drafter_readerprobe_g24d.sh with readerprobe_1.out.
- `_sp/`: the scratch clone, the probe trees and the control workdirs. The launch command excludes it.

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, commit, push, routing-conf write, container, volume or port bind.
- The Secuura checkout was touched only by read verbs: ls-remote, `config --get`, and `clone --no-local` reading it as a source.
- The inbox was read only in the one permitted form (`inbox_digest.sh full wednesday-agent@agentmail.to '<id>'`), for 4 ids: #1250, #1262, #1263 and
  #1264. Each was read twice (raw, then by the capture script), and the sha256 matched each time.
- **UNMEASURED:**
  - every suite count (all counts are READ from push logs or seat mails);
  - every red arm through the REAL suites (R-A..R-G, G0-G4, I-*). The drafter ran the real RUNNERS and the real GUARD only on its own fixture trees
    and subject copies;
  - the INT-pid arm through the real suite (R-E);
  - LATENCY-UNPINNED (R-F);
  - BG-STDIN reach and the INT-trap census;
  - ORPHAN-ON-SIGNAL reach with a real suite;
  - #1253's shapes' BEHAVIOUR (abort reached or swallowed). That was READ from gate24T2b's `reader1253_2.out` and the PR body's table, not re-run;
  - the readerprobe tree was not a git repo, so every probe run also read 1 unrelated CONTROL FAIL (an instrument artefact);
  - #1262 entirely at runtime (no DB was started): the red at 33ccff807eb2, the owner, the trigger firing, the refusal, the catalogue, MODE F, and
    the mock-scoping claim;
  - #1263 and #1264's TypeScript emit (the drafter used a line and comment-strip PORT only);
  - #1265's K-1..K-4 and #1266's P-1..P-3 (READ only);
  - the systemTest/performance and vc-issuer suites;
  - END_TREE over all 5,040 orders (53 were run);
  - #1263's census figures;
  - #1264's deployed-grant claim;
  - the TIMING CELL under load;
  - lint, tsc, shellcheck and prettier;
  - the READY mails of #1253 round 2, #1265 and #1266 (no ids);
  - the usage gate and the machine load at launch;
  - the real launch path (steps 4-6);
  - whether gate24T2c merges before launch.
- **Not controlled:** exit 16 (it needs a TTY), the repin's `mergeable=False` refusal, steps 4-6, and a real develop move (only BASE-as-develop and
  foreign-edit simulations).
