# Spark test-digest harness — report (pilot (a), 2026-11-12)

Filed by Wednesday from the building agent's returned text (its Write was refused by the harness), 2026-11-12 ~11:5x AEDT. Wednesday did not re-run the arms; the numbers below are the agent's.

## BLUF
- Built `2_Project_Files/local-model/digest/digest.py` (parser + Spark client + checker + renderer + delta; stdlib only) with `tests/arms.sh` (40 arms) and 7 real-log fixtures. **40/40 arms PASS; live arm CHECKED in 3.4 s.**
- **Live on real gate logs: 4 of 5 CHECKED, 1 correctly REFUSED** (gate 131's 28-failure vitest log: the Spark wrote "over 1500ms" where the log says 1503/1505/1506 ms).
- **Raw 25-60 KB -> digest 1-2 KB**, 7-14 s of Spark time (71 s on the 28-failure log). A gate reading the digest spends ~300-500 tokens instead of 7-20K per log.
- The checker caught a real model error in development: summing 12 summary lines to 366 where the truth is 367 — the code now sums the lines the Spark lists.

## Statuses
| status | meaning | rc |
|---|---|---|
| CHECKED | Spark digest accepted; every number re-derived from the raw file | 0 |
| REFUSED_MISMATCH | Spark digest refused; parser summary emitted; mismatches in check.json | 0 |
| PARSER_ONLY_SPARK_DOWN | Spark unreachable / timed out / empty reply; parser summary, and digest.md says so | 0 |
| PARSER_ONLY | --no-spark | 0 |
| NO_GROUND_TRUTH | raw truncated / garbled / empty; Spark not asked | 3 |

Checker verifies (the Spark is never shown the parser's answer): verdict and every count; every failure name one-to-one; every quoted error/frame line verbatim in the raw; every 2+-digit number in an anomaly sentence present in the raw. Anomaly wording itself is NOT verified and digest.md labels it advisory.

## Live measurements (deepseek-v4-flash-0731, thinking off)
| artefact | kind | raw | digest | Spark | prompt tok | checker |
|---|---|---|---|---|---|---|
| gate 324 out_dev (11 logs) | bash-suite | 25,748 B | 952 B | 12.4 s | 7,729 | CHECKED |
| gate 324 out_head (12 logs) --delta | bash-suite | 28,732 B | 1,135 B | 7.4 s | 8,583 | CHECKED |
| gate 199 base, full jest | jest | 59,555 B | 1,294 B | 11.8 s | 19,838 | CHECKED |
| gate 199 head --delta | jest | 59,741 B | 1,834 B | 13.8 s | 19,905 | CHECKED |
| gate 131 rw_base_vitest (28 fail) | vitest | 41,268 B | 9,182 B (parser) | 71.2 s | 11,964 | REFUSED (rounding) |

## Arms (40/40 PASS)
Real passing/failing vitest, 28-failure vitest, failing jest, failing/passing bash-suite, real tsc: CHECKED. Truncated/garbled/empty/tsc-count-mismatch: rc 3, Spark not asked. Planted wrong count, wrong verdict, omitted failure, invented failure, paraphrased error, anomaly number absent, prose instead of JSON: REFUSED. Controls (absent number refused / present accepted / fenced JSON / dict rows / null for a printed count refused). Spark unreachable + empty reply: parser summary, rc 0. Delta (fail->pass, pass->fail, cross-kind reported not computed). Missing input rc 2. Live arm L CHECKED 3.4 s.

## NOT TESTED
generic kind live; tsc live (stub only) and `--pretty` output; inputs > 400,000 chars (head 25% + tail 75% cut coded, no arm); watch-mode / multi-project output; vitest retry beyond de-dup; the 900 s Spark timeout path; failure lists > 200 (capped, coverage check relaxed); a re-run of gate 131 with a "quote durations exactly" prompt (refusal left standing as evidence).

## Note on the B7 line
The agent flagged gate 324's `docs_fragments` B7 failing in both digests. That is gate 324's own finding G324-2202-3 (Info): B7 fails whenever TMPDIR sits inside a git work tree (the gate's harness ran under WEDNESDAY); 81/0 outside. Not a new finding.

## Standing instruction for gate and build briefs (Secuura; Wednesday's seat, the Spark is the Studio's)
Do not read raw suite output in full. Run each suite to a log file, then `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/digest/digest.py <log> --kind vitest|jest|bash-suite|tsc|generic --out <dir>` (add `--delta <previous digest.json>` for a re-run or a base-vs-head pair). One Secuura log per call; it waits for the Spark box by itself. Read only `<dir>/digest.md`. CHECKED = trust the numbers; REFUSED_MISMATCH / PARSER_ONLY_SPARK_DOWN = the parser's (deterministic) numbers; NO_GROUND_TRUTH (rc 3) = read the raw log and re-run. Anomaly sentences are the Spark's wording with numbers checked: grep the raw log before any of them enters a ruling. **The digest replaces reading, never a ruling.**
