--- comment 5860216619 by linear[bot] at 2026-09-27T22:00:40Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-747/spec-drift-get-apisecuritykeys-declares-no-parameters-while-the">KS-747 Spec drift: GET /api/security/keys declares no parameters while the handler requires organizationId — the contract suite can never reach its 200 branch</a></summary>
<p>

## BLUF

`GET /api/security/keys` **declares NO parameters in the published spec, while the handler requires** `organizationId` **and 400s without it.** So every spec-driven caller — including Schemathesis — is steered into a 400 and **can never reach the 200 branch**.

That is not a cosmetic drift. It is why the KS-742 cross-tenant key-enumeration defect was invisible to the contract fuzzer: the vulnerable branch was unreachable by anything generating requests from the spec.

Raised by Peter on the KS-742 review thread (2026-09-01 13:11Z); he called it "probably its own ticket rather than widening this one". Re-measured here rather than inherited.

## Measured, on both surfaces

**Source** — `services/security/src/security.openapi.ts`, the `method: 'get'` registration for `/api/security/keys`:

* **no** `request:` **block at all**
* the string `organizationId` does **not** appear anywhere in the registration

**The served contract** — `GET http://localhost:6882/api/docs/openapi.json`, i.e. what a consumer actually reads:

```
parameters declared: NONE
responses: 200, 400, 401, 403, 404, 429, 500, 502, 503
```

**The handler** — `services/security/src/index.ts:915-919`:

```ts
const { organizationId } = req.query;
if (!organizationId) {
  return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'organizationId required' } });
}
```

So the contract says "no inputs", and the implementation says "one required input".

## Why it matters beyond tidiness

1. **It blinds the contract suite to this operation's real behaviour.** A generated call omits `organizationId`, gets 400, and the 400 is *declared* — so the run is green while the 200 path has never been exercised. Peter's read on KS-742 was that Schemathesis "would likely never reach the vulnerable branch", and this is the mechanism.
2. **A consumer cannot call the endpoint from the spec.** Anything generating a client from the published contract produces a call that always fails.
3. **It is a KS-663 instance** (nothing in CI stops the spec drifting from the code) with a concrete, measured consequence attached.

## Fix shape

Declare the query parameter on the registration — required, uuid-shaped — so the spec states what the handler enforces:

```ts
request: { query: z.object({ organizationId: z.string().uuid() }) },
```

Then confirm on the **served** spec (the gateway BIND-MOUNTS `secuura-api.yaml`, so it needs a container restart, not a rebuild) that `parameters` is no longer empty, and re-run the Schemathesis `pr` tier to see whether the operation's outcome changes.

⚠ **Do not simply relax the handler to make the spec true. **`organizationId` is load-bearing for tenancy after KS-742 — the fix is to declare it, not to drop it.

⚠ **KS-424 guard:** a new/edited operation needs an explicit `security:` block; this one already has `bearerAuth`, so no change there.

## What is NOT established

Whether declaring the parameter actually changes the Schemathesis result for this operation. That is a prediction, not a measurement — the current `pr`-tier failing set does **not** contain `GET /api/security/keys` (it is 8 M365 operations plus `POST /api/wallets/verify`), because the operation *passes* today by correctly returning a declared 400. Making it reachable could surface new findings on the 200 path. Worth expecting rather than being surprised by.

Filed session 100 from the KS-742 follow-ups.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-747-declare-organizationid-as-a-required-query-parameter-on-the-b4388077dda0">Review in Linear</a></p>

