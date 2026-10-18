# Gate brief: GATE K1 = PR #1586 (KS-1627), test-only follow-up to the KS-1540 fail-closed read, Opus

Commissioned by the Wednesday morning seat, 2026-10-19 ~06:1x AEDT, under model routing v1.0 row G2: the PR is tests-only, but it pins the mechanism of a TIER-1 surface (the KS-1540 fail-closed allow-list read, gated tier 1 by gate H1 overnight), so G2's "Opus 1st if the follow-up's mechanism sits on a G1 surface" clause applies. Seat R 49th raised it from a held Spark pass. Live develop 840ac4182d750d38ace9bea578e7fc6af100fd7b and head b12f56e303ac36a3e7adecfa4aab9fdeda3c384a (Wednesday `git ls-remote` ~06:1x; re-read both). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1586 KS-1627**, head b12f56e303ac36a3e7adecfa4aab9fdeda3c384a, ONE new test file, +68/-0, product untouched (author's claim; verify). It mounts `createHealthRoutes({}, realRedis)` with the REAL `services/redis` module, never initialised (in-memory fallback), over real HTTP behind the real `authenticateToken(true)`: 2 CONTROL cells (the export exists and reads false; the settings read resolves to null, not a throw) and 2 RED cells (empty fallback store; a restrictive list written into the fallback store), both requiring 503 `SERVICE_UNAVAILABLE` with the create path's text and no `allowedDocumentTypes`.
- **Why it exists:** gate H1's LOW residual on #1582 (KS-1540): nothing pinned the real module's `isRedisAvailable`, and the info reader's guard uses optional chaining, so a rename would make the guard silently inert. Gate H1's verdict: 0_Brain/reference/2026-10-19_gate-H1-pr1582-pr1584/verdict.md (read its residual paragraph).
- **Author's claims (NOT evidence):** suite 4/4; red-proof with `health.ts:53` calling `isRedisReachable` gives exactly the 2 RED cells red and both controls green; api-gateway 1195/1195; `tsc --noEmit` rc 0; leg 16 `check.cjs` 35 errors = 35 baseline; patch byte-identical to `local-model/night/briefs/ks_1627_p1/golden.diff`; committed blob 0886e4639a9af56dda0140fd06a9af2077e0ad29; overlap 0 with the 23 open PRs. R disclosed a tamper left in its working tree by a mis-scoped EXIT trap, restored before the commit (check the committed tree is clean of it).

## Gate
1. Diff the PR at its head: exactly one new file under `services/api-gateway`, nothing else; the blob id equals the claimed one.
2. Red-first and green yourself at the live tip: run the suite untampered (4/4), then the author's tamper (rename the call at the health route's guard to a name the module does not export) and confirm EXACTLY the two RED cells fail while both controls pass (2 failed + 2 passed, never 0+0). Restore and assert the blob equals develop's.
3. **The silent case, which is why this PR exists:** plant a rename of `isRedisAvailable` IN THE REAL MODULE (`services/redis`) and update every caller the compiler would force EXCEPT the optional member the health route reads, and confirm this suite reds. Then the opposite control: a rename applied everywhere (route included) must leave the suite green or fail loudly at compile, and say which. State plainly whether the suite catches the failure H1 named.
4. Independence of the controls: name what each CONTROL cell does NOT share with the RED cells, and whether a broken import (module path wrong) would make all four fail identically (it should: say so) rather than pass.
5. The test runs the real `authenticateToken(true)`: confirm it does not depend on a secret, a network call, a live Redis, a database or a wall-clock that differs between machines; note any env var it sets and whether it leaks into other suites in the same run (run the full api-gateway suite before/after, and this file alongside its neighbours in one run).
6. Merge prediction on live develop (tree id), an overlap check against the open PRs and a planted conflicting control.

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/k1/ — create it and use nothing else in that scratchpad (other folders there belong to other agents).** Clone there with `git clone --shared` from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git in YOUR clone, and fetch with that checkout's `core.sshCommand` (read it with `git config --get`). Build `packages/shared` (`npm ci` then `npm run build -w packages/shared` in Blockchain/Dev) before any suite.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd (absolute paths, `-p`/`--prefix`), delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.** An EXIT trap that restores a file uses an ABSOLUTE path (R's slip this round).
- Write only in this folder and your k1/ scratch folder.

## Output
- Write 0_Brain/reference/2026-10-19_gate-K1-pr1586/verdict.md.
- Line 1: the verdict (GO / GO WITH NOTE / NO GO) naming the head.
- Line 2: the sha256/16 of the report (delete line 2, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
