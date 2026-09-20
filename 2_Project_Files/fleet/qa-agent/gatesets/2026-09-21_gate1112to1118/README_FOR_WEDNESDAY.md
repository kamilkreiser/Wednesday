# Gateset 2026-09-21_gate1112to1118 — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING)

ONE batch gate over Seat B 12th's SEVEN test-only PRs #1112-#1118 on develop `362e51fe0db7e73d5557924902763fe3f10fd8c7` (unmoved), graded
TIER 1 (floor B #1113, C #1114, F #1118; tiers 2/1/1/2/2/2/1 per your 18:47:45Z ANSWER Q3). Produced in the exact shape of
`gatesets/2026-09-21_gate1106to1111/`. Everything below is read-only evidence or a file for YOU to run.

## 1. Read WHOLE before launching
- The prompt (789 lines, 103035 bytes, sha256 365d4279dc691333…): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1112-1118.prompt.txt`
  It carries your rulings exactly: tiers 2/1/1/2/2/2/1, batch tier 1; every ticket STAYS In Progress, no tickets filed by the gate; the MERGE
  ADDENDUM with ONE equality target per FILE (1/1/1/1/5/1/1, PR E's five comma-separated — MG-2, targets13.py:28/:31); the MG-3 key-set rule per
  squash body (merge13.py:58-:64, two keys on C/E/F); report.md BEFORE the verdict mail; NOT PINNED rows in the previous report's format (with BY
  DESIGN rows for the tickets' own defects); the namespace guard (KS-1112..KS-1118 are real tickets; PR #1006 is a real PR that is not KS-1006; the
  ELEVEN newer READYs incl. KS-957 F4-TOOLINGTOKENS-1 are not in this gate); and the LEADS (i)-(ix) as claims for the gate to GRADE (F1 / F2 / F3,
  INSTR-1, the 12/15 skips, the anchoring 328/329 with the ONE red named, shellcheck NOT RUN + TRIVY_JOB_SH copies, the auth 779 first-measured,
  S1-S5, the all-fifteen tree, the line-number discipline).
- The launcher (542 lines): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1112-1118.sh` — pins develop +
  the seven heads (branch AND refs/pull/N/head, exit 6); compare guard per PR merge_base/ahead=1/behind=0/files (exit 10 on any move); the develop
  pin judged by CONTENT over 58 paths (exit 18 GUARDED / exit 19 LANDED); prompt + READY greps 7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33;
  overrides refuse at launch (16); TTY (21). `--check` is headless and launches nothing.
- `mail_leads.out` — 17 leads (every disagreement or two-frame reading I found; NO drafter-vs-seat value disagrees — every re-derived value equals
  the seat's). `DRAFTER_REPORT.md` — FOUND / TESTED / HOW with every value beside its command.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1112-1118.sh --check
  Drafter's run: `launcher_check_1.out` rc=0 at 07:07:20 AEST (2026-09-20T21:07Z). Takes ~60 s (7 compare GETs + 58 contents GETs).

## 3. The routing line to add to `fleet/inbox_routing.conf` FIRST (a cockpit pane that is not routed cannot be tapped)
  Copy the shape of the existing `QA/Secuura-batch1106|coagent@agentmail.to|yes` line (the last line of the file today) and append:
    QA/Secuura-batch1112|coagent@agentmail.to|yes
  Back the file up first as the previous gate did (`inbox_routing.conf.pre-<date>-<time>-qagate1112`). `repin_and_launch.sh` step 0 refuses (rc 1)
  until that line is present (control: it also prints the batch1106 line's count = 1). The drafter did NOT edit inbox_routing.conf.

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1112to1118/repin_and_launch.sh
  It: (0) asserts the routing line; (1) `git ls-remote` develop + the seven pull heads + the seven branch globs (READ, into `lsremote_launch.out`);
  (2) re-reads the seven heads from the PULLS API (`api_heads_launch.out`); (3) refuses rc 10 if develop is not 362e51fe0, rc 11 if any head moved or
  a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own `--check` (rc 13, `launcher_check_launch.out`); (6)
  `cockpit.sh add QA/Secuura-batch1112 <launcher>` (rc 14, `cockpit_add.out`) and a pane census. `bash -n` rc 0; NOT RUN by the drafter.

## 5. What is in this directory (all read-only evidence unless named above)
  capture_ready_mail.py / .out — the nine seat mails + your two ANSWERs captured VERBATIM by message id (TEXT_SHA256 per file):
    mail_seatB12_plan_confirmation_1845.md · mail_seatB12_status_1934.md · mail_seatB12_ready1_A_ks1203.md … ready7_F_ks1006.md ·
    mail_wed_answer_plan_confirmation_1847.md · mail_wed_answer_all_seven_read_2031.md · mail_batch1112_ready.md (the combined capture the launcher greps)
  list_ready_mail.py / .out — the inbox listing (60 newest) at capture time
  lsremote_1.out — develop + 7 pull heads + the 7 branch globs at 20:37:59Z (all pins OK; the same-key merged branches -untyped-1 / -order-1 still exist)
  shape_1.py / .out — local object reads: parents, trees, the 11 (develop blob, head blob) pairs, numstat +216/-0, 21 pairs disjoint, the ten tamper
    files' bytes/sha256/blob, 29 unchanged-read paths (one guessed path ABSENT — drafter S2, dropped)
  source_reads.sh / .out — the 27 `from` lines at the tip (exact-line count 1 each — five re-counted after drafter S1), scope anchors + controls, the
    new cells' titles at each head, the F1/F2/F3 cover-cell titles at develop, T11/T12/T13's shape, the trivy suite's lines, the hook's preflight
    call, the three skip_stack sites, lock versions (vitest 4.1.11 x3, jest 29.7.0), CSL 15.0.3
  predict_batch_scratch.sh / .out — REAL 3-way merges in a --shared scratch clone: 7 fast-forwards, the all-seven tree in SIX orders = the seat's
    6aa9873f97…, read-tree control, 11 files +216, empty-repo rc 128
  gh_pr_reads.py / .out — the seven PRs (heads, bases, files API, Refs lines, closing/completeness detectors 0/0/0, archived/foreign keys NONE,
    scope sentences present, compares), ruleset 18499832, open PRs vs the 11 paths + 10 tamper files (#995 only), the PR-number namespace trap
  linear_reads.py / .out — the ten tickets (all In Progress, bot-walked or already), attachmentsForURL x7 exact, KS-1112..KS-1118, 13 archived,
    17 foreign, KS-256 / KS-1201 / KS-485 / KS-772, the pull/1111 control
  gen_launcher_1112.py + gen_launcher.run1-4.out — the generator (run 1: BOTH tokens the READYs truncate; run 2: one wrapped phrase; run 3: an
    output-control count; run 4: written)
  launcher_check_1.out (rc 0) · launcher_controls.sh + launcher_check_controls.out (controls A-R, each rc) · controls_dir.txt
  prompt_keyword_counts.out — 60 keywords, all non-zero, with three absent-by-design controls at 0
  repin_and_launch.sh — the launch action (NOT run)

## 6. Leads for you (full text in mail_leads.out; the gate grades them, you may want them in the LAUNCH RECEIPT to the seat)
  1 identical census totals in READY A (14 runs) and READY B (12 runs) · 2 auth loopback 208 (STATUS) vs 1896/21 runs (READY F) · 3 the brief's
  per-file absolutes (auth.test 17->19, identity 52->53) vs the seat's 16->18 / 51->52 — your slip class, deltas agree · 4 CODECJOINDROPPED cover ONE
  (brief) vs FOUR (seat) · 5 READY E's "red=N" counts include develop's own red · 6 what F1 means (the widening was already caught on one
  requireSuperAdmin route) · 7 what F2 means (connectorMeta pinned indirectly by the #1106 cell) · 8 INSTR-1 · 9 READY G truncates the cell title ·
  10 "20 listeners" vs "18" · 11 PR #1006 exists (KS-844) · 12 ELEVEN newer READYs, not ten (KS-957 F4-TOOLINGTOKENS-1 landed 06:37) · 13 KS-1273
  EXITCODEENV-1 (banked) touches #1117's tamper file 04-container-trivy.sh · 14 the n_ran duplicate control now 1 (post-#1109) · 15/16 the drafter's
  own two slips · 17 #1116's commit subject is exactly 92 chars (100 with the squash suffix — at the lint boundary).

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no inbox_routing.conf edit, no PAUSE_QUEUE / queue.md / done.md / READY-file touch, no write into the
  Secuura checkout (git show / ls-tree / ls-remote / log / grep / rev-parse / diff / cat-file only; the scratch clone lives in the drafter's
  scratchpad), no key printed.
