# KS-1345-list — Spark brief, golden and round 1

Written 2026-10-05 02:3x AEDT by a Spark brief-writer sub-agent for Wednesday (seat 8e88f5e9). No PR, no push, no post. Linear and GitHub read only. Nothing written under `!CODING/`; git write verbs ran only in scratchpad clones.

- **Carve:** `services/originate/src/routes/webhooks.ts` GET / — the list query's `.catch(... return [])` (`:196`) is dropped so a rejection reaches `fail500` (500 + constant body + logged); the KS-466 comment (`:189`) is reworded and two lines added. The KS-1341 part A test's `control KS-1341 A0` (which pinned the swallow) becomes `RED KS-1345 A0`, plus a new `control KS-1345 C` (a resolving query still answers 200 with its rows). **Refs KS-1345, does NOT close it**: the `GET /:id/deliveries` half (`:412`) needs a decision (a non-UUID id would become a 500), so it goes to a Claude seat.
- **Base:** develop `2d85b84e1012961c880daa3de70d8491fc0a2ff9` (#1374).
- **Files:** `KS-1345.md` (brief) · `golden.diff` (fence form, 3 hunks) · `precheck/` (build_input rc 0 "WEDNESDAY BRIEF"; golden CONTROL PASS 7/7 + A2a; NEGATIVE `` `; `` -> `` `.catch(() => []); `` FAIL A3c) · `hold_ready.out`.
- **Round 1:** 45.67 s, prompt 23,875, completion 1,358, thinking off, `done_reason=stop`. PASS 7/7 strict + A2a; patch.diff BYTE-IDENTICAL to the golden. Red 1/9 -> 9/9; originate suite 1062 -> 1063, 0 failed; tsc rc 0. Run dir `runs/spark_secuura_2026-10-05_KS-1345-list`.
- **Held:** `night/READY_KS-1345-LIST-1_spark-dsv4flash_BRIEFED-CODEPATCH-WEBHOOKS-PASS-7of7_2026-10-05.diff.md` (hold_ready rc 0, no hand edit).
