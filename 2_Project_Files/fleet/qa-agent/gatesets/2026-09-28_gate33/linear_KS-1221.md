KS-1221 ks744 cells never test a falsy claim - a verificationLevel of '' or null must forward no x-verification-level (an undefined-only guard stays green)
state In Progress

## BLUF

**Test-only, Minor.** PR #1028 (KS-744, merged as `0a2b1603f`) changed what the gateway forwards for a falsy claim: a verificationLevel or email of `''` / `null` / `0` / `false` is now dropped, where develop forwarded `''` / `'null'` / `'0'` / `'false'`. No test cell pins that. A guard written as `!== undefined` instead of a truthiness check stays green on the whole api-gateway suite (57 files / 555 tests). Found by the tier-1 gate on #1028 as finding F-1, ruled SHIPS-WITH.

## Recommendation

Add cells to `services/api-gateway/src/__tests__/ks744-a-token-missing-a-claim-is-proxied-not-500.test.ts`: a verified token with `verificationLevel: ''`, and one with `verificationLevel: null`, each proxied (200, one upstream hit) with NO `x-verification-level` reaching the upstream. Optionally add a numeric-claim cell that records today's string coercion.

* **Regression proof:** the gate's G-UNDEFONLY tamper (the level guard at `middleware/auth.ts:398` written as `decoded.verificationLevel !== undefined`) must red the new cells. Today it reds 0.
* Test-only; no product change. Not built here: routed to the local model.

## Detail

* **Today (develop** `0a2b1603f`**):** `auth.ts:393` sets `x-user-email` only `if (decoded.email)`; `:398-399` set `x-verification-level` only `if (decoded.verificationLevel)`, else delete it. The ks744 cells R1 / R2 / R3 build tokens with the claim ABSENT, so a truthiness guard and an undefined-only guard behave identically for them.
* **Measured by the gate on the real gateway:** a falsy level or email is forwarded as `''` / `'null'` / `'0'` / `'false'` at develop `19f1e5475` and is absent at the head and on the merged tree. No reader consumes those values.
* **Searched before filing** (Linear, literal matches in titles, descriptions and comments, archived included): `falsy` (15 hits, none on the gateway claim headers: KS-1006, KS-1123, KS-1074, KS-943 and others on unrelated code); `x-verification-level` (2: KS-744 itself, KS-742 Done); `ERR_HTTP_INVALID_HEADER` (3: KS-744, KS-1208, KS-742). No ticket covers this cell.
* **Refs:** KS-744 (stays In Progress).
