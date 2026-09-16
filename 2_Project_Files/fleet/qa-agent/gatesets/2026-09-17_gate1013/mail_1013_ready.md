hits: 1
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1013 KS-999 @5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-16T18:42:22.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
Seat A

## BLUF
- READY FOR QA: https://github.com/Secuura/Distributed_Secuura/pull/1013 at head 5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2 (API = ls-remote, read just now). Base develop 1125607e9 (#1010's squash, unmoved).
- A14 KS-999, items 1 + 3 + 4. getUserById awaits fromRow (userRepo.ts:406), so a subject-DEK read failure inside fromRow reaches the KS-253 classifier: 503, not a raw 500. AUTH SERVICE, not auth logic.
- Tier: I propose TIER 1 (a 500 -> 503 change on the normal production path of four calling route families; item 2 is the gate's).
- Links: KS-999 contributes, In Progress (its own PR); "Part of KS-999"; it stays open on merge per 5f. KS-1186 / KS-1168 / KS-963 / KS-253 are named, not linked, unmoved. Ticket comment 5970b7c1-a911-47ae-bd53-5706d73951fd.
- Follow-up filed BEFORE the PR, as the brief asks: KS-1186 (Backlog, Medium, related KS-999), the sibling unawaited returns, board searches quoted.
- Now at 3 open again: #1011 0a1f8900c, #1012 e225a4948, #1013. All heads unmoved. Holding; A15 KS-1018 not started.
- Files disjoint from #1011 / #1012: services/auth only.

## Recommendation (for the gate)
1. Item 2 is untested here: no HTTP, no live DB, no contract run for /oauth/token, /users/me, /mfa/status, /wallet/*.
2. A decrypt failure (plaintext cutoff) still propagates as-is but is now LOGGED by the catch as "DB getUserById failed". That is new operator noise; the ks949 characterisation cell for it still passes unchanged.
3. The brief named four sibling sites; the source has FIVE (:442, :508, :581, plus :590, the legacy arm in getUserByEmail, and :623). All five are in KS-1186. :1036 listUsersInner returns Promise.all outside any try, so no classifier is skipped there and it is not listed.
4. Seat edits, declared:
   - ks949 item 4: the logger mock captures error, and the KS-963 infra cell asserts the operator log;
   - ks949 item 3: the "UNAWAITED fromRow" cell renamed to what it proves, assertion unchanged;
   - the ks949 KS-963 header gets a KS-999 note;
   - the userRepo.ts KS-963 doc comment no longer says this await is "deliberately NOT done here".

## Test Evidence (summary; full block in the PR body)
- Apply: --directory=Blockchain/Dev (the paths lack the prefix); the test renamed in the patch to ks999-getuserbyid-awaits-fromrow.test.ts. Both sections clean. Before the seat edits the product diff was exactly the READY pair.
- Red before green at 1125607e9: 5 run, 2 red ("…to throw error matching /temporarily unavailable/ but got 'connection terminated unexpectedly'"; "expected vi.fn() to be called with 'DB getUserById failed'"), 3 controls green, 0 skipped. Product applied: 35/35 (ks999 5 + ks949 30, the gate's "30 still pass").
- Tampers: whole auth suite per row (745 cells, 0 skipped), project tsc rc per row, byte restore asserted. All as predicted, every row tsc 0.
  - T0: 0 red.
  - TA (await removed): 2 red, the ks999 pair.
  - TL (catch no longer logs): 2 red, the ks999 log cell + the ks949 item-4 assertion.
  - TC (classifier disabled): 3 red (ks949 infra, ks999 infra, ks999 query()-side control).
  - TI (inert): 0 red.
  - T0 after: 0 red.
- auth at head 61 files / 745 pass (base 60 / 740). shared 44 / 851 pass. Project tsc auth rc 0.
- Including tsc: 0 in userRepo.ts and ks999. ks949's 7 TS1343 import.meta errors are the same base lines shifted +2, none on a changed line.
- eslint 0.
- Pre-push preflight in-hook 18:35:13Z -> 18:40:52Z rc 0: "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed." Legs 3/4/8 skipped (no stack); not a pass. Push verify PROTOCOL-CLEAN.
- Skill 4 docs unaffected (ks999 / ks949 / userRepo / 745: 0 hits in both), stated in the body. Host line in the body.

## NOT done / NOT covered
- Item 2 (the calling routes over HTTP / contract).
- No live Postgres or DEK store.
- KS-1186's five sites.
- Schemathesis / Akto / Playwright / k6 not run (no stack, 0 docker images).

Seat A

