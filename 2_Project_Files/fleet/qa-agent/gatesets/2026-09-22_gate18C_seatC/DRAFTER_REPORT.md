# DRAFTER REPORT — batch gate over Seat C 18th's SIX PRs (#1167 #1168 #1169 #1171 #1173 #1175; TIER 1 on #1167 KS-947 + the three code_patch PRs #1171 KS-1231 / #1173 KS-1246 / #1175 KS-1257, TIER 2 on #1168 KS-1123 / #1169 KS-1192; round 1 of 2)

Drafter: the SECOND gate-drafter subagent on this commission (under Wednesday, the 11:0x seat of 2026-09-22). Started 2026-09-22T01:13:31Z (UTC,
`date -u`; = 11:13 AEST). A FIRST drafter died on an API 529 at ~10:5x AEST (00:5xZ) after its captures (00:39Z-00:43Z), shape (00:47Z-00:48Z) and
predict (00:50Z) runs; its artefacts are kept beside and were READ (capture_ready_mail_1/2.out, shape_1/2.out, predict_batch_scratch_1/2.out,
lsremote_1.out, checkout_counts_before.txt, round18C.py, the three scripts) — every pin was RE-READ from origin by this drafter in the same action it
was written (lsremote_2.out 01:13:31Z; fill_prompt_3.out's ls-remote 01:49:12Z; the generator's ls-remote 01:49:2xZ; the launcher's own under
--check 01:49:55Z). Both commissions + the gate16C README / DRAFTER_REPORT / scripts / prompt drafts / launcher + the gate16B commission + the
gate18B commission (READ-ONLY, for the sibling's names) read whole before the first write. Every number below names its instrument and its file.

## 0. Constraints honoured
- No `cd`; literal absolute paths; `git -C`; heredocs `<<'EOF'`; rc on its own line; nothing deleted or renamed (`.pre-HHMM-*` COPIES beside; the
  fill script and the generator take a COPY for their backups, never a rename — a deliberate departure from the 16C scripts' `os.replace`).
- Secuura checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` READ-ONLY (read verbs only: `ls-remote`, `show`, `cat-file`,
  `rev-parse`, `rev-list`, `diff`, `ls-tree`, `log`, `status`, `for-each-ref`, `count-objects`, `config --get`; `find`/`stat` over `.git/objects`
  for the loose-object buckets). Every write verb (apply, read-tree, write-tree, merge-tree, commit-tree, init) inside ONE `git clone --shared
  --no-checkout` scratch clone under THIS session's scratchpad
  (`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/003907dd-5b0e-44fc-ad57-43f54dd51893/scratchpad/predict18C.2r8y5_fu/clone`), from the
  script file `predict_batch_scratch_gate18C.py` whose FIRST act asserts its target is a scratchpad under
  `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/` (rc 9 otherwise — the negative control `predict_batch_scratch_ctrl_badtarget.out`: `/tmp`
  refused rc 9), `chdir`s into the clone after cloning and asserts `os.getcwd()` is under the scratchpad before EVERY git write verb (`assert_in_scratch`
  in `g()`; the fetch and the empty-repo init guarded too). `count-objects -v` byte-identical before/after (count 9416 / in-pack 101422 / packs 47 —
  `predict_batch_scratch_3.out` first and last lines; `checkout_counts_before_2.txt` vs `checkout_counts_after.txt`; `loose_objects_1.out`: 0 loose
  objects with an mtime after 01:14Z). No `git fetch` was needed — develop never moved.
- Network: `git ls-remote` ×4 (01:13:31Z; predict (c) 01:20Z; fill 01:42:09Z / 01:49:12Z; the generator 01:49:2xZ) + the launcher's own reads under
  `--check` and the controls; GitHub GET (pulls / files / commits / compare / contents / rulesets); AgentMail GET (list + by id); Linear GraphQL query
  (the file asserts no `mutation`). No mail sent, no pane tapped, no Linear write, nothing launched, no `inbox_routing.conf` write, no write under
  `!CODING/`, no port connected by hand, no key printed (`/usr/bin/grep -c -i -E 'ghp_|github_pat|lin_api'` over `gh_pr_reads_1.out` = 0; `lin_api`
  over `linear_reads_1.out` = 0). Datasec mail neither opened nor listed (the inbox listing filters on Seat B / Seat C / Blockchain subjects only).
  Nothing written into the gate18B dir (its COMMISSION.md read for the sibling's pane / report names only).

## 4. Drafter's own slips (recorded as they happen; FIRST in the final message)
S1 01:22:31Z — `gh_pr_reads_gate18C.py` prints, on each Seat B row, `base develop@8c2f7b3fd (== 3916eacd1: False)`: the GitHub PR `base.sha` is the
   base branch's CURRENT tip, not the PR's parent — the label was the wrong shape (the parent is the compare's `merge_base`, printed on the same
   line: 3916eacd1, ahead 1, behind 1 ×7). No value is wrong; the label is. Left as printed (the file is a record); named here.
S2 01:4xZ — `gen_launcher_gate18C.py` run 1 refused on four BOTH tokens: `x-ratelimit-max` (the READYs truncate the F4 title at 50 chars — the token
   sits only in the brief and the prompt), `TS18046` (the 16th's held-PR error; not in this seat's mails), `Blockchain-B` (the pane tag appears in the
   seat's lock.out files, not its mails) — all three DROPPED from the BOTH list (prompt-only); and `Refs KS-1246` WRAPPED across two prompt lines in
   PR 5's block (rejoined). Run 2 refused on four wrapped by-name phrases (`lsof -nP -iTCP:6000 -sTCP:LISTEN` in part 2; `` `lsof -nP -iTCP:<port>
   -sTCP:LISTEN` before / after every run ``, `grade present / absent + MONOTONIC`, `the SECOND PINS` in part 3 — rejoined). The gate15 / 16B / 16C
   drafters' wrap slip, repeated; the generator's line-wise check is the control that caught it before any file was written.
S3 01:49Z — run 3 refused on the pair-blob output control: I wanted the 40-hex PAIR blob TWICE in the launcher; it appears FOUR times (the exit-35
   header comment, the `PAIR_BLOB=` variable, the JUDGED map's LANDED entry for health.ts, the BOTH loop — the 40-hex form is in the BOTH list). Want
   corrected to 4; run 4 wrote.
S4 (a design note, not a fault) — `shape_gate18C.py`'s first patch had a doubled comma (`% len(R.SEATB_BRIEF_PATHS),,`) — a SyntaxError on run 3's
   first attempt, fixed before any output; the pre-patch copy `shape_gate18C.py.pre-1119-seatb7locks` is the first drafter's version.
S5 (an inherited label) — the prompt's lead (a) first said `(00:00:36Z-00:03:36Z? — READ the rows)` for PR 4's polls — a TYPED guess with a question
   mark; replaced by the READ instants `23:54:54Z-23:57:54Z, TAKEN 23:58:54Z at poll 5` (`raise/KS-1231-lock.out`) before the fill.

S6 02:08:47Z — THE FRESHENING (found at the close, by the counts-after control): `count-objects -v` is byte-identical before / after (9416 / 101422 /
   47) — but 186 loose objects in the SHARED store carry an mtime after 01:14Z (0 at my 01:18Z read): 95 at 01:20Z (= my predict run 3: the six head
   trees, the all-6 tree, the head blobs and the PAIR blob are among them — 165 trees + 21 blobs in all) and 91 at 01:25Z (NOT mine: my processes at
   01:22-01:26Z were GET / query scripts; the sibling gate18B drafter's `--shared` predict is the plausible writer — unproven). Cause: git FRESHENS
   (utime-touches) an existing loose object it finds in an ALTERNATE when a write verb produces the same object — a `--shared` clone's temp object
   dir does not prevent it. No new object, no byte of content changed, no ref — a METADATA write into the shared store's object files by the very
   method the commission mandates (and the first drafter's 00:50Z predict left the same 95-object bucket at 00:5xZ). Consequences: (i) lead (b)'s
   mtime buckets are NOT an attribution instrument (already caveated; the prompt now says the drafters' own runs freshened 95 each and warns the
   gate its clones will too); (ii) `count-objects` byte-identical stays the right control for CONTENT — it held; (iii) a future drafter who must not
   touch even mtimes would need a non-shared clone (a full copy), which the commission does not ask for. `loose_objects_2.out` (+ .rc) is the record;
   `freshened_oids.txt` the 186 oids.

## 1. Timeline (every value: instrument | file)
- 01:13:31Z `lsremote_2.out` (`git -C <checkout> ls-remote origin refs/heads/develop 'refs/pull/116[7-9]/head' 'refs/pull/117*/head' 'refs/heads/feature/ks-947-*' … 'refs/heads/feature/ks-1257-*'`, rc 0):
  develop 8c2f7b3fd; refs/pull/1167 4f2b87547 · 1168 e17efafa7 · 1169 9088a3509 · 1171 f17ec0af4 · 1173 611c9d504 · 1175 be3fb14b6 — all six == the
  commission's / Wednesday's 11:1x heads and == the six branches; Seat B's seven heads present (1170 3e9f7d7b7 · 1172 d74b04678 · 1174 e1dea649c · 1176
  8ced0d50b · 1177 13030ac59 · 1178 e48b90e74 · 1179 e62555dd0); the older `feature/ks-1123-ornith-verify-status-pins` a376756ab present (not this round's).
- 01:13:45Z `checkout_counts_before_2.txt`: porcelain non-untracked 0; porcelain total 17; `.git/worktrees` 272; for-each-ref 1223; count-objects count
  9416 / size 61660 / in-pack 101422 / packs 47 / prune-packable 435; .git/config sha256 6417b203accd…; HEAD `develop` 581ed7fa1. | `git status
  --porcelain | grep -v '^??' | wc -l`; `ls .git/worktrees | wc -l`; `for-each-ref | wc -l`; `count-objects -v`; `shasum -a 256 .git/config`;
  `rev-parse --abbrev-ref HEAD`. (The first drafter's 00:40:47Z read: the same count 9416, for-each-ref 1220 — three refs more at my read: Seat B's
  later pushes' tracking refs in its worktrees, a moving reading.)
- 01:1xZ `inbox_list_gate18C.py` (`inbox_list_2.out`, 200 messages listed): the six Seat C 18th READY subjects 23:37:46Z (PR 1) … 00:32:55Z (PR 6), the
  00:42:07Z HOLDING STATUS, the 22:55 / 23:26 STATUS mails, the 22:43 / 22:46 QUESTIONs; Seat B's SEVEN READYs 00:02:34Z … 01:05:17Z + its 01:08:36Z HOLD;
  nothing from Seat C after 00:42:07Z.
- 01:1xZ `capture_ready_mail_gate18C.py` run 3 (`capture_ready_mail_3.out`): idempotent — every earlier file "exists, not overwritten"; 4 NEW files:
  mail_seatB18_ready05_pr5_ks811.md, ready06_pr6_ks1188.md, ready07_pr7_ks1181.md, mail_seatB18_status_seat_b_18th_holding_seven_ready_1_0108.md; the
  combined `mail_gate18C_ready.md` rebuilt (137676 B; `NOT YET ARRIVED` count 0 by `/usr/bin/grep -c -i`; positive control: `READY FOR QA (Seat C 18th)`
  ≥ 6 lines).
- 01:1x-01:3xZ the six READYs, the three STATUS, the two QUESTION mails, Wednesday's plan ANSWER + tail ANSWER, the brief's BLUF / ITEM 0 / GROUPING /
  DROPPED / QUEUE, Seat B's HOLD (its lock-window table) READ WHOLE; Seat B's seven READYs read for heads / paths / tiers (`grep -o` over the
  captures).
- 01:18:22Z `loose_objects_1.out` (`find .git/objects -type f -regex '.*/[0-9a-f][0-9a-f]/[0-9a-f]*' -newermt … -exec stat -f %Sm …`, `TZ=UTC`, 10-min
  buckets): loose 9416 == `count-objects` count; buckets since 22:00Z: 22:0x 214 / 22:2x 18 / 22:3x 1 / 22:5x 56 / 23:2x 85 / 23:4x 190 / 00:5x 95;
  after 01:14Z: 0 (the control; the first run's `-newermt` used a non-ISO form bfs refused — re-run with ISO). THE ARITHMETIC DOES NOT CLOSE
  and the drafter says so: objects with an mtime before 22:00Z number 9416 - 659 = 8757, so the seat's 9197 (its 22:38Z read) / 9214 / 9215 (22:5xZ)
  cannot be reached by adding the later buckets (8757 + 214 + 18 + 1 + 56 = 9046 at 22:5xZ) — git FRESHENS an existing loose object's mtime when the
  same object is written again (a re-hash by any seat's tooling), so an mtime bucket counts re-touched OLD objects as well as new ones. The buckets
  are therefore a WEAK instrument for attribution; the +201 (9215 -> 9416) is the only firm delta, and reachability from the heads / octopi (the
  gate's lead (b)) is the right instrument. The 0-after-01:14Z control stands (no freshening or writing by this drafter).)
- 01:19Z `round18C.py` patched (`.pre-1119-seatb7` beside): SEATB SEVEN PRs (heads + 9 paths from the captures), SEATB_LOCKS (seven windows from the
  HOLD table), SEATC_OTHER_LOCKS (twelve windows from the STATUS mails + gate/*.lock.out reads), LOCK_POLLS 0/0/0/4/5/5, SEATB_ALL7, SEATB_GO, the
  sibling / report dirs — `round18C_selfcheck.out`: "PRs 6 files 11 distinct 10 canon rows 11 tampers 6 adds 1008 dels 15; per-PR adds/dels consistent
  True; SEATB 7 paths 9 distinct 9 locks 7 | C paths ∩ B paths: NONE | B under its dirs: True | C under AG: True; TIER1 ['1','4','5','6']".
- 01:20:04Z `shape_gate18C.py` run 3 (`shape_3.out`; `.pre-1119-seatb7locks` beside): develop tree == 04b05e093ad8, parent [3916eacd1], first-parent count
  1, the #1036 diff 50 files ∩ 10 paths NONE ∩ 2 tamper files NONE; 11 canonical rows: sha16 11/11, first hunk 11/11, +/- 11/11, `+++` path 11/11, the
  .opts line 2 == pin 8/8 (the ONE non-empty: ` --recount --ignore-whitespace`), declared new == actual on the NEW rows (215 / 144 / 196 / 108 / 136 —
  no truncation class); 7/7 READY fences == run patches; cat(s1,s2) == patch.diff 4/4; A4 red_first 2/4, 1/3, 1/4, 3/22 == pins 4/4, A4 titles == pins
  4/4, A5 0 failed ×4; run tips 64ab10513 ×6 / a1931d2f3 (KS-1257); the 10 targets: 5 ABSENT, 5 at their blobs / lines (99 / 1489 / 237 / 183 / 1555);
  the 2 tamper files == item 0 and identical at 3916eacd1 / 64ab10513 / a1931d2f3; the 5 existing targets identical at all four tips; `from` counts
  8 / 3 / 3 / 1 / 1 / 1 == pins, each at its line; index.ts 1279 lines, :991 `app.use('/api/auth/mfa', rateLimit({`, :1016 `app.use('/api/users/me/mfa',
  rateLimit({`; six READYs captured, PR number / head / branch / tree 6/6 == round18C; per head: parent==DEV, behind/ahead 0/1, tree ==, files == want,
  +/- ==, modes 100644, status A/M as pinned, outside-__tests__ == the PRODUCT set 6/6, nothing under services/auth/ 6/6, lines at head == pins 11/11,
  `-` lines 0 / 0 / 0 / 6 / 1 / 8 == declared; subjects 81 / 90 / 90 / 88 / 77 / 82 chars ASCII, own key only, author the board login; union paths 10, the
  ONE pair health.ts in #1171 + #1173, name-status 5 A + 6 M; ∩ Seat B dirs NONE, ∩ Seat B READY paths (ALL SEVEN, 9) NONE; branches ASCII 78-96 chars,
  own key once, `ks-733` ABSENT from #1167's, scanner NONE ×6, the withdrawn `threehunks` control reads `['ks-1257', 'ks-1']`; `scripts.test` = `vitest`;
  hook :76 `grep '^Blockchain/Dev/'`; scripts/__tests__ 33 `.test.sh`; the ks733 file's four cells at develop (:68 CONTROL, :78 NEGATIVE CONTROL, :84
  the users limiter, :90 PARITY); health.ts :45-:52 / :212-:215 (the two hunk sites) / :40 the TS2339 site; THE TWO-SEAT LOCK WINDOWS: 25 windows
  (this seat 6 pushes + 12 other; Seat B 7), pairwise overlaps NONE, every start ≥ the previous release True; the seat's lock polls per push (its
  KS-<key>-lock.out, `held by other` rows, case-insensitive): 0 / 0 / 0 / 4 / 5 / 5 == LOCK_POLLS 6/6, waited on ks-1118 / ks-1158 / ks-1265; `.push-lock-18`
  ABSENT; s-c18-* 7, s-b18-* 8, .git/worktrees 272.
- 01:20:42Z `predict_batch_scratch_gate18C.py` run 3 (`predict_batch_scratch_3.out`; `.pre-1120-cwdguard` beside; clone `predict18C.2r8y5_fu` in THIS
  session's scratchpad, `cwd now … | under the scratchpad: True`): (a) 11 canonicals strict --check rc 0 ×11, -R --check rc 1 ×11, --recount --check
  rc 0 ×11; STRICT APPLY -> the head blob + lines 11/11; the .opts row three ways == 772a70e4c193; --recount APPLY == strict 11/11; nonexistent-patch
  rc 128; per-PR trees 6/6 == the head trees, blobs + lines 11/11; #1171 reverse + seed-18 shuffle same tree, #1173 / #1175 reverse same; the all-6 (11
  rows) forward / reverse / seed-18 shuffle -> `52853c8bf6c4ff43585cdade61c637ff8cbaa5d0` ×3 == the seat's; shortstat `10 files changed, 1008
  insertions(+), 15 deletions(-)`, name-status 5 A + 5 M; every ALL6 path == its head blob EXCEPT health.ts == the PAIR blob ae6017a84cf7 / 255; read-tree
  back -> 04b05e093ad8; the health.ts pair (sections only) b82418e1c515 both orders; the 3-file PAIR a3becc4c37a9 both orders == the seat's; the trio
  1b956c660f7c ×3 == the seat's; (b) six heads alone over develop by real merge-tree both orders = their head trees = the canonical-apply trees 6/6,
  parent==DEV 6/6; chained in FOUR orders (1-6, 6-1, 3 5 6 4 1 2, 3 6 1 5 4 2) -> `52853c8bf6c4…` ×4; every non-pair path in ALL carries its head blob,
  health.ts the PAIR blob (two EXPECTED lines, no MISMATCH); each head tree != ALL; #1171 then #1173 == #1173 then #1171 == 1b956c660f7c with health.ts
  at the PAIR blob; #1173 alone: health.ts bca1d9500aa3; the seat's batch octopus c28f7a2f538c in the store, its tree == the all-6; (c) develop
  UNMOVED; newdev_tree.txt written (byte-identical to the first drafter's: `diff` rc 0); empty-repo numstat rc 128; temp object dir 112 objects;
  count-objects byte-identical; porcelain 0 / worktrees 272 / for-each-ref 1223.
- 01:22:31Z-01:23:29Z `gh_pr_reads_gate18C.py` (`gh_pr_reads_1.out`): 31 open PRs; six PRs head == READY == round18C, base develop@8c2f7b3fd, open,
  mergeable True / `unstable`, 1 commit each, author kksecura, created 23:34:26Z … 00:31:03Z; closing 0/0/0 ×6; completeness 0/0/0 ×6; body Refs ==
  [own] ×6, commit Refs == [own] ×6; titles == round18C 6/6, ASCII; branches == round18C 6/6, ASCII, scanner NONE ×6, tails f3f4b-1 / f3b-cast-1 /
  noquote-1 / parta-partb-1 / servicesbody-1 / settingsdefaults-1; commit subjects 81 / 90 / 90 / 88 / 77 / 82 ≤ 92 ASCII; files API == the pinned
  paths 6/6, outside-__tests__ == the PRODUCT set 6/6, nothing under services/auth/ 6/6, additions / deletions == the READYs 6/6, status modified ×6
  (in 4 PRs) / added ×5; no archived / content / foreign key in title / branch / subject; every body's KS keys = {own, KS-1201, KS-256}; every body
  carries `#1036` ×3 and `45 passed` ×1, `PREFLIGHT INCOMPLETE` / `12/15` / `SKIPPED` / `skips are not a pass` / `LOCK TAKEN` / `PROTOCOL-CLEAN` /
  `stubs=4` / `typecheck18` / `TS2322` / `netlog` / `:5432` ×1; the code_patch bodies carry `PRODUCT BYTES` ×1, `RED-FIRST` / `GREEN-AFTER` ×7 / ×5 / ×5,
  `A4` / `A5`; `tier 1` ×1 on four bodies, `tier 2` ×1 on two; NO body carries `--pair-blob`, `no-useless-assignment` or `EXCISED`; compare
  develop...head merge_base 8c2f7b3fd ahead 1 behind 0 files 1/1/1/4/2/2; files API union 10; ruleset 18499832 `require-pr-gates` active, updated
  2026-09-10, rules deletion / non_fast_forward / pull_request (required_approving_review_count 0, require_extra_approval_for_unattributed_changes
  True), conditions develop + main; #1036 closed / merged, merge_commit_sha == develop, head == 4b251997a, 50 files (29 locks + 20 manifests +
  audit-baseline.json), ∩ our 10 NONE, ∩ our 2 tamper files NONE; Seat B's SEVEN PRs: head == captured READY 7/7, open, kksecura, created 00:00:24Z …
  01:02:04Z, namespace `feature/ks-<key>-…-r16|r18-…-1` 7/7 (r18 on KS-1118 / KS-1158 / KS-1181), scanner NONE ×7, files == captured 7/7, ∩ our 10
  NONE ×7, ∩ our 2 tamper files NONE ×7, compare merge_base 3916eacd1 ahead 1 behind 1 files 1/1/2/2/1/1/1; Seat B pushed paths 9 (∩ NONE twice, every
  one under its dirs, none under api-gateway); open-PR hits 0; controls: index.ts <- merged #1108 (∩ tamper files {index.ts}), verification.ts <- #1035
  (∩ our 10 {verification.ts}), admin.ts <- #1045 ({ks1230 test, admin.ts}), health.ts <- #1037 ({health.ts}), the ks1230 test <- #1100, the ks733
  test's last subject carries no PR number (`KS-733: rate-limit /api/users/me/mfa at parity with /api/auth/mfa`); negative #1166 ∩ our 10 ∅; #1002 ∩
  our 10 {verification.ts} (a prior product edit on KS-1123's own ticket); PR-number traps: #947 OPEN (a dependabot chore), #1123 closed (KS-1275),
  #1192 / #1231 / #1246 / #1257 404; the window 1167-1179 all open kksecura on base 8c2f7b3fd, #1180 / #1181 404.
- 01:24:30Z-01:26:04Z `linear_reads_gate18C.py` (`linear_reads_1.out`; `grep -c lin_api` = 0; the file asserts no `mutation`): all six own tickets In
  Progress on the board login, archivedAt None, attachments {own PR contributes} (+ #1002 on KS-1123), comments 0 / 3 / 0 / 1 / 0 / 0 == the READYs;
  branchNames: KS-947's carries `ks-733` (the seat excised it from the ref), KS-1192's the hyphenless `ks871`; bot walks (actor GitHub) KS-947
  23:34:36Z, KS-1123 23:44:27Z (+ the 2026-09-16 walk on #1002 12:34:40Z and the manual move back 13:42:58Z by the board login), KS-1192 23:53:19Z,
  KS-1231 00:05:42Z, KS-1246 00:18:07Z, KS-1257 00:31:13Z; assignee changes KS-1246 / KS-1257 `None -> kamil.kreiser@secuura.ai` at 22:33:43Z, actor the
  board login; attachmentsForURL pull/N == [own, contributes] 6/6; Seat B's seven keys: all In Progress with their own PR (+ the 16th's #1149 / #1153
  / #1163 / #1159 on KS-1118 / KS-1158 / KS-1188 / KS-1181), KS-1188's / KS-1181's branchNames still carry `ks-999` / `ks-727`; attachmentsForURL
  pull/1170…1179 == Seat B's own keys 7/7; namespace KS-1167 … KS-1181 all exist (KS-1167 / KS-1169 / KS-1170 Done ARCHIVED; KS-1171 In Progress via
  #1176; KS-1172 / KS-1173 In Review #877 / #1059; KS-1175 In Progress #1116 / #1105; KS-1176 In Progress #1014; KS-1179 In Progress #1157; KS-1180 In
  Progress #1150 / #1029; KS-1181 In Progress #1179 / #1159; the rest Backlog no links); the 30 archived keys all archivedAt set; the 22 content keys as
  the READYs list them (KS-1285 Done NOT archived; KS-1227 Backlog 0 attachments); KS-256 In Progress, KS-1201 Backlog; KS-763 / KS-775 In Progress
  with #1036; KS-485 65 / KS-772 28 comments; controls pull/1036 -> {KS-763, KS-775}, pull/1002 -> {KS-1123}, pull/1035 -> {KS-1204}, pull/1045 ->
  {KS-1230}, pull/1129 -> [], pull/1180 -> []. (Three transient Linear HTTPErrors retried, all recovered.)
- 01:2xZ the seat's record folder listed READ-ONLY (`ls`): boot/ (53), raise/ (354), gate/ (59), mail/ (86), tickets/ (5), proof-synthetic/,
  `history.md.pre-hold-edit`; the six KS-<key>-lock.out files READ (the polls); commit18-lock.out / batch_build18-lock.out / gate/*.lock.out READ
  (the windows); attrib18.json READ (three rows c1-c4 true); measure18b.out tail READ (all-7 / pair / trio over the moved base, ALL OK, byte-identical
  9215 -> 9215); KS-1246-push.out's preflight lines glanced; `worktrees/.push-lock-18/` ABSENT; s-c18-* 7 / s-b18-* 8 worktrees; the HANDOVER files
  present (not read). The vault daily note NOT read.
- 01:3x-01:4xZ the prompt's three draft parts written (part1 ~290 lines / part2 ~330 / part3 ~330); `fill_prompt_gate18C.py` runs 1-3
  (`fill_prompt_1..3.out`): ls-remote in the same action (13 refs, 6/6 AGREE among origin pull/head, branch, round18C and the READY), tokens
  substituted (__DEV__ ×6, __ALL6__ ×7, __N* / __H* / __TS* as counted), no residual, first line `ultrathink`, no PENDING, no `deadbeef` — **prompt
  `2026-09-22_secuura-batch1167-1175.prompt.txt` 1141 lines, 158867 B, sha256 fcf6dc1a6f7fa1fa13e60ba56c38be5f875845f16264837f6526702acb6ab0b5**
  (run 4 — after the lead-(b) freshening caveat; runs 1-3 kept beside as `.pre-HHMMSS` COPIES; the launcher's sha is unchanged by a prompt edit); report dir `2026-09-22-batch1167-1175-r1`; subject prefix `[QA ->
  Wednesday] BATCH GATE #1167-#1175 (six PRs; tier 1 = #1167, #1171, #1173, #1175: Seat C 18th — KS-947 auth-surface pin + three code_patch product PRs;
  tier 2 = #1168, #1169) —`; GO string present; Seat B's GO string absent.
- 01:4xZ `gen_launcher_gate18C.py` runs 1-5 (`gen_launcher.run1..5.out`; S2 / S3; run 5 re-generated after the prompt's lead-(b) edit — identical launcher bytes): pins re-read at origin (develop 8c2f7b3fd = the pin, 6 pull heads + 6
  branches OK, the ks-1123 r15 glob NOTHING); the move 0 paths; per head parent == 8c2f7b3fd, behind/ahead 0/1, tree == pin, files == pinned, +/- ==,
  modes 100644, outside-__tests__ == the PRODUCT set; union 10, the ONE overlap (1171, 1173, health.ts) as wanted; the 10 (develop blob | ABSENT)
  values agree at the parent and the current develop; 32 unchanged-read paths same blob at the parent, the current develop and every head; tree-hash
  control -> the parent tree; compose over the parent == each head tree 6/6; compose(the 10 with health.ts at the PAIR blob) over the parent AND
  over the current develop == 52853c8bf6c4…; per-PR trees == predict 6/6; predict_batch_scratch_3.out's three + four orders + byte-identical + cwd
  guard asserted; BOTH 192 tokens in BOTH the capture and the prompt; by-name 128 keywords across 12 items + the closing; output controls all matched
  (`"ABSENT": DV` 5, ` own"` 11, `the PAIR (#1171 + #1173)"` 1, the six heads ×1, the subject ×1, `PR #1167 is KS-947.` ×3, the GO string ×1, the PAIR
  blob ×4); heredoc parity PY 0 / 10-10, PYJ 0 / 104-104; `bash -n` rc 0 (the tmp copy in the scratchpad) -> **launcher
  `launch_qa_secuura_batch1167-1175.sh` 543 lines, mode 755, sha256 cc8882bef7b931aaf68200e63b2304af5a6ca05467a58a8438cb0e67c6a08ea2**.
- 01:49:55Z-01:51:29Z the launcher's `--check` (`launcher_check_1.out`): **rc 0** — six heads on origin; six compares merge_base 8c2f7b3fd / ahead 1 /
  behind 0 / files 1/1/1/4/2/2; develop judged by content over 42 paths = the pin; every grep passed.
- 01:52:15Z `launcher_controls_gate18C.sh` STARTED in the background (`launcher_check_controls.out`, pid in `launcher_controls.start.txt`): A rc 4, B
  rc 3, **C_wrong_head_last rc 6 (a wrong sha refuses)**, D_curdev_old_parent_3916eacd1 rc 18, E_curdev_is_1167_head rc 19 (LANDED),
  **E2_curdev_is_1173_head_pair_second rc 19 (LANDED on the pair's second alone blob)** OK at the time of this report; the ladder controls F-U + the
  positive follow (~25 min) — read the "controls end" line (0 MISMATCH expected). See section 8 for the final line.
- `repin_and_launch_gate18C.sh` written from gate16C's (pins read FROM the launcher; `bash -n` rc 0; the sed dry-read prints develop 8c2f7b3fd + the
  six `n:head:branch` rows + the prompt path; the routing line `QA/Secuura-batch1167|coagent@agentmail.to|yes` ABSENT at the drafter's read (count 0;
  the batch1148 control 1); NOT run).

## 2. Artefacts produced
- **Prompt** — three draft parts assembled by `fill_prompt_gate18C.py` (first line `ultrathink`): framing (SIX PRs, ONE lane, PRODUCT bytes on exactly
  three paths, TIER 1 on FOUR incl. the code_patch RED/GREEN protocol, the health.ts PAIR and `--pair-blob`, the #1036 base); the LEADS (the seat's
  (1)-(6), S1, the engine slips, MG-10, the record-only writes, the walks, the assignments, the census, the PR-number traps; the drafter's own (a)
  the lock polls, (b) the loose objects, (c) the body without `--pair-blob`, (d) the rule-7 comment counts); the NAMESPACE NOTE (the consecutive
  / every-second numbers, Seat B's seven, the KS-1167…KS-1181 tickets, KS-1171 / KS-1173 / KS-1175 cutting the other way, the six `PR #N is KS-x.`
  sentences, the excision, the kept hyphenless forms, the ruled tail + the scanner control, the other READY_* files, content keys in file names /
  titles); the per-PR table (six entries with canonicals, sections, rc rows, blobs, cells, tampers with the anchor-ambiguity sites and the covers,
  the A4/A5 counts and titles, lane counts, typecheck rows incl. health.ts 1/1, eslint rows incl. the pre-existing warnings and the new one, census,
  lock rows with the polls, Linear history, tier, the seat-specific items); TIER PER PR (six lines, four TIER 1), round 1 of 2, time-box 240 min, the
  budget order (code_patch first); MERGE AUTHORITY (targets18.py / merge18b.py, MG-1 1/1/1/4/2/2 = 11 over 10, MG-2 EXERCISED on three lines, the
  PAIR rewrite via `--ruling`, MG-3 key sets incl. the KEY-FREE SHIPS-WITH lesson from the #1036 squash, the six DRY runs, all six tickets stay, the
  bot walks + the two assignments, the ONE hard merge-order constraint); THE SHAPE (the #1036 squash as the parent, the 50-file move ∩ ∅, the six
  heads and branches, per-PR trees, ALL6 with health.ts at the PAIR blob, the pair / trio / 1-file control trees, the brief's superseded trees, the
  seat's batch suites, Seat B's nine paths, canonical identity STRICT with the .opts row three ways and the no-truncation measurement, the older
  tips, the 6 tampers over 2 files with the batch re-plant, the open-PR sweep with the last-merged-PR controls and #1002's product edit); the
  sources (the READYs by filename, the STATUS / QUESTION mails, Wednesday's three mails, the brief, the seat's record folder file by file incl. the
  gate/ tooling and the #1036 round's records, the seven READY_* files, the run dirs, the SIBLING GATE, PRIOR / EARLIER / OLDER reports, the Linear
  keys, the handover, Seat B's record for BY-NAME 3 / 9 / 10); worktree / history / checkout / lock-directory rules incl. the cwd-guard rule for the
  gate's own scripts; farming per ENTRY (one vitest lane); Postgres isolation + CENSUS RULE v2 + the (b) ruling + the #1173 real-listener question;
  the kill-by-ancestry rule; the spec-conformance question on the three product changes; NOT-TESTED items incl. the served-gateway NOT TESTED, the
  unserved product changes, the #1036 merge not re-gated, and the CONTEXT RULE; TWELVE by-name items exactly as commissioned; the standing rules;
  per-PR requirements; suites on the all-6 tree; CARRY-FORWARD (the prior rows named incl. the sibling's MFASIBLINGSITES rows, four cross-checks);
  hygiene; the report dir; the NOT-PINNED candidate rows (PARITYCOVER, F3SKIPSIBLINGSITES, SECONDPINF2F3, HEALTHTS40TS2339, NOUSELESSASSIGNMENT77,
  REALLISTENERSINCELL, THREEHUNKSEACHNAMED, ALLOWSETTHREEROWS); the SIX-line verdict; the MERGE ADDENDUM line format with the eleven blobs and modes
  (three comma-separated lines; #1173's PAIR note); WRITE report.md BEFORE THE MAIL; the exact subject; the GO string.
- **Launcher** — generated by `gen_launcher_gate18C.py` (above). Pins: develop 8c2f7b3fd + every head by branch AND refs/pull/N/head (exit 6); compare
  per PR merge_base 8c2f7b3fd / ahead 1 / behind 0 / files 1/1/1/4/2/2 (exit 10); develop judged by CONTENT over 42 paths (10 targets with LANDED
  detection incl. the PAIR blob; 32 unchanged-read); GUARDED on a move: api-gateway / packages/shared src + config, scripts/, .githooks/, the Dev
  package.json + lock, eslint.config.mjs; the grep ladder 7/15/8/9/20/12/11/14/17/22/23/24/25/35/26/27/28/29/30/31/32/33 + 34; overrides
  `QAB1167_*` refuse at launch (16); TTY (21); pane `QA/Secuura-batch1167`.
- `repin_and_launch_gate18C.sh` (NOT run), `launcher_controls_gate18C.sh` (running in the background at this report's write), `README.md`, this
  report, `round18C.py` (patched), the capture / inbox / shape / predict (guarded) / gh / linear scripts and their outputs (section 1).

## 3. LEADS for the gate (claims to grade; the drafter's re-derivation disagrees with the seat's VALUES on ONE — (a))
1. (a) THE LOCK POLLS — the HOLDING STATUS's "PR 5 waited one poll and PR 6 five polls" vs the seat's own lock.out files: PR 4 FOUR polls
   (23:54:54Z-23:57:54Z on Seat B's ks-1118 window; TAKEN 23:58:54Z, two seconds after B's 23:58:52Z release), PR 5 FIVE (00:06:36Z-00:10:36Z on
   ks-1158; TAKEN 00:11:36Z), PR 6 FIVE (00:19:06Z-00:23:06Z on ks-1265; TAKEN 00:24:06Z) — a wording slip in the STATUS, no window cut (25 windows
   pairwise disjoint and monotonic as a set).
2. (b) THE LOOSE OBJECTS — 9215 (the seat's 22:55Z read) -> 9416 (00:40Z, 01:13Z): +201; mtime buckets 23:2xZ 85 / 23:4xZ 190 / 00:5xZ 95 — the two
   seats' commits and batch octopi (worktree commits land in the shared store by design); the six GO dry runs 00:37Z-00:38Z wrote NONE; 0 after
   01:14Z. The gate attributes by reachability from the thirteen heads + the two octopi (c28f7a2f538c, 5185c65cf) and names the unreachable count.
3. (c) #1173's BODY does not carry `--pair-blob` (the READY, the STATUS and the HOLD do) — would a merging seat reading the body alone know? The
   addendum's alone blob is BY CONSTRUCTION; the seat's targets18.py rewrites from the `--ruling` text.
4. (d) KS-485 / KS-772 comments 65 / 28 (the 16C gate read 63 / 26 at 19:28Z): two rule-7 posts since — the 16th's / 17th's GO rounds; the gate names
   them from the tickets, never posts.
5. THE SECOND PINS — KS-947 F4AUTH / F4USERS by the file's own PARITY cell (:90 at develop); KS-1123 F2 / F3 by the ks1123-f2 (two cells) / ks1123-f3
   (one cell) files: the seat flagged them FOR THE GATE TO WEIGH; the 16th recorded the same on the held F3b (F-COVER-1123). Are the new cells a
   different witness (the PUBLISHED x-ratelimit-max vs the CONFIGURED max; a cast-typed body vs the earlier untyped one) or NOT-PINNED-FOR-ITS-OWN-FILE?
6. THE STRICT CLASS — no truncation / rc-128 row this round (11/11 strict == recount == head); the ONE .opts row (Part B section 1) equal three ways
   — what did the checker "miscount" (hunk `@@ -45,8 +45,25 @@`, +20/-3 over 8 old lines = 25 new: consistent by the drafter's arithmetic)?
7. verification.ts is BOTH KS-1123's tamper file (F2 :746, F3 :624) AND KS-1231 Part A's product file (:1210) — the seat's batch re-plant at the all-6
   tree (plant sha ≠ the checker's by construction, reds EXACT) — reproduce both readings; the tamper sites and the hunk site do not overlap (drafter:
   :624 / :746 vs :1210-:1243).
8. health.ts:40 `req.user?.role` — ONE in-file error under the temp tsconfig at BOTH head and develop (TS2339) while the service's tsc reads 0: which
   program is right, and is a pre-existing type error on a product file a finding on the PRODUCT?
9. #1173's RED-FIRST run 1 TIMEOUT under load 17 (8.7 s STACK_TRACE_ERROR vs the checker's 185 ms AssertionError) — the code-stage re-read allowance
   coded mid-round: does a re-read rule on a RED-FIRST risk masking a product hunk that does not fix the cell? The cell boots real HTTP listeners —
   which ports?
10. eslint: verification.ts 5 / admin.ts 16 warnings pre-existing (the seat's develop control); ONE NEW `no-useless-assignment` :77 in #1173's new test;
    ONE warning on #1169's new file (rule unnamed in the READY) — is either an error under the repo's eslint.config.mjs?
11. The night2 run's input.json `suggested_test_file` names Part A's file (the seat's finding (2)) — a finding on the run / the brief's shared suggestion.
12. The ruled tail: `-r16-threehunks-1` reads `ks-1` to `re.findall(r'ks-\d+')` (drafter control: `['ks-1257', 'ks-1']`); the pushed
    `-r16-settingsdefaults-1` (96 chars) reads the own key only; all six pushed names NONE beyond the own key.
13. The #1036 base move: 50 files (29 locks + 20 manifests + audit-baseline.json) ∩ the 10 paths = ∅, ∩ the 2 tamper files = ∅ (drafter, three
    instruments); the resolved qs / body-parser / express versions sit under every count at 8c2f7b3fd.
14. Seat B's three attributions by this seat (KS-1118 <- #1170, KS-1158 <- #1172, KS-1265 <- #1174; attrib18.json c1-c4 true) before its HOLD; Seat B's
    later four (#1176-#1179, 00:37:59Z-01:02:04Z) opened after — never this seat's to attribute; Seat B's namespace carries `-r18-` on three refs.
15. The 16th's held F3b TS18046 (`'body' is of type 'unknown'` at :158) is GONE in the CAST row (typecheck 0/0) — what the cast does at the same site.
16. KS-1123's history: walked 2026-09-16 on #1002, moved back the same day by the board login, walked again 23:44:27Z on #1168; #1002 touched
    verification.ts (a PRIOR product edit at :597 `??` -> `||` per the ticket title) — does the CAST row's cell pin it?
17. Subjects 77-90 chars ASCII (#1168's and #1169's exactly 90); branches 78-96 (the ruled KS-1257 name the longest).
18. Seat B's HOLD: "waits on Seat C 18th's live holder: 6 min before #1170, ~2 min before #1174" — which of this seat's windows (drafter: #1169's
    23:46:05Z-23:52:26Z and #1173's 00:11:36Z-00:17:16Z by the interleaving)?
19. The seat's S1 cwd guard in measure18.py — would it refuse a merge-tree from a script whose cwd is a WORKTREE under worktrees/ (also the shared store)?
20. The bodies name `#1036` ×3 and `45 passed` ×1 each; none names `--pair-blob` / `no-useless-assignment` / `EXCISED` — the READY-only facts.

## 5. NOT MEASURED by the drafter (named, not asserted)
- Any suite, tsc, eslint, typecheck or census run — the drafter ran no test (710/710, the per-PR lane counts 716 / 716 / 714 / 717 / 714 / 715, 742/742
  on the all-6 tree, tsc 0, eslint 0 errors + the warning rows, typecheck delta 0 ×11 incl. health.ts 1/1, the A4 / A5 red / green counts, the cells,
  the census sets) are carried as the seat's claims. The 742 = 710 + 32 is the drafter's arithmetic.
- The tampers — not planted by the drafter; the `from` texts, scope anchors and red sets are the seat's / the brief's (only the six `from` counts
  and lines, the :991 / :1016 mount lines and the ks733 file's four develop cells were read).
- The RED-FIRST / GREEN-AFTER halves — not run; the checker's red_first.json / green_after.json counts and titles were READ (shape_3.out) and the
  seat's READY rows carried.
- The live PR bodies' full text beyond the detectors / substrings (bodies never printed); the seat's body records under raise/ (listed, not read).
- The seat's HANDOVER / RECORD.md / the gate/ tooling (merge18b.py, targets18.py, dry18.sh, go18.sh) / the DRY outputs / series18.py / lock18.sh — named,
  not read except the lock.out and attrib18.json files, the *.lock.out window rows and measure18b.out's tail.
- The loose-object attribution by reachability (lead (b)) — buckets measured, reachability not; the seat's 9215 vs the buckets' arithmetic not
  reconciled (section 1).
- The vault daily note — not read.
- The two prior report dirs' full NOT-PINNED sections — the PRIOR (16C) and EARLIER (16B) rows READ by grep; the OLDER (#1036) report's headings only.
- The launcher controls' final line (running at this report's write — section 8).
- Whether the sibling gate18B has launched or reported (its dir held only COMMISSION.md at the drafter's `ls` 01:1xZ; no report dir
  `2026-09-22-batch1170-1179-r1` existed).
- The DKIM / inbox discriminator on the GO (the drafter sends no mail).
- Seat B's lock arm (MG-10) — its raise/lock18.* not read; the prompt asks the gate.

## 6. Checkout counts AFTER (read verbs only throughout) — see `checkout_counts_after.txt` (written at the drafter's close; section 8).

## 7. The launcher's controls — `launcher_controls_gate18C.sh` (A-U + positive; ~25 min; started 01:52:15Z in the background; each control on a COPY of
   the prompt or a QAB1167_* override; control F on a launcher COPY with #1168's compare line edited to behind=1; E2 the pair's second alone blob as
   develop -> LANDED; U `--pair-blob` reworded -> exit 35).

## 8. Final state (addendum, 2026-09-22T02:1xZ UTC = 12:1x AEST)
- **Prompt** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1167-1175.prompt.txt` — 1141 lines, 158867 B,
  sha256 `fcf6dc1a6f7fa1fa13e60ba56c38be5f875845f16264837f6526702acb6ab0b5` (`wc -l`; `shasum -a 256`; fill_prompt_5.out — run 5 after the S6
  freshening sentence in lead (b); runs 1-4 kept beside as `.pre-HHMMSS` COPIES). Every head in it was read from origin in the same action that
  wrote it (fill_prompt's `ls-remote` 02:09:5xZ, 13 refs, 6/6 AGREE with round18C and the READYs).
- **Launcher** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1167-1175.sh` — 543 lines, mode 755,
  sha256 `cc8882bef7b931aaf68200e63b2304af5a6ca05467a58a8438cb0e67c6a08ea2` (unchanged across generator runs 4-6: a prompt edit does not change the
  launcher's bytes); `--check` rc 0 (`launcher_check_1.out` 01:49:55Z-01:51:29Z; `launcher_check_2.out` 02:10:07Z-02:11:37Z on the final prompt) and
  rc 0 again as the controls' POSITIVE at 02:07:35Z-02:08:17Z.
- **Controls** (`launcher_controls_gate18C.sh`, `launcher_check_controls.out`, 01:52:15Z-02:08:17Z): **23 OK / 0 MISMATCH** — A missing prompt 4 · B
  brief absent 3 · **C wrong head (last PR) 6** · D develop at the old parent 3916eacd1 18 · E develop at #1167's head 19 (LANDED) · **E2 develop at
  #1173's alone health.ts blob 19 (LANDED — the pair's second half)** · F compare behind=1 on a launcher copy 10 · G no thinking directive 8 · H
  namespace sentence reworded 32 · I #1171 demoted to tier 2 7 · J MG-2 phrase reworded 25 · K RULE WHETHER IT BLOCKS reworded 30 · L by-name item 9
  reworded 33 · M subject prefix shortened 23 · N non-TTY launch 21 · O BOTH token reworded 30 · P GATEWAY_URL loopback reworded 31 · Q seat worktree
  reworded 28 · R :6000 lsof reworded 29 · S PARTIAL marker planted 34 · T a head altered in the prompt 20 · **U `--pair-blob` reworded 35** · POSITIVE
  0. Controls dir `controls_gate18C.dNfPa0/` (the prompt copies + each control's .out). (Controls H-U ran against the prompt as it stood at each
  copy — runs 3-5 differ only in lead (b)'s wording; the POSITIVE and `launcher_check_2.out` cover the final bytes.)
- **Checkout counts AFTER** (`checkout_counts_after.txt` 02:08:47Z vs BEFORE 01:13:45Z): porcelain non-untracked 0 -> 0; porcelain total 17 -> 17;
  `.git/worktrees` 272 -> 272; for-each-ref 1223 -> 1223; count-objects 9416 / 61660 / 101422 / 47 / 297855 / 435 -> the same; .git/config sha256
  identical; HEAD `develop` 581ed7fa1 unchanged; `diff` of the two files (dates + the three extra AFTER lines excluded) empty. Origin develop
  8c2f7b3fd at the close; the push-lock dir ABSENT. **S6: 186 loose objects FRESHENED (mtime only) — 95 by this drafter's predict at 01:20Z, 91 at
  01:25Z not this drafter's; content byte-identical.**
- Network summary: `git ls-remote` (drafter ×5 + the launcher's own under --check ×2 / the 23 controls), GitHub GET (pulls / files / commits /
  compare / contents / rulesets), AgentMail GET (list + by id), Linear GraphQL query. No fetch, no mail, no tap, no Linear write, nothing launched,
  no `inbox_routing.conf` write, no write under `!CODING/` (S6's mtime freshening excepted and disclosed), no port connected by hand, no key
  printed, nothing written into the gate18B dir.
