# CAPTURE — gate21T2d READY mails, VERBATIM by message id (captured 2026-09-25T09:24:18Z by capture_mail_gate21T2d.py; instrument: `inbox_digest.sh full wednesday-agent@agentmail.to <id>`)

Two READYs from ONE seat (Seat B 26th, pane Secuura/Blockchain, record 5_Project_History/2026-09-25_seatB-26th/). PR #1241 is KS-1226 (item 2 only). PR #1242 is KS-980.

## Seat B 26th READY FOR QA 2 — #1241 KS-1226 item 2 (07:42:29Z)
MESSAGE_ID <010001a0d78409d5-38b1a5db-bb92-418e-948f-80ca7b5d4596-000000@email.amazonses.com>
TEXT_SHA256 7f5dbaae8379d7f09a9416ec743d307e77e428ddf1595d762031d5badf8ffb20
#1241 head e2d0518df40228f0a183bc4223c7a6840821253e

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T07:42:29.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA 2 (Seat B 26th): #1241 KS-1226 item 2 head e2d0518df402, TIER 2
---
READY FOR QA — the five artefacts.

1. PR: #1241  https://github.com/Secuura/Distributed_Secuura/pull/1241
2. HEAD at origin, ls-remote read in the same action as writing this line: e2d0518df40228f0a183bc4223c7a6840821253e
3. TICKET COMMENT naming the PR: posted on KS-1226.
4. TEST EVIDENCE (in the PR body, written by me who ran it):
   RED PROOF, two steps: cells alone at the tip -> 2 failed / 6 passed (8); R1 and R2 fail BY
   ASSERTION with "expected null to deeply equal { passed: 243, failed: 1 }" -- the null IS the
   defect. Both hunks -> 8/8.
   Whole package BOTH SIDES, measured not inferred: base 1085/1085 (63 files) -> head 1090/1090
   (63 files), delta +5 = the five cells. Base taken by restoring the file's base content in place;
   restore verified byte-identical by blob hash d9f45be175d2 before committing.
   Capture groups asserted at BUILD time: the patch builder compiles both bodies and refuses unless
   the new one has exactly 3 groups with passed at group 2.
5. NOT COVERED: no platform preflight ran (zero Blockchain/Dev files -> the hook's documented early
   return; only the KS-989 format gate, 1 package checked / 0 skipped / 0 failed -- a 9-second push,
   NOT offered as preflight evidence). No live child vitest emitting a real skipped segment. `todo`
   and other segments still return null -- only `skipped` was specified.

The local model's three round-1 failures are each GUARDED, not merely avoided:
 (1) the '-' line is asserted equal to the file's :99 before the patch is built;
 (2) the skipped segment is non-capturing and the group count is asserted == 3 with passed at 2;
 (3) both hunk headers are computed from len() of the emitted line lists, never typed.

Item 1 (the 15 s budget at :127, F4) is a DECISION and stays out, as you scoped it. KS-1226 therefore
does not close on this PR, and the ticket comment says so.

— Seat B 26th

## Seat B 26th READY FOR QA 3 — #1242 KS-980 (08:03:01Z)
MESSAGE_ID <010001a0d796d5e3-944c6737-2294-4d1d-9b04-cfb4af1b0580-000000@email.amazonses.com>
TEXT_SHA256 8527868d2e7f656c7fe243a384b80104e488444d1c1be32d2c47fa92931aa783
#1242 head a35569aa020e63b2660b60e48b4f0286c46b27fc

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T08:03:01.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA 3 (Seat B 26th): #1242 KS-980 head a35569aa020e, TIER 2 — shape (1), Q3(a) conditions discharged
---
READY FOR QA — the five artefacts.

1. PR: #1242  https://github.com/Secuura/Distributed_Secuura/pull/1242
2. HEAD at origin, ls-remote in the same action as writing this line: a35569aa020e63b2660b60e48b4f0286c46b27fc
3. TICKET COMMENT naming the PR: posted on KS-980.
4. TEST EVIDENCE (PR body, written by me who ran it):
   head 6/6 on the file; FULL originate integration 14/14 (2 suites).
   RED PROOF, three arms, each naming WHY:
     A,B  the ticket's own tamper (predicate removed from BOTH organizations subqueries, 2/2
          asserted before applying) -> the P1 and P2 cells each FAIL; restore byte-identical.
     C    the fix reverted -> D1 and D2 FAIL (rolbypassrls false vs TRUE; GUC stripped, 0 rows
          vs 1) WHILE THE ORIGINAL FOUR STAY GREEN. That is the ticket's claim demonstrated.
   DB-gate refuses loudly (non-zero, named) when the app DSN is absent -- it does not skip.
   Preflight at this head: PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
   pre_push_hook_base.test.sh 28 passed / 0 failed; ^FIXTURE BUILD FAILED count 0. No STOP.
5. NOT COVERED: legs 3/4/8 (no stack, no such surface); no shared dev stack and no deployed DB;
   TEST_APP_DATABASE_URL exercised only in its COMPOSED form (the explicit branch is one `if`,
   not separately executed); NO CI wiring -- nothing runs this integration config automatically,
   so the cells protect the property only when someone runs test:integration with both DSNs.

SHAPE: (1), and the fallback to (2) was NOT reached -- the no-new-role/grant/migration condition
holds and I re-verified it on the live instance rather than inheriting it.

Q3(a) CONDITIONS, each discharged:
 1. ONE container, s-b26-pg-ks980, postgres:15-alpine (the version compose pins, no :latest),
    127.0.0.1:55432 only. Port proven FREE first: 55432 -> 0 listeners; control 5432 -> 3
    listeners, so the check discriminates. docker ps showed ZERO containers, so no gate stack
    and no secuura-sN-* port was at risk.
 2. Built from docker/init + scripts/run-migrations.sh. applied=49 failed=0, and the
    _secuura_migrations tracker independently reads 49 -- I did not take the runner's own summary
    as the measurement. APP_DB_PASSWORD was generated (token_urlsafe), 0600, OUTSIDE the repo,
    and is NOT the compose default (asserted). Diff contains 0 occurrences of either.
 3. Anonymous volume, no reuse. Torn down with docker rm -f. START 2026-09-25T07:43:11Z,
    STOP 2026-09-25T08:01:56Z. docker ps -a no longer lists it (count 0); no other container
    touched (there were none, and there still are none); port 55432 released (0 listeners).
    No docker compose up/down, no prune.
 4. The three arms as written, and (iii) -- arm C -- is the one that closes the ticket. Said so
    in the PR body and the ticket comment.

TWO THINGS I GOT WRONG AND FIXED, reported because you would rather know:
 - I restored a tampered file with `git checkout --`, which ALSO reverted my own UNCOMMITTED
   edit. I had saved a hash, not a copy. Rebuilt it, saved a copy outside the repo, and
   committed BEFORE red-proving. The rebuild was lucky: it exposed that D2 opened its own
   client instead of going through writerOn(), so it was NOT guarding the wiring. It is now --
   which is why arm C reddens BOTH D1 and D2 rather than only D1.
 - I wrote vitest's two-argument expect(value, message) into a JEST suite. `tsc --noEmit -p
   tsconfig.json` passed because the project tsconfig EXCLUDES src/__tests__; only jest caught
   it. I now typecheck the test file directly.

ONE FINDING, not mine to fix here: scripts/run-migrations.sh reported "PostgreSQL did not become
ready after 30 attempts" (exit 2) while the database was up and answering. The real cause is that
this host has no pg_isready, and the probe's `2>/dev/null` swallows "command not found", so the
message names the database instead of the missing tool. It exits 2 rather than passing, so nothing
shipped on it. Want me to file it, or is it yours/KS-808's neighbourhood?

— Seat B 26th
