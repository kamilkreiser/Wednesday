# DRAFTER REPORT — Seat R 8th (#1398 squash M-4 + F-3 + PRs 3-5 raise), 2026-10-07 ~02:1xZ-02:2xZ UTC

Nothing was sent, launched, merged, pushed, commented or filed. The drafter wrote exactly four files:
- brief `fleet/briefs_staged/2026-10-07_seatR8_squash1398_raise3to5.md` (240 lines, 32,965 B, sha256/16 `195220689a690d66`). That is over the ~220-line aim, because the explicit re-key list (STANDING_LINES `:425`) and the live-floor table were added;
- DRAFT GO `…/2026-10-07_seatR8_GO_1398_DRAFT.md` (30 lines, `b711c3d4b6c68b96`);
- DRAFT ADDENDUM `…/2026-10-07_seatR8_ADDENDUM_1398_DRAFT.md` (43 lines, `bb396ec0ea4a45eb`), with the verdict line left as `ACTIONS VERDICT (Wednesday): <PLACEHOLDER for Wednesday>`;
- this report.
Scratch is in the session scratchpad `…/01e35370-…/scratchpad/r8/`. `!CODING` was read with read verbs only (git `--no-optional-locks` in the builder dry run). The shared `rev-parse --all` read `37fd7656ab74bb16` (1,610 lines) before the drafter's clone and fetch, after them, and after the builder dry runs. `s-ra3-ks1136` porcelain was 0 throughout. The gate71 kit holds 0 `__pycache__`.

## Inputs read whole
- R 7th's handover (352 lines, 26,375 B, sha256/16 `529c54446da6a4e5`, == the task's);
- R 7th's brief and GO;
- R 7th's mails: prepush_M3, WRAP, and the ANSWERs plan/proceed/M2/wrap/xfer;
- R 6th's ADDENDUM;
- E 9th's holdwork, ANSWER plan and ANSWER proceed; D 15th's GO;
- STANDING_LINES (426 lines, incl. `:425`);
- the Secuura launcher's KS-907 branch.

## Measured
1. **develop and M'.** `ls-remote` (own sshCommand, `GIT_SSH_COMMAND` unset) 02:14:40Z-02:14:45Z, 2,104 lines.
   - develop `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`; pull/1398 == the ks-1136 branch == `240d4dfd5b7b656db6e46bb96f934621a67720fd`; pull/1383 `32e8459bc0f5`; highest refs/pull 1406.
   - In a `--shared` scratch clone after a by-SHA fetch: M' tree `ce7f6c7bbda2b45491dbd3b184df7a49d4d52528` (== T'); parents `9414aa54e92c…` then `69f2045af2a4…`; subject byte-exact; trailers 1 B; message 74 B. `D..M'` = 4 paths, modes {100644: 3, 100755: 1}, doc blobs `df566caf…` / `b938c329…`.
   - D: tree `a4a219b87271`, ONE parent `fa24bddedf3b`. deadbeef control rc 128.
2. **Actions on M' (R 7th's classification REPRODUCES).**
   - 6 runs by full head_sha (controls: 6ea65f64e639 -> 6, deadbeef -> 0).
   - Class 1: same job/step as sibling 37546800703, log needles 1/1 and 6/6, `##[group]` 19/19, nonsense 0/0. It also fails on the pre-merge-in head (37461176035).
   - Class 2: the set and step are identical to the develop-branch run 37549079657. Both logs: `packages/shared is not built` x1, the same six failing suites, `##[group]` 24/24. Mine prints 64 passed / 6 failed (of 70); ks1136 is not among the six.
   - Class 3: mine ⊂ the develop run 37549079853 (develop adds Schemathesis), with identical failing steps.
   - NOT re-measured: R 7th's sample-window counts.
3. **Kit and authority files re-hashed.**
   - Body 7,647 B, sha256 `1a0da357…132148`: 0 `Merged by`, 0 trailers, KS-1136 the only key, 0 `(#`.
   - Composed docs hash-object == the two blobs.
   - R 3rd's handover 235 / 18,818 / `35ad164280e587d5`; RULINGS `4b8f2c1e300de84d`; gate71 report `5cbc607a8def3446`.
   - Payloads: KS-998 5,599 B `a4905e4da54a6cf7`; KS-1313 9,252 B `59f5d73d68df586d`; KS-1164 4,643 B `5c5e586406ebe4b1`. The 4,886 B variant is carried, not re-measured.
4. **The draft GO was proven against the real builder logic.** A scratch copy of `build_addendumra7_1398.py`, re-keyed RA7_->RA8_ (46 asserted) with `:88` re-aimed, was run against the real `s-ra3-ks1136` (read verbs) with outputs to scratch.
   - **Positive: the draft GO + a TEST-ONLY addendum line -> rc 0**. Every field parsed exactly once; tree, parents, 4 paths, mode census, body sha and merge_note were all asserted; the composed body ends with ONE `Merged by Seat R 8th … 35ad164280e587d5`.
   - **The draft ADDENDUM as staged -> REFUSES at `:90`** (the zero clause is absent by design, so the placeholder cannot release M-4).
   - R 7th's real GO -> REFUSES at `:88`. The GO used as an addendum -> REFUSES (no prefix).
   - ⚠ **Wednesday: when filling the verdict line, the zero-new-failures clause must be in YOUR line.** The draft deliberately contains that string nowhere (grep -i 0 in all three files).
5. **Linear (HTTP 200):**
   - KS-1136 In Progress (1 comment, last 2026-09-18);
   - KS-998 Backlog;
   - KS-1313 In Progress, **UNASSIGNED**, att pull/1245;
   - KS-1326 Backlog; KS-1164 In Progress; KS-1401 In Progress, att pull/1383.
   - #1398 `mergeable_state` is now **`unstable`** (the red checks); #1383 `dirty`.
6. **Lane declarations (AST, no import)** in R 7th's `namecheckra1.py` / `inbox_matchra1.py`. Line numbers are in the brief. Gaps found: `e9`/`seate9` and all e9 FORMS are ABSENT from FOREIGN (E 9th is live). FOREIGN_FORMS lacks the e6-e8 and d9-d15 forms that FOREIGN holds. COTENANT_EXACT_REFS still names f1/e1/e2. OTHER_SEATS holds `r 8th` (to remove) and has no `r 9th` yet.

## Discrepancies found (named in the brief)
- **Shared `rev-parse --all` = `37fd7656ab74bb16`, not R 7th's re-baseline `45e4418378f83e7e`** (count unchanged at 1,610). Consistent with R 7th's push updating `refs/remotes/origin/feature/ks-1136-…-ra3-2` to `240d4dfd` (read). That is INFERRED, not diffed.
- E 9th's plan says flow `30.`-`33.`; its brief's Q-N9 reserves `30.`-`34.` (`34.` = E5, UNRAISED unless ruled in). The brief says both.
- R 7th's `raise/` holds a `__pycache__`: the copy excludes it.
- The builder's predecessor merge-claim loop names R 1st-R 4th only.

## Open questions for Wednesday (one recommendation each)
1. **Q-ADOPT8:** the adoption sets name R 7th's lane, and M-4 (an API squash) writes no local ref. **Rec (a):** empty both, EXPECTED 0, the ks-1136 lane FOREIGN by name. If the tool refuses a zero, the tool wins (b: keep 1/1, READ-ONLY, R 8th's authority).
2. **Q-REBASE8:** accept the R 8th ITEM 0 `rev-parse --all` reading BY NAME as the new baseline. **Rec: yes**; the count is unchanged and the moved value is explained by R 7th's ruled push.
3. **Q-PRED8:** extend the builder's predecessor loop to R 7th. **Rec (a)**, with a planted-claim arm.
4. **gate73 landing order** (R 8th PRs 3-5 vs E 9th) and so who owes the docs keep-both merge-in. **Rec:** decide at the gate73 GO, merge in ticket/number order (R 8th's 25./26./29. first, then E 9th's 30.+), and each later PR takes ONE docs merge-in, as #1398 did.
5. **§5f comment on KS-1136 after the squash:** it needs your text. **Rec:** put it in the ADDENDUM (or say "none this round") so R 8th does not hold for it.
6. **The launcher pull (owed):** with D 15th and E 9th live, KS-907 should print READ-ONLY. If either wraps before R 8th launches, the pull path is live again. **Rec:** launch R 8th while another seat is live, or land the owed launcher fix first.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 13:22
