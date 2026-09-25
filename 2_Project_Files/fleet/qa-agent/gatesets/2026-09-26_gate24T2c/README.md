# Gateset 2026-09-26_gate24T2c — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane and committed nothing. It wrote only under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9df682b4-df07-4cdb-b01c-fee44dc335fd/scratchpad/gate24T2c/`.

This kit is ONE tier-2 BATCH gate over SEVEN PRs from THREE seats, FROZEN at seven (your commission says "EIGHT" and lists seven; nothing was added):
- **#1245** KS-1313 ROUND 2 OF 2, THE CAP ROUND (L6), `65eb964271b0d6895e90fe8f5ffcbbbb9a484050`: TWO commits on BASE (round 1 `1700b5ae7dd5`, then round 2),
  2 files: the harness test file + a NEW `tests/unit/support/capturedChildOutput.ts`.
- **#1256** KS-1159 (B 28th), `5a41ed7fea96ab77ed1dc263ae0c7d25c9846440`: test-only, the ks1061 guard. Parent is develop `77c6426b9`.
- **#1257** KS-1201 (L5), `d1db0d41ac52359c231cd22abf11124204645d97`: systemTest-only, bootstrap_login_diagnosis 16 -> 18.
- **#1258** KS-1296 (L5), `ff90fbf9d7e351104404e3eaad505a673e656c1e`: run-migrations.sh exit 4 + run_migrations_failure_exit_code 5 -> 7.
- **#1259** KS-906 (L5), `8a2a28f50eb3453db7284da0f098f6a819d40145`: no_tracked_credentials_root 15 -> 16 (CASE 6b).
- **#1260** KS-1139 (L5), `62e69d23b2507780316f1930123c7d57ebba3ae2`: 8 counter lines in sync-secrets.sh. The gate NEVER executes it and NEVER runs `az`.
- **#1261** KS-1293 (B 28th), `eab8d7031b1b19071a66715ca0aabd9c5cb29c6d`: test-only, 1 new file. Parent is develop `fa25c9b1`.

Routing: `QA/Secuura-batch1245r2`. GO string: `GO: merge #1245, #1256, #1257, #1258, #1259, #1260, #1261 batch` (or the subset).

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4). It is **RE-PINNED over develop `4db87c3e4b98b8e366c3dd60d5f399917bad5086`**.
  - **gate24T2b squashed #1249, #1251, #1254, #1252 and #1255 while this kit was drafted** (8b666a33a 17:16:06Z … 4db87c3e4 ~17:24Z). Its #1250 and #1253 are NOT on develop.
  - That move touches none of this batch's paths. predict_5 re-measured everything over it and gave rc 0.
  - The first controls run, over fa25c9b1, was quarantined as controls_0_aborted_devmove.out (§7).
  - Every head was re-read from origin by ls-remote, by a fetch, and by the PULLS API. All seven agree with your reads, and mergeable was True ×7 at 17:31Z.
- **#1245 — predicted NO GO at the cap under THE RULE: H1 KILLED-AFTER-LOOKALIKE.** This comes from the drafter's live probe, so it is a PREDICTION.
  - The round-2 fix is right where it was aimed: through a byte-lifted `readChildOutput`, stdout alone reads S1–S18, the seat's S19 and 12 of the drafter's 13 hunt shapes correctly.
  - It misreads ONE real shape. A child killed by `spawnSync`'s timeout, after a test logged ` Test Files …` + `Tests  7 passed (7)`, reads **{7,0}**.
    The honest answer is NULL: vitest exits 143 and prints no summary.
  - `childSuiteCounts` never checks `result.error`, `.signal` or `.status`.
  - **develop and round 1 read H1 as {7,0} too.** A cap NO GO ships nothing and does not protect develop from this (§6 decision 1).
- **#1245 — two more predicted misses on the must-change list.**
  - **CALLSITE-STILL-TEXT:** the new "behavioural" call-site cell calls `readChildOutput(S17_STDOUT)` on a constant and never enters `childSuiteCounts`.
    So **T-CALL (iii) is predicted GREEN**, and your must-change "T-CALL (iii) must now RED" is predicted NOT MET (decision 2).
  - **JOINED-CLAIM:** the doc comment's "measured to hold on the JOINED text" is refuted on 8 real shapes. These include the seat's own S19 (NULL) and
    H8b ({9,0}, silent). Drafted non-blocking, because no caller passes joined text (decision 3).
  - The {3,2} row is present, S17/S18/E5 cells exist, and the call site is stdout-only (READ).
- **#1261 — predicted NO GO under THE READER RULE: REVERT-SKIPS** (a port, so a PREDICTION).
  - The PR's own header names "revert one file's env line and the suite stays green" as the shape it exists to catch.
  - Deleting the env line of ks1228 (:26) or ks1264 (:16) leaves that file with no mention of the key. CONFIGPINNED then SKIPS it, and 10 bases still clear the floor of 8: GREEN.
  - The seat's arm C3 went red only because ks520 keeps a second mention of the key (decision 4).
  - Also **NODNS-EGRESS**: the NODNS positive control resolves `anchoring` through the REAL resolver on every originate run. The gate measures that
    before running the cells (decision 5).
- **#1256, #1257, #1258, #1259, #1260 — predicted GO / GO WITH FINDINGS.**
  - The #1256 port reads 21 factories and 0 offenders on develop, the head and END.
  - #1260 is exactly 8 counter lines, and the census reads only validate-env.sh's 3 non-defects left at END (validate-lint.sh's 2 went in #1192), so **KS-1139 may close**.
  - #1260's errexit death stays UNREPRODUCED-ON-THIS-HOST (bash 3.2.57 only).
- **Fleet STOP:** none of the seven changes a triple suite or adds a suite file. What moves the count is gate24T2b's #1250/#1253 (§3).
- **The two-sided controls: see §7.**

## 2. Pins — RE-PINNED by predict_5.out at 17:28:51Z over the MOVED develop (predict_4 at 16:40Z over fa25c9b1 is superseded)
- **Develop** `4db87c3e4b98b8e366c3dd60d5f399917bad5086`, 10 commits ahead of BASE `6e2a00bfed57`:
  - #1246, #1247, #1243, #1244 and #1248 (as in gate24T2b's pin);
  - then gate24T2b's #1249, #1251, #1254, #1252 and #1255 squashes.
  - The move touches 20 paths, and ∩ every PR's own paths = EMPTY. **No declared overlap in this batch.**
- **Parents:** BASE for #1245 (2 commits), #1257, #1258, #1259, #1260; `77c6426b9` for #1256; `fa25c9b1` for #1261.
- **Merged trees over 4db87c3e:**
  - #1245 `51c5d76c62e5844d4ae8e2a82025326e29dced2f`;
  - #1256 `ec65dbb1115cc078316fcf9394c8604660a9654e`;
  - #1257 `1d10e93ce6956048c8df52c6f13f4a679d82b1dd`;
  - #1258 `97e17e6a501ab04d67ffbecfcc929531165f6ee4`;
  - #1259 `17f7fa313ef0aaa73c06edf3b93148a35fa88946`;
  - #1260 `6321619733e889a57d75f555e6680814bf5987df`;
  - #1261 `73b25cd2068750f86afd4b17067c67dd5df9b0d7`.
  - Checks (1)–(3) hold for all seven. Every merged blob equals the head blob. Every mode is unchanged (#1257 / #1258's script / #1259 / #1260 100755;
    #1258's suite 100644, as at BASE).
- **END_TREE `dfd7f306de8a6d9067b1ee591156eab9b500f0ce`** (develop + the seven, 9 files, +778/−35).
  - It is identical in 53 orders: every ordered pair first, plus every rotation of the sorted order and of its reverse. `apply --cached` agrees.
  - **END_TREE_NO1245 `54cdda7f4bce2ae72779a3f01065c2ffdac33b8e`** is the cap's END state (identical in 39 orders; `apply --cached` agrees).
- **PAIRWISE:** 21 pairs are path-disjoint. **SIBLING BATCH:** our 9 paths ∩ gate24T2b's 12 (+ #1248's) == EMPTY. #1250 and #1253, still open, are also disjoint.
- **Content coupling, now REAL on develop:** #1256's guard and #1261's CONFIGPINNED read every originate test file, and #1252/#1255 are now on develop.
  - Both ports stay green over develop and END: 21 factories and 0 offenders; 11 bases and 0 offenders.
  - REVERT-SKIPS is unchanged (ks1228, ks1264).
- **Fleet STOP read from develop 4db87c3e:** run_shell_suites 49, fixture_guard 6. It is unchanged, because #1250 and #1253 are not merged.
- **GitHub compare** (launcher `--check` rc 0, launcher_check_2.out):
  - merge_base BASE, ahead 2, behind 10 for #1245; ahead 1, behind 10 for #1257–#1260;
  - merge_base 77c6426b9, ahead 1, behind 8 for #1256;
  - merge_base fa25c9b1, ahead 1, behind 5 for #1261;
  - files == own paths ×7.
- **Counts note:** the prompt's originate figures (869 → 871) are the seats' counts over their own parents. The develop the gate grades carries #1252 (+1) and
  #1255 (+8), so expect develop ~878 and END ~880. The prompt tells the gate to say those cells in the count.
- **Instruments:**
  - ls-remote from the Secuura checkout (a read verb);
  - scratch clone `_sp/g24c_sp/clone.git` (`--bare --no-local`, NO alternates), fetched from origin;
  - REST GET and Linear queries;
  - the seat records read as plain files;
  - the drafter's vitest 4.1.11 (npm ci --offline of #1245's own lockfile into `_sp/pkg`).

## 3. What the gate owes (the prompt `2026-09-26_secuura-batch1245r2-t2.prompt.txt`, 64.6 KB)
- **#1245 LIVE-SHAPE, MANDATORY:**
  - L1: S1–S18 + S19 + hunt H1–H9, all through `spawnSync` with the streams SEPARATE.
  - L2: through the REAL `readChildOutput`, on stdout alone (the product input) AND joined (the seat's claim).
  - L3: E0–E5 through `childSuiteCounts`, plus E6, which is H1 inside the real child with its own 180 s timeout (about 3 min).
  - L4: the committed captured streams checked against real captures.
  - THE RULE verbatim: a wrong reading on any real shape = NO GO. At the cap, NO GO ships nothing and the residue is ticketed.
- **The round-1 MUST-CHANGE list**, item by item. T-CALL (i)–(iv) are included; (iii) "must now RED".
- **THE READER RULE** for #1256 and #1261 through the real suites: REVERT-SKIPS on ks1228 and ks1264, with ks1213 and ks520 as controls. NODNS-EGRESS is measured
  first: read /etc/hosts and `scutil --dns`, and if `anchoring` resolves to a non-loopback address, do not run NODNS.
- **Red proofs per PR:** #1245 G0, R-D, E1–E4, T-CALL, T-210, T-INCLUDES; #1256 T6b/T6c/T7 two-sided + SELF-SCAN/BACKTICK; #1257 K0–K2 with the
  reaper; #1258 M0 (61 s red); #1259 W0; #1260 A0/A1 with the az shim (log EMPTY, then 1 on a deliberate call; :177 excluded); #1261 C1–C3, N1–N2.
- **Suites, serial:**
  - systemTest/performance (BASE 1089 → #1245 1115 over BASE; develop and END MEASURED);
  - originate jest `--runInBand` (869 → 871, 74 → 75 suites);
  - the three changed shell suites standalone in the tester's worktrees (16→18, 5→7, 15→16) and on END.
  - lint/tsc/bash -n/prettier/knip deltas. **shellcheck is NOT installed** on the box.
- **Fleet STOP, claimable BY READ for #1258, #1259, #1260, #1261:** 28/0, 6/0, 49/0, 60/60, INCOMPLETE 12/15, legs 3 4 8. Every one READ OK in predict_4, plus each PR's own suite line (run_migrations 7/0 in #1258's own push, no_tracked 16/0 in #1259's).
  - **#1256:** its record was OVERWRITTEN by #1261's push (15:50:24Z; B 28th's second reuse this round). Only gate24T2b's drafter's predict_5/6/7 reads
    survive (labelled #1255 there, with `.start` 15:13:28Z = #1256's window by timing).
  - **#1245** ran the format gate only, and **#1257** took the hook's early return: no count to claim for either.
  - **Which develop each count is against:** each push ran on its own branch tree (#1256 on 77c6426b9, #1258–#1260 on BASE, #1261 on fa25c9b1), and all read 6/0 and 49/0. The
    count after merge is READ FROM THE DEVELOP IT LANDS ON: 28/0, 6/0, 49/0, 60/60 on 4db87c3e (unchanged: #1250 / #1253 are not merged). It becomes 28/0, **10/0**, **55/0**, 60/60 once
    gate24T2b's #1253/#1250 squash. predict re-derives it (the `stop_at_develop` pin, and control P-T2Bm proves the move).
- **No Docker, no DB, no az.** Legs 3/4/8 are NOT run and owed by none. The report dir is `reports/2026-09-26-batch1245r2-t2c/`. Time-box 240 min.

## 4. The routing line is NOT written by the drafter. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1245r2|coagent@agentmail.to|yes
The drafter's read found it ABSENT (grep -c 0, rc 1; the positive control, gate24T2b's line, was present; routing_read_1.out). Without it, repin step 0
refuses with rc 1. Controls R4 and R4b prove that.

## 5. THE ONE LAUNCH COMMAND (copy to gatesets/ + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9df682b4-df07-4cdb-b01c-fee44dc335fd/scratchpad/gate24T2c/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2c/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2c/repin_and_launch_gate24T2c.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2c/launch_qa_secuura_batch1245r2-t2.sh <your session scratchpad under /private/tmp/claude-501/>

**The moved kit.** Step 0b sees a MOVED KIT and re-runs predict and fill at the new home, in the same action. Predict makes a fresh `--no-local` clone
under `<scratchpad>/g24c_sp` (about 30 s). Controls R6 and F1 prove that the moved kit works.

**Develop moving under the kit** (expected: gate24T2b's squashes). Step 3b re-pins over it. A move on any PR's own path refuses and must be re-predicted
by hand. None is possible from gate24T2b (disjoint). Controls P-T2Bm and P1245–P1261 prove both sides.

The steps and their refusal codes:
- 0 routing (1)
- 0b moved kit: predict + fill (8)
- 1 ls-remote (2)
- 2 PULLS API (3)
- 3 heads == pins on both instruments, open, not `mergeable:false` (11)
- 3b develop moved → predict + fill, then develop re-read (10)
- 4 usage gate (12)
- 5 `--check` (13)
- 6 `cockpit.sh add QA/Secuura-batch1245r2` (14), then a pane census

**Rehearsal:** append `--dry-run`. repin_dryrun_2.out (over 4db87c3e) ended rc 0 at 17:31:25Z. repin_dryrun_1.out (over fa25c9b1) was also rc 0.

## 6. Decide or know before launching
1. **#1245 H1 KILLED-AFTER-LOOKALIKE is drafted as BLOCKING under THE RULE.**
   - Precedent: gate24T2a ruled S17/S18 blocking at reach 0.
   - The drafter predicts NO GO at the cap, so #1245 ships nothing.
   - **Weigh this:** develop reads H1 as {7,0} as well, AND develop still returns NULL on S1–S5 (the original KS-1313 defect). Shipping nothing keeps both.
   - The fix-shape is small: refuse when `result.error`/`signal` is set or `status` is not 0/1, plus one cell with H1's captured stdout.
   - To grade H1 by reach instead: edit THE RULE paragraph's H1 sentence in the prompt TEMPLATE and the exit-40 anchors, then re-fill.
2. **T-CALL (iii) "MUST NOW RED" is drafted as BLOCKING** (your "must"). The drafter predicts it GREEN. Round 1 graded CALLSITE as Minor (N-1245-a). Your
   call whether a missed must-change item alone sinks the cap round.
3. **#1245 JOINED-CLAIM is drafted NON-blocking.** It is a refuted claim, and no caller passes joined text. Flip it in the prompt's THE RULE paragraph if you
   rule a named claim falls under THE RULE.
4. **#1261 REVERT-SKIPS falls under THE READER RULE as drafted**, because the PR's header NAMES the shape. The drafter predicts NO GO for #1261.
   - Reach grading is the alternative. Reach is 2 of the 9 subject files today (ks1228, ks1264).
   - The fix-shape is an explicit subject manifest or an exact count, not a floor plus "mentions the key".
5. **#1261 NODNS-EGRESS:** running the originate suite at #1261's head sends an off-host DNS query for `anchoring` on every run.
   - The prompt lets the gate run it after reading /etc/hosts and the resolver config, and forbids NODNS if `anchoring` resolves non-loopback.
   - Say if you want it READ-only instead.
6. **"EIGHT" vs seven:** the kit is frozen at the seven PRs you listed. If an eighth was meant, it is not in this kit.
7. **Hygiene (for the addendum):**
   - #1257, #1258, #1259 and #1260 carry `Refs` in the commit only, not the PR body.
   - Foreign hyphenated keys go un-hyphenated in the squash bodies (MG-3): #1259's commit (KS-1034, KS-853, KS-859, KS-916) and #1261's (KS-1266).
   - #1257's PR body names KS-989.
   - #1245's head commit subject is 94 chars (> 92), so the squash subject is its 90-char PR title.
   - capturedChildOutput.ts embeds a seat scratchpad path (4×).
8. **B 28th overwrote a push record again** (#1256's, by #1261's push). That is the second time this round, a seat record-keeping finding.
9. **The audit fuse** (both rows lapse `2026-09-30T00:00Z`, L5 flags it again): Kam's call only, outside this gate.
10. **`mergeable: null`:** reported after 3 reads, not refused; `false` refuses (as gate24T2b). #1256 read None at 16:21Z and True at 16:52Z.

## 7. Controls: `controls_gate24T2c.sh <scratchpad> [--invert]`
- **Normal run, `controls_1.out`: rc 0, `RESULT 120 OK / 0 MISMATCH of 120`** (17:31:34Z → 17:59:15Z). Origin develop was UNMOVED during the run (4db87c3e).
- **Inverted run, `controls_2.out`: rc 1, `RESULT (inverted) 0 OK / 120 MISMATCH of 120`** (17:59:20Z → 18:21:12Z). Every control can fail, and the harness
  reports it. develop was UNMOVED.
- **QUARANTINED, `controls_0_aborted_devmove.out`: rc 1, 118 OK / 2 MISMATCH over fa25c9b1.**
  - gate24T2b's squashes moved develop mid-run (fa25c9b1 → 49bc69ab).
  - The two mismatches are exactly the develop-sensitive ones: R6 (the dry run exited 10 on the moved develop) and P-T2Bm (predict refused `fetch == ls-remote` in a race with the move).
  - The kit was re-pinned (predict_5, fill_4) and both runs above were made afresh, the same way gate24T2b's were.
- **What the 120 cover:**
  - the launcher's exits 2, 6, 7, 8, 10, 17, 20, 21, 23, 25, 26 and 30–47, each with a pristine twin through the same override;
  - the repin's exits 0, 1, 9, 10 and 11, and the moved kit (R6, F1);
  - fill refusing SIM pins (F2);
  - predict refusing a foreign edit of each of the seven PRs' own files (P1245–P1261);
  - predict re-pinning cleanly over gate24T2b's seven squashed, and reading the fleet STOP move to 55 / 10 (P-T2Bm).

## 8. Files
- COMMISSION.md (with the LEGITIMATE SHAPES tables) · README.md · PROPOSED_inbox_routing_line.txt · routing_read_1.out
- **Pins:**
  - predict_gate24T2c.py;
  - predict_1.out (rc 1: the drafter's own predicate bug, fixed);
  - predict_2.out and predict_3.out (rc 0, before the lead wording fixes);
  - predict_4.out (rc 0, over fa25c9b1, superseded);
  - predict_5.out (rc 0, **the pinned run**, over 4db87c3e);
  - predict_sim_mergedT2b_1.out (rc 0) and predict_sim_foreign1261_1.out (rc 1);
  - pins_gate24T2c.json and its SIM files.
- **Prompt and launcher:**
  - prompt_gate24T2c.TEMPLATE.txt and launcher_gate24T2c.TEMPLATE.sh.txt;
  - fill_gate24T2c.py with fill_1..4.out (fill_1/2 rc 1: the fill's own seat-item and keyword guards caught two template slips; fill_3 rc 0 over fa25c9b1; fill_4 rc 0 is the pinned fill; `.pre-*` files are earlier fills);
  - the rendered prompt `2026-09-26_secuura-batch1245r2-t2.prompt.txt`;
  - the launcher `launch_qa_secuura_batch1245r2-t2.sh` (`bash -n` rc 0);
  - launcher_check_1.out (rc 0, over fa25c9b1) and launcher_check_2.out (rc 0, over 4db87c3e).
- **Repin and controls:** repin_and_launch_gate24T2c.sh with repin_dryrun_1/2.out; controls_gate24T2c.sh with controls_1.out/.rc (normal), controls_2.out/.rc (inverted) and
  controls_0_aborted_devmove.out/.rc (QUARANTINED).
- **Captured reads:**
  - capture_mail_gate24T2c.py → mail_gate24T2c_ready.md, mail_ready_{1245r2,1256,1257_1260,1261}.md and mail_l5_declared_counts.md (TEXT_SHA256 each,
    all EQUAL to the first reads raw_*.txt; 9 prior-report sha256s);
  - gh_read_gate24T2c.py with gh_read_1.out, gh_body_<n>.md and gh_comments_<n>.md;
  - linear_reads_gate24T2c.py with linear_reads_1.out and linear_KS-*.md;
  - lsremote_1.out.
- **Drafter's live probe (PREDICTION only):** drafter_liveshape_g24c.py; liveshape_1.out (H7b VOID: the drafter's `--silent` swallowed the file argument);
  liveshape_2.out (the read one).
- `_sp/`: the scratch clone, the drafter's vitest install, the live fixtures (`_sp/live2/`, results.json) and the control workdirs. The launch command excludes it.

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, commit, push or routing-conf write.
- The Secuura checkout was touched only by read verbs: ls-remote, config --get, and `clone --no-local` reading it as a source.
- The seat records were read as plain files.
- The inbox was read only in the one permitted form (`inbox_digest.sh full wednesday-agent@agentmail.to '<id>'`): 5 ids, each read twice (once by hand,
  once by the capture script).
- **UNMEASURED:**
  - every PR's red arms and every package / suite count;
  - lint, tsc, bash -n of the changed scripts in a worktree, prettier, knip;
  - #1245 through the REAL function: L2 and L3/E5/E6 (the drafter used a byte-lifted reader and its own spawnSync driver, never childSuiteCounts);
  - T-CALL (i)–(iv) (READ only);
  - L4's byte comparison of the committed captures;
  - #1261 REVERT-SKIPS through the real jest suite (a port only);
  - NODNS-EGRESS: whether `anchoring` resolves on this box, and how long it takes (not probed: the drafter made no DNS query);
  - #1256 BACKTICK / NAMED-FACTORY / SELF-SCAN reach;
  - #1257's leak count on BASE;
  - #1258's 61 s red;
  - #1259's red copy;
  - #1260's lifted per-site and region runs;
  - the errexit death on bash ≥ 4.1 (no such bash on the box);
  - #1256's own push record (overwritten; only another drafter's reads survive, and they carry no branch name);
  - the seats' login_stub counts, `.git/config` hash and porcelain claims;
  - the usage gate and machine load at launch;
  - the real launch path (steps 4–6);
  - END_TREE over all 5,040 orders (53 were run);
  - a real gate24T2b squash (only the P-T2Bm simulation).
- **Not controlled:** exit 16 (it needs a TTY), the repin's `mergeable=False` refusal, steps 4–6.
