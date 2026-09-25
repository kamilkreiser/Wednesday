#!/bin/bash
# drafter_nodeprobe_g25t1.sh — the drafter's LIVE node probes for gate25T1 (PREDICTIONS, never the gate's evidence). Plain node, no repo code, no
# network, no port: (1) HDR-THROW: does node's own ServerResponse.setHeader throw for a header NAME with a space / a VALUE with CR-LF — the two inputs
# #1269's `for (const [name, value] of Object.entries(err.headers)) res.setHeader(name, value)` forwards unvalidated; with a CONTROL (a valid pair
# must NOT throw). (2) ENV-NAN: what `Number(process.env.X || 50)` yields for a garbage value, and what `NaN <= 0` and `Math.min(2000, NaN)` give —
# #1274's three bounds; and how long setTimeout(fn, NaN) actually waits (node coerces it), with a CONTROL setTimeout(fn, 50).
set -u
node --version
node -e '
const http = require("http");
const res = new http.ServerResponse(new http.IncomingMessage(null));
for (const [n, v, what] of [["Allow", "GET", "CONTROL valid pair"], ["Bad Name", "x", "name with a space"], ["X-Ok", "a\r\nInjected: 1", "value with CR-LF"], ["X-Num", NaN, "value NaN (number)"]]) {
  try { res.setHeader(n, v); console.log("setHeader", JSON.stringify(n), "->", "no throw (" + what + "), stored", JSON.stringify(res.getHeader(n))); }
  catch (e) { console.log("setHeader", JSON.stringify(n), "->", "THROWS", e.code, "(" + what + ")"); }
}
for (const raw of ["abc", "", "0", "-5", "25"]) {
  const v = Number(raw || 50); console.log("MAX_ROWS env=" + JSON.stringify(raw), "->", v, "| NaN<=0:", v <= 0, "| Math.min(2000,v):", Math.min(2000, v));
}
const t0 = Date.now();
setTimeout(() => { console.log("setTimeout(fn, NaN) fired after", Date.now() - t0, "ms");
  const t1 = Date.now(); setTimeout(() => console.log("CONTROL setTimeout(fn, 50) fired after", Date.now() - t1, "ms"), 50); }, NaN);
' 2>&1
echo "rc=$?"
