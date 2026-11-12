---
date: 2026-11-12
type: preference
source: Kam, live board 2026-11-12 11:34:05 (view=wednesday)
status: live
tier: W
---

# Use the Spark where tokens are spent on BULK, not judgement: digest test-harness output and run simple token-heavy jobs on an ongoing basis; it is not much use on tickets

**His words, verbatim:** *"I have been thinking.  as the spark is not much use on tickets, can we utilise it in running harness and other tests.  these seem to be token intensive and could be lead with a good testing harness.  In addition to this, have a think about simple and token expensive tasks that we could get the spark to do on an ongoing basis"*

**The operative case, so the headline matches it:** Wednesday is choosing work for the Spark, or noticing a Claude seat or gate spending its window reading long raw output (test logs, suite runs, diffs, compose logs, board censuses). **Ask: can the Spark read the bulk and hand Claude a short summary whose every number a script checks against the raw file?** If yes, that is Spark work. Ticket-fixing is no longer the default Spark job.

**How to apply:**
1. **Running a suite costs no tokens; READING its output does.** The Spark's role is the digest: counts, every failure with its first stack line, the delta since the last run. A deterministic harness re-derives every count from the raw output and refuses a summary that disagrees, so a wrong summary is caught rather than trusted ([[2026-08-07_a-check-that-cannot-fail]]).
2. **Candidates, in Wednesday's order (told to Kam 11:3x, bf-52eeb070f409):** (a) test-run digests for gates and build seats; (b) a nightly stale-ticket screen (does the cited code still exist at develop; already fixed; duplicate), proposals only, a Claude seat confirms before any board change; (c) mechanical test work: mutant generation for red-proofs, numstat/count reconciliation of a seat's claims.
3. **Not for judgement:** its shadow review on gate 324 recalled 0 of 5 findings. Code review and rulings stay with Claude gates.
4. **Pilot, measure, then standing** (go-slow rule 4): pilot (a) on the next two gates: tokens saved vs summary errors caught by the harness. Then (b) overnight.
5. Unchanged: one client's content per Spark task; the Spark never merges or writes to a board; the never-idle rule stands, and this widens what "busy" can mean.

**Family:** [[2026-10-28_never-keep-the-spark-idle-quota-and-capability-data]] · [[2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice]] · [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] · [[2026-08-03_go-slow-earn-autonomy]].
