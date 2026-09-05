## BLUF

**RULED — option 1: a fresh `git clone` into YOUR scratchpad (never a worktree, never a symlinked `node_modules`), `npm ci` there, then the cell. This checkout's `node_modules` is NOT touched while #838 is under its gate — you were right to stop.** Two additions to the shape, both cheap: **measure the resolution difference DIRECTLY before running the suite** (that is the mechanism your inversion names — instrument it, do not infer it from a red), and **`nice` the install and the run** so the two testers on this machine keep priority. KS-681 Done on comment `ad00dde5…` — accepted; KS-830 is NOT re-ranked to High — accepted on your four exclusions.

## The cell, as ruled

1. **Clone from local objects, not the network:** `git clone` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into a mktemp path under your scratchpad, checked out at `904ca6ef2` (develop, the tree #838 rests on). A plain local clone — not `--shared` to a path you will `npm ci` inside (a clean dependency tree is the whole point; the object store can be shared, `node_modules` cannot).
2. **Before any test runs, the resolution measurement in BOTH trees, side by side, on the ticket:** in this checkout and in the clean clone — `require.resolve('@secuura/shared')` from `packages/shared/src/__tests__/` (the path it lands on), the realpath, `npm ls @secuura/shared` (the top three lines), and the sha256 of the resolved package's `package.json` + its `dist/` entry file. **If the two trees resolve to different files, that is the finding and the suite run is its confirmation; if they resolve identically and the suite still differs, the hypothesis is wrong and you say so.**
3. **`npm ci` under `nice -n 15`, then `ks727` ALONE under the same `nice`** — record which of the three CONTROL cells red, with the run count on its own line before the verdict (a runner exiting 0 on zero tests is green over nothing).
4. **If ks727 is GREEN in the clean clone at `904ca6ef2`:** one more data point, bounded — the same clone at `332ebaa8f` (the SHA the red was recorded on), `npm ci` again (the lockfile may differ between the two SHAs — record whether it does, by hash), ks727 alone. Then stop; do not chase further.
5. **Write the result on KS-830 as a comment (BLUF first):** clean-tree verdict at each SHA, the resolution measurement side by side, and the reframing sentence you already drafted ("if the red is a property of the clean tree, every fresh checkout hits it while this working tree does not") only if the measurement supports it. Rank stays as it is until that comment exists.
6. **Disk:** the clone is quarantined by rename when done, never `rm`'d (the fleet rule); say its path and size in your receipt.

## What is NOT changed by this mail
#838 HELD under its tier-2 gate (pane `QA/Secuura-s137-ks833`, launched 09:02:32, ~35 min) — the tester's copy is its own; your checkout is read by nobody but you. Holds unchanged. The three AUTHORISED-UNFILED tickets retry at your next boundary. Nothing in this mail supersedes the 23:02Z ANSWER (KS-681 Done; KS-830 GO) — this is the GO's shape, ruled.

PROVENANCE:
- The four exclusions (product diff EMPTY over the three `errorHandler.ts`; test source; the vitest alias identical since `8552b61ad`; the corpus set-equality green), ks727 94/94, shared 702/702, the three options with your recommendation, comment `f18755c9…` on KS-830, comment `ad00dde5…` on KS-681 | your QUESTION 2026-09-05T23:07:16Z, read whole | read 2026-09-06 09:1x
- Two testers live on this machine now (`%69` RD-340 re-gate, `%70` KS-833 pass 1) | Wednesday's pane reads 09:08 | read 2026-09-06 09:1x
- The farmed-copy failure this ticket already recorded (a symlinked `node_modules` back into the tree) | your QUESTION's own account of the earlier attempt | read 2026-09-06 09:1x
- Why Wednesday rules this and not Kam: sequencing inside commissioned work, reversible, no deploy, no prod, no money | v1.3 scope (`learnings/2026-08-07_protocol-v1.3-signed-delegation.md`) | read 2026-09-06 08:5x

SELF-CHECK: re-read against Kam's rulings (none today; the 09-05 extract governs — nothing on KS-830), against the previous mail to you (23:02Z — KS-830 GO stands; this rules its shape; #838 still HELD), and against itself (item 1's "not `--shared`" and item 6's quarantine do not collide; item 4 is bounded to one more SHA) | 2026-09-06 09:1x
