# Gate brief: GATE E1 = PR #1570 (KS-1613) + PR #1572 (KS-1545), TIER 1, batched (disjoint files)

Commissioned by the Wednesday seat, 2026-10-18 ~21:5x AEDT, under model routing v1.0 (Kam approved 20:55:59): tier-1 gates run on Opus. **This same brief is ALSO run by a second, independent gate on Fable 5.1 (the v1.0 decision-7 trial).** Each gate writes its own verdict file (named below) and must NOT read the other's folder. Both PRs were raised by Seat R 47th on develop 1197ab38a; live develop is 833984fc94acf6bc00ff8e5d6642fa768dd44e09 (Wednesday's ls-remote ~21:5x; re-read it). Heads equal R's table. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1570 KS-1613 items 1+2**, head 2355d1b6b9bcd977b574725b4849913af3cf501c. Blockchain/Dev/scripts/preflight/preflight.sh (step(): the abort message quotes the header's text after the slash; `_hdr_tail` introduced) + scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh (cells killing the #1552 gate's mutants N7/N5/N4). **This is every developer's push gate**: a defect here breaks every push. A Spark (DeepSeek V4 Flash) patch, unmodified.
- **#1572 KS-1545 step 1**, head 778a610bf0afeab8475f5cebb86e8312515487b2. services/api-gateway/src/routes/platform.ts (the platform audit-log route warns when it drops the platform half; 3 sites) + a NEW test ks1545-platform-audit-log-logs-the-dropped-platform-half.test.ts (+135/-1). **The Spark's code (its counter is spent: both rounds failed only the hunk-header line check), re-anchored by Seat R.** It is an audit surface.
- Author's claims (NOT evidence): KS-1613 red-first 2 FAIL / 10 ok, green 12/12, the full shell-suite runner 90/90, bash -n 0, modes 100644, its own push ran the changed step(); KS-1545 red-first and green (see the PR's Test Evidence), api-gateway suite green. All four of R's PRs land the same tree 6581d8d6db39 in either order on 833984fc9. Preflight 13/16 (legs 3, 4, 8 skipped, local stack not up).

## Gate
1. Diff each PR by hunk at its head: nothing outside the named files.
2. #1570: run the shell test yourself with /bin/bash (3.2) red-first and green; run EVERY other preflight-related suite before and after; prove every leg header in the tree that step() parses still yields its denominator and aborts exactly as develop does on empty and non-digit ones; read the new message for anything an attacker-controlled header could inject (quotes, escapes, newlines, `$()`); at least two mutants per hunk plus a comment-only control.
3. #1572: read all three sites of the audit route in full. What exactly is logged when the platform half is dropped (no secret, no request body, no token, bounded length)? Does any audit row or HTTP reply change? Red-first and green yourself; mutants (at least two per site) plus a comment-only control; the api-gateway suite and tsc on a program that includes the new test, with a planted-error control.
4. Merge prediction on the live develop for each PR alone and both in each order, with an overlap check and a planted conflicting control.

## Rules
Read-only on the project: your own clone under /private/tmp/claude-501/ in a folder named for YOUR gate (e1-opus or e1-fable). Use git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git, and fetch with that checkout's core.sshCommand plus `-o ServerAliveInterval=30`. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; delete nothing. **Every loop or multi-step command goes in a script FILE run as `/bin/bash /abs/path/script.sh args`, never inline `bash -c '...'`.** Pick free ports via lsof. If a step needs a permission dialog, write evidence/BLOCKED.txt and skip it. Write only in your own verdict folder (below) and your scratch dir.

## Output
- The Opus gate writes 0_Brain/reference/2026-10-18_gate-E1-pr1570-pr1572/opus/verdict.md.
- The Fable gate writes 0_Brain/reference/2026-10-18_gate-E1-pr1570-pr1572/fable/verdict.md.
- Format: ONE verdict line PER PR on lines 1-2 (GO / GO WITH NOTE / NO GO, each naming its head), sha256/16 of the report on LINE 3 (delete line 3, sha256 the rest, first 16 hex), then FOUND / TESTED / HOW, NOT tested (legs 3, 4, 8 at least), and severities with file:line.
- Also add a final line `WALL-CLOCK: <minutes>`.
- This is round 1 of 2. A merge happens only on Wednesday's head-bound GO, and nothing deploys.
