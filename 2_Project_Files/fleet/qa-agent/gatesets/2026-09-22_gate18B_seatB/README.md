# Gateset 2026-09-22_gate18B_seatB — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE batch gate over Seat B 18th's SEVEN PRs — #1170 KS-1118 F3b (comment), #1172 KS-1158 R5b (comment), #1174 KS-1265 EARLYGUARD (code_patch: the
round's ONE PRODUCT change, originate `documents.ts` +8/-0 + its test), #1176 KS-1171 8J-TSFIX + GUARD3S-TSFIX (test_only, TWO files — MG-2),
#1177 KS-811 F7SETPIN (test_only, AUTH surface), #1178 KS-1188 MFASIBLINGS (test_only, AUTH/MFA surface), #1179 KS-1181 F3w (comment) — TIER 1 on
#1174 / #1177 / #1178, TIER 2 on the rest. Nine paths, 0 overlap, four lanes (originate jest, anchoring `vitest run`, auth vitest, shared
`vitest run`), 0 under api-gateway (Seat C 18th's partition — its six PRs #1167 #1168 #1169 #1171 #1173 #1175 interleave in the same window).
Produced in the exact shape of `gatesets/2026-09-22_gate16B_seatB/` (the gate15/16 pipeline). Everything below is read-only evidence or a file for YOU to run.

## 0. THE ROUND'S ONE NEW SHAPE (read this first — it is what the gate exists to measure)
EVERY head's parent is `3916eacd12af23bfd464440b4c770f7da0f2dd96` (the seat's item-0 tip) while origin develop is `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
— the #1036 squash (KS-763, 50 paths: 20 package.json + 29 package-lock.json + scripts/audit/audit-baseline.json) landed at 22:54:32Z on Seat C 18th's
GO, between the seat's item 0 (22:50Z, develop UNMOVED) and its first push (23:52Z). MEASURED by the drafter (`predict_batch_scratch_1.out` (c),
`p1036_paths.out`, `shape_1.out`): #1036's 50 paths ∩ the seat's 9 targets = ∅ and ∩ its 4 tamper files = ∅ — the seat's load-bearing claim
CONFIRMED — BUT the move touches the MANIFESTS of all four lanes (packages/shared package.json + lock, services/auth package.json + lock,
anchoring lock, originate lock, the Dev root lock): every lane baseline the seat quotes was measured at the OLD locks. So each PR alone over
develop is a REAL 3-way merge (not a fast-forward) and the addendum's per-PR tree is the MERGED tree, not the head tree; the prompt carries all
seven merged trees, the all-7 tree over the parent `a36532029483c3f8a4ca0cd33ec1219076ef9219` (the seat's, reproduced 7 ways) and **the
END_TREE over develop `76a88d9ddfa4f50098aa639a1056c5c9387aeb18`** (4 merge orders + 3 apply orders + generator tree-hash -> ONE sha; differs from
the parent-based tree on EXACTLY the 50 moved paths). THE GO must carry `BASE_GO = 8c2f7b3fd4fde915b2a24542bc32259b24e092a0` and `END_TREE =
76a88d9ddfa4f50098aa639a1056c5c9387aeb18` — while develop is still 8c2f7b3fd. **If develop moves before the launch** (Seat C 18th's six merges on
its own GO is the likely cause — its ten paths are disjoint from these nine and the four tamper files, measured): `python3
predict_batch_scratch_gate18B.py <scratchpad>` (fetches the new tip BY SHA into its own `--shared` scratch clone over the checkout's ssh road —
never into the checkout — and rewrites `newdev_tree.txt` incl. the END_TREE and the seven merged trees), then edit `round18B.py`'s `DEV` /
`DEV_TREE` to the new tip (the fill and the generator REFUSE while origin != the pin — by design), then `python3 fill_prompt_gate18B.py` (it
re-substitutes every merged tree and the END_TREE), then `python3 gen_launcher_gate18B.py <launcher> <that clone>` (BEHIND becomes the move
count), then re-read the prompt's THE SHAPE bullets (the `behind 1` / `50 paths` prose in part2 must be edited by hand).

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1170-1179.prompt.txt`
  (first line `ultrathink`; TWELVE by-name items exactly as commissioned — item 3 carries the #1036 intersection and the END_TREE, item 5 the
  code_patch RED/GREEN protocol and the (b) ruling's BOTH numbers, item 6 the typecheck delta incl. documents.ts and the ks727 TS1378 (F7), item 9
  the lock windows / the four-condition attributions / the process-namespace rule / the measure18.py no-cwd-guard question, item 12 the seven
  addendum lines with MG-2 exercised on #1174 and #1176 and SHIPS-WITH KEY-FREE; the CONTEXT RULE at ctx 80; the seven `PR #N is KS-x.` sentences
  one per line; the namespace coincidences — KS-1171 is PR 4's OWN ticket while PR #1171 is Seat C's KS-1231; KS-1181 is PR 7's while #1181 is a
  404; the drafter's LEAD that #1178 CLOSES the 16C gate's NOT-PINNED rows MFASIBLINGSITES-166 / -397; the NOT-PINNED candidate rows
  ROUTECOLLAPSECOVEREDBYKS795 / MFASIBLINGSITES-166/-397 / HEADERWORDINGONLY / GUARDBEFORESAVEORDER / PRELOADTIMINGARTEFACT / MANIFESTSMOVEDUNDER1036;
  report.md before the mail; the seven-line verdict + the BASE_GO / END_TREE line + the exact subject prefix; the GO string). Drafter's last fill:
  1028 lines, 145682 B, sha256 ea5ffc74b68656fafb2fd5c0032d1921e397f9ac082aad9ff16bd3d8328f3bb2 (`fill_prompt_3.out`; re-derive before launch:
  `shasum -a 256 <prompt>`). No `deadbeef` literal (the fill and the generator both refuse one).
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1170-1179.sh` — pins develop
  8c2f7b3fd + every head (branch AND refs/pull/N/head, exit 6; the ks-1171 glob must return ONLY the R16 TSFIX branch); compare guard per PR
  merge_base 3916eacd1 / ahead 1 / BEHIND 1 / files 1-1-2-2-1-1-1 (exit 10 — Seat C's merges would read behind 7 and REFUSE); the develop pin judged
  by CONTENT over 46 paths (the 9 targets — 4 judged ABSENT, 5 by blob, LANDED exit 19 if any is at its head blob; 28 unchanged-read paths incl.
  the 4 tamper files, the hook, preflight.sh, run-shell-suites.sh, jwt.ts, provenance.ts, proxy.ts, documentRepo.ts, the ks795 / threadTokenMint /
  ks1004 / ks1188-mfa-status / ks949 / ks1181 test files, the lanes' unmoved configs; 8 MOVED manifests judged at develop's post-#1036 blobs);
  the grep ladder (BOTH 174 tokens + 122 by-name keywords); overrides `QAB1170_*` refuse at launch (16); TTY (21); PARTIAL (34, inherited).
  `--check` is headless and launches nothing (~100 s). 530 lines, mode 755, sha256
  508d1e3bfa519238e060be8255941a456a32aa975ddf87f046942b7b7d7d8a56 (`gen_launcher.run5.out`).
- `DRAFTER_REPORT.md` — the drafter's own slips FIRST, every value beside its instrument, the leads, what is NOT MEASURED.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1170-1179.sh --check
  Drafter's runs: `launcher_check_1.out` rc 0 at 01:52:17Z-01:53:59Z; `launcher_check_2.out` rc 0 at 02:17:30Z-02:18:28Z (against the final
  1028-line prompt). The controls: `launcher_controls_gate18B.sh` -> `launcher_check_controls.out` — `controls end 2026-09-22T02:12:33Z: 20 OK / 2
  MISMATCH` then `launcher_controls_gate18B_rerun.sh` -> `rerun end 2026-09-22T02:17:18Z: 2 OK / 0 MISMATCH` (A-U + POSITIVE, each rc on its own
  line; T PASSES by design — the launcher greps heads, not addendum blobs; the two first-run MISMATCHes are the drafter's S5 typo on U's expected
  code (the launcher refused at 31 as intended) and a transient GitHub RemoteDisconnected on the POSITIVE (fail-closed UNJUDGEABLE -> 18; rc 0 on
  the re-run) — DRAFTER_REPORT.md sections 4 and 8).

## 3. The routing line — NOT WRITTEN BY THE DRAFTER (this commission confined writes to the gateset + briefs + launchers): add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1170|coagent@agentmail.to|yes
  `repin_and_launch_gate18B.sh` step 0 asserts it (rc 1 if absent; control: the batch1147 line's count = 1). A cockpit pane that is not routed
  cannot be tapped. Drafter's read at 01:55Z: count 0 (absent, as expected); the batch1147 control 1.

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18B_seatB/repin_and_launch_gate18B.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1170-1179.sh
  It reads its pins FROM THE LAUNCHER (no second copy): (0) asserts the routing line and refuses a PARTIAL prompt (rc 8); (1) `git ls-remote`
  develop + every pull head + every branch + the ks-1171 glob (READ, into `lsremote_launch.out`; rc 4 unless EXACTLY one ks-1171 branch — the
  R16 TSFIX one); (2) re-reads every head from the PULLS API (`api_heads_launch.out`); (3) refuses rc 10 if develop is not the launcher's pin
  (8c2f7b3fd), rc 11 if any head moved or a PR is not open; (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own `--check` (rc 13,
  `launcher_check_launch.out`); (6) `cockpit.sh add QA/Secuura-batch1170 <launcher>` (rc 14, `cockpit_add.out`) and a pane census. `bash -n` rc 0;
  the pin-parse sed dry-read prints develop 8c2f7b3fd, END_TREE 76a88d9ddfa4 and the seven PRs (section 5 of DRAFTER_REPORT); NOT RUN by the drafter.

## 5. What is in this directory (all read-only evidence unless named above)
  COMMISSION.md — Wednesday's commission (11:11 AEST)
  round18B.py — the ONE source of this round's pins for every script (every script imports it and asserts against origin / local objects / the READYs)
  inbox_list_gate18B.py / inbox_list_1.out — the inbox listing (subjects only; Datasec subjects unread)
  capture_ready_mail_gate18B.py / capture_ready_mail_1.out — every Seat B 18th READY (7 mails, 8 rows) + its two STATUS (23:47Z; the 01:08Z HOLD) + two
    QUESTION mails + Wednesday's brief / two ANSWERs, VERBATIM by message id (TEXT_SHA256 per file): mail_seatB18_ready01_pr1_ks1118.md …
    ready07_pr7_ks1181.md · mail_seatB18_status_2347.md · mail_seatB18_status_0108.md (the HOLD) · mail_seatB18_question_*.md · mail_wed_*.md; Seat C
    18th's six READYs + STATUS / QUESTION mails + Wednesday's mails to it (incl. `GO: merge #1036`) as mail_seatC18_*.md / mail_wedC_*.md (context for
    by-name 3 / 9 only); mail_gate18B_ready.md (the combined seat-B capture the launcher greps: the READYs in push order 1-7, then the STATUS mails,
    then the QUESTION mails — rebuilt on every capture run; its first line carries the rebuild instant)
  lsremote_1.out / local_reads_1.out / checkout_counts_before.txt / checkout_counts_after.txt — origin + the checkout's counts (BEFORE 01:14:14Z; AFTER at the drafter's close)
  shape_gate18B.py / shape_1.out — local object reads (the 8 apply units + the KS-1265 whole patch = cat(sections), the READY fences vs the run
    patches 8/8, the checker records incl. A4 / A5, the 9 targets at the parent AND develop, the 4 tamper blobs at three tips, the tamper `from`
    counts substring AND whole-line, per head: parent / behind-ahead vs BOTH bases / tree / blob / lines / `-` lines / the comment-only proof /
    the product hunk; the #1036 move's 50 paths and what they touch; the branch-name scanner 7/7 + the ks-1257 control; the lanes' test scripts;
    the ks795 cover cell by name; the ks727 :243 await; the octopus 5185c65cf)
  predict_batch_scratch_gate18B.py / predict_batch_scratch_1.out / newdev_tree.txt / p1036_paths.out / checkout_counts_predict_{before,after}.txt —
    EVERY git write verb, in ONE --shared --no-checkout scratch clone under a CWD GUARD (the script chdirs into the clone and asserts cwd / git-dir /
    object-dir before any write verb; refuses rc 2 otherwise): the 8 units strict / -R / --recount, the per-PR trees (KS-1265 and KS-1171 both
    orders), the all-7 over the parent in three apply orders + the seven heads by real 3-way merges in four orders, each head MERGED over develop
    both orders (the seven addendum trees), the all-7 over develop in four merge orders + three apply orders (THE END_TREE), the #1036 intersection
    by set arithmetic, the 50-path difference between the two batch trees; count-objects byte-identical; section (d) the develop re-read
  gh_pr_reads_gate18B.py / gh_pr_reads_1.out — GitHub GETs (heads, bases, files API, Refs, detectors, compares, ruleset, #1036's files, Seat C's six
    PRs with the four-condition inputs, the open-PR sweep, the PR-number traps, the window #1167..#1181)
  linear_reads_gate18B.py / linear_reads_1.out — Linear reads (the 7 own tickets + the three bot walks, attachmentsForURL per PR, the Linear
    branchName fields still carrying ks-999 / ks-727, Seat C's six keys, KS-1167..KS-1181, the 30 archived + 19 content keys, KS-795, controls)
  prompt_gate18B.DRAFT.part1..3.txt + fill_prompt_gate18B.py / fill_prompt_N.out — the prompt's three parts and the fill script (re-reads origin IN
    THE SAME ACTION and refuses if origin / round18B / the READYs disagree on any head or develop is off the pin; substitutes the PR numbers, heads,
    READY instants, the parent + its tree, develop + its tree, the all-7 tree over the parent, the END_TREE and the seven merged trees)
  gen_launcher_gate18B.py + gen_launcher.runN.out — the generator (run 1: the Dev root package.json in the MOVED list did not move — corrected; run 2:
    a BOTH token `whole line` vs the prompt's `whole-line`; run 3: three wrapped by-name phrases — unwrapped in part3; run 4: the output-control
    counts for `exit 10` / `exit 19` under this launcher's header — corrected; run 5: written)
  launcher_check_1.out (rc 0) · launcher_check_2.out (rc 0, against the final prompt) · launcher_controls_gate18B.sh + launcher_check_controls.out
    (controls A-U + positive, each rc) · launcher_controls_gate18B_rerun.sh + launcher_check_controls_rerun.out (U2 / POSITIVE2) · controls_dir_gate18B.txt
    · lsremote_final.out · checkout_counts_after.txt
  repin_and_launch_gate18B.sh — the launch action (NOT run)
  *.pre-HHMM-* — the drafter's pre-fix copies (never a delete)

## 6. Leads for the gate (full text in DRAFTER_REPORT.md; the gate grades them; NO drafter-vs-seat VALUE disagrees)
  1 THE MANIFESTS MOVED under #1036 while the seat's baselines were measured at the old locks — the lanes at develop are the gate's NEW baseline ·
  2 #1178 (KS-1188 MFASIBLINGS) CLOSES the 16C gate's NOT-PINNED rows MFASIBLINGSITES-166 / -397 (its proposed cells are this PR's F1c / F1d) —
  the first CLOSED rows a local-model round produces; the gate measures it · 3 the ks795 cover on KS-811's ROUTECOLLAPSE: what the F7SETPIN cells
  add (the published-vs-thrown SET) — and KS-795 is ARCHIVED (content) · 4 the ks727 TS1378 at :243 pre-exists (F7) · 5 the seat's measure18.py has
  no cwd guard — the seat's records say no object was added (9214 -> 9214) and the loose objects it met were Seat C's S1 · 6 the namespace:
  KS-1171 (PR 4's own) vs #1171 (Seat C's KS-1231); KS-1181 vs #1181 (404); KS-1179 (Seat B 16th's #1157) vs #1179 (PR 7) · 7 the Linear
  branchName fields STILL carry `ks-999` / `ks-727` (excised only in the pushed names) · 8 the 8J anchor ambiguity (substring 2 / whole-line 1) ·
  9 the two F9 quarantines and the S3 removed rc file · 10 the loose-object count 9064 (16th) -> 9416 (now) — what grew it · 11 documentRepo.ts's
  cited lines :540-544 (the R5b comment) — is that the shallow spread.

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no PAUSE_QUEUE / queue.md / done.md / READY-file touch, no write into the Secuura checkout (ls-remote /
  show / cat-file / rev-parse / rev-list / diff / ls-tree / log / status / for-each-ref / count-objects / config --get only; every write verb in the
  drafter's scratch clone under the cwd guard; count-objects 9416 / 101422 / 47 byte-identical before and after), no `inbox_routing.conf` write
  (section 3), no key printed, no port connected except `git ls-remote` and the GitHub / AgentMail / Linear READ APIs; no `git fetch` (develop
  unmoved off the pin at every read); no Datasec mail opened (subject lines in the inbox listing only); nothing written into the sibling
  `2026-09-22_gate18C_seatC/` dir (its captures were read as context only).

## 8. How Wednesday (or a cold successor) re-finishes from disk after any change
  In order: (a) `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18B_seatB/capture_ready_mail_gate18B.py`
  (idempotent; never overwrites; picks up any later Seat B STATUS / CORRECTION and rebuilds the combined capture); (b) `python3 …/shape_gate18B.py`
  and `python3 …/predict_batch_scratch_gate18B.py <scratchpad dir>` (re-derives every head, both batch trees, the seven merged trees and the
  END_TREE, and — if develop moved — fetches the new tip by SHA into a fresh scratch clone and rewrites newdev_tree.txt; note the clone path from
  the output); (c) `python3 …/gh_pr_reads_gate18B.py` and `python3 …/linear_reads_gate18B.py` (read-only); (d) if develop moved: edit round18B.py's
  DEV / DEV_TREE and the DRAFT parts' THE SHAPE prose, then `python3 …/fill_prompt_gate18B.py` (refuses on any head disagreement); (e)
  `python3 …/gen_launcher_gate18B.py /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1170-1179.sh <the scratch clone from (b)>`
  (refuses on any pin move, BOTH-list or by-name miss; writes only on bash -n 0); (f) `<that launcher> --check` (rc 0 expected); (g)
  `bash …/launcher_controls_gate18B.sh <that launcher> <that prompt>` (~35 min; read `launcher_check_controls.out`'s "controls end" line);
  (h) read the prompt WHOLE; (i) section 3, then section 4.
