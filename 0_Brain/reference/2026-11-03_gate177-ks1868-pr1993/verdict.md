GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 177 (Tier 1, round 1): PR 1993 / KS-1868 "PR 15": the credential verifier, IdentusClient, ServiceClient and gateway-health catches read an unreadable thrown value safely

## Subject (pinned at start AND end; nothing moved)

| ref | start, 12:58:42Z | end, 13:15:43Z |
|---|---|---|
| refs/heads/develop | `1cbf260548e7fd534603725f9fc6b05c5cdd9907` | `1cbf260548e7fd534603725f9fc6b05c5cdd9907` |
| refs/pull/1993/head | `8712cb115e0ac48f401865a8549a8847cf39a28c` | `8712cb115e0ac48f401865a8549a8847cf39a28c` |

- Both read with `git -C <checkout> ls-remote origin …`. They equal Seat R 80th's pins. The checkout did NOT hold the 1993 (or 1992) objects; I fetched them into my clone only, using the checkout's `core.sshCommand`.
- The PR is one commit on `1cbf2605` (merge-base = develop): 10 files, +378/-4, matching the READY mail. Product files 4. Head blobs: verifier `4deb5acdaded`, identus-client `dd2ab78dadb7`, service-client `f1f1a833f0cb`, health-dashboard `1b6df6244f09`. Base blobs: `c4580aec251a`, `e64ebd7d980b`, `337c07df2601`, `95114beac3fb` (printed by `scripts/swap.sh` on every swap).
- **Merge-tree (Q8):** `merge-tree --write-tree develop 1993` rc 0, tree `49f054ac1f35` = the PR's own head tree.

**Host:** macOS Darwin 27, Node **v26.8.1** (not LTS 24), TypeScript 5.9.3 (both packages' installs), Vitest 4.1.12. Load 10-19 throughout; no cell of mine timed out, so no solo re-run was needed. I did NOT run on Node 24, in a container, against a real Identus agent, a real service health endpoint, a booted api-gateway or vc-issuer, Postgres or Redis.

**Install.**
- packages/shared: lock blob `c100fb8e9447` at develop, at 1993 and in gate 176's checked-out file (hash-object); root lock `30777ce9cb6f` at both refs. I APFS-copied (`cp -Rc`) gate 176's `packages/shared/node_modules` and `scratch/vt` into MY workdir; 0 symlinks resolve into gate 175/176 (positive control: the gate 176 copy's own 2 links point at gate 176).
- services/api-gateway: installed from its OWN lock (`63d57dfbf98b` at both refs) with `npm ci --prefix <repo>/…/api-gateway --ignore-scripts` under `env -i HOME=<workdir>/home`; 311 packages, lock unchanged afterwards.
- Disk 24 GiB free at start and end (floor 18).

**Method.** `scripts/swap.sh base|head` writes develop's or the PR's blobs for the 4 product files; tests stay at head. Recorders in `harness/` drive the REAL modules with gate 175/176's **17 value classes** (`harness/values.ts`, sentinel `SNTL177`), plus 2 EXTRA classes beyond the commission (V18 an Error instance whose `message` is a Symbol, V19 one whose `message` is an object whose toString throws), reported separately:
- `verifier.test.ts`: the real `VerifiableCredentialVerifier.verify()` on a REAL Ed25519 credential signed by the package's own `signCredential` (in-memory key, never written), so every check except the signature passes and `verified` can only be true through a passing signature check. Five trigger points inside `verifySignature`: T1 HMAC proof, resolver rejects on the signature call only; T2 Ed25519 proof, same; T3 HMAC proof, the resolved `publicKey` getter throws (outer try); T4 Ed25519, the getter throws on its 2nd read (reaches the INNER catch at line 400); T5 the resolver rejects on EVERY call (the issuer-DID lookup too, which is what the same resolver does in practice: the signer DID and the issuer DID are the same DID here).
- `clients.test.ts`: real `IdentusClient.resolveDID` (fetch rejects / `json()` rejects / `ok` getter throws), its callers `DIDManager` lines 89/128/181 and `DIDResolver` line 140 with a real IdentusClient injected (see F4), and real `ServiceClient.healthCheck` (fetch rejects / `ok` getter throws).
- `dashboard.test.ts`: the real api-gateway health-dashboard router on a REAL express app on 127.0.0.1 (ephemeral port), requested over a real socket with `node:http`; only the probe `fetch` is replaced. Layout A: 1 deployed (bad) + 1 localhost; layout B: 1 bad + 5 up + 1 localhost.
- Output captured at `console.*`, `console._stdout/_stderr` and `process.std*.write`. Scored by `scripts/classbar.py` (reference = BASE's V01 ordinary-Error outcome per site; message TEXT excluded, outcome/booleans/types/shapes compared) and `scripts/sentinel.py`. Raw rows: `results/q_{base,head}.jsonl` (363 per tree); side by side: `results/table.md`, `results/q1_table.txt`.

## Findings

### G177-F1 — LOW (correction to the READY; read, not driven): the verifier DOES have production callers, through `verifyCredential`; neither configures the DID resolver the changed catch needs
- **FOUND:**
  - The READY says `VerifiableCredentialVerifier` has no non-test user outside `vc/`. True for the class name (4 files, all in `vc/` or tests). But the same module's `verifyCredential()` (verifier.ts:612, `createVCVerifier(config).verify()`) is imported from `@secuura/shared/vc` by **vc-issuer** `routes/credentials.ts:360` (`POST /api/credentials/verify`, commented "public since KS-442 — tokenless") and `routes/presentations.ts:330` (`POST /api/presentations/verify`).
  - Both pass `checkStatus/checkExpiration/checkBlockchain` and `revocationVerifierConfig()` only. **`didResolver` appears in 0 non-test files outside verifier.ts** (positive control: 10 hits in verifier.ts by the same grep). Every hostile-value trigger I found inside the outer try goes through `this.config.didResolver`; the request body is zod-parsed JSON. So, as read, the changed line 417-424 is not reachable with a hostile value from either route's config.
  - What they do with each outcome (read): credentials `/verify`: a rejection goes to `next(error)` (the error handler's 5xx path); `verified:false` answers 200 `{verified:false, result}`. presentations `/verify`: `Promise.all` rejects into `next(error)`; a `verified:false` credential makes the presentation `verified:false` (`allCredentialsValid`). **Neither turns either outcome into `verified: true`.**
- **TESTED:** `git grep -w` at the head tree over the whole repo (not the sparse worktree). The routes were read, not driven (vc-issuer not installed).
- **HOW:** `results/census_q2.txt`. Negative control: a nonexistent name gives rc 1. Positive controls: the same grep form finds 6 `@secuura/shared/security/scopes` importers and the vc-issuer `signCredential` import.

### G177-F2 — LOW, PRE-EXISTING (base = head): verify() still REJECTS when the same resolver also throws the unreadable value at the issuer-DID lookup, and the inner Ed25519 catch is still unguarded
- **FOUND:**
  - **T5 (resolver throws on every call):** `verifyIssuerDID`'s catch (line 458-459) builds `` `Failed to resolve DID ${issuerDID}: ${error}` ``, unguarded. For 7 of the 16 non-ordinary classes (message getter, revoked Proxy, `Object.create(null)`, throwing get trap, thrown Symbol, name getter, throwing toString) `verify()` REJECTS at both trees. So the READY's "verify() now answers instead of rejecting" holds only when the issuer-DID lookup does not also throw an unreadable value; with one shared resolver and signer DID = issuer DID it usually would.
  - **T4 (inner catch, line 400-402):** `verifyErr instanceof Error ? verifyErr.message : String(verifyErr)` is unguarded too; for 5 classes it throws, the outer (now guarded) catch receives the NEW readable error, and the entry reads `Signature verification error: …` instead of `Ed25519 verification error: …`. Same at both trees.
  - **Every one of these 12 cells fails CLOSED** (rejection or `verified:false`, `signature:false`). None is more permissive than base-ordinary.
- **TESTED:** recorder cells at both trees. **HOW:** `results/classbar.txt` (the 12 `head!=base-ordinary` lines without V18/V19), `results/q1_table.txt`.

### G177-F3 — LOW, PRE-EXISTING (base = head; EXTRA classes beyond the commission): an Error INSTANCE with a non-string `message` passes every new guard (the read succeeds) and breaks the use
- **FOUND:** V18 (Symbol message) and V19 (object message whose toString throws):
  - verifier: the template literal `` `Signature verification error: ${msg}` `` sits outside the guard, so `verify()` REJECTS at T1/T2/T3 (6 cells) and T5 (2), both trees. Fail closed.
  - resolveDID returns `errorMessage` of type symbol/object (6 cells), healthCheck returns `error` of type symbol/object (4), and the dashboard entry's `error` is dropped from the JSON (Symbol) or `{}` (8 cells), both trees. `didDocument` stays null, `healthy` stays false, status stays `down`.
  - This is the gate 175/176 F2 shape (the use sits outside the guard). Not this PR's regression.
- **HOW:** `results/classbar.txt` (V18/V19 lines), `results/table.md`.

### G177-F4 — LOW (correction to the READY): the did-manager / resolver lines the READY names do not reach IdentusClient
- **FOUND:**
  - `did-manager.ts` 89/128/181 and `resolver.ts` 140 call `this.client` / `this.prismClient`, which both constructors set with `createPRISMClient()` → **`new MockPRISMClient`** (mock-client.ts:453). `IdentusClient` / `createIdentusClient` have **0 non-test constructions or imports** anywhere in the tree, and `prism/index.ts` does not export `identus-client` (positive control: it does export `mock-client`, `did-manager`, `resolver`); the package barrel and `exports` map carry no prism path.
  - To answer Q3's caller question anyway, I injected a real IdentusClient into those fields and drove them (C1 control: a found DID flows through all 4 callers, proving the injection is live): see Q3 below. Every caller treats `didDocument: null, error: 'notFound'` as not found.
- **HOW:** `git grep -w IdentusClient|createIdentusClient` (hits: the class file and the PR's test only); `harness/clients.test.ts`.

### G177-F5 — LOW (test gap): mutant H5 (drop the DOMException-name probe in checkService) survives the PR's tests and all 17 classes, and it is NOT equivalent
- **FOUND:** a `DOMException('…','AbortError')` whose `name` getter throws (call it VX; outside the 17): head lists the service `down` with the constant; H5-mutated head and base both lose the service from the dashboard (the oracle fails: `expected undefined to be 'down'`). So head handles VX correctly, but nothing pins that probe line.
- **HOW:** `scripts/mut_h5.sh`, `results/mut_h5.txt` (head rc 0, H5 rc 1, base rc 1); the clone was restored to head after (`git diff --quiet` = clean).

### G177-F6 — LOW (disclosure): the seat's patch-group tree `844fb7714826` does not reproduce
- **FOUND:** it is an object in neither the checkout nor my clone, and is not any subtree of develop or 1993 (Blockchain, Dev, packages, shared, src, services). It appears only in the commission, not in the READY mail. My trees: develop+1990+1991+1992 = `70bbceb1bf16` (equal to gate 176's), develop + all four = **`ce7a5d0d1a99`** in 3 orders (1990,1991,1992,1993 / 1993,1992,1991,1990 / 1993,1990,1991,1992), every step rc 0.
- **HOW:** `scripts/mergetree.sh`, `results/mergetree.txt`.

### G177-F7 — LOW, PRE-EXISTING (base = head; not this PR's lines; note for Wednesday): with no DID resolver (the vc-issuer config), the verifier accepts a credential "signed" with the source's default dev key even in production mode, and any `z…` proof outside production
- **FOUND (module driven, route not):** `verify()` with `{}` config and `VC_SIGNING_KEY` unset:
  - a `zDEV_` proof HMAC'd with the literal default `'secuura-dev-signing-key'` (verifier.ts:356): `verified:true, signature:true` under `NODE_ENV=test` AND `NODE_ENV=production`;
  - a forged `zFORGEDgate177` Ed25519-form proof: `verified:true` under `NODE_ENV=test`, refused under `production` ("No DID resolver configured");
  - control `xBAD`: refused at both. All 6 cells identical base = head.
- **Not measured:** whether vc-issuer runs with `VC_SIGNING_KEY` set (production compose passes it through; when it is set, the `zDEV_` key is that value, not the default) and `NODE_ENV=production`; and the route's revocation resolvers, which fail closed on an unknown credential id (so a forgery would need an id with a stored, unrevoked record). I did not check whether this is already ticketed. It does not bear on this merge.
- **HOW:** `harness/nores.test.ts`, `scripts/nores.sh`, `results/nores.jsonl`.

## What passed (measured)

**Q1 (the credential verifier; decides the weight).** 17 classes × 5 triggers = 85 cells per tree (+10 extra V18/V19).
- **The class bar: head cells with `verified: true` or `checks.signature: true` where base did not verify: 0 of 95.** `verified:true` cells: base 0, head 0; `signature:true`: base 0, head 0.
- **T1-T3 (the PR's site, resolver/getter throws on the signature call only):** 48 non-ordinary cells; head = base-ordinary (resolves, `verified:false`, `signature:false`, one `Signature verification error:` entry) in **48/48**. 15 changed, every one REJECT → that ordinary result (message getter, revoked Proxy, `Object.create(null)`, throwing get trap, throwing toString × 3 triggers).
- T4/T5: 32 cells; 20 = base-ordinary, 12 = G177-F2 (base = head, fail closed).
- `verify()` REJECTED cells (17 classes): base 22 → head 7 (all 7 = F2 T5).
- **Ordinary verdicts unchanged, no throw (5 controls, byte-identical rows base = head):** valid Ed25519 credential with the real key → `verified:true`; subject tampered after signing → false ("Ed25519 signature verification failed"); valid signature but a different resolver key → false; HMAC proof with the wrong key → false; valid credential with no resolver → true (pre-existing, `NODE_ENV=test`, see F7).

**Q2 (callers).** See G177-F1: 2 production call sites via `verifyCredential` (vc-issuer credentials.ts:360, presentations.ts:330); 0 configure `didResolver`; neither maps a rejection or a `verified:false` to success. The class's only other users are `vc/verifier.ts` itself and the barrel `vc/index.ts:10`.

**Q3 (IdentusClient.resolveDID).** 17 classes × 3 triggers = 51 cells per tree.
- **Non-null `didDocument` from a hostile value: 0 at base, 0 at head.** Head = base-ordinary (`null`, `notFound`, string `errorMessage`) in 48/48 non-ordinary cells; 15 changed REJECT → notFound. Rejections base 15 → head 0. Controls (found DID; agent 404) identical.
- **Callers (IdentusClient injected; 4 sites × 17 classes = 68 cells + 4 C1 controls):** head = base-ordinary in **64/64**; 17 changed, all toward it. At head every hostile class gives: line 89 throws `Failed to resolve created DID` (as an ordinary Error does); 128 `{connected:false, verified:false}`; 181 `null`; 140 the notFound result with **0 cache entries**. No caller treats the null/notFound answer as anything but not found.

**Q4 (health).**
- `ServiceClient.healthCheck`: 17 × 2 = 34 cells; `healthy:true` 0/0; head = base-ordinary 32/32; 4 changed (REJECT → `{healthy:false, error:'unreadable thrown value'}`). Controls 200 → healthy, 503 → `HTTP 503`, identical.
- `/dashboard` over HTTP: 2 layouts × 2 triggers × 17 classes = 68 cells + 4 controls per tree. **Bad service reported up/degraded: 0 hostile cells** at either tree (positive control: the 2 "bad answers 200" controls report it `up` at both). **Overall `status` differs base→head: 0 of 72; HTTP code differs: 0; healthy count differs: 0.** The bad service's entry is ABSENT at base in 8 cells (message getter, revoked Proxy) and present as `down` + constant at head (0 absent). Layout A is 503/unhealthy and layout B 200/degraded at both trees, as the READY read.

**Q5 (sentinel `SNTL177`; KS-1346/1348).**
- Log lines carrying it: **0 at base, 0 at head** across 350 hostile and ordinary cells. Positive control, same capture: the package logger, `utils/logger` `createLogger('service-client')` and `console.error` each yield 1 captured line with the sentinel, in shared and in api-gateway, at both trees.
- Answers carrying it: Q1 21/21, Q3 15/15, callers 5/5, healthCheck 6/6, dashboard JSON 8/8. **Cells where head prints or answers MORE than base: 0** (and LESS: 0). New hostile classes answer only the constant.
- **Pre-existing (base = head):** an ordinary Error's message (and the name-getter class's readable message) is answered in the dashboard JSON `error` field (8 cells), in the verifier's `errors`, and in resolveDID's `errorMessage`. Not this PR.

**Q6 (red first, suites, mutants).**
- **The PR's 16 cells:** at base 8 fail, **all 8 by AssertionError** (R1/R2 × 4 files); 8 pass (C1/C2 controls, by design). At head 16/16 pass. Note: the verifier file drives the private `verifySignature`, not `verify()`; my Q1 drives `verify()`.
- **Whole packages/shared suite** (own `vitest.config.ts`, sparse clone): base 63 files, 654 tests, 648 passed, 6 failed → head 66 files, 666 tests, 660 passed, 6 failed (648/654 → 660/666). **Failure set identical: 16 items** (10 files that cannot locate the Dev root in a sparse clone, entrypoint-corpus ×4, and the rest listed in `results/suite_summary.txt`). Delta +3 files, +12 tests, all pass. The seat's 1447 → 1459 is a full-checkout count; my delta is the same.
- **Whole services/api-gateway suite:** its own config in the sparse clone cannot resolve `@secuura/shared` (66 files fail to load at both trees): 149/813 → 150/817, failure set identical (97). Re-run with `harness/vitest.gate177.agwsuite.config.ts` (the package's own settings + aliases to the same tree's `packages/shared/src`): base 149 files, 1534 tests, 1204 passed, 43 failed, 287 skipped → head 150 files, 1538 tests, 1208 passed, 43 failed, 287 skipped. **Failure set identical: 35 items** (spec files absent from the sparse clone, real-app and lint cells). Delta +1 file, +4 tests, all pass. The seat's 1566 → 1570 "all pass" is a full-checkout count; the +4 matches.
- **Mutants** (raw table `results/mutants.tsv`, my count of its rows): **19 mutants. 18 KILLED by the PR's own tests, 1 SURVIVED (H5).** The gate oracle (`harness/oracle_*.test.ts`, all 17 classes, asserts outcome/type not text) kills 14; it survives the 4 constant-text changes by design. Killed by either: 18/19.
  - Kinds per site: inner catch rethrows (4: V1 I1 S1 H1), constant changed (4), use-line reads the raw value (3: V3 I3 S3), **fail-open** (V4 unreadable → `valid:true`; V5 catch records no error; I4 non-null didDocument; S4 `healthy:true`; H6 service `up`: 5, **all KILLED by both sets**), probe removed (H3 both, H4 message: KILLED; **H5 DOMException name: SURVIVED, not equivalent, G177-F5**).
  - Control: each unmutated module passed its PR test and the oracle (rc 0) before mutating; each blob was restored after.

**Q7 (tsc with tests).**
- packages/shared (`tsc --noEmit` over `src/**/*.ts` incl. `__tests__`, a workdir tsconfig extending the package's): **base 24, head 24, byte-equal lists.** Confirms the seat.
- api-gateway (`tsc -p tsconfig.test.json`): base 49, head 49, **byte-equal**. 24 of them are sparse-clone artefacts (21 TS2307 `@secuura/shared` not found + 3 TS7006 in `index.ts`/`platform.ts` that follow from it); the other **25 equal the ratchet baseline `baseline-api-gateway.txt` exactly** (file + code + count: csrf 10, ks1165 4+1, ks1374 1, ks1464 2, ks695 1, rateLimitEnforce 6). Confirms the seat's 25/25.
- The PR's 4 new test files contribute 0 errors in either list (positive control: the same grep finds the csrf/ks1179 lines).

**Q8.** See Subject and G177-F6. Shared paths with 1990, 1991, 1992: **0 / 0 / 0** (control 1993∩1993 = 10); only directories are shared (`packages/shared/src/__tests__`, `Projects Documents/fragments/{cheat,flow}`), with different file names. 4-PR group tree `ce7a5d0d1a99` in 3 orders, all rc 0. Planted control: a develop-side edit of the same verifier catch line merged against 1993 gives rc 1, `CONFLICT (content)` in `verifier.ts`.

## NOT tested
- No real Identus agent, service health endpoint, booted api-gateway (the router was driven on my own express app, not the gateway's `index.ts` mount), vc-issuer, Postgres, Redis or network.
- vc-issuer's `/api/credentials/verify` and `/api/presentations/verify` were READ, not driven; whether either runs with `NODE_ENV=production` or `VC_SIGNING_KEY` set was not measured (F1, F7). "Production caller" in F1 means a non-test import in service source, nothing more; deployment was not measured.
- The real `fetch` and `AbortController` timeout path (a genuine `AbortError` → `timeout`) was not driven; only the stand-in fetch.
- No Node 24 / LTS; host Node v26.8.1. Not run: eslint, the test-types ratchet script itself (I compared tsc output with its baseline file), the four platform suites, the pre-push hook.
- My suite counts are sparse-clone counts, not the seat's full-checkout 1447/1459 and 1566/1570.
- The other unguarded reads in verifier.ts that the PR did not touch (inner Ed25519 catch 401, `verifyIssuerDID` 459, `checkStatus` 514/528/549, `verifyBlockchainAnchor` 578) were driven only at 401 and 459 (F2).
- The 2 `Projects Documents/fragments/*.html` files were not assessed.

## Plain answer for Kam
This change stops four error handlers from crashing when they meet a strange kind of error: the credential checker, the DID lookup, a service health check and the gateway's health dashboard. Now they give the same "failed" answer they already gave for a normal error. Nothing that was refused before is now accepted. A credential whose signature check hits one of these errors is still marked not verified, and a bad credential is still rejected. A real, correctly signed one still verifies. The health dashboard now lists a broken service as "down" instead of silently leaving it off, and its overall health rating does not change. Two separate, older things are worth a later ticket, and neither blocks this merge: the credential checker can still crash, which still means "not verified", if the same strange error also hits the issuer lookup; and without a DID resolver configured it trusts a well-known development key.

---
Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993/`.
- Tracked: `verdict.md`, `harness/`, `scripts/`, `results/`, `runs/`.
- Ignored (`.gitignore`): `repo/` (my `--shared` sparse clone at 8712cb11; it also holds harness copies in `src/__gate177__/` and the `vitest.gate177*.config.ts` files), `mut/` (a develop worktree of my clone, with the same configs), `scratch/` (vt install, tsc configs, `_quarantine_2026-11-04/` where I moved harness copies instead of deleting), `home/`, `tmp/`, `node_modules`.

Background processes: 4 started (api-gateway `npm ci` pid 70519; suite driver pid 22635 and its 4 suite children; mutant run pid 30359; plus foreground runs). All exited on their own; `ps` shows no gate177/vitest/mutate process at the end. I wrote nothing outside the workdir. The checkout was used with read verbs only (`ls-remote`, `cat-file -t`, `config --get`, `remote get-url`), plus `git clone --shared` from it; fetches went into my clone only.
