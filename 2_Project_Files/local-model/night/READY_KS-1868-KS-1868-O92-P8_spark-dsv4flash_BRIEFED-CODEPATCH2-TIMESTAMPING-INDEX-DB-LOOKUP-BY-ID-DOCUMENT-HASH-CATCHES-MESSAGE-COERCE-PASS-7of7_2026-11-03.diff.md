# READY — KS-1868-KS-1868-O92-P8 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 08:57 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:57 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/timestamping/src/index.ts } + { Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/timestamping/src/index.ts` (product) and `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/timestamping/src/index.ts
158	0	Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (24 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/timestamping/src/index.ts`; test(s): `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/timestamping/src/index.ts 24 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts 158 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/timestamping/src/index.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the timestamping DB lookup catches answer as usual and log text for a hostile thrown value RED ks1868 R1: a revoked Proxy on GET /api/timestamps/:id is logged as text and the route answers 404', 'KS-1868 the timestamping DB lookup catches answer as usual and log text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws on GET /api/timestamps/:id is logged as text and the route answers 404', 'KS-1868 the timestamping DB lookup catches answer as usual and log text for a hostile thrown value RED ks1868 R3: a revoked Proxy on GET /api/timestamps/document/:documentId is logged as text and the route answers 200', 'KS-1868 the timestamping DB lookup catches answer as usual and log text for a hostile thrown value RED ks1868 R4: an Error whose message getter throws on GET /api/timestamps/document/:documentId is logged as text and the route answers 200', 'KS-1868 the timestamping DB lookup catches answer as usual and log text for a hostile thrown value RED ks1868 R5: a revoked Proxy on GET /api/timestamps/hash/:hash is logged as text and the route answers 200', 'KS-1868 the timestamping DB lookup catches answer as usual and log text for a hostile thrown value RED ks1868 R6: an Error whose message getter throws on GET /api/timestamps/hash/:hash is logged as text and the route answers 200']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=105 failed=7 | after: total=114 failed=0` · `NEW reds: []` [baseline_suite.json total=105 failed=7; after_suite.json total=114 failed=0]
- A6 [verbatim]: `PASS A6 whole services/timestamping suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/timestamping: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/timestamping/src/index.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts` (+158/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/timestamping/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ddd770cab4aa922f5a49376b8bbe5232a94939f7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p8_timestamping_index_db_lookup_by_id_document_hash_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/timestamping/src/index.ts b/Blockchain/Dev/services/timestamping/src/index.ts
--- a/Blockchain/Dev/services/timestamping/src/index.ts
+++ b/Blockchain/Dev/services/timestamping/src/index.ts
@@ -774,7 +774,14 @@
     if (result.rows.length === 0) return undefined;
     return rowToTimestamp(result.rows[0]);
   } catch (err: any) {
-    log('warn', 'DB lookup by id failed', { id, error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    log('warn', 'DB lookup by id failed', { id, error: reason });
     return undefined;
   }
 }
@@ -786,7 +793,14 @@
     const result = await query('SELECT * FROM ts_timestamps WHERE document_id = $1 ORDER BY created_at DESC', [documentId]);
     return result.rows.map(rowToTimestamp);
   } catch (err: any) {
-    log('warn', 'DB lookup by document failed', { documentId, error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    log('warn', 'DB lookup by document failed', { documentId, error: reason });
     return [];
   }
 }
@@ -798,7 +812,14 @@
     const result = await query('SELECT * FROM ts_timestamps WHERE hash = $1 ORDER BY created_at DESC', [hash]);
     return result.rows.map(rowToTimestamp);
   } catch (err: any) {
-    log('warn', 'DB lookup by hash failed', { hash, error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    log('warn', 'DB lookup by hash failed', { hash, error: reason });
     return [];
   }
 }
diff --git a/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts
@@ -0,0 +1,158 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, afterEach, vi } from 'vitest';
+import http from 'http';
+import type { AddressInfo } from 'net';
+import type { RequestHandler } from 'express';
+
+// KS-1868 (operator 92 screen, timestamping index): the three DB lookup catches dbGetTimestampById (line 777), dbGetTimestampsByDocument (line 789) and
+// dbGetTimestampsByHash (line 801) of services/timestamping/src/index.ts pass `err?.message` straight into the log line's meta object, unguarded. `?.` guards
+// null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch throw, so the async route
+// handler rejects (an unhandled rejection) and the request never gets its answer where an ordinary Error is logged and the route answers from the fallback
+// (404 NOT_FOUND; 200 with an empty list; 200 with an empty list). The cells make the one lookup statement reject with such a value and assert the usual answer,
+// no unhandled rejection and a logged line that carries text. Harness: the real index.ts app, served on 127.0.0.1 (it also listens on an ephemeral port at
+// import); `./db` is a stand-in that is available, answers the startup statements and rejects only the lookup SELECT once the cell arms it; the shared JWT check is
+// a pass-through; console.log is a plain recording function (no database, no network).
+const h = vi.hoisted(() => {
+  process.env.PORT = '0';
+  return {
+    toThrow: undefined as unknown,
+    armed: false,
+    lines: [] as string[],
+    unhandled: 0,
+  };
+});
+
+vi.mock('../db', () => ({
+  initDb: async () => true,
+  isDbAvailable: () => true,
+  closeDb: async () => undefined,
+  query: (sql: string, ..._args: unknown[]) =>
+    h.armed && String(sql).includes('FROM ts_timestamps WHERE') ? Promise.reject(h.toThrow) : Promise.resolve({ rows: [{ count: '0' }] }),
+}));
+vi.mock('@secuura/shared', async (importOriginal) => ({
+  ...(await importOriginal<Record<string, unknown>>()),
+  authenticate: () => ((_req, _res, next) => next()) as RequestHandler,
+}));
+
+const realLog = console.log;
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+let base = '';
+let server: http.Server;
+
+beforeAll(async () => {
+  console.log = (...args: unknown[]) => {
+    if (typeof args[0] === 'string') h.lines.push(args[0]);
+  };
+  const { default: app } = await import('../index');
+  for (let i = 0; i < 100 && !h.lines.some((l) => l.includes('Timestamping Service started')); i++) {
+    await new Promise<void>((resolve) => setTimeout(resolve, 20));
+  }
+  server = http.createServer(app);
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(async () => {
+  console.log = realLog;
+  await new Promise<void>((resolve) => server?.close(() => resolve()));
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.armed = false;
+  h.lines.length = 0;
+  h.unhandled = 0;
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+});
+afterEach(() => {
+  h.armed = false;
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+
+/** The answer as {status, code}; null when the request got none within the deadline (a hang). */
+async function get(path: string): Promise<{ status: number; code: string | undefined } | null> {
+  try {
+    const r = await fetch(base + path, { signal: AbortSignal.timeout(1500) });
+    const payload = (await r.json()) as { error?: { code?: string } };
+    return { status: r.status, code: payload.error?.code };
+  } catch {
+    return null;
+  }
+}
+
+const LINE = (message: string): Record<string, unknown>[] =>
+  h.lines
+    .map((l) => {
+      try {
+        return JSON.parse(l) as Record<string, unknown>;
+      } catch {
+        return {} as Record<string, unknown>;
+      }
+    })
+    .filter((o) => o.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? (o.error as string) : '<' + typeof o?.error + '>');
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const SITES = [
+  { log: 'DB lookup by id failed', path: '/api/timestamps/ks1868-unknown', answer: { status: 404, code: 'NOT_FOUND' } },
+  { log: 'DB lookup by document failed', path: '/api/timestamps/document/00000000-0000-4000-8000-000000000001', answer: { status: 200, code: undefined } },
+  { log: 'DB lookup by hash failed', path: '/api/timestamps/hash/' + 'a'.repeat(64), answer: { status: 200, code: undefined } },
+];
+
+async function run(s: (typeof SITES)[number], value: unknown, reason: string): Promise<void> {
+  h.toThrow = value;
+  h.armed = true;
+  const got = await get(s.path);
+  await new Promise<void>((resolve) => setTimeout(resolve, 25));
+  expect(got).toEqual(s.answer);
+  expect(h.unhandled).toBe(0);
+  expect(LINE(s.log)).toHaveLength(1);
+  expect(reasonOf(LINE(s.log)[0])).toBe(reason);
+}
+const CONSTANT = 'unreadable thrown value';
+
+describe('KS-1868 the timestamping DB lookup catches answer as usual and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error on GET /api/timestamps/:id is logged with its message and the route answers 404', async () => {
+    await run(SITES[0], new Error('db boom'), 'db boom');
+  });
+  it('control ks1868 C2: an ordinary Error on GET /api/timestamps/document/:documentId is logged with its message and the route answers 200', async () => {
+    await run(SITES[1], new Error('db boom'), 'db boom');
+  });
+  it('control ks1868 C3: an ordinary Error on GET /api/timestamps/hash/:hash is logged with its message and the route answers 200', async () => {
+    await run(SITES[2], new Error('db boom'), 'db boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy on GET /api/timestamps/:id is logged as text and the route answers 404', async () => {
+    await run(SITES[0], revokedProxy(), CONSTANT);
+  });
+  it('RED ks1868 R2: an Error whose message getter throws on GET /api/timestamps/:id is logged as text and the route answers 404', async () => {
+    await run(SITES[0], getterThrows(), CONSTANT);
+  });
+  it('RED ks1868 R3: a revoked Proxy on GET /api/timestamps/document/:documentId is logged as text and the route answers 200', async () => {
+    await run(SITES[1], revokedProxy(), CONSTANT);
+  });
+  it('RED ks1868 R4: an Error whose message getter throws on GET /api/timestamps/document/:documentId is logged as text and the route answers 200', async () => {
+    await run(SITES[1], getterThrows(), CONSTANT);
+  });
+  it('RED ks1868 R5: a revoked Proxy on GET /api/timestamps/hash/:hash is logged as text and the route answers 200', async () => {
+    await run(SITES[2], revokedProxy(), CONSTANT);
+  });
+  it('RED ks1868 R6: an Error whose message getter throws on GET /api/timestamps/hash/:hash is logged as text and the route answers 200', async () => {
+    await run(SITES[2], getterThrows(), CONSTANT);
+  });
+});
```
