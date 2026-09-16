// qa-netredirect.setup.ts — vitest setupFile for the flake-shape runs of the SEAT's file. Redirects EVERY outbound socket
// connect to 127.0.0.1: QA1004_NET=rst -> a port that was bound then closed (ECONNREFUSED at once: the "fast RST" CI box);
// QA1004_NET=silent -> a listener that accepts and never answers (the "hang" the seat's cells assume, made deterministic).
import * as net from 'net';
const mode = process.env.QA1004_NET || 'rst';
const origConnect = net.Socket.prototype.connect;
const srv = net.createServer(() => {});
await new Promise<void>((r) => srv.listen(0, '127.0.0.1', () => r()));
const port = (srv.address() as net.AddressInfo).port;
if (mode === 'rst') await new Promise<void>((r) => srv.close(() => r()));
else srv.unref();
(net.Socket.prototype as any).connect = function (...args: any[]) {
  const o = Array.isArray(args[0]) ? args[0][0] : args[0];
  if (o && typeof o === 'object' && o.host !== '127.0.0.1') { (globalThis as any).__qa1004_redirects = ((globalThis as any).__qa1004_redirects || 0) + 1; o.host = '127.0.0.1'; o.port = port; delete o.lookup; }
  return (origConnect as any).apply(this, args);
};
