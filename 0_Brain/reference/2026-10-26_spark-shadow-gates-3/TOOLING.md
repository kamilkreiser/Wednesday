# Spark gate tooling, 2026-10-26 (C8 tooling drafter) + shadow calibration 3
All under local-model/gate/. Backups (beside the originals): spark_review.py.pre-1026-repguard, spark_gate.sh.pre-1026-runner, shadow_facts.py.pre-1026-runner, REVIEW_CHECKLIST.md.pre-1026-prbody. No process was running any of them. Nothing deleted, nothing committed.

## Part 1 changes
1. spark_review.py: reply now STREAMED; `detect_repetition()` (same "claim" >=3x, or a 12-word run >=4x, checked every ~1500 chars) aborts the stream (finish=repetition_abort, frees the box). `dedupe_findings()` runs before schema validation. Retry no longer resends the looping text: it is original prompt + a short anti-repetition instruction, max_tokens capped at 4000. meta gains duplicate_findings_removed, per-attempt repetition and max_tokens. Also: missing Linear env file no longer crashes; `--dry-run` writes the prompt and stops.
2. Runner: DECISION = fold, not fork. spark_gate.sh does fetch / head-sha assertion / missing-file refusal / diff, and for non-.py tests HANDS OFF to shadow_facts.py (the single non-pytest harness). shadow_facts.py gained `--tests`, `--node-modules`, bash `N passed, M failed` parsing, `/bin/bash` runs, vitest failed-only parsing, per-file `ok`/`count_unparsed`, `targeted_head_totals`/`targeted_base_totals`, tsc step made conditional, relpath fix for a package.json at repo root. Mixed .py + non-.py REFUSES (exit 2). Bug found by the first live run and fixed: empty `NMARG[@]` under bash 3.2 `set -u` (now arm 8).
3. PR body: `--pr-body-file` (alias of the existing `--pr-body`; it was already wired into the prompt but never supplied). REVIEW_CHECKLIST.md item 11 now applies the overstated-sentence test to the PR description too ("[PR body] " prefix).

## Arms, exactly as printed
- tests/test_spark_review_arms.py: `spark_review arms: 0 failed` - 9 ARM lines, all PASS (1 22x repeat caught; 2 normal passes; 3/3b dedupe 21 of 22 and leaves normal untouched; 4/4b mock server loops ~187 KB, aborted after ~16.6 KB, retry hint present, loop text not resent, cap 4000, valid; 5/5b PR body in prompt / "(not provided)" without; 6 clean review accepted in 1 attempt).
- tests/test_gate_runner_arms.sh: `gate runner arms: 8 passed, 0 failed, 0 skipped` (shell good PR HEAD 3/0, BASE 2/1; shell planted failure 2/1 ok=False; vitest good HEAD 3/0, BASE 2/1; vitest planted 2/1 ok=False; missing file exit 4; mixed exit 2; wrong sha exit 3; no --node-modules).
- tests/test_spark_gate_arms.sh (old, run against the shadow3 clone): ARM1 PASS, ARM2 PASS, ARM3 PASS (3/3).
- Fixtures: tests/fixtures/vitest_repo/ (package.json + .gitignore; node_modules was `npm install`ed there, 24 MB, machine-local: gitignore it, add to PORTABILITY/doctor if the vitest arms matter). Arm scratch goes outside WEDNESDAY (the gate refuses a work dir under it).

## Part 2 (ran; Part 1 arms all passed)
Clone: spark/cache/work/shadow3_20261026/repo (--shared, remote URL + core.sshCommand copied). origin/develop = e9e32b76... as briefed. Work dirs in the session scratchpad (the gate refuses --work under WEDNESDAY).
- #1708: gate 76 s; Spark 75.1 s, 43613 prompt / 1025 completion tokens, 1 attempt. NO GO. HEAD 196/0, BASE 196/0.
- #1709: gate 36 s; Spark 105.5 s, 48541 prompt / 2041 completion tokens, 1 attempt. NO GO. HEAD 36/0, BASE 25/11.
No Claude-gate scoring done.

## NOT done / limits
- PR bodies: gh not logged in (global and both Secuura project configs) -> "PR body not supplied" for both; the overstated-sentence path is armed (dry-run arm) but was not exercised live.
- #1709's 2 changed vitest files (services/security) not run: no install in the clone.
- For test-only PRs (#1708) BASE product code == HEAD, so "red on base" is vacuous; the pre-PR tests were not run.
- Repetition guard is proven against a mock stream, not a real Spark loop (the real run did not loop). The real streaming path was exercised twice (usage returned with include_usage).
- No planted-violation step in the runner (still owed from calibration 1).
