# KS-1015-delegation-get — Spark brief, golden and round 1

Written 2026-10-02 06:20 AEST by a Spark brief-writer sub-agent for Wednesday (session 73252fd5). No PR, no push, no post. Linear and GitHub were read only. Nothing was written under `!CODING/`. Git write verbs ran only in scratchpad clones.

- **Carve:** `transfer.openapi.ts`, one one-line replacement at `:1196`: the GET /api/delegations/{id} 200 body becomes `successEnvelope({ delegation, chain })`, matching `routes/delegations.ts:148`-`:154`. The source is KS-1015's 2026-09-29 sweep comment, the sibling of #1367. **Refs KS-1015, does NOT close it.**
- **Base:** develop `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e` (#1369). Read by GitHub REST at 06:0x AEST and by `ls-remote` at 06:20.
- **Files:**
  - `KS-1015.md`: the brief.
  - `golden.diff`: product first, then the new test.
  - `KS-1015.openapi-yaml.companion.diff`: the raise seat's file (+38/-1).
  - `precheck/`: build_input rc 0 "WEDNESDAY BRIEF"; golden CONTROL PASS 7/7 + A2a; NEGATIVE FAIL A3c.
  - `hold_ready.out`.
  - `READY.md.pre-1002-handline`: the READY as hold_ready wrote it, before the marked raise line was added.
- **Round 1:** 49.8 s, prompt 25,795, completion 1,526, thinking off, `done_reason=stop`. Result: PASS 7/7 strict + A2a, and patch.diff is BYTE-IDENTICAL to the golden (cmp rc 0). Run dir: `runs/spark_secuura_2026-10-02_KS-1015-delegation-get`. Ladder row 58.
- **Held:** `night/READY_KS-1015-DELEGATION-GET-1_spark-dsv4flash_BRIEFED-CODEPATCH-TRANSFER.OPENAPI-PASS-7of7_2026-10-02.diff.md`, written by hold_ready.
