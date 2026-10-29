# KS-1454 p2 (Spark operator 10, 2026-10-29): read-back of metadata.signatureHash on GET /api/anchors/verify/:hash and GET /api/anchors/:id. code_patch2 (2 products + 1 NEW test), mk2.py.
P1='Blockchain/Dev/services/anchoring/src/anchorReadback.ts'
P2='Blockchain/Dev/services/anchoring/src/index.ts'
TP='Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts'
E1=("    identity: Object.keys(identity).length > 0 ? identity : null,\n  };\n}\n\nexport interface VerifyResponseContext {",
    "    identity: Object.keys(identity).length > 0 ? identity : null,\n  };\n}\n\n"
    "/**\n"
    " * KS-1454: the plain SHA-256 of Platform-S's detached .p7s, as anchored beside documentType on a `sign` anchor. A string under\n"
    " * `secuura.signatureHash` is read back verbatim (a 64-char lowercase-hex value is never chunked on chain); anything else, or no key at all\n"
    " * (every anchor that predates the field), reads `null`. Same source-agnostic read as anchorIdentityView: DB (logical) or chain payload.\n"
    " */\n"
    "export function anchorSignatureHashView(secuura: unknown): { signatureHash: string | null } {\n"
    "  const sec = (secuura && typeof secuura === 'object' ? secuura : {}) as Record<string, unknown>;\n"
    "  return { signatureHash: typeof sec.signatureHash === 'string' ? sec.signatureHash : null };\n"
    "}\n\n"
    "export interface VerifyResponseContext {")
E2=("      identity: identityView.identity,\n    },\n  };\n}",
    "      identity: identityView.identity,\n"
    "      // KS-1454: the SHA-256 of the detached .p7s anchored with a `sign` event (null for every other anchor), so a verifier can compare it.\n"
    "      signatureHash: anchorSignatureHashView(sec).signatureHash,\n"
    "    },\n  };\n}")
E3=("import { anchorIdentityView, buildVerifyResponse } from './anchorReadback';",
    "import { anchorIdentityView, anchorSignatureHashView, buildVerifyResponse } from './anchorReadback';")
E4=("    ...anchorIdentityView((anchor.metadataPayload as any)?.secuura),\n",
    "    ...anchorIdentityView((anchor.metadataPayload as any)?.secuura),\n"
    "    // KS-1454: the SHA-256 of the detached .p7s anchored with a `sign` event (S's \"signature anchored\" check); null for any other anchor.\n"
    "    ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),\n")
TEST='''// KS-1454 (anchoring read-back): S shows "signature anchored" from GET /api/anchors/:id and a verifier compares the hash from GET /api/anchors/verify/:hash. Before this change neither read returned the
// anchored `secuura.signatureHash`, so a hash that is on the ledger could not be read back. After it: anchorSignatureHashView reads the string (DB form or chain form), buildVerifyResponse carries it under
// metadata.signatureHash, and the by-id handler spreads the view into its res.json (index.ts is bootless, so that last point is a source-text guard, as in ks1175-getid-view-wired).
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

import * as RB from '../anchorReadback';
import { toCardanoMetadatum, fromCardanoMetadatum } from '../cardano/cardanoMetadatum';

const HASH = 'a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f70819203a4b5c6d7e8f9';
const SIG = 'd'.repeat(32) + '0123456789abcdef0123456789abcdef';
const COMMITMENT = 'identity-commitment-l2.v1:' + 'b'.repeat(64);
const SIGNED = {
  secuura: {
    version: '2.0', type: 'document', hash: HASH, algorithm: 'sha256',
    documentId: 'doc-1777346021120-1e528170', certId: 'doc-1777346021120-1e528170',
    timestamp: '2026-10-29T12:00:00.000Z', network: 'preview', documentType: 'sign', signatureHash: SIG,
    identityCommitment: COMMITMENT,
  },
};
const PLAIN = { secuura: { ...SIGNED.secuura, documentType: 'upload', signatureHash: undefined } };
const CTX = { hash: HASH, network: 'preview' };
const ROW = {
  transaction_hash: 'f'.repeat(64), block_number: 4242, confirmed_at: '2026-10-29T12:01:00.000Z',
  created_at: '2026-10-29T12:00:00.000Z', document_id: 'doc-1777346021120-1e528170', status: 'confirmed',
};
const SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
const FROM = SRC.indexOf("app.get('/api/anchors/:id',");
const END_LINE = 'retryCount: anchor.retryCount ?? 0,';
const GET_BY_ID = FROM < 0 ? '' : SRC.slice(FROM, SRC.indexOf(END_LINE, FROM) + END_LINE.length);

describe('KS-1454: the anchored signatureHash is read back', () => {
  it('RED KS-1454 B1: anchorSignatureHashView returns the anchored hash from a logical (DB-form) payload', () => {
    expect(RB.anchorSignatureHashView?.(SIGNED.secuura)).toEqual({ signatureHash: SIG });
  });

  it('RED KS-1454 B2: anchorSignatureHashView returns the same hash from a payload that went through the chain codec', () => {
    const chainForm = fromCardanoMetadatum(toCardanoMetadatum(SIGNED)) as typeof SIGNED;
    expect(typeof chainForm.secuura.signatureHash).toBe('string');
    expect(RB.anchorSignatureHashView?.(chainForm.secuura)).toEqual({ signatureHash: SIG });
  });

  it('RED KS-1454 B3: GET /api/anchors/verify/:hash (db source) carries the hash under metadata.signatureHash beside documentType', () => {
    const body = RB.buildVerifyResponse('db', SIGNED, ROW, CTX) as any;
    expect(body.metadata.signatureHash).toBe(SIG);
    expect(body.metadata.documentType).toBe('sign');
  });

  it('RED KS-1454 B4: GET /api/anchors/verify/:hash (chain source) carries the same hash', () => {
    const onChain = { secuura: (fromCardanoMetadatum(toCardanoMetadatum(SIGNED)) as typeof SIGNED).secuura, txHash: 'e'.repeat(64) };
    const body = RB.buildVerifyResponse('chain', onChain, undefined, CTX) as any;
    expect(body.metadata.signatureHash).toBe(SIG);
  });

  it('RED KS-1454 B5: the GET /api/anchors/:id handler imports anchorSignatureHashView and spreads it over the row metadata_payload secuura block', () => {
    expect(SRC.includes("import { anchorIdentityView, anchorSignatureHashView, buildVerifyResponse } from './anchorReadback';")).toBe(true);
    expect(GET_BY_ID.includes('...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),')).toBe(true);
  });

  it('control KS-1454 C1: an anchor with no signatureHash reads null (the key is never invented), on both reads', () => {
    expect(RB.anchorSignatureHashView?.(PLAIN.secuura) ?? { signatureHash: null }).toEqual({ signatureHash: null });
    expect((RB.buildVerifyResponse('db', PLAIN, ROW, CTX) as any).metadata.signatureHash ?? null).toBeNull();
  });

  it('control KS-1454 C2: a value that is not a string (a number, an array, an object) is not surfaced as a hash', () => {
    for (const bad of [12345, [SIG], { h: SIG }, null]) {
      expect(RB.anchorSignatureHashView?.({ ...SIGNED.secuura, signatureHash: bad }) ?? { signatureHash: null }).toEqual({ signatureHash: null });
    }
    expect(RB.anchorSignatureHashView?.(undefined) ?? { signatureHash: null }).toEqual({ signatureHash: null });
  });

  it('control KS-1454 C3: the identity read-back is unchanged by a signatureHash beside it', () => {
    expect(RB.anchorIdentityView(SIGNED.secuura)).toEqual({ identityCommitment: COMMITMENT, identity: null });
    expect((RB.buildVerifyResponse('db', SIGNED, ROW, CTX) as any).metadata.identityCommitment).toBe(COMMITMENT);
  });

  it('control KS-1454 C4: the block located in index.ts is ONE handler, the anchor-by-id route (contentHash and the KS-535 errorMessage are in it)', () => {
    expect([GET_BY_ID.split('app.get(').length, GET_BY_ID.includes('contentHash: anchor.contentHash,'), GET_BY_ID.includes('errorMessage: anchor.errorMessage || null,')]).toEqual([2, true, true]);
  });
});
'''
S=dict(dir='ks_1454_p2_readback',ticket='KS-1454',
 title='anchoring: read the anchored metadata.signatureHash back on GET /api/anchors/:id and GET /api/anchors/verify/:hash (RUNG 3, code_patch2: two products, three small insertions + one import edit, plus one NEW vitest file; p2 of KS-1454: the read-back only)',
 intro="DRAFT by Spark operator 10 for Wednesday, 2026-10-29 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1454 (Stuart 2026-10-09, amended 10 Oct), item 3 of its Suggested work, \"Read-back, precisely\": return the anchored `signatureHash` on GET /api/anchors/{id} (S's \"signature anchored\" comes from there) and on GET /api/anchors/verify/{contentHash} (a verifier compares). Part 1 (accept + anchor + 400 on other verbs, anchorSchema.ts) is brief `ks_1454_p1`; this brief does not depend on it applying (its cells feed the read functions a payload that already carries `signatureHash`). NOT in this brief: the OpenAPI declaration (anchoring.openapi.ts and the generated YAML and docs), and the ticket's \"multiplicity\" choice for verify-by-hash (list every anchor for the hash, or declare by-id the only public path): that is Stuart's/Kam's shape decision, so verify-by-hash keeps returning the ONE anchor it returns today and just gains the field.",
 products=[(P1,[E1,E2]),(P2,[E3,E4])],
 prodnote=['product, modified in place: a new exported function inserted after anchorIdentityView, and one field added to the metadata object of buildVerifyResponse','product, modified in place: one import line extended, one spread added in the GET /api/anchors/:id handler'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 9 cells (B1-B5 red, C1-C4 control; pure functions plus one source-text guard on index.ts, because index.ts calls app.listen on import)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` from `Blockchain/Dev/services/anchoring',
 tier='code_patch2', rung='3 (two products, byte-exact hunks; the new test given whole)',
 pins='''# code_patch2: 2 products in services/anchoring (anchorReadback.ts: new function + one metadata field; index.ts: import + one spread) + 1 NEW vitest; ref = the readback test (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts
line=55
ctx=65536
''',
 wrong="Platform-S anchors the SHA-256 of a detached `.p7s` with a `sign` event (KS-1454 part 1 writes it to `secuura.signatureHash`), and the ticket's item 3 says it must come back on the two reads S and a verifier use. Today neither read returns it. `buildVerifyResponse` (`anchorReadback.ts`) builds `metadata` field by field and has no `signatureHash`; the by-id handler (`index.ts` `app.get('/api/anchors/:id'`) spreads `anchorIdentityView(...)` and nothing for the signature. The change: (1) add an exported pure function `anchorSignatureHashView(secuura)` returning `{ signatureHash: string | null }` (a string value is returned verbatim; a missing key or a non-string value gives `null`); (2) add `signatureHash: anchorSignatureHashView(sec).signatureHash,` to the `metadata` object of `buildVerifyResponse`; (3) extend the `anchorReadback` import in `index.ts` with the new function and spread it in the by-id `res.json` directly after the `anchorIdentityView` spread. The existing `anchorIdentityView` is NOT changed (its cells use an exact `toEqual` on `{ identityCommitment, identity }`, so a new key there would turn them red).",
 where="- `src/anchorReadback.ts:49-55` - `anchorIdentityView` ends with `    identity: Object.keys(identity).length > 0 ? identity : null,` (:53), `  };` (:54), `}` (:55); :56 is blank and :57 `export interface VerifyResponseContext {`. **Must change:** insert the new function between :55 and :57.\n- `src/anchorReadback.ts:158-161` - the last field of the `metadata` object: `      identity: identityView.identity,` (:159) then `    },` (:160) `  };` (:161) `}` (:162). **Must change:** add a comment and one field after :159.\n- `src/index.ts:45` - `import { anchorIdentityView, buildVerifyResponse } from './anchorReadback';`. **Must change:** this one line gains `anchorSignatureHashView`.\n- `src/index.ts:958` - `    ...anchorIdentityView((anchor.metadataPayload as any)?.secuura),` inside `app.get('/api/anchors/:id'` (opens :895). **Must change:** add a comment and one spread line after it.\n- NOT touched: `anchorSchema.ts`, `anchoring.openapi.ts`, the verify-by-hash handler `handleAnchorVerifyByHash`, `anchorIdentityView`, `cardano/cardanoMetadatum.ts`, and every existing test.",
 exactnote="Two files, four insertions/edits, in file order (anchorReadback.ts first, then index.ts).\n",
 donot="**Do NOT touch** any other line of the two files, and no other file but the new test. In particular do not add `signatureHash` to `AnchorIdentityView` or `anchorIdentityView`, do not change the verify-by-hash lookup to return several anchors, and do not add anything to the OpenAPI file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports as in `ks1175-anchor-readback.test.ts` and `ks1175-getid-view-wired.test.ts`, no top-level await. The cells call the new function through `RB.anchorSignatureHashView?.(...)` so that, before the change, they fail by ASSERTION (an `undefined` result) and not by a TypeError.",
 red=['RED KS-1454 B1','RED KS-1454 B2','RED KS-1454 B3','RED KS-1454 B4','RED KS-1454 B5'],
 cells="- RED `B1`/`B2`: at the tip `RB.anchorSignatureHashView` is `undefined`, the optional call yields `undefined`, `toEqual({ signatureHash: SIG })` fails; after the edit it is the hash from the DB form / from the chain-codec round trip. RED `B3`/`B4`: at the tip `body.metadata.signatureHash` is `undefined`, `toBe(SIG)` fails. RED `B5`: at the tip the import line and the spread are absent, `toBe(true)` fails. All fail by assertion.\n- CONTROL `C1`-`C4`: green at the tip AND after (an anchor with no hash reads null/absent, non-string values are not surfaced, the identity read-back is unchanged, the located block is one handler). `C1`/`C2` use `?? { signatureHash: null }` so they pass on both trees.",
 premises="- `anchorReadback.ts:41-55` `anchorIdentityView(secuura: unknown)`: `const sec = (secuura && typeof secuura === 'object' ? secuura : {}) as Record<string, unknown>;` is its first line; read at `6d41673e0f79`.\n- `anchorReadback.ts:124-125` `const sec = onChain?.secuura || {};` ... `const identityView = anchorIdentityView(sec);`; the `metadata` object ends at :159-160 with `identity: identityView.identity,` then `},`.\n- `index.ts:45` the import; `index.ts:895` `app.get('/api/anchors/:id'`; `:957-958` the KS-1175 comment and the `anchorIdentityView` spread; `:959-964` the KS-535 `errorMessage` / `retryCount` fields close the `res.json`.\n- `__tests__/ks1175-anchor-readback.test.ts` and `ks1175-getid-view-wired.test.ts`: no cell does a whole-object `toEqual` on `buildVerifyResponse(...).metadata` (the cells read single keys), and the by-id guard locates the handler block from `app.get('/api/anchors/:id',` to the `retryCount` line, so a spread inserted inside it stays in the block.\n- `cardano/cardanoMetadatum.ts:34,59-62`: a string of 64 bytes is not chunked, so a 64-char hex hash is one string on chain and the codec round trip returns it as a string.\n- The ticket (KS-1454, Linear export of 2026-10-12): 'Return it on both reads S and a verifier use'; 'By id - GET /api/anchors/{id}: ... S's Verify comes from here'; 'By hash, with multiplicity: either list every anchor for the hash ... or state on this ticket that the public path is the by-id read only.'",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The ticket's multiplicity choice for verify-by-hash (list every anchor, or declare by-id the only public path) is NOT made here; the verify route still answers with one anchor, so for a content hash that has an upload anchor AND a sign anchor it may show the upload anchor and `signatureHash: null`. That is the open question on the ticket, for Stuart/Kam.\n- The OpenAPI declaration of the new response fields (and the KS-723 declaration of the by-id route), the generated YAML and the docs are not here; `generate-openapi --check` and `check:openapi` were not run on this change.\n- The by-id route over HTTP was not run (index.ts is bootless); the guard is a source-text cell, the real pin is a live read.\n- Whether `GET /api/anchors/document/:documentId` and the provenance surface should carry the field too: not read (the ticket names the two reads).\n- Open PRs touching these files: see the operator's overlap run in the report (gen/overlap.py).",
 scope="**Part 2 of KS-1454** (item 3, the read-back). Link the PR as Refs KS-1454, not Closes: the spec declaration and the multiplicity decision remain. It is independent of part 1 (`ks_1454_p1`) at the file level: p1 edits `anchorSchema.ts` only; this edits `anchorReadback.ts` and `index.ts`.",
)
