KS-980 The KS-597 integration suite claims two RLS-permissive paths and exercises one — platform_bypass never reaches its own mechanism
state In Progress

## BLUF

**The KS-597 integration suite's header claims it isolates TWO RLS-permissive paths. It exercises ONE.** The `platform_bypass` cell never reaches the mechanism it is named for.

**The property under test still holds** — the gate measured it separately on the real path — so this is a **coverage-claim** defect, not a behaviour one. The suite is not wrong about the product; it is wrong about itself.

## The mechanism, verified on merged develop (`2ff0eb850`)

The header (`ks597-issuer-organization-id.integration.test.ts:25-28`) states:

> *"both cells here isolate the two paths where RLS does NOT exclude the row: P1* `app.tenant_scope_bypass = 'platform_admin'` *(the documented admin path), P2 a BYPASSRLS role (the documented rollback connection)."*

But `writerOn()` (`:138-147`) opens **the same connection for both**, and its own comment says why:

```
// 'bypassrls' needs no GUC: TEST_DATABASE_URL's role is the BYPASSRLS one.
```

**The role already bypasses RLS in both branches.** The `platform_bypass` branch merely sets a GUC on top of a connection that was never subject to the policy — so the GUC is **inert**, and P1 (a non-bypassing role relying on the admin GUC) is never exercised at all.

**Corroborating evidence produced by accident:** during KS-597's round-2 tamper (deleting the tenancy predicate from both `organizations` subqueries), the `platform_bypass` and `bypassrls` cells reddened **identically**. Two genuinely distinct mechanisms would not have to.

## Why it matters

P1 is the path a **platform admin** actually uses. It is the arm where the tenancy predicate is doing the work alone against a role that RLS *would* otherwise constrain — which is precisely the property the suite exists to prove. Today that arm has no coverage while the header says it does, and a reader auditing this file would reasonably stop looking.

## Fix-shape — a decision, not just an edit

Either:

1. **Make P1 real** — connect as a role that does **not** carry BYPASSRLS (e.g. `secuura_app`), set `app.tenant_scope_bypass = 'platform_admin'`, and assert the same property. This needs a second connection string in the harness, and the disposable-Postgres provisioning already creates `secuura_app` (`rolsuper=false, rolbypassrls=false`), so the role exists; or
2. **Correct the claim** — state that the suite covers the BYPASSRLS path only, and record P1 as uncovered.

**(1) is the better outcome and (2) is honest.** What is not acceptable is the current state, where the file asserts coverage it does not have.

## Filed separately from F-A — and why

The coordinator proposed grouping this with F-A conditional on their being one edit. **They are not:** F-A is a two-line comment sweep with no decision; this carries the choice above and possibly a new connection role. **Different fixes, different workloads.** Collapse them if you disagree.

## SEARCHED BEFORE FILING

PATH `services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts` · SYMBOL `writerOn`, `tenant_scope_bypass`, `BYPASSRLS`, `secuura_app` · STRING `the two paths`. Only **KS-597** returns an open hit. Related but not duplicate: the RLS/tenancy tickets on this board concern product behaviour, not this suite's self-description. Control: a `KS-970` search is non-zero, so the search discriminates.

## PROVENANCE

QA tier-1 re-gate on **#889 round 2** @ `48ad0354e`, 2026-09-07T10:49:03Z, finding **F-C (Minor)**. **Header and** `writerOn` **re-read from** `origin/develop` **after the merge before filing.**
