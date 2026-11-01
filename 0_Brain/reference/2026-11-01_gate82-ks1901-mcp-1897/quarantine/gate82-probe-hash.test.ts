import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import type { MockInstance } from 'vitest';
import { hostile, SECRETVAL } from './hostile.js';
const h = vi.hoisted(() => ({ toThrow: undefined as unknown }));
vi.mock('../hashing.js', () => ({ hashFile: () => Promise.reject(h.toThrow), extractFileName: (p: string) => p }));
import { registerHashTools } from '../tools/hash.js';
let errSpy: MockInstance<typeof console.error>;
beforeEach(() => { errSpy = vi.spyOn(console, 'error').mockImplementation(() => undefined); });
afterEach(() => errSpy.mockRestore());
describe('gate82 hash probe', () => {
  for (const [label, f] of hostile()) {
    it(label, async () => {
      const handlers: Record<string, (a: { filePath: string }) => Promise<any>> = {};
      registerHashTools({ tool: (n: string, _d: string, _s: unknown, fn: any) => { handlers[n] = fn; } } as never);
      h.toThrow = f();
      const r = await handlers['secuura_hash_document']({ filePath: 'x' });
      const wire = r.content[0].text;
      const log = errSpy.mock.calls.map((a) => a.map((x) => typeof x === 'string' ? x : '<<' + typeof x + '>>').join(' ')).join('\n');
      console.log('PROBE hash |', label, '| wire=', wire, '| log=', JSON.stringify(log));
      expect(r.isError).toBe(true);
      expect(wire).not.toContain(SECRETVAL);
      expect(log).not.toContain('<<');
    });
  }
});
