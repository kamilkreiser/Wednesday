# KS-839 (ASCII_PROXY proof brief) - Wednesday's task for Ornith, VITEST, **PRODUCT FIX + NEW TEST FILE**

PROOF ONLY, NOT QUEUED (2026-09-17 15:5x). A Claude seat owns KS-839 by hand; this brief exists to prove the harness's
ascii_proxy mechanism end to end through the real checker. It is `night/briefs/KS-839.md` (written 14:09 from origin develop
`d7e95cd9f153e9036ed77935a73c93504fa6e3dc`, premises P1-P13 there) with three changes: the `## Where` list is LINE-KEYED, the
em-dash line :353 is declared `ascii_proxy U+2014=--`, and every non-ASCII character is gone from this text.

## THE MODE - read this twice

Your diff contains EXACTLY TWO files, in this order:
1. `Blockchain/Dev/services/auth/src/services/oauth.ts` - ONE hunk, `--- a/...` / `+++ b/...`, carrying the ONE line edit of
   `## The exact change`.
2. The NEW test file `Blockchain/Dev/services/auth/src/__tests__/ks839-security-an-allowedscopes-of-bypasses-the.test.ts`
   - `--- /dev/null` then `+++ b/...`, one `@@ -0,0 +1,52 @@` hunk, every line `+`.

Do NOT modify `ks466-oauth-tenant-guc.test.ts` (it is the reference; ignore it). Do NOT touch `routes/oauth.ts`,
`auth.openapi.ts`, `docs/openapi/secuura-api.yaml` or any other file. The checker applies the test ALONE at the untouched tip and
expects the two red cells RED by assertion and the control GREEN, then applies your product hunk and expects every cell GREEN,
the whole services/auth suite with no new red, and `tsc --noEmit` rc 0.

## What is wrong (one paragraph)

`validateScopes(requested, allowed)` (`:352-355`) decides which scopes an OAuth app is granted. Its first line (`:353`) returns
the request UNFILTERED whenever the app's allow-list contains the wildcard `'*'`. So an app registered with `allowedScopes`
`['*']` is granted any scope it names, including one nobody registered (`admin:everything`) and the wildcard itself, and the
authorize resolver passes the allow-list itself as the request when `scope` is omitted, so an omitted scope grants `'*'` too.
The grant is stored on the authorization code and minted into the token, and the gateway scope gate lets a token holding `'*'`
through every scope check. **This task (Wednesday's default ruling):** an allow-list that contains the wildcard grants NOTHING.
Line `:353` returns an empty array instead of the request. Nothing else changes: `:354` still filters every allow-list that
does not contain the wildcard, and the resolver's existing `invalid_scope` refusal then answers any wildcard app that names a
scope.

## Where (line-keyed - every **must change** line must appear as a '-' line AT ITS NUMBER; the (correct) ones stay)

- `:353` - **`  if (allowed.includes('*')) return requested; // Wildcard -- all scopes` - becomes `  if (allowed.includes('*')) return []; // KS-839: a wildcard grants nothing` (EDIT 1).** ascii_proxy U+2014=--
- `:352` - (correct) `export function validateScopes(requested: string[], allowed: string[]): string[] {` - stays.
- `:354` - (correct) `  return requested.filter(s => allowed.includes(s));` - the named-scope filter. Stays.

## The exact change - ONE edit in `Blockchain/Dev/services/auth/src/services/oauth.ts`, ONE hunk

The fence lists the `-` and `+` lines of the hunk. There are no context lines in the fence; the context is named here, and every
context line is copied byte for byte with its leading space. The `-` line occurs exactly once in the file.

**Line 353 of the file carries one character this task spells as TWO HYPHENS: write the `-` line EXACTLY as the fence shows
it, with `--` between `Wildcard` and `all scopes`.** Do not copy that line from the file content in files[...]; copy it from the
fence below. The checker restores the file's real character at line 353 before it applies your diff, but only when your `-`
line is exactly this text and your hunk's context lines put it at line 353. The `+` line is plain ASCII with no backslash.

**HUNK 1 - EDIT 1, line 353, header `@@ -350,7 +350,7 @@`.** Context above: line 350 (a line of `// ` followed by 77 `=`
characters, indent 0), line 351 (a blank line), line 352 (`export function validateScopes(requested: string[], allowed: string[]): string[] {`,
indent 0). Context below: line 354 (`  return requested.filter(s => allowed.includes(s));`, indent 2 spaces), line 355 (`}`,
indent 0), line 356 (a blank line). One line out, one in. **The `+` line's indent is exactly 2 spaces**, the same as the `-`
line it replaces. Line 354 STAYS: it is context, never a `-` line.

```
-  if (allowed.includes('*')) return requested; // Wildcard -- all scopes
+  if (allowed.includes('*')) return []; // KS-839: a wildcard grants nothing
```

Touch nothing else in the file. Do not change `:354`, `AVAILABLE_SCOPES` (`:57-67`) or `parseScopeString` (`:357-360`).

## The test - CREATE THE NEW FILE `Blockchain/Dev/services/auth/src/__tests__/ks839-security-an-allowedscopes-of-bypasses-the.test.ts`

**Harness:** `vitest run` inside `Blockchain/Dev/services/auth` (`package.json` scripts.test is `vitest`; setupFiles
`./vitest.setup.ts`). To run this file alone: `npx vitest run src/__tests__/ks839-security-an-allowedscopes-of-bypasses-the.test.ts`.

The file mocks `../db` (every query answers no rows) and `../utils/logger`, exactly as the reference test does, then imports the
REAL `validateScopes` from `../services/oauth` and calls it directly. No server, no socket, no database.

**Reproduce the body below EXACTLY as written.** It is 52 lines. Do not shorten it, do not replace any part with a comment, do
not invent a helper, do not rename a variable, do not collapse the cells into a loop or an `it.each`. Every name a cell reads
(`EXPECTED_CELLS`, `CELLS_RUN`, `WILDCARD_APP`, `MIXED_APP`, `NAMED_APP`, and the imported `validateScopes`) is declared ABOVE
the first cell. **The file contains no backslash, no template literal, no dollar sign, no double quote and no non-ASCII
character; keep it that way.** Every string is single-quoted. The comments contain no quote character of any kind.

**Indentation, stated line by line (2 spaces per level, spaces only, no tabs):** the header comment lines ` * ...` start with ONE
space. Inside each `vi.mock(` factory the property line (`query:` or `logger:`) is indented 2 spaces. Each `it(` line is indented
2 spaces. Inside a cell, `CELLS_RUN += 1;` and each `expect(` line are indented 4 spaces; the three `validateScopes(` rows inside
`expect([` are indented 6 spaces; the `]).toEqual(` line is indented 4 spaces; the cell's closing `});` is indented 2 spaces. The
final `});` closing `describe` has no indent.

```ts
/**
 * KS-839: an OAuth app whose allowedScopes holds the wildcard is granted
 * nothing, instead of everything it asks for.
 *
 * validateScopes returned the request unfiltered when the allow-list held the
 * wildcard, so an unknown scope, or the wildcard itself, was granted and stored
 * on the authorization code. The authorize resolver passes the allow-list as
 * the request when scope is omitted, so that path granted the wildcard too.
 */
import { describe, it, expect, vi } from 'vitest';

vi.mock('../db', () => ({
  query: vi.fn(async () => ({ rows: [], rowCount: 0 })),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
}));

import { validateScopes } from '../services/oauth';

const EXPECTED_CELLS = 3;
let CELLS_RUN = 0;
const WILDCARD_APP = ['*'];
const MIXED_APP = ['documents:read', '*'];
const NAMED_APP = ['documents:read', 'openid'];

describe('KS-839 - an allow-list holding the wildcard grants nothing', () => {
  it('KS-839 R1 - a wildcard app asking for a scope nobody registered is granted nothing', () => {
    CELLS_RUN += 1;
    expect(validateScopes(['admin:everything'], WILDCARD_APP)).toEqual([]);
  });
  it('KS-839 R2 - the wildcard itself is never granted, asked for, defaulted or mixed in', () => {
    CELLS_RUN += 1;
    expect([
      validateScopes(['*'], WILDCARD_APP),
      validateScopes(WILDCARD_APP, WILDCARD_APP),
      validateScopes(['documents:read', '*'], MIXED_APP),
    ]).toEqual([[], [], []]);
  });
  it('KS-839 CONTROL - an allow-list without the wildcard still filters to what it names', () => {
    CELLS_RUN += 1;
    expect([
      validateScopes(['documents:read', 'admin:everything', '*'], NAMED_APP),
      validateScopes(['openid'], NAMED_APP),
      validateScopes([], NAMED_APP),
    ]).toEqual([['documents:read'], ['openid'], []]);
  });
  it('KS-839 COMPLETENESS - every graded cell above actually ran', () => {
    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
  });
});
```

Why each cell is what it is:
- **R1 (red):** a wildcard app naming a scope nobody registered. At the untouched tip it FAILS by assertion:
  `expected [ 'admin:everything' ] to deeply equal []`. After the edit it passes.
- **R2 (red):** the wildcard itself is never granted: asked for (`['*']`), defaulted (the resolver passes the allow-list as the
  request when `scope` is omitted, so `validateScopes(WILDCARD_APP, WILDCARD_APP)` is exactly that call), or mixed into a
  named allow-list. At the tip it FAILS by assertion: `expected [ [ '*' ], [ '*' ], ...(1) ] to deeply equal [ [], [], [] ]`. A fix
  that only DELETES line 353 turns R1 green and leaves R2 red, because `'*'` then matches itself in the filter.
- **CONTROL (green before and after):** an allow-list without the wildcard filters to exactly what it names, drops an unknown
  scope and a requested `'*'`, and grants nothing for an empty request. It proves the harness reaches the real function and
  that the fix leaves `:354` alone.
- **COMPLETENESS:** asserts `CELLS_RUN === EXPECTED_CELLS` (3), so a file that summarises instead of transcribing cannot pass.

### READ THIS BEFORE YOU WRITE THE FILE

- The file you write is **exactly 52 lines**. If your output has fewer than 49 lines you have dropped something.
- Write every line of the fenced block above, verbatim, from the opening `/**` to the final `});`.
- Do **NOT** write "rest of the file unchanged", "// remaining tests omitted", `...`, or any other placeholder.
- All four `it(` blocks must be present, in order: `R1`, `R2`, `CONTROL`, `COMPLETENESS`. Three of them contain the line
  `CELLS_RUN += 1;`.

## Red cells

- KS-839 R1 - a wildcard app asking for a scope nobody registered is granted nothing
- KS-839 R2 - the wildcard itself is never granted, asked for, defaulted or mixed in

## Output

Exactly ONE ```diff block containing, in this order: the `oauth.ts` section
(`--- a/Blockchain/Dev/services/auth/src/services/oauth.ts` / `+++ b/Blockchain/Dev/services/auth/src/services/oauth.ts`, the ONE
hunk `@@ -350,7 +350,7 @@`), then the new test file (`--- /dev/null` with NO leading space, then
`+++ b/Blockchain/Dev/services/auth/src/__tests__/ks839-security-an-allowedscopes-of-bypasses-the.test.ts`, `@@ -0,0 +1,52 @@`).
Blank context lines keep their leading space; correct hunk counts. No other file. No prose outside the block.

## Notes (not for the model)

- Build pins (as `night/briefs/KS-839.md`): `product=Blockchain/Dev/services/auth/src/services/oauth.ts ref=services/auth/src/__tests__/ks466-oauth-tenant-guc.test.ts line=353 ctx=65536`, built as ticket id `KS-839-proxy` so this file is the brief.
- NOT queued. The proof (golden PASS, wrong-line FAIL, one-character FAIL) is recorded in the IMPROVEMENTS row of 2026-09-17 for the ascii_proxy mechanism.
