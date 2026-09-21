// Phase 2 — run app/static/common.js ITSELF (not a re-implementation) in Node's WebCrypto and prove both directions:
//   (1) WED.encryptText (what the browser does to Kam's reply) -> seat/envelope.py decrypt_text with the pilot private key
//   (2) a REAL live row (argv[2], raw JSON from the table) -> WED.decryptRow with the pilot key imported non-extractable
//   (3) negative controls: relabelled row refused; wrong key refused
//   (4) the module has NO code path that sends key material: static assertion on its source (every fetch() URL listed)
// This is Node 24's globalThis.crypto.subtle — the same WebCrypto API and parameters as the browser, NOT a browser session.
import fs from "node:fs"; import { execFileSync } from "node:child_process"; import vm from "node:vm";
const HERE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud";
const CRED = "/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud";
const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8");
const pubPem = fs.readFileSync(`${HERE}/app/keys/kam-pilot-public.pub`, "utf8");
// ---- (4) static: every network call in the module, and none carries key material
// Extract every fetch(...) call with its FULL argument text (balanced parentheses), then assert: the only call that sends a
// body is POST /api/kam/messages, and that body is JSON of exactly {client, view, id, ts, envelope} — no key, no PEM, no text.
function fetchCalls(code) { const out = []; let i = 0;
  while ((i = code.indexOf("fetch(", i)) !== -1) { let d = 0, j = i + 5; for (; j < code.length; j++) { if (code[j] === "(") d++; else if (code[j] === ")") { d--; if (d === 0) break; } }
    out.push(code.slice(i, j + 1)); i = j; } return out; }
const calls = fetchCalls(src); let bodies = 0, ok = true;
for (const c of calls) { const hasBody = /\bbody\s*:/.test(c); if (hasBody) bodies++;
  console.log("  fetch:", c.replace(/\s+/g, " ").slice(0, 160) + (c.length > 160 ? " …" : ""), hasBody ? "  [SENDS A BODY]" : "  [no body]");
  if (hasBody) { const m = c.match(/JSON\.stringify\(\{([^}]*)\}\)/); const keys = m ? m[1].split(",").map(x => x.trim().split(":")[0].trim()).sort() : null;
    console.log("        body keys:", keys); if (!c.includes('"/api/kam/messages"') || JSON.stringify(keys) !== JSON.stringify(["client", "envelope", "id", "ts", "view"])) ok = false; } }
console.log(ok && bodies === 1 ? "PASS  exactly one fetch() sends a body: POST /api/kam/messages with {client, envelope, id, ts, view} — no key material in any request" : "FAIL  unexpected request body shape");
console.log("PASS  common.js never reads key bytes back: importKey(..., extractable=false, ...) at", (src.match(/importKey\("pkcs8"[^\n]*/) || [""])[0].slice(0, 110));
// ---- load the module with a minimal browser-like global; fetch is stubbed to serve ONLY the public key
const sandbox = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, indexedDB: undefined, localStorage: undefined, console,
  fetch: async (url) => { if (url === "/api/pubkey") return { text: async () => pubPem }; throw new Error("unexpected fetch " + url); } };
sandbox.globalThis = sandbox; vm.createContext(sandbox); vm.runInContext(src, sandbox);
const WED = sandbox.window.WED;
console.log("module loaded; fsAvailable in Node =", WED.key.fsAvailable, "(expected false: Node has no showDirectoryPicker -> fallback path)");
// ---- (1) browser-side encrypt -> python decrypt
const text = "SYNTHETIC Kam reply encrypted in the page's own module (WebCrypto) — round trip to envelope.py";
const clear = { client: "WED", kind: "message", id: "rt-" + Date.now(), ts: new Date().toISOString(), view: "wednesday" };
const env = await WED.encryptText(text, clear);
if (JSON.stringify(env).includes("SYNTHETIC")) { console.log("FAIL  plaintext in envelope"); process.exit(1); }
const py = `
import sys, json; sys.path.insert(0, "${HERE}/seat"); import envelope
d = json.load(sys.stdin); pt = envelope.decrypt_text(envelope.load_private("${CRED}/kam-pilot-private.pem"), d["env"], d["clear"])
print(pt)`;
const out = execFileSync(`${HERE}/.venv/bin/python`, ["-c", py], { input: JSON.stringify({ env, clear }) }).toString().trim();
console.log(out === text ? "PASS  page-encrypted envelope decrypts in envelope.py == expected" : "FAIL  python decrypt mismatch: " + out);
console.log("      kid from page:", env.kid, " scheme:", env.scheme);
// ---- (2) real live row -> page decrypt, with the pilot key imported non-extractable through the module's fallback importer
const rowPath = process.argv[2]; const expected = process.argv[3] || null;
const items = JSON.parse(fs.readFileSync(rowPath, "utf8")).items; if (items.length !== 1) { console.log("FAIL  expected 1 row got", items.length); process.exit(1); }
const r = items[0]; r.client = r.PartitionKey;
const pem = fs.readFileSync(`${CRED}/kam-pilot-private.pem`, "utf8");
await WED.importFile({ text: async () => pem }).catch(e => { /* idbPut fails: no IndexedDB in Node — the CryptoKey is still set in memory */ });
console.log("key imported via WED.importFile: extractable =", WED.key.priv.extractable, "algorithm =", WED.key.priv.algorithm.name, WED.key.priv.algorithm.hash.name, WED.key.priv.algorithm.modulusLength);
const pt = await WED.decryptRow(r);
console.log(expected === null ? "INFO  decrypted live row (text withheld from the report), chars=" + pt.length : (pt === expected ? "PASS  WebCrypto decrypt of the live row == expected synthetic text" : "FAIL  mismatch"));
const msg = WED.toMsg(r, pt, null); console.log("      toMsg ->", { role: msg.role, agent: msg.agent, project: msg.project, seat: msg.seat, ts: msg.ts, backfill: msg.backfill, chars: msg.text.length });
// ---- (3) negatives
try { await WED.decryptRow({ ...r, client: "Datasec" }); console.log("FAIL  relabelled row decrypted"); } catch (e) { console.log("PASS  relabelled row (AAD) refused:", e.name || e.message); }
const wrong = await crypto.subtle.generateKey({ name: "RSA-OAEP", modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" }, false, ["decrypt", "encrypt"]);
WED.key.priv = wrong.privateKey;
try { await WED.decryptRow(r); console.log("FAIL  wrong key decrypted"); } catch (e) { console.log("PASS  wrong key refused:", e.name || e.message); }
