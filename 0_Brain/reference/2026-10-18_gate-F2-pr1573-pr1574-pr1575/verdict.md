#1573 (KS-1490) head bd935f41d0b8fd8d142c11e199448c5c44433dfa: GO WITH NOTE (trailing-slash strip is correct and host-safe; two LOW notes, neither blocks)
#1574 (KS-1619 p2) head 2bc9cb6502a8bac13eac92cf126602c1829b7c85: GO (new cell reds exactly under M4e, nothing else, full originate 1381/1381)
#1575 (KS-1619 p1) head 8b53b5212fd1b60e7f0a355d57259d2f778af395: GO (new cell reds exactly under M1c, nothing else, full api-gateway 1171/1171)
sha256/16: 37a566667edad8f4

Security-shaped findings: none. (#1573 touches an env-sourced outbound URL; the host, scheme and port never change in any input tried. #1574/#1575 are test-only.)
Round 1 of 2. Live develop re-read: 1f73d7ac8cc17add318601c6c572bcace3d5a596 (matches Wednesday's ls-remote). All three heads fetched match the brief.

## FOUND
- F1 (LOW, #1573, Blockchain/Dev/connectors/whatsapp-bot/src/index.ts:26): the startup banner `API target: ${process.env.SECUURA_API_URL || ...}` still prints the RAW value, so with `SECUURA_API_URL=https://h/` it prints the slash while verify.ts calls the stripped URL. Cosmetic; the ks812 suite greps that exact banner text, so changing it needs the test edited too. Not in this PR's scope (note only).
- F2 (LOW, #1573, verify.ts:5): a base carrying a query string is still mis-joined, before and after: `https://h.test/base/?q=1` -> `https://h.test/base/?q=1/api/verification/verify`. And `https://h.test?q=/` now loses the slash inside the query value (`?q=/api/...`, was `?q=//api/...`; both wrong). Host unchanged either way. Operator misconfiguration only; no reachable input changes host. Informational.
- F3 (INFO, #1573): an override that is only slashes (`/`, `///`) becomes an empty base, so the URL is the relative `/api/verification/verify` (was `//api/...` / `////api/...`). Node fetch rejects both; no new host. `//evil.test/` becomes `//evil.test/api/...` (protocol-relative, was `//evil.test//api/...`): same class, unchanged by the PR, Node fetch rejects a schemeless URL.
- F4 (INFO, #1575): the new cell passes the full file 10 of 10 runs (no flake seen); its own wait is bounded at 2 s and the cell at 15 s. It also reds under M1d (listener removed) together with one existing KS-1183 cell, which is the expected overlap, not a defect.
- F5 (INFO): ks730c test-title style `RED KS-1619 T1 ...` / `RED KS-1619 D1 ...` is consistent with neighbouring cells.

## TESTED (all at live develop 1f73d7ac8; clone /private/tmp/claude-501/gateF2/repo)
1. Hunk diff per PR (merge-base 9251ae54d, `git diff develop...prN`): #1573 = verify.ts +2/-1 and ks812 suite +13, exactly the two named files; #1574 = ks730c test only, +38; #1575 = ks1087 test only, +26. Nothing else. Develop has not touched any of those files since the merge base (`git diff prN develop` on them shows only the PR's own lines).
2. #1573 red-first/green: PR's 7-cell suite against develop's verify.ts: 5 pass, 2 FAIL (`https://example.test//api/...` and `https://example.test/base///api/...`); against the PR's verify.ts: 7/7. Develop's own 5-cell suite against the PR's verify.ts: 5/5. connector tsc --noEmit rc 0 (and a planted type error makes it fail, so tsc is live).
3. #1573 URL join (probe in /private/tmp/claude-501/gateF2/urlprobe.mjs, develop vs PR, real verify.ts with types stripped, stub fetch; table of what the URL becomes):
   - unset / empty -> `https://demo-pk.secuura.net/api/verification/verify` both.
   - `https://h.test` 0 slashes -> `https://h.test/api/verification/verify` both.
   - 1 slash `https://h.test/` -> develop `https://h.test//api/...`, PR `https://h.test/api/...`.
   - 2 slashes -> develop `///api`, PR `/api`. 3 slashes -> develop `////api`, PR `/api`.
   - path + 2 slashes `https://h.test/base//` -> develop `/base///api`, PR `/base/api`.
   - `http://h.test:8080//` -> PR `http://h.test:8080/api/...` (port and scheme kept).
   - query string and empty-base cases: see F2/F3.
   - Host part (protocol//host:port) is identical develop vs PR in all 15 inputs that parse; no input produced a new host or a scheme change.
   - Mutants on #1573: strip only ONE slash (`/\/$/`) -> exactly the two-slash cell reds (6 pass, 1 fail); change the default host -> the VM-ingress cell reds (6/1); comment-only control: 7/7, tsc 0; restored 7/7.
4. #1574: suite 31/31. M4e (`break;` after the catch `results.push`, adminConfig.ts:2237, from-text matched exactly once at develop) -> 30/31, ONLY `RED KS-1619 T1 three tenants, the middle one throwing...` red. Full originate suite under M4e: 1380/1381, the same single cell. Extra mutant M4f (`break;` after the success push, :2229) also reds only that cell. NOT-caught mutant (`copied.docTypes += 5`, count inflation): 31/31, new cell stays green (specific). Comment-only control on adminConfig.ts: 31/31. Restored 31/31. Full originate at PR head 110 suites 1381/1381; develop without the PR 1380 (so +1 exactly). originate tsc rc 0. New cell alone via `-t KS-1619` passes (not order-dependent).
5. #1575: suite 12/12. M1c (`proxyRes.pause()` in the data listener, verification.ts:1068, from-text matched once) -> 11/12, ONLY `RED KS-1619 D1 ...` red; full api-gateway under M1c 1170/1171, same single cell. M1d (listener removed) -> the new cell plus one KS-1183 cell. NOT-caught mutant (drop the 'aborted' settle): 12/12 (specific). Comment-only control: 12/12. Restored 12/12. Full api-gateway at PR head 351 files 1171/1171; develop 1174 (develop carries 3 more tests from other merged work; the PR adds exactly 1). 10 consecutive runs of the file all 12/12. api-gateway tsc rc 0.
6. Merge prediction (git merge-tree --write-tree plus chained commit-tree on live develop): each of #1573, #1574, #1575, #1576 alone merges clean. File overlap among the four: none (7 files, each in exactly one PR; #1576 = originate verification.ts + two ks1114 tests). Orders 1573-1574-1575-1576, 1576-1575-1574-1573, 1574-1576-1573-1575, 1575-1573-1576-1574 ALL give tree d753dcc43754, matching R's prediction. Three-PR orders 1573/1574/1575 and its reverse give 2a2b74b0bf3a both ways; pairs are order-independent. Planted conflicting control (a develop-side commit editing the same verify.ts line and the same ks730c line): merge-tree reports a conflict (rc 1, stages 1/2/3) for #1573 and #1574, and clean for #1575 (untouched file), so the check can fail. On the merged d753dcc43754 tree: ks812 7/7, ks730c 31/31, ks1087 12/12.
7. Shell suite on #1573 (`run-shell-suites.sh`): 89 passed, 2 failed of 91 in my clone; the 91 includes one extra copy I made of develop's ks812 file, so 90 real suites. The 2 failures (ks949_main_seed_idempotence: packages/shared dist missing at that moment; preflight_test_types_ratchet_leg: needs installs my clone lacks) fail identically on develop (rc 1 both), so they are environmental in my clone and not caused by the PR. I could therefore NOT reproduce the author's "90/90"; I reproduce 88 of the other 88 real suites green and the two as environmental.

## NOT tested
- Preflight 13/16 (legs 3, 4, 8 skipped): not run; the author's skips stand unverified here.
- The two environmental shell suites above, under a fully installed tree; docker, e2e, any live demo-pk.secuura.net request (stub fetch only); the dead-host sweep (out of scope per brief).
- whatsapp-bot tsc used the Dev root node_modules (the connector has no node_modules of its own); rc 0 and a planted error fails.
- api-gateway `tsconfig.test.json` has 35 pre-existing errors at develop and the same 35 at #1575 (none in ks1087); I did not chase them.
- Process disclosure: one script (t1573.sh) used a `cd` inside a subshell for tsc, against the brief; every later tsc used `-p <path>`. My clone has untracked `.bak` files and a copy ks812_dev_copy.test.sh (no delete verb used). node_modules in my clone are symlinks to the project's (read only); @secuura workspace links point into my clone and I built packages/shared dist there. Nothing was written in !CODING.

## Severities
- LOW: index.ts:26 raw banner (F1). INFO: F2, F3, F4. No HIGH/MED.

WALL-CLOCK: 17
