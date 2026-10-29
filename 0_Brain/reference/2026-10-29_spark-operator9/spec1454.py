# KS-1454 p1 (Spark operator 9, 2026-10-29): anchorSchema.ts accepts + anchors metadata.signatureHash on the sign verb. code_patch, mk2.py.
P='Blockchain/Dev/services/anchoring/src/anchorSchema.ts'
TP='Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts'
E1=("    ).optional(),\n  }).optional(),\n  // KS-1175: the top-level identity block",
    "    ).optional(),\n"
    "    // KS-1454 (Stuart 2026-10-09, amended 10 Oct): the plain SHA-256 of the detached .p7s, lowercase hex, sign verb only (the refinement below refuses it on any other verb).\n"
    "    signatureHash: z.string().regex(/^[a-f0-9]{64}$/, 'Invalid signatureHash format - expect 64 lowercase hex (the SHA-256 of the detached .p7s)').optional(),\n"
    "  }).optional(),\n  // KS-1175: the top-level identity block")
E2=("      message: 'identity.identityCommitment and metadata.identityCommitment differ — send one value, or the same value in both',\n    });\n  }\n});\n",
    "      message: 'identity.identityCommitment and metadata.identityCommitment differ — send one value, or the same value in both',\n    });\n  }\n"
    "  // KS-1454: a signature hash on any verb but `sign` (or with no verb) is a caller error (400); a stray hash must not be anchored as if it named a signature.\n"
    "  if (data.metadata?.signatureHash !== undefined && data.metadata.documentType !== 'sign') {\n"
    "    ctx.addIssue({\n"
    "      code: z.ZodIssueCode.custom,\n"
    "      path: ['metadata', 'signatureHash'],\n"
    "      message: 'metadata.signatureHash is only accepted with metadata.documentType \"sign\"',\n"
    "    });\n"
    "  }\n"
    "});\n")
E3=("        ? { identityCommitment: resolveIdentityCommitment(data) }\n        : {}),\n",
    "        ? { identityCommitment: resolveIdentityCommitment(data) }\n        : {}),\n"
    "      // KS-1454: the plain SHA-256 of S's detached .p7s, anchored VERBATIM (64 lowercase hex = exactly 64 bytes, the Cardano string cap, so the KS-1284 codec leaves it a single string).\n"
    "      ...(data.metadata?.signatureHash ? { signatureHash: data.metadata.signatureHash } : {}),\n")
TEST='''// KS-1454 (anchoring anchorSchema.ts): Platform-S signs a file detached and wants the SHA-256 of the .p7s in the chain with the sign anchor. Today zod strips the unknown metadata key, so S's hash is silently dropped and
// the anchor looks like a plain sign event. After the change: metadata.signatureHash (64 lowercase hex) is accepted, anchored verbatim as `signatureHash` beside documentType, and refused (400 at the route, a failed
// parse here) on any verb but `sign` and when malformed. Pure cells: zod, the payload builder and the Cardano metadatum codec; no port, no database, no chain.
import { describe, it, expect } from 'vitest';

import { anchorDocumentSchema, buildFlatAnchorMetadataPayload } from '../anchorSchema';
import { toCardanoMetadatum } from '../cardano/cardanoMetadatum';

const BASE_BODY = {
  documentId: 'doc-1777346021120-1e528170',
  contentHash: 'a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f70819203a4b5c6d7e8f9',
};
const SIG = 'd'.repeat(32) + '0123456789abcdef0123456789abcdef';

function signBody(signatureHash: unknown) {
  return { ...BASE_BODY, metadata: { documentType: 'sign', signatureHash } };
}

describe('KS-1454: metadata.signatureHash on the sign verb', () => {
  it('RED KS-1454 R1: a sign anchor carrying a signatureHash is accepted and the hash is anchored verbatim', () => {
    const parsed = anchorDocumentSchema.parse(signBody(SIG));
    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
    expect(sec.signatureHash).toBe(SIG);
    expect(sec.documentType).toBe('sign');
    expect(sec.hash).toBe(BASE_BODY.contentHash);
  });

  it('RED KS-1454 R2: the same hash on an upload anchor is refused, not anchored', () => {
    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'upload', signatureHash: SIG } });
    expect(result.success).toBe(false);
  });

  it('RED KS-1454 R3: a signatureHash with no documentType is refused', () => {
    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { signatureHash: SIG } });
    expect(result.success).toBe(false);
  });

  it.each([
    ['uppercase hex', SIG.toUpperCase()],
    ['63 characters', SIG.slice(1)],
    ['65 characters', SIG + '0'],
    ['non-hex', 'g'.repeat(64)],
    ['a number', 12345],
    ['an array', [SIG]],
  ])('RED KS-1454 R4: a malformed signatureHash (%s) on a sign anchor is refused', (_label, value) => {
    const result = anchorDocumentSchema.safeParse(signBody(value));
    expect(result.success).toBe(false);
  });

  it('RED KS-1454 R5: the anchored signatureHash reaches the Cardano metadatum as ONE string, not an array', () => {
    const parsed = anchorDocumentSchema.parse(signBody(SIG));
    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
    const onChain = toCardanoMetadatum(sec) as Record<string, unknown>;
    expect(onChain.signatureHash).toBe(SIG);
  });

  it('control KS-1454 C1: a sign anchor with no signatureHash is still accepted and anchors no signatureHash key', () => {
    const parsed = anchorDocumentSchema.parse({ ...BASE_BODY, metadata: { documentType: 'sign' } });
    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
    expect('signatureHash' in sec).toBe(false);
    expect(sec.documentType).toBe('sign');
  });

  it('control KS-1454 C2: an upload anchor with no signatureHash is still accepted', () => {
    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'upload' } }).success).toBe(true);
  });

  it('control KS-1454 C3: a body with no metadata at all is still accepted and anchors exactly the base keys', () => {
    const payload = buildFlatAnchorMetadataPayload(anchorDocumentSchema.parse(BASE_BODY), 'preview');
    expect(Object.keys(payload.secuura).sort()).toEqual(['algorithm', 'certId', 'documentId', 'hash', 'network', 'timestamp', 'type', 'version']);
  });

  it('control KS-1454 C4: a sign anchor with a signatureHash and an identityCommitment keeps both distinct', () => {
    const commitment = 'identity-commitment-l2.v1:' + 'b'.repeat(64);
    const parsed = anchorDocumentSchema.parse({ ...BASE_BODY, metadata: { documentType: 'sign', signatureHash: SIG, identityCommitment: commitment } });
    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
    expect(sec.identityCommitment).toBe(commitment);
    expect(sec.hash).toBe(BASE_BODY.contentHash);
  });
});
'''
S=dict(dir='ks_1454_p1',ticket='KS-1454',
 title='anchoring: accept and anchor platform-s\'s metadata.signatureHash (plain SHA-256 of the detached .p7s) on the sign verb, refuse it on any other verb (RUNG 2, code_patch: three insertions in one product + one NEW vitest file; p1 of KS-1454: the write side only)',
 intro="DRAFT by Spark operator 9 for Wednesday, 2026-10-29 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1454 (Stuart 2026-10-09, amended 10 Oct), items 1, 2 and 4 of its Suggested work: accept metadata.signatureHash (optional, `^[a-f0-9]{64}$`), carry it into the CIP-674 payload beside documentType, answer 400 on any verb but sign. NOT in this brief (p2 and later, other files): item 3, the read-back on GET /api/anchors/{id} and verify-by-hash (anchorReadback.ts, index.ts; KS-723 declares the by-id route), and the OpenAPI declaration in anchoring.openapi.ts (Stuart's served-spec gate reads FlatAnchorRequest.metadata.signatureHash, so S's switch stays off until p2 ships). KS-1175 did:jwk (#1805) is MERGED at the tip; this brief edits the same file after it. The ticket text asks K's minimisation review to object BEFORE building if it disagrees; no objection is recorded in the notes read (see UNMEASURED).",
 products=[(P,[E1,E2,E3])],
 prodnote=['product, modified in place: THREE insertions (a 2-line field in the metadata object after :214, a 9-line rule at the end of the superRefine after :247, a 2-line payload spread after :304)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 14 cells (R1-R3, R4 x6 and R5 red = 10, C1-C4 control = 4; pure: zod, the payload builder, the metadatum codec)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` from `Blockchain/Dev/services/anchoring',
 tier='code_patch', rung='2 (three insertions in one product, byte-exact; the new test given whole)',
 pins='''# code_patch, 3 insertions in anchoring anchorSchema.ts + a NEW vitest file; ref = ks1175-identity-anchoring (same pure zod + payload-builder shape); line = the first inserted line.
tier=code_patch
ref=Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
line=215
ctx=65536
''',
 wrong="Platform-S signs a file detached and wants the SHA-256 of the `.p7s` anchored with the sign event (KS-1454). `anchorDocumentSchema.metadata` (`anchorSchema.ts:178-215`) declares only `documentType`, `timestamp` and `identityCommitment`; zod strips every other key, so a `metadata.signatureHash` that S sends is silently dropped and the sign anchor looks like a plain one. `buildFlatAnchorMetadataPayload` (:265-319) is a fixed whitelist and has no `signatureHash` entry, so even a declared field would not reach the ledger. The change: (1) declare `signatureHash` in `metadata` as an optional string matching `^[a-f0-9]{64}$` (lowercase hex only, the ticket's pattern); (2) add a rule at the end of the existing `superRefine` that adds a custom issue when `metadata.signatureHash` is present and `metadata.documentType` is not `'sign'` (the ticket: 400 on any other verb, 'a requirement, not an option'); (3) add one conditional spread after the `identityCommitment` spread in the payload builder, `signatureHash` anchored verbatim under `secuura`. A 64-character lowercase-hex string is exactly 64 bytes, the Cardano string cap, so `toCardanoMetadatum` (`cardano/cardanoMetadatum.ts:59-62`, `> 64` bytes chunks) leaves it one string. `POST /api/anchors` calls `anchorDocumentSchema.parse` (`index.ts:477`) inside a try whose catch handles `z.ZodError` (:582), so a failed rule is the route's validation error, as for every other refusal here.",
 where="- `src/anchorSchema.ts:211-216` - `identityCommitment: z.string()...regex(...).optional(),` ends at :214 (`    ).optional(),`), then `  }).optional(),` :215 closes `metadata`, then the `// KS-1175: the top-level identity block` comment :216. **Must change:** insert two lines (a comment and the `signatureHash` field) between :214 and :215.\n- `src/anchorSchema.ts:239-248` - the `superRefine` body: the KS-1175 identityCommitment pair check ends with `  }` at :247 and the closing `});` at :248. **Must change:** insert a comment line and an 8-line `if` rule between :247 and :248.\n- `src/anchorSchema.ts:302-304` - `...(resolveIdentityCommitment(data)` `? { identityCommitment: resolveIdentityCommitment(data) }` `: {}),`. **Must change:** insert a comment and one spread line directly after :304.\n- NOT touched: `LIFECYCLE_VERBS`, `ACCEPTED_LIFECYCLE_VERBS`, `identitySchema`, `didField`, `resolveIdentityCommitment`, the seven identity spreads, `anchoring.openapi.ts`, `anchorReadback.ts`, `index.ts`, `cardano/cardanoMetadatum.ts`, and the existing exact-key-set cells in `__tests__/anchorSchema.test.ts` (:293-327: their inputs carry no `signatureHash`, so their key sets are unchanged).",
 exactnote="Three insertions in one file, in file order.\n",
 donot="**Do NOT touch** any other line of `anchorSchema.ts`, and no other file but the new test. In particular do not add a `signatureHash` to the openapi file, the read-back, or `identitySchema`; do not widen the regex to uppercase; do not add a length cap other than the regex.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports as in `ks1175-identity-anchoring.test.ts`, no top-level await. Every cell is pure (zod, `buildFlatAnchorMetadataPayload`, `toCardanoMetadatum`).",
 red=['RED KS-1454 R1','RED KS-1454 R2','RED KS-1454 R3','RED KS-1454 R4','RED KS-1454 R5'],
 cells="- RED `R1`: at the tip the key is stripped, so `sec.signatureHash` is `undefined` and the `toBe(SIG)` assertion fails; after the edit it is the input value. RED `R2`/`R3`/`R4`: at the tip the key is stripped and the parse succeeds, so `success` is `true` and `toBe(false)` fails; after the edit the refinement/regex refuses. RED `R5`: `onChain.signatureHash` is `undefined` at the tip. All fail by assertion, none by a throw (`parse` in R1/R5 succeeds at the tip because the unknown key is stripped).\n- CONTROL `C1`-`C4`: green at the tip AND after (no hash: no key; an upload with no hash accepted; the base key set; a hash beside an identityCommitment keeps both).",
 premises="- `anchorSchema.ts:178-215` is the `metadata` object with exactly `documentType` (:186), `timestamp` (:193), `identityCommitment` (:211-214); `:215` is `  }).optional(),`; read at `fd84001c738a`.\n- `anchorSchema.ts:234-248` is `.superRefine((data, ctx) => {` with one rule (the identityCommitment pair, :239-247) and `});` at :248; the issue is added with `ctx.addIssue({ code: z.ZodIssueCode.custom, path: [...], message })` (:242-246).\n- `anchorSchema.ts:302-304` is the identityCommitment spread; the whitelist rule in the doc comment at :257-264 says no object spreads of caller input.\n- `index.ts:477` `anchorDocumentSchema.parse(req.body)` in `POST /api/anchors`; `index.ts:582` `error instanceof z.ZodError`.\n- `cardano/cardanoMetadatum.ts:34` `CARDANO_METADATA_STRING_MAX_BYTES = 64`; :59-62 a string over 64 bytes is chunked, so a 64-byte string is not.\n- `__tests__/anchorSchema.test.ts:266-327`: `EVERY_OPTIONAL_FIELD` carries no `signatureHash`; the two exact-key-set cells therefore do not change.\n- vitest: `services/anchoring/package.json` `\"test\": \"vitest run\"`. The `ks1175-identity-anchoring.test.ts` file imports `describe, it, expect` from vitest and the two functions from `../anchorSchema` (:17-19).\n- The ticket (KS-1454, Linear export of 2026-10-12): pattern `^[a-f0-9]{64}$`; 'Restrict it to documentType = sign and answer 400 to it on any other verb (a requirement, not an option)'; one value, never an array.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether Secuura's minimisation review (KS-240) objects to a plain hash on the ledger: the ticket asks K to say so BEFORE building; Stuart ruled it acceptable; no K-side answer is recorded in the notes read. Kam's 19 Oct card ruling 'build all three [S contract additions] after KS-1454' treats KS-1454 as going ahead. Wednesday decides whether that is enough.\n- This brief is the write side only. The read-back (by-id and verify-by-hash with multiplicity), the OpenAPI declaration and the docs/openapi YAML are NOT here; until they ship S cannot read the hash back or pass its served-spec gate. Whether `docs/openapi/secuura-api.yaml` is generated from `anchoring.openapi.ts` and whether a spec-drift test exists that this change would turn red: not read (the whole-service suite in the checker A6 would show it).\n- `docs/VOCABULARY.md` mentions anchorSchema; whether it should list the new field: not read.\n- Whether S's `sign` events arrive with `documentType: 'sign'` for every detached signature, including any `certify`-aliased or lifecycle-endpoint path: the ticket says S posts a flat anchor with `sign`; not measured.\n- Open PRs touching anchorSchema.ts: not listed here; the raising seat checks (S's seatS did:jwk branch is merged).",
 scope="**Part 1 of KS-1454** (items 1, 2 and 4 of its suggested work). Link the PR as Refs KS-1454, not Closes: the read-back and the spec declaration remain. Follow-up briefs: p2 = read-back; p3 = anchoring.openapi.ts (+ KS-723 for the by-id route).",
)
