SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1013 KS-999 @e0f41a8fafd64fa31524390cfeab320e822f3d15
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TIMESTAMP: 2026-09-16T19:40:13.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
- #1013 KS-999 MERGED at 19:35:44Z as squash e0f41a8fafd64fa31524390cfeab320e822f3d15, pinned with --match-head-commit to the GO head 5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2.
- Verified at origin:
  - develop tip = M (ls-remote);
  - one parent = 79432c797cfb6e647acdd8798dace000a0b35d75;
  - tree 2475a6ff3f3a394b29a5ae5cf6fc9e170416d0dc = my merge-tree prediction;
  - files base..M = the PR's 3 files;
  - all three blobs equal your equality targets.
- KS-999 stays In Progress (§5f). Facts comment 33ca4470-f1b4-4c60-864f-d76d219459ba.
- KS-1186 comment 55453e46-2285-4ca5-9281-fcff9f10a10c.
- New ticket KS-1188: Backlog, Medium, board account, related KS-999 and KS-1186, not built.

## Recommendation
No reply needed. Next, per your ANSWER:
1. The vault commit, with the per-file client grep.
2. The R-3/R-5 ticket.
3. KS-1176.
#1011 round 2 stays held at 6dc825644 until its signed GO or NO GO.

## Detail
Pre-steps, 19:34:37Z to 19:35:40Z:
- Mail guard: 0 STOP/HOLD leading tokens in Wednesday mail newer than the GO. The word-boundary regex was controlled both ways: "HOLD:" matches, and "holds" in an ANSWER subject does not.
- attachmentsForURL(pull/1013) = exactly KS-999 contributes.
- 0 closing phrases in the PR title, body, comments, commit messages and squash body. Regex control finds 2 of 2.
- Head re-read in the same action: API and ls-remote both 5fbfb66a9. develop = 79432c797, equal to the expected base.
- Wrong-sha control: a zero sha stopped with rc 13 before any merge call. A dry run then passed.
- Ruleset: pull_request required approvals still 0 (read at ~19:32Z).

Merge:
- gh pr merge 1013 --squash --match-head-commit 5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2: rc 0, state MERGED, mergedAt 19:35:44Z.
- Squash subject: the PR title + " (#1013)". The body says "Part of KS-999, which stays open for the live sweep", names KS-1186 for the siblings, and ends with the Co-Authored-By line.

Blob equalities (M vs your targets):
- services/auth/src/repositories/userRepo.ts 9060b308e = 9060b308e
- services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts 4f03e6f4f = 4f03e6f4f
- services/auth/src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts 04ce4e156 = 04ce4e156

Board writes, each gated on the previous step's rc and read back:
a. KS-999 facts comment 33ca4470-f1b4-4c60-864f-d76d219459ba at 19:37:03Z, anchors 9/9.
   - The §5f line: "Merged e0f41a8fafd64fa31524390cfeab320e822f3d15; offline gates green; NOT Done per secuura-test-discipline §5f — live sweep owed (torn-down rebuilt stack, all containers verified up), unverified: a real Postgres / real DEK store and the auth service behind nginx".
   - Records R1, R2, R5, R7 and R8. R8 is written without the npm-scope at-sign ("the Node type definitions").
   - KS-999 reads In Progress after the comment; pull/1013 = KS-999 contributes/merged.
b. KS-1186 comment 55453e46-2285-4ca5-9281-fcff9f10a10c at 19:37:33Z, anchors 9/9.
   - R3: mfa/disable raw 500 at base and head; the five sites.
   - R4: listUsersInner :1040 has no try; GET /api/users 500 under both faults. A separate KS-253 gap, recorded, not ticketed.
   - I re-measured the line numbers at e0f41a8fa rather than copying them:
     - :446 getUserByIdWithPasswordHash (try :441)
     - :512 getUserByIdPreAuth (try :510)
     - :585 and :594 getUserByEmail (try :576)
     - :627 getUserBySocialId (try :622)
     - the only awaited site is :410
     - :1040 has no try in the 30 lines above
     Regex control 1/1.
c. KS-1188 "#1013 gate findings (KS-999): the getUserById route-level 503 and its log line are unpinned; a burnt backup code is told to retry".
   - Backlog, Medium, board account, related KS-999 and KS-1186. Anchors 9/9, 0 at-signs, 0 comments.
   - Carries F1 Minor, F2 Polish and F3 Minor.
   - F3 is described with no fix. It notes that the 503 the user sees comes from getUserById's classifier during the read-back ("please retry"), not from updateUserOrThrow's own hedged message ("if you already succeeded, you may not need to"; doc comment userRepo.ts:955-958). The burn is at passwordLoginGate.ts:267.
   - Searches, quoted in the ticket (searchIssues with includeArchived + includeComments, literal-match filter):
     - getUserById: 21 fuzzy / 21 literal
     - SERVICE_UNAVAILABLE: 114 / 16
     - backup-code: 94 / 13
     - userRepo.ts: 98 / 54
     None already covers F1–F3. KS-1052 and KS-253 are named, not related, because both are archived.

The §5f live-sweep list for Sunday is now: KS-1165, KS-932, KS-1073, KS-844, KS-1183, KS-745, KS-999.

Nothing deployed. No stack. Nothing to Peter or Stuart. KS-1187 untouched.
Records: 5_Project_History/2026-09-17_seatA-2nd/ (merges/, tickets/, mail/).
