# Gate brief: GATE M1 = KS-1628 (retire the public POST /api/documents/:id/verify), three PRs, TIER 1, batched, Fable 5.1 (TRIAL)

Commissioned by the Wednesday seat, 2026-10-19 ~08:0x AEDT. Model routing v1.0 row G1 (tier 1: a public route removed,
an honesty check hardened, a security-adjacent gate retired). **This is also the Fable 5.1 trial gate owed under Kam's
approval of routing v1.0 (decision 7, 2026-10-18), measured against the day's Opus gates: report your wall-clock and
anything you could not do.** Kam ruled card `secuura-ks1628-retire-deprecated-verify-route-1019` = c "Retire it now".
Seat R 49th built all three. Live develop 83ed01af70fd5ed6cca9ac66f28ddcb8a1034105 (Wednesday `git ls-remote` ~08:0x; re-read).
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

| merge order | PR | head | what |
|---|---|---|---|
| 1 | #1588 precursor | 0080ac3e155282551d5ebc21fcbc9895a1eaec27 | originate `routes/verification.ts` isAnchoredHonestly refuses six shapes the gateway refused: truthy `simulated` (Boolean rule), failed status even with `anchored: true`, non-64-hex txHash, a REPORTED height not a positive-integer number or digit string (an unreported height is not judged); plus R's own extension to `presentBlockchainHonestly` (flagged) |
| 2 | #1587 PR 1 | b5b78b296c86d4ca8112b2f5bfb48c46165a1dbf | removes originate's in-cluster copy (`routes/documents.ts` ~:1513-1608) + 2 new suites |
| 3 | #1589 PR 2 | 53cb4ec76ea7b5716089af5c4a9c5f6166a55de2 | removes the gateway handler + 3 helpers only it used + the spec entry (yaml regen: one path); 14 suites quarantined in `5_Project_History/quarantine/2026-10-19-seatR49-ks1628-pr2/` with a README mapping each property to its new home; 5 mixed suites edited; leg 16 baseline 35 -> 27 |

**Author's claims (NOT evidence):** R's READY mail figures: originate 1434 (#1588) / 1413 (#1587) / 1405 (#1589); api-gateway 1100/1100 after #1589 (= 1195 - 84 quarantined - 11 removed cells); census of stored rows on kintsugi and demo under #1588's rule: 0 change answer; 0 edge callers of the route in ~30 d (kintsugi) / ~38 d (demo). **Narrowing ruled by Wednesday:** the per-type `verifierVerificationLevel` gate ends enforced nowhere (KS-1632); e2e callers left failing, not run (KS-1631).

## Gate
1. Diff each PR at its head by hunk; nothing outside its named files; the three pairwise file-disjoint.
2. **#1588:** red-first and green yourself; then the census question in code: for EACH of the six shapes plus the non-hex hash, a cell that reds on develop and greens on the PR. Confirm a missing/null height and a missing `simulated` are NOT refused (the 132 confirmed rows have no `simulated` key). Judge R's `presentBlockchainHonestly` extension: does it change any answer for a well-formed blob? Say whether it belongs in this PR.
3. **The quarantine map is the heart of this gate.** For EACH of the 14 quarantined suites and the 11 removed cells, take the property the README says it pinned and find the cell that pins it now (file:line), or confirm the README says "ended" and why. **Plant a regression for each re-homed property** (break it in the successor's code) and confirm a surviving cell reds. A property the README claims is re-homed but no surviving cell reds on = a finding. The two R names as ended (the tier-2 selector, the stale-confidence guard): confirm they existed only for the removed handler.
4. **#1589 removal is complete and nothing else depended on it:** grep the whole repo (connectors, frontends, packages, scripts, docs, systemTest, by literal path AND by concatenated forms; R's ks1199 is the positive control) for any remaining caller of the removed route or the 3 removed helpers. The `/api` index, the spec yaml, `generate-openapi --check`, `check:spec-examples`. After all three: the old path answers 401 unauthenticated and 404 authenticated (say which layer answers), and `POST /api/verification/verify` is unchanged for a well-formed request.
5. One mutant per product hunk; owning suites before/after on a tree with `packages/shared` rebuilt in YOUR clone; leg 16's new baseline: confirm every dropped entry is in a quarantined or edited file.
6. Merge prediction on live develop in the order 1588 -> 1587 -> 1589 (tree ids), and #1587 against #1568 (J, same file `documents.ts`, disjoint ranges; #1568 head 09588895db75354d829df2069452c82b787d8bc8 is at its own gate) in both orders.

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/m1/ — create it and use nothing else in that scratchpad (l1/ belongs to another gate running now).** Clone there with `git clone --shared` from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git in YOUR clone, fetch with that checkout's `core.sshCommand` (read it with `git config --get`). Build `packages/shared` before any suite.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker, no access to the kintsugi or demo servers.
- Never cd, delete nothing outside m1/, every loop in a script FILE run with `/bin/bash`. An EXIT trap that restores a file uses an ABSOLUTE path.

## Output
- Write 0_Brain/reference/2026-10-19_gate-M1-pr1588-1587-1589/verdict.md.
- Lines 1-3: one verdict per PR (GO / GO WITH NOTE / NO GO), each naming its head.
- Line 4: `sha256/16: <16 hex>` of the report with line 4 deleted.
- Then FOUND / TESTED / HOW, the quarantine-map table (property, old cell, new home file:line, planted-regression result), NOT tested, severities with file:line. Final lines: `MODEL: <your model id>` and `WALL-CLOCK: <minutes>`. Round 1 of 2.
