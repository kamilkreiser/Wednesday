# KS-1239 R16B-RAWAUTHDEAD - Wednesday's task for Ornith: the api-gateway's pre-auth `rawAuthorization` capture (`index.ts:345-:350`, with its BUG-PLATFORM-AUTH-001 comment `:335-:344`) is DEAD CODE with 0 readers since #1034 (KS-1215) - DELETE it (ONE product hunk, a PURE DELETION, no `+` line) and pin it gone with ONE NEW vitest file that reads the gateway source (code_patch, VITEST, written 15:00:41 AEST on 2026-09-22 by Wednesday's feed13 drafter from `index.ts` read WHOLE at develop 3bad652d1: 1279 lines)
Tip: `3bad652d17cf111c1e2e1bed1ae7686894637487`
Runner: `vitest`

## Premises (measured by the feed13 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Ticket KS-1239 (Backlog, P4, unassigned, no PR attached; board read at boot): after #1034 (KS-1215) `routes/platform.ts` `authHeaders` (`:211-:215`) forwards `req.headers.authorization`; the capture at `index.ts:347` `(req as any).rawAuthorization = req.headers.authorization;` has NO reader. Measured at the tip with `git grep` over `Blockchain/Dev/`: `rawAuthorization` = 4 hits, ONE write (`index.ts:347`) and THREE comments (`platform.ts:204`, `ks1215-...test.ts:24`, `ks1238-...test.ts:5`) - 0 readers, exactly as the ticket says.
- `index.ts` at the tip: last touched by `97576e8a5` (2026-09-21); the block below is at `:334-:351` with offset 0. The lines: `:334` blank; `:335-:344` the ten-line `// BUG-PLATFORM-AUTH-001 (2026-05-01): capture the raw Authorization header ...` comment; `:345` `app.use((req, _res, next) => {`; `:346` `  if (req.headers.authorization) {`; `:347` the capture; `:348` `  }`; `:349` `  next();`; `:350` `});`; `:351` blank. Before it (`:326-:333`) the trust-header strip middleware (its `stripTrustHeaders(...)` at `:331`, `next();` `:332`, `});` `:333`); after it (`:352-:354`) the `// AUDIT B-7 / D-2` comment.
- Why the hunk is cut where it is: NO blank line is asked of you as CONTEXT (the builder refuses blank context). The two blanks that bracket the block (`:334` and `:351`) are BOTH `-` lines inside the hunk, so the leading context is the three non-blank lines `:331-:333` and the trailing context the three non-blank lines `:352-:354`; after the patch `:333` `});` is followed directly by `:352`'s `// AUDIT B-7 / D-2: ...` comment (no blank between them - tsc does not care and there is no formatter gate in the checker). Old side 24 lines, new side 6: header `@@ -331,24 +331,6 @@`. Strict `git apply --check` rc 0 measured at the tip (the golden PASSes the real checker in the precheck clone).
- The test is a NEW vitest file that reads `index.ts` and `routes/platform.ts` as TEXT (`readFileSync(join(__dirname, '..', 'index.ts'), 'utf8')`) - the shape `ks689-users-admin-create-auth-mount.test.ts` (`:24-:27`, reads `routes/proxy.ts`) and `ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts:142` already use in this directory; it is the honest pin for a dead-code deletion (no request can observe a write nobody reads). Two RED cells by assertion at the tip (`rawAuthorization` occurs 1 time in `index.ts`; `BUG-PLATFORM-AUTH-001` 1 time), two CONTROL cells green on both trees (`stripTrustHeaders(...)` mounted once; `platform.ts` `const auth = req.headers.authorization;` once and no `rawAuthorization` reader). `__dirname` is available under the service's vitest config (ks689 and ks1165 use it and are green at the tip - baseline suite loaded).
- Every `+` line of the test is ASCII-only, backslash-free and carries NO double-quote character (asserted by the writer script); needles are single-quoted strings; `occurrences()` is `split(needle).length - 1` - no regex anywhere.
- Collision check: `api-gateway` is in NEITHER round-19 lane (Seat B 19th = originate/kyc/security/packages/shared/systemTest/performance; Seat C 19th = repo-root CLAUDE.md/.githooks/docs/scripts/Start_Up/systemTest/schemathesis - the two briefs' GROUPING tables, `exclusion_set.log`: 47 paths, none under `services/api-gateway/`); no held READY of 2026-09-2[0-2] names `api-gateway/src/index.ts`; not one of the tickets Kam's counter sent to Claude; not an auth/MFA/OAuth PRODUCT edit (the deleted middleware is a header COPY nobody reads - authentication itself is untouched).

## What is wrong (one paragraph)
`Blockchain/Dev/services/api-gateway/src/index.ts:345-:350` mounts a middleware at request entry that copies `req.headers.authorization` onto `(req as any).rawAuthorization` BEFORE authentication runs (BUG-PLATFORM-AUTH-001, 2026-05-01, so that `routes/platform.ts` could forward the original bearer to tenant-provisioning). #1034 (KS-1215) removed the only reader: `platform.ts` `authHeaders` (`:211-:215`) now forwards the Authorization the auth middleware LEFT in place, because the raw copy sent a caller's Bearer (a revoked session's too) to `/api/tenants`, `/api/keys` and `/api/audit` on the connector branch. The capture is now dead code (0 readers at the tip) and is exactly the trap KS-1215 fell into - a pre-auth copy that `delete req.headers.authorization` cannot affect. The fix is the deletion of the comment and the middleware, nothing else. NOT in this task: `platform.ts`, the trust-header strip (`:326-:333`), the CORS block (`:352-`), the ks1215 / ks1238 suites (their `rawAuthorization` mentions are comments describing the old shape and stay).

## The exact change - ONE EDIT in the product file (one hunk, a PURE DELETION; copy the header)
E1 (hunk 1, header `@@ -331,24 +331,6 @@`) - the eighteen `-` lines are the tip's `:334` (blank - written as a lone `-`), `:335-:344` (the ten comment lines), `:345-:350` (the six middleware lines) and `:351` (blank - a lone `-`). Leading context `:331-:333` (`  stripTrustHeaders(...)`, `  next();`, `});` - all three STAY), trailing context `:352-:354` (the first three `// AUDIT B-7 / D-2` comment lines - all STAY). There is NO `+` line: do not add a replacement line, do not re-add a deleted line as a `+`, do not add a blank `+`.
```
@@ -331,24 +331,6 @@
   stripTrustHeaders(req.headers as unknown as Record<string, unknown>);
   next();
 });
-
-// BUG-PLATFORM-AUTH-001 (2026-05-01): capture the raw Authorization header
-// at request entry, BEFORE any other middleware can mutate or consume
-// req.headers.authorization. Some downstream proxy paths (e.g.
-// routes/platform.ts → tenant-provisioning) need to forward the original
-// bearer token to internal services that JWT-verify directly. Symptom
-// before this fix: GET /api/platform/tenants returned 502 because the
-// inline proxy's `req.headers.authorization` read was empty by the time
-// the handler ran, and tenant-prov returned `Error: No token provided`,
-// which gateway's `r.json()` then failed to parse (HTML stack trace),
-// producing an unhelpful 502.
-app.use((req, _res, next) => {
-  if (req.headers.authorization) {
-    (req as any).rawAuthorization = req.headers.authorization;
-  }
-  next();
-});
-
 // AUDIT B-7 / D-2: refuse to start with wildcard origin in production-like
 // environments. With credentials:true, `*` is spec-illegal AND a CSRF
 // refresh-token exfil risk. Same rule for any wildcard-subdomain entry.
```
There are exactly 0 `+` lines in the product hunk; every `-` line is the tip's line exactly (a blank tip line is a lone `-`); every context line keeps its leading space (`  stripTrustHeaders` has two spaces at the tip, so its context line has three; `});` is at column 0, so its context line is ` });` - one space). Do NOT touch `:331-:333` or `:352-:354` beyond copying them as context.

## THIS IS VITEST
`repo.test_runner` begins with `vitest`. `describe/it/expect` are imported from `'vitest'`; NO `jest.*`, no `vi.mock` needed (the suite reads files, it imports no gateway module).

## The test - one NEW vitest file that reads the gateway source (the ks689 shape)
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 39), every line with a leading `+` (a blank line is a lone `+`). Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only, no `$` anywhere.
```
+/**
+ * KS-1239: index.ts:347 copied req.headers.authorization onto req.rawAuthorization at request
+ * entry, BEFORE authentication ran. #1034 (KS-1215) made routes/platform.ts authHeaders forward
+ * req.headers.authorization instead, so the copy has 0 readers at the tip and is exactly the trap
+ * KS-1215 fell into: a pre-auth copy that delete req.headers.authorization cannot touch. This
+ * suite reads the gateway source the way ks689-users-admin-create-auth-mount.test.ts does and
+ * pins that the copy is gone and that nothing reads it.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const GATEWAY_SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');
+const PLATFORM_SRC = readFileSync(join(__dirname, '..', 'routes', 'platform.ts'), 'utf8');
+
+function occurrences(haystack: string, needle: string): number {
+  return haystack.split(needle).length - 1;
+}
+
+describe('KS-1239: the pre-auth rawAuthorization copy in index.ts is dead code and is gone', () => {
+  it('RED KS-1239 A: index.ts takes no rawAuthorization copy of the Authorization header', () => {
+    expect(occurrences(GATEWAY_SRC, 'rawAuthorization')).toBe(0);
+  });
+
+  it('RED KS-1239 B: no gateway middleware assigns req.headers.authorization onto req before auth runs', () => {
+    expect(occurrences(GATEWAY_SRC, '.rawAuthorization = req.headers.authorization')).toBe(0);
+    expect(occurrences(GATEWAY_SRC, 'BUG-PLATFORM-AUTH-001')).toBe(0);
+  });
+
+  it('control: the trust-header strip stays mounted at request entry', () => {
+    expect(occurrences(GATEWAY_SRC, 'stripTrustHeaders(req.headers as unknown as Record<string, unknown>);')).toBe(1);
+  });
+
+  it('control: routes/platform.ts authHeaders forwards req.headers.authorization and reads no rawAuthorization', () => {
+    expect(occurrences(PLATFORM_SRC, 'const auth = req.headers.authorization;')).toBe(1);
+    expect(occurrences(PLATFORM_SRC, 'req.rawAuthorization')).toBe(0);
+    expect(occurrences(PLATFORM_SRC, '(req as any).rawAuthorization')).toBe(0);
+  });
+});
```
LINE DISCIPLINE: the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string - DECODE them. Every one of the 39 `+` lines above is its OWN physical line of your diff, each starting with its own `+`; NEVER join two lines with a backslash-n pair (a `+` line that carries a backslash is a FAIL). Cells (the two RED cells by assertion at the tip, the two controls green on both trees; nothing optional):
- RED `it('RED KS-1239 A: index.ts takes no rawAuthorization copy of the Authorization header')` - `occurrences(GATEWAY_SRC, 'rawAuthorization')` must be 0. At the tip it is 1 (`:347`) - the red, by assertion; after E1 it is 0.
- RED `it('RED KS-1239 B: no gateway middleware assigns req.headers.authorization onto req before auth runs')` - `'.rawAuthorization = req.headers.authorization'` 0 times and `'BUG-PLATFORM-AUTH-001'` 0 times in `index.ts`. At the tip both are 1 (`:347`, `:335`) - the red; after E1 both 0.
- CONTROL `it('control: the trust-header strip stays mounted at request entry')` - `'stripTrustHeaders(req.headers as unknown as Record<string, unknown>);'` exactly once in `index.ts` (`:331`, E1's first leading context line) - green on both trees.
- CONTROL `it('control: routes/platform.ts authHeaders forwards req.headers.authorization and reads no rawAuthorization')` - in `platform.ts`: `'const auth = req.headers.authorization;'` once (`:214`), `'req.rawAuthorization'` 0, `'(req as any).rawAuthorization'` 0 (`:204` is a comment that says "the `rawAuthorization` copy" - neither needle matches it) - green on both trees.

## Red cells
- RED KS-1239 A: index.ts takes no rawAuthorization copy of the Authorization header
- RED KS-1239 B: no gateway middleware assigns req.headers.authorization onto req before auth runs

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:335` - **must change**: `// BUG-PLATFORM-AUTH-001 (2026-05-01): capture the raw Authorization header` - E1 (deleted; the comment's first line)
* `:346` - **must change**: `  if (req.headers.authorization) {` - E1 (deleted; the middleware's guard - unique in the file; the `app.use((req, _res, next) => {` mount line at `:345` is deleted too but its text occurs three times in the file, so it is not listed as a site)
* `:347` - **must change**: `    (req as any).rawAuthorization = req.headers.authorization;` - E1 (deleted; the capture, the ticket's `:347`)
* `:331` - (correct) `  stripTrustHeaders(req.headers as unknown as Record<string, unknown>);` - stays (E1's first leading context line; the trust-header strip is not this task)
* `:352` - (correct) `// AUDIT B-7 / D-2: refuse to start with wildcard origin in production-like` - stays (E1's first trailing context line)
* `:354` - (correct) `// refresh-token exfil risk. Same rule for any wildcard-subdomain entry.` - stays (E1's last trailing context line)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/index.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/index.ts` with the ONE E1 hunk (header `@@ -331,24 +331,6 @@`, eighteen `-` lines, NO `+` line), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts` (one `@@ -0,0 +1,39 @@` hunk, all `+`); paths repo-rooted (`Blockchain/Dev/...`, never `services/...`); no double quote, no backslash, no non-ASCII character in any `+` line; every `+` line's `(` / `)` and `[` / `]` counts are EXACTLY the fence's - one extra `)` on a `+` line is a FAIL; every context line keeps its leading space; a deleted blank line is a lone `-`; EVERY diff line on its own physical line - never a backslash-n pair joining lines (decode the INPUT JSON's escapes); the cell titles EXACTLY as listed.
