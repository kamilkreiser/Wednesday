# Gateset 2026-09-25_gate21T2 — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, committed NOTHING, wrote nothing outside this directory)

ONE TIER-2 batch gate, round 21, round 1 of 2, over SIX PRs (FROZEN at six by Wednesday) on develop `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (== BASE):
**#1215 KS-1288** `5e3419a46db5a1a4e7e640aee2e60dd89db3912a` (L3, packages/shared test) · **#1218 KS-897+KS-896** `999623d28f7cc3f11140cf379cfd3169e6530b57`
(L4, bash suite; TWO commits, ahead 2) · **#1220 KS-1129** `9c2021ba3e770abc9ad464b62fdc245a920389cb` (L2, anchoring PRODUCT; legs 3/4/8 OWED) ·
**#1221 KS-1266** `0a561a5db393e8f0ced82b86af572c7231330d64` (L1, 7 originate test files) · **#1222 KS-1181** `9bce90229ad60b4ab988248648530b3b9a0d951d`
(L3, packages/shared test) · **#1223 KS-1118** `759726d8d046e6098e720d4768c87e114d0c363c` (L1, originate test + one product COMMENT).
14 paths, pairwise disjoint; END_TREE `75b43d7d4e3a4ea3c6ddff374a50ef7e63a0e7dd` (three orders + `apply --cached`; `14 files changed, 458 insertions(+), 97 deletions(-)`).
Built in the shape of the sibling tier-1 kit `../2026-09-25_gate21T1` (template + pins + fill, self-locating launcher, repin-and-launch, controls) with
the tier-2 content of `../2026-09-23_gate20T2_seatB/`. The expected GO: `GO: merge #1215, #1218, #1220, #1221, #1222, #1223 batch`.

## 0. The kit is SELF-LOCATING — drafted in the drafter's scratchpad
Every path in the prompt and launcher is the directory `fill_gate21T2.py` ran in. The launcher refuses (exit 2) outside that directory;
`repin_and_launch_gate21T2.sh` step 0b re-fills IN PLACE when the kit is moved (proved: `movedkit_fill_1.out` rc 0 + `movedkit_check_1.out` rc 0 on an
rsync copy). `_sp/` holds the drafter's four scratch clones (~185 MB each) — the launch command EXCLUDES it.

## 1. Read WHOLE before launching
- The prompt `2026-09-25_secuura-batch1215-t2.prompt.txt` (fill_2.out: 378 lines, 49994 B, sha256 0020bb51… at the scratch home — it changes with the
  home path when re-filled). Opens with `ultrathink`; names the capture `mail_gate21T2_ready.md` (the SIX READY FOR QA mails, verbatim by message id)
  and COMMISSION.md; the six `PR #N is KS-n.` rows; TIER AND ROUND; THE RED PROOFS (per PR, RED at BASE / GREEN at HEAD); THE PORT PROBE (#1221);
  LEGS 3/4/8 (NOT run ×5, OWED #1220, cases A/B + REACH); #1220's CONSUMERS; the ANCHORING WORDING; LOAD; leads (a)-(m); by-name items 1-12; HOLDS; the
  GO string VERBATIM. Go-template braces in the docker commands are intentional.
- The launcher `launch_qa_secuura_batch1215-t2.sh` (238 lines, mode 755, `bash -n` rc 0). Opus by the configured default: no `--model`.

## 2. What the launcher asserts at every run (`--check` and launch alike)
kit at its filled home (2) · six rows (8) · thinking directive + capture + commission + no unfilled fill token (8) · each head at its branch AND
refs/pull/N/head (6) · origin develop == the pinned launch develop (17) · compare per PR: merge_base BASE, ahead 1/2/1/1/1/1, behind == pin, files
1/1/2/7/1/2 (10) · heads in full in capture + prompt (20) · `PR #N is KS-n.` in both (32) · tier lines `#N T2` (7) · 40 BOTH tokens (30) · 71 by-name
keywords (33) · LEGS rule (35) · RED-PROOF rule (36) · PORT PROBE rule (37) · LOAD + anchoring wording (38) · HOLDS (39) · GO string (26) · MERGE
ADDENDUM 1/1/2/7/1/2 (25) · subject / sender / six lines (23) · BASE / develop / END_TREE in full (31). Non-TTY launch 21; QAB1215_* overrides at launch 16.

## 3. Controls — `controls_gate21T2.sh` -> `controls_1.out`: 28 OK / 0 MISMATCH (04:14:34Z)
Launcher: P 0 · C stale #1223 head 6 · D develop moved 17 · G no ultrathink 8 · U unfilled 8 · O capture missing a seat item 30 · T ticket 32 · I tier 7 ·
L keyword 33 · K legs rule 35 · K2 "a SKIP is not a pass" 35 · K3 "OWED" -> "green" 35 · B red-proof 36 · X port probe 37 · Y anchoring wording 38 · Y2
load 38 · H holds 39 · A GO string 26 · E addendum 25 · S subject 23 · N non-TTY 21 · M moved launcher 2. Repin: R1 dry run 0 · R2 stale head 11 · R3
pinned develop stale 10 · R4 a REAL run with the routing line absent stops at step 0, rc 1 (auto-skipped once the line exists) · R5 bad scratchpad 9 ·
R6 moved-kit dry run 0 (MOVED KIT reported once). Also `repin_dryrun_1.out` rc 0 (04:05Z; every read == the pins).

## 4. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1215|coagent@agentmail.to|yes
Drafter's read: batch1215 ABSENT (0); control batch1213 present (1). Step 0 of the repin script refuses rc 1 without it.

## 5. The exact launch command (copy + re-pin + launch; a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fd48946b-a14b-4837-ab61-8d5d11816b69/scratchpad/gate21T2/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2/repin_and_launch_gate21T2.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2/launch_qa_secuura_batch1215-t2.sh <your session scratchpad under /private/tmp/claude-501/>
Steps: 0 routing (1) · 0b moved kit -> re-fill here (8) · 1 ls-remote develop + six pull heads + branches (2) · 2 pulls API (3) · 3 heads == pins, all
open (11) · 3b develop moved -> predict + fill in the same action, develop re-read once more (10) · 4 usage gate (12) · 5 `--check` (13) · 6 `cockpit.sh
add QA/Secuura-batch1215 <launcher>` (14) + pane census. Append `--dry-run` to rehearse 0-3.

## 6. Things Wednesday should know before (or when) launching
- **#1220's legs 3/4/8 will almost certainly stay OWED.** The tier-1 gate (already running, pane QA/Secuura-batch1213, started 03:55Z) builds its stack
  from #1216/#1217, whose anchoring bytes are develop's, and tears it down at its S9. This prompt obeys "if the stack is up, run legs 3/4/8 for #1220" (case
  A) but requires the run to name whose anchoring answered: a run against develop's anchoring is recorded as a REFERENCE, not #1220's evidence. Also
  measured: `anchors/verify` appears 0 times in `docs/openapi/secuura-api.yaml` at BASE (control `anchors/document` 3) and anchoring.openapi.ts registers
  4 paths, not the verify route — the route is service-to-service only, so spec-driven legs 3/4/8 may be UNABLE to reach #1220's field at all. The gate is
  told to measure that REACH. If you want the legs discharged for real, the only way inside the "stack once" rule is a one-service anchoring rebuild at
  9c2021ba3 inside the tier-1 gate's slot before its S9 — that is a change to the tier-1 commission, your call.
- **#1222 wording:** your widening said the filter "DOES forward entity.too.large"; the seat's READY/body say the opposite — `payloadTooLargeErrorHandler`
  forwards generic and details (true/false/true) and ANSWERS entity.too.large (oversize false). The prompt carries the seat's version as the claim to
  measure and tells the gate to say which is true.
- **#1221's "real ECONNREFUSED" is not measured by the seat's own probe**: netprobe-l1.cjs records connect ATTEMPTS only (no outcome / error code). The
  prompt requires an outcome-recording copy plus a standalone bad-port vs :2 control. The five `127.0.0.1:1` left under originate are all DATABASE_URL.
- **MG-11:** #1218's title is 114 chars and #1221's 113 (> 92) — the merge seats need shorter squash subjects; the gate is told to name them.
- **#1223's PR body omits the legs-3/4/8 line** its READY carries (hygiene lead k).
- **Not in this batch, will need the NEXT one:** #1219 KS-1277 (L1, tier 3 comment-only — no gate by the tier rule, your call); Seat L3's KS-1179
  (tier 1, commit d4862b3ee, push queued), KS-872 (being built), KS-1143 GF-2 (a40cb9eea, held on #1215's squash); Seat L2's KS-1171 (tier 1, in
  build); Seat L1's remaining PRs (J KS-1291 "pushing now", D/E/F/G/H/I, R1); Seat L4's PR 3 (KS-1252+1253), PR 4 (+KS-808 b), PR 2 (tier 1, last).

## 7. Files
COMMISSION.md · PROPOSED_inbox_routing_line.txt · README.md · lsremote_1..3.out · gh_read_gate21T2.py / gh_read_1..3.out (+ .rc) / gh_body_{1215,1218,
1220,1221,1222,1223}.md / gh_comments_*.md · capture_mail_gate21T2.py / capture_list.out / capture_2..4.out (+ .rc; capture_4 rc 0, 6 READY sections,
all six keys) · mail_*.md (35 per-mail files + the combined mail_gate21T2_ready.md) · linear_reads_gate21T2.py / linear_reads_1.out ·
predict_gate21T2.py / predict_1..4.out (+ .rc; predict_4 rc 0, 0 hard fails; predict_1 rc 1 = the drafter's own patch-strip bug in the second
instrument, fixed and recorded in the script) / pins_gate21T2.txt / devlog_gate21T2.txt (empty: develop == BASE) · prompt_gate21T2.TEMPLATE.txt +
launcher_gate21T2.TEMPLATE.sh.txt + fill_gate21T2.py / fill_1.out (rc 8: a BOTH token absent from the capture — fixed) / fill_2.out (rc 0) ·
launcher_check_1.out · derive_repin_gate21T2.py / derive_repin_1.out -> repin_and_launch_gate21T2.sh (NOT run for real except control R4, which stopped
at step 0) / repin_dryrun_1.out · controls_gate21T2.sh / controls_1.out · movedkit_fill_1.out / movedkit_check_1.out · quarantine/ (a mislabelled
first capture, the first capture's out/rc, and one temp file the drafter's fill wrote to the scratchpad root, moved in) · _sp/ (scratch clones — excluded).

## 8. NOT done / NOT measured by the drafter
No launch, mail, tap, commit or routing-conf write. The Secuura checkout was touched only with `ls-remote` and `config --get`; the seats' records were
READ only; every git write verb ran in a scratch clone FROM ORIGIN under this directory. NOT pre-run (the gate's job): any suite, tsc, eslint, red proof,
probe, `npm ci`. UNMEASURED: whether the tier-1 stack will be up when this gate reaches #1220's legs; whether legs 3/4/8 can reach GET
/api/anchors/verify/:hash at all (the drafter read the spec text only); the usage gate's state at launch; the machine load (five builder seats + the
tier-1 stack build); the develop-moved branch of step 3b end to end (develop has not moved).
