# Gate brief: GATE G2 = PR #1578 (KS-1497 items 2 + 4), TIER 2 through-code, Sonnet

Commissioned by the Wednesday seat, 2026-10-19 ~01:0x AEDT, under model routing v1.0 (row G2: tier-2 gates run on Sonnet; build tooling). If you find anything security-shaped, say so on line 1 and Wednesday hands the PR to a tier-1 Opus gate. Seat R 48th raised it. Live develop 8a9970511f22661d92f634058fae8c08c656124f (Wednesday ls-remote 01:0x; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1578 KS-1497 items 2 + 4 (NARROWED; the ticket stays open)**, head 972286126bc69fad209ef4c270aca94f4d8f4c9f, 2 files +78/-0: `Blockchain/Dev/scripts/prisma-generate.cjs` refuses a symlinked or non-directory `node_modules/.generate` (lstat, then the script's own `fail()`, exit 2) before mkdirSync; NEW suite `Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh` (7 cells). Unmodified Spark patch per R.
- **Author's claims (NOT evidence):** red-first 2/5 (the 2 passes are controls; "nothing is written into the symlink's target" wanted 0 got 1 at the tip), green 7/0, full shell runner 91/0 (90 -> 91 = the new suite picked up). Named residuals (NOT to be scored as findings unless worse than stated): the lstat/mkdir race; a symlinked node_modules ABOVE .generate.

## Gate
1. Diff by hunk at the head: nothing outside the two named files.
2. Red-first and green yourself at the live tip.
3. Every staging shape: absent (must still work: run the suite's normal-generate cell), a plain directory left over from a crash (must still work), a symlink to a directory, a symlink to a file, a dangling symlink, a regular file. Exit code and message for each; nothing written outside the service tree in any.
4. The `lstat` error path: what does a non-ENOENT error (e.g. EACCES on a parent) do now? It rethrows: say whether that is acceptable for a build script.
5. Two mutants on the product hunk (lstat -> stat; drop the isDirectory branch) plus a comment-only control; each mutant killed by a named cell.
6. Merge prediction on live develop alone and with #1577 in both orders (R predicts tree 8cda8b91829d), an overlap check and a planted conflicting control.

## Rules
- Read-only on the project. Work in your own clone under /private/tmp/claude-501/ (git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand). Build `packages/shared` in your clone before any suite (`npm run build -w packages/shared` in Blockchain/Dev after `npm ci`).
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd (use absolute paths and `-p`/`--prefix` flags), delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your scratch dir.

## Output
- Write 0_Brain/reference/2026-10-19_gate-G2-pr1578/verdict.md.
- Line 1: the verdict (GO / GO WITH NOTE / NO GO) naming the head. Line 2: a one-line headline.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
