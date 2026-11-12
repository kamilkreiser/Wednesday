# Commission: Spark TEST-DIGEST harness (pilot (a) of Kam's 2026-11-12 11:34 Spark instruction). Wednesday, 11:3x AEDT.

## Why (read first)
- Kam, live board 11:34:05, verbatim, and Wednesday's answer: `0_Brain/learnings/2026-11-12_spark-for-harness-and-token-heavy-simple-tasks.md` (read whole).
- Running a suite costs no tokens; Claude gates and build seats burn their windows READING raw output. The Spark (DeepSeek V4 Flash on the Spark box, one request at a time, thinking OFF for this work, 384K context) reads the raw output and returns a one-page digest; a DETERMINISTIC checker re-derives every number in the digest from the raw file and refuses on any disagreement.

## Read before building
- `2_Project_Files/local-model/spark/` (tunnel.sh, the runner, how a request is made; never a second concurrent request: check `fleet/spark_status.py` and the queue/lock the existing runner uses before calling the endpoint).
- `2_Project_Files/local-model/gate/` (spark_review.py, gate_facts.py, CHANGES.md: the closest existing pattern, including the repetition guard and the oversized-input handling).
- `0_Brain/learnings/2026-09-23_spark-kit-running-a-local-coding-model.md` (thinking eats the budget; empty answer = a thinking block, not a verdict).

## Build (in `2_Project_Files/local-model/digest/`, tracked; never a scratchpad)
1. `digest.py <raw-output-file> --kind vitest|jest|bash-suite|tsc|generic --out <dir>`: (i) a deterministic PARSER per kind extracts the ground truth (files/tests passed/failed/skipped, each failure's name + first error line + first stack frame); (ii) the Spark is asked for the digest in a fixed JSON shape (counts, failures[], anomalies[] such as warnings, slow tests, unhandled rejections the parser does not cover); (iii) a CHECKER compares every Spark count and every failure name against the parser's; any mismatch -> the digest is REFUSED and the parser's own summary is emitted instead, with the mismatch recorded. Output: `digest.md` (one page, BLUF first: verdict, counts, failures) + `digest.json` + `check.json`.
2. A `--delta <previous digest.json>` mode: tests newly failing, newly passing, count changes.
3. Arms in `2_Project_Files/local-model/digest/tests/arms.sh`, run before declaring done: a real passing vitest output, a real failing one (make one by planting a failing assertion in a scratch copy of a small suite; never in a project checkout), a jest output, a bash-suite output, a truncated/garbled file (must refuse cleanly), a planted wrong Spark count (simulate by a stub response: must REFUSE), Spark unreachable (must fall back to the parser summary, rc 0, and say so).
4. Measure on TWO real artefacts already on disk: gate 324's raw suite logs in `0_Brain/reference/2026-11-12_gate324-tier2-pr2202/` (scratch or out_* subfolders) and one more gate's. Report raw bytes vs digest bytes, Spark wall-clock, and whether the checker passed.

## Limits
- Secuura content only per Spark task (one client). Read-only on every project checkout (read git verbs; any suite run happens in a clone in YOUR scratch). Never delete files. Never print credential values. No mail, board or Linear writes. Do not edit a running script (check `pgrep` first). Gitignore any run-output directory in the same action you create it.
- If the Spark endpoint is down, build and arm everything with the stub, report the live arm as NOT RUN, and say why.

## Output
`report.md` in THIS folder: what was built (paths), the arms table (PASS/FAIL each), the two real measurements, NOT TESTED, and the one-paragraph instruction a gate brief would carry to use it. Final message: a 10-line summary.
