# Gate 255, tier 1: verdict

| PR | head | verdict |
|---|---|---|
| 2091 (KS-528, react-router-dom 6 -> react-router 7, three portals) | 258e049aaf75ff8f5009449eb918a7c0a98624fb | **GO WITH NOTES** |

No finding needs a ruling from Kam to merge. F1 needs a decision from whoever owns the issuer UX: accept the change, or opt out (`useTransitions={false}`). Severity is my call. Priority is not.

## Readings (origin, ls-remote with the project deploy key)

| when (UTC) | develop | PR 2091 head / branch `feature/ks-528-react-router-v7-r87` |
|---|---|---|
| start 10:34:07Z | 14ac61bd1a4c854c17539f1cd0f518631f998fbb (matches the commission) | 258e049aaf75 / 258e049aaf75 |
| end 10:54:40Z | **a2c3ec7f3f98f97b886eb789cc2745182b627f6f (moved, 1 commit, KS-1503)** | 258e049aaf75 / 258e049aaf75 (unchanged) |

The head did not move, so this verdict stands. Develop moved by one commit (7 paths: packages/shared jwks + its test, one shell suite, four KS-1503 docs fragments). None of those paths is among this PR's 34, and none is a manifest, lock or audit file. `merge-tree a2c3ec7f 258e049a` gives rc 0, tree 1b95999704e9. I ran the 11-PR merge-tree on 14ac61bd, not on a2c3ec7f.

## BLUF

All three portals build at the head in the Dockerfile layout. Issuer vitest passes 15 of 15. The repo's audit gates pass, and its own `npm audit` does not see the two retired advisories at the head (the control on develop's lock does see them). No react-router-dom is left in any of the 4 locks. The new suite is red on develop for the right reason and green at the head. Auth paths, deep links, 404s and logout behave the same on v6 and v7 in a real browser against a mocked API. All 11 shared-path PRs keep the same conflict state as before.

One behaviour change was **MEASURED AT RUNTIME** and the PR does not state it. In the issuer, React Router 7 now wraps navigations in `startTransition` by default. Because of that, the issuer's `<Suspense>` "Loading..." fallback no longer appears on in-app navigation to a page whose chunk has not loaded yet. The URL changes at once, and the old page stays on screen with no indicator until the chunk arrives (F1). The PR body says "no intended behaviour change", and it and the ticket comment report "0 differences". Both statements are accurate for what the seat measured, but neither covers this case (F2).

## Answers to the commission's questions

**Q1. Build and tests at the head** (Node v26.8.1, npm 11.19.0, macOS arm64. `npm ci --no-audit` from each portal's own lock, then `npm run build` = `tsc && vite build` in the Dockerfile layout: portal copied to `<stage>/app`, `frontend/shared` copied to `app/vendor/shared`, `SHARED_DIR=./vendor/shared/src`, no `../shared` sibling. That layout comes from `frontend/<portal>/Dockerfile:15-28`, and it is what the images build. The images use node:24-alpine, which I did not run.)

| portal | built | tests |
|---|---|---|
| admin | **yes** (rc 0) | no `test` script in package.json, so 0 of 0 (nothing to run) |
| issuer | **yes** (rc 0) | **15 of 15** (`vitest run`, 3 files). None of them imports the router, so they say nothing about routing. |
| verifier | **yes** (rc 0) | no `test` script, so 0 of 0 |

I also ran a control build of develop 14ac61bd's sources in the same layout: 3 of 3 build, on-disk react-router 6.30.6 plus react-router-dom. A side observation that is not a PR finding: `npm run build` run in place in `frontend/<portal>` (the dev-host layout, with no root workspace install) fails tsc. All of those errors come from `../shared/src` failing to resolve `zod`/`react`, plus cascades from that. None of them touches the router. I did not run that layout on develop.

**Q2. v6 to v7 behaviour.** Sources: the installed `node_modules/react-router@7.18.5` `CHANGELOG.md` §7.0.0 (line 1720 on), `docs/upgrading/v6.md`, and `docs/explanation/react-transitions.md`.
- Removed APIs (`json`, `defer`, `useFetcher`, `useNavigation`, `ScrollRestoration`, `createBrowserRouter`/`RouterProvider` (now `react-router/dom`), `NavLink`, `useBlocker`, `useMatch`, any `future=` prop): **0 uses** in the three portals' `src`. Positive control: `useNavigate` gets 30 hits in the same grep. The `json(` and `<Link` hits were all false positives: `setKeyFileJson`, and lucide `Link`/`LinkIcon`/`Link2` icons.
- Develop never set the v6 future flags (no `future=` on any `<BrowserRouter>`), so every v7 default is new behaviour for these apps.
  - `v7_relativeSplatPath`: inert. All 52 navigation targets are absolute: 48 `navigate()` calls and 4 `<Navigate>`. There are no relative `navigate('.`/`'..`, no `navigate(-1)`, and the only splat routes are the two admin `path="*"` catch-alls, which use absolute `<Navigate>`. 52 also matches the seat's figure.
  - **`v7_startTransition`: live in the issuer (F1)**. It is inert for admin and verifier, which have no `React.lazy`/`<Suspense>`. The issuer's `lazy()` calls are at module scope (`issuer/src/App.tsx:27-41`), which is the v6.md-compatible pattern, so nothing breaks. Only the fallback stops showing.
  - Data-router flags (fetcherPersist, normalizeFormMethod, partialHydration, skipActionErrorRevalidation): not applicable, because no data router is used.
- `useNavigate` now returns a Promise. Every call site is in an event handler or after an `await` in a submit handler, and none is in render or in a first-run effect. That covers admin `Login.tsx:28`, issuer `Login.tsx:117,152`, verifier `VerifyPage.tsx:91,141-145`. Nothing awaits or chains the return.
- Call sites I checked, beyond the 48 navigate calls listed above:
  - `useLocation`: admin `Layout.tsx:101` and `PolicyDocs.tsx:17`, issuer `Layout.tsx:82` and `PolicyDocs.tsx:17`, verifier `ResultPage.tsx:77` (`location.state.result` handed over from `VerifyPage` navigate state).
  - `useParams`: admin `DocumentTypeDetail.tsx:82`, `ClientDetail.tsx:52`, `Users.tsx:130`; issuer `DocumentDetail.tsx:147`, `LineageViewer.tsx:78`; verifier `ResultPage.tsx:75`.
  - `useSearchParams`: admin `ClientDetail.tsx:54`.
  - `Outlet`: issuer `App.tsx:82`.
  - `BrowserRouter`: admin `App.tsx` (basename /admin), issuer `main.tsx:41` (none), verifier `App.tsx:35` (basename /verify).
- I found no portal code that relies on v6-only behaviour, apart from the Suspense-fallback expectation in F1.

**Q3. Auth paths, MEASURED AT RUNTIME.** I drove the built `dist` with `vite preview`, head and develop side by side (ports 4301-4303 and 4311-4313). Chromium was driven by Playwright with every API call mocked by route interception: `/auth/refresh`, `/users/me`, `/auth/login` and `/auth/logout` stateful, everything else 200-empty (admin) or 404 (issuer/verifier). This was not the gateway. I ran each scenario on both builds. **Every scenario gave the same result on v6 and v7**:

| portal | scenario | result (head = develop) |
|---|---|---|
| admin | unauthenticated deep link `/admin/platform/clients` | redirected to `/admin/login`, login form |
| admin | unauthenticated unknown path | `/admin/login` |
| admin | authenticated hard-nav deep link (refresh cookie path) | stays on `/admin/platform/clients`, sidebar rendered |
| admin | authenticated unknown path | `/admin` (root). The page shows the app's error screen because my empty mock data breaks PlatformAuditLog, identically on both builds. |
| admin | login submit from a deep link | lands on `/admin`. The deep link is not preserved: `Login.tsx:28` hard-codes `navigate('/')`. Pre-existing, same on v6. |
| admin | logout from `/admin/settings` (real click), then browser Back | `/admin/login`; Back stays on `/admin/login` |
| issuer | unauthenticated deep link `/documents/abc` | `/login` |
| issuer | unauthenticated / authenticated unknown path | **empty page (consent banner only); there is no catch-all route.** Pre-existing, same on v6. |
| issuer | authenticated hard-nav deep link `/documents/abc` | stays, Layout rendered |
| issuer | authenticated visit to `/login` | redirected to `/` |
| issuer | login submit from `/documents` | lands on `/`. Deep link not preserved. Pre-existing. |
| issuer | sidebar click to Documents (real click, app's own `navigate()`), then logout via profile menu, then Back | `/documents`, then `/login`, then Back stays on `/login` |
| verifier | `/verify/`, `/verify/result/abc`, `/verify/result` (no state), `/verify/no-such-page` | VerifyPage / ResultPage with "HTTP 404" from the mock / "Verifying document..." / empty page (no catch-all, pre-existing) |

The only behaviour difference I found is F1, below. I did not exercise real login against the gateway, real cookie handling, or the nginx-served paths.

**Q4. Audit baseline.**
- All 4 locks at the head contain no `react-router-dom` and no `@remix-run/router` at any depth. `react-router` is 7.18.5 everywhere: under each portal workspace in the root lock, and at `node_modules/react-router` in each standalone lock. No other lock package depends on react-router. `npm ls react-router react-router-dom --all` in each portal's installed tree shows only `react-router@7.18.5`.
- Measured per-lock delta, base to head: each standalone lock adds `cookie` and `set-cookie-parser`, removes `@remix-run/router` and `react-router-dom`, and moves `react-router` from 6.30.6 to 7.18.5 (plus the root manifest entry). The root lock adds 3 nested `react-router` entries, 3 nested `cookie@1.1.1` and the hoisted `set-cookie-parser`, and removes hoisted `react-router`, `react-router-dom` and `@remix-run/router`. This matches the PR body.
- Repo gates, run as preflight legs 5 to 7 run them (`scripts/audit` deps via `npm ci --ignore-scripts`, cwd Blockchain/Dev, at 10:50Z):
  - `audit-gate.mjs` rc 0, "4 distinct advisories reported, 4 baselined", with no CLEANUP line.
  - `audit-locks.mjs` rc 0 over 44 standalone locks (46 tracked, minus root, minus 1 out of scope).
  - `audit:contract` 62 of 62, equal to `expected-case-count` 62.
- Baseline at the head: 4 rows (848j, w5hq, 5qjj, gcqx). The diff deletes exactly 14 lines, the two KS-528 rows only.
- **Control:** `npm audit --json` on develop's standalone admin lock reports `react-router` moderate via GHSA-wrjc-x8rr-h8h6 and GHSA-337j-9hxr-rhxg (and `react-router-dom` via react-router). The same call on the head's admin lock reports `{}`. So the instrument can see these advisories, and it no longer finds them at the head.
- I did not run the advisories' exploits. Reachability: the portals use `BrowserRouter` only, with no data router and no SSR, which matches the seat's read.

**Q5. The 16-cell suite** (`Blockchain/Dev/scripts/__tests__/react_router_v7_portals.test.sh`).
- At the head: 16 of 16, rc 0, `SCANNED files=167 locks=4`.
- **Red reproduced:** I ran the head's suite against a `git archive` of develop 14ac61bd (the three portals' src, manifests, the 4 locks and the baseline). The real-tree cell fails, and the extracted checker prints R0 x3, R1 x3 (9+11+3 = 23 files), R2 x6, R3 x8 and R4 x2, with nothing for G1 to G5. That is red for the right reason: real `react-router-dom` imports, manifests, locks and baseline rows, not a crash or a wrong root.
- **My planted defects**, on scratch copies of the head, with the plant asserted present before each run:
  - (P3) a double-quoted `import { Link } from "react-router-dom"` appended to verifier `App.tsx`: R1 red, **caught**.
  - (P1) `"optionalDependencies": {"react-router-dom": "^6.30.4"}` in verifier `package.json` (grep confirms 1 hit): checker reports clean, **missed**.
  - (P2) `src/legacy-router.cjs` containing `require("react-router-dom")` in admin: clean, **missed**.
  - See F4. I did not repeat the seat's 32 tamper replays. The 14 built-in mutants all bite at the head (included in the 16).

**Q6. Merge tree.**
- `merge-tree 14ac61bd 258e049a` gives rc 0, tree 28bfa417d82d.
- I then simulated the merge locally (commit 4101e8060d9e, never pushed) and ran merge-tree for **all 11** PRs against develop and against develop+2091. PR heads were fetched at the start: 575 7d32d8ae, 635 6cbc298f, 639 2069d852, 649 1d9198ac, 945 264098fc, 946 41cc5209, 947 d68b9d79, 948 2f881c24, 949 29d8bfa9, 1360 d0e99f18, 1965 fb0a2bee.
- Results: 635, 639, 945, 946, 947, 1360 and 1965 are clean before and after. 575 (1 file, `services/kyc/package.json`), 649 (15), 948 (6) and 949 (1, root lock) conflict before and after, **with identical conflicted-file lists**. **This PR adds no conflict to any of the 11.**
- For the 7 clean merges, I ran the suite's checker on the merged tree (develop + 2091 + PR): clean for all 7. No shared-path PR reintroduces react-router-dom through a textual auto-merge.
- Shared paths: all 11 share the root lock. 639, 947 and 948 also share portal `package.json` files.
- Not done: `npm ci` on any merged tree, to test whether an auto-merged root lock is still installable, and the 11-PR merge-tree on the late develop a2c3ec7f.

**Q7. PR body and ticket comment 2083ebbe.** I read these from the seat's own records (`5_Project_History/2026-11-08_seatR-88th/push/pr_body_ks528.final.md`, `comment_ks528.md`, and records `pr_record_ks528.json` body_sha1 8af526fe and `comment_record_ks528.json` body_sha1 4cd2a558). I did **not** read the live PR or Linear text (no API calls). Every claim below that I checked holds at this head, except as noted:
- **True, re-measured by me:**
  - 23 import lines (admin 9, issuer 11, verifier 3), 34 files, one commit.
  - The per-lock delta.
  - 14 lines deleted from the baseline, 4 rows remain.
  - Audit gate 4/4 with no CLEANUP line; locks rc 0; contract 62/62.
  - Issuer vitest 15 of 15.
  - The suite is 16 of 16, and red on develop with R1 23 / R2 6 / R3 8 / R4 2.
  - Merge-tree with develop is clean.
  - 575, 649, 948 and 949 already conflict on their own.
  - The 52 navigation targets.
  - The two rows lapse 30 Nov 11:00 AEDT (consistent with `isLapsed`, as the baseline text records).
  - GHSA-jjmj was removed by #1214 (`ba4016fb` on develop).
- **True when written, stale now:** "develop is 9ede880539f3". Develop is now a2c3ec7f. The body's "NOT repeated" merge-tree claim is now repeated by this gate, and it holds.
- **Not verified by me** (registry or network claims): "the registry's latest for react-router is 8.5.1"; "GHSA-qwww-vcr4-c8h2 high, >=7.12.0 <7.18.2"; "v8 drops react-router-dom"; "bumping react-router-dom alone fails with MISSING_EXPORT"; and the eslint figures (0 errors, admin 58 warnings, issuer 11).
- **Incomplete:** "no intended behaviour change" / "0 steps differ" / "0 differences" (F2).
- **Narrowing:** stated plainly enough. The comment's third paragraph begins "This PR does not meet the 'Done when' text of the 2026-08-14 comment as written". It names the three gaps (react-router rather than react-router-dom 7.x, no demo verification, two rows not three, with the reason). The BLUF says "this ticket stays In Progress", and the PR title is `Refs`, not `Fixes`. I do not think a reader would take the ticket as done.

## Findings

**F1. Minor. Issuer: in-app navigation to a not-yet-loaded page no longer shows the loading fallback. The URL changes while the old page stays on screen.** MEASURED AT RUNTIME, replicated twice.
- Location: `Blockchain/Dev/frontend/issuer/src/App.tsx:81` (`<Suspense fallback={<LoadingFallback />}>` around `<Outlet />`), with the lazy routes at `:27-41` and the router at `issuer/src/main.tsx:41`.
- FAIL condition, set before the run: on the v7 build, a sidebar navigation to an unloaded lazy route shows something different from the v6 build during the chunk load.
- HOW:
  1. Load the issuer preview, authenticated (mocked refresh/me), on `/settings`.
  2. Delay only the `DocumentList-*.js` chunk by 2000 ms.
  3. Click the visible sidebar "Documents" button (the app's own `navigate()`).
  4. Sample the body every 200 ms for 1.6 s.
- Result:
  - **develop (v6.30.6):** `/documents` with "Loading..." fallback at every sample.
  - **head (v7.18.5):** `/documents` in the address bar, with the old Settings content and no fallback at every sample.
  - An undelayed run shows the same split: develop briefly shows the fallback, head never does.
- Cause: the installed `CHANGELOG.md` §7.0.0 ("Remove `future.v7_startTransition` flag") and `docs/explanation/react-transitions.md:29` ("In v7, that became the default behavior and all router state updates are currently wrapped in `React.startTransition`"). Develop never enabled the flag.
- Oracle: **H**istory (v6 behaviour) and **U**ser desires. On a slow link, a user who clicks gets no feedback, while the URL already says they are elsewhere. An expert in a hurry will click again.
- Blast radius: the issuer only (12 lazy routes), on first visit per route per session. No data, auth or security effect. Admin and verifier have no `lazy`/`Suspense`.
- Fix-shape for the owner to choose (READ ONLY, not measured):
  - (a) accept it and say so in the PR body and ticket comment; or
  - (b) `<BrowserRouter useTransitions={false}>` in `issuer/src/main.tsx`, the opt-out documented at `react-transitions.md:41-56`; or
  - (c) keep transitions and add a pending indicator.
- Regression test to add: a browser cell with a delayed lazy chunk that asserts whatever the chosen behaviour is.

**F2. Minor. The client-readable text says "no intended behaviour change" and "0 differences" without the F1 case.** READ ONLY (records), checked against F1.
- The PR body's lead paragraph says "a dependency migration with no intended behaviour change". Its Test Evidence, and the ticket comment 2083ebbe, say a 33-step walk showed "0 differences" / "0 steps differ".
- Both do list `v7_startTransition` as UNMEASURED. The flow fragment admits that the issuer sidebar steps used a history push and not the app's own `navigate()`, which is exactly the path where F1 shows.
- So the text is accurate for what was measured, but a client reader gets "no behaviour change" first and the caveat last.
- Fix-shape: replace the UNMEASURED line with F1's measured result and its disposition.

**F3. Nit. The 23 inline comments overstate what v6 kept in react-router-dom.** MEASURED against the installed react-router@6.30.6 `dist/index.d.ts` (develop build).
- Each changed import line carries this comment, e.g. `admin/src/App.tsx:1`: "react-router 7 exports these (v6 kept them in the react-router-dom package, dropped for v8)".
- But react-router 6.30.6 already exported `Routes`, `Route`, `Navigate`, `Outlet`, `useNavigate`, `useLocation` and `useParams` (its export list, line 14). Only `BrowserRouter` and `useSearchParams` were DOM-package-only.
- "dropped for v8" is not verified here.
- Harmless at runtime. It is shipped source text, repeated 23 times.

**F4. Low. The suite's checker misses two shapes of react-router-dom coming back.** MEASURED (planted P1 and P2 above).
- R2 reads only `dependencies` and `devDependencies` (checker line `const deps = { ...(pj.dependencies || {}), ...(pj.devDependencies || {}) }`), so `optionalDependencies`, `peerDependencies` and `overrides` are not scanned.
- The source walker matches `/\.(tsx?|jsx?|mjs)$/`, so `.cjs` and `.cts` files are skipped.
- Exposure is small in practice: a real install of react-router-dom lands in a regenerated lock, and R3 scans every lock at any depth. That cell is proven by the `m_lockdom` mutant.
- Fix-shape: widen R2 to all dependency maps plus `overrides`, and widen the walker's extensions. Regression test: two more named mutants (P1, P2).

**F5. Note, pre-existing (same on v6, not introduced by this PR).** MEASURED.
- Issuer and verifier have no catch-all route, so an unknown path renders an empty page with only the consent banner.
- Admin and issuer always land on `/` after login. A deep link is lost on the login round trip: `admin/src/pages/Login.tsx:28`, `issuer/src/components/Login.tsx:117`.
- Recorded so that nobody files these as KS-528 regressions.

## What was NOT tested

- The images on node:24-alpine. I built on Node v26.8.1 only, in a reproduction of the Docker layout, not in Docker.
- The nginx-served paths and the `sed` URL rewrite in the Dockerfiles.
- Any live platform, gateway, real login, real refresh cookie, or the four platform suites. There was no stack, and docker is excluded by the common rules.
- eslint (it needs the root workspace install). The seat's eslint figures are unverified.
- The dev-host build layout on develop, as a control for the tsc failures noted under Q1.
- The issuer's own `navigate()` calls beyond the sidebar, profile menu and login. Verifier post-verify navigation with real `location.state` (I opened `/verify/result` without state only).
- Keyboard, accessibility and mobile-viewport navigation.
- The `useTransitions={false}` fix-shape in F1. Not built, not run.
- Registry facts in the PR body (latest 8.5.1, GHSA-qwww range) and the claim that v8 drops react-router-dom.
- The seat's 32 planted tampers (not replayed). The full `test:shell` run (only the new suite and `docs_fragments.test.sh`, the latter 80 passed, 1 SKIP: F4 needs `systemTest/` support files outside my sparse checkout).
- `npm ci` on any merged tree. The 11-PR merge-tree on the end-of-session develop a2c3ec7f (I did merge-tree on 14ac61bd for all 11, and on a2c3ec7f for 2091 alone).
- The live PR body and Linear comment. I read them from the seat's records, not from the APIs.

## My own conduct

- Clone: `/private/tmp/g255`, a blobless clone with sparse checkout. Remote and `core.sshCommand` were read from the shared checkout. That checkout was only read, never fetched or written. Final size **1.8 GB** (mostly 6 portal `node_modules` and the dist builds, in `_dock.*` and `_dockdev.*` staging folders). It is on the boot volume, so DevMASTER was untouched: 24 GiB free at the start, 23 GiB at the end. Per the QA template's no-rm rule, I left it in place and removed nothing.
- **Deviation 1:** the Wednesday hook `pretooluse_no_cd.sh` refused `git merge-tree` in `/private/tmp/g255` (a write verb outside WEDNESDAY). Following the hook's own instruction, I ran merge-tree and one local `commit-tree` (the never-pushed merge simulation 4101e806) in a `--shared` bare clone under this session's scratchpad: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e9a953f3-ed71-443f-a697-01394a1dde48/scratchpad/g255_mt` (28 MB including merged-tree extracts). That is outside "gate folder plus clone". I name it here.
- **Deviation 2:** network use went beyond git fetch. The commission's Q1 ("install from its lock") and Q4 ("run the repo's audit check as preflight would") need the npm registry: 6 `npm ci` runs, 1 `scripts/audit` `npm ci`, the audit gate, audit-locks, and 2 `npm audit` calls. Nothing was posted anywhere. I made no GitHub or Linear API calls.
- Inside the clone I moved each portal's `node_modules` into staging with `mv`, not `rm`. The suite under test deletes its own `mktemp` dir by its own `trap`; that is the repo's code, not mine.
- Six `vite preview` servers on 127.0.0.1:4301-4303 and 4311-4313 (my processes) were stopped at the end; I confirmed 0 remain.
- Load was 13.08 at boot, before I started anything, and I waited before installs. During my work it ran 4.6 to 7.3, under 8 throughout my builds and runs.
- I did not use `cd`. I made no change to the target repo, PRs, tickets or the shared checkout.
