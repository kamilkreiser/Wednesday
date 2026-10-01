# KS-1364-v2-verify — Spark brief, golden and round 1 (KS-1364 batch 3)

Written 2026-10-01 18:02 AEST by a Spark brief-writer sub-agent for Wednesday (KS-1364 residue batch 3). No PR, no push, no post. Linear/GitHub READ only; nothing written under `!CODING/`; git write verbs only in scratchpad clones.

- **Carve:** originate.openapi.ts, one insertion after `:2055` (POST /api/v2/verification/verify; route stays public). Handler refuses an absent body at `routes/verificationV2.ts:452`-`:456`. Jest test in the render shape; ref = originate's own spec-registry test `ks978`. **Refs KS-1364, does NOT close it.**
- **Base:** develop `0736d8b7849ef6c725c891d7254f2a3e21f42eb6`.
- **Input:** `NIGHT_EXCERPT_TRIGGER_BYTES=90000` (the 155 KB product file is carried as 4 regions).
- **Files:** `KS-1364.md`, `golden.diff`, `KS-1364.openapi-yaml.companion.diff`, `precheck/` (build_input rc 0; CONTROL PASS 7/7 + A2a; negative FAIL A3c), `READY.md.pre-1001-handline`.
- **Round 1:** 30.6 s, prompt 19,812, completion 810. PASS 7/7 strict + A2a; BYTE-IDENTICAL to golden. Run dir `runs/spark_secuura_2026-10-01_KS-1364-v2-verify`. Ladder row 57.
- **Held:** `night/READY_KS-1364-V2-VERIFY-1_spark-dsv4flash_BRIEFED-CODEPATCH-ORIGINATE.OPENAPI-PASS-7of7_2026-10-01.diff.md` (hold_ready).
