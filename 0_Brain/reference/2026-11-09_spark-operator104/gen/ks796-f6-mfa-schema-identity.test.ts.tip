/**
 * KS-796 F-6 (QA PASS 1 on #819) — the "agreement test below" the previous
 * commit message claimed exists.
 *
 * Q3's substance was right: all four mfaCode sites do use one definition, and no
 * restatement of the union/optional/transform survives. What did not exist was
 * the GUARD. The QA pass measured it: restating the union INLINE in wallet.ts,
 * with the exact text the parent carried, left the auth suite 411/411 green
 * across 4 of 4 tampered runs. Only a BEHAVIOURAL drift was catchable, and only
 * by two rows a previous round happened to add — so a restatement that drifts in
 * some other direction (a widened regex, a different `.optional()` placement)
 * was undetected.
 *
 * Two legs, because they fail on different things:
 *   IDENTITY   — the three runtime sites must be the SAME OBJECT. This reds on
 *                any restatement, including a character-identical one, which is
 *                exactly the tamper that stayed green.
 *   AGREEMENT  — the wire contract (`MFA_CODE_ACCEPTED.optional()`, what
 *                auth.openapi.ts publishes) and the runtime schema must accept
 *                and reject the same inputs. That site cannot be asserted by
 *                identity: `.optional()` builds a new object per call, so
 *                identity there would assert a fact about zod, not about us.
 */

import { describe, it, expect, beforeAll } from 'vitest';
import { mfaCodeRuntimeSchema, MFA_CODE_ACCEPTED, MFA_CODE_PATTERN } from '../services/passwordLoginGate';
import { loginSchema } from '../routes/auth';
import { authorizeCredentialsSchema } from '../routes/oauth';
import { verifySignatureSchema } from '../routes/wallet';
import { ADMIN_WRITABLE_STATUSES, DB_USER_STATUSES } from '../types';
import { readFileSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';

/**
 * `verifySignatureSchema` is `.refine()`d, which wraps it in a ZodEffects — and a
 * ZodEffects has no `.shape`. Reading `.shape.mfaCode` on it THREW, which is how
 * this unwrapper came to exist; had the assertion been written with `?.` it would
 * have compared `undefined` to the schema and reported a drift that is not there.
 * `innerType()` is zod's own accessor for the wrapped schema, so this stays out of
 * `_def`.
 */
function shapeOf(schema: unknown): Record<string, unknown> {
  const s = schema as { innerType?: () => unknown; shape?: Record<string, unknown> };
  const unwrapped = typeof s.innerType === 'function' ? (s.innerType() as typeof s) : s;
  const shape = unwrapped.shape;
  if (!shape) throw new Error('shapeOf: no .shape after unwrapping — the schema kind changed');
  return shape;
}

const RUNTIME_SITES: Array<[string, unknown]> = [
  ['POST /api/auth/login (loginSchema)', loginSchema],
  ['POST /api/oauth/authorize (authorizeCredentialsSchema)', authorizeCredentialsSchema],
  ['POST /api/auth/wallet/verify (verifySignatureSchema)', verifySignatureSchema],
];

describe('KS-796 F-6 — the four mfaCode sites share ONE definition', () => {
  it.each(RUNTIME_SITES)('%s uses the shared runtime schema object itself', (_name, schema) => {
    expect(shapeOf(schema).mfaCode).toBe(mfaCodeRuntimeSchema);
  });

  it('CONTROL — the assertion can fail: a restatement is NOT the shared object', () => {
    // Without this, the leg above would pass just as well against an assertion
    // that compares a thing to itself. This is the exact text the parent carried
    // in wallet.ts, and the QA pass proved the suite stayed green with it.
    const restated = MFA_CODE_ACCEPTED.optional().transform((v) => (v ? v : undefined));
    expect(restated).not.toBe(mfaCodeRuntimeSchema);
  });

  // The published wire contract vs the runtime schema. auth.openapi.ts spells the
  // field `MFA_CODE_ACCEPTED.optional()` — no transform, because a transform
  // describes runtime coercion and not the wire shape — so the two are related by
  // AGREEMENT on what they accept, not by identity.
  const CORPUS: Array<[string, unknown]> = [
    ['a 6-digit TOTP', '123456'],
    ['an 8-char backup code', 'ABCD2345'],
    ['a lowercase backup code', 'abcd2345'],
    ['the empty string (a form-backed client)', ''],
    ['absent', undefined],
    ['too short', 'abc'],
    ['7 digits', '1234567'],
    ['9 alphanumerics', 'ABCD23456'],
    ['an astral char (KS-283)', '12345\u{1F600}'],
    ['a non-string', 42],
  ];

  it.each(CORPUS)('the published shape and the runtime shape agree on %s', (_label, value) => {
    const wire = MFA_CODE_ACCEPTED.optional().safeParse(value);
    const runtime = mfaCodeRuntimeSchema.safeParse(value);
    expect(runtime.success, `runtime accepted=${runtime.success}, published accepted=${wire.success}`).toBe(wire.success);
  });

  it('CONTROL — the corpus discriminates: it contains BOTH accepted and rejected inputs', () => {
    // A corpus that is all-accepted (or all-rejected) makes the agreement leg
    // above pass against two schemas that agree on nothing else.
    const results = CORPUS.map(([, v]) => mfaCodeRuntimeSchema.safeParse(v).success);
    expect(results.filter(Boolean).length).toBeGreaterThan(0);
    expect(results.filter((r) => !r).length).toBeGreaterThan(0);
  });

  it('the empty string normalises to ABSENT at runtime, and stays expressible on the wire', () => {
    expect(mfaCodeRuntimeSchema.parse('')).toBeUndefined();
    expect(MFA_CODE_ACCEPTED.optional().safeParse('').success).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// KS-796 QA2-F4 — the same agreement, asserted at the PUBLISHED contract.
//
// ⚠ WHY THIS READS THE GENERATED YAML AND NOT THE SCHEMA OBJECTS. The obvious
// version imports `LoginRequestSchema` etc. from `auth.openapi.ts` and compares
// them to the runtime schema. It cannot load:
//
//   TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function
//     at src/auth.openapi.ts:152
//
// `packages/shared/src/openapi/registry.ts:245` states the rule — consumers MUST
// import `z` from '@secuura/shared', so `extendZodWithOpenApi` lands on the same
// prototype — and `services/passwordLoginGate.ts:55` imports `z` from 'zod'
// directly, so `MFA_CODE_ACCEPTED` is built on an UNEXTENDED zod. The spec
// generator's single CJS resolution happens to unify them; a vitest run does not.
// That is a one-line change with a blast radius well past this PR, so it is FILED
// rather than slipped in here — and it is the real reason `auth.openapi.ts` sits
// in no test's import graph (the gate's canary: a module-scope throw there left
// the suite 441/441 green).
//
// Reading the generated yaml is not a consolation prize: it is the artefact a
// client actually generates from, and it is what would ship wrong.
// ---------------------------------------------------------------------------

function devRoot(start: string): string {
  let dir = start;
  for (let i = 0; i < 10; i++) {
    if (existsSync(join(dir, 'services')) && existsSync(join(dir, 'packages'))) return dir;
    dir = resolve(dir, '..');
  }
  throw new Error('devRoot: could not locate Blockchain/Dev');
}

/**
 * Pull ONE named schema's own block out of the generated spec.
 *
 * ⚠ This is a text instrument, deliberately, and it is NOT `spec.includes(...)`.
 * The existing KS-622 lockstep guard uses `includes` over the whole 1.3 MB file,
 * and `auth.openapi.ts:76` already records why that is weak: it is
 * OCCURRENCE-BLIND, so one correct occurrence satisfies it while another drifts —
 * which is precisely the per-site drift this leg exists to catch. Isolating the
 * block first is what makes the assertions per-site.
 *
 * A real YAML parse would be better still, but `yaml` is not in this service's
 * package.json OR its lockfile (checked both). `tsc` passes locally only because
 * the workspace root hoists it, and this service's Docker build runs `npm ci` in
 * its own directory and compiles `__tests__` — so importing it here would break
 * the image while every local check stayed green. Adding the dep means touching
 * the service lockfile, which is not this PR's scope.
 *
 * The generated file is machine-indented, so block boundaries are reliable: a
 * schema starts at exactly 4 spaces and ends at the next line indented <= 4.
 */
function schemaBlock(spec: string, name: string): string | null {
  const lines = spec.split('\n');
  const start = lines.findIndex((l) => l === `    ${name}:`);
  if (start === -1) return null;
  const out: string[] = [];
  for (let i = start + 1; i < lines.length; i++) {
    const l = lines[i];
    if (l.trim() !== '' && !/^\s{5,}/.test(l)) break;
    out.push(l);
  }
  return out.join('\n');
}

/** The mfaCode property's own sub-block, with descriptions stripped. */
function mfaCodeShape(block: string): string {
  const lines = block.split('\n');
  const start = lines.findIndex((l) => /^\s{8}mfaCode:\s*$/.test(l));
  if (start === -1) return '';
  const indent = lines[start].search(/\S/);
  const out: string[] = [];
  for (let i = start + 1; i < lines.length; i++) {
    const l = lines[i];
    if (l.trim() !== '' && l.search(/\S/) <= indent) break;
    out.push(l);
  }
  // description differs per site BY DESIGN; the shape must not.
  return out.join('\n').replace(/^\s*description:[\s\S]*$/m, '').trimEnd();
}

describe('KS-796 QA2-F4 — every PUBLISHED site carries the same mfaCode contract', () => {
  const SITES = ['LoginRequest', 'WalletVerifyRequest', 'OAuthAuthorizeRequest'] as const;
  let spec: string;
  const blocks: Record<string, string> = {};

  beforeAll(() => {
    const specPath = join(devRoot(__dirname), 'docs', 'openapi', 'secuura-api.yaml');
    // A missing spec must FAIL, never skip — a skipped leg reads as a pass.
    expect(existsSync(specPath), `generated spec not found at ${specPath}`).toBe(true);
    spec = readFileSync(specPath, 'utf8');
    for (const n of SITES) blocks[n] = schemaBlock(spec, n) ?? '';
  });

  it('CONTROL — the extractor ISOLATES, which is the whole difference from spec.includes()', () => {
    for (const n of SITES) expect(blocks[n], `${n} not found in components.schemas`).not.toBe('');
    // Each block must NOT contain a sibling's distinctive field, or "per site"
    // is a claim about a boundary that is not really there.
    expect(blocks.LoginRequest).not.toContain('client_id');       // OAuthAuthorizeRequest's
    expect(blocks.OAuthAuthorizeRequest).toContain('client_id');  // and it IS somewhere
    expect(blocks.LoginRequest).not.toContain('signature');       // WalletVerifyRequest's
    expect(blocks.WalletVerifyRequest).toContain('signature');
  });

  it.each(SITES)('%s publishes an mfaCode field', (name) => {
    expect(blocks[name]).toContain('mfaCode:');
  });

  it.each(SITES)('%s publishes the SHARED union — the runtime pattern and the empty-string branch', (name) => {
    const shape = mfaCodeShape(blocks[name]);
    expect(shape, `${name} must publish the shared pattern`).toContain(MFA_CODE_PATTERN.source);
    expect(shape, `${name} must publish the empty-string branch`).toMatch(/enum:\s*\n\s*- ""/);
  });

  it('the three sites are IDENTICAL in shape — the whole point of one definition', () => {
    const [a, b, c] = SITES.map((n) => mfaCodeShape(blocks[n]));
    expect(a).not.toBe('');
    expect(b).toBe(a);
    expect(c).toBe(a);
  });
});

// ---------------------------------------------------------------------------
// KS-796 QA2-F5 — the writable subset must be a SUBSET.
//
// `ADMIN_WRITABLE_STATUSES` is a hand-declared list (deliberately: F-3 proved
// deriving it from the vocabulary is what opened the takeover). A hand-declared
// list can drift the other way — a typo, or a value the column's CHECK will
// refuse — and the endpoint would then advertise a status that cannot be stored.
// Its sibling allow-list already has this guard; this one did not.
// ---------------------------------------------------------------------------

describe('KS-796 QA2-F5 — ADMIN_WRITABLE_STATUSES is a subset of the column vocabulary', () => {
  it.each(ADMIN_WRITABLE_STATUSES as readonly string[])('%s is a value the column may hold', (s) => {
    expect(DB_USER_STATUSES as readonly string[]).toContain(s);
  });

  it('and it is a PROPER subset — `invited` is deliberately excluded', () => {
    // Without this the leg above passes just as well for a writable set that IS
    // the vocabulary, which is exactly the defect F-3 was.
    expect(ADMIN_WRITABLE_STATUSES).not.toContain('invited');
    expect(DB_USER_STATUSES).toContain('invited');
    expect(ADMIN_WRITABLE_STATUSES.length).toBeLessThan(DB_USER_STATUSES.length);
  });
});
