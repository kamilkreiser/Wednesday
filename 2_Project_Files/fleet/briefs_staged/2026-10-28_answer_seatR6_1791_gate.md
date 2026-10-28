## BLUF
#1791 (KS-1670 site 1) passed its tier-1 gate (gate 7, round 1): GO WITH NOTES, Seat R 6th. At head, none of the gate's 10 injected connectionId payloads changes the redirect's target or query; at base, 5 of 10 broke the query. Merge slot: docs section **98**, after #1787 (96) and #1789 (97). Do NOT prep yet; Wednesday mails your turn.

## One thing to add AT YOUR PREP (test-only, in the same push as the merge-in and renumber)
- **Add the non-ASCII connectionId cell KS-1670 asks for.** The PR has none; the gate covered it only on the wire (its row A10). Keep it a real behaviour cell through the callback route if your harness allows; a source-text check does not count. The gate's N6 mutant (a raw id added by string concatenation) survives your current text-check test, and a behaviour cell kills it. Name the new cell in your READY. Wednesday's completion check will read that delta as test-only.

## Notes (accepted)
- Site 1 only, as the ticket allows. Sites 2 and 3 (index.ts:869 and :1168, by the gate's citation) wait on the KS-1641 decision. That is narrowing, and the PR body should say it.
- A lone-surrogate id now throws URIError and flips a saved connection to error. Real ids are conn_ plus a uuid, so it cannot happen today. Note it in the PR body; no ticket.

## Provenance
- Verdict: 0_Brain/reference/2026-10-28_gate7-tier1/verdict.md (claude-opus-5-5; Spark shadow first). Pin: #1791 b9d91e119995, unchanged at start and end. File:line citations are the gate's; Wednesday has not re-opened them.
