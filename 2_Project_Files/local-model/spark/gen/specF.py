P='Blockchain/Dev/services/api-gateway/src/services/enforcement.ts'
TP='Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts'
OLD1="  const userIdx = VERIFICATION_LEVEL_ORDER.indexOf((userLevel || 'none').toLowerCase());\n"
NEW1="""  // KS-1197: a level that is not a string (a number, an array, an object off a token claim) made `.toLowerCase()` throw. It now ranks as 'none', the same as any unrecognised level (KS-1176).
  const userIdx = VERIFICATION_LEVEL_ORDER.indexOf((typeof userLevel === 'string' && userLevel ? userLevel : 'none').toLowerCase());
"""
OLD2="  const userLevel = user.verificationLevel || 'none';\n"
NEW2="  const userLevel = typeof user.verificationLevel === 'string' && user.verificationLevel ? user.verificationLevel : 'none';\n"
TEST='''/**
 * KS-1197 (api-gateway services/enforcement.ts): a verificationLevel that is not a string made POST /api/documents answer 500. `meetsVerificationLevel` read
 * `(userLevel || 'none').toLowerCase()`, and `enforceDocumentTypeRules` read `user.verificationLevel || 'none'` and later `userLevel.toUpperCase()` in its 403 text; a
 * truthy non-string (a number, an array, an object) passed the `||` and threw a TypeError. A level that is not a string now ranks as 'none', the lowest authenticated level,
 * exactly as an unrecognised level already does (KS-1176): it meets a 'none' requirement and nothing above it. Every cell reads a thrown error as the string THREW, so a red is an
 * assertion. K1-K5 are red at the tip; C1-C4 pin the known levels and the connector-key level, which must not change.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { enforceDocumentTypeRules, meetsVerificationLevel } from '../services/enforcement';
import type { UserPayload } from '../services/enforcement';

vi.mock('../services/redis', () => ({
  getAllDocumentTypes: vi.fn(),
  getWorkflow: vi.fn(),
  setWorkflowInstance: vi.fn(),
  setPendingDocument: vi.fn(),
}));

import * as redisService from '../services/redis';

type Outcome = string | [boolean, number | undefined, string | undefined];

async function enforce(level: unknown, required: string): Promise<Outcome> {
  vi.mocked(redisService.getAllDocumentTypes).mockResolvedValue([
    { id: 'dt-1', code: 'DEGREE', isActive: true, creatorVerificationLevel: required },
  ]);
  const user = { userId: 'u-1', email: 'u@example.test', role: 'OWNER', verificationLevel: level } as unknown as UserPayload;
  try {
    const result = await enforceDocumentTypeRules({ documentType: 'DEGREE' }, user);
    return [result.ok, (result as { status?: number }).status, (result as { code?: string }).code];
  } catch (err) {
    return 'THREW ' + (err instanceof Error ? err.message : String(err));
  }
}

function meets(level: unknown, required: string): boolean | string {
  try {
    return meetsVerificationLevel(level as string, required);
  } catch (err) {
    return 'THREW ' + (err instanceof Error ? err.message : String(err));
  }
}

const REFUSED: Outcome = [false, 403, 'INSUFFICIENT_VERIFICATION_LEVEL'];
const ADMITTED: Outcome = [true, undefined, undefined];

describe('KS-1197: a non-string verification level ranks as none', () => {
  beforeEach(() => vi.clearAllMocks());

  it.each([
    ['number', 7],
    ['array', ['high']],
    ['object', {}],
  ])('RED KS-1197 K1 a %s level meets nothing above none: a standard type refuses it with 403', async (_kind, level) => {
    expect(await enforce(level, 'standard')).toEqual(REFUSED);
  });

  it('RED KS-1197 K2 the 403 text names the level as NONE', async () => {
    vi.mocked(redisService.getAllDocumentTypes).mockResolvedValue([{ id: 'dt-1', code: 'DEGREE', isActive: true, creatorVerificationLevel: 'standard' }]);
    const user = { userId: 'u-1', email: 'u@example.test', role: 'OWNER', verificationLevel: 7 } as unknown as UserPayload;
    let message = 'THREW';
    try {
      message = (await enforceDocumentTypeRules({ documentType: 'DEGREE' }, user) as { error?: string }).error ?? 'no error text';
    } catch {
      message = 'THREW';
    }
    expect(message).toBe('This document type requires STANDARD verification. Your current level is NONE.');
  });

  it.each([
    ['number', 7],
    ['array', ['high']],
    ['object', {}],
  ])('RED KS-1197 K3 a %s level still meets a none requirement: a none type admits it', async (_kind, level) => {
    expect(await enforce(level, 'none')).toEqual(ADMITTED);
  });

  it('RED KS-1197 K4 meetsVerificationLevel of a number is true against none and false against basic', () => {
    expect([meets(7, 'none'), meets(7, 'basic')]).toEqual([true, false]);
  });

  it('RED KS-1197 K5 meetsVerificationLevel of an array or an object is true against none and false against basic', () => {
    expect([meets(['high'], 'none'), meets(['high'], 'basic'), meets({}, 'none'), meets({}, 'basic')]).toEqual([true, false, true, false]);
  });

  it('control KS-1197 C1 a level that meets the requirement is admitted, case-insensitively', async () => {
    expect([await enforce('standard', 'standard'), await enforce('HIGH', 'standard')]).toEqual([ADMITTED, ADMITTED]);
  });

  it('control KS-1197 C2 a known level below the requirement is still refused with 403', async () => {
    expect(await enforce('basic', 'standard')).toEqual(REFUSED);
  });

  it('control KS-1197 C3 the connector-key level api_key still ranks as none: admitted on a none type, refused on a basic one', async () => {
    expect([await enforce('api_key', 'none'), await enforce('api_key', 'basic')]).toEqual([ADMITTED, REFUSED]);
  });

  it('control KS-1197 C4 an absent or empty level still ranks as none', async () => {
    expect([await enforce(undefined, 'none'), await enforce('', 'none'), await enforce('', 'basic')]).toEqual([ADMITTED, ADMITTED, REFUSED]);
  });
});
'''
S=dict(dir='ks_1197_p1',ticket='KS-1197',
 title='A non-string verificationLevel claim: POST /api/documents answers 500 (the TypeError in meetsVerificationLevel and the 403 text); rank a non-string level as none in services/enforcement.ts (RUNG 2, code_patch: ONE product file, two hunks, + one NEW vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 2 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. This brief takes ONLY the `POST /api/documents` half of KS-1197 (the 500 from `enforceDocumentTypeRules`); the ticket's other half, the verifier-gated verify handler at `routes/verification.ts:556-557` that never answers, is in open PR #1756's file set and is NOT part of this brief. The ticket's recommendation ('coerce or validate the claim once where the principal is built, `middleware/auth.ts`') is not followed: the change is at the consumer so the file is in no open PR; ranking a non-string level as 'none' is the same direction KS-1176 took for an unrecognised level (it only ever REMOVES access relative to a crash, never adds). The raise seat must confirm that shape with the ticket's owner. The Spark may fail this one (capability data).",
 products=[(P,[(OLD1,NEW1),(OLD2,NEW2)])],
 prodnote=['product, modified in place: TWO hunks - one line replaced by two in meetsVerificationLevel, one line replaced in enforceDocumentTypeRules'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 9 cells (16 with their rows)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts` from `Blockchain/Dev/services/api-gateway',
 tier='code_patch', rung='2 (two hunks given byte-exact; the new test given whole)',
 pins='''# code_patch, ONE product file with 2 hunks + a NEW vitest file (test_file NOT pinned: it would mean MODIFY); ref = the ks501 enforcement spec (mock shape only); line = the first changed line at the tip.
tier=code_patch
ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts
line=55
ctx=65536
''',
 wrong="`enforceDocumentTypeRules` (`services/enforcement.ts`) reads `const userLevel = user.verificationLevel || 'none';` (`:152`) and calls `meetsVerificationLevel(userLevel, requiredLevel)`, which reads `(userLevel || 'none').toLowerCase()` (`:55`). If the token's `verificationLevel` claim is a truthy NON-string (a number, an array, an object), the `||` keeps it and `.toLowerCase()` throws a TypeError; the 403 text also calls `userLevel.toUpperCase()`. The KS-529 wrapper turns the throw into a 500 on `POST /api/documents`. The change makes both reads treat a non-string (or empty) level as `'none'`: `meetsVerificationLevel` reads `typeof userLevel === 'string' && userLevel ? userLevel : 'none'` and the caller computes `userLevel` the same way, so the 403 text names the level `NONE`. A string level behaves exactly as before.",
 where="- `services/enforcement.ts:55` - **must change**: `  const userIdx = VERIFICATION_LEVEL_ORDER.indexOf((userLevel || 'none').toLowerCase());` becomes the two lines under \"The exact change\" (a one-line comment and the new `userIdx` line). The `reqIdx` line below it is NOT touched.\n- `services/enforcement.ts:152` - **must change**: `  const userLevel = user.verificationLevel || 'none';` becomes `  const userLevel = typeof user.verificationLevel === 'string' && user.verificationLevel ? user.verificationLevel : 'none';`.\n- Every other line, including the KS-1176 comment block inside `meetsVerificationLevel`, is (correct) and is NOT touched.",
 exactnote="Two hunks in one file. `UserPayload.verificationLevel` is typed `string`, so the `typeof` test type-checks (it narrows nothing and costs nothing).\n",
 donot="**Do NOT touch** `routes/verification.ts` (open PR #1756), `middleware/auth.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Vitest imports are explicit; the redis service is mocked as in `ks501`. Every thrown error is reported as the string `THREW ...`, so a red is an assertion. Pure ASCII.",
 red=['RED KS-1197 K1','RED KS-1197 K2','RED KS-1197 K3','RED KS-1197 K4','RED KS-1197 K5'],
 cells="- RED `K1` (3 rows: number, array, object) a standard type refuses the level with 403 `INSUFFICIENT_VERIFICATION_LEVEL`; RED `K2` the 403 text ends `Your current level is NONE.`; RED `K3` (3 rows) a none type admits it; RED `K4`, `K5` the unit function: at the tip each reads `THREW Cannot read ...` or `toLowerCase is not a function`; after, `[true, false]`.\n- CONTROL `C1`-`C4` (known levels, case-insensitivity, the connector-key level `api_key`, absent/empty levels): green at the tip AND after.",
 premises="- `services/enforcement.ts:55` is the `userIdx` line, `:152` is `const userLevel = user.verificationLevel || 'none';`, `:153` the `meetsVerificationLevel(userLevel, requiredLevel)` call; read with `git show 8894c7486f82:Blockchain/Dev/services/api-gateway/src/services/enforcement.ts`.\n- `ks501-enforcement-non-string-doctype.test.ts` mocks `../services/redis` with exactly the four functions this test mocks and drives `enforceDocumentTypeRules` directly; a catalogue entry `{ id, code, isActive, creatorVerificationLevel }` is what `resolveDocumentType` returns by code.\n- The package test runner is vitest; the golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The ticket's other half (`routes/verification.ts:556-557`, an async throw that never answers) is not addressed and is not reachable from this file; it is in #1756's file set.\n- Whether a non-string level can arrive at all in production (the ticket comment of 2026-10-12 reports that an ISSUER_ADMIN can mint an account whose token carries `verificationLevel: {}`).\n- Open PRs touching either file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the POST /api/documents half of KS-1197 only.** Link the PR as Refs KS-1197, never a close-word.",
)
