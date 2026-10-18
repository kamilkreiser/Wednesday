# Gate brief: GATE F1 = PR #1576 (KS-1114 follow-up), TIER 1 FULL, Opus

Commissioned by the Wednesday seat, 2026-10-18 ~23:1x AEDT, under model routing v1.0 (row G1: a Spark edit on the public verify route gets a tier-1 Opus gate). Kam ruled card secuura-ks1114-deleted-status-found-by-title-1018 = a at 20:55:56 ("Ship as built, hide 'deleted' in a follow-up"); the option detail as amended by Wednesday: make the hidden set case- and space-insensitive and add 'deleted' and 'expired'. Seat R 47th raised the PR on develop 9251ae54d. Live develop is 1f73d7ac8cc17add318601c6c572bcace3d5a596 (Wednesday ls-remote 23:1x; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1576 KS-1114 follow-up**, head 252e53d633d7fda0becd0eefc2ad65525e9e8544, 3 files +178/-8:
  - services/originate/src/routes/verification.ts: the title-lookup predicate becomes lower(btrim(d.status)) NOT IN ('draft','revoked','deleted','expired') (Spark patch, unmodified per R) + a comment.
  - a new unit test file (Spark, unmodified per R) and the T11 integration re-pin (night/briefs/ks_1114_p2/integration_T11_followup.diff, unmodified per R).
- **Author's claims (NOT evidence):** unit red-first 4 fail/3 pass -> 7/7; T11 run on a real PG 15 with all 51 migrations, red without the product line, 17/17 as superuser and as secuura_app; ks1119 + ks1557 green as secuura_app; originate 1387/1387; tsc 0. Preflight 13/16 (legs 3, 4, 8 skipped, local stack not up).

## Gate (tier 1 FULL)
1. Diff by hunk at the head: nothing outside the three named files.
2. **NULL semantics, the first question:** the previous predicate (PR #1555, merged 833984fc9) was a NULL-safe exclusion of draft + revoked (Wednesday's 08:3xZ ruling to J). Under `lower(btrim(NULL)) NOT IN (...)` a NULL status yields NULL and the row drops out of the lookup. Measure, on a real Postgres, what a NULL-status document returned BEFORE (at 833984fc9) and AFTER (at the head) for a title hit. If the behaviour changed, say which way and whether any writer can store NULL (grep the writers of documents.status and the column's DDL/default/constraint across all 51 migrations).
3. The reply shape is unchanged: a hit is still exactly {"verified":false,"checks":{"documentExists":true}}, and a hidden status answers byte-identically to not-found. Test with each hidden status in mixed case and with leading/trailing spaces, plus a tab (tabs are NOT trimmed by btrim's default: the brief states it as narrowing; confirm and record).
4. Tenancy: the lookup stays tenant-bound in both modes (superuser and secuura_app, RLS on), cross-tenant title = not-found.
5. Red-first and green yourself for the unit test and T11 at the live tip, on your OWN Postgres (never the seat's 55473 or 55418).
6. At least three mutants on the product hunk (drop one status, drop lower(), drop btrim()) plus a comment-only control; each mutant must be killed by a named cell.
7. Index/plan: EXPLAIN the lookup before and after on a seeded table; say whether the function wrap changes the plan.
8. Merge prediction on live develop alone, with an overlap check and a planted conflicting control. R predicts tree d753dcc43754 for all four PRs (#1573-#1576) in any order.

## Rules
- Read-only on the project. Work in your own clone under /private/tmp/claude-501/ (git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand).
- No git write verb in !CODING, no push, no GitHub or Linear writes. Docker only for your own throwaway Postgres on a port you check is free first.
- Never cd, delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your scratch dir.

## Output
- Write 0_Brain/reference/2026-10-18_gate-F1-pr1576/verdict.md.
- Line 1: the verdict (GO / GO WITH NOTE / NO GO) naming the head. Line 2: blank or a one-line headline.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
