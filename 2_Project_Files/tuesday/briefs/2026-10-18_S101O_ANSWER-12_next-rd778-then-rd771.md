BLUF: Build RD-778 next (the js/xss-through-dom alerts). Then build RD-771 stacked on it: the two share static/js/index.js and settings.js. RD-768 and then RD-767 come after that, in that order, each by its own ANSWER. No merge: each ends at READY FOR QA, then a draft PR.

What Tuesday checked at source (code-scanning API, open on refs/heads/main, NexusAI gh config, ~16:3x AEDT): js/xss-through-dom is open at exactly your 8 sites (chart-details.js:542, first-run-setup.js:3068, index-offline.js:81, index.js:672/5413/5475/5557, settings.js:1756). js/incomplete-url-substring-sanitization is open at index.js:10/11 and settings.js:10/11. Your screen, predicate and in-flight file set are accepted as you measured them. Tuesday did not re-derive the 59 paths.

One thing your list did not name: a 9th open xss-through-dom alert at docs/test-files/test-import.html:41. It is not shipped code. Find out whether a ticket already covers it (search the path, not the phrasing). If none does, name it in RD-778's NOT TESTED as a separate ticket candidate. Do not fix it inside RD-778.

RD-778, as ruled:
1. Fix in code, never by dismissal: textContent or DOM construction in place of innerHTML/document.write for values read back from the DOM, at all 8 sites. CodeQL is never bypassed and no alert is dismissed.
2. Red-first cells (jsdom, a new test file):
   - For the two real paths you named: a chat message carrying a script/img-onerror payload stays inert text at index-offline.js:81, and a server errorCode carrying markup stays text at first-run-setup.js:3068. Each is red at c7ca0ed, green at your head.
   - Controls: an ordinary message and an ordinary error render exactly as before. Do the same for each of the other 6 sites where a cell can reach it, and say which could not be reached.
3. Rendered text and layout stay IDENTICAL. No customer-facing word changes. If a site needs any visible change, STOP and ask.
4. Branch off main c7ca0ed. Base it on main, not your stack: these files are disjoint from RD-476/856/857, and an off-stack branch lands independently. Name it rd-778-...-s101o.
5. Your verify waits FIFO on the jest lock behind gates 25 and 26 (lock base session-tools/locks-laptop-1017). That is expected; never jump the queue.
6. READY FOR QA carries a PRIOR WORK section, your red/green table, the alert list before and after, and NOT TESTED. QA tier 1: security, browser-rendered. Its gate will drive a real browser to compare renders. Open the draft PR after READY.

RD-771 after RD-778 is READY: one hostname-suffix helper with a dot boundary, behaviour identical (your reading: IS_PRODUCTION only gates debug logging). Stack it on rd-778 because the files are shared. Red-first cells on the evil-suffix host shape. Tier 2.

-- Tuesday
