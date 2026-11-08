# Commission: a `test_only_bash` tier for the Spark harness (Wednesday's own tree; Sonnet tooling subagent). 2026-11-09, the 08:0x seat.

## Why (measured)
Spark operator 111 (report /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator111/report.md) found the pool exhausted, and FOUR tickets (KS-2129, KS-2130, KS-2141, KS-2138 items 2-4) failed ONLY because no tier lets the model edit a bash TEST SUITE on its own: bash_patch2 needs a product script, and test_only_input is vitest/jest only. Rule: every local-model issue gets a TOOLING fix (learnings/2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix.md); never keep the Spark idle (learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md).

## Read first (whole)
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/tiers/ (tier_checker.py, tier_brief.py, build_tier_input.py, task_test_only_input.md, task_doc_only.md, examples/), /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/round.sh, /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/README.md, and how bash_patch2 runs a bash suite (grep the night/ and spark/ trees for bash_patch2). The four tickets' text is in op 111's report.

## Build
A tier `test_only_bash`: the diff may touch ONLY declared `*.test.sh` / bash suite files under Blockchain/Dev/scripts/__tests__/ (or the path the brief declares); product scripts READ-ONLY. Checker legs mirror test_only_input: strict apply at the tip; touched set == declared; runs the declared suite(s) with bash; GREEN without plant on the unmodified product; RED WITH PLANT by the suite's own failure line when a brief-supplied golden_red.diff (plant on a product script) is applied, OR, for a suite whose defect is a wrong regex/sentence in the suite itself, the brief's 'expectations' (grep-able assertions on the suite output) fail on the reverse-applied patch (the doc_only A7 reversion shape); whole-suite no worse where a runner exists; RESTORE to tip sha256. Wire it where the other tiers are wired (round.sh, build_tier_input.py, tier_brief.py, brief_lint.py) by COPY then mv (never edit a running script in place: `pgrep -fl round.sh` and `pgrep -fl queue.sh` first; if either runs, wait and say so). Keep `.pre-1109-bashtier` backups beside every file changed.

## Prove (before anyone uses it)
Arms in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tests/test_only_bash_arms.sh: a PASS arm (a correct suite edit), a touched-a-product-file arm (REFUSED), a red-never-fires arm (REFUSED), a wrong-expected-line arm (REFUSED at apply), a reversion-does-not-discriminate arm (REFUSED). Use scratch clones under /private/tmp only (SPARK_WORK_ROOT style), never the shared Secuura checkout's working tree for writes. No model call needed for the arms (feed canned outputs). Optionally ONE real Spark round on KS-2141 if a brief is writable from the ticket alone; leave the PASS unheld.

## Limits
Never cd; zsh in the Bash tool; never discard stderr; quote heredocs; no rm (quarantine = move with a WHY row); no git commit/push (Wednesday commits); no ticket, PR or mail. DevMASTER ~9.7 GiB free: put every clone on /private/tmp.

## Output
Your final message (a report file Write may be refused): BLUF; files changed with backups; arms table with rc per arm; what is NOT covered; whether the KS-2129/2130/2141 tickets now fit, per ticket.
