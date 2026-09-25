KS-849 KYC mock document flow: a 1.5s timer writes back a STALE verification and silently clobbers the selfie's liveness result
state In Progress

## BLUF

`POST /api/kyc/:id/document` schedules a **1.5-second** `setTimeout` that closes over the verification object it loaded, mutates it, and writes it back. `POST /api/kyc/:id/selfie` loads a **fresh** object. So a selfie that arrives within ~1.5 s of the document upload has its liveness result **silently overwritten** by the stale object when the timer fires.

## The mechanism, read from the code at `8b91ab0ae`

1. `/document` (`services/kyc/src/index.ts`) does `await dbSaveVerification(verification)` and then, `if (KYC_PROVIDER === 'mock')`, `setTimeout(() => { …; dbSaveVerification(verification).catch(() => {}); }, 1500)`. The closure holds the object **as it was at upload time**.
2. `/selfie` does `const verification = await dbGetVerification(req.params.id)` — a **different object** — sets `livenessCompleted = true`, `livenessScore = 0.95`, marks the `facial` and `liveness` checks passed, and saves.
3. `dbSaveVerification` is a full upsert: `ON CONFLICT (id) DO UPDATE SET … liveness_completed = EXCLUDED.liveness_completed, liveness_score = EXCLUDED.liveness_score, checks = EXCLUDED.checks, …`.

So at t+1.5 s the stale object writes `liveness_completed = false`, `liveness_score = NULL` and a `checks` array without the two passes. **The three clobbered columns are named explicitly in the upsert** — this is not a guess about ORM behaviour.

The `.catch(() => {})` on that write means the overwrite is also silent if it fails.

## Scope and priority

`KYC_PROVIDER === 'mock'` gates the timer, so this is the **mock/demo path**, not a live-provider path. It is still the path every demo and every local test drives, and a verification that loses its liveness pass looks like a subject who never completed one. **Pre-existing** — not introduced by KS-386.

## Fix shape (not chosen)

Re-read the verification inside the timer before mutating it, or narrow the timer's write to the document fields it actually owns. Both change concurrency behaviour, so this wants its own gate rather than a drive-by.

## Provenance

Found by the KS-386 #839 tier-1 gate as F-5 and ruled by Wednesday 2026-09-06 as a ticket, not part of that round. Reproduced from the source independently before filing: the fresh-load in `/selfie`, the closure in `/document`, and the upsert's `DO UPDATE SET` column list were each read and are quoted above.
