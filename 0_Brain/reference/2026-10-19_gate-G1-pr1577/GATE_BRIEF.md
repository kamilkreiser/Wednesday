# Gate brief: GATE G1 = PR #1577 (KS-1482), TIER 1 FULL, Opus (the push hook itself)

Commissioned by the Wednesday seat, 2026-10-19 ~01:0x AEDT, under model routing v1.0 (row G1: a change to a security guard, here the pre-push gate, gets a tier-1 Opus gate). Seat R 48th raised it. Live develop 8a9970511f22661d92f634058fae8c08c656124f (Wednesday ls-remote 01:0x; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1577 KS-1482**, head 83b955a6f8db11ed80af4550b7da2bc4d0203a2a, 2 files +35/-3: `.githooks/pre-push` gains `--no-renames` at three `git diff --name-only` sites (near :129 and :143 in `_judge_ref`, near :252 in the no-upstream branch) + 3 RED cells, each paired with a CONTROL, in `Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh`. Unmodified Spark patches (two parts) per R.
- **Author's claims (NOT evidence):** red-first ks998 77/3 (the three new cells), green 80/0; full shell runner 90/0 on the pushed head; the push itself ran the patched hook; "fails closed: --no-renames only makes the changed set larger".

## Gate (tier 1 FULL)
1. Diff by hunk at the head: nothing outside the two named files.
2. **Census the whole hook, not the three sites:** grep `.githooks/pre-push` (and every script it sources or calls) at the head for EVERY `git diff`, `git log`, `git show`, `diff-tree` or `--name-status`/`--name-only` read. Is any other changed-set read still rename-blind, or a different rename/copy shape (`-C`, copies, `git log --follow`)? Name each and say whether it decides a refusal.
3. **Fail-closed claim, tested both ways:** a rename OUT of Blockchain/Dev (must now run the preflight), a rename INTO it, a rename WITHIN it, a copy, and a pure delete. For each: does the preflight run, and could any of them now make a previously-refused push pass? Use the suite's own fixture builder.
4. Red-first and green yourself at the live tip; plant a mutant per site (remove `--no-renames` from each of the three in turn): each must be killed by a named cell. Comment-only control.
5. The FULL shell runner on the merge-predicted tree; the ks998 suite twice (flakiness).
6. Merge prediction on live develop alone and with #1578 in both orders (R predicts tree 8cda8b91829d), an overlap check and a planted conflicting control.

## Rules
- Read-only on the project. Work in your own clone under /private/tmp/claude-501/ (git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand). Build `packages/shared` in your clone before any suite (`npm run build -w packages/shared` in Blockchain/Dev after `npm ci`): an unbuilt shared turns suites into false failures (R 48th, 12:46Z).
- No git write verb in !CODING, no push to origin (your fixtures push only to their own local bare remotes), no GitHub or Linear writes, no Docker.
- Never cd, delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your scratch dir.

## Output
- Write 0_Brain/reference/2026-10-19_gate-G1-pr1577/verdict.md.
- Line 1: the verdict (GO / GO WITH NOTE / NO GO) naming the head. Line 2: a one-line headline.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
