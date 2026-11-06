BATCH: GO WITH NOTES (PR 2032 GO WITH NOTES, PR 2036 GO WITH NOTES)
PR 2032 (KS-864, head 375084cf53d4): GO WITH NOTES
PR 2036 (KS-1841 F2, head 3f5df055343e): GO WITH NOTES

# Gate 217, tier 1, round 1 of 2

A GO is a statement about the two SHAs above; a moved head expires it. Measured 2026-11-06 13:18 to 13:43 AEDT. Node v26.8.1 (not the 24 the images use), macOS Darwin 27.2.0. Dependencies: APFS copies of the finished gate 204 clone's node_modules (`2026-11-05_gate204-ks1460-pr2013/repo`), all locks byte-compared equal; `packages/shared` rebuilt in each of my trees.

## BLUF

Neither PR has a product defect that I could find, and the seat's main figures reproduce exactly. PR 2032's probes change only the three portal URLs, 8080 is right for all three portals, and no reader in the tree newly faults on `degraded`. PR 2036's named COPY leaves everything that reads the directory working, because the one reader in the image reads that one file.

What the notes come to:

1. **The one state KS-864 item 4 exists for has no test.** Kintsugi's F-1 was portals reading `unreachable`. A mutant that lets an `unreachable` portal stay `operational` passes all 66 cells. The product is correct today (I measured it over real sockets); nothing holds it there. I would fix this one in round 2.
2. The seat's reader census missed one real reader. Its conclusion still holds.
3. "The summary counts do not move" is true of item 4, not of the PR: item 3 moves them, and the admin Services Online tile, from 18 to 21.
4. A red portal now reads "System Degraded" while its only advice says it is optional and names a directory that does not exist.
5. PR 2036: the READY softens the wording Wednesday ruled, and the `find` is now dead except for one host-local route.

Not shown by anyone: a portal reading healthy through real nginx, a full image build, any box.

## Findings

Severity is technical impact. Priority is yours.

### F-1 Medium. PR 2032: no cell pins the headline for an unreachable portal
- **Where:** `services/api-gateway/src/__tests__/ks864f-a-red-frontend-makes-the-headline-degraded.test.ts`. Its stub only ever answers 503 or 200 and never throws. `ks864e` does throw, but every required service is down there and it asserts no headline.
- **FOUND:** `allFrontendsHealthy` can be weakened to tolerate `unreachable` and all 66 cells stay green (ks864a to f, ks1101, ks1248, ks1258).
- **TESTED, MEASURED AT RUNTIME:** two of my mutants, each with its anchor asserted and the file restored by sha256: `every(s => s.status === 'healthy' || s.status === 'unreachable')` and `!some(s => s.status === 'unhealthy' || s.status === 'degraded')`. Both 0 red of 66. Control, the seat's `|| true` mutant, 4 red. Evidence: `evidence/tampers_2032.out`.
- **Product today, MEASURED AT RUNTIME:** correct. Real loopback sockets and real fetch, no stub (base then head): verifier refused, `operational` then `degraded`; verifier 404, `operational` then `degraded`; issuer hanging past 5 s, `operational` then `degraded`; all portals HTML 200, `operational` both; a 301 then 200, `operational` both. `/status/simple` 200 `ok` in every row. Evidence: `evidence/real_socket_base.json`, `evidence/real_socket_head.json`.
- **Oracle:** Purpose. This is the F-1 failure the ticket names.
- **Fix-shape:** add a cell where a portal's probe rejects (a stub that throws for one hostname, the rest up), expecting that portal `unreachable` and the headline `degraded`. Both mutants above should then red it. Test-only; the head moves, so the verdict expires with it.

### F-2 Low. PR 2032: the reader census missed a reader; its conclusion holds
- **Where:** `Blockchain/Dev/tests/e2e/tests/recruitment/fixtures/recruitment-helpers.ts:123`, `checkSystemHealth`, reached through `API_ENDPOINTS.system.status` in `recruitment-data.ts:364`. It is the `beforeAll` gate of `happy-path-web`, `happy-path-wallet` and `happy-path-nft`.
- **FOUND:** the seat's file lists name `recruitment-data.ts` (a path constant) but not the helper; `recruitment-helpers` counts 0 in both census files, because it never contains the literal path. The READY's "three tests/e2e specs read data.services only" is therefore not the full e2e set.
- **Does it newly fault? READ ONLY, not executed:** no. It returns healthy on `data.status === 'healthy' || required.healthy === required.total`. It never compares to `operational` and the required counts do not move. So Wednesday's STOP condition is not triggered.
- **Newly silent:** nothing found. The rule only adds a route to `degraded`. Item 3 correctly removes three false `unreachable (optional)` warnings where portals serve.
- **My census:** `evidence/census_q2_system_status.txt`, `evidence/census_q2_operational.txt`. Controls: both greps hit the status page and ks1101. Also read: `frontend/status/index.html:585-586`, `frontend/admin/src/services/api.ts:198-209`, `services/originate/src/routes/adminConfig.ts:674,700` (comments only), three e2e specs (`data.services`), and `/status/simple`.
- **Outside the tree:** Extranet `api`, `app`, `tools`, `ci`: 0 hits (control: `fetch` in 15 `app` files). `observability/`: 0 (control: `health` in 10 files). WEDNESDAY tracked tooling: hits only in QA gatesets, launchers and briefs, no monitor. A monitor on a box or a third-party uptime check stays UNMEASURED.

### F-3 Low. PR 2032: "the summary counts do not move" holds for item 4, not for the PR
- **Where:** PR body "What does not change" and census row for `frontend/admin/src/services/api.ts`; the same wording in the flow fragment.
- **FOUND, MEASURED AT RUNTIME (stubbed fetch modelling frontends that accept only 8080, defaults in force):** `summary.services.healthy` 18 on base, 21 on head. The admin Services Online tile (`healthy + degraded`) follows, 18 to 21. Evidence: `evidence/counts_base.json`, `evidence/counts_head.json`.
- **Impact:** the movement is correct, and no reader faults. Whoever reads the deploy should expect the tile to move and not treat it as an anomaly. **Fix-shape:** one sentence in the body.

### F-4 Low. PR 2032: a red portal's headline and its only advice now disagree
- **Where:** `routes/system-status.ts`, `generateTroubleshooting`, the optional-service branch (unchanged by this PR).
- **FOUND, MEASURED AT RUNTIME:** with a portal refused, the unauthenticated body says `degraded`, and the only item says "The verifier-portal service is optional but recommended for full functionality", with `cd services/verifier-portal && npm run dev`. `services/` holds no directory with `portal` in its name. On base the same text sat under `operational`, so it was wrong but not contradictory. Evidence: `evidence/real_socket_head.json`.
- **Scope:** the ruling says the page stays untouched; it does not speak to this body text. Not a regression; a question for Wednesday whether it is filed. No fix asked of this PR by me.

### F-5 Low. PR 2032: port evidence outside the pinned set
- **Is 8080 right? READ ONLY, per portal, yes for all three:** `frontend/{issuer,verifier,admin}/nginx.conf:2` `listen 8080`; each Dockerfile `EXPOSE 8080` and `HEALTHCHECK` on 8080; `docker-compose.yml` healthchecks on 8080 (lines 1868, 1902, 1937 region); `nginx-demo.conf:475,488,557` and `nginx.conf:242,255,324` proxy to 8080. All on `secuura-network` with the gateway. `location /verify/` and `/admin/` serve `try_files` from a dist copied to those paths, so the health paths answer 200 by reading.
- **Loose ends, none blocking:** `port: 8882` still sits beside the new `:8080` url on all three portal entries in the public body (the status page does not render it; compose comments name the edge as 6882). `nginx-demo.conf:17-19` header comments still say `:80`. `nginx-production.conf:402,410,434` proxies to `:80`, but its own header calls it not the live edge, and it is untouched here. The PR's comment names EXPOSE and the compose healthcheck, but the cells tie only to `nginx.conf` and `nginx-demo.conf`.
- **Sibling probes:** none elsewhere in the services (`evidence/census_q2_sibling_ports.txt`).

### F-6 Low. PR 2036: the READY's wording is softer than the ruling
- **Ruling, as the seat quotes it:** "State plainly in the READY that it does not stop a remote context upload, unless your proof shows otherwise."
- **READY:** "Does the allow-list COPY stop a remote context upload? NOT shown ... UNMEASURED". The proof did not show otherwise, so the ruled sentence was owed.
- **READ ONLY, az not run:** `deployment/azure/deploy.sh:409` and `deploy-all.sh:189` run `az acr build` from the monorepo root, and `.dockerignore:11-12` re-includes `docs/openapi`. By reading, backups would still be in such an upload. **Action:** treat F2's context half as open, which the seat also says. Whether that path is still in use, I did not establish.

### F-7 Low. PR 2036: the scanner only sees COPY, and every cell is source text
- **MEASURED AT RUNTIME, `evidence/tampers_2036.out`:** adding `ADD docs/openapi/ ./docs/openapi/` beside the named COPY: 0 red of 18. Adding exec-form `COPY ["docs/openapi/", "./docs/openapi/"]`: 1 red, and that one is the count control, not the detector, so it is caught by accident.
- **Cells that prove only text:** all of ks1841b and all of ks1823's Dockerfile cells. ks1841 does run the real `find` line via `sh`, on macOS `find`. The ks864e item 1 cells are also text only. **Fix-shape:** match `ADD` too and parse exec form.

### F-8 Info. PR 2036: is the find on line 36 (the ruling's "line 35") still needed?
- **Answer:** dead for what it was written for, still live on one route. Wednesday ruled it stays, and it does no harm.
- **Emulated, not Docker: real `.dockerignore` (matcher with 6 controls) and the real RUN line from each Dockerfile. `evidence/emulate_copy_find.out`.** Head line: the spec alone after COPY, find removes nothing, rc 0. Add a host-local `services/api-gateway/docs/openapi/host-local.bak`: it enters through `COPY services/api-gateway/ .`, because `docs` in `.dockerignore` is anchored at the context root, and find removes it. That path is tracked nowhere and absent from the shared checkout. On that route the file still sits in the line 29 layer, so F2's class survives there if such a file ever exists.
- **Line 35's comment** ("the host directory can hold backups") now describes the line above's old behaviour.

## Questions

### Q1 Scope
PR 2032: 7 paths, PR 2036: 5 paths, each exactly as its READY states, one commit each. Overlap between the two: 0. Both merge orders rc 0, same tree `f967f2c0c982`. Planted same-line controls fire: helper line against 2032 rc 1, COPY line against 2036 rc 1. `evidence/q1_q5_scope_merge.txt`.

### Q2 Behaviour
- **PR 2032 requests, MEASURED AT RUNTIME:** every fetch URL captured from `/status` and `/status/simple` on base and head, for NODE_ENV development, production, staging × portal env unset, empty, set. 21 requests each. The only differences are the three portal URLs when env is unset or empty; none when set. `/status/simple` lists identical. Fetch options identical (`signal`). `evidence/fetchlist_*.json`. The seat's 17 of 18 count is right from the diff.
- **Item 2:** two lines deleted, docker lines kept, as ruled. Readers: F-2.
- **PR 2036 readers:** `index.ts:608-610` reads only `secuura-api.yaml`, and that is the only code reader in the image. `npm run build` is `tsc` with `src/**` only. On base the find already removed everything else before the build, so nothing after it can have depended on the rest. Compose's bind mount names the single file. `x-workflows-doc` is a generator string with no reader in the gateway. Host-side scripts read the host tree, not the image.
- **Other Dockerfiles:** of 37, only `api-gateway` and `mcp-server` mention openapi. `mcp-server` copies its own named `openapi.yaml`. No other whole-directory COPY of `docs/openapi`.

### Q3 Tests that can fail
Red on base: 2032 19 failed, 25 passed of 44, all AssertionError; 2036 4 failed, 14 passed of 18. Green on head: 66 of 66; 18 of 18. Tampers reproduced as the seat predicted: 2032 `|| true` 4, issuer `:80` 4, widened 2; 2036 whole-directory 4, allow-list deleted 3. Controls 0. My own: F-1, F-7. Assertion that each tamper landed is in `tools/tampers.py`.

### Q4 Suites (Node v26.8.1)
| Suite | 2032 | 2036 | both on develop 581fdc8a |
|---|---|---|---|
| api-gateway vitest | 159 files, 1676 passed | 158 files, 1659 passed | 161 files, 1693 passed |
| tsc (service config) | rc 0 | rc 0 | rc 0 |
| ratchet, tests included | 25 of 25 baseline, 0 new | same | same |
| eslint | 0 errors, 30 warnings, none in touched files | same | not run |
| check:openapi | generate --check rc 0, examples OK | same | same |
| docs-fragments | OK | OK | OK |

0 failures, nothing to classify. Controls: planted `debugger`/`var` flagged; planted spec drift fails generate --check rc 1; planted unclosed div fails docs-fragments on both. The two ADVISORY lines (6249, 6235) print the same on `3fbf50ede123`, so same-on-base. All match the seat's figures; I did not re-run the 1654-on-base figure, since there were no failures to compare.

check:openapi was run as its component commands, not `npm run`: see conduct.

### Q5 Merge tree onto develop per pins.txt (581fdc8a9c71)
- PR 2032: rc 0, tree `47ef4c7c8707`. Shared paths with the 73 moved since its base: 0.
- PR 2036: rc 0, tree `9c0dcc2909e1`. Shared paths with the 62 moved since its base: 0.
- Planted shared-path control: 1 each, as it should be.
- Develop moved during the gate to `3703f3f4d5fa` (read 13:42): 2032 rc 0 tree `238bc9b88124`, 2036 rc 0 tree `67e684ab618f`, 0 shared with the two new commits. It will move again. Heads re-read at 13:42, unchanged.

### Rulings
Commission's summary agrees with the quotes in the seat's bodies and test headers: tier 1; item 2 A; item 4 A with the census; F2 A. Diffs do what they say. **But see NOT tested: I compared against the seat's own quotes only.**

## NOT tested

- **PR bodies from the API, not read.** The project's `.gh-config` has an empty `hosts.yml` and anonymous GET answers 404. I read the seat's `drafts/pr_ks864_body.final.md` and `pr_ks1841_body.final.md` and cannot show they equal the live bodies. I did not look for another credential.
- **Wednesday's inbound rulings not read at source.** The seat's `mail/` folder holds outbound mail only, and the phrases are not in tracked WEDNESDAY files. Only the seat's quotes were available.
- **Decision cards:** `prior` returned 0 for KS-864 and KS-1841, but its control failed: it also returns 0 for KS-1585, a card `show` proves exists. So that zero says nothing.
- **Docker: NOT run.** load1 was 8 to 17 at every read, above the commission's 7, and a daemon was already up with 0 and later 10 containers running, so someone else holds it. So no real nginx answering the portal paths, and no alpine `COPY`/`find`: I relied on the seat's kept proof output for that, and did not re-run it. Full `docker build` of the api-gateway image: not run by anyone.
- **Node 24:** not used. **The four platform suites, a live stack, kintsugi, demo:** not run; preflight legs 3, 4, 8 skipped by the seat. Portals reading healthy on a real box remains inferred.
- **A box's `.env.local`.** The gateway loads it through `env_file`, and no tracked file sets `*_PORTAL_URL`. A stale value on a box would now hold the headline at `degraded` and no test can see it. UNMEASURED; read `/system/status` after the deploy.
- **Remote `az acr build` upload:** READ ONLY (F-6). **Monitors outside the tree:** UNMEASURED (F-2). e2e recruitment specs: read, not executed.
- ks864a, ks864c: run, not reviewed cell by cell.

## My own conduct

- **Correction, in the open: my first set of measurements used the wrong dependencies.** I copied gate 216's `node_modules`, which were symlinks into gate 204, and `cp -R` kept them as links. I also missed the gateway's own `node_modules` (`@types/node` 20.19.43). That produced 1 failed cell and 2 "new" ratchet errors in `ks815`, on base as well, which were my environment and not the PR. I replaced the links with real copies from gate 204, moved those outputs to `_quarantine_2026-11-06/evidence_symlinkdeps/`, and re-ran everything; every figure above is from the re-run. I wrote nothing into gate 204 or gate 216 that I could find: their `.vite` directory is dated 13:09, before I started.
- **A false zero of mine:** my first sibling-port grep used `\b` under `git grep -E` and returned 0. The `nginx-production.conf` hit it should have found exposed that. Re-run with `-P`.
- **check:openapi:** `npm run` failed in my trees because tsx's IPC socket path under this folder is too long for a unix socket, my environment and not the PR. I ran the same commands with tsx's own two loaders, keeping scratch in this folder. Service `node_modules` were copied in from gate 204 for the generator.
- Two hook refusals on `git -C "$VAR"`; I re-issued with the literal path to my own clone. All writes stayed in this folder: clone, worktrees, `tmp/`, `tools/`, `evidence/`. Planted and trial-merge commits exist only in my clone and were never pushed.
- Shared checkout: read only, HEAD unchanged, no 2032 or 2036 refs (its five old `refs/remotes/pr/*` date from September).
- Network: git fetch and ls-remote into my clone, and the two failed API reads above. No box, no Linear or GitHub post, no credential printed, no file deleted. Replaced items went by `mv` to `_quarantine_2026-11-06/`. Test fixtures remove their own temp dirs. No process of mine left running; Docker neither started nor stopped.
