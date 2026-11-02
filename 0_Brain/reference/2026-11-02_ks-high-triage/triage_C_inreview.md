# KS In Review triage, part C (34 tickets), 2026-11-02

Evidence: Linear description + newest comments, GitHub REST PR state (read-only), git ancestry vs kintsugi deploy head b1fb543640e7 in repo_b1 (origin/develop fetched). Every merged PR linked to these 34 is an ancestor of b1fb543640e7 (deployed y); the only unmerged PRs are #887 and #1360. DONE rows marked "live check owed" are code-complete; the author left the ticket open for a post-deploy probe, which is the only gap. Bucket DONE-NOT-DEPLOYED is empty.

| key | priority | bucket | evidence | next action |
|---|---|---|---|---|
| KS-1000 | High | WRONG-STATE | #1506 merged f6f2a539, #1499 merged 6b978ca3, #1480 merged 8cfab55b, #874 merged bc067e3e; deployed y; newest comment 2026-09-14; Items 1,2,4 merged (#1480,#1499,#1506); item 3 sibling-service sweep + CI wiring not done; #874 link is stale (KS-933 duplicate) | Move to In Progress (or Todo); drop the #874 link |
| KS-1380 | High | PR-OPEN | #1360 open, #1358 merged a5ab2ca9; deployed y; newest comment 2026-09-30; #1358 (fix) merged by mistake 09-30 and deployed; Peter opened revert #1360 (OPEN, waiting on Peter); ticket reopens develop-build defect | Peter merges #1360 or Kam decides keep #1358; then re-do fix; ticket stays open meanwhile |
| KS-229 | High | WRONG-STATE | #785 merged 89632852; deployed y; newest comment 2026-09-02; Tracker: Urgent+High dispositioned 09-02, Medium/Low sections not; #785 is a docs fix only | Move to In Progress (tracker stays open); do Medium/Low disposition pass |
| KS-577 | High | NEEDS-CLIENT | #880 merged 7d7f6bd5, #854 merged 50913d2c; deployed y; newest comment 2026-09-02; #880 revoke-on-rotate merged 09-14, cutover window a single value; ticket says window is a Stuart contract question, PS-463 must land first; no comment since 09-02 | Stuart (S side) to agree the cutover window value; Peter re PS-463 |
| KS-663 | High | WRONG-STATE | #808 merged d2fe7d6d; deployed y; newest comment 2026-09-04; #808 merged divergence 2 (CI check wired); divergence 1 (verify-file spec) deliberately out, tracked as KS-791 | Move to In Progress, or Done if Kam accepts the KS-791 split |
| KS-968 | High | DONE | #1800 merged 92a02a35, #1485 merged 8f674b3c, #905 merged ede711ca; deployed y; newest comment 2026-09-07; #1485 email-row rewrite fix, #905 column warn, #1800 integration guard; MAJOR fixed | Move to Done |
| KS-1018 | Medium | DONE | #1473 merged 8dcbddb5, #1015 merged eb1051fd; deployed y; newest comment 2026-09-16; #1015 three reads rethrow infra errors; #1473 item 3 fallback; 09-16 comment was a measurement, now acted on | Move to Done |
| KS-1114 | Medium | DONE | #1579 merged 385fc288, #1576 merged d900972f, #1555 merged 833984fc; deployed y; newest comment 2026-10-15; #1555 merged after round-1 NO GO; #1576, #1579 follow-ups landed | Move to Done |
| KS-1186 | Medium | DONE | #1750 merged c7ad5ab5, #1477 merged 6fa9bf7b; deployed y; newest comment 2026-10-12; #1477 five reads await fromRow; #1750 comment cleanup; live check owed (deployed y) | Move to Done |
| KS-1188 | Medium | DONE | #1826 merged 5d9e59b2, #1479 merged 5bfa5a80, #1178 merged a5ead4d8, #1163 merged 5548d26a; deployed y; newest comment 2026-10-12; F1a/F1b/F2 #1163, MFA siblings #1178, F3 #1479, #1826 pin; author wanted post-deploy probe | Move to Done (optionally probe wording first) |
| KS-1232 | Medium | DONE | #1842 merged 0fab207f, #1517 merged f39104e7, #1120 merged e2d0672a, #1106 merged 0e15cf80; deployed y; newest comment 2026-10-12; #1517 non-array allow-list -> 403; pins #1106/#1120/#1842; live check owed (deployed y) | Move to Done |
| KS-1328 | Medium | DONE | #1524 merged 81ac1ea6, #1508 merged c63cec1f, #1430 merged 4aa5cb38; deployed y; newest comment 2026-10-12; #1430 and #1508 give all 17 retry suites 60s budget; test-only | Move to Done |
| KS-1394 | Medium | DONE | #1781 merged f23097c3; deployed y; newest comment 2026-10-28; #1781 now merged (comment 10-28 said unmerged, stale); prints per-lock docker command | Move to Done |
| KS-1490 | Medium | WRONG-STATE | #1580 merged b5742c3e, #1573 merged 8a997051; deployed y; newest comment 2026-10-18; #1573 closes ONE of two halves (trailing slash); #1580 banner; author: other half still open | Move to In Progress; name the remaining half or split it |
| KS-1510 | Medium | DONE | #1754 merged d5432036, #1512 merged 629349da; deployed y; newest comment 2026-10-12; #1512 logs thrown error, status unchanged; #1754 pin; live check owed per author (deployed y since) | Move to Done |
| KS-1512 | Medium | DONE | #1746 merged a7d0e1fb, #1522 merged b08ee629; deployed y; newest comment 2026-10-12; #1522 audit-log reads platform half past upstream; #1746 pins; 10-12 comment only corrects squash text | Move to Done |
| KS-1540 | Medium | DONE | #1594 merged 7b6d479a, #1586 merged 83ed01af, #1582 merged 5d1be7b0; deployed y; newest comment 2026-10-18; #1582 503 when Redis unavailable, real-redis pins #1586/#1594; author kept open for deploy, now deployed | Move to Done |
| KS-1545 | Medium | NEEDS-KAM | #1629 merged 88b8ceb9, #1572 merged 1f73d7ac; deployed y; newest comment 2026-10-18; Step 1 merged (#1572, thrown errors only); author says Step 2 needs Kam ruling; #1629 is KS-1622 follow-up | Kam rules step 2; then close or split step 2 to new ticket |
| KS-1553 | Medium | DONE | #1705 merged 1f2ec373, #1533 merged 7550a969; deployed y; newest comment 2026-10-13; Stuart 10-13: S never sends organizationId, uuid enforcement safe for S; (a) landed #1533, #1705 pins | Move to Done |
| KS-1564 | Medium | DONE | #1734 merged bc958363, #1537 merged a7cffc8d; deployed y; newest comment none; #1537 lists/mints from auth claim; #1734 guard on AST; ticket itself never claimed browser check | Move to Done |
| KS-1633 | Medium | DONE | #1822 merged 530f0911, #1623 merged adb0dfd5; deployed y; newest comment 2026-10-19; Reservation-before-anchor merged; responses byte-identical per gate; live check on kintsugi still owed per author | Move to Done after one live probe (or accept deployed y) |
| KS-1638 | Medium | DONE | #1733 merged d766f6df, #1606 merged ce986062; deployed y; newest comment 2026-10-19; Proved on a real push (shell suites 91/0 after, 90/1 before); tooling-only | Move to Done |
| KS-1694 | Medium | WRONG-STATE | #1662 merged 7e3b9362; deployed y; newest comment none; Linked #1662 is KS-1682 fail-closed warnings, unrelated; description says "Nothing built here"; 0 comments | Move to Todo (or Backlog); drop the #1662 link |
| KS-657 | Medium | NEEDS-KAM | #720 merged 0e78c727, #717 merged 74a330fc, #714 merged 1f54bafb; deployed y; newest comment 2026-08-17; Build half done (#717, #714 backlog); acceptance 2 reserved: retire vs wire up dead services/shared src/ half (connection-pool); nobody imports it | Kam decides retire or wire up; then build/close |
| KS-759 | Medium | DONE | #1596 merged b8168a87, #1543 merged 49a41f3c; deployed y; newest comment none; #1543 reads tenantId/organizationId without casts; #1596 pins GDPR erasure routes; no comments | Move to Done |
| KS-839 | Medium | DONE | #1778 merged d4fc0b8f, #1464 merged f9c7880f, #1026 merged 75ad0e55; deployed y; newest comment 2026-10-12; Code half #1026 deployed; contract half (the missing piece 10-12) now landed via #1464 and #1778 | Move to Done |
| KS-880 | Medium | DONE | #1511 merged 92f68da9, #1133 merged 27ddff8f, #1124 merged af058733, #1110 merged d0ab5d00; deployed y; newest comment 2026-10-12; #1511 single home for row mappers, dead copy removed; #1110/#1124/#1133 pins; author: acceptance as written met, live check owed | Move to Done |
| KS-946 | Medium | DONE | #884 merged db94e9fc; deployed y; newest comment 2026-09-06; #884 normalises repeated slashes once at gateway edge; negative control run 09-06 | Move to Done |
| KS-961 | Medium | PR-OPEN | #887 open; deployed n/a; newest comment 2026-09-08; #887 OPEN (head 05a6cce0989a), reviewer 09-08 holding approval on one small change; no reply since | Kam/Peter: fix the one change or close #887; needs gate then merge |
| KS-969 | Medium | WRONG-STATE | #989 merged a9ce2cff, #892 merged 512480ef; deployed y; newest comment 2026-09-07; #892 is "item 1" only (pre-suite actor provisioning); other items of the systemTest actor/credential path unevidenced | Move to In Progress; list remaining items or close if none |
| KS-1113 | Low | DONE | #1789 merged 56062b37; deployed y; newest comment 2026-10-28; #1789 corrects cell 15.2.5 end to end (comment 10-28 said unmerged, stale); e2e test only | Move to Done |
| KS-1471 | Low | DONE | #1598 merged 0e2bb271; deployed y; newest comment none; #1598 logs full mounted path; no comments; Low | Move to Done |
| KS-1541 | Low | DONE | #1591 merged 8a093d1d, #1566 merged f998e343; deployed y; newest comment 2026-10-18; #1566 get_info names the gateway refusal; gate LOW/NOTEs filed as KS-1620; author kept In Progress only for deploy, now deployed | Move to Done |
| KS-1767 | Low | DONE | #1769 merged 8894c748; deployed y; newest comment 2026-10-27; Change is a types fix; merged, nothing residual | Move to Done |

## Counts
- DONE: 23
- NEEDS-CLIENT: 1
- NEEDS-KAM: 2
- PR-OPEN: 2
- WRONG-STATE: 6
- DONE-NOT-DEPLOYED: 0
- total: 34
