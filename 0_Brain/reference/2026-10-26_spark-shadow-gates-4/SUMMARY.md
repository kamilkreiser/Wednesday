# SUMMARY shadow4 2026-10-26
Wall-clock ~8m43s total (incl. install).

- #1711: Spark NO GO, 5 findings, 11208/972 tokens, 38.5s
- #1712: Spark GO WITH NOTES, 3 findings, 20726/604 tokens, 35.7s
- #1714: Spark NO GO, 8 findings, 36873/1514 tokens, 80.3s

Notes: #1711 test path in brief was wrong (real: systemTest/__tests__/generated_guard_restore.test.sh); #1711 base also 15/0 (test does not go red on base). #1712 first gate run hit 10s hook timeouts under load 13 (discarded, rerun clean: HEAD 113/0, BASE 99/14). #1714 merge-base = develop tip, HEAD 276/0 = BASE 276/0. No PR bodies supplied (gh not logged in). No commits.
