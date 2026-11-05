# KS lane plan — 2026-11-05 (read-only census, Sonnet drafter; saved by Wednesday from the drafter's report)

Kam 2026-11-05 15:42:14, verbatim: "good work on the above. what about secuura tickets.  I would like you to get through all the in progress and all in review tickets"

## BLUF
- **In Progress = 198 exact** (8 pages, hasNextPage false) = 205 at the 13:25 census minus the 7 keys moved to Done since (KS-1401, 1823, 1584, 1612, 1860, 1230, 1990).
- **In Review = 24 exact** (1 page).
- **22 build lanes** (`lanes.md`): 21 file-disjoint lanes + lane X (serial: tickets that span services). All 91 SCOPE-REMAINS tickets are placed. Routing: 28 Spark, 52 Sonnet, 11 Opus.
- **17 Kam-decision tickets, 14 cards drafted** (`kam_decisions.md`). No card for: KS-1336 (ruled 11-02), KS-771 (tracker), KS-1084 (a local-stack measurement, not a decision). Prior ruled cards are named per ticket for KS-692, 843, 1084, 1336, 1493, 1534, 1933.
- **31 human-owned** (`human_owned.md`; Peter/Stuart creator or assignee; KS-1098 is Peter's too).

### In Progress by class (sums to 198)
| Class | n |
|---|---|
| SCOPE-REMAINS | 91 |
| HUMAN-OWNED | 31 |
| KAM-DECISION | 17 |
| OPEN-PR (incl. KS-911/912, Seat K 15th) | 13 |
| FINDING-FILED | 12 |
| NO-COMMENT | 8 |
| LIVE-CHECK-OWED | 8 |
| NEEDS-DISPOSABLE-STACK | 3 |
| DEPLOYED-NOW-CLOSE-CANDIDATE (KS-1335, KS-1031) | 2 |
| CANNOT-RUN-SAFELY | 1 |
| OBS-PARTIAL | 1 |
| NOT-DEPLOYED | 1 |
| live-seat keys the census excluded (no class) | 10 |

### In Review by class (24, `inreview.tsv`)
GATE-OWED 1 (KS-961, PR 887 unmerged, READY for QA since 09-13) · MERGE-READY 0 · HUMAN-REVIEW 4 (KS-1380, 1355, 693, 577) · STALE-STATE 0 · OTHER 19. The 19 are mostly merged + deployed with a "Left open" tail: 7 owe a write-type live check, 3 need a disposable stack, KS-1188 owes only a read-only box check, KS-1553/1533/1508/1194 have scope remaining, KS-1545/968/657 need a Kam ruling, KS-946 needs a second security read, KS-1594 has no status since 10-13. Most should move back to In Progress with the owed step named.

## FOUND / TESTED / HOW
- HOW: Linear GraphQL read-only (python3 -I, key in-process, never printed), first:25 pages until hasNextPage false, comments sorted by createdAt (KS-1868 re-paged to 84). In Review PR ancestry by git subject `(#N)` against 07a2d62be6a0. Prior rulings searched read-only in decisions.json.
- TESTED (controls): direct issue read of KS-961 = In Review, newest comment 2026-09-13 (matches); KS-1717 In Review; KS-911/912 In Progress; negative control KS-1401 and KS-1990 read Done and are in neither set; class counts sum to 198 and 24; the 91 scope keys equal the 91 lane-table keys in both directions; no Peter/Stuart creator or assignee among the 91.

## NOT VERIFIED (read before briefing)
- In Review PR merge state from the local checkout only (no GitHub): 13 PR links unresolved (no `(#N)`); PRs 1794, 1547, 1629 and the KS-1380 revert (PR 1360) open/closed unconfirmed; KS-961 judged unmerged from one empty grep with no control.
- Lane file lists are inferred from path strings in each ticket, not from diffs (disjointness is a string check). Build summaries come from the first ~420 chars of each "Left open" paragraph. Re-read KS-908, 1676, 1804, 1497, 1558, 1407, 758 before briefing.
- The 10 census-excluded live-seat keys and KS-911/912 were not re-read; the 13-vs-10+2 exclusion count was not reconciled.
- Decision recommendations are from ticket text only; KS-1156's refresh-token lifetime on the boxes is unmeasured.
- No box was contacted: nothing here is a statement about live behaviour.
