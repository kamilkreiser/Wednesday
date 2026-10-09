/**
 * KS-1287: GET /api/status/{id}/check/{index} published its path parameter index as required: false - the only
 * optional path parameter in the spec (OpenAPI 3 requires required: true on every in: path parameter; Schemathesis
 * 4.27.5 reports it as a Schema Error). Mechanism, measured in-process: zod-to-openapi v7 computes required as
 * not-isOptional and not-isNullable, and z.coerce.number() parses null as 0, so the coerce wrapper reads as
 * nullable. The one-site fix pins required: true through the param metadata. This suite generates the document
 * in-process from vc-issuer.openapi.ts the way scripts/generate-openapi.ts does.
 */
import { describe, it, expect } from 'vitest';
import '../vc-issuer.openapi';
import { generateOpenApiDocument } from '@secuura/shared';

type Param = { name: string; in: string; required?: boolean; schema?: { type?: string; minimum?: number } };
type Operation = { operationId?: string; parameters?: Param[] };

const doc = generateOpenApiDocument({ title: 'ks1287', version: '0.0.0' }) as unknown as {
  paths: Record<string, Record<string, Operation>>;
};
const op = doc.paths['/api/status/{id}/check/{index}'].get;
const params = op.parameters ?? [];
const indexParam = params.find((p) => p.name === 'index');
const idParam = params.find((p) => p.name === 'id');

function optionalPathParams(): string[] {
  const out: string[] = [];
  for (const [routePath, item] of Object.entries(doc.paths)) {
    for (const [method, operation] of Object.entries(item)) {
      for (const p of operation.parameters ?? []) {
        if (p.in === 'path' && p.required !== true) out.push(method + ' ' + routePath + ' ' + p.name);
      }
    }
  }
  return out;
}

describe('KS-1287: the index path parameter of GET /api/status/{id}/check/{index} is published required', () => {
  it('RED KS-1287 A: the index path parameter renders required: true', () => {
    expect(indexParam?.required).toBe(true);
  });

  it('RED KS-1287 B: no vc-issuer operation publishes an optional in: path parameter', () => {
    expect(optionalPathParams()).toEqual([]);
  });

  it('control: the operation and its two path parameters are registered', () => {
    expect(op.operationId).toBe('getStatusByIdCheckByIndex');
    expect(params.filter((p) => p.in === 'path').map((p) => p.name)).toEqual(['id', 'index']);
  });

  it('control: the id sibling renders required: true and index keeps its pinned integer schema', () => {
    expect(idParam?.required).toBe(true);
    expect(indexParam?.schema?.type).toBe('integer');
    expect(indexParam?.schema?.minimum).toBe(0);
  });
});
