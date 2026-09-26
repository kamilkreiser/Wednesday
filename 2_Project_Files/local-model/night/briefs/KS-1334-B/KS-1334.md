# KS-1334-B ADMINCONFIG500-B — route the seed-demo-users and migrate-tenant-data 500s in routes/adminConfig.ts through fail500, and empty the KS-730 KNOWN list in the same change

File: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts`  (product, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`  (EXISTING, modified in place — NOT a new file)
Tip: `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`
Runner: `jest` (ts-jest; `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)

Written 2026-09-27 02:0x AEST (shell `date`) by a Spark brief-writer sub-agent for Wednesday, from origin develop `94c9c7aa9be7` (part A merged as #1294, `cdba29ad7`), read in a scratch clone with develop fetched. `adminConfig.ts` read at `:1-:30`, `:80-:120`, `:1905-:2160` (2160 lines, 100,681 B, blob `075ca85197fa`). `ks730c-…test.ts` read WHOLE (256 lines, blob `bd23cbd4ba13`, which INCLUDES part A's merged edits: C3 at 48, KNOWN down to two routes, the KS-1334 part A block `:205-:256`). **RUNG 3: every `-`, `+` and context line and every header is given byte for byte. Brief B of 2: A (`:113`, `:1859`) is merged; B converts the last two, `:2031` and `:2158`.**

## The mode — read this twice

CODE+TEST, **MODIFY-IN-PLACE**. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` — `--- a/…` / `+++ b/…`, EXACTLY the 2 hunks in `## The exact change`.
2. `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` — an EXISTING file, `--- a/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`, EXACTLY the 3 hunks in `## The test`. **Do NOT use `--- /dev/null`; do NOT create a new test file.** Its full content is in the input's files; every context line is copied from it.

You never touch any other file: not `routes/webhooks.ts`, `routes/gdpr.ts`, `routes/systemErrors.ts`, `utils/logger.ts`, `utils/demoSeedGate.ts`, `db.ts`, `__tests__/helpers/sharedModuleMock.ts`, nor the reference test.

## What is wrong (one paragraph)

Two handlers in `routes/adminConfig.ts` still answer a caught error with the thrown `message` in the 500 body and **no `NODE_ENV` guard**, so internal text reaches the client in production too (KS-1334). They are `:2031` POST /seed-demo-users and `:2158` POST /migrate-tenant-data — the byte-identical line `    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` (literal count 2 at the tip, at exactly those lines). The same file already has the vehicle: `fail500(res, context, err)` at `:103-:106` logs the thrown text server-side under a route-naming context and answers the constant body; 48 sites use it (46 from KS-730, 2 from part A), each context `Admin config request failed (<METHOD> /api/admin<path>)`. **This brief converts both.** `ks730c`'s SOURCE cells pin the file (C3: exactly 48 helper calls / 48 distinct contexts at `:142`; C4: the KNOWN list of unconditional sites at `:171-:173`, now these two), so fixing them reds C3 and C4 BY DESIGN — the ticket's Done-means says the KNOWN list is emptied in the same change. The test edits are part of the fix.

## The exact change

Both are ONE-line-for-ONE-line replacements; no line before or after moves. The context lines are ASCII.

Edit 1 — line `:2031` (POST /seed-demo-users). **Its `-` line is ALSO the text of `:2158`, and its `  } catch (err: any) {` / `  }` neighbours occur 50+ times** — the TWO leading lines `:2028` `      failed,` (literal count 1) and `:2029` `    });` are what make this hunk unique. Copy all four context lines, and the header, exactly.

```diff
@@ -2028,5 +2028,5 @@
       failed,
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Admin config request failed (POST /api/admin/seed-demo-users)', err);
   }
```

Edit 2 — line `:2158` (POST /migrate-tenant-data). Leading context `:2156` `    res.json({ success: true, results });` (literal count 1) and `:2157`, trailing `:2159`.

```diff
@@ -2156,4 +2156,4 @@
     res.json({ success: true, results });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Admin config request failed (POST /api/admin/migrate-tenant-data)', err);
   }
```

**Do NOT touch:** the `fail500` helper and its KS-730 docblock (`:85-:106`), every other `fail500(res, …)` call, the inner per-user `logger.error('Demo user seed failed', …)` at `:1999`, the per-tenant `err.message?.substring(0, 60)` at `:2152` (a result row in a 200 body — the ticket's fifth site, NOT this brief's), the imports (add NONE), and every other line. The two new contexts follow the file's pattern exactly; do not shorten or reword them — C3 asserts they are DISTINCT.

## The test

File: `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`

MODIFY IN PLACE, three hunks, in file order. The harness (loopback express app, `jest.mock('../db')` with `getTenantManager: () => null`, the logger mock whose `error` is `mockLoggerError` and whose `warn` is a plain `jest.fn()`, `setNodeEnv`, `CONSTANT_BODY`, `beforeEach(() => jest.clearAllMocks())`) is the file's own, `:13-:108`; part A's `KS1334_LEAK` and `KS1334_NODE_ENVS` (`:210-:211`) are reused. The new cells add NO import and NO new `jest.mock`.

T1 — `:142`, C3's expected count 48 → 50. Context `:141`, `:143`.
T2 — `:171-:173`, the KNOWN list becomes the typed empty list (one line). Trailing context `:174`. Old side 4, new side 2.
T3 — a pure INSERTION between `:255` (`  });`, the end of part A's last cell) and `:256` (`});`, the end of part A's describe, the last line of the file). The inserted block's FIRST line `});` closes the part A describe; its last line `  });` ends the last new cell; the file's own `:256` `});` then closes the new part B describe. Context: `:255` leading, `:256` trailing (both non-blank). Because T2 removed two lines, T3's new-side start is 253. 49 `+` lines (4 of them a lone `+`, the blank lines).

```diff
@@ -141,3 +141,3 @@
     expect({ liveTernaries: liveTernaries.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size })
-      .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });
+      .toEqual({ liveTernaries: 0, helperCalls: 50, distinctContexts: 50 });
     expect(contexts.filter((c) => !c)).toEqual([]);
@@ -171,4 +171,2 @@
-    const KNOWN = [
-      'POST /seed-demo-users', 'POST /migrate-tenant-data',
-    ];
+    const KNOWN: string[] = [];
     let route = '';
@@ -255,2 +253,51 @@
   });
+});
+
+// KS-1334 part B: the last two UNCONDITIONAL sites (seed-demo-users, migrate-tenant-data) now go through
+// fail500, so the KNOWN list in C4 is empty and C3 counts 50. Neither handler reaches its outer catch
+// through the prisma mock the cells above use, so each is driven through the first call its try block
+// makes outside any inner catch: seed-demo-users through the refusal warning of its demo-seed gate
+// (the gate is closed here), migrate-tenant-data through the platform pool of its tenant manager.
+const mockLoggerWarn = (jest.requireMock('../utils/logger') as { logger: { warn: jest.Mock } }).logger.warn;
+const mockDb = jest.requireMock('../db') as { getTenantManager: () => unknown };
+const KS1334B_ROUTES = [
+  { label: 'POST /seed-demo-users', path: '/seed-demo-users', calmStatus: 403, context: 'Admin config request failed (POST /api/admin/seed-demo-users)' },
+  { label: 'POST /migrate-tenant-data', path: '/migrate-tenant-data', calmStatus: 400, context: 'Admin config request failed (POST /api/admin/migrate-tenant-data)' },
+] as const;
+
+async function post1334b(route: (typeof KS1334B_ROUTES)[number], nodeEnv: string | undefined, throwIt: boolean): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  delete process.env.ENABLE_DEMO_SEED;
+  mockLoggerWarn.mockReset();
+  mockDb.getTenantManager = () => null;
+  if (throwIt && route.path === '/seed-demo-users') {
+    mockLoggerWarn.mockImplementationOnce(() => { throw new Error(KS1334_LEAK); });
+  }
+  if (throwIt && route.path === '/migrate-tenant-data') {
+    mockDb.getTenantManager = () => ({ getPlatformPool: () => { throw new Error(KS1334_LEAK); } });
+  }
+  const res = await fetch(baseUrl + '/api/admin' + route.path, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify({}),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-1334 part B: seed-demo-users and migrate-tenant-data never answer a 500 with err.message', () => {
+  it.each(KS1334B_ROUTES)('RED KS-1334 B1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', async (route) => {
+    for (const nodeEnv of KS1334_NODE_ENVS) {
+      mockLoggerError.mockClear();
+      const reply = await post1334b(route, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
+    }
+  });
+
+  it.each(KS1334B_ROUTES)('control KS-1334 B0 $label: with nothing thrown the route answers its own refusal and logs no error', async (route) => {
+    const reply = await post1334b(route, 'production', false);
+    expect({ status: reply.status, success: JSON.parse(reply.text).success }).toEqual({ status: route.calmStatus, success: false });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
 });
```

**Every `+` line is ASCII** and carries NO backslash, NO backtick and NO double-quote (counted: 0 of each); `$label` in the two `it.each` titles is jest's row interpolation and is intended (the only `$`, 2 of them). How each route is made to throw, and why: neither handler's outer catch is reachable through the prisma mock — seed-demo-users' DB writes each sit in their own inner `try`, and migrate-tenant-data returns 400 when `getTenantManager()` is null. So seed-demo-users throws from its gate-refusal `logger.warn` (the gate is closed: `ENABLE_DEMO_SEED` is deleted), and migrate-tenant-data from `getPlatformPool()` of a tenant manager the cell installs on the mocked `../db` module (the handler `require`s it at call time). Each is the FIRST call in its `try` outside any inner catch.

## Red cells

- KS-730 C3 SOURCE
- KS-730 C4 SOURCE
- RED KS-1334 B1

(Title SUBSTRINGS. At the tip with ONLY the test hunks applied these FOUR cells fail by assertion: C3 (`helperCalls: 48` received vs 50 expected), C4 (received the two routes, expected `[]`), and both `RED KS-1334 B1` rows (`it.each`: under `production` the 500 body carries `KS1334_LEAK`). The two B0 controls and the 17 other existing cells stay green. With the product hunks all 23 are green.)

## Cells and controls

- `RED KS-1334 B1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it` — 2 rows (seed-demo-users, migrate-tenant-data); per NODE_ENV (`production` FIRST, then development, demo, test, unset) the logger is cleared, then status 500 + `leaked: false`, the exact constant body, and the WHOLE logger call list `[[route.context, { error: KS1334_LEAK }]]`.
- `control KS-1334 B0 $label: with nothing thrown the route answers its own refusal and logs no error` — 2 rows; seed-demo-users answers 403 (gate closed), migrate-tenant-data 400 (no tenant manager), `success: false`, and `mockLoggerError` not called — proves a 500 above is caused by the throw, not by the harness.
- `KS-730 C3 SOURCE …` / `KS-730 C4 SOURCE …` — existing cells whose PINS this brief updates (red at tip by design, green after).
- Every other existing cell (C1 ×4, C2 ×4, 4 KS-730 controls, part A's A1 ×2 / A0 ×2 / A2) — unchanged, green throughout.

## The failing case (the "tamper")

On the FIXED tree, put `:2031` back: `    fail500(res, 'Admin config request failed (POST /api/admin/seed-demo-users)', err);` (literal count 1 in the fixed file) → the tip's `    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });`. **Measured:** exactly C3, C4 and `RED KS-1334 B1 POST /seed-demo-users` red (`3 failed, 20 passed`); B1 migrate + both B0 controls green.

**Arm R3 (the logger-assertion arm):** on the fixed tree, `:104` `  logger.error(context, { error: err instanceof Error ? err.message : String(err) });` (count 1) → `  if (process.env.NODE_ENV === 'production') logger.error(…)`. **Measured:** both B1 rows RED (the whole-call-list assertion at `development`), both B0 controls green; C1 ×4, C2 ×4 and part A's A1 ×2 also red (they assert the same log) — `12 failed, 11 passed`. A green B1 under R3 would be a FAIL of this brief.

## Premises (each one measured, with where)

- Every quoted line was read at `94c9c7aa` in the scratch clone; the site-line text occurs exactly 2 times (`:2031, :2158`); `:2028` and `:2156` once each; no non-ASCII on `adminConfig.ts:2027-:2033, :2155-:2160` (the nearest non-ASCII lines are `:2022` and `:2136`, outside every hunk); `ks730c` non-ASCII only at `:10, :62, :93, :163, :164` (none in a hunk).
- **Golden applies strictly:** `git apply --check` rc 0 and `patch -F0 --dry-run` rc 0 on each of the two files at `94c9c7aa`; the applied results are byte-identical to `golden/adminConfig.B.ts` / `golden/ks730c.B.ts`. Control: with `:2028` altered, `patch -F0` rc 1 (`1 out of 2 hunks failed`). 0 blank context lines in the diff.
- **RED at tip, EXECUTED** (jest/ts-jest in the scratch clone, node_modules farmed from the Secuura checkout): test hunks only → `Tests: 4 failed, 19 passed, 23 total` = exactly the four declared cells, by assertion.
- **GREEN after, EXECUTED:** golden applied → `23 passed`. Whole originate suite: tip `84 suites / 979 tests passed` → fixed `84 / 983 passed`, 0 failures.
- **Compile:** a TEST-INCLUSIVE tsc (a temp config extending originate's `tsconfig.json` with `exclude: []`, so `src/__tests__` compiles under `strict` + `noUnusedLocals` + `noUnusedParameters`) — tip 0 errors, fixed 0 errors, identical sets. (Positive control on this config: an unused const in ks730c surfaces exactly one TS6133.)
- **Lint:** `eslint --max-warnings 0` on the fixed test file rc 0; `npm run lint` (`eslint src`) rc 0, 22 warnings, 0 errors; `adminConfig.ts`'s two warnings (`:2089` prefer-const, `:2129` unused `e`) are both present at the tip and on no changed line.
- Tamper and Arm R3: EXECUTED as stated above.

## UNMEASURED — stated rather than glossed

1. `spark_checker.sh` was NOT run on the golden (no pre-probe). The runs above are the package's own jest.
2. node_modules come from the real checkout, not an install at `94c9c7aa`.
3. The C3 and C4 cell TITLES still say forty-six / four — left alone so the declared red-cell substrings and the cell names stay stable; a follow-up can reword them now the count has settled at 50 and the list is empty.
4. The builder was run against the scratch clone (`NIGHT_SOURCE_CHECKOUT`), whose `source_checkout` field therefore names a scratchpad path.

## Collision

KS-1334 is **In Progress** by design (part A merged; the 2026-09-26T15:31Z comment holds it open for part B), so the build line carries `started_ok=`. No open PR touches `adminConfig.ts` or `ks730c` (GitHub API read, 2026-09-27 01:4x: open #1296/#1297 are systemErrors.ts/gdpr.ts). `git ls-remote` shows `feature/ks-1334-adminconfig-500-part-a-b32-3` (part A's merged head) and `feature/ks-730-…-b29-9` (merged #1284) — both already in develop. **KS-1349** (`night/briefs/KS-1349/`, filed tonight) edits ks730c's C1 loop `:112-:120`, above every hunk here; measured: both goldens apply on `94c9c7aa` in either order and give the same file, 23/23 green. If KS-1349 merges FIRST, this brief's three test hunks shift +2 and must be re-anchored before a round; if THIS merges first, KS-1349 needs nothing.

## Scope

**Closes the last 2 of the 4 unconditional 500 sites; refs KS-1334, does NOT close it.** The ticket also owns a FIFTH site, `:2152` (a per-tenant `err.message` in a 200 result row — Linear comment 2026-09-26T02:48Z; no fix shape ruled), which this brief leaves alone, and the part A merge comment owes a live sweep before Done.

## Output

Exactly ONE fenced diff block with TWO files: first the product (2 hunks, headers `@@ -2028,5 +2028,5 @@` and `@@ -2156,4 +2156,4 @@`), then the EXISTING test file (3 hunks, `@@ -141,3 +141,3 @@`, `@@ -171,4 +171,2 @@`, `@@ -255,2 +253,51 @@`). Paths exactly as the File: / Test file: lines give them, `a/` and `b/` prefixed. Every `+` line on its own physical line. Every context line keeps its single leading space. No prose outside the block.
