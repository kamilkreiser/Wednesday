// loopback_pin.mjs — preload (--import): a listen(port[, cb]) with no host is pinned to 127.0.0.1; the bound address is written to $ADDR_OUT.
// Used ONLY because http-server.ts calls app.listen(PORT, cb) with no host; the service source is not edited.
import net from 'node:net';
import fs from 'node:fs';
const orig = net.Server.prototype.listen;
net.Server.prototype.listen = function (...a) {
  if (typeof a[0] === 'number' && typeof a[1] !== 'string') a.splice(1, 0, '127.0.0.1');
  this.once('listening', () => { try { fs.writeFileSync(process.env.ADDR_OUT, JSON.stringify({ pid: process.pid, ...this.address() })); } catch {} });
  return orig.apply(this, a);
};
