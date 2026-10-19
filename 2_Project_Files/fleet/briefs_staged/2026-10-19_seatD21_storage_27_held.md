## BLUF

You are **Seat D 21st** on Secuura Platform K (lane Secuura/Blockchain-D). **One job: the 27 worktrees that Seat D 20th held in storage round 1 (69.85 GiB). Re-prove each one under the stricter predicate Kam approved, remove ONLY those that pass, and report.** Authority: Kam's card `wed-secuura-storage-27-held-worktrees-1019` = a, 11:07:50 AEDT, live board: "Remove the 27 under the stricter test". Start by reading D 20th's MANIFEST whole: `5_Project_History/2026-10-19_seatD-storage/MANIFEST.md` and its `evidence/` (the 27 are listed there). Send a plan confirmation before the first removal.

## QUEUE

1. **The predicate, per worktree, proved in writing:** EVERY file the worktree's branch changed relative to its merge-base with develop is EITHER byte-identical to develop's copy at the current develop tip, OR develop's copy is a strict descendant of the branch's blob (the branch's blob appears in develop's history of that path, and develop has moved past it). Use NUL-safe, quoted, literal pathspecs. D 20th's catch was that a spaced path word-split the old test into comparing nothing. Read the rc of every comparison on its own line. A worktree with any file that is neither: KEEP, and name the file.
2. **Controls before trusting the predicate:** a positive control (a worktree you know fails, or a planted difference in a scratch copy, must FAIL) and a negative control (a worktree whose files are all identical must PASS). Both fire, or you stop.
3. **Liveness re-check at removal time, per worktree:** no process cwd inside it, no open file, not touched in 48 h. If D 20th's own phase-T touched `seat-a`'s mtime, its 48 h arm passes from 2026-10-20T21:06Z. If it is in the 27 and still under 48 h, SKIP it, do not override.
4. **Remove with `git worktree remove` only** (the same verb D 20th used). Then count three ways (`worktrees/*` dirs, `git worktree list`, `.git/worktrees` admin) and confirm they agree. `df -k` before and after.
5. **The shared checkout's HEAD, refs, tracked mods and untracked count are unchanged** before vs after, as D 20th measured.

## PARTITION

Yours: only the 27 named in D 20th's evidence. **NOT yours, never touched:** the main checkout `2_Project_Files` (beyond `worktree remove`'s own admin entries); every worktree Seat R 50th (Secuura/Blockchain-R) or Seat J 13th (Secuura/Blockchain-J) uses. Both are LIVE: measure their cwds and treat every worktree either has touched in 48 h as live. Also not yours: deploy clones, and anything outside `worktrees/`.

## HOLDS

- No deploy, push, PR, merge, fetch, prune, `branch -D` or gc. No git write verb other than `worktree remove`. No ticket comments.
- STOP and mail Wednesday on any surprise: a predicate result that contradicts D 20th's measurement, a removal error, a count that disagrees, or df not moving.
- Never edit a script while it runs. Every loop goes in a script FILE run with `/bin/bash`.
- Never delete outside the passing worktrees. Never remove anything outside `vet()`, or its equivalent in your tool (D 20th's three outside-vet removals are the anti-pattern).
- Your daily-note section and history entry: write them as D 20th did. **ALSO commit the project's own daily note, which D 20th left uncommitted on disk**, IF your project's rules allow you to commit it. Read the project CLAUDE.md first. If they do not, say so in your wrap.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- wed-secuura-storage-27-held-worktrees-1019 = **a** (2026-10-19 11:07:50, live board). Lands in: your manifest and your wrap mail.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- The storage policy's "never in scope" list stands over any list. If the two disagree, the policy wins and you skip. Policy: `/Volumes/DevMASTER/WEDNESDAY/1_Project_Definition/Policies/2026-10-19_secuura-blockchain-storage-policy.md`.

PROVENANCE:
- the 27 held worktrees, 69.85 GiB, the squash-test fault | Seat D 20th's wrap mail 22:33Z and your own 5_Project_History/2026-10-19_seatD-storage/MANIFEST.md (on disk, read by Wednesday 09:3x) | read 2026-10-19
- Kam's ruling | Wednesday's tools/kam_rulings_today.sh (live board) + decision_queue.sh rule - my project, not yours | read 2026-10-19
- R 50th and J 13th are live | tmux pane list read by Wednesday (%8 Secuura/Blockchain-R, %6 Secuura/Blockchain-J) | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 11:12
