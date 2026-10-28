# QA gate 3 (tier 2, batch, round 1 of 2): Secuura #1777 (KS-1240 p3), #1778 (KS-1472), #1781 (KS-1394), #1783 (KS-1588), #1784 (KS-1537)

- **Gate model:** Claude Sonnet 5.5 (claude-sonnet-5-5), G2 tier-2 batch gate, subagent of Wednesday. Spark review model: deepseek-v4-flash-0731 via the tunnel. Routing receipt as commissioned: claude-sonnet-5-5, G2 tier-2 batch gate, gauge ~74%.
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing. Linear was read-only (KS-1240, KS-1472, KS-1394, KS-1588, KS-1537; comments first:100; key never printed). `gh` is not authenticated in this shell, so the PR bodies were NOT read; each PR's own Flow-doc block and Linear comment stood in for them. Writes were confined to my own clone, my own scratch worktrees, one Docker container I started and removed, and this folder plus the work folder.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate3-batch5/repo` (did not exist; `git -C <path> rev-parse --show-toplevel` asserted equal to that path before the first fetch; origin set to GitHub, deploy key via GIT_SSH_COMMAND with `-o ServerAliveInterval=30 -o IdentitiesOnly=yes`). Re-asserted at the end. Worktrees and scratch: `/private/tmp/claude-501/gatework3/` (spark_gate.sh refuses a work dir under WEDNESDAY). Worktrees (w1777, w1778, w1781, x1781, w1783, w1784, b1781 = develop, m1778_1784 = scratch merge, sg*) were NOT removed (no-delete rule). Evidence under `.../gate3-batch5/out/`.
- **node_modules:** read-only symlinks from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/` for every run. ONE exception, in my own scratch only: for #1784's integration file the Prisma client had to be generated, which would have written `.prisma/client` into the shared tree, so I replaced the symlink in `w1784/.../services/originate` with a private `cp -Rc` copy (the symlink was moved to `/private/tmp/claude-501/gatework3/_quarantine/`), generated there, and pointed `@secuura/shared` at the worktree's own freshly built `packages/shared` (the shared tree's `dist` is stale and lacks `signEmitterHop`). I checked afterwards that `Dev/services/originate/node_modules/.prisma` does not exist in the shared tree. Node v26.8.1 (not the repo's LTS 24) on every run.
- **Load:** load1 was 3 to 9.4 at every heavy run, never above 14. Spark queue lock clear.

## Pins (git ls-remote)

| ref | start (20:19) | end (20:50) |
|---|---|---|
| develop | 2b7ef12fa5649db641bb3a81f5615ac48704036a | same |
| refs/pull/1777/head | 85530f156f771dfe024249340e40a3b0720669c7 | same |
| refs/pull/1778/head | a4c6989224720362b711710a9c931ebe540e7864 | same |
| refs/pull/1781/head | 4b679ffe26aec36badf5c718a7ede7f3f0f76edb | same |
| refs/pull/1783/head | 30d5f583c4d0e29586509568ed3e81d7a58b5c9a | same |
| refs/pull/1784/head | 66c36a960af6128bdc9c8f8a59f50f115cf52b9c | same |

All five equal the brief. Nothing moved. Merge-base of all five with develop is bd6697e079fc; develop's only commit since is `2b7ef12fa Refs KS-1467 ... (#1775)`, which is why every doc-carrying PR now conflicts with develop (docs only, see merge-tree).

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1777 | KS-1240 p3 | **GO WITH NOTES** | All 8 outbound fetches in `ipfs.service.ts` carry a bound; 15/15 at head, 3/12 at base, nine of my own mutants each killed by the predicted cells; suite 61 to 76, 0 failed. Notes: KS-1240 stays open (its own named fetch, api-gateway key-validate, is not here), merge-time docs, a disclosed 30 s behaviour change. |
| #1778 | KS-1472 | **GO WITH NOTES** | Of the three contract sentences, 3 MATCH the code. One residual phrase, "a route that requires no scope accepts any valid token", still OVERSTATES for role-gated routes (ticket-sanctioned wording, Low). ks1210 header MATCHES. `check:openapi` rc 0 at head, rc 1 when the source hunk is reverted, rc 0 on the scratch merge with #1784. |
| #1781 | KS-1394 | **GO WITH NOTES** | The new printed commands, run for real in `node:24-alpine`, do what the comment says (pin moves, rc 0); the old command fails EMISSINGTARGET (reproduced). Verdict, exit codes and stdout are byte-identical to base; only stderr differs. Note: the PR has no test, so the text is unpinned. |
| #1783 | KS-1588 | **GO WITH NOTES** | 8 to 13 cells, route unchanged. Eight planted defects killed by the predicted cells; two plants SURVIVE (an `X-Error`-style header on the 500 path, a header only on the not-registered path). Exact default-header set is Node/Express-version sensitive. |
| #1784 | KS-1537 | **GO WITH NOTES** | 12/12 in both tenancy modes on a real PG 15.19 as `secuura_app`; every claimed mutant killed by the claimed cells, plus my own; contract sentences MATCH the code lines. Finding: a pre-existing sentence on the org-erasure operation (originate.openapi.ts:3717, yaml 31333) now contradicts the new text. |

**Recommended merge order:** **#1781, #1783, #1777, #1778, #1784.** #1781 and #1783 first (script-only and test-only, no docs for #1781). Then the product PR #1777. Then the two contract PRs, #1778 before #1784 (both regenerate the yaml; they auto-merge in either order, proven below, and #1778's regeneration is the smaller). All five are disjoint in code; only the yaml (#1778 and #1784) and the two docs are shared.

**Docs sections** (develop's highest is 84 after #1775; 85 and 86 are already assigned to #1776 and #1780): assign in the order above, **#1783 = 87, #1777 = 88, #1778 = 89, #1784 = 90; #1781 carries no docs.** Heads currently carry: #1777 and #1778 `<h2>84.`, #1783 and #1784 `<h2>85.` (collisions with develop's 84 and with #1776's 85). At merge rewrite the sub-headings and cross-references inside each block: #1783 has `85.x` (to 87.x), #1777 `84.x` (to 88.x), #1778 `84.x` (to 89.x), #1784 `85.1` to `85.3` and in-text "85.3" (to 90.x). The cheat-sheet `<h2>`s are unnumbered. Each head's flow and cheat-sheet block is a pure insertion before the single `</body>` (checked: head == base[:i] + block + base[i:] against bd6697e, all eight files). **Also:** PR #1782 (KS-1240 p4, outside this batch) carries a placeholder 85 and needs the next free number after whatever lands first.

---

## Spark shadow (run FIRST, per PR; `out/p<n>b/`, `out/p1778c/`)

Method: `spark_gate.sh` per PR (work under `/private/tmp/...` because the script refuses WEDNESDAY), `--node-modules` = the Dev root `node_modules` (a service-level `node_modules` has no `vitest` binary: my first attempt at #1777 gave "vitest: command not found" and a vacuous 0/0, kept as `p1777_try1`, not counted). Then `spark_review.py` with `facts_spark.json` = facts minus the two Projects Documents html files, AND minus `docs/openapi/secuura-api.yaml` (1.38 MB; same refusal reason, applied to #1778 and #1784), plus HARNESS LIMIT lines in `not_run` where the harness is blind. No PR body was supplied (gh not authenticated).

| PR | spark_gate (head / base product code) | Spark review |
|---|---|---|
| #1777 | 15 pass / 0 fail ; 3 pass / **12 fail** (matches the PR) | NO GO, 3 Major 3 Minor 1 Note; 59.6 s, 21,978 prompt tokens |
| #1778 | ks1210: 5/0 ; 5/0 (header-only change, expected). ks839 (run separately, `p1778c`): 5/0 ; **3 pass / 2 fail** | GO WITH NOTES, 6 Notes; 87.5 s, 59,216 tokens |
| #1781 | **VACUOUS**: the PR has no test file; the harness was given the unrelated `scripts/audit/gate-exit-codes.test.mjs`, vitest cannot run it, 0/0 rc 1 on both sides. Not a result, flagged in the facts. | NO GO, 2 Major 2 Minor 1 Note; 54.9 s, 12,879 tokens |
| #1783 | 13/0 ; 13/0 (test-only PR: base product code equals head, so this arm cannot be red; see my plants) | GO WITH NOTES, 4 Notes; 37.0 s, 13,088 tokens |
| #1784 | ks1537 pin: 9/0 ; **5 pass / 4 fail** (matches the PR). **`ks1508-...integration.test.ts` is NOT in this result: spark_gate is BLIND to `*.integration.test.ts` because jest ignores them; I did not count any 0/0 for it, and the HARNESS LIMIT line told the model so.** | attempt 1: SCHEMA FAILURE x2 (repetition abort, no usable review; `p1784b/spark/`). Retry in `p1784b/spark_retry/`: valid, NO GO, 3 Major 3 Minor 2 Note; 82.3 s, 154,684 prompt tokens over two attempts |

---

## #1777 (KS-1240 part 3, nft-certificate IPFS bounded fetches): GO WITH NOTES

Head 85530f156f77. Diff vs develop: `ipfs.service.ts` (+36/-3), new test (213 lines, 15 cells), two docs.

### Reading the diff
Eight `await fetch(` calls in the file: 3 x 60 s (uploads: Pinata, Infura, Web3.Storage), 4 x 15 s (pin and unpin on Pinata and Infura), 1 x 30 s (gateway read). Counted by hand at head: 8 `await fetch(`, 8 `signal: AbortSignal.timeout(...)`, nothing else in the file calls fetch (the other grep hits are a comment, the method definition and `this.fetch`). The gateway body read moved into a try that maps to `ServiceUnavailableError` (503). The upload and pin paths already swallowed errors into `success:false` or `false`, so an abort lands in the existing handling.

### Mutation check (own worktree `w1777`, product file rewritten from the PR blob and develop blob, restored by sha256 compare each time; `out/mut1777/`)
| mutant | result (15 cells) | red cells |
|---|---|---|
| M0 head | **15 / 15** | none |
| M1 develop's `ipfs.service.ts` (the whole product hunk reverted) | 3 pass / **12 fail** | IB1, IB2, IB3, IB4 x7, IB5, IB6 |
| M2 body try/catch removed | 13 / 2 | IB2, IB3 |
| M3 gateway `fetch(url)` with no signal | 11 / 4 | IB1, IB2, IB5, IB6 |
| M4 Web3.Storage upload without signal | 12 / 3 | IB4 (web3.storage), IB5, IB6 |
| M5 Infura unpin without signal | 12 / 3 | IB4 (infura unpin), IB5, IB6 |
| M6 pin bound 15 s to 20 s | 14 / 1 | IB5 (the constants pin) |
| M7 gateway signal hoisted to module load (one signal shared by every call) | 11 / 4 | IB1, IB2, IB5, IB6 |
| M8 body catch throws a bare `Error` | 13 / 2 | IB2, IB3 |
| M9 body catch swallows and returns an empty buffer | 13 / 2 | IB2, IB3 |
Full `nft-certificate` suite (vitest json, `out/suite1777/`): develop **61 passed / 0 failed**, head **76 passed / 0 failed**. Matches the PR's 61 to 76.

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1777-1 | Low (scope) | KS-1240's own text names only the api-gateway connector-token / key-validate fetch (T-2). This PR is the coordinator-extended part 3 (the PR says so; KS-1782 is part 4). The ticket stays open until the gateway fetch lands. Spark's Major 1 and Note are this fact. | FOUND in Linear KS-1240 (description plus both comments). Not tested (it is a scope fact). |
| 1777-2 | Low (disclosed behaviour change) | An IPFS object the gateway needs more than 30 s to deliver now answers 503 where it used to wait. Disclosed in the code comment and the PR; no cell drives a real 30 s read (IBC1 runs at a 5 s bound, IB5 pins the 30 000 constant, M6 shows a constant change is caught). | FOUND by reading; TESTED M6, M7. |
| 1777-3 | Info | Other unbounded outbound fetches remain in the same service: `minting.service.ts:148` and `:173` (calls to the originate service). Not in the PR's declared file; not asked for. | FOUND by `git grep "fetch("` at head, outside tests; not executed. |
| 1777-4 | Low (merge-time) | Docs block carries section 84; see BLUF for the number to use. | |

### Spark findings judged
- Major 1 (ticket scope not met): SCOPE NOTE, 1777-1. Major 2 (30 s trade-off untested): DISCLOSED, 1777-2. Major 3 (the 11 other red cells not enumerated): NOT REPRODUCED, I enumerated all 12 (M1 row). Minors (IB5 stub ignores the signal, IB6 is a regex): both are covered by other cells, IB4 uses a stub that honours the signal and a real http server covers IB1 to IB3; M3, M4, M5, M7 show IB5 and IB6 kill their mutants. Net: **no defect confirmed**.

---

## #1778 (KS-1472, authorize-contract wording): GO WITH NOTES

Head a4c698922472. Diff: `docs/openapi/secuura-api.yaml` (+7/-6, two hunks, GET and POST), `services/auth/src/auth.openapi.ts` (the two descriptions, +2/-2), the ks839 pin and two header comments in the ks1210 and ks839 tests, two docs. **Brief correction:** the source is `services/auth/src/auth.openapi.ts`, not an originate file (#1784 is the originate one).

### Every changed sentence against the code it describes
| Sentence (as published) | Verdict | Line read |
|---|---|---|
| "An **OAuth** token with no scopes satisfies no scope requirement" (point 1) | **MATCHES** | An OAuth-minted token carries `authMethod: 'oauth'` and a `scopes` array (`services/auth/src/services/jwt.ts:205` and `:229`); a plain login JWT (`authMethod` jwt or email) is waved through by `requireScope` (`services/api-gateway/src/middleware/scopes.ts:35-39`), so "a token" unqualified was wrong and "an OAuth token" is right. An OAuth token with `[]` falls to the 403 at `scopes.ts:57-62`. |
| "so a route that requires a scope refuses it (403)" | **MATCHES** | `scopes.ts:57-62` (`requireScope`) and `scopes.ts:184-192` (`requireScopeOrRole`) both answer 403. |
| "**unless the route also admits the caller by role**" (point 2) | **MATCHES** | `routes/platform.ts:92-100` `requireOrgProvisioner` admits `SUPER_ROLES` with no scope; `scopes.ts:158-182` admits an accepted role while the KS-843 grace is on. (The role arm in `requireScopeOrRole` is conditional on the switch, the sentence is unconditional but not wrong: it says "unless the route also admits".) |
| "a route that requires **no scope** accepts any valid token" (point 3) | **OVERSTATES (residual, Low)** | "requires no scope" is the ticket's own suggested wording and is better than "requires none". But "accepts any valid token" is still false for a route with no scope requirement and a role gate: `routes/platform.ts:66-72` `requireSuperAdmin` refuses a non-super-admin valid token with 403, and it is used at `:300`, `:317`, `:362` in a file that contains zero `requireScope` (counted: 0). The ks839 header added by this very PR says "role, MFA and tenant gates can still refuse a request on a route with no scope requirement". Ticket point 3 asked for exactly this wording, so it is ticket-sanctioned, not a regression: it is a wording residue to carry, not a blocker. |
| ks1210 header: "`redirectUris`, the only one either site's control reads ... this header used to name `name` too, which no cell checks" (point 5) | **MATCHES** | The test's `SITES` table has the sibling `'redirectUris'` at lines 87 and 88 and the control at 96 reads `sibling`; `name` appears as no sibling. |

### Checks
- Mutation (own worktree `w1778`, yaml rewritten from the PR blob or the develop blob, both ks839 and ks1210 files, restored and compared to the PR blob; `out/mut1778/`): head **10/10**; yaml reverted to develop **8 / 2** (the GET and POST RED cells); only GET updated 9/1 (POST red); only POST updated 9/1 (GET red); POST says "by scope" not "by role" 9/1 (POST red); GET drops the word "OAuth" 9/1 (GET red). Each one-site edit is killed by exactly that site's cell. Matches the PR's "10/10, 8/2, 10/10".
- Source-only revert (auth.openapi.ts back to develop, yaml new): ks839 and ks1210 stay **10/10** (they read the yaml, not the source), and **`npm run check:openapi` goes rc 1 "generated YAML differs from on-disk version"** (`out`: `chk_y6.txt` in scratchpad). So the source-to-yaml drift guard is `check:openapi`, not the cells.
- `npm run check:openapi` on develop: **rc 0**. At #1778 head: **rc 0** ("CHECK PASS: on-disk YAML matches generated"; spec examples 414 blocks OK).
- ks839 base-product arm (Spark gate `p1778c`): 3 pass / 2 fail. ks1210 base-product arm 5/5 (a header-only change cannot be red; by design).

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1778-1 | Low | Residual overstatement in "a route that requires no scope accepts any valid token" (table above); ticket-sanctioned wording. A later pass could say "the scope check admits it". | FOUND / TESTED by reading `platform.ts:66-72, 300, 317, 362`; not executed through a running gateway. |
| 1778-2 | Info | The gateway reads the yaml at boot, so the new text is served only after a deploy and restart (the PR says this). | Not tested. |
| 1778-3 | Low (merge-time) | Docs carry 84 and conflict with develop's own 84 block; see BLUF. | |

Spark GO WITH NOTES: six Notes, none a defect. Its first note ("not verified against the actual gateway behaviour") is closed by the table above.

---

## #1781 (KS-1394, audit-locks refusal message): GO WITH NOTES

Head 4b679ffe26aec. One file, `scripts/audit/audit-locks.mjs` +135/-3. Product-only; no test, no docs.

### What I measured
1. **Verdict, exit code and stdout are unchanged; only stderr differs.** `audit-locks.mjs` driven with a preloaded stub of the bulk-advisory endpoint (`scratchpad/stubfetch.mjs`, the URL is deliberately not configurable in the script) on base (develop) and head: with an advisory on `js-yaml` (present in 7 locks): rc **1 and 1**, stdout identical, stderr differs only in the new text. With a stub that reports nothing: rc 0 and 0, stdout identical, **stderr identical**.
2. **The printed commands work.** I ran the head's printed command for `../../systemTest/performance` exactly as printed, from Blockchain/Dev, in `node:24-alpine`: `docker run --rm -v "$PWD/../..":/app -w /app/systemTest/performance node:24-alpine npm update js-yaml --package-lock-only --ignore-scripts`: **rc 0, the lock moved** (js-yaml 5.4.3 to 5.5.0, argparse 2.0.1 to 3.0.4, 18 insertions / 8 deletions in one file). The command the OLD message pointed at (own-directory mount, `npm install --package-lock-only`): **rc 1, "Missing target in lock file: ../observability is referenced by node_modules/secuura-observability but does not exist"**. The printed clean-room check `npm ci --dry-run ... ` rc 0. A second `npm update` of the already-updated pin: rc 0 and the lock byte-identical, which is the text's own claim "a run that moves nothing still exits 0". All reproduced twice on a scratch worktree (`x1781`).
3. **Helper probes** (extracted `escapingLinkTargets`, `commonAncestor`, `dockerRun` from the head file, ran on eight synthetic locks): no link, mount = own dir; one escaping link, mount `$PWD/../..`, workdir `/app/systemTest/<x>`; two links to different trees, mount the common ancestor; a link inside the parent (`../../packages/shared`), mount `$PWD`; a path with a space or a semicolon: `null` (the code prints "(command not printed ...)"). All correct.
4. **The "no preflight leg clean-rooms these" claim MATCHES** `scripts/preflight/lockfile-cleanroom.sh:46` (`find services packages frontend scripts -maxdepth 2 -name package-lock.json`), and the printed unchecked list in my run is exactly the three systemTest locks.

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1781-1 | Low | No cell pins any of the 135 new lines or the text. A later edit can reintroduce an uncomputable mount and nothing goes red; the PR says "text only" and that is accurate. A follow-up cell over the helpers (the probe in `scratchpad/probe1781.mjs` is a ready start) would pin it. | FOUND by reading the diff; TESTED by the probes above. |
| 1781-2 | Info | For the two `systemTest` locks with an escaping link the mount is `$PWD/../..`, the whole repository checkout, read-write, into a container running `npm update ... --ignore-scripts`. It wrote one file in my run. | FOUND / TESTED (git diff --stat after the run). |
| 1781-3 | Info | The guidance only names packages the advisory lists; a fix outside the manifest range needs the range edited first (the text says so). Not exercised against a real range-blocked advisory. | Not tested. |
| 1781-H | Medium for the PROCESS, none for the PR | spark_gate cannot gate a PR with no test file: I fed it an unrelated existing file and it answered a vacuous 0/0 rc 1 on both sides. A reader of facts.json alone would see "0 failed". | FOUND in `out/p1781b/facts.json`. |

### Spark findings judged
Major 1 ("npm update may not move a pin outside the range"): DISCLOSED by the text itself and reproduced as stated (item 2, no-op rc 0). Major 2 (no test): TRUE, 1781-1, but it is a scope fact, not a defect in the lines. Minor 1 ("mount too narrow when a link target is a file"): NOT REPRODUCED, npm `file:` link targets are directories and the two-target and parent-link probes widen correctly. Minor 2 (several packages in one command): no evidence offered; one `npm update a b` command is the documented form. **No defect confirmed.**

---

## #1783 (KS-1588, wallet-status response cells, test-only): GO WITH NOTES

Head 30d5f583c4d0. `ks1009-wallet-status-reveals-only-existence.test.ts` +71/-3, two docs. Route unchanged: `git diff` of `services/auth/src/routes` and `middleware` between develop and head is **0 lines**. Cells: develop's file **8**, head's **13** (new: 7, 8, 9, C4, C5).

### Planted defects in `routes/wallet.ts` (own worktree `w1783`, restored and compared; `out/mut1783/`)
| plant | result (13 cells) | red |
|---|---|---|
| M0 head | 13 / 13 | none |
| N1 id in the body | 10 / 3 | 1, 2, C4 (the old body cells; C4 reads content-length) |
| N3 `X-User-Id` header | 11 / 2 | 7, 8 |
| N3b id in the `ETag` | 12 / 1 | 8 only (as the PR says) |
| N3c id in `Set-Cookie` | 11 / 2 | 7, 8 |
| N8 500 echoes the error message | 12 / 1 | 9 |
| N8b 500 echoes the requested address | 12 / 1 | 9 |
| N8d 500 becomes a 503 with the generic body | 11 / 2 | 9, C5 |
| N8e error swallowed, answers 200 | 11 / 2 | 9, C5 |
| **N8c error text in an `X-Error` header, generic body kept** | **13 / 13, SURVIVES** | none |
| **N3d a header only on the not-registered path** | **13 / 13, SURVIVES** | none |

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1783-1 | Low | **N8c survives.** Cells 7 and 8 read headers only on the REGISTERED answer; cell 9 reads only the 500 body and status. A defect that leaks the database error text (or the address) through a header on the 500 path is not seen. Spark Note 2 named it; I confirmed it by plant. Not one of the two mutants the PR claims (N3, N8), so it is a gap beyond the claim, not a false claim. | TESTED (plant above, `out/mut1783/N8c...json`). |
| 1783-2 | Info | N3d survives: a header on the not-registered path leaks nothing (no account exists), so this is mostly a statement of coverage. | TESTED. |
| 1783-3 | Low | `EXPRESS_DEFAULT_HEADERS` is an exact set of seven names measured on Node 26.8.1 with this Express. A different Node or Express (the repo's CI is Node 24, which I do not have) that adds or drops a default header makes cell 7 red with no leak. Spark Note 1. | FOUND by reading; not tested on another Node. |
| 1783-4 | Low (merge-time) | Docs carry section 85 (collides with #1776's 85 and with #1784); see BLUF. | |

Spark GO WITH NOTES, 4 Notes: Note 1 (headers environment-dependent) = 1783-3, CONFIRMED as a risk; Note 2 (500-path header leak survives) = 1783-1, CONFIRMED by plant; Notes 3 and 4 not defects.

---

## #1784 (KS-1537 m-1, N-1, N-2): GO WITH NOTES

Head 66c36a960af6. No product file changed (`routes/documents.ts`, `certifications.ts` untouched; verified by diff). Files: `originate.openapi.ts` (+8/-4), the regenerated yaml (+16/-4), the ks1537 pin (new, 68 lines, 9 cells), the ks1508 integration file ported (+93), two docs.

### Real Postgres (one container, `gate3-pg-1784`, postgres:15-alpine, `127.0.0.1:55432`; PostgreSQL 15.19 aarch64 musl)
Built as the PR's own section 85.4 says: `docker/init` mounted read-only, then the head's `scripts/run-migrations.sh` over the head's 57 migrations (`applied=57 failed=0`), then the platform-named migration applied to the main database so that `tenants` exists where the file's `INSERT INTO tenants` needs it (the PR's own run line says "all pointing at one migrated database"; my first run used a separate platform database and failed at SETUP with "relation tenants does not exist": harness, not PR). Checked: `secuura_app` is non-superuser and non-BYPASSRLS; `documents`, `charge_events` and `action_provenance` have row security forced. The test file runs as `secuura_app`.

| # | Check | Result |
|---|---|---|
| C1 | `MULTI_TENANCY_ENABLED=false`, head | **12 / 12** (SETUP proves role and branch) |
| C2 | `MULTI_TENANCY_ENABLED=true`, head | **12 / 12** |
| C3 | Leftover audit after both runs: tenants named `ks1508-%`, charge_events with no tenant, documents carrying a planted `connector:platform-s:` actor | **0 / 0 / 0** (the PR says it fixed a 16-row charge_events leak in its own cells; confirmed gone) |
| C4 | ks1537 contract pin (jest unit, via the Spark gate) | head **9 / 9**; yaml and openapi.ts reverted to develop **5 pass / 4 fail** (the four RED cells; matches the PR) |

### Product mutants (own worktree `w1784`, product file rewritten from the head blob and restored, compared; `out/it1784/`; the integration file, 12 cells; MT = tenancy mode)
| mutant | result | red |
|---|---|---|
| M0 head | 12/12 in both modes | none |
| X0 create strip removed | 9 / 3 | RED create, hash, hash2 |
| X1 strip moved BELOW the hash (the gate's X1) | 11 / 1, **both modes** | hash only |
| X2 strip applied to a throwaway copy | 9 / 3 | create, hash, hash2 |
| X5 thread-token hash over the caller's unstripped body (the PR's own X5, "HASH2") | 11 / 1 | hash2 only |
| G0 `...metadata` after the server keys on /version | 11 / 1 | RED /version |
| G1 same on /sign-cert | 11 / 1 | RED /sign-cert |
| G2 same on /sign-wallet | 11 / 1 | RED /sign-wallet |
| A6b certify spreads the caller's `data` | 10 / 2 | certify JSON, certify form-encoded |
| X4 case-variant strip in the certify destructure (re-derived at the tip) | 10 / 2 | certify JSON, certify form-encoded |
| MP certify spreads `data.__proto__` (the PR's own MP, "b16") | 11 / 1, **both modes** | the `__proto__` cell only |
(My first A6b compiled badly and showed "0 / 12": a compile error, not a kill; redone with a compile-safe form above.)
Extra, mine: each of the other three server keys made overridable alone on /version (versionAction, versionedAt, parentDocumentId): the PR's integration file stays 12/12 for all three (it reads only `versionedById`), but the develop unit file `ks1508-versionedbyid-is-server-set` (50 cells) goes **47 / 3** for each, so the four-key sentence is pinned by existing cells, just not by this PR's file.

### Contract text against the code
| Sentence | Verdict | Line read |
|---|---|---|
| Create: "`data.versionedById` is reserved: a value supplied in `data` is silently STRIPPED before hashing, because the actor of a version is set by the server on the version routes." | **MATCHES** | `routes/documents.ts:617-620` deletes the key from the copy `data` and logs ids only; the server hash is `generateContentHash(data)` at **:666**, after the strip. Caveat the sentence does not claim: a caller-supplied `contentHash` is used as is (`clientHash ||`). The brief's line numbers (strip 617-620, hash :666) are right; X4 re-derived at the tip is right. |
| /version, /sign-cert, /sign-wallet: "the `metadata` keys `versionAction`, `versionedAt`, `versionedById` and `parentDocumentId` are reserved: the server sets them after `metadata` is applied, so a value supplied for any of them is overwritten." | **MATCHES** | `documents.ts:2370-2379` (/version), `:3115-3124` (/sign-cert), `:3311-3320` (/sign-wallet): `...metadata` precedes the four server keys in each; plus the mutants above. |

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1784-1 | **Minor (contract self-contradiction)** | The org-erasure operation's description in the SAME spec still says "A writer can still hide a derivative from this erasure by setting its `versionedById` to `connector:<anything>`, until the server sets `versionedById` itself (KS-1508)" (`originate.openapi.ts:3717`, yaml line 31333). The server now does set it (create strips, certify strips, the three version routes write it after `metadata`; all of this is in the code at this head and measured above). The PR publishes the new reserved-key text on four operations and leaves the old limitation on the fifth, so a client reading the spec gets both. Not a defect in the PR's lines; a sentence it did not touch has become stale. Spark did not find it. | FOUND by `git grep versionedById` at head; TESTED only by reading the strip and spread lines and by the mutants (each of which would re-open the hole and is killed). I did NOT sweep every document-creating route in originate for another path that spreads caller `data`. |
| 1784-2 | Low (scope, disclosed) | N-4 is NOT built (the PR says so, and its section 85.3 measures that the certify response and the derived row's hash still see the planted value). The contract sentences added here make no claim about the certify route, which is the right call. Spark Major 2 is this. | FOUND in the PR's doc block; not re-measured. |
| 1784-3 | Low | Both AA PRs regenerate the yaml; the head yaml here has the create description re-quoted by the dumper (the PR notes it). Auto-merge with #1778 is clean (below). | See merge section. |
| 1784-4 | Low (merge-time) | Docs carry section 85, colliding with #1776's 85; see BLUF. | |
| 1784-H | Medium for the PROCESS | spark_gate is blind to the integration file (jest ignores it); 12 of the PR's 21 new cells live there. The first Spark attempt also produced no valid review (repetition abort) and the retry's prompt was 154,684 tokens. | FOUND in the facts and logs. |

### Spark findings judged (retry review)
Major 1 (cleanup deletes by `tenant_id`, could hit others): **NOT REPRODUCED**, the tenant id `T` is `randomUUID()` per run and my leftover audit and the PR's pre/post row count show nothing else touched. Major 2 (N-4 unaddressed): SCOPE NOTE, 1784-2. Major 3 (mint mock does not prove "only when the flag is on"): not what the cell is for; the cell asserts `mockMintCalls.length` is 1 under the flag and X5 shows it kills a wrong hash. Minor 3 (env not restored on failure): FALSE, the restore is in a `finally`. Minor 2 (`rawAs` does not check 201): callers assert the status (`expect(r.status).toBe(201)`, and the control cell asserts `[status, typeof derived]`). Net: **no defect confirmed**; the real finding (1784-1) is one Spark missed. The first-attempt raw text (`raw_attempt1.txt`, invalid JSON) also flagged "hash2 does not assert the mint was called", which is false (`expect(mockMintCalls.length).toBe(1)` is in the cell).

---

## Merge-tree and the yaml (job 3)

All by `git merge-tree --write-tree --name-only` in my clone (SHA heads, develop = 2b7ef12fa564):

| merge | rc | result |
|---|---|---|
| develop + #1781 | 0 | clean |
| develop + #1777 / #1778 / #1783 / #1784 | 1 each | conflicts in **exactly the two Projects Documents html files**, nothing else (develop now carries #1775's block at the same insertion point) |
| #1781 vs any other PR, either order (4 pairs x 2) | 0 | clean |
| every pair among #1777, #1778, #1783, #1784, both orders (6 pairs x 2) | 1 | the same two html files only; **no code file and no yaml conflict**, and the #1778 vs #1784 output says `Auto-merging Blockchain/Dev/docs/openapi/secuura-api.yaml` with no conflict line |

**No two PRs share a code file** (pairwise intersection of non-doc, non-yaml files, 10 pairs, all 0; control, #1784 against itself, returns 3). The only shared non-doc file is `docs/openapi/secuura-api.yaml` (#1778 and #1784); #1778's two hunks are at lines 19093 and 19242, #1784's four at 27949 and after, disjoint.

**The yaml auto-merge, proven.** I made a commit from the merge-tree tree of #1778 + #1784 (docs conflict markers left in place; `scratchpad/scratch_merge_1778_1784.sha`) and ran `npm run check:openapi` on it: **rc 0, "CHECK PASS: on-disk YAML matches generated"**, spec examples 414 blocks OK. The merged yaml differs from #1778's head by exactly #1784's regenerated hunks and from #1784's head by exactly #1778's. Controls: `check:openapi` rc 0 on develop and on each of the two heads alone; rc 1 on #1778 with its source hunk reverted. So the two regenerations compose, in the order tested (a three-way from the common base); after one merges the second is a similar three-way, which I did not repeat.

I did not execute a five-way resolved merge or renumber the docs; the conflicts are the same "both appended before `</body>`" shape, resolved by keeping every block in merge order.

---

## What I did NOT test

- Any other service's suite, the four platform suites (Schemathesis, Akto, Playwright, Performance/k6), a running stack or gateway, any deploy, Node 24 (host has only v26.8.1), amd64 Postgres, PG versions other than 15.19, CI itself.
- #1777: real provider endpoints; a real 30 s read; the api-gateway key-validate fetch (not in the PR); `minting.service.ts` (finding 1777-3 is a grep).
- #1778: the published text through a running gateway; Linear point 4 (accepted by the ticket).
- #1781: a live run against the real npm registry (the stub stood in; the script's URL is not configurable); an advisory whose fix lies outside the manifest range; `npm run preflight` as a whole.
- #1783: any Node or Express other than this host's; the cell on a different default-header set.
- #1784: every document-creating route in originate other than the create, three version routes and certify; `MULTI_TENANCY_ENABLED=true` against a separate platform database (I used one database for both, as the PR says); the unit suites of `services/originate` as a whole (only the ks1537 pin and the ks1508 unit file).
- PR bodies (gh unauthenticated); doc accuracy beyond heading structure, insertion shape and the figures I re-measured; the doc html checkers named in earlier gate verdicts.
- The Spark gate's `*.integration.test.ts` result: by construction it has none (see 1784-H).

## Spark calibration rows (one per PR)

| PR | Spark verdict | This check | Defects Spark found that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1777 | NO GO (3 Major, 3 Minor, 1 Note) | GO WITH NOTES | 0 | 1777-3 (other unbounded fetches nearby) and the exact docs numbers; also none of the 9 mutant outcomes | **False NO GO.** Two Majors are disclosed scope facts, one is refuted (all 12 reds enumerated); it again escalated disclosed trade-offs to Major. |
| #1778 | GO WITH NOTES (6 Notes) | GO WITH NOTES | 0 | 1778-1 (the residual "accepts any valid token"); it said the new wording was "not verified" and did not verify it | **Right verdict, thin evidence.** Agreed on the outcome, but every Note is a generic caveat; the real residual needed the gateway read. |
| #1781 | NO GO (2 Major, 2 Minor, 1 Note) | GO WITH NOTES | 0 (Major 2, "no test", is true but is a scope fact and I carry it as 1781-1) | 1781-2 (repo-root mount, Info) | **False NO GO**, with one true premise. It had no measurement to work from (vacuous 0/0) and read the text instead of running the command; the command, when run, behaves as the text says. |
| #1783 | GO WITH NOTES (4 Notes) | GO WITH NOTES | 2 of 4 Notes confirmed (header-set brittleness, 500-path header leak) | N3d (Info) | **Right, and the best Spark read of the batch.** Note 2 became my confirmed plant N8c; the cost to confirm was one mutant. |
| #1784 | attempt 1 invalid (schema failure x2); retry NO GO (3 Major, 3 Minor, 2 Note) | GO WITH NOTES | 0 (Major 2 is a disclosed scope note) | **1784-1 (stale contract sentence at originate.openapi.ts:3717)**; the real-PG result it could not run | **False NO GO** on 154k tokens of prompt with the integration file unrun; one Minor is false (env restored in a `finally`), one Major refuted by a per-run random tenant. Spark had to be re-run once to get any valid output. |

Reading: five reviews, two GO WITH NOTES that agree with this check, three NO GO with zero confirmed defects; the NO GOs come on the three PRs whose real evidence is outside the harness (a script with no test, a DB-backed file, a body-stall test needing a real server). Pattern unchanged from gate 2: a Spark NO GO on a PR the harness cannot run is a prompt to run the mutant, not a defect signal. The two places Spark's text pointed at something real (1783 Note 2, 1781 Major 1's premise) were both disclosed or one-mutant cheap.

## Evidence locations
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate3-batch5/out/`: `p1777b`, `p1778b`, `p1778c`, `p1781b`, `p1783b`, `p1784b` (facts, diff, `spark/review.json`; `p1784b/spark_retry/`), `mut1777`, `mut1778`, `mut1783`, `it1784` (integration logs and json, mutants), `suite1777`. Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fcac9e76-d77f-49c4-82e2-80bb20ba8809/scratchpad/` (mutation drivers `mut*.py`, stub `stubfetch.mjs`, probe `probe1781.mjs`, merge-tree outputs `mt_*.txt`, `chk_*.txt`, pins). Container: `gate3-pg-1784` removed by exact name; `docker ps -a` read back: 0 containers matching gate3, port 55432 free.
