# Gateset 2026-09-23_gate20T1_seatB — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/ and nothing outside this directory + its own scratchpad)

ONE TIER-1 batch gate over the round-20 tier-1 SEVEN (COMMISSION.md + its AMENDMENT 18:1x + CORRECTION): **#1204 KS-851 QUOTEDNAME** (test_only, PII surface,
kyc tamper) · **#1208 KS-1287 PATHREQUIRED** (code_patch + the REGENERATED `docs/openapi/secuura-api.yaml`, ruling (a) 06:52Z) · **#1207 KS-1245 DEGRADEDWARN**
(bash_patch) · **#1209 KS-1033 MISSINGBASE** (bash_patch, fail-closed design change) · **#1210 KS-1239 RAWAUTHDEAD** (code_patch, pure removal + the ruled
dangling-comment FINDING) · **#1211 KS-1084 SIGTENANT+TPVTENANT** (the P0; two stages, one product file; cross-tenant NOT measured) · **#1212 KS-1143
GUARDMENTION-SELFTEST** (one file = product + test; red-first BY HUNK). 14 paths / 14 rows (6 A + 8 M), +503/-26. All seven heads' parent = BASE
`2bc5ccf63b8c40911afb568b03cace066238ffcf`. Produced in the shape of `../2026-09-23_gate20T2_seatB/`, re-keyed; the tier-2 set's token / bash-kind guards
replaced by this batch's four: self-testing (exit 35), spec regeneration (36), base move (38), body claims (39).

**PR 11 status: LANDED during drafting** (READY 11 08:31:06Z; #1212 `ebb5d85ee0ed7ea524c686c87d504d5fa114962b`, parent BASE). The drafter first PREDICTED it
from its canonical (predict_batch_scratch_3.out: sub-tree `f85c25b427cd`, END `073e658618cf`) and then MEASURED it on the real head (predict_084856.out) —
both equal READY 11's numbers. The launcher carries seven pinned rows; it still refuses without PR 11 (controls P11a / P11b / X, section 3).

## 0. THE BASE MOVED — and the launch re-reads it
Tier 2 merged 08:09:31Z-08:10:39Z (four squashes, `gh_pr_reads_084856.out`). develop at every drafter read since 08:16Z (predict 08:16/08:22/08:51,
fill 08:54:40Z, gen 08:54:44Z, --check, the repin dry runs 08:57Z/08:58Z) = `72f480ca3584ce6eb2fb8ae87247135fbc3106ce`, tree `d13a26e19c8d…` == the tier-2 END_TREE,
4 commits ahead of BASE, all four tier-2 blobs LANDED, nothing else moved (`devmove.txt`). Merged trees over it: seven, in the prompt; END_TREE of the seven
over it `073e658618cf5cbfb88308c1fa36e30c6cf30bec` (three orders one sha; delta 14 files +503/-26; == ALL-11 over BASE — the control).
The launcher pins that develop and REFUSES any other (17/18/19). **`repin_and_launch_gate20T1.sh` reads develop at launch and, if it moved, re-predicts,
re-fills and regenerates in the SAME action** (it refuses rc 10 if the move touches a tier-1 path, if any step refuses, or if develop moves again during
the re-pin). Nothing is hardcoded from a mail.

## 1. Read WHOLE before launching
- The prompt: `2026-09-23_secuura-batch1204-t1.prompt.txt` (this dir; fill run `fill_prompt_2.out`: 190 lines, 52046 B, sha256
  `14d85ae040e120562494472052c8e6b9d100ef33a06bfb147015dd316ddc8d3f`; the previous fill kept beside as `.pre-085440`). First line `ultrathink`; names both seat
  briefs, the capture `mail_gate20T1_ready.md`, the seven `PR #N is KS-x.` sentences, THE BASE MOVED block (develop, the 4 commits, 7 merged trees, END_TREE),
  twelve by-name items, leads (a)-(k), NOT-PINNED, CARRY-FORWARD (the tier-2 report + gate19C), and the GO VERBATIM:
  `GO: merge #1204, #1207, #1208, #1209, #1210, #1211, #1212 batch`.
- The launcher: `launch_qa_secuura_batch1204-t1.sh` (this dir; generator run 2 `gen_launcher.run2.out`: 353 lines, mode 755, sha256
  `df01bf084ecd89568da6273f7140f56e57d7f16f3e34368354d9e8d42baca40a`; run 1's kept beside as `.pre-085444`). Opus 5.5 by the CONFIGURED DEFAULT: the exec line
  carries NO `--model` (Kam 2026-09-23 09:33).
- **Location note:** the drafter's write fence was this directory, so the prompt and launcher live HERE, not in `briefs/` / `launchers/` like the tier-2
  set. The launcher reads its prompt by absolute path; if you copy the launcher into `launchers/`, pass that path to the repin script (its re-pin
  regenerates the launcher at the path it is given).

## 2. What the launcher asserts at EVERY run (`--check` and launch alike)
PENDING-PR- token (34) · the control prompt's `PR11-NOT-YET-RAISED` marker (34) · fewer than 7 rows / a non-40-hex head (34) · thinking directive + brief +
capture (8) · each of the SEVEN heads at origin by branch AND refs/pull/N/head (6 — a STALE HEAD REFUSES) · develop != the pinned launch develop, judged by
content over the 14 targets (19 LANDED / 18 CHANGED / 17 disjoint) · the GitHub compare develop...head per PR: merge_base == BASE, ahead 1, behind == 4,
files 1/3/2/2/2/3/1 (10) · heads in full in capture + prompt (20) · ticket per PR (32) · tier lines (7) · 88 BOTH tokens (30) · 67 by-name keywords (33) ·
self-testing (35) · spec regeneration (36) · base move (38) · body claims (39) · merge authority (26) · MERGE ADDENDUM (25) · verdict subject / sender /
seven lines (23) · BASE / develop / END_TREE in full (31). QAB1204_* overrides refuse at launch (16); non-TTY refuses (21). `--check` ~60 s, headless.

## 3. Controls run by the drafter (all outputs beside)
- **Real launcher** `launcher_controls_gate20T1.sh` -> `launcher_check_controls_1.out` (read its "controls end" line): C STALE HEAD (#1212) -> 6 · D develop
  at BASE -> 17 · E develop at #1204's head -> 19 · S PENDING-PR- -> 34 · P11a PR-11 row PENDING -> 34 · P11b PR-11 row removed -> 34 · X the control prompt
  on the real launcher -> 34 · G -> 8 · O -> 30 · L -> 33 · I #1204 re-graded T2 -> 7 · U -> 35 · V -> 36 · B -> 38 · Y -> 39 · T -> 30 · N non-TTY -> 21 ·
  POSITIVE -> 0.
- **Before PR 11 landed** (the PENDING state): `fill_prompt_1.out` rc 8 and `gen_launcher.run1.out` rc 8 (both refuse without READY 11); a CONTROL COPY
  (six real rows, CONTROL_COPY=1, in the scratchpad only) passed the same ladder 18/18 incl. K: a launch under a pseudo-TTY -> 37
  (`launcher_check_controls_six_2.out`).
- **Repin** `repin_controls_gate20T1.sh` (all `--dry-run`, nothing launched) -> `repin_controls_2.out` 5/5: R1 positive dry run -> 0 · R2 STALE HEAD
  pinned for #1212 -> 11 · R3 KS-1143 row removed -> 8 · R4 CONTROL_COPY -> 8 · R5 pinned develop stale (== BASE) -> 10 (the real run re-pins there).

## 4. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST
Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-batch1204|coagent@agentmail.to|yes
The repin script's step 0 asserts it (rc 1 if absent; control: the batch1202 line = 1). Drafter's read (repin dry runs): batch1204 ABSENT (0).

## 5. The exact launch command (re-pin + launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1_seatB/repin_and_launch_gate20T1.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1_seatB/launch_qa_secuura_batch1204-t1.sh <your session scratchpad under /private/tmp/claude-501/>
Steps: 0b seven pinned rows incl. KS-1143, not a control copy (8) · 0 routing (1) · 1 ls-remote develop + seven pull heads + branches (2) · 2 PULLS API (3)
· 3 heads == pins on both instruments, all open (11) · 3b develop re-read: unmoved -> go on; moved -> predict + fill + gen in the same action, then
develop re-read once more (10) · 4 usage gate (12; this lane's 90% cut is lifted by Kam's 14:24:05 word) · 5 launcher --check (13) · 6 `cockpit.sh add
QA/Secuura-batch1204 <launcher>` (14) + pane census. Add `--dry-run` as a third argument to rehearse steps 0b-3 with no write and no launch.

## 6. What is in this directory
COMMISSION.md (+ `.pre-amendment-1810`) · round20T1.py (+ `.pre-pr11`; selfcheck outs) · capture_ready_mail_gate20T1.py / capture_*.out — the seven READYs
(mail_seatB21_ready03/06/07, mail_seatB22_ready08/09/10/11), every Seat B 21st / 22nd STATUS / QUESTION / wrap / MERGED mail, Wednesday's mails
(mail_wed_*.md: both briefs, the ANSWERs 05:12 / 06:52 / 07:27 / 07:52 / 08:21, the tier-2 GO, the PR-11 ADDENDUM) and the tier-2 QA verdict
(mail_qa_t2_verdict_0735.md); the combined mail_gate20T1_ready.md (the launcher greps it) · checkout_counts.sh + checkout_counts_before/after.txt ·
predict_batch_scratch_gate20T1.py (+ `.pre-pr11`) / predict_batch_scratch_1 (crashed on a print format — rc 1, fixed) / _2 (crashed, rc 1, fixed) / _3
(PR 11 PREDICTED, rc 0) / predict_084856.out (seven MEASURED, rc 0) / newdev_tree.txt (+ `.pre-*`) / devmove.txt · gh_pr_reads_gate20T1.py / gh_pr_reads_1 +
_084856 · linear_reads_gate20T1.py / linear_reads_1 + _084856 · prompt_gate20T1.DRAFT.txt + fill_prompt_gate20T1.py / fill_prompt_1 (rc 8) / _084856 / _2
+ fill_prompt_control_six_1/_2 · launcher_template_gate20T1.sh.txt + gen_launcher_gate20T1.py / gen_launcher.run1 (rc 8) / _084856 / .run2 +
gen_launcher_control_six_1 (rc 4, fixed) / _2 · launcher_check_084856.out + launcher_check_1.out · launcher_controls_gate20T1.sh /
launcher_check_controls_six_1 (K mismatch: `script` needs a tty — replaced by pty.fork) / _six_2 / launcher_check_controls_1 · repin_and_launch_gate20T1.sh
(NOT run for real) / repin_controls_gate20T1.sh / repin_controls_1 + _2 · take_pr11_gate20T1.sh (the re-finish chain) / take_pr11_run1.out · README.md.

## 7. What the drafter did NOT do
No launch, no mail, no tap, no board write, no inbox seen-marking (direct API GETs by message id), no write into the Secuura checkout (ls-remote / status /
for-each-ref / count-objects / config --get / show / cat-file), every git write verb in a scratch clone FROM ORIGIN under its scratchpad; no
`inbox_routing.conf` write; no key printed; no Datasec mail opened (the capture filters on the from-address AND the Blockchain-B / QA-batch subjects).
**NOT pre-run by the drafter (the gate's job): any suite, `npm run generate-openapi`, tsc, eslint, the LEG F map diff.**

## 8. Re-finishing from disk after any change (a cold successor)
`bash take_pr11_gate20T1.sh <scratchpad>` (capture -> self-check -> predict (MEASURED) -> gh / linear -> fill -> gen -> --check; stops at the first
nonzero rc), then `bash launcher_controls_gate20T1.sh <launcher> <prompt> <scratchpad>` (0 MISMATCH), then read the prompt WHOLE, then sections 4-5.

## 9. Checkout census (checkout_counts_before.txt 08:24:48Z -> checkout_counts_after.txt 08:59:48Z)
porcelain non-untracked 0 -> 0 · worktrees 306 -> 306 · config sha256 6417b203accd… unchanged · HEAD develop 3bad652d1 unchanged · for-each-ref 1287 -> 1288
(+ the seat's `refs/remotes/origin/feature/ks-1143-…` tracking ref = its PR-11 push) · loose `count` 1701 -> 1707: every loose object stamped in the window is
08:30:25-26Z and names the SEAT's values (9d0b59ae7199 = PR 11's blob; 5168d809a51b / 3bccc6696567 / a451d545b514 = tier-1 blobs) — the seat's PR-11 verify,
not the drafter (whose write verbs ran only in scratch clones under its scratchpad; the predict runs print count-objects before == after within each run).
Real-launcher controls: launcher_check_controls_1.out — 18 OK / 0 MISMATCH (09:05:45Z).
