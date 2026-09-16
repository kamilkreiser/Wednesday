matches 2
=====MSG 2026-09-16T22:02:39.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 4446
Seat A

## BLUF
- #1016 KS-1072 MERGED at 21:57:19Z as squash 7e89318bcedbc9a35757d4298ace54a6a23020bd, pinned with --match-head-commit to the GO head a226d94fe8c6fbfecb81de415feb645302cdd166.
- Verified at origin: develop tip = M; one parent = eb1051fd39fe3edab4e0b1d1967515b758d4ba3f; tree e09ede17ec4e211e336de8dde18cf0f5d0bc7fb2 = the merge-tree prediction; files = the PR's 2; both blobs = your equality targets.
- KS-1072 stays In Progress (§5f). The four post-merge writes are done, each gated on the previous rc: KS-1072 facts, KS-1180 comment, KS-1199 (P-1016-3), KS-1200 (R-1016-5).

## Recommendation
No action needed. #1014's delta gate now judges against develop 7e89318bc. Next from me: stop the 84 orphan stubs per your ANSWER, file the leak ticket, then the KS-1195 shape QUESTION.

## Detail
- **Pre-step** (21:56Z): attachmentsForURL(pull/1016) = [KS-1072 contributes, In Progress]. Closing phrases 0 in the PR title, body, comments, commit messages and squash body (regex control = 2). PR head (API) = GO head.
- **Develop-moved check:** git log 523f283c6..eb1051fd3 -- routes/verification.ts = 0 commits (control, the same range on auth routes/users.ts = 1). Develop had not moved onto verification.ts.
- **Mailguard** before the merge: word-boundary STOP/HOLD/HAND OVER NOW on the Wednesday mails after the GO = CLEAR (controls: "STOP: usage" matches; "all three holds stand" does not).
- **Controls:** merge_verify with a wrong sha STOPPED at rc 13 ("head != GO sha"); the dry run passed; the real run rc 0.
- **At origin after the merge:**
  - develop tip (ls-remote) 7e89318bcedbc9a35757d4298ace54a6a23020bd == M: yes
  - parents of M: eb1051fd39fe3edab4e0b1d1967515b758d4ba3f -> OK
  - tree of M: e09ede17ec4e211e336de8dde18cf0f5d0bc7fb2 (predicted) -> OK
  - files base..M == PR files (2)
  - Blockchain/Dev/services/api-gateway/src/routes/verification.ts blob a7a6d46057a18b3460e7d08bbec5df12ab763a81 == target a7a6d4605
  - Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts blob 4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780 == target 4ad1cdcd1
  - Squash subject: "KS-1072: the latest-anchor selector breaks equal blockNumbers on the most recent confirmedAt, as its comment says (#1016)". The body says "Refs KS-1072", with no closing phrase.
- **Writes after the merge:**
  - a. KS-1072 facts comment 5b31961d-3685-49fe-a88f-17b42403ec80: the §5f line (unverified: the selector against a real anchoring service and a real Postgres anchor_store) plus R-1016-1 (offset 13), R-1016-3 (createdAt DESC matches anchoring :1491/:676), R-1016-4 and R-1016-6. Anchors 7/7.
  - b. KS-1180 comment da07a4c1-8466-43de-942a-40e6b1166023: P-1016-1 (the :124 guard is not a tier witness; GT2 5/5 green at head and base; the PR-body claim is false) and P-1016-2 (TS18046 at (124,10)), "NOT a fix round". Not built. Anchors 5/5.
  - c. KS-1199 (Backlog, Low, board account, related KS-1072): P-1016-3, no verdict pin on a status-differing tie; G-STATUS 424/424 green while 14 rows flip; the owner's JAN confirmed / JUN failed test shape and its mirror. Searched first: makeFetchDocFromAnchorStore 3/3, ks1072-the-latest-anchor-selector 120/1, P-1016-3 130/1 (my own KS-1072 comment), verified: true 107/31. None covers it.
  - d. KS-1200 (Backlog, Medium, board account, related KS-1072 + KS-960): R-1016-5, reported not reconciled, asking which schema source is authoritative.
    - Re-read at 7e89318bc: 10 CREATE TABLE anchor_store sites; 9 carry no unique (docker/init 01:188, 03:89, 06:26; azure init.sql :150/:733/:2045; migrations 001:704, 003:16; gateway startup-migrations.ts:316); the unique is at migration 031:39-40 and anchoring index.ts:209; the ensureTables early return is at :172-175.
    - My first grep used \b/\s under git grep ERE and read 0 creates; the control (anchor_store present) exposed it, and the portable pattern gave 10.
    - Searched first: (document_id, network) 118/2, ensureTables 4/3, startup-migrations.ts 88/36, R-1005-1 117/1, R-1016-5 117/1 (my own comment). None covers it.
- **§5f live-sweep list now:** KS-1165, KS-932, KS-1073, KS-844, KS-1183, KS-745, KS-999, KS-871, KS-1018, KS-1072.
- **State at 22:02:06Z:** develop 7e89318bcedbc9a35757d4298ace54a6a23020bd; #1014 head 9ba0caf78b8ddb737541df38303b776c982521d2 (unmoved, no GO). Shared .git/config sha 0c7e6ce57e16e99724706efc86201d54f531a0fe, unchanged since boot. Nothing deployed.

=====MSG 2026-09-16T22:02:07.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 4446
Seat A

## BLUF
- #1016 KS-1072 MERGED at 21:57:19Z as squash 7e89318bcedbc9a35757d4298ace54a6a23020bd, pinned with --match-head-commit to the GO head a226d94fe8c6fbfecb81de415feb645302cdd166.
- Verified at origin: develop tip = M; one parent = eb1051fd39fe3edab4e0b1d1967515b758d4ba3f; tree e09ede17ec4e211e336de8dde18cf0f5d0bc7fb2 = the merge-tree prediction; files = the PR's 2; both blobs = your equality targets.
- KS-1072 stays In Progress (§5f). The four post-merge writes are done, each gated on the previous rc: KS-1072 facts, KS-1180 comment, KS-1199 (P-1016-3), KS-1200 (R-1016-5).

## Recommendation
No action needed. #1014's delta gate now judges against develop 7e89318bc. Next from me: stop the 84 orphan stubs per your ANSWER, file the leak ticket, then the KS-1195 shape QUESTION.

## Detail
- **Pre-step** (21:56Z): attachmentsForURL(pull/1016) = [KS-1072 contributes, In Progress]. Closing phrases 0 in the PR title, body, comments, commit messages and squash body (regex control = 2). PR head (API) = GO head.
- **Develop-moved check:** git log 523f283c6..eb1051fd3 -- routes/verification.ts = 0 commits (control, the same range on auth routes/users.ts = 1). Develop had not moved onto verification.ts.
- **Mailguard** before the merge: word-boundary STOP/HOLD/HAND OVER NOW on the Wednesday mails after the GO = CLEAR (controls: "STOP: usage" matches; "all three holds stand" does not).
- **Controls:** merge_verify with a wrong sha STOPPED at rc 13 ("head != GO sha"); the dry run passed; the real run rc 0.
- **At origin after the merge:**
  - develop tip (ls-remote) 7e89318bcedbc9a35757d4298ace54a6a23020bd == M: yes
  - parents of M: eb1051fd39fe3edab4e0b1d1967515b758d4ba3f -> OK
  - tree of M: e09ede17ec4e211e336de8dde18cf0f5d0bc7fb2 (predicted) -> OK
  - files base..M == PR files (2)
  - Blockchain/Dev/services/api-gateway/src/routes/verification.ts blob a7a6d46057a18b3460e7d08bbec5df12ab763a81 == target a7a6d4605
  - Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts blob 4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780 == target 4ad1cdcd1
  - Squash subject: "KS-1072: the latest-anchor selector breaks equal blockNumbers on the most recent confirmedAt, as its comment says (#1016)". The body says "Refs KS-1072", with no closing phrase.
- **Writes after the merge:**
  - a. KS-1072 facts comment 5b31961d-3685-49fe-a88f-17b42403ec80: the §5f line (unverified: the selector against a real anchoring service and a real Postgres anchor_store) plus R-1016-1 (offset 13), R-1016-3 (createdAt DESC matches anchoring :1491/:676), R-1016-4 and R-1016-6. Anchors 7/7.
  - b. KS-1180 comment da07a4c1-8466-43de-942a-40e6b1166023: P-1016-1 (the :124 guard is not a tier witness; GT2 5/5 green at head and base; the PR-body claim is false) and P-1016-2 (TS18046 at (124,10)), "NOT a fix round". Not built. Anchors 5/5.
  - c. KS-1199 (Backlog, Low, board account, related KS-1072): P-1016-3, no verdict pin on a status-differing tie; G-STATUS 424/424 green while 14 rows flip; the owner's JAN confirmed / JUN failed test shape and its mirror. Searched first: makeFetchDocFromAnchorStore 3/3, ks1072-the-latest-anchor-selector 120/1, P-1016-3 130/1 (my own KS-1072 comment), verified: true 107/31. None covers it.
  - d. KS-1200 (Backlog, Medium, board account, related KS-1072 + KS-960): R-1016-5, reported not reconciled, asking which schema source is authoritative.
    - Re-read at 7e89318bc: 10 CREATE TABLE anchor_store sites; 9 carry no unique (docker/init 01:188, 03:89, 06:26; azure init.sql :150/:733/:2045; migrations 001:704, 003:16; gateway startup-migrations.ts:316); the unique is at migration 031:39-40 and anchoring index.ts:209; the ensureTables early return is at :172-175.
    - My first grep used \b/\s under git grep ERE and read 0 creates; the control (anchor_store present) exposed it, and the portable pattern gave 10.
    - Searched first: (document_id, network) 118/2, ensureTables 4/3, startup-migrations.ts 88/36, R-1005-1 117/1, R-1016-5 117/1 (my own comment). None covers it.
- **§5f live-sweep list now:** KS-1165, KS-932, KS-1073, KS-844, KS-1183, KS-745, KS-999, KS-871, KS-1018, KS-1072.
- **State at 22:02:06Z:** develop 7e89318bcedbc9a35757d4298ace54a6a23020bd; #1014 head 9ba0caf78b8ddb737541df38303b776c982521d2 (unmoved, no GO). Shared .git/config sha 0c7e6ce57e16e99724706efc86201d54f531a0fe, unchanged since boot. Nothing deployed.

