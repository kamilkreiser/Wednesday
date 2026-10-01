# KS-1364-platform-tenants — Spark brief, golden and round 1 (KS-1364 batch 3)

Written 2026-10-01 18:02 AEST by a Spark brief-writer sub-agent for Wednesday (KS-1364 residue batch 3). No PR, no push, no post. Linear/GitHub READ only; nothing written under `!CODING/`; git write verbs only in scratchpad clones.

- **Carve:** tenant-provisioning.openapi.ts, one insertion after `:523` (PATCH /api/platform/tenants/{id}). Wednesday ruled it IN; handler 400 re-verified at `index.ts:455`-`:457` at the new base. **Refs KS-1364, does NOT close it.**
- **Base:** develop `0736d8b7849ef6c725c891d7254f2a3e21f42eb6` (#1365; `ls-remote` 17:43 AEST).
- **Files:** `KS-1364.md` (brief), `golden.diff`, `KS-1364.openapi-yaml.companion.diff` (raise seat's), `precheck/` (build_input rc 0 "WEDNESDAY BRIEF"; golden CONTROL PASS 7/7 + A2a; negative FAIL A3c), `READY.md.pre-1001-handline` (backup of the READY before the hand-added raise line).
- **Round 1:** 29.7 s, prompt 17,383, completion 898. PASS 7/7 strict + A2a; patch.diff BYTE-IDENTICAL to golden. Run dir `runs/spark_secuura_2026-10-01_KS-1364-platform-tenants`. Ladder row 56.
- **Held:** `night/READY_KS-1364-PLATFORM-TENANTS-1_spark-dsv4flash_BRIEFED-CODEPATCH-TENANT-PROVISIONING.OPENAPI-PASS-7of7_2026-10-01.diff.md` (hold_ready).
