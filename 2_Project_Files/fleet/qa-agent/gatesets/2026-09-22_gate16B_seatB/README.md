# Gateset 2026-09-22_gate16B_seatB — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE batch gate over Seat B 16th's EIGHT R15 test-only PRs — the ODD numbers #1147, #1149, #1151, #1153, #1155, #1157, #1159, #1161 (Seat C 16th
holds the EVEN numbers #1148…#1166 in the same window on the same `.git`) — graded at the TIER 2 floor with TIER 1 on #1161 (KS-975, the
`services/security/src/rateLimitScope.ts` surface; the 14th's PRs 3/4 precedent; Wednesday's Q4). Eight paths under `__tests__/`, 0 overlap,
0 product bytes, +755/-1. The seat's PR 8 (KS-1171) is HELD un-pushed (Wednesday 16:50:37Z) and is NOT in this gate. Produced in the exact shape
of `gatesets/2026-09-21_gate15_docs_comments/`. Everything below is read-only evidence or a file for YOU to run.

## 0. THE ROUND'S ONE NEW SHAPE (read this first — it is what the gate exists to catch)
`--recount` is MANDATORY on every apply (the seat's Q5): the model under-declared the hunk's new count on FOUR patches, so a strict `git apply`
returns rc 0 AND WRITES A SHORT FILE (KS-928 97 of 107 lines -> blob e76b3e90db28; KS-1133-B 97 of 109 -> e9dc6e3899f0; KS-1181-F3 74 of 75 ->
6250385ee49e; KS-975-ITEM1 34 of 36 -> 1fcffe443b5c), and OVER-declared one (KS-1158-R3: strict rc 128 `corrupt patch at line 100`). The drafter
reproduced all five in a scratch index (`predict_batch_scratch_1.out` (a)) and the eight heads ARE the RECOUNT blobs (8/8). Develop 64ab10513 is
UNMOVED all night (every READY, the drafter's 18:35:53Z / 18:48:17Z / 19:02:50Z / 19:07:43Z reads) — so every head is a FAST-FORWARD over it, the
compare per PR is merge_base 64ab10513 / ahead 1 / behind 0 / files 1, and the addendum's merged tree IS the head tree. **If develop moves before
the launch** (Seat C 16th's GO landing its twelve is the likely cause — its paths are disjoint from these eight and their nine tamper files,
measured): `python3 predict_batch_scratch_gate16B.py <scratchpad>` (fetches the new tip BY SHA into its own `--shared` scratch clone over the
checkout's ssh road — never into the checkout — and rewrites `newdev_tree.txt`), then `python3 gen_launcher_gate16B.py <launcher> <that clone>`
(BEHIND becomes the move count), then re-read the prompt's THE SHAPE bullets and edit `prompt_gate16B.DRAFT.part2.txt` before `fill_prompt_gate16B.py`.

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1147-1161.prompt.txt`
  (first line `ultrathink`; TWELVE by-name items exactly as commissioned + Wednesday's 04:37 addendum (the #1153 cover predicate `EXACTLY ITS
  DECLARED CELLS + its measured develop cover`, R3 as a NOT-PINNED candidate for its own file; the GO string); the eight `PR #N is KS-x.`
  sentences one per line; the namespace coincidences — KS-1158 is PR 4's ticket while PR #1158 is Seat C's KS-855; KS-1156 is Seat C's #1162's
  ticket while PR #1156 is Seat C's KS-1237; the even numbers are Seat C's; the MERGE ADDENDUM with ONE equality target per PR (no two-file line —
  MG-2 inherited, not exercised); the NOT-PINNED candidate rows R3COVEREDBYKS1004 / TESTFILETAMPER / SHAREDGUARDS5S / ANCHORING4005UNATTRIBUTED;
  report.md before the mail; the eight-line verdict + the exact subject prefix; Seat C's twelve PRs named). Drafter's last fill: 870 lines, 119351 B, sha256
  b2eb1ca82a5cade7c3ceb51ec06ec5bd8a04c7b5d2bbd8f927d51b06dfb51aca (`fill_prompt_4.out`; re-derive before launch: `shasum -a 256 <prompt>`). Wednesday's addendum items are in: the #1153 correction (part1 per-PR
  table + BY-NAME 5 / 12), the GO string (part2 + the closing).
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1147-1161.sh` — pins develop
  64ab10513 + every head (branch AND refs/pull/N/head, exit 6; the ks-1171 glob must be EMPTY at generation); compare guard per PR merge_base
  64ab10513 / ahead 1 / behind 0 / files 1 (exit 10); the develop pin judged by CONTENT over 49 paths (the 8 targets — seven judged ABSENT, LANDED
  exit 19 if any is at its head blob; the ks1213 file by blob — plus 41 unchanged-read paths incl. this round's 9 tamper files, the 15th's five, the
  hook, preflight.sh, run-shell-suites.sh, jwt.ts, provenance.ts, proxy.ts, the ks1004 cover test, threadTokenMint, the four lanes' package.json /
  config / tsconfig / lock); the grep ladder (BOTH 158 tokens + 97 by-name keywords); overrides `QAB1147_*` refuse at launch (16); TTY (21);
  PARTIAL (34, inherited). `--check` is headless and launches nothing (~110 s). 515 lines, mode 755, sha256
  c98661da780e8ab81a9a3c6fcc7a38ea8eb7bb3f954cce51256c38d7a944118f (`gen_launcher.run5.out`; run 6 after the Seat C patch regenerated it byte-identical).
- `DRAFTER_REPORT.md` — the drafter's own slips FIRST, every value beside its instrument, the leads, what is NOT MEASURED.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1147-1161.sh --check
  Drafter's runs: `launcher_check_1.out` rc 0 at 19:09:54Z-19:11:42Z; `launcher_check_2.out` rc 0 at 19:30:15Z-19:31:57Z (after the controls, against
  the 870-line prompt and the rebuilt combined capture). The controls: `launcher_controls_gate16B.sh` -> `launcher_check_controls.out` — `controls end
  2026-09-21T19:29:25Z: 21 OK / 0 MISMATCH` (A-T + POSITIVE, each rc on its own line; control T is the one that PASSES by design — the launcher greps heads, not addendum
  blobs: the gate reads blobs itself).

## 3. The routing line — NOT WRITTEN BY THE DRAFTER (this commission confined writes to the gateset + briefs + launchers): add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1147|coagent@agentmail.to|yes
  `repin_and_launch_gate16B.sh` step 0 asserts it (rc 1 if absent; control: the batch1136 line's count = 1). A cockpit pane that is not routed
  cannot be tapped. Drafter's read at 19:12Z: count 0 (absent, as expected); the batch1136 control 1.

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16B_seatB/repin_and_launch_gate16B.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1147-1161.sh
  It reads its pins FROM THE LAUNCHER (no second copy): (0) asserts the routing line and refuses a PARTIAL prompt (rc 8); (1) `git ls-remote`
  develop + every pull head + every branch + the ks-1171 glob (READ, into `lsremote_launch.out`; rc 4 if a ks-1171 branch exists — the held PR
  pushed); (2) re-reads every head from the PULLS API (`api_heads_launch.out`); (3) refuses rc 10 if develop is not the launcher's pin
  (64ab10513), rc 11 if any head moved or a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own `--check` (rc 13,
  `launcher_check_launch.out`); (6) `cockpit.sh add QA/Secuura-batch1147 <launcher>` (rc 14, `cockpit_add.out`) and a pane census. `bash -n` rc 0;
  the pin-parse sed dry-read prints develop 64ab10513 and the eight PRs (section 5 of DRAFTER_REPORT); NOT RUN by the drafter.

## 5. What is in this directory (all read-only evidence unless named above)
  COMMISSION.md — Wednesday's commission (04:34 AEST) + her 04:37 addendum (relayed in the drafter's launch message, applied in the prompt)
  round16B.py — the ONE source of this round's pins for every script (a wrong pin in the prompt is the most expensive slip; gate15 repeated its
    table in six files — here every script imports this module and asserts against origin / local objects / the READYs; `SEATC` extended at 18:48Z)
  inbox_list_gate16B.py / inbox_list_1.out — the inbox listing (subjects only; Datasec subjects unread)
  capture_ready_mail_gate16B.py / capture_ready_mail_1.out, _2.out — every Seat B 16th READY (8) + its two STATUS + four QUESTION + the ACK + Wednesday's
    mails to it, VERBATIM by message id (TEXT_SHA256 per file): mail_seatB16_ready01_pr1_ks928.md … ready09_pr9_ks975.md · mail_seatB16_status_1654.md ·
    mail_seatB16_status_1833.md · mail_seatB16_question_*.md · mail_seatB16_other_ack_*.md · mail_wed_*.md; Seat C 16th's twelve READYs + STATUS /
    QUESTION mails + Wednesday's mails to it as mail_seatC16_*.md / mail_wedC_*.md (context for by-name 3 / 9 / 10 only); mail_gate16B_ready.md
    (the combined seat-B capture the launcher greps: the READYs in push order 1 2 3 4 5 6 7 9, a HELD marker for slot 8, then the STATUS mails,
    then the QUESTION / ACK mails — rebuilt on every capture run; its first line carries the rebuild instant)
  lsremote_1.out / lsremote_2.out / checkout_counts_before.txt / checkout_counts_after.txt — origin + the checkout's counts (BEFORE 18:35:56Z; AFTER at the drafter's close)
  shape_gate16B.py / shape_1.out — local object reads (the 12 canonicals with the declared-vs-actual new count, the 8 targets at develop, the 9 tamper
    blobs at both tips, per head: parent / behind-ahead / tree / blob / lines / `-` lines / TEST-FILE-ONLY / the strict-blob inequality; the static
    reads for the seat findings — the ks1004 cover cell, threadTokenMint, the `ks-727` file name, principalScope, the tamper sites)
  predict_batch_scratch_gate16B.py / predict_batch_scratch_1.out / newdev_tree.txt — EVERY git write verb, in a --shared --no-checkout scratch clone:
    the 12 applies four ways (strict / -R / --recount / -R --recount --check), the STRICT apply for real on the truncation rows beside the RECOUNT
    apply, the per-PR trees (PR 5 in three orders with its four intermediate blobs), the all-12 tree in three orders, the eight heads by real 3-way
    merges in four orders, the held octopus tree's diff vs the eight-PR tree; count-objects byte-identical; section (c) the develop move (fetch by
    SHA over the checkout's ssh road — not needed this run)
  gh_pr_reads_gate16B.py / gh_pr_reads_1.out / gh_seatc_late_1.out — GitHub GETs (heads, bases, files API, Refs, detectors, compares, ruleset, Seat C's
    PRs with the four-condition inputs, the open-PR sweep, the PR-number traps, the window #1147..#1165 as it stood at 18:46Z)
  linear_reads_gate16B.py / linear_reads_1.out — Linear reads (the 8 own tickets + the held KS-1171, attachmentsForURL per PR, Seat C's 13 keys,
    KS-1147..KS-1163, the 24 archived + 20 content keys, KS-1004, controls)
  seatc_late_paths_1.out — Seat C's READYs 9-13 paths + its 19:12Z STATUS head lines (∩ our 8 = ∅, ∩ our 9 tamper files = ∅ over all 14 of its paths)
  prompt_gate16B.DRAFT.part1..3.txt + fill_prompt_gate16B.py / fill_prompt_N.out — the prompt's three parts and the fill script (re-reads origin IN
    THE SAME ACTION and refuses if origin / round16B / the READYs disagree on any head; substitutes the PR numbers, heads, READY instants, develop,
    its tree and the eight-PR tree)
  gen_launcher_gate16B.py + gen_launcher.runN.out — the generator (run 1: four wrapped / absent BOTH phrases + two prompt-only tokens; run 2: a
    wrapped by-name phrase; runs 3-4: the output-control counts under the unmoved-develop identity (DEV == PARENT, ALL_OVER_DEV == ALL_OVER_PARENT)
    and the header's `exit 10` mentions — fixed; run 5: written)
  launcher_check_1.out (rc 0) · launcher_check_2.out (rc 0, the re-run after the controls) · patch_drafts_seatc_late.py / .out (Seat C's #1164-#1166 folded in) · lsremote_final.out · launcher_controls_gate16B.sh + launcher_check_controls.out
    (controls A-T + positive, each rc) · controls_dir_gate16B.txt
  repin_and_launch_gate16B.sh — the launch action (NOT run)
  *.pre-HHMM-* — the drafter's pre-fix copies (never a delete)

## 6. Leads for the gate (full text in DRAFTER_REPORT.md; the gate grades them; NO drafter-vs-seat VALUE disagrees)
  1 the four TRUNCATION rows + the rc-128 row (README section 0) — the strict SHORT blobs reproduced; the heads are the RECOUNT blobs · 2 #1153's
  develop COVER (the ks1004 lockout cell reds the R3 tamper at develop and in the PR frame) — the seat's own correction; READY 4's "EMPTY for every
  tamper of this PR" template line is false for it · 3 #1159's tamper is on a TEST file's header comment with NO scope anchor in anchors17.json
  (`:None 'None'`) — the whole-line `from` + a `describe(` count located it · 4 #1157's ssrf-guard is a shared security LIBRARY — the tier-1 reading
  question (the drafter says tier 2) · 5 the namespace: KS-1158 vs #1158 (Seat C's KS-855); KS-1156 vs #1156 (Seat C's KS-1237); #928 / #975 /
  #1118 / #1133 closed, other tickets' · 6 Seat C's #1154 head ref ends `-r15-1` (no tag) — does the seat's four-condition regex admit it (no
  attribution was owed for KS-1199: not in the guarded set) · 7 KS-928's Linear history: bot-walked 2026-09-14, moved back by the board login the
  same day, walked again 16:59:38Z · 8 KS-1004 (the cover cell's key) is ARCHIVED — content · 9 the eight linear[bot] walks with their instants ·
  10 the cross-seat SIGTERM (S6 / S7) — one sender alive at every instant (57702 -> 16053), eight READY message ids, none duplicated · 11 the
  originate census's `anchoring:4005` unestablished attempts are "unattributed" — which test file · 12 the shared repo-walk 5 s timeouts (the ks1181
  run-1 STOP) · 13 the seat's S8 — its QUESTION / STATUS request files overwritten by the sender (the mails survive; captured here).

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no PAUSE_QUEUE / queue.md / done.md / READY-file touch, no write into the Secuura checkout (ls-remote /
  show / cat-file / rev-parse / rev-list / diff / ls-tree / log / status / for-each-ref / count-objects / config --get only; every write verb in the
  drafter's scratch clone), no `inbox_routing.conf` write (section 3), no key printed, no port connected except `git ls-remote` and the GitHub /
  AgentMail / Linear READ APIs; no `git fetch` needed (develop unmoved); no Datasec mail opened (subject lines in the inbox listing only).

## 8. How Wednesday (or a cold successor) re-finishes from disk after any change
  In order: (a) `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16B_seatB/capture_ready_mail_gate16B.py`
  (idempotent; never overwrites; picks up any later Seat B STATUS / CORRECTION and rebuilds the combined capture); (b) `python3 …/shape_gate16B.py`
  and `python3 …/predict_batch_scratch_gate16B.py <scratchpad dir>` (re-derives every head, the eight-PR tree, and — if develop moved — fetches the
  new tip by SHA into a fresh scratch clone and rewrites newdev_tree.txt; note the clone path from the output); (c) `python3 …/gh_pr_reads_gate16B.py`
  and `python3 …/linear_reads_gate16B.py` (read-only); (d) edit the DRAFT parts if THE SHAPE changed (a develop move: part2's first bullet and the
  compare line), then `python3 …/fill_prompt_gate16B.py` (refuses on any head disagreement); (e)
  `python3 …/gen_launcher_gate16B.py /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1147-1161.sh <the scratch clone from (b)>`
  (refuses on any pin move, BOTH-list or by-name miss; writes only on bash -n 0); (f) `<that launcher> --check` (rc 0 expected); (g)
  `bash …/launcher_controls_gate16B.sh <that launcher> <that prompt>` (~35 min; read `launcher_check_controls.out`'s "controls end" line — 0 MISMATCH);
  (h) read the prompt WHOLE; (i) section 3, then section 4.
