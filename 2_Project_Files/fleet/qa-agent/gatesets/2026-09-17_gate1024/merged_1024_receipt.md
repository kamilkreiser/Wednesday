SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1024 KS-1202 @79933c79817ce4ef013ce885b3a32ea06419924f; follow-up KS-1213
TS: 2026-09-17T09:09:53.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
MERGED: **#1024 KS-1202 → `79933c79817ce4ef013ce885b3a32ea06419924f`** on your 09:05:48Z GO (spf/dkim/dmarc pass). Verified at origin: one parent `81ee4b729`, tree `ccd3f2819` = prediction, two files, both blob targets equal; originate jest at the merge 63 / 656, 0 failed. KS-1202 stays In Progress; facts comment `be343842-a836-4593-b018-811e2d434219`. **Follow-up filed: KS-1213** (N-A + N-B). The N-4 re-measure is on KS-1203 (comment `81a9546a-1893-473e-a227-c53a1d3770cc`). #1023's GO is next.

## Recommendation
Please queue KS-1213. I merge #1023 on your GO now (pre-step first). The freed slot goes to KS-839: develop merged in again, push, PR, READY.

## Detail
- **Pre-step** (09:06:44Z):
  - ls-remote develop `81ee4b729` (no originate change since `581c9db0d`, 0 files); pull/1024 = `d1a3280880d85ff31fd409aa1b5a16c428c4bb9a`.
  - `git merge-tree --write-tree 81ee4b729 d1a328088` = `ccd3f281977eb0ddda4af2e555c074d30fddd3db` (= GO). `documents.ts` `de9b5ae25` and the ks1202 test `ada07f053` = targets. Control: develop's `documents.ts` `c3a818ac8`.
  - linkKinds [KS-1202 contributes]. Closing-phrase scan of the title, body, 3 commits, 1 + 0 comments and my squash body: 0.
- **Merge:** REST squash with the `sha` pin, 09:06:50Z → http 200 at 09:06:54Z. Title = PR title + ` (#1024)`; body = the fix commit's message (`Refs KS-1202.`, Co-Authored-By).
- **Verified:**
  - ls-remote develop = `79933c798`; parent `81ee4b729e86…`; tree `ccd3f2819`.
  - Files vs `81ee4b729`: ks1202 test +120, `documents.ts` +12. Blobs `de9b5ae25` / `ada07f053`.
  - Message: `Refs KS-1202.`, closing hits 0.
  - Worktree detached at the merge: originate **63 suites / 656 tests, 0 failed, 0 pending**; tsc rc 0; porcelain 0.
- **KS-1202:** In Progress | last state change 2026-09-17T08:11:04.107Z Backlog -> In Progress (the merge moved nothing).
- **KS-1202 comment `be343842`:** the squash sha; create CLOSED (runtime, originate + gateway); R-1 fail-closed exact equality (case variants, non-strings, null / '' now 400); R-2 non-string top-level `type` stored and served at originate, refused at the gateway; R-3 add-in and legacy CERTIFICATE 400 UNKNOWN_DOCUMENT_TYPE at the gateway on develop = head; R-4 a documents:read-only key reaches `/version` past the gateway scope, only originate RBAC refuses; "Writers other than create are NOT closed: see KS-1213"; NOT TESTED; §5f.
- **KS-1213** (Backlog, High, board account, related KS-1202): "Derived-document writers still relabel the served type: POST /api/documents/:id/version with metadata.documentType is stored as one type and served as another (plus the create guard's regression cells)".
  - N-A: the `/version` rows measured in-process and through the gateway; the restricted `['DOCUMENT']` connector served PROPERTY_DEED; sign-cert / sign-wallet / certifications/issue + parentDocumentId read only; blast radius; the verify path not measured; both fix shapes labelled unratified (write-side refuse, or read-side serve stored, which reddens the create cells 10/656).
  - N-B: the G-CASEFOLD / G-TRIM / Q-DOCTYPEONLY 0-red tampers and the four cells.
  - KS-1203 named as related, not widened. Not built.
  - **Searched first:** `metadata.documentType` 18 (lineage / vocabulary tickets, none on served type); `/version` 18 (none on this); `untyped body` 2 (KS-1203, KS-1176); `N-4` 9 (KS-1203 is the #1014 N-4).
- **KS-1203** (Backlog, not archived) is the #1014 N-4. Comment `81a9546a` adds the #1024 gate's re-measure (B22 / B23: untyped body from a restricted connector admitted, stored and served DOCUMENT; a ['DEGREE'] connector served DOCUMENT; untouched by #1024) and names KS-1213 as related.
- **Open PRs of this lineage:** #1018, #1023 = 2.

