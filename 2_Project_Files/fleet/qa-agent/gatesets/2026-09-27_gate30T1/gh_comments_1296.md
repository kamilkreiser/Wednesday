--- comment 5846549936 by linear[bot] at 2026-09-26T13:12:26Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1346/fail500-family-a-non-error-throw-is-logged-as-object-object-so-its">KS-1346 fail500 family: a non-Error throw is logged as [object Object], so its content is lost from the log</a></summary>
<p>

## BLUF

The `fail500` family helper logs a **non-Error** throw as `'[object Object]'`, so the thrown object's content is **lost from the log** — the body stays correctly constant, but the diagnosability the helper exists to preserve is gone. Measured at runtime by the gate29 probe on the routes #1290 converted.

## Detail

`fail500(res, context, err)` logs `err instanceof Error ? err.message : String(err)`. `String({...})` is `'[object Object]'`. So:

* an **Error** throw logs its message — correct;
* a **string** throw logs itself — correct;
* an **object** throw logs `[object Object]` — the content is gone.

At the merge-base neither kind leaked, because `err.message` on a non-Error is `undefined`; the helper is what made the log the only place the detail could live, and for objects it does not live there either.

**Fix shape:** in the family helper, log `err` itself, or `JSON.stringify` / `util.inspect` it for non-Errors.

**Family:** this is the same helper shape merged for KS730 in `routes/gdpr.ts` and `routes/systemErrors.ts`, so a fix belongs in all of them rather than in `webhooks.ts` alone.

## Also not pinned by the shipped cell (gate29 N-1290-3, measured: all green at head)

* (a) **non-Error throws** (string / object) on the three routes part B converted;
* (b) **rotate-secret throwing AFTER** `newSecret` **exists** — a rejected `$executeRaw` UPDATE, with the real `encryptField` and the key loaded. The gate probe drove this (S1) and measured the new secret **absent** from the 500 body and from every logger call, with a positive control — so today's behaviour is safe, but **no committed cell pins it**;
* (c) the **secret's absence from every log level** as an assertion.

## Done when

- ☐ the family helper preserves a non-Error throw's content in the log, in every file carrying the helper
- ☐ a cell pins a non-Error throw on at least one converted route
- ☐ a cell pins rotate-secret throwing after `newSecret` exists, asserting the secret is absent from the body and from every logger call

## Provenance

Gate29 report `2026-09-26-batch1290-g29/report.md` (sha256 `c3a273b3a582c088d3d088a3ac21a954c562ac8735cc679ec7979c12553f1e52`, measured by this seat), notes **N-1290-2** and **N-1290-3**; carries gate28's **N-1288-6**. Filed by the merging seat on that GO's instruction.

## Board search before filing

Literal match over **1335 issues (includeArchived) and 3780 comments**. Control token `b31nonce-9wq4tx-never-written` -> 0, while known terms returned hits, so the search discriminates in both directions. `[object Object]` -> 3 (KS-1341, which is this seat's own gate28 record that it was NOT filed; KS-744, a gateway/verificationLevel issue; KS-440 Done) — **none is this defect.**

Refs KS-1341
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1346-part-a-log-a-non-error-throw-from-systemerrors-fail500-with-4a5a2df235dc">Review in Linear</a></p>

