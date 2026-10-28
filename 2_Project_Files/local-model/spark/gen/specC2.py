PA='Blockchain/Dev/services/auth/src/middleware/errorHandler.ts'
PS='Blockchain/Dev/packages/shared/src/errors/index.ts'
TA='Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts'
TS='Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts'
OLD='    Object.setPrototypeOf(this, AppError.prototype);\n'
NEW='    Object.setPrototypeOf(this, new.target.prototype);\n'
TESTA='''// KS-1467 (services/auth middleware/errorHandler.ts): AppError's constructor ended with `Object.setPrototypeOf(this, AppError.prototype)`, which resets EVERY subclass instance to the base
// prototype. So `err instanceof ValidationError` (or any other subclass) was always false, and the errorHandler's own `err instanceof ValidationError && err.details` branch could never run:
// the password-strength `feedback` that registration, password reset and password change build never reached the client. The constructor now uses `new.target.prototype`.
// P1/P2 pin the prototype of each subclass (and the two-level chain), H1 pins the handler's `details` branch, C1 to C4 pin what must not change.
import { describe, it, expect, vi } from 'vitest';
import type { Request, Response, NextFunction } from 'express';

vi.mock('../utils/logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() },
  createLogger: vi.fn(),
  validateEnv: vi.fn(),
}));

const mod = await import('../middleware/errorHandler');
const { errorHandler, AppError } = mod;

const FACTORIES = [
  { name: 'BadRequestError', make: () => new mod.BadRequestError('x'), cls: mod.BadRequestError, status: 400 },
  { name: 'UnauthorizedError', make: () => new mod.UnauthorizedError('x'), cls: mod.UnauthorizedError, status: 401 },
  { name: 'ForbiddenError', make: () => new mod.ForbiddenError('x'), cls: mod.ForbiddenError, status: 403 },
  { name: 'NotFoundError', make: () => new mod.NotFoundError('Thing'), cls: mod.NotFoundError, status: 404 },
  { name: 'ConflictError', make: () => new mod.ConflictError('x'), cls: mod.ConflictError, status: 409 },
  { name: 'ValidationError', make: () => new mod.ValidationError('x', { a: 1 }), cls: mod.ValidationError, status: 422 },
  { name: 'TooManyRequestsError', make: () => new mod.TooManyRequestsError(), cls: mod.TooManyRequestsError, status: 429 },
  { name: 'ServiceUnavailableError', make: () => new mod.ServiceUnavailableError('x'), cls: mod.ServiceUnavailableError, status: 503 },
  { name: 'MfaRequiredError', make: () => new mod.MfaRequiredError(), cls: mod.MfaRequiredError, status: 403 },
] as const;

interface Captured {
  statusCode: number;
  body: { success: boolean; error: { code: string; message: string; details?: unknown } };
}

function run(err: Error): Captured {
  const captured = { statusCode: 0, body: undefined } as unknown as Captured;
  const res = {
    status(code: number) {
      captured.statusCode = code;
      return this;
    },
    json(payload: unknown) {
      captured.body = payload as Captured['body'];
      return this;
    },
  } as unknown as Response;
  const req = { path: '/api/auth/register', method: 'POST' } as unknown as Request;
  errorHandler(err, req, res, (() => undefined) as unknown as NextFunction);
  return captured;
}

describe('KS-1467: auth AppError subclasses keep their own prototype', () => {
  it.each(FACTORIES)('RED KS-1467 P1 $name: an instance is an instance of its own class', ({ make, cls }) => {
    expect(make() instanceof cls).toBe(true);
  });

  it.each(FACTORIES)('RED KS-1467 P2 $name: the prototype of an instance is the class prototype', ({ make, cls }) => {
    expect(Object.getPrototypeOf(make())).toBe(cls.prototype);
  });

  it('RED KS-1467 P3 a two-level subclass is an instance of both of its classes', () => {
    const e = new mod.InvalidCredentialsError();
    expect([e instanceof mod.InvalidCredentialsError, e instanceof mod.UnauthorizedError, e instanceof AppError]).toEqual([true, true, true]);
  });

  it('RED KS-1467 H1 the handler answers a ValidationError with its details', () => {
    const r = run(new mod.ValidationError('New password is too weak', { feedback: ['add a number'] }));
    expect(r.statusCode).toBe(422);
    expect(r.body.error).toEqual({ code: 'VALIDATION_ERROR', message: 'New password is too weak', details: { feedback: ['add a number'] } });
  });

  it.each(FACTORIES)('control KS-1467 C1 $name: an instance is still an AppError and an Error with its status', ({ make, status }) => {
    const e = make();
    expect([e instanceof AppError, e instanceof Error, e.statusCode]).toEqual([true, true, status]);
  });

  it('control KS-1467 C2 a plain AppError is still an AppError with its own prototype', () => {
    const e = new AppError('teapot', 418, 'TEAPOT');
    expect([e instanceof AppError, Object.getPrototypeOf(e) === AppError.prototype, e.code]).toEqual([true, true, 'TEAPOT']);
  });

  it('control KS-1467 C3 a ValidationError without details is answered without a details key', () => {
    const r = run(new mod.ValidationError('bad'));
    expect(r.statusCode).toBe(422);
    expect(r.body.error).toEqual({ code: 'VALIDATION_ERROR', message: 'bad' });
  });

  it('control KS-1467 C4 a BadRequestError is answered with code and message only', () => {
    const r = run(new mod.BadRequestError('nope'));
    expect(r.statusCode).toBe(400);
    expect(r.body.error).toEqual({ code: 'BAD_REQUEST', message: 'nope' });
  });
});
'''
TESTS='''// KS-1467 (packages/shared src/errors/index.ts, mounted by twelve services): AppError's constructor ended with `Object.setPrototypeOf(this, AppError.prototype)`, which resets EVERY subclass
// instance to the base prototype, so `err instanceof <subclass>` was always false. The constructor now uses `new.target.prototype`. P1/P2/P3 pin the prototypes (three levels deep for
// DocumentNotFoundError); C1/C2 pin what must not change: the status, the code, the details, and the handler's answer.
import { describe, it, expect } from 'vitest';
import type { Response } from 'express';
import {
  errorHandler,
  AppError,
  BadRequestError,
  UnauthorizedError,
  ForbiddenError,
  NotFoundError,
  ConflictError,
  ValidationError,
  RateLimitError,
  InternalError,
  ServiceUnavailableError,
  DocumentNotFoundError,
} from '../errors';

const FACTORIES = [
  { name: 'BadRequestError', make: () => new BadRequestError('x'), cls: BadRequestError, status: 400 },
  { name: 'UnauthorizedError', make: () => new UnauthorizedError('x'), cls: UnauthorizedError, status: 401 },
  { name: 'ForbiddenError', make: () => new ForbiddenError('x'), cls: ForbiddenError, status: 403 },
  { name: 'NotFoundError', make: () => new NotFoundError('Thing'), cls: NotFoundError, status: 404 },
  { name: 'ConflictError', make: () => new ConflictError('x'), cls: ConflictError, status: 409 },
  { name: 'ValidationError', make: () => new ValidationError('x', { a: 1 }), cls: ValidationError, status: 422 },
  { name: 'RateLimitError', make: () => new RateLimitError(5), cls: RateLimitError, status: 429 },
  { name: 'InternalError', make: () => new InternalError('x'), cls: InternalError, status: 500 },
  { name: 'ServiceUnavailableError', make: () => new ServiceUnavailableError('Billing'), cls: ServiceUnavailableError, status: 503 },
] as const;

function run(err: Error): { statusCode: number; body: { error: { code: string; message: string; details?: unknown } } } {
  const captured = { statusCode: 0, body: undefined } as unknown as { statusCode: number; body: { error: { code: string; message: string; details?: unknown } } };
  const res = {
    status(code: number) {
      captured.statusCode = code;
      return this;
    },
    json(payload: unknown) {
      captured.body = payload as typeof captured.body;
      return this;
    },
  } as unknown as Response;
  errorHandler(err, undefined, res, undefined);
  return captured;
}

describe('KS-1467: shared AppError subclasses keep their own prototype', () => {
  it.each(FACTORIES)('RED KS-1467 P1 $name: an instance is an instance of its own class', ({ make, cls }) => {
    expect(make() instanceof cls).toBe(true);
  });

  it.each(FACTORIES)('RED KS-1467 P2 $name: the prototype of an instance is the class prototype', ({ make, cls }) => {
    expect(Object.getPrototypeOf(make())).toBe(cls.prototype);
  });

  it('RED KS-1467 P3 a two-level subclass is an instance of every class in its chain', () => {
    const e = new DocumentNotFoundError('d-1');
    expect([e instanceof DocumentNotFoundError, e instanceof NotFoundError, e instanceof AppError]).toEqual([true, true, true]);
  });

  it.each(FACTORIES)('control KS-1467 C1 $name: an instance is still an AppError and an Error with its status', ({ make, status }) => {
    const e = make();
    expect([e instanceof AppError, e instanceof Error, e.statusCode]).toEqual([true, true, status]);
  });

  it('control KS-1467 C2 the handler still answers a ValidationError with its details and a 422', () => {
    const r = run(new ValidationError('bad', { field: 'name' }));
    expect(r.statusCode).toBe(422);
    expect(r.body.error).toEqual({ code: 'VALIDATION_ERROR', message: 'bad', details: { field: 'name' } });
  });
});
'''
S=dict(dir='ks_1467_p2_shared',ticket='KS-1467',
 title='(packages/shared half) AppError resets every subclass to the base prototype: `instanceof <subclass>` is always false; use new.target.prototype (RUNG 2, code_patch: one line in packages/shared + one NEW vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 2 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge. This is the packages/shared half of KS-1467; the services/auth half is `ks_1467_p1` (a two-package brief is refused by the tier: all files must be under one service). The shared `errorHandler` already formats `details` from any AppError, so only `instanceof` changes here. The Spark may fail this one (capability data).",
 products=[(PS,[('    Object.setPrototypeOf(this, AppError.prototype);\n    Error.captureStackTrace(this, this.constructor);\n','    Object.setPrototypeOf(this, new.target.prototype);\n    Error.captureStackTrace(this, this.constructor);\n')])],
 prodnote=['product, modified in place: ONE hunk, one line replaced'],
 tests=[dict(path=TS,content=TESTS)],
 testnote=['NEW file, vitest, given in full below'],
 runner='vitest` (`npx vitest run src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts` from `Blockchain/Dev/packages/shared',
 tier='code_patch', rung='2 (one line byte-exact; the new test given whole)',
 pins='''# code_patch, ONE line in packages/shared + a NEW vitest file; ref = the shared error-handler spec (shape only); line = the changed line.
tier=code_patch
ref=Blockchain/Dev/packages/shared/src/__tests__/error-handler.test.ts
line=44
ctx=65536
''',
 wrong="The shared `AppError` constructor (`packages/shared/src/errors/index.ts:44`), mounted by twelve services, ends with `Object.setPrototypeOf(this, AppError.prototype)`. That line runs in the BASE constructor for every subclass instance, so it resets the instance's prototype to the base class: `new ValidationError(...) instanceof ValidationError` is `false` for every subclass, and `new DocumentNotFoundError(..) instanceof NotFoundError` is `false`. The fix is the standard one: `Object.setPrototypeOf(this, new.target.prototype)`. The handler already reads `details` off any `AppError`, so no response changes here.",
 where="- `packages/shared/src/errors/index.ts:44` - **must change**: `    Object.setPrototypeOf(this, AppError.prototype);` becomes `    Object.setPrototypeOf(this, new.target.prototype);` (the next line, `Error.captureStackTrace(this, this.constructor);`, is context and stays).\n- Every other line is (correct) and is NOT touched.",
 exactnote="ONE hunk.\n",
 donot="**Do NOT touch** any subclass, `errorHandler`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Vitest imports are explicit. Pure ASCII.",
 red=['RED KS-1467 P1','RED KS-1467 P2','RED KS-1467 P3'],
 cells="- RED `P1`, `P2` (one row per subclass) and `P3` (a two-level chain, DocumentNotFoundError): at the tip every subclass instance has the base prototype; after the edit they hold. Red by assertion.\n- CONTROL `C1` (still an AppError, an Error, status kept) and `C2` (the handler still answers a ValidationError with its details and a 422): green at the tip AND after.",
 premises="- `Object.setPrototypeOf(this, AppError.prototype);` occurs once in the file, followed by `Error.captureStackTrace(this, this.constructor);` (`git show 8894c7486f82:<path>`).\n- The shared `errorHandler` formats details from any `AppError` already (`formatErrorResponse`).",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control (which also runs the package suite: A6).\n- Whether other services mounting `@secuura/shared` have tests that assume the old prototype: the round runs only this package's suite.\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the packages/shared half of KS-1467.** Link the PR as Refs KS-1467.",
)
