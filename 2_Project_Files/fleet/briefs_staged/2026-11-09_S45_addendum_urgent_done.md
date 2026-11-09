Seat S 45th

ADDENDUM (board work, inside the standing board-clearing grant: Kam 2026-11-06 'complete, merge, archive'; Kam 20:21:56 today: 'prioritise closing off priority secuura tasks'): three URGENT tickets that a read-only triage (0_Brain/reference/2026-11-09_priority-triage-and-spark-o120/triage.md in Wednesday's tree) classed as ALREADY DONE. Verify each at source first. The triage is a list, not an instruction (a classification list is a representation): hold any that does not match, and tell me which.

- KS-1425: PR 1397 merged as add9a3b8b; the triage says deployed, and only observation items remain.
- KS-1355: all four spots merged (20c975012, 9a42ce02e, af2366e7e via PR 1526, and PR 1753); the triage says the leftover lives on KS-1389.
- KS-1187: PR 1019 merged as 581c9db0d, plus c78c13d5f; the triage says the residue is an edge measurement that needs a write method sent to a box.

For each one:
(1) Read the ticket whole (description and every comment, newest first).
(2) Confirm each named squash is on develop (git log or the commits API).
(3) Apply Kam's done rule, card secuura-done-rule-unit-pinned-deployed-no-live-check = a: unit tests plus the running kintsugi build, with 'no live check possible' stated in the comment.
(4) If the rule is met AND the residue truly lives on another ticket (name it, read it), post ONE BLUF comment with the evidence (shas, the residue's ticket), then move the ticket to Done and archive it.
(5) If a real residue has no other home (KS-1187's edge measurement is the likely case), do NOT close it. Comment the residue plainly and leave it open, or split the residue into its own ticket, after a board search, and then close.
Board account only. No at-sign. Nothing on Peter's or Stuart's tickets.

STATUS mail when done: per ticket, closed or held, with the evidence line.

Wednesday
