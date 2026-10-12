# Gate verdict: Secuura Platform K PR #1529 round 2 (KS-1556, P2): memory only after COMMIT, per-connector chain, no undo

**VERDICT: GO WITH NOTE.** Majors: 0. Minors: 1 (m1, a test gap; no product defect). Observations: 6.
**Report sha256/16:** `b662a71501b66490`. This is the sha256 of this file with this field set to the literal `SHA16_PLACEHOLDER`, truncated to 16 hex characters.

The new shape does what it claims, and I reproduced the author's red/green with my own instruments.

- **Round-1 n1 is gone by construction.** I measured it in 16 interleavings × 3 runs, each with a proof that the race landed. In every one, the revoke held in memory, in `GET /api/keys` and in validate.
- **Round-1 n2 is closed.** G3 is killed by the author's cross-process grace cell. G4 has no target any more, because there is no undo; its analogue, an early grace expiry, is killed.
- **Nothing on the rotate path writes shared memory before its COMMIT.**
- **The chain's bounded wait can lose memory ordering, but only if something delays the post-COMMIT apply.** That apply runs synchronously after the COMMIT reply. When I forced a delay with a widening probe, the result was cosmetic: memory and the list were wrong, but validate still refused the retired key.
- **The one Minor is a test gap.** Three of the chain's and apply's own guards survive every cell the PR ships (M7, M10, M3b), and a fourth (M1) is caught only by an implementation-string assertion. The consequences are availability or cosmetic only, never credential validity.

## Head and trees under test
- **Head:** `d19b7a708e5bbc308da33384267a24637fa9f39c`.
  - `git ls-remote origin refs/pull/1529/head` from my own scratch clone equals the brief.
  - develop = `b28bfaecf24e4671440b9345289bfc368639bd11`, which also equals the brief. `merge-base --is-ancestor develop head` gives rc 0.
- **The author's bundle file:** `ks1556-round2-d19b7a708e5b.bundle`, sha256/16 **`76c873e4ae861ccb`**. This matches their claim. I hashed it, but did not use it: I fetched from GitHub read-only.
- **How I got the code:**
  - `git clone --shared` of the project checkout into my scratchpad, push URL disabled.
  - The fetch used the project's deploy-key `core.sshCommand`, into `refs/gate/*` in my clone only.
  - Nothing was written to the project folder, nothing was pushed, and there were no GitHub or Linear writes and no remote boxes.
- **Scope:**
  - `git diff --stat develop..head` gives **exactly 4 files, +745/-27**: `index.ts`, the KS-1549 integration file, the m2 file and the new `ks1556-connector-chain.test.ts`.
  - Against the old head `c3b66f7f`, the diff is 13 files. The other 9 are develop's `scripts/` files, brought in by the merge.
  - `git diff af612ae6 d19b7a70 -- services/security` is empty, so the merge changed none of the PR's files.
  - **Overlap with develop:** since the merge-base `af2366e7`, develop changed 9 files. Their overlap with the PR's 4 files is **0**. Control: the PR's file list compared with itself gives 4.
- **The trees I ran:**
  - `head`.
  - `dev` (develop, with the PR's three test files and my harness copied in).
  - `oldhead` (the head tree with only `index.ts` swapped for the `c3b66f7f` blob).
  - `mut` (a separate head worktree for mutants).
  - Each tree had its own `npm ci --ignore-scripts` and its own `packages/shared` build.
- **Database:** my own PostgreSQL 15 on 127.0.0.1:**55422**, with the unix socket off.
  - Built with `initdb -U secuura --auth=trust`, then `docker/init/*` in order.
  - The dblink step failed again (as in round 1), so I created `secuura_platform` by hand.
  - `run-migrations.sh` gave **applied=50 failed=0** (`_secuura_migrations` = 50).
  - `svc_api_keys` has `relrowsecurity=t`, `relforcerowsecurity=t`. `secuura_app` has `rolsuper=f`, `rolbypassrls=f`, and the service ran as `secuura_app`.
  - At the end, I confirmed 0 leftover gate triggers and 0 gate rows, then ran `pg_ctl stop`. 0 listeners remained on 55422 and no gate processes were left.
  - A scan of `evidence/` for the throwaway app password found 0 hits. Positive control: the same scan on `pg.env` found 1.

## The known false red: round-1 harness `A1_replaced` (VERIFIED, not counted, not hidden)
- **Harness:** the round-1 harness ran verbatim at the head. Its source sha256/16 is `274d755084258bbc`, which matches the brief.
- **Result:** 11 of 12 cells pass. **`A1_replaced` FAILS** (`evidence/r1harness_head_rc_1.txt`, `gate1529_r1harness_head_rc.json`).
- **The cell's own JSON, at +300, +800 and +1500 ms:**
  - The only failing line in every trial is the instrument: `mid: true`, where the old cell requires `'Key revoked'`.
  - Every product assertion holds in **3/3** trials: status 500, `key: null`, `dbActive: true`, `memActive: true`, and `post: [true, true, true]`.
  - Count: **0 of 3 trials fail a product assertion, and 3 of 3 fail only the instrument.** This confirms the author's claim from the evidence, not on trust.
- **What I replaced it with:** my cell `A1_pending` reads a settled flag at the instant the validate is issued. It also asserts that the mid-window validate answers `true` (the new shape's correct answer). It runs at grace 0 and 60, at three offsets.
- **Results:**
  - Head: 6/6 trials pending at issue, 0/6 product failures, in 3 RC runs and under RR and SER.
  - Develop: 3/6 product failures, all at grace 0 (mid `Key revoked`, then post-validates `false`), under RC, RR and SER. The instrument can fail independently.
  - The JSON also shows `settledWhenMidReturned: true` in 6/6 trials. The validate's usage write blocks on the rotate's row lock. This matches the author's reason for reading the flag at issue time.

## Numbers (instrument / control)

| # | What | Head | Develop / old head | Instrument | Independent control |
|---|---|---|---|---|---|
| 1 | Author's integration cells (KS-1549 file incl. E9 g0/g60 pairs, n1 A3/A3b and their no-rotate controls, crash, window, after-commit, cross-process; m2 file incl. both cross-process cells) | **26/26, 3 of 3 runs** (`int_head_1..3`) | **develop 19/26, 3 of 3 runs**, the same 7 red each time: E9 g0; window; m2 pair; m2 N=20 (16 nulls); in-process G3; G3 cross-process; m2 cross-process. **old head 22/26**: E9 g0, window, n1 ×2. Every red is a product assertion (`expected false to be true`, `memory keeps the revoke… expected true to be false`) | vitest integration config, app role, `--reporter=verbose` | The no-validate E9 controls and the n1 no-rotate controls are green on all three trees. This reproduces the author's "4 red on the old head". |
| 2 | Chain unit file | **5/5 ×3** (`chainunit_head_1..3`) | develop and old head: **5/5 fail on a missing seam** (`withConnectorChain is not a function`, and once `reading 'size'`), not on a product assertion | vitest default config | — |
| 3 | `services/security` unit | **31 files / 336** | — | `npx vitest run` | `vitest list` (default config): 0 entries for ks1549, ks1556-rotate or gate1529r2, against 5 for the chain unit file and 8 for ks577 (controls) |
| 4 | `packages/shared` | **49 / 949** | — | `npm test -w packages/shared` | — |
| 5 | tsc | `-p tsconfig.json` gives rc 0 with 0 lines. A tsconfig extending the service's own, over `index.ts` and the 3 changed test files, gives rc 0 with 0 lines | — | `tsc_head.txt`, `tsc_tests_head.txt` | A planted `const x: number = "x"` in the chain file gave **rc 2 (TS2322)**, so the instrument can fail. The author's "6 pre-existing" errors are outside this scope; I did not chase them. |
| 6 | eslint, 4 changed files | rc 0 | — | `eslint_head.txt` | — |
| 7 | Integration with no env, and with only the superuser URL | **rc 1** both times, "Refusing to run" ×2, 0 passes | — | `int_noenv.txt`, `int_halfenv.txt` | — |
| 8 | My harness `gate1529r2` (19 cells), RC | **19/19 ×3** (`g2v2_head_rc_{a,b,c}`) | develop: **12/19**. Red: A1_pending and A6 (product), plus the 5 chain cells (seam absent; CH2 and CH6 red on product grounds too, see rows 13 and 17) | harness source `gate1529r2.integration.test.ts.txt` (sha256/16 `f8dfa34802840458`) | — |
| 9 | The same harness under RR and SER pool defaults (URL `options`) | **18/19**. The 1 red is `A3_family`, a **pre-existing** revoke-route serialization failure (o1). Every other cell is green | develop RR and SER: **6/19**. ISO, R1 (12/12 bad), R2_grace (10/10 bad), X1 (0/6 ok), A1, A3_family (the same o1 rows), A6 and the chain cells | `g2v2_head_{rr,ser}`, `g2v2_dev_{rr,ser}` | The C0 cell asserts that the service pool really runs RR or SER while a plain app-role session stays read committed, so there is no leak. |
| 10 | ISO: the level each INSERT ran at, 20 rotate+plain pairs | rotates **20/20 read committed** under RC, RR and SER. Plain mints at the pool default 21/21. 0 wrong on backends that had just run a rotate | develop RR and SER: rotates at the pool default | BEFORE INSERT trigger logging `transaction_isolation` | Develop shows the log discriminates. |
| 11 | **X1: a real second replica.** A raw **app-role** connection with the tenant GUC and the pin holds the same advisory lock, inserts, and retires under RLS. The service rotate must wait for it, then retire the replica's key. Grace 0 and 60, 3 trials each | **6/6 ok** under RC, RR and SER. `waitingAdvisory ≥ 1` in **6/6**: the service was really parked on the replica's lock. The replica's retire matched 1 row (RLS bound) | develop RR and SER: **0/6 ok** | pg_stat_activity (`wait_event = 'advisory'`), superuser readback | The author's cross-process cells use a superuser stand-in. Mine uses the app role and the service's own statements, and both agree. |
| 12 | KS-577 forced (BEFORE UPDATE trigger on retire or expiry change), grace 0 and 60 × RC, RR, SER | 201, `priorKeysRevoked` null, 2 active, no expiries, memory seed byte-identical, new key in memory, both keys validate | develop: same | `K577` | — |
| 13 | KS-888 forced (deferred trigger: 2 s sleep at COMMIT, then raise), grace 0 and 60 × RC, RR, SER | 500, no key, DB holds only the seed (active, no expiry), memory seed **byte-identical (whole entry)**, map size unchanged, chain entry gone, seed validates | develop: same | `K888` | — |
| 14 | Memory-only path (no `DATABASE_URL`), through the HTTP route, grace 0 and 60 | 2/2: double-submit gives 201/201, numeric `priorKeysRevoked`, exactly 1 unexpiring active key, `rotateChains.size = 0` (the chain is never used), and the seed is refused at grace 0 and valid at grace 60 | develop: red on the missing seam only (`rotateChains` undefined) | `memonly_head.txt` (`gate1529r2-memonly.test.ts.txt`) | Code read: `index.ts:345-349` is unchanged from develop. |

### The window, the commit and the crash (brief item 4)

| Cell | Result (head, RC/RR/SER, 3 RC runs) | Control |
|---|---|---|
| **A6: the success window** (2 s slow COMMIT that succeeds, sampled at +800 ms) | **mid-commit:** memory seed active with no expiry; DB seed active; chain entry present; the validate answers `true`. **After the 201:** the new key is in memory before the response, the chain entry is gone, and the new key validates. **grace 0:** memory seed `false`, validate `Key revoked`. **grace 60:** memory seed carries the expiry, validate `true`. All 6/6 | develop: mid-commit memory `false` and `Key revoked` at grace 0, product red. Develop at grace 60 **loses the memory expiry** (the mid validate's refresh overwrote it), a #1527 defect that this head fixes. |
| **CRASH** (COMMIT done, memory reset to its pre-commit state) | `GET /api/keys` still lists the seed **active** (stale), but validate is right: seed `Key revoked` at grace 0 and `true` within the grace window at 60; new key `true`. After `loadFromDb()` (a restart's reload), memory agrees with the DB | — |
| **A2** (the entry deleted mid-window, then the COMMIT fails) | Not resurrected; validate warms from the DB and answers `true` | — |

## Brief item 2: who writes shared memory before its DB write commits (read at the head)
Writers of `memApiKeys`: `:241-246`, `:347`, `:376-379`, `:410`, `:463`, `:536-539`, `:1273`, `:1411` (in place) via `:1418`→`:410`, `:1486`, `:1500`, `:1522`, `:1542-1543` (in place).

- **The rotate path (`:344-383`):** none before COMMIT. `:376-379` runs after `transaction()` resolves. Its continuation is a microtask chain, so no request can interleave between the COMMIT reply and the apply.
- **Still memory-before-DB, by design:**
  - `dbSaveApiKey :410` (non-rotate mint; the mint route deletes on failure at `:1273`).
  - The revoke route (`:1411` then `:410`, KS-888 R2: a fail-closed revoke).
  - Usage: `:1542-1543` then `:463`.
  - `revokePriorConnectorKeys :241-246` (memory first). It is now reached only from the memory-only branch, so its DB branch `:248-264` is unreachable in production (o4).
- **Writers that can interleave with an open rotate on its prior keys:**
  - The revoke route.
  - The validate refresh and usage writes. These are safe because the apply re-reads `memApiKeys.get(id)` at apply time and captures no object (A1, A6).
  - `loadFromDb`. **Not measured.** By reading: a reload whose SELECT predates a COMMIT but lands after the apply leaves memory stale, and validate re-reads the DB (pre-existing, o5).
  - `:1486`, deletion of a vanished entry (A2).
- **The revoke route's put-before-save, at this head:**
  - **A3_family** crosses grace {0, 60} × rotate {fails at COMMIT, succeeds} × revoke save {ok, fails} × 2 trials, giving **16 rows per run**.
  - Instruments: the revoke was issued while the rotate was pending (16/16), and its upsert was **waiting on the rotate's row lock in pg_stat_activity (16/16)**.
  - Memory and `GET /api/keys` are read **before** any validate. A validate re-reads the DB and corrects memory, so reading memory after one could hide a wrong value (see the self-corrections).
  - **Result:** in **16/16 rows × 3 RC runs plus RR and SER**, the revoke holds in memory (`false`), in the list (`false`) and in validate (`false`, twice).
  - The round-1 A3 and A3b shapes are the rotate-fails rows. My own new interleaving is the rotate-succeeds rows.
  - The no-rotate control (`A3_control`): a failing revoke gives 500, the DB stays active, and validate gives `false`.
  - **No wrong outcome at READ COMMITTED.** Under an RR or SER default, see o1.

## Brief item 3: the chain (`index.ts:278-304`)

| Cell | Head (5 runs) | Develop (no chain) |
|---|---|---|
| **CH1** timeout (`ROTATE_CHAIN_WAIT_MS=300`; A has a 2 s successful COMMIT; B queued at +100 ms) | B **proceeds** after the wait, logs `waited the whole chain timeout` (3/3), takes a pooled client and parks on the advisory lock (`waitingAdvisory=1`). B finishes after A. DB = [B], memory = [B]. **No error** | DB and memory correct (the advisory lock alone) |
| **CH2** predecessor throws (A fails at COMMIT; B uses the default 10 s wait) | B starts as soon as A settles: **gap 1–7 ms**, not 10 s. B 201; DB and memory = [B]; chain entry gone; **0 DB waiters** (B waited in-process) | 1 DB waiter per trial (red on that instrument) |
| **CH3** a predecessor that never settles (seam, on the rotate's own key), wait 400 ms | rotate 201 after **405–413 ms**. The next rotate takes 3–11 ms, so the hang does not compound. Chain entry gone | seam absent |
| **CH4** 25 connectors × 2 rotates | map size before = after = 0; 0 keys left; 25/25 connectors with 1 active key | seam absent |
| **CH5** the same connector id in **two tenants** | The tenant-2 rotate finishes in **4–13 ms**, while the tenant-1 rotate holds a 2 s COMMIT. Each tenant keeps its own one key. Control: a second rotate in the **same** tenant waits **1806–1815 ms** | seam absent |
| **CH6** pool pressure: 8 of the service pool's 10 clients held, so **2 remain**. A slow rotate plus 3 queued rotates of the same connector, then a validate of an unrelated key | validate **2–9 ms**, **0** service backends waiting on the advisory lock, all 4 rotates 201, 1 active | **validate 1601–1609 ms, 1 backend parked on the advisory lock**. The control discriminates. |
| **W2 widening probe** (not a mutant: the post-COMMIT apply of a `gdelay` rotate is delayed 1500 ms) | **Wait 300 ms:** B finishes before A in 3/3. Memory = {A, B} active and the list shows **A active** while the DB holds only B. Validate refuses A (`Key revoked`) and corrects memory. **Default 10 s wait:** in order 3/3; memory = DB = [B] | — |

**Answer to item 3.**
- **What happens when the wait expires:** the waiter proceeds; it does not error. The database lock still orders the COMMITs.
- **Memory can be applied out of commit order only if a predecessor's apply is delayed after its COMMIT** (W2). In the code that delay cannot occur: `:374-380` is synchronous after the COMMIT promise resolves.
- **A stalled rotate is safe either way:**
  - Stalled before its COMMIT while holding the lock: successors wait in the DB, and COMMIT order equals apply order (CH1).
  - Stalled before taking the lock: a successor can commit first, but it also applies first.
- **Even when forced out of order, the result is cosmetic:** memory and the list are wrong, but validate stays correct (KS-1370).
- **The other properties:**
  - A predecessor that throws does not poison the chain (CH2).
  - A predecessor that never settles is bounded (CH3).
  - Map entries are removed (CH4).
  - The chain is keyed by tenant and connector (CH5).
  - The no-pool-pressure claim is **proven** (CH6, against develop's 1.6 s).

## Mutants (brief item 6), BY CELL NAME
Recipe (`mut2.py.txt`):
- Exact-anchor replacement, where each anchor must occur once; the marker is asserted.
- Each mutant runs the chain unit file, the author's 2 integration files, and my harness at RC. Isolation and lock mutants also run the harness at RR.
- After each mutant, `index.ts` is restored and checked byte-identical by sha256. Final sha `fc2df2aa475ee53e` equals the baseline.
- At RR, the baseline already has `A3_family` red (o1), so it is excluded from the RR kill lists.

**The author's 12 mutants, re-derived from their own table text (`mutants_v6.py`), plus their control: 12/12 KILLED, and the control SURVIVED.** This reproduces their table.

| Mutant | Author's cells that kill it | My harness |
|---|---|---|
| a memory before COMMIT | E9 CONTROL g0, E9 RED g0, E9 CONTROL g60, window | A1_pending, A6, K888 |
| f grace expiry early | E9 CONTROL g60 only | A6, K888 |
| g3 pin skipped on grace (= round-1 **G3**) | RED (G3, CROSS-PROCESS) only | RR: X1 |
| undo restore-by-id | E9 RED g0, window, n1 save-succeeds, n1 save-fails | A1_pending, A3_family, A6 |
| i1 pin removed | both CROSS-PROCESS cells | RR: X1, ISO, CH1 |
| i3 pin = RR / i4 pin = SER | both CROSS-PROCESS cells | ISO, X1, CH1 (+CH4 for SER) |
| lock removed | both CROSS-PROCESS cells | X1, CH1 |
| b chain removed | chain unit ×3, window (the `chains.has` assertion) | **CH2, CH3, CH6** (behavioural) |
| c chain not released on throw | chain unit "THROWS" | CH2 |
| d idle entry kept | chain unit "removes", window | CH2, CH3, CH4, A6, K888 |
| e unbounded wait | chain unit "NEVER settles" | CH1, CH3 |
| zz comment-only CONTROL | none | none |

**Round-1 G1–G4.**
- G1 (undo by id only if the same object) and **G4** (undo restores `isActive` only) have **no target**, because there is no undo. G4's behaviour (an early grace expiry in memory) is the author's `f`, which is killed.
- **G2** (pin inside the savepoint) is re-derived as M6, below. **G3** is the author's `g3`, killed.

**My own mutants (11):**

| Mutant | Result | Killed by (author) | Killed by (gate) |
|---|---|---|---|
| M1 chain key without tenant | KILLED | **window only, by its `chains.has(\`${TENANT}:${c}\`)` string**, an implementation assertion | **CH5** (behavioural: tenant 2 waits on tenant 1), CH3 |
| M2 advisory lock keyed on tenant only | KILLED | both CROSS-PROCESS cells | X1 (RC and RR) |
| M3 memory retires the connector's keys although the retire returned null | KILLED | E8 | K577 |
| M5 pin after the GUC query (round-1 I2) | KILLED | m2 pair, m2 N=20, in-process G3, both CROSS-PROCESS | RR: 14 cells |
| M6 pin inside the savepoint (round-1 G2) | KILLED | the same 5 cells | RR: 12 cells |
| M8 new key not put into memory after COMMIT | KILLED | after-commit, window, E2, E6, E8 | A6, CH1, CH2, K577, R1 |
| M9 bounded wait = 1 ms | KILLED | chain unit ×2 | CH2, CH3, CH6 |
| **M7 grace path skips the post-COMMIT memory expiry** | KILLED **by the gate only** | **none** | A6 (`memSeedExpAfter`) |
| **M10 the chain entry deleted by whoever finishes, not only its owner** | **SURVIVED everything** | none | none |
| **M3b memory retires every in-memory key of the connector instead of the ids the retire RETURNED** | **SURVIVED everything** | none | none |
| M4 chain released before the memory apply (plus a `setImmediate` yield) | SURVIVED: **equivalent** (see below) | none | none |

## Findings

### m1 (Minor, test gap; no product defect measured): four of the chain's and apply's guards are not pinned behaviourally by the PR's cells
- **M10 (`index.ts:302`, `if (rotateChains.get(key) === mine)`)** survives all 26 author cells, the chain unit file and my 19 cells.
  - **By reading, the consequence is:** rotate A runs and B is queued (the map holds B's promise). A finishes and deletes B's entry. A rotate C arriving while B runs then finds no predecessor, so it takes a pooled client and parks on the advisory lock.
  - That is exactly the pool pressure the chain exists to prevent. CH6 shows the cost when the chain is absent: an unrelated validate waited 1.6 s with 2 clients free, and it would get a 503 once `connectionTimeoutMillis` (5 s) is exceeded.
  - Memory ordering is unaffected, because the advisory lock orders COMMITs and the apply runs immediately after each one.
- **M7 (`:379`)**: the grace path's post-COMMIT memory expiry has no cell in the PR. Mine (A6) kills it. The consequence is cosmetic on the DB path, because validate re-reads the stored row.
- **M3b (`:377`)**: no cell pins "retire in memory exactly the ids the database returned".
  - By reading: if a concurrent non-rotate mint of the same connector commits after the retire's snapshot, the mutant would retire that key in memory while the DB keeps it active.
  - Validate's "revoked if either says so" (`:1497-1499`) would then **refuse a valid key** in this process. That is fail-closed, an availability harm.
- **M1** is caught only by the window cell's literal key string. The behaviour (two tenants with the same connector id are independent) is pinned only by my CH5.
- **Severity:** Minor. No credential-validity outcome depends on any of these: every validate on the DB path decides on the stored row. The harms are availability (M10, M3b) and cosmetic (M7). The author's code is correct today; the gap is that a refactor could regress the chain's stated purpose silently.
- **Fix (owner's call):**
  - A chain cell: A in flight and B queued; after A finishes, issue C and assert C waits for B, with 0 service backends on `wait_event = 'advisory'`.
  - A pool-pressure cell like CH6.
  - A grace-60 assertion that the prior key's memory entry carries the expiry after a 201.
  - A two-tenant cell like CH5.

### Observations (not findings against this PR)
- **o1 (pre-existing, latent, outside the diff): under a REPEATABLE READ or SERIALIZABLE pool default, a revoke whose save waits behind a rotate that then COMMITS fails with SQLSTATE 40001.**
  - The route answers 500 "revoke not stored" (`index.ts:1418-1425`).
  - At grace 60, the DB keeps the revoked key `is_active=true` with up to 60 s left, so **other replicas honour it until expiry**. This process refuses it (KS-888 R2).
  - Measured in 2/2 grace-60 rows and 4/4 grace-0 rows per run, where it is harmless because the rotate already retired the key. Head and develop are identical under RR and SER, and it is absent at RC.
  - Nothing sets that default today, which is the same latency class as m2. It belongs in the author's owed revoke-route ticket.
- **o2 (W2): the bounded wait can lose memory order only when the post-COMMIT apply is delayed,** which the code cannot do on its own. When it is forced, the list shows a retired key as active until a validate corrects it.
- **o3: a validate issued before a successful COMMIT can answer `valid: true` after the COMMIT has retired the key.** Its usage UPDATE waits on the rotate's row lock (A6, and `settledWhenMidReturned` in A1). This is a linearisable decision with a late response, and it is pre-existing.
- **o4: the DB branch of `revokePriorConnectorKeys` (`:248-264`) is now unreachable in production.**
  - Its only caller, `:348`, runs only when `!isDbAvailable()`.
  - The function still holds the memory-first-then-DB pattern this PR removes from the rotate path. A future caller on the DB path would bring that pattern back.
  - This was already true on develop.
- **o5: `loadFromDb` (`:536-539`) can leave memory stale** if its SELECT straddles a rotate's COMMIT. Validate stays right. Not measured, pre-existing.
- **o6: `rotateChainWaitMs` uses `parseInt`,** so `ROTATE_CHAIN_WAIT_MS=10s` means 10 ms. That is effectively no chain, so the CH6 pool pressure returns. This is cosmetic hardening.

## Brief item 7: do the cells pin what they claim?
- **Existing cells that assert a defect as intended behaviour:** none in the PR's files. The only one I found is the round-1 gate's own `A1_replaced`, verified above as the known false red.
- **The settled-flag race-landed proofs** (E9 `:412`, n1 `:541`) are read at the instant of **issue**. They fail if the rotate has already settled, so they cannot pass without the race. My `waitingOnRowLock = 1` in 16/16 A3 rows confirms that the revoke's upsert really waited on the rotate's lock.
- **Counters-only exclusion (`:128`):** `usageCount` and `lastUsedAt` are the only two fields a validate changes (`:1542-1543`), and removing either would break the validate rows, so the list is minimal.
  - The positive controls are static checks on the comparator. The product-level bite is the author's `a` and `f` mutants, killed by the E9 rows.
  - **But** `f` (an early grace expiry) is killed only by the **no-validate CONTROL g60 row**. In the validate rows, the mid-window refresh overwrites memory from the DB, so they cannot see it. The control row is therefore load-bearing.
- **The cross-process cells** use a superuser stand-in: no RLS, no GUC, no pin, a plain UPDATE. They do discriminate: `lock_removed`, `M2` and the pin mutants all die on them.
  - My X1 cell uses an **app-role** replica (RLS, GUC, pin, `RETURNING`) and proves the service rotate really parked on the replica's lock in 6/6 trials. They pass for the right reason.
  - The KS-1549 file's RC cross-process cell is green on develop too. It is a guard, not a regression cell.
- **Labelling:** the m2 file's in-process "RED (G3)" cell (`:182-209`) does **not** kill G3. Its own sibling's comment says so. It is a grace double-submit control. Cosmetic.

## NOT tested
- **pgbouncer: UNMEASURED.** There is no `pgbouncer` binary on this machine and the Docker daemon is down (rc 1). A network install is out of bounds.
- A natural, un-widened COMMIT failure. Every window used a 2 s deferred-trigger sleep.
- A real process crash (simulated by resetting memory, then `loadFromDb`), and a COMMIT acknowledgement lost on the socket. By reading, a lost acknowledgement gives a 5xx with no key while the DB has retired the prior key: a connector lock-out, which is pre-existing.
- The M10 and M3b consequences (by reading only). `loadFromDb` racing a COMMIT (o5).
- Multi-replica deployment, the real gateway, and real JWKS. All calls went direct to the service with a locally signed super_admin token.
- Postgres versions other than 15. The author's pre-push preflight (13/16) and their shell suites (86/86). CI still has no integration job.

## Evidence index (`evidence/`)
- **The author's cells:** `int_head_{1,2,3}.txt`, `int_dev_{1,2,3}.txt`, `int_oldhead_1.txt`. Chain unit: `chainunit_{head_1..3,dev,oldhead}.txt`.
- **The round-1 harness at the head:** `r1harness_head_rc_1.txt`, `gate1529_r1harness_head_rc.json`.
- **My harness, authoritative runs:**
  - Text logs: `g2v2_head_rc_{a,b,c}.txt`, `g2v2_head_{rr,ser}.txt`, `g2v2_dev_{rc,rr,ser}.txt`.
  - JSON: `g2_head_rc_v2{a,b,c}.json`, `g2_head_{rr,ser}_v2.json`, `g2_dev_{rc,rr,ser}_v2.json`.
  - Source: `gate1529r2.integration.test.ts.txt`.
  - Memory-only: `memonly_{head,dev}.txt`.
- **Mutants:** `mut2_results.jsonl`, `mut2_console.txt`, `mut2_<id>_{unit,integ,harn_rc,harn_rr}.txt`, and `g2_mut_*.json`. The W2 probe: `mut2_W2_probe_delay_apply_harn.txt` and `g2_mut_W2_probe_delay_apply.json`.
- **Suites and infrastructure:** `unit_head.txt`, `shared_test_head.txt`, `tsc_head.txt`, `tsc_tests_head.txt`, `tsc_tests_planted_control.txt`, `eslint_head.txt`, `vitest_list_default.txt`, `int_noenv.txt`, `int_halfenv.txt`, `migrations_tail.txt`.
- **Scripts:** `pg_setup.sh.txt`, `runint.sh.txt`, `suites.sh.txt`, `mut2.py.txt`, `summ.py.txt`, `summ2.py.txt`.

## Self-corrections (public)
- **The first version of my harness read memory and `GET /api/keys` AFTER calling validate** in A1_pending, A3_family and A6. Validate re-reads the stored row and rewrites memory, so that ordering could hide a wrong memory value.
  - I moved every memory and list read before the first validate, and re-ran everything.
  - The runs `g2_head_rc_1/2`, `g2_dev_rc_1`, `g2_head_rr_1`, `g2_head_ser_1` and `g2_dev_rr_1` (`.txt`/`.json` without `v2`) are **superseded**. Their results did not change after the fix, but they do not count.
- **My first W2 probe made the same mistake.** It reported memory = [B] because a validate had already corrected it. The re-run reads memory first and shows {A, B}. Only the second run is quoted.
- **My first pass at the overlap measure** compared against `c3b66f7f`, which counts the PR's own round-1 files as develop changes (3 false overlaps). I replaced it with the merge-base `af2366e7`, which gives 0, with a control of 4.
- **The setup's `00-init-platform-db.sh` looped,** waiting for `secuura_platform`, because the dblink create failed. I created that database by hand, as in round 1, and the loop exited.
