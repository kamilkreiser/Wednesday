// emulates BASE catch shape with a revoked Proxy thrown; then a line that must NOT run if gate fails closed
const {proxy,revoke}=Proxy.revocable({}, {}); revoke();
try { throw proxy; } catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`FATAL: ${message}`); process.exit(1);
}
console.log('GATE PASSED - SERVING');
