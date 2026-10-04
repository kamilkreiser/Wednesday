# KS-1388-envexample — Spark brief (bash_patch), golden and round 1

Written 2026-10-05 02:3x AEDT by a Spark brief-writer sub-agent for Wednesday (seat 8e88f5e9). No PR, no push, no post. Linear and GitHub read only. Nothing written under `!CODING/`; git write verbs ran only in scratchpad clones.

- **Carve:** KS-1388 §1, one of its two files: `observability/.env.example:47` `...nginx-gateway:6882/stub_status` -> `:80` (the comment stays commented), plus one new cell in `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh` (MODIFIED in place) pinning the example to the in-network port. The sibling carve is `KS-1388-alerting`; the two edit the test file at non-overlapping points and apply strict in either order (measured). **Refs KS-1388; with the sibling it closes §1 only.**
- **Base:** develop `2d85b84e1012961c880daa3de70d8491fc0a2ff9` (#1374).
- **Files:** `KS-1388.md` (brief) · `golden.diff` · `precheck/` (build_bash_input rc 0; golden CONTROL PASS 7/7; NEGATIVE `:80` -> `:8080` FAIL B3b) · `hold_ready.out` · `READY.md.pre-1005-modeltag` and `READY.ornith-named.as-written.md` (hold_ready's as-written READY, before the marked model-tag correction).
- **Round 1:** 18.28 s, prompt 8796, completion 520, thinking off, `done_reason=stop`. PASS 7/7 strict; A2a by hand hunks=2 ok=2; patch.diff BYTE-IDENTICAL to the golden. Run dir `runs/spark_secuura_2026-10-05_KS-1388-envexample`.
- **Held:** `night/READY_KS-1388-ENVEXAMPLE-1_spark-dsv4flash_BRIEFED-BASHPATCH-ENVEXAMPLE-PASS-7of7_2026-10-05.diff.md` (hold_ready rc 0, then a MARKED hand edit: model tag Ornith -> Spark; IMPROVEMENTS 2026-10-05).
