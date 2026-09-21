// 2026-09-21 17:5x — arms for common.js postKamMessage's ONE retry after the server's "wrapped to the addressed seat key" 400.
// Runs the page's own module in Node WebCrypto (the 09_webcrypto_phase3.mjs sandbox shape). Fixtures: the PUBLIC keys in app/keys.
import fs from "node:fs"; import vm from "node:vm"; import crypto from "node:crypto"; import path from "node:path";
const HERE = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8");
const kid = pem => crypto.createHash("sha256").update(Buffer.from(pem.split("\n").filter(l => l && !l.startsWith("-----")).join(""), "base64")).digest("hex").slice(0, 16);
const pub = n => fs.readFileSync(`${HERE}/app/keys/${n}`, "utf8");
const pilot = pub("kam-pilot-public.pub"), wed = pub("wednesday-seat-public.pub"), tue = pub("tuesday-seat-public.pub");
const ringStale = { kam: [{ name: "pilot", kid: kid(pilot), pem: pilot }], seats: { wednesday: { kid: kid(wed), pem: wed } }, seat_of_client: { WED: ["wednesday"], Secuura: ["wednesday"], Datasec: ["tuesday"], ALL: ["wednesday", "tuesday"] } };
const ringFresh = { ...ringStale, seats: { ...ringStale.seats, tuesday: { kid: kid(tue), pem: tue } } };
let fails = 0; const P = (ok, msg) => { console.log((ok ? "PASS  " : "FAIL  ") + msg); if (!ok) fails++; };
function mk(rings, postFn) {
  const calls = { pub: 0, post: 0 };
  const sandbox = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, console, localStorage: undefined, indexedDB: undefined,
    fetch: async (url, opts) => {
      if (url === "/api/pubkeys") { const r = rings[Math.min(calls.pub, rings.length - 1)]; calls.pub++; return { ok: true, status: 200, json: async () => r }; }
      if (url === "/api/kam/messages") { calls.post++; return postFn(JSON.parse(opts.body), calls.post); }
      throw new Error("unexpected fetch " + url); } };
  sandbox.globalThis = sandbox; vm.createContext(sandbox); vm.runInContext(src, sandbox); return { WED: sandbox.window.WED, calls };
}
const needTue = kid(tue);
const server = (b) => { const kids = new Set((b.envelope.wrapped_keys || []).map(e => e.kid)); kids.add(b.envelope.kid);
  return kids.has(needTue) ? { ok: true, status: 201, redirected: false, json: async () => ({ stored: { id: b.id } }) }
    : { ok: false, status: 400, redirected: false, json: async () => ({ detail: `reply must be wrapped to the addressed seat key(s) ['${needTue}'] (page out of date? reload)` }) }; };
// ARM 1: stale ring first, fresh ring on refetch -> ONE retry, 201, two POSTs, two pubkey fetches
{ const { WED, calls } = mk([ringStale, ringFresh], server); let ok = false; try { const j = await WED.postKamMessage("hello tuesday", "tuesday"); ok = !!(j && j.stored); } catch (e) { console.log("  threw: " + e.message); }
  P(ok && calls.post === 2 && calls.pub === 2, `ARM1 stale ring -> refused once -> refetched ring -> retried once -> 201 (posts=${calls.post}, pubkey fetches=${calls.pub})`); }
// ARM 2 (negative control): the ring stays stale -> retry once, still refused -> throws with the server's detail, exactly two POSTs, no loop
{ const { WED, calls } = mk([ringStale], server); let msg = ""; try { await WED.postKamMessage("hello tuesday", "tuesday"); } catch (e) { msg = e.message; }
  P(/wrapped to the addressed seat/.test(msg) && calls.post === 2, `ARM2 ring stays stale -> exactly ONE retry then the refusal surfaces (posts=${calls.post}): ${msg.slice(0, 60)}`); }
// ARM 3 (discriminating control): a DIFFERENT 400 is never retried
{ const other = () => ({ ok: false, status: 400, redirected: false, json: async () => ({ detail: "envelope must carry …" }) });
  const { WED, calls } = mk([ringFresh], other); let msg = ""; try { await WED.postKamMessage("x", "tuesday"); } catch (e) { msg = e.message; }
  P(/envelope must carry/.test(msg) && calls.post === 1, `ARM3 a different 400 is NOT retried (posts=${calls.post})`); }
// ARM 4 (quiet path): fresh ring from the start -> one POST, 201, wrapped to tuesday's kid
{ const { WED, calls } = mk([ringFresh], server); const j = await WED.postKamMessage("hi", "tuesday"); P(!!(j && j.stored) && calls.post === 1 && calls.pub === 1, `ARM4 fresh ring -> one POST 201 (posts=${calls.post}, pubkey fetches=${calls.pub})`); }
console.log(fails ? `### RESULT: ${fails} FAIL` : "### RESULT: ALL 4 ARMS PASS"); process.exit(fails ? 1 : 0);
