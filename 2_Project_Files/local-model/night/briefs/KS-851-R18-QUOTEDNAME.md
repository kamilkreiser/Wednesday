# KS-851 R18-QUOTEDNAME ADD ONE CELL TO THE KS-386 WRITE-PATH GUARD — a payload write spelled `"svc_kyc_images"` or `public.svc_kyc_images` is a write path the existing matcher cannot see — item G-4 of the KS-386 round-2 re-gate — Wednesday's task for Ornith, TEST_ONLY, **ONE existing vitest suite, ONE pure-insertion hunk, no product file** (written 06:20:51 AEST on 2026-09-23 by the feed18 drafter)

File: `Blockchain/Dev/services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts`
Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`
Runner: `vitest`

Written from develop `2bc5ccf63b8c40911afb568b03cace066238ffcf` (`git ls-remote origin refs/heads/develop` at 06:1x, read verbs only; the object is in the local store, no fetch). The suite at that tip is **221 lines**, read whole; its full content is in `files[...]` of your input. The product it judges is `Blockchain/Dev/services/kyc/src/index.ts` (1261 lines), whose ONE write path is `dbSaveImage` (`:295-:328`) with its INSERT at `:306` and its two `DELETE FROM` erasure statements elsewhere.

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the suite above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as on the `File:` line). You never touch `services/kyc/src/index.ts` or any other file: **no product behaviour changes; ONE cell is ADDED and nothing existing is edited.**

## What the change does (one paragraph)

`writeStatements` (`:99-:102`) is the reader behind the suite's strongest cell at `:149-:162`, which asserts the whole write-path list equals `['INSERT INTO SVC_KYC_IMAGES']`. Its matcher at `:100` is `/(INSERT\s+INTO|UPDATE)\s+svc_kyc_images/gi` — it requires the table name **bare and unquoted**, so a second real payload writer spelled `INSERT INTO "svc_kyc_images" (...)` or `UPDATE public.svc_kyc_images SET ...` is invisible to it and every cell in the file stays green while `data` starts being stored again. That is KS-851 item G-4, MEASURED by the re-gate: both spellings were planted in `index.ts` as real payload writes and the suite read **0 failed / 26** each time, while an `UPDATE` split across lines WAS caught — so the blindness is specifically about how the table NAME is spelled, not about whitespace. This diff adds ONE cell that runs its own spelling-tolerant matcher over the same `SRC` and asserts the same single write path. It deliberately does NOT edit `writeStatements`, because `:161`'s expectation and three sibling readers are written against the bare-name form; the new cell is a second, independent reading of the same file, and it is the one that reds when a quoted or schema-qualified writer appears. Nothing else in the suite changes: `stripComments` (`:74-:79`), `insertColumnLists` (`:91-:96`), `writeStatements` (`:99-:102`) and every cell at `:105-:220` are untouched.

## The exact change — ONE hunk in the suite

A PURE INSERTION of 5 `+` lines between `:220` (`  });`, the close of the last CONTROL cell; leading context) and `:221` (`});`, the close of the `describe` opened at `:104` and the final line of the file; trailing context). `:219` is the third context line. All three anchors are non-blank; none of them is blank, so the fence carries no blank context line, and the hunk has trailing context. The new cell sits inside that `describe`, so `stripComments` and `SRC` are in scope exactly as they are for the cells above it.

Every `+` line is ASCII only and carries **NO backslash (0, counted by the writer), NO backtick (0) and NO `$` (0)** — the character classes are written `[ ]` and `[.]` rather than `\s` and `\.` for exactly that reason, and the match is upper-cased without a whitespace normaliser because every occurrence in this file is single-spaced. Copy every line byte for byte.

```
@@ -219,3 +219,8 @@
     expect(deletes.length).toBe(2);
   });
+  it('KS-851 G-4 - a quoted or schema-qualified table name is a write path too', () => {
+    // The matcher in writeStatements requires the BARE name, so INSERT INTO "svc_kyc_images"
+    // and UPDATE public.svc_kyc_images are invisible to it (re-gate G-4: 0 failed / 26, twice).
+    const anySpelling = stripComments(SRC).match(/(INSERT[ ]+INTO|UPDATE)[ ]+(?:"?public"?[.])?"?svc_kyc_images"?/gi) ?? [];
+    expect(anySpelling.map((w) => w.toUpperCase())).toEqual(['INSERT INTO SVC_KYC_IMAGES']);
+  });
 });
```

**Do NOT touch** `:74-:79` (`stripComments`), `:91-:96` (`insertColumnLists`), `:99-:102` (`writeStatements` — its matcher stays exactly as it is), the module docstring (`:1-:44`), `GUARD_CORPUS` (`:51`), `SRC` (`:57`), or any cell at `:105-:220`. Do NOT rename the new cell: the checker names it by the literal prefix `KS-851 G-4 - a quoted or schema-qualified table name is a write path too`.

## THIS IS VITEST

`repo.test_runner` begins with `vitest`. The file already imports `describe/it/expect` from `'vitest'` and `readFileSync`/`join` from node; **add no import**, mock nothing, and never write `jest.*`.

## The test — ONE new cell in the EXISTING suite (no new file)

File: `Blockchain/Dev/services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts`
The shape to copy is the cell immediately above the insertion point, `:214-:220` (`CONTROL — the DELETE paths are untouched, so this is not "no SQL mentions the table"`): it runs one regex over `stripComments(SRC)` and asserts on the result. There is no database, no app boot, no HTTP, no network and no mock — this is a SOURCE-STRUCTURAL guard that reads one file as text (`:57`). Copy that shape and nothing else.

## Cells

- `spellings` = `KS-851 G-4 - a quoted or schema-qualified table name is a write path too`
- `corpus` = `CONTROL — the corpus is exactly the one file this guard claims to read`
- `not_vacuous` = `CONTROL — the reader actually finds an INSERT, so the assertions below are not vacuous`
- `three_params` = `🔴 the INSERT binds exactly three parameters`
- `stripper` = `CONTROL — stripComments does NOT eat a url, and DOES eat a real comment`
- `deletes` = `CONTROL — the DELETE paths are untouched, so this is not "no SQL mentions the table"`

*(Two of the file's cells are deliberately NOT declared: `'🔴 \`svc_kyc_images\` has exactly ONE write path IN THIS FILE, and it is that INSERT'` (`:149`) and `'🔴 the INSERT does not name the \`data\` column'` (`:121`). Both titles carry a BACKTICK, and a declared cell name may not — so neither can be named here. Neither is disturbed by this diff or by the tamper: `:149`'s matcher is the bare-name one that cannot see the tampered spelling, which is the whole point of the ticket, and `:121` reads `insertColumnLists`, whose regex is also bare-name.)*

## Red cells

- KS-851 G-4 - a quoted or schema-qualified table name is a write path too

## Tampers

ONE tamper, a ONE-line replacement of a whole-line `//` comment inside `dbSaveImage`'s `try` block in `Blockchain/Dev/services/kyc/src/index.ts` with a second, real, quoted-name payload write — the exact shape the re-gate planted when it measured **0 failed / 26**. The suite reads `index.ts` from disk (`:57`, `readFileSync(join(__dirname, '..', GUARD_CORPUS[0]), 'utf8')`), so the tampered file is what every cell sees. The checker plants it and restores the file by bytes.

`:303` is the middle of three `//` comment lines (`:302`, `:303`, `:304`) sitting between `try {` (`:301`) and `await query(` (`:305`), so it is not inside any statement and nothing on a neighbouring line can veto it: replacing it with one complete statement leaves `:302` and `:304` as comments and the `try` block syntactically whole, and `query`, `id`, `mimeType` and `userId` are all in scope there (`:295-:299`, `:305-:309`). `grep -cF` over `index.ts` at the tip = **1** (byte-unique, 4 leading spaces).

### QUOTEDWRITE — a second payload write spelled with a quoted table name
File: `Blockchain/Dev/services/kyc/src/index.ts`
Line: 303
From:
```
    // previously the only linkage was inside the ENCRYPTED documents blob.
```
To:
```
    await query('INSERT INTO "svc_kyc_images" (id, data, mime_type) VALUES ($1,$2,$3)', [id, mimeType, userId]); // TAMPER KS-851 G-4: a quoted-name second write path
```
Reds: `spellings`

## Controls

- `corpus`
- `not_vacuous`
- `three_params`
- `stripper`
- `deletes`

*(Why every one of them stays green under QUOTEDWRITE, stated rather than assumed: `insertColumnLists`'s regex `/INSERT\s+INTO\s+svc_kyc_images\s*\(/` and the `three_params` regex both require the BARE name, so neither sees the tampered line and both keep reading the real statement at `index.ts:306`; `deletes` counts `DELETE FROM` only; `corpus` and `stripper` read no product SQL at all. The ONLY cell whose reading changes is the one this diff adds.)*

## THE CHANGE — state it to yourself before you write a line

At the untouched tip the suite is green. With this hunk at the tip: still green — the new cell's matcher finds exactly the one real statement at `index.ts:306` and upper-cases it to `INSERT INTO SVC_KYC_IMAGES`. Under **QUOTEDWRITE** with the hunk: the new cell RED (its list is two entries — the tampered quoted write at `:303` and the real one at `:306`), every other cell green.

## Premises (measured by reading the tip at 06:1x)

- **The anchors.** `:219` (`    expect(deletes.length).toBe(2);`), `:220` (`  });`) and `:221` (`});`) are non-blank ASCII; `:221` is the last line of the file (221 lines total), so this pure insertion has real trailing context.
- **The product at the tip.** `index.ts:295` `async function dbSaveImage(`, `:300` `if (!isDbAvailable()) return;`, `:301` `try {`, `:302-:304` three `//` comment lines, `:305-:309` the one `await query(...)` INSERT (`INSERT INTO svc_kyc_images (id, mime_type, user_id) VALUES ($1,$2,$3)` at `:306`, single-spaced), `:310` `} catch (err: any) {`. The tamper's `From` is `:303`.
- **Why the new cell is green at the tip.** `:161` already asserts `writeStatements(SRC)` equals the single-element `['INSERT INTO SVC_KYC_IMAGES']`, and the new matcher differs from `writeStatements`' only by allowing an optional `public.` and optional quotes — neither of which `index.ts` uses at the tip. `:218-:219` account for the two `DELETE FROM` statements, which no `INSERT|UPDATE` matcher sees.
- **The cell names.** `KS-851 G-4` occurs 0 times in the suite at the tip (control: `svc_kyc_images` 14 occurrences); no declared name is a prefix of another; no declared name carries a backtick, a `$` or a backslash.
- **Surface.** A unit suite that reads one file from disk and matches text. No network, no database, no credentials, no PII. **Not an auth surface** — `services/kyc/src/index.ts` is read, never edited, and nothing here touches `utils/callbackAuth.ts`, `subjectDeks.ts` or any token path.

## UNMEASURED — stated rather than glossed

The drafter **did not run the suite** (a drafter writes briefs; the checker runs). Reasoned from the file, not executed: that `index.ts` contains no other `INSERT INTO`/`UPDATE` against this table under any spelling at the tip — `:161`'s existing single-element expectation says so for the bare form, and the widened form adds only optional quoting and an optional `public.` qualifier. If that is wrong, T5 (green at the tip) fires and the round is cheap.

## Collision

`services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts` and `services/kyc/src/index.ts` are named by no held READY (checked against `night/candidates.md`'s ⚠ list and its HELD list at 06:1x); KS-851 has **zero rows in `night/done.md`**; the ticket is Backlog, Medium, assigned to kamil.kreiser@secuura.ai, with no attachment and no PR. KS-849 (also kyc) is SET ASIDE for wanting an in-process driver — this task needs none, which is why it is briefable where KS-849 is not.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts` / `+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts`, then the ONE hunk above exactly as shown (`@@ -219,3 +219,8 @@`). Every `+` line is its OWN physical line (the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string — DECODE them; a `+` line that carries a backslash is a FAIL). Every context line keeps its leading space.

## Notes for the raise (not for the model)

- **Refs KS-851 item G-4. Does not close the ticket** — G-1 (the `user_id` / `created_at` ordinal drift across two shipped SQL files), G-2 (the untransacted front/back image pair, which needs `dbSaveImage` to take a client and is more than three edit points) and G-3 (the wrong "ONE HONEST LIMIT" docstring at `index.ts:283-:293`) are untouched and are named in the PR body as remaining.
- **This is the coverage half of G-4, not the refactor.** The ticket's own fix shape is to widen `writeStatements`' regex; that edit also changes what `:161` and the F-3 fixture cells assert and would have retitled the `IN THIS FILE` cell, which is more than a test_only round can carry honestly. The added cell closes the blindness the re-gate measured; the raiser may fold the widened regex into `writeStatements` and delete this cell in the same PR. Say so in the raise text rather than letting a reviewer discover it.
- **Raise tier: TIER 2** (a `services/kyc` unit suite; zero product bytes).
