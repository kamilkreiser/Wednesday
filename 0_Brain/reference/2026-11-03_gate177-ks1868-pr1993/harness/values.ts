// Gate 177 value classes (gate 175/176 set, V01-V17, plus two extra classes V18-V19 beyond the commission). Every value carries the sentinel SNTL177 somewhere readable (or in the thrower) so a log or
// response that prints it can be counted. Fresh value per call.
export const SENT = 'SNTL177';

const revoked = (): unknown => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};

export const VALUES: Array<[string, () => unknown]> = [
  ['V01 ordinary Error', () => new Error(`${SENT}-ord`)],
  [
    'V02 Error, message getter throws',
    () =>
      Object.create(Error.prototype, {
        message: {
          get() {
            throw new Error(`${SENT}-getter`);
          },
        },
      }),
  ],
  ['V03 revoked Proxy', () => revoked()],
  ['V04 null', () => null],
  ['V05 undefined', () => undefined],
  ['V06 string', () => `${SENT}-str`],
  ['V07 number', () => 177],
  ['V08 Object.create(null)', () => Object.create(null)],
  ['V09 {message: Symbol}', () => ({ message: Symbol(`${SENT}-sym`) })],
  ['V10 {message: BigInt}', () => ({ message: BigInt(177) })],
  ['V11 {message: revoked Proxy}', () => ({ message: revoked() })],
  [
    'V12 {message: obj whose toString throws}',
    () => ({
      message: {
        toString() {
          throw new Error(`${SENT}-ts`);
        },
      },
    }),
  ],
  [
    'V13 Proxy whose get trap throws',
    () =>
      new Proxy(
        {},
        {
          get() {
            throw new Error(`${SENT}-trap`);
          },
        },
      ),
  ],
  ['V14 thrown Symbol', () => Symbol(`${SENT}-thrownsym`)],
  [
    'V15 Error, name getter throws (message readable)',
    () => {
      const e = new Error(`${SENT}-namegetter`);
      Object.defineProperty(e, 'name', {
        get() {
          throw new Error('name boom');
        },
      });
      return e;
    },
  ],
  [
    'V16 {message readable, toString throws}',
    () => ({
      message: `${SENT}-msgok`,
      toString() {
        throw new Error('ts boom');
      },
    }),
  ],
  ['V17 plain {message}', () => ({ message: `${SENT}-plain` })],
  // EXTRA (not in the 17): an Error INSTANCE whose message is not a string; the read succeeds and the template literal
  // that uses it is outside the PR's guard (the gate 175/176 F2 shape).
  ['V18 Error instance, message is a Symbol', () => { const e = new Error('x'); Object.defineProperty(e, 'message', { value: Symbol(`${SENT}-e18`) }); return e; }],
  ['V19 Error instance, message obj whose toString throws', () => { const e = new Error('x'); Object.defineProperty(e, 'message', { value: { toString() { throw new Error(`${SENT}-e19`); } } }); return e; }],
];

/** Capture every console call and raw stdout/stderr write made during fn. */
export async function capture<T>(fn: () => Promise<T>): Promise<{ result: T; lines: string[] }> {
  const lines: string[] = [];
  const util = await import('node:util');
  const safe = (a: unknown): string => {
    try {
      return typeof a === 'string' ? a : util.inspect(a, { depth: 6 });
    } catch {
      return '<uninspectable>';
    }
  };
  const methods = ['log', 'warn', 'error', 'info', 'debug'] as const;
  const orig: Record<string, unknown> = {};
  for (const m of methods) {
    orig[m] = (console as any)[m];
    (console as any)[m] = (...args: unknown[]) => {
      lines.push(`console.${m}: ` + args.map(safe).join(' '));
    };
  }
  // winston's Console transport writes to console._stdout / console._stderr when present.
  const c = console as any;
  const os_ = c._stdout;
  const oe_ = c._stderr;
  c._stdout = { write: (chunk: unknown) => (lines.push('winston-stdout: ' + safe(String(chunk))), true) };
  c._stderr = { write: (chunk: unknown) => (lines.push('winston-stderr: ' + safe(String(chunk))), true) };
  const ow = process.stdout.write;
  const ew = process.stderr.write;
  (process.stdout as any).write = (chunk: unknown) => {
    lines.push('stdout: ' + safe(String(chunk)));
    return true;
  };
  (process.stderr as any).write = (chunk: unknown) => {
    lines.push('stderr: ' + safe(String(chunk)));
    return true;
  };
  try {
    const result = await fn();
    return { result, lines };
  } finally {
    for (const m of methods) (console as any)[m] = orig[m];
    c._stdout = os_;
    c._stderr = oe_;
    (process.stdout as any).write = ow;
    (process.stderr as any).write = ew;
  }
}

export function kind(thrown: unknown, original: unknown): string {
  if (thrown === original) return 'SAME value rethrown';
  if (thrown instanceof TypeError) return 'TypeError (new)';
  if (thrown instanceof Error) {
    let m = '';
    try {
      m = thrown.message;
    } catch {
      m = '?';
    }
    return `Error (new: ${m.replace(/SNTL177/g, 'S')})`;
  }
  return `other (${typeof thrown})`;
}

export const hits = (lines: string[]): number => lines.filter((l) => l.includes(SENT)).length;
