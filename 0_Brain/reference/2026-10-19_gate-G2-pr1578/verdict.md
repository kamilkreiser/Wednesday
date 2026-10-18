GO WITH NOTE - PR #1578 head 972286126bc69fad209ef4c270aca94f4d8f4c9f on live develop 8a9970511f22661d92f634058fae8c08c656124f (tier 2, Sonnet, round 1 of 2)
Headline: the fix does what it claims for every staging shape, red-first 2/5 and green 7/0 reproduced, both mutants killed, merges with #1577 clean in both orders to tree 8cda8b91829d; one pre-existing unrelated suite fails in the full runner (also on develop), so the author's 91/0 was not reproduced.
sha256/16: d6d6831b3adf745e
# Findings detail

Scope: Secuura only. Project checkout untouched; all work in a --shared clone at /private/tmp/claude-501/g2w/repo. Live develop re-read at fetch time: 8a9970511f22661d92f634058fae8c08c656124f (matches the brief). Head: 972286126bc69fad209ef4c270aca94f4d8f4c9f. Merge base = develop tip (PR is a clean one-commit-ahead branch).

## FOUND
- No security-shaped finding. The change is hardening (stops a write through a planted symlink); nothing new is introduced. No blocking finding.
- F1 (LOW, informational) Blockchain/Dev/scripts/prisma-generate.cjs:71-74: a non-ENOENT lstat error is rethrown (uncaught stack trace, rc 1) instead of going through fail() (rc 2). Acceptable for a build script: it still fails loud and writes nothing, and it is effectively unreachable, because the earlier `require.resolve` checks (lines ~50-60) already need execute permission on node_modules, so a chmod 000 node_modules is caught first and exits 2 with "prisma CLI is not installed" (measured). Only a race between those checks and the lstat could reach it. Same class as the author's named lstat/mkdir race. Not scored beyond this note.
- F2 (LOW, test coverage) The suite has no cell for symlink-to-file or dangling symlink; they are covered only by the product code (both measured below, correct). Mutant lstat->stat would still be caught by the symlink-to-directory cells, so the suite is not blind to the product line. Optional follow-up, not a blocker.
- F3 (INFO, pre-existing, not this PR) systemTest/__tests__/package_format_gate.test.sh fails 5 cells when run through `npm run test:shell` in my environment (hanging-postinstall / private-HOME cells), on live develop too (develop: 89 passed 1 failed of 90). It passes standalone (rc 0) at both develop and the PR head. So the author's "91/0" is not reproduced here: I get 90/1 of 91, and the one failure is identical at develop and unrelated to the two files. Likely environmental (my clone, macOS, npm config); flag for Wednesday to compare against her own run.

## TESTED (all at the live tip, by me)
1. Diff by hunk: `git diff origin/develop...pr1578` = exactly 2 files, +78/-0: prisma-generate.cjs (+13, one hunk at the staging block, after `const staging = ...`, before mkdirSync) and the new suite (new file, mode 100755). Nothing else.
2. Red-first / green: at the PR head the suite is 7 passed 0 failed rc 0. Same suite against develop's script (via PRISMA_GENERATE_CJS) is 2 passed 5 failed rc 1: both controls pass, the symlink exit/message/"nothing written into target" cells fail (got 0 / no / 1 file) and the file exit/message cells fail (got rc 1 / no). This matches the author's 2/5 claim exactly, including "wanted 0 got 1".
3. Staging shapes, real script vs fixture service, PR head (rc; message; written outside?):
   - absent: rc 0, generates, no .generate left, nothing outside.
   - plain leftover dir (crash): rc 0, reused and removed, nothing outside.
   - symlink to directory: rc 2, "is a symbolic link; refusing ...", target dir empty, link untouched. (develop: rc 0 and schema.prisma written INTO the target dir, confirming the bug.)
   - symlink to file: rc 2, same message, target content unchanged. (develop: rc 1 stack trace.)
   - dangling symlink: rc 2, same message, target not created. (develop: rc 1 stack trace.)
   - regular file: rc 2, "exists and is not a directory", content intact. (develop: rc 1 stack trace.)
   - extras: self-referential symlink rc 2; FIFO rc 2 "not a directory"; both refused, nothing written.
   - Nothing was written outside the service tree in any shape; find over the fixture roots showed no stray files.
4. lstat error path: measured chmod 000 node_modules: script exits 2 at the earlier prisma-resolution check (never reaches lstat). Direct emulation of the hunk with EACCES on the parent: rethrows, rc 1, stack trace. Judgement in F1.
5. Mutants (via PRISMA_GENERATE_CJS on a copy): M1 lstat->stat: killed, 3 cells fail (symlinked .generate refused with exit 2; refusal says so; nothing written into target). M2 drop the isDirectory branch (`if (false)`): killed, 2 cells fail (file refused with exit 2; file refusal message). Comment-only control (comment reworded): 7/0 survives, as it should.
6. Merge prediction (git merge-tree --write-tree, git 2.51.0): develop+1578 clean (tree b06e7dab8114); develop+1577 clean (6d9f9cb691dc). #1577 touches .githooks/pre-push and ks998_pre_push_judges_the_push.test.sh only: zero file overlap with #1578. Both orders (1577 then 1578, 1578 then 1577) clean and produce the same tree 8cda8b91829d44b22cdcf28b653c106be6378c87, which matches R's 8cda8b91829d prediction. Planted conflicting control (a develop-based commit editing the mkdirSync line, merged with #1578) correctly CONFLICTs in prisma-generate.cjs, so the check can fail. (My planted blob carried mode 100755 vs 100644, an extra mode difference in the control only; the content conflict is real and independent.)
7. Full runner: `npm ci --ignore-scripts` + `npm run build -w packages/shared` + `npm run test:shell` at the PR head: 91 suites found (90 -> 91 confirmed, the new suite is picked up: "ks1497 ...: 7 passed, 0 failed"), 90 passed, 1 failed (F3), reproduced twice. Develop baseline runner: 89 of 90 passed, 1 failed, the same suite.

## HOW
Scripts in /private/tmp/claude-501/: g2_setup.sh, g2_a.sh (green/red), g2_shapes.sh (shape matrix, run against PR script and develop script), g2_eacces.sh, g2_mut.sh, g2_merge.sh, g2_full*.sh, g2_base.sh; outputs under /private/tmp/claude-501/g2w/out/. All loops in script files run with /bin/bash. Nothing pushed or written to GitHub/Linear; no git write verb in !CODING.

## NOT tested
- The lstat/mkdir race and a symlinked node_modules above .generate (author's named residuals; not scored).
- Real `prisma generate` (the suite and my shapes use the stub CLI, as the suite does); services/originate with the real schema and Docker not run.
- Whether the F3 failure also occurs on the author's/CI machine; I only show it is identical at develop here.
- Other OS (Linux) behaviour of lstat on FIFO/special files; macOS only.
- A real EACCES arriving at the lstat (unreachable without a race), only emulated.

WALL-CLOCK: 33
