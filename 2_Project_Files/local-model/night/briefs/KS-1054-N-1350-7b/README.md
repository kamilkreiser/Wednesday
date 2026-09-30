# KS-1054 N-1350-7b — Spark brief + golden + round 1 (deploy-all.sh's rc-1 smoke value names both causes)

Written 2026-09-30 13:22 AEST by a Spark brief-writer sub-agent for Wednesday (residue screen). No PR, no push, no post, no mail, no ticket change. Nothing written under `!CODING/`.

- **Finding:** the deploy-all.sh TWIN of gate47 N-1350-7 — gate47 named deploy.sh only; the brief-writer found the same false claim at `deploy-all.sh:312` (`"one or more failed"` for every rc 1, including a missing parser). Wednesday should decide whether it rides with the deploy.sh half or is dropped.
- **Base:** develop `3e3a68260d0ef541b2410d323849d2639ddd6941`.
- **Shape:** ONE product hunk (`:312` -> 3 lines; trailing context cut to 2 so no context line is blank, header `@@ -309,6 +309,8 @@`), NEW test `ks1054_deploy_all_rc1_message.test.sh` in the ks1054 R8 shape. ref = the ks1054 suite, READ ONLY.
- **Files:** `KS-1054.md`, `golden.diff` (sha256 146819a1616e…), `precheck/` (builder rc 0; CONTROL checker on golden PASS 7/7 strict; `negctl/` test-substring mutation FAIL B5 rc 1; A2a golden rc 0, mutated header rc 1).
- **Measured:** new test at tip 3/1 (N1 by assertion); golden 4/0; ks1054 sibling 36/0.
- **Round 1 (Spark, thinking OFF):** `runs/spark_secuura_2026-09-30_KS-1054-N-1350-7b` — PASS 7/7 + A2a; patch.diff BYTE-IDENTICAL to the golden (cmp rc 0; cross-golden control rc 1). Wall 47.6 s, prompt 19,684, completion 1,569. Held: `night/READY_KS-1054-DEPLOYALLRC1-1_spark-dsv4flash_BRIEFED-BASHPATCH-DEPLOY-ALL-PASS-7of7_2026-09-30.diff.md` (heading + filename fixed by hand, marked).
- **Command:** as the deploy.sh brief, with `product=Blockchain/Dev/deployment/azure/deploy-all.sh test_file=Blockchain/Dev/scripts/__tests__/ks1054_deploy_all_rc1_message.test.sh`.
- **Scope:** the deploy-all.sh twin only. Refs KS-1054, does NOT close it.
