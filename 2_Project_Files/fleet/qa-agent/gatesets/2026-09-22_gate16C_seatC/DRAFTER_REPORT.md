# DRAFTER REPORT — batch gate over Seat C 16th's TWELVE test-only PRs (#1148 #1150 #1152 #1154 #1156 #1158 #1160 #1162 #1163 #1164 #1165 #1166; TIER 2 floor, TIER 1 on the six auth pins; round 1 of 2)

Drafter: gate-drafter subagent under Wednesday (the 03:45 seat of 2026-09-22), commissioned 05:11 AEST. Started 2026-09-21T19:12:22Z (UTC, `date -u`);
both commissions + the gate15 README / DRAFTER_REPORT / scripts / prompt / launcher + the gate16B sibling's scripts and drafts read whole before the
first write. Every number below names its instrument and its file. The sibling gate16B drafter's dir was READ (its scripts are the template), never
written.

## 0. Constraints honoured
- No `cd`; literal absolute paths; `git -C`; heredocs `<<'EOF'`; rc on its own line; nothing deleted or renamed (`.pre-HHMM-*` copies beside).
- Secuura checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` READ-ONLY (read verbs only: `ls-remote`, `show`, `cat-file`, `rev-parse`,
  `rev-list`, `diff`, `ls-tree`, `log`, `status`, `for-each-ref`, `count-objects`, `config --get`). Every write verb (apply, read-tree, write-tree, merge-tree,
  commit-tree) inside ONE `git clone --shared --no-checkout` scratch clone under this session's scratchpad (`predict16C.p9o7o6_c/clone`), from the script
  file `predict_batch_scratch_gate16C.py` with literal paths. `count-objects -v` byte-identical before/after (count 9064 / in-pack 101422 / packs 47 —
  `predict_batch_scratch_1.out` first and last lines; `checkout_counts_before.txt` vs `checkout_counts_after.txt`). No `git fetch` was needed — develop
  never moved.
- Network: `git ls-remote` ×4 (19:12:22Z, 19:24:5xZ in predict (c), 19:44:11Z in fill, 19:4xZ in the generator) + the launcher's own reads under `--check`
  and the controls; GitHub GET (pulls / files / commits / compare / contents / rulesets); AgentMail GET (list + by id); Linear GraphQL query (the file
  asserts no `mutation`). No mail sent, no pane tapped, no Linear write, nothing launched, no `inbox_routing.conf` write, no write under `!CODING/`, no
  port connected by hand, no key printed (`/usr/bin/grep -c -i 'lin_api\|ghp_\|github_pat'` over `gh_pr_reads_1.out` = 0; `lin_api` over `linear_reads_1.out`
  = 0). Datasec mail unread (the inbox listing filters on Seat B / Seat C / Blockchain subjects only). Nothing written into the gate16B dir.

## 4. Drafter's own slips (recorded as they happen; FIRST in the final message)
S1 19:13:23Z — `capture_ready_mail_gate16C.py` run 1 tested the "names Seat B 16th" branch BEFORE the "[Secuura/Blockchain-C ...] STATUS" branch, so
   Seat C's 16:56:14Z S3 STATUS (its subject names "Seat B 16th ready_send WRAPPER") was written as `mail_seatB16_status_seat_c_16th_s3_cross_seat_i_sigte_1656.md`
   and left OUT of the combined seat-C capture. Fixed by testing the `[Secuura/Blockchain-C ->` prefix first (`capture_ready_mail_gate16C.py.pre-1913-s3status`
   beside); run 2 wrote the correctly named `mail_seatC16_status_1656.md` (same message id, same TEXT_SHA256 29166adc7679…) and rebuilt the combined
   capture with FOUR STATUS sections (242508 B, sha256 210c5393fb67…). The mis-named copy stays beside as a record (never a delete); no value was wrong.
S2 19:22:56Z — `shape_gate16C.py` run 1 looked for KS-1199's READY file as `READY_KS-1199-R15-R15_*` (KS-1156's shape) and printed NOT FOUND for it (the file
   is `READY_KS-1199-R15_…` — its TAG is R15); also counted "leg 12" case-sensitively (the comment says "Leg 12": 0). Fixed both (`shape_gate16C.py.pre-1923-ks1199glob`
   beside); run 2 (`shape_2.out`): 15/15 fences == run patches, "leg 12" (case-insensitive) 1 at :49. `shape_1.out` kept as the pre-fix record.
S3 19:49Z — `gen_launcher_gate16C.py` run 1 refused on four BOTH tokens the prompt did not carry: `1256 insertions` (the prompt said `+1256/-11`),
   `1471 insertions` (NEITHER side — the capture says `+1471/-11`; the token was mine), `delta -1` (the prompt used a Unicode MINUS U+2212 in three
   places — the READYs' ASCII `delta -1` is the seat's word), `Refs KS-1185` (wrapped across two prompt lines). Fixed in the drafts (U+2212 -> `-` ×7,
   the shortstat quoted in the seat's own form, the wrapped phrase rejoined) and the token replaced by `+1471/-11`; run 2 refused on four WRAPPED by-name
   phrases (`outside __tests__: []`, `grade present / absent + MONOTONIC`, `never by a basename`, and a keyword that named the pre-substitution token
   `__ALL12__` — replaced by `on exactly KS-1123's one file`); run 3 wrote. The gate15 / gate16B drafters' wrap slip, repeated — the generator's line-wise
   check is the control that caught it before any file was written.
S4 (a design note, not a fault) — the generator's unchanged-read list first named guessed file names (`ks949-repo-walk.test.ts`, an auth-side ks1123
   file) before the drafter read the tree; corrected to the real names (`ks949-platform-admin-seed-identity.test.ts`, `ks1072-the-latest-anchor-selector-documents-a.test.ts`,
   `ks815-verification-router-guards-its-own-body.test.ts`, the two api-gateway ks1123 files) BEFORE the first generator run — no output carried the guess
   (the generator drops an absent path with a printed line; none was dropped: 38 unchanged-read paths, `gen_launcher.run3.out`).

## 1. Timeline (every value: instrument | file)
- 19:12:22Z `lsremote_1.out` (`git -C <checkout> ls-remote origin refs/heads/develop 'refs/pull/114[7-9]/head' 'refs/pull/115*/head' 'refs/pull/116*/head'`, rc 0):
  develop 64ab10513; refs/pull/1148 c4a96cfe0 · 1150 250a9b9ed · 1152 28d1e4df6 · 1154 889b05391 · 1156 58d293a87 · 1158 ddac6d7d5 · 1160 ef4713cc6 · 1162 b6b70d787 ·
  1163 02f12926f · 1164 ba730c6ac · 1165 4ecb09cf2 · 1166 a08741f51 — all twelve == the commission's heads; Seat B's eight odd heads present.
- 19:12:25Z `checkout_counts_before.txt`: porcelain non-untracked 0; porcelain total 17; `.git/worktrees` 257; for-each-ref 1197; count-objects count 9064 /
  in-pack 101422 / packs 47; .git/config sha256 6417b203accd…; HEAD `develop` 581ed7fa1 (the 15th's S1). | `git status --porcelain | grep -v '^??' | wc -l`;
  `ls .git/worktrees | wc -l`; `for-each-ref | wc -l`; `count-objects -v`; `shasum -a 256 .git/config`; `rev-parse --abbrev-ref HEAD`.
- 19:13:xxZ `inbox_list_gate16C.py` (`inbox_list_1.out`, 200 messages listed): the twelve Seat C 16th READY subjects 17:06:23Z (PR 1) … 19:08:40Z (PR 13),
  the 19:12:28Z HOLDING STATUS, the 16:46 / 16:51 / 16:56 STATUS mails, the 16:08 and 17:29 QUESTIONs; Seat B's eight READYs + its mails.
- 19:13:23Z-19:13:54Z `capture_ready_mail_gate16C.py` runs 1-2 (`capture_ready_mail_1/2.out`): 47 files written by message id (12 READYs, 4 seat-C STATUS, 2
  seat-C QUESTIONs, 6 Wednesday->C mails incl. the brief, 8 Seat B READYs, 8 Seat B STATUS/QUESTION/ACK, 7 Wednesday->B mails); TEXT_SHA256 per file;
  combined `mail_gate16C_ready.md` 242508 B sha256 210c5393fb673304aab67fe1672ab071012c14f20465a9e8aec4dd1e54660423, `NOT YET ARRIVED` count 0
  (`/usr/bin/grep -c -i`; positive control: the same grep for `READY FOR QA (Seat C 16th)` = 12+ lines).
- 19:13-19:20Z the twelve READYs, the four STATUS, the two QUESTIONs, Wednesday's five rulings, the brief's GROUPING + QUEUE sections READ WHOLE (the brief's
  QUEUE names the tampers, `from` counts and run dirs the round module carries).
- 19:2xZ `round16C.py` written: 12 PRs, 16 files (16 distinct), 16 canonical rows (14 run patches + 2 sections), 14 tampers over 8 files, +1256/-11 — the
  module's self-check (`python3 -c 'import round16C …'`: "PRs 12 files 16 distinct 16 canon rows 16 tampers 14 adds 1256 dels 11; per-PR adds/dels consistent;
  tamper files 8; auth pins ['1158','1160','1162','1163','1164','1165']").
- 19:1xZ the twelve heads' raw diffs read (`git diff --raw --abbrev=40 64ab10513 <head>` ×12 + `--numstat` + `rev-list --parents` + `rev-parse ^{tree}` + `log -1
  --format=%s`): every parent == 64ab10513, every tree == the READY's, every blob 40-hex == the READY's 12-hex prefix (the two KS-910 blobs read in full here:
  e33da9a44e112c64bd887e7b434c9a39b0ecc7eb / a1598f1163d730e15951f2e3449d6a8ea7d55ceb); the 8 tamper files' blobs identical at 64ab10513 / 581ed7fa1 / 9f0265eb0.
- 19:2xZ the 15 run patches' sha16 + byte counts + `input.json` tips read (`shasum -a 256`; `json.load`): 15/15 == the GROUPING; tips 581ed7fa1 ×10 / 9f0265eb0 ×5
  (KS-1185, KS-1199, KS-1188-F2, KS-1193-F1, KS-910); KS-910's `section_1.diff` == `section_1.diff.reanchored` (sha16 9d6dccc83f8020df, 828 B), `section_2.diff`
  ebb9a15ecfa32f88 (3166 B), `section_1.diff.as-written` 931 B (8907427113920a52); patch.diff b660b8c4b260f1f5 4097 B. The READY files under night/: all fifteen
  present (+ KS-1123's R15 / R16 CAST / DROPPED F2 rows, not this gate's).
- 19:22:53Z / 19:23:xxZ `shape_gate16C.py` runs 1-2 (`shape_1.out`, `shape_2.out`): develop tree == 87b4aa12d2eb; `rev-list --count 581ed7fa1..64ab10513` = 13;
  16 canonical rows exist, sha16 16/16, first hunk 16/16, +/- 16/16, `+++` path 16/16; the truncation class: F4 declared 97 vs 108, F2 97 vs 122, F1 124 vs 153
  (TRUNCATION); F1009b declared new=7 vs 16 `+` (MISCOUNT — rc 128 expected); KS-1180's patch SEVEN hunks; 15/15 fences == run patches (KS-910's fence == its
  non-applying patch.diff); the 16 targets: 11 ABSENT at develop, 5 at their GROUPING blobs with lines 80 / 188 / 292 / 185 / 646; 8/8 tamper files == item 0
  at all three tips; mfa.ts 426 lines, the :143 line text occurs 3× (:143 :166 :397), :138 `mfaRoutes.get('/status', authenticate(), …`; twelve READYs
  captured, PR number / head / branch / tree 12/12 == round16C; per head: parent==DEV, behind/ahead 0/1, tree ==, files == want, +/- ==, modes 100644, status
  A/M as pinned, every path under __tests__/, lines at head == RECOUNT 16/16, `-` lines 2 / 4 / 0 / 0 / 1 / 0 / 0 / 0 / 0 / 0 / 1 / 3 == declared; subjects 81 /
  86 / 81 / 87 / 91 / 87 / 88 / 77 / 91 / 92 / 84 / 90 chars ASCII, own key only, author the board login; union paths 16, overlaps NONE, name-status 11 A + 5 M,
  ∩ Seat B dirs NONE, ∩ Seat B paths NONE; the HELD ks1123 file ABSENT at develop and in every head; branches ASCII 74-95 chars, own key once, the three
  excised keys ABSENT, no archived key form; `scripts.test` = `vitest` in both lanes; hook :76 `grep '^Blockchain/Dev/'`; scripts/__tests__ holds 32 files
  (all `.test.sh`) at develop; pre_push_hook_base.test.sh :49-:51 = the three `-` lines of section_1 ("Leg 12 of the preflight now reaches this suite …").
- 19:24:43Z `predict_batch_scratch_gate16C.py` run 1 (`predict_batch_scratch_1.out`; clone `predict16C.p9o7o6_c`): (a) 14 run patches --recount --check rc 0 ×14,
  -R --recount rc 1 ×14; strict --check rc 0 ×13 + rc 128 `corrupt patch at line 10` (F1009b; -R rc 128); STRICT APPLY: F1009b rc 128 -> the develop blob
  f886bdadf706 / 80 survives; F4 rc 0 -> 4f68a823f31f / 97; F2 rc 0 -> 686a707056af / 97; F1 rc 0 -> 610c209861d1 / 124 (the seat's item-0 strict blobs 3/3);
  strict == recount on the other ten; RECOUNT APPLY -> the RECOUNT column 14/14 with line counts; KS-910's two sections strict rc 0 / -R rc 1 -> e33da9a44e11 /
  646 and a1598f1163d7 / 58; KS-910's patch.diff strict rc 1 AND --recount rc 1 (`patch failed: …pre_push_hook_base.test.sh`); nonexistent-patch rc 128; per-PR
  trees 12/12 == the head trees, final blobs + lines 16/16; KS-1188 reverse + seed-16 shuffle (F1a F2 F1b) same tree; KS-1193 and KS-910 reverse same; the
  all-15 in forward / reverse / seed-16 shuffle -> `4817a9c2ea2334b89395c4faa588312cfd609550` ×3 == the seat's; shortstat `16 files changed, 1256 insertions(+),
  11 deletions(-)`, name-status 11 A + 5 M; every ALL12 path == its RECOUNT blob 16/16; the HELD file ABSENT in ALL12; the thirteen-PR tree 48528fa3c355 IS in
  the shared store and differs from ALL12 on exactly `ks1123-api-gateway-verify-an-empty-string.test.ts` (17 files +1471/-11 over develop); read-tree back
  -> 87b4aa12d2eb; (b) twelve heads alone over develop by real merge-tree both orders = their head trees = the canonical-apply trees 12/12, parent==DEV 12/12;
  chained in FOUR orders -> `4817a9c2ea23…` ×4; every PR path in ALL carries its head blob; each head tree != ALL; (c) develop UNMOVED; newdev_tree.txt
  written (DEV_NOW 64ab10513, ALL12_OVER_NEW 4817a9c2ea23); empty-repo numstat rc 128; count-objects byte-identical; porcelain 0 / worktrees 257 / for-each-ref 1197.
- 19:26:00Z `gh_pr_reads_gate16C.py` (`gh_pr_reads_1.out`): 39 open PRs; twelve PRs head == READY == round16C, base develop@64ab10513, open, mergeable True /
  `unstable`, 1 commit each, author kksecura, created 17:03:56Z … 19:07:04Z; closing 0/0/0 ×12; completeness 0/1/0 on #1158 and #1160 ("a completeness cell"
  in the body — the model's own wording); body Refs == [own] ×12, commit Refs == [own] ×12; titles == round16C 12/12, ASCII; branches == round16C 12/12,
  ASCII, the excised keys absent 3/3; files API == the pinned paths 12/12, `outside __tests__: []` ×12, additions / deletions == the READYs 12/12, status
  modified ×5 / added ×11; no archived / content / foreign key in title / branch / subject; every body's KS keys = {own, KS-1201, KS-256}; every body carries
  `TS18046` ×1 (the round paragraph names the held PR by description), `LOCK TAKEN` ×1, `red-first` (×1; ×5 on #1166), `TRUNCATION` on #1152 / #1163 / #1164,
  `45 passed` on #1166, `anchor-ambiguity` on #1163; compare develop...head merge_base 64ab10513 ahead 1 behind 0 files 1/1/1/1/1/1/1/1/3/2/1/2; files API
  union 16; ruleset 18499832 `require-pr-gates` active, updated 2026-09-10, rules deletion / non_fast_forward / pull_request (required_approving_review_count 0,
  require_extra_approval_for_unattributed_changes True), conditions develop + main; Seat B's eight PRs: head == captured READY 8/8, base 64ab10513, kksecura,
  created 16:59:28Z … 18:29:29Z, namespace `feature/ks-<key>-…-r15-…-1` 8/8, ∩ our 16 paths NONE, ∩ our 8 tamper files NONE, every path under Seat B's four
  dirs; the HELD KS-1171 branch ABSENT at origin; no `feature/ks-1123-*` r15 branch at origin; open-PR hits 0; controls merged #1009 ∩ our 16 -> {ks864c…},
  merged #1007 ∩ our 8 tamper files -> {system-status.ts}, merged #1130 ∩ our 16 -> ∅; PR-number traps: #855 (KS-854) / #864 (KS-916) / #910 (KS-1013) / #1123
  (KS-1275) closed, other tickets'; #944 / #1180 / #1185 / #1188 / #1193 / #1199 / #1217 / #1237 404; the window 1147-1166 all open kksecura, #1167 404.
- 19:28:30Z `linear_reads_gate16C.py` (`linear_reads_1.out`; `grep -c lin_api` = 0; the file asserts no `mutation`): all twelve own tickets In Progress on the board
  login, archivedAt None, attachments {own PR contributes} (+ #1007 #1009 #1064 #1073 on KS-864; #1029 on KS-1180; #1146 on KS-1156), comments 6 / 2 / 0 / 0 /
  1 / 0 / 0 / 0 / 0 / 0 / 0 / 0 == the READYs; branchNames: the three LIVE foreign keys ks-1183 / ks-999 / ks-1018 present in Linear's field (the seat excised
  them from the refs), the hyphenless ks1073 / ks1072 / ks1204 / ks1050 forms present; bot walks (actor GitHub) KS-864 17:04:07Z (+ an earlier walk
  2026-09-19T04:28:51Z on #1073 and a manual move back 05:32:55Z by the board login), KS-1185 17:29:38Z, KS-1199 17:42:39Z, KS-1237 17:56:09Z, KS-855 18:09:51Z,
  KS-944 18:23:41Z, KS-1188 18:43:43Z, KS-1193 18:51:55Z, KS-1217 18:59:31Z, KS-910 19:07:15Z; KS-1180 (walked 2026-09-17 on #1029) and KS-1156 (13:34:51Z on
  #1146) unchanged; attachmentsForURL pull/N == [own, contributes] 12/12; KS-1123 (HELD) Backlog, #1002 only, walked on #1002 2026-09-16 and moved back the
  same day by the board login; Seat B's nine keys: eight In Progress with their own PR (+#874 on KS-928), KS-1171 Backlog 0 attachments, KS-975 assigned to the
  board login; attachmentsForURL pull/1147…1161 == Seat B's own keys 8/8; namespace KS-1147 … KS-1167 all exist: KS-1150 In Progress #987, KS-1151 Done
  ARCHIVED, KS-1152 In Progress #1143, KS-1153 In Progress #1056, KS-1156 In Progress {#1162, #1146}, KS-1158 In Progress #1153, KS-1165 In Progress {#1003,
  #1001}, KS-1166 / KS-1167 Done ARCHIVED, the rest Backlog no links; the 24 archived keys all archivedAt set; the 14 content keys as the READYs list them;
  KS-485 63 / KS-772 26 comments; controls pull/1146 -> {KS-1156}, pull/1029 -> {KS-1180}, pull/1009 -> {KS-864}, pull/1002 -> {KS-1123}, pull/1129 -> [],
  pull/1167 -> [].
- 19:3xZ the seat's record folder listed READ-ONLY (`ls`): raise/ (the twelve KS-<key>-lock.out / -push.* / -snapshot.out / -stubs.txt; attrib17.json +
  attrib17.retro.json (three rows c1-c4 true, controls c2 / c3 false); the ks1123 records; the `.run1-loadintermittent` copies for ks1156 / ks1188 / ks1193 /
  ks1217; ks944-census.run1-falsecover-STOP.json; the tooling + its pre-fix copies), boot/, mail/ (out-01..16), tickets/, gate/; KS-1199-lock.out read: five
  `lock HELD by other` polls on Seat B's ks-1158 window then `LOCK TAKEN … pid 68501` 17:35:51Z, `RELEASED` 17:41:46Z; `worktrees/.push-lock-16/` ABSENT
  (`ls -la worktrees/ | grep push-lock` empty — the seat's "lock FREE"); the s-c16-ks1123 worktree carries `HOLD-PR2-NOT-PUSHED-wednesday-answer.txt`; the
  s-c16-ks1199 worktree carries no marker (the series-stop marker is gone). The vault daily note was NOT read (a Wednesday-vault file; the seat's S1 record
  copies sit in its boot/).
- 19:3x-19:4xZ the prompt's three draft parts written (part1 335 lines / part2 421 / part3 341); `fill_prompt_gate16C.py` runs 1-3 (`fill_prompt_1..3.out`):
  ls-remote in the same action (25 refs, 12/12 AGREE among origin pull/head, branch, round16C and the READY), tokens substituted (__DEV__ ×6, __ALL12__ ×8,
  __N* / __H* / __TS* as counted), no residual, first line `ultrathink`, no PENDING — **prompt `2026-09-22_secuura-batch1148-1166.prompt.txt` 1097 lines,
  153090 B, sha256 cb537771b382e22702d2b44cc1550d9173a830e36c31943d68a92a6546077885**; report dir `2026-09-22-batch1148-1166-r1`; subject prefix
  `[QA -> Wednesday] BATCH GATE #1148-#1166 (twelve PRs; tier 2 floor, tier 1 = #1158, #1160, #1162, #1163, #1164, #1165: Seat C 16th test-only pins) —`;
  GO string present.
- 19:4xZ `gen_launcher_gate16C.py` runs 1-3 (`gen_launcher.run1..3.out`; S3): pins re-read at origin (develop 64ab10513 = the pin, 12 pull heads + 12 branches
  OK, the ks-1123 r15 glob NOTHING); the move 0 paths; per head parent == 64ab10513, behind/ahead 0/1, tree == pin, files == pinned, +/- ==, modes 100644,
  every path __tests__/; union 16, overlaps none; the 16 (develop blob | ABSENT) values agree at the parent and the current develop; 38 unchanged-read paths
  same blob at the parent, the current develop and every head; tree-hash control -> the parent tree; compose over the parent == each head tree 12/12;
  compose(the 16) over the parent AND over the current develop == 4817a9c2ea23…; per-PR trees == predict 12/12; BOTH 189 tokens in BOTH the capture and
  the prompt; by-name 114 keywords across 12 items + the closing; output controls all matched (`"ABSENT": DV` 11, ` own"` 16, the twelve heads ×1, the
  subject ×1, `PR #1148 is KS-864.` ×3, the GO string ×1); heredoc parity PY 0 / 10-10, PYJ 0 / 115-115; `bash -n` rc 0 -> **launcher
  `launch_qa_secuura_batch1148-1166.sh` 562 lines, mode 755, sha256 4c9d555ca4a8a56eec51293d2f04a1ed5ab7d08c03b17058f4ecc01510bec011**.
- 19:50:01Z-19:51:11Z the launcher's `--check` (`launcher_check_1.out`): **rc 0** — twelve heads on origin; twelve compares merge_base 64ab10513 / ahead 1 /
  behind 0 / files 1/1/1/1/1/1/1/1/3/2/1/2; develop judged by content over 54 paths = the pin; every grep passed.
- 19:51:55Z `launcher_controls_gate16C.sh` STARTED in the background (`launcher_check_controls.out`): A rc 4, B rc 3, **C_wrong_head_last rc 6 (a wrong sha
  refuses)**, D_curdev_old_parent rc 18, E_curdev_is_1148_head rc 19 (LANDED) OK at the time of this report; the ladder controls F-T + the positive follow
  (~20 min) — read the "controls end" line (0 MISMATCH expected). See section 8 for the final line.
- `repin_and_launch_gate16C.sh` written from gate15's (pins read FROM the launcher; `bash -n` rc 0; the sed dry-read prints develop 64ab10513 + the twelve
  `n:head:branch` rows + the prompt path; NOT run).

## 2. Artefacts produced
- **Prompt** — three draft parts assembled by `fill_prompt_gate16C.py` (first line `ultrathink`): framing (TWELVE PRs, THREE lanes, ZERO product bytes,
  TIER 2 floor + TIER 1 on the six auth pins, a product byte anywhere = NO GO on that PR); the LEADS (the seat's F1-F4, F-COVER-1123, F-FALSECOVER-944, F-45,
  the auth REPORT set, S1-S3, the tally slip, the bodies lint, the typecheck rows, the series stop / relaunch, the bot walks, the ks949 timeouts, the ALLOW
  rows, the PR-number traps); the NAMESPACE NOTE (the even / odd split, the KS-1147…KS-1167 tickets, KS-1156 / KS-1158 / KS-1165 cutting the other way, the
  twelve `PR #N is KS-x.` sentences, the multi-file PRs, the three excisions, the kept hyphenless forms, the other READY_* files, content keys in file names);
  the per-PR table (twelve entries with canonicals, rc rows, blobs, cells, tampers with scope anchors and positive controls, lane counts, census, lock rows,
  Linear history, tier, the seat-specific items — the SEVEN hunks, the delta -1, the anchor-ambiguity, the completeness cells, the underscore branch, the
  R-C2 title, the modify-in-place +0, the bash red-first / 45th suite); TIER PER PR (twelve lines, six TIER 1), round 1 of 2, time-box 240 min, the budget
  order; MERGE AUTHORITY (targets17 / merge17, MG-1 1/1/1/1/1/1/1/1/3/2/1/2 = 16, MG-2 EXERCISED on three lines, MG-3 key sets, `--pair-blob` unused, all
  twelve tickets stay, the ten bot walks + the two already-there, KS-1237 assigned); THE SHAPE (the heads' parent, develop unmoved, the twelve heads and
  branches, per-PR trees, ALL12 and the thirteen-PR superset with the api-gateway 716 -> 710 arithmetic, Seat B's eight paths, canonical identity with the
  recount class + the section rows + the non-applying patch.diff, the older tips, the 14 tampers over 8 files, the open-PR sweep); the sources (the READYs
  by filename, the STATUS / QUESTION mails, Wednesday's five rulings, the brief, the seat's record folder file by file, the fifteen READY_* files, the run
  dirs, the SIBLING GATE if present, PRIOR / EARLIER / OLDER reports, the Linear keys, the handover, Seat B's record for BY-NAME 3 / 9 / 10); worktree /
  history / checkout / lock-directory rules; farming per ENTRY (two vitest lanes; the two bash suites in the gate's own clone after reading their headers;
  the 44/45 corpus NOT run); Postgres isolation + CENSUS RULE v2 (api-gateway ALLOW STOP; auth REPORT; bash n/a) + listeners :4003 / :4004 / :4005 / :6000;
  the S3 kill + kills by ancestry; NOT-TESTED items; TWELVE by-name items exactly as commissioned; the standing rules; per-PR requirements; suites on the
  twelve-PR tree; CARRY-FORWARD (the prior rows named, four cross-checks); hygiene (incl. the count == 3 plant for F1A); the report dir; the NOT-PINNED
  candidate rows (LEGCOMMENTWORDINGONLY, F1AANCHORAMBIGUITY, COMPLETENESSCELL, AUTHGUARDS5S, ALLOWSETTHREEROWS — records, no cover row expected); the
  TWELVE-line verdict; the MERGE ADDENDUM line format with the sixteen blobs and modes (three comma-separated lines); WRITE report.md BEFORE THE MAIL; the
  exact subject; the GO string.
- **Launcher** — generated by `gen_launcher_gate16C.py` (above). Pins: develop 64ab10513 + every head by branch AND refs/pull/N/head (exit 6); compare per PR
  merge_base 64ab10513 / ahead 1 / behind 0 / files (exit 10); develop judged by CONTENT over 54 paths (16 targets with LANDED detection; 38 unchanged-read);
  GUARDED on a move: api-gateway / auth src + config, packages/shared, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs; the grep ladder
  7/15/8/9/20/12/11/14/17/22/23/24/25/26/27/28/29/30/31/32/33 + 34; overrides `QAB1148_*` refuse at launch (16); TTY (21); pane `QA/Secuura-batch1148`.
- `repin_and_launch_gate16C.sh` (NOT run), `launcher_controls_gate16C.sh` (running in the background at this report's write), `README.md`, this report,
  `round16C.py`, the capture / inbox / shape / predict / gh / linear scripts and their outputs (section 1).

## 3. LEADS for the gate (claims to grade; the drafter's re-derivation disagrees with the seat's VALUES nowhere)
1. TIER: the six auth pins are TIER 1 by the commission (the seat proposed tier 2 and named them; Wednesday's Q4 said expect tier 1) — the prompt pins
   them; the api-gateway five and the bash one stay at the floor.
2. THE RECOUNT CLASS — F1009b strict rc 128 `corrupt patch at line 10` and the strict APPLY writes NOTHING (the develop blob survives); F4 / F2 / F1 strict
   rc 0 with SHORT files 97 / 97 / 124 = the seat's item-0 blobs 4f68a823f31f / 686a707056af / 610c209861d1 (reproduced 3/3); the other ten strict == recount.
3. KS-910 — its canonical is the two SECTION files (strict rc 0 each, either order -> one tree); its patch.diff / the READY fence (b660b8c4b260f1f5, 4097 B —
   the READY header says 4093) does NOT apply: strict rc 1 AND --recount rc 1 (the brief's BLUF 4 and the seat's "neither applies" reproduced); the checker
   REANCHORED section_1 at :49 (the model's header said -46,9; the `.as-written` copy is 931 B vs 828 B).
4. KS-1188-F1A — the `from` line occurs 3× in mfa.ts (:143 :166 :397; drafter count 3); :138 is `mfaRoutes.get('/status', authenticate(), …`.
5. TYPECHECK — ks1073 delta -1 (the develop file carries one TS18046; the patch removes it); the held ks1123 +1 (not this gate).
6. THE ALLOW SET — the seat's census ATTRIBUTES the 13th's three rows to `ks1072-the-latest-anchor-selector-docume…` and `ks815-verification-router-guards-its-own…`
   (the 15th's carried set said "unattributed" for anchoring:4005 on the originate lane — a different lane); the two named files exist at develop.
7. A prior auth REPORT set EXISTS (`raise/net/auth-baseline-report.json.14th-carried`, every list empty) — against the brief's "no set yet" (Wednesday's Q7
   wording "a FIRST reading"); the seat's own finding.
8. F-FALSECOVER-944 — the instrument read three ks949 timeout cells (5002-5266 ms) as develop cover; the re-read rule was coded mid-round and fired on four
   later PRs (ks1156, ks1188 F1a, ks1193 F1, ks1217 — their `.run1-loadintermittent` records) and cleared each time: is four-in-twelve a load signal on a box
   running two seats and a gate?
9. F-45 — KS-910's push ran 45 shell suites (its new suite in-hook as the 45th); the other eleven ran 44.
10. THE S3 CROSS-SEAT KILL — Seat B's ready_send WRAPPER shell (57699) SIGTERMed by this seat's basename `ps | grep | head -1`; Seat B's 57702 survived;
    the fix: kills by ancestry of pid 53817 — grade every later kill in the seat's records.
11. THE SERIES STOP at ks1199 — an untracked marker in s-c16-ks1199 (now gone) made push17.sh refuse before any snapshot; KS-1199-lock.out shows five polls
    on Seat B's ks-1158 window then TAKEN 17:35:51Z; the stop cut no window.
12. THE EIGHT SEAT B ATTRIBUTIONS — three retro-verified (attrib17.retro.json, two failing controls) + five live (attrib17.json); the asymmetry: Seat B owed
    attributions only for KS-1180 / KS-1185 (in its 20-key content set), this seat owed eight (its 47-key guard held all nine of Seat B's keys).
13. TWENTY LOCK WINDOWS on one `.git` (12 + 8) with zero overlap — the READYs' rows on both sides; the seat's commit window 16:47:37Z-41Z and its 31 s batch
    window (npm ci inside — "I will not hold a window over deps again").
14. THE BODIES — "a completeness cell" wording on #1158 / #1160 hit the completeness detector (the model's own guard); every body carries `TS18046` in its
    round paragraph (the held PR by description, never its key — the S7 shape avoided).
15. KS-864's history — walked 2026-09-19T04:28:51Z on #1073, moved back 05:32:55Z by the board login, walked again 17:04:07Z on #1148; KS-1123 (HELD) the
    same shape on #1002 / 2026-09-16.
16. SUBJECTS 77-92 chars ASCII (KS-1193's exactly 92 — the ceiling); KS-855's branch carries `available_scopes` with an underscore (Linear's own form; 91 chars).
17. The api-gateway count on the TWELVE-PR tree should be 710 (716 - the held file's 6) and auth 818 unchanged — arithmetic from the READYs, never measured
    by anyone on that tree (the seat ran suites on the thirteen-PR tree only).
18. KS-1217's +0 — a modify-in-place: the pre-patch cell stays GREEN under the tamper (the ticket's claim) and the post-patch cell reds.
19. Seat B's #1155 head ref (five tags, 138 chars) and this seat's #1154 tail `-r15-1` — do both seats' namespace regexes admit both shapes?
20. The vault-note S1 — a VAULT event (restored byte-exact per the seat); the drafter did not read the vault note (NOT MEASURED).

## 5. NOT MEASURED by the drafter (named, not asserted)
- Any suite, tsc, eslint, typecheck or census run — the drafter ran no test (697/697, 786/786, the per-PR lane counts, 716/716 / 818/818 on the thirteen-PR
  tree, tsc 0 ×2, eslint 0/0 ×14, the cells, the census sets, the bash 4/4 + 28/28 + red-first 2/2) are carried as the seat's claims. The 710 on the twelve-PR
  tree is the drafter's arithmetic.
- The tampers — not planted by the drafter; the `from` texts, scope anchors and red sets are the seat's / the brief's (only the mfa.ts count 3 and the :138
  scope line were read).
- The live PR bodies' full text beyond the detectors / substrings (bodies never printed); the seat's body records under raise/ (listed, not read except one
  grep for `TS18046` on ks864-body.md :78).
- The seat's HANDOVER / RECORD.md / attrib17.json (the five live rows) / series-run*.out / the push logs — named, not read (attrib17.retro.json head read;
  KS-1199-lock.out read).
- The vault daily note (`Notes (MASTER)/daily/2026-09-22.md`) — not read; the seat's S1 record copies in its boot/ not read.
- The two prior report dirs' NOT-PINNED rows — carried by name from the gate16B prompt; not re-read this session.
- The launcher controls' final line (running at this report's write — section 8).
- Whether the sibling gate16B has launched or reported (its dir was read for scripts only; no report dir `2026-09-22-batch1147-1161-r1` existed at the
  drafter's `ls` 19:3xZ).
- The DKIM / inbox discriminator on the GO (the drafter sends no mail).

## 6. Checkout counts AFTER (read verbs only throughout) — see `checkout_counts_after.txt` (written at the drafter's close; section 8).

## 7. The launcher's controls — `launcher_controls_gate16C.sh` (A-T + positive; ~20 min; started 19:51:55Z in the background; each control on a COPY of the
   prompt or a QAB1148_* override; control F on a launcher COPY with #1150's compare line edited to behind=1).

## 8. Final state — see the addendum at the end of this file (written when the controls finish).

## 8. Final state (addendum, 2026-09-21T20:20Z UTC = 06:20 AEST)
- **Prompt** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1148-1166.prompt.txt` — 1097 lines, 153090 B,
  sha256 `cb537771b382e22702d2b44cc1550d9173a830e36c31943d68a92a6546077885` (`wc -l`; `shasum -a 256`; fill_prompt_3.out). Every head in it was read
  from origin in the same action that wrote it (fill_prompt's `ls-remote` 19:44:11Z, 25 refs, 12/12 AGREE with round16C and the READYs).
- **Launcher** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1148-1166.sh` — 562 lines, mode 755,
  sha256 `4c9d555ca4a8a56eec51293d2f04a1ed5ab7d08c03b17058f4ecc01510bec011`; `--check` rc 0 (`launcher_check_1.out` 19:50:01Z-19:51:11Z) and rc 0 again
  as the controls' POSITIVE at 20:17:31Z-20:19:48Z.
- **Controls** (`launcher_controls_gate16C.sh`, `launcher_check_controls.out`, 19:51:55Z-20:19:48Z): **21 OK / 0 MISMATCH** — A missing prompt 4 · B
  brief absent 3 · **C wrong head (last PR) 6** · D develop at the old parent 18 · E develop at #1148's head 19 (LANDED) · F compare behind=1 on a launcher
  copy 10 · G no thinking directive 8 · H namespace sentence reworded 32 · I #1158 demoted to tier 2 7 · J MG-2 phrase reworded 25 · K RULE WHETHER IT
  BLOCKS reworded 30 · L by-name item 9 reworded 33 · M subject prefix shortened 23 · N non-TTY launch 21 · O BOTH token reworded 30 · P GATEWAY_URL
  loopback reworded 31 · Q seat worktree reworded 28 · R :6000 lsof reworded 29 · S PARTIAL marker planted 34 · T a head altered in the prompt 20 ·
  POSITIVE 0. Controls dir `controls_gate16C.4VoYAp/` (the prompt copies + each control's .out).
- **Checkout counts AFTER** (`checkout_counts_after.txt` 19:58:30Z vs BEFORE 19:12:25Z): porcelain non-untracked 0 -> 0; porcelain total 17 -> 17;
  `.git/worktrees` 257 -> 257; for-each-ref 1197 -> 1197; count-objects 9064 / 101422 / 47 -> the same; .git/config sha256 identical; HEAD `develop`
  581ed7fa1 unchanged; `diff` of the two files (dates excluded) rc 0. Origin develop 64ab10513 at the close; the push-lock dir ABSENT.
- Network summary: `git ls-remote` (drafter ×4 + the launcher's own under --check / the 21 controls), GitHub GET (pulls / files / commits / compare /
  contents / rulesets), AgentMail GET (list + by id), Linear GraphQL query. No fetch, no mail, no tap, no Linear write, nothing launched, no
  `inbox_routing.conf` write, no write under `!CODING/`, no port connected by hand, no key printed, nothing written into the gate16B dir.
