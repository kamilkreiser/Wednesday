--- comment 5826048358 by linear[bot] at 2026-09-25T03:11:32Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-976/rate-limit-refusals-name-the-wrong-field-400-says-key-required-when">KS-976 Rate-limit refusals name the wrong field: 400 says "Key required" when the key was fine, and 403 says "Caller has no tenant" when the caller has one</a></summary>
<p>

## BLUF

**Every new refusal path returns a message that names the wrong thing.** A 400 says the key is missing when the key was fine; a 403 says the caller has no tenant when the caller has a perfectly good one. Charter §4d: a 4xx must not be scored as a healthy rejection without knowing *why* it was returned — and these messages actively mislead about the why.

Recoverable rather than silent: `details` carries the truth on the 400.

## ITEM 1 — `/reset` answers 400 "Key required" for failures that have nothing to do with the key

`index.ts:1358` — the top-level message is a constant:

```
{"key":"login","tenantId":"   "}      -> 400 "Key required"  details:[{path:["tenantId"],message:"must not be blank"}]
{"key":"login","tenantId":"\ud800"}   -> 400 "Key required"  details:[{path:["tenantId"],message:"must not contain an unpaired surrogate"}]
{"key":"login","tenantId":257 c.p.}   -> 400 "Key required"  details:[{path:["tenantId"],message:"must not exceed 256 characters"}]
```

The key was supplied and was fine in all three. **KS-970 item 6 has just PUBLISHED "Refused with** `400` **if present but blank"** — so the contract now promises a refusal whose top-level message names a different field.

**Fix-shape:** derive the message from the first failing path, or make it generic ("Invalid request body").

## ITEM 2 — the 403 "Caller has no tenant" now fires when the caller HAS a tenant

`index.ts:1267` (`/check`) and `index.ts:1377` (`/reset`). After KS-970 item 2 this fires when the caller has a good tenant and the *user* claim or the *body* is unusable:

```
claims {tenantId:'…a', userId:123}  -> 403 "Caller has no tenant"   <- false: the caller has tenant …a
```

**Fix-shape:** split it, so "no claim to scope by" and "present but unusable" say different things.

## ⚠ AN IMPLEMENTATION HAZARD I MEASURED, WHICH THE FINDING DOES NOT MENTION

`"Caller has no tenant"` appears at **FOUR** sites, not two: `index.ts:665`, `:716`, `:1267`, `:1377`. **A fix that greps for the string will touch all four and two of them are correct.**

Verified at `0281b0faa`:

* `:665` **and** `:716` **are NOT instances.** Both guard `if (!isPlatformRole(...) && !callerTenantId)` — they test the tenant claim *directly*, so the message is literally true there.
* `:1267` **and** `:1377` **ARE the instances.** Both sit behind `if (scope === null)`, and `scope` is null for **three** different reasons — no tenant claim, a MALFORMED tenant, or a MALFORMED user/`sub`. The message asserts only the first.

So the finding named the right two sites. **The other two share the string and not the defect**, and that distinction is the thing to carry into the fix.

## REGRESSION TEST

**Assert the message TEXT, not just the status.** Every cell here passes today on status alone, which is why the defect shipped: a 400 is a 400 and a 403 is a 403 whatever they say. Include a cell for `:665` or `:716` asserting the message stays "Caller has no tenant" there, so a fix does not over-reach into the two correct sites.

## RELATED, NOT MERGED IN

Item 2's root cause is the same tri-state as **KS-975**. Kept separate because the fix lives in the error-construction path rather than in the tri-state itself — but whoever takes one should read the other.

## SEARCHED BEFORE FILING

STRING `Caller has no tenant`, `Key required` · SYMBOL `resetRateLimitSchema`, `checkRateLimitSchema`, `explicitScope`, `principalScope` · PATH `services/security/src/index.ts`. Linear's search is fuzzy on multi-word phrases and returned ~20 loosely-related hits for each string; **none on inspection concerns these routes' message construction.** The precise symbol searches return only **KS-970** (parent) and **KS-645** (a closed Duplicate about `/reset`'s role check, a different property). Control: a `KS-970` search is non-zero, so the search discriminates.

## PROVENANCE

QA tier-1 gate on **#894 over #893**, verdict 2026-09-07T09:45:45Z, quoted verbatim by the coordinator. **All four call sites re-verified against** `0281b0faa` **before filing** — which is how the two non-instances were found.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-976-msg400-the-reset-400-names-the-field-that-actually-failed-4ee152375ed2">Review in Linear</a></p>

