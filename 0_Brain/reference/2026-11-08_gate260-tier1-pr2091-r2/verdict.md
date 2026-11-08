**GO WITH NOTES**: PR 2091 (KS-528), head e5742b73748b6ae49f942f4bb8a797f4e076e5b2, gate 260, tier 1 compare, round 2 of 2

| PR | head | verdict |
|---|---|---|
| 2091 (KS-528, react-router 6 -> 7, round 2) | e5742b73748b6ae49f942f4bb8a797f4e076e5b2 | **GO WITH NOTES** |

No finding needs a ruling from Kam. All four round-1 findings are closed. What remains are three nits (N1 to N3), and none of them changes runtime behaviour. Severity is my call. Priority is not.

## Readings (origin, `git ls-remote` with the project deploy key)

| when (UTC) | develop | PR 2091 head |
|---|---|---|
| start 12:05:42Z | abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82 (matches the commission) | e5742b73748b (matches) |
| end 12:27:47Z | **765701307eb3ffb9cf98f380ffea3a51d8c70b74 (MOVED, 1 commit: KS-2081, 8 paths)** | e5742b73748b (unchanged) |

The head did not move, so this verdict stands. Develop moved by one commit. Its 8 paths share 0 with the PR's 34 and include no portal file, lock, manifest or baseline (control: the first moved path, `docs/openapi/secuura-api.yaml`, was listed). I re-ran Q6 in full on 765701307eb3; see below.

## BLUF

- **F1 is closed.** On my own builds, in a real browser, with a visibility predicate:
  - The head shows the issuer's "Loading..." screen and hides the old page in 8 of 8 held samples, in both directions (Settings to Documents and Documents to Settings), twice each, with and without a settle wait. That is sample for sample the same as develop on react-router 6.30.6.
  - The round-1 head 258e049aaf75 reproduces F1 in every run: 0 of 8 fallback, and the old page visible 8 of 8.
  - Admin and verifier are unaffected. Their production `dist` at the head is byte-identical to round 1's (0 differing files). The control is the issuer `dist`, which does differ (72 entries).
- **F3 is closed.** The new comment is true against the installed 6.30.6 and 7.18.5.
- **F4 is closed.** The six new mutants are red against the round-1 checker and green at the head. The suite passes 25 of 25 and leaves the real files unchanged by sha256. No new rule refuses anything on develop's real manifests.
- **F2 is closed in substance.** The live PR body and comment 2083ebbe no longer claim "no behaviour change". They state F1 and its reversal. One docs-fragment cell is now false (N1).
- **Merge state is unchanged.** The merge-tree is clean on both develop readings. None of the 11 PRs gains a conflict.

## Q1. F1: does the issuer show "Loading..." again on lazy navigation? (MEASURED AT RUNTIME)

**FAIL condition, set before the run:** on any held sample, the head differs from develop's v6 build in whether the fallback is visible or whether the old page's `<h1>` is visible.

**Builds.** All three are mine: `tools/build.sh`, the Dockerfile layout (portal in `app`, `frontend/shared` in `app/vendor/shared`, `SHARED_DIR=./vendor/shared/src`), `npm ci --offline` from each portal's own lock, `tsc && vite build`, Node v26.8.1 and npm 11.19.0. Each one was served by `vite preview` on 127.0.0.1.

| build | source | react-router on disk | ci / build |
|---|---|---|---|
| dev | develop abd044f63a9d | 6.30.6 + react-router-dom 6.30.6 | 0 / 0 |
| r1 | 258e049aaf75 (round-1 head) | 7.18.5, react-router-dom absent | 0 / 0 |
| head | e5742b73748b | 7.18.5, react-router-dom absent | 0 / 0 |

**Drive.**
- Chromium through the Playwright MCP.
- `/api/auth/refresh` and `/api/users/me` stood in (ISSUER_ADMIN). Every other `/api` call returned 404.
- One lazy chunk was held for 2500 ms, then I clicked the visible sidebar button (the app's own `navigate()`).
- 8 samples were taken 200 ms apart.

**Predicate.**
- "Shown" means `checkVisibility({checkOpacity, checkVisibilityCSS})` passes AND the element has a non-zero box. It is applied to the `<p>Loading...</p>` inside `<main>` and to the old page's own `<h1>` inside `<main>`.
- DOM presence is recorded separately and is not the predicate.
- Full table: `f1_drive_results.md`. Script: `tools/drive_f1_v2.js`.

| (fallback visible / old page visible), held, of 8 | dev v6 | r1 | head |
|---|---|---|---|
| Settings -> Documents (DocumentList held), settle 1 s, rep 1 and 2 | 8/0, 8/0 | 0/8, 0/8 | **8/0, 8/0** |
| Documents -> Settings (Settings chunk held), settle 1 s, rep 1 and 2 | 8/0, 8/0 | 0/8, 0/8 | **8/0, 8/0** |
| both directions, no settle | 8/0, 8/0 | 0/8, 0/8 | **8/0, 8/0** |

- During the hold, the Layout header shows the new page's name on dev and head and keeps the old name on r1. The path is the new one in all samples on all builds.
- Unheld: dev and head show the fallback in their first sample; r1 never shows it.
- After the chunk arrives, every run shows the new page and no fallback.
- The chunk is requested 0 times before the click and once after it. 0 pageerrors.
- The second direction (Settings chunk) goes beyond the builder's run, which covered Documents only.

**Controls.**
- **Planted:** on the head build, with no chunk held, I appended a `display:none` `<p>Loading...</p>` to `<main>` before the click. The predicate called it hidden in 7 of 8 samples (the 8th was the real fallback) while it stayed in the DOM to the end. So the instrument does not read DOM presence as "shown".
- **Natural:** in dev and head, the old `<h1>` is in the DOM but hidden in 8 of 8 held samples, while r1's old `<h1>` is visible. The predicate separates the two cases that the builder's run 1 confused.

**My own instrument error, kept and labelled INVALID** (`tools/drive_f1.js`). v1 waited for `getByRole('heading', {level: 1, name})`. That matched the Layout HEADER `<h1>`, which shows the route's name before the lazy page renders, so v1 clicked while the start page was still in its own fallback. All three builds, r1 included, then read 8 of 8 "Loading...". The control (r1) failed to separate, so I discarded the run and diagnosed it with a marked-node probe before v2.

**Mechanism, READ ONLY:**
- `BrowserRouterProps.useTransitions?: boolean` is typed in the installed 7.18.5 (`dist/production/index-react-server-client-BaaZU3sM.d.ts:2081`).
- `docs/explanation/react-transitions.md` documents the declarative opt-out. It says "This will stop the router from wrapping internal state updates in `startTransition`". It also states the plan to make the opt-in the default in v8 and to "likely retain the opt-out flag". That is a v8 caveat for whoever does that upgrade, not a defect now.

**Admin and verifier: still unaffected, MEASURED.**
- Round 2 changes only line-1 comments in their 12 files.
- I built both portals at the head and at 258e049aaf75: `diff -rq` of the two `dist` trees gives **0** differing entries for admin (20 files) and for verifier (13 files). The issuer pair differs in 72 entries, which is the control.
- Because the shipped bytes are identical, round 1's runtime results for those two portals carry over unchanged.
- Neither portal has `lazy(` or `<Suspense` in its `src` (0 and 0; control: issuer 1 file).

## Q2. F2: do the PR body, the docs fragments and comment 2083ebbe now say true things?

I read the live text read-only:
- **PR:** GitHub REST GET with the project's `GH_TOKEN` (the project's `.gh-config` has no login). Open, base develop, head e5742b73748b, 2 commits, 34 files, not merged, title unchanged, updated 12:03:18Z.
- **Comment:** Linear GraphQL query (no mutation). Comment 2083ebbe is top-level, edited 12:03:31Z, and still authored by the project account. KS-528 is In Progress, priority 3, 10 comments.

- **The "no intended behaviour change" claim is gone from all four texts.**
  - PR lead: "a dependency migration with ONE measured behaviour change, which round 2 reverses".
  - Comment BLUF: "Gate 255 found one behaviour change the first text did not state ... Round 2 opts the issuer out".
  - Both say round 1's walk "could not see" F1 because its issuer sidebar steps were history pushes.
  - The flow fragment's old "`v7_startTransition` is UNMEASURED" line now reads "was UNMEASURED in round 1. Round 2 measured it for the issuer". True: I re-measured it above.
- **Re-measured and true:**
  - 8 of 8 for the control and round 2, 0 of 8 for the first head, the old Settings heading visible.
  - Admin and verifier have 0 `lazy`/`Suspense`.
  - Round 2 changes 26 of the 34 files: 23 portal sources, the suite and 2 fragments (`main.tsx` is one of the 23).
  - 25 cells = 16 + 9: 15 R mutants and 8 G mutants.
  - Red-first: six F4 cells fail against the round-1 checker, the other 16 pass.
  - Real files unchanged by the run.
  - The 11 PR heads equal gate 255's (all 11 are open and unmoved, by API GET and fetch).
  - Base b7d433fda83c.
  - "admin and verifier ... untouched": byte-identical `dist`.
- **True when written, stale now:** the body's "develop is cfb6c1573ba9 ... merge-tree ... tree 769f0351". cfb6c1573ba9 is an ancestor of abd044f6, one commit behind the start reading, with 65 files past base (I measured 65). Develop is now 765701307eb3, and merge-tree still holds (Q6).
- **N1 (Nit, false sentence in shipped docs).** `Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html`, the "cells" row, says: "against develop b7d433fda83c the checker reports R1 (23 files), R2 (6 lines), R3 (8 lines), R4 (2 rows) and nothing for G1 to G6".
  - At this head the checker reports **`G6 issuer: <BrowserRouter useTransitions={false}> is not present exactly once`** on develop, because develop's issuer has no opt-out.
  - MEASURED: I extracted the head's checker and ran it on develop abd044f6, whose issuer is identical to b7d433fd's (develop changed no issuer file since base). Output: R0 ×3, R1 ×3, R2 ×6, R3 ×8, R4 ×2, **G6 ×1**.
  - The flow fragment's "G1 to G5 are green on develop" is correct. Only the cheat row says G6.
  - Fix-shape: "nothing for G1 to G5; G6 is red on develop by design".
- **N2 (Nit, wording).**
  - The body and the comment call the v6 control "this PR's parent". The builder's own evidence names it as b7d433fda83c, which is the PR's base, not the parent of the head (the head's parent is 258e049aaf75, the "first head").
  - The body's "Unheld, the control and round 2 show the screen for their first two samples": I saw one sample of 8 unheld, on both. That is timing on a loaded host, not a contradiction of the direction.
  - Neither point changes a conclusion.
- Not verified (registry claims, as in round 1): latest 8.5.1, the GHSA-qwww range, `MISSING_EXPORT`, and the eslint counts.

## Q3. F3: the import-comment wording against the installed packages (MEASURED)

New text, on all 23 lines: "was react-router-dom (v6), now react-router 7. v6.30.6 already exported these from react-router except BrowserRouter and useSearchParams; only the module name changed."

- Every name imported across the 23 lines: BrowserRouter ×3, Navigate ×2, Outlet ×1, Route ×3, Routes ×3, useLocation ×5, useNavigate ×15, useParams ×6, useSearchParams ×1.
- **react-router 6.30.6** (develop build, runtime export list of `dist/main.js`, 56 exports; control: `createMemoryRouter` is present): Routes, Route, Navigate, Outlet, useNavigate, useLocation and useParams are **exported**. BrowserRouter and useSearchParams are **not**. The comment is exact.
- **react-router 7.18.5** (head build, `dist/production/index.mjs` imported): all 9 names are exported.
- The comment appears 23 times and sits immediately above each of the 23 `from 'react-router'` lines (0 misplaced). The old "dropped for v8" wording appears 0 times at the head; control: 23 times at 258e049aaf75.
- One wording quirk, not a finding: on `issuer/src/main.tsx` the only import is BrowserRouter, so "these ... except BrowserRouter" covers zero names. It is still true.

## Q4. F4: the widened checker (MEASURED)

- **Red-first.** I built a hybrid suite: the head's suite file with the checker heredoc swapped for 258e049aaf75's (the diff is the checker lines only). I ran it on a copy of the head's tree.
  - The six new F4 cells **FAIL** ("mutant left R1/R2 green"): optionalDependencies, peerDependencies, overrides flat, overrides nested, `.cjs`, `.cts`.
  - The three G6 cells fail too (no G6 rule), and so does the real-tree cell, through round 1's bare-literal G3.
  - All 11 round-1 R and G mutants pass, and so does the RX cell.
  - Total: `passed=15 failed=10`.
- **Head.** `passed=25 failed=0`, rc 0. The sha256 of all 176 checker-read files (3 portal `src`, 3 manifests, 4 locks, the baseline) is identical before and after the run. `git status` in the worktree shows 0 changes.
- **Legitimate shapes on develop's real manifests.** I ran the head's checker on develop abd044f6:
  - R2 lines name only `dependencies ^6.30.4` (the real shape) plus the floor line, 6 in all, the same count as round 1's checker on the same tree.
  - The overrides walk produces no hit. The real overrides keys are minimatch, postcss-selector-parser, ip-address, undici, and jsdom → undici.
  - The widened walker adds 0 files (`.cjs`/`.cts`/`.mts` in portal `src`: 0 on develop and at the head; control: 166/167 `.ts`/`.tsx`). SCANNED is 168 under both checkers.
  - G3 does not fire. G6 fires, and that is intended: develop lacks the opt-out.
  - So **no new rule refuses a legitimate shape that exists on develop.** The checker is also clean on the merged tree (develop + head).
- **My plants** on scratch copies of the head's checker inputs (the unmodified control copy reads clean):
  - `.mts` re-export from react-router-dom: R1 red, **caught** (not among the builder's mutants).
  - A dynamic `import("react-router-dom")` appended to issuer `App.tsx`: R1 red, **caught**.
  - The overrides key `"react-router-dom@6"` (npm accepts a `name@range` key): **missed**. Low: an actual install still lands in a lock, which R3 scans at any depth.
  - `bundleDependencies: ["react-router-dom"]`: **missed**. Nit: npm also requires a bundled dependency to be in `dependencies`, which R2 reads.
  - Two future legitimate shapes that the source-text pins refuse (N3, by design, recorded):
    - The opt-out reformatted over two lines (`<BrowserRouter\n useTransitions={false}\n>`) turns G6 red.
    - A test wrapper under `issuer/src` that renders a `<BrowserRouter>` turns G3 red.
    - G3 already refused the bare form in round 1, and the suite says to change a pin on purpose. Not a defect today.

## Q5. Anything round 2 changed beyond F1 to F4 (258e049aaf75..e5742b73748b, 26 files)

All 26 files map to a finding:

| files | finding |
|---|---|
| 23 portal sources | comment line only (F3) |
| `issuer/src/main.tsx` | also the opt-out and its comment (F1) |
| `react_router_v7_portals.test.sh` | F4 checker and mutants, plus F1's G6 |
| 2 docs fragments | F2 |

**No file falls outside the four findings.**

The one change inside the suite that is not literally F4 is the **G3 rewrite**: it now counts `<BrowserRouter[\s>]` instead of the bare literal, because the issuer's element now carries a prop. It still refuses any `basename=` in the issuer, its g3 mutant was re-anchored and bites (head 25 of 25), and `</BrowserRouter>` does not match. Judged correct. Its legitimate-shape edge is N3.

## Q6. Merge state (MEASURED)

- `merge-tree abd044f6 e5742b73`: rc 0, tree 1ea2290685609833f8b1a642f1ee9cb30bbbfce6. This equals the builder's 1ea229068560.
- `merge-tree 76570130 e5742b73` (develop at end): rc 0, tree 715e01d3be7da3f0ce805e501bfb8771151ea0b1.
- Develop's own frontend changes since base (admin `Settings.tsx`, `api.ts`, `authStore.ts`, `settingsSavePayload.ts`, shared `auth/index.ts`) contain 0 react-router references. The head's checker on the merged tree is clean.
- **The 11 PRs** (heads equal gate 255's: 575 7d32d8ae, 635 6cbc298f, 639 2069d852, 649 1d9198ac, 945 264098fc, 946 41cc5209, 947 d68b9d79, 948 2f881c24, 949 29d8bfa9, 1360 d0e99f18, 1965 fb0a2bee; all open). For each, I ran `merge-tree` against develop and against a local, never-pushed simulated merge of develop + head. I did this on BOTH develop readings (abd044f6 and 76570130) and got identical results both times:
  - 635, 639, 945, 946, 947, 1360 and 1965: clean before and after.
  - 575 (1 file), 649 (15), 948 (6) and 949 (1): conflict before and after, **with identical conflicted-file lists**.
  - The 4 pre-existing conflicts are the positive control: the instrument does see conflicts.
- **The head adds no conflict to any of the 11.**

## Findings

| id | severity | where | status |
|---|---|---|---|
| F1 (round 1) | was Minor | `issuer/src/main.tsx:44` | **CLOSED**, measured |
| F2 (round 1) | was Minor | PR body, comment 2083ebbe, fragments | **CLOSED** in substance; residue N1, N2 |
| F3 (round 1) | was Nit | 23 import comments | **CLOSED**, measured |
| F4 (round 1) | was Low | suite checker | **CLOSED**, red-first reproduced; residue in Q4 (two missed plants, Low/Nit) |
| N1 | Nit | `Projects Documents/fragments/cheat/KS-528-react-router-v7-portals.html`, "cells" row | false: G6 is red on develop |
| N2 | Nit | PR body and comment | "this PR's parent" means its base b7d433fd; "first two samples" unheld is timing |
| N3 | Note | suite G3/G6 | source-text pins refuse a multi-line opt-out and a `<BrowserRouter>` test wrapper; by design |

## Controls I planted or used

- **F1:** a hidden "Loading..." plant (the predicate said hidden in 7 of 8 samples while it stayed in the DOM). Old-page hidden-in-DOM on dev and head versus visible on r1. My own v1 run, invalid and kept.
- **Admin/verifier `dist` identity:** the issuer pair differs (72 entries) under the same diff.
- **Q3:** `createMemoryRouter` present in the v6 export list, and the old wording counted 23 at 258e049aaf75.
- **Q4:**
  - The round-1 checker as the red arm.
  - An unmodified scratch copy reads clean.
  - Two plants caught, two missed.
  - `.ts`/`.tsx` count beside the 0 for `.cjs`/`.cts`/`.mts`.
  - SCANNED equal under both checkers.
- **Q6:** 4 PRs that already conflict, as positive controls for merge-tree.

## NOT TESTED

- The images on node:24-alpine, Node 24 at all, Docker, the nginx-served paths, any live gateway, real login or cookies.
- Issuer vitest, eslint, tsc in the dev-host layout, the audit gates, `npm audit`. Round 2 touches no manifest, lock or baseline (verified: 0 of 26 paths), so round 1's results there carry over by identity. I did not re-run them.
- Builds of the merged tree (develop + head). Develop changed 4 admin files and shared `auth/index.ts` since base. I checked them only for router references (0) and with the checker, not with `tsc`/`vite build`.
- Lazy pages other than Documents and Settings. Roles other than ISSUER_ADMIN. Keyboard, mobile and accessibility. Slow-network throttling (I held chunks by route interception instead).
- Admin and verifier in a browser in round 2: covered by byte-identical `dist`, not by a fresh drive.
- The builder's walk scenarios A to E (I drove F1 only). The builder's unexplained console observations.
- The 32 round-1 tampers. The full `test:shell` and preflight.
- `npm ci` on any merged tree.
- Registry facts in the body (8.5.1, the GHSA-qwww range, `MISSING_EXPORT`), and the eslint counts.

## My own conduct

- **Clone.** `/private/tmp/g260` on the boot volume, **2.2 GB** at the end. It holds a blobless bare clone, three sparse worktrees (head, r1, dev), 9 build stages with `node_modules`, scratch copies, plant dirs and logs. Left in place; nothing removed.
- **Refs and tools.** Local refs `refs/pr/*`, `refs/g260/sim`, and two never-pushed commit-tree merge simulations (61f17d0f, 68dea021) live only in that clone. The deploy-key `core.sshCommand` is set in that clone's own config.
- **DevMASTER.** 25 GiB free at start, 24 GiB at end. I made no writes under `!CODING`: the shared checkout was read only (remote and sshCommand read), never fetched or written.
- **Network.**
  - git ls-remote/fetch.
  - `npm ci --offline` ×9.
  - GitHub REST: 12 GETs (PR 2091 plus the 11 PRs), using the project's `GH_TOKEN` from `4_Credentials/.env`, exported for the call only and never written anywhere.
  - Linear GraphQL: 1 read query, using `LINEAR_API_KEY` the same way.
  - Nothing was posted, edited or mutated.
- **Deletes.** I removed no files with `rm`. The suite under test deletes its own `mktemp` directory (under `/private/tmp/g260/tmp`) through its own `trap`. That is the repo's code, run twice (head and hybrid), as in round 1.
- **Writes outside the gate folder and the clone:**
  - this session's scratchpad (ls-remote output, the PR JSON and body, the live comment text, an empty gh config dir);
  - the Playwright MCP's own console logs in `/Volumes/DevMASTER/WEDNESDAY/.playwright-mcp/` (a tool-managed folder that already existed).
  - The drive scripts sit in this gate folder's `tools/`, because the MCP only reads files under WEDNESDAY.
- **Processes.** I started six `vite preview` processes. The first three failed at once on a bad flag (`--root`, see `logs/preview_*_43xx.log`). The other three were killed at the end, and 0 `vite` processes remain. The Playwright browser was left as the MCP owns it.
- **Load.**
  - Load was 7.3 at boot. Spark's own `tsc`/vitest jobs (not mine) pushed it to 10 to 13 several times.
  - I gated every build and suite run on load1 below 7 (once below 7.5) and waited whenever it was above.
  - The 1-minute figure read 8.65 directly after my third issuer build and 13.5 at the end readings, both while the Spark jobs were running.
- **Shell.** I used no `cd` in any shell command. My build script runs npm and tar with `--prefix`/`-C`, and every invocation used `bash /abs/path`.
