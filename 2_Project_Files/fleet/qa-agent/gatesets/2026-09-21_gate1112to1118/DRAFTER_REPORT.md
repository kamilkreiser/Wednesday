# DRAFTER REPORT — batch gate #1112-#1118 (Seat B 12th, seven test-only PRs, tier-1 floor B/C/F)
Drafted 2026-09-20T20:36Z-21:3xZ (06:36-07:3x AEST 2026-09-21). Nothing launched, mailed, tapped or posted. Read verbs only in the Secuura checkout.

## FOUND (what was produced — every path absolute)
- Gateset dir `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1112to1118/` (43 files): `gen_launcher_1112.py` (+ run1-4 outs),
  `capture_ready_mail.py/.out`, `list_ready_mail.py/.out`, the ELEVEN mail captures (`mail_seatB12_plan_confirmation_1845.md`, `mail_seatB12_status_1934.md`,
  `mail_seatB12_ready1_A_ks1203.md` … `mail_seatB12_ready7_F_ks1006.md`, `mail_wed_answer_plan_confirmation_1847.md`, `mail_wed_answer_all_seven_read_2031.md`) and the
  combined `mail_batch1112_ready.md` the launcher greps, `lsremote_1.out`, `shape_1.py/.out`, `source_reads.sh/.out`, `predict_batch_scratch.sh/.out`,
  `gh_pr_reads.py/.out`, `linear_reads.py/.out`, `launcher_check_1.out`, `launcher_controls.sh` + `launcher_check_controls.out`, `controls_dir.txt`,
  `prompt_keyword_counts.out`, `repin_and_launch.sh` (NOT run), `mail_leads.out` (17 leads), `README_FOR_WEDNESDAY.md`, this report.
- Launcher `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1112-1118.sh` (542 lines, sha256 b918efc7a016457a…, mode 755):
  pins develop 362e51fe0 + the seven heads; compare guard per PR (merge_base/ahead=1/behind=0/files 1/1/1/1/5/1/1 → exit 10 on any move); develop judged
  by CONTENT over 58 paths (11 PR paths — 8 develop blobs + 3 ABSENT, LANDED → 19; 10 tamper files; 37 unchanged-read paths) → 18/19; the grep ladder
  7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33; overrides refuse at launch 16; TTY 21; pane name `QA/Secuura-batch1112`; report dir
  `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/`.
- Prompt `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1112-1118.prompt.txt` (789 lines, 103035 bytes, sha256
  365d4279dc691333…; first line `ultrathink`) in the previous prompt's shape: namespace note (KS-1112..KS-1118 real tickets; PR #1006 a real PR that is
  not KS-1006; the ELEVEN newer READYs not in this gate; KS-1273's patch touches #1117's tamper file); per-PR table; TIER PER PR 2/1/1/2/2/2/1
  (Wednesday's Q3), batch tier 1; MERGE AUTHORITY = WEDNESDAY'S signed GO naming each head; MG-1 1/1/1/1/5/1/1, MG-2 targets13.py:28/:31 with PR E's
  five comma-separated, MG-3 KEY-SET rule per squash body (merge13.py:54-:64, two keys on C/E/F); all ten tickets STAY, none filed; THE SHAPE (no
  develop move → seven fast-forwards; all-seven tree 6aa9873f97… six orders); CANONICAL-PATCH identity for all fifteen (sha256 x15, hunks, head blobs);
  the ten tamper files; sources (the eleven captures, the brief, the seat's record folder READ-ONLY, the fifteen READYs by filename, the run dirs, the
  PRIOR #1106-#1111 / ANCHORING #1105 / EARLIER #1102-#1104 reports); Postgres isolation + CENSUS RULE v2 with the REPORT extension for anchoring/auth
  (Q7); the services' own listens (anchoring :4005 on import, auth :4003 via auth.integration.test.ts:609, originate :4000) and the census interaction;
  KS-1201; NOT-TESTED.written-first.md opening items; SEVENTEEN by-name items with the nine LEADS as claims (F1 / F2 / F3 graded, INSTR-1, the 12/15
  skips, the anchoring ratio with the ONE red, TRIVY_JOB_SH copies + shellcheck NOT RUN, auth 779 first-measured, S1-S5, the all-fifteen tree, the
  line-number discipline naming who inherited a wrong value); NOT-PINNED candidate rows incl. BY DESIGN rows; the seven MERGE ADDENDUM reads (11 blobs
  with modes); report.md BEFORE the mail; the exact subject `[QA -> Wednesday] BATCH GATE #1112-#1118 (seven PRs; tier 1 = #1113, #1114, #1118) — …`.

## TESTED (every re-derived value beside the seat's, with the command)
- `git ls-remote origin refs/heads/develop refs/pull/1112..1118/head 'refs/heads/feature/ks-<key>-*'` (lsremote_1.out, 20:37:59Z): develop 362e51fe0 = seat;
  heads 3a28d2a3c / abf8321a9 / 762a70117 / b008489e4 / 9a485cfe7 / b3f94f14a / f132c9214 at BOTH refs = the seven READYs; the merged same-key branches
  `-untyped-1` (47593b77b) and `-order-1` (f5a599b07) still exist (the seat's zero-at-origin was on the NAME — consistent).
- `shape_1.py` (rev-list --parents / rev-parse / diff --raw --abbrev=40 / diff --numstat, 20:39:31Z): parent == 362e51fe0 x7; develop...head 0/1 x7; head
  trees == GROUPING x7 (7b8734234ed5 / 5c8e11681434 / c6a6a7380f1d / fea63ca447a2 / ea9fc7d7cefc / 8de2a19066c9 / 7e75405911ec); 11 (develop, head)
  blob pairs == GROUPING (d68c6b2be95b / 92966f9c1f62 / 6d837e0aeeb8 / 27366baf3251 / d3d29533c9ee / a6765883d409 / 57de9c9e2478 / f461e832c566 /
  d42259343d79 / 35bbb4519950 / bfa8b1d3fc36; three ABSENT at develop); +8/+4/+24/+6/+131/+19/+24 = +216, deletions 0 x7; 11 paths all under
  `__tests__/`, 21 pairs overlap 0; the ten tamper files' bytes / sha256 / blob == the seat's x10 and the develop blob at every head x70; commit
  subjects 91/88/90/78/92/90/91 chars (#1116 exactly 92 — lead 17). ALL SHAPE ASSERTIONS HELD: True.
- `source_reads.sh` (git show … | grep -c -x -F, 20:41:07Z): the 27 `from` lines each exactly once at the tip (22 on the first pass; five re-counted after
  the drafter's typed-whitespace slip — all 1); positive controls SUPER_ROLES.includes 2 / x-api-key 3 / connectormeta 5 / LIFECYCLE_EVENT_ACTIONS 3 /
  anchorIdentityView 2 / toCardanoMetadatum 2 / verifyTOTP 3 / LEVEL_ORDER 3 / latest 3 = the seat's nine; the trivy `# ----` context line 8x = the plan
  mail's 8; the F1 cell at ks1215:319, the F2 cell at ks480-connector-auth:135, the F3 covers at readback :88 / :107 / :101 / :72 / :55 / :58 and
  metadatum :198 / :170 / :181 — every title the seat names is at develop; the new cells' `it(` titles at each head (2 / 1 / 2 / 1 / 10 / 1 / 3 = 20 +
  the trivy `ok` line); T11/T12 read index.ts as TEXT (readFileSync), T13 imports CSL + `vi.mock('../cardano/provider')`; the hook runs the BRANCH's
  preflight (`.githooks/pre-push:276-278`); skip_stack at preflight.sh :296 / :310 / :495 (legs 3/4/8); locks: vitest 4.1.11 (api-gateway, anchoring,
  auth), jest 29.7.0 (originate); CSL 15.0.3 in anchoring package.json; anchoring index.ts `PORT || 4005` + `app.listen` on import (:80/:2028), auth
  `PORT || 4003` (:65/:276) with auth.integration.test.ts:609 importing ../index, originate `PORT || 4000`.
- `predict_batch_scratch.sh` (git clone --shared --no-checkout into the scratchpad; merge-tree --write-tree chained through commit-tree; 20:42:36Z):
  each head alone over develop = its head tree, both orders (fast-forward) x7; all-seven tree 6aa9873f974019a92574d6db52e6356734573c8c in SIX orders
  (forward A B C D E G F, exact reverse, four others) == the seat's octopus tree; read-tree back → 2e981e7779dc… ; 11 files +216 insertions, 8 M + 3 A;
  every PR path in the all-seven tree carries its head blob (0 MISMATCH lines); each single-PR tree ≠ the all-seven tree x7; numstat from an empty
  repo rc 128; checkout porcelain 17 / worktrees 204 before and after (the seat's eight s-b12-* worktrees are the +8 over the previous gate's 196).
- `gh_pr_reads.py` (read-only GETs, 20:43:38Z): heads == pins x7, base == 362e51fe0 x7, open, mergeable_state unstable x7; files API union 11, 0 files
  outside `__tests__/`, deletions 0 x7; Refs lines == own key set x7 (two on #1114 / #1116 / #1118); closing/completeness detectors 0/0/0 x7 (controls
  fire on "Completes KS-1282", not on "PREFLIGHT INCOMPLETE — 12/15"); archived / foreign keys in title / branch / subject NONE x7; `ks-878867` in no
  branch; the required scope sentences present in every body (B guard/register-connector/requireSuperAdmin; C optional-mount/Bearer/NOT pinned; E live
  sweep/MOCKED provider/nothing anchored/threadTokenMint; F mfaSecret/stale-approval/NOT decided); compares merge_base 362e51fe0 ahead 1 behind 0
  files 1/1/1/1/5/1/1; ruleset 18499832 require-pr-gates active, three rules, required_approving_review_count 0, require_extra_approval_for_unattributed_changes
  true; 25 open PRs — only #995 touches a tamper file (anchoring index.ts), none touches the 11 paths; control: merged #1105 ∩ tamper files = 4.
  PR-number namespace: PR #1006 exists (closed, KS-844); the other nine 404.
- `linear_reads.py` (read-only GraphQL, 20:45:17Z): ten tickets In Progress, assignee the board login x10, none archived; the six Backlog-at-boot walked by
  actor GitHub at 19:52:34Z / 19:59:44Z x2 / 20:20:58Z / 20:27:57Z x2; attachmentsForURL pull/1112..1118 == {KS-1203} / {KS-1283} / {KS-1198, KS-1244} /
  {KS-1275} / {KS-1175, KS-1284} / {KS-1137} / {KS-1006, KS-1236}, all contributes; the existing #1103 / #1102 / #1105 links untouched; comments
  1/0/0/0/0/1/3/0/0/0; KS-1112..KS-1118 exist, Backlog, 0 attachments; the 13 archived (archivedAt set, none reopened) and 17 foreign as the seat
  read; control pull/1111 → {KS-1223 contributes}.
- `gen_launcher_1112.py` run 4 (07:05Z): 15 refs OK; tree-hash control; 7 composes == head trees; compose(11) == 6aa9873f97…; BOTH-list 180 tokens in
  BOTH the capture and the prompt; namespace + tier lines one line each; by-name ladder 100 keywords across 17 items + closing; output controls all
  equal; heredoc parity PY (10/10) PYJ (120/120); bash -n rc 0.
- `--check` (`launcher_check_1.out`, 07:07:20 AEST): rc=0.
- Controls (`launcher_check_controls.out`, 21:09-21:27Z), each rc on its own line, 19/19 OK, 0 MISMATCH: A missing prompt 4 · B brief absent 3 · C
  wrong #1118 head 6 · D CUR_DEV = old develop cbae988db 18 (GUARDED ks480-connector-auth.test.ts eca492723) · E CUR_DEV = #1118's head 19 (LANDED
  #1118 own) · F launcher copy expecting behind=1 10 (the sed asserted landed: copy 1, real 0) · G no thinking directive 8 · H #1114 namespace sentence
  reworded 32 · I COMMA-separated reworded 25 · J RULE WHETHER IT BLOCKS reworded 30 · K by-name 5 reworded 33 · L loopback GATEWAY_URL reworded 31 ·
  M #1113 demoted to TIER 2 7 · N non-TTY LAUNCH 21 (all guards passed first; nothing launched) · O subject prefix shortened 23 · P (new) MG-3 KEY-SET
  phrase reworded 25 · Q (new) :4003 lsof discipline reworded 29 · R (new) #1116's second key dropped from its namespace sentence 32 · positive: the
  real launcher --check 0.
- `prompt_keyword_counts.out`: 60 keywords all non-zero (each head x1, #1116 x34, KS-1244 x20, targets13.py x12, merge13.py x15, BY DESIGN x12, RULE
  WHETHER IT BLOCKS x1, ultrathink x1); absent-by-design controls KS-1102 / the #1106 table line / the full cbae988db sha = 0.

## HOW (method)
Read the previous gateset whole (generator, launcher, prompt, report, helpers, outputs), the template, charter, standing lines, the seat's brief,
inbox_routing.conf; captured the eleven mails verbatim by message id (key by name from the WEDNESDAY .env, never printed); re-derived every value with
read verbs in the checkout and write verbs only in a `--shared --no-checkout` scratch clone under the scratchpad; wrote the prompt in the previous shape
with Wednesday's rulings and the leads as claims; generated the launcher with pins re-read live, tree hashing, BOTH-list and by-name ladders, output
controls, heredoc parity and bash -n; ran `--check` and eighteen refusing controls plus a positive; wrote the launch action (not run) and the README.
The drafter's tools never wrote into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (porcelain 17 → 17, worktrees 204 → 204,
for-each-ref 1102 → 1102), never connected to any port, never printed a key.

## LEADS (in `mail_leads.out`, 17 — the gate grades them; the drafter's re-derivation disagrees with the seat NOWHERE)
1 identical census totals in READY A (14 runs) and B (12 runs) · 2 auth loopback 208 (STATUS) vs 1896/21 (READY F) · 3 the brief's per-file absolutes
(auth.test 17->19, identity 52->53, ks480prov UNSTATED) vs the seat's 16->18 / 51->52 / 13->14 — Wednesday's class, deltas agree · 4 CODECJOINDROPPED
cover ONE (brief) vs FOUR (seat) · 5 READY E's "red=N" includes develop's own red (NEW = N-1) · 6 F1's meaning · 7 F2's meaning · 8 INSTR-1 · 9 READY G
truncates the cell title (five truncated-title tokens excluded from the BOTH list, commented in the generator) · 10 "20 listeners" vs "18" · 11 PR
#1006 exists (KS-844) · 12 ELEVEN newer READYs, not ten (KS-957 F4-TOOLINGTOKENS-1, 06:37) · 13 KS-1273 EXITCODEENV-1 (banked) patches #1117's tamper
file · 14 the `n_ran=$(printf` duplicate control now 1 (post-#1109) · 15/16 the drafter's own slips · 17 #1116's subject exactly 92 chars.

## DRAFTER'S OWN SLIPS (recorded, none reached a produced artefact uncorrected)
S1 five tamper `from` lines typed into source_reads.sh with the brief's unindented whitespace (originate.openapi.ts:1740, anchorReadback.ts:111/:112,
   cardanoMetadatum.ts:81, anchoring index.ts:890) counted 0; re-counted from the tip's bytes → 1 each (source_reads.out addendum, 20:41:37Z). The
   prompt names the class (BY-NAME 4 / 17) and quotes the lines WITH their indentation.
S2 shape_1.py's unchanged-read list guessed a non-existent path `services/anchoring/src/anchorIdentityView.ts` (the function lives in
   anchorReadback.ts:38); printed ABSENT, dropped from the generator (whose list refuses on a missing path).
S3 gen run 1 refused on eight BOTH tokens: six the READYs TRUNCATE (cell titles cut at ~80 chars) — removed from the BOTH list with a comment, kept in
   the prompt; two the prompt had wrapped across lines — the prompt lines were rejoined (the greps are line-based). Run 2 refused on a third wrapped
   phrase (RULE WHETHER IT BLOCKS); run 3 on an output-control count (' own"' 12, not 11 — the by-name keyword "deterministic, develop's own"); run 4 written.

## NOT DONE (by instruction)
No launch (`repin_and_launch.sh` not run; `cockpit.sh add` not called), no mail, no pane tap, no board / queue / PAUSE_QUEUE / done.md / READY-file
write, no `inbox_routing.conf` edit (the line to add is in the README), no write into the Secuura checkout, no key printed, no port connected.
