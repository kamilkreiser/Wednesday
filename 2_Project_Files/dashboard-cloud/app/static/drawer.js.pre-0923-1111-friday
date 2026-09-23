/* drawer.js — the FILE DRAWER of the live site (2026-09-22), shared by / and /chat. Loaded after common.js.
   Kam, 15:26:48: "create a download button next to autoplay replies and stop so that if I ask for a file to be shared, you
   can share it with me and place it there and I can download it at a later stage from the live site". 15:31:07: "Does the
   dashboard that's live still provide the file upload feature? If not, can you please add this?"
   WHAT LIVES HERE: (1) the "files" button beside auto-play / stop and the drawer it opens (every ready file the viewer may see:
   the seats' shares AND Kam's own uploads; name / size / when / note decrypt with the key; one download button per row —
   the bytes are fetched, DECRYPTED IN THIS PAGE (WED.decryptFileBytes), sha256-checked against the meta, then saved);
   (2) the drop zone (the whole conversation column) + the attach button: files queue as chips in #pending and are encrypted +
   uploaded when the message is sent (WED.uploadKamFile; the message row carries their ids in `attachments`);
   (3) attachment chips under a message (names from the drawer's rows; click = download).
   Nothing here talks to the server except through WED (common.js); no key material, no plaintext leaves the page. */
"use strict";
window.WEDFILES = (function () {
  const rows = new Map();          // row_key -> file row (raw) ; meta cache in metas
  const metas = new Map();         // row_key -> decrypted meta | null (locked) | undefined (failed)
  const byId = new Map();          // file id -> row_key
  const pending = [];              // File objects queued for the next send
  let sinceF = null, drawerEl = null, listEl = null, btn = null, open = false, lastErr = "";
  const fmt = n => n < 1024 ? n + " B" : n < 1048576 ? (n / 1024).toFixed(1) + " KB" : (n / 1048576).toFixed(1) + " MB";
  const esc = s => String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  function whoOf(r) { return r.role === "kam" ? "you" : (r.seat === "tuesday" || r.client === "Datasec") ? "Tuesday" : "Wednesday"; }

  async function refresh() {
    try {
      const list = await WED.listFiles(sinceF);
      for (const r of list) { if (WED.isSynthetic(r) || WED.isHidden(r)) continue; if (!sinceF || r.row_key > sinceF) sinceF = r.row_key; rows.set(r.row_key, r); byId.set(r.id, r.row_key); }
      await decryptMetas(); lastErr = "";
    } catch (e) { lastErr = String(e.message || e); }
    paint(); paintButton();
  }
  async function decryptMetas() {
    for (const [k, r] of rows) {
      if (metas.has(k) && metas.get(k) !== null) continue;
      if (!WED.key.priv) { metas.set(k, null); continue; }
      try { metas.set(k, await WED.decryptFileMeta(r)); } catch (e) { metas.set(k, undefined); r._err = String(e.message || e); }
    }
  }
  function afterKeyChange() { metas.clear(); return decryptMetas().then(paint); }

  async function download(r) {
    const m = metas.get(r.row_key);
    if (!m) throw new Error("unlock the key first");
    const ct = await WED.fetchFileBytes(r);
    const pt = await WED.decryptFileBytes(r, ct);
    const sha = await WED.sha256hex(pt);
    if (m.sha256 && sha !== m.sha256) throw new Error("decrypted bytes do not match the file's sha256 — not saved");
    const blob = new Blob([pt], { type: m.mime || "application/octet-stream" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = m.name || (r.id + ".bin"); document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
    return { name: m.name, size: pt.byteLength, sha256: sha };
  }

  // ---- drawer DOM ----
  function ensureDrawer() {
    if (drawerEl) return;
    drawerEl = document.createElement("aside"); drawerEl.id = "drawer"; drawerEl.hidden = true; drawerEl.setAttribute("aria-label", "Files shared with you");
    drawerEl.innerHTML = '<div id="drawer-h"><span>Files</span><span id="drawer-n" class="note"></span><button id="drawer-close" type="button" title="close">&#10005;</button></div>'
      + '<div id="drawer-note" class="note">shared by a seat, or attached by you — encrypted at rest; decrypted in this browser when you download</div><div id="drawer-list"></div>';
    document.body.appendChild(drawerEl);
    listEl = drawerEl.querySelector("#drawer-list");
    drawerEl.querySelector("#drawer-close").addEventListener("click", () => toggle(false));
  }
  function toggle(on) { ensureDrawer(); open = on === undefined ? !open : !!on; drawerEl.hidden = !open; btn && btn.classList.toggle("on", open); if (open) refresh(); }
  function paintButton() { if (!btn) return; const n = rows.size; btn.textContent = "⬇ files" + (n ? " (" + n + ")" : ""); }
  function paint() {
    if (!drawerEl || !open) return;
    const items = [...rows.values()].sort((a, b) => a.row_key < b.row_key ? 1 : -1);
    drawerEl.querySelector("#drawer-n").textContent = items.length ? items.length + " file" + (items.length === 1 ? "" : "s") + (WED.key.priv ? "" : " — unlock the key to read the names") : (lastErr ? "○ " + lastErr : "");
    listEl.innerHTML = "";
    if (!items.length) { const p = document.createElement("p"); p.className = "empty"; p.textContent = lastErr ? "could not load: " + lastErr : "nothing shared yet"; listEl.appendChild(p); return; }
    for (const r of items) {
      const m = metas.get(r.row_key);
      const div = document.createElement("div"); div.className = "frow" + (r.role === "kam" ? " mine" : "");
      const name = document.createElement("div"); name.className = "fname";
      name.textContent = m === null ? "🔒 encrypted file" : m === undefined ? "decrypt failed" + (r._err ? ": " + r._err : "") : (m.name || "(unnamed)");
      const meta = document.createElement("div"); meta.className = "fmeta";
      meta.textContent = fmt(Number(r.size || 0)) + " · " + (r.direction === "upload" ? "attached by " : "shared by ") + whoOf(r) + " · " + WED.localTs(r.ts).replace("T", " ") + (r.client && r.client !== "WED" ? " · " + r.client : "");
      div.append(name, meta);
      if (m && m.note) { const n = document.createElement("div"); n.className = "fnote"; n.textContent = m.note; div.appendChild(n); }
      const b = document.createElement("button"); b.type = "button"; b.className = "fdl"; b.textContent = "⬇ download"; b.disabled = !m;
      b.title = m ? "fetch, decrypt in this browser, verify sha256, save" : "unlock the key to download";
      b.addEventListener("click", async () => { b.disabled = true; const t = b.textContent; b.textContent = "…"; try { await download(r); b.textContent = "✓ saved"; } catch (e) { b.textContent = t; alert("download failed: " + (e.message || e)); } finally { setTimeout(() => { b.disabled = !metas.get(r.row_key); if (b.textContent === "✓ saved") b.textContent = t; }, 1500); } });
      div.appendChild(b);
      listEl.appendChild(div);
    }
  }

  // ---- pending attachments (Kam -> the seat) ----
  function pendingEl() { return document.getElementById("pending"); }
  function paintPending() {
    const el = pendingEl(); if (!el) return; el.innerHTML = "";
    pending.forEach((f, i) => {
      const chip = document.createElement("span"); chip.className = "pf";
      chip.innerHTML = "📎 " + esc(f.name) + " <i>" + esc(fmt(f.size)) + "</i> ";
      const x = document.createElement("button"); x.type = "button"; x.textContent = "×"; x.title = "remove"; x.addEventListener("click", () => { pending.splice(i, 1); paintPending(); });
      chip.appendChild(x); el.appendChild(chip);
    });
  }
  function addFiles(list) {
    for (const f of list || []) {
      if (f.size + 16 > WED.FILE_MAX) { alert(f.name + " is larger than the " + Math.floor(WED.FILE_MAX / 1048576) + " MiB bound — not attached"); continue; }
      if (f.size === 0) { alert(f.name + " is empty — not attached"); continue; }
      pending.push(f);
    }
    paintPending();
  }
  function pendingCount() { return pending.length; }
  /* encrypt + upload every queued file for the message `msgId` on tab `view`; returns the file ids (the message's `attachments`) */
  async function uploadPending(view, msgId) {
    const ids = [];
    while (pending.length) {
      const f = pending[0];
      const u = await WED.uploadKamFile(f, view, msgId, "");
      ids.push(u.id); pending.shift(); paintPending();
    }
    if (ids.length) refresh();
    return ids;
  }
  function armDropZone(zone, input, attachBtn) {
    if (!zone) return;
    ["dragenter", "dragover"].forEach(ev => zone.addEventListener(ev, e => { e.preventDefault(); zone.classList.add("dropping"); }));
    ["dragleave", "drop"].forEach(ev => zone.addEventListener(ev, e => { e.preventDefault(); zone.classList.remove("dropping"); }));
    zone.addEventListener("drop", e => addFiles(e.dataTransfer && e.dataTransfer.files));
    if (input) input.addEventListener("change", e => { addFiles(e.target.files); input.value = ""; });
    if (attachBtn && input) attachBtn.addEventListener("click", () => input.click());
  }
  /* attachment chips under a message (the drawer knows the names once the key is unlocked) */
  function attachmentsEl(m) {
    if (!m || !Array.isArray(m.attachments) || !m.attachments.length) return null;
    const div = document.createElement("div"); div.className = "atts";
    for (const id of m.attachments) {
      const rk = byId.get(id), r = rk ? rows.get(rk) : null, meta = rk ? metas.get(rk) : null;
      const a = document.createElement("a"); a.href = "#files"; a.textContent = "📎 " + (meta && meta.name ? meta.name : r ? "🔒 file" : "file " + id);
      a.title = r ? (meta ? "download (decrypted in this browser)" : "unlock the key to read the name") : "not loaded yet — open the drawer";
      a.addEventListener("click", async e => { e.preventDefault(); if (!r) { toggle(true); return; } try { await download(r); } catch (err) { alert("download failed: " + (err.message || err)); } });
      div.appendChild(a);
    }
    return div;
  }
  function init(opts) {
    btn = document.getElementById("filesbtn");
    if (btn) btn.addEventListener("click", () => toggle());
    if (location.hash === "#files") setTimeout(() => toggle(true), 300);
    armDropZone(opts && opts.zone, opts && opts.input, opts && opts.attachBtn);
    refresh(); setInterval(refresh, 20000);
  }
  return { init, refresh, toggle, download, addFiles, pendingCount, uploadPending, attachmentsEl, afterKeyChange, rows, metas, _internals: { fmt, whoOf } };
})();
