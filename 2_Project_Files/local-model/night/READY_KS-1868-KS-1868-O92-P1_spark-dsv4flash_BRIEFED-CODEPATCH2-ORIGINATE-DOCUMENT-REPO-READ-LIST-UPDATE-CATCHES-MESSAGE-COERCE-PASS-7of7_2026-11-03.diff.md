# READY — KS-1868-KS-1868-O92-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 08:31 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:31 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `b85b7b6786fa6329b6f781cebf2475147738004e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/repositories/documentRepo.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/repositories/documentRepo.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
25	4	Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
143	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (25 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: documentRepo.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/repositories/documentRepo.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/repositories/documentRepo.ts 25 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts 143 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/repositories/documentRepo.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=6 of total=10; red cell(s): ['KS-1868 the originate documentRepo read, list and update catches log text for a hostile thrown value RED ks1868 R1: a read failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', 'KS-1868 the originate documentRepo read, list and update catches log text for a hostile thrown value RED ks1868 R2: a read failure that is an Error whose message getter throws is logged as text and rethrown as is, as for an ordinary Error', 'KS-1868 the originate documentRepo read, list and update catches log text for a hostile thrown value RED ks1868 R3: a list failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', 'KS-1868 the originate documentRepo read, list and update catches log text for a hostile thrown value RED ks1868 R4: a list failure that is an Error whose message getter throws is logged as text and rethrown as is, as for an ordinary Error', 'KS-1868 the originate documentRepo read, list and update catches log text for a hostile thrown value RED ks1868 R5: an update failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', 'KS-1868 the originate documentRepo read, list and update catches log text for a hostile thrown value RED ks1868 R6: an update failure that is an Error whose message getter throws is logged as text and rethrown as is, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2349 failed=11 | after: total=2359 failed=11` · `NEW reds: []` [baseline_suite.json total=2349 failed=11; after_suite.json total=2359 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/repositories/documentRepo.ts` (+25/-4 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts` (+143/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/repositories/documentRepo.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `b85b7b6786fa6329b6f781cebf2475147738004e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p1_originate_document_repo_read_list_update_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts b/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
--- a/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
+++ b/Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
@@ -262,8 +262,17 @@
     if (rows.length > 0) return fromDbRow(rows[0]);
     return null;
   } catch (err: any) {
-    if (!err?.message?.includes('invalid input syntax for type uuid')) {
-      logger.warn('DB read failed', { error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    let isUuidSyntax = false;
+    try {
+      isUuidSyntax = !!err?.message?.includes('invalid input syntax for type uuid');
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      isUuidSyntax = false;
+      reason = 'unreadable thrown value';
+    }
+    if (!isUuidSyntax) {
+      logger.warn('DB read failed', { error: reason });
     }
     throw err;
   }
@@ -296,6 +305,12 @@
     return { items: paginated, total: all.length };
   } catch (err: any) {
-    logger.warn('DB list failed', { error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB list failed', { error: reason });
     throw err;
   }
 }
@@ -694,6 +709,12 @@
     // so both writers could pass it and both recorded a revocation.
     if (guardStatus !== null && affected === 0) return null;
   } catch (err: any) {
-    logger.error('DB update failed for document', { id, error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('DB update failed for document', { id, error: reason });
     throw err;
   }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts
@@ -0,0 +1,143 @@
+// KS-1868 (operator 92 screen, originate documentRepo): the read catch of getDocument (line 265), the list catch of listDocuments (line 298) and the
+// update catch of updateDocument (line 697) of services/originate/src/repositories/documentRepo.ts read the thrown value inside the logger call's
+// arguments, unguarded (`err?.message?.includes(...)` then `err instanceof Error ? err.message : String(err)`). A thrown value whose read throws (a revoked
+// Proxy, an Error whose message getter throws) makes the catch itself throw: the line is never logged and the caller sees the TypeError of the failed read
+// where an ordinary Error is logged and rethrown as is. The cells make the database stand-in reject with such a value and assert the original value is
+// rethrown and the logged line carries text (the constant when the value cannot be turned into text). The uuid-syntax refusal of getDocument stays
+// unlogged. Harness: the real module with ../db and ../utils/logger replaced by plain stand-ins; the database stand-in is passed as the `db` argument
+// (no database, no network).
+const mockH: { logs: { level: string; message: string; meta: Record<string, unknown> | undefined }[] } = { logs: [] };
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: () => Promise.resolve([]), $executeRaw: () => Promise.resolve(0) },
+  withTenant: () => undefined,
+}));
+jest.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    mockH.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+import { getDocument, listDocuments, updateDocument } from '../repositories/documentRepo';
+
+const TENANT = '33333333-3333-4333-8333-333333333333';
+const ROW = {
+  id: '11111111-1111-4111-8111-111111111111',
+  external_id: 'doc-ks1868',
+  document_type: 'document',
+  status: 'draft',
+  owner_user_id: '22222222-2222-4222-8222-222222222222',
+  title: 'ks1868',
+  content_hash: 'h',
+  metadata: {},
+  certification_metadata: {},
+};
+const READ = 'DB read failed';
+const LIST = 'DB list failed';
+const UPDATE = 'DB update failed for document';
+
+beforeEach(() => {
+  mockH.logs.length = 0;
+});
+
+const LINES = (message: string) => mockH.logs.filter((l) => l.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string => {
+  const v = l?.meta?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+/** A database stand-in whose read rejects with the value. */
+const readFails = (value: unknown): any => ({
+  $queryRaw: () => Promise.reject(value),
+  $executeRaw: () => Promise.resolve(0),
+});
+/** A database stand-in whose read answers one row and whose write rejects with the value. */
+const writeFails = (value: unknown): any => ({
+  $queryRaw: () => Promise.resolve([ROW]),
+  $executeRaw: () => Promise.reject(value),
+});
+
+async function outcome(fn: () => Promise<unknown>, value: unknown): Promise<{ rejected: boolean; same: boolean }> {
+  try {
+    await fn();
+    return { rejected: false, same: false };
+  } catch (e) {
+    return { rejected: true, same: Object.is(e, value) };
+  }
+}
+const read = (value: unknown) => outcome(() => getDocument('doc-ks1868', TENANT, readFails(value)), value);
+const list = (value: unknown) => outcome(() => listDocuments(TENANT, undefined, readFails(value)), value);
+const update = (value: unknown) => outcome(() => updateDocument('doc-ks1868', TENANT, { status: 'signed' }, writeFails(value)), value);
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
+const CONSTANT = 'unreadable thrown value';
+
+describe('KS-1868 the originate documentRepo read, list and update catches log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the read is logged with its message and rethrown as is', async () => {
+    const e = new Error('read boom');
+    expect(await read(e)).toEqual({ rejected: true, same: true });
+    expect(LINES(READ)).toHaveLength(1);
+    expect(reasonOf(LINES(READ)[0])).toBe('read boom');
+  });
+  it('control ks1868 C2: a uuid-syntax Error from the read is rethrown as is and not logged', async () => {
+    const e = new Error('invalid input syntax for type uuid: "x"');
+    expect(await read(e)).toEqual({ rejected: true, same: true });
+    expect(LINES(READ)).toHaveLength(0);
+  });
+  it('control ks1868 C3: an ordinary Error from the list is logged with its message and rethrown as is', async () => {
+    const e = new Error('list boom');
+    expect(await list(e)).toEqual({ rejected: true, same: true });
+    expect(LINES(LIST)).toHaveLength(1);
+    expect(reasonOf(LINES(LIST)[0])).toBe('list boom');
+  });
+  it('control ks1868 C4: an ordinary Error from the update is logged with its message and rethrown as is', async () => {
+    const e = new Error('update boom');
+    expect(await update(e)).toEqual({ rejected: true, same: true });
+    expect(LINES(UPDATE)).toHaveLength(1);
+    expect(reasonOf(LINES(UPDATE)[0])).toBe('update boom');
+  });
+  it('RED ks1868 R1: a read failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await read(revokedProxy())).toEqual({ rejected: true, same: true });
+    expect(LINES(READ)).toHaveLength(1);
+    expect(reasonOf(LINES(READ)[0])).toBe(CONSTANT);
+  });
+  it('RED ks1868 R2: a read failure that is an Error whose message getter throws is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await read(getterThrows())).toEqual({ rejected: true, same: true });
+    expect(LINES(READ)).toHaveLength(1);
+    expect(reasonOf(LINES(READ)[0])).toBe(CONSTANT);
+  });
+  it('RED ks1868 R3: a list failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await list(revokedProxy())).toEqual({ rejected: true, same: true });
+    expect(LINES(LIST)).toHaveLength(1);
+    expect(reasonOf(LINES(LIST)[0])).toBe(CONSTANT);
+  });
+  it('RED ks1868 R4: a list failure that is an Error whose message getter throws is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await list(getterThrows())).toEqual({ rejected: true, same: true });
+    expect(LINES(LIST)).toHaveLength(1);
+    expect(reasonOf(LINES(LIST)[0])).toBe(CONSTANT);
+  });
+  it('RED ks1868 R5: an update failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await update(revokedProxy())).toEqual({ rejected: true, same: true });
+    expect(LINES(UPDATE)).toHaveLength(1);
+    expect(reasonOf(LINES(UPDATE)[0])).toBe(CONSTANT);
+  });
+  it('RED ks1868 R6: an update failure that is an Error whose message getter throws is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await update(getterThrows())).toEqual({ rejected: true, same: true });
+    expect(LINES(UPDATE)).toHaveLength(1);
+    expect(reasonOf(LINES(UPDATE)[0])).toBe(CONSTANT);
+  });
+});
```
