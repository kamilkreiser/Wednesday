import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import { parseAccessLine, foldGatewayLog } from '../../../src/scan/gatewayTimeline';
const D = process.env.G132_EVID as string;
describe('g132', () => {
  it('base and head lines parse identically (except time second)', () => {
    const b = fs.readFileSync(D + '/log_base.txt', 'utf8').trim().split('\n');
    const h = fs.readFileSync(D + '/log_head.txt', 'utf8').trim().split('\n');
    b.forEach((l, i) => {
      const pb = parseAccessLine(l); const ph = parseAccessLine(h[i] as string);
      expect(pb).not.toBeNull(); expect(ph).not.toBeNull();
      expect({ ...ph, epoch: 0 }).toEqual({ ...pb, epoch: 0 });
    });
    expect(foldGatewayLog(h.join('\n')).reduce((n, r) => n + r.requests, 0)).toBe(2);
  });
  it('control: garbage is null', () => expect(parseAccessLine('nope')).toBeNull());
});
