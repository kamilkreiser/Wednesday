/**
 * KS-1410 (the tenant-provisioning file of the class): the catch blocks of tenant-provisioning/src/index.ts answered 500 with the thrown text
 * as the response message (`message: message`), so a driver message or an internal host:port reached the caller. The six handlers other than
 * POST /api/tenants now log the thrown text with console.error and answer the constant message below.
 * POST /api/tenants (the key-generation path, whose 500 answer is Kam's open card secuura-ks1240-tenant-create-key-fail-answer-1028) is NOT
 * changed here and must stay as it is. Source-text guard: the module starts a server and a pool on import, so the file is read, not imported.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
const CONSTANT = 'An unexpected error occurred';

type Five = { line: number; stmt: string; handler: string; context: string };

/** Every statement that answers 500 through `.status(500).json(...)`, with the route it sits in and the 4 lines (plus the same line's prefix) before it. */
function fiveHundreds(source: string): Five[] {
  const lines = source.split('\n');
  const out: Five[] = [];
  lines.forEach((text, i) => {
    const at = text.indexOf('.status(500).json(');
    if (at < 0) return;
    let handler = '';
    for (let j = i; j >= 0; j--) {
      const m = /^\s*(?:app|router)\.(get|post|put|patch|delete)\(\s*'([^']+)'/.exec(lines[j]);
      if (m) {
        handler = m[1].toUpperCase() + ' ' + m[2];
        break;
      }
    }
    out.push({ line: i + 1, stmt: text.slice(at), handler, context: lines.slice(Math.max(0, i - 4), i).join('\n') + '\n' + text.slice(0, at) });
  });
  return out;
}

/** True when the response argument names a caught value: an identifier left once string literals and the envelope keys are removed. */
function leaks(stmt: string): boolean {
  const bare = stmt.replace(/'[^']*'/g, "''").replace(/\b(success|error|code|message|verified)\s*:/g, '');
  return /\b(err|error|msg|message|detail|details|stack)\b/.test(bare);
}

const FIVE = fiveHundreds(SRC);

const EXEMPT = 'POST /api/tenants';
const CHANGED = FIVE.filter((f) => f.handler !== EXEMPT);

describe('tenant-provisioning index.ts: no 500 answer carries the thrown text', () => {
  it('RED tp-500 P1 no 500 answer outside POST /api/tenants names a caught value', () => {
    expect(CHANGED.filter((f) => leaks(f.stmt)).map((f) => f.handler)).toEqual([]);
  });

  it('RED tp-500 P2 each of the six answers the constant message', () => {
    expect(CHANGED.map((f) => f.handler)).toHaveLength(6);
    expect(CHANGED.filter((f) => !f.stmt.includes("message: '" + CONSTANT + "'")).map((f) => f.handler)).toEqual([]);
  });

  it('RED tp-500 P3 each of the six logs the thrown text with console.error just before it answers', () => {
    expect(CHANGED.filter((f) => !/console\.error\(.*\b(message|err)\b/.test(f.context)).map((f) => f.handler)).toEqual([]);
  });

  it('control tp-500 C1 the scanner flags a leaking answer and passes the constant one', () => {
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });")).toBe(true);
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'x', details: { detail: msg } } });")).toBe(true);
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: '" + CONSTANT + "' } });")).toBe(false);
  });

  it('control tp-500 C2 the file has exactly seven 500 answers and POST /api/tenants is untouched', () => {
    expect(FIVE).toHaveLength(7);
    const post = FIVE.filter((f) => f.handler === EXEMPT);
    expect(post).toHaveLength(1);
    expect(post[0].stmt).toContain('message: message');
  });

  it('control tp-500 C3 the three 400 validation answers keep their details', () => {
    expect(SRC.split("details: err.errors").length - 1).toBe(3);
  });
});
