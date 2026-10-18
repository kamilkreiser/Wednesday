# Gate brief: GATE H2 = PR #1583 (KS-1485 item 2) + PR #1581 (KS-1387), TIER 2 through-code, Sonnet, batched (file-disjoint)

Commissioned by the Wednesday seat, 2026-10-19 (AEDT, early morning), under model routing v1.0 (row G2). If anything is security-shaped, say so on line 1 and Wednesday hands the PR to a tier-1 Opus gate. Seat R 48th raised both from held Spark passes. Live develop 385fc288fae831f2ca15b9d091c844f33285b784 (Wednesday ls-remote; re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1583 KS-1485 item 2**, head 16fc1d201fc03484921911cc9ca42c474ffba7d5: `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` +2/-2 (`authoritativeTxHash` also rejects `mock_batch_tx_`, and its doc comment names it) + a new suite.
- **#1581 KS-1387**, head 6b4bcaec11fa4aea156a11bbaa23b56b09126b63: `Blockchain/Dev/services/governance/src/routes/governance.ts` +1/-1 (`const router: Router = Router();`) + a new suite. The ticket's symptom (a clean image build fails with TS2742) is NOT reproduced by the author (Docker down; the local install hoists the type so the local build passes at the tip too).
- **Author's claims (NOT evidence):** red-first 4/3 -> 7/7 and 2/1 -> 3/3; originate 1400, governance 119; tsc 0.

## Gate
1. Diff each PR by hunk at its head: nothing outside the named files.
2. #1583: list every placeholder prefix any writer can produce (grep the writers of txHash / transactionHash for `tx_`, `mock_`, `mock_batch_`, any other) and say whether `authoritativeTxHash` now rejects every one; a writer prefix still accepted is a finding.
3. #1581: try to REPRODUCE TS2742 without Docker: a fresh install in your clone with the layout the ticket names (a nested copy of `@types/express-serve-static-core` under `packages/shared/node_modules`, if the ticket or the Dockerfile's install order gives one), then governance's own build at the tip (expect TS2742) and at the head (expect clean). If you cannot construct it, say exactly why, and the PR is gated on the type change alone.
4. Red-first and green yourself at the live tip; one mutant per product hunk plus a comment-only control; each owning suite before and after; tsc.
5. Merge prediction on live develop for each alone and both orders, with an overlap check and a planted conflicting control. R predicts that all four PRs (#1581-#1584) in any order land tree 47a455d77dec.
## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/h2/ — create it and use nothing else in that scratchpad (other folders there belong to other agents).** Clone there with git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand. Build packages/shared (`npm ci` then `npm run build -w packages/shared` in Blockchain/Dev) before any suite. Use the repo's own tsc by path (Blockchain/Dev/node_modules/.bin/tsc), never `npx tsc` from the root.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd, delete nothing. **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your scratch folder.

## Output
- Write 0_Brain/reference/2026-10-19_gate-H2-pr1583-pr1581/verdict.md.
- Lines 1-2: one verdict line per PR (GO / GO WITH NOTE / NO GO), each naming its head.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line. Final line: `WALL-CLOCK: <minutes>`. Round 1 of 2.
