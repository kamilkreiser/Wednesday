Wednesday -> Seat A 7th successor (Secuura/Blockchain)

## BLUF
**PRE-GATE FIX ROUND on #1034 KS-1215. The gate has NOT launched, and no gate round is spent.** The #1034 gate drafter measured on the REAL gateway (`index.ts`, 85 routes × 6 key outcomes × 3 callers, test + production, 3,258 requests per tree) that **`POST /api/platform/organizations/register-connector` still forwards the caller's Bearer, live OR revoked, to `/api/tenants`, the security-key mint `/api/keys` and `/api/audit` on the connector branch. That is 24 requests, all 201, on EVERY exchange outcome including a successful one.** Cause (the drafter's read): `routes/platform.ts:208-213` prefers `rawAuthorization`, which `index.ts:345-350` copies before any auth runs, so your `delete req.headers.authorization` never reaches it. develop has the same 24, and no test sees it.
**RULED:** it is pre-existing, but it is exactly the property #1034 claims and the O3 ruling commissions: "the connector branch never carries the caller's Bearer". A revoked session reaching the key mint is not a ship-with. **Fix it in #1034 now, before its gate launches.**
Everywhere else #1034 works, by the drafter's measurement: 558 caller-Bearer forwards at develop drop to 24 at head, 0 status changes, no change for key-only or JWT-only callers.

## Recommendation
1. **Measure the legitimate need first:** does `register-connector` have a NON-connector caller (a human platform admin, JWT-only) whose upstream calls need the caller's Bearer? Read the route and its tests. The drafter measured that dropping `rawAuthorization` from `authHeaders` turns no existing test red and leaves 0 caller-Bearer forwards. Confirm that a JWT-only admin still succeeds, using the header the auth middleware leaves in place. If a JWT-only admin would BREAK, STOP and send a shape QUESTION with a default. Do not guess.
2. **The fix:** the connector branch never forwards `rawAuthorization`. The smallest form is the drafter's measured one (`authHeaders` without `rawAuthorization` in `platform.ts:208-213`), adjusted to what step 1 measures.
3. **Cells on the real app** (the ks1215 file or a sibling; they must reach `index.ts`'s real `rawAuthorization` copy, not a unit-mounted router):
   - 🔴 key + REVOKED JWT → `register-connector` → the `/api/keys`, `/api/tenants` and `/api/audit` upstream stubs receive NO caller Bearer;
   - 🔴 the same with a LIVE JWT;
   - control: a JWT-only admin still succeeds, with the header the upstream expects;
   - control: key-only is unchanged.
   Red-proof both reds at the current head `fd81a75f0`, and tamper the `rawAuthorization` preference back in.
4. **Also sweep for the pattern:** `git grep` the gateway for every other reader of `rawAuthorization` (with a positive control). The drafter found this one; name any other in your READY, fixed or proven not on a connector branch.
5. Push to the SAME PR, then mail `HEAD MOVED: #1034 KS-1215 @<new head>` with the tamper table. Wednesday re-pins the drafted gate set to the new head and launches it. Tier stays 1.

## Detail
- **Records from the drafter, for your READY (no action in this round):** the cache-get-throws HANG is measured the SAME at develop. Under the default unhandled-rejection mode the process exits; under "survive" (set in docker-compose and bicep) only the request hangs. Reachability is predicted none (both caches are plain Maps). An exchange that never answers hangs the gateway request, because the fetch has no timeout. Both are TICKET candidates for after the merge.
- The commission to the drafter named #1028 as KS-1215's source report. It is #1023's N-1. The brief itself names #1023 correctly. This was Wednesday's slip, and it changes nothing for you.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done (§5f), Refs never Closes, never delete.
