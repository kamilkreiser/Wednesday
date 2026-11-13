PR 2226: GO WITH NOTES (at head 15914b780cb605df02895eb173aeaa2a70c35262; tier 1)

Gate 349 (tier 1, Opus), 2026-11-13 11:19 to 11:28 AEDT. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**Pins.** I read them with `git ls-remote` at 11:19:32 and again at 11:28:00 AEDT:
- develop 9105cfdee484a6342d4980d8fc9ea6da3bc87851
- refs/pull/2226/head 15914b780cb6…
- refs/pull/2099/head 8967de8b1755…

**Nothing moved**, and all three equal the commission's pins. `npm view` dist-tags latest is still 2.1.8 at both reads.
- PR 2226 is ONE commit, with one parent: dc57df60a959.
- `dc57df60a959..9105cfdee484` touches 2 paths: the ks1868 api-gateway test and `systemTest/fixtures/provision.ts`. It touches no lock and no package.json (`git diff --name-only`).
- `git diff --numstat develop...head` gives exactly `3 3` on each of the 2 locks.
- The builder's READY is in this folder as `s77_ready.txt` (read whole).

## FOUND

**G349-2226-1 (Low; the READY, the body and the ticket misstate WHY the suite was the proof; not a blocker).** mcp-server never loads `@hono/node-server` at runtime. The changed hono code is unreachable from every entry point this repo ships.
- **The claim:** the body, the ticket "Risk" paragraph and the READY item 4 say "the 2.1.6 -> 2.1.8 code changes sit in stream handling that the MCP SDK's HTTP transport uses". That is true of the SDK. It is not true of this repo.
- **Where hono lives in the SDK:** the ONLY SDK module that imports `@hono/node-server` is `dist/{esm,cjs}/server/streamableHttp.js` (`getRequestListener`; grep over the installed SDK 1.32.1). The other hits are an example file and .d.ts files.
- **What mcp-server imports:**
  - `src/index.ts` (stdio) imports `server/mcp.js` and `server/stdio.js` only.
  - `src/http-server.ts`, the Dockerfile `CMD node dist/http-server.js`, is plain **express** and imports no SDK module at all.
  - There are 0 dynamic `import(` calls in non-test src.
  - Whole-repo `git grep` for `@hono/node-server` imports or `sdk/server/streamableHttp` (locks excluded) finds 0. Positive control: `McpServer` imports are found in 5 src files.
- **Runtime measurement:** a loader-hook import walk (`scratch/importwalk.mjs`) over the BUILT head dist:

  | Entry | Modules | hono hits |
  |---|---|---|
  | `dist/http-server.js` | 86 | 0 |
  | `dist/index.js` | 434 | 0 |
  | control: the SDK's `streamableHttp.js` | 13 | **2** |

- **`@prisma/dev` 0.24.3** (root lock, under originate's `prisma@7.8.0`) runs hono only inside `prisma dev`. `git grep "prisma +dev"` over the repo (locks and .md excluded) finds 0. Control: `prisma generate` hits 11 files. Its consumer in the root lock is reached by no runtime image either: 0 Dockerfiles COPY the root lock, against 23 that copy a `services/*` lock. originate's own lock has 0 hono entries (census).
- **Consequences:**
  1. The 137/137 suite is a valid NO-REGRESSION proof, but it exercises no hono code. "Same ratio" was never able to catch a hono stream bug.
  2. The two advisories were not exploitable on any shipped path. The PR's value is unfreezing legs 6 and 7, which it does.
  3. Risk from 2.1.8's young code to this repo's runtime is nil on every path I could find.
- **No fix is required for merge.** If the seat patches gate notes: one sentence in the body saying "hono is installed but not loaded by mcp-server (express HTTP entry, stdio entry); the suite is a no-regression check, not a hono-path check".

**G349-2226-2 (Info; the drafter's dist read was incomplete, and harmless here per G349-2226-1).** The 2.1.6 -> 2.1.8 `dist/` diff has one more behaviour change than the three the drafter named. In `responseViaResponseObject`, the `.catch((e) => { console.error(e); done = true; })` around `readWithoutBlocking(currentReadPromise)` is REMOVED. A response-body stream that rejects in its first reads now rejects out of the response function instead of being logged and treated as end-of-body.

Full list of 2.1.6 -> 2.1.8 changes. Files: index.mjs/.cjs and serve-static.mjs/.cjs; .cjs mirrors .mjs; 18 changed lines in index.cjs.
- (a) `"duplex"` added to the request-init key list.
- (b) `writeFromReadableStreamDefaultReader`: an already destroyed or closed writable now cancels the reader up front and returns `reader.closed`.
- (c) In `flow`, the `return` is dropped before the re-read. The promise chain is no longer returned; behaviour is the same, but the outer promise settles earlier.
- (d) `writeFromReadableStream` on a destroyed writable now `stream.cancel()`s instead of a bare return.
- (e) The catch removal above.
- (f) `serveStatic`: the percent check moves AFTER decode. With `allowPercentInPath` it now also 404s a path whose decode differs from `%25`→`%` collapsing (stricter).

The full lock delta is 2.1.5 -> 2.1.8, so 2.1.5 -> 2.1.6 also ships. That is the actual security fix:
- `validateRequestTarget` rejects a backslash before `?` with a RequestError (400) in `buildUrl` and for absolute URLs;
- WebSocket-upgrade socket error/close handling: the ECONNRESET crash fix;
- upgrade URL building now goes through `buildUrl`.

None of these is reached by this repo (G349-2226-1). Instrument: `npm pack` of 2.1.5, 2.1.6 and 2.1.8 into `scratch/tar/`, `diff -rq` then `diff -u`. Each packed integrity equals the lock's.

**G349-2226-3 (Info; open-PR conflicts are pre-existing, not caused by this PR).**
- **Scan:** 89 open PRs (the seat saw 90; one has left the open set since), 0 file-list errors.
  - Same 11 on the root lock: 2099, 1965, 949, 948, 947, 946, 945, 649, 639, 635, 575.
  - 0 on mcp-server's lock or manifest.
  - Control: 2226 itself and 2099 are both found.
- **merge-tree against 2226, both orders:**
  - **PR 2099: rc 0, tree 64bbd936240a.** The merged root lock keeps hono 2.1.8 AND 2099's `services/governance/node_modules/ioredis` entry (1, against develop's 0). 2099's lock hunks sit at lines 22623, 22641 and 22655 (+38), far from 6055.
  - **1965, 947, 946, 945, 639, 635: rc 0.**
  - **949, 948, 649: rc 1 on the root lock** (and package.json files for 948 and 649). **575: rc 1 on `services/kyc/package.json` only.**
- **Already true at develop:** all four of 949, 948, 649 and 575 ALREADY conflict with develop 9105cfdee484, on the same file sets (merge-tree develop × PR, rc 1). These are stale Dependabot PRs, so 2226 adds no new conflict.
- **PR 949 (prisma 7.8.0 → 7.10.0):** its lock drops `@prisma/dev`'s `"@hono/node-server": "1.19.11"` dependency line. If it is ever regenerated it removes the `@prisma/dev` consumer; it does not reintroduce a vulnerable copy.

**G349-2226-4 (Info; GitHub CI is red, but billing, not code).**
- **What is red:** 11 check runs failed on the head: Dependency Audit, Standalone locks clean-room, Linear ticket present, build, Secret Detection, and others.
- **Cause:** the Dependency Audit job's annotation reads "The job was not started because recent account payments have failed or your spending limit needs to be increased". The job ran 0 steps.
- **Same at other commits:** the identical failure set is on PR 2224's head a160347eab66, which was gated this morning, and an overlapping set on develop 9105cfdee484 itself.
- The 2 "Pre-merge acknowledged" failures are the unticked boxes. Per card `secuura-premerge-block-nine-prs-1113` = c, they do not hold a merge.
- **Not fixable in this PR.**

**G349-2226-5 (Info; override range).**
- **Where:** `Blockchain/Dev/package.json:101` and `services/originate/package.json:60` keep `@hono/node-server ^2.1.3`. That range still admits the vulnerable 2.1.3–2.1.5.
- **Why it is harmless today:** the complete locks pin 2.1.8, `npm ci` honours the lock, and every Dockerfile uses `npm ci` (31 `npm ci` Dockerfiles; the only `npm install` text in a Dockerfile is a comment in kyc). So the range is harmless today.
- **Optional hardening for a later row, not this one:** raise both floors to `^2.1.6` (out of scope here; the brief forbade manifest edits).

No finding against lock integrity, the census, the audit legs, the install, merge-tree, or the body or ticket.

## TESTED

**Q1 Lock integrity** (python structural JSON diff of both locks, develop vs head; `scratch/` instrument inline):
- Root lock:
  - top-level keys: 0 differ;
  - `packages`: 1955 = 1955 entries;
  - exactly ONE changed entry, `node_modules/@hono/node-server`, with fields changed = {version, resolved, integrity}.
- mcp-server lock: the same, with 302 = 302 entries.
- Entries carrying `libc`/`os`/`cpu`: root 137 → 137, mcp-server 53 → 53. The hono entry has none on either side.
- **Control:** a planted version change on `node_modules/hono` is detected by the same differ.
- `integrity` equals `npm view @hono/node-server@2.1.8 dist.integrity` (sha512-jdf7FHh6…Qv7bEA==) and the integrity of my own `npm pack`.
- `resolved` = `https://registry.npmjs.org/@hono/node-server/-/node-server-2.1.8.tgz` = `npm view … dist.tarball`.
- The entry's `engines` (`node >=20`) and `peerDependencies` (`hono ^4 || ^5.0.0-0`) equal the 2.1.8 tarball's package.json, which declares no `dependencies`.
- sha256 at dc57df60, develop and head, all identical:
  - root package.json 991d4f5a…;
  - mcp-server package.json 6980207c…;
  - `Blockchain/Dev/scripts/audit/audit-baseline.json` d6e7f1ed…fd21aa (the READY's value).
- GitHub advisories API, read now: 9 advisories for the package; none names 2.1.6, 2.1.7 or 2.1.8. `latest` = 2.1.8.

**Q2 Census** (`scratch/census.py`, JSON parse of every `package-lock.json` blob in the commit tree, both `packages` and legacy `dependencies`):

| Ref | Locks tracked / parsed | Carriers | Versions | Locks with none |
|---|---|---|---|---|
| develop | 47 / 47 | 2 (root, mcp-server) | 2.1.5, 2.1.5 (flagged vulnerable) | 45 |
| head | 47 / 47 | 2 (root, mcp-server) | 2.1.8, 2.1.8 (not vulnerable) | 45 |

- The positive control is the develop row: it finds the 2 carriers the hook names.
- Other lock formats (pnpm-lock, yarn.lock, npm-shrinkwrap, bun): 0.
- The manifests naming hono are only the two overrides (G349-2226-5).
- Every Dockerfile installs with `npm ci` from a committed lock. The mcp-server Dockerfile copies its own `package-lock.json` in both stages.
- So nothing else can pull a vulnerable copy at build time.
- The out-of-scope `mobile/secuura-app` lock is inside the 47 and carries none.

**Q3 Audit legs, reproduced by me** (fresh worktrees at develop and head, each with its own root `npm ci --ignore-scripts`, Node v26.8.1, npm 11.19.0):

| Leg | develop 9105cfde | head 15914b78 |
|---|---|---|
| `audit:gate` | **rc 1**: "7 distinct advisories reported, 5 baselined", FAIL with 2 NEW (qv5m, jpvv) | **rc 0**: "5 distinct advisories reported, 5 baselined", OK |
| `audit:locks` | **rc 1**: "45 standalone lockfiles (47 tracked − root − 1 out of scope) … 1629 distinct packages pinned — 6 advisories match, 4 already baselined", FAIL with 2 | **rc 0**: "45 standalone lockfiles … 1629 distinct packages pinned — 4 advisories match, 4 already baselined", OK |
| `audit:contract` | rc 0: tests 62, pass 62, fail 0, skipped 0 | rc 0: 62/62, fail 0, skipped 0 |
| id counts (qv5m / jpvv / any GHSA) | gate 2 / 2 / 4; locks 1 / 1 / 2 | gate 0 / 0 / 0; locks 0 / 0 / 0 |

- The head's pass is not a vacuous one: 45 lockfiles and 1629 packages were checked, and 4 advisories still match (all baselined).
- The develop failure is the control that the instrument sees the two ids.

**Q4 Runtime:** see G349-2226-1 (reachability, read at source + measured by import walk) and G349-2226-2 (the whole dist diff).

**Q5 mcp-server suite, Dockerfile route, reproduced by me.** Setup: `git archive` of `packages/shared` + `services/mcp-server` at each ref into `scratch/iso-{dev,head}` (no workspace root above). Then shared `npm ci --ignore-scripts` + `npm run build`, mcp-server `npm ci --ignore-scripts`, and `node_modules/@secuura/shared` symlinked to that shared copy. All rc 0.

| Run | Installed hono | Result |
|---|---|---|
| head, NO link (control) | 2.1.8 | rc 1: 5 failed / 10 passed files, 62 passed / 75 skipped tests (137). All 5 fail on "Cannot find package '@secuura/shared/zod3-compat'". This is exactly the known build-shape fault. |
| develop, linked | 2.1.5 | rc 0: **15/15 files, 137/137 tests** |
| head, linked | 2.1.8 | rc 0: **15/15 files, 137/137 tests** |

- `tsc --noEmit -p tsconfig.json`: rc 0 with 0 output lines at both. tsc lists 10 src files. Control: tsc on a planted `const n: number = "x"` gives rc 2, TS2322.
- **In-process smoke** (`scratch/smoke.mjs`, NODE_ENV=test, the BUILT dist at each ref, run on 127.0.0.1 only):
  - mcp-server's real HTTP entry: GET /health 200; POST /hash `{}` 400 BAD_REQUEST; POST /hash with content 200, sha256. Identical at develop and head.
  - As a contrast on the hono path the repo does not use: the SDK's `StreamableHTTPServerTransport` (stateless, SSE). It loaded hono 2.1.5 at develop and 2.1.8 at head. `initialize` 200 SSE, `tools/call ping` 200 "pong", a client abort mid-stream left the process alive. Identical both sides.

**Q6 Root install:** `npm ci --ignore-scripts` rc 0 at develop and at head ("added 1794 packages" both). `npm ls @hono/node-server --all`, rc 0:
- **develop:** 2.1.5 under `@secuura/mcp-server → @modelcontextprotocol/sdk@1.32.1`, and "2.1.5 deduped" under `@secuura/originate → prisma@7.8.0 → @prisma/dev@0.24.3`.
- **head:** 2.1.8 at both, the second "deduped".
- One physical copy on disk in each tree (`find` of `node_modules/@hono/node-server/package.json` = 1). Its version is read from the file.

**Q7 merge-tree** (`--write-tree`, in my clone, each side's own merge-base):

| Merge | rc | Tree |
|---|---|---|
| develop × 2226, both orders | 0 | 630e31d69ee2 |
| 2099 × 2226, both orders | 0 | 64bbd936240a |
| planted conflict: develop + the hono `version` line set to 2.1.7, × 2226, both orders | **1**, conflict in `Blockchain/Dev/package-lock.json` | (conflicted) |
| twin: develop + head's root-lock blob, × 2226, both orders | 0 | 630e31d69ee2 |

- **Survival:** 630e31d69ee2 vs develop differs in exactly the 2 locks, with blobs equal to the head's (1918ff80e47c, 36cafc0004f1). Against the head it differs in exactly develop's 2 moved paths, whose blobs equal develop's (006a4d35aa16, a91eb7e6085c).
- The Dependabot pairs are in G349-2226-3.

**Q8 Body and ticket:**
- **PR (GitHub API):** open, not draft, base develop, head = pin, mergeable true (mergeable_state `unstable`, the CI of G349-2226-4). 2 files, +6 −6.
- **Body (59 lines):**
  - Test Evidence is present. It has the Node line, a BEFORE/AFTER table, the hook verdict quoted as "PREFLIGHT INCOMPLETE — 13/16 … This is NOT a pass", NOT covered, and "Before this deploys: nothing deploys from this PR; deploy is Kam's tap".
  - **Self-hold regex: 0 hits.** Control: "Do not merge until the pre-merge tests have been run." gives 1.
  - Close words: 0 (control "Closes KS-1" gives 1). `Refs KS-2194` is in the Summary. The commit message has `Refs KS-2194` and the Sonnet trailer.
  - The docs escape clause cites SKILL.md section 4, lines 483-484. At the head those lines read "If a change genuinely does not affect either doc, **say so explicitly and why** — do not silently skip." (section 5 starts at 488). The body says so and why.
  - The ack boxes are PRESENT and unticked. Unlike gate 348's PRs, this body does carry them.
- **KS-2194** (Linear GraphQL, read-only, key read inside python and never printed):
  - In Progress, priority 1, assignee the board account, project "Dependency and Version Currency".
  - Attachment: PR 2226. One comment, 4c4db94b…, 2026-11-13T00:15:35Z, 1445 characters, names 2226.
  - The title and BLUF scope is "in-range lock refresh 2.1.5 -> 2.1.8 in the root lock and services/mcp-server … lock-only … no package.json edit, no audit-baseline row, no code change". **The PR matches it exactly.**
  - `Refs` (not a close word) follows the brief. The ticket stays for the merge seat or the owner to close.

## HOW
- **Clone:** `scratch/clone`, `git clone --shared --no-checkout` of the Blockchain checkout, push URL `DISABLED` (re-read at the end), `core.sshCommand` copied from the project config.
- **Refs:** develop and PR heads 2226, 2099 and the ten Dependabot PRs, fetched BY URL into `refs/gate/*` of my clone only.
- **Worktrees:** `scratch/wt-dev` and `scratch/wt-head` (full, detached at the pins, clean at the end).
- **Isolated copies:** `scratch/iso-dev` and `scratch/iso-head`.
- **Logs:** `scratch/*.log`, `census.out`, `openprs.out`, `plant.out`, `smoke-*.log`, `pr2226.json`, `pr2226_body.md`, `KS-2194.json`.
- **GitHub:** read-only via `gh api` with the Blockchain gh config (kksecura confirmed by `gh auth status`).
- **In the Blockchain project:** only `ls-remote`, `config --get` and `cat-file`.
- **Leftovers (in `scratch/`):**
  - `plant_*.json` / `.idx` files;
  - in my clone only: two unreferenced plant commits (a3cab5b59c01 conflict, 89ffcf2bd212 twin), never pushed.
  - A first `plant.sh` run failed on a missing git identity and created nothing. I re-ran it with a scratch identity in env.

## NOT TESTED
- Node 24 / the `node:24-alpine` docker route; image build; deploy.
- Schemathesis, Akto, Playwright, k6.
- The full 16-leg pre-push hook (I ran legs 5, 6 and 7 as npm scripts only).
- `prisma dev` itself.
- A live MCP client against a deployed mcp-server. The smoke was in-process on localhost, at develop and head.
- The 2.1.6 → 2.1.8 behaviour at runtime beyond that smoke. Specifically, the removed catch (G349-2226-2) was read, not exercised with a rejecting body stream.
- Merges of the stale Dependabot PRs beyond merge-tree.
- The CI jobs: none ran (billing; G349-2226-4).
- The other services' suites. No other service consumes hono per the census and `npm ls`.
