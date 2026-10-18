# Gate brief: GATE I1 = PR #1585 (KS-1626), TIER 1 FULL, Opus

Commissioned by the Wednesday seat, 2026-10-19 (AEDT, before dawn), under model routing v1.0 (row G1: honest-labelling of anchors on the public verify readback across three services). Seat R 48th raised it from three held Spark passes plus seven hand-edited comments. Live develop 5d1be7b06279950e3bfe176c237e5d640eb04581 (Wednesday ls-remote; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1585 KS-1626**, head 664d3fd2494b15cde3c34175c0c979dbee0edc9a, 11 files: five regex sites become `/^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/` (anchoring honestAnchor.ts:17 + anchorReadback.ts:115; originate services/anchorHonesty.ts:28 + routes/verification.ts:52; api-gateway routes/verification.ts:655 + :692), seven prefix-listing comments edited by hand (named in the PR), one deliberately left (api-gateway routes/verification.ts:679, a measurement record), and three new test files.
- **Author's claims (NOT evidence):** red-first 3/2 -> 5/5 per service; anchoring 375/376 (the one red, threadTokenMint, is pre-existing KS-562, an install split of @lucid-evolution), originate 1405, api-gateway 1191; tsc 0; each product file differs from the tip only on its regex line.

## Gate (tier 1 FULL)
1. Diff by hunk at the head: nothing outside the 11 named files; every product hunk changes only the regex line (blank-line churn is net zero); every comment edit is a comment.
2. **Census, the core question:** grep all of Blockchain/Dev (every service, packages/, scripts/) at the head for EVERY reader that decides whether a txHash is a placeholder: the prefix regexes, `startsWith('tx_'` / `'mock_'` style checks, `simulated` derivations. Does any reader still treat `mock_batch_tx_<hex>` as a real on-chain hash? Name each with file:line; one left open is a finding.
3. **Writers:** confirm `mock_batch_tx_` has exactly one writer (anchoring/src/index.ts ~1986) and whether any OTHER placeholder prefix is written anywhere that the new regex still misses.
4. **Behaviour:** with a `mock_batch_tx_<64hex>` anchor marked confirmed (the mock-mode batch shape), drive the readback / verify paths the five sites serve and show the answer is labelled simulated or not-on-chain after the change and real before. A real 64-hex hash stays real.
5. Red-first and green yourself; one mutant per site (drop the new alternative) killed by a named cell; a comment-only control; each owning suite before/after; tsc per service.
6. Merge prediction on live develop with an overlap check and a planted conflicting control.

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/i1/ — create it and use nothing else in that scratchpad (other folders there belong to other agents).** Clone there with git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand. Build packages/shared (`npm ci` then `npm run build -w packages/shared` in Blockchain/Dev) before any suite. Use the repo's tsc by path (Blockchain/Dev/node_modules/.bin/tsc), never `npx tsc` from the root. The anchoring threadTokenMint cell may fail on a root-workspace install (KS-562): report it, do not chase it.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd, delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.** Beware zsh unmatched globs: use bash scripts with nullglob.
- Write only in this folder and your i1/ scratch folder.

## Output
- Write 0_Brain/reference/2026-10-19_gate-I1-pr1585/verdict.md.
- Line 1: the verdict (GO / GO WITH NOTE / NO GO) naming the head. Line 2: a one-line headline.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
