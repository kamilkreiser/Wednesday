# B428 drafter report (for Tuesday) · 2026-10-22 01:05 to 01:20 AEDT

Brief: `2026-10-22_B428_SEAT-R19_composer-records-fold-b426.md` (slot `@STAMP_TIME@` x1, last line `READ-WHOLE-BY-TUESDAY: PENDING`). Read verbs only (`git --no-optional-locks`, `cmp`, `wc`, `ls`); nothing in the project written, nothing moved.

## MEASURED (01:05 to 01:15)
- `main` 348e5087; `records/b344` f4e57d8a; `records/b426` 2c6ee579 (parent f4e57d8a). `main..records/b426` = 2 commits, unfolded (`is-ancestor` rc 1). Tree of `records/b426` = fe4252e498c851cb9d4c3cd6ee7377434109bd7d.
- `diff --name-status 348e5087 records/b426`: 68 paths = 64 A + 4 M. Numstat: 68 files, +3354, **-1**.
- 4 M paths (BACKLOG, history, CLARIFICATIONS, B339 STATUS): clean in the root.
- Collision: **all 64 A paths exist untracked in the root**, none tracked on main. `git show records/b426:<path> | cmp -`: **62 EQ, 2 NE**.
- The 2 NE are `Briefs/2026-10-20_B344_STATUS.md` (blob 23,305 B, root 29,588) and `Briefs/2026-10-21_B426_STATUS.md` (blob 28,027, root 35,115). Both are APPEND-ONLY: `head -c <blob size>` of the root copy cmp-equals the blob (each root copy = committed bytes plus the seat's After block).
- Root: 1037 `status --short` lines (1035 `??`, 2 ` M`: B26 and B298 STATUS); `-uall` count 42,772; nothing staged; no MERGE_HEAD; HEAD = main; no remote; no hooksPath; 89 refs; C-97 on b426 only; rows #366-#368 on b426; `.tools/b428` absent.

## Where the brief departs from your task text (please check)
1. **"0 deletions" is wrong for this fold: it is 1.** B344 changed row #340's State cell (BACKLOG: 4 added, 1 deleted). The brief asserts 68 files, 3354 insertions, 1 deletion, and that `git diff 348e5087 main` equals `git diff 348e5087 records/b426`.
2. **"Stop on any non-equal collision" collides with 2 measured non-equal files.** I wrote an exception for exactly those two named paths, with a program-checked prefix test and a control. Any other non-equal path is still a STOP.
3. The brief asserts `rev-list --count 348e5087..main` = 3 and main's tree = fe4252e4... (that tree is the branch's; a no-conflict merge must give it).
4. Dirt proof is by sorted `status --short --untracked-files=all` before/after (`comm`), not by count equality: the collapsed 1,037-line view hides directory lines that can vanish or split. Left-set must be exactly the 64 `??` lines; the appeared-set must hold only the seat's own files and quoted other-seat files.

## Questions for Tuesday (each with a recommendation)
1. **The two append-only STATUS files lose their After blocks on merge** (the checkout writes the committed bytes; the closing `RECORDS COMMITTED:` lines would exist only in quarantine). Restore them into the root after the merge, leaving 2 new tracked ` M` lines? **Recommend yes** (the brief's default): STATUS last lines are the channel, B344 restored the B339 After block the same way, a later records seat commits them, and the originals stay in quarantine either way. If you strike it, the brief's Step 4 says to skip it.
2. **Stamp pre-check:** nothing is running; I did not run `ps`/`tmux`. **Recommend** you re-measure `main`/`records/b426` and any live Composer records seat at stamp (REFUSE 2, 7 re-check it for the seat anyway).
3. **Who files B428's own brief copy, STATUS and evidence (untracked after the fold), plus the 21 root-only evidence files and the earlier untracked chain (B322, B330, B331, B333, B341, B350, B353, B358)?** **Recommend** one later catch-up records brief; B428 makes no commit by design (a fold seat that also commits would defeat "main's second parent = 2c6ee579" cleanly, and the parents/diff proofs would shift).
4. **Worktrees `.tools/wt-b344-rec` and `.tools/wt-b426-rec` may be pruned after the fold.** **Recommend** do not prune now; no deletes in this brief, ask Kam later.

## Judgement calls
- Merge message avoids any name; trailer passed as a second `-m`. No gitleaks run (nothing staged; both source commits were scanned at commit, RELAYED).
- Model row C8, as for B344 and B426 (MEASURED by me: `grep -i -c '^| *C8 '` on model-routing.md = 1; the brief's C10 control is taken from the B426 brief, not re-run by me).
- Brief kept the REFUSE-1 quote-split slot form from B426; no `.pre-stamp` copy was made by me (the brief says a scratch file works as the control).
