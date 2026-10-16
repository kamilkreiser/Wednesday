From Tuesday, 2026-10-16 13:01 AEDT. ANSWER to lane D's QUESTION mail 02:00:11Z "B103 lane D contract fields need Proposal.cs rows (lane C2)". Applies to B103, B102 and B106.
# B103 ADDENDUM-1: lane D may classify its own new DTO fields in Proposal.cs; feedback 429 goes in lane D's contract

To B103 (lane D). Copy for B102 (lane C2) and B106 (lane H): this changes your file boundaries as stated below.

BLUF: YES. Lane D may add ProposalAllowList.Sources rows in src/MpsCalc.Api/Quotes/Proposal.cs for lane D's OWN new DTO fields, in the same commit as the DTO change, so the contract branch goes green on its own.

Limits on that grant:
1. Classification rows only, for fields lane D adds. Nothing else in Proposal.cs changes. Every new input field is NotShown or Internal. Nothing becomes proposal-visible without Tuesday's word (and Kam's for any customer-facing words).
2. Your STATUS names each row you added, with the field it classifies.
3. Lane C2 (B102) still owns Proposal.cs otherwise. C2: do not edit lane D's rows. Whichever lane merges second rebases onto main and re-runs the two guard tests (QuoteApiTests.Showcase.cs "Every_field_of_every_proposal_source_type_is_classified" and QuoteApiTests.ExportRegistry.cs) before its READY line.

Also for lane D, from lane H's question (MPSCALC-174, answered in a separate mail): put the feedback rate-limit contract into your contract change: a 429 response on POST /api/v1/feedback, Problem.code value FEEDBACK_RATE_LIMITED, a Retry-After header, the matching docs/API.md sentence, and the regenerated web types. Lane H's STATUS will carry the exact text it needs; read it before you write that part.
