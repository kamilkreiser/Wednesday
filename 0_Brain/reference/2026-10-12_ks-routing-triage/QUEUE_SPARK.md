# QUEUE_SPARK (top 25 of 3; ranked HIGH confidence first, then priority, then most recently touched)

- **KS-638** [Backlog, p2, kamil.kreiser@secuura.ai, SPARK/LOW] The extranet test board has never shown a green run — 0 passed in 22, and the latest red is E2E 210/0 with Schemathesis producing no results
  - why: names file:line and an action; no open PR
  - quote: "**The team's own status board has never once been green.** The extranet Testing tab has recorded **22 Platform K runs since 2026-05-25: 17** `failed`**, 5** `error`**, 0** `passed`**.** Not one."
  - area: schemathesis/systemTest
- **KS-678** [Backlog, p2, kamil.kreiser@secuura.ai, SPARK/LOW] #568 publishes 17 URLs on secuura.io — an unresolving, seemingly unowned domain (KS-669 class; no guard rule covers URLs)
  - why: names file:line and an action; no open PR
  - quote: "Filed separately from KS-669 rather than as a comment on it, deliberately: KS-669 is In Progress with its own scope (17 of its 18 URLs are still open work) and its operative defect is that it is **una"
  - area: Blockchain/Dev/docs
- **KS-1409** [Backlog, p3, kamil.kreiser@secuura.ai, SPARK/LOW] webhooks routes reject connector principals (userId connector:<id>) - 500 after KS 1345, silent 200 before
  - why: names file:line and an action; no open PR
  - quote: "A 500 for a principal-class condition is arguably a mis-mapping. It could reasonably be a 4xx, or the list could be keyed on the organisation rather than the user. That decision is the owner's and was"
  - area: services/jwt
