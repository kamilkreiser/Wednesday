# Gateset 2026-09-25_gate21T1b — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, committed NOTHING, wrote nothing outside its session scratchpad)

ONE TIER-1 batch gate, round 21 (the round's SECOND tier-1 batch), round 1 of 2, over FOUR PRs (widened from three by Wednesday ~15:2x AEST, FROZEN at four):
**#1224 KS-1179** `d4862b3eee3566635c61cf9d0b810131140e4fa2` (Seat L3; packages/shared ssrf-guard, security) · **#1226 KS-872** `fcda1a6ef7e4fde33215466a29b730025fcd6233`
(Seat L3; type-only jwks.ts) · **#1228 KS-1171** `43279280f76ed9982782ad7652288d2c3d522b71` (Seat L2; anchoring product, Kam's ruling c; legs 3/4/8 OWED) ·
**#1230 KS-1131** `1116dab0466da48ce96c4811f8086b061a49aa70` (Seat B 25th; the ks963 helper, F-A + F-B, TWO commits).
BASE (every head's merge base) = the OLD develop `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`. Develop at the last fill = `379c6eb1d45905f398fae67ee7dd2f46ad40432f`
(7 ahead: the first tier-1 batch AND, during drafting, the tier-2 batch's #1220 / #1215 / #1222). END_TREE over it `58ebabf264e02776ea8fdb3b8f35e016085af75d`
(three distinct orders + `apply --cached`; `9 files changed, 602 insertions(+), 37 deletions(-)`) — predict_4.out. 9 paths, pairwise disjoint; the move's 17
paths ∩ each PR's own paths = EMPTY. Expected GO: `GO: merge #1224, #1226, #1228, #1230 batch`.

## 0. Self-locating kit, and BASE-INVARIANT merge checks
- Every path in the prompt and launcher is the directory `fill_gate21T1b.py` ran in. The launcher refuses (exit 2) anywhere else (control M). Step 0b of the
  repin script re-fills IN PLACE when moved: proved by `movedkit_fill_1.out` (fill rc 0 at `scratchpad/gate21T1b_movedcopy_1`) + `movedkit_check_1.out`
  (`--check` rc 0 there, its launcher names the new home), and control R6.
- Base-invariant (your 04:35Z ruling, `answer_seatB25_movedbase`), in three places: **predict** asserts per PR (1) diff(develop, merged) == exactly its own
  paths at the head blobs, (2) numstat(develop→merged) == numstat(BASE→head), (3) the move ∩ its own paths == EMPTY. **The launcher's** compare (exit 10)
  asserts merge_base == BASE, ahead (1/1/1/2), behind == pin, AND the file NAMES == the PR's own paths (a same-count wrong path refuses: control V).
  **The repin script** also refuses a PR the pulls API reports `mergeable: false` (all four read `True` in repin_dryrun_1.out).

## 1. Read WHOLE before launching
- The prompt `2026-09-25_secuura-batch1224-t1.prompt.txt` (fill_2.out: 207 lines, 54426 B at the scratch home; the byte count changes with the home path).
  Opens `ultrathink`; names the capture `mail_gate21T1b_ready.md` and COMMISSION.md; the four `PR #N is KS-n.` rows; the BASE-INVARIANT section; THE
  STACK S0-S9 (for #1228 only); #1228's ruling section (truth table, real poller, the 400-vs-poll-start equivalence, the early-return check, the census)
  and INTEGRATION section; #1224's guard section; #1226's type-only section; #1230's arms/residuals/relaxation section; LOAD; the LOGIN_STUB REAPER; leads
  (a)-(i); by-name items 1-12; HOLDS; the GO string VERBATIM. Go-template braces in the docker commands are intentional.
- The launcher `launch_qa_secuura_batch1224-t1.sh` (255 lines, mode 755, `bash -n` rc 0 inside fill). Opus by the configured default: no `--model`.

## 2. What the launcher asserts at every run (`--check` and launch alike)
kit at its filled home (2) · four rows (8) · thinking directive + capture + commission + no unfilled fill token (8) · each head at its branch AND
refs/pull/N/head (6) · origin develop == the pinned develop (17) · the base-invariant compare per PR (10) · heads in full in capture + prompt (20) · `PR #N is
KS-n.` in both (32) · tier lines `#N T1` (7) · 37 BOTH tokens (30) · 83 by-name keywords (33) · BASE-INVARIANT rule (34) · STACK rule incl. leg-4 honesty (35)
· #1228 ruling rule (36) · #1228 integration rule (37) · LOAD + the anchoring wording (38) · HOLDS (39) · #1224 guard rule (40) · #1226 type-only rule (41) ·
#1230 rule (42) · login_stub reaper rule (43) · GO string (26) · MERGE ADDENDUM 2/1/5/1 (25) · subject / sender / four lines (23) · BASE / develop / END_TREE
in full (31). Non-TTY launch 21; QAB1224_* overrides at launch 16.

## 3. Controls — `controls_gate21T1b.sh` (both arms: the positive passes, every assertion's fail arm fires)
`controls_3.out`: **35 OK / 0 MISMATCH** (05:48:15Z → 06:01:14Z, over develop 379c6eb1d). Launcher (--check): P positive 0 · C stale #1230 head 6 ·
D develop moved 17 · **V base-invariant compare, a same-count WRONG path for #1226, 10** · G no ultrathink 8 · U unfilled token 8 · O capture missing a seat
item (832/832) 30 · T ticket statement 32 · I tier line 7 · L by-name keyword 33 · B base-invariant rule 34 · K stack rule 35 · K2 "a SKIP is not a pass"
35 · K3 leg-4 honesty ("mint NO credential") 35 · J #1228 both conditions (AND→OR) 36 · J2 integration "NOT APPLICABLE" 37 · Y anchoring wording 38 · Y2
load 38 · H holds 39 · R #1224 "TAMPER THE GUARD" 40 · W #1226 no package.json/lockfile 41 · Q #1230 F-A relaxation 42 · Q2 #1230 residual never green
42 · Z login_stub reaper 43 · A GO string 26 · E addendum 25 · S subject 23 · N non-TTY 21 · M moved launcher 2. Repin: R1 dry run 0 · R2 stale head
11 · R3 pinned develop stale 10 · R4 a REAL run with the routing line absent stops at step 0, rc 1 (auto-skipped once the line exists) · R5 bad
scratchpad 9 · R6 moved-kit dry run 0 (MOVED KIT reported once). Also `repin_dryrun_1.out` rc 0 (05:28Z, over ecb1aa75; mergeable True ×4).
History, not hidden: `controls_1.out` 34/1. B's first anchor wrapped across two prompt lines, so its doctor asserted (rc 4). That was my control's
fault; I re-anchored it. `controls_2.out` 24/11: develop moved mid-run (→ 379c6eb1d), and the launcher REFUSED it for real (17 on every control after H,
10 on R1/R6). That is the guard working; I re-pinned (predict_4, fill_2) and re-ran.

## 4. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1224|coagent@agentmail.to|yes
Drafter's read: batch1224 ABSENT (0); controls batch1213 and batch1215 present (1 each). Repin step 0 refuses rc 1 without it (control R4).

## 5. The exact launch command (copy + re-pin + launch; a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fa11cd0d-1030-4620-83ac-40d313b499eb/scratchpad/gate21T1b/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1b/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1b/repin_and_launch_gate21T1b.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1b/launch_qa_secuura_batch1224-t1.sh <your session scratchpad under /private/tmp/claude-501/>
Steps: 0 routing (1) · 0b moved kit → re-fill here (8) · 1 ls-remote develop + four pull heads + branches (2) · 2 pulls API incl. mergeable (3) · 3 heads
== pins on both instruments, open, not mergeable:false (11) · 3b develop moved → predict (FULL scratch clone, ~275 MB, ~1-2 min) + fill in the same action,
develop re-read once more (10) · 4 usage gate (12) · 5 `--check` (13) · 6 `cockpit.sh add QA/Secuura-batch1224 <launcher>` (14) + pane census. Append
`--dry-run` to rehearse 0-3. `_sp/` holds the drafter's scratch clones and is excluded; the target gatesets dir did not exist at the drafter's read.

## 6. Things Wednesday should decide or know before launching
1. **#1228's "integration cells" do not exist (measured).** At the head: 0 `*.integration.test.ts` and 0 `jest.integration.config.js` under
   services/anchoring (it runs vitest, `vitest.config.ts`); the only `jest.integration.config.js` in the repo is services/originate's (the instrument's
   control), and originate does not import anchorSubmission/confirmation (predict (h), `git grep`). The READY, the PR body and L2's wrap never say
   "integration" (case-insensitive grep for integration|jest|postgres over the 39 mails captured at that point: 1 hit, L2's wrap on KS-1129's JSONB round-trip). The prompt therefore says MEASURE FIRST: if
   0, record "NOT APPLICABLE — none exist" (never green, no originate substitute); if any, run them against the gate's OWN slot Postgres only. If you
   wanted something else (e.g. a DB-backed anchoring cell written by the seat), that is a new ask to L2, not this gate.
2. **The Docker engine is unhealthy.** Docker Desktop's backend processes run, but the API answers `500 Internal Server Error` on `/info`,
   `/containers/json` and `/volumes` (docker_info_1.out 05:08Z; docker_info_2.out 05:59Z, the same 500 on `/info`). The prompt lets the gate wait 300 s,
   then record #1228's legs NOT RUN. It forbids restarting / quitting Docker Desktop it did not start. **If you want the gate to restart Docker Desktop,
   edit S1 before launch; that is your call, not the drafter's.** Also: today's first tier-1 gate KEPT the slot-2 volumes, so the slot rule will pick 3.
3. **#1226's tier:** your 02:25Z plan ANSWER ruled KS-872 **tier 2**; L3's wrap and this commission say tier 1. The gate runs it at tier 1 (a full gate
   subsumes tier 2) and reports both (lead e). Nothing to do unless you want it moved to a tier-2 batch.
4. **MG-3 finding before the gate even runs:** #1226 is attached in Linear to **two** issues, KS-872 AND KS-1292 (both `contributes`), because its body
   says `Refs KS-1292` (linear_reads_2.out). The squash body must carry KS-872 only; whether KS-1292's attachment stays is yours (lead f). #1228's body
   names KS-584 and KS-726 (both ARCHIVED) and KS-562 as hyphenated keys; attachments today are KS-1171 only.
5. **#1228's timing proof is "since poll start", not "since the 400".** You adopted it at 03:06Z. The gate is told to confirm on the code path that
   polling starts at or after the 400 on the guard-3 path (lead c). The drafter modelled the production schedule (30 attempts, 10 s start, ×1.5, 60 s
   cap, 0-2 s jitter): attempt 5 is the first that always starts ≥ 60 s after polling began (~81 s), so the ABSENT arm is reachable. This is a
   PREDICTION from the code (predict (h)), not a run.
6. **#1230's blind spot is real by construction:** F-A swaps `count(…, consumeFn)` for `count(…, consumeFn + '(')` (predict (j)), so a hoisted consume
   that is not written `consumeResetToken(` (an alias, `.call`, a space before the paren) is no longer counted. The prompt names these shapes and demands
   red-proof or a KS-1131 residual, never green.
7. **Seat B 25th's same READY mail also carries #1231 KS-1281 and #1232 KS-1128.** The seat labels them tier 2, but your 10:59 plan ruling said "tier 1 ×3
   in ONE batch". They are NOT in this gate (per your widening); route them to the next tier-2 batch or re-tier them.
8. Develop moved DURING the drafting (ecb1aa75 → 379c6eb1d at ~05:45Z, the tier-2 batch merging). The launcher refused it for real (controls_2.out: every
   control after H returned 17, and R1/R6 returned 10). predict_4 + fill_2 re-pinned. If develop moves again before launch, the repin script's step 3b
   re-pins in the same action. Nothing else needs doing.

## 7. How to widen (not needed now, the batch is frozen at four; recorded for the next time)
To add a PR: `predict_gate21T1b.py` (a `PRS` dict row: n, key, head, branch, files with numstat, `ncommits` if > 1; plus any per-PR section) ·
`fill_gate21T1b.py` (`BR`, `ROWS`, BOTH tokens from the new READY) · `launcher_gate21T1b.TEMPLATE.sh.txt` (a `PRS` row `n|KS|branch|{{HEAD_n}}|files|ahead|{{PATHS_n}}`,
the row count `-eq 4`, the GO string, the subject, the addendum counts `2/1/5/1 = 9`) · `prompt_gate21T1b.TEMPLATE.txt` (the `PR #N is KS-n.` row, the tier
line, the GO string, the subject, the addendum counts, the merged-tree list) · `capture_mail_gate21T1b.py` (KEYS + the READY-set filter) ·
`gh_read_gate21T1b.py` / `linear_reads_gate21T1b.py` (the PR tuples) · `derive_repin_gate21T1b.py` (the `NS` list and the ls-remote line) · `controls_gate21T1b.sh`
(the doctored GO/subject/addendum strings). Then run capture → predict → fill → `--check` → controls → `--dry-run`, in that order.

## 8. Files
COMMISSION.md · PROPOSED_inbox_routing_line.txt · README.md · lsremote_1..3.out · gh_read_gate21T1b.py / gh_read_1.out (three PRs) / gh_read_2.out (four) /
gh_body_{1224,1226,1228,1230}.md / gh_comments_*.md · capture_mail_gate21T1b.py / capture_list.out / capture_1..3.out (+ .rc; capture_1 swept L2's #1216/#1217
READY in because its subject names KS-1171, which I fixed; capture_3 rc 0, 4 sections, all eight keys) · mail_*.md (50 per-mail files + the combined
mail_gate21T1b_ready.md) · quarantine/ (one hand-captured duplicate of Seat B 25th's READY 3/4/5, moved there rather than deleted) · linear_reads_gate21T1b.py /
linear_reads_1.out (three) / linear_reads_2.out (four) · predict_gate21T1b.py / predict_1..4.out (+ .rc: predict_1 rc 1 = the drafter's own instrument bug
(stripped stdout lost a file-final `}`), fixed and recorded in the script; predict_2 rc 0 three PRs over ecb1aa75; predict_3 rc 0 four PRs over ecb1aa75;
predict_4 rc 0 four PRs over 379c6eb1d) / pins_gate21T1b.txt / devlog_gate21T1b.txt · prompt_gate21T1b.TEMPLATE.txt + launcher_gate21T1b.TEMPLATE.sh.txt +
fill_gate21T1b.py / fill_1.out (rc 0, over ecb1aa75) / fill_2.out (rc 0, over 379c6eb1d; the fill_1 outputs kept as `.pre-054728`) · launcher_check_1.out /
_2.out (rc 0 each) · derive_repin_gate21T1b.py / derive_repin_1.out → repin_and_launch_gate21T1b.sh / repin_dryrun_1.out (rc 0, over ecb1aa75 — before the
move) · controls_gate21T1b.sh / controls_1..3.out · movedkit_fill_1.out / movedkit_check_1.out · docker_info_1.out / docker_info_2.out.

## 9. NOT done / NOT measured by the drafter
No launch, mail, tap, commit, push or routing-conf write. The Secuura checkout was touched only with `ls-remote` and `config --get`. The seats' records
were READ only (`ls`). Every git write verb (clone, fetch, merge-tree, commit-tree, read-tree/apply/write-tree) ran in scratch clones FROM ORIGIN under the
session scratchpad (`g21b_sp/`, `gate21T1b/_sp/`). NOT pre-run (the gate's job): any suite, tsc, eslint, emit, red proof, tamper, truth table, `npm ci`, the
stack. UNMEASURED: whether the Docker engine recovers; the usage gate's state at launch; whether legs 3/4/8 reach any anchoring operation; whether
polling starts after the 400 on every guard-3 path (read, not measured); the production reachability of the 60 s condition beyond the modelled schedule;
`mergeable` after the latest develop move (repin_dryrun_1 read `True` ×4 over ecb1aa75; the real run re-reads it); the develop-moved branch of repin step 3b
end to end (its parts ran by hand: predict_4 → fill_2 → `--check`).
