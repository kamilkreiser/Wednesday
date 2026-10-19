# Spark screen, part 17 (2026-10-20 ~02:50-03:20 AEDT): KS-1676 (the fifteen unpinned heal guards), four test_only briefs, FOUR PASS, all BYTE-IDENTICAL

model: claude-sonnet-5-5 -- Spark screen-17 brief-writing sub-agent -- P1-P4 no

By a Spark brief-writing sub-agent for Wednesday. Secuura only. Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write; no `hold_ready`. Nothing under `!CODING` was written (the Linear key was read inside a scratch script file and never printed; read-only query of KS-1676 plus its comments). Every clock below came from `date`.

## BLUF
- **KS-1676 is a pure coverage gap and test-only was enough: no product edit needed.** Four briefs, four new jest files (the product is only the tamper target), together covering **all 15 ticket rows**; each is lint rc 0 (empty stderr), dry-run rc 0 (no WARNING), CONTROL-PASS first, then ONE real round: **4 PASS, golden BYTE-IDENTICAL, `spliced 0`, `inlined 0`, plain `section_1.diff` in every `.opts`.**
- **The settled/failed pair is first (p1 v2, p2 v1)**: four cells each (failed, anchor_failed, confirmed, anchored:true); the checker's tamper reds all four, and each single-clause mutant reds exactly its own cell.
- **A fact the ticket did not have:** v2's heal guards are unreachable from a single-row cell. `matchesForHash` (`verificationV2.ts:392-400`) repeats the stored-simulated, stored-shape, settled and failed tests as a prefilter and fetches the chain fact only when SOME row passes it, so with a failed row alone `healBlobWithChainFact` gets `chain = null` and returns on `!chain`. Measured: the p1 cells WITHOUT a stale-pending companion row stayed GREEN under the checker's tamper (4 of 5 passed, C1 red). So every v2 cell lists a companion row beside the target. This is the same trap the ticket describes (a survived mutant read as no test), one level up.
- **NOT covered, by the ticket's own account:** v2's null-chain guard `!chain` (:130; no single-line mutant compiles under TS18047). No brief pins it.
- The Spark's limit is still not found: longest prompt 33.8k tokens (p2/p4, the v1 file is big), 69 s model.

## Pinned sha
`git ls-remote origin refs/heads/develop` at the start (02:51): `17ab917aa6f4646d92ce2d1ee9743362ad5bc548` (as the task said; fetched into the literal cache path, `cat-file -t` commit). The briefs' `Tip:` lines say it. Develop then moved twice during the rounds: `c129c63cf777` (KS-1634, touches only `originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts`; p3 and p4 ran here) and `f7d35d628cdc` (KS-1673, m365-integration + openapi; p2's rerun ran here). `git diff --name-only 17ab917aa6f4 f7d35d628cdc` = the m365 files, `secuura-api.yaml` and the ks1634 test: **no briefed product file, no new test path touched**. Re-read at the end: `f7d35d628cdc`. Not re-pinned.

## Lanes
Untouched: `services/m365-integration/**` and `ks1634-v2-chain-only-match-carries-simulated.test.ts` (both only seen in the develop diff above, not edited, not read for content). Open-PR overlap on `verification.ts` / `verificationV2.ts` was NOT checked on GitHub (no identity); both files are busy.

## Ticket (read-only, Linear API)
KS-1676, Medium (Wednesday's ruling: a coverage gap with no live defect), Backlog. 15 rows: v1 A1 A2 A3 A3b A4 A4b V4 V5 (verification.ts), v2 W4 B1 B2 B2b B3 B3b B5 (verificationV2.ts). Line numbers in the ticket (develop `09336b24`) still match at `17ab917a` (the KS-1661 comment lines were already in): v1 :432 :434 :435-437 :455, v2 :130 :132-135 :137.

## Briefs (dirs under `local-model/night/briefs/`; each `KS-1676.md`, `golden.diff`, `spark.pins`; tier test_only, rung 1, ONE edit point = ONE new file, path pinned by the `File:` line under `## The test`)
| dir | new test file (`originate/src/__tests__/`) | ticket rows | tamper (product line, text) | red under tamper | cells |
|---|---|---|---|---|---|
| ks_1676_p1 | `ks1676-v2-settled-and-failed-rows-never-heal.test.ts` (161 lines) | B2 B2b B3 B3b (+ the `status==='confirmed'` clause) | `verificationV2.ts:135` `  if (settled \|\| failed) return blob;` -> `  if ((settled && false) \|\| (failed && false)) return blob;` | S1 S2 S3 S4 (4 failed / 5) | S1-S4 RED, C1 CONTROL |
| ks_1676_p2 | `ks1676-v1-settled-and-failed-rows-never-heal.test.ts` (136) | A3 A3b A4 A4b (+ confirmed clause) | `verification.ts:437` same line, same replacement | S1 S2 S3 S4 (4 / 5) | S1-S4, C1 |
| ks_1676_p3 | `ks1676-v2-simulated-and-malformed-anchors-never-heal.test.ts` (155) | W4 B1 B5 | `verificationV2.ts:130` `  if (!blob \|\| blob.simulated === true \|\| !chain \|\| chain.simulated) return blob;` -> `  if (!blob \|\| !chain \|\| chain.simulated) return blob;` | G1 (1 / 4) | G1-G3, C1 |
| ks_1676_p4 | `ks1676-v1-simulated-and-malformed-anchors-never-heal.test.ts` (143) | A1 A2 V5 V4 | `verification.ts:455` `    if (chain?.verified !== true \|\| chain.simulated \|\| !chainTx \|\| !REAL_TXHASH_RE.test(chainTx)) return blob;` -> `    if (chain.simulated \|\| !chainTx \|\| !REAL_TXHASH_RE.test(chainTx)) return blob;` | G3 (1 / 5) | G1-G4, C1 |

The checker plants ONE tamper per brief; the cells that red only under another clause's mutant (p3 G2 G3; p4 G1 G2 G4) are green under the checker's tamper and are proved by the hand-run mutants below (stated in each brief's UNMEASURED).

## Mutants, run by hand BEFORE the briefs were written (scratch clone, jest, one clause at a time; no `TS####` in any failure text, tested by script; restored and re-run green)
All at `17ab917aa6f4`. Every row below = exactly the named cells red, the rest green.
- **p1 (v2 settled/failed)**: `:135` failed->`(failed && false)` S1 S2; `:135` settled->`(settled && false)` S3 S4; whole line S1-S4; B2b `:134` drop `anchor_failed` clause S2; B3b `:133` drop `anchored === true` S4; extra `:133` drop `status === 'confirmed'` S3.
- **p2 (v1 settled/failed)**: the same six at `:437`, `:436`, `:435` with the same cell sets.
- **p3 (v2)**: W4 `:130` drop `blob.simulated === true ||` G1; B1 `:132` drop `|| !REAL_TXHASH_RE.test(tx)` G2; B5 `:137` drop `|| !REAL_TXHASH_RE.test(chainTx)` G3.
- **p4 (v1)**: V5 `:455` drop `chain?.verified !== true ||` G3; A1 `:432` drop `|| blob.simulated === true` G1; A2 `:434` drop `|| !REAL_TXHASH_RE.test(tx)` G2; V4 `:455` drop `|| !REAL_TXHASH_RE.test(chainTx)` G4.
- Compile-safety: every mutant keeps its variable used (`(x && false)`) or drops an operand over names that stay used; a TS diagnostic scan of each output found none. The mutant of p1 without a companion row, written carelessly by me, tripped TS6133 on the then-unused `companion` helper: the ticket's own trap, caught by the same scan, fixed with `void companion`.
- Also by hand: `ks1293-originate-suite-is-hermetic` 10/10 with the four new files present (they do not name the anchoring base URL, so no manifest line is owed); each file GREEN at the tip.

## Design choices (Wednesday's rule): choice / rejected alternative / what reds
| brief | choice | alternative | result |
|---|---|---|---|
| p1, p3 | v2 target row plus a stale-pending COMPANION in one request | single-row cell | single-row cells stay GREEN under the p1 tamper and C1 reds (measured, 4 passed / 1 failed): the prefilter skips the fetch, so the companion is kept |
| p3 | chain reply attributes to the target by `metadata.documentId` (sameDoc) | attribute by `sameTx` | a malformed stored tx (G2) can never equal a real chain tx, so under sameTx the B1 mutant would stay green; sameDoc survives each dropped shape guard |
| p1, p2 | assert status plus stored `blockHeight`/`network` (S3 S4), and in v1 the fetch count 0 | assert presented status only | status alone would not red S3 (a re-heal of a confirmed row keeps `confirmed`); block height/network do |
| p4 | each RED cell differs from C1 in exactly ONE field | a two-field cell | stays red after dropping either guard, so it would not pin which guard |

## Rounds (verbatim verdict lines; run dirs under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/`)
| brief | control | real round |
|---|---|---|
| p1 | `SPARK ROUND ks_1676_p1: CONTROL-PASS ... golden BYTE-IDENTICAL · tip 17ab917aa6f4 · 81s` (`spark_secuura_2026-10-20_ks_1676_p1-control`) | `SPARK ROUND ks_1676_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 17ab917aa6f4 · 138s round, 59.172s model, 19445+2373 tok` (`..._ks_1676_p1`) |
| p2 | `CONTROL-PASS ... BYTE-IDENTICAL · tip 17ab917aa6f4 · 72s` (`..._p2-control`); re-run at the new tip `CONTROL-PASS ... tip f7d35d628cdc · 66s` (`..._p2-control-r2`) | first attempt REFUSED before any model call (below); `SPARK ROUND ks_1676_p2: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip f7d35d628cdc · 139s round, 69.442s model, 33831+2018 tok` (`..._ks_1676_p2-r2`) |
| p3 | `CONTROL-PASS ... BYTE-IDENTICAL · tip 17ab917aa6f4 · 82s` (`..._p3-control`) | `SPARK ROUND ks_1676_p3: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip c129c63cf777 · 133s round, 57.809s model, 19187+2310 tok` (`..._ks_1676_p3`) |
| p4 | `CONTROL-PASS ... BYTE-IDENTICAL · tip 17ab917aa6f4 · 84s` (`..._p4-control`) | `SPARK ROUND ks_1676_p4: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip c129c63cf777 · 136s round, 67.865s model, 33803+2078 tok` (`..._ks_1676_p4`) |

Checker lines (`checker.out`): p1 `A4 (4 failed / 5 run; controls green; assertion reds)`, `A5 (5/5)`, `baseline total=1523 | after 1528`, A6 no new red, A7 tsc rc 0; p2 `A4 (4 failed / 5)`, `baseline 1526 | after 1531`; p3 `A4 (1 failed / 4)`, `A5 (4/4)`, `baseline 1526 | after 1530`; p4 `A4 (1 failed / 5)`, `A5 (5/5)`, `baseline 1526 | after 1531`. All A3 = the one new file, product untouched.

**Accommodation check:** `decl_splice*.out` = `spliced 0`, `tdz_inline*.out` = `inlined 0`, `section_1.opts` names the plain `section_1.diff`, `cmp section_1.diff section_1.decl.diff` and `...tdz.diff` equal, in all four rounds. **Golden comparison:** all four `BYTE-IDENTICAL` (cmp), so the model reproduced the golden test file exactly (the golden carries the `new file mode` and `index` lines; the model kept them).

**The REFUSED p2 attempt (not a model round):** at 03:1x develop had moved to `c129c63cf777` between p1 and p2, and `build_input` REFUSED (rc 2: "develop tip ... is not in the local object store; a fetch is a write verb on the source checkout, so a Secuura seat must fetch first"). I had fetched only before p1. No model was called (the run dir `..._ks_1676_p2` holds `build_input.out` only). I fetched, confirmed the changed files were not mine, re-ran p2's control at `f7d35d628cdc` (CONTROL-PASS) and then the one real round (PASS). Counter: one real model round per brief, no rebrief, no FAIL. Classified HARNESS/process (a moving develop needs a fetch before EVERY round).

## Things Wednesday should read before holding
1. **Four PRs or one?** The four new files are independent of each other and of every product file. They could ship as ONE PR (four files, all `ks1676-*`) or four; none edits an existing file. Together they close KS-1676 except the undecided `!chain` guard; each brief says "Refs, does not close alone".
2. The tamper pins one clause per brief; the rest rest on my hand-run mutants (in each brief's table). If Wednesday wants a machine-proof of every clause, the cost is more briefs (one tamper each); that is a ruling, not a gap I hid.
3. The v2 cells depend on `matchesForHash`'s prefilter (:392-400) staying as it is. If a refactor removed the prefilter the companion would become redundant but harmless; if it changed what makes a row "healable" the C1 control reds first.
4. p3's G2/G3 and p4's G1/G2/G4 carry `RED` in their title but are not in `## Red cells` (they red only under their own mutant); the checker reads them as plain green cells. Said in each brief.
5. Open-PR overlap on `verification.ts` / `verificationV2.ts` NOT checked.

## IMPROVEMENTS rows added (3) and queue line (1)
`local-model/IMPROVEMENTS.md` (v2 prefilter, fetch-before-every-round, TS6133 caught in my own scratch) and one `#` line in `spark/queue.md`.

## NOT run / NOT done
- No hold, no raise, no `hold_ready`, no GitHub or Linear write, no Postgres, no integration suites (they need a database), no platform suites, no `!CODING` write. The `!chain` guard (:130) is unpinned. v2's `fetchChainFact` `verified === true` filter (:111) and the `!chain` / `chain.simulated` operands were not pinned here (only the ticket's rows). Whole-workspace run beyond each checker's A6/A7 for originate: not run.
- Housekeeping: `spark/cache/work/` gained ~9 per-round clones (not pruned); `spark/state/dry/` four dry-run inputs; the cache clone fetched develop up to `f7d35d628cdc`.

## Files written
Briefs: `local-model/night/briefs/ks_1676_p1/`, `ks_1676_p2/`, `ks_1676_p3/`, `ks_1676_p4/`. Scratch (not durable): `/private/tmp/wed_screen17/` (get.py, clone/, h.sh, mut.py, mk.py, muts_p*.sh, drafts/, mutant outputs `mut_*.out`, lint/dry/ctl/real outputs).
