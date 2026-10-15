# Gate brief: GATE B = PR #1556 (KS-1543 part 1 of 2), TIER 2 through-code, alone, Opus

Commissioned by the Wednesday seat, 2026-10-15. Authority past the usage stop: Kam, terminal 2026-10-15 ~12:5x, "if anything needs to be pushed, merged or deployed, do that first as well". A Spark (DeepSeek V4 Flash) patch from Wednesday's brief, checked 7/7, read at source, raised unmodified. 0_Brain paths relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- Head 67b763305a0b3c70f652868c350e294883995543 (author's ls-remote; re-read refs/pull/1556/head yourself). Live develop 0bb4f17ca5010baa3ad9d91b790522e87b8c9dc1 is an ancestor of the head (author's claim; check it).
- Change: services/api-gateway/src/routes/verification.ts +2/-2: two catches that deliberately ignore their error (the live-anchor fall-through, ~:661; the rejected-document DB fallback, ~:1503) become a bare `catch {`; new test src/__tests__/ks1543-five-pre-existing-eslint-warnings-in.test.ts +47/-0, which lints the real file through ESLint's Node API (plus a planted-binding control and a 0-errors control). The shared config has no caughtErrorsIgnorePattern, which is why `_err` warned.
- Author's claims (NOT evidence): red 2/4 -> green 4/4; ESLint 5 -> 3 warnings, exactly those two lines gone; leg-16 ratchet 0 new; api-gateway suite all passing.

## Gate
1. Diff by hunk: only those two catch lines in the product; the catch bodies and comments unchanged; behaviour unchanged (an empty catch drops the same exceptions as before).
2. Red-first and green yourself, and run ESLint on the file before and after (count by rule and line).
3. Is the new test robust? It locates each catch by an anchor comment: does it fail cleanly (not vacuously) if a comment is reworded or the file moves; does `lintFiles` from cwd Blockchain/Dev really pick up the repo's flat config; its runtime.
4. Whole api-gateway suite and tsc on a program that INCLUDES the test file (planted-error control).
5. Two mutants (restore one binding; delete a catch body line), plus a comment-only control.
6. Merge prediction on the live tip (re-read it), overlap + a planted conflicting control.

## Rules
Read-only on the project: your own clone under /private/tmp/claude-501/, fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; delete nothing (no rm, rmdir, find -delete). **Every loop or multi-step command goes in a script FILE run as `/bin/bash /abs/path/script.sh args`, never inline `bash -c '...'`.** Run npm/npx/vitest ONLY with the clone's api-gateway as the working tree (`npm --prefix <clone>/Blockchain/Dev/services/api-gateway`, and check that no file appears under /Volumes/DevMASTER/WEDNESDAY/node_modules). Write only here and in your scratch dir.

## Output
0_Brain/reference/2026-10-15_gate-B-pr1556/verdict.md: VERDICT on line 1 naming the head, sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. Round 1 of 2. Merge only on Wednesday's head-bound GO; nothing deploys.
