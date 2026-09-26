--- comment 5846285814 by linear[bot] at 2026-09-26T12:30:51Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1344/ks1341a-a1-the-reached-assertion-reads-callsat-1-with-no-per-iteration">KS-1344 ks1341a A1: the REACHED assertion reads calls.at(-1) with no per-iteration clear, so a fail500 that logs only in production stays green</a></summary>
<p>

## BLUF

The `ks1341a` A1 cell's "REACHED" assertion does not pin *reached* **per environment**, so a `fail500` that logs only under `NODE_ENV=production` would keep the cell 8/8 green. Measured at runtime by the gate28 probe, and re-read at source by the seat that wrote the cell.

## The mechanism

`src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` clears its mocks with `beforeEach(() => jest.clearAllMocks())` — **once per cell**. A1 then loops `production -> development -> test -> unset` **inside a single** `it()` and asserts:

```
expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
```

`calls` accumulates across the four iterations and `.at(-1)` reads only the last call. So the production iteration's call satisfies iterations 2-4, and the assertion cannot distinguish "logged in every environment" from "logged once, in the first". A2 checks production only, so it does not close the gap either.

The **body** assertions in the same loop are unaffected — they are still per environment. This is about the log-side "reached" claim only.

## Fix shape

* `mockLoggerError.mockClear()` at the top of each loop iteration, and
* assert the whole call list per environment: `expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]])`.

## Regression cell

A tamper making the helper log only under production must **red A1 for development, test and unset** — the gate's R3 probe reds 18 cells under exactly that tamper today, and A1 is not among them.

## Why it is filed rather than fixed here

PR #1288 (merged `a2a2b4c50d64`) was raised byte-identical to a reviewed local-model patch on an explicit ruling, so the cell was not edited after the gate. The fix also belongs with parts B and C, which convert the remaining five sites and will inherit the same cell shape.

## Board search before filing

Literal match over **1332 issues (includeArchived) and 3776 comments**: `calls.at(-1)` -> 0, `mockLoggerError` -> 0, `ks1341a-webhooks-500` -> 0. Control token `b31nonce-zqx7vk-never-written` -> 0; the same scan finds `MULTI-TENANCY.md` in 2 issues, so it is not blind.

## Provenance

Gate28 report `2026-09-26-batch1286-g28/report.md` (sha256 `760c86711baee5a5…`), note N-1288-2, MEASURED AT RUNTIME. Re-read at source and confirmed by the cell's author.

Refs KS-1341
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1344-clear-the-logger-per-environment-in-the-ks1341a-cell-and-0ec8773ce1ef">Review in Linear</a></p>

