PR 2227: GO WITH NOTES (at head e29f8e8fa4b6ff15ffb3c749d400b93586f66aab; tier 1)

Gate 350 (tier 1, Opus), 2026-11-13 12:40 to 12:50 AEDT. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**Pins.** `git ls-remote` at 12:40:56 and again at 12:48:49 / 12:49:18 AEDT:
- refs/pull/2227/head e29f8e8fa4b6ff15ffb3c749d400b93586f66aab at every read. **The head did not move.**
- refs/pull/2099/head 8967de8b1755 at every read.
- **develop MOVED:** a288aa45d6b2f96e96abb5491308e77c3fa07605 at 12:40:56, then **a6af38a517161709e56bbce61b82e2a9ccbce6a5** at 12:48:49. The new commit is one docs-only commit, a6af38a51 "Refs KS-2077: the architecture reference routes /api/rewards to Referral…" (2 +2 −2 in `Projects Documents/Secuura-Architecture-Reference.md`). It touches no lock, no manifest and no baseline. I re-ran merge-tree against it (G350-2227-4). Every other measurement was taken at a288aa45 (the PR's own base). Nothing it measured can be changed by a docs-only commit.
- `npm view hono dist-tags.latest` = 4.13.18 at both reads.
- PR 2227 is ONE commit, with one parent, a288aa45d6b2. `git diff --numstat develop...head` gives exactly `3 3` on each of the 2 locks.
- The builder's READY (`s78_ready.txt`) and STATUS 1 (`s78_status1.txt`) are already in this folder. I read both whole.

## FOUND

**G350-2227-1 (Low; the body and the ticket are now stale on the two "GitHub-only" ids, and the change makes the proof stronger, not weaker).** npm's feed now lists all five ids.
- **The claim:** the PR body, the KS-2195 description and READY item 5 say GHSA-46wx-v44x-9hh2 and GHSA-4h7h-rv7c-7m2v "occurred 0 times BEFORE too (npm's feed does not list them yet), so for those two the proof is the range". They quote BEFORE figures of "8 distinct advisories reported, 5 baselined" with 3 NEW, and "7 advisories match".
- **What I measured at develop a288aa45 (12:4x AEDT):**
  - `audit:gate` rc 1: "10 distinct advisories reported, 5 baselined", **5 NEW**. The five are 4m76, h7mg, 3gg2, **46wx and 4h7h**.
  - `audit:locks` rc 1: "9 advisories match, 4 already baselined", the same **5** in `services/mcp-server`.
- **At the head:** all five occur 0 times in both legs, and the head passes (Q3).
- **Consequences:**
  1. All five ids are now cleared by an audit-output absence, with a develop-side control that sees each of them. The range result also holds (Q3).
  2. The body's BEFORE numbers (8/3 and 7) no longer reproduce. They were true when the seat measured them.
- **No fix is required for merge.** If the seat patches the body, one sentence would do: "npm's feed now lists all five; at base the legs report 10 distinct / 5 NEW and 9 match; at head all five are absent."

**G350-2227-2 (Info; THE runtime question: the 4.13.13 → 4.13.18 diff is large and security-relevant, and no path this repo runs reaches it).** The READY and body left the code diff, the CommonJS paths and `@prisma/dev` unmeasured. I measured them.
- **Size of the diff** (`npm pack` of 4.13.13 / 4.13.16 / 4.13.18; each packed integrity equals the registry's and the lock's): 37 runtime modules changed in `dist/` (ESM), and the CJS build mirrors them. Plus one new module, `utils/mount.js`, and the `.d.ts`, README and package.json files. I read the ESM diff whole (1178 lines, `scratch/hono_esm.diff`).
- **Behaviour changes, all of them:**
  - (a) **`mount()` / `app.mount()`:** the request rewrite now goes through the new `createMountedRequest`. It builds the prefix from the matched route params. It now throws an `Error` on duplicate param names, on optional-regex params, and on a wildcard that does not follow "/". It answers **400** on unsafe mounted paths: dot segments, `%2e`, a backslash or `?`/`#` in the authority, and a trailing-slash mismatch. This is the GHSA-4m76 fix.
  - (b) **RegExpRouter:** handler and middleware merging is rewritten (key lists plus `covers()` instead of a regex-of-path). Wildcards change from `.*` to `[^]*`, so they now match line terminators (the GHSA-h7mg fix). Static paths now carry params. A param regex that matches "" is refused. PreparedRegExpRouter now keeps static params and serialises `undefined`.
  - (c) **trie tokeniser:** gains the `s` flag and nested `{n,m}` quantifiers inside param patterns.
  - (d) **TrieRouter:** with a duplicate param name, the first match now wins.
  - (e) **`getPath`:** a malformed `%` is re-encoded when the decode is not stable. **`getQueryParam`:** keys containing `%+&=` take the slow path, and an earlier encoded key disables the fast path.
  - (f) **`c.header()`** after finalize no longer rebuilds a response whose body has been used.
  - (g) **`csrf()`:** now treats `text/ping` as a form content type (GHSA-46wx).
  - (h) **`validator`:** json and form match on the media type before `;`, so `multipart/form-data` with extra params is now validated (GHSA-4h7h). The JSON type regex is stricter.
  - (i) **`css` helper:** `</` is escaped after minify, values escape `\"'`, `url(...)` is kept intact, `:` spacing changes (GHSA-3gg2), and the style-replace regex gains the `s` flag.
  - (j) **JSX:** attribute rendering is refactored (`attributeToBuffer`), and a RENDERED_JSX mark stops rendered JSX being treated as pre-escaped. A non-`on*` function prop throws (`ref` is skipped). `dangerouslySetInnerHTML` needs `__html`. The `shadowroot*` booleans are added. The Suspense/ErrorBoundary scripts carry the nonce. `cloneElement` handles undefined children. `jsxAttr` gains action/formaction permalinks.
  - (k) **`serveStatic`:** only GET and HEAD are served. The percent check moves after decode. Accept-Encoding is parsed with q>0.
  - (l) **`bodyLimit`:** buffers into one Uint8Array instead of re-streaming with `duplex`.
  - (m) **`etag`:** If-None-Match is parsed as quoted tags, and the body is cancelled on 304. **`prettyJSON`** also cancels the old body.
  - (n) **Auth headers:** basic, bearer, jwt and jwk escape `\` as well as `"` in the realm and description. `bearerAuth` passes through a Response message and adds WWW-Authenticate. `timing` quotes desc and treats precision 0 as 0.
  - (o) **JWT:** a header carrying `crit` is rejected, and the signature must be in the base64url charset.
  - (p) **Cookies:** the `__Secure-` / `__Host-` prefix checks are case-insensitive.
  - (q) **Small fixes:**
    - accepts: an exact type beats `type/*`;
    - `getExtension` and the ssg extension lookup lower-case the type;
    - ssg `createdDirs` is per call;
    - the route helper `basePath` is fixed;
    - aws-lambda sanitises header values;
    - the client trims content-type.
- **Which hono modules each consumer can load** (`scratch/honoclosure.py`: a static import/require closure inside 4.13.18 per export subpath, ESM and CJS, intersected with the changed set; positive control: `hono` root reaches 10 changed modules):
  - **`@modelcontextprotocol/sdk` 1.32.1:**
    - its only direct `hono` imports are in `examples/server/honoWebStandardStreamableHttp.js` (not loaded by anything);
    - it reaches hono only via `@hono/node-server` in `server/streamableHttp.js`. node-server's index loads `hono/ws` (1 module, **0 changed**). Its `serve-static` loads `hono/utils/mime`, which IS changed, but only in `getExtension`; node-server calls `getMimeType`, which is unchanged.
  - **`@prisma/dev` 0.24.3** (root lock only) imports `hono/tiny`, `validator`, `client`, `http-exception` and `logger`. tiny, validator and client do reach changed modules (hono-base, context, url, mount, validator, cookie, fetch-result-please).
- **What this repo runs** (measured, positive controls in brackets):
  - **mcp-server built dist, isolated Dockerfile-route copy, develop AND head** (`scratch/walk.mjs`, the synchronous `module.registerHooks`, which sees import AND require, plus a CommonJS-cache scan):

    | Load | Modules resolved | In CJS cache | hono | @hono/node-server |
    |---|---|---|---|---|
    | `dist/http-server.js` (Dockerfile CMD), ESM | 775 | 715 | **0** | 0 |
    | `dist/http-server.js`, require() | 775 | 716 | **0** | 0 |
    | `dist/index.js` (package main, stdio), ESM | 349 | 167 | **0** | 0 |
    | SDK `server/mcp.js`, require() | 240 | 240 | 0 | 0 |
    | SDK `server/stdio.js`, require() | 100 | 99 | 0 | 0 |
    | [control] SDK `server/streamableHttp.js`, ESM | 109 | 1 | **1** | 2 |
    | [control] SDK `server/streamableHttp.js`, require() | 109 | 106 | **1** | 2 |
    | [control] `require('hono')` | 26 | 26 | **26** | 0 |

    The only SDK subpaths mcp-server imports, in src and dist, are `server/mcp.js` (10) and `server/stdio.js` (2).
  - **Note on the seat's instrument:** the seat counted 55 modules for `http-server.js` because the async `module.register` hook does not see CommonJS `require()`, and express is CommonJS. Its zero was right, but its instrument could not see the CJS half. My 775/715 row closes that gap.
  - **Prisma CLI 7.8.0** (the one that pulls `@prisma/dev`), head tree, a preload hook counting resolved modules:

    | Command | Modules | `@prisma/dev` modules | hono |
    |---|---|---|---|
    | `--version` | 901 | 2 | 0 |
    | `generate --help` | 900 | 2 | 0 |
    | `dev --help` | 1167 | 15 | 0 |
    | [control] require of `hono/tiny` | — | — | 17 |

    `git grep 'prisma +dev'` (locks and .md excluded) finds 0. Control: `prisma generate` hits 11 files. 0 Dockerfiles COPY the root lock. originate's own lock carries no hono (census).
- **Verdict on runtime:** mcp-server is the only image that installs hono, and it never loads it. `@prisma/dev` loads hono only inside a running `prisma dev`, which nothing here runs. So the changed code is reached by no path this repo runs, and the five advisories were not exploitable on a shipped path. The PR's value is unfreezing legs 6 and 7, and it does that.
- Risk from 4.13.18's large diff to this repo's runtime: nil on every path I could find. The 137/137 suite is a no-regression check, not a hono-path check, as the body already says.

**G350-2227-3 (Info; GitHub CI is red on billing, not code).**
- 19 check runs on the head: 11 failure, 8 skipped.
- The failed jobs' annotations (Dependency Audit, Linear ticket present, Pre-merge acknowledged — Akto; the same set as gate 349) read "The job was not started because recent account payments have failed or your spending limit needs to be increased".
- GitHub reads mergeable true, mergeable_state `unstable`.
- Not fixable in this PR.

**G350-2227-4 (Info; develop moved during the gate, and the merge is still clean).**
- **Against develop a6af38a5** (merge-base a288aa45), merge-tree `--write-tree` in both orders gives rc 0 and tree 3aee88a0360a.
  - The merged tree differs from develop a6af38a5 in exactly the 2 locks, and their blobs equal the head's (e0f4edae4cce, d632dc90c5fd).
  - It differs from the head only in the KS-2077 doc, whose blob equals develop's (c7c3144bbc71).
- The PR is now one commit behind develop. No rebase is needed for content. Whether branch protection wants it up to date is the merge seat's call.

**G350-2227-5 (Info; the body says acknowledgment boxes "stay unticked", but the body carries none).**
- 0 checkbox lines in the 34-line body. Control: `- [ ] Akto` gives 1.
- The two "Pre-merge acknowledged" checks failed on billing either way (G350-2227-3). Per card `secuura-premerge-block-nine-prs-1113` = c, they do not hold a merge.
- Cosmetic.

No finding against lock integrity, the census, the audit legs, the install, the mcp-server suite, merge-tree, the open-PR picture, the title, or KS-2194.

## TESTED

**Q1 Lock integrity** (`scratch/lockdiff.py`, a structural JSON diff, develop a288aa45 vs head):
- **Root lock:**
  - top-level keys: 0 differ;
  - `packages`: 1955 = 1955 entries;
  - exactly ONE changed entry, `node_modules/hono`, with fields changed = {integrity, resolved, version};
  - entries with `libc`/`os`/`cpu`: 137 → 137, and 0 platform-field diffs.
- **mcp-server lock:** the same, with 302 = 302 entries and platform entries 53 → 53.
- **Control:** a planted `@hono/node-server` version change plus a planted `os` field are both detected by the same differ, in both locks.
- `integrity` sha512-H9q/E1XizaWs…f3DA== = `npm view hono@4.13.18 dist.integrity` = my `npm pack` integrity.
- `resolved` = `https://registry.npmjs.org/hono/-/hono-4.13.18.tgz` = `dist.tarball`.
- The entry's `engines` (`node >=16.9.0`) equals the tarball's. hono declares no dependencies.
- sha256 at develop and head, identical:
  - root package.json 991d4f5ae1e2…;
  - mcp-server package.json 6980207cc065…;
  - `scripts/audit/audit-baseline.json` d6e7f1ed1175… (the READY's value).

**Q2 Census** (`scratch/census.py`, JSON parse of every tracked `package-lock.json`, `packages` plus nested legacy `dependencies`):

| Ref | Locks tracked / parsed | hono carriers | hono versions | @hono/node-server | Locks with no hono |
|---|---|---|---|---|---|
| develop a288aa45 | 47 / 47 | 2 (root, mcp-server) | 4.13.13 ×2 (vulnerable) | 2.1.8 ×2 | 45 |
| head e29f8e8f | 47 / 47 | 2 (root, mcp-server) | 4.13.18 ×2 (not vulnerable) | 2.1.8 ×2 | 45 |

- The positive control is the develop row: it finds the two carriers.
- Other lock formats: 0.
- **No `package.json` declares `hono`.** The only `@hono/*` manifest hits are the KS-530 `@hono/node-server ^2.1.3` override in root and originate.
- The binding ranges are inside locked packages and all admit 4.13.18:
  - SDK `^4.11.4`;
  - `@prisma/dev` `^4.12.8`;
  - the node-server peer `^4 || ^5.0.0-0` (per the ticket, consistent with the lock).
- 31 Dockerfiles use `npm ci`, and 0 use `npm install`, `yarn add` or `pnpm add`. Nothing can pull a vulnerable copy at build time.

**Q3 Audit legs, reproduced by me** (fresh worktrees at develop a288aa45 and the head, each with its own root `npm ci --ignore-scripts`, Node v26.8.1, npm 11.19.0):

| Leg | develop a288aa45 | head e29f8e8f |
|---|---|---|
| `audit:gate` | **rc 1**: "10 distinct advisories reported, 5 baselined", FAIL with 5 NEW (4m76, h7mg, 3gg2, 46wx, 4h7h) | **rc 0**: "5 distinct advisories reported, 5 baselined", OK |
| `audit:locks` | **rc 1**: "45 standalone lockfiles … 1629 distinct packages pinned — 9 advisories match, 4 already baselined", FAIL with the 5 in services/mcp-server | **rc 0**: "45 standalone lockfiles … 1629 distinct packages pinned — 4 advisories match, 4 already baselined", OK |
| `audit:contract` | rc 0: tests 62, pass 62, fail 0, skipped 0 | rc 0: 62/62, fail 0, skipped 0 |
| each of the 5 hono ids (gate / locks) | 2 / 1 each | 0 / 0 each |
| node-server ids qv5m, jpvv | 0 | 0 |
| distinct GHSA ids in output (gate / locks) | 5 / 5 | 0 / 0 |

- **Not "0 checked":** at the head, 45 lockfiles and 1629 packages were checked, and 4 advisories still match, all baselined.
- **Ranges** (`scratch/range.cjs`, semver over the GitHub `/advisories/<id>` hono ranges):
  - All 5 ranges (`< 4.13.16` twice, `>=4.1.4 <=4.13.15`, `>=3.12.0 <=4.13.15`, `>=4.5.1 <=4.13.15`; first patched 4.13.16) EXCLUDE 4.13.18.
  - Planted controls: 4.13.13 is IN all 5, and 4.13.16 is OUT of all 5.
  - `/advisories?ecosystem=npm&affects=hono@4.13.18` gives **0**. Control: `affects=hono@4.13.13` gives the 5 ids.

**Q4 Runtime:** G350-2227-2.

**Q5 mcp-server suite, Dockerfile route, reproduced by me.** Setup:
- `git archive` of `packages/shared` + `services/mcp-server` at each ref into `scratch/iso-{dev,head}`, with no workspace root above;
- shared `npm ci --ignore-scripts` + `npm run build`;
- mcp-server `npm ci --ignore-scripts`;
- `node_modules/@secuura/shared` symlinked to the shared copy.
- All rc 0. The isolated `npm ci` left each lock byte-identical: the head's is e46e404c4e5d… = the committed blob, the READY's value; develop's is 8203e98f6caa….

| Run | Installed hono | Result |
|---|---|---|
| head, NO link (control) | 4.13.18 | rc 1: 5 failed / 10 passed files, 62 passed / 75 skipped (137). All 5 fail on "Cannot find package '@secuura/shared/zod3-compat'", the known build-shape fault. |
| develop, linked | 4.13.13 | rc 0: **15/15 files, 137/137 tests** |
| head, linked | 4.13.18 | rc 0: **15/15 files, 137/137 tests** |

- `tsc --noEmit -p tsconfig.json` gives rc 0 with 0 output lines at both refs. Control: a planted `const n: number = "x"` gives rc 2, TS2322.
- `npm run build` gives rc 0 at both. The built dist is what Q4 walked.

**Q6 Root install:** `npm ci --ignore-scripts` rc 0 at develop and at head ("added 1794 packages" both). `npm ls hono @hono/node-server --all`, rc 0:
- **head:** ONE `hono@4.13.18`:
  - under `@secuura/mcp-server → @modelcontextprotocol/sdk@1.32.1`;
  - "deduped" under that SDK's `@hono/node-server@2.1.8`;
  - "deduped" under `@secuura/originate → prisma@7.8.0 → @prisma/dev@0.24.3` (and its node-server).
- **develop:** the same shape at 4.13.13.
- One physical copy on disk in each tree (`find` = 1). Its version is read from the file: 4.13.13 / 4.13.18.

**Q7 merge-tree** (`scratch/plant.sh`, `--write-tree`, in my clone, each side's own merge-base):

| Merge | rc | Tree |
|---|---|---|
| develop a288aa45 × 2227, both orders | 0 | bf0a468f7663 |
| develop a6af38a5 × 2227, both orders (G350-2227-4) | 0 | 3aee88a0360a |
| PR 2099 × 2227, both orders (merge-base c0e6e744b7b2) | 0 | 9d87a1b91836 |
| planted conflict: develop + the hono `version` line set to 4.13.17 (numstat 1 1), × 2227, both orders | **1**, conflict in `Blockchain/Dev/package-lock.json` | (conflicted) |
| twin: develop + head's root-lock blob (numstat 3 3), × 2227, both orders | 0 | bf0a468f7663 |

- **Survival:** bf0a468f7663 vs develop differs in exactly the 2 locks, with blobs = head's. Against the head it differs in nothing, because the PR's only parent is a288aa45.
- **PR 2099:** the merged root lock keeps `hono` 4.13.18, and the merge carries all of 2099's files.
- **Open-PR scan** (`scratch/openprs.py`, read-only gh api): 88 open PRs (the seat saw 89), 0 file-list errors.
  - On the root lock: 2227 plus the same 11 (2099, 1965, 949, 948, 947, 946, 945, 649, 639, 635, 575).
  - 0 PRs other than 2227 touch mcp-server's lock or manifest.
  - Controls: 2227 and 2099 are both found.
  - None of them bumps hono.

**Q8 Body and ticket:**
- **PR (GitHub API):** open, not draft, base develop, head = pin, 2 files, +6 −6. mergeable true / `unstable` (G350-2227-3).
- **Title:** "Refs KS-2195: refresh hono 4.13.13 -> 4.13.18 in the root and mcp-server locks". It starts `Refs KS-2195:`. The commit subject is the same, with a Sonnet trailer.
- **Body (34 lines):**
  - `## Test Evidence` is present: the Node line; Touched / Ran / NOT run / Migrations and config; and "Before this deploys: nothing deploys from this PR; deploy is Kam's tap".
  - **The PREFLIGHT line is quoted verbatim:** "PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed." The body explicitly says this is not a pass of legs 3, 4 and 8.
  - **Self-hold regex: 0 hits.** Control: "Do not merge until the pre-merge tests have been run." gives 1.
  - Close words: 0. Control: "Closes KS-1" gives 1.
  - **Docs escape clause:** the body cites SKILL.md lines 483-484. At the head those lines read "If a change genuinely does not affect either doc, **say so explicitly and why** — do not silently skip." The body says so and why (no test, probe or gate added; one dependency's three lock fields).
- **KS-2195** (Linear GraphQL, read-only, key read inside python and never printed):
  - In Progress, priority 1, project "Dependency and Version Currency", created 2026-11-13T01:14:42Z.
  - Attachment: PR 2227.
  - One comment, cc53912a… at 01:38:25Z, 1637 characters, names 2227. Its only `@` token is `@hono`; 0 profile links (control 1). There is no user mention.
  - **Scope:** "lock-only refresh of `hono` 4.13.13 -> 4.13.18 in the two locks that carry it. No manifest edit, no baseline row … Not touched: KS-2194, both package.json files, audit-baseline.json, services/originate". **The PR matches it exactly.**
- **KS-2194 untouched:**
  - its last history entries are 00:14:57Z (PR 2226 attached) and 00:31:31Z (a description edit), both before KS-2195 existed (01:14:42Z);
  - its single comment (4c4db94b…, 00:15:35Z) does not name 2227;
  - its attachment is only PR 2226.

## HOW
- **Clone:** `scratch/clone`, `git clone --shared --no-checkout` of the Blockchain checkout. Origin is set to GitHub, push URL `DISABLED` (re-read at the end), and `core.sshCommand` is copied from the project config.
- **Refs:** develop (twice), PR heads 2227 and 2099, fetched BY URL into `refs/gate/*` of my clone only.
- **Worktrees:** `scratch/wt-dev` and `scratch/wt-head` (detached, `git status --porcelain` = 0 lines at the end).
- **Isolated copies:** `scratch/iso-dev` and `scratch/iso-head`.
- **Tarballs:** `scratch/tar/`. npm caches: `scratch/npmcache*`.
- **Logs:** `scratch/*.log`, `setup.out`, `iso.out`, `walk.out`, `honoclosure.out`, `census.out`, `lockdiff.out`, `plant.out`, `openprs.out`, `ghadv.tsv`, `checks.json`, `pr2227.json`, `pr2227_body.md`, `KS-2195.json`, `KS-2194.json`, `linear*.out`, `pin1.out`, `pin2.out`.
- **GitHub:** read-only via `gh api` with the Blockchain gh config (kksecura confirmed by `gh auth status`).
- **In the Blockchain project:** only `config --get` and the `--shared` clone source. I made no writes there.
- **Leftovers:**
  - in my clone only: two unreferenced plant commits (18c43955b79e conflict, cd0fbcd6921e twin), never pushed;
  - `scratch/plant_*.json` / `.idx`.
- **Side effect, declared:** `prisma dev --help` printed "Fetching latest updates for this subcommand…". The Prisma CLI may have written to its own user-level cache outside `scratch/`. Nothing in any project was touched.

## NOT TESTED
- Node 24 / the `node:24-alpine` docker route; image build; deploy.
- Schemathesis, Akto, Playwright, k6.
- The full 16-leg pre-push hook (I ran legs 5, 6 and 7 as npm scripts only).
- A running `prisma dev` server (only `--help` was measured).
- A live MCP client against a deployed mcp-server. I ran no in-process HTTP smoke this gate; the suite's HTTP-route files ran at both refs.
- Any of the G350-2227-2 behaviour changes exercised at runtime. They were read, and shown unreached, not executed.
- The audit legs and suite at the moved develop a6af38a5 (docs-only; merge-tree only).
- Merges of the stale Dependabot PRs beyond the file-list scan.
- The CI jobs: none ran (billing).
- Other services' suites. No other service's lock carries hono (census).
