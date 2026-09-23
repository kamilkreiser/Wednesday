# Gateset 2026-09-23_gate20T1r2_1210 — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, committed NOTHING, wrote nothing outside this directory + its scratchpad)

ONE TIER-1 RE-GATE, round 2 of 2 (under the two-NO-GO cap), of **#1210 KS-1239 RAWAUTHDEAD** alone: head `6b572240fc31e564a6d0c516fdff66814bb856c6`
(parent = round-1 head `231ab8b5c898`, parent BASE `2bc5ccf63b8c`). The first job is round 1's one Major, **LEGD-LINEPIN**. Built in the shape of
`../2026-09-23_gate20T1_seatB/`, reduced to one PR. The launcher is rendered from a template (not generated from a 7-PR table) because there's only one row.

## 1. Read WHOLE before launching
- The prompt: `2026-09-23_secuura-1210-t1r2.prompt.txt` (185 lines, 23313 B, sha256 `e07194f9b2f4a71b69c1ece0e37938671577542645fe142c8525db56c2c44315`).
  It opens with `ultrathink`, names the capture `mail_r2_ready.md` (READY r2 + the round-1 QA verdict, verbatim by message id), the commission, the
  round-1 report, THE THREE JOBS (LEGD-LINEPIN closed? / the +17/-8 graded for scope / disjointness from #1212 with a control that fires), leads (a)-(j),
  and the GO string VERBATIM: `GO: merge #1210 batch`.
- The launcher: `launch_qa_secuura_1210-t1r2.sh` (141 lines, mode 755, sha256 `c874de583672400900241951a07dd508192e40e961d264282730a84ecf9a5788`).
  Opus 5.5 by the configured default: the exec line has NO `--model`.

## 2. What the launcher asserts at every run (`--check` and launch alike)
The head is at its branch AND `refs/pull/1210/head` (6; a STALE HEAD REFUSES) · origin develop == the pinned `dd8f99cc75b9…` (17) · the GitHub compare:
merge_base BASE, ahead 2, behind 10, files 3 (10) · thinking directive + capture + commission named, no unfilled token (8) · the head in full in the
capture and the prompt (20) · 21 BOTH tokens (30) · 33 by-name keywords (33) · merge authority + the GO string (26) · MERGE ADDENDUM rules (25) · verdict
subject / sender (23) · BASE / develop / merged tree in full (31). Non-TTY launch refuses (21); QA1210_* overrides refuse at launch (16).

## 3. Controls (all outputs beside) — `controls_r2.sh` -> `controls_1.out`: 13 OK / 0 MISMATCH
Launcher: P positive `--check` 0 · C STALE HEAD 6 · D develop at BASE 17 · G no `ultrathink` 8 · O the capture missing a seat item 30 · L a keyword
missing 33 · A the GO string missing 26 · N non-TTY launch 21. Repin: R1 positive dry run 0 · **R2 STALE HEAD pinned 11** · R3 pinned develop stale
(== BASE) 10 · R4 a REAL run with the routing line absent stops at step 0, rc 1 (it is skipped automatically once the line exists, so the controls
script can never launch) · R5 a bad scratchpad 9.

## 4. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST
Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (back it up first with a `$(date +%H%M)` stamp):
    QA/Secuura-1210r2|coagent@agentmail.to|yes
The repin script's step 0 checks for it (rc 1 if missing; the control line is batch1204 = 1). What the drafter read: 1210r2 ABSENT (0).

## 5. The exact launch command (re-pin + launch are ONE action — you run it, in a shell that can reach tmux)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1r2_1210/repin_and_launch_r2.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1r2_1210/launch_qa_secuura_1210-t1r2.sh <your session scratchpad under /private/tmp/claude-501/>
The steps: 0 routing (1) · 1 ls-remote develop + pull head + branch (2) · 2 pulls API (3) · 3 head == pin on both, open (11) · 3b re-read develop.
If it hasn't moved, carry on. If it has moved, run `predict_r2.py` and then `fill_r2.py` in the same action, then re-read develop once more (10) · 4 usage gate (12) · 5 `--check` (13) ·
6 `cockpit.sh add QA/Secuura-1210r2 <launcher>` (14) + a pane census. Add `--dry-run` as the third argument to rehearse steps 0-3.

## 6. Files
COMMISSION.md · capture_mail_r2.py / capture_1.out (6 mails since 08:59Z, read by message id and never marked as seen; from-address AND subject filter) ·
mail_*.md + the combined mail_r2_ready.md · predict_r2.py (+ `.pre-controlfix`, `.pre-devmove`) / predict_1.out (**rc 1: the drafter's own
overlap control was on the wrong line and did not fire**), predict_2.out (fixed, rc 0), predict_3.out (+ the develop-move guard, rc 0) / pins_r2.txt /
devlog_r2.txt · gh_read_r2.py / gh_read_1.out · prompt_r2.TEMPLATE.txt + launcher_r2.TEMPLATE.sh.txt + fill_r2.py / fill_1.out · launcher_check_1.out ·
repin_and_launch_r2.sh (NOT run for real; R4 ran for real and stopped at step 0 — `launch_103236.routing.out` is that run's) · controls_r2.sh / controls_1.out.

## 7. NOT done by the drafter
No launch, no mail, no tap, no commit, no routing-conf write. The Secuura checkout was touched only with `ls-remote` and `config --get`, and every git write verb ran in a scratch clone from origin
under the scratchpad. Not pre-run (these are the gate's job): any suite, tsc, eslint, the red-first at the round-1 head, the live-pin control, Linear reads.
The develop-moved branch of step 3b (predict + fill over a NEW develop) was not exercised end to end, because develop has not moved. Its parts ran over the current develop.
