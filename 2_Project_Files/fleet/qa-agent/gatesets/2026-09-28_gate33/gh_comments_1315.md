--- comment 5857137435 by linear[bot] at 2026-09-27T15:20:55Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1220/ks839-cells-pin-padded-wildcards-with-ascii-separators-only-a-second">KS-1220 ks839 cells pin padded wildcards with ASCII separators only - a second tokenizer that differs from parseScopeString stays green</a></summary>
<p>

## BLUF

**Test-only:** no cell pins that `validateScopes` tokenizes allow-list entries with the SAME splitter the token route uses (`parseScopeString`). The ks839 cells use ASCII carriers only (space, tab, newline, comma). A second tokenizer that also handles those but differs on other whitespace, for example one that skips the non-ASCII characters JavaScript's `\s` matches, would stay green while a padded wildcard mints `*` again. Found by the tier-1 round-2 gate on PR #1026 (finding F-4), whose drafter's G-SECOND-REGEX tamper scored no red.

## Recommendation

Add ks839 cells for carriers built from non-ASCII and less common `\s` characters, each asserting the grant is `[]` with scope omitted and the minted token scopes are `[]`. Examples: `[' *']` (no-break space), `['\v*']` (vertical tab), `['　*']` (ideographic space). **Regression proof:** the drafter's G-SECOND-REGEX tamper (a tokenizer regex that differs from `parseScopeString`'s `/[\s,]+/`) must red. Test-only; not built here, routed to the local model. `Refs KS-839`.

## Detail

* **Today (develop after #1026):** `validateScopes` returns `[]` if any allow-list entry, split with `parseScopeString`, yields `*` (`services/auth/src/services/oauth.ts:353`). The ks839 R3/R4 carriers are `' *'`, `'* '`, `'\t*'`, `'*\n'`, `',*'`, `'openid *'`, `'openid,*'` and `['openid', ' *']`.
* **The gate measured the product closed across every code point** (0 leaks in 18,437,344 checks at head; develop before the fix: 27,157). So the gap is the pin, not the behaviour. A future edit that swaps the splitter would not be caught by the current cells.
* The look-alike controls (a zero-width-space star, a fullwidth star) stay literal and are already pinned by CONTROL 2. U+200B is not in JavaScript's `\s`.
* **Searched before filing** (Linear, literal matches, archived included): `parseScopeString` (0), `ks839` (1: KS-839 itself), `invalid_scope` (3: KS-839, KS-840, KS-822). No ticket covers this cell.
* **Source:** gate report `2026-09-17-ks839-1026-df97c0def-tier1-r2` (F-4), relayed in Wednesday's GO for #1026 (2026-09-17 10:51Z).
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1220-pin-padded-wildcards-carried-by-non-ascii-whitespace-in-ks839-7063d6b011e2">Review in Linear</a></p>

