GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 176 (Tier 1, round 1): PR 1992 / KS-1868 "PR 14": shared SSRF, secrets and indexer catches read an unreadable thrown value safely

## Subject (pinned at start AND end; nothing moved)

| ref | start, 12:23:00Z | end, 12:38:53Z |
|---|---|---|
| refs/heads/develop | `1cbf260548e7fd534603725f9fc6b05c5cdd9907` | `1cbf260548e7fd534603725f9fc6b05c5cdd9907` |
| refs/pull/1992/head | `651f25b0d0e23f53eadede35e38c21fa2c31a599` | `651f25b0d0e23f53eadede35e38c21fa2c31a599` |

Both read with `git -C <checkout> ls-remote origin …`. These are equal to Seat R 80th's pins. The PR is one commit on `1cbf2605` (merge-base = develop): 9 files, +384/-4, matching the READY mail. The product files are 3: ssrf-guard.ts, secrets-manager.ts and event-indexer.ts. Head blobs: `edb91bb87f69`, `c081a06040c7`, `3f067b59dfb9`. Base blobs: `78179f4878ad`, `53f532732398`, `44204cd0e383`.

**Merge-tree (Q8), run in my clone:**
- `merge-tree --write-tree develop 1992`: rc 0, tree `ebefea7358a7`. That equals the PR's own head tree.
- Shared paths with tonight's two PRs: **0** with 1990 (`5550a714`) and **0** with 1991 (`a44e59c5`). The control (1992 against itself) gives 9. The only shared things are directories (`packages/shared/src/__tests__`, `Projects Documents/fragments/{cheat,flow}`), and the file names in them all differ.
- Group merge develop + 1990 + 1991 + 1992: rc 0/0/0, tree **`70bbceb1bf16`**. The other order (1992, 1990, 1991) gives rc 0/0/0 and the same tree `70bbceb1bf16`.
- **The seat's "group tree `0a2814d535d7`" was NOT reproduced.** That object exists neither in the checkout nor in my clone. Origin has no PR head above 1992. I do not know which set the seat merged (see G176-F5).
- Planted control: a develop-side commit editing the same line of `ssrf-guard.ts` merged against 1992 gives rc 1, `CONFLICT (content)` in `ssrf-guard.ts`. So the instrument does detect conflicts.

**Host:**
- macOS Darwin 27, Node **v26.8.1** (not the LTS 24 line), TypeScript 5.9.3 (packages/shared's own install).
- Vitest **4.1.12** with vite 7.3.7 and esbuild 0.28.1, equal to develop's root lock (read from blob `30777ce9`).
- Load averages 15-19 throughout. No cell of mine timed out, so nothing needed a solo re-run.
- I did NOT run on Node 24, in a container, with a real DNS lookup, a real socket, a real Vault, Blockfrost, Postgres or Prisma, or a booted service.

**Install.** Gate 175's install, used only after a hash check:
- The `packages/shared/package-lock.json` blob is `c100fb8e` at develop, at 1992 and in gate 175's checked-out file (hash-object). The root lock is `30777ce9` at both refs.
- I then APFS-clone-copied (`cp -Rc`) gate 175's `packages/shared/node_modules` and `scratch/vt` into MY workdir, so nothing of mine resolves into gate 175's folder. `find -type l | readlink` gives 0 links into gate175.
- Disk: 24 GiB free at start and at end (floor 18).

**Method.**
- `scripts/swap.sh base|head` writes develop's blobs or the PR head's blobs for the 3 product files and prints the blob hashes on every swap. Tests stay at head.
- `harness/` recorders drive the REAL modules with the same **17 value classes** gate 175 used (`harness/values.ts`, sentinel `SNTL176`):
  - `ssrf.test.ts`: the stand-in `dns/promises.lookup` and stand-in `http`/`https.request` (a counter that then throws; no socket ever opens).
  - `secrets_indexer.test.ts`: the real VaultClient with the global `fetch` rejecting; the real package logger; a Blockfrost API object, with `@blockfrost/blockfrost-js` aliased to a stub for `start()`.
  - `dispatch.test.ts`: the REAL `services/originate/src/routes/webhooks.ts` `dispatchEvent` → `deliverWebhook` → real `safeOutboundRequest`. It uses the real originate winston logger and stand-ins for the db client, `../db`, `../middleware/auth`, DNS and request. Originate's bare imports are aliased to packages/shared's install.
- Output was captured at `console.*`, `console._stdout/_stderr` and `process.std*.write`.
- The class bar is computed by `scripts/classbar.py` and `scripts/q2bar.py`. The reference is BASE's outcome for the ordinary Error, per site.
- Raw rows: `results/q_{base,head}.jsonl` (408 cells per tree) and `results/q2_{base,head}.jsonl` (34 per tree). Side by side: `results/table.md` and `results/q2_table.txt`.

## Findings

### G176-F1 — LOW (note for Wednesday's ruling): originate's webhook dispatch now goes on to the OTHER subscribers where base aborted the whole loop, which is exactly base-ordinary
- **FOUND:**
  - **Base.** The real `dispatchEvent` gets 3 subscriptions, and wh1 receives the hostile value at DNS or at request construction. For 5 classes (message getter throws, revoked Proxy, null, undefined, throwing get trap) × 2 trigger points = **10 cells**, base aborted the loop at wh1:
    - `safeOutboundRequest` rejected, and the outer catch returned 0;
    - there were no delivery rows;
    - wh2 and wh3 were never attempted.
  - **Head.** In those 10 cells head logs wh1 as a failed delivery (`success=false`), delivers wh2 and wh3 to the stand-in, and returns 2. That is the base-ordinary outcome in 10/10 cells.
  - **wh1 itself is never sent at either tree:** 0 of 34 cells per tree.
  - Head's extra sends go only to subscribers that base-ordinary also sends to. Cells where head sends beyond base-ordinary: **0 of 32**.
  - I did not write HOLD-FOR-KAM:
    - the class bar is 0;
    - the sends go to partner endpoints that already passed the guard;
    - this is the intended effect.
  - If Wednesday rules partner webhook delivery a "message to a human" signature class, the condition and the evidence are here.
- **TESTED:** 17 classes × {wh1 DNS throws, wh1 request throws} per tree. Not tested: real Prisma (a non-string `error` bound into `$executeRaw`), real sockets, the m365 Teams loop (read only, see Q2).
- **HOW:** `harness/dispatch.test.ts` via `scripts/run_q2.sh base|head`, scored by `scripts/q2bar.py`. Positive control: the ordinary Error gives `returned 2`, with rows `1:false, 2:true, 3:true` at both trees.

### G176-F2 — LOW, PRE-EXISTING (base = head): three value classes still make the DNS-path guard REJECT instead of returning its refusal
- **FOUND:**
  - **Where it happens.** For `{message: Symbol}`, `{message: revoked Proxy}` and `{message: object whose toString throws}`, `reason = err.message` succeeds. The template literal `` `could not be resolved (${reason})` `` then throws, and it sits outside the new guard.
  - **Affected functions.** `resolvePublicAddresses`, `assertResolvedHostPublic`, `assertSafeOutboundUrl` and `safeOutboundRequest` all REJECT: 3 × 4 = **12 cells**, base = head.
  - **Effect.** Every one of them is LESS permissive than base-ordinary: nothing is allowed and 0 requests are constructed.
  - **Downstream, in the real dispatchEvent:**
    - The same 3 classes at DNS abort the dispatch loop (return 0, wh2 and wh3 never sent) at both trees: 3 cells.
    - `{message: BigInt}` and `{message: revoked Proxy}` at request construction do the same: 2 cells. There the request catch returns a non-string `error`, and deliverWebhook's `logger.warn` meta (read, not traced) and the outer catch end the loop.
  - **Related, also pre-existing:** the request catch returns a non-string `error` (symbol, bigint or object) for 4 classes at both trees.
  - This is the gate 175 F2 shape (the template literal sits outside the guard).
- **TESTED:** recorder cells at both trees. **HOW:** `results/classbar_Q1.txt` (12 lines) and `results/classbar_Q2.txt` (5 lines).

### G176-F3 — LOW, PRE-EXISTING (base = head): EventIndexer's `isRateLimited` reads the value BEFORE `handleError`, so the PR's guard is not reached for 3 classes, and the indexer re-reads the same block forever
- **FOUND:**
  - **Where it happens.** At catch sites 210, 223/232 and 326/329, `isRateLimited(err)` reads `err?.status_code` and `err.message` unguarded. For the message getter throws, the revoked Proxy and the throwing get trap, that read throws first.
  - **Site 210:** `poll()` REJECTS on every poll at both trees: 6 cells (onError on and off). The production caller is `setInterval(() => void this.poll())`, so this would be an unhandled rejection. That is read, not driven.
  - **Sites 232 and 329:** the throw reaches poll's catch as a new, readable Error, so `lastProcessedBlock` is NOT advanced. Block 11 is re-fetched on every poll: 3 of 3 polls, 12 cells at both trees. With a persistent bad value, that is a retry forever.
  - **The default path.** `handleError`'s `console.error(error.message)` still throws for the getter class (it is an `instanceof Error`, so it passes through the guard unconverted). That is 2 more cells (sites 133 and 321, onError off).
  - Total: **20 cells where head ≠ base-ordinary, all base = head.**
- **TESTED:** the real indexer over 3 polls with a stand-in API. Not tested: the real `setInterval` path, real Blockfrost.
- **HOW:** `results/classbar_Q4.txt`.

### G176-F4 — LOW: for 2 classes the indexer now SKIPS a block where base retried it (equal to base-ordinary, which already skips)
- **FOUND:**
  - For `Object.create(null)` and `{message readable, toString throws}`, base's handleError threw. That throw escaped processBlock or processTransaction, so the block was not advanced, and base re-read block 11 on all 3 polls.
  - Head handles the error, marks block 11 processed after the first poll, and does not come back to it:
    - **at site 232:** the whole block is skipped;
    - **at site 329:** only the failing tx1 is skipped, and tx2 is delivered.
  - Count: 2 classes × 2 sites × 2 (onError on and off) = **8 cells**.
  - Base-ordinary does exactly this: an ordinary `blocksByNumber` failure skips the block (`lastBlock 10→11`, no retry). So head swallows what base propagated, in a way that skips a block. That is the class bar's reference, not an excess, and the skip-on-error design is pre-existing.
  - At site 321 (onTransaction throws), head now fires the callback for both policies (4 deliveries) where base stopped after the first (2), equal to base-ordinary.
  - No head cell retries forever where base did not: **0**.
- **HOW:** Q4 recorder, `results/table.md` (columns `block11Advanced`, `blocksByNumberCalls`, `delivered`).

### G176-F5 — LOW (disclosure): the seat's group tree `0a2814d535d7` does not reproduce
- **FOUND:** my develop+1990+1991+1992 tree is `70bbceb1bf16` in both orders. The object `0a2814d535d7` is in neither the checkout nor my clone. The READY mail does not carry the group tree (only the commission does), so I could not see how the seat formed it.
- **HOW:** `scripts/mergetree.sh`, `results/mergetree.txt`.

## What passed (measured)

**Q1 (the SSRF guard; decides the weight).** 17 classes × 6 cells per tree = 102 cells: the DNS lookup throws for each of the 4 functions, and the request throws for both the hostname and the IP-literal URL.
- **The class bar: head cells that are ALLOWED (null or `ok:true`) or SENT where base-ordinary refused or sent nothing: 0.**
- ALLOWED cells at head across all 102: 0. At base: 0.
- Requests constructed in the DNS-throws cells: 0 at both trees. The 34 request-throws cells construct and throw by design (a stand-in), and none sends.
- Of 96 non-ordinary cells, 84 equal base-ordinary. 30 changed base→head, every one TO base-ordinary (a REJECT became a `blocked` or `request_failed` refusal carrying the constant `unreadable thrown value`). The 12 that do not reach base-ordinary are G176-F2: base = head, all rejections.
- **Hostile addresses with ordinary errors:** 68 cells per tree, **68/68 identical base = head**:
  - 19 DNS answers: private, loopback, IMDS, link-local, unique-local, four v4-mapped forms, 0.0.0.0, three mixes (public-first, private-first, public + mapped IMDS), and empty;
  - 10 literal URLs;
  - an ordinary ENOTFOUND.
  - Every hostile one is refused (`blocked`), with 0 requests constructed.
  - The only ALLOWED or constructed cells are the 2 public controls and the public literal (4 allowed, 3 constructed, at both trees). Those are the instrument's positive arm.
- So the guard's own refusals are unchanged by this PR.

**Q2 (callers).**
- **Census.** My own `git grep -w` at the head tree finds exactly the seat's **4 non-test call sites**: m365 `index.ts:1286` and `:1495`, originate `webhooks.ts:172` and `:459`. The other hits are the barrel `index.ts` and intra-module calls; I filtered out tests, md, html, py and comments.
  - Positive control: the same grep finds the 4 barrel exports and the 4 definitions.
  - Negative control: a nonexistent name gives 0, rc 1.
  - No `require('@secuura/shared').safeOutboundRequest` form exists, and no path import of `ssrf-guard` outside tests and the barrel.
- **originate dispatchEvent, driven:** 34 cells per tree. Head = base-ordinary in 27 of 32; the other 5 are G176-F2, base = head. See G176-F1 for the 10 changed cells.
- **originate 172, read:** the guard result becomes a 400 `webhook url rejected: …`. At base the hostile classes rejected into the route catch.
- **m365 1286, read:** base rejected into `next(error)`; head answers a 400 whose message is the constant. Neither tree registers the URL.
- **m365 1495, read:** base's rejection lands in the loop's own `catch { failed.push }`; head's `request_failed` goes to `log` + `failed.push`. The same row outcome, and the loop continues at both trees.
- So head changes no caller's handling of a refused result except dispatchEvent's (F1), and that change goes toward base-ordinary.

**Q3 (security `SecretsManager.getSecret`, real VaultClient, fetch rejects):** 17 classes × {getSecret, getSecretOrThrow} × useEnvironment {on, off} = 68 cells per tree.
- Head = base-ordinary in **64/64** non-ordinary cells; 17 changed.
- With useEnvironment **on**, head returns the environment value (and caches it) for 5 classes where base REJECTED: the getter, the revoked Proxy, `Object.create(null)`, the get trap, the throwing toString. That is the ordinary-Error outcome.
- With useEnvironment **off**, head never returns a secret: 0/34. getSecret returns `null`; getSecretOrThrow throws `Required secret not found`.
- **Cells where head returns a secret that base-ordinary would not: 0.**
- **"No non-test importer": confirmed.**
  - `@secuura/shared/security/secrets-manager`, `initializeSecretsManager`, this file's `getSecretsManager`, `useEnvironment` and `new SecretsManager(`: 0 non-test users outside the file itself.
  - The barrel does not export it; `security/index.ts` does not either.
  - jwt.ts uses `vault/key-vault`'s `getSecretsManager`.
  - Positive control: the same subpath-import grep finds `@secuura/shared/security/scopes` importers in api-gateway, auth and originate.

**Q4 (EventIndexer.handleError):** 5 sites × onError {on, off} × 17 classes = 170 cells per tree, with 3 polls per poll-site.
- Head = base-ordinary in 140/160 non-ordinary cells; 28 changed, all TO base-ordinary.
- The 20 others are G176-F3, base = head.
- At site 133, base `start()` rejected for 4 classes; head resolves and calls onError once, as base-ordinary does.
- Unhandled rejections counted: 0 at both trees (`poll()` awaited directly).

**Q5 (sentinel `SNTL176`; KS-1346/1348):**
- Log lines carrying it, across Q1/Q3/Q4: base 72, head 70. Answers carrying it (a returned error string, or the Error handed to onError): base 75, head 73.
- originate dispatch: log lines base 13, head 9.
- **Cells where head prints or answers MORE: 0 of 442.** Head prints less in 2 + 4 cells: base logged the get trap's own text.
- Positive control: the ordinary Error prints the sentinel in the Vault warning, the indexer's console.error and originate's delivery-failed line, and answers it in the SSRF refusal string, at both trees.
- **Pre-existing (base = head), not this PR:**
  - the ordinary-Error DNS reason is carried into the refusal string;
  - m365 and originate answer that string to the client in a 400;
  - so an ordinary lookup error's text does reach a response body.

**Q6 (red first, suites, mutants).**
- **The PR's 16 cells:** at base 8 fail, **all 8 by AssertionError**, and 8 pass (the C1/C2 controls, by design). At head 16/16 pass.
- **Whole `packages/shared` suite** (its own `vitest.config.ts`, in a sparse clone without the workspace-root install):
  - Base: 63 files, 640 tests, 633 passed, 7 failed.
  - Head: 67 files, 656 tests, 649 passed, 7 failed.
  - Ratio 633/640 → 649/656. **The failure set is identical: 18 items**, namely 11 files that fail to load (repo-walk guards, no Dev root in a sparse clone), plus entrypoint-corpus ×4, ks843, threadToken "different policy IDs", and the CIP-8 wallet signature (KS-1727).
  - The seat's 1447 → 1463 is a full-checkout count. My delta (+4 files, +16 tests) is the same.
- **Mutants** (raw table `results/mutants.tsv`, my count of the rows): **17 mutants. 16 KILLED by the PR's own tests, 1 SURVIVED them.**
  - The survivor is `ssrf-guard.ts` G6, which drops the `return;` after `done(...)` in the request catch.
  - It is not equivalent: execution would fall through to `req.on` on an undefined `req`, and later to a deadline timer calling `req.destroy()` on it.
  - The existing ssrf test files (the KS-931 cells) KILL it. So it is killed by either set: 17/17.
  - The other ssrf tests alone leave the 6 guard-specific mutants alive (G1-G3). Only the PR's cells pin the guard.
  - Kinds: inner catch rethrows (4), constant changed (4), use-line reverts to the raw read (4), plus G4 DNS catch fails OPEN, `ok:true` (KILLED by both sets), request catch tagged `blocked`, the `return` dropped, getSecret returns null without the env fallback, and handleError swallows without onError.
  - Control: the unmutated head passed each module's test set (rc 0) before mutating.

**Q7 (tsc with tests):**
- `tsc --noEmit` over `src/**/*.ts` including `__tests__` (a workdir tsconfig extending the package's): **base 24 errors, head 25.**
- The diff is exactly 1 line: TS1378 (top-level await) at `ks1868-ssrf-guard-safe-outbound-request-catch-unreadable-throw.test.ts:22`.
- Base already has 5 TS1378 errors in 4 files (ks1179, ks727, ks914-shipped, ks932 ×2), which confirms the seat's correction.
- **It matters for no runner the repo uses:**
  - the package's `build` (`tsc`) excludes `src/__tests__`;
  - vitest runs the file green;
  - the test-types ratchet (`check:test-types`, preflight leg 16) covers services/auth, api-gateway, vc-issuer, security and m365-integration, not packages/shared.

**Q8:** see Subject. rc 0, tree = the head tree, 0 shared paths with 1990 or 1991, group tree `70bbceb1bf16` in both orders, and the planted control conflicts.

## NOT tested
- No real DNS, socket, TLS, Vault, Blockfrost, Postgres or Prisma. `$executeRaw` receiving a non-string `error` (F2 classes) was not run against Prisma.
- m365 `index.ts` was READ, not driven (1286, 1495).
- The indexer's `setInterval` path, where an unhandled rejection would occur, was read, not driven.
- No Node 24 / LTS; host Node is v26.8.1.
- Not run: eslint, the test-types ratchet, the four platform suites, the pre-push hook.
- My suite is a sparse-clone count, not the seat's full-checkout 1447/1463.
- Reachability: the call-site census is `git grep` only. Whether either service is deployed with these paths live was not measured. Deployed images may vendor `@secuura/shared` some other way I did not see.
- Remaining unguarded reads in ssrf-guard that the PR did not touch (`req.on('error')` at 629 reading `err.message`, the write/end catch at 638), and originate `webhooks.ts:553`'s `err.message`: I did not drive them with hostile values. The seat already names 553.
- The 2 `Projects Documents/fragments/*.html` files were not assessed.

## Plain answer for Kam
This change stops three shared error handlers from crashing when they meet a strange kind of error. Now they behave exactly as they already did for a normal error. The web-address safety check never lets anything through that it blocked before: every private, internal or cloud-metadata address is still refused, and a lookup failure is still a refusal. One visible effect: if one partner's webhook address hits one of these strange errors, the other partners' webhooks are now still delivered instead of the whole batch stopping. That is what already happens with a normal error. A few rarer error shapes still crash the same way they did before, and the blockchain indexer can still get stuck re-reading one block. Neither is new, and both are worth a later KS-1868 ticket; neither blocks this merge.

---
Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992/`.
- Tracked: `verdict.md`, `harness/`, `scripts/`, `results/`, `runs/`.
- Ignored (`.gitignore`): `repo/` (my `--shared` clone; it also holds my harness copy in `packages/shared/src/__gate176__/` and two `vitest.gate176*.config.ts`), `mut/` (a base worktree of my clone), `scratch/`, `home/`, `tmp/`, `node_modules`.

Background processes: 3 started (base suite pid 54159, head suite pid 54163, mutant run pid 14530). All exited on their own, and `ps` shows none at the end. I wrote nothing outside the workdir. The checkout was used with read verbs only (`ls-remote`, `config --get`, `remote get-url`, `cat-file -t`, `status --short`), plus `git clone --shared` from it. Fetches went into my clone only.
