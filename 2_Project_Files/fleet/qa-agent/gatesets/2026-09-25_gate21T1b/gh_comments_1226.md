--- comment 5826637052 by linear[bot] at 2026-09-25T04:19:48Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1292/nothing-runs-tsc-p-packagesshared-the-push-preflight-has-no-project">KS-1292 Nothing runs `tsc -p packages/shared` — the push preflight has no project type-check leg, so a type error is invisible (KS-872 acceptance, second half)</a></summary>
<p>

## BLUF

`npx tsc -p packages/shared --noEmit` is **not run by anything**. Not by the push preflight's fifteen legs, not by vitest (which does not type-check), not by any remaining CI. A type error in `packages/shared` is therefore red in `tsc` and **invisible everywhere the team actually looks**.

KS-872 was filed when exactly that happened: `crypto.JsonWebKey` vanished in `@types/node` 26.1.0 and the project tsc went red on develop with nobody noticing. That ticket's acceptance has two halves. The fix is one; **this is the other** — *"either the preflight gains a shared project type-check leg, or a ticket says explicitly why it should not."*

## Measured today (2026-09-25, at develop `6ab9d5021e96`)

`npx tsc -p packages/shared --noEmit` exits **rc 0**, zero output, on a clean `npm ci` at `Blockchain/Dev`. A planted `const x: number = 'not a number'` gives **rc 2 / TS2322**, and removing it returns rc 0 — so the check is live, and the original error genuinely does not reproduce.

**Why it is green is the point, and it is fragile.** `npm ci` NESTS `packages/shared/node_modules/@types/node@20.19.43` (the package declares `^20.11.5`) beside the hoisted `@types/node@26.1.0`. The nested 20.x still carries `crypto.JsonWebKey` at `crypto.d.ts:513`; in 26.1.0 that interface moved to `webcrypto.JsonWebKey` (`crypto.d.ts:3630`). **Nothing pins that nesting.** A hoist change, a dedupe, or a lockfile refresh can remove it, and the error returns — to a check that still nobody runs.

## Ask

Add a `packages/shared` project type-check leg to the push preflight (`.githooks/pre-push`), **or** record here why it should not exist. If it is added it needs a planted-error control, like every other leg — a type-check that cannot fail is the failure mode this ticket is about.

## Searched before filing

Six terms, `includeArchived: true`, every page literal-matched on the title: `type-check leg` (50 fuzzy / **0** literal), `tsc` (50 / **12**), `preflight leg` (50 / **8**), `project type-check` (50 / **0**), `packages/shared tsc` (50 / **0**), `noEmit` (50 / **1**). **KS-872 itself has zero relations, zero inverse relations and zero children.**

Nearest, and all a different class:

* **KS-892** and **KS-933** — both *Duplicate/ARCHIVED* — say the project tsc is VACUOUS for `src/__tests__` because the tsconfig excludes it. That is *"the tsc does not cover enough"*, not *"no leg runs the tsc"*. Named rather than linked: archived issues refuse relations.
* **KS-1000 / KS-1122 / KS-848 / KS-1090** — the same excludes-`__tests__` class in auth, vc-issuer, kyc and api-gateway.
* **KS-910 / KS-1040** — preflight *leg* tickets, but legs 12 and 4.

**No open home; filed new.**

---

*Filed by Seat L3, 2026-09-25, on Wednesday's ruling (ANSWER Q1b). Carries the second half of KS-872's acceptance;* `.githooks/` *is in no seat's lane this round.*
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-872/packagesshared-project-tsc-is-red-on-develop-cryptojsonwebkey-is-gone">KS-872 packages/shared project tsc is RED on develop — crypto.JsonWebKey is gone in @types/node 26.1.0; a live type error no gate owns</a></summary>
<p>

## BLUF

`packages/shared`'s **project** `tsc` reports **1 error** on develop, and no gate owns it.

```
src/crypto/jwks.ts(129,51): TS2694 — namespace 'crypto' has no exported member 'JsonWebKey'
```

`crypto.JsonWebKey` was removed in `@types/node` **26.1.0**. Found by the KS-843 round-3 gate.

## Not caused by the KS-843 work — measured

`git diff 59248bf38 e1d9d9380 -- '*packages/shared*'` is **EMPTY**. The toolchain moved under the shared install some time after 12:38; the source did not change.

## Why nothing caught it

The push preflight's twelve legs do not include a `packages/shared` project type-check, and the vitest suite is green (**709/709**) because vitest does not type-check. So this is red in `tsc` and invisible everywhere the team actually looks.

## Fix shape

Either import `JsonWebKey` from where `@types/node` 26.x now exposes it, or declare the shape locally (it is a small, stable JWK interface). Check whether the dependency bump was intended before pinning around it — an unintended `@types/node` major arriving via a transitive install is itself worth knowing.

## Acceptance

`npx tsc -p packages/shared --noEmit` exits 0 **with a planted-error control proving the check is live**; `packages/shared` stays 709/709; and the reason it went unnoticed is closed — either the preflight gains a shared project type-check leg, or a ticket says explicitly why it should not.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-872-jwklocal-declare-the-jwk-shape-locally-instead-of-db11acf368af">Review in Linear</a></p>

