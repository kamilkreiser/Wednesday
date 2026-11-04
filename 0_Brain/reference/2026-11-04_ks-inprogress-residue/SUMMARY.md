# KS In Progress residue census, 2026-11-04 (read-only)

## BLUF
238 KS tickets in "In Progress" fetched (Wednesday's board_count: 238, exact match). Primary class by newest comment:

| Class | n |
|---|---|
| SCOPE-REMAINS (merged fix covers part; items/halves not built) | 95 |
| KAM-DECISION (ruling/decision/evidence awaits Kam) | 30 |
| NEEDS-DISPOSABLE-STACK ("Not run on kintsugi": induced failure, logins, connector key, issuer, custody transfer) | 27 |
| OPEN-PR (PR up / gate round / migration clash) | 25 |
| LIVE-CHECK-OWED (live sweep/re-probe owed after deploy) | 18 |
| FINDING-FILED (comment is a datum/census, no closure path stated) | 17 |
| NO-COMMENT | 10 |
| NOT-DEPLOYED (merged, nothing deployed) | 5 |
| CANNOT-RUN-SAFELY | 5 |
| OBS-PARTIAL | 3 |
| HUMAN-OWNED (Stuart assignee; Peter closed PR 1440) | 3 |
| Total | 238 |

Next closable classes for a Claude seat:
1. **LIVE-CHECK-OWED (18) + NOT-DEPLOYED (5)**: need only a deploy-SHA read plus the named live probe on kintsugi/demo. Evidence: the deployed REVISION head vs the merge SHA, and the probe output (route, status, body) pasted on the ticket.
2. **NEEDS-DISPOSABLE-STACK (27)**: 12 are "needs an induced failure", others need a test login/connector key. One disposable stack with seeded logins, a connector key, and a fault-injection switch would unlock the whole class. Evidence: observed failure behaviour on that stack with the stack's id/SHA.
3. **OPEN-PR (25)**: close by gate GO plus merge, then deploy-check. Evidence: gate report and merge SHA.
Avoid for now: SCOPE-REMAINS (95; needs building, or a Kam ruling that the remainder splits to new tickets), KAM-DECISION (30), CANNOT-RUN-SAFELY (5; needs 0-row vc_credentials_store populated or demo-seed gate closed).

## FOUND / TESTED / HOW
- HOW: GraphQL (read only) `issues(filter team KS, state name "In Progress")`, first:25 pages (100 hit complexity limits in design; 25 used), comments(first:50) per issue, sorted client-side by createdAt, never last:N. KS-1868 had >50 comments; paginated to 83. Classification is a keyword/regex rule on the first ~900 chars of the newest comment (board account's BLUF/"Left open" line), in priority order, plus 14 hand overrides for comments with no BLUF line.
- FOUND: 195 assigned to the board account (kamil.kreiser@secuura.ai), 42 unassigned, 1 to Stuart. 51 tickets have a newest comment dated 11-04, 68 dated 11-03, 35 dated 11-02; 10 have no comment. Per-ticket class, date, 150-char quote and PR attachment count are in residue.tsv.
- Control (a): re-read raw JSON for KS-1673 (class NEEDS-DISPOSABLE-STACK, "needs two organisations' logins and Entra", 11-04), KS-1250 (SCOPE-REMAINS, "only the gateway half is done", 11-03), KS-1346 (FINDING-FILED, "Facts only... N-1432-2", 10-09). All three match.
- Control (b): the API returns comments newest-first (first element dated 2026-11-04T02:32 for KS-1673; oldest last); client-side max(createdAt) equals that first element for all three. Sort is consistent.
- NOT tested: classes are keyword inferences, not a human reading of all 238; boundaries between SCOPE-REMAINS and LIVE-CHECK-OWED are fuzzy where one comment lists both (the rule picks the earlier-listed class). Expect roughly 10-15% misfiles. I did not verify that any claimed deploy SHA is current, and did not check Linear state of PRs.

## Surprises
- Count matched 238 exactly.
- Only 3 HUMAN-OWNED: the "Stuart's/Peter's" blocker is rare in this state set.
- Comments are mostly authored by the board account regardless of which seat wrote them, so authorship cannot split seat work.
- 10 tickets have no comment at all, so they were not among the 328 worked.
