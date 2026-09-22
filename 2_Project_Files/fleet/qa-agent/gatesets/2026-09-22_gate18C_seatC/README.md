# Gateset 2026-09-22_gate18C_seatC — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE batch gate over Seat C 18th's SIX PRs (#1167, #1168, #1169 consecutive, then #1171, #1173, #1175 — Seat B 18th's gate18B holds #1170, #1172,
#1174, #1176, #1177, #1178, #1179): TIER 1 on FOUR (#1167 KS-947 the MFA-limiter auth-surface pin; #1171 KS-1231, #1173 KS-1246, #1175 KS-1257 the
three code_patch PRs with PRODUCT bytes on api-gateway), TIER 2 on #1168 KS-1123 and #1169 KS-1192. SEVEN local-model R16 round-2 READYs (three run
patches strict + four code_patch runs applied per SECTION file, the ONE `.opts` accommodation on KS-1231 Part B section 1 — the same blob strict)
grouped by TICKET = by FILE into six PRs on ONE lane (api-gateway vitest); 10 distinct paths (5 A + 5 M over 11 file rows — `health.ts` is the ONE
same-file PAIR between #1171 Part B and #1173: the merging seat passes `--pair-blob …health.ts=ae6017a84cf7aff42e17e1fe06ed66032e513d8c` on #1173
after #1171), +1008/-15; the all-6 tree over develop 8c2f7b3fd = `52853c8bf6c4ff43585cdade61c637ff8cbaa5d0` (re-derived three + four orders, incl.
#1173 before #1171). Produced in the exact shape of `gatesets/2026-09-22_gate16C_seatC/` (the gate15/16 pipeline), re-keyed. A FIRST drafter on this
commission died on an API 529 at ~10:5x AEST after its captures / shape / predict runs (its artefacts are kept beside: `capture_ready_mail_1/2.out`,
`shape_1/2.out`, `predict_batch_scratch_1/2.out`, `lsremote_1.out`, `checkout_counts_before.txt`); THIS drafter re-read every pin from origin
(`lsremote_2.out` 01:13:31Z), re-ran shape / predict (runs 3, under the commission's cwd guard) and wrote everything below. **The two gates
(gate18B over Seat B's seven, gate18C over these six) are INDEPENDENT by the partition: each gate clones `--shared` from the same checkout into ITS
OWN report dir / mktemp clones and never enters the other's; they may run in parallel on the same `.git` (read-only, no ref write by either) — the
launcher's develop pin refuses (exit 10 / 18 / 19) if the OTHER seat's GO lands its merges first, which is a re-pin, not a defect.**

## 0. THE DEVELOP PIN (the #1036 squash; unmoved since — the launcher refuses if it moves)
Origin develop = `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (tree `04b05e093ad8…`; the KS-763 #1036 squash the seat itself wrote FIRST at 22:54:41Z
on Wednesday's separate GO) at every READY (23:37Z … 00:32Z), at the seat's 00:42:07Z HOLDING STATUS, at Seat B 18th's 01:08:36Z HOLD, at the
drafters' 00:40:42Z / 01:13:31Z / 01:20Z (predict (c)) / 01:42:09Z (fill) / 01:49:5xZ (--check) reads. Every head's parent IS 8c2f7b3fd, so each PR
alone over develop is a fast-forward (merged tree = head tree) and the compare reads merge_base 8c2f7b3fd / ahead 1 / behind 0 / files 1/1/1/4/2/2
(the launcher asserts exactly that, exit 10). Seat B 18th's seven commits sit on 3916eacd1 (BEFORE the squash) — their compares read behind 1 against
8c2f7b3fd; that is the SIBLING gate's shape, not this one's. **If develop moves before the launch (Seat B 18th's GO landing its seven merges is the
likely mover — a disjoint move by the partition, still a re-pin):** `python3 predict_batch_scratch_gate18C.py <this session's scratchpad>` (it
refuses rc 9 unless the target is a scratchpad under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/`; it fetches the new tip BY SHA into its
own `--shared` scratch clone over the checkout's ssh road — never into the checkout — and re-predicts every tree), then `python3
gen_launcher_gate18C.py <launcher> <that clone>`, then re-read the prompt's THE SHAPE bullets (the move, the merged trees, the END STATE) and edit
`prompt_gate18C.DRAFT.part2.txt` accordingly before `fill_prompt_gate18C.py`.

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1167-1175.prompt.txt`
  (1141 lines, 158867 B, sha256 `fcf6dc1a6f7fa1fa13e60ba56c38be5f875845f16264837f6526702acb6ab0b5`; first line `ultrathink`; no `deadbeef` literal;
  TWELVE by-name items exactly as commissioned incl. the code_patch RED/GREEN protocol, the `--pair-blob` addendum note on #1173, the KEY-FREE
  SHIPS-WITH, the READ-THE-WHOLE-TEST-FILE rule and the CONTEXT RULE; the six `PR #N is KS-x.` sentences one per line; the namespace coincidences —
  KS-1171 is Seat B's PR #1176's ticket while PR #1171 is this seat's KS-1231; KS-1173 / KS-1175 are foreign tickets while PR #1173 / #1175 are
  this seat's; the MERGE ADDENDUM with ONE equality target per FILE — 1/1/1/4/2/2 = ELEVEN over TEN paths, three comma-separated lines = MG-2
  EXERCISED, #1173's health.ts at the ALONE blob by construction with the PAIR note; the drafter's candidate NOT-PINNED rows PARITYCOVER /
  F3SKIPSIBLINGSITES / SECONDPINF2F3 / HEALTHTS40TS2339 / NOUSELESSASSIGNMENT77 / REALLISTENERSINCELL / THREEHUNKSEACHNAMED / ALLOWSETTHREEROWS;
  report.md before the mail; the six-line verdict + the exact subject prefix; the GO string the seat expects VERBATIM: `GO: merge #1167, #1168,
  #1169, #1171, #1173, #1175 batch`; Seat B's GO string is NOT in it).
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1167-1175.sh` (543 lines, mode 755,
  sha256 `cc8882bef7b931aaf68200e63b2304af5a6ca05467a58a8438cb0e67c6a08ea2`) — pins develop 8c2f7b3fd + every head (branch AND refs/pull/N/head,
  exit 6); compare guard per PR merge_base 8c2f7b3fd / ahead 1 / behind 0 / files 1/1/1/4/2/2 (exit 10); the develop pin judged by CONTENT over 42
  paths (the 10 targets — 5 judged ABSENT, the 5 modified by blob; LANDED exit 19 if any is at a head blob OR health.ts at the PAIR blob — plus 32
  unchanged-read paths: index.ts (this round's other tamper file), the 16th's seven other tamper files, the 15th's five, the hook, preflight.sh,
  run-shell-suites.sh, fix-libsodium-symlink.js, audit-baseline.json (#1036's), proxy.ts, the ks1072 / ks815 / ks1123-f2 / ks1123-f3 test files,
  api-gateway's package.json / vitest.config.ts / tsconfig.json / lock, packages/shared's package.json / config, the Dev package.json + lock,
  eslint.config.mjs); the grep ladder (BOTH 192 tokens + 128 by-name keywords); the PAIR grep (exit 35); overrides `QAB1167_*` refuse at launch (16);
  TTY (21); PARTIAL (34). `--check` is headless and launches nothing (~95 s).
- `DRAFTER_REPORT.md` — every value beside its instrument, the leads, the drafter's own slips FIRST, what is NOT MEASURED.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1167-1175.sh --check
  Drafter's run: `launcher_check_1.out` rc 0 at 01:49:55Z-01:51:29Z (six heads on origin; six compares behind=0; develop judged by content over 42
  paths = the pin; every grep passed). The controls (`launcher_controls_gate18C.sh`, ~25 min): `launcher_check_controls.out` — read its "controls end"
  line — the drafter's run: 23 OK / 0 MISMATCH at 02:08:17Z; C_wrong_head_last rc 6 (a wrong sha refuses) is the first API-phase control; the by-name / BOTH / subject / namespace
  / tier / lsof / worktree / PENDING / PAIR ladder controls follow, each on a COPY of the prompt under `controls_gate18C.*/`.

## 3. The routing line — NOT WRITTEN BY THE DRAFTER (this commission confined writes to the gateset + briefs + launchers): add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1167|coagent@agentmail.to|yes
  `repin_and_launch_gate18C.sh` step 0 asserts it (rc 1 if absent; control: the batch1148 line's count = 1). A cockpit pane that is not routed
  cannot be tapped. (The drafter's read: the batch1167 line is ABSENT (count 0); the batch1148 control line is present (1).)

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18C_seatC/repin_and_launch_gate18C.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1167-1175.sh
  It reads its pins FROM THE LAUNCHER (no second copy; the sed dry-read in `DRAFTER_REPORT.md` prints develop 8c2f7b3fd + the six `n:head:branch`
  rows + the prompt path): (0) asserts the routing line and refuses a PARTIAL prompt (rc 8); (1) `git ls-remote` develop + every pull head + every
  branch (READ, into `lsremote_launch.out`); (2) re-reads every head from the PULLS API (`api_heads_launch.out`); (3) refuses rc 10 if develop is
  not the launcher's pin (8c2f7b3fd), rc 11 if any head moved or a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own
  `--check` (rc 13, `launcher_check_launch.out`); (6) `cockpit.sh add QA/Secuura-batch1167 <launcher>` (rc 14, `cockpit_add.out`) and a pane census.
  `bash -n` rc 0; NOT RUN by the drafter. The gate18B launch (pane `QA/Secuura-batch1170`) may be running or about to: the two panes are
  independent; never launch this one from inside the other's.

## 5. What is in this directory (all read-only evidence unless named above)
  COMMISSION.md — Wednesday's commission (the 07:2x seat; mtime 10:35 AEST)
  round18C.py (+ `.pre-1119-seatb7` — the first drafter's version with four Seat B PRs) — the ONE source of the round's pins for every script (6 PRs,
    11 file rows / 10 paths, 11 canonical rows, 6 tampers over 2 files, the A4/A5 counts, the lock windows of BOTH seats, the measured lock polls,
    Seat B's SEVEN PRs / 9 paths / GO string / all-7 tree, the 30 archived + 22 content keys, the report dirs)
  round18C_selfcheck.out — the module's self-check (6 PRs, 10 distinct paths, 11 canon rows, 6 tampers, +1008/-15; Seat B 7 / 9 / ∩ NONE)
  inbox_list_gate18C.py / inbox_list_1.out (first drafter 00:38Z) / inbox_list_2.out (01:1xZ) — the read-only inbox listing (subjects only; Datasec
    mails never fetched, never listed)
  capture_ready_mail_gate18C.py / capture_ready_mail_1.out / _2.out (first drafter) / _3.out (this drafter — idempotent: 4 NEW files, Seat B's
    #1177 #1178 #1179 READYs + its 01:08:36Z HOLD; no new Seat C mail) — every Seat C 18th READY / STATUS / QUESTION mail + Wednesday's mails to
    the seat + the brief as sent, VERBATIM by message id (TEXT_SHA256 per file): mail_seatC18_ready01_pr1_ks947.md … ready06_pr6_ks1257.md (six;
    PR 4's carries BOTH KS-1231 READY rows) · mail_seatC18_status_2255.md (#1036 MERGED) / _2326.md (six RAISED) / _0042.md (HOLDING) ·
    mail_seatC18_question_question_plan_confirmation_seat_c_18th_2243.md · mail_seatC18_question_question_ks_1257_branch_tail_seat_c_18th_2246.md ·
    mail_wed_*.md (the brief; ANSWER plan; GO #1036; ANSWER tail) · mail_gate18C_ready.md (the combined capture the launcher greps: the six READYs in
    push order, then the three STATUS mails, then the two QUESTION mails; 137676 B; no `NOT YET ARRIVED`). Beside them, CONTEXT only: Seat B 18th's
    SEVEN READYs + its STATUS / QUESTION / HOLD mails (mail_seatB18_*.md) and Wednesday's mails to Seat B (mail_wedB_*.md).
  lsremote_1.out (first drafter 00:40:42Z) / lsremote_2.out (+ .rc; 01:13:31Z — develop + refs/pull/116[7-9],117*/head + the six branches; Seat B's
    seven heads present) / checkout_counts_before.txt (first drafter) / checkout_counts_before_2.txt / checkout_counts_after.txt — origin + the
    checkout's counts BEFORE / AFTER
  loose_objects_1.out (+ .rc) — the shared store's loose objects by mtime bucket (the drafter's lead (b)); 0 after 01:14Z at 01:18Z (the control)
  loose_objects_2.out (+ .rc) / freshened_oids.txt — the drafter's S6: 186 existing loose objects FRESHENED (mtime only; 95 by this drafter's
    `--shared` predict at 01:20Z, 91 at 01:25Z not this drafter's); count-objects byte-identical
  shape_gate18C.py (+ `.pre-1119-seatb7locks` — the first drafter's version) / shape_1.out / shape_2.out (first drafter) / shape_3.out (this drafter:
    + the two-seat lock windows as a set (25, zero overlap, monotonic), the seat's lock polls 0/0/0/4/5/5 from its KS-<key>-lock.out files, the
    push-lock dir / worktree counts) — local object reads (the 11 canonicals' sha16 / hunks / counts / the .opts line, the 7 READY fences == the run
    patches, cat(s1,s2) == patch.diff ×4, the checker A4/A5 == the pins, the 10 targets at develop, the 2 tamper files at four tips, the tamper
    `from` counts 8/3/3/1/1/1, per head: parent / behind-ahead / tree / blobs / modes / numstat / `-` lines / the product set, disjointness vs
    Seat B's SEVEN, the branch names + the excision + the scanner controls)
  predict_batch_scratch_gate18C.py (+ `.pre-1050-pairdef` first drafter S2; `.pre-1120-cwdguard` — before this drafter's cwd/target guard) /
    predict_batch_scratch_1.out / _2.out (first drafter, its own scratchpad) / _3.out (this drafter, this session's scratchpad
    `predict18C.2r8y5_fu/clone`, the guard live) / predict_batch_scratch_ctrl_badtarget.out (+ .rc 9 — the negative control: `/tmp` refused) /
    newdev_tree.txt (+ `.pre-1120-rerun`, byte-identical) — EVERY git write verb, in a --shared --no-checkout scratch clone with a temp index +
    temp object dir: the 11 applies (strict / -R / --recount / the .opts row three ways), the per-PR and all-6 trees over 8c2f7b3fd in three
    orders, the health.ts pair + trio, the six heads by real 3-way merges in four orders, count-objects byte-identical
  gh_pr_reads_gate18C.py / gh_pr_reads_1.out — GitHub GETs (heads, bases, files API vs the PRODUCT sets, Refs, detectors, compares, ruleset, the
    merged #1036's 50 files, Seat B's SEVEN PRs + their compares (behind 1), the open-PR sweep with the last-merged-PR-per-path positive controls,
    the PR-number traps, the 1167-1181 window)
  linear_reads_gate18C.py / linear_reads_1.out — Linear reads (the 6 own tickets with the assignment rows, attachmentsForURL per PR, the bot walks,
    Seat B's seven keys, KS-1167..KS-1181, the 30 archived + 22 content keys, KS-256 / KS-1201 / KS-763 / KS-775 / KS-485 / KS-772, controls)
  prompt_gate18C.DRAFT.part1..3.txt + fill_prompt_gate18C.py / fill_prompt_1..3.out — the prompt's three parts and the fill script (three agreeing
    sources per head; refuses a `deadbeef` literal; a COPY beside on change, never a rename)
  gen_launcher_gate18C.py + gen_launcher.run1..4.out — the generator (run 1: four BOTH misses — three tokens the READYs do not carry + one wrapped
    `Refs KS-1246`; run 2: four wrapped by-name phrases; run 3: the pair-blob output-control miscount; run 4: written)
  launcher_check_1.out (+ .rc 0; 01:49Z) · launcher_check_2.out (+ .rc 0; 02:10Z, the final prompt) · launcher_controls_gate18C.sh + launcher_check_controls.out + launcher_controls.nohup.out + launcher_controls.start.txt
    (controls A-U + positive, each rc) · controls_dir_gate18C.txt
  repin_and_launch_gate18C.sh — the launch action (NOT run)
  *.pre-HHMM-* — the drafters' pre-fix copies (never a delete, never a rename)

## 6. Leads for the gate (full text in DRAFTER_REPORT.md; the gate grades them; ONE drafter-vs-seat VALUE disagrees — (a))
  (a) THE LOCK POLLS: the seat's HOLDING STATUS says "PR 5 waited one poll and PR 6 five polls"; its own KS-<key>-lock.out files read PR 4 FOUR polls
  (on Seat B's ks-1118 window), PR 5 FIVE (ks-1158), PR 6 FIVE (ks-1265) — 0/0/0/4/5/5; no window cut (25 windows of both seats pairwise disjoint,
  monotonic) · (b) THE LOOSE OBJECTS: 9215 (the seat, 22:55Z) -> 9416 (00:40Z and 01:13Z): +201 in buckets 23:2xZ 85 / 23:4xZ 190 / 00:5xZ 95 — both
  seats' worktree commits + batch octopi land in the shared store by design; the six GO dry runs 00:37-00:38Z wrote NONE; attribute by reachability
  · (c) #1173's BODY does not carry `--pair-blob` (the READY does) · (d) KS-485 / KS-772 comments 65 / 28 (the 16C gate read 63 / 26) · the seat's own
  (1)-(6) + S1 + the engine slips + MG-10, each named in the prompt · the SECOND PINS on four of six tampers (FOR THE GATE TO WEIGH) · health.ts:40
  TS2339 1/1 under the temp tsconfig · #1246's `no-useless-assignment` :77 and #1192's eslint warning · the RED-FIRST timeout under load 17 · the
  `suggested_test_file` shared between the two KS-1231 runs · the ruled `settingsdefaults` tail (the scanner's `ks-1`) · the #1036 base move (50
  files, ∩ = ∅) · Seat B's three attributions by this seat before its HOLD (the later four opened after) · verification.ts is BOTH KS-1123's tamper
  file and KS-1231 Part A's product file (the batch re-plant reading).

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no queue / READY-file touch, no write into the Secuura checkout (ls-remote / show / cat-file /
  rev-parse / rev-list / diff / ls-tree / log / status / for-each-ref / count-objects / config --get only; every write verb in this drafter's scratch
  clone `predict18C.2r8y5_fu` under the cwd guard), no `inbox_routing.conf` write (section 3), no key printed, no port connected except `git
  ls-remote` and the GitHub / AgentMail / Linear READ APIs; no `git fetch` (develop never moved); no Datasec mail opened or listed (the inbox listing
  filters on Seat B / Seat C / Blockchain subjects only). Nothing written into the gate18B dir (read-only for its COMMISSION.md).

## 8. Re-finishing from disk after any change (a cold successor)
  In order: (a) `python3 …/capture_ready_mail_gate18C.py` (idempotent; never overwrites; picks up any later STATUS / CORRECTION); (b) `python3
  …/shape_gate18C.py` and `python3 …/predict_batch_scratch_gate18C.py <this session's scratchpad>` (re-derives every head, the all-6 tree, and — if
  develop moved — fetches the new tip by SHA into a fresh scratch clone: note its path); (c) `python3 …/gh_pr_reads_gate18C.py` and `python3
  …/linear_reads_gate18C.py`; (d) `python3 …/fill_prompt_gate18C.py` (refuses on any pin disagreement); (e) `python3 …/gen_launcher_gate18C.py
  /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1167-1175.sh <the scratch clone from (b)>` (refuses on
  any pin move, BOTH-list or by-name miss; writes only on bash -n 0); (f) `<that launcher> --check` (rc 0 expected); (g) `bash
  …/launcher_controls_gate18C.sh <that launcher> <that prompt>` (~25 min; read the "controls end" line — 0 MISMATCH); (h) read the prompt WHOLE; (i)
  section 3, then section 4.
