# KS-1054 N-1350-7 — Spark brief + golden + round 1 (deploy.sh's rc-1 line names both causes)

Written 2026-09-30 13:22 AEST by a Spark brief-writer sub-agent for Wednesday (residue screen). No PR, no push, no post, no mail, no ticket change. Nothing written under `!CODING/`; git write verbs only in this session's scratchpad clones `rs/{src,gold,ctl,round}`.

- **Finding:** gate47 N-1350-7 (Polish; report `:374`, evidence `:167`), carried unraised by B 47th's handover `:177`.
- **Base:** develop `3e3a68260d0ef541b2410d323849d2639ddd6941` (`ls-remote` 03:09:42Z, unchanged at the builder run).
- **Shape:** ONE product hunk (`deploy.sh:857` -> 3 lines), NEW test `ks1054_deploy_sh_rc1_message.test.sh` (79 lines). ref = the ks1054 suite, READ ONLY (B 49th owns it).
- **Files:** `KS-1054.md` (brief; fences filled FROM the golden by script), `golden.diff` (sha256 898dd867aa24…), `precheck/` (builder input, CONTROL checker run on the golden = PASS 7/7 strict; `negctl/` product-line mutation = FAIL B3b rc 1; `negctl2/` test-substring mutation = FAIL B5 rc 1).
- **Measured:** new test at tip 3/1 (M1 by assertion); golden 4/0; ks1054 sibling 36/0 on the golden; A2a golden rc 0, mutated header rc 1.
- **Round 1 (Spark, thinking OFF):** `runs/spark_secuura_2026-09-30_KS-1054-N-1350-7` — PASS 7/7 + A2a; BYTE-IDENTICAL to the golden. Wall 59.6 s, prompt 31,344, completion 1,574. Held: `night/READY_KS-1054-DEPLOYRC1-1_spark-dsv4flash_BRIEFED-BASHPATCH-DEPLOY-PASS-7of7_2026-09-30.diff.md` (heading + filename fixed by hand, marked).
- **Command:** `NIGHT_SOURCE_CHECKOUT=<rs/src> bash tasks/bash_patch/build_bash_input.sh KS-1054 <input> KS-1054.md product=Blockchain/Dev/deployment/azure/deploy.sh ref=Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh test_file=Blockchain/Dev/scripts/__tests__/ks1054_deploy_sh_rc1_message.test.sh` -> `LM_BACKEND=spark SPARK_THINK=0 bash local_model_task.sh tasks/bash_patch/task.md <input> <out.md>` -> `bash tasks/bash_patch/checker.sh <input> <out.md> <clean clone at tip>` -> `a2a_anchor.py` by hand (`n` added to sections.json).
- **Scope:** closes N-1350-7 in deploy.sh only. Refs KS-1054, does NOT close it. The WORDING is the brief-writer's choice (the gate named the defect, not the text).
