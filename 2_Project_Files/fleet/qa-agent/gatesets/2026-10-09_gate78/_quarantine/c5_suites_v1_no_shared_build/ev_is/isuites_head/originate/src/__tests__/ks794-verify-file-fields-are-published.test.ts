/**
 * =============================================================================
 * KS-794 — the verify-file body fields must be DISCOVERABLE FROM THE SCHEMA
 * =============================================================================
 * The defect: both verify-file handlers return `fileSize` on every 200, and the
 * v1 one also returns `fileHash`, while neither response schema declared any of
 * them. Both bases are `.passthrough()`, so the responses validated and nothing
 * went red — a consumer reading the spec simply could not know the fields exist.
 *
 * WHY A TEST AND NOT JUST THE REGENERATED YAML. `check:openapi` proves the
 * committed yaml matches what the generator emits. It cannot prove the generator
 * declares any particular field: delete the two lines from the schema, regenerate,
 * and `check:openapi` is green again on a spec that has silently lost them. The
 * same blindness KS-811 records, and it is why this file exists.
 *
 * WHY `fileHash` IS ON v1 ONLY, asserted here so the asymmetry cannot be "tidied"
 * away by someone who reads it as an oversight. MEASURED at source: v1
 * verify-file returns `fileHash`; the v2 handler computes the same sha256 over the
 * same bytes and returns it as `hash`. Declaring `fileHash` on V2VerifyResponse
 * would publish a field no v2 operation emits. Renaming either is a breaking
 * change and is not proposed (KS-794), so the divergence is asserted, not fixed.
 * =============================================================================
 */
import { sharedRegistry } from '@secuura/shared';

// Imported for the side effect: this is what registers the schemas. Without it
// every assertion below would read an empty registry, and "the field is missing"
// would be indistinguishable from "nothing was registered" — which is why each
// cell asserts the schema was FOUND before it asserts anything about its shape.
import '../originate.openapi';

type AnyDef = Record<string, any>;

/** The registered schema with this refId, or undefined. */
function registered(refId: string): AnyDef | undefined {
  const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
  return defs.find((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === refId);
}

/** The published property names of a registered object schema. */
function props(refId: string): string[] {
  const shape = registered(refId)?.schema?._def?.shape?.() ?? registered(refId)?.schema?.shape ?? {};
  return Object.keys(shape);
}

/** The zod type name of one published property, e.g. ZodOptional wrapping ZodNumber. */
function innerTypeName(refId: string, prop: string): string {
  const shape = registered(refId)?.schema?._def?.shape?.() ?? registered(refId)?.schema?.shape ?? {};
  const p = shape[prop];
  const inner = p?._def?.innerType ?? p;
  return String(inner?._def?.typeName ?? 'MISSING');
}

/** Is the published property optional? */
function isOptional(refId: string, prop: string): boolean {
  const shape = registered(refId)?.schema?._def?.shape?.() ?? registered(refId)?.schema?.shape ?? {};
  return shape[prop]?.isOptional?.() === true;
}

describe('KS-794 — verify-file response fields are declared, not only described', () => {
  it('KS-794 V1PUBLISHESBOTH: VerifyResponse declares fileSize as an optional integer and fileHash as an optional string', () => {
    // non-vacuity first: an unregistered schema would make every later assertion trivially wrong
    // in a way that reads like a missing field.
    expect([registered('VerifyResponse') !== undefined, props('VerifyResponse').length > 0])
      .toEqual([true, true]);
    expect([
      props('VerifyResponse').includes('fileSize'),
      innerTypeName('VerifyResponse', 'fileSize'),
      isOptional('VerifyResponse', 'fileSize'),
      props('VerifyResponse').includes('fileHash'),
      innerTypeName('VerifyResponse', 'fileHash'),
      isOptional('VerifyResponse', 'fileHash'),
    ]).toEqual([true, 'ZodNumber', true, true, 'ZodString', true]);
  });

  it('KS-794 V2PUBLISHESFILESIZEONLY: V2VerifyResponse declares fileSize, keeps hash, and does NOT declare fileHash', () => {
    expect([registered('V2VerifyResponse') !== undefined, props('V2VerifyResponse').length > 0])
      .toEqual([true, true]);
    expect([
      props('V2VerifyResponse').includes('fileSize'),
      innerTypeName('V2VerifyResponse', 'fileSize'),
      isOptional('V2VerifyResponse', 'fileSize'),
      // the asymmetry, asserted as an ABSENCE — with the presence of `hash` proving the schema was
      // really read, so "fileHash is absent" cannot pass by the shape coming back empty.
      props('V2VerifyResponse').includes('hash'),
      props('V2VerifyResponse').includes('fileHash'),
    ]).toEqual([true, 'ZodNumber', true, true, false]);
  });

  it('KS-794 NOTONLYPROSE: neither field is discoverable from the description alone — each is a real property', () => {
    // The state this ticket closed was "named in the description, absent from the schema". This cell
    // fails if someone reverts to that: a description mentioning the field is NOT the deliverable.
    const v1 = props('VerifyResponse');
    const v2 = props('V2VerifyResponse');
    expect([
      v1.length > 0 && v2.length > 0,             // both schemas really read
      v1.includes('fileSize') && v1.includes('fileHash'),
      v2.includes('fileSize'),
    ]).toEqual([true, true, true]);
  });
});
