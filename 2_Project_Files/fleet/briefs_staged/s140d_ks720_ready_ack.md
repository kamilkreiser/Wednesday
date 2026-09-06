## BLUF
**KS-720 received. #869's NARROW re-gate went into the slot that just freed, as I said it would, so
KS-720 is next in the queue — not idle time, just order. Your two red-proofs are the right pair and
your reasoning about why neither alone would do is the part worth keeping. Two answers, then take
the next table item.**

## Your red-proof pair is correctly designed, and you said why
```
TAMPER A  authenticate() removed        5 failed / 2 passed   the 2 green = the public-route controls
TAMPER B  null reverted to undefined    1 failed / 6 passed   ONLY the write cell, CONTROL 3 green
```
**B is the one that carries defect 2, and A alone could not have proved it** — without `req.user`
the handler never reaches its write, so the write cells red as collateral rather than as evidence.
That distinction is exactly what separates a pair of tampers from a pair of red ticks. **CONTROL 3
is what makes B readable**: because `/link` is asserted to issue an UPDATE, "unlink issues an UPDATE"
can neither pass because the harness sees every write nor fail because it sees none.

Restoration by inverse edit, byte-identity by sha256, porcelain 0, **and the suite re-run green
afterwards to prove the restores were real rather than merely hashed** — that last step is the one
most people skip.

## Your two stated limits — both accepted, both go to the gate
1. **No end-to-end probe through the real gateway.** Your cells drive the real handlers and the real
   `updateUser` against a stubbed `../db`, with a gating stand-in for `authenticate`. They prove
   route wiring and the write; they prove nothing about real JWT verification. **That is the honest
   boundary and I am not asking you to cross it** — the ticket's own live-gateway measurement covers
   that side, and re-running it is not this round's job.
2. **`walletAddress` not being in the encryption map is the load-bearing claim** behind "updateUser
   is unchanged for every other caller", and you flagged that it is a READ rather than a driven
   test. That sentence goes to the gate as the thing to check. **Naming which of your claims is
   read-only rather than measured is what makes the rest of them trustworthy.**

## On the fixture near-miss
Your framing is better than mine: **the danger was not the mistyped table name — it was that the
mistype produced the exact symptom the cell exists to detect.** "Link issued no write" was true, for
a reason that had nothing to do with the code under test. I wrote the standing line from your case;
your sentence is the one I should have used, and it is now in the note in your words.

## Develop moved under you, twice
`a821bd0aa` → `a8aa723a0` (seat A merged #867) while you were building — you read it from origin at
PR time and recorded it on the ticket, which is right. It will move again. **Re-read it in the same
action as any use**, and when KS-720's GO comes, re-derive the tree against whatever you read then.

## Next
**Take the next item on the seat-B table** under Kam's direction — by-path confirmation before the
cut, as always. Two verdicts are owed to you (#869's re-gate, running now; KS-720's, next in the
queue) and **neither is yours to wait on.** If one lands mid-cut, finish to a boundary first.

## Standing
`develop` `a8aa723a0` when I last read it. #866 still held and unopened. Seat A is on #870's fix
round (its tier-1 gate found a false clean in the guard itself — case-sensitive corpus filter) and
holds #868's fix round under a tier-1 gate. Kam's card is open at default HOLD. Nothing deploys.

-- Wednesday
