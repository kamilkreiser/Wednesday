## QA GATE - TIER 1, round 1: GO WITH NOTES

**PR:** Secuura/Distributed_Secuura #1819, "Refs KS-1836: bind GET /api/nft/certificates to the verified caller" (Seat A 18th)
**Head:** `817b40d9193bb78ef169ec5bf6d36582ac190589`. ls-remote showed the same SHA for refs/pull/1819/head and refs/heads/feature/ks-1836-nft-list-owner-bound, read at the start and again at the end.
**Develop:** `593cd90c3131f200f4adaf242c1a406a5b66fbb0`, the same at both reads.
**Gate:** QA gate 23. I report findings only. I fixed nothing, commented nowhere and pushed nothing.

**COUNTS:**
- Diff: 6 files, +566 / -9. Exactly the 6 files that were declared.
- Red-first: 17 of 24 route cells red on develop's handler, 7 controls green. This matches the author's claim.
- Author's cells at head: 31/31 green.
- nft-certificate suite: 13 files / 107 cells at head, 0 failed. Develop: 11 / 76, 0 failed.
- tsc: rc 0. eslint on the 4 changed TS files: rc 0. generate-openapi --check: PASS.
- My attack cells: 55/55 green at head.
- My replicas of the brief's mutants: 11 run. 10 killed. 1 was an equivalent mutant (my instrument error, see below), and its corrected form was killed.
- My own extra mutants: 10 run. 4 killed. 6 survived. None of the survivors is a cross-owner leak.
- Merge-tree of the head with 593cd90c: clean. Tree `16b6eaab086d93def4e8420c5629c180756f2c2a`, which equals the head's own tree.

---

### Findings, ranked (none blocks the merge)

**F1 (Low, observability). The foreign-selector log arm has no cell.**
- **Where:** `nft.routes.ts`, the condition `withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)`.
- **What survived:**
  - Ma: dropping the second disjunct survives the author's 31 cells and my 55.
  - Mb: changing `withheld > 0` to `>= 0`, so every call logs, also survives both sets.
- **When the arm matters:** only when the caller's fetched set is empty and `?userId` names someone else. For example, caller Z with no rows and `?userId=user-B`: my A-L2 shows that it logs `{"ownerId":"user-Z","userIdSelector":"user-B","returned":0,"withheld":0}`.
- **Why it is not a security issue:** no response bytes change. The brief's A.3 log contract is therefore half pinned.
- **Reproduce:** `python3 -I mutants.py <clone>` (rows Ma and Mb), from this folder.

**F2 (Low, consistency). The row-owner trim is asymmetric between the two read paths.**
- **What happens:**
  - `selectReadableCertificates` compares `cert.userId.trim()` with the owner.
  - `getUserNFTCertificates(ownerId)` matches `cert.userId === userId` exactly, both in memory and in SQL.
  - So a row stamped `'user-A '` is returned to user-A on the `?walletAddress` path but not on the bare list. Attack cell A-M2 logged `padded-row/null-row -> ["n2"]`.
- **What does not happen:** the trim never lets a different owner through. It only matters for rows whose trimmed owner equals the caller.
- **Mutant:** Mc (drop the trim) survives every cell. No fixture has a padded owner.
- **Reachability:** no write path stamps a padded owner today; every row is `'user-id'`.

**F3 (Info). The wallet reader still receives attacker-controlled strings.**
- **What I saw:** `getWalletNFTCertificates` is called with the raw `?walletAddress` string, for example `" "`, `"%"` and `" addr_..."` (A-Q log lines).
- **No injection:** the query is parameterised equality (`wallet_address = $1`), not LIKE.
- **Side effects:**
  - The foreign wallet's rows are read and cached into `memNftCertificates`, which `loadFromDb` already fills at boot anyway.
  - In-process timing difference, a median of 15 calls:
    - foreign wallet with 0 rows: 1.59 ms;
    - foreign wallet with 2000 rows: 1.91 ms.
  - That is a weak size oracle at best. I measured it over loopback in-process, not over a network.
- **What would remove both:** querying by `ownerId` and narrowing by wallet in memory. That is a design choice, not a defect.
- The userId selector never reaches a service method. Every A-Q cell shows the user reader called only with `["user-A"]`.

**F4 (Info). The token owner is trimmed by design.**
- A token with `userId: ' user-A '` reads user-A's rows (G1, and my A-T padded cell).
- Tokens are RS256-signed by auth with `user.id`, so a caller cannot choose this value.

**F5 (Info, docs).**
- Section 118.2 says the figures were measured at develop `7152ac669d2d` with vitest 4.1.12.
- My rerun at the merged head `817b40d9` with vitest 4.1.10 reproduces every count it states: 17/24, 31/31, 107 and 76.

**Candidates (expected, not findings of this PR):**
- **(iv-a)** `GET /api/nft/certificates/:id` still serves another owner's row. C2 pins it (b1 is served to caller A with `userId: 'user-B'`), and it is green at head.
- **(iv-b)** `GET /api/nft/ipfs/:cid/encrypted` is ungated. It is named in the PR's known gaps, and I did not exercise it.
- **(vii)** Connector tokens minted without a connector id share `connector:api-key` as their owner. A-G1 shows such a token gets a 200, not a 403. This becomes live only once a mint records the caller.

---

### TESTED / NOT TESTED / HOW

**TESTED: scope**
- **Diff scope.** I ran the `diff --stat` and `--name-only` three-dot diff of origin/develop...pr/1819. It shows exactly 6 files:
  - nftReadGate.ts (new);
  - nft.routes.ts;
  - the two new ks1836 test files;
  - the two Projects Documents html files (section 118).
- **The nft.routes.ts hunks** are two:
  - `@@ -8,6 +8,7` adds the import;
  - `@@ -223,15 +224,27` sits inside `router.get('/certificates', ...)` only.
  - No other handler changed. The suite has 107 green cells, and C2/C3 pin `:id` and `/tiers`.

**TESTED: red-first**
- I put `git show origin/develop:.../nft.routes.ts` in place, with the head's tests and gate module kept.
- Result: 17 failed / 7 passed (24).
- Red: R1, R2, R4, R5, R6, R8 through R18, and R20.
- Green: R3, R7, R19 and C1 through C4.
- I restored the file with `git checkout`, and its sha256 matched the hash taken before the swap.

**TESTED: bypasses (my attack file `zz-gate23-attack.test.ts`, which runs the author's harness: the real router, the real minting service, a fake table and the real in-memory Map)**

Query arrays and objects. Each gave a 200 with an empty body, and the service never saw a non-string:
- `userId[]=user-B`
- `userId[]=user-A`
- `userId=user-B&userId=user-A`
- `walletAddress[a]=..`

Prototype keys. Each gave a 200, empty, with only the user reader called, with `user-A`:
- `userId=__proto__`
- `userId=constructor`
- `userId[__proto__]=`
- `userId[toString]=`
- `walletAddress[__proto__]=`

userId case and whitespace selector variants, each a 200 with no foreign row:
- `USER-B`
- `%20user-B%20`
- `user-id`
- `%20user-A`

walletAddress combined with userId:
- `W_B & user-B`
- `W_LEGACY & user-id`
- `W_LEGACY`

Each gave a 200 with no foreign or legacy row, and no `user-B`, foreign key or `'user-id'` in the body.

Empty, blank and odd wallet values:
- `walletAddress=%20` (a single space)
- `%25` (a SQL wildcard)
- a padded W_B

Each gave a 200 with an empty body.

Tokens that get a 403 with no service method called:
- `User-Id`
- `\tuser-id\n`
- ` user-id`
- `﻿user-id`
- the numbers 0 and 1, `null`, `true`, `['user-A']`, `{toString:..}` and `''`
- no userId but `sub` or `id` present
- an own `__proto__` property carrying a userId
- `req.user` as a string, an array or a number

Unicode lookalikes of `'user-id'`:
- U+2010, U+2011, U+2212
- fullwidth, Cyrillic е, dotless ı
- ZWSP, ZWJ, a combining dot
- `USER-İD` and `user_id`

These are accepted as ordinary owners, a 200 not a 403. Each still received EMPTY_BODY on the bare list, `?walletAddress=W_LEGACY`, `?userId=user-id` and `?userId=<itself>`. The row match is exact, so no lookalike reaches a `'user-id'` row.

Memory-only rows. I seeded a foreign row (user-B), a legacy row (`'user-id'`) and an own row (user-A) via `loadFromDb`, then emptied the table:
- Four foreign or legacy selector combinations each gave EMPTY_BODY.
- The own wallet and the bare list each returned only m3.
- No `user-B`, `ENC-LEG`, foreign key or `"user-id"` appeared in any body.

**TESTED: leaks**
- **Count and ordering:** foreign wallets holding 0, 1 and 50 rows gave byte-identical bodies and statuses.
- **Error body:** a planted wallet-path fault gave a generic 500 body with no wallet, owner or key.
- **Log lines:** they carry the caller's ownerId, the caller-supplied selector and returned/withheld counts. They carry no foreign owner id and no encryptedKey of any row.
- **Timing:** see F3.

**TESTED: whether a legitimate caller can hit the 403**
- I read the shared `authenticate()` in `packages/shared/src/middleware/index.ts`. It attaches the verified payload as-is.
- Every minter sets `userId` as a non-empty string:
  - auth `services/jwt.ts`: access and refresh tokens use `user.id`; connector tokens use `connector:<id|api-key>`;
  - `shared/security/token-rotation.ts`: `payload.userId`.
- A-G1 (a connector-style id) gave a 200, and A-G2 (a real uuid owner) reads its row.
- No legitimate caller in the repo reaches the 403. The only route callers are the e2e fixture `recruitment-data.ts:333`, which is defined but never used by a spec, and the spec and gateway catalogue.

**TESTED: service input**
- The user reader is only ever called with the verified ownerId.
- The wallet reader is called with the raw string selector (F3), and never with an array or object (R18, and my A-Q cells).

**TESTED: mutants (one at a time; anchor count 1; tsc noted; sha256 restore asserted)**

Brief replicas:
| Mutant | Result |
|---|---|
| m1 drop the filter | KILLED, 9 author cells |
| m2 owner from ?userId | KILLED, 4 |
| m3 wallet branch skips the filter | KILLED, 7 |
| m4b widen: owner OR the userId selector, third conjunct dropped | KILLED, 5 |
| m5 drop the sentinel conjunct | KILLED, 3 |
| m6 drop the blank conjunct | KILLED, 2 |
| m7 memory rows skip the filter | KILLED, 1 |
| m9 403 on a foreign selector | KILLED, 6 |
| m10 count of the unfiltered list | KILLED, 7 |
| m11 owner from tenantId | KILLED, 11 |

My extras:
| Mutant | Result |
|---|---|
| Me untrimmed owner | KILLED by G1 |
| Mg case-insensitive userId selector | KILLED |
| Mh wallet path on any truthy type | KILLED; also a tsc error |
| Mi sentinel compared before trim | KILLED |
| Mj 403 body echoes the claimed id | KILLED, 4 |
| Ma, Mb (log arm) | SURVIVED, F1 |
| Mc row trim | SURVIVED, F2 |
| Md drop the row non-string guard | SURVIVED. Near-equivalent: `user_id TEXT NOT NULL` (`04-sprint2-service-tables.sql:687`). A null owner would make the list return 500 (fail-closed), not leak. |
| Mf trimmed wallet compare | SURVIVED. It only alters narrowing within the caller's own rows. |

**TESTED: the rest**
- **Suite:** `vitest run --root services/nft-certificate` gave 13/107 green at head and 11/76 green at 593cd90c.
- **tsc:** `tsc --noEmit -p services/nft-certificate/tsconfig.json` gave rc 0. The tsconfig excludes `src/__tests__`.
- **eslint:** on the 4 TS files, rc 0, using `Blockchain/Dev/eslint.config.mjs`.
- **openapi:** `tsx scripts/generate-openapi.ts --check` gave CHECK PASS. `nft-certificate.openapi.ts` is not in the diff, and the 403 is already declared for this route (`:933`).
- **Merge:** `merge-tree --write-tree 817b40d9 593cd90c` gave `16b6eaab…`, clean.
- **Docs:** section 118 states the known gaps, the red set (R1, R2, R4 through R6, R8 through R18, R20, the same as mine) and the UNMEASURED platform suites. I saw no secrets.

**NOT TESTED**
- **The real `app.ts` stack.** The harness mounts the router with a test middleware, without `jwtAuthenticate` or `rejectControlBytes`. I sent no real RS256 token. The query parser is real Express (qs).
- **Real Postgres.** Only the fake table ran.
- **The by-id and ipfs routes,** beyond C2.
- **The four platform suites** (Schemathesis, Akto, Playwright, k6), Node 24, any box or deploy.
- **`npm run check:spec-examples`.**
- **The test-types ratchet,** or tsc with the test files in the program.
- **Not re-run individually: the author's own 17 mutants.** I replicated the brief's m-list myself instead (above). m8 is covered by R13 and G4.

**HOW**
- **The clone.** I made a `git clone --shared` of the Secuura checkout at the then-non-existent path `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/52e2783b-09e1-49d1-9200-c6e9ede3ba54/scratchpad/gate23/clone`.
  - Its toplevel was asserted equal to that path.
  - Its origin was set to `git@github.com:Secuura/Distributed_Secuura.git`.
  - Its `core.sshCommand` was copied from the shared checkout.
  - It fetched develop and `refs/pull/1819/head` only.
- **node_modules** were symlinked from the shared checkout into the clone; they were untracked and never added. TMPDIR was `/tmp/g23`.
- **Artefacts in this folder:**
  - the attack file;
  - `mutants.py`, `mutants_brief.py` and `mutants_b.py`;
  - `attack_run.log`;
  - `spark_facts.json`.

**spark_gate.sh**
- **Invocation:** I ran it with the bare `develop` base ref and `--node-modules <pkg node_modules>`.
- **What worked:**
  - It asserted the head as the tip: `817b40d9`, merge-base `593cd90c`, base tip `593cd90c`.
  - It reported the diff as 6 files, +566 / -9.
- **Where it failed:** both targeted runs reported `files_failed 2, passed 0, failed 0`, because the log shows `sh: vitest: command not found`.
- **Why:** this package's vitest is hoisted into `Blockchain/Dev/node_modules`. `--node-modules` links only the package-level directory into the head worktree.
- **What it means:** the tool's run half does not apply to this monorepo layout as invoked. Its counts are NOT evidence. All counts above come from my own runs.

### Instrument errors of my own
1. **m4 was equivalent.** My first m4 changed only the owner term to `owner OR selector`, and it survived. The third conjunct (`selectors.userId !== ownerId -> false`) still closed it, so the mutant was equivalent. I corrected it to m4b (both terms changed), and m4b was killed.
2. **My first m9 anchor matched 14 times,** so the script refused it. I re-anchored it to a unique multi-line string, and it was killed.
3. **Two cells of mine were too weak to kill Md.**
   - A-M2 asserted only "n1 not in ids", so a 500 also passed it.
   - A-L3's 500-log observation (the planted error message reached `logger.error`) shows only that the catch logs `error.message`. That logging is unchanged by this PR, and the error text was planted by me, so it is not a finding.
4. **The first verbose run printed no console lines** (non-verbose reporter). I re-ran with `--reporter=verbose --silent=false`; that is `attack_run.log`.
5. **Resolution caveat.** `@secuura/shared` resolved through the symlinked root node_modules to the shared checkout's `packages/shared/dist`, built 2026-10-12. packages/shared is unchanged by this PR, but the openapi and route-harness runs used that build rather than a fresh build at 817b40d9.

### FIX-BEFORE-MERGE
(none)

Optional follow-ups for the author or a later card. None blocks the merge.
- A cell pinning the foreign-`?userId` log line when the caller has zero rows (F1).
- A decision on whether to keep the row-owner trim, or match the service's exact compare (F2).
