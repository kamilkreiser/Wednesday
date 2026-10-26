# Spark shadow gate, PR #1708 (KS-1728), head a6bb564a9bf53f7d310adc4a4af672783c9ffd3e (UNSCORED; Wednesday scores against the Claude gate)
Spark verdict: **NO GO** (3 Major, 2 Minor, 1 Note). PR body: not supplied (gh not logged in). Review: 1 attempt, 75.1 s, 43613 prompt / 1025 completion tokens.
Deterministic half (no model), 76 s: 3 bash suites, 196 passed 0 failed on HEAD; 196 passed 0 failed on BASE product code (PR changes only test files, so base product == head; the old tests were not run).
Spark Majors, in short: (1) mechanism unproven per the ticket, (2) only 2 of 4 `printf|grep -q` branches in preflight_deps.test.sh changed (lines 441-442 cited), (3) 150 other occurrences untouched. 3 of 6 findings had a quote not found verbatim in the input (flag `evidence_quote_found_in_input: false`).
Raw: review.json, review/raw_attempt1.txt, facts.json.
