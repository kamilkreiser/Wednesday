auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
[QA -> Wednesday] TIER 1 GATE #1033 (KS-763) 2cab54988 — GO WITH FINDINGS
Composed 2026-09-17 23:35:08 AEST (from `date`). QA agent, round 1 of 2.

VERDICT: GO WITH FINDINGS
- Head: 2cab54988b4e7b71d403576719f5fd80e470fa92.
- Merged tree: ad795aa72a32a1ba045dbe87f20608c4cfa2fbcd, over the LIVE develop 732c13459d76f5b05ade94bb91de7e47585b0e7d.
- Develop moved twice after the draft: 27e53ec3a (#1029), then 732c13459 (#1031 KS-1213).
  - #1031 changes originate SOURCE: src/routes/certifications.ts, src/routes/documents.ts, and one new test.
  - It touches 0 of the 5 PR paths.
  - The merged tree was built, suite-run and start-traced on its own.
- No finding blocks the merge. All findings are RECORD-class.

Head re-verified at origin:
- ls-remote refs/pull/1033/head and the branch = 2cab54988 at 23:18:35, 23:21:38, 23:28:03 and 23:33:55.
- PR API head.sha = 2cab54988 at 23:27:00 and 23:34:08.
- Develop 732c13459 at all four readings.

BLUF
1. RUNTIME REACH
- Which mysql2 ships: the originate runtime tree (Dockerfile :79 `npm ci --ignore-scripts --omit=dev`, which reinstalls from scratch, then :86 .prisma and :89 /shared) moves mysql2 3.15.3 -> 3.23.1.
  - It also adds sql-escaper 1.5.2 and drops seq-queue 0.0.5 and sqlstring 2.3.3. Nothing else moves.
  - Measured on host npm 11.5.1 and on node:24-alpine npm 11.19.0 (arm64).
  - 304 -> 303 packages. 96 differing files: 95 in those 4 dirs + node_modules/.package-lock.json. .prisma is byte-identical.
  - Positive control: the FULL :30 install moves the same 4.
  - Determinism head vs head2 is 0/0 on both routes. Merged tree vs head is 0/0.
- Which trees carry mysql2: only originate's runtime tree.
  - Parse of all 45 tracked locks at head, base, develop and merged: 2 carry mysql2 (root, originate). Control: express is in 28 locks.
  - Of 37 tracked Dockerfiles, only originate's installs either lock. None installs the root lock.
- Does anything load it: NO.
  - In-process `node dist/index.js` starts in the Dockerfile-shaped runner loaded 0 mysql2 / sql-escaper / sqlstring / seq-queue files.
  - Starts traced: host base, head and merged (NODE_ENV=development); host head and merged under NODE_ENV=production (a throwaway 64-hex PII key generated in-process, never printed; "PII encryption keyring initialised"); alpine base and head.
  - Every start ran the Prisma adapter-pg path: `[DB] Prisma connection failed` x1, /health 503, listener 127.0.0.1 only, SIGTERM to the verified pid (argv + cwd), exit 0.
  - POSITIVE CONTROLS, same hook, same tree: `require('mysql2')` 82 files and `import('mysql2/promise')` 89 at head; 77 / 79 at base, with sqlstring.
  - `npx prisma generate` traced: 0 mysql2 files (control: prisma CLI 3).
- Cause-side census over the runner node_modules, with markers inside the mysql2 subtree as positive control:
  - `compressed_protocol`: outside 0.
  - `mysql_clear_password`: outside 1 = @prisma/query-plan-executor 7.2.0's bundled mariadb@3.4.5 (F3).
  - No bundled mysql2 copy ships.
2. PIN CONFLICT: the override holds.
- `npm ci` on originate's own lock succeeds without --legacy-peer-deps, rc 0 on both routes.
- `npm ls mysql2` = `prisma@7.8.0 └── mysql2@3.23.1 overridden`. Not invalid.
- FULL `npm ls --all`: rc 0, 0 invalid, 3 overridden (base: 2). The RUNTIME tree's rc 1 is identical at base and head (10 missing devDependencies): instrument.
- `prisma generate` rc 0, tsc rc 0.
- originate `jest --runInBand`:
  - host base 63/63, 656/656 (load1 17.6->16.0);
  - host head 63/63, 656/656 (16.0->15.7);
  - host MERGED 64/64, 741/741 (15.7->15.8; includes develop's ks1213 test);
  - alpine base 63/656 (ctr loadavg 1.54->1.69);
  - alpine head 63/656 (0.86->1.04).
3. ADVISORY CLOSED THROUGH THE SHIPPED GATES (my worktrees; scripts/audit `npm ci` lock sha 84ba271fc131d8a5 unchanged; no root node_modules; load1 13-15)
- H1 head + 29 rows: audit-gate rc 0 "28 distinct advisories reported, 29 baselined."; audit-locks rc 0 "43 standalone lockfiles"; 0 CLEANUP.
- H2 head + base's 31 rows: CLEANUP exactly GHSA-3f6p-5ww8-9rcr + GHSA-rgwj-5xj2-c3m3, printed by audit-gate.mjs:210-211. audit-locks lists none: its stale filter at :298-300 keeps only scope standalone-locks rows.
- NEGATIVE CONTROL, base bb848b828 + base baseline minus the 2 (bytes == head's baseline):
  - audit-gate rc 1: "30 reported, 29 baselined", FAIL "2 NEW advisories" = GHSA-3f6p [high] + GHSA-rgwj [moderate];
  - audit-locks rc 1: exactly the 2, "pinned: 3.15.3", "in 1 lock(s): services/originate".
- Teed from audit-locks' own bulk fetch: rgwj moderate "<=3.23.0", 3f6p high "<3.22.0". Requests: head mysql2 ["3.23.1"]; base ["3.15.3"].
- Shipped semver 7.8.5: 3.21.9 in 3f6p / 3.22.0 out; 3.23.0 in rgwj / 3.23.1 out. 3.23.1 is outside both.
- Gate inputs: develop's (package*.json blobs, scripts/audit tree 822cd1214) == base's; the merged tree's (94/94 blobs, tree bba64599e) == head's.
4. SCOPE BY PARSE
- Root lock 1970 -> 1969, originate 655 -> 654. Exactly 4 entries each, class devOptional unchanged, out-of-subtree 0, class drift 0, packages[""] equal, --omit=dev diff exactly the 4.
- Manifests: only overrides.mysql2 = "3.23.1".
- Baseline 31 -> 29: exactly the 2, 0 added, 0 altered.
- Edges: 10 distinct edges touch the moved entries per lock; 1 unsatisfied = the ruled prisma -> mysql2 "3.15.3".
- NEW: a whole-lock unsatisfied-edge diff. Root 9 -> 10, originate 1 -> 2. NEW at head = only the ruled pin; GONE 0.
- Planted controls on UNMOVED entries all fire: named-placeholders devOptional->dev; express version; a named-placeholders edge.
5. MERGE-IN
- `merge-tree(9fd3cb924, bb848b828)` = head tree e52244863 (control fires).
- It moved exactly develop's 45-file delta: develop-only patch-id 866e99d2096e both sides.
- Both-sides files = root lock + baseline, merge blob == head blob. Per entry 43 + 4, 0 both, 0 mismatch (planted control reported).
- Regeneration re-derived:
  - baseline = develop minus the 2, byte-equal;
  - originate recipe -> 4c1800aee on npm 11.5.1 AND 11.19.0 (control without override -> 040908e22);
  - ROOT recipe `npm update mysql2 --package-lock-only --ignore-scripts` -> 646c19f6f byte-identical ONLY on npm 11.19.0; its trap -> 5bd5680f8; its no-override control -> 5bd5680f8;
  - host npm 11.5.1 is inert (mysql2 stays 3.15.3) and writes 86c3685d8, even for the trap.
- merge-tree --write-tree over LIVE develop 732c13459: rc 0, 0 conflicts, ad795aa72a32a1ba045dbe87f20608c4cfa2fbcd.
  - Delta to the head tree = develop's 4 files since base: the api-gateway ks1072 test, plus originate's ks1213 test, certifications.ts and documents.ts.
6. LINKING (re-read 23:34:08-23:34:50, immediately before this mail)
- attachmentsForURL(pull/1033) = 1: KS-763 [In Progress] linkKind contributes, status open. Controls: pull/1030 -> KS-1211; pull/99999 -> 0.
- 0 closing phrases in the title, the body (8,510 chars; "Refs KS-763" x1), both commit messages, the linear[bot] comment, and KS-763's 10 comments. Planted regex controls hit and miss as designed.
- KS-763: In Progress, completedAt null.
- KS-751: archived 2026-09-05T06:48Z (Tested Not Deployed), 0 attachments to pull/1033. As ruled, so not a defect.
7. DEPENDABOT (record only)
- The root lock is shared with 10: #949 #948 #947 #946 #945 #649 #639 #635 #575 #572.
- #949 (prisma 7.10.0) and #575 (dotenv) also touch services/originate/package.json. #945 and #920 touch the root package.json.
- `npm view` 23:27:53: prisma@7.10.0 still pins mysql2 3.15.3, so the override stays load-bearing.
- Open PRs 21 -> 22: new #1035 (KS-1204) shares 0 files.

REAL-BROWSER HALF OF TIER 1: not applicable. No rendered surface changes (2 manifests, 2 locks, 1 baseline).

FINDINGS (all RECORD)

F1 Polish — MEASURED AT RUNTIME; target: seat evidence + merge addendum; oracle: History / Product
- The READY's root recipe "BYTE-IDENTICAL" holds only under npm 11.19.0.
- On host npm 11.5.1 the same command is inert and writes 86c3685d8; so does the trap. The READY names no npm version.
- Regenerate root locks with npm >= 11.19.0.

F2 Polish — MEASURED; target: seat evidence; oracle: Image
- The READY's "no runtime load trace" is now closed: 0 mysql2 files loaded, development AND production mode, base / head / merged, host + alpine.
- Residual, not traced: post-connection paths, requests beyond /health, prisma CLI other than generate.
- prisma 7.8.0 build/index.js has exactly 1 `import("mysql2/promise")`, inside the Studio server's executor map (mysql adapter). The drafter's "3 hits" = 3 "mysql2" strings.

F3 Polish (curio; TICKET-class at most) — MEASURED census + READ; oracle: Comparable
- @prisma/query-plan-executor 7.2.0 dist/index.js ships in the originate runtime tree: 5,008,761 bytes, sha256 b3f006c009bb4d0b, byte-identical base/head.
- It bundles mariadb@3.4.5 (140 strings, 4 mysql_clear_password, 0 mysql2).
- Not loaded at any traced start. Not mysql2, so outside both advisories.
- Invisible to both audit scripts (#1027 F1 class). An analogous mariadb advisory is not assessed.

F4 Polish — PROBED; target: seat evidence + drafter; oracle: Product
- Edge counts by instrument: READY 9; drafter 11 (it counts mysql2 -> sql-escaper as both a declarer edge and an own-dep edge); QA 10 distinct. All agree on the single BAD edge.
- The 10 pre-existing unsatisfied edges are all declared overrides and unmoved: postcss x3, @cardano-sdk/crypto x5, path-to-regexp (router), deepmerge-ts (@prisma/config).

F5 none — brief/drafter corrections
- Develop is 732c13459 (#1031), not 27e53ec3a, so the merged tree is ad795aa72, not ae3624597.
- Compare develop...head now reads behind 2.
- Host file counts include .bin symlinks (14,978 vs the drafter's 14,965); the 96 differing files are equal.
- Every other drafter number re-derived equal.

F6 none — `npm audit --json` replay
- At head, prisma is still high via @prisma/config and @prisma/dev (pre-existing, baselined; H1 rc 0). At base the via list also named mysql2.

SELF-AUDIT
- My v1 no-override regeneration controls were INERT (O0 host originate, N3 alpine root).
  - Cause: my loops unpacked `override` but never passed it to mk(), so both ran WITH the head manifests and "moved".
  - Caught by reading why the controls were green.
  - Re-run as v2 with the on-disk manifest state asserted ([False, False] / [True, True]): O0v2 -> 040908e22 and N3v2 -> 5bd5680f8 (both 3.15.3); twins -> 4c1800aee and 646c19f6f.
  - v1 output kept.
- Container starts read START_RC=0, not 143. Node's SIGTERM handler exits 0 under busybox timeout; alive at 12 s is proven by the 503.
- A `ps | awk login_stub` count read 6. Two rows were claude processes carrying the prompt text: mine (pid 50312) and another QA session (45537, not #1033).
  - Re-read by argv + cwd: 4 Seat A login_stub listeners, pids 2849 2927 3001 3080, ppid 1, cwd worktrees/raise-0916-a/Blockchain/Dev, started 23:29:55-57.
  - NOT mine, not touched. 0 remained at 23:33:55.
- Start census 23:19:22: 2 node LISTEN rows = pid 47979, a drafter1034 vitest fork (not mine, gone by 23:29). It added host load.
- Bounds:
  - 3 `npm view` reads;
  - 1 `npm audit --json` replay per tree (same request shape as audit-gate);
  - 7 + 2 containers, all qa1033-*, sequential, each removed by its exact name (0 left);
  - nothing removed; no cd; no write verb on the Secuura checkout; no credential echoed.
- Secuura checkout:
  - start 23:21:35: porcelain 0, config f9ef2cb7e4b9fa5a, refs 942, worktrees 112, branch feature/ks-597-b-caller-scoped-externalref;
  - mid 23:28:03: same, refs 943;
  - close 23:33:55: porcelain 0, f9ef2cb7e4b9fa5a, refs 944, worktrees 112, same branch.
  - Porcelain and worktrees are equal start to close.
  - The +2 refs are a seat's ks-1204 branch and remote ref (#1035). Not mine: my clone is --shared and all my git writes are in it.

MERGE ADDENDUM
- Squash 2cab54988 onto develop 732c13459d76f5b05ade94bb91de7e47585b0e7d.
  - Merged tree ad795aa72a32a1ba045dbe87f20608c4cfa2fbcd.
  - The drafter's ae3624597 was over 27e53ec3a, superseded by #1031. #1031 moves originate src, and the merged tree was measured directly: tsc rc 0, jest 64/741, traced start 0 mysql2.
- Linking: #1033 attaches to KS-763 only, linkKind contributes, no closes.
  - KS-763 stays In Progress (Refs, never Closes; no ticket to Done).
  - KS-751 stays archived, untouched.
- Dependabot overlap: the root lock is shared with 10 open Dependabot PRs (#949 #948 #947 #946 #945 #649 #639 #635 #575 #572), which rebase after this.
  - #949's prisma 7.10.0 still pins mysql2 3.15.3, so the override stays load-bearing.
  - #949 and #575 also touch services/originate/package.json.
  - Regenerate with npm >= 11.19.0, not host npm 11.5.1.
- Equality targets:
  - scripts/audit/audit-baseline.json 91d8b71c9 (29 rows, both GHSA absent);
  - Dev root package-lock.json 646c19f6f;
  - root package.json 773443a9f;
  - services/originate/package-lock.json 4c1800aee;
  - services/originate/package.json d4435238d.
  - Checked at head AND the merged tree: all 5 equal; develop holds the base blobs.
- Unchanged: services/originate/Dockerfile ac2fb91bf and prisma/schema.prisma 96c3342fa (base, head, develop, merged).
- Gate re-measures on the squash:
  - audit-gate rc 0 28/29 and audit-locks rc 0 43 scanned, 27/27, 0 CLEANUP;
  - originate runtime mysql2 3.23.1 (+sql-escaper 1.5.2, no sqlstring/seq-queue);
  - 0 mysql2 files loaded at start.
- Records:
  - F1 root recipe is npm-version dependent (11.19.0 reproduces; 11.5.1 is inert and drifts to 86c3685d8);
  - F2 load trace closed, with the residue named (post-connection, Studio mysql executor);
  - F3 bundled mariadb@3.4.5 in @prisma/query-plan-executor ships unloaded;
  - F4 edge count 9 / 11 / 10 by instrument, 1 BAD agrees;
  - F5 develop 732c13459, merged tree ad795aa72;
  - QA self-audit: v1 no-override controls inert, fixed by v2.

NOT TESTED (same prominence)
- Not applicable:
  - the real-browser half of tier 1 and human-emulation persona dimensions (no rendered surface);
  - any MySQL datasource path (none exists).
- Image and platform:
  - image build; the deployed amd64/musl npm (my alpine is arm64, 50c8e8ca1d27);
  - apk (:23 :55 :73) and native builds;
  - :94 chmod and USER secuura.
- Load-trace residue:
  - post-connection paths; requests beyond /health;
  - prisma CLI other than generate (Studio's mysql2/promise; prisma migrate — the migrations job uses psql, READ by the drafter only);
  - live Redis / anchoring / auth upstreams.
- Alpine route:
  - merged tree not run in alpine (host only; its locks == head's);
  - alpine FULL determinism pair not run;
  - alpine production-mode start not run.
- Out of scope by the brief:
  - other members' suites (trees unmoved by parse);
  - packages/shared's suite (0 files moved, content digest equal base/head/merged);
  - the READY's host root-install originate run (I ran the Dockerfile's standalone-lock route);
  - lockfile-cleanroom.sh;
  - preflight.sh whole, the in-hook preflight, the real pre-push hook, any push (forbidden);
  - live Schemathesis / Akto / Playwright / k6, stack, kintsugi, demo, az.
- Evidence not re-derived:
  - whether mariadb 3.4.5 has an analogous advisory;
  - the READY's import-grep counts;
  - whether the 12 host-npm flag drifts reached any committed lock;
  - the drafter's ae3624597 over 27e53ec3a (superseded).
- Structural: a later advisory-feed change.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks763-1033-2cab54988-tier1-r1/report.md
NOT-TESTED written first (23:19:31): /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks763-1033-2cab54988-tier1-r1/NOT-TESTED.written-first.md
Evidence + scripts: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks763-1033-2cab54988-tier1-r1/evidence/
