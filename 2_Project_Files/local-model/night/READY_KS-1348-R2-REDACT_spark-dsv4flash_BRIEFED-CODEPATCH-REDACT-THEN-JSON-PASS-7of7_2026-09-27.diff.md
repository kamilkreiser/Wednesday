# CORRECTION by Wednesday 19:21 AEST 2026-09-27: SPARK run (deepseek-v4-flash-0731), NOT Ornith (hold_ready template); renamed by Wednesday. The FIRST checker pass FAILED on the HARNESS (prepare_clone: no node_modules in the brief-writer's source clone), not the model; RE-CHECK of the SAME out.md with source_checkout -> a clone that has node_modules (input_recheck.json; the failed artefacts kept as *.prepfail): PASS 7/7 strict, A2a 2/2. Round counter: 1 model round.
# BYTE PROOF: out.md.checker/patch.diff BYTE-IDENTICAL to night/briefs/KS-1348-r2/KS-1348.golden.diff (cmp rc 0). Golden proven by the brief-writer: red 5/10 (declared cells by assertion), green 10/10, originate 983->993 0 failed, variant arms (json-only 5 fail, non-recursive 5, json dropped 4, email removed 4). PR NOTES: Kam's ruling secuura-ks1348-log-files-persist-secrets => a (2026-09-27 19:06, 'Redact first, then JSON files'). A FRESH PR from develop a24db57e65c9 REPLACING #1302 (close #1302 citing the ruling; round 2 of 2 at the cap). `Refs KS-1348`, NO closing keyword. TIER 1. State in the body: redaction runs in EVERY environment (dev console shows [REDACTED]), and the key-suffix matching limits named in the brief README.
# READY — KS-1348-KS-1348-R2-REDACT (Ornith, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1348-r2/out.md.checker/patch.diff`** (from `ls` at 19:21 2026-09-27; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1348-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1348-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 19:21 2026-09-27 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1348-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `a24db57e65c9d0b96e8560ea7feaa0c764dee564`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/utils/logger.ts , Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/logger.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
29	2	Blockchain/Dev/services/originate/src/utils/logger.ts
146	0	Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (26 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 29 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/utils/logger.ts byte-exact incl. leading whitespace (apply mode strict): OK 26 line(s) byte-exact incl. leading whitespace (of 26; 29 line(s) added by the apply)` [a3i_indent.out: `OK 26 line(s) byte-exact incl. leading whitespace (of 26; 29 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/logger.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts fails at the untouched tip (5 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=5 of total=10; red cell(s): ['KS-1348: originate production file logs are JSON lines with every secret and PII value redacted RED KS-1348 A1 logs/error.log: the line is JSON carrying the message, the error text and the plain fields, with each secret key redacted', 'KS-1348: originate production file logs are JSON lines with every secret and PII value redacted RED KS-1348 A1 logs/combined.log: the line is JSON carrying the message, the error text and the plain fields, with each secret key redacted', 'KS-1348: originate production file logs are JSON lines with every secret and PII value redacted RED KS-1348 A3 logs/error.log: no sentinel value is in the file, and the six redaction markers are', 'KS-1348: originate production file logs are JSON lines with every secret and PII value redacted RED KS-1348 A3 logs/combined.log: no sentinel value is in the file, and the six redaction markers are', 'KS-1348: originate production file logs are JSON lines with every secret and PII value redacted RED KS-1348 B1: the logger-level format, which feeds the Console as well as the files, redacts before any transport']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts passes with the product hunk (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=983 failed=0 | after: total=993 failed=0` · `NEW reds: []` [baseline_suite.json total=983 failed=0; after_suite.json total=993 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +175/-2 test=src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/logger.ts` (+29/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts` (+146/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `a24db57e65c9d0b96e8560ea7feaa0c764dee564` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1348-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-27_KS-1348-r2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/utils/logger.ts
+++ b/Blockchain/Dev/services/originate/src/utils/logger.ts
@@ -42,7 +42,33 @@
+// KS-1348: every transport (the Console and both production files) first passes through this
+// logger-level redaction. The VALUE of any key naming a secret or PII field is replaced by
+// [REDACTED], at any depth: the packages/shared logger list, matched case-insensitively on the
+// key ending, so recipientEmail and accessToken match too. The message and the error text stay
+// readable, because that is what fail500 exists to log. The production File transports then render
+// JSON, as the production Console does, so the files hold text rather than the literal undefined.
+const SENSITIVE_LOG_KEY = /(password|passwd|secret|token|apikey|api_key|api-key|authorization|cookie|ssn|email|creditcard|phonenumber)$/i;
+
+function redactLogValue(key: string, value: unknown, depth: number): unknown {
+  if (SENSITIVE_LOG_KEY.test(key)) return '[REDACTED]';
+  if (value === null || typeof value !== 'object' || value instanceof Error || value instanceof Date || ArrayBuffer.isView(value)) return value;
+  if (depth >= 10) return '[TRUNCATED]';
+  if (Array.isArray(value)) return value.map((item) => redactLogValue('', item, depth + 1));
+  const copy: Record<string, unknown> = {};
+  for (const [k, v] of Object.entries(value)) copy[k] = redactLogValue(k, v, depth + 1);
+  return copy;
+}
+
+const redactSecrets = winston.format((info) => {
+  const copy = { ...info };
+  for (const key of Object.keys(copy)) {
+    if (key !== 'level' && key !== 'message') copy[key] = redactLogValue(key, copy[key], 0);
+  }
+  return copy;
+});
+
 // File transports for production
 if (nodeEnv === 'production') {
   transports.push(
-    new winston.transports.File({ filename: 'logs/error.log', level: 'error', maxsize: 10_000_000, maxFiles: 5 }),
-    new winston.transports.File({ filename: 'logs/combined.log', maxsize: 10_000_000, maxFiles: 5 }),
+    new winston.transports.File({ filename: 'logs/error.log', level: 'error', format: combine(json()), maxsize: 10_000_000, maxFiles: 5 }),
+    new winston.transports.File({ filename: 'logs/combined.log', format: combine(json()), maxsize: 10_000_000, maxFiles: 5 }),
   );
 }
@@ -53,6 +79,7 @@
   format: combine(
     errors({ stack: true }),
     timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
+    redactSecrets(),
   ),
   transports,
 });
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-redact-secrets.test.ts
@@ -0,0 +1,146 @@
+// KS-1348: under NODE_ENV=production utils/logger.ts adds two File transports (logs/error.log and
+// logs/combined.log) and gave them no format, so every line written to either file was the literal
+// text undefined. The first fix (#1302) gave them json() alone, and gate31 held it: every secret and
+// PII field of a logged metadata object then reached both files, nested ones included.
+// Kam ruled 2026-09-27 (card secuura-ks1348-log-files-persist-secrets, option a): redact first, then
+// JSON files. A logger-level format replaces the VALUE of every secret or PII key, at any depth, with
+// [REDACTED] before any transport runs; the message and the error text still reach the files.
+//
+// The cell loads the REAL module under production through jest.isolateModules (it reads NODE_ENV
+// once, at import), with the working directory moved to a fresh temp dir so the relative logs/
+// paths land there, logs one error carrying six sentinels, and reads back what winston wrote.
+import { existsSync, mkdtempSync, readFileSync, rmSync } from 'fs';
+import { EOL, tmpdir } from 'os';
+import path from 'path';
+
+type LoggerModule = typeof import('../utils/logger');
+
+const FILES = ['error.log', 'combined.log'];
+const PROBE_MESSAGE = 'Admin config request failed (POST /api/admin/ks1348-probe)';
+const PROBE_ERROR = 'ks1348-fail500-error-text';
+const SENTINELS = {
+  password: 'ks1348-pw-hunter2x',
+  token: 'ks1348-tok-9c1e77',
+  apiKey: 'ks1348-key-sk-test-4d',
+  email: 'ks1348.subject@example.test',
+  ssn: 'ks1348-ssn-987-65-4320',
+  authorization: 'ks1348-auth-bearer-2b8',
+};
+const META = {
+  error: PROBE_ERROR,
+  requestId: 'ks1348-request-id',
+  password: SENTINELS.password,
+  token: SENTINELS.token,
+  apiKey: SENTINELS.apiKey,
+  email: SENTINELS.email,
+  subject: { id: 'ks1348-subject-id', ssn: SENTINELS.ssn },
+  headers: { accept: 'application/json', authorization: SENTINELS.authorization },
+};
+const REDACTED_ENTRY = {
+  level: 'error',
+  message: PROBE_MESSAGE,
+  service: 'originate',
+  error: PROBE_ERROR,
+  requestId: 'ks1348-request-id',
+  password: '[REDACTED]',
+  token: '[REDACTED]',
+  apiKey: '[REDACTED]',
+  email: '[REDACTED]',
+  subject: { id: 'ks1348-subject-id', ssn: '[REDACTED]' },
+  headers: { accept: 'application/json', authorization: '[REDACTED]' },
+};
+const ORIGINAL_CWD = process.cwd();
+const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
+const ORIGINAL_LOG_LEVEL = process.env.LOG_LEVEL;
+const META_BEFORE = JSON.stringify(META);
+const written: Record<string, string[]> = {};
+let workDir = '';
+let transportShape: string[] = [];
+let loggerFormat: LoggerModule['logger']['format'];
+
+function loadLogger(nodeEnv: string): LoggerModule {
+  process.env.NODE_ENV = nodeEnv;
+  delete process.env.LOG_LEVEL;
+  let mod!: LoggerModule;
+  jest.isolateModules(() => {
+    mod = require('../utils/logger') as LoggerModule;
+  });
+  return mod;
+}
+
+async function readLines(file: string): Promise<string[]> {
+  for (let i = 0; i < 100 && !(existsSync(file) && readFileSync(file, 'utf8').includes(EOL)); i++) {
+    await new Promise((resolve) => setTimeout(resolve, 20));
+  }
+  return existsSync(file) ? readFileSync(file, 'utf8').split(EOL).filter((l) => l !== '') : [];
+}
+
+beforeAll(async () => {
+  workDir = mkdtempSync(path.join(tmpdir(), 'ks1348-'));
+  process.chdir(workDir);
+  const { logger } = loadLogger('production');
+  loggerFormat = logger.format;
+  transportShape = logger.transports.map((t) => {
+    const filename = (t as unknown as { filename?: string }).filename;
+    return filename ? t.constructor.name + ':' + filename : t.constructor.name;
+  });
+  for (const t of logger.transports) {
+    if (t.constructor.name === 'Console') t.silent = true;
+  }
+  logger.error(PROBE_MESSAGE, META);
+  for (const file of FILES) written[file] = await readLines(path.join(workDir, 'logs', file));
+  logger.close();
+});
+
+afterAll(() => {
+  process.chdir(ORIGINAL_CWD);
+  if (ORIGINAL_NODE_ENV === undefined) delete process.env.NODE_ENV;
+  else process.env.NODE_ENV = ORIGINAL_NODE_ENV;
+  if (ORIGINAL_LOG_LEVEL === undefined) delete process.env.LOG_LEVEL;
+  else process.env.LOG_LEVEL = ORIGINAL_LOG_LEVEL;
+  rmSync(workDir, { recursive: true, force: true });
+});
+
+function parseEach(lines: string[]): unknown[] {
+  return lines.map((l) => {
+    try {
+      return JSON.parse(l) as unknown;
+    } catch {
+      return l;
+    }
+  });
+}
+
+describe('KS-1348: originate production file logs are JSON lines with every secret and PII value redacted', () => {
+  it.each(FILES)('RED KS-1348 A1 logs/%s: the line is JSON carrying the message, the error text and the plain fields, with each secret key redacted', (file) => {
+    expect({ file, entries: parseEach(written[file]) }).toEqual({ file, entries: [expect.objectContaining(REDACTED_ENTRY)] });
+  });
+
+  it.each(FILES)('RED KS-1348 A3 logs/%s: no sentinel value is in the file, and the six redaction markers are', (file) => {
+    const text = written[file].join(EOL);
+    const leaked = Object.entries(SENTINELS).filter(([, value]) => text.includes(value)).map(([key]) => key);
+    expect({ file, leaked, markers: text.split('[REDACTED]').length - 1 }).toEqual({ file, leaked: [], markers: 6 });
+  });
+
+  it('RED KS-1348 B1: the logger-level format, which feeds the Console as well as the files, redacts before any transport', () => {
+    const out = loggerFormat.transform({ level: 'error', message: PROBE_MESSAGE, ...META }, {}) as Record<string, unknown>;
+    expect(out).toEqual(expect.objectContaining({ message: PROBE_MESSAGE, error: PROBE_ERROR, password: '[REDACTED]', subject: { id: 'ks1348-subject-id', ssn: '[REDACTED]' }, headers: { accept: 'application/json', authorization: '[REDACTED]' } }));
+  });
+
+  it.each(FILES)('control KS-1348 A0 logs/%s: exactly one line was written, so A1 and A3 read a real write', (file) => {
+    expect({ file, lines: written[file].length }).toEqual({ file, lines: 1 });
+  });
+
+  it('control KS-1348 A2: the module loaded its production shape, one Console and the two File transports', () => {
+    expect(transportShape).toEqual(['Console', 'File:error.log', 'File:combined.log']);
+  });
+
+  it('control KS-1348 A4: the probe really carries all six sentinels, so A3 is not vacuous', () => {
+    const probe = JSON.stringify(META);
+    expect(Object.values(SENTINELS).filter((value) => probe.includes(value)).length).toBe(6);
+  });
+
+  it('control KS-1348 A5: the caller metadata object is left untouched by the logger', () => {
+    expect(JSON.stringify(META)).toBe(META_BEFORE);
+  });
+});
```
