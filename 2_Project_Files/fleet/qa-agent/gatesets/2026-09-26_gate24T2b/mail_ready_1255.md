## Seat B 28th READY FOR QA — #1255 KS-1301 (15:07:10Z)
MESSAGE_ID <010001a0d91b2915-eb1ec62a-d8a8-4e8c-8728-927b0216b971-000000@email.amazonses.com>
TEXT_SHA256 093b425936b000e8426b35ce44c83db496950c38f1b833cff1732b9f5a8d3917
#1255 KS-1301 head 59245ff0b11c6b760ba5e2a9daedc5927e915e10 (the READY names it in full; origin read by predict_gate24T2b.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T15:07:10.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 28th): #1255 KS-1301 head 59245ff0b11c — 2 red arms, route isolation measured; PROTOCOL CLEAN
---
READY FOR QA (Seat B 28th): #1255 KS-1301 at head 59245ff0b11c6b760ba5e2a9daedc5927e915e10

## BLUF
Item 3 READY, test-only. #1237's presence-not-truthiness pin ported to /sign-cert and /sign-wallet,
ONE RED ARM PER ROUTE with isolation measured both ways. **This push was PROTOCOL CLEAN** — config
diff 0, and the only ref change was my own tracking ref. Not merged. develop `77c6426b96d9`, my base.

## THE FIVE ARTEFACTS
1. **PR #1255** — https://github.com/Secuura/Distributed_Secuura/pull/1255 (open, base develop, 1 commit).
2. **Head, read from origin in the same action:** `59245ff0b11c6b760ba5e2a9daedc5927e915e10`
   (GET /pulls/1255 -> head.sha, and `ls-remote` agrees). 1 file, +23 −0.
3. **Ticket comment naming the PR:** KS-1301 `2f9b93a6-d32e-4dc2-87c8-ceeb86ba3564`, re-counted 0 -> 1.
4. **Test Evidence: in the PR body, written by me, who ran it.**
5. **NOT covered: below.**

## THE GAP, MEASURED RATHER THAN QUOTED
The relabel guard is **byte-identical at three call sites** in `routes/documents.ts`:
  `:2029` /version  — pinned by #1237 (its QVT cells)
  `:2663` /sign-cert  — unpinned
  `:2932` /sign-wallet — unpinned
So the distinction hardest to get right had no coverage on two of its three call sites. Four cells per
route, as the ticket asked: present `null`, present `''`, present `false`, plus a control proving an
ABSENT documentType is still accepted (201, stored and served as the source type). **The control is
what makes these pin a DISTINCTION rather than a refusal** — without it a guard that refused
everything would pass. Built as one describe per route over the suite's existing WRITERS table.

## ONE RED ARM PER ROUTE, ISOLATION MEASURED
  arm: truthiness at :2663 (/sign-cert)   -> own route 3 red | sibling 0 | #1237 /version QVT 0
  arm: truthiness at :2932 (/sign-wallet) -> own route 3 red | sibling 0 | #1237 /version QVT 0
The tamper is `metadata.documentType && …`. Because the line is byte-identical at all three sites a
content replace would be AMBIGUOUS, so each arm tampers **by line number** with the other two guard
lines asserted unmoved. Every restore sha256-verified; `documents.ts` byte-identical to its pre-tamper
state at commit time (checked against a saved copy, not assumed); untampered re-run 122/122.

⚠ **An instrument correction worth carrying.** My first classifier read route attribution off jest's
`✕` lines. **That line carries the TEST name only, with no `describe` prefix** — so with the route in
the describe title, it reported "0 red for this route, 3 for the other" on BOTH arms. The counts were
right and the isolation claim was unsupported. Re-read from `--json` `fullName` (`describe > test`),
where the route is present. Route isolation was the whole point of the arm, so measuring it off a line
that cannot express the route would have been a false pass with the right-looking numbers.

## RAN
- originate jest `--runInBand`: **877/877, 74/74 suites**, rc 0. Baseline **869** at `77c6426b9` in the
  same worktree; **+8 = 2 routes × 4 cells**, fully accounted. Suite file 114 -> 122.
- `npm run lint` (= `eslint src`): rc 0, 0 errors.
- `tsc --noEmit` rc 0; re-run with `exclude: []` and the edited test file asserted in the program
  (705 files, `--listFilesOnly`) because the project tsconfig excludes `src/__tests__`: rc 0.
- `npm test -w packages/shared`: 47 files / 928 tests, rc 0.
- Push rc 0, 7m46s. STOP count matched exactly: `pre_push_hook_base` 28/0,
  `pre_push_hook_base_fixture_guard` 6/0, shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.

## NOT COVERED
- **Preflight INCOMPLETE — 12/15 legs, 3 SKIPPED** (legs 3, 4, 8; `local stack not up`). None of the
  three bears on a test-only change, but they did not run and I am not rounding that up to a pass.
- No live signing path: the issuer-certs upstream is the suite's loopback stub and CIP-8 verification
  is stubbed true, as elsewhere in this suite. The cells prove the GUARD's shape, not the signing.
- `/version`'s guard is untouched, so #1237's own cells are re-run here, not re-proved.
- No integration/e2e cell; no runtime surface changed.

## PUSH PROTOCOL — CLEAN, for once
Lock taken poll 1, 0 s wait. Snapshot diff: **config 0 lines**, refs **1 line** —
`refs/remotes/origin/feature/ks-1301-…-r24-c-1` at my sha, mine. No foreign ref, no foreign worktree,
nothing on develop. The other two seats were quiet during my window, so there is nothing to attribute.

## SESSION SO FAR
#1246 KS-1312+KS-1298 **MERGED** (develop `14cc526d10ee`) · #1252 KS-1275+KS-1299 **READY** ·
#1255 KS-1301 **READY**. Nothing deployed. Every push matched the STOP count; every preflight read
INCOMPLETE 12/15 with legs 3/4/8 skipped, stated in each PR body.

## NEXT, IN THIS TURN
Item 4: **KS-1159** — the ks1061 shared-mock guard is a text scanner blind to `jest.doMock`, double
quotes and subdirectories (its `testFiles()` is non-recursive). Three red arms, T6b/T6c/T7, per the
gate's own probes. Not ending my turn here.

— Seat B 28th
