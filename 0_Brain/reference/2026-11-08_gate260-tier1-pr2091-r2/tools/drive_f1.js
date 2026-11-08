async (page) => {
  // Gate 260 F1 drive. Predicates declared BEFORE the first run:
  //  fallbackVisible = a "Loading..." element inside <main> region passes Playwright isVisible() (CSS-visible, non-empty box)
  //  oldVisible      = the OLD page's <h1> (Settings or Documents) passes isVisible()
  //  oldInDom        = same <h1> present in the DOM (recorded separately, NOT the predicate)
  // Expected: dev (v6) and head (v7 + useTransitions={false}) => fallbackVisible && !oldVisible on every held sample;
  //           r1 (v7, no opt-out) => !fallbackVisible && oldVisible on every held sample.
  // FAIL for F1 = head differs from dev in any held sample on fallbackVisible or oldVisible.
  const builds = [['dev', 4323], ['r1', 4321], ['head', 4322]];
  const HOLD = 2500;
  const user = { id: 'u1', email: 'qa@example.test', role: 'ISSUER_ADMIN', displayName: 'QA Gate' };
  const scen = [
    { name: 'settings->documents', start: '/settings', click: 'Documents', chunk: /\/assets\/DocumentList-[^/]+\.js$/, oldH: 'Settings', newH: 'Documents', path: '/documents' },
    { name: 'documents->settings', start: '/documents', click: 'Settings', chunk: /\/assets\/Settings-[^/]+\.js$/, oldH: 'Documents', newH: 'Settings', path: '/settings' },
  ];
  const results = {};
  for (const s of scen) for (const [b, port] of builds) for (const held of [true, false]) {
    const key = `${s.name}|${b}|${held ? 'held' : 'unheld'}`;
    await page.unrouteAll({ behavior: 'ignoreErrors' });
    const errs = [];
    const onErr = (e) => errs.push('pageerror: ' + String(e).slice(0, 120));
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
    const startH = page.getByRole('heading', { level: 1, name: s.oldH, exact: true });
    await startH.first().waitFor({ state: 'visible', timeout: 15000 });
    const hitsBeforeClick = chunkHits;
    const btn = page.getByRole('button', { name: s.click, exact: true }).locator('visible=true').first();
    await btn.click();
    const samples = [];
    const loading = page.locator('main').getByText('Loading...', { exact: true });
    const anyLoading = page.getByText('Loading...', { exact: true });
    const oldH = page.getByRole('heading', { level: 1, name: s.oldH, exact: true, includeHidden: true });
    for (let i = 0; i < 8; i++) {
      await page.waitForTimeout(200);
      const lv = await anyLoading.first().isVisible().catch(() => false);
      const lc = await anyLoading.count();
      const ov = await oldH.first().isVisible().catch(() => false);
      const oc = await oldH.count();
      samples.push({ path: new URL(page.url()).pathname, fallbackVisible: lv, fallbackInDom: lc, oldVisible: ov, oldInDom: oc });
    }
    await page.waitForTimeout(held ? HOLD : 500);
    const newH = page.getByRole('heading', { level: 1, name: s.newH, exact: true });
    await newH.first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
    const after = { path: new URL(page.url()).pathname, newVisible: await newH.first().isVisible().catch(() => false), fallbackVisible: await anyLoading.first().isVisible().catch(() => false), oldInDom: await oldH.count() };
    page.off('pageerror', onErr);
    results[key] = {
      chunkHitsBeforeClick: hitsBeforeClick, chunkHitsTotal: chunkHits,
      fbVisible: samples.filter((x) => x.fallbackVisible).length,
      oldVisible: samples.filter((x) => x.oldVisible).length,
      oldInDomButHidden: samples.filter((x) => x.oldInDom > 0 && !x.oldVisible).length,
      pathsOk: samples.filter((x) => x.path === s.path).length,
      samples: samples.map((x) => `${x.fallbackVisible ? 'F' : '-'}${x.fallbackInDom}${x.oldVisible ? 'O' : '-'}${x.oldInDom}`).join(' '),
      after, errs,
    };
  }
  await page.unrouteAll({ behavior: 'ignoreErrors' });
  return results;
}
