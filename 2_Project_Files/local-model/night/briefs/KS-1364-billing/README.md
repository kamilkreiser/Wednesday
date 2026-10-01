# KS-1364-billing — Spark brief, golden and round 1 (KS-1364 batch 2)

Written 2026-10-01 10:28 AEST by a Spark brief-writer sub-agent for Wednesday (session cb6b682a). Coordinator-approved batch 2 of KS-1364 carves. No PR, no merge, no post, no mail. Linear/GitHub READ only; nothing written under `!CODING/`; git write verbs only in scratchpad clones.

- **Carve:** billing.openapi.ts, insertions after :740 + :880 (2 ops). **Refs KS-1364, does NOT close it.** With batch 1 the six KS-1364 READYs cover 11 of 17 operations.
- **Base:** develop `723dc0722b68482a03de8577fdb5eb5b3359e725` (ls-remote, unchanged since 09:47). Open PRs re-read 10:21: 23, none on these files.
- **Files:** `KS-1364.md` (brief), `golden.diff`, `KS-1364.openapi-yaml.companion.diff` (raise seat's, not the model's), `precheck/` (build_input rc 0 "WEDNESDAY BRIEF"; golden CONTROL PASS 7/7 + A2a; negative with a mutated `+` line FAIL A3c — checked with the new MULTISET A3c).
- **Round 1 (Spark, thinking OFF):** 34.2 s, prompt 20,311, completion 984. **PASS 7/7 strict + A2a**, `patch.diff` BYTE-IDENTICAL to the golden (cmp rc 0); suite 93 -> 98, 0 new reds; tsc rc 0. Run dir `runs/spark_secuura_2026-10-01_KS-1364-billing`. Ladder row 53.
- **Held:** `night/READY_KS-1364-BILLING-1_spark-dsv4flash_*`.
- **For the raise (ONE PR with the other five KS-1364 READYs):** apply the model sections strictly, then this folder's YAML companion, then `npm run check:openapi`.
