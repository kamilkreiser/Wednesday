# o149 RE-COMMISSION (operator o149r). The first o149 died with the 03:0x coordinator rotation (~40 min in, no report.md)

Re-commissioned 2026-11-12 ~03:1x AEDT by the 03:0x Wednesday rotation-successor seat (Mac mini).

commission.md in this folder is binding (TASK 1 KS-1376 doc_only; TASK 2 the arm refresh). The pin moved: develop is now 801a2a7145c6ad7ea5d6139b799b18d45ba824d3 (Wednesday ls-remote ~03:0x; PR 2179 merged). Re-read ls-remote before every round.

WHAT ALREADY EXISTS (committed by the coordinator in a9d89b36cb as "o149 PARTIAL ... unverified"; read it, do not trust it, do not redo it blindly):
1. KS-1376 brief + golden: 2_Project_Files/local-model/night/briefs/ks_1376_o149_p1_038a_header_two_false_claims/ (KS-1376.md, golden.diff, spark.pins). Its pins were cut at dbde0ac76339: re-verify lines 16-17 of 038a and 058 lines 68-79 at 801a2a7145c6 (they are unlikely to have moved; prove it) and re-pin if needed. scratch/dry1376.txt is the old run's dry build. The KS-1376 ROUND WAS NEVER RUN: run it (the checksum grep first, as the commission says).
2. Arm refresh, PARTIAL: test_only_arms.sh and spec_examples_arms.sh were edited (backups *.pre-1112-armrefresh beside them in local-model/spark/tests/). Their before/after pass counts were NEVER recorded. Run both now and report counts against the .pre backups (run the backup too, from a copy, for the "before"). config_tier_arms.sh is UNTOUCHED: still owed (19 stale fails). The `## Tamper` scripts-path arm (TASK 2b): check whether spec_examples_arms.sh already carries it (scratch/arm_e*.out suggest an arm e was being built); if not, add it, proved both ways.
3. scratch/ holds the dead run's outputs (arm_*.out, e*.json, cfg_before.txt, cfgT1/, held.json, prs.json). Use them only as hints; re-measure.

Never edit a script that is running (pgrep first). Copy-edit-mv; never delete. Report to report.md in THIS folder, under 60 lines, naming which of items 1-3 you finished and the counts.
