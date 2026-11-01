// Gate 73: the head's BUILT dist with the REAL winston logger. Residual-class probe:
// an Error whose message is READABLE but is not a string (a revoked Proxy, or an object whose toJSON throws).
// The inner try does not throw for these (instanceof + .message succeed), so `reason` is a non-string handed to logger.error.
// Also: an onEvent rejection from the timer-driven flush (no catch around this.flush() in the interval).
const dist = process.argv[2];
const { AuditLogger, AuditEventCategory } = require(dist + '/security/audit-logger.js');

function revoked() { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
const cases = {
  'Error.message = revoked Proxy': () => { const e = new Error('x'); Object.defineProperty(e, 'message', { value: revoked() }); return e; },
  'Error.message = {toJSON throws}': () => { const e = new Error('x'); Object.defineProperty(e, 'message', { value: { toJSON() { throw new Error('toJSON boom'); } } }); return e; },
  'Error.message = BigInt': () => { const e = new Error('x'); Object.defineProperty(e, 'message', { value: 10n }); return e; },
  'revoked Proxy (control, the fixed case)': revoked,
};

(async () => {
  for (const [label, mk] of Object.entries(cases)) {
    let fail = true; let delivered = 0;
    const a = new AuditLogger({ serviceName: 's', version: '1', environment: 'test', hashIntegrity: true, flushIntervalMs: 3600000,
      onEvent: () => { if (fail) return Promise.reject(mk()); delivered++; return Promise.resolve(); } });
    await a.log(AuditEventCategory.SECURITY, 'X');
    let threw = null;
    try { await a.flush(); } catch (e) { threw = (e && e.message) || String(e); }
    const buf = a.eventBuffer.length;
    fail = false; try { await a.flush(); } catch (e) { /* ignore */ }
    a.stopFlushTimer();
    console.log(`G73_REAL ${label}: flush_threw=${threw === null ? 'no' : JSON.stringify(threw)} buffer_after_fail=${buf} delivered_after_retry=${delivered}`);
  }
})().catch((e) => { console.log('G73_REAL harness error', e); process.exitCode = 2; });
