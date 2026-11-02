// Minimal CBOR encoder (uint, nint, bytes, text, array, Map). cbor@9.0.2's encoder truncates maps/arrays on Node 26 (measured).
function head(major, n) {
  if (n < 24) return Buffer.from([(major << 5) | n]);
  if (n < 256) return Buffer.from([(major << 5) | 24, n]);
  if (n < 65536) { const b = Buffer.alloc(3); b[0] = (major << 5) | 25; b.writeUInt16BE(n, 1); return b; }
  const b = Buffer.alloc(5); b[0] = (major << 5) | 26; b.writeUInt32BE(n, 1); return b;
}
function enc(v) {
  if (typeof v === 'number') return v >= 0 ? head(0, v) : head(1, -1 - v);
  if (Buffer.isBuffer(v)) return Buffer.concat([head(2, v.length), v]);
  if (typeof v === 'string') { const b = Buffer.from(v, 'utf8'); return Buffer.concat([head(3, b.length), b]); }
  if (Array.isArray(v)) return Buffer.concat([head(4, v.length), ...v.map(enc)]);
  if (v instanceof Map) { const parts = [head(5, v.size)]; for (const [k, x] of v) parts.push(enc(k), enc(x)); return Buffer.concat(parts); }
  throw new Error('cborlite: unsupported');
}
module.exports = { encode: enc };
