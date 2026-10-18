VERDICT: GO WITH NOTE at head ae9dd501b6971a5eb6e0db6bafce0560b2d7d8df (round 2 of 2)
moves callers onto the chain-first path: NO. No in-repo caller is rerouted: there are zero code callers at ae9dd501b697 (the control fired), the five tests/e2e callers and systemTest `verifyById` now get 401/404 rather than a successor, and nothing redirects the path. BUT the removed handler never had a hash-only chain answer, while the advertised successor POST /api/verification/verify takes the :1156/:1191 chain-first branch on every registry miss. I probed it: L1 and L6 report `isAnchored: true` there. So any EXTERNAL caller forced to migrate would land on KS-1634's defect, and whether any such caller exists rests on R's 0-call edge census, which I did not re-measure.
sha256/16: 46f8f032c375a8a4

# GATE N1: #1589 delta gate, TIER 1, round 2 of 2

`git ls-remote` at gate start (09:16 AEDT): develop `f95ad12fe5c22f8d037e7139d052363422463c79`, #1589 `ae9dd501b6971a5eb6e0db6bafce0560b2d7d8df`, #1568 `09588895db75354d829df2069452c82b787d8bc8`. All three match the brief. merge-base(develop, #1589) = 83ed01af.

## FOUND

**Item 4 (decisive).**
- **Old route's input:** `id` (path) plus an optional `contentHash`. The handler (gateway `routes/verification.ts:534` at develop) looked the document up BY ID through three tiers (originate, anchor-store, mock), and a miss answered 404 (:571-587). Its live chain scan (:635-659) ran only for a document it had already FOUND, with the strict guards `j.verified === true && !j.simulated`, a non-placeholder hash and an integer height > 0. The old route had no hash-only chain answer. R's sentence ("never on that code path") is true of the removed handler.
- **After removal:** POST /api/documents/:id/verify gets 401 at the gateway proxy mount (`routes/proxy.ts:635-640`). An authed caller with a documents scope reaches originate, which has no `/:id/verify` route: I grepped for it and the `'/:id/anchor'` control hit at documents.ts:1378. `publicDocumentsRouter` has one GET route only (:3077). No path lands on the chain-first branch.
- **Callers at ae9dd501b697:**
  - Census script: `n1/census.sh`. It covers literal, templated, concatenated and helper-name forms over the whole tree.
  - Control: at develop the same script finds ks1072:120 and ks1199:35, which build the path by concatenation. At the head they are gone.
  - Code callers in connectors, sdk, frontends, packages, scripts and services: **zero**. M1's finding holds.
  - Remaining callers:
    - `tests/e2e` ×5 (test-data.ts:82 → recruitment-helpers `verifyCredentialOnChain` etc., KS-1631).
    - `systemTest/playwright/clients/documents.client.ts:95-100` `verifyById`, used only by `notifications.spec.ts:40-43`, which expects an unauthenticated 401/403. The proxy mount still gives that.
    - Everything else is prose: BACKLOG, CLI-AGENT-INSTRUCTIONS, docs/diagrams, PLAN-*, TEST_IMPROVEMENTS, Testing/*.md, Projects Documents/*.md and the comment at `frontend/shared/src/schemas/verify.ts:3`.
  - `MCP Deployment/*` `/verify` refers to the MCP server's own route. `services/mcp-server/src/api-client.ts:77` already calls `/api/verification/verify`.
  - Nginx (all three confs): the only verify rewrites are the `/verify/` SPA. None touches /api/documents/:id/verify.
- **The successor DOES contain the path:**
  - The Deprecation `Link` successor was `/api/verification/verify` (`documents.ts:1530` at 83ed01af).
  - I drove the REAL `verificationRouter` POST /verify with a registry miss (`n1/n1probe.test.ts`, run in my worktree and then removed). Anchoring was called 9/9 times.
  - Results:
    - L1 (`verified:'false'`): `isAnchored:true`, txHash presented.
    - L6 (`simulated:true`): `isAnchored:true`.
    - L2/L3/L4: `isAnchored:false`, but top-level `verified:true` (hard-coded at :1271).
    - L5 `'4242'`: on-chain, which ruling (b) intends.
    - Controls: C1 and C2 are on-chain, and NEG (`verified:false`) gives `verified:false`, so the control fired.
  - The successor's existing callers already reached this branch before #1589: verifier frontend, issuer, outlook, gmail, connectors (whatsapp, flutter, libreoffice, nextcloud, euro-office), sdk/python and mcp-server. They are not moved by this PR.
  - KS-1634 is live today on the successor, whether or not #1589 merges.

**Item 1, delta.**
- `git diff 53cb4ec76ea7 ae9dd501b697`: 5 files, +214/−5. The files are SERVICES.md (−1), QUICK-REFERENCE.md (−1), RUNBOOK.md (1 row repointed), gateway `routes/verification.ts` (a doc comment on the `meetsVerificationLevel` dep only, :114-127; no executable change) and the new suite (199 lines).
- Nothing outside the 5 files. The product change is a doc comment only. The gateway and packages trees are identical between the head and my landing tree (empty `diff --stat`).

**Item 2, Major 1: CLOSED.**
- Red-first: the PR's suite was copied onto develop f95ad12 (the pre-removal gateway `verification.ts:534` plus `index.ts:820`). G1, G2 and G3 went red on assertions:
  - G1: `expected [ '/api/documents/:id/verify', …(10) ] to not include`.
  - G2: `[404, true]` ≠ `[404, false]`. The real handler answered its own 404 JSON "Document not found", which is exactly the trap G2 exists for.
  - G3: the index still lists the entry.
- G-C1, G-C2 and G-C3 were green in both arms. On the landing tree all 6 were green.
- Planted regressions at the head (`n1/mutants.sh`, restored by an absolute-path EXIT trap; tree clean afterwards):

| mutant | G1 | G2 | G3 |
|---|---|---|---|
| Ma `router.post(path)` → 200 JSON (M1's M9) | RED | RED | ok |
| Mb `router.post(path)` → 404 JSON itself | RED | RED | ok |
| Mc `router.post(path)` → 404 **text/html** itself | RED | ok | ok |
| Md `router.all(path)` → 200 JSON | ok | RED | ok |
| Me `router.all(path)` → 404 text/html | ok | ok | ok |
| Mf `router.post(path)` → 200 text/plain | RED | RED | ok |
| Mg `router.post('/api/documents/:docId/verify')` → 200 JSON | ok | RED | ok |
| Mh `app.post(path)` in **index.ts** before the router → 200 JSON | ok | ok | ok |
| Mi `/api` index entry re-added (M1's M10) | ok | ok | RED |

- **G2 discriminator, judged:**
  - The content-type rule alone is fooled by a handler that answers 404 HTML (Mc), but G1 catches that one.
  - G2 catches what G1 is blind to: `router.all` (Md) and a renamed param (Mg).
  - Me is an equivalent mutant: it behaves exactly like an absent route.
  - The pair G1+G2 is sound for the router file. R's "weakest link" self-assessment is fair but not a defect.
- **Residual:** Mh. Re-adding the route at app level in `index.ts` reddens nothing, because G1 and G2 read only the `createVerificationRoutes` router. Minor 1 below.
- Mi shows M1's Minor 2 (the index text) is now pinned by G3.

**Item 3, Major 2: CLOSED, with count errors.**
- I read the README at `5_Project_History/quarantine/2026-10-19-seatR49-ks1628-pr2/README.md` (69 lines).
- The ks1057 :357 heal now has an ENDED row (line 18) with its reason. The citations check out at develop:
  - `confirmStalePendingAnchor` starts at :426 (`:427` is its first parameter, which is fine).
  - `:436-437` are the `failed` and `return blob` lines, exact.
  - `:454` is the strict `chain?.verified !== true`, exact.
- The ks1069 O1 block now has a row (line 20) and a LOST block (lines 39-58) pointing to KS-1634. `:712` and `:1191` are exactly `if (chain?.verified)`. There are 0 `chain.simulated` reads in the file; the `chain?.verified` control finds 3 sites.
- My probe reproduces the LOST pair on the live route: L1 and L6 report on-chain.
- Both quarantined files are byte-identical to their 83ed01af blobs (`git hash-object`).
- Count errors: Minor 2 below.

**Item 5, R's judgement calls.**
- **RUNBOOK.md:263 repoint is half right.**
  - The literal symptom "Document not found" is real on the successor: `originate verification.ts:1427` and `:1479` give "Document not found in the registry" (the documentId-only strategy).
  - The named cause ("Bearer token not forwarded to originate", `[CSRF]` 403) does not apply to `/api/verification/verify`. That route is public and CSRF-excluded (`api-gateway middleware/csrf.ts:113-119`).
  - On `/api/certifications/:id/verify` the bearer IS forwarded (gateway `verification.ts:336-337`), but that route's message is "Certification not found".
  - It is a Nit and stays in the doc.
- **`meetsVerificationLevel`:** I confirmed `services/enforcement.ts:54` is defined and called at `:153` inside `enforceDocumentTypeRules` (:97). The dep is read nowhere in `routes/verification.ts` (only the declaration at :128). index.ts :49 and :904 pass it.
  - The comment says "14 `__tests__` doubles". I count 15 files, because the new suite is the 15th.
  - I did not look up KS-1635 in Linear.
- **G2:** judged above.

**Item 6.**
- Merge predictions (`git merge-tree --write-tree`), all clean:
  - #1589 onto develop f95ad12 → tree `1ca89b2b5b7280ced0760012b09338dec94766aa`. That equals R's predicted 1ca89b2b5b72.
  - With #1568 in both orders (develop+1589+1568 and develop+1568+1589) → `9d456fd9d6aff5548eb3db8e99939a7bfa69bcd8`, so the order does not matter. #1568's 11 files and #1589's 34 files have no file in common.
- Suites on tree 1ca89b2b, with `packages/shared` rebuilt in that worktree (tsc rc 0, 29 dist entries):
  - api-gateway: **1106/1106** (112 files).
  - originate: **1442/1442** (117 suites).
  - Both exactly match R.

## README property table (ks1057 and ks1069, the M1 Major 2 blocks; rest unchanged from M1)

| property | old cell | status | new home / reason / ticket | checked how |
|---|---|---|---|---|
| anchor_failed blob with hash+height not on-chain | ks1057 :207 | RE-HOMED | precursor F1 | M1 mutant M4; cell exists in precursor it.each |
| declared-simulated not on-chain | ks1057 :229 | RE-HOMED | precursor C5 | read |
| tier-2 failed / submitted not on-chain | ks1057 :316 :324 | RE-HOMED | precursor F2, C8 | read |
| statusless legacy blob on-chain | ks1057 :269 | ENDED (stricter, ruled) | precursor C7 refuses | read |
| live chain heals an anchor_failed blob | ks1057 :357 | ENDED by design | `confirmStalePendingAnchor` returns failed blobs untouched, :436-437 | citations read at develop; not executed (not exported). README says so |
| placeholder hashes (persisted) | ks1069 E1 E2 E11 | RE-HOMED | precursor C6, X1; originate ks1626 | read |
| `simulated` truthiness (persisted) | ks1069 E3 E4 E12 | RE-HOMED | precursor S1 S2 C3 | read |
| height shape (persisted) | ks1069 E5 E6 E8 E9 E10 | RE-HOMED | precursor H1–H8, C1 | read |
| digit-string height refused | ks1069 E7 | RETIRED (ruling b) | precursor C9 pins the opposite | read |
| live reply: placeholder hash | ks1069 L2 | RE-HOMED (on-chain claim only) | precursor C6 via `presentBlockchainHonestly` | my probe: `isAnchored:false`, txHash null; top-level `verified:true` |
| live reply: height −1 / 4242.5 | ks1069 L3 L4 | RE-HOMED (on-chain claim only) | precursor `isAnchorHeight` H1/H8 | probe: `isAnchored:false`; txHash still presented, `verified:true` |
| live reply: numeric-string height refused | ks1069 L5 | RETIRED (ruling b) | precursor C9 | probe: on-chain |
| live reply: string `verified` | ks1069 L1 | **LOST → KS-1634** | :712, :1191 truthy read | probe: `isAnchored:true` |
| live reply: declared `simulated` | ks1069 L6 | **LOST → KS-1634** | never read off `chain` | probe: `isAnchored:true`; grep 0 `chain.simulated`, control 3 `chain?.verified` |

## TESTED / HOW
- **Clone:** `git clone --shared` into `scratchpad/n1/repo`. I set origin to `git@github.com:Secuura/Distributed_Secuura.git` and fetched develop and pull/1589 and pull/1568 with the checkout's `core.sshCommand` plus `ServerAliveInterval=30`.
- **Worktrees:** `wt-land` (a predicted merge commit e41265f4 → tree 1ca89b2b) and `wt-dev` (develop).
- **node_modules:** symlinked to the master checkout's installed modules (read-only). `@secuura/*` was re-pointed to each worktree's own packages, and `packages/shared` was built with `tsc -p <abs>` in each.
- **Commands:** vitest/jest invoked by absolute binary with `--root`/`--config`. Every loop ran from a script file under `n1/` with `/bin/bash`; temporary files were restored by EXIT traps with absolute paths. The trees had no dirty tracked files afterwards (`git status`: only the untracked node_modules symlinks).
- **Scripts:** `merge.sh`, `wt.sh`, `redfirst.sh`, `mutants.sh` (+`parse.py`), `census.sh`, `suites.sh`/`orig.sh`, `probe.sh` (+`n1probe.test.ts`).

## NOT tested
- No live HTTP against a running stack and no kintsugi/demo access. The external-caller population (R's 0-call edge census) is unmeasured by me. This is the one open leg of item 4.
- tests/e2e and systemTest/playwright were not run (KS-1631).
- R's leg 16 (`check.cjs`) and ESLint claims were not re-run on this delta.
- KS-1634 and KS-1635 ticket contents were not read (no Linear access used).
- `confirmStalePendingAnchor` was not executed (not exported). The ENDED row rests on reading the code, as the README itself states.

## Severities (file:line)
- **Minor 1:** the removal pin covers the router file only. An app-level re-add in `services/api-gateway/src/index.ts` (Mh, before `app.use(createVerificationRoutes(` at :901) reddens no cell. M1 offered "or an app-level cell that the path reaches the proxy mount's 401"; that is the cell that would close it. Not blocking: the file that served the route is pinned.
- **Minor 2:** the README miscounts the O1 block.
  - Line 20 says "FOUR KEPT, ONE RETIRED, TWO LOST" (7 for 6 cells), and line 41 says "keep four of its six". Only three are kept (L2, L3, L4).
  - "Kept" holds for `checks.isAnchored` only. The successor still answers top-level `verified:true` and presents the txHash for L3/L4 (my probe), where the gateway answered `verified:false, off-chain-only`.
  - Also: "19 `simulated` matches" measures 20 lines here. Immaterial.
- **Minor 3 (pre-existing, not this PR):** KS-1634 is live on POST /api/verification/verify and /verify-file today, for the successor's existing callers (frontends, connectors, sdk, mcp-server). The follow-up is already ruled (iii). Its priority should not rest on "nobody migrates".
- **Nit 1:** the new suite's header (`ks1628-gateway-documents-verify-is-removed.test.ts:18-33`) still describes "R1/R2/R3, C1-C3" and says R2 reads a `fetch` spy at 0 calls. The G2 cell (:166-168) says a fetch count cannot do that job, and `fetchSpy` (:53) is asserted nowhere. The G2 title still says "fetches no document".
- **Nit 2:** `Blockchain/Dev/deployment/azure/RUNBOOK.md:263`: the repointed cause (bearer, `[CSRF]`) does not apply to the public, CSRF-excluded `/api/verification/verify` (`api-gateway/src/middleware/csrf.ts:113`).
- **Nit 3:** the doc comment at `services/api-gateway/src/routes/verification.ts:120` says "the 14 `__tests__` doubles". There are 15 files including the new suite.

## Self-report
- `wt.sh` used one `$(cd … && pwd -P)` subshell inside my own scratch worktree to print the resolved `@secuura/shared` target. It was read-only and inside n1/. No other cd was used.
- Hooks refused a `$VAR`-pathed `git -C` and a mixed mkdir+read call. I re-issued them with literal paths and split the calls. No hook was bypassed.

MODEL: claude-opus-5-5
WALL-CLOCK: 12 minutes (09:15:56 -> 09:28 AEDT)
