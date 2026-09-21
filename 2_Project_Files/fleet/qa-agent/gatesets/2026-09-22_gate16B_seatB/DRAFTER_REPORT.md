# DRAFTER REPORT — batch gate over Seat B 16th's EIGHT R15 test-only PRs (#1147 #1149 #1151 #1153 #1155 #1157 #1159 #1161; TIER 2 floor, TIER 1 on #1161; round 1 of 2)

Drafter: gate-drafter subagent under Wednesday (the 03:45 seat of 2026-09-22; session bb573f73). Started 2026-09-21T18:35:39Z (UTC, `date -u`; 04:35:39 AEST); the commission
and Wednesday's 04:37 AEST addendum (the 18:33Z HOLD mail; the #1153 cover predicate; the GO string) read whole; the gate15 gateset (COMMISSION / README / DRAFTER_REPORT /
capture / fill / gen / predict / gh / linear / shape / controls / repin) and its prompt (852 lines) read whole.
Status: COMPLETE — eight of eight READYs captured before the drafter began (17:01:06Z … 18:31:47Z; captures 18:37:07Z); every number below names its instrument.

## 0. Constraints honoured
- No `cd`; literal absolute paths; `git -C`; heredocs `<<'EOF'`; rc on its own line; nothing deleted or renamed (`.pre-HHMM-*` copies beside).
- Secuura checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` READ-ONLY (read verbs only: `ls-remote`, `show`, `cat-file`, `rev-parse`, `rev-list`, `diff`,
  `ls-tree`, `log`, `status`, `for-each-ref`, `count-objects`, `config --get`). Every write verb (apply, read-tree, write-tree, merge-tree, commit-tree) inside ONE
  `git clone --shared --no-checkout` scratch clone under this session's scratchpad (`predict16B.lyi_wnfu/clone`), from the script file `predict_batch_scratch_gate16B.py`
  with literal paths. `count-objects -v` byte-identical before/after (count 9064 / in-pack 101422 / packs 47 — `predict_batch_scratch_1.out`).
- Network: `git ls-remote` ×4 + GitHub / AgentMail / Linear READ APIs. No `git fetch` (develop unmoved). No launch, no mail, no pane tap, no Linear write, no
  `inbox_routing.conf` write, no write under `!CODING/`. Datasec mail unread (the inbox listing filters Seat B / Seat C / QA subjects only). No port connected by hand
  (`lsof` not needed — no listener of mine). No queue appended.

## 4. Drafter's own slips (recorded as they happen; FIRST in the final message)
S1 18:37Z — `capture_ready_mail_gate16B.py` shipped with a dead line (`hits = … if False else None`, a leftover from re-ordering the filter definitions); harmless (the
   next line rebound `hits`), removed at 19:13Z with `capture_ready_mail_gate16B.py.pre-0513-deadline` beside; the second run (`capture_ready_mail_2.out`) rebuilt the
   combined capture byte-for-byte in its sections (40 "exists, not overwritten"; the 6 NEW captures were all Seat C's — its READYs 9-13 and its 19:12Z STATUS).
S2 18:46Z — `gh_pr_reads_gate16B.py`'s Seat C namespace regex (`^feature/ks-<key>-.*-r15-.*-1$`) read #1154 (KS-1199) as OUTSIDE the namespace because its tail is
   `-r15-1` with NO tag between `r15` and `1` (its READY tag is `R15`); Wednesday's rule text reads `feature/ks-<key>-…-r15-…-1`. The drafter's regex was the stricter
   reading; NOT a Seat B fault (KS-1199 is not in the seat's 46-ticket guarded set — no attribution was owed) — carried into the prompt as a LEAD for the gate (by-name
   9: read series17.py's regex). No artefact carried a wrong value.
S3 19:07-19:08Z — four BOTH phrases and one by-name phrase were WRAPPED or absent in the prompt drafts (`declared ∪ the measured cover` wrapped; `MG-3 (the KEY-SET
   rule` wrapped; the literal tokens `started_utc` / `lock released` / `16053` absent), so the generator's line-wise checks refused (runs 1-2); rejoined / added
   (`fill_prompt_2.out`, `fill_prompt_3.out`). Two BOTH tokens (`KS-1201`, `KS-256`) were dropped from the BOTH list — they sit in the PR BODIES, not the READY mails
   (prompt-only now). The gate15 drafter's S3, repeated.
S4 19:08-19:09Z — the generator's output-control WANTS were typed against gate15's moved-develop shape: with develop UNMOVED, `DEVELOP_SHA` == `MERGE_BASE` and
   `ALL_OVER_DEV` == `ALL_OVER_PARENT` are ONE string each (count 4, not 2 + 2 / 2 + 3), and the header mentions `exit 10` six times, not four; run 3 refused, run 4
   refused again on the drafter's own miscount (5 for the tree), run 5 wrote. Caught by the generator's own controls before any file was written.
S5 19:00Z — the first prompt draft (part 1, framing paragraph) carried a self-correcting sentence ("seven NEW test files … no — FOUR new files + ONE modified");
   rewritten before the first fill — never in a written prompt.
S6 19:07Z — `gen_launcher_gate16B.py` run 1 printed seven `fatal: path … does not exist` lines to stderr from an uncaptured `git cat-file -e` (the rc was what was
   read; the message is git's) — cosmetic, captured from run 2.
S7 (a design note, not a fault) — the READY capture's combined file is REBUILT on every capture run with a fresh `rebuilt <instant>` first line, so its bytes change
   whenever the capture script runs even when no seat-B section changed; the launcher greps content, not a hash. `launcher_check_2.out` is the re-run against the
   rebuilt file.

## 1. Timeline (every value: instrument | file)
- 18:35:39Z commission + addendum read whole; the gate15 exemplar read whole.
- 18:35:53Z `lsremote_1.out` (`git ls-remote origin refs/heads/develop refs/pull/{1147..1165}/head 'refs/heads/feature/ks-<9 keys>-*'`, rc 0): develop 64ab10513; the
  eight heads = the commission's eight; Seat C's #1148 #1150 #1152 #1154 #1156 #1158 #1160 present; #1162+ absent; NO `feature/ks-1171-*` branch at origin (the HELD PR).
  18:35:56Z `checkout_counts_before.txt`: porcelain non-untracked 0; porcelain total 17; `.git/worktrees` 257; for-each-ref 1193; count-objects 9064 / in-pack 101422 /
  packs 47; .git/config sha256 6417b203accd…; HEAD `develop` 581ed7fa1 (the 15th's S1) | `git -C <checkout> status --porcelain | grep -v '^??' | wc -l`; `ls .git/worktrees | wc -l`;
  `for-each-ref | wc -l`; `count-objects -v`; `shasum -a 256 .git/config`; `rev-parse --abbrev-ref HEAD`.
- 18:36Z `inbox_list_gate16B.py` (`inbox_list_1.out`): 100 messages listed; the eight Seat B 16th READYs (PR 1 17:01:06Z … PR 9 18:31:47Z; PR 8 absent — HELD), the
  16:54:31Z and 18:33:17Z STATUS mails, four QUESTIONs, the 17:00:23Z ACK, Wednesday's ANSWERs / ADDENDA, Seat C's seven READYs to 18:25:36Z.
- 18:37:07Z `capture_ready_mail_gate16B.py` run 1 (`capture_ready_mail_1.out`): 40 mails captured VERBATIM by message id (TEXT_SHA256 per file): Seat B's 8 READYs
  (14576 / 13813 / 14169 / 14873 / 24702 / 15244 / 15392 / 14755 chars), 2 STATUS, 4 QUESTION, 1 ACK; Wednesday's 7 mails to B (incl. the brief 101834 chars); Seat C's
  7 READYs + 3 STATUS + 2 QUESTION; Wednesday's 6 mails to C. Combined `mail_gate16B_ready.md` 193388 B (sha256 ccc0616772057331… at 19:13Z after the rebuild).
- 18:40Z `round16B.py` written — the ONE pin source (every script imports it): sums adds 755 / dels 1 / lines 980 / canonicals 12 / tampers 12 / cells added 40 / paths 8
  (`python3 -c` over the module — the seat's `8 files +755/-1` and its lane deltas +26 / +10 / +4).
- 18:43:15Z `shape_gate16B.py` (`shape_1.out`, rc 0): develop tree 87b4aa12d2eb == round16B; `rev-list --count 581ed7fa1..64ab10513` = 13 (seat 13); the 12 canonicals
  EXIST, sha16 == the GROUPING 12/12, hunk headers == the QUEUE 12/12, `+`/`-` == the GROUPING 12/12, `+++` == the target 12/12, the READY fences == the run patches
  12/12; the declared-vs-actual new count: TRUNCATION on KS-928 (97 vs 107), KS-1133-B (97 vs 109), KS-1181-F3 (74 vs 75), KS-975-ITEM1 (34 vs 36); MISCOUNT-OVER on
  KS-1158-R3 (97 vs 96); consistent on the other seven | `re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@')` vs `sum(l.startswith('+') and not '+++')`. The 8 targets at
  develop: 7 ABSENT (`cat-file -e` rc 1), the ks1213 file 8082826898c2 / 226 lines (`rev-parse DEV:<path>`; `show | count('\n')`). The 9 tamper files == the seat's
  item-0 blobs 9/9 AND identical at 581ed7fa1 9/9. Per head (8/8): READY head == round16B == origin; parent == 64ab10513; behind/ahead 0/1; tree == the READY's; files ==
  the ONE test file; +/- == the READY; name-status A ×7 / M ×1; modes 100644; every path under `__tests__/`; head blob == the RECOUNT blob; line count at head 107 / 150 /
  109 / 96 / 309 / 98 / 75 / 36; `-` lines 0 ×7 and 1 on #1155 (`-});`); the four truncation rows' head blob != the seat's STRICT blob (4/4); subjects 90 / 82 / 81 / 88 /
  90 / 68 / 81 / 83 chars, all ASCII, own key only; author kamil.kreiser@secuura.ai ×8. Union paths 8, overlaps NONE, ∩ Seat C's dirs / pushed paths NONE. Static: the
  ks1004 lockout test exists at develop with "CARRIED FORWARD" ×1; anchorStateSync.ts:155 / :166 as the READY quotes; anchoring 22 test files incl. threadTokenMint.test.ts;
  the KS-1181 FILE NAME carries `ks-727` and its tamper file is a TEST file; rateLimitScope.ts 276 lines, :112 `export function principalScope(`, :118 as quoted;
  adminConfig.ts :1892 / :1897, documents.ts :1993 / :2609 / :2878, ssrf-guard.ts :477 / :478, ks727-errorhandler-class-guard.test.ts :32 as the READYs quote; the eight
  branches ASCII (lengths 94 / 78 / 82 / 84 / 138 / 73 / 73 / 85), own key once each, no archived key form; lane runners `jest` / `vitest run` ×3 (`scripts.test`);
  the hook :76 path filter as the 15th's F8.
- 18:44:48Z `predict_batch_scratch_gate16B.py` (`predict_batch_scratch_1.out`, rc 0; clone `predict16B.lyi_wnfu`): (a) the 12 canonicals into temp indexes read from
  64ab10513: strict `--check` rc 0 ×11, rc 128 `error: corrupt patch at line 100` on KS-1158-R3; `-R --check` rc 1 ×11 (rc 128 on R3); `--recount --check` rc 0 ×12;
  `-R --recount` rc 1 ×12; the STRICT APPLY for real on the new-file rows: KS-928 rc 0 -> e76b3e90db28 / 97 lines, KS-1133-B rc 0 -> e9dc6e3899f0 / 97, KS-1181-F3 rc 0
  -> 6250385ee49e / 74, KS-975 rc 0 -> 1fcffe443b5c / 34 (= the seat's F3 blobs 4/4), KS-1158-R3 rc 128 (nothing written), KS-1118 / KS-1179 strict == recount; the
  RECOUNT apply -> the RECOUNT column 8/8 with the line counts; nonexistent patch rc 128; per-PR trees == the head trees 8/8, final blobs == RECOUNT 8/8; PR 5's five
  stages -> the READY's four intermediate blobs + the final (5/5), reverse and seed-16 shuffle (`random.Random(16)`) -> the same tree; the all-12 in forward / reverse /
  seed-16 shuffle -> `c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d` ×3 = the seat's; shortstat `8 files changed, 755 insertions(+), 1 deletion(-)`, name-status 7 A + 1 M;
  every path in ALL8 == its RECOUNT blob 8/8; the HELD KS-1171 files ABSENT in ALL8 (2/2); the nine-PR octopus tree 649ccf34c6d1 IS in the shared store and differs from
  ALL8 on exactly KS-1171's two anchoring files; read-tree back -> 87b4aa12d2eb. (b) the eight heads by REAL `merge-tree --write-tree` over 64ab10513 both orders ==
  their head trees (fast-forward; parent == DEV ×8; == the canonical-apply tree ×8); chained in FOUR orders (forward, reverse, two seed-16 shuffles) -> `c54c1ae73ba3…`
  ×4; every PR path carries its head blob; each head tree != ALL8; ALL8 shortstat +755/-1. (c) origin develop 64ab10513 UNMOVED — no fetch; `newdev_tree.txt` written
  (DEV_NOW / TREE / ALL8_OVER_NEW = the head trees). Empty-repo numstat rc 128. count-objects byte-identical; for-each-ref 1193 -> 1194 (a moving reading — the seats).
- 18:46:02Z `gh_pr_reads_gate16B.py` (`gh_pr_reads_1.out`, rc 0): 36 open PRs; per PR (8/8): head == READY == round16B, base develop@64ab10513, open, mergeable True /
  `unstable`, 1 commit, author kksecura, created 16:59:28Z / 17:10:54Z / 17:28:29Z / 17:38:22Z / 17:49:50Z / 18:02:56Z / 18:16:30Z / 18:29:29Z; closing 0/0/0 ×8;
  completeness detector hits: #1147 body ×1 + commit ×1 ("a completeness cell asserts every graded cell ran"), #1153 commit ×1, #1157 commit ×1 (the model's guard
  wording — for the gate to read); body Refs exactly the own key ×8; commit Refs the same; titles == round16B ×8, ASCII; branches == round16B, ASCII, no non-ASCII byte;
  files API == the ONE test file ×8, `outside __tests__: []` ×8, additions == the READY ×8, deletions == ×8, status added ×7 / modified ×1; archived keys in
  title/branch/subject NONE ×8; live content key `KS-1213` in #1155's branch (the file-name form, kept); `ks-727` in #1159's FILE NAME (files API) True, in its branch
  False; body keys = own + KS-1201 + KS-256 ×8 (the standing mentions); every body carries INCOMPLETE / 12/15 / SKIPPED / skips are not a pass / TEST-FILE-ONLY /
  --recount / RECOUNT / strict / cover / lock / started_utc / released / PROTOCOL-CLEAN / stubs=4 / typecheck17 / TS2322 / netlog / :5432 / threadTokenMint / tier 1 /
  tier 2; #1153's body `corrupt patch` ×3; #1161's `SECURITY` ×2; compare develop...head merge_base 64ab10513 / ahead 1 / behind 0 / files 1 ×8; files API union 8.
  Ruleset 18499832 `require-pr-gates` active, updated_at 2026-09-10, rules deletion / non_fast_forward / pull_request (required_approving_review_count 0,
  require_extra_approval_for_unattributed_changes True, merge / squash / rebase), conditions develop + main. Seat C's seven PRs: head == its READY ×7, base
  develop@64ab10513, kksecura, created 17:03:56Z … 18:23:31Z; head-ref namespace `feature/ks-<key>-…-r15-…-1` True ×6 and FALSE on #1154 (`…-r15-1`, S2); files ×7 under
  its three dirs; ∩ our 8 paths NONE, ∩ our 9 tamper files NONE. Open PRs touching any of the 8 paths or 9 tamper files: 0 hits; positive control merged #894 ∩ tamper
  files -> {rateLimitScope.ts}; negative control merged #1146 -> ∅. PR-number traps: #928 closed (KS-950), #975 closed (KS-1126), #1118 closed (KS-1006 + KS-1236),
  #1133 closed (KS-880), #1158 OPEN = Seat C's KS-855, #1171 / #1179 / #1181 / #1229 404. The window #1147..#1165 at 18:46Z: #1147-#1161 as pinned; #1162 (KS-1156,
  18:36:04Z) and #1163 (KS-1188, 18:43:32Z) landed after the drafter's capture; #1164 / #1165 404 then.
- 18:48:17Z `lsremote_2.out`: develop 64ab10513; Seat C's KS-1199 branch `…-rows-r15-1` (the tag-less tail), KS-1156's `…-r15-r15-1` (#1162) beside the 15th's
  `…-r15-a3-1` (#1146, merged), KS-1188's `…-r15-f1a-f1b-f2-1`; refs/pull/1162/head b6b70d787, 1163 02f12926f; 1164 / 1165 absent then.
  18:48:44Z `gh_seatc_late_1.out`: #1162 ONE auth test file (+111), #1163 THREE auth test files (+122 / +136 / +144) — ∩ our paths NONE; round16B.SEATC extended.
- 18:49:29Z `linear_reads_gate16B.py` (`linear_reads_1.out`; the file asserts no `mutation`): the 8 own tickets In Progress on the board login, archivedAt None,
  attachments exactly {own PR contributes} (+ #874 on KS-928, 2026-09-06), comments 2 / 0 / 0 / 0 / 0 / 0 / 0 / 0; the linear[bot] (actor GitHub) walks Backlog -> In
  Progress: KS-928 16:59:38Z (with an earlier walk 2026-09-14T10:14:36Z and a manual move back to Backlog 10:15:35Z by the board login), KS-1118 17:11:05Z, KS-1133
  17:28:39Z, KS-1158 17:38:32Z, KS-1229 17:50:00Z, KS-1179 18:03:06Z, KS-1181 18:16:40Z, KS-975 18:29:39Z; attachmentsForURL pull/N == [(own key, contributes)] 8/8;
  KS-1171 Backlog, 0 attachments (HELD); branchName scan: KS-1229's `ks1213`, KS-1181's `ks-727` — the brief's two findings CONFIRMED; non-ASCII 0. Seat C's 13 keys:
  attachments +#1148 / +#1150 / +#1152 / +#1154 / +#1156 / +#1158 / +#1160 / +#1162 / +#1163 on the nine pushed; KS-1123 Backlog #1002; KS-1193 / KS-1217 / KS-910 none
  (at that read); attachmentsForURL for Seat C's nine == its own key each. Namespace KS-1147 … KS-1163 ALL exist: KS-1158 = PR 4's OWN (att #1153); KS-1156 att #1162 +
  #1146; KS-1150 In Progress #987; KS-1151 Done ARCHIVED; KS-1152 In Progress #1143; KS-1153 In Progress #1056; the rest Backlog, no links. Archived 24/24 with
  archivedAt set (KS-727 2026-09-05T05:31Z; KS-597 2026-09-17T23:51Z; KS-1270 2026-09-20T06:32Z); the 20 live content keys as the READYs list them (KS-1285 Done on
  Peter, not archived); KS-1004 Done ARCHIVED 2026-09-14 (the #1153 cover cell's key); KS-1123 Backlog #1002 (3 comments); KS-256 In Progress 44 comments / KS-1201
  Backlog 1 comment (no new attachment); KS-485 63 / KS-772 26 comments (the 15th's counts, unchanged); KS-696 Todo 11:42Z; KS-1287 Backlog (Peter's new). Controls:
  pull/1146 -> {KS-1156}; pull/1135 -> {KS-1006, KS-1236}; pull/1129 -> []; pull/874 -> six keys incl. KS-928; pull/894 -> []; pull/1164 -> [].
- 19:02:47Z `fill_prompt_gate16B.py` run 1 (`fill_prompt_1.out`): origin re-read IN THE SAME ACTION (ls-remote 19:02:50Z, 17 refs) — origin / round16B / the READYs
  AGREE on develop and all eight heads; 30 tokens substituted (the eight PR numbers ×24 / 21 / 21 / 29 / 23 / 21 / 21 / 27, the eight heads ×2 each, the eight READY
  instants, develop ×6, its tree ×1, the eight-PR tree ×8); the prompt written: 867 lines, 118572 B. Runs 2-3 after S3: 867 lines, 118649 B, sha256
  28e2e57b1ac69d354af80015bceae83802a901d025251a23e3c7122d03ae9147 (`fill_prompt_3.out`); report dir `2026-09-22-batch1147-1161-r1`; subject prefix
  `[QA -> Wednesday] BATCH GATE #1147-#1161 (eight PRs; tier 2 floor, tier 1 = #1161: Seat B 16th test-only pins) —`; the GO string present.
- 19:07-19:09Z `gen_launcher_gate16B.py` runs 1-5 (`gen_launcher.runN.out`): pins re-read at origin (develop 64ab10513 = the pin, UNMOVED; 8 pull heads + 8 branches OK;
  the ks-1171 glob EMPTY), `rev-list --count parent..develop` 0, merge-base == parent, the move ∅; per head parent == 64ab10513, behind/ahead 0/1, tree == pin, files ==
  the one path, +/- == the READY, modes 100644, status A ×7 / M ×1, every path `__tests__/`, tier 2 ×7 / tier 1 ×1; union paths 8, overlaps none; the 8 (develop blob |
  ABSENT) values agree at the parent AND the current develop; 41 unchanged-read paths (this round's 9 tamper files, the 15th's five, the hook, preflight.sh,
  run-shell-suites.sh, fix-libsodium-symlink.js, jwt.ts, provenance.ts, proxy.ts, the ks1004 cover test, threadTokenMint, the four lanes' package.json / config /
  tsconfig / lock (shared has no lock), the Dev package.json + lock, eslint.config.mjs) same blob at the parent, the current develop and every head; tree-hash control ->
  the parent tree; compose over the parent == each head tree 8/8; compose(the 8 into the parent tree) = `c54c1ae73ba3…`; compose(the 8 into the current develop tree) =
  the same; per-PR trees == predict 8/8; BOTH 158 tokens present in BOTH the capture and the prompt; by-name 97 keywords across 12 items + the closing; output controls
  matched (run 5); heredoc parity PY 0 / 10-10, PYJ 0 / 110-110; `bash -n` rc 0 -> **`launch_qa_secuura_batch1147-1161.sh` 515 lines, mode 755, sha256
  c98661da780e8ab81a9a3c6fcc7a38ea8eb7bb3f954cce51256c38d7a944118f** (`gen_launcher.run5.out`).
- 19:09:54Z-19:11:42Z `launcher_check_1.out`: **`--check` rc 0** — eight heads on origin; compares merge_base 64ab10513 / ahead 1 / behind 0 / files 1 ×8; develop
  judged by content over 49 paths = the pin; every grep passed.
- 19:12:28Z `launcher_controls_gate16B.sh` started in the background (`launcher_check_controls.out`): A rc 4, B rc 3, C (wrong sha on #1161) rc 6, D (curdev = the old
  parent 581ed7fa1) rc 18, E (curdev = #1147's head) rc 19 LANDED, F (a launcher copy expecting behind=1 on #1149) rc 10, G rc 8 … — see the addendum for the end line.
- 19:12Z `repin_and_launch_gate16B.sh` written (reads its pins FROM the launcher; `bash -n` rc 0; the sed pin-parse dry-read prints develop 64ab10513 and the eight
  PRs; NOT run). Routing line `QA/Secuura-batch1147|coagent@agentmail.to|yes` count 0 (absent, as commissioned — Wednesday adds it); the batch1136 control 1.
- 19:13Z `capture_ready_mail_gate16B.py` run 2 (`capture_ready_mail_2.out`, after S1): 40 exists-not-overwritten; 6 NEW — all Seat C's (READYs 9-13: #1162 KS-1156,
  #1163 KS-1188, #1164 KS-1193 ba730c6ac, #1165 KS-1217 4ecb09cf2, #1166 KS-910 a08741f51; its 19:12Z HOLDING STATUS: twelve READY, GO subject
  `GO: merge #1148, #1150, #1152, #1154, #1156, #1158, #1160, #1162, #1163, #1164, #1165, #1166 batch`, twelve-PR tree 4817a9c2ea23…). `seatc_late_paths_1.out`: Seat C's
  14 READY paths (12 `.test.ts` under api-gateway / auth + 2 `.test.sh` under scripts/__tests__/) ∩ our 8 = ∅, ∩ our 9 tamper files = ∅, all under its three dirs.

## 2. Artefacts produced
- **Prompt** — three draft parts `prompt_gate16B.DRAFT.part1..3.txt` assembled by `fill_prompt_gate16B.py` (first line `ultrathink`): framing (EIGHT PRs, THREE lanes,
  ZERO product bytes, TIER 2 floor + TIER 1 on #1161, the HELD PR named and excluded); the LEADS; the NAMESPACE NOTE (the odd numbers are this seat's, the even Seat C's;
  KS-1158 vs #1158; KS-1156 vs #1156; the closed #928 / #975 / #1118 / #1133; the held / superseded / Seat C READY files; the archived keys inside file names); the per-PR
  table (eight entries: canonical + sha16 + hunk + the strict/recount class with the strict SHORT blob, the tree, the cells, the tamper site with its scope anchor and
  declared reds, the cover, the lane counts, tsc / typecheck17 / eslint, the census, the lock window, the tier, the Refs); TIER PER PR (eight lines, `#1161 KS-975: TIER 1`),
  round 1 of 2, time-box 180 min, the budget order (tier 1 first); MERGE AUTHORITY (targets17 / merge17 re-keyed to EIGHT, MG-1 1×8, MG-2 inherited not exercised, MG-3
  key sets, the lock around merge17's fetch, `--pair-blob` unused, all eight tickets stay, the eight bot walks with instants, KS-975's assignment, the merge order); THE
  SHAPE (develop unmoved, the heads' parent = develop, the compare behind 0, the branches, the held branch absent at origin, the per-PR trees = the head trees, the
  eight-PR tree in three + four orders, the held octopus's diff, the zero overlap with Seat C's 12 paths at the drafter's read, the canonical identity with the recount
  class and the four strict SHORT blobs, the run tips, the 12 tampers, the open-PR sweep); the sources (the READYs by filename, the STATUS / QUESTION / ACK mails,
  Wednesday's ANSWERs by filename, Seat C's mails as context, the brief, the seat's record folder by file, the 12 READY files + run dirs, PRIOR = batch1136-1146-tier2-r1
  / EARLIER = batch1130-1135-tier1-r1 / OLDER = batch1119-1128-tier1-r1, the Linear keys incl. the namespace / archived / content / Seat C sets, the handover, Seat C's
  attrib17.retro.json, the charter); worktree / history / checkout / push-lock rules (s-b16-*, s-c16-*, the held worktree, the lock directory read-only); farming per
  ENTRY (three node lanes; anchoring not a lane; no shell suite); Postgres isolation + CENSUS RULE v2 (originate / shared / security REPORT; the `anchoring:4005` shape;
  the ephemeral-port triples) + the jest preload note; listeners incl. the cross-seat SIGTERM and the ancestry rule; NOT-TESTED items (the eight preflight pushes 12/15 +
  44 of 44 inside the lock; the HELD PR; the recount class; the cover; mergeable_state; the two-seat artefacts; the intermittents); TWELVE by-name items exactly as
  commissioned (1 TIER AND ROUND; 2 TEST-FILE-ONLY; 3 THE TREES incl. Seat C's set-and-when; 4 CANONICAL-PATCH IDENTITY with the `--recount` class; 5 THE CELLS with
  the cover predicate; 6 PER-FILE TYPECHECK DELTA 0; 7 THE CENSUS RULE v2; 8 LINEAR LINK HYGIENE; 9 THE TWO-SEAT ARTEFACTS (the lock rows monotonic; the attributions
  by NAME under the four conditions with the corrected (4); the tag-less `-r15-1` regex question; Seat C's mirror); 10 THE SEAT'S OWN FINDINGS / SLIPS F1-F8 + S1-S8;
  11 THE INTERMITTENTS; 12 MERGE ADDENDUM — EIGHT lines, NOT-PINNED rows NAMED incl. #1153 R3 for its own file) + the standing rules; per-PR requirements; suites at each
  head AND on the eight-PR tree; CARRY-FORWARD; hygiene; the report dir `…/reports/2026-09-22-batch1147-1161-r1/`; the NOT-PINNED candidate rows (R3COVEREDBYKS1004,
  TESTFILETAMPER, SHAREDGUARDS5S, ANCHORING4005UNATTRIBUTED); the EIGHT-line verdict; the MERGE ADDENDUM line format with the eight head blobs and modes; WRITE report.md
  BEFORE THE MAIL; the exact subject; the GO string the seat expects.
- **Launcher** — generated by `gen_launcher_gate16B.py` (above). Pins: develop 64ab10513 + every head by branch AND refs/pull/N/head (exit 6); compare per PR merge_base
  64ab10513 / ahead 1 / behind 0 / files 1 (exit 10); develop judged by CONTENT over 49 paths (8 targets — 7 ABSENT-judged with LANDED detection, 41 unchanged-read);
  GUARDED list for a move (shared / originate / security / anchoring src + config, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs); the grep ladder
  7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33 + 34; overrides `QAB1147_*` refuse at launch (16); TTY (21); pane `QA/Secuura-batch1147`.
- `repin_and_launch_gate16B.sh` (pins read FROM the launcher; the ks-1171 glob asserted empty; NOT run), `launcher_controls_gate16B.sh` (running at this write), `README.md`
  (section 0 the recount class + the move recipe; section 8 the finish-from-disk recipe), this report, `round16B.py`, the capture / list / shape / predict / gh / linear
  scripts and their outputs (section 1).

## 3. LEADS for the gate (claims to grade; the drafter's re-derivation disagrees with the seat's VALUES nowhere)
1. THE RECOUNT CLASS — four TRUNCATION rows whose strict apply rc 0 writes a SHORT file (the seat's F3 blobs reproduced 4/4) and one rc-128 row; the eight heads are
   the RECOUNT blobs (8/8). A strict-first seat would have committed truncated tests (KS-1133-B's two controls among the dropped lines).
2. #1153's DEVELOP COVER — the ks1004-anchor-failed-lockout cell (`… the txHash is CARRIED FORWARD, not nulled …`) reds the R3 tamper at develop (809 cells, red 1
   NEW) and in the PR frame (814, red 3); the seat corrected READY 4's cover sentence in its 18:33Z STATUS; READY 4's "FOR THE GATE" template line ("EMPTY for every
   tamper of this PR") is false for it; KS-1004 is ARCHIVED (content). The NOT-PINNED-for-its-own-file question: what does R3 pin that ks1004 does not (the NETWORK
   field?) — read both cells.
3. #1159's tamper is on a TEST file's header COMMENT (`ks727-errorhandler-class-guard.test.ts:32`) with NO scope anchor in anchors17.json (`:None 'None'`) — located by
   the whole-line `from` + a `describe(` x4 control; the STANDING_LINES rule wants a unique anchor or a line number with content asserted — grade the instrument.
4. #1157's ssrf-guard.ts is packages/shared — a shared security LIBRARY; the tier-1 precedent names services/security (and auth): the drafter pins tier 2; the gate rules.
5. The namespace: KS-1158 (PR 4's ticket) vs PR #1158 (Seat C's KS-855); KS-1156 (Seat C's #1162's + the 15th's #1146's) vs PR #1156 (Seat C's KS-1237); #928 / #975 /
   #1118 / #1133 closed, other tickets'; every even number in the window is Seat C's.
6. Seat C's #1154 head ref `feature/ks-1199-ks1072-…-rows-r15-1` — a tag-less tail; the drafter's stricter regex read it as outside the `-r15-…-1` namespace (S2). No
   attribution was owed for KS-1199 (not in the seat's guarded set); the question is whether series17.py's regex admits that shape — for the gate.
7. KS-928's Linear history: bot-walked 2026-09-14T10:14:36Z (on #874), moved BACK to Backlog 10:15:35Z by the board login, walked again 16:59:38Z on #1147 — the READY
   says "Backlog at boot -> In Progress now": true; the earlier rows are context the READY did not carry.
8. The eight bot walks with instants (section 1, linear_reads) — the READYs say "walked", the instants are the drafter's.
9. The cross-seat SIGTERM (Seat C's S3 at 16:55Z; the seat's S6 / S7): the wrapper died, sender 57702 survived then exited 3 on the seat's own series STOP, ONE sender
   (16053) alive after — eight READY message ids, one per PR (`inbox_list_1.out`), none duplicated.
10. The originate census's `anchoring:4005 (unattributed)` unestablished attempts (51 per five runs; 367 per 31 on #1155) — the 15th's carried shape; WHICH test file
    the seat's instrument did not name.
11. The shared repo-walk 5 s timeouts under load — the ks1181 run-1 STOP (five cells red beside the originate jest stream, wall 40.5 s; serial re-run clean); the
    anchoring db.retry 7.2 s under load avg 13 (baseline run 1; not a lane here).
12. The seat's S8 — its mail/out-03 / out-04 request files were overwritten by the sender (READY 1 / READY 2 requests); the 16:48Z QUESTION and 16:54Z STATUS survive as
    mails (captured here by id) — a RECORD slip.
13. The seat's completeness-detector hits (#1147 body + commit; #1153 / #1157 commit) are the model's "a completeness cell asserts every graded cell ran" wording — read
    the cell; not a closing word.
14. Seat C's READY 13 (#1166, KS-910) carries TWO `.test.sh` files under scripts/__tests__/ — a bash lane; not ours; disjoint (seatc_late_paths_1.out).

## 5. NOT MEASURED by the drafter (named, not asserted)
- Any suite, tsc, eslint, typecheck17 or census run — the drafter ran no test (809 -> 813 / 812 / 813 / 814 / 819, 907 -> 914 / 910, 216 -> 220, the batch 835 / 917 /
  220, anchoring 328/329, tsc 0 ×4, eslint 0/0 ×8, typecheck delta 0 ×8, TS2322 CAUGHT ×8, the cells 4 / 3 / 4 / 5 / 85->95 / 7 / 3 / 4, the red sets, the census
  attempts / established / REPORT sets) are carried as the seat's claims.
- The tamper plants themselves — the drafter did not plant any tamper (the `from` texts were not re-located in the tip's bytes beyond the READY-quoted lines the
  shape script printed at :1897 / :742 / :446 / :166 / :1993 / :2609 / :2878 / :478 / :32 / :118).
- The live PR bodies' full text beyond the detectors / substrings (bodies never printed); the seat's raise/ records (bodies17.py, series17.py's regex, batch8.py,
  typecheck17.py, the lock files, the push logs, the stubs files) — named in the prompt, not read by the drafter beyond `ls`.
- The seat's HANDOVER (head read for the ON THE GO steps) and RECORD.md (read) — their claims not re-measured beyond what section 1 lists; Seat C's record folder — not
  read (`ls` of the parent only).
- The Seat C READYs' contents beyond their subject line, head line and path lines (their bodies not read; Seat C's own findings are its gate's).
- Whether the combined capture's TEXT_SHA256 per mail matches what a re-fetch returns (the gate re-fetches by message id).
- The DKIM / inbox discriminator on the GO (the drafter sends no mail).

## 6. Checkout counts AFTER (read verbs only throughout) — `checkout_counts_after.txt` (written at the drafter's close; section 8).

## 7. The launcher's controls — RUNNING at this write (`launcher_controls_gate16B.sh` -> `launcher_check_controls.out`; ~35 min; A-G OK at 19:16Z). Control T
   (the #1161 addendum blob replaced by zeros) is designed to PASS (rc 0): the launcher greps heads and 12-hex tokens, not the addendum's 40-hex blobs — the gate reads
   blobs itself; a MISMATCH there would mean the launcher is stricter than documented, not a fault.

## 8. Final state — see the addendum at the end of this file (written at the close).

## 8. Final state (addendum, 2026-09-21T19:33Z / 05:33 AEST)
- **Controls: `launcher_check_controls.out` — `controls end 2026-09-21T19:29:25Z: 21 OK / 0 MISMATCH`** (A rc 4 · B rc 3 · C wrong sha on #1161 rc 6 · D curdev = the old
  parent 581ed7fa1 rc 18 · E curdev = #1147's head rc 19 LANDED · F a launcher copy expecting behind=1 on #1149 rc 10 · G no `ultrathink` rc 8 · H namespace sentence
  reworded rc 32 · I #1147 promoted to TIER 1 rc 7 · J MG-1 phrase reworded rc 25 · K RULE WHETHER IT BLOCKS reworded rc 30 · L by-name item 9 reworded rc 33 · M subject
  shortened rc 23 · N non-TTY launch rc 21 · O BOTH token `threadTokenMint` recased rc 30 · P GATEWAY_URL localhost rc 31 · Q s-b16-batch reworded rc 28 · R the :4003 lsof
  reworded rc 29 · S a PENDING-PR- marker planted rc 34 (the partial ladder) · T the #1161 addendum blob zeroed rc 0 BY DESIGN (the launcher greps heads, not addendum
  blobs — the gate reads them) · POSITIVE rc 0). Controls dir `controls_gate16B.b1BQig/` (every control's own `.out`).
- **After the controls, Seat C's late READYs folded into the prompt** (`patch_drafts_seatc_late.py` -> `patch_drafts_seatc_late.out`; `.pre-0529-seatclate` copies of the
  three draft parts beside): #1164 KS-1193 (ba730c6ac), #1165 KS-1217 (4ecb09cf2), #1166 KS-910 (a08741f51; two `.test.sh`) — twelve Seat C PRs at its 19:12Z HOLDING
  STATUS, its GO string and twelve-PR tree named. `fill_prompt_4.out` (origin re-read 19:29Z, eight heads AGREE): **prompt
  `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1147-1161.prompt.txt` — 870 lines, 119351 B, sha256
  b2eb1ca82a5cade7c3ceb51ec06ec5bd8a04c7b5d2bbd8f927d51b06dfb51aca** (`.pre-192947` = the 867-line sha 28e2e57b… form the controls ran against; the delta is the three
  Seat C sentences only — every pin, count and by-name line unchanged). `gen_launcher.run6.out` (PYTHONDONTWRITEBYTECODE=1): the launcher regenerated BYTE-IDENTICAL —
  **`launch_qa_secuura_batch1147-1161.sh` 515 lines, mode 755, sha256 c98661da780e8ab81a9a3c6fcc7a38ea8eb7bb3f954cce51256c38d7a944118f** (the generator's `.pre-0529`
  copy beside it is the same bytes; BOTH 158 / by-name 97 / output controls / heredoc parity / `bash -n` 0 as run 5).
- **`launcher_check_2.out`: `--check` rc 0 at 19:30:15Z-19:31:57Z** against the 870-line prompt and the rebuilt combined capture (193388 B, sha256 ccc0616772057331…).
- `lsremote_final.out` 19:31:57Z: **develop 64ab105132eada0621622acf4d6053bc59926780 (UNMOVED)**; the eight refs/pull/N/head as pinned (e456ffb5e 75f5b924e 10c689dcf
  be21a0ae4 b455e4594 8b0713d8f c6af5ca67 7f426f170); the `ks-1171` glob EMPTY (the HELD PR still un-pushed).
- Checkout counts AFTER (`checkout_counts_after.txt` 19:32:02Z vs BEFORE 18:35:56Z): porcelain non-untracked 0 -> 0; porcelain total 17 -> 17; `.git/worktrees` 257 -> 257;
  for-each-ref 1193 -> 1197 (the seats' remote-tracking refs — a moving reading, not mine); count-objects 9064 -> 9064, in-pack 101422 -> 101422, packs 47 -> 47
  (byte-identical); .git/config sha256 identical; HEAD `develop` 581ed7fa1 (unchanged).
- S8 (hygiene) — importing `round16B.py` wrote a `__pycache__/` directory into this gateset (the interpreter's bytecode cache); left in place (never delete), the later
  runs used `PYTHONDONTWRITEBYTECODE=1`. Nothing reads it.
- Network: `git ls-remote` ×6 (18:35:53Z, 18:48:17Z, 19:02:50Z, 19:07:43Z, 19:29Z, 19:31:57Z) + the launcher's own ls-remote / compare / contents GETs under `--check` and
  the controls; GitHub GET (pulls / files / commits / compare / rulesets); AgentMail GET (list + by id); Linear GraphQL query. No mail sent, no pane tapped, no Linear
  write, nothing launched, no `inbox_routing.conf` write (count 0 at 19:12Z; Wednesday adds it), no write under `!CODING/`, no `git fetch`, no port connected by hand.
