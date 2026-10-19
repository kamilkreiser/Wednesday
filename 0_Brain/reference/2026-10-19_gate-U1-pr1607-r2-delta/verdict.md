VERDICT: GO at head 243d324d4dd7e9ac5e277b2ac0b8566f54d32a30 (round 2 of 2, delta, tier 1 Opus; landing tree 5adb4e513696 on develop ce98606212e4)

# Gate U1 verdict: PR 1607 round 2 (KS-1385 (b), T1's MIN-1 + MIN-2), anchoring BOOTED

- **Head gated:** `243d324d4dd7e9ac5e277b2ac0b8566f54d32a30`, one commit on round 1's `c241bb8624bc5e0f49dfb85ec135997da0864c18`. **Develop:** `ce98606212e4e0dce8212d4541ffff2484f2217b`.
  - ls-remote at 04:18:03Z and again at 04:39:27Z: both refs unchanged between the two reads.
  - Author and committer: `Kam Kreiser <kamil.kreiser@secuura.ai>`.
- **Setup:** findings only. The project checkout has 0 tracked changes, before and after. No push, no GitHub or Linear write, no Docker, no real Cardano network, no `cd`, no `rm`.
- **Scratch:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/u1/` (`scripts/`, `cells/`, `logs/`, `wt/{head,dev,r1,land}`, `repo/`).
  - I re-used T1's scripts and cells, copied into u1. The only changes are the paths and the ports. I did not touch T1's own scratch.
  - My own PG 15 ran on 55891, built with T1's mkpg method: `applied=53 failed=0`. Redis ran on 55892 and anchoring on 55893. All three ports were free before use and are stopped now.
- **Counts:** Major 0. Minor 0. Info 5.

## Q1. Delta scope
- **HOW:** `git diff --stat c241bb8624bc 243d324d4dd7`.
- **Result:** **3 files, +130/-12**, exactly as J claimed:
  - the main KS-1385 integration file (+96/-2);
  - `anchorOverwriteGuard.ts` (+21/-0);
  - `index.ts` (+25/-10).
- **What the delta contains, and nothing else:**
  - MIN-1: two `jsonb_typeof` guards, one in the merge's `jsonb_each` and one in the `RETURNING` `rest_is_incoming`;
  - MIN-2: the inline log split moved into a pure `classifyPersistOutcome`, called at the one site, with the W4 source pin updated;
  - the new cells: I8 ×10, I9 ×10, and L1-L5.
- **The PR as a whole** (`develop...head`) is still the same 4 anchoring files, +282/-10.
- **Logic equivalence:** I compared `classifyPersistOutcome` against round 1's inline conditions by reading them side by side. It gives the same info and warn outcome for every combination of `row` / `payload_is_incoming` / `rest_is_incoming` / `holdsIssuerFields` / `isQuietKeep`.

## Q2. MIN-1 closed? YES, for every stored shape, booted, both callers
**HOW:**
- **Booted cell:** `cells/odd.ts`, built on T1's booted cell, whose helpers are verbatim. Logs: `logs/cell_odd_odd_{dev,r1,head}.log` and `logs/anchoring_boot_odd_*.log`.
- **Per cell:**
  - the issuer anchors normally;
  - the stored `metadata_payload` is set by the owner to the shape;
  - then the HOLDER (admitted, a colleague in the custodian org) or THIRD (refused) re-anchors through the real HTTP route with the holder's four and actor.
- **Trees:** run on develop, on round 1 (the inverted control) and on the head. 10 shapes × 2 callers = 20 cells per tree.
- **SQL level:** I also re-ran T1's own `cells/q4.ts` on all three trees (`logs/q4_*.log`), with two shapes added: payload JSON null and payload number.

| Stored shape | HEAD holder | HEAD refused | R1 (round 1) | DEVELOP |
|---|---|---|---|---|
| `secuura` JSON null / string / array / number | 202, rest applied (actor = holder), four ABSENT, 1 info line | 202, payload byte-identical, 1 warn | holder **500** on all 4; refused **500** on null, string and number | 202 everywhere; holder gets the holder's four |
| no `secuura` key `{}` | 202, applied, four absent, info | 202, kept, warn | 202 | 202 |
| payload SQL NULL | 202, applied, four absent, info | 202, kept, **no line** | 202 | 202, no line |
| payload JSON null / string / number | 202, applied, four absent, info | 202, kept byte for byte, warn | refused **500** on all three (J's 3 extra shapes, confirmed) | 202, warn |
| payload array | 202, applied, four absent, info | 202, kept, warn | 202 | 202, warn |

- **Refused caller = develop byte for byte:** **10/10**. That covers the status, the response `data` key set, the message, the stored payload text before and after (`::text`), and the presence of the warn line.
  - Warn totals: head 9, develop 9. The SQL NULL cell is silent on both.
- **Admitted holder:** 10/10 answered 202; the rest applied; the issuer fields absent; 10 info lines.
- **Errors:** 0 occurrences of 22023 in the head's boot log, against 20 in round 1's.
- **T1's q4 at the SQL level on the head:** all 33 stored-shape × mode cells are OK (holder, issuer and refused). On r1 the same probe reproduces T1's raises.
- **Residual: see INF-1.** An INCOMING non-object `secuura` still raises. No route builds one.

## Q3. MIN-2 closed? YES
**HOW:** `scripts/mutants_u1.py` (`logs/mutants_u1.log`).
- Each mutant ran the KS-1385 trio (89 cells loaded each time).
- Each "booted" mutant also ran T1's booted cell.
- After every mutant I verified the restore by sha256: `index.ts 4b398c9bb1fa…`, guard `42ef8af92246…`.

| Mutant | Committed suite | Booted (info / warn; head baseline 6 / 2) |
|---|---|---|
| C0 comment-only control | survives (89/89) | n/a |
| **UT1 = T1's mutant, re-expressed where the split now lives** (the held branch of `classifyPersistOutcome` forced false) | **KILLED: L1 + I8 ×10** (11 red) | 0 / 8 |
| UT1b, T1's mutant at the call site (`if (false && outcome === 'held-issuer-fields')`) | KILLED: W4 (source pin) | 0 / 2 |
| UT1c (mine): the call site forces `row.rest_is_incoming = false` before classifying, leaving W4's three lines intact | **survives (89/89)** | 0 / 8; killed only booted (INF-2) |
| UM9 merge back on `COALESCE` (round 1's merge read) | KILLED: I8 ×4 (the 4 non-object `secuura` shapes) | n/a |
| UM10 (mine) payload-level `jsonb_typeof` dropped from `RETURNING` | survives. **EQUIVALENT:** `->'secuura'` on a non-object yields SQL NULL, so the CASE falls to ELSE either way | n/a |

- **Is `classifyPersistOutcome` exercised on real rows from the real statement?** **YES.**
  - L1-L5, I8 and I9 call it on `persistWith(...).row`. That row is the RETURNING row of the product's statement, extracted from `index.ts` source as the harness extracts it. The binds are assembled by the test and pinned by W2.
  - The call site in `dbPersistAnchor` is pinned by W4 (source) and by the booted cell.
- **Answer:** a COMMITTED cell now reds T1's mutant: L1, plus I8 ×10.

## Q4. Round 1's booted scenario on the new head: still YES
- **HOW:** T1's `cells/booted.ts` via `scripts/07_boot.sh head q4head`. Logs: `logs/cell_booted_q4head.log`, `logs/anchoring_boot_q4head.log`.
- **S1b holder re-anchor:**
  - the stored four are the issuer's (`org-issuer-x`, `zORGISSUER`, government, true), with actor `zHOLDERACTOR`;
  - verify-by-hash returns 200 with the same;
  - chain4 is the issuer's four, chainActor `zHOLDERACTOR` (submission #2).
- **The four controls:**
  - C1c, the issuer replaces the four: `org-issuer-x2`, `zORGISSUER2`, kyc, false;
  - C2b, refused: payload md5 unchanged (`cf829255ab` → `cf829255ab`), chain actor `zISSUERACTOR`;
  - C3b and C3c, omitted fields: the four are kept;
  - C4a/b, a row first anchored without the four: stays `{}`.
- **Extras:** E1 keeps the first four, and B1b leaves the single row unchanged.
- **Responses and log lines:** every POST answered 202. 6 info lines and 2 warn lines, identical to T1's round-1 head figures.

## Q5. `allow` unchanged; no option (c)
- **The guard file:** `git diff develop..head -- anchorOverwriteGuard.ts` has **0 `-` lines and 34 `+` lines**:
  - `ISSUER_FIELDS` and `holdsIssuerFields` (round 1);
  - `PersistOutcome` and `classifyPersistOutcome` (round 2), which only read a decision.
  - So `decideMetadataOverwrite`, `mayOverwriteStoredMetadata`, `readOwningDocument`, `isQuietKeep`, `isUuidShaped` and `CUSTODY_OPTION` are byte-identical to develop.
- **`index.ts`:** `overwrite = await mayOverwriteStoredMetadata(...)` (`:1369`) and the `$23` bind `overwrite.allow` (`:1497`) are unchanged. The outer `WHEN $23 AND hash AND type` is unchanged.
- **The moved develop:** develop's own delta (9512cc70..ce98606) touches 0 anchoring files.
- **Option (c):** no line admits the issuing organisation on a no-issuer row. The only "(c)" in the guard is the earlier custody card's `CUSTODY_OPTION = 'c'`, which is on develop.

## Q6. Landing on the moved develop
- **Predicted tree:** `git merge-tree --write-tree ce98606212e4 243d324d4dd7` gives rc 0, tree **`5adb4e513696128baa072f371f8145997c88554d`**, equal to J's prediction.
  - Landing tree vs develop: exactly #1607's 4 files, +282/-10.
  - Landing tree vs head: exactly develop's 3 files (`scripts/__tests__/ks998_pre_push_judges_the_push.test.sh`, `scripts/__tests__/preflight_deps.test.sh`, `scripts/preflight/preflight.sh`), +89/-2.
  - The delta touches `scripts/`; it does not touch `.githooks/`. Its leg-14 code reads `.githooks/pre-push`.
  - The scratch landing commit is `7318dc88ba31` (worktree `wt/land`). It exists only in the scratch clone and was never pushed.
- **Shell suites ON THE PREDICTED TREE** (`scripts/run-shell-suites.sh`, run under `env -i` as leg 14 de-slots):
  - `--check-unreached`: rc 0, `all 91 tracked shell suite(s) are reached`.
  - **Run 1:** 89/91 (`logs/shell_land_run1.log`). Both reds were my harness:
    - `ks949_main_seed_idempotence`: postgres refused to start, `postmaster became multithreaded… Set the LC_ALL environment variable`. My `env -i` stripped `LANG`.
    - `preflight_test_types_ratchet_leg`: the real tsc of auth, the api-gateway and vc-issuer needs those services' installs, which my worktree did not link.
    - With `LANG/LC_ALL` set and every service's `node_modules` symlinked, both pass on the landing tree AND on develop (27/27 and 38/38 each). Logs: `logs/shell_{land,dev}_*.log`.
  - **Run 2, the full set, fixed harness:** **`shell suites: 91 passed, 0 failed, 0 skipped (of 91)`**, rc 0, 517 s (`logs/shell_land_run2.log`).
- **Anchoring on the landing tree:**
  - KS-1385 integration trio 89/89 (`logs/int_land_owner_1.log`);
  - unit 379/380, the red being `threadTokenMint.test.ts`, the same KS-562 red T1 recorded on develop;
  - `tsc` rc 0, 0 lines.
- **Anchoring on the head:** the trio was 89/89 in each of 2 serial runs.
- **Hook timeouts:** 0 `beforeAll` hook timeouts in any run.

## Q7. NOT tested
- **Not driven by me:**
  - the in-hook preflight run (legs 1-16 as the pre-push hook drives them, including slot targeting);
  - ESLint;
  - the four platform suites (no Docker);
  - preflight legs 3, 4 and 8.
- **Anchoring integration:** only the 3 KS-1385 files make up the lane, and all were run. Develop's anchoring unit/tsc was not re-run at ce98606; its anchoring tree equals 9512cc70's, which T1 measured.
- **Repetition:** J's 5-run, one-database repetition was not repeated. I ran the head trio 2× serial, plus 1× on the landing tree, plus 6 mutant runs.
- **Mutants:** J's M1-M8 and M12 were not re-run individually. T1 measured M1-M8 on round 1, and none of their anchors moved in this delta except W4's.
- **Out of scope here:** originate (not booted; the holder verbs through `x-emitter-internal` were not driven), the gateway, real Cardano, `buildAnchorTransaction`, multi-tenant mode, Prisma, real boxes' stored rows.
- **Overlap with open PRs (#995 and others):** not re-checked; I relied on T1's round-1 result. Develop's new commit touches none of the 4 files.
- **The PR body and Linear links** J reports: not read, because no GitHub API was used.

## INFO
- **INF-1 (residual MIN-1, unreachable): an INCOMING non-object `secuura` still raises 22023 on the head.**
  - **Cells** (`logs/q4_head.log`): a fresh INSERT whose incoming `secuura` is null (I1), and a holder whose incoming `secuura` is null or a string (X2, X3). They raise on the head and on r1, and pass on develop.
  - **Mechanism (inferred, not measured):** `($9::jsonb->'secuura') - $25::text[]` in the `RETURNING` CASE is built from parameters only. Postgres constant-folds it at plan time, so the `jsonb_typeof` guard (which tests the STORED column) cannot short-circuit it. The merge's `COALESCE(EXCLUDED…->'secuura') - $25` behaves the same way.
  - **Not reachable:** both `dbPersistAnchor` callers (`:507` single via `buildFlatAnchorMetadataPayload`, and `:804` batch) build `secuura` as an object (`anchorSchema.ts:264-266`, `index.ts:779-780`).
  - It is outside T1's MIN-1, which concerned stored rows, and it is not new in round 2.
- **INF-2 (residual MIN-2): the call site's hand-off to the classifier is pinned by source text plus the booted cell only.**
  - Mutant UT1c survives the committed suite and is killed only by the booted cell (info 6 → 0, warn 2 → 8). UT1c corrupts `row` between the statement and `classifyPersistOutcome` while leaving W4's three pinned lines intact.
  - This is narrower than T1's MIN-2, because the decision itself is now pinned on real rows. It is a test-coverage note, not a defect: the behaviour on the head is correct, as measured.
- **INF-3 (unreachable): a holder's incoming payload with NO `secuura` key** (X1) yields `rest_is_incoming` = SQL NULL on the head (true on r1). It would classify as `kept`, so the update would apply but the warn line would fire. No builder emits such a payload.
- **INF-4:** UM10 is an equivalent mutant. The payload-level `jsonb_typeof(metadata_payload) = 'object'` conjunct is redundant but harmless, so its survival is not a coverage gap.
- **INF-5 (harness, for the next gate):**
  - running `run-shell-suites.sh` under a bare `env -i` reds `ks949` (locale), and a gate worktree without every service's install reds the ratchet leg;
  - the hook's own environment has both, so this is a harness lesson, not a product finding;
  - the `node_modules` symlinks show as untracked in scratch worktrees (`node_modules/` does not ignore a symlink).

Merge only on Wednesday's head-bound GO; the squash must land tree `5adb4e513696` on develop `ce98606212e4`, re-predicted if develop moves. Nothing deploys from this verdict.

MODEL: claude-opus-5-5
WALL-CLOCK: 31 min (04:17Z to 04:48Z, 2026-10-19)
sha256: 016dd217fbdc9601ceddeb955c97c683f1d8e69662e4401f95b530a034e265bc (of this file with its first and last lines removed: sed '1d;$d' | shasum -a 256)
