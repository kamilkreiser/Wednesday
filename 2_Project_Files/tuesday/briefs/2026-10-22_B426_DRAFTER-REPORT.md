# B426 DRAFTER REPORT (Composer records seat R18, PR #85 fix round 3) · 2026-10-22 00:39 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B426_SEAT-R18_composer-records-pr85-round3.md`. Read-only drafting: no push, fetch, merge, commit, worktree, no tmux, no card other than `show composer-pr85-round2-nogo-one-line-1021`. Stamp slot: ONE line (the Model line), one literal slot. The drafter did not make a `.pre-stamp` copy (only two files may be written): make it with `cp` before filling the slot (REFUSE 1 control expects count 1).

## What I measured (all read verbs, 00:33 to 00:39)
- **Route:** the Composer root repo has **0 remotes**. Records land as ONE local commit on `records/bNNN` in a worktree `.tools/wt-bNNN-rec`, and Tuesday folds with `git merge --no-ff` (source: `Briefs/2026-10-20_B344_STATUS.md` lines 38, 42, 63, 140; history entry B344). No PR, no push.
- **State that matters:** root `main` = `348e5087…`; `records/b344` = `f4e57d8a…` is ONE commit ahead and **NOT folded** (`is-ancestor` rc 1). So B344's records are still only on their branch.
- **Highest C = C-96** on `main`, on `records/b344`, and on all 88 local refs carrying the file (0 refs with C-97 or above; positive controls: C-95 found, C-9999 not; the control pattern `C-9[0-6]` hit 4 refs). So the new entry is **C-97**. BACKLOG max id: 366 on `records/b344` (365 on `main`), so the rows are **#367 and #368**.
- Prior work: 0 hits for B358, B350, B353, B423, B424, `renderedTextCredentialShapes`, PR #85, B358-2, B424-1 in BACKLOG, CLARIFICATIONS and history on `records/b344` (control `| 340 |` found).
- `records/b344` and `main` contain 0 of the B423 to B426 files (control: 36 B344 files), so all four catch-up files are absent. The project copies of the B423 and B424 briefs are `cmp`-equal to your stamped originals. Hashes are in the brief (REFUSE 5).
- PR #85 at 00:36:41: open, draft, not merged, head `85105729…`, main `308b7aa6…` (ls-remote and one `gh api` GET).
- The card `show` for the exact id printed `status ruled`, `ruling: choice='a' ruled_ts=2026-10-21T14:46:09.011213+11:00`; option labels and details are quoted in the brief's AUTHORITY block.
- Tooling the seat can copy: `.tools/b344/scripts/` (build_backlog.py, scan_hidden.py, check_staged.py, refs_assert.py) and `.tools/b424/kit/qgate424.py` (a fragment-built schema-name scanner, labels only; modes `controls`, `lines`, `tree`).

## Questions for Tuesday (each with a recommendation)

1. **Base: stack on `records/b344` (S1) or fold it first?** Brief default: the seat branches `records/b426` from `records/b344`'s tip and does NOT touch root `main` or the root checkout (1,034 dirty lines); you fold `records/b426` and B344 rides in with it. If you fold `records/b344` before launch, the brief accepts that too (S2, base = merged `main`). **Recommend S1 (as written):** it avoids a second 35-file quarantine dance and keeps one fold for you. The cost is that B426's BACKLOG ids (367, 368) and C-97 depend on `records/b344` landing first; the fold order is stated in the brief.

2. **Names rule vs the file's own convention.** Your commission says no person's or client's name in any record; the existing entries and rows say the owner's first name in headings and "Note for Kam". I wrote the brief so the seat uses "the project owner", "the coordinator", "the project's GitHub account" (handle not printed), quotes only the card title, options and default (NOT the card's BLUF, which names the client's export schema and the owner), and does not copy the placeholder example string for B358-2 (it contains a first name); it cites the line instead. The commit's git author header is machine config and stays. **Recommend keeping it literal** as written. If you want the owner named as the existing entries do, say so and I drop the scan.

3. **"Ruled Minor by Tuesday" has no time.** Your commission gives the ruling but no timestamp or file. The brief tells the seat to write "ruled Minor by Tuesday in the commission of B426 (time not recorded here)". **Recommend:** add the time (and the file or ledger line) at stamp time if you have it; otherwise leave as is.

4. **B423 Records proposals 2 and 3 are not in the two rows.** Proposal 2 (the strict-scanner gap, ruling 3, B353 Records) and proposal 3 (the field-types derivation) are still unfiled in BACKLOG (0 hits for "strict-scanner"). The brief keeps your count of 2 rows and lists them in FOR TUESDAY. **Recommend:** a follow-up records round rather than loading this brief (adding them here would make it 4 BACKLOG rows, #367 to #370, and change the last line); the earlier #85 chain (B350, B353, B358 STATUS and briefs) is also untracked in the root and unfiled.

5. **Catch-up scope: B423 and B424 only (4 files), no evidence folders.** As commissioned. B424 STATUS depends on B358 STATUS, which is untracked. **Recommend** a single later catch-up round for the whole #85 chain (B330, B350, B353, B358, with evidence), one decision.

6. **Last-line count `<n>`.** The brief defines `catch-up <n>` as the four copied files (not counting the B426 brief copy and STATUS, which are the seat's own). **Recommend** keeping that; say so if you want the count to include them.

7. **STATUS file date 2026-10-21.** The path you gave (`2026-10-21_B426_STATUS.md`) is used verbatim although the brief file is dated 10-22. No action unless you want them to match.

8. **Model.** Sonnet, row C8 (line 98 of model-routing.md; no "records" row exists; B344 used C8). **Recommend** unchanged.

## Risks I could not close
- Whether another records or Composer seat is live was not checked (no `ps`/`tmux` by me); REFUSE 7 makes the seat check.
- `AGENTMAIL_API_KEY` was not re-counted (relayed from B423 and B424).
- The open Composer cards' state is unread, and the brief forbids saying any is ruled.
- Fold collisions: the root already holds untracked, byte-equal copies of the B344 files and of the four catch-up files; they will collide on your fold (the brief makes the seat list them, as B344 did).

READ-WHOLE-BY-TUESDAY: not applicable to this report (the brief's last line is `READ-WHOLE-BY-TUESDAY: PENDING`).
