# react-router v6 -> v7 migration: sizing for KS-528 rows 11 and 12

Sizing agent for Wednesday (read-only). Written 2026-09-17 18:57 AEST.
Pin: `origin/develop` = `81ee4b729e86a645fc9098aafa1aaf39035a9950` (`git ls-remote` at 18:45:49 and again at 18:56:00, unchanged).
Ruling this serves: Kam, 18:31:25 AEST, card `secuura-audit-rows-react-router-v7-migration`: "Commission the v7 migration AND date both rows to its planned landing (recommended)".

## BLUF

1. **Affected:** 3 portals only: `frontend/admin`, `frontend/issuer` and `frontend/verifier`, plus the root workspace lock. No other manifest, lockfile or shared package declares or imports react-router.
2. **Size: 1 PR, 1 Claude-seat session, plus 1 buffer session for a gate fix round (1 to 2 sessions).** All three portals use only declarative v6 APIs: 23 import lines, no data router, no `<Link>`, no relative paths. A trial swap to react-router 7.18.4, which only rewrote imports, built all 3 portals with no errors. The issuer's 12 unit tests passed, and its bundle-size check passed.
3. **Can it land before Wed 30 Sep 10:00 AEST?** The code can. The schedule cannot promise it. The PR must rewrite the root lock, and only one root-lock PR may be open at a time. Seat B's 6 queued root-lock PRs all have rows lapsing on 24 or 30 Sep. The earliest landing is PR-5's slot (about 25 to 28 Sep), which leaves no slack.
4. **PROPOSED planned landing (for Wednesday to rule): Thu 1 Oct 2026. Rows 11 and 12 re-dated to `expires: "2026-10-02"`, which lapses Fri 2 Oct 10:00 AEST.** Reasoning: the migration takes the root-lock lane no later than right after PR-8, the last Sep-30 PR. That leaves about 1.5 working days for the tier-1 gate, the real-browser pass on 3 portals and one fix round. It also avoids Mon 5 Oct, which I believe is Labour Day in NSW, ACT and SA. I did not check which state's holidays apply.
5. **What the PR clears:** rows 11 (GHSA-wrjc) and 12 (GHSA-337j) together, only once the root tree and all 3 standalone locks are on 7.x. Splitting the work per portal clears nothing until the last portal lands. It also clears row 13 (GHSA-jjmj), because it removes react-router-dom.

---

## 1. What depends on react-router (at the pin)

Instrument: `git grep -n -E '"react-router(-dom)?"' <sha> -- '*package.json'`, which found 3 hits (its own control). Lockfiles were checked with `git grep 'node_modules/(react-router|react-router-dom|@remix-run/router)"'` across all 45 `package-lock.json` at the pin. The same-command control, `"node_modules/react":`, matched in 9 locks. Versions come from parsing the lock JSON.

| App / lock | Declares | Resolved | Class |
|---|---|---|---|
| `Blockchain/Dev/frontend/admin` (manifest + standalone lock) | `react-router-dom ^6.30.4` | rrd 6.30.4, react-router 6.30.4, @remix-run/router 1.23.3 | runtime |
| `Blockchain/Dev/frontend/issuer` (manifest + standalone lock) | `react-router-dom ^6.30.4` | same | runtime |
| `Blockchain/Dev/frontend/verifier` (manifest + standalone lock) | `react-router-dom ^6.30.4` | same | runtime |
| `Blockchain/Dev/package-lock.json` (root workspace `packages/* services/* frontend/*`) | none directly. Dependents: `frontend/admin`, `frontend/issuer`, `frontend/verifier` | **one hoisted copy** at `node_modules/react-router` 6.30.4 / rrd 6.30.4 / @remix-run/router 1.23.3 | runtime |

- **Nothing else uses it.** A repo-wide `git grep` for `from 'react-router…'` or `require('react-router…')` (lockfiles excluded) found only the 3 portals (9, 11 and 3 files) and one code sample in `Blockchain/Dev/docs/TESTING.md:332`. `frontend/shared`, `packages/shared`, `website`, `demo-overlay`, `outlook-addin`, `status`, `gmail-addon`, `mobile` and systemTest have no react-router dependency.
- **Other versions in all 4 locks:** react / react-dom 19.2.7; TypeScript 5.9.3. The standalone locks resolve vite 8.1.4, and the root lock nests vite 8.2.1 under each portal. The portal tsconfigs set `moduleResolution: "bundler"`. The Dockerfiles (`frontend/{admin,issuer,verifier}/Dockerfile`) use `node:24-alpine` and run `npm ci` against the **standalone** lock.

## 2. The v6 API surface in use

Frame: `Blockchain/Dev/frontend/{admin,issuer,verifier}/`, all `*.ts *.tsx *.js *.jsx` at the pin, including tests and configs. Instrument: `git grep -n -P <regex> <sha>`, one per construct (script at `scratchpad/count.sh`; hit files at `scratchpad/hits/`).
**Positive controls:**
- `navigate(` totals 14 + 26 + 8 = **48**. Seat B's independent count was also 48.
- `BrowserRouter` totals **9** lines (3 per portal). Seat B also counted 9.

Every hit behind a non-zero count below was read by eye.

| Construct | admin | issuer | verifier | Evidence (file:line) |
|---|---|---|---|---|
| Files importing `react-router-dom` | 9 | 11 | 3 | e.g. `admin/src/App.tsx:1`, `issuer/src/main.tsx:10`, `verifier/src/App.tsx:16` |
| Files importing `react-router` (core) directly | 0 | 0 | 0 | All 23 import lines name `react-router-dom`, read by eye. My first regex, `from .react-router.`, was too broad (`.` matched `-`), so I discarded its count. |
| `<BrowserRouter>` | 1 (`basename="/admin"`, `App.tsx:93`) | 1 (no basename, `main.tsx:40`) | 1 (`basename="/verify"`, `App.tsx:34`) | |
| `<Routes>` | 2 (`App.tsx:34`, `:49`: two alternative top-level trees chosen by an auth branch, not nested) | 1 (`App.tsx:116`) | 1 (`App.tsx:35`) | |
| `<Route element=>` | 18 | 16 (one pathless layout route at `App.tsx:126` with `<Outlet/>` at `:81`, plus an `index` route) | 3 | |
| `useNavigate` / `navigate(` calls | 6 / 14 | 7 / 26 | 2 / 8 | **All 48 targets are absolute** (`'/…'` or `` `/…${id}` ``). None are relative or `..`, and none use `navigate(-1)`. |
| `navigate(…, { state })` | 0 | 0 | 4 (`VerifyPage.tsx:90,140,142,144`) | read by `ResultPage.tsx:76` via `useLocation` |
| `useParams` | 3 | 2 | 1 | `admin/pages/platform/ClientDetail.tsx:51`, `issuer/components/DocumentDetail.tsx:146`, `verifier/components/ResultPage.tsx:74` |
| `useSearchParams` | 1 (`ClientDetail.tsx:53`) | 0 | 0 | |
| `useLocation` | 2 | 2 | 1 | `Layout.tsx`, `PolicyDocs.tsx` pathname reads |
| `<Navigate>` | 2 (`App.tsx:41,66`) | 2 (`App.tsx:74,122`) | 0 | |
| `<Outlet>` | 0 | 1 | 0 | |
| Splat routes | 2, both **single-segment** `path="*"` (`admin/App.tsx:41,66`) | 0 | 0 | 0 multi-segment splats (`x/*`) |
| Router `<Link>` / `<NavLink>` / `relative=` | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | issuer's 4 `<Link …/>` hits are the lucide-react icon, e.g. `DocumentDetail.tsx:366` |
| NavLink `className`/`style` functions | 0 | 0 | 0 | The `isActive` hits (39 / 26) are domain fields and local variables, not NavLink. Samples read: `admin/src/__mocks__/documentTypesData.ts:15`, `admin/components/Layout.tsx:169` |
| `createBrowserRouter` / `RouterProvider` / data routers | 0 | 0 | 0 | |
| loaders / actions / `useLoaderData` / `useFetcher` / `useNavigation` / `errorElement` | 0 | 0 | 0 | The broad regex hit 18 / 33 lines. All were domain `action:` fields (e.g. `admin/pages/AuditLogs.tsx:26`, `admin/services/api.ts:433`), read by eye. |
| `json` / `defer` imports | 0 | 0 | 0 | |
| `useBlocker` / `unstable_*` / `UNSAFE_*` / `usePrompt` | 0 | 0 | 0 | |
| Future flags already set (`v7_*`, `future={`) | 0 | 0 | 0 | |
| `React.lazy` / `lazy(` | 0 | 12, **all at module scope** (`App.tsx:26-40`), inside `<Suspense>` at `App.tsx:80` | 0 | |
| `<Form>` / `useSubmit` / `ScrollRestoration` / `generatePath` / `matchPath` / `useRoutes` / `useMatch` | 0 | 0 | 0 | |
| SSR: `StaticRouter` / `renderToString` / `hydrationData` | 0 | 0 | 0 | |
| Build config naming react-router | 0 | 1: `vite.config.ts:124` manualChunks `id.includes('/react-router')` → `react` chunk (still matches `node_modules/react-router/` in v7) | 0 | |

## 3. Upgrade guide: breaking changes mapped to the counts

**Source read this session:** "Upgrading from v6", React Router **v7.18.4** docs.
- Page: `https://reactrouter.com/v7/upgrading/v6` (HTTP 200, `<title>Upgrading from v6 v7.18.4 | React Router`), fetched 18:47 AEST.
- Markdown source: `https://raw.githubusercontent.com/remix-run/react-router/react-router@7.18.4/docs/upgrading/v6.md`, read in full at 18:47:22 AEST.
- `https://reactrouter.com/upgrading/v6` now returns **404**. The site's main docs are for **v8**: npm `latest` = **8.4.0**, and `version-7` = 7.18.4.

The guide's own framing is "The v7 upgrade has no breaking changes if you have enabled all future flags." Minimum versions are node@20 and react / react-dom@18.

| Guide step | Applies when | Measured here | Code change needed |
|---|---|---|---|
| Minimums node@20, react@18 | always | react 19.2.7 in all 4 locks; Dockerfiles `node:24-alpine`; local trial node v24.7.0 | none. The root `engines.node >=18` is stale but not enforced. vite 8 already needs ≥20.19. |
| `v7_relativeSplatPath` | multi-segment splat routes (`dashboard/*`) with relative links below them | 0 multi-segment splats; 2 single-segment `*` (admin); 0 `<Link>`; 0 relative navigates (48 of 48 absolute) | **none** |
| `v7_startTransition` | always (router state updates now use transitions); code breaks only with `React.lazy` *inside* a component | issuer: 12 `lazy()` calls, all at module scope; admin and verifier: 0 | **none**. **Behaviour change:** in the issuer, navigating to a lazy route inside `<Suspense>` may keep the old screen until the chunk loads instead of showing `LoadingFallback`. This is not a compile error, and only a browser pass can confirm it. |
| `v7_fetcherPersist`, `v7_normalizeFormMethod`, `v7_partialHydration`, `v7_skipActionErrorRevalidation` | `<RouterProvider>` / `createBrowserRouter` only (guide: "you can skip this") | 0 data routers | **none (skip)** |
| Deprecation: `json` / `defer` | loaders | 0 | none |
| Install v7; replace `react-router-dom` with `react-router` | always | 3 manifests | 3 `package.json` edits, 3 standalone locks, root lock |
| Update imports `react-router-dom` → `react-router` | always | 23 import lines (admin 9, issuer 11, verifier 3) | mechanical, 23 one-line edits |
| DOM deep import `react-router/dom` for `RouterProvider` / `HydratedRouter` | those two only | 0 | none |

**Pinning trap (measured):** the guide says `npm install react-router@latest`. Today that resolves to **8.4.0**, which needs node ≥22.22 and react ≥19.2.7 and is a *further* major version. `react-router-dom@latest` resolves to 7.18.4. The PR must pin **`react-router@^7.18.4`**. Advisory check: GitHub `/advisories?affects=react-router@7.18.4` returns **0**. The control, `affects=react-router@6.30.4`, returns 2 (wrjc, 337j).

## 4. Test surface

| App | Unit test files | Touch routing? | `test` script | Builds without docker? | Browser e2e naming the portal (all need a running stack; gateway `localhost:6882`) |
|---|---|---|---|---|---|
| admin | 0 | n/a | none (`build`, `lint`, `dev`, `preview`) | **yes**. `tsc && vite build` with the Dockerfile layout (below) | `tests/e2e`: `admin-portal.admin.spec.ts`, `sysadmin-exhaustive.admin.spec.ts`, `recruitment/admin-config.admin.spec.ts` |
| issuer | 2 (`src/__tests__/blockchain-card.test.tsx`, `provenance-timeline.test.tsx`), 12 tests | **no** (0 router mentions) | none. vitest is a devDep and runs via `npx vitest run`. There is also `check:bundle`. | **yes** | `tests/e2e`: `issuer-portal.issuer.spec.ts` |
| verifier | 0 | n/a | none | **yes** | `tests/e2e`: `verifier-portal.verifier.spec.ts` |

- **Router mentions in tests and config.** Instrument: `git grep -n -i router` over `*.test.* *.spec.* *__mocks__* *setup* *vitest.config* *vite.config* *jest.config* *eslint*`. The control is that it hit `packages/shared` Express-router tests and `issuer/vite.config.ts:124`. Result: 0 in any portal test.
- **e2e counts.** `tests/e2e` has 5 of 48 spec files tagged to a portal project (`.admin|.issuer|.verifier.spec.ts`), and 30 of its files call `page.goto`. `tests/e2e-v2` has 12 browser specs (tiers 2–4: `tier2-smoke/portals|login|…`, `tier3-e2e/*`, `tier4-a11y/{admin,issuer,verifier}.spec.ts`) plus 12 API specs. None of these can run without the stack.
- **No routing unit tests.** No test anywhere exercises a route, a redirect or a param in-process. The routing coverage is the browser e2e plus the gate's real-browser pass.

## 5. Blast radius

- **Root lock hoisting (measured from the root lock JSON).** The three portals share **one** hoisted `node_modules/react-router`. Moving one portal alone to v7 either nests a second copy or leaves v6 hoisted for the others. **Rows 11 and 12 come out only when all 3 standalone locks *and* the root tree are clean** (legs 6 and 7 per the KS-528 06:41Z comment). So a per-portal split buys nothing on the audit rows.
- **Root-lock lane.** Seat B's approved order is #1022 → PR-3 → PR-7 → PR-4 → PR-5 → PR-6 → PR-8, with "one root-lock PR open at a time". The migration is a root-lock PR, so it has to join that lane.
- **Overlap with PR-5 (row 13, rrd 6.30.6).** PR-5 touches the same 3 manifests and 4 locks. The migration removes `react-router-dom`, and react-router 7.18.4 is outside GHSA-jjmj's react-router range (≥7.9.6 ≤7.12.0). So **the migration clears row 13 too and makes PR-5 redundant**. Stale baseline rows are advisory only: `audit-gate.mjs:201-211` and `audit-locks.mjs:292-297` report CLEANUP and do not fail.
- **Overlap with PR-8 (ip-address override).** PR-8 touches `frontend/issuer/package.json`, the issuer lock and root. The two must not be open at the same time.
- **Overlap with the re-date.** The re-date of rows 11 and 12 (Seat B, in `scripts/audit/audit-baseline.json`) must merge *before* the migration PR, which deletes those rows.
- **Dependency delta (trial).** Removes `react-router-dom` and `@remix-run/router`. Adds `cookie` 1.1.1 and `set-cookie-parser` 2.7.2. No react, vite or TypeScript bump is required.
- **Bundle delta (trial, vite build output):**
  - verifier `index` chunk: 285.31 → 293.81 kB gzip (+8.50)
  - admin: 192.60 → 200.48 kB gzip (+7.88)
  - issuer `react` chunk: 63.11 → 71.49 kB gzip (+8.38)
  - issuer `check:bundle` eager total: 242.0 → 249.7 KB against a 450 KB budget, still **OK**.
- **Lock regeneration drift (trial).** A host `npm install` (npm 11.5.1, darwin) on the issuer lock dropped 28 package entries: `@rollup/rollup-*` platform binaries, `@emnapi/runtime` and `@remix-run/router`. It added 2. That is the same host-drift class Seat B already regenerates inside the bounded container, so the PR's locks must be regenerated there, not on a host.

## 6. PR plan

**Recommended: 1 migration PR (call it MIG-1), TIER 1 with a real-browser pass, built by one source-scope seat.**

| Order | PR | Files (partition) | Checks in the PR | Clears |
|---|---|---|---|---|
| 0 (now, before 30 Sep 10:00 AEST) | Re-date: Seat B's own instruction | `Blockchain/Dev/scripts/audit/audit-baseline.json`, rows GHSA-wrjc and GHSA-337j only: `expires` → the ruled date; reason names KS-528 and the planned landing | `audit:gate`, `audit:locks`, `audit:contract` | none (defers 11 and 12) |
| 1 | **MIG-1: react-router v7** | `Blockchain/Dev/frontend/admin/{package.json,package-lock.json,src/**}` (9 files), `…/issuer/{…}` (11 files), `…/verifier/{…}` (3 files), `Blockchain/Dev/package-lock.json` (root, container regen), `scripts/audit/audit-baseline.json` (delete rows 11, 12, and 13 if PR-5 has not landed) | 3× `tsc && vite build` (Dockerfile layout), issuer `vitest run` + `check:bundle`, `audit:gate` + `audit:locks` green with the rows removed, repo-wide `git grep react-router-dom` = 0 outside docs, tier-1 gate real-browser pass on all 3 portals (login, deep-link reload under `/admin` and `/verify`, `documents/:id`, verifier result via navigate state, the `*` redirects, an issuer lazy-route navigation to observe the transition change) | **GHSA-wrjc (row 11), GHSA-337j (row 12), GHSA-jjmj (row 13)** |
| optional follow-up | `TESTING.md:332` sample import | `Blockchain/Dev/docs/TESTING.md` | none | none |

- **Seats never share files.** MIG-1 owns `frontend/{admin,issuer,verifier}/**` and takes the root lock only in its lane slot. Seat B keeps the lane and `audit-baseline.json` until the re-date merges, then hands the row deletion to MIG-1.
- **No separate future-flags PR.** The guide's flag-first path would change 0 lines of app code here (§3). The only real behaviour change, the startTransition one, is covered by the browser pass.
- **Option for Wednesday.** A src-only PR could turn on `future={{ v7_startTransition: true, v7_relativeSplatPath: true }}` on v6 now, without using a root-lock slot, to browser-gate the transition change early. It costs +1 session. The `future` prop may then need removing at v7; that is **untested**.
- **Lane placement (Wednesday to rule).**
  - (a) MIG-1 takes **PR-5's slot** and PR-5 is dropped. Earliest landing is about 25 to 28 Sep, with no slack before the 30 Sep lapse.
  - (b) MIG-1 goes **after PR-8**. It lands about 30 Sep to 1 Oct, which is the basis for the proposed date.
  - Under (b), PR-5 stays in place as cheap cover for row 13.

**Sessions:** MIG-1 build and local checks is 1 session. The tier-1 gate with the browser pass is the gate's own session. One fix round needs +1 builder session. **Total 1 to 2 builder sessions.**

## 7. Risks

1. **Lane contention (highest).** The date depends on Seat B finishing 6 root-lock PRs by 30 Sep. Their speed is not measured, and a slip pushes MIG-1 back day for day.
2. **The startTransition behaviour change in the issuer.** It is invisible to `tsc`, the build and the 12 unit tests; only a browser shows it.
3. **Installing `@latest`.** It would pull v8 (node ≥22.22). Pin `^7.18.4`.
4. **Host lock regeneration.** It drops platform optional deps (§5), so regenerate in the container.
5. **No in-process routing tests.** A mis-edit in routing passes every local check, which is why the browser pass is required, not optional.
6. **Lapse semantics.** `isLapsed` treats a date as dead on that UTC date. `"2026-10-02"` lapses at **Fri 2 Oct 10:00 AEST**. If MIG-1 slips past Thu 1 Oct, the preflight refuses pushes touching `Blockchain/Dev` unless the rows are re-dated again.
7. **Unreachability leads.** Both are leads, not proof (Seat B, KS-528 08:35Z comment): 0 navigate targets built from input (wrjc), and 0 SSR or hydration APIs (337j). This sizing re-confirms the counts behind them, 48 absolute navigate targets and 0 SSR, but not the react-router internals.

## 8. Audit-row consequence

| Row | GHSA | Package / range → fix | Cleared by |
|---|---|---|---|
| 11 | GHSA-wrjc-x8rr-h8h6 (CVE-2026-53669, medium, open redirect via backslash) | react-router ≥6.0.0 <7.18.0 → 7.18.0 | MIG-1 only, once all 4 locks are clean |
| 12 | GHSA-337j-9hxr-rhxg (CVE-2026-53666, medium, deserializeErrors constructor injection) | react-router ≥6.4.0 <7.18.0 → 7.18.0 | MIG-1 only, same condition |
| 13 | GHSA-jjmj-jmhj-qwj2 (CVE-2026-53668, medium) | rrd ≥6.30.2 ≤6.30.5 → 6.30.6; react-router ≥7.9.6 ≤7.12.0 → 7.13.0 | PR-5 (6.30.6) **or** MIG-1 (rrd removed, rr 7.18.4 out of range) |

Instrument: GitHub REST `GET /advisories/<GHSA>` at 18:46 AEST, unauthenticated. The baseline rows were read from `audit-baseline.json` at the pin: 37 accepted entries, and these 3 carry `ticket: KS-528`, `decidedAt: 2026-07-29`, `expires: 2026-09-30`.

## 9. Linear (read-only)

- **KS-528** — "Frontends: react-router v6 → v7 migration…". State Backlog, priority 3, no estimate, no due date, assignee kamil.kreiser@secuura.ai, project "Dependency and Version Currency", no relations.
  - **Description:** scope is the 3 portals, verified end-to-end, with the 3 GHSA rows removed in the same PR. It also names a "`RouterProvider` shape" change; **measured: 0 RouterProvider**, so that part of the scope does not apply.
  - **3 comments**, sorted client-side:
    - 2026-08-14: acceptance criteria. rrd@7.x in all 3 portals; e2e local; rows removed and `audit:gate` + `audit:locks` green.
    - 2026-09-17 06:41Z: lapse measurement, all 3 rows present.
    - 2026-09-17 08:35Z: Kam's ruling relayed, "nothing re-dated today".
  - The acceptance criteria say `react-router-dom@7.x`. The guide says use `react-router`. MIG-1 should satisfy the intent (off the vulnerable range, rows removed) and say so on the ticket.
- **Other tickets.** None found.
  - Instrument: `issues(filter: title OR description containsIgnoreCase)` and `comments(filter: body containsIgnoreCase)` for `react-router`, `react router`, `RouterProvider`, `createBrowserRouter`, `KS-528`.
  - Every hit was KS-528 or its own comments. `react router` gave 0; `KS-528` gave 0 in other tickets.
  - `searchIssues` (fuzzy, 5 terms, first 50) returned unrelated noise, listed in `scratchpad/linear.out`.

---

## FOUND

- Only the 3 portals and the root lock carry react-router: 6.30.4 runtime everywhere, one hoisted copy in the root.
- The API surface is small and purely declarative: 23 imports, 3 `BrowserRouter`, 4 `<Routes>`, 37 `<Route>`, 48 absolute `navigate(` calls, 0 `<Link>`/`<NavLink>`, 0 data routers, 0 future flags, 0 multi-segment splats, and 12 module-scope `lazy()` in the issuer.
- Every breaking-change step in the v7.18.4 upgrade guide maps to **zero app-code changes** apart from the import rewrite and the package swap. The one behaviour change is startTransition, which matters in the issuer.
- npm `latest` for `react-router` is now **8.4.0**, so the guide's `@latest` command would overshoot to v8.
- The migration clears rows 11 and 12, and row 13 too. Per-portal PRs clear nothing until the last one lands.
- A host lock regeneration drops 28 platform optional packages, so regenerate in the container.

## TESTED

Own clone, own temp dir: `scratchpad/rr2.ZIuc/`, script `scratchpad/trial2.sh`, log `scratchpad/trial2.out`, 18:51:53 → 18:55:03 AEST. For each portal I copied it to `<tmp>/<app>/app`, vendored `frontend/shared` to `app/vendor/shared` and set `SHARED_DIR=./vendor/shared/src`, mirroring the Dockerfile without docker.

| Step | verifier | admin | issuer |
|---|---|---|---|
| `npm ci --ignore-scripts` (standalone lock) | rc 0 | rc 0 | rc 0 |
| **Control:** `npm run build` at v6 (the pin) | rc 0 | rc 0 | rc 0 |
| Control: `npx vitest run` at v6 | n/a | n/a | rc 0, 2 files / 12 tests passed |
| Control: `npm run check:bundle` at v6 | n/a | n/a | rc 0, 242.0 KB / 450 |
| `npm uninstall react-router-dom` + `npm install react-router@7.18.4` | rc 0 / 0 → rr 7.18.4, no rrd, no @remix-run/router | same | same |
| `sed` import rewrite (the guide's command); rrd importers after | 0 (3 now import `react-router`) | 0 (9) | 0 (11) |
| `npm run build` at v7 (`tsc` + vite) | **rc 0** | **rc 0** | **rc 0** |
| `npx vitest run` at v7 | n/a | n/a | **rc 0, 2 files / 12 tests passed** |
| `npm run check:bundle` at v7 | n/a | n/a | **rc 0, 249.7 KB / 450** |

- **The first trial was discarded, and why.** It built in the sparse monorepo layout. Its **v6 control failed** (rc 2: `../shared/src` could not resolve `zod` / `react` from a standalone install). Because the control failed, that run measured nothing. I stopped it and re-ran in the Dockerfile layout, where the control passes.
- **Other network reads:**
  - GitHub advisories API: 3 GHSA reads, plus the `affects=` queries with a 6.30.4 control.
  - npm registry metadata: react-router 6.30.4 / 7.18.4 / 8.4.0, react-router-dom dist-tags.
  - The guide page and its source.

## HOW (instruments and controls)

- **Pin and reads.** `git ls-remote origin develop` (twice), then `git show / git grep / git ls-tree <sha>` only, on the Secuura checkout. No fetch, checkout or worktree there. The one working tree is `git clone --shared --no-checkout` + sparse checkout + `checkout --detach <sha>` **inside my own `mktemp -d`**, run from a script file.
- **Construct counts.** `git grep -n -P` per construct over the frame in §2. Controls: `navigate(` = 48 and `BrowserRouter` = 9, both matching Seat B's independent counts. Every non-zero broad count was read line by line, and false positives were removed and named (domain `action:`, `isActive`, lucide `Link`, the over-broad core-import regex).
- **Lockfile facts.** JSON parse of the 4 relevant locks (`packages[...]` version, dev flags, `dependencies`). The dependents of react-router in the root lock were enumerated the same way.
- **Linear.** GraphQL POST with the `Authorization: <key>` header, no Bearer. The key was read by name inside `scratchpad/linear.py` and `linear2.py` and never printed. `comments(first:50)` was sorted client-side. Queries only.
- **Upgrade guide.** Fetched with curl and read in full (§3 has URLs and times). The v6-to-v7 guide is not on the site root any more (404). It is served under `/v7/…`, and its source is at the `react-router@7.18.4` tag.
- **Times.** From `date`: start 18:45:49, guide 18:47:22, trial 18:51:53–18:55:03, re-pin 18:56:00 AEST.

## NOT TESTED

- **Any browser run of any portal.** Not v6, not v7. The startTransition behaviour change, deep-link reloads under `basename`, `<Navigate>` redirects and verifier navigate-state are **unverified at runtime**. They need the stack (docker), which was out of scope.
- **The e2e suites.** `tests/e2e` (5 portal-project specs), `tests/e2e-v2` (12 browser specs) and systemTest were not run, because they need a running gateway.
- **The root workspace lock regeneration and the root-level `audit:gate` / `audit:locks` with rows removed.** Not run. The claim that the root tree clears is inferred from the advisory ranges plus the hoisting structure, not observed.
- **The container lock regeneration.** Only the host `npm install` was run, and it showed drift (§5).
- **`npm run lint`.** No ESLint config file exists in the three portal directories (per `ls-tree`), so it was not run.
- **The optional v6 future-flags PR, and whether v7 `BrowserRouter` rejects a leftover `future` prop.** Not tried.
- **react-router's internals.** Not read, so I have not confirmed that `deserializeErrors` is reachable only via hydration data. The GHSA-337j unreachability stays a lead.
- **Seat B's velocity through the root-lock lane, and which Australian state's public holidays apply.** Not measured. The proposed date rests on both.
- **The trial's scope.** The diffs were not reviewed as production code. The trial ran the guide's mechanical steps only, to size the work; it is not the migration.
