--- comment 5860401337 by linear[bot] at 2026-09-27T22:25:27Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-692/security-apistatus-revokeunrevoke-has-no-tenant-ownership-check-an">KS-692 Security: /api/status revoke/unrevoke has no tenant ownership check — an ISSUER_ADMIN in any tenant can revoke another tenant’s credential (KS-586’s deferred half, now untracked)</a></summary>
<p>

## Summary

`POST /api/status/:id/revoke` and `/unrevoke` enforce an **admin-class role** but **no tenant ownership check**. An `ISSUER_ADMIN` in one tenant can revoke or un-revoke a credential in **another tenant's** status list. Reproduced live on `develop 576ebef85`.

This is the **second half of KS-586**, which fixed the role gap and explicitly deferred the tenant gap — but **KS-586 is now** `Done`**, so nothing tracks the remainder.** That is why this ticket exists.

## ⚠️ What is already FIXED — read this before working the ticket

**KS-586 is done and its fix is live. **`/api/status` is no longer "no authorization at all". Anyone picking this up from a summary of [KS-570](https://linear.app/secuura/issue/KS-570) will be looking for a defect that is not there.

| probe (local, `develop 576ebef85`) | result |
| -- | -- |
| `holder@secuura.com` (**OWNER**, non-admin) → revoke | **403 **`Role OWNER is not authorized for this action` |

The role gate at `services/vc-issuer/src/routes/status.ts:42-53` (`STATUS_WRITE_ROLES`, applied as a router-level gate ahead of the route table) works. Commit `bda40c91c` on `develop`, present in the running container.

## The defect that IS live — reproduced, controls both ways

Two `ISSUER_ADMIN`s in **different tenants**:

* `demo@secuura.io` — tenant `default`
* `registrar@oxford-test.invalid` — tenant `oxford`

| # | actor | request | result |
| -- | -- | -- | -- |
| 1 | demo (owner) | `POST /api/status` create list | **201** |
| 2 | demo (owner) | `POST /api/status/:id/allocate` `cred-xtenant-probe` | **200**, index 0 |
| 3 | **oxford registrar (foreign tenant)** | `POST /api/status/:id/revoke` that credential | 🔴 **200** — `{"revoked":true,"reason":"cross-tenant probe"}` |
| 4 | demo (owner) | `GET /api/status/:id/revoked` | **200** — `{"revokedIndexes":[0],"totalRevoked":1}` — the write really landed |
| 5 | **control** — oxford registrar | revoke against a **non-existent** list id | **404 **`Status list not found` |
| 6 | **control** — holder (OWNER) | revoke the same list | **403** (role gate) |

**Controls 5 and 6 are what make row 3 mean something.** Row 5 proves the 200 was a genuine authorisation pass and not a blanket accept — the same foreign caller is refused when the target does not exist. Row 6 proves role is still evaluated, so the only thing missing is the tenant comparison.

## Root cause

`services/vc-issuer/src/routes/status.ts`. The router-level gate checks **role only**:

```ts
return requireRole(...STATUS_WRITE_ROLES)(req, res, next);
```

There is no comparison of the caller's tenant to the status list's owner — **because the status list has no owner to compare to.** Status lists live in a process-local `Map` with no tenant linkage. The code says so itself (`status.ts:35-38`):

> *"Tenant scoping is NOT enforced here yet: status lists live in a process-local Map with no tenant linkage, and the ownership model is the KS-539/KS-547/KS-586 joint authorization decision — tracked on KS-586."*

**"tracked on KS-586" is no longer true.** KS-586 is `Done` (2026-08-12) and KS-547 is `Done`; KS-539 is open but scoped to *governing rules for document operations by agents*, not status-list tenancy. The deferral outlived its tracker — which is the actual reason this went untracked for two weeks.

## Why this is not a duplicate

* **KS-586** — `Done`. The **role** half. Fixed.
* **KS-570** — the **authentication** half: the gateway mount at `proxy.ts:702` has no `authenticateToken`, so revoked-session JWTs still pass. Different layer, still open.
* **KS-588** — `Backlog`. **Test coverage** for `/api/status` authorization. Would catch this once it exists; is not the fix.
* **This ticket** — the **tenant/ownership** half. No ticket held it after KS-586 closed.

## Severity

**High.** Revocation state is an integrity operation on a document-authenticity platform — an attacker with any admin-class role in any tenant can un-revoke a credential their victim revoked, or revoke a live one. Same family as [KS-643](https://linear.app/secuura/issue/KS-643) (cross-tenant API-key revoke) and [KS-642](https://linear.app/secuura/issue/KS-642), and it sits on the same **KS-621 tenancy boundary** that is currently held for @kamil.kreiser's design ruling.

Not raised to Urgent: exploitation needs a valid admin-class credential in *some* tenant, so it is privilege-escalation-across-tenants, not anonymous.

## Suggested fix — NOT implemented, deliberately

The ownership model is a **KS-621 boundary decision** and is @kamil.kreiser's call, exactly as with KS-643. Filing only, per the same hold.

The prerequisite is structural: **a status list must carry an owning tenant before any check can be written.** The process-local `Map` has nowhere to put one, so this is not a middleware one-liner — it needs the list persisted with a tenant column, which is likely the same decision as KS-539's ownership model.

Note the interlock, learned from KS-578/KS-643: adding a tenant check **without** giving lists an owner would refuse every caller, since no list has a tenant to match.

## Reproduction

Local stack, `develop 576ebef85`, both accounts seeded. Full curl sequence is rows 1–6 above. Probe artefacts were written to the **local** stack only (`ks661-tenantprobe-*`); status lists are process-local and clear on a `vc-issuer` restart. **Nothing was written to demo.**

Handed over by @peter on KS-570 (2026-08-26 08:10Z): *"The one still open is the /api/status authorisation gap … I will let you file that one too, as you hold the evidence for it."* — filed with the measurement rather than the paraphrase, which is how the KS-586 half turned out to be already fixed.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-692-restrict-vc-issuer-status-writes-to-the-platform-roles-c44be83300e1">Review in Linear</a></p>

