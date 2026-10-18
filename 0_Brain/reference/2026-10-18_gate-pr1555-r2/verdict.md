VERDICT: PR #1555 (KS-1114) head 986732cf5f70de4417a76b3d2100a57bc8fe0d04: GO WITH NOTE (round 2 of 2, the cap). F1 and F2 are closed, as measured. No finding below blocks. The notes are residuals for a card, not fixes for this PR.
SHA256/16: bea8745916286da7

# Gate: PR #1555, KS-1114 anonymous title lookup in one tenant, ROUND 2 (Opus tier 1, FULL)

Commissioned by Wednesday, 2026-10-18. This gate reports findings only and fixed nothing. All work ran in `/private/tmp/claude-501/gate1555r2-1792314908/`: my own `--shared` clone (origin set to `git@github.com:Secuura/Distributed_Secuura.git`, fetched with the checkout's sshCommand plus `ServerAliveInterval=30`) and my own Postgres 18 on port 55841. In `!CODING` I used only `ls-remote`. I ran no Docker, pushed nothing, made no GitHub or Linear writes and deleted nothing. Evidence: `evidence/scripts/` (every script I ran) and `evidence/runs/` (raw outputs). Round 1's attack set is the base, with round-2 attacks added (`R01`-`R25`, `X1`-`X8`).

## Heads (re-read by me, 09:36Z)
- `refs/pull/1555/head` = `986732cf5f70de4417a76b3d2100a57bc8fe0d04`, which matches the brief. It is a fast-forward of round 1's `c85cc28d`.
- Live develop = `d2ec786e6130c7ce13384185c84cc1e7566d77cb`, which is the base and the merge-base. Develop has not moved, and #1565 and #1566 have not landed (`runs/merge.txt`).
- Both merge commits are clean merges. `7c32b44f1` and `986732cf5` each have a tree equal to the automatic `merge-tree` of their parents, so neither carries an extra edit (`runs/` via `scripts/hunks.sh`).

## Severity summary
| # | Sev | What | Where |
|---|---|---|---|
| F1 | **CLOSED** | A title hit now answers exactly `{"verified":false,"checks":{"documentExists":true}}` (51 bytes). The query selects only `1 AS found`. The reply has no id, hash, title, issuer, status, certification, lineage, newerVersions, warning or strategy. Nothing in it leads to `contentHash`, so there is no chain to `verified:true`. | `services/originate/src/routes/verification.ts:1460-1470` |
| F2 | **CLOSED** | Draft and revoked are excluded in the WHERE (`AND d.status NOT IN ('draft','revoked')`). `status` is `NOT NULL` (measured), so `NOT IN` cannot drop a NULL row. A newer draft or a newer revoked row does not shadow an older published one. M3 (status checked on the newest row only) is killed by T4b and T4c only. | `verification.ts:1466` |
| N1 | LOW (residual, card) | The hidden set is an exact, case-sensitive deny-list. Measured as hits: `deleted` (pinned on purpose by T11), `expired`, and the case variants `REVOKED`, `Draft` and `revoked ` (with a trailing space). **No writer** of `deleted`, `expired` or any case variant into `documents.status` exists in originate today. The only `status='deleted'` writer is `users` (`gdprService.ts:839`). But `certificationRepo.toDbStatus` maps `expired` to `'expired'` (`certificationRepo.ts:113`), and the author's status census omits it. My mutant G3 (`lower(btrim(status)) NOT IN`) **survives**: no cell pins case behaviour. The by-id strategy has the same exact-match semantics (`status === 'revoked'`, `verification.ts:1027`), so the two strategies agree. | `verification.ts:1466`; test T11 at `ks1114-…integration.test.ts:272` |
| N2 | INFO (inherent) | The existence bit itself, which is Kam's ruling (b). Hit and miss differ only in the body (`Content-Length` 51 vs 141, and the weak `ETag`). Timing between hit and miss is indistinguishable on my data (below). | `verification.ts:1470` vs `:1449-1453` |
| N3 | INFO | The erasure sentinel returns before the query, so it answers about 0.35 ms faster (p≈1e-127). This depends only on the input, not on stored data, and is unchanged from round 1. | `verification.ts:1458` |
| N4 | INFO | `respondExistenceOnly` keeps its name but is now only the by-id body, which carries the hash. The comment at `:1014-1022` says so. The name is a misnomer and harmless. | `verification.ts:1023` |
| F3 | CLOSED (text) | The spec now names the 400 `Missing tenant context` under `MULTI_TENANCY_ENABLED` in production. Measured: MT-prod gives 400 on every unvouched probe (64 of 64). | `originate.openapi.ts:555-562` |
| F4 | CLOSED (named) | T9 now asserts its two preconditions by name. Measured: under Sydney TZ it goes red as `precondition: app DB session TimeZone … Australia/Sydney`, and with my colliding seed hash it goes red as `precondition: no foreign row shares a fixed hash` (row `15550000-…00a1`). It is still not hermetic, but it is honest. | `ks1114-…integration.test.ts:331-343`; `runs/ks1114_h_sydney_false_app.log`, `runs/ks1114_h_collide.log` |
| F5 | ACCEPTED | The dead guard is kept, with a comment that says it is unreachable. Mutant A9a/o3 class still survives. | `verification.ts:1455-1458` |
| F8 | INFO (pre-existing, carried) | A vouched upper-case `x-tenant-id` misses under `secuura_app` (RLS GUC raw vs predicate lower-cased) but hits under superuser. That is the only difference between superuser and app in 72 probes. It fails closed under the app role. | probe P16b |

**What would block:** nothing here. N1 is a ruling question (should `deleted`, `expired` or a case variant hide?), and it is already being carded to Kam. Under the two-NO-GO cap it is ticketed residue, not a third round.

## FOUND / TESTED / HOW

**1. Hunks (r1 head to r2 head, with the merges excluded).** I diffed `merge-tree(c85cc28d, d2ec786e)` against the head (`runs/r1_to_r2_owndiff.patch`). It touches 5 files and nothing else:
- verification.ts:
  - comments;
  - the title SELECT is now `SELECT 1 AS found`, with no JOIN, no ORDER BY and an added `status NOT IN ('draft','revoked')`;
  - a hit returns the fixed two-key body instead of `respondExistenceOnly(...)`.
- originate.openapi.ts: `KS1114_TITLE_SEMANTICS` and the route description now state the exact hit body, the draft/revoked exclusion and the MT-prod 400. "newest first" is removed.
- yaml: generated.
- spec test S1/S2: new must-strings; `newest first` must be absent.
- integration test:
  - HIT_BODY/MISS_BODY are byte pins;
  - new cells T1b, T4b, T4c, T10, T10b, T11;
  - T4 is re-pinned;
  - T9 preconditions are added.
- Lint commit a83499eb3: one line, `let json: any;`.

**yaml:** I regenerated it in place with `generate-openapi`. Diff 0 lines; blob `77e7d4b0…` equals HEAD's. `--check` PASS, `check-spec-examples` OK. **Control:** a planted word in `KS1114_TITLE_SEMANTICS` gives `CHECK FAIL` rc=1, and the worktree was clean after restore (`runs/oapi.txt`).

**Hit body against the declared 200 schema:** ajv against the generated `VerifyResponse` (required `["verified"]`, checks `.partial()`) gives HIT VALID and MISS VALID. **Controls:** without `verified` it is INVALID (required), and with `documentExists:"yes"` it is INVALID (boolean) (`runs/schemacheck.txt`). Wednesday's reading holds: `verified` is required, and the shape conforms.

**2. Attack set through the real route.** I booted the real originate app (`src/index.ts` via tsx, real provenance middleware, vouch secret set) in seven instances against Postgres 55841. The DB has the schema from `docker/init` plus `migrations`, `secuura_app` NOBYPASSRLS, `documents` under FORCE RLS, and TimeZone UTC. The instances:
- head: ST/app, ST/super, MT-dev/app, MT-dev/super and MT-prod/app;
- develop: ST/app;
- r1: ST/app.

Each ran 72 probes. Every body is in `runs/probe_<instance>.json` and `.txt`, and the comparisons are in `runs/cmp.txt`.
- **Hits (27, all exactly the 51-byte HIT body):**
  - P01 default-tenant hit;
  - exact `%_` and quote/backslash titles;
  - 500-char title;
  - NFC title;
  - `{contentHash:""}` / `{documentId:""}` / `{providedHash:""}` + title;
  - P14 shared title;
  - P16/P16e vouched tenant B;
  - R01-R05 (pending_signature, signed, anchored, anchor_failed, certified);
  - R06 deleted, R07 expired, and R08-R10 case variants (N1);
  - R11/R12 an older certified row under a newer draft / newer revoked row (F2 closed);
  - R14 `created_at` NULL;
  - R18-R20: `Accept: text/html`, `requestedFields:[contentHash,issuer,lineage]` and `includeLineage/verbose` all add nothing;
  - X6 trailing slash; X7 duplicate key.
- **Misses (29, one body, byte-identical, sha256/16 `cebed88e6b6b4417`):**
  - absent; title only in tenant B; erasure sentinel `[erased]`, `[erased] `, `[ERASED]`;
  - `%`, `100% off__`, a bare `%`, two SQL injections;
  - 501 chars and 100k chars (X8 1 MB also); NFD;
  - P13 draft, P13b revoked, R13 a title held only by a draft and a revoked row;
  - R15 vouched-B draft, R16 vouched-B on a default-tenant draft, R17 anonymous on a B draft;
  - all forged-tenant variants P15-P15g; P16b-d.

  The measured miss set equals the expected set exactly. The miss body is byte-identical to round 1's (`r1_st_app` P02/P03/P04 identical). Develop answers every title-only request with 400 (it has no title strategy), so "unchanged" means unchanged against round 1.
- **400s:** empty, whitespace, `\t\n` and NBSP titles get 400 naming title. A NUL gets 400 VALIDATION_ERROR. A non-string, an array, `{toString}` or `documentHash:null` gets 400 type error. `?title=` in the query gets 400. A lone surrogate (X3/X4) is a miss, not an error.
- **Precedence:** documentId+title takes the documentId strategy (its full by-id body, unchanged from develop). Unknown documentId+title gives the documentId not-found, with no fall-through. Hash+title, unknown hash+title, documentData+title and `hash:"sha256:"`+title all take the hash strategy. The 11 non-title probes are byte-identical to develop.
- **Modes and roles:**
  - head ST/app = MT-dev/app on 72/72;
  - ST/super and MT/super differ from app only at P16b (F8);
  - MT-prod: 64/72 differ, and all 64 are 400 `Missing tenant context` (every request that is not vouched and is not refused for a NUL). This is the control that the comparator sees differences. The 7 vouched probes and the NUL 400 answer as in ST.
- **v2:** `/api/v2/verification/verify` with a title gives 400 on both head and develop, so the PR does not touch it.

**3. F1/F2 closure.** F1: the hit body carries no field from which a hash, id or lineage can be read. T1 pins the 51 bytes, T1b pins absent keys plus no row value in the text, and my probes confirm it. The round-1 escalation chain (title → contentHash → `{hash}` → `verified:true`) has no first step. F2: the filter is in the WHERE (`:1466`). R11/R12 hit through a newer draft or revoked row. Mutant A4 (M3, my re-implementation: `SELECT d.status … ORDER BY created_at DESC LIMIT 1`, then a JS status check) is **KILLED by T4b and T4c only**, which confirms the author's claim.

**4. Leaks beyond existence.**
- **Headers:** helmet/CORS identical. Hit vs miss differ only in `Content-Length` and the weak `ETag`, both of which are functions of the body. One header set across all 29 misses and one across all 27 hits.
- **Error bodies:** the type, NUL, JSON and empty-title 400s are input-only. The DB-error path (`'Verification lookup failed'`) was not reachable from any title I sent.
- **Timing** (`runs/timing_h_st_app_summary.json`, `runs/timing_h_mt_app_summary.json`): 400 interleaved samples per class after 20 warm-ups, shuffled.

  | Mode | Comparison | Result |
  |---|---|---|
  | ST | absent vs hit | medians 0.532 / 0.528 ms, p=0.49 |
  | ST | absent vs otherTenant | p=0.83 |
  | ST | absent vs draft | p=0.54 |
  | ST | absent vs revoked | p=0.14 |
  | ST | draft vs revoked | p=0.043 (one of 8 pairs tested; not seen in MT, p=0.96, so read as chance) |
  | MT | absent vs hit | p=0.99 |
  | MT | absent vs otherTenant | p=0.09 |
  | MT | absent vs draft | p=0.99 |
  | MT | absent vs revoked | p=0.98 |
  | both | sentinel | about 0.17 ms vs about 0.53 ms, p≈1e-127 (N3; control that fires) |

  Round 1's 2.0 ms hit (the lineage queries) is gone. The difference is inherent at scale: there is no title index (measured), so a hit can stop at LIMIT 1 while a miss scans the tenant. That was not measured on a large table.
- **`deleted` residual:** it is a leak only if legacy rows with `status='deleted'` exist in a tenant. No code writes one today, so the card is worth one prod census query (count by status per tenant). If the count is zero, close it. Fold `expired` and case variants into the same card (N1).

**5. Mutants at head** (`runs/mutants.txt`, worktree `m`, ks1114 17 cells). The clean baseline is 17/17 under both app and super, and the worktree was clean after the run.
- KILLED:

  | Mutant | Killed by |
  |---|---|
  | A1 tenant predicate removed as superuser | T2, T3, T10 |
  | A3 caller tenant hard-coded DEFAULT | T2b |
  | A4 [M3] | T4b, T4c only |
  | A5 status filter removed | T10, T11 |
  | A6 only draft excluded | T10, T11 |
  | A7 only revoked excluded | T10, T11 |
  | A8 case-insensitive title | T5 |
  | A9′ both sentinel lines removed (compile-valid) | T6 |
  | A10 miss echoes the title | T2, T6, T10, T11 |
  | A11 whitespace treated as present | T7 |
  | A12 round-1 full body on a hit | 8 cells |
  | A13 `strategy:"title"` added | 8 cells |
  | A14 KS-1032 gate removed | T3 |

- **SURVIVED as predicted:**
  - A2/A2b [M9b], the tenant predicate removed as `secuura_app`, in both MT=false and MT=true;
  - A9a and A9b, each sentinel line alone (defence in depth: the pair is pinned by A9′).
- **A9 as written** (`ERASED_MARKER` left unused) is a compile break that turns all 17 cells red. It is not scored, the same as round 1's m6c.
- **My own:**
  - G1 `deleted` also hidden: KILLED by T11, so the residual is pinned.
  - G2 allow-list `IN ('certified')`: KILLED by T11.
  - G4 hit adds `hashValid:false`: KILLED by 8 cells.
  - G5 hit returns 404 with the same body: KILLED by T1.
  - **G3 case/space-insensitive status: SURVIVES** (N1).
- Comment-only control: SURVIVES (0 red).
- **"M9b survives by design" is honest.** It survives only under `secuura_app` with FORCE RLS: the policy restricts rows to `app.current_tenant_id`. The only bypass (`tenant_scope_bypass='platform_admin'`) is set by `runWithPlatformScope`, which appears only in `adminConfig.ts`, never on the verify route. The superuser control A1 kills it. Caveat: that production originate connects as a NOBYPASSRLS role was not measured by me.
- Author's count "9/9 killable killed" cannot be checked row for row. The author's mutant table was not readable (gh has no auth in that config dir). My re-implementations of the named ones (M3, M9b) behave as claimed.

**6. Author's claims, checked.**
- Verify matrix ks1114+ks1119+ks1557 × MT false/true × super/app (`runs/verifymatrix.txt`): head 52 cells, develop 35, r1 47. Red sets are **identical** to develop's in all four combinations:
  - MT=false/super: 5 ks1119 + 1 ks1557 red;
  - MT=true/app: 1 ks1557 red;
  - the other two combinations: 0 red.

  MT engagement confirmed (TenantPoolManager init in the MT logs). Reproduced.
- Red-first: head's ks1114 cells on r1's source give **9 red / 8 green ×4** (T1, T1b, T2b, T4, T4b, T4c, T10, T10b, T11). r1 worktree restored, diff empty (`runs/redfirst.txt`). Reproduced.
- Originate unit: **110/110 suites, 1376/1376 tests**. Reproduced.
- `check:openapi` PASS. Reproduced.
- tsc: product config 0 errors. A test-inclusive scratch config (`wt/tsconfig.gate-tests.json`, which includes `src/__tests__`, both ks1114 files listed) also gives 0 errors. Reproduced.
- Status census: `VARCHAR(20) NOT NULL DEFAULT 'draft'`, no CHECK, measured. The census omits `expired` (N1).

**7. Merge prediction** (`runs/merge.txt`).
- Live develop is `d2ec786e`, the merge-base. `merge-tree` is clean, and the merged tree `c215bfde…` equals the PR head tree, so this is a fast-forward-equivalent merge. Overlap 0: develop has no commits since the base.
- **Cross-lane:**
  - #1565 (`47ca5621`, 1 file `systemTest/akto/src/scan/credentialLiveness.ts`) and #1566 (`36970138`, 2 files in `services/mcp-server`) share no file with #1555, and neither touches the yaml, an openapi source or `routes/verification.ts`.
  - #1555 onto develop+#1565 merges clean (tree `e4ecf401…`), and onto develop+#1566 merges clean (tree `e1c3eaa3…`). Merge order does not matter.
- **Planted control:** a develop-side edit of the `req.body` destructuring line in verification.ts gives `CONFLICT (content)` with rc=1.

## NOT tested
- **Preflight legs 3, 4 and 8** (skipped in-hook, Docker down) and **leg 6** (`npm audit` errored in-hook). Brief rule: I ran no Docker. I did not re-run `npm run audit:gate`; the author's rc 0 is unverified by me. The preflight stands at 12/16, INCOMPLETE, as carried.
- The api-gateway path: no gateway was booted, so the gateway strip and the per-IP limiter were read from source only, as in round 1.
- Timing on a large tenant, with a title index, or with network jitter.
- Production data for N1: whether any `deleted`, `expired` or case-variant document rows exist.
- That production originate connects as a NOBYPASSRLS role (the premise of M9b).
- The author's own mutant table, row by row (not readable).
- The full originate integration suite (only the three verify suites were run).
- No Docker and no remote box.
