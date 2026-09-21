# Gateset 2026-09-22_gate16C_seatC — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE batch gate over Seat C 16th's TWELVE test-only PRs (#1148, #1150, #1152, #1154, #1156, #1158, #1160, #1162 — the EVEN numbers, Seat B 16th's
gate16B holds the ODD #1147-#1161 — then #1163, #1164, #1165, #1166), graded at the TIER 2 floor with TIER 1 on the SIX auth-surface pins (#1158 KS-855,
#1160 KS-944, #1162 KS-1156, #1163 KS-1188, #1164 KS-1193, #1165 KS-1217 — the commission item 1). FIFTEEN local-model R15 READYs (fourteen run patches
`--recount` + KS-910's two checker section files strict) grouped by TICKET = by FILE into twelve PRs; 16 paths (11 A + 5 M), 0 overlap, 0 product
bytes, +1256/-11; the twelve-PR tree over develop 64ab10513 = `4817a9c2ea2334b89395c4faa588312cfd609550` (re-derived three + four orders). The seat's
push-order PR 2 (KS-1123 F3b) is HELD un-pushed (Wednesday 16:53:40Z, TS18046) and is NOT in this gate. Produced in the exact shape of
`gatesets/2026-09-22_gate16B_seatB/` (the sibling drafter's pipeline, itself from gate15's). Everything below is read-only evidence or a file for YOU
to run. **The two gates (gate16B over Seat B's eight, gate16C over Seat C's twelve) are INDEPENDENT by the partition: each gate clones `--shared` from
the same checkout into ITS OWN report dir / mktemp clones and never enters the other's; they may run in parallel on the same `.git` (read-only, no
ref write by either) — the launcher's develop pin refuses (exit 10 / 18 / 19) if the OTHER seat's GO lands its merges first, which is a re-pin, not a
defect.**

## 0. THE DEVELOP PIN (unmoved all night — the launcher refuses if it moves)
Origin develop = `64ab105132eada0621622acf4d6053bc59926780` (tree `87b4aa12d2eb…`) at every READY (17:06Z … 19:08Z), at the seat's 19:12:28Z HOLDING
STATUS, at the drafter's 19:12:22Z / 19:24:xxZ / 19:44:11Z / 19:50Z reads (`lsremote_1.out`, `predict_batch_scratch_1.out` (c), `fill_prompt_3.out`,
`launcher_check_1.out`). Every head's parent IS 64ab10513, so each PR alone over develop is a fast-forward (merged tree = head tree) and the compare
reads merge_base 64ab10513 / ahead 1 / behind 0 / files 1/1/1/1/1/1/1/1/3/2/1/2 (the launcher asserts exactly that, exit 10). **If develop moves before
the launch (Seat B 16th's GO landing its eight merges is the likely mover — a disjoint move by the partition, still a re-pin):**
`python3 predict_batch_scratch_gate16C.py <scratchpad>` (it fetches the new tip BY SHA into its own `--shared` scratch clone over the checkout's ssh
road — never into the checkout — and re-predicts every tree), then `python3 gen_launcher_gate16C.py <launcher> <that clone>`, then re-read the
prompt's THE SHAPE bullets (the move, the merged trees, the END STATE) and edit `prompt_gate16C.DRAFT.part2.txt` accordingly before
`fill_prompt_gate16C.py`.

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1148-1166.prompt.txt`
  (1097 lines, 153090 B, sha256 `cb537771b382e22702d2b44cc1550d9173a830e36c31943d68a92a6546077885`; first line `ultrathink`; TWELVE by-name items
  exactly as commissioned; the twelve `PR #N is KS-x.` sentences one per line; the namespace coincidences — KS-1156 is PR 9's ticket + the 15th's
  #1146's while PR #1156 is PR 6's KS-1237; KS-1158 is Seat B's while PR #1158 is PR 7's KS-855; KS-1165 is a foreign ticket while PR #1165 is PR 12;
  the MERGE ADDENDUM with ONE equality target per FILE — 1/1/1/1/1/1/1/1/3/2/1/2 = SIXTEEN, three comma-separated lines = MG-2 EXERCISED; NOT-PINNED
  candidate rows as RECORDS (no cover row expected — every cover EMPTY); report.md before the mail; the twelve-line verdict + the exact subject prefix;
  the GO string the seat expects VERBATIM: `GO: merge #1148, #1150, #1152, #1154, #1156, #1158, #1160, #1162, #1163, #1164, #1165, #1166 batch`).
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1148-1166.sh` (562 lines, mode 755,
  sha256 `4c9d555ca4a8a56eec51293d2f04a1ed5ab7d08c03b17058f4ecc01510bec011`) — pins develop 64ab10513 + every head (branch AND refs/pull/N/head, exit 6);
  compare guard per PR merge_base 64ab10513 / ahead 1 / behind 0 / files (exit 10); the develop pin judged by CONTENT over 54 paths (the 16 targets —
  11 judged ABSENT, LANDED exit 19 if any is at a head blob — plus 38 unchanged-read paths: the 8 tamper files, the 15th's five (users.ts in both), the
  hook, preflight.sh, run-shell-suites.sh, fix-libsodium-symlink.js, jwt.ts, provenance.ts, proxy.ts, the ks949 / ks1072 / ks815 / ks1123-f2 / ks1123-f3
  test files, the two lanes' package.json / vitest.config.ts / tsconfig.json / lock, packages/shared's package.json / config, the Dev package.json + lock,
  eslint.config.mjs); the grep ladder (BOTH 189 tokens + 114 by-name keywords); overrides `QAB1148_*` refuse at launch (16); TTY (21); PARTIAL (34).
  `--check` is headless and launches nothing (~70 s).
- `DRAFTER_REPORT.md` — every value beside its instrument, the leads, the drafter's own slips FIRST, what is NOT MEASURED.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1148-1166.sh --check
  Drafter's run: `launcher_check_1.out` rc 0 at 19:50:01Z-19:51:11Z (twelve heads on origin; twelve compares behind=0; develop judged by content over 54
  paths = the pin; every grep passed). The controls (`launcher_controls_gate16C.sh`, ~20 min): `launcher_check_controls.out` — read its "controls end"
  line (0 MISMATCH expected); C_wrong_head_last rc 6 (a wrong sha refuses) is the first API-phase control; the by-name / BOTH / subject / namespace /
  tier / lsof / worktree / PENDING ladder controls follow, each on a COPY of the prompt under `controls_gate16C.*/`.

## 3. The routing line — NOT WRITTEN BY THE DRAFTER (this commission confined writes to the gateset + briefs + launchers): add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1148|coagent@agentmail.to|yes
  `repin_and_launch_gate16C.sh` step 0 asserts it (rc 1 if absent; control: the batch1136 line's count = 1). A cockpit pane that is not routed
  cannot be tapped. (The batch1147 line — gate16B's — is already at :64 of the conf at the drafter's read.)

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16C_seatC/repin_and_launch_gate16C.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1148-1166.sh
  It reads its pins FROM THE LAUNCHER (no second copy; the sed dry-read in `DRAFTER_REPORT.md` prints develop 64ab10513 + the twelve heads): (0) asserts
  the routing line and refuses a PARTIAL prompt (rc 8); (1) `git ls-remote` develop + every pull head + every branch (READ, into `lsremote_launch.out`);
  (2) re-reads every head from the PULLS API (`api_heads_launch.out`); (3) refuses rc 10 if develop is not the launcher's pin (64ab10513), rc 11 if any
  head moved or a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own `--check` (rc 13, `launcher_check_launch.out`);
  (6) `cockpit.sh add QA/Secuura-batch1148 <launcher>` (rc 14, `cockpit_add.out`) and a pane census. `bash -n` rc 0; NOT RUN by the drafter.
  The gate16B launch (pane `QA/Secuura-batch1147`) may already be running: the two panes are independent; never launch this one from inside the other's.

## 5. What is in this directory (all read-only evidence unless named above)
  COMMISSION.md — Wednesday's commission (05:11 AEST)
  round16C.py — the ONE source of the round's pins for every script (12 PRs, 16 files, 16 canonical rows, 14 tampers over 8 files; Seat B's 8; the 24 archived + 14 content keys)
  inbox_list_gate16C.py / inbox_list_1.out — the read-only inbox listing (subjects only; the twelve READY subjects 17:06:23Z-19:08:40Z + the 19:12:28Z HOLDING STATUS)
  capture_ready_mail_gate16C.py (+ `.pre-1913-s3status` — drafter S1) / capture_ready_mail_1.out / _2.out — every Seat C 16th READY / STATUS / QUESTION mail + Wednesday's
    mails to the seat + the brief as sent, VERBATIM by message id (TEXT_SHA256 per file): mail_seatC16_ready01_pr1_ks864.md … ready13_pr13_ks910.md (twelve) ·
    mail_seatC16_status_1646.md / _1651.md / _1656.md (the S3 disclosure) / _1912.md (HOLDING) · mail_seatC16_question_question_plan_confirmation_seat_c_16th_1608.md ·
    mail_seatC16_question_question_attachment_guard_condition_4_th_1729.md · mail_wed_*.md (ANSWER plan / ADDENDUM push lock / ANSWER PR 2 hold / ADDENDUM
    linear guard / ANSWER condition (4) / the SUCCESSOR brief) · mail_gate16C_ready.md (the combined capture the launcher greps: the twelve READYs in push
    order, then the four STATUS mails, then the two QUESTION mails; 242508 B, sha256 210c5393fb67…, no `NOT YET ARRIVED`). Beside them, CONTEXT only:
    Seat B 16th's eight READYs + its STATUS / QUESTION / ACK mails (mail_seatB16_*.md — incl. one MIS-NAMED copy `mail_seatB16_status_seat_c_16th_s3_cross_seat_i_sigte_1656.md`
    of Seat C's S3 STATUS from the drafter's first run, drafter S1; the correctly named `mail_seatC16_status_1656.md` is the one in the combined capture)
    and Wednesday's mails to Seat B (mail_wedB_*.md).
  lsremote_1.out / checkout_counts_before.txt / checkout_counts_after.txt — origin (19:12:22Z: develop + refs/pull/1147..1166/head) + the checkout's counts BEFORE / AFTER
  shape_gate16C.py (+ `.pre-1923-ks1199glob` — drafter S2) / shape_1.out / shape_2.out — local object reads (the 16 canonicals' sha16 / hunks / counts / the truncation
    class, the 15 READY fences == the run patches, the 16 targets at develop, the 8 tamper files at three tips, the mfa.ts `from` count 3, per head: parent /
    behind-ahead / tree / blobs / modes / numstat / `-` lines / TEST-FILE-ONLY, disjointness vs Seat B, the branch names + excisions, the hook :76, the
    KS-910 hunk site :46-:55 at develop)
  predict_batch_scratch_gate16C.py / predict_batch_scratch_1.out / newdev_tree.txt — EVERY git write verb, in a --shared --no-checkout scratch clone: the 16
    applies (strict / -R / --recount rcs; the STRICT apply's short blobs on the three truncation rows; the rc-128 row's no-write; KS-910's sections and its
    non-applying patch.diff), the per-PR and all-15 trees over 64ab10513 in three orders (multi-file PRs in every order), the twelve heads by real 3-way merges
    in four orders, the thirteen-PR tree's diff = the held file; count-objects byte-identical
  gh_pr_reads_gate16C.py / gh_pr_reads_1.out — GitHub GETs (heads, bases, files API, Refs, detectors, compares, ruleset, Seat B's eight PRs + the four-condition inputs,
    the open-PR sweep with the seat's #1009 / #1007 controls, the PR-number traps, the 1147-1167 window)
  linear_reads_gate16C.py / linear_reads_1.out — Linear reads (the 12 own tickets + the held KS-1123, attachmentsForURL per PR, the bot walks, Seat B's nine keys,
    KS-1147..KS-1167, the 24 archived + 14 content keys, controls)
  prompt_gate16C.DRAFT.part1..3.txt + fill_prompt_gate16C.py / fill_prompt_1..3.out — the prompt's three parts and the fill script (three agreeing sources per head)
  gen_launcher_gate16C.py + gen_launcher.run1..3.out — the generator (run 1: four BOTH misses — two tokens wrapped / Unicode minus / a capture-only phrase;
    run 2: four by-name phrases wrapped; run 3: written)
  launcher_check_1.out (rc 0) · launcher_controls_gate16C.sh + launcher_check_controls.out + launcher_controls.nohup.out (controls A-T + positive, each rc) · controls_dir_gate16C.txt
  repin_and_launch_gate16C.sh — the launch action (NOT run)
  *.pre-HHMM-* — the drafter's pre-fix copies (never a delete)

## 6. Leads for the gate (full text in DRAFTER_REPORT.md; the gate grades them; NO drafter-vs-seat VALUE disagrees)
  1 the six auth pins are TIER 1 (the commission; the seat proposed tier 2 and named them) · 2 the recount class: F1009b rc 128 `corrupt patch at line 10`
  (strict apply writes NOTHING), three truncation rows 97->108 / 97->122 / 124->153 with the seat's strict blobs reproduced · 3 KS-910's canonical is the
  two SECTION files; its patch.diff / fence does not apply either way (rc 1 / rc 1); the checker REANCHORED section_1 at :49 · 4 KS-1188-F1A's `from` occurs
  3× in mfa.ts (:143 :166 :397 — drafter count 3) · 5 typecheck ks1073 delta -1 (a removal) · 6 the ALLOW set's three rows now ATTRIBUTED to ks1072-… /
  ks815-… test files · 7 a prior auth REPORT set EXISTS (14th-carried) — against the brief's "no set yet" · 8 F-FALSECOVER-944 and the re-read rule coded
  mid-round (fired on four PRs) · 9 F-45: KS-910's push ran 45 shell suites · 10 the S3 cross-seat SIGTERM (Seat B's wrapper) + the fix by ancestry · 11 the
  series stop / relaunch at ks1199 (the marker is gone; KS-1199-lock.out shows 5 polls on Seat B's ks-1158 window) · 12 the eight Seat B attributions
  (3 retro + 5 live) and the asymmetry of the two seats' guarded sets · 13 twenty lock windows on one `.git` (12 + 8), zero overlap — measure as a set ·
  14 the bodies' "a completeness cell" wording (#1158, #1160) hit the completeness detector · 15 every body says `TS18046` in its round paragraph (the held
  PR by description, never its key) · 16 KS-864's history: walked 2026-09-19 on #1073, moved back by the board login, walked again on #1148 · 17 KS-1123
  (HELD) was itself walked on #1002 and moved back 2026-09-16 · 18 subjects 77-92 chars (KS-1193's exactly 92) · 19 the `available_scopes` underscore in
  KS-855's branch · 20 the vault-note S1 (a VAULT event, restored; not a repo byte).

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no queue / READY-file touch, no write into the Secuura checkout (ls-remote / show / cat-file / rev-parse /
  rev-list / diff / ls-tree / log / status / for-each-ref / count-objects / config --get only; every write verb in the drafter's scratch clone
  `predict16C.p9o7o6_c`), no `inbox_routing.conf` write (section 3), no key printed, no port connected except `git ls-remote` and the GitHub / AgentMail
  / Linear READ APIs; no `git fetch` (develop never moved); no Datasec mail opened (subject lines in listings only). Nothing written into the gate16B dir.

## 8. Re-finishing from disk after any change (a cold successor)
  In order: (a) `python3 …/capture_ready_mail_gate16C.py` (idempotent; never overwrites; picks up any later STATUS / CORRECTION); (b) `python3 …/shape_gate16C.py`
  and `python3 …/predict_batch_scratch_gate16C.py <scratchpad dir>` (re-derives every head, the all-15 tree, and — if develop moved — fetches the new tip by
  SHA into a fresh scratch clone: note its path); (c) `python3 …/gh_pr_reads_gate16C.py` and `python3 …/linear_reads_gate16C.py`; (d) `python3 …/fill_prompt_gate16C.py`
  (refuses on any pin disagreement); (e) `python3 …/gen_launcher_gate16C.py /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1148-1166.sh <the scratch clone from (b)>`
  (refuses on any pin move, BOTH-list or by-name miss; writes only on bash -n 0); (f) `<that launcher> --check` (rc 0 expected); (g)
  `bash …/launcher_controls_gate16C.sh <that launcher> <that prompt>` (~20 min; read the "controls end" line — 0 MISMATCH); (h) read the prompt WHOLE;
  (i) section 3, then section 4.
