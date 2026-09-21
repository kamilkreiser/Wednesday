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
   3. ROW -> LOCAL MESSAGE SHAPE, so the two pages can keep the local cockpit.html / chat.html render code unchanged. */
"use strict";
window.WED = (function () {
  const SCHEME = "rsa-oaep-sha256+aes-256-gcm/v1";
  const DB = "wedpanel", STORE = "keys", K_CRYPTOKEY = "kam-pilot", K_DIR = "keydir";
  const LS_FILENAME = "wed_key_filename", DEFAULT_FILENAME = "kam-pilot-private.pem";
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

  // ---- key state ----
  const key = { priv: null, source: null, dirName: null, needsClick: false, fsAvailable: typeof window.showDirectoryPicker === "function" };
  function filename() { try { return localStorage.getItem(LS_FILENAME) || DEFAULT_FILENAME; } catch (e) { return DEFAULT_FILENAME; } }
  function setFilename(n) { try { localStorage.setItem(LS_FILENAME, (n || "").trim() || DEFAULT_FILENAME); } catch (e) {} }
  async function importPem(text) {
    if (!/BEGIN PRIVATE KEY/.test(text)) throw new Error('need a PKCS8 "BEGIN PRIVATE KEY" PEM');
    // extractable=false: even this page cannot read the key material back out of the CryptoKey
    return crypto.subtle.importKey("pkcs8", pemToDer(text), { name: "RSA-OAEP", hash: "SHA-256" }, false, ["decrypt"]);
  }
  async function readFromFolder(handle, interactive) {
    let perm = await handle.queryPermission({ mode: "read" });
    if (perm !== "granted") {
      if (!interactive) { key.needsClick = true; key.dirName = handle.name; return false; }
      perm = await handle.requestPermission({ mode: "read" });      // the ONE click, inside a user gesture
      if (perm !== "granted") throw new Error("read permission for folder “" + handle.name + "” was not granted");
    }
    const fh = await handle.getFileHandle(filename());               // throws NotFoundError if the file is not there
    const text = await (await fh.getFile()).text();
    key.priv = await importPem(text); key.source = "folder"; key.dirName = handle.name; key.needsClick = false;
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
    if (ck) { key.priv = ck; key.source = "imported"; return true; }
    return false;
  }
  /* Fallback (Safari/iOS/Firefox, or by choice): import the file once; kept in IndexedDB for this browser only. */
  async function importFile(file) {
    key.priv = await importPem(await file.text()); key.source = "imported"; key.dirName = null; key.needsClick = false;
    await idbPut(K_CRYPTOKEY, key.priv);
  }
  async function forget() { await idbDel(K_CRYPTOKEY); await idbDel(K_DIR); key.priv = null; key.source = null; key.dirName = null; key.needsClick = false; }
  async function rememberedFolderName() { if (!key.fsAvailable) return null; const h = await idbGet(K_DIR); return h ? h.name : null; }

  // ---- envelope: decrypt (rows from the seats and from Kam himself) ----
  async function decryptRow(r) {
    if (!key.priv) return null;
    if (r.scheme !== SCHEME) throw new Error("scheme " + r.scheme);
    const dk = await crypto.subtle.decrypt({ name: "RSA-OAEP" }, key.priv, unb64(r.wrapped_key));
    const k = await crypto.subtle.importKey("raw", dk, { name: "AES-GCM" }, false, ["decrypt"]);
    const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv: unb64(r.iv), additionalData: AAD(r) }, k, unb64(r.ciphertext));
    return new TextDecoder().decode(pt);
  }
  // ---- envelope: encrypt (Kam's replies, to his own PUBLIC key; the server never sees the text) ----
  let pubCache = null;
  async function publicKey() {
    if (pubCache) return pubCache;
    const pem = await (await fetch("/api/pubkey", { cache: "no-store" })).text();
    if (!/BEGIN PUBLIC KEY/.test(pem)) throw new Error("public key unavailable");
    const der = pemToDer(pem);
    pubCache = { key: await crypto.subtle.importKey("spki", der, { name: "RSA-OAEP", hash: "SHA-256" }, false, ["encrypt"]), kid: (await sha256hex(der)).slice(0, 16) };
    return pubCache;
  }
  async function encryptText(text, clear) {
    const pub = await publicKey();
    const dk = crypto.getRandomValues(new Uint8Array(32)), iv = crypto.getRandomValues(new Uint8Array(12));
    const ak = await crypto.subtle.importKey("raw", dk, { name: "AES-GCM" }, false, ["encrypt"]);
    const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv, additionalData: AAD(clear) }, ak, new TextEncoder().encode(text));
    const wrapped = await crypto.subtle.encrypt({ name: "RSA-OAEP" }, pub.key, dk);
    return { scheme: SCHEME, kid: pub.kid, iv: b64(iv), wrapped_key: b64(wrapped), ciphertext: b64(ct) };
  }
  function utcNow() { return new Date().toISOString(); }               // 2026-09-21T01:23:45.678Z — the API's ts format
  function newId() { const u = crypto.getRandomValues(new Uint8Array(6)); return "kam-" + [...u].map(x => x.toString(16).padStart(2, "0")).join(""); }
  /* Kam types on a tab -> view -> partition. Encrypted here; POSTed as an envelope; refused by the server if it carries text. */
  async function postKamMessage(text, view) {
    const client = VIEW_TO_CLIENT[view]; if (!client) throw new Error("view " + view);
    const clear = { client, kind: "message", id: newId(), ts: utcNow(), view };
    const envelope = await encryptText(text, clear);
    const r = await fetch("/api/kam/messages", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ client, view, id: clear.id, ts: clear.ts, envelope }) });
    if (r.status === 401 || r.redirected) throw new Error("session expired — reload to sign in");
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error((j && j.detail) || ("HTTP " + r.status));
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
      text: pt == null ? "" : pt, locked: pt === null, error: err || null, backfill: !!r.backfill, kind: r.kind };
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

  // ---- speech (client-side speechSynthesis; the local page used the Studio's Moira voice server-side) ----
  function speak(text) { try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(String(text || "").slice(0, 4000)); u.lang = "en-IE"; speechSynthesis.speak(u); } catch (e) {} }
  function stopSpeech() { try { speechSynthesis.cancel(); } catch (e) {} }

  return { key, filename, setFilename, chooseFolder, unlock, importFile, forget, rememberedFolderName, DEFAULT_FILENAME,
           decryptRow, encryptText, postKamMessage, getJSON, toMsg, toCard, agentOfRow, localTs, speak, stopSpeech, VIEW_TO_CLIENT,
           _internals: { pemToDer, unb64, b64, AAD, SCHEME } };
})();
