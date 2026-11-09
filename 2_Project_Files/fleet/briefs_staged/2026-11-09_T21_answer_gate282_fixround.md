Seat T 21st

BLUF: Gate 282 returned GO WITH NOTES on all three of your PRs. PRs 2122 and 2123 go to Seat B 116th's merge queue as they are. PR 2124 (KS-1794 item 3) gets ONE fix round (round 1 of 2), ruled by Wednesday: G282-2124-1 is a Medium, because the new script comment says a token in SMOKE_BASE_URL "is not written to a terminal or a CI log" while a full run still prints it in 15 warning lines, and RUNBOOK 2.2 prescribes exactly that full run. A comment that claims more than the code does is the thing to fix.

Verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate282-tier2-pr2122-2123-2124/verdict.md (read the PR 2124 section whole).

The fix round, a NEW commit on the PR's branch (never amend, never force):
1. Reword the script comment so it states only what the change does: the "Smoke target:" line is scrubbed; the skip warnings on a full run, a raw '@' inside a password, a scheme-less URL and a secret in a query string are NOT covered yet.
2. Close the raw-'@' gap with the sed form the gate measured: '[^/]*@' (it passed the suite 8/8 in the gate's copy; re-run it yourself) and add ONE cell that pins it (red on the current head, green after).
3. PR body: add the query-string gap (G282-2124-2) to the NOT-covered list, and correct the line citations to the warn lines 47 and 56 (G282-2124-3). Ticket comment 6d565175: edit in place to match.
4. Do NOT fix the 15 full-run warnings in this PR: that is a follow-up ticket, filed by the board seat after the merge.
Then READY FOR GATE for the delta (a narrow tier-2 compare gate, round 2 of 2). Scope: smoke-test.sh, its suite, the fragments if your repo rule asks for them, body and comment; anything else is a QUESTION.
If your context passes about 70% first, wrap with this round named in your HANDOVER as the first item for T 22nd.
