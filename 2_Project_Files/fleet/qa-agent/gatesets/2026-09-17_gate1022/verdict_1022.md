SUBJECT: [QA -> Wednesday] TIER 1 GATE #1022 (KS-1211) ff49d0242 — GO WITH FINDINGS
TS: 2026-09-17T09:04:39.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA -> Wednesday

TIER 1 GATE R1: #1022 (KS-1211, Seat B) @ ff49d0242a8ae764155d427232b15647c6bfa849 — GO WITH FINDINGS
Also GO WITH FINDINGS on the merged tree 1b03e6951f447a28c60bf69d2ebbed426a272697 over develop 81ee4b729e86a645fc9098aafa1aaf39035a9950.

Timing (from date): session 18:43:50–19:03 AEST. Head verified at origin 18:45:09 and again 19:02:51 (ls-remote pull head + branch + PR API). Develop was 81ee4b729 at 18:45:09, 18:52:48 and 19:02:51.

BLUF

1. RUNTIME REACH (lead): no shipped mcp-server path loads hono, on develop or on head.
   - I installed mcp-server the Dockerfile way OUTSIDE Blockchain/Dev, at head and at develop (npm ci / tsc / npm ci --omit=dev; lock sha unchanged). Installed hono: head 4.13.8, develop 4.13.0.
   - A per-process module census (module.registerHooks resolve, delivered by NODE_OPTIONS) counted 0 hono resolutions in each of:
     (a) the stdio entry dist/index.js, driven by the SDK Client: initialize, tools/list (9), hash on a scratch file, missing file, fail-closed connector_info (API at a refused loopback port), unknown tool (-32602), wrong-typed argument, missing argument;
     (b) the image CMD dist/http-server.js on 127.0.0.1:0 (loopback-pin preload, source not edited), over real HTTP in two modes, NODE_ENV unset and NODE_ENV=production as in the image. Routes: /health, /hash (content, filePath, {}, NUL, malformed JSON, 413), /register, /verify, /documents, /workflow, /connector and /policy fail-closed, /generate-package (bad type, no key, zip), /mcp 404;
     (c) the SDK StreamableHTTPServerTransport with the real compiled tools. This is NOT a shipped path. It loads @hono/node-server once and hono 0 times.
   - Positive controls, same instrument: ESM import('hono') 39 on develop / 43 on head; CJS require('hono') 34 / 36. Taken in a standalone process and again inside probe (c)'s own process after its run.
   - Responses are identical base vs head in (a), (c) and production-mode (b). The only volatile fields are named and proven: stack-trace absolute paths in dev mode (stderr equal after path normalisation), and a timestamp in the generated zip. With the clock pinned, the zip matches on all 6 entries by name, CRC and size.
   - The premise that mcp-server uses the SDK HTTP transport is FALSE at source: src/index.ts:3,19 uses StdioServerTransport; src/http-server.ts:7,28,272 is express app.listen; the Dockerfile has CMD ["node","dist/http-server.js"].
   - Static corroboration: in the runtime tree, the only files outside hono that import bare hono are @hono/node-server serve-static and the SDK's examples/ hono file. None loaded.
   - LISTEN census (lsof), node rows:
     - start 18:46:15: 0;
     - 18:49:18: 4 foreign rows (pids 67519, 67523), not mine;
     - MID while (b) was up: exactly the child pid + port (e.g. 69433 on 127.0.0.1:52793). Argv and cwd were verified, then SIGTERM by pid;
     - after 18:49:37: 0; close 19:02:51: 0.
   - login_stub.mjs processes: 3, none mine, left alone.

2. hono 4.13.8 itself, on the installed bytes (base vs head):
   - crvj: "http://x/p#frag?a=1" reads a = "1" on 4.13.0 and null on 4.13.8, both via getQueryParam and via a raw request-target through @hono/node-server. Controls ?a=1 unchanged.
   - g6gw: parseBody({dot:true}) at depth 5000 gives 200 on 4.13.0 and 500 "Nesting limit exceeded" on 4.13.8. Bisected limit: 33 OK, 34 fails. Control depth 3 unchanged.
   - gqvv (toSSG): NOT differentiated. My route-param shapes wrote inside the output dir on both versions.

3. originate: hono SHIPS in its image too. The --omit=dev runtime stage (Dockerfile:79), reproduced at head, installs hono 4.13.8, @hono/node-server 1.19.11, @prisma/dev 0.24.3 and prisma 7.8.0, all devOptional. Control: @babel/core (dev) is ABSENT. Nothing loads hono: 0 of 117 src files import hono, @hono/* or @prisma/dev (controls: prisma 52, express 53). @prisma/dev's only importer is prisma/build/index.js (the CLI), and run-migrations.sh uses psql.

ITEMS

Item 1, runtime reach: as above. NOT driven: originate dist/index.js start (needs builder-stage prisma generate, network behaviour unverified, plus a DB URL); gqvv differential; anything behind a live Secuura API beyond its fail-closed branch.

Item 2, gates, from Blockchain/Dev in my worktrees. scripts/audit npm ci, lock unchanged, no root node_modules. Bulk response and npm audit stdout teed in-process; tee transparency control: H1 with and without the tee gives equal rc and byte-equal stdout.
- H1, head + real baseline (34): audit-gate rc 0, "33 distinct advisories reported, 34 baselined.", 0 CLEANUP. audit-locks rc 0, "43 standalone lockfiles … 32 advisories match, 32 already baselined.", 0 CLEANUP.
- H2, head + develop's baseline (37): audit-gate rc 0, CLEANUP exactly GHSA-crvj-82cr-hjcx, GHSA-g6gw-c38x-mqfc, GHSA-gqvv-2mrq-wpjv. audit-locks rc 0, no CLEANUP.
- B0, develop + real baseline: rc 0 "36 reported, 37 baselined" / rc 0.
- B1, develop + head's baseline: audit-gate rc 1, exactly the 3 [moderate] hono. audit-locks rc 1, exactly the 3, "pinned: 4.13.0 / in 2 lock(s): services/mcp-server, services/originate".
- CLEANUP by line: audit-gate.mjs:203-212 excludes scope standalone-locks and exits 0 (:216). audit-locks.mjs:298-300 lists only standalone-locks rows (printStale :334).
- Teed bulk response (B1 request hono ["4.13.0"]): all three vulnerable_versions "<4.13.5", moderate. H1 request ["4.13.8"]: 0 hono advisories. npm audit via[].range: "<4.13.5" x3; H1 has no hono entry.
- Shipped semver 7.8.5: 4.13.0 true, 4.13.8 false; controls 4.13.4 true, 4.13.5 false.
- Declarers, read from the head locks: sdk ^4.11.4 (mcp-server, root), @prisma/dev ^4.12.8 (originate, root), @hono/node-server peer ^4 (x4). 4.13.8 is inside all of them; the out-of-range controls (5.0.0, 3.12.0, 4.11.3, 4.12.7) are all false.

Item 3, scope by parse, develop 81ee4b729 vs head:
- mcp-server lock 312/312, originate 655/655, root 1970/1970. Only node_modules/hono moves in each (version/resolved/integrity 4.13.0 -> 4.13.8; flags unchanged).
- Root lock: exactly the 12 ruled entries, each checked against the ruling and found in the PR body. Eleven lightningcss-{android-arm64, darwin-arm64, darwin-x64, freebsd-x64, linux-arm-gnueabihf, linux-arm64-gnu, linux-arm64-musl, linux-x64-gnu, linux-x64-musl, win32-arm64-msvc, win32-x64-msvc} change dev+optional -> optional; magicast changes dev -> devOptional. 0 version fields, 0 unexpected.
- Control: a planted unruled dev flag plus a planted lightningcss version gave 2 unexpected, both named. The service locks' planted-version controls gave 1 each.
- The 3 lock blobs at head are identical to 58684e653 (the merge commit brought no lock byte). 0 manifests changed.
- Baseline: 34 = develop's 37 minus exactly the 3. 0 added, 0 altered, $comment equal, order kept; bytes equal the json.dumps round-trip. Against 58684e653 only GHSA-2wm5-q62r-hmrv is gone. Planted reason-change control: 1 altered.
- Three-dot: 4 files, 2 commits; -w numstat equals plain numstat; PR files API and compare API agree (ahead 2, behind 0).

Item 4, clean-room, builds, suites:
- lockfile-cleanroom.sh services/originate services/mcp-server (host node 24 path, docker never called): head rc 0 2/2 OK; develop rc 0 2/2 OK.
- Control: head mcp-server zod ^3.24.0 -> ^9.0.0 gave rc 1, FAIL services/mcp-server, originate OK. Restored sha-identical, porcelain 0.
- mcp-server tsc rc 0 on head and develop.
- Root npm ci --ignore-scripts in my worktrees: hoisted hono 4.13.8 at head, 4.13.0 at develop.
- originate jest: rc 0, 62/62 suites, 637/637 tests, on BOTH trees.
- packages/shared vitest, sequential: rc 0, 44/44 files, 851/851 tests, on BOTH trees.
- CURIO: the first shared run, both trees in parallel at load about 39 (another gate's vitest workers were live), showed 2 failed / 849 on both trees. Both were 5 s timeouts in the source-scanning guards crypto-agility.guard and ks764-key-revoke-call-site-guard. Those 2 files alone: 17/17 on both; the sequential full run: 851/851. Load-induced, not the PR.

Item 5, merge: the then-current develop 81ee4b729 (re-read 18:52:48) plus head gives merge-tree rc 0 = 1b03e6951 = the head tree; the reversed order and a commit-tree squash simulation give the same tree. Delta vs head: none. Delta vs develop: the 4 PR files. Audit inputs are blob-identical between merged tree and head (4 PR files, audit-gate 8e236ee70, audit-locks aff23b042, lock-discovery 3dd903b52, baseline-contract 2504d9a28), with 34 rows. #1021 landed as predicted: develop tree 207ba797c equals the drafter's #1021 prediction, and #1022 on top gives 1b03e6951, clean, 34 rows. RULING on HEAD MOVED: the seat re-ran the gates, not the suites, and that was correct. The merge brought only the baseline, 3 api-gateway files and 2 systemTest locks, none of which a suite reads. My re-run at ff49d0242 confirms 637/637 and 851/851.

Item 6, linkKind: re-read at 19:02:51, immediately before this mail.
- attachmentsForURL(pull/1022) = 1: KS-1211 [In Progress], completedAt null, linkKind 'contributes', closedAt null. Control pull/99999 = 0.
- 0 closing phrases in title, body ("Refs KS-1211" x1), both commit messages, the linear[bot] comment, 0 review comments and 0 reviews. Controls "Fixes KS-1211", "closes #12", "Resolves: KS-1211" and a linear URL all hit; "Refs"/"Part of" do not.
- RULING §5f: a shipped-but-unloaded dependency IS a §5f runtime-behaviour change for the TICKET (not a PR blocker). The bytes of two runtime images change, and "unloaded" is established only offline, for driven paths plus a static scan, which is exactly what §5f says is not enough (SKILL.md:526).
  - A live sweep could add: the image's own npm installing these bytes, both images booting healthy in production env, and the REST mirror and originate answering.
  - It could NOT exercise the advisory behaviour, because no deployed path loads hono. KS-1211 stays In Progress.

FINDINGS (none block the PR)
- F1 RECORD: the lead-question premise is false at source (see BLUF 1). Target: seat evidence and brief.
- F2 RECORD: hono ships in the originate image too (devOptional kept by --omit=dev). The seat's reach statement is incomplete. The §5f sweep should name originate. Target: TICKET KS-1211.
- F3 RECORD/Polish: 4.13.8 caps parseBody dot nesting at 33. Nothing shipped uses it; context for any future hono consumer.
- F4 RECORD: the seat's "32 match, 32 baselined" and the drafter's "43 standalone lockfiles" are the same summary line. Reconciled.
- F5 RECORD: the HEAD MOVED re-measure covered what the second PR owed (ruled above).
- O1 OPEN, out of scope and pre-existing (NOT introduced by #1022; mcp-server/src tree identical at develop and head), for routing:
  - mcp-server's REST mirror POST /hash accepts a caller-supplied filePath and returns the SHA-256 of any server-local file. MEASURED: 200 for my scratch file via HTTP.
  - On error it returns err.message (ENOENT plus the path, so it reveals whether a file exists; READ http-server.ts:41-62).
  - No auth middleware is mounted (:29,33).
  - Severity depends on whether the deployed port is reachable by untrusted callers (not measured). Major if it is.

Own-tooling corrections (public):
- Four of my scripts printed "rc $?" after a $(date) substitution, which reset it to 0. Every rc quoted here was re-measured with rc on its own line (s16), plus an "npm error" line count of 0 in every install/build/test log (controls: the failed vitest logs, 7 each).
- My first login_stub count used pgrep -f from the tool line, which matched its own shell. Replaced with a ps scan from a script.
- One limit-probe first run died on a relative path. Quarantined and re-run.

MERGE ADDENDUM: squash ff49d0242 onto develop 81ee4b729e86a645fc9098aafa1aaf39035a9950 (merged tree 1b03e6951f447a28c60bf69d2ebbed426a272697; drafter and seat 1b03e6951 = the head tree over 81ee4b729); #1021 already merged and merged in; #1022 attaches to KS-1211 only, linkKind contributes, no closes; KS-1211 stays In Progress (§5f: hono ships in the mcp-server and originate images; live sweep owed; Refs, never Closes; no ticket to Done); equality targets root package-lock.json blob 99db3e7c2, audit-baseline.json 45ef8220f (34 rows), services/mcp-server/package-lock.json f942d659b, services/originate/package-lock.json d91d746ef; audit-gate rc 0 33/34 and audit-locks rc 0 43 scanned (re-measure); Records: F1 lead premise false (stdio + express, hono 0 resolutions, controls ESM 39/43 CJS 34/36); F2 hono also ships in originate's --omit=dev image; F3 4.13.8 parseBody dot limit 33; F4 "32 match" = "43 lockfiles" same line; F5 suites-not-re-run ruled correct (637/637, 851/851 re-run at ff49d0242); O1 pre-existing mcp-server /hash filePath disclosure, out of scope, for routing; curio shared vitest timeouts under parallel load.

Checkout readings (START 18:45:09 / MID 18:54:42 / CLOSE 19:02:51), identical at all three: porcelain 0; .git/config sha256 d7e7298b02c45f52; for-each-ref 925; .git/worktrees 112; origin develop 81ee4b729; refs/pull/1022/head ff49d0242. No push, hook or preflight in the checkout; no seat worktree or other gate's clone entered; no docker, az, stack or prisma dev.

NOT TESTED (same weight as the findings)
- Not applicable:
  - real-browser half of tier 1 (no rendered surface; 4 non-UI files);
  - docker, clean-room/regen containers and image builds (forbidden), so the images' own node/npm were not used and host node 24.7.0 / npm 11.5.1 stood in;
  - shared stack, slots, kintsugi, demo, az, mnemonic;
  - the live stack sweep §5f owes (still owed on KS-1211);
  - preflight.sh whole and the in-hook preflight (legs 2/6/7 run directly instead);
  - Schemathesis, Akto, Playwright, k6;
  - any prisma dev command.
- Not run, with blocker:
  - GHSA-gqvv toSSG differential: attempted, not differentiated; the advisory's trigger shape was not found in the time-box;
  - originate dist/index.js start census and originate build: need prisma generate (network unverified) and a DB;
  - prisma CLI census: relayed from the drafter;
  - the seat's allow-list checker and the node:24-alpine no-op flag control (own parse used instead; the control needs docker);
  - mcp-server placeholder vitest (no evidence);
  - jest-internal resolution of hono: jest bypasses Node resolve hooks, so "cannot fail on hono" rests on 0 static imports.
- Beyond this gate: tools behind a live Secuura API beyond their fail-closed branch; deployment exposure of the mcp-server REST port (O1 severity); future wiring of the SDK HTTP transport, hono/ssg or prisma dev.

REPORT: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1022-ff49d0242-tier1-r1/report.md (NOT-TESTED.written-first.md written 18:44, before any run; evidence/ holds raw outputs, scripts and census files)

QA agent (findings only — nothing fixed, merged, pushed, commented on, filed or ticked; nothing sent to Peter or Stuart)

