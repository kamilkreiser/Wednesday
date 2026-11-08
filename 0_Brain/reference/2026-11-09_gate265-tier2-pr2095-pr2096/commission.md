# Gate 265, tier 2 BATCH: PR 2095 (KS-2012) and PR 2096 (KS-2016), both TEST-ONLY in Blockchain/Dev/services/api-gateway, raised by Seat T 15th from held Spark passes. Launched 2026-11-09 01:1x AEDT by the overnight Wednesday seat. Model: Sonnet (routing row G2, tier 2).

Tier reason: each PR adds cells to ONE existing api-gateway test file and changes no product byte (T 15th's diff-tree, each +12/+15 -0). Batched under Kam's 2026-09-18 minimise-gate-duplication rule: the two touch different files and share a tier. Tier 2 = through code: the cells, their red-proof, the suite; no live stack.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md (read whole; it binds tier 2 too). QA gate: findings only; fix nothing; post nothing; write only in this folder and your scratch; never cd; never delete; one clone on the boot volume (/private/tmp), report the GiB you leave (DevMASTER read 21 GiB free at 01:0x and falling).

Pins, Wednesday's `git ls-remote origin` at 01:15:40 AEDT:
- develop 092d30706b9561bb7d28aeffedf1e37ba62b4cd5 (both PRs were cut on 7eda23b34d3b; develop has moved by one squash, PR 2061, auth service only)
- PR 2095 head 90e8ee1d8f93422d9a43f2984cec0b673a3f06f1
- PR 2096 head 85785a9f3663ac2ac784ecb76cf896619e5f90e6
Re-read all three at your start and end; a moved head voids that PR's verdict.

The builder's claims (READ, then test, do not take): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatT-15th/mail/out_07_ready_ks2012_body.txt and out_08_ready_ks2016_body.txt; PR bodies pr_body_ks2012.md and pr_body_ks2016.md beside them. Tickets KS-2012 and KS-2016 (read at source, read-only).

Per PR, questions:
1. Does each new cell test what its ticket says, at the surface the READY names (PR 2095: the api-gateway approve-forward warn line logs; PR 2096: the caller's Authorization reaches the upstream on EVERY page of the audit export)? Read the ticket's own words against the cell.
2. RED-FIRST: plant the defect the cell exists for in the product file (never committed), show the new cell alone goes red by assertion and the rest stay green, then restore byte-equal (sha256). A cell that stays green under its own defect is a blocker. Prefer a plant that is NOT the builder's: an independent mutant (e.g. drop the header on page 2 only; log the line at the wrong level).
3. The whole api-gateway suite with and without each PR on the current develop, same instrument both sides: counts and failed-name lists. T 15th's figure: 1869 unpatched, 1870 with each.
4. Merge-tree of each head onto 092d30706b95: rc and tree; shared paths with PR 2061 (expect none).
5. Anything in the cell that would pass for the wrong reason (a mock that answers regardless, an assertion on a constant).

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate265-tier2-pr2095-pr2096/verdict.md. Line 1: "PR 2095: GO | GO WITH NOTES | NO GO; PR 2096: GO | GO WITH NOTES | NO GO". Then BLUF, findings per PR (severity, file:line, FOUND / TESTED / HOW), a NOT TESTED list, NEEDS TIER 1 if you think either needs it, your own conduct, GiB left. Final message: line 1 plus one line per finding.
