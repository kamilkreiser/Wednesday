# KS-1121 R16B-EXACTID - Wednesday's task for Ornith: `credentialRepo.getById` resolves a credential by its EXACT id or not at all - the DB `LIKE '%id%'` fallback and the in-memory `includes()` scan are DELETED (the KS-1020 / #966 rule, Kam's 2026-09-16 07:01 ruling option a), the pinned partial-match cell in the EXISTING `credentialRepo.test.ts` is REPLACED by three RED cells (code_patch, VITEST, THREE product hunks - numbered, ascending, each ONE group of context / minus / plus / context - plus ONE test hunk that MODIFIES the existing file IN PLACE, `test_file=` pin; re-brief of the STALE READY_KS-1121 at develop 3bad652d1, written 13:47:59 AEST on 2026-09-22 by Wednesday's feed12 drafter from the two files read WHOLE at the tip: `credentialRepo.ts` 265 lines, `credentialRepo.test.ts` 127 lines)
Tip: `3bad652d17cf111c1e2e1bed1ae7686894637487`
Runner: `vitest`

## Premises (measured by the feed12 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1121_ornith35b-q4_VITEST-MODIFYINPLACE-REANCHORED-PASS-7of7_2026-09-16.diff.md` (Ornith PASS 7/7 at develop 48e65c435 on the r2 retry, apply_mode REANCHORED; its test hunk is corrupt at the tip - it closes the third cell with `  }` where the file has `  });`, so neither strict nor `--recount` applies it). Same behaviour here, every hunk RE-CUT from the tip; the test rewritten under the `+`-line rule (no `\u` escapes, no template literal, ASCII titles declared under `## Red cells`).
- BOTH files are UNCHANGED since 2026-04-28 (`git log -1` on each at the tip: `1305bbda9`), so every line number below is the tip's (offset 0): `:73` the JSDoc line, `:80`-`:85` the exact SELECT, `:86` blank, `:87`-`:92` the LIKE fallback, `:98`-`:107` the memory fallback with its `includes()` loop at `:102`-`:106`; the test's pinned cell `:59`-`:64` between the blank `:58` and the blank `:65`. `revoke()` (`:231`-`:265`) calls `getById(id)` at `:235` and is NOT edited - it inherits the exact lookup, which is what RED cell B pins.
- The shape is #966's, byte for byte in spirit: `routes/presentations.ts:118-131` at the tip keeps `const exact = ...get(id); if (exact) return exact; return undefined;` after deleting the scan - so E3 here is a pure DELETION of the loop (`:101`-`:106`), and `:99`, `:100`, `:107` stay as context. E2 is a pure DELETION of the LIKE block (`:86`-`:92`). Only E1 (the JSDoc) ADDS lines - 2 `+` lines in the whole product side. `let result` at `:81` stays `let` (never reassigned after E2; tsc does not object and vc-issuer has no eslint config at the tip).
- The test file EXISTS at the tip and is MODIFIED IN PLACE (`test_file=` pin; its full content is in `files[...]`): ONE hunk replaces `:58`-`:63` (the blank line and the first five lines of the pinned cell `getById supports partial-match substring lookup` - its title, `const c`, `await repo.store(c)`, `const got`, `expect(got?.id)`) with three RED cells; the pinned cell's closing `  });` at `:64` STAYS as the hunk's trailing context and closes RED cell C, so no `+` line repeats a `-` line; the file's other nine cells are untouched and green on both trees. No `import` is added: RED cell C reaches the mocked `../db` through `await import('../db')` (the shape `ks1020-presentation-lookup-exact-or-404.test.ts:64` already uses), so the file's import block (`:6`-`:19`) is not in the diff.
- Why the hunks are cut where they are: NO blank line is asked of you as CONTEXT anywhere (the blanks `:86`, `:101` are `-` lines inside E2 / E3; the blank `:58` is the test hunk's first `-` line and comes back as its first `+` line; `:65` is outside the hunk). E2's trailing context is the single line `:93`; E3's leading context is `:98`-`:100` and its trailing context `:107`-`:108`; E1's context is `:72` and `:74`-`:75`. Strict `git apply --check` rc 0 measured on the four hunks at the tip (the golden PASSes the real checker in the precheck clone).
- Every `+` line of both fences is ASCII-only, backslash-free and carries NO double-quote character (2 product lines, 30 test lines, asserted by the writer script); the test's `%` and `_` fragments are single-quoted strings; the two regexes `/SELECT credential/i` and `/ LIKE /i` carry no backslash.
- Collision check: vc-issuer is in NEITHER round-19 lane (Seat B 19th = originate/anchoring/auth/kyc/security/packages/shared/systemTest; Seat C 19th = scripts/docs/api-gateway; `seat_grep.log`); no held READY of 2026-09-2[0-2] touches `credentialRepo.ts`, `credentialRepo.test.ts` or any vc-issuer path (`held_pool_seat_grep.log`, positive control security/src/index.ts = 6). Ticket KS-1121: Backlog, not archived, no PR attached (board read 13:41:52).

## What is wrong (one paragraph)
`getById(id)` (`Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts:75`-`:108`) is the ONLY lookup behind `GET /api/credentials/:id` (`routes/credentials.ts:268`) and `POST /api/credentials/:id/revoke` (`:289`, through `revoke()` at `credentialRepo.ts:235`). When the exact DB match (`:81`-`:85`) finds nothing it runs `WHERE id LIKE '%<id>%' LIMIT 1` (`:87`-`:92`), and when the exact memory get (`:99`-`:100`) finds nothing it scans every stored credential for `key.includes(id) || value.id.includes(id)` (`:102`-`:106`) - so an id that names nothing (`abc`, `1234`, `%`, `_`) resolves to an ARBITRARY stored credential, and a revoke on a fragment revokes an arbitrary row. #966 (KS-1020) deleted the same two fallbacks for presentations; Kam ruled (2026-09-16 07:01, option a) to do exactly that here and flip the one pinned test. The fix: delete the LIKE block and the `includes()` loop, say so in the JSDoc; `getById` is then exact-or-undefined and the routes' existing `undefined` branches answer 404 / refuse. NOT in this task: `revoke()` itself, `getByHash`, `list`, `store`, the routes, ownership checks (KS-1116).

## The exact change - THREE EDITS in the product file (three hunks, NUMBERED, in ASCENDING line order; copy all three headers)
THE ORDER IS THE TASK. Hunk 1 at `:72` comes BEFORE hunk 2 at `:83`, which comes BEFORE hunk 3 at `:98`; emit them in this order, each under its own `@@` header, never merged into one hunk. Inside EVERY hunk the lines run in exactly ONE sequence: context lines, then `-` lines, then `+` lines, then context lines - never a `+` line before a `-` line, never context between a `-` and a `+`. Hunks 2 and 3 have NO `+` line at all (pure deletions): do not add a replacement line, do not re-add a deleted line as a `+`.
E1 (hunk 1, header `@@ -72,4 +72,5 @@`) - the JSDoc sentence at `:73` (the one `-` line) is REPLACED by two lines; leading context `:72` (`/**`), trailing context `:74`-`:75` (` */` and the `export async function getById` line). Old side 4 lines, new side 5.
E2 (hunk 2, header `@@ -83,11 +84,4 @@`) - a PURE DELETION of the LIKE fallback: the seven `-` lines are the tip's `:86` (blank - written as a lone `-`), `:87` `// Partial match`, `:88`-`:91` the LIKE query and its `%id%` binding, `:92` the second `if (result.rows.length > 0) return ...;`. Leading context `:83`-`:85` (`[id],`, `);`, the FIRST `if (result.rows.length > 0) return ...;` - which STAYS), trailing context `:93` (`} catch (err: any) {`). Old side 11, new side 4; new-side start 84 = 83 + the 1 line E1 adds.
E3 (hunk 3, header `@@ -98,11 +92,5 @@`) - a PURE DELETION of the memory scan: the six `-` lines are the tip's `:101` (blank - a lone `-`), `:102`-`:106` (the `for` loop over `memoryStore.entries()` with its `includes()` test, five lines). Leading context `:98`-`:100` (`// Fall back to memory`, `const exact = memoryStore.get(id);`, `if (exact) return exact;` - all three STAY), trailing context `:107`-`:108` (`return undefined;` and the function's closing `}` - both STAY). Old side 11, new side 5; new-side start 92 = 98 + 1 - 7.
```
@@ -72,4 +72,5 @@
 /**
- * Retrieve a credential by its full ID, or by a partial-match substring.
+ * Retrieve a credential by its EXACT id only (KS-1121; the KS-1020 / #966 rule): a fragment resolves
+ * nothing. The LIKE fallback and the includes() scan are deleted.
  */
 export async function getById(id: string): Promise<SecuuraCredential | undefined> {
@@ -83,11 +84,4 @@
         [id],
       );
       if (result.rows.length > 0) return result.rows[0].credential;
-
-      // Partial match
-      result = await query<{ credential: SecuuraCredential }>(
-        'SELECT credential FROM vc_credentials_store WHERE id LIKE $1 LIMIT 1',
-        [`%${id}%`],
-      );
-      if (result.rows.length > 0) return result.rows[0].credential;
     } catch (err: any) {
@@ -98,11 +92,5 @@
   // Fall back to memory
   const exact = memoryStore.get(id);
   if (exact) return exact;
-
-  for (const [key, value] of memoryStore.entries()) {
-    if (key.includes(id) || value.id.includes(id)) {
-      return value;
-    }
-  }
   return undefined;
 }
```
Copy every `+` line byte for byte (there are exactly 2, both in E1); every `-` line is the tip's line exactly (a blank tip line is a lone `-`); every context line keeps its leading space. The `%${id}%` binding line `:90` and the backtick-bearing lines are `-` lines: copy them exactly as printed, including their backticks and `$`. Do NOT touch `:81` (`let result` stays), `:82`, `:85`, `:99`, `:100`, `:107`. No `+` line carries a double quote, a backslash or a non-ASCII character.

## THIS IS VITEST
`repo.test_runner` begins with `vitest`. `describe/it/expect/vi/beforeEach` are imported from `'vitest'` at `:6` of the test file already; `vi.mock('../db')` and `vi.mock('../utils/logger')` at `:10`-`:17` are already there and hoisted. Use `vi.mocked(...)` on the mocked module's functions; NO `jest.*`.

## The test - the EXISTING credentialRepo file MODIFIED IN PLACE (ONE hunk), not a new file
File: `Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts`
MODIFY: `--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts` then `+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts` then the ONE hunk below with its header exactly as printed (`@@ -55,10 +55,34 @@`): leading context `:55`-`:57` (the last two `expect` lines of the round-trip cell and its `});`), then the 6 `-` lines (`:58` blank - a lone `-` - and `:59`-`:63`, the pinned cell's title and its first four body lines), then the 30 `+` lines (a blank, cell A whole, a blank, cell B whole, a blank, cell C WITHOUT its closing line - the blank `+` lines are lone `+` and part of the fence), then the ONE trailing context line `:64` (`  });`), which is the old cell's closing line and now closes RED cell C. Cell C's last `+` line is `    }` (the end of its `finally`); the `  });` after it is CONTEXT (leading space), not a `+`. Do NOT touch any other line of the file; do NOT add an import; do NOT use `--- /dev/null`.
```
@@ -55,10 +55,34 @@
     expect(got).toBeDefined();
     expect(got!.id).toBe(c.id);
   });
-
-  it('getById supports partial-match substring lookup', async () => {
-    const c = makeCredential({ id: 'urn:vc:abcdef-1234' });
-    await repo.store(c);
-    const got = await repo.getById('abcdef');
-    expect(got?.id).toBe('urn:vc:abcdef-1234');
+
+  it('RED KS-1121 A: getById resolves a credential by its EXACT id only - every fragment is undefined', async () => {
+    const stored = makeCredential({ id: 'urn:vc:abcdef-1234' });
+    await repo.store(stored);
+    expect((await repo.getById(stored.id))?.id).toBe('urn:vc:abcdef-1234');
+    for (const fragment of ['abcdef', 'urn:vc:abc', '1234', 'bcde', 'urn:vc:abcdef-123', '%', '_']) {
+      expect(await repo.getById(fragment), 'fragment ' + fragment).toBeUndefined();
+    }
+  });
+
+  it('RED KS-1121 B: revoke on a fragment returns undefined and mutates nothing', async () => {
+    const target = makeCredential({ id: 'urn:vc:revoke-target-5678' });
+    await repo.store(target);
+    expect(await repo.revoke('revoke-target', 'fragment')).toBeUndefined();
+    expect((await repo.getById(target.id))?.credentialStatus?.revoked).toBe(false);
+  });
+
+  it('RED KS-1121 C: DB path - an unknown id costs exactly ONE lookup query, and it is never a LIKE', async () => {
+    const db = await import('../db');
+    vi.mocked(db.isDbAvailable).mockReturnValue(true);
+    vi.mocked(db.query).mockResolvedValue({ rows: [] } as any);
+    try {
+      expect(await repo.getById('abcdef')).toBeUndefined();
+      const lookups = vi.mocked(db.query).mock.calls.map((call) => String(call[0])).filter((sql) => /SELECT credential/i.test(sql));
+      expect(lookups).toHaveLength(1);
+      expect(lookups[0]).not.toMatch(/ LIKE /i);
+    } finally {
+      vi.mocked(db.isDbAvailable).mockReturnValue(false);
+      vi.mocked(db.query).mockReset();
+    }
   });
```
LINE DISCIPLINE (the 13:5x run FAILED on exactly this, twice): the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string - DECODE them. Every one of the 30 `+` lines above is its OWN physical line of your diff, each starting with its own `+`; NEVER join two lines with a backslash-n pair - a `+` line that carries a backslash is a FAIL by the hygiene rule, and the previous run wrote all 30 test lines as ONE line joined by backslash-n, which the checker read as a placeholder. The blank `+` lines are a lone `+` on their own line. The same holds for the product hunks: every context line is ONE leading space plus the tip's own indentation (`:72` `/**` is at column 0, so its context line is ` /**` - one space, not three; `:83` `[id],` has 8 spaces at the tip, so its context line has 9); the previous run indented every product context line by two extra spaces.
Cells (every NEW cell RED, nothing optional; the file's other nine cells are untouched CONTROLS, green on both trees):
- RED `it('RED KS-1121 A: getById resolves a credential by its EXACT id only - every fragment is undefined')` - stores `urn:vc:abcdef-1234`, pins the exact get, then every fragment (`abcdef`, `urn:vc:abc`, `1234`, `bcde`, `urn:vc:abcdef-123`, `%`, `_`) must be `undefined`. At the tip the memory scan (`:102`-`:106`) answers the stored credential for `abcdef` - the red, by assertion (`toBeUndefined`); after E3 every fragment is `undefined`.
- RED `it('RED KS-1121 B: revoke on a fragment returns undefined and mutates nothing')` - stores `urn:vc:revoke-target-5678`; `revoke('revoke-target', 'fragment')` must be `undefined` and the stored credential's `credentialStatus.revoked` must stay `false`. At the tip `revoke()` resolves the fragment through the scan and revokes the row (the red, by assertion); after E3 `getById` answers `undefined` and `revoke()` returns at `:236`.
- RED `it('RED KS-1121 C: DB path - an unknown id costs exactly ONE lookup query, and it is never a LIKE')` - flips the mocked `isDbAvailable` to `true` and `query` to resolve `{ rows: [] }` (through `await import('../db')`, the same mocked module), asks for `abcdef`, and pins: `undefined`, exactly ONE `SELECT credential` query issued, and that query is not a `LIKE`. At the tip the DB path issues the exact SELECT then the LIKE SELECT and, both empty, falls to the memory scan which answers cell A's credential - the red, by assertion on the first `expect`; after E2 + E3 one exact SELECT, then `memoryStore.get('abcdef')` = `undefined`. The `finally` restores `isDbAvailable` to `false` and resets `query`, so the cells after it run in memory-only mode exactly as before.

## Red cells
- RED KS-1121 A: getById resolves a credential by its EXACT id only - every fragment is undefined
- RED KS-1121 B: revoke on a fragment returns undefined and mutates nothing
- RED KS-1121 C: DB path - an unknown id costs exactly ONE lookup query, and it is never a LIKE

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:73` - **must change**: ` * Retrieve a credential by its full ID, or by a partial-match substring.` - E1's one `-` line (the JSDoc sentence)
* `:87` - **must change**: `      // Partial match` - E2 (deleted)
* `:88` - **must change**: `      result = await query<{ credential: SecuuraCredential }>(` - E2 (deleted; the second query)
* `:89` - **must change**: `        'SELECT credential FROM vc_credentials_store WHERE id LIKE $1 LIMIT 1',` - E2 (deleted; the LIKE statement)
* `:102` - **must change**: `  for (const [key, value] of memoryStore.entries()) {` - E3 (deleted; the scan)
* `:103` - **must change**: `    if (key.includes(id) || value.id.includes(id)) {` - E3 (deleted; the includes() test)
* `:72` - (correct) `/**` - stays (E1's leading context)
* `:75` - (correct) `export async function getById(id: string): Promise<SecuuraCredential | undefined> {` - stays (E1's last trailing context line; the signature does not change)
* `:81` - (correct) `      let result = await query<{ credential: SecuuraCredential }>(` - stays (`let` stays `let`; not in any hunk)
* `:82` - (correct) `        'SELECT credential FROM vc_credentials_store WHERE id = $1',` - stays (the exact SELECT; not in any hunk; its `:85` return line - the FIRST of the two identical `if (result.rows.length > 0)` lines - is E2's last leading context line and STAYS; the SECOND, `:92`, is deleted)
* `:93` - (correct) `    } catch (err: any) {` - stays (E2's trailing context)
* `:98` - (correct) `  // Fall back to memory` - stays (E3's first leading context line)
* `:99` - (correct) `  const exact = memoryStore.get(id);` - stays (E3's leading context)
* `:100` - (correct) `  if (exact) return exact;` - stays (E3's last leading context line)
* `:107` - (correct) `  return undefined;` - stays (E3's first trailing context line)
* `:235` - (correct) `  const credential = await getById(id);` - stays (`revoke()` inherits the exact lookup; not in any hunk)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` / `+++ b/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` with the E1, E2 and E3 hunks IN THAT ORDER (headers `@@ -72,4 +72,5 @@`, `@@ -83,11 +84,4 @@`, `@@ -98,11 +92,5 @@`), then `--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts` / `+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts` with the one test hunk (header `@@ -55,10 +55,34 @@`); paths repo-rooted (`Blockchain/Dev/...`, never `services/...`); no double quote, no backslash, no non-ASCII character in any `+` line; every `+` line's `(` / `)` and `[` / `]` counts are EXACTLY the fence's - one extra `)` on a `+` line is a FAIL (two of today's model runs failed on exactly that); every context line keeps its leading space; a deleted blank line is a lone `-` and an added blank line a lone `+`; inside every hunk the order is context, `-`, `+`, context; the cell titles EXACTLY as listed; EVERY diff line on its own physical line - never a backslash-n pair joining lines (decode the INPUT JSON's escapes; the 13:5x run failed twice on this); product context lines carry exactly one leading space plus the tip's indentation.
