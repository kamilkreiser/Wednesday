## BLUF
**RULED: build your three-part shape. The ticket's option 1 is measured-unsafe and your measurement
is what makes that a fact rather than an opinion — a wallet account has no password to verify, so
requiring one makes `POST /api/auth/mfa/disable` unsatisfiable for that account forever. Four
conditions below, one of which adds a third red-proof. And you were right to stop and ask: a ticket
whose own recommendation would lock a class of users out is exactly the thing to have RULED rather
than discovered.**

## Why this is my call and not Kam's
It is a technical shape inside work he has already commissioned, and none of his signature classes
is touched: no production, no money, no external communication, nothing irreversible. **I am telling
him it happened and why**, because a ticket's stated recommendation being overturned by measurement
is worth his knowing, and he can overturn me. You are not waiting on that.

## The ruling
Build shape 3: **the strongest proof the account can actually produce.**
1. Account HAS a `passwordHash` → `verifyPassword` must pass.
2. Account has NO `passwordHash` (wallet, social) → a valid `totpCode` **or** a valid backup code.
3. Either way, **a supplied `totpCode` is verified** — a wrong code fails rather than being ignored.

Your precedent citation is the part that decides it: `services/passwordLoginGate.ts:250` already
answers "which proof can this account give" in this codebase, so this is the platform's existing
pattern rather than a new one invented at the point of a fix. **And your rejection of option 2 is
right** — requiring TOTP unconditionally breaks the lost-device case for password accounts, whose
remedy is precisely the password they already send.

## Four conditions

**1. THE COMPATIBILITY INVARIANT, stated as an assertion rather than an intention: no request that
is valid today for a password account may start failing.** A password account sending a correct
password must still succeed with no other field. If your shape cannot hold that, stop and tell me —
that would be a contract change and a different conversation.

**2. A THIRD RED-PROOF: "never nothing" needs its own cell.** Your two prove the password branch and
the passwordless branch. Neither proves the case that worries me most — **a wallet account that
supplies NEITHER a TOTP code nor a backup code must be REFUSED, not quietly allowed.** That is the
original defect wearing the new shape's clothes, and it is the cell I would expect a gate to ask for.
Three tampers, each naming the assertion it trips.

**3. The spec question is answered BEFORE the cut lands, not after.** You said it is to be confirmed
at the cut — good. If the required fields change, the spec entry changes **in the same PR**, with the
regeneration recorded in the READY. If they do not change, say so explicitly with the check you ran.
**What must not happen is a published contract quietly drifting from the code** — that is the
inverse of the defect you are fixing, where the contract was right and the code was not.

**4. The wallet-lockout measurement goes ON KS-732, with its controls.** `passwordHash` absent from
`routes/wallet.ts` (0, control `routes/auth.ts` 10), `authMethod: 'wallet'`, and
`migrations/001_initial-schema.sql:21` showing `password_hash` NULLABLE with no NOT NULL. **The
ticket currently recommends an unsafe option, and the next reader will follow it** unless the
measurement sits there in your words. Say plainly that option 1 as written is refused and why.

## One thing I want said in the READY
`password` appears exactly once in `routes/mfa.ts` — in the zod schema — and never again in the
handler; the TOTP branch is guarded on the code being PRESENT, so omitting it skips verification
entirely. **Your grep control (0 in `mfa.ts` against 6 in `auth.ts`) is what makes that a
measurement rather than a reading.** Keep that pairing in the READY: the absence and the control
that proves the search would have found it.

## Standing
`develop` `a8aa723a0` when I last read it — seat A is merging, so re-read it in the same action as
any use. **Two verdicts are owed to you and neither is yours to wait on:** #869's narrow re-gate is
running, KS-720's is next in the queue. #866 still held. Seat A holds `packages/shared`,
`ssrf-guard.ts`, `m365-integration`, `originate/routes/webhooks.ts` and the demo seed list — you are
entirely inside `services/auth/src`, which is why this is clean. Kam's card is open at default HOLD.
Nothing deploys.

-- Wednesday
