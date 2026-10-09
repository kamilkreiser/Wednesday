// KS-1348: under NODE_ENV=production utils/logger.ts adds two File transports (logs/error.log and
// logs/combined.log) and gave them no format, so every line in either file was the literal text
// undefined. Round 2 (#1310) redacted a list of key names and then wrote json() to the files, and
// gate33 held it: a nested Error (its config.headers.Authorization, its toJSON) and every secret or
// PII key the suffix rule does not name (secretKey, privateKey, passwordHash, mnemonic, phone,
// email_address, userEmails, ip) then reached both files, where develop wrote undefined.
// Kam ruled 2026-09-28 (card secuura-ks1348-r2-files-still-leak-allowlist, option a): allow-list the
// file format. The files record ONLY named safe fields (message, error text, request method and
// path, and the line bookkeeping); everything else stays out. Redaction stays on the Console.
//
// The cell loads the REAL module under production through jest.isolateModules (it reads NODE_ENV
// once, at import), with the working directory moved to a fresh temp dir so the relative logs/
// paths land there. It captures what the Console transport would print, logs one error and one info
// line carrying the sentinels, and reads back what winston wrote to each file.
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'fs';
import { EOL, tmpdir } from 'os';
import path from 'path';

type LoggerModule = typeof import('../utils/logger');
type ConsoleLog = (info: Record<symbol, unknown>, next: () => void) => void;

const MESSAGE = Symbol.for('message');
const FILES = ['error.log', 'combined.log'];
const PROBE_MESSAGE = 'Admin config request failed (POST /api/admin/ks1348-probe)';
const PROBE_ERROR = 'ks1348r3-fail500-error-text';
const INFO_MESSAGE = 'ks1348r3 info line reached the combined log';
const RULED = {
  password: 'ks1348r3-pw-hunter2x',
  token: 'ks1348r3-tok-9c1e77',
  apiKey: 'ks1348r3-key-sk-test-4d',
  email: 'ks1348r3.subject@example.test',
  ssn: 'ks1348r3-ssn-987-65-4320',
  authorization: 'ks1348r3-auth-bearer-2b8',
};
const UNNAMED = {
  nestedAuthorization: 'ks1348r3-nested-err-authz-5q1',
  nestedResponseToken: 'ks1348r3-nested-err-token-7m3',
  toJsonAuthorization: 'ks1348r3-tojson-authz-3v8',
  passwordHash: 'ks1348r3-pwhash-8d2',
  privateKey: 'ks1348r3-privkey-1k9',
  secretKey: 'ks1348r3-secretkey-6j4',
  mnemonic: 'ks1348r3-mnemonic-abandon-ability',
  phone: 'ks1348r3-phone-0400111222',
  emailAddress: 'ks1348r3.address@example.test',
  userEmail: 'ks1348r3.listed@example.test',
  ip: 'ks1348r3-ip-203.0.113.9',
  recipientPhone: 'ks1348r3-recipient-phone-0400999888',
  sessionId: 'ks1348r3-session-4w6',
};
const SENTINELS: Record<string, string> = { ...RULED, ...UNNAMED };
const upstream = Object.assign(new Error('ks1348r3 upstream call failed'), {
  config: { headers: { Authorization: UNNAMED.nestedAuthorization } },
  response: { data: { token: UNNAMED.nestedResponseToken } },
});
const upstreamWithToJson = Object.assign(new Error('ks1348r3 upstream with toJSON'), {
  toJSON: () => ({ authorization: UNNAMED.toJsonAuthorization }),
});
const META = {
  error: PROBE_ERROR,
  requestId: 'ks1348r3-request-id',
  method: 'POST',
  path: '/api/admin/ks1348-probe',
  statusCode: 500,
  password: RULED.password,
  token: RULED.token,
  apiKey: RULED.apiKey,
  email: RULED.email,
  subject: { id: 'ks1348r3-subject-id', ssn: RULED.ssn },
  headers: { accept: 'application/json', authorization: RULED.authorization },
  upstream,
  upstreamWithToJson,
  passwordHash: UNNAMED.passwordHash,
  privateKey: UNNAMED.privateKey,
  secretKey: UNNAMED.secretKey,
  mnemonic: UNNAMED.mnemonic,
  phone: UNNAMED.phone,
  email_address: UNNAMED.emailAddress,
  userEmails: [UNNAMED.userEmail],
  ip: UNNAMED.ip,
};
const INFO_META = { requestId: 'ks1348r3-info-request', recipientPhone: UNNAMED.recipientPhone, sessionId: UNNAMED.sessionId };
const ERROR_ENTRY = {
  timestamp: expect.any(String),
  level: 'error',
  service: 'originate',
  message: PROBE_MESSAGE,
  requestId: 'ks1348r3-request-id',
  method: 'POST',
  path: '/api/admin/ks1348-probe',
  statusCode: 500,
  error: PROBE_ERROR,
};
const INFO_ENTRY = { timestamp: expect.any(String), level: 'info', service: 'originate', message: INFO_MESSAGE, requestId: 'ks1348r3-info-request' };
const EXPECTED: Record<string, unknown[]> = { 'error.log': [ERROR_ENTRY], 'combined.log': [ERROR_ENTRY, INFO_ENTRY] };
const ORIGINAL_CWD = process.cwd();
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
const ORIGINAL_LOG_LEVEL = process.env.LOG_LEVEL;
const META_BEFORE = JSON.stringify(META);
const written: Record<string, string[]> = {};
const consoleLines: string[] = [];
let workDir = '';
let transportShape: string[] = [];

function loadLogger(nodeEnv: string): LoggerModule {
  process.env.NODE_ENV = nodeEnv;
  delete process.env.LOG_LEVEL;
  let mod!: LoggerModule;
  jest.isolateModules(() => {
    mod = require('../utils/logger') as LoggerModule;
  });
  return mod;
}

async function readLines(file: string, want: number): Promise<string[]> {
  const lines = (): string[] => (existsSync(file) ? readFileSync(file, 'utf8').split(EOL).filter((l) => l !== '') : []);
  for (let i = 0; i < 100 && lines().length < want; i++) {
    await new Promise((resolve) => setTimeout(resolve, 20));
  }
  return lines();
}

beforeAll(async () => {
  workDir = mkdtempSync(path.join(tmpdir(), 'ks1348r3-'));
  process.chdir(workDir);
  const { logger } = loadLogger('production');
  transportShape = logger.transports.map((t) => {
    const filename = (t as unknown as { filename?: string }).filename;
    return filename ? t.constructor.name + ':' + filename : t.constructor.name;
  });
  for (const t of logger.transports) {
    if (t.constructor.name === 'Console') {
      const capture: ConsoleLog = (info, next) => {
        consoleLines.push(String(info[MESSAGE]));
        next();
      };
      (t as unknown as { log: ConsoleLog }).log = capture;
    }
  }
  logger.error(PROBE_MESSAGE, META);
  logger.info(INFO_MESSAGE, INFO_META);
  for (const file of FILES) written[file] = await readLines(path.join(workDir, 'logs', file), EXPECTED[file].length);
  logger.close();
});

afterAll(() => {
  process.chdir(ORIGINAL_CWD);
  if (ORIGINAL_NODE_ENV === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = ORIGINAL_NODE_ENV;
  if (ORIGINAL_LOG_LEVEL === undefined) delete process.env.LOG_LEVEL;
  else process.env.LOG_LEVEL = ORIGINAL_LOG_LEVEL;
  rmSync(workDir, { recursive: true, force: true });
});

function parseEach(lines: string[]): unknown[] {
  return lines.map((l) => {
    try {
      return JSON.parse(l) as unknown;
    } catch {
      return l;
    }
  });
}

function leakedIn(text: string, sentinels: Record<string, string>): string[] {
  return Object.entries(sentinels).filter(([, value]) => text.includes(value)).map(([key]) => key);
}

describe('KS-1348: originate production file logs record only the allow-listed fields; the Console stays redacted', () => {
  it.each(FILES)('RED KS-1348 A1 logs/%s: each line is JSON holding EXACTLY the allow-listed fields and nothing else', (file) => {
    expect({ file, entries: parseEach(written[file]) }).toEqual({ file, entries: EXPECTED[file] });
  });

  it.each(FILES)('RED KS-1348 A3 logs/%s: no sentinel of any shape is in the file, and the message and error text are', (file) => {
    const text = written[file].join(EOL);
    expect({ file, leaked: leakedIn(text, SENTINELS), message: text.includes(PROBE_MESSAGE), error: text.includes(PROBE_ERROR) }).toEqual({ file, leaked: [], message: true, error: true });
  });

  it('RED KS-1348 B1: the Console line carries the message with the six ruled keys redacted and none of their values', () => {
    const line = consoleLines.find((l) => l.includes(PROBE_MESSAGE)) ?? '';
    expect({ leaked: leakedIn(line, RULED), markers: line.split('[REDACTED]').length - 1, error: line.includes(PROBE_ERROR) }).toEqual({ leaked: [], markers: 6, error: true });
  });

  it.each(FILES)('control KS-1348 A0 logs/%s: the expected number of lines was written, so A1 and A3 read a real write', (file) => {
    expect({ file, lines: written[file].length }).toEqual({ file, lines: EXPECTED[file].length });
  });

  it('control KS-1348 A2: the module loaded its production shape, one Console and the two File transports', () => {
    expect(transportShape).toEqual(['Console', 'File:error.log', 'File:combined.log']);
  });

  it('control KS-1348 A4: the probe really carries every sentinel, so A3 is not vacuous', () => {
    const probe = JSON.stringify(META) + JSON.stringify(INFO_META);
    expect(leakedIn(probe, SENTINELS)).toEqual(Object.keys(SENTINELS));
  });

  it('control KS-1348 A5: the caller metadata object is left untouched by the logger', () => {
    expect(JSON.stringify(META)).toBe(META_BEFORE);
  });

  it('control KS-1348 C1: the Console transport printed both lines', () => {
    expect(consoleLines.length).toBe(2);
  });
});
