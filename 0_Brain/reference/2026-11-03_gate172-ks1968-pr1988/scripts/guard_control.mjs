// Positive control for the gate172 guard. Never addresses the real breach service: every request uses the .invalid control host.
const orig = globalThis.fetch;                       // captured BEFORE the guard: proves the lower layers catch a fetch that bypasses layer 1
const { GATE_HOST_RE } = await import(process.argv[2]);
const https = await import('node:https');
const dns = await import('node:dns');
const out = {};
out.regex_real_host = GATE_HOST_RE.test('api.pwnedpasswords.com');           // pure string test, no I/O
out.regex_other_host = GATE_HOST_RE.test('example.com');
const C = 'https://gate172-guard-control.invalid/range/00000';
try { await fetch(C); out.fetch = 'NOT BLOCKED'; } catch (e) { out.fetch = String(e.message); }
try { await orig(C); out.unguarded_fetch = 'NOT BLOCKED'; } catch (e) { out.unguarded_fetch = String(e?.cause?.message ?? e.message); }
out.https_get = await new Promise((r) => { try { const q = https.get(C, () => r('NOT BLOCKED')); q.on('error', (e) => r(e.message)); } catch (e) { r(e.message); } });
out.dns = await new Promise((r) => dns.lookup('gate172-guard-control.invalid', (e) => r(e ? e.message : 'NOT BLOCKED')));
console.log(JSON.stringify(out, null, 1));
