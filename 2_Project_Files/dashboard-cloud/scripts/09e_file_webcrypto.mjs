// 2026-09-22 file drawer — the page's OWN common.js file path in Node WebCrypto (not a browser) against seat/envelope.py:
//   (1) page encryptFile (as Kam's pilot key holder, view=wednesday -> WED) -> the WEDNESDAY seat's key decrypts meta + bytes in
//       envelope.py (sha256 equal); the TUESDAY seat key is refused (KeyError); the pilot key opens it too
//   (2) seat encrypt_file (envelope.py, WED) -> the page's decryptFileMeta + decryptFileBytes with the pilot key (sha256 equal);
//       a relabelled row (other id) is refused by the page
// usage: node 09e_file_webcrypto.mjs <pubkeys.json> <scratch dir>
import fs from "node:fs"; import { execFileSync } from "node:child_process"; import vm from "node:vm"; import crypto from "node:crypto";
const HERE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud", CRED = "/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud", V = `${HERE}/.venv/bin/python`;
const pubkeys = JSON.parse(fs.readFileSync(process.argv[2], "utf8")), SCR = process.argv[3];
let fails = 0; const P = (ok, msg) => { console.log((ok ? "PASS  " : "FAIL  ") + msg); if (!ok) fails++; };
const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8"); const store = new Map();
const sandbox = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, console, localStorage: undefined,
  indexedDB: { open: () => { const r = {}; setTimeout(() => { r.result = { transaction: () => ({ objectStore: () => ({ put: (v, k) => store.set(k, v), get: (k) => { const g = {}; setTimeout(() => { g.result = store.get(k); g.onsuccess && g.onsuccess(); }, 0); return g; }, delete: (k) => store.delete(k) }), set oncomplete(f) { setTimeout(f, 0); }, set onerror(f) {} }) }; r.onsuccess && r.onsuccess(); }, 0); return r; } },
  fetch: async (url) => { if (url === "/api/pubkeys") return { ok: true, status: 200, json: async () => pubkeys }; throw new Error("unexpected fetch " + url); } };
sandbox.globalThis = sandbox; vm.createContext(sandbox); vm.runInContext(src, sandbox); const WED = sandbox.window.WED;
await WED.importFile({ name: "kam-pilot-private.pem", text: async () => fs.readFileSync(`${CRED}/kam-pilot-private.pem`, "utf8") });
const sha = b => crypto.createHash("sha256").update(Buffer.from(b)).digest("hex");
// (1) page -> seat
const bytes = crypto.randomBytes(100000); const clear = { client: "WED", kind: "file", id: "f-09e-" + Date.now().toString(36), ts: new Date().toISOString() };
const meta = { name: "synthetic-09e.bin", note: "page->seat", size: bytes.length, sha256: sha(bytes), mime: "application/octet-stream" };
const enc = await WED.encryptFile(bytes, meta, clear);
const row = { ...clear, ...enc.envelope, iv_blob: enc.iv_blob };
fs.writeFileSync(`${SCR}/09e_row.json`, JSON.stringify(row)); fs.writeFileSync(`${SCR}/09e_ct.bin`, Buffer.from(enc.ct));
P(enc.ct.length === bytes.length + 16 && !JSON.stringify(row).includes("synthetic-09e") && enc.envelope.wrapped_keys.length === 4, `page encryptFile: ct = plaintext + 16, 4 wrapped keys, name absent from the row`);
const py = (code, ...args) => execFileSync(V, ["-c", code, ...args], { encoding: "utf8" }).trim();
const PYD = `import sys,json,hashlib; sys.path.insert(0,"${HERE}/seat"); import envelope
row=json.load(open(sys.argv[1])); ct=open(sys.argv[2],"rb").read(); clear={k:row[k] for k in ("client","kind","id","ts")}
try:
    priv=envelope.load_private(sys.argv[3]); m=json.loads(envelope.decrypt_text(priv,row,clear)); pt=envelope.decrypt_file(priv,row,clear,ct)
    print("OK", m["name"], hashlib.sha256(pt).hexdigest(), m["sha256"])
except KeyError as e: print("KEYERROR")
except Exception as e: print("ERR", type(e).__name__)`;
for (const k of ["wednesday-seat.pem", "kam-pilot-private.pem", "kam-laptop-private.pem"]) {
  const out = py(PYD, `${SCR}/09e_row.json`, `${SCR}/09e_ct.bin`, `${CRED}/${k}`).split(" ");
  P(out[0] === "OK" && out[1] === "synthetic-09e.bin" && out[2] === sha(bytes) && out[3] === sha(bytes), `${k} opens the page-encrypted file in envelope.py: meta name + bytes sha256 == ${sha(bytes).slice(0, 12)}…`);
}
P(py(PYD, `${SCR}/09e_row.json`, `${SCR}/09e_ct.bin`, `${CRED}/tuesday-seat.pem`) === "KEYERROR", "tuesday-seat.pem REFUSED on a WED file (KeyError: not a recipient)");
// (2) seat -> page
const PYE = `import sys,json,os,hashlib; sys.path.insert(0,"${HERE}/seat"); import envelope
data=os.urandom(65537); clear={"client":"WED","kind":"file","id":"f-09e-seat","ts":"2026-09-22T00:00:00.000Z"}
env,ct=envelope.encrypt_file(data,{"name":"seat-09e.bin","note":"seat->page","size":len(data),"sha256":hashlib.sha256(data).hexdigest(),"mime":"application/octet-stream"},clear)
json.dump({**clear,**env},open(sys.argv[1],"w")); open(sys.argv[2],"wb").write(ct); print(hashlib.sha256(data).hexdigest())`;
const want = py(PYE, `${SCR}/09e_row2.json`, `${SCR}/09e_ct2.bin`);
const row2 = JSON.parse(fs.readFileSync(`${SCR}/09e_row2.json`, "utf8")); const ct2 = fs.readFileSync(`${SCR}/09e_ct2.bin`);
const m2 = await WED.decryptFileMeta(row2); const pt2 = await WED.decryptFileBytes(row2, ct2);
P(m2 && m2.name === "seat-09e.bin" && sha(pt2) === want && sha(pt2) === m2.sha256, `page decryptFileMeta + decryptFileBytes (pilot key) open the seat-encrypted file: name + sha256 == ${want.slice(0, 12)}…`);
let refused = false; try { await WED.decryptFileBytes({ ...row2, id: "f-other" }, ct2); } catch (e) { refused = true; }
P(refused, "page refuses the blob under a relabelled row (AAD client|fileblob|id|ts)");
console.log(fails ? `### RESULT: ${fails} FAILED` : "### RESULT: ALL FILE WEBCRYPTO CHECKS PASS (page module in Node WebCrypto <-> envelope.py; not a browser)");
process.exit(fails ? 1 : 0);
