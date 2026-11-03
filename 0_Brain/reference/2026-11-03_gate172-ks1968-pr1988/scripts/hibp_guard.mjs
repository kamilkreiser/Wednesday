// Gate 172 outbound guard (written by the gate, independent of the builder's /private/tmp/f28t/hibp_guard.mjs).
// Loaded with NODE_OPTIONS=--import=<this>. Blocks and counts any attempt to reach api.pwnedpasswords.com at THREE layers:
//   1. globalThis.fetch (the URL), 2. dns.lookup / dns.promises.lookup (the hostname), 3. net/tls connect (host option).
// Writes one line per block to $GATE_GUARD_LOG: "<pid> <layer> BLOCKED". Never writes a URL path or a value.
import { appendFileSync } from 'node:fs';
import dns from 'node:dns';
import net from 'node:net';
import tls from 'node:tls';
import { createRequire } from 'node:module';
const LOG = process.env.GATE_GUARD_LOG;
// The control host (.invalid never resolves, RFC 6761) is blocked by the SAME code, so a positive control proves every layer
// fires without any risk of a packet to the real service if the guard were broken.
const HOST = /((^|\.)api\.pwnedpasswords\.com|^gate172-guard-control\.invalid)\.?$/i;
export const GATE_HOST_RE = HOST;
const note = (layer) => { try { if (LOG) appendFileSync(LOG, `${process.pid} ${layer} BLOCKED\n`); } catch {} };
try { if (process.env.GATE_GUARD_LOADED) appendFileSync(process.env.GATE_GUARD_LOADED, `${process.pid}\n`); } catch {}

const realFetch = globalThis.fetch;
globalThis.fetch = async function gateGuardedFetch(input, init) {
  let host = '';
  try { const u = typeof input === 'string' ? input : (input && input.url) || String(input); host = new URL(u).hostname; } catch { host = ''; }
  if (HOST.test(host)) { note('fetch'); throw new Error('gate172 guard: breach service blocked'); }
  return realFetch.call(this, input, init);
};

const realLookup = dns.lookup;
dns.lookup = function gateLookup(hostname, options, cb) {
  if (typeof hostname === 'string' && HOST.test(hostname)) {
    note('dns');
    const callback = typeof options === 'function' ? options : cb;
    const e = Object.assign(new Error('gate172 guard: dns blocked'), { code: 'ENOTFOUND' });
    process.nextTick(() => callback(e));
    return {};
  }
  return realLookup.apply(this, arguments);
};
const realPLookup = dns.promises.lookup;
dns.promises.lookup = async function gatePLookup(hostname, ...rest) {
  if (typeof hostname === 'string' && HOST.test(hostname)) { note('dns.promises'); throw Object.assign(new Error('gate172 guard: dns blocked'), { code: 'ENOTFOUND' }); }
  return realPLookup.call(this, hostname, ...rest);
};
// CJS view of the same modules (undici and http load them via require).
try {
  const req = createRequire(import.meta.url);
  const cdns = req('dns'); if (cdns.lookup !== dns.lookup) cdns.lookup = dns.lookup;
} catch {}

for (const [mod, name] of [[net, 'net'], [tls, 'tls']]) {
  const real = mod.connect;
  const wrapped = function gateConnect(...args) {
    const a0 = args[0];
    const host = a0 && typeof a0 === 'object' ? (a0.host || a0.servername || '') : (typeof args[1] === 'string' ? args[1] : '');
    if (typeof host === 'string' && HOST.test(host)) { note(name); throw new Error('gate172 guard: connect blocked'); }
    return real.apply(this, args);
  };
  mod.connect = wrapped;
  if (name === 'net') mod.createConnection = wrapped;
}

// Make ESM named imports of these builtins see the patched functions too.
try { (await import('node:module')).syncBuiltinESMExports(); } catch {}
