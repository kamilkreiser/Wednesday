# Gate brief: GATE A = PR #1552 (KS-1547) + PR #1554 (KS-1542), batched (disjoint files), TIER 2 through-code, Opus

Commissioned by the Wednesday seat, 2026-10-15. Authority past the usage stop: Kam, terminal 2026-10-15 ~12:5x, "if anything needs to be pushed, merged or deployed, do that first as well". Both patches were written by the Spark (DeepSeek V4 Flash) from Wednesday's briefs, checked 7/7, read at source by Wednesday, raised unmodified by Seat R 45th. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- #1552 head 762d044b05c9d1943d4d857e7f99e21b5b8d7e67 (based on develop e67e0dc1): Blockchain/Dev/scripts/preflight/preflight.sh +1/-1 (step() reads the leg denominator up to the first NON-DIGIT instead of the first space) + new Blockchain/Dev/scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh +73/-0. preflight.sh is every developer's push gate.
- #1554 head 3c15af5693fa3d841182a8b4fb2258fc02f825b4 (develop 53b429ed merged in): services/api-gateway/src/routes/verification.ts +10/-1 (a refused non-primitive forward-timeout bound prints as JSON, type tag only if JSON.stringify throws) + its existing test ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts +26/-0.
- Live develop 53b429ed6b4bf4d23c0721bf573b9df1c858bc06 (re-read it yourself). Author's merge prediction: either order lands tree 0b5143d06f5c85a21dfac9e56edd7d6d21067c4d; file sets disjoint.
- Author's claims (NOT evidence): KS-1547 red 2/4 -> green 6/0; KS-1542 red 6/19 -> green 25/25; api-gateway 118 files / 1153 tests passed; in-hook shell suites 89/89 and 88/88.

## Gate
1. Diff each PR by hunk at its head: nothing outside the named files; product vs test.
2. Red-first and green yourself for each named test at the live tip (product reverted -> red for the right reason, with real assertion messages; product applied -> green). For KS-1547 run the bash suite with /bin/bash (3.2) as the repo's runner does.
3. #1552: every leg header in the tree that step() parses (grep the callers) still yields the same denominator; an empty or non-digit denominator ("3/", "3/x") aborts exactly as develop does. Run the preflight-related sibling suites before and after.
4. #1554: what the new branch prints for Date, Map, Set, RegExp and a nested object; all must still be REFUSED. Say whether a printed `{}` for a Map loses information that matters for an operator-supplied config value (severity). Confirm the invariant cell reads the file's DISTINCT table as intended. Run the whole api-gateway suite and tsc (on a program that INCLUDES the test file, with a planted-error control).
5. Mutation: at least two mutants per product hunk that a weak test would miss; each must be killed. Include a comment-only control.
6. Merge prediction on the live tip for each PR alone and both in each order, with an overlap check and a planted conflicting control.

## Rules
Read-only on the project: make your own clone (git clone --shared or the checkout's origin URL with its core.sshCommand) under /private/tmp/claude-501/ and fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; never delete anything (no rm, rmdir, find -delete; make a new uniquely named dir per run instead). **Every loop or multi-step command goes in a script FILE run as `/bin/bash /abs/path/script.sh args`, never inline `bash -c '...'`: an inline script raised a permission dialog twice today and parked the whole fleet for an hour each time.** If a step truly needs a dialog, write evidence/BLOCKED.txt and skip it, naming it in NOT tested. Write only in this folder and your scratch dir (raw outputs under evidence/, never a directory named out).

## Output
0_Brain/reference/2026-10-15_gate-A-pr1552-pr1554/verdict.md: ONE verdict line PER PR on lines 1-2 (GO / GO WITH NOTE / NO GO, each naming its head), sha256/16 of the report on LINE 3 (delete line 3, sha256 the rest, first 16 hex), then FOUND / TESTED / HOW, NOT tested, severities with file:line. Round 1 of 2. Merge only on Wednesday's head-bound GO; nothing deploys.
