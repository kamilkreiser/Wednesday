# Gate brief: GATE F2 = PR #1573 (KS-1490) + PR #1574 (KS-1619 p2) + PR #1575 (KS-1619 p1), TIER 2 through-code, batched (disjoint files), Sonnet

Commissioned by the Wednesday seat, 2026-10-18 ~23:1x AEDT, under model routing v1.0 (row G2: tier-2 gates run on Sonnet; #1574 and #1575 are test-only). If you find anything security-shaped, say so on line 1 and Wednesday hands the PR to a tier-1 Opus gate. Seat R 47th raised all three on develop 9251ae54d. Live develop is 1f73d7ac8cc17add318601c6c572bcace3d5a596 (Wednesday ls-remote 23:1x; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1573 KS-1490 (trailing-slash note only)**, head bd935f41d0b8fd8d142c11e199448c5c44433dfa, 2 files +15/-1: whatsapp-bot verify.ts + the ks812 suite. Unmodified Spark patch per R. Scope: the trailing-slash note only; the dead-host sweep stays open.
- **#1574 KS-1619 part 2**, head 2bc9cb6502a8bac13eac92cf126602c1829b7c85, 1 file +38/-0: originate ks730c test (3-tenant migrate-tenant-data cell, meant to kill gate mutant M4e at adminConfig.ts:2237). Test only.
- **#1575 KS-1619 part 1**, head 8b53b5212fd1b60e7f0a355d57259d2f778af395, 1 file +26/-0: api-gateway ks1087 test (multi-chunk approve-forward reply cell, meant to kill gate mutant M1c at verification.ts:1068). Test only.
- **Author's claims (NOT evidence):** #1573 red-first 2 FAIL (//api and ///api URLs) -> 7/7, connector tsc 0, full shell-suite 90/90; #1574 31/31, M4e reds exactly the new cell; #1575 12/12, M1c reds exactly the new cell; originate 1381, api-gateway 1171. Preflight 13/16 for all (legs 3, 4, 8 skipped).

## Gate
1. Diff each PR by hunk at its head: nothing outside the named files.
2. Red-first and green yourself for each named test at the live tip.
3. #1573: read how the URL is joined before and after. Inputs with 0, 1, 2 and 3 trailing slashes, a path with a query string, and an empty base: what URL comes out? The host part must never change (no new host, no scheme change).
4. #1574 and #1575: plant the named mutant yourself (from-text checked at develop) and confirm it reds EXACTLY the new cell and nothing else; restore and re-run green. Also one mutant the new cell should NOT catch, to show it is specific.
5. One comment-only control per PR; run each owning suite and tsc, before and after.
6. Merge prediction on live develop for each PR alone and all three in at least two orders, with an overlap check and a planted conflicting control. R predicts tree d753dcc43754 for all four (#1573-#1576) in any order.

## Rules
- Read-only on the project. Work in your own clone under /private/tmp/claude-501/ (git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand).
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd, delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your scratch dir.

## Output
- Write 0_Brain/reference/2026-10-18_gate-F2-pr1573-pr1574-pr1575/verdict.md.
- Lines 1-3: one verdict line per PR (GO / GO WITH NOTE / NO GO), each naming its head.
- Line 4: the sha256/16 of the report (delete line 4, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
