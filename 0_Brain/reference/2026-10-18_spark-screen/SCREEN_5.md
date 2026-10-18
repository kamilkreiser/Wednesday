# Spark screen, part 5 (2026-10-19 ~04:1x-04:4x AEDT): KS-1626, three briefs, three rounds, three PASS

By a Spark brief-writing sub-agent for Wednesday. Secuura only. Briefs written against develop `4a547a11997e0e80bbeced0db57c2acb4c345368` (the round script's own cache fetch ran first; `cat-file -t` = commit; `ls-remote` agreed at the start). Develop then moved to `5d1be7b06279950e3bfe176c237e5d640eb04581` (two commits: KS-1504 rateLimitEnforce, KS-1540 health.ts); round.sh's stale check passed (none of my files touched) and the controls and rounds ran at `5d1be7b06279`. Nothing held, raised, pushed, merged, committed or deleted. The ticket text of KS-1626 was NOT read (no Linear reader); the briefs rest on Wednesday's commission text.

## Sites (all five re-read at 4a547a11997e; line numbers match R's)

anchoring `honestAnchor.ts:17` (`export const FABRICATED_TX_PREFIX`), `anchorReadback.ts:115` (inline in `buildVerifyResponse`); originate `services/anchorHonesty.ts:28` (`FABRICATED_TX_PREFIX`), `routes/verification.ts:52` (`FABRICATED_TXHASH_RE`); api-gateway `routes/verification.ts:655` (live chain-scan reply) and `:692` (persisted blob). The writer: `anchoring/src/index.ts:1986` (`mock_batch_tx_${randomBytes(32).toString('hex')}`, mock branch, confirmed status). A repo-wide grep of `mock_tx_|tx_sim_` in non-test, non-comment source at the tip found exactly these five regex sites (plus the already fixed `originate/.../anchorStateSync.ts:81`); other placeholder-test shapes (a `startsWith('tx_')` elsewhere) were not searched.

Fix chosen at every site: `/^(tx_sim_|mock_tx_|tx_)/` becomes `/^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/`. The new alternative shares no leading text with the others (`mock_b` vs `mock_t`), so order is immaterial; `mock_batch_tx_` is inserted after `mock_tx_` and `tx_` stays last (so the regex form does not need it before them).

## Result

| service | brief dir (`local-model/night/briefs/`) | mode / rung | edit points | control | round verdict | golden | model s / tokens | run dir (`local-model/runs/`) | FAIL class |
|---|---|---|---|---|---|---|---|---|---|
| anchoring | `ks_1626_anchoring` | code_patch2, rung 2 | 3 (2 product lines, 1 NEW vitest file) | CONTROL-PASS 7/7 BYTE-IDENTICAL (`..._ks_1626_anchoring-control`) | PASS | TREE-IDENTICAL (the model left out the three `index` lines; hunks and `+` lines identical) | 45.4 / 13337+1754 | `spark_secuura_2026-10-19_ks_1626_anchoring` | none |
| originate | `ks_1626_originate` | code_patch2, rung 2 | 3 (2 product lines, 1 NEW jest file) | CONTROL-PASS 7/7 BYTE-IDENTICAL (`..._ks_1626_originate-control`) | PASS | BYTE-IDENTICAL | 74.2 / 35604+2175 | `spark_secuura_2026-10-19_ks_1626_originate` | none |
| api-gateway | `ks_1626_apigw` | code_patch, rung 2 | 3 (2 hunks of one product file, 1 NEW vitest file) | CONTROL-PASS 7/7 BYTE-IDENTICAL (`..._ks_1626_apigw-control`) | PASS | BYTE-IDENTICAL | 88.7 / 36011+3174 | `spark_secuura_2026-10-19_ks_1626_apigw` | none |

brief_lint rc 0 and dry-run rc 0 for all three before any control or round. No rebrief used (counter: original only, for each).

## Checker lines (all three rounds)
- anchoring: `RESULT: PASS (7/7)`; A4 "fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)"; A5 "5 passed / 5 run"; A6 whole anchoring suite no new red; A7 tsc rc 0; `PASS A2a ... hunks=2 ok=2 bad=0 skipped_newfile=1`; `SPARK RESULT: PASS`.
- originate: same shape: A3b 1 site (first product), A4 2 failed / 5 run, A5 5 passed / 5, A6, A7 rc 0, A2a hunks=2 ok=2.
- api-gateway: A3b 2 sites, A4 "fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)", A5 5 passed / 5, A6 whole api-gateway suite no new red, A7 rc 0, A2a hunks=2 ok=2.

## Red cells and controls (exact titles, in each brief's `## Red cells`)
- anchoring: RED `RED KS-1626 A1 honestTxView reads a mock_batch_tx_ hash as a placeholder`, `RED KS-1626 A2 buildVerifyResponse reads a mock_batch_tx_ hash as a placeholder`; CONTROL A3 (real 64-hex read as real by both; the cardanoscan URL is built), A4 (the three older prefixes still placeholders), A5 (prefix test only: `abc_mock_batch_tx_def` is not one).
- originate: RED `... O1 anchorHonesty reads a mock_batch_tx_ hash as a placeholder` (FABRICATED_TX_PREFIX, isSimulatedAnchor, simulatedFieldsFromAnchor, composeHonestBlockchainBlob), `... O2 presentBlockchainHonestly reads a mock_batch_tx_ txHash as a placeholder`; CONTROL O3 (real hash unchanged, same reference returned), O4, O5. Test mocks are the neighbouring ks563 file's.
- api-gateway: RED `... G1 a mock_batch_tx_ hash from the live chain-scan reply is not a hash` (site :655), `... G2 a mock_batch_tx_ persisted hash with a height and confirmed must not report on-chain` (site :692); CONTROL GC1 (real hash live still on-chain), GC2 (real hash persisted still on-chain), GC3 (tx_sim_ still off-chain-only on both). The harness is the KS-1069 file's, sliced at generation time (non-ASCII comment characters replaced by ASCII).
- Each hash is `mock_batch_tx_` + 64 hex-shaped characters (`'c'.repeat(64)`), the writer's shape; the real-hash control is 64 hex.

## Decisions and things Wednesday should read
- The adjacent comments that list the three prefixes were NOT edited, in any service: most carry non-ASCII (`...` and em dash) on lines the harness mishandles when changed, and the per-brief edit-point budget (3) was already spent. The comment sites are: `honestAnchor.ts:5`, `anchorReadback.ts:110-114`, `anchorHonesty.ts:6`, `routes/verification.ts:42` (originate), `routes/verification.ts:679` (api-gateway; this one is ASCII). A comment-only follow-up is open.
- The Where lists are written for the first product file (the builder reads `:NNN` bullets against it); the second product's sites are bullets in prose with their own line numbers, still bold for must-change. A3b counted 1 site for the two-product briefs, so the second product's edit is graded by A3 (declared set), A3x (byte identity) and the RED cell that reads it (A4/A5), not by A3b.
- Blank neighbours: `honestAnchor.ts:17`, `anchorHonesty.ts:28` and `originate routes/verification.ts:52` sit beside blank lines; those are written as `-`/`+` blank pairs (the KS-1387 form). Worked.
- api-gateway `routes/verification.ts` only; `services/health.ts` (#1582) and `middleware/rateLimitEnforce.ts` (#1584) untouched. Open-PR overlap on the other four files: NOT checked.
- Ordering: the three diffs are independent (different services) and apply in any order.

## NOT tested / unmeasured
- I did not read the three model patches beyond the checker (two byte-identical to my golden, one tree-identical). Wednesday reads at source.
- No jest/vitest/tsc by hand; every red/green figure is the checker's.
- The ticket text itself, open-PR overlap, live seats' unpushed work, whether any demo/production row holds `mock_batch_tx_`, other placeholder-test shapes outside these five sites.
- Audit surface: honest-labelling of anchors on verify paths (a hash that is not on chain stops being presented as on-chain). Not an auth or credential surface; the api-gateway change moves a verify answer toward `off-chain-only` for placeholder hashes only. Route to a normal gate.

## Files written
Briefs: `local-model/night/briefs/ks_1626_anchoring/`, `ks_1626_originate/`, `ks_1626_apigw/` (each `KS-1626.md`, `golden.diff`, `spark.pins`). `local-model/spark/queue.md` (one provenance comment line). Run dirs and `spark/state/dry/` are round.sh's own; `spark/cache/work/` accumulated 3 control + 3 round clones (about 335 MB each, not pruned). Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/spark_1626/` (`gen.py` generator, `prove.sh`, `rounds.sh`, logs, scratch apply-check trees).
