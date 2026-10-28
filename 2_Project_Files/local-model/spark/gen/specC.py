PA='Blockchain/Dev/services/auth/src/middleware/errorHandler.ts'
PS='Blockchain/Dev/packages/shared/src/errors/index.ts'
TA='Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts'
TS='Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts'
PG='Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts'
OLD='    Object.setPrototypeOf(this, AppError.prototype);\n'
NEW='    Object.setPrototypeOf(this, new.target.prototype);\n'
TESTA='''// KS-1467 (services/auth middleware/errorHandler.ts): AppError's constructor ended with `Object.setPrototypeOf(this, AppError.prototype)`, which resets EVERY subclass instance to the base
// prototype. So `err instanceof ValidationError` (or any other subclass) was always false, and the errorHandler's own `err instanceof ValidationError && err.details` branch could never run:
// the password-strength `feedback` that registration, password reset and password change build never reached the client. The constructor now uses `new.target.prototype`.
// P1/P2 pin the prototype of each subclass (and the two-level chain), H1 pins the handler's `details` branch, S1 pins that the stale comment in passwordLoginGate.ts is reworded, C1 to C4 and S2 pin what must not change.
import { describe, it, expect, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import type { Request, Response, NextFunction } from 'express';
import * as mod from '../middleware/errorHandler';

vi.mock('../utils/logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() },
  createLogger: vi.fn(),
  validateEnv: vi.fn(),
}));

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

  it('RED KS-1467 S1 the comment above the 503 statusCode check no longer claims instanceof is always false', () => {
    const source = readFileSync(join(process.cwd(), 'src', 'services', 'passwordLoginGate.ts'), 'utf8');
    expect(source).not.toContain('is always false here');
  });

  it('control KS-1467 S2 passwordLoginGate.ts still reaches the 503 by statusCode and still throws the unconfirmed message', () => {
    const source = readFileSync(join(process.cwd(), 'src', 'services', 'passwordLoginGate.ts'), 'utf8');
    expect(source).toContain('?.statusCode === 503) throw new ServiceUnavailableError(BACKUP_CODE_UNCONFIRMED_MESSAGE);');
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
GATE_CONST="/** KS-1188 F3: the 503 text when a backup-code burn could not be confirmed. True whether or not the burn landed. */\nconst BACKUP_CODE_UNCONFIRMED_MESSAGE =\n  'Sign-in could not be confirmed. If you signed in with a backup code, your backup code may already have been spent: ' +\n  'try again with another backup code or an authenticator app code.';\n"
GATE_OLD1="\n"+GATE_CONST
GATE_NEW1=""
GATE_IMP="import { STATUSES_MAY_RECEIVE_CREDENTIAL } from '../types';\n"
GATE_NEW1B=GATE_IMP+"\n"+GATE_CONST
GATE_OLD2="          // `statusCode`, not `instanceof`: AppError's constructor ends with Object.setPrototypeOf(this, AppError.prototype), which\n          // resets every subclass instance to the base prototype, so `err instanceof ServiceUnavailableError` is always false here.\n"
GATE_NEW2="          // `statusCode`, not `instanceof`: this reads the same for an AppError from any package. (KS-1467: AppError's constructor used to end with\n          // Object.setPrototypeOf(this, AppError.prototype), which reset every subclass instance, so `instanceof ServiceUnavailableError` was always false here.)\n"
S=dict(dir='ks_1467_p1',ticket='KS-1467',
 title='(services/auth half) AppError resets every subclass to the base prototype, so the handler never sends ValidationError details; use new.target.prototype, and reword the comment in passwordLoginGate.ts that the fix makes untrue (RUNG 3, code_patch2: TWO product files in services/auth, 2 hunks, + one NEW vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 2 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. The ticket's Recommendation is followed for services/auth (`Object.setPrototypeOf(this, new.target.prototype)`, a cell per subclass); the packages/shared half is `ks_1467_p2_shared` (a two-package brief is refused by the tier). Also folded in: the stale comment in `passwordLoginGate.ts` that the fix makes untrue (the ticket's gate note 1, moving a const below the imports, is NOT part of this brief: its diff would be a move, which the builder refuses). The ticket's clause 'decide deliberately that 422 responses now carry `details`' is NOT decided here: the handler's existing `details` branch simply starts to run, which cell H1 pins; the raise seat must put that visible change to the owner before merge. The Spark may fail this one (capability data).",
 products=[(PA,[(OLD,NEW)]),(PG,[(GATE_OLD2,GATE_NEW2)])],
 prodnote=['product 1 of 2, modified in place: ONE hunk, one line replaced','product 2 of 2, modified in place: ONE hunk - the comment above the statusCode check reworded'],
 tests=[dict(path=TA,content=TESTA)],
 testnote=['NEW file, vitest, given in full below'],
 runner='vitest` (`npx vitest run src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch2', rung='3 (two product files in one service, two hunks, and a new test with a source-text cell; every `+` line given byte-exact)',
 pins='''# code_patch2: 2 products in services/auth (errorHandler.ts one line; passwordLoginGate.ts two hunks) + 1 NEW vitest file; ref = the auth ks727 handler spec (shape only); line = the changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/auth/src/__tests__/ks727-internal-error-message-leak.test.ts
line=25
ctx=65536
''',
 wrong="The auth `AppError` constructor (`services/auth/src/middleware/errorHandler.ts:25`) ends with `Object.setPrototypeOf(this, AppError.prototype)`. That line runs in the BASE constructor for every subclass instance, so it resets the instance's prototype to the base class: `new ValidationError(...) instanceof ValidationError` is `false` for every subclass. This kills the handler's own branch `if (err instanceof ValidationError && err.details)` (`errorHandler.ts:296`), so the password-strength `feedback` that register, reset-password and change-password pass as `details` is never sent. The fix is the standard one: `Object.setPrototypeOf(this, new.target.prototype)`; the 422 response then carries `details` when the error has them. One comment rides along in `services/passwordLoginGate.ts`: the comment above the `statusCode === 503` check says `instanceof` is always false, which the fix makes untrue; it is reworded (the code stays on `statusCode`).",
 where="- `services/auth/src/middleware/errorHandler.ts:25` - **must change**: `    Object.setPrototypeOf(this, AppError.prototype);` becomes `    Object.setPrototypeOf(this, new.target.prototype);`.\n- `services/auth/src/services/passwordLoginGate.ts:286-287` - **must change**: the two comment lines above `if ((err as { statusCode?: unknown } | null)?.statusCode === 503) ...` are replaced by the two lines under \"The exact change\". The code line below them is NOT touched.\n- Every other line of both files is (correct) and is NOT touched.",
 exactnote="Two hunks in two files, in the order of `## The mode`.\n",
 donot="**Do NOT touch** any subclass, `errorHandler`, anything else in `passwordLoginGate.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Vitest imports are explicit. Pure ASCII. The two source-text cells read `src/services/passwordLoginGate.ts` relative to the service directory the test runs from.",
 red=['RED KS-1467 P1','RED KS-1467 P2','RED KS-1467 P3','RED KS-1467 H1','RED KS-1467 S1'],
 cells="- RED `P1`, `P2` (one row per subclass) and `P3` (a two-level chain): at the tip every subclass instance has the base prototype, so `instanceof <subclass>` is false and `getPrototypeOf` is `AppError.prototype`; after the edit they hold. Red by assertion.\n- RED `H1`: at the tip `details` is dropped from the 422 body; after, it is sent. RED `S1`: at the tip `passwordLoginGate.ts` still says `is always false here`; after, it does not.\n- CONTROL `C1`-`C4` and `S2`: green at the tip AND after (still an AppError and an Error with its status; a plain AppError keeps its own prototype; a ValidationError without details has no `details` key; a BadRequestError body is code and message only; the 503-by-statusCode line is unchanged).",
 premises="- `Object.setPrototypeOf(this, AppError.prototype);` occurs once in `errorHandler.ts`; `instanceof <Subclass>` appears nowhere else under `services/` or `packages/` outside tests (a grep at the tip: only `errorHandler.ts:296` and a comment in `passwordLoginGate.ts`), so the change makes exactly one dead branch live.\n- In `passwordLoginGate.ts` at the tip the stale comment is `:287-288`.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control (which also runs the whole services/auth suite: A6).\n- Whether any client depends on `details` being absent from a 422 (ticket: not established). The raise seat must put the visible response change to the owner.\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28. Gate notes 1 (a const placed mid-import) and 2 (a burn-once assertion in the ks1188 test) of the ticket are NOT part of this brief.",
 scope="**Closes the services/auth half of KS-1467.** Link the PR as Refs KS-1467 unless the owner confirms the visible 422 change.",
)
