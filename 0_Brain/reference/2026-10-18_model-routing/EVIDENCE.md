# Model routing v1.0 -- evidence appendix (Wednesday-only; names Secuura tickets)

Moved out of fleet/specs/model-routing.md on approval, 2026-10-18 20:5x.

## 9. Evidence appendix (Wednesday-only; names Secuura tickets; strip before sharing)

**Method, Spark ladder (`2_Project_Files/local-model/SPARK_LADDER.md`, 2026-09-25..10-02).** Parsed every numbered table row: 58 rows, of which 4 were refused before the model ran. Rung taken from the Rung column, verdict from the Verdict column. Smoke rows S0-S3 excluded.

Table A, the ladder by rung (model rounds):

| Rung | PASS | FAIL | Notes |
|---|---|---|---|
| 1 | 13 | 0 | incl. row 4 (doc_patch, PASS, not held: KS-789 was already at the counter) |
| 2 | 19 | 0 | |
| 3 | 16 | 0 | rows 28 and 38 PASS on re-check after harness faults |
| 4 | 3 | 3 | KS-1226 r1+r2 FAIL, sent to Opus 5.5; KS-1347 r1 FAIL, r2 PASS; KS-1337 and KS-1339 PASS r1 |

**Method, Spark queue era (`2_Project_Files/local-model/spark/done.md`, 2026-10-05..10-16).** Counted rows starting `| 2026`: **73 rows**, verdicts **64 PASS / 8 FAIL / 1 REFUSED**. Items = tag, with the `-r2` suffix folded (KS-1438, KS-865): **63 items**. **56 PASS on their first run. 61 PASS inside done.md.** KS-1278 later PASSed on code_patch2 r3 and merged as #1393 (`IMPROVEMENTS.md` 10-07 15:06). KS-1438 spent its counter and went to Claude. Median round 93 s, median model time 44.8 s, 56.3 model-minutes in total over 72 timed rounds. Rung labels come from `spark/queue.md` comments where stated. done.md has no rung column, so the queue-era rung counts in L2-L5 are only the labelled items.

Table B, the 7 queue-era items that did not PASS on their first run:

| Item | Runs | Cause (source) | Spent a round, current practice | Spent a round, section 5 proposal |
|---|---|---|---|---|
| KS-1278-revoke-atomic | 1 FAIL A3 | harness/brief: not runnable on the checker; the model's patch was identical to the brief in all 4 files (IMPROVEMENTS 10-05 11:4x; daily 10-05 11:42) | no | no (output shown correct) |
| KS-948-mixed-backtick | FAIL B4, PASS, PASS | suspect instrument: 0 pass and 0 fail lines (daily 10-05 11:55) | no | yes |
| KS-1333-blocknumber-pin | REFUSED, PASS | harness: round.sh edited mid-run, verdict lost (IMPROVEMENTS 10-05) | no | no |
| KS-593-adminconfig-negative-offset | FAIL A3d, PASS | harness: A3d read test lines against the product; output byte-identical to the brief (IMPROVEMENTS 10-05 13:4x) | no | no (output shown correct) |
| KS-1438-html-docs-check (rung 3) | FAIL, FAIL | **model**: one inserted `:`, byte-identical both rounds (IMPROVEMENTS 10-09) | yes, counter spent | yes, counter spent |
| KS-1417-p1-env-example (rung 2) | FAIL B1, PASS | format: unclosed output fence (v0.1 section 6) | no | yes |
| ks_1547_p1 (rung 1) | FAIL, FAIL, PASS | harness flake, output tree-identical each time (queue.md:32-33) | no | no |

**Method, Ornith (`2_Project_Files/local-model/night/done.md`, 2026-09-15..10-08).** Non-comment rows without "spark": **507**. Verdict counts: 342 PASS, 146 FAIL, 5 BUILD_REFUSED, 9 CHECKER_NO_RESULT, 2 SKIP_MEMORY, 1 HARNESS_FAIL, 1 DRY_RUN, 1 unparsed. Items = the first token (the ticket), so sub-items of one ticket fold together, which UNDERSTATES first-round rates: **176 items, 172 with a model round, 112 PASS on round 1, 138 PASS within 2 rounds, 151 PASS ever**. By period: 09-15..16 calibration, 27/68 on round 1; 09-17..23, 80/97; 09-24 on, 5/7. One retracted false green (KS-1097 D, `night/done.md:118`) is not subtracted. **All of these rows except the last are Ornith 1.0** (`ornith35b` run tag, `ornith:35b` on Ollama). **Ornith 1.5 has one real ticket row: KS-937, 2026-10-08 21:24, PASS 7/7, rung 2 bash_patch, held 10-09, merged #1444.** Plus the A/B in `ORNITH15_AB.md`. Ornith has run little since the Spark arrived. Kam, 2026-10-09 13:55:51: *"No need to report or apologise"*.

**Method, Claude seats (`0_Brain/projects_index/scoreboard.md`).** Rows naming Sonnet 5.5, 2026-10-10..10-13, all one client: **32 seat rows**.
- Merge 12 (mean 0.958).
- Raise 8 (mean 0.956).
- Mixed lane 10 (mean 0.946).
- Fix round 1 (0.97).
- Build 1 (0.98).
- Overall mean 0.955, range 0.93-0.98.

Opus comparator rows on the same client, 10-09..10-16: R 29th 1.0, R 30th 1.0, F 7th 0.98, J 1st 0.98, R 45th 1.0, R 46th 0.95, J 11th 0.90, D 17th 0.96, D 18th 0.96. That is n=9, mean 0.97, on a different work mix (deploys, a board seat). **Not a like-for-like comparison.**

Majors that gates caught on Sonnet-built or Sonnet-raised PRs: #1450, #1474, #1476, #1484 and #1497 (5). Majors that reached develop: 0, as recorded. Sonnet-tier gates on 10-12: 11, with 1 real Major found (#1464).
