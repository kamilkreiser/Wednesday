# Gateset 2026-09-22_gate19B_seatB — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE batch gate over Seat B 19th/20th's NINE PRs (#1182 #1184 #1186 #1194 #1196 #1198 #1199 #1200 #1201; READY 1-3 by Seat B 19th, READY 4-9 by Seat B
20th after the mid-series hand-over; Seat C 19th's twelve (#1180 #1181 #1183 #1185 #1187 #1188 #1190 #1191 #1192 #1193 #1195 #1197) interleave and
are gate19C's, NOT this gate's). TIER 1 on EIGHT (product/tooling bytes or an auth-adjacent surface: #1182 #1184 #1186 originate, #1196 kyc, #1198
#1199 security — the ONE same-file PAIR `Blockchain/Dev/services/security/src/index.ts`, #1200 systemTest/performance tooling, #1201 the ssrf-guard
tamper), TIER 2 on #1194 (KS-1229 test-only cells — the plan ANSWER). The drafter's FILE-RULE tier == the READY's proposal on 9/9 (the tier table in
DRAFTER_REPORT.md; #1201's tier-1 reading rests on the READY's tamper-file claim, which the prompt tells the gate to MEASURE). ELEVEN READYs (9 R16B
rows + 2 Claude-written goldens) as nine PRs; 17 distinct paths over 18 file rows (8 NEW test files + 6 product/tooling + 3 existing test files);
+642/-13 (the AMENDED count — KS-1164's ruled (b) whitespace rewrap; item 0's +639/-13 is the control); the all-11 tree over develop 3bad652d1 =
`3df72c02d3250ca584c591fd89734d3391d99337` (re-derived by REAL merge-tree chains in three orders in a scratch clone FROM ORIGIN — never `--shared`
from the checkout; the UNAMENDED control 34728affba20 re-derived too); the PAIR blob `2ad45cd8e5552d5d52e48749406203d149967073` / 1603 re-derived in
both orders. Produced in the shape of `gatesets/2026-09-22_gate19C_seatC/` (the gate15→18→19C pipeline), re-keyed.

## 0. THE DEVELOP PIN (unmoved; the launcher refuses if it moves)
Origin develop = `3bad652d17cf111c1e2e1bed1ae7686894637487` (tree cd9b0f6c7b84) at every READY (05:48Z … 07:52Z), at the 07:55:39Z HOLD, at the
drafter's ls-remote 07:59:11Z, fetch 08:05:10Z, fill 08:15:49Z / 08:18:11Z / 08:20:27Z, generator 08:17:56Z / 08:18:14Z and the launcher's own --check
08:18:20Z-08:18:57Z. Every head's parent IS 3bad652d1 (fast-forward; compare merge_base 3bad652d1 / ahead 1 / behind 0 / files 2/2/2/1/2/4/2/2/1 — the
launcher asserts exactly that, exit 10). **gate19C (Seat C 19th's twelve, the SAME base, a SEPARATE GO) is the likely mover: its report dir
`2026-09-22-batch1180-1197-r1/` already exists at the drafter's read, and its routing line is in inbox_routing.conf. If develop moves before the
launch:** `python3 predict_batch_scratch_gate19B.py <this session's scratchpad>` (refuses rc 9 unless the target is a scratchpad under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/`; clones FROM ORIGIN — bare, blob:none — over the checkout's ssh road; re-predicts every tree;
writes `newdev_tree.txt`; it ALREADY prints the COMBINED tree with both rounds landed over 3bad652d1: b4f2a8beaecd, C-then-B == B-then-C), then edit the
prompt DRAFT's THE SHAPE bullets, `python3 fill_prompt_gate19B.py`, then `python3 gen_launcher_gate19B.py <launcher> <that clone>` (it refuses rc 3
while round19B.DEV != origin — update round19B.py's DEV / DEV_TREE12 / SEAT_ALL11 deliberately from the re-prediction first).

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1182-1201.prompt.txt`
  (301 lines, 51121 B, sha256 `d20a94e4af7685c9cce49ddbcb0e871659286f5e64a190204598dbec2b640231` — fill run 3; runs 1-2 kept beside as `.pre-081811`
  / `.pre-082027`; first line `ultrathink`; no `deadbeef` literal; names the brief paths `fleet/briefs_staged/2026-09-22_raise_seatB_19.md` +
  `…raise_seatB_20.md` and the capture `mail_gate19B_ready.md`; TWELVE by-name items exactly as commissioned incl. the KS-1164 INSTRUMENT (the
  whitespace-stripped byte-stream equality, `git diff -w` named as NOT the instrument), the `--pair-blob` addendum note on #1199, the KEY-FREE
  SHIPS-WITH, READ-THE-WHOLE-TEST-FILE, the CONTEXT RULE and the gate19C BASE-moves note; the nine `PR #N is KS-x.` sentences; the MERGE ADDENDUM with
  ONE equality target per FILE — 2/2/2/1/2/4/2/2/1 = 18 over 17 paths, MG-2 on #1198 (FOUR), #1199's index.ts at the ALONE blob by construction with the
  PAIR note, #1200's test at the AMENDED blob; the drafter's leads (a)-(n); the NOT-PINNED candidates; the exact subject prefix; the GO string the
  seat expects VERBATIM).
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1182-1201.sh` (387 lines, mode 755,
  sha256 `760b904227551aee26c71dc267af5f35fd1acc0d5f5106e6ce78c2cdfcbce640` — generator run 3, 08:28:14Z) — pins develop 3bad652d1 + every head (branch AND refs/pull/N/head, exit 6);
  compare guard per PR (exit 10); the develop pin judged by CONTENT over the 17 target paths via the contents API when develop != the pin (LANDED
  19 / CHANGED 18 / disjoint 17); the grep ladder (126 BOTH tokens in the capture AND the prompt; 71 by-name keywords; tier lines; the PAIR exit 35;
  the KS-1164 instrument exit 36; PARTIAL exit 34; thinking directive + brief path exit 8); overrides `QAB1182_*` refuse at launch (16); TTY (21).
  `--check` is headless (~40 s).
- `DRAFTER_REPORT.md` — slips FIRST, every count with its command, NOT MEASURED, the tier table.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1182-1201.sh --check
  Drafter's runs: `launcher_check_1.out` rc 0 at 08:18:20Z-08:18:57Z (the run-2 launcher); `launcher_check_2.out` rc 0 at 08:28:14Z-08:29:28Z (the
  run-3 launcher, after the controls). Controls end: 12 OK / 1 MISMATCH (U: rc 33 before 35 by ladder order — still a refusal; DRAFTER_REPORT.md section 7). The controls (`launcher_controls_gate19B.sh`, `launcher_check_controls.out` — read its "controls end" line): C wrong head
  (#1201) -> 6 · D develop at the stale 581ed7fa1 -> 17/18/19 (any = a stale sha refused) · E develop at #1182's head -> 19 LANDED · G no thinking
  directive -> 8 · S PARTIAL -> 34 · O RULE WHETHER IT BLOCKS reworded -> 30 · L by-name reworded -> 33 · I #1198 demoted -> 7 · U `alone blob`
  reworded -> 35 · W the instrument line reworded -> 36 · T a BOTH token altered -> 30 · N non-TTY launch -> 21 · POSITIVE -> 0.

## 3. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1182|coagent@agentmail.to|yes
  `repin_and_launch_gate19B.sh` step 0 asserts it (rc 1 if absent; control: the batch1180 line's count = 1). The drafter's read 08:19Z: batch1182 ABSENT (0), batch1180 present (1).

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate19B_seatB/repin_and_launch_gate19B.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1182-1201.sh
  Reads its pins FROM THE LAUNCHER (the sed dry-read in DRAFTER_REPORT.md prints develop 3bad652d1 + the nine `n:head:branch` rows + the prompt
  path): (0) routing line; (1) ls-remote develop + every pull head + branch (`lsremote_launch.out`); (2) the PULLS API (`api_heads_launch.out`); (3)
  rc 10 if develop is not the pin, rc 11 if any head moved or a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own
  `--check` (rc 13); (6) `cockpit.sh add QA/Secuura-batch1182 <launcher>` (rc 14) + a pane census. `bash -n` rc 0; NOT RUN by the drafter.

## 5. What is in this directory
  COMMISSION.md · mail_seatB20_status_hold.md (Wednesday's own HOLD capture, untouched) · round19B.py (+ round19B_selfcheck.out: 9 PRs, 18 file rows /
  17 paths, 19 canon rows, +642/-13, TIER1 by FILE rule == READY 9/9, B ∩ C NONE) · capture_ready_mail_gate19B.py / capture_ready_mail_1.out (+ .rc) —
  mail_seatB19_ready01..03_*.md, mail_seatB20_ready04..09_*.md, mail_seatB19_status_0524.md, mail_seatB20_status_0709.md / _0755.md (the HOLD), the
  QUESTION / wrap mails, mail_wed_*.md ×7, mail_wedC_*.md ×3 (the S1 addendum, the (2') addendum, the band addendum to C), mail_seatC19_*.md ×4
  (STATUS / QUESTION / wrap — context); the combined mail_gate19B_ready.md (the launcher greps it; 0 `NOT YET ARRIVED`) · parse_readys_gate19B.py /
  parse_readys_1.out (the compact pin table the round file was built from) · checkout_counts.sh + checkout_counts_before.txt / _after.txt (+ .rc) ·
  lsremote_1.out (+ .rc; 07:59:11Z) · loose_objects_1.out (+ .rc) · predict_batch_scratch_gate19B.py / predict_batch_scratch_1.out (+ .rc) /
  newdev_tree.txt · gh_pr_reads_gate19B.py / gh_pr_reads_1.out (+ .rc) · linear_reads_gate19B.py / linear_reads_1.out (+ .rc) ·
  prompt_gate19B.DRAFT.txt (+ .pre-HHMM-rc0count) + fill_prompt_gate19B.py / fill_prompt_1..3.out (+ .rc) · launcher_template_gate19B.sh.txt +
  gen_launcher_gate19B.py / gen_launcher.run1..3.out (+ .rc) · launcher_check_1.out / _2.out (+ .rc) · launcher_controls_gate19B.sh /
  launcher_check_controls.out / launcher_controls.start.txt · repin_and_launch_gate19B.sh (NOT run) · README.md · DRAFTER_REPORT.md.

## 6. Leads for the gate (full text in DRAFTER_REPORT.md section 3; all in the prompt as leads (a)-(n))
  (a) the KS-1164 amendment — the INSTRUMENT (drafter: True; control False; `git diff -w` rc 1 / 1228 B) · (b) the hand-over — every head unchanged
  across it · (c) F-GUARD 06:14:10Z and the (2') predicate + refusal control · (d) the 20th's S1 zero-ref fetches · (e) the 20th's S2-S4 · (f) the
  19th's S1-S7 · (g) the lock windows · (h) no exec-bit file (drafter: 18/18 rows 100644) · (i) the kyc preload timeout · (j) #1184's `complete…`
  word (drafter's detector 0/2/2), #1194's `ks1213` path token, the archived-title reads on KS-730 / KS-1028 · (k) KS-1179's typecheck delta -1 ·
  (l) the census REPORT rows · (m) loose objects (drafter: 0 after 07:57Z) · (n) F-BATCH octopus. ONE drafter-vs-seat VALUE disagreement: NONE —
  every pinned value re-derived EQUAL (9/9 heads, trees, 18/18 blobs + lines, 19/19 canonicals + 8/8 patch.diff sha16s, the all-11 tree in 3 orders, the
  unamended control, the pair both orders, the shortstat, the KS-1164 instrument True / control False).

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no queue / READY-file touch, no write into the Secuura checkout (ls-remote / status / for-each-ref /
  count-objects / config --get / cat-file -t / find over .git/objects / ls of .git/worktrees only; every write verb in the scratch clone FROM ORIGIN
  under the scratchpad guard; `count-objects -v` byte-identical before/after), no `inbox_routing.conf` write, no key printed, no port connected except
  `git ls-remote` / `git clone` / `git fetch` FROM ORIGIN and the GitHub / AgentMail / Linear READ APIs; no Datasec mail opened or listed. Nothing
  written into the gate19C dir (READ only: COMMISSION, README, DRAFTER_REPORT, round19C.py, the scripts, the controls output).

## 8. Re-finishing from disk after any change (a cold successor)
  In order: (a) `python3 …/capture_ready_mail_gate19B.py` (idempotent; never overwrites); (b) `python3 …/predict_batch_scratch_gate19B.py <this
  session's scratchpad>`; (c) `python3 …/gh_pr_reads_gate19B.py` and `python3 …/linear_reads_gate19B.py`; (d) `python3 …/fill_prompt_gate19B.py`;
  (e) `python3 …/gen_launcher_gate19B.py <launcher> <the scratch clone from (b): …/predict19B.*/origin.git>`; (f) `<launcher> --check`; (g) `bash
  …/launcher_controls_gate19B.sh <launcher> <prompt>` (read the "controls end" line — 0 MISMATCH); (h) read the prompt WHOLE; (i) section 3, then 4.
