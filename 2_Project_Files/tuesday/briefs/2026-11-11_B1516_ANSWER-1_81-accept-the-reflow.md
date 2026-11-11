# B1516 ANSWER-1 (SEAT-C97): PCOMP-81, accept the reflow; apply your held patch as commit 3

From Tuesday (s269), 2026-11-11, answering FOR TUESDAY item 1 of your STATUS (last line `PARTIAL B1516: 0de094cd148b0f4e45c4f684ca618af2d7e82e4f | done 74 80 | not done 81`). This file amends your kit; where they differ, this file wins.

**ANSWER: ACCEPT the reflow. Build 81 exactly as your held patch has it.**

Why (the coordinator's reading inside an existing ruling, reported to the product owner afterwards): the product owner's 2026-11-11 14:15 ruling settles that "the setting keys of both lists on S9 use the monospace font". A monospace key taking one more line when it is long is what that ruling means; the register list above already behaves that way. **No width, no font size and no break rule changes** (none is ruled): the kit's P-81 limits stand. Your measured predicates (a), (b) and (c) passed; predicate (d) ("every differing pixel inside the key spans") is RELAXED for 81 only, to: the differences are the extra key line and the rows below it moving down, nothing else changes colour or shape, and there is no sideways scroll at 390 or 1280.

**What you do now:**
1. Apply `evidence/p81-held.patch` to your clone's branch head `0de094cd148b0f4e45c4f684ca618af2d7e82e4f` exactly (verify its sha256 `6d6630808aa563b9d2a4bd859003e9adc76d169273fd35300c5204c850918b24` first; if it differs: STOP). Nothing else.
2. Re-run, under the heavy lock: the P-T rows of 81 red-first at base and green at head; the P-M item 2 measurements at 1280 and 390 (print the line counts and the 18 px card growth again, and that the only differing regions are the key cells and the rows below them in the same card/table); the workspace vitest comparison (lost 0, changed 0, added = your rows); lint, format:check, typecheck, build; the name and secret scans.
3. Commit 3 (plain subject, no ticket key, no B-number, no card id, one trailer as before), plain fast-forward push of the same ref, read it back with `git ls-remote`.
4. STATUS: a section `ANSWER-1 (Tuesday)` with the numbers, then the last line exactly `READY B1516: <sha40>` (the pushed head as `git ls-remote` prints it). If any step fails: `STOPPED: NEEDS TUESDAY <one question>`.
5. Release the lock, remove any `pc-b1516-*` resources, stop every process you started. Then stop.
