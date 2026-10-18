## BLUF

You are a Secuura/Blockchain seat on the D lane (Secuura/Blockchain-D), commissioned for ONE job: the first removal round of the approved Platform K storage policy. **Kam approved it on his live board at 07:24:57 AEDT today: card `wed-secuura-storage-policy-1019` = a "Approve the policy and the first removal".** Option text, verbatim: "A Secuura seat removes the 371 GB set from today's dry-run report (merged clean worktrees plus regenerable node_modules), re-checking liveness at the moment of removal, with counts and disk space before and after. Weekly removals of the same classes then need no card." The policy is `/Volumes/DevMASTER/WEDNESDAY/1_Project_Definition/Policies/2026-10-19_secuura-blockchain-storage-policy.md` (Wednesday's project; read it whole, read-only). This narrows the never-delete rule for exactly these classes and nothing else.

## QUEUE

1. **Read first, read-only:** the policy, then the dry-run report `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_storage-policy/dryrun_2026-10-19.md` (every candidate path with size, age and verdict) and `MEASUREMENT.md` beside it. Your removal list is the report's CANDIDATE rows for classes **W** (merged-clean worktrees + deploy clones, 181 items, ~200 GiB), **N** (`node_modules` in kept working copies idle 14 d+, 107 sets, ~166 GiB), **E** (one regenerable `node_modules` inside `5_Project_History/quarantine/2026-09-15-s233/`, ~1.4 GiB) and **T** (4 test-output dirs, ~2.7 MB). NOT class R or S (those are in Wednesday's tree; Wednesday does them).
2. **Before anything:** `df -h /Volumes/DevMASTER` and a count of `Blockchain/worktrees/*` and `Blockchain/deploy-clones/*`, written to your manifest.
3. **Re-check every candidate AT THE MOMENT of its removal, in a script FILE, and SKIP (never remove) any that fails:** (a) no process has its cwd inside it (`lsof +D` is slow: use `lsof -a -d cwd` over the live claude/node pids, and the two live seats' known worktrees below); (b) nothing inside modified in the last 48 h; (c) for W: `git -C <worktree> status --porcelain` empty AND its HEAD still contained in the local `origin/develop` (or squash-equivalent, as the dry-run measured it; no fetch needed: merged stays merged); (d) for N/E: the path's basename is exactly `node_modules`.
4. **How to remove:** W = `git -C <the main checkout> worktree remove <path>` WITHOUT `--force` (a refusal means it is not clean: skip and list it); a deploy clone or an unregistered checkout = skip and list (not removed in this round). N/E/T = remove that directory only. Never a path outside `Blockchain/worktrees/`, `Blockchain/deploy-clones/`, `Blockchain/5_Project_History/quarantine/2026-09-15-s233/` and the four T dirs. **Expansions guarded (`${P:?}`), every path absolute, refuse a path that is `/`, the project root, `2_Project_Files`, or any path not on the report's list.**
5. **After:** `df -h` again, the counts again, and a manifest file in your own `5_Project_History/2026-10-19_seatD-storage/` listing every path removed (class, size from the report), every path skipped and why, totals per class, and df before/after. Then a STATUS mail to Wednesday, BLUF-first, and wrap.

## PARTITION

Yours: only the report's candidate paths in the classes above. **NOT yours, never touched even if listed:** the main checkout `2_Project_Files`; anything Seat R 49th (Secuura/Blockchain-R) or Seat J 13th (Secuura/Blockchain-J) is using: both are LIVE now (KS-1628 PRs and #1568 round 3); measure their cwds and treat every worktree either has touched in 48 h as live. `Blockchain/scratchpad/` (class P: no candidates this round). Records in `5_Project_History` (reports, evidence, mail, HANDOVER, history.md). Credentials. You share one inbox with R and J: a mail addressed to them is not yours.

## HOLDS

- No deploy, no push, no PR, no merge; this round changes no code. No git write verb other than `worktree remove` (no `prune`, no `branch -D`, no `gc`, no `fetch`).
- STOP and mail Wednesday on any surprise: a removal error, a candidate that is on the list but looks live, a count that disagrees with the report by more than a few items, or free space that does not move as expected.
- Never edit a script while it runs; every loop in a script FILE run with `/bin/bash`, never inline.
- Client-facing communication: none needed for this job.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- wed-secuura-storage-policy-1019 = **a** (2026-10-19 07:24:57, live board). Lands in: your manifest + your STATUS mail.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- The policy's "never in scope" list stands over the report: if the two disagree, the policy wins and you skip.

PROVENANCE:
- the policy, the dry-run report and MEASUREMENT.md | /Volumes/DevMASTER/WEDNESDAY/1_Project_Definition/Policies/2026-10-19_secuura-blockchain-storage-policy.md and /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_storage-policy/ - my project, not yours | read 2026-10-19
- Kam's ruling | Wednesday's tools/kam_rulings_today.sh (live board) + tools/decision_queue.sh rule - my project, not yours | read 2026-10-19
- R 49th and J 13th are live | tmux pane list read by Wednesday (%5 Secuura/Blockchain-R, %6 Secuura/Blockchain-J) | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 07:27
