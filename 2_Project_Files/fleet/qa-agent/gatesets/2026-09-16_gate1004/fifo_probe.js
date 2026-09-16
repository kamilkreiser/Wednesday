// fifo_probe.js — a REAL dns/promises lookup made deterministically slow with NO network: UV_THREADPOOL_SIZE=1 and the
// only threadpool thread parked in open(2) on a FIFO that no writer ever opens. getaddrinfo is queued behind it and never
// runs, so no DNS query leaves the host. Usage: UV_THREADPOOL_SIZE=1 node fifo_probe.js <dist ssrf-guard.js> <fifo> <label> <timeoutMs>
const fs = require('fs');
const [guardPath, fifo, label, tms] = process.argv.slice(2);
const g = require(guardPath);
const timeoutMs = Number(tms);
fs.promises.open(fifo, 'r'); // parks the single threadpool thread
let statDone = false;
setTimeout(async () => {
  fs.promises.stat(__filename).then(() => { statDone = true; }); // positive control: must NOT complete (pool is parked)
  const unhandled = []; process.on('unhandledRejection', (e) => unhandled.push(String(e && e.message || e)));
  const t0 = Date.now();
  const pending = g.safeOutboundRequest('https://qa-gate-1004.example.com/', { timeoutMs });
  const bound = timeoutMs + 1200;
  const r = await Promise.race([pending.then((v) => ({ settled: true, v })), new Promise((res) => setTimeout(() => res({ settled: false }), bound))]);
  const elapsed = Date.now() - t0;
  await new Promise((res) => setTimeout(res, 300));
  const active = process.getActiveResourcesInfo();
  const line = JSON.stringify({ label, node: process.version, UV_THREADPOOL_SIZE: process.env.UV_THREADPOOL_SIZE, timeoutMs, observeBoundMs: bound, settled: r.settled, elapsedMs: elapsed, result: r.v, statControlCompleted: statDone,
    getAddrInfoPendingAfterReturn: active.filter((x) => x === 'GetAddrInfoReqWrap').length, fsReqPending: active.filter((x) => x === 'FSReqPromise' || x === 'FSReqCallback').length, active, unhandled }) + '\n';
  // process.exit() would JOIN the parked threadpool thread (libuv shutdown) and hang; releasing the FIFO would let the queued
  // getaddrinfo run (a real DNS query). So: write synchronously (main thread, no pool), then SIGKILL self. Measured first run: exit hung.
  fs.writeFileSync(process.env.QA1004_FIFO_OUT, line);
  process.kill(process.pid, 'SIGKILL');
}, 100);
