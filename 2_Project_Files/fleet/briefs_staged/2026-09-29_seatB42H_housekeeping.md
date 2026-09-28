# LAUNCH BRIEF (Secuura/Blockchain-B, housekeeping seat "Seat H 29-09"): delete the node_modules of stale Secuura worktrees, per Kam's ruling (b). Measure before and after. Nothing else. From Wednesday

## BLUF
DevMASTER is FULL (1,518 MiB free of 1.8 TiB). **Kam ruled card `wed-devmaster-full-secuura-worktree-node-modules` = (b), "Delete those node_modules", on the live board at 08:05:14 AEST 2026-09-29**, with the note: "there is no need to keep historical CI files. these seem to be very hungry in terms of storage so limit storing what has been used and no longer needed." You are a short, single-purpose seat on the B lane. **You delete directories named `node_modules` inside stale worktrees, and nothing else.** No product work, no PR, no ticket, no push, no mail to any human.

**Another seat is LIVE on the A lane: Seat B 42nd** (pane `Secuura/Blockchain`). It shares your inbox (`secuura-blockchain@agentmail.to`). A mail naming Seat B 42nd is NOT yours. Its worktrees are on `/System/Volumes/Data` (a session scratchpad), not under `worktrees/`; you must still prove you touch none of them (step 2).

## THE SCOPE, EXACTLY (the card's option text)
"a Secuura seat [removes] node_modules only (never source, never git state) from worktrees untouched for more than 3 days and whose seats have wrapped ... then re-measures df."
- **Root:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/` — its immediate subdirectories are the worktrees.
- **Stale = the worktree's top-level directory mtime is more than 3 days old** (`find <root> -mindepth 1 -maxdepth 1 -type d -mtime +3`). Wednesday counted **307** of **448** at 08:0x AEST. Re-count; if your count differs, report both and use yours.
- **Delete ONLY directories whose basename is exactly `node_modules`, at any depth inside a stale worktree** (the monorepo has several: `Blockchain/Dev/node_modules`, per-service and per-package ones). Never a file, never a `.git` file or directory, never `git worktree remove` / `prune`, never anything outside a stale worktree, never the shared checkout `2_Project_Files/`.

## STEPS
1. **Before:** `df -m /Volumes/DevMASTER`; the stale list to a file in YOUR record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatH-housekeeping/` (it is small; everything else goes on the Data volume); for a SAMPLE of 5 stale worktrees, `du -sm` their node_modules dirs (a full du over 300 GB times out; sample and extrapolate, and say it is a sample).
2. **Exclusions, proved:** list every worktree path registered to a LIVE process (`lsof +D` is too slow; instead: `ps -axo pid,command` for claude/node processes, then `lsof -a -p <pid> -d cwd` for each) and every path named in Seat B 42nd's brief; assert NONE is in the stale list. Any overlap → remove it from the list and say so.
3. **Dry run:** write the exact list of `node_modules` directories you WOULD delete (`find <stale wt> -type d -name node_modules -prune`), with a count. A positive control: the list contains `<one stale wt>/Blockchain/Dev/node_modules` if that path exists. A negative control: it contains nothing outside the stale worktrees and no path containing `/.git/`.
4. **Delete** from that list only, in batches, logging each path. `rm -rf -- "<path>"` with the path quoted and guarded (`${P:?}`; refuse any path that does not end in `/node_modules` or does not start with the root).
5. **After:** `df -m /Volumes/DevMASTER`; re-run the dry-run finder over the same stale list and show it now returns 0; `git -C <3 sampled stale worktrees> status --porcelain | wc -l` shows the SAME value as before (node_modules is ignored, so porcelain must not change — a change means you touched source).
6. **Mail Wednesday** one STATUS (FOUND / TESTED / HOW): before/after df, count deleted, the sample sizes, the exclusion proof, the porcelain control, anything you could not do. Then wrap cold (history entry + handover in your record folder). You do not rotate into other work.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- wed-devmaster-full-secuura-worktree-node-modules: "b — Delete those node_modules | note: there is no need to keep historical CI files. these seem to be very hungry in terms of storage so limit storing what has been used and no longer needed" -> must land in YOUR STATUS mail and your handover in `5_Project_History/2026-09-29_seatH-housekeeping/` (the before/after df is the receipt).
- The other Secuura cards `decision_queue.sh list ruled --undelivered secuura-` prints (older rulings on build work: identity, advisories, KS-1011, KS-1081 and others) are NOT this seat's scope; they belong to build seats' briefs. Listed here only so the omission is visible, not so you act on them.

## HOLDS
- This is the ONE deletion Kam authorised. Nothing else is deleted, including other "historical CI files": NAME any large regenerable leftovers you notice (QA clones, caches) in the STATUS; do not remove them.
- No push, no PR, no ticket, no Linear write, no git write verb on `2_Project_Files` or any worktree's git state.
- Never touch Seat B 42nd's worktrees, lock (`worktrees/.push-lock-38`) or record folder.
- STOP and mail Wednesday on any surprise (a path outside the root, a porcelain change, a live process in a stale worktree).
- Necessity (cloud): Wednesday may not delete another project's files, and a local model cannot run shell work on this drive.

PROVENANCE:
- Kam's ruling (b) + note | bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show wed-devmaster-full-secuura-worktree-node-modules, and kam_msgs.sh (live, 08:05:14) | read 2026-09-29 08:0x
- 448 worktrees, 307 stale (mtime +3), DevMASTER 1,518 MiB free | find /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees -mindepth 1 -maxdepth 1 -type d [-mtime +3] | wc -l ; df -m /Volumes/DevMASTER | read 2026-09-29 08:0x
- Seat B 42nd live on the A lane, worktrees on the Data volume | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-29_seatB42_build.md | read 2026-09-29 08:0x

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 08:09
