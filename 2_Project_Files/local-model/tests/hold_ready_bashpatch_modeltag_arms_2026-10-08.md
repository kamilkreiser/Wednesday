# hold_ready.py --model-tag on bash_patch — arms, Thu 08 Oct 2026 02:54:15 AEDT

Why: the Spark writes bash_patch runs (KS-1139, 2026-10-07). Before this change `--model-tag` was refused on every path but code_patch, and WITHOUT it the bash READY named a Spark diff `ornith35b-q4` (a false label), so KS-1139 was held by hand. Owed in the pickup since 10-07 (met twice). `--brief` stays code_patch-only.

Backup: `night/hold_ready.py.pre-1008-0256-bashmodeltag` (`cmp` rc 0 against the pre-edit file, taken before any edit).
Change: 3 lines of logic — the refusal split into a `--brief` clause (code_patch only) and a `--model-tag` clause (code_patch OR bash_patch); the bash READY filename uses `{model_tag}`, its heading `{model_label}`.

Runs used (all real, read-only, `--dry-run` unless stated):
- bash: `runs/spark_secuura_2026-10-07_KS-1139-smoke-test-counters-errexit` + its `-control` golden, ROWID SMOKECOUNTERS-1
- code_patch: `runs/2026-09-22_ks1265-ornith35b-night` + golden `runs/2026-09-22_feed3-drafter-precheck/1265EARLYGUARD-R16`
- test_only: `runs/2026-09-22_ks947-ornith35b-night2`

| arm | BEFORE (old code) | AFTER | verdict |
|---|---|---|---|
| defect: bash + `--model-tag spark-dsv4flash` | rc 2 REFUSE "code_patch path only" | rc 0, `READY_KS-1139-SMOKECOUNTERS-1_spark-dsv4flash_BRIEFED-BASHPATCH-…` | FIXED |
| bash, no tag (regression) | rc 0 | rc 0, clock-normalised `cmp` rc 0 vs BEFORE | PASS |
| code_patch, no tag (regression) | rc 0 | clock-normalised `cmp` rc 0 | PASS |
| code_patch + tag (regression) | rc 0 | clock-normalised `cmp` rc 0 | PASS |
| test_only, no tag (regression) | rc 0 | clock-normalised `cmp` rc 0 | PASS |
| test_only + tag (must still refuse) | rc 2 | rc 2 "--model-tag is supported on the code_patch and bash_patch paths only" | PASS |
| bash + `--brief` (must still refuse) | rc 2 | rc 2 "--brief is supported on the code_patch path only" | PASS |
| control: AFTER bash no-tag vs AFTER bash tag (must DIFFER) | — | `cmp` rc 1 | the comparison instrument can fail |
| real WRITE (scratch copy of the script with NIGHT_DIR → scratchpad) | — | heading `# READY — KS-1139-SMOKECOUNTERS-1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA`; `night/` READY count unchanged (474 before and after) | PASS |

Not done, on purpose: the hand-held KS-1139 READY in `night/` was NOT regenerated — Seat R 14th is raising from it now (a live lane's input does not move under it).
Not tested: doc_patch + tag (refused by the same clause as test_only; not run).
