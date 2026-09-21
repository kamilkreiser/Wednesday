# Gateset 2026-09-21_gate1130to1135 — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING)

ONE batch gate over Seat B 14th's SIX PRs #1130-#1135 on develop `9f0265eb06ecf24d4de18149ce862ad2330a61ee` (unmoved), graded TIER 1
(floor #1132 KS-958, #1133 KS-880, #1134 KS-887, #1135 KS-1236 + KS-1006; tiers 2/2/1/1/1/1 in push order 1 2 6 3 5 4 = #1130 #1131 #1132 #1133
#1134 #1135 per your 08:03:24Z ANSWER Q6). FIVE test-only + #1132's TWO product lines on the re-link PUSH GUARD (`check-shared-relink.sh` -2/+2,
preflight leg 13) + its NEW suite. ONE same-file pair (#1133 / #1134 on `ks869-connector-id-persisted.test.ts`, disjoint hunks, one blob
`dcd3efaaf45a` either order). Produced in the exact shape of `gatesets/2026-09-21_gate1119to1128/`. Everything below is read-only evidence or a
file for YOU to run. **If the drafter was killed mid-run, section 8 says how a cold successor finishes from disk.**

## 1. Read WHOLE before launching
- The prompt (931 lines, 125767 bytes, sha256 e9b24f21bb31d496d30f9706af59d1f7fc90cab61463e19c2edad189b0b5fd52; first line `ultrathink`):
  `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1130-1135.prompt.txt`
  It carries your rulings exactly: tiers 2/2/1/1/1/1, batch tier 1; every ticket STAYS In Progress, no tickets filed by the gate (KS-1273's and
  KS-958's Done are YOUR closing pass); the MERGE ADDENDUM with ONE equality target per FILE (1/1/2/1/1/1 — #1132's two comma-separated; #1135 ONE
  despite two READYs — MG-2, targets15.py:28/:31/:37); the MG-3 key-set rule per squash body (merge15.py:54-:65; TWO keys on #1135 only); the PAIR's
  addendum (#1133 / #1134 each ALONE over the GO's develop; the second to merge graded by merge15.py's re-prediction, :83-:89); the two DECLARED
  covers (EXITCODEFLAGGONE's two #1122 cells; DRIVERTHROWS's seven) as covers the gate measures; the seat's S6 (harness dist) + attempt 1 and S8
  (an unrendered PR number in READY 5, corrected) as recorded facts, NOT findings on the product; report.md BEFORE the verdict mail; NOT PINNED
  rows in the PRIOR report's format with BY DESIGN rows; the namespace guard (KS-1129..KS-1137 are real tickets — KS-1130 / KS-1134 ARCHIVED,
  KS-1135 is PR 2's OWN ticket while PR #1131 is its PR; PR #887 is OPEN and is KS-961's); SEVENTEEN by-name items; the LEADS (the hook's
  Blockchain/Dev trigger — a systemTest-only push ran NO preflight legs; the completeness-detector artefact on #1132; READY 3's / READY 4's census
  multiplicity frames; the new suite's mode 100644; KS-973 live on #989; #1129 measured as a docs-only chore PR with NO path conflict).
- The launcher (513 lines, sha256 3697f1eaa5776e544349d337e8544ec2f850773c643e8adc4d28494ac08896e8, mode 755):
  `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1130-1135.sh` — pins develop + the six heads (branch AND refs/pull/N/head, exit 6);
  compare guard per PR merge_base/ahead=1/behind=0/files 1/1/2/1/1/1 (exit 10 on any move); the develop pin judged by CONTENT over 36 paths
  (6 PR paths — 5 develop blobs + 1 ABSENT, LANDED → 19 incl. the PAIR blob; 4 tamper files; 26 unchanged-read paths → 18); prompt + READY greps
  7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33 (176 BOTH tokens; 96 by-name keywords); overrides refuse at launch (16); TTY (21).
  `--check` is headless and launches nothing (~90 s: 6 compare GETs + 36 contents GETs).
- `DRAFTER_REPORT.md` — every value beside its instrument, the leads, the drafter's own slips FIRST, what is UNMEASURED.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1130-1135.sh --check
  Drafter's run: `launcher_check_1.out` rc=0 at 09:43:24Z-09:44:52Z (19:43 AEST).

## 3. The routing line — ADDED BY THE DRAFTER (backup beside)
  `fleet/inbox_routing.conf` now carries `QA/Secuura-batch1130|coagent@agentmail.to|yes` (appended 09:45:10Z; the backup
  `inbox_routing.conf.pre-batch1130-094510` sits beside it; `diff` = that one added line). `repin_and_launch_1130.sh` step 0 asserts it
  (rc 1 if absent; control: the batch1119 line's count = 1).

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/repin_and_launch_1130.sh
  It: (0) asserts the routing line; (1) `git ls-remote` develop + the six pull heads + the six branch globs (READ, into `lsremote_launch.out`);
  (2) re-reads the six heads from the PULLS API (`api_heads_launch.out`); (3) refuses rc 10 if develop is not 9f0265eb0, rc 11 if any head moved or
  a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own `--check` (rc 13, `launcher_check_launch.out`); (6)
  `cockpit.sh add QA/Secuura-batch1130 <launcher>` (rc 14, `cockpit_add.out`) and a pane census. `bash -n` rc 0; sha256 a6dbd89bd8a6ddef4d571f68856648f47d6250d48f91111d81b11b3e0851525a; NOT RUN by the drafter.

## 5. What is in this directory (all read-only evidence unless named above)
  COMMISSION.md — Wednesday's commission (19:01 AEST)
  poll_ready_1130.sh / .log / inbox_all_1.out + inbox_all_pollN.out — the bounded inbox poller (`inbox_digest.sh --all`, never marks seen); stopped at six READYs 09:33:38Z
  capture_ready_mail_1130.py / capture_ready_mail_N.out — the SIX READYs + READY 5's CORRECTION + the two STATUS mails + the two QUESTIONs + Wednesday's
    two ANSWERs + the brief as sent + the 09:33 "ALL SIX READ", VERBATIM by message id (TEXT_SHA256 per file): mail_seatB14_ready01_pr1_ks1273.md …
    ready06_pr4_ks1236.md · mail_seatB14_ready05_pr5_ks887_CORRECTION_0924.md · mail_seatB14_status_0833.md · mail_seatB14_status_0934.md ·
    mail_seatB14_question_question_plan_confirmation_seat_b_14th_0800.md · mail_seatB14_question_question_pr_1_push_refused_by_preflight__0843.md ·
    mail_wed_answer_plan_confirmation_seat_b_14th_0803.md · mail_wed_answer_pr_1_push_refused_by_preflight_le_0844.md ·
    mail_wed_successor_seat_b_14th_raise_five_held_lo_0740.md · mail_wed_all_six_read_wait_for_the_batch_gate_and_0933.md ·
    mail_batch1130_ready.md (the combined capture the launcher greps: the six READYs in push order + the CORRECTION after section 05 + the STATUS mails + the QUESTIONs)
  lsremote_1.out / checkout_counts_before.txt — origin + the checkout's counts at 09:06:51Z (BEFORE)
  shape_1130.py / shape_N.out — local object reads (parents, trees, blobs, modes, the tamper `from` counts at develop, the run-dir reads, the hook/preflight lines); shape_4.out is the all-six read
  predict_batch_scratch_1130.py / predict_batch_scratch_N.out — REAL 3-way merges in a --shared scratch clone: predict_batch_scratch_2.out = all six in SIX orders → 60bd96e7078c…, the PAIR both orders → 9e5dec6aef20 / blob dcd3efaaf45a, the FOUR → 6eeef3623e8a, controls, count-objects byte-identical
  gh_pr_reads_1130.py / gh_pr_reads_N.out / gh_body_checks.out — GitHub GETs (heads, bases, files API, Refs, detectors, compares, ruleset, open-PR sweep incl. #1129, the PR-number trap; the live-body wording reads)
  linear_reads_1130.py / linear_reads_N.out — Linear reads (the seven tickets, attachmentsForURL per PR, KS-1129..KS-1137, the 17 archived, the 26 live-foreign, controls)
  prompt_1130.DRAFT.part1..5.txt + fill_prompt_1130.py / fill_prompt_N.out — the prompt's five parts and the fill script (substitutes the PR numbers / heads / READY times from the captures; refuses on any residual token)
  gen_launcher_1130.py + gen_launcher.runN.out — the generator (run 1: ten BOTH-list misses — two 40-hex pair values the READYs print as 12-hex, three cell titles the READYs never carry, five prompt wording gaps; run 2: a comment that swallowed a line — a generator SyntaxError; run 3: four by-name phrases wrapped across lines; run 4: written)
  launcher_check_1.out (rc 0) · launcher_controls_1130.sh + launcher_check_controls.out (controls A-S + positive, each rc) · controls_dir_1130.txt
  prompt_keyword_counts.out — the keywords with absent-by-design controls at 0
  repin_and_launch_1130.sh — the launch action (NOT run)
  *.S2-/S5-/S6-*-pre-fix — the drafter's pre-fix copies

## 6. Leads for you (full text in DRAFTER_REPORT.md; the gate grades them; NO drafter-vs-seat VALUE disagrees)
  1 READY 2's NO PREFLIGHT VERDICT — `.githooks/pre-push` :4 / :76 fires only on Blockchain/Dev changes; a systemTest-only push is ungated while
  run-shell-suites.sh counts systemTest's 12 suites among its 43 — design or gap? a Polish / ticket CANDIDATE for YOU · 2 the completeness detector
  fires 0/1/0 on #1132's negated "whether the ticket is complete" (the #1122 artefact) · 3 READY 3's census "attempts 30 / established 30" vs
  SPECIFICS "10 / 10", READY 4's "21 runs … attempts 1896" vs "208 per whole-suite run" — multiplicity frames · 4 #1132's new suite is mode 100644
  (16 of 31 scripts/__tests__/*.test.sh at develop are 100644) — how run-shell-suites.sh reaches it · 5 the seat's S6 (a missing dist in the
  pushing worktree) vs F6 / INT-1 — one class, two or three? · 6 READY 5's unrendered `#1133` (the seat's S8, corrected; NOT in the PR body —
  the drafter's live-body read) and the body's overlap statement that names no partner PR number · 7 PR #887 OPEN = KS-961's (namespace) ·
  8 KS-1130 / KS-1134 ARCHIVED namespace tickets; KS-1135 = PR 2's OWN ticket · 9 the linear[bot] walks (KS-1135 08:56:00Z, KS-958 09:05:10Z,
  KS-887 09:21:05Z) · 10 KS-973 live on #989 (the seat's F1) · 11 #1129 = a docs-only chore PR (history.md) — NO path conflict, measured by the
  files API · 12 the drafter PREDICTS run-shell-suites reachability 43 → 44 on the all-six tree · 13 the seat's S7 appears in no mail (S1-S6 + S8 do).

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no PAUSE_QUEUE / queue.md / done.md / READY-file touch, no write into the Secuura checkout (ls-remote /
  show / cat-file / rev-parse / rev-list / diff / ls-tree / log / grep / status / for-each-ref / count-objects only; the scratch clones live in the
  drafter's scratchpad), no key printed, no port connected except `git ls-remote` + the GitHub / AgentMail / Linear READ APIs; ONE write outside
  the gateset: the routing line (section 3, backup beside).

## 8. If the drafter was killed — how a cold successor finishes from disk
  The six READYs are captured and the artefacts exist. In order: (a) `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/poll_ready_1130.sh` is NOT needed (all six landed 09:33Z); re-run
  `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/capture_ready_mail_1130.py` once to pick up any later seat mail (idempotent; never overwrites); (b) if the prompt parts were edited
  after the last fill, `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/fill_prompt_1130.py` (prints lines/bytes/sha256; backs up a differing previous prompt beside it); (c) if the
  prompt or the capture changed, `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/gen_launcher_1130.py /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1130-1135.sh` (refuses on any pin move, BOTH-list or by-name miss; writes only on bash -n 0);
  (d) `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1130-1135.sh --check` (rc 0 expected); (e) read `launcher_check_controls.out` — if it lacks the "controls end" line, re-run
  `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/launcher_controls_1130.sh` (25 min; each control names its rc); (f) read the prompt WHOLE; (g) `/bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/repin_and_launch_1130.sh`.
  The generator's own sha256 is 0fb898633abb92911393db2f64e00ba809658bc156e672ac9c461cd9f78f27f1.
