/* common.js — shared by / (cockpit mirror) and /chat (chat mirror). Phase 2, 2026-09-21.

   THREE THINGS LIVE HERE, AND NOTHING ELSE:
   1. KEY ACCESS (Kam, 11:45:52: "Rather than loading the certificate, can it check for it in a specific local C or
      Mac drive? Allow the user to define where it is stored.")
        Chrome/Edge: File System Access API. Kam picks the FOLDER that holds the key ONCE; the directory handle is
        remembered in this browser's IndexedDB; every visit the page asks the folder for read permission (one click —
        or none, when Chrome was told "allow on every visit") and reads <filename> (default kam-pilot-private.pem, user-
        settable) from it, importing it as a NON-EXTRACTABLE WebCrypto key held in memory only. The PEM is never stored
        by the page and never leaves the machine: there is no network call in this module that carries key material,
        and the server has no key route (see REPORT_2026-09-21_phase2.md, piece B).
        Safari / iOS / Firefox (no showDirectoryPicker): the Phase 1 import-once flow — a file picker, imported non-
        extractable and kept in IndexedDB for this browser, "Forget key" removes it.
   2. THE ENVELOPE, both directions (mirror of seat/envelope.py): decrypt rows written by the seats; ENCRYPT Kam's own
      replies to his public key before POST /api/kam/messages, so the server never sees his prose either.
   3. ROW -> LOCAL MESSAGE SHAPE, so the two pages can keep the local cockpit.html / chat.html render code unchanged.

   PHASE 3 (2026-09-21, D-2(b); Kam 12:50 "a new key for my laptop and one for my iPad"): a row's data key is wrapped to
   EVERY recipient — Kam's key ring (pilot, laptop, ipad: any of his devices reads any row) and the ADDRESSED SEAT's
   certificate public key (so the seat can read what Kam typed). `wrapped_keys: [{kid, wrapped_key}, …]`; the top-level
   kid/wrapped_key pair (= the pilot entry) stays for one release. This module therefore (a) computes the KID of the private
   key it holds at import (sha256(SPKI)[:16], the same function the seats use) and SELECTS its wrapped entry by kid — with a
   trial-decrypt fallback for a key imported before Phase 3 whose kid was not recorded (the matching kid is then remembered);
   (b) wraps Kam's replies to the whole ring + the addressed seat(s) from GET /api/pubkeys; (c) when reading the key from
   the chosen folder, tries the configured filename first and then every known device filename.

   FILE DRAWER (2026-09-22, Kam 15:26 / 15:31): files are records too — item 2 covers them. ONE data key per file, used twice:
   over the meta JSON {name, note, size, sha256, mime} as the row's ciphertext (AAD client|file|id|ts — decryptRow opens it)
   and over the bytes as the blob (AAD client|fileblob|id|ts, its own iv_blob). Wrapped to the ring + the addressed seat(s)
   exactly like a reply, so the seat can read what Kam attached. encryptFile / decryptFileMeta / decryptFileBytes here;
   the drawer's DOM lives in drawer.js. The server stores bytes it cannot read; downloads are decrypted here before saving. */
"use strict";
window.WED = (function () {
  const SCHEME = "rsa-oaep-sha256+aes-256-gcm/v1";
  const DB = "wedpanel", STORE = "keys", K_CRYPTOKEY = "kam-pilot", K_DIR = "keydir", K_KID = "kam-kid";
  const LS_FILENAME = "wed_key_filename", DEFAULT_FILENAME = "kam-pilot-private.pem";
  const KNOWN_FILENAMES = ["kam-pilot-private.pem", "kam-laptop-private.pem", "kam-ipad-private.pem"];
  const VIEW_TO_CLIENT = { wednesday: "WED", tuesday: "Datasec", both: "ALL" };

  // ---- IndexedDB (per browser; the ONLY persistence this module has) ----
  function idb() { return new Promise((res, rej) => { const r = indexedDB.open(DB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore(STORE); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }); }
  async function idbPut(k, v) { const d = await idb(); return new Promise((res, rej) => { const t = d.transaction(STORE, "readwrite");
    t.objectStore(STORE).put(v, k); t.oncomplete = res; t.onerror = () => rej(t.error); }); }
  async function idbGet(k) { const d = await idb(); return new Promise((res, rej) => { const t = d.transaction(STORE, "readonly");
    const g = t.objectStore(STORE).get(k); g.onsuccess = () => res(g.result === undefined ? null : g.result); g.onerror = () => rej(g.error); }); }
  async function idbDel(k) { const d = await idb(); return new Promise((res, rej) => { const t = d.transaction(STORE, "readwrite");
    t.objectStore(STORE).delete(k); t.oncomplete = res; t.onerror = () => rej(t.error); }); }

  // ---- bytes ----
  function pemToDer(pem) { const b = pem.replace(/-----[^-]+-----/g, "").replace(/\s+/g, ""); const s = atob(b);
    const u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return u.buffer; }
  const unb64 = s => { const b = atob(s); const u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; };
  const b64 = u => { let s = ""; const a = new Uint8Array(u); for (let i = 0; i < a.length; i++) s += String.fromCharCode(a[i]); return btoa(s); };
  const AAD = r => new TextEncoder().encode([r.client, r.kind, r.id, r.ts].map(x => x == null ? "" : String(x)).join("|"));
  async function sha256hex(buf) { const h = await crypto.subtle.digest("SHA-256", buf); return [...new Uint8Array(h)].map(x => x.toString(16).padStart(2, "0")).join(""); }
  // ---- kid of a PKCS8 private key: build the SPKI DER from the key's public (n, e) and hash it — same kid as the seats ----
  const unb64url = s => unb64(s.replace(/-/g, "+").replace(/_/g, "/") + "=".repeat((4 - s.length % 4) % 4));
  function derLen(n) { if (n < 128) return [n]; const b = []; while (n) { b.unshift(n & 255); n >>= 8; } return [0x80 | b.length, ...b]; }
  function derInt(u) { let a = [...u]; while (a.length > 1 && a[0] === 0) a.shift(); if (a[0] & 0x80) a.unshift(0); return [0x02, ...derLen(a.length), ...a]; }
  function derSeq(body) { return [0x30, ...derLen(body.length), ...body]; }
  function spkiFromJwk(jwk) {
    const rsaPub = derSeq([...derInt(unb64url(jwk.n)), ...derInt(unb64url(jwk.e))]);
    const algId = [0x30, 0x0d, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86, 0xf7, 0x0d, 0x01, 0x01, 0x01, 0x05, 0x00];
    const bitStr = [0x03, ...derLen(rsaPub.length + 1), 0x00, ...rsaPub];
    return new Uint8Array(derSeq([...algId, ...bitStr]));
  }
  async function kidOfPkcs8(der) {
    // an EXTRACTABLE import is used ONLY to read n/e for the kid; it is dropped at once — the key kept/persisted is non-extractable
    const tmp = await crypto.subtle.importKey("pkcs8", der, { name: "RSA-OAEP", hash: "SHA-256" }, true, ["decrypt"]);
    const jwk = await crypto.subtle.exportKey("jwk", tmp);
    return (await sha256hex(spkiFromJwk(jwk))).slice(0, 16);
  }

  // ---- key state ----
  const key = { priv: null, kid: null, source: null, dirName: null, fileName: null, needsClick: false, fsAvailable: typeof window.showDirectoryPicker === "function" };
  function filename() { try { return localStorage.getItem(LS_FILENAME) || DEFAULT_FILENAME; } catch (e) { return DEFAULT_FILENAME; } }
  function setFilename(n) { try { localStorage.setItem(LS_FILENAME, (n || "").trim() || DEFAULT_FILENAME); } catch (e) {} }
  async function importPem(text) {
    if (!/BEGIN PRIVATE KEY/.test(text)) throw new Error('need a PKCS8 "BEGIN PRIVATE KEY" PEM');
    const der = pemToDer(text);
    key.kid = await kidOfPkcs8(der);
    // extractable=false: even this page cannot read the key material back out of the CryptoKey
    return crypto.subtle.importKey("pkcs8", der, { name: "RSA-OAEP", hash: "SHA-256" }, false, ["decrypt"]);
  }
  async function readFromFolder(handle, interactive) {
    let perm = await handle.queryPermission({ mode: "read" });
    if (perm !== "granted") {
      if (!interactive) { key.needsClick = true; key.dirName = handle.name; return false; }
      perm = await handle.requestPermission({ mode: "read" });      // the ONE click, inside a user gesture
      if (perm !== "granted") throw new Error("read permission for folder “" + handle.name + "” was not granted");
    }
    // the configured filename first, then every known device filename (Phase 3: a laptop folder holds kam-laptop-private.pem)
    let fh = null, used = null;
    for (const n of [filename(), ...KNOWN_FILENAMES.filter(x => x !== filename())]) {
      try { fh = await handle.getFileHandle(n); used = n; break; } catch (e) { if (e.name !== "NotFoundError") throw e; }
    }
    if (!fh) throw new Error("no key file in folder “" + handle.name + "” (looked for " + [filename(), ...KNOWN_FILENAMES].filter((x, i, a) => a.indexOf(x) === i).join(", ") + ")");
    const text = await (await fh.getFile()).text();
    key.priv = await importPem(text); key.source = "folder"; key.dirName = handle.name; key.fileName = used; key.needsClick = false;
    return true;
  }
  /* Chrome/Edge: pick the folder ONCE (a user gesture is required). Remembered per browser. */
  async function chooseFolder() {
    if (!key.fsAvailable) throw new Error("this browser has no File System Access API — use Import key");
    const handle = await window.showDirectoryPicker({ id: "wed-key-folder", mode: "read" });
    await idbPut(K_DIR, handle);
    await idbDel(K_CRYPTOKEY);                                        // a folder source supersedes an imported copy
    return readFromFolder(handle, true);
  }
  /* Every visit: try the remembered folder silently; if Chrome wants a click, say so (key.needsClick). */
  async function unlock(interactive) {
    if (key.fsAvailable) {
      const handle = await idbGet(K_DIR);
      if (handle) { try { return await readFromFolder(handle, !!interactive); }
        catch (e) { if (interactive) throw e; key.needsClick = true; key.dirName = handle.name; return false; } }
    }
    const ck = await idbGet(K_CRYPTOKEY);                              // fallback browsers: the imported copy
    if (ck) { key.priv = ck; key.kid = await idbGet(K_KID); key.source = "imported"; return true; }   // kid null = pre-Phase-3 import -> trial decrypt
    return false;
  }
  /* Fallback (Safari/iOS/Firefox, or by choice): import the file once; kept in IndexedDB for this browser only. */
  async function importFile(file) {
    key.priv = await importPem(await file.text()); key.source = "imported"; key.dirName = null; key.fileName = file.name || null; key.needsClick = false;
    await idbPut(K_CRYPTOKEY, key.priv); await idbPut(K_KID, key.kid);
  }
  async function forget() { await idbDel(K_CRYPTOKEY); await idbDel(K_KID); await idbDel(K_DIR); key.priv = null; key.kid = null; key.source = null; key.dirName = null; key.fileName = null; key.needsClick = false; }
  async function rememberedFolderName() { if (!key.fsAvailable) return null; const h = await idbGet(K_DIR); return h ? h.name : null; }

  // ---- envelope: decrypt (rows from the seats and from Kam himself) ----
  function wrappedEntries(r) {
    let wk = r.wrapped_keys; if (typeof wk === "string") { try { wk = JSON.parse(wk); } catch (e) { wk = null; } }
    const out = Array.isArray(wk) ? wk.filter(e => e && e.kid && e.wrapped_key) : [];
    if (r.kid && r.wrapped_key && !out.some(e => e.kid === r.kid)) out.push({ kid: r.kid, wrapped_key: r.wrapped_key });   // legacy top-level pair
    return out;
  }
  /* Unwrap the data key with the held private key: SELECT BY KID; if this key's kid is unknown (imported before Phase 3) try
     each entry once and remember the kid that worked. A row with no entry for this key throws "not wrapped to this key". */
  async function unwrapDataKey(r) {
    const entries = wrappedEntries(r);
    if (key.kid) {
      const e = entries.find(x => x.kid === key.kid);
      if (!e) throw new Error("row is not wrapped to this key (kid " + key.kid + "; row has " + entries.map(x => x.kid).join(",") + ")");
      return crypto.subtle.decrypt({ name: "RSA-OAEP" }, key.priv, unb64(e.wrapped_key));
    }
    for (const e of entries) {
      try { const dk = await crypto.subtle.decrypt({ name: "RSA-OAEP" }, key.priv, unb64(e.wrapped_key)); key.kid = e.kid; try { await idbPut(K_KID, e.kid); } catch (x) {} return dk; } catch (x) {}
    }
    throw new Error("no wrapped entry opens with this key");
  }
  async function decryptRow(r) {
    if (!key.priv) return null;
    if (r.scheme !== SCHEME) throw new Error("scheme " + r.scheme);
    const dk = await unwrapDataKey(r);
    const k = await crypto.subtle.importKey("raw", dk, { name: "AES-GCM" }, false, ["decrypt"]);
    const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv: unb64(r.iv), additionalData: AAD(r) }, k, unb64(r.ciphertext));
    return new TextDecoder().decode(pt);
  }
  // ---- envelope: encrypt (Kam's replies: to his whole key ring AND the addressed seat(s); the server never sees the text) ----
  let pubCache = null;
  async function importSpki(pem) { const der = pemToDer(pem);
    return { key: await crypto.subtle.importKey("spki", der, { name: "RSA-OAEP", hash: "SHA-256" }, false, ["encrypt"]), kid: (await sha256hex(der)).slice(0, 16) }; }
  /* GET /api/pubkeys -> { kam: [{name,kid,pem}…] (pilot first), seats: {wednesday:{kid,pem}, tuesday:{kid,pem}}, seat_of_client } */
  async function publicKeys() {
    if (pubCache) return pubCache;
    const r = await fetch("/api/pubkeys", { cache: "no-store" });
    if (!r.ok) throw new Error("public keys unavailable (HTTP " + r.status + ")");
    const j = await r.json();
    const kam = []; for (const k of j.kam || []) { const ik = await importSpki(k.pem); if (ik.kid !== k.kid) throw new Error("kid mismatch for " + k.name); kam.push({ name: k.name, ...ik }); }
    const seats = {}; for (const s of Object.keys(j.seats || {})) { const ik = await importSpki(j.seats[s].pem); if (ik.kid !== j.seats[s].kid) throw new Error("kid mismatch for seat " + s); seats[s] = ik; }
    if (!kam.length) throw new Error("no Kam public key");
    pubCache = { kam, seats, seatOfClient: j.seat_of_client || { WED: ["wednesday"], Secuura: ["wednesday"], Datasec: ["tuesday"], ALL: ["wednesday", "tuesday"] } };
    return pubCache;
  }
  function keyNameOfKid(kid) { if (!pubCache || !kid) return null; const k = pubCache.kam.find(x => x.kid === kid); return k ? k.name : null; }
  /* the data key wrapped to the ring + the addressed seat(s) of `client` — shared by replies and files */
  async function wrapTo(client, dk) {
    const pk = await publicKeys();
    const recipients = [...pk.kam, ...(pk.seatOfClient[client] || []).map(s => pk.seats[s]).filter(Boolean)];
    const wrapped_keys = [];
    for (const rk of recipients) { if (wrapped_keys.some(e => e.kid === rk.kid)) continue;
      wrapped_keys.push({ kid: rk.kid, wrapped_key: b64(await crypto.subtle.encrypt({ name: "RSA-OAEP" }, rk.key, dk)) }); }
    return wrapped_keys;
  }
  async function encryptText(text, clear) {
    const dk = crypto.getRandomValues(new Uint8Array(32)), iv = crypto.getRandomValues(new Uint8Array(12));
    const ak = await crypto.subtle.importKey("raw", dk, { name: "AES-GCM" }, false, ["encrypt"]);
    const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv, additionalData: AAD(clear) }, ak, new TextEncoder().encode(text));
    const wrapped_keys = await wrapTo(clear.client, dk);
    // top-level pair = the first ring entry (pilot), kept for one release
    return { scheme: SCHEME, kid: wrapped_keys[0].kid, iv: b64(iv), wrapped_key: wrapped_keys[0].wrapped_key, ciphertext: b64(ct), wrapped_keys };
  }
  // ---- files (2026-09-22): one data key -> meta row + blob; both directions ----
  const FILE_MAX = 32 * 1024 * 1024;            // ciphertext bound (mirrors app/main.py FILE_MAX); plaintext up to FILE_MAX - 16
  const BLOB_AAD = r => new TextEncoder().encode([r.client, "fileblob", r.id, r.ts].map(x => x == null ? "" : String(x)).join("|"));
  async function encryptFile(bytes, meta, clear) {
    const dk = crypto.getRandomValues(new Uint8Array(32)), ivM = crypto.getRandomValues(new Uint8Array(12)), ivB = crypto.getRandomValues(new Uint8Array(12));
    const ak = await crypto.subtle.importKey("raw", dk, { name: "AES-GCM" }, false, ["encrypt"]);
    const ctM = await crypto.subtle.encrypt({ name: "AES-GCM", iv: ivM, additionalData: AAD(clear) }, ak, new TextEncoder().encode(JSON.stringify(meta)));
    const ctB = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv: ivB, additionalData: BLOB_AAD(clear) }, ak, bytes));
    const wrapped_keys = await wrapTo(clear.client, dk);
    return { envelope: { scheme: SCHEME, kid: wrapped_keys[0].kid, iv: b64(ivM), wrapped_key: wrapped_keys[0].wrapped_key, ciphertext: b64(ctM), wrapped_keys }, iv_blob: b64(ivB), ct: ctB };
  }
  async function decryptFileMeta(r) { const pt = await decryptRow(r); if (pt === null) return null; try { return JSON.parse(pt); } catch (e) { return { name: "(meta is not JSON)" }; } }
  async function decryptFileBytes(r, ct) {
    if (!key.priv) throw new Error("no key");
    const dk = await unwrapDataKey(r);
    const k = await crypto.subtle.importKey("raw", dk, { name: "AES-GCM" }, false, ["decrypt"]);
    return crypto.subtle.decrypt({ name: "AES-GCM", iv: unb64(r.iv_blob), additionalData: BLOB_AAD(r) }, k, ct);
  }
  async function listFiles(since) { const d = await getJSON("/api/files?limit=1000" + (since ? "&since=" + encodeURIComponent(since) : "")); return d.files || []; }
  async function fetchFileBytes(r) {
    const resp = await fetch("/api/files/" + encodeURIComponent(r.client) + "/" + encodeURIComponent(r.row_key) + "/blob", { cache: "no-store" });
    if (resp.status === 401 || resp.redirected) throw new Error("session expired — reload to sign in");
    if (!resp.ok) throw new Error("download failed (HTTP " + resp.status + ")");
    return resp.arrayBuffer();
  }
  /* Kam attaches a file on a tab: encrypted HERE (meta + bytes, one data key wrapped to ring + seat), POST the row, PUT the bytes. */
  async function uploadKamFile(file, view, msgId, note) {
    const client = VIEW_TO_CLIENT[view]; if (!client) throw new Error("view " + view);
    if (file.size + 16 > FILE_MAX) throw new Error(file.name + " is larger than the " + Math.floor(FILE_MAX / 1048576) + " MiB bound");
    if (file.size === 0) throw new Error(file.name + " is empty");
    const bytes = await file.arrayBuffer();
    const clear = { client, kind: "file", id: "f-" + newId().slice(4), ts: utcNow() };
    const meta = { name: file.name, note: note || "", size: file.size, sha256: await sha256hex(bytes), mime: file.type || "application/octet-stream" };
    const enc = await encryptFile(bytes, meta, clear);
    const body = { ...clear, view, size: enc.ct.length, sha256: await sha256hex(enc.ct), iv_blob: enc.iv_blob, envelope: enc.envelope, ...(msgId ? { msg_id: msgId } : {}) };
    let r = await fetch("/api/files", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    if (r.status === 401 || r.redirected) throw new Error("session expired — reload to sign in");
    let j = await r.json().catch(() => ({}));
    if (r.status === 400 && /wrapped to the addressed seat/i.test(String(j && j.detail))) { pubCache = null; return uploadKamFile(file, view, msgId, note); }
    if (!r.ok) throw new Error((j && j.detail) || ("HTTP " + r.status));
    const rk = j.stored.row_key;
    r = await fetch("/api/files/" + encodeURIComponent(client) + "/" + encodeURIComponent(rk) + "/blob", { method: "PUT", headers: { "Content-Type": "application/octet-stream" }, body: enc.ct });
    j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error("bytes refused: " + ((j && j.detail) || ("HTTP " + r.status)));
    return { id: clear.id, row_key: rk, client, name: file.name, size: file.size };
  }
  function utcNow() { return new Date().toISOString(); }               // 2026-09-21T01:23:45.678Z — the API's ts format
  function newId() { const u = crypto.getRandomValues(new Uint8Array(6)); return "kam-" + [...u].map(x => x.toString(16).padStart(2, "0")).join(""); }
  /* Kam types on a tab -> view -> partition. Encrypted here; POSTed as an envelope; refused by the server if it carries text. */
  async function postKamMessage(text, view, _retried, opts) {
    const client = VIEW_TO_CLIENT[view]; if (!client) throw new Error("view " + view);
    opts = opts || {};
    const clear = { client, kind: "message", id: opts.id || newId(), ts: utcNow(), view };
    const envelope = await encryptText(text, clear);
    const att = Array.isArray(opts.attachments) && opts.attachments.length ? { attachments: opts.attachments } : {};   // 2026-09-22: file ids (clear)
    const r = await fetch("/api/kam/messages", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ client, view, id: clear.id, ts: clear.ts, envelope, ...att }) });
    if (r.status === 401 || r.redirected) throw new Error("session expired — reload to sign in");
    const j = await r.json().catch(() => ({}));
    if (!r.ok) {
      const detail = (j && j.detail) || ("HTTP " + r.status);
      // 2026-09-21 17:5x (Kam's screenshot, Tuesday tab): the server refused a reply not wrapped to the addressed seat's
      // key — the page's key ring was older than the server's (a tab open across a deploy, or a seat key added since the
      // page loaded). The ring is a cache; on THIS refusal drop it, refetch /api/pubkeys, re-encrypt and retry ONCE.
      if (r.status === 400 && /wrapped to the addressed seat/i.test(String(detail)) && !_retried) {
        pubCache = null;
        return postKamMessage(text, view, true, opts);
      }
      throw new Error(detail);
    }
    return j;
  }

  // ---- API reads ----
  async function getJSON(url) {
    const r = await fetch(url, { cache: "no-store" });
    if (r.status === 401 || r.status === 302 || r.redirected) throw new Error("session expired — reload to sign in");
    if (!r.ok) throw new Error("HTTP " + r.status + " " + url);
    return r.json();
  }

  // ---- row -> the shape the local pages render ----
  function agentOfRow(r) {
    if (r.role === "kam") return (r.view === "wednesday" || r.view === "tuesday") ? r.view : "both";
    if (r.seat === "tuesday" || r.client === "Datasec") return "tuesday";
    return "wednesday";
  }
  function localTs(utc) { const d = new Date(utc); if (isNaN(d)) return String(utc || "");
    const p = n => String(n).padStart(2, "0");
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate()) + "T" + p(d.getHours()) + ":" + p(d.getMinutes()) + ":" + p(d.getSeconds()); }
  /* pt === null -> locked (no key); pt === undefined -> decrypt failed (error in .error) */
  function toMsg(r, pt, err) {
    return { role: r.role === "kam" ? "kam" : "wednesday", agent: agentOfRow(r), project: r.client === "ALL" ? "WED" : r.client,
      seat: r.seat, view: r.view, ts: localTs(r.ts), utc: r.ts, row_key: r.row_key, id: r.id,
      text: pt == null ? "" : pt, locked: pt === null, error: err || null, backfill: !!r.backfill, kind: r.kind,
      attachments: Array.isArray(r.attachments) ? r.attachments : [] };   // 2026-09-22: file ids on the row (the drawer names them)
  }
  function toCard(r, pt) {
    let prose = {}; try { prose = pt ? JSON.parse(pt) : {}; } catch (e) { prose = { title: "(card prose is not JSON)", bluf: "" }; }
    const keys = Array.isArray(r.option_keys) ? r.option_keys : [];
    const options = Array.isArray(prose.options) && prose.options.length ? prose.options
      : keys.map(k => ({ key: k, label: pt === null ? "🔒 " + k : k, detail: "" }));   // locked: keys only (they are clear)
    return { id: r.id, client_project: r.client_project || r.client, title: pt === null ? "🔒 encrypted — unlock the key to read" : (prose.title || "(untitled)"),
      bluf: prose.bluf || "", default_action: prose.default_action || "", options, recommended: r.recommended || "",
      status: r.status, ruled_choice: r.ruled_choice || null, ts: r.ts, ruled_ts: r.ruled_ts || "", locked: pt === null,
      ruling_note: prose.ruling_note || "", withdrawn_reason: prose.withdrawn_reason || "", delivered_artefact: prose.delivered_artefact || "" };
  }

  // ---- synthetic rows (Phase 3, Kam 12:48 "a lot of secure synthetic cards"): probe/test rows carry synthetic=true and are
  //      HIDDEN by both pages (never deleted; the seats still read them). hidden{} counts what each page skipped, for its footer.
  const hidden = { messages: 0, cards: 0 };
  function isSynthetic(r) { return !!(r && r.synthetic === true); }
  // ---- hidden rows (2026-09-22, Kam 14:27 "clean up your boards"): a seat may HIDE a row of its own tab (POST /api/seat/hide,
  //      reversible, audited, never deleted). The API already omits them; the pages skip them too (defence in depth) UNLESS the
  //      page URL carries ?hidden=1 — the reveal for audit, passed through to the API as hiddenQ.
  let revealHidden = false; try { revealHidden = new URLSearchParams(window.location ? window.location.search : "").get("hidden") === "1"; } catch (e) {}
  const hiddenQ = revealHidden ? "&hidden=1" : "";
  function isHidden(r) { return !revealHidden && !!(r && r.hidden === true); }
  // ---- speech (client-side speechSynthesis; the local page used the Studio's Moira voice server-side) ----
  function speak(text) { try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(String(text || "").slice(0, 4000)); u.lang = "en-IE"; speechSynthesis.speak(u); } catch (e) {} }
  function stopSpeech() { try { speechSynthesis.cancel(); } catch (e) {} }

  return { key, filename, setFilename, chooseFolder, unlock, importFile, forget, rememberedFolderName, DEFAULT_FILENAME, KNOWN_FILENAMES, isSynthetic, hidden, isHidden, hiddenQ, revealHidden,
           decryptRow, encryptText, publicKeys, keyNameOfKid, postKamMessage, getJSON, toMsg, toCard, agentOfRow, localTs, speak, stopSpeech, VIEW_TO_CLIENT,
           FILE_MAX, encryptFile, decryptFileMeta, decryptFileBytes, listFiles, fetchFileBytes, uploadKamFile, newId, sha256hex,
           _internals: { pemToDer, unb64, b64, AAD, BLOB_AAD, SCHEME, wrappedEntries, spkiFromJwk, kidOfPkcs8 } };
})();
