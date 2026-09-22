# DRAFTER REPORT — batch gate over Seat B 18th's SEVEN PRs (#1170 #1172 #1174 #1176 #1177 #1178 #1179; TIER 1 on #1174 / #1177 / #1178, TIER 2 on the rest; round 1 of 2)

Drafter: gate-drafter subagent under Wednesday (the 11:0x seat of 2026-09-22; session 003907dd). Started 2026-09-22T01:14:14Z (UTC, `date -u`; 11:14 AEST);
the commission read whole; the three commissions it names (gate18C, gate16B, gate16C) read whole; the gate16B gateset (README / DRAFTER_REPORT / round16B /
fill / gen / repin / capture / shape / predict / gh / linear / controls) and its prompt (the three DRAFT parts) read whole; the gate18C dead drafter's
round18C.py / capture / shape / predict read as the 18th-round shape; the sibling dir NOT written into.
Status: COMPLETE — seven of seven READYs captured before the drafter began (00:02:34Z … 01:05:17Z; captures 01:15:52Z); every number below names its instrument.

## 4. Drafter's own slips (recorded as they happen; FIRST in the final message)
S1 01:22Z — `shape_gate18B.py`'s docstring carried `\d` in a non-raw string (a SyntaxWarning at run 1, `shape_1.out` line 2); made a raw docstring with
   `shape_gate18B.py.pre-1123-rawdoc` (backup names carry LOCAL HHMM per the `$(date +%H%M)` rule; the timeline is UTC) beside; every value in `shape_1.out` is from that run (the warning is cosmetic — the regex in code was raw).
S2 01:2xZ — `shape_gate18B.py` prints "diff vs develop same set: False" per PR: the check compares `git diff --name-only 8c2f7b3fd <head>` (a TREE diff, which
   includes the 50 #1036 paths the head lacks) against the parent-based set — a wrongly-framed check, NOT a finding; the right reading is the 3-way
   MERGED tree (predict (c)), where every merged tree carries its own paths at the head blobs and the 50 moved paths at develop's blobs (7/7). Left in
   the .out as written; named here so nobody reads that False as a disagreement.
S3 01:4xZ — `gen_launcher_gate18B.py` run 1 refused on its own MOVED-manifest list: the Dev root `package.json` did NOT move under #1036 (only the root
   LOCK did; `shape_1.out`) — the list was corrected to the 8 manifests that did (`gen_launcher_gate18B.py.pre-1150-movedlist` beside). Run 1 also dropped a wrong
   unchanged-read path (`originate/src/services/documentRepo.ts` — the file lives under `src/repositories/`; corrected). No launcher was written by run 1.
S4 01:47Z — run 2 refused on a BOTH-list token `whole line` (the prompt says `whole-line`, as the READYs do) — token corrected. Run 3 refused on THREE
   wrapped by-name phrases (`THE LINE-NUMBER DISCIPLINE`, `NAME WHO INHERITED IT`, `re-run standalone 3× serial` broke across lines in part3) — the
   gate16B drafter's S3 repeated; unwrapped (`prompt_gate18B.DRAFT.part3.txt.pre-1151-wrapped` beside), re-filled (`fill_prompt_2.out`: 1027 lines,
   145463 B). Run 4 refused on the output-control WANTS for `exit 10` (6 mentions in this launcher's header, not 5) and `exit 19` (4, not 3) — the
   drafter's miscount, caught by the generator's own controls before any file was written; run 5 wrote.
S5 01:54Z — `launcher_controls_gate18B.sh` control U (the END_TREE zeroed everywhere in a prompt COPY) was written with `want=30`; the launcher's exit-30
   BOTH loop does not carry the END_TREE (only the parent-based tree's 12-hex), so the refusal lands at exit 31 (the full-sha grep) — the CONTROL's
   expected code is the drafter's typo; the launcher refusing at 31 on a zeroed END_TREE is the intended behaviour. The controls script was already
   running when this was seen (a running bash script is not edited); U reads `MISMATCH rc=31 want=30` in `launcher_check_controls.out` — read it as OK
   at 31. Recorded here rather than re-run (nothing else in the ladder depends on it).
S6 (a design note) — the prompt carries the literal placeholder `__M<k>__` in prose ("the merged tree __M<k>__") for "the k-th PR's merged tree"; the fill's
   residual-token check does not match it (the `<k>`), and it is read as prose. Five occurrences; harmless, named.

## 0. Constraints honoured
- No `cd`; literal absolute paths; `git -C`; heredocs `<<'EOF'`; rc on its own line; nothing deleted or renamed (`.pre-HHMM-*` copies beside).
- Secuura checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` READ-ONLY (read verbs only: `ls-remote`, `show`, `cat-file`, `rev-parse`,
  `rev-list`, `diff`, `ls-tree`, `log`, `status`, `for-each-ref`, `count-objects`, `config --get`). Every write verb (apply, read-tree, write-tree,
  merge-tree, commit-tree) inside ONE `git clone --shared --no-checkout` scratch clone under this session's scratchpad
  (`scratchpad/predict18B.ac4jedrc/clone`), from the script file `predict_batch_scratch_gate18B.py`, which CHDIRS INTO THE CLONE FIRST and asserts
  `{'cwd_is_clone': True, 'clone_under_scratchpad': True, 'gitdir_is_clone': True, 'gitdir_not_checkout': True, 'objdir_under_scratch': True}` before
  any write verb (rc 2 otherwise; every git call also `-C <clone>`; `GIT_OBJECT_DIRECTORY` under the scratchpad asserted per call). `count-objects -v`
  on the checkout byte-identical before/after (count 9416 / in-pack 101422 / packs 47 — `checkout_counts_predict_before.txt` / `_after.txt`;
  `predict_batch_scratch_1.out`: "byte-identical to before: True"; 211 objects written into the temp objdir, 1 into the clone's own objects dir).
- Network: `git ls-remote` ×4 (01:14:19Z lsremote_1.out; 01:25:23Z predict (d); 01:44:44Z fill; 01:4xZ gen) + the launcher's own under `--check` and
  the controls; GitHub / AgentMail / Linear READ APIs. No `git fetch` (develop unmoved off the pin at every read). No launch, no mail, no pane tap,
  no Linear write, no `inbox_routing.conf` write, no write under `!CODING/`, nothing written into `2026-09-22_gate18C_seatC/`. Datasec mail unread
  (the inbox listing filters Seat B / Seat C / QA subjects only; the capture filters on from-address AND subject prefix). No port connected by hand.
  No `deadbeef` literal in the prompt (fill + generator refuse one; `grep -c -i deadbeef <prompt>` = 0). No secret in any file (keys read by NAME).

## 1. Timeline (every value: instrument | file)
- 01:14:14Z `checkout_counts_before.txt`: porcelain non-untracked 0; porcelain total 17; `.git/worktrees` 272; for-each-ref 1223; count-objects 9416 /
  in-pack 101422 / packs 47; .git/config sha256 6417b203accd…; HEAD `develop` 581ed7fa1 | `git -C <checkout> status --porcelain | grep -v '^??' | wc -l`;
  `ls .git/worktrees | wc -l`; `for-each-ref | wc -l`; `count-objects -v`; `shasum -a 256 .git/config`; `rev-parse --abbrev-ref HEAD`.
- 01:14:19Z `lsremote_1.out` (`git ls-remote origin refs/heads/develop refs/pull/{1167..1179 as listed}/head 'refs/heads/feature/ks-<7 keys>-*'`, rc 0):
  develop `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`; the seven heads == the commission's seven (3e9f7d7b7 d74b04678 e1dea649c 8ced0d50b 13030ac59
  e48b90e74 e62555dd0) at BOTH refs/pull/N/head and their branches; Seat C's six as in round18C; the ks-1171 glob returns ONLY the R16 TSFIX branch
  (the 16th's HELD R15 pair NOT at origin); the R15 branches of KS-1118 / KS-1158 / KS-1181 / KS-1188 still exist (merged, the 16th's).
- 01:15Z `inbox_list_gate18B.py` (`inbox_list_1.out`): 200 messages listed (125 matched the round filter); the seven Seat B 18th READYs 00:02:34Z …
  01:05:17Z, the 23:47:45Z STATUS, the 01:08:36Z HOLD (message id == the commission's), the 22:50:35Z plan QUESTION, the 23:29:09Z baselines QUESTION,
  Wednesday's brief 22:27:53Z + ANSWERs 22:52:30Z / 23:30:26Z; Seat C 18th's six READYs 23:37Z … 00:32Z + its three STATUS + two QUESTIONs.
- 01:15:52Z `capture_ready_mail_gate18B.py` run 1 (`capture_ready_mail_1.out`): 29 mails captured VERBATIM by message id (TEXT_SHA256 per file): Seat B's
  7 READYs (11086 / 11211 / 14351 / 15678 / 15311 / 14606 / 13170 chars), 2 STATUS (7171; 6068 — the HOLD, TEXT_SHA256 9f5be41efd1d…), 2 QUESTION (29626;
  4697); Wednesday's brief (106560) + 2 ANSWERs to B; Seat C's 6 READYs + 3 STATUS + 2 QUESTION; Wednesday's brief + 3 mails to C (incl. `GO: merge
  #1036` 22:46:56Z). Combined `mail_gate18B_ready.md` 151623 B (sha256 50ca07b0dd7d…). `grep -c written capture_ready_mail_1.out` = 29.
- 01:18:21Z `local_reads_1.out` (rev-list --parents / rev-parse ^{tree} / log -1 / diff --raw --abbrev=40 / diff --numstat per head; rev-parse of the tamper
  files at both tips; cat-file -e on the octopus): parents 3916eacd1 ×7; trees == the READYs 7/7; subjects == titles 7/7; author kamil.kreiser@secuura.ai ×7;
  the 40-hex blobs (carried into round18B.py); the 4 tamper files identical at 3916eacd1 and 8c2f7b3fd (4/4); develop's parent [3916eacd1],
  first-parent count 1; the octopus 5185c65cf in the store with tree a36532029483 (8 parents).
- 01:20Z `round18B.py` written — the ONE pin source (every script imports it).
- 01:22:42Z `shape_gate18B.py` (`shape_1.out`, rc 0): the parent tree 4b573853be61 == pin; develop tree 04b05e093ad8 == pin, parents [3916eacd1],
  `rev-list --count --first-parent 3916eacd1..8c2f7b3fd` = 1 (= all); THE MOVE: `git diff --name-only 3916eacd1 8c2f7b3fd` = 50 files (20 package.json +
  29 package-lock.json + scripts/audit/audit-baseline.json; shortstat `50 files changed, 552 insertions(+), 951 deletions(-)`), ∩ the 9 PR paths NONE,
  ∩ the 4 tamper files NONE, NOTHING under any lane's src/, the lane manifests that moved: Dev root package-lock.json, packages/shared/package.json,
  services/anchoring/package-lock.json, services/auth/package-lock.json, services/auth/package.json, services/originate/package-lock.json (+ shared's
  lock — p1036_paths.out); the 8 apply units EXIST, sha16 == the READYs 8/8, hunk headers / `+`/`-` / `+++` == the pins 8/8, declared-vs-actual new
  count consistent on all four NEW-file rows (no truncation), `.opts` empty on both sections; KS-1265 whole patch.diff sha16 d955f73e1c5d70c3 ==
  cat(section_1, section_2) True, decl / tdz variants byte-identical to section_2; the READY fences == the run patches 8/8; input.json tips
  19f1e5475 / 75ad0e55c ×2 / 64ab10513 ×4 / 3916eacd1 == the READYs 8/8; checker RESULTs PASS 9/9 ×3 / 8/8 ×4 / 7/7; KS-1265 red_first 1 failed / 4
  run (the E-01 title == pin), green_after 0 / 4; the tamper verdicts red == declared 6/6; the 9 targets: 5 at their blobs / lines at the parent, develop
  AND 64ab10513, 4 ABSENT at all three; the 4 tamper blobs == item 0 at all three tips; the `from` counts: 8J whole-line 1 at [260] / substring 2 (want
  1 / 2), SPECRENAME 1 / 1, ROUTECOLLAPSE 1 / 1, F1C 1 / 3 (the first from-line `const user = await userRepo.getUserById(userId);` occurs 3× as a
  substring in mfa.ts — the 2-line block is unique; the seat's "substring 1" counted the block), F1D 1 / 1; scope anchors present at :255 / :1077 /
  :161 / :391; per head 7/7: parent == PARENT, PARENT...head 0/1, develop...head 1/1, merge-base(develop, head) == PARENT, tree / files / +/- / modes
  100644 / name-status == pins, product paths [] ×6 and [documents.ts] on #1174, nothing under services/auth that is not a test; the comment-only
  proof 9 / 2 / 2 changed lines, 0 violations ×3, the `+const x = 1;` control 1; the product hunk `@@ -613,0 +614,8 @@ documentsRouter.post(` +8/-0
  with the 8 lines quoted; union paths 9, overlaps NONE, name-status 4 A + 5 M, product paths [documents.ts]; ∩ Seat C's 10 paths / dirs / tamper
  files NONE; lanes {anchoring, auth, originate, shared}; the 7 branch names ASCII (79 / 85 / 92 / 102 / 86 / 84 / 74), scanner == [own] 7/7, the
  ks-1257 control reads [ks-1257, ks-1]; excised tokens absent 2/2; `815s` in KS-811's; lane scripts jest / vitest run / vitest / vitest run; the
  auth + shared package.json DIFFER at develop (the #1036 move); hook :76 as the 15th's F8, same blob at develop; 33 `*.test.sh` under
  Dev/scripts/__tests__ (45 tracked repo-wide — `git ls-tree -r --name-only 3916eacd1 | grep -c '\.test\.sh$'` = 45 = the seat's corpus); the ks795
  cover cell at :509 by exact title; ks727 :243 `const HANDLERS = await discover();` (the F7 TS1378 site); the F3w changed line :34 `The 10th handler
  is` -> `The surplus handler is`; the octopus tree == a365… with 8 parents.
- 01:25:03Z `predict_batch_scratch_gate18B.py` (`predict_batch_scratch_1.out`, rc 0; clone `predict18B.ac4jedrc`; CWD GUARD all True): (a) the 8 units
  into temp indexes read from 3916eacd1: strict `--check` rc 0 ×8, `-R --check` rc 1 ×8, `--recount --check` rc 0 ×8; STRICT APPLY -> the head blob +
  line count 8/8; `--recount` APPLY -> the same blob 8/8 (a no-op); nonexistent patch rc 128; per-PR trees == head trees 7/7 (#1174 and #1176 reverse
  order same); the all-7 (8 units) in forward / reverse / seed-18 shuffle -> `a36532029483c3f8a4ca0cd33ec1219076ef9219` ×3 == the seat's; shortstat `9
  files changed, 513 insertions(+), 11 deletions(-)`; name-status 4 A + 5 M; every path in ALL7 == its head blob 9/9; read-tree back -> 4b573853be61.
  (b) the seven heads by REAL `merge-tree --write-tree` over 3916eacd1 both orders == their head trees (fast-forward 7/7; == the canonical-apply trees
  7/7); chained in FOUR orders (1234567, 7654321, 7563412, 1352764) -> `a36532029483…` ×4; every PR path at its head blob; each head tree != ALL; the
  octopus 5185c65cf's tree == ALL, 8 parents. **(c) THE #1036 MOVE 3916eacd1 -> 8c2f7b3fd: 50 paths (p1036_paths.out) | ∩ the 9 PR paths: NONE (∅) |
  ∩ the 4 tamper files: NONE (∅) | ∩ the lane manifests: the 8 named; each head MERGED over 8c2f7b3fd (3-way, base 3916eacd1) both orders one sha,
  != its head tree, its own paths at the head blobs and the 50 moved paths at develop's blobs (7/7): #1170 1424bf3f00ded4b4f7114136996044a63ed35c30 ·
  #1172 de5a08d7792d22ed94a52c4c7d96d8ca46e8eb03 · #1174 774e927ae7a38f35192e8d147429d7015fa70046 · #1176 c746486f45219ef1c8792748ca11ddc87abf3780 ·
  #1177 275b722c53341fbf2280b7a1a5cc3c727c1fc1dd · #1178 fd0ab1e4fe2a77f431fd6919741bfb1cc8849303 · #1179 6f63daf6210227222312daa8ce20c32e8b320d1e;
  all seven chained over 8c2f7b3fd in FOUR orders -> ONE sha = THE END_TREE `76a88d9ddfa4f50098aa639a1056c5c9387aeb18`; the 8 canonicals applied
  over 8c2f7b3fd in THREE orders -> the same sha; END_TREE != ALL_OVER_PARENT; `diff-tree -r --name-only a365… 76a8…` = 50 paths == the moved set;
  END_TREE's 9 PR paths at the head blobs and 50 moved paths at develop's blobs; shortstat vs develop `9 files changed, 513 insertions(+), 11
  deletions(-)`, vs the parent `59 files changed, 1065 insertions(+), 962 deletions(-)`; a numstat of it in the shared store rc 128.** (d) origin
  develop at 01:25:23Z still 8c2f7b3fd — no fetch; `newdev_tree.txt` written (DEV_NOW / TREE / ALL7_OVER_NEW / ALL7_OVER_PARENT / ALL7_OVER_8c2f7b3fd /
  PR1..7). Empty-repo numstat rc 128. count-objects byte-identical; porcelain non-untracked 0; worktrees 272; for-each-ref 1223.
- 01:26:43Z `gh_pr_reads_gate18B.py` (`gh_pr_reads_1.out`, rc 0): 31 open PRs; per PR (7/7): head == READY == round18B, base develop@8c2f7b3fd (== DEV;
  != PARENT — the PRs opened after #1036 landed), open, mergeable True / `unstable`, 1 commit, author kksecura, created 00:00:24Z / 00:12:03Z /
  00:25:15Z / 00:37:59Z / 00:46:47Z / 00:54:27Z / 01:02:04Z; closing 0/0/0 ×7; completeness 0/0/0 ×7; body Refs exactly the own key ×7; commit Refs
  the same; titles == round18B ×7, ASCII; commit subject == title ×7 (87 / 77 / 82 / 89 / 88 / 88 / 82 chars); branches == round18B, ASCII, scanner ==
  [own] ×7; files API == the pins ×7, `outside __tests__: []` ×6 and `['documents.ts']` on #1174 == the declared product set, additions / deletions
  per file == the pins ×7; archived / content / foreign keys in title / branch / subject NONE ×7; the archived file-name tokens ks1103 / ks1058 /
  ks549 / ks727 as PATHS on #1170 / #1172 / #1174 / #1179; body keys = own + KS-1201 + KS-256 ×7 (the standing mentions), sibling own keys in body
  NONE ×7 (S4 confirmed); every body carries INCOMPLETE / 12/15 / SKIPPED / skips are not a pass / strict / cover / lock / started_utc / released /
  PROTOCOL-CLEAN / stubs=4 / typecheck / TS2322 / netlog / :5432 / threadTokenMint / bare / preload; #1174's A4 ×9 / A5 ×7; #1177's ks795 ×5;
  compare develop...head merge_base 3916eacd1 (== PARENT) / ahead 1 / behind 1 / files 1-1-2-2-1-1-1 ×7; files API union 9 with [documents.ts] the
  only product path. Ruleset 18499832 `require-pr-gates` active, updated_at 2026-09-10, rules deletion / non_fast_forward / pull_request (0 approvals,
  require_extra_approval_for_unattributed_changes True), conditions develop + main. #1036: closed, merged 2026-09-21T22:54:32Z, merge_commit_sha ==
  DEV, head == 4b251997a, files API 50 paths ∩ ours NONE, non-manifest [audit-baseline.json]. Seat C's six: head == READY ×6, base develop@8c2f7b3fd,
  kksecura, created 23:34:26Z … 00:31:03Z, namespace `feature/ks-<key>-…-r16-…-1` True ×6, scanner == [own] ×6 (the ruled `-settingsdefaults-1` tail
  on #1175), files == the READY paths ×6, ∩ ours NONE ×6; 10 distinct paths all under api-gateway; ours ∪ tamper files under api-gateway NONE. Open
  PRs touching the 9 paths or 4 tamper files: 0; controls #1163 / #1159 / #1146 ∩ ours -> [] each (negatives by construction — a POSITIVE control
  on a tamper file is left to the gate, see NOT MEASURED). PR-number traps: #811 closed (a docs PR), #1118 closed (KS-1006 + KS-1236), #1158 closed
  (KS-855), #1171 OPEN = Seat C's KS-1231, #815 closed (KS-795), #1181 / #1188 / #1265 / #1180 404. The window #1167..#1179 all open as pinned.
- 01:28:46Z `linear_reads_gate18B.py` (`linear_reads_1.out`; the file asserts no `mutation`): the 7 own tickets In Progress on the board login,
  archivedAt None; attachments exactly the own PR (+ #1149 on KS-1118, #1153 on KS-1158, #1163 on KS-1188, #1159 on KS-1181 — merged, the 16th's);
  comments 0 / 0 / 0 / 0 / 1 / 0 / 0; the linear[bot] (actor GitHub) walks: KS-1265 2026-09-22T00:25:25.901Z, KS-1171 00:38:08.411Z, KS-811
  00:46:56.839Z (this round); KS-1118 2026-09-21T17:11:05Z, KS-1158 17:38:32Z, KS-1188 18:43:43Z, KS-1181 18:16:40Z (the 16th's); attachmentsForURL
  pull/N == [(own key, contributes)] 7/7; the Linear branchName fields: KS-1188's `feature/ks-1188-1013-gate-findings-ks-999-the-getuserbyid-route-level-503`
  (scanner [ks-1188, ks-999]) and KS-1181's `feature/ks-1181-ks-727-error-handler-guard-corpus-1-canary-cells-cannot` (scanner [ks-1181, ks-727]) —
  the two excisions CONFIRMED against their source; the other five scan clean; hyphenless file-name tokens NONE. Seat C's six keys: In Progress,
  +#1167 / +#1168 (+#1002) / +#1169 / +#1171 / +#1173 / +#1175, each bot-walked on open (23:34:36Z … 00:31:13Z); attachmentsForURL for its six ==
  its own key each. Namespace KS-1167 … KS-1181: KS-1167 / KS-1169 / KS-1170 Done ARCHIVED (#992 / #993 / #997); KS-1168 / KS-1174 / KS-1177 /
  KS-1178 Backlog; KS-1171 = PR 4's OWN (#1176); KS-1172 / KS-1173 In Review (#877, #1059); KS-1175 In Progress (#1116, #1105); KS-1176 In
  Progress (#1014); KS-1179 In Progress (#1157 — Seat B 16th's); KS-1180 In Progress (#1150, #1029); KS-1181 = PR 7's OWN (#1179 + #1159).
  Archived 30/30 with archivedAt set (KS-727 2026-09-05; KS-549 2026-08-04; KS-733 / KS-815 / KS-1013 / KS-1058 / KS-1103 as the READYs list);
  KS-795 Deployed to UAT, ARCHIVED 2026-09-06 (the ROUTECOLLAPSE cover cell's key — CONTENT; #815 its PR); KS-999 In Progress (#1013); the 19 content
  keys as the READYs list them; KS-1227 Backlog 0 attachments (DEFERRED); KS-256 In Progress 44 comments / KS-1201 Backlog 1 (no new attachment);
  KS-485 Todo 65 comments / KS-772 Todo 28 (the 17th's rule-7 posts landed); KS-1004 Done archived. Controls: pull/1036 -> {KS-763, KS-775};
  pull/1149 -> {KS-1118}; pull/1153 -> {KS-1158}; pull/1159 -> {KS-1181}; pull/1163 -> {KS-1188}; pull/1129 -> []; pull/1180 -> [].
- 01:44:41Z `fill_prompt_gate18B.py` run 1 (`fill_prompt_1.out`): origin re-read IN THE SAME ACTION (ls-remote 01:44:44Z, 15 refs) — origin / round18B
  / the READYs AGREE on develop and all seven heads; newdev_tree.txt for THIS develop; 41 tokens substituted (the seven PR numbers ×25 / 20 / 44 / 34 /
  28 / 32 / 29, the seven heads ×2 each, the seven READY instants, the seven merged trees ×2 / 2 / 4 / 2 / 2 / 2 / 2, the parent ×64, its tree ×3,
  develop ×64, its tree ×2, the parent-based all-7 ×9, the END_TREE ×14); the prompt written: 1026 lines, 145459 B. Run 2 after S4: **1027 lines,
  145463 B, sha256 8852dcef53ab095b4a26ea5d01bd1fe8d0bb2b10c35429d79efd957d90c27878** (`fill_prompt_2.out`); report dir `2026-09-22-batch1170-1179-r1`;
  subject prefix `[QA -> Wednesday] BATCH GATE #1170-#1179 (seven PRs; tier 1 = #1174, #1177, #1178: Seat B 18th, one product change) —`; the GO
  string present; END_TREE and BASE_GO named in full.
- 01:45-01:50Z `gen_launcher_gate18B.py` runs 1-5 (`gen_launcher.runN.out`; S3 / S4): pins re-read at origin (develop == the pin 8c2f7b3fd; 7 pull heads
  + 7 branches OK; the ks-1171 glob = the TSFIX branch only), `rev-list --count parent..develop` 1, merge-base == parent, the move 50 paths ∩ targets /
  tampers NONE; per head parent == 3916eacd1, parent...head 0/1, develop...head 1/1, tree == pin, files == the pins, +/- == the READYs, modes 100644,
  status M / M / MM / AA / A / A / M, product paths [] ×6 + [documents.ts], tier 2 / 2 / 1 / 2 / 1 / 1 / 2; union paths 9, overlaps none; the 9
  (develop blob | ABSENT) values agree at the parent AND the current develop; 28 unchanged-read paths same blob at the parent, develop and every
  head; 8 MOVED manifests differ parent -> develop and every head carries the PARENT blob; tree-hash control -> the parent tree; compose over the
  parent == each head tree 7/7; compose(the 9 into the parent tree) = `a36532029483…`; compose(the 9 into the CURRENT develop tree) = `76a88d9ddfa4…`
  == the END_TREE (the THIRD independent derivation: pure tree hashing, after real merges and real applies) and != the parent-based tree; per-PR trees
  over develop == predict 7/7; the newest predict .out carries all five markers incl. the CWD GUARD line; BOTH 174 tokens present in BOTH the capture
  and the prompt; by-name 122 keywords across 12 items + the closing; output controls matched (run 5); heredoc parity PY 0 / 10-10, PYJ 0 / 107-107;
  `bash -n` rc 0 -> **`launch_qa_secuura_batch1170-1179.sh` 530 lines, mode 755, sha256 508d1e3bfa519238e060be8255941a456a32aa975ddf87f046942b7b7d7d8a56**
  (`gen_launcher.run5.out`).
- 01:52:17Z-01:53:59Z `launcher_check_1.out`: **`--check` rc 0** — seven heads on origin; compares merge_base 3916eacd1 / ahead 1 / behind 1 / files
  1-1-2-2-1-1-1 ×7; develop judged by content over 46 paths = the pin; every grep passed.
- 01:54:43Z `launcher_controls_gate18B.sh` started in the background (`launcher_check_controls.out`): A rc 4, B rc 3, C (wrong sha on #1179) rc 6, D
  (curdev = the parent 3916eacd1) rc 18, E (curdev = #1170's head) rc 19 LANDED, F (a launcher copy expecting behind=2 on #1172) rc 10, … — see the
  addendum at the end of this file for the "controls end" line.
- 01:5xZ `repin_and_launch_gate18B.sh` written (reads its pins FROM the launcher; `bash -n` rc 0; the sed pin-parse dry-read prints develop 8c2f7b3fd,
  END_TREE 76a88d9ddfa4 and the seven PRs; NOT run). Routing line `QA/Secuura-batch1170|coagent@agentmail.to|yes` count 0 (absent, as commissioned —
  Wednesday adds it); the batch1147 control 1. `grep -c -i deadbeef <prompt>` = 0.

## 2. Artefacts produced
- **Prompt** — three draft parts `prompt_gate18B.DRAFT.part1..3.txt` assembled by `fill_prompt_gate18B.py` (first line `ultrathink`): framing (SEVEN PRs, FOUR
  lanes, ONE product change, TIER 1 ×3, the #1036 move as the round's shape with the moved manifests, the END_TREE and BASE_GO the GO must carry); the
  LEADS (F1-F9, S1-S6, the bot walks, the (b) ruling, the ks795 cover with KS-795 archived, the PR-number traps, the MFASIBLINGSITES CLOSED lead); the
  NAMESPACE NOTE (the interleaved Seat C numbers; KS-1171 vs #1171; KS-1181 vs #1181; the READY files not in this gate; the archived keys inside file
  names); the per-PR table (seven entries: canonical + sha16 + hunk + tip + checker verdict, the tree over the parent AND the merged tree over develop,
  the cells, the tampers with their scope anchors and declared reds and cover, the lane counts with the (b) ruling's BOTH numbers, tsc / typecheck18 /
  eslint, the census, the lock window, the ticket state, the tier, the Refs); TIER PER PR (seven lines `#N KS-x: TIER n`), round 1 of 2, time-box 180
  min, the budget order, THE CONTEXT RULE; MERGE AUTHORITY (go18.sh / targets18.py 7 keys 9 targets 1/1/2/2/1/1/1 / MG-2 EXERCISED / MG-3 / dry18.sh
  END_TREE REQUIRED / merge18.py / merge_series18.sh / postmerge18.py / the lock / `--pair-blob` not exercised / the tickets stay / the three bot
  walks / the merge order); THE SHAPE (the parent, develop = the parent + #1036, the 50-path move and the moved manifests, the compare behind 1, the
  heads and branches with the scanner, the per-PR trees over BOTH bases, the two batch trees and their 50-path difference, Seat C's ten paths, the
  strict canonical identity, the run tips, the five tampers, the open-PR sweep); the sources (the READYs by filename, the STATUS / HOLD / QUESTION
  mails, Wednesday's ANSWERs, Seat C's mails as context, the brief, the seat's record folder by file incl. the two quarantines and the proof-targets18,
  the eight READY files + run dirs, PRIOR = batch1147-1161-r1 / EARLIER = batch1148-1166-r1 / OLDER = the #1036 gate, the Linear keys incl. KS-795, the
  handover, Seat C's record for by-name 3 / 9, the charter); worktree / history / checkout / push-lock rules (s-b18-*, s-c18-*, the lock directory
  read-only); farming per ENTRY with the MOVED LOCKS caveat (install from each tree's own lock; print the express / body-parser / qs versions);
  Postgres isolation + CENSUS RULE v2 + the (b) ruling on the gate's own reads; listeners incl. the process-namespace rule; NOT-TESTED items (the seven
  preflight pushes 12/15 + 45 of 45 inside the lock; the #1036 move; the code_patch protocol; the cover; mergeable_state; the two-seat artefacts; the
  intermittents incl. the preload timing artefact by name); TWELVE by-name items exactly as commissioned; per-PR requirements; suites at develop bare /
  each head / each merged tree / the END_TREE; CARRY-FORWARD incl. the CLOSED candidates; hygiene; the report dir; the NOT-PINNED candidate rows
  (ROUTECOLLAPSECOVEREDBYKS795, MFASIBLINGSITES-166/-397, HEADERWORDINGONLY, GUARDBEFORESAVEORDER, PRELOADTIMINGARTEFACT, MANIFESTSMOVEDUNDER1036);
  the SEVEN-line verdict + the BASE_GO / END_TREE line; the MERGE ADDENDUM line format with the nine head blobs and modes; WRITE report.md BEFORE
  THE MAIL; the exact subject; the GO string the seat expects.
- **Launcher** — generated by `gen_launcher_gate18B.py` (above). Pins: develop 8c2f7b3fd + every head by branch AND refs/pull/N/head (exit 6); compare per
  PR merge_base 3916eacd1 / ahead 1 / behind 1 / files per PR (exit 10); develop judged by CONTENT over 46 paths (9 targets — 4 ABSENT-judged with
  LANDED detection, 5 by blob; 28 unchanged-read; 8 MOVED manifests at develop's blobs); GUARDED list for a further move (shared / originate / security
  / anchoring / auth src + config + locks, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs; api-gateway NOT guarded); the grep
  ladder 7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33 + 34; overrides `QAB1170_*` refuse at launch (16); TTY (21); pane `QA/Secuura-batch1170`.
- `repin_and_launch_gate18B.sh` (pins read FROM the launcher; the ks-1171 glob asserted == 1; NOT run), `launcher_controls_gate18B.sh` (running at this
  write), `README.md` (section 0 the #1036 shape + the move recipe; section 8 the finish-from-disk recipe), this report, `round18B.py`, the capture /
  list / shape / predict / gh / linear scripts and their outputs (section 1).

## 3. LEADS for the gate (claims to grade; the drafter's re-derivation disagrees with the seat's VALUES nowhere)
1. THE MANIFESTS MOVED UNDER #1036 — the seat's claim "∩ my 9 targets + 4 tamper files = NONE" is TRUE and the drafter measured what it omits: 8 lane /
   root manifests (packages/shared package.json + lock, services/auth package.json + lock, anchoring / originate locks, the Dev root lock,
   audit-baseline.json) moved; every seat baseline and batch suite ran on trees installed from the OLD locks. The gate's bare lanes at 8c2f7b3fd are a
   NEW baseline; the per-PR addendum tree is a MERGED tree, not the head tree; the END_TREE is `76a88d9ddfa4…`.
2. #1178 CLOSES the EARLIER REPORT's NOT-PINNED rows MFASIBLINGSITES-166 / -397 (KS-1188, #1163): the proposed cells `RED KS-1188 F1c - POST
   /api/auth/mfa/setup/start answers 503 SERVICE_UNAVAILABLE …` / `F1d - … backup-codes/regenerate …` are exactly the two cells this PR's file carries,
   red under the seat's F1C / F1D plants at mfa.ts:166 / :396 (the EARLIER row said :397 — the second line of the seat's 2-line block). The first
   CLOSED rows a local-model round produces; nothing in the mails names it.
3. The ks795 COVER on KS-811's ROUTECOLLAPSE — the seat measured ONE existing cell red at develop ("the throw was witnessed, the published-vs-thrown SET
   was not"; its S6 corrected title); KS-795 is ARCHIVED (Deployed to UAT 2026-09-06) — content in a file name; the NOT-PINNED-for-its-own-file question
   in the PRIOR REPORT's R3COVEREDBYKS1004 shape.
4. F7 — the ks727 file's TS1378 at :243 (`const HANDLERS = await discover();`) pre-exists at the parent; the drafter read the line, not the compiler.
5. The seat's measure18.py has NO cwd guard (the successor-19 COUNTS flag): its records say count-objects 9214 -> 9214 across both item-0 runs and the
   loose #1036 objects it met were Seat C 18th's S1 (Wednesday's Q12 attribution) — the gate reads boot/measure18.py and rules whether a write verb
   COULD have run in the checkout; the drafter's own predictor asserts its cwd (section 0).
6. The namespace: KS-1171 (PR 4's own) vs #1171 (Seat C's KS-1231, OPEN); KS-1181 (PR 7's own) vs #1181 (404); KS-1179 (Seat B 16th's #1157) vs #1179
   (PR 7); KS-1170 / KS-1167 / KS-1169 Done ARCHIVED tickets.
7. The Linear branchName fields STILL carry `ks-999` (KS-1188) and `ks-727` (KS-1181) — the excisions are in the pushed names only (by design: findings
   on Linear's branchName, not on the PRs).
8. The 8J anchor ambiguity reproduced: substring 2 / whole-line 1 at :260 (the :401 occurrence deeper-indented). F1C's first `from` line occurs 3× as a
   substring in mfa.ts; the 2-line block is unique — the seat's "substring 1" counted the block (its instrument's contract; not a fault).
9. The two F9 quarantines (ks1171 run 1: db.retry 8.9 s; ks1188 run 1: ks949 5000-5133 ms) and the S3 removed 2-byte rc file — the record's wholeness.
10. The loose-object count 9064 (the 16th's drafter) -> 9416 (now): the seats' boot fetches, Seat C 18th's 17 S1 objects, the s-b18-* / s-c18-*
    worktree commits — for the gate's count-objects reading.
11. #1172's comment re-points a citation to documentRepo.ts:540-544 — the drafter did not read documentRepo.ts; the gate reads it.
12. The compare API reads every PR's base as develop@8c2f7b3fd (the PRs opened after #1036 landed) while every commit's parent is 3916eacd1 — the
    "behind 1" the launcher pins; Seat C's six merges would make it 7 and the launcher refuses at exit 10 by design (re-pin: README section 0).

## 5. NOT MEASURED by the drafter (named, not asserted)
- Any suite, tsc, eslint, typecheck18 or census run — the drafter ran no test (originate 835/835, anchoring 328/329 -> 334/335, auth 818 -> 824 / 822 ->
  828 bare, shared 917/917, the cells 14 / 6 / 4 / 3+3 / 6 / 4 / 103, the A4 1/4 -> A5 4/4, the red sets, tsc 0 ×4, eslint 0/0 ×9, typecheck delta 0 ×8
  incl. ks727's 1/1, TS2322 CAUGHT ×8, the census attempts / established / REPORT sets) are carried as the seat's claims; the lanes at 8c2f7b3fd
  (the moved locks) have NO baseline yet — the gate's first measurement.
- The tamper plants themselves — the drafter did not plant any tamper (the `from` texts were located in the parent's bytes and counted; not mutated).
- The ks795 cover cell's ASSERTION (only its title and line were read); the two MFASIBLINGSITES rows' closure (only the titles matched); the F3 pin's
  reading of the ks727 header (#1159's file not read).
- documentRepo.ts:540-544 (the R5b citation) not read.
- The live PR bodies' full text beyond the detectors / substrings (bodies never printed); the seat's raise/ records (raise18.py, series18.py, lock18.sh,
  measure18.py, typecheck_pre18.py, the push logs, the stubs files, the quarantines, proof-targets18/) — named in the prompt, `ls`'d, not read.
- The seat's HANDOVER and RECORD.md — not read (their names are from the commission); Seat C's record folder — not read.
- The Seat C READYs' contents beyond their subject / head / path lines (their bodies not read; Seat C's own findings are its gate's).
- A POSITIVE control for the open-PR sweep (a merged PR that touched one of the 4 tamper files) — the three controls run are negatives by construction;
  the prompt asks the gate to find one.
- Whether the combined capture's TEXT_SHA256 per mail matches what a re-fetch returns (the gate re-fetches by message id).
- The DKIM / inbox discriminator on the GO (the drafter sends no mail).

## 6. Checkout counts AFTER (read verbs only throughout) — `checkout_counts_after.txt` (written at the drafter's close; section 8).

## 7. The launcher's controls — RUNNING at this write (`launcher_controls_gate18B.sh` -> `launcher_check_controls.out`; ~35 min; A-F OK at 01:57Z). Control T
   (the #1179 addendum blob replaced by zeros) is designed to PASS (rc 0): the launcher greps heads and 12-hex tokens, not the addendum's 40-hex blobs — the
   gate reads blobs itself. Control U (the END_TREE zeroed) refuses at exit 31 (the drafter's S5: the control's expected code was typed 30).

## 8. Final state — see the addendum at the end of this file (written at the close).

## 8. Final state (addendum, 2026-09-22T02:19:18Z / 12:19 AEST)
- **Controls: `launcher_check_controls.out` — first run `controls end 2026-09-22T02:12:33Z: 20 OK / 2 MISMATCH`, then the re-run
  `rerun end 2026-09-22T02:17:18Z: 2 OK / 0 MISMATCH`** (A rc 4 · B rc 3 · C wrong sha on #1179 rc 6 · D curdev = the parent 3916eacd1 rc 18 (the moved
  manifests read the parent's blobs -> GUARDED) · E curdev = #1170's head rc 19 LANDED · F a launcher copy expecting behind=2 on #1172 rc 10 · G no
  `ultrathink` rc 8 · H namespace sentence reworded rc 32 · I #1170 promoted to TIER 1 rc 7 · J MG-1 phrase reworded rc 25 · K RULE WHETHER IT BLOCKS
  reworded rc 30 · L by-name item 9 reworded rc 33 · M subject shortened rc 23 · N non-TTY launch rc 21 · O BOTH token `threadTokenMint` recased rc 30 ·
  P GATEWAY_URL localhost rc 31 · Q s-b18-batch reworded rc 28 · R the :4003 lsof reworded rc 29 · S a PENDING-PR- marker planted rc 34 (the partial
  ladder) · T the #1179 addendum blob zeroed rc 0 BY DESIGN (the launcher greps heads, not addendum blobs — the gate reads them) · **U the END_TREE zeroed
  rc 31: the first run's `want=30` was the drafter's S5 (MISMATCH by the control's typo, the launcher refusing at 31 as intended); re-run as U2 with
  want=31 -> OK · POSITIVE: the first run refused rc 18 on a TRANSIENT GitHub `RemoteDisconnected` on ONE contents GET (ks949-…test.ts) — UNJUDGEABLE is
  fail-closed by design (a launcher that cannot read a judged path must refuse, not assume); POSITIVE2 against the final prompt rc 0**). Controls dir
  `controls_gate18B.a5Z4Y5/` (every control's own `.out`); the re-run script `launcher_controls_gate18B_rerun.sh` -> `launcher_check_controls_rerun.out`.
- **After the controls, two prompt corrections** (part2; `prompt_gate18B.DRAFT.part2.txt.pre-1201-heldpair` beside): (i) the 16th's HELD pair 685d5f264 carries the SAME two anchoring
  paths at OTHER blobs (f66f3309d187 / d16d505fcc9c — `git ls-tree 685d5f264 …/anchoring/src/__tests__/`) — the earlier sentence asked the gate to assert
  their ABSENCE by path, which is false (the paths exist in every #1176 tree at c0c345bd0aae / a7d2c4bb3799): corrected to assert by BLOB; (ii) the
  root-manifest wording: the Dev root package.json did NOT move under #1036 (only the root lock; `p1036_paths.out`) — corrected (the drafter's S3 class,
  repeated in prose). `fill_prompt_3.out` (origin re-read 02:15Z, seven heads AGREE): **prompt
  `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1170-1179.prompt.txt` — 1028 lines, 145682 B, sha256
  ea5ffc74b68656fafb2fd5c0032d1921e397f9ac082aad9ff16bd3d8328f3bb2** (`.pre-021523` = the 1027-line sha 8852dcef… form the first controls run ran
  against; the delta is the two sentences above — every pin, count and by-name line unchanged). `gen_launcher.run6.out` (PYTHONDONTWRITEBYTECODE=1):
  the launcher regenerated BYTE-IDENTICAL — **`launch_qa_secuura_batch1170-1179.sh` 530 lines, mode 755, sha256
  508d1e3bfa519238e060be8255941a456a32aa975ddf87f046942b7b7d7d8a56** (the `.pre-1215` copy beside it is the same bytes; BOTH 174 / by-name 122 /
  output controls / heredoc parity / `bash -n` 0 as run 5).
- **`launcher_check_2.out`: `--check` rc 0 at 02:17:30Z-02:18:28Z** against the 1028-line prompt.
- `lsremote_final.out` 02:18:28Z: **develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 (UNMOVED off the pin at every read: 01:14:19Z, 01:25:23Z,
  01:44:44Z, 02:15Z, 02:18:28Z)**; the seven refs/pull/N/head as pinned (3e9f7d7b7 d74b04678 e1dea649c 8ced0d50b 13030ac59 e48b90e74 e62555dd0); the
  `ks-1171` glob returns ONLY the R16 TSFIX branch at 8ced0d50b.
- Checkout counts AFTER (`checkout_counts_after.txt` 02:18:31Z vs BEFORE 01:14:14Z): porcelain non-untracked 0 -> 0; porcelain total 17 -> 17;
  `.git/worktrees` 272 -> 272; for-each-ref 1223 -> 1223; count-objects 9416 -> 9416, in-pack 101422 -> 101422, packs 47 -> 47 (byte-identical —
  `diff` of the two files after their timestamp line rc 0); .git/config sha256 identical; HEAD `develop` 581ed7fa1 (unchanged).
- S7 (hygiene) — importing `round18B.py` under `PYTHONDONTWRITEBYTECODE=1` throughout: NO `__pycache__/` was written into this gateset (the gate16B
  drafter's S8 avoided). Nothing deleted anywhere; every pre-fix copy beside its file.
- Network: `git ls-remote` ×6 + the launcher's own ls-remote / compare / contents GETs under `--check` ×2 and the controls (×23 --check runs); GitHub GET
  (pulls / files / commits / compare / rulesets); AgentMail GET (list + by id); Linear GraphQL query. No mail sent, no pane tapped, no Linear write,
  nothing launched, no `inbox_routing.conf` write (count 0 at 01:55Z; Wednesday adds it), no write under `!CODING/`, no write into
  `2026-09-22_gate18C_seatC/`, no `git fetch`, no port connected by hand, no secret in any file, no `deadbeef` literal in the prompt.
