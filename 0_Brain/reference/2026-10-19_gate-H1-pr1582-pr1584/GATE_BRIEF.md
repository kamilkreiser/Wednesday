# Gate brief: GATE H1 = PR #1582 (KS-1540) + PR #1584 (KS-1504), TIER 1 FULL, Opus, batched (file-disjoint)

Commissioned by the Wednesday seat, 2026-10-19 (AEDT, early morning), under model routing v1.0 (row G1: Spark edits on security-adjacent api-gateway surfaces get a tier-1 Opus gate). Seat R 48th raised both from held Spark passes. Live develop 385fc288fae831f2ca15b9d091c844f33285b784 (Wednesday ls-remote; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1582 KS-1540**, head c86b91c5a7c2da906bce6f8db2d1226089863bb4: `Blockchain/Dev/services/api-gateway/src/services/health.ts` +10 (GET /api/connector/info answers 503 SERVICE_UNAVAILABLE when `redisService.isRedisAvailable?.() === false`, the create path's text) + a new suite.
- **#1584 KS-1504**, head e8b4206f09d237fdb177c08a6b0c2b16e631acc2: `Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts` +1/-1 (the no-allowance warning's authMethod through the file's `logField`, at the call site) + a new suite.
- **Author's claims (NOT evidence):** red-first 3/2 -> 5/5 and 3/3 -> 6/6; api-gateway 1180 and 1181; tsc 0; leg 16 0 new; 503 text byte-identical to routes/verification.ts:1277.

## Gate (tier 1 FULL)
1. Diff each PR by hunk at its head: nothing outside the named files.
2. #1582: **is the fail-closed read actually closed?** In the in-memory fallback (Redis down), drive GET /api/connector/info end to end with the REAL redis module (not a double): before the change it answers allowedDocumentTypes [] ("all permitted"), after it answers 503. Then: what else reads the allow-list in fallback mode with the same "null -> all permitted" shape (grep the readers of the connector settings key)? Name each; any left open is a finding. The author's named residual (optional chaining makes a missing method a silent no-op): say whether a cell pinning that the real module exports `isRedisAvailable` is needed, and its severity.
3. #1584: `logField`'s escaping covers CR, LF, U+2028/U+2029 and backslash: plant each in authMethod and read the emitted log line. Is there any OTHER field of that warning (principal, tenant, clientId) still written raw? Name each.
4. Red-first and green yourself at the live tip; one mutant per product hunk (drop the guard / restore the raw String()) plus a comment-only control; api-gateway in full before and after; tsc.
5. Merge prediction on live develop for each alone and both orders, with an overlap check and a planted conflicting control. R predicts that all four PRs (#1581-#1584) in any order land tree 47a455d77dec.
## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/h1/ — create it and use nothing else in that scratchpad (other folders there belong to other agents).** Clone there with git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand. Build packages/shared (`npm ci` then `npm run build -w packages/shared` in Blockchain/Dev) before any suite. Use the repo's own tsc by path (Blockchain/Dev/node_modules/.bin/tsc), never `npx tsc` from the root.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd, delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your scratch folder.

## Output
- Write 0_Brain/reference/2026-10-19_gate-H1-pr1582-pr1584/verdict.md.
- Lines 1-2: one verdict line per PR (GO / GO WITH NOTE / NO GO), each naming its head.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
