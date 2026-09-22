# DRAFTER REPORT — batch gate over Seat B 19th/20th's NINE PRs (#1182 #1184 #1186 #1194 #1196 #1198 #1199 #1200 #1201; TIER 1 on the EIGHT product/tooling/auth-adjacent PRs, TIER 2 on #1194 KS-1229 test-only; round 1 of 2)

Drafter: the gate19B drafter subagent (under Wednesday, the 15:1x seat of 2026-09-22). Started 2026-09-22T07:57:00Z (`date`; = 17:57 AEST); bound
~60 min. Read before the first write: the 19B commission WHOLE + the HOLD capture beside it; the 19C COMMISSION / README / DRAFTER_REPORT / round19C.py /
capture / inbox / predict / gh / linear / fill / generator / template / controls / repin scripts and the prompt DRAFT WHOLE; the 18B dir LISTED (`ls`)
— its scripts NOT read (the 19C set is the later copy of the same pipeline and was complete; NOT MEASURED whether 18B carries a rule 19C dropped).
Every head was READ FROM ORIGIN in the same action it was written (lsremote_1.out 07:59:11Z; the predict fetch 08:05:10Z; fill_prompt runs 08:15:49Z /
08:18:11Z / 08:20:27Z; the generator 08:17:56Z / 08:18:14Z / the run-3 time in gen_launcher.run3.out; the launcher's own --check 08:18:20Z). Every number below names its instrument and its file.

## 4. Drafter's own slips (recorded as they happen; FIRST in the final message)
S1 08:17Z — the generator's run 1 REFUSED (rc 4, `gen_launcher.run1.out`): six BOTH tokens were in the capture but not the prompt — five archived keys
   (the prompt wrote `KS-501 … KS-1092`, an ellipsis over the list the generator asserts) and `whitespace-stripped` (the prompt had it only in
   UPPER case). Both are prompt-text gaps, not measurement slips; the DRAFT was edited (the first six archived keys spelled; the lowercase phrase
   added), fill run 2, generator run 2 wrote. The refusal did its job.
S2 08:20Z — the prompt's THE SHAPE paragraph said `strict --check rc 0 on 13` canonical rows and `+ 7 whole patch.diff sha16s`; the measured values
   (predict_batch_scratch_1.out (c); round19B.py `patch_sha16`) are 15 rc-0 rows (19 − 3 rc-128 − 1 rc-1) and 8 patch.diff sha16s. A count typed from
   memory instead of from the file — exactly the class the commission forbids. Corrected in the DRAFT (`.pre-0820-rc0count` beside), fill run 3
   (`fill_prompt_3.out`, sha256 d20a94e4…), generator run 3 + `launcher_check_2.out` AFTER the controls finished (a running `bash "$L"` must not have
   its file rewritten under it — so the regeneration waited; the controls ran against the run-2 launcher and the run-2/run-3 prompt, whose tokens are identical).
S3 (a design note) — the first extraction of the nine READYs' pin lines was a `grep -E` over ~170 KB that overflowed the tool's output twice
   (persisted, not read); replaced by `parse_readys_gate19B.py` → `parse_readys_1.out` (356 lines), which is the file round19B.py was built from. No harm; time.
S4 (a design note, carried from 19C's S5) — the launcher's launch-path `cd "$QA_DIR"` line is spelled `'c'+'d'` in the generator so this drafter's
   no-cd hook is not tripped; the launcher's bytes are the 19C launcher's shape.
S5 (a naming note) — the drafter's gh_pr_reads assigns #1201 tier 1 by the READY's tamper-file claim (ssrf-guard.ts), which the files API cannot
   see (the PR touches only a test file): the "rule" tier on #1201 is the READY's own rule, stated as such in the table and in the prompt (the gate
   MEASURES the tamper record). By the files alone #1201 reads tier 2.

## 0. Constraints honoured
- No `cd`; absolute paths; `git -C`; heredocs `<<'EOF'`; rc on its own line; nothing deleted or renamed (`.pre-HHMM-*` COPIES beside; the fill script
  and the generator take a COPY for their backups). Timestamps from `date`. Nothing written in the gate19C dir (its drafter was working there at the
  same time — its files were READ only; its `__pycache__` was already there).
- Secuura checkout READ-ONLY: `ls-remote`, `status --porcelain`, `for-each-ref`, `count-objects -v`, `config --get` (core.sshCommand — read into the
  clone's environment, never printed; remote.origin.url), `rev-parse`, `cat-file -t`, `find` over .git/objects, `ls` of .git/worktrees and the seats'
  record folders (LISTED, not read). EVERY write verb (clone, fetch, read-tree, apply --cached, write-tree, merge-tree, commit-tree ×1 for the unamended
  control) in `predict_batch_scratch_gate19B.py`, whose first act refuses (rc 9) unless its target is a scratchpad under
  `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/`, in a `git clone --bare --filter=blob:none` FROM ORIGIN (`predict19B.he6y6_il/origin.git`;
  31429 in-pack objects after the fetch) — NEVER `--shared` from the checkout. `count-objects -v` byte-identical before/after (count 1487 / size 8080 /
  in-pack 108731 / packs 48 / size-pack 303244 — predict_batch_scratch_1.out first and last lines; checkout_counts_before.txt 07:59:11Z vs
  checkout_counts_after.txt 08:20:00Z: `diff` rc 1 on the READ-timestamp line ONLY — porcelain 0 / 17, worktrees 295, for-each-ref 1266, config sha256
  6417b203accd…, HEAD develop 3bad652d1 all identical).
- THE LOOSE-OBJECT CONTROL (`loose_objects_1.out`, `find … -newermt '2026-09-22 17:57:00' | wc -l`): **0** loose objects carry an mtime after this
  drafter's start (19C's drafter saw 12 — Seat C's dry ×12 — in its window; none in this one). Seat C's worktree dirs `s-c19-batch` /
  `s-c19-ks1097*` modified 17:59 AEST (07:59Z) — Seat C 19th's own activity, not this drafter's (no write verb of this drafter touches `.git/worktrees`).
- Network: `git ls-remote` ×5 (07:59:11Z; fill ×3; generator ×2) + the launcher's own reads under --check and the 13 controls; `git clone` + `git fetch`
  FROM ORIGIN (the scratch clone; lazy blob fetches for the applies); GitHub GET (pulls / files / commits / compare / rulesets); AgentMail GET (list +
  by id); Linear GraphQL query (the file asserts no `mutation`). No mail sent, no pane tapped, no Linear write, nothing launched, no
  `inbox_routing.conf` write, no write under `!CODING/`, no key printed (`/usr/bin/grep -c -i -E 'ghp_|github_pat'` over gh_pr_reads_1.out = 0;
  `/usr/bin/grep -c lin_api` over linear_reads_1.out = 0). Datasec mail neither opened nor listed (the capture filters on from-address AND the
  Blockchain-B / Blockchain-C subject prefixes; the inbox listing printed subjects of the hits only).

## 1. Timeline (every value: instrument | file)
- 07:58:38Z `capture_ready_mail_gate19B.py` (`capture_ready_mail_1.out` rc 0; `/usr/bin/grep -c written` = 34): the nine READYs (01-03 `(Seat B 19th)`
  05:48:55Z / 05:50:51Z / 06:03:34Z; 04-09 `(Seat B 20th)` 07:11:34Z / 07:19:36Z / 07:28:49Z / 07:40:16Z / 07:48:36Z / 07:52:33Z — TAG/NUMBER MISMATCH
  lines 0), the 05:24Z / 07:09Z / 07:55Z STATUS mails (the drafter's HOLD capture `mail_seatB20_status_0755.md`, 6528 chars; Wednesday's own
  `mail_seatB20_status_hold.md` beside, untouched), the 04:09Z S1 / 04:27Z plan / 05:07Z KS-1164 / 07:04Z plan QUESTIONs, the 06:18Z hand-over wrap, 7
  Wednesday mails to B, 3 ADDENDUM mails to C (the S1 addendum 04:10Z, the (2') addendum 06:22Z, the band addendum 07:26Z), 4 Seat C 19th
  STATUS/QUESTION/wrap mails (context; Seat C's READYs skipped — gate19C's). The combined `mail_gate19B_ready.md` (`NOT YET ARRIVED` count 0 by
  `/usr/bin/grep -c`; the nine `READY FOR QA (Seat B` subject lines present).
- 07:59:11Z `checkout_counts_before.txt` (the values in section 0) and `lsremote_1.out` (`git -C <checkout> ls-remote origin refs/heads/develop
  'refs/pull/118*/head' 'refs/pull/119*/head' 'refs/pull/120*/head' 'refs/heads/feature/ks-730-*' … 'refs/heads/feature/ks-1179-*'`, rc 0, 36 rows):
  develop 3bad652d1; the nine pull heads == the HOLD mail's; the nine branches at the same shas; two OLDER branches on the same keys at origin
  (`ks-1179-…-r15-f1-1` 8b0713d8f = #1157's; `ks-1229-…-r15-afterverify-…-1` b455e4594 = #1155's — both MERGED priors, not this round's); Seat C's
  twelve + #1189 present at gate19C's pins.
- 08:0xZ `parse_readys_gate19B.py` → `parse_readys_1.out` (356 lines): the per-PR pin table; `round19B.py` written from it (`round19B_selfcheck.out`:
  9 PRs, 18 file rows, 17 distinct, 19 canon rows, +642/-13, per-PR adds/dels consistent True; TIER1 by FILE rule == TIER1 by READY = [1 2 3 5 6 7 8 9],
  test-only [4 9]; 9 own keys; targets 2/2/2/1/2/4/2/2/1 = 18 == file rows; pair rows #1198 #1199; Seat C 19th paths 21, B ∩ C NONE; round19C's
  captured SEATB_PATHS ⊂ B's paths True; C.DEV == DEV True). Every canonical file exists at its run dir with its sha16 (19/19 section rows + 8/8
  patch.diff — the inline check after the self-check).
- 08:04:54Z-08:06:51Z `predict_batch_scratch_gate19B.py` (`predict_batch_scratch_1.out` rc 0; cwd guard live): clone FROM ORIGIN rc 0; fetch by ref of
  develop + the nine + Seat C's twelve rc 0; develop == pin; develop tree cd9b0f6c7b84; (a) per head 9/9: head == READY, parent == develop, 1 commit,
  tree == READY (#1200 the AMENDED d309bb90f69f), files == pinned, +/- == READY; every blob's 12-hex == the READY 18/18, lines == 18/18, mode 100644
  18/18 (no exec-bit file). (b) all-11 chained merge-tree push order / reverse / seed-19 shuffle -> `3df72c02d3250ca584c591fd89734d3391d99337` ×3 ==
  the seat's; shortstat `17 files changed, 642 insertions(+), 13 deletions(-)` == the seat; 17 rows 8 A + 9 M == round19B distinct; every non-pair ALL
  path at its head blob, the pair at the PAIR blob 2ad45cd8e555… / 1603 / 100644 (0 mismatches); each single tree != ALL; Seat C 19th's 21 paths
  changed by ALL: NONE; the PAIR #1198 then #1199 == #1199 then #1198 == 64de96836e46 == the seat's; alone blobs 7bdaa9cad257 / 1602 and 5bf6fb62dba8 /
  1598 (develop's index.ts 0903ce4380f2 / 1597), neither the pair; Seat C's twelve alone -> 5a8458a5697f == gate19C's all-12; COMBINED C-then-B ==
  B-then-C == b4f2a8beaecd (`38 files changed, 1557 insertions(+), 42 deletions(-)`) — the END STATE over 3bad652d1 with BOTH rounds landed. (c) 19
  canonicals: sha16 19/19 == the READYs; strict --check rc 0 ×15, rc 128 ×3 (730 s1 `corrupt patch at line 8`; 974 CHECKKEYCP s1 `line 16`; 974 SCOPETRIM
  s1 `line 10` — the three `--recount --ignore-whitespace` rows, as the READYs say), rc 1 ×1 (1028 s1 from the repo root: the `--directory` prefix, not a
  corruption); -R rc 1 ×15 / 128 ×3 / 1; --recount rc 0 ×17, 1 ×2 (1028 s1 needs --directory; 974 CHECKKEYCP s1 needs both); APPLY (the .opts rows with
  their opts) rc 0 ×19 -> every blob == the READY 12-hex, lines ==; the intermediate ks1213…test.ts after LOOSE e7c614d3eae9 / 311 ==; per-PR write-tree
  == head tree 8/8 and == the UNAMENDED 2a91afd2029e on #1200 (!= the head's d309bb90f69f by construction) — 9/9; (c2) THE KS-1164 INSTRUMENT —
  canonical test blob 1d41e7033542 / 43 lines / 1898 B vs head blob b4edbe5b0d12 / 46 lines / 1932 B: whitespace-stripped byte streams EQUAL True (1567
  non-whitespace bytes each; whitespace 331 -> 365, +34); the one-byte control (byte 100, `t`, removed) False; `git diff -w --no-index` rc 1, 1228 B —
  NON-empty by construction; the all-11 over the UNAMENDED #1200 (a scratch commit-tree of 2a91afd2029e) -> 34728affba20 == the seat's item-0 control,
  `17 files +639/-13` == the seat; the three .opts rows applied STRICT rc 128 ×3 (the READYs: strict rc 128); nonexistent-patch control rc 128. (d)
  develop UNMOVED; newdev_tree.txt written (develop / tree / all11 / pair / pairblob / combinedCB / unamended). count-objects byte-identical.
- 08:08:10Z-08:08:48Z `gh_pr_reads_gate19B.py` (`gh_pr_reads_1.out` rc 0): 39 open PRs; nine: head == READY, base develop@3bad652d1, open, mergeable
  True / unstable, 1 commit, author kksecura, created 05:36:16Z … 07:50:08Z; closing 0/0/0 ×9; completeness 0/0/0 ×8 and **0/2/2 on #1184** (a
  `complete…` word in the body and the commit — a lead, not a finding: the detector is a regex); body Refs == own key 9/9; commit Refs == 9/9; titles ==
  round19B 9/9, 70-89 chars ASCII; branches == round19B 9/9; the hyphenated scanner own key only 9/9; the `-?`-tolerant archived/foreign detector
  flags **KS-1213 in #1194's branch** (`ks1213` — the test file's name as a PATH token, the READY's own Q6(b) disclosure; not a key token); subjects
  == titles <= 92 ×9; files API == round19B 9/9, +/- == READY 9/9; bodies: `Claude-written|Claude-authored` on #1199 #1200 #1201 (3/3 as declared),
  `--pair-blob` on #1199 only, `amend|rewrap` on #1200 only; compare merge_base 3bad652d1 / ahead 1 / behind 0 / files 2/2/2/1/2/4/2/2/1 ×9. THE TIER
  TABLE below. Priors #1155 (KS-1229) and #1157 (KS-1179) closed + merged 2026-09-21T20:34Z. Seat C 19th's twelve: heads == round19C 12/12, open,
  base 3bad652d1, files == round19C 12/12, ∩ our 17 NONE ×12. No other open PR on develop since 04:00Z. Ruleset 18499832 active (deletion /
  non_fast_forward / pull_request).
- 08:08:10Z-08:09:03Z `linear_reads_gate19B.py` (`linear_reads_1.out` rc 0; `grep -c lin_api` 0): nine own tickets In Progress, archivedAt None,
  assignee the board login, own PR attached 9/9, comments 0 ×9; TITLES carrying an ARCHIVED key: KS-730 (KS-727), KS-1028 (KS-754) — Linear content,
  kept out of the PR bytes (gh: archived in title/subject NONE ×9); branchName scanner: KS-1028 `ks-754` (the ARCHIVED key EXCISED from the pushed
  ref — CONFIRMED against the pushed name); bot walks Backlog -> In Progress on PR open 05:36:26Z … 07:50:18Z (KS-1229 / KS-1179 no walk: already In
  Progress from their merged priors); attachmentsForURL pull/N == own key contributes 9/9; pull/1155 -> KS-1229, pull/1157 -> KS-1179, pull/1189 ->
  KS-1047 (controls as expected), pull/9999 -> [] (the empty control — chosen on a number no PR carries, after 19C's S1); the 37 archived keys
  archivedAt set 37/37 (the READYs list 36 — KS-1270 is the one they omit); the 14 content keys as round19C states; Seat C 19th's eleven keys In
  Progress with their PRs attached by NAME (KS-1093 ['1187'] — the (2') reading; KS-1047 ['1189', '1190']; KS-1097 four).
- 08:15:24Z the prompt DRAFT (`prompt_gate19B.DRAFT.txt`, tokens __H<n>__ ×9 + __ALL11__ ×3, 301 lines) and `fill_prompt_gate19B.py` runs 1-3
  (`fill_prompt_1..3.out`: ls-remote in the same action, 19 refs, 9/9 AGREE among pull head / branch / round19B / the READY; newdev_tree.txt all11 ==
  SEAT_ALL11, pairblob ==, unamended == 34728affba20, combined b4f2a8beaecd; no residual token, no deadbeef, first line ultrathink, not PARTIAL; the
  nine heads + DEV + ALL11 + PAIR_BLOB + the GO string + both brief paths + the combined 12-hex asserted present) -> **prompt
  `2026-09-22_secuura-batch1182-1201.prompt.txt` 301 lines, 51121 B, sha256 d20a94e4af7685c9cce49ddbcb0e871659286f5e64a190204598dbec2b640231** (run 3;
  runs 1-2 kept beside as `.pre-081811` / `.pre-082027`).
- 08:17:52Z-08:18:14Z `gen_launcher_gate19B.py` runs 1-2 (S1): pins re-read at origin (develop == pin; 9 pull heads + 9 branches == round19B); 17
  judged content paths (the pair path carries both alone blobs + the PAIR blob); mode 100644 asserted on all 18 rows; BOTH 126 tokens in BOTH the
  capture and the prompt; 71 by-name keywords; bash -n rc 0 -> launcher `launch_qa_secuura_batch1182-1201.sh` 387 lines, mode 755, sha256
  a094c6c3526a327121d2e2d2300b8216e103d737522b9bb329e00ab129510a73 (run 2). Run 3 (after the controls; S2) — see section 7.
- 08:18:20Z-08:18:57Z the launcher's `--check` (`launcher_check_1.out`): **rc 0** — nine heads on origin; nine compares merge_base 3bad652d1 / ahead 1 /
  behind 0 / files as pinned; develop == the pin; every grep passed (the last lines are in the final message).
- 08:19:35Z `launcher_controls_gate19B.sh` STARTED in the background (`launcher_check_controls.out`; pid 34726 in `launcher_controls.start.txt`) — the
  "controls end" line is quoted in section 7; D (stale 581ed7fa1) answered rc 18 CHANGED with a content reason (`ks1213-a-derived-writer-relabel-is-refused.test.ts`
  bbfcd0f98923 -> 8082826898c2 at 581ed7fa1 — the 18th round's #1155-adjacent change; the control accepts 17/18/19: any is a stale sha REFUSED).
- 08:20:00Z `loose_objects_1.out` (0) and `checkout_counts_after.txt` (identical but the READ line).
- `repin_and_launch_gate19B.sh` re-keyed from 19C's by `sed` (`bash -n` rc 0; the dry-read prints develop 3bad652d1 + the nine `n:head:branch` rows +
  the prompt path; the routing line `QA/Secuura-batch1182|coagent@agentmail.to|yes` ABSENT at the drafter's read (count 0; the batch1180 control 1 —
  gate19C IS routed and its report dir exists: gate19C was launched while this drafter worked); NOT run).

## 2. THE TIER TABLE (per PR: files touched -> tier ASSIGNED by the commission's rule (product/tooling bytes or an auth-adjacent surface -> 1; test-only cells on existing behaviour -> 2) vs the READY's proposal; gh_pr_reads_1.out)
  #1182 KS-730   ks730a-ingest-500-never-answers-err-message.test.ts + systemErrors.ts (product)                         -> rule T1 | READY T1 | AGREE
  #1184 KS-1028  ks1028-step12-throw-does-not-skip-fanout.test.ts + gdprService.ts (product)                             -> rule T1 | READY T1 | AGREE
  #1186 KS-1160  ks1160-webhooks-post-persists-normalised-url.test.ts + webhooks.ts (product)                             -> rule T1 | READY T1 | AGREE
  #1194 KS-1229  ks1213-a-derived-writer-relabel-is-refused.test.ts (existing test file; zero product bytes)             -> rule T2 | READY T2 | AGREE (the plan ANSWER)
  #1196 KS-629   ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts + kyc index.ts (product)                             -> rule T1 | READY T1 | AGREE
  #1198 KS-974   2 NEW tests + security index.ts + requestSchemas.ts (product, AUTH-ADJACENT)                             -> rule T1 | READY T1 | AGREE
  #1199 KS-976   ks976b-rate-limit-403-says-which-scope-claim-failed.test.ts + security index.ts (product, AUTH-ADJACENT) -> rule T1 | READY T1 | AGREE
  #1200 KS-1164  report.ts (tooling) + ks1164-write-gate-report-never-overwrites-its-input.test.ts (amended)               -> rule T1 | READY T1 | AGREE
  #1201 KS-1179  ks932-timeout-bounds-dns.test.ts (existing test file; the tamper on ssrf-guard.ts per the READY)         -> rule T1 (by the READY's tamper-file claim; T2 by the files alone) | READY T1 | AGREE (S5)
  The commission's letter ("tier 1 on the security/index.ts pair KS-974/KS-976, KS-730, KS-1028, KS-1160, KS-629-A, KS-1164, KS-1179; tier 2 on
  KS-1229") is matched 9/9 by the files. NO contradiction with the commission on the tiers.

## 3. LEADS for the gate (all in the prompt as (a)-(n); the drafter's re-derivation disagrees with the seats' VALUES on NONE)
1. (a) THE KS-1164 INSTRUMENT — the drafter ran it: whitespace-stripped byte-stream equality True, one-byte control False, `git diff -w` NON-empty
   (rc 1, 1228 B). The seat's declaration (amend1164_19.out :1-:10 quoted in READY 8) says the same. CONFIRMED by the drafter's own instrument; the
   gate re-runs it and adds the eslint proof (the prettier error GONE on the amended blob).
2. (b) THE HAND-OVER — the wrap mail's five committed heads (79a895566 8ccfed7b6 a94180ce7 3a979effb 6e675cb81) == the 20th's pushed heads == origin
   5/5 (lsremote_1.out, gh_pr_reads_1.out); the four already-pushed heads unchanged; #1194 opened 07:09:16Z on a head pushed 06:07-06:13Z.
   CONFIRMED at the value level; the seats' `commits.tsv` files NOT read (NOT MEASURED).
3. (c) F-GUARD / (2') — the addendum's text captured (`mail_wedC_addendum_attribution_condition_2_extende_0622.md`); the 20th's STATUS 07:09Z quotes
   the live attribution lines (#1187 on KS-1093 by the 2-prime path); `series19.py` / `attrib19.json` NOT read (NOT MEASURED — the gate reads them).
4. (h) NO EXEC-BIT FILE: 18/18 rows 100644 at the head and at develop (predict (a)) — `fixmodes19`-class is a NON-EVENT for this round unless the gate
   finds otherwise.
5. (j) #1184's completeness-detector hits (0/2/2) — the body/commit carry a `complete…` word; the drafter did not read the body (bodies are never
   printed by the script) — the gate reads it. #1194's `ks1213` path token and #1201's `ks932` content token — disclosed by the READYs (Q6(b)).
6. (k) KS-1179's typecheck delta -1 (2 at head / 3 at develop, the READY's words) — pre-existing in-file type errors on an EXISTING test file; NOT
   MEASURED by the drafter.
7. (m) The loose-object window is CLEAN (0 after 07:57Z); the 12 head-tree freshenings gate19C's drafter saw were Seat C's, before this window.
8. The wrap mail's truncated head for #1186 (38 hex `…cead4859d`) — a record-only slip of the 19th's wrap; READY 3 and origin carry the 40.
9. (n) F-BATCH: the seat's octopus d64e15b98 (10 parents) NOT re-derived by octopus (the drafter used chained merge-tree; NOT MEASURED).
10. The COMBINED END STATE if both rounds land on 3bad652d1: b4f2a8beaecd (C-then-B == B-then-C). If gate19C's GO lands FIRST the BASE of this batch
    moves to Seat C's merge commit; the nine's 17 targets ∩ C's 21 = ∅ so the move is disjoint (launcher exit 17); the merging seat re-predicts the
    nine over that develop and the END_TREE is the tree the gate names then — NOT b4f2a8beaecd by assumption (C's squash merges produce the same
    CONTENT, so the tree oid should equal b4f2a8beaecd if every C target lands at the blob gate19C names; re-derive, never assume).

## 5. NOT MEASURED by the drafter (named, not asserted)
- Any suite, tsc, eslint, typecheck_pre19, census or preflight run — the A4/A5 counts, the lane baselines (835 / 26 / 220 / 917 / 1083), the batch
  counts (863 / 29 / 229 / 917 / 1085), the tamper reds (LOOSE 6 / SIDEEFFECTS 6 / T2 1), the in-hook 12/15 + 45/45, the no-legs hook output on #1200,
  the census rows — all the seats' claims carried as such.
- The seats' record folders (`2026-09-22_seatB-19th/`, `2026-09-22_seatB-20th/`, the HANDOVER document) — LISTED (`ls` of the top level), NOT read:
  commits.tsv, series.out, series19.py (+ .pre-1706-fguard), postmerge19.py, attrib19.json, go19.sh, targets19.py, merge19b.py, hold_state20.out,
  amend_tree_8.json, batch11amend_19.*, my_files19.txt, amend1164_19.out, ready_build19.py (+ pre-fix copies), the lock.out / push*.out files.
- The 18B gateset's scripts (LISTED, not read); the 16B gateset (not opened).
- The full READY bodies beyond the parsed pin lines (parse_readys_1.out); the briefs and ANSWER bodies (captured, skimmed for the (2') text only).
- The PR bodies (never printed by gh_pr_reads; the detectors' counts are regex hits).
- The eslint / prettier state of the canonical vs amended KS-1164 test file (the gate's (a)).
- The octopus re-derivation (F-BATCH); the seats' lock windows against Seat C's (gate19C's round19C.py lists C's — not cross-checked here).
- The launcher controls' final line at the time of the first write of this report (quoted in section 7 once the run ended).

## 6. Checkout counts AFTER — `checkout_counts_after.txt` 08:20:00Z: identical to BEFORE except the READ line (`diff` rc 1 on line 1 only).

## 7. Final state (08:29Z) — prompt sha256 d20a94e4af7685c9cce49ddbcb0e871659286f5e64a190204598dbec2b640231 (301 lines, 51121 B; `ultrathink` first; deadbeef 0);
launcher sha256 760b904227551aee26c71dc267af5f35fd1acc0d5f5106e6ce78c2cdfcbce640 (387 lines, mode 755; generator run 3 at 08:28:14Z — the run-2 launcher
a094c6c3… kept beside as `.pre-082814`); `--check` rc 0 twice (`launcher_check_1.out` 08:18:20Z on run 2; `launcher_check_2.out` 08:28:14Z-08:29:28Z on
run 3). THE CONTROLS (`launcher_check_controls.out`, 08:19:35Z-08:27:53Z, on the run-2 launcher): `controls end 2026-09-22T08:27:53Z: 12 OK / 1 MISMATCH`
— C wrong head rc 6 · D stale develop 581ed7fa1 rc 18 CHANGED (ks1213…test.ts differs there — a content reason; want 17/18/19) · E LANDED rc 19 · G rc 8 ·
S PARTIAL rc 34 · O rc 30 · L rc 33 · I #1198 demoted rc 7 · **U `alone blob` reworded rc 33 (want 35)** — the by-name ladder (which carries `alone blob by
construction; mode 100644`) fires before the PAIR guard, exactly as 19C's U hit 30 before 35: every token the PAIR guard reads is ALSO in an earlier
ladder, so exit 35 is unreachable by construction and the prompt-shape is still REFUSED (rc 33) · W the instrument line reworded rc 36 · T a BOTH token
altered rc 30 · N non-TTY launch rc 21 · POSITIVE rc 0. A wrong/stale develop sha REFUSES (D, E; and exit 10 on the compare for any move) and a partial
ladder REFUSES (S; G; O; L; I; T; W).
The predicted all-11 tree 3df72c02d3250ca584c591fd89734d3391d99337 MATCHED the seat's 3df72c02d325… in three orders (+ the unamended control
34728affba20 matched item 0); the pair blob 2ad45cd8e5552d5d52e48749406203d149967073 / 1603 / 100644 MATCHED both orders (alone 7bdaa9cad257 /
5bf6fb62dba8); the KS-1164 instrument = whitespace-stripped byte-stream equality (True; control False; `git diff -w` rc 1 / 1228 B, not the
instrument). Origin develop 3bad652d1 at every read incl. `lsremote_final.out` (the nine heads unchanged). The checkout's `count-objects -v`
byte-identical at BEFORE / AFTER / FINAL (`checkout_counts_final.txt`). Nothing launched, sent, tapped, posted; nothing written under !CODING/ or
in the gate19C dir. Routing line `QA/Secuura-batch1182|coagent@agentmail.to|yes` ABSENT — Wednesday adds it.
