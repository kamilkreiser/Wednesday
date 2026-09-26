// KS-1348: under NODE_ENV=production utils/logger.ts adds two File transports (logs/error.log and
// logs/combined.log) and gave them no format. The logger-level format carries no json() and no
// printf(), so nothing rendered the entry and every line written to either file was the literal
// text undefined. Only production builds these transports, so no other cell can see this.
//
// The cell loads the REAL module under production through jest.isolateModules (it reads NODE_ENV
// once, at import), with the working directory moved to a fresh temp dir so the relative logs/
// paths land there, logs one error, and reads back what winston wrote.
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'fs';
import { EOL, tmpdir } from 'os';
import path from 'path';

type LoggerModule = typeof import('../utils/logger');

const FILES = ['error.log', 'combined.log'];
const PROBE_MESSAGE = 'Admin config request failed (POST /api/admin/ks1348-probe)';
const PROBE_ERROR = 'ks1348-private-detail';
const ORIGINAL_CWD = process.cwd();
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
const ORIGINAL_LOG_LEVEL = process.env.LOG_LEVEL;
const written: Record<string, string[]> = {};
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

async function readLines(file: string): Promise<string[]> {
  for (let i = 0; i < 100 && !(existsSync(file) && readFileSync(file, 'utf8').includes(EOL)); i++) {
    await new Promise((resolve) => setTimeout(resolve, 20));
  }
  return existsSync(file) ? readFileSync(file, 'utf8').split(EOL).filter((l) => l !== '') : [];
}

beforeAll(async () => {
  workDir = mkdtempSync(path.join(tmpdir(), 'ks1348-'));
  process.chdir(workDir);
  const { logger } = loadLogger('production');
  transportShape = logger.transports.map((t) => {
    const filename = (t as unknown as { filename?: string }).filename;
    return filename ? t.constructor.name + ':' + filename : t.constructor.name;
  });
  for (const t of logger.transports) {
    if (t.constructor.name === 'Console') t.silent = true;
  }
  logger.error(PROBE_MESSAGE, { error: PROBE_ERROR });
  for (const file of FILES) written[file] = await readLines(path.join(workDir, 'logs', file));
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

describe('KS-1348: originate production file logs are JSON lines, not the literal undefined', () => {
  it.each(FILES)('RED KS-1348 A1 logs/%s: the production line parses as JSON and carries the message, the error and the service', (file) => {
    expect({ file, entries: parseEach(written[file]) }).toEqual({
      file,
      entries: [expect.objectContaining({ level: 'error', message: PROBE_MESSAGE, error: PROBE_ERROR, service: 'originate' })],
    });
  });

  it.each(FILES)('control KS-1348 A0 logs/%s: exactly one line was written, so A1 reads a real write', (file) => {
    expect({ file, lines: written[file].length }).toEqual({ file, lines: 1 });
  });

  it('control KS-1348 A2: the module loaded its production shape, one Console and the two File transports', () => {
    expect(transportShape).toEqual(['Console', 'File:error.log', 'File:combined.log']);
  });
});
