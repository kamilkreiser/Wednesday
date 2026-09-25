--- comment 5827185838 by linear[bot] at 2026-09-25T05:14:27Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1131/ks963-structural-cells-count-raw-text-a-comment-naming">KS-1131 ks963 structural cells count raw text — a comment naming consumeResetToken reds the cell, a deleted consume stays green, a non-await write stays green, the wallet slice is positional</a></summary>
<p>

## BLUF

PR #970 (KS-963, merged 2026-09-13) shipped three structural cells in `services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` that check `auth.ts` / `wallet.ts` for the shape KS-963 requires (the consume inside the `!user` branch; nothing consumed before the lookup; no write before the wallet lookup). The tier-1 gate measured that all three read RAW TEXT and so can be fooled in both directions — a false red on a comment, a false green on a deleted consume, a false green on a non-`await` write — while the product itself is correct on every one of the five pre-auth callers driven over real HTTP. One file, one test pass, one helper away from closing.

Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks963-970-ae274f7cb-tier1-r1/report.md` — FINDINGS F-A, F-B, F-C, P2; §5 (tampers Tg3/Tg4/Tg5, R12/R13); §6 (the legitimate-shape table). Line numbers are head `ae274f7cb` = develop after the squash.

## Items (one test pass)

1. **F-A — a false RED.** `:219` `expect(count(src.slice(expiryGuard, lookup), consumeFn)).toBe(1)` is a raw split; `braceBlock` skips comments and quotes only while counting braces and returns the raw slice, and this clause does not use it at all. MEASURED: Tg3 (`// NOTE: consumeResetToken …`) and Tg4 (`logger.debug('… consumeResetToken')`) in the gap before the lookup both red the reset cell with `expected 2 to be 1`. The cell exists to detect a hoisted consume, not a mention.
2. **F-B — a false GREEN.** `:206` `expect(guardBody).toContain(consumeFn)` over the raw brace-matched block. MEASURED (R13): replacing `await userRepo.consumeResetToken(tokenHash);` inside `if (!user) {` with `// consumeResetToken deliberately not called here any more` leaves 13/13 GREEN while the cell's title ("the reset-token consume is INSIDE the !user branch") is false of the file. Property 2 does not catch it (the count before the lookup is still 1).
3. **F-C — a false GREEN.** `:256` `/await\s+([A-Za-z_$][\w$.]*)\s*\(/g` — `void query('INSERT …')` (or a `.then` chain) before the wallet lookup is outside the allow-set's universe, so `['query']` still holds and the cell is green with partial state possible. MEASURED (Tg5).
4. **P2 — positional slice.** The wallet cell's body slice is `fn.indexOf('\n}\n')`; a trailing comment on the closing brace widens the slice to lines 183–277 without changing the verdict (R12). It would start mis-measuring only if a write were added between the function's true end and the next `\n}\n`.

## Fix shape (the gate's, not authored)

* Strip comments and string literals from a slice before counting — factor the skipper `braceBlock` already has into a `stripCommentsAndStrings(src)` helper — or count call-shaped matches (`/\bconsumeResetToken\s*\(/`).
* Allow-set every call to a write-capable name before the lookup regardless of `await` (`/\b(query|userRepo\.\w+)\s*\(/g`), or additionally assert `count(before, 'query(') === 1`.
* Brace-match the wallet function body with the file's own `braceBlock`, as the `auth.ts` cells do.
* **Regression cells that must RED after the fix, GREEN before:** Tg3 and Tg4 (a comment / a string in the gap stays green while T2 — the hoisted consume — stays red), R13 (the deleted consume reds), Tg5 (the non-`await` write reds). The report's tamper set is the oracle: `evidence/` under the report dir.

## Deliberately not here

* `getPlatformAdmin`'s swallow (F-6) — its own Low, filed alongside (same file, different class: product, not test efficacy).
* The RLS round-trip of the pre-change tenant-less UPDATE (NOT TESTED at the gate; on KS-963's closing comment); P3 (`/refresh` message, pre-existing) — a line on KS-963, no ticket.

## Dedupe, before filing (s205, 2026-09-13)

Literal census over 1,120 KS issues (692 archived) and 911 comments — `ks963-preauth-rethrow` → KS-963 (comment) · `stripCommentsAndStrings` 0 · `braceBlock` 0 · `consumeResetToken` 0 · `consumeEmailToken` → KS-963 (comment) · `structural cell` → KS-900 (a different guard, `packages/shared` parser factories), KS-963. No home; filed new. Controls fired (`persistedStatus == null` → KS-1073; `raw pg BIGINT` → KS-1129; nonsense → 0).

## Provenance

Tier-1 gate on PR #970 at `ae274f7cb`, 2026-09-13 (report path above): F-A, F-B, F-C (Minor, test efficacy), P2 (Polish). Wednesday's ADDENDUM to s205, 2026-09-13 16:57 AEST: ONE Low ticket, related KS-963, one file, one test pass. Filed by s205 (the merge seat for #970) at the per-PR order's step 1, before KS-963's archive.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1131-callshaped-ks963-helper-counts-consume-calls-not-mentions-ae1ff0be8b7e">Review in Linear</a></p>

