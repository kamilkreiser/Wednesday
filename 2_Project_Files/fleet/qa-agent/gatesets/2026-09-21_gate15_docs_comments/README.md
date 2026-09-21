# Gateset 2026-09-21_gate15_docs_comments — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE batch gate over Seat B 15th's TEN docs / test-file-comment PRs (#1136, #1137, #1139, #1140, #1141, #1142, … — NOT contiguous: #1138 is KS-1285's
foreign PR, MERGED at 12:44:19Z and the reason develop MOVED), graded at the TIER 2 floor (five Markdown documents + five comment-only test-file
PRs; 11 paths, 0 overlap, 0 product bytes). Produced in the exact shape of `gatesets/2026-09-21_gate1130to1135/`. Everything below is read-only
evidence or a file for YOU to run. **Section 8 says how to finish from disk if the drafter's bound hit before all ten READYs landed (the prompt
and launcher on disk are then the `…batch15_partial…` pair, which REFUSE to launch — a record, not a gate).**

## 0. THE DEVELOP MOVE (read this first — it changes the addendum's merged trees)
Origin develop moved off the heads' parent `581ed7fa124b85c7c2da89ac05d52f99c2502911` to **`b192ffd4a61d1b01bb9485a0f5260ca9fd69cf05`** (tree
`30c3e9342d64…`) at 12:44:19Z: PR **#1138** KS-1285 (Schemathesis 4.27.2 -> 4.27.5) merged as a **MERGE COMMIT** (3 commits, 7 files under
`systemTest/` + `Projects Documents/`, +121/-27). ∩ this round's 11 paths = ∅; ∩ the paths the gate reads = ∅; no `services/` or `packages/` path
(`dev_move_reads_1.out`, `predict_batch_scratch_3.out` (c)). Every head's parent is still 581ed7fa1, so: compare develop...head = merge_base
581ed7fa1, ahead 1, **behind 3** (the launcher asserts exactly that — a FURTHER move refuses at exit 10); each PR's merged tree over the CURRENT
develop is a real 3-way tree, NOT its head tree (the ten are in `newdev_tree.txt` and in the prompt's THE SHAPE); the END STATE over b192ffd4a is
`87b4aa12d2ebae335f11790ceed9158f7d5614ec` (the seat's `a93fe063d28a…` is the all-ten over the OLD base — still true, still the tree its batch
suites ran on). Who merged #1138 was not this seat; the seat recorded the move as a non-event at READY 3 onward.
**If develop moves AGAIN before the launch**: `python3 predict_batch_scratch_gate15.py <scratchpad>` (it fetches the new tip BY SHA into its own
`--shared` scratch clone over the checkout's ssh road — never into the checkout), then `python3 gen_launcher_gate15.py <launcher> <that clone>`,
then re-read the prompt's THE SHAPE bullets (the move, the merged trees, the END STATE) and edit `prompt_gate15.DRAFT.part1.txt` accordingly
before `fill_prompt_gate15.py`.

## 1. Read WHOLE before launching
- The prompt (COMPLETE form, once all ten READYs are captured): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1136-<last>.prompt.txt`
  (first line `ultrathink`; THIRTEEN by-name items exactly as commissioned; the develop-move shape; the ten `PR #N is KS-x.` sentences one per
  line; the namespace coincidences — KS-1140 is PR 6's ticket while PR #1140 is PR 4; #1138 is foreign; PR #1036 is KS-763's; PR #1049 (merged,
  KS-1271) is the commit that moved CLAUDE.md :293 -> :303; the MERGE ADDENDUM with ONE equality target per FILE (PR 7 two, comma-separated =
  MG-2); NOT-PINNED rows NONE EXPECTED, said so; report.md before the mail; the ten-line verdict + the exact subject prefix).
  The PARTIAL form written at the drafter's bound, if that is what is on disk: `…/briefs/2026-09-21_secuura-batch15_partial.prompt.txt` — its
  second line names which PRs are IN; every `PENDING-PR-n` / `PENDING-HEAD-PR-n` token is a slot; the launcher refuses it at exit 34.
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1136-<last>.sh` (or
  `launch_qa_secuura_batch15_partial.sh`) — pins the CURRENT develop b192ffd4a + every head (branch AND refs/pull/N/head, exit 6); compare guard
  per PR merge_base 581ed7fa1 / ahead 1 / behind 3 / files (exit 10); the develop pin judged by CONTENT over 41 paths (the 11 targets — LANDED
  exit 19 if any is at a head blob — plus 30 unchanged-read paths incl. the 14th's five tamper files, the hook, preflight.sh, run-shell-suites.sh,
  jwt.ts, provenance.ts, proxy.ts, the four lanes' package.json / lock / config); the grep ladder (BOTH tokens + 91 by-name keywords); overrides
  `QAB1136_*` refuse at launch (16); TTY (21); PARTIAL (34). `--check` is headless and launches nothing (~60-90 s).
- `DRAFTER_REPORT.md` — every value beside its instrument, the leads, the drafter's own slips FIRST, what is UNMEASURED.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1136-<last>.sh --check
  Drafter's runs: see DRAFTER_REPORT.md section 1 (the partial launcher's `--check` rc 34 by design at 13:08:34Z; the complete launcher's, if
  written before the bound, `launcher_check_1.out`).

## 3. The routing line — NOT WRITTEN BY THE DRAFTER (this commission confined writes to the gateset + briefs + launchers): add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1136|coagent@agentmail.to|yes
  `repin_and_launch_gate15.sh` step 0 asserts it (rc 1 if absent; control: the batch1130 line's count = 1). A cockpit pane that is not routed
  cannot be tapped.

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments/repin_and_launch_gate15.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1136-<last>.sh
  It reads its pins FROM THE LAUNCHER (no second copy): (0) asserts the routing line and refuses a PARTIAL prompt (rc 8); (1) `git ls-remote`
  develop + every pull head + every branch (READ, into `lsremote_launch.out`); (2) re-reads every head from the PULLS API (`api_heads_launch.out`);
  (3) refuses rc 10 if develop is not the launcher's pin (b192ffd4a), rc 11 if any head moved or a PR is not open; (4) `fleet/usage_gate.sh --check`
  (rc 12); (5) the launcher's own `--check` (rc 13, `launcher_check_launch.out`); (6) `cockpit.sh add QA/Secuura-batch1136 <launcher>` (rc 14,
  `cockpit_add.out`) and a pane census. `bash -n` rc 0; NOT RUN by the drafter.

## 5. What is in this directory (all read-only evidence unless named above)
  COMMISSION.md — Wednesday's commission (22:32 AEST)
  poll_ready_gate15.sh / .log / .nohup.out / inbox_all_pollN.out — the bounded inbox poller (`inbox_digest.sh --all`, never marks seen; 120 s cadence, 60 min, stop at ten)
  capture_ready_mail_gate15.py / capture_ready_mail_N.out — every READY + the 12:30 STATUS + the 12:02 QUESTION + Wednesday's ANSWER + the brief as sent,
    VERBATIM by message id (TEXT_SHA256 per file): mail_seatB15_ready01_pr1_ks1035.md … ready10_pr10_ks1156.md · mail_seatB15_status_1230.md ·
    mail_seatB15_question_question_plan_confirmation_seat_b_15th_1202.md · mail_wed_answer_plan_confirmation_seat_b_15th_1203.md ·
    mail_wed_successor_seat_b_15th_raise_14_held_doc__1141.md · mail_gate15_ready.md (the combined capture the launcher greps: the READYs in push order, then the STATUS, then the QUESTION)
  lsremote_1.out / lsremote_2.out / checkout_counts_before.txt / checkout_counts_after.txt — origin + the checkout's counts (BEFORE 12:35:38Z; AFTER at the drafter's close)
  shape_gate15.py / shape_N.out — local object reads (the 14 canonicals + sha16s + fence-vs-run, the 11 target blobs, per landed head: parent / behind-ahead / tree / blobs / modes / numstat / DOCS-ONLY / COMMENT-ONLY proof with its control; the F4 / F5 / hook static reads)
  predict_batch_scratch_gate15.py / predict_batch_scratch_N.out / newdev_tree.txt — EVERY git write verb, in a --shared --no-checkout scratch clone: the 14 applies (strict / -R / --recount rcs, blobs), the per-PR and all-14 trees over 581ed7fa1 in three orders, the landed heads by real 3-way merges, and section (c) the develop move (fetched by SHA into the clone; the per-PR merged trees and the END STATE over b192ffd4a); count-objects byte-identical
  dev_move_reads_gate15.py / dev_move_reads_1.out — the move via the GitHub API (compare, PR #1138, the 11 blobs at the new tip)
  gh_pr_reads_gate15.py / gh_pr_reads_N.out — GitHub GETs (heads, bases, files API, Refs, detectors, compares, ruleset, the open-PR sweep incl. #920 / #887 / #1138, the PR-number traps)
  linear_reads_gate15.py / linear_reads_N.out — Linear reads (the 12 own tickets, attachmentsForURL per PR, KS-1136..KS-1147, the 19 archived + content keys, controls)
  prompt_gate15.DRAFT.part1..3.txt + fill_prompt_gate15.py / fill_prompt_N.out — the prompt's three parts and the fill script (substitutes PRs 5-10 from the captures; PARTIAL when any is missing)
  gen_launcher_gate15.py + gen_launcher.runN.out — the generator (run 1: two BOTH misses — a wrapped seat phrase and `127.0.0.1` absent from the READYs; run 2: four by-name phrases wrapped; run 3: the same, rejoin incomplete; run 4: output-control counts and a `-` in a bash variable name (the `-PARTIAL` suffix) — fixed with a separate `__SUFFIX__` token; run 5: written)
  launcher_check_partial_1.out (rc 34, by design) · launcher_check_1.out (the complete launcher, if written) · launcher_controls_gate15.sh + launcher_check_controls.out (controls A-S + positive, each rc; run by Wednesday or a successor — ~25 min) · controls_dir_gate15.txt
  repin_and_launch_gate15.sh — the launch action (NOT run)
  *.pre-HHMM-* — the drafter's pre-fix copies (never a delete)

## 6. Leads for the gate (full text in DRAFTER_REPORT.md; the gate grades them; NO drafter-vs-seat VALUE disagrees)
  1 the develop move (#1138, a MERGE commit) — the addendum's merged trees are the 3-way trees over b192ffd4a, not the head trees · 2 F8: the hook's
  filter is by PATH — nine `.md`/comment pushes RAN the preflight (12/15, 44 of 44), the CLAUDE.md push ran none; KS-1049-A's ADDED line and the
  hook header :5 both say "docs-only" loosely · 3 F4: CLAUDE.md moved between the hold tip 48e65c435 (blob b1020f4b8c77, the `-` line at :293) and
  581ed7fa1 (:303) via merged #1049 KS-1271 — a PR number equal to a ticket number of this round; "step 6" count 0 in the whole file · 4 F5: the
  tip's proxy.ts three-part shape count 6 (attachScopes 8, requireScope( 6; `router.<verb>(` 69) — neither "eight" nor "seven" · 5 F1: the four run
  patches byte-equal to their fences; KS-890's two run patches (00164f008163dead / 36e396b3a007e5f0) ≠ its fence · 6 the READYs list KS-764 /
  KS-879 / KS-1020 / KS-835 under "Live-but-foreign / content" by state while they are ARCHIVED (the seat's own F3) — a labelling slip · 7 the
  namespace: KS-1140 = PR 6's ticket, PR #1140 = PR 4; PR #1036 OPEN = KS-763's (+ KS-775); #1138 foreign · 8 the linear[bot] walks (all twelve,
  actor GitHub; the first four at 12:32:16Z / 12:39:54Z) · 9 PR 7's `generateAccessToken` exists at jwt.ts:187; `tenantId: user.tenantId` at :201
  is unconditional in that payload literal while :295 spreads it conditionally elsewhere — is the new comment right? · 10 PR 8's provenance.ts:109
  is `if (!connectorOrgId) return null;` with the reason at :107-:108 · 11 the shared repo-walk guards' 5 s timeouts (the seat's run 1) — does not
  block · 12 the seat's S1 (a ref write before the brief; Q8 LEAVE) — the checkout's HEAD is `develop` at 581ed7fa1.

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no PAUSE_QUEUE / queue.md / done.md / READY-file touch, no write into the Secuura checkout (ls-remote /
  show / cat-file / rev-parse / rev-list / diff / ls-tree / log / status / for-each-ref / count-objects / config --get only; every write verb in
  the drafter's scratch clones), no `inbox_routing.conf` write (section 3), no key printed, no port connected except `git ls-remote`, ONE
  `git fetch` BY SHA into the scratch clone over the checkout's own ssh road (b192ffd4a — the moved develop; the https road with the token was
  refused "Repository not found" — S1), and the GitHub / AgentMail / Linear READ APIs; no Datasec mail opened (subject lines in listings only).

## 8. If the drafter's bound hit first — how Wednesday (or a cold successor) finishes from disk
  In order: (a) `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments/capture_ready_mail_gate15.py` until every
  `mail_seatB15_ready<k>_pr<n>_*.md` (01..10) exists (idempotent; never overwrites; it also picks up any later STATUS / CORRECTION); (b)
  `python3 …/shape_gate15.py <scratchpad dir>` and `python3 …/predict_batch_scratch_gate15.py <scratchpad dir>` (re-derives every landed head, the
  all-ten trees over BOTH bases, and re-fetches the current develop by SHA into a fresh scratch clone — note its path from the output); (c)
  `python3 …/gh_pr_reads_gate15.py` and `python3 …/linear_reads_gate15.py` (read-only; the attachmentsForURL sets and the bot walks for the
  late PRs); (d) `python3 …/fill_prompt_gate15.py` — with all ten captured it writes `…/briefs/2026-09-21_secuura-batch1136-<last>.prompt.txt`
  (it refuses if PR 10's number is not the highest); READ the two by-name lines that name PR 10's READY details (F5 with the seat's instrument;
  the GO subject string the seat wrote — `GO: merge #1136-#<last> batch` is what the generator's BOTH list expects: if the seat wrote the numbers
  listed instead, edit that BOTH token in gen_launcher_gate15.py to the seat's exact string); (e)
  `python3 …/gen_launcher_gate15.py /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1136-<last>.sh <the scratch clone from (b)>`
  (refuses on any pin move, BOTH-list or by-name miss; writes only on bash -n 0); (f) `<that launcher> --check` (rc 0 expected); (g)
  `bash …/launcher_controls_gate15.sh <that launcher> <that prompt>` (~25 min; each control names its rc; read `launcher_check_controls.out` — the
  "controls end" line with 0 MISMATCH); (h) read the prompt WHOLE; (i) section 3, then section 4.
