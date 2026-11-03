GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 178 (Tier 1, round 1): PR 1994 / KS-1868 PR 16, eight nft-certificate route catches read an unreadable thrown value safely

## Subject
- Repo Secuura/Distributed_Secuura. Read from the checkout's origin with `git -C <checkout> ls-remote origin`.
- **Start (2026-11-03 16:29:01Z):** PR 1994 head `74dc459edbb6cdef368f0bc74a54b081cc4b3835`. develop `ea5134d6b98c470615c59fca5d3ec30356adfbd7`. PR 1993 head `8712cb115e0ac48f401865a8549a8847cf39a28c`.
- **End (2026-11-03 16:44:41Z):** PR 1994 head `74dc459edbb6cdef368f0bc74a54b081cc4b3835` (**unchanged**). develop **moved** to `ee1e1b83211504f96ebccba325d1ef7139bc83cc`. That commit is PR 1993's squash (parent `ea5134d6b`). Its tree is identical to my simulated develop+1993 tree `ce7a5d0d1a99` (0 paths differ). 1994 merged onto it gives tree `d5816ee2f624`, which is the tree I suite-tested and drove (see Q7).
- Head is ONE commit. Its parent, measured, is `79145a312f0150ca9adaf5a36bb3dea93d108cff`. It changes 11 files, +957/-8: 56/8 in `services/nft-certificate/src/routes/nft.routes.ts`, 8 new test files of 106-108 lines, and 2 fragment HTML files (20 and 29 lines). 79145a is an ancestor of develop. Between 79145a and develop, 0 lines change under `services/nft-certificate` (repo-wide control: 9 files, and 19 at the end develop).
- Host: macOS Darwin 27, Node v26.8.1 (not an LTS line). Express **4.22.3**, both installed and in the lock blob (`85ab2efb`, the same at base, head and develop). Vitest 4.1.12, TypeScript 5.9.3, ESLint 10.7.0, typescript-eslint 8.64.0 (versions from the root lock `30777ce9`).
- NOT run on: Node 24 LTS, a container, the booted `server.ts` (no Postgres, Blockfrost, IPFS or Cardano), the api-gateway in front of the service, or the four platform suites.

**Install.** `git clone --shared --no-checkout` of the checkout into `repo/`, with a sparse checkout of `Blockchain/Dev/services/nft-certificate`, `packages/shared` and the root config. PR refs were fetched into MY clone only, through a second remote at the checkout's origin URL. In the clone:
- `npm ci --ignore-scripts` for the service, against its own lock `85ab2efb`.
- `packages/shared/node_modules` was APFS-copied (`cp -Rc`) from gate 176, after a hash check: the lock blob is `c100fb8e` at base, at head, at develop and in gate 176's file. 0 symlinks point into another gate.
- `node_modules/@secuura/shared` is a symlink to `../../packages/shared`, with shared `tsc`-built at the tree under test.
- ESLint is installed at the root-lock versions into `scratch/eslint` and linked.
- Nothing was written to the checkout (read verbs only). Its 18 untracked entries (`--full`, `systemTest/akto/...`) were not written by me.

**Method.**
- The eight handlers were driven through the REAL compiled app (`tsc` of the service at base and at head into `dist_gate_<tree>/`). That means `app.ts` in full: helmet, cors, boundedJson, rejectControlBytes, the shared RS256 `authenticate` with its publicOps, the router, the 404 handler and the shared errorHandler. Each cell went over a real listening socket with `fetch`, a 2.5 s reply bound and a 10 s solo re-run.
- Each handler's real singleton dependency method was replaced by one that throws or rejects the cell's value: `getNFTCertificate`, `getUserNFTCertificates`, `getQuickEstimate` (sync), `estimateCost` (sync), `verifyTransaction`, `verifyAsset`, `ipfs.pin` and `ipfs.unpin`.
- The authenticated routes carry a real RS256 token, signed by a key pair generated in memory (only the public half goes into `JWT_PUBLIC_KEY`; nothing is written).
- The real winston logger runs, and every output channel is captured.
- Per cell I recorded: status, body, header names, whether a reply arrived, the logged meta's `error` TYPE (never its value), sentinel counts, unhandled rejections and `/health` afterwards.
- 17 value classes x 8 handlers x 2 trees = 272 cells, plus 40 solo re-runs. Harness: `harness/classbar.cjs`. Results: `runs/classbar_{base,head,T2}.json`.

## Findings

### G178-F1 — INFO, PRE-EXISTING (base = head): seven other catches in nft.routes.ts keep the unguarded read
- **FOUND:** At head, these catches still read `error instanceof Error ? error.message : String(error)` inside the `logger.error` argument:
  - mint (catch 117, log 118)
  - record (176/177)
  - privacy-options (365/366)
  - supported-chains (411/412)
  - ipfs/upload (557/558)
  - metadata/estimate-size (740/741)
  - admin/platform-fee (786/787)

  By the same mechanism as the eight fixed sites, an unreadable value there would still leave the request open. The PR does not touch them, and the seat listed them as not covered.
- **TESTED:** Read only, at head. Not driven.
- **HOW:** Line numbers come from `git show 74dc459edbb6:…/nft.routes.ts` plus a grep of `router.`, `catch (` and `logger.error`. The three-dot diff's 8 hunks start at base lines 214/259/290/318/423/459/547/572, and none of them overlaps these lines.

### G178-F2 — INFO: at base, one unreadable value on a PUBLIC route killed the whole service process; at head it answers 500 and the process lives
- **FOUND:** I ran the compiled base app with NO `unhandledRejection` listener. `server.ts` installs none (grep 0, with a control of 2 `process.env` hits in the same file). One tokenless `POST /api/nft/verify/asset`, whose dependency rejected with a revoked Proxy, made the process exit **rc=1** with a `TypeError` and no reply.
  - Base with an ordinary Error: rc 0, a 500 reply, alive.
  - Head with either value: rc 0, a 500 reply, alive.

  This is the fix's real-world weight: a remote, unauthenticated request could take down the service if the verifier ever throws such a value.
- **TESTED:** 4 runs: {base, head} x {ordinary, revoked Proxy}, on the compiled `app.ts`, not `server.ts`. NOT measured: whether the real `blockchainVerifier` / Blockfrost client can actually throw an unreadable value, and whether the deployed process manager restarts the service.
- **HOW:** `harness/crash.cjs` and `runs/crash_*.log`.

### G178-F3 — INFO: the PR's 32 cells call the handler off the router stack with a fake `res`, not over HTTP
- **FOUND:** That is not a defect, and my HTTP cells agree with them cell for cell. A reader should still know that the PR's own tests never pass through the middleware or the auth gate.
- **TESTED / HOW:** I read the 8 test files (`router.stack.find(...)`, a plain `res` object) and compared them with my Q1/Q2 HTTP results.

## What passed (measured)

**Q1 Class bar.**
- Base-ordinary (V01) gives the same status and body at base and at head for all 8 handlers: 8 of 8. Each is a 500 with a constant envelope, for example `{"success":false,"error":{"code":"INTERNAL_ERROR","message":"Failed to verify asset"}}`.
- **Head: 136 of 136 cells equal base-ordinary** in status, body and header names (136/136), and each cell gives 1 log line whose `error` field is a string. 0 cells are more permissive than base-ordinary: 0 are 2xx, 0 are success-shaped and 0 carry extra fields.
- Base: 96 cells equal base-ordinary. 40 got **no reply**. Those 40 are V02, V03, V08, V13 and V16, each on all 8 handlers, and every one of them raised exactly 1 `unhandledRejection` and logged 0 lines.
- All 40 re-run alone with a 10 s bound: 40 of 40 still no reply, with the same rejection. So this is not a load artefact. Under load1 of about 11-14, 0 cells at head timed out.
- Base to head: 40 cells changed, every one from NO REPLY to base-ordinary. 0 other changes.
- Process health afterwards (`/health`): 200 in 136/136 cells at base (with the harness's listener present) and 136/136 at head.

**Q2 Public routes.**
- At head, `app.ts:48` reads `publicOps: ['POST /nft/verify/asset', 'POST /nft/verify/transaction']`. `app.ts` has 0 hunks in the PR.
- Through the full app with no token:
  - Both verify routes reach the handler (500, logged).
  - The 6 others stop at auth with 401 `{"success":false,"error":{"code":"UNAUTHORIZED","message":"No token provided"}}` and 0 handler logs.
- Base equals head on 8 of 8 (status, and whether the handler was reached). Also equal on the merged tree `d5816ee2`. So no change alters who can reach any handler.

**Q3 Neighbours.**
- `git diff -U0 79145a312f01...74dc459edbb6 -- nft.routes.ts` counts 8 hunks (-U3: 8).
- Controls: the untouched `app.ts` gives 0 hunks, and a new test file gives 1.
- The seven neighbours are untouched, at the head lines listed in G178-F1. The two `ipfs/:cid` catches (645, 670; they hand over with `next(error)`) are untouched as well.

**Q4 Sentinel `SNTL178`.**
- Response bodies: 0 at base and 0 at head (over 136 cells each).
- Log lines with the sentinel: base 32 cells, head 32 cells, and they are the same cells. Those are V01, V06, V14 and V15 (readable messages) on each handler, and those hits are themselves the positive control.
- Cells where head prints more sentinel than base: **0**. V02's sentinel sits inside the getter's throw: 0 at both trees (base sent no reply; head logs the constant).

**Q5 Red-first and suites.**
- The PR's 8 files at base routes: 32 cells, 16 fail and 16 pass. All 16 failures are R1 or R2 and fail by `AssertionError: expected true to be false` on `out.rejected`, which means the handler rejected. The C1/C2 controls pass. My HTTP cells confirm the cause independently: no reply, plus `unhandledRejection`, at base for V02 and V03.
- At head: 32 of 32 pass.
- Whole service suite: base 30 files / 209 tests (all pass). Head 38 / 241 (all pass). Merged tree `d5816ee2` (develop+1993+1994, shared rebuilt) 38 / 241 (all pass).
- **Mutants: 56 = 8 sites x 7 kinds, plus 1 unmutated control (32/32 pass). Raw table `runs/mutants.json`: 56 KILLED, 0 SURVIVED.** The table count equals the headline. The seven kinds:
  - raw read (guard removed)
  - constant changed
  - inner catch rethrows
  - Error branch dropped
  - logger.error dropped
  - status 500 changed to 200
  - reply dropped

**Q6 tsc and eslint.**
- `tsc` with tests (`tsconfig.gate178.json`: the service tsconfig with `src/__tests__` included, noEmit, which lists the 8 new files): rc 0, 0 errors. Planted control: rc 2, 1 error.
- ESLint (root `eslint.config.mjs`, `--max-warnings=0`) on the 9 changed .ts files: rc 0, 0 errors, 0 warnings. Planted control: 1 error (`no-var`) and 1 warning (`no-unused-vars`).

**Q7 Merge-tree.**
- Onto `ea5134d6`: rc 0, tree `aea99dbbad2f`.
- Onto develop+1993 (`8712cb11` merged): rc 0, tree `d5816ee2f624`. This equals the merge onto the end develop `ee1e1b83`: rc 0, the same tree.
- In both trees, 11 of 11 PR paths equal head's blobs, and 11 paths change in total.
- Paths shared with 1993's 10 files: 0. Planted control: 1.
- Callers, by `git grep -F` at head over `Blockchain/`, excluding tests:
  - Negative control `nft/zzgate178nonexistent`: 0. Positive control `nft/mint`: 5.
  - The only code callers of the 8 endpoints are the api-gateway description map (`services/api-gateway/src/index.ts:834`) and the e2e fixture (`tests/e2e/tests/recruitment/fixtures/recruitment-data.ts:333-334`).
  - Every other hit is OpenAPI, docs or comments.

**Q8 Express.**
- Installed version 4.22.3, the same as the lock blob.
- Control app on the same `express` module:
  - An async handler that rejects: NO reply within 3 s, plus 1 `unhandledRejection`.
  - A sync throw: 500 via the error handler.
  - An async handler that calls `next(err)`: 500.

  The seat's claim is confirmed: Express 4 does not catch a rejected async handler.

## NOT tested
- The booted `server.ts`, a real Postgres, Blockfrost, IPFS or Cardano provider, and the api-gateway proxy in front of the service.
- Whether any real dependency can throw one of the hostile classes. Every hostile value was injected by stub.
- A process manager's restart behaviour after the base crash (G178-F2).
- Node 24 LTS, and a container image.
- The other KS-1868 sites, and the seven unchanged catches of this file (read only, G178-F1).
- The four platform suites (Schemathesis, Akto, Playwright, k6), the pre-push hook, the test-types ratchet, and the docs-fragments check. The 2 fragment HTML files were not reviewed for content.
- Frontend or SDK callers that build these paths dynamically, without the literal `nft/<path>` string.

## Plain answer for Kam
Eight NFT-certificate endpoints used to hang, never answering, when a background service failed in an unusual way. On two public verify endpoints, which need no login, that same failure could crash the whole NFT service process. After this change, all eight give the same "internal error" reply they already gave for a normal failure, and the service keeps running. Nothing new is exposed: the replies carry no extra detail, no secret text from the error reaches users or the logs, and who may call each endpoint is unchanged. Seven other endpoints in the same file still have the old weakness. They are untouched here and are worth a follow-up ticket.

## Files
- Tracked in this folder: `verdict.md`, `harness/classbar.cjs`, `harness/crash.cjs`, `scripts/{swap.sh,mergetree.sh,mutate.py}`, and `runs/*`.
- Ignored by `.gitignore`: `repo/` (my clone, including `dist_gate_*`, `tsconfig.gate178.json` and a staged copy of shared files from the T2 check), `scratch/`, `home/`, `tmp/`.
- Background processes I started have all exited: harness pid 16329, mutants pid 83064, and monitor `bpslsail1`. None is left running.
