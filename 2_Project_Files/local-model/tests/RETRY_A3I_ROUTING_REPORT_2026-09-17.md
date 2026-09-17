# night_run.sh RETRY-ONCE routing for A3i INDENT SHIFT + the A3c verdict — report (2026-09-17)

Written by Wednesday from the builder agent's final message. The agent was told to report in its message because the previous agent's report write under `tests/` had been hook-refused.

## BLUF
1. **The runner was swapped.** `night/night_run.sh` swapped 13:37:53, sha `e45575c8056a` → `88988d49f3a1`, backup `night_run.sh.pre-0917-a3iretry`. The lock was absent at the swap.
2. **Three edits.**
   - The retry trigger gains `stopped at A3i \(an indentation shift`.
   - The retry_feedback verdict regex gains `FAIL A3c INCOMPLETE.*` and `FAIL A3i INDENT SHIFT.*`.
   - A fixed INDENT-SHIFT sentence is added to the instruction, outside the `verdict[:600]` slice, so the cap cannot cut it.
3. **Arms** `tests/retry_a3i_routing_arms.sh` (usage: `<new night_run.sh> <old night_run.sh>`): **15/15**. Agent run 13:44:25; **Wednesday's own re-run: 15 passed, 0 failed.**
4. **Regression after the swap:** `a3i_indent_arms.sh` 11/11 (13:40:25) · `a3b_line_number_arms.sh` 19/19 (13:44:21).
5. **IMPROVEMENTS.md** row appended, stamped 13:44 (backup `IMPROVEMENTS.md.pre-0917-a3iretry`).

## FOUND
- **A3c really was missing from the verdict regex.** Old list: A3b / A2b / A3d / A4. KS-1180-P1 r1's retry therefore carried the generic "the checker refused the first attempt (see verdict)" (arm b3).
- **The A3i FAIL line carries no `:NNN \`` shape** (it reads `:21 indent 4, brief 2 …`), so `missed_sites == []` (measured).
- **Correction to the A3I report's premise.** A bare `stopped at A3i` would NOT match today's measure-error line, because the checker prints `stopped at the A3i measure (a harness error…`. The specific clause is still used, since it is robust to future wording changes.

## HOW
- The arm cuts the runner's OWN lines from each runner file (the VERDICT line, the trigger `if`, the `<<'PYR'` builder), asserts each was found exactly once, and runs them on real checker outputs. No regex is re-implemented.
- **Fixtures:**
  - (a) the KS-623 A3i FAIL;
  - (b) KS-1180-P1 A3c FAIL;
  - (c) a measure error synthesised from `checker.sh:591-592`;
  - (d) KS-1121 A3b PARTIAL;
  - (e) KS-730 PASS;
  - (a5) a 900-byte A3i line.
- **Mutation check:** a runner whose trigger also matched `A3i measure` scored 14/15, failing arm c.

## NOT TESTED
- A live model retry end to end (no queue entry, no model call).

## Diff (night_run.sh.pre-0917-a3iretry → night_run.sh), summarised
- The trigger grep gains `|stopped at A3i \(an indentation shift`.
- The builder regex gains `FAIL A3c INCOMPLETE.*|FAIL A3i INDENT SHIFT.*`.
- `a3i_note` holds the sentence when the verdict starts `FAIL A3i INDENT SHIFT`. It is inserted after `verdict[:600] + ". "` in the instruction.
