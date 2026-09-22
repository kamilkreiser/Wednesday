// Phase 3 — run app/static/common.js ITSELF in Node's WebCrypto (same API/parameters as the browser; NOT a browser session):
//   (1) kid computed by the page at import == the seats' kid, for pilot / laptop / ipad
//   (2) a REAL migrated live row (argv[2]) decrypts with EACH device key, kid-selected; a legacy import (kid unknown) finds
//       its entry by trial and remembers the kid; a key outside the ring is refused
//   (3) WED.encryptText (Kam's reply) wraps to the ring + the addressed seat: the WEDNESDAY seat key decrypts a view=wednesday
//       reply in envelope.py, the TUESDAY seat key is refused (KeyError); a view=both (ALL) reply opens with BOTH seat keys
//   (4) static: still exactly one fetch() sends a body — POST /api/kam/messages {client, envelope, id, ts, view}
import fs from "node:fs"; import { execFileSync } from "node:child_process"; import vm from "node:vm";
const HERE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud", CRED = "/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud";
const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8");
const pubkeys = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
let fails = 0; const P = (ok, msg) => { console.log((ok ? "PASS  " : "FAIL  ") + msg); if (!ok) fails++; };
// (4) static
function fetchCalls(code) { const out = []; let i = 0; while ((i = code.indexOf("fetch(", i)) !== -1) { let d = 0, j = i + 5; for (; j < code.length; j++) { if (code[j] === "(") d++; else if (code[j] === ")") { d--; if (d === 0) break; } } out.push(code.slice(i, j + 1)); i = j; } return out; }
const bodies = fetchCalls(src).filter(c => /\bbody\s*:/.test(c));
// 2026-09-22 file drawer: THREE body-sending fetches — the reply (now + attachments ids), POST /api/files (row: envelope + clear), PUT .../blob (ciphertext bytes)
const bReply = bodies.find(b => b.includes('"/api/kam/messages"')), bRow = bodies.find(b => b.includes('"/api/files"')), bBlob = bodies.find(b => /\/blob"/.test(b));
P(bodies.length === 3 && !!bReply && /JSON\.stringify\(\{ client, view, id: clear\.id, ts: clear\.ts, envelope, \.\.\.att \}\)/.test(bReply)
  && !!bRow && /JSON\.stringify\(body\)/.test(bRow) && !!bBlob && /body: enc\.ct/.test(bBlob)
  && !bodies.some(b => /priv|pkcs8|key\.priv/.test(b)), "static: exactly three fetch() calls send a body — POST /api/kam/messages {client, view, id, ts, envelope, ...att}, POST /api/files (row), PUT /api/files/../blob (ciphertext bytes); no key material in any request");
P(/importKey\("pkcs8", der, \{ name: "RSA-OAEP", hash: "SHA-256" \}, false, \["decrypt"\]\)/.test(src), "static: the kept private CryptoKey is imported extractable=false (the extractable copy exists only inside kidOfPkcs8 for n/e)");
// sandbox
const store = new Map();
const sandbox = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, console, localStorage: undefined,
  indexedDB: { open: () => { const r = {}; setTimeout(() => { r.result = { transaction: () => ({ objectStore: () => ({ put: (v, k) => store.set(k, v), get: (k) => { const g = {}; setTimeout(() => { g.result = store.get(k); g.onsuccess && g.onsuccess(); }, 0); return g; }, delete: (k) => store.delete(k) }), set oncomplete(f) { setTimeout(f, 0); }, set onerror(f) {} }) }; r.onsuccess && r.onsuccess(); }, 0); return r; } },
  fetch: async (url) => { if (url === "/api/pubkeys") return { ok: true, status: 200, json: async () => pubkeys }; throw new Error("unexpected fetch " + url); } };
sandbox.globalThis = sandbox; vm.createContext(sandbox); vm.runInContext(src, sandbox); const WED = sandbox.window.WED;
const expectedKid = Object.fromEntries(pubkeys.kam.map(k => [k.name, k.kid]));
// (1) kid at import
for (const dev of ["pilot", "laptop", "ipad"]) {
  await WED.forget(); await WED.importFile({ name: `kam-${dev}-private.pem`, text: async () => fs.readFileSync(`${CRED}/kam-${dev}-private.pem`, "utf8") });
  P(WED.key.kid === expectedKid[dev] && WED.key.priv.extractable === false, `kid computed by the page for kam-${dev} = ${WED.key.kid} == seats' kid ${expectedKid[dev]}; CryptoKey extractable=false`);
}
// (2) migrated row
const r = JSON.parse(fs.readFileSync(process.argv[2], "utf8")).items[0]; r.client = r.PartitionKey; const expected = process.argv[4];
const texts = {};
for (const dev of ["pilot", "laptop", "ipad"]) {
  await WED.forget(); await WED.importFile({ name: `kam-${dev}-private.pem`, text: async () => fs.readFileSync(`${CRED}/kam-${dev}-private.pem`, "utf8") });
  texts[dev] = await WED.decryptRow(r);
  P(texts[dev] === expected, `migrated live row ${r.RowKey} decrypts with the ${dev} key (kid-selected) == expected synthetic text`);
}
WED.key.kid = null; const legacy = await WED.decryptRow(r);           // ipad key held, kid unknown -> trial
P(legacy === expected && WED.key.kid === expectedKid.ipad, `legacy import (kid unknown) found its entry by trial and remembered kid ${WED.key.kid}`);
const outsider = await crypto.subtle.generateKey({ name: "RSA-OAEP", modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" }, false, ["decrypt", "encrypt"]);
WED.key.priv = outsider.privateKey; WED.key.kid = "0000000000000000";
try { await WED.decryptRow(r); P(false, "outsider key decrypted"); } catch (e) { P(/not wrapped to this key/.test(e.message), "a key outside the ring is refused: " + e.message.slice(0, 60)); }
WED.key.kid = null; try { await WED.decryptRow(r); P(false, "outsider key (trial) decrypted"); } catch (e) { P(/no wrapped entry/.test(e.message), "outsider key by trial refused: " + e.message); }
try { await WED.decryptRow({ ...r, client: "Datasec" }); } catch (e) {}
await WED.forget(); await WED.importFile({ name: "kam-pilot-private.pem", text: async () => fs.readFileSync(`${CRED}/kam-pilot-private.pem`, "utf8") });
try { await WED.decryptRow({ ...r, client: "Datasec" }); P(false, "relabelled row decrypted"); } catch (e) { P(e.name === "OperationError", "relabelled row (AAD) refused: " + e.name); }
// (3) Kam's reply path
const py = (env, clear, keyfile) => execFileSync(`${HERE}/.venv/bin/python`, ["-c", `
import sys, json; sys.path.insert(0, "${HERE}/seat"); import envelope
d = json.load(sys.stdin)
try: print("OK " + envelope.decrypt_text(envelope.load_private("${CRED}/${keyfile}"), d["env"], d["clear"]))
except KeyError as e: print("KEYERROR " + str(e)[:80])
`], { input: JSON.stringify({ env, clear }) }).toString().trim();
const text = "SYNTHETIC Kam reply (Phase 3) wrapped in the page to the ring + the addressed seat";
for (const [view, client, yes, no] of [["wednesday", "WED", ["wednesday-seat.pem", "kam-laptop-private.pem", "kam-ipad-private.pem", "kam-pilot-private.pem"], ["tuesday-seat.pem"]],
                                       ["tuesday", "Datasec", ["tuesday-seat.pem", "kam-pilot-private.pem"], ["wednesday-seat.pem"]],
                                       ["both", "ALL", ["wednesday-seat.pem", "tuesday-seat.pem", "kam-laptop-private.pem"], []]]) {
  const clear = { client, kind: "message", id: "p3-" + view + "-" + Date.now(), ts: new Date().toISOString(), view };
  const env = await WED.encryptText(text, clear);
  P(!JSON.stringify(env).includes("SYNTHETIC"), `view=${view}: plaintext absent from the envelope`);
  const kids = env.wrapped_keys.map(e => e.kid);
  const want = [...pubkeys.kam.map(k => k.kid), ...pubkeys.seat_of_client[client].map(s => pubkeys.seats[s].kid)];
  P(JSON.stringify(kids) === JSON.stringify(want) && env.kid === kids[0] && env.wrapped_key === env.wrapped_keys[0].wrapped_key, `view=${view} -> ${client}: wrapped_keys kids = ${kids.join(",")} (ring + ${pubkeys.seat_of_client[client].join("+")}); top-level pair = pilot entry`);
  for (const k of yes) { const out = py(env, clear, k); P(out === "OK " + text, `view=${view}: ${k} decrypts the page-made reply in envelope.py`); }
  for (const k of no) { const out = py(env, clear, k); P(out.startsWith("KEYERROR"), `view=${view}: ${k} is REFUSED (${out.slice(0, 40)}…)`); }
}
console.log(fails === 0 ? "### RESULT: ALL PHASE 3 WEBCRYPTO CHECKS PASS (Node WebCrypto on the page's own module — not a browser)" : `### RESULT: ${fails} FAILED`);
process.exit(fails ? 1 : 0);
