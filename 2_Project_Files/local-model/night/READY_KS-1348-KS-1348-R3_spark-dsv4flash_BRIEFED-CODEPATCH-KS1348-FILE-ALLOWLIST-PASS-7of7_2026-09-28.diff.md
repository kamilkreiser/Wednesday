# READY — KS-1348-KS-1348-R3 (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1348-R3/out.md.checker/patch.diff`** (from `ls` at 07:24 2026-09-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1348-R3/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1348-R3/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1348-R3/out.md.checker/patch.diff /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/golden_KS-1348-R3/out.md.checker/patch.diff` rc 0, Wednesday morning 4901153c).

**Held 07:24 2026-09-28 by Wednesday morning 4901153c after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1348-R3/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/utils/logger.ts , Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/logger.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
41	2	Blockchain/Dev/services/originate/src/utils/logger.ts
203	0	Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (36 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 41 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/utils/logger.ts byte-exact incl. leading whitespace (apply mode strict): OK 36 line(s) byte-exact incl. leading whitespace (of 36; 41 line(s) added by the apply)` [a3i_indent.out: `OK 36 line(s) byte-exact incl. leading whitespace (of 36; 41 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/logger.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1348-production-file-logs-allow-list.test.ts fails at the untouched tip (5 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=5 of total=11; red cell(s): ['KS-1348: originate production file logs record only the allow-listed fields; the Console stays redacted RED KS-1348 A1 logs/error.log: each line is JSON holding EXACTLY the allow-listed fields and nothing else', 'KS-1348: originate production file logs record only the allow-listed fields; the Console stays redacted RED KS-1348 A1 logs/combined.log: each line is JSON holding EXACTLY the allow-listed fields and nothing else', 'KS-1348: originate production file logs record only the allow-listed fields; the Console stays redacted RED KS-1348 A3 logs/error.log: no sentinel of any shape is in the file, and the message and error text are', 'KS-1348: originate production file logs record only the allow-listed fields; the Console stays redacted RED KS-1348 A3 logs/combined.log: no sentinel of any shape is in the file, and the message and error text are', 'KS-1348: originate production file logs record only the allow-listed fields; the Console stays redacted RED KS-1348 B1: the Console line carries the message with the six ruled keys redacted and none of their values']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1348-production-file-logs-allow-list.test.ts passes with the product hunk (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1013 failed=0 | after: total=1024 failed=0` · `NEW reds: []` [baseline_suite.json total=1013 failed=0; after_suite.json total=1024 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +244/-2 test=src/__tests__/ks1348-production-file-logs-allow-list.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/logger.ts` (+41/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts` (+203/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1348-R3/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1348-R3/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/utils/logger.ts
+++ b/Blockchain/Dev/services/originate/src/utils/logger.ts
@@ -42,7 +42,45 @@
+// KS-1348: the Console first passes through this logger-level redaction. The VALUE of any key
+// naming a secret or PII field is replaced by [REDACTED], at any depth: the packages/shared logger
+// list, matched case-insensitively on the key ending, so recipientEmail and accessToken match too.
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
+// KS-1348 r3 (Kam ruled 2026-09-28: allow-list the file format): the production log FILES are a
+// closed world. They record ONLY these named fields, when each is a string or a number, plus the
+// error text when it is a string. Every other key a caller logs, under any name and at any depth,
+// nested Errors included, stays out of the files. The Console keeps the redacted line above.
+const FILE_LOG_FIELDS = ['timestamp', 'level', 'service', 'message', 'requestId', 'method', 'path', 'statusCode'];
+
+const keepFileFields = winston.format((info) => {
+  const kept: Record<string, unknown> = {};
+  for (const key of FILE_LOG_FIELDS) {
+    if (typeof info[key] === 'string' || typeof info[key] === 'number') kept[key] = info[key];
+  }
+  if (typeof info.error === 'string') kept.error = info.error;
+  return kept as winston.Logform.TransformableInfo;
+});
+
 // File transports for production
 if (nodeEnv === 'production') {
   transports.push(
-    new winston.transports.File({ filename: 'logs/error.log', level: 'error', maxsize: 10_000_000, maxFiles: 5 }),
-    new winston.transports.File({ filename: 'logs/combined.log', maxsize: 10_000_000, maxFiles: 5 }),
+    new winston.transports.File({ filename: 'logs/error.log', level: 'error', format: combine(keepFileFields(), json()), maxsize: 10_000_000, maxFiles: 5 }),
+    new winston.transports.File({ filename: 'logs/combined.log', format: combine(keepFileFields(), json()), maxsize: 10_000_000, maxFiles: 5 }),
   );
 }
@@ -53,6 +91,7 @@
   format: combine(
     errors({ stack: true }),
     timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
+    redactSecrets(),
   ),
   transports,
 });
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts
@@ -0,0 +1,203 @@
+// KS-1348: under NODE_ENV=production utils/logger.ts adds two File transports (logs/error.log and
+// logs/combined.log) and gave them no format, so every line in either file was the literal text
+// undefined. Round 2 (#1310) redacted a list of key names and then wrote json() to the files, and
+// gate33 held it: a nested Error (its config.headers.Authorization, its toJSON) and every secret or
+// PII key the suffix rule does not name (secretKey, privateKey, passwordHash, mnemonic, phone,
+// email_address, userEmails, ip) then reached both files, where develop wrote undefined.
+// Kam ruled 2026-09-28 (card secuura-ks1348-r2-files-still-leak-allowlist, option a): allow-list the
+// file format. The files record ONLY named safe fields (message, error text, request method and
+// path, and the line bookkeeping); everything else stays out. Redaction stays on the Console.
+//
+// The cell loads the REAL module under production through jest.isolateModules (it reads NODE_ENV
+// once, at import), with the working directory moved to a fresh temp dir so the relative logs/
+// paths land there. It captures what the Console transport would print, logs one error and one info
+// line carrying the sentinels, and reads back what winston wrote to each file.
+import { existsSync, mkdtempSync, readFileSync, rmSync } from 'fs';
+import { EOL, tmpdir } from 'os';
+import path from 'path';
+
+type LoggerModule = typeof import('../utils/logger');
+type ConsoleLog = (info: Record<symbol, unknown>, next: () => void) => void;
+
+const MESSAGE = Symbol.for('message');
+const FILES = ['error.log', 'combined.log'];
+const PROBE_MESSAGE = 'Admin config request failed (POST /api/admin/ks1348-probe)';
+const PROBE_ERROR = 'ks1348r3-fail500-error-text';
+const INFO_MESSAGE = 'ks1348r3 info line reached the combined log';
+const RULED = {
+  password: 'ks1348r3-pw-hunter2x',
+  token: 'ks1348r3-tok-9c1e77',
+  apiKey: 'ks1348r3-key-sk-test-4d',
+  email: 'ks1348r3.subject@example.test',
+  ssn: 'ks1348r3-ssn-987-65-4320',
+  authorization: 'ks1348r3-auth-bearer-2b8',
+};
+const UNNAMED = {
+  nestedAuthorization: 'ks1348r3-nested-err-authz-5q1',
+  nestedResponseToken: 'ks1348r3-nested-err-token-7m3',
+  toJsonAuthorization: 'ks1348r3-tojson-authz-3v8',
+  passwordHash: 'ks1348r3-pwhash-8d2',
+  privateKey: 'ks1348r3-privkey-1k9',
+  secretKey: 'ks1348r3-secretkey-6j4',
+  mnemonic: 'ks1348r3-mnemonic-abandon-ability',
+  phone: 'ks1348r3-phone-0400111222',
+  emailAddress: 'ks1348r3.address@example.test',
+  userEmail: 'ks1348r3.listed@example.test',
+  ip: 'ks1348r3-ip-203.0.113.9',
+  recipientPhone: 'ks1348r3-recipient-phone-0400999888',
+  sessionId: 'ks1348r3-session-4w6',
+};
+const SENTINELS: Record<string, string> = { ...RULED, ...UNNAMED };
+const upstream = Object.assign(new Error('ks1348r3 upstream call failed'), {
+  config: { headers: { Authorization: UNNAMED.nestedAuthorization } },
+  response: { data: { token: UNNAMED.nestedResponseToken } },
+});
+const upstreamWithToJson = Object.assign(new Error('ks1348r3 upstream with toJSON'), {
+  toJSON: () => ({ authorization: UNNAMED.toJsonAuthorization }),
+});
+const META = {
+  error: PROBE_ERROR,
+  requestId: 'ks1348r3-request-id',
+  method: 'POST',
+  path: '/api/admin/ks1348-probe',
+  statusCode: 500,
+  password: RULED.password,
+  token: RULED.token,
+  apiKey: RULED.apiKey,
+  email: RULED.email,
+  subject: { id: 'ks1348r3-subject-id', ssn: RULED.ssn },
+  headers: { accept: 'application/json', authorization: RULED.authorization },
+  upstream,
+  upstreamWithToJson,
+  passwordHash: UNNAMED.passwordHash,
+  privateKey: UNNAMED.privateKey,
+  secretKey: UNNAMED.secretKey,
+  mnemonic: UNNAMED.mnemonic,
+  phone: UNNAMED.phone,
+  email_address: UNNAMED.emailAddress,
+  userEmails: [UNNAMED.userEmail],
+  ip: UNNAMED.ip,
+};
+const INFO_META = { requestId: 'ks1348r3-info-request', recipientPhone: UNNAMED.recipientPhone, sessionId: UNNAMED.sessionId };
+const ERROR_ENTRY = {
+  timestamp: expect.any(String),
+  level: 'error',
+  service: 'originate',
+  message: PROBE_MESSAGE,
+  requestId: 'ks1348r3-request-id',
+  method: 'POST',
+  path: '/api/admin/ks1348-probe',
+  statusCode: 500,
+  error: PROBE_ERROR,
+};
+const INFO_ENTRY = { timestamp: expect.any(String), level: 'info', service: 'originate', message: INFO_MESSAGE, requestId: 'ks1348r3-info-request' };
+const EXPECTED: Record<string, unknown[]> = { 'error.log': [ERROR_ENTRY], 'combined.log': [ERROR_ENTRY, INFO_ENTRY] };
+const ORIGINAL_CWD = process.cwd();
+const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
+const ORIGINAL_LOG_LEVEL = process.env.LOG_LEVEL;
+const META_BEFORE = JSON.stringify(META);
+const written: Record<string, string[]> = {};
+const consoleLines: string[] = [];
+let workDir = '';
+let transportShape: string[] = [];
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
+async function readLines(file: string, want: number): Promise<string[]> {
+  const lines = (): string[] => (existsSync(file) ? readFileSync(file, 'utf8').split(EOL).filter((l) => l !== '') : []);
+  for (let i = 0; i < 100 && lines().length < want; i++) {
+    await new Promise((resolve) => setTimeout(resolve, 20));
+  }
+  return lines();
+}
+
+beforeAll(async () => {
+  workDir = mkdtempSync(path.join(tmpdir(), 'ks1348r3-'));
+  process.chdir(workDir);
+  const { logger } = loadLogger('production');
+  transportShape = logger.transports.map((t) => {
+    const filename = (t as unknown as { filename?: string }).filename;
+    return filename ? t.constructor.name + ':' + filename : t.constructor.name;
+  });
+  for (const t of logger.transports) {
+    if (t.constructor.name === 'Console') {
+      const capture: ConsoleLog = (info, next) => {
+        consoleLines.push(String(info[MESSAGE]));
+        next();
+      };
+      (t as unknown as { log: ConsoleLog }).log = capture;
+    }
+  }
+  logger.error(PROBE_MESSAGE, META);
+  logger.info(INFO_MESSAGE, INFO_META);
+  for (const file of FILES) written[file] = await readLines(path.join(workDir, 'logs', file), EXPECTED[file].length);
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
+function leakedIn(text: string, sentinels: Record<string, string>): string[] {
+  return Object.entries(sentinels).filter(([, value]) => text.includes(value)).map(([key]) => key);
+}
+
+describe('KS-1348: originate production file logs record only the allow-listed fields; the Console stays redacted', () => {
+  it.each(FILES)('RED KS-1348 A1 logs/%s: each line is JSON holding EXACTLY the allow-listed fields and nothing else', (file) => {
+    expect({ file, entries: parseEach(written[file]) }).toEqual({ file, entries: EXPECTED[file] });
+  });
+
+  it.each(FILES)('RED KS-1348 A3 logs/%s: no sentinel of any shape is in the file, and the message and error text are', (file) => {
+    const text = written[file].join(EOL);
+    expect({ file, leaked: leakedIn(text, SENTINELS), message: text.includes(PROBE_MESSAGE), error: text.includes(PROBE_ERROR) }).toEqual({ file, leaked: [], message: true, error: true });
+  });
+
+  it('RED KS-1348 B1: the Console line carries the message with the six ruled keys redacted and none of their values', () => {
+    const line = consoleLines.find((l) => l.includes(PROBE_MESSAGE)) ?? '';
+    expect({ leaked: leakedIn(line, RULED), markers: line.split('[REDACTED]').length - 1, error: line.includes(PROBE_ERROR) }).toEqual({ leaked: [], markers: 6, error: true });
+  });
+
+  it.each(FILES)('control KS-1348 A0 logs/%s: the expected number of lines was written, so A1 and A3 read a real write', (file) => {
+    expect({ file, lines: written[file].length }).toEqual({ file, lines: EXPECTED[file].length });
+  });
+
+  it('control KS-1348 A2: the module loaded its production shape, one Console and the two File transports', () => {
+    expect(transportShape).toEqual(['Console', 'File:error.log', 'File:combined.log']);
+  });
+
+  it('control KS-1348 A4: the probe really carries every sentinel, so A3 is not vacuous', () => {
+    const probe = JSON.stringify(META) + JSON.stringify(INFO_META);
+    expect(leakedIn(probe, SENTINELS)).toEqual(Object.keys(SENTINELS));
+  });
+
+  it('control KS-1348 A5: the caller metadata object is left untouched by the logger', () => {
+    expect(JSON.stringify(META)).toBe(META_BEFORE);
+  });
+
+  it('control KS-1348 C1: the Console transport printed both lines', () => {
+    expect(consoleLines.length).toBe(2);
+  });
+});
```
