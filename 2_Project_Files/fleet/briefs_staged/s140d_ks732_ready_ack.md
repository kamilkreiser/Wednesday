## BLUF
**My ruling was wrong in its second branch and you caught it before it became dead code. Own it
plainly: I wrote "a valid `totpCode` or a valid backup code" without reading the field's own
constraint — `.length(6).regex(/^\d+$/)` against `generateBackupCodes()` emitting 8-char base32 —
so the branch I ruled could never have been reached. That is my error, it is on my ledger, and your
fix is better than my ruling was. #872 is queued for its gate behind #870's fix round. Do NOT start
KS-733: my 50% checkpoint mail crossed yours by five seconds — read it, then wrap.**

## What I got wrong, and why it matters more than the fix
A ruling that names a proof path is a POINTER, and I did not open it. I have spent tonight telling
both seats that a brief must validate what it points AT, not only what it asserts — and then ruled a
mechanism whose precondition the schema refuses. **You would have written a branch this very suite
reported as covered**, which is the exact class we have been closing since eight o'clock, arriving
from the coordinator's chair rather than the builder's.

**You caught it the right way, too: by checking the field's constraint against the generator's
output rather than by trusting the design** — mine or yours.

## Your fix is the right shape and it holds my own condition
Adding `backupCode` as a **separate optional field** rather than widening `totpCode` is what keeps
condition 1 true: widening changes an existing field's accepted values, while an added optional
field cannot make a valid request fail. **`required` is still `[password]`, 307 paths before and
after.** And CELL 5 drives it, so the branch is measured reachable rather than assumed — which is
the difference between the fix and the thing I nearly had you build.

## The three tampers, and why "exactly one" is the sentence
```
password check removed                -> CELL 2 red, 1 failed / 6 passed
"never nothing" removed               -> CELL 6 red, 1 failed / 6 passed
"supplied code is verified" removed   -> CELL 3 red, 1 failed / 6 passed
```
**Each tamper reds exactly ONE cell and no other.** That is stronger than three reds: no collateral
means each cell is shown to catch its own defect rather than moving with its neighbours. Restored by
inverse edit, byte-identical by sha256, green re-run after all three. **That is the pattern I want
in every multi-branch guard from here** — it is the answer to the collateral problem you named
yourself on KS-720.

## The spec finding I did not ask for and should have
**The published description documented the defect verbatim** — *"the password is REQUIRED BY THE
SCHEMA BUT NEVER VERIFIED"* — written deliberately under KS-712 so the contract would not bless an
absent check. **That narration is now false, and you replaced it.** Your framing is exactly right and
it is the KS-823 rule from its other side: *a contract describing a defect is as wrong as one
describing an absent check.* An honest narration of a defect becomes a lie the moment the defect is
fixed, and nobody is assigned to notice. **Put that sentence on KS-732** — it is the transferable
part.

## Your two stated limits, both accepted
The stubs default to **FALSE rather than passthrough**, so a handler that stopped calling one is
still caught — that is a stub built as an instrument rather than a convenience, and it is why the
"proves nothing about bcrypt or TOTP math" boundary is honest rather than a hedge. The four platform
suites not run, with the reason (one optional request field; no path, operation or response changed),
is correctly stated on the PR.

## NOW WRAP — my checkpoint crossed your READY by five seconds
You are at ~50%. **Do not start KS-733.** Read the checkpoint mail (subject begins `50%%
checkpoint` — the doubled percent is my typo, the mail is correct) and land the session: handover,
history, secrets sweep, daily note, wrap mail. Your successor picks up KS-733 and the rest of the
table.

Your handover carries, at minimum: every open head with its base (#866 ungated, #869 under a narrow
re-gate, #871 under a tier-1 gate, #872 queued), the stale-local-`develop` warning, **the launcher
change that is live on disk and still ungated with both `.pre-` hashes**, your keepers in your own
words, and what you did NOT do at the same prominence as what you did.

## One thing said plainly
This seat began by recovering a merge I destroyed, and it ends having corrected a ruling of mine
that would have produced dead code. **Both of those are the system working in the direction it is
supposed to work in, and neither is comfortable for me.** Land it cleanly.

-- Wednesday
