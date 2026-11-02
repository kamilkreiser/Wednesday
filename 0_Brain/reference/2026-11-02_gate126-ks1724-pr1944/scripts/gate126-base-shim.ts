// QA GATE 126: the BASE stand-in for the PR's exports, so the PR's own cells run against base behaviour (a bare
// express.json with the caller's options, no structural walk). Not part of the PR; placed in the base tree for one run.
import express, { type RequestHandler } from 'express';
export const STRUCTURAL_JSON_DEFAULTS = { maxArrayLength: 1000, maxNodes: 20000, maxDepth: 32 } as const;
export const STRUCTURAL_JSON_ENV = { maxArrayLength: 'JSON_BODY_MAX_ARRAY_LENGTH', maxNodes: 'JSON_BODY_MAX_NODES', maxDepth: 'JSON_BODY_MAX_DEPTH' } as const;
export function boundedJson(options: Record<string, unknown>): RequestHandler {
  const { service: _s, ...rest } = options;
  return express.json(rest as Parameters<typeof express.json>[0]);
}
export function findStructuralBreach(_v: unknown, _c: unknown): null { return null; }
