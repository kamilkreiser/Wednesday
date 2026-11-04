GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 193 (Tier 1, round 2): PR 2004 / KS-1986 v1 verify answers not found, no chain, when the cross-tenant read fails (G192-F2 fix)

## Subject (pinned at start AND end; the same at both)
- **Start** 2026-11-04T22:17:59Z: `git ls-remote origin` on the read-only checkout.
  - `refs/pull/2004/head` = `4432db224a5867fdb6afaabf56df08cdf640d067` (= claimed).
  - `refs/heads/develop` = `e899463d2a0b1b30f2cff46b23d001622620029a` (= Wednesday's read).
  - Evidence: `runs/pin_start.txt`.
- **End** 2026-11-04T22:29:37Z: the same two SHAs (`runs/pin_end.txt`). Neither the head nor develop moved.
- **Commits:** head `4432db224a58` has parent `577f668f478679a3e4965a28fba6b96a9e2212d6`. It is 1 commit on top of round 1, 2 commits over the built base `035685291b9d`, and there are 0 merge commits.
- **Merge tree for the merge seat** (develop `e899463d2a0b`):
  - `git merge-tree --write-tree e899463d2a0b 4432db224a58` gave rc 0, tree **`4048c96cbe5164205355207de0f2cc840c41b780`**.
  - I ran it at the start and again at the end. The output was byte-identical (`runs/merge_start.out`, `runs/merge_end.out`).
- **Host:** macOS, Node v26.8.1 (NOT Node 24), TypeScript 5.9.3, jest 29.7.0, PostgreSQL 15.19 (Homebrew keg).
  - Dependencies came from `npm ci --ignore-scripts` against the head's `Blockchain/Dev/package-lock.json`, then `npm run build -w @secuura/shared` (both rc 0, `runs/npm_ci.log`).
- **Method.**
  - **Clone:** I cloned the read-only checkout with `git clone --shared` into `repo/`. I fetched `refs/pull/2004/head`, develop and the base from GitHub into that clone only.
  - **Harness:** I copied gate 192's PG15 harness and tools into `pgcell/` and `tools/`; gate 192's workdir was only read.
    - I re-keyed them to my own cluster: socket `/private/tmp/g193/s`, port 55493, `listen_addresses` empty, postmaster pid 67578 recorded and stopped.
    - I added Seat F 33rd's three F33 cells verbatim, which gives the seat's 30 cells.
    - I added 19 cells of my own (G193-*), for 49 cells in total.
    - I added probe counters to `rec`.
    - I widened `resetAll` to delete the hash forms my cells rewrite. This changes no cell's semantics.
  - **What the harness drives:** the REAL `verificationRouter` / `verificationV2Router` over HTTP against 11 real databases. The chain is the global-`fetch` stub, and gate 192's call counter is the instrument for chain calls.
  - **Versions:** each version is its committed `verification.ts` blob, overlaid in my clone. After each run it was restored, and the blob was checked equal to head every time.
  - **Comparison:** gate 192's `compare.py`, unchanged.
  - **Process placement:** every test process ran under `env -i` with HOME and TMPDIR in the workdir and CWD in `cwd/`.
  - **Reproduction control:** my base and 577f runs reproduce gate 192's round-1 records byte-for-byte on its 27 cells: 54 SAME + 18 V2-EQUAL against `pg_base2.jsonl` and `pg_head2.jsonl` (`runs/cmp_g192base2_base.txt`, `runs/cmp_g192head2_r1.txt`).

## Findings
No FIX-BEFORE-MERGE and no HOLD-FOR-KAM. G192-F2 is closed on every read-failure form I could drive, on both v1 paths. Nothing outside the chain-fallback rows moved.

### G193-F1 — NOTE: mutant m4 ("flag set on every `judgeAcrossTenants` return") SURVIVES. It is equivalent at the routes, because the only empty-rows successful return (head line 686, round 1's "682") is unreachable
- **FOUND:**
  - The commission expected m4 to kill ("a successful read with no original would then skip the chain"). It does not: 0 of 95 unit cells red, 0 of 116 PG rows differ.
  - The reason is in the code. In both callers, `crossTenantReadFailed` is read only by the chain guard `rows.length === 0 && !crossTenantReadFailed`. `judgeAcrossTenants` returns empty `rows` only at line 681 (read failure, flag already true) and line 686.
  - Line 686 cannot be reached with non-empty `localRows`, and both callers call `judgeAcrossTenants` only when `rows.length > 0`:
    - Line 686 needs a successful read in which no foreign row sits at the union's earliest instant. Then the earliest instant belongs to a local row object.
    - That object is in the originals set of BOTH `certificationEligibility(localRows)` and `certificationEligibility(union)`, because both sets are identified by object and the local minimum equals the union minimum.
    - So `bothEligible(...).certifiedRow` is true for it, and line 679 returns first.
    - `rowCreatedMs` maps an unreadable time to `MAX_SAFE_INTEGER`, never NaN, so the minimum is always attained by some row.
  - So m4 changes the flag only on returns whose `rows` are non-empty, where the guard is already false.
  - **Test gap (not a defect):** no unit cell pins `crossTenantReadFailed: false` on a direct successful `judgeAcrossTenants` call. That is the only place m4 is observable.
- **TESTED:**
  - All 49 PG cells, including 11 aimed at line 686 (see Q4).
  - The three unit files.
  - Probe on line 686: 0 of 98 v1 rows. Control probes fire: line 681 in 20 rows, line 679 in 40 rows.
- **HOW:** `tools/mutants193.py`, `runs/mutants193.json`, `runs/pg_probe.jsonl` (probe build `mut/probe_verification.ts`).

### G193-F2 — NOTE: line 686 (`originals.length === 0` on a successful read) is UNREACHABLE by the code from both routes. It is not "reachable-and-harmless"
- **FOUND:** the code argument is in G193-F1. G192-F2 cannot reopen through this door.
- **TESTED:** 11 driven attempts at PG15, each with the chain UP, so that a reached 686 would show a chain call. Each was run at base, 577f and head. Probe count on 686 was 0 in every row of every attempt. The attempts are listed under Q4.
- **HOW:** a probe build with `logger.warn('G193-PROBE-686')` before the 686 return, plus control probes on 679 and 681. It ran over the whole harness (`runs/pg_probe.jsonl`).

### G193-F3 — NOTE (stated consequence, not new): during a cross-tenant read outage, a caller whose same-hash rows are all certified is told its own document is "not registered"
- **FOUND:**
  - Under every read-failure form with all-certified local rows, head returns the pre-existing not-found body (Q2). It does so although the caller's tenant holds the bytes.
  - Against base (which showed the local `cert-a-1`), this is round 1's ruled D-B4 outage cost. Against 577f, the only rows that change are the chain-fallback rows, which are now LESS.
  - The PR body states this in "For Kam (card secuura-pr2004-ks1986-gate192-hold-1105)". That section also offers a distinct "temporarily unable to verify" wording for Kam to rule.
  - It is stated, so it is not an unstated consequence under this gate's HOLD rule. It is recorded so the reader of the merge sees it.
- **TESTED/HOW:** `runs/analyse_all.txt` (NF=REF rows).

### G193-F4 — NOTE (PRE-EXISTING, base = 577f = head): a foreign original stored with an UPPER-case hex hash is invisible to the originals read, so the caller's own latecomer certification is presented
- **FOUND:** `G193-L686-HASH-UPPER` and `G193-L686-REGISTRY-PREFIXED-TENANT-UPPER`.
  - Setup: B is the original in T2 with an upper-case `content_hash`, it is registered, and A is a certified latecomer in the caller.
  - Result: `cert-a-1` on both v1 paths at all three versions. `ORIGINAL_ROWS_POOL_SQL` binds only the bare, raw and `sha256:` lower forms.
  - This is the "upper-case client hashes stored raw" item that gate 192 left read-only. It is now driven at PG for one form. Unchanged by this PR.
- **TESTED/HOW:** `runs/pg_{base,r1,head}.jsonl`. Whether production holds upper-case hashes was NOT measured.

### G193-F5 — NOTE: the m2/m3 forms as specified (guard reverted to `rows.length === 0`) do not compile under ts-jest at unit level
- **FOUND:**
  - The m2/m3 forms fail with TS6133 ("'crossTenantReadFailed' is declared but its value is never read"), 3 suites failed to run. This matches the seat's own note.
  - On PG (ts-jest diagnostics off) they kill 10 rows each.
  - Valid forms that keep reading the flag (`m2v`/`m3v`: `&& (crossTenantReadFailed || !crossTenantReadFailed)`) kill on both instruments: 2 unit red and 10 PG rows each.
- **HOW:** `runs/unit_m2.out`, `runs/mutants193_m2v_m3v.json`.

### G193-F6 — NOTE: G192-F5's stale "Not measured here" line in the CHEAT fragment stays stale, by Wednesday's ruling
- The cheat blob is unchanged, `5e5e44f2329e` at both 577f and head. Not raised as a defect.

## What passed (measured)
1. **Scope of the delta.**
   - `git diff --name-only 577f668f..4432db22` = exactly 3 paths, with numstat:
     - `routes/verification.ts` 17/6
     - `__tests__/ks1986-v1-original-across-tenants.test.ts` 78/0
     - `Projects Documents/fragments/flow/KS-1986-v1-original-across-tenants.html` 3/3
   - CHEAT is untouched (blob equal). No other path or hunk.
   - The verification.ts hunks are the D-B4 comment (3 lines), plus these head lines:
     - flag declaration, `669: crossTenantReadFailed: boolean;`
     - the single true-set site, `681: if (!foreign.ok) return { rows: [], skipCrossTenantLookup: true, crossTenantReadFailed: true };`
     - `false` at 679, 686 and 698
     - caller locals `930`/`1404 let crossTenantReadFailed = false;` and the copies at `936`/`1410`
     - the guards, `951` (verify-file) `if (rows.length === 0 && !crossTenantReadFailed) {` and `1423` (/verify) the same line
   - **Full range `035685291b9d..4432db22`:** 5 files.
     - The existing-test change is still 2/2. It is the `describe` title and one `expect`, and the blob is unchanged between 577f and head (`7e8d99b9aced`).
     - 0 api-gateway, migration or `verificationV2.ts` paths. The `verificationV2.ts` blob is base = head (`41750ecf1b91`).
2. **G192-F2 closed (PG15, both v1 paths, base / 577f / head).**
   - **`G-CHAIN-UP-REGISTRY-DOWN`:**
     - Base: `cert-a-1`, chain 0.
     - 577f: `cert-chain-x`, chain **1**, with the planted issuer UUID and issuer name in the body (2 canaries). This is the control that fires.
     - Head: chain **0**, 0 canaries in body+headers, and the body is byte-equal to the reference not-found body.
   - **`G-TENANT-POOL-THROWS-ALL-CERTIFIED`** (chain down): base `cert-a-1`; 577f chain 1 then not found; head chain **0**, not-found body byte-equal.
   - **The reference not-found body comes from a different cell:** 577f's `S-LOOKUP-FAILURE-REGISTRY` (chain down). Base's pre-existing not-found branch produces the same body (`S-NO-LOCAL-ROW` verify-file and `G-NO-LOCAL-ROW-PREFIXED-REGISTRY` /verify at base are NF=REF), so the reused body is the existing branch's body in both callers.
   - **Read-failure forms: all reach the single set site (681), probe-confirmed.**

     | form | chain | cells |
     |---|---|---|
     | registry DB missing | up | `G-CHAIN-UP-REGISTRY-DOWN` |
     | registry DB missing | down | `S-LOOKUP-FAILURE-REGISTRY`, `G193-CHAIN-DOWN-REGISTRY-DOWN-ALL-CERTIFIED` |
     | registry SQL error | up | `G193-CHAIN-UP-REGISTRY-SQL-ERROR-ALL-CERTIFIED` |
     | one tenant DB missing | up | `F33-CHAIN-UP-TENANT-DB-DOWN-ALL-CERTIFIED` |
     | one tenant DB missing | down | `G193-CHAIN-DOWN-TENANT-DB-DOWN-ALL-CERTIFIED` |
     | `getPool` throwing | up | `F33-CHAIN-UP-TENANT-POOL-THROWS-ALL-CERTIFIED` |
     | `getPool` throwing | down | `G-TENANT-POOL-THROWS-ALL-CERTIFIED` |
     | tenant originals SQL error | up | `G193-CHAIN-UP-TENANT-SQL-ERROR-ALL-CERTIFIED` |
     | tenant originals SQL error | down | `G193-CHAIN-DOWN-TENANT-SQL-ERROR-ALL-CERTIFIED` |

     - Result over these 10 cells × 2 paths = 20 rows at head: chain calls **0**, canary hits 0, not-found body byte-equal 20 of 20, HTTP 200, 0 `logger.error`.
   - **Mixed local sets** (an uncertified row plus a certified A) under each failure form with the chain up (`F33-CHAIN-UP-REGISTRY-DOWN-MIXED-LOCAL`, `G193-CHAIN-UP-TENANT-POOL-THROWS-MIXED`, `G193-CHAIN-UP-TENANT-DB-DOWN-MIXED`, `S-LOOKUP-FAILURE-TENANT`, `G-TENANT-POOL-THROWS`):
     - These return at 679 and do NOT reach the flag. That is correct, because rows are non-empty and the chain is never asked.
     - Chain 0 and no certification at 577f and head.
   - **Successful-read control** (`G193-CHAIN-UP-REGISTRY-UP-NO-FOREIGN-ALL-CERTIFIED`): `cert-a-1` at all three, chain 0.
3. **Nothing else moved.** Matrix = 30 cells (gate 192's 27 + Seat F 33rd's 3) × 2 v1 paths = **60 v1 rows + 18 v2 rows**.
   - **Row-count reconciliation:** the 6 extra rows over gate 192's 54 are `F33-CHAIN-UP-TENANT-POOL-THROWS-ALL-CERTIFIED`, `F33-CHAIN-UP-TENANT-DB-DOWN-ALL-CERTIFIED` and `F33-CHAIN-UP-REGISTRY-DOWN-MIXED-LOCAL` × 2 paths. They are v1-only, so v2 stays 18.
   - **(a) NEW:** 577f→head **0 of 60**; base→head **0 of 60**.
   - **(b) DIFFERENT:** 577f→head **0 of 60**. base→head **8 of 60**, by cell:
     - `S-FOREIGN-ORIGINAL-CERTIFIED` `cert-b-own` ×2: the original holder's own.
     - `G-THREE-TENANTS-TIED` `cert-y-1` ×2: Y holds a tied original, so the original holder's own.
     - `G-ORIGINAL-UNREGISTERED` `cert-y-1` ×2: a latecomer (G192-F1).
     - `G-CAP-9-SKEWED` `cert-y-2` ×2: a latecomer (G192-F1).
     - That is 4 original holder's and 4 latecomer's. All 8 have `certifierOrganizationId null` and `certifiedBy null`.
     - Base→577f over the 60 rows was 14 DIFFERENT: these 8, plus the 2 gate-192 chain rows, plus the 4 F33 chain rows.
   - **(c) LESS:** 577f→head **6 of 60**, each a chain-fallback row: `G-CHAIN-UP-REGISTRY-DOWN`, `F33-CHAIN-UP-TENANT-POOL-THROWS-ALL-CERTIFIED` and `F33-CHAIN-UP-TENANT-DB-DOWN-ALL-CERTIFIED` × 2 paths. Each went `cert-chain-x` (chain 1, 2 canaries) → not found (chain 0, 0 canaries). SAME 54. SAME-CERT 0.
     - Over my 19 extra cells, 577f→head is LESS 4 (the two chain-up SQL-error read-failure cells × 2) and SAME 34.
     - Over all 98 v1 rows: NEW 0, DIFFERENT 0, LESS 10 (every one a read-failure chain-fallback row).
   - **(d) v2 equal:** base→head 18 of 18, 577f→head 18 of 18, base→577f 18 of 18.
   - **(e) `G-CONTROL-NO-LOCAL-CHAIN-UP`:** at base, 577f AND head: `cert-chain-x`, chain 1, 2 canaries (planted issuer UUID and name) on both paths. The pre-existing chain-branch exposure is UNCHANGED, so the guard is not wider than claimed.
   - **(f) Disclosure** (5 planted values; whole body + headers):
     - DB-sourced head v1 matrix rows: **0 of 56** with hits. The 60 rows minus 2 `G-CONTROL-LOCAL-CANARY` rows and 2 chain-sourced control rows leave 56.
     - Controls fire in the same action:
       - `G-CONTROL-LOCAL-CANARY` 3 and 3 at all three versions;
       - gate 192's scrub-drop mutant at head hits 6 rows (`S-LEAK-CANARY`, `S-FOREIGN-ORIGINAL-CERTIFIED`, `G-THREE-TENANTS-TIED` × 2: title + issuer name) (`runs/pg_scrubdrop.jsonl`).
4. **Line 686 (round 1's "682").**
   - **(a) Code:** see G193-F1/F2. Reaching it needs a successful read whose foreign rows are all later than the earliest local row, while no local row is eligible. The earliest local row is always eligible, so it is unreachable.
   - **(b) My attempts.** All are driven at PG15 with the chain up and probe-counted. Each was **not reached** (probe 686 = 0) on both paths at head:
     - `G193-L686-EMPTY-TENANT`: the registry lists T2, and T2 holds nothing. The local `cert-a-1` answers.
     - `G193-L686-TENANT-ROW-DELETED`: B was registered, then deleted from T2. Local `cert-a-1`.
     - `G193-L686-HASH-UPPER`: B in T2 upper-case. Local `cert-a-1` (G193-F4).
     - `G193-L686-REGISTRY-PREFIXED-TENANT-UPPER`: Local `cert-a-1`.
     - `G193-L686-HASH-PREFIXED-IN-TENANT`: B stored as `sha256:`, registry bare. Found by the three-form read, so D-B2 presents B without a certification.
     - `G193-L686-ALL-REVOKED-FOREIGN`: every T2 row revoked. The originals SQL has no status filter, so D-B2 shows revoked B.
     - `G193-L686-FOREIGN-LATER`: T2 holds only a row later than A. Local `cert-a-1`.
     - `G193-L686-NULL-CREATED-BOTH`: the foreign MIN is NULL, so the originals read is empty. Local `cert-a-1`.
     - `G193-L686-NULL-CREATED-LOCAL`: D-B2 presents B.
     - `G193-L686-CALLER-ONLY-REGISTRY`: all foreign rows deduped. Local `cert-a-2`.
     - `G193-L686-CALLER-TENANT-ALIAS`: T2's pool is the caller's DB, so every row is deduped by id. Local `cert-a-1`.
     - Verdict: **unreachable** by the code (not merely "not reached").
   - **(c) The seat's probe** (READY line 28 and PR body): a counter on the return fired 0 of 95 unit cells and 0 of 78 PG rows, with the control on the read-failure return firing 6 and 10. Its mutant m-d (flag also set on 682) survives and was judged equivalent. My result agrees.
5. **Mutants** (committed bytes, every anchor count 1, every restore blob-equal to head, final blob equal; raw table counted from `runs/mutants193.json` + `runs/mutants193_m2v_m3v.json`):

   | mutant | what | unit red (of 95) | PG rows ≠ head (of 116) | result | killed by (e.g.) |
   |---|---|---|---|---|---|
   | m1 | flag never set | 4 | 20 | KILLED | `G-CHAIN-UP-REGISTRY-DOWN` both paths |
   | m2 | verify-file guard → `rows.length === 0` | 0 (TS6133, 3 suites failed to run) | 10 | KILLED (PG) | `G-CHAIN-UP-REGISTRY-DOWN` verify-file |
   | m2v | valid m2 | 2 | 10 | KILLED | same |
   | m3 | /verify guard → `rows.length === 0` | 0 (TS6133) | 10 | KILLED (PG) | `G-CHAIN-UP-REGISTRY-DOWN` /verify |
   | m3v | valid m3 | 2 | 10 | KILLED | same |
   | m4 | flag true on every return | 0 | 0 | **SURVIVED (equivalent, G193-F1)** | — |
   | m5a | flag only on the registry-read failure | 2 | 12 | KILLED | `F33-CHAIN-UP-TENANT-POOL-THROWS-ALL-CERTIFIED`, `F33-CHAIN-UP-TENANT-DB-DOWN-…` |
   | m5b | flag only on tenant-read failures | 2 | 8 | KILLED | `G-CHAIN-UP-REGISTRY-DOWN` |
   | m6 | guard `rows.length === 0 \|\| crossTenantReadFailed` (as written) | 4 | 20 | KILLED | `G-CHAIN-UP-REGISTRY-DOWN` |
   | m6b | GATE: negation dropped (`&& crossTenantReadFailed`) | 9 | 24 | KILLED | `G-CONTROL-NO-LOCAL-CHAIN-UP` |
   | m7a | verify-file not-found message altered | 2 | 11 | KILLED | `G-CHAIN-UP-REGISTRY-DOWN` verify-file |
   | m7b | /verify not-found message altered | 2 | 11 | KILLED | `G-CHAIN-UP-REGISTRY-DOWN` /verify |

   - Headline = table: 12 run, 11 KILLED, 1 SURVIVED (m4, equivalent).
   - What I tried to separate m4: all 49 PG cells, including the 11 line-686 attempts, and the three unit files. No route-level input separates it (G193-F1).
6. **G192-F1 ticket: live board read UNMEASURED.**
   - The gate holds no Linear identity. The instrument that closes it is a Wednesday-side `linear_*` read of KS-1991.
   - The READY gives the id KS-1991 and no URL. The seat's filing record gives the URL `https://linear.app/secuura/issue/KS-1991/verify-by-hash-shows-a-later-tenants-certification-when-the-originals` (`seatF-33rd/evidence/file_ticket_real.out`).
   - From the seat's read-back of the live description (`evidence/ks1991_live_description.md`):
     - it carries facts only;
     - it names both cells `G-ORIGINAL-UNREGISTERED` and `G-CAP-9-SKEWED` with v1 and v2 outcomes;
     - reachability is marked "read from code … NOT measured";
     - it claims no fix ("how to fix it is a design choice for Kam");
     - it names no ruling: it cites the card's default as "open". That was true at filing (~21:48Z, before the 22:05Z ruling).
   - The seat's own read-back printed `body equal (bullets normalised) False`. The read-back text shows Linear's markdown normalisation (`*` bullets, `[url](<url>)` links). I did not verify that from the board myself.
7. **PR body.** Read from the seat's read-back files `seatF-33rd/pr/body_after.md` and `edit_real.out` ("readback by number: body equal True | title unchanged True | head 4432db224a58 | state open"), NOT live. The gate holds no Secuura GitHub identity.
   - Lines 1-2 are byte-identical before and after (`body_before.md` vs `body_after.md`).
     - Line 1 is Kam's release line (card wed-morning-fleet-activity-1105 = a, 07:07:25 AEDT).
     - Line 2 is the supersede of the commit body's HOLD line.
   - The "For Kam (card secuura-pr2004-ks1986-gate192-hold-1105)" section is present. Quote: "On a cross-tenant read failure v1 now answers with the existing not-found body (verify-file: 'This document is NOT in the Secuura registry...'; /verify: 'This document hash is not registered...'), although the caller's tenant holds the bytes; …". The body is measured as reused unchanged (Q2).
   - G192-F4 and G192-F5 appear as notes only ("Not changed here." / "Not edited this round.").
   - Title `Refs KS-1986: v1 verify judges the original registration across tenants, as v2 does` = **83 chars** (≤ 92).
   - Close words before a key: 0 in the body and 0 in both commit messages. The regex control fires 2 on a planted "Fixes KS-1986 and closes #2004".
   - Nothing in the body claims more than the delta does: "Unchanged: … `readCrossTenantOriginals`" holds by the diff.
8. **Merge tree:**
   - rc 0, tree `4048c96cbe5164205355207de0f2cc840c41b780` on develop `e899463d2a0b`. Base is an ancestor of develop.
   - Shared paths between `035685291b9d..develop` (9 files: KS-1401 migration 058 and its test, KS-1958 vc-issuer, 4 fragments) and the PR's 5 paths: **0**.
     - Controls: the PR against itself gives 5; a planted develop list plus `verification.ts` gives 1.
   - Per-path blob in the merge tree vs head: **5 of 5 EQUAL**. `diff --numstat develop..tree` = the PR's 5 files with the PR's own counts.
   - develop's `verification.ts` blob = base's (`484c0a65d8a9`).
9. **Suites and static checks at head:**
   - **Unit files:** the three KS-1561/KS-1986 unit files **95 of 95**.
   - **Whole originate suite:** **2,485 of 2,485 tests, 210 of 210 suites**, rc 0. That is gate 192's 2,475 at 577f, +10 (the 10 new KS-1986 cells: 24 → 34).
   - **tsc:**
     - `tsc --noEmit -p services/originate` rc 0, 0 errors.
     - tsc over verification.ts + the 3 test files with jest types: rc 0, 0 errors. Planted control rc 2, 1 error.
   - **eslint** on verification.ts, the KS-1986 test and the KS-1561 g188 test: rc 0, 0 problems. Planted control rc 1, 2 problem lines.
   - **docs-fragments:** `docs-fragments.mjs check` clean rc 0. Planted dangling `<!--ref:KS-9999-g193-…-->` rc 1. Restored (git diff clean) rc 0.
   - **Red proof:** head's KS-1986 test file against 577f product bytes gives **4 of 34 red**, exactly the 4 "F2 … CHAIN UP" cells (registry down / one tenant pool down × 2 paths). All are by assertion (`expect(chainCalls(f)).toBe(0)`, Received 1). 0 TS diagnostics (planted control 1), 0 TypeError. The same file at head is 34 of 34.
   - My clone's `git status` was clean after every step.

## NOT tested
- Node 24 (ran on Node v26.8.1).
- A real deploy, demo, kintsugi, real Platform S traffic, and the real anchoring service (the chain was a global-fetch stub). Production data volume and index behaviour.
- How many production hashes G192-F1 reaches. It is NOT fixed by this PR and is ticketed as KS-1991.
- How many production rows hold upper-case hashes (G193-F4).
- The real tenant manager / `runWithTenantId` / RLS GUCs: stubbed by the seam. The request `db` and the caller's tenant pool were the same database here.
- Lineage walks (stubbed) and `/verify`'s by-documentId strategy.
- `verificationV2.ts` beyond base = head blob equality and the 18 v2 rows.
- The four platform suites (Schemathesis, Akto, Playwright, k6), the KS-380 preflight, and CI checks on the PR.
- A live GitHub read of the PR title and body (taken from the seat's read-back files), and a live Linear read of KS-1991 (UNMEASURED; taken from the seat's read-back).
- The line-686 probe at unit level. I probed only the PG harness; the seat reports 0 of 95 at unit level, which I did not re-run.
- Timing and timeout behaviour of a slow (rather than failing) registry or tenant read.

## Plain answer for Kam
- **What the merge changes for users:** if the cross-organisation check fails, and everything the visitor's own organisation holds for that file is a certified copy, the public verify page now says the document is not registered.
- **What round 1 would have done instead:** in that case it asked the blockchain service and showed the chain's certificate, including that issuer's organisation ID and name. That no longer happens, on either verify path. I checked five different kinds of failure, with the blockchain both up and down.
- **Two consequences:** everything else the page shows is exactly as in round 1, and the blockchain answer for a file nobody in the platform holds is unchanged.
- **The cost:** during such an outage, that visitor sees "not registered" for a file their own organisation holds. The PR names this cost, and offers a gentler "temporarily unable to verify" wording if you want one.
- **Still open:** the first-round issue where a later copier in another organisation can be credited (G192-F1) is not fixed by this PR. It is filed as ticket KS-1991.
