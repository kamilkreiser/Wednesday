async (page) => {
  // Gate 260 F1 drive v2. v1 (drive_f1.js) is kept and labelled INVALID: its "old page" locator (first h1 named X) matched the
  // Layout HEADER h1, whose text follows the URL, and v1 clicked at the instant the start heading appeared (no settle).
  // Predicates, declared before this run:
  //   fbVisible  = some <p> "Loading..." inside <main> passes el.checkVisibility({checkOpacity, checkVisibilityCSS}) AND has a non-zero box
  //   oldVisible = the OLD page's own <h1> inside <main> passes the same visibility test
  //   oldInDom   = that <h1> exists in <main> (recorded, NOT a predicate)
  //   header     = the Layout header <h1> text (shows whether the Layout re-rendered with the new location)
  // Expected (settled runs): dev and head => fbVisible && !oldVisible in 8 of 8 held samples; r1 => !fbVisible && oldVisible in 8 of 8.
  // F1 FAIL = head differs from dev on fbVisible or oldVisible in any held sample.
  // Planted control (run 'plant'): a display:none <p>Loading...</p> is appended to <main> on the head build before the click with
  // NO chunk held; the predicate must say fbVisible=false on samples taken after the page arrives while the plant is still in the DOM.
  const builds = [['dev', 4323], ['r1', 4321], ['head', 4322]];
  const HOLD = 2500;
  const user = { id: 'u1', email: 'qa@example.test', role: 'ISSUER_ADMIN', displayName: 'QA Gate' };
  const scen = [
    { name: 'settings->documents', start: '/settings', click: 'Documents', chunk: /\/assets\/DocumentList-[^/]+\.js$/, oldH: 'Settings', newH: 'Documents', path: '/documents' },
    { name: 'documents->settings', start: '/documents', click: 'Settings', chunk: /\/assets\/Settings-[^/]+\.js$/, oldH: 'Documents', newH: 'Settings', path: '/settings' },
  ];
  const probe = (oldH) => page.evaluate((oldH) => {
    const vis = (el) => !!el && el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }) && el.getBoundingClientRect().height > 0;
    const main = document.querySelector('main');
    const ld = main ? [...main.querySelectorAll('p')].filter((p) => p.textContent.trim() === 'Loading...') : [];
    const old = main ? [...main.querySelectorAll('h1')].filter((h) => h.textContent.trim() === oldH) : [];
    const hdr = document.querySelector('header h1');
    return { path: location.pathname, fbVisible: ld.some(vis), fbInDom: ld.length, oldVisible: old.some(vis), oldInDom: old.length, header: hdr ? hdr.textContent.trim() : null };
  }, oldH);
  const results = {};
  const runOne = async (key, s, port, held, settle, plant) => {
    await page.unrouteAll({ behavior: 'ignoreErrors' });
    const errs = [];
    const onErr = (e) => errs.push(String(e).slice(0, 120));
    page.on('pageerror', onErr);
    let chunkHits = 0;
    await page.route('**/*', async (route) => {
      const u = new URL(route.request().url());
      if (u.pathname.startsWith('/api/')) {
        if (u.pathname === '/api/auth/refresh') return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, data: { accessToken: 'tok', expiresIn: 900, tokenType: 'Bearer' } }) });
        if (u.pathname === '/api/users/me') return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, data: user }) });
        return route.fulfill({ status: 404, contentType: 'application/json', body: '{"success":false}' });
      }
      if (s.chunk.test(u.pathname)) { chunkHits++; if (held) await new Promise((r) => setTimeout(r, HOLD)); }
      return route.continue();
    });
    await page.goto(`http://127.0.0.1:${port}${s.start}`, { waitUntil: 'load' });
    await page.locator('main h1', { hasText: s.oldH }).first().waitFor({ state: 'visible', timeout: 15000 });
    if (settle) await page.waitForTimeout(settle);
    const pre = await probe(s.oldH);
    if (plant) await page.evaluate(() => { const p = document.createElement('p'); p.textContent = 'Loading...'; p.style.display = 'none'; p.id = 'qa-plant'; document.querySelector('main').appendChild(p); });
    const hitsBeforeClick = chunkHits;
    await page.getByRole('button', { name: s.click, exact: true }).locator('visible=true').first().click();
    const samples = [];
    for (let i = 0; i < 8; i++) { await page.waitForTimeout(200); samples.push(await probe(s.oldH)); }
    await page.waitForTimeout(held ? HOLD : 300);
    await page.locator('main h1', { hasText: s.newH }).first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
    const after = await probe(s.oldH);
    after.newVisible = await page.locator('main h1', { hasText: s.newH }).first().isVisible().catch(() => false);
    after.plantInDom = await page.locator('#qa-plant').count();
    page.off('pageerror', onErr);
    results[key] = {
      hitsBeforeClick, chunkHits, pre: `${pre.fbVisible ? 'F' : '-'}${pre.oldVisible ? 'O' : '-'} hdr=${pre.header}`,
      fbVisible: samples.filter((x) => x.fbVisible).length, oldVisible: samples.filter((x) => x.oldVisible).length,
      oldInDomHidden: samples.filter((x) => x.oldInDom > 0 && !x.oldVisible).length, fbInDomHidden: samples.filter((x) => x.fbInDom > 0 && !x.fbVisible).length,
      pathOk: samples.filter((x) => x.path === s.path).length,
      headers: [...new Set(samples.map((x) => x.header))].join('/'),
      after: `path=${after.path} new=${after.newVisible} fb=${after.fbVisible} fbInDom=${after.fbInDom} old=${after.oldInDom} plant=${after.plantInDom}`, errs,
    };
  };
  for (const settle of [1000, 0]) for (const s of scen) for (const [b, port] of builds) for (const held of [true, false]) for (const rep of (settle && held ? [1, 2] : [1])) {
    await runOne(`settle${settle}|${s.name}|${b}|${held ? 'held' : 'unheld'}|rep${rep}`, s, port, held, settle, false);
  }
  await runOne('PLANT|settings->documents|head|unheld', scen[0], 4322, false, 1000, true);
  await page.unrouteAll({ behavior: 'ignoreErrors' });
  return results;
}
