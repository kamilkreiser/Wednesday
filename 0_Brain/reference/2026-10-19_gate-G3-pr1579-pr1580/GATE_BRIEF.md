# Gate brief: GATE G3 = PR #1579 (KS-1623 N3) + PR #1580 (KS-1624 F1 ruled (a)), TIER 2 through-code, batched (file-disjoint), Sonnet

Commissioned by the Wednesday seat, 2026-10-19 ~02:3x AEDT, under model routing v1.0 (row G2: tier-2 gates run on Sonnet; #1579 is a comment + a test, #1580 a connector banner/export). If you find anything security-shaped, say so on line 1 and Wednesday hands the PR to a tier-1 Opus gate. Seat R 48th raised both from held Spark passes. Live develop 6184eaa0af75c1e27eb69bbff67a7790ef494b5f (Wednesday ls-remote 02:3x; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1579 KS-1623 N3**, head 76de780c20421cf963d53273571776c1e2e8a97a, 2 files +45/-1: `Blockchain/Dev/services/originate/src/routes/verification.ts:1445` summary comment gains deleted + expired; NEW `services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts` (5 source-text cells, 3 CONTROL).
- **#1580 KS-1624 F1 (a)**, head fcc1451c7bfed310d2d38e63386c9b687c1ad2a4, 3 files +41/-5: `Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts` exports `SECUURA_API_URL` (the slash-stripped base), `.../src/index.ts` imports it for the "API target:" banner, `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` moves with it.
- **Author's claims (NOT evidence):** #1579 red-first 3/2 -> 5/5, originate 1393/1393, tsc 0; shell runner not re-run by subtree-id measurement. #1580 ks812 8/3 -> 11/0; connector tsc rc 0 (TypeScript 5.9.3, via Blockchain/Dev/node_modules/.bin/tsc); full shell runner 91/0; p1->p2 order measured; Node v24.7.0.

## Gate
1. Diff each PR by hunk at its head: nothing outside the named files.
2. Red-first and green yourself for each named test at the live tip.
3. #1579: the suite's cells compare the comment with the SQL predicate. Confirm the cells would red if the comment drops one status AND if the SQL gains a status the comment lacks (plant each, restore). Name the coupling the author flagged (a CONTROL matches `lower(btrim(d.status)) NOT IN (` literally) and whether a legitimate future widening of btrim would fail it loudly or silently.
4. #1580: importing `./verify` from `index.ts` must not change startup behaviour: read `verify.ts` top-level for side effects at import (env reads, network, timers) and say what runs at import time now that did not before. The banner must print the stripped value: inputs unset, `https://x.test`, `https://x.test/`, `https://x.test//base///`. Connector tsc with `Blockchain/Dev/node_modules/.bin/tsc -p Blockchain/Dev/connectors/whatsapp-bot/tsconfig.json` (assert the version; never `npx tsc` from the root: it resolves a squatted package).
5. One mutant per product hunk plus a comment-only control per PR; owning suites before/after.
6. Merge prediction on live develop for each PR alone and both orders (R predicts tree 526bc67b37d3), an overlap check and a planted conflicting control.

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/g3/ — create it and use nothing else in that scratchpad (other folders there belong to other agents).** Clone there with git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand. Build `packages/shared` (`npm ci` then `npm run build -w packages/shared` in Blockchain/Dev) before any suite.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd (absolute paths, `-p`/`--prefix`), delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your g3/ scratch folder.

## Output
- Write 0_Brain/reference/2026-10-19_gate-G3-pr1579-pr1580/verdict.md.
- Lines 1-2: one verdict line per PR (GO / GO WITH NOTE / NO GO), each naming its head.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
