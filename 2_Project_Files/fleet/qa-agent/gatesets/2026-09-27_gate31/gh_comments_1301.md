--- comment 5852829283 by linear[bot] at 2026-09-27T05:03:56Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1349/ks730c-a1-reads-callsat-1-with-no-per-iteration-clear-the-same">KS-1349 ks730c A1 reads calls.at(-1) with no per-iteration clear — the same blindness KS1344 fixed in ks1341a</a></summary>
<p>

**BLUF:** `ks730c-adminconfig-500-never-answers-err-message.test.ts:119` **asserts** `expect(mockLoggerError.mock.calls.at(-1))` **inside a per-environment loop and never clears the mock, so a** `fail500` **that logged in one environment and not the others would leave the last call in place and the assertion would pass for every iteration.** This is the sibling of the defect KS1344 fixed in the ks1341a cell.

## Measured

On develop at `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`:

* `ks730c…test.ts:119` — `expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);`
* the file contains **no** `mockClear()` call at all.

The fix that landed for ks1341a (merged as `aa3827c975dc7cd79ae3ca1af871bfc86ee3718f`) clears the mock at the top of each iteration and asserts the whole call list:

```
mockLoggerError.mockClear();
...
expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
```

## Why it is worth doing

The A1 rows of ks730c are the REACHED half of an admin-surface security guard: they are what proves the thrown text is logged server-side rather than merely absent from the body. With the blindness present, a production-only logger would keep them green.

## Fix shape

Apply the KS1344 shape to ks730c's per-environment loop. The discriminating proof is the same 2x2: tamper the helper to log only under production, and the A1 rows must red at the fixed cell while staying green at the unfixed one.

## Not covered

The newer part-A rows added by #1294 already clear the logger per environment; this is about the pre-existing rows only. No other cell was audited for the same pattern.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1349-clear-the-logger-per-environment-in-the-ks730c-cell-and-assert-9c9fd80c4212">Review in Linear</a></p>

