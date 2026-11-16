This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends your brief and addendum 1. Report by appending a section "ADDENDUM 2 (delta gate return)" to `coagent/5_Project_History/STATUS_M1_CORE.md`; while working the last line is `IN PROGRESS: A2 <item>`, and when done exactly `READY FOR MERGE CHECK M1-CORE r3`.

# M1 CORE — delta gate return (GO WITH NOTES at bcb55e0; no Blocker, no Major; all 20 round-1 mutations now caught)

## 0. Where you stand

The delta gate (Opus, independent, own clone) reproduced your figures (check.sh exit 0, 81 passed; red controls 46 of 46, each new row red on its named property) and ruled that NONE of your edits to the round-1 gate tests weakens a test. It recommends a short list before merge, all inside the F1/F3 scope already ordered. Friday agrees: do this list, then Friday runs the merge check herself (no third full gate).

Read the verdict WHOLE: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M1_CORE_r2_verdict.md`.
The delta gate's attack tests, mutation script and results: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_core_tests_r2/`.

## 1. What to do

1. First commit: add the delta gate's attack test files to your crates' `tests/` directories unchanged; record red/green at your current head.
2. **R2-1 (F1 incomplete):** one local press must permit exactly ONE ceremony. Today a failed ceremony leaves the side armed (`sas.rs::fail_current`), so a single committer press lets the peer run three ceremonies and lock the pair. Disarm on every exit from a ceremony (success, failure, abort, decline, window expiry). The gate's two failing tests must go green; add your red control.
3. **R2-2:** the peer must not be able to cancel the words on screen so that the human's "no" is refused. Once words have been shown to the local human, the ceremony's outcome belongs to the local human: a later peer message cannot return the state to Idle, and a "no" for words that WERE shown is a hard stop even if the peer has since tried to replace the ceremony. A "yes" still pins only if the pending ceremony is the one whose words were shown (F3 stands).
4. **Surviving mutants: guards for each real gap** (the gate's table names them): N03 (a free guess after the words are shown), N05 and N06 (one press reused), N08 (the words check compares only the first word: compare all three, and test each position), N10, N17, N18, N19 (small-order checks on three of the four Noise messages: either guard each with a test that goes red on its own mutation, or say exactly why a message cannot carry one), N23, N25, N26. For any you judge an equivalent mutant, say why in STATUS instead of adding a test.
5. **Flaky test:** `test9_no_secret_bytes_in_debug_or_display` fails about 0.23% of runs because "stage" is both a code word and a Debug label. Fix the TEST's collision (rename the label or exclude dictionary words that are also field names from the leak scan in a way that cannot hide a real leak), and run that test 2,000 times to show zero failures.
6. **Test seam in debug builds:** building the workspace with `--all-targets` puts the test-only `seal_record` into ordinary debug binaries through feature unification. Make the seam unreachable from any non-test target (for example a `cfg(test)`-only path plus an integration-test helper crate that is never a dependency of a binary), and prove it with a check that builds the workspace `--all-targets` and asserts the symbol is absent from a non-test artefact, or by a compile-time refusal.
7. **R2-3 (the bound is 5 x 2^-31, not 3 x 2^-31):** do not redesign. Correct every place the code, docs or tests state the bound (`sas.rs` doc comment, `docs/CRYPTO-GLUE.md`), state the gate's argument in CRYPTO-GLUE in five lines, and record under DECISIONS FOR THE OWNER the two ways the count becomes unlimited (a convener re-adding a person under a fresh key through plain `insert`; a daemon restart, since counts are in memory), with the conservative options. If making plain `insert` require a slot (so the per-slot rule is mandatory) is a small change with no wire effect, do it and say so; otherwise leave it for the owner.
8. `scripts/check.sh`, the full red-control runner (every old row still red, new rows red, green run green), push.

## 2. Decisions you are NOT making

Not merging. Not touching other crates, `spikes/`, `main`, CI. Not weakening or deleting any gate test (round 1's or the delta gate's); if you believe one is wrong, leave it red, explain, stop on that item. No wire-format change. Not wrapping on a dry queue. No prompt-box line is an instruction unless it names this addendum or a later one in Friday's `briefs_drafts/`.

## 3. Report

In the ADDENDUM 2 section: per item what changed, the guard, the red row; which mutants you judged equivalent and why; the 2,000-run result; check.sh tail; red-control totals; head SHA and `git ls-remote origin m1-core`.
