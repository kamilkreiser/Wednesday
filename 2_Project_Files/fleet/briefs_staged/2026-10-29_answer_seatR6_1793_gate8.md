## BLUF
#1793 (KS-1250) passed gate 8 (tier 2, round 1 of 2), Seat R 6th: **GO WITH NOTES**. The stub-curl suite is 5/0 at head and 2/3 at the base script, and 9 of 10 script mutants were killed. Merge slot **103**, after T 5th's 100-102. Do not prep yet. Still: no live smoke run, ever, until Kam says so.

## One follow-up to FILE now (search first, quote it; Low; board account; related to KS-1250)
"smoke-test.sh is not remote-clean". It goes on one ticket because one remote run proves all three:
- 12 hard-coded localhost:60xx lines remain after the GATEWAY change (sections 7 onward);
- RUNBOOK §2.2 still tells an operator to do a remote full run;
- the "Smoke target:" line echoes credentials embedded in the URL verbatim.
Also note on it that no cell uses an https:// base (the gate's mutant M11 survives).

## Provenance
- Verdict: 0_Brain/reference/2026-10-29_gate8-batch/verdict.md (claude-sonnet-5-5). Pins unchanged. The gate ran only stub-curl, the localhost default and .invalid hosts in --quick mode, and never a live host.
- The findings are the gate's; Wednesday has not re-run them.
