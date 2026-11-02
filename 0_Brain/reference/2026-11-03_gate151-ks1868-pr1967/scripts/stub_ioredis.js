// preload: replaces ONLY the ioredis module. Records constructions; a client whose 'error' was emitted is dead (commands reject like a closed connection).
const Module = require('module');
const orig = Module._load;
const store = new Map();
const reg = { clients: [], getCalls: 0, setCalls: 0, setFail: null };
globalThis.__redisReg = reg;
class FakeRedis {
  constructor(url, opts) { this.id = reg.clients.length + 1; this.dead = false; this.handlers = {}; this.url = url; reg.clients.push(this); }
  on(ev, fn) { (this.handlers[ev] = this.handlers[ev] || []).push(fn); return this; }
  emitError(v) { this.dead = true; for (const f of this.handlers.error || []) f(v); }
  get(k) { reg.getCalls++; return this.dead ? Promise.reject(new Error('Connection is closed.')) : Promise.resolve(store.has(k) ? store.get(k) : null); }
  set(k, v) { reg.setCalls++; if (this.dead) return Promise.reject(new Error('Connection is closed.')); if (reg.setFail !== null) return Promise.reject(reg.setFail()); store.set(k, v); return Promise.resolve('OK'); }
}
Module._load = function (request, parent, isMain) {
  if (request === 'ioredis') return { __esModule: true, default: FakeRedis };
  return orig.apply(this, arguments);
};
