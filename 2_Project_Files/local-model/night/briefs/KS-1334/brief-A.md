# KS-1334-A ADMINCONFIG500-A — route the refresh-tenants and backfill-certification-metadata 500s in routes/adminConfig.ts through fail500, and update the KS-730 SOURCE pins in the same change

File: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts`  (product, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`  (EXISTING, modified in place — NOT a new file)
Tip: `3f70224a069b944334480478ad5d16a5ed33eeae`
Runner: `jest` (ts-jest; `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)

Written 2026-09-26 21:20:57 AEST (shell `date`) by a Spark brief-writer sub-agent for Wednesday, from origin develop `3f70224a069b`, read in a `--no-local` scratch clone with develop fetched. `adminConfig.ts` read at `:80-:120`, `:1835-:1862`, `:2015-:2034`, `:2130-:2160` and grepped whole (2160 lines, blob `ea34a439ffc8`, last changed `e6056de7e` KS-730 #1284). `ks730c-…test.ts` read WHOLE (204 lines, blob `611809c1e828`). **RUNG 3: every `-`, `+` and context line and every header is given byte for byte. Brief A of 2 (A → B): A converts `:113` and `:1859`; B (`:2031`, `:2158`) is written after A merges, because both edit the same two pins in the test file.**

## The mode — read this twice

CODE+TEST, **MODIFY-IN-PLACE**. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` — `--- a/…` / `+++ b/…`, EXACTLY the 2 hunks in `## The exact change`.
2. `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` — an EXISTING file, `--- a/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`, EXACTLY the 3 hunks in `## The test`. **Do NOT use `--- /dev/null`; do NOT create a new test file.** Its full content is in the input's files; every context line is copied from it.

You never touch any other file: not `routes/webhooks.ts`, `routes/gdpr.ts`, `routes/systemErrors.ts`, `utils/logger.ts`, `db.ts`, `__tests__/helpers/sharedModuleMock.ts`, nor the reference test.

## What is wrong (one paragraph)

Four handlers in `routes/adminConfig.ts` answer a caught error with the thrown `message` in the 500 body and **no `NODE_ENV` guard**, so internal text reaches the client in production too (KS-1334, filed while finishing KS-730 PR 3). They are `:113` POST /refresh-tenants (`message: err?.message || 'Refresh failed'`), `:1859` POST /backfill-certification-metadata, `:2031` POST /seed-demo-users and `:2158` POST /migrate-tenant-data (the last three are the byte-identical line `    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` — literal count 3 at the tip, at exactly those lines). The same file already has the vehicle: `fail500(res, context, err)` at `:103-:106` (KS-730, #1284) logs the thrown text server-side under a route-naming context and answers the constant body `{ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } }`; 46 sites use it, each context `Admin config request failed (<METHOD> /api/admin<path>)`. **This brief converts `:113` and `:1859`.** Because `ks730c`'s SOURCE cells pin the file (C3: exactly 46 helper calls / 46 distinct contexts at `:142`; C4: the four unconditional sites by route at `:171-:174`), fixing any site reds them BY DESIGN — the ticket's Done-means 2 says the KNOWN list is updated in the same change. So the test edits are part of the fix, not optional.

## The exact change

Both are ONE-line-for-ONE-line replacements; no line before or after moves. The context lines are ASCII.

Edit 1 — line `:113` (POST /refresh-tenants). Context: `:112` is `  } catch (err: any) {`, `:114` is `  }`.

```diff
@@ -112,3 +112,3 @@
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err?.message || 'Refresh failed' } });
+    fail500(res, 'Admin config request failed (POST /api/admin/refresh-tenants)', err);
   }
```

Edit 2 — line `:1859` (POST /backfill-certification-metadata). **Its `-` line is ALSO the text of `:2031` and `:2158`** — the TWO leading context lines are what make this hunk unique: `:1857` is `    res.json({ success: true, updatedCount: result });` (literal count 1 in the file), `:1858` is `  } catch (err: any) {`, `:1860` is `  }`. Copy all three, and the header, exactly.

```diff
@@ -1857,4 +1857,4 @@
     res.json({ success: true, updatedCount: result });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Admin config request failed (POST /api/admin/backfill-certification-metadata)', err);
   }
```

**Do NOT touch:** `:2031` and `:2158` (brief B), the `fail500` helper and its KS-730 docblock (`:85-:106`), every other `fail500(res, …)` call, the imports (`:12-:23` — `Response` and `logger` are already imported; add NONE), and every other line. The two new contexts follow the file's generated pattern exactly (`Admin config request failed (POST /api/admin/<route>)`); do not shorten or reword them — C3 asserts they are DISTINCT.

## The test

File: `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`

MODIFY IN PLACE, three hunks, in file order. The harness (loopback express app on `127.0.0.1:0`, `jest.mock('../db')` with `prisma.$executeRaw: mockExecuteRaw` and `refreshTenantConfigs: jest.fn()`, the logger mock `mockLoggerError`, `setNodeEnv`, `CONSTANT_BODY`, `beforeEach(() => jest.clearAllMocks())`) is the file's own, `:13-:108`; the new cells reuse it and add NO import and NO new `jest.mock`.

T1 — `:142`, C3's expected count 46 → 48 (two more helper calls, two more distinct contexts). Context `:141`, `:143`.
T2 — `:172`, DELETE the KNOWN list's first row (the two routes this brief fixes). Context `:171`, `:173`. Old side 3, new side 2.
T3 — a pure INSERTION between `:203` (`  });`, the end of the last KS-730 cell) and `:204` (`});`, the end of the file's describe). The inserted block's FIRST line `});` closes the KS-730 describe; its last line `  });` ends the last new cell; the file's own `:204` `});` then closes the new KS-1334 describe. Context: `:203` leading, `:204` trailing (both non-blank). Because T2 removed one line, T3's new-side start is 202. 53 `+` lines (5 of them a lone `+`, the blank lines).

```diff
@@ -141,3 +141,3 @@
     expect({ liveTernaries: liveTernaries.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size })
-      .toEqual({ liveTernaries: 0, helperCalls: 46, distinctContexts: 46 });
+      .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });
     expect(contexts.filter((c) => !c)).toEqual([]);
@@ -171,3 +171,2 @@
     const KNOWN = [
-      'POST /refresh-tenants', 'POST /backfill-certification-metadata',
       'POST /seed-demo-users', 'POST /migrate-tenant-data',
@@ -203,2 +202,55 @@
   });
+});
+
+// KS-1334 part A: two of the four UNCONDITIONAL sites named by C4 above now go through fail500. They
+// answered err.message in EVERY environment, production included, so unlike the KS-730 cells the
+// production row is the one that separates this class, and it is driven first. Part B covers the
+// other two (seed-demo-users, migrate-tenant-data). Its own LEAK carries no double quote: the shared
+// LEAK above does, JSON-escapes to a backslash-quote in the body, and so can never be found by includes.
+const KS1334_LEAK = 'could not serialize access due to concurrent update ks1334-private-detail';
+const KS1334_NODE_ENVS = ['production', 'development', 'demo', 'test', undefined];
+const KS1334_ROUTES = [
+  { label: 'POST /refresh-tenants', path: '/refresh-tenants', body: {}, context: 'Admin config request failed (POST /api/admin/refresh-tenants)' },
+  { label: 'POST /backfill-certification-metadata', path: '/backfill-certification-metadata', body: { issuerName: 'ks1334-issuer' }, context: 'Admin config request failed (POST /api/admin/backfill-certification-metadata)' },
+] as const;
+const mockRefreshTenantConfigs = (jest.requireMock('../db') as { refreshTenantConfigs: jest.Mock }).refreshTenantConfigs;
+
+async function post1334(route: (typeof KS1334_ROUTES)[number], nodeEnv: string | undefined, throwIt: boolean): Promise<{ status: number; text: string }> {
+  setNodeEnv(nodeEnv);
+  if (throwIt) {
+    mockRefreshTenantConfigs.mockRejectedValue(new Error(KS1334_LEAK));
+    mockExecuteRaw.mockRejectedValue(new Error(KS1334_LEAK));
+  } else {
+    mockRefreshTenantConfigs.mockResolvedValue(undefined);
+    mockExecuteRaw.mockResolvedValue(3);
+  }
+  const res = await fetch(baseUrl + '/api/admin' + route.path, {
+    method: 'POST',
+    headers: { 'content-type': 'application/json' },
+    body: JSON.stringify(route.body),
+  });
+  return { status: res.status, text: await res.text() };
+}
+
+describe('KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message', () => {
+  it.each(KS1334_ROUTES)('RED KS-1334 A1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', async (route) => {
+    for (const nodeEnv of KS1334_NODE_ENVS) {
+      mockLoggerError.mockClear();
+      const reply = await post1334(route, nodeEnv, true);
+      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
+      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
+      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
+    }
+  });
+
+  it.each(KS1334_ROUTES)('control KS-1334 A0 $label: a call that does not throw answers 200 and logs nothing', async (route) => {
+    const reply = await post1334(route, 'production', false);
+    expect({ status: reply.status, success: JSON.parse(reply.text).success }).toEqual({ status: 200, success: true });
+    expect(mockLoggerError).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1334 A2: KS1334_LEAK survives JSON encoding, so leaked: false above is not vacuous', () => {
+    expect(JSON.stringify({ success: false, error: { message: KS1334_LEAK } }).includes(KS1334_LEAK)).toBe(true);
+    expect(new Error(KS1334_LEAK).message).toBe(KS1334_LEAK);
+  });
 });
```

**Every `+` line is ASCII** and carries NO backslash, NO backtick and NO double-quote (counted: 0 of each); `$label` in the two `it.each` titles is jest's row interpolation and is intended. `KS1334_LEAK` is deliberately NOT the file's `LEAK`: `LEAK` carries double quotes, which JSON-escape in the body, so `reply.text.includes(LEAK)` can never be true (measured — see Premises); control A2 pins that `KS1334_LEAK` survives encoding.

## Red cells

- KS-730 C3 SOURCE
- KS-730 C4 SOURCE
- RED KS-1334 A1

(Title SUBSTRINGS. At the tip with ONLY the test hunks applied these FOUR cells fail by assertion: C3 (`helperCalls: 46` received vs 48 expected), C4 (received KNOWN has the two extra routes), and both `RED KS-1334 A1` rows (`it.each`: under `production` the body carries `KS1334_LEAK` and nothing is logged). All three A0/A2 controls and the 14 KS-730 cells other than C3/C4 stay green. With the product hunks all 19 are green.)

## Cells and controls

- `RED KS-1334 A1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it` — 2 rows (refresh-tenants, backfill-certification-metadata); per NODE_ENV (`production` FIRST, then development, demo, test, unset) the logger is cleared, then status 500 + `leaked: false`, the exact constant body, and the WHOLE logger call list `[[route.context, { error: KS1334_LEAK }]]` (REACHED fail500 for THIS route, THIS nodeEnv — the N-1288-2 shape).
- `control KS-1334 A0 $label: a call that does not throw answers 200 and logs nothing` — 2 rows; proves a 500 above is caused by the throw, not by the harness.
- `control KS-1334 A2: KS1334_LEAK survives JSON encoding, so leaked: false above is not vacuous`.
- `KS-730 C3 SOURCE …` / `KS-730 C4 SOURCE …` — existing cells whose PINS this brief updates (red at tip by design, green after).
- The 12 other KS-730 cells — unchanged, green throughout.

## The failing case (the "tamper")

On the FIXED tree, put `:113` back: `    fail500(res, 'Admin config request failed (POST /api/admin/refresh-tenants)', err);` (literal count 1 in the fixed file) → the tip's `    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err?.message || 'Refresh failed' } });`. **Measured:** exactly C3, C4 and `RED KS-1334 A1 POST /refresh-tenants` red; A1 backfill + all controls green.

**Arm R3 (the logger-assertion arm, as KS-1341 B/C carried):** on the fixed tree, `:104` `  logger.error(context, { error: err instanceof Error ? err.message : String(err) });` (count 1) → `  if (process.env.NODE_ENV === 'production') logger.error(…)`. **Measured:** both A1 rows RED (the whole-call-list assertion at `development`), all three KS-1334 controls green. (The eight KS-730 C1/C2 rows also red under R3 — they assert the same log.) A green A1 under R3 would be a FAIL of this brief.

## Premises (each one measured, with where)

- Every quoted line was read with `git show 3f70224a069b:<path>`; the site-line text occurs exactly 3 times (`:1859, :2031, :2158`); `:1857`'s text once; no non-ASCII on `adminConfig.ts:111-:115, :1856-:1861`; `ks730c` non-ASCII only at `:10, :62, :93, :163, :164` (none in a hunk).
- **Golden applies strictly:** `git apply --check` rc 0 and `patch -p1 -F0` rc 0 on the two files at `3f70224a`; the results are byte-identical to the scratch goldens. Control: with `:1859` tampered, `patch -F0 --dry-run` rc 1. 0 blank context lines in the diff.
- **RED at tip, EXECUTED** (jest/ts-jest in a scratch clone, node_modules symlink-farmed from the Secuura checkout by `tasks/code_patch/prepare_clone.sh`, shared built in the clone): test hunks only → `Tests: 4 failed, 15 passed, 19 total` = exactly the four declared cells, by assertion.
- **GREEN after, EXECUTED:** golden applied → `19 passed`. Whole originate suite: tip `82 suites / 962 tests passed` → fixed `82 / 967 passed`, 0 failures. `tsc --noEmit -p tsconfig.json` rc 0. `npm run lint` (`eslint src`) rc 0 (warnings only, none on a changed line: the two in `adminConfig.ts` are `:2089` and `:2129`, both present at the tip); `eslint --max-warnings 0` on the test file rc 0.
- Tamper and Arm R3: EXECUTED as stated above.
- **Found while writing (a KS-730 note, NOT fixed here):** `ks730c`'s own C1 `leaked` check is vacuous — `LEAK` contains `"admin_settings_pkey"`, which the JSON body carries as `\"`, so `reply.text.includes(LEAK)` is false even when the body leaks (measured with this brief's first draft, whose A1 used `LEAK`: at the tip the leaking production body PASSED `leaked: false` and failed only on the CONSTANT_BODY line). The CONSTANT_BODY assertion still catches a leak, so C1 is not blind; the `leaked` field is. Worth a line on KS-730 or KS-1334.

## UNMEASURED — stated rather than glossed

1. `spark_checker.sh` was NOT run on the golden (no pre-probe). The run above is the package's own jest, not the checker's A4 sequencing.
2. node_modules come from the real checkout (HEAD `3bad652d`), not an install at `3f70224a`; the KS-1341 B/C rounds ran the same way.
3. The C3 cell title still says "forty-six" (now 48) — left alone to keep the cell name stable; B can reword it when the count settles at 50.
4. The builder was run against the scratch clone (`NIGHT_SOURCE_CHECKOUT`), whose `source_checkout` field therefore names a scratchpad path.

## Collision

KS-1334 is Backlog, no attachment, 0 model rounds. `git ls-remote` shows one branch naming adminConfig — `feature/ks-730-adminconfig-prod-message-b29-9` (`dfc2468a5`), the pre-squash head of merged #1284: its `adminConfig.ts` is identical to develop's (`git diff --stat` empty). No other in-flight work touches either file.

## Scope

**Closes 2 of 4 sites; refs KS-1334, does NOT close it.** Brief B (`:2031` seed-demo-users, `:2158` migrate-tenant-data; KNOWN emptied, C3 → 50) is written after A merges.

## Output

Exactly ONE fenced diff block with TWO files: first the product (2 hunks, headers `@@ -112,3 +112,3 @@` and `@@ -1857,4 +1857,4 @@`), then the EXISTING test file (3 hunks, `@@ -141,3 +141,3 @@`, `@@ -171,3 +171,2 @@`, `@@ -203,2 +202,55 @@`). Paths exactly as the File: / Test file: lines give them, `a/` and `b/` prefixed. Every `+` line on its own physical line. Every context line keeps its single leading space. No prose outside the block.
