# Gateset 2026-09-22_gate19C_seatC — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE batch gate over Seat C 19th's TWELVE PRs (#1180 #1181 #1183 #1185 #1187 #1188 #1190 #1191 #1192 #1193 #1195 #1197; Seat B 19th/20th's numbers
interleave: #1182 #1184 #1186 #1194 #1196 #1198 #1199 are NOT this gate's; #1189 is this seat's CLOSED twin of #1190). TIER 1 on the NINE bash_patch
script PRs (the commission's FILE RULE names six scripts — #1185 check-no-demo-mutation.sh and #1192 validate-lint.sh are tier 1 by the brief / the
READYs and UNNAMED by the rule: the prompt grades them at tier-1 weight and asks the gate to STATE BOTH; see DRAFTER_REPORT.md lead (a)); TIER 2 on
the three KS-1097 docs PRs. FOURTEEN READYs (13 R16B rows + 1 Claude-written PRPROCESS) as twelve PRs; 21 distinct paths over 22 file rows (10 NEW
suites + 8 scripts + 3 docs; Start_Up/start-secuura.sh the ONE same-file PAIR #1180 + #1181 — the merging seat passes
`--pair-blob Start_Up/start-secuura.sh=58cdd3dc846b730e9f7eb5b517a6e4108ac05fdb` (mode 100755) on #1181 after #1180); +915/-29; the all-12 tree over
develop 3bad652d1 = `5a8458a5697f7ee5b1800864b9f49347c8cbe34e` (re-derived by REAL merge-tree chains in three orders in a scratch clone FROM ORIGIN —
never `--shared` from the checkout). Produced in the shape of `gatesets/2026-09-22_gate18C_seatC/` (the gate15→18 pipeline), re-keyed; the prompt is
SHORTER than 18C's (264 lines vs 1141) under the commission's ~60 min bound — every commissioned item is in it by name; the per-PR blocks carry the
READYs' numbers for the gate to VERIFY.

## 0. THE DEVELOP PIN (unmoved; the launcher refuses if it moves)
Origin develop = `3bad652d17cf111c1e2e1bed1ae7686894637487` (tree cd9b0f6c7b84 — the 18th round's END tree) at every READY (05:24Z … 07:20Z), at the seat's
07:22:26Z HOLD, at the drafter's ls-remote 07:28:09Z, fetch 07:33:34Z, fill 07:43:17Z / 07:48:01Z, generator 07:47:23Z / 07:48:07Z and the launcher's
own --check 07:48:12Z-07:49:43Z. Every head's parent IS 3bad652d1 (fast-forward; compare merge_base 3bad652d1 / ahead 1 / behind 0 / files
2/2/2/2/3/2/2/2/2/1/1/1 — the launcher asserts exactly that, exit 10). **If develop moves before the launch (Seat B 20th's GO landing its merges is the
likely mover — a disjoint move by the partition, still a re-pin):** `python3 predict_batch_scratch_gate19C.py <this session's scratchpad>` (refuses rc 9
unless the target is a scratchpad under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/`; it clones FROM ORIGIN — bare, blob:none — over the
checkout's ssh road and re-predicts every tree; it writes `newdev_tree.txt`), then edit the prompt DRAFT's THE SHAPE bullets, `python3
fill_prompt_gate19C.py`, then `python3 gen_launcher_gate19C.py <launcher> <that clone>` (it refuses rc 3 while round19C.DEV != origin — update
round19C.py's DEV / DEV_TREE12 / SEAT_ALL14 deliberately from the re-prediction first).

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1180-1197.prompt.txt`
  (264 lines, 42997 B, sha256 `620dfda995336934db8ab04954820c0a9d2443dc5fe1850107a5f04029fba816`; first line `ultrathink`; no `deadbeef` literal; names the brief path
  `fleet/briefs_staged/2026-09-22_raise_seatC_19.md` and the capture `mail_gate19C_ready.md`; TWELVE by-name items exactly as commissioned incl. the
  MODES / F-HOOK item, the `--pair-blob` addendum note on #1181, the KEY-FREE SHIPS-WITH, READ-THE-WHOLE-TEST-FILE and the CONTEXT RULE; the twelve
  `PR #N is KS-x.` sentences; the MERGE ADDENDUM with ONE equality target per FILE — 2/2/2/2/3/2/2/2/2/1/1/1 = 22 over 21 paths, MG-2 on every script
  line, #1181's start-secuura.sh at the ALONE blob by construction with the PAIR note, modes stated; the drafter's leads (a)-(k); the NOT-PINNED
  candidates; the exact subject prefix; the GO string the seat expects VERBATIM).
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1180-1197.sh` (368 lines, mode 755,
  sha256 `9889eb579302270f8c14e82ccf710eb927077e77795a82ec7540b9dce93804e2`) — pins develop 3bad652d1 + every head (branch AND refs/pull/N/head, exit 6); compare guard per PR (exit 10);
  the develop pin judged by CONTENT over the 21 target paths via the contents API when develop != the pin (LANDED 19 / CHANGED 18 / disjoint 17);
  the grep ladder (116 BOTH tokens in the capture AND the prompt; 59 by-name keywords; tier lines; the PAIR exit 35; PARTIAL exit 34; thinking
  directive + brief path exit 8); overrides `QAB1180_*` refuse at launch (16); TTY (21). `--check` is headless (~90 s).
- `DRAFTER_REPORT.md` — slips FIRST, every count with its command, NOT MEASURED, the tier table.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1180-1197.sh --check
  Drafter's run: `launcher_check_1.out` rc 0 at 07:48:12Z-07:49:43Z. The controls (`launcher_controls_gate19C.sh`, `launcher_check_controls.out` —
  read its "controls end" line): C wrong head (last PR) -> 6 · D develop at the stale 581ed7fa1 -> 17 · E develop at #1180's head -> 19 LANDED · G no
  thinking directive -> 8 · S PARTIAL -> 34 · O RULE WHETHER IT BLOCKS reworded -> 30 · L by-name reworded -> 33 · I #1190 demoted -> 7 · U --pair-blob
  reworded -> 35 · T a BOTH token altered -> 30 · N non-TTY launch -> 21 · POSITIVE -> 0.

## 3. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1180|coagent@agentmail.to|yes
  `repin_and_launch_gate19C.sh` step 0 asserts it (rc 1 if absent; control: the batch1167 line's count = 1). The drafter's read: batch1180 ABSENT (0), batch1167 present (1).

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate19C_seatC/repin_and_launch_gate19C.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1180-1197.sh
  Reads its pins FROM THE LAUNCHER (the sed dry-read in DRAFTER_REPORT.md prints develop 3bad652d1 + the twelve `n:head:branch` rows + the prompt
  path): (0) routing line; (1) ls-remote develop + every pull head + branch (`lsremote_launch.out`); (2) the PULLS API (`api_heads_launch.out`); (3)
  rc 10 if develop is not the pin, rc 11 if any head moved or a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own
  `--check` (rc 13); (6) `cockpit.sh add QA/Secuura-batch1180 <launcher>` (rc 14) + a pane census. `bash -n` rc 0; NOT RUN by the drafter.

## 5. What is in this directory
  COMMISSION.md · round19C.py (+ round19C_selfcheck.out: 12 PRs, 22 file rows / 21 paths, 24 canon rows, +915/-29, TIER1 by FILE rule vs READY) ·
  inbox_list_gate19C.py / inbox_list_1.out (subjects only; Datasec never fetched) · capture_ready_mail_gate19C.py / capture_ready_mail_1.out (+ .rc) —
  mail_seatC19_ready01..12_*.md, mail_seatC19_status_0508.md / _0722.md (the HOLD; Wednesday's own earlier capture `mail_seatC19_status_hold_0722.md`
  sits beside, untouched), the two QUESTION mails, mail_wed_*.md ×5, Seat B's mails beside (mail_seatB19_*, mail_wedB_*) as CONTEXT; the combined
  mail_gate19C_ready.md (the launcher greps it; 0 `NOT YET ARRIVED`) · lsremote_1.out (+ .rc; 07:28:09Z) · checkout_counts_before.txt / _after.txt
  (+ .rc) · loose_objects_1.out (+ .rc) · predict_batch_scratch_gate19C.py / predict_batch_scratch_1.out (+ .rc) / newdev_tree.txt ·
  gh_pr_reads_gate19C.py / gh_pr_reads_1.out (+ .rc) · linear_reads_gate19C.py / linear_reads_1.out (+ .rc) · prompt_gate19C.DRAFT.txt +
  fill_prompt_gate19C.py / fill_prompt_1..2.out (+ .rc) · launcher_template_gate19C.sh.txt + gen_launcher_gate19C.py / gen_launcher.run1..3.out (+ .rc)
  · launcher_check_1.out (+ .rc) · launcher_controls_gate19C.sh / launcher_check_controls.out / launcher_controls.start.txt ·
  repin_and_launch_gate19C.sh (NOT run) · README.md · DRAFTER_REPORT.md.

## 6. Leads for the gate (full text in DRAFTER_REPORT.md section 3; all in the prompt as leads (a)-(k))
  (a) the TIER GAP on #1185 / #1192 · (b) F-HOOK + fixmodes19 on every push from #1190 (six -fixmodes.out files listed) · (c) two runners in one
  worktree · (d) the guard log line vs the (2') predicate · (e) S7 / the watcher since · (f) check_shared_relink tally-only · (g) the lock polls
  0/0/4/6/4/5/0/0/0/0/0/5 · (h) the docs PRs' D4-D8 · (i) #1190's cat(s1,s2) != patch.diff · (j) the drafter's own pull/1199 control slip · (k)
  F-BATCH octopus vs sequential ort. ONE drafter-vs-seat VALUE disagreement: NONE — every pinned value re-derived EQUAL (12/12 heads, trees, blobs,
  modes, 24/24 canonicals, the all-12 tree in 3 orders, the pair both orders, the shortstat).

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no queue / READY-file touch, no write into the Secuura checkout (ls-remote / ls / config --get /
  status / for-each-ref / count-objects / cat-file -t only; every write verb in the scratch clone FROM ORIGIN under the scratchpad guard), no
  `inbox_routing.conf` write, no key printed, no port connected except `git ls-remote` / `git clone` / `git fetch` FROM ORIGIN and the GitHub /
  AgentMail / Linear READ APIs; no Datasec mail opened or listed. Nothing written into any other gateset dir.

## 8. Re-finishing from disk after any change (a cold successor)
  In order: (a) `python3 …/capture_ready_mail_gate19C.py` (idempotent; never overwrites); (b) `python3 …/predict_batch_scratch_gate19C.py <this
  session's scratchpad>`; (c) `python3 …/gh_pr_reads_gate19C.py` and `python3 …/linear_reads_gate19C.py`; (d) `python3 …/fill_prompt_gate19C.py`;
  (e) `python3 …/gen_launcher_gate19C.py <launcher> <the scratch clone from (b): …/predict19C.*/origin.git>`; (f) `<launcher> --check`; (g) `bash
  …/launcher_controls_gate19C.sh <launcher> <prompt>` (read the "controls end" line — 0 MISMATCH); (h) read the prompt WHOLE; (i) section 3, then 4.
